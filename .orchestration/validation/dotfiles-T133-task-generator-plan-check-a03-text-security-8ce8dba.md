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
session id: 01a152ae-bc64-7cf2-b9ad-d373241b6328
--------
user
Pre-dispatch security review (read-only, security profile) of the task text .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a03.md and its threat_table, before any implementation exists. Judge the design the text states: can the controls it names bind what actually executes on this host (mise shims first on PATH, same-user worker processes, gh outside the sandbox on Linux, symlinks and case-insensitive filesystems, inherited GIT_* environment)? Check every threat row: a closed row whose named test cannot close it, a residual row whose control does not mitigate the risk, a missing row for a file or non-path control, and any gap of the class decision-not-bound-to-execution (a decision made on text or on a validated copy while the execution resolves binaries, files or ledgers from an attacker-influenced place). Read the related acceptance records and reviews the text cites for context. Report each finding as [P0-P3] <confidence> <file:line> <one line>; findings are input for the orchestrator, who decides. End with exactly one line: Verdict: correct or Verdict: incorrect.
warning: loading hooks from both ~/.codex/hooks.json and ~/.codex/config.toml; prefer a single representation for this layer
hook: SessionStart
hook: SessionStart
hook: SessionStart Completed
hook: SessionStart Completed
hook: UserPromptSubmit
hook: UserPromptSubmit Completed
codex
🤖 I read the AGENTS.md for mryfmo/dotfiles.
タスク本文、threat_table、引用された acceptance・レビューを読み、判断に使う対象と実際に実行・参照される対象が結び付いているかを確認します。agmsg-orchestration と Ponytail のスキルを適用し、読み取り専用で進めます。
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
/bin/zsh -lc 'nl -ba .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a03.md' in ~/Workspace/dotfiles
 succeeded in 0ms:
     1	---
     2	format: 2
     3	task_id: dotfiles-T133-task-generator-plan-check-a03
     4	kind: code
     5	security: true
     6	allowed_files:
     7	  - scripts/orchestrator/task-from-plan.py
     8	  - scripts/orchestrator/plan-check.py
     9	  - scripts/orchestrator/task-consistency-check.py
    10	  - scripts/orchestrator/task-template.md
    11	  - tests/unit/test_task_from_plan.py
    12	  - tests/unit/test_plan_check.py
    13	  - tests/unit/test_task_consistency_c11_c15.py
    14	  - tests/unit/test_regime_ci.py
    15	  - tests/unit/test_task_checkers.py
    16	  - .orchestration/dotfiles-T133-task-generator-plan-check-a03/**
    17	after: [dotfiles-T133-worker-write-boundary-a01]
    18	reset_of: [dotfiles-T133-task-generator-plan-check-a02]
    19	threat_table:
    20	  - control: "scripts/orchestrator/task-from-plan.py (plan data, bundled content, unverified command records and confined exclusive output creation)"
    21	    disposition: "residual: the generator executes no plan command and grants no premise authority to generated bytes; trusted subprocess execution and exclusive output creation reduce injected execution and overwrite risks without establishing same-UID host isolation."
    22	  - control: "scripts/orchestrator/plan-check.py (retained form, drift and invariant checks with confined glob enumeration)"
    23	    disposition: "residual: patterns and resolved matches remain under the inspected root, directory symlinks are not followed and subprocesses use trusted executable bindings; the twelve audit P2 retain their recorded owner."
    24	  - control: "scripts/orchestrator/task-consistency-check.py (shell-free C14 probe interpretation and the C11 pytest node-id grammar)"
    25	    disposition: "residual: C14 requires the orchestrator-supplied digest of the same parsed bytes, interprets only the fixed read-only probe vocabulary and starts only trusted absolute Git for its Git probe; unsupported forms fail with their text printed; C11 accepts the class form; trusted caller authority and same-UID host access remain residual."
    26	  - control: "scripts/orchestrator/task-template.md (bundled rows, unverified Check commands and Completion wording)"
    27	    disposition: "residual: bundled text supplies generation defaults without authorizing execution or inventing observations; generator fixtures verify its use without reading sibling task records."
    28	  - control: "tests/unit/test_task_from_plan.py (generation, command non-execution and exclusive output fixtures)"
    29	    disposition: "residual: temporary repositories and marker files demonstrate non-execution and refusal without touching live credentials, canonical records or deployment state."
    30	  - control: "tests/unit/test_plan_check.py (confined glob, retained form, stubbed drift and invariant fixtures)"
    31	    disposition: "residual: temporary roots and trusted fixture bindings exercise traversal and symlink refusals; fixtures contact no live GitHub service and establish no host isolation."
    32	  - control: "tests/unit/test_task_consistency_c11_c15.py (shell-free probe, uv launch, environment, digest and selector fixtures)"
    33	    disposition: "residual: adversarial fixtures reject executable premise forms, verify trusted Git and uv bindings and retain the inherited structural checks; hostile .venv and uv.toml fixtures establish selection behavior without establishing deployment; the original edited-file evidence defect remains with its owner."
    34	  - control: "tests/unit/test_regime_ci.py (retained a02 Amendment 1 fixture dispositions)"
    35	    disposition: "closed: tests/unit/test_regime_ci.py::RegimeCiTest::test_regime_ci_checks_only_the_latest_copy_of_a_reset_of_lineage"
    36	  - control: "tests/unit/test_task_checkers.py (retained historical fixture and expected-set edits)"
    37	    disposition: "residual: the inherited C4 fixture and justified C11 and C15 expected-set edits remain; the report explains any further change required by this reset's explicit contracts."
    38	  - control: ".orchestration/dotfiles-T133-task-generator-plan-check-a03/** (this reset's branch artifacts)"
    39	    disposition: "residual: artifacts identify historical observations, new red proofs and final-head results separately; acceptance compares the dispatched bytes, implementation, evidence and CI."
    40	  - control: "the task-file copy at .orchestration/dotfiles-T133-task-generator-plan-check-a03/task.md replaces .orchestration/dotfiles-T133-task-generator-plan-check-a02/task.md"
    41	    disposition: "residual: the first push deletes the named a02 copy and adds the byte-identical dispatched a03 copy; TASK and RESULT bind the a03 copy's own SHA256 and acceptance verifies the replacement."
    42	  - control: "the evidence records under .orchestration/dotfiles-T133-task-generator-plan-check-a03/ (report.md, validation.md, sandbox.md, learning.md, measure.md and worker review evidence)"
    43	    disposition: "residual: records preserve commands, stdout, stderr, exits, tested revisions and source hashes without secrets or unmasked home-directory paths; the final-head audit compares claims with the diff and CI."
    44	  - control: "task metadata (PR_FEEDBACK_EVIDENCE, AUDIT_EVIDENCE, ACCEPTANCE_EVIDENCE and REVIEW_EVIDENCE)"
    45	    disposition: "residual: structural checks and dispatched-byte comparison bind this task's scope; integration evidence binds the final head, and authoritative approval and gate evidence are obtained through GitHub at a SHA under the owning integration mechanisms."
    46	  - control: metadata separators
    47	    disposition: "residual: the first document separators delimit the YAML front matter and the task-copy digest covers the complete dispatched document."
    48	  - control: in-process effects
    49	    disposition: "residual: generation reads plan data and writes one confined new task file without running plan or Check commands; C14 interprets digest-authorized read-only probes without a shell and never executes premise text as code; plan-check writes no records."
    50	  - control: workflow and interpreter or environment inputs
    51	    disposition: "residual: no workflow changes occur; all subprocesses of the three scripts enter env -i with validated absolute executables and a private PATH, and Python uses -I; every uv launch by the three scripts and their tests uses --no-config --no-project --offline --python with an absolute trusted interpreter and the private UV_CACHE_DIR; native loaders and same-UID host processes remain trusted residuals."
    52	  - control: new or renamed scripts
    53	    disposition: "residual: the inherited two new Python scripts and bundled Markdown template remain the complete new production-file inventory; this reset adds no production file outside allowed_files."
    54	  - control: "5.14 item 0: host threat model"
    55	    disposition: "residual: these scripts run on the orchestrator host and execute nothing from an inspected checkout; host controls reduce accidental and injected damage rather than isolate same-UID seats; shared GitHub credentials leave the GitHub boundary as detection, not prevention, with P1-11 owning the missing-acceptance or gate-evidence main-push flag."
    56	  - control: "5.14 item 1: worker write controls"
    57	    disposition: "residual: Codex seat sandbox restrictions do not establish the Claude file-tool boundary; the claimed worker write controls take effect only after P1-15 is deployed by make update and verified; until then the manifest retains failIfUnavailable: false and the Linux gh exclusion, and Claude trusted-path protection remains residual; this task changes no seat settings, managed exclusions, Herdr socket allowance or permission policy."
    58	  - control: "5.14 item 2: sanitized environment and private executable PATH"
    59	    disposition: "residual: every subprocess starts under env -i, uses validated absolute executable paths and receives only the private trusted-binary PATH; every Git call carries the prescribed configuration and explicit -C; caller PATH, checkout bin directories and injected Git environment supply no executable authority."
    60	  - control: "5.14 item 3: trusted-path checks"
    61	    disposition: "residual: trusted executables, helpers, templates, snapshots and output destinations receive realpath checks, worker-root rejection and filesystem-appropriate identity comparison; worker exclusion from trusted paths applies only after P1-15 is deployed, while the current failIfUnavailable: false and Linux gh exclusion remain pre-deployment residuals; inspected data stays confined to its declared root, and concurrent same-UID replacement remains a host residual."
    62	  - control: "5.14 item 4: verified executable and consumed-byte identity"
    63	    disposition: "residual: validated executable realpaths are executed without rediscovery; consumed file snapshots have unique trusted-root names, mode 0600 and last-use digest checks; worker write protection of those bindings applies only after P1-15 is deployed, with the current failIfUnavailable: false and Linux gh exclusion residual until then; C14 parses and hashes the same bytes, and generation never promotes plan text into executable authority."
    64	  - control: "5.14 item 5: output and reservation identity"
    65	    disposition: "residual: task output creation uses O_EXCL and refuses existing files and symlinks; new head-specific resources use the full 40-character head; this task introduces no reservation protocol or physical-slot lock and claims no protection against every same-UID path race."
    66	  - control: "5.14 item 6: honest residuals"
    67	    disposition: "residual: trusted caller decisions, native execution, shared credentials, host processes outside seat sandboxes and concurrent filesystem changes remain explicit residuals; fixture success does not establish deployment or malicious-worker isolation."
    68	  - control: "5.14 item 7: trusted-execution verification"
    69	    disposition: "residual: the allowed test modules retain red-then-green cases for hostile PATH, injected Git environment and configuration, worker-root trusted paths and replacement before consumption; P1-6 owns tests/unit/trusted_exec_contract.py and this task does not create or modify that separately owned helper."
    70	  - control: "5.14 item 8: committed approval ledger"
    71	    disposition: "residual: these scripts make no permission approval or merge decision; the integration mechanism obtains the main SHA through git ls-remote and reads approval and gate evidence through the GitHub API at that SHA, with no local-file, local-ref or object-database substitute."
    72	  - control: "5.14 item 9: private uv caches"
    73	    disposition: "residual: every uv launch by the three scripts and their tests uses uv run --no-config --no-project --offline --python <absolute trusted interpreter from the trusted root> with UV_CACHE_DIR fixed to the anchored .agents/worklog/uv-cache; worker caches, shared uv caches and mise caches supply no trusted executable or dependency content; cache write protection applies only after P1-15 is deployed, while the current failIfUnavailable: false and Linux gh exclusion remain pre-deployment residuals."
    74	  - control: "5.14 item 10: worker commands remain inside the sandbox"
    75	    disposition: "residual: the requirement that every worker command, including gh and Git network writes, stays inside its sandbox becomes effective only after P1-15 is deployed and verified; until then the manifest retains failIfUnavailable: false and the Linux gh exclusion, so automatic unsandboxed execution remains possible; after deployment unavailable operations produce a blocked PONG and no exception or Herdr socket access authorizes escape."
    76	  - control: orchestrator effect merge
    77	    disposition: "residual: the worker has no merge assignment; the orchestrator follows Orchestrator Playbook step 10 and pins the squash merge to the audited final head, while shared credentials leave unauthorized merges detectable rather than prevented."
    78	  - control: orchestrator effect update-branch
    79	    disposition: "residual: an update-branch changes the head and requires fresh CI, feedback, audit and security-review evidence before acceptance and the integration gate."
    80	  - control: orchestrator effect forced worker removal
    81	    disposition: "residual: no forced removal is planned; existing dirty-worktree protections remain and acceptance records any operator-authorized discarded state."
    82	premises:
    83	  - claim: none of the five new files exists on origin/main
    84	    command: git ls-files scripts/orchestrator/task-from-plan.py scripts/orchestrator/plan-check.py tests/unit/test_task_from_plan.py tests/unit/test_plan_check.py tests/unit/test_task_consistency_c11_c15.py | wc -l
    85	    output: |-
    86	      0
    87	  - claim: the checker documents eleven checks today (C1 to C10 and C7b), so C11 to C15 are additions at the end of its list
    88	    command: /usr/bin/grep -c '^C[0-9]*b\? ' scripts/orchestrator/task-consistency-check.py
    89	    output: |-
    90	      11
    91	  - claim: the plan 024 group is eleven files (ten Markdown documents and the progress TSV), the set plan-check reads
    92	    command: /bin/ls .orchestration/plans/024-*.md .orchestration/plans/024-progress.tsv | wc -l
    93	    output: |-
    94	      11
    95	  - claim: the todo table has fifteen P1 rows, the rows task-from-plan reads
    96	    command: /usr/bin/grep -c '^| P1-' .orchestration/plans/024-todo.md
    97	    output: |-
    98	      15
    99	  - claim: tests/unit/test_task_checkers.py is in flight in PR #413, so the new checks get their own test module
   100	    command: git ls-files tests/unit/test_task_checkers.py | wc -l
   101	    output: |-
   102	      1
   103	---
   104	
   105	# AGMSG-TASK dotfiles-T133-task-generator-plan-check-a03 — S1 reset of dotfiles-T133-task-generator-plan-check-a02 on PR #417 (plan 024 P1-12; seat a009, worker-c)
   106	
   107	This text is the independent redesign by a review-profile context other than the author of a02. Plan 006 S1 stopped a02 at 2026-10-19T04:34Z after its security review found three P1 of class `decision-not-bound-to-execution` and one P2 glob-confinement defect. Its task-level audit found twelve P2. The worker had reached the C-61 cap through one pre-push review round and one CI-repair round.
   108	
   109	The source records are `.orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a02.md`, `.orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-security-8a09b93.md.last.md` and `.orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-audit-8a09b93.md.last.md`. The acceptance record's `decision-not-bound-to-execution` replan supplies this reset's specification, design, implementation and verification boundary.
   110	
   111	The pre-dispatch C-80 review at `.orchestration/validation/dotfiles-T133-task-generator-plan-check-a03-text-security-f6797ab.md.last.md` returned `Verdict: incorrect` with three P1. This revision applies the orchestrator's fixed-probe, uv-launch and P1-15 deployment decisions and amended section 5.14 items 2 and 9.
   112	
   113	Seat a009 in worker-c continues branch `tools/task-generator-plan-check-a01` and PR #417 from `8a09b9365932f23b09df8aa2385a93d0b3016a3e`. The a02 implementation stays. This reset changes the execution and path contracts stated below and adds the C11 selector correction. Its dependency is `dotfiles-T133-worker-write-boundary-a01`. Dispatch follows that task's merge, deployment with `make update` and verification of the effective worker boundary. The sandbox statements in this text become effective only after P1-15 is deployed. Before deployment, the manifest's `failIfUnavailable: false` and Linux `gh *` exclusion remain residuals.
   114	
   115	The first push deletes `.orchestration/dotfiles-T133-task-generator-plan-check-a02/task.md` and adds the byte-identical dispatched text at `.orchestration/dotfiles-T133-task-generator-plan-check-a03/task.md`. The orchestrator directs that exact predecessor-copy deletion as reset bookkeeping outside `allowed_files`. Every other worker edit stays within `allowed_files`. One branch and one implementation PR carry this reset.
   116	
   117	The a01 and a02 task texts, acceptance history, evidence, amendments and counters remain historical records. The five premises above are copied from a02 verbatim and describe their original write-time observations. Fresh validation identifies the actual tested root and revision and reports drift without rewriting those observations. C14 interprets existing dispatched `premises[].command` lines through the fixed vocabulary below. A historical form outside that vocabulary fails C14 with the form printed and receives no shell fallback.
   118	
   119	## Goal
   120	
   121	The generator produces a format-2 task skeleton from one plan todo row using the bundled template, proposed file scope and unverified command text. It executes no plan command. The orchestrator separately runs commands it trusts and records their observations.
   122	
   123	The consistency checker retains its structural, disposition, concrete-scope and invariant checks, accepts the regime's pytest node-id selectors and interprets C14 premises only for the orchestrator-authorized task bytes through a fixed read-only probe vocabulary without a shell. The plan checker retains its form, drift and invariant reporting while refusing glob traversal outside its inspected root.
   124	
   125	Section 5.14 items 0 through 10 of `.orchestration/plans/024-design-quality.md` apply by reference. Items 2, 3 and 4 govern all three scripts and every subprocess they start. The inspected checkout root supplies data and supplies no executable trust. Trusted executable, helper, template and snapshot bindings come from the orchestrator's trusted root independently of the inspected checkout and caller environment.
   126	
   127	Every subprocess starts under `env -i`. Its PATH contains only a private directory of links to absolute binaries resolved and validated in the trusted root. Checkout `<root>/bin`, caller PATH, shims, empty PATH entries and relative PATH entries supply no executable selection. The selected executable runs by its validated realpath without another lookup. Python runs with `-I`.
   128	
   129	Every uv launch performed by the three scripts and their tests uses `uv run --no-config --no-project --offline --python <absolute trusted interpreter from the trusted root>`. `UV_CACHE_DIR` is fixed to the anchored checkout's `.agents/worklog/uv-cache` under section 5.14 item 9. The uv executable and interpreter are validated absolute realpaths from the trusted root. The uv command notation in this text denotes that absolute executable under the clean launch environment. Current-directory and parent-directory `.venv` discovery and uv configuration discovery supply no interpreter, dependency or executable authority.
   130	
   131	Every Git call uses an explicit `-C`, `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `-c core.hooksPath=/dev/null`, `-c core.fsmonitor=false`, `-c protocol.allow=never` and `-c protocol.https.allow=always`. Diff and show additionally use `--no-ext-diff`, `--no-textconv`, `-c core.attributesFile=/dev/null` and `-c core.sshCommand=false`. Inherited `GIT_*`, loader and interpreter environment variables do not enter the clean environment.
   132	
   133	Git filter commands (`filter.<name>.clean`, `filter.<name>.process` and `filter.<name>.smudge`) are defined only in configuration files and never in the tree's `.gitattributes`. With `GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL=/dev/null`, the effective configuration includes the checkout's local configuration file, the worktree-scoped `config.worktree` when `extensions.worktreeConfig` is set, and every include the local file pulls in. Before every Git invocation by the three scripts, including the clean-plan status check, the scripts first verify that `git -C <checkout> config --show-origin --get-regexp '^filter\.'` prints nothing under the section 5.14 item 2 environment and the same trusted Git launch contract. The scripts refuse on any match with the origin and key printed before any status or diff runs. Every status invocation uses `git --no-optional-locks status`.
   134	
   135	Trusted paths receive realpath checks and reject `.claude/worktrees/` and manifest worker roots. Comparisons account for symlink components and case-insensitive filesystem identity. Validated file content passed to a consuming process uses a uniquely named mode-0600 snapshot under the trusted root and a SHA256 recheck immediately before consumption. Evidence records the digests of inputs used for decisions.
   136	
   137	These controls reduce accidents and prompt injection. Same-UID processes, shared GitHub credentials and host execution outside seat sandboxes remain residuals. The GitHub boundary is detection, not prevention, until the operator establishes separate-user or separate-host isolation under future P1-16. P1-11 owns the main-push flag for a merge lacking acceptance or gate-passage evidence.
   138	
   139	## Files
   140	
   141	1. `scripts/orchestrator/task-consistency-check.py` applies the trusted execution contract to Git probes and replaces C14 shell execution with fixed read-only probe interpretation.
   142	
   143	   C14 retains the existing `--premises-sha <sha256>` gate. It hashes and parses the same file bytes. Only the orchestrator supplies the trusted dispatched digest. A missing or mismatching digest executes no premise command and retains the explicit `C14: not run (no trusted sha)` warning. Acceptance does not authorize branch commands by calculating a replacement trusted digest from the branch copy.
   144	
   145	   An authorized premise is exactly `git rev-parse <ref>`, `test -e <path>`, `test -f <path>` or `grep -c <pattern> <path>`. The checker interprets the existing command field itself without a shell. It starts no premise subprocess except the validated absolute Git for `git rev-parse <ref>`, with every section 5.14 item 2 Git flag and explicit `-C` naming the inspected checkout. The ref is a single revision operand and supplies no Git options.
   146	
   147	   The checker implements both test forms itself after resolving the path under the inspected checkout and refusing a realpath outside that checkout. The checker implements grep itself as a fixed-string count of matching lines in a file whose realpath remains under the checkout. Patterns are literal data and supply no regular-expression, option or shell authority. Shell expansion, pipelines, redirection, command substitution and command chaining are not probe forms.
   148	
   149	   Every other premise form fails C14 with the form printed. `python -I scripts/probe.py`, `source ./x.sh`, arbitrary Git subcommands and legacy shell pipelines are rejected without execution. A trusted task digest authorizes only interpretation of this vocabulary and grants no authority to execute checkout-controlled file operands.
   150	
   151	   Whitespace normalization and output-mismatch findings retain their a02 behavior for supported probes. Unsupported forms fail rather than becoming network skip notes or absent-tool warnings. The missing or mismatching digest warning still runs no probe. Successful structural checks remain distinct from premise verification. Existing C10 literals remain pattern operands after `git grep -e`, and the C6 design-path confinement remains.
   152	
   153	   `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c14_interprets_the_probe_vocabulary_without_a_shell` is written first and is red against `8a09b9365932f23b09df8aa2385a93d0b3016a3e`. Its valid-hash fixture verifies the Git, test and grep probe forms, including both test flags. Premises `python -I scripts/probe.py` and `source ./x.sh` fail with their forms printed and create no marker. A fake PATH fails on every executable other than Git, and subprocess assertions establish that premise evaluation starts no subprocess other than the trusted absolute Git. Its cases cover fixed-string counting, confined path resolution, unsupported forms, the sanitized environment, prescribed Git flags, rejected worker-root trusted bindings and consumed-byte identity. It is green on the final implementation.
   154	
   155	2. `scripts/orchestrator/task-from-plan.py` retains its CLI, committed plan-group reads, bundled template, whole-token wave selection, program-item extraction, scope proposals, grep provenance and threat-row generation.
   156	
   157	   The clean-plan check remains a data-provenance check for staged, unstaged and untracked changes in the `024-*` group. A clean committed HEAD supplies no authorization to execute its plan text.
   158	
   159	   The generator never executes a command extracted from a plan item. It also never executes bundled or plan-derived Check commands. It records each recognized command as text with an explicit `verify:` explanation that execution and verification remain pending. It fabricates no stdout or exit status and distinguishes a missing observation from an observed empty output.
   160	
   161	   The generator creates no scratch worktree for Check execution. The former premise runner, scratch Check runner and their execution-only cleanup disappear. Trusted Git calls needed to read committed data and obtain provenance remain under the common execution contract.
   162	
   163	   The generator invokes the trusted consistency checker without `--premises-sha`. It does not turn its own computed output digest into permission to execute generated premise text. Structural findings and the C14 not-run warning remain visible. The generated file remains available for editing when structural findings occur.
   164	
   165	   `scripts/orchestrator/task-template.md` retains the bundled task-copy, evidence, non-path and orchestrator-effect rows, common Check command text and Completion contract. Its wording describes unverified commands and separate orchestrator verification. It makes no claim that generation ran those commands.
   166	
   167	   Existing generation tests change their execution expectations only where this reset changes the contract. Recognized commands remain present as unverified text. The separately owned command-recognition and parser defects remain outside this task.
   168	
   169	   `tests/unit/test_task_from_plan.py::TaskFromPlanTest::test_the_generator_never_executes_a_plan_command` is written first and is red against `8a09b9365932f23b09df8aa2385a93d0b3016a3e`. A clean committed plan and bundled Check content contain marker-writing commands. Generation retains their text and unverified status, creates no marker and no scratch worktree, and passes no trusted premise digest to the checker. It is green on the final implementation.
   170	
   171	3. `scripts/orchestrator/task-from-plan.py` confines its output to `<root>/.orchestration/tasks/` and creates the destination with `O_EXCL`.
   172	
   173	   The generator resolves the root, task directory and destination through realpath before creation. A destination resolving outside the task directory is refused. An existing destination is refused. An existing symlink is refused, including a dangling symlink and a symlink whose target remains inside the task directory.
   174	
   175	   Exclusive creation supplies the final leaf-existence check. The generator writes the generated bytes through the exclusively created file and does not reopen the destination through a following write. Refusal leaves existing files, symlink targets and outside-root markers unchanged.
   176	
   177	   The destination's confinement and exclusive creation reduce redirection and truncation risks. Concurrent parent-directory replacement by a same-UID process remains the item 0 host residual.
   178	
   179	   `tests/unit/test_task_from_plan.py::TaskFromPlanTest::test_the_generator_refuses_a_symlinked_or_existing_output` is written first and is red against `8a09b9365932f23b09df8aa2385a93d0b3016a3e`. It covers an existing ordinary file, existing and dangling symlinks, an outside destination, symlinked parent traversal and successful creation of a fresh confined output. Existing target bytes remain unchanged. It is green on the final implementation.
   180	
   181	4. `scripts/orchestrator/plan-check.py` retains the eleven-file plan scope, F1 to F6 reporting, timestamped acceptance drift, per-occurrence PR comparisons and forbidden-pattern checks.
   182	
   183	   Every glob is interpreted under `--root`. The checker validates the pattern's confinement before enumeration and realpath-checks resolved matches before inspecting or reporting them. An absolute or traversal pattern escaping the root produces a violation. A resolved path outside the root produces a violation.
   184	
   185	   Enumeration does not follow directory symlinks, including directory symlinks whose targets remain inside the root. It does not recursively enter a symlink before checking the resulting path. Outside-root filenames are not collected for overlap diagnostics.
   186	
   187	   Existing concrete overlap detection and literal-versus-glob treatment remain. Drift uses trusted read-only gh execution under the common subprocess contract. The script writes no records and retains exit 1 for violations and exit 0 for a clean result.
   188	
   189	   `tests/unit/test_plan_check.py::PlanCheckTest::test_globs_never_resolve_outside_root` is written first and is red against `8a09b9365932f23b09df8aa2385a93d0b3016a3e`. It covers absolute and parent-traversal globs, directory symlinks, outside-resolving matches and an ordinary confined overlap. Marker and diagnostic assertions establish that outside paths were not traversed or disclosed. It is green on the final implementation.
   190	
   191	5. `scripts/orchestrator/task-consistency-check.py` accepts `closed:` payloads shaped as `tests/<path>::<test>` and `tests/<path>::<Class>::<test>`.
   192	
   193	   Each class and test segment remains an identifier. Malformed selectors remain findings. The existing `out-of-scope:` task-id check, `residual:` minimum length and C13 form grammar remain.
   194	
   195	   The C11 and C14 docstrings state their revised contracts. C1 to C10, C7b, C12, C13 and C15 retain their implemented behavior apart from the shared subprocess hardening. The known audit P2 remain recorded with their owner.
   196	
   197	   `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c11_accepts_the_pytest_node_id_with_a_class` is written first and is red against `8a09b9365932f23b09df8aa2385a93d0b3016a3e`. The byte-identical a02 task copy at that head is the class-form red fixture. The fixture is checked under a filename matching its task id so that a C1 filename mismatch cannot supply the red result. It runs without `--premises-sha` and establishes its red result through C11's selector finding, with the C14 not-run warning recorded separately. The test also retains the function form and malformed-selector rejection. It is green on the final implementation.
   198	
   199	The inherited fixture repairs in `tests/unit/test_regime_ci.py` remain. The inherited narrowly scoped edits in `tests/unit/test_task_checkers.py` remain. Tests in the three dedicated modules reuse the existing temporary-repository fixtures and trusted fixture bindings without placing fakes first on the production executable PATH. C14 fixtures requiring successful premise verification use the fixed vocabulary. Unsupported-form fixtures assert C14 failure. Historical task-copy fixtures retain their bytes and receive no trusted digest for structural-only checks.
   200	
   201	`tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_uv_launches_ignore_a_hostile_venv_and_uv_config` is written first and is red against `8a09b9365932f23b09df8aa2385a93d0b3016a3e`. A fixture checkout contains a hostile `.venv` directory and hostile `uv.toml`. The test exercises uv launches performed by the three scripts and their tests, verifies the complete required argument vector and private `UV_CACHE_DIR`, and establishes that the trusted absolute interpreter is selected while the hostile environment and configuration are never selected. It is green on the final implementation.
   202	
   203	`tests/unit/test_task_from_plan.py::TaskFromPlanTest::test_all_three_scripts_refuse_repository_local_filters_before_status_or_diff` is written first. The marker regression plants three fixtures: a local `filter.probe.clean`, a worktree-scoped `filter.probe.clean` in `config.worktree` with `extensions.worktreeConfig` set, and an included file carrying `filter.probe.clean`. Each fixture has a `.gitattributes` line selecting that filter for a tracked fixture file. The filter command writes a marker if executed. The test asserts that all three scripts refuse in all three fixtures with the matching origins and keys printed before any status or diff runs and that the marker remains absent. The worktree-scoped and included-file fixtures are red against the current text's `--local` check, and all three fixtures are red against `8a09b9365932f23b09df8aa2385a93d0b3016a3e`. It is green on the final implementation.
   204	
   205	The named tests contain the applicable section 5.14 item 7 cases for each mechanism: a planted PATH shim does not execute, planted Git environment and configuration do not affect execution, worker-root trusted paths are refused, and replaced content does not reach a consumer as previously validated bytes. P1-6 owns the common trusted-execution helper. This task adds no separately owned helper file.
   206	
   207	The a03 evidence directory contains the dispatched `task.md`, `report.md`, `validation.md`, `sandbox.md`, `learning.md`, `measure.md` and worker review evidence. The report maps the four a02 security findings, C11 correction and four a03 pre-dispatch P1 to the implementation, exact selectors, dependency deployment evidence and fix commits. It distinguishes retained a02 behavior from changed contracts and remaining owner findings.
   208	
   209	## Out of scope
   210	
   211	The twelve findings `audit:8a09b93:1` through `audit:8a09b93:12` remain owned by `dotfiles-T133-task-generator-plan-check-followup-a01`. They are not reproduced as implementation items in this reset. The orchestrator dispatches that owner task after this task merges.
   212	
   213	The owner records retain the C15 local-design acceptance finding, C12 agent-instruction coverage and scope-confinement findings, generator root-file omission, directory-with-child rows, path normalization, unavailable single-word command recognition, plan-check F1 completion-cell parsing, the edited-file SHA test defect, the selector-grammar row, the bundled-template feedback disposition and the parser-gap search evidence.
   214	
   215	This reset supplies the explicitly required C11 interface correction. The owner retains its selector-grammar row and consumes this reset's fix evidence instead of implementing the same correction again. The orchestrator reconciles that record before dispatching the owner. The parser-gap lineage rows and replan remain with that owner.
   216	
   217	`scripts/orchestrator/dispatch.sh` remains unchanged. Its trusted-SHA argument and successful-warning forwarding remain in the P1-5 to P1-6 dispatch lineage following `dotfiles-T133-result-precheck-a03`. The report identifies that pending integration and does not claim that this task wires dispatch.
   218	
   219	The regime job and validate wiring remain P1-11. `reset-task.sh` remains the later C-69 item. `ruleset-request.sh`, `ruleset-verify.sh`, permission-policy changes and integration authority remain with their existing owners.
   220	
   221	Canonical task texts, plan files, progress records, acceptance records, owner task texts and approval ledgers remain outside the worker's edit boundary. The orchestrator performs reset and ownership bookkeeping. The exact predecessor-copy deletion stated above is the sole directed exception.
   222	
   223	Seat configuration, administrative managed settings, credential separation, agmsg hardening, reservation locks, live deployment and sandbox-escape policy remain outside this task. The scripts read inspected checkout data without treating local records, refs or objects as permission approval or integration authority.
   224	
   225	## Check
   226	
   227	`.orchestration/dotfiles-T133-task-generator-plan-check-a03/validation.md` contains commands, verbatim stdout and stderr, exit statuses and tested revisions for `make unit-test`, `make format` and `uv run --no-config --no-project --offline --python <absolute trusted interpreter from the trusted root> python -m unittest tests.unit.test_task_from_plan tests.unit.test_plan_check tests.unit.test_task_consistency_c11_c15 tests.unit.test_task_checkers -v`.
   228	
   229	The four task modules are green. The retained regime fixture repair is verified with `uv run --no-config --no-project --offline --python <absolute trusted interpreter from the trusted root> python -m unittest tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_checks_only_the_latest_copy_of_a_reset_of_lineage -v`.
   230	
   231	The seven new selectors are the complete pytest node ids stated in Files. Validation records each selector's red and green execution and the corresponding unittest class and method invocation. The complete final module runs remain required.
   232	
   233	Each new regression runs its current test source against production code at `8a09b9365932f23b09df8aa2385a93d0b3016a3e` before the corresponding fix and passes on the final implementation. Each proof records the production revision, regression-source SHA256, exact command, output and exit status. A missing method, import error, unavailable runner or zero-test run does not establish a red regression.
   234	
   235	An inherited full-suite or formatting failure is reproduced against the unchanged base in the same sandbox and recorded with that comparison. It is not labelled green or repaired outside `allowed_files`. Final-head required GitHub Actions checks pass before RESULT.
   236	
   237	The checker run is `uv run --no-config --no-project --offline --python <absolute trusted interpreter from the trusted root> --with pyyaml python -I scripts/orchestrator/task-consistency-check.py .orchestration/tasks/dotfiles-T133-*.md`. Validation preserves its complete output and exit status. C1 to C15 and C7b are accounted for separately from warnings and known owner findings.
   238	
   239	Without `--premises-sha`, C14 is recorded as not run with its warning. An authorized rerun uses only the orchestrator's trusted dispatched digest, interprets only the fixed read-only probe vocabulary and preserves its actual output. A premise outside the vocabulary fails with the form printed. Acceptance does not calculate a replacement trusted digest from branch data. Historical premise drift and unsupported historical forms are reported with the tested root and revision.
   240	
   241	The plan checker runs once as `uv run --no-config --no-project --offline --python <absolute trusted interpreter from the trusted root> --with pyyaml python -I scripts/orchestrator/plan-check.py`. Its output and exit status are preserved. Real-plan violations remain reported for the orchestrator. Dedicated fixtures exercise `--drift` and `--invariants` without live GitHub access.
   242	
   243	Orchestrator-side executions of these commands use the section 5.14 trusted launch environment, selected absolute executables, private `UV_CACHE_DIR` and the complete uv launch flags stated above. Every uv launch in the three scripts and their tests uses those flags and the absolute trusted interpreter. Worker-side validation remains inside the worker sandbox after P1-15 is deployed. Before deployment, `failIfUnavailable: false` and the Linux `gh *` exclusion remain residuals, and this task is not dispatched. Evidence records the full actual invocation, trusted interpreter realpath, cache path and execution context.
   244	
   245	The cap comparison base is `b22a5580`. At `8a09b9365932f23b09df8aa2385a93d0b3016a3e`, the inherited diff against that base measures 659 changed lines outside `tests/` and `.orchestration/` and 673 changed lines under `tests/`.
   246	
   247	The complete final diff against `b22a5580` has at most 800 changed lines outside `tests/` and `.orchestration/` and at most 900 changed lines under `tests/`. Changed lines are additions plus deletions. The totals include inherited a01 and a02 changes, fixtures and the bundled template. The reset does not restart the measurement at `8a09b936`.
   248	
   249	Validation includes `git diff --numstat b22a5580 HEAD` and `git diff --numstat origin/main...HEAD`, executed through the prescribed trusted Git invocation. `measure.md` and RESULT record the comparison identities, per-file numstat, both totals and the complete changed-file inventory.
   250	
   251	The orchestrator checks the canonical a03 text and verifies the merged P1-15 dependency's deployment with `make update` and effective sandbox settings before dispatch, and checks the task-copy replacement and byte identity at acceptance. A C-80 security-profile context reviews this complete text before dispatch. A passing C-80 result is a dispatch prerequisite and is recorded separately from this draft.
   252	
   253	Local Bats tests do not run. GitHub Actions supplies any required Bats result.
   254	
   255	## Completion
   256	
   257	One branch, `tools/task-generator-plan-check-a01`, continues PR #417 from `8a09b9365932f23b09df8aa2385a93d0b3016a3e`. The first push contains the a02 task-copy deletion and this text's byte-identical a03 copy. No second implementation branch or PR is created.
   258	
   259	The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies with this task's scope, explicit comparison base, 800/900 caps, continuing branch and review restrictions. This text's continuation, automatic-review window and prohibition on a requested Codex review govern this reset.
   260	
   261	`dotfiles-T133-task-generator-plan-check-followup-a01` owns every advisory P2 assigned from this task and retains the twelve a02 audit P2. The orchestrator records each advisory ownership disposition against the existing owner task before integration and reconciles the C11 fix evidence before dispatching that owner after this merge.
   262	
   263	RESULT carries `task_copy=<sha256 of .orchestration/dotfiles-T133-task-generator-plan-check-a03/task.md>`. It carries `precheck=<the precheck evidence hash>` when PR #411 has merged and the applicable precheck has run. It otherwise carries `precheck=pending-411`.
   264	
   265	RESULT names the final head, base, branch, changed files, new production-file inventory, exact test selectors, red and green evidence, both measured caps, feedback dispositions and evidence paths. It names the trusted execution root, executable realpaths, private PATH construction, Git flags, fixed probe forms, complete uv launch arguments, private cache, consumed-input digests, verified P1-15 deployment and remaining deployment residuals. It identifies the dispatch SHA and warning-forwarding integration as externally owned.
   266	
   267	The worker's own pre-push review is one round at most. A P0 or P1 surviving that round appears in RESULT as open and goes to the orchestrator for the operator's decision. An inherited Bot P0/P1 receives its actual root-cause disposition or remains open. A surviving thread is reported as `open:<thread id>`, and a review-body finding as `open:review-<review id>`.
   268	
   269	Every worker-side fix round counts toward INV-6. The worker starts no additional private correction-and-review cycle before RESULT. The a01 and a02 stopped histories and amendment accounting remain recorded. A third non-advisory finding of one class stops the artifact under plan 006 and requires the recorded search and redesign procedure.
   270	
   271	A Codex seat writes evidence at the required relative paths in its own worktree and states that location in RESULT. Worker review evidence uses the required `-worker-` infix. The orchestrator copies worktree evidence by absolute path before acceptance. Evidence distinguishes inherited observations, new red proofs and final-head green results.
   272	
   273	Crit review remains agent-side. Crit-data evidence and its receipt follow repository rules without a browser review or a human review request.
   274	
   275	This task is `security: true`. The orchestrator obtains the task-level audit and a separate security-profile review on the final head. The final-head security review precedes the integration gate.
   276	
   277	Final-head CI, the complete feedback sweep, finding dispositions, task-level audit, acceptance record and gate follow Orchestrator Playbook step 10 in its prescribed order. The gate receives `PR_FEEDBACK_EVIDENCE`, `AUDIT_EVIDENCE`, `ACCEPTANCE_EVIDENCE` and the required agent review receipt. A changed head receives fresh required evidence.
   278	
   279	The orchestrator runs `make require-crit-review` with the required review evidence before completion and uses the integration evidence required by step 10 before merging. Merge uses `gh pr merge --squash --match-head-commit <audited head>` after the gate. The worker has no merge assignment.
   280	
   281	No `@codex review` comment is posted. Automatic final-head reviews are observed within the bounded 15-minute window. Absence is recorded as `bot: none`. Every feedback item has its proposed disposition, and surviving P0/P1 findings remain open for the operator's decision.
   282	
   283	Every gh command and every Git write runs as a single separate command without shell chaining or a wrapper combining writes. Every worker command remains inside its sandbox after P1-15 is deployed and its effective settings are verified. The current `failIfUnavailable: false` and Linux `gh *` exclusion remain residuals before that deployment and do not satisfy this statement. A permission denial or unavailable operation produces a blocked PONG with the exact command, output and boundary. An alternate command or API does not bypass the denial.
   284	
   285	Until P1-14 lands, any string containing the words `gh pr merge` or `gh pr create` is written with the file-edit tool, never in a Bash heredoc or `echo`.
   286	
   287	The report states the user-visible changes. Generation no longer executes plan or Check commands and records them as unverified. Existing output files and symlinks are refused. C14 interprets fixed read-only probes without a shell, uv launches ignore checkout virtual environments and configuration through explicit trusted selection, C11 accepts class-qualified selectors and plan-check refuses escaping globs without following directory symlinks. Merge alone establishes no deployment result.
   288	
   289	## Checks (pasted by the orchestrator before each send)
   290	
   291	```
   292	(pasted at dispatch)
   293	```
   294	
   295	Local Bats, live deployment and the owner's twelve audit P2 remain outside this task.
   296	Same-UID host access and shared GitHub credentials remain residual risks.
exec
/bin/zsh -lc "sed -n '1,155p' .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a03.md | nl -ba" in ~/Workspace/dotfiles
 succeeded in 0ms:
     1	---
     2	format: 2
     3	task_id: dotfiles-T133-task-generator-plan-check-a03
     4	kind: code
     5	security: true
     6	allowed_files:
     7	  - scripts/orchestrator/task-from-plan.py
     8	  - scripts/orchestrator/plan-check.py
     9	  - scripts/orchestrator/task-consistency-check.py
    10	  - scripts/orchestrator/task-template.md
    11	  - tests/unit/test_task_from_plan.py
    12	  - tests/unit/test_plan_check.py
    13	  - tests/unit/test_task_consistency_c11_c15.py
    14	  - tests/unit/test_regime_ci.py
    15	  - tests/unit/test_task_checkers.py
    16	  - .orchestration/dotfiles-T133-task-generator-plan-check-a03/**
    17	after: [dotfiles-T133-worker-write-boundary-a01]
    18	reset_of: [dotfiles-T133-task-generator-plan-check-a02]
    19	threat_table:
    20	  - control: "scripts/orchestrator/task-from-plan.py (plan data, bundled content, unverified command records and confined exclusive output creation)"
    21	    disposition: "residual: the generator executes no plan command and grants no premise authority to generated bytes; trusted subprocess execution and exclusive output creation reduce injected execution and overwrite risks without establishing same-UID host isolation."
    22	  - control: "scripts/orchestrator/plan-check.py (retained form, drift and invariant checks with confined glob enumeration)"
    23	    disposition: "residual: patterns and resolved matches remain under the inspected root, directory symlinks are not followed and subprocesses use trusted executable bindings; the twelve audit P2 retain their recorded owner."
    24	  - control: "scripts/orchestrator/task-consistency-check.py (shell-free C14 probe interpretation and the C11 pytest node-id grammar)"
    25	    disposition: "residual: C14 requires the orchestrator-supplied digest of the same parsed bytes, interprets only the fixed read-only probe vocabulary and starts only trusted absolute Git for its Git probe; unsupported forms fail with their text printed; C11 accepts the class form; trusted caller authority and same-UID host access remain residual."
    26	  - control: "scripts/orchestrator/task-template.md (bundled rows, unverified Check commands and Completion wording)"
    27	    disposition: "residual: bundled text supplies generation defaults without authorizing execution or inventing observations; generator fixtures verify its use without reading sibling task records."
    28	  - control: "tests/unit/test_task_from_plan.py (generation, command non-execution and exclusive output fixtures)"
    29	    disposition: "residual: temporary repositories and marker files demonstrate non-execution and refusal without touching live credentials, canonical records or deployment state."
    30	  - control: "tests/unit/test_plan_check.py (confined glob, retained form, stubbed drift and invariant fixtures)"
    31	    disposition: "residual: temporary roots and trusted fixture bindings exercise traversal and symlink refusals; fixtures contact no live GitHub service and establish no host isolation."
    32	  - control: "tests/unit/test_task_consistency_c11_c15.py (shell-free probe, uv launch, environment, digest and selector fixtures)"
    33	    disposition: "residual: adversarial fixtures reject executable premise forms, verify trusted Git and uv bindings and retain the inherited structural checks; hostile .venv and uv.toml fixtures establish selection behavior without establishing deployment; the original edited-file evidence defect remains with its owner."
    34	  - control: "tests/unit/test_regime_ci.py (retained a02 Amendment 1 fixture dispositions)"
    35	    disposition: "closed: tests/unit/test_regime_ci.py::RegimeCiTest::test_regime_ci_checks_only_the_latest_copy_of_a_reset_of_lineage"
    36	  - control: "tests/unit/test_task_checkers.py (retained historical fixture and expected-set edits)"
    37	    disposition: "residual: the inherited C4 fixture and justified C11 and C15 expected-set edits remain; the report explains any further change required by this reset's explicit contracts."
    38	  - control: ".orchestration/dotfiles-T133-task-generator-plan-check-a03/** (this reset's branch artifacts)"
    39	    disposition: "residual: artifacts identify historical observations, new red proofs and final-head results separately; acceptance compares the dispatched bytes, implementation, evidence and CI."
    40	  - control: "the task-file copy at .orchestration/dotfiles-T133-task-generator-plan-check-a03/task.md replaces .orchestration/dotfiles-T133-task-generator-plan-check-a02/task.md"
    41	    disposition: "residual: the first push deletes the named a02 copy and adds the byte-identical dispatched a03 copy; TASK and RESULT bind the a03 copy's own SHA256 and acceptance verifies the replacement."
    42	  - control: "the evidence records under .orchestration/dotfiles-T133-task-generator-plan-check-a03/ (report.md, validation.md, sandbox.md, learning.md, measure.md and worker review evidence)"
    43	    disposition: "residual: records preserve commands, stdout, stderr, exits, tested revisions and source hashes without secrets or unmasked home-directory paths; the final-head audit compares claims with the diff and CI."
    44	  - control: "task metadata (PR_FEEDBACK_EVIDENCE, AUDIT_EVIDENCE, ACCEPTANCE_EVIDENCE and REVIEW_EVIDENCE)"
    45	    disposition: "residual: structural checks and dispatched-byte comparison bind this task's scope; integration evidence binds the final head, and authoritative approval and gate evidence are obtained through GitHub at a SHA under the owning integration mechanisms."
    46	  - control: metadata separators
    47	    disposition: "residual: the first document separators delimit the YAML front matter and the task-copy digest covers the complete dispatched document."
    48	  - control: in-process effects
    49	    disposition: "residual: generation reads plan data and writes one confined new task file without running plan or Check commands; C14 interprets digest-authorized read-only probes without a shell and never executes premise text as code; plan-check writes no records."
    50	  - control: workflow and interpreter or environment inputs
    51	    disposition: "residual: no workflow changes occur; all subprocesses of the three scripts enter env -i with validated absolute executables and a private PATH, and Python uses -I; every uv launch by the three scripts and their tests uses --no-config --no-project --offline --python with an absolute trusted interpreter and the private UV_CACHE_DIR; native loaders and same-UID host processes remain trusted residuals."
    52	  - control: new or renamed scripts
    53	    disposition: "residual: the inherited two new Python scripts and bundled Markdown template remain the complete new production-file inventory; this reset adds no production file outside allowed_files."
    54	  - control: "5.14 item 0: host threat model"
    55	    disposition: "residual: these scripts run on the orchestrator host and execute nothing from an inspected checkout; host controls reduce accidental and injected damage rather than isolate same-UID seats; shared GitHub credentials leave the GitHub boundary as detection, not prevention, with P1-11 owning the missing-acceptance or gate-evidence main-push flag."
    56	  - control: "5.14 item 1: worker write controls"
    57	    disposition: "residual: Codex seat sandbox restrictions do not establish the Claude file-tool boundary; the claimed worker write controls take effect only after P1-15 is deployed by make update and verified; until then the manifest retains failIfUnavailable: false and the Linux gh exclusion, and Claude trusted-path protection remains residual; this task changes no seat settings, managed exclusions, Herdr socket allowance or permission policy."
    58	  - control: "5.14 item 2: sanitized environment and private executable PATH"
    59	    disposition: "residual: every subprocess starts under env -i, uses validated absolute executable paths and receives only the private trusted-binary PATH; every Git call carries the prescribed configuration and explicit -C; caller PATH, checkout bin directories and injected Git environment supply no executable authority."
    60	  - control: "5.14 item 3: trusted-path checks"
    61	    disposition: "residual: trusted executables, helpers, templates, snapshots and output destinations receive realpath checks, worker-root rejection and filesystem-appropriate identity comparison; worker exclusion from trusted paths applies only after P1-15 is deployed, while the current failIfUnavailable: false and Linux gh exclusion remain pre-deployment residuals; inspected data stays confined to its declared root, and concurrent same-UID replacement remains a host residual."
    62	  - control: "5.14 item 4: verified executable and consumed-byte identity"
    63	    disposition: "residual: validated executable realpaths are executed without rediscovery; consumed file snapshots have unique trusted-root names, mode 0600 and last-use digest checks; worker write protection of those bindings applies only after P1-15 is deployed, with the current failIfUnavailable: false and Linux gh exclusion residual until then; C14 parses and hashes the same bytes, and generation never promotes plan text into executable authority."
    64	  - control: "5.14 item 5: output and reservation identity"
    65	    disposition: "residual: task output creation uses O_EXCL and refuses existing files and symlinks; new head-specific resources use the full 40-character head; this task introduces no reservation protocol or physical-slot lock and claims no protection against every same-UID path race."
    66	  - control: "5.14 item 6: honest residuals"
    67	    disposition: "residual: trusted caller decisions, native execution, shared credentials, host processes outside seat sandboxes and concurrent filesystem changes remain explicit residuals; fixture success does not establish deployment or malicious-worker isolation."
    68	  - control: "5.14 item 7: trusted-execution verification"
    69	    disposition: "residual: the allowed test modules retain red-then-green cases for hostile PATH, injected Git environment and configuration, worker-root trusted paths and replacement before consumption; P1-6 owns tests/unit/trusted_exec_contract.py and this task does not create or modify that separately owned helper."
    70	  - control: "5.14 item 8: committed approval ledger"
    71	    disposition: "residual: these scripts make no permission approval or merge decision; the integration mechanism obtains the main SHA through git ls-remote and reads approval and gate evidence through the GitHub API at that SHA, with no local-file, local-ref or object-database substitute."
    72	  - control: "5.14 item 9: private uv caches"
    73	    disposition: "residual: every uv launch by the three scripts and their tests uses uv run --no-config --no-project --offline --python <absolute trusted interpreter from the trusted root> with UV_CACHE_DIR fixed to the anchored .agents/worklog/uv-cache; worker caches, shared uv caches and mise caches supply no trusted executable or dependency content; cache write protection applies only after P1-15 is deployed, while the current failIfUnavailable: false and Linux gh exclusion remain pre-deployment residuals."
    74	  - control: "5.14 item 10: worker commands remain inside the sandbox"
    75	    disposition: "residual: the requirement that every worker command, including gh and Git network writes, stays inside its sandbox becomes effective only after P1-15 is deployed and verified; until then the manifest retains failIfUnavailable: false and the Linux gh exclusion, so automatic unsandboxed execution remains possible; after deployment unavailable operations produce a blocked PONG and no exception or Herdr socket access authorizes escape."
    76	  - control: orchestrator effect merge
    77	    disposition: "residual: the worker has no merge assignment; the orchestrator follows Orchestrator Playbook step 10 and pins the squash merge to the audited final head, while shared credentials leave unauthorized merges detectable rather than prevented."
    78	  - control: orchestrator effect update-branch
    79	    disposition: "residual: an update-branch changes the head and requires fresh CI, feedback, audit and security-review evidence before acceptance and the integration gate."
    80	  - control: orchestrator effect forced worker removal
    81	    disposition: "residual: no forced removal is planned; existing dirty-worktree protections remain and acceptance records any operator-authorized discarded state."
    82	premises:
    83	  - claim: none of the five new files exists on origin/main
    84	    command: git ls-files scripts/orchestrator/task-from-plan.py scripts/orchestrator/plan-check.py tests/unit/test_task_from_plan.py tests/unit/test_plan_check.py tests/unit/test_task_consistency_c11_c15.py | wc -l
    85	    output: |-
    86	      0
    87	  - claim: the checker documents eleven checks today (C1 to C10 and C7b), so C11 to C15 are additions at the end of its list
    88	    command: /usr/bin/grep -c '^C[0-9]*b\? ' scripts/orchestrator/task-consistency-check.py
    89	    output: |-
    90	      11
    91	  - claim: the plan 024 group is eleven files (ten Markdown documents and the progress TSV), the set plan-check reads
    92	    command: /bin/ls .orchestration/plans/024-*.md .orchestration/plans/024-progress.tsv | wc -l
    93	    output: |-
    94	      11
    95	  - claim: the todo table has fifteen P1 rows, the rows task-from-plan reads
    96	    command: /usr/bin/grep -c '^| P1-' .orchestration/plans/024-todo.md
    97	    output: |-
    98	      15
    99	  - claim: tests/unit/test_task_checkers.py is in flight in PR #413, so the new checks get their own test module
   100	    command: git ls-files tests/unit/test_task_checkers.py | wc -l
   101	    output: |-
   102	      1
   103	---
   104	
   105	# AGMSG-TASK dotfiles-T133-task-generator-plan-check-a03 — S1 reset of dotfiles-T133-task-generator-plan-check-a02 on PR #417 (plan 024 P1-12; seat a009, worker-c)
   106	
   107	This text is the independent redesign by a review-profile context other than the author of a02. Plan 006 S1 stopped a02 at 2026-10-19T04:34Z after its security review found three P1 of class `decision-not-bound-to-execution` and one P2 glob-confinement defect. Its task-level audit found twelve P2. The worker had reached the C-61 cap through one pre-push review round and one CI-repair round.
   108	
   109	The source records are `.orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a02.md`, `.orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-security-8a09b93.md.last.md` and `.orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-audit-8a09b93.md.last.md`. The acceptance record's `decision-not-bound-to-execution` replan supplies this reset's specification, design, implementation and verification boundary.
   110	
   111	The pre-dispatch C-80 review at `.orchestration/validation/dotfiles-T133-task-generator-plan-check-a03-text-security-f6797ab.md.last.md` returned `Verdict: incorrect` with three P1. This revision applies the orchestrator's fixed-probe, uv-launch and P1-15 deployment decisions and amended section 5.14 items 2 and 9.
   112	
   113	Seat a009 in worker-c continues branch `tools/task-generator-plan-check-a01` and PR #417 from `8a09b9365932f23b09df8aa2385a93d0b3016a3e`. The a02 implementation stays. This reset changes the execution and path contracts stated below and adds the C11 selector correction. Its dependency is `dotfiles-T133-worker-write-boundary-a01`. Dispatch follows that task's merge, deployment with `make update` and verification of the effective worker boundary. The sandbox statements in this text become effective only after P1-15 is deployed. Before deployment, the manifest's `failIfUnavailable: false` and Linux `gh *` exclusion remain residuals.
   114	
   115	The first push deletes `.orchestration/dotfiles-T133-task-generator-plan-check-a02/task.md` and adds the byte-identical dispatched text at `.orchestration/dotfiles-T133-task-generator-plan-check-a03/task.md`. The orchestrator directs that exact predecessor-copy deletion as reset bookkeeping outside `allowed_files`. Every other worker edit stays within `allowed_files`. One branch and one implementation PR carry this reset.
   116	
   117	The a01 and a02 task texts, acceptance history, evidence, amendments and counters remain historical records. The five premises above are copied from a02 verbatim and describe their original write-time observations. Fresh validation identifies the actual tested root and revision and reports drift without rewriting those observations. C14 interprets existing dispatched `premises[].command` lines through the fixed vocabulary below. A historical form outside that vocabulary fails C14 with the form printed and receives no shell fallback.
   118	
   119	## Goal
   120	
   121	The generator produces a format-2 task skeleton from one plan todo row using the bundled template, proposed file scope and unverified command text. It executes no plan command. The orchestrator separately runs commands it trusts and records their observations.
   122	
   123	The consistency checker retains its structural, disposition, concrete-scope and invariant checks, accepts the regime's pytest node-id selectors and interprets C14 premises only for the orchestrator-authorized task bytes through a fixed read-only probe vocabulary without a shell. The plan checker retains its form, drift and invariant reporting while refusing glob traversal outside its inspected root.
   124	
   125	Section 5.14 items 0 through 10 of `.orchestration/plans/024-design-quality.md` apply by reference. Items 2, 3 and 4 govern all three scripts and every subprocess they start. The inspected checkout root supplies data and supplies no executable trust. Trusted executable, helper, template and snapshot bindings come from the orchestrator's trusted root independently of the inspected checkout and caller environment.
   126	
   127	Every subprocess starts under `env -i`. Its PATH contains only a private directory of links to absolute binaries resolved and validated in the trusted root. Checkout `<root>/bin`, caller PATH, shims, empty PATH entries and relative PATH entries supply no executable selection. The selected executable runs by its validated realpath without another lookup. Python runs with `-I`.
   128	
   129	Every uv launch performed by the three scripts and their tests uses `uv run --no-config --no-project --offline --python <absolute trusted interpreter from the trusted root>`. `UV_CACHE_DIR` is fixed to the anchored checkout's `.agents/worklog/uv-cache` under section 5.14 item 9. The uv executable and interpreter are validated absolute realpaths from the trusted root. The uv command notation in this text denotes that absolute executable under the clean launch environment. Current-directory and parent-directory `.venv` discovery and uv configuration discovery supply no interpreter, dependency or executable authority.
   130	
   131	Every Git call uses an explicit `-C`, `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `-c core.hooksPath=/dev/null`, `-c core.fsmonitor=false`, `-c protocol.allow=never` and `-c protocol.https.allow=always`. Diff and show additionally use `--no-ext-diff`, `--no-textconv`, `-c core.attributesFile=/dev/null` and `-c core.sshCommand=false`. Inherited `GIT_*`, loader and interpreter environment variables do not enter the clean environment.
   132	
   133	Git filter commands (`filter.<name>.clean`, `filter.<name>.process` and `filter.<name>.smudge`) are defined only in configuration files and never in the tree's `.gitattributes`. With `GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL=/dev/null`, the effective configuration includes the checkout's local configuration file, the worktree-scoped `config.worktree` when `extensions.worktreeConfig` is set, and every include the local file pulls in. Before every Git invocation by the three scripts, including the clean-plan status check, the scripts first verify that `git -C <checkout> config --show-origin --get-regexp '^filter\.'` prints nothing under the section 5.14 item 2 environment and the same trusted Git launch contract. The scripts refuse on any match with the origin and key printed before any status or diff runs. Every status invocation uses `git --no-optional-locks status`.
   134	
   135	Trusted paths receive realpath checks and reject `.claude/worktrees/` and manifest worker roots. Comparisons account for symlink components and case-insensitive filesystem identity. Validated file content passed to a consuming process uses a uniquely named mode-0600 snapshot under the trusted root and a SHA256 recheck immediately before consumption. Evidence records the digests of inputs used for decisions.
   136	
   137	These controls reduce accidents and prompt injection. Same-UID processes, shared GitHub credentials and host execution outside seat sandboxes remain residuals. The GitHub boundary is detection, not prevention, until the operator establishes separate-user or separate-host isolation under future P1-16. P1-11 owns the main-push flag for a merge lacking acceptance or gate-passage evidence.
   138	
   139	## Files
   140	
   141	1. `scripts/orchestrator/task-consistency-check.py` applies the trusted execution contract to Git probes and replaces C14 shell execution with fixed read-only probe interpretation.
   142	
   143	   C14 retains the existing `--premises-sha <sha256>` gate. It hashes and parses the same file bytes. Only the orchestrator supplies the trusted dispatched digest. A missing or mismatching digest executes no premise command and retains the explicit `C14: not run (no trusted sha)` warning. Acceptance does not authorize branch commands by calculating a replacement trusted digest from the branch copy.
   144	
   145	   An authorized premise is exactly `git rev-parse <ref>`, `test -e <path>`, `test -f <path>` or `grep -c <pattern> <path>`. The checker interprets the existing command field itself without a shell. It starts no premise subprocess except the validated absolute Git for `git rev-parse <ref>`, with every section 5.14 item 2 Git flag and explicit `-C` naming the inspected checkout. The ref is a single revision operand and supplies no Git options.
   146	
   147	   The checker implements both test forms itself after resolving the path under the inspected checkout and refusing a realpath outside that checkout. The checker implements grep itself as a fixed-string count of matching lines in a file whose realpath remains under the checkout. Patterns are literal data and supply no regular-expression, option or shell authority. Shell expansion, pipelines, redirection, command substitution and command chaining are not probe forms.
   148	
   149	   Every other premise form fails C14 with the form printed. `python -I scripts/probe.py`, `source ./x.sh`, arbitrary Git subcommands and legacy shell pipelines are rejected without execution. A trusted task digest authorizes only interpretation of this vocabulary and grants no authority to execute checkout-controlled file operands.
   150	
   151	   Whitespace normalization and output-mismatch findings retain their a02 behavior for supported probes. Unsupported forms fail rather than becoming network skip notes or absent-tool warnings. The missing or mismatching digest warning still runs no probe. Successful structural checks remain distinct from premise verification. Existing C10 literals remain pattern operands after `git grep -e`, and the C6 design-path confinement remains.
   152	
   153	   `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c14_interprets_the_probe_vocabulary_without_a_shell` is written first and is red against `8a09b9365932f23b09df8aa2385a93d0b3016a3e`. Its valid-hash fixture verifies the Git, test and grep probe forms, including both test flags. Premises `python -I scripts/probe.py` and `source ./x.sh` fail with their forms printed and create no marker. A fake PATH fails on every executable other than Git, and subprocess assertions establish that premise evaluation starts no subprocess other than the trusted absolute Git. Its cases cover fixed-string counting, confined path resolution, unsupported forms, the sanitized environment, prescribed Git flags, rejected worker-root trusted bindings and consumed-byte identity. It is green on the final implementation.
   154	
   155	2. `scripts/orchestrator/task-from-plan.py` retains its CLI, committed plan-group reads, bundled template, whole-token wave selection, program-item extraction, scope proposals, grep provenance and threat-row generation.

exec
/bin/zsh -lc "rg -n -A 48 -B 3 'Codex seat worklogs' ~/.agents/skills/agmsg-orchestration/SKILL.md; cat ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail/SKILL.md" in ~/Workspace/dotfiles
 succeeded in 0ms:
214-    - Fix P0/P1 findings, inline or review-body, in at most one worker-side fix round before RESULT, then request `@codex review` and restart the wait from the push. A P0/P1 surviving that round is not fixed again: send `AGMSG-RESULT … bot_rounds=2` with each listed as `open:<thread id>` (`open:review-<review id>` for a review-body finding); this stops the PR for the operator's decision, and the next bullet's `fixed:`/`not-applicable:` rule does not override it.
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
250-
251-## Pitfalls
252-
253-- Do not start work from the agmsg message alone; read `task_file` first.
254-- Do not edit outside `allowed_files`, even for convenient cleanup.
255-- Do not perform forbidden actions such as dependency changes, gate changes, product changes, promotion decisions, image builds, or LLM calls when listed.
256-- Do not collapse candidate, promoted, rejected, and merged skill registry states into one directory.
257-- Do not put secrets, raw logs with credentials, or unredacted AutoSkill inputs in artifacts.
258-- Do not wake workers with `pane send-text` + `send-keys Enter`; use `agmsg-dispatch`, `poke.sh --body-file`, or `send.sh --body-file` as step 6 selects, and verify `read_at` in messages.db.
259-- Do not treat `AGMSG-ACCEPTANCE status=revise` as a new task unless it changes the task file or explicitly provides a next action.
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

**Reviewing context briefly**
exec
/bin/zsh -lc 'cat .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a02.md' in ~/Workspace/dotfiles
exec
/bin/zsh -lc "sed -n '155,180p' .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a03.md; cat .orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md" in ~/Workspace/dotfiles
exec
/bin/zsh -lc 'cat .orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-security-8a09b93.md.last.md; cat .orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-audit-8a09b93.md.last.md; cat .orchestration/validation/dotfiles-T133-task-generator-plan-check-a03-text-security-f6797ab.md.last.md' in ~/Workspace/dotfiles
exec
/bin/zsh -lc "rg -n -A 100 '"'^## 5.14|''^### 5.14'"' .orchestration/plans/024-design-quality.md" in ~/Workspace/dotfiles
exec
/bin/zsh -lc 'git --no-optional-locks status --short; if test -f .ua/meta.json; then cat .ua/meta.json; fi; git rev-parse HEAD' in ~/Workspace/dotfiles
 succeeded in 111ms:
---
{
  "audit_findings": [
    {
      "evidence": "grep -n 'Owned by dotfiles-T133-task-generator-plan-check-followup-a01' .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a02.md",
      "n": "1",
      "reason": "not-applicable: advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (implementation: C15 accepts a locally present design absent from origin/main); the a02 has reached the C-61 cap (one pre-push review round, one CI-repair round) and the audit found no P0/P1"
    },
    {
      "evidence": "grep -n 'Owned by dotfiles-T133-task-generator-plan-check-followup-a01' .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a02.md",
      "n": "2",
      "reason": "not-applicable: advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (implementation: C12 excludes agent instruction files such as .claude/skills/*/SKILL.md); the a02 has reached the C-61 cap (one pre-push review round, one CI-repair round) and the audit found no P0/P1"
    },
    {
      "evidence": "grep -n 'Owned by dotfiles-T133-task-generator-plan-check-followup-a01' .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a02.md",
      "n": "3",
      "reason": "not-applicable: advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (implementation: an out-of-checkout scope skips C12 instead of a confinement finding); the a02 has reached the C-61 cap (one pre-push review round, one CI-repair round) and the audit found no P0/P1"
    },
    {
      "evidence": "grep -n 'Owned by dotfiles-T133-task-generator-plan-check-followup-a01' .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a02.md",
      "n": "4",
      "reason": "not-applicable: advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (implementation: task-from-plan.py drops explicitly named repository-root files); the a02 has reached the C-61 cap (one pre-push review round, one CI-repair round) and the audit found no P0/P1"
    },
    {
      "evidence": "grep -n 'Owned by dotfiles-T133-task-generator-plan-check-followup-a01' .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a02.md",
      "n": "5",
      "reason": "not-applicable: advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (implementation: a directory scope with its child yields a C7b-rejected row); the a02 has reached the C-61 cap (one pre-push review round, one CI-repair round) and the audit found no P0/P1"
    },
    {
      "evidence": "grep -n 'Owned by dotfiles-T133-task-generator-plan-check-followup-a01' .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a02.md",
      "n": "6",
      "reason": "not-applicable: advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (implementation: paths are not normalized (./scripts/new.py)); the a02 has reached the C-61 cap (one pre-push review round, one CI-repair round) and the audit found no P0/P1"
    },
    {
      "evidence": "grep -n 'Owned by dotfiles-T133-task-generator-plan-check-followup-a01' .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a02.md",
      "n": "7",
      "reason": "not-applicable: advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (implementation: unavailable single-word commands are discarded); the a02 has reached the C-61 cap (one pre-push review round, one CI-repair round) and the audit found no P0/P1"
    },
    {
      "evidence": "grep -n 'Owned by dotfiles-T133-task-generator-plan-check-followup-a01' .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a02.md",
      "n": "8",
      "reason": "not-applicable: advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (implementation: plan-check F1 mistakes the work cell for the completion cell); the a02 has reached the C-61 cap (one pre-push review round, one CI-repair round) and the audit found no P0/P1"
    },
    {
      "evidence": "grep -n 'Owned by dotfiles-T133-task-generator-plan-check-followup-a01' .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a02.md",
      "n": "9",
      "reason": "not-applicable: advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (implementation: the edited-file test recomputes the SHA instead of rejecting changed bytes); the a02 has reached the C-61 cap (one pre-push review round, one CI-repair round) and the audit found no P0/P1"
    },
    {
      "evidence": "uv run --no-project --with pyyaml python -I <PR checker> --root <repo> .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a02.md (pasted in the record)",
      "n": "10",
      "reason": "not-applicable: C11 rejects the tests/<module>::<Class>::<test> selector form the regime uses everywhere (dispositions test: refutations, verdict, every task text); the grammar is the defect, not the texts: the first owned row of dotfiles-T133-task-generator-plan-check-followup-a01 widens C11 to the pytest node-id form with an optional class segment; until it lands, dispatch.sh runs the checker from main as before this PR (the orchestrator sequences the owner fix immediately after this merge)"
    },
    {
      "evidence": "grep -n '4306960626' .agents/worklog/orchestrator-glue/417-extra.tsv .orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-pr-feedback.json",
      "n": "11",
      "reason": "not-applicable: corrected in the sweep input: 417-extra.tsv now dispositions thread 4306960626 as fixed:eb20d063 (the bundled-template fix), superseding fixed:b3c6b7ea (the error-message improvement); the sweep JSON regenerates on the chain re-run"
    },
    {
      "evidence": "grep -n 'search:' .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a02.md; grep -l 'parser-gap' .orchestration/learning/mistakes/*.md",
      "n": "12",
      "reason": "not-applicable: corrected in this record: the parser-gap class (four lineage rows) carries its re-plan in the JSON replans object and the pasted search line below (no mistake record carries the slug yet; M-20261019-04 is written for it)"
    }
  ],
  "dispatch": [
    "AGMSG-TASK v1 task_id=dotfiles-T133-task-generator-plan-check-a02 round=1 reset_of=dotfiles-T133-task-generator-plan-check-a01 repo=~/Workspace/dotfiles/.claude/worktrees/worker-c task_file=.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a02.md task_sha256=a3ab8ea6addda207fa9a9ff5d96921e080dab7a1025117f33cbd087e6b805f98 deadline=none done_signal=AGMSG-RESULT note=a009:INV-6-reset-of-a01(the-fifteen-audit-findings-as-items,the-bundled-template,the-C14-sha-gate,item-20-the-checker-hardening)"
  ],
  "format": 1,
  "head": "8a09b9365932f23b09df8aa2385a93d0b3016a3e",
  "ledger": [
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
      "class": "trust-boundary-pr-input",
      "id": "4306960622"
    },
    {
      "class": "missing-input-crash",
      "id": "4306960626"
    },
    {
      "class": "string-form-comparison",
      "id": "4306960630"
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
    }
  ],
  "pr": 417,
  "replans": {
    "decision-not-bound-to-execution": {
      "design": "design 5.14 items 2, 3 and 4 applied to task-consistency-check.py, task-from-plan.py and plan-check.py: env -i with a private PATH of absolute trusted-root binaries (never <root>/bin), realpath checks that refuse outputs or globs resolving outside the checkout, O_EXCL output creation that refuses an existing symlink, and the C11 node-id grammar",
      "implementation": "the a03 reset of P1-12 on the same branch (PR #417): the a02 implementation stays, the three security P1 and the P2 traversal become items with red-then-green tests, C11 accepts tests/<path>::<Class>::<test>; the twelve audit P2 stay with the owner dotfiles-T133-task-generator-plan-check-followup-a01",
      "specification": "the checker and the generator execute nothing from a checkout-controlled place: premise commands run only for a text whose sha256 the orchestrator supplied and under a trusted interpreter and PATH; plan commands are never executed by the generator (it records them as text); outputs are written through a symlink-checked path inside .orchestration/tasks/",
      "verification": "red against 8a09b936: a checkout bin/bash is never executed by C14; a plan command is never executed by the generator; a symlinked output path is refused; a traversal glob is refused; the a02 copy passes C11"
    },
    "parser-gap": {
      "design": "a parsing module shared by both scripts with the construct table and its fixtures; the generator and the checker consume parsed records, not lines",
      "implementation": "the P1-12 owner task dotfiles-T133-task-generator-plan-check-followup-a01 (rows audit:9da0ed3:10-13 and audit:8a09b93:7-8), after the C11 grammar row",
      "specification": "task-from-plan.py and plan-check.py parse plan and todo tables through one table-driven tokenizer with a fixture per construct (numbered items with blank lines and fenced blocks, commands with redirects or single words, acceptance events with timestamps and task ids, PR occurrences with several SHAs), never ad-hoc substring tests",
      "verification": "one red-then-green fixture per construct; plan-check.py run against the live plan 024 files reports zero parser warnings"
    }
  },
  "searches": [
    {
      "class": "parser-gap",
      "records": []
    },
    {
      "class": "decision-not-bound-to-execution",
      "records": []
    }
  ],
  "task": "dotfiles-T133-task-generator-plan-check-a02"
}
---

# Acceptance record: dotfiles-T133-task-generator-plan-check-a02

Plan 024 P1-12, the INV-6 reset of `dotfiles-T133-task-generator-plan-check-a01` (two amendments by substance, M-20261018-15; the audit of 9da0ed3: 3 P1 and 12 P2, folded in as items 5 to 19). Redesigned by a review-profile context (`.agents/worklog/orchestrator-glue/redesign/p112-a02.md`, prompt `p112-a02-redesign-prompt.md`); the orchestrator added item 20 (the checker hardening PR #418's review pointed here: C10 literals as `git grep -e` operands, C6 paths confined to the checkout) and the stale-premise note before the send. Seat a009 (worker-c, Claude) continues PR #417 from 9da0ed3. Owner of advisory P2: `dotfiles-T133-task-generator-plan-check-followup-a01` (written 21:0xZ).

- 2026-10-18T21:4xZ: task text installed, `task-consistency-check.py … : OK`, home-path scan 0 matches, dispatched to a009 (the line above; the full note is in the bus history). Known stale premise 5 (test_task_checkers.py "in flight in PR #413"): #413 merged at 10:46Z; a C14 finding at acceptance, records-form.
- 2026-10-19T00:08:22Z: RESULT round 1 from a009: PR #417 head 3f12e603118b8bb1acc9005f5befcdb5b9cbd2b7 (code head 6e07d291, continued from 9da0ed3) on 3e41e36a; `task_copy=a3ab8ea6…` (the dispatched sha); first push 6da92853 (the a01 copy deleted, the a02 copy added); the three Bot threads fixed (538e60bd, eb20d063); audit items 5 to 19 fixed at eb20d063 (item 19's C12 remedy owned here) and item 20 (C10 `-e` operands, C6 confinement); one self-review round (2 P2 + 4 P3, fixed 6e07d291); 15 new or updated end-to-end tests red on 9da0ed3 by exact id; four modules 28 OK; unit baseline identical to 3e41e36a; the checker passes 29 T133 files with the C14 not-run warning ×20; plan-check exit 1 with six violations left for the orchestrator (F3 ×2, F4, F6 ×3); caps 659/700 and 657/800; dispatch.sh:238 needs `--premises-sha` (the P1-5/P1-6 lineage); INV-6 0/0/0. `status=pending-integration` sent 00:1xZ; the chain is queued after #411 and #420.

## Owned by dotfiles-T133-task-generator-plan-check-followup-a01

- `checker:C17` residual-sentence-vs-allowed-files: a threat row whose disposition claims "no <kind> file is in allowed_files" (workflow, interpreter, script) is verified by task-consistency-check.py against the front matter; PR #421 shipped a false residual (Bot P1 4309302616, local P2) copied from the narrow owner template after the task was widened to three workflow files.
- `checker:C19` inherited-caps: a task text that applies another task's Check or Completion clause by reference restates its own comparison range and caps; task-consistency-check.py resolves the reference and fails a text whose caps are only inherited (PR #423 audit:9d13a06:2: the a01 amendment's 741e242...HEAD 60/120 caps were imported into a02 and measured 1,025/1,997 there).
- 2026-10-19T03:41Z: the chain update-branched #417 onto b22a5580 (→ 63b6acae); the four `test` jobs fail on three regime tests (run 39195158133): the #418 fixtures in tests/unit/test_regime_ci.py carry pre-C13 threat-row dispositions and the regime verifier runs this task's checker on them ("C13 disposition is not closed:, residual: or out-of-scope: and a space"); a semantic conflict between two merged lineages, not a defect of either alone. Counters: tasks=1 amendments=0 results=1 revises=0. Decision: amendment 1 (fixture repair only; tests/unit/test_regime_ci.py joins allowed_files with its row; C-61: one CI-repair round) dispatched to a009 03:4xZ (sha 60d4c2db…, previous a3ab8ea6…). Root cause: the checker vocabulary changed in one lineage while another lineage's fixtures were written against the old grammar; nothing runs the full suite of main-plus-PR before the update-branch (the chain's CI does, which is where it surfaced).
- 2026-10-19T04:03:46Z: CI-repair-1 RESULT from a009: PR #417 head 8a09b936 (code head eb0b1c06, previous 63b6acae) on b22a5580; `task_copy=60d4c2db…` (amendment 1); repair in tests/unit/test_regime_ci.py only (the five fixture threat rows take the C13 grammar); regime tests red on 63b6acae, 101 tests green on eb0b1c06; CI 11/11; Bot none in 15 min; caps 659/700 and 673/800. `status=pending-integration` sent 04:0xZ; the chain re-runs after #424.
local:8a09b93:1	advisory-p2
local-finding: 8a09b93:1 not-applicable:advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (- [P2] Classify agent instruction files as applied files — scripts/orchestrator/task-consistency-check.py:63-65); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-task-generator-plan-check-followup-a01.md (27d121f5bc4d7ae7d41100e35b8ab026b9d018493eaae601ca5176a72252befb)
local:8a09b93:2	advisory-p2
local-finding: 8a09b93:2 not-applicable:advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (- [P2] Handle nested directory scopes before invoking C7b — scripts/orchestrator/task-from-plan.py:153-153); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-task-generator-plan-check-followup-a01.md (27d121f5bc4d7ae7d41100e35b8ab026b9d018493eaae601ca5176a72252befb)
local:8a09b93:3	advisory-p2
local-finding: 8a09b93:3 not-applicable:advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (- [P2] Include repository-root files in the generated edit scope — scripts/orchestrator/task-from-plan.py:137-137); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-task-generator-plan-check-followup-a01.md (27d121f5bc4d7ae7d41100e35b8ab026b9d018493eaae601ca5176a72252befb)
local:8a09b93:4	advisory-p2
local-finding: 8a09b93:4 not-applicable:advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (- [P2] Normalize extracted paths before emitting allowed_files — scripts/orchestrator/task-from-plan.py:138-143); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-task-generator-plan-check-followup-a01.md (27d121f5bc4d7ae7d41100e35b8ab026b9d018493eaae601ca5176a72252befb)
local:8a09b93:5	advisory-p2
local-finding: 8a09b93:5 not-applicable:advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (- [P2] Use a threat-row selector accepted by C11 — .orchestration/dotfiles-T133-task-generator-plan-check-a02/task.md:37); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-task-generator-plan-check-followup-a01.md (27d121f5bc4d7ae7d41100e35b8ab026b9d018493eaae601ca5176a72252befb)

## Lineage ledger rows for the audit of 9da0ed3 (the a01 head; the a01 stopped at S2 and the a02 reset absorbed the fifteen findings as its items, all reported fixed in the a02 RESULT 00:08Z; the a01 record carries no rows because the task was withdrawn before disposition; the record step writes no lineage rows, the P1-6 item)

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

## Bot-thread ledger rows carried from the a01 record (PR #417 round 1 and revise 1 of the a01; fixed:b3c6b7ea and fixed:538e60bd, in 417-extra.tsv; the record step writes no Bot rows)

4306960622	trust-boundary-pr-input
4306960626	missing-input-crash
4306960630	string-form-comparison
- 2026-10-19T04:17-04:19Z: the #417 chain was started twice in the same review worktree (a guarded launch waited for the ledger rows while the orchestrator wrote them and launched again); the second run failed at its fetch step ("git checkout --detach does not take a path argument FETCH_HEAD") and the first stopped on three Bot-thread ledger gaps (4306960622/26/30, dispositioned in 417-extra.tsv but absent from the record's ledger). Rows carried from the a01 record's JSON ledger (trust-boundary-pr-input, missing-input-crash, string-form-comparison) and the chain re-run alone at 04:19Z. Hygiene: a guarded launch is never combined with a later unguarded launch of the same chain; one review worktree per PR (P1-6) removes the collision class.

## Audit of 8a09b936 (2026-10-19T04:28Z): twelve P2, no P0/P1; acceptance with owner rows

- The chain (sweep 7 items 0 gaps; local review 0; the ledger completed by hand with the 15 lineage rows of 9da0ed3 and the 3 Bot rows) ran the audit (`.orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-audit-8a09b93.md`): `Verdict: incorrect` on twelve P2: nine implementation (C15 local-design acceptance; C12 scope and confinement gaps; task-from-plan.py root files, directory-with-child rows, unnormalized paths, discarded single-word commands; plan-check.py F1 cell), one evidence (the edited-file SHA test), three orchestration (C11 rejects the `::Class::test` selector form amendment 1 uses; the template thread's `fixed:b3c6b7ea` should be `fixed:eb20d063`; the parser-gap class lacks its search evidence). Task-copy SHA and both caps verified by the auditor.
- counters: tasks=1 amendments=1 (the CI-repair amendment) results=2 revises=0; worker rounds 2 (pre-push review, CI repair): the C-61 cap.
- decision: no worker round (the cap; no P0/P1). The nine implementation P2 and the evidence P2 are advisory rows of the P1-12 owner `dotfiles-T133-task-generator-plan-check-followup-a01`, dispatched to a009 right after this merge with the C11 grammar as its first row (the regime's selector convention is the pytest node id with an optional class; C11's narrower grammar would make dispatch.sh refuse the next texts, so the owner fix lands first and no text is dispatched through a C11-bearing checker before it). The template disposition is corrected in 417-extra.tsv. The parser-gap class (rows audit:9da0ed3:10-13, audit:8a09b93:7-8) gets its re-plan in the JSON block and the search below.

search: grep -l 'parser-gap' .orchestration/learning/mistakes/*.md → (no record; M-20261019-04 written now)

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

## Owned by dotfiles-T133-task-generator-plan-check-followup-a01

- `audit:8a09b93:10` selector-grammar (first): C11 accepts the pytest node id `tests/unit/<module>.py::<Class>::<test>` and `::<test>`; red against 8a09b936 with the a02 copy itself.
- `audit:8a09b93:1` C15 requires the design on origin/main; `audit:8a09b93:2` C12 covers agent instruction files; `audit:8a09b93:3` an out-of-checkout scope is a confinement finding; `audit:8a09b93:4` root files are kept; `audit:8a09b93:5` directory-with-child rows; `audit:8a09b93:6` path normalization; `audit:8a09b93:7` single-word commands retained with their failure status; `audit:8a09b93:8` plan-check F1 reads the completion cell by header; `audit:8a09b93:9` the edited-file test rejects changed bytes against the original SHA. Plus the lineage rows audit:9da0ed3:10-13 (parser-gap) under the parser-gap re-plan.
- 2026-10-19T04:31:54Z: the chain refuses a second run for an already-audited head, so the sweep was redone by its two steps alone (`pr-feedback.py 417 --json`, the comments dump, `fill_sweep.py … 417-extra.tsv --orchestrator-login moriya-fumio-thd`): 10 items, 0 gaps; thread 4306960626 now `fixed:eb20d063`, 4306960630 `fixed:b3c6b7ea`, 4306960622 `fixed:538e60bd`. The gate reads this JSON.

## Security review of 8a09b936 (2026-10-19T04:34Z): three P1, one P2; S1 by class; a02 withdrawn, a03 reset

- `.orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-security-8a09b93.md`: `Verdict: incorrect`: (1) P1 task-from-plan.py:114 executes a committed PR HEAD's plan commands with no trusted digest; (2) P1 task-consistency-check.py:89 resolves even `bash` through `<root>/bin` first, so a checkout-controlled interpreter runs under a valid premise hash; (3) P1 task-from-plan.py:228 writes its output through an existing symlink; (4) P2 plan-check.py:86 task-controlled globs enumerate outside --root. C14's same-byte hash, the C10 fix, C6 and yaml.safe_load hold.
- class: `decision-not-bound-to-execution` (the class of P1-14's a03/a04 and of every C-80 review today); three security P1 in one mechanism text written before design 5.14 → S1 at the class level; the C-61 cap is also reached (pre-push review, CI repair). The glue guard refuses the merge (P1 lines).
- decision: a02 withdrawn (`status=withdrawn` to a009 04:3xZ; the branch and PR #417 stay); a03 (reset_of a02) applies 5.14 items 2-4 to the three scripts, folds the three P1 and the P2 as items, and the C11 node-id grammar (so the merged checker accepts the regime's selector form); the twelve audit P2 stay with the owner followup-a01, which is dispatched after a03 merges. The a03 text passes C-80 before dispatch; a009 implements on the same branch.

security:8a09b93:1	decision-not-bound-to-execution
security:8a09b93:2	decision-not-bound-to-execution
security:8a09b93:3	decision-not-bound-to-execution
security:8a09b93:4	glob-filter
- 2026-10-19T04:45:46Z: C-80 review of the a03 text (`dotfiles-T133-task-generator-plan-check-a03-text-security-f6797ab.md`): `Verdict: incorrect`, three P1: (1) C14 authenticates the premise command text, not its file operands (`python -I scripts/probe.py`, `source ./probe.sh` run checkout bytes under a trusted interpreter) → premises become a fixed read-only probe vocabulary the checker interprets, no shell (5.14 item 2 amended); (2) `uv run --no-project … python -I` still discovers `.venv` and uv configuration → `--no-config --python <absolute trusted interpreter> --offline` with a hostile .venv fixture (5.14 item 9 amended); (3) the sandbox claims have no deployment prerequisite (the manifest still has failIfUnavailable false and the Linux gh exclusion) → `after: [dotfiles-T133-worker-write-boundary-a01]` and the pre-P1-15 residual stated. Round 2 of the a03 text follows.
- 2026-10-19T04:5xZ: a03 round-2 text installed (C14 probe vocabulary without a shell; uv --no-config --python <abs>; after: worker-write-boundary-a01); checker OK; its C-80 review started.
- 2026-10-19T05:32:41Z: a03 round-3 text installed (the repository-local git filter check before any status or diff, with the marker regression); checker OK; its third C-80 review started 05:33Z.
- 2026-10-19T05:36Z: C-80 third review of the a03 text (`…-a03-text-security-49a7944.md`): one P1: `git config --local` misses the worktree-scoped config.worktree and includes, so a filter defined there bypasses the check → the check reads the effective configuration (`--show-origin --get-regexp`) with three fixtures; round 4 follows.

 succeeded in 388ms:
99:## 5.14 信頼ホスト実行契約（trusted-host execution contract、D-024-18）
100-
101-orchestrator 側の仕組み（merge gate、integrate-merge、orch-gate、dispositions、audit-pool、verdict、chain）は、同じホスト上で同じ UID の worker プロセスと共存する。2026-10-19 の C-80 審査（a05、dispositions-a02、audit-pool-a01 の 3 文、計 19 件の P1）は、どの文も同じ前提を書かず同じ穴を持つことを示した。以後、`security: true` の orchestrator 側タスク文は本節を参照で適用し、本節の各項目に対応する threat 行を持つ。文ごとに言い換えない。
102-
103-1. **書き込み境界（前提 6、ランタイム別に正直に）** Claude worker 席は専用の設定ディレクトリ `CLAUDE_CONFIG_DIR=~/.claude-worker`（chezmoi が描画、operator が一度 login）で起動し、orchestrator の `~/.claude` と設定を共有しない。worker 設定：除外コマンド無し、Herdr socket 無し、sandbox の allowWrite は自席 worktree と agmsg store と席別キャッシュだけ、`failIfUnavailable: true`、信頼パス（anchored checkout の `.claude/worktrees/` 以外、`~/.agents`、`~/.claude*`、`~/.local`、`~/.config`）への Edit deny（公式文書：file tool の permission 検査は要求パスと symlink 解決後のパスの両方に deny を適用し、symlink そのものへの書き込みは拒否する）、sandbox の強制範囲はユーザー設定ではなく **managed settings**（`/Library/Application Support/ClaudeCode/managed-settings.json`、公式文書 "Repository settings under an admin-required sandbox"：project/local 設定は sandbox を無効化したり除外・socket を足したりできない）に置く。chezmoi は user ではこのファイルを書けないので、描画した内容を操作者が `sudo` で一度配置する（操作者手順）。worker 設定は worktree 自身の `.claude/**` と `.mcp.json` への Edit deny（`//<anchored>/.claude/worktrees/*/.claude/**`）を持つ（Bash 側は sandbox 既定の settings/hooks の denyWithinAllow）。agmsg store（全席が書く）から配送 hook が driver や plugin を source する上流の経路（storage.sh の `drivers.partition` traversal、`db/trusted-plugins` と `plugins/partition/shared.sh` による差し替え承認）は別タスク（agmsg hardening）の行で、worker 設定は `~/.agents/skills/agmsg/plugins/**` と `~/.agents/skills/agmsg/db/trusted-plugins` への書き込みを deny し（Edit deny は sandbox の deny にも合流する）、hook 側は store 由来の設定値を検証するまで残余と書く。managed settings の配置先は OS で異なる（macOS `/Library/Application Support/ClaudeCode/managed-settings.json`、Linux `/etc/claude-code/managed-settings.json`）。hook は agmsg 配送だけを、hook コマンドを `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<home> …` で始めて（`BASH_ENV` などの継承環境を bash 起動前に消す；PATH 固定だけでは BASH_ENV が先に走る）絶対パスのインタプリタで呼び（上流の agmsg スクリプトは `/usr/bin/env bash` の shebang を持つので、hook 実行環境の PATH が shim を含まないことで束縛する）、各 hook に `onFailure: "block"`。公式文書：linked worktree の session は **main checkout の `.claude/settings.local.json` を読む**ので、worker 向けの hook を worktree の settings.local.json に書いても読まれず、逆に orchestrator の local hooks が worker session でも走る。したがって orchestrator 側の local hooks も guard 経由にし、worker 側の hook は worker config dir の settings に置く。Edit deny の一覧は `git ls-tree` ではなく描画時の静的一覧（manifest に列挙、`.agents/worklog/**` と `.agents/worklog/uv-cache/**` を含む）とし、`~/.agents/**` の全面 deny は agmsg store の書き込みと矛盾するので、`~/.agents/agent-config.yaml`、`~/.agents/skills/**/scripts/**`、`~/.agents/model-profiles.env` などストア以外を列挙する。公式文書で確認した事実（2026-10-19）：`Edit(path)` の deny は Write/MultiEdit/NotebookEdit にも効き、deny → ask → allow の順で最初の一致が決まる；ただし Read/Edit の deny は **Bash sandbox の設定にも合流する**（"Paths and domains from both sandbox settings and permission rules are merged into the final sandbox configuration"）ので、ユーザー設定（全席共有）に `.orchestration/**` の Edit deny を書くと orchestrator の Bash による記録書き込みも止まる。hook は起動時に固定されず、設定ファイルの編集は file watcher が即座に反映する。`sandbox.failIfUnavailable` の既定は fail-open（依存が無ければ sandbox 無しで実行）。したがって Claude 席の境界は Edit deny 規則ではなく、**ユーザーレベルの PreToolUse hook**（`~/.claude/hooks/worker-write-boundary`、chezmoi が描画、`/bin/sh` または絶対パスの `python3 -I`）で作る：cwd の realpath が `<anchored>/.claude/worktrees/` 配下の session では、Write/Edit/MultiEdit/NotebookEdit の対象が cwd の外、または `<cwd>/.claude/**`・`<cwd>/.mcp.json` のとき `permissionDecision: deny` を返す。Bash 側は sandbox の既定 `denyWithinAllow`（settings、hooks）と `allowWrite`（自席 worktree）が担う。`failIfUnavailable: true` を全席に置く。 Codex 席は sandbox（workspace-write）がツールの書き込み全部を自席の worktree と列挙パスに限る。Claude 席は Seatbelt sandbox が Bash を限るだけで、Write/Edit/MultiEdit/NotebookEdit、hook、MCP プロセスは sandbox 外で動き、permission policy（permgate の決定論ポリシー）が path で拒否しない限り anchored checkout や `~/.agents` にも書ける（2026-10-19 時点、描画済み設定にその deny は無い）。したがって前提 6 は「Codex 席は成立、Claude 席は P1-15 が描画設定に Edit の path deny を入れるまで残余」と書く。P1-15 以前に「worker は信頼ルートに書けない」と書く文は誤りで、C-80 が拒否する。P1-15 が入るまで、承認の出所は項目 8 の「コミット済み台帳」で守る。書き込みは自席の worktree（`.claude/worktrees/<name>`）、scratch、列挙されたツールキャッシュに限る。anchored checkout（`.claude/worktrees/` 以外）、`~/.agents/agent-config.yaml`、`~/.claude/hooks`、信頼ルートのバイナリ、orchestrator の証跡・スナップショット・lock は worker から書けない。render テストが描画後の deny を検証する。残余は「どの席 sandbox にも属さない同一 UID プロセス」と、Worker Playbook step 4 が sandbox 外に出す少数のコマンド（gh）。後者は D-024-17（P1-15）で絶対パスの実行体に束縛する。
104-2. **無害化した環境を最初に** 最初の処理として `env -i` に入り、PATH は信頼ルートで解決した絶対バイナリへのリンクだけの私設ディレクトリ（shims、空、相対は拒否）。git は毎回 `GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null -c core.hooksPath=/dev/null -c core.fsmonitor=false -c protocol.allow=never -c protocol.https.allow=always` と明示 `-C`（https だけ許す。`protocol.allow=never` 単独は必要な fetch を止める）。 premise や検査の「コマンド実行」は、固定語彙の読み取り専用プローブ（`git rev-parse <ref>`、`test -e <path>`、`grep -c <pattern> <file>` のように検査器自身が解釈する形）だけを許し、任意のシェル文字列は実行しない（本文のハッシュはコマンド文を認証するだけで、`python -I scripts/x.py` のファイル被演算子や `source ./x.sh` の中身は認証しない）。diff と show は `--no-ext-diff --no-textconv` と `-c core.attributesFile=/dev/null -c core.sshCommand=false` を付け、PR 側の `.gitattributes`（external diff、textconv、filter）が検査内容や実行物を変えないようにする。Python は `-I`。PATH 探索で実行するものは無い。
105-3. **信頼パスの境界検査** 仕組みが信頼するパス（スクリプト、台帳、証跡、worktree、lock、出力先）は realpath で解決し、`.claude/worktrees/` または manifest の worker ルート配下なら拒否（ask/hold）。symlink 構成要素は解決後に比較し、大小文字を区別しないファイルシステムでは同一性比較を大小文字非依存で行う。
106-4. **検証したものを実行し、検証した内容を渡す** 検証した実行体はその realpath で実行する（再探索しない）。検証したファイル内容は信頼ルート配下のスナップショット（0600、一意名）として渡し、使用直前に sha256 を再照合する。判断に読んだ証跡は sha256 を出力に記録する。
107-5. **出力と予約の同一性** 名前には 40 桁の head を使う（7 桁で衝突させない）。lock は信頼ルート配下の固定 inode に O_EXCL で作り、置換を inode 比較で検出する。物理スロット 1 つに lock 1 つ。
108-6. **正直な残余** 境界だけが緩和するリスクを `closed` と書かない。各文は残余を 1 行で明記する。
109-0. **脅威モデル（D-024-21）** 席は同じ OS ユーザで動き、ホストは席間の信頼境界ではない（同一 UID のプロセスは symlink 差し替え、共有 `.git` の object 差し替え、hook の子プロセス、Herdr socket 経由の host 実行で、ホスト内のどの検査も迂回できる）。regime の硬い境界は GitHub（保護された main、必須チェック、orchestrator の identity によるマージ）。ただしこの境界は **worker 席が orchestrator の GitHub 資格情報を共有しない**ときだけ成立する（D-024-22：worker 席は専用の GitHub identity（別アカウントまたは App のトークン）で `gh` に login し、ruleset の bypass 一覧に入らない。orchestrator の keychain トークンを worker の config dir に持ち込まない。identity が分かれるまで「GitHub が境界」は未成立と書く）。**同一 macOS ユーザでは資格情報は分離できない**（gh は keychain の項目を host/user で引き、同じ UID の gh は orchestrator のトークンを読める。`GH_CONFIG_DIR` は設定を分けるだけ）。防止には worker 席を別の OS ユーザ（または別ホスト）で動かすしかなく、それは D-024-23 の将来項目（P1-16、操作者の判断）。それまで GitHub 境界は **検知**で守る：regime CI の main push 実行が、受け入れ記録と gate 通過の証跡を持たないマージを検知して警報を出す（P1-11 lineage の行）。文は「防止ではなく検知」と書く。悪意ある worker に耐えるべき入力（承認台帳、gate が読む証跡 of record）は GitHub から sha 指定で API 経由（sandbox 内）に読み、ローカルファイルやローカル object database からは読まない。ホスト内の制御（本節 1〜10）は事故と prompt injection による損害の抑制であり、文はそう書く。
110-8. **承認はコミット済み台帳から読む** permission の決定行（`scope=permission approved_by=user diff_sha256=…`）は anchored checkout の作業コピーではなく、コミット済みの台帳から読む。読み方は `git ls-remote origin refs/heads/main` が返す commit sha を取り、GitHub API（`gh api repos/<owner>/<repo>/contents/.orchestration/decisions.tsv?ref=<sha>`、sandbox 内）でその sha の内容を取得する。ローカルの `git show` は共有 object database が書けるため中間 tree の差し替えで偽物を返しうる（第 3 回審査の所見 2）（ローカルの ref 名 `origin/main` は経由しない。`refs/replace/` も書けるので replacement を無効にする。Codex worker は `.git/objects` と `.git/refs` に書けるので ref は差し替えられるが、sha で指した object は内容アドレスで偽造できない）。作業コピーの行は提案で、記録 PR が main にマージされて初めて承認になる（PR の承認は操作者の操作）。偽造には main へのマージが要る。
111-9. **私設キャッシュ** orchestrator 側の実行は worker と共有するキャッシュ（`~/.cache/uv`、`~/.local/share/uv`、mise）から実行可能物を読まない。`UV_CACHE_DIR` を anchored checkout 配下（`.agents/worklog/uv-cache`、gitignored、worker 書き込み不可）に固定し、`uv run --no-config --no-project --offline --python <信頼ルートの絶対パスのインタプリタ>` で起動する（`--no-config` で uv の設定探索を止め、`--python` の絶対パスで cwd や親の `.venv` の発見を止める；敵対的な `.venv` と `uv.toml` を置いた fixture で検証）。hook は uv を使わず jq と python 標準ライブラリだけで動く。
112-10. **worker は sandbox 外でコマンドを実行しない（D-024-17 の改訂）** 2026-10-19T03:45Z の実測で `gh api` は Claude sandbox の中から成功した（sandbox の proxy は CONNECT 型で TLS を終端しない；keychain のトークンも読めた）。worker 席の除外コマンドは空にし、gh も git push も sandbox 内の proxy 経由で実行する。Codex 席は `sandbox_workspace_write.network_access = true` で同じ状態にし、permgate の codex ポリシーは sandbox 外への escape を承認しない（permgate の変更は操作者の手順）。wrapper 方式（絶対パス、env -i、固定 GH_CONFIG_DIR）は LD_PRELOAD と引数転送（`gh repo clone -- --config`）を閉じられないので採らない。
113-7. **検証** threat_table は本節の項目 1〜10 に 1 行ずつ対応させる（参照だけでは足りない）。共通テスト補助 `tests/unit/trusted_exec_contract.py`（P1-6 で作る）を使い、仕組みごとに 4 つの red→green テストを持つ：PATH 先頭の shim が実行されない、植え付けた GIT_* と git 設定が効かない、worker ルート配下の信頼パスが拒否される、検証後に差し替えたファイルが消費側に届かない。

 succeeded in 395ms:
2. `scripts/orchestrator/task-from-plan.py` retains its CLI, committed plan-group reads, bundled template, whole-token wave selection, program-item extraction, scope proposals, grep provenance and threat-row generation.

   The clean-plan check remains a data-provenance check for staged, unstaged and untracked changes in the `024-*` group. A clean committed HEAD supplies no authorization to execute its plan text.

   The generator never executes a command extracted from a plan item. It also never executes bundled or plan-derived Check commands. It records each recognized command as text with an explicit `verify:` explanation that execution and verification remain pending. It fabricates no stdout or exit status and distinguishes a missing observation from an observed empty output.

   The generator creates no scratch worktree for Check execution. The former premise runner, scratch Check runner and their execution-only cleanup disappear. Trusted Git calls needed to read committed data and obtain provenance remain under the common execution contract.

   The generator invokes the trusted consistency checker without `--premises-sha`. It does not turn its own computed output digest into permission to execute generated premise text. Structural findings and the C14 not-run warning remain visible. The generated file remains available for editing when structural findings occur.

   `scripts/orchestrator/task-template.md` retains the bundled task-copy, evidence, non-path and orchestrator-effect rows, common Check command text and Completion contract. Its wording describes unverified commands and separate orchestrator verification. It makes no claim that generation ran those commands.

   Existing generation tests change their execution expectations only where this reset changes the contract. Recognized commands remain present as unverified text. The separately owned command-recognition and parser defects remain outside this task.

   `tests/unit/test_task_from_plan.py::TaskFromPlanTest::test_the_generator_never_executes_a_plan_command` is written first and is red against `8a09b9365932f23b09df8aa2385a93d0b3016a3e`. A clean committed plan and bundled Check content contain marker-writing commands. Generation retains their text and unverified status, creates no marker and no scratch worktree, and passes no trusted premise digest to the checker. It is green on the final implementation.

3. `scripts/orchestrator/task-from-plan.py` confines its output to `<root>/.orchestration/tasks/` and creates the destination with `O_EXCL`.

   The generator resolves the root, task directory and destination through realpath before creation. A destination resolving outside the task directory is refused. An existing destination is refused. An existing symlink is refused, including a dangling symlink and a symlink whose target remains inside the task directory.

   Exclusive creation supplies the final leaf-existence check. The generator writes the generated bytes through the exclusively created file and does not reopen the destination through a following write. Refusal leaves existing files, symlink targets and outside-root markers unchanged.

   The destination's confinement and exclusive creation reduce redirection and truncation risks. Concurrent parent-directory replacement by a same-UID process remains the item 0 host residual.

   `tests/unit/test_task_from_plan.py::TaskFromPlanTest::test_the_generator_refuses_a_symlinked_or_existing_output` is written first and is red against `8a09b9365932f23b09df8aa2385a93d0b3016a3e`. It covers an existing ordinary file, existing and dangling symlinks, an outside destination, symlinked parent traversal and successful creation of a fresh confined output. Existing target bytes remain unchanged. It is green on the final implementation.

---
format: 2
task_id: dotfiles-T133-worker-write-boundary-a01
kind: code
security: true
allowed_files:
  - home/dot_agents/agent-config.yaml
  - home/.chezmoitemplates/claude-settings-managed.json
  - home/.chezmoitemplates/claude-worker-settings.json
  - home/.chezmoitemplates/claude-managed-settings.json
  - home/dot_claude-worker/modify_private_settings.json
  - home/dot_claude/hooks/executable_orchestrator-only.sh
  - .claude/settings.json
  - scripts/generate-agent-configs.py
  - Makefile
  - home/dot_local/bin/common/executable_herdr-agents
  - home/dot_local/bin/common/executable_herdr-agent-state.sh
  - home/dot_agents/skills/agmsg-orchestration/SKILL.md
  - .gitignore
  - tests/unit/test_generate_agent_configs.py
  - tests/unit/test_claude_settings_merge.py
  - tests/unit/test_herdr_agents.py
  - tests/unit/test_claude_worker_settings.py
  - tests/unit/test_claude_managed_settings.py
  - .orchestration/dotfiles-T133-worker-write-boundary-a01/**
after: []
threat_table:
  - control: "home/dot_agents/agent-config.yaml (trusted checkout and interpreter bindings, static trusted_paths inventory, distinct worker policy, managed sandbox policy and worker caches)"
    disposition: "residual: the rendered policy reduces accidental and injected damage; tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_policy_is_separate_from_orchestrator_policy checks both platforms without claiming same-UID isolation."
  - control: "home/.chezmoitemplates/claude-settings-managed.json (orchestrator user settings with failIfUnavailable true, onFailure block and hook PATH bindings)"
    disposition: "residual: the user baseline preserves orchestrator functions within the managed sandbox policy; tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_orchestrator_settings_keep_existing_policy checks the specified changes and retained settings."
  - control: "home/.chezmoitemplates/claude-worker-settings.json (static trusted-path and worktree-configuration Edit denies, empty user exclusions, restricted write allowances, native merge denials and minimal delivery hooks)"
    disposition: "residual: dedicated user settings reduce worker access to trusted paths; tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_policy_renders_for_both_platforms checks the baseline and distinguishes it from shared managed exclusions and socket access."
  - control: "home/.chezmoitemplates/claude-managed-settings.json (admin-required sandbox enforcement, fixed rendered control-plane exclusions and Herdr socket allowance)"
    disposition: "residual: operator installation establishes the documented enforcement scope against project and local sandbox relaxation; tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_rendered_policy_requires_admin_sandbox asserts the rendered keys; shared control-plane capabilities and same-UID host access remain residual."
  - control: "home/dot_claude-worker/modify_private_settings.json (deployment of the dedicated worker baseline without importing orchestrator policy)"
    disposition: "residual: replacing the worker baseline's managed values reduces stale or permissive user configuration; tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_settings_replace_stale_policy_idempotently checks repeated rendering in temporary homes."
  - control: "home/dot_claude/hooks/executable_orchestrator-only.sh (anchored launch-root guard for tracked and main-checkout local project hooks)"
    disposition: "residual: the guard reduces execution of worker-influenced project code and orchestrator hooks in worker sessions; tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_project_guard_uses_launch_root_and_never_runs_worker_payloads checks fixed arguments, canonical identity and child status."
  - control: "formatter and project-map reload configuration-selection boundary (the edited file path in the hook tool input and its owning repository)"
    disposition: "residual: the guard skips these commands for input outside CLAUDE_PROJECT_DIR or in a worker repository under .claude/worktrees/, preventing consumption of worker-controlled Prettier JavaScript configuration and ruff settings; tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_project_guard_uses_launch_root_and_never_runs_worker_payloads checks both the skip and normal anchored-file execution."
  - control: ".claude/settings.json (every tracked project command routed through the installed guard with pinned PATH bindings, absolute interpreters and onFailure block)"
    disposition: "residual: guarded commands reduce worker-triggered project-hook execution; tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_every_tracked_project_hook_is_guarded_and_blocks_on_failure exhaustively traverses the hook entries."
  - control: "scripts/generate-agent-configs.py (separate user and managed settings generation, static manifest deny inventory and absolute executable bindings)"
    disposition: "residual: rendering an explicit manifest list removes Git object traversal from inventory construction; tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_deny_inventory_is_static_and_matches_manifest checks exact manifest correspondence and filesystem coverage."
  - control: "Makefile (the install-managed-settings target that renders a home-directory staging file and prints the operator's sudo install command)"
    disposition: "residual: staging makes the administrative installation concrete without granting the worker administrative authority; tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_install_target_stages_and_prints_without_running_sudo checks the destination, rendered content, quoting and absence of privileged execution."
  - control: "home/dot_local/bin/common/executable_herdr-agents (worker pane environment, dedicated Claude configuration, private caches, worker user hooks and guarded main-checkout local hooks)"
    disposition: "residual: launch preparation reduces accidental inheritance of orchestrator settings and stale hooks; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_every_worker_launch_receives_dedicated_policy_and_private_caches captures managed and standalone launches and repeated starts."
  - control: "home/dot_local/bin/common/executable_herdr-agent-state.sh (repository-owned Herdr state helper with an explicitly supplied absolute Python interpreter)"
    disposition: "residual: binding the helper and its Python child reduces shim execution; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_hook_descendants_do_not_execute_path_interpreters checks executed identities with planted shims."
  - control: "home/dot_agents/skills/agmsg-orchestration/SKILL.md (the governing Worker Playbook step 4 sentence)"
    disposition: "residual: the sentence removes procedural authorization for worker sandbox escapes; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_playbook_requires_every_command_inside_sandbox checks its replacement; shared managed control-plane capabilities remain available and are not represented as per-seat isolation."
  - control: ".gitignore (the .uv-cache directory pattern)"
    disposition: "residual: ignoring the private cache reduces accidental cache publication; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_uv_cache_directory_is_gitignored checks the pattern in a temporary checkout."
  - control: "tests/unit/test_generate_agent_configs.py (separate platform policies, static inventory, interpreter bindings and tracked hook coverage)"
    disposition: "residual: render fixtures verify configuration and command construction; they do not establish live enforcement or authenticate host-local inputs."
  - control: "tests/unit/test_claude_settings_merge.py (orchestrator baseline preservation and failure-policy rendering through the existing merge)"
    disposition: "residual: temporary HOME fixtures verify baseline entries and identify runtime-added hooks separately; they do not install administrative settings."
  - control: "tests/unit/test_herdr_agents.py (every launch route, repeated starts, main-local and worker-user hook placement, descendants, caches and retained native denials)"
    disposition: "residual: fake launchers and subprocess markers verify effective arguments and executed fixture identities without starting live seats; shared managed exceptions remain explicitly outside per-seat exclusion claims."
  - control: "tests/unit/test_claude_worker_settings.py (dedicated settings deployment, static narrow denies, worktree configuration protection, project guard and hook failure configuration)"
    disposition: "residual: fixtures verify configured controls and credential-free deployment behavior; runtime permission checks and the remaining path-consumption window remain deployment and host residuals."
  - control: "tests/unit/test_claude_managed_settings.py (managed policy rendering, conflicting project and local settings fixtures and nonprivileged staging)"
    disposition: "residual: fixtures verify the selected documented enforcement keys and staging behavior without simulating proof of Claude runtime enforcement or performing sudo installation."
  - control: ".orchestration/dotfiles-T133-worker-write-boundary-a01/** (this task's branch artifacts)"
    disposition: "residual: artifacts distinguish documentation facts, historical probes, final-head fixture results and unperformed operator deployment; acceptance compares their claims with the diff and CI."
  - control: "the task-file copy at .orchestration/dotfiles-T133-worker-write-boundary-a01/task.md"
    disposition: "residual: the first push includes the byte-identical dispatched task; TASK and RESULT carry its SHA256, which the orchestrator verifies at acceptance."
  - control: "the evidence records under .orchestration/dotfiles-T133-worker-write-boundary-a01/"
    disposition: "residual: report.md, validation.md, sandbox.md, learning.md, autoskill.md and worker review evidence retain commands, outputs, statuses and tested revisions without credentials or unmasked home-directory paths."
  - control: "task metadata (PR_FEEDBACK_EVIDENCE, AUDIT_EVIDENCE, ACCEPTANCE_EVIDENCE and REVIEW_EVIDENCE)"
    disposition: "residual: the orchestrator checks C1 to C10 and C7b, verifies dispatched bytes and binds integration evidence to the final head; P1-14 a05 and P1-6 implement retrieval of evidence of record from GitHub at its SHA; the GitHub boundary is detection, not prevention."
  - control: metadata separators
    disposition: "residual: the first document separators delimit format-2 metadata; the task-copy SHA256 binds the complete document."
  - control: in-process effects
    disposition: "residual: generation and tests use repository files and temporary fixtures; the worker performs no live deployment, login, administrative installation, permission-policy mutation or operator-session restart."
  - control: workflow and interpreter or environment inputs
    disposition: "residual: absolute interpreters, Python -I, sanitized Git, fixed hook PATH and trusted executable bindings reduce environment injection; the host, native loader and same-UID processes remain outside this task's security guarantee."
  - control: new or renamed scripts
    disposition: "residual: the worker settings modify script, orchestrator-only guard and repository-owned Herdr state helper have named source and installed paths; RESULT inventories their interpreter and descendant bindings without introducing a worker-write-boundary hook or gh wrapper."
  - control: "5.14 item 0: host threat model"
    disposition: "residual: host controls reduce accidental and injected damage without isolating seats sharing one OS user; prevention of worker-initiated merges requires a separate OS user or host under D-024-23's future P1-16, which the operator decides; the GitHub boundary is detection, not prevention, through P1-11's main-push flag for missing acceptance or gate evidence; shared managed control-plane exclusions and the Herdr socket remain residual."
  - control: "5.14 item 1: worker write controls"
    disposition: "residual: dedicated configuration, static symlink-aware Edit denies including worktree configuration and orchestrator worklogs and caches, narrow writable agmsg stores, managed sandbox enforcement and failIfUnavailable true reduce damage; documented path checks do not establish atomic immunity to concurrent path swaps."
  - control: "5.14 item 2: sanitized environment and private executable PATH"
    disposition: "residual: sanitized Git verification and absolute hook entrypoints reduce injected configuration, while PATH=/usr/bin:/bin binds upstream env-bash descendants away from shims; the remaining consuming-helper contracts belong to P1-14 a05, P1-10 a02, audit-pool-a02 and P1-6."
  - control: "5.14 item 3: trusted-path checks"
    disposition: "residual: canonical anchor and interpreter checks reduce worker-selected trusted paths and account for symlink components and filesystem case aliases; other consuming-helper checks remain with their owning hardening tasks."
  - control: "5.14 item 4: verified executable and consumed-byte identity"
    disposition: "residual: hooks execute selected absolute entrypoints and trusted scripts, and upstream shell descendants inherit the fixed system PATH; evidence snapshots, last-use digest checks and their race limitations remain with the consuming orchestrator-side tasks; store-selected driver execution remains the separately named agmsg residual."
  - control: "5.14 item 5: output and reservation identity"
    disposition: "residual: this task adds no reservation protocol; full-head output names, fixed-inode locks and physical-slot identity remain with the orchestrator-side tasks that create them."
  - control: "5.14 item 6: honest residuals, hooks and MCP"
    disposition: "residual: guarded tracked and main-local project hooks and minimal worker user hooks reduce host execution routes; shared managed Herdr socket access, control-plane exclusions, approved external processes and same-UID processes outside every seat sandbox remain residual."
  - control: "5.14 item 7: trusted-execution verification"
    disposition: "residual: this task records red-then-green render, merge, managed-policy, guard, launch, descendant and cache tests; P1-6 owns tests/unit/trusted_exec_contract.py and the consuming-helper contract tests."
  - control: "5.14 item 8: committed approval ledger"
    disposition: "residual: the regime reads the ledger through the GitHub contents API at the SHA returned by git ls-remote origin refs/heads/main; P1-14 a05 implements that read, and local refs, files and object traversal provide no approval authority; the GitHub boundary is detection, not prevention."
  - control: "5.14 item 9: private uv caches"
    disposition: "residual: per-seat worker caches, restricted worker write allowances and explicit denies on the orchestrator worklog and uv-cache reduce cache poisoning; consuming hardening tasks use the protected orchestrator cache with --offline and execute no worker, shared uv or mise cache content."
  - control: "5.14 item 10: no worker command outside the sandbox"
    disposition: "residual: empty worker user exclusions, disabled unsandboxed requests and Codex in-sandbox network reduce escape routes; the worker rule forbids using shared managed control-plane exceptions, whose availability and Herdr socket access remain residual; the deterministic Codex permgate rule and live deployment remain operator steps."
  - control: "hook failure policy"
    disposition: "residual: every generated and tracked hook entry, including launcher-written worker user and main-local entries, carries onFailure block, reducing fail-open behavior where Claude supports it; configuration tests cover missing-command and timeout policy, while background hooks and events on which the field has no effect carry no enforcement responsibility."
  - control: "agmsg store driver and plugin selection (team configuration drivers.partition, db/trusted-plugins authorization and installed storage.sh sourcing)"
    disposition: "residual: every seat writes the store, and installed storage.sh resolves drivers.partition as a driver path and sources it during unsandboxed delivery; it also uses db/trusted-plugins to authorize plugins/partition/shared.sh for sourcing; fixed PATH does not stop these routes; worker denies on plugins/** and db/trusted-plugins reduce the plugin route; dotfiles-T133-agmsg-hardening-a01 owns upstream basename validation, plugin authorization hardening and their adversarial red-then-green tests; this task introduces no store-derived sourcing beyond the installed scripts' current behavior."
  - control: orchestrator effect merge
    disposition: "residual: the worker is forbidden to merge; the orchestrator follows the final-head integration gate, required permission approval and pinned squash-merge procedure, with evidence of record retrieved from GitHub; shared credentials still permit worker-initiated API merges, so the GitHub boundary is detection, not prevention."
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
      D-024-21 establishes the host threat model and dedicated Claude worker configuration. D-024-23 supersedes D-024-22's credential-separation claim because gh Keychain access is shared by seats running as the same macOS user. Prevention requires a separate OS user or host; the current GitHub boundary is detection, not prevention.
    sources:
      - .orchestration/decisions.tsv
      - .orchestration/plans/024-design-quality.md
      - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md
  - claim: >-
      The existing Claude settings modify script merges the orchestrator user baseline into current settings and appends an attachment hook. The dedicated worker renderer does not import that orchestrator settings merge or its attachment behavior. The administrative managed-settings file is a separate deployment destination.
    sources:
      - home/dot_claude/modify_private_settings.json
      - home/.chezmoitemplates/claude-settings-managed.json
    verification: tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_settings_do_not_import_orchestrator_hooks
  - claim: >-
      The current launcher constructs worker profile options separately from the pane environment. The dedicated Claude configuration directory and private cache variables reach the actual worker process on every launch route. This task adds no gh configuration directory or credential-separation mechanism.
    sources:
      - home/dot_local/bin/common/executable_herdr-agents
      - home/dot_agents/agent-config.yaml
    verification: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_every_worker_launch_receives_dedicated_policy_and_private_caches
  - claim: >-
      Linked-worktree Claude sessions load the main checkout's .claude/settings.local.json. The current launcher writes worker-local delivery hooks and merge denials into a different file. Worker delivery moves to the worker configuration directory's user settings, and the launcher's main-checkout local hooks receive the orchestrator-only guard.
    sources:
      - https://code.claude.com/docs/en/settings#where-claude-code-keeps-the-local-file-in-a-git-repository
      - home/dot_local/bin/common/executable_herdr-agents
      - .claude/settings.local.json
    verification: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_linked_worktree_uses_worker_user_hooks_and_guarded_main_local_hooks
  - claim: >-
      Managed sandbox.enabled true, failIfUnavailable true and allowUnsandboxedCommands false establish the documented admin-required enforcement scope. Project and local settings cannot supply sandbox relaxations in that scope. User settings and shared managed exceptions remain distinct from project and local settings.
    sources:
      - https://code.claude.com/docs/en/sandboxing#repository-settings-under-an-admin-required-sandbox
      - .orchestration/plans/024-design-quality.md
      - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md
    verification: tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_managed_render_is_independent_of_conflicting_project_and_local_settings
  - claim: >-
      Installed agmsg storage.sh resolves the writable team configuration's drivers.partition value as a driver path and sources it during delivery. The upstream hardening belongs to dotfiles-T133-agmsg-hardening-a01 and remains a residual of this task.
    sources:
      - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md
      - .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-08e6ac7.md.last.md
---

# AGMSG-TASK dotfiles-T133-worker-write-boundary-a01 — plan 024 P1-15 under D-024-17, D-024-19, D-024-20, D-024-21 and D-024-23

## Goal

The host is not a security boundary between seats sharing one OS user. gh keys Keychain credentials by host and user, so a worker running as the same macOS user can read the orchestrator's token regardless of `GH_CONFIG_DIR`. Prevention of a worker-initiated merge requires a separate OS user or host under D-024-23's future P1-16, which the operator decides whether to pursue. Until then the GitHub boundary is detection, not prevention. The regime rule requires the main-push CI run to flag a merge that lacks the required acceptance record or gate-passage evidence. P1-11 owns implementation of that flag; this task states the rule. Approvals and gate evidence of record are read from GitHub at a SHA through its API inside the sandbox. Host-local controls reduce accidental and injected damage without establishing isolation from a malicious same-UID process.

This task implements section 5.14 items 1, 9 and 10 through a dedicated Claude worker configuration directory, static Edit deny rules on trusted paths and worktree configuration, managed sandbox enforcement, guarded project hooks, hook interpreter and PATH bindings, private worker caches and the rule that worker commands run inside their sandbox. Every Claude seat has `sandbox.failIfUnavailable: true`. Codex workers have `sandbox_workspace_write.network_access=true`.

The administrative managed policy is shared by every Claude seat. Its Herdr socket allowance and three control-plane exclusions remain available to workers as well as the orchestrator. Empty arrays in worker user settings do not subtract these managed entries. Their availability is a residual under item 0, and the worker execution rule supplies no authorization to use them outside the sandbox.

[memory:decision] D-024-20 makes this task the dispatch prerequisite of P1-14 a05, P1-10 a02, audit-pool-a02 and P1-6. The orchestrator places this task in their `after:` fields before dispatch. This task has `after: []`. A Codex seat performs these Claude configuration edits under the routing rule, including the Worker Playbook step 4 sentence permitted by plan 021 step 8.3.

The design source is `.orchestration/plans/024-design-quality.md` section 5.14 items 0 through 10. D-024-21, D-024-23 and the amended items 0, 1 and 8 govern this revision. D-024-22's proposed gh credential separation is superseded. The acceptance record preserves documentation facts and earlier proposals as history.

The third C-80 text review is `.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-ecc7ab5.md.last.md`. Its five P1 findings remain recorded. The retained mechanisms are documented symlink-aware deny rules, approval reads outside the local object database, hook interpreter bindings and runtime hook failure policy.

The fourth C-80 text review is `.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-8d42532.md.last.md`. Its six P1 findings remain recorded. The retained mechanisms are the static manifest deny inventory, protection of the orchestrator worklog and cache, narrow home denies around writable agmsg stores, correct linked-worktree hook placement and fixed hook-runtime PATH.

The fifth C-80 text review is `.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-08e6ac7.md.last.md`. Its three P1 findings remain recorded. This revision removes the gh credential-separation mechanism, records the upstream agmsg store-driver residual and moves sandbox enforcement into administrative managed settings.

The file-tool rule is the documented sentence, “Deny rules: apply when either the requested path or the file it resolves to matches.” Edit and Write refuse a requested file that is itself a symlink. Directory symlinks are subject to resolved-target permission checks, and the tools check the resolved location again when opening the approved file. These documented checks reduce redirection risk without establishing an atomic host security boundary against concurrent same-UID changes. [Claude permission reference](https://code.claude.com/docs/en/permissions#symlinks)

The 2026-10-19T03:45:06Z sandbox probe ran `gh api repos/mryfmo/dotfiles --jq .name` and returned `dotfiles`. The recorded sandbox proxy used CONNECT without TLS interception, and gh read the Keychain token. This historical observation confirms neither credential separation nor final-head deployment readiness.

The documentation facts recorded at 03:2xZ establish that Edit denies also affect the Bash sandbox, hooks reload during a session and an unavailable sandbox is fail-open by default. D-024-21's 04:0xZ decision establishes the dedicated Claude configuration mechanism, directory-specific Claude credentials, symlink coverage and `onFailure: "block"` support. These Claude credentials do not separate gh Keychain access.

The settings documentation states, “In a worktree, it uses the file at the main checkout’s root.” Linked-worktree sessions therefore load the main checkout's `.claude/settings.local.json`. Worker hooks belong in `~/.claude-worker/settings.json`, and the main checkout's local hooks also receive the orchestrator-only guard. [Claude local settings reference](https://code.claude.com/docs/en/settings#where-claude-code-keeps-the-local-file-in-a-git-repository)

## Files

1. `home/dot_agents/agent-config.yaml` remains the source of agent policy and model profiles.

   The manifest names `orchestrator_checkout` as the anchored primary checkout and supplies trusted deployment bindings for the guard, hook scripts and absolute interpreters. These bindings resolve outside worker worktrees and executable caches. Worker cwd, tool input, worktree configuration and inherited command variables do not select them. The manifest also supplies the trusted bindings from which the render resolves the absolute directories holding `ruff`, `prettier` and `terminal-browser`, without using mise shims.

   The manifest defines a separate Claude worker settings output at `home/.chezmoitemplates/claude-worker-settings.json` and an administrative managed-settings output at `home/.chezmoitemplates/claude-managed-settings.json`. The worker configuration directory is `~/.claude-worker`. The launcher passes its expanded absolute path as `CLAUDE_CONFIG_DIR`.

   A static `trusted_paths:` list names every protected top-level path of the anchored checkout and the protected home paths. It explicitly includes `<anchored-checkout>/.agents/worklog/**` and `<anchored-checkout>/.agents/worklog/uv-cache/**`. The `.claude` entries protect tracked contents and the main checkout's `.claude/settings.local.json` without denying the whole `.claude/worktrees/` tree. The list explicitly names directory targets and descendant patterns where both are required.

   Separate worker Edit denies protect `//<anchored-checkout>/.claude/worktrees/*/.claude/**` and `//<anchored-checkout>/.claude/worktrees/*/.mcp.json`. The `.claude` directory target is also protected. Ordinary worktree source files and the per-seat cache remain outside these configuration denies.

   The home-path denies are `~/.agents/agent-config.yaml`, `~/.agents/model-profiles.env`, `~/.agents/skills/**/scripts/**`, `~/.agents/skills/**/SKILL.md`, `~/.agents/skills/agmsg/plugins/**`, `~/.agents/skills/agmsg/db/trusted-plugins`, `~/.claude/**`, `~/.claude-worker/**`, `~/.local/bin/**`, `~/.local/share/**`, `~/.local/state/**`, `~/.local/share/mise/**`, `~/.config/**`, `~/.cache/uv/**` and `~/.local/share/uv/**`. No blanket deny on `~/.agents/**` or `~/.local/**` replaces this list.

   The agmsg store paths `~/.agents/skills/agmsg/db`, `~/.agents/skills/agmsg/teams`, `~/.agents/skills/agmsg/run` and `~/.agents/skills/agmsg/ext-tools` remain writable. Deny patterns cover neither these directory targets nor their descendants except the file `~/.agents/skills/agmsg/db/trusted-plugins`. Edit denies merge into the sandbox configuration, so Bash writes to that file and `~/.agents/skills/agmsg/plugins/**` are refused too. Their influence on installed delivery-script driver and plugin selection remains the separately owned agmsg residual.

   The orchestrator retains its existing permissions, cache allowances and hook functions within the administrative managed policy. Its user baseline receives `failIfUnavailable: true`, `onFailure: "block"` on its hooks and the interpreter and PATH bindings below. Its exclusion entries match the three control-plane entries specified below; the former Linux `gh *` exclusion is removed.

   The worker user policy contains no excluded commands and sets `allowUnsandboxedCommands: false`. It contains no Herdr socket allowance and no allow-all Unix socket switch. Its sandbox is enabled and has `failIfUnavailable: true`. Shared managed entries remain effective despite these empty worker arrays.

   Worker `sandbox.filesystem.allowWrite` contains only the existing agmsg store paths and per-seat cache paths. The worktree is the project root and supplies its ordinary project write root. Shared uv and mise write allowances are not copied into worker settings.

   The Codex worker profile sets `sandbox_workspace_write.network_access=true`. Existing model selections and Codex shared Git grants retain their meaning. The deterministic Codex permgate rule that stops approving sandbox escapes is an operator step.

2. `scripts/generate-agent-configs.py` renders the distinct orchestrator user, worker user and administrative managed baselines from the manifest.

   The trusted-path deny inventory is rendered from the static `trusted_paths:` list. Rendering performs no Git object traversal, `git ls-tree` enumeration or tracked-path discovery. Worker-writable refs, replacement refs and objects do not determine the list.

   Anchored checkout rules use absolute `//` permission patterns. Rendering includes the explicitly listed trusted paths themselves and their descendants. It emits no checkout-wide parent deny that defeats ordinary worktree writes. The separate worktree-configuration denies remain present.

   Edit denies cover Write, MultiEdit and NotebookEdit through Claude's permission system. Requested-path and resolved-target matching supply the documented symlink coverage. The generator creates no `executable_worker-write-boundary.py` or replacement PreToolUse path validator.

   Every direct Git verification introduced or changed by this task follows section 5.14 item 2. It begins with `env -i`, uses the selected absolute Git executable and an explicit `-C`, sets `GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL=/dev/null`, and supplies `-c core.hooksPath=/dev/null -c core.fsmonitor=false -c protocol.allow=never -c protocol.https.allow=always`. Diff and show also use `--no-ext-diff --no-textconv` and `-c core.attributesFile=/dev/null -c core.sshCommand=false`.

   The private executable-link directory contains only links to selected absolute trusted binaries. Rendering rejects missing bindings, worker-controlled executable paths, shims, empty PATH entries and relative PATH entries. Python invocations use `-I`. Hook execution uses the role-specific pinned PATH bindings specified below. The render test asserts that `ruff`, `prettier` and `terminal-browser` resolve under the rendered orchestrator tool PATH on the rendering host and that no entry of that PATH is a shims directory.

   `tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_deny_inventory_is_static_and_matches_manifest` asserts that the rendered list equals the manifest entry after trusted anchor and home expansion. It explicitly asserts the rendered home-path deny patterns `~/.local/share/**` and `~/.local/state/**`, including the application code under `~/.local/share` used by `~/.local/bin` wrappers such as `terminal-browser`. It reads the filesystem of the test's own checkout and asserts that every tracked top-level source path is represented. It invokes no Git command to discover those paths.

   The inventory fixtures cover files, directories, `.claude` children, the main-local settings file, ordinary worktree writes, both worktree-configuration patterns, an anchor containing spaces and both explicit worklog patterns. Adding a top-level source path without a manifest entry makes the coverage assertion fail. Planted Git environment and replacement-ref fixtures leave rendering unchanged.

   `tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_denies_leave_agmsg_stores_writable` asserts the rendered deny patterns `~/.agents/skills/agmsg/plugins/**` and `~/.agents/skills/agmsg/db/trusted-plugins` and verifies that the four store directories `db`, `teams`, `run` and `ext-tools` and their descendant fixtures remain writable except that one file.

3. `home/.chezmoitemplates/claude-settings-managed.json` remains the orchestrator user baseline.

   The existing `home/dot_claude/modify_private_settings.json` continues to render the orchestrator's `~/.claude/settings.json`. That modify script is not imported into the dedicated worker renderer and remains outside `allowed_files`.

   This existing template's name does not make it administrative managed settings. The new `claude-managed-settings.json` template supplies that separate scope.

   The orchestrator retains its current user policy content apart from `failIfUnavailable: true`, `onFailure: "block"`, the required interpreter and PATH bindings and alignment of exclusions with the three control-plane entries. Worker-specific Edit denies and restricted worker cache allowances do not enter this baseline. Administrative sandbox requirements apply to the orchestrator as well as workers.

   Every generated hook entry carries `onFailure: "block"`. Every generated command hook starts with `/usr/bin/env -i PATH=<pinned> HOME=<rendered home> LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}"` before its selected absolute interpreter and script path. The formatter and project-map hooks run through the installed orchestrator-only guard and receive the role-specific pinned PATH specified below. Merge evidence identifies hooks appended by the existing modify script and distinguishes them from generated baseline entries. The report accounts for the effective deployed hook set without equating baseline coverage with coverage of runtime-added entries.

   `tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_orchestrator_settings_keep_existing_policy` compares the merged policy with the preceding baseline and accounts for the specified changes. Repeated merging remains idempotent and preserves unrelated settings.

4. `home/.chezmoitemplates/claude-worker-settings.json` is the dedicated worker user baseline.

   It renders the static trusted-path Edit denies, the worktree `.claude` and `.mcp.json` Edit denies, retained native merge denials, empty user `excludedCommands`, `allowUnsandboxedCommands: false`, restricted `allowWrite`, no user Herdr socket allowance and `failIfUnavailable: true` for both Darwin and Linux.

   Its hooks are limited to agmsg delivery. It contains no formatter, project-map, permgate, orchestrator attachment, Herdr state or worker-write-boundary hook. Tracked project hooks and main-checkout local hooks still load and receive the guard described below.

   Every worker hook entry carries `onFailure: "block"`. Every command starts with `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<rendered home> LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}" AGMSG_RESOLVE_PROJECT=0` before the selected absolute shell interpreter and absolute installed agmsg script path. The prefix also re-exports `AGMSG_STORAGE_PATH` when it is set in the launcher environment. Project resolution from a writable `run/proj.<pid>.project` marker remains disabled, so delivery retains the explicit worker path. Descendants inherit this PATH.

   The worker baseline does not copy the orchestrator's plugins, credential files or current hook arrays. Hook settings reload during a session, so protection is stated as current configuration rather than startup capture. `CLAUDE_CONFIG_DIR` selects the separate user settings directory while project settings continue to apply within the administrative enforcement scope. [Claude settings reference](https://code.claude.com/docs/en/settings)

   Worker user settings supply no additional socket or exclusion allowance. Their empty lists cannot remove the shared managed Herdr socket or control-plane exclusions.

5. `home/.chezmoitemplates/claude-managed-settings.json` supplies the administrative sandbox policy.

   The rendered policy sets `sandbox.enabled: true`, `sandbox.failIfUnavailable: true` and `sandbox.allowUnsandboxedCommands: false`. The last setting makes sandboxing admin-required. Project and local files cannot add sandbox exclusions, socket allowances or other documented relaxations in this scope. Managed Boolean values prevail over lower scopes. User settings remain a separate trusted scope, and arrays such as exclusions have no general managed-only lock. [Repository settings under an admin-required sandbox](https://code.claude.com/docs/en/sandboxing#repository-settings-under-an-admin-required-sandbox)

   The rendered policy sets `sandbox.filesystem.disabled: false`, `sandbox.enableWeakerNestedSandbox: false`, `sandbox.enableWeakerNetworkIsolation: false`, `sandbox.network.allowAllUnixSockets: false`, `sandbox.network.allowLocalBinding: false` and `sandbox.allowAppleEvents: false`.

   The rendered `sandbox.excludedCommands` list contains exactly `agmsg-dispatch *`, `herdr-agents *` and `<absolute-home>/.agents/skills/agmsg/scripts/actas-claim.sh *`. These are the orchestrator's three control-plane entries. It contains no `gh *`, `git push *` or authenticated-fetch exemption.

   The rendered `sandbox.network.allowUnixSockets` list contains exactly the trusted home expansion of `~/.config/herdr/herdr.sock`. This allowance is shared by every seat under managed settings. Per-seat removal is unavailable in that scope, and the worker baseline's empty list does not revoke it.

   Shared control-plane exclusions are also available in worker sessions. The worker execution rule forbids using them to leave the sandbox. The text treats their availability and the socket's host-execution capability as item 0 residuals rather than enforced per-seat separation.

   `tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_rendered_policy_requires_admin_sandbox` asserts the rendered content, exact exclusion and socket lists, trusted home expansion and every required Boolean value.

   `tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_managed_render_is_independent_of_conflicting_project_and_local_settings` supplies project and local fixtures that disable sandboxing, disable startup failure, enable unsandboxed retries, add exclusions and sockets, enable weaker isolation and widen filesystem writes. The trusted managed render remains unchanged. The test verifies configuration scope and content without presenting a simulated settings merger as runtime enforcement.

6. `Makefile` adds only the `install-managed-settings` target and its `.PHONY` declaration.

   The target uses the repository's existing rendering facilities to render `home/.chezmoitemplates/claude-managed-settings.json` into `~/.claude/managed-settings.rendered.json`. The staging path is expanded to an absolute path under the user's home.

   The target selects `/Library/Application Support/ClaudeCode/managed-settings.json` on macOS and `/etc/claude-code/managed-settings.json` on Linux and prints the exact command `sudo install -m 0644 "<absolute-home>/.claude/managed-settings.rendered.json" "<detected-managed-settings-path>"` with the actual staging path and detected destination substituted and shell quoting preserved. The printed command is ready for the operator to run.

   The target performs no sudo call, administrative installation, live settings application, authentication or session restart. The staging file alone does not establish managed enforcement.

   `tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_install_target_stages_and_prints_without_running_sudo` covers both macOS and Linux, uses a temporary home, verifies the staged JSON and exact printed command with the detected destination, includes a home path containing spaces and asserts that a planted sudo marker remains absent.

7. `home/dot_claude-worker/modify_private_settings.json` renders `~/.claude-worker/settings.json` from the dedicated baseline.

   The script follows the existing chezmoi modify-script interface: current content arrives on stdin and the desired settings object is written to stdout. It uses Python's standard library and the same trusted source and home resolution conventions as the existing renderer.

   Worker permissions, sandbox policy and hooks managed by this renderer replace stale managed values. Permissive old user exclusions, socket allowances, hook commands and shared cache allowances do not survive as additive worker user policy. The script does not read or copy `~/.claude/settings.json`.

   Rendering handles empty and malformed input through the repository's existing baseline behavior and is idempotent. It neither reads credentials nor initiates authentication.

   `tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_settings_replace_stale_policy_idempotently` exercises repeated deployment in temporary homes. `tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_settings_do_not_import_orchestrator_hooks` plants orchestrator hook and plugin markers and verifies their absence.

8. `home/dot_claude/hooks/executable_orchestrator-only.sh` is installed as `~/.claude/hooks/orchestrator-only.sh`.

   The guard runs under the selected absolute shell interpreter and compares canonical `CLAUDE_PROJECT_DIR` with the anchored checkout. Equality executes the supplied fixed command subject to the formatter and project-map tool-input check below. Every other launch root exits 0 without executing it.

   Worker launch roots, sibling worktrees and unrelated checkouts execute no guarded project code. Missing or unresolvable launch-root identity also executes no supplied command. Event cwd does not change the launch-root decision.

   The guard also binds the formatter and project-map reload to the edited file path from the hook's tool input and its owning repository. When the resolved path is outside canonical `CLAUDE_PROJECT_DIR` or belongs to a worker repository under `.claude/worktrees/`, the guard exits 0 without running the command. Worker-repository configuration, including Prettier JavaScript configuration and ruff settings, is never consumed by an orchestrator hook.

   The guard preserves argument boundaries, stdin and child exit status. It performs no eval, PATH interpreter lookup or worktree-relative script selection. Its caller starts with `/usr/bin/env -i PATH=<pinned> HOME=<rendered home> LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}"` followed by the absolute interpreter and script. The launch identity and the few variables Claude Code documents for hooks are re-exported explicitly after `env -i`, so the guard sees `CLAUDE_PROJECT_DIR`.

   The pinned PATH differs by role. Worker-session hooks use `/usr/bin:/bin`. For the orchestrator's formatter and project-map hooks, which the guard runs only in orchestrator sessions, the guard itself sets PATH to a rendered list of absolute tool directories of the trusted root before executing the guarded command. Those directories hold `ruff`, `prettier` and `terminal-browser` and are resolved by the render from the manifest without using mise shims. The formatter and project-map scripts remain outside `allowed_files` and unchanged.

   `tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_project_guard_uses_launch_root_and_never_runs_worker_payloads` plants worker Stop, contextdb and formatter payloads. Worker and unrelated-root invocations leave all markers absent. The positive-path case runs the complete rendered command in a subprocess with a fake `CLAUDE_PROJECT_DIR` equal to the anchored checkout and asserts that the guarded script executed while preserving its arguments and status. A second case runs the complete rendered command with a worktree `CLAUDE_PROJECT_DIR` and asserts that the guarded script did not execute. A planted `BASH_ENV` in the outer environment remains unexecuted in both cases. Formatter and project-map reload cases keep `CLAUDE_PROJECT_DIR` anchored and supply hook tool input for an outside file and a worker-repository file under `.claude/worktrees/`; both exit 0 with command and planted configuration markers absent. Matching anchored-file inputs run both commands normally.

9. `.claude/settings.json` retains its tracked project hooks and rewrites every command through the installed orchestrator-only guard.

   Every command starts with `/usr/bin/env -i PATH=<pinned> HOME=<rendered home> LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}"` before the absolute shell interpreter and installed guard path. The guarded child command uses an absolute interpreter and an anchored script path. Contextdb commands do not invoke bare `python3` or select `.claude/hooks` from a worker checkout. The Stop gate does not invoke bare `bash` or a worker checkout's `scripts/agent-stop-gate.sh`.

   Every hook entry carries `onFailure: "block"`. Existing event functions remain available to the anchored orchestrator. They are no-ops in worker sessions because the guard rejects their launch roots.

   `tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_every_tracked_project_hook_is_guarded_and_blocks_on_failure` traverses every event, matcher and command entry. It rejects unguarded commands, missing failure policy, missing `/usr/bin/env -i` prefixes with the specified environment, relative interpreters and worker-selected executable paths.

10. `home/dot_local/bin/common/executable_herdr-agents` supplies the dedicated worker configuration at the actual worker launch boundary.

    Every Claude worker pane starts with `CLAUDE_CONFIG_DIR=<absolute-home>/.claude-worker`. This value reaches the actual worker process through the pane command and environment construction. Setting it only in the parent spawn process does not satisfy this requirement.

    Managed-workspace and standalone-worker routes receive the same binding. Repeated starts do not inherit a conflicting caller Claude configuration directory. This task introduces no worker gh configuration directory, gh templates or credential-separation claim.

    Every worker launch exports `UV_CACHE_DIR=<absolute-worktree>/.uv-cache` and `UV_PYTHON_INSTALL_DIR=<absolute-worktree>/.uv-cache/python`. Both worker kinds receive values derived from the selected canonical worktree. Caller-provided values do not replace them.

    The launcher stops writing Claude worker delivery hooks and merge denials into worktree-local `.claude/settings.local.json`. It renders the worker delivery hooks and native merge denials into `~/.claude-worker/settings.json`, the user-level settings file selected for that directory.

    Before every Claude worker start, managed worker delivery entries are regenerated from trusted inputs. An existing delivery match does not skip preparation. Stale managed commands are replaced, unknown command hooks are not promoted into the trusted delivery set and the effective delivery set contains no duplicate managed invocation.

    The launcher also regenerates its managed hooks in the main checkout's `.claude/settings.local.json`. Every local agmsg delivery and orchestrator attachment command that it writes runs through the installed orchestrator-only guard. The existing permissions object and unrelated non-hook settings remain stored. Their effective sandbox interpretation follows the administrative managed policy.

    Every command hook in both `~/.claude-worker/settings.json` and the main checkout's `.claude/settings.local.json` starts with `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<rendered home> LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}"` before its absolute interpreter and script path. The prefix removes inherited `BASH_ENV` before Bash starts and explicitly re-exports the launch identity and documented hook variables. Agmsg delivery prefixes additionally re-export `AGMSG_RESOLVE_PROJECT=0` and `AGMSG_STORAGE_PATH` when the latter is set in the launcher environment, so the clean environment does not re-enable project resolution from the writable `run/proj.<pid>.project` marker. Every entry carries `onFailure: "block"`. Main-local hooks loaded by a worker session execute no guarded payload.

    Worker settings retain existing native merge denials. They add no user excluded commands, Herdr socket allowance, unsandboxed requests or orchestrator hooks. Shared managed exclusions and socket access remain effective.

    Codex launches retain `--sandbox workspace-write`, `--ask-for-approval never` and `sandbox_workspace_write.network_access=true`. Tests inspect effective launch arguments rather than inferring them from the base manifest.

    The retained Codex Git grant permits shared `.git/objects`, `.git/refs`, `.git/logs` and the worker's administration directory. It does not authenticate local ledger content and is not represented as a host security boundary.

    `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_every_worker_launch_receives_dedicated_policy_and_private_caches` covers both worker kinds and all launch routes. `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_repeated_worker_start_replaces_stale_managed_hooks` covers repeated preparation.

    `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_launch_adds_no_unsandboxed_route` checks that worker launch construction adds no outside-sandbox command route, worker user exclusions or socket allowances and retains native merge denials. It separately records the shared managed exceptions and does not claim that empty user arrays remove them.

    `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_linked_worktree_uses_worker_user_hooks_and_guarded_main_local_hooks` asserts that worker hooks are written to worker user settings, worker preparation writes no worktree-local settings file and main-local agmsg and attachment hooks execute no payload under a worker launch root. An anchored orchestrator invocation still reaches the expected fixture payloads.

    `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_every_settings_hook_has_system_path_prefix` exhaustively traverses both settings files after initial preparation and repeated starts. It asserts the literal `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<rendered home> LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}"` prefix on every command hook before the absolute interpreter and script path and that a planted `BASH_ENV` in the hook's inherited environment does not run. The planted-`BASH_ENV` case is red against the current PATH-only form. The test also asserts `AGMSG_RESOLVE_PROJECT=0` in every agmsg delivery prefix and preservation of `AGMSG_STORAGE_PATH` when set in the launcher environment. It invokes the delivery resolver through the rendered prefix with an explicit worker path and a conflicting writable `run/proj.<pid>.project` marker and asserts that the resolver retains the explicit worker path.

11. `home/dot_local/bin/common/executable_herdr-agent-state.sh` provides the repository-owned Herdr state helper installed as `~/.local/bin/common/herdr-agent-state.sh`.

    The currently installed `~/.claude/hooks/herdr-agent-state.sh` is generated by Herdr and is not a tracked source in this repository. Its bare `python3` descendant is not retained as a trusted worker hook. The repository-owned helper preserves the required state-reporting function and receives its absolute Python interpreter through the rendered invocation.

    Every hook command invokes its entrypoint with a selected absolute interpreter and absolute script path. Repository-owned shell descendants use absolute shebangs or explicit absolute shell invocations. Python descendants use the selected absolute interpreter with `-I`.

    Upstream agmsg scripts retain their `/usr/bin/env bash` shebangs and direct calls to other installed agmsg scripts. The `PATH=/usr/bin:/bin` supplied by the delivery hook's `/usr/bin/env -i` prefix propagates to those descendants, so their Bash resolution uses the system directories without reaching host shims. The installed upstream files are neither edited nor vendored.

    The delivery inventory names `~/.agents/skills/agmsg/scripts/session-start.sh`, `~/.agents/skills/agmsg/scripts/session-end.sh`, `~/.agents/skills/agmsg/scripts/check-inbox.sh`, `~/.agents/skills/agmsg/scripts/identities.sh` and every additional delivery descendant actually reached.

    The inventory records source ownership, installed path, caller, entrypoint interpreter and inherited PATH for each reached script. Binding only the first command does not establish descendant coverage.

    The inventory separately records the current `storage.sh` route from writable team configuration to driver sourcing. A `drivers.partition` value such as `../../../db/payload` can select a planted driver file during unsandboxed delivery. Fixed PATH does not mitigate that selection. The upstream fix belongs to `dotfiles-T133-agmsg-hardening-a01` as recorded in the acceptance record's ownership section.

    No worker hook added by this task introduces store-derived driver sourcing beyond the behavior of the currently installed agmsg scripts. This task neither implements nor claims the upstream validation.

    `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_hook_descendants_do_not_execute_path_interpreters` executes the fixture hook routes with planted Python and Bash shims. It includes a directly executed descendant with an `/usr/bin/env bash` shebang, checks descendant markers and records actual interpreter identities and inherited PATH. Capturing launcher command strings alone does not satisfy this test. Its result does not close the store-driver residual.

12. `home/dot_agents/skills/agmsg-orchestration/SKILL.md` changes only the Worker Playbook step 4 sentence that lists outside-sandbox worker commands.

    The replacement sentence is: “Every worker command, including gh, git push and authenticated git fetch, runs inside the worker's sandbox; no worker command runs outside it.”

    This sentence governs worker execution. Historical TLS, keyring, artifact-writing and delivery exceptions elsewhere in the playbook provide no authorization to leave the sandbox. Shared managed control-plane exceptions provide no worker authorization either. An unavailable operation produces a blocked PONG with its exact command and boundary.

    `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_playbook_requires_every_command_inside_sandbox` checks the replacement and removal of the former three-command exception sentence.

13. `.gitignore` adds only `.uv-cache/`.

    Section 5.14 item 9 fixes trusted orchestrator consumers to `UV_CACHE_DIR=<anchored-checkout>/.agents/worklog/uv-cache`, places managed Python installations beneath that cache and uses `--offline`. Those consumers execute no dependency content from worker caches, shared uv caches or mise caches. Their owning hardening tasks implement the consumer changes.

    This task's static deny inventory explicitly protects both `.agents/worklog/**` and `.agents/worklog/uv-cache/**` beneath the anchored checkout. Their gitignored status does not remove them from the inventory.

    This task's hooks use standard-library Python and absolute shell interpreters without uv. The existing `.agents/worklog/` ignore covers the orchestrator cache.

14. The five allowed test modules reuse existing render, merge, fake-launcher and temporary-HOME fixtures.

    Tests are written before implementation and retain identified base-failure and implementation-success evidence. A missing new entrypoint supplies its baseline failure.

    Worker settings tests cover both platforms, exact static manifest correspondence, current-checkout filesystem coverage, every protected path category, directory targets, descendants, both worklog patterns, ordinary worktree writes, the worktree `.claude` and `.mcp.json` denies, writable agmsg stores, stale settings and the absence of the removed boundary hook.

    Managed settings tests cover the exact rendered policy, conflicting project and local sandbox relaxations, shared control-plane exclusions, shared Herdr socket access and staging without privileged execution. They distinguish worker user settings from the effective shared policy.

    Path fixtures cover symlink components and filesystem case aliases. They verify inventory and configuration identities without presenting a simulated permission matcher as proof of Claude runtime enforcement.

    Hook tests cover every generated and tracked entry's failure policy, worker user settings, guarded main-local settings, the `/usr/bin/env -i` prefix with explicit hook-variable re-exports, complete rendered-command positive and worktree-negative cases, role-specific pinned PATH bindings, suppression of a planted inherited `BASH_ENV` and actual descendant execution. They distinguish synchronous policy hooks from background delivery and post-action events.

    `onFailure: "block"` requires Claude Code v2.1.295 or later and has no enforcement effect on background hooks or the documented excluded events. [Claude hook failure reference](https://code.claude.com/docs/en/hooks#block-the-action-when-a-hook-fails)

    Tests create no identities, initiate no login and access no real credential store. No fixture result is represented as proof of credential isolation, live managed enforcement or upstream agmsg hardening.

15. `.orchestration/dotfiles-T133-worker-write-boundary-a01/` contains the byte-identical dispatched `task.md`, `report.md`, `validation.md`, `sandbox.md`, `learning.md`, `autoskill.md` and worker review evidence.

    The report maps each of the third C-80 review's five findings, fourth C-80 review's six findings and fifth C-80 review's three findings to the revised mechanism, its tests and its remaining residual or owning task. It distinguishes policy configuration from live enforcement and deployment.

## Out of scope

The worker-write-boundary Python hook, its hook entries and `tests/unit/test_worker_write_boundary.py` are dropped. The gh-trusted wrapper remains dropped. The worker gh configuration directory, its templates and the dedicated-identity implementation are removed from this task.

D-024-23 establishes that `GH_CONFIG_DIR` does not separate same-macOS-user Keychain access. A separate OS user or host is required for prevention of worker-initiated merges. Future P1-16 remains the operator's decision. This task implements no credential-separation substitute.

The permission guard and merge gate remain P1-14 a05's work. P1-14 a05 and P1-6 implement the regime rule that approvals and gate evidence of record come from GitHub at a SHA through its API inside the sandbox. The GitHub boundary is detection, not prevention.

For the committed approval ledger, the regime obtains the commit SHA returned by `git ls-remote origin refs/heads/main` and reads `gh api repos/<owner>/<repo>/contents/.orchestration/decisions.tsv?ref=<sha>` inside the sandbox. The consuming implementation reads the API response's file content at that exact SHA. It does not fall back to local files, local refs or local object traversal.

A working-copy decision remains a proposal until its record PR reaches main. This task writes no approval row and implements no local-object substitute for GitHub authority. Shared credentials can still authorize a worker-initiated merge. P1-11 owns the main-push CI flag for missing acceptance or gate evidence under the detection rule.

The upstream agmsg driver-selection fix belongs to `dotfiles-T133-agmsg-hardening-a01`. Its recorded scope validates the `drivers.partition` driver name as an allowlisted basename without path separators before sourcing and supplies an adversarial red-then-green test. This task leaves the shared stores writable and records the current sourcing route as a residual. The ownership section identifies that upstream task as a task to be written; this text does not claim that its fix or test exists.

Permgate code and deterministic policy remain the operator's responsibility. The worker prepares the operator step that stops the Codex permgate policy from approving sandbox escapes. The worker performs no live policy edit or escape probe.

The operator logs into Claude once with `CLAUDE_CONFIG_DIR=<absolute-home>/.claude-worker` selected. The Claude Keychain entry is keyed to that directory. This Claude login does not authenticate or isolate gh.

Administrative installation of `/Library/Application Support/ClaudeCode/managed-settings.json` on macOS and `/etc/claude-code/managed-settings.json` on Linux is the operator's step. The worker implements rendering, staging and the printed installation command without running sudo or installing live managed settings.

The documented file-tool checks reduce symlink redirection risk. A same-UID process can race filesystem changes, alter host-local state or execute outside a seat sandbox. The remaining interval between permission checks and path consumption is a residual under section 5.14 item 0. This text makes no claim that the worker could already write every redirected target directly.

The managed Herdr socket allowance stays available to every seat. Per-seat socket removal is unavailable in that shared scope. Shared control-plane exclusions, socket RPC, hooks, approved MCP processes and other processes outside every seat sandbox retain their stated host trust. The configuration is not represented as same-UID adversarial isolation.

`onFailure: "block"` supplies runtime failure behavior where Claude supports it. Python exit-status tests do not establish timeout handling by the runtime. Background hooks and events on which the field has no effect perform no security enforcement in this design.

Consuming-helper snapshots, reservation locks, the common trusted-execution test helper and orchestrator review-worktree relocation remain with their owning hardening tasks. Codex writable-root grants remain unchanged.

The worker edits neither `.orchestration/decisions.tsv` nor other tasks' canonical texts, evidence or acceptance records. It performs no authentication change, keyring mutation, ruleset mutation, administrative installation, live settings application, global installation, operator restart or merge.

## Check

`make render-check`, `make validate-agent-assets` and `make format` pass.

Shellcheck and shfmt cover the changed shell sources, including the launcher, orchestrator-only guard and repository-owned Herdr state helper. Added or changed shell comments use English shdoc-compatible annotations. Changed Python receives the repository's Python formatting and lint checks.

`uv run python -m unittest tests.unit.test_generate_agent_configs tests.unit.test_claude_settings_merge tests.unit.test_herdr_agents tests.unit.test_claude_worker_settings tests.unit.test_claude_managed_settings -v` is green. The validation record contains every named red-then-green selector and the complete final module run.

The final diff has at most 700 changed lines outside `tests/` and `.orchestration/`, excluding the regenerated `home/.chezmoitemplates/claude-settings-managed.json`, `home/.chezmoitemplates/claude-worker-settings.json` and `home/.chezmoitemplates/claude-managed-settings.json`. It has at most 800 changed lines under `tests/`. Changed lines are additions plus deletions. The validation record includes per-file numstat, base and head identities and both totals.

The validation record contains exact commands, verbatim outputs, exit statuses and tested identities. Git commands producing that evidence follow section 5.14 item 2.

Both platform renders show separate worker and orchestrator user settings, exact manifest deny-inventory correspondence, filesystem coverage of current tracked top-level source paths, both worklog denies, ordinary worktree writes, the worktree `.claude` and `.mcp.json` denies, narrow home denies, writable agmsg stores, empty worker user exclusions, restricted worker writes and `failIfUnavailable: true` for every Claude seat.

Managed render evidence asserts sandbox enablement, startup failure, disabled unsandboxed retries, the required anti-weakening Boolean values, exactly the three rendered control-plane exclusions and exactly the Herdr socket allowance. Conflicting project and local fixtures leave that render unchanged. The evidence names the documented enforcement scope without claiming live runtime verification.

Staging evidence shows the home-directory output and exact printed `sudo install -m 0644` command with the detected administrative destination on both macOS and Linux. The temporary-HOME test proves that the target executes no sudo command.

Hook evidence inventories every generated and tracked entry, its `onFailure` value, `/usr/bin/env -i PATH=<pinned> HOME=<rendered home> LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}"` prefix, installed script, absolute entrypoint interpreter and reached descendants. It includes worker user settings and main-checkout local settings. Render evidence shows that `ruff`, `prettier` and `terminal-browser` resolve under the guard's rendered orchestrator tool PATH on the rendering host and that no PATH entry is a shims directory. Merged-settings evidence identifies runtime-added entries separately. No report claims complete effective failure-policy coverage from template inspection alone.

Launch evidence shows both cache variables reaching the actual worker process on every route. Claude processes additionally receive the dedicated Claude configuration directory. Repeated-start evidence shows replacement of stale managed hooks, retained native merge denials and explicit Codex sandbox and network arguments.

Linked-worktree evidence shows worker hooks in the worker configuration directory's user settings and no new worker-local `.claude/settings.local.json`. Guard markers show that the main checkout's local agmsg and attachment hooks execute no payload under worker launch roots.

Guard markers also show that worker project scripts, contextdb hooks, Stop gates and formatter payloads do not execute through tracked hooks. Descendant markers show that planted PATH interpreters do not execute on the tested hook routes, including an upstream-style `/usr/bin/env bash` descendant.

The report separately identifies the writable agmsg store's current driver-selection route and `dotfiles-T133-agmsg-hardening-a01` ownership. Hook interpreter tests do not claim to close that residual.

The report states the GitHub API ledger rule without claiming this task implements the permission guard or the P1-11 main-push flag. It states detection, not prevention, and records D-024-23's future P1-16 decision. It also records shared managed exclusions and Herdr socket access, same-UID credential access, path-consumption residuals, external-process trust, hook-event failure limitations and the retained Codex shared Git grant.

No local Bats tests run. Required Bats results come from GitHub Actions. Failed required checks retain their actual output and receive an in-scope fix before RESULT.

The orchestrator runs `uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py .orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md` before dispatch and at acceptance. C1 to C10 and C7b pass.

A C-80 security-profile context reviews this complete revised text before dispatch. That review is a dispatch prerequisite and is not claimed as a result of this draft.

## Completion

One implementation PR starts from a fresh branch off `origin/main`. The first push includes the byte-identical dispatched task at `.orchestration/dotfiles-T133-worker-write-boundary-a01/task.md`.

The Completion clauses of `.orchestration/tasks/dotfiles-T133-permission-guard-gate-a05.md` apply with this task's branch, files and evidence paths, `dotfiles-T133-worker-write-boundary-followup-a01` as the owner of any advisory P2, and `task_copy=<sha256 of .orchestration/dotfiles-T133-worker-write-boundary-a01/task.md>` in RESULT. The a05-specific continuation of PR #420, predecessor-copy deletion, inherited counters, deadline and implementation requirements do not transfer. The orchestrator writes the follow-up owner task before assigning its first advisory P2.

Every worker-side fix round counts toward INV-6. The worker's own pre-push review is one round at most. A surviving P0/P1 is sent in RESULT as open and stops integration. The worker starts no additional private correction-and-review cycle to avoid reporting it.

No `@codex review` comment is posted. Automatic final-head reviews are observed within the bounded 15-minute window, and absence is recorded as `bot: none`. Required GitHub Actions checks pass before RESULT. Every feedback item carries its proposed disposition, and surviving P0/P1 findings remain open for the operator's decision.

Every gh write and every git write runs as a separate command without shell chaining. Every worker command remains inside its sandbox. An operation that cannot complete there produces a blocked PONG with the exact command and boundary.

The Codex worker writes evidence at the required relative paths in its own worktree and says so in RESULT. Worker review evidence uses the `-worker-` infix. Crit-data evidence and its receipt follow repository rules without a browser review or human review request. The orchestrator copies evidence by absolute path before acceptance.

`AGMSG-RESULT v1` names the final head, base, branch, changed files, new deployable scripts, source and installed paths, trusted anchor, interpreter and descendant inventory, hook PATH bindings, user and administrative settings destinations, staging path and printed installation command, Bot findings and proposed dispositions, open P0/P1 findings, exact test selectors, measured caps, task-copy SHA256 and evidence paths. It distinguishes historical observations from final-head results and names all pending operator steps.

The report states the user-visible effects. Claude workers use `~/.claude-worker` and require its own Claude login. Worker trusted-path and worktree-configuration Edit denies also affect Bash sandbox writes. Agmsg store paths remain writable except `~/.agents/skills/agmsg/db/trusted-plugins`, and worker denies also cover `~/.agents/skills/agmsg/plugins/**`. Worker user settings add no excluded commands or Herdr socket allowance, while shared managed settings retain the three control-plane exclusions and Herdr socket for every seat. Tracked and main-local orchestrator project hooks are no-ops in worker sessions. Worker caches are private. Every Claude seat fails when its sandbox is unavailable. Codex workers have in-sandbox network access.

Administrative managed settings require sandboxing for the orchestrator as well as workers and disable unsandboxed retries. The former Linux gh exemption is removed. The orchestrator retains its existing functions within those requirements and the specified hook failure, guarding and interpreter/PATH-binding changes.

The report states that no gh credential separation is established. Shared credentials permit worker-initiated API merges despite native command denials. The GitHub boundary is detection, not prevention, with the required main-push flag owned by P1-11.

This task is `security: true`. The orchestrator obtains the task-level audit and a separate security-profile review of the final implementation head. The finding-class record includes `decision-not-bound-to-execution`, `unbound-evidence` and `fail-open-on-error`. A third non-advisory finding of one class stops the artifact for redesign under the inherited completion rules.

Final-head feedback collection, task-level audit, finding dispositions, acceptance and the integration gate follow Orchestrator Playbook step 10 in its prescribed order. The gate receives `PR_FEEDBACK_EVIDENCE`, `AUDIT_EVIDENCE`, `ACCEPTANCE_EVIDENCE` and the agent review receipt. Changed heads receive fresh required evidence. The final-head security review precedes the gate.

The permission-surface change receives the required operator-backed approval through the repository's existing process. The worker writes no approval row and treats no candidate-tree decision as authority.

Live deployment is the operator's post-merge `make update`. The operator runs `make install-managed-settings`, inspects the rendered staging file and executes its printed `sudo install -m 0644 "<absolute-home>/.claude/managed-settings.rendered.json" "<detected-managed-settings-path>"` command with `/Library/Application Support/ClaudeCode/managed-settings.json` detected on macOS and `/etc/claude-code/managed-settings.json` detected on Linux. Administrative installation is recorded separately from staging and ordinary chezmoi application.

The operator performs the Claude worker-directory login with `CLAUDE_CONFIG_DIR=<absolute-home>/.claude-worker` selected.

The operator applies the prepared deterministic Codex permgate rule that stops approving sandbox escapes and restarts affected sessions.

The deployment record checks effective settings after `make update` and administrative installation, including hooks added by merge scripts or integration installers. It verifies the installed managed-settings content, admin-required sandbox scope, worker directory, both platform policy outputs, static deny inventory, worktree-configuration denies, writable agmsg stores, worker-user and main-local hook placement, hook PATH and interpreter descendants, failure-policy coverage and sandbox startup without exposing credentials.

The effective-settings check includes conflicting project and local sandbox relaxations and confirms that they do not weaken the administrative policy. It also records the shared control-plane exclusions and Herdr socket as available capabilities. It makes no claim that worker user arrays subtract those entries.

Merge alone does not establish deployment readiness. The orchestrator records `make update`, the managed-settings installation with sudo, the Claude worker-directory login, effective startup checks and the Codex permgate rule before releasing dependent hardening tasks for live operation. The upstream agmsg store-driver route remains a named residual until its owning task is implemented. GitHub remains detection, not prevention, until the operator pursues separate-user or separate-host isolation under future P1-16.

## Checks (pasted by the orchestrator before each send)

```
2026-10-19T05:4xZ dispatch 1 (plan 024 P1-15, D-024-17/19/20/21/22/23)
task=dotfiles-T133-worker-write-boundary-a01 tasks=0 amendments=0 questions=0 results=0 withdrawn=0 revises=0 source=live
C-80: text-security review rounds 1-8 incorrect (7,7,5,6,3,3,2,3 findings), round 9 Verdict: correct (.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-435275a.md.last.md)
C-78: no in-flight task edits these code files; SKILL.md is shared with the RESULTed P1-8 (#427) in a disjoint section; the later PR update-branches
task-consistency-check: OK
```

Local Bats, live enforcement, administrative installation, worker-directory login, permgate policy changes and deployment are not performed by the worker.
Deployment remains unverified until the operator completes the post-merge steps; same-UID credential access, shared control-plane exclusions and Herdr socket access, writable-store driver selection and concurrent path consumption remain stated residuals.
 succeeded in 448ms:
Found four security issues in [PR #417](https://github.com/mryfmo/dotfiles/pull/417), at head `8a09b9365932f23b09df8aa2385a93d0b3016a3e`:

1. **P1 · High confidence · `scripts/orchestrator/task-from-plan.py:114`** — A clean, committed PR HEAD is treated as authorization to execute its plan commands; no trusted revision or operator-supplied digest establishes that these are the orchestrator’s approved text. The mocked execution probe reached an unreviewed HEAD’s command. This undermines the generator and in-process threat controls.

2. **P1 · High confidence · `scripts/orchestrator/task-consistency-check.py:89`** — `<root>/bin` precedes system directories when resolving even `bash`, so a checkout-controlled `bin/bash` executes despite a valid trusted task hash and an unchanged harmless premise. The hash authenticates command text, not its interpreter. Use a trusted interpreter and executable search path.

3. **P1 · High confidence · `scripts/orchestrator/task-from-plan.py:228`** — The output write follows existing symlinks without validating the destination; a checkout-provided `.orchestration/tasks/P1-1.md` symlink can redirect generation onto another repository file, such as `scripts/orchestrator/dispatch.sh`, and truncate it. The clean-plan check does not cover this output path.

4. **P2 · High confidence · `scripts/orchestrator/plan-check.py:86`** — Task-controlled absolute/traversal globs and directory symlinks can enumerate outside `--root`, exposing filenames in overlap diagnostics and permitting uncontrolled recursive traversal. A read-only probe with `/etc/hos*` returned outside-root paths. The plan-check row’s cited test does not close this boundary.

The C14 same-byte hash check, C10 `git grep -e` fix, C6 confinement, and `yaml.safe_load` usage hold under inspection. The other threat rows showed no additional security defect; external acceptance controls remain the orchestrator’s responsibility. Existing regime CI continues to execute the base verifier, not PR-head code.

📝 まとめ: Completed the pinned security review and identified four findings; acceptance remains with the orchestrator.

Not checked: write-dependent tests and live CI (`gh` connectivity failed); no files changed. Local execution and filesystem-boundary risks remain.
Verdict: incorrectAudited [PR #417](https://github.com/mryfmo/dotfiles/pull/417) at `8a09b936`.

- [P2] high implementation scripts/orchestrator/task-consistency-check.py:240 C15 accepts a design absent from `origin/main` when it exists locally and the task omits invariants; reproduced with no finding, contrary to item 2’s missing-design requirement.
- [P2] high implementation scripts/orchestrator/task-consistency-check.py:65 C12 excludes agent instruction files such as `.claude/skills/example/SKILL.md`; a wildcard covering these applied rules passes without concrete threat rows.
- [P2] high implementation scripts/orchestrator/task-consistency-check.py:209 An out-of-checkout scope such as `../../outside/*.py` silently skips C12 instead of producing item 20’s required confinement finding.
- [P2] high implementation scripts/orchestrator/task-from-plan.py:137 The slash requirement drops explicitly named repository-root files, including `AGENTS.md`, `README.md`, and `Makefile`; generation can report success with none of the requested edit scope.
- [P2] high implementation scripts/orchestrator/task-from-plan.py:153 A directory scope alongside its child produces a child threat row matching both entries, causing C7b to reject the generated task; reproduced with `scripts/orchestrator/` and a contained file.
- [P2] high implementation scripts/orchestrator/task-from-plan.py:138 Paths remain unnormalized: `./scripts/new.py` can enter `allowed_files`, but the regime verifier rejects the corresponding Git path `scripts/new.py` when no grep hit supplies a canonical entry.
- [P2] high implementation scripts/orchestrator/task-from-plan.py:72 Unavailable single-word commands are discarded through `shutil.which`; item 15 requires retaining them with actual failure status, but `is_command("no-such-tool-a02")` returns false.
- [P2] high implementation scripts/orchestrator/plan-check.py:116 F1 checks only whether the last supplied cell is nonempty; a todo row missing its completion cell entirely passes because its work cell is mistaken for completion.
- [P2] high evidence tests/unit/test_task_consistency_c11_c15.py:166 The edited-file case recomputes the edited file’s trusted SHA through `self.check(edited)`; it never tests item 7’s required rejection of changed bytes using the original dispatched SHA.
- [P2] high orchestration .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a02.md:37 Amendment 1 supplies `tests/...::RegimeCiTest::test_...`, which C11 rejects; directly checking the byte-identical final task produces a structural failure.
- [P2] high orchestration .orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-pr-feedback.json:130 The template finding remains dispositioned `fixed:b3c6b7ea`, although that commit merely improved the missing-file error; item 5 requires superseding this disposition with the actual bundled-template fix, `eb20d063`.
- [P2] high orchestration .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a02.md:130 Four non-advisory `parser-gap` entries have no required pasted correction-record search; the empty `searches.records` assertion does not supply the mandated command/output or `search:` line.

INV-6: violated .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a02.md:130 — the repeated-class search evidence is missing.

Orchestration findings: 3

📝 まとめ: Read-only audit completed; task-copy SHA and both diff caps verified. Filesystem-writing suites were not rerun; live CI remains unverified because both `gh` and web access failed.
Verdict: incorrect- [P1] high .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a03.md:139 — C14 authenticates shell text but does not constrain its executable file operands: an unchanged `python -I scripts/probe.py` or `source ./probe.sh` still executes checkout-controlled bytes; trusted interpreters, PATH and task snapshots do not bind those files. Likewise, binary links cannot inject the required Git flags into shell descendants, leaving `git status` exposed to checkout-configured fsmonitor execution. [Python semantics](https://docs.python.org/3/using/cmdline.html#cmdoption-I), [Git configuration](https://git-scm.com/docs/git-config#Documentation/git-config.txt-corefsmonitor).

- [P1] high .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a03.md:223 — The specified `uv run --no-project … python -I` launch still discovers current/parent virtual environments and persistent configuration; adding a private cache, trusted PATH and `--offline` does not bind uv’s selected interpreter or dependencies to that cache. Require explicit trusted interpreter/environment selection and disabled configuration discovery, with a hostile `.venv` fixture. [uv environment selection](https://docs.astral.sh/uv/reference/cli/#uv-run--no-project), [configuration discovery](https://docs.astral.sh/uv/concepts/configuration-files/).

- [P1] high .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a03.md:75 — The sandbox claim has no deployment prerequisite: the current manifest retains `failIfUnavailable: false` and Linux’s `gh *` exclusion, so execution can escape automatically without producing the denial that triggers blocked PONG; require verified effective sandbox settings before dispatch. [Current configuration](~/Workspace/dotfiles/home/dot_agents/agent-config.yaml:276).

📝 まとめ: Reviewed the task, all threat rows, and cited acceptance/review context; identified three execution-binding gaps for orchestrator disposition.

Not checked: implementation tests or live Linux enforcement; no files changed. Declared controls remain insufficient for the execution paths above.
Verdict: incorrect
 succeeded in 531ms:
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
?? .orchestration/validation/dotfiles-T133-ci-efficiency-followup-a02-chain-7329f0e.log
?? .orchestration/validation/dotfiles-T133-ci-efficiency-followup-a02-chain-c013846.log
?? .orchestration/validation/dotfiles-T133-ci-efficiency-followup-a02-local-review-7329f0e.md
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
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a03-text-security-8ce8dba.md
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
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-ecc7ab5.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-ecc7ab5.md.last.md
{
  "lastAnalyzedAt": "2026-10-02T14:12:51Z",
  "gitCommitHash": "940a3a2b07adfd14140a0acff96784ef53a0a509",
  "version": "1.0.0",
  "analyzedFiles": 368
}
b22a5580d0778e57a66d3f75c76e3c55b88701e1

**Avoiding batch outputs**
exec
/bin/zsh -lc 'cat .orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-security-8a09b93.md.last.md .orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-audit-8a09b93.md.last.md .orchestration/validation/dotfiles-T133-task-generator-plan-check-a03-text-security-f6797ab.md.last.md' in ~/Workspace/dotfiles
 succeeded in 0ms:
Found four security issues in [PR #417](https://github.com/mryfmo/dotfiles/pull/417), at head `8a09b9365932f23b09df8aa2385a93d0b3016a3e`:

1. **P1 · High confidence · `scripts/orchestrator/task-from-plan.py:114`** — A clean, committed PR HEAD is treated as authorization to execute its plan commands; no trusted revision or operator-supplied digest establishes that these are the orchestrator’s approved text. The mocked execution probe reached an unreviewed HEAD’s command. This undermines the generator and in-process threat controls.

2. **P1 · High confidence · `scripts/orchestrator/task-consistency-check.py:89`** — `<root>/bin` precedes system directories when resolving even `bash`, so a checkout-controlled `bin/bash` executes despite a valid trusted task hash and an unchanged harmless premise. The hash authenticates command text, not its interpreter. Use a trusted interpreter and executable search path.

3. **P1 · High confidence · `scripts/orchestrator/task-from-plan.py:228`** — The output write follows existing symlinks without validating the destination; a checkout-provided `.orchestration/tasks/P1-1.md` symlink can redirect generation onto another repository file, such as `scripts/orchestrator/dispatch.sh`, and truncate it. The clean-plan check does not cover this output path.

4. **P2 · High confidence · `scripts/orchestrator/plan-check.py:86`** — Task-controlled absolute/traversal globs and directory symlinks can enumerate outside `--root`, exposing filenames in overlap diagnostics and permitting uncontrolled recursive traversal. A read-only probe with `/etc/hos*` returned outside-root paths. The plan-check row’s cited test does not close this boundary.

The C14 same-byte hash check, C10 `git grep -e` fix, C6 confinement, and `yaml.safe_load` usage hold under inspection. The other threat rows showed no additional security defect; external acceptance controls remain the orchestrator’s responsibility. Existing regime CI continues to execute the base verifier, not PR-head code.

📝 まとめ: Completed the pinned security review and identified four findings; acceptance remains with the orchestrator.

Not checked: write-dependent tests and live CI (`gh` connectivity failed); no files changed. Local execution and filesystem-boundary risks remain.
Verdict: incorrectAudited [PR #417](https://github.com/mryfmo/dotfiles/pull/417) at `8a09b936`.

- [P2] high implementation scripts/orchestrator/task-consistency-check.py:240 C15 accepts a design absent from `origin/main` when it exists locally and the task omits invariants; reproduced with no finding, contrary to item 2’s missing-design requirement.
- [P2] high implementation scripts/orchestrator/task-consistency-check.py:65 C12 excludes agent instruction files such as `.claude/skills/example/SKILL.md`; a wildcard covering these applied rules passes without concrete threat rows.
- [P2] high implementation scripts/orchestrator/task-consistency-check.py:209 An out-of-checkout scope such as `../../outside/*.py` silently skips C12 instead of producing item 20’s required confinement finding.
- [P2] high implementation scripts/orchestrator/task-from-plan.py:137 The slash requirement drops explicitly named repository-root files, including `AGENTS.md`, `README.md`, and `Makefile`; generation can report success with none of the requested edit scope.
- [P2] high implementation scripts/orchestrator/task-from-plan.py:153 A directory scope alongside its child produces a child threat row matching both entries, causing C7b to reject the generated task; reproduced with `scripts/orchestrator/` and a contained file.
- [P2] high implementation scripts/orchestrator/task-from-plan.py:138 Paths remain unnormalized: `./scripts/new.py` can enter `allowed_files`, but the regime verifier rejects the corresponding Git path `scripts/new.py` when no grep hit supplies a canonical entry.
- [P2] high implementation scripts/orchestrator/task-from-plan.py:72 Unavailable single-word commands are discarded through `shutil.which`; item 15 requires retaining them with actual failure status, but `is_command("no-such-tool-a02")` returns false.
- [P2] high implementation scripts/orchestrator/plan-check.py:116 F1 checks only whether the last supplied cell is nonempty; a todo row missing its completion cell entirely passes because its work cell is mistaken for completion.
- [P2] high evidence tests/unit/test_task_consistency_c11_c15.py:166 The edited-file case recomputes the edited file’s trusted SHA through `self.check(edited)`; it never tests item 7’s required rejection of changed bytes using the original dispatched SHA.
- [P2] high orchestration .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a02.md:37 Amendment 1 supplies `tests/...::RegimeCiTest::test_...`, which C11 rejects; directly checking the byte-identical final task produces a structural failure.
- [P2] high orchestration .orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-pr-feedback.json:130 The template finding remains dispositioned `fixed:b3c6b7ea`, although that commit merely improved the missing-file error; item 5 requires superseding this disposition with the actual bundled-template fix, `eb20d063`.
- [P2] high orchestration .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a02.md:130 Four non-advisory `parser-gap` entries have no required pasted correction-record search; the empty `searches.records` assertion does not supply the mandated command/output or `search:` line.

INV-6: violated .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a02.md:130 — the repeated-class search evidence is missing.

Orchestration findings: 3

📝 まとめ: Read-only audit completed; task-copy SHA and both diff caps verified. Filesystem-writing suites were not rerun; live CI remains unverified because both `gh` and web access failed.
Verdict: incorrect- [P1] high .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a03.md:139 — C14 authenticates shell text but does not constrain its executable file operands: an unchanged `python -I scripts/probe.py` or `source ./probe.sh` still executes checkout-controlled bytes; trusted interpreters, PATH and task snapshots do not bind those files. Likewise, binary links cannot inject the required Git flags into shell descendants, leaving `git status` exposed to checkout-configured fsmonitor execution. [Python semantics](https://docs.python.org/3/using/cmdline.html#cmdoption-I), [Git configuration](https://git-scm.com/docs/git-config#Documentation/git-config.txt-corefsmonitor).

- [P1] high .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a03.md:223 — The specified `uv run --no-project … python -I` launch still discovers current/parent virtual environments and persistent configuration; adding a private cache, trusted PATH and `--offline` does not bind uv’s selected interpreter or dependencies to that cache. Require explicit trusted interpreter/environment selection and disabled configuration discovery, with a hostile `.venv` fixture. [uv environment selection](https://docs.astral.sh/uv/reference/cli/#uv-run--no-project), [configuration discovery](https://docs.astral.sh/uv/concepts/configuration-files/).

- [P1] high .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a03.md:75 — The sandbox claim has no deployment prerequisite: the current manifest retains `failIfUnavailable: false` and Linux’s `gh *` exclusion, so execution can escape automatically without producing the denial that triggers blocked PONG; require verified effective sandbox settings before dispatch. [Current configuration](~/Workspace/dotfiles/home/dot_agents/agent-config.yaml:276).

📝 まとめ: Reviewed the task, all threat rows, and cited acceptance/review context; identified three execution-binding gaps for orchestrator disposition.

Not checked: implementation tests or live Linux enforcement; no files changed. Declared controls remain insufficient for the execution paths above.
Verdict: incorrect
**Reviewing security context**
codex
前回指摘された任意の premise 実行、uv の環境選択、sandbox の配備前提は、今回の本文で修正されています。残る確認点は、Git 設定の検査が実際の有効設定を網羅するか、また信頼済みツールの起動契約が外部コマンドまで届くかです。読み取り専用のため、worklog やレビュー証跡のファイルは作成していません。
exec
/bin/zsh -lc "rg -n -A 78 '"'^### 5.14|''^## 5.14'"' .orchestration/plans/024-design-quality.md" in ~/Workspace/dotfiles
 succeeded in 0ms:
99:## 5.14 信頼ホスト実行契約（trusted-host execution contract、D-024-18）
100-
101-orchestrator 側の仕組み（merge gate、integrate-merge、orch-gate、dispositions、audit-pool、verdict、chain）は、同じホスト上で同じ UID の worker プロセスと共存する。2026-10-19 の C-80 審査（a05、dispositions-a02、audit-pool-a01 の 3 文、計 19 件の P1）は、どの文も同じ前提を書かず同じ穴を持つことを示した。以後、`security: true` の orchestrator 側タスク文は本節を参照で適用し、本節の各項目に対応する threat 行を持つ。文ごとに言い換えない。
102-
103-1. **書き込み境界（前提 6、ランタイム別に正直に）** Claude worker 席は専用の設定ディレクトリ `CLAUDE_CONFIG_DIR=~/.claude-worker`（chezmoi が描画、operator が一度 login）で起動し、orchestrator の `~/.claude` と設定を共有しない。worker 設定：除外コマンド無し、Herdr socket 無し、sandbox の allowWrite は自席 worktree と agmsg store と席別キャッシュだけ、`failIfUnavailable: true`、信頼パス（anchored checkout の `.claude/worktrees/` 以外、`~/.agents`、`~/.claude*`、`~/.local`、`~/.config`）への Edit deny（公式文書：file tool の permission 検査は要求パスと symlink 解決後のパスの両方に deny を適用し、symlink そのものへの書き込みは拒否する）、sandbox の強制範囲はユーザー設定ではなく **managed settings**（`/Library/Application Support/ClaudeCode/managed-settings.json`、公式文書 "Repository settings under an admin-required sandbox"：project/local 設定は sandbox を無効化したり除外・socket を足したりできない）に置く。chezmoi は user ではこのファイルを書けないので、描画した内容を操作者が `sudo` で一度配置する（操作者手順）。worker 設定は worktree 自身の `.claude/**` と `.mcp.json` への Edit deny（`//<anchored>/.claude/worktrees/*/.claude/**`）を持つ（Bash 側は sandbox 既定の settings/hooks の denyWithinAllow）。agmsg store（全席が書く）から配送 hook が driver や plugin を source する上流の経路（storage.sh の `drivers.partition` traversal、`db/trusted-plugins` と `plugins/partition/shared.sh` による差し替え承認）は別タスク（agmsg hardening）の行で、worker 設定は `~/.agents/skills/agmsg/plugins/**` と `~/.agents/skills/agmsg/db/trusted-plugins` への書き込みを deny し（Edit deny は sandbox の deny にも合流する）、hook 側は store 由来の設定値を検証するまで残余と書く。managed settings の配置先は OS で異なる（macOS `/Library/Application Support/ClaudeCode/managed-settings.json`、Linux `/etc/claude-code/managed-settings.json`）。hook は agmsg 配送だけを、hook コマンドを `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<home> …` で始めて（`BASH_ENV` などの継承環境を bash 起動前に消す；PATH 固定だけでは BASH_ENV が先に走る）絶対パスのインタプリタで呼び（上流の agmsg スクリプトは `/usr/bin/env bash` の shebang を持つので、hook 実行環境の PATH が shim を含まないことで束縛する）、各 hook に `onFailure: "block"`。公式文書：linked worktree の session は **main checkout の `.claude/settings.local.json` を読む**ので、worker 向けの hook を worktree の settings.local.json に書いても読まれず、逆に orchestrator の local hooks が worker session でも走る。したがって orchestrator 側の local hooks も guard 経由にし、worker 側の hook は worker config dir の settings に置く。Edit deny の一覧は `git ls-tree` ではなく描画時の静的一覧（manifest に列挙、`.agents/worklog/**` と `.agents/worklog/uv-cache/**` を含む）とし、`~/.agents/**` の全面 deny は agmsg store の書き込みと矛盾するので、`~/.agents/agent-config.yaml`、`~/.agents/skills/**/scripts/**`、`~/.agents/model-profiles.env` などストア以外を列挙する。公式文書で確認した事実（2026-10-19）：`Edit(path)` の deny は Write/MultiEdit/NotebookEdit にも効き、deny → ask → allow の順で最初の一致が決まる；ただし Read/Edit の deny は **Bash sandbox の設定にも合流する**（"Paths and domains from both sandbox settings and permission rules are merged into the final sandbox configuration"）ので、ユーザー設定（全席共有）に `.orchestration/**` の Edit deny を書くと orchestrator の Bash による記録書き込みも止まる。hook は起動時に固定されず、設定ファイルの編集は file watcher が即座に反映する。`sandbox.failIfUnavailable` の既定は fail-open（依存が無ければ sandbox 無しで実行）。したがって Claude 席の境界は Edit deny 規則ではなく、**ユーザーレベルの PreToolUse hook**（`~/.claude/hooks/worker-write-boundary`、chezmoi が描画、`/bin/sh` または絶対パスの `python3 -I`）で作る：cwd の realpath が `<anchored>/.claude/worktrees/` 配下の session では、Write/Edit/MultiEdit/NotebookEdit の対象が cwd の外、または `<cwd>/.claude/**`・`<cwd>/.mcp.json` のとき `permissionDecision: deny` を返す。Bash 側は sandbox の既定 `denyWithinAllow`（settings、hooks）と `allowWrite`（自席 worktree）が担う。`failIfUnavailable: true` を全席に置く。 Codex 席は sandbox（workspace-write）がツールの書き込み全部を自席の worktree と列挙パスに限る。Claude 席は Seatbelt sandbox が Bash を限るだけで、Write/Edit/MultiEdit/NotebookEdit、hook、MCP プロセスは sandbox 外で動き、permission policy（permgate の決定論ポリシー）が path で拒否しない限り anchored checkout や `~/.agents` にも書ける（2026-10-19 時点、描画済み設定にその deny は無い）。したがって前提 6 は「Codex 席は成立、Claude 席は P1-15 が描画設定に Edit の path deny を入れるまで残余」と書く。P1-15 以前に「worker は信頼ルートに書けない」と書く文は誤りで、C-80 が拒否する。P1-15 が入るまで、承認の出所は項目 8 の「コミット済み台帳」で守る。書き込みは自席の worktree（`.claude/worktrees/<name>`）、scratch、列挙されたツールキャッシュに限る。anchored checkout（`.claude/worktrees/` 以外）、`~/.agents/agent-config.yaml`、`~/.claude/hooks`、信頼ルートのバイナリ、orchestrator の証跡・スナップショット・lock は worker から書けない。render テストが描画後の deny を検証する。残余は「どの席 sandbox にも属さない同一 UID プロセス」と、Worker Playbook step 4 が sandbox 外に出す少数のコマンド（gh）。後者は D-024-17（P1-15）で絶対パスの実行体に束縛する。
104-2. **無害化した環境を最初に** 最初の処理として `env -i` に入り、PATH は信頼ルートで解決した絶対バイナリへのリンクだけの私設ディレクトリ（shims、空、相対は拒否）。git は毎回 `GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null -c core.hooksPath=/dev/null -c core.fsmonitor=false -c protocol.allow=never -c protocol.https.allow=always` と明示 `-C`（https だけ許す。`protocol.allow=never` 単独は必要な fetch を止める）。 premise や検査の「コマンド実行」は、固定語彙の読み取り専用プローブ（`git rev-parse <ref>`、`test -e <path>`、`grep -c <pattern> <file>` のように検査器自身が解釈する形）だけを許し、任意のシェル文字列は実行しない（本文のハッシュはコマンド文を認証するだけで、`python -I scripts/x.py` のファイル被演算子や `source ./x.sh` の中身は認証しない）。diff と show は `--no-ext-diff --no-textconv` と `-c core.attributesFile=/dev/null -c core.sshCommand=false` を付け、PR 側の `.gitattributes`（external diff、textconv、filter）が検査内容や実行物を変えないようにする。Python は `-I`。PATH 探索で実行するものは無い。
105-3. **信頼パスの境界検査** 仕組みが信頼するパス（スクリプト、台帳、証跡、worktree、lock、出力先）は realpath で解決し、`.claude/worktrees/` または manifest の worker ルート配下なら拒否（ask/hold）。symlink 構成要素は解決後に比較し、大小文字を区別しないファイルシステムでは同一性比較を大小文字非依存で行う。
106-4. **検証したものを実行し、検証した内容を渡す** 検証した実行体はその realpath で実行する（再探索しない）。検証したファイル内容は信頼ルート配下のスナップショット（0600、一意名）として渡し、使用直前に sha256 を再照合する。判断に読んだ証跡は sha256 を出力に記録する。
107-5. **出力と予約の同一性** 名前には 40 桁の head を使う（7 桁で衝突させない）。lock は信頼ルート配下の固定 inode に O_EXCL で作り、置換を inode 比較で検出する。物理スロット 1 つに lock 1 つ。
108-6. **正直な残余** 境界だけが緩和するリスクを `closed` と書かない。各文は残余を 1 行で明記する。
109-0. **脅威モデル（D-024-21）** 席は同じ OS ユーザで動き、ホストは席間の信頼境界ではない（同一 UID のプロセスは symlink 差し替え、共有 `.git` の object 差し替え、hook の子プロセス、Herdr socket 経由の host 実行で、ホスト内のどの検査も迂回できる）。regime の硬い境界は GitHub（保護された main、必須チェック、orchestrator の identity によるマージ）。ただしこの境界は **worker 席が orchestrator の GitHub 資格情報を共有しない**ときだけ成立する（D-024-22：worker 席は専用の GitHub identity（別アカウントまたは App のトークン）で `gh` に login し、ruleset の bypass 一覧に入らない。orchestrator の keychain トークンを worker の config dir に持ち込まない。identity が分かれるまで「GitHub が境界」は未成立と書く）。**同一 macOS ユーザでは資格情報は分離できない**（gh は keychain の項目を host/user で引き、同じ UID の gh は orchestrator のトークンを読める。`GH_CONFIG_DIR` は設定を分けるだけ）。防止には worker 席を別の OS ユーザ（または別ホスト）で動かすしかなく、それは D-024-23 の将来項目（P1-16、操作者の判断）。それまで GitHub 境界は **検知**で守る：regime CI の main push 実行が、受け入れ記録と gate 通過の証跡を持たないマージを検知して警報を出す（P1-11 lineage の行）。文は「防止ではなく検知」と書く。悪意ある worker に耐えるべき入力（承認台帳、gate が読む証跡 of record）は GitHub から sha 指定で API 経由（sandbox 内）に読み、ローカルファイルやローカル object database からは読まない。ホスト内の制御（本節 1〜10）は事故と prompt injection による損害の抑制であり、文はそう書く。
110-8. **承認はコミット済み台帳から読む** permission の決定行（`scope=permission approved_by=user diff_sha256=…`）は anchored checkout の作業コピーではなく、コミット済みの台帳から読む。読み方は `git ls-remote origin refs/heads/main` が返す commit sha を取り、GitHub API（`gh api repos/<owner>/<repo>/contents/.orchestration/decisions.tsv?ref=<sha>`、sandbox 内）でその sha の内容を取得する。ローカルの `git show` は共有 object database が書けるため中間 tree の差し替えで偽物を返しうる（第 3 回審査の所見 2）（ローカルの ref 名 `origin/main` は経由しない。`refs/replace/` も書けるので replacement を無効にする。Codex worker は `.git/objects` と `.git/refs` に書けるので ref は差し替えられるが、sha で指した object は内容アドレスで偽造できない）。作業コピーの行は提案で、記録 PR が main にマージされて初めて承認になる（PR の承認は操作者の操作）。偽造には main へのマージが要る。
111-9. **私設キャッシュ** orchestrator 側の実行は worker と共有するキャッシュ（`~/.cache/uv`、`~/.local/share/uv`、mise）から実行可能物を読まない。`UV_CACHE_DIR` を anchored checkout 配下（`.agents/worklog/uv-cache`、gitignored、worker 書き込み不可）に固定し、`uv run --no-config --no-project --offline --python <信頼ルートの絶対パスのインタプリタ>` で起動する（`--no-config` で uv の設定探索を止め、`--python` の絶対パスで cwd や親の `.venv` の発見を止める；敵対的な `.venv` と `uv.toml` を置いた fixture で検証）。hook は uv を使わず jq と python 標準ライブラリだけで動く。
112-10. **worker は sandbox 外でコマンドを実行しない（D-024-17 の改訂）** 2026-10-19T03:45Z の実測で `gh api` は Claude sandbox の中から成功した（sandbox の proxy は CONNECT 型で TLS を終端しない；keychain のトークンも読めた）。worker 席の除外コマンドは空にし、gh も git push も sandbox 内の proxy 経由で実行する。Codex 席は `sandbox_workspace_write.network_access = true` で同じ状態にし、permgate の codex ポリシーは sandbox 外への escape を承認しない（permgate の変更は操作者の手順）。wrapper 方式（絶対パス、env -i、固定 GH_CONFIG_DIR）は LD_PRELOAD と引数転送（`gh repo clone -- --config`）を閉じられないので採らない。
113-7. **検証** threat_table は本節の項目 1〜10 に 1 行ずつ対応させる（参照だけでは足りない）。共通テスト補助 `tests/unit/trusted_exec_contract.py`（P1-6 で作る）を使い、仕組みごとに 4 つの red→green テストを持つ：PATH 先頭の shim が実行されない、植え付けた GIT_* と git 設定が効かない、worker ルート配下の信頼パスが拒否される、検証後に差し替えたファイルが消費側に届かない。

exec
/bin/zsh -lc "sed -n '155,180p' .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a03.md; sed -n '250,340p' .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a02.md" in ~/Workspace/dotfiles
 succeeded in 0ms:
2. `scripts/orchestrator/task-from-plan.py` retains its CLI, committed plan-group reads, bundled template, whole-token wave selection, program-item extraction, scope proposals, grep provenance and threat-row generation.

   The clean-plan check remains a data-provenance check for staged, unstaged and untracked changes in the `024-*` group. A clean committed HEAD supplies no authorization to execute its plan text.

   The generator never executes a command extracted from a plan item. It also never executes bundled or plan-derived Check commands. It records each recognized command as text with an explicit `verify:` explanation that execution and verification remain pending. It fabricates no stdout or exit status and distinguishes a missing observation from an observed empty output.

   The generator creates no scratch worktree for Check execution. The former premise runner, scratch Check runner and their execution-only cleanup disappear. Trusted Git calls needed to read committed data and obtain provenance remain under the common execution contract.

   The generator invokes the trusted consistency checker without `--premises-sha`. It does not turn its own computed output digest into permission to execute generated premise text. Structural findings and the C14 not-run warning remain visible. The generated file remains available for editing when structural findings occur.

   `scripts/orchestrator/task-template.md` retains the bundled task-copy, evidence, non-path and orchestrator-effect rows, common Check command text and Completion contract. Its wording describes unverified commands and separate orchestrator verification. It makes no claim that generation ran those commands.

   Existing generation tests change their execution expectations only where this reset changes the contract. Recognized commands remain present as unverified text. The separately owned command-recognition and parser defects remain outside this task.

   `tests/unit/test_task_from_plan.py::TaskFromPlanTest::test_the_generator_never_executes_a_plan_command` is written first and is red against `8a09b9365932f23b09df8aa2385a93d0b3016a3e`. A clean committed plan and bundled Check content contain marker-writing commands. Generation retains their text and unverified status, creates no marker and no scratch worktree, and passes no trusted premise digest to the checker. It is green on the final implementation.

3. `scripts/orchestrator/task-from-plan.py` confines its output to `<root>/.orchestration/tasks/` and creates the destination with `O_EXCL`.

   The generator resolves the root, task directory and destination through realpath before creation. A destination resolving outside the task directory is refused. An existing destination is refused. An existing symlink is refused, including a dangling symlink and a symlink whose target remains inside the task directory.

   Exclusive creation supplies the final leaf-existence check. The generator writes the generated bytes through the exclusively created file and does not reopen the destination through a following write. Refusal leaves existing files, symlink targets and outside-root markers unchanged.

   The destination's confinement and exclusive creation reduce redirection and truncation risks. Concurrent parent-directory replacement by a same-UID process remains the item 0 host residual.

   `tests/unit/test_task_from_plan.py::TaskFromPlanTest::test_the_generator_refuses_a_symlinked_or_existing_output` is written first and is red against `8a09b9365932f23b09df8aa2385a93d0b3016a3e`. It covers an existing ordinary file, existing and dangling symlinks, an outside destination, symlinked parent traversal and successful creation of a fresh confined output. Existing target bytes remain unchanged. It is green on the final implementation.

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

## Bot-thread ledger rows carried from the a01 record (PR #417 round 1 and revise 1 of the a01; fixed:b3c6b7ea and fixed:538e60bd, in 417-extra.tsv; the record step writes no Bot rows)

4306960622	trust-boundary-pr-input
4306960626	missing-input-crash
4306960630	string-form-comparison
- 2026-10-19T04:17-04:19Z: the #417 chain was started twice in the same review worktree (a guarded launch waited for the ledger rows while the orchestrator wrote them and launched again); the second run failed at its fetch step ("git checkout --detach does not take a path argument FETCH_HEAD") and the first stopped on three Bot-thread ledger gaps (4306960622/26/30, dispositioned in 417-extra.tsv but absent from the record's ledger). Rows carried from the a01 record's JSON ledger (trust-boundary-pr-input, missing-input-crash, string-form-comparison) and the chain re-run alone at 04:19Z. Hygiene: a guarded launch is never combined with a later unguarded launch of the same chain; one review worktree per PR (P1-6) removes the collision class.

## Audit of 8a09b936 (2026-10-19T04:28Z): twelve P2, no P0/P1; acceptance with owner rows

- The chain (sweep 7 items 0 gaps; local review 0; the ledger completed by hand with the 15 lineage rows of 9da0ed3 and the 3 Bot rows) ran the audit (`.orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-audit-8a09b93.md`): `Verdict: incorrect` on twelve P2: nine implementation (C15 local-design acceptance; C12 scope and confinement gaps; task-from-plan.py root files, directory-with-child rows, unnormalized paths, discarded single-word commands; plan-check.py F1 cell), one evidence (the edited-file SHA test), three orchestration (C11 rejects the `::Class::test` selector form amendment 1 uses; the template thread's `fixed:b3c6b7ea` should be `fixed:eb20d063`; the parser-gap class lacks its search evidence). Task-copy SHA and both caps verified by the auditor.
- counters: tasks=1 amendments=1 (the CI-repair amendment) results=2 revises=0; worker rounds 2 (pre-push review, CI repair): the C-61 cap.
- decision: no worker round (the cap; no P0/P1). The nine implementation P2 and the evidence P2 are advisory rows of the P1-12 owner `dotfiles-T133-task-generator-plan-check-followup-a01`, dispatched to a009 right after this merge with the C11 grammar as its first row (the regime's selector convention is the pytest node id with an optional class; C11's narrower grammar would make dispatch.sh refuse the next texts, so the owner fix lands first and no text is dispatched through a C11-bearing checker before it). The template disposition is corrected in 417-extra.tsv. The parser-gap class (rows audit:9da0ed3:10-13, audit:8a09b93:7-8) gets its re-plan in the JSON block and the search below.

search: grep -l 'parser-gap' .orchestration/learning/mistakes/*.md → (no record; M-20261019-04 written now)

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

## Owned by dotfiles-T133-task-generator-plan-check-followup-a01

- `audit:8a09b93:10` selector-grammar (first): C11 accepts the pytest node id `tests/unit/<module>.py::<Class>::<test>` and `::<test>`; red against 8a09b936 with the a02 copy itself.
- `audit:8a09b93:1` C15 requires the design on origin/main; `audit:8a09b93:2` C12 covers agent instruction files; `audit:8a09b93:3` an out-of-checkout scope is a confinement finding; `audit:8a09b93:4` root files are kept; `audit:8a09b93:5` directory-with-child rows; `audit:8a09b93:6` path normalization; `audit:8a09b93:7` single-word commands retained with their failure status; `audit:8a09b93:8` plan-check F1 reads the completion cell by header; `audit:8a09b93:9` the edited-file test rejects changed bytes against the original SHA. Plus the lineage rows audit:9da0ed3:10-13 (parser-gap) under the parser-gap re-plan.
- 2026-10-19T04:31:54Z: the chain refuses a second run for an already-audited head, so the sweep was redone by its two steps alone (`pr-feedback.py 417 --json`, the comments dump, `fill_sweep.py … 417-extra.tsv --orchestrator-login moriya-fumio-thd`): 10 items, 0 gaps; thread 4306960626 now `fixed:eb20d063`, 4306960630 `fixed:b3c6b7ea`, 4306960622 `fixed:538e60bd`. The gate reads this JSON.

## Security review of 8a09b936 (2026-10-19T04:34Z): three P1, one P2; S1 by class; a02 withdrawn, a03 reset

- `.orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-security-8a09b93.md`: `Verdict: incorrect`: (1) P1 task-from-plan.py:114 executes a committed PR HEAD's plan commands with no trusted digest; (2) P1 task-consistency-check.py:89 resolves even `bash` through `<root>/bin` first, so a checkout-controlled interpreter runs under a valid premise hash; (3) P1 task-from-plan.py:228 writes its output through an existing symlink; (4) P2 plan-check.py:86 task-controlled globs enumerate outside --root. C14's same-byte hash, the C10 fix, C6 and yaml.safe_load hold.
- class: `decision-not-bound-to-execution` (the class of P1-14's a03/a04 and of every C-80 review today); three security P1 in one mechanism text written before design 5.14 → S1 at the class level; the C-61 cap is also reached (pre-push review, CI repair). The glue guard refuses the merge (P1 lines).
- decision: a02 withdrawn (`status=withdrawn` to a009 04:3xZ; the branch and PR #417 stay); a03 (reset_of a02) applies 5.14 items 2-4 to the three scripts, folds the three P1 and the P2 as items, and the C11 node-id grammar (so the merged checker accepts the regime's selector form); the twelve audit P2 stay with the owner followup-a01, which is dispatched after a03 merges. The a03 text passes C-80 before dispatch; a009 implements on the same branch.

security:8a09b93:1	decision-not-bound-to-execution
security:8a09b93:2	decision-not-bound-to-execution
security:8a09b93:3	decision-not-bound-to-execution
security:8a09b93:4	glob-filter
- 2026-10-19T04:45:46Z: C-80 review of the a03 text (`dotfiles-T133-task-generator-plan-check-a03-text-security-f6797ab.md`): `Verdict: incorrect`, three P1: (1) C14 authenticates the premise command text, not its file operands (`python -I scripts/probe.py`, `source ./probe.sh` run checkout bytes under a trusted interpreter) → premises become a fixed read-only probe vocabulary the checker interprets, no shell (5.14 item 2 amended); (2) `uv run --no-project … python -I` still discovers `.venv` and uv configuration → `--no-config --python <absolute trusted interpreter> --offline` with a hostile .venv fixture (5.14 item 9 amended); (3) the sandbox claims have no deployment prerequisite (the manifest still has failIfUnavailable false and the Linux gh exclusion) → `after: [dotfiles-T133-worker-write-boundary-a01]` and the pre-P1-15 residual stated. Round 2 of the a03 text follows.
- 2026-10-19T04:5xZ: a03 round-2 text installed (C14 probe vocabulary without a shell; uv --no-config --python <abs>; after: worker-write-boundary-a01); checker OK; its C-80 review started.
- 2026-10-19T05:32:41Z: a03 round-3 text installed (the repository-local git filter check before any status or diff, with the marker regression); checker OK; its third C-80 review started 05:33Z.
- 2026-10-19T05:36Z: C-80 third review of the a03 text (`…-a03-text-security-49a7944.md`): one P1: `git config --local` misses the worktree-scoped config.worktree and includes, so a filter defined there bypasses the check → the check reads the effective configuration (`--show-origin --get-regexp`) with three fixtures; round 4 follows.

**Analyzing git and environment configurations**
**Verifying uv environment behavior**
exec
/bin/zsh -lc "cat .orchestration/validation/dotfiles-T133-task-generator-plan-check-a03-text-security-11c9399.md.last.md .orchestration/validation/dotfiles-T133-task-generator-plan-check-a03-text-security-49a7944.md.last.md; nl -ba .orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md | sed -n '1,175p'" in ~/Workspace/dotfiles
 succeeded in 0ms:
- [P1] high .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a03.md:131 — The prescribed Git flags leave repository-local `filter.<name>.clean` and `.process` commands enabled: the retained clean-plan status check can execute them when refreshing tracked files selected by `.gitattributes`, bypassing trusted executable selection; disable this execution route and require a marker regression. [Git filter semantics](https://git-scm.com/docs/gitattributes#_filter).

📝 まとめ: Reviewed every threat row and cited context; identified one remaining execution-binding gap for orchestrator disposition.

Not checked: future implementation tests or live deployment; no files changed. Checkout-selected Git filter execution remains unmitigated.
Verdict: incorrect- [P1] high [.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a03.md:133](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a03.md:133) — `git config --local --get-regexp '^filter\.'` excludes `config.worktree` and disables includes by default, while subsequent status/diff commands consume those settings; an included or worktree-scoped filter therefore bypasses the check and executes attacker-selected commands, and line 203’s direct-local-config fixture misses this bypass. Require inspection of the effective configuration and regressions for both sources. [Git configuration semantics](https://git-scm.com/docs/git-config), [filter execution](https://git-scm.com/docs/gitattributes#_filter).

📝 まとめ: Reviewed every threat row and the cited acceptance/review context; identified one remaining execution-binding gap for orchestrator disposition.

Not checked: future implementation tests or live deployment; no files changed. Git filter execution remains insufficiently constrained.
Verdict: incorrect     1	---
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
    12	  - home/dot_claude/hooks/executable_orchestrator-only.sh
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
    23	  - tests/unit/test_claude_worker_settings.py
    24	  - tests/unit/test_claude_managed_settings.py
    25	  - .orchestration/dotfiles-T133-worker-write-boundary-a01/**
    26	after: []
    27	threat_table:
    28	  - control: "home/dot_agents/agent-config.yaml (trusted checkout and interpreter bindings, static trusted_paths inventory, distinct worker policy, managed sandbox policy and worker caches)"
    29	    disposition: "residual: the rendered policy reduces accidental and injected damage; tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_policy_is_separate_from_orchestrator_policy checks both platforms without claiming same-UID isolation."
    30	  - control: "home/.chezmoitemplates/claude-settings-managed.json (orchestrator user settings with failIfUnavailable true, onFailure block and hook PATH bindings)"
    31	    disposition: "residual: the user baseline preserves orchestrator functions within the managed sandbox policy; tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_orchestrator_settings_keep_existing_policy checks the specified changes and retained settings."
    32	  - control: "home/.chezmoitemplates/claude-worker-settings.json (static trusted-path and worktree-configuration Edit denies, empty user exclusions, restricted write allowances, native merge denials and minimal delivery hooks)"
    33	    disposition: "residual: dedicated user settings reduce worker access to trusted paths; tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_policy_renders_for_both_platforms checks the baseline and distinguishes it from shared managed exclusions and socket access."
    34	  - control: "home/.chezmoitemplates/claude-managed-settings.json (admin-required sandbox enforcement, fixed rendered control-plane exclusions and Herdr socket allowance)"
    35	    disposition: "residual: operator installation establishes the documented enforcement scope against project and local sandbox relaxation; tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_rendered_policy_requires_admin_sandbox asserts the rendered keys; shared control-plane capabilities and same-UID host access remain residual."
    36	  - control: "home/dot_claude-worker/modify_private_settings.json (deployment of the dedicated worker baseline without importing orchestrator policy)"
    37	    disposition: "residual: replacing the worker baseline's managed values reduces stale or permissive user configuration; tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_settings_replace_stale_policy_idempotently checks repeated rendering in temporary homes."
    38	  - control: "home/dot_claude/hooks/executable_orchestrator-only.sh (anchored launch-root guard for tracked and main-checkout local project hooks)"
    39	    disposition: "residual: the guard reduces execution of worker-influenced project code and orchestrator hooks in worker sessions; tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_project_guard_uses_launch_root_and_never_runs_worker_payloads checks fixed arguments, canonical identity and child status."
    40	  - control: "formatter and project-map reload configuration-selection boundary (the edited file path in the hook tool input and its owning repository)"
    41	    disposition: "residual: the guard skips these commands for input outside CLAUDE_PROJECT_DIR or in a worker repository under .claude/worktrees/, preventing consumption of worker-controlled Prettier JavaScript configuration and ruff settings; tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_project_guard_uses_launch_root_and_never_runs_worker_payloads checks both the skip and normal anchored-file execution."
    42	  - control: ".claude/settings.json (every tracked project command routed through the installed guard with pinned PATH bindings, absolute interpreters and onFailure block)"
    43	    disposition: "residual: guarded commands reduce worker-triggered project-hook execution; tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_every_tracked_project_hook_is_guarded_and_blocks_on_failure exhaustively traverses the hook entries."
    44	  - control: "scripts/generate-agent-configs.py (separate user and managed settings generation, static manifest deny inventory and absolute executable bindings)"
    45	    disposition: "residual: rendering an explicit manifest list removes Git object traversal from inventory construction; tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_deny_inventory_is_static_and_matches_manifest checks exact manifest correspondence and filesystem coverage."
    46	  - control: "Makefile (the install-managed-settings target that renders a home-directory staging file and prints the operator's sudo install command)"
    47	    disposition: "residual: staging makes the administrative installation concrete without granting the worker administrative authority; tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_install_target_stages_and_prints_without_running_sudo checks the destination, rendered content, quoting and absence of privileged execution."
    48	  - control: "home/dot_local/bin/common/executable_herdr-agents (worker pane environment, dedicated Claude configuration, private caches, worker user hooks and guarded main-checkout local hooks)"
    49	    disposition: "residual: launch preparation reduces accidental inheritance of orchestrator settings and stale hooks; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_every_worker_launch_receives_dedicated_policy_and_private_caches captures managed and standalone launches and repeated starts."
    50	  - control: "home/dot_local/bin/common/executable_herdr-agent-state.sh (repository-owned Herdr state helper with an explicitly supplied absolute Python interpreter)"
    51	    disposition: "residual: binding the helper and its Python child reduces shim execution; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_hook_descendants_do_not_execute_path_interpreters checks executed identities with planted shims."
    52	  - control: "home/dot_agents/skills/agmsg-orchestration/SKILL.md (the governing Worker Playbook step 4 sentence)"
    53	    disposition: "residual: the sentence removes procedural authorization for worker sandbox escapes; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_playbook_requires_every_command_inside_sandbox checks its replacement; shared managed control-plane capabilities remain available and are not represented as per-seat isolation."
    54	  - control: ".gitignore (the .uv-cache directory pattern)"
    55	    disposition: "residual: ignoring the private cache reduces accidental cache publication; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_uv_cache_directory_is_gitignored checks the pattern in a temporary checkout."
    56	  - control: "tests/unit/test_generate_agent_configs.py (separate platform policies, static inventory, interpreter bindings and tracked hook coverage)"
    57	    disposition: "residual: render fixtures verify configuration and command construction; they do not establish live enforcement or authenticate host-local inputs."
    58	  - control: "tests/unit/test_claude_settings_merge.py (orchestrator baseline preservation and failure-policy rendering through the existing merge)"
    59	    disposition: "residual: temporary HOME fixtures verify baseline entries and identify runtime-added hooks separately; they do not install administrative settings."
    60	  - control: "tests/unit/test_herdr_agents.py (every launch route, repeated starts, main-local and worker-user hook placement, descendants, caches and retained native denials)"
    61	    disposition: "residual: fake launchers and subprocess markers verify effective arguments and executed fixture identities without starting live seats; shared managed exceptions remain explicitly outside per-seat exclusion claims."
    62	  - control: "tests/unit/test_claude_worker_settings.py (dedicated settings deployment, static narrow denies, worktree configuration protection, project guard and hook failure configuration)"
    63	    disposition: "residual: fixtures verify configured controls and credential-free deployment behavior; runtime permission checks and the remaining path-consumption window remain deployment and host residuals."
    64	  - control: "tests/unit/test_claude_managed_settings.py (managed policy rendering, conflicting project and local settings fixtures and nonprivileged staging)"
    65	    disposition: "residual: fixtures verify the selected documented enforcement keys and staging behavior without simulating proof of Claude runtime enforcement or performing sudo installation."
    66	  - control: ".orchestration/dotfiles-T133-worker-write-boundary-a01/** (this task's branch artifacts)"
    67	    disposition: "residual: artifacts distinguish documentation facts, historical probes, final-head fixture results and unperformed operator deployment; acceptance compares their claims with the diff and CI."
    68	  - control: "the task-file copy at .orchestration/dotfiles-T133-worker-write-boundary-a01/task.md"
    69	    disposition: "residual: the first push includes the byte-identical dispatched task; TASK and RESULT carry its SHA256, which the orchestrator verifies at acceptance."
    70	  - control: "the evidence records under .orchestration/dotfiles-T133-worker-write-boundary-a01/"
    71	    disposition: "residual: report.md, validation.md, sandbox.md, learning.md, autoskill.md and worker review evidence retain commands, outputs, statuses and tested revisions without credentials or unmasked home-directory paths."
    72	  - control: "task metadata (PR_FEEDBACK_EVIDENCE, AUDIT_EVIDENCE, ACCEPTANCE_EVIDENCE and REVIEW_EVIDENCE)"
    73	    disposition: "residual: the orchestrator checks C1 to C10 and C7b, verifies dispatched bytes and binds integration evidence to the final head; P1-14 a05 and P1-6 implement retrieval of evidence of record from GitHub at its SHA; the GitHub boundary is detection, not prevention."
    74	  - control: metadata separators
    75	    disposition: "residual: the first document separators delimit format-2 metadata; the task-copy SHA256 binds the complete document."
    76	  - control: in-process effects
    77	    disposition: "residual: generation and tests use repository files and temporary fixtures; the worker performs no live deployment, login, administrative installation, permission-policy mutation or operator-session restart."
    78	  - control: workflow and interpreter or environment inputs
    79	    disposition: "residual: absolute interpreters, Python -I, sanitized Git, fixed hook PATH and trusted executable bindings reduce environment injection; the host, native loader and same-UID processes remain outside this task's security guarantee."
    80	  - control: new or renamed scripts
    81	    disposition: "residual: the worker settings modify script, orchestrator-only guard and repository-owned Herdr state helper have named source and installed paths; RESULT inventories their interpreter and descendant bindings without introducing a worker-write-boundary hook or gh wrapper."
    82	  - control: "5.14 item 0: host threat model"
    83	    disposition: "residual: host controls reduce accidental and injected damage without isolating seats sharing one OS user; prevention of worker-initiated merges requires a separate OS user or host under D-024-23's future P1-16, which the operator decides; the GitHub boundary is detection, not prevention, through P1-11's main-push flag for missing acceptance or gate evidence; shared managed control-plane exclusions and the Herdr socket remain residual."
    84	  - control: "5.14 item 1: worker write controls"
    85	    disposition: "residual: dedicated configuration, static symlink-aware Edit denies including worktree configuration and orchestrator worklogs and caches, narrow writable agmsg stores, managed sandbox enforcement and failIfUnavailable true reduce damage; documented path checks do not establish atomic immunity to concurrent path swaps."
    86	  - control: "5.14 item 2: sanitized environment and private executable PATH"
    87	    disposition: "residual: sanitized Git verification and absolute hook entrypoints reduce injected configuration, while PATH=/usr/bin:/bin binds upstream env-bash descendants away from shims; the remaining consuming-helper contracts belong to P1-14 a05, P1-10 a02, audit-pool-a02 and P1-6."
    88	  - control: "5.14 item 3: trusted-path checks"
    89	    disposition: "residual: canonical anchor and interpreter checks reduce worker-selected trusted paths and account for symlink components and filesystem case aliases; other consuming-helper checks remain with their owning hardening tasks."
    90	  - control: "5.14 item 4: verified executable and consumed-byte identity"
    91	    disposition: "residual: hooks execute selected absolute entrypoints and trusted scripts, and upstream shell descendants inherit the fixed system PATH; evidence snapshots, last-use digest checks and their race limitations remain with the consuming orchestrator-side tasks; store-selected driver execution remains the separately named agmsg residual."
    92	  - control: "5.14 item 5: output and reservation identity"
    93	    disposition: "residual: this task adds no reservation protocol; full-head output names, fixed-inode locks and physical-slot identity remain with the orchestrator-side tasks that create them."
    94	  - control: "5.14 item 6: honest residuals, hooks and MCP"
    95	    disposition: "residual: guarded tracked and main-local project hooks and minimal worker user hooks reduce host execution routes; shared managed Herdr socket access, control-plane exclusions, approved external processes and same-UID processes outside every seat sandbox remain residual."
    96	  - control: "5.14 item 7: trusted-execution verification"
    97	    disposition: "residual: this task records red-then-green render, merge, managed-policy, guard, launch, descendant and cache tests; P1-6 owns tests/unit/trusted_exec_contract.py and the consuming-helper contract tests."
    98	  - control: "5.14 item 8: committed approval ledger"
    99	    disposition: "residual: the regime reads the ledger through the GitHub contents API at the SHA returned by git ls-remote origin refs/heads/main; P1-14 a05 implements that read, and local refs, files and object traversal provide no approval authority; the GitHub boundary is detection, not prevention."
   100	  - control: "5.14 item 9: private uv caches"
   101	    disposition: "residual: per-seat worker caches, restricted worker write allowances and explicit denies on the orchestrator worklog and uv-cache reduce cache poisoning; consuming hardening tasks use the protected orchestrator cache with --offline and execute no worker, shared uv or mise cache content."
   102	  - control: "5.14 item 10: no worker command outside the sandbox"
   103	    disposition: "residual: empty worker user exclusions, disabled unsandboxed requests and Codex in-sandbox network reduce escape routes; the worker rule forbids using shared managed control-plane exceptions, whose availability and Herdr socket access remain residual; the deterministic Codex permgate rule and live deployment remain operator steps."
   104	  - control: "hook failure policy"
   105	    disposition: "residual: every generated and tracked hook entry, including launcher-written worker user and main-local entries, carries onFailure block, reducing fail-open behavior where Claude supports it; configuration tests cover missing-command and timeout policy, while background hooks and events on which the field has no effect carry no enforcement responsibility."
   106	  - control: "agmsg store driver and plugin selection (team configuration drivers.partition, db/trusted-plugins authorization and installed storage.sh sourcing)"
   107	    disposition: "residual: every seat writes the store, and installed storage.sh resolves drivers.partition as a driver path and sources it during unsandboxed delivery; it also uses db/trusted-plugins to authorize plugins/partition/shared.sh for sourcing; fixed PATH does not stop these routes; worker denies on plugins/** and db/trusted-plugins reduce the plugin route; dotfiles-T133-agmsg-hardening-a01 owns upstream basename validation, plugin authorization hardening and their adversarial red-then-green tests; this task introduces no store-derived sourcing beyond the installed scripts' current behavior."
   108	  - control: orchestrator effect merge
   109	    disposition: "residual: the worker is forbidden to merge; the orchestrator follows the final-head integration gate, required permission approval and pinned squash-merge procedure, with evidence of record retrieved from GitHub; shared credentials still permit worker-initiated API merges, so the GitHub boundary is detection, not prevention."
   110	  - control: orchestrator effect update-branch
   111	    disposition: "residual: the orchestrator owns branch updates and obtains fresh required CI, feedback, audit and security evidence for the resulting head."
   112	  - control: orchestrator effect forced worker removal
   113	    disposition: "residual: no forced removal is planned; existing dirty-worktree protections remain, and acceptance identifies any operator-authorized discarded state."
   114	premises:
   115	  - claim: >-
   116	      The historical a05 premises carried by the preceding text describe its recorded observations. They do not require this worker to rebuild PR 400, edit the approval ledger or implement P1-14 a05.
   117	    sources:
   118	      - .orchestration/tasks/dotfiles-T133-permission-guard-gate-a05.md
   119	      - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md
   120	  - claim: >-
   121	      D-024-21 establishes the host threat model and dedicated Claude worker configuration. D-024-23 supersedes D-024-22's credential-separation claim because gh Keychain access is shared by seats running as the same macOS user. Prevention requires a separate OS user or host; the current GitHub boundary is detection, not prevention.
   122	    sources:
   123	      - .orchestration/decisions.tsv
   124	      - .orchestration/plans/024-design-quality.md
   125	      - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md
   126	  - claim: >-
   127	      The existing Claude settings modify script merges the orchestrator user baseline into current settings and appends an attachment hook. The dedicated worker renderer does not import that orchestrator settings merge or its attachment behavior. The administrative managed-settings file is a separate deployment destination.
   128	    sources:
   129	      - home/dot_claude/modify_private_settings.json
   130	      - home/.chezmoitemplates/claude-settings-managed.json
   131	    verification: tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_settings_do_not_import_orchestrator_hooks
   132	  - claim: >-
   133	      The current launcher constructs worker profile options separately from the pane environment. The dedicated Claude configuration directory and private cache variables reach the actual worker process on every launch route. This task adds no gh configuration directory or credential-separation mechanism.
   134	    sources:
   135	      - home/dot_local/bin/common/executable_herdr-agents
   136	      - home/dot_agents/agent-config.yaml
   137	    verification: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_every_worker_launch_receives_dedicated_policy_and_private_caches
   138	  - claim: >-
   139	      Linked-worktree Claude sessions load the main checkout's .claude/settings.local.json. The current launcher writes worker-local delivery hooks and merge denials into a different file. Worker delivery moves to the worker configuration directory's user settings, and the launcher's main-checkout local hooks receive the orchestrator-only guard.
   140	    sources:
   141	      - https://code.claude.com/docs/en/settings#where-claude-code-keeps-the-local-file-in-a-git-repository
   142	      - home/dot_local/bin/common/executable_herdr-agents
   143	      - .claude/settings.local.json
   144	    verification: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_linked_worktree_uses_worker_user_hooks_and_guarded_main_local_hooks
   145	  - claim: >-
   146	      Managed sandbox.enabled true, failIfUnavailable true and allowUnsandboxedCommands false establish the documented admin-required enforcement scope. Project and local settings cannot supply sandbox relaxations in that scope. User settings and shared managed exceptions remain distinct from project and local settings.
   147	    sources:
   148	      - https://code.claude.com/docs/en/sandboxing#repository-settings-under-an-admin-required-sandbox
   149	      - .orchestration/plans/024-design-quality.md
   150	      - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md
   151	    verification: tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_managed_render_is_independent_of_conflicting_project_and_local_settings
   152	  - claim: >-
   153	      Installed agmsg storage.sh resolves the writable team configuration's drivers.partition value as a driver path and sources it during delivery. The upstream hardening belongs to dotfiles-T133-agmsg-hardening-a01 and remains a residual of this task.
   154	    sources:
   155	      - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md
   156	      - .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-08e6ac7.md.last.md
   157	---
   158	
   159	# AGMSG-TASK dotfiles-T133-worker-write-boundary-a01 — plan 024 P1-15 under D-024-17, D-024-19, D-024-20, D-024-21 and D-024-23
   160	
   161	## Goal
   162	
   163	The host is not a security boundary between seats sharing one OS user. gh keys Keychain credentials by host and user, so a worker running as the same macOS user can read the orchestrator's token regardless of `GH_CONFIG_DIR`. Prevention of a worker-initiated merge requires a separate OS user or host under D-024-23's future P1-16, which the operator decides whether to pursue. Until then the GitHub boundary is detection, not prevention. The regime rule requires the main-push CI run to flag a merge that lacks the required acceptance record or gate-passage evidence. P1-11 owns implementation of that flag; this task states the rule. Approvals and gate evidence of record are read from GitHub at a SHA through its API inside the sandbox. Host-local controls reduce accidental and injected damage without establishing isolation from a malicious same-UID process.
   164	
   165	This task implements section 5.14 items 1, 9 and 10 through a dedicated Claude worker configuration directory, static Edit deny rules on trusted paths and worktree configuration, managed sandbox enforcement, guarded project hooks, hook interpreter and PATH bindings, private worker caches and the rule that worker commands run inside their sandbox. Every Claude seat has `sandbox.failIfUnavailable: true`. Codex workers have `sandbox_workspace_write.network_access=true`.
   166	
   167	The administrative managed policy is shared by every Claude seat. Its Herdr socket allowance and three control-plane exclusions remain available to workers as well as the orchestrator. Empty arrays in worker user settings do not subtract these managed entries. Their availability is a residual under item 0, and the worker execution rule supplies no authorization to use them outside the sandbox.
   168	
   169	[memory:decision] D-024-20 makes this task the dispatch prerequisite of P1-14 a05, P1-10 a02, audit-pool-a02 and P1-6. The orchestrator places this task in their `after:` fields before dispatch. This task has `after: []`. A Codex seat performs these Claude configuration edits under the routing rule, including the Worker Playbook step 4 sentence permitted by plan 021 step 8.3.
   170	
   171	The design source is `.orchestration/plans/024-design-quality.md` section 5.14 items 0 through 10. D-024-21, D-024-23 and the amended items 0, 1 and 8 govern this revision. D-024-22's proposed gh credential separation is superseded. The acceptance record preserves documentation facts and earlier proposals as history.
   172	
   173	The third C-80 text review is `.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-ecc7ab5.md.last.md`. Its five P1 findings remain recorded. The retained mechanisms are documented symlink-aware deny rules, approval reads outside the local object database, hook interpreter bindings and runtime hook failure policy.
   174	
   175	The fourth C-80 text review is `.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-8d42532.md.last.md`. Its six P1 findings remain recorded. The retained mechanisms are the static manifest deny inventory, protection of the orchestrator worklog and cache, narrow home denies around writable agmsg stores, correct linked-worktree hook placement and fixed hook-runtime PATH.

exec
/bin/zsh -lc '/usr/bin/env -i PATH=/usr/bin:/bin GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null /usr/bin/git -c core.hooksPath=/dev/null -c core.fsmonitor=false -c protocol.allow=never -c protocol.https.allow=always -C ~/Workspace/dotfiles show 8a09b9365932f23b09df8aa2385a93d0b3016a3e:scripts/orchestrator/plan-check.py' in ~/Workspace/dotfiles
 succeeded in 16ms:
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-UZdymvgj' (errno=Operation not permitted)
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-jGyK3xq8' (errno=Operation not permitted)
"""Form, drift and invariant checks over the plan 024 group (plan 024 programs (15)), one violation per line.

`uv run --no-project --with pyyaml python -I scripts/orchestrator/plan-check.py [--root <repo>] [--drift] [--invariants]`
reads the eleven `.orchestration/plans/024-*` files under --root (default: the current git toplevel), prints every
violation on its own line and exits 1 when there is one, 0 otherwise. It writes nothing.
F1 every 024-todo.md table row has a non-empty completion (last) column.
F2 the tasks one wave row of the plan's section 6 names have pairwise-disjoint allowed_files once their task files
   exist (a task file belongs to the todo id its `# ` title line names): each glob entry stands for the tree files it
   matches, a literal entry for itself, and two lists overlap where a path is in both or inside the other's directory,
   or where a literal matches the other's glob; the finding names the first shared path. Glob spellings are never
   compared with each other.
F3 every P1-<n> row names a bottleneck id: a B<n> row of 024-design-mechanism.md or an M<n> row of 024-design-quality.md.
F4 every DoD row of 024-checklists.md holds a backtick command or a file path.
F5 every decision row of the plan's section 2 has a bold default.
F6 every cited dotfiles-T<n>-... id is a task file, every D-... id a row of .orchestration/decisions.tsv, and with
   --drift every #<pr> a pull request.
--drift: every head sha or state word (CLEAN, BEHIND, draft, merged, closed) that starts within 40 characters after a
   #<pr> on its line, before the next #, each compared on its own against `gh pr view`; and every 024-progress.tsv row
   naming a task against the status of that task's latest AGMSG-ACCEPTANCE event (task_id=<task>, each event read up
   to the next one on its line) in its acceptance record, latest by the last timestamp before the event on its line (an
   untimed event carries the latest timestamp above it), then by position: `drift: <file>:<line> <cited> != <live>`.
--invariants: ANTHROPIC_OAUTH_TOKEN= with a value (bare, single- or double-quoted; an empty "" or '' is none),
   `git push origin main`, `gh pr merge` with --admin or --auto in the
   plan files, and a claude.permissions.ask entry home/dot_agents/agent-config.yaml adds against origin/main.
"""

import argparse
import glob
import json
import pathlib
import re
import subprocess
import sys
from fnmatch import fnmatchcase

try:
    import yaml
except ImportError:
    print("needs pyyaml: run with uv run --no-project --with pyyaml")
    sys.exit(2)

PLANS = ".orchestration/plans"
TASK_ID = r"\bdotfiles-T\d+(?:-[a-z0-9]+)+"
DECISION_ID = r"\bD-(?!W\d)[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*"
GLOB = re.compile(r"[*?[]")
STATES = {"CLEAN": ("mergeStateStatus", "CLEAN"), "BEHIND": ("mergeStateStatus", "BEHIND"), "draft": ("isDraft", True)}
STATES |= {"merged": ("state", "MERGED"), "closed": ("state", "CLOSED")}
FORBIDDEN = {
    "ANTHROPIC_OAUTH_TOKEN with a value": r"ANTHROPIC_OAUTH_TOKEN=(?:\"[^\"\n]+\"|'[^'\n]+'|[^\s`'\")<])",
    "git push origin main": r"git push origin main\b",
    "gh pr merge --admin or --auto": r"gh pr merge\b[^\n]*?--(?:admin|auto)\b",
}


def run(root, *args):
    return subprocess.run(args, cwd=root, capture_output=True, text=True, check=False)


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def table_rows(lines):
    """(line number, cells) of every table data row: not a header (the row above a separator) nor a separator."""
    rows = []
    for i, line in enumerate(lines):
        nxt = lines[i + 1] if i + 1 < len(lines) else ""
        if line.startswith("|") and not re.match(r"\|\s*-{3}", line) and not re.match(r"\|\s*-{3}", nxt):
            rows.append((i + 1, cells(line)))
    return rows


def section(lines, number):
    start = next((i for i, l in enumerate(lines) if l.startswith(f"## {number}.")), None)
    if start is None:
        return []
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    return [""] * (start + 1) + lines[start + 1 : end]  # keeps the file's line numbers


def scope(root, entries):
    """(paths, globs) of an allowed_files list: its literals and the tree files each glob matches, and its globs."""
    globs = {e for e in entries if GLOB.search(e)}
    paths = {e.rstrip("/") for e in entries if e not in globs}
    for g in globs:
        paths |= {p for p in glob.glob(g, root_dir=root, recursive=True, include_hidden=True) if (root / p).is_file()}
    return paths, globs


def shared(a, b):
    (pa, ga), (pb, gb) = a, b
    out = {x for x in pa for y in pb if x == y or x.startswith(y + "/")}
    out |= {y for x in pa for y in pb if y.startswith(x + "/")}
    # A literal not yet in the tree overlaps a glob it matches (fnmatch's * also crosses /, which errs toward a report).
    out |= {x for x in pa for g in gb if fnmatchcase(x, g)} | {y for y in pb for g in ga if fnmatchcase(y, g)}
    return sorted(out)


def latest(text, tid):
    """The status of tid's latest AGMSG-ACCEPTANCE event, or none."""
    events, carried, stamp = [], "", r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2})?"
    for i, line in enumerate(text.splitlines()):
        for m in re.finditer(r"AGMSG-ACCEPTANCE v1 (.*?)(?=AGMSG-ACCEPTANCE v1 |$)", line):  # one event at a time
            status = re.search(r"\bstatus=([\w-]+)", m[1])
            if status and re.search(rf"\btask_id={re.escape(tid)}(?![\w-])", m[1]):
                stamps = re.findall(stamp, line[: m.start()])
                events.append((stamps[-1] if stamps else carried, i, m.start(), status[1]))
        carried = max([carried, *re.findall(stamp, line)])
    return max(events)[3] if events else "none"


def form(root, files):
    out = []
    todo, plan = files["024-todo.md"], files["024-omp-cutover-and-corrective-order.md"]
    for n, c in table_rows(todo):  # F1
        if not c[-1]:
            out.append(f"F1 024-todo.md:{n} {c[0][:20]} has an empty completion column")
    ids = set(re.findall(r"^\| (B\d+) \|", "\n".join(files["024-design-mechanism.md"]), re.M))
    ids |= set(re.findall(r"^\| (M\d+) \|", "\n".join(files["024-design-quality.md"]), re.M))
    for n, c in table_rows(todo):  # F3
        if c[0].startswith("P1-") and not set(re.findall(r"\b[BM]\d+\b", " ".join(c))) & ids:
            out.append(f"F3 024-todo.md:{n} {c[0].split()[0]} names no bottleneck id of 5.0 or 5.10")
    tasks = {}
    for p in sorted((root / ".orchestration/tasks").glob("*.md")):
        title = next((l for l in p.read_text().splitlines() if l.startswith("# ")), "")
        for tid in set(re.findall(r"\bP1-\d+[a-z]?\b", title)):
            allowed = (yaml.safe_load(p.read_text().split("\n---\n", 1)[0].lstrip("-\n")) or {}).get("allowed_files")
            tasks.setdefault(tid, set()).update(allowed or [])
    tasks = {tid: scope(root, entries) for tid, entries in tasks.items()}
    for n, c in table_rows(section(plan, 6)):  # F2
        wave = sorted(set(re.findall(r"\bP1-\d+[a-z]?\b", " ".join(c[1:]))) & set(tasks))
        for i, a in enumerate(wave):
            for b in wave[i + 1 :]:
                if both := shared(tasks[a], tasks[b]):
                    out.append(f"F2 024-omp-cutover-and-corrective-order.md:{n} {c[0]} {a} and {b} share {both[0]}")
    for n, c in table_rows(files["024-checklists.md"]):  # F4
        if not re.search(r"`[^`]+`|[\w.~-]*/[\w./-]+|\b\w+\.(?:md|json|tsv|ya?ml|sh|py)\b", " ".join(c[1:])):
            out.append(f"F4 024-checklists.md:{n} {c[0]} holds no backtick command or file path")
    for n, c in table_rows(section(plan, 2)):  # F5
        if re.match(r"D\d+\b", c[0]) and not re.search(r"\*\*[^*]+\*\*", c[-1]):
            out.append(f"F5 024-omp-cutover-and-corrective-order.md:{n} {c[0].split()[0]} has no bold default")
    decisions = {l.split("\t", 1)[0] for l in (root / ".orchestration/decisions.tsv").read_text().splitlines()[1:]}
    for name, lines in files.items():  # F6
        for n, line in enumerate(lines, 1):
            for tid in dict.fromkeys(re.findall(TASK_ID, line)):
                if not (root / f".orchestration/tasks/{tid}.md").is_file():
                    out.append(f"F6 {name}:{n} cites {tid}, which is not a task file")
            # A family such as D-024-* names no single decision.
            ids = [m.group() for m in re.finditer(DECISION_ID, line) if line[m.end() : m.end() + 2] != "-*"]
            for did in dict.fromkeys(ids):
                if did not in decisions:
                    out.append(f"F6 {name}:{n} cites {did}, which is not a row of decisions.tsv")
    return out


def drift(root, files):
    out, live = [], {}

    def pr(number):
        if number not in live:
            got = run(root, "gh", "pr", "view", number, "--json", "headRefOid,mergeStateStatus,isDraft,state")
            live[number] = json.loads(got.stdout) if got.returncode == 0 else None
        return live[number]

    for name, lines in files.items():
        for n, line in enumerate(lines, 1):
            for number in dict.fromkeys(re.findall(r"#(\d{2,6})\b", line)):
                if pr(number) is None:
                    out.append(f"F6 {name}:{n} cites #{number}, which is not a pull request")
            found = {}
            for m in re.finditer(r"#(\d{2,6})\b([^#\n]*)", line):
                state = pr(m.group(1))
                if state is None:
                    continue
                tokens = re.finditer(r"\b([0-9a-f]{7,40}|CLEAN|BEHIND|draft|merged|closed)\b", m.group(2))
                for cited in dict.fromkeys(t.group() for t in tokens if t.start() <= 40):
                    if cited in STATES:
                        key, want = STATES[cited]
                        if state.get(key) != want:
                            found[f"drift: {name}:{n} #{m.group(1)} {cited} != {state.get(key)}"] = None
                    elif not state.get("headRefOid", "").startswith(cited):
                        found[f"drift: {name}:{n} #{m.group(1)} {cited} != {state.get('headRefOid', '')[:12]}"] = None
            out += found
    for n, line in enumerate(files["024-progress.tsv"][1:], 2):
        tid, *rest = line.split("\t")
        record = root / f".orchestration/acceptance/{tid}.md"
        if not rest or not (root / f".orchestration/tasks/{tid}.md").is_file():
            continue
        live = latest(record.read_text(), tid) if record.is_file() else "none"
        if len(rest) > 2 and rest[2] != live:
            out.append(f"drift: 024-progress.tsv:{n} {tid} {rest[2]} != {live}")
    return out


def invariants(root, files):
    out = []
    for name, lines in files.items():
        for n, line in enumerate(lines, 1):
            out += [f"invariant: {name}:{n} {what}" for what, rx in FORBIDDEN.items() if re.search(rx, line)]
    path = "home/dot_agents/agent-config.yaml"
    base = run(root, "git", "show", f"origin/main:{path}")
    if base.returncode == 0 and (root / path).is_file():

        def asks(text):
            return ((yaml.safe_load(text) or {}).get("claude") or {}).get("permissions", {}).get("ask") or []

        old = asks(base.stdout)
        out += [f"invariant: {path} permissions.ask adds {e}" for e in asks((root / path).read_text()) if e not in old]
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=pathlib.Path, help="the repository (default: the current git toplevel)")
    parser.add_argument(
        "--drift", action="store_true", help="compare cited PR states and progress rows with live state"
    )
    parser.add_argument("--invariants", action="store_true", help="report forbidden patterns and added ask entries")
    args = parser.parse_args()
    root = args.root or pathlib.Path(run(".", "git", "rev-parse", "--show-toplevel").stdout.strip())
    paths = sorted((root / PLANS).glob("024-*.md")) + [root / PLANS / "024-progress.tsv"]
    files = {p.name: p.read_text().splitlines() for p in paths}
    found = form(root, files)
    found += drift(root, files) if args.drift else []
    found += invariants(root, files) if args.invariants else []
    if found:
        print("\n".join(found))
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())

web search: 
web search: https://git-scm.com/docs/git-config
**Analyzing Git status and submodule behavior**
**Reviewing Git remote and security risks**
exec
/bin/zsh -lc "/usr/bin/env -i PATH=/usr/bin:/bin GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null /usr/bin/git -c core.hooksPath=/dev/null -c core.fsmonitor=false -C ~/Workspace/dotfiles show 8a09b9365932f23b09df8aa2385a93d0b3016a3e:scripts/orchestrator/task-from-plan.py | sed -n '1,135p'; sed -n '109,155p' .orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md" in ~/Workspace/dotfiles
 succeeded in 91ms:
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-ppSK9j8j' (errno=Operation not permitted)
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-5eT1Mvtv' (errno=Operation not permitted)
"""A format-2 task file from one plan 024 todo row, every premise and Check command run (plan 024 programs (12)).

`uv run --offline --with pyyaml python -I scripts/orchestrator/task-from-plan.py <todo-id> [--out <task.md>]
[--seat <identity>] [--worktree <path>]` refuses, before it runs or writes anything, while the
.orchestration/plans/024-* group under the current git toplevel has a staged, unstaged or untracked change. Otherwise it
reads, at the committed revision HEAD (named in the task's opening line), the row <todo-id> of
.orchestration/plans/024-todo.md, the items of 024-design-programs.md its work column names by (n) (each through the
next **(<n>) heading or the end of the file), the wave row of the plan's section 6 whose cell (the --seat column's when
given) holds the whole id <todo-id>, and the Q-A row of 024-design-quality.md (security: true when it lists the id or a
range holding it). task-template.md beside this script supplies the control rows, the common Check commands and the
Completion section; no file under .orchestration/tasks/ is read. It writes --out (default
.orchestration/tasks/<todo-id>.md), runs task-consistency-check.py on it with --premises-sha of the written bytes,
prints the checker's output and exits 0 when the checker passes, 1 otherwise (the file stays for editing).
allowed_files: every path or glob scope the row and its items name in backticks (a literal has a file extension or
exists, inside the checkout), every file `git grep -l -F` finds under scripts/ and tests/ for each named script or test
(each listed as `# from: <hit>` in the Files section), and the task's own evidence directory. threat_table: one draft
row per entry (residual: the row's completion), one per executed or applied file a glob entry matches (C12), then the
template's rows with <task_id> replaced.
A backticked span is a command by its form: its first word is a lowercase name, a / or ./ path, or a .sh or .py path,
and it holds no <placeholder>; a lone word is one only when PATH holds it (a lone path is a scope). premises: every
command the items quote but `make`, run once through the checker's rerun (C14's environment, so C14 reproduces the
pasted stdout); a nonzero exit is pasted as `verify:` with its code, and a gh, curl or URL command is not run, as C14
skips it. Check: the template's commands and the items' `make` commands, each run once in a detached scratch worktree of
origin/main with the caller's PATH and pasted with its exit code, the revision and its last 20 output lines; the
worktree is removed with `git worktree remove --force` and its temporary parent deleted.
"""

import argparse
import hashlib
import importlib.util
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

import yaml

PLANS = ".orchestration/plans"
TEMPLATE = pathlib.Path(__file__).with_name("task-template.md")
NETWORK = r"\b(?:gh|curl)\b|https?://"
GLOB = r"[*?\[]"
spec = importlib.util.spec_from_file_location("checker", pathlib.Path(__file__).with_name("task-consistency-check.py"))
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


def git(root, *args):
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=False)


def rows(lines):
    return [
        [c.strip() for c in l.strip().strip("|").split("|")]
        for l in lines
        if l.startswith("|") and not re.match(r"\|\s*-{3}", l)
    ]


def spans(text):
    return re.findall(r"`([^`\n]+)`", text)


def is_command(span):
    words = span.split() or [""]
    if re.search(r"<[^<>\s]+>", span) or not re.fullmatch(
        r"[a-z][\w.+-]*|\.?\.?/[\w./-]+|[\w./-]+\.(?:sh|py)", words[0]
    ):
        return False
    return len(words) > 1 or ("/" not in words[0] and shutil.which(words[0]) is not None)


def program(lines, n):
    start = next(i for i, l in enumerate(lines) if l.startswith(f"**({n}) "))
    end = next((i for i in range(start + 1, len(lines)) if re.match(r"\*\*\(\d+\) ", lines[i])), len(lines))
    return "\n".join(lines[start:end]).strip()


def run_check_commands(root, commands, tid):
    parent = pathlib.Path(tempfile.mkdtemp(prefix=f"{tid}."))
    scratch = parent / "origin-main"
    try:
        if git(root, "worktree", "add", "--detach", str(scratch), "origin/main").returncode:
            return [f"- `{c}`: not run (no origin/main worktree)" for c in commands]
        try:
            rev, out = git(scratch, "rev-parse", "HEAD").stdout.strip(), []
            for c in commands:
                stdout, code, stderr = checker.rerun(c, scratch, os.environ["PATH"])
                tail = ["```", *((stdout or "") + stderr).splitlines()[-20:], "```"]
                out.append(f"- `{c}`: exit {code} on origin/main {rev[:12]}" + "".join(f"\n  {l}" for l in tail))
            return out
        finally:
            git(root, "worktree", "remove", "--force", str(scratch))
    finally:
        shutil.rmtree(parent, ignore_errors=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("todo_id")
    parser.add_argument("--out", type=pathlib.Path)
    parser.add_argument("--seat", help="the wave table column to read (for example a009)")
    parser.add_argument("--worktree", help="the seat's worktree, named in the task's opening line")
    args = parser.parse_args()
    root = pathlib.Path(git(".", "rev-parse", "--show-toplevel").stdout.strip())
    # The plan's commands are the orchestrator's own text, so they run only as committed.
    status = git(root, "status", "--porcelain=v1", "--untracked-files=all", "--", f":(glob){PLANS}/024-*")
    if status.returncode or status.stdout:
        sys.exit(
            f"task-from-plan: refused: the plan group has uncommitted changes; commit them first:\n{status.stdout}"
        )
    rev = git(root, "rev-parse", "HEAD").stdout.strip()

    def read(name):
        shown = git(root, "show", f"{rev}:{PLANS}/{name}")
        if shown.returncode:
            sys.exit(f"task-from-plan: {PLANS}/{name} is not in the commit {rev}")
        return shown.stdout.splitlines()

    out = args.out or pathlib.Path(f".orchestration/tasks/{args.todo_id}.md")
    tid, own = out.stem, f".orchestration/{out.stem}/"
    template = TEMPLATE.read_text().replace("<task_id>", tid)
    bundled = checker.front(template)
    row = next(c for c in rows(read("024-todo.md")) if c[0].split()[0] == args.todo_id)
    title, purpose, work, completion = row[0].split(" ", 1)[-1], row[1], row[2], row[-1]
    items = [program(read("024-design-programs.md"), n) for n in dict.fromkeys(re.findall(r"\((\d+)\)", work))]
    qa = next((c for c in rows(read("024-design-quality.md")) if c[0].startswith("Q-A")), [""])
    listed = " ".join(qa)
    num = re.fullmatch(r"P1-(\d+)", args.todo_id)
    in_range = num and any(int(a) <= int(num[1]) <= int(b) for a, b in re.findall(r"P1-(\d+)〜P1-(\d+)", listed))
    security = bool(re.search(rf"{re.escape(args.todo_id)}(?![\w-])", listed) or in_range)

    names = [s.split()[0] for s in spans(work + "\n" + "\n".join(items)) if s.split()]
    disposition: "residual: the worker is forbidden to merge; the orchestrator follows the final-head integration gate, required permission approval and pinned squash-merge procedure, with evidence of record retrieved from GitHub; shared credentials still permit worker-initiated API merges, so the GitHub boundary is detection, not prevention."
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
      D-024-21 establishes the host threat model and dedicated Claude worker configuration. D-024-23 supersedes D-024-22's credential-separation claim because gh Keychain access is shared by seats running as the same macOS user. Prevention requires a separate OS user or host; the current GitHub boundary is detection, not prevention.
    sources:
      - .orchestration/decisions.tsv
      - .orchestration/plans/024-design-quality.md
      - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md
  - claim: >-
      The existing Claude settings modify script merges the orchestrator user baseline into current settings and appends an attachment hook. The dedicated worker renderer does not import that orchestrator settings merge or its attachment behavior. The administrative managed-settings file is a separate deployment destination.
    sources:
      - home/dot_claude/modify_private_settings.json
      - home/.chezmoitemplates/claude-settings-managed.json
    verification: tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_settings_do_not_import_orchestrator_hooks
  - claim: >-
      The current launcher constructs worker profile options separately from the pane environment. The dedicated Claude configuration directory and private cache variables reach the actual worker process on every launch route. This task adds no gh configuration directory or credential-separation mechanism.
    sources:
      - home/dot_local/bin/common/executable_herdr-agents
      - home/dot_agents/agent-config.yaml
    verification: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_every_worker_launch_receives_dedicated_policy_and_private_caches
  - claim: >-
      Linked-worktree Claude sessions load the main checkout's .claude/settings.local.json. The current launcher writes worker-local delivery hooks and merge denials into a different file. Worker delivery moves to the worker configuration directory's user settings, and the launcher's main-checkout local hooks receive the orchestrator-only guard.
    sources:
      - https://code.claude.com/docs/en/settings#where-claude-code-keeps-the-local-file-in-a-git-repository
      - home/dot_local/bin/common/executable_herdr-agents
      - .claude/settings.local.json
    verification: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_linked_worktree_uses_worker_user_hooks_and_guarded_main_local_hooks
  - claim: >-
      Managed sandbox.enabled true, failIfUnavailable true and allowUnsandboxedCommands false establish the documented admin-required enforcement scope. Project and local settings cannot supply sandbox relaxations in that scope. User settings and shared managed exceptions remain distinct from project and local settings.
    sources:
      - https://code.claude.com/docs/en/sandboxing#repository-settings-under-an-admin-required-sandbox
      - .orchestration/plans/024-design-quality.md
      - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md
    verification: tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_managed_render_is_independent_of_conflicting_project_and_local_settings
  - claim: >-
      Installed agmsg storage.sh resolves the writable team configuration's drivers.partition value as a driver path and sources it during delivery. The upstream hardening belongs to dotfiles-T133-agmsg-hardening-a01 and remains a residual of this task.
    sources:
      - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md

web search: 
web search: 'submodule.recurse' in https://git-scm.com/docs/git-config
**Evaluating security considerations**
**Confirming safe lazy fetch handling**
web search: 
web search: https://git-scm.com/docs/partial-clone
exec
/bin/zsh -lc "sed -n '1,125p' tests/unit/test_regime_ci.py; rg -n -A 45 'def test_regime_ci_checks_only_the_latest_copy_of_a_reset_of_lineage' tests/unit/test_regime_ci.py; sed -n '160,240p' .orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md" in ~/Workspace/dotfiles
 succeeded in 103ms:
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
ROWS = "".join(
    f"  - control: {name}\n    disposition: residual\n"
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
        fake = 'import pathlib\npathlib.Path("head-program-ran").write_text("x")\nprint("{line}")\n'
357:    def test_regime_ci_checks_only_the_latest_copy_of_a_reset_of_lineage(self):
358-        # Amendment 1: a later copy whose reset_of names an earlier one is the lineage's only target; the earlier copy
359-        # warns, and its own .orchestration/ paths are no stray of the later one. Without reset_of, both are targets.
360-        later = "t1-a02"
361-        rows = f"  - control: the predecessor copy .orchestration/{T}/task.md\n    disposition: residual\n"
362-        rows += f"  - control: the task copy .orchestration/{later}/task.md\n    disposition: residual\n"
363-        reset = TASK.replace(T, later).replace("allowed_files:", f"reset_of: [{T}]\nallowed_files:")
364-        reset = reset.replace("threat_table:\n", "threat_table:\n" + rows)
365-        for text, expected, kept in ((reset, 0, True), (reset, 0, False), (TASK.replace(T, later), 1, True)):
366-            with self.subTest(reset_of="reset_of" in text, predecessor_copy_kept=kept):
367-                self.build(evidence=False, base={f".orchestration/tasks/{later}.md": text})
368-                pre = json.dumps({"head": self.head})
369-                token, copy = hashlib.sha256(pre.encode()).hexdigest(), hashlib.sha256(text.encode()).hexdigest()
370-                evidence = {f".orchestration/{later}/precheck.json": pre, f".orchestration/{later}/task.md": text}
371-                evidence[f".orchestration/{later}/result.txt"] = f"AGMSG-RESULT v1 precheck={token} task_copy={copy}\n"
372-                predecessor = {f".orchestration/{T}/task.md": TASK} if kept else {}  # a02: deleted in the first push
373-                self.head_commit(evidence | predecessor | {f".orchestration/{T}/note.md": "x\n"}, "two")
374-                result = self.regime()
375-                self.assertEqual(expected, result.returncode, result.stdout + result.stderr)
376-                if expected == 0:
377-                    warning = (
378-                        f"regime-ci: warning: {T}: predecessor copy .orchestration/{T}/task.md (reset_of of {later})"
379-                    )
380-                    self.assertEqual([warning] * kept + ["regime-ci: ok 1 task(s)"], result.stdout.splitlines())
381-                else:
382-                    self.assertIn(
383-                        f"regime-ci: {T}: allowed-files: .orchestration/{later}/task.md is outside", result.stdout
384-                    )
385-
386-    def test_regime_ci_passes_a_records_only_pr_with_no_target(self):
387-        result = self.build(code={".orchestration/validation/note.md": "a record\n"}, evidence=False)
388-        self.assertEqual(
389-            (0, "regime-ci: no target (records-only)\n"), (result.returncode, result.stdout), result.stderr
390-        )
391-        self.head_commit({"src/tool.sh": "a\n"}, "a code change without a task copy")
392-        result = self.regime()
393-        self.assertEqual(1, result.returncode, result.stdout)
394-        self.assertIn("regime-ci: no target: 1 changed path(s) outside .orchestration/ and no task copy", result.stdout)
395-
396-    def test_regime_ci_warns_without_precheck_and_without_dispatched_text(self):
397-        result = self.build(dispatched=None, precheck_head="absent")
398-        warnings = [
399-            f"regime-ci: warning: {T}: task copy unverifiable (no dispatched text at base)",
400-            SKIPPED,
401-            f"regime-ci: warning: {T}: precheck absent",
402-            "regime-ci: ok 1 task(s)",

## Goal

The host is not a security boundary between seats sharing one OS user. gh keys Keychain credentials by host and user, so a worker running as the same macOS user can read the orchestrator's token regardless of `GH_CONFIG_DIR`. Prevention of a worker-initiated merge requires a separate OS user or host under D-024-23's future P1-16, which the operator decides whether to pursue. Until then the GitHub boundary is detection, not prevention. The regime rule requires the main-push CI run to flag a merge that lacks the required acceptance record or gate-passage evidence. P1-11 owns implementation of that flag; this task states the rule. Approvals and gate evidence of record are read from GitHub at a SHA through its API inside the sandbox. Host-local controls reduce accidental and injected damage without establishing isolation from a malicious same-UID process.

This task implements section 5.14 items 1, 9 and 10 through a dedicated Claude worker configuration directory, static Edit deny rules on trusted paths and worktree configuration, managed sandbox enforcement, guarded project hooks, hook interpreter and PATH bindings, private worker caches and the rule that worker commands run inside their sandbox. Every Claude seat has `sandbox.failIfUnavailable: true`. Codex workers have `sandbox_workspace_write.network_access=true`.

The administrative managed policy is shared by every Claude seat. Its Herdr socket allowance and three control-plane exclusions remain available to workers as well as the orchestrator. Empty arrays in worker user settings do not subtract these managed entries. Their availability is a residual under item 0, and the worker execution rule supplies no authorization to use them outside the sandbox.

[memory:decision] D-024-20 makes this task the dispatch prerequisite of P1-14 a05, P1-10 a02, audit-pool-a02 and P1-6. The orchestrator places this task in their `after:` fields before dispatch. This task has `after: []`. A Codex seat performs these Claude configuration edits under the routing rule, including the Worker Playbook step 4 sentence permitted by plan 021 step 8.3.

The design source is `.orchestration/plans/024-design-quality.md` section 5.14 items 0 through 10. D-024-21, D-024-23 and the amended items 0, 1 and 8 govern this revision. D-024-22's proposed gh credential separation is superseded. The acceptance record preserves documentation facts and earlier proposals as history.

The third C-80 text review is `.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-ecc7ab5.md.last.md`. Its five P1 findings remain recorded. The retained mechanisms are documented symlink-aware deny rules, approval reads outside the local object database, hook interpreter bindings and runtime hook failure policy.

The fourth C-80 text review is `.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-8d42532.md.last.md`. Its six P1 findings remain recorded. The retained mechanisms are the static manifest deny inventory, protection of the orchestrator worklog and cache, narrow home denies around writable agmsg stores, correct linked-worktree hook placement and fixed hook-runtime PATH.

The fifth C-80 text review is `.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-08e6ac7.md.last.md`. Its three P1 findings remain recorded. This revision removes the gh credential-separation mechanism, records the upstream agmsg store-driver residual and moves sandbox enforcement into administrative managed settings.

The file-tool rule is the documented sentence, “Deny rules: apply when either the requested path or the file it resolves to matches.” Edit and Write refuse a requested file that is itself a symlink. Directory symlinks are subject to resolved-target permission checks, and the tools check the resolved location again when opening the approved file. These documented checks reduce redirection risk without establishing an atomic host security boundary against concurrent same-UID changes. [Claude permission reference](https://code.claude.com/docs/en/permissions#symlinks)

The 2026-10-19T03:45:06Z sandbox probe ran `gh api repos/mryfmo/dotfiles --jq .name` and returned `dotfiles`. The recorded sandbox proxy used CONNECT without TLS interception, and gh read the Keychain token. This historical observation confirms neither credential separation nor final-head deployment readiness.

The documentation facts recorded at 03:2xZ establish that Edit denies also affect the Bash sandbox, hooks reload during a session and an unavailable sandbox is fail-open by default. D-024-21's 04:0xZ decision establishes the dedicated Claude configuration mechanism, directory-specific Claude credentials, symlink coverage and `onFailure: "block"` support. These Claude credentials do not separate gh Keychain access.

The settings documentation states, “In a worktree, it uses the file at the main checkout’s root.” Linked-worktree sessions therefore load the main checkout's `.claude/settings.local.json`. Worker hooks belong in `~/.claude-worker/settings.json`, and the main checkout's local hooks also receive the orchestrator-only guard. [Claude local settings reference](https://code.claude.com/docs/en/settings#where-claude-code-keeps-the-local-file-in-a-git-repository)

## Files

1. `home/dot_agents/agent-config.yaml` remains the source of agent policy and model profiles.

   The manifest names `orchestrator_checkout` as the anchored primary checkout and supplies trusted deployment bindings for the guard, hook scripts and absolute interpreters. These bindings resolve outside worker worktrees and executable caches. Worker cwd, tool input, worktree configuration and inherited command variables do not select them. The manifest also supplies the trusted bindings from which the render resolves the absolute directories holding `ruff`, `prettier` and `terminal-browser`, without using mise shims.

   The manifest defines a separate Claude worker settings output at `home/.chezmoitemplates/claude-worker-settings.json` and an administrative managed-settings output at `home/.chezmoitemplates/claude-managed-settings.json`. The worker configuration directory is `~/.claude-worker`. The launcher passes its expanded absolute path as `CLAUDE_CONFIG_DIR`.

   A static `trusted_paths:` list names every protected top-level path of the anchored checkout and the protected home paths. It explicitly includes `<anchored-checkout>/.agents/worklog/**` and `<anchored-checkout>/.agents/worklog/uv-cache/**`. The `.claude` entries protect tracked contents and the main checkout's `.claude/settings.local.json` without denying the whole `.claude/worktrees/` tree. The list explicitly names directory targets and descendant patterns where both are required.

   Separate worker Edit denies protect `//<anchored-checkout>/.claude/worktrees/*/.claude/**` and `//<anchored-checkout>/.claude/worktrees/*/.mcp.json`. The `.claude` directory target is also protected. Ordinary worktree source files and the per-seat cache remain outside these configuration denies.

   The home-path denies are `~/.agents/agent-config.yaml`, `~/.agents/model-profiles.env`, `~/.agents/skills/**/scripts/**`, `~/.agents/skills/**/SKILL.md`, `~/.agents/skills/agmsg/plugins/**`, `~/.agents/skills/agmsg/db/trusted-plugins`, `~/.claude/**`, `~/.claude-worker/**`, `~/.local/bin/**`, `~/.local/share/**`, `~/.local/state/**`, `~/.local/share/mise/**`, `~/.config/**`, `~/.cache/uv/**` and `~/.local/share/uv/**`. No blanket deny on `~/.agents/**` or `~/.local/**` replaces this list.

   The agmsg store paths `~/.agents/skills/agmsg/db`, `~/.agents/skills/agmsg/teams`, `~/.agents/skills/agmsg/run` and `~/.agents/skills/agmsg/ext-tools` remain writable. Deny patterns cover neither these directory targets nor their descendants except the file `~/.agents/skills/agmsg/db/trusted-plugins`. Edit denies merge into the sandbox configuration, so Bash writes to that file and `~/.agents/skills/agmsg/plugins/**` are refused too. Their influence on installed delivery-script driver and plugin selection remains the separately owned agmsg residual.

   The orchestrator retains its existing permissions, cache allowances and hook functions within the administrative managed policy. Its user baseline receives `failIfUnavailable: true`, `onFailure: "block"` on its hooks and the interpreter and PATH bindings below. Its exclusion entries match the three control-plane entries specified below; the former Linux `gh *` exclusion is removed.

   The worker user policy contains no excluded commands and sets `allowUnsandboxedCommands: false`. It contains no Herdr socket allowance and no allow-all Unix socket switch. Its sandbox is enabled and has `failIfUnavailable: true`. Shared managed entries remain effective despite these empty worker arrays.

   Worker `sandbox.filesystem.allowWrite` contains only the existing agmsg store paths and per-seat cache paths. The worktree is the project root and supplies its ordinary project write root. Shared uv and mise write allowances are not copied into worker settings.

   The Codex worker profile sets `sandbox_workspace_write.network_access=true`. Existing model selections and Codex shared Git grants retain their meaning. The deterministic Codex permgate rule that stops approving sandbox escapes is an operator step.

2. `scripts/generate-agent-configs.py` renders the distinct orchestrator user, worker user and administrative managed baselines from the manifest.

   The trusted-path deny inventory is rendered from the static `trusted_paths:` list. Rendering performs no Git object traversal, `git ls-tree` enumeration or tracked-path discovery. Worker-writable refs, replacement refs and objects do not determine the list.

   Anchored checkout rules use absolute `//` permission patterns. Rendering includes the explicitly listed trusted paths themselves and their descendants. It emits no checkout-wide parent deny that defeats ordinary worktree writes. The separate worktree-configuration denies remain present.

   Edit denies cover Write, MultiEdit and NotebookEdit through Claude's permission system. Requested-path and resolved-target matching supply the documented symlink coverage. The generator creates no `executable_worker-write-boundary.py` or replacement PreToolUse path validator.

   Every direct Git verification introduced or changed by this task follows section 5.14 item 2. It begins with `env -i`, uses the selected absolute Git executable and an explicit `-C`, sets `GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL=/dev/null`, and supplies `-c core.hooksPath=/dev/null -c core.fsmonitor=false -c protocol.allow=never -c protocol.https.allow=always`. Diff and show also use `--no-ext-diff --no-textconv` and `-c core.attributesFile=/dev/null -c core.sshCommand=false`.

   The private executable-link directory contains only links to selected absolute trusted binaries. Rendering rejects missing bindings, worker-controlled executable paths, shims, empty PATH entries and relative PATH entries. Python invocations use `-I`. Hook execution uses the role-specific pinned PATH bindings specified below. The render test asserts that `ruff`, `prettier` and `terminal-browser` resolve under the rendered orchestrator tool PATH on the rendering host and that no entry of that PATH is a shims directory.

   `tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_deny_inventory_is_static_and_matches_manifest` asserts that the rendered list equals the manifest entry after trusted anchor and home expansion. It explicitly asserts the rendered home-path deny patterns `~/.local/share/**` and `~/.local/state/**`, including the application code under `~/.local/share` used by `~/.local/bin` wrappers such as `terminal-browser`. It reads the filesystem of the test's own checkout and asserts that every tracked top-level source path is represented. It invokes no Git command to discover those paths.

   The inventory fixtures cover files, directories, `.claude` children, the main-local settings file, ordinary worktree writes, both worktree-configuration patterns, an anchor containing spaces and both explicit worklog patterns. Adding a top-level source path without a manifest entry makes the coverage assertion fail. Planted Git environment and replacement-ref fixtures leave rendering unchanged.

   `tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_denies_leave_agmsg_stores_writable` asserts the rendered deny patterns `~/.agents/skills/agmsg/plugins/**` and `~/.agents/skills/agmsg/db/trusted-plugins` and verifies that the four store directories `db`, `teams`, `run` and `ext-tools` and their descendant fixtures remain writable except that one file.

3. `home/.chezmoitemplates/claude-settings-managed.json` remains the orchestrator user baseline.

   The existing `home/dot_claude/modify_private_settings.json` continues to render the orchestrator's `~/.claude/settings.json`. That modify script is not imported into the dedicated worker renderer and remains outside `allowed_files`.

   This existing template's name does not make it administrative managed settings. The new `claude-managed-settings.json` template supplies that separate scope.

   The orchestrator retains its current user policy content apart from `failIfUnavailable: true`, `onFailure: "block"`, the required interpreter and PATH bindings and alignment of exclusions with the three control-plane entries. Worker-specific Edit denies and restricted worker cache allowances do not enter this baseline. Administrative sandbox requirements apply to the orchestrator as well as workers.

   Every generated hook entry carries `onFailure: "block"`. Every generated command hook starts with `/usr/bin/env -i PATH=<pinned> HOME=<rendered home> LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}"` before its selected absolute interpreter and script path. The formatter and project-map hooks run through the installed orchestrator-only guard and receive the role-specific pinned PATH specified below. Merge evidence identifies hooks appended by the existing modify script and distinguishes them from generated baseline entries. The report accounts for the effective deployed hook set without equating baseline coverage with coverage of runtime-added entries.

   `tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_orchestrator_settings_keep_existing_policy` compares the merged policy with the preceding baseline and accounts for the specified changes. Repeated merging remains idempotent and preserves unrelated settings.


**Assessing git config and test coverage**
web search: 
web search: https://raw.githubusercontent.com/astral-sh/uv/main/crates/uv/src/commands/project/run.rs
**Analyzing submodule security risks**
**Summarizing lazy fetch testing**

I'm wrapping up the lazy fetch behavior tests, noting how missing blobs trigger fetches, and confirming that remote credentials and network tokens don't impact some commands. I need to recommend disabling lazy fetch reads and rejecting submodules to avoid missing data issues. The summary will include final findings, a Japanese summary line, and a clear user verdict, keeping to concise lines as requested.
codex
Git 側に、本文の filter 検査を通らない経路が二つ残っています。親リポジトリの設定検査後に submodule 内の status が別の設定を読む経路と、欠落 object の読み取りが自動 fetch に進む経路です。どちらも、列挙された Git フラグだけでは checkout 側が指定する外部コマンドの実行を止められません。
**Reviewing git submodule test details**
**Confirming API ledger content**
codex
- [P1] high .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a03.md:133 — The filter preflight checks only the parent repository: status can spawn another status inside a selected submodule, whose own configuration can activate `filter.*` commands without that preflight; prohibit submodule traversal or validate each consumed repository, with a nested-filter marker regression. [Git implementation](https://raw.githubusercontent.com/git/git/master/submodule.c)

- [P1] high .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a03.md:131 — The prescribed flags leave lazy fetching enabled: reading a missing object can trigger an HTTPS fetch using checkout-configured `credential.helper` shell commands, bypassing the filter check and trusted executable selection; disable lazy fetching for inspection reads and add a regression. [Lazy fetching](https://git-scm.com/docs/partial-clone#_handling_missing_objects), [credential helpers](https://git-scm.com/docs/git-config#Documentation/git-config.txt-credentialhelper)

📝 まとめ: Reviewed every threat row and cited acceptance/review context; found two remaining execution-binding gaps for orchestrator disposition.

Not checked: future implementation tests or live deployment; no files changed. Checkout-configured execution remains possible through these paths.
Verdict: incorrect
hook: Stop
hook: Stop Completed
tokens used
89,562
- [P1] high .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a03.md:133 — The filter preflight checks only the parent repository: status can spawn another status inside a selected submodule, whose own configuration can activate `filter.*` commands without that preflight; prohibit submodule traversal or validate each consumed repository, with a nested-filter marker regression. [Git implementation](https://raw.githubusercontent.com/git/git/master/submodule.c)

- [P1] high .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a03.md:131 — The prescribed flags leave lazy fetching enabled: reading a missing object can trigger an HTTPS fetch using checkout-configured `credential.helper` shell commands, bypassing the filter check and trusted executable selection; disable lazy fetching for inspection reads and add a regression. [Lazy fetching](https://git-scm.com/docs/partial-clone#_handling_missing_objects), [credential helpers](https://git-scm.com/docs/git-config#Documentation/git-config.txt-credentialhelper)

📝 まとめ: Reviewed every threat row and cited acceptance/review context; found two remaining execution-binding gaps for orchestrator disposition.

Not checked: future implementation tests or live deployment; no files changed. Checkout-configured execution remains possible through these paths.
Verdict: incorrect
