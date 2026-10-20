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
session id: 01a1521f-bc8f-7f11-8159-a5763393db10
--------
user
Pre-dispatch security review (read-only, security profile) of the task text .orchestration/tasks/dotfiles-T133-dispositions-a02.md and its threat_table, before any implementation exists. Judge the design the text states: can the controls it names bind what actually executes on this host (mise shims first on PATH, same-user worker processes, gh outside the sandbox on Linux, symlinks and case-insensitive filesystems, inherited GIT_* environment)? Check every threat row: a closed row whose named test cannot close it, a residual row whose control does not mitigate the risk, a missing row for a file or non-path control, and any gap of the class decision-not-bound-to-execution (a decision made on text or on a validated copy while the execution resolves binaries, files or ledgers from an attacker-influenced place). Read the related acceptance records and reviews the text cites for context. Report each finding as [P0-P3] <confidence> <file:line> <one line>; findings are input for the orchestrator, who decides. End with exactly one line: Verdict: correct or Verdict: incorrect.
warning: loading hooks from both ~/.codex/hooks.json and ~/.codex/config.toml; prefer a single representation for this layer
hook: SessionStart
hook: SessionStart
hook: SessionStart Completed
hook: SessionStart Completed
hook: UserPromptSubmit
hook: UserPromptSubmit Completed
codex
🤖 I read the AGENTS.md for mryfmo/dotfiles.
I’ll use the agmsg-orchestration and Ponytail review instructions to assess the stated controls and cited evidence, keeping the review read-only.

exec
/bin/zsh -lc pwd in ~/Workspace/dotfiles
 succeeded in 0ms:
~/Workspace/dotfiles

exec
/bin/zsh -lc 'cat ~/.agents/skills/agmsg-orchestration/SKILL.md' in ~/Workspace/dotfiles
exec
/bin/zsh -lc 'git status --short; nl -ba .orchestration/tasks/dotfiles-T133-dispositions-a02.md' in ~/Workspace/dotfiles
exec
/bin/zsh -lc 'cat ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail/SKILL.md' in ~/Workspace/dotfiles
 succeeded in 96ms:
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

 succeeded in 132ms:
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

 succeeded in 180ms:
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
?? .orchestration/acceptance/dotfiles-T129-anthropic-auth-runtime-check-a01.md
?? .orchestration/acceptance/dotfiles-T129-assets-omp-hcom-followup-a02.md
?? .orchestration/acceptance/dotfiles-T129-audit-inherit-replan-json-followup-a01.md
?? .orchestration/acceptance/dotfiles-T129-audit-inherit-replan-json-followup-a02.md
?? .orchestration/acceptance/dotfiles-T129-hcom-dispatch-bus-a01.md
?? .orchestration/acceptance/dotfiles-T129-integration-seat-result-gate-cap-followup-a01.md
?? .orchestration/acceptance/dotfiles-T129-normalised-comparison-lint-followup-a01.md
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
?? .orchestration/acceptance/dotfiles-T133-dispositions-a01.md
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
?? .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a01.md
?? .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a02.md
?? .orchestration/acceptance/dotfiles-T133-verdict-audit-pool-a01.md
?? .orchestration/acceptance/dotfiles-T133-verdict-audit-pool-a02.md
?? .orchestration/acceptance/dotfiles-T133-verdict-audit-pool-a03.md
?? .orchestration/acceptance/dotfiles-T133-worker-cap-hookspath-a01.md
?? .orchestration/acceptance/dotfiles-T133-worker-cap-hookspath-a02.md
?? .orchestration/acceptance/dotfiles-T133-worker-cap-hookspath-followup-a01.md
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
?? .orchestration/tasks/dotfiles-T129-anthropic-auth-runtime-check-a01.md
?? .orchestration/tasks/dotfiles-T129-assets-omp-hcom-followup-a02.md
?? .orchestration/tasks/dotfiles-T129-assets-omp-hcom-followup-a03.md
?? .orchestration/tasks/dotfiles-T129-audit-inherit-replan-json-followup-a02.md
?? .orchestration/tasks/dotfiles-T129-audit-inherit-replan-json-followup-a03.md
?? .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a01.md
?? .orchestration/tasks/dotfiles-T129-normalised-comparison-lint-followup-a02.md
?? .orchestration/tasks/dotfiles-T129-omp-config-render-a01.md
?? .orchestration/tasks/dotfiles-T130-sandbox-portability-followup-a01.md
?? .orchestration/tasks/dotfiles-T131-claude-pinned-merge-gate-review-a01.md
?? .orchestration/tasks/dotfiles-T132-make-update-followups-a01.md
?? .orchestration/tasks/dotfiles-T132-merge-train-builder-a01.md
?? .orchestration/tasks/dotfiles-T132-merge-train-ci-a01.md
?? .orchestration/tasks/dotfiles-T133-audit-pool-a01.md
?? .orchestration/tasks/dotfiles-T133-ci-efficiency-a01.md
?? .orchestration/tasks/dotfiles-T133-ci-efficiency-a02.md
?? .orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a02.md
?? .orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a03.md
?? .orchestration/tasks/dotfiles-T133-dispositions-a01.md
?? .orchestration/tasks/dotfiles-T133-dispositions-a02.md
?? .orchestration/tasks/dotfiles-T133-dispositions-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-permission-guard-gate-a01.md
?? .orchestration/tasks/dotfiles-T133-permission-guard-gate-a02.md
?? .orchestration/tasks/dotfiles-T133-permission-guard-gate-a03.md
?? .orchestration/tasks/dotfiles-T133-permission-guard-gate-a04.md
?? .orchestration/tasks/dotfiles-T133-permission-guard-gate-a05.md
?? .orchestration/tasks/dotfiles-T133-permission-guard-gate-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-regime-ci-a01.md
?? .orchestration/tasks/dotfiles-T133-regime-ci-a02.md
?? .orchestration/tasks/dotfiles-T133-regime-ci-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-result-precheck-a01.md
?? .orchestration/tasks/dotfiles-T133-result-precheck-a02.md
?? .orchestration/tasks/dotfiles-T133-result-precheck-a03.md
?? .orchestration/tasks/dotfiles-T133-result-precheck-a04.md
?? .orchestration/tasks/dotfiles-T133-result-precheck-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a01.md
?? .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a02.md
?? .orchestration/tasks/dotfiles-T133-task-generator-plan-check-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-verdict-audit-pool-a01.md
?? .orchestration/tasks/dotfiles-T133-verdict-audit-pool-a02.md
?? .orchestration/tasks/dotfiles-T133-verdict-audit-pool-a03.md
?? .orchestration/tasks/dotfiles-T133-verdict-audit-pool-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-cap-hookspath-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-cap-hookspath-a02.md
?? .orchestration/tasks/dotfiles-T133-worker-cap-hookspath-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-cap-hookspath-followup-a02.md
?? .orchestration/tasks/dotfiles-T133-worker-hooks-path-a01.md
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
?? .orchestration/validation/dotfiles-T129-audit-inherit-replan-json-followup-a02-chain-6fd8c49.log
?? .orchestration/validation/dotfiles-T129-audit-inherit-replan-json-followup-a02-chain-9d13a06.log
?? .orchestration/validation/dotfiles-T129-audit-inherit-replan-json-followup-a02-crit.json
?? .orchestration/validation/dotfiles-T129-audit-inherit-replan-json-followup-a02-local-review-9d13a06.md
?? .orchestration/validation/dotfiles-T129-audit-inherit-replan-json-followup-a02-pr-feedback.json
?? .orchestration/validation/dotfiles-T129-audit-inherit-replan-json-followup-a02-review-receipt.md
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
?? .orchestration/validation/dotfiles-T129-normalised-comparison-lint-followup-a01-chain-b0479c8.log
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
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a01-audit-9da0ed3.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a01-audit-9da0ed3.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a01-chain-37d969e.log
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a01-chain-9da0ed3.log
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a01-crit.json
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a01-local-review-9da0ed3.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a01-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a01-review-receipt.md
?? .orchestration/validation/dotfiles-T133-verdict-audit-pool-a01-chain-0db5f17.log
?? .orchestration/validation/dotfiles-T133-verdict-audit-pool-a01-chain-485d6b3.log
?? .orchestration/validation/dotfiles-T133-verdict-audit-pool-a01-chain-85a4722.log
?? .orchestration/validation/dotfiles-T133-verdict-audit-pool-a01-local-review-85a4722.md
?? .orchestration/validation/dotfiles-T133-verdict-audit-pool-a02-chain-82b99ed.log
?? .orchestration/validation/dotfiles-T133-verdict-audit-pool-a02-chain-b8998de.log
?? .orchestration/validation/dotfiles-T133-verdict-audit-pool-a02-chain-cfeca64.log
?? .orchestration/validation/dotfiles-T133-verdict-audit-pool-a02-local-review-b8998de.md
?? .orchestration/validation/dotfiles-T133-verdict-audit-pool-a02-local-review-cfeca64.md
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
     1	---
     2	format: 2
     3	task_id: dotfiles-T133-dispositions-a02
     4	kind: code
     5	security: true
     6	allowed_files:
     7	  - scripts/orchestrator/dispositions.py
     8	  - scripts/orchestrator/orch-gate.sh
     9	  - tests/unit/test_dispositions.py
    10	  - tests/unit/test_orch_gate_path.py
    11	  - .orchestration/dotfiles-T133-dispositions-a02/**
    12	after: [dotfiles-T133-permission-guard-gate-a05]
    13	reset_of: [dotfiles-T133-dispositions-a01]
    14	threat_table:
    15	  - control: "scripts/orchestrator/dispositions.py (disposition proposals, the three refutation forms, static selector verification against the head tree and parsing of prefetched required-check data)"
    16	    disposition: "closed: tests/unit/test_dispositions.py::DispositionsTest::test_dispositions_verifies_test_refutations_from_head_tree_and_required_checks"
    17	  - control: "scripts/orchestrator/orch-gate.sh (re-validation immediately before the gate, enforcement only under DISPOSITIONS_REQUIRE_REFUTATION=1 and reporting otherwise)"
    18	    disposition: "closed: tests/unit/test_orch_gate_path.py::OrchGatePathTest::test_orch_gate_revalidates_the_dispositions_before_the_gate"
    19	  - control: "tests/unit/test_dispositions.py (temporary Git repositories, sweep fixtures, prefetched API fixtures and file URLs for source verification)"
    20	    disposition: "residual: fixtures use temporary repositories and files, perform no live GitHub writes and leave markers that detect importing or executing a named head test; the final-head audit reads their assertions."
    21	  - control: "tests/unit/test_orch_gate_path.py (fake binaries, fixture main, inherited-environment cases, verifier authentication and sweep-copy identity)"
    22	    disposition: "residual: fake binaries record arguments, environments, working directories and execution order; fixture main supplies authenticated verifier bytes, and the final-head audit reads refusal and restoration assertions."
    23	  - control: ".orchestration/dotfiles-T133-dispositions-a02/** (this reset task's branch artifacts)"
    24	    disposition: "residual: evidence identifies tested revisions, preserves predecessor failures and separates worker fixtures from the orchestrator's API reads; the audit compares its claims with the diff and CI."
    25	  - control: "the task-file copy on the branch (.orchestration/dotfiles-T133-dispositions-a02/task.md) replaces the reset_of task's copy (.orchestration/dotfiles-T133-dispositions-a01/task.md)"
    26	    disposition: "residual: the first push deletes the a01 copy and adds the byte-identical dispatched a02 copy as specified reset bookkeeping; TASK and RESULT name the a02 copy's SHA256, and the orchestrator verifies the replacement at acceptance."
    27	  - control: task metadata
    28	    disposition: "residual: the orchestrator checks format, task identity, reset_of, allowed_files, threat_table and premises with task-consistency-check C1 to C10 and C7b before dispatch and at acceptance; whole-file byte identity protects the dispatched policy."
    29	  - control: metadata separators
    30	    disposition: "residual: the first document separators bound structured metadata, and the task-copy comparison covers the complete file."
    31	  - control: in-process effects
    32	    disposition: "residual: the verifier performs Git data reads and the source URL fetch, parses API JSON inside the sandbox and writes only its requested output; it never imports head modules, discovers tests or executes a selector."
    33	  - control: workflow and interpreter or environment inputs
    34	    disposition: "residual: no workflow or interpreter configuration changes; execution uses isolated Python, a constructed env -i environment and a private PATH of absolute binaries resolved in the trusted root."
    35	  - control: new or renamed scripts
    36	    disposition: "residual: dispositions.py is the only new script relative to main; RESULT lists it, and any other new or renamed script fails the audit."
    37	  - control: the environment before Git discovery
    38	    disposition: "closed: tests/unit/test_orch_gate_path.py::OrchGatePathTest::test_orch_gate_sanitizes_the_environment_before_git_discovery"
    39	  - control: the executed verifier's identity
    40	    disposition: "closed: tests/unit/test_orch_gate_path.py::OrchGatePathTest::test_orch_gate_runs_dispositions_only_when_it_matches_main"
    41	  - control: the validated sweep's identity
    42	    disposition: "closed: tests/unit/test_orch_gate_path.py::OrchGatePathTest::test_orch_gate_validates_the_copy_it_reads"
    43	  - control: the prefetched required-check data
    44	    disposition: "residual: the orchestrator records its own ruleset and exact-head check-runs reads in protected evidence, and the verifier parses their raw JSON again rather than accepting saved verification booleans."
    45	  - control: the strength of a test refutation
    46	    disposition: "residual: selector presence and successful required checks provide evidence of the head's CI strength only; P0/P1 remain unrefuted claims until programs item (16), P1-10 part 2, confirms them."
    47	  - control: the outside-sandbox gh exception
    48	    disposition: "residual: decision D-024-17 assigns closure to plan 024 P1-15, whose worker exclusions execute an absolute trusted binary; this task retains today's individual gh reads and does not change worker exclusions."
    49	  - control: the worker-seat write boundary
    50	    disposition: "residual: every worker seat's sandbox denies writes outside its worktree and listed scratch paths, protecting the trusted checkout, review worktree and orchestrator evidence; a same-UID process outside every seat sandbox remains outside this protection."
    51	  - control: orchestrator effect merge
    52	    disposition: "residual: merge uses only gh pr merge --squash --match-head-commit <audited head> after the integration gate; local merges and pushes to main remain forbidden."
    53	  - control: orchestrator effect update-branch
    54	    disposition: "residual: a rebase or gh pr update-branch changes the head, so required CI, feedback collection, task-level audit and security review bind the resulting final head before integration."
    55	  - control: orchestrator effect forced worker removal
    56	    disposition: "residual: no forced removal is planned; the existing dirty-worktree rule applies, and the acceptance record identifies any discarded uncommitted state."
    57	premises:
    58	  - claim: neither new file exists on origin/main
    59	    command: git ls-files scripts/orchestrator/dispositions.py tests/unit/test_dispositions.py | wc -l
    60	    output: |-
    61	      0
    62	  - claim: a sweep item of pr-feedback.py carries source, author, bot, level, path, line, body, url, the source's extra state and disposition, so the thread's commit comes from gh when the item lacks it
    63	    command: sed -n '133,143p' scripts/pr-feedback.py | /usr/bin/grep -o '"[a-z]*"' | tr '\n' ' '
    64	    output: |-
    65	      "source" "author" "login" "slug" "" "bot" "level" "path" "line" "body" "" "url" "disposition" "" 
    66	  - claim: orch-gate.sh invokes the gate once with PR_FEEDBACK_EVIDENCE, the point before which the re-validation runs
    67	    command: /usr/bin/grep -c 'PR_FEEDBACK_EVIDENCE="${sweep}"' scripts/orchestrator/orch-gate.sh
    68	    output: |-
    69	      1
    70	  - claim: the orch-gate tests live in tests/unit/test_orch_gate_path.py and use fake binaries on a private PATH
    71	    command: /usr/bin/grep -c 'def test_orch_gate_' tests/unit/test_orch_gate_path.py
    72	    output: |-
    73	      3
    74	  - claim: audit-pool.sh is not on origin/main at the predecessor's write time, so the --second-opinion mode of programs item (16) is a later task
    75	    command: git ls-files scripts/orchestrator/audit-pool.sh | wc -l
    76	    output: |-
    77	      0
    78	  - claim: the gate already holds the disposition and commit validators dispositions.py reuses
    79	    command: /usr/bin/grep -n 'def commit_in_range\|def parse_disposition' scripts/require-crit-review.py | cut -c1-24
    80	    output: |-
    81	      389:def commit_in_range(
    82	      397:def parse_disposition(
    83	---
    84	
    85	# AGMSG-TASK dotfiles-T133-dispositions-a02 — INV-6 reset of dotfiles-T133-dispositions-a01 (plan 006 S2; plan 024 P1-10 part 1, programs item (5))
    86	
    87	This reset incorporates the independent review-profile redesign and the orchestrator's decisions after C-80 returned `Verdict: incorrect` with eight P1 and one P2 in `.orchestration/validation/dotfiles-T133-dispositions-a02-text-security.md.last.md`.
    88	
    89	The local review of revise-1 head `bdbbbf91765a8f9c2f94565096c8bcbf2fca47b3` stopped the chain at `2026-10-18T22:1xZ`. It found one P1 in the CI-log verifier and two P2 concerning interleaved diagnostic output and loss of the full selector. A second revise would reach INV-6 S2, and the operator forbids a third round. The unsound CI-log design came from the orchestrator's amendment 1.
    90	
    91	PR #419 continues on `tools/dispositions-a01` from `bdbbbf91765a8f9c2f94565096c8bcbf2fca47b3`. The merged P1-11 baseline is `origin/main` at `0e496ce7449e9286aeac3b2770cbff374c7dc5cf`. The worker rebases onto main containing that baseline and merged PR #421 before its first push. One branch and one PR carry the reset. The orchestrator names the worker seat in the TASK line.
    92	
    93	The worker's first push deletes `.orchestration/dotfiles-T133-dispositions-a01/task.md` and adds this dispatched text's byte-identical copy at `.orchestration/dotfiles-T133-dispositions-a02/task.md`. That predecessor-copy deletion is the specified reset bookkeeping exception to `allowed_files`. The predecessor's other artifacts, canonical task text and acceptance history remain unchanged.
    94	
    95	The six command-output premises retain a01's write-time observations as historical evidence. New report, validation, sandbox and learning records use the a02 directory. The a01 acceptance record retains its audit, amendment, revise, advisory rows and S2 withdrawal.
    96	
    97	The design sources are `.orchestration/plans/024-design-programs.md` items (5) and (16), and `.orchestration/plans/024-design-quality.md` section 5.13. The additional inputs are the a01 task and acceptance records, `.orchestration/validation/dotfiles-T133-dispositions-a01-local-review-bdbbbf9.md`, the C-80 verdict, the branch diff through `bdbbbf91`, `scripts/orchestrator/orch-gate.sh` at `origin/main` and the checker docstring in `scripts/orchestrator/task-consistency-check.py`.
    98	
    99	The audit decision at `fa47987` established that a `test:` refutation never executes head code on the orchestrator's host. Running a test in the trusted checkout tests pre-regression code. The merged regime workflow executes base code and inspects the PR as data. It has no head-test execution responsibility.
   100	
   101	The CI results-artifact design is withdrawn. A head-authored test produces its own result, so an artifact, runner, workflow step or download cannot establish producer trust. The Linux keyring restriction also prevents an in-sandbox helper from implementing the proposed authenticated gh fetch. This task adds no results runner, results artifact, artifact download or workflow change.
   102	
   103	The write-boundary premise is that every worker seat's sandbox denies writes outside its worktree and listed scratch paths. The trusted checkout, review worktree and orchestrator's evidence are protected by that boundary. The threat table states its residual once. Decision D-024-17 owns the separate outside-sandbox executable-selection defect; this task retains today's single-command gh reads.
   104	
   105	## Goal
   106	
   107	For a PR head, every review-comment item of the sweep gets a machine proposal: `fixed:<commit>` when an eligible branch commit between the thread's commit and the head touches the thread's hunk, otherwise a demand for `not-applicable:` with one of the three refutation forms. The gate wrapper re-validates the saved dispositions before the gate runs.
   108	
   109	A `test:` refutation holds only when its selector names a test function present at the stated path in the head tree, the required unit-test check runs concluded success for that exact head, and the finding is P2 or P3. A P0/P1 `test:` refutation is a claim that programs item (16)'s second opinion must confirm. `--require-refutation` treats that claim as not yet refuted.
   110	
   111	This evidence has the strength of the head's CI. It supplies no proof against a head-authored test and establishes no per-selector execution outcome.
   112	
   113	## Files
   114	
   115	1. `scripts/orchestrator/dispositions.py <pr> <head> --feedback <sweep.json> [--out <json>] [--require-refutation] [--commits <json>] [--checks <json>]` is a Python CLI run with `python -I`, using the standard library only and an English shdoc-style module docstring.
   116	
   117	   The tool processes each `review_comment` item and each badged `review` finding. The location comes from the item's path and line, with the existing review-body blob-link handling retained. A finding without a location gets the not-applicable demand and still requires a refutation when its disposition is not-applicable.
   118	
   119	   The thread's commit comes from `original_commit_id`, the existing `commit` field, the `--commits` map from URL to commit, or the existing gh read, in that order. A required commit that cannot be obtained or read produces a hold with the reason. Item 6 defines the proposal path that needs no thread-commit lookup.
   120	
   121	   The proposal uses the PR diff and `git diff <thread commit>..<head> -- <path>`. A covering hunk uses its old-side and new-side ranges. The tool walks eligible branch commits newest first and proposes `fixed:<commit>` only for a commit whose own diff against its parent touches that range. Base commits and base-merge-only changes supply no branch fix. An unchanged hunk, an upstream-only change or the absence of an eligible fixing commit produces the not-applicable demand. Paths remain literal Git pathspecs, and sweep text is never evaluated.
   122	
   123	   The output is the sweep with `proposal` added per processed item and the existing `disposition` untouched. A checked not-applicable disposition also receives its verification record. `--out` selects the output file, and stdout is the default. Diagnostic lines go to stderr.
   124	
   125	   The three refutation forms remain `test:<selector>`, `source:{url, fetched_at, quote}` and `diff:<range>`. The existing `; evidence=<form>` disposition representation remains. The CI-log parser and `--ci-log` input are removed.
   126	
   127	   The `test:` form reads the named file with `git show <head>:<path>` and parses it as Python syntax data with the standard-library AST. The full selector identifies the file and function, including its module and class components when present. A full dotted selector maps deterministically to its repository path. The existing path spelling remains supported, and a classless function name must identify one function unambiguously at that path. Missing paths, missing functions, mismatched classes, ambiguous selectors and malformed syntax fail verification with a reason.
   128	
   129	   The head file is never imported, sourced, evaluated or executed. Decorators and test bodies remain data. The verifier performs no unittest discovery and launches no selector.
   130	
   131	   `--checks` supplies prefetched API data. Its JSON contains the repository, exact head, raw ruleset response and raw check-runs response pages. The orchestrator obtains the ruleset with an individual gh read and obtains the head's check runs with one individual `gh api --paginate --slurp` command against `repos/{owner}/{repo}/commits/<head>/check-runs?filter=latest&per_page=100`. The repository comes from the trusted checkout. The check-runs endpoint names the exact audited head.
   132	
   133	   Each gh read runs outside the sandbox as the individual command permitted today. Its output is parsed inside the sandbox and recorded as data. The Python helper, JSON construction and JSON parsing do not run outside the sandbox. The worker uses fixtures for tests and prefetched inputs for authenticated reads; it never attempts to escape the sandbox through a Python gh subprocess.
   134	
   135	   The required unit-test contexts come from the orchestrator's ruleset read. Their current names are `test (ubuntu-24.04, server)`, `test (ubuntu-24.04, client)` and `test (macos-14, client)`. The sweep and head-authored workflow text cannot choose the required names. Missing or malformed ruleset data and an empty required unit-test set fail verification.
   136	
   137	   Every required unit-test context must have its latest check run on the exact head with `status: completed` and `conclusion: success`. Pagination is consumed completely. Selection never searches older runs for a preferred success. A missing context, wrong head, pending run, skipped run, neutral conclusion, failure or malformed response fails verification with a reason.
   138	
   139	   The verification record preserves the original selector, resolved path and function, head, required context names and selected check-run identities and conclusions. It states that selector presence and successful CI were checked. It never states that the named function ran.
   140	
   141	   A P2/P3 finding with both checks satisfied receives a verified `test:` record. A P0/P1 finding receives `claim-recorded` and `refutation.ok: false` until programs item (16), P1-10 part 2, confirms it. Missing or ambiguous priority receives no P2/P3 acceptance. A P0/P1 marker always selects the stricter handling.
   142	
   143	   The `source:` form fetches the named URL read-only, verifies that the quote occurs in the fetched page text and records the page's SHA256. The existing `file://` fixtures remain accepted for tests. A malformed form, failed fetch or absent quote fails verification with the reason. This check establishes quote occurrence and page identity; semantic refutation remains subject to the design's judgment rules.
   144	
   145	   The `diff:` form uses the tool-fixed `<thread commit>..<audited head>` range. A caller-supplied range is accepted only when its endpoints equal those fixed commits, the thread's hunk is unchanged over that range and the disposition names why the path is unreachable. The reason retains the existing minimum of 20 characters. The result is recorded as `claim-recorded`. A range such as `<head>..<head>` is refused. Until programs item (16)'s second opinion confirms it, `--require-refutation` refuses a P0/P1 not-applicable resting on `diff:` alone.
   146	
   147	   `--require-refutation` prints one line per not-applicable disposition with a missing, failed or not-yet-confirmed form and exits 1. The legacy `evidence=<command>` form is reported as `legacy-evidence` and fails only under `--require-refutation`. Exit 0 means the selected mode completed, exit 1 means a required refutation failed, and exit 2 means usage failure or a hold such as an unreadable sweep or a required missing thread commit. Missing check data fails the refutation and never authorizes local head-code execution.
   148	
   149	2. `scripts/orchestrator/orch-gate.sh` enters a constructed `env -i` environment before any Git discovery or checkout.
   150	
   151	   The trusted root is established from the wrapper's physical source location. Absolute tools are resolved in that root, and the existing private links directory supplies the private PATH. The interpreter is resolved in the trusted root before the review worktree is entered and is invoked directly with isolated Python options.
   152	
   153	   The environment sets `GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL=/dev/null`. Every Git call carries `-c core.hooksPath=/dev/null` and `-c core.fsmonitor=false`, including discovery, authentication, data reads, checkout, cleanup and restoration. Inherited `GIT_DIR`, `GIT_WORK_TREE`, `GIT_CONFIG_GLOBAL` and other caller Git overrides do not reach discovery. The existing removal and worktree-restoration trap remains effective on failure.
   154	
   155	   The wrapper authenticates `scripts/orchestrator/dispositions.py` as it authenticates the gate and validator. The executed file is the trusted checkout's regular tracked file, and its SHA256 equals the SHA256 of `git show origin/main:scripts/orchestrator/dispositions.py`. Missing, changed, untracked or substituted verifier bytes refuse before execution. No verifier is loaded from the PR head or review checkout.
   156	
   157	   Until PR #419 merges, the new verifier is absent from trusted main. The new gate step is exercised only by worker tests with a fixture main containing its authenticated verifier. Integration of PR #419 uses the existing trusted main gate. The candidate wrapper and verifier are never run on the orchestrator's host to bootstrap their own integration.
   158	
   159	   After checkout and evidence preparation, the wrapper retains one dispositions re-validation step immediately before the gate. It validates the review-worktree sweep at the same path and working directory passed to `scripts/require-crit-review.py` through `PR_FEEDBACK_EVIDENCE`. It records that file's SHA256 in its output. It never validates the trusted-root source copy while the gate reads another copy.
   160	
   161	   The orchestrator's prefetched checks are recorded at `.orchestration/<task>/checks.json` and supplied through `--checks` when a `test:` form needs them. Production evidence comes from the orchestrator's own API reads. Worker-authored check fixtures do not become production evidence. The wrapper passes the protected data to the authenticated verifier and does not accept cached `refutation.ok` values as authority.
   162	
   163	   Under `DISPOSITIONS_REQUIRE_REFUTATION=1`, re-validation adds `--require-refutation`, and failure refuses with wrapper exit 2 and the tool's diagnostic lines. Without the variable, the same step reports verification failures without enforcing them. A usage failure, hold or verifier-authentication failure remains a wrapper refusal. The PR number and head come from the wrapper's existing arguments.
   164	
   165	   The step executes no head code and no test selector.
   166	
   167	3. `tests/unit/test_dispositions.py` retains temporary-repository coverage for changed-hunk proposals, untouched-line demands, all three refutation forms, legacy evidence and holds.
   168	
   169	   `test_dispositions_proposes_fixed_for_a_changed_hunk_and_demands_not_applicable_otherwise` checks the actual fixing commit, an untouched line and unchanged existing dispositions. The review-body finding and literal-pathspec regressions remain.
   170	
   171	   `test_require_refutation_fails_without_a_form_and_accepts_each_of_the_three` uses head-tree and prefetched-check fixtures for `test:`, a `file://` page for present and absent source quotes, and fixed-range diff fixtures for accepted and refused claims. It checks the recorded source hash, reporting mode and enforcement mode.
   172	
   173	   `test_dispositions_holds_on_an_unreadable_sweep_or_a_missing_commit` retains exit-2 coverage for malformed input and an unavailable commit needed by a located in-diff thread.
   174	
   175	   `test_diff_refutation_range_is_fixed_to_thread_commit_and_head_and_is_a_claim` retains arbitrary-range refusal, the unreachable-path reason and the P0/P1 second-opinion restriction.
   176	
   177	   `test_dispositions_verifies_test_refutations_from_head_tree_and_required_checks` checks an exact present function with successful required checks for P2 and P3. It separately checks missing paths, absent functions, wrong classes, malformed check data, missing required contexts, incomplete pagination, wrong heads and pending or unsuccessful latest runs. An older successful run never overrides a newer failed or pending run. P0/P1 produce claims and fail `--require-refutation`. Missing priority does not acquire P2/P3 treatment.
   178	
   179	   Head-test fixtures contain import and execution markers. Verification creates neither marker. The test forbids log reads, artifact commands and selector execution. Assertions describe static presence and CI conclusions without claiming a per-selector result.
   180	
   181	4. `tests/unit/test_orch_gate_path.py` retains its existing fake-binary style and private-PATH, shim-refusal, cleanup and restoration coverage.
   182	
   183	   `test_orch_gate_revalidates_the_dispositions_before_the_gate` checks that enforcement refuses before the fake gate runs when current verification fails, including when saved verification claims success. Reporting mode prints the failed verification and permits the fake gate. The audited head reaches the verifier, and no local head-test marker is created.
   184	
   185	   `test_orch_gate_sanitizes_the_environment_before_git_discovery` supplies inherited `GIT_DIR`, `GIT_WORK_TREE`, `GIT_CONFIG_GLOBAL` and Git configuration overrides pointing to a decoy repository. The gate selects the intended trusted root and PR worktree. The recorded first Git invocation already has the sanitized environment and required configuration arguments. Checkout and restoration retain those controls.
   186	
   187	   `test_orch_gate_runs_dispositions_only_when_it_matches_main` supplies verifier bytes in fixture main. Matching trusted-checkout bytes execute. Modified bytes, a missing main version and a substituted file refuse before verifier or gate execution. A matching file in the head tree cannot authorize different trusted-checkout bytes.
   188	
   189	   `test_orch_gate_validates_the_copy_it_reads` makes the source sweep and copied review sweep differ. The verifier and fake gate record the same sweep path and bytes, and the wrapper's reported SHA256 matches those bytes. A valid source copy cannot authorize an invalid review copy. Enforcement refuses before the fake gate runs.
   190	
   191	   Fixture main is used for every case exercising the new step before merge. Fixture lines count against the test cap.
   192	
   193	5. The inherited row `local:fa47987:1` remains the skipped-only rejection item.
   194	
   195	   `tests/unit/test_dispositions.py::DispositionsTest::test_test_refutation_rejects_skipped_required_checks` checks that `skipped`, `neutral`, absent and incomplete required checks cannot satisfy `test:`, even when their output contains fabricated passing-test text. Exit 0 from a selector or helper supplies no evidence because verification executes no selector or helper from the head.
   196	
   197	   Check-runs data does not distinguish a successful suite that skipped the named function. The report states that limitation when recording this row's absorption. This task makes no claim that static presence plus suite success proves execution of a non-skipped test.
   198	
   199	6. The inherited row `local:fa47987:2` remains the not-applicable demand for upstream-only threads.
   200	
   201	   A thread whose path and line are outside the audited base-to-head PR diff gets the not-applicable demand. Proposal generation checks PR-diff membership before a thread-commit lookup that the proposal does not need. An absent path, an uncovered line and an upstream-only change supply no branch fixing commit.
   202	
   203	   The proposal is `not-applicable:` rather than a hold or an unrelated `fixed:` candidate. A separately requested `diff:` refutation still needs the thread commit required by fixed-range verification.
   204	
   205	   `tests/unit/test_dispositions.py::DispositionsTest::test_dispositions_demands_not_applicable_for_a_thread_outside_the_diff` covers an absent path and an uncovered line without a readable thread commit and forbids an unnecessary gh lookup. `test_upstream_only_hunk_changes_demand_not_applicable` retains proof that a base merge supplies no branch fix.
   206	
   207	7. The inherited row `local:bdbbbf9:3` remains the full-selector preservation item.
   208	
   209	   `tests/unit/test_dispositions.py::DispositionsTest::test_test_refutation_preserves_the_full_selector` checks the original selector in the verification record and matches its complete file, module, class and function identity against the head tree. A similarly named function in another module or class cannot satisfy it. Selector parsing never discards module or class components to obtain a match.
   210	
   211	8. The inherited row `local:bdbbbf9:2` remains the interleaved-output item and is moot under this design.
   212	
   213	   Verification consumes no human-readable test output. Interleaved diagnostics and fabricated `... ok` lines have no authority. The old CI-log parser is deleted. The head-tree and check-runs regressions assert that no log request is made and that unrelated output text cannot change the result.
   214	
   215	9. `.orchestration/dotfiles-T133-dispositions-a02/report.md` states the proposal rule, the three forms, static selector verification, required-check selection, the priority restriction and the legacy-evidence transition.
   216	
   217	   The report pastes the output of `grep -l "evidence=" .orchestration/validation/*-pr-feedback.json | wc -l` and identifies it as a count of matching records. It names programs item (16), `audit-pool.sh --second-opinion`, as P1-10 part 2 after PR #410.
   218	
   219	   The report maps the four inherited rows to items 5 through 8 and their final-head evidence. They belong to this reset and receive no new advisory deferral. The report distinguishes predecessor results from new red-then-green evidence.
   220	
   221	   The report records withdrawal of the artifact design, the strength and skipped-test limitation of the replacement evidence, D-024-17's ownership of the outside-sandbox exception, the environment controls, verifier authentication and the validated sweep's SHA256.
   222	
   223	## Out of scope
   224	
   225	`audit-pool.sh --second-opinion` is programs item (16) and P1-10 part 2, after PR #410. This task adds no second-opinion mode and accepts no saved consensus boolean as a substitute.
   226	
   227	`scripts/require-crit-review.py` remains unchanged. Its existing disposition and commit validators are reused or re-implemented read-only. `fill_sweep.py`, `pr-feedback.py` and the sweep format remain unchanged. The chain scripts continue calling the gate wrapper.
   228	
   229	Flipping `DISPOSITIONS_REQUIRE_REFUTATION` remains a decision row. This task changes no enforcement default.
   230	
   231	All workflows remain unchanged, including `.github/workflows/test.yaml` and `.github/workflows/regime.yml`. `scripts/orchestrator/regime-ci.py` and the Makefile remain unchanged. `scripts/ci/unittest-results.py` and `tests/unit/test_unittest_results.py` are excluded. The regime job receives no head-test execution or selector-result responsibility.
   232	
   233	CI-log parsing, results-artifact production, artifact downloads and head-test execution during refutation verification are excluded.
   234	
   235	The worker-exclusion change owned by D-024-17 and plan 024 P1-15 is outside this task. This task changes no sandbox permissions, exclusion configuration or executable-selection policy for worker seats.
   236	
   237	## Check
   238	
   239	`make format` completes, and `uv run python -m unittest tests.unit.test_dispositions tests.unit.test_orch_gate_path -v` is green. `shellcheck scripts/orchestrator/orch-gate.sh` and `shfmt -d scripts/orchestrator/orch-gate.sh` are clean.
   240	
   241	The new head-tree and required-check regression, the skipped-check regression, the outside-diff regression, the full-selector regression and the three named gate-boundary regressions have recorded red runs against `bdbbbf91765a8f9c2f94565096c8bcbf2fca47b3` and green runs against the final head. Each record names its tested revision, exact selector, command, exit status and output. Unsupported predecessor inputs are recorded as unsupported inputs and are never presented as exploit reproductions.
   242	
   243	The interleaved-output item records deletion of the log parser and the final-head assertions that log commands and free-text outcomes have no authority. Historical green runs do not replace final-head evidence.
   244	
   245	The real-sweep check retains PR #409 and head `4fe243803971bd5ba8ab45f8ede5cfb4dd37f719`. Required thread commits are read with individual gh commands and saved as `.orchestration/dotfiles-T133-dispositions-a02/thread-commits.json`. The helper runs inside the sandbox as `uv run --no-project python -I scripts/orchestrator/dispositions.py 409 4fe243803971bd5ba8ab45f8ede5cfb4dd37f719 --feedback .orchestration/validation/dotfiles-T133-ci-efficiency-a02-pr-feedback.json --commits .orchestration/dotfiles-T133-dispositions-a02/thread-commits.json`. Its output is pasted once.
   246	
   247	A real `test:` verification uses the orchestrator's own prefetched ruleset and exact-head check-runs data through `--checks`. The validation record includes the individual gh commands, repository, requested head, exit statuses and raw-response hashes. A missing real input remains a failed verification and is never replaced by a worker fixture.
   248	
   249	All command output is pasted in `.orchestration/dotfiles-T133-dispositions-a02/validation.md`. Sandbox records identify each individual outside-sandbox gh command and the in-sandbox helper and parser. The record identifies fixture-main tests separately from production gate execution.
   250	
   251	At `bdbbbf91`, the measured diff contains 284 changed lines outside `tests/` and `.orchestration/`, and 279 under `tests/`. `git diff --numstat origin/main...HEAD` records the final totals: at most 420 changed lines outside `tests/` and `.orchestration/`, and at most 480 under `tests/`. Changed lines are additions plus deletions, including fixtures.
   252	
   253	No local Bats tests run. Required Bats results come from GitHub Actions. The orchestrator runs task-consistency-check C1 to C10 and C7b before dispatch and at acceptance.
   254	
   255	## Completion
   256	
   257	PR #419 continues on `tools/dispositions-a01` from `bdbbbf91765a8f9c2f94565096c8bcbf2fca47b3`, rebased onto main containing `0e496ce7` and merged PR #421 before the first push. The first push deletes the a01 task copy and adds the byte-identical dispatched a02 copy. This reset creates no fresh implementation branch or second implementation PR.
   258	
   259	The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies with this task's branch, dependency and review requirements, `dotfiles-T133-dispositions-followup-a01` as the owner of any new advisory P2, and `task_copy=<sha256 of .orchestration/dotfiles-T133-dispositions-a02/task.md>` in RESULT. The orchestrator writes that owner task before assigning its first advisory row. The four inherited rows remain completion requirements of a02.
   260	
   261	RESULT also carries `precheck=<sha256 of .orchestration/dotfiles-T133-dispositions-a02/precheck.json>` when `scripts/orchestrator/result-precheck.sh` has merged through PR #411, and otherwise carries `precheck=pending-411`.
   262	
   263	Every worker-side fix round, before or after the first RESULT, counts toward INV-6 under C-61. The predecessor's pre-RESULT fix round, amendment, revise and S2 stop remain recorded. This reset does not recast predecessor findings or failed verification as approvals.
   264	
   265	The worker's own pre-push review is one round at most. A P0/P1 surviving that round is sent in RESULT as open and stops integration. The worker starts no further private correction-and-review cycle to avoid reporting it. Any later permitted round remains subject to INV-6 and the inherited completion rule.
   266	
   267	No `@codex review` comment is posted. Automatic final-head Bot reviews are observed within the bounded 15-minute window, and absence is recorded as `bot: none`. Required CI passes before a completion RESULT. RESULT identifies every inline and review-body finding, its proposed disposition and every surviving P0/P1 as `open:<thread id>` or `open:review-<review id>`.
   268	
   269	A Codex seat writes evidence at the same relative paths in its worktree and says so in RESULT. Worker-side review evidence carries the required `-worker-` infix. RESULT names the head, base, branch, changed files, Bot findings and dispositions, open P0/P1 findings, exact test selectors, red-then-green evidence, caps, the one new script, task-copy hash and artifact paths. The orchestrator copies worktree evidence by absolute path before review.
   270	
   271	This task is `security: true`. Under C-80, a separate security-profile context reviews this complete revised text before dispatch. That review is a dispatch prerequisite and is not claimed as completed by this text. The orchestrator also runs the task-level audit and a separate security-profile review on the final implementation head.
   272	
   273	Final-head feedback collection, task-level audit, finding dispositions, acceptance and the integration gate follow Orchestrator Playbook step 10 in its prescribed order. The gate receives `PR_FEEDBACK_EVIDENCE`, `AUDIT_EVIDENCE`, `ACCEPTANCE_EVIDENCE` and the agent review receipt. A changed head receives fresh required evidence. Integration of this PR uses the existing trusted main gate; the new step remains confined to fixture-main tests until merge. Merge uses `gh pr merge --squash --match-head-commit <audited head>`.
   274	
   275	Commands for gh and Git writes run individually, without shell chaining or a wrapper combining writes. A classifier denial produces a blocked PONG naming the command and reason. Until P1-14 lands, strings containing `gh pr merge` or `gh pr create` are written with the file-edit tool rather than a Bash heredoc or `echo`.
   276	
   277	## Sequencing note (orchestrator, 2026-10-19T03:0xZ)
   278	
   279	This task edits `scripts/orchestrator/orch-gate.sh`, which `dotfiles-T133-permission-guard-gate-a05` also edits (the sanitized environment of design 5.14 item 2 and the private uv cache of item 9). The a05 change lands first; this task starts after PR #420 merges, rebases onto that main, and its orch-gate.sh item builds on the sanitized environment a05 provides instead of adding a second one. Design 5.14 applies to this task by reference (D-024-18); the threat table's environment, trusted-path and committed-ledger rows are read against it.
   280	
   281	## Checks (pasted by the orchestrator before each send)
   282	
   283	```
   284	(pasted at dispatch)
   285	```
   286	
   287	Local Bats tests, live enforcement changes and head-code execution during refutation verification are not performed.
   288	A `test:` refutation has the strength of the head's CI and supplies no proof against a head-authored test; P0/P1 claims remain unrefuted until the item-16 second opinion confirms them.
exec
/bin/zsh -lc "nl -ba .orchestration/tasks/dotfiles-T133-dispositions-a02.md | sed -n '1,148p'" in ~/Workspace/dotfiles
 succeeded in 186ms:
     1	---
     2	format: 2
     3	task_id: dotfiles-T133-dispositions-a02
     4	kind: code
     5	security: true
     6	allowed_files:
     7	  - scripts/orchestrator/dispositions.py
     8	  - scripts/orchestrator/orch-gate.sh
     9	  - tests/unit/test_dispositions.py
    10	  - tests/unit/test_orch_gate_path.py
    11	  - .orchestration/dotfiles-T133-dispositions-a02/**
    12	after: [dotfiles-T133-permission-guard-gate-a05]
    13	reset_of: [dotfiles-T133-dispositions-a01]
    14	threat_table:
    15	  - control: "scripts/orchestrator/dispositions.py (disposition proposals, the three refutation forms, static selector verification against the head tree and parsing of prefetched required-check data)"
    16	    disposition: "closed: tests/unit/test_dispositions.py::DispositionsTest::test_dispositions_verifies_test_refutations_from_head_tree_and_required_checks"
    17	  - control: "scripts/orchestrator/orch-gate.sh (re-validation immediately before the gate, enforcement only under DISPOSITIONS_REQUIRE_REFUTATION=1 and reporting otherwise)"
    18	    disposition: "closed: tests/unit/test_orch_gate_path.py::OrchGatePathTest::test_orch_gate_revalidates_the_dispositions_before_the_gate"
    19	  - control: "tests/unit/test_dispositions.py (temporary Git repositories, sweep fixtures, prefetched API fixtures and file URLs for source verification)"
    20	    disposition: "residual: fixtures use temporary repositories and files, perform no live GitHub writes and leave markers that detect importing or executing a named head test; the final-head audit reads their assertions."
    21	  - control: "tests/unit/test_orch_gate_path.py (fake binaries, fixture main, inherited-environment cases, verifier authentication and sweep-copy identity)"
    22	    disposition: "residual: fake binaries record arguments, environments, working directories and execution order; fixture main supplies authenticated verifier bytes, and the final-head audit reads refusal and restoration assertions."
    23	  - control: ".orchestration/dotfiles-T133-dispositions-a02/** (this reset task's branch artifacts)"
    24	    disposition: "residual: evidence identifies tested revisions, preserves predecessor failures and separates worker fixtures from the orchestrator's API reads; the audit compares its claims with the diff and CI."
    25	  - control: "the task-file copy on the branch (.orchestration/dotfiles-T133-dispositions-a02/task.md) replaces the reset_of task's copy (.orchestration/dotfiles-T133-dispositions-a01/task.md)"
    26	    disposition: "residual: the first push deletes the a01 copy and adds the byte-identical dispatched a02 copy as specified reset bookkeeping; TASK and RESULT name the a02 copy's SHA256, and the orchestrator verifies the replacement at acceptance."
    27	  - control: task metadata
    28	    disposition: "residual: the orchestrator checks format, task identity, reset_of, allowed_files, threat_table and premises with task-consistency-check C1 to C10 and C7b before dispatch and at acceptance; whole-file byte identity protects the dispatched policy."
    29	  - control: metadata separators
    30	    disposition: "residual: the first document separators bound structured metadata, and the task-copy comparison covers the complete file."
    31	  - control: in-process effects
    32	    disposition: "residual: the verifier performs Git data reads and the source URL fetch, parses API JSON inside the sandbox and writes only its requested output; it never imports head modules, discovers tests or executes a selector."
    33	  - control: workflow and interpreter or environment inputs
    34	    disposition: "residual: no workflow or interpreter configuration changes; execution uses isolated Python, a constructed env -i environment and a private PATH of absolute binaries resolved in the trusted root."
    35	  - control: new or renamed scripts
    36	    disposition: "residual: dispositions.py is the only new script relative to main; RESULT lists it, and any other new or renamed script fails the audit."
    37	  - control: the environment before Git discovery
    38	    disposition: "closed: tests/unit/test_orch_gate_path.py::OrchGatePathTest::test_orch_gate_sanitizes_the_environment_before_git_discovery"
    39	  - control: the executed verifier's identity
    40	    disposition: "closed: tests/unit/test_orch_gate_path.py::OrchGatePathTest::test_orch_gate_runs_dispositions_only_when_it_matches_main"
    41	  - control: the validated sweep's identity
    42	    disposition: "closed: tests/unit/test_orch_gate_path.py::OrchGatePathTest::test_orch_gate_validates_the_copy_it_reads"
    43	  - control: the prefetched required-check data
    44	    disposition: "residual: the orchestrator records its own ruleset and exact-head check-runs reads in protected evidence, and the verifier parses their raw JSON again rather than accepting saved verification booleans."
    45	  - control: the strength of a test refutation
    46	    disposition: "residual: selector presence and successful required checks provide evidence of the head's CI strength only; P0/P1 remain unrefuted claims until programs item (16), P1-10 part 2, confirms them."
    47	  - control: the outside-sandbox gh exception
    48	    disposition: "residual: decision D-024-17 assigns closure to plan 024 P1-15, whose worker exclusions execute an absolute trusted binary; this task retains today's individual gh reads and does not change worker exclusions."
    49	  - control: the worker-seat write boundary
    50	    disposition: "residual: every worker seat's sandbox denies writes outside its worktree and listed scratch paths, protecting the trusted checkout, review worktree and orchestrator evidence; a same-UID process outside every seat sandbox remains outside this protection."
    51	  - control: orchestrator effect merge
    52	    disposition: "residual: merge uses only gh pr merge --squash --match-head-commit <audited head> after the integration gate; local merges and pushes to main remain forbidden."
    53	  - control: orchestrator effect update-branch
    54	    disposition: "residual: a rebase or gh pr update-branch changes the head, so required CI, feedback collection, task-level audit and security review bind the resulting final head before integration."
    55	  - control: orchestrator effect forced worker removal
    56	    disposition: "residual: no forced removal is planned; the existing dirty-worktree rule applies, and the acceptance record identifies any discarded uncommitted state."
    57	premises:
    58	  - claim: neither new file exists on origin/main
    59	    command: git ls-files scripts/orchestrator/dispositions.py tests/unit/test_dispositions.py | wc -l
    60	    output: |-
    61	      0
    62	  - claim: a sweep item of pr-feedback.py carries source, author, bot, level, path, line, body, url, the source's extra state and disposition, so the thread's commit comes from gh when the item lacks it
    63	    command: sed -n '133,143p' scripts/pr-feedback.py | /usr/bin/grep -o '"[a-z]*"' | tr '\n' ' '
    64	    output: |-
    65	      "source" "author" "login" "slug" "" "bot" "level" "path" "line" "body" "" "url" "disposition" "" 
    66	  - claim: orch-gate.sh invokes the gate once with PR_FEEDBACK_EVIDENCE, the point before which the re-validation runs
    67	    command: /usr/bin/grep -c 'PR_FEEDBACK_EVIDENCE="${sweep}"' scripts/orchestrator/orch-gate.sh
    68	    output: |-
    69	      1
    70	  - claim: the orch-gate tests live in tests/unit/test_orch_gate_path.py and use fake binaries on a private PATH
    71	    command: /usr/bin/grep -c 'def test_orch_gate_' tests/unit/test_orch_gate_path.py
    72	    output: |-
    73	      3
    74	  - claim: audit-pool.sh is not on origin/main at the predecessor's write time, so the --second-opinion mode of programs item (16) is a later task
    75	    command: git ls-files scripts/orchestrator/audit-pool.sh | wc -l
    76	    output: |-
    77	      0
    78	  - claim: the gate already holds the disposition and commit validators dispositions.py reuses
    79	    command: /usr/bin/grep -n 'def commit_in_range\|def parse_disposition' scripts/require-crit-review.py | cut -c1-24
    80	    output: |-
    81	      389:def commit_in_range(
    82	      397:def parse_disposition(
    83	---
    84	
    85	# AGMSG-TASK dotfiles-T133-dispositions-a02 — INV-6 reset of dotfiles-T133-dispositions-a01 (plan 006 S2; plan 024 P1-10 part 1, programs item (5))
    86	
    87	This reset incorporates the independent review-profile redesign and the orchestrator's decisions after C-80 returned `Verdict: incorrect` with eight P1 and one P2 in `.orchestration/validation/dotfiles-T133-dispositions-a02-text-security.md.last.md`.
    88	
    89	The local review of revise-1 head `bdbbbf91765a8f9c2f94565096c8bcbf2fca47b3` stopped the chain at `2026-10-18T22:1xZ`. It found one P1 in the CI-log verifier and two P2 concerning interleaved diagnostic output and loss of the full selector. A second revise would reach INV-6 S2, and the operator forbids a third round. The unsound CI-log design came from the orchestrator's amendment 1.
    90	
    91	PR #419 continues on `tools/dispositions-a01` from `bdbbbf91765a8f9c2f94565096c8bcbf2fca47b3`. The merged P1-11 baseline is `origin/main` at `0e496ce7449e9286aeac3b2770cbff374c7dc5cf`. The worker rebases onto main containing that baseline and merged PR #421 before its first push. One branch and one PR carry the reset. The orchestrator names the worker seat in the TASK line.
    92	
    93	The worker's first push deletes `.orchestration/dotfiles-T133-dispositions-a01/task.md` and adds this dispatched text's byte-identical copy at `.orchestration/dotfiles-T133-dispositions-a02/task.md`. That predecessor-copy deletion is the specified reset bookkeeping exception to `allowed_files`. The predecessor's other artifacts, canonical task text and acceptance history remain unchanged.
    94	
    95	The six command-output premises retain a01's write-time observations as historical evidence. New report, validation, sandbox and learning records use the a02 directory. The a01 acceptance record retains its audit, amendment, revise, advisory rows and S2 withdrawal.
    96	
    97	The design sources are `.orchestration/plans/024-design-programs.md` items (5) and (16), and `.orchestration/plans/024-design-quality.md` section 5.13. The additional inputs are the a01 task and acceptance records, `.orchestration/validation/dotfiles-T133-dispositions-a01-local-review-bdbbbf9.md`, the C-80 verdict, the branch diff through `bdbbbf91`, `scripts/orchestrator/orch-gate.sh` at `origin/main` and the checker docstring in `scripts/orchestrator/task-consistency-check.py`.
    98	
    99	The audit decision at `fa47987` established that a `test:` refutation never executes head code on the orchestrator's host. Running a test in the trusted checkout tests pre-regression code. The merged regime workflow executes base code and inspects the PR as data. It has no head-test execution responsibility.
   100	
   101	The CI results-artifact design is withdrawn. A head-authored test produces its own result, so an artifact, runner, workflow step or download cannot establish producer trust. The Linux keyring restriction also prevents an in-sandbox helper from implementing the proposed authenticated gh fetch. This task adds no results runner, results artifact, artifact download or workflow change.
   102	
   103	The write-boundary premise is that every worker seat's sandbox denies writes outside its worktree and listed scratch paths. The trusted checkout, review worktree and orchestrator's evidence are protected by that boundary. The threat table states its residual once. Decision D-024-17 owns the separate outside-sandbox executable-selection defect; this task retains today's single-command gh reads.
   104	
   105	## Goal
   106	
   107	For a PR head, every review-comment item of the sweep gets a machine proposal: `fixed:<commit>` when an eligible branch commit between the thread's commit and the head touches the thread's hunk, otherwise a demand for `not-applicable:` with one of the three refutation forms. The gate wrapper re-validates the saved dispositions before the gate runs.
   108	
   109	A `test:` refutation holds only when its selector names a test function present at the stated path in the head tree, the required unit-test check runs concluded success for that exact head, and the finding is P2 or P3. A P0/P1 `test:` refutation is a claim that programs item (16)'s second opinion must confirm. `--require-refutation` treats that claim as not yet refuted.
   110	
   111	This evidence has the strength of the head's CI. It supplies no proof against a head-authored test and establishes no per-selector execution outcome.
   112	
   113	## Files
   114	
   115	1. `scripts/orchestrator/dispositions.py <pr> <head> --feedback <sweep.json> [--out <json>] [--require-refutation] [--commits <json>] [--checks <json>]` is a Python CLI run with `python -I`, using the standard library only and an English shdoc-style module docstring.
   116	
   117	   The tool processes each `review_comment` item and each badged `review` finding. The location comes from the item's path and line, with the existing review-body blob-link handling retained. A finding without a location gets the not-applicable demand and still requires a refutation when its disposition is not-applicable.
   118	
   119	   The thread's commit comes from `original_commit_id`, the existing `commit` field, the `--commits` map from URL to commit, or the existing gh read, in that order. A required commit that cannot be obtained or read produces a hold with the reason. Item 6 defines the proposal path that needs no thread-commit lookup.
   120	
   121	   The proposal uses the PR diff and `git diff <thread commit>..<head> -- <path>`. A covering hunk uses its old-side and new-side ranges. The tool walks eligible branch commits newest first and proposes `fixed:<commit>` only for a commit whose own diff against its parent touches that range. Base commits and base-merge-only changes supply no branch fix. An unchanged hunk, an upstream-only change or the absence of an eligible fixing commit produces the not-applicable demand. Paths remain literal Git pathspecs, and sweep text is never evaluated.
   122	
   123	   The output is the sweep with `proposal` added per processed item and the existing `disposition` untouched. A checked not-applicable disposition also receives its verification record. `--out` selects the output file, and stdout is the default. Diagnostic lines go to stderr.
   124	
   125	   The three refutation forms remain `test:<selector>`, `source:{url, fetched_at, quote}` and `diff:<range>`. The existing `; evidence=<form>` disposition representation remains. The CI-log parser and `--ci-log` input are removed.
   126	
   127	   The `test:` form reads the named file with `git show <head>:<path>` and parses it as Python syntax data with the standard-library AST. The full selector identifies the file and function, including its module and class components when present. A full dotted selector maps deterministically to its repository path. The existing path spelling remains supported, and a classless function name must identify one function unambiguously at that path. Missing paths, missing functions, mismatched classes, ambiguous selectors and malformed syntax fail verification with a reason.
   128	
   129	   The head file is never imported, sourced, evaluated or executed. Decorators and test bodies remain data. The verifier performs no unittest discovery and launches no selector.
   130	
   131	   `--checks` supplies prefetched API data. Its JSON contains the repository, exact head, raw ruleset response and raw check-runs response pages. The orchestrator obtains the ruleset with an individual gh read and obtains the head's check runs with one individual `gh api --paginate --slurp` command against `repos/{owner}/{repo}/commits/<head>/check-runs?filter=latest&per_page=100`. The repository comes from the trusted checkout. The check-runs endpoint names the exact audited head.
   132	
   133	   Each gh read runs outside the sandbox as the individual command permitted today. Its output is parsed inside the sandbox and recorded as data. The Python helper, JSON construction and JSON parsing do not run outside the sandbox. The worker uses fixtures for tests and prefetched inputs for authenticated reads; it never attempts to escape the sandbox through a Python gh subprocess.
   134	
   135	   The required unit-test contexts come from the orchestrator's ruleset read. Their current names are `test (ubuntu-24.04, server)`, `test (ubuntu-24.04, client)` and `test (macos-14, client)`. The sweep and head-authored workflow text cannot choose the required names. Missing or malformed ruleset data and an empty required unit-test set fail verification.
   136	
   137	   Every required unit-test context must have its latest check run on the exact head with `status: completed` and `conclusion: success`. Pagination is consumed completely. Selection never searches older runs for a preferred success. A missing context, wrong head, pending run, skipped run, neutral conclusion, failure or malformed response fails verification with a reason.
   138	
   139	   The verification record preserves the original selector, resolved path and function, head, required context names and selected check-run identities and conclusions. It states that selector presence and successful CI were checked. It never states that the named function ran.
   140	
   141	   A P2/P3 finding with both checks satisfied receives a verified `test:` record. A P0/P1 finding receives `claim-recorded` and `refutation.ok: false` until programs item (16), P1-10 part 2, confirms it. Missing or ambiguous priority receives no P2/P3 acceptance. A P0/P1 marker always selects the stricter handling.
   142	
   143	   The `source:` form fetches the named URL read-only, verifies that the quote occurs in the fetched page text and records the page's SHA256. The existing `file://` fixtures remain accepted for tests. A malformed form, failed fetch or absent quote fails verification with the reason. This check establishes quote occurrence and page identity; semantic refutation remains subject to the design's judgment rules.
   144	
   145	   The `diff:` form uses the tool-fixed `<thread commit>..<audited head>` range. A caller-supplied range is accepted only when its endpoints equal those fixed commits, the thread's hunk is unchanged over that range and the disposition names why the path is unreachable. The reason retains the existing minimum of 20 characters. The result is recorded as `claim-recorded`. A range such as `<head>..<head>` is refused. Until programs item (16)'s second opinion confirms it, `--require-refutation` refuses a P0/P1 not-applicable resting on `diff:` alone.
   146	
   147	   `--require-refutation` prints one line per not-applicable disposition with a missing, failed or not-yet-confirmed form and exits 1. The legacy `evidence=<command>` form is reported as `legacy-evidence` and fails only under `--require-refutation`. Exit 0 means the selected mode completed, exit 1 means a required refutation failed, and exit 2 means usage failure or a hold such as an unreadable sweep or a required missing thread commit. Missing check data fails the refutation and never authorizes local head-code execution.
   148	

exec
/bin/zsh -lc "rg -n 'Codex seat worklogs|"'^##|''^###'"' ~/.agents/skills/agmsg-orchestration/SKILL.md" in ~/Workspace/dotfiles
 succeeded in 191ms:
10:## Architecture
17:## Regime activation and progress
29:## Parallel workers
46:## Identity, delivery, and storage
59:## Live verification
64:## Review and integration invariants
95:## Message Contract v1
144:## `.orchestration` Workspace Layout
157:## Orchestrator Playbook
187:## Worker Playbook
217:## Codex seat worklogs
251:## Pitfalls

exec
/bin/zsh -lc 'cat ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail/SKILL.md' in ~/Workspace/dotfiles
 succeeded in 50ms:
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

**Seeking substantial evidence**
exec
/bin/zsh -lc "sed -n '64,94p' ~/.agents/skills/agmsg-orchestration/SKILL.md; sed -n '217,250p' ~/.agents/skills/agmsg-orchestration/SKILL.md" in ~/Workspace/dotfiles
exec
/bin/zsh -lc "git status --short; git rev-parse HEAD; cat .ua/meta.json; python3 -c 'import json; p=json.load(open(\".ua/knowledge-graph.json\")); print(\"\\n\".join(str({k:n.get(k) for k in (\"filePath\",\"summary\")}) for n in p.get(\"nodes\",[]) if any(x in n.get(\"filePath\", \"\") for x in (\"orch-gate\", \"dispositions\", \"permission-guard\"))))'" in ~/Workspace/dotfiles
exec
/bin/zsh -lc "cat .orchestration/validation/dotfiles-T133-dispositions-a02-text-security.md.last.md; cat .orchestration/validation/dotfiles-T133-dispositions-a01-local-review-bdbbbf9.md; rg -n '5\\.14|D-024-17|D-024-18|dispositions-a01|dispositions-a02' .orchestration/plans/024-design-quality.md .orchestration/acceptance* .orchestration/decisions*" in ~/Workspace/dotfiles
 succeeded in 140ms:
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


 succeeded in 225ms:
cat: .orchestration/validation/dotfiles-T133-dispositions-a02-text-security.md.last.md: No such file or directory
---
task: dotfiles-T133-dispositions-a01
head: bdbbbf91765a8f9c2f94565096c8bcbf2fca47b3
pr: 419
base: 3e41e36abc949acd7e6b4859c1a22df9e665c8d4
started: 2026-10-18T22:13:24Z
finished: 2026-10-18T22:17:35Z
findings: 3
engine: codex review --base main (profile review, read-only)
---

- [P1] Verify test outcomes rather than arbitrary job output — scripts/orchestrator/dispositions.py:151-153
- [P2] Handle passing tests with interleaved diagnostic output — scripts/orchestrator/dispositions.py:152-153
- [P2] Preserve the full selector when identifying a test — scripts/orchestrator/dispositions.py:143-146

```text
The test-refutation verifier accepts fabricated or mismatched evidence and rejects some genuinely passing tests. Although PR #419's head CI passed 1,215 Python tests, direct reproductions confirmed these uncovered cases.

Full review comments:

- [P1] Verify test outcomes rather than arbitrary job output — scripts/orchestrator/dispositions.py:151-153
  PR-controlled code can print `test_disabled (test_proof.Proof.test_disabled) ... ok` and satisfy this regex even when that test is skipped. A green unittest run with a separate test printing that line reproduced `refutation.ok: true` for the skipped test. Under `--require-refutation`, an unexecuted test can therefore dismiss a finding. Use runner-controlled results and reject skipped, failed, or absent selections. The proposal-only test cited by the script's `closed` threat-table row does not close this boundary ([AGENTS.md:78](AGENTS.md#L78)).

- [P2] Preserve the full selector when identifying a test — scripts/orchestrator/dispositions.py:143-146
  The path selector discards every directory component, and the dotted selector similarly discards parent modules. Consequently, `tests/missing/test_stub.py::test_pass` is accepted from a passing `test_stub.T.test_pass` log entry even when the selected file does not exist; this was reproduced directly. Resolve the selector against the accepted head and CI discovery root so evidence cannot identify a different or nonexistent test.

- [P2] Handle passing tests with interleaved diagnostic output — scripts/orchestrator/dispositions.py:152-153
  Unittest writes the test identifier before execution and its result afterward, so test diagnostics can separate them. In the [successful head CI log](https://github.com/mryfmo/dotfiles/actions/runs/39168116318/job/117795274272), `test_unknown_interactive_profile_fails` prints `... ERROR: ...` followed by a separate timestamped `ok`. This regex rejects that genuinely passing test, blocking its refutation when enforcement is enabled. Parse complete runner records or structured results instead of requiring the identifier and `ok` on one line.
The test-refutation verifier accepts fabricated or mismatched evidence and rejects some genuinely passing tests. Although PR #419's head CI passed 1,215 Python tests, direct reproductions confirmed these uncovered cases.

Full review comments:

- [P1] Verify test outcomes rather than arbitrary job output — scripts/orchestrator/dispositions.py:151-153
  PR-controlled code can print `test_disabled (test_proof.Proof.test_disabled) ... ok` and satisfy this regex even when that test is skipped. A green unittest run with a separate test printing that line reproduced `refutation.ok: true` for the skipped test. Under `--require-refutation`, an unexecuted test can therefore dismiss a finding. Use runner-controlled results and reject skipped, failed, or absent selections. The proposal-only test cited by the script's `closed` threat-table row does not close this boundary ([AGENTS.md:78](AGENTS.md#L78)).

- [P2] Preserve the full selector when identifying a test — scripts/orchestrator/dispositions.py:143-146
  The path selector discards every directory component, and the dotted selector similarly discards parent modules. Consequently, `tests/missing/test_stub.py::test_pass` is accepted from a passing `test_stub.T.test_pass` log entry even when the selected file does not exist; this was reproduced directly. Resolve the selector against the accepted head and CI discovery root so evidence cannot identify a different or nonexistent test.

- [P2] Handle passing tests with interleaved diagnostic output — scripts/orchestrator/dispositions.py:152-153
  Unittest writes the test identifier before execution and its result afterward, so test diagnostics can separate them. In the [successful head CI log](https://github.com/mryfmo/dotfiles/actions/runs/39168116318/job/117795274272), `test_unknown_interactive_profile_fails` prints `... ERROR: ...` followed by a separate timestamped `ok`. This regex rejects that genuinely passing test, blocking its refutation when enforcement is enabled. Parse complete runner records or structured results instead of requiring the identifier and `ok` on one line.
```
.orchestration/decisions.tsv:63:D-024-17	2026-10-19T02:4xZ	worker seats: the commands Worker Playbook step 4 sends outside the sandbox (gh) execute an absolute trusted binary rendered from the manifest, never a PATH lookup in the worker shell; the Claude sandbox exclusion and the Codex policy name that absolute path, and a bare gh stays inside the sandbox	the C-80 review of the a05 text (finding 3) showed that any unsandboxed worker command resolved through the worker PATH (mise shims, a worktree mise.toml) runs worker-selected code with full user rights, which defeats every in-process check of the merge gate and of the regime; the seat sandbox write boundary is the load-bearing control and the unsandboxed exemption is its hole	default under the autonomy directive, reported 2026-10-19 11:4x JST; a design-tier item for plan 024 (new P1-15), dispatched after P1-14 as a security: true task with a C-80 text review; scope=design,permission	pending-P1-15
.orchestration/decisions.tsv:64:D-024-18	2026-10-19T02:5xZ	every security: true orchestrator-side task text applies design section 5.14 (trusted-host execution contract: the write-boundary premise, sanitized environment first, trusted-path boundary checks, execute-what-you-verified, 40-hex identities and inode-bound locks, honest residuals, four shared red-then-green tests) by reference, with one threat row per item	the C-80 reviews of three texts on 2026-10-19 (permission-guard-gate-a05, dispositions-a02, audit-pool-a01: 19 P1 in total) found the same unstated premise and the same gaps in each; a design-tier contract replaces per-text rewording (M-20261019-03 class)	default under the autonomy directive, reported 2026-10-19 12:0x JST; scope=design	applied-from-a05-and-the-a02-texts
.orchestration/decisions.tsv:65:D-024-19	2026-10-19T03:0xZ	permission decision rows are read from the committed ledger (git show origin/main:.orchestration/decisions.tsv after fetch), never from the working copy; a working-copy row is a proposal until the records PR carrying it merges, and that PR approval is the operator's operation (design 5.14 item 8)	the second C-80 review of the a05 text: a Claude worker seat's file tools run outside the Seatbelt sandbox and the rendered policy has no path deny, so a same-UID forged row in the working-copy ledger was possible; the committed ledger moves forgery behind a protected-branch merge	default under the autonomy directive, reported 2026-10-19 12:0x JST; the consequence is one records PR (boundary 24) before the a05 merge, approved by the operator through the live hook; scope=design,permission	applied-from-a05
.orchestration/plans/024-design-quality.md:99:## 5.14 信頼ホスト実行契約（trusted-host execution contract、D-024-18）
.orchestration/plans/024-design-quality.md:101:orchestrator 側の仕組み（merge gate、integrate-merge、orch-gate、dispositions、audit-pool、verdict、chain）は、同じホスト上で同じ UID の worker プロセスと共存する。2026-10-19 の C-80 審査（a05、dispositions-a02、audit-pool-a01 の 3 文、計 19 件の P1）は、どの文も同じ前提を書かず同じ穴を持つことを示した。以後、`security: true` の orchestrator 側タスク文は本節を参照で適用し、本節の各項目に対応する threat 行を持つ。文ごとに言い換えない。
.orchestration/plans/024-design-quality.md:103:1. **書き込み境界（前提 6、ランタイム別に正直に）** Codex 席は sandbox（workspace-write）がツールの書き込み全部を自席の worktree と列挙パスに限る。Claude 席は Seatbelt sandbox が Bash を限るだけで、Write/Edit/MultiEdit/NotebookEdit、hook、MCP プロセスは sandbox 外で動き、permission policy（permgate の決定論ポリシー）が path で拒否しない限り anchored checkout や `~/.agents` にも書ける（2026-10-19 時点、描画済み設定にその deny は無い）。したがって前提 6 は「Codex 席は成立、Claude 席は P1-15 が permgate に path 拒否を入れるまで残余」と書く。P1-15 が入るまで、承認の出所は項目 8 の「コミット済み台帳」で守る。書き込みは自席の worktree（`.claude/worktrees/<name>`）、scratch、列挙されたツールキャッシュに限る。anchored checkout（`.claude/worktrees/` 以外）、`~/.agents/agent-config.yaml`、`~/.claude/hooks`、信頼ルートのバイナリ、orchestrator の証跡・スナップショット・lock は worker から書けない。render テストが描画後の deny を検証する。残余は「どの席 sandbox にも属さない同一 UID プロセス」と、Worker Playbook step 4 が sandbox 外に出す少数のコマンド（gh）。後者は D-024-17（P1-15）で絶対パスの実行体に束縛する。
.orchestration/plans/024-design-quality.md:111:10. **sandbox 外コマンドの束縛（D-024-17 の中身）** worker の除外コマンド（gh）は信頼ルートの wrapper が `env -i` と絶対パスの gh、固定の `GH_CONFIG_DIR`（alias を持たない読み取り専用の設定）で実行する。絶対パスだけでは `GH_CONFIG_DIR` の alias 経由でコードが走る。
.orchestration/acceptance/dotfiles-T133-dispositions-a01.md:5:    "AGMSG-TASK v1 task_id=dotfiles-T133-dispositions-a01 round=1 repo=~/Workspace/dotfiles/.claude/worktrees/worker-c task_file=.orchestration/tasks/dotfiles-T133-dispositions-a01.md task_sha256=5ed78fc9a916decddb3fd668e3fb5494b7a01f219e02a68e4c93b7794feeae48 deadline=none done_signal=AGMSG-RESULT note=a009:plan-024-P1-10-part-1(programs-item-5):dispositions.py-and-the-orch-gate.sh-re-validation-step"
.orchestration/acceptance/dotfiles-T133-dispositions-a01.md:22:  "task": "dotfiles-T133-dispositions-a01"
.orchestration/acceptance/dotfiles-T133-dispositions-a01.md:26:# Acceptance record: dotfiles-T133-dispositions-a01
.orchestration/acceptance/dotfiles-T133-dispositions-a01.md:47:- The chain re-run ran the ledger check (rows 2, findings 2, gaps 0) and the audit: `Verdict: incorrect` (`.orchestration/validation/dotfiles-T133-dispositions-a01-audit-fa47987.md`): (1) P1 orchestration, the a01 text line 80: the `diff:<range>` form was specified as "no covering hunk" instead of the design's unreachable-path proof, so `diff:<head>..<head>` passes `--require-refutation` (the orchestrator's text defect); (2) P1 implementation `orch-gate.sh:87`: `test:` refutations run on the trusted main checkout, not the audited head (pre-regression code dismisses a regression; a PR-introduced test cannot run); (3) P2 `dispositions.py:132`: exit 0 with only skipped tests accepted; (4) P2 `dispositions.py:102`: an empty eligible commit list is a hold where upstream-only changes should demand not-applicable; (5) P2 orchestration, this record: `INV-6 0/0/0` understates the rounds (the pre-RESULT Bot fix round dd567d77 counts under C-61: rounds 1 before the RESULT); (6) P2 conformance, `sandbox.md:22`: the worker ran the whole Python helper outside the sandbox (step 4 exempts `gh`, not its caller).
.orchestration/acceptance/dotfiles-T133-dispositions-a01.md:50:- counters before the send (`scripts/regime-counters.sh dotfiles-T133-dispositions-a01 --pr 419`, 21:0xZ): `tasks=1 amendments=0 questions=0 results=1 withdrawn=0 revises=0 first_result_head=97a0820d bot_p1_heads_after_result=0` (no S line).
.orchestration/acceptance/dotfiles-T133-dispositions-a01.md:60:- The chain on the revise-1 head ran the local review: 1 P1 (`dispositions.py:151-153`: the CI-log check accepts `ok` from arbitrary job output, so a passing line elsewhere verifies a `test:` refutation) and 2 P2 (interleaved diagnostic output around a passing test; the full selector not preserved when identifying a test), `.orchestration/validation/dotfiles-T133-dispositions-a01-local-review-bdbbbf9.md`; the chain stopped at "a P0/P1 local finding: the one round or the operator"; its three advisory rows under the owner section are superseded by the deferred redesign.
.orchestration/acceptance/dotfiles-T133-dispositions-a01.md:62:- 2026-10-19T02:51:15Z: C-80 pre-dispatch security review of the a02 text (`.orchestration/validation/dotfiles-T133-dispositions-a02-text-security.md`): `Verdict: incorrect`, eight P1 and one P2. The decisive finding: a head-authored test produces its own result, so no CI artifact can establish producer trust; the artifact design (runner, workflow step, download) is withdrawn before implementation. Revised design: the `test:` form holds for P2/P3 threads when the selector exists in the head tree (git show, a data read) and the head's required unit-test checks concluded success (gh api check-runs, one read outside the sandbox); for P0/P1 it is a claim the item-16 second opinion must confirm; orch-gate.sh sanitizes the environment before git discovery, authenticates dispositions.py against origin/main like the gate itself, and validates the one sweep copy it reads; the outside-sandbox gh is the D-024-17 residual. Revision running (prompt `p110-a02r-redesign-prompt.md`), then a second C-80 review.
.orchestration/acceptance/dotfiles-T133-permission-guard-gate-a04.md:63:- root cause (the whole class, now named): the design treats worker processes as adversarial while every control is an in-process check on the same host; the only thing that can make such checks meaningful is the seat sandbox's write boundary, which no text stated and no test verified. Decisions for the revised a05 text (prompt `p114-a05r-redesign-prompt.md`): premise 6 states the boundary; a render test asserts the rendered worker sandbox denies the trusted root; the hook and entrypoint refuse trusted paths under worker-writable roots; updatedInput binds the verified realpath; the snapshot is re-verified before gh; git runs with NOSYSTEM/GLOBAL=/dev/null/hooksPath=/dev/null/fsmonitor=false/protocol.allow=never; the `--decisions` exception is removed; per-effect rows added; residuals (a same-UID process outside every seat sandbox; the step-4 unsandboxed gh of workers) stated. The unsandboxed-gh residual is a regime design gap beyond P1-14: D-024-17 (default: a worker's sandbox exclusion executes an absolute trusted binary, never a PATH lookup) is recorded for the operator with its default.
.orchestration/acceptance/dotfiles-T133-permission-guard-gate-a04.md:64:- 2026-10-19T03:02Z: C-80 second review of the a05 text: `Verdict: incorrect`, four P1, one P2: (1) the render test cannot close premise 6: the Claude seat sandbox covers shell commands only; the file tools, hooks and MCP processes run outside it, so a Claude worker can write the anchor, ledger or snapshots unless its permission policy denies it; (2) D-024-17 is pending (no present mitigation) and an absolute gh still executes worker code through a worker-selected GH_CONFIG_DIR alias; (3) `uv run --offline --with pyyaml` imports from the uv cache the worker sandbox may write (~/.cache/uv is in every seat's allow list), so a worker can poison the code the authoritative guard executes; (4) the unchanged orch-gate.sh rebuilds its environment without the git controls and the validator calls bare git, so the contract is not implementable without editing orch-gate.sh; (5) `protocol.allow=never` also blocks the required HTTPS fetch (probe: transport https not allowed). Decisions pending the facts (the rendered worker permission policy for file tools; the codex sandbox scope) read at 03:0xZ; design 5.14 is amended (per-runtime boundary, protocol.https.allow=always, a private UV_CACHE_DIR under the trusted root, D-024-17 widened to a trusted wrapper with env -i and a fixed GH_CONFIG_DIR); orch-gate.sh joins a05 and P1-10 a02 is sequenced after a05 for that file.
.orchestration/acceptance/dotfiles-T133-permission-guard-gate-a04.md:65:- note (2026-10-19T03:05Z): the Codex seat sandbox scope asserted in 5.14 item 1 rests on the seats' own reports (a010: `packed-refs.lock` under the main .git refused as outside its writable roots, 00:44Z; a012: `~/.cache/uv` writes refused, 23:38Z) and on codex `--sandbox workspace-write` semantics; the rendered profile config was not re-read (the chezmoi modify script embeds it). The Claude-seat gap (file tools outside Seatbelt, no path deny in the rendered policy) is read from `home/.chezmoitemplates/claude-settings-managed.json` (deny list lines 14-30; `defaultMode: auto`) and the worker `settings.local.json` (gh denies only).
.orchestration/acceptance/dotfiles-T133-verdict-audit-pool-a03.md:22:- 2026-10-19T02:58:31Z: C-80 review of the audit-pool-a01 text (`.orchestration/validation/dotfiles-T133-audit-pool-a01-text-security.md`): `Verdict: incorrect`, six P1 and four P2 (mise-shim resolution; GIT_* inheritance; tracked-and-unchanged checks before execution through mutable paths; previous evidence not frozen; symlink redirects of worktree and output paths; the queue lock replaceable; the shadow TSV rows not bound to outputs; shared physical slots across queues; 7-char head names collide; the closure test reads only the JSON ledger). The third text with the same class in one morning → design section 5.14 (D-024-18) written; a01 is withdrawn from a009's queue before it started, and a02 (the a01 text with 5.14 applied and the ten findings as items) is redesigned for a008.
.orchestration/acceptance/dotfiles-T133-ci-efficiency-a02.md:165:- note (13:4xZ): the dispatched text of `dotfiles-T133-dispositions-a01` (sha 5ed78fc9…) pastes premise 6's output as `397:def parse_disposition(`; the command (`cut -c1-24`) prints `397:def parse_dispositio`. A records-form defect of the orchestrator's paste; C14 reports it at acceptance and its disposition is `records-form`, no amendment is spent on it.
.orchestration/acceptance/dotfiles-T133-result-precheck-a02.md:69:- 13:4xZ: `AGMSG-ACCEPTANCE … status=withdrawn` sent to a009 (wJ:p2); the a03 redesign (review profile, prompt `.agents/worklog/orchestrator-glue/p15-a03-redesign-prompt.md`) follows and takes priority over a009's dotfiles-T133-dispositions-a01 when it arrives. Record: `.orchestration/acceptance/dotfiles-T133-result-precheck-a03.md` (created at dispatch).

 succeeded in 354ms:
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
?? .orchestration/acceptance/dotfiles-T129-anthropic-auth-runtime-check-a01.md
?? .orchestration/acceptance/dotfiles-T129-assets-omp-hcom-followup-a02.md
?? .orchestration/acceptance/dotfiles-T129-audit-inherit-replan-json-followup-a01.md
?? .orchestration/acceptance/dotfiles-T129-audit-inherit-replan-json-followup-a02.md
?? .orchestration/acceptance/dotfiles-T129-hcom-dispatch-bus-a01.md
?? .orchestration/acceptance/dotfiles-T129-integration-seat-result-gate-cap-followup-a01.md
?? .orchestration/acceptance/dotfiles-T129-normalised-comparison-lint-followup-a01.md
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
?? .orchestration/acceptance/dotfiles-T133-dispositions-a01.md
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
?? .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a01.md
?? .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a02.md
?? .orchestration/acceptance/dotfiles-T133-verdict-audit-pool-a01.md
?? .orchestration/acceptance/dotfiles-T133-verdict-audit-pool-a02.md
?? .orchestration/acceptance/dotfiles-T133-verdict-audit-pool-a03.md
?? .orchestration/acceptance/dotfiles-T133-worker-cap-hookspath-a01.md
?? .orchestration/acceptance/dotfiles-T133-worker-cap-hookspath-a02.md
?? .orchestration/acceptance/dotfiles-T133-worker-cap-hookspath-followup-a01.md
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
?? .orchestration/tasks/dotfiles-T129-anthropic-auth-runtime-check-a01.md
?? .orchestration/tasks/dotfiles-T129-assets-omp-hcom-followup-a02.md
?? .orchestration/tasks/dotfiles-T129-assets-omp-hcom-followup-a03.md
?? .orchestration/tasks/dotfiles-T129-audit-inherit-replan-json-followup-a02.md
?? .orchestration/tasks/dotfiles-T129-audit-inherit-replan-json-followup-a03.md
?? .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a01.md
?? .orchestration/tasks/dotfiles-T129-normalised-comparison-lint-followup-a02.md
?? .orchestration/tasks/dotfiles-T129-omp-config-render-a01.md
?? .orchestration/tasks/dotfiles-T130-sandbox-portability-followup-a01.md
?? .orchestration/tasks/dotfiles-T131-claude-pinned-merge-gate-review-a01.md
?? .orchestration/tasks/dotfiles-T132-make-update-followups-a01.md
?? .orchestration/tasks/dotfiles-T132-merge-train-builder-a01.md
?? .orchestration/tasks/dotfiles-T132-merge-train-ci-a01.md
?? .orchestration/tasks/dotfiles-T133-audit-pool-a01.md
?? .orchestration/tasks/dotfiles-T133-ci-efficiency-a01.md
?? .orchestration/tasks/dotfiles-T133-ci-efficiency-a02.md
?? .orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a02.md
?? .orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a03.md
?? .orchestration/tasks/dotfiles-T133-dispositions-a01.md
?? .orchestration/tasks/dotfiles-T133-dispositions-a02.md
?? .orchestration/tasks/dotfiles-T133-dispositions-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-permission-guard-gate-a01.md
?? .orchestration/tasks/dotfiles-T133-permission-guard-gate-a02.md
?? .orchestration/tasks/dotfiles-T133-permission-guard-gate-a03.md
?? .orchestration/tasks/dotfiles-T133-permission-guard-gate-a04.md
?? .orchestration/tasks/dotfiles-T133-permission-guard-gate-a05.md
?? .orchestration/tasks/dotfiles-T133-permission-guard-gate-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-regime-ci-a01.md
?? .orchestration/tasks/dotfiles-T133-regime-ci-a02.md
?? .orchestration/tasks/dotfiles-T133-regime-ci-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-result-precheck-a01.md
?? .orchestration/tasks/dotfiles-T133-result-precheck-a02.md
?? .orchestration/tasks/dotfiles-T133-result-precheck-a03.md
?? .orchestration/tasks/dotfiles-T133-result-precheck-a04.md
?? .orchestration/tasks/dotfiles-T133-result-precheck-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a01.md
?? .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a02.md
?? .orchestration/tasks/dotfiles-T133-task-generator-plan-check-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-verdict-audit-pool-a01.md
?? .orchestration/tasks/dotfiles-T133-verdict-audit-pool-a02.md
?? .orchestration/tasks/dotfiles-T133-verdict-audit-pool-a03.md
?? .orchestration/tasks/dotfiles-T133-verdict-audit-pool-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-cap-hookspath-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-cap-hookspath-a02.md
?? .orchestration/tasks/dotfiles-T133-worker-cap-hookspath-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-cap-hookspath-followup-a02.md
?? .orchestration/tasks/dotfiles-T133-worker-hooks-path-a01.md
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
?? .orchestration/validation/dotfiles-T129-audit-inherit-replan-json-followup-a02-chain-6fd8c49.log
?? .orchestration/validation/dotfiles-T129-audit-inherit-replan-json-followup-a02-chain-9d13a06.log
?? .orchestration/validation/dotfiles-T129-audit-inherit-replan-json-followup-a02-crit.json
?? .orchestration/validation/dotfiles-T129-audit-inherit-replan-json-followup-a02-local-review-9d13a06.md
?? .orchestration/validation/dotfiles-T129-audit-inherit-replan-json-followup-a02-pr-feedback.json
?? .orchestration/validation/dotfiles-T129-audit-inherit-replan-json-followup-a02-review-receipt.md
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
?? .orchestration/validation/dotfiles-T129-normalised-comparison-lint-followup-a01-chain-b0479c8.log
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
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a01-audit-9da0ed3.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a01-audit-9da0ed3.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a01-chain-37d969e.log
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a01-chain-9da0ed3.log
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a01-crit.json
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a01-local-review-9da0ed3.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a01-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a01-review-receipt.md
?? .orchestration/validation/dotfiles-T133-verdict-audit-pool-a01-chain-0db5f17.log
?? .orchestration/validation/dotfiles-T133-verdict-audit-pool-a01-chain-485d6b3.log
?? .orchestration/validation/dotfiles-T133-verdict-audit-pool-a01-chain-85a4722.log
?? .orchestration/validation/dotfiles-T133-verdict-audit-pool-a01-local-review-85a4722.md
?? .orchestration/validation/dotfiles-T133-verdict-audit-pool-a02-chain-82b99ed.log
?? .orchestration/validation/dotfiles-T133-verdict-audit-pool-a02-chain-b8998de.log
?? .orchestration/validation/dotfiles-T133-verdict-audit-pool-a02-chain-cfeca64.log
?? .orchestration/validation/dotfiles-T133-verdict-audit-pool-a02-local-review-b8998de.md
?? .orchestration/validation/dotfiles-T133-verdict-audit-pool-a02-local-review-cfeca64.md
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
212efe972a14d4d5f209bf739c1b8008471ba775
{
  "lastAnalyzedAt": "2026-10-02T14:12:51Z",
  "gitCommitHash": "940a3a2b07adfd14140a0acff96784ef53a0a509",
  "version": "1.0.0",
  "analyzedFiles": 368
}


**Designing gate graph freshness**
codex
The cited acceptance record identifies two gaps that remain relevant: Claude file tools bypass the seat’s shell sandbox, and worker `gh` commands can still run outside it. I’m checking whether the revised task and inherited design actually protect the verifier, evidence and executable paths from those gaps.

exec
/bin/zsh -lc 'cat .orchestration/acceptance/dotfiles-T133-dispositions-a01.md; cat .orchestration/validation/dotfiles-T133-dispositions-a01-audit-fa47987.md.last.md' in ~/Workspace/dotfiles
exec
/bin/zsh -lc "nl -ba .orchestration/plans/024-design-quality.md | sed -n '70,135p'; nl -ba scripts/orchestrator/orch-gate.sh" in ~/Workspace/dotfiles
exec
/bin/zsh -lc "git diff --name-only 940a3a2b07adfd14140a0acff96784ef53a0a509..HEAD | head -35; rg --files .orchestration | rg '(dispositions.*(security|review)|permission-guard-gate-a05|024-design-programs)'" in ~/Workspace/dotfiles
 succeeded in 174ms:
    70	5.13 **「人の判断」の細分化（ルール化・プログラム化できるもの / AI エージェントが判断できるもの / 人にしかできないもの）**
    71	
    72	| 判断項目 | 細分化 | 分類 | 具体（ルールとプログラム） | 位置 |
    73	| --- | --- | --- | --- | --- |
    74	| plan と設計の是非 | 形式の整合: 各 todo 行に完了条件がある、同時実行行の allowed_files が互いに素、各 P1 行がボトルネック id に対応、DoD が「コマンド + 期待出力」で書かれている、各決定に既定値と期限がある、相互参照（PR 番号、ブランチ、タスク id、節番号）が実在する | プログラム | `plan-check.py`（task-consistency-check と同型。plan 群 5 文書を読み、違反 1 行 1 件で exit 1）。`validate` CI に追加 | P1-12 に含める |
    75	| 〃 | 実態との drift: plan の PR/ブランチ/head/状態が gh と git の現在値と一致、progress.tsv の state が受け入れ記録と一致 | プログラム | `plan-check.py --drift`（boundary ごとに実行、不一致を progress に書く） | P1-12 |
    76	| 〃 | 方向の不変条件: 禁止事項（Anthropic OAuth、main への直接 push、`--admin`、人の ask を増やす設定）が plan と diff に無い | プログラム | `plan-check.py --invariants`（禁止パターンの grep と validator 連携） | P1-12 |
    77	| 〃 | 起案、再計画（S1 後）、見積もりの更新、進行中作業の分類（規則表に従う） | AI | 第 3 節の分類規則（Claude/Codex 専用 → E 後に不要、ハーネス非依存 → 継続）と plan 第 8 節のモデルを AI が適用し、plan-check を通してから提示 | orchestrator |
    78	| 〃 | 方向と価値の決定（どのハーネスか、どのベンダーか、費用上限、品質閾値の変更、範囲の増減） | **人** | decisions.tsv に `scope=direction` の行として記録。既定値なし | ユーザー |
    79	| hold（S1 / INV-6 / P0） | 検知と凍結: 同一クラス 3 回、revise 2 回、P0 の出現で artifact を止め、`re-plan:` 行の雛形と `search:` 行を出す | プログラム（既存を拡張） | `three-repeat.sh` + counters + verdict の hold。凍結は `dispatch.sh` が hold 中の task への TASK/revise 送信を拒否 | P1-4a |
    80	| 〃 | クラス別の是正手順（playbook）: `.orchestration/learning/classes.yaml` の各 class に `remedy:`（例: `string-form-comparison` → 正規化関数経由に置換、`ps-output-parsing` → 起動時 JSON 記録との照合、`records-form` → 記録生成の自動化）と `blast_radius:`（許される変更範囲） | プログラム + AI | `hold-playbook.sh <task> <class>`: remedy を再計画の骨格に展開し、変更範囲が task の allowed_files 内なら AI が再計画を書いて再 dispatch（決定不要）。範囲外なら決定パネル行を生成 | 新 P1-13 |
    81	| 〃 | P0（セキュリティ）の即時対応: 修正 forward か revert かの選択 | AI（規則） | 規則: main に入っていれば revert PR を即時、未マージなら hold。例外なし | P1-4a の verdict |
    82	| 〃 | 残存リスクの受容（P0/P1 を直さずに進む）、期限や範囲を変える再計画 | **人** | `D-…-residual-risk` 行。既定値なし | ユーザー |
    83	| not-applicable の refutation | 形の検査: refutation は 3 形式のどれか。(i) `test:<selector>` が所見の前提を再現しない（実行して pass を貼る）、(ii) `source:{url, fetched_at, quote}` が所見と矛盾（quote が取得ページに実在することをハッシュで確認）、(iii) `diff:<range>` で該当経路が到達不能（静的）。所見の file:line が実在、空文・一般論は拒否 | プログラム | `dispositions.py --require-refutation` の 3 形式検査 + 再現コマンドの実行と出力の貼り付け | P1-10 |
    84	| 〃 | 妥当性の判断（P2/P3）: 2 モデルの独立判定の一致 | AI（合議） | `audit-pool.sh --second-opinion <finding>`: audit profile と security profile（または別ベンダー）に refutation を渡し、両方が「所見は成立しない」なら受理。不一致は hold | P1-10 + P1-4a |
    85	| 〃 | 妥当性の判断（P0/P1）で 2 モデルが不一致、または根拠がコマンドで検証できない外部事実（契約条項、業務意図） | **人** | 残存リスクの受容と同じ決定行 | ユーザー |
    86	| trust-boundary タスクのタスク文レビュー | 形の検査: 3 つの形の規則（test selector、sentence、owning task id）、threat_table の単位規則（allowed_files 1 行につき 1 行、非パス制御 1 つにつき 1 行、orchestrator 効果 1 つにつき 1 行）、各行の disposition が `closed`（テストあり）/ `residual`（制御あり）/ `out-of-scope`（owner 実在）、premises が実行出力、invariants の設計文と byte 一致（INV-2） | プログラム | `task-consistency-check.py` の拡張（C11〜C15） | P1-12 |
    87	| 〃 | 内容のレビュー（threat の見落とし、制御の妥当性） | AI（独立モデル、1 ラウンド固定） | 既存の headless review（Codex review profile）を `security: true` のタスクだけに限定。停止条件は SKILL の既定 | 既存 |
    88	| 〃 | 権限・信頼境界を広げるタスク（excludedCommands、allowMachLookup、hooks で gh 書込を決める、sandbox の allowWrite） | **人** | 下の「権限の変更」に合流 | ユーザー |
    89	| ruleset と権限の変更 | 検知: 権限面（`permissions.*`、`excludedCommands`、`allowMachLookup`、`allowWrite`、`allowedDomains`、gh 書込を決める hook、ruleset パラメータ）の diff を機械で抽出し、`D-… scope=permission approved_by=user diff_sha256=<…>` の決定行が無ければ validator と CI が fail | プログラム | `permission-guard.py`（validate CI。diff の sha256 と決定行を照合） | 新 P1-14 |
    90	| 〃 | 提案: 最小の広げ方と threat_table、現在値との diff、適用後の検証 | AI | `ruleset-request.sh`（望む ruleset JSON と現在値の diff を出す）、`ruleset-verify.sh`（適用後に一致を確認し progress に書く） | P1-14 |
    91	| 〃 | 承認そのもの。トークンに権限が無い管理者操作（ruleset のトグル）、資格情報の投入（OAuth ログイン、API キー、relay トークン） | **人** | 構造上の制約（権限・資格情報は人が保持）。plan の「ユーザーが必要なこと」欄に時機付きで明記 | ユーザー |
    92	
    93	結論: 5 項目のうち機械とAI で吸収できる部分を除くと、人に残るのは (a) 方向と価値の決定、(b) P0/P1 の残存リスクの受容、(c) 権限・信頼境界を広げる変更の承認、(d) トークンに権限が無い管理者操作と資格情報の投入、の 4 つ。(c)(d) は能力ではなく権限の所在による。新規タスクは P1-13（hold playbook）と P1-14（permission guard と ruleset 補助）の 2 本。
    94	
    95	5.12 **プログラム仕様** は `024-design-programs.md` に分離（17 項目: verdict.sh、audit-pool.sh と orch-audit.sh --json、schemas、result-precheck.sh、dispositions.py、regime.yml、dispatch.sh --next、acceptance-front-matter.py、git hooks、handoff.sh、flakes、task-from-plan.py）。
    96	
    97	結論: 第 1 段階で消えるのは今の直列点（S1 の一部、S2、S8 の一部）。残る天井は S3（hosted runner）、S4/S5（モデルと監査の枠）、S7（hot spot）で、これらは席数の上限 D10（4 → 6）の根拠になる。6 を超える並列は、S3 と S5 の実測が出るまで plan に入れない。
    98	
    99	## 5.14 信頼ホスト実行契約（trusted-host execution contract、D-024-18）
   100	
   101	orchestrator 側の仕組み（merge gate、integrate-merge、orch-gate、dispositions、audit-pool、verdict、chain）は、同じホスト上で同じ UID の worker プロセスと共存する。2026-10-19 の C-80 審査（a05、dispositions-a02、audit-pool-a01 の 3 文、計 19 件の P1）は、どの文も同じ前提を書かず同じ穴を持つことを示した。以後、`security: true` の orchestrator 側タスク文は本節を参照で適用し、本節の各項目に対応する threat 行を持つ。文ごとに言い換えない。
   102	
   103	1. **書き込み境界（前提 6、ランタイム別に正直に）** Codex 席は sandbox（workspace-write）がツールの書き込み全部を自席の worktree と列挙パスに限る。Claude 席は Seatbelt sandbox が Bash を限るだけで、Write/Edit/MultiEdit/NotebookEdit、hook、MCP プロセスは sandbox 外で動き、permission policy（permgate の決定論ポリシー）が path で拒否しない限り anchored checkout や `~/.agents` にも書ける（2026-10-19 時点、描画済み設定にその deny は無い）。したがって前提 6 は「Codex 席は成立、Claude 席は P1-15 が permgate に path 拒否を入れるまで残余」と書く。P1-15 が入るまで、承認の出所は項目 8 の「コミット済み台帳」で守る。書き込みは自席の worktree（`.claude/worktrees/<name>`）、scratch、列挙されたツールキャッシュに限る。anchored checkout（`.claude/worktrees/` 以外）、`~/.agents/agent-config.yaml`、`~/.claude/hooks`、信頼ルートのバイナリ、orchestrator の証跡・スナップショット・lock は worker から書けない。render テストが描画後の deny を検証する。残余は「どの席 sandbox にも属さない同一 UID プロセス」と、Worker Playbook step 4 が sandbox 外に出す少数のコマンド（gh）。後者は D-024-17（P1-15）で絶対パスの実行体に束縛する。
   104	2. **無害化した環境を最初に** 最初の処理として `env -i` に入り、PATH は信頼ルートで解決した絶対バイナリへのリンクだけの私設ディレクトリ（shims、空、相対は拒否）。git は毎回 `GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null -c core.hooksPath=/dev/null -c core.fsmonitor=false -c protocol.allow=never -c protocol.https.allow=always` と明示 `-C`（https だけ許す。`protocol.allow=never` 単独は必要な fetch を止める）。Python は `-I`。PATH 探索で実行するものは無い。
   105	3. **信頼パスの境界検査** 仕組みが信頼するパス（スクリプト、台帳、証跡、worktree、lock、出力先）は realpath で解決し、`.claude/worktrees/` または manifest の worker ルート配下なら拒否（ask/hold）。symlink 構成要素は解決後に比較し、大小文字を区別しないファイルシステムでは同一性比較を大小文字非依存で行う。
   106	4. **検証したものを実行し、検証した内容を渡す** 検証した実行体はその realpath で実行する（再探索しない）。検証したファイル内容は信頼ルート配下のスナップショット（0600、一意名）として渡し、使用直前に sha256 を再照合する。判断に読んだ証跡は sha256 を出力に記録する。
   107	5. **出力と予約の同一性** 名前には 40 桁の head を使う（7 桁で衝突させない）。lock は信頼ルート配下の固定 inode に O_EXCL で作り、置換を inode 比較で検出する。物理スロット 1 つに lock 1 つ。
   108	6. **正直な残余** 境界だけが緩和するリスクを `closed` と書かない。各文は残余を 1 行で明記する。
   109	8. **承認はコミット済み台帳から読む** permission の決定行（`scope=permission approved_by=user diff_sha256=…`）は anchored checkout の作業コピーではなく、fetch 後の `git show origin/main:.orchestration/decisions.tsv` から読む。作業コピーの行は提案で、記録 PR が main にマージされて初めて承認になる（PR の承認は操作者の操作）。偽造には main へのマージが要る。
   110	9. **私設キャッシュ** orchestrator 側の実行は worker と共有するキャッシュ（`~/.cache/uv`、`~/.local/share/uv`、mise）から実行可能物を読まない。`UV_CACHE_DIR` を anchored checkout 配下（`.agents/worklog/uv-cache`、gitignored、worker 書き込み不可）に固定し、`--offline` で使う。hook は uv を使わず jq と python 標準ライブラリだけで動く。
   111	10. **sandbox 外コマンドの束縛（D-024-17 の中身）** worker の除外コマンド（gh）は信頼ルートの wrapper が `env -i` と絶対パスの gh、固定の `GH_CONFIG_DIR`（alias を持たない読み取り専用の設定）で実行する。絶対パスだけでは `GH_CONFIG_DIR` の alias 経由でコードが走る。
   112	7. **検証** 共通テスト補助 `tests/unit/trusted_exec_contract.py`（P1-6 で作る）を使い、仕組みごとに 4 つの red→green テストを持つ：PATH 先頭の shim が実行されない、植え付けた GIT_* と git 設定が効かない、worker ルート配下の信頼パスが拒否される、検証後に差し替えたファイルが消費側に届かない。
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

 succeeded in 202ms:
---
{
  "audit_findings": [],
  "dispatch": [
    "AGMSG-TASK v1 task_id=dotfiles-T133-dispositions-a01 round=1 repo=~/Workspace/dotfiles/.claude/worktrees/worker-c task_file=.orchestration/tasks/dotfiles-T133-dispositions-a01.md task_sha256=5ed78fc9a916decddb3fd668e3fb5494b7a01f219e02a68e4c93b7794feeae48 deadline=none done_signal=AGMSG-RESULT note=a009:plan-024-P1-10-part-1(programs-item-5):dispositions.py-and-the-orch-gate.sh-re-validation-step"
  ],
  "format": 1,
  "head": "fa47987b408927c507bfadec6115ebdfceb0a110",
  "ledger": [
    {
      "class": "review-body-findings-skipped",
      "id": "4307288053"
    },
    {
      "class": "pathspec-literal",
      "id": "4307288056"
    }
  ],
  "pr": 419,
  "replans": {},
  "searches": [],
  "task": "dotfiles-T133-dispositions-a01"
}
---

# Acceptance record: dotfiles-T133-dispositions-a01

Plan 024 P1-10, part 1 (programs item (5)): `scripts/orchestrator/dispositions.py` (fixed candidates from git, the not-applicable demand, the three refutation forms of 5.13, `--require-refutation`) and the `orch-gate.sh` re-validation step (refusing only under `DISPOSITIONS_REQUIRE_REFUTATION=1`, reporting otherwise, since today's records carry the legacy `evidence=` form). Item (16), `audit-pool.sh --second-opinion`, follows after PR #410. Seat: a009 (worker-c, Claude), after its #417 revise-1 RESULT.

- 2026-10-18T13:4xZ: task text written with six pasted premises, `task-consistency-check.py … : OK`, home-path scan 0 matches, dispatched to a009 (the line above; the full note is in the bus history). Files disjoint from every in-flight task (#410 has no orch-gate.sh; #411, #412, #415, #416, #417, P1-11, P1-14).
- 2026-10-18T14:25:56Z: RESULT round 1 from a009: PR #419 head 97a0820dd416ae7193fb0f74e388aa5371e2ba80 (code head dd567d77), `task_copy=5ed78fc9…` (the dispatched sha), CI 10/10, Bot rounds 2: 4307288053 and 4307288056 `fixed:dd567d77`, `bot_final_head=none-in-15min`; CI round 1 broke `test_orchestrator_tools`'s gate-restore test because the re-validation step ran before the checkout step (moved right before the gate, premise 3); caps 243/350 and 196/450; the legacy `evidence=` form counted 37 of 131 dispositions on main (47 of 141 in the main checkout); a real run on PR #409's sweep gave 2 proposals (one equal to the hand-typed 99b07d2b, one naming the later 492e7e28, both touching the hunk); INV-6 0/0/0. Read at 19:58Z (session suspended); `status=pending-integration` sent 20:0xZ; the chain is queued behind #412 and #410.

## Owned by dotfiles-T133-dispositions-followup-a01 (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)

local:fa47987:1	advisory-p2
local-finding: fa47987:1 not-applicable:advisory P2 owned by dotfiles-T133-dispositions-followup-a01 (- [P2] Reject test refutations that execute only skipped tests — scripts/orchestrator/dispositions.py:131-132); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-dispositions-followup-a01.md (2a43c1c40274561b0dff02438431765c1b42b178b24c408d226a1573fb0887ae)
local:fa47987:2	advisory-p2
local-finding: fa47987:2 not-applicable:advisory P2 owned by dotfiles-T133-dispositions-followup-a01 (- [P2] Return a not-applicable demand for upstream-only changes — scripts/orchestrator/dispositions.py:102-103); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-dispositions-followup-a01.md (2a43c1c40274561b0dff02438431765c1b42b178b24c408d226a1573fb0887ae)

4307288053	review-body-findings-skipped
4307288056	pathspec-literal

- 2026-10-18T20:4xZ to 20:57Z: the chain update-branched PR #419 (97a0820d → fa47987b408927c507bfadec6115ebdfceb0a110, code head dd567d77 unchanged), waited for the required checks, ran the local review (2 advisory P2: a `test:` refutation that executes only skipped tests passes, dispositions.py:131-132; an upstream-only change should return the not-applicable demand, :102-103; recorded under the owner `dotfiles-T133-dispositions-followup-a01`), the sweep (9 items, 9 filled, 0 gaps: 7 not-applicable, 2 `fixed:dd567d77`) and the record step, which again wrote no row for the two Bot threads (the P1 4307288053 `review-body-findings-skipped` and the P2 4307288056 `pathspec-literal`), so the ledger check refused the audit (gaps 2); the rows were added by hand (prose and block) and the chain re-run. The same record-step gap as PRs #408, #409 and #416 (P1-6 item).

## Audit of fa47987 (2026-10-18T21:02Z): two P1, four P2; amendment 1 and revise 1

- The chain re-run ran the ledger check (rows 2, findings 2, gaps 0) and the audit: `Verdict: incorrect` (`.orchestration/validation/dotfiles-T133-dispositions-a01-audit-fa47987.md`): (1) P1 orchestration, the a01 text line 80: the `diff:<range>` form was specified as "no covering hunk" instead of the design's unreachable-path proof, so `diff:<head>..<head>` passes `--require-refutation` (the orchestrator's text defect); (2) P1 implementation `orch-gate.sh:87`: `test:` refutations run on the trusted main checkout, not the audited head (pre-regression code dismisses a regression; a PR-introduced test cannot run); (3) P2 `dispositions.py:132`: exit 0 with only skipped tests accepted; (4) P2 `dispositions.py:102`: an empty eligible commit list is a hold where upstream-only changes should demand not-applicable; (5) P2 orchestration, this record: `INV-6 0/0/0` understates the rounds (the pre-RESULT Bot fix round dd567d77 counts under C-61: rounds 1 before the RESULT); (6) P2 conformance, `sandbox.md:22`: the worker ran the whole Python helper outside the sandbox (step 4 exempts `gh`, not its caller).
- correction of (5): the a01 had one pre-RESULT fix round (dd567d77, the two Bot threads) before its RESULT; INV-6 counts amendments 0, questions 0, revises 0, pre-RESULT fix rounds 1.
- decision: findings 1 and 2 are specification defects of the a01 text (the forms were simplified past soundness; `test:` must never execute head code on the orchestrator's host, and `diff:` must not let the caller pick the range), so amendment 1 restates item 1's three forms (CI-log verification for `test:`, a tool-fixed `<thread commit>..<head>` range recorded as a claim for `diff:` with the item (16) second opinion required for P0/P1, the not-applicable demand for upstream-only changes, no skipped-only acceptance, the real run redone with `gh` outside and the helper inside the sandbox), and revise 1 fixes 2, 3, 4 and 6 under it. One round (a01: rounds 1 pre-RESULT, 1 revise; no further round).
- counters before the send (`scripts/regime-counters.sh dotfiles-T133-dispositions-a01 --pr 419`, 21:0xZ): `tasks=1 amendments=0 questions=0 results=1 withdrawn=0 revises=0 first_result_head=97a0820d bot_p1_heads_after_result=0` (no S line).
- 2026-10-18T21:0xZ: amendment 1 (task sha256 05ad23ef…, previous 5ed78fc9…) and `status=revise previous_head=fa47987…` sent to a009 (wJ:p2), to run after its P1-5 a03 RESULT; `check=` names the four tests. INV-6 after the round: amendments 1, questions 0, revises 1 (no further round).
- 2026-10-18T21:45:53Z: revise-1 RESULT from a009: PR #419 head bdbbbf91765a8f9c2f94565096c8bcbf2fca47b3 (code head 9e97732a, previous fa47987b), `task_copy=05ad23ef…` (amendment 1's sha), CI 10/10, `bot=none-in-15min`; the audit's findings `fixed:9e97732a` (orch-gate.sh: the `test:` form verified from the head's CI log; the `diff:` form with the tool-fixed range recorded as a claim; an executed non-skipped test required; upstream-only changes demand not-applicable), the sandbox P2 fixed by redoing the real run (gh outside twice at 7779e78b, the helper inside with `--commits`, proposals unchanged), the record P2 fixed in this record (the round count); selectors 4/4 red on fa47987b and green; caps 284/350 and 279/450; INV-6 amendments 1, questions 0, revises 1 (no further round). `status=pending-integration` sent 21:4xZ; the chain runs on bdbbbf91 after the running #411 chain.
local:bdbbbf9:2	advisory-p2
local-finding: bdbbbf9:2 not-applicable:advisory P2 owned by dotfiles-T133-dispositions-followup-a01 (- [P2] Handle passing tests with interleaved diagnostic output — scripts/orchestrator/dispositions.py:152-153); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-dispositions-followup-a01.md (2a43c1c40274561b0dff02438431765c1b42b178b24c408d226a1573fb0887ae)
local:bdbbbf9:3	advisory-p2
local-finding: bdbbbf9:3 not-applicable:advisory P2 owned by dotfiles-T133-dispositions-followup-a01 (- [P2] Preserve the full selector when identifying a test — scripts/orchestrator/dispositions.py:143-146); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-dispositions-followup-a01.md (2a43c1c40274561b0dff02438431765c1b42b178b24c408d226a1573fb0887ae)

## Local review of bdbbbf9 (2026-10-18T22:1xZ), S2, withdrawal and deferral

- The chain on the revise-1 head ran the local review: 1 P1 (`dispositions.py:151-153`: the CI-log check accepts `ok` from arbitrary job output, so a passing line elsewhere verifies a `test:` refutation) and 2 P2 (interleaved diagnostic output around a passing test; the full selector not preserved when identifying a test), `.orchestration/validation/dotfiles-T133-dispositions-a01-local-review-bdbbbf9.md`; the chain stopped at "a P0/P1 local finding: the one round or the operator"; its three advisory rows under the owner section are superseded by the deferred redesign.
- decision: a second revise would be INV-6's S2 and the operator forbids a third round; the `test:` verification design (parsing the human-readable CI log) came from the orchestrator's amendment 1 and is unsound as a trust input. The task stops (`status=withdrawn` sent to a009 at 22:1xZ; the branch and PR #419 stay). The a02 redesign is deferred until `dotfiles-T133-regime-ci-a02` merges: its `regime` job is the right place to run the named selectors on the head and publish machine-readable per-selector results (ok, fail, error, skipped, missing), which dispositions.py then reads; the deferral is recorded in the progress table (P1-10 part 1 stopped; a02 after P1-11), and the lesson joins M-20261018-15's class (a verification design chosen at amendment time under round pressure).
- 2026-10-19T02:51:15Z: C-80 pre-dispatch security review of the a02 text (`.orchestration/validation/dotfiles-T133-dispositions-a02-text-security.md`): `Verdict: incorrect`, eight P1 and one P2. The decisive finding: a head-authored test produces its own result, so no CI artifact can establish producer trust; the artifact design (runner, workflow step, download) is withdrawn before implementation. Revised design: the `test:` form holds for P2/P3 threads when the selector exists in the head tree (git show, a data read) and the head's required unit-test checks concluded success (gh api check-runs, one read outside the sandbox); for P0/P1 it is a claim the item-16 second opinion must confirm; orch-gate.sh sanitizes the environment before git discovery, authenticates dispositions.py against origin/main like the gate itself, and validates the one sweep copy it reads; the outside-sandbox gh is the D-024-17 residual. Revision running (prompt `p110-a02r-redesign-prompt.md`), then a second C-80 review.
Audited [PR #419](https://github.com/mryfmo/dotfiles/pull/419) at `fa47987`. Final-head CI is green; the task copy matches its dispatch hash.

- [P1] high orchestration `.orchestration/tasks/dotfiles-T133-dispositions-a01.md:80` replaces design §5.13’s “unreachable path” proof with “no covering hunk.” A read-only probe using `diff:<head>..<head>` passed `--require-refutation` with exit 0 despite proving nothing about the finding.
- [P1] high implementation `scripts/orchestrator/orch-gate.sh:87` runs test refutations from the trusted main checkout, not the audited head; a PR regression can therefore be dismissed using passing pre-regression code, while tests introduced by the PR cannot run.
- [P2] high implementation `scripts/orchestrator/dispositions.py:132` accepts exit 0 without checking whether any test actually executed; a run containing one skipped test produced an accepted `exit 0: OK (skipped=1)` refutation.
- [P2] high implementation `scripts/orchestrator/dispositions.py:102` treats an empty eligible commit list as a hold; when only merged upstream changes touch the hunk, it should demand `not-applicable:` instead. Reproduced against this history using `scripts/orchestrator/ci-rerun.sh:90`.
- [P2] high orchestration `.orchestration/acceptance/dotfiles-T133-dispositions-a01.md:31` records `INV-6 0/0/0` despite the documented `dd567d77` fix round; the inherited Completion clause explicitly counts pre-RESULT fix rounds, so this understates the round count.
- [P2] high conformance `.orchestration/dotfiles-T133-dispositions-a01/sandbox.md:22` records running the entire Python helper outside the sandbox; Worker Playbook step 4 exempts `gh`, not its caller. Fetching commit IDs with `gh` and supplying `--commits` would preserve the boundary.

INV-6: violated `.orchestration/acceptance/dotfiles-T133-dispositions-a01.md:31` — the pre-RESULT fix round is omitted.

Orchestration findings: 2

📝 まとめ: 読み取り専用で監査を完了し、6 件の所見を確認しました。ファイルは変更していません。

Not checked: no local full-suite or Bats rerun; verified GitHub CI does not cover the demonstrated refutation gaps.
Verdict: incorrect
 succeeded in 888ms:
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
.orchestration/acceptance/dot-formatter-hook-root-fix-T61-a01.md
.orchestration/acceptance/dot-git-ignore-cc-writes-T56-a01.md
.orchestration/acceptance/dot-macos-brew-untrusted-taps-T57-a01.md
.orchestration/acceptance/dot-main-push-guard-revert-T60-a01.md
.orchestration/acceptance/dot-plain-start-visibility-T45-a01.md
.orchestration/acceptance/dot-ua-graph-refresh-T55-a01.md
.orchestration/acceptance/dot-ubuntu-parity-T2-a01.md
.orchestration/acceptance/dot-worker-kind-guard-T14-a01.md
.orchestration/acceptance/dotfiles-T100-compactiondb-claude-symlink-note-a01.md
.orchestration/acceptance/dotfiles-T101-codex-worker-profile-default-a01.md
.orchestration/plans/024-design-programs.md
.orchestration/tasks/dotfiles-T133-permission-guard-gate-a05.md
.orchestration/validation/dotfiles-T133-dispositions-a02-text-security.md
.orchestration/validation/dotfiles-T133-permission-guard-gate-a05-text-security.md.last.md
.orchestration/validation/dotfiles-T133-dispositions-a01-review-receipt.md
.orchestration/validation/dotfiles-T133-dispositions-a01-local-review-bdbbbf9.md
.orchestration/validation/dotfiles-T133-dispositions-a01-local-review-fa47987.md
.orchestration/validation/dotfiles-T133-permission-guard-gate-a05-text-security.md

**Monitoring token count and source validation**
exec
/bin/zsh -lc "nl -ba .orchestration/tasks/dotfiles-T133-permission-guard-gate-a05.md | sed -n '1,230p'" in ~/Workspace/dotfiles
exec
/bin/zsh -lc 'wc -l .orchestration/validation/dotfiles-T133-dispositions-a02-text-security.md; tail -100 .orchestration/validation/dotfiles-T133-dispositions-a02-text-security.md; cat .orchestration/validation/dotfiles-T133-permission-guard-gate-a05-text-security.md.last.md' in ~/Workspace/dotfiles
exec
/bin/zsh -lc "nl -ba tests/unit/test_orch_gate_path.py | sed -n '1,260p'; rg -n '\\(5\\)|\\(16\\)|dispositions|second-opinion' .orchestration/plans/024-design-programs.md; command -v git gh uv python3 mise; printf '%s\\n' \""'$PATH"' in ~/Workspace/dotfiles
 succeeded in 257ms:
     1	---
     2	format: 2
     3	task_id: dotfiles-T133-permission-guard-gate-a05
     4	kind: code
     5	security: true
     6	allowed_files:
     7	  - scripts/permission-guard.py
     8	  - scripts/orchestrator/ruleset-request.sh
     9	  - scripts/orchestrator/ruleset-verify.sh
    10	  - home/dot_claude/hooks/executable_gh-merge-gate.sh
    11	  - home/dot_agents/agent-config.yaml
    12	  - home/.chezmoitemplates/claude-settings-managed.json
    13	  - scripts/generate-agent-configs.py
    14	  - scripts/validate-agent-assets.py
    15	  - scripts/check-agent-runtime.py
    16	  - home/dot_config/git/config.tmpl
    17	  - tests/unit/test_gh_merge_gate.py
    18	  - tests/unit/test_permission_guard.py
    19	  - tests/unit/test_ruleset_scripts.py
    20	  - tests/unit/test_generate_agent_configs.py
    21	  - tests/unit/test_validate_agent_assets.py
    22	  - tests/unit/test_check_agent_runtime.py
    23	  - .orchestration/dotfiles-T133-permission-guard-gate-a05/**
    24	  - scripts/orchestrator/integrate-merge.sh
    25	  - scripts/orchestrator/finish-pr.sh
    26	  - tests/unit/test_integrate_merge.py
    27	  - tests/unit/test_claude_settings_merge.py
    28	after: []
    29	reset_of: [dotfiles-T133-permission-guard-gate-a04]
    30	threat_table:
    31	  - control: "scripts/permission-guard.py (canonical permission-surface comparison and exact diff SHA256 approval only from the anchored ledger protected by premise 6; the deployed anchor and its ledger remain outside worker-writable roots, and candidate revisions and the PR ledger supply no approval authority)"
    32	    disposition: "closed: tests/unit/test_permission_guard.py::PermissionGuardTest::test_guard_reads_the_ledger_from_the_anchored_checkout_never_the_pr_tree"
    33	  - control: "scripts/orchestrator/ruleset-request.sh (expected ruleset 24397953, duplicate-preserving live comparison, unchanged CLI and GET-only access)"
    34	    disposition: "closed: tests/unit/test_ruleset_scripts.py::RulesetScriptsTest::test_ruleset_comparison_preserves_duplicate_rule_types"
    35	  - control: "scripts/orchestrator/ruleset-verify.sh (comparison result and optional updates of an explicitly selected existing progress ledger only on equality)"
    36	    disposition: "closed: tests/unit/test_ruleset_scripts.py::RulesetScriptsTest::test_progress_is_optional_and_missing_file_is_print_only"
    37	  - control: "home/dot_claude/hooks/executable_gh-merge-gate.sh (only the tracked anchored entrypoint can receive allow; direct gh merge, create and update-branch text always asks)"
    38	    disposition: "closed: tests/unit/test_gh_merge_gate.py::GhMergeGateTest::test_gate_asks_for_every_gh_text_form"
    39	  - control: "home/dot_agents/agent-config.yaml (the deployed checkout anchor, synchronous hook source and removal of exactly the three ask rules approved by D-024-14)"
    40	    disposition: "closed: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_manifest_gates_merge_update_branch_and_create_through_the_hook_and_keeps_every_other_gh_write_on_ask"
    41	  - control: "home/.chezmoitemplates/claude-settings-managed.json (the generated synchronous Bash PreToolUse hook and retained permission rules)"
    42	    disposition: "residual: the existing generator renders this file from the manifest, and make render-check rejects any byte drift."
    43	  - control: "scripts/generate-agent-configs.py (one synchronous Bash PreToolUse command entry rendered from gh_merge_gate_hook)"
    44	    disposition: "closed: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_manifest_gates_merge_update_branch_and_create_through_the_hook_and_keeps_every_other_gh_write_on_ask"
    45	  - control: "scripts/validate-agent-assets.py (every retained gh write ask rule and the exact synchronous deployed hook entry)"
    46	    disposition: "closed: tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_gate_validator_requires_every_retained_ask_rule_and_the_exact_synchronous_hook_entry"
    47	  - control: "scripts/check-agent-runtime.py (the deployed hook's content and executable status)"
    48	    disposition: "closed: tests/unit/test_check_agent_runtime.py::CheckAgentRuntimeTest::test_runtime_check_compares_the_deployed_gh_merge_gate_hook_with_the_source"
    49	  - control: "home/dot_config/git/config.tmpl (removal of the GitHub HTTPS-to-SSH pushinsteadof block)"
    50	    disposition: "residual: the removed block contains no credential, the existing gh credential helper remains, and the operator verifies deployment after make update."
    51	  - control: "tests/unit/test_gh_merge_gate.py (entrypoint identity, exact argv, sanitized checks, trusted tools, gh-text asks, JSON decisions and no-decision cases)"
    52	    disposition: "residual: temporary repositories and synthetic deployed manifests exercise decisions without executing submitted payload text or changing GitHub."
    53	  - control: "tests/unit/test_permission_guard.py (revision fixtures, permission digests, temporary anchored checkouts named by their deployed manifest fixtures and forged PR-tree decisions)"
    54	    disposition: "residual: fixture ledgers exist only at .orchestration/decisions.tsv inside their temporary anchored checkout; tests use no external ledger override, read no credentials and leave the live decision ledger untouched."
    55	  - control: "tests/unit/test_ruleset_scripts.py (GET-only argv capture, duplicate occurrences and optional temporary progress ledgers)"
    56	    disposition: "residual: fake GitHub responses and temporary ledgers preserve the live ruleset and progress records while the audit checks the assertions."
    57	  - control: "tests/unit/test_generate_agent_configs.py (the manifest anchor, rendered synchronous hook and complete retained ask set)"
    58	    disposition: "residual: fixture renders cover supported darwin and linux configurations, and the final-head audit checks the assertions."
    59	  - control: "tests/unit/test_validate_agent_assets.py (independent removal of retained rules and substitution of fake, duplicate or async hook entries)"
    60	    disposition: "residual: fixture settings exercise validation failures without changing deployed settings."
    61	  - control: "tests/unit/test_check_agent_runtime.py (missing, matching, stale and non-executable deployed-hook fixtures)"
    62	    disposition: "residual: a temporary HOME supplies all deployment fixtures, leaving the live runtime untouched."
    63	  - control: ".orchestration/dotfiles-T133-permission-guard-gate-a05/** (this reset's branch artifacts)"
    64	    disposition: "residual: new evidence stays in this directory, separates inherited observations from final-head results and is checked against the diff and CI."
    65	  - control: "scripts/orchestrator/integrate-merge.sh (trusted execution of the gate, final-head security guard, PR checks, pinned squash merge and anchored fast-forward; premise 6 protects trusted scripts, evidence, the ledger and resolved binaries, and worker-writable trusted paths refuse)"
    66	    disposition: "closed: tests/unit/test_integrate_merge.py::IntegrateMergeTest::test_integrate_merge_binds_gh_and_git_to_the_trusted_root"
    67	  - control: "scripts/orchestrator/finish-pr.sh (tracked finishing glue and publication of validated PR-body bytes through a write-once snapshot in the anchored checkout, protected by premise 6 and rehashed immediately before gh)"
    68	    disposition: "closed: tests/unit/test_integrate_merge.py::IntegrateMergeTest::test_finish_pr_passes_a_body_snapshot_never_the_caller_path"
    69	  - control: "tests/unit/test_integrate_merge.py (trusted execution, head mismatch, gate and security refusals, safe fast-forward, publication controls and source- and snapshot-swap fixtures)"
    70	    disposition: "residual: fake binaries capture writes and synthetic files exercise swaps, metadata aliases and evidence failures without merging or publishing anything."
    71	  - control: "tests/unit/test_claude_settings_merge.py (darwin and linux worker-policy renders, seat worktree and scratch/cache allowances, and denied trusted paths)"
    72	    disposition: "residual: fixture renders assert the filesystem write boundary without changing live settings or claiming a live sandbox probe."
    73	  - control: "the task-file copy on the branch (.orchestration/dotfiles-T133-permission-guard-gate-a05/task.md) replaces the reset_of task's copy (.orchestration/dotfiles-T133-permission-guard-gate-a04/task.md)"
    74	    disposition: "residual: the first push deletes the a04 copy and adds the byte-identical dispatched a05 copy; TASK and RESULT carry the a05 copy's SHA256, which the orchestrator verifies at acceptance."
    75	  - control: "the branch evidence records under .orchestration/dotfiles-T133-permission-guard-gate-a05/ (report.md, validation.md, sandbox.md, learning.md and dry-probe transcripts)"
    76	    disposition: "residual: records retain tested identities and verbatim outputs, distinguish historical evidence from new closure and list refused commands for the audit."
    77	  - control: task metadata
    78	    disposition: "residual: the orchestrator checks C1 to C10 and C7b before dispatch and at acceptance, and whole-file byte comparison protects the dispatched metadata."
    79	  - control: metadata separators
    80	    disposition: "residual: the first document separators bound structured metadata, and whole-file byte comparison protects the complete task copy."
    81	  - control: in-process effects
    82	    disposition: "residual: the hook executes no payload text; tests use temporary state; ruleset helpers use GET access and write only an explicitly selected existing temporary progress ledger on equality."
    83	  - control: workflow and interpreter or environment inputs
    84	    disposition: "residual: the orchestrator seat's own Claude Code process launches the interpreter from its own environment, which workers cannot write under premise 6; the retained env bash shebang and Bash startup precede env -i, so that launch remains dependent on the orchestrator environment. A same-UID process outside every seat sandbox remains residual. Trusted execution constructs env -i inputs and a private PATH, excludes caller Git and tool-manager overrides, and runs Python in isolated mode."
    85	  - control: new or renamed scripts
    86	    disposition: "residual: the new deployable inventory is the hook, permission guard, two ruleset helpers and two tracked orchestration entrypoints; RESULT lists all six, and no untracked glue becomes an execution dependency."
    87	  - control: the sanitized environment
    88	    disposition: "closed: tests/unit/test_gh_merge_gate.py::GhMergeGateTest::test_gate_runs_its_identity_checks_under_a_sanitized_environment"
    89	  - control: the interpreter sanitization order
    90	    disposition: "closed: tests/unit/test_gh_merge_gate.py::GhMergeGateTest::test_gate_sanitizes_before_any_other_command"
    91	  - control: "the identity check of the entrypoint (updatedInput names the verified realpath inside the anchored checkout protected by premise 6 and preserves the three arguments)"
    92	    disposition: "closed: tests/unit/test_gh_merge_gate.py::GhMergeGateTest::test_gate_allows_only_through_updated_input_naming_the_verified_realpath"
    93	  - control: the manifest-rendered worker filesystem write boundary
    94	    disposition: "closed: tests/unit/test_claude_settings_merge.py::test_rendered_worker_sandbox_denies_the_trusted_root"
    95	  - control: "the trusted-path write-boundary check (the hook and entrypoint ask when trusted paths lie under .claude/worktrees/ or a manifest-listed worker worktree)"
    96	    disposition: "closed: tests/unit/test_gh_merge_gate.py::GhMergeGateTest::test_gate_refuses_trusted_paths_under_a_worker_writable_root"
    97	  - control: "the approval and executable provenance boundary"
    98	    disposition: "residual: premise 6 prevents sandboxed workers from replacing the deployed anchor, anchored ledger, scripts, evidence or trusted binaries; identity checks and updatedInput operate within that write boundary. A same-UID process outside every seat sandbox remains residual."
    99	  - control: "the Git configuration inputs"
   100	    disposition: "closed: tests/unit/test_gh_merge_gate.py::GhMergeGateTest::test_gate_git_ignores_planted_hooks_fsmonitor_and_global_config"
   101	  - control: "the snapshot rule (the entrypoint creates the snapshot directory under the anchored checkout's gitignored .agents/worklog/snapshots/ at mode 0700, writes the snapshot once and compares its SHA256 again immediately before gh)"
   102	    disposition: "closed: tests/unit/test_integrate_merge.py::IntegrateMergeTest::test_finish_pr_reverifies_the_snapshot_before_gh"
   103	  - control: the snapshot write boundary
   104	    disposition: "residual: premise 6 prevents sandboxed workers from changing the snapshot directory or snapshot, and the last SHA256 comparison refuses a detected change; mode 0700 alone does not exclude the same UID. A same-UID process outside every seat sandbox can still race the last comparison and gh's read."
   105	  - control: the worker sandbox exclusions
   106	    disposition: "residual: the few commands Worker Playbook step 4 sends outside the sandbox through the permission gate, including gh, are outside premise 6's write boundary; D-024-17 closes that exclusion path outside this task by requiring an absolute trusted binary and forbidding PATH lookup."
   107	  - control: orchestrator effect merge
   108	    disposition: "residual: only the trusted entrypoint performs the squash merge, after final-head evidence and API checks, with --match-head-commit binding the merged head; no task branch is merged locally or pushed to main."
   109	  - control: "orchestrator effect PR creation and publication (finish-pr.sh publishes only a snapshot it wrote from validated bytes and reverified, retains the draft flag and applies the records-only check)"
   110	    disposition: "closed: tests/unit/test_integrate_merge.py::IntegrateMergeTest::test_finish_pr_preserves_draft_and_records_only_publication_controls"
   111	  - control: "orchestrator effect fetch, checkout and fast-forward (fetch of origin/main only, fast-forward only, refusal of modified tracked files outside .orchestration and preservation of untracked records)"
   112	    disposition: "closed: tests/unit/test_integrate_merge.py::IntegrateMergeTest::test_integrate_merge_fetches_only_origin_main_and_preserves_local_records"
   113	  - control: orchestrator effect update-branch
   114	    disposition: "residual: direct gh update-branch text asks, and any resulting head receives fresh CI, feedback, audit and security evidence before the integration gate."
   115	  - control: orchestrator effect forced worker removal
   116	    disposition: "residual: no forced removal is planned; the existing dirty-worktree rule applies and the acceptance record identifies any discarded uncommitted state."
   117	premises:
   118	  - claim: none of the five new files exists on origin/main
   119	    command: git ls-files scripts/permission-guard.py scripts/orchestrator/ruleset-request.sh scripts/orchestrator/ruleset-verify.sh home/dot_claude/hooks/executable_gh-merge-gate.sh tests/unit/test_gh_merge_gate.py | wc -l
   120	    output: |-
   121	      0
   122	  - claim: PR #400's branch, the material this task rebuilds from, is at the head the T131 review assessed
   123	    command: git rev-parse origin/fix/claude-pinned-merge-gate
   124	    output: |-
   125	      0b874adb9850ff9647fbc039ec3cf6cc30487488
   126	  - claim: the tracked git config still rewrites GitHub pushes to SSH while the live config (hand-edited) does not, the mismatch D3 (d) resolves
   127	    command: /usr/bin/grep -c 'pushinsteadof = https://github.com/' home/dot_config/git/config.tmpl
   128	    output: |-
   129	      1
   130	  - claim: the manifest still asks for gh pr merge, the rule the hook replaces
   131	    command: /usr/bin/grep -c 'Bash(gh pr merge:\*)' home/dot_agents/agent-config.yaml
   132	    output: |-
   133	      1
   134	  - claim: decisions.tsv carries no permission-scoped decision row yet, so the guard's first run on this PR itself must find the row this task adds
   135	    command: /usr/bin/grep -c 'scope=permission' .orchestration/decisions.tsv
   136	    output: |-
   137	      0
   138	  - claim: >-
   139	      every worker seat runs under a sandbox whose filesystem write policy is rendered from the manifest and allows only the seat's own worktree under .claude/worktrees/, its scratch directories and the listed tool caches, so no worker process can write the anchored checkout outside .claude/worktrees/, the deployed ~/.agents/agent-config.yaml, ~/.claude/hooks, the trusted-root binaries or the orchestrator's snapshot directory; the exception is the few commands Worker Playbook step 4 sends outside the sandbox through the permission gate, including gh, recorded as a residual that D-024-17 closes outside this task by requiring an absolute trusted binary and forbidding PATH lookup.
   140	    sources:
   141	      - home/dot_agents/agent-config.yaml
   142	      - home/.chezmoitemplates/claude-settings-managed.json
   143	    verification: tests/unit/test_claude_settings_merge.py::test_rendered_worker_sandbox_denies_the_trusted_root
   144	---
   145	
   146	# AGMSG-TASK dotfiles-T133-permission-guard-gate-a05 — S1 reset of a04 under D-024-16 (plan 006 S1; plan 024 P1-14 and D3 (d); PR #420)
   147	
   148	This text replaces the stopped a04 task under decision D-024-16. The a04 artifact stopped at `2026-10-19T02:20Z` after six findings of the class `decision-not-bound-to-execution` across a03 and a04. The design tier now permits only a trusted tracked entrypoint. The hook never allows a gh text form.
   149	
   150	PR #420 continues on `tools/permission-guard-gate-a01` from `911f5202e61a2e46f527fcd9a4eda0041e97410a`. Seat a010, worker-e, keeps its branch, prepared fixes and evidence. One PR carries this task. This reset creates no fresh implementation branch or second implementation PR.
   151	
   152	The worker's first push deletes `.orchestration/dotfiles-T133-permission-guard-gate-a04/task.md` and adds the byte-identical dispatched text at `.orchestration/dotfiles-T133-permission-guard-gate-a05/task.md`. That predecessor-copy deletion is the specified reset bookkeeping exception to the edit boundary. The orchestrator owns canonical reset records. Predecessor canonical task texts, evidence and acceptance histories remain unchanged.
   153	
   154	The a04 acceptance record preserves the S1 class table, re-plan line and D-024-16. Its six instances are the following.
   155	
   156	| Source | Finding | Class |
   157	| --- | --- | --- |
   158	| a03 security review, `31d6c322` | Hook binaries resolve through mise shims. | `decision-not-bound-to-execution` |
   159	| a03 security review, `31d6c322` | `.GIT` case variants bypass Git-metadata exclusion. | `decision-not-bound-to-execution` |
   160	| a03 security review, `31d6c322` | The PR tree supplies its own decision ledger. | `decision-not-bound-to-execution` |
   161	| a04 security review, `911f5202` | The allowed bare gh resolves through the caller's PATH. | `decision-not-bound-to-execution` |
   162	| a04 security review, `911f5202` | The body pathname can be swapped after validation. | `decision-not-bound-to-execution` |
   163	| a04 local review, `911f5202` | Caller GIT_* variables redirect checkout identity checks. | `decision-not-bound-to-execution` |
   164	
   165	The `.GIT` finding is the sibling identified in the acceptance record's class accounting. S1 had already been reached by the a04 security review. The attempted instance-by-instance revise after that threshold remains recorded as an orchestration error. This reset does not turn predecessor findings or historical green tests into approvals.
   166	
   167	The first five premises preserve a04's write-time observations verbatim. They remain historical observations, including the ledger observation that predates D-024-14. Premise 6 states the orchestrator's worker sandbox write-boundary contract and receives its own render regression. New reports and evidence use the a05 directory and identify their tested revisions.
   168	
   169	The design sources are `.orchestration/plans/024-design-programs.md` item (14), `.orchestration/plans/024-design-quality.md` section 5.13, D-024-03 (d), D-024-14, D-024-16 and D-024-17. The a04 acceptance record and the three named a03/a04 review records supply the reset findings. D-024-16 replaces their text-form allowance design. The a05 pre-dispatch review at `.orchestration/validation/dotfiles-T133-permission-guard-gate-a05-text-security.md.last.md` returned `Verdict: incorrect` with five P1 and two P2. This text incorporates the orchestrator's seven decisions and retains the stated residuals.
   170	
   171	The deadline `2026-10-19T03:00Z`, which is 12:00 JST, is missed. The new estimate belongs to the orchestrator. The a04 acceptance record reports 14:00–14:30 JST as that estimate, without turning it into a new worker deadline. An open security P1 stops integration regardless of the estimate.
   172	
   173	## Goal
   174	
   175	The PreToolUse hook decides on the executable identity of one tracked anchored entrypoint inside premise 6's write boundary and returns its verified realpath through `hookSpecificOutput.updatedInput`. That entrypoint binds the tools, environment, evidence and head used by execution. Every gh merge, create or update-branch text form asks with the reason `the merge runs through integrate-merge.sh`. The permission guard retains exact-digest approval from the anchored ledger, and the ruleset scripts retain duplicate-preserving display and verification without changing the live ruleset.
   176	
   177	## Files
   178	
   179	0. The inherited dry-probe baseline remains preserved at `.claude/worktrees/worker-e/.orchestration/dotfiles-T133-permission-guard-gate-a01/validation.md`. Its 54 entries, the a02 independent review and corpus, the a03 Bot fixes and fixture repairs, and the a04 regressions retain their original tested identities and limitations.
   180	
   181	   The a03 Ubuntu directory-order repair and macOS resolved-temporary-root repair remain one historical CI-repair round under C-61. The initial omission of the macOS CI failure remains disclosed. Historical formatting, gate, CI and review failures remain failures.
   182	
   183	   The a05 validation record references those transcripts and adds a closure table with input, expected a05 result, actual result, exit status and source identity. Former gh-text allow expectations become ask under D-024-16 and are identified explicitly. Retained regressions keep their original red evidence and receive final-head green runs. The new identity contract has red-then-green evidence under `tests/unit/test_gh_merge_gate.py::GhMergeGateTest::test_gate_allows_only_the_tracked_entrypoint_of_the_anchored_checkout`.
   184	
   185	1. `scripts/permission-guard.py --base <ref> --head <ref> [--manifest home/dot_agents/agent-config.yaml]` retains its Python CLI apart from removal of `--decisions`, isolated interpreter execution, PyYAML dependency through `uv run --offline --with pyyaml`, and standard-library implementation otherwise.
   186	
   187	   It reads both revisions of the manifest and rendered `home/.chezmoitemplates/claude-settings-managed.json` and `home/.chezmoitemplates/codex-config-managed.toml` as data. Its permission surface includes Claude permissions, sandbox settings, permission-deciding PreToolUse hooks, `orchestrator_checkout`, Codex approval and sandbox settings, and the corresponding rendered permission, sandbox and hook surface. Both supported platform renders remain covered.
   188	
   189	   Sorted keys and compact JSON produce canonical surfaces. Equal surfaces print `permission surface: unchanged` and exit 0. A changed surface prints the unified canonical diff and its SHA256. A trusted `D-…` row carries `scope=permission`, `approved_by=user` and the exact `diff_sha256=<digest>` in its `basis` or `what` column. A matching row prints its id and exits 0. A missing approval prints one violation per changed key path and exits 1. Revisions and record contents are never executed.
   190	
   191	   `tests/unit/test_permission_guard.py::PermissionGuardTest::test_permission_diff_without_an_approved_decision_row_fails_and_with_it_passes` retains its red-then-green evidence. Unchanged surfaces, non-permission changes, rendered-only changes, sandbox and anchor changes, malformed data and bad revisions remain covered. Item 11 retains the anchored-ledger regression.
   192	
   193	2. `scripts/orchestrator/ruleset-request.sh [--expected <json>]` retains its CLI, output, exit behavior and GET-only access. It prints the expected JSON for `main integration gate`, ruleset id `24397953`, with the seven contexts named by `tests/unit/test_workflow_orchestration_skip.py`, `strict_required_status_checks_policy: false`, no `pull_request` rule, and retained `deletion` and `non_fast_forward` rules. It reads the live ruleset with `gh api repos/{owner}/{repo}/rulesets/24397953` and prints the canonical comparison.
   194	
   195	   `scripts/orchestrator/ruleset-verify.sh [--expected <json>] [--progress <tsv>]` uses the same comparison. Equality exits 0. An explicitly selected existing progress ledger receives `verified` and the current UTC timestamp in rows `D1` and `D2`, using asserted row anchors and preserving unrelated bytes. An omitted progress flag or absent named file produces print-only behavior and creates no ledger. A difference prints each differing occurrence and key, exits 1 and writes nothing.
   196	
   197	   `tests/unit/test_ruleset_scripts.py::RulesetScriptsTest::test_ruleset_request_prints_the_diff_and_never_writes`, `tests/unit/test_ruleset_scripts.py::RulesetScriptsTest::test_ruleset_verify_reports_each_difference_and_writes_progress_only_on_match` and `tests/unit/test_ruleset_scripts.py::RulesetScriptsTest::test_progress_is_optional_and_missing_file_is_print_only` retain red-then-green evidence. Tests use temporary progress records. The live ruleset and `.orchestration/plans/024-progress.tsv` remain untouched.
   198	
   199	3. `home/dot_claude/hooks/executable_gh-merge-gate.sh` implements the D-024-16 identity gate with English shdoc comments. Its outcomes are allow, ask and no decision. Every outcome exits 0. Allow and ask emit valid PreToolUse decision JSON. No decision emits empty stdout. Recognition never executes, evaluates or sources submitted command text.
   200	
   201	   The orchestrator seat's own Claude Code process launches the interpreter from the orchestrator's environment, which workers cannot write under premise 6. The hook keeps `#!/usr/bin/env bash`. Its first executed command enters `env -i` with fixed bootstrap inputs, before any other command, payload parsing, logging, identity check or tool resolution. The shebang's interpreter lookup and Bash startup occur before that first action and remain dependent on the orchestrator's environment. A same-UID process outside every seat sandbox remains residual.
   202	
   203	   Inside that clean environment, the hook establishes the trusted root from deployed `~/.agents/agent-config.yaml` using shell builtins and fixed bootstrap utilities. It resolves `python3`, `jq`, `gh` and `git` in that root and constructs a private directory of links to the absolute binaries. Item 9 governs resolution and environment construction.
   204	
   205	   `tests/unit/test_gh_merge_gate.py::GhMergeGateTest::test_gate_sanitizes_before_any_other_command` asserts the retained shebang and that entry into `env -i` precedes every other command. It records red-then-green evidence without claiming that in-script sanitization precedes interpreter startup.
   206	
   207	   The manifest's `orchestrator_checkout` is expanded and resolved with realpath. It identifies a primary checkout whose Git common directory resolves to its own `.git` and whose origin identifies `mryfmo/dotfiles`. The deployed manifest supplies this authority independently of payload cwd and candidate revisions. Premise 6 protects that manifest and checkout from worker writes. Git identity operations use the captured absolute git with explicit `-C <anchored checkout>` under the sanitized environment and item 9's fixed configuration controls.
   208	
   209	   The hook and the entrypoint refuse with ask when any path they trust lies under `.claude/worktrees/` or under a worker worktree listed by the deployed manifest, including `worker_worktree`. The checks cover the anchored checkout's `scripts/orchestrator`, `.orchestration/decisions.tsv`, the snapshot directory and every resolved binary. Path resolution and containment use filesystem identity and reject a trusted path reached through a worker-writable component. Checkout identity alone supplies no approval provenance.
   210	
   211	   `tests/unit/test_gh_merge_gate.py::GhMergeGateTest::test_gate_refuses_trusted_paths_under_a_worker_writable_root` exercises both the hook and entrypoint with each trusted path placed under `.claude/worktrees/` and under a manifest-listed worker root, including aliases. Each case asks and performs no merge or publication.
   212	
   213	   The only allow candidate is one shlex argv containing an executable pathname followed by exactly three arguments: `<task> <head40> <pr>`. The task matches `^[A-Za-z0-9][A-Za-z0-9._-]*$`, the head is a full 40-hex commit id, and the PR is decimal. The executable pathname resolves directly to `<anchored checkout>/scripts/orchestrator/integrate-merge.sh`. The hook performs no PATH search for that submitted pathname. There are no extra flags, assignments, wrappers or trailing commands.
   214	
   215	   Raw allow candidates contain none of `;`, `&`, `|`, `<`, `>`, `(`, `)`, backtick, `$`, backslash, newline, `*`, `?`, `[`, `]`, `{`, `}`, `#` or `~`. Space and tab are the permitted separators. Other ASCII control characters are excluded. POSIX shlex performs splitting without expansion or execution.
   216	
   217	   The hook fetches `origin/main` using the absolute git and item 9's fixed configuration controls. The anchored checkout's `git rev-parse HEAD` equals the fetched `git rev-parse origin/main`. `git status --porcelain -- scripts/orchestrator/` is empty. The SHA256 of the file selected by `argv[0]` equals the SHA256 of `git show HEAD:scripts/orchestrator/integrate-merge.sh`. Missing tracking, dirty orchestration scripts, a stale HEAD, a different executable identity or a wrong argument shape asks.
   218	
   219	   An allow response contains `hookSpecificOutput.updatedInput` with the Bash command rebuilt from the checked argv. `argv[0]` is replaced by the verified realpath inside the anchored checkout, and the three argument values remain unchanged. The returned command is encoded without shell expansion. The hook asks whenever it cannot produce that updated input. It never emits allow for the original unchecked spelling alone. Premise 6 protects the verified realpath through execution; a same-UID process outside every seat sandbox remains residual.
   220	
   221	   `tests/unit/test_gh_merge_gate.py::GhMergeGateTest::test_gate_allows_only_through_updated_input_naming_the_verified_realpath` asserts the complete allow JSON, the verified realpath and the unchanged three arguments. It covers a submitted alias, replacement of that alias after validation and failure to construct updated input. The allow response executes through the verified realpath, and missing updated input asks.
   222	
   223	   Every visible gh `pr merge`, `pr create` and `pr update-branch` text form asks, including path-prefixed executables, quoted spellings, draft creation, records-only operations and formerly eligible pinned merges. Its reason is `the merge runs through integrate-merge.sh`. Entrypoint-looking commands that fail the identity or argv contract ask. Every other command receives no decision. The remaining gh-text detection supplies ask only and interprets no operation options.
   224	
   225	   Missing trusted tools, malformed payloads and failed candidate checks ask. Missing jq uses static valid ask JSON. Decision encoding uses the captured absolute jq and logging uses only constructed trusted paths and tools.
   226	
   227	   `tests/unit/test_gh_merge_gate.py::GhMergeGateTest::test_gate_allows_only_the_tracked_entrypoint_of_the_anchored_checkout` is red before the redesign and green afterward. Its positive case is the tracked matching entrypoint at the anchored primary checkout's fetched main. A modified file, an untracked copy with identical bytes, a HEAD behind origin/main, dirty orchestration scripts and each wrong argv shape ask. A failed fetch or hash comparison never allows.
   228	
   229	   `tests/unit/test_gh_merge_gate.py::GhMergeGateTest::test_gate_asks_for_every_gh_text_form` is red against the a04 behavior and green afterward. It covers the three operations, bare and path-prefixed executables, quoted spellings, retained wrapper and heredoc examples, and every former positive operation class. Unrelated commands retain empty output.
   230	

 succeeded in 269ms:
     1	"""Exercise orch-gate.sh's private PATH (the audit of 6847aa9f, P1) with the binaries it runs by name stubbed.
     2	
     3	orch-gate.sh runs from its copy in a temporary root with `uv`, `mise`, `gh` and `git` stubbed first on PATH. Every stub
     4	appends one line `<name> <argv> <cwd>` to one log and runs nothing else: `uv` answers the gate stub's path, `mise
     5	which <name>` answers `installs/<name>` (`payload/<name>` under the mise overrides every run exports, as a real mise
     6	does), and `git` answers `rev-parse` with the root or the head and succeeds silently otherwise. The gate stub also records its environment and its PATH's entries with their link targets. Shebangs are
     7	absolute and the stubs record with builtins or absolute paths, as the private PATH holds neither bash nor env.
     8	"""
     9	
    10	import os
    11	import shutil
    12	import subprocess
    13	import tempfile
    14	import unittest
    15	from pathlib import Path
    16	
    17	ROOT = Path(__file__).resolve().parents[2]
    18	HEAD = "0123456789abcdef0123456789abcdef01234567"
    19	LOG = '#!/bin/bash\nprintf "%s\\n" "{name} $* $(pwd -P)" >> "{t}/calls/log"\n'
    20	STUBS = {
    21	    "bin/uv": 'printf "%s\\n" "{t}/gate/python"\n',
    22	    "bin/mise": '[[ -z "$MISE_CONFIG_FILE$MISE_TRUSTED_CONFIG_PATHS" ]] && d=installs || d=payload\n'
    23	    + 'printf "%s\\n" "{t}/$d/$2"\n',
    24	    "bin/gh": "",
    25	    "bin/git": 'case "$*" in\n*"rev-parse --show-toplevel") printf "%s\\n" "{t}/repo" ;;\n'
    26	    + '*"rev-parse HEAD") printf "%s\\n" {head} ;;\nesac\n',
    27	    "gate/python": '/usr/bin/env > "{t}/calls/gate-env"\n'
    28	    + 'for f in "$PATH"/*; do printf "%s %s\\n" "$f" "$(/usr/bin/readlink "$f")"; done > "{t}/calls/gate-path"\n',
    29	}
    30	
    31	
    32	class OrchGatePathTest(unittest.TestCase):
    33	    def setUp(self):
    34	        temp = tempfile.TemporaryDirectory()
    35	        self.addCleanup(temp.cleanup)
    36	        self.t = Path(temp.name).resolve()
    37	        self.root, self.review = self.t / "repo", self.t / "repo/.claude/worktrees/orchestrator-review"
    38	        for directory in ("bin", "calls", "gate", "pr", "tmp", "repo/scripts/orchestrator", self.review):
    39	            (self.t / directory).mkdir(parents=True, exist_ok=True)
    40	        shutil.copy(ROOT / "scripts/orchestrator/orch-gate.sh", self.root / "scripts/orchestrator")
    41	        v = self.root / ".orchestration/validation"
    42	        v.mkdir(parents=True)
    43	        (v / "t-a01-pr-feedback.json").write_text('{"pr": 9}\n')
    44	        for name in (f"audit-{HEAD[:7]}.md", f"audit-{HEAD[:7]}.md.last.md", "review-receipt.md", "crit.json"):
    45	            (v / f"t-a01-{name}").write_text("x\n")
    46	        (self.root / ".orchestration/acceptance").mkdir()
    47	        (self.root / ".orchestration/acceptance/t-a01.md").write_text("x\n")
    48	        for path, body in STUBS.items():
    49	            self.stub(path, body)
    50	
    51	    def stub(self, path, body):
    52	        name = Path(path).name
    53	        (self.t / path).write_text((LOG + body).format(name=name, t=self.t, head=HEAD))
    54	        (self.t / path).chmod(0o755)
    55	
    56	    def run_gate(self, code):
    57	        """Run the gate from outside the root; return the stub log as (command, cwd) pairs."""
    58	        (self.t / "calls/log").unlink(missing_ok=True)
    59	        env = {**os.environ, "PATH": f"{self.t}/bin{os.pathsep}{os.environ['PATH']}", "TMPDIR": str(self.t / "tmp")}
    60	        # A caller's mise overrides that would point mise which at a payload (PR #355 thread 4267889542).
    61	        env |= {"MISE_CONFIG_FILE": f"{self.t}/payload.toml", "MISE_TRUSTED_CONFIG_PATHS": str(self.t)}
    62	        script = self.root / "scripts/orchestrator/orch-gate.sh"
    63	        result = subprocess.run(
    64	            ["bash", str(script), "t-a01", str(self.t / "pr"), "9"],
    65	            capture_output=True,
    66	            text=True,
    67	            cwd=self.t,
    68	            env=env,
    69	            timeout=30,
    70	            check=False,
    71	        )
    72	        self.assertEqual(code, result.returncode, result.stderr)
    73	        self.stderr = result.stderr
    74	        return [tuple(line.rsplit(" ", 1)) for line in (self.t / "calls/log").read_text().splitlines()]
    75	
    76	    def gate_path(self):
    77	        lines = (self.t / "calls/gate-env").read_text().splitlines()
    78	        return dict(line.split("=", 1) for line in lines if "=" in line)["PATH"]
    79	
    80	    def test_orch_gate_runs_the_gate_with_a_private_path_of_resolved_binaries(self):
    81	        log = self.run_gate(0)
    82	        private = self.gate_path()
    83	        self.assertEqual(1, len(private.split(os.pathsep)))
    84	        # Compare the intersection only, so a failure prints no caller PATH.
    85	        self.assertEqual(set(), {private} & {str(self.t / "bin"), *os.environ["PATH"].split(os.pathsep)})
    86	        links = dict(line.split(" ", 1) for line in (self.t / "calls/gate-path").read_text().splitlines())
    87	        self.assertEqual({f"{private}/{n}": f"{self.t}/installs/{n}" for n in ("gh", "git")}, links)
    88	        # Resolved in the trusted root, before the head is checked out in the review worktree.
    89	        mise = [i for i, (command, _) in enumerate(log) if command.startswith("mise ")]
    90	        self.assertEqual(
    91	            [("mise which gh", str(self.root)), ("mise which git", str(self.root))], [log[i] for i in mise]
    92	        )
    93	        checkout = log.index((f"git -C {self.review} checkout -q --detach {HEAD}", str(self.root)))
    94	        self.assertLess(mise[-1], checkout)
    95	
    96	    def test_orch_gate_refuses_a_binary_resolved_under_a_shims_directory(self):
    97	        for answer in ('printf "%s\\n" "{t}/mise/shims/$2"\n', "exit 0\n"):
    98	            with self.subTest(answer=answer):
    99	                self.stub("bin/mise", answer)
   100	                log = self.run_gate(2)
   101	                self.assertIn("no binary for gh outside a shims directory", self.stderr)
   102	                self.assertEqual([], [command for command, _ in log if command.endswith(HEAD)])
   103	                self.assertEqual([], os.listdir(self.review))
   104	                self.assertFalse((self.t / "calls/gate-env").exists())
   105	
   106	    def test_orch_gate_removes_the_private_bin_on_exit(self):
   107	        self.run_gate(0)
   108	        self.assertTrue(Path(self.gate_path()).parent == self.t / "tmp")
   109	        self.assertEqual([], os.listdir(self.t / "tmp"))
   110	        self.stub("bin/mise", 'printf "%s\\n" "{t}/mise/shims/$2"\n')
   111	        self.run_gate(2)
   112	        self.assertEqual([], os.listdir(self.t / "tmp"))
   113	
   114	
   115	if __name__ == "__main__":
   116	    unittest.main()
9:- 判定条件（9。すべて真で accept）: (1) `precheck` の sha256 = `.orchestration/<task>/precheck.json` の sha256 かつ `head` 一致、(2) 必須チェック 7 本が head で success、(3) audit JSON が schema 合格かつ verdict=correct、または残る所見が `scope=records` のみ、(4) 全スレッドに最終 head の disposition があり、not-applicable には refutation、(5) 変更ファイル ⊆ allowed_files、caps 内、(6) S1 同一クラス < 3、INV-6 revise < 2、(7) P0/P1 の未対処 0、(8) `security: true` なら security review の verdict=correct、(9) 受け入れ記録に書かれた証跡 sha256 と実ファイルが一致。
48:**(5) `scripts/orchestrator/dispositions.py <pr> <head> --feedback <json> [--require-refutation]`**（P1-10）
51:- 出力: `<task>-pr-feedback.json` の候補行（人または (16) の合議が確定）。`--require-refutation` は not-applicable に 3 形式のどれも無い行があると exit 1。`orch-gate.sh` は `PR_FEEDBACK_EVIDENCE` をこのモードで再検証する。
91:**(16) `audit-pool.sh --second-opinion <finding-id> --refutation <file>`**（P1-10）: 所見と refutation を audit profile と security profile（別ベンダーがあればそちら）に渡し、両方が「所見は成立しない」なら `accepted-by-consensus`、不一致なら hold を `dispositions` の結果に書く。P0/P1 の not-applicable はこの合議を必須にする。
95:- 手順: (a) BEHIND かつ衝突があるときだけ `gh pr update-branch <pr>`（strict OFF 後は通常不要）、(b) `gh pr checks <pr> --watch --interval 30`（必須 7 本の success か failure まで）、(c) 最終 head の sweep `scripts/pr-feedback.py <pr> --json .orchestration/validation/<task>-pr-feedback.json`、(d) `dispositions.py` の候補生成、(e) `local-review.sh` と `local-advisory.sh` を実行して validation に保存、(f) `.orchestration/validation/audit-queue/<task>-<head>.request` を置く、(g) `audit-<head>.json` が現れるまで待つ（上限 30 分、超えたら exit 4）、(h) 各 step の command・exit code・時刻を `.orchestration/validation/<task>-integrate-<head>.log` に書く。
/opt/homebrew/bin/git
~/.local/share/mise/shims/gh
~/.local/share/mise/shims/uv
~/.local/share/mise/shims/python3
~/.local/bin/mise
~/.local/share/mise/shims:~/.local/bin:~/.local/bin/common:/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:~/.local/share/mise/installs/npm-openai-codex/0.162.1/lib/node_modules/@openai/codex/node_modules/@openai/codex-darwin-arm64/vendor/aarch64-apple-darwin/codex-path:~/.local/share/mise/installs/node/lts/bin:/usr/bin:/bin:/usr/sbin:/sbin

 succeeded in 274ms:
    2117 .orchestration/validation/dotfiles-T133-dispositions-a02-text-security.md

## Owned by dotfiles-T133-dispositions-followup-a01 (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)

local:fa47987:1	advisory-p2
local-finding: fa47987:1 not-applicable:advisory P2 owned by dotfiles-T133-dispositions-followup-a01 (- [P2] Reject test refutations that execute only skipped tests — scripts/orchestrator/dispositions.py:131-132); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-dispositions-followup-a01.md (2a43c1c40274561b0dff02438431765c1b42b178b24c408d226a1573fb0887ae)
local:fa47987:2	advisory-p2
local-finding: fa47987:2 not-applicable:advisory P2 owned by dotfiles-T133-dispositions-followup-a01 (- [P2] Return a not-applicable demand for upstream-only changes — scripts/orchestrator/dispositions.py:102-103); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-dispositions-followup-a01.md (2a43c1c40274561b0dff02438431765c1b42b178b24c408d226a1573fb0887ae)

4307288053	review-body-findings-skipped
4307288056	pathspec-literal

- 2026-10-18T20:4xZ to 20:57Z: the chain update-branched PR #419 (97a0820d → fa47987b408927c507bfadec6115ebdfceb0a110, code head dd567d77 unchanged), waited for the required checks, ran the local review (2 advisory P2: a `test:` refutation that executes only skipped tests passes, dispositions.py:131-132; an upstream-only change should return the not-applicable demand, :102-103; recorded under the owner `dotfiles-T133-dispositions-followup-a01`), the sweep (9 items, 9 filled, 0 gaps: 7 not-applicable, 2 `fixed:dd567d77`) and the record step, which again wrote no row for the two Bot threads (the P1 4307288053 `review-body-findings-skipped` and the P2 4307288056 `pathspec-literal`), so the ledger check refused the audit (gaps 2); the rows were added by hand (prose and block) and the chain re-run. The same record-step gap as PRs #408, #409 and #416 (P1-6 item).

## Audit of fa47987 (2026-10-18T21:02Z): two P1, four P2; amendment 1 and revise 1

- The chain re-run ran the ledger check (rows 2, findings 2, gaps 0) and the audit: `Verdict: incorrect` (`.orchestration/validation/dotfiles-T133-dispositions-a01-audit-fa47987.md`): (1) P1 orchestration, the a01 text line 80: the `diff:<range>` form was specified as "no covering hunk" instead of the design's unreachable-path proof, so `diff:<head>..<head>` passes `--require-refutation` (the orchestrator's text defect); (2) P1 implementation `orch-gate.sh:87`: `test:` refutations run on the trusted main checkout, not the audited head (pre-regression code dismisses a regression; a PR-introduced test cannot run); (3) P2 `dispositions.py:132`: exit 0 with only skipped tests accepted; (4) P2 `dispositions.py:102`: an empty eligible commit list is a hold where upstream-only changes should demand not-applicable; (5) P2 orchestration, this record: `INV-6 0/0/0` understates the rounds (the pre-RESULT Bot fix round dd567d77 counts under C-61: rounds 1 before the RESULT); (6) P2 conformance, `sandbox.md:22`: the worker ran the whole Python helper outside the sandbox (step 4 exempts `gh`, not its caller).
- correction of (5): the a01 had one pre-RESULT fix round (dd567d77, the two Bot threads) before its RESULT; INV-6 counts amendments 0, questions 0, revises 0, pre-RESULT fix rounds 1.
- decision: findings 1 and 2 are specification defects of the a01 text (the forms were simplified past soundness; `test:` must never execute head code on the orchestrator's host, and `diff:` must not let the caller pick the range), so amendment 1 restates item 1's three forms (CI-log verification for `test:`, a tool-fixed `<thread commit>..<head>` range recorded as a claim for `diff:` with the item (16) second opinion required for P0/P1, the not-applicable demand for upstream-only changes, no skipped-only acceptance, the real run redone with `gh` outside and the helper inside the sandbox), and revise 1 fixes 2, 3, 4 and 6 under it. One round (a01: rounds 1 pre-RESULT, 1 revise; no further round).
- counters before the send (`scripts/regime-counters.sh dotfiles-T133-dispositions-a01 --pr 419`, 21:0xZ): `tasks=1 amendments=0 questions=0 results=1 withdrawn=0 revises=0 first_result_head=97a0820d bot_p1_heads_after_result=0` (no S line).
- 2026-10-18T21:0xZ: amendment 1 (task sha256 05ad23ef…, previous 5ed78fc9…) and `status=revise previous_head=fa47987…` sent to a009 (wJ:p2), to run after its P1-5 a03 RESULT; `check=` names the four tests. INV-6 after the round: amendments 1, questions 0, revises 1 (no further round).
- 2026-10-18T21:45:53Z: revise-1 RESULT from a009: PR #419 head bdbbbf91765a8f9c2f94565096c8bcbf2fca47b3 (code head 9e97732a, previous fa47987b), `task_copy=05ad23ef…` (amendment 1's sha), CI 10/10, `bot=none-in-15min`; the audit's findings `fixed:9e97732a` (orch-gate.sh: the `test:` form verified from the head's CI log; the `diff:` form with the tool-fixed range recorded as a claim; an executed non-skipped test required; upstream-only changes demand not-applicable), the sandbox P2 fixed by redoing the real run (gh outside twice at 7779e78b, the helper inside with `--commits`, proposals unchanged), the record P2 fixed in this record (the round count); selectors 4/4 red on fa47987b and green; caps 284/350 and 279/450; INV-6 amendments 1, questions 0, revises 1 (no further round). `status=pending-integration` sent 21:4xZ; the chain runs on bdbbbf91 after the running #411 chain.
local:bdbbbf9:2	advisory-p2
local-finding: bdbbbf9:2 not-applicable:advisory P2 owned by dotfiles-T133-dispositions-followup-a01 (- [P2] Handle passing tests with interleaved diagnostic output — scripts/orchestrator/dispositions.py:152-153); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-dispositions-followup-a01.md (2a43c1c40274561b0dff02438431765c1b42b178b24c408d226a1573fb0887ae)
local:bdbbbf9:3	advisory-p2
local-finding: bdbbbf9:3 not-applicable:advisory P2 owned by dotfiles-T133-dispositions-followup-a01 (- [P2] Preserve the full selector when identifying a test — scripts/orchestrator/dispositions.py:143-146); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-dispositions-followup-a01.md (2a43c1c40274561b0dff02438431765c1b42b178b24c408d226a1573fb0887ae)

## Local review of bdbbbf9 (2026-10-18T22:1xZ), S2, withdrawal and deferral

- The chain on the revise-1 head ran the local review: 1 P1 (`dispositions.py:151-153`: the CI-log check accepts `ok` from arbitrary job output, so a passing line elsewhere verifies a `test:` refutation) and 2 P2 (interleaved diagnostic output around a passing test; the full selector not preserved when identifying a test), `.orchestration/validation/dotfiles-T133-dispositions-a01-local-review-bdbbbf9.md`; the chain stopped at "a P0/P1 local finding: the one round or the operator"; its three advisory rows under the owner section are superseded by the deferred redesign.
- decision: a second revise would be INV-6's S2 and the operator forbids a third round; the `test:` verification design (parsing the human-readable CI log) came from the orchestrator's amendment 1 and is unsound as a trust input. The task stops (`status=withdrawn` sent to a009 at 22:1xZ; the branch and PR #419 stay). The a02 redesign is deferred until `dotfiles-T133-regime-ci-a02` merges: its `regime` job is the right place to run the named selectors on the head and publish machine-readable per-selector results (ok, fail, error, skipped, missing), which dispositions.py then reads; the deferral is recorded in the progress table (P1-10 part 1 stopped; a02 after P1-11), and the lesson joins M-20261018-15's class (a verification design chosen at amendment time under round pressure).
- 2026-10-19T02:51:15Z: C-80 pre-dispatch security review of the a02 text (`.orchestration/validation/dotfiles-T133-dispositions-a02-text-security.md`): `Verdict: incorrect`, eight P1 and one P2. The decisive finding: a head-authored test produces its own result, so no CI artifact can establish producer trust; the artifact design (runner, workflow step, download) is withdrawn before implementation. Revised design: the `test:` form holds for P2/P3 threads when the selector exists in the head tree (git show, a data read) and the head's required unit-test checks concluded success (gh api check-runs, one read outside the sandbox); for P0/P1 it is a claim the item-16 second opinion must confirm; orch-gate.sh sanitizes the environment before git discovery, authenticates dispositions.py against origin/main like the gate itself, and validates the one sweep copy it reads; the outside-sandbox gh is the D-024-17 residual. Revision running (prompt `p110-a02r-redesign-prompt.md`), then a second C-80 review.
Audited [PR #419](https://github.com/mryfmo/dotfiles/pull/419) at `fa47987`. Final-head CI is green; the task copy matches its dispatch hash.

- [P1] high orchestration `.orchestration/tasks/dotfiles-T133-dispositions-a01.md:80` replaces design §5.13’s “unreachable path” proof with “no covering hunk.” A read-only probe using `diff:<head>..<head>` passed `--require-refutation` with exit 0 despite proving nothing about the finding.
- [P1] high implementation `scripts/orchestrator/orch-gate.sh:87` runs test refutations from the trusted main checkout, not the audited head; a PR regression can therefore be dismissed using passing pre-regression code, while tests introduced by the PR cannot run.
- [P2] high implementation `scripts/orchestrator/dispositions.py:132` accepts exit 0 without checking whether any test actually executed; a run containing one skipped test produced an accepted `exit 0: OK (skipped=1)` refutation.
- [P2] high implementation `scripts/orchestrator/dispositions.py:102` treats an empty eligible commit list as a hold; when only merged upstream changes touch the hunk, it should demand `not-applicable:` instead. Reproduced against this history using `scripts/orchestrator/ci-rerun.sh:90`.
- [P2] high orchestration `.orchestration/acceptance/dotfiles-T133-dispositions-a01.md:31` records `INV-6 0/0/0` despite the documented `dd567d77` fix round; the inherited Completion clause explicitly counts pre-RESULT fix rounds, so this understates the round count.
- [P2] high conformance `.orchestration/dotfiles-T133-dispositions-a01/sandbox.md:22` records running the entire Python helper outside the sandbox; Worker Playbook step 4 exempts `gh`, not its caller. Fetching commit IDs with `gh` and supplying `--commits` would preserve the boundary.

INV-6: violated `.orchestration/acceptance/dotfiles-T133-dispositions-a01.md:31` — the pre-RESULT fix round is omitted.

Orchestration findings: 2

📝 まとめ: 読み取り専用で監査を完了し、6 件の所見を確認しました。ファイルは変更していません。

Not checked: no local full-suite or Bats rerun; verified GitHub CI does not cover the demonstrated refutation gaps.
Verdict: incorrect
 succeeded in 888ms:
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
.orchestration/acceptance/dot-formatter-hook-root-fix-T61-a01.md
.orchestration/acceptance/dot-git-ignore-cc-writes-T56-a01.md
.orchestration/acceptance/dot-macos-brew-untrusted-taps-T57-a01.md
.orchestration/acceptance/dot-main-push-guard-revert-T60-a01.md
.orchestration/acceptance/dot-plain-start-visibility-T45-a01.md
.orchestration/acceptance/dot-ua-graph-refresh-T55-a01.md
.orchestration/acceptance/dot-ubuntu-parity-T2-a01.md
.orchestration/acceptance/dot-worker-kind-guard-T14-a01.md
.orchestration/acceptance/dotfiles-T100-compactiondb-claude-symlink-note-a01.md
.orchestration/acceptance/dotfiles-T101-codex-worker-profile-default-a01.md
.orchestration/plans/024-design-programs.md
.orchestration/tasks/dotfiles-T133-permission-guard-gate-a05.md
.orchestration/validation/dotfiles-T133-dispositions-a02-text-security.md
.orchestration/validation/dotfiles-T133-permission-guard-gate-a05-text-security.md.last.md
.orchestration/validation/dotfiles-T133-dispositions-a01-review-receipt.md
.orchestration/validation/dotfiles-T133-dispositions-a01-local-review-bdbbbf9.md
.orchestration/validation/dotfiles-T133-dispositions-a01-local-review-fa47987.md
.orchestration/validation/dotfiles-T133-permission-guard-gate-a05-text-security.md

**Monitoring token count and source validation**
exec
/bin/zsh -lc "nl -ba .orchestration/tasks/dotfiles-T133-permission-guard-gate-a05.md | sed -n '1,230p'" in ~/Workspace/dotfiles
exec
/bin/zsh -lc 'wc -l .orchestration/validation/dotfiles-T133-dispositions-a02-text-security.md; tail -100 .orchestration/validation/dotfiles-T133-dispositions-a02-text-security.md; cat .orchestration/validation/dotfiles-T133-permission-guard-gate-a05-text-security.md.last.md' in ~/Workspace/dotfiles
exec
/bin/zsh -lc "nl -ba tests/unit/test_orch_gate_path.py | sed -n '1,260p'; rg -n '\\(5\\)|\\(16\\)|dispositions|second-opinion' .orchestration/plans/024-design-programs.md; command -v git gh uv python3 mise; printf '%s\\n' \""'$PATH"' in ~/Workspace/dotfiles
[P1] High confidence [.orchestration/tasks/dotfiles-T133-permission-guard-gate-a05.md:94](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-permission-guard-gate-a05.md:94) The render test cannot close premise 6’s “every worker process” boundary: Claude’s filesystem sandbox covers shell commands, while file tools, hooks and MCP processes remain outside it; no corresponding protection of the anchor, ledger and snapshots is specified. [Sandbox scope](https://code.claude.com/docs/en/sandboxing#what-runs-outside-the-sandbox).

[P1] High confidence [.orchestration/tasks/dotfiles-T133-permission-guard-gate-a05.md:106](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-permission-guard-gate-a05.md:106) D-024-17 is pending, so it supplies no present mitigation for unsandboxed worker execution; even its proposed absolute gh pathname permits shell aliases through worker-selected `GH_CONFIG_DIR`, allowing same-user code execution outside the boundary protecting approvals. [gh configuration](https://cli.github.com/manual/gh_help_environment), [shell aliases](https://cli.github.com/manual/gh_alias_set).

[P1] High confidence [.orchestration/tasks/dotfiles-T133-permission-guard-gate-a05.md:185](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-permission-guard-gate-a05.md:185) `uv run --offline --with pyyaml` consumes executable dependency content from the worker-writable uv cache retained by item 4; pinning the interpreter and using `-I` does not authenticate those imports, so a sandboxed worker can poison code subsequently executed by the authoritative guard. [uv cache](https://docs.astral.sh/uv/concepts/cache/), [Python isolation](https://docs.python.org/3.13/using/cmdline.html#cmdoption-I).

[P1] High confidence [.orchestration/tasks/dotfiles-T133-permission-guard-gate-a05.md:329](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-permission-guard-gate-a05.md:329) The required unchanged `orch-gate.sh` rebuilds its environment at lines 87–89 without the required Git configuration controls, then the validator invokes bare git; links to absolute binaries cannot preserve discarded environment settings or inject `-c` arguments, so the claimed subprocess isolation is not implementable through the specified helper contract.

[P2] High confidence [.orchestration/tasks/dotfiles-T133-permission-guard-gate-a05.md:283](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-permission-guard-gate-a05.md:283) Mandatory `protocol.allow=never` also blocks the required HTTPS fetch unless an explicit protocol exception exists; none is specified, and a read-only host probe returned `fatal: transport 'https' not allowed`, so captured fake-Git calls cannot establish the promised successful allowance and fast-forward paths. [Git protocol policy](https://git-scm.com/docs/git-config#Documentation/git-config.txt-protocolallow).

📝 まとめ: Reviewed every threat row and the available cited acceptance/review records; declared file and effect categories have rows, but the five substantive findings above remain for orchestrator disposition.

Not checked: implementation tests, live sandbox enforcement or deployment; the cited initial a05 `.last.md` was unavailable. Approval integrity remains at risk.
Verdict: incorrect
**Reviewing git object replacement issues**
**Analyzing source URL SSRF and test coverage gaps**
exec
/bin/zsh -lc "rg -n 'PR_FEEDBACK_EVIDENCE|read_text|subprocess|git.*diff|core\\.|GIT_' scripts/require-crit-review.py scripts/validate-agent-assets.py | head -100; sed -n '1,100p' scripts/orchestrator/task-consistency-check.py; sed -n '48,55p' .orchestration/plans/024-design-programs.md" in ~/Workspace/dotfiles
exec
/bin/zsh -lc "nl -ba .orchestration/tasks/dotfiles-T133-permission-guard-gate-a05.md | sed -n '270,345p'; tail -32 .orchestration/tasks/dotfiles-T133-permission-guard-gate-a05.md; sed -n '1,70p' home/.chezmoitemplates/claude-settings-managed.json; rg -n 'excludedCommands|gh|worker_kind|worker_worktree|allowWrite|mise|uv-cache' home/dot_agents/agent-config.yaml | head -65" in ~/Workspace/dotfiles
 succeeded in 132ms:
scripts/require-crit-review.py:12:import subprocess
scripts/require-crit-review.py:24:PR_FEEDBACK_ENV = "PR_FEEDBACK_EVIDENCE"
scripts/require-crit-review.py:138:def run_git(args: list[str], root: Path | None = None) -> subprocess.CompletedProcess[str]:
scripts/require-crit-review.py:139:    return subprocess.run(
scripts/require-crit-review.py:144:        stdout=subprocess.PIPE,
scripts/require-crit-review.py:145:        stderr=subprocess.PIPE,
scripts/require-crit-review.py:306:    text = path.read_text()
scripts/require-crit-review.py:362:        data = json.loads(path.read_text())
scripts/require-crit-review.py:427:        data = json.loads(path.read_text())
scripts/require-crit-review.py:523:        repository = subprocess.run(
scripts/require-crit-review.py:539:        result = subprocess.run(
scripts/require-crit-review.py:614:        result = subprocess.run(
scripts/require-crit-review.py:619:            stdout=subprocess.PIPE,
scripts/require-crit-review.py:620:            stderr=subprocess.PIPE,
scripts/require-crit-review.py:625:        collected = json.loads(collected_path.read_text())
scripts/require-crit-review.py:683:    if not source.is_file() or not source.read_text().strip():
scripts/require-crit-review.py:696:    text = source.read_text()
scripts/require-crit-review.py:752:    lines = path.read_text().split("\n")
scripts/require-crit-review.py:903:    return source.read_text(), None
scripts/require-crit-review.py:960:    The same match as `grep -rl 'classes:.*<class>'`, without a subprocess; the gate reads its result, never
scripts/require-crit-review.py:969:            lines = path.read_text(errors="replace").splitlines()
scripts/require-crit-review.py:1005:        help="also review committed changes in <base>...HEAD and require PR_FEEDBACK_EVIDENCE and ACCEPTANCE_EVIDENCE, plus AUDIT_EVIDENCE when review is required (PR integration)",
scripts/require-crit-review.py:1033:    # pr_feedback_errors already validated PR_FEEDBACK_EVIDENCE's location and -pr-feedback.json suffix.
scripts/require-crit-review.py:1037:    feedback_document = json.loads((root / feedback).read_text()) if feedback else {}
scripts/validate-agent-assets.py:12:import subprocess
scripts/validate-agent-assets.py:82:    data = yaml.safe_load(path.read_text()) or {}
scripts/validate-agent-assets.py:89:    text = path.read_text()
scripts/validate-agent-assets.py:168:    text = path.read_text()
scripts/validate-agent-assets.py:219:        if not symlink.exists() or symlink.read_text() != expected_target:
scripts/validate-agent-assets.py:232:    for number, line in enumerate(manifest_path.read_text().splitlines(), start=1):
scripts/validate-agent-assets.py:256:    marketplace = json.loads(marketplace_path.read_text())
scripts/validate-agent-assets.py:272:            manifest = json.loads(manifest_path.read_text())
scripts/validate-agent-assets.py:403:    if not crit_rule.exists() or "/crit" not in crit_rule.read_text():
scripts/validate-agent-assets.py:573:GIT_COMMIT_SHA = re.compile(r"^[0-9a-f]{40}$")
scripts/validate-agent-assets.py:651:    if not isinstance(ref_commit, str) or not GIT_COMMIT_SHA.match(ref_commit):
scripts/validate-agent-assets.py:686:        for line in (removal_file.read_text().splitlines() if removal_file.exists() else [])
scripts/validate-agent-assets.py:809:        for match in LITERAL_VERSION_ASSIGNMENT.finditer(path.read_text()):
scripts/validate-agent-assets.py:859:    readme = (ROOT / "README.md").read_text()
scripts/validate-agent-assets.py:939:    text = path.read_text()
scripts/validate-agent-assets.py:958:        result = subprocess.run(
scripts/validate-agent-assets.py:962:            stdout=subprocess.PIPE,
scripts/validate-agent-assets.py:963:            stderr=subprocess.PIPE,
scripts/validate-agent-assets.py:982:    updater = (ROOT / "scripts/update-agent-assets.sh").read_text()
scripts/validate-agent-assets.py:995:    codex_agents = (ROOT / "home/dot_config/codex/AGENTS.md").read_text()
scripts/validate-agent-assets.py:1008:    guard_text = guard_path.read_text()
scripts/validate-agent-assets.py:1025:    readme = (ROOT / "README.md").read_text()
scripts/validate-agent-assets.py:1039:    updater = (ROOT / "scripts/update-agent-assets.sh").read_text()
scripts/validate-agent-assets.py:1072:    codex_agents = (ROOT / "home/dot_config/codex/AGENTS.md").read_text()
scripts/validate-agent-assets.py:1080:    claude_rule_text = claude_rule.read_text()
scripts/validate-agent-assets.py:1093:    if not claude_symlink.exists() or claude_symlink.read_text() != expected_target:
scripts/validate-agent-assets.py:1096:    readme = (ROOT / "README.md").read_text()
scripts/validate-agent-assets.py:1108:    updater = (ROOT / "scripts/update-agent-assets.sh").read_text()
scripts/validate-agent-assets.py:1128:    codex_agents = (ROOT / "home/dot_config/codex/AGENTS.md").read_text()
scripts/validate-agent-assets.py:1142:    claude_rule_text = claude_rule.read_text()
scripts/validate-agent-assets.py:1156:    if not claude_symlink.exists() or claude_symlink.read_text() != expected_target:
scripts/validate-agent-assets.py:1159:    readme = (ROOT / "README.md").read_text()
scripts/validate-agent-assets.py:1171:    policy = json.loads(policy_path.read_text())
scripts/validate-agent-assets.py:1208:    permgate_text = permgate_path.read_text()
scripts/validate-agent-assets.py:1223:    removals = (ROOT / "home/.chezmoiremove").read_text() if (ROOT / "home/.chezmoiremove").exists() else ""
scripts/validate-agent-assets.py:1233:    env_text = env_path.read_text()
scripts/validate-agent-assets.py:1244:    if not express_agent.exists() or "model:" not in express_agent.read_text():
scripts/validate-agent-assets.py:1247:    herdr = (ROOT / "home/dot_local/bin/common/executable_herdr-agents").read_text()
scripts/validate-agent-assets.py:1254:    codex_agents = (ROOT / "home/dot_config/codex/AGENTS.md").read_text()
scripts/validate-agent-assets.py:1262:    claude_rule_text = claude_rule.read_text()
scripts/validate-agent-assets.py:1271:    text = path.read_text()
scripts/validate-agent-assets.py:1288:    setup_text = setup_path.read_text()
scripts/validate-agent-assets.py:1295:    result = subprocess.run(
scripts/validate-agent-assets.py:1299:        stdout=subprocess.PIPE,
scripts/validate-agent-assets.py:1300:        stderr=subprocess.STDOUT,
scripts/validate-agent-assets.py:1310:    result = subprocess.run(
scripts/validate-agent-assets.py:1345:        if removed_skill in path.read_text(errors="ignore"):
scripts/validate-agent-assets.py:1639:    data = json.loads(settings_path.read_text())
scripts/validate-agent-assets.py:1650:    result = subprocess.run(
"""Read-only cross-field check of a format-2 task file, before dispatch and at acceptance (plan 007 T704).

`uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py [--root <repo>] <task.md>...`
resolves the design path (C6) and probes origin/main with git (C8 to C10) under --root (default: the first file's git
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
import pathlib
import re
import subprocess
import sys

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


def front(text):
    return yaml.safe_load(text.split("\n---\n", 1)[0].lstrip("-\n"))


def git(cwd, *args):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=False)


def check(p, root):
    fm = front(text := p.read_text())
    tid = fm.get("task_id")
    suffix = tid.rsplit("-", 1)[-1]
    fails = []
    if tid != p.stem:
        fails.append(f"C1 task_id {tid} != file {p.stem}")
    allowed = fm.get("allowed_files") or []
    own_dir = f".orchestration/{tid}/"
    if not any(a.startswith(own_dir) for a in allowed):
        fails.append(f"C2 allowed_files lacks {own_dir}**")
    for a in allowed:
        m = re.match(r"\.orchestration/([^/]+)/", a)
        if m and m.group(1) != tid:
            fails.append(f"C2 allowed_files names another task directory: {a}")
    rows = fm.get("threat_table") or []
    rowtext = "\n".join((r.get("control") or "") + " " + (r.get("disposition") or "") for r in rows)
    reset_of = fm.get("reset_of") or []
    for rid in reset_of + [tid] if reset_of else []:
        if not re.search(rf"(?:{re.escape(rid)}|-{rid.rsplit('-', 1)[-1]})/task\.md", rowtext):
            fails.append(f"C3 no threat_table row names {rid} task.md")
    for a in allowed:
        # a row's control names the entry only at a path boundary: scripts/foo.py.bak does not name scripts/foo.py
        named = re.compile(re.escape(a.split("*")[0].rstrip("/")) + r"(?=$|[ /\"'(),*?\[])")
        if rows and not any(named.search(r.get("control") or "") for r in rows):
            fails.append(f"C4 allowed path has no threat_table row naming it: {a}")
    dr = fm.get("design_review") or {}
    if dr.get("design") and dr.get("receipt") and (design := root / dr["design"]).exists():
        cur = (front(design.read_text()).get("design_review") or {}).get("receipt")
        if cur and cur != dr["receipt"]:
            fails.append(f"C6 design_review.receipt {dr['receipt']} is not the design's current receipt {cur}")
    for r in rows:
        m = re.search(r"names the (a\d\d) file's hash", r.get("disposition") or "")
        if m and m.group(1) != suffix:
            fails.append(f"C5 residual binds the {m.group(1)} hash, the task is {suffix}: {r.get('control')[:60]}")
    controls = " || ".join((r.get("control") or "") for r in rows)
    for name in C7_NAMES:
        if rows and name not in controls.lower():
            fails.append(f"C7 threat_table has no row named for: {name}")
    prefixes = [re.sub(r"(/\*\*|/\*|\*)$", "", e) for e in allowed if isinstance(e, str)]
    for r in rows:
        if (r.get("control") or "").lstrip('"').startswith(NONPATH):
            continue  # a non-path control may describe several files
        hit = [e for e in prefixes if e and e in (r.get("control") or "")]
        if len(hit) > 1:
            fails.append(f"C7b one row names {len(hit)} allowed_files entries ({', '.join(hit)}); one row per entry")
    body = text.split("\n---\n", 1)[1] if "\n---\n" in text else ""
    if fm.get("kind") == "code":
        for var in sorted(set(re.findall(r"\b[A-Z][A-Z0-9]+(?:_[A-Z0-9]+)*_EVIDENCE\b", body))):
            # an input a script on origin/main already reads is not an added input
            added = git(root, "grep", "-q", var, "origin/main", "--", "scripts", "Makefile", "home").returncode != 0
            if added and rows and var not in controls:
                fails.append(f"C8 the task adds input {var} but no threat row controls it")
    sentences = re.findall(r'"([^"]{20,})"', body) if fm.get("kind") == "docs" else []
**(5) `scripts/orchestrator/dispositions.py <pr> <head> --feedback <json> [--require-refutation]`**（P1-10）
- 入力: pr-feedback.py の JSON（thread_id、commit、path、line、body）。各スレッドの (path, line) を `git diff <thread.commit>..<head> -- <path>` に当て、該当 hunk があれば `fixed:<commit touching the hunk>` を候補に、無ければ `not-applicable:` を要求。
- refutation の 3 形式（5.13）: `test:<selector>`（実行して pass を貼る）、`source:{url, fetched_at, quote}`（quote の実在をページのハッシュで確認）、`diff:<range>`（静的に到達不能）。
- 出力: `<task>-pr-feedback.json` の候補行（人または (16) の合議が確定）。`--require-refutation` は not-applicable に 3 形式のどれも無い行があると exit 1。`orch-gate.sh` は `PR_FEEDBACK_EVIDENCE` をこのモードで再検証する。
- テスト: 変更あり → fixed 候補；変更なし → not-applicable 要求；refutation 無しで exit 1；3 形式それぞれの受理。

**(6) `.github/workflows/regime.yml`（P1-11。任意チェック → 安定後に必須）**


 succeeded in 145ms:
   270	
   271	   Static recognition still cannot identify commands whose names and gated words are entirely assembled at runtime. Such input receives no new allowance from this hook. Native permission controls, permgate and the auto-mode classifier remain the next layer. This task makes no change to them.
   272	
   273	8. The two ruleset scripts preserve every duplicate rule occurrence during canonicalization and comparison. A map keyed only by rule type or a set that removes occurrences does not satisfy this requirement. Two differing rules of one type produce two separately reported differences.
   274	
   275	   `tests/unit/test_ruleset_scripts.py::RulesetScriptsTest::test_ruleset_comparison_preserves_duplicate_rule_types` retains its red-then-green evidence for both scripts. Fixtures cover two differing occurrences, an earlier missing or differing occurrence whose last occurrence matches, and exact equality with duplicates. A mismatch leaves the temporary progress ledger byte-identical. Equality permits an update only to an explicitly selected existing ledger.
   276	
   277	9. Trusted-root binary resolution remains a requirement before hook processing and becomes an execution requirement of both tracked orchestration scripts. The resolver runs from the deployed anchored root in a constructed trusted environment. It follows `scripts/orchestrator/orch-gate.sh`'s private-directory-of-links precedent without inheriting the caller's PATH or tool-manager configuration.
   278	
   279	   The hook resolves `python3`, `jq`, `gh` and `git` to absolute non-shim binaries. Empty, relative and `shims` resolutions ask. Every later invocation uses the captured absolute binary or its private link. Returning to another cwd never repeats resolution.
   280	
   281	   Environment construction starts with item 3's first-action `env -i`. Caller `GIT_DIR`, `GIT_WORK_TREE`, `GIT_CEILING_DIRECTORIES`, other `GIT_*` overrides, PATH and tool-manager overrides do not reach identity checks. Required HOME, private PATH, color settings and named gate inputs are supplied explicitly. Caller bypass flags and interpreter search-path overrides are not copied.
   282	
   283	   Every git invocation of the hook and the tracked entrypoints runs with `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `-c core.hooksPath=/dev/null`, `-c core.fsmonitor=false` and `-c protocol.allow=never`. These settings also govern Git subprocesses in their gate and finishing paths. The only on-disk Git configuration read is the anchored checkout's own `.git/config`, which premise 6 protects. Candidate worktree configuration and global or system configuration supply no authority.
   284	
   285	   `tests/unit/test_gh_merge_gate.py::GhMergeGateTest::test_gate_git_ignores_planted_hooks_fsmonitor_and_global_config` has red-then-green evidence. It plants hooks, fsmonitor commands and global configuration with execution sentinels and exercises the hook and entrypoints. Captured Git calls carry every required setting, the worker's planted configuration does not redirect checks or execution, and no sentinel executes.
   286	
   287	   `tests/unit/test_gh_merge_gate.py::GhMergeGateTest::test_gate_resolves_its_binaries_in_the_trusted_root_and_refuses_shims` remains. Fake caller shims record any execution, trusted-root resolution supplies concrete binaries, and shim-only, empty and relative answers ask with valid JSON. The sentinels remain untouched.
   288	
   289	   `tests/unit/test_gh_merge_gate.py::GhMergeGateTest::test_gate_runs_its_identity_checks_under_a_sanitized_environment` is red against a04 and green after the fix. It supplies caller `GIT_DIR`, `GIT_WORK_TREE`, `GIT_CEILING_DIRECTORIES` and PATH values that would redirect the old checks. Neither a forged positive nor a forged negative changes the correct anchored decision.
   290	
   291	   The tracked scripts also capture every additional binary their existing gate or finishing path needs before entering a PR worktree. Their private execution environment contains no caller PATH component and uses no caller-selected shell startup file. Their initial interpreter launch shares item 3's orchestrator-environment premise and its same-UID residual.
   292	
   293	10. `scripts/orchestrator/finish-pr.sh` moves the required finishing glue into the repository and owns PR-body preparation for its `gh pr create` calls. Its tools and subprocesses follow item 9. It uses existing tracked helpers and the tracked merge entrypoint rather than executing untracked glue.
   294	
   295	    The body source is a regular file inside the invoking Git worktree, identified using sanitized absolute git. Validation and copying use the same opened file's bytes. Symlinks, traversal, directories, FIFOs, stdin, external files and cross-worktree sources remain refused.
   296	
   297	    Containment and Git-metadata exclusion compare resolved filesystem identities. Both Git directory and common directory are excluded. The filesystem's case-sensitivity probe governs case-folded comparison, so `.GIT/config`, `.Git/…` and equivalent metadata aliases cannot become published content. Evidence paths used by the merge entrypoint receive the same resolved containment, regular-file, symlink and metadata exclusions.
   298	
   299	    The entrypoint creates the snapshot directory at `<anchored checkout>/.agents/worklog/snapshots/`, which is gitignored and protected by premise 6, with mode `0700`. It writes each snapshot once from the validated bytes. The snapshot is named by those bytes' SHA256 and is outside Git metadata by filesystem identity. Its path and directory are not selected through caller PATH, TMPDIR or a caller-provided destination. The snapshot file is private and regular.
   300	
   301	    Immediately before invoking gh, the script compares the snapshot's SHA256 again with the digest of the validated bytes and refuses a mismatch. The script passes only that snapshot pathname to gh. Gh never opens the caller's `--body-file` pathname. Replacing or deleting the caller's source after validation cannot change the published bytes. Snapshot lifetime includes gh's complete read and cleanup removes only script-owned snapshot state. Premise 6 prevents sandboxed workers from rewriting the snapshot; mode `0700` alone does not exclude the same UID. A same-UID process outside every seat sandbox remains a residual between the final comparison and gh's read.
   302	
   303	    `tests/unit/test_integrate_merge.py::IntegrateMergeTest::test_finish_pr_passes_a_body_snapshot_never_the_caller_path` has red-then-green evidence. It swaps the original source for a synthetic private-target symlink after validation and captures the pathname and bytes received by fake gh. Gh receives the original validated bytes through the digest-named snapshot. The same selector covers safe relative and absolute sources, refused source types, metadata case variants, snapshot permissions and snapshot metadata exclusion. Case-insensitive behavior is exercised deterministically on case-sensitive CI hosts.
   304	
   305	    `tests/unit/test_integrate_merge.py::IntegrateMergeTest::test_finish_pr_reverifies_the_snapshot_before_gh` has red-then-green evidence. It alters the snapshot after its initial write and before the final comparison. A digest mismatch refuses without invoking gh. The unchanged snapshot passes and the captured gh invocation receives that snapshot. This test does not claim to close the same-UID process residual after the last comparison.
   306	
   307	    The finishing path retains the draft flag and the records-only publication check. Draft creation passes `--draft`. A records-only publication requires a non-empty complete comparison whose every `filename` and present `previous_filename` stays under `.orchestration/`. Existing accepted-tip checks for other non-draft publication remain execution requirements.
   308	
   309	    `tests/unit/test_integrate_merge.py::IntegrateMergeTest::test_finish_pr_preserves_draft_and_records_only_publication_controls` has red-then-green evidence. Captured PR creation receives only the script-written validated snapshot and preserves `--draft` for a draft. Records-only publication succeeds for a complete records-only comparison and refuses an empty or incomplete comparison and a renamed source outside `.orchestration/`. A failed publication check produces no gh write.
   310	
   311	    The retained filesystem-identity assertions move from hook body-file tests to these execution and evidence fixtures. Synthetic metadata and synthetic private contents provide the fixtures. No real credential file is opened or published.
   312	
   313	11. `scripts/permission-guard.py` reads its only ledger from `<verified orchestrator_checkout>/.orchestration/decisions.tsv`. It obtains the anchor from deployed `~/.agents/agent-config.yaml`, independently of the candidate revisions, expands it and resolves it with realpath. Premise 6 protects both the deployed anchor and the ledger from worker writes.
   314	
   315	    The invoking checkout is the anchored primary checkout. Its common Git directory resolves to its own `.git`, and its origin and GitHub repository identity identify `mryfmo/dotfiles`. These checks use sanitized Git inputs and trusted-root binaries. Missing, ambiguous or mismatched authority refuses approval.
   316	
   317	    The PR tree's ledger and candidate manifest supply no approval authority. The production `--decisions` exception is removed. There is no external ledger path. Tests create a temporary anchored checkout, name it in the deployed manifest fixture and place the fixture ledger only at that checkout's `.orchestration/decisions.tsv`.
   318	
   319	    `tests/unit/test_permission_guard.py::PermissionGuardTest::test_guard_reads_the_ledger_from_the_anchored_checkout_never_the_pr_tree` retains its red-then-green regression with those anchored fixtures. A matching row present only in the PR tree fails. Candidate-manifest changes and aliases cannot choose another ledger. Missing or mismatched anchors and unrelated checkouts fail. Approval succeeds only with the matching row in the fixture's anchored ledger after identity and write-boundary checks. A same-UID process outside every seat sandbox remains residual.
   320	
   321	    P1-11 owns future CI wiring. That job reads the base commit's ledger rather than the head's ledger. Until it lands, the orchestrator runs the authoritative final-head comparison at acceptance and pastes its output.
   322	
   323	12. `scripts/orchestrator/integrate-merge.sh <task> <head40> <pr>` is the new tracked merge entrypoint. It moves the required behavior from `.agents/worklog/orchestrator-glue/integrate-merge.sh` into the repository, with English shdoc comments and no execution dependency on that untracked file.
   324	
   325	    The entrypoint validates its three arguments, establishes the same deployed anchored primary checkout and enters its own sanitized execution environment. It applies item 3's worker-writable-root refusal to every trusted path and asks before any effect when the boundary check fails. Its absolute trusted-root gh and git are the binaries used for the eventual writes, with item 9's fixed Git configuration controls. Pinning tools only inside the hook does not satisfy this requirement.
   326	
   327	    The entrypoint checks the final-head permission guard from the anchored checkout and uses only its anchored decision ledger. It requires the task's acceptance record and the gate evidence that record names. Evidence remains inside the trusted checkout, outside Git metadata, regular and free of symlink components. Record contents are parsed as data and never sourced or evaluated.
   328	
   329	    The entrypoint invokes the trusted `scripts/require-crit-review.py` through tracked `scripts/orchestrator/orch-gate.sh`, with the final-head feedback sweep, audit and companion verdict, review receipt, Crit data and acceptance record. It passes a verified PR worktree as orch-gate.sh's second argument, matching that helper's existing `<task> <pr-worktree> <pr>` interface. A SHA string is not substituted for that worktree argument. The worktree's HEAD equals the requested head.
   330	
   331	    The gate and validator remain the trusted checkout's copies. A PR-controlled Makefile, gate, interpreter configuration or environment cannot replace them. The task adds no bypass input and does not change the fixed acceptance schema or `scripts/require-crit-review.py`.
   332	
   333	    A `security: true` task requires `.orchestration/validation/<task>-security-<sha7>.md` and its non-empty `.last.md` companion for that head. The final non-blank verdict is `Verdict: correct`. Missing, mismatched or unsuccessful security evidence stops the entrypoint before any merge.
   334	
   335	    Trusted gh checks that the PR is open, ready, targets the repository's valid default branch and carries exactly the head argument. Every required check passes on that head. Malformed responses, missing required checks and failed or pending checks stop execution. The entrypoint performs `gh pr merge --squash --match-head-commit <head> <pr>` only after the gate, security guard and PR checks pass.
   336	
   337	    The entrypoint refuses modified tracked files outside `.orchestration/` in the anchored checkout before merging or changing the local checkout. After the merge, trusted git fetches only `origin/main`, checks out the default branch and fast-forwards the anchored checkout with `--ff-only`. It fetches no task-branch or PR-head ref. The fast-forward preserves local orchestration evidence and recoverable copies on failure. Untracked records are never removed. It performs no reset that discards local records, no local integration of the task branch and no push to main. Required glue behavior stays within the two allowed tracked scripts and reuses existing tracked helpers.
   338	
   339	    `tests/unit/test_integrate_merge.py::IntegrateMergeTest::test_integrate_merge_binds_gh_and_git_to_the_trusted_root` has red-then-green evidence. A shim first on the caller's PATH is never executed. Captured calls prove that identity checks, gate subprocesses, merge and fast-forward use trusted tools and a constructed environment. Its refusal cases prove that a failed gate, missing or incorrect security verdict, unsafe evidence path or failed required check produces no merge.
   340	
   341	    `tests/unit/test_integrate_merge.py::IntegrateMergeTest::test_integrate_merge_refuses_a_head_the_pr_does_not_carry` has red-then-green evidence. A PR-head mismatch produces no merge and no fast-forward. The positive case captures the exact `--match-head-commit` argument, binding a later head change to GitHub's merge refusal.
   342	
   343	    `tests/unit/test_integrate_merge.py::IntegrateMergeTest::test_integrate_merge_fetches_only_origin_main_and_preserves_local_records` has red-then-green evidence. Captured fetch and checkout calls target only the valid default-branch update and every fast-forward uses `--ff-only`. Modified tracked files outside `.orchestration/` refuse without a merge or local update. Dirty tracked orchestration records and untracked records survive successful and failed fast-forwards, with recoverable copies retained on failure.
   344	
   345	## Decision row

The existing branch `tools/permission-guard-gate-a01` continues PR #420 from `911f5202e61a2e46f527fcd9a4eda0041e97410a`. The first push replaces the a04 branch task copy with the byte-identical dispatched a05 copy. Seat a010 keeps its branch, fixes and evidence. The reset creates no second implementation PR. The missed `2026-10-19T03:00Z` deadline remains reported, and the orchestrator owns the new estimate.

The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies with this task's existing branch, the qualifications below, `dotfiles-T133-permission-guard-gate-followup-a01` as the owner of any advisory P2, and `task_copy=<sha256 of .orchestration/dotfiles-T133-permission-guard-gate-a05/task.md>` in RESULT. The orchestrator writes the owner task before assigning its first advisory P2. The six reset defects and retained duplicate-rule defect belong to this task.

Every worker-side fix round, before or after the first RESULT, counts toward INV-6 under C-61. Predecessor counters, the a03 Bot correction, its single CI-repair round, question PONGs, S2 withdrawal and a04 S1 stop remain historical records. They are not recast as approvals.

The worker's own pre-push review is one round at most. A surviving P0/P1 is sent in RESULT as open and stops integration. The worker starts no further private correction-and-review cycle to avoid reporting it. Permitted later rounds remain subject to INV-6 and the inherited completion rule.

No `@codex review` comment is posted. Automatic final-head reviews are observed within the bounded 15-minute window, and absence is recorded as `bot: none`. Required GitHub Actions checks pass before RESULT. Every feedback item carries its proposed disposition. Surviving P0/P1 findings remain open for the operator's decision.

A Codex seat writes evidence at the same relative paths in its worktree and says so in RESULT. Worker review evidence uses the required `-worker-` infix. Agent-side review evidence and its receipt follow the repository's Crit-data rules without opening a browser review or asking the user to review.

RESULT names the final head, base, branch, changed files, Bot findings and dispositions, every open P0/P1, exact test selectors, measured caps, all six new deployable scripts, task-copy SHA256 and evidence paths. The report distinguishes predecessor observations from final-head closure and records the indirect-command-recognition residual, the interpreter-launch premise, the same-UID process residual outside every seat sandbox and the sandbox-exclusion residual owned by D-024-17. The orchestrator copies worktree evidence by absolute path before acceptance review.

This task is `security: true`. Under C-80, a security-profile context reviews this complete a05 task text before dispatch. That review is a dispatch prerequisite rather than a claim made by this draft. The orchestrator also runs the task-level audit and a separate security-profile review on the final implementation head.

The finding-class table includes `decision-not-bound-to-execution` and preserves the predecessor classes `argv-text-mismatch`, `unbound-evidence` and `fail-open-on-error`. A third non-advisory finding of one class stops the artifact for redesign. It never starts another instance-by-instance correction round. The acceptance record retains the required class search and re-plan evidence.

Final-head feedback collection, task-level audit, finding dispositions, acceptance and the integration gate follow Orchestrator Playbook step 10 in its prescribed order. The gate receives `PR_FEEDBACK_EVIDENCE`, `AUDIT_EVIDENCE`, `ACCEPTANCE_EVIDENCE` and the agent review receipt. A changed head receives fresh required evidence. The security review of that final head precedes the gate.

The deployed hook allows only the anchored tracked `integrate-merge.sh` invocation through updated input naming the verified realpath. The script itself runs each gh and git write as a separate command, without shell chaining. Callers submit the entrypoint as one command with its three arguments. The eventual merge is exactly `gh pr merge --squash --match-head-commit <audited head> <pr>`.

Until PR #420 lands, strings carrying `gh pr merge` or `gh pr create` are written with the file-edit tool rather than Bash heredocs or echo. This includes test fixtures, reports and validation prose. The worker does not deploy the new hook or relax its tracked-main identity conditions to bootstrap this PR.

## Checks (pasted by the orchestrator before each send)

```
(pasted at dispatch)
```

Local Bats, live payload execution and live deployment are not performed by this task. Deployment remains unverified until the operator's post-merge checks.{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "model": "claude-fable-5-1",
  "effortLevel": "xhigh",
  "advisorModel": "fable",
  "alwaysThinkingEnabled": true,
  "autoUpdates": false,
  "autoUpdatesChannel": "stable",
  "plansDirectory": "./.agents/worklog/claude",
  "permissions": {
    "allow": [
      "Bash(agmsg-dispatch:*)"
    ],
    "deny": [
      "Bash(sudo:*)",
      "Bash(rm -rf:*)",
      "Read(.env.*)",
      "Read(id_rsa*)",
      "Read(id_ed25519*)",
      "Edit(.env*)",
      "Bash(curl * | sh)",
      "Bash(wget * | sh)",
      "Read(secrets/**)",
      "Read(config/credentials.json)",
      "Bash(gh release:*)",
      "Bash(npm publish:*)",
      "Bash(uv publish:*)",
      "Bash(terraform apply:*)",
      "Bash(kubectl apply:*)"
    ],
    "defaultMode": "auto",
    "ask": [
      "Bash(gh pr merge:*)",
      "Bash(gh pr create:*)",
      "Bash(gh pr comment:*)",
      "Bash(gh pr review:*)",
      "Bash(gh pr close:*)",
      "Bash(gh pr edit:*)",
      "Bash(gh pr update-branch:*)",
      "Bash(gh issue:*)",
      "Bash(gh api -X POST:*)",
      "Bash(gh api --method POST:*)",
      "Bash(gh api -XPOST:*)",
      "Bash(gh api --method=POST:*)",
      "Bash(gh api -X PATCH:*)",
      "Bash(gh api --method PATCH:*)",
      "Bash(gh api -XPATCH:*)",
      "Bash(gh api --method=PATCH:*)",
      "Bash(gh api -X PUT:*)",
      "Bash(gh api --method PUT:*)",
      "Bash(gh api -XPUT:*)",
      "Bash(gh api --method=PUT:*)",
      "Bash(gh api -X DELETE:*)",
      "Bash(gh api --method DELETE:*)",
      "Bash(gh api -XDELETE:*)",
      "Bash(gh api --method=DELETE:*)",
      "Bash(gh api -f:*)",
      "Bash(gh api -F:*)",
      "Bash(gh api --raw-field:*)",
      "Bash(gh api --field:*)",
      "Bash(gh api -f*)",
      "Bash(gh api -F*)",
      "Bash(gh api --raw-field=*)",
      "Bash(gh api --field=*)"
    ]
  },
  "sandbox": {{ if eq .chezmoi.os "darwin" }}
{
  "enabled": true,
  "failIfUnavailable": false,
13:#   The Claude sandbox allowWrite list is rendered from the same entries.
34:    claude: { model: claude-opus-5-5, effort: xhigh, advisor: fable }
37:      model_reasoning_effort: xhigh
42:    claude: { model: claude-fable-5-1, effort: xhigh }
43:    codex: { model: gpt-6.1-sol, model_reasoning_effort: xhigh }
45:    claude: { model: claude-fable-5-1, effort: xhigh, advisor: fable }
48:      model_reasoning_effort: xhigh
52:    claude: { model: claude-fable-5, effort: high }
56:      model_reasoning_effort: high
60:    # at xhigh reasoning effort (operator pin 2026-10-09, T115).
61:    claude: { model: claude-fable-5-1, effort: high }
64:      model_reasoning_effort: xhigh
71:worker_kind: claude
85:worker_worktree: .claude/worktrees/worker-c
124:      PATH: '{{ .chezmoi.homeDir }}/.local/share/mise/installs/node/lts/bin:{{ .chezmoi.homeDir }}/.local/share/mise/shims:{{ .chezmoi.homeDir }}/.local/bin:{{ .chezmoi.homeDir }}/.local/bin/common:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin'
223:      - Bash(gh release:*)
230:      - Bash(gh pr merge:*)
231:      - Bash(gh pr create:*)
232:      - Bash(gh pr comment:*)
233:      - Bash(gh pr review:*)
234:      - Bash(gh pr close:*)
235:      - Bash(gh pr edit:*)
236:      - Bash(gh pr update-branch:*)
237:      - Bash(gh issue:*)
238:      - Bash(gh api -X POST:*)
239:      - Bash(gh api --method POST:*)
240:      - Bash(gh api -XPOST:*)
241:      - Bash(gh api --method=POST:*)
242:      - Bash(gh api -X PATCH:*)
243:      - Bash(gh api --method PATCH:*)
244:      - Bash(gh api -XPATCH:*)
245:      - Bash(gh api --method=PATCH:*)
246:      - Bash(gh api -X PUT:*)
247:      - Bash(gh api --method PUT:*)
248:      - Bash(gh api -XPUT:*)
249:      - Bash(gh api --method=PUT:*)
250:      - Bash(gh api -X DELETE:*)
251:      - Bash(gh api --method DELETE:*)
252:      - Bash(gh api -XDELETE:*)
253:      - Bash(gh api --method=DELETE:*)
254:      - Bash(gh api -f:*)
255:      - Bash(gh api -F:*)
256:      - Bash(gh api --raw-field:*)
257:      - Bash(gh api --field:*)
258:      - Bash(gh api -f*)
259:      - Bash(gh api -F*)
260:      - Bash(gh api --raw-field=*)
261:      - Bash(gh api --field=*)
269:  # filesystem.allowWrite. The generator renders allowWrite from
285:    excludedCommands:
291:    # Linux blocks gh's keyring and herdr-agents -> actas-claim.sh socket calls;
294:      - gh *
298:      # Rendered into sandbox.filesystem.allowWrite after the Codex writable
304:        - ~/.local/state/mise
307:        - ~/Library/Caches/mise
393:# minimum_release_age in home/dot_mise/config.toml). Only a component whose
397:# pins here only, through generate-agent-configs.py --set-asset. `pin: unknown`
400:  mise:
402:    upstream: jdx/mise
405:    attestation: when-gh-authenticated
407:    note: the newest cooled-down release installs only when gpg and gpgv (SHASUMS256.asc checked against the release key with gpg_fingerprint, fetched from keys.openpgp.org as mise documents) or an authenticated gh (the release attestation) can verify it before it runs; otherwise the fallback release does, and mise self-update moves it forward afterwards.
415:      reason: a host without gpg and without an authenticated gh (a fresh macOS) can check neither the release key's signature nor the release attestation before mise runs, and SHASUMS256.txt comes from the same release; so it bootstraps this reviewed release, SHASUMS256.txt kept as a second check.
416:    install_path: ~/.local/bin/mise
417:    installer: install/common/mise.sh
419:      file: install/common/mise.sh

web search: 
web search: site.mise.jdx.dev shims current directory config ...
**Limiting output for efficiency**
codex
The inherited §5.14 contract addresses Git environment sanitization and path aliases, but the task still calls the sweep identity “closed” using a test that compares copies before validation; it does not test replacement before the gate reads the file. I also found a conflict between retaining the existing review worktree and §5.14’s rule rejecting trusted paths under `.claude/worktrees/`.

exec
/bin/zsh -lc "sed -n '1,45p' home/.chezmoitemplates/claude-settings-managed.json; rg -n 'excludedCommands|worker_kind:|worker_worktree:|allowWrite|mise' home/dot_agents/agent-config.yaml | head -45; rg -n '"'^def git|subprocess|PR_FEEDBACK_EVIDENCE|read_text'"' scripts/require-crit-review.py | head -45; rg -n '5\\.14|committed|orch-gate.sh|UV_CACHE' .orchestration/tasks/dotfiles-T133-permission-guard-gate-a05.md" in ~/Workspace/dotfiles
 succeeded in 40ms:
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "model": "claude-fable-5-1",
  "effortLevel": "xhigh",
  "advisorModel": "fable",
  "alwaysThinkingEnabled": true,
  "autoUpdates": false,
  "autoUpdatesChannel": "stable",
  "plansDirectory": "./.agents/worklog/claude",
  "permissions": {
    "allow": [
      "Bash(agmsg-dispatch:*)"
    ],
    "deny": [
      "Bash(sudo:*)",
      "Bash(rm -rf:*)",
      "Read(.env.*)",
      "Read(id_rsa*)",
      "Read(id_ed25519*)",
      "Edit(.env*)",
      "Bash(curl * | sh)",
      "Bash(wget * | sh)",
      "Read(secrets/**)",
      "Read(config/credentials.json)",
      "Bash(gh release:*)",
      "Bash(npm publish:*)",
      "Bash(uv publish:*)",
      "Bash(terraform apply:*)",
      "Bash(kubectl apply:*)"
    ],
    "defaultMode": "auto",
    "ask": [
      "Bash(gh pr merge:*)",
      "Bash(gh pr create:*)",
      "Bash(gh pr comment:*)",
      "Bash(gh pr review:*)",
      "Bash(gh pr close:*)",
      "Bash(gh pr edit:*)",
      "Bash(gh pr update-branch:*)",
      "Bash(gh issue:*)",
      "Bash(gh api -X POST:*)",
      "Bash(gh api --method POST:*)",
      "Bash(gh api -XPOST:*)",
      "Bash(gh api --method=POST:*)",
      "Bash(gh api -X PATCH:*)",
13:#   The Claude sandbox allowWrite list is rendered from the same entries.
71:worker_kind: claude
85:worker_worktree: .claude/worktrees/worker-c
124:      PATH: '{{ .chezmoi.homeDir }}/.local/share/mise/installs/node/lts/bin:{{ .chezmoi.homeDir }}/.local/share/mise/shims:{{ .chezmoi.homeDir }}/.local/bin:{{ .chezmoi.homeDir }}/.local/bin/common:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin'
269:  # filesystem.allowWrite. The generator renders allowWrite from
285:    excludedCommands:
298:      # Rendered into sandbox.filesystem.allowWrite after the Codex writable
304:        - ~/.local/state/mise
307:        - ~/Library/Caches/mise
393:# minimum_release_age in home/dot_mise/config.toml). Only a component whose
400:  mise:
402:    upstream: jdx/mise
407:    note: the newest cooled-down release installs only when gpg and gpgv (SHASUMS256.asc checked against the release key with gpg_fingerprint, fetched from keys.openpgp.org as mise documents) or an authenticated gh (the release attestation) can verify it before it runs; otherwise the fallback release does, and mise self-update moves it forward afterwards.
415:      reason: a host without gpg and without an authenticated gh (a fresh macOS) can check neither the release key's signature nor the release attestation before mise runs, and SHASUMS256.txt comes from the same release; so it bootstraps this reviewed release, SHASUMS256.txt kept as a second check.
416:    install_path: ~/.local/bin/mise
417:    installer: install/common/mise.sh
419:      file: install/common/mise.sh
482:    note: chezmoi signs its checksums with cosign only, which a fresh host cannot run; the newest cooled-down release installs only when an authenticated gh can check its release attestation before it runs, otherwise the fallback release does, and mise's own chezmoi takes over after the bootstrap.
12:import subprocess
24:PR_FEEDBACK_ENV = "PR_FEEDBACK_EVIDENCE"
138:def run_git(args: list[str], root: Path | None = None) -> subprocess.CompletedProcess[str]:
139:    return subprocess.run(
144:        stdout=subprocess.PIPE,
145:        stderr=subprocess.PIPE,
149:def git_root() -> Path:
306:    text = path.read_text()
362:        data = json.loads(path.read_text())
427:        data = json.loads(path.read_text())
523:        repository = subprocess.run(
539:        result = subprocess.run(
614:        result = subprocess.run(
619:            stdout=subprocess.PIPE,
620:            stderr=subprocess.PIPE,
625:        collected = json.loads(collected_path.read_text())
683:    if not source.is_file() or not source.read_text().strip():
696:    text = source.read_text()
752:    lines = path.read_text().split("\n")
903:    return source.read_text(), None
960:    The same match as `grep -rl 'classes:.*<class>'`, without a subprocess; the gate reads its result, never
969:            lines = path.read_text(errors="replace").splitlines()
1005:        help="also review committed changes in <base>...HEAD and require PR_FEEDBACK_EVIDENCE and ACCEPTANCE_EVIDENCE, plus AUDIT_EVIDENCE when review is required (PR integration)",
1033:    # pr_feedback_errors already validated PR_FEEDBACK_EVIDENCE's location and -pr-feedback.json suffix.
1037:    feedback_document = json.loads((root / feedback).read_text()) if feedback else {}
116:    disposition: "residual: no forced removal is planned; the existing dirty-worktree rule applies and the acceptance record identifies any discarded uncommitted state."
261:   Uncommitted source identities are recorded with content SHA256 values before red runs and after fixes. Missing intermediate identities in predecessor reports remain evidence limitations. Historical suites and probe counts do not close new regressions by themselves.
277:9. Trusted-root binary resolution remains a requirement before hook processing and becomes an execution requirement of both tracked orchestration scripts. The resolver runs from the deployed anchored root in a constructed trusted environment. It follows `scripts/orchestrator/orch-gate.sh`'s private-directory-of-links precedent without inheriting the caller's PATH or tool-manager configuration.
329:    The entrypoint invokes the trusted `scripts/require-crit-review.py` through tracked `scripts/orchestrator/orch-gate.sh`, with the final-head feedback sweep, audit and companion verdict, review receipt, Crit data and acceptance record. It passes a verified PR worktree as orch-gate.sh's second argument, matching that helper's existing `<task> <pr-worktree> <pr>` interface. A SHA string is not substituted for that worktree argument. The worktree's HEAD equals the requested head.

web search: 
web search: https://code.claude.com/docs/en/sandboxing
**Analyzing git diff and config vulnerabilities**
**Examining threat table inconsistencies and race conditions**

I’m identifying gaps in committed-ledger cache locks and trusted path rows, noting race conditions in closure checks and potential spoofing in app check-run identities. Some findings may overlap, so I’m weighing if multiple race findings are redundant and reviewing risks from CI workflow naming collisions.
exec
/bin/zsh -lc "sed -n '138,154p' scripts/require-crit-review.py; sed -n '275,311p' home/dot_agents/agent-config.yaml; rg -n 'integration_id|app_id|check_suite' scripts/orchestrator/ruleset-request.sh scripts/orchestrator/ruleset-verify.sh tests/unit/test_ruleset_scripts.py; git ls-files scripts/orchestrator/dispositions.py tests/unit/test_dispositions.py; git rev-parse origin/main" in ~/Workspace/dotfiles
 succeeded in 44ms:
def run_git(args: list[str], root: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=root,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def git_root() -> Path:
    result = run_git(["rev-parse", "--show-toplevel"])
    if result.returncode != 0:
        print("Review guard skipped: not inside a git repository.")
        raise SystemExit(0)
    return Path(result.stdout.strip())
  # create user namespaces.
  sandbox:
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
rg: scripts/orchestrator/ruleset-request.sh: No such file or directory (os error 2)
rg: scripts/orchestrator/ruleset-verify.sh: No such file or directory (os error 2)
rg: tests/unit/test_ruleset_scripts.py: No such file or directory (os error 2)
212efe972a14d4d5f209bf739c1b8008471ba775

web search: 
web search: https://cli.github.com/manual/gh_alias_set
**Ensuring final verdict clarity**
**Evaluating Git wrapper limitations**
**Analyzing environment overrides**
**Examining symlink attack risks**
exec
/bin/zsh -lc "nl -ba .orchestration/tasks/dotfiles-T133-dispositions-a02.md | sed -n '145,191p'; nl -ba .orchestration/tasks/dotfiles-T133-dispositions-a02.md | sed -n '273,281p'; sed -n '70,104p' .orchestration/tasks/dotfiles-T133-dispositions-a01.md; shasum -a 256 .orchestration/tasks/dotfiles-T133-dispositions-a02.md" in ~/Workspace/dotfiles
 succeeded in 37ms:
   145	   The `diff:` form uses the tool-fixed `<thread commit>..<audited head>` range. A caller-supplied range is accepted only when its endpoints equal those fixed commits, the thread's hunk is unchanged over that range and the disposition names why the path is unreachable. The reason retains the existing minimum of 20 characters. The result is recorded as `claim-recorded`. A range such as `<head>..<head>` is refused. Until programs item (16)'s second opinion confirms it, `--require-refutation` refuses a P0/P1 not-applicable resting on `diff:` alone.
   146	
   147	   `--require-refutation` prints one line per not-applicable disposition with a missing, failed or not-yet-confirmed form and exits 1. The legacy `evidence=<command>` form is reported as `legacy-evidence` and fails only under `--require-refutation`. Exit 0 means the selected mode completed, exit 1 means a required refutation failed, and exit 2 means usage failure or a hold such as an unreadable sweep or a required missing thread commit. Missing check data fails the refutation and never authorizes local head-code execution.
   148	
   149	2. `scripts/orchestrator/orch-gate.sh` enters a constructed `env -i` environment before any Git discovery or checkout.
   150	
   151	   The trusted root is established from the wrapper's physical source location. Absolute tools are resolved in that root, and the existing private links directory supplies the private PATH. The interpreter is resolved in the trusted root before the review worktree is entered and is invoked directly with isolated Python options.
   152	
   153	   The environment sets `GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL=/dev/null`. Every Git call carries `-c core.hooksPath=/dev/null` and `-c core.fsmonitor=false`, including discovery, authentication, data reads, checkout, cleanup and restoration. Inherited `GIT_DIR`, `GIT_WORK_TREE`, `GIT_CONFIG_GLOBAL` and other caller Git overrides do not reach discovery. The existing removal and worktree-restoration trap remains effective on failure.
   154	
   155	   The wrapper authenticates `scripts/orchestrator/dispositions.py` as it authenticates the gate and validator. The executed file is the trusted checkout's regular tracked file, and its SHA256 equals the SHA256 of `git show origin/main:scripts/orchestrator/dispositions.py`. Missing, changed, untracked or substituted verifier bytes refuse before execution. No verifier is loaded from the PR head or review checkout.
   156	
   157	   Until PR #419 merges, the new verifier is absent from trusted main. The new gate step is exercised only by worker tests with a fixture main containing its authenticated verifier. Integration of PR #419 uses the existing trusted main gate. The candidate wrapper and verifier are never run on the orchestrator's host to bootstrap their own integration.
   158	
   159	   After checkout and evidence preparation, the wrapper retains one dispositions re-validation step immediately before the gate. It validates the review-worktree sweep at the same path and working directory passed to `scripts/require-crit-review.py` through `PR_FEEDBACK_EVIDENCE`. It records that file's SHA256 in its output. It never validates the trusted-root source copy while the gate reads another copy.
   160	
   161	   The orchestrator's prefetched checks are recorded at `.orchestration/<task>/checks.json` and supplied through `--checks` when a `test:` form needs them. Production evidence comes from the orchestrator's own API reads. Worker-authored check fixtures do not become production evidence. The wrapper passes the protected data to the authenticated verifier and does not accept cached `refutation.ok` values as authority.
   162	
   163	   Under `DISPOSITIONS_REQUIRE_REFUTATION=1`, re-validation adds `--require-refutation`, and failure refuses with wrapper exit 2 and the tool's diagnostic lines. Without the variable, the same step reports verification failures without enforcing them. A usage failure, hold or verifier-authentication failure remains a wrapper refusal. The PR number and head come from the wrapper's existing arguments.
   164	
   165	   The step executes no head code and no test selector.
   166	
   167	3. `tests/unit/test_dispositions.py` retains temporary-repository coverage for changed-hunk proposals, untouched-line demands, all three refutation forms, legacy evidence and holds.
   168	
   169	   `test_dispositions_proposes_fixed_for_a_changed_hunk_and_demands_not_applicable_otherwise` checks the actual fixing commit, an untouched line and unchanged existing dispositions. The review-body finding and literal-pathspec regressions remain.
   170	
   171	   `test_require_refutation_fails_without_a_form_and_accepts_each_of_the_three` uses head-tree and prefetched-check fixtures for `test:`, a `file://` page for present and absent source quotes, and fixed-range diff fixtures for accepted and refused claims. It checks the recorded source hash, reporting mode and enforcement mode.
   172	
   173	   `test_dispositions_holds_on_an_unreadable_sweep_or_a_missing_commit` retains exit-2 coverage for malformed input and an unavailable commit needed by a located in-diff thread.
   174	
   175	   `test_diff_refutation_range_is_fixed_to_thread_commit_and_head_and_is_a_claim` retains arbitrary-range refusal, the unreachable-path reason and the P0/P1 second-opinion restriction.
   176	
   177	   `test_dispositions_verifies_test_refutations_from_head_tree_and_required_checks` checks an exact present function with successful required checks for P2 and P3. It separately checks missing paths, absent functions, wrong classes, malformed check data, missing required contexts, incomplete pagination, wrong heads and pending or unsuccessful latest runs. An older successful run never overrides a newer failed or pending run. P0/P1 produce claims and fail `--require-refutation`. Missing priority does not acquire P2/P3 treatment.
   178	
   179	   Head-test fixtures contain import and execution markers. Verification creates neither marker. The test forbids log reads, artifact commands and selector execution. Assertions describe static presence and CI conclusions without claiming a per-selector result.
   180	
   181	4. `tests/unit/test_orch_gate_path.py` retains its existing fake-binary style and private-PATH, shim-refusal, cleanup and restoration coverage.
   182	
   183	   `test_orch_gate_revalidates_the_dispositions_before_the_gate` checks that enforcement refuses before the fake gate runs when current verification fails, including when saved verification claims success. Reporting mode prints the failed verification and permits the fake gate. The audited head reaches the verifier, and no local head-test marker is created.
   184	
   185	   `test_orch_gate_sanitizes_the_environment_before_git_discovery` supplies inherited `GIT_DIR`, `GIT_WORK_TREE`, `GIT_CONFIG_GLOBAL` and Git configuration overrides pointing to a decoy repository. The gate selects the intended trusted root and PR worktree. The recorded first Git invocation already has the sanitized environment and required configuration arguments. Checkout and restoration retain those controls.
   186	
   187	   `test_orch_gate_runs_dispositions_only_when_it_matches_main` supplies verifier bytes in fixture main. Matching trusted-checkout bytes execute. Modified bytes, a missing main version and a substituted file refuse before verifier or gate execution. A matching file in the head tree cannot authorize different trusted-checkout bytes.
   188	
   189	   `test_orch_gate_validates_the_copy_it_reads` makes the source sweep and copied review sweep differ. The verifier and fake gate record the same sweep path and bytes, and the wrapper's reported SHA256 matches those bytes. A valid source copy cannot authorize an invalid review copy. Enforcement refuses before the fake gate runs.
   190	
   191	   Fixture main is used for every case exercising the new step before merge. Fixture lines count against the test cap.
   273	Final-head feedback collection, task-level audit, finding dispositions, acceptance and the integration gate follow Orchestrator Playbook step 10 in its prescribed order. The gate receives `PR_FEEDBACK_EVIDENCE`, `AUDIT_EVIDENCE`, `ACCEPTANCE_EVIDENCE` and the agent review receipt. A changed head receives fresh required evidence. Integration of this PR uses the existing trusted main gate; the new step remains confined to fixture-main tests until merge. Merge uses `gh pr merge --squash --match-head-commit <audited head>`.
   274	
   275	Commands for gh and Git writes run individually, without shell chaining or a wrapper combining writes. A classifier denial produces a blocked PONG naming the command and reason. Until P1-14 lands, strings containing `gh pr merge` or `gh pr create` are written with the file-edit tool rather than a Bash heredoc or `echo`.
   276	
   277	## Sequencing note (orchestrator, 2026-10-19T03:0xZ)
   278	
   279	This task edits `scripts/orchestrator/orch-gate.sh`, which `dotfiles-T133-permission-guard-gate-a05` also edits (the sanitized environment of design 5.14 item 2 and the private uv cache of item 9). The a05 change lands first; this task starts after PR #420 merges, rebases onto that main, and its orch-gate.sh item builds on the sanitized environment a05 provides instead of adding a second one. Design 5.14 applies to this task by reference (D-024-18); the threat table's environment, trusted-path and committed-ledger rows are read against it.
   280	
   281	## Checks (pasted by the orchestrator before each send)
# AGMSG-TASK dotfiles-T133-dispositions-a01 — disposition candidates and refutation forms (plan 024 P1-10, programs item (5); the item (16) second opinion is a later task)

Written 2026-10-18 by the orchestrator seat from plan 024 (`024-todo.md` row P1-10, `024-design-programs.md` item (5), `024-design-quality.md` 5.13 refutation forms). Today every Bot thread's disposition is typed by hand into an extra TSV; this tool proposes `fixed:<commit>` from git and refuses an empty not-applicable. Seat: a Claude seat.

## Goal

For a PR head, every review-comment item of the sweep gets a machine proposal: `fixed:<commit>` when a commit between the thread's commit and the head touches the thread's hunk, otherwise a demand for `not-applicable:` with one of the three refutation forms. The gate wrapper re-validates the saved dispositions in that mode before the gate runs.

## Files

1. `scripts/orchestrator/dispositions.py <pr> <head> --feedback <sweep.json> [--out <json>] [--require-refutation] [--commits <json>]` (new, Python, `python -I`, standard library only, shdoc-style module docstring in English). For each item with `source` `review_comment` (and each badged `review` item that names a path and line): the thread's commit is the item's `original_commit_id` when the sweep carries it, else `--commits <json>` (a map url → commit, the test and cache form), else `gh api repos/{owner}/{repo}/pulls/comments/<id> --jq .original_commit_id` (gh resolved from PATH; a failure is a hold line, never a guess). `git diff <commit>..<head> -- <path>` is parsed for a hunk whose new-side or old-side range covers `line`; when one exists, `git log --format=%H <commit>..<head> -- <path>` is walked to the newest commit whose diff against its parent touches that range, and the proposal is `fixed:<that commit>`; otherwise the proposal is `not-applicable:` with an empty reason to be filled. The output JSON (`--out`, default stdout) is the sweep with `proposal` added per item and the existing `disposition` untouched. Refutation forms for a not-applicable disposition (5.13): `test:<selector>` (the selector runs as `uv run --no-project python -m unittest <selector>` in the checkout, and the form is accepted only on exit 0, with the run's last line recorded), `source:{url, fetched_at, quote}` (the URL is fetched, the quote must occur in the page text, the page's sha256 is recorded; `file://` URLs are accepted for tests), `diff:<range>` (accepted only when `git diff <range> -- <path>` has no hunk covering the line). `--require-refutation` exits 1 and prints one line per not-applicable disposition that carries none of the three forms or whose form fails verification; the `evidence=<command>` form used by today's records is reported as `legacy-evidence` and counts as a failure only under `--require-refutation`. Exit codes: 0 ok, 1 a disposition failed the requirement, 2 usage or a hold (gh failure, unreadable sweep).
2. `scripts/orchestrator/orch-gate.sh`: before the gate runs, one step `dispositions.py <pr> <head> --feedback "${sweep}" --require-refutation` under `DISPOSITIONS_REQUIRE_REFUTATION=1` refuses with exit 2 and the tool's lines; without the variable the same command runs without `--require-refutation` and its lines are printed as a report (the records of today's PRs still carry the legacy form; the flip is a decision row). The PR number and head come from the wrapper's existing arguments; the step uses the wrapper's private PATH.
3. Tests `tests/unit/test_dispositions.py`: `test_dispositions_proposes_fixed_for_a_changed_hunk_and_demands_not_applicable_otherwise` (a temporary repository: a thread commit, a fix commit touching the line, a head; the proposal names the fix commit; a second thread on an untouched line gets the not-applicable demand; `--commits` supplies the commits), `test_require_refutation_fails_without_a_form_and_accepts_each_of_the_three` (the legacy `evidence=` form fails; `test:` with a stub selector that passes is accepted and one that fails is refused; `source:` with a `file://` page containing the quote is accepted and a missing quote refused; `diff:` with an untouched range is accepted and a touching range refused), `test_dispositions_holds_on_an_unreadable_sweep_or_a_missing_commit` (exit 2 with the reason). `tests/unit/test_orch_gate_path.py::test_orch_gate_revalidates_the_dispositions_before_the_gate` (in the module's fake-binary style: with `DISPOSITIONS_REQUIRE_REFUTATION=1` and a sweep whose not-applicable lacks a form, the wrapper exits 2 and the fake gate records no run; without the variable the fake gate runs and the report line is printed). Fixture lines count against the test cap.
4. `report.md` states the proposal rule, the three forms and their verification, the legacy-evidence transition (how many of today's records carry it: `grep -l "evidence=" .orchestration/validation/*-pr-feedback.json | wc -l`, pasted), and the later task for item (16) (`audit-pool.sh --second-opinion`, after PR #410).

## Out of scope

`audit-pool.sh --second-opinion` (item (16), after PR #410 merges), `scripts/require-crit-review.py` (its validators are imported or re-implemented read-only, not edited), `fill_sweep.py` and `pr-feedback.py` (the sweep stays as it is), the chain scripts (they call the gate wrapper), flipping `DISPOSITIONS_REQUIRE_REFUTATION` (a decision row).

## Check

`make format`, `uv run python -m unittest tests.unit.test_dispositions tests.unit.test_orch_gate_path -v` green, `shellcheck` and `shfmt -d` on orch-gate.sh clean, `uv run --no-project python -I scripts/orchestrator/dispositions.py 409 4fe243803971bd5ba8ab45f8ede5cfb4dd37f719 --feedback .orchestration/validation/dotfiles-T133-ci-efficiency-a02-pr-feedback.json` run once with its output pasted (a real sweep; `gh` resolves the thread commits), all pasted in `.orchestration/dotfiles-T133-dispositions-a01/validation.md`, with `git diff --numstat origin/main...HEAD`: at most 350 changed lines outside `tests/` and `.orchestration/`, 450 under `tests/`.

## Completion

One PR from a fresh branch off `origin/main`. The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies as written, with `dotfiles-T133-dispositions-followup-a01` as the owner of any advisory P2 (written by the orchestrator when the first one appears) and `task_copy=<sha256 of .orchestration/dotfiles-T133-dispositions-a01/task.md>` in the RESULT; the RESULT also carries `precheck=` when `scripts/orchestrator/result-precheck.sh` has merged (PR #411), else `precheck=pending-411`. `security: true`: the orchestrator runs the task-level audit and the security-profile review on the final head. No `@codex review` comment; single commands for every gh and git write; a classifier denial is a blocked PONG. Until P1-14 lands, any string containing the words gh pr merge or gh pr create is written with the file-edit tool, never in a Bash heredoc or echo.

## Amendment 1 (round 1, 2026-10-18T21:0xZ): the three refutation forms after the audit of fa47987

The task-level audit of fa47987 (`Verdict: incorrect`, two P1) found item 1's forms unsound, and item 1 changes as follows; everything else stands. (a) `test:<selector>`: the form is verified against the accepted head's CI, never by a local run at the gate (a run on the trusted checkout tests pre-regression code and cannot run a test the PR introduces; a run of the head's code on the orchestrator's host crosses the trust boundary): dispositions.py reads the log of the head's required unit-test check (`gh run view <run id> --log` for `test (ubuntu-24.04, client)` on the accepted head, or a `--ci-log <file>` for tests) and accepts the form only when the selector appears there with `ok`; a selector absent from the log, skipped, or present only as `skipped=` is refused. (b) `diff:<range>`: the caller does not choose the range; the tool fixes it to `<thread commit>..<accepted head>` and accepts the form only when a caller-given range equals that, when the thread's hunk is unchanged over it, and when the disposition text names the reason the path is unreachable; the form is then recorded as `claim-recorded`, and for a P0 or P1 finding a `claim-recorded` not-applicable needs the second opinion of programs item (16) before the gate accepts it (until item (16) lands, `--require-refutation` refuses a P0 or P1 not-applicable that rests on `diff:` alone). A range such as `<head>..<head>` is refused. (c) upstream-only changes: when the only commits touching the thread's hunk between the thread commit and the head are merges of the base (no commit of the branch), the proposal is the `not-applicable:` demand, not a hold. (d) `test:` acceptance requires at least one executed, non-skipped test; `OK (skipped=1)` alone is refused. The real run of item 4 is redone with `gh` fetching the thread commits as one command each and the helper running inside the seat's sandbox with `--commits` (Worker Playbook step 4 exempts `gh`, not its caller). This is INV-6's first amendment (C-61); the counters are pasted below.

## Checks (pasted by the orchestrator before each send)

```
dotfiles-T133-dispositions-a01.md: OK
ea3413a09bc0aebb4f363fd267f70a3dc0c2e154c972ea88534b035c5f5460d1  .orchestration/tasks/dotfiles-T133-dispositions-a02.md

**Finalizing with design considerations**
**Concluding security and design review**
codex
- [P1] High confidence [.orchestration/tasks/dotfiles-T133-dispositions-a02.md:50](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-dispositions-a02.md:50) The worker-write residual assumes protection that §5.14 and the cited acceptance record explicitly deny for Claude seats: file tools, hooks and MCP processes can modify the trusted checkout and evidence before P1-15; committed-ledger reads do not protect these executable and evidence paths. [Sandbox scope](https://code.claude.com/docs/en/sandboxing#what-runs-outside-the-sandbox).

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-dispositions-a02.md:48](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-dispositions-a02.md:48) Pending D-024-17 supplies no present mitigation: retained unsandboxed worker `gh` commands still resolve through mise shims and worker-controlled configuration, permitting execution outside the boundary protecting the verifier and prefetched evidence; P1-15 is neither implemented here nor a dispatch dependency. [Shim resolution](https://mise.jdx.dev/dev-tools/shims.html).

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-dispositions-a02.md:189](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-dispositions-a02.md:189) The sweep-identity “closed” test compares copies before validation, but never replaces the validated file before the unchanged gate reopens it; identical pathnames and a printed digest cannot bind consumed bytes, and §5.14’s snapshot protection still depends on the false worker-write premise.

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-dispositions-a02.md:187](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-dispositions-a02.md:187) The verifier-identity “closed” test does not require replacement after authentication but before Python opens the script; a SHA256 comparison followed by execution through a mutable pathname cannot establish the claimed closure against the same-user workers described in the cited records.

- [P1] Medium confidence [.orchestration/tasks/dotfiles-T133-dispositions-a02.md:153](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-dispositions-a02.md:153) Wrapper-local `git -c` arguments do not propagate to the unchanged gate’s bare Git subprocesses; the specified binary-link PATH and two configuration environment variables provide no mechanism for enforcing hooks/fsmonitor settings there, while the named test checks discovery, checkout and restoration rather than actual gate descendants.

- [P2] High confidence [.orchestration/tasks/dotfiles-T133-dispositions-a02.md:279](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-dispositions-a02.md:279) Applying §5.14’s rejection of trusted paths beneath `.claude/worktrees/` conflicts with retaining `.claude/worktrees/orchestrator-review` as the trusted sweep-consumption location; resolving symlinks and case aliases does not resolve this policy contradiction, so the design must distinguish the protected review worktree or relocate it.

- [P2] High confidence [.orchestration/tasks/dotfiles-T133-dispositions-a02.md:279](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-dispositions-a02.md:279) The claimed trusted-path and committed-ledger threat rows are absent, as are explicit dispositions for §5.14’s private-cache and output/lock-identity controls; incorporation by reference does not satisfy its requirement for one threat row per contract item.

📝 まとめ: Read-only review completed with seven findings for orchestrator disposition; no files changed.

Not checked: implementation tests or live enforcement; the cited earlier a02 review’s `.last.md` was unavailable. Execution and evidence integrity remain unestablished.
Verdict: incorrect
hook: Stop
hook: Stop Completed
tokens used
96,923
- [P1] High confidence [.orchestration/tasks/dotfiles-T133-dispositions-a02.md:50](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-dispositions-a02.md:50) The worker-write residual assumes protection that §5.14 and the cited acceptance record explicitly deny for Claude seats: file tools, hooks and MCP processes can modify the trusted checkout and evidence before P1-15; committed-ledger reads do not protect these executable and evidence paths. [Sandbox scope](https://code.claude.com/docs/en/sandboxing#what-runs-outside-the-sandbox).

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-dispositions-a02.md:48](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-dispositions-a02.md:48) Pending D-024-17 supplies no present mitigation: retained unsandboxed worker `gh` commands still resolve through mise shims and worker-controlled configuration, permitting execution outside the boundary protecting the verifier and prefetched evidence; P1-15 is neither implemented here nor a dispatch dependency. [Shim resolution](https://mise.jdx.dev/dev-tools/shims.html).

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-dispositions-a02.md:189](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-dispositions-a02.md:189) The sweep-identity “closed” test compares copies before validation, but never replaces the validated file before the unchanged gate reopens it; identical pathnames and a printed digest cannot bind consumed bytes, and §5.14’s snapshot protection still depends on the false worker-write premise.

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-dispositions-a02.md:187](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-dispositions-a02.md:187) The verifier-identity “closed” test does not require replacement after authentication but before Python opens the script; a SHA256 comparison followed by execution through a mutable pathname cannot establish the claimed closure against the same-user workers described in the cited records.

- [P1] Medium confidence [.orchestration/tasks/dotfiles-T133-dispositions-a02.md:153](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-dispositions-a02.md:153) Wrapper-local `git -c` arguments do not propagate to the unchanged gate’s bare Git subprocesses; the specified binary-link PATH and two configuration environment variables provide no mechanism for enforcing hooks/fsmonitor settings there, while the named test checks discovery, checkout and restoration rather than actual gate descendants.

- [P2] High confidence [.orchestration/tasks/dotfiles-T133-dispositions-a02.md:279](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-dispositions-a02.md:279) Applying §5.14’s rejection of trusted paths beneath `.claude/worktrees/` conflicts with retaining `.claude/worktrees/orchestrator-review` as the trusted sweep-consumption location; resolving symlinks and case aliases does not resolve this policy contradiction, so the design must distinguish the protected review worktree or relocate it.

- [P2] High confidence [.orchestration/tasks/dotfiles-T133-dispositions-a02.md:279](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-dispositions-a02.md:279) The claimed trusted-path and committed-ledger threat rows are absent, as are explicit dispositions for §5.14’s private-cache and output/lock-identity controls; incorporation by reference does not satisfy its requirement for one threat row per contract item.

📝 まとめ: Read-only review completed with seven findings for orchestrator disposition; no files changed.

Not checked: implementation tests or live enforcement; the cited earlier a02 review’s `.last.md` was unavailable. Execution and evidence integrity remain unestablished.
Verdict: incorrect
