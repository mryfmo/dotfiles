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
session id: 01a152e8-0c52-7c92-b66f-883bc666d709
--------
user
Pre-dispatch security review (read-only, security profile) of the task text .orchestration/tasks/dotfiles-T133-codex-worker-network-a01.md and its threat_table, before any implementation exists. Judge the design the text states: can the controls it names bind what actually executes on this host (mise shims first on PATH, same-user worker processes, gh outside the sandbox on Linux, symlinks and case-insensitive filesystems, inherited GIT_* environment)? Check every threat row: a closed row whose named test cannot close it, a residual row whose control does not mitigate the risk, a missing row for a file or non-path control, and any gap of the class decision-not-bound-to-execution (a decision made on text or on a validated copy while the execution resolves binaries, files or ledgers from an attacker-influenced place). Read the related acceptance records and reviews the text cites for context. Report each finding as [P0-P3] <confidence> <file:line> <one line>; findings are input for the orchestrator, who decides. End with exactly one line: Verdict: correct or Verdict: incorrect.
warning: loading hooks from both ~/.codex/hooks.json and ~/.codex/config.toml; prefer a single representation for this layer
hook: SessionStart
hook: SessionStart
hook: SessionStart Completed
hook: SessionStart Completed
hook: UserPromptSubmit
hook: UserPromptSubmit Completed
codex
🤖 I read the AGENTS.md for mryfmo/dotfiles.
Ponytail と agmsg-orchestration の関連手順を読み、タスク本文・threat_table・参照された証跡を読み取り専用で監査します。実行時のバイナリ、ファイル、環境が設計上の判断に拘束されるかを重点的に確認します。

exec
/bin/zsh -lc 'cat ~/.agents/skills/agmsg-orchestration/SKILL.md' in ~/Workspace/dotfiles
 succeeded in 5ms:
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
 succeeded in 26ms:
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
/bin/zsh -lc 'git status --short; git rev-parse HEAD; nl -ba .orchestration/tasks/dotfiles-T133-codex-worker-network-a01.md' in ~/Workspace/dotfiles
 succeeded in 57ms:
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
?? .orchestration/acceptance/dotfiles-T133-dispositions-a01.md
?? .orchestration/acceptance/dotfiles-T133-hold-playbook-a01.md
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
?? .orchestration/tasks/dotfiles-T129-anthropic-auth-runtime-check-a01.md
?? .orchestration/tasks/dotfiles-T129-assets-omp-hcom-followup-a02.md
?? .orchestration/tasks/dotfiles-T129-assets-omp-hcom-followup-a03.md
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
?? .orchestration/tasks/dotfiles-T133-codex-worker-network-a01.md
?? .orchestration/tasks/dotfiles-T133-dispositions-a01.md
?? .orchestration/tasks/dotfiles-T133-dispositions-a02.md
?? .orchestration/tasks/dotfiles-T133-dispositions-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-hold-playbook-a01.md
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
?? .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a01.md
?? .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a02.md
?? .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a03.md
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
?? .orchestration/validation/dotfiles-T133-codex-worker-network-a01-text-security-cf5efd5.md
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
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-8bac9e5.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-8bac9e5.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-8d42532.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-8d42532.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-987865d.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-987865d.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-e5d1b57.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-ecc7ab5.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-ecc7ab5.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-f1b862c.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-f1b862c.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-f589c7c.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-f589c7c.md.last.md
205fe85c19c03750fe3551bb96e084e9f0a676b6
     1	---
     2	format: 2
     3	task_id: dotfiles-T133-codex-worker-network-a01
     4	kind: code
     5	security: true
     6	allowed_files:
     7	  - home/dot_agents/agent-config.yaml
     8	  - scripts/generate-agent-configs.py
     9	  - tests/unit/test_generate_agent_configs.py
    10	  - home/dot_codex/modify_private_standard.config.toml
    11	  - home/dot_codex/modify_private_security.config.toml
    12	  - .orchestration/dotfiles-T133-codex-worker-network-a01/**
    13	after: [dotfiles-T133-worker-write-boundary-a01]
    14	threat_table:
    15	  - control: home/dot_agents/agent-config.yaml
    16	    disposition: "residual: only the standard and security Codex profiles gain sandbox network access; the shared sandbox defaults, writable roots, approval policy and permission hooks remain unchanged."
    17	  - control: scripts/generate-agent-configs.py
    18	    disposition: "closed: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_codex_worker_network_is_profile_scoped"
    19	  - control: tests/unit/test_generate_agent_configs.py
    20	    disposition: "residual: render tests execute generated modify scripts in temporary homes and parse their TOML output without accessing credentials or performing network operations."
    21	  - control: home/dot_codex/modify_private_standard.config.toml
    22	    disposition: "closed: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_codex_worker_network_is_profile_scoped"
    23	  - control: home/dot_codex/modify_private_security.config.toml
    24	    disposition: "closed: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_codex_worker_network_is_profile_scoped"
    25	  - control: .orchestration/dotfiles-T133-codex-worker-network-a01/**
    26	    disposition: "residual: task artifacts contain the dispatched copy and evidence for this task alone; the final-head audit compares their claims with the diff and CI."
    27	  - control: the task-file copy on the branch (.orchestration/dotfiles-T133-codex-worker-network-a01/task.md)
    28	    disposition: "residual: the copy is byte-identical to the dispatched text; TASK and RESULT bind its own sha256 and the orchestrator compares it at acceptance."
    29	  - control: the branch evidence records under .orchestration/dotfiles-T133-codex-worker-network-a01/ (report.md, validation.md, sandbox.md, learning.md and worker review evidence)
    30	    disposition: "residual: records contain prose and command output; sandbox.md lists every refused command and the audit distinguishes rendered configuration from live enforcement."
    31	  - control: task metadata
    32	    disposition: "residual: the orchestrator checks C1 to C10 and C7b before dispatch and at acceptance; the task-copy byte comparison covers the complete dispatched front matter."
    33	  - control: metadata separators
    34	    disposition: "residual: the checker reads the first YAML front-matter document and the task-copy byte comparison covers every separator."
    35	  - control: in-process effects
    36	    disposition: "residual: rendering changes repository artifacts and temporary test outputs; the worker performs no deployment, authentication change, live policy edit or sandbox-escape probe."
    37	  - control: workflow and interpreter or environment inputs
    38	    disposition: "residual: workflow files, interpreter selection, launch arguments and shell environment policy remain unchanged; tests use the existing unittest and temporary-home conventions."
    39	  - control: new or renamed scripts
    40	    disposition: "residual: no script is added or renamed; the existing renderer and two generated profile modify scripts retain their existing responsibilities."
    41	  - control: design section 5.14 item 1 (Codex worker write boundary)
    42	    disposition: "residual: worker outbound traffic goes through the Codex sandbox with network access enabled; existing writable roots and filesystem restrictions remain unchanged, and this configuration does not establish isolation from same-UID host processes."
    43	  - control: design section 5.14 item 10 (worker commands remain inside the sandbox, D-024-17a)
    44	    disposition: "residual: gh and git push use network access inside the Codex sandbox; the worker never retries outside it, while the permgate Codex no-escape rule remains pending operator action and is not claimed as implemented."
    45	  - control: orchestrator effect merge
    46	    disposition: "residual: the orchestrator merges only through gh pr merge --squash --match-head-commit <audited head> after the integration gate in Orchestrator Playbook step 10."
    47	  - control: orchestrator effect update-branch
    48	    disposition: "residual: gh pr update-branch moves the head, so CI, the feedback sweep, the task-level audit and the security review bind the new final head before the gate."
    49	  - control: orchestrator effect forced worker removal
    50	    disposition: "residual: no forced removal is planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and any forced removal records discarded uncommitted state in acceptance."
    51	premises: []
    52	---
    53	
    54	# AGMSG-TASK dotfiles-T133-codex-worker-network-a01 — plan 024 P1-15's Codex-side item split out for routing (D-024-17a)
    55	
    56	## Goal
    57	
    58	The Codex worker profiles `standard` and `security` set `sandbox_workspace_write.network_access = true` so `gh` and `git push` run inside the Codex sandbox through its network, as specified by `.orchestration/plans/024-design-quality.md` section 5.14 items 1 and 10 and decision D-024-17a. The shared base configuration and the `audit`, `review`, `express` and `deep` profiles retain their existing behavior. No other sandbox setting changes, and writable roots remain unchanged. This Codex-boundary change is assigned to a Claude seat using the `security` profile under the routing invariant.
    59	
    60	## Files
    61	
    62	1. `home/dot_agents/agent-config.yaml` declares `sandbox_workspace_write.network_access: true` under `model_profiles.standard.codex` and `model_profiles.security.codex`.
    63	
    64	   The shared `codex.sandbox_workspace_write.network_access` remains `false`. The shared block currently supplies one sandbox configuration to all profiles, so the change uses worker-profile overrides. The manifest's writable roots, sandbox modes, approval policy, permission-request hook and Claude settings remain unchanged.
    65	
    66	2. `scripts/generate-agent-configs.py` renders the declared worker-profile network overrides through `render_codex_profile`.
    67	
    68	   The renderer currently emits the sandbox network setting only in the shared base configuration. A renderer change is therefore required and is included in `allowed_files`. The new profile table overrides only `network_access`. It introduces no writable-root override or launcher-specific setting.
    69	
    70	3. `tests/unit/test_generate_agent_configs.py` adds `tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_codex_worker_network_is_profile_scoped`.
    71	
    72	   The test uses the existing `unittest`, generated modify-script and temporary-home patterns. It checks the manifest's two worker-profile declarations and parses rendered profile TOML with `tomllib`. The rendered `standard` and `security` profiles carry `network_access = true`. The shared base retains `network_access = false`, and the rendered `audit`, `review`, `express` and `deep` profiles remain unchanged. The audit profile retains its `read-only` sandbox mode, and existing writable-root settings remain unchanged.
    73	
    74	   The test is written before the manifest and renderer changes. Its assertions fail against the unchanged implementation and pass after the change. The existing audit-profile and runtime-state preservation tests remain green.
    75	
    76	4. `home/dot_codex/modify_private_standard.config.toml` and `home/dot_codex/modify_private_security.config.toml` are regenerated through the existing generator.
    77	
    78	   These two tracked paths are included in `allowed_files` as regeneration-only outputs. They receive no manual edits. Other generated outputs remain unchanged.
    79	
    80	5. `.orchestration/dotfiles-T133-codex-worker-network-a01/` contains the byte-identical dispatched `task.md`, `report.md`, `validation.md`, `sandbox.md`, `learning.md` and worker review evidence. Worker review filenames carry the required `-worker-` infix.
    81	
    82	   The report maps the requirements to test selectors and states the user-visible effect that Codex sessions selecting `standard` or `security` gain sandbox network access. It states that this boolean setting supplies no outbound domain allowlist.
    83	
    84	   The report prepares the operator's exact deterministic rule that stops Codex PermissionRequest handling from approving sandbox escapes or unsandboxed retries. It identifies the insertion point before allow-pattern evaluation in `home/dot_local/bin/common/executable_permgate::decide`, the policy source `home/dot_agents/permgate-policy.yaml` and the existing `permgate codex` hook binding. It accounts for unsupported request shapes without allowing an escape. This is proposed operator text, and neither permgate source is changed by the worker.
    85	
    86	## Out of scope
    87	
    88	Permgate code, deterministic policy and permission-request hook changes belong to the operator. The worker performs no live policy edit or escape probe.
    89	
    90	The Claude-side boundary of P1-15 belongs to `dotfiles-T133-worker-write-boundary-a01`. D-024-20 makes that task's merge a dispatch prerequisite. This task's branch is rebased onto `origin/main` after that merge and before implementation.
    91	
    92	Any writable-root change is outside this task. Sandbox modes, approval policy, launch arguments, authentication, credential storage and deployment remain unchanged. The dropped wrapper design is not reintroduced.
    93	
    94	## Measurements
    95	
    96	The caps in Check are measured from their analogues on `origin/main` (C-79). Source: the existing per-profile `sandbox_mode` override is 2 renderer lines (`scripts/generate-agent-configs.py:598-600`) and 1 manifest line; the network override adds a `[sandbox_workspace_write]` table with one key in `render_codex_profile` (about 6 lines), 2 manifest lines and the matching lines in `render_codex_profile_modify` (line 1036; about 10), so about 20 lines, capped at 40. Tests: the analogous `test_audit_profile_renders_read_only_sandbox_override` is 37 lines (`tests/unit/test_generate_agent_configs.py:795-831`); one test of the same shape is capped at 80.
    97	
    98	## Check
    99	
   100	`make render-check`, `make validate-agent-assets`, `make format` and `uv run --no-project --with pyyaml python -m unittest tests.unit.test_generate_agent_configs -v` have their commands, verbatim output, exit statuses and tested heads pasted in `.orchestration/dotfiles-T133-codex-worker-network-a01/validation.md`. The render check, asset validation and unit module are green.
   101	
   102	The new profile-scoping test carries red-before-implementation and green-final-head evidence. Render evidence identifies both changed worker profiles and all four unchanged orchestrator-side profiles. It records the unchanged base sandbox block and writable roots. These tests establish rendered configuration behavior and make no claim of live sandbox enforcement. No local Bats tests run.
   103	
   104	An inherited formatting failure is reproduced on the unchanged base and recorded with its output. It remains a reported failure and receives no repair outside `allowed_files`.
   105	
   106	`git diff --numstat origin/main...HEAD` shows at most 40 changed lines outside `tests/` and `.orchestration/`, excluding the regenerated `home/dot_codex/modify_private_standard.config.toml` and `home/dot_codex/modify_private_security.config.toml`, and at most 80 changed lines under `tests/`. Changed lines are additions plus deletions. Validation includes per-file numstat, both totals and the complete changed-file inventory.
   107	
   108	The orchestrator runs the format-2 task-consistency checker, including C1 to C10 and C7b, before dispatch and at acceptance. The task text and threat table pass the security-profile C-80 review before dispatch, and its findings enter the task's finding-class table. The task copy remains byte-identical to the dispatched file.
   109	
   110	## Completion
   111	
   112	The Completion clause of `.orchestration/tasks/dotfiles-T133-hold-playbook-a01.md` applies with `dotfiles-T133-codex-worker-network-followup-a01` as the owner of any advisory P2 and `task_copy=<sha256 of .orchestration/dotfiles-T133-codex-worker-network-a01/task.md>` in the RESULT. This task's scope, Check, `security: true`, prerequisite, Claude-seat routing and evidence paths govern that reference.
   113	
   114	One PR starts from a fresh branch off `origin/main`. The orchestrator writes the advisory owner task before recording its first ownership disposition. A small in-scope P2 follows the inherited `check=` revise procedure while INV-6 permits it.
   115	
   116	The worker's own pre-push review is one round at most. Every worker-side fix round counts toward INV-6. A surviving P0/P1 is sent in the RESULT as `open:<finding-or-thread-id>` and stops integration for the operator's decision. The worker starts no additional private correction-and-review cycle. The third finding of one class stops further rounds until the orchestrator's re-plan.
   117	
   118	The RESULT identifies the final head, base, branch, changed files, test selectors, measured caps, evidence paths, task-copy hash, pending operator step and every Bot finding's proposed disposition. It carries the precheck evidence required by the applicable RESULT procedure.
   119	
   120	The orchestrator runs the task-level audit and the security review on the final head and dispositions every finding before the gate. Final-head CI, the feedback sweep, audit, security review, acceptance record, gate and merge follow Orchestrator Playbook step 10 and the repository's security-review requirements. A changed head receives fresh evidence.
   121	
   122	No `@codex review` comment is issued. Every `gh` write and Git write runs as an individual command without shell chaining or a wrapper combining writes. Every worker command remains inside its sandbox. An operation that cannot complete there produces a blocked PONG naming the exact command and refusal, with no retry outside the sandbox.
   123	
   124	## Checks (pasted by the orchestrator before each send)
   125	
   126	```
   127	(pasted at dispatch)
   128	```
   129	
   130	Implementation and runtime verification remain pending worker execution.
   131	Unrestricted outbound sandbox network access and the pending operator permgate rule remain residuals.
**Focusing on task scope**
exec
/bin/zsh -lc "sed -n '/## Codex seat worklogs/,/"'^## /p'"' ~/.agents/skills/agmsg-orchestration/SKILL.md" in ~/Workspace/dotfiles
exec
/bin/zsh -lc 'cat ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail/SKILL.md' in ~/Workspace/dotfiles
exec
/bin/zsh -lc "python3 -c 'import json,pathlib; p=pathlib.Path(\".ua\"); print((p/\"meta.json\").read_text() if (p/\"meta.json\").exists() else \"no meta\"); g=json.loads((p/\"knowledge-graph.json\").read_text()) if (p/\"knowledge-graph.json\").exists() else {}; print(json.dumps([{k:n.get(k) for k in (\"name\",\"filePath\",\"summary\")} for n in g.get(\"nodes\",[]) if any(x in str(n.get(\"filePath\",\"\")) for x in (\"generate-agent-config\",\"agent-config.yaml\",\"worker-cap\",\"permgate\"))],ensure_ascii=False))'" in ~/Workspace/dotfiles
exec
/bin/zsh -lc 'nl -ba .orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md' in ~/Workspace/dotfiles
 succeeded in 169ms:
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

 succeeded in 260ms:
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

 succeeded in 280ms:
     1	---
     2	format: 2
     3	task_id: dotfiles-T133-worker-write-boundary-a01
     4	kind: code
     5	security: true
     6	allowed_files:
     7	  - home/dot_agents/agent-config.yaml
     8	  - home/.chezmoitemplates/claude-settings-managed.json
     9	  - home/.chezmoitemplates/claude-worker-settings.json
    10	  - home/.chezmoitemplates/claude-managed-settings.json
    11	  - home/dot_claude-worker/modify_private_settings.json
    12	  - home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl
    13	  - .claude/settings.json
    14	  - scripts/generate-agent-configs.py
    15	  - Makefile
    16	  - home/dot_local/bin/common/executable_herdr-agents
    17	  - home/dot_local/bin/common/executable_herdr-agent-state.sh
    18	  - home/dot_agents/skills/agmsg-orchestration/SKILL.md
    19	  - .gitignore
    20	  - tests/unit/test_generate_agent_configs.py
    21	  - tests/unit/test_claude_settings_merge.py
    22	  - tests/unit/test_herdr_agents.py
    23	  - tests/unit/test_agmsg_orchestration_docs.py
    24	  - tests/unit/test_claude_worker_settings.py
    25	  - tests/unit/test_claude_managed_settings.py
    26	  - .orchestration/dotfiles-T133-worker-write-boundary-a01/**
    27	after: []
    28	threat_table:
    29	  - control: "tests/unit/test_agmsg_orchestration_docs.py (amendment 1: only the assertion of the Worker Playbook step 4 sentence this task rewrites changes; PR #427 edits this file first and merges before this PR, which rebases onto it)"
    30	    disposition: "residual: one assertion follows the rewritten sentence; the doc test module stays green in CI on the final head"
    31	  - control: "home/dot_agents/agent-config.yaml (trusted checkout and interpreter bindings, static trusted_paths inventory, distinct worker policy, managed sandbox policy and worker caches)"
    32	    disposition: "residual: the rendered policy reduces accidental and injected damage; tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_policy_is_separate_from_orchestrator_policy checks both platforms without claiming same-UID isolation."
    33	  - control: "home/.chezmoitemplates/claude-settings-managed.json (orchestrator user settings with failIfUnavailable true, onFailure block and hook PATH bindings)"
    34	    disposition: "residual: the user baseline preserves orchestrator functions within the managed sandbox policy; tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_orchestrator_settings_keep_existing_policy checks the specified changes and retained settings."
    35	  - control: "home/.chezmoitemplates/claude-worker-settings.json (static trusted-path and worktree-configuration Edit denies, empty user exclusions, restricted write allowances, native merge denials and minimal delivery hooks)"
    36	    disposition: "residual: dedicated user settings reduce worker access to trusted paths; tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_policy_renders_for_both_platforms checks the baseline and distinguishes it from shared managed exclusions and socket access."
    37	  - control: "home/.chezmoitemplates/claude-managed-settings.json (admin-required sandbox enforcement, fixed rendered control-plane exclusions and Herdr socket allowance)"
    38	    disposition: "residual: operator installation establishes the documented enforcement scope against project and local sandbox relaxation; tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_rendered_policy_requires_admin_sandbox asserts the rendered keys; shared control-plane capabilities and same-UID host access remain residual."
    39	  - control: "home/dot_claude-worker/modify_private_settings.json (deployment of the dedicated worker baseline without importing orchestrator policy)"
    40	    disposition: "residual: replacing the worker baseline's managed values reduces stale or permissive user configuration; tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_settings_replace_stale_policy_idempotently checks repeated rendering in temporary homes."
    41	  - control: "home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl (anchored launch-root guard for tracked and main-checkout local project hooks)"
    42	    disposition: "residual: the guard reduces execution of worker-influenced project code and orchestrator hooks in worker sessions; tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_project_guard_uses_launch_root_and_never_runs_worker_payloads checks fixed arguments, canonical identity and child status."
    43	  - control: "formatter and project-map reload configuration-selection boundary (the edited file path in the hook tool input and its owning repository)"
    44	    disposition: "residual: the guard skips these commands for input outside CLAUDE_PROJECT_DIR or in a worker repository under .claude/worktrees/, preventing consumption of worker-controlled Prettier JavaScript configuration and ruff settings; tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_project_guard_uses_launch_root_and_never_runs_worker_payloads checks both the skip and normal anchored-file execution."
    45	  - control: ".claude/settings.json (portable HOME-relative installed-guard commands with fixed operation identifiers, explicit HOME re-export, pinned system PATH and onFailure block)"
    46	    disposition: "residual: guarded commands reduce worker-triggered project-hook execution while host-specific executable bindings remain in the per-host rendered guard and worker settings; tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_every_tracked_project_hook_is_guarded_and_blocks_on_failure exhaustively traverses the hook entries and checks this split."
    47	  - control: "scripts/generate-agent-configs.py (separate user and managed settings generation, static manifest deny inventory and absolute executable bindings)"
    48	    disposition: "residual: rendering an explicit manifest list removes Git object traversal from inventory construction; tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_deny_inventory_is_static_and_matches_manifest checks exact manifest correspondence and filesystem coverage."
    49	  - control: "Makefile (the install-managed-settings target that renders a home-directory staging file and prints the operator's sudo install command)"
    50	    disposition: "residual: staging makes the administrative installation concrete without granting the worker administrative authority; tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_install_target_stages_and_prints_without_running_sudo checks the destination, rendered content, quoting and absence of privileged execution."
    51	  - control: "home/dot_local/bin/common/executable_herdr-agents (worker pane environment, dedicated Claude configuration, private caches, worker user hooks and guarded main-checkout local hooks)"
    52	    disposition: "residual: launch preparation reduces accidental inheritance of orchestrator settings and stale hooks (the legacy worktree-local file included: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_add_worker_migrates_legacy_worktree_local_hooks checks that migration against a fixture with a previously generated entry); tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_every_worker_launch_receives_dedicated_policy_and_private_caches captures managed and standalone launches and repeated starts."
    53	  - control: "home/dot_local/bin/common/executable_herdr-agent-state.sh (repository-owned Herdr state helper with an explicitly supplied absolute Python interpreter)"
    54	    disposition: "residual: binding the helper and its Python child reduces shim execution; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_hook_descendants_do_not_execute_path_interpreters checks executed identities with planted shims."
    55	  - control: "home/dot_agents/skills/agmsg-orchestration/SKILL.md (the governing Worker Playbook step 4 sentence)"
    56	    disposition: "residual: the sentence removes procedural authorization for worker sandbox escapes; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_playbook_requires_every_command_inside_sandbox checks its replacement; shared managed control-plane capabilities remain available and are not represented as per-seat isolation."
    57	  - control: ".gitignore (the .uv-cache directory pattern)"
    58	    disposition: "residual: ignoring the private cache reduces accidental cache publication; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_uv_cache_directory_is_gitignored checks the pattern in a temporary checkout."
    59	  - control: "tests/unit/test_generate_agent_configs.py (separate platform policies, static inventory, interpreter bindings and tracked hook coverage)"
    60	    disposition: "residual: render fixtures verify configuration and command construction; they do not establish live enforcement or authenticate host-local inputs."
    61	  - control: "tests/unit/test_claude_settings_merge.py (orchestrator baseline preservation and failure-policy rendering through the existing merge)"
    62	    disposition: "residual: temporary HOME fixtures verify baseline entries and identify runtime-added hooks separately; they do not install administrative settings."
    63	  - control: "tests/unit/test_herdr_agents.py (every launch route, repeated starts, main-local and worker-user hook placement, the legacy worktree-local migration, descendants, caches and retained native denials)"
    64	    disposition: "residual: fake launchers and subprocess markers verify effective arguments and executed fixture identities without starting live seats; shared managed exceptions remain explicitly outside per-seat exclusion claims."
    65	  - control: "tests/unit/test_claude_worker_settings.py (dedicated settings deployment, static narrow denies, worktree configuration protection, project guard and hook failure configuration)"
    66	    disposition: "residual: fixtures verify configured controls and credential-free deployment behavior; runtime permission checks and the remaining path-consumption window remain deployment and host residuals."
    67	  - control: "tests/unit/test_claude_managed_settings.py (managed policy rendering, conflicting project and local settings fixtures and nonprivileged staging)"
    68	    disposition: "residual: fixtures verify the selected documented enforcement keys and staging behavior without simulating proof of Claude runtime enforcement or performing sudo installation."
    69	  - control: ".orchestration/dotfiles-T133-worker-write-boundary-a01/** (this task's branch artifacts)"
    70	    disposition: "residual: artifacts distinguish documentation facts, historical probes, final-head fixture results and unperformed operator deployment; acceptance compares their claims with the diff and CI."
    71	  - control: "the task-file copy at .orchestration/dotfiles-T133-worker-write-boundary-a01/task.md (amendment 1 text)"
    72	    disposition: "residual: the first push deletes the a01 copy and adds the byte-identical dispatched a02 copy; TASK and RESULT carry the a02 copy's SHA256, which the orchestrator verifies at acceptance."
    73	  - control: "the evidence records under .orchestration/dotfiles-T133-worker-write-boundary-a01/"
    74	    disposition: "residual: report.md, validation.md, sandbox.md, learning.md, autoskill.md and worker review evidence retain commands, outputs, statuses and tested revisions without credentials or unmasked home-directory paths."
    75	  - control: "task metadata (PR_FEEDBACK_EVIDENCE, AUDIT_EVIDENCE, ACCEPTANCE_EVIDENCE and REVIEW_EVIDENCE)"
    76	    disposition: "residual: the orchestrator checks C1 to C10 and C7b, verifies dispatched bytes and binds integration evidence to the final head; P1-14 a05 and P1-6 implement retrieval of evidence of record from GitHub at its SHA; the GitHub boundary is detection, not prevention."
    77	  - control: metadata separators
    78	    disposition: "residual: the first document separators delimit format-2 metadata; the task-copy SHA256 binds the complete document."
    79	  - control: in-process effects
    80	    disposition: "residual: generation and tests use repository files and temporary fixtures; the worker performs no live deployment, login, administrative installation, permission-policy mutation or operator-session restart."
    81	  - control: workflow and interpreter or environment inputs
    82	    disposition: "residual: absolute interpreters, Python -I, sanitized Git, fixed hook PATH and trusted executable bindings reduce environment injection; the host, native loader and same-UID processes remain outside this task's security guarantee."
    83	  - control: new or renamed scripts
    84	    disposition: "residual: the worker settings modify script, orchestrator-only guard and repository-owned Herdr state helper have named source and installed paths; RESULT inventories their interpreter and descendant bindings without introducing a worker-write-boundary hook or gh wrapper."
    85	  - control: "5.14 item 0: host threat model"
    86	    disposition: "residual: host controls reduce accidental and injected damage without isolating seats sharing one OS user; prevention of worker-initiated merges requires a separate OS user or host under D-024-23's future P1-16, which the operator decides; the GitHub boundary is detection, not prevention, through P1-11's regime check in the next records PR for missing acceptance or gate evidence; shared managed control-plane exclusions and the Herdr socket remain residual."
    87	  - control: "5.14 item 1: worker write controls"
    88	    disposition: "residual: dedicated configuration, static symlink-aware Edit denies including worktree configuration and orchestrator worklogs and caches, narrow writable agmsg stores, managed sandbox enforcement and failIfUnavailable true reduce damage; documented path checks do not establish atomic immunity to concurrent path swaps."
    89	  - control: "5.14 item 2: sanitized environment and private executable PATH"
    90	    disposition: "residual: sanitized Git verification and absolute hook entrypoints reduce injected configuration, while PATH=/usr/bin:/bin binds upstream env-bash descendants away from shims; the remaining consuming-helper contracts belong to P1-14 a05, P1-10 a02, audit-pool-a02 and P1-6."
    91	  - control: "5.14 item 3: trusted-path checks"
    92	    disposition: "residual: canonical anchor and interpreter checks reduce worker-selected trusted paths and account for symlink components and filesystem case aliases; other consuming-helper checks remain with their owning hardening tasks."
    93	  - control: "5.14 item 4: verified executable and consumed-byte identity"
    94	    disposition: "residual: hooks execute selected absolute entrypoints and trusted scripts, and upstream shell descendants inherit the fixed system PATH; evidence snapshots, last-use digest checks and their race limitations remain with the consuming orchestrator-side tasks; store-selected driver execution remains the separately named agmsg residual."
    95	  - control: "5.14 item 5: output and reservation identity"
    96	    disposition: "residual: this task adds no reservation protocol; full-head output names, fixed-inode locks and physical-slot identity remain with the orchestrator-side tasks that create them."
    97	  - control: "5.14 item 6: honest residuals, hooks and MCP"
    98	    disposition: "residual: guarded tracked and main-local project hooks and minimal worker user hooks reduce host execution routes; shared managed Herdr socket access, control-plane exclusions, approved external processes and same-UID processes outside every seat sandbox remain residual."
    99	  - control: "5.14 item 7: trusted-execution verification"
   100	    disposition: "residual: this task records red-then-green render, merge, managed-policy, guard, launch, descendant and cache tests; P1-6 owns tests/unit/trusted_exec_contract.py and the consuming-helper contract tests."
   101	  - control: "5.14 item 8: committed approval ledger"
   102	    disposition: "residual: the regime reads the ledger through the GitHub contents API at the SHA returned by git ls-remote origin refs/heads/main; P1-14 a05 implements that read, and local refs, files and object traversal provide no approval authority; the GitHub boundary is detection, not prevention."
   103	  - control: "5.14 item 9: private uv caches"
   104	    disposition: "residual: per-seat worker caches, restricted worker write allowances and explicit denies on the orchestrator worklog and uv-cache reduce cache poisoning; consuming hardening tasks use the protected orchestrator cache with --offline and execute no worker, shared uv or mise cache content."
   105	  - control: "5.14 item 10: no worker command outside the sandbox"
   106	    disposition: "residual: empty worker user exclusions and disabled unsandboxed requests reduce escape routes; the worker rule forbids using shared managed control-plane exceptions, whose availability and Herdr socket access remain residual; the deterministic Codex permgate rule and live deployment remain operator steps."
   107	  - control: "hook failure policy"
   108	    disposition: "residual: every generated and tracked hook entry, including launcher-written worker user and main-local entries, carries onFailure block, reducing fail-open behavior where Claude supports it; configuration tests cover missing-command and timeout policy, while background hooks and events on which the field has no effect carry no enforcement responsibility."
   109	  - control: "agmsg store driver and plugin selection (team configuration drivers.partition, db/trusted-plugins authorization and installed storage.sh sourcing)"
   110	    disposition: "residual: every seat writes the store, and installed storage.sh resolves drivers.partition as a driver path and sources it during unsandboxed delivery; it also uses db/trusted-plugins to authorize plugins/partition/shared.sh for sourcing; fixed PATH does not stop these routes; worker denies on plugins/** and db/trusted-plugins reduce the plugin route; dotfiles-T133-agmsg-hardening-a01 owns upstream basename validation, plugin authorization hardening and their adversarial red-then-green tests; this task introduces no store-derived sourcing beyond the installed scripts' current behavior."
   111	  - control: orchestrator effect merge
   112	    disposition: "residual: the worker is forbidden to merge; the orchestrator follows the final-head integration gate, required permission approval and pinned squash-merge procedure, with evidence of record retrieved from GitHub; shared credentials still permit worker-initiated API merges, so the GitHub boundary is detection, not prevention."
   113	  - control: orchestrator effect update-branch
   114	    disposition: "residual: the orchestrator owns branch updates and obtains fresh required CI, feedback, audit and security evidence for the resulting head."
   115	  - control: orchestrator effect forced worker removal
   116	    disposition: "residual: no forced removal is planned; existing dirty-worktree protections remain, and acceptance identifies any operator-authorized discarded state."
   117	premises:
   118	  - claim: >-
   119	      The historical a05 premises carried by the preceding text describe its recorded observations. They do not require this worker to rebuild PR 400, edit the approval ledger or implement P1-14 a05.
   120	    sources:
   121	      - .orchestration/tasks/dotfiles-T133-permission-guard-gate-a05.md
   122	      - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md
   123	  - claim: >-
   124	      D-024-21 establishes the host threat model and dedicated Claude worker configuration. D-024-23 supersedes D-024-22's credential-separation claim because gh Keychain access is shared by seats running as the same macOS user. Prevention requires a separate OS user or host; the current GitHub boundary is detection, not prevention.
   125	    sources:
   126	      - .orchestration/decisions.tsv
   127	      - .orchestration/plans/024-design-quality.md
   128	      - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md
   129	  - claim: >-
   130	      The existing Claude settings modify script merges the orchestrator user baseline into current settings and appends an attachment hook. The dedicated worker renderer does not import that orchestrator settings merge or its attachment behavior. The administrative managed-settings file is a separate deployment destination.
   131	    sources:
   132	      - home/dot_claude/modify_private_settings.json
   133	      - home/.chezmoitemplates/claude-settings-managed.json
   134	    verification: tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_settings_do_not_import_orchestrator_hooks
   135	  - claim: >-
   136	      The current launcher constructs worker profile options separately from the pane environment. The dedicated Claude configuration directory and private cache variables reach the actual worker process on every launch route. This task adds no gh configuration directory or credential-separation mechanism.
   137	    sources:
   138	      - home/dot_local/bin/common/executable_herdr-agents
   139	      - home/dot_agents/agent-config.yaml
   140	    verification: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_every_worker_launch_receives_dedicated_policy_and_private_caches
   141	  - claim: >-
   142	      Linked-worktree Claude sessions load the main checkout's .claude/settings.local.json. The current launcher writes worker-local delivery hooks and merge denials into a different file. Worker delivery moves to the worker configuration directory's user settings, and the launcher's main-checkout local hooks receive the orchestrator-only guard.
   143	    sources:
   144	      - https://code.claude.com/docs/en/settings#where-claude-code-keeps-the-local-file-in-a-git-repository
   145	      - home/dot_local/bin/common/executable_herdr-agents
   146	      - .claude/settings.local.json
   147	    verification: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_linked_worktree_uses_worker_user_hooks_and_guarded_main_local_hooks
   148	  - claim: >-
   149	      Managed sandbox.enabled true, failIfUnavailable true and allowUnsandboxedCommands false establish the documented admin-required enforcement scope. Project and local settings cannot supply sandbox relaxations in that scope. User settings and shared managed exceptions remain distinct from project and local settings.
   150	    sources:
   151	      - https://code.claude.com/docs/en/sandboxing#repository-settings-under-an-admin-required-sandbox
   152	      - .orchestration/plans/024-design-quality.md
   153	      - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md
   154	    verification: tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_managed_render_is_independent_of_conflicting_project_and_local_settings
   155	  - claim: >-
   156	      Installed agmsg storage.sh resolves the writable team configuration's drivers.partition value as a driver path and sources it during delivery. The upstream hardening belongs to dotfiles-T133-agmsg-hardening-a01 and remains a residual of this task.
   157	    sources:
   158	      - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md
   159	      - .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-08e6ac7.md.last.md
   160	---
   161	
   162	# AGMSG-TASK dotfiles-T133-worker-write-boundary-a01 — INV-6 reset of a01 on tools/worker-write-boundary-a01, seat a010; plan 024 P1-15 under D-024-17, D-024-19, D-024-20, D-024-21 and D-024-23
   163	
   164	## Goal
   165	
   166	This is the amendment-1 text of the task dispatched at 2026-10-19T05:42Z (the ninth-round text that passed its pre-dispatch security review). Amendment 1 folds in two interpretation notes the worker needed (the inherited make format clause; the portable tracked `.claude/settings.json` with host-specific paths only in the rendered guard) and removes the Codex worker profile item (a Codex seat edits no Codex-boundary source; it becomes the separate Claude-seat task dotfiles-T133-codex-worker-network-a01). Everything else is the dispatched text in meaning; the branch, the eight green tests and the fixtures stay; the worker swaps the task copy to this text at its next push.
   167	
   168	The host is not a security boundary between seats sharing one OS user. gh keys Keychain credentials by host and user, so a worker running as the same macOS user can read the orchestrator's token regardless of `GH_CONFIG_DIR`. Prevention of a worker-initiated merge requires a separate OS user or host under D-024-23's future P1-16, which the operator decides whether to pursue. Until then the GitHub boundary is detection, not prevention. The regime detects missing acceptance or gate-passage evidence in the next records PR, not at main-push time, because the records reach main only with that boundary PR. On a PR touching `.orchestration/acceptance/**`, the regime job checks every main merge commit since the previous boundary for its corresponding acceptance record with gate-passage evidence and fails the PR when one is missing. P1-11 owns implementation of that check; this task states section 5.14 item 0's detection rule. Approvals and gate evidence of record are read from GitHub at a SHA through its API inside the sandbox. Host-local controls reduce accidental and injected damage without establishing isolation from a malicious same-UID process.
   169	
   170	This task implements section 5.14 items 1, 9 and 10 through a dedicated Claude worker configuration directory, static Edit deny rules on trusted paths and worktree configuration, managed sandbox enforcement, guarded project hooks, hook interpreter and PATH bindings, private worker caches and the rule that worker commands run inside their sandbox. Every Claude seat has `sandbox.failIfUnavailable: true`.
   171	
   172	The administrative managed policy is shared by every Claude seat. Its Herdr socket allowance and three control-plane exclusions remain available to workers as well as the orchestrator. Empty arrays in worker user settings do not subtract these managed entries. Their availability is a residual under item 0, and the worker execution rule supplies no authorization to use them outside the sandbox.
   173	
   174	[memory:decision] D-024-20 makes this task the dispatch prerequisite of P1-14 a05, P1-10 a02, audit-pool-a02 and P1-6. The orchestrator places this task in their `after:` fields before dispatch. This task has `after: []`. A Codex seat performs these Claude configuration edits under the routing rule, including the Worker Playbook step 4 sentence permitted by plan 021 step 8.3. This Codex seat edits no Codex-boundary source.
   175	
   176	The design source is `.orchestration/plans/024-design-quality.md` section 5.14 items 0 through 10. D-024-21, D-024-23 and the amended items 0, 1 and 8 govern this revision. D-024-22's proposed gh credential separation is superseded. The acceptance record preserves documentation facts and earlier proposals as history.
   177	
   178	The third C-80 text review is `.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-ecc7ab5.md.last.md`. Its five P1 findings remain recorded. The retained mechanisms are documented symlink-aware deny rules, approval reads outside the local object database, hook interpreter bindings and runtime hook failure policy.
   179	
   180	The fourth C-80 text review is `.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-8d42532.md.last.md`. Its six P1 findings remain recorded. The retained mechanisms are the static manifest deny inventory, protection of the orchestrator worklog and cache, narrow home denies around writable agmsg stores, correct linked-worktree hook placement and fixed hook-runtime PATH.
   181	
   182	The fifth C-80 text review is `.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-08e6ac7.md.last.md`. Its three P1 findings remain recorded. This revision removes the gh credential-separation mechanism, records the upstream agmsg store-driver residual and moves sandbox enforcement into administrative managed settings.
   183	
   184	The file-tool rule is the documented sentence, “Deny rules: apply when either the requested path or the file it resolves to matches.” Edit and Write refuse a requested file that is itself a symlink. Directory symlinks are subject to resolved-target permission checks, and the tools check the resolved location again when opening the approved file. These documented checks reduce redirection risk without establishing an atomic host security boundary against concurrent same-UID changes. [Claude permission reference](https://code.claude.com/docs/en/permissions#symlinks)
   185	
   186	The 2026-10-19T03:45:06Z sandbox probe ran `gh api repos/mryfmo/dotfiles --jq .name` and returned `dotfiles`. The recorded sandbox proxy used CONNECT without TLS interception, and gh read the Keychain token. This historical observation confirms neither credential separation nor final-head deployment readiness.
   187	
   188	The documentation facts recorded at 03:2xZ establish that Edit denies also affect the Bash sandbox, hooks reload during a session and an unavailable sandbox is fail-open by default. D-024-21's 04:0xZ decision establishes the dedicated Claude configuration mechanism, directory-specific Claude credentials, symlink coverage and `onFailure: "block"` support. These Claude credentials do not separate gh Keychain access.
   189	
   190	The settings documentation states, “In a worktree, it uses the file at the main checkout’s root.” Linked-worktree sessions therefore load the main checkout's `.claude/settings.local.json`. Worker hooks belong in `~/.claude-worker/settings.json`, and the main checkout's local hooks also receive the orchestrator-only guard. [Claude local settings reference](https://code.claude.com/docs/en/settings#where-claude-code-keeps-the-local-file-in-a-git-repository)
   191	
   192	## Files
   193	
   194	1. `home/dot_agents/agent-config.yaml` remains the source of agent policy and model profiles.
   195	
   196	   The manifest names `orchestrator_checkout` as the anchored primary checkout and supplies trusted deployment bindings for the guard, hook scripts and absolute interpreters. These bindings resolve outside worker worktrees and executable caches. Worker cwd, tool input, worktree configuration and inherited command variables do not select them. The manifest also supplies the trusted bindings from which the render resolves the absolute directories holding `ruff`, `prettier` and `terminal-browser`, without using mise shims.
   197	
   198	   The manifest defines a separate Claude worker settings output at `home/.chezmoitemplates/claude-worker-settings.json` and an administrative managed-settings output at `home/.chezmoitemplates/claude-managed-settings.json`. The worker configuration directory is `~/.claude-worker`. The launcher passes its expanded absolute path as `CLAUDE_CONFIG_DIR`.
   199	
   200	   A static `trusted_paths:` list names every protected top-level path of the anchored checkout and the protected home paths. It explicitly includes `<anchored-checkout>/.agents/worklog/**` and `<anchored-checkout>/.agents/worklog/uv-cache/**`. The `.claude` entries protect tracked contents and the main checkout's `.claude/settings.local.json` without denying the whole `.claude/worktrees/` tree. The list explicitly names directory targets and descendant patterns where both are required.
   201	
   202	   Separate worker Edit denies protect `//<anchored-checkout>/.claude/worktrees/*/.claude/**` and `//<anchored-checkout>/.claude/worktrees/*/.mcp.json`. The `.claude` directory target is also protected. Ordinary worktree source files and the per-seat cache remain outside these configuration denies.
   203	
   204	   The home-path denies are `~/.agents/agent-config.yaml`, `~/.agents/model-profiles.env`, `~/.agents/skills/**/scripts/**`, `~/.agents/skills/**/SKILL.md`, `~/.agents/skills/agmsg/plugins/**`, `~/.agents/skills/agmsg/db/trusted-plugins`, `~/.claude/**`, `~/.claude-worker/**`, `~/.local/bin/**`, `~/.local/share/**`, `~/.local/state/**`, `~/.local/share/mise/**`, `~/.config/**`, `~/.cache/uv/**` and `~/.local/share/uv/**`. No blanket deny on `~/.agents/**` or `~/.local/**` replaces this list.
   205	
   206	   The agmsg store paths `~/.agents/skills/agmsg/db`, `~/.agents/skills/agmsg/teams`, `~/.agents/skills/agmsg/run` and `~/.agents/skills/agmsg/ext-tools` remain writable. Deny patterns cover neither these directory targets nor their descendants except the file `~/.agents/skills/agmsg/db/trusted-plugins`. Edit denies merge into the sandbox configuration, so Bash writes to that file and `~/.agents/skills/agmsg/plugins/**` are refused too. Their influence on installed delivery-script driver and plugin selection remains the separately owned agmsg residual.
   207	
   208	   The orchestrator retains its existing permissions, cache allowances and hook functions within the administrative managed policy. Its user baseline receives `failIfUnavailable: true`, `onFailure: "block"` on its hooks and the interpreter and PATH bindings below. Its exclusion entries match the three control-plane entries specified below; the former Linux `gh *` exclusion is removed.
   209	
   210	   The worker user policy contains no excluded commands and sets `allowUnsandboxedCommands: false`. It contains no Herdr socket allowance and no allow-all Unix socket switch. Its sandbox is enabled and has `failIfUnavailable: true`. Shared managed entries remain effective despite these empty worker arrays.
   211	
   212	   Worker `sandbox.filesystem.allowWrite` contains only the existing agmsg store paths and per-seat cache paths. The worktree is the project root and supplies its ordinary project write root. Shared uv and mise write allowances are not copied into worker settings.
   213	
   214	   Existing model selections, Codex worker profile values, Codex sandbox and approval arguments and Codex shared Git grants retain their meaning and remain unchanged. The deterministic Codex permgate rule that stops approving sandbox escapes is an operator step.
   215	
   216	2. `scripts/generate-agent-configs.py` renders the distinct orchestrator user, worker user and administrative managed baselines from the manifest.
   217	
   218	   The trusted-path deny inventory is rendered from the static `trusted_paths:` list. Rendering performs no Git object traversal, `git ls-tree` enumeration or tracked-path discovery. Worker-writable refs, replacement refs and objects do not determine the list.
   219	
   220	   Anchored checkout rules use absolute `//` permission patterns. Rendering includes the explicitly listed trusted paths themselves and their descendants. It emits no checkout-wide parent deny that defeats ordinary worktree writes. The separate worktree-configuration denies remain present.
   221	
   222	   Edit denies cover Write, MultiEdit and NotebookEdit through Claude's permission system. Requested-path and resolved-target matching supply the documented symlink coverage. The generator creates no `executable_worker-write-boundary.py` or replacement PreToolUse path validator.
   223	
   224	   Every direct Git verification introduced or changed by this task follows section 5.14 item 2. It begins with `env -i`, uses the selected absolute Git executable and an explicit `-C`, sets `GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL=/dev/null`, and supplies `-c core.hooksPath=/dev/null -c core.fsmonitor=false -c protocol.allow=never -c protocol.https.allow=always`. Diff and show also use `--no-ext-diff --no-textconv` and `-c core.attributesFile=/dev/null -c core.sshCommand=false`.
   225	
   226	   The private executable-link directory contains only links to selected absolute trusted binaries. Rendering rejects missing bindings, worker-controlled executable paths, shims, empty PATH entries and relative PATH entries. Python invocations use `-I`. Hook execution uses the role-specific pinned PATH bindings specified below. The render test asserts that `ruff`, `prettier` and `terminal-browser` resolve under the rendered orchestrator tool PATH on the rendering host and that no entry of that PATH is a shims directory.
   227	
   228	   `tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_deny_inventory_is_static_and_matches_manifest` asserts that the rendered list equals the manifest entry after trusted anchor and home expansion. It explicitly asserts the rendered home-path deny patterns `~/.local/share/**` and `~/.local/state/**`, including the application code under `~/.local/share` used by `~/.local/bin` wrappers such as `terminal-browser`. It reads the filesystem of the test's own checkout and asserts that every tracked top-level source path is represented. It invokes no Git command to discover those paths.
   229	
   230	   The inventory fixtures cover files, directories, `.claude` children, the main-local settings file, ordinary worktree writes, both worktree-configuration patterns, an anchor containing spaces and both explicit worklog patterns. Adding a top-level source path without a manifest entry makes the coverage assertion fail. Planted Git environment and replacement-ref fixtures leave rendering unchanged.
   231	
   232	   `tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_denies_leave_agmsg_stores_writable` asserts the rendered deny patterns `~/.agents/skills/agmsg/plugins/**` and `~/.agents/skills/agmsg/db/trusted-plugins` and verifies that the four store directories `db`, `teams`, `run` and `ext-tools` and their descendant fixtures remain writable except that one file.
   233	
   234	3. `home/.chezmoitemplates/claude-settings-managed.json` remains the orchestrator user baseline.
   235	
   236	   The existing `home/dot_claude/modify_private_settings.json` continues to render the orchestrator's `~/.claude/settings.json`. That modify script is not imported into the dedicated worker renderer and remains outside `allowed_files`.
   237	
   238	   This existing template's name does not make it administrative managed settings. The new `claude-managed-settings.json` template supplies that separate scope.
   239	
   240	   The orchestrator retains its current user policy content apart from `failIfUnavailable: true`, `onFailure: "block"`, the required interpreter and PATH bindings and alignment of exclusions with the three control-plane entries. Worker-specific Edit denies and restricted worker cache allowances do not enter this baseline. Administrative sandbox requirements apply to the orchestrator as well as workers.
   241	
   242	   Every generated hook entry carries `onFailure: "block"`. Every generated command hook starts with `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}"` before its trusted installed entrypoint. The prefix re-exports HOME from the launcher environment before any HOME-relative entrypoint path. Host-specific interpreter, private-link-directory, anchored-checkout and tool-directory bindings remain in the per-host rendered guard and rendered worker settings. The formatter and project-map hooks run through the installed orchestrator-only guard and receive the role-specific pinned PATH specified below. Merge evidence identifies hooks appended by the existing modify script and distinguishes them from generated baseline entries. The report accounts for the effective deployed hook set without equating baseline coverage with coverage of runtime-added entries.
   243	
   244	   `tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_orchestrator_settings_keep_existing_policy` compares the merged policy with the preceding baseline and accounts for the specified changes. Repeated merging remains idempotent and preserves unrelated settings.
   245	
   246	4. `home/.chezmoitemplates/claude-worker-settings.json` is the dedicated worker user baseline.
   247	
   248	   It renders the static trusted-path Edit denies, the worktree `.claude` and `.mcp.json` Edit denies, retained native merge denials, empty user `excludedCommands`, `allowUnsandboxedCommands: false`, restricted `allowWrite`, no user Herdr socket allowance and `failIfUnavailable: true` for both Darwin and Linux.
   249	
   250	   Its hooks are limited to agmsg delivery. It contains no formatter, project-map, permgate, orchestrator attachment, Herdr state or worker-write-boundary hook. Tracked project hooks and main-checkout local hooks still load and receive the guard described below.
   251	
   252	   Every worker hook entry carries `onFailure: "block"`. Every command starts with `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}" AGMSG_RESOLVE_PROJECT=0` before the selected absolute shell interpreter and absolute installed agmsg script path. The prefix also re-exports `AGMSG_STORAGE_PATH` when it is set in the launcher environment. Project resolution from a writable `run/proj.<pid>.project` marker remains disabled, so delivery retains the explicit worker path. Descendants inherit this PATH.
   253	
   254	   The worker baseline does not copy the orchestrator's plugins, credential files or current hook arrays. Hook settings reload during a session, so protection is stated as current configuration rather than startup capture. `CLAUDE_CONFIG_DIR` selects the separate user settings directory while project settings continue to apply within the administrative enforcement scope. [Claude settings reference](https://code.claude.com/docs/en/settings)
   255	
   256	   Worker user settings supply no additional socket or exclusion allowance. Their empty lists cannot remove the shared managed Herdr socket or control-plane exclusions.
   257	
   258	5. `home/.chezmoitemplates/claude-managed-settings.json` supplies the administrative sandbox policy.
   259	
   260	   The rendered policy sets `sandbox.enabled: true`, `sandbox.failIfUnavailable: true` and `sandbox.allowUnsandboxedCommands: false`. The last setting makes sandboxing admin-required. Project and local files cannot add sandbox exclusions, socket allowances or other documented relaxations in this scope. Managed Boolean values prevail over lower scopes. User settings remain a separate trusted scope, and arrays such as exclusions have no general managed-only lock. [Repository settings under an admin-required sandbox](https://code.claude.com/docs/en/sandboxing#repository-settings-under-an-admin-required-sandbox)
   261	
   262	   The rendered policy sets `sandbox.filesystem.disabled: false`, `sandbox.enableWeakerNestedSandbox: false`, `sandbox.enableWeakerNetworkIsolation: false`, `sandbox.network.allowAllUnixSockets: false`, `sandbox.network.allowLocalBinding: false` and `sandbox.allowAppleEvents: false`.
   263	
   264	   The rendered `sandbox.excludedCommands` list contains exactly `agmsg-dispatch *`, `herdr-agents *` and `<absolute-home>/.agents/skills/agmsg/scripts/actas-claim.sh *`. These are the orchestrator's three control-plane entries. It contains no `gh *`, `git push *` or authenticated-fetch exemption.
   265	
   266	   The rendered `sandbox.network.allowUnixSockets` list contains exactly the trusted home expansion of `~/.config/herdr/herdr.sock`. This allowance is shared by every seat under managed settings. Per-seat removal is unavailable in that scope, and the worker baseline's empty list does not revoke it.
   267	
   268	   Shared control-plane exclusions are also available in worker sessions. The worker execution rule forbids using them to leave the sandbox. The text treats their availability and the socket's host-execution capability as item 0 residuals rather than enforced per-seat separation.
   269	
   270	   `tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_rendered_policy_requires_admin_sandbox` asserts the rendered content, exact exclusion and socket lists, trusted home expansion and every required Boolean value.
   271	
   272	   `tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_managed_render_is_independent_of_conflicting_project_and_local_settings` supplies project and local fixtures that disable sandboxing, disable startup failure, enable unsandboxed retries, add exclusions and sockets, enable weaker isolation and widen filesystem writes. The trusted managed render remains unchanged. The test verifies configuration scope and content without presenting a simulated settings merger as runtime enforcement.
   273	
   274	6. `Makefile` adds only the `install-managed-settings` target and its `.PHONY` declaration.
   275	
   276	   The target uses the repository's existing rendering facilities to render `home/.chezmoitemplates/claude-managed-settings.json` into `~/.claude/managed-settings.rendered.json`. The staging path is expanded to an absolute path under the user's home.
   277	
   278	   The target selects `/Library/Application Support/ClaudeCode/managed-settings.json` on macOS and `/etc/claude-code/managed-settings.json` on Linux and prints the exact command `sudo install -m 0644 "<absolute-home>/.claude/managed-settings.rendered.json" "<detected-managed-settings-path>"` with the actual staging path and detected destination substituted and shell quoting preserved. The printed command is ready for the operator to run.
   279	
   280	   The target performs no sudo call, administrative installation, live settings application, authentication or session restart. The staging file alone does not establish managed enforcement.
   281	
   282	   `tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_install_target_stages_and_prints_without_running_sudo` covers both macOS and Linux, uses a temporary home, verifies the staged JSON and exact printed command with the detected destination, includes a home path containing spaces and asserts that a planted sudo marker remains absent.
   283	
   284	7. `home/dot_claude-worker/modify_private_settings.json` renders `~/.claude-worker/settings.json` from the dedicated baseline.
   285	
   286	   The script follows the existing chezmoi modify-script interface: current content arrives on stdin and the desired settings object is written to stdout. It uses Python's standard library and the same trusted source and home resolution conventions as the existing renderer.
   287	
   288	   Worker permissions, sandbox policy and hooks managed by this renderer replace stale managed values. Permissive old user exclusions, socket allowances, hook commands and shared cache allowances do not survive as additive worker user policy. The script does not read or copy `~/.claude/settings.json`.
   289	
   290	   Rendering handles empty and malformed input through the repository's existing baseline behavior and is idempotent. It neither reads credentials nor initiates authentication.
   291	
   292	   `tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_settings_replace_stale_policy_idempotently` exercises repeated deployment in temporary homes. `tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_settings_do_not_import_orchestrator_hooks` plants orchestrator hook and plugin markers and verifies their absence.
   293	
   294	8. `home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl` is installed as `~/.claude/hooks/orchestrator-only.sh`.
   295	
   296	   Chezmoi renders the installed guard per host. Its rendered absolute shebang selects the trusted shell interpreter. The host-specific absolute interpreter paths, private executable-link directory, anchored checkout and tool directories are bound inside this rendered guard and the rendered worker settings. The tracked project settings contain none of these paths.
   297	
   298	   The guard compares canonical `CLAUDE_PROJECT_DIR` with the anchored checkout. Equality executes the fixed operation supplied by the caller through the guard's trusted interpreter and anchored-script bindings, subject to the formatter and project-map tool-input check below. Every other launch root exits 0 without executing it. `CLAUDE_PROJECT_DIR` supplies launch identity and never selects an executable.
   299	
   300	   Worker launch roots, sibling worktrees and unrelated checkouts execute no guarded project code. Missing or unresolvable launch-root identity also executes no supplied command. Event cwd does not change the launch-root decision.
   301	
   302	   The guard also binds the formatter and project-map reload to the edited file path from the hook's tool input and its owning repository. When the resolved path is outside canonical `CLAUDE_PROJECT_DIR` or belongs to a worker repository under `.claude/worktrees/`, the guard exits 0 without running the command. Worker-repository configuration, including Prettier JavaScript configuration and ruff settings, is never consumed by an orchestrator hook.
   303	
   304	   The guard preserves argument boundaries, stdin and child exit status. It performs no eval, PATH interpreter lookup or worktree-relative script selection. Its portable caller starts with `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}"` followed by `"$HOME/.claude/hooks/orchestrator-only.sh"` and a fixed operation identifier with its arguments. The shell running the hook expands `$HOME`. The prefix re-exports `HOME` from the launcher environment as `HOME="$HOME"` before any path that uses it and explicitly re-exports the launch identity and the few variables Claude Code documents for hooks. No interpreter or anchored script path is supplied by the tracked settings.
   305	
   306	   The pinned PATH differs by role. Worker-session hooks use `/usr/bin:/bin`. For the orchestrator's formatter and project-map hooks, which the guard runs only in orchestrator sessions, the guard itself sets PATH to a rendered list of absolute tool directories of the trusted root before executing the guarded command. Those directories hold `ruff`, `prettier` and `terminal-browser` and are resolved by the render from the manifest without using mise shims. The formatter and project-map scripts remain outside `allowed_files` and unchanged.
   307	
   308	   `tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_project_guard_uses_launch_root_and_never_runs_worker_payloads` plants worker Stop, contextdb and formatter payloads. Worker and unrelated-root invocations leave all markers absent. The positive-path case runs the complete rendered command in a subprocess with a fake `CLAUDE_PROJECT_DIR` equal to the anchored checkout and asserts that the guarded script executed while preserving its arguments and status. A second case runs the complete rendered command with a worktree `CLAUDE_PROJECT_DIR` and asserts that the guarded script did not execute. A planted `BASH_ENV` in the outer environment remains unexecuted in both cases. Formatter and project-map reload cases keep `CLAUDE_PROJECT_DIR` anchored and supply hook tool input for an outside file and a worker-repository file under `.claude/worktrees/`; both exit 0 with command and planted configuration markers absent. Matching anchored-file inputs run both commands normally. The guard tests execute the portable HOME-relative hook command against separately rendered per-host guards, assert the `HOME="$HOME"` re-export and verify that interpreter and anchor selection occurs only inside the rendered guard. Changing `CLAUDE_PROJECT_DIR` never changes the selected executable.
   309	
   310	9. `.claude/settings.json` retains its tracked project hooks and rewrites every command through the installed orchestrator-only guard.
   311	
   312	   This tracked file is not a chezmoi template and remains portable across hosts. Every command starts with `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}"` followed by `"$HOME/.claude/hooks/orchestrator-only.sh"` and a fixed operation identifier with its arguments. The shell running the hook expands `$HOME`, and the clean environment re-exports the launcher's HOME before any path that uses it. The file names no interpreter, anchor path, private links directory or host-specific tool directory.
   313	
   314	   Host-specific absolute bindings live only inside the per-host rendered guard and rendered worker settings. The guard binds the selected operation to its absolute interpreter and anchored script path. Contextdb commands do not invoke bare `python3` or select `.claude/hooks` from a worker checkout. The Stop gate does not invoke bare `bash` or a worker checkout's `scripts/agent-stop-gate.sh`. `CLAUDE_PROJECT_DIR` never selects an executable.
   315	
   316	   Every hook entry carries `onFailure: "block"`. Existing event functions remain available to the anchored orchestrator. They are no-ops in worker sessions because the guard rejects their launch roots.
   317	
   318	   `tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_every_tracked_project_hook_is_guarded_and_blocks_on_failure` traverses every event, matcher and command entry. It rejects unguarded commands, missing failure policy, missing `/usr/bin/env -i` prefixes with the specified HOME re-export, interpreter or anchor paths in the tracked file and worker-selected executable paths. Render fixtures use distinct homes and anchors and assert that the tracked commands stay identical while the guard and worker settings receive their own host bindings.
   319	
   320	10. `home/dot_local/bin/common/executable_herdr-agents` supplies the dedicated worker configuration at the actual worker launch boundary.
   321	
   322	    Every Claude worker pane starts with `CLAUDE_CONFIG_DIR=<absolute-home>/.claude-worker`. This value reaches the actual worker process through the pane command and environment construction. Setting it only in the parent spawn process does not satisfy this requirement.
   323	
   324	    Managed-workspace and standalone-worker routes receive the same binding. Repeated starts do not inherit a conflicting caller Claude configuration directory. This task introduces no worker gh configuration directory, gh templates or credential-separation claim.
   325	
   326	    Every worker launch exports `UV_CACHE_DIR=<absolute-worktree>/.uv-cache` and `UV_PYTHON_INSTALL_DIR=<absolute-worktree>/.uv-cache/python`. Both worker kinds receive values derived from the selected canonical worktree. Caller-provided values do not replace them.
   327	
   328	    The launcher stops writing Claude worker delivery hooks and merge denials into worktree-local `.claude/settings.local.json`. It renders the worker delivery hooks and native merge denials into `~/.claude-worker/settings.json`, the user-level settings file selected for that directory.
   329	
   330	    Before every Claude worker start, the launcher also migrates the legacy worktree-local file. Claude Code loads the worktree's own `.claude/settings.local.json` alongside the main checkout's local settings, so a previously generated delivery entry there would stay effective with its unsanitized environment and PATH-resolved interpreter. The launcher removes every managed delivery hook entry it previously wrote from `<worktree>/.claude/settings.local.json`, keeps that file's unrelated entries, and refuses to start the worker while a command hook it did not write remains there, naming the entry. The effective hook set is asserted across the three files Claude Code loads for a linked worktree (worker user settings, the main checkout's local settings, the legacy worktree-local file) with a fixture holding a previously generated unsanitized entry: `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_add_worker_migrates_legacy_worktree_local_hooks` is red at the base and green on the final head.
   331	
   332	    Before every Claude worker start, managed worker delivery entries are regenerated from trusted inputs. An existing delivery match does not skip preparation. Stale managed commands are replaced, unknown command hooks are not promoted into the trusted delivery set and the effective delivery set contains no duplicate managed invocation.
   333	
   334	    The launcher also regenerates its managed hooks in the main checkout's `.claude/settings.local.json`. Every local agmsg delivery and orchestrator attachment command that it writes runs through the installed orchestrator-only guard. The existing permissions object and unrelated non-hook settings remain stored. Their effective sandbox interpretation follows the administrative managed policy.
   335	
   336	    Every command hook in both `~/.claude-worker/settings.json` and the main checkout's `.claude/settings.local.json` starts with `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}"`. Worker user settings contain their per-host rendered absolute interpreter and script bindings. Main-local commands invoke `"$HOME/.claude/hooks/orchestrator-only.sh"` with fixed operation identifiers, leaving host-specific executable bindings inside the rendered guard. The prefix removes inherited `BASH_ENV` before Bash starts and explicitly re-exports the launch identity and documented hook variables. Agmsg delivery prefixes additionally re-export `AGMSG_RESOLVE_PROJECT=0` and `AGMSG_STORAGE_PATH` when the latter is set in the launcher environment, so the clean environment does not re-enable project resolution from the writable `run/proj.<pid>.project` marker. Every entry carries `onFailure: "block"`. Main-local hooks loaded by a worker session execute no guarded payload.
   337	
   338	    Worker settings retain existing native merge denials. They add no user excluded commands, Herdr socket allowance, unsandboxed requests or orchestrator hooks. Shared managed exclusions and socket access remain effective.
   339	
   340	    Codex launches retain their existing `--sandbox workspace-write` and `--ask-for-approval never` arguments unchanged. This task changes no Codex worker profile or network-policy source and adds no network-policy test.
   341	
   342	    The retained Codex Git grant permits shared `.git/objects`, `.git/refs`, `.git/logs` and the worker's administration directory. It does not authenticate local ledger content and is not represented as a host security boundary.
   343	
   344	    `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_every_worker_launch_receives_dedicated_policy_and_private_caches` covers both worker kinds and all launch routes. `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_repeated_worker_start_replaces_stale_managed_hooks` covers repeated preparation.
   345	
   346	    `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_launch_adds_no_unsandboxed_route` checks that worker launch construction adds no outside-sandbox command route, worker user exclusions or socket allowances and retains native merge denials. It separately records the shared managed exceptions and does not claim that empty user arrays remove them.
   347	
   348	    `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_linked_worktree_uses_worker_user_hooks_and_guarded_main_local_hooks` asserts that worker hooks are written to worker user settings, worker preparation writes no worktree-local settings file and main-local agmsg and attachment hooks execute no payload under a worker launch root. An anchored orchestrator invocation still reaches the expected fixture payloads.
   349	
   350	    `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_every_settings_hook_has_system_path_prefix` exhaustively traverses both settings files after initial preparation and repeated starts. It asserts the literal `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}"` prefix on every command hook, checks the split between absolute bindings in rendered worker settings and HOME-relative main-local guard calls, and asserts that a planted `BASH_ENV` in the hook's inherited environment does not run. The planted-`BASH_ENV` case is red against the current PATH-only form. The test also asserts `AGMSG_RESOLVE_PROJECT=0` in every agmsg delivery prefix and preservation of `AGMSG_STORAGE_PATH` when set in the launcher environment. It invokes the delivery resolver through the rendered prefix with an explicit worker path and a conflicting writable `run/proj.<pid>.project` marker and asserts that the resolver retains the explicit worker path.
   351	
   352	11. `home/dot_local/bin/common/executable_herdr-agent-state.sh` provides the repository-owned Herdr state helper installed as `~/.local/bin/common/herdr-agent-state.sh`.
   353	
   354	    The currently installed `~/.claude/hooks/herdr-agent-state.sh` is generated by Herdr and is not a tracked source in this repository. Its bare `python3` descendant is not retained as a trusted worker hook. The repository-owned helper preserves the required state-reporting function and receives its absolute Python interpreter through the rendered invocation.
   355	
   356	    Every hook command reaches a selected absolute interpreter and absolute script path through trusted installed bindings. The tracked settings name only the HOME-relative guard and fixed operation identifiers. Host-specific interpreter and anchor bindings reside inside the per-host rendered guard or rendered worker settings. Repository-owned shell descendants use absolute shebangs or explicit absolute shell invocations. Python descendants use the selected absolute interpreter with `-I`.
   357	
   358	    Upstream agmsg scripts retain their `/usr/bin/env bash` shebangs and direct calls to other installed agmsg scripts. The `PATH=/usr/bin:/bin` supplied by the delivery hook's `/usr/bin/env -i` prefix propagates to those descendants, so their Bash resolution uses the system directories without reaching host shims. The installed upstream files are neither edited nor vendored.
   359	
   360	    The delivery inventory names `~/.agents/skills/agmsg/scripts/session-start.sh`, `~/.agents/skills/agmsg/scripts/session-end.sh`, `~/.agents/skills/agmsg/scripts/check-inbox.sh`, `~/.agents/skills/agmsg/scripts/identities.sh` and every additional delivery descendant actually reached.
   361	
   362	    The inventory records source ownership, installed path, caller, entrypoint interpreter and inherited PATH for each reached script. Binding only the first command does not establish descendant coverage.
   363	
   364	    The inventory separately records the current `storage.sh` route from writable team configuration to driver sourcing. A `drivers.partition` value such as `../../../db/payload` can select a planted driver file during unsandboxed delivery. Fixed PATH does not mitigate that selection. The upstream fix belongs to `dotfiles-T133-agmsg-hardening-a01` as recorded in the acceptance record's ownership section.
   365	
   366	    No worker hook added by this task introduces store-derived driver sourcing beyond the behavior of the currently installed agmsg scripts. This task neither implements nor claims the upstream validation.
   367	
   368	    `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_hook_descendants_do_not_execute_path_interpreters` executes the fixture hook routes with planted Python and Bash shims. It includes a directly executed descendant with an `/usr/bin/env bash` shebang, checks descendant markers and records actual interpreter identities and inherited PATH. Capturing launcher command strings alone does not satisfy this test. Its result does not close the store-driver residual.
   369	
   370	12. `home/dot_agents/skills/agmsg-orchestration/SKILL.md` changes only the Worker Playbook step 4 sentence that lists outside-sandbox worker commands.
   371	
   372	    The replacement sentence is: “Every worker command, including gh, git push and authenticated git fetch, runs inside the worker's sandbox; no worker command runs outside it.”
   373	
   374	    This sentence governs worker execution. Historical TLS, keyring, artifact-writing and delivery exceptions elsewhere in the playbook provide no authorization to leave the sandbox. Shared managed control-plane exceptions provide no worker authorization either. An unavailable operation produces a blocked PONG with its exact command and boundary.
   375	
   376	    `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_playbook_requires_every_command_inside_sandbox` checks the replacement and removal of the former three-command exception sentence.
   377	
   378	13. `.gitignore` adds only `.uv-cache/`.
   379	
   380	    Section 5.14 item 9 fixes trusted orchestrator consumers to `UV_CACHE_DIR=<anchored-checkout>/.agents/worklog/uv-cache`, places managed Python installations beneath that cache and uses `--offline`. Those consumers execute no dependency content from worker caches, shared uv caches or mise caches. Their owning hardening tasks implement the consumer changes.
   381	
   382	    This task's static deny inventory explicitly protects both `.agents/worklog/**` and `.agents/worklog/uv-cache/**` beneath the anchored checkout. Their gitignored status does not remove them from the inventory.
   383	
   384	    This task's hooks use standard-library Python and absolute shell interpreters without uv. The existing `.agents/worklog/` ignore covers the orchestrator cache.
   385	
   386	14. The five allowed test modules reuse existing render, merge, fake-launcher and temporary-HOME fixtures.
   387	
   388	    Tests are written before implementation and retain identified base-failure and implementation-success evidence. A missing new entrypoint supplies its baseline failure.
   389	
   390	    Worker settings tests cover both platforms, exact static manifest correspondence, current-checkout filesystem coverage, every protected path category, directory targets, descendants, both worklog patterns, ordinary worktree writes, the worktree `.claude` and `.mcp.json` denies, writable agmsg stores, stale settings and the absence of the removed boundary hook.
   391	
   392	    Managed settings tests cover the exact rendered policy, conflicting project and local sandbox relaxations, shared control-plane exclusions, shared Herdr socket access and staging without privileged execution. They distinguish worker user settings from the effective shared policy.
   393	
   394	    Path fixtures cover symlink components and filesystem case aliases. They verify inventory and configuration identities without presenting a simulated permission matcher as proof of Claude runtime enforcement.
   395	
   396	    Hook tests cover every generated and tracked entry's failure policy, worker user settings, guarded main-local settings, the `/usr/bin/env -i` prefix with explicit hook-variable re-exports, complete rendered-command positive and worktree-negative cases, role-specific pinned PATH bindings, suppression of a planted inherited `BASH_ENV` and actual descendant execution. They distinguish synchronous policy hooks from background delivery and post-action events.
   397	
   398	    `onFailure: "block"` requires Claude Code v2.1.295 or later and has no enforcement effect on background hooks or the documented excluded events. [Claude hook failure reference](https://code.claude.com/docs/en/hooks#block-the-action-when-a-hook-fails)
   399	
   400	    Tests create no identities, initiate no login and access no real credential store. No fixture result is represented as proof of credential isolation, live managed enforcement or upstream agmsg hardening.
   401	
   402	15. `.orchestration/dotfiles-T133-worker-write-boundary-a01/` contains the byte-identical dispatched `task.md`, `report.md`, `validation.md`, `sandbox.md`, `learning.md`, `autoskill.md` and worker review evidence.
   403	
   404	    The report maps each of the third C-80 review's five findings, fourth C-80 review's six findings and fifth C-80 review's three findings to the revised mechanism, its tests and its remaining residual or owning task. It distinguishes policy configuration from live enforcement and deployment.
   405	
   406	The guard source is `home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl`: chezmoi renders the guard from its .tmpl source with the per-host absolute interpreter, anchored-checkout and tool-directory paths at apply time (a plain `executable_` source would be copied without expansion), and the render test renders the template with the test host values and asserts the paths it contains.
   407	
   408	The doc test `tests/unit/test_agmsg_orchestration_docs.py` asserts the exact step 4 sentence this task rewrites (lines 200-201 at the base); the assertion follows the new sentence, nothing else in that module changes; PR #427 (P1-8) edits the same module and merges before this pull request, which rebases onto it before its first push.
   409	
   410	## Out of scope
   411	
   412	The Codex worker profile change `sandbox_workspace_write.network_access=true` belongs to the separate task `dotfiles-T133-codex-worker-network-a01` for a Claude seat. This task contains no implementation, threat row or test for that change. This Codex seat edits no Codex-boundary source. The operator step for the deterministic Codex permgate policy remains named below.
   413	
   414	The worker-write-boundary Python hook, its hook entries and `tests/unit/test_worker_write_boundary.py` are dropped. The gh-trusted wrapper remains dropped. The worker gh configuration directory, its templates and the dedicated-identity implementation are removed from this task.
   415	
   416	D-024-23 establishes that `GH_CONFIG_DIR` does not separate same-macOS-user Keychain access. A separate OS user or host is required for prevention of worker-initiated merges. Future P1-16 remains the operator's decision. This task implements no credential-separation substitute.
   417	
   418	The permission guard and merge gate remain P1-14 a05's work. P1-14 a05 and P1-6 implement the regime rule that approvals and gate evidence of record come from GitHub at a SHA through its API inside the sandbox. The GitHub boundary is detection, not prevention.
   419	
   420	For the committed approval ledger, the regime obtains the commit SHA returned by `git ls-remote origin refs/heads/main` and reads `gh api repos/<owner>/<repo>/contents/.orchestration/decisions.tsv?ref=<sha>` inside the sandbox. The consuming implementation reads the API response's file content at that exact SHA. It does not fall back to local files, local refs or local object traversal.
   421	
   422	A working-copy decision remains a proposal until its record PR reaches main. This task writes no approval row and implements no local-object substitute for GitHub authority. Shared credentials can still authorize a worker-initiated merge. P1-11 owns the next-records-PR regime check for missing acceptance or gate evidence under section 5.14 item 0's detection rule.
   423	
   424	The upstream agmsg driver-selection fix belongs to `dotfiles-T133-agmsg-hardening-a01`. Its recorded scope validates the `drivers.partition` driver name as an allowlisted basename without path separators before sourcing and supplies an adversarial red-then-green test. This task leaves the shared stores writable and records the current sourcing route as a residual. The ownership section identifies that upstream task as a task to be written; this text does not claim that its fix or test exists.
   425	
   426	Permgate code and deterministic policy remain the operator's responsibility. The worker prepares the operator step that stops the Codex permgate policy from approving sandbox escapes. The worker performs no live policy edit or escape probe.
   427	
   428	The operator logs into Claude once with `CLAUDE_CONFIG_DIR=<absolute-home>/.claude-worker` selected. The Claude Keychain entry is keyed to that directory. This Claude login does not authenticate or isolate gh.
   429	
   430	Administrative installation of `/Library/Application Support/ClaudeCode/managed-settings.json` on macOS and `/etc/claude-code/managed-settings.json` on Linux is the operator's step. The worker implements rendering, staging and the printed installation command without running sudo or installing live managed settings.
   431	
   432	The documented file-tool checks reduce symlink redirection risk. A same-UID process can race filesystem changes, alter host-local state or execute outside a seat sandbox. The remaining interval between permission checks and path consumption is a residual under section 5.14 item 0. This text makes no claim that the worker could already write every redirected target directly.
   433	
   434	The managed Herdr socket allowance stays available to every seat. Per-seat socket removal is unavailable in that shared scope. Shared control-plane exclusions, socket RPC, hooks, approved MCP processes and other processes outside every seat sandbox retain their stated host trust. The configuration is not represented as same-UID adversarial isolation.
   435	
   436	`onFailure: "block"` supplies runtime failure behavior where Claude supports it. Python exit-status tests do not establish timeout handling by the runtime. Background hooks and events on which the field has no effect perform no security enforcement in this design.
   437	
   438	Consuming-helper snapshots, reservation locks, the common trusted-execution test helper and orchestrator review-worktree relocation remain with their owning hardening tasks. Codex writable-root grants remain unchanged.
   439	
   440	The worker edits neither `.orchestration/decisions.tsv` nor other tasks' canonical texts, evidence or acceptance records, apart from the explicitly named deletion of the predecessor's task-file copy. It performs no authentication change, keyring mutation, ruleset mutation, administrative installation, live settings application, global installation, operator restart or merge.
   441	
   442	## Check
   443	
   444	`make render-check` and `make validate-agent-assets` pass. The task's own files pass the `make format` flags: `shfmt -i 4 -sr --diff`, `ruff format --config ruff.toml --check` and `prettier --check`.
   445	
   446	The clean base `205fe85c` has an inherited formatting failure on 12 out-of-scope files: ten archived task shell sources, `project-map-reload.sh` and `brew.bats`. The inherited failure is reproduced against that unchanged base and disclosed in `validation.md` with its exact output and per-file exit statuses. This clause authorizes no out-of-scope repair.
   447	
   448	Shellcheck and shfmt cover the changed shell sources, including the launcher, orchestrator-only guard and repository-owned Herdr state helper. Added or changed shell comments use English shdoc-compatible annotations. Changed Python receives the repository's Python formatting and lint checks.
   449	
   450	`uv run python -m unittest tests.unit.test_generate_agent_configs tests.unit.test_claude_settings_merge tests.unit.test_herdr_agents tests.unit.test_claude_worker_settings tests.unit.test_claude_managed_settings -v` is green. The validation record contains every named red-then-green selector and the complete final module run.
   451	
   452	The final diff has at most 700 changed lines outside `tests/` and `.orchestration/`, excluding the regenerated `home/.chezmoitemplates/claude-settings-managed.json`, `home/.chezmoitemplates/claude-worker-settings.json` and `home/.chezmoitemplates/claude-managed-settings.json`. It has at most 800 changed lines under `tests/`. Changed lines are additions plus deletions. The validation record includes per-file numstat, base and head identities and both totals.
   453	
   454	The validation record contains exact commands, verbatim outputs, exit statuses and tested identities. Git commands producing that evidence follow section 5.14 item 2.
   455	
   456	Both platform renders show separate worker and orchestrator user settings, exact manifest deny-inventory correspondence, filesystem coverage of current tracked top-level source paths, both worklog denies, ordinary worktree writes, the worktree `.claude` and `.mcp.json` denies, narrow home denies, writable agmsg stores, empty worker user exclusions, restricted worker writes and `failIfUnavailable: true` for every Claude seat.
   457	
   458	Managed render evidence asserts sandbox enablement, startup failure, disabled unsandboxed retries, the required anti-weakening Boolean values, exactly the three rendered control-plane exclusions and exactly the Herdr socket allowance. Conflicting project and local fixtures leave that render unchanged. The evidence names the documented enforcement scope without claiming live runtime verification.
   459	
   460	Staging evidence shows the home-directory output and exact printed `sudo install -m 0644` command with the detected administrative destination on both macOS and Linux. The temporary-HOME test proves that the target executes no sudo command.
   461	
   462	Hook evidence inventories every generated and tracked entry, its `onFailure` value, `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}"` prefix, installed script, absolute entrypoint interpreter and reached descendants. It states the portable tracked-command and per-host-rendered-binding split, verifies HOME re-export before HOME-relative paths and shows that tracked commands name no interpreter or anchor path. It includes worker user settings and main-checkout local settings. Render evidence shows that `ruff`, `prettier` and `terminal-browser` resolve under the guard's rendered orchestrator tool PATH on the rendering host and that no PATH entry is a shims directory. Merged-settings evidence identifies runtime-added entries separately. No report claims complete effective failure-policy coverage from template inspection alone.
   463	
   464	Launch evidence shows both cache variables reaching the actual worker process on every route. Claude processes additionally receive the dedicated Claude configuration directory. Repeated-start evidence shows replacement of stale managed hooks, retained native merge denials and the unchanged Codex sandbox and approval arguments.
   465	
   466	Linked-worktree evidence shows worker hooks in the worker configuration directory's user settings and no new worker-local `.claude/settings.local.json`. Guard markers show that the main checkout's local agmsg and attachment hooks execute no payload under worker launch roots.
   467	
   468	Guard markers also show that worker project scripts, contextdb hooks, Stop gates and formatter payloads do not execute through tracked hooks. Descendant markers show that planted PATH interpreters do not execute on the tested hook routes, including an upstream-style `/usr/bin/env bash` descendant.
   469	
   470	The report separately identifies the writable agmsg store's current driver-selection route and `dotfiles-T133-agmsg-hardening-a01` ownership. Hook interpreter tests do not claim to close that residual.
   471	
   472	The report states the GitHub API ledger rule without claiming this task implements the permission guard or the P1-11 next-records-PR regime check. It states detection, not prevention, and records D-024-23's future P1-16 decision. It also records shared managed exclusions and Herdr socket access, same-UID credential access, path-consumption residuals, external-process trust, hook-event failure limitations and the retained Codex shared Git grant.
   473	
   474	No local Bats tests run. Required Bats results come from GitHub Actions. Failed required checks retain their actual output and receive an in-scope fix before RESULT.
   475	
   476	The orchestrator runs `uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py .orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md` before dispatch and at acceptance. C1 to C10 and C7b pass.
   477	
   478	A C-80 security-profile context reviews this complete revised text before dispatch. That review is a dispatch prerequisite and is not claimed as a result of this draft.
   479	
   480	## Completion
   481	
   482	One implementation PR continues the existing branch `tools/worker-write-boundary-a01`, created from clean base `205fe85c`, on the Codex seat a010. The eight green tests, fixtures and evidence stay. The first push deletes the predecessor copy `.orchestration/dotfiles-T133-worker-write-boundary-a01/task.md` and adds the byte-identical dispatched a02 task at `.orchestration/dotfiles-T133-worker-write-boundary-a01/task.md`. This predecessor-copy deletion is the sole authorized edit to the predecessor's artifact directory.
   483	
   484	The Completion clauses of `.orchestration/tasks/dotfiles-T133-permission-guard-gate-a05.md` apply with this task's branch, files and evidence paths, `dotfiles-T133-worker-write-boundary-followup-a01` as the owner of any advisory P2, and `task_copy=<sha256 of .orchestration/dotfiles-T133-worker-write-boundary-a01/task.md>` in RESULT. The a05-specific continuation of PR #420, predecessor-copy deletion, inherited counters, deadline and implementation requirements do not transfer. The orchestrator writes the follow-up owner task before assigning its first advisory P2.
   485	
   486	Every worker-side fix round counts toward INV-6. The worker's own pre-push review is one round at most. A surviving P0/P1 is sent in RESULT as open and stops integration. The worker starts no additional private correction-and-review cycle to avoid reporting it.
   487	
   488	No `@codex review` comment is posted. Automatic final-head reviews are observed within the bounded 15-minute window, and absence is recorded as `bot: none`. Required GitHub Actions checks pass before RESULT. Every feedback item carries its proposed disposition, and surviving P0/P1 findings remain open for the operator's decision.
   489	
   490	Every gh write and every git write runs as a separate command without shell chaining. Every worker command remains inside its sandbox. An operation that cannot complete there produces a blocked PONG with the exact command and boundary.
   491	
   492	The Codex worker writes evidence at the required relative paths in its own worktree and says so in RESULT. Worker review evidence uses the `-worker-` infix. Crit-data evidence and its receipt follow repository rules without a browser review or human review request. The orchestrator copies evidence by absolute path before acceptance.
   493	
   494	`AGMSG-RESULT v1` names the final head, base, branch, changed files, new deployable scripts, source and installed paths, trusted anchor, interpreter and descendant inventory, hook PATH bindings, user and administrative settings destinations, staging path and printed installation command, Bot findings and proposed dispositions, open P0/P1 findings, exact test selectors, measured caps, task-copy SHA256 and evidence paths. It distinguishes historical observations from final-head results and names all pending operator steps.
   495	
   496	The report states the user-visible effects. Claude workers use `~/.claude-worker` and require its own Claude login. Worker trusted-path and worktree-configuration Edit denies also affect Bash sandbox writes. Agmsg store paths remain writable except `~/.agents/skills/agmsg/db/trusted-plugins`, and worker denies also cover `~/.agents/skills/agmsg/plugins/**`. Worker user settings add no excluded commands or Herdr socket allowance, while shared managed settings retain the three control-plane exclusions and Herdr socket for every seat. Tracked and main-local orchestrator project hooks are no-ops in worker sessions. Worker caches are private. Every Claude seat fails when its sandbox is unavailable.
   497	
   498	Administrative managed settings require sandboxing for the orchestrator as well as workers and disable unsandboxed retries. The former Linux gh exemption is removed. The orchestrator retains its existing functions within those requirements and the specified hook failure, guarding and interpreter/PATH-binding changes.
   499	
   500	The report states that no gh credential separation is established. Shared credentials permit worker-initiated API merges despite native command denials. The GitHub boundary is detection, not prevention, with the required next-records-PR regime check owned by P1-11.
   501	
   502	This task is `security: true`. The orchestrator obtains the task-level audit and a separate security-profile review of the final implementation head. The finding-class record includes `decision-not-bound-to-execution`, `unbound-evidence` and `fail-open-on-error`. A third non-advisory finding of one class stops the artifact for redesign under the inherited completion rules.
   503	
   504	Final-head feedback collection, task-level audit, finding dispositions, acceptance and the integration gate follow Orchestrator Playbook step 10 in its prescribed order. The gate receives `PR_FEEDBACK_EVIDENCE`, `AUDIT_EVIDENCE`, `ACCEPTANCE_EVIDENCE` and the agent review receipt. Changed heads receive fresh required evidence. The final-head security review precedes the gate.
   505	
   506	The permission-surface change receives the required operator-backed approval through the repository's existing process. The worker writes no approval row and treats no candidate-tree decision as authority.
   507	
   508	Live deployment is the operator's post-merge `make update`. The operator runs `make install-managed-settings`, inspects the rendered staging file and executes its printed `sudo install -m 0644 "<absolute-home>/.claude/managed-settings.rendered.json" "<detected-managed-settings-path>"` command with `/Library/Application Support/ClaudeCode/managed-settings.json` detected on macOS and `/etc/claude-code/managed-settings.json` detected on Linux. Administrative installation is recorded separately from staging and ordinary chezmoi application.
   509	
   510	The operator performs the Claude worker-directory login with `CLAUDE_CONFIG_DIR=<absolute-home>/.claude-worker` selected.
   511	
   512	The operator applies the prepared deterministic Codex permgate rule that stops approving sandbox escapes and restarts affected sessions.
   513	
   514	The deployment record checks effective settings after `make update` and administrative installation, including hooks added by merge scripts or integration installers. It verifies the installed managed-settings content, admin-required sandbox scope, worker directory, both platform policy outputs, static deny inventory, worktree-configuration denies, writable agmsg stores, worker-user and main-local hook placement, hook PATH and interpreter descendants, failure-policy coverage and sandbox startup without exposing credentials.
   515	
   516	The effective-settings check includes conflicting project and local sandbox relaxations and confirms that they do not weaken the administrative policy. It also records the shared control-plane exclusions and Herdr socket as available capabilities. It makes no claim that worker user arrays subtract those entries.
   517	
   518	Merge alone does not establish deployment readiness. The orchestrator records `make update`, the managed-settings installation with sudo, the Claude worker-directory login, effective startup checks and the Codex permgate rule before releasing dependent hardening tasks for live operation. The upstream agmsg store-driver route remains a named residual until its owning task is implemented. GitHub remains detection, not prevention, until the operator pursues separate-user or separate-host isolation under future P1-16.
   519	
   520	## Checks (pasted by the orchestrator before each send)
   521	
   522	```
   523	2026-10-19T05:42Z dispatch 1: C-80 rounds 1-8 incorrect, round 9 correct (…-text-security-435275a)
   524	2026-10-19T06:2xZ amendment 1: task=dotfiles-T133-worker-write-boundary-a01 tasks=1 amendments=0 questions=0(the two questions came as status=running question=N, C-87) results=0 withdrawn=0 revises=0 source=live; C-80 of this amended text: (pasted after its review)
   525	```
   526	
   527	Local Bats, live enforcement, administrative installation, worker-directory login, permgate policy changes and deployment are not performed by the worker.
   528	Deployment remains unverified until the operator completes the post-merge steps; same-UID credential access, shared control-plane exclusions and Herdr socket access, writable-store driver selection and concurrent path consumption remain stated residuals.
 succeeded in 378ms:
{
  "lastAnalyzedAt": "2026-10-02T14:12:51Z",
  "gitCommitHash": "940a3a2b07adfd14140a0acff96784ef53a0a509",
  "version": "1.0.0",
  "analyzedFiles": 368
}

[{"name": "agent-config.yaml", "filePath": "home/dot_agents/agent-config.yaml", "summary": "Canonical hand-edited manifest for Codex and Claude Code: model profiles (express/standard/review/deep/security/audit/adh), herdr-agents worker kind/profile/worktree, Codex and Claude settings, sandboxes, permissions, hooks, plugins, disabled-by-default MCP servers, and pinned install assets. All agent-native config files are rendered from it."}, {"name": "permgate-policy.yaml", "filePath": "home/dot_agents/permgate-policy.yaml", "summary": "Policy for the permgate PermissionRequest hook: shadow-only LLM classifier providers, read-deny patterns for secrets, layered deny/workspace-write/allow decisions, regex allowlists for read-only gh/git/process/version commands, a catastrophic rm deny rule, enablement latency thresholds, and observed fallthrough metrics."}, {"name": "executable_permgate", "filePath": "home/dot_local/bin/common/executable_permgate", "summary": "uv-run Python PermissionRequest hook and CLI for Claude Code, Codex, and normalized CLI actions that applies deterministic deny/allow patterns and workspace rules first, optionally consults a shadow LLM classifier on metadata only, and logs every decision to a JSONL state file."}, {"name": "load_policy", "filePath": "home/dot_local/bin/common/executable_permgate", "summary": "Loads and strictly validates the schema-v2 permgate policy (providers, categories, patterns, classifier actions, CLI rules)."}, {"name": "request_parts", "filePath": "home/dot_local/bin/common/executable_permgate", "summary": "Normalizes a hook payload into tool name, tool input, and the text matched by patterns."}, {"name": "hook_output", "filePath": "home/dot_local/bin/common/executable_permgate", "summary": "Builds the PermissionRequest hookSpecificOutput decision object."}, {"name": "classifier_schema", "filePath": "home/dot_local/bin/common/executable_permgate", "summary": "Builds the JSON schema the LLM classifier must answer with (category, confidence)."}, {"name": "classification_subject", "filePath": "home/dot_local/bin/common/executable_permgate", "summary": "Derives normalized, value-free metadata for classifiable read-only gh/git actions, or None."}, {"name": "parse_classification", "filePath": "home/dot_local/bin/common/executable_permgate", "summary": "Validates classifier output against provider thresholds, categories, and the subject action."}, {"name": "classify", "filePath": "home/dot_local/bin/common/executable_permgate", "summary": "Runs the claude or codex CLI as a one-shot schema-constrained classifier over normalized metadata and returns its parsed result, latency, and status."}, {"name": "decision_record", "filePath": "home/dot_local/bin/common/executable_permgate", "summary": "Builds the redacted decision log record for a request."}, {"name": "strict_candidate_path", "filePath": "home/dot_local/bin/common/executable_permgate", "summary": "Resolves a CLI action path strictly relative to an absolute cwd, rejecting traversal and unsafe symlinks."}, {"name": "cli_read_decision", "filePath": "home/dot_local/bin/common/executable_permgate", "summary": "Decides allow or deny for a CLI read path against the read pattern list."}, {"name": "cli_workspace_decision", "filePath": "home/dot_local/bin/common/executable_permgate", "summary": "Applies workspace-write rules for normalized CLI actions when enabled by policy."}, {"name": "decide", "filePath": "home/dot_local/bin/common/executable_permgate", "summary": "Core decision pipeline: deterministic deny, workspace, allow patterns, then optional shadow or enabled LLM classification, returning hook output and a log record."}, {"name": "cli_payload", "filePath": "home/dot_local/bin/common/executable_permgate", "summary": "Converts a normalized CLI action (bash/read/write/edit) into a hook-style payload with strict validation."}, {"name": "run_cli", "filePath": "home/dot_local/bin/common/executable_permgate", "summary": "Handles the `cli` mode: parses a normalized action, decides, logs, and prints the decision."}, {"name": "run_bench", "filePath": "home/dot_local/bin/common/executable_permgate", "summary": "Benchmarks decision latency over fixed gh/git fixtures and prints p50/p95 statistics."}, {"name": "main", "filePath": "home/dot_local/bin/common/executable_permgate", "summary": "Entry point dispatching hook, cli, and bench modes, guarding against recursion via the sentinel env var."}, {"name": "generate-agent-configs.py", "filePath": "scripts/generate-agent-configs.py", "summary": "Generator that renders agent-native configuration (Codex config.toml, Claude settings/sandbox/MCP, plugin marketplace, model-profile TOML and modify scripts, profiles env, express-explorer agent, asset pin constants) from home/dot_agents/agent-config.yaml, with --check and --set-asset modes."}, {"name": "parse_manifest", "filePath": "scripts/generate-agent-configs.py", "summary": "Parses the agent manifest YAML with PyYAML, failing clearly when PyYAML is missing or the document is not a mapping."}, {"name": "quote_toml", "filePath": "scripts/generate-agent-configs.py", "summary": "Serializes Python scalars, lists, and tables into TOML literal syntax."}, {"name": "model_profiles", "filePath": "scripts/generate-agent-configs.py", "summary": "Validates the model_profiles mapping (required express/standard profiles, claude/codex fields) and returns it."}, {"name": "set_asset_field", "filePath": "scripts/generate-agent-configs.py", "summary": "Rewrites one scalar under assets.<name> in the manifest text while preserving comments and layout."}, {"name": "render_asset_constants", "filePath": "scripts/generate-agent-configs.py", "summary": "Rewrites each asset's NAME=\"...\" pin assignment in its render target file (e.g. installer-pins.sh), enforcing plain pin values and exactly one assignment."}, {"name": "render_codex", "filePath": "scripts/generate-agent-configs.py", "summary": "Renders the managed Codex config.toml: models, sandbox and writable roots, features, hooks, MCP servers, plugins, and projects."}, {"name": "render_claude_sandbox", "filePath": "scripts/generate-agent-configs.py", "summary": "Renders the Claude sandbox settings block, reusing the Codex agmsg writable roots for allowWrite."}, {"name": "render_claude_settings", "filePath": "scripts/generate-agent-configs.py", "summary": "Renders the managed Claude Code settings JSON: hooks, permissions, sandbox, env, plugins, statusline, and model defaults."}, {"name": "claude_mcp_entry", "filePath": "scripts/generate-agent-configs.py", "summary": "Builds one Claude MCP server entry for stdio or HTTP transports from the manifest definition."}, {"name": "render_marketplace", "filePath": "scripts/generate-agent-configs.py", "summary": "Renders the local Codex plugin marketplace JSON from manifest plugin entries."}, {"name": "render_codex_plugin", "filePath": "scripts/generate-agent-configs.py", "summary": "Renders one managed Codex plugin manifest, failing when required plugin keys are missing."}, {"name": "claude_skill_symlink_outputs", "filePath": "scripts/generate-agent-configs.py", "summary": "Produces chezmoi symlink_ outputs mirroring every shared skill file into home/dot_claude/skills."}, {"name": "render_codex_profile", "filePath": "scripts/generate-agent-configs.py", "summary": "Renders a per-profile Codex TOML (model, reasoning effort, notify) launched via `codex --profile <name>`."}, {"name": "render_codex_profile_modify", "filePath": "scripts/generate-agent-configs.py", "summary": "Generates a chezmoi modify_ Python script that merges the managed profile keys into an existing ~/.codex/<profile>.config.toml without clobbering user keys."}, {"name": "render_model_profiles_env", "filePath": "scripts/generate-agent-configs.py", "summary": "Renders the model-profiles.env shell fragment (interactive profile, worker kind/profile/worktree, per-profile CLI args) for agent launchers."}, {"name": "render_claude_express_agent", "filePath": "scripts/generate-agent-configs.py", "summary": "Renders the express-explorer Claude subagent definition pinned to the express profile model."}, {"name": "expected_outputs", "filePath": "scripts/generate-agent-configs.py", "summary": "Collects every generated output path and rendered content derived from the manifest."}, {"name": "remove_stale_generated_outputs", "filePath": "scripts/generate-agent-configs.py", "summary": "Deletes generated files and empty directories under home/dot_claude/skills that are no longer expected."}, {"name": "main", "filePath": "scripts/generate-agent-configs.py", "summary": "CLI entry handling --set-asset pin rewrites, --check drift verification, stale output removal, and writing all generated files."}, {"name": "test_permgate.py", "filePath": "tests/unit/test_permgate.py", "summary": "Large unittest suite for the fail-closed permgate PermissionRequest hook: deterministic allow/deny layers, workspace and sensitive-path read rules, CLI protocol, classifier timeouts and shadow logging, and provider enablement."}, {"name": "permission_behavior", "filePath": "tests/unit/test_permgate.py", "summary": "Extracts the decision behavior from permgate hook JSON output, returning None for empty output."}, {"name": "PermgateTest", "filePath": "tests/unit/test_permgate.py", "summary": "Test case with about fifty checks for permgate deterministic layers, path rules, CLI protocol, classifier handling, and logging."}]

**Reviewing token budget**
exec
/bin/zsh -lc 'git diff --name-only 940a3a2b07adfd14140a0acff96784ef53a0a509..HEAD' in ~/Workspace/dotfiles
exec
/bin/zsh -lc "rg -n 'D-024-17a|D-024-20|5\\.14|P1-15|mise|GIT_' .orchestration/plans/024-design-quality.md .orchestration/tasks/dotfiles-T133-hold-playbook-a01.md" in ~/Workspace/dotfiles
exec
/bin/zsh -lc "rg --files .orchestration/acceptance .orchestration/validation | rg '(codex-worker-network|worker-write-boundary|worker-cap)'" in ~/Workspace/dotfiles
exec
/bin/zsh -lc "sed -n '1,200p' .orchestration/tasks/dotfiles-T133-hold-playbook-a01.md; sed -n '575,640p' scripts/generate-agent-configs.py; sed -n '970,1060p' scripts/generate-agent-configs.py" in ~/Workspace/dotfiles
 succeeded in 240ms:
.orchestration/plans/024-design-quality.md:27:| Q4 | キャッシュ | F5 の item 0 で各 job の所要を step ごとに計測し、uv / pip / mise / Homebrew の取得が 1 分超なら `actions/cache` を入れる（効果が無ければ入れない） | 取得物は pin とハッシュで検証済み（PR A）なので cache は再現性を変えない | — |
.orchestration/plans/024-design-quality.md:43:| M4 | タスク文の作成（10〜20 分）と presend チェッカーの往復（最大 107 分） | `task-from-plan.py`: todo の 1 行から task.md の骨格を生成。allowed_files は `git grep` で触れる箇所を列挙して提案、premises は command を実行して output を貼る（recall しない）、trust-boundary ファイルなら threat_table の雛形を 1 行ずつ出す。`task-consistency-check.py` に 3 つの形の規則（test selector、sentence、owning task id）と threat_table の単位規則を追加し、レビュー席の 1 ラウンドは trust-boundary タスクだけに | premises が実行結果になる。チェッカーがレビューで繰り返し出た指摘を吸収（mistakes into mechanisms） | タスク文 3〜5 分、presend 失敗ほぼ 0、review 席の往復が減る | 採用。新 P1-12 |
.orchestration/plans/024-design-quality.md:86:| trust-boundary タスクのタスク文レビュー | 形の検査: 3 つの形の規則（test selector、sentence、owning task id）、threat_table の単位規則（allowed_files 1 行につき 1 行、非パス制御 1 つにつき 1 行、orchestrator 効果 1 つにつき 1 行）、各行の disposition が `closed`（テストあり）/ `residual`（制御あり）/ `out-of-scope`（owner 実在）、premises が実行出力、invariants の設計文と byte 一致（INV-2） | プログラム | `task-consistency-check.py` の拡張（C11〜C15） | P1-12 |
.orchestration/plans/024-design-quality.md:99:## 5.14 信頼ホスト実行契約（trusted-host execution contract、D-024-18）
.orchestration/plans/024-design-quality.md:103:1. **書き込み境界（前提 6、ランタイム別に正直に）** Claude worker 席は専用の設定ディレクトリ `CLAUDE_CONFIG_DIR=~/.claude-worker`（chezmoi が描画、operator が一度 login）で起動し、orchestrator の `~/.claude` と設定を共有しない。worker 設定：除外コマンド無し、Herdr socket 無し、sandbox の allowWrite は自席 worktree と agmsg store と席別キャッシュだけ、`failIfUnavailable: true`、信頼パス（anchored checkout の `.claude/worktrees/` 以外、`~/.agents`、`~/.claude*`、`~/.local`、`~/.config`）への Edit deny（公式文書：file tool の permission 検査は要求パスと symlink 解決後のパスの両方に deny を適用し、symlink そのものへの書き込みは拒否する）、sandbox の強制範囲はユーザー設定ではなく **managed settings**（`/Library/Application Support/ClaudeCode/managed-settings.json`、公式文書 "Repository settings under an admin-required sandbox"：project/local 設定は sandbox を無効化したり除外・socket を足したりできない）に置く。chezmoi は user ではこのファイルを書けないので、描画した内容を操作者が `sudo` で一度配置する（操作者手順）。worker 設定は worktree 自身の `.claude/**` と `.mcp.json` への Edit deny（`//<anchored>/.claude/worktrees/*/.claude/**`）を持つ（Bash 側は sandbox 既定の settings/hooks の denyWithinAllow）。agmsg store（全席が書く）から配送 hook が driver や plugin を source する上流の経路（storage.sh の `drivers.partition` traversal、`db/trusted-plugins` と `plugins/partition/shared.sh` による差し替え承認）は別タスク（agmsg hardening）の行で、worker 設定は `~/.agents/skills/agmsg/plugins/**` と `~/.agents/skills/agmsg/db/trusted-plugins` への書き込みを deny し（Edit deny は sandbox の deny にも合流する）、hook 側は store 由来の設定値を検証するまで残余と書く。managed settings の配置先は OS で異なる（macOS `/Library/Application Support/ClaudeCode/managed-settings.json`、Linux `/etc/claude-code/managed-settings.json`）。hook は agmsg 配送だけを、hook コマンドを `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<home> …` で始めて（`BASH_ENV` などの継承環境を bash 起動前に消す；PATH 固定だけでは BASH_ENV が先に走る）絶対パスのインタプリタで呼び（上流の agmsg スクリプトは `/usr/bin/env bash` の shebang を持つので、hook 実行環境の PATH が shim を含まないことで束縛する）、各 hook に `onFailure: "block"`。公式文書：linked worktree の session は **main checkout の `.claude/settings.local.json` を読む**ので、worker 向けの hook を worktree の settings.local.json に書いても読まれず、逆に orchestrator の local hooks が worker session でも走る。したがって orchestrator 側の local hooks も guard 経由にし、worker 側の hook は worker config dir の settings に置く。Edit deny の一覧は `git ls-tree` ではなく描画時の静的一覧（manifest に列挙、`.agents/worklog/**` と `.agents/worklog/uv-cache/**` を含む）とし、`~/.agents/**` の全面 deny は agmsg store の書き込みと矛盾するので、`~/.agents/agent-config.yaml`、`~/.agents/skills/**/scripts/**`、`~/.agents/model-profiles.env` などストア以外を列挙する。公式文書で確認した事実（2026-10-19）：`Edit(path)` の deny は Write/MultiEdit/NotebookEdit にも効き、deny → ask → allow の順で最初の一致が決まる；ただし Read/Edit の deny は **Bash sandbox の設定にも合流する**（"Paths and domains from both sandbox settings and permission rules are merged into the final sandbox configuration"）ので、ユーザー設定（全席共有）に `.orchestration/**` の Edit deny を書くと orchestrator の Bash による記録書き込みも止まる。hook は起動時に固定されず、設定ファイルの編集は file watcher が即座に反映する。`sandbox.failIfUnavailable` の既定は fail-open（依存が無ければ sandbox 無しで実行）。したがって Claude 席の境界は Edit deny 規則ではなく、**ユーザーレベルの PreToolUse hook**（`~/.claude/hooks/worker-write-boundary`、chezmoi が描画、`/bin/sh` または絶対パスの `python3 -I`）で作る：cwd の realpath が `<anchored>/.claude/worktrees/` 配下の session では、Write/Edit/MultiEdit/NotebookEdit の対象が cwd の外、または `<cwd>/.claude/**`・`<cwd>/.mcp.json` のとき `permissionDecision: deny` を返す。Bash 側は sandbox の既定 `denyWithinAllow`（settings、hooks）と `allowWrite`（自席 worktree）が担う。`failIfUnavailable: true` を全席に置く。 Codex 席は sandbox（workspace-write）がツールの書き込み全部を自席の worktree と列挙パスに限る。Claude 席は Seatbelt sandbox が Bash を限るだけで、Write/Edit/MultiEdit/NotebookEdit、hook、MCP プロセスは sandbox 外で動き、permission policy（permgate の決定論ポリシー）が path で拒否しない限り anchored checkout や `~/.agents` にも書ける（2026-10-19 時点、描画済み設定にその deny は無い）。したがって前提 6 は「Codex 席は成立、Claude 席は P1-15 が描画設定に Edit の path deny を入れるまで残余」と書く。P1-15 以前に「worker は信頼ルートに書けない」と書く文は誤りで、C-80 が拒否する。P1-15 が入るまで、承認の出所は項目 8 の「コミット済み台帳」で守る。書き込みは自席の worktree（`.claude/worktrees/<name>`）、scratch、列挙されたツールキャッシュに限る。anchored checkout（`.claude/worktrees/` 以外）、`~/.agents/agent-config.yaml`、`~/.claude/hooks`、信頼ルートのバイナリ、orchestrator の証跡・スナップショット・lock は worker から書けない。render テストが描画後の deny を検証する。残余は「どの席 sandbox にも属さない同一 UID プロセス」と、Worker Playbook step 4 が sandbox 外に出す少数のコマンド（gh）。後者は D-024-17（P1-15）で絶対パスの実行体に束縛する。
.orchestration/plans/024-design-quality.md:104:2. **無害化した環境を最初に** 最初の処理として `env -i` に入り、PATH は信頼ルートで解決した絶対バイナリへのリンクだけの私設ディレクトリ（shims、空、相対は拒否）。git は毎回 `GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null -c core.hooksPath=/dev/null -c core.fsmonitor=false -c protocol.allow=never -c protocol.https.allow=always` と明示 `-C`（https だけ許す。`protocol.allow=never` 単独は必要な fetch を止める）。 検査の読み取りは `GIT_NO_LAZY_FETCH=1` で部分クローンの遅延 fetch（checkout 設定の credential.helper を起動しうる）を止め、`-c submodule.recurse=false --ignore-submodules=all` で submodule 内の status/diff（submodule 自身の設定が filter を有効化しうる）を止める。`.gitmodules` を持つ checkout は検査対象として拒否する。 `-C` は作業木を束縛しないので（repo-local の `core.worktree` が読み先を checkout 外へ向けられる）、git は `--git-dir=<checkout>/.git --work-tree=<checkout>` を明示し、`git rev-parse --show-toplevel` の realpath が checkout と一致しないときは拒否する。 premise や検査の「コマンド実行」は、固定語彙の読み取り専用プローブ（`git rev-parse <ref>`、`test -e <path>`、`grep -c <pattern> <file>` のように検査器自身が解釈する形）だけを許し、任意のシェル文字列は実行しない（本文のハッシュはコマンド文を認証するだけで、`python -I scripts/x.py` のファイル被演算子や `source ./x.sh` の中身は認証しない）。diff と show は `--no-ext-diff --no-textconv` と `-c core.attributesFile=/dev/null -c core.sshCommand=false` を付け、PR 側の `.gitattributes`（external diff、textconv、filter）が検査内容や実行物を変えないようにする。Python は `-I`。PATH 探索で実行するものは無い。
.orchestration/plans/024-design-quality.md:111:9. **私設キャッシュ** orchestrator 側の実行は worker と共有するキャッシュ（`~/.cache/uv`、`~/.local/share/uv`、mise）から実行可能物を読まない。`UV_CACHE_DIR` を anchored checkout 配下（`.agents/worklog/uv-cache`、gitignored、worker 書き込み不可）に固定し、`uv run --no-config --no-project --offline --python <信頼ルートの絶対パスのインタプリタ>` で起動する（`--no-config` で uv の設定探索を止め、`--python` の絶対パスで cwd や親の `.venv` の発見を止める；敵対的な `.venv` と `uv.toml` を置いた fixture で検証）。hook は uv を使わず jq と python 標準ライブラリだけで動く。
.orchestration/plans/024-design-quality.md:113:7. **検証** threat_table は本節の項目 1〜10 に 1 行ずつ対応させる（参照だけでは足りない）。共通テスト補助 `tests/unit/trusted_exec_contract.py`（P1-6 で作る）を使い、仕組みごとに 4 つの red→green テストを持つ：PATH 先頭の shim が実行されない、植え付けた GIT_* と git 設定が効かない、worker ルート配下の信頼パスが拒否される、検証後に差し替えたファイルが消費側に届かない。
.orchestration/tasks/dotfiles-T133-hold-playbook-a01.md:38:premises: []

 succeeded in 302ms:
.orchestration/acceptance/dotfiles-T133-worker-cap-hookspath-followup-a01.md
.orchestration/acceptance/dotfiles-T133-worker-cap-hookspath-a02.md
.orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md
.orchestration/acceptance/dotfiles-T133-worker-cap-hookspath-a01.md
.orchestration/validation/dotfiles-T133-worker-cap-hookspath-a02-security-bb84bde.md
.orchestration/validation/dotfiles-T133-worker-cap-hookspath-a02-local-review-bb84bde.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-8d42532.md.last.md
.orchestration/validation/dotfiles-T133-worker-cap-hookspath-a01-local-review-c96697a.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-08e6ac7.md.last.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-8bac9e5.md.last.md
.orchestration/validation/dotfiles-T133-worker-cap-hookspath-a01-audit-c96697a.md
.orchestration/validation/dotfiles-T133-worker-cap-hookspath-a02-review-receipt.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-5cbbc03.md.last.md
.orchestration/validation/dotfiles-T133-worker-cap-hookspath-followup-a01-crit.json
.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-ecc7ab5.md
.orchestration/validation/dotfiles-T133-worker-cap-hookspath-a02-security-bb84bde.md.last.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-435275a.md
.orchestration/validation/dotfiles-T133-worker-cap-hookspath-followup-a01-audit-2d8b0fe.md.last.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-f1b862c.md.last.md
.orchestration/validation/dotfiles-T133-worker-cap-hookspath-followup-a01-security-570d749.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-e5d1b57.md
.orchestration/validation/dotfiles-T133-worker-cap-hookspath-a02-chain-bb84bde.log
.orchestration/validation/dotfiles-T133-worker-cap-hookspath-a01-review-receipt.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-f589c7c.md.last.md
.orchestration/validation/dotfiles-T133-worker-cap-hookspath-a02-audit-bb84bde.md.last.md
.orchestration/validation/dotfiles-T133-worker-cap-hookspath-followup-a01-security-2d8b0fe.md
.orchestration/validation/dotfiles-T133-worker-cap-hookspath-followup-a01-pr-feedback.json
.orchestration/validation/dotfiles-T133-worker-cap-hookspath-a01-audit-c96697a.md.last.md
.orchestration/validation/dotfiles-T133-worker-cap-hookspath-a02-pr-feedback.json
.orchestration/validation/dotfiles-T133-worker-cap-hookspath-a01-crit.json
.orchestration/validation/dotfiles-T133-worker-cap-hookspath-followup-a01-local-review-2d8b0fe.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-5cbbc03.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-08e6ac7.md
.orchestration/validation/dotfiles-T133-worker-cap-hookspath-followup-a01-chain-570d749.log
.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-67415f5.md
.orchestration/validation/dotfiles-T133-worker-cap-hookspath-followup-a01-security-2d8b0fe.md.last.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-435275a.md.last.md
.orchestration/validation/dotfiles-T133-worker-cap-hookspath-a02-chain-b813355.log
.orchestration/validation/dotfiles-T133-worker-cap-hookspath-followup-a01-audit-2d8b0fe.md
.orchestration/validation/dotfiles-T133-worker-cap-hookspath-a01-chain-c96697a.log
.orchestration/validation/dotfiles-T133-worker-cap-hookspath-followup-a01-chain-2d8b0fe.log
.orchestration/validation/dotfiles-T133-worker-cap-hookspath-followup-a01-security-570d749.md.last.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-519afd7.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-987865d.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-f1b862c.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-8bac9e5.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-f589c7c.md
.orchestration/validation/dotfiles-T133-codex-worker-network-a01-text-security-cf5efd5.md
.orchestration/validation/dotfiles-T133-worker-cap-hookspath-followup-a01-review-receipt.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-67415f5.md.last.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-1ae3138.md
.orchestration/validation/dotfiles-T133-worker-cap-hookspath-a01-pr-feedback.json
.orchestration/validation/dotfiles-T133-worker-cap-hookspath-a02-audit-bb84bde.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-ecc7ab5.md.last.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-1ae3138.md.last.md
.orchestration/validation/dotfiles-T133-worker-cap-hookspath-a02-crit.json
.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-987865d.md.last.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-8d42532.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-519afd7.md.last.md

 succeeded in 313ms:
---
format: 2
task_id: dotfiles-T133-hold-playbook-a01
kind: code
security: false
allowed_files:
  - scripts/orchestrator/hold-playbook.sh
  - tests/unit/test_hold_playbook.py
  - .orchestration/dotfiles-T133-hold-playbook-a01/**
after: []
threat_table:
  - control: scripts/orchestrator/hold-playbook.sh
    disposition: "residual: the fixed Python helper reads records as data, writes only the replan file and the conditional decisions row, and never executes record text or dispatches work; the temporary-directory tests verify these effects."
  - control: tests/unit/test_hold_playbook.py
    disposition: "residual: script executions use a copied script and fixture records in temporary directories; the vocabulary test reads the real learning tree without changing it."
  - control: .orchestration/dotfiles-T133-hold-playbook-a01/**
    disposition: "residual: branch artifacts stay in this task's directory and contain the dispatched copy, source attribution and validation evidence for the final-head audit."
  - control: the task-file copy on the branch (.orchestration/dotfiles-T133-hold-playbook-a01/task.md)
    disposition: "residual: the copy is byte-identical to the dispatched text; the TASK and RESULT bind its own sha256 and the orchestrator compares it at acceptance."
  - control: the branch evidence records under .orchestration/dotfiles-T133-hold-playbook-a01/ (report.md, validation.md, sandbox.md, learning.md and worker review evidence)
    disposition: "residual: records contain prose and command output; sandbox.md lists every refused command and the audit compares the claims with the final diff and CI."
  - control: task metadata
    disposition: "residual: the orchestrator checks C1 to C10 and C7b before dispatch and at acceptance; the byte comparison authenticates the complete dispatched front matter."
  - control: metadata separators
    disposition: "residual: the helper reads only the bounded first YAML front-matter document of the input task; the task-copy byte comparison covers every separator."
  - control: in-process effects
    disposition: "residual: the helper creates only .orchestration/tasks/<task>-replan.md and conditionally appends one row to .orchestration/decisions.tsv; it preserves the source task and existing replans and executes no command derived from records."
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or environment configuration changes; the script runs its embedded Python helper through uv run --no-project --with pyyaml python -I and loads YAML with yaml.safe_load."
  - control: new or renamed scripts
    disposition: "residual: hold-playbook.sh is the only new script; its Python helper is embedded, and any sibling helper or additional script falls outside allowed_files."
  - control: orchestrator effect merge
    disposition: "residual: the orchestrator merges only through gh pr merge --squash --match-head-commit <audited head> after the integration gate in Orchestrator Playbook step 10.5."
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the feedback sweep and the task-level audit bind the new final head before the gate."
  - control: orchestrator effect forced worker removal
    disposition: "residual: no forced removal is planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal records the discarded uncommitted state in acceptance."
premises: []
---

# AGMSG-TASK dotfiles-T133-hold-playbook-a01 — plan 024 P1-13 hold playbook

## Goal

`scripts/orchestrator/hold-playbook.sh <task> <class>` expands a pinned corrective procedure into a replan skeleton and records a pending decision when its prospective changes exceed the task's `allowed_files`. It implements item (13) of `.orchestration/plans/024-design-programs.md` and the class-specific playbook of `.orchestration/plans/024-design-quality.md` section 5.13. This task is `security: false`: the script reads records and writes records and executes no PR-controlled input. Existing controls own hold detection at three findings of one class, INV-6's S2 thresholds including two revises, and a P0 finding. The P0 rule remains an immediate revert PR for a defect already on main and hold for an unmerged artifact.

## Files

1. `.orchestration/learning/classes.yaml` is a new tracked mapping keyed by class slug. It contains one entry for every distinct slug in the `classes:` lines of `.orchestration/learning/mistakes/M-*.md`. The worker recounts the records and distinct slugs at start and records both counts in `validation.md`.

   Each entry has `remedy:` and `blast_radius:`. The remedy is one or two plain sentences describing a corrective procedure derived from the records' Corrections lines and their references in `.orchestration/learning/corrections-inventory.tsv`. The blast radius is a list of repository-relative globs naming files a fix of that class touches, derived from the records' Evidence lines. The report attributes each entry to its source mistake records and correction references. A class without a known corrective procedure has `remedy: unknown` and `blast_radius: []`. Review titles and illustrative class names do not add vocabulary entries.

   `tests/unit/test_hold_playbook.py::HoldPlaybookTests::test_vocabulary_covers_mistake_classes` reads the real mistake records and asserts that every recorded slug appears in this mapping. `tests/unit/test_hold_playbook.py::HoldPlaybookTests::test_known_class_without_remedy_is_reported` verifies the explicit unknown-remedy representation.

2. `scripts/orchestrator/hold-playbook.sh` accepts exactly `<task> <class>`. A small Python helper embedded in the shell script performs parsing and record generation through `uv run --no-project --with pyyaml python -I`. It uses `yaml.safe_load` for the class mapping and the task's first YAML front-matter document. Shell comments use English shdoc annotations.

   The task id matches `^[A-Za-z0-9][A-Za-z0-9._-]*$`. An invalid task id exits 2 before constructing output paths. A class absent from `classes.yaml` exits 2 and names the supplied slug in its diagnostic. These refusals leave the replan and decision ledger unchanged.

   The helper reads `.orchestration/tasks/<task>.md` for `allowed_files` and creates `.orchestration/tasks/<task>-replan.md`. Creation refuses an existing filesystem entry at that destination with exit 4 and preserves its contents. The script never edits the source task text and never dispatches.

   The replan contains the cause class, the remedy sentence, every blast-radius glob, and the task's allowed-files entries that cover each glob. Uncovered globs are explicitly marked outside `allowed_files`. Coverage concerns the entire prospective scope denoted by a glob, including paths that do not exist yet. Matching a pattern string as though it were a filename or expanding only currently existing files does not establish coverage.

   The replan includes a new Completion sentence skeleton with placeholders for the observable result, verification selectors and evidence. It includes this four-field line:

   ```text
   re-plan: specification — <fill>; design — <fill>; implementation — <fill>; verification — <fill>
   ```

   The four fields follow the structure of the S1 re-plan in `.orchestration/acceptance/dotfiles-T133-permission-guard-gate-a04.md` and its `replans` JSON object. The skeleton remains a proposal until the orchestrator supplies concrete content. The script leaves the acceptance record unchanged.

   Every blast-radius glob covered by `allowed_files` produces exit 0. The orchestrator fills the skeleton and re-dispatches through the applicable hold procedure. A known class with `remedy: unknown` is reported explicitly with its empty blast radius; it follows the same coverage rule and acquires no invented corrective procedure. Exit 0 establishes scope coverage only.

   Any uncovered glob produces the replan, appends exactly one six-column TSV row to `.orchestration/decisions.tsv`, and exits 3. The row has `id` equal to `D-<task>-replan`, `when` equal to the current UTC timestamp, `what` naming the uncovered globs, `why` naming the class, `basis` equal to `hold-playbook`, and `result` equal to `pending`. It contains no default or deadline that consumes a default.

   `tests/unit/test_hold_playbook.py::HoldPlaybookTests::test_three_classes_expand_into_replans`, `test_uncovered_scope_appends_pending_decision`, `test_unknown_class_exits_2`, `test_existing_replan_exits_4`, `test_invalid_task_id_is_refused`, `test_scope_comparison_covers_the_whole_glob` and `test_record_text_is_never_executed` verify these statements.

3. `tests/unit/test_hold_playbook.py` uses `unittest` and temporary repository layouts containing a copied script, fixture `classes.yaml`, source task text and decision ledger. Its three-class expansion fixture uses `colored-json-parse`, `concurrent-ff-clobber` and `records-form`. Each class produces its own replan skeleton with the expected remedy, scope classification, Completion placeholder and four re-plan fields.

   The scope decision test verifies exit 3, the exact decision id and six fields, preservation of existing ledger rows and absence of a default. Refusal tests verify their exit codes and unchanged records. The overwrite test also repeats an out-of-scope invocation and verifies that exit 4 appends no second decision row. The literal-data test uses command-looking record text and verifies that it remains text without executing.

   The known-class unknown-remedy test verifies the reported `unknown`, empty blast radius and coverage exit status. The whole-glob test includes an exact permitted scope, a scope covered by an allowed directory glob and a broader scope that extends outside the allowed files. The vocabulary test reads the real tree without invoking the script there.

   The behavioral tests are written before implementation and have red results followed by green results. The vocabulary test has a red result before the tracked mapping is added and a green result with the completed mapping.

4. `.orchestration/dotfiles-T133-hold-playbook-a01/` contains the byte-identical dispatched `task.md`, `report.md`, `validation.md`, `sandbox.md`, `learning.md` and worker review evidence. The report maps the Files requirements to their test selectors and records the class-source attribution. Worker review filenames carry the required `-worker-` infix.

## Out of scope

`dispatch.sh` changes, including refusal of TASK or revise sends during hold, are deferred until P1-6 merges. That follow-on work includes the hold-send-refusal fixture named by the plan. This task has no dependency on that merge.

`verdict.sh`, `scripts/regime-counters.sh`, hold detection, counter output and P0 enforcement remain outside this implementation. The existing S1 and S2 lines supply context for the orchestrator; this helper neither parses review titles into classes nor releases a hold.

Editing any mistake record, correction record, correction inventory or acceptance record is outside this task. Tests exercise replan creation and decision appends in temporary directories. Live recovery records are written only when the orchestrator later invokes the completed helper.

## Check

`make format`, `shellcheck scripts/orchestrator/hold-playbook.sh`, `shfmt -d scripts/orchestrator/hold-playbook.sh` and `uv run --no-project --with pyyaml python -m unittest tests.unit.test_hold_playbook -v` have their commands, verbatim output, exit statuses and tested heads pasted in `.orchestration/dotfiles-T133-hold-playbook-a01/validation.md`. The script passes shellcheck and shfmt, and the unit module is green.

The three-class expansion tests and the decision, refusal, literal-data and vocabulary tests carry their red-before-implementation and green-final-head evidence. Every script execution uses a temporary fixture tree. No local Bats tests run.

An inherited formatting failure is reproduced on the unchanged base and recorded with its output. It remains a reported failure and receives no repair outside `allowed_files`.

`git diff --numstat origin/main...HEAD` shows at most 350 changed lines outside `tests/` and `.orchestration/`, and at most 400 changed lines under `tests/`. Changed lines are additions plus deletions, and fixtures count against the test cap. Validation includes the totals and changed-file inventory.

The orchestrator runs the format-2 task-consistency checker, including C1 to C10 and C7b, before dispatch and at acceptance. The task copy remains byte-identical to the dispatched file.

## Completion

The Completion clause of `.orchestration/tasks/dotfiles-T133-regime-ci-followup-a01.md` applies with `dotfiles-T133-hold-playbook-followup-a01` as the owner of any advisory P2 and `task_copy=<sha256 of .orchestration/dotfiles-T133-hold-playbook-a01/task.md>` in the RESULT. This task's scope, Check, `security: false`, fresh-branch rule and prohibition on `@codex review` comments govern that reference.

One PR starts from a fresh branch off `origin/main`. The orchestrator writes the advisory owner task before recording its first ownership disposition. A small in-scope P2 follows the inherited `check=` revise procedure while INV-6 permits it.

The worker's own pre-push review is one round at most. Every worker-side fix round counts toward INV-6. A surviving P0/P1 is sent in the RESULT as `open:<finding-or-thread-id>` and stops integration for the operator's decision. The third finding of one class stops further rounds until the orchestrator's re-plan.

The RESULT identifies the final head, base, branch, changed files, test selectors, caps, evidence paths, task-copy hash and every Bot finding's disposition. It carries the precheck evidence required by the applicable RESULT procedure.

The orchestrator runs the task-level audit on the final head and dispositions every finding before the gate. Final-head CI, the feedback sweep, audit, acceptance record, gate and merge follow Orchestrator Playbook step 10 in its prescribed order. A changed head receives fresh evidence.

No `@codex review` comment is issued. Every `gh` write and Git write runs as an individual command without shell chaining or a wrapper combining writes. A classifier denial produces a blocked PONG naming the command and refusal.

## Orchestrator note (2026-10-19T03:2xZ): classes.yaml is a record, not a worker file

`.orchestration/learning/classes.yaml` is written by the orchestrator (checker C2 keeps every `.orchestration/` path except the task directory out of a worker's allowed_files); the orchestrator seeds it from the `classes:` lines of the mistake records before this task is dispatched and keeps it current. The worker therefore does not edit it: item 1 is read as the file format the script consumes, the pinned-vocabulary check is implemented as `hold-playbook.sh --check-vocabulary <classes.yaml> <mistakes dir>` (exit 2 listing every class slug of the records that the file lacks, exit 0 otherwise) and tested with fixtures only; the orchestrator runs it against the real tree at acceptance and pastes the output. No test reads the real `.orchestration/learning/` tree.

## Checks (pasted by the orchestrator before each send)

```
2026-10-19T03:2xZ dispatch 1
task=dotfiles-T133-hold-playbook-a01 tasks=0 amendments=0 questions=0 results=0 withdrawn=0 revises=0 source=live
C-78: no in-flight task names scripts/orchestrator/hold-playbook.sh or tests/unit/test_hold_playbook.py (P1-5 a04, #412 a05, worker-write-boundary-a01 checked)
task-consistency-check: OK after the classes.yaml entry moved to the orchestrator (C2)
```

Implementation and runtime verification remain pending worker execution.
Unknown remedies and pending scope decisions require orchestrator resolution before recovery.    skills_root = ROOT / "home/dot_agents/skills"
    claude_root = ROOT / "home/dot_claude/skills"
    if not skills_root.exists():
        return outputs
    for source_file in sorted(path for path in skills_root.rglob("*") if path.is_file()):
        if source_file.name.startswith("."):
            continue
        rel = source_file.relative_to(skills_root)
        target_path = rel.with_name(chezmoi_target_name(rel.name))
        target_dir = claude_root / target_path.parent
        outputs[target_dir / f"symlink_{target_path.name}.tmpl"] = render_claude_skill_symlink(source_file)
    return outputs


def render_codex_profile(name: str, profile: dict[str, Any]) -> str:
    codex = profile["codex"]
    lines = [
        f'# Codex model profile "{name}"; launch with: codex --profile {name}',
        f"# {GENERATED_HEADER}",
        "",
        f"model = {quote_toml(codex['model'])}",
        f"model_reasoning_effort = {quote_toml(codex['model_reasoning_effort'])}",
    ]
    # Overrides the global sandbox_mode; profiles without it inherit the base config.
    if sandbox_mode := codex.get("sandbox_mode"):
        lines.append(f"sandbox_mode = {quote_toml(sandbox_mode)}")
    if notify := codex.get("notify"):
        lines.append(f"notify = {quote_toml(notify)}")
    lines.extend(
        [
            "",
            "[features]",
            "hooks = true",
            "",
            "[hooks.state]",
        ]
    )
    return "\n".join(lines) + "\n"


HOOK_TRUST_BEGIN = "# >>> codex hook trust (generated by scripts/generate-agent-configs.py; edit it there) >>>\n"
HOOK_TRUST_END = "# <<< codex hook trust <<<\n"
# Apply-time Codex hook trust, shared by the base and profile modify scripts. Codex runs a config or
# plugin hook only when [hooks.state."<key>"] holds the trust hash of its current definition, and that
# hash covers the absolute command path, so it is computed on each host from the hook it names.
HOOK_TRUST_CODE = """import functools
import hashlib
import json
import re

HOOK_TRUST_HOME = "{{ .chezmoi.homeDir }}"
NO_MATCHER_HOOK_EVENTS = frozenset({"user_prompt_submit", "stop", "interrupt"})
SHORT_TIMEOUT_HOOK_EVENTS = frozenset({"session_end", "interrupt"})


def hook_event_label(event: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", event).lower()


def with_home(value, home: str):
    if isinstance(value, str):
        return value.replace(HOOK_TRUST_HOME, home)
    if isinstance(value, list):
        return [with_home(item, home) for item in value]
    if isinstance(value, dict):
        return {key: with_home(item, home) for key, item in value.items()}
            chunk = drop_declared_assignments(chunk, by_key, HOOK_STATE_SCOPES[name])
        kept.append((name, chunk))
    return kept


def guarded_merge(merged: str, current: str, declared_keys) -> str:
    \"\"\"The merged config, or the current content unchanged unless it is valid TOML holding every declared key.\"\"\"
    if hook_trust_toml is None:
        return merged
    try:
        state = hook_trust_toml.loads(merged).get("hooks", {}).get("state", {})
        valid = isinstance(state, dict) and all(key in state for key in declared_keys)
    except (ValueError, AttributeError):  # tomllib.TOMLDecodeError is a ValueError.
        valid = False
    if valid:
        return merged
    print("WARN: codex config merge produced invalid TOML; keeping the existing file", file=sys.stderr)
    return current
"""


def codex_hook_trust(manifest: dict[str, Any]) -> dict[str, Any]:
    """The declared trusted hooks and the config hook definitions the modify scripts hash at apply time."""
    hooks = manifest["codex"].get("hooks", {})
    config_hooks: dict[str, list[dict[str, Any]]] = {}
    definitions = [("PermissionRequest", hooks["permission_request"])] if hooks.get("permission_request") else []
    definitions += [(hook["event"], hook) for hook in hooks.get("command_hooks", [])]
    for event, hook in definitions:
        # Mirrors codex_command_hook_lines(): one matcher group per definition, in render order.
        config_hooks.setdefault(re.sub(r"(?<!^)(?=[A-Z])", "_", event).lower(), []).append(
            {
                "matcher": "*",
                "hooks": [
                    {
                        "type": "command",
                        "command": hook["command"],
                        "timeout": hook["timeout"],
                        "statusMessage": hook["status_message"],
                    }
                ],
            }
        )
    declared = []
    for key, state in hooks.get("state", {}).items():
        if not isinstance(state, dict) or set(state) - {"trusted_hash", "enabled"}:
            fail(f"codex.hooks.state.{key} may only set trusted_hash and enabled")
        declared.append({"key": key, **state})
    return {"declared": declared, "config_hooks": config_hooks}


def render_hook_trust_block(manifest: dict[str, Any]) -> str:
    return HOOK_TRUST_BEGIN + f"HOOK_TRUST = {codex_hook_trust(manifest)!r}\n" + HOOK_TRUST_CODE + HOOK_TRUST_END


def render_codex_base_modify(manifest: dict[str, Any]) -> str:
    """The hand-maintained base modify script with its generated hook-trust block refreshed."""
    relative = "home/dot_codex/modify_private_config.toml"
    # A fixture ROOT (unit tests) has no base script of its own; take the repository's copy then.
    source = ROOT / relative if (ROOT / relative).exists() else Path(__file__).resolve().parents[1] / relative
    text = source.read_text()
    start, end = text.find(HOOK_TRUST_BEGIN), text.find(HOOK_TRUST_END)
    if start == -1 or end < start:
        fail("home/dot_codex/modify_private_config.toml must keep the codex hook trust block markers")
    return text[:start] + render_hook_trust_block(manifest) + text[end + len(HOOK_TRUST_END) :]


def render_codex_profile_modify(name: str, profile: dict[str, Any], manifest: dict[str, Any]) -> str:
    managed = render_codex_profile(name, profile)
    render_helper = ""
    managed_source = "MANAGED"
    if "{{ .chezmoi.homeDir }}" in managed:
        render_helper = """\n\ndef render_managed_paths(text: str) -> str:
    return text.replace("{{ .chezmoi.homeDir }}", str(Path.home()))
"""
        managed_source = "render_managed_paths(MANAGED)"
    return f'''#!/usr/bin/env python3
"""Merge the managed Codex {name} profile with Codex-owned runtime state."""

from __future__ import annotations

import sys
from pathlib import Path
import re

RUNTIME_PREFIXES = {RUNTIME_PREFIXES!r}
MANAGED = {managed!r}
{render_helper}
__HOOK_TRUST_BLOCK__

def table_name(header: str) -> str | None:
    """The raw name of a `[table]` or `[[array]]` header line, which may end in a `# comment`, else None."""

 succeeded in 835ms:
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
.orchestration/acceptance/dotfiles-T102-add-worker-credential-notice-a01.md
.orchestration/acceptance/dotfiles-T103-gh-auth-stores-a01.md
.orchestration/acceptance/dotfiles-T104-pins-2026-10-06-a01.md
.orchestration/acceptance/dotfiles-T108-one-login-per-machine-a01.md
.orchestration/acceptance/dotfiles-T109-claude-worker-merge-deny-a01.md
.orchestration/acceptance/dotfiles-T110-gh-auth-file-storage-a01.md
.orchestration/acceptance/dotfiles-T111-project-map-subagent-a01.md
.orchestration/acceptance/dotfiles-T112-pins-2026-10-07-a01.md
.orchestration/acceptance/dotfiles-T113-codify-T111-lessons-a01.md
.orchestration/acceptance/dotfiles-T114-canonical-clone-reconcile-a01.md
.orchestration/acceptance/dotfiles-T115-worker-audit-xhigh-a01.md
.orchestration/acceptance/dotfiles-T116-on-demand-workers-a01.md
.orchestration/acceptance/dotfiles-T117-upgrade-outside-canonical-clone-a01.md
.orchestration/acceptance/dotfiles-T118-rolling-tools-single-update-a01.md
.orchestration/acceptance/dotfiles-T119-rolling-release-assets-a01.md
.orchestration/acceptance/dotfiles-T120-npm-provenance-and-claude-channel-a01-design-reset.md
.orchestration/acceptance/dotfiles-T120-npm-provenance-and-claude-channel-a01.md
.orchestration/acceptance/dotfiles-T121-claude-hook-install-hint-a01.md
.orchestration/acceptance/dotfiles-T124-design-receipt-canonical-a01.md
.orchestration/acceptance/dotfiles-T124-design-review-a01.md
.orchestration/acceptance/dotfiles-T124-wave1-task-validator-a01-design-reset.md
.orchestration/acceptance/dotfiles-T124-wave1-task-validator-a01.md
.orchestration/acceptance/dotfiles-T124-wave3b-audit-grammar-a01-design-reset.md
.orchestration/acceptance/dotfiles-T128-audit-s1-report-a01.md
.orchestration/acceptance/dotfiles-T128-aws-cli-macos-a01.md
.orchestration/acceptance/dotfiles-T128-chain-github-scripts-a01.md
.orchestration/acceptance/dotfiles-T128-chain-github-scripts-followup-a01.md
.orchestration/acceptance/dotfiles-T128-chain-github-scripts-followup-a02.md
.orchestration/acceptance/dotfiles-T128-chain-glue-finish-a01.md
.orchestration/acceptance/dotfiles-T128-chain-glue-integrate-a01.md
.orchestration/acceptance/dotfiles-T128-chain-review-scripts-a01.md
.orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a01.md
.orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a02.md
.orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a03.md
.orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a04.md
.orchestration/acceptance/dotfiles-T128-ci-skip-orchestration-a01-design-reset.md
.orchestration/acceptance/dotfiles-T128-ci-skip-orchestration-a01.md
.orchestration/acceptance/dotfiles-T128-ci-skip-orchestration-a02.md
.orchestration/acceptance/dotfiles-T128-ci-skip-redesign-a01.md
.orchestration/acceptance/dotfiles-T128-design-review-a01.md
.orchestration/acceptance/dotfiles-T128-doctor-codex-trust-a01.md
.orchestration/acceptance/dotfiles-T128-gate-evidence-a01-design-reset.md
.orchestration/acceptance/dotfiles-T128-gate-evidence-a01.md
.orchestration/acceptance/dotfiles-T128-gate-evidence-a02-amend-review-a01.md
.orchestration/acceptance/dotfiles-T128-gate-evidence-a02-design-reset.md
.orchestration/acceptance/dotfiles-T128-gate-evidence-a02.md
.orchestration/acceptance/dotfiles-T128-gate-evidence-a03-amend-review-a01.md
.orchestration/acceptance/dotfiles-T128-gate-evidence-a03-design-reset.md
.orchestration/acceptance/dotfiles-T128-gate-evidence-a03.md
.orchestration/acceptance/dotfiles-T128-gate-evidence-a04-amend-review-a01.md
.orchestration/acceptance/dotfiles-T128-gate-evidence-a04.md
.orchestration/acceptance/dotfiles-T128-gate-evidence-redesign-a01.md
.orchestration/acceptance/dotfiles-T128-gate-evidence-redesign-a02.md
.orchestration/acceptance/dotfiles-T128-gate-wrapper-path-a01.md
.orchestration/acceptance/dotfiles-T128-model-profiles-xhigh-a01.md
.orchestration/acceptance/dotfiles-T128-orchestrator-tools-a01-amend-review-a01.md
.orchestration/acceptance/dotfiles-T128-orchestrator-tools-a01-design-reset.md
.orchestration/acceptance/dotfiles-T128-orchestrator-tools-a01.md
.orchestration/acceptance/dotfiles-T128-orchestrator-tools-a02-design-reset.md
.orchestration/acceptance/dotfiles-T128-orchestrator-tools-a02.md
.orchestration/acceptance/dotfiles-T128-orchestrator-tools-a03-design-reset.md
.orchestration/acceptance/dotfiles-T128-orchestrator-tools-a03.md
.orchestration/acceptance/dotfiles-T128-orchestrator-tools-a04.md
.orchestration/acceptance/dotfiles-T128-orchestrator-tools-a05-design-reset.md
.orchestration/acceptance/dotfiles-T128-orchestrator-tools-a05.md
.orchestration/acceptance/dotfiles-T128-orchestrator-tools-a06.md
.orchestration/acceptance/dotfiles-T128-orchestrator-tools-followup-a01.md
.orchestration/acceptance/dotfiles-T128-orchestrator-tools-followup-a02.md
.orchestration/acceptance/dotfiles-T128-orchestrator-tools-followup-a03.md
.orchestration/acceptance/dotfiles-T128-plan-007-review-a01.md
.orchestration/acceptance/dotfiles-T128-playbook-rules-a01-design-reset.md
.orchestration/acceptance/dotfiles-T128-playbook-rules-a01.md
.orchestration/acceptance/dotfiles-T128-playbook-rules-a02-design-reset.md
.orchestration/acceptance/dotfiles-T128-playbook-rules-a02.md
.orchestration/acceptance/dotfiles-T128-playbook-rules-a03-design-reset.md
.orchestration/acceptance/dotfiles-T128-playbook-rules-a03.md
.orchestration/acceptance/dotfiles-T128-playbook-rules-a04.md
.orchestration/acceptance/dotfiles-T128-playbook-rules-followup-a01.md
.orchestration/acceptance/dotfiles-T128-playbook-rules-redesign-a01.md
.orchestration/acceptance/dotfiles-T128-playbook-rules-redesign-a02.md
.orchestration/acceptance/dotfiles-T128-playbook-rules-redesign-a03.md
.orchestration/acceptance/dotfiles-T128-process-rules-a01-design-reset.md
.orchestration/acceptance/dotfiles-T128-process-rules-a01.md
.orchestration/acceptance/dotfiles-T128-process-rules-a02-design-reset.md
.orchestration/acceptance/dotfiles-T128-process-rules-a02.md
.orchestration/acceptance/dotfiles-T128-process-rules-a03-design-reset.md
.orchestration/acceptance/dotfiles-T128-process-rules-a03.md
.orchestration/acceptance/dotfiles-T128-process-rules-a04-design-reset.md
.orchestration/acceptance/dotfiles-T128-process-rules-a04.md
.orchestration/acceptance/dotfiles-T128-process-rules-a05-design-reset.md
.orchestration/acceptance/dotfiles-T128-process-rules-a05.md
.orchestration/acceptance/dotfiles-T128-process-rules-a06-design-reset.md
.orchestration/acceptance/dotfiles-T128-process-rules-a06.md
.orchestration/acceptance/dotfiles-T128-process-rules-a07.md
.orchestration/acceptance/dotfiles-T128-process-rules-redesign-a01.md
.orchestration/acceptance/dotfiles-T128-process-rules-redesign-a02.md
.orchestration/acceptance/dotfiles-T128-process-rules-redesign-a03.md
.orchestration/acceptance/dotfiles-T128-process-rules-redesign-a04.md
.orchestration/acceptance/dotfiles-T128-process-rules-redesign-a05.md
.orchestration/acceptance/dotfiles-T128-process-rules-redesign-a06.md
.orchestration/acceptance/dotfiles-T128-project-map-pane-open-a01-followup-a01.md
.orchestration/acceptance/dotfiles-T128-project-map-pane-open-a01.md
.orchestration/acceptance/dotfiles-T128-project-map-reload-hook-a01.md
.orchestration/acceptance/dotfiles-T128-project-map-reload-hook-followup-a01.md
.orchestration/acceptance/dotfiles-T128-regime-counters-a01-design-reset.md
.orchestration/acceptance/dotfiles-T128-regime-counters-a01.md
.orchestration/acceptance/dotfiles-T128-regime-counters-a02.md
.orchestration/acceptance/dotfiles-T128-regime-counters-redesign-a01.md
.orchestration/acceptance/dotfiles-T128-regime-v3-inv6-redesign-a01.md
.orchestration/acceptance/dotfiles-T128-rules-s1-replan-a01.md
.orchestration/acceptance/dotfiles-T128-rules-step8-a01.md
.orchestration/acceptance/dotfiles-T128-s1-replan-gate-a01.md
.orchestration/acceptance/dotfiles-T128-seat-launch-args-a01.md
.orchestration/acceptance/dotfiles-T128-seat-liveness-a01.md
.orchestration/acceptance/dotfiles-T128-seat-liveness-followup-a01.md
.orchestration/acceptance/dotfiles-T128-settings-hook-dedupe-a01.md
.orchestration/acceptance/dotfiles-T128-settings-hook-dedupe-followup-a01.md
.orchestration/acceptance/dotfiles-T128-task-checkers-a01.md
.orchestration/acceptance/dotfiles-T128-task-checkers-followup-a01.md
.orchestration/acceptance/dotfiles-T128-task-review-contracts-a01.md
.orchestration/acceptance/dotfiles-T128-task-review-phase-a-a01.md
.orchestration/acceptance/dotfiles-T128-task-review-phase1-a01.md
.orchestration/acceptance/dotfiles-T128-task-review-phase1-amend-a01.md
.orchestration/acceptance/dotfiles-T128-task-review-phase1-amend-a02.md
.orchestration/acceptance/dotfiles-T128-task-review-t718-a01.md
.orchestration/acceptance/dotfiles-T128-task-review-t718-a02.md
.orchestration/acceptance/dotfiles-T128-task-review-v1-v2-a01.md
.orchestration/acceptance/dotfiles-T128-v0-main-tests-a01.md
.orchestration/acceptance/dotfiles-T128-validator-offline-a01.md
.orchestration/acceptance/dotfiles-T128-worker-s1-stop-a01.md
.orchestration/acceptance/dotfiles-T128-worker-stop-and-watch-a01-design-reset.md
.orchestration/acceptance/dotfiles-T128-worker-stop-and-watch-a01.md
.orchestration/acceptance/dotfiles-T128-worker-stop-and-watch-a02.md
.orchestration/acceptance/dotfiles-T128-worker-stop-and-watch-redesign-a01.md
.orchestration/acceptance/dotfiles-T129-anthropic-auth-route-check-a01.md
.orchestration/acceptance/dotfiles-T129-anthropic-auth-route-check-followup-a01.md
.orchestration/acceptance/dotfiles-T129-assets-omp-hcom-a01.md
.orchestration/acceptance/dotfiles-T129-assets-omp-hcom-followup-a01.md
.orchestration/acceptance/dotfiles-T129-audit-inherit-replan-json-a01.md
.orchestration/acceptance/dotfiles-T129-doctor-sleep-disabled-a01.md
.orchestration/acceptance/dotfiles-T129-integration-seat-result-gate-cap-a01.md
.orchestration/acceptance/dotfiles-T129-normalised-comparison-lint-a01.md
.orchestration/acceptance/dotfiles-T129-orchestrator-load-mechanisms-a01.md
.orchestration/acceptance/dotfiles-T129-pstack-asset-a01.md
.orchestration/acceptance/dotfiles-T130-claude-sandbox-integration-a01.md
.orchestration/acceptance/dotfiles-T130-codex-local-review-exclusion-a01.md
.orchestration/acceptance/dotfiles-T130-sandbox-portability-a01.md
.orchestration/acceptance/dotfiles-T62-claude-auto-deny-a01.md
.orchestration/acceptance/dotfiles-T63-codex-execpolicy-forbidden-a01.md
.orchestration/acceptance/dotfiles-T64-codex-worker-never-network-a01.md
.orchestration/acceptance/dotfiles-T65-agent-stop-gate-a01.md
.orchestration/acceptance/dotfiles-T66-permgate-dead-lanes-a01.md
.orchestration/acceptance/dotfiles-T67-audit-task-level-a01.md
.orchestration/acceptance/dotfiles-T68-gate-audit-evidence-a01.md
.orchestration/acceptance/dotfiles-T69-protocol-docs-unification-a01.md
.orchestration/acceptance/dotfiles-T70-make-update-unattended-a01.md
.orchestration/acceptance/dotfiles-T71-generator-multi-target-a01.md
.orchestration/acceptance/dotfiles-T72-bootstrap-ci-pins-a01.md
.orchestration/acceptance/dotfiles-T73-tool-versions-from-config-a01.md
.orchestration/acceptance/dotfiles-T74-bootstrap-dead-code-a01.md
.orchestration/acceptance/dotfiles-T75-shell-dead-code-a01.md
.orchestration/acceptance/dotfiles-T76-ineffective-settings-a01.md
.orchestration/acceptance/dotfiles-T77-harness-dead-code-a01.md
.orchestration/acceptance/dotfiles-T77b-enforce-uv-hook-contract-a01.md
.orchestration/acceptance/dotfiles-T78-dead-docs-adh-a01.md
.orchestration/acceptance/dotfiles-T79-remove-adh-profile-a01.md
.orchestration/acceptance/dotfiles-T80-codex-command-hooks-a01.md
.orchestration/acceptance/dotfiles-T81-compactiondb-vendor-a01.md
.orchestration/acceptance/dotfiles-T81b-compactiondb-vendor-hygiene-a01.md
.orchestration/acceptance/dotfiles-T82-codex-compaction-hooks-a01.md
.orchestration/acceptance/dotfiles-T82b-codex-hook-trust-pins-a01.md
.orchestration/acceptance/dotfiles-T83-docs-diet-a01.md
.orchestration/acceptance/dotfiles-T84-orchestrator-kind-a01.md
.orchestration/acceptance/dotfiles-T85-launcher-orchestrator-kind-a01.md
.orchestration/acceptance/dotfiles-T86-codex-orchestrate-a01.md
.orchestration/acceptance/dotfiles-T88-parallel-execution-rule-a01.md
.orchestration/acceptance/dotfiles-T89-add-worker-same-workspace-a01.md
.orchestration/acceptance/dotfiles-T90-github-identity-separation-a01.md
.orchestration/acceptance/dotfiles-T90b-ruleset-sole-merger-a01.md
.orchestration/acceptance/dotfiles-T91-secret-scan-sk-boundary-a01.md
.orchestration/acceptance/dotfiles-T92-stop-gate-sandbox-placeholders-a01.md
.orchestration/acceptance/dotfiles-T93-gate-masked-feedback-bodies-a01.md
.orchestration/acceptance/dotfiles-T94-upgrade-pins-a01.md
.orchestration/acceptance/dotfiles-T95-sandbox-placeholder-files-on-disk-a01.md
.orchestration/acceptance/dotfiles-T96-codex-worker-gpt61-sol-high-a01.md
.orchestration/acceptance/dotfiles-T97-claude-sandbox-github-calls-a01.md
.orchestration/acceptance/dotfiles-T98-evidence-home-path-masking-a01.md
.orchestration/acceptance/dotfiles-T98b-runner-home-and-review-body-a01.md
.orchestration/acceptance/dotfiles-T98c-claude-seat-artifact-write-exception-a01.md
.orchestration/acceptance/dotfiles-T99-nix-plans-history-a01.md
.orchestration/acceptance/plan-003-final-pr.md
.orchestration/acceptance/plan-003-review-round-1.md
.orchestration/acceptance/plan-003-review-round-2.md
.orchestration/acceptance/plan-003.md
.orchestration/autoskill/runs/dot-ccstatusline-ubuntu26-hang-T59-a01.md
.orchestration/autoskill/runs/dot-ci-runner-label-pin-T58-a01.md
.orchestration/autoskill/runs/dot-formatter-hook-root-fix-T61-a01.md
.orchestration/autoskill/runs/dot-git-ignore-cc-writes-T56-a01.md
.orchestration/autoskill/runs/dot-macos-brew-untrusted-taps-T57-a01.md
.orchestration/autoskill/runs/dot-main-push-guard-revert-T60-a01.md
.orchestration/autoskill/runs/dot-ua-graph-refresh-T55-a01.md
.orchestration/autoskill/runs/dotfiles-T100-compactiondb-claude-symlink-note-a01.md
.orchestration/autoskill/runs/dotfiles-T101-codex-worker-profile-default-a01.md
.orchestration/autoskill/runs/dotfiles-T102-add-worker-credential-notice-a01.md
.orchestration/autoskill/runs/dotfiles-T103-gh-auth-stores-a01.md
.orchestration/autoskill/runs/dotfiles-T104-pins-2026-10-06-a01.md
.orchestration/autoskill/runs/dotfiles-T107-gh-stores-per-machine-a01.md
.orchestration/autoskill/runs/dotfiles-T108-one-login-per-machine-a01.md
.orchestration/autoskill/runs/dotfiles-T109-claude-worker-merge-deny-a01.md
.orchestration/autoskill/runs/dotfiles-T110-gh-auth-file-storage-a01.md
.orchestration/autoskill/runs/dotfiles-T111-project-map-subagent-a01.md
.orchestration/autoskill/runs/dotfiles-T112-pins-2026-10-07-a01.md
.orchestration/autoskill/runs/dotfiles-T113-codify-T111-lessons-a01.md
.orchestration/autoskill/runs/dotfiles-T114-canonical-clone-reconcile-a01.md
.orchestration/autoskill/runs/dotfiles-T115-worker-audit-xhigh-a01.md
.orchestration/autoskill/runs/dotfiles-T116-on-demand-workers-a01.md
.orchestration/autoskill/runs/dotfiles-T117-upgrade-outside-canonical-clone-a01.md
.orchestration/autoskill/runs/dotfiles-T118-rolling-tools-single-update-a01.md
.orchestration/autoskill/runs/dotfiles-T119-rolling-release-assets-a01.md
.orchestration/autoskill/runs/dotfiles-T120-npm-provenance-and-claude-channel-a01.md
.orchestration/autoskill/runs/dotfiles-T124-wave1-task-validator-a01.md
.orchestration/autoskill/runs/dotfiles-T124-wave3b-audit-grammar-a01.md
.orchestration/autoskill/runs/dotfiles-T128-ci-skip-orchestration-a01.md
.orchestration/autoskill/runs/dotfiles-T128-ci-skip-orchestration-a02.md
.orchestration/autoskill/runs/dotfiles-T128-gate-evidence-a02.md
.orchestration/autoskill/runs/dotfiles-T128-gate-evidence-a03.md
.orchestration/autoskill/runs/dotfiles-T128-gate-evidence-a04.md
.orchestration/autoskill/runs/dotfiles-T128-orchestrator-tools-a01.md
.orchestration/autoskill/runs/dotfiles-T128-orchestrator-tools-a02.md
.orchestration/autoskill/runs/dotfiles-T128-orchestrator-tools-a03.md
.orchestration/autoskill/runs/dotfiles-T128-orchestrator-tools-a04.md
.orchestration/autoskill/runs/dotfiles-T128-orchestrator-tools-a05.md
.orchestration/autoskill/runs/dotfiles-T128-playbook-rules-a02.md
.orchestration/autoskill/runs/dotfiles-T128-playbook-rules-a03.md
.orchestration/autoskill/runs/dotfiles-T128-playbook-rules-a04.md
.orchestration/autoskill/runs/dotfiles-T128-process-rules-a01.md
.orchestration/autoskill/runs/dotfiles-T128-process-rules-a02.md
.orchestration/autoskill/runs/dotfiles-T128-process-rules-a03.md
.orchestration/autoskill/runs/dotfiles-T128-process-rules-a04.md
.orchestration/autoskill/runs/dotfiles-T128-process-rules-a05.md
.orchestration/autoskill/runs/dotfiles-T128-process-rules-a06.md
.orchestration/autoskill/runs/dotfiles-T128-process-rules-a07.md
.orchestration/autoskill/runs/dotfiles-T128-regime-counters-a01.md
.orchestration/autoskill/runs/dotfiles-T128-regime-counters-a02.md
.orchestration/autoskill/runs/dotfiles-T128-v0-main-tests-a01.md
.orchestration/autoskill/runs/dotfiles-T128-worker-stop-and-watch-a01.md
.orchestration/autoskill/runs/dotfiles-T128-worker-stop-and-watch-a02.md
.orchestration/autoskill/runs/dotfiles-T62-claude-auto-deny-a01.md
.orchestration/autoskill/runs/dotfiles-T63-codex-execpolicy-forbidden-a01.md
.orchestration/autoskill/runs/dotfiles-T64-codex-worker-never-network-a01.md
.orchestration/autoskill/runs/dotfiles-T65-agent-stop-gate-a01.md
.orchestration/autoskill/runs/dotfiles-T66-permgate-dead-lanes-a01.md
.orchestration/autoskill/runs/dotfiles-T67-audit-task-level-a01.md
.orchestration/autoskill/runs/dotfiles-T68-gate-audit-evidence-a01.md
.orchestration/autoskill/runs/dotfiles-T69-protocol-docs-unification-a01.md
.orchestration/autoskill/runs/dotfiles-T70-make-update-unattended-a01.md
.orchestration/autoskill/runs/dotfiles-T71-generator-multi-target-a01.md
.orchestration/autoskill/runs/dotfiles-T72-bootstrap-ci-pins-a01.md
.orchestration/autoskill/runs/dotfiles-T73-tool-versions-from-config-a01.md
.orchestration/autoskill/runs/dotfiles-T74-bootstrap-dead-code-a01.md
.orchestration/autoskill/runs/dotfiles-T75-shell-dead-code-a01.md
.orchestration/autoskill/runs/dotfiles-T76-ineffective-settings-a01.md
.orchestration/autoskill/runs/dotfiles-T77-harness-dead-code-a01.md
.orchestration/autoskill/runs/dotfiles-T77b-enforce-uv-hook-contract-a01.md
.orchestration/autoskill/runs/dotfiles-T78-dead-docs-adh-a01.md
.orchestration/autoskill/runs/dotfiles-T79-remove-adh-profile-a01.md
.orchestration/autoskill/runs/dotfiles-T80-codex-command-hooks-a01.md
.orchestration/autoskill/runs/dotfiles-T81-compactiondb-vendor-a01.md
.orchestration/autoskill/runs/dotfiles-T81b-compactiondb-vendor-hygiene-a01.md
.orchestration/autoskill/runs/dotfiles-T82-codex-compaction-hooks-a01.md
.orchestration/autoskill/runs/dotfiles-T82b-codex-hook-trust-pins-a01.md
.orchestration/autoskill/runs/dotfiles-T83-docs-diet-a01.md
.orchestration/autoskill/runs/dotfiles-T84-orchestrator-kind-a01.md
.orchestration/autoskill/runs/dotfiles-T85-launcher-orchestrator-kind-a01.md
.orchestration/autoskill/runs/dotfiles-T86-codex-orchestrate-a01.md
.orchestration/autoskill/runs/dotfiles-T88-parallel-execution-rule-a01.md
.orchestration/autoskill/runs/dotfiles-T89-add-worker-same-workspace-a01.md
.orchestration/autoskill/runs/dotfiles-T90-github-identity-separation-a01.md
.orchestration/autoskill/runs/dotfiles-T90b-ruleset-sole-merger-a01.md
.orchestration/autoskill/runs/dotfiles-T91-secret-scan-sk-boundary-a01.md
.orchestration/autoskill/runs/dotfiles-T92-stop-gate-sandbox-placeholders-a01.md
.orchestration/autoskill/runs/dotfiles-T93-gate-masked-feedback-bodies-a01.md
.orchestration/autoskill/runs/dotfiles-T94-upgrade-pins-a01.md
.orchestration/autoskill/runs/dotfiles-T95-sandbox-placeholder-files-on-disk-a01.md
.orchestration/autoskill/runs/dotfiles-T96-codex-worker-gpt61-sol-high-a01.md
.orchestration/autoskill/runs/dotfiles-T97-claude-sandbox-github-calls-a01.md
.orchestration/autoskill/runs/dotfiles-T98-evidence-home-path-masking-a01.md
.orchestration/autoskill/runs/dotfiles-T98b-runner-home-and-review-body-a01.md
.orchestration/autoskill/runs/dotfiles-T98c-claude-seat-artifact-write-exception-a01.md
.orchestration/autoskill/runs/dotfiles-T99-nix-plans-history-a01.md
.orchestration/decisions.tsv
.orchestration/dotfiles-T128-aws-cli-macos-a01/autoskill.md
.orchestration/dotfiles-T128-aws-cli-macos-a01/learning.md
.orchestration/dotfiles-T128-aws-cli-macos-a01/report.md
.orchestration/dotfiles-T128-aws-cli-macos-a01/sandbox.md
.orchestration/dotfiles-T128-aws-cli-macos-a01/task.md
.orchestration/dotfiles-T128-aws-cli-macos-a01/validation.md
.orchestration/dotfiles-T128-chain-github-scripts-a01/autoskill.md
.orchestration/dotfiles-T128-chain-github-scripts-a01/learning.md
.orchestration/dotfiles-T128-chain-github-scripts-a01/report.md
.orchestration/dotfiles-T128-chain-github-scripts-a01/sandbox.md
.orchestration/dotfiles-T128-chain-github-scripts-a01/task.md
.orchestration/dotfiles-T128-chain-github-scripts-a01/validation.md
.orchestration/dotfiles-T128-chain-github-scripts-followup-a01/autoskill.md
.orchestration/dotfiles-T128-chain-github-scripts-followup-a01/learning.md
.orchestration/dotfiles-T128-chain-github-scripts-followup-a01/report.md
.orchestration/dotfiles-T128-chain-github-scripts-followup-a01/sandbox.md
.orchestration/dotfiles-T128-chain-github-scripts-followup-a01/task.md
.orchestration/dotfiles-T128-chain-github-scripts-followup-a01/validation.md
.orchestration/dotfiles-T128-chain-glue-integrate-a01/autoskill.md
.orchestration/dotfiles-T128-chain-glue-integrate-a01/learning.md
.orchestration/dotfiles-T128-chain-glue-integrate-a01/report.md
.orchestration/dotfiles-T128-chain-glue-integrate-a01/sandbox.md
.orchestration/dotfiles-T128-chain-glue-integrate-a01/task.md
.orchestration/dotfiles-T128-chain-glue-integrate-a01/validation.md
.orchestration/dotfiles-T128-chain-review-scripts-a01/autoskill.md
.orchestration/dotfiles-T128-chain-review-scripts-a01/learning.md
.orchestration/dotfiles-T128-chain-review-scripts-a01/report.md
.orchestration/dotfiles-T128-chain-review-scripts-a01/sandbox.md
.orchestration/dotfiles-T128-chain-review-scripts-a01/task.md
.orchestration/dotfiles-T128-chain-review-scripts-a01/validation.md
.orchestration/dotfiles-T128-chain-review-scripts-followup-a01/autoskill.md
.orchestration/dotfiles-T128-chain-review-scripts-followup-a01/learning.md
.orchestration/dotfiles-T128-chain-review-scripts-followup-a01/report.md
.orchestration/dotfiles-T128-chain-review-scripts-followup-a01/revise.yaml
.orchestration/dotfiles-T128-chain-review-scripts-followup-a01/sandbox.md
.orchestration/dotfiles-T128-chain-review-scripts-followup-a01/task.md
.orchestration/dotfiles-T128-chain-review-scripts-followup-a01/validation.md
.orchestration/dotfiles-T128-chain-review-scripts-followup-a02/autoskill.md
.orchestration/dotfiles-T128-chain-review-scripts-followup-a02/learning.md
.orchestration/dotfiles-T128-chain-review-scripts-followup-a02/report.md
.orchestration/dotfiles-T128-chain-review-scripts-followup-a02/sandbox.md
.orchestration/dotfiles-T128-chain-review-scripts-followup-a02/task.md
.orchestration/dotfiles-T128-chain-review-scripts-followup-a02/validation.md
.orchestration/dotfiles-T128-chain-review-scripts-followup-a03/autoskill.md
.orchestration/dotfiles-T128-chain-review-scripts-followup-a03/learning.md
.orchestration/dotfiles-T128-chain-review-scripts-followup-a03/report.md
.orchestration/dotfiles-T128-chain-review-scripts-followup-a03/sandbox.md
.orchestration/dotfiles-T128-chain-review-scripts-followup-a03/task.md
.orchestration/dotfiles-T128-chain-review-scripts-followup-a03/validation.md
.orchestration/dotfiles-T128-chain-review-scripts-followup-a04/autoskill.md
.orchestration/dotfiles-T128-chain-review-scripts-followup-a04/learning.md
.orchestration/dotfiles-T128-chain-review-scripts-followup-a04/report.md
.orchestration/dotfiles-T128-chain-review-scripts-followup-a04/sandbox.md
.orchestration/dotfiles-T128-chain-review-scripts-followup-a04/task.md
.orchestration/dotfiles-T128-chain-review-scripts-followup-a04/validation.md
.orchestration/dotfiles-T128-ci-skip-orchestration-a01/autoskill.md
.orchestration/dotfiles-T128-ci-skip-orchestration-a01/learning.md
.orchestration/dotfiles-T128-ci-skip-orchestration-a01/report.md
.orchestration/dotfiles-T128-ci-skip-orchestration-a01/revise.yaml
.orchestration/dotfiles-T128-ci-skip-orchestration-a01/sandbox.md
.orchestration/dotfiles-T128-ci-skip-orchestration-a01/task.md
.orchestration/dotfiles-T128-ci-skip-orchestration-a01/validation.md
.orchestration/dotfiles-T128-ci-skip-orchestration-a02/autoskill.md
.orchestration/dotfiles-T128-ci-skip-orchestration-a02/learning.md
.orchestration/dotfiles-T128-ci-skip-orchestration-a02/report.md
.orchestration/dotfiles-T128-ci-skip-orchestration-a02/sandbox.md
.orchestration/dotfiles-T128-ci-skip-orchestration-a02/task.md
.orchestration/dotfiles-T128-ci-skip-orchestration-a02/validation.md
.orchestration/dotfiles-T128-gate-evidence-a01/autoskill.md
.orchestration/dotfiles-T128-gate-evidence-a01/learning.md
.orchestration/dotfiles-T128-gate-evidence-a01/report.md
.orchestration/dotfiles-T128-gate-evidence-a01/sandbox.md
.orchestration/dotfiles-T128-gate-evidence-a01/task.md
.orchestration/dotfiles-T128-gate-evidence-a01/validation.md
.orchestration/dotfiles-T128-gate-evidence-a02/autoskill.md
.orchestration/dotfiles-T128-gate-evidence-a02/learning.md
.orchestration/dotfiles-T128-gate-evidence-a02/report.md
.orchestration/dotfiles-T128-gate-evidence-a02/sandbox.md
.orchestration/dotfiles-T128-gate-evidence-a02/task.md
.orchestration/dotfiles-T128-gate-evidence-a02/validation.md
.orchestration/dotfiles-T128-gate-evidence-a03/autoskill.md
.orchestration/dotfiles-T128-gate-evidence-a03/learning.md
.orchestration/dotfiles-T128-gate-evidence-a03/report.md
.orchestration/dotfiles-T128-gate-evidence-a03/sandbox.md
.orchestration/dotfiles-T128-gate-evidence-a03/task.md
.orchestration/dotfiles-T128-gate-evidence-a03/validation.md
.orchestration/dotfiles-T128-gate-evidence-a04/autoskill.md
.orchestration/dotfiles-T128-gate-evidence-a04/learning.md
.orchestration/dotfiles-T128-gate-evidence-a04/report.md
.orchestration/dotfiles-T128-gate-evidence-a04/sandbox.md
.orchestration/dotfiles-T128-gate-evidence-a04/task.md
.orchestration/dotfiles-T128-gate-evidence-a04/validation.md
.orchestration/dotfiles-T128-gate-wrapper-path-a01/autoskill.md
.orchestration/dotfiles-T128-gate-wrapper-path-a01/learning.md
.orchestration/dotfiles-T128-gate-wrapper-path-a01/report.md
.orchestration/dotfiles-T128-gate-wrapper-path-a01/sandbox.md
.orchestration/dotfiles-T128-gate-wrapper-path-a01/task.md
.orchestration/dotfiles-T128-gate-wrapper-path-a01/validation.md
.orchestration/dotfiles-T128-orchestrator-tools-a01/autoskill.md
.orchestration/dotfiles-T128-orchestrator-tools-a01/learning.md
.orchestration/dotfiles-T128-orchestrator-tools-a01/report.md
.orchestration/dotfiles-T128-orchestrator-tools-a01/sandbox.md
.orchestration/dotfiles-T128-orchestrator-tools-a01/task.md
.orchestration/dotfiles-T128-orchestrator-tools-a01/validation.md
.orchestration/dotfiles-T128-orchestrator-tools-a02/autoskill.md
.orchestration/dotfiles-T128-orchestrator-tools-a02/learning.md
.orchestration/dotfiles-T128-orchestrator-tools-a02/report.md
.orchestration/dotfiles-T128-orchestrator-tools-a02/sandbox.md
.orchestration/dotfiles-T128-orchestrator-tools-a02/task.md
.orchestration/dotfiles-T128-orchestrator-tools-a02/validation.md
.orchestration/dotfiles-T128-orchestrator-tools-a03/autoskill.md
.orchestration/dotfiles-T128-orchestrator-tools-a03/learning.md
.orchestration/dotfiles-T128-orchestrator-tools-a03/report.md
.orchestration/dotfiles-T128-orchestrator-tools-a03/revise.yaml
.orchestration/dotfiles-T128-orchestrator-tools-a03/sandbox.md
.orchestration/dotfiles-T128-orchestrator-tools-a03/task.md
.orchestration/dotfiles-T128-orchestrator-tools-a03/validation.md
.orchestration/dotfiles-T128-orchestrator-tools-a04/autoskill.md
.orchestration/dotfiles-T128-orchestrator-tools-a04/learning.md
.orchestration/dotfiles-T128-orchestrator-tools-a04/report.md
.orchestration/dotfiles-T128-orchestrator-tools-a04/revise.yaml
.orchestration/dotfiles-T128-orchestrator-tools-a04/sandbox.md
.orchestration/dotfiles-T128-orchestrator-tools-a04/task.md
.orchestration/dotfiles-T128-orchestrator-tools-a04/validation.md
.orchestration/dotfiles-T128-orchestrator-tools-a05/autoskill.md
.orchestration/dotfiles-T128-orchestrator-tools-a05/learning.md
.orchestration/dotfiles-T128-orchestrator-tools-a05/report.md
.orchestration/dotfiles-T128-orchestrator-tools-a05/sandbox.md
.orchestration/dotfiles-T128-orchestrator-tools-a05/task.md
.orchestration/dotfiles-T128-orchestrator-tools-a05/validation.md
.orchestration/dotfiles-T128-orchestrator-tools-a06/autoskill.md
.orchestration/dotfiles-T128-orchestrator-tools-a06/learning.md
.orchestration/dotfiles-T128-orchestrator-tools-a06/report.md
.orchestration/dotfiles-T128-orchestrator-tools-a06/sandbox.md
.orchestration/dotfiles-T128-orchestrator-tools-a06/task.md
.orchestration/dotfiles-T128-orchestrator-tools-a06/validation.md
.orchestration/dotfiles-T128-orchestrator-tools-followup-a01/autoskill.md
.orchestration/dotfiles-T128-orchestrator-tools-followup-a01/learning.md
.orchestration/dotfiles-T128-orchestrator-tools-followup-a01/report.md
.orchestration/dotfiles-T128-orchestrator-tools-followup-a01/sandbox.md
.orchestration/dotfiles-T128-orchestrator-tools-followup-a01/task.md
.orchestration/dotfiles-T128-orchestrator-tools-followup-a01/validation.md
.orchestration/dotfiles-T128-orchestrator-tools-followup-a02/autoskill.md
.orchestration/dotfiles-T128-orchestrator-tools-followup-a02/learning.md
.orchestration/dotfiles-T128-orchestrator-tools-followup-a02/report.md
.orchestration/dotfiles-T128-orchestrator-tools-followup-a02/sandbox.md
.orchestration/dotfiles-T128-orchestrator-tools-followup-a02/task.md
.orchestration/dotfiles-T128-orchestrator-tools-followup-a02/validation.md
.orchestration/dotfiles-T128-orchestrator-tools-followup-a03/autoskill.md
.orchestration/dotfiles-T128-orchestrator-tools-followup-a03/learning.md
.orchestration/dotfiles-T128-orchestrator-tools-followup-a03/report.md
.orchestration/dotfiles-T128-orchestrator-tools-followup-a03/revise.yaml
.orchestration/dotfiles-T128-orchestrator-tools-followup-a03/sandbox.md
.orchestration/dotfiles-T128-orchestrator-tools-followup-a03/task.md
.orchestration/dotfiles-T128-orchestrator-tools-followup-a03/validation.md
.orchestration/dotfiles-T128-playbook-rules-a01/autoskill.md
.orchestration/dotfiles-T128-playbook-rules-a01/learning.md
.orchestration/dotfiles-T128-playbook-rules-a01/report.md
.orchestration/dotfiles-T128-playbook-rules-a01/sandbox.md
.orchestration/dotfiles-T128-playbook-rules-a01/task.md
.orchestration/dotfiles-T128-playbook-rules-a01/validation.md
.orchestration/dotfiles-T128-playbook-rules-a02/autoskill.md
.orchestration/dotfiles-T128-playbook-rules-a02/learning.md
.orchestration/dotfiles-T128-playbook-rules-a02/report.md
.orchestration/dotfiles-T128-playbook-rules-a02/sandbox.md
.orchestration/dotfiles-T128-playbook-rules-a02/task.md
.orchestration/dotfiles-T128-playbook-rules-a02/validation.md
.orchestration/dotfiles-T128-playbook-rules-a03/autoskill.md
.orchestration/dotfiles-T128-playbook-rules-a03/learning.md
.orchestration/dotfiles-T128-playbook-rules-a03/report.md
.orchestration/dotfiles-T128-playbook-rules-a03/sandbox.md
.orchestration/dotfiles-T128-playbook-rules-a03/task.md
.orchestration/dotfiles-T128-playbook-rules-a03/validation.md
.orchestration/dotfiles-T128-playbook-rules-a04/autoskill.md
.orchestration/dotfiles-T128-playbook-rules-a04/learning.md
.orchestration/dotfiles-T128-playbook-rules-a04/report.md
.orchestration/dotfiles-T128-playbook-rules-a04/revise.yaml
.orchestration/dotfiles-T128-playbook-rules-a04/sandbox.md
.orchestration/dotfiles-T128-playbook-rules-a04/task.md
.orchestration/dotfiles-T128-playbook-rules-a04/validation.md
.orchestration/dotfiles-T128-playbook-rules-followup-a01/autoskill.md
.orchestration/dotfiles-T128-playbook-rules-followup-a01/learning.md
.orchestration/dotfiles-T128-playbook-rules-followup-a01/report.md
.orchestration/dotfiles-T128-playbook-rules-followup-a01/sandbox.md
.orchestration/dotfiles-T128-playbook-rules-followup-a01/task.md
.orchestration/dotfiles-T128-playbook-rules-followup-a01/validation.md
.orchestration/dotfiles-T128-process-rules-a01/autoskill.md
.orchestration/dotfiles-T128-process-rules-a01/learning.md
.orchestration/dotfiles-T128-process-rules-a01/report.md
.orchestration/dotfiles-T128-process-rules-a01/revise.yaml
.orchestration/dotfiles-T128-process-rules-a01/sandbox.md
.orchestration/dotfiles-T128-process-rules-a01/task.md
.orchestration/dotfiles-T128-process-rules-a01/validation.md
.orchestration/dotfiles-T128-process-rules-a02/autoskill.md
.orchestration/dotfiles-T128-process-rules-a02/learning.md
.orchestration/dotfiles-T128-process-rules-a02/report.md
.orchestration/dotfiles-T128-process-rules-a02/revise.yaml
.orchestration/dotfiles-T128-process-rules-a02/sandbox.md
.orchestration/dotfiles-T128-process-rules-a02/task.md
.orchestration/dotfiles-T128-process-rules-a02/validation.md
.orchestration/dotfiles-T128-process-rules-a03/autoskill.md
.orchestration/dotfiles-T128-process-rules-a03/learning.md
.orchestration/dotfiles-T128-process-rules-a03/report.md
.orchestration/dotfiles-T128-process-rules-a03/revise.yaml
.orchestration/dotfiles-T128-process-rules-a03/sandbox.md
.orchestration/dotfiles-T128-process-rules-a03/task.md
.orchestration/dotfiles-T128-process-rules-a03/validation.md
.orchestration/dotfiles-T128-process-rules-a04/autoskill.md
.orchestration/dotfiles-T128-process-rules-a04/learning.md
.orchestration/dotfiles-T128-process-rules-a04/report.md
.orchestration/dotfiles-T128-process-rules-a04/sandbox.md
.orchestration/dotfiles-T128-process-rules-a04/task.md
.orchestration/dotfiles-T128-process-rules-a04/validation.md
.orchestration/dotfiles-T128-process-rules-a05/autoskill.md
.orchestration/dotfiles-T128-process-rules-a05/learning.md
.orchestration/dotfiles-T128-process-rules-a05/report.md
.orchestration/dotfiles-T128-process-rules-a05/revise.yaml
.orchestration/dotfiles-T128-process-rules-a05/sandbox.md
.orchestration/dotfiles-T128-process-rules-a05/task.md
.orchestration/dotfiles-T128-process-rules-a05/validation.md
.orchestration/dotfiles-T128-process-rules-a06/autoskill.md
.orchestration/dotfiles-T128-process-rules-a06/learning.md
.orchestration/dotfiles-T128-process-rules-a06/report.md
.orchestration/dotfiles-T128-process-rules-a06/sandbox.md
.orchestration/dotfiles-T128-process-rules-a06/task.md
.orchestration/dotfiles-T128-process-rules-a06/validation.md
.orchestration/dotfiles-T128-process-rules-a07/autoskill.md
.orchestration/dotfiles-T128-process-rules-a07/learning.md
.orchestration/dotfiles-T128-process-rules-a07/report.md
.orchestration/dotfiles-T128-process-rules-a07/sandbox.md
.orchestration/dotfiles-T128-process-rules-a07/task.md
.orchestration/dotfiles-T128-process-rules-a07/validation.md
.orchestration/dotfiles-T128-project-map-pane-open-a01-followup-a01/autoskill.md
.orchestration/dotfiles-T128-project-map-pane-open-a01-followup-a01/learning.md
.orchestration/dotfiles-T128-project-map-pane-open-a01-followup-a01/project-map-worker-crit.json
.orchestration/dotfiles-T128-project-map-pane-open-a01-followup-a01/project-map-worker-review-receipt.md
.orchestration/dotfiles-T128-project-map-pane-open-a01-followup-a01/report.md
.orchestration/dotfiles-T128-project-map-pane-open-a01-followup-a01/revise.yaml
.orchestration/dotfiles-T128-project-map-pane-open-a01-followup-a01/sandbox.md
.orchestration/dotfiles-T128-project-map-pane-open-a01-followup-a01/task.md
.orchestration/dotfiles-T128-project-map-pane-open-a01-followup-a01/validation.md
.orchestration/dotfiles-T128-project-map-pane-open-a01/20261015_001500_done.md
.orchestration/dotfiles-T128-project-map-pane-open-a01/20261015_001500_plan.md
.orchestration/dotfiles-T128-project-map-pane-open-a01/autoskill.md
.orchestration/dotfiles-T128-project-map-pane-open-a01/dotfiles-T128-project-map-pane-open-a01-worker-crit.json
.orchestration/dotfiles-T128-project-map-pane-open-a01/dotfiles-T128-project-map-pane-open-a01-worker-review-receipt.md
.orchestration/dotfiles-T128-project-map-pane-open-a01/learning.md
.orchestration/dotfiles-T128-project-map-pane-open-a01/report.md
.orchestration/dotfiles-T128-project-map-pane-open-a01/result/report.md
.orchestration/dotfiles-T128-project-map-pane-open-a01/result/validation.md
.orchestration/dotfiles-T128-project-map-pane-open-a01/sandbox.md
.orchestration/dotfiles-T128-project-map-pane-open-a01/task.md
.orchestration/dotfiles-T128-project-map-pane-open-a01/validation.md
.orchestration/dotfiles-T128-project-map-reload-hook-a01/autoskill.md
.orchestration/dotfiles-T128-project-map-reload-hook-a01/dotfiles-T128-project-map-reload-hook-a01-worker-crit.json
.orchestration/dotfiles-T128-project-map-reload-hook-a01/dotfiles-T128-project-map-reload-hook-a01-worker-review-receipt.md
.orchestration/dotfiles-T128-project-map-reload-hook-a01/learning.md
.orchestration/dotfiles-T128-project-map-reload-hook-a01/report.md
.orchestration/dotfiles-T128-project-map-reload-hook-a01/sandbox.md
.orchestration/dotfiles-T128-project-map-reload-hook-a01/task.md
.orchestration/dotfiles-T128-project-map-reload-hook-a01/validation.md
.orchestration/dotfiles-T128-project-map-reload-hook-followup-a01/20261015_004907_done.md
.orchestration/dotfiles-T128-project-map-reload-hook-followup-a01/20261015_004907_plan.md
.orchestration/dotfiles-T128-project-map-reload-hook-followup-a01/autoskill.md
.orchestration/dotfiles-T128-project-map-reload-hook-followup-a01/dotfiles-T128-project-map-reload-hook-followup-a01-worker-crit.json
.orchestration/dotfiles-T128-project-map-reload-hook-followup-a01/dotfiles-T128-project-map-reload-hook-followup-a01-worker-review-receipt.md
.orchestration/dotfiles-T128-project-map-reload-hook-followup-a01/learning.md
.orchestration/dotfiles-T128-project-map-reload-hook-followup-a01/report.md
.orchestration/dotfiles-T128-project-map-reload-hook-followup-a01/result/report.md
.orchestration/dotfiles-T128-project-map-reload-hook-followup-a01/result/validation.md
.orchestration/dotfiles-T128-project-map-reload-hook-followup-a01/ruff-base.json
.orchestration/dotfiles-T128-project-map-reload-hook-followup-a01/ruff-current.json
.orchestration/dotfiles-T128-project-map-reload-hook-followup-a01/sandbox.md
.orchestration/dotfiles-T128-project-map-reload-hook-followup-a01/task.md
.orchestration/dotfiles-T128-project-map-reload-hook-followup-a01/validation.md
.orchestration/dotfiles-T128-regime-counters-a01/task.md
.orchestration/dotfiles-T128-regime-counters-a02/task.md
.orchestration/dotfiles-T128-rules-step8-a01/20261015_231106_done.md
.orchestration/dotfiles-T128-rules-step8-a01/20261015_231106_plan.md
.orchestration/dotfiles-T128-rules-step8-a01/amend5/autoskill.md
.orchestration/dotfiles-T128-rules-step8-a01/amend5/bot-inline.json
.orchestration/dotfiles-T128-rules-step8-a01/amend5/bot-receipts.json
.orchestration/dotfiles-T128-rules-step8-a01/amend5/bot-result.json
.orchestration/dotfiles-T128-rules-step8-a01/amend5/bot-reviews.json
.orchestration/dotfiles-T128-rules-step8-a01/amend5/bot-summaries.json
.orchestration/dotfiles-T128-rules-step8-a01/amend5/checks.txt
.orchestration/dotfiles-T128-rules-step8-a01/amend5/ci-watch.txt
.orchestration/dotfiles-T128-rules-step8-a01/amend5/commit.txt
.orchestration/dotfiles-T128-rules-step8-a01/amend5/final-ci.txt
.orchestration/dotfiles-T128-rules-step8-a01/amend5/head-proof.txt
.orchestration/dotfiles-T128-rules-step8-a01/amend5/learning.md
.orchestration/dotfiles-T128-rules-step8-a01/amend5/previous-learning.md
.orchestration/dotfiles-T128-rules-step8-a01/amend5/previous-report.md
.orchestration/dotfiles-T128-rules-step8-a01/amend5/previous-sandbox.md
.orchestration/dotfiles-T128-rules-step8-a01/amend5/previous-validation.md
.orchestration/dotfiles-T128-rules-step8-a01/amend5/publication.txt
.orchestration/dotfiles-T128-rules-step8-a01/amend5/push.txt
.orchestration/dotfiles-T128-rules-step8-a01/amend5/red.txt
.orchestration/dotfiles-T128-rules-step8-a01/amend5/render.txt
.orchestration/dotfiles-T128-rules-step8-a01/amend5/report.md
.orchestration/dotfiles-T128-rules-step8-a01/amend5/review-gate.txt
.orchestration/dotfiles-T128-rules-step8-a01/amend5/sandbox.md
.orchestration/dotfiles-T128-rules-step8-a01/amend5/tests.txt
.orchestration/dotfiles-T128-rules-step8-a01/amend5/validation.md
.orchestration/dotfiles-T128-rules-step8-a01/amend6/acceptance-pr.json
.orchestration/dotfiles-T128-rules-step8-a01/amend6/advisory-owner.txt
.orchestration/dotfiles-T128-rules-step8-a01/amend6/autoskill.md
.orchestration/dotfiles-T128-rules-step8-a01/amend6/bot-inline.json
.orchestration/dotfiles-T128-rules-step8-a01/amend6/bot-receipts.json
.orchestration/dotfiles-T128-rules-step8-a01/amend6/bot-result.json
.orchestration/dotfiles-T128-rules-step8-a01/amend6/bot-reviews.json
.orchestration/dotfiles-T128-rules-step8-a01/amend6/bot-summaries.json
.orchestration/dotfiles-T128-rules-step8-a01/amend6/checks.txt
.orchestration/dotfiles-T128-rules-step8-a01/amend6/ci-watch.txt
.orchestration/dotfiles-T128-rules-step8-a01/amend6/commit.txt
.orchestration/dotfiles-T128-rules-step8-a01/amend6/final-ci.txt
.orchestration/dotfiles-T128-rules-step8-a01/amend6/final-pr.json
.orchestration/dotfiles-T128-rules-step8-a01/amend6/head-proof.txt
.orchestration/dotfiles-T128-rules-step8-a01/amend6/learning.md
.orchestration/dotfiles-T128-rules-step8-a01/amend6/previous-validation.md
.orchestration/dotfiles-T128-rules-step8-a01/amend6/publication.txt
.orchestration/dotfiles-T128-rules-step8-a01/amend6/push.txt
.orchestration/dotfiles-T128-rules-step8-a01/amend6/red.txt
.orchestration/dotfiles-T128-rules-step8-a01/amend6/render-format.txt
.orchestration/dotfiles-T128-rules-step8-a01/amend6/report.md
.orchestration/dotfiles-T128-rules-step8-a01/amend6/review-gate.txt
.orchestration/dotfiles-T128-rules-step8-a01/amend6/sandbox.md
.orchestration/dotfiles-T128-rules-step8-a01/amend6/tests.txt
.orchestration/dotfiles-T128-rules-step8-a01/amend6/validation.md
.orchestration/dotfiles-T128-rules-step8-a01/autoskill.md
.orchestration/dotfiles-T128-rules-step8-a01/bot-comments.json
.orchestration/dotfiles-T128-rules-step8-a01/bot-final-summary.json
.orchestration/dotfiles-T128-rules-step8-a01/bot-issue-comments.json
.orchestration/dotfiles-T128-rules-step8-a01/bot-reviews.json
.orchestration/dotfiles-T128-rules-step8-a01/bot-status.txt
.orchestration/dotfiles-T128-rules-step8-a01/ci-watch.txt
.orchestration/dotfiles-T128-rules-step8-a01/dotfiles-T128-rules-step8-a01-worker-crit.json
.orchestration/dotfiles-T128-rules-step8-a01/dotfiles-T128-rules-step8-a01-worker-review-receipt.md
.orchestration/dotfiles-T128-rules-step8-a01/learning.md
.orchestration/dotfiles-T128-rules-step8-a01/pr-body.md
.orchestration/dotfiles-T128-rules-step8-a01/report.md
.orchestration/dotfiles-T128-rules-step8-a01/revise.yaml
.orchestration/dotfiles-T128-rules-step8-a01/round2/autoskill.md
.orchestration/dotfiles-T128-rules-step8-a01/round2/bot-comments.json
.orchestration/dotfiles-T128-rules-step8-a01/round2/bot-final-comments.json
.orchestration/dotfiles-T128-rules-step8-a01/round2/bot-final-reviews.json
.orchestration/dotfiles-T128-rules-step8-a01/round2/bot-issue-comments.json
.orchestration/dotfiles-T128-rules-step8-a01/round2/bot-reviews.json
.orchestration/dotfiles-T128-rules-step8-a01/round2/bot-status.txt
.orchestration/dotfiles-T128-rules-step8-a01/round2/ci-watch.txt
.orchestration/dotfiles-T128-rules-step8-a01/round2/learning.md
.orchestration/dotfiles-T128-rules-step8-a01/round2/previous-bot-comments.json
.orchestration/dotfiles-T128-rules-step8-a01/round2/previous-bot-final-summary.json
.orchestration/dotfiles-T128-rules-step8-a01/round2/previous-bot-issue-comments.json
.orchestration/dotfiles-T128-rules-step8-a01/round2/previous-bot-reviews.json
.orchestration/dotfiles-T128-rules-step8-a01/round2/previous-bot-status.txt
.orchestration/dotfiles-T128-rules-step8-a01/round2/previous-ci-watch.txt
.orchestration/dotfiles-T128-rules-step8-a01/round2/report.md
.orchestration/dotfiles-T128-rules-step8-a01/round2/sandbox.md
.orchestration/dotfiles-T128-rules-step8-a01/round2/threads.txt
.orchestration/dotfiles-T128-rules-step8-a01/round2/validation.md
.orchestration/dotfiles-T128-rules-step8-a01/sandbox.md
.orchestration/dotfiles-T128-rules-step8-a01/task.md
.orchestration/dotfiles-T128-rules-step8-a01/validation.md
.orchestration/dotfiles-T128-s1-replan-gate-a01/autoskill.md
.orchestration/dotfiles-T128-s1-replan-gate-a01/learning.md
.orchestration/dotfiles-T128-s1-replan-gate-a01/report-final.md
.orchestration/dotfiles-T128-s1-replan-gate-a01/report.md
.orchestration/dotfiles-T128-s1-replan-gate-a01/revise.yaml
.orchestration/dotfiles-T128-s1-replan-gate-a01/s1-worker-crit.json
.orchestration/dotfiles-T128-s1-replan-gate-a01/s1-worker-review-receipt.md
.orchestration/dotfiles-T128-s1-replan-gate-a01/sandbox.md
.orchestration/dotfiles-T128-s1-replan-gate-a01/task.md
.orchestration/dotfiles-T128-s1-replan-gate-a01/validation-final.md
.orchestration/dotfiles-T128-s1-replan-gate-a01/validation.md
.orchestration/dotfiles-T128-seat-liveness-a01/autoskill.md
.orchestration/dotfiles-T128-seat-liveness-a01/learning.md
.orchestration/dotfiles-T128-seat-liveness-a01/report.md
.orchestration/dotfiles-T128-seat-liveness-a01/revise.yaml
.orchestration/dotfiles-T128-seat-liveness-a01/sandbox.md
.orchestration/dotfiles-T128-seat-liveness-a01/task.md
.orchestration/dotfiles-T128-seat-liveness-a01/validation.md
.orchestration/dotfiles-T128-seat-liveness-followup-a01/autoskill.md
.orchestration/dotfiles-T128-seat-liveness-followup-a01/learning.md
.orchestration/dotfiles-T128-seat-liveness-followup-a01/report.md
.orchestration/dotfiles-T128-seat-liveness-followup-a01/sandbox.md
.orchestration/dotfiles-T128-seat-liveness-followup-a01/task.md
.orchestration/dotfiles-T128-seat-liveness-followup-a01/validation.md
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/20261015_052953_done.md
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/20261015_052953_plan.md
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/20261015_052953_todo.md
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend1/autoskill.md
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend1/bot-comments.json
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend1/bot-final-comments.json
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend1/bot-final-reviews.json
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend1/bot-issue-comments.json
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend1/bot-reviews.json
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend1/bot-status.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend1/ci-watch.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend1/learning.md
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend1/report.md
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend1/sandbox.md
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend1/validation.md
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend2/autoskill.md
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend2/bot-inline.json
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend2/bot-receipts.json
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend2/bot-result.json
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend2/bot-reviews.json
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend2/bot-summaries.json
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend2/checks.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend2/ci-watch.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend2/commit.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend2/compact-chain-repro.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend2/final-ci.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend2/final-tests.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend2/head-proof.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend2/learning.md
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend2/previous-validation.md
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend2/publication.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend2/push.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend2/red.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend2/render.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend2/report.md
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend2/review-gate.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend2/sandbox.md
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend2/source-format-baseline.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend2/tests.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend2/validation.md
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend3/autoskill.md
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend3/bot-inline.json
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend3/bot-receipts.json
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend3/bot-result.json
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend3/bot-reviews.json
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend3/bot-summaries.json
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend3/checks.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend3/ci-watch.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend3/commit.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend3/final-ci.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend3/final-pr.json
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend3/head-proof.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend3/learning.md
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend3/pr-blocker-description.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend3/previous-validation.md
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend3/project-local-repro.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend3/publication.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend3/push.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend3/red.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend3/render.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend3/report.md
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend3/review-gate.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend3/sandbox.md
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend3/source-format-baseline.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend3/tests.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend3/validation.md
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend4/checks.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend4/interpreter-chain-repro.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend4/peer-regression-red.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend4/peer-review-pending.json
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend4/previous-validation.md
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend4/red.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend4/render.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend4/review-gate-blocked.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend4/source-format-baseline.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend4/tests.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend5/acceptance-pr.json
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend5/autoskill.md
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend5/bot-inline.json
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend5/bot-receipts.json
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend5/bot-result.json
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend5/bot-reviews.json
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend5/bot-summaries.json
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend5/checks.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend5/ci-progress.json
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend5/ci-watch.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend5/commit.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend5/final-checks.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend5/head-proof.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend5/learning.md
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend5/pr-before.json
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend5/previous-validation.md
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend5/publication.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend5/push.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend5/red.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend5/render.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend5/report.md
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend5/review-gate.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend5/sandbox.md
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend5/source-format-baseline.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend5/tests.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/amend5/validation.md
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/autoskill.md
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/dotfiles-T128-settings-hook-dedupe-a01-worker-crit.json
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/dotfiles-T128-settings-hook-dedupe-a01-worker-review-receipt.md
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/evidence2/autoskill.md
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/evidence2/bot-inline.json
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/evidence2/bot-receipts.json
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/evidence2/bot-result.json
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/evidence2/bot-reviews.json
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/evidence2/bot-summaries.json
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/evidence2/chained-command-repro-corrected.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/evidence2/chained-command-repro.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/evidence2/ci-watch.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/evidence2/commit.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/evidence2/final-ci.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/evidence2/final-local-gate.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/evidence2/final-pr.json
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/evidence2/head-proof.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/evidence2/learning.md
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/evidence2/local-gate.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/evidence2/previous-validation.md
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/evidence2/publication.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/evidence2/push.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/evidence2/report.md
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/evidence2/sandbox.md
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/evidence2/validation.md
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/learning.md
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/pr-body.md
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/report.md
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/result/autoskill.md
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/result/bot-comments.json
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/result/bot-issue-comments.json
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/result/bot-reviews.json
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/result/bot-status.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/result/ci-watch.txt
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/result/learning.md
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/result/report.md
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/result/sandbox.md
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/result/validation.md
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/revise.yaml
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/ruff-base.json
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/ruff-current.json
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/sandbox.md
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/task.md
.orchestration/dotfiles-T128-settings-hook-dedupe-a01/validation.md
.orchestration/dotfiles-T128-settings-hook-dedupe-followup-a01/autoskill.md
.orchestration/dotfiles-T128-settings-hook-dedupe-followup-a01/learning.md
.orchestration/dotfiles-T128-settings-hook-dedupe-followup-a01/report.md
.orchestration/dotfiles-T128-settings-hook-dedupe-followup-a01/sandbox.md
.orchestration/dotfiles-T128-settings-hook-dedupe-followup-a01/task.md
.orchestration/dotfiles-T128-settings-hook-dedupe-followup-a01/validation.md
.orchestration/dotfiles-T128-task-checkers-a01/autoskill.md
.orchestration/dotfiles-T128-task-checkers-a01/learning.md
.orchestration/dotfiles-T128-task-checkers-a01/report.md
.orchestration/dotfiles-T128-task-checkers-a01/sandbox.md
.orchestration/dotfiles-T128-task-checkers-a01/task.md
.orchestration/dotfiles-T128-task-checkers-a01/validation.md
.orchestration/dotfiles-T128-task-checkers-followup-a01/autoskill.md
.orchestration/dotfiles-T128-task-checkers-followup-a01/learning.md
.orchestration/dotfiles-T128-task-checkers-followup-a01/report.md
.orchestration/dotfiles-T128-task-checkers-followup-a01/sandbox.md
.orchestration/dotfiles-T128-task-checkers-followup-a01/task.md
.orchestration/dotfiles-T128-task-checkers-followup-a01/validation.md
.orchestration/dotfiles-T128-validator-offline-a01/autoskill.md
.orchestration/dotfiles-T128-validator-offline-a01/learning.md
.orchestration/dotfiles-T128-validator-offline-a01/report.md
.orchestration/dotfiles-T128-validator-offline-a01/sandbox.md
.orchestration/dotfiles-T128-validator-offline-a01/task.md
.orchestration/dotfiles-T128-validator-offline-a01/validation.md
.orchestration/dotfiles-T129-assets-omp-hcom-a01/autoskill.md
.orchestration/dotfiles-T129-assets-omp-hcom-a01/dotfiles-T129-assets-omp-hcom-a01-worker-crit.json
.orchestration/dotfiles-T129-assets-omp-hcom-a01/dotfiles-T129-assets-omp-hcom-a01-worker-review-receipt.md
.orchestration/dotfiles-T129-assets-omp-hcom-a01/learning.md
.orchestration/dotfiles-T129-assets-omp-hcom-a01/report.md
.orchestration/dotfiles-T129-assets-omp-hcom-a01/revise.yaml
.orchestration/dotfiles-T129-assets-omp-hcom-a01/sandbox.md
.orchestration/dotfiles-T129-assets-omp-hcom-a01/task.md
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md
.orchestration/dotfiles-T129-assets-omp-hcom-followup-a01/autoskill.md
.orchestration/dotfiles-T129-assets-omp-hcom-followup-a01/learning.md
.orchestration/dotfiles-T129-assets-omp-hcom-followup-a01/report.md
.orchestration/dotfiles-T129-assets-omp-hcom-followup-a01/revise.yaml
.orchestration/dotfiles-T129-assets-omp-hcom-followup-a01/sandbox.md
.orchestration/dotfiles-T129-assets-omp-hcom-followup-a01/task.md
.orchestration/dotfiles-T129-assets-omp-hcom-followup-a01/validation.md
.orchestration/dotfiles-T129-assets-omp-hcom-followup-a02/dotfiles-T129-assets-omp-hcom-followup-a02-worker-crit.json
.orchestration/dotfiles-T129-assets-omp-hcom-followup-a02/dotfiles-T129-assets-omp-hcom-followup-a02-worker-review-receipt.md
.orchestration/dotfiles-T129-assets-omp-hcom-followup-a02/learning.md
.orchestration/dotfiles-T129-assets-omp-hcom-followup-a02/pr-body.md
.orchestration/dotfiles-T129-assets-omp-hcom-followup-a02/report.md
.orchestration/dotfiles-T129-assets-omp-hcom-followup-a02/revise.yaml
.orchestration/dotfiles-T129-assets-omp-hcom-followup-a02/sandbox.md
.orchestration/dotfiles-T129-assets-omp-hcom-followup-a02/task.md
.orchestration/dotfiles-T129-assets-omp-hcom-followup-a02/validation.md
.orchestration/dotfiles-T129-audit-inherit-replan-json-a01/autoskill.md
.orchestration/dotfiles-T129-audit-inherit-replan-json-a01/learning.md
.orchestration/dotfiles-T129-audit-inherit-replan-json-a01/report.md
.orchestration/dotfiles-T129-audit-inherit-replan-json-a01/revise.yaml
.orchestration/dotfiles-T129-audit-inherit-replan-json-a01/sandbox.md
.orchestration/dotfiles-T129-audit-inherit-replan-json-a01/task.md
.orchestration/dotfiles-T129-audit-inherit-replan-json-a01/validation.md
.orchestration/dotfiles-T129-audit-inherit-replan-json-followup-a01/dotfiles-T129-audit-inherit-replan-json-followup-a01-worker-crit.json
.orchestration/dotfiles-T129-audit-inherit-replan-json-followup-a01/dotfiles-T129-audit-inherit-replan-json-followup-a01-worker-review-receipt.md
.orchestration/dotfiles-T129-audit-inherit-replan-json-followup-a01/learning.md
.orchestration/dotfiles-T129-audit-inherit-replan-json-followup-a01/report.md
.orchestration/dotfiles-T129-audit-inherit-replan-json-followup-a01/sandbox.md
.orchestration/dotfiles-T129-audit-inherit-replan-json-followup-a01/task.md
.orchestration/dotfiles-T129-audit-inherit-replan-json-followup-a01/validation.md
.orchestration/dotfiles-T129-audit-inherit-replan-json-followup-a02/dotfiles-T129-audit-inherit-replan-json-followup-a02-worker-crit.json
.orchestration/dotfiles-T129-audit-inherit-replan-json-followup-a02/dotfiles-T129-audit-inherit-replan-json-followup-a02-worker-review-receipt.md
.orchestration/dotfiles-T129-audit-inherit-replan-json-followup-a02/learning.md
.orchestration/dotfiles-T129-audit-inherit-replan-json-followup-a02/pr-body.md
.orchestration/dotfiles-T129-audit-inherit-replan-json-followup-a02/report.md
.orchestration/dotfiles-T129-audit-inherit-replan-json-followup-a02/sandbox.md
.orchestration/dotfiles-T129-audit-inherit-replan-json-followup-a02/task.md
.orchestration/dotfiles-T129-audit-inherit-replan-json-followup-a02/validation.md
.orchestration/dotfiles-T129-doctor-sleep-disabled-a01/autoskill.md
.orchestration/dotfiles-T129-doctor-sleep-disabled-a01/dotfiles-T129-doctor-sleep-disabled-a01-worker-crit.json
.orchestration/dotfiles-T129-doctor-sleep-disabled-a01/dotfiles-T129-doctor-sleep-disabled-a01-worker-review-receipt.md
.orchestration/dotfiles-T129-doctor-sleep-disabled-a01/learning.md
.orchestration/dotfiles-T129-doctor-sleep-disabled-a01/report.md
.orchestration/dotfiles-T129-doctor-sleep-disabled-a01/sandbox.md
.orchestration/dotfiles-T129-doctor-sleep-disabled-a01/task.md
.orchestration/dotfiles-T129-doctor-sleep-disabled-a01/validation.md
.orchestration/dotfiles-T129-normalised-comparison-lint-a01/autoskill.md
.orchestration/dotfiles-T129-normalised-comparison-lint-a01/baseline-rows.md
.orchestration/dotfiles-T129-normalised-comparison-lint-a01/dotfiles-T129-normalised-comparison-lint-a01-worker-crit.json
.orchestration/dotfiles-T129-normalised-comparison-lint-a01/dotfiles-T129-normalised-comparison-lint-a01-worker-review-receipt.md
.orchestration/dotfiles-T129-normalised-comparison-lint-a01/learning.md
.orchestration/dotfiles-T129-normalised-comparison-lint-a01/question-1.md
.orchestration/dotfiles-T129-normalised-comparison-lint-a01/report.md
.orchestration/dotfiles-T129-normalised-comparison-lint-a01/revise.yaml
.orchestration/dotfiles-T129-normalised-comparison-lint-a01/sandbox.md
.orchestration/dotfiles-T129-normalised-comparison-lint-a01/task.md
.orchestration/dotfiles-T129-normalised-comparison-lint-a01/validation.md
.orchestration/dotfiles-T129-normalised-comparison-lint-followup-a01/dotfiles-T129-normalised-comparison-lint-followup-a01-worker-crit.json
.orchestration/dotfiles-T129-normalised-comparison-lint-followup-a01/dotfiles-T129-normalised-comparison-lint-followup-a01-worker-review-receipt.md
.orchestration/dotfiles-T129-normalised-comparison-lint-followup-a01/learning.md
.orchestration/dotfiles-T129-normalised-comparison-lint-followup-a01/pr-body.md
.orchestration/dotfiles-T129-normalised-comparison-lint-followup-a01/report.md
.orchestration/dotfiles-T129-normalised-comparison-lint-followup-a01/revise.yaml
.orchestration/dotfiles-T129-normalised-comparison-lint-followup-a01/sandbox.md
.orchestration/dotfiles-T129-normalised-comparison-lint-followup-a01/validation.md
.orchestration/dotfiles-T129-normalised-comparison-lint-followup-a03/autoskill.md
.orchestration/dotfiles-T129-normalised-comparison-lint-followup-a03/dotfiles-T129-normalised-comparison-lint-followup-a03-worker-crit.json
.orchestration/dotfiles-T129-normalised-comparison-lint-followup-a03/dotfiles-T129-normalised-comparison-lint-followup-a03-worker-review-receipt.md
.orchestration/dotfiles-T129-normalised-comparison-lint-followup-a03/learning.md
.orchestration/dotfiles-T129-normalised-comparison-lint-followup-a03/report.md
.orchestration/dotfiles-T129-normalised-comparison-lint-followup-a03/sandbox.md
.orchestration/dotfiles-T129-normalised-comparison-lint-followup-a03/task.md
.orchestration/dotfiles-T129-normalised-comparison-lint-followup-a03/validation.md
.orchestration/dotfiles-T130-claude-sandbox-integration-a01/autoskill.md
.orchestration/dotfiles-T130-claude-sandbox-integration-a01/dotfiles-T130-claude-sandbox-integration-a01-worker-crit.json
.orchestration/dotfiles-T130-claude-sandbox-integration-a01/dotfiles-T130-claude-sandbox-integration-a01-worker-review-receipt.md
.orchestration/dotfiles-T130-claude-sandbox-integration-a01/learning.md
.orchestration/dotfiles-T130-claude-sandbox-integration-a01/report.md
.orchestration/dotfiles-T130-claude-sandbox-integration-a01/revise.yaml
.orchestration/dotfiles-T130-claude-sandbox-integration-a01/sandbox.md
.orchestration/dotfiles-T130-claude-sandbox-integration-a01/task.md
.orchestration/dotfiles-T130-claude-sandbox-integration-a01/validation.md
.orchestration/dotfiles-T132-make-update-followups-a01/dotfiles-T132-make-update-followups-a01-worker-crit.json
.orchestration/dotfiles-T132-make-update-followups-a01/dotfiles-T132-make-update-followups-a01-worker-review-receipt.md
.orchestration/dotfiles-T132-make-update-followups-a01/learning.md
.orchestration/dotfiles-T132-make-update-followups-a01/report.md
.orchestration/dotfiles-T132-make-update-followups-a01/sandbox.md
.orchestration/dotfiles-T132-make-update-followups-a01/task.md
.orchestration/dotfiles-T132-make-update-followups-a01/validation.md
.orchestration/dotfiles-T133-ci-efficiency-a01/dotfiles-T133-ci-efficiency-a01-worker-crit.json
.orchestration/dotfiles-T133-ci-efficiency-a01/dotfiles-T133-ci-efficiency-a01-worker-review-receipt.md
.orchestration/dotfiles-T133-ci-efficiency-a01/learning.md
.orchestration/dotfiles-T133-ci-efficiency-a01/measure.md
.orchestration/dotfiles-T133-ci-efficiency-a01/report.md
.orchestration/dotfiles-T133-ci-efficiency-a01/revise.yaml
.orchestration/dotfiles-T133-ci-efficiency-a01/sandbox.md
.orchestration/dotfiles-T133-ci-efficiency-a01/task.md
.orchestration/dotfiles-T133-ci-efficiency-a01/validation.md
.orchestration/dotfiles-T133-ci-efficiency-a02/autoskill.md
.orchestration/dotfiles-T133-ci-efficiency-a02/dotfiles-T133-ci-efficiency-a02-worker-crit.json
.orchestration/dotfiles-T133-ci-efficiency-a02/dotfiles-T133-ci-efficiency-a02-worker-review-receipt.md
.orchestration/dotfiles-T133-ci-efficiency-a02/learning.md
.orchestration/dotfiles-T133-ci-efficiency-a02/measure.md
.orchestration/dotfiles-T133-ci-efficiency-a02/report.md
.orchestration/dotfiles-T133-ci-efficiency-a02/revise.yaml
.orchestration/dotfiles-T133-ci-efficiency-a02/sandbox.md
.orchestration/dotfiles-T133-ci-efficiency-a02/task.md
.orchestration/dotfiles-T133-ci-efficiency-a02/validation.md
.orchestration/dotfiles-T133-ci-efficiency-followup-a01/dotfiles-T133-ci-efficiency-followup-a01-worker-crit.json
.orchestration/dotfiles-T133-ci-efficiency-followup-a01/dotfiles-T133-ci-efficiency-followup-a01-worker-review-receipt.md
.orchestration/dotfiles-T133-ci-efficiency-followup-a01/learning.md
.orchestration/dotfiles-T133-ci-efficiency-followup-a01/report.md
.orchestration/dotfiles-T133-ci-efficiency-followup-a01/sandbox.md
.orchestration/dotfiles-T133-ci-efficiency-followup-a01/task.md
.orchestration/dotfiles-T133-ci-efficiency-followup-a01/validation.md
.orchestration/dotfiles-T133-regime-ci-a01/dotfiles-T133-regime-ci-a01-worker-crit.json
.orchestration/dotfiles-T133-regime-ci-a01/dotfiles-T133-regime-ci-a01-worker-review-receipt.md
.orchestration/dotfiles-T133-regime-ci-a01/learning.md
.orchestration/dotfiles-T133-regime-ci-a01/pr-body.md
.orchestration/dotfiles-T133-regime-ci-a01/report.md
.orchestration/dotfiles-T133-regime-ci-a01/sandbox.md
.orchestration/dotfiles-T133-regime-ci-a01/validation.md
.orchestration/dotfiles-T133-regime-ci-a02/dotfiles-T133-regime-ci-a02-worker-crit.json
.orchestration/dotfiles-T133-regime-ci-a02/dotfiles-T133-regime-ci-a02-worker-review-receipt.md
.orchestration/dotfiles-T133-regime-ci-a02/learning.md
.orchestration/dotfiles-T133-regime-ci-a02/report.md
.orchestration/dotfiles-T133-regime-ci-a02/revise.yaml
.orchestration/dotfiles-T133-regime-ci-a02/sandbox.md
.orchestration/dotfiles-T133-regime-ci-a02/task.md
.orchestration/dotfiles-T133-regime-ci-a02/validation.md
.orchestration/dotfiles-T133-worker-cap-hookspath-a01/revise.yaml
.orchestration/dotfiles-T133-worker-cap-hookspath-a01/task.md
.orchestration/dotfiles-T133-worker-cap-hookspath-a02/task.md
.orchestration/dotfiles-T133-worker-cap-hookspath-followup-a01/task.md
.orchestration/handoff/2026-10-17T1110Z.md
.orchestration/learning/corrections-inventory.tsv
.orchestration/learning/corrections/C-1.md
.orchestration/learning/corrections/C-10.md
.orchestration/learning/corrections/C-11.md
.orchestration/learning/corrections/C-12.md
.orchestration/learning/corrections/C-13.md
.orchestration/learning/corrections/C-14.md
.orchestration/learning/corrections/C-15.md
.orchestration/learning/corrections/C-16.md
.orchestration/learning/corrections/C-17.md
.orchestration/learning/corrections/C-18.md
.orchestration/learning/corrections/C-19.md
.orchestration/learning/corrections/C-2.md
.orchestration/learning/corrections/C-20.md
.orchestration/learning/corrections/C-21.md
.orchestration/learning/corrections/C-22.md
.orchestration/learning/corrections/C-23.md
.orchestration/learning/corrections/C-24.md
.orchestration/learning/corrections/C-25.md
.orchestration/learning/corrections/C-26.md
.orchestration/learning/corrections/C-27.md
.orchestration/learning/corrections/C-28.md
.orchestration/learning/corrections/C-29.md
.orchestration/learning/corrections/C-3.md
.orchestration/learning/corrections/C-30.md
.orchestration/learning/corrections/C-31.md
.orchestration/learning/corrections/C-32.md
.orchestration/learning/corrections/C-33.md
.orchestration/learning/corrections/C-34.md
.orchestration/learning/corrections/C-35.md
.orchestration/learning/corrections/C-36.md
.orchestration/learning/corrections/C-37.md
.orchestration/learning/corrections/C-38.md
.orchestration/learning/corrections/C-39.md
.orchestration/learning/corrections/C-4.md
.orchestration/learning/corrections/C-40.md
.orchestration/learning/corrections/C-41.md
.orchestration/learning/corrections/C-42.md
.orchestration/learning/corrections/C-43.md
.orchestration/learning/corrections/C-44.md
.orchestration/learning/corrections/C-45.md
.orchestration/learning/corrections/C-46.md
.orchestration/learning/corrections/C-47.md
.orchestration/learning/corrections/C-48.md
.orchestration/learning/corrections/C-49.md
.orchestration/learning/corrections/C-5.md
.orchestration/learning/corrections/C-50.md
.orchestration/learning/corrections/C-51.md
.orchestration/learning/corrections/C-52.md
.orchestration/learning/corrections/C-53.md
.orchestration/learning/corrections/C-54.md
.orchestration/learning/corrections/C-55.md
.orchestration/learning/corrections/C-56.md
.orchestration/learning/corrections/C-57.md
.orchestration/learning/corrections/C-58.md
.orchestration/learning/corrections/C-59.md
.orchestration/learning/corrections/C-6.md
.orchestration/learning/corrections/C-60.md
.orchestration/learning/corrections/C-61.md
.orchestration/learning/corrections/C-7.md
.orchestration/learning/corrections/C-8.md
.orchestration/learning/corrections/C-9.md
.orchestration/learning/dot-ccstatusline-ubuntu26-hang-T59-a01.md
.orchestration/learning/dot-ci-runner-label-pin-T58-a01.md
.orchestration/learning/dot-formatter-hook-root-fix-T61-a01.md
.orchestration/learning/dot-git-ignore-cc-writes-T56-a01.md
.orchestration/learning/dot-macos-brew-untrusted-taps-T57-a01.md
.orchestration/learning/dot-main-push-guard-revert-T60-a01.md
.orchestration/learning/dot-ua-graph-refresh-T55-a01.md
.orchestration/learning/dotfiles-T100-compactiondb-claude-symlink-note-a01.md
.orchestration/learning/dotfiles-T101-codex-worker-profile-default-a01.md
.orchestration/learning/dotfiles-T102-add-worker-credential-notice-a01.md
.orchestration/learning/dotfiles-T103-gh-auth-stores-a01.md
.orchestration/learning/dotfiles-T104-pins-2026-10-06-a01.md
.orchestration/learning/dotfiles-T107-gh-stores-per-machine-a01.md
.orchestration/learning/dotfiles-T108-one-login-per-machine-a01.md
.orchestration/learning/dotfiles-T109-claude-worker-merge-deny-a01.md
.orchestration/learning/dotfiles-T110-gh-auth-file-storage-a01.md
.orchestration/learning/dotfiles-T111-project-map-subagent-a01.md
.orchestration/learning/dotfiles-T112-pins-2026-10-07-a01.md
.orchestration/learning/dotfiles-T113-codify-T111-lessons-a01.md
.orchestration/learning/dotfiles-T114-canonical-clone-reconcile-a01.md
.orchestration/learning/dotfiles-T115-worker-audit-xhigh-a01.md
.orchestration/learning/dotfiles-T116-on-demand-workers-a01.md
.orchestration/learning/dotfiles-T117-upgrade-outside-canonical-clone-a01.md
.orchestration/learning/dotfiles-T118-rolling-tools-single-update-a01.md
.orchestration/learning/dotfiles-T119-rolling-release-assets-a01.md
.orchestration/learning/dotfiles-T120-npm-provenance-and-claude-channel-a01.md
.orchestration/learning/dotfiles-T124-wave1-task-validator-a01.md
.orchestration/learning/dotfiles-T124-wave3b-audit-grammar-a01.md
.orchestration/learning/dotfiles-T128-aws-cli-macos-a01.md
.orchestration/learning/dotfiles-T128-chain-github-scripts-a01.md
.orchestration/learning/dotfiles-T128-chain-github-scripts-followup-a01.md
.orchestration/learning/dotfiles-T128-chain-review-scripts-followup-a01.md
.orchestration/learning/dotfiles-T128-chain-review-scripts-followup-a02.md
.orchestration/learning/dotfiles-T128-ci-skip-orchestration-a01.md
.orchestration/learning/dotfiles-T128-ci-skip-orchestration-a02.md
.orchestration/learning/dotfiles-T128-gate-evidence-a02.md
.orchestration/learning/dotfiles-T128-gate-evidence-a03.md
.orchestration/learning/dotfiles-T128-gate-evidence-a04.md
.orchestration/learning/dotfiles-T128-gate-wrapper-path-a01.md
.orchestration/learning/dotfiles-T128-orchestrator-tools-a01.md
.orchestration/learning/dotfiles-T128-orchestrator-tools-a02.md
.orchestration/learning/dotfiles-T128-orchestrator-tools-a03.md
.orchestration/learning/dotfiles-T128-orchestrator-tools-a04.md
.orchestration/learning/dotfiles-T128-orchestrator-tools-a05.md
.orchestration/learning/dotfiles-T128-orchestrator-tools-a06.md
.orchestration/learning/dotfiles-T128-orchestrator-tools-followup-a01.md
.orchestration/learning/dotfiles-T128-orchestrator-tools-followup-a03.md
.orchestration/learning/dotfiles-T128-playbook-rules-a02.md
.orchestration/learning/dotfiles-T128-playbook-rules-a03.md
.orchestration/learning/dotfiles-T128-playbook-rules-a04.md
.orchestration/learning/dotfiles-T128-process-rules-a01.md
.orchestration/learning/dotfiles-T128-process-rules-a02.md
.orchestration/learning/dotfiles-T128-process-rules-a03.md
.orchestration/learning/dotfiles-T128-process-rules-a04.md
.orchestration/learning/dotfiles-T128-process-rules-a05.md
.orchestration/learning/dotfiles-T128-process-rules-a06.md
.orchestration/learning/dotfiles-T128-process-rules-a07.md
.orchestration/learning/dotfiles-T128-project-map-pane-open-a01.md
.orchestration/learning/dotfiles-T128-project-map-reload-hook-followup-a01.md
.orchestration/learning/dotfiles-T128-regime-counters-a01.md
.orchestration/learning/dotfiles-T128-regime-counters-a02.md
.orchestration/learning/dotfiles-T128-seat-liveness-a01.md
.orchestration/learning/dotfiles-T128-settings-hook-dedupe-followup-a01.md
.orchestration/learning/dotfiles-T128-v0-main-tests-a01.md
.orchestration/learning/dotfiles-T128-worker-stop-and-watch-a01.md
.orchestration/learning/dotfiles-T128-worker-stop-and-watch-a02.md
.orchestration/learning/dotfiles-T62-claude-auto-deny-a01.md
.orchestration/learning/dotfiles-T63-codex-execpolicy-forbidden-a01.md
.orchestration/learning/dotfiles-T64-codex-worker-never-network-a01.md
.orchestration/learning/dotfiles-T65-agent-stop-gate-a01.md
.orchestration/learning/dotfiles-T66-permgate-dead-lanes-a01.md
.orchestration/learning/dotfiles-T67-audit-task-level-a01.md
.orchestration/learning/dotfiles-T68-gate-audit-evidence-a01.md
.orchestration/learning/dotfiles-T69-protocol-docs-unification-a01.md
.orchestration/learning/dotfiles-T70-make-update-unattended-a01.md
.orchestration/learning/dotfiles-T71-generator-multi-target-a01.md
.orchestration/learning/dotfiles-T72-bootstrap-ci-pins-a01.md
.orchestration/learning/dotfiles-T73-tool-versions-from-config-a01.md
.orchestration/learning/dotfiles-T74-bootstrap-dead-code-a01.md
.orchestration/learning/dotfiles-T75-shell-dead-code-a01.md
.orchestration/learning/dotfiles-T76-ineffective-settings-a01.md
.orchestration/learning/dotfiles-T77-harness-dead-code-a01.md
.orchestration/learning/dotfiles-T77b-enforce-uv-hook-contract-a01.md
.orchestration/learning/dotfiles-T78-dead-docs-adh-a01.md
.orchestration/learning/dotfiles-T79-remove-adh-profile-a01.md
.orchestration/learning/dotfiles-T80-codex-command-hooks-a01.md
.orchestration/learning/dotfiles-T81-compactiondb-vendor-a01.md
.orchestration/learning/dotfiles-T81b-compactiondb-vendor-hygiene-a01.md
.orchestration/learning/dotfiles-T82-codex-compaction-hooks-a01.md
.orchestration/learning/dotfiles-T82b-codex-hook-trust-pins-a01.md
.orchestration/learning/dotfiles-T83-docs-diet-a01.md
.orchestration/learning/dotfiles-T84-orchestrator-kind-a01.md
.orchestration/learning/dotfiles-T85-launcher-orchestrator-kind-a01.md
.orchestration/learning/dotfiles-T86-codex-orchestrate-a01.md
.orchestration/learning/dotfiles-T88-parallel-execution-rule-a01.md
.orchestration/learning/dotfiles-T89-add-worker-same-workspace-a01.md
.orchestration/learning/dotfiles-T90-github-identity-separation-a01.md
.orchestration/learning/dotfiles-T90b-ruleset-sole-merger-a01.md
.orchestration/learning/dotfiles-T91-secret-scan-sk-boundary-a01.md
.orchestration/learning/dotfiles-T92-stop-gate-sandbox-placeholders-a01.md
.orchestration/learning/dotfiles-T93-gate-masked-feedback-bodies-a01.md
.orchestration/learning/dotfiles-T94-upgrade-pins-a01.md
.orchestration/learning/dotfiles-T95-sandbox-placeholder-files-on-disk-a01.md
.orchestration/learning/dotfiles-T96-codex-worker-gpt61-sol-high-a01.md
.orchestration/learning/dotfiles-T97-claude-sandbox-github-calls-a01.md
.orchestration/learning/dotfiles-T98-evidence-home-path-masking-a01.md
.orchestration/learning/dotfiles-T98b-runner-home-and-review-body-a01.md
.orchestration/learning/dotfiles-T98c-claude-seat-artifact-write-exception-a01.md
.orchestration/learning/dotfiles-T99-nix-plans-history-a01.md
.orchestration/learning/index.yaml
.orchestration/learning/mistakes/M-20261011-1.md
.orchestration/learning/mistakes/M-20261012-1.md
.orchestration/learning/mistakes/M-20261012-10.md
.orchestration/learning/mistakes/M-20261012-11.md
.orchestration/learning/mistakes/M-20261012-12.md
.orchestration/learning/mistakes/M-20261012-13.md
.orchestration/learning/mistakes/M-20261012-14.md
.orchestration/learning/mistakes/M-20261012-15.md
.orchestration/learning/mistakes/M-20261012-16.md
.orchestration/learning/mistakes/M-20261012-17.md
.orchestration/learning/mistakes/M-20261012-18.md
.orchestration/learning/mistakes/M-20261012-19.md
.orchestration/learning/mistakes/M-20261012-2.md
.orchestration/learning/mistakes/M-20261012-20.md
.orchestration/learning/mistakes/M-20261012-21.md
.orchestration/learning/mistakes/M-20261012-22.md
.orchestration/learning/mistakes/M-20261012-23.md
.orchestration/learning/mistakes/M-20261012-24.md
.orchestration/learning/mistakes/M-20261012-25.md
.orchestration/learning/mistakes/M-20261012-26.md
.orchestration/learning/mistakes/M-20261012-27.md
.orchestration/learning/mistakes/M-20261012-28.md
.orchestration/learning/mistakes/M-20261012-29.md
.orchestration/learning/mistakes/M-20261012-3.md
.orchestration/learning/mistakes/M-20261012-30.md
.orchestration/learning/mistakes/M-20261012-31.md
.orchestration/learning/mistakes/M-20261012-32.md
.orchestration/learning/mistakes/M-20261012-33.md
.orchestration/learning/mistakes/M-20261012-34.md
.orchestration/learning/mistakes/M-20261012-35.md
.orchestration/learning/mistakes/M-20261012-4.md
.orchestration/learning/mistakes/M-20261012-5.md
.orchestration/learning/mistakes/M-20261012-6.md
.orchestration/learning/mistakes/M-20261012-7.md
.orchestration/learning/mistakes/M-20261012-8.md
.orchestration/learning/mistakes/M-20261012-9.md
.orchestration/learning/mistakes/M-20261014-01.md
.orchestration/learning/mistakes/M-20261014-02.md
.orchestration/learning/mistakes/M-20261014-03.md
.orchestration/learning/mistakes/M-20261014-04.md
.orchestration/learning/mistakes/M-20261014-05.md
.orchestration/learning/mistakes/M-20261014-06.md
.orchestration/learning/mistakes/M-20261014-07.md
.orchestration/learning/mistakes/M-20261014-08.md
.orchestration/learning/mistakes/M-20261014-09.md
.orchestration/learning/mistakes/M-20261014-10.md
.orchestration/learning/mistakes/M-20261014-11.md
.orchestration/learning/mistakes/M-20261014-12.md
.orchestration/learning/mistakes/M-20261014-13.md
.orchestration/learning/mistakes/M-20261014-14.md
.orchestration/learning/mistakes/M-20261015-01.md
.orchestration/learning/mistakes/M-20261015-02.md
.orchestration/learning/mistakes/M-20261015-03.md
.orchestration/learning/mistakes/M-20261015-04.md
.orchestration/learning/mistakes/M-20261015-05.md
.orchestration/learning/mistakes/M-20261015-06.md
.orchestration/learning/mistakes/M-20261016-01.md
.orchestration/learning/mistakes/M-20261017-01.md
.orchestration/learning/mistakes/M-20261017-02.md
.orchestration/learning/mistakes/M-20261017-03.md
.orchestration/learning/mistakes/M-20261017-04.md
.orchestration/learning/mistakes/M-20261017-05.md
.orchestration/learning/mistakes/M-20261017-06.md
.orchestration/learning/mistakes/M-20261017-07.md
.orchestration/learning/plan-006-s1-gate-evidence-search-command-scan-2026-10-12.md
.orchestration/learning/plan-006-s1-playbook-rules-search-procedure-2026-10-12.md
.orchestration/learning/plan-006-s1-pr318-finding-classes-2026-10-12.md
.orchestration/learning/plan-006-s1-process-rules-counters-bullet-2026-10-11.md
.orchestration/learning/plan-006-s1-v0-main-tests-2026-10-11.md
.orchestration/learning/rule_candidates/agmsg-worker-identity-delivery.md
.orchestration/metrics/pr-cost.tsv
.orchestration/plans/006-regime-v3-execution.md
.orchestration/plans/007-mistakes-into-mechanisms.md
.orchestration/plans/008-resume-a7-pr323.md
.orchestration/plans/009-resume-t703-pr328.md
.orchestration/plans/010-resume-t703-third-cycle.md
.orchestration/plans/011-resume-t702-pr329.md
.orchestration/plans/012-resume-t703-fourth-cycle.md
.orchestration/plans/013-resume-t702-third-cycle.md
.orchestration/plans/014-resume-t702-fourth-cycle.md
.orchestration/plans/015-resume-t718-a03-second-cycle.md
.orchestration/plans/016-resume-t718-a03-third-cycle.md
.orchestration/plans/017-resume-t703-a04-after-t718.md
.orchestration/plans/018-stop-and-situation.md
.orchestration/plans/019-root-causes-and-corrective-order.md
.orchestration/plans/020-certain-order.md
.orchestration/plans/021-execution-detail-and-scrutiny.md
.orchestration/plans/022-stabilise-and-operate.md
.orchestration/plans/023-omp-hcom-migration.md
.orchestration/reports/T18-herdr-agents-two-pane.md
.orchestration/reports/T19-herdr-file-viewer-popup-config.md
.orchestration/reports/T24-usage-review-automation.md
.orchestration/reports/T28-ccgate-removal-permgate-deploy.md
.orchestration/reports/T29-agmsg-regime-default-on.md
.orchestration/reports/T30-orchestration-evidence-sync.md
.orchestration/reports/T31-codex-profile-modify-pattern.md
.orchestration/reports/T32-evidence-and-mise-sync.md
.orchestration/reports/dot-adh-baseline-T6-a01.md
.orchestration/reports/dot-agmsg-dispatch-T4-a01.md
.orchestration/reports/dot-audit-exec-channel-T33e-a01.md
.orchestration/reports/dot-audit-pane-hardening-T32b-a01.md
.orchestration/reports/dot-audit-pane-prompt-detect-T33j-a01.md
.orchestration/reports/dot-audit-pane-visibility-T32-a01.md
.orchestration/reports/dot-audit-profile-gpt6-sol-T48-a01.md
.orchestration/reports/dot-audit-verdict-gate-T33b-a01.md
.orchestration/reports/dot-ccstatusline-ubuntu26-hang-T59-a01.md
.orchestration/reports/dot-ci-runner-label-pin-T58-a01.md
.orchestration/reports/dot-claude-sandbox-manifest-T39-a01.md
.orchestration/reports/dot-codex-apparmor-userns-T30-a01.md
.orchestration/reports/dot-env-converge-T10-a01.md
.orchestration/reports/dot-formatter-hook-root-fix-T61-a01.md
.orchestration/reports/dot-git-ignore-cc-writes-T56-a01.md
.orchestration/reports/dot-herdr-sheldon-T1-a02.md
.orchestration/reports/dot-macos-brew-untrusted-taps-T57-a01.md
.orchestration/reports/dot-main-push-guard-revert-T60-a01.md
.orchestration/reports/dot-mosh-and-asset-bumps-T31-a01.md
.orchestration/reports/dot-orchestration-hygiene-T33i-a01.md
.orchestration/reports/dot-orchestration-rules-T33a-a01.md
.orchestration/reports/dot-orchestration-rules-T43-a01.md
.orchestration/reports/dot-orchestrator-delivery-sandbox-T49-a01.md
.orchestration/reports/dot-permgate-bench-flake-T33d-a01.md
.orchestration/reports/dot-permgate-codex-stdin-T33h-a01.md
.orchestration/reports/dot-plain-start-visibility-T45-a01.md
.orchestration/reports/dot-pr-feedback-gate-T38-a01.md
.orchestration/reports/dot-pr-gate-trust-boundary-T40-a01.md
.orchestration/reports/dot-restart-worker-name-wait-T27-a01.md
.orchestration/reports/dot-sandbox-unix-sockets-T44-a01.md
.orchestration/reports/dot-security-profile-model-T42-a01.md
.orchestration/reports/dot-three-role-constellation-T28-a01.md
.orchestration/reports/dot-ua-core-build-T33f-a01.md
.orchestration/reports/dot-ua-core-build-shim-T33g-a01.md
.orchestration/reports/dot-ua-graph-refresh-T33c-a01.md
.orchestration/reports/dot-ua-graph-refresh-T36-a01.md
.orchestration/reports/dot-ua-graph-refresh-T41-a01.md
.orchestration/reports/dot-ua-graph-refresh-T55-a01.md
.orchestration/reports/dot-ua-refresh-T5-a01.md
.orchestration/reports/dot-ubuntu-parity-T2-a01.md
.orchestration/reports/dot-ubuntu-parity-T3-a01.md
.orchestration/reports/dot-ubuntu-parity-T4-a01.md
.orchestration/reports/dot-update-convergence-T1-a01.md
.orchestration/reports/dot-upgrade-pins-sync-T37-a01.md
.orchestration/reports/dot-validator-worktrees-T7-a01.md
.orchestration/reports/dot-version-currency-T29-a01.md
.orchestration/reports/dotfiles-T100-compactiondb-claude-symlink-note-a01.md
.orchestration/reports/dotfiles-T101-codex-worker-profile-default-a01.md
.orchestration/reports/dotfiles-T102-add-worker-credential-notice-a01.md
.orchestration/reports/dotfiles-T103-gh-auth-stores-a01.md
.orchestration/reports/dotfiles-T104-pins-2026-10-06-a01.md
.orchestration/reports/dotfiles-T108-one-login-per-machine-a01.md
.orchestration/reports/dotfiles-T109-claude-worker-merge-deny-a01.md
.orchestration/reports/dotfiles-T110-gh-auth-file-storage-a01.md
.orchestration/reports/dotfiles-T111-project-map-subagent-a01.md
.orchestration/reports/dotfiles-T112-pins-2026-10-07-a01.md
.orchestration/reports/dotfiles-T113-codify-T111-lessons-a01.md
.orchestration/reports/dotfiles-T114-canonical-clone-reconcile-a01.md
.orchestration/reports/dotfiles-T115-worker-audit-xhigh-a01.md
.orchestration/reports/dotfiles-T116-on-demand-workers-a01.md
.orchestration/reports/dotfiles-T117-upgrade-outside-canonical-clone-a01.md
.orchestration/reports/dotfiles-T118-rolling-tools-single-update-a01.md
.orchestration/reports/dotfiles-T119-rolling-release-assets-a01.md
.orchestration/reports/dotfiles-T121-claude-hook-install-hint-a01.md
.orchestration/reports/dotfiles-T124-wave1-task-validator-a01.md
.orchestration/reports/dotfiles-T124-wave3b-audit-grammar-a01.md
.orchestration/reports/dotfiles-T128-aws-cli-macos-a01.md
.orchestration/reports/dotfiles-T128-chain-github-scripts-a01.md
.orchestration/reports/dotfiles-T128-chain-github-scripts-followup-a01.md
.orchestration/reports/dotfiles-T128-chain-review-scripts-followup-a01.md
.orchestration/reports/dotfiles-T128-chain-review-scripts-followup-a02.md
.orchestration/reports/dotfiles-T128-ci-skip-orchestration-a01.md
.orchestration/reports/dotfiles-T128-ci-skip-orchestration-a02.md
.orchestration/reports/dotfiles-T128-gate-evidence-a02.md
.orchestration/reports/dotfiles-T128-gate-evidence-a03.md
.orchestration/reports/dotfiles-T128-gate-evidence-a04.md
.orchestration/reports/dotfiles-T128-gate-wrapper-path-a01.md
.orchestration/reports/dotfiles-T128-orchestrator-tools-a01.md
.orchestration/reports/dotfiles-T128-orchestrator-tools-a02.md
.orchestration/reports/dotfiles-T128-orchestrator-tools-a03.md
.orchestration/reports/dotfiles-T128-orchestrator-tools-a04.md
.orchestration/reports/dotfiles-T128-orchestrator-tools-a05.md
.orchestration/reports/dotfiles-T128-orchestrator-tools-a06.md
.orchestration/reports/dotfiles-T128-orchestrator-tools-followup-a01.md
.orchestration/reports/dotfiles-T128-orchestrator-tools-followup-a03.md
.orchestration/reports/dotfiles-T128-playbook-rules-a02.md
.orchestration/reports/dotfiles-T128-playbook-rules-a03.md
.orchestration/reports/dotfiles-T128-playbook-rules-a04.md
.orchestration/reports/dotfiles-T128-process-rules-a01.md
.orchestration/reports/dotfiles-T128-process-rules-a02.md
.orchestration/reports/dotfiles-T128-process-rules-a03.md
.orchestration/reports/dotfiles-T128-process-rules-a04.md
.orchestration/reports/dotfiles-T128-process-rules-a05.md
.orchestration/reports/dotfiles-T128-process-rules-a06.md
.orchestration/reports/dotfiles-T128-process-rules-a07.md
.orchestration/reports/dotfiles-T128-project-map-pane-open-a01.md
.orchestration/reports/dotfiles-T128-project-map-reload-hook-a01.md
.orchestration/reports/dotfiles-T128-project-map-reload-hook-followup-a01.md
.orchestration/reports/dotfiles-T128-regime-counters-a01.md
.orchestration/reports/dotfiles-T128-regime-counters-a02.md
.orchestration/reports/dotfiles-T128-seat-liveness-a01.md
.orchestration/reports/dotfiles-T128-settings-hook-dedupe-followup-a01.md
.orchestration/reports/dotfiles-T128-v0-main-tests-a01.md
.orchestration/reports/dotfiles-T128-worker-stop-and-watch-a01.md
.orchestration/reports/dotfiles-T128-worker-stop-and-watch-a02.md
.orchestration/reports/dotfiles-T62-claude-auto-deny-a01.md
.orchestration/reports/dotfiles-T63-codex-execpolicy-forbidden-a01.md
.orchestration/reports/dotfiles-T64-codex-worker-never-network-a01.md
.orchestration/reports/dotfiles-T65-agent-stop-gate-a01.md
.orchestration/reports/dotfiles-T66-permgate-dead-lanes-a01.md
.orchestration/reports/dotfiles-T67-audit-task-level-a01.md
.orchestration/reports/dotfiles-T68-gate-audit-evidence-a01.md
.orchestration/reports/dotfiles-T69-protocol-docs-unification-a01.md
.orchestration/reports/dotfiles-T70-make-update-unattended-a01.md
.orchestration/reports/dotfiles-T71-generator-multi-target-a01.md
.orchestration/reports/dotfiles-T72-bootstrap-ci-pins-a01.md
.orchestration/reports/dotfiles-T73-tool-versions-from-config-a01.md
.orchestration/reports/dotfiles-T74-bootstrap-dead-code-a01.md
.orchestration/reports/dotfiles-T75-shell-dead-code-a01.md
.orchestration/reports/dotfiles-T76-ineffective-settings-a01.md
.orchestration/reports/dotfiles-T77-harness-dead-code-a01.md
.orchestration/reports/dotfiles-T77b-enforce-uv-hook-contract-a01.md
.orchestration/reports/dotfiles-T78-dead-docs-adh-a01.md
.orchestration/reports/dotfiles-T79-remove-adh-profile-a01.md
.orchestration/reports/dotfiles-T80-codex-command-hooks-a01.md
.orchestration/reports/dotfiles-T81-compactiondb-vendor-a01.md
.orchestration/reports/dotfiles-T81b-compactiondb-vendor-hygiene-a01.md
.orchestration/reports/dotfiles-T82-codex-compaction-hooks-a01.md
.orchestration/reports/dotfiles-T82b-codex-hook-trust-pins-a01.md
.orchestration/reports/dotfiles-T83-docs-diet-a01.md
.orchestration/reports/dotfiles-T84-orchestrator-kind-a01.md
.orchestration/reports/dotfiles-T85-launcher-orchestrator-kind-a01.md
.orchestration/reports/dotfiles-T86-codex-orchestrate-a01.md
.orchestration/reports/dotfiles-T88-parallel-execution-rule-a01.md
.orchestration/reports/dotfiles-T89-add-worker-same-workspace-a01.md
.orchestration/reports/dotfiles-T90-github-identity-separation-a01.md
.orchestration/reports/dotfiles-T90b-ruleset-sole-merger-a01.md
.orchestration/reports/dotfiles-T91-secret-scan-sk-boundary-a01.md
.orchestration/reports/dotfiles-T92-stop-gate-sandbox-placeholders-a01.md
.orchestration/reports/dotfiles-T93-gate-masked-feedback-bodies-a01.md
.orchestration/reports/dotfiles-T94-upgrade-pins-a01.md
.orchestration/reports/dotfiles-T95-sandbox-placeholder-files-on-disk-a01.md
.orchestration/reports/dotfiles-T96-codex-worker-gpt61-sol-high-a01.md
.orchestration/reports/dotfiles-T97-claude-sandbox-github-calls-a01.md
.orchestration/reports/dotfiles-T98-evidence-home-path-masking-a01.md
.orchestration/reports/dotfiles-T98b-runner-home-and-review-body-a01.md
.orchestration/reports/dotfiles-T98c-claude-seat-artifact-write-exception-a01.md
.orchestration/reports/dotfiles-T99-nix-plans-history-a01.md
.orchestration/reports/fix-chezmoi-pycache-modify-exec.md
.orchestration/reports/remote-diff-01.md
.orchestration/sandboxes/T10-herdr-files-pane.md
.orchestration/sandboxes/T11-agmsg-join-unique-identity-guard.md
.orchestration/sandboxes/T13-agmsg-orchestration-rule-file.md
.orchestration/sandboxes/T15-herdr-lazy-start-attach-layout.md
.orchestration/sandboxes/T16-herdr-attach-layout-order-repair.md
.orchestration/sandboxes/T17-herdr-attach-agmsg-bootstrap.md
.orchestration/sandboxes/T18-herdr-agents-two-pane.md
.orchestration/sandboxes/T19-herdr-file-viewer-popup-config.md
.orchestration/sandboxes/T20-agmsg-setup-automation.md
.orchestration/sandboxes/T29-agmsg-regime-default-on.md
.orchestration/sandboxes/T30-orchestration-evidence-sync.md
.orchestration/sandboxes/T31-codex-profile-modify-pattern.md
.orchestration/sandboxes/T32-evidence-and-mise-sync.md
.orchestration/sandboxes/T45.md
.orchestration/sandboxes/T46.md
.orchestration/sandboxes/T47.md
.orchestration/sandboxes/T48.md
.orchestration/sandboxes/T48b.md
.orchestration/sandboxes/T48c.md
.orchestration/sandboxes/T49.md
.orchestration/sandboxes/T5.md
.orchestration/sandboxes/T50.md
.orchestration/sandboxes/T51a.md
.orchestration/sandboxes/T52.md
.orchestration/sandboxes/T53.md
.orchestration/sandboxes/T54.md
.orchestration/sandboxes/T55.md
.orchestration/sandboxes/T56.md
.orchestration/sandboxes/T56b.md
.orchestration/sandboxes/T57.md
.orchestration/sandboxes/T58.md
.orchestration/sandboxes/T59.md
.orchestration/sandboxes/T59b.md
.orchestration/sandboxes/T6.md
.orchestration/sandboxes/T60.md
.orchestration/sandboxes/T61a.md
.orchestration/sandboxes/T61b.md
.orchestration/sandboxes/T62.md
.orchestration/sandboxes/T62b.md
.orchestration/sandboxes/T67d.md
.orchestration/sandboxes/T7.md
.orchestration/sandboxes/T8.md
.orchestration/sandboxes/T80-sandbox.md
.orchestration/sandboxes/T83-sandbox.md
.orchestration/sandboxes/T83b-sandbox.md
.orchestration/sandboxes/T84-sandbox.md
.orchestration/sandboxes/T84b-sandbox.md
.orchestration/sandboxes/T84c-sandbox.md
.orchestration/sandboxes/T85-sandbox.md
.orchestration/sandboxes/T87-boundary-bookkeeping-147.md
.orchestration/sandboxes/T9.md
.orchestration/sandboxes/WP-B.md
.orchestration/sandboxes/WP-C.md
.orchestration/sandboxes/WP-D.md
.orchestration/sandboxes/WP-F.md
.orchestration/sandboxes/WP-G.md
.orchestration/sandboxes/WP-H.md
.orchestration/sandboxes/WP-I.md
.orchestration/sandboxes/WP-J.md
.orchestration/sandboxes/WP-K.md
.orchestration/sandboxes/dot-audit-profile-gpt6-sol-T48-a01.md
.orchestration/sandboxes/dot-ccstatusline-ubuntu26-hang-T59-a01.md
.orchestration/sandboxes/dot-ci-runner-label-pin-T58-a01.md
.orchestration/sandboxes/dot-codex-worktree-git-writable-T50-a01.md
.orchestration/sandboxes/dot-crit-linux-T1-a01.md
.orchestration/sandboxes/dot-formatter-hook-root-fix-T61-a01.md
.orchestration/sandboxes/dot-git-ignore-cc-writes-T56-a01.md
.orchestration/sandboxes/dot-macos-brew-untrusted-taps-T57-a01.md
.orchestration/sandboxes/dot-main-push-guard-revert-T60-a01.md
.orchestration/sandboxes/dot-orchestrator-delivery-sandbox-T49-a01.md
.orchestration/sandboxes/dot-orchestrator-linkage-evidence-T46-a01.md
.orchestration/sandboxes/dot-orchestrator-pane-profile-args-T47-a01.md
.orchestration/sandboxes/dot-plain-start-visibility-T45-a01.md
.orchestration/sandboxes/dot-pr-gate-trust-boundary-T40-a01.md
.orchestration/sandboxes/dot-shell-sp-T1-a01.md
.orchestration/sandboxes/dot-ua-graph-refresh-T55-a01.md
.orchestration/sandboxes/dot-ubuntu-parity-T2-a01.md
.orchestration/sandboxes/dot-ubuntu-parity-T4-a01.md
.orchestration/sandboxes/dotfiles-T100-compactiondb-claude-symlink-note-a01.md
.orchestration/sandboxes/dotfiles-T101-codex-worker-profile-default-a01.md
.orchestration/sandboxes/dotfiles-T102-add-worker-credential-notice-a01.md
.orchestration/sandboxes/dotfiles-T103-gh-auth-stores-a01.md
.orchestration/sandboxes/dotfiles-T104-pins-2026-10-06-a01.md
.orchestration/sandboxes/dotfiles-T107-gh-stores-per-machine-a01.md
.orchestration/sandboxes/dotfiles-T108-one-login-per-machine-a01.md
.orchestration/sandboxes/dotfiles-T109-claude-worker-merge-deny-a01.md
.orchestration/sandboxes/dotfiles-T110-gh-auth-file-storage-a01.md
.orchestration/sandboxes/dotfiles-T111-project-map-subagent-a01.md
.orchestration/sandboxes/dotfiles-T112-pins-2026-10-07-a01.md
.orchestration/sandboxes/dotfiles-T113-codify-T111-lessons-a01.md
.orchestration/sandboxes/dotfiles-T114-canonical-clone-reconcile-a01.md
.orchestration/sandboxes/dotfiles-T115-worker-audit-xhigh-a01.md
.orchestration/sandboxes/dotfiles-T116-on-demand-workers-a01.md
.orchestration/sandboxes/dotfiles-T117-upgrade-outside-canonical-clone-a01.md
.orchestration/sandboxes/dotfiles-T118-rolling-tools-single-update-a01.md
.orchestration/sandboxes/dotfiles-T119-rolling-release-assets-a01.md
.orchestration/sandboxes/dotfiles-T120-npm-provenance-and-claude-channel-a01.md
.orchestration/sandboxes/dotfiles-T121-claude-hook-install-hint-a01.md
.orchestration/sandboxes/dotfiles-T124-wave1-task-validator-a01.md
.orchestration/sandboxes/dotfiles-T124-wave3b-audit-grammar-a01.md
.orchestration/sandboxes/dotfiles-T128-aws-cli-macos-a01.md
.orchestration/sandboxes/dotfiles-T128-chain-github-scripts-a01.md
.orchestration/sandboxes/dotfiles-T128-chain-github-scripts-followup-a01.md
.orchestration/sandboxes/dotfiles-T128-chain-review-scripts-followup-a01.md
.orchestration/sandboxes/dotfiles-T128-chain-review-scripts-followup-a02.md
.orchestration/sandboxes/dotfiles-T128-ci-skip-orchestration-a01.md
.orchestration/sandboxes/dotfiles-T128-ci-skip-orchestration-a02.md
.orchestration/sandboxes/dotfiles-T128-gate-evidence-a02.md
.orchestration/sandboxes/dotfiles-T128-gate-evidence-a03.md
.orchestration/sandboxes/dotfiles-T128-gate-evidence-a04.md
.orchestration/sandboxes/dotfiles-T128-gate-wrapper-path-a01.md
.orchestration/sandboxes/dotfiles-T128-orchestrator-tools-a01.md
.orchestration/sandboxes/dotfiles-T128-orchestrator-tools-a02.md
.orchestration/sandboxes/dotfiles-T128-orchestrator-tools-a03.md
.orchestration/sandboxes/dotfiles-T128-orchestrator-tools-a04.md
.orchestration/sandboxes/dotfiles-T128-orchestrator-tools-a05.md
.orchestration/sandboxes/dotfiles-T128-orchestrator-tools-a06.md
.orchestration/sandboxes/dotfiles-T128-orchestrator-tools-followup-a01.md
.orchestration/sandboxes/dotfiles-T128-orchestrator-tools-followup-a03.md
.orchestration/sandboxes/dotfiles-T128-playbook-rules-a02.md
.orchestration/sandboxes/dotfiles-T128-playbook-rules-a03.md
.orchestration/sandboxes/dotfiles-T128-playbook-rules-a04.md
.orchestration/sandboxes/dotfiles-T128-process-rules-a01.md
.orchestration/sandboxes/dotfiles-T128-process-rules-a02.md
.orchestration/sandboxes/dotfiles-T128-process-rules-a03.md
.orchestration/sandboxes/dotfiles-T128-process-rules-a04.md
.orchestration/sandboxes/dotfiles-T128-process-rules-a05.md
.orchestration/sandboxes/dotfiles-T128-process-rules-a06.md
.orchestration/sandboxes/dotfiles-T128-process-rules-a07.md
.orchestration/sandboxes/dotfiles-T128-project-map-pane-open-a01.md
.orchestration/sandboxes/dotfiles-T128-project-map-reload-hook-a01.md
.orchestration/sandboxes/dotfiles-T128-project-map-reload-hook-followup-a01.md
.orchestration/sandboxes/dotfiles-T128-regime-counters-a01.md
.orchestration/sandboxes/dotfiles-T128-regime-counters-a02.md
.orchestration/sandboxes/dotfiles-T128-seat-liveness-a01.md
.orchestration/sandboxes/dotfiles-T128-settings-hook-dedupe-followup-a01.md
.orchestration/sandboxes/dotfiles-T128-v0-main-tests-a01.md
.orchestration/sandboxes/dotfiles-T128-worker-stop-and-watch-a01.md
.orchestration/sandboxes/dotfiles-T128-worker-stop-and-watch-a02.md
.orchestration/sandboxes/dotfiles-T62-claude-auto-deny-a01.md
.orchestration/sandboxes/dotfiles-T63-codex-execpolicy-forbidden-a01.md
.orchestration/sandboxes/dotfiles-T64-codex-worker-never-network-a01.md
.orchestration/sandboxes/dotfiles-T65-agent-stop-gate-a01.md
.orchestration/sandboxes/dotfiles-T66-permgate-dead-lanes-a01.md
.orchestration/sandboxes/dotfiles-T67-audit-task-level-a01.md
.orchestration/sandboxes/dotfiles-T68-gate-audit-evidence-a01.md
.orchestration/sandboxes/dotfiles-T69-protocol-docs-unification-a01.md
.orchestration/sandboxes/dotfiles-T70-make-update-unattended-a01.md
.orchestration/sandboxes/dotfiles-T71-generator-multi-target-a01.md
.orchestration/sandboxes/dotfiles-T72-bootstrap-ci-pins-a01.md
.orchestration/sandboxes/dotfiles-T73-tool-versions-from-config-a01.md
.orchestration/sandboxes/dotfiles-T74-bootstrap-dead-code-a01.md
.orchestration/sandboxes/dotfiles-T75-shell-dead-code-a01.md
.orchestration/sandboxes/dotfiles-T76-ineffective-settings-a01.md
.orchestration/sandboxes/dotfiles-T77-harness-dead-code-a01.md
.orchestration/sandboxes/dotfiles-T77b-enforce-uv-hook-contract-a01.md
.orchestration/sandboxes/dotfiles-T78-dead-docs-adh-a01.md
.orchestration/sandboxes/dotfiles-T79-remove-adh-profile-a01.md
.orchestration/sandboxes/dotfiles-T80-codex-command-hooks-a01.md
.orchestration/sandboxes/dotfiles-T81-compactiondb-vendor-a01.md
.orchestration/sandboxes/dotfiles-T81b-compactiondb-vendor-hygiene-a01.md
.orchestration/sandboxes/dotfiles-T82-codex-compaction-hooks-a01.md
.orchestration/sandboxes/dotfiles-T82b-codex-hook-trust-pins-a01.md
.orchestration/sandboxes/dotfiles-T83-docs-diet-a01.md
.orchestration/sandboxes/dotfiles-T84-orchestrator-kind-a01.md
.orchestration/sandboxes/dotfiles-T85-launcher-orchestrator-kind-a01.md
.orchestration/sandboxes/dotfiles-T86-codex-orchestrate-a01.md
.orchestration/sandboxes/dotfiles-T88-parallel-execution-rule-a01.md
.orchestration/sandboxes/dotfiles-T89-add-worker-same-workspace-a01.md
.orchestration/sandboxes/dotfiles-T90-github-identity-separation-a01.md
.orchestration/sandboxes/dotfiles-T90b-ruleset-sole-merger-a01.md
.orchestration/sandboxes/dotfiles-T91-secret-scan-sk-boundary-a01.md
.orchestration/sandboxes/dotfiles-T92-stop-gate-sandbox-placeholders-a01.md
.orchestration/sandboxes/dotfiles-T93-gate-masked-feedback-bodies-a01.md
.orchestration/sandboxes/dotfiles-T94-upgrade-pins-a01.md
.orchestration/sandboxes/dotfiles-T95-sandbox-placeholder-files-on-disk-a01.md
.orchestration/sandboxes/dotfiles-T96-codex-worker-gpt61-sol-high-a01.md
.orchestration/sandboxes/dotfiles-T97-claude-sandbox-github-calls-a01.md
.orchestration/sandboxes/dotfiles-T98-evidence-home-path-masking-a01.md
.orchestration/sandboxes/dotfiles-T98b-runner-home-and-review-body-a01.md
.orchestration/sandboxes/dotfiles-T98c-claude-seat-artifact-write-exception-a01.md
.orchestration/sandboxes/dotfiles-T99-nix-plans-history-a01.md
.orchestration/sandboxes/fix-chezmoi-pycache-modify-exec.md
.orchestration/tasks/T1-herdr-agents-idempotency.md
.orchestration/tasks/T11-agmsg-join-unique-identity-guard.md
.orchestration/tasks/T13-agmsg-orchestration-rule-file.md
.orchestration/tasks/T14-t13-pr-lifecycle.md
.orchestration/tasks/T15-herdr-lazy-start-attach-layout.md
.orchestration/tasks/T16-herdr-attach-layout-order-repair.md
.orchestration/tasks/T17-herdr-attach-agmsg-bootstrap.md
.orchestration/tasks/T18-herdr-agents-two-pane.md
.orchestration/tasks/T18-herdr-thirds-layout.md
.orchestration/tasks/T19-herdr-file-viewer-popup-config.md
.orchestration/tasks/T2-ensure-herdr-integrations.md
.orchestration/tasks/T20-agmsg-setup-automation.md
.orchestration/tasks/T21-model-profiles-pr.md
.orchestration/tasks/T22-doctor-settings-idempotency.md
.orchestration/tasks/T24-usage-review-automation.md
.orchestration/tasks/T29-agmsg-regime-default-on.md
.orchestration/tasks/T3-agent-config-herdr-hook.md
.orchestration/tasks/T30-orchestration-evidence-sync.md
.orchestration/tasks/T31-codex-profile-modify-pattern.md
.orchestration/tasks/T32-evidence-and-mise-sync.md
.orchestration/tasks/T33-herdr-session-design-restore.md
.orchestration/tasks/T34-profile-codex-turn-delivery.md
.orchestration/tasks/T35-evidence-sync.md
.orchestration/tasks/T36-understand-anything-analysis.md
.orchestration/tasks/T4-readme-herdr-section.md
.orchestration/tasks/T43-compactiondb-integration.md
.orchestration/tasks/T45-acceptance-memory-consolidation-rules.md
.orchestration/tasks/T46-compactiondb-recovery-config.md
.orchestration/tasks/T47-recovery-packet-sections.md
.orchestration/tasks/T48-codex-notify-ingest.md
.orchestration/tasks/T48b-ingest-source-attribution.md
.orchestration/tasks/T48c-notify-path-render.md
.orchestration/tasks/T49-probe-subcommand.md
.orchestration/tasks/T5-herdr-session-bootstrap.md
.orchestration/tasks/T50-recall-subcommand.md
.orchestration/tasks/T51a-shfmt-drift-fix.md
.orchestration/tasks/T52-ua-graph-update.md
.orchestration/tasks/T53-compactiondb-optin-dotfiles.md
.orchestration/tasks/T54-recovery-injection-ledger.md
.orchestration/tasks/T55-hook-composition-validation.md
.orchestration/tasks/T56-session-staleness.md
.orchestration/tasks/T56b-staleness-baseline-fix.md
.orchestration/tasks/T57-asset-install-manifest.md
.orchestration/tasks/T58-remove-agent-asset.md
.orchestration/tasks/T59-doctor-repair.md
.orchestration/tasks/T59b-repair-gaps.md
.orchestration/tasks/T6-claude-settings-modify-merge.md
.orchestration/tasks/T60-agmsg-effects-contract.md
.orchestration/tasks/T61a-ci-fixes.md
.orchestration/tasks/T61b-bot-review-fixes.md
.orchestration/tasks/T62-ua-graph-update.md
.orchestration/tasks/T62b-ua-shell-sources.md
.orchestration/tasks/T62c-ua-compactiondb-node.md
.orchestration/tasks/T63-e2e-driver-model-rule.md
.orchestration/tasks/T64-security-profile.md
.orchestration/tasks/T64b-codex-security-guidance.md
.orchestration/tasks/T65-pi-install-base.md
.orchestration/tasks/T65b-repin-0841.md
.orchestration/tasks/T66-permgate-pi.md
.orchestration/tasks/T66b-workspace-write-policy.md
.orchestration/tasks/T66c-read-semantics.md
.orchestration/tasks/T66d-tilde-normalization.md
.orchestration/tasks/T66e-strict-realpath.md
.orchestration/tasks/T67-model-access.md
.orchestration/tasks/T67b-checker-subscription-lane.md
.orchestration/tasks/T67c-checker-lane-precedence.md
.orchestration/tasks/T67d-checker-reasoning-models.md
.orchestration/tasks/T67e-checker-error-diagnostics.md
.orchestration/tasks/T68-rpc-agmsg-bridge.md
.orchestration/tasks/T68b-agmsg-send-tool.md
.orchestration/tasks/T68c-security-review-fixes.md
.orchestration/tasks/T69-contextdb-pi-extension.md
.orchestration/tasks/T7-zprofile-path-noninteractive.md
.orchestration/tasks/T70-pi-session-evidence.md
.orchestration/tasks/T74-pi-source-removal.md
.orchestration/tasks/T76-absorption.md
.orchestration/tasks/T76b-registration-grammar.md
.orchestration/tasks/T79-rule-two-tier.md
.orchestration/tasks/T79b-scope-qualifier-audit.md
.orchestration/tasks/T8-check-agent-runtime-drift.md
.orchestration/tasks/T80-codex-agents-two-tier.md
.orchestration/tasks/T81-result-cost-reporting.md
.orchestration/tasks/T83-ua-graph-update.md
.orchestration/tasks/T83b-ua-freshness-and-edges.md
.orchestration/tasks/T84-chezmoi-drift-resolution.md
.orchestration/tasks/T84b-bashsource-under-include.md
.orchestration/tasks/T84c-bats-private-profile-paths.md
.orchestration/tasks/T85-ua-graph-update-140.md
.orchestration/tasks/T9-herdr-lr-layout-gpt56sol.md
.orchestration/tasks/WP-A.md
.orchestration/tasks/WP-B.md
.orchestration/tasks/WP-C.md
.orchestration/tasks/WP-D.md
.orchestration/tasks/WP-E.md
.orchestration/tasks/WP-F.md
.orchestration/tasks/WP-G.md
.orchestration/tasks/WP-H.md
.orchestration/tasks/WP-I.md
.orchestration/tasks/WP-J.md
.orchestration/tasks/WP-K.md
.orchestration/tasks/WP-L.md
.orchestration/tasks/WP-M.md
.orchestration/tasks/dot-adh-baseline-T6-a01.md
.orchestration/tasks/dot-agmsg-upstream-sync-T19-a01.md
.orchestration/tasks/dot-asset-manifest-T15-a01.md
.orchestration/tasks/dot-audit-exec-channel-T33e-a01.md
.orchestration/tasks/dot-audit-pane-hardening-T32b-a01.md
.orchestration/tasks/dot-audit-pane-prompt-detect-T33j-a01.md
.orchestration/tasks/dot-audit-pane-visibility-T32-a01.md
.orchestration/tasks/dot-audit-profile-gpt6-sol-T48-a01.md
.orchestration/tasks/dot-audit-verdict-gate-T33b-a01.md
.orchestration/tasks/dot-ccstatusline-ubuntu26-hang-T59-a01.md
.orchestration/tasks/dot-ci-runner-label-pin-T58-a01.md
.orchestration/tasks/dot-claude-sandbox-T13-a01.md
.orchestration/tasks/dot-claude-sandbox-manifest-T39-a01.md
.orchestration/tasks/dot-codex-apparmor-userns-T30-a01.md
.orchestration/tasks/dot-env-converge-T10-a01.md
.orchestration/tasks/dot-formatter-hook-root-fix-T61-a01.md
.orchestration/tasks/dot-git-ignore-cc-writes-T56-a01.md
.orchestration/tasks/dot-herdr-agents-seat-labels-T35-a01.md
.orchestration/tasks/dot-herdr-worker-relaunch-T25-a01.md
.orchestration/tasks/dot-herdr-worker-worktree-T11-a01.md
.orchestration/tasks/dot-macos-brew-untrusted-taps-T57-a01.md
.orchestration/tasks/dot-macos-crit-pinned-install-T17-a01.md
.orchestration/tasks/dot-main-push-guard-revert-T60-a01.md
.orchestration/tasks/dot-mosh-and-asset-bumps-T31-a01.md
.orchestration/tasks/dot-orchestration-hygiene-T33i-a01.md
.orchestration/tasks/dot-orchestration-rules-T33a-a01.md
.orchestration/tasks/dot-orchestration-rules-T43-a01.md
.orchestration/tasks/dot-orchestrator-delivery-sandbox-T49-a01.md
.orchestration/tasks/dot-orchestrator-guardrails-T21-a01.md
.orchestration/tasks/dot-orchestrator-linkage-evidence-T46-a01.md
.orchestration/tasks/dot-orchestrator-pane-profile-args-T47-a01.md
.orchestration/tasks/dot-permgate-bench-flake-T33d-a01.md
.orchestration/tasks/dot-permgate-codex-stdin-T33h-a01.md
.orchestration/tasks/dot-plain-start-visibility-T45-a01.md
.orchestration/tasks/dot-pr-feedback-gate-T16-a01.md
.orchestration/tasks/dot-pr-feedback-gate-T38-a01.md
.orchestration/tasks/dot-pr-gate-trust-boundary-T40-a01.md
.orchestration/tasks/dot-restart-worker-name-wait-T27-a01.md
.orchestration/tasks/dot-sandbox-unix-sockets-T44-a01.md
.orchestration/tasks/dot-security-profile-model-T42-a01.md
.orchestration/tasks/dot-three-role-constellation-T28-a01.md
.orchestration/tasks/dot-ua-core-build-T33f-a01.md
.orchestration/tasks/dot-ua-core-build-shim-T33g-a01.md
.orchestration/tasks/dot-ua-graph-refresh-T33c-a01.md
.orchestration/tasks/dot-ua-graph-refresh-T36-a01.md
.orchestration/tasks/dot-ua-graph-refresh-T41-a01.md
.orchestration/tasks/dot-ua-graph-refresh-T55-a01.md
.orchestration/tasks/dot-ua-hook-regex-T12-a01.md
.orchestration/tasks/dot-ua-incremental-T20-a01.md
.orchestration/tasks/dot-ua-refresh-T5-a01.md
.orchestration/tasks/dot-ubuntu-parity-T2-a01.md
.orchestration/tasks/dot-ubuntu-parity-T3-a01.md
.orchestration/tasks/dot-update-convergence-T1-a01.md
.orchestration/tasks/dot-upgrade-pins-sync-T37-a01.md
.orchestration/tasks/dot-validator-worktrees-T7-a01.md
.orchestration/tasks/dot-version-currency-T29-a01.md
.orchestration/tasks/dot-worker-advisor-fable-T26-a01.md
.orchestration/tasks/dot-worker-kind-guard-T14-a01.md
.orchestration/tasks/dot-worker-profile-opus55-T24-a01.md
.orchestration/tasks/dotfiles-T100-compactiondb-claude-symlink-note-a01.md
.orchestration/tasks/dotfiles-T101-codex-worker-profile-default-a01.md
.orchestration/tasks/dotfiles-T102-add-worker-credential-notice-a01.md
.orchestration/tasks/dotfiles-T103-gh-auth-stores-a01.md
.orchestration/tasks/dotfiles-T104-pins-2026-10-06-a01.md
.orchestration/tasks/dotfiles-T105-orchestrator-kind-codex-a01.md
.orchestration/tasks/dotfiles-T106-orchestrator-kind-claude-a01.md
.orchestration/tasks/dotfiles-T107-gh-stores-per-machine-a01.md
.orchestration/tasks/dotfiles-T108-one-login-per-machine-a01.md
.orchestration/tasks/dotfiles-T109-claude-worker-merge-deny-a01.md
.orchestration/tasks/dotfiles-T110-gh-auth-file-storage-a01.md
.orchestration/tasks/dotfiles-T111-project-map-subagent-a01.md
.orchestration/tasks/dotfiles-T112-pins-2026-10-07-a01.md
.orchestration/tasks/dotfiles-T113-codify-T111-lessons-a01.md
.orchestration/tasks/dotfiles-T114-canonical-clone-reconcile-a01.md
.orchestration/tasks/dotfiles-T115-worker-audit-xhigh-a01.md
.orchestration/tasks/dotfiles-T116-on-demand-workers-a01.md
.orchestration/tasks/dotfiles-T117-upgrade-outside-canonical-clone-a01.md
.orchestration/tasks/dotfiles-T118-rolling-tools-single-update-a01.md
.orchestration/tasks/dotfiles-T119-rolling-release-assets-a01.md
.orchestration/tasks/dotfiles-T120-npm-provenance-and-claude-channel-a01.md
.orchestration/tasks/dotfiles-T121-claude-hook-install-hint-a01.md
.orchestration/tasks/dotfiles-T122-codify-bot-ci-root-cause-a01.md
.orchestration/tasks/dotfiles-T123-starship-through-mise-a01.md
.orchestration/tasks/dotfiles-T124-design-gate-and-reset-rule-a01.md
.orchestration/tasks/dotfiles-T124-design-receipt-canonical-a01.md
.orchestration/tasks/dotfiles-T124-design-review-a01.md
.orchestration/tasks/dotfiles-T124-wave1-task-validator-a01.md
.orchestration/tasks/dotfiles-T124-wave1b-redesign-profile-a01.md
.orchestration/tasks/dotfiles-T124-wave3b-audit-grammar-a01.md
.orchestration/tasks/dotfiles-T125-acceptance-automation-a01.md
.orchestration/tasks/dotfiles-T126-regime-v2-a01.md
.orchestration/tasks/dotfiles-T126-w2b-herdr-audit-delegation-a01.md
.orchestration/tasks/dotfiles-T126-w3-headless-design-review-a01.md
.orchestration/tasks/dotfiles-T128-audit-s1-report-a01.md
.orchestration/tasks/dotfiles-T128-audit-s1-report-review-a01.md
.orchestration/tasks/dotfiles-T128-aws-cli-macos-a01.md
.orchestration/tasks/dotfiles-T128-aws-cli-macos-review-a01.md
.orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/pr-cost.sh
.orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/resolve-threads.sh
.orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-review-a01.md
.orchestration/tasks/dotfiles-T128-chain-github-scripts-a01.md
.orchestration/tasks/dotfiles-T128-chain-github-scripts-followup-a01-review-a01.md
.orchestration/tasks/dotfiles-T128-chain-github-scripts-followup-a01.md
.orchestration/tasks/dotfiles-T128-chain-github-scripts-followup-a02-review-a01.md
.orchestration/tasks/dotfiles-T128-chain-github-scripts-followup-a02.md
.orchestration/tasks/dotfiles-T128-chain-github-scripts-followup-a03.md
.orchestration/tasks/dotfiles-T128-chain-glue-finish-a01.md
.orchestration/tasks/dotfiles-T128-chain-glue-finish-followup-a01.md
.orchestration/tasks/dotfiles-T128-chain-glue-finish-review-a01.md
.orchestration/tasks/dotfiles-T128-chain-glue-integrate-a01.md
.orchestration/tasks/dotfiles-T128-chain-glue-integrate-followup-a01.md
.orchestration/tasks/dotfiles-T128-chain-glue-integrate-review-a01.md
.orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-amend-review-a01.md
.orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-advisory.sh
.orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-review.sh
.orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/sandbox-scan.sh
.orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-review-a01.md
.orchestration/tasks/dotfiles-T128-chain-review-scripts-a01.md
.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a01-review-a01.md
.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a01.md
.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a02-review-a01.md
.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a02.md
.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a03.md
.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a04-review-a01.md
.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a04.md
.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a05.md
.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-review-a03.md
.orchestration/tasks/dotfiles-T128-ci-skip-orchestration-a01.md
.orchestration/tasks/dotfiles-T128-ci-skip-orchestration-a02.md
.orchestration/tasks/dotfiles-T128-ci-skip-orchestration-contract-a01.md
.orchestration/tasks/dotfiles-T128-ci-skip-redesign-a01.md
.orchestration/tasks/dotfiles-T128-design-review-a01.md
.orchestration/tasks/dotfiles-T128-doctor-codex-trust-a01.md
.orchestration/tasks/dotfiles-T128-doctor-codex-trust-review-a01.md
.orchestration/tasks/dotfiles-T128-followup-owners-review-a01.md
.orchestration/tasks/dotfiles-T128-gate-evidence-a01.md
.orchestration/tasks/dotfiles-T128-gate-evidence-a02-amend-review-a01.md
.orchestration/tasks/dotfiles-T128-gate-evidence-a02.md
.orchestration/tasks/dotfiles-T128-gate-evidence-a03-amend-review-a01.md
.orchestration/tasks/dotfiles-T128-gate-evidence-a03.md
.orchestration/tasks/dotfiles-T128-gate-evidence-a04-amend-review-a01.md
.orchestration/tasks/dotfiles-T128-gate-evidence-a04.md
.orchestration/tasks/dotfiles-T128-gate-evidence-followup-a01.md
.orchestration/tasks/dotfiles-T128-gate-evidence-redesign-a01.md
.orchestration/tasks/dotfiles-T128-gate-evidence-redesign-a02.md
.orchestration/tasks/dotfiles-T128-gate-evidence-redesign-a03.md
.orchestration/tasks/dotfiles-T128-gate-wrapper-path-a01.md
.orchestration/tasks/dotfiles-T128-gate-wrapper-path-review-a01.md
.orchestration/tasks/dotfiles-T128-homebrew-attestation-token-a01.md
.orchestration/tasks/dotfiles-T128-model-profiles-xhigh-a01.md
.orchestration/tasks/dotfiles-T128-model-profiles-xhigh-followup-a01.md
.orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-amend-review-a01.md
.orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/boundary.sh
.orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/codex-review-prompt-example.txt
.orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/design-keydiff.py
.orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/ff-main.sh
.orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/fill_sweep.py
.orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-audit.sh
.orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-gate.sh
.orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/t717-prep.sh
.orchestration/tasks/dotfiles-T128-orchestrator-tools-a01.md
.orchestration/tasks/dotfiles-T128-orchestrator-tools-a02.md
.orchestration/tasks/dotfiles-T128-orchestrator-tools-a03-amend-review-a01.md
.orchestration/tasks/dotfiles-T128-orchestrator-tools-a03.md
.orchestration/tasks/dotfiles-T128-orchestrator-tools-a04.md
.orchestration/tasks/dotfiles-T128-orchestrator-tools-a05-amend-review-a01.md
.orchestration/tasks/dotfiles-T128-orchestrator-tools-a05.md
.orchestration/tasks/dotfiles-T128-orchestrator-tools-a06.md
.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a01.md
.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a02-input/a05-record.md
.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a02-input/dotfiles-T128-chain-github-scripts-followup-a01-audit-e9404a6.last.md
.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a02-input/dotfiles-T128-orchestrator-tools-followup-a01-audit-2e77a33.last.md
.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a02-input/dotfiles-T128-validator-offline-a01-audit-39c186a.last.md
.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a02-review-a01.md
.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a02.md
.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a03.md
.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a04-review-a01.md
.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a04.md
.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-review-a03.md
.orchestration/tasks/dotfiles-T128-orchestrator-tools-redesign-a01.md
.orchestration/tasks/dotfiles-T128-orchestrator-tools-redesign-a02.md
.orchestration/tasks/dotfiles-T128-orchestrator-tools-redesign-a03.md
.orchestration/tasks/dotfiles-T128-orchestrator-tools-redesign-a04.md
.orchestration/tasks/dotfiles-T128-owner-tasks-refresh-review-a01.md
.orchestration/tasks/dotfiles-T128-plan-007-review-a01.md
.orchestration/tasks/dotfiles-T128-playbook-rules-a01.md
.orchestration/tasks/dotfiles-T128-playbook-rules-a02.md
.orchestration/tasks/dotfiles-T128-playbook-rules-a03.md
.orchestration/tasks/dotfiles-T128-playbook-rules-a04-amend-review-a01.md
.orchestration/tasks/dotfiles-T128-playbook-rules-a04.md
.orchestration/tasks/dotfiles-T128-playbook-rules-followup-a01-amend-review-a01.md
.orchestration/tasks/dotfiles-T128-playbook-rules-followup-a01.md
.orchestration/tasks/dotfiles-T128-playbook-rules-redesign-a01.md
.orchestration/tasks/dotfiles-T128-playbook-rules-redesign-a02.md
.orchestration/tasks/dotfiles-T128-playbook-rules-redesign-a03.md
.orchestration/tasks/dotfiles-T128-process-hardening-a01.md
.orchestration/tasks/dotfiles-T128-process-hardening-a02.md
.orchestration/tasks/dotfiles-T128-process-hardening-review-a01.md
.orchestration/tasks/dotfiles-T128-process-hardening-review-a02.md
.orchestration/tasks/dotfiles-T128-process-rules-a01.md
.orchestration/tasks/dotfiles-T128-process-rules-a02.md
.orchestration/tasks/dotfiles-T128-process-rules-a03.md
.orchestration/tasks/dotfiles-T128-process-rules-a04.md
.orchestration/tasks/dotfiles-T128-process-rules-a05.md
.orchestration/tasks/dotfiles-T128-process-rules-a06.md
.orchestration/tasks/dotfiles-T128-process-rules-a07.md
.orchestration/tasks/dotfiles-T128-process-rules-redesign-a01.md
.orchestration/tasks/dotfiles-T128-process-rules-redesign-a02.md
.orchestration/tasks/dotfiles-T128-process-rules-redesign-a03.md
.orchestration/tasks/dotfiles-T128-process-rules-redesign-a04.md
.orchestration/tasks/dotfiles-T128-process-rules-redesign-a05.md
.orchestration/tasks/dotfiles-T128-process-rules-redesign-a06.md
.orchestration/tasks/dotfiles-T128-project-map-pane-open-a01-followup-a01.md
.orchestration/tasks/dotfiles-T128-project-map-pane-open-a01-followup-a02.md
.orchestration/tasks/dotfiles-T128-project-map-pane-open-a01-followup-review-a01.md
.orchestration/tasks/dotfiles-T128-project-map-pane-open-a01-review-a01.md
.orchestration/tasks/dotfiles-T128-project-map-pane-open-a01.md
.orchestration/tasks/dotfiles-T128-project-map-reload-hook-a01-amend-review-a01.md
.orchestration/tasks/dotfiles-T128-project-map-reload-hook-a01-amend-review-a02.md
.orchestration/tasks/dotfiles-T128-project-map-reload-hook-a01.md
.orchestration/tasks/dotfiles-T128-project-map-reload-hook-followup-a01.md
.orchestration/tasks/dotfiles-T128-project-map-reload-hook-followup-review-a01.md
.orchestration/tasks/dotfiles-T128-project-map-reload-hook-review-a01.md
.orchestration/tasks/dotfiles-T128-regime-counters-a01.md
.orchestration/tasks/dotfiles-T128-regime-counters-a02.md
.orchestration/tasks/dotfiles-T128-regime-counters-redesign-a01.md
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md
.orchestration/tasks/dotfiles-T128-regime-v3-inv6-redesign-a01.md
.orchestration/tasks/dotfiles-T128-rules-s1-replan-a01.md
.orchestration/tasks/dotfiles-T128-rules-s1-replan-review-a01.md
.orchestration/tasks/dotfiles-T128-rules-step8-a01.md
.orchestration/tasks/dotfiles-T128-rules-step8-followup-a01.md
.orchestration/tasks/dotfiles-T128-rules-step8-review-a01.md
.orchestration/tasks/dotfiles-T128-s1-replan-gate-a01.md
.orchestration/tasks/dotfiles-T128-s1-replan-gate-followup-a01.md
.orchestration/tasks/dotfiles-T128-s1-replan-gate-review-a01.md
.orchestration/tasks/dotfiles-T128-seat-launch-args-a01.md
.orchestration/tasks/dotfiles-T128-seat-launch-args-followup-a01.md
.orchestration/tasks/dotfiles-T128-seat-launch-args-review-a01.md
.orchestration/tasks/dotfiles-T128-seat-liveness-a01.md
.orchestration/tasks/dotfiles-T128-seat-liveness-followup-a01.md
.orchestration/tasks/dotfiles-T128-seat-liveness-followup-a02-review-a01.md
.orchestration/tasks/dotfiles-T128-seat-liveness-followup-a02.md
.orchestration/tasks/dotfiles-T128-seat-liveness-followup-review-a01.md
.orchestration/tasks/dotfiles-T128-seat-liveness-review-a01.md
.orchestration/tasks/dotfiles-T128-settings-hook-dedupe-a01.md
.orchestration/tasks/dotfiles-T128-settings-hook-dedupe-followup-a01.md
.orchestration/tasks/dotfiles-T128-settings-hook-dedupe-followup-review-a01.md
.orchestration/tasks/dotfiles-T128-settings-hook-dedupe-review-a01.md
.orchestration/tasks/dotfiles-T128-task-checkers-a01-amend-review-a01.md
.orchestration/tasks/dotfiles-T128-task-checkers-a01-amend-review-a02.md
.orchestration/tasks/dotfiles-T128-task-checkers-a01-input/ledger-check.py
.orchestration/tasks/dotfiles-T128-task-checkers-a01-input/task-consistency-check.py
.orchestration/tasks/dotfiles-T128-task-checkers-a01.md
.orchestration/tasks/dotfiles-T128-task-checkers-followup-a01.md
.orchestration/tasks/dotfiles-T128-task-checkers-followup-review-a01.md
.orchestration/tasks/dotfiles-T128-task-checkers-review-a01.md
.orchestration/tasks/dotfiles-T128-task-review-a201-a01.md
.orchestration/tasks/dotfiles-T128-task-review-contracts-a01.md
.orchestration/tasks/dotfiles-T128-task-review-phase-a-a01.md
.orchestration/tasks/dotfiles-T128-task-review-phase1-a01.md
.orchestration/tasks/dotfiles-T128-task-review-phase1-amend-a01.md
.orchestration/tasks/dotfiles-T128-task-review-phase1-amend-a02.md
.orchestration/tasks/dotfiles-T128-task-review-t718-a01.md
.orchestration/tasks/dotfiles-T128-task-review-t718-a02.md
.orchestration/tasks/dotfiles-T128-task-review-v1-v2-a01.md
.orchestration/tasks/dotfiles-T128-update-bootstrap-canonical-a01.md
.orchestration/tasks/dotfiles-T128-v0-main-tests-a01.md
.orchestration/tasks/dotfiles-T128-v1-task-schema-a01.md
.orchestration/tasks/dotfiles-T128-v1-task-schema-contract-a01.md
.orchestration/tasks/dotfiles-T128-v1b-pr-caps-a01.md
.orchestration/tasks/dotfiles-T128-v1c-regime-ci-check-a01.md
.orchestration/tasks/dotfiles-T128-v2-audit-schema-and-runner-a01.md
.orchestration/tasks/dotfiles-T128-v2-audit-schema-and-runner-contract-a01.md
.orchestration/tasks/dotfiles-T128-validator-offline-a01.md
.orchestration/tasks/dotfiles-T128-validator-offline-review-a01.md
.orchestration/tasks/dotfiles-T128-worker-s1-stop-a01.md
.orchestration/tasks/dotfiles-T128-worker-s1-stop-review-a01.md
.orchestration/tasks/dotfiles-T128-worker-stop-and-watch-a01.md
.orchestration/tasks/dotfiles-T128-worker-stop-and-watch-a02.md
.orchestration/tasks/dotfiles-T128-worker-stop-and-watch-redesign-a01.md
.orchestration/tasks/dotfiles-T129-anthropic-auth-route-check-a01.md
.orchestration/tasks/dotfiles-T129-anthropic-auth-route-check-followup-a01.md
.orchestration/tasks/dotfiles-T129-assets-omp-hcom-a01.md
.orchestration/tasks/dotfiles-T129-assets-omp-hcom-followup-a01.md
.orchestration/tasks/dotfiles-T129-assets-omp-hcom-review-a01.md
.orchestration/tasks/dotfiles-T129-audit-inherit-replan-json-a01.md
.orchestration/tasks/dotfiles-T129-audit-inherit-replan-json-followup-a01.md
.orchestration/tasks/dotfiles-T129-audit-inherit-replan-json-review-a01.md
.orchestration/tasks/dotfiles-T129-doctor-sleep-disabled-a01.md
.orchestration/tasks/dotfiles-T129-integration-seat-result-gate-cap-a01.md
.orchestration/tasks/dotfiles-T129-integration-seat-result-gate-cap-followup-a01.md
.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md
.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-followup-a01.md
.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-review-a01.md
.orchestration/tasks/dotfiles-T129-orchestrator-load-mechanisms-a01.md
.orchestration/tasks/dotfiles-T129-pstack-asset-a01.md
.orchestration/tasks/dotfiles-T129-pstack-asset-review-a01.md
.orchestration/tasks/dotfiles-T130-claude-sandbox-integration-a01.md
.orchestration/tasks/dotfiles-T130-claude-sandbox-integration-followup-a01.md
.orchestration/tasks/dotfiles-T130-codex-local-review-exclusion-a01.md
.orchestration/tasks/dotfiles-T130-sandbox-portability-a01.md
.orchestration/tasks/dotfiles-T62-claude-auto-deny-a01.md
.orchestration/tasks/dotfiles-T63-codex-execpolicy-forbidden-a01.md
.orchestration/tasks/dotfiles-T64-codex-worker-never-network-a01.md
.orchestration/tasks/dotfiles-T65-agent-stop-gate-a01.md
.orchestration/tasks/dotfiles-T66-permgate-dead-lanes-a01.md
.orchestration/tasks/dotfiles-T67-audit-task-level-a01.md
.orchestration/tasks/dotfiles-T68-gate-audit-evidence-a01.md
.orchestration/tasks/dotfiles-T69-protocol-docs-unification-a01.md
.orchestration/tasks/dotfiles-T70-make-update-unattended-a01.md
.orchestration/tasks/dotfiles-T71-generator-multi-target-a01.md
.orchestration/tasks/dotfiles-T72-bootstrap-ci-pins-a01.md
.orchestration/tasks/dotfiles-T73-tool-versions-from-config-a01.md
.orchestration/tasks/dotfiles-T74-bootstrap-dead-code-a01.md
.orchestration/tasks/dotfiles-T75-shell-dead-code-a01.md
.orchestration/tasks/dotfiles-T76-ineffective-settings-a01.md
.orchestration/tasks/dotfiles-T77-harness-dead-code-a01.md
.orchestration/tasks/dotfiles-T77b-enforce-uv-hook-contract-a01.md
.orchestration/tasks/dotfiles-T78-dead-docs-adh-a01.md
.orchestration/tasks/dotfiles-T79-remove-adh-profile-a01.md
.orchestration/tasks/dotfiles-T80-codex-command-hooks-a01.md
.orchestration/tasks/dotfiles-T81-compactiondb-vendor-a01.md
.orchestration/tasks/dotfiles-T81b-compactiondb-vendor-hygiene-a01.md
.orchestration/tasks/dotfiles-T82-codex-compaction-hooks-a01.md
.orchestration/tasks/dotfiles-T82b-codex-hook-trust-pins-a01.md
.orchestration/tasks/dotfiles-T83-docs-diet-a01.md
.orchestration/tasks/dotfiles-T84-orchestrator-kind-a01.md
.orchestration/tasks/dotfiles-T85-launcher-orchestrator-kind-a01.md
.orchestration/tasks/dotfiles-T86-codex-orchestrate-a01.md
.orchestration/tasks/dotfiles-T87-live-e2e-matrix-a01.md
.orchestration/tasks/dotfiles-T88-parallel-execution-rule-a01.md
.orchestration/tasks/dotfiles-T89-add-worker-same-workspace-a01.md
.orchestration/tasks/dotfiles-T90-github-identity-separation-a01.md
.orchestration/tasks/dotfiles-T90b-ruleset-sole-merger-a01.md
.orchestration/tasks/dotfiles-T91-secret-scan-sk-boundary-a01.md
.orchestration/tasks/dotfiles-T92-stop-gate-sandbox-placeholders-a01.md
.orchestration/tasks/dotfiles-T93-gate-masked-feedback-bodies-a01.md
.orchestration/tasks/dotfiles-T94-pending-pins.patch
.orchestration/tasks/dotfiles-T94-upgrade-pins-a01.md
.orchestration/tasks/dotfiles-T95-sandbox-placeholder-files-on-disk-a01.md
.orchestration/tasks/dotfiles-T96-codex-worker-gpt61-sol-high-a01.md
.orchestration/tasks/dotfiles-T97-claude-sandbox-github-calls-a01.md
.orchestration/tasks/dotfiles-T98-evidence-home-path-masking-a01.md
.orchestration/tasks/dotfiles-T98b-runner-home-and-review-body-a01.md
.orchestration/tasks/dotfiles-T98c-claude-seat-artifact-write-exception-a01.md
.orchestration/tasks/dotfiles-T99-nix-plans-history-a01.md
.orchestration/tasks/fix-chezmoi-pycache-modify-exec.md
.orchestration/tasks/plan-001.md
.orchestration/tasks/plan-002.md
.orchestration/tasks/plan-003.md
.orchestration/tasks/refkit-P0-01.md
.orchestration/tasks/refkit-P1.md
.orchestration/tasks/refkit-P2-A.md
.orchestration/tasks/refkit-P2-B.md
.orchestration/tasks/refkit-P2-C.md
.orchestration/tasks/refkit-P3.md
.orchestration/tasks/refkit-P4.md
.orchestration/tasks/refkit-P4b.md
.orchestration/tasks/refkit-P5.md
.orchestration/tasks/refkit-P6.md
.orchestration/tasks/refkit-P7.md
.orchestration/tasks/refkit-P8-a.md
.orchestration/tasks/refkit-P8-b.md
.orchestration/tasks/refkit-P8.md
.orchestration/templates/task-short.md
.orchestration/validation/T10-herdr-files-pane.md
.orchestration/validation/T15-V1-verify.md
.orchestration/validation/T15-herdr-lazy-start-attach-layout.md
.orchestration/validation/T16-herdr-attach-layout-order-repair.md
.orchestration/validation/T18-herdr-agents-two-pane.md
.orchestration/validation/T18-herdr-thirds-layout.md
.orchestration/validation/T19-herdr-file-viewer-popup-config.md
.orchestration/validation/T20-agmsg-setup-automation.md
.orchestration/validation/T21-final-integration.txt
.orchestration/validation/T22-doctor-settings-idempotency.txt
.orchestration/validation/T24-usage-review-automation.txt
.orchestration/validation/T26-pr86-herdr-rebase.txt
.orchestration/validation/T28-ccgate-removal-permgate-deploy.txt
.orchestration/validation/T29-agmsg-regime-default-on.md
.orchestration/validation/T30-orchestration-evidence-sync.md
.orchestration/validation/T31-codex-profile-modify-pattern.md
.orchestration/validation/T32-evidence-and-mise-sync.md
.orchestration/validation/T48.txt
.orchestration/validation/T48c.txt
.orchestration/validation/T5.txt
.orchestration/validation/T51-e2e.txt
.orchestration/validation/T53.txt
.orchestration/validation/T56b-crit-comments.json
.orchestration/validation/T57.txt
.orchestration/validation/T59.txt
.orchestration/validation/T59b-crit-comments.json
.orchestration/validation/T6.txt
.orchestration/validation/T61a.txt
.orchestration/validation/T61b.txt
.orchestration/validation/T63.txt
.orchestration/validation/T66b.txt
.orchestration/validation/T66c.txt
.orchestration/validation/T66d.txt
.orchestration/validation/T66e.txt
.orchestration/validation/T68b.txt
.orchestration/validation/T68c.txt
.orchestration/validation/T7.txt
.orchestration/validation/T70.txt
.orchestration/validation/T74.txt
.orchestration/validation/T8.txt
.orchestration/validation/T84b-validation.md
.orchestration/validation/WP-B.txt
.orchestration/validation/WP-C.txt
.orchestration/validation/WP-D.txt
.orchestration/validation/WP-F.txt
.orchestration/validation/WP-G.txt
.orchestration/validation/WP-H.txt
.orchestration/validation/WP-M.txt
.orchestration/validation/baseline-20260925.md
.orchestration/validation/codex-usage-2026-10-05.md
.orchestration/validation/dot-adh-baseline-T6-a01.md
.orchestration/validation/dot-agent-assets-T1-a01.md
.orchestration/validation/dot-agmsg-dispatch-T4-a01.md
.orchestration/validation/dot-agmsg-upstream-sync-T19-a01-audit-r2.md
.orchestration/validation/dot-agmsg-upstream-sync-T19-a01.md
.orchestration/validation/dot-asset-manifest-T15-a01.md
.orchestration/validation/dot-audit-exec-channel-T33e-a01-audit-rev2.md
.orchestration/validation/dot-audit-exec-channel-T33e-a01-audit.md
.orchestration/validation/dot-audit-exec-channel-T33e-a01-live-e2e.md
.orchestration/validation/dot-audit-exec-channel-T33e-a01.md
.orchestration/validation/dot-audit-pane-hardening-T32b-a01-audit.md
.orchestration/validation/dot-audit-pane-hardening-T32b-a01-live-e2e.md
.orchestration/validation/dot-audit-pane-hardening-T32b-a01.md
.orchestration/validation/dot-audit-pane-prompt-detect-T33j-a01-audit.md
.orchestration/validation/dot-audit-pane-prompt-detect-T33j-a01-live-e2e-2.md
.orchestration/validation/dot-audit-pane-prompt-detect-T33j-a01-live-e2e.md
.orchestration/validation/dot-audit-pane-prompt-detect-T33j-a01.md
.orchestration/validation/dot-audit-pane-visibility-T32-a01-audit.md
.orchestration/validation/dot-audit-pane-visibility-T32-a01-live-e2e.md
.orchestration/validation/dot-audit-pane-visibility-T32-a01.md
.orchestration/validation/dot-audit-profile-gpt6-sol-T48-a01-audit-81d720f.md
.orchestration/validation/dot-audit-profile-gpt6-sol-T48-a01-audit-8956c3d.md
.orchestration/validation/dot-audit-profile-gpt6-sol-T48-a01.md
.orchestration/validation/dot-audit-verdict-gate-T33b-a01-audit-rev2.md
.orchestration/validation/dot-audit-verdict-gate-T33b-a01-audit-rev3.md
.orchestration/validation/dot-audit-verdict-gate-T33b-a01-audit.md
.orchestration/validation/dot-audit-verdict-gate-T33b-a01-live-e2e.md
.orchestration/validation/dot-audit-verdict-gate-T33b-a01.md
.orchestration/validation/dot-builtin-git-auto-T1-a01.md
.orchestration/validation/dot-ccstatusline-ubuntu26-hang-T59-a01-audit.md
.orchestration/validation/dot-ccstatusline-ubuntu26-hang-T59-a01-audit.md.last.md
.orchestration/validation/dot-ccstatusline-ubuntu26-hang-T59-a01-crit.json
.orchestration/validation/dot-ccstatusline-ubuntu26-hang-T59-a01-pr-feedback.json
.orchestration/validation/dot-ccstatusline-ubuntu26-hang-T59-a01-review-receipt.md
.orchestration/validation/dot-ccstatusline-ubuntu26-hang-T59-a01.md
.orchestration/validation/dot-ci-runner-label-pin-T58-a01-audit.md
.orchestration/validation/dot-ci-runner-label-pin-T58-a01-audit.md.last.md
.orchestration/validation/dot-ci-runner-label-pin-T58-a01-crit.json
.orchestration/validation/dot-ci-runner-label-pin-T58-a01-pr-feedback.json
.orchestration/validation/dot-ci-runner-label-pin-T58-a01-review-receipt.md
.orchestration/validation/dot-ci-runner-label-pin-T58-a01.md
.orchestration/validation/dot-claude-sandbox-T13-a01.md
.orchestration/validation/dot-claude-sandbox-manifest-T39-a01-audit-841e12b.md
.orchestration/validation/dot-claude-sandbox-manifest-T39-a01-audit.md
.orchestration/validation/dot-claude-sandbox-manifest-T39-a01.md
.orchestration/validation/dot-codex-apparmor-userns-T30-a01-audit.md
.orchestration/validation/dot-codex-apparmor-userns-T30-a01.md
.orchestration/validation/dot-codex-worktree-git-writable-T50-a01-audit-5952ab8.md
.orchestration/validation/dot-codex-worktree-git-writable-T50-a01-audit-e334af5.md
.orchestration/validation/dot-codex-worktree-git-writable-T50-a01.md
.orchestration/validation/dot-crit-linux-T1-a01.md
.orchestration/validation/dot-dependabot-verify-T8-a01.md
.orchestration/validation/dot-docs-align-T1-a01.md
.orchestration/validation/dot-env-converge-T10-a01.md
.orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-0827371f.md
.orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-0827371f.md.last.md
.orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-45d44292.md
.orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-45d44292.md.last.md
.orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-57021632.md
.orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-57021632.md.last.md
.orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-74ade52f.md
.orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-74ade52f.md.last.md
.orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-772ff3c6.md
.orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-772ff3c6.md.last.md
.orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-7dff3a5c.md
.orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-7dff3a5c.md.last.md
.orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-ae806f37.md
.orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-ae806f37.md.last.md
.orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-b5084de5.md
.orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-b5084de5.md.last.md
.orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-bd9a7995.md
.orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-bd9a7995.md.last.md
.orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-e5648fa6.md
.orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-e5648fa6.md.last.md
.orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-ff37f41d.md
.orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-ff37f41d.md.last.md
.orchestration/validation/dot-formatter-hook-root-fix-T61-a01-crit.json
.orchestration/validation/dot-formatter-hook-root-fix-T61-a01-pr-feedback.json
.orchestration/validation/dot-formatter-hook-root-fix-T61-a01-review-receipt.md
.orchestration/validation/dot-formatter-hook-root-fix-T61-a01.md
.orchestration/validation/dot-git-ignore-cc-writes-T56-a01-audit.md
.orchestration/validation/dot-git-ignore-cc-writes-T56-a01-audit.md.last.md
.orchestration/validation/dot-git-ignore-cc-writes-T56-a01-crit.json
.orchestration/validation/dot-git-ignore-cc-writes-T56-a01-pr-feedback.json
.orchestration/validation/dot-git-ignore-cc-writes-T56-a01-review-receipt.md
.orchestration/validation/dot-git-ignore-cc-writes-T56-a01.md
.orchestration/validation/dot-herdr-agents-add-worker-T22-a01-audit-r4.md
.orchestration/validation/dot-herdr-agents-add-worker-T22-a01-audit-r5.md
.orchestration/validation/dot-herdr-agents-add-worker-T22-a01-audit-r6.md
.orchestration/validation/dot-herdr-agents-add-worker-T22-a01.md
.orchestration/validation/dot-herdr-agents-seat-labels-T35-a01-audit-rev2.md
.orchestration/validation/dot-herdr-agents-seat-labels-T35-a01-audit.md
.orchestration/validation/dot-herdr-agents-seat-labels-T35-a01-live-e2e.md
.orchestration/validation/dot-herdr-agents-seat-labels-T35-a01.md
.orchestration/validation/dot-herdr-sheldon-T1-a02.md
.orchestration/validation/dot-herdr-worker-relaunch-T25-a01.md
.orchestration/validation/dot-macos-brew-untrusted-taps-T57-a01-audit-rev1.md
.orchestration/validation/dot-macos-brew-untrusted-taps-T57-a01-audit-rev1.md.last.md
.orchestration/validation/dot-macos-brew-untrusted-taps-T57-a01-audit.md
.orchestration/validation/dot-macos-brew-untrusted-taps-T57-a01-audit.md.last.md
.orchestration/validation/dot-macos-brew-untrusted-taps-T57-a01-crit.json
.orchestration/validation/dot-macos-brew-untrusted-taps-T57-a01-pr-feedback.json
.orchestration/validation/dot-macos-brew-untrusted-taps-T57-a01-review-receipt.md
.orchestration/validation/dot-macos-brew-untrusted-taps-T57-a01.md
.orchestration/validation/dot-main-push-guard-revert-T60-a01-audit-4445917b.md
.orchestration/validation/dot-main-push-guard-revert-T60-a01-audit-4445917b.md.last.md
.orchestration/validation/dot-main-push-guard-revert-T60-a01-audit-560df81b.md
.orchestration/validation/dot-main-push-guard-revert-T60-a01-audit-560df81b.md.last.md
.orchestration/validation/dot-main-push-guard-revert-T60-a01-audit-rev1.md
.orchestration/validation/dot-main-push-guard-revert-T60-a01-audit-rev1.md.last.md
.orchestration/validation/dot-main-push-guard-revert-T60-a01-audit.md
.orchestration/validation/dot-main-push-guard-revert-T60-a01-audit.md.last.md
.orchestration/validation/dot-main-push-guard-revert-T60-a01-crit.json
.orchestration/validation/dot-main-push-guard-revert-T60-a01-pr-feedback.json
.orchestration/validation/dot-main-push-guard-revert-T60-a01-review-receipt.md
.orchestration/validation/dot-main-push-guard-revert-T60-a01.md
.orchestration/validation/dot-mise-pin-test-sync-T53-a01-audit.md
.orchestration/validation/dot-mise-pin-test-sync-T53-a01.md
.orchestration/validation/dot-mise-symlink-T3-a01.md
.orchestration/validation/dot-mkt-mode-T1-a01.md
.orchestration/validation/dot-mkt-owner-T1-a01.md
.orchestration/validation/dot-mosh-and-asset-bumps-T31-a01-audit.md
.orchestration/validation/dot-mosh-and-asset-bumps-T31-a01.md
.orchestration/validation/dot-orchestration-hygiene-T33i-a01-audit-rev2.md
.orchestration/validation/dot-orchestration-hygiene-T33i-a01-audit-rev3.md
.orchestration/validation/dot-orchestration-hygiene-T33i-a01-audit.md
.orchestration/validation/dot-orchestration-hygiene-T33i-a01.md
.orchestration/validation/dot-orchestration-rules-T33a-a01-audit-rev3.md
.orchestration/validation/dot-orchestration-rules-T33a-a01-audit.md
.orchestration/validation/dot-orchestration-rules-T33a-a01.md
.orchestration/validation/dot-orchestration-rules-T43-a01-audit-0a34a68.md
.orchestration/validation/dot-orchestration-rules-T43-a01-audit-0a34a68.md.last.md
.orchestration/validation/dot-orchestration-rules-T43-a01-audit-12d3f80.md
.orchestration/validation/dot-orchestration-rules-T43-a01-audit-1843dd1.md
.orchestration/validation/dot-orchestration-rules-T43-a01-audit-1b6741b.md
.orchestration/validation/dot-orchestration-rules-T43-a01-audit-56f308c.md
.orchestration/validation/dot-orchestration-rules-T43-a01-audit-6b53337.md
.orchestration/validation/dot-orchestration-rules-T43-a01-audit-72746d4.md
.orchestration/validation/dot-orchestration-rules-T43-a01-audit-85919df.md
.orchestration/validation/dot-orchestration-rules-T43-a01-audit-99c1174.md
.orchestration/validation/dot-orchestration-rules-T43-a01-audit-afb2c9d.md
.orchestration/validation/dot-orchestration-rules-T43-a01-audit-c878b0d.md
.orchestration/validation/dot-orchestration-rules-T43-a01-audit.md
.orchestration/validation/dot-orchestration-rules-T43-a01.md
.orchestration/validation/dot-orchestrator-delivery-sandbox-T49-a01-audit-00268f1.md
.orchestration/validation/dot-orchestrator-delivery-sandbox-T49-a01-audit-11d87f3.md
.orchestration/validation/dot-orchestrator-delivery-sandbox-T49-a01-audit-1fa2a48.md
.orchestration/validation/dot-orchestrator-delivery-sandbox-T49-a01-audit-229896a.md
.orchestration/validation/dot-orchestrator-delivery-sandbox-T49-a01-audit-4452516.md
.orchestration/validation/dot-orchestrator-delivery-sandbox-T49-a01-audit-50ebfdc.md
.orchestration/validation/dot-orchestrator-delivery-sandbox-T49-a01-audit-63d4e03.md
.orchestration/validation/dot-orchestrator-delivery-sandbox-T49-a01-audit-68ac54d.md
.orchestration/validation/dot-orchestrator-delivery-sandbox-T49-a01-audit-99d734b.md
.orchestration/validation/dot-orchestrator-delivery-sandbox-T49-a01-audit-9b658a9.md
.orchestration/validation/dot-orchestrator-delivery-sandbox-T49-a01-audit-9dc4e53.md
.orchestration/validation/dot-orchestrator-delivery-sandbox-T49-a01-audit-e4903a1.md
.orchestration/validation/dot-orchestrator-delivery-sandbox-T49-a01.md
.orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01-audit-00573f3.md
.orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01-audit-2721f0c.md
.orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01-audit-63c993b.md
.orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01-audit-7d0c585.md
.orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01-audit-91cc85f.md
.orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01-audit-98ea49f.md
.orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01-audit-9e36e63.md
.orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01-audit-a71e78d.md
.orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01-audit-b29ef04.md
.orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01-audit-b91f949.md
.orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01-audit-bec48d4.md
.orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01-audit-d806a3d.md
.orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01.md
.orchestration/validation/dot-orchestrator-pane-profile-args-T47-a01-audit-7103797.md
.orchestration/validation/dot-orchestrator-pane-profile-args-T47-a01.md
.orchestration/validation/dot-permgate-bench-flake-T33d-a01-audit.md
.orchestration/validation/dot-permgate-bench-flake-T33d-a01.md
.orchestration/validation/dot-permgate-codex-stdin-T33h-a01-audit.md
.orchestration/validation/dot-permgate-codex-stdin-T33h-a01.md
.orchestration/validation/dot-plain-start-visibility-T45-a01-audit-0a35010.md
.orchestration/validation/dot-plain-start-visibility-T45-a01-audit-51f8bc7.md
.orchestration/validation/dot-plain-start-visibility-T45-a01-audit-89e95e4.md
.orchestration/validation/dot-plain-start-visibility-T45-a01-audit-9eb3e43.md
.orchestration/validation/dot-plain-start-visibility-T45-a01-audit-dfdfbe8.md
.orchestration/validation/dot-plain-start-visibility-T45-a01-audit-e6f350b.md
.orchestration/validation/dot-plain-start-visibility-T45-a01.md
.orchestration/validation/dot-pr-feedback-gate-T38-a01-audit-fa934f7.md
.orchestration/validation/dot-pr-feedback-gate-T38-a01-audit.md
.orchestration/validation/dot-pr-feedback-gate-T38-a01.md
.orchestration/validation/dot-pr-gate-trust-boundary-T40-a01-audit-0dfe823.md
.orchestration/validation/dot-pr-gate-trust-boundary-T40-a01-audit-10dfc10.md
.orchestration/validation/dot-pr-gate-trust-boundary-T40-a01-audit-c67ec77.md
.orchestration/validation/dot-pr-gate-trust-boundary-T40-a01.md
.orchestration/validation/dot-restart-worker-name-wait-T27-a01.md
.orchestration/validation/dot-sandbox-unix-sockets-T44-a01-audit-c2c1f62.md
.orchestration/validation/dot-sandbox-unix-sockets-T44-a01-audit-dcb8839.md
.orchestration/validation/dot-sandbox-unix-sockets-T44-a01.md
.orchestration/validation/dot-security-profile-model-T42-a01-audit.md
.orchestration/validation/dot-security-profile-model-T42-a01.md
.orchestration/validation/dot-shell-sp-T1-a01.md
.orchestration/validation/dot-three-role-constellation-T28-a01-audit.md
.orchestration/validation/dot-three-role-constellation-T28-a01.md
.orchestration/validation/dot-ua-core-build-T33f-a01-audit-rev2.md
.orchestration/validation/dot-ua-core-build-T33f-a01-audit.md
.orchestration/validation/dot-ua-core-build-T33f-a01.md
.orchestration/validation/dot-ua-core-build-shim-T33g-a01-audit.md
.orchestration/validation/dot-ua-core-build-shim-T33g-a01.md
.orchestration/validation/dot-ua-full-T9-a01.md
.orchestration/validation/dot-ua-graph-refresh-T33c-a01-audit-rev2.md
.orchestration/validation/dot-ua-graph-refresh-T33c-a01-audit.md
.orchestration/validation/dot-ua-graph-refresh-T33c-a01.md
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md
.orchestration/validation/dot-ua-graph-refresh-T36-a01.md
.orchestration/validation/dot-ua-graph-refresh-T41-a01-audit-rev2.md
.orchestration/validation/dot-ua-graph-refresh-T41-a01-audit.md
.orchestration/validation/dot-ua-graph-refresh-T41-a01.md
.orchestration/validation/dot-ua-graph-refresh-T51-a01.md
.orchestration/validation/dot-ua-graph-refresh-T55-a01-audit-rev1.md
.orchestration/validation/dot-ua-graph-refresh-T55-a01-audit-rev1.md.last.md
.orchestration/validation/dot-ua-graph-refresh-T55-a01-audit.md
.orchestration/validation/dot-ua-graph-refresh-T55-a01-audit.md.last.md
.orchestration/validation/dot-ua-graph-refresh-T55-a01-crit.json
.orchestration/validation/dot-ua-graph-refresh-T55-a01-pr-feedback.json
.orchestration/validation/dot-ua-graph-refresh-T55-a01-review-receipt.md
.orchestration/validation/dot-ua-graph-refresh-T55-a01.md
.orchestration/validation/dot-ua-refresh-T5-a01.md
.orchestration/validation/dot-ua-refresh-policy-T52-a01-audit-f700b14.md
.orchestration/validation/dot-ua-refresh-policy-T52-a01.md
.orchestration/validation/dot-ubuntu-fix-T1-a01.md
.orchestration/validation/dot-ubuntu-parity-T2-a01.md
.orchestration/validation/dot-ubuntu-parity-T3-a01.md
.orchestration/validation/dot-ubuntu-parity-T7-a01.md
.orchestration/validation/dot-ubuntu-parity-T9-a01.md
.orchestration/validation/dot-update-conv-T1-a01.md
.orchestration/validation/dot-update-convergence-T1-a01.md
.orchestration/validation/dot-upgrade-pin-path-codify-T54-a01-audit-1128abb.md
.orchestration/validation/dot-upgrade-pin-path-codify-T54-a01-audit-c636452.md
.orchestration/validation/dot-upgrade-pin-path-codify-T54-a01-audit.md
.orchestration/validation/dot-upgrade-pin-path-codify-T54-a01.md
.orchestration/validation/dot-upgrade-pins-T2-a01.md
.orchestration/validation/dot-upgrade-pins-sync-T37-a01-audit.md
.orchestration/validation/dot-upgrade-pins-sync-T37-a01.md
.orchestration/validation/dot-upgrade-regen-T1-a01.md
.orchestration/validation/dot-validator-worktrees-T7-a01.md
.orchestration/validation/dot-version-currency-T29-a01-audit.md
.orchestration/validation/dot-version-currency-T29-a01.md
.orchestration/validation/dot-worker-advisor-fable-T26-a01.md
.orchestration/validation/dot-worker-kind-guard-T14-a01.md
.orchestration/validation/dot-worker-profile-opus55-T24-a01.md
.orchestration/validation/dotfiles-T100-compactiondb-claude-symlink-note-a01-audit-bc001fc.md
.orchestration/validation/dotfiles-T100-compactiondb-claude-symlink-note-a01-audit-bc001fc.md.last.md
.orchestration/validation/dotfiles-T100-compactiondb-claude-symlink-note-a01-crit.json
.orchestration/validation/dotfiles-T100-compactiondb-claude-symlink-note-a01-pr-feedback.json
.orchestration/validation/dotfiles-T100-compactiondb-claude-symlink-note-a01-review-receipt.md
.orchestration/validation/dotfiles-T100-compactiondb-claude-symlink-note-a01-worker-crit.json
.orchestration/validation/dotfiles-T100-compactiondb-claude-symlink-note-a01-worker-review-receipt.md
.orchestration/validation/dotfiles-T100-compactiondb-claude-symlink-note-a01.md
.orchestration/validation/dotfiles-T101-codex-worker-profile-default-a01-audit-462bbb1.md
.orchestration/validation/dotfiles-T101-codex-worker-profile-default-a01-audit-462bbb1.md.last.md
.orchestration/validation/dotfiles-T101-codex-worker-profile-default-a01-crit.json
.orchestration/validation/dotfiles-T101-codex-worker-profile-default-a01-pr-feedback.json
.orchestration/validation/dotfiles-T101-codex-worker-profile-default-a01-review-receipt.md
.orchestration/validation/dotfiles-T101-codex-worker-profile-default-a01-worker-crit.json
.orchestration/validation/dotfiles-T101-codex-worker-profile-default-a01-worker-review-receipt.md
.orchestration/validation/dotfiles-T101-codex-worker-profile-default-a01.md
.orchestration/validation/dotfiles-T102-add-worker-credential-notice-a01-audit-015929c.md
.orchestration/validation/dotfiles-T102-add-worker-credential-notice-a01-audit-015929c.md.last.md
.orchestration/validation/dotfiles-T102-add-worker-credential-notice-a01-crit.json
.orchestration/validation/dotfiles-T102-add-worker-credential-notice-a01-pr-feedback.json
.orchestration/validation/dotfiles-T102-add-worker-credential-notice-a01-review-receipt.md
.orchestration/validation/dotfiles-T102-add-worker-credential-notice-a01-worker-crit.json
.orchestration/validation/dotfiles-T102-add-worker-credential-notice-a01-worker-review-receipt.md
.orchestration/validation/dotfiles-T102-add-worker-credential-notice-a01.md
.orchestration/validation/dotfiles-T103-gh-auth-stores-a01-audit-0a28eb7.md
.orchestration/validation/dotfiles-T103-gh-auth-stores-a01-audit-0a28eb7.md.last.md
.orchestration/validation/dotfiles-T103-gh-auth-stores-a01-audit-a41a56b.md
.orchestration/validation/dotfiles-T103-gh-auth-stores-a01-audit-a41a56b.md.last.md
.orchestration/validation/dotfiles-T103-gh-auth-stores-a01-audit-c4fa1c1.md
.orchestration/validation/dotfiles-T103-gh-auth-stores-a01-audit-c4fa1c1.md.last.md
.orchestration/validation/dotfiles-T103-gh-auth-stores-a01-crit.json
.orchestration/validation/dotfiles-T103-gh-auth-stores-a01-pr-feedback.json
.orchestration/validation/dotfiles-T103-gh-auth-stores-a01-review-receipt.md
.orchestration/validation/dotfiles-T103-gh-auth-stores-a01-worker-crit.json
.orchestration/validation/dotfiles-T103-gh-auth-stores-a01-worker-review-receipt.md
.orchestration/validation/dotfiles-T103-gh-auth-stores-a01.md
.orchestration/validation/dotfiles-T104-pins-2026-10-06-a01-audit-bd0327a.md
.orchestration/validation/dotfiles-T104-pins-2026-10-06-a01-audit-bd0327a.md.last.md
.orchestration/validation/dotfiles-T104-pins-2026-10-06-a01-crit.json
.orchestration/validation/dotfiles-T104-pins-2026-10-06-a01-pr-feedback.json
.orchestration/validation/dotfiles-T104-pins-2026-10-06-a01-review-receipt.md
.orchestration/validation/dotfiles-T104-pins-2026-10-06-a01-worker-crit.json
.orchestration/validation/dotfiles-T104-pins-2026-10-06-a01-worker-review-receipt.md
.orchestration/validation/dotfiles-T104-pins-2026-10-06-a01.md
.orchestration/validation/dotfiles-T108-one-login-per-machine-a01-audit-b66f429.md
.orchestration/validation/dotfiles-T108-one-login-per-machine-a01-audit-b66f429.md.last.md
.orchestration/validation/dotfiles-T108-one-login-per-machine-a01-audit-f0a5407.md
.orchestration/validation/dotfiles-T108-one-login-per-machine-a01-audit-f0a5407.md.last.md
.orchestration/validation/dotfiles-T108-one-login-per-machine-a01-crit.json
.orchestration/validation/dotfiles-T108-one-login-per-machine-a01-pr-feedback.json
.orchestration/validation/dotfiles-T108-one-login-per-machine-a01-review-receipt.md
.orchestration/validation/dotfiles-T108-one-login-per-machine-a01-worker-crit.json
.orchestration/validation/dotfiles-T108-one-login-per-machine-a01-worker-review-receipt.md
.orchestration/validation/dotfiles-T108-one-login-per-machine-a01.md
.orchestration/validation/dotfiles-T109-claude-worker-merge-deny-a01-audit-c856e51.md
.orchestration/validation/dotfiles-T109-claude-worker-merge-deny-a01-audit-c856e51.md.last.md
.orchestration/validation/dotfiles-T109-claude-worker-merge-deny-a01-crit.json
.orchestration/validation/dotfiles-T109-claude-worker-merge-deny-a01-pr-feedback.json
.orchestration/validation/dotfiles-T109-claude-worker-merge-deny-a01-review-receipt.md
.orchestration/validation/dotfiles-T109-claude-worker-merge-deny-a01-worker-crit.json
.orchestration/validation/dotfiles-T109-claude-worker-merge-deny-a01-worker-review-receipt.md
.orchestration/validation/dotfiles-T109-claude-worker-merge-deny-a01.md
.orchestration/validation/dotfiles-T110-gh-auth-file-storage-a01-audit-1d4d2e4.md
.orchestration/validation/dotfiles-T110-gh-auth-file-storage-a01-audit-1d4d2e4.md.last.md
.orchestration/validation/dotfiles-T110-gh-auth-file-storage-a01-audit-449fa66.md
.orchestration/validation/dotfiles-T110-gh-auth-file-storage-a01-audit-449fa66.md.last.md
.orchestration/validation/dotfiles-T110-gh-auth-file-storage-a01-audit-80cc3e3.md
.orchestration/validation/dotfiles-T110-gh-auth-file-storage-a01-audit-80cc3e3.md.last.md
.orchestration/validation/dotfiles-T110-gh-auth-file-storage-a01-audit-a431fd4.md
.orchestration/validation/dotfiles-T110-gh-auth-file-storage-a01-audit-a431fd4.md.last.md
.orchestration/validation/dotfiles-T110-gh-auth-file-storage-a01-crit.json
.orchestration/validation/dotfiles-T110-gh-auth-file-storage-a01-pr-feedback.json
.orchestration/validation/dotfiles-T110-gh-auth-file-storage-a01-review-receipt.md
.orchestration/validation/dotfiles-T110-gh-auth-file-storage-a01-worker-crit.json
.orchestration/validation/dotfiles-T110-gh-auth-file-storage-a01-worker-review-receipt.md
.orchestration/validation/dotfiles-T110-gh-auth-file-storage-a01.md
.orchestration/validation/dotfiles-T111-project-map-subagent-a01-audit-0c1d280.md
.orchestration/validation/dotfiles-T111-project-map-subagent-a01-audit-0c1d280.md.last.md
.orchestration/validation/dotfiles-T111-project-map-subagent-a01-audit-2e15d4a.md
.orchestration/validation/dotfiles-T111-project-map-subagent-a01-audit-2e15d4a.md.last.md
.orchestration/validation/dotfiles-T111-project-map-subagent-a01-audit-32e7742.md
.orchestration/validation/dotfiles-T111-project-map-subagent-a01-audit-32e7742.md.last.md
.orchestration/validation/dotfiles-T111-project-map-subagent-a01-crit.json
.orchestration/validation/dotfiles-T111-project-map-subagent-a01-pr-feedback.json
.orchestration/validation/dotfiles-T111-project-map-subagent-a01-review-receipt.md
.orchestration/validation/dotfiles-T111-project-map-subagent-a01-worker-crit.json
.orchestration/validation/dotfiles-T111-project-map-subagent-a01-worker-review-receipt.md
.orchestration/validation/dotfiles-T111-project-map-subagent-a01.md
.orchestration/validation/dotfiles-T112-pins-2026-10-07-a01-audit-f678999.md
.orchestration/validation/dotfiles-T112-pins-2026-10-07-a01-audit-f678999.md.last.md
.orchestration/validation/dotfiles-T112-pins-2026-10-07-a01-crit.json
.orchestration/validation/dotfiles-T112-pins-2026-10-07-a01-pins.patch
.orchestration/validation/dotfiles-T112-pins-2026-10-07-a01-pr-feedback.json
.orchestration/validation/dotfiles-T112-pins-2026-10-07-a01-review-receipt.md
.orchestration/validation/dotfiles-T112-pins-2026-10-07-a01-worker-crit.json
.orchestration/validation/dotfiles-T112-pins-2026-10-07-a01-worker-review-receipt.md
.orchestration/validation/dotfiles-T112-pins-2026-10-07-a01.md
.orchestration/validation/dotfiles-T113-codify-T111-lessons-a01-audit-9311c6c.md
.orchestration/validation/dotfiles-T113-codify-T111-lessons-a01-audit-9311c6c.md.last.md
.orchestration/validation/dotfiles-T113-codify-T111-lessons-a01-audit-d0fa723.md
.orchestration/validation/dotfiles-T113-codify-T111-lessons-a01-audit-d0fa723.md.last.md
.orchestration/validation/dotfiles-T113-codify-T111-lessons-a01-crit.json
.orchestration/validation/dotfiles-T113-codify-T111-lessons-a01-pr-feedback.json
.orchestration/validation/dotfiles-T113-codify-T111-lessons-a01-review-receipt.md
.orchestration/validation/dotfiles-T113-codify-T111-lessons-a01-worker-crit.json
.orchestration/validation/dotfiles-T113-codify-T111-lessons-a01-worker-review-receipt.md
.orchestration/validation/dotfiles-T113-codify-T111-lessons-a01.md
.orchestration/validation/dotfiles-T114-canonical-clone-reconcile-a01-audit-0003cbd.md
.orchestration/validation/dotfiles-T114-canonical-clone-reconcile-a01-audit-0003cbd.md.last.md
.orchestration/validation/dotfiles-T114-canonical-clone-reconcile-a01-audit-0f0f2cb.md
.orchestration/validation/dotfiles-T114-canonical-clone-reconcile-a01-audit-0f0f2cb.md.last.md
.orchestration/validation/dotfiles-T114-canonical-clone-reconcile-a01-audit-46a229c.md
.orchestration/validation/dotfiles-T114-canonical-clone-reconcile-a01-audit-46a229c.md.last.md
.orchestration/validation/dotfiles-T114-canonical-clone-reconcile-a01-crit.json
.orchestration/validation/dotfiles-T114-canonical-clone-reconcile-a01-pr-feedback.json
.orchestration/validation/dotfiles-T114-canonical-clone-reconcile-a01-review-receipt.md
.orchestration/validation/dotfiles-T114-canonical-clone-reconcile-a01-worker-crit.json
.orchestration/validation/dotfiles-T114-canonical-clone-reconcile-a01-worker-review-receipt.md
.orchestration/validation/dotfiles-T114-canonical-clone-reconcile-a01.md
.orchestration/validation/dotfiles-T115-worker-audit-xhigh-a01-audit-282c5e8.md
.orchestration/validation/dotfiles-T115-worker-audit-xhigh-a01-audit-282c5e8.md.last.md
.orchestration/validation/dotfiles-T115-worker-audit-xhigh-a01-crit.json
.orchestration/validation/dotfiles-T115-worker-audit-xhigh-a01-pr-feedback.json
.orchestration/validation/dotfiles-T115-worker-audit-xhigh-a01-review-receipt.md
.orchestration/validation/dotfiles-T115-worker-audit-xhigh-a01-worker-crit.json
.orchestration/validation/dotfiles-T115-worker-audit-xhigh-a01-worker-review-receipt.md
.orchestration/validation/dotfiles-T115-worker-audit-xhigh-a01.md
.orchestration/validation/dotfiles-T116-on-demand-workers-a01-audit-ff4ffa0.md
.orchestration/validation/dotfiles-T116-on-demand-workers-a01-audit-ff4ffa0.md.last.md
.orchestration/validation/dotfiles-T116-on-demand-workers-a01-crit.json
.orchestration/validation/dotfiles-T116-on-demand-workers-a01-pr-feedback.json
.orchestration/validation/dotfiles-T116-on-demand-workers-a01-review-receipt.md
.orchestration/validation/dotfiles-T116-on-demand-workers-a01-worker-crit.json
.orchestration/validation/dotfiles-T116-on-demand-workers-a01-worker-review-receipt.md
.orchestration/validation/dotfiles-T116-on-demand-workers-a01.md
.orchestration/validation/dotfiles-T117-upgrade-outside-canonical-clone-a01-audit-bdd01aa.md
.orchestration/validation/dotfiles-T117-upgrade-outside-canonical-clone-a01-audit-bdd01aa.md.last.md
.orchestration/validation/dotfiles-T117-upgrade-outside-canonical-clone-a01-crit.json
.orchestration/validation/dotfiles-T117-upgrade-outside-canonical-clone-a01-pr-feedback.json
.orchestration/validation/dotfiles-T117-upgrade-outside-canonical-clone-a01-review-receipt.md
.orchestration/validation/dotfiles-T117-upgrade-outside-canonical-clone-a01-worker-crit.json
.orchestration/validation/dotfiles-T117-upgrade-outside-canonical-clone-a01-worker-review-receipt.md
.orchestration/validation/dotfiles-T117-upgrade-outside-canonical-clone-a01.md
.orchestration/validation/dotfiles-T118-rolling-tools-single-update-a01-audit-408727c.md
.orchestration/validation/dotfiles-T118-rolling-tools-single-update-a01-audit-408727c.md.last.md
.orchestration/validation/dotfiles-T118-rolling-tools-single-update-a01-audit-5d991b4.md
.orchestration/validation/dotfiles-T118-rolling-tools-single-update-a01-audit-5d991b4.md.last.md
.orchestration/validation/dotfiles-T118-rolling-tools-single-update-a01-audit-61c38cd.md
.orchestration/validation/dotfiles-T118-rolling-tools-single-update-a01-audit-61c38cd.md.last.md
.orchestration/validation/dotfiles-T118-rolling-tools-single-update-a01-audit-88e369d.md
.orchestration/validation/dotfiles-T118-rolling-tools-single-update-a01-audit-88e369d.md.last.md
.orchestration/validation/dotfiles-T118-rolling-tools-single-update-a01-audit-9a7a6ca.md
.orchestration/validation/dotfiles-T118-rolling-tools-single-update-a01-audit-9a7a6ca.md.last.md
.orchestration/validation/dotfiles-T118-rolling-tools-single-update-a01-audit-a9eb7f0.md
.orchestration/validation/dotfiles-T118-rolling-tools-single-update-a01-audit-a9eb7f0.md.last.md
.orchestration/validation/dotfiles-T118-rolling-tools-single-update-a01-audit-b6e27bd.md
.orchestration/validation/dotfiles-T118-rolling-tools-single-update-a01-audit-b6e27bd.md.last.md
.orchestration/validation/dotfiles-T118-rolling-tools-single-update-a01-audit-eee788f.md
.orchestration/validation/dotfiles-T118-rolling-tools-single-update-a01-audit-eee788f.md.last.md
.orchestration/validation/dotfiles-T118-rolling-tools-single-update-a01-crit.json
.orchestration/validation/dotfiles-T118-rolling-tools-single-update-a01-pr-feedback.json
.orchestration/validation/dotfiles-T118-rolling-tools-single-update-a01-review-receipt.md
.orchestration/validation/dotfiles-T118-rolling-tools-single-update-a01-worker-crit.json
.orchestration/validation/dotfiles-T118-rolling-tools-single-update-a01-worker-review-receipt.md
.orchestration/validation/dotfiles-T118-rolling-tools-single-update-a01.md
.orchestration/validation/dotfiles-T119-rolling-release-assets-a01-audit-0d264db.md
.orchestration/validation/dotfiles-T119-rolling-release-assets-a01-audit-0d264db.md.last.md
.orchestration/validation/dotfiles-T119-rolling-release-assets-a01-audit-36d87f6.md
.orchestration/validation/dotfiles-T119-rolling-release-assets-a01-audit-36d87f6.md.last.md
.orchestration/validation/dotfiles-T119-rolling-release-assets-a01-audit-674aaac.md
.orchestration/validation/dotfiles-T119-rolling-release-assets-a01-audit-674aaac.md.last.md
.orchestration/validation/dotfiles-T119-rolling-release-assets-a01-audit-73034ae.md
.orchestration/validation/dotfiles-T119-rolling-release-assets-a01-audit-73034ae.md.last.md
.orchestration/validation/dotfiles-T119-rolling-release-assets-a01-crit.json
.orchestration/validation/dotfiles-T119-rolling-release-assets-a01-pr-feedback.json
.orchestration/validation/dotfiles-T119-rolling-release-assets-a01-review-receipt.md
.orchestration/validation/dotfiles-T119-rolling-release-assets-a01-worker-crit.json
.orchestration/validation/dotfiles-T119-rolling-release-assets-a01-worker-review-receipt.md
.orchestration/validation/dotfiles-T119-rolling-release-assets-a01.md
.orchestration/validation/dotfiles-T120-npm-provenance-and-claude-channel-a01-worker-crit.json
.orchestration/validation/dotfiles-T121-claude-hook-install-hint-a01-worker-crit.json
.orchestration/validation/dotfiles-T121-claude-hook-install-hint-a01-worker-review-receipt.md
.orchestration/validation/dotfiles-T121-claude-hook-install-hint-a01.md
.orchestration/validation/dotfiles-T124-design-gate-and-reset-rule-a01-design-review-addendum-redesign-seat.md
.orchestration/validation/dotfiles-T124-design-gate-and-reset-rule-a01-design-review-canonical.md
.orchestration/validation/dotfiles-T124-design-gate-and-reset-rule-a01-design-review-round2.md
.orchestration/validation/dotfiles-T124-design-gate-and-reset-rule-a01-design-review-round3.md
.orchestration/validation/dotfiles-T124-design-gate-and-reset-rule-a01-design-review.md
.orchestration/validation/dotfiles-T124-wave1-task-validator-a01-worker-crit.json
.orchestration/validation/dotfiles-T124-wave1-task-validator-a01-worker-review-receipt.md
.orchestration/validation/dotfiles-T124-wave1-task-validator-a01.md
.orchestration/validation/dotfiles-T124-wave3b-audit-grammar-a01.md
.orchestration/validation/dotfiles-T126-regime-v2-a01-design-review-round2.md
.orchestration/validation/dotfiles-T126-regime-v2-a01-design-review-round3.md
.orchestration/validation/dotfiles-T126-regime-v2-a01-design-review-round4.md
.orchestration/validation/dotfiles-T126-regime-v2-a01-design-review.md
.orchestration/validation/dotfiles-T128-audit-s1-report-review-a01-codex-r1.md
.orchestration/validation/dotfiles-T128-audit-s1-report-review-a01-codex-r2.md
.orchestration/validation/dotfiles-T128-audit-s1-report-review-a01-codex-r3.md
.orchestration/validation/dotfiles-T128-audit-s1-report-review-a01-codex-r4.md
.orchestration/validation/dotfiles-T128-audit-s1-report-review-a01-codex-r5.md
.orchestration/validation/dotfiles-T128-audit-s1-report-review-a01-codex-r6.md
.orchestration/validation/dotfiles-T128-audit-s1-report-review-a01-codex-r7.md
.orchestration/validation/dotfiles-T128-audit-s1-report-review-a01-codex-r8.md
.orchestration/validation/dotfiles-T128-audit-s1-report-review-a01.md
.orchestration/validation/dotfiles-T128-aws-cli-macos-a01-audit-86212a4.md
.orchestration/validation/dotfiles-T128-aws-cli-macos-a01-audit-86212a4.md.last.md
.orchestration/validation/dotfiles-T128-aws-cli-macos-a01-crit.json
.orchestration/validation/dotfiles-T128-aws-cli-macos-a01-local-review-86212a4.md
.orchestration/validation/dotfiles-T128-aws-cli-macos-a01-pr-feedback.json
.orchestration/validation/dotfiles-T128-aws-cli-macos-a01-review-receipt.md
.orchestration/validation/dotfiles-T128-aws-cli-macos-a01.md
.orchestration/validation/dotfiles-T128-aws-cli-macos-review-a01-codex-r1.md
.orchestration/validation/dotfiles-T128-aws-cli-macos-review-a01-codex-r2.md
.orchestration/validation/dotfiles-T128-aws-cli-macos-review-a01-codex-r3.md
.orchestration/validation/dotfiles-T128-aws-cli-macos-review-a01.md
.orchestration/validation/dotfiles-T128-chain-github-scripts-a01-audit-d15fa87.md
.orchestration/validation/dotfiles-T128-chain-github-scripts-a01-audit-d15fa87.md.last.md
.orchestration/validation/dotfiles-T128-chain-github-scripts-a01-crit.json
.orchestration/validation/dotfiles-T128-chain-github-scripts-a01-local-review-d15fa87.md
.orchestration/validation/dotfiles-T128-chain-github-scripts-a01-pr-feedback.json
.orchestration/validation/dotfiles-T128-chain-github-scripts-a01-review-a01.md
.orchestration/validation/dotfiles-T128-chain-github-scripts-a01-review-receipt.md
.orchestration/validation/dotfiles-T128-chain-github-scripts-a01.md
.orchestration/validation/dotfiles-T128-chain-github-scripts-followup-a01-audit-e9404a6.md
.orchestration/validation/dotfiles-T128-chain-github-scripts-followup-a01-audit-e9404a6.md.last.md
.orchestration/validation/dotfiles-T128-chain-github-scripts-followup-a01-crit.json
.orchestration/validation/dotfiles-T128-chain-github-scripts-followup-a01-local-review-e9404a6.md
.orchestration/validation/dotfiles-T128-chain-github-scripts-followup-a01-pr-feedback.json
.orchestration/validation/dotfiles-T128-chain-github-scripts-followup-a01-review-a01.md
.orchestration/validation/dotfiles-T128-chain-github-scripts-followup-a01-review-receipt.md
.orchestration/validation/dotfiles-T128-chain-github-scripts-followup-a01.md
.orchestration/validation/dotfiles-T128-chain-github-scripts-followup-a02-audit-2c8acdb.md
.orchestration/validation/dotfiles-T128-chain-github-scripts-followup-a02-audit-2c8acdb.md.last.md
.orchestration/validation/dotfiles-T128-chain-github-scripts-followup-a02-audit-59eca2a.md
.orchestration/validation/dotfiles-T128-chain-github-scripts-followup-a02-audit-59eca2a.md.last.md
.orchestration/validation/dotfiles-T128-chain-github-scripts-followup-a02-audit-5ef1c90.md
.orchestration/validation/dotfiles-T128-chain-github-scripts-followup-a02-audit-5ef1c90.md.last.md
.orchestration/validation/dotfiles-T128-chain-github-scripts-followup-a02-crit.json
.orchestration/validation/dotfiles-T128-chain-github-scripts-followup-a02-local-review-157d8f3.md
.orchestration/validation/dotfiles-T128-chain-github-scripts-followup-a02-local-review-2c8acdb.md
.orchestration/validation/dotfiles-T128-chain-github-scripts-followup-a02-local-review-59eca2a.md
.orchestration/validation/dotfiles-T128-chain-github-scripts-followup-a02-local-review-5ef1c90.md
.orchestration/validation/dotfiles-T128-chain-github-scripts-followup-a02-pr-feedback.json
.orchestration/validation/dotfiles-T128-chain-github-scripts-followup-a02-review-a01-codex-r1.md
.orchestration/validation/dotfiles-T128-chain-github-scripts-followup-a02-review-a01-codex-r2.md
.orchestration/validation/dotfiles-T128-chain-github-scripts-followup-a02-review-a01-codex-r3.md
.orchestration/validation/dotfiles-T128-chain-github-scripts-followup-a02-review-a01-codex-r4.md
.orchestration/validation/dotfiles-T128-chain-github-scripts-followup-a02-review-a01-codex-r5.md
.orchestration/validation/dotfiles-T128-chain-github-scripts-followup-a02-review-a01-codex-r6.md
.orchestration/validation/dotfiles-T128-chain-github-scripts-followup-a02-review-a01-codex-r7.md
.orchestration/validation/dotfiles-T128-chain-github-scripts-followup-a02-review-a01.md
.orchestration/validation/dotfiles-T128-chain-github-scripts-followup-a02-review-receipt.md
.orchestration/validation/dotfiles-T128-chain-github-scripts-followup-review-a01-codex-r1.md
.orchestration/validation/dotfiles-T128-chain-github-scripts-followup-review-a01-codex-r2.md
.orchestration/validation/dotfiles-T128-chain-github-scripts-review-a01-codex-r1.md
.orchestration/validation/dotfiles-T128-chain-github-scripts-review-a01-codex-r2.md
.orchestration/validation/dotfiles-T128-chain-github-scripts-review-a01-codex-r3.md
.orchestration/validation/dotfiles-T128-chain-github-scripts-review-a01-codex-r4.md
.orchestration/validation/dotfiles-T128-chain-glue-finish-a01-local-review-9c01191.md
.orchestration/validation/dotfiles-T128-chain-glue-finish-a01-local-review-f20826e.md
.orchestration/validation/dotfiles-T128-chain-glue-finish-a01-local-review-f4d86ee.md
.orchestration/validation/dotfiles-T128-chain-glue-finish-a01-pr-feedback.json
.orchestration/validation/dotfiles-T128-chain-glue-finish-review-a01-codex-r1.md
.orchestration/validation/dotfiles-T128-chain-glue-finish-review-a01-codex-r2.md
.orchestration/validation/dotfiles-T128-chain-glue-finish-review-a01-codex-r3.md
.orchestration/validation/dotfiles-T128-chain-glue-finish-review-a01-codex-r4.md
.orchestration/validation/dotfiles-T128-chain-glue-finish-review-a01-codex-r5.md
.orchestration/validation/dotfiles-T128-chain-glue-finish-review-a01-codex-r6.md
.orchestration/validation/dotfiles-T128-chain-glue-finish-review-a01.md
.orchestration/validation/dotfiles-T128-chain-glue-integrate-a01-audit-23d9af3.md
.orchestration/validation/dotfiles-T128-chain-glue-integrate-a01-audit-23d9af3.md.last.md
.orchestration/validation/dotfiles-T128-chain-glue-integrate-a01-crit.json
.orchestration/validation/dotfiles-T128-chain-glue-integrate-a01-local-review-23d9af3.md
.orchestration/validation/dotfiles-T128-chain-glue-integrate-a01-local-review-2fe135c.md
.orchestration/validation/dotfiles-T128-chain-glue-integrate-a01-local-review-6e4e9aa.md
.orchestration/validation/dotfiles-T128-chain-glue-integrate-a01-pr-feedback.json
.orchestration/validation/dotfiles-T128-chain-glue-integrate-a01-review-receipt.md
.orchestration/validation/dotfiles-T128-chain-glue-integrate-review-a01-codex-r1.md
.orchestration/validation/dotfiles-T128-chain-glue-integrate-review-a01-codex-r11.md
.orchestration/validation/dotfiles-T128-chain-glue-integrate-review-a01-codex-r12.md
.orchestration/validation/dotfiles-T128-chain-glue-integrate-review-a01-codex-r2.md
.orchestration/validation/dotfiles-T128-chain-glue-integrate-review-a01-codex-r3.md
.orchestration/validation/dotfiles-T128-chain-glue-integrate-review-a01-codex-r4.md
.orchestration/validation/dotfiles-T128-chain-glue-integrate-review-a01-codex-r5.md
.orchestration/validation/dotfiles-T128-chain-glue-integrate-review-a01-codex-r6.md
.orchestration/validation/dotfiles-T128-chain-glue-integrate-review-a01-codex-r7.md
.orchestration/validation/dotfiles-T128-chain-glue-integrate-review-a01-codex-r8.md
.orchestration/validation/dotfiles-T128-chain-glue-integrate-review-a01-codex-r9.md
.orchestration/validation/dotfiles-T128-chain-glue-integrate-review-a01.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-a01-amend-review-a01-codex-r1.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-a01-amend-review-a01-codex-r2.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-a01-amend-review-a01.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-a01-audit-b6ce4ff.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-a01-audit-b6ce4ff.md.last.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-a01-crit.json
.orchestration/validation/dotfiles-T128-chain-review-scripts-a01-local-review-b6ce4ff.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-a01-pr-feedback.json
.orchestration/validation/dotfiles-T128-chain-review-scripts-a01-pre-amend1.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-a01-review-a01.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-a01-review-receipt.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a01-audit-2e3ff49.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a01-audit-2e3ff49.md.last.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a01-audit-40f3be4.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a01-audit-40f3be4.md.last.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a01-audit-ba451c6.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a01-audit-ba451c6.md.last.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a01-audit-c45f9b5.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a01-audit-c45f9b5.md.last.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a01-crit.json
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a01-local-review-2e3ff49.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a01-local-review-40f3be4.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a01-local-review-850fc54.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a01-local-review-b879aac.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a01-local-review-ba451c6.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a01-local-review-c45f9b5.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a01-pr-feedback.json
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a01-review-a01.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a01-review-receipt.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a01.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a02-audit-8afc458.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a02-audit-8afc458.md.last.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a02-crit.json
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a02-local-review-8afc458.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a02-pr-feedback.json
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a02-review-a01-codex-r1.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a02-review-a01-codex-r2.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a02-review-a01-codex-r3.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a02-review-a01-codex-r4.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a02-review-a01.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a02-review-receipt.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a02.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a03-audit-d3e8acf.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a03-audit-d3e8acf.md.last.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a03-crit.json
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a03-local-review-d3e8acf.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a03-pr-feedback.json
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a03-review-receipt.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a04-audit-000c5c6.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a04-audit-000c5c6.md.last.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a04-crit.json
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a04-local-review-000c5c6.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a04-local-review-a588a98.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a04-pr-feedback.json
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a04-review-a01-codex-r1.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a04-review-a01-codex-r2.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a04-review-a01-codex-r3.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a04-review-a01-codex-r4.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a04-review-a01.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a04-review-receipt.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-review-a01-codex-r1.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-review-a01-codex-r2.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-review-a03-codex-r1.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-review-a03-codex-r2.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-review-a03-codex-r3.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-review-a03.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-review-a01-codex-r1.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-review-a01-codex-r2.md
.orchestration/validation/dotfiles-T128-chain-review-scripts-review-a01-codex-r3.md
.orchestration/validation/dotfiles-T128-ci-skip-orchestration-a01-audit-d634349.md
.orchestration/validation/dotfiles-T128-ci-skip-orchestration-a01-audit-d634349.md.last.md
.orchestration/validation/dotfiles-T128-ci-skip-orchestration-a01-audit-dc4e6c3.md
.orchestration/validation/dotfiles-T128-ci-skip-orchestration-a01-audit-dc4e6c3.md.last.md
.orchestration/validation/dotfiles-T128-ci-skip-orchestration-a01-crit.json
.orchestration/validation/dotfiles-T128-ci-skip-orchestration-a01-pr-feedback.json
.orchestration/validation/dotfiles-T128-ci-skip-orchestration-a01-review-receipt.md
.orchestration/validation/dotfiles-T128-ci-skip-orchestration-a01.md
.orchestration/validation/dotfiles-T128-ci-skip-orchestration-a02-audit-3bafe4f.md
.orchestration/validation/dotfiles-T128-ci-skip-orchestration-a02-audit-3bafe4f.md.last.md
.orchestration/validation/dotfiles-T128-ci-skip-orchestration-a02-crit.json
.orchestration/validation/dotfiles-T128-ci-skip-orchestration-a02-pr-feedback.json
.orchestration/validation/dotfiles-T128-ci-skip-orchestration-a02-review-receipt.md
.orchestration/validation/dotfiles-T128-ci-skip-orchestration-a02.md
.orchestration/validation/dotfiles-T128-ci-skip-redesign-a01.md
.orchestration/validation/dotfiles-T128-followup-owners-review-a01-codex-r2.md
.orchestration/validation/dotfiles-T128-followup-owners-review-a01-codex-r3.md
.orchestration/validation/dotfiles-T128-followup-owners-review-a01-codex-r4.md
.orchestration/validation/dotfiles-T128-followup-owners-review-a01-codex.md
.orchestration/validation/dotfiles-T128-followup-owners-review-a01.md
.orchestration/validation/dotfiles-T128-gate-evidence-a02-amend-review-a01-codex.md
.orchestration/validation/dotfiles-T128-gate-evidence-a02-amend-review-a01.md
.orchestration/validation/dotfiles-T128-gate-evidence-a02.md
.orchestration/validation/dotfiles-T128-gate-evidence-a03-amend-review-a01-codex-r2.md
.orchestration/validation/dotfiles-T128-gate-evidence-a03-amend-review-a01-codex-r3.md
.orchestration/validation/dotfiles-T128-gate-evidence-a03-amend-review-a01-codex-r4.md
.orchestration/validation/dotfiles-T128-gate-evidence-a03-amend-review-a01-codex-r5.md
.orchestration/validation/dotfiles-T128-gate-evidence-a03-amend-review-a01-codex.md
.orchestration/validation/dotfiles-T128-gate-evidence-a03-amend-review-a01.md
.orchestration/validation/dotfiles-T128-gate-evidence-a03.md
.orchestration/validation/dotfiles-T128-gate-evidence-a04-amend-review-a01-codex.md
.orchestration/validation/dotfiles-T128-gate-evidence-a04-amend-review-a01.md
.orchestration/validation/dotfiles-T128-gate-evidence-a04-audit-20d776d.md
.orchestration/validation/dotfiles-T128-gate-evidence-a04-audit-20d776d.md.last.md
.orchestration/validation/dotfiles-T128-gate-evidence-a04-audit-2231a4f.md
.orchestration/validation/dotfiles-T128-gate-evidence-a04-audit-2231a4f.md.last.md
.orchestration/validation/dotfiles-T128-gate-evidence-a04-audit-60d152a.md
.orchestration/validation/dotfiles-T128-gate-evidence-a04-audit-60d152a.md.last.md
.orchestration/validation/dotfiles-T128-gate-evidence-a04-audit-71eb920.md
.orchestration/validation/dotfiles-T128-gate-evidence-a04-audit-71eb920.md.last.md
.orchestration/validation/dotfiles-T128-gate-evidence-a04-crit.json
.orchestration/validation/dotfiles-T128-gate-evidence-a04-local-review-71eb920.md
.orchestration/validation/dotfiles-T128-gate-evidence-a04-pr-feedback.json
.orchestration/validation/dotfiles-T128-gate-evidence-a04-review-receipt.md
.orchestration/validation/dotfiles-T128-gate-evidence-a04.md
.orchestration/validation/dotfiles-T128-gate-evidence-redesign-a01.md
.orchestration/validation/dotfiles-T128-gate-evidence-redesign-a02.md
.orchestration/validation/dotfiles-T128-gate-evidence-redesign-a03-codex-r2.md
.orchestration/validation/dotfiles-T128-gate-evidence-redesign-a03-codex-r3.md
.orchestration/validation/dotfiles-T128-gate-evidence-redesign-a03-codex-r4.md
.orchestration/validation/dotfiles-T128-gate-evidence-redesign-a03-codex.md
.orchestration/validation/dotfiles-T128-gate-evidence-redesign-a03.md
.orchestration/validation/dotfiles-T128-gate-wrapper-path-a01-audit-a235637.md
.orchestration/validation/dotfiles-T128-gate-wrapper-path-a01-audit-a235637.md.last.md
.orchestration/validation/dotfiles-T128-gate-wrapper-path-a01-crit.json
.orchestration/validation/dotfiles-T128-gate-wrapper-path-a01-local-review-a235637.md
.orchestration/validation/dotfiles-T128-gate-wrapper-path-a01-pr-feedback.json
.orchestration/validation/dotfiles-T128-gate-wrapper-path-a01-review-receipt.md
.orchestration/validation/dotfiles-T128-gate-wrapper-path-a01.md
.orchestration/validation/dotfiles-T128-gate-wrapper-path-review-a01-codex-r2.md
.orchestration/validation/dotfiles-T128-gate-wrapper-path-review-a01-codex-r3.md
.orchestration/validation/dotfiles-T128-gate-wrapper-path-review-a01-codex.md
.orchestration/validation/dotfiles-T128-gate-wrapper-path-review-a01.md
.orchestration/validation/dotfiles-T128-model-profiles-xhigh-a01-audit-429a6c5.md
.orchestration/validation/dotfiles-T128-model-profiles-xhigh-a01-audit-429a6c5.md.last.md
.orchestration/validation/dotfiles-T128-model-profiles-xhigh-a01-audit-707ed3a.md
.orchestration/validation/dotfiles-T128-model-profiles-xhigh-a01-audit-707ed3a.md.last.md
.orchestration/validation/dotfiles-T128-model-profiles-xhigh-a01-crit.json
.orchestration/validation/dotfiles-T128-model-profiles-xhigh-a01-local-review-429a6c5.md
.orchestration/validation/dotfiles-T128-model-profiles-xhigh-a01-local-review-707ed3a.md
.orchestration/validation/dotfiles-T128-model-profiles-xhigh-a01-pr-feedback.json
.orchestration/validation/dotfiles-T128-model-profiles-xhigh-a01-review-receipt.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-a01-amend-review-a01-codex-r2.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-a01-amend-review-a01-codex.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-a01-amend-review-a01.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-a01.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-a02-audit-7b574d3.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-a02-audit-7b574d3.md.last.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-a02-crit.json
.orchestration/validation/dotfiles-T128-orchestrator-tools-a02-local-review-7b574d3.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-a02-local-review-9ad0c15.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-a02-pr-feedback.json
.orchestration/validation/dotfiles-T128-orchestrator-tools-a02-review-receipt.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-a02.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-a03-amend-review-a01-codex.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-a03-amend-review-a01.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-a03-crit.json
.orchestration/validation/dotfiles-T128-orchestrator-tools-a03-local-review-0d19947.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-a03-pr-feedback.json
.orchestration/validation/dotfiles-T128-orchestrator-tools-a03-review-receipt.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-a03.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-a04-audit-3e5cad3.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-a04-audit-3e5cad3.md.last.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-a04-crit.json
.orchestration/validation/dotfiles-T128-orchestrator-tools-a04-local-review-3e5cad3.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-a04-local-review-5b99a74.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-a04-pr-feedback.json
.orchestration/validation/dotfiles-T128-orchestrator-tools-a04-review-receipt.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-a04.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-a05-amend-review-a01-codex-r2.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-a05-amend-review-a01-codex-r3.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-a05-amend-review-a01-codex.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-a05-amend-review-a01.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-a05-audit-046901b.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-a05-audit-046901b.md.last.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-a05-audit-8576645.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-a05-audit-8576645.md.last.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-a05-audit-a06c874.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-a05-audit-a06c874.md.last.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-a05-audit-f48593d.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-a05-audit-f48593d.md.last.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-a05-crit.json
.orchestration/validation/dotfiles-T128-orchestrator-tools-a05-local-review-046901b.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-a05-local-review-8576645.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-a05-local-review-a06c874.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-a05-local-review-f48593d.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-a05-pr-feedback.json
.orchestration/validation/dotfiles-T128-orchestrator-tools-a05-review-receipt.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-a05.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-a06-audit-6847aa9.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-a06-audit-6847aa9.md.last.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-a06-crit.json
.orchestration/validation/dotfiles-T128-orchestrator-tools-a06-local-review-6847aa9.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-a06-pr-feedback.json
.orchestration/validation/dotfiles-T128-orchestrator-tools-a06-review-receipt.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-a06-taskfile-review-codex-round1.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-a06-taskfile-review-codex-round2.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-a06-taskfile-review-codex-round3.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-a06.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a01-audit-2e77a33.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a01-audit-2e77a33.md.last.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a01-crit.json
.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a01-local-review-2e77a33.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a01-pr-feedback.json
.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a01-review-receipt.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a01.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a02-audit-7ef55f0.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a02-audit-7ef55f0.md.last.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a02-audit-cfebc1f.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a02-audit-cfebc1f.md.last.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a02-crit.json
.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a02-local-review-7ef55f0.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a02-local-review-cfebc1f.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a02-pr-feedback.json
.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a02-review-a01-codex-r1.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a02-review-a01-codex-r2.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a02-review-a01-codex-r3.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a02-review-a01.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a02-review-receipt.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a03-audit-ef74eae.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a03-audit-ef74eae.md.last.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a03-audit-f364b7d.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a03-audit-f364b7d.md.last.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a03-crit.json
.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a03-local-review-94c36f4.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a03-local-review-9df6b0c.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a03-local-review-ef74eae.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a03-local-review-f364b7d.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a03-pr-feedback.json
.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a03-review-receipt.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a03.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a04-review-a01-codex-r1.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a04-review-a01-codex-r2.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-review-a03-codex-r1.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-review-a03-codex-r10.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-review-a03-codex-r11.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-review-a03-codex-r12.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-review-a03-codex-r13.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-review-a03-codex-r2.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-review-a03-codex-r3.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-review-a03-codex-r4.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-review-a03-codex-r5.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-review-a03-codex-r6.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-review-a03-codex-r7.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-review-a03-codex-r8.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-review-a03-codex-r9.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-review-a03.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-redesign-a01-codex-r2.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-redesign-a01-codex.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-redesign-a01.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-redesign-a02-codex-r2.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-redesign-a02-codex-r4.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-redesign-a02-codex-r5.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-redesign-a02-codex.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-redesign-a02.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-redesign-a03-codex.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-redesign-a03.md
.orchestration/validation/dotfiles-T128-orchestrator-tools-redesign-a04.md
.orchestration/validation/dotfiles-T128-owner-tasks-refresh-review-a01-codex-r1.md
.orchestration/validation/dotfiles-T128-owner-tasks-refresh-review-a01-codex-r2.md
.orchestration/validation/dotfiles-T128-owner-tasks-refresh-review-a01.md
.orchestration/validation/dotfiles-T128-plan-007-review-a01-codex.md
.orchestration/validation/dotfiles-T128-plan-007-review-a01.md
.orchestration/validation/dotfiles-T128-playbook-rules-a02.md
.orchestration/validation/dotfiles-T128-playbook-rules-a03.md
.orchestration/validation/dotfiles-T128-playbook-rules-a04-amend-review-a01-codex-r2.md
.orchestration/validation/dotfiles-T128-playbook-rules-a04-amend-review-a01-codex.md
.orchestration/validation/dotfiles-T128-playbook-rules-a04-amend-review-a01.md
.orchestration/validation/dotfiles-T128-playbook-rules-a04-audit-65a3d71.md
.orchestration/validation/dotfiles-T128-playbook-rules-a04-audit-65a3d71.md.last.md
.orchestration/validation/dotfiles-T128-playbook-rules-a04-crit.json
.orchestration/validation/dotfiles-T128-playbook-rules-a04-local-review-65a3d71.md
.orchestration/validation/dotfiles-T128-playbook-rules-a04-local-review-7771082.md
.orchestration/validation/dotfiles-T128-playbook-rules-a04-pr-feedback.json
.orchestration/validation/dotfiles-T128-playbook-rules-a04-review-receipt.md
.orchestration/validation/dotfiles-T128-playbook-rules-a04.md
.orchestration/validation/dotfiles-T128-playbook-rules-followup-a01-amend-review-a01-codex-r1.md
.orchestration/validation/dotfiles-T128-playbook-rules-followup-a01-amend-review-a01.md
.orchestration/validation/dotfiles-T128-playbook-rules-followup-a01-audit-3a8f809.md
.orchestration/validation/dotfiles-T128-playbook-rules-followup-a01-audit-3a8f809.md.last.md
.orchestration/validation/dotfiles-T128-playbook-rules-followup-a01-crit.json
.orchestration/validation/dotfiles-T128-playbook-rules-followup-a01-local-review-3a8f809.md
.orchestration/validation/dotfiles-T128-playbook-rules-followup-a01-pr-feedback.json
.orchestration/validation/dotfiles-T128-playbook-rules-followup-a01-pre-amend1.md
.orchestration/validation/dotfiles-T128-playbook-rules-followup-a01-review-receipt.md
.orchestration/validation/dotfiles-T128-playbook-rules-redesign-a01.md
.orchestration/validation/dotfiles-T128-playbook-rules-redesign-a02.md
.orchestration/validation/dotfiles-T128-playbook-rules-redesign-a03.md
.orchestration/validation/dotfiles-T128-process-hardening-review-a01-codex-r1.md
.orchestration/validation/dotfiles-T128-process-hardening-review-a01-codex-r2.md
.orchestration/validation/dotfiles-T128-process-hardening-review-a02-codex-r1.md
.orchestration/validation/dotfiles-T128-process-hardening-review-a02-codex-r2.md
.orchestration/validation/dotfiles-T128-process-rules-a01-pr-feedback.json
.orchestration/validation/dotfiles-T128-process-rules-a01.md
.orchestration/validation/dotfiles-T128-process-rules-a02-audit-27ea99b.md
.orchestration/validation/dotfiles-T128-process-rules-a02-audit-27ea99b.md.last.md
.orchestration/validation/dotfiles-T128-process-rules-a02-crit.json
.orchestration/validation/dotfiles-T128-process-rules-a02-pr-feedback.json
.orchestration/validation/dotfiles-T128-process-rules-a02-review-receipt.md
.orchestration/validation/dotfiles-T128-process-rules-a02.md
.orchestration/validation/dotfiles-T128-process-rules-a03-audit-b7ae2d5.md
.orchestration/validation/dotfiles-T128-process-rules-a03-audit-b7ae2d5.md.last.md
.orchestration/validation/dotfiles-T128-process-rules-a03-crit.json
.orchestration/validation/dotfiles-T128-process-rules-a03-pr-feedback.json
.orchestration/validation/dotfiles-T128-process-rules-a03-review-receipt.md
.orchestration/validation/dotfiles-T128-process-rules-a03.md
.orchestration/validation/dotfiles-T128-process-rules-a04.md
.orchestration/validation/dotfiles-T128-process-rules-a05-audit-4af8939.md
.orchestration/validation/dotfiles-T128-process-rules-a05-audit-4af8939.md.last.md
.orchestration/validation/dotfiles-T128-process-rules-a05-pr-feedback.json
.orchestration/validation/dotfiles-T128-process-rules-a05-taskfile-review-codex-round1.md
.orchestration/validation/dotfiles-T128-process-rules-a05-taskfile-review-codex-round2.md
.orchestration/validation/dotfiles-T128-process-rules-a05-taskfile-review-codex-round3.md
.orchestration/validation/dotfiles-T128-process-rules-a05-taskfile-review-codex-round4.md
.orchestration/validation/dotfiles-T128-process-rules-a05.md
.orchestration/validation/dotfiles-T128-process-rules-a06.md
.orchestration/validation/dotfiles-T128-process-rules-a07-audit-92634b2.md
.orchestration/validation/dotfiles-T128-process-rules-a07-audit-92634b2.md.last.md
.orchestration/validation/dotfiles-T128-process-rules-a07-crit.json
.orchestration/validation/dotfiles-T128-process-rules-a07-pr-feedback.json
.orchestration/validation/dotfiles-T128-process-rules-a07-review-receipt.md
.orchestration/validation/dotfiles-T128-process-rules-a07.md
.orchestration/validation/dotfiles-T128-process-rules-redesign-a01.md
.orchestration/validation/dotfiles-T128-process-rules-redesign-a02.md
.orchestration/validation/dotfiles-T128-process-rules-redesign-a03.md
.orchestration/validation/dotfiles-T128-process-rules-redesign-a04.md
.orchestration/validation/dotfiles-T128-process-rules-redesign-a05.md
.orchestration/validation/dotfiles-T128-process-rules-redesign-a06.md
.orchestration/validation/dotfiles-T128-project-map-pane-open-a01-audit-73f51ab.md
.orchestration/validation/dotfiles-T128-project-map-pane-open-a01-audit-73f51ab.md.last.md
.orchestration/validation/dotfiles-T128-project-map-pane-open-a01-crit.json
.orchestration/validation/dotfiles-T128-project-map-pane-open-a01-followup-a01-audit-00048df.md
.orchestration/validation/dotfiles-T128-project-map-pane-open-a01-followup-a01-audit-00048df.md.last.md
.orchestration/validation/dotfiles-T128-project-map-pane-open-a01-followup-a01-audit-3288959.md
.orchestration/validation/dotfiles-T128-project-map-pane-open-a01-followup-a01-audit-3288959.md.last.md
.orchestration/validation/dotfiles-T128-project-map-pane-open-a01-followup-a01-audit-8607a87.md
.orchestration/validation/dotfiles-T128-project-map-pane-open-a01-followup-a01-audit-8607a87.md.last.md
.orchestration/validation/dotfiles-T128-project-map-pane-open-a01-followup-a01-audit-990b607.md
.orchestration/validation/dotfiles-T128-project-map-pane-open-a01-followup-a01-audit-990b607.md.last.md
.orchestration/validation/dotfiles-T128-project-map-pane-open-a01-followup-a01-crit.json
.orchestration/validation/dotfiles-T128-project-map-pane-open-a01-followup-a01-local-review-00048df.md
.orchestration/validation/dotfiles-T128-project-map-pane-open-a01-followup-a01-local-review-2842c34.md
.orchestration/validation/dotfiles-T128-project-map-pane-open-a01-followup-a01-local-review-3288959.md
.orchestration/validation/dotfiles-T128-project-map-pane-open-a01-followup-a01-local-review-8607a87.md
.orchestration/validation/dotfiles-T128-project-map-pane-open-a01-followup-a01-local-review-990b607.md
.orchestration/validation/dotfiles-T128-project-map-pane-open-a01-followup-a01-pr-feedback.json
.orchestration/validation/dotfiles-T128-project-map-pane-open-a01-followup-a01-pre-amend1.md
.orchestration/validation/dotfiles-T128-project-map-pane-open-a01-followup-a01-review-receipt.md
.orchestration/validation/dotfiles-T128-project-map-pane-open-a01-followup-review-a01-amend1-codex-r1.md
.orchestration/validation/dotfiles-T128-project-map-pane-open-a01-followup-review-a01-amend1-codex-r2.md
.orchestration/validation/dotfiles-T128-project-map-pane-open-a01-followup-review-a01-codex-r1.md
.orchestration/validation/dotfiles-T128-project-map-pane-open-a01-followup-review-a01-codex-r2.md
.orchestration/validation/dotfiles-T128-project-map-pane-open-a01-followup-review-a01-codex-r3.md
.orchestration/validation/dotfiles-T128-project-map-pane-open-a01-followup-review-a01.md
.orchestration/validation/dotfiles-T128-project-map-pane-open-a01-local-review-73f51ab.md
.orchestration/validation/dotfiles-T128-project-map-pane-open-a01-pr-feedback.json
.orchestration/validation/dotfiles-T128-project-map-pane-open-a01-review-a01.md
.orchestration/validation/dotfiles-T128-project-map-pane-open-a01-review-receipt.md
.orchestration/validation/dotfiles-T128-project-map-pane-open-a01.md
.orchestration/validation/dotfiles-T128-project-map-pane-open-review-a01-codex-r2.md
.orchestration/validation/dotfiles-T128-project-map-reload-hook-a01-amend-review-a01-codex.md
.orchestration/validation/dotfiles-T128-project-map-reload-hook-a01-amend-review-a01.md
.orchestration/validation/dotfiles-T128-project-map-reload-hook-a01-amend-review-a02-codex-r2.md
.orchestration/validation/dotfiles-T128-project-map-reload-hook-a01-amend-review-a02-codex-r3.md
.orchestration/validation/dotfiles-T128-project-map-reload-hook-a01-amend-review-a02-codex-r4.md
.orchestration/validation/dotfiles-T128-project-map-reload-hook-a01-amend-review-a02-codex-r5.md
.orchestration/validation/dotfiles-T128-project-map-reload-hook-a01-amend-review-a02-codex-r6.md
.orchestration/validation/dotfiles-T128-project-map-reload-hook-a01-amend-review-a02-codex-r7.md
.orchestration/validation/dotfiles-T128-project-map-reload-hook-a01-amend-review-a02-codex-r8.md
.orchestration/validation/dotfiles-T128-project-map-reload-hook-a01-amend-review-a02-codex.md
.orchestration/validation/dotfiles-T128-project-map-reload-hook-a01-amend-review-a02.md
.orchestration/validation/dotfiles-T128-project-map-reload-hook-a01-audit-2fb97db.md
.orchestration/validation/dotfiles-T128-project-map-reload-hook-a01-audit-2fb97db.md.last.md
.orchestration/validation/dotfiles-T128-project-map-reload-hook-a01-crit.json
.orchestration/validation/dotfiles-T128-project-map-reload-hook-a01-local-review-2fb97db.md
.orchestration/validation/dotfiles-T128-project-map-reload-hook-a01-pr-feedback.json
.orchestration/validation/dotfiles-T128-project-map-reload-hook-a01-pre-amend2.md
.orchestration/validation/dotfiles-T128-project-map-reload-hook-a01-review-receipt.md
.orchestration/validation/dotfiles-T128-project-map-reload-hook-a01.md
.orchestration/validation/dotfiles-T128-project-map-reload-hook-followup-a01-audit-7f4f3f1.md
.orchestration/validation/dotfiles-T128-project-map-reload-hook-followup-a01-audit-7f4f3f1.md.last.md
.orchestration/validation/dotfiles-T128-project-map-reload-hook-followup-a01-crit.json
.orchestration/validation/dotfiles-T128-project-map-reload-hook-followup-a01-local-review-7f4f3f1.md
.orchestration/validation/dotfiles-T128-project-map-reload-hook-followup-a01-pr-feedback.json
.orchestration/validation/dotfiles-T128-project-map-reload-hook-followup-a01-review-receipt.md
.orchestration/validation/dotfiles-T128-project-map-reload-hook-followup-a01.md
.orchestration/validation/dotfiles-T128-project-map-reload-hook-followup-review-a01-codex-r1.md
.orchestration/validation/dotfiles-T128-project-map-reload-hook-followup-review-a01-codex-r2.md
.orchestration/validation/dotfiles-T128-project-map-reload-hook-followup-review-a01.md
.orchestration/validation/dotfiles-T128-project-map-reload-hook-review-a01-codex-r2.md
.orchestration/validation/dotfiles-T128-project-map-reload-hook-review-a01-codex-r3.md
.orchestration/validation/dotfiles-T128-project-map-reload-hook-review-a01-codex.md
.orchestration/validation/dotfiles-T128-project-map-reload-hook-review-a01.md
.orchestration/validation/dotfiles-T128-regime-counters-a01-audit-72764f0.md
.orchestration/validation/dotfiles-T128-regime-counters-a01-audit-72764f0.md.last.md
.orchestration/validation/dotfiles-T128-regime-counters-a01-pr-feedback.json
.orchestration/validation/dotfiles-T128-regime-counters-a01.md
.orchestration/validation/dotfiles-T128-regime-counters-a02-audit-8ce912b.md
.orchestration/validation/dotfiles-T128-regime-counters-a02-audit-8ce912b.md.last.md
.orchestration/validation/dotfiles-T128-regime-counters-a02-crit.json
.orchestration/validation/dotfiles-T128-regime-counters-a02-pr-feedback.json
.orchestration/validation/dotfiles-T128-regime-counters-a02-review-receipt.md
.orchestration/validation/dotfiles-T128-regime-counters-a02.md
.orchestration/validation/dotfiles-T128-regime-counters-redesign-a01.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round10-codex.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round10-codex.md.transcript.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round11-codex.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round11-codex.md.transcript.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round11.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round12-codex.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round12-codex.md.transcript.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round12.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round13-codex-premises.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round13-codex-premises.md.transcript.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round13-codex.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round13-codex.md.transcript.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round13.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round14-codex.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round14-codex.md.transcript.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round14.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round15-codex.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round15-codex.md.transcript.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round15.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round16-codex.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round16-codex.md.transcript.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round16.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round17-codex.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round17-codex.md.transcript.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round18-codex.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round18-codex.md.transcript.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round18.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round19-codex.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round19-codex.md.transcript.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round2.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round20-codex.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round20.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round21-codex.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22-codex.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round23-codex.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round24-codex.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round24.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round25-codex.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round25.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round26-codex.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round26.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round27-codex.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round27.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round28-codex.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round28.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round29-codex.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round29.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round3.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round30-codex.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round30.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round31-codex.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round31.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round32-codex.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round32.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round33-codex.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round33.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round34-codex.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round34.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round4.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round5.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round6.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round7-codex.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round7-codex.md.transcript.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round7.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round8-codex.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round8-codex.md.transcript.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round8.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round9-codex.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round9-codex.md.transcript.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round9.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-research/baseline.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-research/claude-code-factsheet.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-research/codex-factsheet.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-research/github-factsheet.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-research/method-draft.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-research/practice-evidence.md
.orchestration/validation/dotfiles-T128-regime-v3-inv6-redesign-a01-proposal.md
.orchestration/validation/dotfiles-T128-rules-s1-replan-review-a01-codex-r1.md
.orchestration/validation/dotfiles-T128-rules-s1-replan-review-a01-codex-r2.md
.orchestration/validation/dotfiles-T128-rules-s1-replan-review-a01-codex-r3.md
.orchestration/validation/dotfiles-T128-rules-s1-replan-review-a01-codex-r4.md
.orchestration/validation/dotfiles-T128-rules-s1-replan-review-a01-codex-r5.md
.orchestration/validation/dotfiles-T128-rules-s1-replan-review-a01-codex-r6.md
.orchestration/validation/dotfiles-T128-rules-s1-replan-review-a01.md
.orchestration/validation/dotfiles-T128-rules-step8-a01-audit-0740069.md
.orchestration/validation/dotfiles-T128-rules-step8-a01-audit-0740069.md.last.md
.orchestration/validation/dotfiles-T128-rules-step8-a01-audit-4d3d639.md
.orchestration/validation/dotfiles-T128-rules-step8-a01-audit-4d3d639.md.last.md
.orchestration/validation/dotfiles-T128-rules-step8-a01-crit.json
.orchestration/validation/dotfiles-T128-rules-step8-a01-local-review-0740069.md
.orchestration/validation/dotfiles-T128-rules-step8-a01-local-review-4d3d639.md
.orchestration/validation/dotfiles-T128-rules-step8-a01-pr-feedback.json
.orchestration/validation/dotfiles-T128-rules-step8-a01-pre-amend1.md
.orchestration/validation/dotfiles-T128-rules-step8-a01-pre-amend2.md
.orchestration/validation/dotfiles-T128-rules-step8-a01-pre-amend3.md
.orchestration/validation/dotfiles-T128-rules-step8-a01-pre-amend4.md
.orchestration/validation/dotfiles-T128-rules-step8-a01-pre-amend5.md
.orchestration/validation/dotfiles-T128-rules-step8-a01-pre-amend6.md
.orchestration/validation/dotfiles-T128-rules-step8-a01-review-receipt.md
.orchestration/validation/dotfiles-T128-rules-step8-review-a01-codex-amend1.md
.orchestration/validation/dotfiles-T128-rules-step8-review-a01-codex-amend2.md
.orchestration/validation/dotfiles-T128-rules-step8-review-a01-codex-amend2b.md
.orchestration/validation/dotfiles-T128-rules-step8-review-a01-codex-amend2c.md
.orchestration/validation/dotfiles-T128-rules-step8-review-a01-codex-amend3.md
.orchestration/validation/dotfiles-T128-rules-step8-review-a01-codex-amend3b.md
.orchestration/validation/dotfiles-T128-rules-step8-review-a01-codex-amend3c.md
.orchestration/validation/dotfiles-T128-rules-step8-review-a01-codex-amend4.md
.orchestration/validation/dotfiles-T128-rules-step8-review-a01-codex-amend5.md
.orchestration/validation/dotfiles-T128-rules-step8-review-a01-codex-amend6.md
.orchestration/validation/dotfiles-T128-rules-step8-review-a01-codex-r1.md
.orchestration/validation/dotfiles-T128-rules-step8-review-a01-codex-r3.md
.orchestration/validation/dotfiles-T128-rules-step8-review-a01-codex-r4.md
.orchestration/validation/dotfiles-T128-rules-step8-review-a01-codex-r5.md
.orchestration/validation/dotfiles-T128-rules-step8-review-a01-codex-r6.md
.orchestration/validation/dotfiles-T128-rules-step8-review-a01-codex-r7.md
.orchestration/validation/dotfiles-T128-rules-step8-review-a01-codex-r8.md
.orchestration/validation/dotfiles-T128-rules-step8-review-a01.md
.orchestration/validation/dotfiles-T128-s1-replan-gate-a01-audit-4460d52.md
.orchestration/validation/dotfiles-T128-s1-replan-gate-a01-audit-4460d52.md.last.md
.orchestration/validation/dotfiles-T128-s1-replan-gate-a01-audit-5185dc1.md
.orchestration/validation/dotfiles-T128-s1-replan-gate-a01-audit-5185dc1.md.last.md
.orchestration/validation/dotfiles-T128-s1-replan-gate-a01-crit.json
.orchestration/validation/dotfiles-T128-s1-replan-gate-a01-local-review-4460d52.md
.orchestration/validation/dotfiles-T128-s1-replan-gate-a01-local-review-5185dc1.md
.orchestration/validation/dotfiles-T128-s1-replan-gate-a01-pr-feedback.json
.orchestration/validation/dotfiles-T128-s1-replan-gate-a01-review-receipt.md
.orchestration/validation/dotfiles-T128-s1-replan-gate-review-a01-codex-r1.md
.orchestration/validation/dotfiles-T128-s1-replan-gate-review-a01-codex-r2.md
.orchestration/validation/dotfiles-T128-s1-replan-gate-review-a01-codex-r3.md
.orchestration/validation/dotfiles-T128-s1-replan-gate-review-a01-codex-r4.md
.orchestration/validation/dotfiles-T128-s1-replan-gate-review-a01-codex-r5.md
.orchestration/validation/dotfiles-T128-s1-replan-gate-review-a01.md
.orchestration/validation/dotfiles-T128-seat-launch-args-a01-audit-3345c4d.md
.orchestration/validation/dotfiles-T128-seat-launch-args-a01-audit-3345c4d.md.last.md
.orchestration/validation/dotfiles-T128-seat-launch-args-a01-audit-45b9dd9.md
.orchestration/validation/dotfiles-T128-seat-launch-args-a01-audit-45b9dd9.md.last.md
.orchestration/validation/dotfiles-T128-seat-launch-args-a01-crit.json
.orchestration/validation/dotfiles-T128-seat-launch-args-a01-local-review-3345c4d.md
.orchestration/validation/dotfiles-T128-seat-launch-args-a01-local-review-45b9dd9.md
.orchestration/validation/dotfiles-T128-seat-launch-args-a01-local-review-8b210af.md
.orchestration/validation/dotfiles-T128-seat-launch-args-a01-pr-feedback.json
.orchestration/validation/dotfiles-T128-seat-launch-args-a01-review-receipt.md
.orchestration/validation/dotfiles-T128-seat-launch-args-review-a01-codex-r1.md
.orchestration/validation/dotfiles-T128-seat-launch-args-review-a01-codex-r2.md
.orchestration/validation/dotfiles-T128-seat-launch-args-review-a01-codex-r3.md
.orchestration/validation/dotfiles-T128-seat-launch-args-review-a01.md
.orchestration/validation/dotfiles-T128-seat-liveness-a01-audit-cb9ea17.md
.orchestration/validation/dotfiles-T128-seat-liveness-a01-audit-cb9ea17.md.last.md
.orchestration/validation/dotfiles-T128-seat-liveness-a01-audit-d3bc745.md
.orchestration/validation/dotfiles-T128-seat-liveness-a01-audit-d3bc745.md.last.md
.orchestration/validation/dotfiles-T128-seat-liveness-a01-crit.json
.orchestration/validation/dotfiles-T128-seat-liveness-a01-local-review-cb9ea17.md
.orchestration/validation/dotfiles-T128-seat-liveness-a01-local-review-d3bc745.md
.orchestration/validation/dotfiles-T128-seat-liveness-a01-pr-feedback.json
.orchestration/validation/dotfiles-T128-seat-liveness-a01-review-receipt.md
.orchestration/validation/dotfiles-T128-seat-liveness-a01.md
.orchestration/validation/dotfiles-T128-seat-liveness-followup-a01-audit-b0d39dc.md
.orchestration/validation/dotfiles-T128-seat-liveness-followup-a01-audit-b0d39dc.md.last.md
.orchestration/validation/dotfiles-T128-seat-liveness-followup-a01-audit-bf650af.md
.orchestration/validation/dotfiles-T128-seat-liveness-followup-a01-audit-bf650af.md.last.md
.orchestration/validation/dotfiles-T128-seat-liveness-followup-a01-crit.json
.orchestration/validation/dotfiles-T128-seat-liveness-followup-a01-local-review-b0d39dc.md
.orchestration/validation/dotfiles-T128-seat-liveness-followup-a01-local-review-bf650af.md
.orchestration/validation/dotfiles-T128-seat-liveness-followup-a01-pr-feedback.json
.orchestration/validation/dotfiles-T128-seat-liveness-followup-a01-review-receipt.md
.orchestration/validation/dotfiles-T128-seat-liveness-followup-a02-review-a01-codex-r1.md
.orchestration/validation/dotfiles-T128-seat-liveness-followup-a02-review-a01-codex-r2.md
.orchestration/validation/dotfiles-T128-seat-liveness-followup-review-a01-codex-r1.md
.orchestration/validation/dotfiles-T128-seat-liveness-followup-review-a01-codex-r2.md
.orchestration/validation/dotfiles-T128-seat-liveness-followup-review-a01-codex-r3.md
.orchestration/validation/dotfiles-T128-seat-liveness-followup-review-a01-codex-r4.md
.orchestration/validation/dotfiles-T128-seat-liveness-followup-review-a01-codex-r5.md
.orchestration/validation/dotfiles-T128-seat-liveness-followup-review-a01-codex-r6.md
.orchestration/validation/dotfiles-T128-seat-liveness-followup-review-a01.md
.orchestration/validation/dotfiles-T128-seat-liveness-review-a01-codex-r1.md
.orchestration/validation/dotfiles-T128-seat-liveness-review-a01-codex-r2.md
.orchestration/validation/dotfiles-T128-seat-liveness-review-a01.md
.orchestration/validation/dotfiles-T128-settings-hook-dedupe-a01-audit-bdefcbe.md
.orchestration/validation/dotfiles-T128-settings-hook-dedupe-a01-audit-bdefcbe.md.last.md
.orchestration/validation/dotfiles-T128-settings-hook-dedupe-a01-audit-bf6beb5.md
.orchestration/validation/dotfiles-T128-settings-hook-dedupe-a01-audit-bf6beb5.md.last.md
.orchestration/validation/dotfiles-T128-settings-hook-dedupe-a01-audit-ca892e4.md
.orchestration/validation/dotfiles-T128-settings-hook-dedupe-a01-audit-ca892e4.md.last.md
.orchestration/validation/dotfiles-T128-settings-hook-dedupe-a01-crit.json
.orchestration/validation/dotfiles-T128-settings-hook-dedupe-a01-local-review-bdefcbe.md
.orchestration/validation/dotfiles-T128-settings-hook-dedupe-a01-local-review-bf6beb5.md
.orchestration/validation/dotfiles-T128-settings-hook-dedupe-a01-local-review-ca892e4.md
.orchestration/validation/dotfiles-T128-settings-hook-dedupe-a01-pr-feedback.json
.orchestration/validation/dotfiles-T128-settings-hook-dedupe-a01-pre-amend1.md
.orchestration/validation/dotfiles-T128-settings-hook-dedupe-a01-pre-amend2.md
.orchestration/validation/dotfiles-T128-settings-hook-dedupe-a01-pre-amend3.md
.orchestration/validation/dotfiles-T128-settings-hook-dedupe-a01-pre-amend4.md
.orchestration/validation/dotfiles-T128-settings-hook-dedupe-a01-pre-amend5.md
.orchestration/validation/dotfiles-T128-settings-hook-dedupe-a01-review-receipt.md
.orchestration/validation/dotfiles-T128-settings-hook-dedupe-followup-a01-audit-002f188.md
.orchestration/validation/dotfiles-T128-settings-hook-dedupe-followup-a01-audit-002f188.md.last.md
.orchestration/validation/dotfiles-T128-settings-hook-dedupe-followup-a01-crit.json
.orchestration/validation/dotfiles-T128-settings-hook-dedupe-followup-a01-local-review-002f188.md
.orchestration/validation/dotfiles-T128-settings-hook-dedupe-followup-a01-pr-feedback.json
.orchestration/validation/dotfiles-T128-settings-hook-dedupe-followup-a01-review-receipt.md
.orchestration/validation/dotfiles-T128-settings-hook-dedupe-followup-a01.md
.orchestration/validation/dotfiles-T128-settings-hook-dedupe-followup-review-a01-codex-r1.md
.orchestration/validation/dotfiles-T128-settings-hook-dedupe-followup-review-a01-codex-r2.md
.orchestration/validation/dotfiles-T128-settings-hook-dedupe-followup-review-a01.md
.orchestration/validation/dotfiles-T128-settings-hook-dedupe-review-a01-codex-amend1.md
.orchestration/validation/dotfiles-T128-settings-hook-dedupe-review-a01-codex-amend2.md
.orchestration/validation/dotfiles-T128-settings-hook-dedupe-review-a01-codex-amend3.md
.orchestration/validation/dotfiles-T128-settings-hook-dedupe-review-a01-codex-amend3b.md
.orchestration/validation/dotfiles-T128-settings-hook-dedupe-review-a01-codex-amend4.md
.orchestration/validation/dotfiles-T128-settings-hook-dedupe-review-a01-codex-amend5.md
.orchestration/validation/dotfiles-T128-settings-hook-dedupe-review-a01-codex-r1.md
.orchestration/validation/dotfiles-T128-settings-hook-dedupe-review-a01-codex-r2.md
.orchestration/validation/dotfiles-T128-settings-hook-dedupe-review-a01.md
.orchestration/validation/dotfiles-T128-task-checkers-a01-amend-review-a01-codex.md
.orchestration/validation/dotfiles-T128-task-checkers-a01-amend-review-a01.md
.orchestration/validation/dotfiles-T128-task-checkers-a01-amend-review-a02-codex-r2.md
.orchestration/validation/dotfiles-T128-task-checkers-a01-amend-review-a02-codex-r3.md
.orchestration/validation/dotfiles-T128-task-checkers-a01-amend-review-a02-codex-r4.md
.orchestration/validation/dotfiles-T128-task-checkers-a01-amend-review-a02-codex.md
.orchestration/validation/dotfiles-T128-task-checkers-a01-amend-review-a02.md
.orchestration/validation/dotfiles-T128-task-checkers-a01-audit-c1f60f7.md
.orchestration/validation/dotfiles-T128-task-checkers-a01-audit-c1f60f7.md.last.md
.orchestration/validation/dotfiles-T128-task-checkers-a01-crit.json
.orchestration/validation/dotfiles-T128-task-checkers-a01-local-review-c1f60f7.md
.orchestration/validation/dotfiles-T128-task-checkers-a01-pr-feedback.json
.orchestration/validation/dotfiles-T128-task-checkers-a01-review-receipt.md
.orchestration/validation/dotfiles-T128-task-checkers-followup-a01-audit-19bd6de.md
.orchestration/validation/dotfiles-T128-task-checkers-followup-a01-audit-19bd6de.md.last.md
.orchestration/validation/dotfiles-T128-task-checkers-followup-a01-audit-b84e81f.md
.orchestration/validation/dotfiles-T128-task-checkers-followup-a01-audit-b84e81f.md.last.md
.orchestration/validation/dotfiles-T128-task-checkers-followup-a01-crit.json
.orchestration/validation/dotfiles-T128-task-checkers-followup-a01-local-review-19bd6de.md
.orchestration/validation/dotfiles-T128-task-checkers-followup-a01-local-review-b84e81f.md
.orchestration/validation/dotfiles-T128-task-checkers-followup-a01-pr-feedback.json
.orchestration/validation/dotfiles-T128-task-checkers-followup-a01-review-receipt.md
.orchestration/validation/dotfiles-T128-task-checkers-followup-review-a01-codex-r2.md
.orchestration/validation/dotfiles-T128-task-checkers-followup-review-a01-codex-r3.md
.orchestration/validation/dotfiles-T128-task-checkers-followup-review-a01-codex-r4.md
.orchestration/validation/dotfiles-T128-task-checkers-followup-review-a01-codex.md
.orchestration/validation/dotfiles-T128-task-checkers-followup-review-a01.md
.orchestration/validation/dotfiles-T128-task-checkers-review-a01-codex-r2.md
.orchestration/validation/dotfiles-T128-task-checkers-review-a01-codex-r3.md
.orchestration/validation/dotfiles-T128-task-checkers-review-a01-codex.md
.orchestration/validation/dotfiles-T128-task-checkers-review-a01.md
.orchestration/validation/dotfiles-T128-task-review-a02-a01-round2.md
.orchestration/validation/dotfiles-T128-task-review-a02-a01.md
.orchestration/validation/dotfiles-T128-task-review-a201-a01.md
.orchestration/validation/dotfiles-T128-task-review-a7-a01-round2.md
.orchestration/validation/dotfiles-T128-task-review-a7-a01-round3.md
.orchestration/validation/dotfiles-T128-task-review-a7-a01-round4.md
.orchestration/validation/dotfiles-T128-task-review-a7-a01-round5.md
.orchestration/validation/dotfiles-T128-task-review-a7-a01-round6.md
.orchestration/validation/dotfiles-T128-task-review-a7-a01-round7.md
.orchestration/validation/dotfiles-T128-task-review-a7-a01.md
.orchestration/validation/dotfiles-T128-task-review-contracts-a01-round2.md
.orchestration/validation/dotfiles-T128-task-review-contracts-a01-round3.md
.orchestration/validation/dotfiles-T128-task-review-contracts-a01.md
.orchestration/validation/dotfiles-T128-task-review-phase-a-a01.md
.orchestration/validation/dotfiles-T128-task-review-phase1-a01-codex.md
.orchestration/validation/dotfiles-T128-task-review-phase1-a01.md
.orchestration/validation/dotfiles-T128-task-review-phase1-amend-a01-codex.md
.orchestration/validation/dotfiles-T128-task-review-phase1-amend-a01.md
.orchestration/validation/dotfiles-T128-task-review-phase1-amend-a02-codex.md
.orchestration/validation/dotfiles-T128-task-review-phase1-amend-a02.md
.orchestration/validation/dotfiles-T128-task-review-t718-a01-codex-r2.md
.orchestration/validation/dotfiles-T128-task-review-t718-a01-codex.md
.orchestration/validation/dotfiles-T128-task-review-t718-a01.md
.orchestration/validation/dotfiles-T128-task-review-t718-a02-codex-r10.md
.orchestration/validation/dotfiles-T128-task-review-t718-a02-codex-r11.md
.orchestration/validation/dotfiles-T128-task-review-t718-a02-codex-r12.md
.orchestration/validation/dotfiles-T128-task-review-t718-a02-codex-r13.md
.orchestration/validation/dotfiles-T128-task-review-t718-a02-codex-r14.md
.orchestration/validation/dotfiles-T128-task-review-t718-a02-codex-r15.md
.orchestration/validation/dotfiles-T128-task-review-t718-a02-codex-r16.md
.orchestration/validation/dotfiles-T128-task-review-t718-a02-codex-r17.md
.orchestration/validation/dotfiles-T128-task-review-t718-a02-codex-r18.md
.orchestration/validation/dotfiles-T128-task-review-t718-a02-codex-r19.md
.orchestration/validation/dotfiles-T128-task-review-t718-a02-codex-r2.md
.orchestration/validation/dotfiles-T128-task-review-t718-a02-codex-r3.md
.orchestration/validation/dotfiles-T128-task-review-t718-a02-codex-r4.md
.orchestration/validation/dotfiles-T128-task-review-t718-a02-codex-r5.md
.orchestration/validation/dotfiles-T128-task-review-t718-a02-codex-r6.md
.orchestration/validation/dotfiles-T128-task-review-t718-a02-codex-r7.md
.orchestration/validation/dotfiles-T128-task-review-t718-a02-codex-r8.md
.orchestration/validation/dotfiles-T128-task-review-t718-a02-codex-r9.md
.orchestration/validation/dotfiles-T128-task-review-t718-a02-codex.md
.orchestration/validation/dotfiles-T128-task-review-t718-a02.md
.orchestration/validation/dotfiles-T128-task-review-v1-v2-a01-round11.md
.orchestration/validation/dotfiles-T128-task-review-v1-v2-a01-round12.md
.orchestration/validation/dotfiles-T128-task-review-v1-v2-a01-round13.md
.orchestration/validation/dotfiles-T128-task-review-v1-v2-a01-round14.md
.orchestration/validation/dotfiles-T128-task-review-v1-v2-a01-round15.md
.orchestration/validation/dotfiles-T128-task-review-v1-v2-a01-round16.md
.orchestration/validation/dotfiles-T128-task-review-v1-v2-a01-round17.md
.orchestration/validation/dotfiles-T128-task-review-v1-v2-a01-round18.md
.orchestration/validation/dotfiles-T128-task-review-v1-v2-a01-round19.md
.orchestration/validation/dotfiles-T128-task-review-v1-v2-a01-round2.md
.orchestration/validation/dotfiles-T128-task-review-v1-v2-a01-round3.md
.orchestration/validation/dotfiles-T128-task-review-v1-v2-a01-round4.md
.orchestration/validation/dotfiles-T128-task-review-v1-v2-a01-round5.md
.orchestration/validation/dotfiles-T128-task-review-v1-v2-a01-round6.md
.orchestration/validation/dotfiles-T128-task-review-v1-v2-a01-round7.md
.orchestration/validation/dotfiles-T128-task-review-v1-v2-a01-round8.md
.orchestration/validation/dotfiles-T128-task-review-v1-v2-a01-round9.md
.orchestration/validation/dotfiles-T128-task-review-v1-v2-a01.md
.orchestration/validation/dotfiles-T128-v0-main-tests-a01-audit-adcf783.md
.orchestration/validation/dotfiles-T128-v0-main-tests-a01-audit-adcf783.md.last.md
.orchestration/validation/dotfiles-T128-v0-main-tests-a01-crit.json
.orchestration/validation/dotfiles-T128-v0-main-tests-a01-pr-feedback.json
.orchestration/validation/dotfiles-T128-v0-main-tests-a01-review-receipt.md
.orchestration/validation/dotfiles-T128-v0-main-tests-a01.md
.orchestration/validation/dotfiles-T128-validator-offline-a01-audit-39c186a.md
.orchestration/validation/dotfiles-T128-validator-offline-a01-audit-39c186a.md.last.md
.orchestration/validation/dotfiles-T128-validator-offline-a01-crit.json
.orchestration/validation/dotfiles-T128-validator-offline-a01-local-review-39c186a.md
.orchestration/validation/dotfiles-T128-validator-offline-a01-pr-feedback.json
.orchestration/validation/dotfiles-T128-validator-offline-a01-review-receipt.md
.orchestration/validation/dotfiles-T128-validator-offline-review-a01-codex-r1.md
.orchestration/validation/dotfiles-T128-validator-offline-review-a01-codex-r2.md
.orchestration/validation/dotfiles-T128-validator-offline-review-a01.md
.orchestration/validation/dotfiles-T128-worker-s1-stop-review-a01-codex-r1.md
.orchestration/validation/dotfiles-T128-worker-s1-stop-review-a01-codex-r2.md
.orchestration/validation/dotfiles-T128-worker-s1-stop-review-a01-codex-r3.md
.orchestration/validation/dotfiles-T128-worker-s1-stop-review-a01-codex-r4.md
.orchestration/validation/dotfiles-T128-worker-s1-stop-review-a01-codex-r5.md
.orchestration/validation/dotfiles-T128-worker-s1-stop-review-a01-codex-r6.md
.orchestration/validation/dotfiles-T128-worker-s1-stop-review-a01-codex-r7.md
.orchestration/validation/dotfiles-T128-worker-s1-stop-review-a01-codex-r8.md
.orchestration/validation/dotfiles-T128-worker-s1-stop-review-a01.md
.orchestration/validation/dotfiles-T128-worker-stop-and-watch-a01.md
.orchestration/validation/dotfiles-T128-worker-stop-and-watch-a02-audit-3a54d34.md
.orchestration/validation/dotfiles-T128-worker-stop-and-watch-a02-audit-3a54d34.md.last.md
.orchestration/validation/dotfiles-T128-worker-stop-and-watch-a02-crit.json
.orchestration/validation/dotfiles-T128-worker-stop-and-watch-a02-pr-feedback.json
.orchestration/validation/dotfiles-T128-worker-stop-and-watch-a02-review-receipt.md
.orchestration/validation/dotfiles-T128-worker-stop-and-watch-a02.md
.orchestration/validation/dotfiles-T128-worker-stop-and-watch-redesign-a01.md
.orchestration/validation/dotfiles-T129-assets-omp-hcom-a01-audit-b49da6d.md
.orchestration/validation/dotfiles-T129-assets-omp-hcom-a01-audit-b49da6d.md.last.md
.orchestration/validation/dotfiles-T129-assets-omp-hcom-a01-crit.json
.orchestration/validation/dotfiles-T129-assets-omp-hcom-a01-local-review-b49da6d.md
.orchestration/validation/dotfiles-T129-assets-omp-hcom-a01-pr-feedback.json
.orchestration/validation/dotfiles-T129-assets-omp-hcom-a01-review-codex-r1.md
.orchestration/validation/dotfiles-T129-assets-omp-hcom-a01-review-receipt.md
.orchestration/validation/dotfiles-T129-audit-inherit-replan-json-a01-review-codex-r1.md
.orchestration/validation/dotfiles-T129-normalised-comparison-lint-a01-review-codex-r1.md
.orchestration/validation/dotfiles-T129-pstack-asset-a01-review-codex-r1.md
.orchestration/validation/dotfiles-T62-claude-auto-deny-a01-audit-de8b8b2.md
.orchestration/validation/dotfiles-T62-claude-auto-deny-a01-audit-de8b8b2.md.last.md
.orchestration/validation/dotfiles-T62-claude-auto-deny-a01-crit.json
.orchestration/validation/dotfiles-T62-claude-auto-deny-a01-pr-feedback.json
.orchestration/validation/dotfiles-T62-claude-auto-deny-a01-review-receipt.md
.orchestration/validation/dotfiles-T62-claude-auto-deny-a01-worker-crit.json
.orchestration/validation/dotfiles-T62-claude-auto-deny-a01-worker-review-receipt.md
.orchestration/validation/dotfiles-T62-claude-auto-deny-a01.md
.orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01-audit-04d6e1f3.md
.orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01-audit-04d6e1f3.md.last.md
.orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01-audit-1f4f409a.md
.orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01-audit-1f4f409a.md.last.md
.orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01-audit-34e7423f.md
.orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01-audit-34e7423f.md.last.md
.orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01-audit-7a7c21cd.md
.orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01-audit-7a7c21cd.md.last.md
.orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01-audit-7e83ed9c.md
.orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01-audit-7e83ed9c.md.last.md
.orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01-audit-8770ed66.md
.orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01-audit-8770ed66.md.last.md
.orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01-audit-a0b05905.md
.orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01-audit-a0b05905.md.last.md
.orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01-audit-c58e4835.md
.orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01-audit-c58e4835.md.last.md
.orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01-audit-ddb7bf16.md
.orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01-audit-ddb7bf16.md.last.md
.orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01-audit-e16012eb.md
.orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01-audit-e16012eb.md.last.md
.orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01-audit-eb67299c.md
.orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01-audit-eb67299c.md.last.md
.orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01-crit.json
.orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01-pr-feedback.json
.orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01-review-receipt.md
.orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01.md
.orchestration/validation/dotfiles-T64-codex-worker-never-network-a01-audit-b9c1aefa.md
.orchestration/validation/dotfiles-T64-codex-worker-never-network-a01-audit-b9c1aefa.md.last.md
.orchestration/validation/dotfiles-T64-codex-worker-never-network-a01-audit-d950ac69.md
.orchestration/validation/dotfiles-T64-codex-worker-never-network-a01-audit-d950ac69.md.last.md
.orchestration/validation/dotfiles-T64-codex-worker-never-network-a01-crit.json
.orchestration/validation/dotfiles-T64-codex-worker-never-network-a01-pr-feedback.json
.orchestration/validation/dotfiles-T64-codex-worker-never-network-a01-review-receipt.md
.orchestration/validation/dotfiles-T64-codex-worker-never-network-a01.md
.orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-13340185.md
.orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-13340185.md.last.md
.orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-1845139e.md
.orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-1845139e.md.last.md
.orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-3568b7e2.md
.orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-3568b7e2.md.last.md
.orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-4dfceb6e.md
.orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-4dfceb6e.md.last.md
.orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-5a9f35f5.md
.orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-5a9f35f5.md.last.md
.orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-775a527a.md
.orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-775a527a.md.last.md
.orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-8262be37.md
.orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-8262be37.md.last.md
.orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-8433a01b.md
.orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-8433a01b.md.last.md
.orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-92cad32.md
.orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-92cad32.md.last.md
.orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-a62fce9d.md
.orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-a62fce9d.md.last.md
.orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-a9a85ecf.md
.orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-a9a85ecf.md.last.md
.orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-bc636cb7.md
.orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-bc636cb7.md.last.md
.orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-cb3ded43.md
.orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-cb3ded43.md.last.md
.orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-e11659ac.md
.orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-e11659ac.md.last.md
.orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-ea112e2e.md
.orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-ea112e2e.md.last.md
.orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-fd8aa36.md
.orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-fd8aa36.md.last.md
.orchestration/validation/dotfiles-T65-agent-stop-gate-a01-crit.json
.orchestration/validation/dotfiles-T65-agent-stop-gate-a01-pr-feedback.json
.orchestration/validation/dotfiles-T65-agent-stop-gate-a01-review-receipt.md
.orchestration/validation/dotfiles-T65-agent-stop-gate-a01.md
.orchestration/validation/dotfiles-T66-permgate-dead-lanes-a01-audit-8ae3fdc9.md
.orchestration/validation/dotfiles-T66-permgate-dead-lanes-a01-audit-8ae3fdc9.md.last.md
.orchestration/validation/dotfiles-T66-permgate-dead-lanes-a01-audit-a31dcf86.md
.orchestration/validation/dotfiles-T66-permgate-dead-lanes-a01-audit-a31dcf86.md.last.md
.orchestration/validation/dotfiles-T66-permgate-dead-lanes-a01-audit-a93fcb94.md
.orchestration/validation/dotfiles-T66-permgate-dead-lanes-a01-audit-a93fcb94.md.last.md
.orchestration/validation/dotfiles-T66-permgate-dead-lanes-a01-crit.json
.orchestration/validation/dotfiles-T66-permgate-dead-lanes-a01-pr-feedback.json
.orchestration/validation/dotfiles-T66-permgate-dead-lanes-a01-review-receipt.md
.orchestration/validation/dotfiles-T66-permgate-dead-lanes-a01.md
.orchestration/validation/dotfiles-T67-audit-task-level-a01-audit-28373e27.md
.orchestration/validation/dotfiles-T67-audit-task-level-a01-audit-28373e27.md.last.md
.orchestration/validation/dotfiles-T67-audit-task-level-a01-audit-9476141f.md
.orchestration/validation/dotfiles-T67-audit-task-level-a01-audit-9476141f.md.last.md
.orchestration/validation/dotfiles-T67-audit-task-level-a01-crit.json
.orchestration/validation/dotfiles-T67-audit-task-level-a01-pr-feedback.json
.orchestration/validation/dotfiles-T67-audit-task-level-a01-review-receipt.md
.orchestration/validation/dotfiles-T67-audit-task-level-a01.md
.orchestration/validation/dotfiles-T68-gate-audit-evidence-a01-audit-3ba270d.md
.orchestration/validation/dotfiles-T68-gate-audit-evidence-a01-audit-3ba270d.md.last.md
.orchestration/validation/dotfiles-T68-gate-audit-evidence-a01-audit-4fe3427.md
.orchestration/validation/dotfiles-T68-gate-audit-evidence-a01-audit-4fe3427.md.last.md
.orchestration/validation/dotfiles-T68-gate-audit-evidence-a01-audit-5168613.md
.orchestration/validation/dotfiles-T68-gate-audit-evidence-a01-audit-5168613.md.last.md
.orchestration/validation/dotfiles-T68-gate-audit-evidence-a01-audit-5168613.md.last.md.round1
.orchestration/validation/dotfiles-T68-gate-audit-evidence-a01-audit-5168613.md.round1
.orchestration/validation/dotfiles-T68-gate-audit-evidence-a01-crit.json
.orchestration/validation/dotfiles-T68-gate-audit-evidence-a01-pr-feedback.json
.orchestration/validation/dotfiles-T68-gate-audit-evidence-a01-review-receipt.md
.orchestration/validation/dotfiles-T68-gate-audit-evidence-a01.md
.orchestration/validation/dotfiles-T69-protocol-docs-unification-a01-audit-4656f19.md
.orchestration/validation/dotfiles-T69-protocol-docs-unification-a01-audit-4656f19.md.last.md
.orchestration/validation/dotfiles-T69-protocol-docs-unification-a01-audit-6b060ac.md
.orchestration/validation/dotfiles-T69-protocol-docs-unification-a01-audit-6b060ac.md.last.md
.orchestration/validation/dotfiles-T69-protocol-docs-unification-a01-audit-d31dc32.md
.orchestration/validation/dotfiles-T69-protocol-docs-unification-a01-audit-d31dc32.md.last.md
.orchestration/validation/dotfiles-T69-protocol-docs-unification-a01-audit-d9bbd80.md
.orchestration/validation/dotfiles-T69-protocol-docs-unification-a01-audit-d9bbd80.md.last.md
.orchestration/validation/dotfiles-T69-protocol-docs-unification-a01-crit.json
.orchestration/validation/dotfiles-T69-protocol-docs-unification-a01-pr-feedback.json
.orchestration/validation/dotfiles-T69-protocol-docs-unification-a01-review-receipt.md
.orchestration/validation/dotfiles-T69-protocol-docs-unification-a01.md
.orchestration/validation/dotfiles-T70-make-update-unattended-a01-audit-229a2ec1.md
.orchestration/validation/dotfiles-T70-make-update-unattended-a01-audit-229a2ec1.md.last.md
.orchestration/validation/dotfiles-T70-make-update-unattended-a01-audit-95acd5b6.md
.orchestration/validation/dotfiles-T70-make-update-unattended-a01-audit-95acd5b6.md.last.md
.orchestration/validation/dotfiles-T70-make-update-unattended-a01-crit.json
.orchestration/validation/dotfiles-T70-make-update-unattended-a01-pr-feedback.json
.orchestration/validation/dotfiles-T70-make-update-unattended-a01-review-receipt.md
.orchestration/validation/dotfiles-T70-make-update-unattended-a01.md
.orchestration/validation/dotfiles-T71-generator-multi-target-a01-audit-3ecb487.md
.orchestration/validation/dotfiles-T71-generator-multi-target-a01-audit-3ecb487.md.last.md
.orchestration/validation/dotfiles-T71-generator-multi-target-a01-audit-c7b5fb3.md
.orchestration/validation/dotfiles-T71-generator-multi-target-a01-audit-c7b5fb3.md.last.md
.orchestration/validation/dotfiles-T71-generator-multi-target-a01-audit-ef4324d.md
.orchestration/validation/dotfiles-T71-generator-multi-target-a01-audit-ef4324d.md.last.md
.orchestration/validation/dotfiles-T71-generator-multi-target-a01-crit.json
.orchestration/validation/dotfiles-T71-generator-multi-target-a01-pr-feedback.json
.orchestration/validation/dotfiles-T71-generator-multi-target-a01-review-receipt.md
.orchestration/validation/dotfiles-T71-generator-multi-target-a01.md
.orchestration/validation/dotfiles-T72-bootstrap-ci-pins-a01-audit-d5856e2.md
.orchestration/validation/dotfiles-T72-bootstrap-ci-pins-a01-audit-d5856e2.md.last.md
.orchestration/validation/dotfiles-T72-bootstrap-ci-pins-a01-crit.json
.orchestration/validation/dotfiles-T72-bootstrap-ci-pins-a01-pr-feedback.json
.orchestration/validation/dotfiles-T72-bootstrap-ci-pins-a01-review-receipt.md
.orchestration/validation/dotfiles-T72-bootstrap-ci-pins-a01.md
.orchestration/validation/dotfiles-T73-tool-versions-from-config-a01-audit-60688d49.md
.orchestration/validation/dotfiles-T73-tool-versions-from-config-a01-audit-60688d49.md.last.md
.orchestration/validation/dotfiles-T73-tool-versions-from-config-a01-crit.json
.orchestration/validation/dotfiles-T73-tool-versions-from-config-a01-pr-feedback.json
.orchestration/validation/dotfiles-T73-tool-versions-from-config-a01-review-receipt.md
.orchestration/validation/dotfiles-T73-tool-versions-from-config-a01.md
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-audit-2487b05a.md
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-audit-2487b05a.md.last.md
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-audit-c0ea3e7f.md
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-audit-c0ea3e7f.md.last.md
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-crit.json
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-pr-feedback.json
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-review-receipt.md
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01.md
.orchestration/validation/dotfiles-T75-shell-dead-code-a01-audit-339c1496.md
.orchestration/validation/dotfiles-T75-shell-dead-code-a01-audit-339c1496.md.last.md
.orchestration/validation/dotfiles-T75-shell-dead-code-a01-audit-ef5742f9.md
.orchestration/validation/dotfiles-T75-shell-dead-code-a01-audit-ef5742f9.md.last.md
.orchestration/validation/dotfiles-T75-shell-dead-code-a01-crit.json
.orchestration/validation/dotfiles-T75-shell-dead-code-a01-pr-feedback.json
.orchestration/validation/dotfiles-T75-shell-dead-code-a01-review-receipt.md
.orchestration/validation/dotfiles-T75-shell-dead-code-a01.md
.orchestration/validation/dotfiles-T76-ineffective-settings-a01-audit-26a882a.md
.orchestration/validation/dotfiles-T76-ineffective-settings-a01-audit-26a882a.md.last.md
.orchestration/validation/dotfiles-T76-ineffective-settings-a01-audit-f805ee3.md
.orchestration/validation/dotfiles-T76-ineffective-settings-a01-audit-f805ee3.md.last.md
.orchestration/validation/dotfiles-T76-ineffective-settings-a01-crit.json
.orchestration/validation/dotfiles-T76-ineffective-settings-a01-pr-feedback.json
.orchestration/validation/dotfiles-T76-ineffective-settings-a01-review-receipt.md
.orchestration/validation/dotfiles-T76-ineffective-settings-a01.md
.orchestration/validation/dotfiles-T77-harness-dead-code-a01-audit-977bdf1.md
.orchestration/validation/dotfiles-T77-harness-dead-code-a01-audit-977bdf1.md.last.md
.orchestration/validation/dotfiles-T77-harness-dead-code-a01-crit.json
.orchestration/validation/dotfiles-T77-harness-dead-code-a01-pr-feedback.json
.orchestration/validation/dotfiles-T77-harness-dead-code-a01-review-receipt.md
.orchestration/validation/dotfiles-T77-harness-dead-code-a01.md
.orchestration/validation/dotfiles-T77b-enforce-uv-hook-contract-a01-audit-43d45ff.md
.orchestration/validation/dotfiles-T77b-enforce-uv-hook-contract-a01-audit-43d45ff.md.last.md
.orchestration/validation/dotfiles-T77b-enforce-uv-hook-contract-a01-crit.json
.orchestration/validation/dotfiles-T77b-enforce-uv-hook-contract-a01-pr-feedback.json
.orchestration/validation/dotfiles-T77b-enforce-uv-hook-contract-a01-review-receipt.md
.orchestration/validation/dotfiles-T77b-enforce-uv-hook-contract-a01-worker-crit.json
.orchestration/validation/dotfiles-T77b-enforce-uv-hook-contract-a01-worker-review-receipt.md
.orchestration/validation/dotfiles-T77b-enforce-uv-hook-contract-a01.md
.orchestration/validation/dotfiles-T78-dead-docs-adh-a01-audit-8d536a3.md
.orchestration/validation/dotfiles-T78-dead-docs-adh-a01-audit-8d536a3.md.last.md
.orchestration/validation/dotfiles-T78-dead-docs-adh-a01-crit.json
.orchestration/validation/dotfiles-T78-dead-docs-adh-a01-pr-feedback.json
.orchestration/validation/dotfiles-T78-dead-docs-adh-a01-review-receipt.md
.orchestration/validation/dotfiles-T78-dead-docs-adh-a01.md
.orchestration/validation/dotfiles-T79-remove-adh-profile-a01-audit-123bf10.md
.orchestration/validation/dotfiles-T79-remove-adh-profile-a01-audit-123bf10.md.last.md
.orchestration/validation/dotfiles-T79-remove-adh-profile-a01-crit.json
.orchestration/validation/dotfiles-T79-remove-adh-profile-a01-pr-feedback.json
.orchestration/validation/dotfiles-T79-remove-adh-profile-a01-review-receipt.md
.orchestration/validation/dotfiles-T79-remove-adh-profile-a01.md
.orchestration/validation/dotfiles-T80-codex-command-hooks-a01-audit-8a4cf12.md
.orchestration/validation/dotfiles-T80-codex-command-hooks-a01-audit-8a4cf12.md.last.md
.orchestration/validation/dotfiles-T80-codex-command-hooks-a01-crit.json
.orchestration/validation/dotfiles-T80-codex-command-hooks-a01-pr-feedback.json
.orchestration/validation/dotfiles-T80-codex-command-hooks-a01-review-receipt.md
.orchestration/validation/dotfiles-T80-codex-command-hooks-a01.md
.orchestration/validation/dotfiles-T81-compactiondb-vendor-a01-audit-8c8cf69.md
.orchestration/validation/dotfiles-T81-compactiondb-vendor-a01-audit-8c8cf69.md.last.md
.orchestration/validation/dotfiles-T81-compactiondb-vendor-a01-audit-a1c69c4.md
.orchestration/validation/dotfiles-T81-compactiondb-vendor-a01-audit-a1c69c4.md.last.md
.orchestration/validation/dotfiles-T81-compactiondb-vendor-a01-crit.json
.orchestration/validation/dotfiles-T81-compactiondb-vendor-a01-pr-feedback.json
.orchestration/validation/dotfiles-T81-compactiondb-vendor-a01-review-receipt.md
.orchestration/validation/dotfiles-T81-compactiondb-vendor-a01.md
.orchestration/validation/dotfiles-T81b-compactiondb-vendor-hygiene-a01-audit-a536af5.md
.orchestration/validation/dotfiles-T81b-compactiondb-vendor-hygiene-a01-audit-a536af5.md.last.md
.orchestration/validation/dotfiles-T81b-compactiondb-vendor-hygiene-a01-audit-b9acaa3.md
.orchestration/validation/dotfiles-T81b-compactiondb-vendor-hygiene-a01-audit-b9acaa3.md.last.md
.orchestration/validation/dotfiles-T81b-compactiondb-vendor-hygiene-a01-crit.json
.orchestration/validation/dotfiles-T81b-compactiondb-vendor-hygiene-a01-pr-feedback.json
.orchestration/validation/dotfiles-T81b-compactiondb-vendor-hygiene-a01-review-receipt.md
.orchestration/validation/dotfiles-T81b-compactiondb-vendor-hygiene-a01-worker-crit.json
.orchestration/validation/dotfiles-T81b-compactiondb-vendor-hygiene-a01-worker-review-receipt.md
.orchestration/validation/dotfiles-T81b-compactiondb-vendor-hygiene-a01.md
.orchestration/validation/dotfiles-T82-codex-compaction-hooks-a01-audit-7ee9108.md
.orchestration/validation/dotfiles-T82-codex-compaction-hooks-a01-audit-7ee9108.md.last.md
.orchestration/validation/dotfiles-T82-codex-compaction-hooks-a01-audit-94761d1.md
.orchestration/validation/dotfiles-T82-codex-compaction-hooks-a01-audit-94761d1.md.last.md
.orchestration/validation/dotfiles-T82-codex-compaction-hooks-a01-audit-9ff2ad5.md
.orchestration/validation/dotfiles-T82-codex-compaction-hooks-a01-audit-9ff2ad5.md.last.md
.orchestration/validation/dotfiles-T82-codex-compaction-hooks-a01-audit-c466231.md
.orchestration/validation/dotfiles-T82-codex-compaction-hooks-a01-audit-c466231.md.last.md
.orchestration/validation/dotfiles-T82-codex-compaction-hooks-a01-crit.json
.orchestration/validation/dotfiles-T82-codex-compaction-hooks-a01-pr-feedback.json
.orchestration/validation/dotfiles-T82-codex-compaction-hooks-a01-review-receipt.md
.orchestration/validation/dotfiles-T82-codex-compaction-hooks-a01.md
.orchestration/validation/dotfiles-T82b-codex-hook-trust-pins-a01-audit-00a5b09.md
.orchestration/validation/dotfiles-T82b-codex-hook-trust-pins-a01-audit-00a5b09.md.last.md
.orchestration/validation/dotfiles-T82b-codex-hook-trust-pins-a01-audit-2552205.md
.orchestration/validation/dotfiles-T82b-codex-hook-trust-pins-a01-audit-2552205.md.last.md
.orchestration/validation/dotfiles-T82b-codex-hook-trust-pins-a01-audit-315e739.md
.orchestration/validation/dotfiles-T82b-codex-hook-trust-pins-a01-audit-315e739.md.last.md
.orchestration/validation/dotfiles-T82b-codex-hook-trust-pins-a01-audit-569bc44.md
.orchestration/validation/dotfiles-T82b-codex-hook-trust-pins-a01-audit-569bc44.md.last.md
.orchestration/validation/dotfiles-T82b-codex-hook-trust-pins-a01-audit-a6c997b.md
.orchestration/validation/dotfiles-T82b-codex-hook-trust-pins-a01-audit-a6c997b.md.last.md
.orchestration/validation/dotfiles-T82b-codex-hook-trust-pins-a01-audit-ad05e8b.md
.orchestration/validation/dotfiles-T82b-codex-hook-trust-pins-a01-audit-ad05e8b.md.last.md
.orchestration/validation/dotfiles-T82b-codex-hook-trust-pins-a01-audit-c54fdc0.md
.orchestration/validation/dotfiles-T82b-codex-hook-trust-pins-a01-audit-c54fdc0.md.last.md
.orchestration/validation/dotfiles-T82b-codex-hook-trust-pins-a01-audit-d870215.md
.orchestration/validation/dotfiles-T82b-codex-hook-trust-pins-a01-audit-d870215.md.last.md
.orchestration/validation/dotfiles-T82b-codex-hook-trust-pins-a01-audit-f6e99ba.md
.orchestration/validation/dotfiles-T82b-codex-hook-trust-pins-a01-audit-f6e99ba.md.last.md
.orchestration/validation/dotfiles-T82b-codex-hook-trust-pins-a01-crit.json
.orchestration/validation/dotfiles-T82b-codex-hook-trust-pins-a01-pr-feedback.json
.orchestration/validation/dotfiles-T82b-codex-hook-trust-pins-a01-review-receipt.md
.orchestration/validation/dotfiles-T82b-codex-hook-trust-pins-a01.md
.orchestration/validation/dotfiles-T83-docs-diet-a01-audit-914c765.md
.orchestration/validation/dotfiles-T83-docs-diet-a01-audit-914c765.md.last.md
.orchestration/validation/dotfiles-T83-docs-diet-a01-crit.json
.orchestration/validation/dotfiles-T83-docs-diet-a01-pr-feedback.json
.orchestration/validation/dotfiles-T83-docs-diet-a01-review-receipt.md
.orchestration/validation/dotfiles-T83-docs-diet-a01.md
.orchestration/validation/dotfiles-T84-orchestrator-kind-a01-audit-26e748e.md
.orchestration/validation/dotfiles-T84-orchestrator-kind-a01-audit-26e748e.md.last.md
.orchestration/validation/dotfiles-T84-orchestrator-kind-a01-audit-55f4d43.md
.orchestration/validation/dotfiles-T84-orchestrator-kind-a01-audit-55f4d43.md.last.md
.orchestration/validation/dotfiles-T84-orchestrator-kind-a01-crit.json
.orchestration/validation/dotfiles-T84-orchestrator-kind-a01-pr-feedback.json
.orchestration/validation/dotfiles-T84-orchestrator-kind-a01-review-receipt.md
.orchestration/validation/dotfiles-T84-orchestrator-kind-a01.md
.orchestration/validation/dotfiles-T85-launcher-orchestrator-kind-a01-audit-20361c5.md
.orchestration/validation/dotfiles-T85-launcher-orchestrator-kind-a01-audit-20361c5.md.last.md
.orchestration/validation/dotfiles-T85-launcher-orchestrator-kind-a01-crit.json
.orchestration/validation/dotfiles-T85-launcher-orchestrator-kind-a01-pr-feedback.json
.orchestration/validation/dotfiles-T85-launcher-orchestrator-kind-a01-review-receipt.md
.orchestration/validation/dotfiles-T85-launcher-orchestrator-kind-a01.md
.orchestration/validation/dotfiles-T86-codex-orchestrate-a01-audit-567c8d1.md
.orchestration/validation/dotfiles-T86-codex-orchestrate-a01-audit-567c8d1.md.last.md
.orchestration/validation/dotfiles-T86-codex-orchestrate-a01-audit-63a9b10.md
.orchestration/validation/dotfiles-T86-codex-orchestrate-a01-audit-63a9b10.md.last.md
.orchestration/validation/dotfiles-T86-codex-orchestrate-a01-crit.json
.orchestration/validation/dotfiles-T86-codex-orchestrate-a01-pr-feedback.json
.orchestration/validation/dotfiles-T86-codex-orchestrate-a01-review-receipt.md
.orchestration/validation/dotfiles-T86-codex-orchestrate-a01-worker-crit.json
.orchestration/validation/dotfiles-T86-codex-orchestrate-a01-worker-review-receipt.md
.orchestration/validation/dotfiles-T86-codex-orchestrate-a01.md
.orchestration/validation/dotfiles-T88-parallel-execution-rule-a01-audit-0189cfb.md
.orchestration/validation/dotfiles-T88-parallel-execution-rule-a01-audit-0189cfb.md.last.md
.orchestration/validation/dotfiles-T88-parallel-execution-rule-a01-audit-04fd942.md
.orchestration/validation/dotfiles-T88-parallel-execution-rule-a01-audit-04fd942.md.last.md
.orchestration/validation/dotfiles-T88-parallel-execution-rule-a01-audit-19becfc.md
.orchestration/validation/dotfiles-T88-parallel-execution-rule-a01-audit-19becfc.md.last.md
.orchestration/validation/dotfiles-T88-parallel-execution-rule-a01-audit-5bef558.md
.orchestration/validation/dotfiles-T88-parallel-execution-rule-a01-audit-5bef558.md.last.md
.orchestration/validation/dotfiles-T88-parallel-execution-rule-a01-audit-62845ab.md
.orchestration/validation/dotfiles-T88-parallel-execution-rule-a01-audit-62845ab.md.last.md
.orchestration/validation/dotfiles-T88-parallel-execution-rule-a01-audit-e50150df.md
.orchestration/validation/dotfiles-T88-parallel-execution-rule-a01-audit-e50150df.md.last.md
.orchestration/validation/dotfiles-T88-parallel-execution-rule-a01-audit-e68eb6a7.md
.orchestration/validation/dotfiles-T88-parallel-execution-rule-a01-audit-e68eb6a7.md.last.md
.orchestration/validation/dotfiles-T88-parallel-execution-rule-a01-audit-fb4c9a9.md
.orchestration/validation/dotfiles-T88-parallel-execution-rule-a01-audit-fb4c9a9.md.last.md
.orchestration/validation/dotfiles-T88-parallel-execution-rule-a01-crit.json
.orchestration/validation/dotfiles-T88-parallel-execution-rule-a01-pr-feedback.json
.orchestration/validation/dotfiles-T88-parallel-execution-rule-a01-review-receipt.md
.orchestration/validation/dotfiles-T88-parallel-execution-rule-a01.md
.orchestration/validation/dotfiles-T89-add-worker-same-workspace-a01-audit-37cf5e47.md
.orchestration/validation/dotfiles-T89-add-worker-same-workspace-a01-audit-37cf5e47.md.last.md
.orchestration/validation/dotfiles-T89-add-worker-same-workspace-a01-audit-55d7e77c.md
.orchestration/validation/dotfiles-T89-add-worker-same-workspace-a01-audit-55d7e77c.md.last.md
.orchestration/validation/dotfiles-T89-add-worker-same-workspace-a01-audit-958468ba.md
.orchestration/validation/dotfiles-T89-add-worker-same-workspace-a01-audit-958468ba.md.last.md
.orchestration/validation/dotfiles-T89-add-worker-same-workspace-a01-crit.json
.orchestration/validation/dotfiles-T89-add-worker-same-workspace-a01-pr-feedback.json
.orchestration/validation/dotfiles-T89-add-worker-same-workspace-a01-review-receipt.md
.orchestration/validation/dotfiles-T89-add-worker-same-workspace-a01.md
.orchestration/validation/dotfiles-T90-github-identity-separation-a01-audit-507e9c1.md
.orchestration/validation/dotfiles-T90-github-identity-separation-a01-audit-507e9c1.md.last.md
.orchestration/validation/dotfiles-T90-github-identity-separation-a01-audit-e2d5c9a.md
.orchestration/validation/dotfiles-T90-github-identity-separation-a01-audit-e2d5c9a.md.last.md
.orchestration/validation/dotfiles-T90-github-identity-separation-a01-crit.json
.orchestration/validation/dotfiles-T90-github-identity-separation-a01-pr-feedback.json
.orchestration/validation/dotfiles-T90-github-identity-separation-a01-review-receipt.md
.orchestration/validation/dotfiles-T90-github-identity-separation-a01-worker-crit.json
.orchestration/validation/dotfiles-T90-github-identity-separation-a01-worker-review-receipt.md
.orchestration/validation/dotfiles-T90-github-identity-separation-a01.md
.orchestration/validation/dotfiles-T90b-ruleset-sole-merger-a01-audit-5db3200.md
.orchestration/validation/dotfiles-T90b-ruleset-sole-merger-a01-audit-5db3200.md.last.md
.orchestration/validation/dotfiles-T90b-ruleset-sole-merger-a01-crit.json
.orchestration/validation/dotfiles-T90b-ruleset-sole-merger-a01-pr-feedback.json
.orchestration/validation/dotfiles-T90b-ruleset-sole-merger-a01-review-receipt.md
.orchestration/validation/dotfiles-T90b-ruleset-sole-merger-a01-worker-crit.json
.orchestration/validation/dotfiles-T90b-ruleset-sole-merger-a01-worker-review-receipt.md
.orchestration/validation/dotfiles-T90b-ruleset-sole-merger-a01.md
.orchestration/validation/dotfiles-T91-secret-scan-sk-boundary-a01-audit-1af78d7.md
.orchestration/validation/dotfiles-T91-secret-scan-sk-boundary-a01-audit-1af78d7.md.last.md
.orchestration/validation/dotfiles-T91-secret-scan-sk-boundary-a01-audit-35d102b7.md
.orchestration/validation/dotfiles-T91-secret-scan-sk-boundary-a01-audit-35d102b7.md.last.md
.orchestration/validation/dotfiles-T91-secret-scan-sk-boundary-a01-audit-ffddc8a.md
.orchestration/validation/dotfiles-T91-secret-scan-sk-boundary-a01-audit-ffddc8a.md.last.md
.orchestration/validation/dotfiles-T91-secret-scan-sk-boundary-a01-crit.json
.orchestration/validation/dotfiles-T91-secret-scan-sk-boundary-a01-pr-feedback.json
.orchestration/validation/dotfiles-T91-secret-scan-sk-boundary-a01-review-receipt.md
.orchestration/validation/dotfiles-T91-secret-scan-sk-boundary-a01.md
.orchestration/validation/dotfiles-T92-stop-gate-sandbox-placeholders-a01-audit-153a647.md
.orchestration/validation/dotfiles-T92-stop-gate-sandbox-placeholders-a01-audit-153a647.md.last.md
.orchestration/validation/dotfiles-T92-stop-gate-sandbox-placeholders-a01-audit-3371cc8.md
.orchestration/validation/dotfiles-T92-stop-gate-sandbox-placeholders-a01-audit-3371cc8.md.last.md
.orchestration/validation/dotfiles-T92-stop-gate-sandbox-placeholders-a01-audit-bbd3d3f.md
.orchestration/validation/dotfiles-T92-stop-gate-sandbox-placeholders-a01-audit-bbd3d3f.md.last.md
.orchestration/validation/dotfiles-T92-stop-gate-sandbox-placeholders-a01-crit.json
.orchestration/validation/dotfiles-T92-stop-gate-sandbox-placeholders-a01-pr-feedback.json
.orchestration/validation/dotfiles-T92-stop-gate-sandbox-placeholders-a01-review-receipt.md
.orchestration/validation/dotfiles-T92-stop-gate-sandbox-placeholders-a01.md
.orchestration/validation/dotfiles-T93-gate-masked-feedback-bodies-a01-audit-254d9eb.md
.orchestration/validation/dotfiles-T93-gate-masked-feedback-bodies-a01-audit-254d9eb.md.last.md
.orchestration/validation/dotfiles-T93-gate-masked-feedback-bodies-a01-audit-aa5b061.md
.orchestration/validation/dotfiles-T93-gate-masked-feedback-bodies-a01-audit-aa5b061.md.last.md
.orchestration/validation/dotfiles-T93-gate-masked-feedback-bodies-a01-audit-dd155f2.md
.orchestration/validation/dotfiles-T93-gate-masked-feedback-bodies-a01-audit-dd155f2.md.last.md
.orchestration/validation/dotfiles-T93-gate-masked-feedback-bodies-a01-crit.json
.orchestration/validation/dotfiles-T93-gate-masked-feedback-bodies-a01-pr-feedback.json
.orchestration/validation/dotfiles-T93-gate-masked-feedback-bodies-a01-review-receipt.md
.orchestration/validation/dotfiles-T93-gate-masked-feedback-bodies-a01.md
.orchestration/validation/dotfiles-T94-upgrade-pins-a01-audit-6f5c776.md
.orchestration/validation/dotfiles-T94-upgrade-pins-a01-audit-6f5c776.md.last.md
.orchestration/validation/dotfiles-T94-upgrade-pins-a01-crit.json
.orchestration/validation/dotfiles-T94-upgrade-pins-a01-pr-feedback.json
.orchestration/validation/dotfiles-T94-upgrade-pins-a01-review-receipt.md
.orchestration/validation/dotfiles-T94-upgrade-pins-a01.md
.orchestration/validation/dotfiles-T95-sandbox-placeholder-files-on-disk-a01-audit-b9beca2.md
.orchestration/validation/dotfiles-T95-sandbox-placeholder-files-on-disk-a01-audit-b9beca2.md.last.md
.orchestration/validation/dotfiles-T95-sandbox-placeholder-files-on-disk-a01-crit.json
.orchestration/validation/dotfiles-T95-sandbox-placeholder-files-on-disk-a01-pr-feedback.json
.orchestration/validation/dotfiles-T95-sandbox-placeholder-files-on-disk-a01-review-receipt.md
.orchestration/validation/dotfiles-T95-sandbox-placeholder-files-on-disk-a01.md
.orchestration/validation/dotfiles-T96-codex-worker-gpt61-sol-high-a01-audit-3a06011.md
.orchestration/validation/dotfiles-T96-codex-worker-gpt61-sol-high-a01-audit-3a06011.md.last.md
.orchestration/validation/dotfiles-T96-codex-worker-gpt61-sol-high-a01-crit.json
.orchestration/validation/dotfiles-T96-codex-worker-gpt61-sol-high-a01-pr-feedback.json
.orchestration/validation/dotfiles-T96-codex-worker-gpt61-sol-high-a01-review-receipt.md
.orchestration/validation/dotfiles-T96-codex-worker-gpt61-sol-high-a01.md
.orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-audit-391d2b4.md
.orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-audit-391d2b4.md.last.md
.orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-audit-5b6b0d9.md
.orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-audit-5b6b0d9.md.last.md
.orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-audit-8ffa554.md
.orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-audit-8ffa554.md.last.md
.orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-audit-efe6735.md
.orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-audit-efe6735.md.last.md
.orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-crit.json
.orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-pr-feedback.json
.orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-review-receipt.md
.orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-worker-crit.json
.orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-worker-review-receipt.md
.orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01.md
.orchestration/validation/dotfiles-T98-evidence-home-path-masking-a01-audit-6ce4e3b.md
.orchestration/validation/dotfiles-T98-evidence-home-path-masking-a01-audit-6ce4e3b.md.last.md
.orchestration/validation/dotfiles-T98-evidence-home-path-masking-a01-audit-aa55684.md
.orchestration/validation/dotfiles-T98-evidence-home-path-masking-a01-audit-aa55684.md.last.md
.orchestration/validation/dotfiles-T98-evidence-home-path-masking-a01-audit-aceb1b1.md
.orchestration/validation/dotfiles-T98-evidence-home-path-masking-a01-audit-aceb1b1.md.last.md
.orchestration/validation/dotfiles-T98-evidence-home-path-masking-a01-crit.json
.orchestration/validation/dotfiles-T98-evidence-home-path-masking-a01-pr-feedback.json
.orchestration/validation/dotfiles-T98-evidence-home-path-masking-a01-review-receipt.md
.orchestration/validation/dotfiles-T98-evidence-home-path-masking-a01.md
.orchestration/validation/dotfiles-T98b-runner-home-and-review-body-a01-audit-70f060e.md
.orchestration/validation/dotfiles-T98b-runner-home-and-review-body-a01-audit-70f060e.md.last.md
.orchestration/validation/dotfiles-T98b-runner-home-and-review-body-a01-crit.json
.orchestration/validation/dotfiles-T98b-runner-home-and-review-body-a01-pr-feedback.json
.orchestration/validation/dotfiles-T98b-runner-home-and-review-body-a01-review-receipt.md
.orchestration/validation/dotfiles-T98b-runner-home-and-review-body-a01.md
.orchestration/validation/dotfiles-T98c-claude-seat-artifact-write-exception-a01-audit-d175164.md
.orchestration/validation/dotfiles-T98c-claude-seat-artifact-write-exception-a01-audit-d175164.md.last.md
.orchestration/validation/dotfiles-T98c-claude-seat-artifact-write-exception-a01-crit.json
.orchestration/validation/dotfiles-T98c-claude-seat-artifact-write-exception-a01-pr-feedback.json
.orchestration/validation/dotfiles-T98c-claude-seat-artifact-write-exception-a01-review-receipt.md
.orchestration/validation/dotfiles-T98c-claude-seat-artifact-write-exception-a01.md
.orchestration/validation/dotfiles-T99-nix-plans-history-a01-audit-43eeb91.md
.orchestration/validation/dotfiles-T99-nix-plans-history-a01-audit-43eeb91.md.last.md
.orchestration/validation/dotfiles-T99-nix-plans-history-a01-crit.json
.orchestration/validation/dotfiles-T99-nix-plans-history-a01-pr-feedback.json
.orchestration/validation/dotfiles-T99-nix-plans-history-a01-review-receipt.md
.orchestration/validation/dotfiles-T99-nix-plans-history-a01-worker-crit.json
.orchestration/validation/dotfiles-T99-nix-plans-history-a01-worker-review-receipt.md
.orchestration/validation/dotfiles-T99-nix-plans-history-a01.md
.orchestration/validation/e2e-claude-claude-linux.md
.orchestration/validation/e2e-claude-codex-linux.md
.orchestration/validation/e2e-codex-claude-linux.md
.orchestration/validation/e2e-codex-codex-linux.md
.orchestration/validation/e2e-macos-installers.md
.orchestration/validation/fix-chezmoi-pycache-modify-exec.txt
.orchestration/validation/github-auth-design-2026-10-05.md
.orchestration/validation/operator-patches/README.md
.orchestration/validation/operator-patches/t710.patch
.orchestration/validation/operator-patches/t717+t710.patch
.orchestration/validation/operator-patches/t717.patch
.orchestration/validation/orchestration-boundary-2026-10-03-pr-feedback.json
.orchestration/validation/pins-2026-10-06.diff
.orchestration/validation/plan-004.md
.orchestration/validation/regime-boundary-check-2026-10-14T1354Z.txt
.orchestration/validation/remote-diff-01.md
.prettierignore
.ua/fingerprints.json
.ua/knowledge-graph.json
.ua/meta.json
AGENTS.md
CLAUDE.md
Dockerfile
Makefile
README.md
archive/CompactionDB-2.0.0.zip
docs/history/README.md
docs/history/nix-first-architecture.md
docs/history/nix-migration.md
flake.lock
flake.nix
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
install/common/mise.sh
install/common/sheldon.sh
install/macos/arm64/run.sh
install/macos/common/brew.sh
install/macos/common/dependencies.sh
install/ubuntu/client/zed.sh
install/ubuntu/common/apparmor_userns.sh
install/ubuntu/common/aws_cli.sh
install/ubuntu/server/starship.sh
nix/home-manager/default.nix
nix/nix-darwin/default.nix
nix/shared/packages.nix
plans/004-harden-and-lock-the-supply-chain.md
plans/005-make-runtime-health-and-verification-truthful.md
plans/README.md
renovate.json
reviews/ADH_Integrated_Plan/CHANGELOG_JA.md
reviews/ADH_Integrated_Plan/DESIGN_JA.md
reviews/ADH_Integrated_Plan/DOCUMENT_VALIDATION.md
reviews/ADH_Integrated_Plan/INTEGRATED_PLAN_JA.md
reviews/ADH_Integrated_Plan/MODEL_OPTIMIZATION_JA.md
reviews/ADH_Integrated_Plan/PACKAGE_MANIFEST.json
reviews/ADH_Integrated_Plan/PLAN_QA.json
reviews/ADH_Integrated_Plan/README_JA.md
reviews/ADH_Integrated_Plan/REVISION_GUIDE_JA.md
reviews/ADH_Integrated_Plan/SHA256SUMS
reviews/ADH_Integrated_Plan/START_HERE.md
reviews/ADH_Integrated_Plan/artifacts/L10_EVAL.md
reviews/ADH_Integrated_Plan/artifacts/L1_BRD.md
reviews/ADH_Integrated_Plan/artifacts/L2_PRD.md
reviews/ADH_Integrated_Plan/artifacts/L3_REQ.md
reviews/ADH_Integrated_Plan/artifacts/L4_ACCEPTANCE.md
reviews/ADH_Integrated_Plan/artifacts/L5_ARCH_ADR.md
reviews/ADH_Integrated_Plan/artifacts/L6_SPEC.md
reviews/ADH_Integrated_Plan/artifacts/L7_TEST.md
reviews/ADH_Integrated_Plan/artifacts/L8_IPLAN.md
reviews/ADH_Integrated_Plan/artifacts/L9_CHG.md
reviews/ADH_Integrated_Plan/artifacts/README.md
reviews/ADH_Integrated_Plan/contracts/OPERATION_INDEX.md
reviews/ADH_Integrated_Plan/contracts/STACK_CONTRACT_NOTES.md
reviews/ADH_Integrated_Plan/contracts/document-graph.schema.json
reviews/ADH_Integrated_Plan/contracts/guardrails.schema.json
reviews/ADH_Integrated_Plan/contracts/model-execution.schema.json
reviews/ADH_Integrated_Plan/contracts/operation_inventory.json
reviews/ADH_Integrated_Plan/contracts/requirements.json
reviews/ADH_Integrated_Plan/contracts/stack-integration.schema.json
reviews/ADH_Integrated_Plan/docs/00_WBS_INDEX.md
reviews/ADH_Integrated_Plan/docs/01_SCOPE_AND_BASELINE.md
reviews/ADH_Integrated_Plan/docs/02_ROLES_AND_AGMSG.md
reviews/ADH_Integrated_Plan/docs/03_BOOTSTRAP_AND_RUN_ORDER.md
reviews/ADH_Integrated_Plan/docs/04_SPECIFICATION_COMPLETIONS.md
reviews/ADH_Integrated_Plan/docs/05_VERIFICATION_STANDARD.md
reviews/ADH_Integrated_Plan/docs/06_ENVIRONMENT_AND_NATIVE.md
reviews/ADH_Integrated_Plan/docs/07_COMPLETION_AND_RELEASE.md
reviews/ADH_Integrated_Plan/docs/08_CODING_AND_COMMANDS.md
reviews/ADH_Integrated_Plan/docs/09_RECOVERY_AND_HANDOFF.md
reviews/ADH_Integrated_Plan/docs/10_API_COMPLETION_PLAN.md
reviews/ADH_Integrated_Plan/docs/11_ACCEPTANCE_FIXTURES.md
reviews/ADH_Integrated_Plan/docs/12_DOCUMENT_USE_AND_DELIVERY.md
reviews/ADH_Integrated_Plan/docs/13_TASK_PROTOCOL_AND_CHECKPOINT.md
reviews/ADH_Integrated_Plan/docs/14_MODEL_CONTEXT_AND_SKILLS.md
reviews/ADH_Integrated_Plan/docs/15_MODEL_EVALUATION_AND_ROLLOUT.md
reviews/ADH_Integrated_Plan/docs/16_V4_RUNBOOK.md
reviews/ADH_Integrated_Plan/docs/17_COMPONENT_CATALOG.md
reviews/ADH_Integrated_Plan/evaluation/DOCUMENT_GUARDRAIL_PROTOCOL.md
reviews/ADH_Integrated_Plan/evaluation/EXPERIMENT_PROTOCOL.md
reviews/ADH_Integrated_Plan/evaluation/V4_INTEGRATION_PROTOCOL.md
reviews/ADH_Integrated_Plan/evaluation/control_prompts/CLAUDE_LEAD.md
reviews/ADH_Integrated_Plan/evaluation/control_prompts/CLAUDE_REVIEWER.md
reviews/ADH_Integrated_Plan/evaluation/control_prompts/CODEX_WORKER.md
reviews/ADH_Integrated_Plan/evaluation/control_prompts/VERIFIER_RUNBOOK.md
reviews/ADH_Integrated_Plan/evaluation/knowledge_cases.json
reviews/ADH_Integrated_Plan/evaluation/quality_cases.json
reviews/ADH_Integrated_Plan/evaluation/run_matrix.json
reviews/ADH_Integrated_Plan/evaluation/skill-routing-cases.json
reviews/ADH_Integrated_Plan/evaluation/stack_skill_routing_cases.json
reviews/ADH_Integrated_Plan/examples/README.md
reviews/ADH_Integrated_Plan/examples/guard_decision.example.json
reviews/ADH_Integrated_Plan/examples/guard_qualification.example.json
reviews/ADH_Integrated_Plan/examples/model_profile.example.json
reviews/ADH_Integrated_Plan/examples/operation_intent.example.json
reviews/ADH_Integrated_Plan/examples/stack_KnowledgeQuery.example.json
reviews/ADH_Integrated_Plan/examples/stack_LearningCandidate.example.json
reviews/ADH_Integrated_Plan/examples/stack_QualityPlan.example.json
reviews/ADH_Integrated_Plan/examples/stack_ReleaseSet.example.json
reviews/ADH_Integrated_Plan/examples/task_packet.example.json
reviews/ADH_Integrated_Plan/profiles/README.md
reviews/ADH_Integrated_Plan/profiles/model_profiles.json
reviews/ADH_Integrated_Plan/prompts/CLAUDE_LEAD.md
reviews/ADH_Integrated_Plan/prompts/CLAUDE_REVIEWER.md
reviews/ADH_Integrated_Plan/prompts/CODEX_WORKER.md
reviews/ADH_Integrated_Plan/prompts/COMMON_CONTRACT.md
reviews/ADH_Integrated_Plan/prompts/VERIFIER_RUNBOOK.md
reviews/ADH_Integrated_Plan/registers/acceptance_scenarios.json
reviews/ADH_Integrated_Plan/registers/artifact_catalog.json
reviews/ADH_Integrated_Plan/registers/artifact_graph.json
reviews/ADH_Integrated_Plan/registers/authority_map.json
reviews/ADH_Integrated_Plan/registers/component_catalog.json
reviews/ADH_Integrated_Plan/registers/cross_contract_flows.json
reviews/ADH_Integrated_Plan/registers/document_contracts.json
reviews/ADH_Integrated_Plan/registers/document_guardrail_test_mapping.json
reviews/ADH_Integrated_Plan/registers/execution_status.json
reviews/ADH_Integrated_Plan/registers/generated_views.json
reviews/ADH_Integrated_Plan/registers/guard_applicability.json
reviews/ADH_Integrated_Plan/registers/guardrails.json
reviews/ADH_Integrated_Plan/registers/integrated_contracts.json
reviews/ADH_Integrated_Plan/registers/integration_traceability.json
reviews/ADH_Integrated_Plan/registers/legacy_addon_mapping.json
reviews/ADH_Integrated_Plan/registers/model_optimization_contracts.json
reviews/ADH_Integrated_Plan/registers/model_optimization_traceability.json
reviews/ADH_Integrated_Plan/registers/phases.json
reviews/ADH_Integrated_Plan/registers/prior_findings.json
reviews/ADH_Integrated_Plan/registers/requirement_traceability.json
reviews/ADH_Integrated_Plan/registers/revision_delta.json
reviews/ADH_Integrated_Plan/registers/runtime_requirements.json
reviews/ADH_Integrated_Plan/registers/skill_routes.json
reviews/ADH_Integrated_Plan/registers/source_check_mapping.json
reviews/ADH_Integrated_Plan/registers/structured_requirements.json
reviews/ADH_Integrated_Plan/registers/upstream_instruction_adaptation.json
reviews/ADH_Integrated_Plan/registers/v4_integration_checks.json
reviews/ADH_Integrated_Plan/registers/verification_cases.json
reviews/ADH_Integrated_Plan/registers/work_packages.json
reviews/ADH_Integrated_Plan/skill-pack/README.md
reviews/ADH_Integrated_Plan/skill-pack/skills/adh-design-choice/SKILL.md
reviews/ADH_Integrated_Plan/skill-pack/skills/adh-design-choice/references/workflow.md
reviews/ADH_Integrated_Plan/skill-pack/skills/adh-environment-repair/SKILL.md
reviews/ADH_Integrated_Plan/skill-pack/skills/adh-environment-repair/references/workflow.md
reviews/ADH_Integrated_Plan/skill-pack/skills/adh-failure-diagnosis/SKILL.md
reviews/ADH_Integrated_Plan/skill-pack/skills/adh-failure-diagnosis/references/workflow.md
reviews/ADH_Integrated_Plan/skill-pack/skills/adh-independent-review/SKILL.md
reviews/ADH_Integrated_Plan/skill-pack/skills/adh-independent-review/references/workflow.md
reviews/ADH_Integrated_Plan/skill-pack/skills/adh-integration-review/SKILL.md
reviews/ADH_Integrated_Plan/skill-pack/skills/adh-integration-review/references/workflow.md
reviews/ADH_Integrated_Plan/skill-pack/skills/adh-knowledge-context/SKILL.md
reviews/ADH_Integrated_Plan/skill-pack/skills/adh-knowledge-context/references/workflow.md
reviews/ADH_Integrated_Plan/skill-pack/skills/adh-quality-check/SKILL.md
reviews/ADH_Integrated_Plan/skill-pack/skills/adh-quality-check/references/workflow.md
reviews/ADH_Integrated_Plan/skill-pack/skills/adh-requirements/SKILL.md
reviews/ADH_Integrated_Plan/skill-pack/skills/adh-requirements/references/workflow.md
reviews/ADH_Integrated_Plan/skill-pack/skills/adh-schema-migration/SKILL.md
reviews/ADH_Integrated_Plan/skill-pack/skills/adh-schema-migration/references/workflow.md
reviews/ADH_Integrated_Plan/skill-pack/skills/adh-task-implementation/SKILL.md
reviews/ADH_Integrated_Plan/skill-pack/skills/adh-task-implementation/references/workflow.md
reviews/ADH_Integrated_Plan/sources/DOCUMENT_GUARDRAIL_SOURCES.md
reviews/ADH_Integrated_Plan/sources/MODEL_SOURCES.md
reviews/ADH_Integrated_Plan/sources/README.md
reviews/ADH_Integrated_Plan/sources/V4_SOURCES.md
reviews/ADH_Integrated_Plan/sources/api_v1_snapshot.json
reviews/ADH_Integrated_Plan/sources/document_guardrail_sources.json
reviews/ADH_Integrated_Plan/sources/dsh_sources.json
reviews/ADH_Integrated_Plan/sources/input_provenance.json
reviews/ADH_Integrated_Plan/sources/model_optimization_sources.json
reviews/ADH_Integrated_Plan/sources/prior_source_index.json
reviews/ADH_Integrated_Plan/sources/v2_integration_delta_history.json
reviews/ADH_Integrated_Plan/sources/v3_input_provenance.json
reviews/ADH_Integrated_Plan/sources/v4_input_provenance.json
reviews/ADH_Integrated_Plan/sources/v4_sources.json
reviews/ADH_Integrated_Plan/spec/00_DECISION.md
reviews/ADH_Integrated_Plan/spec/01_REQUIREMENTS.md
reviews/ADH_Integrated_Plan/spec/02_ARCHITECTURE.md
reviews/ADH_Integrated_Plan/spec/03_INTEGRATED_CONTRACTS.md
reviews/ADH_Integrated_Plan/spec/04_STATE_SEQUENCES.md
reviews/ADH_Integrated_Plan/spec/05_OPERATIONS_NFR.md
reviews/ADH_Integrated_Plan/spec/06_MODEL_OPTIMIZATION.md
reviews/ADH_Integrated_Plan/spec/07_MODEL_CONTRACTS.md
reviews/ADH_Integrated_Plan/spec/08_DOCUMENT_GRAPH.md
reviews/ADH_Integrated_Plan/spec/09_GUARDRAILS.md
reviews/ADH_Integrated_Plan/spec/10_CHANGE_AND_REGATE.md
reviews/ADH_Integrated_Plan/spec/11_DISTRIBUTION_AND_COMPOSITION.md
reviews/ADH_Integrated_Plan/spec/12_KNOWLEDGE_AND_CONTEXT.md
reviews/ADH_Integrated_Plan/spec/13_QUALITY_AND_TOOLCHAIN.md
reviews/ADH_Integrated_Plan/spec/14_LIFECYCLE_LEARNING_AND_REGATE.md
reviews/ADH_Integrated_Plan/traceability/DOCUMENT_AND_GUARDRAILS.md
reviews/ADH_Integrated_Plan/traceability/DOCUMENT_GRAPH.md
reviews/ADH_Integrated_Plan/traceability/GUARDRAIL_MATRIX.md
reviews/ADH_Integrated_Plan/traceability/INTEGRATION_PROVENANCE.md
reviews/ADH_Integrated_Plan/traceability/MODEL_OPTIMIZATION.md
reviews/ADH_Integrated_Plan/traceability/PRIOR_FINDINGS.md
reviews/ADH_Integrated_Plan/traceability/REQUIREMENTS.md
reviews/ADH_Integrated_Plan/traceability/V4_INTEGRATION_MAP.md
reviews/ADH_Integrated_Plan/verification/VERIFICATION_CATALOG.md
reviews/ADH_Integrated_Plan/verification/VERIFICATION_INDEX.md
reviews/ADH_Integrated_Plan/work_packages/WP00.md
reviews/ADH_Integrated_Plan/work_packages/WP01.md
reviews/ADH_Integrated_Plan/work_packages/WP02.md
reviews/ADH_Integrated_Plan/work_packages/WP03.md
reviews/ADH_Integrated_Plan/work_packages/WP04.md
reviews/ADH_Integrated_Plan/work_packages/WP05.md
reviews/ADH_Integrated_Plan/work_packages/WP06.md
reviews/ADH_Integrated_Plan/work_packages/WP07.md
reviews/ADH_Integrated_Plan/work_packages/WP08.md
reviews/ADH_Integrated_Plan/work_packages/WP09.md
reviews/ADH_Integrated_Plan/work_packages/WP10.md
reviews/ADH_Integrated_Plan/work_packages/WP11.md
reviews/ADH_Integrated_Plan/work_packages/WP12.md
reviews/ADH_Integrated_Plan/work_packages/WP13.md
reviews/ADH_Integrated_Plan/work_packages/WP14.md
reviews/ADH_Integrated_Plan/work_packages/WP15.md
reviews/ADH_Integrated_Plan/work_packages/WP16.md
reviews/ADH_Integrated_Plan/work_packages/WP17.md
reviews/ADH_Integrated_Plan/work_packages/WP18.md
reviews/ADH_Integrated_Plan/work_packages/WP19.md
reviews/ADH_Integrated_Plan/work_packages/WP20.md
reviews/ADH_Integrated_Plan/work_packages/WP21.md
reviews/ADH_Integrated_Plan/work_packages/WP22.md
reviews/ADH_Integrated_Plan/work_packages/WP23.md
reviews/ADH_Integrated_Plan/work_packages/WP24.md
reviews/ADH_Integrated_Plan/work_packages/WP25.md
reviews/ADH_Integrated_Plan/work_packages/WP26.md
reviews/ADH_Integrated_Plan/work_packages/WP27.md
reviews/ADH_Integrated_Plan/work_packages/WP28.md
reviews/ADH_Integrated_Plan/work_packages/WP29.md
reviews/ADH_Integrated_Plan/work_packages/WP30.md
reviews/ADH_Integrated_Plan/work_packages/WP31.md
ruff.toml
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
setup.sh
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
vendor/compactiondb/.claude/contextdb/config.json
vendor/compactiondb/.claude/contextdb/contextdb/cli.py
vendor/compactiondb/.claude/contextdb/contextdb/config.py
vendor/compactiondb/.claude/contextdb/contextdb/hook.py
vendor/compactiondb/.claude/contextdb/contextdb/normalize.py
vendor/compactiondb/.claude/contextdb/contextdb/paths.py
vendor/compactiondb/.claude/contextdb/contextdb/recovery.py
vendor/compactiondb/.claude/contextdb/contextdb/storage.py
vendor/compactiondb/.claude/contextdb/contextdb/util.py
vendor/compactiondb/CHANGELOG.md
vendor/compactiondb/MANIFEST.sha256
vendor/compactiondb/Makefile
vendor/compactiondb/README.md
vendor/compactiondb/install.py
vendor/compactiondb/snippets/CLAUDE_CONTEXTDB.md
vendor/compactiondb/tests/test_cli.py
vendor/compactiondb/tests/test_concurrency.py
vendor/compactiondb/tests/test_config.py
vendor/compactiondb/tests/test_hooks.py
vendor/compactiondb/tests/test_install.py
vendor/compactiondb/tests/test_memory.py
vendor/compactiondb/tests/test_paths.py
vendor/compactiondb/tests/test_probe.py
vendor/compactiondb/tests/test_recall.py
vendor/compactiondb/tests/test_recover_hook.py
vendor/compactiondb/tests/test_recovery.py
vendor/compactiondb/tests/test_redaction.py
vendor/compactiondb/tests/test_semantic.py
vendor/compactiondb/tests/test_spool.py
vendor/compactiondb/tests/test_storage.py

**Verifying Codex configuration support**
codex
対象タスクはネットワーク設定の描画に範囲を絞り、同一 UID の隔離やライブ強制は保証しないと明記しています。現在は、参照先の境界タスクが提供する前提と、描画された設定を Codex が実際に適用するかを分けて確認しています。読み取り専用のため、worklog やレビュー証跡は書き込みません。

exec
/bin/zsh -lc "rg -n 'D-024-17a|D-024-20|D-024-23' .orchestration/decisions.tsv; cat ~/.codex/skills/.system/openai-docs/SKILL.md" in ~/Workspace/dotfiles
exec
/bin/zsh -lc 'cat .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md' in ~/Workspace/dotfiles
exec
/bin/zsh -lc "sed -n '99,118p' .orchestration/plans/024-design-quality.md" in ~/Workspace/dotfiles
exec
/bin/zsh -lc "command -v codex; command -v git; command -v gh; rg -n 'sandbox_workspace_write|sandbox_mode|profile' home/dot_agents/agent-config.yaml | head -60; rg -n 'codex-worker-network|D-024-17a' .orchestration/acceptance .orchestration/validation -g '*.last.md' -g '*accept*'" in ~/Workspace/dotfiles
 succeeded in 166ms:
---
{
  "audit_findings": [],
  "dispatch": [
    "AGMSG-TASK v1 task_id=dotfiles-T133-worker-write-boundary-a01 round=1 repo=~/Workspace/dotfiles/.claude/worktrees/worker-e task_file=.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md task_sha256=bf5881da1c1c289ae3f4fb26cdd94b8a9d01496af0beab448d0cfa4a450c946b deadline=none done_signal=AGMSG-RESULT note=a010:plan-024-P1-15(the-worker-write-boundary;design-5.14-items-0-10;the-text-passed-its-9th-pre-dispatch-security-review);fresh-branch-from-origin/main-b22a5580;your-#420-branch-stays-untouched-for-a05-which-follows-this-merge;security-true:task-level-audit-and-security-review-on-the-final-head;the-operator-steps-named-in-the-text(managed-settings-sudo-install,worker-directory-login,permgate-codex-rule,make-update)are-not-yours;no-@codex-review-comment;single-gh/git-write-commands;one-pre-push-review-round-at-most"
  ],
  "format": 1,
  "head": null,
  "ledger": [],
  "pr": null,
  "searches": [],
  "task": "dotfiles-T133-worker-write-boundary-a01"
}
---

# Acceptance: dotfiles-T133-worker-write-boundary-a01 (plan 024 P1-15: the worker write boundary; D-024-17/19/20)

- text: review-profile design 03:18Z (prompt `.agents/worklog/orchestrator-glue/p115-a01-design-prompt.md`); checker OK; 14 files; not dispatched.
- 2026-10-19T03:24:11Z: C-80 review of the text (`.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-8bac9e5.md`): `Verdict: incorrect`, seven P1, one P2: (1) the gh wrapper forwards argv verbatim, so `gh repo clone … -- --config core.sshCommand=<exe>` runs worker code outside the sandbox → the wrapper allows an explicit subcommand list and refuses `--` passthrough and config-carrying forms; (2) a bash wrapper reads BASH_ENV before `env -i` (probe confirmed) → the wrapper is Python under an absolute `-I` interpreter path rendered from the trusted root; (3) project hooks execute the worktree's `.claude/hooks/contextdb_hook.py` through bare `python3` and the format hooks resolve tools through shims → worker seats run no project hooks (a factual check of the settings switch is pending with the Claude Code docs); (4) Codex workers share `.git/objects` and `.git/refs` writes (herdr-agents:439), so `origin/main` can be replaced after a fetch → design 5.14 item 8 now binds the committed ledger to the sha `git ls-remote origin refs/heads/main` returns (amended 03:2xZ); (5) `git ls-tree` enumeration needs the sanitized git environment; (6) the reviewer states Edit deny rules also enter the Bash sandbox configuration, which would block the orchestrator's sandboxed record writes under `.orchestration/**` → a factual check pending; (7) `failIfUnavailable: false` lets a seat run unsandboxed when Linux dependencies are missing → `true` for worker seats; (8) P2: symlink and case-alias identity tests missing. Five facts are being verified against the Claude Code documentation before the revision (excludedCommands matching, hooks switches and capture, Edit denies vs sandbox, failIfUnavailable, Edit rule scope and path forms).
- 2026-10-19T03:2xZ: Claude Code documentation facts (the claude-code-guide agent, code.claude.com/docs sandboxing, hooks, permissions pages): excludedCommands match the whole call and every chained sub-command must match; `disableAllHooks` exists but no project-only switch; hooks are not captured at start (a file watcher applies edits); Read/Edit deny rules merge into the sandbox filesystem configuration (so an Edit deny on `.orchestration/**` would block the orchestrator's sandboxed record writes); `failIfUnavailable` is fail-open by default; `Edit(path)` rules cover Write/MultiEdit/NotebookEdit, path forms `//abs`, `~/`, project-relative, deny wins. Consequence (5.14 item 1 amended): the Claude-seat boundary is a user-level PreToolUse hook keyed on the session cwd (worktree sessions: deny file-tool writes outside the cwd and inside `<cwd>/.claude/**`, `<cwd>/.mcp.json`), not Edit deny rules; `failIfUnavailable: true`; the gh wrapper is Python under an absolute `-I` interpreter with a subcommand allowlist; the committed ledger is read at the `git ls-remote` sha.
- 2026-10-19T03:35:17Z: the revised P1-15 text (prompt `p115-a01r-redesign-prompt.md`, 320 lines) installed: the Claude-seat boundary as the user-level PreToolUse hook `executable_worker-write-boundary.py` (session-cwd classification, canonical target checks), `failIfUnavailable: true`, the Python `-I` gh-trusted wrapper with a subcommand allowlist, the committed ledger at the ls-remote sha, per-seat caches; checker OK; the second C-80 review started 03:38Z.
- 2026-10-19T03:42:19Z: C-80 second review of the P1-15 text (`…-text-security-67415f5.md`): `Verdict: incorrect`, seven P1: the hook classifies by the mutable event cwd (a worker can cd out) → classify by CLAUDE_PROJECT_DIR; project hooks execute worker-writable scripts (`scripts/agent-stop-gate.sh`, `.claude/hooks/*.py`, PATH-resolved prettier with worker config) → hooks move out of the tracked `.claude/settings.json` into generated local settings, worker seats get a minimal trusted hook set; `python -I` does not neutralize LD_PRELOAD on Linux for the excluded wrapper → the outside-sandbox gh path is abandoned if gh can run inside the sandbox (CA trust experiment 03:4xZ); `gh pr create` runs git against the caller repository without the git controls → moot when gh is sandboxed; `refs/replace` redirects `git show <sha>` → `--no-replace-objects` (5.14 item 8); a worker's own sandboxed background child can swap a validated path before the unsandboxed file-tool write → stated as the residual it is; the hook lacks a failure policy → every error path exits 2 (fail-closed) with tests.
- 2026-10-19T03:45:06Z: probe from the orchestrator seat inside the Claude sandbox: `gh api repos/mryfmo/dotfiles --jq .name` → `dotfiles` (the sandbox proxy is a CONNECT proxy without TLS interception; the keychain token was read). The 2026-10-1x memory "gh inside the sandbox fails TLS" does not hold today. Consequence (5.14 item 10 amended, D-024-17 revised): worker seats run gh inside the sandbox, their excludedCommands are empty, the wrapper design is dropped (it cannot close LD_PRELOAD or argv passthrough); Codex seats get network inside their sandbox and permgate stops approving escapes (the permgate part is the operator's).
- 2026-10-19T03:53:27Z: the round-3 P1-15 text (prompt `p115-a01r2-redesign-prompt.md`, 333 lines) installed: CLAUDE_PROJECT_DIR classification, the orchestrator-only guard for project hooks (.claude/settings.json joins), no unsandboxed worker command (gh * leaves excludedCommands, Codex network inside the sandbox, the permgate codex rule as the operator step), --no-replace-objects at the ls-remote sha, fail-closed hook (exit 2), the worker race stated as a residual; checker OK; the third C-80 review started 03:54Z.
- 2026-10-19T03:58:10Z: C-80 third review of the P1-15 text (`…-text-security-ecc7ab5.md`): `Verdict: incorrect`, five P1: (1) a sandboxed worker can swap an allowed directory for a symlink after the hook validated, so the unsandboxed file tool overwrites a trusted path (the race is an escape, not a self-harm); (2) the writable object database defeats sha pinning: a replaced intermediate tree object redirects `git show <sha>:path` to an attacker blob (tree traversal does not re-hash intermediate objects); (3) hook descendants still resolve `python3` and `env bash` through shims (herdr-agent-state.sh, delivery scripts); (4) the Herdr unix socket in the worker sandbox lets a sandboxed client request host execution (`pane run`) through the server; (5) a hook timeout or kill is fail-open unless the per-hook `onFailure: "block"` (Claude Code ≥ 2.1.295) is set.
- design conclusion (03:5xZ, pending two fact checks): three text rounds show the host is not a security boundary between seats that share one OS user; the regime's hard boundary is GitHub (protected main, required checks, the merge by the orchestrator's identity), and inputs that must resist a malicious worker (the approval ledger, the gate's evidence of record) are read from GitHub at a sha through the API inside the sandbox, never from local files or the local object database; host-local controls target accidental and injected damage and are stated as such. The per-seat mechanism that makes worker-specific policy possible at all is a separate `CLAUDE_CONFIG_DIR` for worker seats (own settings: no excluded commands, no Herdr socket, minimal trusted hooks with absolute interpreters and `onFailure: block`, Edit denies on trusted paths, failIfUnavailable true); the facts (credentials with a second config dir; onFailure; sandbox per config dir; symlink resolution of file-tool paths) are being verified against the documentation.
- 2026-10-19T04:09Z: the round-4 P1-15 text (prompt `p115-a01r3-redesign-prompt.md`, 373 lines) installed: the 5.14 item 0 threat model opens the Goal; Claude worker seats under CLAUDE_CONFIG_DIR=~/.claude-worker rendered from a new template (Edit denies on trusted paths with symlink coverage, no exclusions, no Herdr socket, restricted allowWrite, failIfUnavailable, minimal hooks with onFailure block); project hooks behind the orchestrator-only guard; the ledger read through the GitHub API at the ls-remote sha; hook descendants with absolute interpreters (herdr-agent-state.sh joins); checker OK; the fourth C-80 review started 04:12Z.
- 2026-10-19T04:15:38Z: C-80 fourth review of the P1-15 text (`…-text-security-8d42532.md`): `Verdict: incorrect`, six P1: (1) workers share the orchestrator's gh credential, so a worker can merge through the API inside the sandbox (GitHub cannot distinguish seats) → D-024-22: a dedicated worker GitHub identity outside the ruleset bypass list (operator step); (2) the deny inventory from `git ls-tree` trusts the writable object store (replace refs) → a static rendered list; (3) the orchestrator cache `.agents/worklog/uv-cache` is missing from the inventory → listed; (4) `~/.agents/**` deny conflicts with the agmsg store writes → a narrower list; (5) linked-worktree sessions load the main checkout's `.claude/settings.local.json` (documented), so worktree-local worker settings are not read and the orchestrator's local hooks run in worker sessions → the guard covers them and worker hooks live in the worker config dir; (6) upstream agmsg scripts carry `/usr/bin/env bash` shebangs → the hook command pins PATH=/usr/bin:/bin. Design 5.14 items 0 and 1 amended; round 5 of the text follows.
- 2026-10-19T04:22:08Z: the round-5 P1-15 text (prompt `p115-a01r4-redesign-prompt.md`, 439 lines) installed: the worker gh identity (D-024-22) as a Files item with the worker gh configuration directory and the operator steps; a static `trusted_paths` inventory in the manifest; narrow home-path denies that leave the agmsg store writable; worker hooks in the worker configuration directory because linked-worktree sessions load the main checkout's settings.local.json; the orchestrator's local hooks behind the guard; PATH=/usr/bin:/bin pinned on every hook command; "reduces" wording where item 0 applies; checker OK; the fifth C-80 review started 04:22Z.
- 2026-10-19T04:25:41Z: C-80 fifth review (`…-text-security-08e6ac7.md`): `Verdict: incorrect`, three P1 (converging from seven): (1) GH_CONFIG_DIR separates configuration, not Keychain access: gh keys credentials by host and user, so a same-UID worker reads the orchestrator token → D-024-23: credential separation needs a separate OS user (future P1-16); the GitHub boundary is detection (regime main-push check), stated as such; (2) the agmsg store every seat writes also selects executables: a team's `drivers.partition` path traversal makes storage.sh source a planted file during unsandboxed delivery → an upstream agmsg hardening task (row recorded) and a stated residual; (3) sandbox restrictions in user settings are overridable by project/local settings → the enforcement scope is managed settings (operator `sudo` step) and the worker denies cover `<worktree>/.claude/**` and `.mcp.json`. Design 5.14 items 0 and 1 amended; round 6 follows.

## Owned by dotfiles-T133-agmsg-hardening-a01 (a task to be written; upstream agmsg)

- `text-security:08e6ac7:2` store-driver-traversal: `~/.agents/skills/agmsg/scripts/lib/storage.sh:196` resolves a team config `drivers.partition` value as a built-in driver path and sources it during delivery; a worker that writes the shared store can plant `../../../db/payload` and have the orchestrator's unsandboxed delivery hook source it; the fix validates the driver name against the installed drivers directory (an allowlisted basename, no path separators) before sourcing, with a red-then-green test; reported upstream.
- 2026-10-19T04:32:56Z: the round-6 P1-15 text (prompt `p115-a01r5-redesign-prompt.md`, 501 lines) installed: the dedicated-identity item removed (D-024-23: detection, not prevention); the agmsg-store driver residual row; managed settings as the sandbox enforcement scope (a rendered staging file, `make install-managed-settings` prints the operator's sudo command); worker denies on `<worktree>/.claude/**` and `.mcp.json`; checker OK; the sixth C-80 review started 04:34Z.
- 2026-10-19T04:37:39Z: C-80 sixth review (`…-text-security-5cbbc03.md`): `Verdict: incorrect`, three P1, all local: (1) a pinned PATH does not neutralize an inherited BASH_ENV (probe) → hook commands start with `/usr/bin/env -i PATH=… HOME=…`; (2) the agmsg store's `db/trusted-plugins` and `plugins/partition/shared.sh` let a worker authorize a replacement plugin storage.sh sources → the worker denies cover both paths and the agmsg-hardening row widens; (3) the managed-settings path differs on Linux (`/etc/claude-code/managed-settings.json`) → the Makefile target selects the OS path. Design 5.14 amended; round 7 follows.
- `text-security:5cbbc03:2` store-plugin-trust (agmsg-hardening-a01, widening the first row): storage.sh:208-228 selects and sources a plugin a team's `db/trusted-plugins` authorizes; a worker that writes the store authorizes `plugins/partition/shared.sh`; the fix refuses plugins not installed under the skill's read-only plugins directory with a trust list outside the shared store.
- 2026-10-19T04:43:45Z: the round-7 P1-15 text (prompt `p115-a01r6-redesign-prompt.md`, 501 lines; the three local changes only: env -i on every hook command, the agmsg plugins and trusted-plugins denies with the store kept writable, the OS-selected managed-settings path) installed; checker OK; the seventh C-80 review started 04:44Z.
- 2026-10-19T04:46Z: C-80 seventh review (`…-text-security-519afd7.md`): `Verdict: incorrect`, one P1 and one P2, both consequences of the env -i decision: `env -i` strips CLAUDE_PROJECT_DIR, which the guard needs (every hook would exit 0 without running) → the hook command re-exports the launch identity explicitly after env -i; the pinned PATH removes ruff, prettier and terminal-browser from the orchestrator's formatter and map hooks → in orchestrator sessions the guard runs them with a rendered PATH of the trusted root's absolute tool directories. Round 8 (local) follows.
- 2026-10-19T04:5xZ: round-8 P1-15 text installed (env -i with the launch identity re-exported; role-specific PATH in the guard); checker OK; the eighth C-80 review started.
- 2026-10-19T05:41Z: C-80 ninth review (`…-text-security-435275a.md`): `Verdict: correct`. The text is dispatched to a010 (wJ:p5, worker-e; a012 is on its #412 revise) at 05:4xZ with the counters and the review history pasted in its Checks block; a05 follows on the same seat after this merge.
- 2026-10-19T05:45Z: PING to a010: design 5.14 and D-024-16..23 exist only in the orchestrator working copy until the next records PR; the worker reads them at the absolute path of the main checkout (C-86 recorded).
- 2026-10-19T05:46:28Z: a010 `status=running`: branch `tools/worker-write-boundary-a01` from 205fe85c (origin/main had advanced); the #420 and #427 branches preserved; reading callers and adding the red tests.
- 2026-10-19T05:50:16Z: a010 `status=running question=1`: the Check requires `make format` pass while the clean base 205fe85c fails on 12 out-of-scope files (the known inherited set). Interpretation note 1 (05:5xZ, no amendment): the sibling texts' clause applies (an inherited formatting failure is reproduced against the unchanged base and disclosed with exact output and per-file exit statuses; no out-of-scope repair); the task's own files pass the make format flags. INV-6: questions 1.
- 2026-10-19T06:01:06Z: a010 `status=running question=2`: the tracked `.claude/settings.json` is not a chezmoi template, so literal rendered HOME/anchor/interpreter paths would bind it to this macOS host; it proposes HOME-relative paths in the tracked file with the host-specific absolute paths only inside the rendered guard, and CLAUDE_PROJECT_DIR never selecting an executable. The reading is right and the text is wrong. This is the second question PONG (the first 05:50:16Z) → INV-6 S2: `status=withdrawn` 06:1xZ (branch, 8 green tests, fixtures and evidence kept); the reset a02 = the a01 text with both clarifications folded in and the Codex `network_access` item removed (routing: a Codex seat edits no Codex-boundary source; that item becomes a small Claude-seat task), redesigned by the review profile and passed through C-80 before dispatch.
- correction (2026-10-19T06:13Z): the S2 line above was premature: `regime-counters.sh --history-only` counts `status=question` PONGs and reports questions=0, because a010 sent its two questions as `status=running question=N` (a Codex-seat form deviation of the PONG contract, recorded as a conformance note; C-87: the counter also reads a `question=` field). By the counter INV-6 S2 did not fire; no withdrawal was sent (the send was guarded on the counter). Both questions are answered by interpretation notes (note 1 at 05:5xZ; note 2 at 06:13Z: $HOME-relative paths in the tracked file, host-specific paths only in the rendered guard) and amendment 1 folds both into the text and removes the Codex network_access item (routing); the running redesign output becomes that amendment text (same task id, no reset).
- 2026-10-19T06:19:54Z: a010 `status=blocked` on an optional progress inspection only (`ps -axo … | rg …` refused by its Codex sandbox: operation not permitted); no retry; the authorized unit run continues and is collected through its session; implementation per note 2 continues after that run. No action: an optional inspection outside the sandbox is correctly refused and not escalated (Worker Playbook step 4).
- 2026-10-19T06:23Z: the amendment-1 text (the review-profile a02 output re-targeted to a01: the inherited make format clause, the portable tracked settings.json with host paths only in the rendered guard, the Codex network_access item removed to the Claude-seat task dotfiles-T133-codex-worker-network-a01) installed; checker OK; its C-80 review started 06:23Z; dispatch to a010 on correct.
- 2026-10-19T06:25:59Z: C-80 of the amendment-1 text (`…-text-security-f1b862c.md`): one P2 (the guard source is a plain `executable_` file, which chezmoi copies without template expansion, so the per-host paths cannot be rendered) → the source becomes `executable_orchestrator-only.sh.tmpl` with the rendering sentence and the render test stated; the review runs again before dispatch.
- 2026-10-19T06:26:42Z: a010 `status=blocked` on the required CI doc test: tests/unit/test_agmsg_orchestration_docs.py:200-201 asserts the step 4 sentence this task rewrites and is outside allowed_files. Amendment 1 (in its C-80 review) gains the module for that one assertion with a threat row; C-78: PR #427 (P1-8, the same seat) edits the module and merges first; this PR rebases. PING sent 06:2xZ.

 succeeded in 250ms:
## 5.14 信頼ホスト実行契約（trusted-host execution contract、D-024-18）

orchestrator 側の仕組み（merge gate、integrate-merge、orch-gate、dispositions、audit-pool、verdict、chain）は、同じホスト上で同じ UID の worker プロセスと共存する。2026-10-19 の C-80 審査（a05、dispositions-a02、audit-pool-a01 の 3 文、計 19 件の P1）は、どの文も同じ前提を書かず同じ穴を持つことを示した。以後、`security: true` の orchestrator 側タスク文は本節を参照で適用し、本節の各項目に対応する threat 行を持つ。文ごとに言い換えない。

1. **書き込み境界（前提 6、ランタイム別に正直に）** Claude worker 席は専用の設定ディレクトリ `CLAUDE_CONFIG_DIR=~/.claude-worker`（chezmoi が描画、operator が一度 login）で起動し、orchestrator の `~/.claude` と設定を共有しない。worker 設定：除外コマンド無し、Herdr socket 無し、sandbox の allowWrite は自席 worktree と agmsg store と席別キャッシュだけ、`failIfUnavailable: true`、信頼パス（anchored checkout の `.claude/worktrees/` 以外、`~/.agents`、`~/.claude*`、`~/.local`、`~/.config`）への Edit deny（公式文書：file tool の permission 検査は要求パスと symlink 解決後のパスの両方に deny を適用し、symlink そのものへの書き込みは拒否する）、sandbox の強制範囲はユーザー設定ではなく **managed settings**（`/Library/Application Support/ClaudeCode/managed-settings.json`、公式文書 "Repository settings under an admin-required sandbox"：project/local 設定は sandbox を無効化したり除外・socket を足したりできない）に置く。chezmoi は user ではこのファイルを書けないので、描画した内容を操作者が `sudo` で一度配置する（操作者手順）。worker 設定は worktree 自身の `.claude/**` と `.mcp.json` への Edit deny（`//<anchored>/.claude/worktrees/*/.claude/**`）を持つ（Bash 側は sandbox 既定の settings/hooks の denyWithinAllow）。agmsg store（全席が書く）から配送 hook が driver や plugin を source する上流の経路（storage.sh の `drivers.partition` traversal、`db/trusted-plugins` と `plugins/partition/shared.sh` による差し替え承認）は別タスク（agmsg hardening）の行で、worker 設定は `~/.agents/skills/agmsg/plugins/**` と `~/.agents/skills/agmsg/db/trusted-plugins` への書き込みを deny し（Edit deny は sandbox の deny にも合流する）、hook 側は store 由来の設定値を検証するまで残余と書く。managed settings の配置先は OS で異なる（macOS `/Library/Application Support/ClaudeCode/managed-settings.json`、Linux `/etc/claude-code/managed-settings.json`）。hook は agmsg 配送だけを、hook コマンドを `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<home> …` で始めて（`BASH_ENV` などの継承環境を bash 起動前に消す；PATH 固定だけでは BASH_ENV が先に走る）絶対パスのインタプリタで呼び（上流の agmsg スクリプトは `/usr/bin/env bash` の shebang を持つので、hook 実行環境の PATH が shim を含まないことで束縛する）、各 hook に `onFailure: "block"`。公式文書：linked worktree の session は **main checkout の `.claude/settings.local.json` を読む**ので、worker 向けの hook を worktree の settings.local.json に書いても読まれず、逆に orchestrator の local hooks が worker session でも走る。したがって orchestrator 側の local hooks も guard 経由にし、worker 側の hook は worker config dir の settings に置く。Edit deny の一覧は `git ls-tree` ではなく描画時の静的一覧（manifest に列挙、`.agents/worklog/**` と `.agents/worklog/uv-cache/**` を含む）とし、`~/.agents/**` の全面 deny は agmsg store の書き込みと矛盾するので、`~/.agents/agent-config.yaml`、`~/.agents/skills/**/scripts/**`、`~/.agents/model-profiles.env` などストア以外を列挙する。公式文書で確認した事実（2026-10-19）：`Edit(path)` の deny は Write/MultiEdit/NotebookEdit にも効き、deny → ask → allow の順で最初の一致が決まる；ただし Read/Edit の deny は **Bash sandbox の設定にも合流する**（"Paths and domains from both sandbox settings and permission rules are merged into the final sandbox configuration"）ので、ユーザー設定（全席共有）に `.orchestration/**` の Edit deny を書くと orchestrator の Bash による記録書き込みも止まる。hook は起動時に固定されず、設定ファイルの編集は file watcher が即座に反映する。`sandbox.failIfUnavailable` の既定は fail-open（依存が無ければ sandbox 無しで実行）。したがって Claude 席の境界は Edit deny 規則ではなく、**ユーザーレベルの PreToolUse hook**（`~/.claude/hooks/worker-write-boundary`、chezmoi が描画、`/bin/sh` または絶対パスの `python3 -I`）で作る：cwd の realpath が `<anchored>/.claude/worktrees/` 配下の session では、Write/Edit/MultiEdit/NotebookEdit の対象が cwd の外、または `<cwd>/.claude/**`・`<cwd>/.mcp.json` のとき `permissionDecision: deny` を返す。Bash 側は sandbox の既定 `denyWithinAllow`（settings、hooks）と `allowWrite`（自席 worktree）が担う。`failIfUnavailable: true` を全席に置く。 Codex 席は sandbox（workspace-write）がツールの書き込み全部を自席の worktree と列挙パスに限る。Claude 席は Seatbelt sandbox が Bash を限るだけで、Write/Edit/MultiEdit/NotebookEdit、hook、MCP プロセスは sandbox 外で動き、permission policy（permgate の決定論ポリシー）が path で拒否しない限り anchored checkout や `~/.agents` にも書ける（2026-10-19 時点、描画済み設定にその deny は無い）。したがって前提 6 は「Codex 席は成立、Claude 席は P1-15 が描画設定に Edit の path deny を入れるまで残余」と書く。P1-15 以前に「worker は信頼ルートに書けない」と書く文は誤りで、C-80 が拒否する。P1-15 が入るまで、承認の出所は項目 8 の「コミット済み台帳」で守る。書き込みは自席の worktree（`.claude/worktrees/<name>`）、scratch、列挙されたツールキャッシュに限る。anchored checkout（`.claude/worktrees/` 以外）、`~/.agents/agent-config.yaml`、`~/.claude/hooks`、信頼ルートのバイナリ、orchestrator の証跡・スナップショット・lock は worker から書けない。render テストが描画後の deny を検証する。残余は「どの席 sandbox にも属さない同一 UID プロセス」と、Worker Playbook step 4 が sandbox 外に出す少数のコマンド（gh）。後者は D-024-17（P1-15）で絶対パスの実行体に束縛する。
2. **無害化した環境を最初に** 最初の処理として `env -i` に入り、PATH は信頼ルートで解決した絶対バイナリへのリンクだけの私設ディレクトリ（shims、空、相対は拒否）。git は毎回 `GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null -c core.hooksPath=/dev/null -c core.fsmonitor=false -c protocol.allow=never -c protocol.https.allow=always` と明示 `-C`（https だけ許す。`protocol.allow=never` 単独は必要な fetch を止める）。 検査の読み取りは `GIT_NO_LAZY_FETCH=1` で部分クローンの遅延 fetch（checkout 設定の credential.helper を起動しうる）を止め、`-c submodule.recurse=false --ignore-submodules=all` で submodule 内の status/diff（submodule 自身の設定が filter を有効化しうる）を止める。`.gitmodules` を持つ checkout は検査対象として拒否する。 `-C` は作業木を束縛しないので（repo-local の `core.worktree` が読み先を checkout 外へ向けられる）、git は `--git-dir=<checkout>/.git --work-tree=<checkout>` を明示し、`git rev-parse --show-toplevel` の realpath が checkout と一致しないときは拒否する。 premise や検査の「コマンド実行」は、固定語彙の読み取り専用プローブ（`git rev-parse <ref>`、`test -e <path>`、`grep -c <pattern> <file>` のように検査器自身が解釈する形）だけを許し、任意のシェル文字列は実行しない（本文のハッシュはコマンド文を認証するだけで、`python -I scripts/x.py` のファイル被演算子や `source ./x.sh` の中身は認証しない）。diff と show は `--no-ext-diff --no-textconv` と `-c core.attributesFile=/dev/null -c core.sshCommand=false` を付け、PR 側の `.gitattributes`（external diff、textconv、filter）が検査内容や実行物を変えないようにする。Python は `-I`。PATH 探索で実行するものは無い。
3. **信頼パスの境界検査** 仕組みが信頼するパス（スクリプト、台帳、証跡、worktree、lock、出力先）は realpath で解決し、`.claude/worktrees/` または manifest の worker ルート配下なら拒否（ask/hold）。symlink 構成要素は解決後に比較し、大小文字を区別しないファイルシステムでは同一性比較を大小文字非依存で行う。
4. **検証したものを実行し、検証した内容を渡す** 検証した実行体はその realpath で実行する（再探索しない）。検証したファイル内容は信頼ルート配下のスナップショット（0600、一意名）として渡し、使用直前に sha256 を再照合する。判断に読んだ証跡は sha256 を出力に記録する。
5. **出力と予約の同一性** 名前には 40 桁の head を使う（7 桁で衝突させない）。lock は信頼ルート配下の固定 inode に O_EXCL で作り、置換を inode 比較で検出する。物理スロット 1 つに lock 1 つ。
6. **正直な残余** 境界だけが緩和するリスクを `closed` と書かない。各文は残余を 1 行で明記する。
0. **脅威モデル（D-024-21）** 席は同じ OS ユーザで動き、ホストは席間の信頼境界ではない（同一 UID のプロセスは symlink 差し替え、共有 `.git` の object 差し替え、hook の子プロセス、Herdr socket 経由の host 実行で、ホスト内のどの検査も迂回できる）。regime の硬い境界は GitHub（保護された main、必須チェック、orchestrator の identity によるマージ）。ただしこの境界は **worker 席が orchestrator の GitHub 資格情報を共有しない**ときだけ成立する（D-024-22：worker 席は専用の GitHub identity（別アカウントまたは App のトークン）で `gh` に login し、ruleset の bypass 一覧に入らない。orchestrator の keychain トークンを worker の config dir に持ち込まない。identity が分かれるまで「GitHub が境界」は未成立と書く）。**同一 macOS ユーザでは資格情報は分離できない**（gh は keychain の項目を host/user で引き、同じ UID の gh は orchestrator のトークンを読める。`GH_CONFIG_DIR` は設定を分けるだけ）。防止には worker 席を別の OS ユーザ（または別ホスト）で動かすしかなく、それは D-024-23 の将来項目（P1-16、操作者の判断）。それまで GitHub 境界は **検知**で守る：記録は boundary の記録 PR まで main に無いので、検知は次の記録 PR の regime ジョブで行う（`.orchestration/acceptance/**` に触れる PR で、前回 boundary 以降の main の各マージ commit に、gate 通過の証跡を持つ受け入れ記録が対応することを検査し、無ければその PR を失敗させる；P1-11 owner a02 の行 `ci:detection:1`）。main push 時点の検知は記録が無いので不可能であり、文は「次の記録 PR で検知、防止ではない」と書く。悪意ある worker に耐えるべき入力（承認台帳、gate が読む証跡 of record）は GitHub から sha 指定で API 経由（sandbox 内）に読み、ローカルファイルやローカル object database からは読まない。ホスト内の制御（本節 1〜10）は事故と prompt injection による損害の抑制であり、文はそう書く。
8. **承認はコミット済み台帳から読む** permission の決定行（`scope=permission approved_by=user diff_sha256=…`）は anchored checkout の作業コピーではなく、コミット済みの台帳から読む。読み方は `git ls-remote origin refs/heads/main` が返す commit sha を取り、GitHub API（`gh api repos/<owner>/<repo>/contents/.orchestration/decisions.tsv?ref=<sha>`、sandbox 内）でその sha の内容を取得する。ローカルの `git show` は共有 object database が書けるため中間 tree の差し替えで偽物を返しうる（第 3 回審査の所見 2）（ローカルの ref 名 `origin/main` は経由しない。`refs/replace/` も書けるので replacement を無効にする。Codex worker は `.git/objects` と `.git/refs` に書けるので ref は差し替えられるが、sha で指した object は内容アドレスで偽造できない）。作業コピーの行は提案で、記録 PR が main にマージされて初めて承認になる（PR の承認は操作者の操作）。偽造には main へのマージが要る。
9. **私設キャッシュ** orchestrator 側の実行は worker と共有するキャッシュ（`~/.cache/uv`、`~/.local/share/uv`、mise）から実行可能物を読まない。`UV_CACHE_DIR` を anchored checkout 配下（`.agents/worklog/uv-cache`、gitignored、worker 書き込み不可）に固定し、`uv run --no-config --no-project --offline --python <信頼ルートの絶対パスのインタプリタ>` で起動する（`--no-config` で uv の設定探索を止め、`--python` の絶対パスで cwd や親の `.venv` の発見を止める；敵対的な `.venv` と `uv.toml` を置いた fixture で検証）。hook は uv を使わず jq と python 標準ライブラリだけで動く。
10. **worker は sandbox 外でコマンドを実行しない（D-024-17 の改訂）** 2026-10-19T03:45Z の実測で `gh api` は Claude sandbox の中から成功した（sandbox の proxy は CONNECT 型で TLS を終端しない；keychain のトークンも読めた）。worker 席の除外コマンドは空にし、gh も git push も sandbox 内の proxy 経由で実行する。Codex 席は `sandbox_workspace_write.network_access = true` で同じ状態にし、permgate の codex ポリシーは sandbox 外への escape を承認しない（permgate の変更は操作者の手順）。wrapper 方式（絶対パス、env -i、固定 GH_CONFIG_DIR）は LD_PRELOAD と引数転送（`gh repo clone -- --config`）を閉じられないので採らない。
7. **検証** threat_table は本節の項目 1〜10 に 1 行ずつ対応させる（参照だけでは足りない）。共通テスト補助 `tests/unit/trusted_exec_contract.py`（P1-6 で作る）を使い、仕組みごとに 4 つの red→green テストを持つ：PATH 先頭の shim が実行されない、植え付けた GIT_* と git 設定が効かない、worker ルート配下の信頼パスが拒否される、検証後に差し替えたファイルが消費側に届かない。

 succeeded in 388ms:
66:D-024-20	2026-10-19T03:1xZ	P1-15 (the worker write boundary: deny rules for the Claude file tools on every trusted path outside the seat worktree, hooks and MCP locked, per-seat caches, the gh wrapper of D-024-17) is implemented before and as the dispatch prerequisite (after:) of every orchestrator-side security: true task (P1-14 a05, P1-10 a02, audit-pool-a02, P1-6); the orchestrator review worktree moves out of .claude/worktrees/ (design 5.14 item 3)	the C-80 reviews of 2026-10-19 (a05 twice, dispositions-a02 twice, audit-pool-a01) all reduce to the unstated Claude-seat boundary; hardening texts dispatched before it carry false closed rows	default under the autonomy directive, reported 2026-10-19 12:1x JST; scope=design	applied
69:D-024-23	2026-10-19T04:2xZ	credential separation between the orchestrator and worker seats is not achievable on one macOS user (gh keys Keychain items by host and user; any same-UID gh reads the orchestrator token; GH_CONFIG_DIR separates configuration only); prevention needs worker seats under a dedicated OS user or host (a future P1-16, the operator decides whether to pursue it); until then the GitHub boundary is detection: the regime CI main-push run flags a merge without acceptance and gate evidence, and every text says "detection, not prevention"	the fifth C-80 review of the P1-15 text (04:25Z) traced gh credential selection in the gh source	default under the autonomy directive, reported 2026-10-19 13:3x JST; scope=design	recorded
71:D-024-17a	2026-10-19T06:0xZ	amendment of D-024-17: the wrapper design is dropped (design 5.14 item 10): worker seats run no command outside the sandbox at all (gh inside the sandbox, Codex network inside its sandbox, the permgate codex rule stops approving escapes)	the probe of 03:45Z (gh works inside the sandbox) and the C-80 reviews that showed the wrapper cannot close LD_PRELOAD or argv passthrough	recorded; scope=design	supersedes-the-wrapper-wording
72:D-024-22a	2026-10-19T06:0xZ	amendment of D-024-22: the dedicated worker GitHub identity is not pursued on this host (D-024-23: same-UID gh reads the orchestrator keychain token); result becomes not-applicable-on-one-macos-user	the fifth C-80 review of the P1-15 text	recorded; scope=design	not-applicable-on-one-macos-user
---
name: "openai-docs"
description: "Use for Codex models/pricing, scheduled tasks, skills, settings, setup, troubleshooting, customization, automations, and self-knowledge—including 'you,' 'your,' 'this app,' or 'this coding agent' when they refer to Codex—and for OpenAI APIs/products and ChatGPT Work. Also use for model choice/migration, prompting, SDKs, Responses, Realtime, agents, evals, and Chat/Work/Codex comparisons. Do not use for generic app/software tasks that merely mention Codex."
metadata:
  short-description: "Codex models/pricing, scheduled tasks, skills, settings, setup, troubleshooting, and self-knowledge; OpenAI APIs and ChatGPT Work. 'You'/'this app' means Codex only."
---

# OpenAI Docs

Provide current, cited OpenAI product, API, model, and Codex guidance. Read zero or one primary reference.

**First substantive action:** Search the user's exact requested official OpenAI documentation topic and any explicitly named model using a concise, topic-specific query of 2-6 essential terms. When an already-available direct official documentation search and page-retrieval capability is present, use it first: search, then fetch or open the matching official page before general web search. Otherwise, immediately use official-domain web search, then actually open or fetch the relevant official page. Complete this source order before reading a reference, inspecting local or repository files, running a Codex manual or model resolver, drafting a plan, or answering from memory. Use the actual fetched page, not a search snippet or an unopened link. If one official search or page does not establish the answer, search another appropriate official domain and actually open or fetch the result. Preserve the exact requested model; never substitute a newer model.

**Only exception:** An explicitly requested, genuinely broad, cross-topic Codex setup, orientation, or system-map synthesis may use the manual first when shell execution and an allowed temporary cache are available. A specific Codex feature, setting, command, error, model, or requested citation remains docs-first. Mixed Chat/Work/Codex comparisons are official documentation questions, not manual-first Codex requests.

For generic software tasks, answer the software task directly. OpenAI implementation, debugging, SDK, API, prompting, agent, and eval requests are not generic.

For a straightforward factual or citation-only request, follow the source order and do not read a route reference. This includes straightforward API facts, ChatGPT Work or mixed Chat/Work/Codex comparisons, model tiers, aliases, Pro mode, reasoning settings, factual migration baselines, and narrow Codex facts. Prioritize `learn.chatgpt.com` for ChatGPT Work.

## Choose one primary route

Use the first matching route, and read its reference only when the requested task needs that specialized workflow:

- **Explicitly requested local documentation integration:** Read [integration guidance](references/mcp-diagnostics.md) only when the user explicitly requests that local integration.
- **Model migration, upgrades, or model-specific prompting:** Read [model-migration.md](references/model-migration.md) for actual migration planning, implementation, dynamic target resolution, or prompt changes. Preserve an explicitly requested target.
- **Model selection and comparisons:** Read [model-selection.md](references/model-selection.md) only when nuanced current, latest, default, cost, latency, quality, or modality tradeoffs need more guidance. Do not run a migration resolver for selection alone.
- **Product, API, ChatGPT Work, and mixed Chat/Work/Codex documentation:** Read [official-docs.md](references/official-docs.md) only when fetched official pages leave source selection, API schemas, or the requested implementation unresolved. This route is not manual-first.
- **Explicitly broad Codex setup, orientation, or cross-topic synthesis:** Read [codex-self-knowledge.md](references/codex-self-knowledge.md) when the eligible Codex manual or deeper Codex procedures are needed.

Read at most one primary reference. Do not open every route, bundled model guide, or helper script. Read a supporting reference or run a helper only when the chosen workflow demonstrably needs it.

## Source and execution boundaries

- Search, open, fetch, and cite only `developers.openai.com`, `platform.openai.com`, and `learn.chatgpt.com`. Cite the page that supports the claim. State uncertainty when official sources do not establish pricing, availability, account access, limits, or behavior.
- Preserve an explicitly requested model for selection, migration, and prompting. Resolve an unspecified latest or current migration target only after searching and fetching current official guidance.
- Use `references/latest-model.md` only as a disclosed fallback after current official model guidance does not answer the question. Read `references/upgrading-to-gpt-6-astra.md` only for an actual, requested GPT-6 migration; read `references/prompting-guide.md` only for requested prompting work.
- Before building, running, editing, debugging, or testing an API-backed app or tool, use `openai-platform-api-key` first when available. Documentation, conceptual examples, model selection, and read-only guidance do not require an API key.
- Say "OpenAI Docs" or "official OpenAI documentation" in user-facing answers. Keep exact official citations and examples concise.

 exited 1 in 394ms:
~/.local/share/mise/shims/codex
/opt/homebrew/bin/git
~/.local/share/mise/shims/gh
12:# - Keep Codex writable roots for shared agmsg state under codex.sandbox_workspace_write.
26:# settings, per-profile Codex config files (~/.codex/<name>.config.toml), and
27:# ~/.agents/model-profiles.env for launchers. Keep main-session models fixed
29:model_profiles:
41:    # INV-7: the Claude review profile is the same model and effort as deep.
65:      sandbox_mode: read-only
67:interactive_profile: deep
69:# ~/.agents/model-profiles.env as HERDR_AGENTS_WORKER_KIND; an explicit
74:# ~/.agents/model-profiles.env as HERDR_AGENTS_ORCHESTRATOR_KIND; an explicit
77:# Worker pane model profile for herdr-agents. Renders into
78:# ~/.agents/model-profiles.env as HERDR_AGENTS_WORKER_PROFILE; an explicit
80:worker_profile: standard
82:# repository root. Renders into ~/.agents/model-profiles.env as
96:  sandbox_mode: workspace-write
114:  sandbox_workspace_write:
147:    # profiles' notify entries still carry each turn's assistant message.
194:  # interactive profile maps to Sonnet or below.
267:  # Claude Code Bash sandbox, the counterpart of codex.sandbox_workspace_write:
270:  # codex.sandbox_workspace_write.writable_roots so both agents share one agmsg
274:  # AppArmor profile (install/ubuntu/common/apparmor_userns.sh) lets bwrap

**Verifying budget and tools**
exec
/bin/zsh -lc "ls -l ~/.local/share/mise/shims/codex; rg --files ~/.local/share/mise/installs | rg '(codex.*/(config.schema.json|config/profile.rs|config/mod.rs|config.md|package.json)|codex["'^/]*$)'"' | head -45" in ~/Workspace/dotfiles
 succeeded in 181ms:
lrwxr-xr-x  1 a0004262  staff  31 Sep 30 13:43 ~/.local/share/mise/shims/codex -> ~/.local/bin/mise
~/.local/share/mise/installs/npm-openai-codex/0.160.0/lib/node_modules/@openai/codex/package.json
~/.local/share/mise/installs/npm-openai-codex/0.160.0/lib/node_modules/@openai/codex/node_modules/@openai/codex-darwin-arm64/vendor/aarch64-apple-darwin/codex-package.json
~/.local/share/mise/installs/npm-openai-codex/0.160.0/lib/node_modules/@openai/codex/node_modules/@openai/codex-darwin-arm64/vendor/aarch64-apple-darwin/codex-resources/voice/bin/codex-voice-host
~/.local/share/mise/installs/npm-openai-codex/0.160.0/lib/node_modules/@openai/codex/node_modules/@openai/codex-darwin-arm64/vendor/aarch64-apple-darwin/bin/codex-code-mode-host
~/.local/share/mise/installs/npm-openai-codex/0.160.0/lib/node_modules/@openai/codex/node_modules/@openai/codex-darwin-arm64/vendor/aarch64-apple-darwin/bin/codex
~/.local/share/mise/installs/npm-openai-codex/0.160.0/lib/node_modules/@openai/codex/node_modules/@openai/codex-darwin-arm64/package.json
~/.local/share/mise/installs/npm-openai-codex/0.160.0/lib/node_modules/@openai/codex/bin/codex.js
~/.local/share/mise/installs/npm-openai-codex/0.159.2/lib/node_modules/@openai/codex/package.json
~/.local/share/mise/installs/npm-openai-codex/0.159.2/lib/node_modules/@openai/codex/node_modules/@openai/codex-darwin-arm64/vendor/aarch64-apple-darwin/codex-package.json
~/.local/share/mise/installs/npm-openai-codex/0.159.2/lib/node_modules/@openai/codex/node_modules/@openai/codex-darwin-arm64/vendor/aarch64-apple-darwin/codex-resources/voice/bin/codex-voice-host
~/.local/share/mise/installs/npm-openai-codex/0.159.2/lib/node_modules/@openai/codex/node_modules/@openai/codex-darwin-arm64/vendor/aarch64-apple-darwin/bin/codex-code-mode-host
~/.local/share/mise/installs/npm-openai-codex/0.159.2/lib/node_modules/@openai/codex/node_modules/@openai/codex-darwin-arm64/vendor/aarch64-apple-darwin/bin/codex
~/.local/share/mise/installs/npm-openai-codex/0.159.2/lib/node_modules/@openai/codex/node_modules/@openai/codex-darwin-arm64/package.json
~/.local/share/mise/installs/npm-openai-codex/0.159.2/lib/node_modules/@openai/codex/bin/codex.js
~/.local/share/mise/installs/npm-openai-codex/0.158.0/lib/node_modules/@openai/codex/package.json
~/.local/share/mise/installs/npm-openai-codex/0.158.0/lib/node_modules/@openai/codex/node_modules/@openai/codex-darwin-arm64/vendor/aarch64-apple-darwin/codex-package.json
~/.local/share/mise/installs/npm-openai-codex/0.158.0/lib/node_modules/@openai/codex/node_modules/@openai/codex-darwin-arm64/package.json
~/.local/share/mise/installs/npm-openai-codex/0.158.0/lib/node_modules/@openai/codex/bin/codex.js
~/.local/share/mise/installs/npm-openai-codex/0.158.0/lib/node_modules/@openai/codex/node_modules/@openai/codex-darwin-arm64/vendor/aarch64-apple-darwin/bin/codex-code-mode-host
~/.local/share/mise/installs/npm-openai-codex/0.158.0/lib/node_modules/@openai/codex/node_modules/@openai/codex-darwin-arm64/vendor/aarch64-apple-darwin/bin/codex
~/.local/share/mise/installs/npm-openai-codex/0.158.0/lib/node_modules/@openai/codex/node_modules/@openai/codex-darwin-arm64/vendor/aarch64-apple-darwin/codex-resources/voice/bin/codex-voice-host
~/.local/share/mise/installs/npm-openai-codex/0.162.1/lib/node_modules/@openai/codex/package.json
~/.local/share/mise/installs/npm-openai-codex/0.162.1/lib/node_modules/@openai/codex/node_modules/@openai/codex-darwin-arm64/vendor/aarch64-apple-darwin/codex-package.json
~/.local/share/mise/installs/npm-openai-codex/0.162.1/lib/node_modules/@openai/codex/node_modules/@openai/codex-darwin-arm64/vendor/aarch64-apple-darwin/codex-resources/voice/bin/codex-voice-host
~/.local/share/mise/installs/npm-openai-codex/0.162.1/lib/node_modules/@openai/codex/node_modules/@openai/codex-darwin-arm64/vendor/aarch64-apple-darwin/bin/codex-code-mode-host
~/.local/share/mise/installs/npm-openai-codex/0.162.1/lib/node_modules/@openai/codex/node_modules/@openai/codex-darwin-arm64/vendor/aarch64-apple-darwin/bin/codex
~/.local/share/mise/installs/npm-openai-codex/0.162.1/lib/node_modules/@openai/codex/node_modules/@openai/codex-darwin-arm64/package.json
~/.local/share/mise/installs/npm-openai-codex/0.162.1/lib/node_modules/@openai/codex/bin/codex.js

**Evaluating operator gating and task deployment**
exec
/bin/zsh -lc 'cat .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-435275a.md.last.md .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-f1b862c.md.last.md .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-f589c7c.md.last.md; tail -12 .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md' in ~/Workspace/dotfiles
exec
/bin/zsh -lc "sed -n '1060,1160p' scripts/generate-agent-configs.py; sed -n '775,850p' tests/unit/test_generate_agent_configs.py; sed -n '29,68p' home/dot_agents/agent-config.yaml; sed -n '90,135p' home/dot_agents/agent-config.yaml; rg -n 'profile|config.toml|sandbox_workspace_write' home/dot_local/bin/common/executable_codex* home/dot_codex/modify_private_config.toml | head -65" in ~/Workspace/dotfiles
exec
/bin/zsh -lc "rg -n 'sandbox_workspace_write|standard.config.toml|config-profile' ~/.codex/skills/.system/openai-docs/references/codex-self-knowledge.md; ls ~/Workspace; rg -n 'excluded_commands|excludedCommands|gh \\*|linux' home/dot_agents/agent-config.yaml | head -35" in ~/Workspace/dotfiles
 succeeded in 183ms:
No actionable findings in this revision. All 19 `allowed_files` entries are represented across 43 threat rows; none claims closure from configuration tests alone. The design distinguishes its controls from the acknowledged same-UID, shared-capability, agmsg sourcing and path-race residuals. Its enforcement claims match the documented [managed sandbox scope](https://code.claude.com/docs/en/sandboxing#repository-settings-under-an-admin-required-sandbox) and [symlink checks](https://code.claude.com/docs/en/permissions#symlinks).

📝 まとめ: Reviewed the task, every threat row and cited acceptance/review context. No files changed; acceptance remains the orchestrator’s decision.

Not checked: implementation tests or live deployment; the stated residuals remain.
Verdict: correct- [P2] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:293](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:293) The per-host guard rendering is not connected to deployment: its allowed source is plain `executable_orchestrator-only.sh`, which `chezmoi apply` copies without template expansion; no `.tmpl` source or installation renderer is specified, so separately rendered fixture tests cannot establish the installed interpreter and anchor bindings. [Chezmoi attributes](https://www.chezmoi.io/reference/source-state-attributes/).

📝 まとめ: Reviewed every threat row and cited acceptance/review context; one finding remains for orchestrator disposition. No files changed.

Not checked: implementation or live deployment; the stated same-UID and shared-capability residuals remain.
Verdict: incorrect- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:328](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:328) Moving delivery hooks to worker user settings leaves existing worktree-local hooks active: Claude still reads legacy starting-directory settings alongside main-local settings, so previously generated commands retain unsanitized environments and PATH-resolved interpreters; the design needs migration of those entries and a legacy-settings fixture, since checking that no new local file is written cannot establish effective hook binding. [Settings loading](https://code.claude.com/docs/en/settings#where-claude-code-keeps-the-local-file-in-a-git-repository).

📝 まとめ: Reviewed all 44 threat rows, 20 allowed-file entries and cited review context; one finding remains for orchestrator disposition. No files changed.

Not checked: implementation or live deployment; the stated same-user and shared-capability residuals remain.
Verdict: incorrect- 2026-10-19T04:46Z: C-80 seventh review (`…-text-security-519afd7.md`): `Verdict: incorrect`, one P1 and one P2, both consequences of the env -i decision: `env -i` strips CLAUDE_PROJECT_DIR, which the guard needs (every hook would exit 0 without running) → the hook command re-exports the launch identity explicitly after env -i; the pinned PATH removes ruff, prettier and terminal-browser from the orchestrator's formatter and map hooks → in orchestrator sessions the guard runs them with a rendered PATH of the trusted root's absolute tool directories. Round 8 (local) follows.
- 2026-10-19T04:5xZ: round-8 P1-15 text installed (env -i with the launch identity re-exported; role-specific PATH in the guard); checker OK; the eighth C-80 review started.
- 2026-10-19T05:41Z: C-80 ninth review (`…-text-security-435275a.md`): `Verdict: correct`. The text is dispatched to a010 (wJ:p5, worker-e; a012 is on its #412 revise) at 05:4xZ with the counters and the review history pasted in its Checks block; a05 follows on the same seat after this merge.
- 2026-10-19T05:45Z: PING to a010: design 5.14 and D-024-16..23 exist only in the orchestrator working copy until the next records PR; the worker reads them at the absolute path of the main checkout (C-86 recorded).
- 2026-10-19T05:46:28Z: a010 `status=running`: branch `tools/worker-write-boundary-a01` from 205fe85c (origin/main had advanced); the #420 and #427 branches preserved; reading callers and adding the red tests.
- 2026-10-19T05:50:16Z: a010 `status=running question=1`: the Check requires `make format` pass while the clean base 205fe85c fails on 12 out-of-scope files (the known inherited set). Interpretation note 1 (05:5xZ, no amendment): the sibling texts' clause applies (an inherited formatting failure is reproduced against the unchanged base and disclosed with exact output and per-file exit statuses; no out-of-scope repair); the task's own files pass the make format flags. INV-6: questions 1.
- 2026-10-19T06:01:06Z: a010 `status=running question=2`: the tracked `.claude/settings.json` is not a chezmoi template, so literal rendered HOME/anchor/interpreter paths would bind it to this macOS host; it proposes HOME-relative paths in the tracked file with the host-specific absolute paths only inside the rendered guard, and CLAUDE_PROJECT_DIR never selecting an executable. The reading is right and the text is wrong. This is the second question PONG (the first 05:50:16Z) → INV-6 S2: `status=withdrawn` 06:1xZ (branch, 8 green tests, fixtures and evidence kept); the reset a02 = the a01 text with both clarifications folded in and the Codex `network_access` item removed (routing: a Codex seat edits no Codex-boundary source; that item becomes a small Claude-seat task), redesigned by the review profile and passed through C-80 before dispatch.
- correction (2026-10-19T06:13Z): the S2 line above was premature: `regime-counters.sh --history-only` counts `status=question` PONGs and reports questions=0, because a010 sent its two questions as `status=running question=N` (a Codex-seat form deviation of the PONG contract, recorded as a conformance note; C-87: the counter also reads a `question=` field). By the counter INV-6 S2 did not fire; no withdrawal was sent (the send was guarded on the counter). Both questions are answered by interpretation notes (note 1 at 05:5xZ; note 2 at 06:13Z: $HOME-relative paths in the tracked file, host-specific paths only in the rendered guard) and amendment 1 folds both into the text and removes the Codex network_access item (routing); the running redesign output becomes that amendment text (same task id, no reset).
- 2026-10-19T06:19:54Z: a010 `status=blocked` on an optional progress inspection only (`ps -axo … | rg …` refused by its Codex sandbox: operation not permitted); no retry; the authorized unit run continues and is collected through its session; implementation per note 2 continues after that run. No action: an optional inspection outside the sandbox is correctly refused and not escalated (Worker Playbook step 4).
- 2026-10-19T06:23Z: the amendment-1 text (the review-profile a02 output re-targeted to a01: the inherited make format clause, the portable tracked settings.json with host paths only in the rendered guard, the Codex network_access item removed to the Claude-seat task dotfiles-T133-codex-worker-network-a01) installed; checker OK; its C-80 review started 06:23Z; dispatch to a010 on correct.
- 2026-10-19T06:25:59Z: C-80 of the amendment-1 text (`…-text-security-f1b862c.md`): one P2 (the guard source is a plain `executable_` file, which chezmoi copies without template expansion, so the per-host paths cannot be rendered) → the source becomes `executable_orchestrator-only.sh.tmpl` with the rendering sentence and the render test stated; the review runs again before dispatch.
- 2026-10-19T06:26:42Z: a010 `status=blocked` on the required CI doc test: tests/unit/test_agmsg_orchestration_docs.py:200-201 asserts the step 4 sentence this task rewrites and is outside allowed_files. Amendment 1 (in its C-80 review) gains the module for that one assertion with a threat row; C-78: PR #427 (P1-8, the same seat) edits the module and merges first; this PR rebases. PING sent 06:2xZ.

 succeeded in 257ms:
dotfiles
local-speech
reports
slides
tpro-platform
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

 succeeded in 299ms:
    """The raw name of a `[table]` or `[[array]]` header line, which may end in a `# comment`, else None."""
    stripped = header.strip()
    if not stripped.startswith("["):
        return None
    double = stripped.startswith("[[")
    start = index = 2 if double else 1
    quote = None
    while index < len(stripped):
        char = stripped[index]
        if quote == '"' and char == "\\\\":
            index += 2
            continue
        if char == quote:
            quote = None
        elif quote is None and char in ('"', "'"):
            quote = char
        elif quote is None and char == "]":
            break
        index += 1
    else:
        return None
    rest = stripped[index + 1 :]
    if double:
        if not rest.startswith("]"):
            return None
        rest = rest[1:]
    rest = rest.lstrip()
    if rest and not rest.startswith("#"):
        return None
    return canonical_table_name(stripped[start:index].strip())


def multiline_string_after(line: str, delimiter: str | None) -> str | None:
    """The multiline string delimiter still open after this line, given the one open before it, else None."""
    index = 0
    while index < len(line):
        if delimiter is not None:
            if delimiter == '"""' and line[index] == "\\\\":
                index += 2
            elif line.startswith(delimiter, index):
                # Up to two more quotes before the closing delimiter belong to the string.
                index += len(line[index:]) - len(line[index:].lstrip(delimiter[0]))
                delimiter = None
            else:
                index += 1
            continue
        char = line[index]
        if char == "#":
            return None
        if line.startswith('"""', index) or line.startswith("\'\'\'", index):
            delimiter = line[index : index + 3]
            index += 3
        elif char == '"':
            index += 1
            while index < len(line) and line[index] != '"':
                index += 2 if line[index] == "\\\\" else 1
            index += 1
        elif char == "'":
            end = line.find("'", index + 1)
            index = len(line) if end == -1 else end + 1
        else:
            index += 1
    return delimiter


def split_chunks(text: str) -> list[tuple[str | None, str]]:
    chunks: list[tuple[str | None, str]] = []
    current_name: str | None = None
    current_lines: list[str] = []
    pending_lines: list[str] = []
    string = None
    for line in text.splitlines(keepends=True):
        # A header-like line inside a multiline string is string content, never a chunk boundary.
        name = table_name(line) if string is None else None
        string = multiline_string_after(line, string)
        if name is None:
            if current_name is None:
                pending_lines.append(line)
            else:
                current_lines.append(line)
            continue
        if current_name is None:
            if pending_lines:
                split_at = len(pending_lines)
                while split_at and not pending_lines[split_at - 1].strip():
                    split_at -= 1
                if split_at:
                    chunks.append((None, "".join(pending_lines[:split_at])))
                pending_lines = pending_lines[split_at:]
        else:
            chunks.append((current_name, "".join(current_lines)))
        current_name = name
        current_lines = pending_lines + [line]
        pending_lines = []
    if current_name is None:
        if pending_lines:
            chunks.append((None, "".join(pending_lines)))
    else:
        chunks.append((current_name, "".join(current_lines)))
    return chunks

                        "AWS_EC2_METADATA_DISABLED": "true",
                    },
                    settings["env"],
                )
                self.assertFalse(sandbox["network"].get("allowAllUnixSockets", False))

    def test_linux_sandbox_excludes_the_top_level_herdr_agents_invocation(self) -> None:
        manifest = load_manifest_fixture(self.temp_dir)
        settings = self.render_claude_template(self.module.render_claude_settings(manifest), "linux")
        self.assertEqual(
            [
                "agmsg-dispatch *",
                "gh *",
                "herdr-agents *",
                "/render-home/.agents/skills/agmsg/scripts/actas-claim.sh *",
            ],
            settings["sandbox"]["excludedCommands"],
        )
        self.assertEqual(["Bash(agmsg-dispatch:*)"], settings["permissions"]["allow"])

    def test_audit_profile_renders_read_only_sandbox_override(self) -> None:
        manifest = sample_manifest()
        manifest["model_profiles"]["audit"] = {
            "claude": {"model": "claude-fable-5-1", "effort": "high"},
            "codex": {
                "model": "gpt-6-astra",
                "model_reasoning_effort": "high",
                "sandbox_mode": "read-only",
            },
        }
        outputs = self.module.expected_outputs(manifest)
        self.module.write_outputs(outputs)

        def render(name: str) -> dict:
            path = self.temp_dir / f"home/dot_codex/modify_private_{name}.config.toml"
            result = subprocess.run(
                [str(path)],
                input="",
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            return tomllib.loads(result.stdout)

        self.assertEqual(render("audit")["sandbox_mode"], "read-only")
        self.assertNotIn("sandbox_mode", render("standard"))
        self.assertIn(
            'sandbox_mode = "workspace-write"',
            outputs[self.temp_dir / manifest["codex"]["config_path"]],
        )
        env = outputs[self.temp_dir / "home/dot_agents/model-profiles.env"]
        self.assertIn('MODEL_PROFILE_AUDIT_CODEX_ARGS="--profile audit"', env)

    def test_model_profiles_reject_invalid_sandbox_mode(self) -> None:
        manifest = sample_manifest()
        manifest["model_profiles"]["standard"]["codex"]["sandbox_mode"] = "readonly"

        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
            self.module.model_profiles(manifest)
        self.assertIn("standard.codex.sandbox_mode must be one of", stderr.getvalue())

    def test_profile_modify_scripts_are_byte_idempotent_with_runtime_state(
        self,
    ) -> None:
        outputs = self.module.expected_outputs(sample_manifest())
        standard_profile = self.temp_dir / "home/dot_codex/modify_private_standard.config.toml"
        self.module.write_outputs(outputs)
        current = (
            '# Codex model profile "standard"; launch with: codex --profile standard\n'
            f"# {self.module.GENERATED_HEADER}\n"
            "\n"
            'model = "gpt-6.1-sol"\n'
            'model_reasoning_effort = "high"\n'
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
    # INV-7: the Claude review profile is the same model and effort as deep.
    claude: { model: claude-fable-5-1, effort: xhigh }
    codex: { model: gpt-6.1-sol, model_reasoning_effort: xhigh }
  deep:
    claude: { model: claude-fable-5-1, effort: xhigh, advisor: fable }
    codex:
      model: gpt-6.1-sol
      model_reasoning_effort: xhigh
      notify: ['{{ .chezmoi.homeDir }}/.local/bin/common/contextdb-codex-notify']
  security:
    # Security-audit tier: specialist model for auditing pending changes.
    claude: { model: claude-fable-5, effort: high }
    codex:
      # gpt-daybreak-blue-latest requires API-key auth (rejected under ChatGPT login).
      model: gpt-6-astra
      model_reasoning_effort: high
      notify: ['{{ .chezmoi.homeDir }}/.local/bin/common/contextdb-codex-notify']
  audit:
    # Auditor tier (監査役): cross-vendor read-only audit of worker changesets
    # at xhigh reasoning effort (operator pin 2026-10-09, T115).
    claude: { model: claude-fable-5-1, effort: high }
    codex:
      model: gpt-6-astra
      model_reasoning_effort: xhigh
      sandbox_mode: read-only
      notify: ['{{ .chezmoi.homeDir }}/.local/bin/common/contextdb-codex-notify']
interactive_profile: deep
# Worker pane agent for herdr-agents: codex or claude. Renders into
codex:
  config_path: home/.chezmoitemplates/codex-config-managed.toml
  model_reasoning_summary: concise
  model_verbosity: low
  personality: pragmatic
  approval_policy: on-request
  sandbox_mode: workspace-write
  web_search: cached
  check_for_update_on_startup: false
  project_doc_max_bytes: 65536
  project_doc_fallback_filenames:
    - CLAUDE.md
  tui:
    status_line:
      - model-with-reasoning
      - context-remaining
      - used-tokens
      - total-input-tokens
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
      enabled: true
    ponytail@ponytail:
      enabled: true
home/dot_local/bin/common/executable_codex-orchestrate:46:[[ -r $HOME/.agents/model-profiles.env ]] || die 'deploy model-profiles.env for herdr-agents first'
home/dot_local/bin/common/executable_codex-orchestrate:48:source "$HOME/.agents/model-profiles.env"
home/dot_local/bin/common/executable_codex-orchestrate:50:profile="$MODEL_PROFILE_INTERACTIVE"
home/dot_local/bin/common/executable_codex-orchestrate:51:[[ $profile =~ ^[a-zA-Z][a-zA-Z0-9_]*$ ]] || die 'invalid interactive profile'
home/dot_local/bin/common/executable_codex-orchestrate:52:key="MODEL_PROFILE_$(printf '%s' "$profile" | tr '[:lower:]' '[:upper:]')_CODEX_ARGS"
home/dot_local/bin/common/executable_codex-orchestrate:53:[[ -n $profile && -n ${!key:-} ]] || die 'missing interactive Codex profile arguments'
home/dot_local/bin/common/executable_codex-orchestrate:103:name="codex-$profile-$suffix"
home/dot_codex/modify_private_config.toml:181:HOOK_TRUST = {'declared': [{'key': '{{ .chezmoi.homeDir }}/.codex/config.toml:permission_request:0:0', 'enabled': True}, {'key': '{{ .chezmoi.homeDir }}/.codex/config.toml:pre_compact:0:0', 'enabled': True}, {'key': '{{ .chezmoi.homeDir }}/.codex/config.toml:post_compact:0:0', 'enabled': True}, {'key': '{{ .chezmoi.homeDir }}/.codex/config.toml:session_end:0:0', 'enabled': True}, {'key': 'crit@mryfmo-personal-plugins:hooks/hooks.json:stop:0:0', 'trusted_hash': 'sha256:bf6ad428ae7902810fa2d68d8db42228377af118aa18508ad0eccf73a95ed1f8', 'enabled': True}, {'key': 'ponytail@ponytail:hooks/claude-codex-hooks.json:session_start:0:0', 'trusted_hash': 'sha256:7ee5d5ae1f4a9e55f1f429f2960c2f9f32293f198c0e8e2e42b2fb3b4eeda142', 'enabled': True}, {'key': 'ponytail@ponytail:hooks/claude-codex-hooks.json:user_prompt_submit:0:0', 'trusted_hash': 'sha256:8c9efc5a5e649c8cdca3f0b7bf4cba81d9717d1bc930c7dbc18b6efd66c7c58c', 'enabled': True}, {'key': 'ponytail@ponytail:hooks/claude-codex-hooks.json:subagent_start:0:0', 'trusted_hash': 'sha256:7954d675ef3bafd5e5a6073ae51d7de57a08f21340f241c332f99078e955675d', 'enabled': True}], 'config_hooks': {'permission_request': [{'matcher': '*', 'hooks': [{'type': 'command', 'command': '{{ .chezmoi.homeDir }}/.local/bin/common/permgate codex', 'timeout': 10, 'statusMessage': 'Evaluating permission request'}]}], 'pre_compact': [{'matcher': '*', 'hooks': [{'type': 'command', 'command': '{{ .chezmoi.homeDir }}/.local/bin/common/contextdb-codex-notify', 'timeout': 10, 'statusMessage': 'Recording to CompactionDB'}]}], 'post_compact': [{'matcher': '*', 'hooks': [{'type': 'command', 'command': '{{ .chezmoi.homeDir }}/.local/bin/common/contextdb-codex-notify', 'timeout': 10, 'statusMessage': 'Recording to CompactionDB'}]}], 'session_end': [{'matcher': '*', 'hooks': [{'type': 'command', 'command': '{{ .chezmoi.homeDir }}/.local/bin/common/contextdb-codex-notify', 'timeout': 3, 'statusMessage': 'Recording to CompactionDB'}]}]}}
home/dot_codex/modify_private_config.toml:354:    if source == home + "/.codex/config.toml":

**Evaluating codex execution options**
codex
`closed` の3行は設定の描画だけを検証する設計で、sandbox の強制を証明するとは書いていません。その区別は妥当です。一方、依存タスクのマージと実機への適用は別なので、Linux の既存 `gh` 除外や未適用のポリシーが残る状態で、このタスクを開始できないか確認しています。設定の解釈には OpenAI Docs も参照します。

web search: 
web search: site:developers.openai.com codex profiles sandbox_workspace_write network_access
exec
/bin/zsh -lc '~/.local/share/mise/installs/npm-openai-codex/0.162.1/lib/node_modules/@openai/codex/node_modules/@openai/codex-darwin-arm64/vendor/aarch64-apple-darwin/bin/codex --help' in ~/Workspace/dotfiles
 succeeded in 0ms:
WARNING: proceeding, even though we could not create PATH aliases: Operation not permitted (os error 1)
Codex CLI

If no subcommand is specified, options will be forwarded to the interactive CLI.

Usage: codex [OPTIONS] [PROMPT]
       codex [OPTIONS] <COMMAND> [ARGS]

Commands:
  agents            Browse all agent sessions on the shared local app-server daemon
  exec              Run Codex non-interactively [aliases: e]
  review            Run a code review non-interactively
  login             Manage login
  logout            Remove stored authentication credentials
  mcp               Manage external MCP servers for Codex
  plugin            Manage Codex plugins
  app-server        [experimental] Run the app server or related tooling
  remote-control    [experimental] Manage the app-server daemon with remote control enabled
  app               Launch the Desktop app (opens the app installer if missing)
  completion        Generate shell completion scripts
  update            Update Codex to the latest version
  doctor            Diagnose local Codex installation, config, auth, and runtime health
  sandbox           Run commands within a Codex-provided sandbox
  debug             Debugging tools
  apply             Apply the latest diff produced by Codex agent as a `git apply` to your local
                    working tree [aliases: a]
  resume            Resume a previous interactive session (picker by default; use --last to continue
                    the most recent)
  queue             Queue a message for an existing session
  archive           Archive a saved session by id or session name
  delete            Permanently delete a saved session by id or session name
  migrate-rollouts  Inspect or migrate legacy local sessions to paginated thread history
  unarchive         Unarchive a saved session by id or session name
  fork              Fork a previous interactive session (picker by default; use --last to fork the
                    most recent)
  cloud             [EXPERIMENTAL] Browse tasks from Codex Cloud and apply changes locally
  exec-server       [EXPERIMENTAL] Run the standalone exec-server service
  features          Inspect feature flags
  help              Print this message or the help of the given subcommand(s)

Arguments:
  [PROMPT]
          Optional user prompt to start the session

Options:
  -c, --config <key=value>
          Override a configuration value that would otherwise be loaded from `~/.codex/config.toml`.
          Use a dotted path (`foo.bar.baz`) to override nested values. The `value` portion is parsed
          as TOML. If it fails to parse as TOML, the raw string is used as a literal.
          
          Examples: - `-c model="o3"` - `-c 'sandbox_permissions=["disk-full-read-access"]'` - `-c
          shell_environment_policy.inherit=all`

      --enable <FEATURE>
          Enable a feature (repeatable). Equivalent to `-c features.<name>=true`

      --disable <FEATURE>
          Disable a feature (repeatable). Equivalent to `-c features.<name>=false`

      --remote <ADDR>
          Connect the TUI to a remote app server endpoint.
          
          Accepted forms: `ws://host:port`, `wss://host:port`, `unix://`, or `unix://PATH`.

      --remote-auth-token-env <ENV_VAR>
          Name of the environment variable containing the bearer token to send to a remote app
          server websocket

      --strict-config
          Error out when config.toml contains fields that are not recognized by this version of
          Codex

  -i, --image <FILE>...
          Optional image(s) to attach to the initial prompt

  -m, --model <MODEL>
          Model the agent should use

      --oss
          Use open-source provider

      --local-provider <OSS_PROVIDER>
          Specify which local provider to use (lmstudio or ollama). If not specified with --oss,
          will use config default or show selection

  -p, --profile <CONFIG_PROFILE_V2>
          Layer $CODEX_HOME/<name>.config.toml on top of the base user config

  -s, --sandbox <SANDBOX_MODE>
          Select the sandbox policy to use when executing model-generated shell commands
          
          [possible values: read-only, workspace-write, danger-full-access]

      --approve-for-me
          Route approval requests through automatic review using the workspace-write sandbox

      --dangerously-bypass-approvals-and-sandbox
          Skip all confirmation prompts and execute commands without sandboxing. EXTREMELY
          DANGEROUS. Intended solely for running in environments that are externally sandboxed

      --dangerously-bypass-hook-trust
          Run enabled hooks without requiring persisted hook trust for this invocation. DANGEROUS.
          Intended only for automation that already vets hook sources

  -C, --cd <DIR>
          Tell the agent to use the specified directory as its working root

      --worktree
          Run the session in a new managed Git worktree

      --add-dir <DIR>
          Additional directories that should be writable alongside the primary workspace

  -a, --ask-for-approval <APPROVAL_POLICY>
          Configure when the model requires human approval before executing a command

          Possible values:
          - on-request: The model decides when to ask the user for approval
          - never:      Never ask for user approval Execution failures are immediately returned to
            the model

      --search
          Enable live web search. When enabled, the native Responses `web_search` tool is available
          to the model (no per‑call approval)

      --no-alt-screen
          Disable alternate screen mode
          
          Runs the TUI in inline mode, preserving terminal scrollback history.

      --no-daemon
          Run without the shared background server, even if it is already running

  -h, --help
          Print help (see a summary with '-h')

  -V, --version
          Print version

**Analyzing config merge behavior**
**Reviewing merge logic for tests**
web search: 
web search: https://developers.openai.com/codex/config-reference
exec
/bin/zsh -lc "sed -n '1160,1255p' scripts/generate-agent-configs.py; sed -n '850,950p' tests/unit/test_generate_agent_configs.py" in ~/Workspace/dotfiles
exec
/bin/zsh -lc "git diff --numstat -- .orchestration/tasks/dotfiles-T133-codex-worker-network-a01.md; rg -n 'codex-worker-network' .orchestration/acceptance -g '*.md'; sed -n '300,335p' .orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md" in ~/Workspace/dotfiles
exec
/bin/zsh -lc "rg -n 'Completion|prerequisite|pending|permission|approval' .orchestration/tasks/dotfiles-T133-regime-ci-followup-a01.md; rg -n 'gh.*outside|sandbox|threat.table|trust.boundary' ~/.agents/skills/agmsg-orchestration/SKILL.md" in ~/Workspace/dotfiles
 succeeded in 167ms:


def runtime_prefix(name: str | None) -> str | None:
    if name is None:
        return None
    for prefix in RUNTIME_PREFIXES:
        if name == prefix or name.startswith(f"{{prefix}}."):
            return prefix
    return None


def base_hook_state() -> list[tuple[str, str]]:
    """Harvest operator-granted hook trust from the base Codex config."""
    path = Path.home() / ".codex/config.toml"
    if not path.is_file():
        return []
    return [
        (name, chunk)
        for name, chunk in split_chunks(path.read_text())
        if runtime_prefix(name) == "hooks.state"
    ]


def trusted_hash(chunk: str) -> str | None:
    """Parse a persisted hook-trust hash without recalculating or trusting it."""
    match = re.search(r'^trusted_hash = "([^"]+)"$', chunk, re.MULTILINE)
    return match.group(1) if match else None


def merge_config(current: str) -> str:
    """Keep profile trust authoritative and only warn when base trust diverges."""
    managed_chunks = split_chunks({managed_source})
    declared = declared_hook_state(str(Path.home()))
    declared_keys = {{hook_state_key(name) for name, _ in declared}}
    current_chunks = drop_declared_hook_state(split_chunks(current) if current.strip() else [], declared)
    current_by_name: dict[str, list[str]] = {{}}
    current_by_runtime_prefix: dict[str, list[tuple[int, str, str]]] = {{}}
    managed_by_runtime_prefix: dict[str, list[tuple[str, str]]] = {{}}
    for current_index, (current_name, current_chunk) in enumerate(current_chunks):
        if current_name is not None:
            current_by_name.setdefault(current_name, []).append(current_chunk)
            prefix = runtime_prefix(current_name)
            if prefix is not None:
                current_by_runtime_prefix.setdefault(prefix, []).append((current_index, current_name, current_chunk))
    for managed_name, managed_chunk in managed_chunks:
        prefix = runtime_prefix(managed_name)
        if managed_name is not None and prefix is not None:
            managed_by_runtime_prefix.setdefault(prefix, []).append((managed_name, managed_chunk))
    managed_by_runtime_prefix.setdefault("hooks.state", []).extend(declared)
    for base_name, base_chunk in base_hook_state():
        if hook_state_key(base_name) in declared_keys:
            continue
        if base_name in current_by_name:
            profile_hash = trusted_hash(current_by_name[base_name][0])
            base_hash = trusted_hash(base_chunk)
            if profile_hash and base_hash and profile_hash != base_hash:
                print(
                    f"warning: hook trust divergence for {{base_name}}: profile={{profile_hash}} base={{base_hash}}",
                    file=sys.stderr,
                )
        if base_name not in current_by_name and base_name not in {{
            name for name, _ in managed_by_runtime_prefix.get("hooks.state", [])
        }}:
            managed_by_runtime_prefix.setdefault("hooks.state", []).append((base_name, base_chunk))
    managed_names = {{table_name for table_name, _ in managed_chunks if table_name is not None}}
    emitted_current: set[int] = set()
    emitted_runtime_prefixes: set[str] = set()
    output: list[str] = []
    for managed_name, managed_chunk in managed_chunks:
        prefix = runtime_prefix(managed_name)
        if prefix is not None:
            if prefix in emitted_runtime_prefixes:
                continue
            current_group = current_by_runtime_prefix.get(prefix, [])
            if current_group:
                for runtime_name, runtime_chunk in managed_by_runtime_prefix.get(prefix, []):
                    if runtime_name == prefix and runtime_name not in current_by_name:
                        output.append(runtime_chunk)
                for current_index, current_name, current_chunk in current_group:
                    output.append(current_chunk)
                    emitted_current.add(current_index)
                for runtime_name, runtime_chunk in managed_by_runtime_prefix.get(prefix, []):
                    if runtime_name != prefix and runtime_name not in current_by_name:
                        output.append(runtime_chunk)
            else:
                output.extend(chunk for _, chunk in managed_by_runtime_prefix.get(prefix, []))
            emitted_runtime_prefixes.add(prefix)
        else:
            output.append(managed_chunk)
    for current_index, (current_name, current_chunk) in enumerate(current_chunks):
        if current_name is None or current_index in emitted_current:
            continue
        prefix = runtime_prefix(current_name)
        if prefix is not None:
            if prefix in emitted_runtime_prefixes:
                continue
            'model_reasoning_effort = "high"\n'
            "\n"
            "[features]\n"
            "hooks = true\n"
            "\n"
            "[hooks.state]\n"
            "trusted = true\n"
        )
        result = subprocess.run(
            [str(standard_profile)],
            input=current,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env={**os.environ, "HOME": str(self.temp_dir / "target-home")},
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, current)

    def test_profile_modify_scripts_preserve_repeated_runtime_tables(self) -> None:
        outputs = self.module.expected_outputs(sample_manifest())
        standard_profile = self.temp_dir / "home/dot_codex/modify_private_standard.config.toml"
        self.module.write_outputs(outputs)
        current = (
            '# Codex model profile "standard"; launch with: codex --profile standard\n'
            f"# {self.module.GENERATED_HEADER}\n"
            "\n"
            'model = "gpt-6.1-sol"\n'
            'model_reasoning_effort = "high"\n'
            "\n"
            "[features]\n"
            "hooks = true\n"
            "\n"
            "[hooks.state]\n"
            "\n"
            "[[hooks.state.sub]]\n"
            'name = "first"\n'
            "\n"
            "[[hooks.state.sub]]\n"
            'name = "second"\n'
        )
        result = subprocess.run(
            [str(standard_profile)],
            input=current,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env={**os.environ, "HOME": str(self.temp_dir / "target-home")},
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, current)

        env_path = self.temp_dir / "home/dot_agents/model-profiles.env"
        self.assertIn('MODEL_PROFILE_INTERACTIVE="standard"', outputs[env_path])
        self.assertIn('MODEL_PROFILE_STANDARD_CODEX_ARGS="--profile standard"', outputs[env_path])
        self.assertIn(
            'MODEL_PROFILE_EXPRESS_CLAUDE_ARGS="--model haiku --effort low"',
            outputs[env_path],
        )

        agent_path = self.temp_dir / "home/dot_claude/agents/express-explorer.md"
        self.assertIn("model: haiku", outputs[agent_path])
        self.assertIn("effort: low", outputs[agent_path])

        project_map_path = self.temp_dir / "home/dot_claude/agents/project-map.md"
        self.assertIn("model: sonnet", outputs[project_map_path])
        self.assertIn("effort: high", outputs[project_map_path])
        self.assertIn("  - project-map\n", outputs[project_map_path])

        self.assertFalse([path for path in outputs if path.name == "ccgate.jsonnet"])

    def hook_trust_namespace(self, manifest: dict) -> dict:
        namespace = {"sys": sys, "Path": Path, "HOOK_TRUST": self.module.codex_hook_trust(manifest)}
        exec(self.module.HOOK_TRUST_CODE, namespace)
        return namespace

    def test_hook_trust_hash_reproduces_codex_current_hashes(self) -> None:
        # Values Codex 0.160.0 reported as current_hash (app-server hooks/list) on the operator's host.
        codex_hook_hash = self.hook_trust_namespace(sample_manifest())["codex_hook_hash"]
        notify = "~/.local/bin/common/contextdb-codex-notify"
        for event, matcher, handler, expected in (
            (
                "permission_request",
                "*",
                {
                    "type": "command",
                    "command": "~/.local/bin/common/permgate codex",
                    "timeout": 10,
                    "statusMessage": "Evaluating permission request",
                },
                "sha256:64d9851fb629f7cd5608706436fb5b8588dc60abf355893ebe3eaca401a9ff65",
            ),
            (
                "pre_compact",
                "*",
                {"type": "command", "command": notify, "timeout": 10, "statusMessage": "Recording to CompactionDB"},
                "sha256:daa1e215632e85e1b578f07ff0647c8f650d6d73f454c1089a74a6d354736edc",

 succeeded in 191ms:
53:## Check and Completion
55:The Check and Completion clauses of `.orchestration/tasks/dotfiles-T133-regime-ci-a02.md` apply as written, with `dotfiles-T133-regime-ci-followup-a02` as the owner of any advisory P2 and `task_copy=<sha256 of .orchestration/dotfiles-T133-regime-ci-followup-a01/task.md>` in the RESULT.
21:- A Claude session started in the repository root outside Herdr (a plain shell, mosh/ssh, or `claude -p`) is a pane-less orchestrator: nothing seats a worker automatically, and the SessionStart `herdr-agents --attach` hook prints a summary line naming that state, the on-demand commands, and any seated worker, followed in a regime repository by the `agmsg-orchestration:` directive line. Bring the regime up on demand: claim the seat outside the sandbox with the composite instance id, `actas-claim.sh <repo> claude-code <name> <session_id>.<claude pid>` (a claim from sandboxed Bash writes the bare session id and turn delivery then skips silently; see the seat-lock bullet below); seat the worker with `herdr-agents --add-worker <worktree>` (it derives `HERDR_SOCKET_PATH` from the default Herdr server socket `~/.config/herdr/herdr.sock`, the path the Claude sandbox allowlists, before creating anything, accepts a claude worker's workspace-trust dialog during spawn's readiness wait, and takes `--ready-timeout <seconds>`); confirm the worker's placement from its `run/spawn.*` placement record itself (the `herdr:<socket>:<pane>` row that upstream `agmsg_spawn_path` resolves) and the `linkage=` line `--add-worker` prints, never from `team.sh <team> --json`, which observes Codex members by reading their pane; treat the `linkage=` line `--add-worker` prints as the `AGMSG-PING` evidence, and on `pong=no` or `linkage=unreached` wake again with `agmsg-dispatch <team> <orchestrator> <worker> <pane> 'AGMSG-PING v1 task_id=<id> reason=<reason>'` and verify the PING's `read_at` (`poke.sh` only for a viewed workspace); and dispatch no AGMSG-TASK before its `AGMSG-PONG` arrives. Without a managed workspace the auditor runs headless, in the form the task-level audit bullet below names. A pane-less session uses turn delivery when the Monitor cannot run; see "Identity, delivery, and storage" for the platform limits.
22:- Start checklist (operator or orchestrator, repository cwd, plain shell or Herdr): the workspace created by `herdr-agents <DIR>` full mode holds the orchestrator pane only, and only the operator creates or relaunches it; inside a Herdr pane the SessionStart `--attach` hook claims the orchestrator seat and prints the directive, and never seats, restarts or repairs a worker. Inside Herdr or outside it, the orchestrator seats a worker on demand with `herdr-agents --add-worker [<worktree>]` (its own tab of the managed workspace, or its own workspace for a pane-less orchestrator), confirms it by PING/PONG before any task, and removes it with `--remove-worker` when the task is done. A Claude that finds itself outside Herdr is the pane-less orchestrator of the bullet above: its SessionStart line reports the state, and it brings the regime up on demand exactly as that bullet describes (composite seat claim outside the sandbox, `--add-worker`, PING/PONG before any task, headless auditor); anything neither bullet describes is not improvised.
31:- Add and remove parallel workers only with `herdr-agents --add-worker <worktree> [--kind codex|claude] [--profile NAME]` and `herdr-agents --remove-worker <worktree> [--force]` (worktree under `.claude/worktrees/`). For Codex, seat ordinary tasks with `--profile standard`; use `--profile security` only for trust-boundary tasks (permgate, redaction or secret handling, sandbox or permission policy), per the model-selection rule, with an identity such as `codex-security-dot-aNNN`. Add-worker seats the worker in its own tab of the pair workspace, labeled `<team>:<name>` with the pair tab untouched (in its own workspace only when no pair workspace exists, as in the pane-less bring-up), through upstream `spawn.sh --project <worktree> --terminal-driver herdr` with the profile's launch args in a generated spawn options file, so a placement record exists and `poke.sh`/`despawn.sh` work. Remove-worker despawns it, then turns delivery off, leaves, and closes that tab (or workspace), refusing a dirty worktree without `--force`. Keep about three concurrent workers at most; raw herdr topology commands stay forbidden (T21 G7).
52:- On activation, check `delivery.sh status <type> <repo>`. This repo runs Claude Code seats on `both` (monitor's push plus turn's pull), one notch more redundant than upstream's Claude Code default `monitor`, since an unattended worker pane has no one to notice a Monitor watch that silently failed to re-arm; Codex seats run on `turn` (see the next bullet). If weaker than that, run `delivery.sh set both claude-code <repo>` (or `delivery.sh set turn codex <repo>` for a Codex identity), use the SessionStart-provided `watch.sh <session_id> <repo> <type>` started outside the sandbox as a persistent in-session monitor, and claim exclusivity with `actas-claim.sh <project> <type> <name> <session_id>`. A Claude worker seated by `--add-worker` gets its Monitor watch through its actas boot; when it is seated in its own workspace (no managed workspace exists), `herdr-agents` also sets `AGMSG_CC_MONITOR_KEEP_ALIVE=1` in that workspace's environment so the watch re-arms unconditionally on expiry, not only when the expired watch delivered something (upstream's default).
55:- A codex worker in a nested worktree gets `<common>/objects`, `<common>/refs`, `<common>/logs` and `<common>/worktrees/<name>` (`<common>` from `git -C <worktree> rev-parse --git-common-dir`) as writable roots from `herdr-agents` (`-c sandbox_workspace_write.writable_roots`, with the configured agmsg roots kept first), so local git operations need no escalation. The common dir itself, `config`, `hooks`, `info`, `HEAD` and `packed-refs` stay read-only. The worker seat runs with `--ask-for-approval never` and `sandbox_workspace_write.network_access=true`, so a GitHub fetch, push or `gh` call works inside the sandbox and the worker never prompts: there is no escalation for a worker, and an action outside the sandbox or forbidden by the execpolicy fails and is reported as `AGMSG-PONG v1 status=blocked`. The `sandbox_workspace_write.network_access` switch is a boolean, so the worker reaches any host (no domain allowlist is configured, unlike Claude Code's `allowedDomains`), and the permgate PermissionRequest hook never fires for the worker seat; it stays live for interactive Codex sessions, which keep on-request approvals and no sandbox network.
56:- The orchestrator's actas seat lock must hold the composite instance id `<sid>.<pid>`; check it with `cat ~/.agents/skills/agmsg/run/actas.<team>__<name>.session`. `actas-claim.sh` run from sandboxed Bash cannot read the Claude pid, writes the bare session id, and the Stop-hook inbox check then skips delivery silently (`other:<sid>`). On macOS, the Claude Seatbelt sandbox denies `ps`; a `watch.sh` Monitor started outside the sandbox (by SessionStart or the orchestrator pane) keeps running, but one started inside computes the bare session id and exits against the composite actas lock. On Linux, the bubblewrap pid namespace hides the Claude pid: a sandbox-started Monitor exits "no longer alive", and `pgrep` sees only the sandbox. No seat starts its watch from sandboxed Bash. `herdr-agents` therefore claims the seat outside the sandbox when it starts the orchestrator pane and from its SessionStart `--attach` hook, printing `seat_claim=ok owner=<sid>.<pid>` (or `seat_claim=unresolved`, never a bare-id lock), and `make doctor` warns on a bare-id orchestrator lock while a claude session runs in the repository. When the Monitor is unavailable, turn delivery is the working path, and an idle orchestrator is woken by the worker's `agmsg-dispatch` to the orchestrator pane.
71:- A task that touches a trust boundary (anything the design tier lists, CI that decides a required check, code that executes PR-controlled input) carries a `threat_table` in its front matter: one `{control, disposition}` row per thing the PR or the orchestrator controls (the tree and its tests, task.md, workflow files, interpreter and environment files, in-process effects, new or renamed scripts, metadata separators). The row unit is one row per `allowed_files` entry, one row per listed control that is not a path (task metadata, workflow and interpreter or environment inputs, in-process effects, new or renamed scripts, metadata separators), carried by the declared test module's row where that is where the control acts, and one row per orchestrator effect from the fixed list (forced removal, merge, update-branch); under a wildcard `allowed_files` entry whose files are executed or applied (scripts, workflows, hooks, settings, the rules seats follow), one row per concrete file the PR changes; a wildcard over test fixtures or other data files keeps one row; C4 and C7b of `scripts/orchestrator/task-consistency-check.py` verify the path half before dispatch, and the task-file review checks the rest. A disposition takes one of three forms: `closed: tests/<file>::<name>`, the test that closes the row; `residual: <sentence>`, the compensating control; `out-of-scope: <task id>`, the task that owns the row. The task-file review checks the three shape rules by hand: a `closed` selector names a test present in the PR tree at acceptance, an `out-of-scope` owner is a task id in the design's `implementing_tasks`, a `residual` payload is a sentence of at least 20 characters (the gate's minimum for a reason). For a `closed` row it checks the selector's form only, since the test does not exist before implementation. Substance is the reviewers': the task-file review, the Bot and the auditor judge each row against the diff. The table is the task's completion condition: a missing row is added once, counted as an amendment, never fixed finding by finding.
84:    - Give codex the same task-level inputs the pair form builds: the task file `.orchestration/tasks/<id>.md` (required), the worker's report, validation and sandbox files and `<id>-pr-feedback.json` (those present), the final head `<head-sha>` and the PR diff `git diff $(git merge-base origin/main <head-sha>) <head-sha>`. Ask for findings as `[P0-P3] confidence dimension file:line rationale` and exactly one concluding `Verdict: correct|incorrect|blocked` line.
85:    - Run `rm -f <out> <out>.last.md && set -o pipefail && codex <MODEL_PROFILE_AUDIT_CODEX_ARGS> exec --sandbox read-only -C <repo> -o <out>.last.md '<that prompt>' 2>&1 | tee <out>`. Removing both files first means a failed rerun can never leave an earlier `Verdict: correct` behind, as the pair form also ensures, and `pipefail` keeps codex's exit status through `tee`. A nonzero codex exit means no audit: there is nothing to gate, so rerun it.
88:  - Run either form from a clean tree: the only untracked content in the audited checkout is this task's `.orchestration` evidence that the audit prompt names (task file, report, validation, sandbox file, feedback JSON). Otherwise run it from a dedicated clean checkout, so no other edit can reach the auditor.
105:expected_sandbox_file=<path> expected_learning_file=<path>
116:report=<path> validation=<path> sandbox=<path> learning=<path> autoskill=<path>
150:- `sandboxes/`: per-task isolation records (sandbox/worktree evidence).
161:3. Write a task file that includes objective, scope, allowed files, forbidden actions, expected artifacts, validation commands, and max turns. Name the render check as `make render-check`, never the bare `python3 scripts/generate-agent-configs.py --check`, which fails without PyYAML. Ground `allowed_files` by grepping the repository for every touch point the task names (tests that pin call sequences, mirrors, fixtures) before dispatch. Verify every CLI constraint the task asserts by running the real command in a safe form, not by reading `--help`. Presume an auditor finding that contradicts your own review is right until you refute it with evidence. Decide the worker kind from the allowed files before dispatch: a seat never edits the source of its own execution boundary, so a change is routed by the boundary it touches. A change that touches only Claude's boundary goes to a Codex seat: the `claude.permissions`, `claude.sandbox` and `claude.hooks` blocks of `home/dot_agents/agent-config.yaml` (including excludedCommands, allowUnsandboxedCommands, writable roots, network and the PermissionRequest hook), the Claude-rendering parts of `scripts/generate-agent-configs.py`, the rendered `home/.chezmoitemplates/claude-settings-managed.json`, and `home/dot_claude/modify_private_settings.json`. A change that touches only Codex's boundary goes to a Claude seat: `codex.sandbox_workspace_write`, `codex.approval_policy`, the Codex-rendering parts of the renderer, and `home/.chezmoitemplates/codex-config-managed.toml`. A change that touches both, or a shared source the orchestrator cannot split (such as `codex.sandbox_workspace_write.writable_roots`, which also renders into Claude's `allowWrite`), goes to the operator. The orchestrator decides the kind from the diff the task will produce and records it and the chosen worker profile in the task file. The Claude Code auto-mode classifier also refuses a Claude-boundary task on a Claude seat as Self-Modification. A task that edits permgate (`home/dot_agents/permgate-policy.yaml`, `home/dot_local/bin/common/executable_permgate`), the PermissionRequest hook of both seats, goes to the operator; a Codex `security`-profile worker reviews the change before the orchestrator accepts it, per the model-selection rule. `auto` is Claude Code's built-in starting permission mode since 2.1.283. A project-level `defaultMode: auto` (`.claude/settings.json` or `.claude/settings.local.json`) does not take effect, and the session then also ignores the user-level `defaultMode`, so `auto` belongs only in user or managed settings. Before dispatch, read the task's verbatim blocks against each other for contradictions, and state each rule once; a second artifact references the first instead of restating it.
168:10. For a RESULT that carries a pull request, integrate in this order. This is the single procedure that the PR integration rule, `AGENTS.md`, the README and the gh-first-workflow skill cite. A `gh pr update-branch` moves the head, so steps 1 to 4 run again on the new head. After an update-branch the orchestrator runs it, the order is CI on the new head, then the sweep, then the audit; an audit started before CI finishes sees incomplete evidence and returns an evidence-only `incorrect`. Select a checkout with git -C <absolute path>, never with cd, which the sandboxed Bash may not honour. After moving the review worktree to the audited head, verify git -C <review> rev-parse HEAD equals that head and git -C <main> symbolic-ref --short HEAD prints main before the audit and the gate.
190:2. Switch to the `repo` and read `task_file` before editing or running validations. Create the task branch without touching the shared `.git/config`, which is read-only for a Codex seat by design (T64 writable roots): `git switch -c <branch> --no-track origin/main`, push with `git push origin <branch>` (no `-u`), and open the PR as a draft with `gh pr create --draft --head <branch>`. Commit inside the sandbox, with `git -c commit.gpgsign=false` when the signing key is unreadable there; for a Claude seat only the push leaves the sandbox, and a Codex seat pushes from inside it (step 4). A Claude seat's sandbox can leave the same failed write behind, so it uses the same commands. A leftover `.git/config.lock` from a failed attempt is removed by the orchestrator. Remove a scratch worktree (for example one that proves a test fails on `origin/main`) with `git worktree remove <path>` only; never run `git worktree prune` from a sandboxed seat, because other worktrees' paths look missing inside the sandbox and prune then targets their admin directories in the shared `.git/worktrees`.
192:4. Do not perform any `forbidden_actions`. Complete every command inside the sandbox and allowlist; never escalate an action outside that boundary for approval. Fail it instead, send `AGMSG-PONG v1 status=blocked` with the exact command and the boundary it crosses, and wait for the orchestrator to re-task. Agent-to-agent permission approval is forbidden: only the human operator answers a permission prompt. A Claude Code auto-mode classifier denial (for example Self-Modification) is such a boundary: stop without a diff, send `AGMSG-PONG v1 status=blocked` naming the classifier reason, and never pursue the same outcome through another tool. Fetch and fast-forward inside the sandbox; a public remote needs no credential. For Claude seats on macOS, Seatbelt denies the Mach lookup of `com.apple.trustd.agent`, so Go-based CLIs (`gh`, `gcloud`, `terraform`) fail TLS verification with `x509: OSStatus -26276` (`errSecInternal`); `git` uses Apple libcurl, LibreSSL and `/etc/ssl/cert.pem` and succeeds. On Linux, the bubblewrap sandbox denies the AF_UNIX keyring socket, so `gh` answers HTTP 401; `allowUnixSockets` cannot grant a path. Monitor and process visibility limits are in "Identity, delivery, and storage". On both platforms a Claude seat runs three commands outside the sandbox through the permission gate: `gh`, `git push`, and an authenticated `git fetch` (a private HTTPS remote, whose credential helper is `gh`); `excludedCommands` and `enableWeakerNetworkIsolation` are operator options, not selected alternatives. Look up a VERIFY item's external reference (upstream documentation, release notes, an API schema) with the WebFetch tool, not Bash `curl`. Three documented cases run outside the sandbox too: the task's main-checkout CompactionDB `memory add`, through the permission gate because that state directory is read-only from a worktree sandbox; writing the task's artifacts at their expected main-checkout paths and masking them with the repository masker, through the permission gate because the main checkout is not writable from a worktree sandbox; and `agmsg-dispatch`, through `excludedCommands` (step 11). Every other out-of-sandbox action stays a blocked PONG. A Codex seat has in-sandbox network (T64) and never leaves its sandbox.
193:5. Write artifacts to the exact expected paths (a Claude seat writes them through the permission gate, step 4). Do not invent alternate paths. A seat whose sandbox cannot write the main checkout (a Codex seat) writes them at the same relative paths in its own worktree, untracked, and the RESULT says so; the orchestrator moves them into the main checkout by absolute path before review. Worker-side review evidence carries a `-worker-` infix (`<task>-worker-crit.json`, `<task>-worker-review-receipt.md`), so it never collides with the orchestrator's own files.
195:7. Put the isolation status or fallback rationale in `expected_sandbox_file`.
199:11. Reply with the requested `done_signal`, normally `AGMSG-RESULT v1`, and include all artifact paths. To a herdr-paned orchestrator, send RESULT and PONG with `agmsg-dispatch <team> <worker> <orchestrator> <pane_id>` (for example `wN:p1`; single-line, shell-safe text) rather than bare `send.sh`, so the wake starts the idle orchestrator's turn and its Stop hook delivers the message. The Claude sandbox manifest lists `agmsg-dispatch` in `claude.sandbox.excludedCommands`, so a Claude worker runs it outside the sandbox from the first attempt: no failed sandboxed run, no unsandboxed retry, and no escalation. Claude Code still applies its permission rules to excluded commands, so the managed settings allow `Bash(agmsg-dispatch:*)` (the only managed `permissions.allow` entry) and the dispatch runs without a prompt. A Codex seat runs under Codex's own sandbox, which this setting does not cover.
203:    - A worker cannot reliably stop the server itself (verified with crit v0.21.1 on a scratch `crit plan`). Inside the sandbox, `crit stop` always reports no running daemon. Outside it, `crit stop` stops the plan server only on the branch the server was started on, so it misses a server started before `git switch -c <task-branch>`, which is the common worker case. `crit stop <plan-file>` does not match a plan session on any branch. An unsandboxed `crit stop` is also not pre-approved.
204:    - A worker cannot inspect the host for the server either. Neither seat may leave its sandbox for host commands, because that would be an escalation, which step 4 forbids. For a Claude seat on macOS or Linux, the platform-specific process limits in "Identity, delivery, and storage" also apply here; no sandboxed host inspection is attempted.
206:    - The orchestrator handles it as control-plane hygiene on the host. It runs these `pgrep`/`ps`/`kill` calls outside its own sandbox through the permission gate (`dangerouslyDisableSandbox`, answered by the operator or the auto-mode classifier) under its control-plane exemption, as it already does for `agmsg-dispatch` and `herdr-agents --audit`. It lists servers with `pgrep -fl _serve`, where a process named `crit` is a Crit server and the calling shell is listed under its own name. It reads each server's session record (`~/.crit/sessions/*.json` holds `pid`, `cwd` and `branch`) and confirms the server is live before acting: `ps -o args= -p <pid>` must show `crit _serve`, and the record's `cwd` must be that worker's worktree. The live process's own cwd must also match: `readlink /proc/<pid>/cwd` on Linux (`lsof -a -d cwd -p <pid> -Fn` on macOS) must equal the record's `cwd`. A mismatch means the pid was reused, and the record is stale. Only then does it stop the server with `kill <pid>`. A record whose pid is gone or runs another command is stale; it is removed, never killed. Never use `crit stop --all`, which stops every seat's server.

 succeeded in 225ms:
.orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md:48:- 2026-10-19T06:23Z: the amendment-1 text (the review-profile a02 output re-targeted to a01: the inherited make format clause, the portable tracked settings.json with host paths only in the rendered guard, the Codex network_access item removed to the Claude-seat task dotfiles-T133-codex-worker-network-a01) installed; checker OK; its C-80 review started 06:23Z; dispatch to a010 on correct.
   Worker launch roots, sibling worktrees and unrelated checkouts execute no guarded project code. Missing or unresolvable launch-root identity also executes no supplied command. Event cwd does not change the launch-root decision.

   The guard also binds the formatter and project-map reload to the edited file path from the hook's tool input and its owning repository. When the resolved path is outside canonical `CLAUDE_PROJECT_DIR` or belongs to a worker repository under `.claude/worktrees/`, the guard exits 0 without running the command. Worker-repository configuration, including Prettier JavaScript configuration and ruff settings, is never consumed by an orchestrator hook.

   The guard preserves argument boundaries, stdin and child exit status. It performs no eval, PATH interpreter lookup or worktree-relative script selection. Its portable caller starts with `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}"` followed by `"$HOME/.claude/hooks/orchestrator-only.sh"` and a fixed operation identifier with its arguments. The shell running the hook expands `$HOME`. The prefix re-exports `HOME` from the launcher environment as `HOME="$HOME"` before any path that uses it and explicitly re-exports the launch identity and the few variables Claude Code documents for hooks. No interpreter or anchored script path is supplied by the tracked settings.

   The pinned PATH differs by role. Worker-session hooks use `/usr/bin:/bin`. For the orchestrator's formatter and project-map hooks, which the guard runs only in orchestrator sessions, the guard itself sets PATH to a rendered list of absolute tool directories of the trusted root before executing the guarded command. Those directories hold `ruff`, `prettier` and `terminal-browser` and are resolved by the render from the manifest without using mise shims. The formatter and project-map scripts remain outside `allowed_files` and unchanged.

   `tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_project_guard_uses_launch_root_and_never_runs_worker_payloads` plants worker Stop, contextdb and formatter payloads. Worker and unrelated-root invocations leave all markers absent. The positive-path case runs the complete rendered command in a subprocess with a fake `CLAUDE_PROJECT_DIR` equal to the anchored checkout and asserts that the guarded script executed while preserving its arguments and status. A second case runs the complete rendered command with a worktree `CLAUDE_PROJECT_DIR` and asserts that the guarded script did not execute. A planted `BASH_ENV` in the outer environment remains unexecuted in both cases. Formatter and project-map reload cases keep `CLAUDE_PROJECT_DIR` anchored and supply hook tool input for an outside file and a worker-repository file under `.claude/worktrees/`; both exit 0 with command and planted configuration markers absent. Matching anchored-file inputs run both commands normally. The guard tests execute the portable HOME-relative hook command against separately rendered per-host guards, assert the `HOME="$HOME"` re-export and verify that interpreter and anchor selection occurs only inside the rendered guard. Changing `CLAUDE_PROJECT_DIR` never changes the selected executable.

9. `.claude/settings.json` retains its tracked project hooks and rewrites every command through the installed orchestrator-only guard.

   This tracked file is not a chezmoi template and remains portable across hosts. Every command starts with `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}"` followed by `"$HOME/.claude/hooks/orchestrator-only.sh"` and a fixed operation identifier with its arguments. The shell running the hook expands `$HOME`, and the clean environment re-exports the launcher's HOME before any path that uses it. The file names no interpreter, anchor path, private links directory or host-specific tool directory.

   Host-specific absolute bindings live only inside the per-host rendered guard and rendered worker settings. The guard binds the selected operation to its absolute interpreter and anchored script path. Contextdb commands do not invoke bare `python3` or select `.claude/hooks` from a worker checkout. The Stop gate does not invoke bare `bash` or a worker checkout's `scripts/agent-stop-gate.sh`. `CLAUDE_PROJECT_DIR` never selects an executable.

   Every hook entry carries `onFailure: "block"`. Existing event functions remain available to the anchored orchestrator. They are no-ops in worker sessions because the guard rejects their launch roots.

   `tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_every_tracked_project_hook_is_guarded_and_blocks_on_failure` traverses every event, matcher and command entry. It rejects unguarded commands, missing failure policy, missing `/usr/bin/env -i` prefixes with the specified HOME re-export, interpreter or anchor paths in the tracked file and worker-selected executable paths. Render fixtures use distinct homes and anchors and assert that the tracked commands stay identical while the guard and worker settings receive their own host bindings.

10. `home/dot_local/bin/common/executable_herdr-agents` supplies the dedicated worker configuration at the actual worker launch boundary.

    Every Claude worker pane starts with `CLAUDE_CONFIG_DIR=<absolute-home>/.claude-worker`. This value reaches the actual worker process through the pane command and environment construction. Setting it only in the parent spawn process does not satisfy this requirement.

    Managed-workspace and standalone-worker routes receive the same binding. Repeated starts do not inherit a conflicting caller Claude configuration directory. This task introduces no worker gh configuration directory, gh templates or credential-separation claim.

    Every worker launch exports `UV_CACHE_DIR=<absolute-worktree>/.uv-cache` and `UV_PYTHON_INSTALL_DIR=<absolute-worktree>/.uv-cache/python`. Both worker kinds receive values derived from the selected canonical worktree. Caller-provided values do not replace them.

    The launcher stops writing Claude worker delivery hooks and merge denials into worktree-local `.claude/settings.local.json`. It renders the worker delivery hooks and native merge denials into `~/.claude-worker/settings.json`, the user-level settings file selected for that directory.

    Before every Claude worker start, the launcher also migrates the legacy worktree-local file. Claude Code loads the worktree's own `.claude/settings.local.json` alongside the main checkout's local settings, so a previously generated delivery entry there would stay effective with its unsanitized environment and PATH-resolved interpreter. The launcher removes every managed delivery hook entry it previously wrote from `<worktree>/.claude/settings.local.json`, keeps that file's unrelated entries, and refuses to start the worker while a command hook it did not write remains there, naming the entry. The effective hook set is asserted across the three files Claude Code loads for a linked worktree (worker user settings, the main checkout's local settings, the legacy worktree-local file) with a fixture holding a previously generated unsanitized entry: `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_add_worker_migrates_legacy_worktree_local_hooks` is red at the base and green on the final head.

    Before every Claude worker start, managed worker delivery entries are regenerated from trusted inputs. An existing delivery match does not skip preparation. Stale managed commands are replaced, unknown command hooks are not promoted into the trusted delivery set and the effective delivery set contains no duplicate managed invocation.

    The launcher also regenerates its managed hooks in the main checkout's `.claude/settings.local.json`. Every local agmsg delivery and orchestrator attachment command that it writes runs through the installed orchestrator-only guard. The existing permissions object and unrelated non-hook settings remain stored. Their effective sandbox interpretation follows the administrative managed policy.


**Tracking file changes and security controls**
**Assessing design consistency and deployment prerequisites**
web search: 
web search: 'profile'
exec
/bin/zsh -lc 'nl -ba .orchestration/tasks/dotfiles-T133-codex-worker-network-a01.md; nl -ba .orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md | tail -28; shasum -a 256 .orchestration/tasks/dotfiles-T133-codex-worker-network-a01.md' in ~/Workspace/dotfiles
exec
/bin/zsh -lc "sed -n '50,55p' ~/.agents/skills/agmsg-orchestration/SKILL.md; sed -n '71,74p' ~/.agents/skills/agmsg-orchestration/SKILL.md; sed -n '1235,1280p' scripts/generate-agent-configs.py; rg -n 'network_access|ask-for-approval|--sandbox' home/dot_local/bin/common/executable_herdr-agents | head -35" in ~/Workspace/dotfiles
 succeeded in 128ms:
     1	---
     2	format: 2
     3	task_id: dotfiles-T133-codex-worker-network-a01
     4	kind: code
     5	security: true
     6	allowed_files:
     7	  - home/dot_agents/agent-config.yaml
     8	  - scripts/generate-agent-configs.py
     9	  - tests/unit/test_generate_agent_configs.py
    10	  - home/dot_codex/modify_private_standard.config.toml
    11	  - home/dot_codex/modify_private_security.config.toml
    12	  - .orchestration/dotfiles-T133-codex-worker-network-a01/**
    13	after: [dotfiles-T133-worker-write-boundary-a01]
    14	threat_table:
    15	  - control: home/dot_agents/agent-config.yaml
    16	    disposition: "residual: only the standard and security Codex profiles gain sandbox network access; the shared sandbox defaults, writable roots, approval policy and permission hooks remain unchanged."
    17	  - control: scripts/generate-agent-configs.py
    18	    disposition: "closed: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_codex_worker_network_is_profile_scoped"
    19	  - control: tests/unit/test_generate_agent_configs.py
    20	    disposition: "residual: render tests execute generated modify scripts in temporary homes and parse their TOML output without accessing credentials or performing network operations."
    21	  - control: home/dot_codex/modify_private_standard.config.toml
    22	    disposition: "closed: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_codex_worker_network_is_profile_scoped"
    23	  - control: home/dot_codex/modify_private_security.config.toml
    24	    disposition: "closed: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_codex_worker_network_is_profile_scoped"
    25	  - control: .orchestration/dotfiles-T133-codex-worker-network-a01/**
    26	    disposition: "residual: task artifacts contain the dispatched copy and evidence for this task alone; the final-head audit compares their claims with the diff and CI."
    27	  - control: the task-file copy on the branch (.orchestration/dotfiles-T133-codex-worker-network-a01/task.md)
    28	    disposition: "residual: the copy is byte-identical to the dispatched text; TASK and RESULT bind its own sha256 and the orchestrator compares it at acceptance."
    29	  - control: the branch evidence records under .orchestration/dotfiles-T133-codex-worker-network-a01/ (report.md, validation.md, sandbox.md, learning.md and worker review evidence)
    30	    disposition: "residual: records contain prose and command output; sandbox.md lists every refused command and the audit distinguishes rendered configuration from live enforcement."
    31	  - control: task metadata
    32	    disposition: "residual: the orchestrator checks C1 to C10 and C7b before dispatch and at acceptance; the task-copy byte comparison covers the complete dispatched front matter."
    33	  - control: metadata separators
    34	    disposition: "residual: the checker reads the first YAML front-matter document and the task-copy byte comparison covers every separator."
    35	  - control: in-process effects
    36	    disposition: "residual: rendering changes repository artifacts and temporary test outputs; the worker performs no deployment, authentication change, live policy edit or sandbox-escape probe."
    37	  - control: workflow and interpreter or environment inputs
    38	    disposition: "residual: workflow files, interpreter selection, launch arguments and shell environment policy remain unchanged; tests use the existing unittest and temporary-home conventions."
    39	  - control: new or renamed scripts
    40	    disposition: "residual: no script is added or renamed; the existing renderer and two generated profile modify scripts retain their existing responsibilities."
    41	  - control: design section 5.14 item 1 (Codex worker write boundary)
    42	    disposition: "residual: worker outbound traffic goes through the Codex sandbox with network access enabled; existing writable roots and filesystem restrictions remain unchanged, and this configuration does not establish isolation from same-UID host processes."
    43	  - control: design section 5.14 item 10 (worker commands remain inside the sandbox, D-024-17a)
    44	    disposition: "residual: gh and git push use network access inside the Codex sandbox; the worker never retries outside it, while the permgate Codex no-escape rule remains pending operator action and is not claimed as implemented."
    45	  - control: orchestrator effect merge
    46	    disposition: "residual: the orchestrator merges only through gh pr merge --squash --match-head-commit <audited head> after the integration gate in Orchestrator Playbook step 10."
    47	  - control: orchestrator effect update-branch
    48	    disposition: "residual: gh pr update-branch moves the head, so CI, the feedback sweep, the task-level audit and the security review bind the new final head before the gate."
    49	  - control: orchestrator effect forced worker removal
    50	    disposition: "residual: no forced removal is planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and any forced removal records discarded uncommitted state in acceptance."
    51	premises: []
    52	---
    53	
    54	# AGMSG-TASK dotfiles-T133-codex-worker-network-a01 — plan 024 P1-15's Codex-side item split out for routing (D-024-17a)
    55	
    56	## Goal
    57	
    58	The Codex worker profiles `standard` and `security` set `sandbox_workspace_write.network_access = true` so `gh` and `git push` run inside the Codex sandbox through its network, as specified by `.orchestration/plans/024-design-quality.md` section 5.14 items 1 and 10 and decision D-024-17a. The shared base configuration and the `audit`, `review`, `express` and `deep` profiles retain their existing behavior. No other sandbox setting changes, and writable roots remain unchanged. This Codex-boundary change is assigned to a Claude seat using the `security` profile under the routing invariant.
    59	
    60	## Files
    61	
    62	1. `home/dot_agents/agent-config.yaml` declares `sandbox_workspace_write.network_access: true` under `model_profiles.standard.codex` and `model_profiles.security.codex`.
    63	
    64	   The shared `codex.sandbox_workspace_write.network_access` remains `false`. The shared block currently supplies one sandbox configuration to all profiles, so the change uses worker-profile overrides. The manifest's writable roots, sandbox modes, approval policy, permission-request hook and Claude settings remain unchanged.
    65	
    66	2. `scripts/generate-agent-configs.py` renders the declared worker-profile network overrides through `render_codex_profile`.
    67	
    68	   The renderer currently emits the sandbox network setting only in the shared base configuration. A renderer change is therefore required and is included in `allowed_files`. The new profile table overrides only `network_access`. It introduces no writable-root override or launcher-specific setting.
    69	
    70	3. `tests/unit/test_generate_agent_configs.py` adds `tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_codex_worker_network_is_profile_scoped`.
    71	
    72	   The test uses the existing `unittest`, generated modify-script and temporary-home patterns. It checks the manifest's two worker-profile declarations and parses rendered profile TOML with `tomllib`. The rendered `standard` and `security` profiles carry `network_access = true`. The shared base retains `network_access = false`, and the rendered `audit`, `review`, `express` and `deep` profiles remain unchanged. The audit profile retains its `read-only` sandbox mode, and existing writable-root settings remain unchanged.
    73	
    74	   The test is written before the manifest and renderer changes. Its assertions fail against the unchanged implementation and pass after the change. The existing audit-profile and runtime-state preservation tests remain green.
    75	
    76	4. `home/dot_codex/modify_private_standard.config.toml` and `home/dot_codex/modify_private_security.config.toml` are regenerated through the existing generator.
    77	
    78	   These two tracked paths are included in `allowed_files` as regeneration-only outputs. They receive no manual edits. Other generated outputs remain unchanged.
    79	
    80	5. `.orchestration/dotfiles-T133-codex-worker-network-a01/` contains the byte-identical dispatched `task.md`, `report.md`, `validation.md`, `sandbox.md`, `learning.md` and worker review evidence. Worker review filenames carry the required `-worker-` infix.
    81	
    82	   The report maps the requirements to test selectors and states the user-visible effect that Codex sessions selecting `standard` or `security` gain sandbox network access. It states that this boolean setting supplies no outbound domain allowlist.
    83	
    84	   The report prepares the operator's exact deterministic rule that stops Codex PermissionRequest handling from approving sandbox escapes or unsandboxed retries. It identifies the insertion point before allow-pattern evaluation in `home/dot_local/bin/common/executable_permgate::decide`, the policy source `home/dot_agents/permgate-policy.yaml` and the existing `permgate codex` hook binding. It accounts for unsupported request shapes without allowing an escape. This is proposed operator text, and neither permgate source is changed by the worker.
    85	
    86	## Out of scope
    87	
    88	Permgate code, deterministic policy and permission-request hook changes belong to the operator. The worker performs no live policy edit or escape probe.
    89	
    90	The Claude-side boundary of P1-15 belongs to `dotfiles-T133-worker-write-boundary-a01`. D-024-20 makes that task's merge a dispatch prerequisite. This task's branch is rebased onto `origin/main` after that merge and before implementation.
    91	
    92	Any writable-root change is outside this task. Sandbox modes, approval policy, launch arguments, authentication, credential storage and deployment remain unchanged. The dropped wrapper design is not reintroduced.
    93	
    94	## Measurements
    95	
    96	The caps in Check are measured from their analogues on `origin/main` (C-79). Source: the existing per-profile `sandbox_mode` override is 2 renderer lines (`scripts/generate-agent-configs.py:598-600`) and 1 manifest line; the network override adds a `[sandbox_workspace_write]` table with one key in `render_codex_profile` (about 6 lines), 2 manifest lines and the matching lines in `render_codex_profile_modify` (line 1036; about 10), so about 20 lines, capped at 40. Tests: the analogous `test_audit_profile_renders_read_only_sandbox_override` is 37 lines (`tests/unit/test_generate_agent_configs.py:795-831`); one test of the same shape is capped at 80.
    97	
    98	## Check
    99	
   100	`make render-check`, `make validate-agent-assets`, `make format` and `uv run --no-project --with pyyaml python -m unittest tests.unit.test_generate_agent_configs -v` have their commands, verbatim output, exit statuses and tested heads pasted in `.orchestration/dotfiles-T133-codex-worker-network-a01/validation.md`. The render check, asset validation and unit module are green.
   101	
   102	The new profile-scoping test carries red-before-implementation and green-final-head evidence. Render evidence identifies both changed worker profiles and all four unchanged orchestrator-side profiles. It records the unchanged base sandbox block and writable roots. These tests establish rendered configuration behavior and make no claim of live sandbox enforcement. No local Bats tests run.
   103	
   104	An inherited formatting failure is reproduced on the unchanged base and recorded with its output. It remains a reported failure and receives no repair outside `allowed_files`.
   105	
   106	`git diff --numstat origin/main...HEAD` shows at most 40 changed lines outside `tests/` and `.orchestration/`, excluding the regenerated `home/dot_codex/modify_private_standard.config.toml` and `home/dot_codex/modify_private_security.config.toml`, and at most 80 changed lines under `tests/`. Changed lines are additions plus deletions. Validation includes per-file numstat, both totals and the complete changed-file inventory.
   107	
   108	The orchestrator runs the format-2 task-consistency checker, including C1 to C10 and C7b, before dispatch and at acceptance. The task text and threat table pass the security-profile C-80 review before dispatch, and its findings enter the task's finding-class table. The task copy remains byte-identical to the dispatched file.
   109	
   110	## Completion
   111	
   112	The Completion clause of `.orchestration/tasks/dotfiles-T133-hold-playbook-a01.md` applies with `dotfiles-T133-codex-worker-network-followup-a01` as the owner of any advisory P2 and `task_copy=<sha256 of .orchestration/dotfiles-T133-codex-worker-network-a01/task.md>` in the RESULT. This task's scope, Check, `security: true`, prerequisite, Claude-seat routing and evidence paths govern that reference.
   113	
   114	One PR starts from a fresh branch off `origin/main`. The orchestrator writes the advisory owner task before recording its first ownership disposition. A small in-scope P2 follows the inherited `check=` revise procedure while INV-6 permits it.
   115	
   116	The worker's own pre-push review is one round at most. Every worker-side fix round counts toward INV-6. A surviving P0/P1 is sent in the RESULT as `open:<finding-or-thread-id>` and stops integration for the operator's decision. The worker starts no additional private correction-and-review cycle. The third finding of one class stops further rounds until the orchestrator's re-plan.
   117	
   118	The RESULT identifies the final head, base, branch, changed files, test selectors, measured caps, evidence paths, task-copy hash, pending operator step and every Bot finding's proposed disposition. It carries the precheck evidence required by the applicable RESULT procedure.
   119	
   120	The orchestrator runs the task-level audit and the security review on the final head and dispositions every finding before the gate. Final-head CI, the feedback sweep, audit, security review, acceptance record, gate and merge follow Orchestrator Playbook step 10 and the repository's security-review requirements. A changed head receives fresh evidence.
   121	
   122	No `@codex review` comment is issued. Every `gh` write and Git write runs as an individual command without shell chaining or a wrapper combining writes. Every worker command remains inside its sandbox. An operation that cannot complete there produces a blocked PONG naming the exact command and refusal, with no retry outside the sandbox.
   123	
   124	## Checks (pasted by the orchestrator before each send)
   125	
   126	```
   127	(pasted at dispatch)
   128	```
   129	
   130	Implementation and runtime verification remain pending worker execution.
   131	Unrestricted outbound sandbox network access and the pending operator permgate rule remain residuals.   501	
   502	This task is `security: true`. The orchestrator obtains the task-level audit and a separate security-profile review of the final implementation head. The finding-class record includes `decision-not-bound-to-execution`, `unbound-evidence` and `fail-open-on-error`. A third non-advisory finding of one class stops the artifact for redesign under the inherited completion rules.
   503	
   504	Final-head feedback collection, task-level audit, finding dispositions, acceptance and the integration gate follow Orchestrator Playbook step 10 in its prescribed order. The gate receives `PR_FEEDBACK_EVIDENCE`, `AUDIT_EVIDENCE`, `ACCEPTANCE_EVIDENCE` and the agent review receipt. Changed heads receive fresh required evidence. The final-head security review precedes the gate.
   505	
   506	The permission-surface change receives the required operator-backed approval through the repository's existing process. The worker writes no approval row and treats no candidate-tree decision as authority.
   507	
   508	Live deployment is the operator's post-merge `make update`. The operator runs `make install-managed-settings`, inspects the rendered staging file and executes its printed `sudo install -m 0644 "<absolute-home>/.claude/managed-settings.rendered.json" "<detected-managed-settings-path>"` command with `/Library/Application Support/ClaudeCode/managed-settings.json` detected on macOS and `/etc/claude-code/managed-settings.json` detected on Linux. Administrative installation is recorded separately from staging and ordinary chezmoi application.
   509	
   510	The operator performs the Claude worker-directory login with `CLAUDE_CONFIG_DIR=<absolute-home>/.claude-worker` selected.
   511	
   512	The operator applies the prepared deterministic Codex permgate rule that stops approving sandbox escapes and restarts affected sessions.
   513	
   514	The deployment record checks effective settings after `make update` and administrative installation, including hooks added by merge scripts or integration installers. It verifies the installed managed-settings content, admin-required sandbox scope, worker directory, both platform policy outputs, static deny inventory, worktree-configuration denies, writable agmsg stores, worker-user and main-local hook placement, hook PATH and interpreter descendants, failure-policy coverage and sandbox startup without exposing credentials.
   515	
   516	The effective-settings check includes conflicting project and local sandbox relaxations and confirms that they do not weaken the administrative policy. It also records the shared control-plane exclusions and Herdr socket as available capabilities. It makes no claim that worker user arrays subtract those entries.
   517	
   518	Merge alone does not establish deployment readiness. The orchestrator records `make update`, the managed-settings installation with sudo, the Claude worker-directory login, effective startup checks and the Codex permgate rule before releasing dependent hardening tasks for live operation. The upstream agmsg store-driver route remains a named residual until its owning task is implemented. GitHub remains detection, not prevention, until the operator pursues separate-user or separate-host isolation under future P1-16.
   519	
   520	## Checks (pasted by the orchestrator before each send)
   521	
   522	```
   523	2026-10-19T05:42Z dispatch 1: C-80 rounds 1-8 incorrect, round 9 correct (…-text-security-435275a)
   524	2026-10-19T06:2xZ amendment 1: task=dotfiles-T133-worker-write-boundary-a01 tasks=1 amendments=0 questions=0(the two questions came as status=running question=N, C-87) results=0 withdrawn=0 revises=0 source=live; C-80 of this amended text: (pasted after its review)
   525	```
   526	
   527	Local Bats, live enforcement, administrative installation, worker-directory login, permgate policy changes and deployment are not performed by the worker.
   528	Deployment remains unverified until the operator completes the post-merge steps; same-UID credential access, shared control-plane exclusions and Herdr socket access, writable-store driver selection and concurrent path consumption remain stated residuals.cf5efd587cf1990f91c044b03767261dbf1c2dc321f0fd18916f03d7b743a1d3  .orchestration/tasks/dotfiles-T133-codex-worker-network-a01.md

 succeeded in 133ms:
- Register `project` as the worker's real working-tree path (the dedicated worktree for parallel workers), byte-identical across join, delivery setup, and hook arguments. Trailing slashes and unresolved symlinks orphan inboxes through exact-string mismatch. `$HOME` registrations are forbidden because they create Codex-hook ambiguity and steal inbox messages.
- Register a worker identity at its own worktree path with resolution off: `AGMSG_RESOLVE_PROJECT=0 join.sh <team> <name> <type> <worktree>`, and point its delivery at the same path with `delivery.sh set <mode> <type> <worktree>` so the hook bakes the worktree into the session's project marker. Every `join.sh`/`whoami.sh`/`actas-claim.sh`/`reset.sh`/`watch.sh` call a worker makes runs with `AGMSG_RESOLVE_PROJECT=0` (herdr-agents sets it in every worker pane it creates; `spawn.sh --project` sets it for agmsg-spawned seats). Upstream project resolution (#92, `docs/design.md` "Project resolution") otherwise rewrites the path in order: the live SessionStart marker `run/proj.<agent_pid>.project`, then the nearest registered ancestor, then the registered main checkout via `git rev-parse --git-common-dir`. Verified against a scratch v1.5.0 install: a `join.sh` from inside `.claude/worktrees/<x>` without the opt-out registers at the main checkout; a session whose marker names the main checkout (a seat launched from the main path) makes `whoami.sh` inside the worktree answer with the main checkout's identities; the opt-out restores the worktree in both cases. `session-start.sh` exits before the watcher and marker for any session whose cwd is under `.claude/worktrees/` (#367), so a Claude seat launched inside a nested worktree gets no Monitor watch from that hook: the herdr-agents pair worker relies on turn delivery (a spawn-seated worker starts its Monitor through its actas boot) or the inbox checks below. `identities.sh` stays a pure lookup of the exact path.
- On activation, check `delivery.sh status <type> <repo>`. This repo runs Claude Code seats on `both` (monitor's push plus turn's pull), one notch more redundant than upstream's Claude Code default `monitor`, since an unattended worker pane has no one to notice a Monitor watch that silently failed to re-arm; Codex seats run on `turn` (see the next bullet). If weaker than that, run `delivery.sh set both claude-code <repo>` (or `delivery.sh set turn codex <repo>` for a Codex identity), use the SessionStart-provided `watch.sh <session_id> <repo> <type>` started outside the sandbox as a persistent in-session monitor, and claim exclusivity with `actas-claim.sh <project> <type> <name> <session_id>`. A Claude worker seated by `--add-worker` gets its Monitor watch through its actas boot; when it is seated in its own workspace (no managed workspace exists), `herdr-agents` also sets `AGMSG_CC_MONITOR_KEEP_ALIVE=1` in that workspace's environment so the watch re-arms unconditionally on expiry, not only when the expired watch delivered something (upstream's default).
- `herdr-agents --bootstrap-agmsg` (and full or attach mode) sets the main checkout's orchestrator hooks, Claude Code on `both`; a worker seat gets its own hooks from `herdr-agents --add-worker`, Codex on `turn` and Claude Code on `both`, so the Stop/SessionStart hook in the worktree's tree-scoped, gitignored `.codex/hooks.json` or `.claude/settings.local.json` delivers inbox messages. Codex deliberately stays on `turn` instead of upstream's shim-based `monitor` bridge (the upstream README names `monitor` as the Codex default in one place and `turn` in its delivery table): as of agmsg v1.5.0 that bridge has open reliability defects an unattended resident worker cannot risk — no teardown on session end (upstream #149), a mode switch that does not start the bridge in a live session (#151), and a bridge that restarts forever while its status reports it alive (#1236), all still open. Storage resolution is env-only: keep `AGMSG_STORAGE_PATH` unset for same-repository default-store workers, or set it to the regime's dedicated store for separate cross-project regimes; a wrong or stray value silently reroutes the worker to another database. Pane nudges are only generic wakes; message content always travels over agmsg.
- Worker panes run in their worktree: `herdr-agents --add-worker [<worktree>]` seats the worker in that worktree (default the manifest's `worker_worktree`, created from `origin/main` when missing), registers its identity there with `AGMSG_RESOLVE_PROJECT=0`, sets delivery on that path, and starts it through upstream `spawn.sh`, so turn delivery reaches the worker directly through the worktree's Stop hook and its Monitor watch comes from the actas boot (upstream `session-start.sh` skips sessions under `.claude/worktrees/`, #367). The interim worker inbox discipline (running `~/.agents/skills/agmsg/scripts/inbox.sh <team> <identity>` at each milestone: task start, push, CI green, before RESULT, after any PONG) is retired for a worktree-seated worker; it applies only to a worker still acting under a worktree-registered identity from a main-path pane, until `herdr-agents --remove-worker` and `--add-worker` re-seat it.
- A codex worker in a nested worktree gets `<common>/objects`, `<common>/refs`, `<common>/logs` and `<common>/worktrees/<name>` (`<common>` from `git -C <worktree> rev-parse --git-common-dir`) as writable roots from `herdr-agents` (`-c sandbox_workspace_write.writable_roots`, with the configured agmsg roots kept first), so local git operations need no escalation. The common dir itself, `config`, `hooks`, `info`, `HEAD` and `packed-refs` stay read-only. The worker seat runs with `--ask-for-approval never` and `sandbox_workspace_write.network_access=true`, so a GitHub fetch, push or `gh` call works inside the sandbox and the worker never prompts: there is no escalation for a worker, and an action outside the sandbox or forbidden by the execpolicy fails and is reported as `AGMSG-PONG v1 status=blocked`. The `sandbox_workspace_write.network_access` switch is a boolean, so the worker reaches any host (no domain allowlist is configured, unlike Claude Code's `allowedDomains`), and the permgate PermissionRequest hook never fires for the worker seat; it stays live for interactive Codex sessions, which keep on-request approvals and no sandbox network.
- A task that touches a trust boundary (anything the design tier lists, CI that decides a required check, code that executes PR-controlled input) carries a `threat_table` in its front matter: one `{control, disposition}` row per thing the PR or the orchestrator controls (the tree and its tests, task.md, workflow files, interpreter and environment files, in-process effects, new or renamed scripts, metadata separators). The row unit is one row per `allowed_files` entry, one row per listed control that is not a path (task metadata, workflow and interpreter or environment inputs, in-process effects, new or renamed scripts, metadata separators), carried by the declared test module's row where that is where the control acts, and one row per orchestrator effect from the fixed list (forced removal, merge, update-branch); under a wildcard `allowed_files` entry whose files are executed or applied (scripts, workflows, hooks, settings, the rules seats follow), one row per concrete file the PR changes; a wildcard over test fixtures or other data files keeps one row; C4 and C7b of `scripts/orchestrator/task-consistency-check.py` verify the path half before dispatch, and the task-file review checks the rest. A disposition takes one of three forms: `closed: tests/<file>::<name>`, the test that closes the row; `residual: <sentence>`, the compensating control; `out-of-scope: <task id>`, the task that owns the row. The task-file review checks the three shape rules by hand: a `closed` selector names a test present in the PR tree at acceptance, an `out-of-scope` owner is a task id in the design's `implementing_tasks`, a `residual` payload is a sentence of at least 20 characters (the gate's minimum for a reason). For a `closed` row it checks the selector's form only, since the test does not exist before implementation. Substance is the reviewers': the task-file review, the Bot and the auditor judge each row against the diff. The table is the task's completion condition: a missing row is added once, counted as an amendment, never fixed finding by finding.
- Before every acceptance action (revise, accept, merge) the orchestrator runs `scripts/regime-counters.sh <task id>` and pastes its output into the acceptance record. S2 is decided from INV-6's counts: each component the script prints is read from its output, and for each component it prints as `unknown` the record pastes the command and output that read the source INV-6 names for that component, or, while that source has no entry for the task, says so and pastes the reading of the interim record the orchestrator used in its place. S1 (plan 006: the same finding class three times on one artifact, from any reviewer) is decided from the record's finding-class table, which gives a class to every finding the PR-feedback sweep lists, whatever its disposition, and to every task-level audit finding; three rows of one class stop the artifact. Read that table over non-advisory rows only: list advisory P2 rows with their classes (`advisory-p2` and the `local:<sha7>:<n>` rows `local-advisory.sh` writes), exclude them from S1's three-rows count, and name the excluded rows in the record. The gate's S6 check still sees every ledger row, so an advisory class at three rows gets its `searches` entry from `acceptance-front-matter.py` like any other. INV-6's message and head counts and the S2 lines (`revises`, `amendments`, `questions`, `bot_p1_heads`) take no ledger rows; `scripts/regime-counters.sh` prints them unchanged.
- A change to a rule sentence requested of a worker travels as a task amendment (hashed, checked by `scripts/orchestrator/task-consistency-check.py` (C1 to C10 and C7b) before dispatch and at acceptance, confirmed by the review seat), never as a PONG answer.
- When a finding class reaches three on one artifact (the record's ledger) or `scripts/regime-counters.sh` prints an S1 candidate, the next acceptance action is the records search for that class, pasted into the record as the line `search: <class> -> <the matching mistake records or none>`, and the matching correction is applied when its mechanism is landed, or landed first when it is pending, mechanism by mechanism, before any dispatch; a class is a slug of `[a-z0-9-]` assigned at disposition time, never text taken from a review title. `scripts/orchestrator/three-repeat.sh <class>` validates the slug, runs the records search and the CompactionDB search without a shell and prints the line. The gate (`scripts/require-crit-review.py`, S6) refuses the merge for a ledger class at three or more rows whose `searches` entry does not equal the mistake records naming the class; `acceptance-front-matter.py` writes the entry from the same lookup. Pasting the `search:` line and applying the correction before any dispatch remain the orchestrator's rule. Every `not-applicable` disposition carries `; evidence=<command>` with the output pasted in the record.
                for runtime_name, runtime_chunk in managed_by_runtime_prefix.get(prefix, []):
                    if runtime_name == prefix and runtime_name not in current_by_name:
                        output.append(runtime_chunk)
                for current_index, current_name, current_chunk in current_group:
                    output.append(current_chunk)
                    emitted_current.add(current_index)
                for runtime_name, runtime_chunk in managed_by_runtime_prefix.get(prefix, []):
                    if runtime_name != prefix and runtime_name not in current_by_name:
                        output.append(runtime_chunk)
            else:
                output.extend(chunk for _, chunk in managed_by_runtime_prefix.get(prefix, []))
            emitted_runtime_prefixes.add(prefix)
        else:
            output.append(managed_chunk)
    for current_index, (current_name, current_chunk) in enumerate(current_chunks):
        if current_name is None or current_index in emitted_current:
            continue
        prefix = runtime_prefix(current_name)
        if prefix is not None:
            if prefix in emitted_runtime_prefixes:
                continue
            for grouped_index, _, grouped_chunk in current_by_runtime_prefix[prefix]:
                output.append(grouped_chunk)
                emitted_current.add(grouped_index)
            emitted_runtime_prefixes.add(prefix)
        elif current_name not in managed_names:
            output.append(current_chunk)
            emitted_current.add(current_name)
    merged = "".join(output)
    return guarded_merge(merged if merged.endswith("\\n") else merged + "\\n", current, declared_keys)


sys.stdout.write(merge_config(sys.stdin.read()))
'''.replace("__HOOK_TRUST_BLOCK__\n", render_hook_trust_block(manifest))


def render_model_profiles_env(manifest: dict[str, Any]) -> str:
    profiles = model_profiles(manifest)
    interactive_profile(manifest)
    lines = [
        "# Shell fragment sourced by agent launchers (herdr-agents).",
        f"# {GENERATED_HEADER}",
        f'MODEL_PROFILE_INTERACTIVE="{manifest["interactive_profile"]}"',
        f'HERDR_AGENTS_WORKER_KIND="{worker_kind(manifest)}"',
        f'HERDR_AGENTS_ORCHESTRATOR_KIND="{orchestrator_kind(manifest)}"',
    ]
33:#   `--ask-for-approval never` and `sandbox_workspace_write.network_access=true`,
144:codex or claude. A codex worker runs with --sandbox workspace-write,
145:--ask-for-approval never and sandbox_workspace_write.network_access=true: it
394:#   runs with --ask-for-approval never, so nothing escalates). Granted:
451:#   --sandbox workspace-write --ask-for-approval never --config
452:#   sandbox_workspace_write.network_access=true` for codex, plus the
474:    [[ ${kind} == claude ]] || args="--profile ${HERDR_AGENTS_WORKER_PROFILE} --sandbox workspace-write --ask-for-approval never --config sandbox_workspace_write.network_access=true"
1203:    printf 'herdr-agents: not in a Herdr pane, so the orchestrator pane is not started; start the worker on demand with "herdr-agents --add-worker %s [DIR]" and run the auditor headless as the agmsg-orchestration SKILL task-level audit bullet shows ("codex <audit profile args> exec --sandbox read-only -C <repo> -o <out>.last.md <prompt>"); %s.\n' \
2053:        printf 'herdr-agents: no managed Herdr workspace for %q; run herdr-agents %q (full mode) to create one, or run the audit headless as the agmsg-orchestration SKILL task-level audit bullet shows ("codex <audit profile args> exec --sandbox read-only -C <repo> -o <out>.last.md <prompt>").\n' "${workdir}" "${workdir}" >&2
2106:    printf -v audit_inner "cd -- %q && set -o pipefail && rm -f -- %q && codex%s exec --sandbox read-only -C %q -o %q %q 2>&1 | tee -- %q; printf '%s:%%s\\\\n' \"\$?\"" \

**Evaluating deployment and merge tests**
**Assessing safe AST parsing**
exec
/bin/zsh -lc "sed -n '62,92p' .orchestration/tasks/dotfiles-T133-regime-ci-followup-a01.md; sed -n '71p' ~/.agents/skills/agmsg-orchestration/SKILL.md" in ~/Workspace/dotfiles
exec
/bin/zsh -lc "nl -ba scripts/generate-agent-configs.py | sed -n '1243,1288p'; sed -n '850,912p' tests/unit/test_generate_agent_configs.py; rg -n 'network_access|ask-for-approval|--sandbox' home/dot_local/bin/common/executable_herdr-agents" in ~/Workspace/dotfiles
 succeeded in 90ms:
```
- A task that touches a trust boundary (anything the design tier lists, CI that decides a required check, code that executes PR-controlled input) carries a `threat_table` in its front matter: one `{control, disposition}` row per thing the PR or the orchestrator controls (the tree and its tests, task.md, workflow files, interpreter and environment files, in-process effects, new or renamed scripts, metadata separators). The row unit is one row per `allowed_files` entry, one row per listed control that is not a path (task metadata, workflow and interpreter or environment inputs, in-process effects, new or renamed scripts, metadata separators), carried by the declared test module's row where that is where the control acts, and one row per orchestrator effect from the fixed list (forced removal, merge, update-branch); under a wildcard `allowed_files` entry whose files are executed or applied (scripts, workflows, hooks, settings, the rules seats follow), one row per concrete file the PR changes; a wildcard over test fixtures or other data files keeps one row; C4 and C7b of `scripts/orchestrator/task-consistency-check.py` verify the path half before dispatch, and the task-file review checks the rest. A disposition takes one of three forms: `closed: tests/<file>::<name>`, the test that closes the row; `residual: <sentence>`, the compensating control; `out-of-scope: <task id>`, the task that owns the row. The task-file review checks the three shape rules by hand: a `closed` selector names a test present in the PR tree at acceptance, an `out-of-scope` owner is a task id in the design's `implementing_tasks`, a `residual` payload is a sentence of at least 20 characters (the gate's minimum for a reason). For a `closed` row it checks the selector's form only, since the test does not exist before implementation. Substance is the reviewers': the task-file review, the Bot and the auditor judge each row against the diff. The table is the task's completion condition: a missing row is added once, counted as an amendment, never fixed finding by finding.

 succeeded in 100ms:
  1243	                        output.append(runtime_chunk)
  1244	            else:
  1245	                output.extend(chunk for _, chunk in managed_by_runtime_prefix.get(prefix, []))
  1246	            emitted_runtime_prefixes.add(prefix)
  1247	        else:
  1248	            output.append(managed_chunk)
  1249	    for current_index, (current_name, current_chunk) in enumerate(current_chunks):
  1250	        if current_name is None or current_index in emitted_current:
  1251	            continue
  1252	        prefix = runtime_prefix(current_name)
  1253	        if prefix is not None:
  1254	            if prefix in emitted_runtime_prefixes:
  1255	                continue
  1256	            for grouped_index, _, grouped_chunk in current_by_runtime_prefix[prefix]:
  1257	                output.append(grouped_chunk)
  1258	                emitted_current.add(grouped_index)
  1259	            emitted_runtime_prefixes.add(prefix)
  1260	        elif current_name not in managed_names:
  1261	            output.append(current_chunk)
  1262	            emitted_current.add(current_name)
  1263	    merged = "".join(output)
  1264	    return guarded_merge(merged if merged.endswith("\\n") else merged + "\\n", current, declared_keys)
  1265	
  1266	
  1267	sys.stdout.write(merge_config(sys.stdin.read()))
  1268	'''.replace("__HOOK_TRUST_BLOCK__\n", render_hook_trust_block(manifest))
  1269	
  1270	
  1271	def render_model_profiles_env(manifest: dict[str, Any]) -> str:
  1272	    profiles = model_profiles(manifest)
  1273	    interactive_profile(manifest)
  1274	    lines = [
  1275	        "# Shell fragment sourced by agent launchers (herdr-agents).",
  1276	        f"# {GENERATED_HEADER}",
  1277	        f'MODEL_PROFILE_INTERACTIVE="{manifest["interactive_profile"]}"',
  1278	        f'HERDR_AGENTS_WORKER_KIND="{worker_kind(manifest)}"',
  1279	        f'HERDR_AGENTS_ORCHESTRATOR_KIND="{orchestrator_kind(manifest)}"',
  1280	    ]
  1281	    if (profile_name := worker_profile(manifest)) is not None:
  1282	        lines.append(f'HERDR_AGENTS_WORKER_PROFILE="{profile_name}"')
  1283	    if (worktree := worker_worktree(manifest)) is not None:
  1284	        lines.append(f'HERDR_AGENTS_WORKER_WORKTREE="{worktree}"')
  1285	    for name, profile in sorted(profiles.items()):
  1286	        var = str(name).upper()
  1287	        claude = profile["claude"]
  1288	        claude_args = f"--model {claude['model']} --effort {claude['effort']}"
            'model_reasoning_effort = "high"\n'
            "\n"
            "[features]\n"
            "hooks = true\n"
            "\n"
            "[hooks.state]\n"
            "trusted = true\n"
        )
        result = subprocess.run(
            [str(standard_profile)],
            input=current,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env={**os.environ, "HOME": str(self.temp_dir / "target-home")},
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, current)

    def test_profile_modify_scripts_preserve_repeated_runtime_tables(self) -> None:
        outputs = self.module.expected_outputs(sample_manifest())
        standard_profile = self.temp_dir / "home/dot_codex/modify_private_standard.config.toml"
        self.module.write_outputs(outputs)
        current = (
            '# Codex model profile "standard"; launch with: codex --profile standard\n'
            f"# {self.module.GENERATED_HEADER}\n"
            "\n"
            'model = "gpt-6.1-sol"\n'
            'model_reasoning_effort = "high"\n'
            "\n"
            "[features]\n"
            "hooks = true\n"
            "\n"
            "[hooks.state]\n"
            "\n"
            "[[hooks.state.sub]]\n"
            'name = "first"\n'
            "\n"
            "[[hooks.state.sub]]\n"
            'name = "second"\n'
        )
        result = subprocess.run(
            [str(standard_profile)],
            input=current,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env={**os.environ, "HOME": str(self.temp_dir / "target-home")},
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, current)

        env_path = self.temp_dir / "home/dot_agents/model-profiles.env"
        self.assertIn('MODEL_PROFILE_INTERACTIVE="standard"', outputs[env_path])
        self.assertIn('MODEL_PROFILE_STANDARD_CODEX_ARGS="--profile standard"', outputs[env_path])
        self.assertIn(
            'MODEL_PROFILE_EXPRESS_CLAUDE_ARGS="--model haiku --effort low"',
            outputs[env_path],
        )
33:#   `--ask-for-approval never` and `sandbox_workspace_write.network_access=true`,
144:codex or claude. A codex worker runs with --sandbox workspace-write,
145:--ask-for-approval never and sandbox_workspace_write.network_access=true: it
394:#   runs with --ask-for-approval never, so nothing escalates). Granted:
451:#   --sandbox workspace-write --ask-for-approval never --config
452:#   sandbox_workspace_write.network_access=true` for codex, plus the
474:    [[ ${kind} == claude ]] || args="--profile ${HERDR_AGENTS_WORKER_PROFILE} --sandbox workspace-write --ask-for-approval never --config sandbox_workspace_write.network_access=true"
1203:    printf 'herdr-agents: not in a Herdr pane, so the orchestrator pane is not started; start the worker on demand with "herdr-agents --add-worker %s [DIR]" and run the auditor headless as the agmsg-orchestration SKILL task-level audit bullet shows ("codex <audit profile args> exec --sandbox read-only -C <repo> -o <out>.last.md <prompt>"); %s.\n' \
2053:        printf 'herdr-agents: no managed Herdr workspace for %q; run herdr-agents %q (full mode) to create one, or run the audit headless as the agmsg-orchestration SKILL task-level audit bullet shows ("codex <audit profile args> exec --sandbox read-only -C <repo> -o <out>.last.md <prompt>").\n' "${workdir}" "${workdir}" >&2
2106:    printf -v audit_inner "cd -- %q && set -o pipefail && rm -f -- %q && codex%s exec --sandbox read-only -C %q -o %q %q 2>&1 | tee -- %q; printf '%s:%%s\\\\n' \"\$?\"" \

**Summarizing test findings for final report**

I’m preparing a concise final summary that clearly justifies two key findings without overstating. One is a high-priority deployment issue causing exceptions, and the other is a medium-high priority about how merge behavior affects sandbox table settings. I’m making sure to include precise file references, keep rationale brief but clear, and wrap up with the necessary closing lines from Ponytail’s notes. I’ll avoid generic points and keep the whole summary under 350 words for clarity.
**Confirming final review completeness**

I’m wrapping up by verifying all 18 expected rows from six files are accounted for without missing action items. I’m carefully checking the implications of a line lacking explicit gating but covered by a parent reference, concluding it doesn’t contradict the priority P1 finding. I’ll finalize the summary in clear English, focusing on closed issues and highlighting the last two findings with confidence.
codex
- [P1] High confidence [.orchestration/tasks/dotfiles-T133-codex-worker-network-a01.md:90](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-codex-worker-network-a01.md:90) Dispatch requires the prerequisite’s merge but not its recorded deployment readiness: the Claude worker can therefore retain Linux’s automatic `gh` sandbox exclusion and old hook bindings; require the prerequisite’s installation, effective-settings checks and session restart before dispatch, because “no unsandboxed retry” cannot prevent an automatically excluded first execution.
- [P2] High confidence [.orchestration/tasks/dotfiles-T133-codex-worker-network-a01.md:72](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-codex-worker-network-a01.md:72) The proposed test does not require merging an existing `[sandbox_workspace_write]` table: the current merger replaces managed tables wholesale, so adding the network table can silently discard `writable_roots` and restrictive `exclude_slash_tmp`/`exclude_tmpdir_env_var` settings while the scoping test passes; require preservation fixtures before marking the generated-script rows closed. [Configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference).

📝 まとめ: Reviewed all 18 threat rows, six allowed-file entries and related acceptance/review context; two findings remain for orchestrator disposition. No files changed.

Not checked: implementation or live enforcement; declared same-user and unrestricted-network residuals remain.
Verdict: incorrect
hook: Stop
hook: Stop Completed
tokens used
99,502
- [P1] High confidence [.orchestration/tasks/dotfiles-T133-codex-worker-network-a01.md:90](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-codex-worker-network-a01.md:90) Dispatch requires the prerequisite’s merge but not its recorded deployment readiness: the Claude worker can therefore retain Linux’s automatic `gh` sandbox exclusion and old hook bindings; require the prerequisite’s installation, effective-settings checks and session restart before dispatch, because “no unsandboxed retry” cannot prevent an automatically excluded first execution.
- [P2] High confidence [.orchestration/tasks/dotfiles-T133-codex-worker-network-a01.md:72](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-codex-worker-network-a01.md:72) The proposed test does not require merging an existing `[sandbox_workspace_write]` table: the current merger replaces managed tables wholesale, so adding the network table can silently discard `writable_roots` and restrictive `exclude_slash_tmp`/`exclude_tmpdir_env_var` settings while the scoping test passes; require preservation fixtures before marking the generated-script rows closed. [Configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference).

📝 まとめ: Reviewed all 18 threat rows, six allowed-file entries and related acceptance/review context; two findings remain for orchestrator disposition. No files changed.

Not checked: implementation or live enforcement; declared same-user and unrestricted-network residuals remain.
Verdict: incorrect
