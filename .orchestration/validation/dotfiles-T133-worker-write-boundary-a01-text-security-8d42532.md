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
session id: 01a1525c-6c7c-72d2-84a5-5e7f440f7d59
--------
user
Pre-dispatch security review (read-only, security profile) of the task text .orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md and its threat_table, before any implementation exists. Judge the design the text states: can the controls it names bind what actually executes on this host (mise shims first on PATH, same-user worker processes, gh outside the sandbox on Linux, symlinks and case-insensitive filesystems, inherited GIT_* environment)? Check every threat row: a closed row whose named test cannot close it, a residual row whose control does not mitigate the risk, a missing row for a file or non-path control, and any gap of the class decision-not-bound-to-execution (a decision made on text or on a validated copy while the execution resolves binaries, files or ledgers from an attacker-influenced place). Read the related acceptance records and reviews the text cites for context. Report each finding as [P0-P3] <confidence> <file:line> <one line>; findings are input for the orchestrator, who decides. End with exactly one line: Verdict: correct or Verdict: incorrect.
warning: loading hooks from both ~/.codex/hooks.json and ~/.codex/config.toml; prefer a single representation for this layer
hook: SessionStart
hook: SessionStart
hook: SessionStart Completed
hook: SessionStart Completed
hook: UserPromptSubmit
hook: UserPromptSubmit Completed
codex
🤖 I read the AGENTS.md for mryfmo/dotfiles.
指定されたタスク本文と参照先の記録を読み、判定に使った対象と実際に実行される対象が一致するかを重点的に確認します。読み取り専用でレビューします。

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
/bin/zsh -lc 'nl -ba .orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md' in ~/Workspace/dotfiles
 succeeded in 0ms:
     1	---
     2	format: 2
     3	task_id: dotfiles-T133-worker-write-boundary-a01
     4	kind: code
     5	security: true
     6	allowed_files:
     7	  - home/dot_agents/agent-config.yaml
     8	  - home/.chezmoitemplates/claude-settings-managed.json
     9	  - home/.chezmoitemplates/claude-worker-settings.json
    10	  - home/dot_claude-worker/modify_private_settings.json
    11	  - home/dot_claude/hooks/executable_orchestrator-only.sh
    12	  - .claude/settings.json
    13	  - scripts/generate-agent-configs.py
    14	  - home/dot_local/bin/common/executable_herdr-agents
    15	  - home/dot_local/bin/common/executable_herdr-agent-state.sh
    16	  - home/dot_agents/skills/agmsg-orchestration/SKILL.md
    17	  - .gitignore
    18	  - tests/unit/test_generate_agent_configs.py
    19	  - tests/unit/test_claude_settings_merge.py
    20	  - tests/unit/test_herdr_agents.py
    21	  - tests/unit/test_claude_worker_settings.py
    22	  - .orchestration/dotfiles-T133-worker-write-boundary-a01/**
    23	after: []
    24	threat_table:
    25	  - control: "home/dot_agents/agent-config.yaml (trusted checkout and interpreter bindings, distinct Claude worker policy, sandbox startup and worker cache policy)"
    26	    disposition: "residual: the rendered policy reduces accidental and injected damage; tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_policy_is_separate_from_orchestrator_policy checks both platforms without claiming same-UID isolation."
    27	  - control: "home/.chezmoitemplates/claude-settings-managed.json (orchestrator settings with failIfUnavailable true and onFailure block)"
    28	    disposition: "residual: the shared baseline retains orchestrator behavior and reduces silent startup and hook failures; tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_orchestrator_settings_keep_existing_policy checks the merged settings."
    29	  - control: "home/.chezmoitemplates/claude-worker-settings.json (worker Edit denies, empty exclusions, restricted socket and write allowances, and minimal delivery hooks)"
    30	    disposition: "residual: dedicated settings reduce worker access to trusted paths and host execution routes; tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_policy_renders_for_both_platforms checks the complete rendered policy."
    31	  - control: "home/dot_claude-worker/modify_private_settings.json (deployment of the dedicated worker baseline without importing orchestrator policy)"
    32	    disposition: "residual: authoritative managed policy reduces stale or permissive worker configuration; tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_settings_replace_stale_policy_idempotently checks repeated rendering and merging in temporary homes."
    33	  - control: "home/dot_claude/hooks/executable_orchestrator-only.sh (anchored launch-root guard for tracked project hooks)"
    34	    disposition: "residual: the guard reduces execution of worker-influenced project code; tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_project_guard_uses_launch_root_and_never_runs_worker_payloads checks fixed arguments, canonical identity and child status."
    35	  - control: ".claude/settings.json (every tracked project command routed through the installed guard with absolute interpreters and onFailure block)"
    36	    disposition: "residual: guarded commands reduce worker-triggered project-hook execution; tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_every_tracked_project_hook_is_guarded_and_blocks_on_failure exhaustively traverses the hook entries."
    37	  - control: "scripts/generate-agent-configs.py (separate settings generation, sanitized tracked-path enumeration and absolute executable bindings)"
    38	    disposition: "residual: trusted rendering reduces configuration mistakes and injected executable selection; tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_deny_inventory_uses_sanitized_anchored_git checks the command, inventory and render inputs."
    39	  - control: "home/dot_local/bin/common/executable_herdr-agents (worker pane environment, dedicated configuration directory, private caches and trusted delivery setup)"
    40	    disposition: "residual: launch preparation reduces inheritance of orchestrator capabilities and stale hooks; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_every_worker_launch_receives_dedicated_policy_and_private_caches captures managed and standalone launches and repeated starts."
    41	  - control: "home/dot_local/bin/common/executable_herdr-agent-state.sh (repository-owned Herdr state helper with an explicitly supplied absolute Python interpreter)"
    42	    disposition: "residual: binding the helper and its Python child reduces shim execution; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_hook_descendants_do_not_execute_path_interpreters checks executed identities with planted shims."
    43	  - control: "home/dot_agents/skills/agmsg-orchestration/SKILL.md (the governing Worker Playbook step 4 sentence)"
    44	    disposition: "residual: the sentence removes procedural authorization for worker sandbox escapes; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_playbook_requires_every_command_inside_sandbox checks its replacement."
    45	  - control: ".gitignore (the .uv-cache directory pattern)"
    46	    disposition: "residual: ignoring the private cache reduces accidental cache publication; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_uv_cache_directory_is_gitignored checks the pattern in a temporary checkout."
    47	  - control: "tests/unit/test_generate_agent_configs.py (separate platform policies, inventory generation, interpreter bindings and tracked hook coverage)"
    48	    disposition: "residual: render fixtures verify configuration and command construction; they do not establish live enforcement or authenticate host-local inputs."
    49	  - control: "tests/unit/test_claude_settings_merge.py (orchestrator baseline preservation and failure-policy rendering through the existing merge)"
    50	    disposition: "residual: temporary HOME fixtures verify managed entries and identify runtime-added hooks separately; they do not apply live settings."
    51	  - control: "tests/unit/test_herdr_agents.py (every launch route, repeated starts, hook descendants, caches and retained native denials)"
    52	    disposition: "residual: fake launchers and subprocess markers verify effective arguments and executed fixture identities without starting live seats."
    53	  - control: "tests/unit/test_claude_worker_settings.py (dedicated settings deployment, deny inventory, project guard, socket restrictions and hook failure configuration)"
    54	    disposition: "residual: fixtures verify the configured controls and guard behavior; runtime permission checks and their remaining path-consumption window remain documented host residuals."
    55	  - control: ".orchestration/dotfiles-T133-worker-write-boundary-a01/** (this task's branch artifacts)"
    56	    disposition: "residual: artifacts distinguish documentation facts, historical probes, final-head fixture results and unperformed operator deployment; acceptance compares their claims with the diff and CI."
    57	  - control: "the task-file copy at .orchestration/dotfiles-T133-worker-write-boundary-a01/task.md"
    58	    disposition: "residual: the first push includes the byte-identical dispatched task; TASK and RESULT carry its SHA256, which the orchestrator verifies at acceptance."
    59	  - control: "the evidence records under .orchestration/dotfiles-T133-worker-write-boundary-a01/"
    60	    disposition: "residual: report.md, validation.md, sandbox.md, learning.md, autoskill.md and worker review evidence retain commands, outputs, statuses and tested revisions without credentials or unmasked home-directory paths."
    61	  - control: "task metadata (PR_FEEDBACK_EVIDENCE, AUDIT_EVIDENCE, ACCEPTANCE_EVIDENCE and REVIEW_EVIDENCE)"
    62	    disposition: "residual: the orchestrator checks C1 to C10 and C7b, verifies dispatched bytes and binds integration evidence to the final head; evidence of record is retrieved from GitHub at its SHA under the regime rule implemented by P1-14 a05 and P1-6."
    63	  - control: metadata separators
    64	    disposition: "residual: the first document separators delimit format-2 metadata; the task-copy SHA256 binds the complete document."
    65	  - control: in-process effects
    66	    disposition: "residual: generation and tests use repository files and temporary fixtures; the worker performs no live deployment, login, permission-policy mutation or operator-session restart."
    67	  - control: workflow and interpreter or environment inputs
    68	    disposition: "residual: absolute interpreters, Python -I, sanitized Git and trusted executable bindings reduce environment injection; the host, native loader and same-UID processes remain outside this task's security guarantee."
    69	  - control: new or renamed scripts
    70	    disposition: "residual: the worker settings modify script, orchestrator-only guard and repository-owned Herdr state helper have named source and installed paths; RESULT inventories their interpreter and descendant bindings without introducing a worker-write-boundary hook or gh wrapper."
    71	  - control: "5.14 item 0: threat model"
    72	    disposition: "residual: host controls reduce accidental and injected damage and do not close a boundary between seats sharing one OS user; GitHub is the hard boundary, and approvals and gate evidence of record come from its API at a SHA inside the sandbox."
    73	  - control: "5.14 item 1: worker write controls"
    74	    disposition: "residual: dedicated configuration, symlink-aware Edit denies, restricted sandbox capabilities and failIfUnavailable true reduce damage; documented requested-path and resolved-target checks address static symlink redirection without claiming atomic immunity to a concurrent path swap."
    75	  - control: "5.14 item 2: sanitized environment and private executable PATH"
    76	    disposition: "residual: sanitized anchored Git enumeration and absolute hook interpreter bindings reduce injected configuration and shim execution; the remaining consuming-helper contracts belong to P1-14 a05, P1-10 a02, audit-pool-a02 and P1-6."
    77	  - control: "5.14 item 3: trusted-path checks"
    78	    disposition: "residual: canonical anchor and interpreter checks reduce worker-selected trusted paths and account for symlink components and filesystem case aliases; other consuming-helper checks remain with their owning hardening tasks."
    79	  - control: "5.14 item 4: verified executable and consumed-byte identity"
    80	    disposition: "residual: hooks execute their selected absolute interpreter and trusted script without rediscovery; evidence snapshots, last-use digest checks and their race limitations remain with the consuming orchestrator-side tasks."
    81	  - control: "5.14 item 5: output and reservation identity"
    82	    disposition: "residual: this task adds no reservation protocol; full-head output names, fixed-inode locks and physical-slot identity remain with the orchestrator-side tasks that create them."
    83	  - control: "5.14 item 6: honest residuals, hooks and MCP"
    84	    disposition: "residual: guarded project hooks, minimal worker delivery hooks and removal of the worker Herdr socket allowance reduce host execution routes; approved external processes and same-UID processes outside every seat sandbox remain residual."
    85	  - control: "5.14 item 7: trusted-execution verification"
    86	    disposition: "residual: this task records red-then-green render, merge, guard, launch, descendant and cache tests; P1-6 owns tests/unit/trusted_exec_contract.py and the consuming-helper contract tests."
    87	  - control: "5.14 item 8: committed approval ledger"
    88	    disposition: "residual: the regime reads the ledger through the GitHub contents API at the SHA returned by git ls-remote origin refs/heads/main; P1-14 a05 implements that read, and local refs, files and object traversal provide no approval authority."
    89	  - control: "5.14 item 9: private uv caches"
    90	    disposition: "residual: per-seat worker caches and restricted worker write allowances reduce cache poisoning; consuming hardening tasks use the protected orchestrator cache with --offline and execute no worker, shared uv or mise cache content."
    91	  - control: "5.14 item 10: no worker command outside the sandbox"
    92	    disposition: "residual: empty worker exclusions, disabled unsandboxed requests, absent Herdr socket allowance and Codex in-sandbox network reduce escape routes; the deterministic Codex permgate rule and live deployment remain operator steps."
    93	  - control: "hook failure policy"
    94	    disposition: "residual: every generated and tracked hook entry carries onFailure block, reducing fail-open behavior where Claude supports it; configuration tests cover missing-command and timeout policy, while background hooks and events on which the field has no effect carry no enforcement responsibility."
    95	  - control: orchestrator effect merge
    96	    disposition: "residual: the worker never merges; the orchestrator follows the final-head integration gate, required permission approval and pinned squash-merge procedure, with evidence of record retrieved from GitHub."
    97	  - control: orchestrator effect update-branch
    98	    disposition: "residual: the orchestrator owns branch updates and obtains fresh required CI, feedback, audit and security evidence for the resulting head."
    99	  - control: orchestrator effect forced worker removal
   100	    disposition: "residual: no forced removal is planned; existing dirty-worktree protections remain, and acceptance identifies any operator-authorized discarded state."
   101	premises:
   102	  - claim: >-
   103	      The historical a05 premises carried by the preceding text describe its recorded observations. They do not require this worker to rebuild PR 400, edit the approval ledger or implement P1-14 a05.
   104	    sources:
   105	      - .orchestration/tasks/dotfiles-T133-permission-guard-gate-a05.md
   106	      - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md
   107	  - claim: >-
   108	      D-024-21 establishes the current threat model and dedicated Claude worker configuration. The earlier cwd-hook, launch-root-hook and local Git ledger proposals remain historical records.
   109	    sources:
   110	      - .orchestration/decisions.tsv
   111	      - .orchestration/plans/024-design-quality.md
   112	      - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md
   113	  - claim: >-
   114	      The existing Claude settings modify script merges the managed baseline into current settings and appends an attachment hook. The dedicated worker renderer must not import that orchestrator settings merge or its attachment behavior.
   115	    sources:
   116	      - home/dot_claude/modify_private_settings.json
   117	      - home/.chezmoitemplates/claude-settings-managed.json
   118	    verification: tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_settings_do_not_import_orchestrator_hooks
   119	  - claim: >-
   120	      The current launcher constructs worker profile options separately from the pane environment. The dedicated configuration directory and private cache variables must reach the actual Claude process on every worker launch route.
   121	    sources:
   122	      - home/dot_local/bin/common/executable_herdr-agents
   123	      - home/dot_agents/agent-config.yaml
   124	    verification: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_every_worker_launch_receives_dedicated_policy_and_private_caches
   125	---
   126	
   127	# AGMSG-TASK dotfiles-T133-worker-write-boundary-a01 — plan 024 P1-15 under D-024-17, D-024-19, D-024-20 and D-024-21
   128	
   129	## Goal
   130	
   131	The host is not a security boundary between seats sharing one OS user. The regime's hard boundary is GitHub: protected main, required checks and merge through the orchestrator's identity. Approvals and gate evidence of record are read from GitHub at a SHA through its API inside the sandbox. Host-local controls in this task reduce accidental and injected damage. They do not establish isolation from a malicious same-UID process.
   132	
   133	This task implements section 5.14 items 1, 9 and 10 through a dedicated Claude worker configuration directory, Edit deny rules on trusted paths, guarded tracked project hooks, absolute hook interpreter bindings, private worker caches and sandboxed worker commands. Every Claude seat has `sandbox.failIfUnavailable: true`. Codex workers have `sandbox_workspace_write.network_access=true`.
   134	
   135	[memory:decision] D-024-20 makes this task the dispatch prerequisite of P1-14 a05, P1-10 a02, audit-pool-a02 and P1-6. The orchestrator places this task in their `after:` fields before dispatch. This task has `after: []`. A Codex seat performs these Claude configuration edits under the routing rule, including the Worker Playbook step 4 sentence permitted by plan 021 step 8.3.
   136	
   137	The design source is `.orchestration/plans/024-design-quality.md` section 5.14 items 0 through 10. D-024-21 and the amended items 0, 1 and 8 govern this revision. The acceptance record preserves the documentation facts and earlier proposals as history.
   138	
   139	The third C-80 text review is `.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-ecc7ab5.md.last.md`. Its five P1 findings remain recorded. This revision replaces the custom file-tool boundary hook with documented symlink-aware deny rules, moves approval reads out of the local object database, binds hook descendants to absolute interpreters, removes the worker Herdr socket allowance and specifies runtime-level hook failure policy.
   140	
   141	The file-tool rule is the documented sentence, “Deny rules: apply when either the requested path or the file it resolves to matches.” Edit and Write refuse a requested file that is itself a symlink. Directory symlinks are subject to resolved-target permission checks, and the tools check the resolved location again when opening the approved file. These documented checks address the preceding text's validation-only design. They do not establish an atomic host security boundary against concurrent same-UID changes. [Claude permission reference](https://code.claude.com/docs/en/permissions#symlinks)
   142	
   143	The 2026-10-19T03:45:06Z sandbox probe ran `gh api repos/mryfmo/dotfiles --jq .name` and returned `dotfiles`. The recorded sandbox proxy used CONNECT without TLS interception, and gh read the Keychain token. This is a historical host observation. It does not establish enforcement or credential readiness for the new worker directory on either platform.
   144	
   145	The documentation facts recorded at 03:2xZ establish that Edit denies also affect the Bash sandbox, hooks reload during a session and an unavailable sandbox is fail-open by default. D-024-21's 04:0xZ decision establishes the dedicated configuration mechanism, directory-specific credentials, symlink coverage and `onFailure: "block"` support. The earlier shared-user-hook proposal is superseded.
   146	
   147	## Files
   148	
   149	1. `home/dot_agents/agent-config.yaml` remains the source of agent policy and model profiles.
   150	
   151	   The manifest names `orchestrator_checkout` as the anchored primary checkout and supplies trusted deployment bindings for the guard, hook scripts and absolute interpreters. These bindings resolve outside worker worktrees and executable caches. Worker cwd, tool input, worktree configuration and inherited command variables do not select them.
   152	
   153	   The manifest defines a separate Claude worker settings output at `home/.chezmoitemplates/claude-worker-settings.json`. The worker configuration directory is `~/.claude-worker`. The launcher passes its expanded absolute path as `CLAUDE_CONFIG_DIR`.
   154	
   155	   The orchestrator policy retains its existing permissions, exclusions, socket access, cache allowances and hook functions. Its required policy changes are `failIfUnavailable: true` and `onFailure: "block"` on its hooks. The interpreter bindings required below preserve those hook functions.
   156	
   157	   The worker policy contains no excluded commands and sets `allowUnsandboxedCommands: false`. It contains no Herdr socket allowance and no allow-all Unix socket switch. Its sandbox is enabled and has `failIfUnavailable: true`.
   158	
   159	   Worker `sandbox.filesystem.allowWrite` contains only the existing agmsg store paths and per-seat cache paths. The worktree is the project root and supplies its ordinary project write root. Shared uv and mise write allowances are not copied into worker settings.
   160	
   161	   The Codex worker profile sets `sandbox_workspace_write.network_access=true`. Existing model selections and Codex shared Git grants retain their meaning. The deterministic Codex permgate rule that stops approving sandbox escapes is an operator step.
   162	
   163	2. `scripts/generate-agent-configs.py` renders the distinct orchestrator and worker baselines from the manifest.
   164	
   165	   The trusted-path deny inventory is generated at render time from the anchored checkout's tracked tree using `git ls-tree`. The inventory covers every top-level tracked path outside `.claude/worktrees/`. The `.claude` entry is expanded sufficiently to protect its tracked contents without emitting a parent deny that also denies worker worktrees. Directory and file entries receive patterns appropriate to their complete protected extent.
   166	
   167	   Anchored checkout rules use absolute `//` permission patterns. Rendering includes the trusted paths themselves and their descendants. It emits no checkout-wide parent deny that defeats the `.claude/worktrees/` exclusion.
   168	
   169	   Worker Edit denies also cover `~/.agents/**`, `~/.claude/**`, `~/.claude-worker/**`, `~/.local/**`, `~/.config/**`, `~/.cache/uv/**` and `~/.local/share/uv/**`. The rules protect the corresponding directory targets as well as their contents.
   170	
   171	   Edit denies cover Write, MultiEdit and NotebookEdit through Claude's permission system. Requested-path and resolved-target matching supply the documented symlink coverage. The generator does not create `executable_worker-write-boundary.py` or a replacement PreToolUse path validator.
   172	
   173	   Every direct Git verification introduced or changed by this task follows section 5.14 item 2. It begins with `env -i`, uses the selected absolute Git executable and an explicit `-C`, sets `GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL=/dev/null`, and supplies `-c core.hooksPath=/dev/null -c core.fsmonitor=false -c protocol.allow=never -c protocol.https.allow=always`. Diff and show also use `--no-ext-diff --no-textconv` and `-c core.attributesFile=/dev/null -c core.sshCommand=false`.
   174	
   175	   The private executable-link directory contains only links to selected absolute trusted binaries. Rendering rejects missing bindings, worker-controlled executable paths, shims, empty PATH entries and relative PATH entries. Python invocations use `-I`.
   176	
   177	   `tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_deny_inventory_uses_sanitized_anchored_git` records the exact Git environment and arguments. Its fixtures cover a newly tracked top-level path, tracked files, tracked directories, `.claude` children, the worktree exclusion and an anchor containing spaces.
   178	
   179	3. `home/.chezmoitemplates/claude-settings-managed.json` remains the orchestrator baseline.
   180	
   181	   The existing `home/dot_claude/modify_private_settings.json` continues to render the orchestrator's `~/.claude/settings.json`. That modify script is not imported into the dedicated worker renderer and remains outside `allowed_files`.
   182	
   183	   The orchestrator retains its current policy content apart from `failIfUnavailable: true`, `onFailure: "block"` and the required absolute interpreter bindings. Worker-specific Edit denies, empty exclusions and restricted socket policy do not enter this shared baseline.
   184	
   185	   Every managed hook entry carries `onFailure: "block"`. Merge evidence identifies hooks appended by the existing modify script and distinguishes them from generated baseline entries. The report accounts for the effective deployed hook set and does not equate baseline coverage with coverage of runtime-added entries.
   186	
   187	   `tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_orchestrator_settings_keep_existing_policy` compares the merged policy with the preceding baseline. Repeated merging remains idempotent and preserves unrelated settings.
   188	
   189	4. `home/.chezmoitemplates/claude-worker-settings.json` is the dedicated worker baseline.
   190	
   191	   It renders the trusted-path Edit denies, empty `excludedCommands`, `allowUnsandboxedCommands: false`, restricted `allowWrite`, absent Herdr socket allowance and `failIfUnavailable: true` for both Darwin and Linux.
   192	
   193	   Its hooks are limited to agmsg delivery. It contains no formatter, project-map, permgate, orchestrator attachment, Herdr state or worker-write-boundary hook. Project hooks still load from the tracked `.claude/settings.json` and receive the guard described below.
   194	
   195	   Every worker hook entry carries `onFailure: "block"`. Command hooks invoke the installed agmsg scripts through the selected absolute shell interpreter. Their script paths are absolute paths beneath the trusted installed agmsg root.
   196	
   197	   The worker baseline does not copy the orchestrator's plugins, credential files or current hook arrays. Hook settings reload during a session, so protection is stated as current configuration rather than startup capture. `CLAUDE_CONFIG_DIR` selects the separate user settings directory while project settings continue to apply. [Claude settings reference](https://code.claude.com/docs/en/settings)
   198	
   199	5. `home/dot_claude-worker/modify_private_settings.json` renders `~/.claude-worker/settings.json` from the dedicated baseline.
   200	
   201	   The script follows the existing chezmoi modify-script interface: current content arrives on stdin and the desired settings object is written to stdout. It uses Python's standard library and the same trusted source and home resolution conventions as the existing renderer.
   202	
   203	   Managed worker permissions, sandbox policy and hooks replace stale managed values. Permissive old exclusions, socket allowances, hook commands and shared cache allowances do not survive as additive worker policy. The script does not read or copy `~/.claude/settings.json`.
   204	
   205	   Rendering handles empty and malformed input through the repository's existing baseline behavior and is idempotent. It neither reads credentials nor initiates authentication.
   206	
   207	   `tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_settings_replace_stale_policy_idempotently` exercises repeated deployment in temporary homes. `tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_settings_do_not_import_orchestrator_hooks` plants orchestrator hook and plugin markers and verifies their absence.
   208	
   209	6. `home/dot_claude/hooks/executable_orchestrator-only.sh` is installed as `~/.claude/hooks/orchestrator-only.sh`.
   210	
   211	   The guard runs under the selected absolute shell interpreter and compares canonical `CLAUDE_PROJECT_DIR` with the anchored checkout. Equality executes the supplied fixed command. Every other launch root exits 0 without executing it.
   212	
   213	   Worker launch roots, sibling worktrees and unrelated checkouts execute no guarded project code. Missing or unresolvable launch-root identity also executes no supplied command. Event cwd does not change the launch-root decision.
   214	
   215	   The guard preserves argument boundaries, stdin and child exit status. It performs no eval, PATH interpreter lookup or worktree-relative script selection.
   216	
   217	   `tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_project_guard_uses_launch_root_and_never_runs_worker_payloads` plants worker Stop, contextdb and formatter payloads. Worker and unrelated-root invocations leave all markers absent. The anchored invocation reaches the selected fixture interpreter and preserves its arguments and status.
   218	
   219	7. `.claude/settings.json` retains its tracked project hooks and rewrites every command through the installed orchestrator-only guard.
   220	
   221	   The guard invocation uses its absolute installed path and absolute shell interpreter. The guarded child command uses an absolute interpreter and an anchored script path. Contextdb commands do not invoke bare `python3` or select `.claude/hooks` from a worker checkout. The Stop gate does not invoke bare `bash` or a worker checkout's `scripts/agent-stop-gate.sh`.
   222	
   223	   Every hook entry carries `onFailure: "block"`. Existing event functions remain available to the anchored orchestrator. They are no-ops in worker sessions because the guard rejects their launch roots.
   224	
   225	   `tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_every_tracked_project_hook_is_guarded_and_blocks_on_failure` traverses every event, matcher and command entry. It rejects unguarded commands, missing failure policy, relative interpreters and worker-selected executable paths.
   226	
   227	8. `home/dot_local/bin/common/executable_herdr-agents` supplies the dedicated worker configuration at the actual worker launch boundary.
   228	
   229	   Every Claude worker pane starts with `CLAUDE_CONFIG_DIR=<absolute-home>/.claude-worker`. The value reaches the Claude process through the pane command and environment construction. Setting it only in the parent spawn process does not satisfy this requirement.
   230	
   231	   Managed-workspace and standalone-worker routes receive the same binding. Repeated starts do not inherit a caller's conflicting configuration directory.
   232	
   233	   Every worker launch exports `UV_CACHE_DIR=<absolute-worktree>/.uv-cache` and `UV_PYTHON_INSTALL_DIR=<absolute-worktree>/.uv-cache/python`. Both worker kinds receive values derived from the selected canonical worktree. Caller-provided values do not replace them.
   234	
   235	   Before every Claude worker start, the launcher regenerates managed local delivery entries from trusted inputs. An existing delivery match does not skip preparation. Stale managed commands are replaced, and unknown command hooks are not promoted into the trusted delivery set.
   236	
   237	   Local settings retain existing native merge denials. They do not reintroduce excluded commands, the Herdr socket, unsandboxed requests or orchestrator hooks. The effective delivery set contains no duplicate managed invocation.
   238	
   239	   Codex launches retain `--sandbox workspace-write`, `--ask-for-approval never` and `sandbox_workspace_write.network_access=true`. Tests inspect effective launch arguments rather than inferring them from the base manifest.
   240	
   241	   The retained Codex Git grant permits shared `.git/objects`, `.git/refs`, `.git/logs` and the worker's administration directory. It does not authenticate local ledger content and is not represented as a host security boundary.
   242	
   243	   `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_every_worker_launch_receives_dedicated_policy_and_private_caches` covers both worker kinds and all launch routes. `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_repeated_worker_start_replaces_stale_managed_hooks` covers repeated preparation. `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_commands_have_no_unsandboxed_launch_route` checks effective exclusions, socket policy, sandbox requests and retained merge denials.
   244	
   245	9. `home/dot_local/bin/common/executable_herdr-agent-state.sh` provides the repository-owned Herdr state helper installed as `~/.local/bin/common/herdr-agent-state.sh`.
   246	
   247	   The currently installed `~/.claude/hooks/herdr-agent-state.sh` is generated by Herdr and is not a tracked source in this repository. Its bare `python3` descendant is not retained as a trusted worker hook. The repository-owned helper preserves the required state-reporting function and receives its absolute Python interpreter through the rendered invocation.
   248	
   249	   Every hook command and every interpreted descendant it runs uses a selected absolute interpreter. Repository-owned shell descendants use absolute shebangs or explicit absolute shell invocations. Python descendants use the selected absolute interpreter with `-I`. No trusted hook route reaches bare `python3` or an `/usr/bin/env bash` shebang through PATH.
   250	
   251	   The delivery inventory names `~/.agents/skills/agmsg/scripts/session-start.sh`, `~/.agents/skills/agmsg/scripts/check-inbox.sh` and every additional delivery descendant actually reached. Scripts outside this repository are invoked with the absolute interpreter in the hook command itself. Their installed files are not edited or vendored.
   252	
   253	   The inventory records source ownership, installed path, caller and interpreter for each reached script. Binding only the first command does not establish descendant coverage.
   254	
   255	   `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_hook_descendants_do_not_execute_path_interpreters` executes the fixture hook routes with planted Python and Bash shims. It checks descendant markers and actual selected interpreter identities. Capturing launcher command strings alone does not satisfy this test.
   256	
   257	10. `home/dot_agents/skills/agmsg-orchestration/SKILL.md` changes only the Worker Playbook step 4 sentence that lists outside-sandbox worker commands.
   258	
   259	    The replacement sentence is: “Every worker command, including gh, git push and authenticated git fetch, runs inside the worker's sandbox; no worker command runs outside it.”
   260	
   261	    This sentence governs worker execution. Historical TLS, keyring, artifact-writing and delivery exceptions elsewhere in the playbook provide no authorization to leave the sandbox. An unavailable operation produces a blocked PONG with its exact command and boundary.
   262	
   263	    `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_playbook_requires_every_command_inside_sandbox` checks the replacement and removal of the former three-command exception sentence.
   264	
   265	11. `.gitignore` adds only `.uv-cache/`.
   266	
   267	    Section 5.14 item 9 fixes trusted orchestrator consumers to `UV_CACHE_DIR=<anchored-checkout>/.agents/worklog/uv-cache`, places managed Python installations beneath that cache and uses `--offline`. Those consumers execute no dependency content from worker caches, shared uv caches or mise caches. Their owning hardening tasks implement the consumer changes.
   268	
   269	    This task's hooks use standard-library Python and absolute shell interpreters without uv. The existing `.agents/worklog/` ignore covers the orchestrator cache.
   270	
   271	12. The four allowed test modules reuse existing render, merge, fake-launcher and temporary-HOME fixtures.
   272	
   273	    Tests are written before implementation and retain identified base-failure and implementation-success evidence. A missing new entrypoint supplies its baseline failure.
   274	
   275	    Worker settings tests cover both platforms, every protected path category, directory targets, descendants, the worktree exclusion, stale settings, exact socket and exclusion policy, and the absence of the removed boundary hook.
   276	
   277	    Path fixtures cover symlink components and filesystem case aliases. They verify inventory and configuration identities without presenting a simulated permission matcher as proof of Claude runtime enforcement.
   278	
   279	    Hook tests cover every generated and tracked entry's failure policy. They distinguish synchronous policy hooks from background delivery and post-action events. `onFailure: "block"` requires Claude Code v2.1.295 or later and has no enforcement effect on background hooks or the documented excluded events. [Claude hook failure reference](https://code.claude.com/docs/en/hooks#block-the-action-when-a-hook-fails)
   280	
   281	13. `.orchestration/dotfiles-T133-worker-write-boundary-a01/` contains the byte-identical dispatched `task.md`, `report.md`, `validation.md`, `sandbox.md`, `learning.md`, `autoskill.md` and worker review evidence.
   282	
   283	    The report maps each of the third C-80 review's five findings to the revised mechanism, its tests and its remaining residual. It distinguishes policy configuration from live enforcement and deployment.
   284	
   285	## Out of scope
   286	
   287	The worker-write-boundary Python hook, its hook entries and `tests/unit/test_worker_write_boundary.py` are dropped. The gh-trusted wrapper and its configuration directory remain dropped. This task introduces no outside-sandbox gh execution route.
   288	
   289	The permission guard and merge gate remain P1-14 a05's work. P1-14 a05 and P1-6 implement the regime rule that approvals and gate evidence of record come from GitHub at a SHA through its API inside the sandbox.
   290	
   291	For the committed approval ledger, the regime obtains the commit SHA returned by `git ls-remote origin refs/heads/main` and reads `gh api repos/<owner>/<repo>/contents/.orchestration/decisions.tsv?ref=<sha>` inside the sandbox. The consuming implementation reads the API response's file content at that exact SHA. It does not fall back to local files, local refs or local object traversal.
   292	
   293	A working-copy decision remains a proposal until its record PR reaches main. This task writes no approval row and implements no local-object substitute for GitHub authority.
   294	
   295	Permgate code and deterministic policy remain the operator's responsibility. The worker prepares the operator step that stops the Codex permgate policy from approving sandbox escapes. The worker performs no live policy edit or escape probe.
   296	
   297	The operator logs in once with the worker configuration directory selected. The Keychain entry is keyed to that directory. Credentials are not copied from the orchestrator directory, committed, printed or included in fixtures.
   298	
   299	The documented file-tool checks reduce symlink redirection risk. A same-UID process can race filesystem changes, alter host-local state or execute outside a seat sandbox. The remaining interval between permission checks and path consumption is a residual under section 5.14 item 0. This text makes no claim that the worker could already write every redirected target directly.
   300	
   301	The absence of a worker Herdr socket allowance reduces the documented host-execution route through socket RPC. Hooks, approved MCP processes and other processes outside every seat sandbox retain their stated host trust. The configuration is not represented as same-UID adversarial isolation.
   302	
   303	`onFailure: "block"` supplies runtime failure behavior where Claude supports it. Python exit-status tests do not establish timeout handling by the runtime. Background hooks and events on which the field has no effect perform no security enforcement in this design.
   304	
   305	Consuming-helper snapshots, reservation locks, the common trusted-execution test helper and orchestrator review-worktree relocation remain with their owning hardening tasks. Codex writable-root grants remain unchanged.
   306	
   307	The worker edits neither `.orchestration/decisions.tsv` nor other tasks' canonical texts, evidence or acceptance records. It performs no authentication change, keyring mutation, ruleset mutation, live settings application, global installation, operator restart or merge.
   308	
   309	## Check
   310	
   311	`make render-check`, `make validate-agent-assets` and `make format` pass.
   312	
   313	Shellcheck and shfmt cover the changed shell sources, including the launcher, orchestrator-only guard and repository-owned Herdr state helper. Added or changed shell comments use English shdoc-compatible annotations. Changed Python receives the repository's Python formatting and lint checks.
   314	
   315	`uv run python -m unittest tests.unit.test_generate_agent_configs tests.unit.test_claude_settings_merge tests.unit.test_herdr_agents tests.unit.test_claude_worker_settings -v` is green. The validation record contains every named red-then-green selector and the complete final module run.
   316	
   317	The final diff has at most 650 changed lines outside `tests/` and `.orchestration/`, excluding the regenerated `home/.chezmoitemplates/claude-settings-managed.json` and `home/.chezmoitemplates/claude-worker-settings.json`. It has at most 750 changed lines under `tests/`. Changed lines are additions plus deletions. The validation record includes per-file numstat, base and head identities and both totals.
   318	
   319	The validation record contains exact commands, verbatim outputs, exit statuses and tested identities. Git commands producing that evidence follow section 5.14 item 2.
   320	
   321	Both platform renders show separate worker and orchestrator settings, the complete trusted-path inventory, the `.claude/worktrees/` exclusion, empty worker exclusions, absent worker Herdr socket allowance, restricted worker writes and `failIfUnavailable: true` for every Claude seat.
   322	
   323	Hook evidence inventories every generated and tracked entry, its `onFailure` value, installed script, absolute interpreter and reached descendants. Merged-settings evidence identifies runtime-added entries separately. No report claims complete effective failure-policy coverage from template inspection alone.
   324	
   325	Launch evidence shows the actual Claude process receiving the dedicated configuration directory and both cache variables on every route. Repeated-start evidence shows replacement of stale managed hooks, retained native merge denials and explicit Codex sandbox and network arguments.
   326	
   327	Guard markers show that worker project scripts, contextdb hooks, Stop gates and formatter payloads do not execute through tracked hooks. Descendant markers show that planted PATH interpreters do not execute on the tested hook routes.
   328	
   329	The report states the GitHub API ledger rule without claiming this task implements the permission guard. It records the same-UID and path-consumption residuals, external-process trust, hook-event failure limitations and retained Codex shared Git grant.
   330	
   331	No local Bats tests run. Required Bats results come from GitHub Actions. Failed required checks retain their actual output and receive an in-scope fix before RESULT.
   332	
   333	The orchestrator runs `uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py .orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md` before dispatch and at acceptance. C1 to C10 and C7b pass.
   334	
   335	A C-80 security-profile context reviews this complete revised text before dispatch. That review is a dispatch prerequisite and is not claimed as a result of this draft.
   336	
   337	## Completion
   338	
   339	One implementation PR starts from a fresh branch off `origin/main`. The first push includes the byte-identical dispatched task at `.orchestration/dotfiles-T133-worker-write-boundary-a01/task.md`.
   340	
   341	The Completion clauses of `.orchestration/tasks/dotfiles-T133-permission-guard-gate-a05.md` apply with this task's branch, files and evidence paths, `dotfiles-T133-worker-write-boundary-followup-a01` as the owner of any advisory P2, and `task_copy=<sha256 of .orchestration/dotfiles-T133-worker-write-boundary-a01/task.md>` in RESULT. The a05-specific continuation of PR #420, predecessor-copy deletion, inherited counters, deadline and implementation requirements do not transfer. The orchestrator writes the follow-up owner task before assigning its first advisory P2.
   342	
   343	Every worker-side fix round counts toward INV-6. The worker's own pre-push review is one round at most. A surviving P0/P1 is sent in RESULT as open and stops integration. The worker starts no additional private correction-and-review cycle to avoid reporting it.
   344	
   345	No `@codex review` comment is posted. Automatic final-head reviews are observed within the bounded 15-minute window, and absence is recorded as `bot: none`. Required GitHub Actions checks pass before RESULT. Every feedback item carries its proposed disposition, and surviving P0/P1 findings remain open for the operator's decision.
   346	
   347	Every gh write and every git write runs as a separate command without shell chaining. Every worker command remains inside its sandbox. An operation that cannot complete there produces a blocked PONG with the exact command and boundary.
   348	
   349	The Codex worker writes evidence at the required relative paths in its own worktree and says so in RESULT. Worker review evidence uses the `-worker-` infix. Crit-data evidence and its receipt follow repository rules without a browser review or human review request. The orchestrator copies evidence by absolute path before acceptance.
   350	
   351	`AGMSG-RESULT v1` names the final head, base, branch, changed files, new deployable scripts, source and installed paths, trusted anchor, interpreter and descendant inventory, Bot findings and proposed dispositions, open P0/P1 findings, exact test selectors, measured caps, task-copy SHA256 and evidence paths. It distinguishes historical observations from final-head results.
   352	
   353	The report states the user-visible effects. Claude workers use `~/.claude-worker` and require its own login. Worker trusted-path Edit denies also affect Bash sandbox writes. Workers have no excluded commands or Herdr socket allowance. Tracked project hooks are no-ops in worker sessions. Worker caches are private. Every Claude seat fails when its sandbox is unavailable. Codex workers have in-sandbox network access. The orchestrator retains its existing policy apart from the specified startup, hook failure and interpreter-binding changes.
   354	
   355	This task is `security: true`. The orchestrator obtains the task-level audit and a separate security-profile review of the final implementation head. The finding-class record includes `decision-not-bound-to-execution`, `unbound-evidence` and `fail-open-on-error`. A third non-advisory finding of one class stops the artifact for redesign under the inherited completion rules.
   356	
   357	Final-head feedback collection, task-level audit, finding dispositions, acceptance and the integration gate follow Orchestrator Playbook step 10 in its prescribed order. The gate receives `PR_FEEDBACK_EVIDENCE`, `AUDIT_EVIDENCE`, `ACCEPTANCE_EVIDENCE` and the agent review receipt. Changed heads receive fresh required evidence. The final-head security review precedes the gate.
   358	
   359	The permission-surface change receives the required operator-backed approval through the repository's existing process. The worker writes no approval row and treats no candidate-tree decision as authority.
   360	
   361	Live deployment is the operator's post-merge `make update`. The operator performs the worker-directory login with `CLAUDE_CONFIG_DIR=<absolute-home>/.claude-worker` selected. The operator applies the prepared deterministic Codex permgate rule that stops approving sandbox escapes and restarts affected sessions.
   362	
   363	The deployment record checks the effective settings after `make update`, including hooks added by merge scripts or integration installers. It verifies the worker directory, both platform policy outputs, hook interpreter descendants, failure-policy coverage, sandbox startup and credential readiness without exposing credentials.
   364	
   365	Merge alone does not establish deployment readiness. The orchestrator records deployment, the worker-directory login, effective startup checks and the Codex permgate rule before releasing dependent hardening tasks for live operation.
   366	
   367	## Checks (pasted by the orchestrator before each send)
   368	
   369	```
   370	(pasted at dispatch)
   371	```
   372	
   373	Local Bats, live enforcement, worker-directory login, permgate policy changes and deployment are not performed by the worker.
   374	Deployment remains unverified until the operator completes the post-merge steps; same-UID host access and concurrent path consumption remain stated residuals.
exec
/bin/zsh -lc "sed -n '1,175p' .orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md" in ~/Workspace/dotfiles
 succeeded in 20ms:
---
format: 2
task_id: dotfiles-T133-worker-write-boundary-a01
kind: code
security: true
allowed_files:
  - home/dot_agents/agent-config.yaml
  - home/.chezmoitemplates/claude-settings-managed.json
  - home/.chezmoitemplates/claude-worker-settings.json
  - home/dot_claude-worker/modify_private_settings.json
  - home/dot_claude/hooks/executable_orchestrator-only.sh
  - .claude/settings.json
  - scripts/generate-agent-configs.py
  - home/dot_local/bin/common/executable_herdr-agents
  - home/dot_local/bin/common/executable_herdr-agent-state.sh
  - home/dot_agents/skills/agmsg-orchestration/SKILL.md
  - .gitignore
  - tests/unit/test_generate_agent_configs.py
  - tests/unit/test_claude_settings_merge.py
  - tests/unit/test_herdr_agents.py
  - tests/unit/test_claude_worker_settings.py
  - .orchestration/dotfiles-T133-worker-write-boundary-a01/**
after: []
threat_table:
  - control: "home/dot_agents/agent-config.yaml (trusted checkout and interpreter bindings, distinct Claude worker policy, sandbox startup and worker cache policy)"
    disposition: "residual: the rendered policy reduces accidental and injected damage; tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_policy_is_separate_from_orchestrator_policy checks both platforms without claiming same-UID isolation."
  - control: "home/.chezmoitemplates/claude-settings-managed.json (orchestrator settings with failIfUnavailable true and onFailure block)"
    disposition: "residual: the shared baseline retains orchestrator behavior and reduces silent startup and hook failures; tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_orchestrator_settings_keep_existing_policy checks the merged settings."
  - control: "home/.chezmoitemplates/claude-worker-settings.json (worker Edit denies, empty exclusions, restricted socket and write allowances, and minimal delivery hooks)"
    disposition: "residual: dedicated settings reduce worker access to trusted paths and host execution routes; tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_policy_renders_for_both_platforms checks the complete rendered policy."
  - control: "home/dot_claude-worker/modify_private_settings.json (deployment of the dedicated worker baseline without importing orchestrator policy)"
    disposition: "residual: authoritative managed policy reduces stale or permissive worker configuration; tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_settings_replace_stale_policy_idempotently checks repeated rendering and merging in temporary homes."
  - control: "home/dot_claude/hooks/executable_orchestrator-only.sh (anchored launch-root guard for tracked project hooks)"
    disposition: "residual: the guard reduces execution of worker-influenced project code; tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_project_guard_uses_launch_root_and_never_runs_worker_payloads checks fixed arguments, canonical identity and child status."
  - control: ".claude/settings.json (every tracked project command routed through the installed guard with absolute interpreters and onFailure block)"
    disposition: "residual: guarded commands reduce worker-triggered project-hook execution; tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_every_tracked_project_hook_is_guarded_and_blocks_on_failure exhaustively traverses the hook entries."
  - control: "scripts/generate-agent-configs.py (separate settings generation, sanitized tracked-path enumeration and absolute executable bindings)"
    disposition: "residual: trusted rendering reduces configuration mistakes and injected executable selection; tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_deny_inventory_uses_sanitized_anchored_git checks the command, inventory and render inputs."
  - control: "home/dot_local/bin/common/executable_herdr-agents (worker pane environment, dedicated configuration directory, private caches and trusted delivery setup)"
    disposition: "residual: launch preparation reduces inheritance of orchestrator capabilities and stale hooks; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_every_worker_launch_receives_dedicated_policy_and_private_caches captures managed and standalone launches and repeated starts."
  - control: "home/dot_local/bin/common/executable_herdr-agent-state.sh (repository-owned Herdr state helper with an explicitly supplied absolute Python interpreter)"
    disposition: "residual: binding the helper and its Python child reduces shim execution; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_hook_descendants_do_not_execute_path_interpreters checks executed identities with planted shims."
  - control: "home/dot_agents/skills/agmsg-orchestration/SKILL.md (the governing Worker Playbook step 4 sentence)"
    disposition: "residual: the sentence removes procedural authorization for worker sandbox escapes; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_playbook_requires_every_command_inside_sandbox checks its replacement."
  - control: ".gitignore (the .uv-cache directory pattern)"
    disposition: "residual: ignoring the private cache reduces accidental cache publication; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_uv_cache_directory_is_gitignored checks the pattern in a temporary checkout."
  - control: "tests/unit/test_generate_agent_configs.py (separate platform policies, inventory generation, interpreter bindings and tracked hook coverage)"
    disposition: "residual: render fixtures verify configuration and command construction; they do not establish live enforcement or authenticate host-local inputs."
  - control: "tests/unit/test_claude_settings_merge.py (orchestrator baseline preservation and failure-policy rendering through the existing merge)"
    disposition: "residual: temporary HOME fixtures verify managed entries and identify runtime-added hooks separately; they do not apply live settings."
  - control: "tests/unit/test_herdr_agents.py (every launch route, repeated starts, hook descendants, caches and retained native denials)"
    disposition: "residual: fake launchers and subprocess markers verify effective arguments and executed fixture identities without starting live seats."
  - control: "tests/unit/test_claude_worker_settings.py (dedicated settings deployment, deny inventory, project guard, socket restrictions and hook failure configuration)"
    disposition: "residual: fixtures verify the configured controls and guard behavior; runtime permission checks and their remaining path-consumption window remain documented host residuals."
  - control: ".orchestration/dotfiles-T133-worker-write-boundary-a01/** (this task's branch artifacts)"
    disposition: "residual: artifacts distinguish documentation facts, historical probes, final-head fixture results and unperformed operator deployment; acceptance compares their claims with the diff and CI."
  - control: "the task-file copy at .orchestration/dotfiles-T133-worker-write-boundary-a01/task.md"
    disposition: "residual: the first push includes the byte-identical dispatched task; TASK and RESULT carry its SHA256, which the orchestrator verifies at acceptance."
  - control: "the evidence records under .orchestration/dotfiles-T133-worker-write-boundary-a01/"
    disposition: "residual: report.md, validation.md, sandbox.md, learning.md, autoskill.md and worker review evidence retain commands, outputs, statuses and tested revisions without credentials or unmasked home-directory paths."
  - control: "task metadata (PR_FEEDBACK_EVIDENCE, AUDIT_EVIDENCE, ACCEPTANCE_EVIDENCE and REVIEW_EVIDENCE)"
    disposition: "residual: the orchestrator checks C1 to C10 and C7b, verifies dispatched bytes and binds integration evidence to the final head; evidence of record is retrieved from GitHub at its SHA under the regime rule implemented by P1-14 a05 and P1-6."
  - control: metadata separators
    disposition: "residual: the first document separators delimit format-2 metadata; the task-copy SHA256 binds the complete document."
  - control: in-process effects
    disposition: "residual: generation and tests use repository files and temporary fixtures; the worker performs no live deployment, login, permission-policy mutation or operator-session restart."
  - control: workflow and interpreter or environment inputs
    disposition: "residual: absolute interpreters, Python -I, sanitized Git and trusted executable bindings reduce environment injection; the host, native loader and same-UID processes remain outside this task's security guarantee."
  - control: new or renamed scripts
    disposition: "residual: the worker settings modify script, orchestrator-only guard and repository-owned Herdr state helper have named source and installed paths; RESULT inventories their interpreter and descendant bindings without introducing a worker-write-boundary hook or gh wrapper."
  - control: "5.14 item 0: threat model"
    disposition: "residual: host controls reduce accidental and injected damage and do not close a boundary between seats sharing one OS user; GitHub is the hard boundary, and approvals and gate evidence of record come from its API at a SHA inside the sandbox."
  - control: "5.14 item 1: worker write controls"
    disposition: "residual: dedicated configuration, symlink-aware Edit denies, restricted sandbox capabilities and failIfUnavailable true reduce damage; documented requested-path and resolved-target checks address static symlink redirection without claiming atomic immunity to a concurrent path swap."
  - control: "5.14 item 2: sanitized environment and private executable PATH"
    disposition: "residual: sanitized anchored Git enumeration and absolute hook interpreter bindings reduce injected configuration and shim execution; the remaining consuming-helper contracts belong to P1-14 a05, P1-10 a02, audit-pool-a02 and P1-6."
  - control: "5.14 item 3: trusted-path checks"
    disposition: "residual: canonical anchor and interpreter checks reduce worker-selected trusted paths and account for symlink components and filesystem case aliases; other consuming-helper checks remain with their owning hardening tasks."
  - control: "5.14 item 4: verified executable and consumed-byte identity"
    disposition: "residual: hooks execute their selected absolute interpreter and trusted script without rediscovery; evidence snapshots, last-use digest checks and their race limitations remain with the consuming orchestrator-side tasks."
  - control: "5.14 item 5: output and reservation identity"
    disposition: "residual: this task adds no reservation protocol; full-head output names, fixed-inode locks and physical-slot identity remain with the orchestrator-side tasks that create them."
  - control: "5.14 item 6: honest residuals, hooks and MCP"
    disposition: "residual: guarded project hooks, minimal worker delivery hooks and removal of the worker Herdr socket allowance reduce host execution routes; approved external processes and same-UID processes outside every seat sandbox remain residual."
  - control: "5.14 item 7: trusted-execution verification"
    disposition: "residual: this task records red-then-green render, merge, guard, launch, descendant and cache tests; P1-6 owns tests/unit/trusted_exec_contract.py and the consuming-helper contract tests."
  - control: "5.14 item 8: committed approval ledger"
    disposition: "residual: the regime reads the ledger through the GitHub contents API at the SHA returned by git ls-remote origin refs/heads/main; P1-14 a05 implements that read, and local refs, files and object traversal provide no approval authority."
  - control: "5.14 item 9: private uv caches"
    disposition: "residual: per-seat worker caches and restricted worker write allowances reduce cache poisoning; consuming hardening tasks use the protected orchestrator cache with --offline and execute no worker, shared uv or mise cache content."
  - control: "5.14 item 10: no worker command outside the sandbox"
    disposition: "residual: empty worker exclusions, disabled unsandboxed requests, absent Herdr socket allowance and Codex in-sandbox network reduce escape routes; the deterministic Codex permgate rule and live deployment remain operator steps."
  - control: "hook failure policy"
    disposition: "residual: every generated and tracked hook entry carries onFailure block, reducing fail-open behavior where Claude supports it; configuration tests cover missing-command and timeout policy, while background hooks and events on which the field has no effect carry no enforcement responsibility."
  - control: orchestrator effect merge
    disposition: "residual: the worker never merges; the orchestrator follows the final-head integration gate, required permission approval and pinned squash-merge procedure, with evidence of record retrieved from GitHub."
  - control: orchestrator effect update-branch
    disposition: "residual: the orchestrator owns branch updates and obtains fresh required CI, feedback, audit and security evidence for the resulting head."
  - control: orchestrator effect forced worker removal
    disposition: "residual: no forced removal is planned; existing dirty-worktree protections remain, and acceptance identifies any operator-authorized discarded state."
premises:
  - claim: >-
      The historical a05 premises carried by the preceding text describe its recorded observations. They do not require this worker to rebuild PR 400, edit the approval ledger or implement P1-14 a05.
    sources:
      - .orchestration/tasks/dotfiles-T133-permission-guard-gate-a05.md
      - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md
  - claim: >-
      D-024-21 establishes the current threat model and dedicated Claude worker configuration. The earlier cwd-hook, launch-root-hook and local Git ledger proposals remain historical records.
    sources:
      - .orchestration/decisions.tsv
      - .orchestration/plans/024-design-quality.md
      - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md
  - claim: >-
      The existing Claude settings modify script merges the managed baseline into current settings and appends an attachment hook. The dedicated worker renderer must not import that orchestrator settings merge or its attachment behavior.
    sources:
      - home/dot_claude/modify_private_settings.json
      - home/.chezmoitemplates/claude-settings-managed.json
    verification: tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_settings_do_not_import_orchestrator_hooks
  - claim: >-
      The current launcher constructs worker profile options separately from the pane environment. The dedicated configuration directory and private cache variables must reach the actual Claude process on every worker launch route.
    sources:
      - home/dot_local/bin/common/executable_herdr-agents
      - home/dot_agents/agent-config.yaml
    verification: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_every_worker_launch_receives_dedicated_policy_and_private_caches
---

# AGMSG-TASK dotfiles-T133-worker-write-boundary-a01 — plan 024 P1-15 under D-024-17, D-024-19, D-024-20 and D-024-21

## Goal

The host is not a security boundary between seats sharing one OS user. The regime's hard boundary is GitHub: protected main, required checks and merge through the orchestrator's identity. Approvals and gate evidence of record are read from GitHub at a SHA through its API inside the sandbox. Host-local controls in this task reduce accidental and injected damage. They do not establish isolation from a malicious same-UID process.

This task implements section 5.14 items 1, 9 and 10 through a dedicated Claude worker configuration directory, Edit deny rules on trusted paths, guarded tracked project hooks, absolute hook interpreter bindings, private worker caches and sandboxed worker commands. Every Claude seat has `sandbox.failIfUnavailable: true`. Codex workers have `sandbox_workspace_write.network_access=true`.

[memory:decision] D-024-20 makes this task the dispatch prerequisite of P1-14 a05, P1-10 a02, audit-pool-a02 and P1-6. The orchestrator places this task in their `after:` fields before dispatch. This task has `after: []`. A Codex seat performs these Claude configuration edits under the routing rule, including the Worker Playbook step 4 sentence permitted by plan 021 step 8.3.

The design source is `.orchestration/plans/024-design-quality.md` section 5.14 items 0 through 10. D-024-21 and the amended items 0, 1 and 8 govern this revision. The acceptance record preserves the documentation facts and earlier proposals as history.

The third C-80 text review is `.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-ecc7ab5.md.last.md`. Its five P1 findings remain recorded. This revision replaces the custom file-tool boundary hook with documented symlink-aware deny rules, moves approval reads out of the local object database, binds hook descendants to absolute interpreters, removes the worker Herdr socket allowance and specifies runtime-level hook failure policy.

The file-tool rule is the documented sentence, “Deny rules: apply when either the requested path or the file it resolves to matches.” Edit and Write refuse a requested file that is itself a symlink. Directory symlinks are subject to resolved-target permission checks, and the tools check the resolved location again when opening the approved file. These documented checks address the preceding text's validation-only design. They do not establish an atomic host security boundary against concurrent same-UID changes. [Claude permission reference](https://code.claude.com/docs/en/permissions#symlinks)

The 2026-10-19T03:45:06Z sandbox probe ran `gh api repos/mryfmo/dotfiles --jq .name` and returned `dotfiles`. The recorded sandbox proxy used CONNECT without TLS interception, and gh read the Keychain token. This is a historical host observation. It does not establish enforcement or credential readiness for the new worker directory on either platform.

The documentation facts recorded at 03:2xZ establish that Edit denies also affect the Bash sandbox, hooks reload during a session and an unavailable sandbox is fail-open by default. D-024-21's 04:0xZ decision establishes the dedicated configuration mechanism, directory-specific credentials, symlink coverage and `onFailure: "block"` support. The earlier shared-user-hook proposal is superseded.

## Files

1. `home/dot_agents/agent-config.yaml` remains the source of agent policy and model profiles.

   The manifest names `orchestrator_checkout` as the anchored primary checkout and supplies trusted deployment bindings for the guard, hook scripts and absolute interpreters. These bindings resolve outside worker worktrees and executable caches. Worker cwd, tool input, worktree configuration and inherited command variables do not select them.

   The manifest defines a separate Claude worker settings output at `home/.chezmoitemplates/claude-worker-settings.json`. The worker configuration directory is `~/.claude-worker`. The launcher passes its expanded absolute path as `CLAUDE_CONFIG_DIR`.

   The orchestrator policy retains its existing permissions, exclusions, socket access, cache allowances and hook functions. Its required policy changes are `failIfUnavailable: true` and `onFailure: "block"` on its hooks. The interpreter bindings required below preserve those hook functions.

   The worker policy contains no excluded commands and sets `allowUnsandboxedCommands: false`. It contains no Herdr socket allowance and no allow-all Unix socket switch. Its sandbox is enabled and has `failIfUnavailable: true`.

   Worker `sandbox.filesystem.allowWrite` contains only the existing agmsg store paths and per-seat cache paths. The worktree is the project root and supplies its ordinary project write root. Shared uv and mise write allowances are not copied into worker settings.

   The Codex worker profile sets `sandbox_workspace_write.network_access=true`. Existing model selections and Codex shared Git grants retain their meaning. The deterministic Codex permgate rule that stops approving sandbox escapes is an operator step.

2. `scripts/generate-agent-configs.py` renders the distinct orchestrator and worker baselines from the manifest.

   The trusted-path deny inventory is generated at render time from the anchored checkout's tracked tree using `git ls-tree`. The inventory covers every top-level tracked path outside `.claude/worktrees/`. The `.claude` entry is expanded sufficiently to protect its tracked contents without emitting a parent deny that also denies worker worktrees. Directory and file entries receive patterns appropriate to their complete protected extent.

   Anchored checkout rules use absolute `//` permission patterns. Rendering includes the trusted paths themselves and their descendants. It emits no checkout-wide parent deny that defeats the `.claude/worktrees/` exclusion.

   Worker Edit denies also cover `~/.agents/**`, `~/.claude/**`, `~/.claude-worker/**`, `~/.local/**`, `~/.config/**`, `~/.cache/uv/**` and `~/.local/share/uv/**`. The rules protect the corresponding directory targets as well as their contents.

   Edit denies cover Write, MultiEdit and NotebookEdit through Claude's permission system. Requested-path and resolved-target matching supply the documented symlink coverage. The generator does not create `executable_worker-write-boundary.py` or a replacement PreToolUse path validator.

   Every direct Git verification introduced or changed by this task follows section 5.14 item 2. It begins with `env -i`, uses the selected absolute Git executable and an explicit `-C`, sets `GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL=/dev/null`, and supplies `-c core.hooksPath=/dev/null -c core.fsmonitor=false -c protocol.allow=never -c protocol.https.allow=always`. Diff and show also use `--no-ext-diff --no-textconv` and `-c core.attributesFile=/dev/null -c core.sshCommand=false`.

   The private executable-link directory contains only links to selected absolute trusted binaries. Rendering rejects missing bindings, worker-controlled executable paths, shims, empty PATH entries and relative PATH entries. Python invocations use `-I`.

exec
/bin/zsh -lc "rg -n -A 32 -B 2 'Codex seat worklogs' ~/.agents/skills/agmsg-orchestration/SKILL.md" in ~/Workspace/dotfiles
 succeeded in 1ms:
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
248-Optional frontmatter keys are `depends_on` (todo ID array), `blocked_reason`
249-for blocked work, `evidence` (path array), and `tags`.

exec
/bin/zsh -lc 'cat ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail/SKILL.md; cat ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail-review/SKILL.md' in ~/Workspace/dotfiles
 succeeded in 7ms:
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

**Seeking efficient text and references**
codex
Ponytail のレビュー手順と agmsg-orchestration の記録規則を確認しました。今回は読み取り専用の依頼なので、worklog やレビュー証跡ファイルは作成せず、指摘をこの応答にまとめます。

exec
/bin/zsh -lc 'cat .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md' in ~/Workspace/dotfiles
exec
/bin/zsh -lc 'cat .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-ecc7ab5.md.last.md' in ~/Workspace/dotfiles
exec
/bin/zsh -lc "nl -ba .orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md | sed -n '175,257p'" in ~/Workspace/dotfiles
exec
/bin/zsh -lc "git --no-optional-locks status --short; cat .ua/meta.json; rg -n '5\\.14|D-024-21' .orchestration/plans/024-design-quality.md .orchestration/decisions.tsv" in ~/Workspace/dotfiles
 succeeded in 140ms:
   175	   The private executable-link directory contains only links to selected absolute trusted binaries. Rendering rejects missing bindings, worker-controlled executable paths, shims, empty PATH entries and relative PATH entries. Python invocations use `-I`.
   176	
   177	   `tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_deny_inventory_uses_sanitized_anchored_git` records the exact Git environment and arguments. Its fixtures cover a newly tracked top-level path, tracked files, tracked directories, `.claude` children, the worktree exclusion and an anchor containing spaces.
   178	
   179	3. `home/.chezmoitemplates/claude-settings-managed.json` remains the orchestrator baseline.
   180	
   181	   The existing `home/dot_claude/modify_private_settings.json` continues to render the orchestrator's `~/.claude/settings.json`. That modify script is not imported into the dedicated worker renderer and remains outside `allowed_files`.
   182	
   183	   The orchestrator retains its current policy content apart from `failIfUnavailable: true`, `onFailure: "block"` and the required absolute interpreter bindings. Worker-specific Edit denies, empty exclusions and restricted socket policy do not enter this shared baseline.
   184	
   185	   Every managed hook entry carries `onFailure: "block"`. Merge evidence identifies hooks appended by the existing modify script and distinguishes them from generated baseline entries. The report accounts for the effective deployed hook set and does not equate baseline coverage with coverage of runtime-added entries.
   186	
   187	   `tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_orchestrator_settings_keep_existing_policy` compares the merged policy with the preceding baseline. Repeated merging remains idempotent and preserves unrelated settings.
   188	
   189	4. `home/.chezmoitemplates/claude-worker-settings.json` is the dedicated worker baseline.
   190	
   191	   It renders the trusted-path Edit denies, empty `excludedCommands`, `allowUnsandboxedCommands: false`, restricted `allowWrite`, absent Herdr socket allowance and `failIfUnavailable: true` for both Darwin and Linux.
   192	
   193	   Its hooks are limited to agmsg delivery. It contains no formatter, project-map, permgate, orchestrator attachment, Herdr state or worker-write-boundary hook. Project hooks still load from the tracked `.claude/settings.json` and receive the guard described below.
   194	
   195	   Every worker hook entry carries `onFailure: "block"`. Command hooks invoke the installed agmsg scripts through the selected absolute shell interpreter. Their script paths are absolute paths beneath the trusted installed agmsg root.
   196	
   197	   The worker baseline does not copy the orchestrator's plugins, credential files or current hook arrays. Hook settings reload during a session, so protection is stated as current configuration rather than startup capture. `CLAUDE_CONFIG_DIR` selects the separate user settings directory while project settings continue to apply. [Claude settings reference](https://code.claude.com/docs/en/settings)
   198	
   199	5. `home/dot_claude-worker/modify_private_settings.json` renders `~/.claude-worker/settings.json` from the dedicated baseline.
   200	
   201	   The script follows the existing chezmoi modify-script interface: current content arrives on stdin and the desired settings object is written to stdout. It uses Python's standard library and the same trusted source and home resolution conventions as the existing renderer.
   202	
   203	   Managed worker permissions, sandbox policy and hooks replace stale managed values. Permissive old exclusions, socket allowances, hook commands and shared cache allowances do not survive as additive worker policy. The script does not read or copy `~/.claude/settings.json`.
   204	
   205	   Rendering handles empty and malformed input through the repository's existing baseline behavior and is idempotent. It neither reads credentials nor initiates authentication.
   206	
   207	   `tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_settings_replace_stale_policy_idempotently` exercises repeated deployment in temporary homes. `tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_settings_do_not_import_orchestrator_hooks` plants orchestrator hook and plugin markers and verifies their absence.
   208	
   209	6. `home/dot_claude/hooks/executable_orchestrator-only.sh` is installed as `~/.claude/hooks/orchestrator-only.sh`.
   210	
   211	   The guard runs under the selected absolute shell interpreter and compares canonical `CLAUDE_PROJECT_DIR` with the anchored checkout. Equality executes the supplied fixed command. Every other launch root exits 0 without executing it.
   212	
   213	   Worker launch roots, sibling worktrees and unrelated checkouts execute no guarded project code. Missing or unresolvable launch-root identity also executes no supplied command. Event cwd does not change the launch-root decision.
   214	
   215	   The guard preserves argument boundaries, stdin and child exit status. It performs no eval, PATH interpreter lookup or worktree-relative script selection.
   216	
   217	   `tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_project_guard_uses_launch_root_and_never_runs_worker_payloads` plants worker Stop, contextdb and formatter payloads. Worker and unrelated-root invocations leave all markers absent. The anchored invocation reaches the selected fixture interpreter and preserves its arguments and status.
   218	
   219	7. `.claude/settings.json` retains its tracked project hooks and rewrites every command through the installed orchestrator-only guard.
   220	
   221	   The guard invocation uses its absolute installed path and absolute shell interpreter. The guarded child command uses an absolute interpreter and an anchored script path. Contextdb commands do not invoke bare `python3` or select `.claude/hooks` from a worker checkout. The Stop gate does not invoke bare `bash` or a worker checkout's `scripts/agent-stop-gate.sh`.
   222	
   223	   Every hook entry carries `onFailure: "block"`. Existing event functions remain available to the anchored orchestrator. They are no-ops in worker sessions because the guard rejects their launch roots.
   224	
   225	   `tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_every_tracked_project_hook_is_guarded_and_blocks_on_failure` traverses every event, matcher and command entry. It rejects unguarded commands, missing failure policy, relative interpreters and worker-selected executable paths.
   226	
   227	8. `home/dot_local/bin/common/executable_herdr-agents` supplies the dedicated worker configuration at the actual worker launch boundary.
   228	
   229	   Every Claude worker pane starts with `CLAUDE_CONFIG_DIR=<absolute-home>/.claude-worker`. The value reaches the Claude process through the pane command and environment construction. Setting it only in the parent spawn process does not satisfy this requirement.
   230	
   231	   Managed-workspace and standalone-worker routes receive the same binding. Repeated starts do not inherit a caller's conflicting configuration directory.
   232	
   233	   Every worker launch exports `UV_CACHE_DIR=<absolute-worktree>/.uv-cache` and `UV_PYTHON_INSTALL_DIR=<absolute-worktree>/.uv-cache/python`. Both worker kinds receive values derived from the selected canonical worktree. Caller-provided values do not replace them.
   234	
   235	   Before every Claude worker start, the launcher regenerates managed local delivery entries from trusted inputs. An existing delivery match does not skip preparation. Stale managed commands are replaced, and unknown command hooks are not promoted into the trusted delivery set.
   236	
   237	   Local settings retain existing native merge denials. They do not reintroduce excluded commands, the Herdr socket, unsandboxed requests or orchestrator hooks. The effective delivery set contains no duplicate managed invocation.
   238	
   239	   Codex launches retain `--sandbox workspace-write`, `--ask-for-approval never` and `sandbox_workspace_write.network_access=true`. Tests inspect effective launch arguments rather than inferring them from the base manifest.
   240	
   241	   The retained Codex Git grant permits shared `.git/objects`, `.git/refs`, `.git/logs` and the worker's administration directory. It does not authenticate local ledger content and is not represented as a host security boundary.
   242	
   243	   `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_every_worker_launch_receives_dedicated_policy_and_private_caches` covers both worker kinds and all launch routes. `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_repeated_worker_start_replaces_stale_managed_hooks` covers repeated preparation. `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_commands_have_no_unsandboxed_launch_route` checks effective exclusions, socket policy, sandbox requests and retained merge denials.
   244	
   245	9. `home/dot_local/bin/common/executable_herdr-agent-state.sh` provides the repository-owned Herdr state helper installed as `~/.local/bin/common/herdr-agent-state.sh`.
   246	
   247	   The currently installed `~/.claude/hooks/herdr-agent-state.sh` is generated by Herdr and is not a tracked source in this repository. Its bare `python3` descendant is not retained as a trusted worker hook. The repository-owned helper preserves the required state-reporting function and receives its absolute Python interpreter through the rendered invocation.
   248	
   249	   Every hook command and every interpreted descendant it runs uses a selected absolute interpreter. Repository-owned shell descendants use absolute shebangs or explicit absolute shell invocations. Python descendants use the selected absolute interpreter with `-I`. No trusted hook route reaches bare `python3` or an `/usr/bin/env bash` shebang through PATH.
   250	
   251	   The delivery inventory names `~/.agents/skills/agmsg/scripts/session-start.sh`, `~/.agents/skills/agmsg/scripts/check-inbox.sh` and every additional delivery descendant actually reached. Scripts outside this repository are invoked with the absolute interpreter in the hook command itself. Their installed files are not edited or vendored.
   252	
   253	   The inventory records source ownership, installed path, caller and interpreter for each reached script. Binding only the first command does not establish descendant coverage.
   254	
   255	   `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_hook_descendants_do_not_execute_path_interpreters` executes the fixture hook routes with planted Python and Bash shims. It checks descendant markers and actual selected interpreter identities. Capturing launcher command strings alone does not satisfy this test.
   256	
   257	10. `home/dot_agents/skills/agmsg-orchestration/SKILL.md` changes only the Worker Playbook step 4 sentence that lists outside-sandbox worker commands.

 succeeded in 208ms:
---
{
  "audit_findings": [],
  "dispatch": [],
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

 succeeded in 242ms:
- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:273](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:273) The race acceptance rests on a false premise: a sandboxed worker can swap an allowed directory for a symlink after validation, causing the unsandboxed file tool to overwrite a trusted path that the worker cannot write directly; static path tests cannot close this boundary.

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:80](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:80) Remote SHA pinning and `--no-replace-objects` do not authenticate the writable object database: replacing an intermediate tree object can redirect ledger lookup to an attacker’s valid blob because that traversal does not verify the intermediate object’s content hash. [Git tree traversal](https://github.com/git/git/blob/v2.51.0/tree-walk.c), [object reading](https://github.com/git/git/blob/v2.51.0/odb.c).

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:219](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:219) Absolute hook entrypoints do not bind their descendants: retained `herdr-agent-state.sh:25` invokes bare `python3`, while delivery invokes scripts with `/usr/bin/env bash` shebangs; the specified launcher captures and tracked-hook tests miss these unsandboxed, PATH-resolved executions on this shim-first host. [Mise shim resolution](https://mise.jdx.dev/dev-tools/shims.html).

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:84](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:84) The table omits the retained Herdr socket capability (`agent-config.yaml:325`): a sandboxed client can request terminal execution through the host server, whose existing driver uses `pane run`; refusing excluded command names does not restrict socket RPCs or the resulting host execution. [Unix-socket escape risk](https://code.claude.com/docs/en/sandboxing#security-limitations).

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:275](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:275) Startup validation does not mitigate a later hook timeout or termination, which permits the protected action; Python exit-2 tests therefore leave enforcement fail-open, although Claude provides runtime-level `onFailure: "block"` starting with v2.1.295. [Hook failure control](https://code.claude.com/docs/en/hooks#block-the-action-when-a-hook-fails).

📝 まとめ: Reviewed the task, every threat row, and cited acceptance/review context; five findings remain for orchestrator disposition. No files changed.

Not checked: implementation tests or live enforcement; write isolation and approval integrity remain unestablished.
Verdict: incorrect
 succeeded in 263ms:
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
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-chain-3f12e60.log
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-chain-63b6aca.log
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-chain-8a09b93.log
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
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-67415f5.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-67415f5.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-8bac9e5.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-8bac9e5.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-8d42532.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-ecc7ab5.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-ecc7ab5.md.last.md
{
  "lastAnalyzedAt": "2026-10-02T14:12:51Z",
  "gitCommitHash": "940a3a2b07adfd14140a0acff96784ef53a0a509",
  "version": "1.0.0",
  "analyzedFiles": 368
}
.orchestration/plans/024-design-quality.md:99:## 5.14 信頼ホスト実行契約（trusted-host execution contract、D-024-18）
.orchestration/plans/024-design-quality.md:109:0. **脅威モデル（D-024-21）** 席は同じ OS ユーザで動き、ホストは席間の信頼境界ではない（同一 UID のプロセスは symlink 差し替え、共有 `.git` の object 差し替え、hook の子プロセス、Herdr socket 経由の host 実行で、ホスト内のどの検査も迂回できる）。regime の硬い境界は GitHub（保護された main、必須チェック、orchestrator の identity によるマージ）。悪意ある worker に耐えるべき入力（承認台帳、gate が読む証跡 of record）は GitHub から sha 指定で API 経由（sandbox 内）に読み、ローカルファイルやローカル object database からは読まない。ホスト内の制御（本節 1〜10）は事故と prompt injection による損害の抑制であり、文はそう書く。
.orchestration/decisions.tsv:64:D-024-18	2026-10-19T02:5xZ	every security: true orchestrator-side task text applies design section 5.14 (trusted-host execution contract: the write-boundary premise, sanitized environment first, trusted-path boundary checks, execute-what-you-verified, 40-hex identities and inode-bound locks, honest residuals, four shared red-then-green tests) by reference, with one threat row per item	the C-80 reviews of three texts on 2026-10-19 (permission-guard-gate-a05, dispositions-a02, audit-pool-a01: 19 P1 in total) found the same unstated premise and the same gaps in each; a design-tier contract replaces per-text rewording (M-20261019-03 class)	default under the autonomy directive, reported 2026-10-19 12:0x JST; scope=design	applied-from-a05-and-the-a02-texts
.orchestration/decisions.tsv:65:D-024-19	2026-10-19T03:0xZ	permission decision rows are read from the committed ledger (git show origin/main:.orchestration/decisions.tsv after fetch), never from the working copy; a working-copy row is a proposal until the records PR carrying it merges, and that PR approval is the operator's operation (design 5.14 item 8)	the second C-80 review of the a05 text: a Claude worker seat's file tools run outside the Seatbelt sandbox and the rendered policy has no path deny, so a same-UID forged row in the working-copy ledger was possible; the committed ledger moves forgery behind a protected-branch merge	default under the autonomy directive, reported 2026-10-19 12:0x JST; the consequence is one records PR (boundary 24) before the a05 merge, approved by the operator through the live hook; scope=design,permission	applied-from-a05
.orchestration/decisions.tsv:66:D-024-20	2026-10-19T03:1xZ	P1-15 (the worker write boundary: deny rules for the Claude file tools on every trusted path outside the seat worktree, hooks and MCP locked, per-seat caches, the gh wrapper of D-024-17) is implemented before and as the dispatch prerequisite (after:) of every orchestrator-side security: true task (P1-14 a05, P1-10 a02, audit-pool-a02, P1-6); the orchestrator review worktree moves out of .claude/worktrees/ (design 5.14 item 3)	the C-80 reviews of 2026-10-19 (a05 twice, dispositions-a02 twice, audit-pool-a01) all reduce to the unstated Claude-seat boundary; hardening texts dispatched before it carry false closed rows	default under the autonomy directive, reported 2026-10-19 12:1x JST; scope=design	applied
.orchestration/decisions.tsv:67:D-024-21	2026-10-19T04:0xZ	threat model and mechanism of the worker boundary: the host is not a security boundary between seats sharing one OS user; the hard boundary is GitHub (protected main, required checks, the orchestrator identity merge); approvals and gate evidence of record are read from GitHub at a sha through the API inside the sandbox; Claude worker seats run under their own CLAUDE_CONFIG_DIR (~/.claude-worker: no excluded commands, no Herdr socket, Edit denies on trusted paths with symlink coverage, failIfUnavailable true, minimal trusted hooks with onFailure block); host-local controls target accidental and injected damage and the texts say so (design 5.14 items 0, 1, 8)	three C-80 reviews of the P1-15 text (03:24Z, 03:42Z, 03:58Z) found host-level escapes no in-process check closes (symlink swap race, writable object database, hook descendants through shims, Herdr socket RPC, hook timeout fail-open); the documentation confirms per-directory settings and credentials (one operator login for the worker directory), onFailure block (>= 2.1.295; installed 2.1.300), and symlink-aware file-tool deny rules	default under the autonomy directive, reported 2026-10-19 13:0x JST; the worker-directory login is an operator step at the P1-15 deployment; scope=design,permission	applied-to-the-P1-15-text

**Allocating time and resources**
web search: 
exec
/bin/zsh -lc "sed -n '99,145p' .orchestration/plans/024-design-quality.md; cat .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-8bac9e5.md.last.md; cat .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-67415f5.md.last.md" in ~/Workspace/dotfiles
exec
/bin/zsh -lc "sed -n '1,160p' .orchestration/tasks/dotfiles-T133-permission-guard-gate-a05.md; sed -n '250,355p' home/dot_agents/agent-config.yaml; cat .claude/settings.json" in ~/Workspace/dotfiles
 succeeded in 156ms:
## 5.14 信頼ホスト実行契約（trusted-host execution contract、D-024-18）

orchestrator 側の仕組み（merge gate、integrate-merge、orch-gate、dispositions、audit-pool、verdict、chain）は、同じホスト上で同じ UID の worker プロセスと共存する。2026-10-19 の C-80 審査（a05、dispositions-a02、audit-pool-a01 の 3 文、計 19 件の P1）は、どの文も同じ前提を書かず同じ穴を持つことを示した。以後、`security: true` の orchestrator 側タスク文は本節を参照で適用し、本節の各項目に対応する threat 行を持つ。文ごとに言い換えない。

1. **書き込み境界（前提 6、ランタイム別に正直に）** Claude worker 席は専用の設定ディレクトリ `CLAUDE_CONFIG_DIR=~/.claude-worker`（chezmoi が描画、operator が一度 login）で起動し、orchestrator の `~/.claude` と設定を共有しない。worker 設定：除外コマンド無し、Herdr socket 無し、sandbox の allowWrite は自席 worktree と agmsg store と席別キャッシュだけ、`failIfUnavailable: true`、信頼パス（anchored checkout の `.claude/worktrees/` 以外、`~/.agents`、`~/.claude*`、`~/.local`、`~/.config`）への Edit deny（公式文書：file tool の permission 検査は要求パスと symlink 解決後のパスの両方に deny を適用し、symlink そのものへの書き込みは拒否する）、hook は agmsg 配送と境界 hook だけを絶対パスのインタプリタで、各 hook に `onFailure: "block"`。公式文書で確認した事実（2026-10-19）：`Edit(path)` の deny は Write/MultiEdit/NotebookEdit にも効き、deny → ask → allow の順で最初の一致が決まる；ただし Read/Edit の deny は **Bash sandbox の設定にも合流する**（"Paths and domains from both sandbox settings and permission rules are merged into the final sandbox configuration"）ので、ユーザー設定（全席共有）に `.orchestration/**` の Edit deny を書くと orchestrator の Bash による記録書き込みも止まる。hook は起動時に固定されず、設定ファイルの編集は file watcher が即座に反映する。`sandbox.failIfUnavailable` の既定は fail-open（依存が無ければ sandbox 無しで実行）。したがって Claude 席の境界は Edit deny 規則ではなく、**ユーザーレベルの PreToolUse hook**（`~/.claude/hooks/worker-write-boundary`、chezmoi が描画、`/bin/sh` または絶対パスの `python3 -I`）で作る：cwd の realpath が `<anchored>/.claude/worktrees/` 配下の session では、Write/Edit/MultiEdit/NotebookEdit の対象が cwd の外、または `<cwd>/.claude/**`・`<cwd>/.mcp.json` のとき `permissionDecision: deny` を返す。Bash 側は sandbox の既定 `denyWithinAllow`（settings、hooks）と `allowWrite`（自席 worktree）が担う。`failIfUnavailable: true` を全席に置く。 Codex 席は sandbox（workspace-write）がツールの書き込み全部を自席の worktree と列挙パスに限る。Claude 席は Seatbelt sandbox が Bash を限るだけで、Write/Edit/MultiEdit/NotebookEdit、hook、MCP プロセスは sandbox 外で動き、permission policy（permgate の決定論ポリシー）が path で拒否しない限り anchored checkout や `~/.agents` にも書ける（2026-10-19 時点、描画済み設定にその deny は無い）。したがって前提 6 は「Codex 席は成立、Claude 席は P1-15 が描画設定に Edit の path deny を入れるまで残余」と書く。P1-15 以前に「worker は信頼ルートに書けない」と書く文は誤りで、C-80 が拒否する。P1-15 が入るまで、承認の出所は項目 8 の「コミット済み台帳」で守る。書き込みは自席の worktree（`.claude/worktrees/<name>`）、scratch、列挙されたツールキャッシュに限る。anchored checkout（`.claude/worktrees/` 以外）、`~/.agents/agent-config.yaml`、`~/.claude/hooks`、信頼ルートのバイナリ、orchestrator の証跡・スナップショット・lock は worker から書けない。render テストが描画後の deny を検証する。残余は「どの席 sandbox にも属さない同一 UID プロセス」と、Worker Playbook step 4 が sandbox 外に出す少数のコマンド（gh）。後者は D-024-17（P1-15）で絶対パスの実行体に束縛する。
2. **無害化した環境を最初に** 最初の処理として `env -i` に入り、PATH は信頼ルートで解決した絶対バイナリへのリンクだけの私設ディレクトリ（shims、空、相対は拒否）。git は毎回 `GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null -c core.hooksPath=/dev/null -c core.fsmonitor=false -c protocol.allow=never -c protocol.https.allow=always` と明示 `-C`（https だけ許す。`protocol.allow=never` 単独は必要な fetch を止める）。 diff と show は `--no-ext-diff --no-textconv` と `-c core.attributesFile=/dev/null -c core.sshCommand=false` を付け、PR 側の `.gitattributes`（external diff、textconv、filter）が検査内容や実行物を変えないようにする。Python は `-I`。PATH 探索で実行するものは無い。
3. **信頼パスの境界検査** 仕組みが信頼するパス（スクリプト、台帳、証跡、worktree、lock、出力先）は realpath で解決し、`.claude/worktrees/` または manifest の worker ルート配下なら拒否（ask/hold）。symlink 構成要素は解決後に比較し、大小文字を区別しないファイルシステムでは同一性比較を大小文字非依存で行う。
4. **検証したものを実行し、検証した内容を渡す** 検証した実行体はその realpath で実行する（再探索しない）。検証したファイル内容は信頼ルート配下のスナップショット（0600、一意名）として渡し、使用直前に sha256 を再照合する。判断に読んだ証跡は sha256 を出力に記録する。
5. **出力と予約の同一性** 名前には 40 桁の head を使う（7 桁で衝突させない）。lock は信頼ルート配下の固定 inode に O_EXCL で作り、置換を inode 比較で検出する。物理スロット 1 つに lock 1 つ。
6. **正直な残余** 境界だけが緩和するリスクを `closed` と書かない。各文は残余を 1 行で明記する。
0. **脅威モデル（D-024-21）** 席は同じ OS ユーザで動き、ホストは席間の信頼境界ではない（同一 UID のプロセスは symlink 差し替え、共有 `.git` の object 差し替え、hook の子プロセス、Herdr socket 経由の host 実行で、ホスト内のどの検査も迂回できる）。regime の硬い境界は GitHub（保護された main、必須チェック、orchestrator の identity によるマージ）。悪意ある worker に耐えるべき入力（承認台帳、gate が読む証跡 of record）は GitHub から sha 指定で API 経由（sandbox 内）に読み、ローカルファイルやローカル object database からは読まない。ホスト内の制御（本節 1〜10）は事故と prompt injection による損害の抑制であり、文はそう書く。
8. **承認はコミット済み台帳から読む** permission の決定行（`scope=permission approved_by=user diff_sha256=…`）は anchored checkout の作業コピーではなく、コミット済みの台帳から読む。読み方は `git ls-remote origin refs/heads/main` が返す commit sha を取り、GitHub API（`gh api repos/<owner>/<repo>/contents/.orchestration/decisions.tsv?ref=<sha>`、sandbox 内）でその sha の内容を取得する。ローカルの `git show` は共有 object database が書けるため中間 tree の差し替えで偽物を返しうる（第 3 回審査の所見 2）（ローカルの ref 名 `origin/main` は経由しない。`refs/replace/` も書けるので replacement を無効にする。Codex worker は `.git/objects` と `.git/refs` に書けるので ref は差し替えられるが、sha で指した object は内容アドレスで偽造できない）。作業コピーの行は提案で、記録 PR が main にマージされて初めて承認になる（PR の承認は操作者の操作）。偽造には main へのマージが要る。
9. **私設キャッシュ** orchestrator 側の実行は worker と共有するキャッシュ（`~/.cache/uv`、`~/.local/share/uv`、mise）から実行可能物を読まない。`UV_CACHE_DIR` を anchored checkout 配下（`.agents/worklog/uv-cache`、gitignored、worker 書き込み不可）に固定し、`--offline` で使う。hook は uv を使わず jq と python 標準ライブラリだけで動く。
10. **worker は sandbox 外でコマンドを実行しない（D-024-17 の改訂）** 2026-10-19T03:45Z の実測で `gh api` は Claude sandbox の中から成功した（sandbox の proxy は CONNECT 型で TLS を終端しない；keychain のトークンも読めた）。worker 席の除外コマンドは空にし、gh も git push も sandbox 内の proxy 経由で実行する。Codex 席は `sandbox_workspace_write.network_access = true` で同じ状態にし、permgate の codex ポリシーは sandbox 外への escape を承認しない（permgate の変更は操作者の手順）。wrapper 方式（絶対パス、env -i、固定 GH_CONFIG_DIR）は LD_PRELOAD と引数転送（`gh repo clone -- --config`）を閉じられないので採らない。
7. **検証** threat_table は本節の項目 1〜10 に 1 行ずつ対応させる（参照だけでは足りない）。共通テスト補助 `tests/unit/trusted_exec_contract.py`（P1-6 で作る）を使い、仕組みごとに 4 つの red→green テストを持つ：PATH 先頭の shim が実行されない、植え付けた GIT_* と git 設定が効かない、worker ルート配下の信頼パスが拒否される、検証後に差し替えたファイルが消費側に届かない。
- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:169](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:169) Verbatim argv forwarding permits `gh repo clone … -- --config core.sshCommand=<worker executable>` to execute worker code outside the Linux sandbox; fixed binaries and alias-free configuration do not close this path, and the named alias test never exercises it. [gh forwarding](https://cli.github.com/manual/gh_repo_clone), [Git configuration timing](https://git-scm.com/docs/git-clone).

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:163](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:163) An absolute noninteractive interpreter does not suppress Bash’s `BASH_ENV`; a read-only host probe printed the injected startup marker before the `env -i` body, so the interpreter/environment residual requires protection before interpreter startup. [Bash startup behavior](https://www.gnu.org/software/bash/manual/html_node/Bash-Startup-Files.html).

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:159](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:159) Capturing hook configuration does not bind executable bytes: existing project hooks execute worker-worktree `.claude/hooks/contextdb_hook.py` through bare `python3`, and formatting hooks resolve tools through mise shims; restoring `settings.local.json` leaves these unsandboxed execution paths worker-influenced. [Hook authority](https://code.claude.com/docs/en/hooks#security-considerations), [shim resolution](https://mise.jdx.dev/dev-tools/shims.html).

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:80](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:80) The retained launcher grants Codex workers shared `.git/objects` and `.git/refs` writes (`executable_herdr-agents:439`), allowing replacement of `origin/main` after fetch; protecting the working-copy ledger does not bind the committed approval read to the fetched authority.

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:139](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:139) The deny inventory depends on `git ls-tree` without a specified sanitized Git environment or authenticated repository/tree identity; inherited `GIT_DIR`/`GIT_COMMON_DIR` can redirect enumeration, while the named fixture only checks paths from its selected tree. [Git environment controls](https://git-scm.com/docs/git).

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:151](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:151) The claimed orchestrator write route contradicts Claude’s documented enforcement: Edit denies also enter the Bash sandbox configuration, so shared denies covering `.orchestration/**` and `.agents/**` block the promised sandboxed record/cache writes; JSON merge tests cannot establish otherwise. [Combined enforcement](https://code.claude.com/docs/en/sandboxing#how-sandboxing-relates-to-permissions).

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:66](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:66) The boundary is marked closed while the preserved Bash policy has `failIfUnavailable: false`; missing Linux sandbox dependencies therefore permit unsandboxed execution, and no threat row or named test establishes fail-closed sandbox activation. [Startup enforcement](https://code.claude.com/docs/en/sandboxing#enforce-sandboxing-with-managed-settings).

- [P2] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:171](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:171) The executable-boundary closure test covers a PATH shim but never a selected absolute path resolving through symlinks or case aliases into a worker root; it cannot establish §5.14.3’s filesystem-identity requirement on this host, where `.git` and `.GIT` have the same inode.

📝 まとめ: Reviewed every threat row and the related acceptance/review records; findings are for orchestrator disposition. No files changed.

Not checked: implementation tests, live Claude enforcement or deployment; execution and approval binding remain unestablished.
Verdict: incorrect- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:174](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:174) Worker identity depends on mutable event `cwd`: a worker can `cd` outside the worker root and receive the nonworker “no decision” result; identity and allowed roots must remain bound to the launched seat. [Hook cwd semantics](https://code.claude.com/docs/en/hooks#common-input-fields).

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:186](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:186) The existing-hook residual provides no effective mitigation: `.claude/settings.json` executes worker-writable `scripts/agent-stop-gate.sh`, while formatting runs PATH-resolved Prettier against worker-controlled JavaScript configuration; protecting `.claude` settings does not bind the executed code. [Hook execution privileges](https://code.claude.com/docs/en/sandboxing), [Prettier configuration](https://prettier.io/docs/configuration).

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:200](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:200) Absolute Python with `-I` does not neutralize Linux `LD_PRELOAD`: worker-selected native code can execute before Python constructs the clean gh environment; the interpreter/environment row lacks a control and test for this pre-interpreter execution path. [Dynamic-loader behavior](https://man7.org/linux/man-pages/man8/ld.so.8.html).

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:90](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:90) Refusing clone/config argv cannot close outside-sandbox execution: admitted `pr create` invokes Git status and potentially push against the caller-selected repository, without the prescribed Git configuration overrides, permitting repository-configured fsmonitor/hooks execution; fake-gh allowlist tests miss this path. [gh implementation](https://raw.githubusercontent.com/cli/cli/trunk/pkg/cmd/pr/create/create.go), [Git configuration](https://git-scm.com/docs/git-config).

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:86](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:86) Remote-SHA pinning still permits forged approval reads: the retained writable `.git/refs` includes `refs/replace/<sha>`, which redirects `git show <sha>:…`; neither `env -i` nor the prescribed Git flags disable replacement objects. [Git replacement semantics](https://git-scm.com/docs/git-replace).

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:266](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:266) The race residual incorrectly excludes the adversarial worker itself: a sandboxed background child can replace an allowed worktree path after canonical validation, redirecting an unsandboxed file-tool write or gh body-file read; static symlink/case-alias fixtures do not bind validation to consumption.

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:146](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:146) The load-bearing hook lacks a failure-policy threat row and tests for launch failure, crashes and timeout; Claude normally continues after those failures, and `sandbox.failIfUnavailable` protects Bash startup rather than file-tool hook enforcement. [Hook failure behavior](https://code.claude.com/docs/en/hooks#block-the-action-when-a-hook-fails).

📝 まとめ: Reviewed all threat rows and cited acceptance/review context; seven P1 findings remain for orchestrator disposition. No files changed.

Not checked: implementation tests or live enforcement; this text does not establish the proposed execution boundary.
Verdict: incorrect
 succeeded in 162ms:
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
after: [dotfiles-T133-worker-write-boundary-a01]
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
    disposition: "residual: the first document separators bound structured metadata, and whole-file byte comparison protects the complete task copy."
  - control: in-process effects
    disposition: "residual: the hook executes no payload text; tests use temporary state; ruleset helpers use GET access and write only an explicitly selected existing temporary progress ledger on equality."
  - control: workflow and interpreter or environment inputs
    disposition: "residual: the retained env bash shebang and Bash startup precede first-action env -i, so initial launch depends on the orchestrator environment. Codex tool writes are sandbox-confined; Claude file tools, hooks and MCP processes lack that boundary until P1-15, and same-UID processes outside every seat sandbox remain residual. Trusted execution then constructs env -i inputs and a private PATH, excludes caller Git and tool-manager overrides, isolates Python and uses only the private offline uv cache."
  - control: new or renamed scripts
    disposition: "residual: the new deployable inventory is the hook, permission guard, two ruleset helpers and two tracked orchestration entrypoints; RESULT lists all six, and no untracked glue becomes an execution dependency."
  - control: "the sanitized environment (section 5.14 item 2)"
    disposition: "closed: tests/unit/test_gh_merge_gate.py::GhMergeGateTest::test_gate_runs_its_identity_checks_under_a_sanitized_environment"
  - control: the interpreter sanitization order
    disposition: "closed: tests/unit/test_gh_merge_gate.py::GhMergeGateTest::test_gate_sanitizes_before_any_other_command"
  - control: "the identity check of the entrypoint (section 5.14 item 4; updatedInput names the verified anchored realpath and preserves the three arguments, subject to premise 6's runtime-specific residuals)"
    disposition: "closed: tests/unit/test_gh_merge_gate.py::GhMergeGateTest::test_gate_allows_only_through_updated_input_naming_the_verified_realpath"
  - control: "the manifest-rendered worker filesystem write boundary (section 5.14 item 1)"
    disposition: "residual: tests/unit/test_claude_settings_merge.py::test_rendered_worker_sandbox_denies_the_trusted_root_for_bash asserts only Bash sandbox denial; Codex confines all tool writes, while Claude file tools, hooks and MCP processes remain outside Seatbelt with no rendered path deny until P1-15 under D-024-17."
  - control: "the trusted-path write-boundary check (section 5.14 item 3; the hook and entrypoint ask when trusted paths lie under .claude/worktrees/ or a manifest-listed worker worktree)"
    disposition: "closed: tests/unit/test_gh_merge_gate.py::GhMergeGateTest::test_gate_refuses_trusted_paths_under_a_worker_writable_root"
  - control: "the approval provenance boundary (section 5.14 item 8)"
    disposition: "closed: tests/unit/test_permission_guard.py::PermissionGuardTest::test_guard_reads_the_committed_ledger_never_the_working_copy_or_the_pr_tree"
  - control: "the executable provenance boundary"
    disposition: "residual: identity checks, verified realpaths and trusted-path refusal bind checked execution; Codex tool writes are confined, while Claude file tools, hooks and MCP processes retain the P1-15 path-deny gap and a same-UID process outside every seat sandbox remains residual."
  - control: "the Git configuration inputs"
    disposition: "closed: tests/unit/test_gh_merge_gate.py::GhMergeGateTest::test_gate_git_ignores_planted_hooks_fsmonitor_and_global_config"
  - control: "the snapshot rule (the entrypoint creates the snapshot directory under the anchored checkout's gitignored .agents/worklog/snapshots/ at mode 0700, writes the snapshot once and compares its SHA256 again immediately before gh)"
    disposition: "closed: tests/unit/test_integrate_merge.py::IntegrateMergeTest::test_finish_pr_reverifies_the_snapshot_before_gh"
  - control: the snapshot write boundary
    disposition: "residual: the last SHA256 comparison refuses a detected change and Codex confines tool writes; mode 0700 does not exclude the same UID, Claude file tools, hooks and MCP processes retain the P1-15 path-deny gap, and a same-UID process outside every seat sandbox can race the final comparison and gh's read."
  - control: "the worker sandbox exclusions (section 5.14 item 10)"
    disposition: "residual: Worker Playbook step 4 sends gh outside the sandbox through the permission gate with no present mitigation for this exclusion; P1-15 owns the pending D-024-17 wrapper using env -i, an absolute trusted gh and a fixed alias-free read-only GH_CONFIG_DIR."
  - control: "the output and reservation identity (section 5.14 item 5)"
    disposition: "residual: new snapshot names carry the full 40-hex head, the content digest and a unique suffix; legacy gate evidence retains its existing filename contract and binds the full head in its contents, and this task introduces no reservation or slot lock."
  - control: "the honest residuals (section 5.14 item 6)"
    disposition: "residual: the report preserves the Claude-seat path-deny gap owned by P1-15, the unmitigated outside-sandbox gh exclusion and the same-UID process risk, and labels none closed."
  - control: "the shared trusted-execution regressions (section 5.14 item 7)"
    disposition: "residual: the required red-then-green fixtures cover caller shims, planted Git inputs, worker-root trusted paths and a source swap after validation; the report records their exact selectors and outputs, and P1-6 owns the future shared helper."
  - control: "the private offline uv cache (section 5.14 item 9)"
    disposition: "closed: tests/unit/test_integrate_merge.py::IntegrateMergeTest::test_integrate_merge_uses_the_private_uv_cache_only"
  - control: orchestrator effect merge
    disposition: "residual: only the trusted entrypoint performs the squash merge, after final-head evidence and API checks, with --match-head-commit binding the merged head; no task branch is merged locally or pushed to main."
  - control: "orchestrator effect PR creation and publication (finish-pr.sh publishes only a snapshot it wrote from validated bytes and reverified, retains the draft flag and applies the records-only check)"
    disposition: "closed: tests/unit/test_integrate_merge.py::IntegrateMergeTest::test_finish_pr_preserves_draft_and_records_only_publication_controls"
  - control: "orchestrator effect fetch, checkout and fast-forward (fetch of origin/main only, fast-forward only, refusal of modified tracked files outside .orchestration and preservation of untracked records)"
    disposition: "closed: tests/unit/test_integrate_merge.py::IntegrateMergeTest::test_integrate_merge_fetches_only_origin_main_and_preserves_local_records"
  - control: orchestrator effect update-branch
    disposition: "residual: direct gh update-branch text asks, and any resulting head receives fresh CI, feedback, audit and security evidence before the integration gate."
  - control: orchestrator effect forced worker removal
    disposition: "residual: no forced removal is planned; the existing dirty-worktree rule applies and the acceptance record identifies any discarded uncommitted state."
premises:
  - claim: none of the five new files exists on origin/main
    command: git ls-files scripts/permission-guard.py scripts/orchestrator/ruleset-request.sh scripts/orchestrator/ruleset-verify.sh home/dot_claude/hooks/executable_gh-merge-gate.sh tests/unit/test_gh_merge_gate.py | wc -l
    output: |-
      0
  - claim: PR #400's branch, the material this task rebuilds from, is at the head the T131 review assessed
    command: git rev-parse origin/fix/claude-pinned-merge-gate
    output: |-
      0b874adb9850ff9647fbc039ec3cf6cc30487488
  - claim: the tracked git config still rewrites GitHub pushes to SSH while the live config (hand-edited) does not, the mismatch D3 (d) resolves
    command: /usr/bin/grep -c 'pushinsteadof = https://github.com/' home/dot_config/git/config.tmpl
    output: |-
      1
  - claim: the manifest still asks for gh pr merge, the rule the hook replaces
    command: /usr/bin/grep -c 'Bash(gh pr merge:\*)' home/dot_agents/agent-config.yaml
    output: |-
      1
  - claim: decisions.tsv carries no permission-scoped decision row yet, so the guard's first run on this PR itself must find the row this task adds
    command: /usr/bin/grep -c 'scope=permission' .orchestration/decisions.tsv
    output: |-
      0
  - claim: >-
      section 5.14 item 1 applies per runtime: a Codex seat's sandbox confines all tool writes to its worktree and enumerated writable paths; a Claude seat's Seatbelt sandbox confines Bash only, while Write/Edit/MultiEdit/NotebookEdit, hooks and MCP processes run outside it and the rendered permission policy has no path deny today. The Claude-seat boundary is residual until P1-15 under D-024-17 adds the permgate path deny. The Bash render test asserts only that sandbox's scope. Approval provenance instead uses the committed origin/main ledger after fetch under D-024-19. Worker Playbook step 4's outside-sandbox gh has no present mitigation and is owned by P1-15, whose pending wrapper uses env -i, an absolute gh and a fixed alias-free read-only GH_CONFIG_DIR. A same-UID process outside every seat sandbox remains residual.
    sources:
      - home/dot_agents/agent-config.yaml
      - home/.chezmoitemplates/claude-settings-managed.json
    verification: tests/unit/test_claude_settings_merge.py::test_rendered_worker_sandbox_denies_the_trusted_root_for_bash
---
      - Bash(gh api -X DELETE:*)
      - Bash(gh api --method DELETE:*)
      - Bash(gh api -XDELETE:*)
      - Bash(gh api --method=DELETE:*)
      - Bash(gh api -f:*)
      - Bash(gh api -F:*)
      - Bash(gh api --raw-field:*)
      - Bash(gh api --field:*)
      - Bash(gh api -f*)
      - Bash(gh api -F*)
      - Bash(gh api --raw-field=*)
      - Bash(gh api --field=*)
  env:
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
        - uploads.github.com
        - objects.githubusercontent.com
        - codeload.github.com
        - pypi.org
        - files.pythonhosted.org
      # macOS certificate validation; the generator omits Mach services on Linux.
      allowMachLookup:
        - com.apple.trustd.agent
      # macOS only: Claude Code ignores this list on Linux and WSL2, where the
      # seccomp filter can't inspect socket paths. The Claude messaging socket
      # (CLAUDE_CODE_MESSAGING_SOCKET, a per-process path set at runtime) cannot
      # be listed without a glob, so it is not.
      allowUnixSockets:
        - ~/.config/herdr/herdr.sock
      # The allow-all Unix socket switch is deliberately not set: with a
      # docker-group user or a reachable `systemd --user` bus it turns the
      # auto-approved sandbox into an escape (T44 r2, operator 2026-10-01).
  hooks:
    enforce_uv_hook: ~/.claude/hooks/enforce-uv.sh
    format_edited_files_hook: ~/.claude/hooks/format-edited-files.py
    project_map_reload_hook: ~/.claude/hooks/project-map-reload.sh
    permission_request:
      command: ~/.local/bin/common/permgate claude
      timeout: 10
      status_message: Evaluating permission request
    session_start:
      - matcher: "^(startup|resume|clear|compact|fork)$"
        hooks:
          - type: command
            # Must stay byte-identical to herdr's own SessionStart entry after
            # template expansion; herdr integration install no-ops on exact match
            # and would otherwise append a duplicate on every `make update`.
            command: "bash '{{ .chezmoi.homeDir }}/.claude/hooks/herdr-agent-state.sh' session"
            timeout: 10
      - matcher: "*"
        hooks:
          - type: command
            command: "{{ .chezmoi.homeDir }}/.local/bin/common/agent-session-staleness hook"
            async: true
            timeout: 5
  statusLine:
    type: command
    command: ccstatusline

{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python3",
            "args": [
              "${CLAUDE_PROJECT_DIR}/.claude/hooks/contextdb_hook.py"
            ],
            "async": true,
            "timeout": 30
          }
        ]
      },
      {
        "matcher": "compact",
        "hooks": [
          {
            "type": "command",
            "command": "python3",
            "args": [
              "${CLAUDE_PROJECT_DIR}/.claude/hooks/contextdb_recover.py"
            ],
            "timeout": 15
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3",
            "args": [
              "${CLAUDE_PROJECT_DIR}/.claude/hooks/contextdb_hook.py"
            ],
            "async": true,
            "timeout": 30
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python3",
            "args": [
              "${CLAUDE_PROJECT_DIR}/.claude/hooks/contextdb_hook.py"
            ],
            "async": true,
            "timeout": 30
          }
        ]
      }
    ],
    "PostToolUseFailure": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python3",
            "args": [
              "${CLAUDE_PROJECT_DIR}/.claude/hooks/contextdb_hook.py"
            ],
            "async": true,
            "timeout": 30
          }
        ]
      }
    ],
    "PermissionDenied": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python3",
            "args": [
              "${CLAUDE_PROJECT_DIR}/.claude/hooks/contextdb_hook.py"
            ],
            "async": true,
            "timeout": 30
          }
        ]
      }
    ],
    "PreCompact": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python3",
            "args": [
              "${CLAUDE_PROJECT_DIR}/.claude/hooks/contextdb_hook.py"
            ],
            "timeout": 10
          }
        ]
      }
    ],
    "PostCompact": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python3",
            "args": [
              "${CLAUDE_PROJECT_DIR}/.claude/hooks/contextdb_hook.py"
            ],
            "timeout": 10
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3",
            "args": [
              "${CLAUDE_PROJECT_DIR}/.claude/hooks/contextdb_hook.py"
            ],
            "async": true,
            "timeout": 30
          }
        ]
      },
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash",
            "args": [
              "${CLAUDE_PROJECT_DIR}/scripts/agent-stop-gate.sh"
            ],
            "timeout": 5
          }
        ]
      }
    ],
    "StopFailure": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3",
            "args": [
              "${CLAUDE_PROJECT_DIR}/.claude/hooks/contextdb_hook.py"
            ],
            "async": true,
            "timeout": 30
          }
        ]
      }
    ],
    "SubagentStop": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python3",
            "args": [
              "${CLAUDE_PROJECT_DIR}/.claude/hooks/contextdb_hook.py"
            ],
            "async": true,
            "timeout": 30
          }
        ]
      }
    ],
    "SessionEnd": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python3",
            "args": [
              "${CLAUDE_PROJECT_DIR}/.claude/hooks/contextdb_hook.py"
            ],
            "timeout": 10
          }
        ]
      }
    ],
    "SubagentStart": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python3",
            "args": [
              "${CLAUDE_PROJECT_DIR}/.claude/hooks/contextdb_hook.py"
            ],
            "async": true,
            "timeout": 30
          }
        ]
      }
    ],
    "TaskCreated": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3",
            "args": [
              "${CLAUDE_PROJECT_DIR}/.claude/hooks/contextdb_hook.py"
            ],
            "async": true,
            "timeout": 30
          }
        ]
      }
    ],
    "TaskCompleted": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3",
            "args": [
              "${CLAUDE_PROJECT_DIR}/.claude/hooks/contextdb_hook.py"
            ],
            "async": true,
            "timeout": 30
          }
        ]
      }
    ]
  }
}

web search: https://code.claude.com/docs/en/permissions
**Handling project environment constraints**
**Verifying .agents directory tracking**
exec
/bin/zsh -lc "sed -n '109,145p' .orchestration/plans/024-design-quality.md; git ls-tree --name-only HEAD; git rev-parse HEAD; git diff --name-only 940a3a2b07adfd14140a0acff96784ef53a0a509..HEAD -- ':"'!.ua'"' ':"'!.orchestration'"' | head -25" in ~/Workspace/dotfiles
 succeeded in 52ms:
0. **脅威モデル（D-024-21）** 席は同じ OS ユーザで動き、ホストは席間の信頼境界ではない（同一 UID のプロセスは symlink 差し替え、共有 `.git` の object 差し替え、hook の子プロセス、Herdr socket 経由の host 実行で、ホスト内のどの検査も迂回できる）。regime の硬い境界は GitHub（保護された main、必須チェック、orchestrator の identity によるマージ）。悪意ある worker に耐えるべき入力（承認台帳、gate が読む証跡 of record）は GitHub から sha 指定で API 経由（sandbox 内）に読み、ローカルファイルやローカル object database からは読まない。ホスト内の制御（本節 1〜10）は事故と prompt injection による損害の抑制であり、文はそう書く。
8. **承認はコミット済み台帳から読む** permission の決定行（`scope=permission approved_by=user diff_sha256=…`）は anchored checkout の作業コピーではなく、コミット済みの台帳から読む。読み方は `git ls-remote origin refs/heads/main` が返す commit sha を取り、GitHub API（`gh api repos/<owner>/<repo>/contents/.orchestration/decisions.tsv?ref=<sha>`、sandbox 内）でその sha の内容を取得する。ローカルの `git show` は共有 object database が書けるため中間 tree の差し替えで偽物を返しうる（第 3 回審査の所見 2）（ローカルの ref 名 `origin/main` は経由しない。`refs/replace/` も書けるので replacement を無効にする。Codex worker は `.git/objects` と `.git/refs` に書けるので ref は差し替えられるが、sha で指した object は内容アドレスで偽造できない）。作業コピーの行は提案で、記録 PR が main にマージされて初めて承認になる（PR の承認は操作者の操作）。偽造には main へのマージが要る。
9. **私設キャッシュ** orchestrator 側の実行は worker と共有するキャッシュ（`~/.cache/uv`、`~/.local/share/uv`、mise）から実行可能物を読まない。`UV_CACHE_DIR` を anchored checkout 配下（`.agents/worklog/uv-cache`、gitignored、worker 書き込み不可）に固定し、`--offline` で使う。hook は uv を使わず jq と python 標準ライブラリだけで動く。
10. **worker は sandbox 外でコマンドを実行しない（D-024-17 の改訂）** 2026-10-19T03:45Z の実測で `gh api` は Claude sandbox の中から成功した（sandbox の proxy は CONNECT 型で TLS を終端しない；keychain のトークンも読めた）。worker 席の除外コマンドは空にし、gh も git push も sandbox 内の proxy 経由で実行する。Codex 席は `sandbox_workspace_write.network_access = true` で同じ状態にし、permgate の codex ポリシーは sandbox 外への escape を承認しない（permgate の変更は操作者の手順）。wrapper 方式（絶対パス、env -i、固定 GH_CONFIG_DIR）は LD_PRELOAD と引数転送（`gh repo clone -- --config`）を閉じられないので採らない。
7. **検証** threat_table は本節の項目 1〜10 に 1 行ずつ対応させる（参照だけでは足りない）。共通テスト補助 `tests/unit/trusted_exec_contract.py`（P1-6 で作る）を使い、仕組みごとに 4 つの red→green テストを持つ：PATH 先頭の shim が実行されない、植え付けた GIT_* と git 設定が効かない、worker ルート配下の信頼パスが拒否される、検証後に差し替えたファイルが消費側に届かない。
.chezmoiroot
.claude
.coderabbit.yaml
.editorconfig
.github
.gitignore
.orchestration
.prettierignore
.simplecov
.ua
AGENTS.md
CLAUDE.md
Dockerfile
LICENSE
Makefile
README.md
codecov.yml
docs
home
install
mise.toml
mkdocs.yml
plans
renovate.json
ruff.toml
scripts
setup.sh
tests
vendor
b22a5580d0778e57a66d3f75c76e3c55b88701e1
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
.prettierignore
AGENTS.md
CLAUDE.md
Dockerfile

exec
/bin/zsh -lc "sed -n '1,150p' ~/.agents/skills/agmsg/scripts/session-start.sh; sed -n '1,150p' ~/.agents/skills/agmsg/scripts/check-inbox.sh" in ~/Workspace/dotfiles
 succeeded in 0ms:
#!/usr/bin/env bash
set -euo pipefail
# shellcheck disable=SC1091
source "$(cd "$(dirname "$0")" && pwd)/lib/compat.sh"

# SessionStart hook for delivery modes `monitor` and `both`.
#
# Usage: session-start.sh <type> <project_path>
#
# Reads the hook input JSON from stdin to extract the session_id, then emits
# an instruction telling Claude to invoke the Monitor tool against watch.sh.
# The hook input includes session_id for SessionStart events.
#
# Before emitting the directive, this script also takes care of preventing
# duplicate watchers across `/clear` (and similar) re-fires of SessionStart
# within the same Claude Code instance. State is kept in
# `~/.agents/agmsg/run/cc-instance.<cc_pid>`, which records the last
# session_id this CC instance attached to. On each fire we kill the watcher
# for the previous session_id, then record the new one. Multiple CC
# instances of the same project get their own cc_pid, so they never step
# on each other.
#
# Quietly exits 0 when whoami says the agent isn't joined to anything yet.
# Mode is implicit: if this script is being invoked at all, it's because
# `delivery.sh set monitor` (or `both`) installed it in the project's
# settings.local.json — that fact alone is the source of truth for "should
# we emit the directive?". No separate global mode value to consult.

TYPE="${1:?Usage: session-start.sh <type> <project_path>}"
PROJECT="${2:?Missing project_path}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
RUN_DIR="$SKILL_DIR/run"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/lib/actas-lock.sh"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/lib/registry-lock.sh"  # publish cc-instance only after a complete write
# shellcheck disable=SC1091
source "$SCRIPT_DIR/lib/resolve-project.sh"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/lib/node.sh"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/lib/hash.sh"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/lib/storage.sh"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/lib/type-registry.sh"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/lib/role-session.sh"  # role->session reverse lookup (#339)
# Only DEFINES agmsg_close_inherited_fds; nothing is closed here. The type
# plug calls it inside a subshell around its own long-lived spawn, so this
# shell's descriptors are untouched. See lib/close-fds.sh.
source "$SCRIPT_DIR/lib/close-fds.sh"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/lib/terminal-context-line.sh"

# Identity sanity check — no point launching a watcher with an empty pair set.
PAIRS=$("$SCRIPT_DIR/identities.sh" "$PROJECT" "$TYPE" 2>/dev/null || true)
[ -n "$PAIRS" ] || exit 0

# Read hook input JSON from stdin BEFORE the type plug below runs (#1468):
# stdin can only be read once, and a plug that needs a hook input field (e.g.
# codex reading `source` to tell startup/resume/clear apart) has to see it
# while it is still there. No plug reads it yet, so this move is order-only —
# nothing downstream changes behavior. The session id field name differs by
# vendor: Claude Code emits snake_case "session_id"; Grok Build (and Cursor)
# emit camelCase "sessionId". Try snake first (claude-code unaffected), then
# camel, then the GROK_SESSION_ID env Grok injects into every hook.
INPUT=$(cat 2>/dev/null || true)
SESSION_ID=""
if [ -n "$INPUT" ]; then
  SESSION_ID=$(printf '%s' "$INPUT" \
    | sed -n 's/.*"session_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' \
    | head -1)
  [ -z "$SESSION_ID" ] && SESSION_ID=$(printf '%s' "$INPUT" \
    | sed -n 's/.*"sessionId"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' \
    | head -1)
fi
[ -z "$SESSION_ID" ] && SESSION_ID="${GROK_SESSION_ID:-}"
# Fallback so the instruction is still actionable even outside a hook flow.
[ -z "$SESSION_ID" ] && SESSION_ID="unknown-$$"

# Type-specific SessionStart behaviour (Template Method). A type may ship
# scripts/drivers/types/<type>/_session-start.sh defining agmsg_session_start to override the
# default no-op — codex uses it to hand the session off to the bridge. The plug
# is sourced in this script's context so it sees PROJECT / RUN_DIR / SKILL_DIR /
# PAIRS / INPUT / SESSION_ID and the helpers sourced above; it may exit 0
# (codex does, having no Monitor tool) to skip the Monitor-directive path below.
agmsg_session_start_default() { :; }

_tdir="$(agmsg_type_dir "$TYPE" 2>/dev/null || true)"
if [ -n "$_tdir" ] && [ -f "$_tdir/_session-start.sh" ]; then
  # shellcheck disable=SC1090
  . "$_tdir/_session-start.sh"
  agmsg_session_start
else
  agmsg_session_start_default
fi

# One where.sh call, rendered once, reused by every text-emitting exit below —
# so a session always learns its own terminal driver and capabilities as the
# FIRST thing in its context, before any Monitor-tool instruction, rather than
# having to guess from env vars/grep the way #1171's incident agent did.
TERMINAL_LINE="$(agmsg_terminal_context_line "$SESSION_ID" "$SKILL_DIR" 2>/dev/null || true)"
[ -n "$TERMINAL_LINE" ] || TERMINAL_LINE="AGMSG terminal: could not be determined (agmsg_terminal_context_line produced no output)"

# Companion to TERMINAL_LINE: that line is this session's OWN placement;
# teammates' placement is team.sh's question, not this hook's to compute and
# print stale — a teammate can move between this session start and the moment
# the reader acts on it. So this points at the live command rather than a
# snapshotted answer. Deliberately does not claim team.sh's output already
# states per-teammate peek/poke/arrange reachability -- as of this line, it
# does not (that display is tracked separately); wording this makes true only
# what team.sh actually shows today.
TEAM_LINE="AGMSG team.sh <team>: shows every teammate's placement and status. To act on one, run peek.sh/poke.sh/arrange.sh <team> <name> directly — its exit code says whether it worked and why not (see each driver's own SKILL.md), so there is no need to guess reachability first."

# --- Skip spawned worktree sub-sessions (.claude/worktrees checkouts). ---
# Claude Code's background-task feature runs a short-lived sub-session in an
# isolated worktree under .claude/worktrees/<name>. SessionStart still fires
# there (#92's resolve-project normalizes its cwd back to the registered
# project, so identities resolve fine), so a persistent inbox watcher was
# getting launched for it too — but that watcher keeps the sub-session's
# Monitor alive past the point its task finishes, so the parent session never
# receives the sub-session's completion notification (#367). The sub-session
# is also not normally an agmsg team member in its own right, so a watcher
# has little value there anyway. cwd may arrive as forward slashes or
# JSON-escaped backslashes depending on platform (a single escaped backslash
# decodes to two raw '\' bytes in the captured substring), so normalize both
# to '/' and squeeze doubled separators before matching. Match the exact
# ".claude/worktrees" PATH SEGMENT sequence, not a loose substring — a naive
# `*.claude*worktrees*` glob would also skip an unrelated project merely
# named e.g. ".claude-tools/my-worktrees-app".
HOOK_CWD=""
if [ -n "$INPUT" ]; then
  HOOK_CWD=$(printf '%s' "$INPUT" \
    | sed -n 's/.*"cwd"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' \
    | head -1)
fi
[ -z "$HOOK_CWD" ] && HOOK_CWD="${PWD:-}"
HOOK_CWD_NORM=$(printf '%s' "$HOOK_CWD" | tr '\\' '/' | sed 's#//*#/#g')
case "$HOOK_CWD_NORM" in
  */.claude/worktrees|*/.claude/worktrees/*|.claude/worktrees|.claude/worktrees/*) exit 0 ;;
esac

mkdir -p "$RUN_DIR" 2>/dev/null || true

# --- Identify the enclosing Claude Code process. ---
# Reuse the shared agent-process resolver (#92) instead of a local ps-walk: it
# checks both the `comm` name and argv[0] basename against the type's binaries,
#!/usr/bin/env bash
set -euo pipefail
# shellcheck disable=SC1091
source "$(cd "$(dirname "$0")" && pwd)/lib/compat.sh"

# Check inbox across all teams with cooldown. Skips if last check was < 60 seconds ago.
# Usage: check-inbox.sh <type> <project_path>

TYPE="${1:?Usage: check-inbox.sh <type> <project_path>}"
PROJECT="${2:?Missing project_path}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
source "$SCRIPT_DIR/lib/storage.sh"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/lib/actas-lock.sh"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/lib/resolve-project.sh"  # agmsg_agent_pid, for instance-id derivation
# shellcheck disable=SC1091
source "$SCRIPT_DIR/lib/type-registry.sh"

# Which hook event fired. The Stop entry runs `check-inbox.sh <type> <project>`
# (EVENT defaults to Stop); the mid-turn PostToolUse entry (#1003) appends the
# event as a 3rd arg so this script emits the shape that event's runtime accepts,
# without branching on the type name.
EVENT="${3:-Stop}"

# Some Stop-hook runtimes (codex, copilot) want an explicit JSON status object
# even when there is nothing to deliver; others (claude-code) stay silent. This
# is the type's manifest `stop_output=` (data), not a hardcoded type list.
STOP_OUTPUT="$(agmsg_type_get "$TYPE" stop_output 2>/dev/null || true)"
# The wire shape for a PostToolUse payload, from the type manifest (#1003) — the
# same data-driven approach as stop_output. Measured on codex-cli 0.149.1:
# hookSpecificOutput. An unknown/unset value emits nothing rather than a guess.
POSTTOOL_OUTPUT="$(agmsg_type_get "$TYPE" posttooluse_output 2>/dev/null || true)"

# Status (nothing-to-deliver / cooldown) output. For PostToolUse this stays
# SILENT: codex 0.149.1 treats malformed post-tool-use JSON as a failure, and an
# empty additionalContext on every tool call would be pure noise — so a no-op
# turn emits no bytes, which every runtime reads as "hook did nothing".
# Status of the write that hands a payload over. Declared before the first emit
# (the cooldown one) so EVERY emit in this file reports through the same
# variable: "each emit says whether it worked" is checkable, while "the emits
# that can carry a message are guarded" needs the next reader to work out which
# ones those are -- and that is how one of three ends up unguarded.
EMIT_RC=0
emit_status_json() {
  [ "$EVENT" = "PostToolUse" ] && return 0
  [ "$STOP_OUTPUT" = "json" ] || return 0
  printf '{\n  "continue": true,\n  "systemMessage": "%s"\n}\n' "$1" || EMIT_RC=$?
}

# Hook runtimes that pass JSON do so on stdin. Interactive invocations such as
# Gemini's PostToolUse command may inherit a terminal stdin instead; reading
# unconditionally there blocks waiting for input. The `[ ! -t 0 ]` guard just below
# only rules out that TTY case -- a non-TTY stdin whose write end is left
# open (a hook runtime that writes the payload and then simply never closes
# the pipe) still leaves this `cat` waiting for an EOF that never arrives.
# Stop/turn hooks run synchronously, so a `cat` stuck here freezes the whole
# agent pane until the user kills it. Bound the read; a runtime that forgets
# to close its pipe still gets its payload delivered (it's already sitting in
# the command substitution buffer by the time the deadline fires), just a few
# seconds late instead of never. Fails open when `timeout` isn't on PATH
# (stock macOS) -- same unbounded read as before, no regression there. #381
INPUT=""
if [ ! -t 0 ]; then
  if command -v timeout >/dev/null 2>&1; then
    INPUT=$(timeout "${AGMSG_HOOK_STDIN_TIMEOUT:-2}" cat 2>/dev/null || true)
  else
    INPUT=$(cat 2>/dev/null || true)
  fi
fi

# Prevent infinite loop: if stop hook is already active, exit silently
if echo "$INPUT" | grep -q '"stop_hook_active"[[:space:]]*:[[:space:]]*true' 2>/dev/null; then
  exit 0
fi

# The session id is still resolved: the actas-ownership check further down
# needs it. Only the deferral that used to follow it is gone. The field name
# differs by vendor: Claude Code emits snake_case "session_id"; Grok Build (and
# Cursor) emit camelCase "sessionId". Try snake first (claude-code unaffected),
# then camel, then the GROK_SESSION_ID env Grok injects into every hook.
SESSION_ID=$(printf '%s' "$INPUT" \
  | sed -n 's/.*"session_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' \
  | head -1)
[ -z "$SESSION_ID" ] && SESSION_ID=$(printf '%s' "$INPUT" \
  | sed -n 's/.*"sessionId"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' \
  | head -1)
[ -z "$SESSION_ID" ] && SESSION_ID="${GROK_SESSION_ID:-}"
# Normalized to the per-process instance id (#93), which is the token the
# actas owner file is keyed on.
[ -n "$SESSION_ID" ] && SESSION_ID="$(agmsg_normalize_instance_id "$SESSION_ID" "$TYPE")"

# No deferral to a live watcher (#694).
#
# This used to exit here whenever a watcher process was alive for this session,
# to avoid double delivery in `both` mode. The condition was LIVENESS, and the
# failure `both` exists for preserves liveness exactly: a watcher that is alive
# and delivering nothing. So the one mode advertised as a safety net stood down
# in front of the one situation it was wanted for. On 2026-08-08 a session with
# a broken watcher was switched to `both` to recover delivery and nothing
# changed; what worked was `mode turn`, which stops the watcher, which removes
# the liveness signal, which lets this hook run.
#
# Removing it does not double-deliver, and that is measured rather than
# assumed. Both sides consume through the same state:
#
#   watcher      storage_read_cursor_consume -> inserts a `message_read` event
#                per delivered id AND advances read_cursors.local_position
#   this hook    storage_list_unread -> excludes rows at or below that cursor
#                AND rows with a `message_read` event
#
# So a message the watcher has emitted is not offered here. The remaining
# window is an interleave: this hook SELECTs, the watcher emits and consumes
# the same row, then this hook marks it read. Bounded by one poll interval, and
# the trade is explicit -- a rare duplicate line against a mode that silently
# delivered nothing at all.
#
# Deferral was an optimisation, not a correctness requirement. The read state
# is the correctness requirement, and it was already there.

# Resolve the invocation path to the registered project root (session marker /
# nearest ancestor / sibling worktree) before the identity lookup — the
# whoami.sh path did this resolution, and identities.sh itself is an exact
# registry lookup by design (its other callers rely on that).
PROJECT="$(agmsg_resolve_project "$PROJECT" "$TYPE")"

# Consume exact (team, agent) TSV rows instead of independently flattened
# agent/team lists. For multiple agents, preserve the existing first-agent
# policy, but subscribe only to that agent's actual team rows.
IDENTITIES=$("$SCRIPT_DIR/identities.sh" "$PROJECT" "$TYPE")
[ -n "$IDENTITIES" ] || exit 0

AGENT=""
TEAM_LIST=()
IDENTITIES_VALID=1
while IFS=$'\t' read -r identity_team identity_agent identity_extra; do
  if [ -z "$identity_team" ] || [ -z "$identity_agent" ] || [ -n "$identity_extra" ]; then
    IDENTITIES_VALID=0
    break
  fi

  [ -n "$AGENT" ] || AGENT="$identity_agent"
  [ "$identity_agent" = "$AGENT" ] || continue

  team_seen=0
  # ${arr[@]+...} guards the empty-array expansion: under `set -u` bash 3.2
  # (macOS default) treats "${TEAM_LIST[@]}" on an empty array as unbound.
  for selected_team in ${TEAM_LIST[@]+"${TEAM_LIST[@]}"}; do

web search: 
web search: 'Symlinks'
**Analyzing Git remote security**
**Investigating Git config and environment risks**
codex
今回の改訂は、前回指摘のローカル台帳読み取り、Herdr socket、hook 失敗時の扱いを変更しています。残る確認点は、deny 対象を列挙する Git データ自体の信頼性、gitignored な orchestrator cache の保護、外部 agmsg スクリプトの子プロセスまで interpreter を固定できるかです。

web search: 
exec
/bin/zsh -lc "cat .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-8bac9e5.md.last.md; cat .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-67415f5.md.last.md; sed -n '99,109p' .orchestration/plans/024-design-quality.md" in ~/Workspace/dotfiles
exec
/bin/zsh -lc "rg -n 'bash|python|node|SCRIPT_DIR|type_dir' ~/.agents/skills/agmsg/scripts/identities.sh ~/.agents/skills/agmsg/scripts/lib/type-registry.sh ~/.agents/skills/agmsg/scripts/lib/node.sh; rg -n 'delivery|hooks|CLAUDE_CONFIG_DIR|sandbox|writable_roots|AGMSG_|worktree.*claude' home/dot_local/bin/common/executable_herdr-agents | head -100; rg -n '\\.agents|worklog' .gitignore" in ~/Workspace/dotfiles
 succeeded in 95ms:
- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:169](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:169) Verbatim argv forwarding permits `gh repo clone … -- --config core.sshCommand=<worker executable>` to execute worker code outside the Linux sandbox; fixed binaries and alias-free configuration do not close this path, and the named alias test never exercises it. [gh forwarding](https://cli.github.com/manual/gh_repo_clone), [Git configuration timing](https://git-scm.com/docs/git-clone).

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:163](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:163) An absolute noninteractive interpreter does not suppress Bash’s `BASH_ENV`; a read-only host probe printed the injected startup marker before the `env -i` body, so the interpreter/environment residual requires protection before interpreter startup. [Bash startup behavior](https://www.gnu.org/software/bash/manual/html_node/Bash-Startup-Files.html).

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:159](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:159) Capturing hook configuration does not bind executable bytes: existing project hooks execute worker-worktree `.claude/hooks/contextdb_hook.py` through bare `python3`, and formatting hooks resolve tools through mise shims; restoring `settings.local.json` leaves these unsandboxed execution paths worker-influenced. [Hook authority](https://code.claude.com/docs/en/hooks#security-considerations), [shim resolution](https://mise.jdx.dev/dev-tools/shims.html).

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:80](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:80) The retained launcher grants Codex workers shared `.git/objects` and `.git/refs` writes (`executable_herdr-agents:439`), allowing replacement of `origin/main` after fetch; protecting the working-copy ledger does not bind the committed approval read to the fetched authority.

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:139](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:139) The deny inventory depends on `git ls-tree` without a specified sanitized Git environment or authenticated repository/tree identity; inherited `GIT_DIR`/`GIT_COMMON_DIR` can redirect enumeration, while the named fixture only checks paths from its selected tree. [Git environment controls](https://git-scm.com/docs/git).

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:151](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:151) The claimed orchestrator write route contradicts Claude’s documented enforcement: Edit denies also enter the Bash sandbox configuration, so shared denies covering `.orchestration/**` and `.agents/**` block the promised sandboxed record/cache writes; JSON merge tests cannot establish otherwise. [Combined enforcement](https://code.claude.com/docs/en/sandboxing#how-sandboxing-relates-to-permissions).

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:66](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:66) The boundary is marked closed while the preserved Bash policy has `failIfUnavailable: false`; missing Linux sandbox dependencies therefore permit unsandboxed execution, and no threat row or named test establishes fail-closed sandbox activation. [Startup enforcement](https://code.claude.com/docs/en/sandboxing#enforce-sandboxing-with-managed-settings).

- [P2] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:171](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:171) The executable-boundary closure test covers a PATH shim but never a selected absolute path resolving through symlinks or case aliases into a worker root; it cannot establish §5.14.3’s filesystem-identity requirement on this host, where `.git` and `.GIT` have the same inode.

📝 まとめ: Reviewed every threat row and the related acceptance/review records; findings are for orchestrator disposition. No files changed.

Not checked: implementation tests, live Claude enforcement or deployment; execution and approval binding remain unestablished.
Verdict: incorrect- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:174](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:174) Worker identity depends on mutable event `cwd`: a worker can `cd` outside the worker root and receive the nonworker “no decision” result; identity and allowed roots must remain bound to the launched seat. [Hook cwd semantics](https://code.claude.com/docs/en/hooks#common-input-fields).

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:186](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:186) The existing-hook residual provides no effective mitigation: `.claude/settings.json` executes worker-writable `scripts/agent-stop-gate.sh`, while formatting runs PATH-resolved Prettier against worker-controlled JavaScript configuration; protecting `.claude` settings does not bind the executed code. [Hook execution privileges](https://code.claude.com/docs/en/sandboxing), [Prettier configuration](https://prettier.io/docs/configuration).

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:200](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:200) Absolute Python with `-I` does not neutralize Linux `LD_PRELOAD`: worker-selected native code can execute before Python constructs the clean gh environment; the interpreter/environment row lacks a control and test for this pre-interpreter execution path. [Dynamic-loader behavior](https://man7.org/linux/man-pages/man8/ld.so.8.html).

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:90](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:90) Refusing clone/config argv cannot close outside-sandbox execution: admitted `pr create` invokes Git status and potentially push against the caller-selected repository, without the prescribed Git configuration overrides, permitting repository-configured fsmonitor/hooks execution; fake-gh allowlist tests miss this path. [gh implementation](https://raw.githubusercontent.com/cli/cli/trunk/pkg/cmd/pr/create/create.go), [Git configuration](https://git-scm.com/docs/git-config).

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:86](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:86) Remote-SHA pinning still permits forged approval reads: the retained writable `.git/refs` includes `refs/replace/<sha>`, which redirects `git show <sha>:…`; neither `env -i` nor the prescribed Git flags disable replacement objects. [Git replacement semantics](https://git-scm.com/docs/git-replace).

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:266](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:266) The race residual incorrectly excludes the adversarial worker itself: a sandboxed background child can replace an allowed worktree path after canonical validation, redirecting an unsandboxed file-tool write or gh body-file read; static symlink/case-alias fixtures do not bind validation to consumption.

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:146](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:146) The load-bearing hook lacks a failure-policy threat row and tests for launch failure, crashes and timeout; Claude normally continues after those failures, and `sandbox.failIfUnavailable` protects Bash startup rather than file-tool hook enforcement. [Hook failure behavior](https://code.claude.com/docs/en/hooks#block-the-action-when-a-hook-fails).

📝 まとめ: Reviewed all threat rows and cited acceptance/review context; seven P1 findings remain for orchestrator disposition. No files changed.

Not checked: implementation tests or live enforcement; this text does not establish the proposed execution boundary.
Verdict: incorrect## 5.14 信頼ホスト実行契約（trusted-host execution contract、D-024-18）

orchestrator 側の仕組み（merge gate、integrate-merge、orch-gate、dispositions、audit-pool、verdict、chain）は、同じホスト上で同じ UID の worker プロセスと共存する。2026-10-19 の C-80 審査（a05、dispositions-a02、audit-pool-a01 の 3 文、計 19 件の P1）は、どの文も同じ前提を書かず同じ穴を持つことを示した。以後、`security: true` の orchestrator 側タスク文は本節を参照で適用し、本節の各項目に対応する threat 行を持つ。文ごとに言い換えない。

1. **書き込み境界（前提 6、ランタイム別に正直に）** Claude worker 席は専用の設定ディレクトリ `CLAUDE_CONFIG_DIR=~/.claude-worker`（chezmoi が描画、operator が一度 login）で起動し、orchestrator の `~/.claude` と設定を共有しない。worker 設定：除外コマンド無し、Herdr socket 無し、sandbox の allowWrite は自席 worktree と agmsg store と席別キャッシュだけ、`failIfUnavailable: true`、信頼パス（anchored checkout の `.claude/worktrees/` 以外、`~/.agents`、`~/.claude*`、`~/.local`、`~/.config`）への Edit deny（公式文書：file tool の permission 検査は要求パスと symlink 解決後のパスの両方に deny を適用し、symlink そのものへの書き込みは拒否する）、hook は agmsg 配送と境界 hook だけを絶対パスのインタプリタで、各 hook に `onFailure: "block"`。公式文書で確認した事実（2026-10-19）：`Edit(path)` の deny は Write/MultiEdit/NotebookEdit にも効き、deny → ask → allow の順で最初の一致が決まる；ただし Read/Edit の deny は **Bash sandbox の設定にも合流する**（"Paths and domains from both sandbox settings and permission rules are merged into the final sandbox configuration"）ので、ユーザー設定（全席共有）に `.orchestration/**` の Edit deny を書くと orchestrator の Bash による記録書き込みも止まる。hook は起動時に固定されず、設定ファイルの編集は file watcher が即座に反映する。`sandbox.failIfUnavailable` の既定は fail-open（依存が無ければ sandbox 無しで実行）。したがって Claude 席の境界は Edit deny 規則ではなく、**ユーザーレベルの PreToolUse hook**（`~/.claude/hooks/worker-write-boundary`、chezmoi が描画、`/bin/sh` または絶対パスの `python3 -I`）で作る：cwd の realpath が `<anchored>/.claude/worktrees/` 配下の session では、Write/Edit/MultiEdit/NotebookEdit の対象が cwd の外、または `<cwd>/.claude/**`・`<cwd>/.mcp.json` のとき `permissionDecision: deny` を返す。Bash 側は sandbox の既定 `denyWithinAllow`（settings、hooks）と `allowWrite`（自席 worktree）が担う。`failIfUnavailable: true` を全席に置く。 Codex 席は sandbox（workspace-write）がツールの書き込み全部を自席の worktree と列挙パスに限る。Claude 席は Seatbelt sandbox が Bash を限るだけで、Write/Edit/MultiEdit/NotebookEdit、hook、MCP プロセスは sandbox 外で動き、permission policy（permgate の決定論ポリシー）が path で拒否しない限り anchored checkout や `~/.agents` にも書ける（2026-10-19 時点、描画済み設定にその deny は無い）。したがって前提 6 は「Codex 席は成立、Claude 席は P1-15 が描画設定に Edit の path deny を入れるまで残余」と書く。P1-15 以前に「worker は信頼ルートに書けない」と書く文は誤りで、C-80 が拒否する。P1-15 が入るまで、承認の出所は項目 8 の「コミット済み台帳」で守る。書き込みは自席の worktree（`.claude/worktrees/<name>`）、scratch、列挙されたツールキャッシュに限る。anchored checkout（`.claude/worktrees/` 以外）、`~/.agents/agent-config.yaml`、`~/.claude/hooks`、信頼ルートのバイナリ、orchestrator の証跡・スナップショット・lock は worker から書けない。render テストが描画後の deny を検証する。残余は「どの席 sandbox にも属さない同一 UID プロセス」と、Worker Playbook step 4 が sandbox 外に出す少数のコマンド（gh）。後者は D-024-17（P1-15）で絶対パスの実行体に束縛する。
2. **無害化した環境を最初に** 最初の処理として `env -i` に入り、PATH は信頼ルートで解決した絶対バイナリへのリンクだけの私設ディレクトリ（shims、空、相対は拒否）。git は毎回 `GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null -c core.hooksPath=/dev/null -c core.fsmonitor=false -c protocol.allow=never -c protocol.https.allow=always` と明示 `-C`（https だけ許す。`protocol.allow=never` 単独は必要な fetch を止める）。 diff と show は `--no-ext-diff --no-textconv` と `-c core.attributesFile=/dev/null -c core.sshCommand=false` を付け、PR 側の `.gitattributes`（external diff、textconv、filter）が検査内容や実行物を変えないようにする。Python は `-I`。PATH 探索で実行するものは無い。
3. **信頼パスの境界検査** 仕組みが信頼するパス（スクリプト、台帳、証跡、worktree、lock、出力先）は realpath で解決し、`.claude/worktrees/` または manifest の worker ルート配下なら拒否（ask/hold）。symlink 構成要素は解決後に比較し、大小文字を区別しないファイルシステムでは同一性比較を大小文字非依存で行う。
4. **検証したものを実行し、検証した内容を渡す** 検証した実行体はその realpath で実行する（再探索しない）。検証したファイル内容は信頼ルート配下のスナップショット（0600、一意名）として渡し、使用直前に sha256 を再照合する。判断に読んだ証跡は sha256 を出力に記録する。
5. **出力と予約の同一性** 名前には 40 桁の head を使う（7 桁で衝突させない）。lock は信頼ルート配下の固定 inode に O_EXCL で作り、置換を inode 比較で検出する。物理スロット 1 つに lock 1 つ。
6. **正直な残余** 境界だけが緩和するリスクを `closed` と書かない。各文は残余を 1 行で明記する。
0. **脅威モデル（D-024-21）** 席は同じ OS ユーザで動き、ホストは席間の信頼境界ではない（同一 UID のプロセスは symlink 差し替え、共有 `.git` の object 差し替え、hook の子プロセス、Herdr socket 経由の host 実行で、ホスト内のどの検査も迂回できる）。regime の硬い境界は GitHub（保護された main、必須チェック、orchestrator の identity によるマージ）。悪意ある worker に耐えるべき入力（承認台帳、gate が読む証跡 of record）は GitHub から sha 指定で API 経由（sandbox 内）に読み、ローカルファイルやローカル object database からは読まない。ホスト内の制御（本節 1〜10）は事故と prompt injection による損害の抑制であり、文はそう書く。

 succeeded in 133ms:
~/.agents/skills/agmsg/scripts/lib/node.sh:1:#!/usr/bin/env bash
~/.agents/skills/agmsg/scripts/lib/node.sh:7:# via the `#!/usr/bin/env node` shebang, and Codex monitor silently never starts.
~/.agents/skills/agmsg/scripts/lib/node.sh:12:# bare "node" so the behaviour is never worse than relying on PATH today (the
~/.agents/skills/agmsg/scripts/lib/node.sh:15:agmsg_resolve_node() {
~/.agents/skills/agmsg/scripts/lib/node.sh:28:  if command -v node >/dev/null 2>&1; then
~/.agents/skills/agmsg/scripts/lib/node.sh:29:    command -v node
~/.agents/skills/agmsg/scripts/lib/node.sh:33:  # Glob the version-manager dirs directly in the for-list (expands in both bash
~/.agents/skills/agmsg/scripts/lib/node.sh:39:    "$HOME"/.nvm/versions/node/*/bin/node \
~/.agents/skills/agmsg/scripts/lib/node.sh:40:    "$HOME"/.fnm/node-versions/*/installation/bin/node \
~/.agents/skills/agmsg/scripts/lib/node.sh:41:    "$HOME"/.local/share/fnm/node-versions/*/installation/bin/node; do
~/.agents/skills/agmsg/scripts/lib/node.sh:52:  for n in "$HOME/.volta/bin/node" /opt/homebrew/bin/node /usr/local/bin/node /usr/bin/node; do
~/.agents/skills/agmsg/scripts/lib/node.sh:59:  printf '%s\n' "node"
~/.agents/skills/agmsg/scripts/lib/node.sh:63:# agmsg_node_usable -- 0 if agmsg_resolve_node's answer is actually usable,
~/.agents/skills/agmsg/scripts/lib/node.sh:64:# 1 otherwise. agmsg_resolve_node always returns SOMETHING (falling back to
~/.agents/skills/agmsg/scripts/lib/node.sh:65:# the bare string "node" even when nothing was found), so callers that need
~/.agents/skills/agmsg/scripts/lib/node.sh:72:agmsg_node_usable() {
~/.agents/skills/agmsg/scripts/lib/node.sh:73:  local node; node="$(agmsg_resolve_node)"
~/.agents/skills/agmsg/scripts/lib/node.sh:74:  if [ "${node#*/}" != "$node" ]; then
~/.agents/skills/agmsg/scripts/lib/node.sh:75:    [ -x "$node" ]
~/.agents/skills/agmsg/scripts/lib/node.sh:77:    command -v "$node" >/dev/null 2>&1
~/.agents/skills/agmsg/scripts/lib/type-registry.sh:1:#!/usr/bin/env bash
~/.agents/skills/agmsg/scripts/lib/type-registry.sh:56:agmsg_type_dir() {
~/.agents/skills/agmsg/scripts/lib/type-registry.sh:105:  dir="$(agmsg_type_dir "$name")" || { printf '%s\n' "$def"; return 0; }
~/.agents/skills/agmsg/scripts/lib/type-registry.sh:132:  dir="$(agmsg_type_dir "$name")" || return 1
~/.agents/skills/agmsg/scripts/lib/type-registry.sh:157:# and test_helper.bash's agmsg_renderable_types() read as a plain variable.
~/.agents/skills/agmsg/scripts/identities.sh:1:#!/usr/bin/env bash
~/.agents/skills/agmsg/scripts/identities.sh:20:SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
~/.agents/skills/agmsg/scripts/identities.sh:21:SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"  # resolve-project.sh requires SKILL_DIR
~/.agents/skills/agmsg/scripts/identities.sh:22:TEAMS_DIR="$SCRIPT_DIR/../teams"
~/.agents/skills/agmsg/scripts/identities.sh:24:source "$SCRIPT_DIR/lib/resolve-project.sh"
~/.agents/skills/agmsg/scripts/identities.sh:26:source "$SCRIPT_DIR/lib/storage.sh"
26:#   it, claim the orchestrator's agmsg seat outside the sandbox under the
33:#   `--ask-for-approval never` and `sandbox_workspace_write.network_access=true`,
34:#   so it never prompts and out-of-sandbox actions fail instead of escalating.
40:# @option --bootstrap-agmsg Configure repo-scoped agmsg hooks without changing Herdr panes.
46:#   `.orchestration/tasks/<id>.md`, the worker's report, validation and sandbox
58:# @option --stale Remove-worker: retire a seat whose pane is gone (no despawn; delivery off, leave, the placement record moved to the run directory's stale/); refused for any other state.
77:#   herdr-agents --add-worker .claude/worktrees/worker-c --kind claude
92:       herdr-agents --add-worker [<worktree>] [--kind codex|claude] [--profile NAME] [--ready-timeout SECONDS] [DIR]
122:Bootstrap mode only configures missing repo-scoped agmsg hooks and removes the
133:sandbox files and ID-pr-feedback.json (those present), and the PR diff from
144:codex or claude. A codex worker runs with --sandbox workspace-write,
145:--ask-for-approval never and sandbox_workspace_write.network_access=true: it
146:never prompts, it reaches the network (GitHub included) inside the sandbox, and
149:config (on-request approvals, no sandbox network).
151:socket ~/.config/herdr/herdr.sock (the path the Claude sandbox allowlists), a claude worker's workspace-trust dialog is accepted while spawn.sh
153:remove-worker mode despawns it, turns its delivery off, leaves its team, and
287:#   checkout; it is joined with AGMSG_RESOLVE_PROJECT=0 so upstream project
308:    seated="$(AGMSG_RESOLVE_PROJECT=0 "${scripts}/identities.sh" "${worktree}" "${agent_type}" 2> /dev/null | sort -u)" || seated=""
319:    orchestrator="$(AGMSG_RESOLVE_PROJECT=0 "${scripts}/identities.sh" "${workdir}" "${orchestrator_agmsg_type}" 2> /dev/null |
322:        printf 'herdr-agents: need exactly one orchestrator %s identity at %s to name the worker; register the worker yourself with: AGMSG_RESOLVE_PROJECT=0 %s/join.sh <team> <name> %s %q\n' \
328:    next="$(AGMSG_RESOLVE_PROJECT=0 "${scripts}/team.sh" "${team}" --json 2> /dev/null |
332:        AGMSG_RESOLVE_PROJECT=0 "${scripts}/join.sh" "${team}" "${name}" "${agent_type}" "${worktree}" > /dev/null
337:# @description Point agmsg delivery at the worker worktree when its hook is
338:#   missing: `both` for claude-code (turn delivery; upstream session-start.sh
340:#   there), `turn` for codex. delivery.sh bakes the path into the hook.
343:function ensure_worker_delivery() {
346:    local delivery="${HOME}/.agents/skills/agmsg/scripts/delivery.sh"
349:    [[ -x ${delivery} ]] || return 0
352:        jq -e 'any(.hooks.Stop[]?.hooks[]?; ((.command // "") | contains("agmsg/scripts/check-inbox.sh")))' \
353:            "${worktree}/.claude/settings.local.json" > /dev/null 2>&1 && return 0
354:        "${delivery}" set both claude-code "${worktree}" >> "${log_file}" 2>&1 || true
356:        jq -e 'any(.hooks.Stop[]?.hooks[]?; ((.bash // .command // "") | contains("agmsg/scripts/check-inbox.sh")))' \
357:            "${worktree}/.codex/hooks.json" > /dev/null 2>&1 && return 0
358:        if "${delivery}" set turn codex "${worktree}" >> "${log_file}" 2>&1; then
359:            printf 'Codex loads the new hook in %s only after that project .codex layer is trusted; run /hooks or trust it in Codex.\n' "${worktree}" >&2
365:#   settings, preserving hooks and other permissions. Main checkouts and Codex
371:    local settings="${worktree}/.claude/settings.local.json" input temporary
397:#   dir itself, config, hooks, info, HEAD, packed-refs and, in a shallow
403:#   when the file exists but cannot be parsed, or its writable_roots is not a
408:# @stdout `sandbox_workspace_write.writable_roots=[...]`, or nothing.
409:function codex_worktree_writable_roots() {
427:    roots = tomllib.load(handle).get("sandbox_workspace_write", {}).get("writable_roots", [])
433:        printf 'herdr-agents: cannot read sandbox_workspace_write.writable_roots in %s as a list of strings (python3 3.11+ tomllib); the codex worker in %s gets no git metadata roots.\n' "${config}" "${worktree}" >&2
438:        if all(.[]; type == "string" and (contains("#") | not)) then "sandbox_workspace_write.writable_roots=" + tojson else error("unsupported") end' \
451:#   --sandbox workspace-write --ask-for-approval never --config
452:#   sandbox_workspace_write.network_access=true` for codex, plus the
454:#   codex_worktree_writable_roots) for a codex worker when a worktree is given.
474:    [[ ${kind} == claude ]] || args="--profile ${HERDR_AGENTS_WORKER_PROFILE} --sandbox workspace-write --ask-for-approval never --config sandbox_workspace_write.network_access=true"
489:        roots="$(codex_worktree_writable_roots "$2")"
553:#   AGMSG_AGENT_PID overrides the walk as in upstream agmsg_agent_pid: a numeric
559:    if [[ -n ${AGMSG_AGENT_PID+set} ]]; then
560:        [[ ${AGMSG_AGENT_PID} =~ ^[0-9]+$ ]] || return 1
561:        printf '%s\n' "${AGMSG_AGENT_PID}"
577:# @description Claim the orchestrator's agmsg seat outside any sandbox under the
579:#   inbox check compares the actas lock against. A claim from sandboxed Bash
581:#   turn delivery then skips silently. Applies only in a git main checkout with
592:#   and the claim repeated. A bare owner can only come from a sandboxed claim
614:    identity="$(AGMSG_RESOLVE_PROJECT=0 "${scripts}/identities.sh" "${workdir}" claude-code 2> /dev/null |
617:    teams="$(AGMSG_RESOLVE_PROJECT=0 "${scripts}/identities.sh" "${workdir}" claude-code 2> /dev/null |
625:            ! AGMSG_RESOLVE_PROJECT=0 "${scripts}/identities.sh" "${workdir}" claude-code 2> /dev/null |
656:        if result="$(AGMSG_SELF_NAME="${self_name}" AGMSG_RESOLVE_PROJECT=0 \
695:    identity="$(AGMSG_RESOLVE_PROJECT=0 "${identities}" "${workdir}" "${type}" 2> /dev/null |
992:        [[ ${worktree} == "$1/.claude/worktrees/"* ]] || continue
994:            AGMSG_RESOLVE_PROJECT=0 "${identities}" "${worktree}" claude-code
995:            AGMSG_RESOLVE_PROJECT=0 "${identities}" "${worktree}" codex
1190:            seat="$(AGMSG_RESOLVE_PROJECT=0 "${scripts}/identities.sh" "${seat_dir}" "${seat_type}" 2> /dev/null | head -n 1)" || seat=""
1203:    printf 'herdr-agents: not in a Herdr pane, so the orchestrator pane is not started; start the worker on demand with "herdr-agents --add-worker %s [DIR]" and run the auditor headless as the agmsg-orchestration SKILL task-level audit bullet shows ("codex <audit profile args> exec --sandbox read-only -C <repo> -o <out>.last.md <prompt>"); %s.\n' \
1236:    rows="$(AGMSG_RESOLVE_PROJECT=0 "${scripts}/identities.sh" "${main}" claude-code 2> /dev/null |
1246:    rows="$(AGMSG_RESOLVE_PROJECT=0 "${scripts}/identities.sh" "${main}" "${worker_type}" 2> /dev/null |
1249:    if [[ ${seat_worktree} =~ ^\.claude/worktrees/[A-Za-z0-9._-]+$ && -d ${main}/${seat_worktree} ]]; then
1250:        rows+=$'\n'"$(AGMSG_RESOLVE_PROJECT=0 "${scripts}/identities.sh" "${main}/${seat_worktree}" "${worker_type}" 2> /dev/null)" || true
1338:    printf '%s' '(((.cwd // "") | startswith($worktrees)) or .label == "codex-worker" or .label == "claude-worker")'
1345:    printf '%s\n' "$1" | jq -e --arg worktrees "${workdir}/.claude/worktrees/" \
1364:#   creates exports AGMSG_RESOLVE_PROJECT=0 so those calls keep the worker's own
1380:#   installer placed it (`git rev-parse --git-path hooks`, which honours
1381:#   core.hooksPath) and only inside the common git dir, where alone the
1392:    hook="$(git -C "${workdir}" rev-parse --path-format=absolute --git-path hooks 2> /dev/null)/pre-push" || return 0
1393:    # The installer never wrote outside the common git dir (a core.hooksPath
1404:# @description Skip $HOME or ensure Codex and Claude Code agmsg delivery hooks,
1417:    local delivery="${scripts}/delivery.sh"
1419:    local claude_hooks_file="${workdir}/.claude/settings.local.json"
1425:    # Workers are seated in linked worktrees with their own hooks there, so
1427:    if [[ ! -f ${delivery} ]]; then
1428:        printf 'agmsg delivery script not found; skipping bootstrap: %s\n' "${delivery}" >&2
1432:    if ! { [[ -f ${claude_hooks_file} ]] && jq -e \
1433:        'any(.hooks.SessionStart[]?.hooks[]?; ((.command // "") | contains("agmsg/scripts/session-start.sh")))' \
1434:        "${claude_hooks_file}" > /dev/null 2>&1; }; then
1435:        if "${delivery}" set both claude-code "${workdir}" >> "${log_file}" 2>&1; then
1436:            printf 'First-time Claude Code agmsg setup may stop one same-repo watcher once; the hooks apply in the next Claude Code session.\n' >&2
1463:                printf 'No agmsg %s identity for %s; run: AGMSG_RESOLVE_PROJECT=0 %s/join.sh <team> <agent-name> %s "%s"\n' \
1485:    printf '%s\n' "$1" | jq -r --arg worktrees "${workdir:-}/.claude/worktrees/" \
1644:    # SessionStart runs outside the Bash sandbox: claim the orchestrator seat
1717:        if [[ $# -eq 0 && -n ${seat_worktree} && ${seat_worktree} != .claude/worktrees/* ]]; then
1757:    # Hooks only: an existing worker worktree gets its delivery hook; seating
1762:        ensure_worker_delivery "${seat_kind}" "${seat_dir}"
1776:    if [[ ! ${seat_worktree} =~ ^\.claude/worktrees/[A-Za-z0-9._-]+$ || ${seat_worktree##*/} == . || ${seat_worktree##*/} == .. ]]; then
1777:        printf 'herdr-agents: the worker worktree must be a path under .claude/worktrees/; got %q\n' "${seat_worktree}" >&2
1790:        # sandbox allowlists (allowUnixSockets); XDG_CONFIG_HOME is not honoured,
1844:            [[ -n "$(AGMSG_RESOLVE_PROJECT=0 "${scripts}/identities.sh" "${seat_path}" claude-code 2> /dev/null)$(AGMSG_RESOLVE_PROJECT=0 "${scripts}/identities.sh" "${seat_path}" codex 2> /dev/null)" ]] || continue
1859:    ensure_worker_delivery "${seat_kind}" "${seat_dir}"
9:.agents/worklog/
11:.agents/runs/

web search: https://git-scm.com/docs/git-replace
**Analyzing access and permission rules**
exec
/bin/zsh -lc "rg -n -A 16 -B 3 'writable_roots' home/dot_agents/agent-config.yaml; sed -n '380,465p' home/dot_local/bin/common/executable_herdr-agents; sed -n '1,70p' ~/.agents/skills/agmsg/scripts/lib/storage.sh; sed -n '50,85p' ~/.agents/skills/agmsg/scripts/lib/type-registry.sh" in ~/Workspace/dotfiles
 succeeded in 15ms:
113-      gpt-5.6-sol: 2
114-  sandbox_workspace_write:
115-    network_access: false
116:    writable_roots:
117-      - '{{ .chezmoi.homeDir }}/.agents/skills/agmsg/db'
118-      - '{{ .chezmoi.homeDir }}/.agents/skills/agmsg/teams'
119-      - '{{ .chezmoi.homeDir }}/.agents/skills/agmsg/run'
120-      - '{{ .chezmoi.homeDir }}/.agents/skills/agmsg/ext-tools'
121-  shell_environment_policy:
122-    inherit: core
123-    set:
124-      PATH: '{{ .chezmoi.homeDir }}/.local/share/mise/installs/node/lts/bin:{{ .chezmoi.homeDir }}/.local/share/mise/shims:{{ .chezmoi.homeDir }}/.local/bin:{{ .chezmoi.homeDir }}/.local/bin/common:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin'
125-  features:
126-    plugins: true
127-    hooks: true
128-    plugin_hooks: true
129-  plugins:
130-    superpowers@openai-curated:
131-      enabled: true
132-    crit@mryfmo-personal-plugins:
--
267-  # Claude Code Bash sandbox, the counterpart of codex.sandbox_workspace_write:
268-  # commands may write only the working directory, the session TMPDIR, and
269-  # filesystem.allowWrite. The generator renders allowWrite from
270:  # codex.sandbox_workspace_write.writable_roots so both agents share one agmsg
271-  # writable-roots list; ~/.claude is sandbox-protected, so it is not listed.
272-  # bubblewrap and socat come from the installers that the operator runs with
273-  # `make update` outside Claude sessions; on Ubuntu 24.04+ the bwrap-userns
274-  # AppArmor profile (install/ubuntu/common/apparmor_userns.sh) lets bwrap
275-  # create user namespaces.
276-  sandbox:
277-    enabled: true
278-    # Two-stage rollout: warn and run unsandboxed while bwrap/socat are missing;
279-    # flip to true only after live E2E.
280-    failIfUnavailable: false
281-    autoAllowBashIfSandboxed: true
282-    allowUnsandboxedCommands: true
283-    # Patterns need a trailing wildcard for arguments; every chained command must match.
284-    # Exclusion retains the normal permission flow (sandboxing docs, T130).
285-    excludedCommands:
286-      # agmsg-dispatch: inserts one agmsg row and sends a herdr wake. From
        $deny + (["Bash(gh pr merge:*)", "Bash(gh api -X PUT:*)",
                  "Bash(gh api --method PUT:*)", "Bash(gh api graphql:*)"] - $deny))' \
        "${input}" > "${temporary}"
    if cmp -s "${settings}" "${temporary}"; then
        rm -- "${temporary}"
    else
        mv -- "${temporary}" "${settings}"
    fi
}

# @description Print the Codex `-c` override that makes a linked worktree's git
#   metadata writable for a codex worker. A worktree's index, HEAD and objects
#   live under the main checkout's git common dir, outside the workspace-write
#   root, so every git add/commit/fetch/rebase would otherwise fail (the worker
#   runs with --ask-for-approval never, so nothing escalates). Granted:
#   <common>/objects, <common>/refs, <common>/logs and the worktree's own
#   <common>/worktrees/<name>; the common
#   dir itself, config, hooks, info, HEAD, packed-refs and, in a shallow
#   clone, shallow (so git fetch --deepen/--unshallow still fails, reported on
#   stderr) stay read-only.
#   `-c` replaces the array, so the roots configured in
#   ${CODEX_HOME:-~/.codex}/config.toml (the agmsg store) are kept in front.
#   The file is parsed with python3's tomllib (3.11+). The grant fails closed:
#   when the file exists but cannot be parsed, or its writable_roots is not a
#   list of strings, it prints a stderr line and no override, so the worker
#   keeps its configured roots. Prints nothing for a main checkout (its git dir
#   is the common dir).
# @arg $1 path Worker worktree.
# @stdout `sandbox_workspace_write.writable_roots=[...]`, or nothing.
function codex_worktree_writable_roots() {
    local worktree="$1"
    local common git_dir config configured="[]"

    [[ -n ${worktree} ]] || return 0
    common="$(git -C "${worktree}" rev-parse --path-format=absolute --git-common-dir 2> /dev/null)" || return 0
    git_dir="$(git -C "${worktree}" rev-parse --path-format=absolute --git-dir 2> /dev/null)" || return 0
    [[ ${git_dir} == "${common}/worktrees/"* ]] || return 0
    config="${CODEX_HOME:-${HOME}/.codex}/config.toml"
    # A missing file or key leaves the configured roots empty, which -c cannot
    # narrow; any other doubt keeps the configured roots by emitting nothing.
    if [[ -e ${config} ]] && ! configured="$(
        python3 - "${config}" 2> /dev/null << 'PY'
import json
import sys
import tomllib

with open(sys.argv[1], "rb") as handle:
    roots = tomllib.load(handle).get("sandbox_workspace_write", {}).get("writable_roots", [])
if not isinstance(roots, list) or not all(isinstance(root, str) for root in roots):
    sys.exit(1)
print(json.dumps(roots))
PY
    )"; then
        printf 'herdr-agents: cannot read sandbox_workspace_write.writable_roots in %s as a list of strings (python3 3.11+ tomllib); the codex worker in %s gets no git metadata roots.\n' "${config}" "${worktree}" >&2
        return 0
    fi
    # The spawn options dialect strips ` #...` as a comment, so no root may hold `#`.
    if ! jq -cn --argjson configured "${configured}" '$configured + $ARGS.positional |
        if all(.[]; type == "string" and (contains("#") | not)) then "sandbox_workspace_write.writable_roots=" + tojson else error("unsupported") end' \
        -r --args "${common}/objects" "${common}/refs" "${common}/logs" "${git_dir}" 2> /dev/null; then
        printf 'herdr-agents: a writable root for the codex worker in %s contains "#"; it gets no git metadata roots.\n' "${worktree}" >&2
        return 0
    fi
    if [[ "$(git -C "${worktree}" rev-parse --is-shallow-repository 2> /dev/null)" == true ]]; then
        printf 'herdr-agents: %s is a shallow clone; its shallow metadata (%s/shallow) is not granted, so git fetch --deepen or --unshallow in the codex worker fails.\n' "${worktree}" "${common}" >&2
    fi
}

# @description Print the agmsg spawn options YAML that carries a worker
#   profile's launch arguments (spawn.sh splices the type section into the boot
#   command): MODEL_PROFILE_<NAME>_CLAUDE_ARGS for claude, and `--profile <name>
#   --sandbox workspace-write --ask-for-approval never --config
#   sandbox_workspace_write.network_access=true` for codex, plus the
#   worktree's git metadata roots (`--config`, see
#   codex_worktree_writable_roots) for a codex worker when a worktree is given.
# @arg $1 string Worker kind.
# @arg $2 path Worker worktree (optional).
# @exitcode 2 If the profile is not defined in ~/.agents/model-profiles.env or
#   its arguments are not plain `--flag value` pairs.
function write_spawn_options() {
    local kind="$1"
    local profile_env_key args index roots
    local -a words=()

    profile_env_key="MODEL_PROFILE_$(printf '%s' "${HERDR_AGENTS_WORKER_PROFILE}" | tr '[:lower:]' '[:upper:]')_$(printf '%s' "${kind}" | tr '[:lower:]' '[:upper:]')_ARGS"
    args="$(
#!/usr/bin/env bash
# storage.sh — resolve the path to the sqlite message store (messages.db).
#
# Scope: the storage axis only — where messages are persisted. This is NOT a
# storage-driver interface; it just centralizes the path resolution that was
# previously duplicated across the script set.
#
# Resolution order:
#   1. AGMSG_STORAGE_PATH — directory that holds messages.db (env override)
#   2. SKILL_DIR env var  — set by callers before sourcing (sandbox fallback)
#   3. BASH_SOURCE[0]     — derive from this file's own path (standard case)
#
# [seam] A config-file layer is expected to slot in between the env override
# and the built-in default once the storage-driver work lands; the intended
# full order is env > config > default. Keep that logic here so call sites
# stay unchanged.

# Guard against double-source. This used to be genuinely harmless to skip
# (every top-level assignment below was a pure function definition, so
# re-running them just redefined the same functions) -- resolve-project.sh's
# own comment on its unconditional ". storage.sh" says so explicitly. That
# stopped being true once this file gained STATEFUL per-process caches
# (agmsg_storage_dir, _agmsg_partition_load): re-sourcing reset them to their
# initial empty state, silently discarding whatever a caller had already
# warmed (measured: watch.sh's own top-level warm of agmsg_storage_dir was
# being wiped by resolve-project.sh's re-source moments later, #1330 second
# stage). Every existing caller already tolerates a no-op re-source (that
# was the whole premise); this guard just makes that no-op literal instead
# of a same-effect-so-far redefinition that quietly stopped being one.
[ -n "${_AGMSG_STORAGE_SH:-}" ] && return 0
_AGMSG_STORAGE_SH=1

# agmsg_db_path turns the team selector into a path segment, so it cannot do its
# job without the shared name validator. Sourced here rather than left to each
# caller: watch.sh already reached the store without validate.sh in scope, and a
# caller that forgets it would build an unchecked path rather than fail.
# validate.sh guards against double-sourcing, so a caller that sources it too is
# unaffected. If neither locator resolves, the validator is simply absent and
# agmsg_db_path fails on the call — never silently unvalidated.
if ! declare -F agmsg_validate_team_name >/dev/null 2>&1; then
  if [ -n "${BASH_SOURCE[0]:-}" ]; then
    # shellcheck disable=SC1091
    source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/validate.sh"
  elif [ -n "${SKILL_DIR:-}" ]; then
    # BASH_SOURCE empty — see agmsg_storage_dir for when that happens.
    # shellcheck disable=SC1091
    source "$SKILL_DIR/scripts/lib/validate.sh"
  fi
fi

# Built-in storage drivers use the shared UUIDv7 generator. Keep it available
# through the storage facade so direct and registry-driven loads use one
# implementation on every platform.
if ! declare -F compat_uuid7 >/dev/null 2>&1; then
  if [ -n "${BASH_SOURCE[0]:-}" ]; then
    # shellcheck disable=SC1091
    source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/compat.sh"
  elif [ -n "${SKILL_DIR:-}" ]; then
    # shellcheck disable=SC1091
    source "$SKILL_DIR/scripts/lib/compat.sh"
  fi
fi

# Echo the directory that holds (or will hold) the message store.
#
# Memoized for the life of the process (_AGMSG_STORAGE_DIR_CACHE): every
# input this depends on -- AGMSG_STORAGE_PATH, this script's own on-disk
# location -- is fixed for as long as the process runs, unlike a team's
# storage driver choice (see _agmsg_partition_load's own comment for that
# distinction). A caller that overrides AGMSG_STORAGE_PATH mid-process
EOF
}

# Echo the directory holding <name>/type.conf, or return 1. Later bases override
# earlier ones among ELIGIBLE candidates: built-ins are always eligible; external
# drivers only once opted into. Untrusted external candidates are skipped.
agmsg_type_dir() {
  local want="$1" kind base dir chosen=""
  while IFS=$'\t' read -r kind base; do
    dir="$base/types/$want"
    [ -f "$dir/type.conf" ] || continue
    if [ "$kind" = builtin ] || agmsg_driver_is_trusted types "$want" "$dir"; then
      chosen="$dir"
    fi
  done <<EOF
$(agmsg_driver_bases)
EOF
  [ -n "$chosen" ] && { printf '%s\n' "$chosen"; return 0; }
  return 1
}

# List all known (eligible) type names, with duplicates the caller dedups via
# `sort -u`. Surfaces untrusted-external warnings as a side effect (once/process).
agmsg_known_types() {
  _agmsg_type_warn_untrusted
  local kind base dir name
  while IFS=$'\t' read -r kind base; do
    [ -d "$base/types" ] || continue
    for dir in "$base"/types/*/; do
      [ -f "${dir}type.conf" ] || continue
      name="$(basename "$dir")"
      [ "$kind" = builtin ] || agmsg_driver_is_trusted types "$name" "${dir%/}" || continue
      printf '%s\n' "$name"
    done
  done <<EOF
$(agmsg_driver_bases)

web search: 
web search: 'deny rules'
**Analyzing settings precedence**
web search: 
web search: 
exec
/bin/zsh -lc "sed -n '320,389p' home/dot_local/bin/common/executable_herdr-agents; sed -n '1404,1450p' home/dot_local/bin/common/executable_herdr-agents; rg -n -A 16 -B 8 'agmsg|attach|hooks' home/dot_claude/modify_private_settings.json" in ~/Workspace/dotfiles
 succeeded in 141ms:
        awk -F '\t' '$2 !~ /-a[0-9][0-9][0-9]$/' | sort -u)" || orchestrator=""
    if [[ -z ${orchestrator} || ${orchestrator} == *$'\n'* ]]; then
        printf 'herdr-agents: need exactly one orchestrator %s identity at %s to name the worker; register the worker yourself with: AGMSG_RESOLVE_PROJECT=0 %s/join.sh <team> <name> %s %q\n' \
            "${orchestrator_agmsg_type}" "${workdir}" "${scripts}" "${agent_type}" "${worktree}" >&2
        exit 2
    fi
    team="${orchestrator%%$'\t'*}"
    suffix="${orchestrator##*-}"
    next="$(AGMSG_RESOLVE_PROJECT=0 "${scripts}/team.sh" "${team}" --json 2> /dev/null |
        jq -r '.[]?.member // empty' | sed -n 's/.*-a\([0-9][0-9][0-9]\)$/\1/p' | sort -n | tail -n 1)" || next=""
    printf -v name '%s-%s-%s-a%03d' "${kind}" "${HERDR_AGENTS_WORKER_PROFILE}" "${suffix}" "$((10#${next:-0} + 1))"
    if [[ ${join} != --no-join ]]; then
        AGMSG_RESOLVE_PROJECT=0 "${scripts}/join.sh" "${team}" "${name}" "${agent_type}" "${worktree}" > /dev/null
    fi
    printf '%s\t%s\n' "${team}" "${name}"
}

# @description Point agmsg delivery at the worker worktree when its hook is
#   missing: `both` for claude-code (turn delivery; upstream session-start.sh
#   skips sessions under .claude/worktrees, #367, so no Monitor watch starts
#   there), `turn` for codex. delivery.sh bakes the path into the hook.
# @arg $1 string Worker kind.
# @arg $2 path Absolute worker worktree path.
function ensure_worker_delivery() {
    local kind="$1"
    local worktree="$2"
    local delivery="${HOME}/.agents/skills/agmsg/scripts/delivery.sh"
    local log_file="${HOME}/.config/herdr/herdr-agents.log"

    [[ -x ${delivery} ]] || return 0
    mkdir -p "${log_file%/*}"
    if [[ ${kind} == claude ]]; then
        jq -e 'any(.hooks.Stop[]?.hooks[]?; ((.command // "") | contains("agmsg/scripts/check-inbox.sh")))' \
            "${worktree}/.claude/settings.local.json" > /dev/null 2>&1 && return 0
        "${delivery}" set both claude-code "${worktree}" >> "${log_file}" 2>&1 || true
    else
        jq -e 'any(.hooks.Stop[]?.hooks[]?; ((.bash // .command // "") | contains("agmsg/scripts/check-inbox.sh")))' \
            "${worktree}/.codex/hooks.json" > /dev/null 2>&1 && return 0
        if "${delivery}" set turn codex "${worktree}" >> "${log_file}" 2>&1; then
            printf 'Codex loads the new hook in %s only after that project .codex layer is trusted; run /hooks or trust it in Codex.\n' "${worktree}" >&2
        fi
    fi
}

# @description Add merge-denial rules to a Claude worker worktree's local
#   settings, preserving hooks and other permissions. Main checkouts and Codex
#   workers are untouched.
# @arg $1 string Worker kind.
# @arg $2 path Absolute worker worktree path.
function ensure_worker_merge_denials() {
    local kind="$1" worktree="$2"
    local settings="${worktree}/.claude/settings.local.json" input temporary

    [[ ${kind} == claude && -f ${worktree}/.git ]] || return 0
    is_main_checkout "${worktree}" && return 0
    mkdir -p "${settings%/*}"
    input="${settings}"
    [[ -f ${input} ]] || input=/dev/null
    temporary="$(mktemp "${settings}.XXXXXX")"
    jq -s '.[0] // {} | .permissions.deny = ((.permissions.deny // []) as $deny |
        $deny + (["Bash(gh pr merge:*)", "Bash(gh api -X PUT:*)",
                  "Bash(gh api --method PUT:*)", "Bash(gh api graphql:*)"] - $deny))' \
        "${input}" > "${temporary}"
    if cmp -s "${settings}" "${temporary}"; then
        rm -- "${temporary}"
    else
        mv -- "${temporary}" "${settings}"
    fi
}

# @description Skip $HOME or ensure Codex and Claude Code agmsg delivery hooks,
#   after removing the retired main-push guard stub (remove_retired_pre_push_stub).
# @arg $1 workdir Repository path used for repo-scoped agmsg registration.
function bootstrap_agmsg() {
    local workdir="$1"

    if [[ "$(cd -- "${workdir}" && pwd -P)" == "$(cd -- "${HOME}" && pwd -P)" ]]; then
        printf "Skipping agmsg bootstrap for \$HOME; use a repository directory instead.\n" >&2
        return 0
    fi
    remove_retired_pre_push_stub "$(cd -- "${workdir}" && pwd -P)"

    local scripts="${HOME}/.agents/skills/agmsg/scripts"
    local delivery="${scripts}/delivery.sh"
    local doctor="${scripts}/doctor.sh"
    local claude_hooks_file="${workdir}/.claude/settings.local.json"
    local log_file="${HOME}/.config/herdr/herdr-agents.log"
    local agent_type
    local agent_label
    local agent_types=(claude-code)

    # Workers are seated in linked worktrees with their own hooks there, so
    # the main checkout only carries the orchestrator's claude-code identity.
    if [[ ! -f ${delivery} ]]; then
        printf 'agmsg delivery script not found; skipping bootstrap: %s\n' "${delivery}" >&2
        return 0
    fi
    mkdir -p "${log_file%/*}"
    if ! { [[ -f ${claude_hooks_file} ]] && jq -e \
        'any(.hooks.SessionStart[]?.hooks[]?; ((.command // "") | contains("agmsg/scripts/session-start.sh")))' \
        "${claude_hooks_file}" > /dev/null 2>&1; }; then
        if "${delivery}" set both claude-code "${workdir}" >> "${log_file}" 2>&1; then
            printf 'First-time Claude Code agmsg setup may stop one same-repo watcher once; the hooks apply in the next Claude Code session.\n' >&2
        fi
    fi

    if [[ ! -x ${doctor} ]]; then
        printf 'agmsg doctor script not found; skipping identity checks: %s\n' "${doctor}" >&2
        return 0
    fi
    for agent_type in "${agent_types[@]}"; do
        local doctor_output doctor_status has_registration=true
        local count

        if [[ ${agent_type} == codex ]]; then
            agent_label=Codex
        else
24-MANAGED_SESSION_START_SCRIPTS = ("herdr-agent-state.sh", "herdr-agents")
25-MANAGED_POST_TOOL_USE_SCRIPTS = ("format-edited-files.py", "project-map-reload.sh")
26-
27-
28-def managed_post_tool_use_paths() -> set[str]:
29-    return {
30-        path
31-        for name in MANAGED_POST_TOOL_USE_SCRIPTS
32:        for path in (f"~/.claude/hooks/{name}", str(home_dir() / ".claude" / "hooks" / name))
33-    }
34-
35-
36-def source_dir() -> Path:
37-    if os.environ.get("CHEZMOI_SOURCE_DIR"):
38-        return Path(os.environ["CHEZMOI_SOURCE_DIR"])
39-    return Path(__file__).resolve().parents[1]
40-
41-
42-def home_dir() -> Path:
43-    if os.environ.get("CHEZMOI_HOME_DIR"):
44-        return Path(os.environ["CHEZMOI_HOME_DIR"])
45-    return Path.home()
46-
47-
48-def render_managed_template(text: str) -> str:
--
92-def is_managed_post_tool_use_hook(hook: Any) -> bool:
93-    if not isinstance(hook, dict) or not isinstance(hook.get("command"), str):
94-        return False
95-    # The whole command, not shlex's words: a quoted or escaped ~ is a literal directory, not the home path.
96-    return hook["command"].strip() in managed_post_tool_use_paths()
97-
98-
99-def entry_has_managed_hook(entry: Any, is_managed: Any) -> bool:
100:    if not isinstance(entry, dict) or not isinstance(entry.get("hooks"), list):
101-        return False
102:    return any(is_managed(hook) for hook in entry["hooks"])
103-
104-
105:def merge_managed_entries(current_hooks: Any, managed_entries: list[Any], is_managed: Any) -> list[Any]:
106-    """Replace managed entries in place so their position in the list is kept.
107-
108-    A fully managed entry is swapped for its managed counterpart, which is what
109-    lets a stale command (for example one rendered with a different home
110:    directory) be dropped without reordering the surrounding hooks. A mixed
111:    entry keeps its unmanaged hooks where they are, and the managed hook is
112-    re-appended with the rest of the managed entries.
113-    """
114-    queue = [entry for entry in managed_entries if entry_has_managed_hook(entry, is_managed)]
115-    merged: list[Any] = []
116-    index = 0
117:    for entry in current_hooks:
118-        if not entry_has_managed_hook(entry, is_managed):
119-            merged.append(entry)
120-            continue
121:        unmanaged = [hook for hook in entry["hooks"] if not is_managed(hook)]
122-        if unmanaged:
123:            merged.append({**entry, "hooks": unmanaged})
124-            continue
125-        if index < len(queue):
126-            merged.append(queue[index])
127-            index += 1
128-    return merged + [entry for entry in managed_entries if entry not in merged]
129-
130-
131-MANAGED_HOOK_PREDICATES = {
132-    "PermissionRequest": is_managed_permission_hook,
133-    "SessionStart": is_managed_session_start_hook,
134-    "PostToolUse": is_managed_post_tool_use_hook,
135-}
136-
137-
138:def merge_hooks(
139-    managed: dict[str, Any], current: dict[str, Any]
140-) -> dict[str, Any]:
141-    merged: dict[str, Any] = {}
142-    for key, value in current.items():
143-        managed_value = managed.get(key)
144-        if key in MANAGED_HOOK_PREDICATES and isinstance(managed_value, list):
145:            current_hooks = value if isinstance(value, list) else []
146-            merged[key] = merge_managed_entries(
147:                current_hooks, managed_value, MANAGED_HOOK_PREDICATES[key]
148-            )
149-        elif isinstance(value, list) and isinstance(managed_value, list):
150-            # ponytail: hook arrays are tiny; index entries only if they grow materially.
151-            merged[key] = value + [entry for entry in managed_value if entry not in value]
152-        elif key in managed:
153-            merged[key] = managed_value
154-        else:
155-            merged[key] = value
156-
157-    for key, value in managed.items():
158-        if key not in merged:
159-            merged[key] = value
160-    return merged
161-
162-
163-def merge_settings(managed: dict[str, Any], current: dict[str, Any] | None) -> dict[str, Any]:
--
166-
167-    merged: dict[str, Any] = {}
168-    for key, value in current.items():
169-        if key in RUNTIME_KEYS:
170-            merged[key] = value
171-        elif key in managed:
172-            managed_value = managed[key]
173-            if (
174:                key == "hooks"
175-                and isinstance(value, dict)
176-                and isinstance(managed_value, dict)
177-            ):
178:                merged[key] = merge_hooks(managed_value, value)
179-            elif key == "env" and isinstance(value, dict) and isinstance(managed_value, dict):
180-                merged[key] = value | managed_value
181-            else:
182-                merged[key] = managed_value
183-        else:
184-            merged[key] = value
185-
186-    for key, value in managed.items():
187-        if key not in merged:
188-            merged[key] = value
189-    return merged
190-
191-
192-def dump_settings(settings: dict[str, Any]) -> str:
193-    return json.dumps(settings, indent=2) + "\n"
194-
195-
196-def main() -> int:
197-    baseline = source_dir() / ".chezmoitemplates/claude-settings-managed.json"
198-    managed = json.loads(render_managed_template(baseline.read_text()))
199:    session_start = managed.get("hooks", {}).get("SessionStart")
200-    if isinstance(session_start, list):
201-        session_start.append(
202-            {
203-                "matcher": "*",
204:                "hooks": [
205-                    {
206-                        "type": "command",
207:                        "command": f'{home_dir()}/.local/bin/common/herdr-agents --attach 2>> "$HOME/.config/herdr/herdr-agents.log" || true',
208-                        "timeout": 10,
209-                    }
210-                ],
211-            }
212-        )
213-    current_text = sys.stdin.read()
214-    current = load_json_object(current_text)
215-    merged = merge_settings(managed, current)
216-    if current is not None and merged == current:
217-        sys.stdout.write(current_text)
218-    else:
219-        sys.stdout.write(dump_settings(merged))
220-    return 0
221-
222-
223-if __name__ == "__main__":

**Reviewing hook configurations**
**Analyzing shared GitHub credential risks**
web search: 
web search: https://cli.github.com/manual/gh_help_environment
exec
/bin/zsh -lc "/usr/bin/python3 -I -c 'import json,pathlib; p=pathlib.Path(\".claude/settings.local.json\"); d=json.loads(p.read_text()) if p.exists() else {}; print(\"main local settings exists:\", p.exists()); print(\"sandbox keys:\", sorted(d.get(\"sandbox\",{}))); print(\"hook counts:\", {k:sum(len(x.get(\"hooks\",[])) for x in v) for k,v in d.get(\"hooks\",{}).items()}); print(\"agmsg commands:\", [(k,h.get(\"command\", \"\").replace(str(pathlib.Path.home()),\"~\")) for k,v in d.get(\"hooks\",{}).items() for e in v for h in e.get(\"hooks\",[]) if \"agmsg/scripts/\" in h.get(\"command\", \"\")])'" in ~/Workspace/dotfiles
 succeeded in 78ms:
python3: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
python3: error: couldn't create cache file '/tmp/xcrun_db-iWiOCoIf' (errno=Operation not permitted)
python3: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
python3: error: couldn't create cache file '/tmp/xcrun_db-dLsCcV41' (errno=Operation not permitted)
main local settings exists: True
sandbox keys: []
hook counts: {'SessionStart': 1, 'SessionEnd': 1, 'Stop': 1}
agmsg commands: [('SessionStart', "'~/.agents/skills/agmsg/scripts/session-start.sh' 'claude-code' '~/Workspace/dotfiles'"), ('SessionEnd', "'~/.agents/skills/agmsg/scripts/session-end.sh' 'claude-code' '~/Workspace/dotfiles'"), ('Stop', "'~/.agents/skills/agmsg/scripts/check-inbox.sh' 'claude-code' '~/Workspace/dotfiles'")]

**Summarizing final key findings**
**Analyzing permission and ignore file issues**
exec
/bin/zsh -lc "sed -n '172,220p' home/dot_agents/agent-config.yaml; nl -ba .orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md | sed -n '64,97p'; nl -ba .orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md | sed -n '121,177p'" in ~/Workspace/dotfiles
 succeeded in 20ms:
        enabled: true
      crit@mryfmo-personal-plugins:hooks/hooks.json:stop:0:0:
        trusted_hash: sha256:bf6ad428ae7902810fa2d68d8db42228377af118aa18508ad0eccf73a95ed1f8
        enabled: true
      ponytail@ponytail:hooks/claude-codex-hooks.json:session_start:0:0:
        trusted_hash: sha256:7ee5d5ae1f4a9e55f1f429f2960c2f9f32293f198c0e8e2e42b2fb3b4eeda142
        enabled: true
      ponytail@ponytail:hooks/claude-codex-hooks.json:user_prompt_submit:0:0:
        trusted_hash: sha256:8c9efc5a5e649c8cdca3f0b7bf4cba81d9717d1bc930c7dbc18b6efd66c7c58c
        enabled: true
      ponytail@ponytail:hooks/claude-codex-hooks.json:subagent_start:0:0:
        trusted_hash: sha256:7954d675ef3bafd5e5a6073ae51d7de57a08f21340f241c332f99078e955675d
        enabled: true
  projects:
    "{{ .chezmoi.workingTree }}":
      trust_level: trusted

claude:
  settings_path: home/.chezmoitemplates/claude-settings-managed.json
  mcp_config_path: home/dot_claude/private_mcp.json.tmpl
  schema: https://json.schemastore.org/claude-code-settings.json
  # No effect on Fable 5 (thinking cannot be disabled there); applies when the
  # interactive profile maps to Sonnet or below.
  alwaysThinkingEnabled: true
  autoUpdates: false
  autoUpdatesChannel: stable
  plansDirectory: ./.agents/worklog/claude
  disableSkillShellExecution: true
  includeGitInstructions: true
  permissions:
    # This must be user-level: project settings do not honour auto; the Stop gate and deny list are the boundaries.
    defaultMode: auto
    # The only managed allow rule: agmsg-dispatch inserts one agmsg row and
    # sends a herdr wake, the sanctioned worker-to-orchestrator wake (T49).
    # It does not authorise chains: "Claude Code is aware of shell operators,
    # so a rule like `Bash(safe-cmd *)` won't give it permission to run the
    # command `safe-cmd && other-cmd`. ... A rule must match each subcommand
    # independently." (code.claude.com/docs/en/permissions)
    allow:
      - Bash(agmsg-dispatch:*)
    deny:
      - Bash(sudo:*)
      - Bash(rm -rf:*)
      - Read(.env.*)
      - Read(id_rsa*)
      - Read(id_ed25519*)
      - Edit(.env*)
      - Bash(curl * | sh)
      - Bash(wget * | sh)
    64	    disposition: "residual: the first document separators delimit format-2 metadata; the task-copy SHA256 binds the complete document."
    65	  - control: in-process effects
    66	    disposition: "residual: generation and tests use repository files and temporary fixtures; the worker performs no live deployment, login, permission-policy mutation or operator-session restart."
    67	  - control: workflow and interpreter or environment inputs
    68	    disposition: "residual: absolute interpreters, Python -I, sanitized Git and trusted executable bindings reduce environment injection; the host, native loader and same-UID processes remain outside this task's security guarantee."
    69	  - control: new or renamed scripts
    70	    disposition: "residual: the worker settings modify script, orchestrator-only guard and repository-owned Herdr state helper have named source and installed paths; RESULT inventories their interpreter and descendant bindings without introducing a worker-write-boundary hook or gh wrapper."
    71	  - control: "5.14 item 0: threat model"
    72	    disposition: "residual: host controls reduce accidental and injected damage and do not close a boundary between seats sharing one OS user; GitHub is the hard boundary, and approvals and gate evidence of record come from its API at a SHA inside the sandbox."
    73	  - control: "5.14 item 1: worker write controls"
    74	    disposition: "residual: dedicated configuration, symlink-aware Edit denies, restricted sandbox capabilities and failIfUnavailable true reduce damage; documented requested-path and resolved-target checks address static symlink redirection without claiming atomic immunity to a concurrent path swap."
    75	  - control: "5.14 item 2: sanitized environment and private executable PATH"
    76	    disposition: "residual: sanitized anchored Git enumeration and absolute hook interpreter bindings reduce injected configuration and shim execution; the remaining consuming-helper contracts belong to P1-14 a05, P1-10 a02, audit-pool-a02 and P1-6."
    77	  - control: "5.14 item 3: trusted-path checks"
    78	    disposition: "residual: canonical anchor and interpreter checks reduce worker-selected trusted paths and account for symlink components and filesystem case aliases; other consuming-helper checks remain with their owning hardening tasks."
    79	  - control: "5.14 item 4: verified executable and consumed-byte identity"
    80	    disposition: "residual: hooks execute their selected absolute interpreter and trusted script without rediscovery; evidence snapshots, last-use digest checks and their race limitations remain with the consuming orchestrator-side tasks."
    81	  - control: "5.14 item 5: output and reservation identity"
    82	    disposition: "residual: this task adds no reservation protocol; full-head output names, fixed-inode locks and physical-slot identity remain with the orchestrator-side tasks that create them."
    83	  - control: "5.14 item 6: honest residuals, hooks and MCP"
    84	    disposition: "residual: guarded project hooks, minimal worker delivery hooks and removal of the worker Herdr socket allowance reduce host execution routes; approved external processes and same-UID processes outside every seat sandbox remain residual."
    85	  - control: "5.14 item 7: trusted-execution verification"
    86	    disposition: "residual: this task records red-then-green render, merge, guard, launch, descendant and cache tests; P1-6 owns tests/unit/trusted_exec_contract.py and the consuming-helper contract tests."
    87	  - control: "5.14 item 8: committed approval ledger"
    88	    disposition: "residual: the regime reads the ledger through the GitHub contents API at the SHA returned by git ls-remote origin refs/heads/main; P1-14 a05 implements that read, and local refs, files and object traversal provide no approval authority."
    89	  - control: "5.14 item 9: private uv caches"
    90	    disposition: "residual: per-seat worker caches and restricted worker write allowances reduce cache poisoning; consuming hardening tasks use the protected orchestrator cache with --offline and execute no worker, shared uv or mise cache content."
    91	  - control: "5.14 item 10: no worker command outside the sandbox"
    92	    disposition: "residual: empty worker exclusions, disabled unsandboxed requests, absent Herdr socket allowance and Codex in-sandbox network reduce escape routes; the deterministic Codex permgate rule and live deployment remain operator steps."
    93	  - control: "hook failure policy"
    94	    disposition: "residual: every generated and tracked hook entry carries onFailure block, reducing fail-open behavior where Claude supports it; configuration tests cover missing-command and timeout policy, while background hooks and events on which the field has no effect carry no enforcement responsibility."
    95	  - control: orchestrator effect merge
    96	    disposition: "residual: the worker never merges; the orchestrator follows the final-head integration gate, required permission approval and pinned squash-merge procedure, with evidence of record retrieved from GitHub."
    97	  - control: orchestrator effect update-branch
   121	    sources:
   122	      - home/dot_local/bin/common/executable_herdr-agents
   123	      - home/dot_agents/agent-config.yaml
   124	    verification: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_every_worker_launch_receives_dedicated_policy_and_private_caches
   125	---
   126	
   127	# AGMSG-TASK dotfiles-T133-worker-write-boundary-a01 — plan 024 P1-15 under D-024-17, D-024-19, D-024-20 and D-024-21
   128	
   129	## Goal
   130	
   131	The host is not a security boundary between seats sharing one OS user. The regime's hard boundary is GitHub: protected main, required checks and merge through the orchestrator's identity. Approvals and gate evidence of record are read from GitHub at a SHA through its API inside the sandbox. Host-local controls in this task reduce accidental and injected damage. They do not establish isolation from a malicious same-UID process.
   132	
   133	This task implements section 5.14 items 1, 9 and 10 through a dedicated Claude worker configuration directory, Edit deny rules on trusted paths, guarded tracked project hooks, absolute hook interpreter bindings, private worker caches and sandboxed worker commands. Every Claude seat has `sandbox.failIfUnavailable: true`. Codex workers have `sandbox_workspace_write.network_access=true`.
   134	
   135	[memory:decision] D-024-20 makes this task the dispatch prerequisite of P1-14 a05, P1-10 a02, audit-pool-a02 and P1-6. The orchestrator places this task in their `after:` fields before dispatch. This task has `after: []`. A Codex seat performs these Claude configuration edits under the routing rule, including the Worker Playbook step 4 sentence permitted by plan 021 step 8.3.
   136	
   137	The design source is `.orchestration/plans/024-design-quality.md` section 5.14 items 0 through 10. D-024-21 and the amended items 0, 1 and 8 govern this revision. The acceptance record preserves the documentation facts and earlier proposals as history.
   138	
   139	The third C-80 text review is `.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-ecc7ab5.md.last.md`. Its five P1 findings remain recorded. This revision replaces the custom file-tool boundary hook with documented symlink-aware deny rules, moves approval reads out of the local object database, binds hook descendants to absolute interpreters, removes the worker Herdr socket allowance and specifies runtime-level hook failure policy.
   140	
   141	The file-tool rule is the documented sentence, “Deny rules: apply when either the requested path or the file it resolves to matches.” Edit and Write refuse a requested file that is itself a symlink. Directory symlinks are subject to resolved-target permission checks, and the tools check the resolved location again when opening the approved file. These documented checks address the preceding text's validation-only design. They do not establish an atomic host security boundary against concurrent same-UID changes. [Claude permission reference](https://code.claude.com/docs/en/permissions#symlinks)
   142	
   143	The 2026-10-19T03:45:06Z sandbox probe ran `gh api repos/mryfmo/dotfiles --jq .name` and returned `dotfiles`. The recorded sandbox proxy used CONNECT without TLS interception, and gh read the Keychain token. This is a historical host observation. It does not establish enforcement or credential readiness for the new worker directory on either platform.
   144	
   145	The documentation facts recorded at 03:2xZ establish that Edit denies also affect the Bash sandbox, hooks reload during a session and an unavailable sandbox is fail-open by default. D-024-21's 04:0xZ decision establishes the dedicated configuration mechanism, directory-specific credentials, symlink coverage and `onFailure: "block"` support. The earlier shared-user-hook proposal is superseded.
   146	
   147	## Files
   148	
   149	1. `home/dot_agents/agent-config.yaml` remains the source of agent policy and model profiles.
   150	
   151	   The manifest names `orchestrator_checkout` as the anchored primary checkout and supplies trusted deployment bindings for the guard, hook scripts and absolute interpreters. These bindings resolve outside worker worktrees and executable caches. Worker cwd, tool input, worktree configuration and inherited command variables do not select them.
   152	
   153	   The manifest defines a separate Claude worker settings output at `home/.chezmoitemplates/claude-worker-settings.json`. The worker configuration directory is `~/.claude-worker`. The launcher passes its expanded absolute path as `CLAUDE_CONFIG_DIR`.
   154	
   155	   The orchestrator policy retains its existing permissions, exclusions, socket access, cache allowances and hook functions. Its required policy changes are `failIfUnavailable: true` and `onFailure: "block"` on its hooks. The interpreter bindings required below preserve those hook functions.
   156	
   157	   The worker policy contains no excluded commands and sets `allowUnsandboxedCommands: false`. It contains no Herdr socket allowance and no allow-all Unix socket switch. Its sandbox is enabled and has `failIfUnavailable: true`.
   158	
   159	   Worker `sandbox.filesystem.allowWrite` contains only the existing agmsg store paths and per-seat cache paths. The worktree is the project root and supplies its ordinary project write root. Shared uv and mise write allowances are not copied into worker settings.
   160	
   161	   The Codex worker profile sets `sandbox_workspace_write.network_access=true`. Existing model selections and Codex shared Git grants retain their meaning. The deterministic Codex permgate rule that stops approving sandbox escapes is an operator step.
   162	
   163	2. `scripts/generate-agent-configs.py` renders the distinct orchestrator and worker baselines from the manifest.
   164	
   165	   The trusted-path deny inventory is generated at render time from the anchored checkout's tracked tree using `git ls-tree`. The inventory covers every top-level tracked path outside `.claude/worktrees/`. The `.claude` entry is expanded sufficiently to protect its tracked contents without emitting a parent deny that also denies worker worktrees. Directory and file entries receive patterns appropriate to their complete protected extent.
   166	
   167	   Anchored checkout rules use absolute `//` permission patterns. Rendering includes the trusted paths themselves and their descendants. It emits no checkout-wide parent deny that defeats the `.claude/worktrees/` exclusion.
   168	
   169	   Worker Edit denies also cover `~/.agents/**`, `~/.claude/**`, `~/.claude-worker/**`, `~/.local/**`, `~/.config/**`, `~/.cache/uv/**` and `~/.local/share/uv/**`. The rules protect the corresponding directory targets as well as their contents.
   170	
   171	   Edit denies cover Write, MultiEdit and NotebookEdit through Claude's permission system. Requested-path and resolved-target matching supply the documented symlink coverage. The generator does not create `executable_worker-write-boundary.py` or a replacement PreToolUse path validator.
   172	
   173	   Every direct Git verification introduced or changed by this task follows section 5.14 item 2. It begins with `env -i`, uses the selected absolute Git executable and an explicit `-C`, sets `GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL=/dev/null`, and supplies `-c core.hooksPath=/dev/null -c core.fsmonitor=false -c protocol.allow=never -c protocol.https.allow=always`. Diff and show also use `--no-ext-diff --no-textconv` and `-c core.attributesFile=/dev/null -c core.sshCommand=false`.
   174	
   175	   The private executable-link directory contains only links to selected absolute trusted binaries. Rendering rejects missing bindings, worker-controlled executable paths, shims, empty PATH entries and relative PATH entries. Python invocations use `-I`.
   176	
   177	   `tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_deny_inventory_uses_sanitized_anchored_git` records the exact Git environment and arguments. Its fixtures cover a newly tracked top-level path, tracked files, tracked directories, `.claude` children, the worktree exclusion and an anchor containing spaces.

web search: 
web search: 'GH_CONFIG_DIR'
**Reviewing agent and config protection**
**Checking acceptance permission references**
codex
deny 設定には二つの具体的な不整合があります。`~/.agents/**` の禁止は必要な agmsg store への書き込みも塞ぐ一方、追跡ファイルだけの列挙では checkout 内の `.agents/worklog/uv-cache` が漏れます。また、Claude の現行仕様では linked worktree も main checkout の local settings を読み込むため、専用 user settings だけでは実効 hook 集合を分離できません。

exec
/bin/zsh -lc "rg -n -A 60 '"'^## Completion'"' .orchestration/tasks/dotfiles-T133-permission-guard-gate-a05.md; nl -ba ~/.agents/skills/agmsg/scripts/session-start.sh | sed -n '48,59p'; nl -ba ~/.agents/skills/agmsg/scripts/check-inbox.sh | sed -n '136,149p'" in ~/Workspace/dotfiles
 succeeded in 32ms:
415:## Completion
416-
417-The existing branch `tools/permission-guard-gate-a01` continues PR #420 from `911f5202e61a2e46f527fcd9a4eda0041e97410a`. The first push replaces the a04 branch task copy with the byte-identical dispatched a05 copy. Seat a010 keeps its branch, fixes and evidence. The reset creates no second implementation PR. The missed `2026-10-19T03:00Z` deadline remains reported, and the orchestrator owns the new estimate.
418-
419-The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies with this task's existing branch, the qualifications below, `dotfiles-T133-permission-guard-gate-followup-a01` as the owner of any advisory P2, and `task_copy=<sha256 of .orchestration/dotfiles-T133-permission-guard-gate-a05/task.md>` in RESULT. The orchestrator writes the owner task before assigning its first advisory P2. The six reset defects and retained duplicate-rule defect belong to this task.
420-
421-Every worker-side fix round, before or after the first RESULT, counts toward INV-6 under C-61. Predecessor counters, the a03 Bot correction, its single CI-repair round, question PONGs, S2 withdrawal and a04 S1 stop remain historical records. They are not recast as approvals.
422-
423-The worker's own pre-push review is one round at most. A surviving P0/P1 is sent in RESULT as open and stops integration. The worker starts no further private correction-and-review cycle to avoid reporting it. Permitted later rounds remain subject to INV-6 and the inherited completion rule.
424-
425-No `@codex review` comment is posted. Automatic final-head reviews are observed within the bounded 15-minute window, and absence is recorded as `bot: none`. Required GitHub Actions checks pass before RESULT. Every feedback item carries its proposed disposition. Surviving P0/P1 findings remain open for the operator's decision.
426-
427-A Codex seat writes evidence at the same relative paths in its worktree and says so in RESULT. Worker review evidence uses the required `-worker-` infix. Agent-side review evidence and its receipt follow the repository's Crit-data rules without opening a browser review or asking the user to review.
428-
429-RESULT names the final head, base, branch, changed files, Bot findings and dispositions, every open P0/P1, exact test selectors, measured caps, all six new deployable scripts, the orch-gate.sh change, task-copy SHA256 and evidence paths with the SHA256 values consumed by the entrypoint. The report distinguishes predecessor observations from final-head closure and records the indirect-command-recognition residual, interpreter-launch premise, Claude-seat path-deny gap, same-UID process residual and unmitigated outside-sandbox gh exclusion owned by P1-15 under D-024-17. The orchestrator copies worktree evidence by absolute path before acceptance review.
430-
431-This task is `security: true`. Under C-80, a security-profile context reviews this complete a05 task text before dispatch. That review is a dispatch prerequisite rather than a claim made by this draft. The orchestrator also runs the task-level audit and a separate security-profile review on the final implementation head.
432-
433-The finding-class table includes `decision-not-bound-to-execution` and preserves the predecessor classes `argv-text-mismatch`, `unbound-evidence` and `fail-open-on-error`. A third non-advisory finding of one class stops the artifact for redesign. It never starts another instance-by-instance correction round. The acceptance record retains the required class search and re-plan evidence.
434-
435-Final-head feedback collection, task-level audit, finding dispositions, acceptance and the integration gate follow Orchestrator Playbook step 10 in its prescribed order. The gate receives `PR_FEEDBACK_EVIDENCE`, `AUDIT_EVIDENCE`, `ACCEPTANCE_EVIDENCE` and the agent review receipt. A changed head receives fresh required evidence. The security review of that final head precedes the gate.
436-
437-The deployed hook allows only the anchored tracked `integrate-merge.sh` invocation through updated input naming the verified realpath. The script itself runs each gh and git write as a separate command, without shell chaining. Callers submit the entrypoint as one command with its three arguments. The eventual merge is exactly `gh pr merge --squash --match-head-commit <audited head> <pr>`.
438-
439-Until PR #420 lands, strings carrying `gh pr merge` or `gh pr create` are written with the file-edit tool rather than Bash heredocs or echo. This includes test fixtures, reports and validation prose. The worker does not deploy the new hook or relax its tracked-main identity conditions to bootstrap this PR.
440-
441-## Checks (pasted by the orchestrator before each send)
442-
443-```
444-(pasted at dispatch)
445-```
446-
447-Local Bats, live payload execution and live deployment are not performed by this task; deployment remains unverified until the operator's post-merge checks.
448-Claude file tools, hooks and MCP processes retain the P1-15 path-deny gap, outside-sandbox gh has no present mitigation, and a same-UID process outside every seat sandbox remains residual.
    48	source "$SCRIPT_DIR/lib/type-registry.sh"
    49	# shellcheck disable=SC1091
    50	source "$SCRIPT_DIR/lib/role-session.sh"  # role->session reverse lookup (#339)
    51	# Only DEFINES agmsg_close_inherited_fds; nothing is closed here. The type
    52	# plug calls it inside a subshell around its own long-lived spawn, so this
    53	# shell's descriptors are untouched. See lib/close-fds.sh.
    54	source "$SCRIPT_DIR/lib/close-fds.sh"
    55	# shellcheck disable=SC1091
    56	source "$SCRIPT_DIR/lib/terminal-context-line.sh"
    57	
    58	# Identity sanity check — no point launching a watcher with an empty pair set.
    59	PAIRS=$("$SCRIPT_DIR/identities.sh" "$PROJECT" "$TYPE" 2>/dev/null || true)
   136	TEAM_LIST=()
   137	IDENTITIES_VALID=1
   138	while IFS=$'\t' read -r identity_team identity_agent identity_extra; do
   139	  if [ -z "$identity_team" ] || [ -z "$identity_agent" ] || [ -n "$identity_extra" ]; then
   140	    IDENTITIES_VALID=0
   141	    break
   142	  fi
   143	
   144	  [ -n "$AGENT" ] || AGENT="$identity_agent"
   145	  [ "$identity_agent" = "$AGENT" ] || continue
   146	
   147	  team_seen=0
   148	  # ${arr[@]+...} guards the empty-array expansion: under `set -u` bash 3.2
   149	  # (macOS default) treats "${TEAM_LIST[@]}" on an empty array as unbound.

**Reviewing final findings and configuration risks**
**Analyzing design inconsistencies and credential risks**

I'm examining how absolute paths for executables interact with environment PATH settings and launcher configurations, noting potential security concerns about trusted PATH usage and missing credential bindings in orchestrator identity. There’s a notable design gap where workers share GitHub credentials without strict separation, posing conditional but real risks.
codex
- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:131](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:131) No threat row or control separates worker GitHub credentials from the orchestrator’s: `CLAUDE_CONFIG_DIR` does not isolate gh authentication, so a worker with the shared credential can call the merge API through permitted sandbox networking; GitHub cannot enforce the claimed seat identity distinction. [gh credential selection](https://cli.github.com/manual/gh_help_environment).

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:165](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:165) The deny inventory trusts the same worker-writable Git objects and refs rejected for ledger authority: planted replacement refs can make `git ls-tree` omit protected paths, and neither `env -i` nor the prescribed flags authenticate that enumeration; the named fixtures omit this attack. [Git replacement semantics](https://git-scm.com/docs/git-replace).

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:267](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:267) The “protected” orchestrator cache is absent from the specified deny inventory: checkout-local `.agents/worklog/uv-cache` is gitignored, `.agents` is absent from the tracked top-level tree, and `~/.agents/**` names a different directory; `--offline` does not prevent execution of poisoned local cache content.

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:169](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:169) Denying all `~/.agents/**` also denies the required agmsg `db`, `teams`, `run` and `ext-tools` writes beneath it, contradicting line 159’s allowances and preventing sandboxed worker messaging; render tests that merely assert both lists cannot establish a functioning policy. [Combined sandbox enforcement](https://code.claude.com/docs/en/sandboxing#how-sandboxing-relates-to-permissions).

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:235](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:235) Preparing worktree-local delivery settings misses the main checkout’s local settings, which linked-worktree sessions also load and which currently contain unguarded agmsg hooks bound to the main project; dedicated user settings and tracked-hook guards therefore do not establish the promised effective hook set. [Local settings resolution](https://code.claude.com/docs/en/settings#where-claude-code-keeps-the-local-file-in-a-git-repository).

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:251](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:251) Absolute entrypoint interpreters cannot satisfy the descendant contract while installed agmsg scripts remain unchanged: `session-start.sh:59` directly executes `identities.sh`, whose shebang is `/usr/bin/env bash`; the text supplies no hook-runtime PATH binding that prevents this unsandboxed descendant from resolving through the host’s shims. [Shim resolution](https://mise.jdx.dev/dev-tools/shims.html).

📝 まとめ: Reviewed every threat row and the cited acceptance/review context; six findings remain for orchestrator disposition. No files changed.

Not checked: implementation, live enforcement or credential scopes; execution and authority binding remain unestablished.
Verdict: incorrect
hook: Stop
hook: Stop Completed
tokens used
116,180
- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:131](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:131) No threat row or control separates worker GitHub credentials from the orchestrator’s: `CLAUDE_CONFIG_DIR` does not isolate gh authentication, so a worker with the shared credential can call the merge API through permitted sandbox networking; GitHub cannot enforce the claimed seat identity distinction. [gh credential selection](https://cli.github.com/manual/gh_help_environment).

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:165](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:165) The deny inventory trusts the same worker-writable Git objects and refs rejected for ledger authority: planted replacement refs can make `git ls-tree` omit protected paths, and neither `env -i` nor the prescribed flags authenticate that enumeration; the named fixtures omit this attack. [Git replacement semantics](https://git-scm.com/docs/git-replace).

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:267](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:267) The “protected” orchestrator cache is absent from the specified deny inventory: checkout-local `.agents/worklog/uv-cache` is gitignored, `.agents` is absent from the tracked top-level tree, and `~/.agents/**` names a different directory; `--offline` does not prevent execution of poisoned local cache content.

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:169](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:169) Denying all `~/.agents/**` also denies the required agmsg `db`, `teams`, `run` and `ext-tools` writes beneath it, contradicting line 159’s allowances and preventing sandboxed worker messaging; render tests that merely assert both lists cannot establish a functioning policy. [Combined sandbox enforcement](https://code.claude.com/docs/en/sandboxing#how-sandboxing-relates-to-permissions).

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:235](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:235) Preparing worktree-local delivery settings misses the main checkout’s local settings, which linked-worktree sessions also load and which currently contain unguarded agmsg hooks bound to the main project; dedicated user settings and tracked-hook guards therefore do not establish the promised effective hook set. [Local settings resolution](https://code.claude.com/docs/en/settings#where-claude-code-keeps-the-local-file-in-a-git-repository).

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:251](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:251) Absolute entrypoint interpreters cannot satisfy the descendant contract while installed agmsg scripts remain unchanged: `session-start.sh:59` directly executes `identities.sh`, whose shebang is `/usr/bin/env bash`; the text supplies no hook-runtime PATH binding that prevents this unsandboxed descendant from resolving through the host’s shims. [Shim resolution](https://mise.jdx.dev/dev-tools/shims.html).

📝 まとめ: Reviewed every threat row and the cited acceptance/review context; six findings remain for orchestrator disposition. No files changed.

Not checked: implementation, live enforcement or credential scopes; execution and authority binding remain unestablished.
Verdict: incorrect
