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
session id: 01a15348-1206-7453-aacc-f7f45bc52a08
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
I’ll review the task and its cited evidence as a read-only security design review, using the relevant Ponytail and agmsg-orchestration instructions. I’ll check whether each stated control binds the decision to what actually executes on this host.
exec
/bin/zsh -lc 'cat ~/.agents/skills/agmsg-orchestration/SKILL.md ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail/SKILL.md' in ~/Workspace/dotfiles
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
 succeeded in 16ms:
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
    15	  - control: "scripts/orchestrator/verdict.sh (nine conditions, privileged program startup, fixed executable identities, contained output and explicit security metadata)"
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
    41	  - control: "agmsg storage route (~/.agents/skills/agmsg/scripts/lib/storage.sh)"
    42	    disposition: "out-of-scope: dotfiles-T133-agmsg-hardening-a01 owns worker-writable drivers.partition and plugin sourcing; the orchestrator writes that owner task before dispatch. The compensating control here is no agmsg shell sourcing or counter-script execution: verdict reads only the orchestrator-pasted counters in the acceptance record."
    43	  - control: task metadata
    44	    disposition: "residual: the orchestrator checks format-2 consistency before dispatch and at acceptance, validates security as an explicit boolean, and compares the complete dispatched task with its branch copy."
    45	  - control: metadata separators
    46	    disposition: "residual: the first opening and closing document separators bound safe-loaded YAML; the byte comparison also covers the body and subsequent separators."
    47	  - control: in-process effects
    48	    disposition: "residual: the Python child contains verdict and shadow writes; hold never appends a shadow row, and application still requires accept, four distinct agreeing PRs and a successful integration gate before dispatch or merge."
    49	  - control: workflow and interpreter or environment inputs
    50	    disposition: "residual: program startup, sanitized callers and internally fixed executable paths remove the caller-bin interface; shared-UID access to installations, credentials and host state remains outside the isolation these controls provide."
    51	  - control: new or renamed scripts
    52	    disposition: "residual: verdict.sh remains the only implementation executable introduced by this PR; no pool executable, caller wrapper, dependency or production test-override interface is added."
    53	  - control: orchestrator effect merge
    54	    disposition: "residual: only the orchestrator performs the live head-matched squash merge after the prescribed evidence and integration gate; worker application tests use fixtures."
    55	  - control: orchestrator effect update-branch
    56	    disposition: "residual: an update-branch changes the head and invalidates head-bound evidence; the orchestrator repeats required CI, feedback collection, audit and security review for the resulting head."
    57	  - control: orchestrator effect forced worker removal
    58	    disposition: "residual: no forced removal is planned; any forced removal follows the existing dirty-worktree rule and records discarded uncommitted state."
    59	  - control: "design 5.14 item 1 (worker write boundary)"
    60	    disposition: "residual: the worker does not change its own execution boundary; Claude write isolation is not inferred from render-check, and the orchestrator verifies the deployed boundary separately."
    61	  - control: "design 5.14 item 2 (sanitized environment before execution)"
    62	    disposition: "residual: privileged program startup and env -i callers remove inherited startup functions and selectors before verdict processing; caller integration and shared-UID host execution remain separately assessed."
    63	  - control: "design 5.14 item 3 (trusted path boundaries)"
    64	    disposition: "residual: resolved executable and destination paths are checked against the declared trusted roots; a same-UID process outside a worker sandbox can still mutate host paths."
    65	  - control: "design 5.14 item 4 (execute verified identities and consume verified contents)"
    66	    disposition: "residual: executables run by verified realpath, consumed snapshots are rehashed immediately before use, and decision-input hashes enter the verdict; snapshots do not create a boundary against unrestricted same-UID mutation."
    67	  - control: "design 5.14 item 5 (output and reservation identity)"
    68	    disposition: "residual: verdict and evidence snapshot filenames and shadow rows use the full head; each audit, security, local-review and sweep input is also matched by its full-head metadata, and this verdict task introduces no reservation lock."
    69	  - control: "design 5.14 item 6 (honest residuals)"
    70	    disposition: "residual: startup, path and snapshot controls are reported as damage reduction; neither host isolation nor independent GitHub credentials is claimed."
    71	  - control: "design 5.14 item 7 (verification)"
    72	    disposition: "residual: this task supplies concrete regression selectors and final-head evidence; the shared trusted-execution test helper remains owned by P1-6 and is reused only if available without expanding this task's edit boundary."
    73	  - control: "design 5.14 item 8 (committed approval ledger)"
    74	    disposition: "residual: verdict evaluation supplies no permission approval; PR base, head, changeset and inspected PR bytes come from GitHub at full SHAs, never the main checkout's shared refs or objects; the integration gate remains authoritative and shared credentials remain a residual."
    75	  - control: "design 5.14 item 9 (private cache and absolute interpreter)"
    76	    disposition: "residual: the shared trusted-interpreter resolver and anchored private uv cache exclude worktrees, worker-writable caches and temporary directories; until the P1-3 resolver is available, verdict holds without a private resolver or PATH fallback."
    77	  - control: "design 5.14 item 10 (worker commands remain sandboxed)"
    78	    disposition: "residual: every worker gh command and git write runs individually inside the sandbox; a command that cannot complete there produces a blocked PONG rather than an escape or alternate execution route."
    79	premises: []
    80	---
    81	
    82	# AGMSG-TASK dotfiles-T133-verdict-audit-pool-a04 — INV-6 S1 re-plan of a03 (plan 024 P1-4a; PR #410)
    83	
    84	Worker: a008, Claude Code, worktree `worker-f`.
    85	
    86	This text is the independent redesign by a review-profile context other than the author of the predecessor task texts. The a03 pre-push fix round and revise 1 exhausted its C-61 allowance. The security review of `513e5d05` found caller-controlled executable selection and cached-bytecode execution; the review of `6b7e7833` found inherited `compgen` execution, acceptance of attacker-selected absolute symlink targets, uncontained output writes and an implicit non-security branch.
    87	
    88	The a03 acceptance record contains three `env-trust-bypass` rows: `security:513e5d0:1`, `security:6b7e783:1` and `security:6b7e783:2`. Its recorded `re-plan:` line establishes INV-6 S1. Another a03 patch round is not authorized. This reset changes the execution contract so sanitization precedes the first statement and no caller executable directory exists.
    89	
    90	Read these records before implementation:
    91	
    92	- `.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a03.md`
    93	- `.orchestration/acceptance/dotfiles-T133-verdict-audit-pool-a03.md`
    94	- `.orchestration/validation/dotfiles-T133-verdict-audit-pool-a03-security-513e5d0.md.last.md`
    95	- `.orchestration/validation/dotfiles-T133-verdict-audit-pool-a03-security-6b7e783.md.last.md`
    96	
    97	The design at `$HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md`, section 5.14, applies by reference, including today's amendments to items 2, 8 and 9 and items 4 and 5. This absolute path identifies the orchestrator's uncommitted working copy under C-86. The task does not claim that section is already on `origin/main`.
    98	
    99	The sentences of section 5.14 this task relies on are quoted here verbatim (C-88: the quoted sentences are normative; the path above is context, and the design file is uncommitted at authoring time):
   100	
   101	> 2. **無害化した環境を最初に** 最初の処理として `env -i` に入り、PATH は信頼ルートで解決した絶対バイナリへのリンクだけの私設ディレクトリ（shims、空、相対は拒否）。git は毎回 `GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null -c core.hooksPath=/dev/null -c core.fsmonitor=false -c protocol.allow=never -c protocol.https.allow=always` と明示 `-C`（https だけ許す。`protocol.allow=never` 単独は必要な fetch を止める）。 検査の読み取りは `GIT_NO_LAZY_FETCH=1` で部分クローンの遅延 fetch（checkout 設定の credential.helper を起動しうる）を止め、`-c submodule.recurse=false --ignore-submodules=all` で submodule 内の status/diff（submodule 自身の設定が filter を有効化しうる）を止める。`.gitmodules` を持つ checkout は検査対象として拒否する。 `-C` は作業木を束縛しないので（repo-local の `core.worktree` が読み先を checkout 外へ向けられる）、git は `--git-dir=<checkout>/.git --work-tree=<checkout>` を明示し、`git rev-parse --show-toplevel` の realpath が checkout と一致しないときは拒否する。 premise や検査の「コマンド実行」は、固定語彙の読み取り専用プローブ（`git rev-parse <ref>`、`test -e <path>`、`grep -c <pattern> <file>` のように検査器自身が解釈する形）だけを許し、任意のシェル文字列は実行しない（本文のハッシュはコマンド文を認証するだけで、`python -I scripts/x.py` のファイル被演算子や `source ./x.sh` の中身は認証しない）。diff と show は `--no-ext-diff --no-textconv` と `-c core.attributesFile=/dev/null -c core.sshCommand=false` を付け、PR 側の `.gitattributes`（external diff、textconv、filter）が検査内容や実行物を変えないようにする。Python は `-I`。PATH 探索で実行するものは無い。 A shell script that runs under a PR-controlled or worker-controlled environment (verdict.sh, the chain glue, CI steps) is executed as a program with `#!/bin/bash -p`, never as `bash <file>`: privileged mode discards inherited functions, `BASH_ENV`/`ENV`, `SHELLOPTS`, `BASHOPTS`, `CDPATH` and `GLOBIGNORE` before the first statement, and the first statement re-executes the program under `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 /bin/bash --noprofile --norc -p "$0" "$@"` (long options before `-p`: bash exits 2 otherwise) unless its environment already consists of exactly the allowed names, checked through absolute paths (`/usr/bin/env`, `/usr/bin/grep`) under `-p`; a caller-set sentinel variable is not a sanitization proof, because the caller controls it (a04 C-80 round 1, 2026-10-19); sanitization performed by later statements (unset -f, compgen, PATH edits) is not a boundary, because the statements themselves resolve through the untrusted names (PR #410 security reviews 513e5d0 and 6b7e783, 2026-10-19). No script accepts a caller-supplied executable directory; interpreters are the fixed absolute paths item 9 names.
   102	
   103	> 4. **検証したものを実行し、検証した内容を渡す** 検証した実行体はその realpath で実行する（再探索しない）。検証したファイル内容は信頼ルート配下のスナップショット（0600、一意名）として渡し、使用直前に sha256 を再照合する。判断に読んだ証跡は sha256 を出力に記録する。
   104	
   105	> 5. **出力と予約の同一性** 名前には 40 桁の head を使う（7 桁で衝突させない）。lock は信頼ルート配下の固定 inode に O_EXCL で作り、置換を inode 比較で検出する。物理スロット 1 つに lock 1 つ。
   106	
   107	> 8. **承認はコミット済み台帳から読む** permission の決定行（`scope=permission approved_by=user diff_sha256=…`）は anchored checkout の作業コピーではなく、コミット済みの台帳から読む。読み方は `git ls-remote origin refs/heads/main` が返す commit sha を取り、GitHub API（`gh api repos/<owner>/<repo>/contents/.orchestration/decisions.tsv?ref=<sha>`、sandbox 内）でその sha の内容を取得する。ローカルの `git show` は共有 object database が書けるため中間 tree の差し替えで偽物を返しうる（第 3 回審査の所見 2）（ローカルの ref 名 `origin/main` は経由しない。`refs/replace/` も書けるので replacement を無効にする。Codex worker は `.git/objects` と `.git/refs` に書けるので ref は差し替えられるが、sha で指した object は内容アドレスで偽造できない）。作業コピーの行は提案で、記録 PR が main にマージされて初めて承認になる（PR の承認は操作者の操作）。偽造には main へのマージが要る。 The same applies to the PR content a mechanism evaluates (the verdict, the audit precheck, the counters): the changeset is read from GitHub at the 40-hex head (`gh api repos/{owner}/{repo}/compare/<base40>...<head40>`, `…/contents/<path>?ref=<head40>`) or from a private clone whose object store no worker can write; the main checkout's shared `.git/objects` and its `origin/main` ref are not evidence sources, because Codex workers write them (a04 C-80 round 1, 2026-10-19). Evidence files are named and matched by the full 40-hex head, never by a 7-character prefix.
   108	
   109	> 9. **私設キャッシュ** orchestrator 側の実行は worker と共有するキャッシュ（`~/.cache/uv`、`~/.local/share/uv`、mise）から実行可能物を読まない。`UV_CACHE_DIR` を anchored checkout 配下（`.agents/worklog/uv-cache`、gitignored、worker 書き込み不可）に固定し、`uv run --no-config --no-project --offline --python <信頼ルートの絶対パスのインタプリタ>` で起動する（`--no-config` で uv の設定探索を止め、`--python` の絶対パスで cwd や親の `.venv` の発見を止める；敵対的な `.venv` と `uv.toml` を置いた fixture で検証）。hook は uv を使わず jq と python 標準ライブラリだけで動く。 One trusted interpreter resolver (`scripts/orchestrator/trusted-interpreter.sh`, P1-3 lineage) resolves `<abs>` from the repository's pinned declaration to a regular file under the tool manager's install root, refuses anything else, and every orchestrator-side script consumes it; no script keeps its own `command -v`, `mise which` or PATH fallback (ci-rerun.sh security review 44cb835, 2026-10-19). Shell code of other projects (the agmsg storage layer and its `drivers.partition` sourcing) is never sourced by an orchestrator-side mechanism; counters are read from the agmsg SQLite store read-only with a fixed query or from the pasted record.
   110	
   111	
   112	Host controls reduce accidents and prompt-injected damage. They do not isolate unrestricted processes sharing one UID. The design's GitHub prevention boundary is also not established while worker and orchestrator credentials remain accessible to that same UID; subsequent boundary-record checks provide detection as the design states.
   113	
   114	## Branch and reset boundary
   115	
   116	Continue `tools/verdict-audit-pool-a01`, PR #410, from `6b7e7833a85528440dc397c2555bc9dd603c685a`, already update-branched onto main `3f240b12`. Keep the a03 implementation, regression coverage and evidence. Create neither another implementation branch nor another PR.
   117	
   118	The first push deletes `.orchestration/dotfiles-T133-verdict-audit-pool-a03/task.md` and adds the dispatched text byte-for-byte at `.orchestration/dotfiles-T133-verdict-audit-pool-a04/task.md`. This single predecessor-copy deletion is the explicit reset-bookkeeping exception to `allowed_files`. Other a03 evidence remains unchanged under its original task identifier and tested heads.
   119	
   120	The orchestrator retains the a03 acceptance history, class rows, stopped status and counters. The final inventory identifies preserved a03 evidence separately from a04 additions; preservation does not authorize further worker edits in the a03 directory. The a01/a02 artifact removals already completed by a03 are not repeated or reversed.
   121	
   122	The split remains intact. The pool sibling owns `scripts/orchestrator/audit-pool.sh`, changes to `scripts/orchestrator/orch-audit.sh`, `.schemas/classes.yaml` and `tests/unit/test_audit_pool.py`. `audit-pool.sh` is absent at `6b7e7833`; the audit schema at that head is `.schemas/audit.json`. Neither fact authorizes recreating a split file or adding a `schemas/` mirror. PR #407 remains parked; its parking operation is not repeated.
   123	
   124	## Goal
   125	
   126	Produce one schema-valid verdict from nine positively checked conditions without executing inherited shell startup code, accepting caller-selected executable directories, following output symlinks or treating invalid `security` metadata as an exemption.
   127	
   128	Retain the a03 gate-before-application behavior, complete feedback validation, amended-cap precedence, offline operation, finding counts and trusted-checkout refresh.
   129	
   130	## Files
   131	
   132	1. `scripts/orchestrator/verdict.sh <pr> [--apply] [--loop] [--shadow]` remains Bash with `set -Eeuo pipefail`, English shdoc documentation and `jq` for JSON. Its startup and executable selection follow the Reset design below. Each condition is `{id, ok, evidence}` and becomes true only through a positive check of parsed, validated input.
   133	
   134	   Inputs remain the PR view and checks, the acceptance record's JSON block and prose, the selected task or `--task <id>`, the audit JSON, a fresh feedback sweep, saved feedback dispositions, the task's allowed paths and caps, regime counters, the GitHub merge-base changeset and the head-specific security review. The acceptance block names the PR, task and current head and contains a ledger array. The PR is open, non-draft and based on `main`. Read `head.sha` and `base.sha` from `gh api repos/{owner}/{repo}/pulls/<pr>`, require both to be 40 lowercase hexadecimal characters, and bind all reads to those values. This task chooses GitHub API reads, not a local clone: read the changeset through `…/compare/<base40>...<head40>` and inspected PR bytes through `…/contents/<path>?ref=<head40>`. Repository identity is fixed from the trusted repository declaration, not caller environment or local Git configuration. Missing, incomplete, truncated or unreadable API data holds; no local-head fetch or shared-object fallback is allowed.
   135	
   136	   Condition 1 verifies that the GitHub contents response for `.orchestration/<task>/precheck.json?ref=<head40>` hashes to the record's `precheck:` value and names the head or an ancestor authenticated by GitHub compare data whose diff to the head contains only `.orchestration/<task>/` paths. The retained `PRECHECK_REQUIRED` setting is supplied explicitly as `--precheck-required 0|1`; absent or zero makes this condition's failure a warning. No environment exception is added for it.
   137	
   138	   Condition 2 requires every required check to be present with state `SUCCESS` for the head. Empty or unreadable checks hold. Every duplicate entry for a required name must also be `SUCCESS`.
   139	
   140	   Condition 3 requires an audit that validates against `.schemas/audit.json`, names the task and full head, has zero open P0/P1 findings, and has verdict `correct` or a non-empty set of remaining findings whose scopes are all `records`. A blocked audit holds. An incorrect audit without remaining findings fails this condition.
   141	
   142	   Condition 4 requires saved and fresh feedback documents to name the accepted head, complete feedback identity matching with multiplicity, and a valid disposition for every fresh item. Diagnostic URLs do not determine the result.
   143	
   144	   Condition 5 requires every path in the base-to-head diff to match an `allowed_files` entry and additions-plus-deletions totals to remain within the effective Check caps. The comparison is `gh api repos/{owner}/{repo}/compare/<base40>...<head40>` using the PR API's base and head, and its full `merge_base_commit.sha` identifies the merge base. Consume the complete authenticated file list and its additions/deletions; account for both names of a rename. An unreadable merge base or incomplete changeset holds. The main checkout's `.git`, including `origin/main`, replacement refs and objects, is not an evidence source. Backticked exclusions after `outside` leave the outside count; default exclusions remain `tests/` and `.orchestration/`. Item 7 retains amendment precedence.
   145	
   146	   Condition 6 reads one orchestrator-pasted INV-6 counters block in the acceptance record, bound there to this task, PR and full head. This task chooses the pasted record rather than a live store query so verdict executes no agmsg shell code and cannot follow worker-writable `drivers.partition`. It never invokes `scripts/regime-counters.sh` or sources the agmsg storage layer. No `S1:` line is present and the parsed decimal `revises` value is below 2. A missing ledger or counters block, duplicate block, mismatched binding or unreadable count holds; an absent count is never zero.
   147	
   148	   Condition 7 requires the numeric count of open P0/P1 findings to be zero. Findings with status `new`, `still-open` or absent count as open regardless of identifier or scope.
   149	
   150	   Condition 8 first validates `security` as an explicit boolean. Only boolean `false` permits the non-security branch. Boolean `true` requires the security review's front-matter `head:` to equal the verdict's own full 40-hex head and its last non-blank line to be `Verdict: correct`. A sha7 filename is never a head match. Missing, null or non-boolean metadata holds with the named reason specified below.
   151	
   152	   Condition 9 requires at least one `sha256:<hex> <path>` line in the acceptance record's prose and verifies every such line against its file. Every inspected evidence file, including audit, security, local review and saved or fresh sweep, is named with and matched against the verdict's full 40-hex head: Markdown uses front-matter `head:`, audit and local-review JSON use `head` (on every record for a JSON list), and feedback JSON uses `head_sha`. Missing, invalid or different full-head metadata holds even when a filename or sha7 prefix matches. Hashes preserve consumed bytes; they do not authenticate a local Git object or ref.
   153	
   154	   All nine conditions passing produces `accept`. Failure of condition 6 or 7, missing or unreadable input, schema-invalid input, invalid security metadata or an internal evaluation error produces `hold`. Other failed conditions produce `revise`. The revise line remains `AGMSG-ACCEPTANCE v1 task_id=<task> status=revise previous_head=<head> reason=<failed ids> next_action=<the first failed condition's evidence, shell-safe>`. The orchestrator supplies `check=` selectors.
   155	
   156	   The generated verdict is `.orchestration/validation/<task>-verdict-<head>.json`, using the full 40-character head under design 5.14 item 5. Its fields remain `verdict`, `pr`, `head`, `task_id`, `conditions[]`, `inputs_sha256{}`, `generated_at` and optional `revise_line`, validated against `.schemas/verdict.json`. Audit, security, local-review and sweep inputs use full-head-named verified snapshots with the metadata bindings above. External producers are not edited; the orchestrator supplies the full-head-named evidence and required metadata before evaluation, retaining original artifacts separately. Historical verdict files remain untouched.
   157	
   158	   Exit codes remain 0 for accept, 10 for revise, 20 for hold and 2 for usage or internal error, with internal error treated as hold. A destination or execution-boundary refusal holds with exit 20. Refusal before a usable task or head exists reports hold without inventing an output identity.
   159	
   160	   `--apply` requires the trusted execution context and scripts, schemas and task files whose consumed bytes and complete file inventory equal GitHub's `base40` tree, read through its API at that SHA, with no substituted or extra executable helper in those code directories. Do not use local tracking status, `origin/main` equality or shared objects to authenticate them. Execute verified snapshots as Reset design item 2 requires. The last four shadow rows must agree between machine and human and represent four distinct PRs. Four rows for one PR do not unlock application. Item 6 retains the integration gate before either application effect.
   161	
   162	   After accept and a successful gate, application writes the accepted line to a temporary file, sends it through `scripts/orchestrator/dispatch.sh <team> <from> <to> <pane> <file> <record>`, then invokes `gh pr merge <pr> --squash --match-head-commit <head>`. Its reason names `verdict-<head>`. Team, sender, recipient and placement remain explicit arguments. Arguments containing `--admin` or `--auto` anywhere are refused with exit 2 before input reads or tool calls other than mandatory startup sanitization.
   163	
   164	   `--shadow` writes the verdict JSON and, only for a non-hold verdict, appends `<pr>\t<head>\t<verdict>\t\t\t<generated_at>` to `.orchestration/validation/verdict-shadow.tsv`. Columns remain `pr`, `head`, `machine`, `human`, `agree` and `at`; the orchestrator supplies the human and agreement columns. Shadow mode sends nothing and merges nothing.
   165	
   166	   `--loop` retains PR-number order, eligible open non-draft PRs on `main`, and an acceptance record naming each current head. Each recursive verdict invocation uses the sanitized program-entry contract. The loop rereads GitHub's PR base and head between PRs and, with `--apply`, refreshes the trusted execution files from GitHub at the newly authenticated main/base SHA after each child, verifying their complete inventory and bytes before another child executes. Failed refresh holds with exit 20; a fetch or local fast-forward alone does not satisfy refresh. Neither evaluation nor refreshed execution uses the main checkout's shared refs or objects.
   167	
   168	2. `.schemas/verdict.json` and `.schemas/audit.json` remain JSON Schema 2020-12 documents with `additionalProperties: false` at the top level and in defined item objects.
   169	
   170	   The audit contains `head`, `task_id`, `auditor`, `generated_at`, `verdict` and findings with `id`, `priority`, `confidence`, `file`, `line`, `class`, `scope`, `rationale` and optional `status`. The controlled class enum retains the vocabulary snapshot at `b8998de162afc72d53d07679b8f0a194fcc480ff`.
   171	
   172	   The existing stdlib schema validator remains available through `--validate` under the fixed isolated interpreter, without a new helper file or dependency. Required keys, types, enums, bounds, SHA patterns, additional-property restrictions and RFC 3339 timestamps with offsets remain checked. Date-only values, naive timestamps and invalid calendar dates fail. Runtime validation does not depend on the sibling's `orch-audit.sh --validate`.
   173	
   174	3. The retained interpreter-selection requirement is implemented through Reset design item 2 rather than the a03 caller-bin mechanism.
   175	
   176	   Before PR input processing, the trusted entrypoint fixes absolute executable identities and the offline PyYAML environment. Checkout `.python-version`, `.venv`, executable files, uv configuration, mise configuration and inherited tool-selection variables cannot select an interpreter or tool. Missing trusted installations or unavailable offline dependencies hold before dispatch or merge.
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
   190	   Neither `scripts/require-crit-review.py` nor its validator is edited. Their execution and consumption follow design 5.14 item 4 by reference. Retained red evidence keeps its original head; final-head green results are new evidence.
   191	
   192	5. `tests/unit/test_verdict.py` retains all nineteen tests and their behavior coverage at `6b7e7833`, including schema-rule rejection, offline PyYAML refusal, numeric finding counts, feedback head binding, null diagnostic URLs, identity and multiplicity, disposition validation, gate ordering, amended caps, checkout refresh and cached-bytecode refusal.
   193	
   194	   The a03 test named `test_verdict_ignores_caller_bin_and_path_overrides` retains its coverage of hostile PATH selection while its removed executable-directory fixture is replaced by the fixed-entrypoint fixture. Neither the script nor the test source retains `VERDICT_BIN` or another production executable-directory override.
   195	
   196	   Existing positive and negative controls remain: empty checks, failed duplicate checks, blocked audits, incorrect audits without findings, missing ledgers and records, unavailable GitHub heads, unreadable GitHub merge bases, backticked cap exclusions, absent evidence hashes, PR-code-checkout refusal, four-distinct-PR enforcement and head-matched merge arguments.
   197	
   198	   Fixtures use temporary repositories and fake external tools whose absolute identities are established in the fixture's trusted entrypoint before invocation. They do not reintroduce caller PATH discovery or a production test-only override. The actual Python used for valid execution satisfies the interpreter boundary. All fixture lines count toward the test cap.
   199	
   200	6. The retained application-gate fix remains enforced.
   201	
   202	   After accept and shadow unlock, `--apply` runs the trusted `scripts/orchestrator/orch-gate.sh <task> <head> <pr>` and requires zero exit before dispatch or merge. Missing, refused or nonzero gate execution holds with exit 20, leaves no accepted application result and performs neither effect.
   203	
   204	   `test_verdict_apply_runs_the_integration_gate_before_dispatch_or_merge_and_holds_on_failure` retains failure, refusal, missing-gate and successful-gate controls. The successful order remains gate, dispatch, merge, with the exact task, full head, PR and head-matched merge arguments recorded.
   205	
   206	   Its original red result against `b8998de162afc72d53d07679b8f0a194fcc480ff` remains historical. The current gate wrapper's second positional argument is a PR-worktree path; this task changes no gate interface. Refusal of the specified head form remains hold, with no alternate gate or direct-merge fallback.
   207	
   208	7. The retained cap-parser fix remains enforced.
   209	
   210	   The last applicable cap declaration in text order governs, including its exclusions and outside limit. A later test-only amendment changes the test limit while retaining the outside limit.
   211	
   212	   `test_verdict_condition_5_honors_the_latest_amended_caps` retains the original 500 versus amended 550 case with 531 changed test lines, the actual a02 test-only wording, a later lower limit, changed exclusions and changed outside limit. Unrelated conditions stay green and evidence hashes are refreshed. Its original red head remains historical.
   213	
   214	The required check names remain `validate`, `test (ubuntu-24.04, server)`, `test (ubuntu-24.04, client)`, `test (macos-14, client)`, `public-bootstrap (ubuntu-24.04, server)`, `public-bootstrap (ubuntu-24.04, client)` and `public-bootstrap (macos-14, client)`.
   215	
   216	## Reset design
   217	
   218	1. **Privileged program startup precedes all statements.**
   219	
   220	   `verdict.sh` has mode 0755 and shebang `#!/bin/bash -p`. It is executed as a program. Privileged mode discards inherited functions, `BASH_ENV`/`ENV`, `SHELLOPTS`, `BASHOPTS`, `CDPATH` and `GLOBIGNORE` at startup, before the first statement.
   221	
   222	   The first executable compound statement rejects an invocation lacking privileged mode with the named message `verdict: execute as a program` and exit 20; under privileged mode it checks the environment names through absolute `/usr/bin/env` and `/usr/bin/grep` and re-executes under `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 /bin/bash --noprofile --norc -p "$0" "$@"` unless the environment already consists of exactly `PATH`, `HOME`, `LANG`, `PWD`, `SHLVL` and `_`. Require the fixed PATH and LANG values as well. A caller-set sentinel proves nothing and is not accepted. Long Bash options precede `-p`. This occurs before `set`, traps, function enumeration, argument processing or executable discovery. No `compgen`, `unset -f` loop or PATH edit serves as the startup boundary.
   223	
   224	   Every ordinary caller invokes the executable itself with `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8` as its prefix. The exact environment-name check terminates re-execution; no sentinel is exported or trusted. The retained `PRECHECK_REQUIRED` control is passed as the explicit `--precheck-required 0|1` argument when needed, defaults to 0, and is never inherited or retained as an environment name.
   225	
   226	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_program_discards_hostile_startup_environment` executes the program with exported functions named `compgen`, `[`, `test`, `exec`, `command`, `builtin` and `command_not_found_handle`, a marker-writing `BASH_ENV`, and a planted PATH. It checks that no marker appears and the verdict and condition results equal the clean invocation. The fixture also supplies the other startup selectors discarded by privileged mode. A separate subcase exports `VERDICT_SANITIZED=1` together with `GIT_CONFIG_GLOBAL`, `GIT_DIR` and `GIT_INDEX_FILE` pointing to planted files; it observes the re-exec and the child's allowed-name-only environment, verifies the planted configuration and object/index selectors are not consumed, and requires the same verdict and conditions as the clean invocation. Exercise the exact long-options-before-`-p` command so an exit 2 cannot satisfy the test.
   227	
   228	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_refuses_bash_file_invocation` invokes `bash scripts/orchestrator/verdict.sh …` in a clean fixture and requires exit 20 and the named message. This negative invocation is the sole deliberate non-program verdict call in the tests.
   229	
   230	2. **Executable identities are fixed at the trusted entrypoint.**
   231	
   232	   No caller-supplied executable directory exists. Remove `VERDICT_BIN`, its environment whitelist, symlink-directory acceptance and every equivalent caller override from the script and fixtures. Do not replace them with a differently named environment variable or CLI option.
   233	
   234	   The trusted entrypoint fixes the absolute paths for Bash, uv, Python, gh, git, jq and required utilities before reading PR-controlled input. It executes verified realpaths without rediscovery. The repository's Python declaration is a read-only input; consume `scripts/orchestrator/trusted-interpreter.sh` from the authenticated trusted base when present. The P1-3 resolver alone resolves the pinned declaration to a regular executable file under the tool manager's install root, outside worktrees, worker-writable caches and `$TMPDIR`. A symlink spelling alone authenticates nothing. An absent resolver or invalid trusted installation holds rather than selecting another interpreter from PATH, mise, uv discovery or a checkout. No private resolver, `command -v` or `mise which` fallback is retained here. Implementation may proceed before `dotfiles-T133-ci-efficiency-followup-a04` lands by implementing and testing this unavailable-resolver hold with a trusted resolver fixture for successful cases; live execution stays on hold until that lineage supplies the resolver. This task therefore does not need the resolver at implementation time and adds no P1-3 `after:` dependency.
   235	
   236	   Design 5.14 items 2, 4 and 9 apply by reference to Git invocation, executable paths, verified snapshots and private cache use. The uv invocation is `uv run --no-config --no-project --offline --python <abs>`, with uv itself an internally fixed absolute executable and `<abs>` the validated interpreter realpath. `UV_CACHE_DIR` is the anchored private cache from the design. Worker-shared uv or mise caches supply no executable. Python children use `-I`; the a03 `-B`, `sys.dont_write_bytecode` and refusal of checkout bytecode that helper imports could consume remain enforced.
   237	
   238	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_uses_only_declared_absolute_executables` verifies fixed tool identities with hostile PATH and inherited interpreter selectors, including an absolute symlink to a marker-writing interpreter.
   239	
   240	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_rejects_interpreters_in_worktrees_caches_or_tmp` covers each excluded root, a non-regular target and a valid trusted regular-file control.
   241	
   242	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_executes_verified_snapshots_and_records_input_hashes` changes a validated source or input before consumption and verifies refusal or consumption of the verified snapshot, never the substituted contents, and checks the recorded input hashes.
   243	
   244	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_holds_without_the_shared_trusted_interpreter_resolver` verifies the interim hold and absence of interpreter discovery or application effects.
   245	
   246	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_reads_pasted_counters_without_sourcing_agmsg` plants a marker-writing agmsg driver and counter executable, supplies the valid pasted counters, and requires unchanged verdicts with no marker; missing, duplicate, mismatched and unreadable counter cases hold.
   247	
   248	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_ignores_replaced_local_objects_and_refs` serves forged PR bytes through a replaced local object and forged `origin/main`, while fixed GitHub fixtures return the authentic full-head changeset and contents. It requires the clean verdict and authenticated input hashes, no local-object evidence read, and hold on incomplete API data rather than a local fallback. Cover precheck ancestry, fix-commit membership, application equality and loop refresh through the same GitHub fixtures.
   249	
   250	   The retained `test_verdict_pins_tools_interpreter_and_environment_before_reading_a_pr_checkout` and `test_verdict_never_imports_cached_bytecode` remain green. Unavailable offline PyYAML still holds with no online fallback.
   251	
   252	3. **The Python child contains persistent writes.**
   253	
   254	   Verdict JSON and shadow logging are opened through the fixed isolated Python child inside `<repo>/.orchestration/validation/`. Their resolved paths remain inside the repository and the validation directory. Symlinks, non-regular files and paths outside that boundary refuse before truncation or append. Directory-component validation and descriptor checks prevent a symlinked parent from defeating a leaf-only check.
   255	
   256	   Both opens use `O_NOFOLLOW`; shadow logging also uses `O_APPEND`. Regular-file checks apply to the opened descriptor. Shell `>` and `>>` redirections do not open these destinations. The JSON is schema-valid before it is committed to its destination. A write refusal holds and performs neither dispatch nor merge.
   257	
   258	   On `hold`, the shadow log receives nothing, whether absent or already populated. A contained hold JSON may still be written when task and head are known.
   259	
   260	   New verdict filenames use the full head; every shadow row retains the full head. No reservation or lock mechanism is introduced.
   261	
   262	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_opens_outputs_without_following_symlinks` plants a symlink separately at the JSON destination and shadow-log destination, requires refusal, and verifies each target's bytes remain unchanged. It includes escaping-parent and non-regular destination controls.
   263	
   264	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_shadow_does_not_append_on_hold` checks absent and populated logs and unchanged prior bytes. The existing successful shadow-column test remains green.
   265	
   266	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_output_names_use_the_full_head` checks the full-head JSON filename and shadow identity rather than accepting a seven-character output name.
   267	
   268	4. **Security metadata is an explicit boolean.**
   269	
   270	   Validate the parsed task's `security` value before selecting condition 8's branch. Missing, null or non-boolean values produce condition 8 failure, overall hold with exit 20, and the named reason `security must be an explicit boolean`. They never produce `not a security task`, append a shadow row, dispatch or merge.
   271	
   272	   Only boolean `false` permits the no-security-review branch. Boolean `true` retains the required head-specific review, with front-matter `head:` exactly equal to the verdict's full 40-hex head. A quoted `"false"` is a string and does not exempt the task.
   273	
   274	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_rejects_evidence_for_another_full_head_with_the_same_sha7` uses two distinct 40-hex heads sharing their first seven characters. Separate subcases substitute the audit, security report, local review and saved or fresh sweep; each mismatched or absent full-head field holds despite a matching prefix and a correct security verdict. Full-head-matched controls remain green.
   275	
   276	   Add these separate tests:
   277	
   278	   - `tests/unit/test_verdict.py::VerdictTest::test_verdict_holds_when_security_is_missing`
   279	   - `tests/unit/test_verdict.py::VerdictTest::test_verdict_holds_when_security_is_null`
   280	   - `tests/unit/test_verdict.py::VerdictTest::test_verdict_holds_when_security_is_a_string`
   281	   - `tests/unit/test_verdict.py::VerdictTest::test_verdict_holds_when_security_is_an_integer`
   282	   - `tests/unit/test_verdict.py::VerdictTest::test_verdict_holds_when_security_is_a_float`
   283	   - `tests/unit/test_verdict.py::VerdictTest::test_verdict_holds_when_security_is_a_list`
   284	   - `tests/unit/test_verdict.py::VerdictTest::test_verdict_holds_when_security_is_a_mapping`
   285	
   286	   Each test checks the named reason, hold and absence of application effects. The true and false positive controls remain in the retained condition tests. Unreadable or malformed YAML also holds.
   287	
   288	## Caller inventory and ownership
   289	
   290	At `6b7e7833`, executable verdict callers are the `--loop` child invocation in `scripts/orchestrator/verdict.sh` and the helpers and direct subprocess calls in `tests/unit/test_verdict.py`. Both files are in `allowed_files`. Update every ordinary call to the sanitized program form; the explicit refusal test remains the named exception.
   291	
   292	There is no direct verdict invocation in the PR head's CI workflows and no separate tracked shadow-runner executable. CI exercises the updated test helper. This task's concrete shadow command below is the shadow runner. Do not add an unused wrapper or workflow step.
   293	
   294	The orchestrator owns the follow-up connection in `scripts/orchestrator/chain-integrate.sh` and its local glue `.agents/worklog/orchestrator-glue/integrate-pr.sh`. Before either connects to verdict execution, the orchestrator applies the same sanitized program-entry contract. Those files are not edited by a008. Any later direct CI or shadow caller follows that contract before use.
   295	
   296	## Measured budget
   297	
   298	The read-only command `git diff --numstat 3f240b12 6b7e7833` produced these relevant rows:
   299	
   300	```text
   301	11	0	.schemas/audit.json
   302	10	0	.schemas/verdict.json
   303	278	0	scripts/orchestrator/verdict.sh
   304	399	0	tests/unit/test_verdict.py
   305	```
   306	
   307	The implementation budget is the measured 278 script lines plus Reset design estimates of 60 for startup and callers, 95 for fixed execution and verified consumption, 90 for contained writes, 20 for explicit security metadata, 20 for pasted-counter validation, 70 for GitHub changeset reads and trusted refresh, and 25 for full-head evidence binding, plus the measured 21 schema lines and 51 lines of reserve: `278 + 60 + 95 + 90 + 20 + 20 + 70 + 25 + 21 + 51 = 730`.
   308	
   309	The test budget is the measured 399 lines plus corresponding estimates of 140, 130, 110, 60, 50, 95 and 60, with 41 lines of reserve: `399 + 140 + 130 + 110 + 60 + 50 + 95 + 60 + 41 = 1085`.
   310	
   311	These are cumulative PR ceilings, not targets. Changed lines mean additions plus deletions; fixture changes count. No behavior, validation, assertion or trust-boundary control is removed to meet them.
   312	
   313	## Out of scope
   314	
   315	Pool implementation, the audit wrapper, vocabulary ownership, `dispatch.sh`, record generation, `dispositions.py`, `--second-opinion`, `hold-playbook.sh`, `integrate-seat.sh`, gate and validator changes, task-checker implementation, Makefile targets, CI changes, model configuration, worker permission configuration and live deployment remain outside this task.
   316	
   317	The four findings from the `6b7e7833` security review belong to this reset, including its two P2 findings. They are not assigned to an advisory owner. The a03 no-bytecode fix remains in scope as retained behavior.
   318	
   319	## Check
   320	
   321	Write the new regressions before their implementation changes. Record each new regression's red result against `6b7e7833a85528440dc397c2555bc9dd603c685a` and green result after the fix. A red result must reach its named defect; an unrelated startup or fixture failure is not evidence. Historical a01/a02/a03 red results retain their original references and do not replace new or final-head results.
   322	
   323	The validation file contains commands, verbatim output, exit statuses and tested heads for `make unit-test`, `make render-check`, `make format`, `shellcheck scripts/orchestrator/verdict.sh`, `shfmt -i 4 -sr -d scripts/orchestrator/verdict.sh` and `uv run python -m unittest tests.unit.test_verdict -v`. The script checks are clean and the verdict module is green. Record the executable mode and exact shebang.
   324	
   325	Run every Reset design selector, including all seven invalid-security tests, and retain all nineteen inherited behavior tests. Record the fixed executable realpaths, trusted interpreter and cache location without exposing credentials. Confirm that no executable-directory override remains in script or test source.
   326	
   327	The concrete shadow invocation is `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 scripts/orchestrator/verdict.sh --shadow 410 --task dotfiles-T133-verdict-audit-pool-a04`. Its JSON, exit status, tested head and unchanged shadow-log state on hold appear in `.orchestration/dotfiles-T133-verdict-audit-pool-a04/validation.md`. Hold is expected before required audit and acceptance evidence exists. No live `--apply` is exercised.
   328	
   329	`git diff --numstat --no-renames origin/main...HEAD` shows at most 730 changed lines outside `tests/` and `.orchestration/`, including both JSON schemas, with `verdict.sh` limited to 709 physical lines.
   330	
   331	The cumulative test cap is 1085 under `tests/` over that same complete PR diff.
   332	
   333	Report the implementation total, test total, script length and each schema's line count separately. An inherited check failure is reproduced against the unchanged base with the same command and environment and reported as a failure, never labelled passing or repaired outside scope. Local Bats tests remain unrun; GitHub Actions supplies their required results.
   334	
   335	The orchestrator runs the format-2 task-consistency checker before dispatch and at acceptance, covering C1 to C10, C7b, the required C11 selector grammar and C18's design-by-reference requirement. It records the checker version and actual coverage; a version lacking a check is not evidence that the check passed. Every `closed` row is checked against its single concrete selector, including the class name.
   336	
   337	The orchestrator performs the C-80 security-profile review of this task text and threat table before dispatch. Findings enter the class table and receive dispositions before a send. The orchestrator also performs the complete task-copy byte comparison and SHA256 check; these are not worker self-attestations.
   338	
   339	The final inventory confirms the split remains intact, identifies preserved a03 evidence, shows the a03 task-copy deletion and a04 replacement, and accounts for every new or modified path against the declared boundary.
   340	
   341	## Completion
   342	
   343	One branch, `tools/verdict-audit-pool-a01`, continues PR #410 from the named a03 head. The first push contains the C3 task-copy replacement. The implementation, tests and historical evidence remain; no new implementation PR, branch or repeated parking operation is created.
   344	
   345	The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies with this task's branch, reset boundary and live rules taking precedence, `dotfiles-T133-verdict-audit-pool-a05` as the advisory P2 owner, `task_copy=<sha256 of .orchestration/dotfiles-T133-verdict-audit-pool-a04/task.md>` and `parked_pr=407` in the RESULT. The orchestrator writes the advisory owner task before assigning an advisory disposition and records owned findings under its matching acceptance-record section.
   346	
   347	There is one worker-side pre-push review round at most. Every worker fix round before or after the first RESULT counts toward INV-6 under C-61, including Bot-driven fixes. A pre-push fix followed by revise 1 exhausts the two-round allowance. Predecessor counters and stopped histories remain recorded; a reset does not erase them. A third finding of one class stops further rounds until the orchestrator records the required re-plan.
   348	
   349	A P0/P1 surviving the allowed fix round is sent as `open:<id>` in the RESULT, including review-body and local/security finding identifiers. It stops the PR for the operator's decision. It is neither silently deferred nor converted to not-applicable to permit another worker round or merge. The worker resolves no review thread.
   350	
   351	The report and RESULT identify head, base, branch, changed files, every feedback disposition, retained and added test names, code and test totals, schema counts, script length, task-copy hash, review-round counts and evidence paths. They distinguish historical evidence from final-head validation. Record actual Bot review events rather than inventing a re-review count.
   352	
   353	Expected worker artifacts are `.orchestration/dotfiles-T133-verdict-audit-pool-a04/report.md`, `validation.md`, `sandbox.md`, `learning.md` and `autoskill.md`; revision instructions and selectors are also recorded in `revise.yaml`. Worker review evidence uses the required `-worker-` infix. Artifacts are written at those relative paths in `worker-f`; the RESULT states their placement, and the orchestrator copies required evidence by absolute path. Plan, todo and learn worklogs remain uncommitted.
   354	
   355	This task is `security: true`. The orchestrator performs its final-head task-level audit and separate security-profile review before the integration gate. Final-head CI, the complete feedback sweep, dispositions, audit, acceptance record, gate and merge follow Orchestrator Playbook step 10 in its prescribed order. Changed heads receive fresh required evidence. Only the orchestrator performs `gh pr merge --squash --match-head-commit <audited head>` after the gate. Four-distinct-PR enforcement stays in code; PR #410 is integrated manually.
   356	
   357	No `@codex review` comment is posted. Observe automatic review for the bounded window, read both review bodies and inline findings, and record absence after 15 minutes as `bot: none`. Wait for the required CI checks to pass before a ready-for-review RESULT. Any new push requires checking its CI again.
   358	
   359	Every worker `gh` command, Git write, push and fetch is an individual command inside the sandbox, without shell chaining or a wrapper combining commands. No excluded command, unsandboxed retry, API substitution or browser path bypasses a live boundary. Anything that cannot complete there produces `AGMSG-PONG v1 task_id=dotfiles-T133-verdict-audit-pool-a04 status=blocked` naming the exact command, exit status, output and boundary; preserve the available artifacts and wait for the orchestrator to re-task.
   360	
   361	Until plan 024 P1-14 lands, strings containing `gh pr merge` or `gh pr create` are written through the file-edit tool, not shell commands, heredocs or shell wrappers. This writing rule grants no execution authority.
   362	
   363	Live dispatch, merge and local Bats are not exercised. A gate rejecting the head argument keeps application on hold; the shared-UID residual remains as stated in the design.
   364	
   365	## Checks (pasted by the orchestrator before each send)
   366	
   367	```
   368	(pasted at dispatch)
   369	```
exec
/bin/zsh -lc "sed -n '1,190p' .orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md" in ~/Workspace/dotfiles
 succeeded in 0ms:
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
  - control: "scripts/orchestrator/verdict.sh (nine conditions, privileged program startup, fixed executable identities, contained output and explicit security metadata)"
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
  - control: "agmsg storage route (~/.agents/skills/agmsg/scripts/lib/storage.sh)"
    disposition: "out-of-scope: dotfiles-T133-agmsg-hardening-a01 owns worker-writable drivers.partition and plugin sourcing; the orchestrator writes that owner task before dispatch. The compensating control here is no agmsg shell sourcing or counter-script execution: verdict reads only the orchestrator-pasted counters in the acceptance record."
  - control: task metadata
    disposition: "residual: the orchestrator checks format-2 consistency before dispatch and at acceptance, validates security as an explicit boolean, and compares the complete dispatched task with its branch copy."
  - control: metadata separators
    disposition: "residual: the first opening and closing document separators bound safe-loaded YAML; the byte comparison also covers the body and subsequent separators."
  - control: in-process effects
    disposition: "residual: the Python child contains verdict and shadow writes; hold never appends a shadow row, and application still requires accept, four distinct agreeing PRs and a successful integration gate before dispatch or merge."
  - control: workflow and interpreter or environment inputs
    disposition: "residual: program startup, sanitized callers and internally fixed executable paths remove the caller-bin interface; shared-UID access to installations, credentials and host state remains outside the isolation these controls provide."
  - control: new or renamed scripts
    disposition: "residual: verdict.sh remains the only implementation executable introduced by this PR; no pool executable, caller wrapper, dependency or production test-override interface is added."
  - control: orchestrator effect merge
    disposition: "residual: only the orchestrator performs the live head-matched squash merge after the prescribed evidence and integration gate; worker application tests use fixtures."
  - control: orchestrator effect update-branch
    disposition: "residual: an update-branch changes the head and invalidates head-bound evidence; the orchestrator repeats required CI, feedback collection, audit and security review for the resulting head."
  - control: orchestrator effect forced worker removal
    disposition: "residual: no forced removal is planned; any forced removal follows the existing dirty-worktree rule and records discarded uncommitted state."
  - control: "design 5.14 item 1 (worker write boundary)"
    disposition: "residual: the worker does not change its own execution boundary; Claude write isolation is not inferred from render-check, and the orchestrator verifies the deployed boundary separately."
  - control: "design 5.14 item 2 (sanitized environment before execution)"
    disposition: "residual: privileged program startup and env -i callers remove inherited startup functions and selectors before verdict processing; caller integration and shared-UID host execution remain separately assessed."
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
    disposition: "residual: verdict evaluation supplies no permission approval; PR base, head, changeset and inspected PR bytes come from GitHub at full SHAs, never the main checkout's shared refs or objects; the integration gate remains authoritative and shared credentials remain a residual."
  - control: "design 5.14 item 9 (private cache and absolute interpreter)"
    disposition: "residual: the shared trusted-interpreter resolver and anchored private uv cache exclude worktrees, worker-writable caches and temporary directories; until the P1-3 resolver is available, verdict holds without a private resolver or PATH fallback."
  - control: "design 5.14 item 10 (worker commands remain sandboxed)"
    disposition: "residual: every worker gh command and git write runs individually inside the sandbox; a command that cannot complete there produces a blocked PONG rather than an escape or alternate execution route."
premises: []
---

# AGMSG-TASK dotfiles-T133-verdict-audit-pool-a04 — INV-6 S1 re-plan of a03 (plan 024 P1-4a; PR #410)

Worker: a008, Claude Code, worktree `worker-f`.

This text is the independent redesign by a review-profile context other than the author of the predecessor task texts. The a03 pre-push fix round and revise 1 exhausted its C-61 allowance. The security review of `513e5d05` found caller-controlled executable selection and cached-bytecode execution; the review of `6b7e7833` found inherited `compgen` execution, acceptance of attacker-selected absolute symlink targets, uncontained output writes and an implicit non-security branch.

The a03 acceptance record contains three `env-trust-bypass` rows: `security:513e5d0:1`, `security:6b7e783:1` and `security:6b7e783:2`. Its recorded `re-plan:` line establishes INV-6 S1. Another a03 patch round is not authorized. This reset changes the execution contract so sanitization precedes the first statement and no caller executable directory exists.

Read these records before implementation:

- `.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a03.md`
- `.orchestration/acceptance/dotfiles-T133-verdict-audit-pool-a03.md`
- `.orchestration/validation/dotfiles-T133-verdict-audit-pool-a03-security-513e5d0.md.last.md`
- `.orchestration/validation/dotfiles-T133-verdict-audit-pool-a03-security-6b7e783.md.last.md`

The design at `$HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md`, section 5.14, applies by reference, including today's amendments to items 2, 8 and 9 and items 4 and 5. This absolute path identifies the orchestrator's uncommitted working copy under C-86. The task does not claim that section is already on `origin/main`.

The sentences of section 5.14 this task relies on are quoted here verbatim (C-88: the quoted sentences are normative; the path above is context, and the design file is uncommitted at authoring time):

> 2. **無害化した環境を最初に** 最初の処理として `env -i` に入り、PATH は信頼ルートで解決した絶対バイナリへのリンクだけの私設ディレクトリ（shims、空、相対は拒否）。git は毎回 `GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null -c core.hooksPath=/dev/null -c core.fsmonitor=false -c protocol.allow=never -c protocol.https.allow=always` と明示 `-C`（https だけ許す。`protocol.allow=never` 単独は必要な fetch を止める）。 検査の読み取りは `GIT_NO_LAZY_FETCH=1` で部分クローンの遅延 fetch（checkout 設定の credential.helper を起動しうる）を止め、`-c submodule.recurse=false --ignore-submodules=all` で submodule 内の status/diff（submodule 自身の設定が filter を有効化しうる）を止める。`.gitmodules` を持つ checkout は検査対象として拒否する。 `-C` は作業木を束縛しないので（repo-local の `core.worktree` が読み先を checkout 外へ向けられる）、git は `--git-dir=<checkout>/.git --work-tree=<checkout>` を明示し、`git rev-parse --show-toplevel` の realpath が checkout と一致しないときは拒否する。 premise や検査の「コマンド実行」は、固定語彙の読み取り専用プローブ（`git rev-parse <ref>`、`test -e <path>`、`grep -c <pattern> <file>` のように検査器自身が解釈する形）だけを許し、任意のシェル文字列は実行しない（本文のハッシュはコマンド文を認証するだけで、`python -I scripts/x.py` のファイル被演算子や `source ./x.sh` の中身は認証しない）。diff と show は `--no-ext-diff --no-textconv` と `-c core.attributesFile=/dev/null -c core.sshCommand=false` を付け、PR 側の `.gitattributes`（external diff、textconv、filter）が検査内容や実行物を変えないようにする。Python は `-I`。PATH 探索で実行するものは無い。 A shell script that runs under a PR-controlled or worker-controlled environment (verdict.sh, the chain glue, CI steps) is executed as a program with `#!/bin/bash -p`, never as `bash <file>`: privileged mode discards inherited functions, `BASH_ENV`/`ENV`, `SHELLOPTS`, `BASHOPTS`, `CDPATH` and `GLOBIGNORE` before the first statement, and the first statement re-executes the program under `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 /bin/bash --noprofile --norc -p "$0" "$@"` (long options before `-p`: bash exits 2 otherwise) unless its environment already consists of exactly the allowed names, checked through absolute paths (`/usr/bin/env`, `/usr/bin/grep`) under `-p`; a caller-set sentinel variable is not a sanitization proof, because the caller controls it (a04 C-80 round 1, 2026-10-19); sanitization performed by later statements (unset -f, compgen, PATH edits) is not a boundary, because the statements themselves resolve through the untrusted names (PR #410 security reviews 513e5d0 and 6b7e783, 2026-10-19). No script accepts a caller-supplied executable directory; interpreters are the fixed absolute paths item 9 names.

> 4. **検証したものを実行し、検証した内容を渡す** 検証した実行体はその realpath で実行する（再探索しない）。検証したファイル内容は信頼ルート配下のスナップショット（0600、一意名）として渡し、使用直前に sha256 を再照合する。判断に読んだ証跡は sha256 を出力に記録する。

> 5. **出力と予約の同一性** 名前には 40 桁の head を使う（7 桁で衝突させない）。lock は信頼ルート配下の固定 inode に O_EXCL で作り、置換を inode 比較で検出する。物理スロット 1 つに lock 1 つ。

> 8. **承認はコミット済み台帳から読む** permission の決定行（`scope=permission approved_by=user diff_sha256=…`）は anchored checkout の作業コピーではなく、コミット済みの台帳から読む。読み方は `git ls-remote origin refs/heads/main` が返す commit sha を取り、GitHub API（`gh api repos/<owner>/<repo>/contents/.orchestration/decisions.tsv?ref=<sha>`、sandbox 内）でその sha の内容を取得する。ローカルの `git show` は共有 object database が書けるため中間 tree の差し替えで偽物を返しうる（第 3 回審査の所見 2）（ローカルの ref 名 `origin/main` は経由しない。`refs/replace/` も書けるので replacement を無効にする。Codex worker は `.git/objects` と `.git/refs` に書けるので ref は差し替えられるが、sha で指した object は内容アドレスで偽造できない）。作業コピーの行は提案で、記録 PR が main にマージされて初めて承認になる（PR の承認は操作者の操作）。偽造には main へのマージが要る。 The same applies to the PR content a mechanism evaluates (the verdict, the audit precheck, the counters): the changeset is read from GitHub at the 40-hex head (`gh api repos/{owner}/{repo}/compare/<base40>...<head40>`, `…/contents/<path>?ref=<head40>`) or from a private clone whose object store no worker can write; the main checkout's shared `.git/objects` and its `origin/main` ref are not evidence sources, because Codex workers write them (a04 C-80 round 1, 2026-10-19). Evidence files are named and matched by the full 40-hex head, never by a 7-character prefix.

> 9. **私設キャッシュ** orchestrator 側の実行は worker と共有するキャッシュ（`~/.cache/uv`、`~/.local/share/uv`、mise）から実行可能物を読まない。`UV_CACHE_DIR` を anchored checkout 配下（`.agents/worklog/uv-cache`、gitignored、worker 書き込み不可）に固定し、`uv run --no-config --no-project --offline --python <信頼ルートの絶対パスのインタプリタ>` で起動する（`--no-config` で uv の設定探索を止め、`--python` の絶対パスで cwd や親の `.venv` の発見を止める；敵対的な `.venv` と `uv.toml` を置いた fixture で検証）。hook は uv を使わず jq と python 標準ライブラリだけで動く。 One trusted interpreter resolver (`scripts/orchestrator/trusted-interpreter.sh`, P1-3 lineage) resolves `<abs>` from the repository's pinned declaration to a regular file under the tool manager's install root, refuses anything else, and every orchestrator-side script consumes it; no script keeps its own `command -v`, `mise which` or PATH fallback (ci-rerun.sh security review 44cb835, 2026-10-19). Shell code of other projects (the agmsg storage layer and its `drivers.partition` sourcing) is never sourced by an orchestrator-side mechanism; counters are read from the agmsg SQLite store read-only with a fixed query or from the pasted record.


Host controls reduce accidents and prompt-injected damage. They do not isolate unrestricted processes sharing one UID. The design's GitHub prevention boundary is also not established while worker and orchestrator credentials remain accessible to that same UID; subsequent boundary-record checks provide detection as the design states.

## Branch and reset boundary

Continue `tools/verdict-audit-pool-a01`, PR #410, from `6b7e7833a85528440dc397c2555bc9dd603c685a`, already update-branched onto main `3f240b12`. Keep the a03 implementation, regression coverage and evidence. Create neither another implementation branch nor another PR.

The first push deletes `.orchestration/dotfiles-T133-verdict-audit-pool-a03/task.md` and adds the dispatched text byte-for-byte at `.orchestration/dotfiles-T133-verdict-audit-pool-a04/task.md`. This single predecessor-copy deletion is the explicit reset-bookkeeping exception to `allowed_files`. Other a03 evidence remains unchanged under its original task identifier and tested heads.

The orchestrator retains the a03 acceptance history, class rows, stopped status and counters. The final inventory identifies preserved a03 evidence separately from a04 additions; preservation does not authorize further worker edits in the a03 directory. The a01/a02 artifact removals already completed by a03 are not repeated or reversed.

The split remains intact. The pool sibling owns `scripts/orchestrator/audit-pool.sh`, changes to `scripts/orchestrator/orch-audit.sh`, `.schemas/classes.yaml` and `tests/unit/test_audit_pool.py`. `audit-pool.sh` is absent at `6b7e7833`; the audit schema at that head is `.schemas/audit.json`. Neither fact authorizes recreating a split file or adding a `schemas/` mirror. PR #407 remains parked; its parking operation is not repeated.

## Goal

Produce one schema-valid verdict from nine positively checked conditions without executing inherited shell startup code, accepting caller-selected executable directories, following output symlinks or treating invalid `security` metadata as an exemption.

Retain the a03 gate-before-application behavior, complete feedback validation, amended-cap precedence, offline operation, finding counts and trusted-checkout refresh.

## Files

1. `scripts/orchestrator/verdict.sh <pr> [--apply] [--loop] [--shadow]` remains Bash with `set -Eeuo pipefail`, English shdoc documentation and `jq` for JSON. Its startup and executable selection follow the Reset design below. Each condition is `{id, ok, evidence}` and becomes true only through a positive check of parsed, validated input.

   Inputs remain the PR view and checks, the acceptance record's JSON block and prose, the selected task or `--task <id>`, the audit JSON, a fresh feedback sweep, saved feedback dispositions, the task's allowed paths and caps, regime counters, the GitHub merge-base changeset and the head-specific security review. The acceptance block names the PR, task and current head and contains a ledger array. The PR is open, non-draft and based on `main`. Read `head.sha` and `base.sha` from `gh api repos/{owner}/{repo}/pulls/<pr>`, require both to be 40 lowercase hexadecimal characters, and bind all reads to those values. This task chooses GitHub API reads, not a local clone: read the changeset through `…/compare/<base40>...<head40>` and inspected PR bytes through `…/contents/<path>?ref=<head40>`. Repository identity is fixed from the trusted repository declaration, not caller environment or local Git configuration. Missing, incomplete, truncated or unreadable API data holds; no local-head fetch or shared-object fallback is allowed.

   Condition 1 verifies that the GitHub contents response for `.orchestration/<task>/precheck.json?ref=<head40>` hashes to the record's `precheck:` value and names the head or an ancestor authenticated by GitHub compare data whose diff to the head contains only `.orchestration/<task>/` paths. The retained `PRECHECK_REQUIRED` setting is supplied explicitly as `--precheck-required 0|1`; absent or zero makes this condition's failure a warning. No environment exception is added for it.

   Condition 2 requires every required check to be present with state `SUCCESS` for the head. Empty or unreadable checks hold. Every duplicate entry for a required name must also be `SUCCESS`.

   Condition 3 requires an audit that validates against `.schemas/audit.json`, names the task and full head, has zero open P0/P1 findings, and has verdict `correct` or a non-empty set of remaining findings whose scopes are all `records`. A blocked audit holds. An incorrect audit without remaining findings fails this condition.

   Condition 4 requires saved and fresh feedback documents to name the accepted head, complete feedback identity matching with multiplicity, and a valid disposition for every fresh item. Diagnostic URLs do not determine the result.

   Condition 5 requires every path in the base-to-head diff to match an `allowed_files` entry and additions-plus-deletions totals to remain within the effective Check caps. The comparison is `gh api repos/{owner}/{repo}/compare/<base40>...<head40>` using the PR API's base and head, and its full `merge_base_commit.sha` identifies the merge base. Consume the complete authenticated file list and its additions/deletions; account for both names of a rename. An unreadable merge base or incomplete changeset holds. The main checkout's `.git`, including `origin/main`, replacement refs and objects, is not an evidence source. Backticked exclusions after `outside` leave the outside count; default exclusions remain `tests/` and `.orchestration/`. Item 7 retains amendment precedence.

   Condition 6 reads one orchestrator-pasted INV-6 counters block in the acceptance record, bound there to this task, PR and full head. This task chooses the pasted record rather than a live store query so verdict executes no agmsg shell code and cannot follow worker-writable `drivers.partition`. It never invokes `scripts/regime-counters.sh` or sources the agmsg storage layer. No `S1:` line is present and the parsed decimal `revises` value is below 2. A missing ledger or counters block, duplicate block, mismatched binding or unreadable count holds; an absent count is never zero.

   Condition 7 requires the numeric count of open P0/P1 findings to be zero. Findings with status `new`, `still-open` or absent count as open regardless of identifier or scope.

   Condition 8 first validates `security` as an explicit boolean. Only boolean `false` permits the non-security branch. Boolean `true` requires the security review's front-matter `head:` to equal the verdict's own full 40-hex head and its last non-blank line to be `Verdict: correct`. A sha7 filename is never a head match. Missing, null or non-boolean metadata holds with the named reason specified below.

   Condition 9 requires at least one `sha256:<hex> <path>` line in the acceptance record's prose and verifies every such line against its file. Every inspected evidence file, including audit, security, local review and saved or fresh sweep, is named with and matched against the verdict's full 40-hex head: Markdown uses front-matter `head:`, audit and local-review JSON use `head` (on every record for a JSON list), and feedback JSON uses `head_sha`. Missing, invalid or different full-head metadata holds even when a filename or sha7 prefix matches. Hashes preserve consumed bytes; they do not authenticate a local Git object or ref.

   All nine conditions passing produces `accept`. Failure of condition 6 or 7, missing or unreadable input, schema-invalid input, invalid security metadata or an internal evaluation error produces `hold`. Other failed conditions produce `revise`. The revise line remains `AGMSG-ACCEPTANCE v1 task_id=<task> status=revise previous_head=<head> reason=<failed ids> next_action=<the first failed condition's evidence, shell-safe>`. The orchestrator supplies `check=` selectors.

   The generated verdict is `.orchestration/validation/<task>-verdict-<head>.json`, using the full 40-character head under design 5.14 item 5. Its fields remain `verdict`, `pr`, `head`, `task_id`, `conditions[]`, `inputs_sha256{}`, `generated_at` and optional `revise_line`, validated against `.schemas/verdict.json`. Audit, security, local-review and sweep inputs use full-head-named verified snapshots with the metadata bindings above. External producers are not edited; the orchestrator supplies the full-head-named evidence and required metadata before evaluation, retaining original artifacts separately. Historical verdict files remain untouched.

   Exit codes remain 0 for accept, 10 for revise, 20 for hold and 2 for usage or internal error, with internal error treated as hold. A destination or execution-boundary refusal holds with exit 20. Refusal before a usable task or head exists reports hold without inventing an output identity.

   `--apply` requires the trusted execution context and scripts, schemas and task files whose consumed bytes and complete file inventory equal GitHub's `base40` tree, read through its API at that SHA, with no substituted or extra executable helper in those code directories. Do not use local tracking status, `origin/main` equality or shared objects to authenticate them. Execute verified snapshots as Reset design item 2 requires. The last four shadow rows must agree between machine and human and represent four distinct PRs. Four rows for one PR do not unlock application. Item 6 retains the integration gate before either application effect.

   After accept and a successful gate, application writes the accepted line to a temporary file, sends it through `scripts/orchestrator/dispatch.sh <team> <from> <to> <pane> <file> <record>`, then invokes `gh pr merge <pr> --squash --match-head-commit <head>`. Its reason names `verdict-<head>`. Team, sender, recipient and placement remain explicit arguments. Arguments containing `--admin` or `--auto` anywhere are refused with exit 2 before input reads or tool calls other than mandatory startup sanitization.

   `--shadow` writes the verdict JSON and, only for a non-hold verdict, appends `<pr>\t<head>\t<verdict>\t\t\t<generated_at>` to `.orchestration/validation/verdict-shadow.tsv`. Columns remain `pr`, `head`, `machine`, `human`, `agree` and `at`; the orchestrator supplies the human and agreement columns. Shadow mode sends nothing and merges nothing.

   `--loop` retains PR-number order, eligible open non-draft PRs on `main`, and an acceptance record naming each current head. Each recursive verdict invocation uses the sanitized program-entry contract. The loop rereads GitHub's PR base and head between PRs and, with `--apply`, refreshes the trusted execution files from GitHub at the newly authenticated main/base SHA after each child, verifying their complete inventory and bytes before another child executes. Failed refresh holds with exit 20; a fetch or local fast-forward alone does not satisfy refresh. Neither evaluation nor refreshed execution uses the main checkout's shared refs or objects.

2. `.schemas/verdict.json` and `.schemas/audit.json` remain JSON Schema 2020-12 documents with `additionalProperties: false` at the top level and in defined item objects.

   The audit contains `head`, `task_id`, `auditor`, `generated_at`, `verdict` and findings with `id`, `priority`, `confidence`, `file`, `line`, `class`, `scope`, `rationale` and optional `status`. The controlled class enum retains the vocabulary snapshot at `b8998de162afc72d53d07679b8f0a194fcc480ff`.

   The existing stdlib schema validator remains available through `--validate` under the fixed isolated interpreter, without a new helper file or dependency. Required keys, types, enums, bounds, SHA patterns, additional-property restrictions and RFC 3339 timestamps with offsets remain checked. Date-only values, naive timestamps and invalid calendar dates fail. Runtime validation does not depend on the sibling's `orch-audit.sh --validate`.

3. The retained interpreter-selection requirement is implemented through Reset design item 2 rather than the a03 caller-bin mechanism.

   Before PR input processing, the trusted entrypoint fixes absolute executable identities and the offline PyYAML environment. Checkout `.python-version`, `.venv`, executable files, uv configuration, mise configuration and inherited tool-selection variables cannot select an interpreter or tool. Missing trusted installations or unavailable offline dependencies hold before dispatch or merge.

   The historical interpreter regression against `85a472294d0c10835bd7235e3c76d045846a6ed9` remains identified as historical. Its marker-writing interpreter cases run again against the final implementation.

4. The a02 and a03 finding-count and feedback fixes remain acceptance requirements.

   Conditions 3 and 7 count open P0/P1 findings numerically. Empty identifiers and records scope cannot hide a finding.

   Condition 4 requires both saved and fresh `head_sha` values to equal the accepted head. Missing or invalid dispositions are counted before formatting URLs; null and empty URLs affect diagnostics only.

   Complete identity and multiplicity retain the trusted helper's `feedback_key()` and `missing_feedback()` behavior. Source, URL, level, path, line, body and author participate, with only existing exact masked-body and masked-path equivalence. One saved occurrence covers one fresh occurrence.

   Dispositions retain `parse_disposition()` validation and `commit_in_range()` semantics, but verdict checks commit membership through complete GitHub compare/commit data instead of calling the helper's local-Git range check. A fix commit exists within the authenticated base-to-head range. A not-applicable disposition has a non-empty reason and evidence command and satisfies existing level-specific reason requirements. Evidence commands remain data and are never executed.

   Neither `scripts/require-crit-review.py` nor its validator is edited. Their execution and consumption follow design 5.14 item 4 by reference. Retained red evidence keeps its original head; final-head green results are new evidence.

exec
/bin/zsh -lc "rg -n 'Codex seat worklogs|"'^## |threat.table'"' ~/.agents/skills/agmsg-orchestration/SKILL.md" in ~/Workspace/dotfiles
 succeeded in 0ms:
10:## Architecture
17:## Regime activation and progress
29:## Parallel workers
46:## Identity, delivery, and storage
59:## Live verification
64:## Review and integration invariants
71:- A task that touches a trust boundary (anything the design tier lists, CI that decides a required check, code that executes PR-controlled input) carries a `threat_table` in its front matter: one `{control, disposition}` row per thing the PR or the orchestrator controls (the tree and its tests, task.md, workflow files, interpreter and environment files, in-process effects, new or renamed scripts, metadata separators). The row unit is one row per `allowed_files` entry, one row per listed control that is not a path (task metadata, workflow and interpreter or environment inputs, in-process effects, new or renamed scripts, metadata separators), carried by the declared test module's row where that is where the control acts, and one row per orchestrator effect from the fixed list (forced removal, merge, update-branch); under a wildcard `allowed_files` entry whose files are executed or applied (scripts, workflows, hooks, settings, the rules seats follow), one row per concrete file the PR changes; a wildcard over test fixtures or other data files keeps one row; C4 and C7b of `scripts/orchestrator/task-consistency-check.py` verify the path half before dispatch, and the task-file review checks the rest. A disposition takes one of three forms: `closed: tests/<file>::<name>`, the test that closes the row; `residual: <sentence>`, the compensating control; `out-of-scope: <task id>`, the task that owns the row. The task-file review checks the three shape rules by hand: a `closed` selector names a test present in the PR tree at acceptance, an `out-of-scope` owner is a task id in the design's `implementing_tasks`, a `residual` payload is a sentence of at least 20 characters (the gate's minimum for a reason). For a `closed` row it checks the selector's form only, since the test does not exist before implementation. Substance is the reviewers': the task-file review, the Bot and the auditor judge each row against the diff. The table is the task's completion condition: a missing row is added once, counted as an amendment, never fixed finding by finding.
95:## Message Contract v1
144:## `.orchestration` Workspace Layout
157:## Orchestrator Playbook
187:## Worker Playbook
217:## Codex seat worklogs
251:## Pitfalls

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

**Seeking efficient evidence reading**
exec
/bin/zsh -lc "nl -ba .orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md | sed -n '185,250p'" in ~/Workspace/dotfiles
exec
/bin/zsh -lc "sed -n '217,250p' ~/.agents/skills/agmsg-orchestration/SKILL.md" in ~/Workspace/dotfiles
exec
/bin/zsh -lc 'cat .orchestration/acceptance/dotfiles-T133-verdict-audit-pool-a03.md .orchestration/validation/dotfiles-T133-verdict-audit-pool-a03-security-513e5d0.md.last.md .orchestration/validation/dotfiles-T133-verdict-audit-pool-a03-security-6b7e783.md.last.md' in ~/Workspace/dotfiles
exec
/bin/zsh -lc "sed -n '1,110p' .orchestration/tasks/dotfiles-T133-verdict-audit-pool-a03.md" in ~/Workspace/dotfiles
exec
/bin/zsh -lc 'git status --short' in ~/Workspace/dotfiles
 succeeded in 103ms:
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


 succeeded in 198ms:
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
 succeeded in 266ms:
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
?? .orchestration/validation/dotfiles-T129-assets-omp-hcom-followup-a03-chain-1b3e0ee.log
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
?? .orchestration/validation/dotfiles-T133-hold-playbook-a01-chain-9f5eaee.log
?? .orchestration/validation/dotfiles-T133-hold-playbook-a01-local-review-9f5eaee.md
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
?? .orchestration/validation/dotfiles-T133-verdict-audit-pool-a04-text-security-6748694.md
?? .orchestration/validation/dotfiles-T133-verdict-audit-pool-a04-text-security-6748694.md.last.md
?? .orchestration/validation/dotfiles-T133-verdict-audit-pool-a04-text-security-b9bf09a.md
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

 succeeded in 279ms:
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

 succeeded in 295ms:
   185	
   186	   Complete identity and multiplicity retain the trusted helper's `feedback_key()` and `missing_feedback()` behavior. Source, URL, level, path, line, body and author participate, with only existing exact masked-body and masked-path equivalence. One saved occurrence covers one fresh occurrence.
   187	
   188	   Dispositions retain `parse_disposition()` validation and `commit_in_range()` semantics, but verdict checks commit membership through complete GitHub compare/commit data instead of calling the helper's local-Git range check. A fix commit exists within the authenticated base-to-head range. A not-applicable disposition has a non-empty reason and evidence command and satisfies existing level-specific reason requirements. Evidence commands remain data and are never executed.
   189	
   190	   Neither `scripts/require-crit-review.py` nor its validator is edited. Their execution and consumption follow design 5.14 item 4 by reference. Retained red evidence keeps its original head; final-head green results are new evidence.
   191	
   192	5. `tests/unit/test_verdict.py` retains all nineteen tests and their behavior coverage at `6b7e7833`, including schema-rule rejection, offline PyYAML refusal, numeric finding counts, feedback head binding, null diagnostic URLs, identity and multiplicity, disposition validation, gate ordering, amended caps, checkout refresh and cached-bytecode refusal.
   193	
   194	   The a03 test named `test_verdict_ignores_caller_bin_and_path_overrides` retains its coverage of hostile PATH selection while its removed executable-directory fixture is replaced by the fixed-entrypoint fixture. Neither the script nor the test source retains `VERDICT_BIN` or another production executable-directory override.
   195	
   196	   Existing positive and negative controls remain: empty checks, failed duplicate checks, blocked audits, incorrect audits without findings, missing ledgers and records, unavailable GitHub heads, unreadable GitHub merge bases, backticked cap exclusions, absent evidence hashes, PR-code-checkout refusal, four-distinct-PR enforcement and head-matched merge arguments.
   197	
   198	   Fixtures use temporary repositories and fake external tools whose absolute identities are established in the fixture's trusted entrypoint before invocation. They do not reintroduce caller PATH discovery or a production test-only override. The actual Python used for valid execution satisfies the interpreter boundary. All fixture lines count toward the test cap.
   199	
   200	6. The retained application-gate fix remains enforced.
   201	
   202	   After accept and shadow unlock, `--apply` runs the trusted `scripts/orchestrator/orch-gate.sh <task> <head> <pr>` and requires zero exit before dispatch or merge. Missing, refused or nonzero gate execution holds with exit 20, leaves no accepted application result and performs neither effect.
   203	
   204	   `test_verdict_apply_runs_the_integration_gate_before_dispatch_or_merge_and_holds_on_failure` retains failure, refusal, missing-gate and successful-gate controls. The successful order remains gate, dispatch, merge, with the exact task, full head, PR and head-matched merge arguments recorded.
   205	
   206	   Its original red result against `b8998de162afc72d53d07679b8f0a194fcc480ff` remains historical. The current gate wrapper's second positional argument is a PR-worktree path; this task changes no gate interface. Refusal of the specified head form remains hold, with no alternate gate or direct-merge fallback.
   207	
   208	7. The retained cap-parser fix remains enforced.
   209	
   210	   The last applicable cap declaration in text order governs, including its exclusions and outside limit. A later test-only amendment changes the test limit while retaining the outside limit.
   211	
   212	   `test_verdict_condition_5_honors_the_latest_amended_caps` retains the original 500 versus amended 550 case with 531 changed test lines, the actual a02 test-only wording, a later lower limit, changed exclusions and changed outside limit. Unrelated conditions stay green and evidence hashes are refreshed. Its original red head remains historical.
   213	
   214	The required check names remain `validate`, `test (ubuntu-24.04, server)`, `test (ubuntu-24.04, client)`, `test (macos-14, client)`, `public-bootstrap (ubuntu-24.04, server)`, `public-bootstrap (ubuntu-24.04, client)` and `public-bootstrap (macos-14, client)`.
   215	
   216	## Reset design
   217	
   218	1. **Privileged program startup precedes all statements.**
   219	
   220	   `verdict.sh` has mode 0755 and shebang `#!/bin/bash -p`. It is executed as a program. Privileged mode discards inherited functions, `BASH_ENV`/`ENV`, `SHELLOPTS`, `BASHOPTS`, `CDPATH` and `GLOBIGNORE` at startup, before the first statement.
   221	
   222	   The first executable compound statement rejects an invocation lacking privileged mode with the named message `verdict: execute as a program` and exit 20; under privileged mode it checks the environment names through absolute `/usr/bin/env` and `/usr/bin/grep` and re-executes under `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 /bin/bash --noprofile --norc -p "$0" "$@"` unless the environment already consists of exactly `PATH`, `HOME`, `LANG`, `PWD`, `SHLVL` and `_`. Require the fixed PATH and LANG values as well. A caller-set sentinel proves nothing and is not accepted. Long Bash options precede `-p`. This occurs before `set`, traps, function enumeration, argument processing or executable discovery. No `compgen`, `unset -f` loop or PATH edit serves as the startup boundary.
   223	
   224	   Every ordinary caller invokes the executable itself with `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8` as its prefix. The exact environment-name check terminates re-execution; no sentinel is exported or trusted. The retained `PRECHECK_REQUIRED` control is passed as the explicit `--precheck-required 0|1` argument when needed, defaults to 0, and is never inherited or retained as an environment name.
   225	
   226	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_program_discards_hostile_startup_environment` executes the program with exported functions named `compgen`, `[`, `test`, `exec`, `command`, `builtin` and `command_not_found_handle`, a marker-writing `BASH_ENV`, and a planted PATH. It checks that no marker appears and the verdict and condition results equal the clean invocation. The fixture also supplies the other startup selectors discarded by privileged mode. A separate subcase exports `VERDICT_SANITIZED=1` together with `GIT_CONFIG_GLOBAL`, `GIT_DIR` and `GIT_INDEX_FILE` pointing to planted files; it observes the re-exec and the child's allowed-name-only environment, verifies the planted configuration and object/index selectors are not consumed, and requires the same verdict and conditions as the clean invocation. Exercise the exact long-options-before-`-p` command so an exit 2 cannot satisfy the test.
   227	
   228	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_refuses_bash_file_invocation` invokes `bash scripts/orchestrator/verdict.sh …` in a clean fixture and requires exit 20 and the named message. This negative invocation is the sole deliberate non-program verdict call in the tests.
   229	
   230	2. **Executable identities are fixed at the trusted entrypoint.**
   231	
   232	   No caller-supplied executable directory exists. Remove `VERDICT_BIN`, its environment whitelist, symlink-directory acceptance and every equivalent caller override from the script and fixtures. Do not replace them with a differently named environment variable or CLI option.
   233	
   234	   The trusted entrypoint fixes the absolute paths for Bash, uv, Python, gh, git, jq and required utilities before reading PR-controlled input. It executes verified realpaths without rediscovery. The repository's Python declaration is a read-only input; consume `scripts/orchestrator/trusted-interpreter.sh` from the authenticated trusted base when present. The P1-3 resolver alone resolves the pinned declaration to a regular executable file under the tool manager's install root, outside worktrees, worker-writable caches and `$TMPDIR`. A symlink spelling alone authenticates nothing. An absent resolver or invalid trusted installation holds rather than selecting another interpreter from PATH, mise, uv discovery or a checkout. No private resolver, `command -v` or `mise which` fallback is retained here. Implementation may proceed before `dotfiles-T133-ci-efficiency-followup-a04` lands by implementing and testing this unavailable-resolver hold with a trusted resolver fixture for successful cases; live execution stays on hold until that lineage supplies the resolver. This task therefore does not need the resolver at implementation time and adds no P1-3 `after:` dependency.
   235	
   236	   Design 5.14 items 2, 4 and 9 apply by reference to Git invocation, executable paths, verified snapshots and private cache use. The uv invocation is `uv run --no-config --no-project --offline --python <abs>`, with uv itself an internally fixed absolute executable and `<abs>` the validated interpreter realpath. `UV_CACHE_DIR` is the anchored private cache from the design. Worker-shared uv or mise caches supply no executable. Python children use `-I`; the a03 `-B`, `sys.dont_write_bytecode` and refusal of checkout bytecode that helper imports could consume remain enforced.
   237	
   238	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_uses_only_declared_absolute_executables` verifies fixed tool identities with hostile PATH and inherited interpreter selectors, including an absolute symlink to a marker-writing interpreter.
   239	
   240	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_rejects_interpreters_in_worktrees_caches_or_tmp` covers each excluded root, a non-regular target and a valid trusted regular-file control.
   241	
   242	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_executes_verified_snapshots_and_records_input_hashes` changes a validated source or input before consumption and verifies refusal or consumption of the verified snapshot, never the substituted contents, and checks the recorded input hashes.
   243	
   244	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_holds_without_the_shared_trusted_interpreter_resolver` verifies the interim hold and absence of interpreter discovery or application effects.
   245	
   246	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_reads_pasted_counters_without_sourcing_agmsg` plants a marker-writing agmsg driver and counter executable, supplies the valid pasted counters, and requires unchanged verdicts with no marker; missing, duplicate, mismatched and unreadable counter cases hold.
   247	
   248	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_ignores_replaced_local_objects_and_refs` serves forged PR bytes through a replaced local object and forged `origin/main`, while fixed GitHub fixtures return the authentic full-head changeset and contents. It requires the clean verdict and authenticated input hashes, no local-object evidence read, and hold on incomplete API data rather than a local fallback. Cover precheck ancestry, fix-commit membership, application equality and loop refresh through the same GitHub fixtures.
   249	
   250	   The retained `test_verdict_pins_tools_interpreter_and_environment_before_reading_a_pr_checkout` and `test_verdict_never_imports_cached_bytecode` remain green. Unavailable offline PyYAML still holds with no online fallback.

**Managing token limits**
codex
The reset addresses the earlier `compgen`, caller-bin, bytecode and invalid-`security` defects explicitly. I’m now checking the remaining links between validation and execution: environment values, verified helpers and their dependencies, evidence paths, and the gate/merge handoff. I’ll keep worklogs unchanged under the read-only scope.
exec
/bin/zsh -lc "nl -ba .orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md | sed -n '192,246p'" in ~/Workspace/dotfiles
 succeeded in 0ms:
   192	5. `tests/unit/test_verdict.py` retains all nineteen tests and their behavior coverage at `6b7e7833`, including schema-rule rejection, offline PyYAML refusal, numeric finding counts, feedback head binding, null diagnostic URLs, identity and multiplicity, disposition validation, gate ordering, amended caps, checkout refresh and cached-bytecode refusal.
   193	
   194	   The a03 test named `test_verdict_ignores_caller_bin_and_path_overrides` retains its coverage of hostile PATH selection while its removed executable-directory fixture is replaced by the fixed-entrypoint fixture. Neither the script nor the test source retains `VERDICT_BIN` or another production executable-directory override.
   195	
   196	   Existing positive and negative controls remain: empty checks, failed duplicate checks, blocked audits, incorrect audits without findings, missing ledgers and records, unavailable GitHub heads, unreadable GitHub merge bases, backticked cap exclusions, absent evidence hashes, PR-code-checkout refusal, four-distinct-PR enforcement and head-matched merge arguments.
   197	
   198	   Fixtures use temporary repositories and fake external tools whose absolute identities are established in the fixture's trusted entrypoint before invocation. They do not reintroduce caller PATH discovery or a production test-only override. The actual Python used for valid execution satisfies the interpreter boundary. All fixture lines count toward the test cap.
   199	
   200	6. The retained application-gate fix remains enforced.
   201	
   202	   After accept and shadow unlock, `--apply` runs the trusted `scripts/orchestrator/orch-gate.sh <task> <head> <pr>` and requires zero exit before dispatch or merge. Missing, refused or nonzero gate execution holds with exit 20, leaves no accepted application result and performs neither effect.
   203	
   204	   `test_verdict_apply_runs_the_integration_gate_before_dispatch_or_merge_and_holds_on_failure` retains failure, refusal, missing-gate and successful-gate controls. The successful order remains gate, dispatch, merge, with the exact task, full head, PR and head-matched merge arguments recorded.
   205	
   206	   Its original red result against `b8998de162afc72d53d07679b8f0a194fcc480ff` remains historical. The current gate wrapper's second positional argument is a PR-worktree path; this task changes no gate interface. Refusal of the specified head form remains hold, with no alternate gate or direct-merge fallback.
   207	
   208	7. The retained cap-parser fix remains enforced.
   209	
   210	   The last applicable cap declaration in text order governs, including its exclusions and outside limit. A later test-only amendment changes the test limit while retaining the outside limit.
   211	
   212	   `test_verdict_condition_5_honors_the_latest_amended_caps` retains the original 500 versus amended 550 case with 531 changed test lines, the actual a02 test-only wording, a later lower limit, changed exclusions and changed outside limit. Unrelated conditions stay green and evidence hashes are refreshed. Its original red head remains historical.
   213	
   214	The required check names remain `validate`, `test (ubuntu-24.04, server)`, `test (ubuntu-24.04, client)`, `test (macos-14, client)`, `public-bootstrap (ubuntu-24.04, server)`, `public-bootstrap (ubuntu-24.04, client)` and `public-bootstrap (macos-14, client)`.
   215	
   216	## Reset design
   217	
   218	1. **Privileged program startup precedes all statements.**
   219	
   220	   `verdict.sh` has mode 0755 and shebang `#!/bin/bash -p`. It is executed as a program. Privileged mode discards inherited functions, `BASH_ENV`/`ENV`, `SHELLOPTS`, `BASHOPTS`, `CDPATH` and `GLOBIGNORE` at startup, before the first statement.
   221	
   222	   The first executable compound statement rejects an invocation lacking privileged mode with the named message `verdict: execute as a program` and exit 20; under privileged mode it checks the environment names through absolute `/usr/bin/env` and `/usr/bin/grep` and re-executes under `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 /bin/bash --noprofile --norc -p "$0" "$@"` unless the environment already consists of exactly `PATH`, `HOME`, `LANG`, `PWD`, `SHLVL` and `_`. Require the fixed PATH and LANG values as well. A caller-set sentinel proves nothing and is not accepted. Long Bash options precede `-p`. This occurs before `set`, traps, function enumeration, argument processing or executable discovery. No `compgen`, `unset -f` loop or PATH edit serves as the startup boundary.
   223	
   224	   Every ordinary caller invokes the executable itself with `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8` as its prefix. The exact environment-name check terminates re-execution; no sentinel is exported or trusted. The retained `PRECHECK_REQUIRED` control is passed as the explicit `--precheck-required 0|1` argument when needed, defaults to 0, and is never inherited or retained as an environment name.
   225	
   226	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_program_discards_hostile_startup_environment` executes the program with exported functions named `compgen`, `[`, `test`, `exec`, `command`, `builtin` and `command_not_found_handle`, a marker-writing `BASH_ENV`, and a planted PATH. It checks that no marker appears and the verdict and condition results equal the clean invocation. The fixture also supplies the other startup selectors discarded by privileged mode. A separate subcase exports `VERDICT_SANITIZED=1` together with `GIT_CONFIG_GLOBAL`, `GIT_DIR` and `GIT_INDEX_FILE` pointing to planted files; it observes the re-exec and the child's allowed-name-only environment, verifies the planted configuration and object/index selectors are not consumed, and requires the same verdict and conditions as the clean invocation. Exercise the exact long-options-before-`-p` command so an exit 2 cannot satisfy the test.
   227	
   228	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_refuses_bash_file_invocation` invokes `bash scripts/orchestrator/verdict.sh …` in a clean fixture and requires exit 20 and the named message. This negative invocation is the sole deliberate non-program verdict call in the tests.
   229	
   230	2. **Executable identities are fixed at the trusted entrypoint.**
   231	
   232	   No caller-supplied executable directory exists. Remove `VERDICT_BIN`, its environment whitelist, symlink-directory acceptance and every equivalent caller override from the script and fixtures. Do not replace them with a differently named environment variable or CLI option.
   233	
   234	   The trusted entrypoint fixes the absolute paths for Bash, uv, Python, gh, git, jq and required utilities before reading PR-controlled input. It executes verified realpaths without rediscovery. The repository's Python declaration is a read-only input; consume `scripts/orchestrator/trusted-interpreter.sh` from the authenticated trusted base when present. The P1-3 resolver alone resolves the pinned declaration to a regular executable file under the tool manager's install root, outside worktrees, worker-writable caches and `$TMPDIR`. A symlink spelling alone authenticates nothing. An absent resolver or invalid trusted installation holds rather than selecting another interpreter from PATH, mise, uv discovery or a checkout. No private resolver, `command -v` or `mise which` fallback is retained here. Implementation may proceed before `dotfiles-T133-ci-efficiency-followup-a04` lands by implementing and testing this unavailable-resolver hold with a trusted resolver fixture for successful cases; live execution stays on hold until that lineage supplies the resolver. This task therefore does not need the resolver at implementation time and adds no P1-3 `after:` dependency.
   235	
   236	   Design 5.14 items 2, 4 and 9 apply by reference to Git invocation, executable paths, verified snapshots and private cache use. The uv invocation is `uv run --no-config --no-project --offline --python <abs>`, with uv itself an internally fixed absolute executable and `<abs>` the validated interpreter realpath. `UV_CACHE_DIR` is the anchored private cache from the design. Worker-shared uv or mise caches supply no executable. Python children use `-I`; the a03 `-B`, `sys.dont_write_bytecode` and refusal of checkout bytecode that helper imports could consume remain enforced.
   237	
   238	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_uses_only_declared_absolute_executables` verifies fixed tool identities with hostile PATH and inherited interpreter selectors, including an absolute symlink to a marker-writing interpreter.
   239	
   240	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_rejects_interpreters_in_worktrees_caches_or_tmp` covers each excluded root, a non-regular target and a valid trusted regular-file control.
   241	
   242	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_executes_verified_snapshots_and_records_input_hashes` changes a validated source or input before consumption and verifies refusal or consumption of the verified snapshot, never the substituted contents, and checks the recorded input hashes.
   243	
   244	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_holds_without_the_shared_trusted_interpreter_resolver` verifies the interim hold and absence of interpreter discovery or application effects.
   245	
   246	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_reads_pasted_counters_without_sourcing_agmsg` plants a marker-writing agmsg driver and counter executable, supplies the valid pasted counters, and requires unchanged verdicts with no marker; missing, duplicate, mismatched and unreadable counter cases hold.

exec
/bin/zsh -lc 'cat .orchestration/validation/dotfiles-T133-verdict-audit-pool-a04-text-security-6748694.md.last.md' in ~/Workspace/dotfiles
 succeeded in 0ms:
- [P1] High confidence [.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:206](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:206) — Caller-set `VERDICT_SANITIZED=1` skips `env -i`; `bash -p` preserves `GIT_*`, so fixed binaries still consume attacker-selected Git configuration and object stores; read-only probes confirmed both survive the proposed sentinel check. [Bash semantics](https://www.gnu.org/s/bash/manual/html_node/The-Set-Builtin.html)

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:130](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:130) — The retained counter sources agmsg storage code, whose `drivers.partition` selects a sourced file through worker-writable team configuration; pinning the counter and its interpreter does not bind that descendant execution, and this known route lacks a threat row or compensating control.

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:144](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:144) — Equality to local `origin/main` and the merge-base calculation still trust shared refs/objects that sandboxed Codex workers can write; snapshot hashes preserve the selected bytes without authenticating them against GitHub, allowing the evaluated changeset to differ from the actual PR.

- [P2] High confidence [.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:134](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:134) — Condition 8 checks only the security report’s final verdict while retaining its sha7 filename; a different head sharing that prefix can reuse an earlier approval because no full-head content check is required, and full-head output names do not mitigate this input collision.

- [P2] High confidence [.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:206](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:206) — The prescribed `/bin/bash -p --noprofile --norc` re-exec exits 2 on this host before evaluation; Bash requires long options before `-p`, so the hostile-startup regression cannot produce the required clean-equivalent verdict through this branch. [Invocation rules](https://www.gnu.org/software/bash/manual/html_node/Invoking-Bash.html)

📝 まとめ: Reviewed every declared threat row and the cited context; five findings remain for orchestrator disposition.
Not run: implementation tests, live CI or deployment checks; no files changed. The execution and evidence-binding risks above remain unresolved.
Verdict: incorrect
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

exec
/bin/zsh -lc "sed -n '1,180p' .orchestration/tasks/dotfiles-T133-verdict-audit-pool-a03.md" in ~/Workspace/dotfiles
 succeeded in 0ms:
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

exec
/bin/zsh -lc "rg -n '5\\.14|D-024-20|Linux|case.insensitive|same.UID|gh.*sandbox|shim' .orchestration/plans/024-design-quality.md" in ~/Workspace/dotfiles
 succeeded in 0ms:
88:| 〃 | 権限・信頼境界を広げるタスク（excludedCommands、allowMachLookup、hooks で gh 書込を決める、sandbox の allowWrite） | **人** | 下の「権限の変更」に合流 | ユーザー |
99:## 5.14 信頼ホスト実行契約（trusted-host execution contract、D-024-18）
103:1. **書き込み境界（前提 6、ランタイム別に正直に）** Claude worker 席は専用の設定ディレクトリ `CLAUDE_CONFIG_DIR=~/.claude-worker`（chezmoi が描画、operator が一度 login）で起動し、orchestrator の `~/.claude` と設定を共有しない。worker 設定：除外コマンド無し、Herdr socket 無し、sandbox の allowWrite は自席 worktree と agmsg store と席別キャッシュだけ、`failIfUnavailable: true`、信頼パス（anchored checkout の `.claude/worktrees/` 以外、`~/.agents`、`~/.claude*`、`~/.local`、`~/.config`）への Edit deny（公式文書：file tool の permission 検査は要求パスと symlink 解決後のパスの両方に deny を適用し、symlink そのものへの書き込みは拒否する）、sandbox の強制範囲はユーザー設定ではなく **managed settings**（`/Library/Application Support/ClaudeCode/managed-settings.json`、公式文書 "Repository settings under an admin-required sandbox"：project/local 設定は sandbox を無効化したり除外・socket を足したりできない）に置く。chezmoi は user ではこのファイルを書けないので、描画した内容を操作者が `sudo` で一度配置する（操作者手順）。worker 設定は worktree 自身の `.claude/**` と `.mcp.json` への Edit deny（`//<anchored>/.claude/worktrees/*/.claude/**`）を持つ（Bash 側は sandbox 既定の settings/hooks の denyWithinAllow）。agmsg store（全席が書く）から配送 hook が driver や plugin を source する上流の経路（storage.sh の `drivers.partition` traversal、`db/trusted-plugins` と `plugins/partition/shared.sh` による差し替え承認）は別タスク（agmsg hardening）の行で、worker 設定は `~/.agents/skills/agmsg/plugins/**` と `~/.agents/skills/agmsg/db/trusted-plugins` への書き込みを deny し（Edit deny は sandbox の deny にも合流する）、hook 側は store 由来の設定値を検証するまで残余と書く。managed settings の配置先は OS で異なる（macOS `/Library/Application Support/ClaudeCode/managed-settings.json`、Linux `/etc/claude-code/managed-settings.json`）。hook は agmsg 配送だけを、hook コマンドを `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<home> …` で始めて（`BASH_ENV` などの継承環境を bash 起動前に消す；PATH 固定だけでは BASH_ENV が先に走る）絶対パスのインタプリタで呼び（上流の agmsg スクリプトは `/usr/bin/env bash` の shebang を持つので、hook 実行環境の PATH が shim を含まないことで束縛する）、各 hook に `onFailure: "block"`。公式文書：linked worktree の session は **main checkout の `.claude/settings.local.json` を読む**ので、worker 向けの hook を worktree の settings.local.json に書いても読まれず、逆に orchestrator の local hooks が worker session でも走る。したがって orchestrator 側の local hooks も guard 経由にし、worker 側の hook は worker config dir の settings に置く。Edit deny の一覧は `git ls-tree` ではなく描画時の静的一覧（manifest に列挙、`.agents/worklog/**` と `.agents/worklog/uv-cache/**` を含む）とし、`~/.agents/**` の全面 deny は agmsg store の書き込みと矛盾するので、`~/.agents/agent-config.yaml`、`~/.agents/skills/**/scripts/**`、`~/.agents/model-profiles.env` などストア以外を列挙する。公式文書で確認した事実（2026-10-19）：`Edit(path)` の deny は Write/MultiEdit/NotebookEdit にも効き、deny → ask → allow の順で最初の一致が決まる；ただし Read/Edit の deny は **Bash sandbox の設定にも合流する**（"Paths and domains from both sandbox settings and permission rules are merged into the final sandbox configuration"）ので、ユーザー設定（全席共有）に `.orchestration/**` の Edit deny を書くと orchestrator の Bash による記録書き込みも止まる。hook は起動時に固定されず、設定ファイルの編集は file watcher が即座に反映する。`sandbox.failIfUnavailable` の既定は fail-open（依存が無ければ sandbox 無しで実行）。したがって Claude 席の境界は Edit deny 規則ではなく、**ユーザーレベルの PreToolUse hook**（`~/.claude/hooks/worker-write-boundary`、chezmoi が描画、`/bin/sh` または絶対パスの `python3 -I`）で作る：cwd の realpath が `<anchored>/.claude/worktrees/` 配下の session では、Write/Edit/MultiEdit/NotebookEdit の対象が cwd の外、または `<cwd>/.claude/**`・`<cwd>/.mcp.json` のとき `permissionDecision: deny` を返す。Bash 側は sandbox の既定 `denyWithinAllow`（settings、hooks）と `allowWrite`（自席 worktree）が担う。`failIfUnavailable: true` を全席に置く。 Codex 席は sandbox（workspace-write）がツールの書き込み全部を自席の worktree と列挙パスに限る。Claude 席は Seatbelt sandbox が Bash を限るだけで、Write/Edit/MultiEdit/NotebookEdit、hook、MCP プロセスは sandbox 外で動き、permission policy（permgate の決定論ポリシー）が path で拒否しない限り anchored checkout や `~/.agents` にも書ける（2026-10-19 時点、描画済み設定にその deny は無い）。したがって前提 6 は「Codex 席は成立、Claude 席は P1-15 が描画設定に Edit の path deny を入れるまで残余」と書く。P1-15 以前に「worker は信頼ルートに書けない」と書く文は誤りで、C-80 が拒否する。P1-15 が入るまで、承認の出所は項目 8 の「コミット済み台帳」で守る。書き込みは自席の worktree（`.claude/worktrees/<name>`）、scratch、列挙されたツールキャッシュに限る。anchored checkout（`.claude/worktrees/` 以外）、`~/.agents/agent-config.yaml`、`~/.claude/hooks`、信頼ルートのバイナリ、orchestrator の証跡・スナップショット・lock は worker から書けない。render テストが描画後の deny を検証する。残余は「どの席 sandbox にも属さない同一 UID プロセス」と、Worker Playbook step 4 が sandbox 外に出す少数のコマンド（gh）。後者は D-024-17（P1-15）で絶対パスの実行体に束縛する。
104:2. **無害化した環境を最初に** 最初の処理として `env -i` に入り、PATH は信頼ルートで解決した絶対バイナリへのリンクだけの私設ディレクトリ（shims、空、相対は拒否）。git は毎回 `GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null -c core.hooksPath=/dev/null -c core.fsmonitor=false -c protocol.allow=never -c protocol.https.allow=always` と明示 `-C`（https だけ許す。`protocol.allow=never` 単独は必要な fetch を止める）。 検査の読み取りは `GIT_NO_LAZY_FETCH=1` で部分クローンの遅延 fetch（checkout 設定の credential.helper を起動しうる）を止め、`-c submodule.recurse=false --ignore-submodules=all` で submodule 内の status/diff（submodule 自身の設定が filter を有効化しうる）を止める。`.gitmodules` を持つ checkout は検査対象として拒否する。 `-C` は作業木を束縛しないので（repo-local の `core.worktree` が読み先を checkout 外へ向けられる）、git は `--git-dir=<checkout>/.git --work-tree=<checkout>` を明示し、`git rev-parse --show-toplevel` の realpath が checkout と一致しないときは拒否する。 premise や検査の「コマンド実行」は、固定語彙の読み取り専用プローブ（`git rev-parse <ref>`、`test -e <path>`、`grep -c <pattern> <file>` のように検査器自身が解釈する形）だけを許し、任意のシェル文字列は実行しない（本文のハッシュはコマンド文を認証するだけで、`python -I scripts/x.py` のファイル被演算子や `source ./x.sh` の中身は認証しない）。diff と show は `--no-ext-diff --no-textconv` と `-c core.attributesFile=/dev/null -c core.sshCommand=false` を付け、PR 側の `.gitattributes`（external diff、textconv、filter）が検査内容や実行物を変えないようにする。Python は `-I`。PATH 探索で実行するものは無い。 A shell script that runs under a PR-controlled or worker-controlled environment (verdict.sh, the chain glue, CI steps) is executed as a program with `#!/bin/bash -p`, never as `bash <file>`: privileged mode discards inherited functions, `BASH_ENV`/`ENV`, `SHELLOPTS`, `BASHOPTS`, `CDPATH` and `GLOBIGNORE` before the first statement, and the first statement re-executes the program under `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 /bin/bash --noprofile --norc -p "$0" "$@"` (long options before `-p`: bash exits 2 otherwise) unless its environment already consists of exactly the allowed names, checked through absolute paths (`/usr/bin/env`, `/usr/bin/grep`) under `-p`; a caller-set sentinel variable is not a sanitization proof, because the caller controls it (a04 C-80 round 1, 2026-10-19); sanitization performed by later statements (unset -f, compgen, PATH edits) is not a boundary, because the statements themselves resolve through the untrusted names (PR #410 security reviews 513e5d0 and 6b7e783, 2026-10-19). No script accepts a caller-supplied executable directory; interpreters are the fixed absolute paths item 9 names.
109:0. **脅威モデル（D-024-21）** 席は同じ OS ユーザで動き、ホストは席間の信頼境界ではない（同一 UID のプロセスは symlink 差し替え、共有 `.git` の object 差し替え、hook の子プロセス、Herdr socket 経由の host 実行で、ホスト内のどの検査も迂回できる）。regime の硬い境界は GitHub（保護された main、必須チェック、orchestrator の identity によるマージ）。ただしこの境界は **worker 席が orchestrator の GitHub 資格情報を共有しない**ときだけ成立する（D-024-22：worker 席は専用の GitHub identity（別アカウントまたは App のトークン）で `gh` に login し、ruleset の bypass 一覧に入らない。orchestrator の keychain トークンを worker の config dir に持ち込まない。identity が分かれるまで「GitHub が境界」は未成立と書く）。**同一 macOS ユーザでは資格情報は分離できない**（gh は keychain の項目を host/user で引き、同じ UID の gh は orchestrator のトークンを読める。`GH_CONFIG_DIR` は設定を分けるだけ）。防止には worker 席を別の OS ユーザ（または別ホスト）で動かすしかなく、それは D-024-23 の将来項目（P1-16、操作者の判断）。それまで GitHub 境界は **検知**で守る：記録は boundary の記録 PR まで main に無いので、検知は次の記録 PR の regime ジョブで行う（`.orchestration/acceptance/**` に触れる PR で、前回 boundary 以降の main の各マージ commit に、gate 通過の証跡を持つ受け入れ記録が対応することを検査し、無ければその PR を失敗させる；P1-11 owner a02 の行 `ci:detection:1`）。main push 時点の検知は記録が無いので不可能であり、文は「次の記録 PR で検知、防止ではない」と書く。悪意ある worker に耐えるべき入力（承認台帳、gate が読む証跡 of record）は GitHub から sha 指定で API 経由（sandbox 内）に読み、ローカルファイルやローカル object database からは読まない。ホスト内の制御（本節 1〜10）は事故と prompt injection による損害の抑制であり、文はそう書く。
110:8. **承認はコミット済み台帳から読む** permission の決定行（`scope=permission approved_by=user diff_sha256=…`）は anchored checkout の作業コピーではなく、コミット済みの台帳から読む。読み方は `git ls-remote origin refs/heads/main` が返す commit sha を取り、GitHub API（`gh api repos/<owner>/<repo>/contents/.orchestration/decisions.tsv?ref=<sha>`、sandbox 内）でその sha の内容を取得する。ローカルの `git show` は共有 object database が書けるため中間 tree の差し替えで偽物を返しうる（第 3 回審査の所見 2）（ローカルの ref 名 `origin/main` は経由しない。`refs/replace/` も書けるので replacement を無効にする。Codex worker は `.git/objects` と `.git/refs` に書けるので ref は差し替えられるが、sha で指した object は内容アドレスで偽造できない）。作業コピーの行は提案で、記録 PR が main にマージされて初めて承認になる（PR の承認は操作者の操作）。偽造には main へのマージが要る。 The same applies to the PR content a mechanism evaluates (the verdict, the audit precheck, the counters): the changeset is read from GitHub at the 40-hex head (`gh api repos/{owner}/{repo}/compare/<base40>...<head40>`, `…/contents/<path>?ref=<head40>`) or from a private clone whose object store no worker can write; the main checkout's shared `.git/objects` and its `origin/main` ref are not evidence sources, because Codex workers write them (a04 C-80 round 1, 2026-10-19). Evidence files are named and matched by the full 40-hex head, never by a 7-character prefix.
112:10. **worker は sandbox 外でコマンドを実行しない（D-024-17 の改訂）** 2026-10-19T03:45Z の実測で `gh api` は Claude sandbox の中から成功した（sandbox の proxy は CONNECT 型で TLS を終端しない；keychain のトークンも読めた）。worker 席の除外コマンドは空にし、gh も git push も sandbox 内の proxy 経由で実行する。Codex 席は `sandbox_workspace_write.network_access = true` で同じ状態にし、permgate の codex ポリシーは sandbox 外への escape を承認しない（permgate の変更は操作者の手順）。wrapper 方式（絶対パス、env -i、固定 GH_CONFIG_DIR）は LD_PRELOAD と引数転送（`gh repo clone -- --config`）を閉じられないので採らない。
113:7. **検証** threat_table は本節の項目 1〜10 に 1 行ずつ対応させる（参照だけでは足りない）。共通テスト補助 `tests/unit/trusted_exec_contract.py`（P1-6 で作る）を使い、仕組みごとに 4 つの red→green テストを持つ：PATH 先頭の shim が実行されない、植え付けた GIT_* と git 設定が効かない、worker ルート配下の信頼パスが拒否される、検証後に差し替えたファイルが消費側に届かない。

**Analyzing GH config resolution**
exec
/bin/zsh -lc "sed -n '1,240p' scripts/orchestrator/orch-gate.sh" in ~/Workspace/dotfiles
exec
/bin/zsh -lc "sed -n '99,116p' .orchestration/plans/024-design-quality.md" in ~/Workspace/dotfiles
exec
/bin/zsh -lc "sed -n '1,230p' scripts/orchestrator/dispatch.sh" in ~/Workspace/dotfiles
exec
/bin/zsh -lc "rg -n 'HOME|install root|realpath|shim|case|trusted|gh |Python|resolver' .orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md" in ~/Workspace/dotfiles
 succeeded in 210ms:
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

 succeeded in 288ms:
#!/usr/bin/env bash
# @file dispatch.sh
# @brief Send one AGMSG-TASK, AGMSG-ACCEPTANCE or AGMSG-PING line after checking its sha256 fields, and record it.
# @description
#   Plan 007 T718 (C-20). Reads exactly one physical line from a file (a second
#   line, blank or not, or a NUL byte is refused). Every `<name>_sha256=<64
#   hex>` token is recomputed from the file its sibling token names,
#   `<name>_file=` or else `<name>=` (`task_sha256` from `task_file=`,
#   `design_sha256` from `design=`, `amended_task_sha256` from `amended_task=`;
#   a line naming the file both ways, or repeating one of these keys, is
#   refused), except a `previous_<name>_sha256=` reference to an earlier
#   version, which is checked as 64 lowercase hex only; every line must carry
#   exactly one non-empty `task_id=`, and an AGMSG-TASK line must carry
#   `task_file=` and `task_sha256=`. Tokens are separated by any run of spaces
#   and tabs, and every token after `v1` is `<key>=<value>` (exit 2 otherwise,
#   so a repeated prefix or a value split by a space is refused); the
#   recorder takes `task_id` from that one parse (thread 4255272793). A relative path is read from the root of
#   the checkout this script lives in (`git rev-parse --show-toplevel` there, under the allowlisted environment),
#   never from the caller's directory. A missing field or file, a malformed value
#   or a mismatch exits 1 naming the field, and nothing is sent. Otherwise the
#   line goes to `agmsg-dispatch` as one argument, byte for byte.
#   With an acceptance record, the record is checked before the send and, once
#   the line is on the bus, `<the line> read_at=<read|unread>` is appended to
#   the `dispatch` list of
#   the record's JSON block, the object between its first two `---` lines. The
#   block is read and written with Python's standard json (malformed JSON, a
#   duplicate key, NaN or Infinity, a block that is not an object or a
#   `dispatch` that is not a list is refused; `sort_keys`, `indent=2`); the key
#   is created when absent, and a record without a block gets a block holding
#   only `dispatch`. The prose after the block is kept byte for byte, CRLF
#   included (thread 4256987087), and the record is replaced atomically (a
#   temporary file in its directory, fsync, rename) under an exclusive `flock`
#   of that directory, so two dispatches to one record never lose an entry
#   (thread 4255272797). A record that is not an existing regular file writable in a
#   writable directory, or whose `task` is not the line's `task_id`, is refused
#   before the send, and nothing is sent.
#   An AGMSG-TASK line whose `task_file=` fails `task-consistency-check.py`
#   (beside this script, run as `python -I` through `uv run --offline`, PyYAML from the pinned cache only,
#   with `--no-config`, `--no-project` and a pinned `--python`, from the root, under `env -i` with only
#   `PATH`, `HOME` (the script owner's passwd home), `UV_CACHE_DIR` (under it), `LANG`, `LC_ALL` and the `AGMSG_*`
#   variables) is refused with the checker's output, and nothing is sent (C-52).
#   Only a review brief is exempt: a front matter (the text between the first
#   two `---` lines) that PyYAML parses, refusing a duplicate key, to a mapping
#   whose `kind` is the string `review`; every other outcome runs the checker.
#   Only a bus row this send created is recorded. Both reads of the team-wide
#   `history.sh <team> "" <BUS_READ_WINDOW>` take the newest rows (C-53: a
#   whole-bus read took 56 minutes on a 1385-row team), and the recorder aligns
#   them as two views of one bus: the pre-send window (each row's timestamp,
#   sender, recipient and text) goes to a private `mktemp` file removed on exit;
#   after the send every shift j from 0 to m-1 of the m post-send rows is tried,
#   and exactly one may leave the post-send window, without its j newest rows,
#   equal to the pre-send window without the rows that left it (all m new rows
#   when the pre-send window was empty). This send is the last of those j new
#   rows equal to the line, sender and recipient. No fit, several fits (a
#   periodic bus), j = 0 or no equal new row leaves the record unchanged and
#   exits 1. The read state is the marker history.sh prints for that row
#   (`●` unread, `○` read): agmsg's scripts expose no read_at time, this script
#   never reads the message database, and it never passes an agent to
#   history.sh, whose agent argument renames the caller's pane after it.
# @arg $1 string agmsg team.
# @arg $2 string Sender identity.
# @arg $3 string Recipient identity.
# @arg $4 string Recipient pane id (for example `w5:pA`).
# @arg $5 path File holding the line.
# @arg $6 path Optional acceptance record (`.orchestration/acceptance/<task>.md`), relative to the current directory.
# @env AGMSG_SCRIPTS The agmsg scripts directory (default `$HOME/.agents/skills/agmsg/scripts`).
# @env BUS_READ_WINDOW The newest rows each history read takes (default 200, a positive integer).
# @exitcode 0 Sent, and recorded when a record was given (agmsg-dispatch's own status otherwise).
# @exitcode 1 A field check failed, the task file fails the task-consistency check, the record is malformed, or the sent line was not recorded.
# @exitcode 2 Usage error, the file is not one AGMSG-TASK, AGMSG-ACCEPTANCE or AGMSG-PING v1 line, or PyYAML is not in
#   the pinned uv cache (run `make validate-agent-assets` to warm it).
# @example
#   scripts/orchestrator/dispatch.sh dotfiles-conformance claude-deep-dot claude-standard-dot-a003 w5:pA \
#     "$TMPDIR/task-line.txt" .orchestration/acceptance/dotfiles-T128-orchestrator-tools-a01.md
set -euo pipefail

usage() {
    echo "usage: dispatch.sh <team> <from> <to> <pane> <line-file> [<acceptance-record>]" >&2
    exit 2
}
(($# == 5 || $# == 6)) || usage
team=$1 from=$2 to=$3 pane=$4 file=$5 record=${6:-}
[[ -f ${file} ]] || usage
# Thread 4256541716: command substitution drops a NUL byte, so the line sent would not be the file's.
if (($(tr -d '\0' < "${file}" | wc -c) != $(wc -c < "${file}"))); then
    echo "dispatch: ${file} holds a NUL byte" >&2
    exit 2
fi
# The sentinel keeps every trailing newline, which $( ) alone would drop (thread 4254107304).
line="$(cat -- "${file}" && printf x)" && line=${line%x} && line=${line%$'\n'}
[[ ${line} != *$'\n'* ]] || {
    echo "dispatch: ${file} holds more than one line" >&2
    exit 2
}
[[ ${line} =~ ^AGMSG-(TASK|ACCEPTANCE|PING)[[:blank:]]+v1[[:blank:]] ]] || {
    echo "dispatch: not an AGMSG-TASK, AGMSG-ACCEPTANCE or AGMSG-PING v1 line" >&2
    exit 2
}
# One allowlisted environment for git and uv: no inherited GIT_DIR, GIT_WORK_TREE or other GIT_*, VIRTUAL_ENV, UV_* or
# PYTHON* variable chooses the root, the interpreter or the code they run (audit:ef74eae:1, C-57).
# HOME is the script owner's passwd home and the uv cache sits under it, never inherited values (4300738707).
owner="$(stat -c %U -- "${BASH_SOURCE[0]}" 2> /dev/null || stat -f %Su -- "${BASH_SOURCE[0]}")" || owner=
[[ ${owner} =~ ^[A-Za-z0-9._][A-Za-z0-9._-]*$ ]] || {
    echo "dispatch: cannot tell the owner of ${BASH_SOURCE[0]}" >&2
    exit 1
}
home=
eval "home=~${owner}" # the name is checked above; ~name is its passwd home
[[ ${home} == /* ]] || {
    echo "dispatch: no passwd home for ${owner}" >&2
    exit 1
}
clean=(env -i PATH="${PATH}" HOME="${home}" UV_CACHE_DIR="${home}/.cache/uv")
for v in LANG LC_ALL; do
    [[ -z ${!v:-} ]] || clean+=("${v}=${!v}")
done
while IFS= read -r v; do
    [[ ${v} != AGMSG_* ]] || clean+=("${v}=${!v}")
done < <(compgen -e)
root="$("${clean[@]}" git -C "$(dirname -- "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"

read -ra tokens <<< "${line}"
for t in "${tokens[@]:2}"; do
    [[ ${t} == *=* ]] || {
        echo "dispatch: ${t} is not a <key>=<value> token" >&2
        exit 2
    }
done
# @description Print the value of the first `<key>=` token, or fail.
# @arg $1 string Key.
value_of() {
    local t
    for t in "${tokens[@]}"; do
        [[ ${t} == "$1="* ]] && printf '%s' "${t#*=}" && return 0
    done
    return 1
}
# @description Print how many tokens carry `<key>=`.
# @arg $1 string Key.
count_of() {
    local t n=0
    for t in "${tokens[@]}"; do
        [[ ${t} == "$1="* ]] && n=$((n + 1))
    done
    printf '%s' "${n}"
}
# Thread 4254893065: every message names exactly one task, before any hash or record work.
if (($(count_of task_id) != 1)) || [[ -z "$(value_of task_id)" ]]; then
    echo "dispatch: the line needs exactly one non-empty task_id=" >&2
    exit 1
fi
# Thread 4254163604: a TASK whose file is not hash-bound is never sent. The kind is the parsed
# first token, so a tab after it does not skip this check (thread 4260535901).
if [[ ${tokens[0]} == AGMSG-TASK ]]; then
    for field in task_file task_sha256; do
        value_of "${field}" > /dev/null || {
            echo "dispatch: an AGMSG-TASK line needs ${field}=" >&2
            exit 1
        }
    done
fi
for t in "${tokens[@]}"; do
    # Thread 4254771302: any name before _sha256=, digits included (a02_expected_sha256=).
    [[ ${t} =~ ^([^=]+)_sha256=(.*)$ ]] || continue
    name=${BASH_REMATCH[1]} want=${BASH_REMATCH[2]}
    field="${name}_sha256"
    [[ ${want} =~ ^[0-9a-f]{64}$ ]] || {
        echo "dispatch: ${field} is not 64 lowercase hex digits" >&2
        exit 1
    }
    # Thread 4256541725: a previous_<name>_sha256= reference names no file here (a02 item 4's grammar row).
    if [[ ${name} == previous_* ]]; then
        continue
    fi
    # Thread 4254494989: a repeated key leaves a second, unhashed value in the line.
    for key in "${field}" "${name}_file" "${name}"; do
        (($(count_of "${key}") <= 1)) || {
            echo "dispatch: ${field}: ${key}= appears more than once" >&2
            exit 1
        }
    done
    if value_of "${name}_file" > /dev/null && value_of "${name}" > /dev/null; then
        echo "dispatch: ${field}: both ${name}_file= and ${name}= name a file" >&2
        exit 1
    fi
    path="$(value_of "${name}_file" || value_of "${name}")" || {
        echo "dispatch: ${field} has no ${name}_file= or ${name}= field naming its file" >&2
        exit 1
    }
    [[ ${path} == /* ]] || path="${root}/${path}"
    [[ -f ${path} ]] || {
        echo "dispatch: ${field}: ${path} does not exist" >&2
        exit 1
    }
    got="$(shasum -a 256 "${path}")" && got=${got%% *}
    [[ ${got} == "${want}" ]] || {
        echo "dispatch: ${field} mismatch: the line has ${want}, ${path} hashes to ${got}" >&2
        exit 1
    }
done
if [[ ${tokens[0]} == AGMSG-TASK ]]; then
    tf="$(value_of task_file)" && [[ ${tf} == /* ]] || tf="${root}/${tf}"
    # Offline only: PyYAML comes from the pinned cache the validator recipes warm, and a cold cache stops the send,
    # never a fetch. --no-project: a pyproject.toml in the caller's directory is never discovered, synced or built.
    # The interpreter is named, python3 as mise answers it under env -i at the root, else python3 on PATH, and uv
    # runs under env -i with an allowlist, so no VIRTUAL_ENV, CONDA_PREFIX, UV_* or PYTHON* variable reaches it
    # (local:9df6b0c:1, C-57, the Bot's P1 4300102967).
    py="$(cd -- "${root}" && { env -i PATH="${PATH}" HOME="${home}" mise which python3 2> /dev/null || command -v python3; })" || py=
    [[ ${py} == /* ]] || {
        echo "dispatch: no python3 interpreter to pin for uv" >&2
        exit 1
    }
    uvy=(uv run --no-config --no-project --offline --python "${py}" --with pyyaml)
    here="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
    # Run from the trusted root, so a caller's .python-version or virtual environment picks no interpreter (4299651928).
    uvr() { (cd -- "${root}" && "${clean[@]}" "${uvy[@]}" "$@"); }
    uvr python -I -c 'import yaml' > /dev/null 2>&1 || {
        echo "dispatch: PyYAML is not in the uv cache ${home}/.cache/uv; run make validate-agent-assets to warm it" >&2
        exit 2
    }
    read -r -d '' brief << 'PY' || true
import sys, yaml
def unique(loader, node, deep=False):
    keys = [loader.construct_object(k, deep=deep) for k, _ in node.value]
    if len(keys) != len(set(keys)):
        raise yaml.YAMLError("duplicate key")
    return loader.construct_mapping(node, deep)
class Loader(yaml.SafeLoader):
    pass
Loader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique)

 succeeded in 343ms:
## 5.14 信頼ホスト実行契約（trusted-host execution contract、D-024-18）

orchestrator 側の仕組み（merge gate、integrate-merge、orch-gate、dispositions、audit-pool、verdict、chain）は、同じホスト上で同じ UID の worker プロセスと共存する。2026-10-19 の C-80 審査（a05、dispositions-a02、audit-pool-a01 の 3 文、計 19 件の P1）は、どの文も同じ前提を書かず同じ穴を持つことを示した。以後、`security: true` の orchestrator 側タスク文は本節を参照で適用し、本節の各項目に対応する threat 行を持つ。文ごとに言い換えない。

1. **書き込み境界（前提 6、ランタイム別に正直に）** Claude worker 席は専用の設定ディレクトリ `CLAUDE_CONFIG_DIR=~/.claude-worker`（chezmoi が描画、operator が一度 login）で起動し、orchestrator の `~/.claude` と設定を共有しない。worker 設定：除外コマンド無し、Herdr socket 無し、sandbox の allowWrite は自席 worktree と agmsg store と席別キャッシュだけ、`failIfUnavailable: true`、信頼パス（anchored checkout の `.claude/worktrees/` 以外、`~/.agents`、`~/.claude*`、`~/.local`、`~/.config`）への Edit deny（公式文書：file tool の permission 検査は要求パスと symlink 解決後のパスの両方に deny を適用し、symlink そのものへの書き込みは拒否する）、sandbox の強制範囲はユーザー設定ではなく **managed settings**（`/Library/Application Support/ClaudeCode/managed-settings.json`、公式文書 "Repository settings under an admin-required sandbox"：project/local 設定は sandbox を無効化したり除外・socket を足したりできない）に置く。chezmoi は user ではこのファイルを書けないので、描画した内容を操作者が `sudo` で一度配置する（操作者手順）。worker 設定は worktree 自身の `.claude/**` と `.mcp.json` への Edit deny（`//<anchored>/.claude/worktrees/*/.claude/**`）を持つ（Bash 側は sandbox 既定の settings/hooks の denyWithinAllow）。agmsg store（全席が書く）から配送 hook が driver や plugin を source する上流の経路（storage.sh の `drivers.partition` traversal、`db/trusted-plugins` と `plugins/partition/shared.sh` による差し替え承認）は別タスク（agmsg hardening）の行で、worker 設定は `~/.agents/skills/agmsg/plugins/**` と `~/.agents/skills/agmsg/db/trusted-plugins` への書き込みを deny し（Edit deny は sandbox の deny にも合流する）、hook 側は store 由来の設定値を検証するまで残余と書く。managed settings の配置先は OS で異なる（macOS `/Library/Application Support/ClaudeCode/managed-settings.json`、Linux `/etc/claude-code/managed-settings.json`）。hook は agmsg 配送だけを、hook コマンドを `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<home> …` で始めて（`BASH_ENV` などの継承環境を bash 起動前に消す；PATH 固定だけでは BASH_ENV が先に走る）絶対パスのインタプリタで呼び（上流の agmsg スクリプトは `/usr/bin/env bash` の shebang を持つので、hook 実行環境の PATH が shim を含まないことで束縛する）、各 hook に `onFailure: "block"`。公式文書：linked worktree の session は **main checkout の `.claude/settings.local.json` を読む**ので、worker 向けの hook を worktree の settings.local.json に書いても読まれず、逆に orchestrator の local hooks が worker session でも走る。したがって orchestrator 側の local hooks も guard 経由にし、worker 側の hook は worker config dir の settings に置く。Edit deny の一覧は `git ls-tree` ではなく描画時の静的一覧（manifest に列挙、`.agents/worklog/**` と `.agents/worklog/uv-cache/**` を含む）とし、`~/.agents/**` の全面 deny は agmsg store の書き込みと矛盾するので、`~/.agents/agent-config.yaml`、`~/.agents/skills/**/scripts/**`、`~/.agents/model-profiles.env` などストア以外を列挙する。公式文書で確認した事実（2026-10-19）：`Edit(path)` の deny は Write/MultiEdit/NotebookEdit にも効き、deny → ask → allow の順で最初の一致が決まる；ただし Read/Edit の deny は **Bash sandbox の設定にも合流する**（"Paths and domains from both sandbox settings and permission rules are merged into the final sandbox configuration"）ので、ユーザー設定（全席共有）に `.orchestration/**` の Edit deny を書くと orchestrator の Bash による記録書き込みも止まる。hook は起動時に固定されず、設定ファイルの編集は file watcher が即座に反映する。`sandbox.failIfUnavailable` の既定は fail-open（依存が無ければ sandbox 無しで実行）。したがって Claude 席の境界は Edit deny 規則ではなく、**ユーザーレベルの PreToolUse hook**（`~/.claude/hooks/worker-write-boundary`、chezmoi が描画、`/bin/sh` または絶対パスの `python3 -I`）で作る：cwd の realpath が `<anchored>/.claude/worktrees/` 配下の session では、Write/Edit/MultiEdit/NotebookEdit の対象が cwd の外、または `<cwd>/.claude/**`・`<cwd>/.mcp.json` のとき `permissionDecision: deny` を返す。Bash 側は sandbox の既定 `denyWithinAllow`（settings、hooks）と `allowWrite`（自席 worktree）が担う。`failIfUnavailable: true` を全席に置く。 Codex 席は sandbox（workspace-write）がツールの書き込み全部を自席の worktree と列挙パスに限る。Claude 席は Seatbelt sandbox が Bash を限るだけで、Write/Edit/MultiEdit/NotebookEdit、hook、MCP プロセスは sandbox 外で動き、permission policy（permgate の決定論ポリシー）が path で拒否しない限り anchored checkout や `~/.agents` にも書ける（2026-10-19 時点、描画済み設定にその deny は無い）。したがって前提 6 は「Codex 席は成立、Claude 席は P1-15 が描画設定に Edit の path deny を入れるまで残余」と書く。P1-15 以前に「worker は信頼ルートに書けない」と書く文は誤りで、C-80 が拒否する。P1-15 が入るまで、承認の出所は項目 8 の「コミット済み台帳」で守る。書き込みは自席の worktree（`.claude/worktrees/<name>`）、scratch、列挙されたツールキャッシュに限る。anchored checkout（`.claude/worktrees/` 以外）、`~/.agents/agent-config.yaml`、`~/.claude/hooks`、信頼ルートのバイナリ、orchestrator の証跡・スナップショット・lock は worker から書けない。render テストが描画後の deny を検証する。残余は「どの席 sandbox にも属さない同一 UID プロセス」と、Worker Playbook step 4 が sandbox 外に出す少数のコマンド（gh）。後者は D-024-17（P1-15）で絶対パスの実行体に束縛する。
2. **無害化した環境を最初に** 最初の処理として `env -i` に入り、PATH は信頼ルートで解決した絶対バイナリへのリンクだけの私設ディレクトリ（shims、空、相対は拒否）。git は毎回 `GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null -c core.hooksPath=/dev/null -c core.fsmonitor=false -c protocol.allow=never -c protocol.https.allow=always` と明示 `-C`（https だけ許す。`protocol.allow=never` 単独は必要な fetch を止める）。 検査の読み取りは `GIT_NO_LAZY_FETCH=1` で部分クローンの遅延 fetch（checkout 設定の credential.helper を起動しうる）を止め、`-c submodule.recurse=false --ignore-submodules=all` で submodule 内の status/diff（submodule 自身の設定が filter を有効化しうる）を止める。`.gitmodules` を持つ checkout は検査対象として拒否する。 `-C` は作業木を束縛しないので（repo-local の `core.worktree` が読み先を checkout 外へ向けられる）、git は `--git-dir=<checkout>/.git --work-tree=<checkout>` を明示し、`git rev-parse --show-toplevel` の realpath が checkout と一致しないときは拒否する。 premise や検査の「コマンド実行」は、固定語彙の読み取り専用プローブ（`git rev-parse <ref>`、`test -e <path>`、`grep -c <pattern> <file>` のように検査器自身が解釈する形）だけを許し、任意のシェル文字列は実行しない（本文のハッシュはコマンド文を認証するだけで、`python -I scripts/x.py` のファイル被演算子や `source ./x.sh` の中身は認証しない）。diff と show は `--no-ext-diff --no-textconv` と `-c core.attributesFile=/dev/null -c core.sshCommand=false` を付け、PR 側の `.gitattributes`（external diff、textconv、filter）が検査内容や実行物を変えないようにする。Python は `-I`。PATH 探索で実行するものは無い。 A shell script that runs under a PR-controlled or worker-controlled environment (verdict.sh, the chain glue, CI steps) is executed as a program with `#!/bin/bash -p`, never as `bash <file>`: privileged mode discards inherited functions, `BASH_ENV`/`ENV`, `SHELLOPTS`, `BASHOPTS`, `CDPATH` and `GLOBIGNORE` before the first statement, and the first statement re-executes the program under `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 /bin/bash --noprofile --norc -p "$0" "$@"` (long options before `-p`: bash exits 2 otherwise) unless its environment already consists of exactly the allowed names, checked through absolute paths (`/usr/bin/env`, `/usr/bin/grep`) under `-p`; a caller-set sentinel variable is not a sanitization proof, because the caller controls it (a04 C-80 round 1, 2026-10-19); sanitization performed by later statements (unset -f, compgen, PATH edits) is not a boundary, because the statements themselves resolve through the untrusted names (PR #410 security reviews 513e5d0 and 6b7e783, 2026-10-19). No script accepts a caller-supplied executable directory; interpreters are the fixed absolute paths item 9 names.
3. **信頼パスの境界検査** 仕組みが信頼するパス（スクリプト、台帳、証跡、worktree、lock、出力先）は realpath で解決し、`.claude/worktrees/` または manifest の worker ルート配下なら拒否（ask/hold）。symlink 構成要素は解決後に比較し、大小文字を区別しないファイルシステムでは同一性比較を大小文字非依存で行う。
4. **検証したものを実行し、検証した内容を渡す** 検証した実行体はその realpath で実行する（再探索しない）。検証したファイル内容は信頼ルート配下のスナップショット（0600、一意名）として渡し、使用直前に sha256 を再照合する。判断に読んだ証跡は sha256 を出力に記録する。
5. **出力と予約の同一性** 名前には 40 桁の head を使う（7 桁で衝突させない）。lock は信頼ルート配下の固定 inode に O_EXCL で作り、置換を inode 比較で検出する。物理スロット 1 つに lock 1 つ。
6. **正直な残余** 境界だけが緩和するリスクを `closed` と書かない。各文は残余を 1 行で明記する。
0. **脅威モデル（D-024-21）** 席は同じ OS ユーザで動き、ホストは席間の信頼境界ではない（同一 UID のプロセスは symlink 差し替え、共有 `.git` の object 差し替え、hook の子プロセス、Herdr socket 経由の host 実行で、ホスト内のどの検査も迂回できる）。regime の硬い境界は GitHub（保護された main、必須チェック、orchestrator の identity によるマージ）。ただしこの境界は **worker 席が orchestrator の GitHub 資格情報を共有しない**ときだけ成立する（D-024-22：worker 席は専用の GitHub identity（別アカウントまたは App のトークン）で `gh` に login し、ruleset の bypass 一覧に入らない。orchestrator の keychain トークンを worker の config dir に持ち込まない。identity が分かれるまで「GitHub が境界」は未成立と書く）。**同一 macOS ユーザでは資格情報は分離できない**（gh は keychain の項目を host/user で引き、同じ UID の gh は orchestrator のトークンを読める。`GH_CONFIG_DIR` は設定を分けるだけ）。防止には worker 席を別の OS ユーザ（または別ホスト）で動かすしかなく、それは D-024-23 の将来項目（P1-16、操作者の判断）。それまで GitHub 境界は **検知**で守る：記録は boundary の記録 PR まで main に無いので、検知は次の記録 PR の regime ジョブで行う（`.orchestration/acceptance/**` に触れる PR で、前回 boundary 以降の main の各マージ commit に、gate 通過の証跡を持つ受け入れ記録が対応することを検査し、無ければその PR を失敗させる；P1-11 owner a02 の行 `ci:detection:1`）。main push 時点の検知は記録が無いので不可能であり、文は「次の記録 PR で検知、防止ではない」と書く。悪意ある worker に耐えるべき入力（承認台帳、gate が読む証跡 of record）は GitHub から sha 指定で API 経由（sandbox 内）に読み、ローカルファイルやローカル object database からは読まない。ホスト内の制御（本節 1〜10）は事故と prompt injection による損害の抑制であり、文はそう書く。
8. **承認はコミット済み台帳から読む** permission の決定行（`scope=permission approved_by=user diff_sha256=…`）は anchored checkout の作業コピーではなく、コミット済みの台帳から読む。読み方は `git ls-remote origin refs/heads/main` が返す commit sha を取り、GitHub API（`gh api repos/<owner>/<repo>/contents/.orchestration/decisions.tsv?ref=<sha>`、sandbox 内）でその sha の内容を取得する。ローカルの `git show` は共有 object database が書けるため中間 tree の差し替えで偽物を返しうる（第 3 回審査の所見 2）（ローカルの ref 名 `origin/main` は経由しない。`refs/replace/` も書けるので replacement を無効にする。Codex worker は `.git/objects` と `.git/refs` に書けるので ref は差し替えられるが、sha で指した object は内容アドレスで偽造できない）。作業コピーの行は提案で、記録 PR が main にマージされて初めて承認になる（PR の承認は操作者の操作）。偽造には main へのマージが要る。 The same applies to the PR content a mechanism evaluates (the verdict, the audit precheck, the counters): the changeset is read from GitHub at the 40-hex head (`gh api repos/{owner}/{repo}/compare/<base40>...<head40>`, `…/contents/<path>?ref=<head40>`) or from a private clone whose object store no worker can write; the main checkout's shared `.git/objects` and its `origin/main` ref are not evidence sources, because Codex workers write them (a04 C-80 round 1, 2026-10-19). Evidence files are named and matched by the full 40-hex head, never by a 7-character prefix.
9. **私設キャッシュ** orchestrator 側の実行は worker と共有するキャッシュ（`~/.cache/uv`、`~/.local/share/uv`、mise）から実行可能物を読まない。`UV_CACHE_DIR` を anchored checkout 配下（`.agents/worklog/uv-cache`、gitignored、worker 書き込み不可）に固定し、`uv run --no-config --no-project --offline --python <信頼ルートの絶対パスのインタプリタ>` で起動する（`--no-config` で uv の設定探索を止め、`--python` の絶対パスで cwd や親の `.venv` の発見を止める；敵対的な `.venv` と `uv.toml` を置いた fixture で検証）。hook は uv を使わず jq と python 標準ライブラリだけで動く。 One trusted interpreter resolver (`scripts/orchestrator/trusted-interpreter.sh`, P1-3 lineage) resolves `<abs>` from the repository's pinned declaration to a regular file under the tool manager's install root, refuses anything else, and every orchestrator-side script consumes it; no script keeps its own `command -v`, `mise which` or PATH fallback (ci-rerun.sh security review 44cb835, 2026-10-19). Shell code of other projects (the agmsg storage layer and its `drivers.partition` sourcing) is never sourced by an orchestrator-side mechanism; counters are read from the agmsg SQLite store read-only with a fixed query or from the pasted record.
10. **worker は sandbox 外でコマンドを実行しない（D-024-17 の改訂）** 2026-10-19T03:45Z の実測で `gh api` は Claude sandbox の中から成功した（sandbox の proxy は CONNECT 型で TLS を終端しない；keychain のトークンも読めた）。worker 席の除外コマンドは空にし、gh も git push も sandbox 内の proxy 経由で実行する。Codex 席は `sandbox_workspace_write.network_access = true` で同じ状態にし、permgate の codex ポリシーは sandbox 外への escape を承認しない（permgate の変更は操作者の手順）。wrapper 方式（絶対パス、env -i、固定 GH_CONFIG_DIR）は LD_PRELOAD と引数転送（`gh repo clone -- --config`）を閉じられないので採らない。
7. **検証** threat_table は本節の項目 1〜10 に 1 行ずつ対応させる（参照だけでは足りない）。共通テスト補助 `tests/unit/trusted_exec_contract.py`（P1-6 で作る）を使い、仕組みごとに 4 つの red→green テストを持つ：PATH 先頭の shim が実行されない、植え付けた GIT_* と git 設定が効かない、worker ルート配下の信頼パスが拒否される、検証後に差し替えたファイルが消費側に届かない。

 succeeded in 362ms:
11:  - scripts/orchestrator/trusted-interpreter.sh
12:  - tests/unit/test_trusted_interpreter.py
23:    disposition: "residual: reports, command output and review records are untrusted claims checked against the final diff and CI; predecessor evidence remains historical evidence"
24:  - control: scripts/orchestrator/trusted-interpreter.sh fixed declaration parser and trusted installation resolution
25:    disposition: "closed: tests/unit/test_trusted_interpreter.py::TrustedInterpreterTest::test_pinned_interpreter_ignores_checkout_path_without_mise"
26:  - control: tests/unit/test_trusted_interpreter.py isolated installation and hostile-input fixtures
27:    disposition: "residual: fixtures exercise the resolver contract without installing tools or modifying the operator's real installation; they cannot establish host directory protection"
35:    disposition: "residual: fixtures use fake GitHub executables and temporary ledgers; production retains the existing reservation, ledger append and gh run rerun --failed effect, which is not exercised against GitHub during unit tests"
37:    disposition: "residual: workflow files do not change; the exact Python declaration is a read-only trusted input, never caller-selected; the currently available repository has no exact Python pin, so dispatch remains held until that prerequisite is resolved"
39:    disposition: "residual: scripts/orchestrator/trusted-interpreter.sh is the one new executable script; no other new or renamed script is authorized"
41:    disposition: "residual: only the orchestrator merges PR #424 after the integration gate, using gh pr merge --squash --match-head-commit with the audited head; local controls do not prevent a same-UID credential holder from bypassing this procedure"
50:  - control: design 5.14 item 3 trusted path boundaries
51:    disposition: "closed: tests/unit/test_trusted_interpreter.py::TrustedInterpreterTest::test_interpreter_in_worktree_cache_or_tmp_is_refused"
52:  - control: design 5.14 item 4 execute the verified realpath
53:    disposition: "residual: both Python invocation sites consume the resolver's absolute realpath without rediscovery or a temporary Python link; this does not prevent replacement by an unrestricted same-UID process or establish snapshot controls for unrelated evidence consumers"
59:    disposition: "residual: this task adds resolver and consumer regressions and retains the lineage tests; it does not claim that these replace the common trusted-execution helper or complete the four-test contract for every orchestrator mechanism"
61:    disposition: "residual: the resolver makes no permission decision and consumes no approval ledger; integration evidence provenance remains the orchestrator's responsibility, and local task copies or Git objects are not approval authority"
62:  - control: design 5.14 item 9 private cache and shared interpreter resolver
63:    disposition: "residual: this task introduces the common resolver and migrates the rerun consumer, using the protected anchored uv cache and offline execution; migration of other consumers is not authorized by allowed_files and must not be reported complete"
65:    disposition: "residual: every worker gh command and git write runs individually inside the sandbox; an unavailable operation produces a blocked PONG rather than an outside-sandbox retry"
71:# AGMSG-TASK dotfiles-T133-ci-efficiency-followup-a04 — replace the interpreter-selection class with one trusted resolver
75:[memory:failure] The predecessor reached the C-61 round cap with its worker-side fix round and revise 1, and INV-6 S2 with two amendment dispatches. Its rebase repair and update-branches do not erase those counts. The security review of `44cb8353` found the owned `interpreter-selection` class again: `command -v python3` accepts an activated checkout’s absolute `.venv/bin/python3`, which then executes through uv and directly with operator authority.
83:The inspected repository does **not** contain `.mise.toml`, `.tool-versions` or `.python-version`. Its root `mise.toml` contains only `[tools]`; its actual managed declaration, `home/dot_mise/config.toml`, says `python = "latest"`, which is not an exact pin. Do not describe any of these as an existing pinned Python declaration.
85:Before dispatch, the orchestrator must resolve that missing prerequisite through an authorized change and bind this text to the actual trusted declaration and its exact grammar. No declaration file is writable under this task’s `allowed_files`; the worker must not add a pin, select the newest installation, or substitute an installed version. Until resolved, this task is held.
95:Item 2: “A shell script that runs under a PR-controlled or worker-controlled environment (verdict.sh, the chain glue, CI steps) is executed as a program with `#!/bin/bash -p`, never as `bash <file>`: privileged mode discards inherited functions, `BASH_ENV`/`ENV`, `SHELLOPTS`, `BASHOPTS`, `CDPATH` and `GLOBIGNORE` before the first statement, and the first statement re-executes the program under `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 /bin/bash --noprofile --norc -p "$0" "$@"` (long options before `-p`: bash exits 2 otherwise) unless its environment already consists of exactly the allowed names, checked through absolute paths (`/usr/bin/env`, `/usr/bin/grep`) under `-p`; a caller-set sentinel variable is not a sanitization proof, because the caller controls it (a04 C-80 round 1, 2026-10-19); sanitization performed by later statements (unset -f, compgen, PATH edits) is not a boundary, because the statements themselves resolve through the untrusted names (PR #410 security reviews 513e5d0 and 6b7e783, 2026-10-19).” “No script accepts a caller-supplied executable directory; interpreters are the fixed absolute paths item 9 names.” “Python は `-I`。” “PATH 探索で実行するものは無い。”
97:Item 4: “検証した実行体はその realpath で実行する（再探索しない）。” “検証したファイル内容は信頼ルート配下のスナップショット（0600、一意名）として渡し、使用直前に sha256 を再照合する。” “判断に読んだ証跡は sha256 を出力に記録する。”
99:Item 9: “orchestrator 側の実行は worker と共有するキャッシュ（`~/.cache/uv`、`~/.local/share/uv`、mise）から実行可能物を読まない。” “`UV_CACHE_DIR` を anchored checkout 配下（`.agents/worklog/uv-cache`、gitignored、worker 書き込み不可）に固定し、`uv run --no-config --no-project --offline --python <信頼ルートの絶対パスのインタプリタ>` で起動する（`--no-config` で uv の設定探索を止め、`--python` の絶対パスで cwd や親の `.venv` の発見を止める；敵対的な `.venv` と `uv.toml` を置いた fixture で検証）。” “One trusted interpreter resolver (`scripts/orchestrator/trusted-interpreter.sh`, P1-3 lineage) resolves `<abs>` from the repository's pinned declaration to a regular file under the tool manager's install root, refuses anything else, and every orchestrator-side script consumes it; no script keeps its own `command -v`, `mise which` or PATH fallback (ci-rerun.sh security review 44cb835, 2026-10-19).”
101:## Item 1 — one trusted interpreter resolver
103:Add executable `scripts/orchestrator/trusted-interpreter.sh`, with English shdoc comments and `#!/bin/bash -p`. Execute it as a program; do not source it or invoke it as `bash <file>`. Its first statement implements the quoted environment check and re-exec, before assignments, traps, tool discovery or declaration reads. Check the actual environment through absolute paths; a caller-provided sentinel is not proof. The clean invocation must terminate normally rather than repeatedly re-execing because Bash maintains its own environment entries.
105:Read only the repository’s exact Python declaration established by the dispatch prerequisite, anchored to the trusted script/repository location rather than the caller’s cwd. Parse its fixed grammar as data with trusted absolute tools, without `source`, `eval`, shell interpolation of declaration content, or an interpreter selected from that content. Refuse missing, duplicate, malformed, non-exact or metacharacter-bearing declarations; `latest` is invalid.
107:Derive the installation root from HOME as `$HOME/.local/share/mise/installs` and construct only `<install root>/python/<version>/bin/python3`. Resolve and validate the candidate before printing it. Require an executable regular file after `realpath`, within the expected protected installation, outside the worktree, manifest worker roots, worker-writable caches and `$TMPDIR`. Check resolved path boundaries, including filesystem case behavior where applicable. Refuse a symlinked installation rather than accepting a redirected install directory.
109:On success print exactly one absolute interpreter realpath and exit 0. On every refusal print a named `trusted-interpreter:` diagnostic to stderr, print no interpreter on stdout, and exit 2. There is no `command -v`, `mise which`, PATH search, version-alias selection, download or fallback. Do not execute a candidate to discover whether it is trustworthy.
111:This is the common resolver required by item 9. This PR migrates its first consumer only; it does not authorize edits to other orchestrator scripts.
113:## Item 2 — consume the resolver in ci-rerun.sh
115:Apply the same privileged program-entry and first-statement environment contract to `scripts/orchestrator/ci-rerun.sh`. Invoke the resolver by its bound absolute path and consume its single validated result; propagate refusal without trying another interpreter.
117:Remove Python from the old tool-discovery loop, including the line-45 fallback and line-47 shims test. Do not retain or recreate those mechanisms elsewhere. Bind non-Python tools from explicit protected installation locations, using their validated realpaths or a private fixed PATH of links to those realpaths; caller PATH entries never populate that directory. Missing trusted tools fail closed.
121:Run the YAML-loading Python only through `uv run --no-config --no-project --offline --python "<abs>"`, retaining `--with pyyaml`, with `python -I` as the command. Run the reservation Python directly as `"<abs>" -I …`. Both use the resolver’s realpath, never a Python link in a temporary directory, another lookup, or an inherited virtual environment.
123:Set `UV_CACHE_DIR` to the protected anchored checkout’s `.agents/worklog/uv-cache`, not a caller-supplied location or the worker’s shared HOME cache. Preserve isolation from inherited `UV_*`, `VIRTUAL_ENV` and `PYTHON*` inputs. A fixture containing hostile `.venv`, `.python-version` and `uv.toml` must not change the executable or configuration consumed.
131:Write the failing regressions before the fix and paste red and green output. Add `tests/unit/test_trusted_interpreter.py` with class `TrustedInterpreterTest` and these tests:
133:- `test_pinned_interpreter_ignores_checkout_path_without_mise`: prepend a checkout’s marker-writing `.venv/bin/python3` to PATH with mise unavailable; the resolver prints only the valid pinned installation’s realpath, or refuses when no valid installation exists, and the marker remains absent.
135:- `test_symlinked_install_is_refused`: redirect the installation through a symlink; refusal occurs before any candidate executes.
141:Extend `tests/unit/test_ci_rerun.py::CiRerunTest::test_ci_rerun_pins_its_interpreter_against_a_checkout_and_the_environment`, currently at line 273, with the marker-writing **`python3`** in `.venv/bin` **prepended to PATH**, with mise unavailable. Assert the marker is absent and that a valid trusted fixture installation still permits exactly one rerun. Also cover safe refusal when that installation is absent.
143:Retain and adapt `test_ci_rerun_starts_the_pinned_interpreter_by_its_own_path` and `test_ci_rerun_never_runs_a_path_resolved_command_before_the_pin`; their assertions must exercise the new trusted-path contract rather than preserve acceptance of arbitrary PATH wrappers or the removed shims mechanism. Add `test_ci_rerun_executes_as_a_sanitized_program` for hostile startup state and the forged-sentinel case.
145:Fixtures copy the resolver beside the consumer, supply an exact declaration and protected-installation layout, and execute both scripts as programs. Adapt fake-gh fixture data delivery to the clean environment; do not add production environment exemptions, executable-directory parameters or test-only resolver bypasses. Keep every existing behavioral assertion and keep all fixture calls off live GitHub.
151:Source budget: the retained a02 source delta is `31 + 5 = 36` changed lines, plus about `60` for the resolver and `60` for consumer integration, giving `156`, with `24` lines of allowance and a resulting cap of **180 changed lines outside `tests/` and `.orchestration/`**.
153:Test budget: the retained a02 test delta is `67 + 1 = 68` changed lines, plus about `80` for resolver tests and `80` for consumer regressions and fixture migration, giving `228`, with `22` lines of allowance and a resulting cap of **250 changed lines under `tests/`**.
159:Retain the predecessor’s checks: `make unit-test`, `make format`, ShellCheck and repository-style `shfmt -i 4 -sr -d` on the changed shell scripts, and the workflow-orchestration, workflow-security and ci-rerun unit modules. Add the trusted-interpreter module, the new startup and hostile-PATH cases, and the changed-file comparison lint. Do not run bats locally.
163:After pushing, paste `gh run list --branch tools/ci-efficiency-followup-a02 --json name,event,conclusion` and final-head required-check evidence, showing the seven required contexts and no pull-request private-bootstrap run.

**Evaluating symlink handling and PR merge checks**
**Analyzing environment and repository trust issues**

I’m examining how trusted entry points, environment variables like LD_PRELOAD, and repository identity affect script security and merge commands, especially focusing on bootstrap trust and process startup nuances on Linux.
exec
/bin/zsh -lc "sed -n '94,145p' .orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md" in ~/Workspace/dotfiles
 succeeded in 0ms:

Item 2: “A shell script that runs under a PR-controlled or worker-controlled environment (verdict.sh, the chain glue, CI steps) is executed as a program with `#!/bin/bash -p`, never as `bash <file>`: privileged mode discards inherited functions, `BASH_ENV`/`ENV`, `SHELLOPTS`, `BASHOPTS`, `CDPATH` and `GLOBIGNORE` before the first statement, and the first statement re-executes the program under `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 /bin/bash --noprofile --norc -p "$0" "$@"` (long options before `-p`: bash exits 2 otherwise) unless its environment already consists of exactly the allowed names, checked through absolute paths (`/usr/bin/env`, `/usr/bin/grep`) under `-p`; a caller-set sentinel variable is not a sanitization proof, because the caller controls it (a04 C-80 round 1, 2026-10-19); sanitization performed by later statements (unset -f, compgen, PATH edits) is not a boundary, because the statements themselves resolve through the untrusted names (PR #410 security reviews 513e5d0 and 6b7e783, 2026-10-19).” “No script accepts a caller-supplied executable directory; interpreters are the fixed absolute paths item 9 names.” “Python は `-I`。” “PATH 探索で実行するものは無い。”

Item 4: “検証した実行体はその realpath で実行する（再探索しない）。” “検証したファイル内容は信頼ルート配下のスナップショット（0600、一意名）として渡し、使用直前に sha256 を再照合する。” “判断に読んだ証跡は sha256 を出力に記録する。”

Item 9: “orchestrator 側の実行は worker と共有するキャッシュ（`~/.cache/uv`、`~/.local/share/uv`、mise）から実行可能物を読まない。” “`UV_CACHE_DIR` を anchored checkout 配下（`.agents/worklog/uv-cache`、gitignored、worker 書き込み不可）に固定し、`uv run --no-config --no-project --offline --python <信頼ルートの絶対パスのインタプリタ>` で起動する（`--no-config` で uv の設定探索を止め、`--python` の絶対パスで cwd や親の `.venv` の発見を止める；敵対的な `.venv` と `uv.toml` を置いた fixture で検証）。” “One trusted interpreter resolver (`scripts/orchestrator/trusted-interpreter.sh`, P1-3 lineage) resolves `<abs>` from the repository's pinned declaration to a regular file under the tool manager's install root, refuses anything else, and every orchestrator-side script consumes it; no script keeps its own `command -v`, `mise which` or PATH fallback (ci-rerun.sh security review 44cb835, 2026-10-19).”

## Item 1 — one trusted interpreter resolver

Add executable `scripts/orchestrator/trusted-interpreter.sh`, with English shdoc comments and `#!/bin/bash -p`. Execute it as a program; do not source it or invoke it as `bash <file>`. Its first statement implements the quoted environment check and re-exec, before assignments, traps, tool discovery or declaration reads. Check the actual environment through absolute paths; a caller-provided sentinel is not proof. The clean invocation must terminate normally rather than repeatedly re-execing because Bash maintains its own environment entries.

Read only the repository’s exact Python declaration established by the dispatch prerequisite, anchored to the trusted script/repository location rather than the caller’s cwd. Parse its fixed grammar as data with trusted absolute tools, without `source`, `eval`, shell interpolation of declaration content, or an interpreter selected from that content. Refuse missing, duplicate, malformed, non-exact or metacharacter-bearing declarations; `latest` is invalid.

Derive the installation root from HOME as `$HOME/.local/share/mise/installs` and construct only `<install root>/python/<version>/bin/python3`. Resolve and validate the candidate before printing it. Require an executable regular file after `realpath`, within the expected protected installation, outside the worktree, manifest worker roots, worker-writable caches and `$TMPDIR`. Check resolved path boundaries, including filesystem case behavior where applicable. Refuse a symlinked installation rather than accepting a redirected install directory.

On success print exactly one absolute interpreter realpath and exit 0. On every refusal print a named `trusted-interpreter:` diagnostic to stderr, print no interpreter on stdout, and exit 2. There is no `command -v`, `mise which`, PATH search, version-alias selection, download or fallback. Do not execute a candidate to discover whether it is trustworthy.

This is the common resolver required by item 9. This PR migrates its first consumer only; it does not authorize edits to other orchestrator scripts.

## Item 2 — consume the resolver in ci-rerun.sh

Apply the same privileged program-entry and first-statement environment contract to `scripts/orchestrator/ci-rerun.sh`. Invoke the resolver by its bound absolute path and consume its single validated result; propagate refusal without trying another interpreter.

Remove Python from the old tool-discovery loop, including the line-45 fallback and line-47 shims test. Do not retain or recreate those mechanisms elsewhere. Bind non-Python tools from explicit protected installation locations, using their validated realpaths or a private fixed PATH of links to those realpaths; caller PATH entries never populate that directory. Missing trusted tools fail closed.

Every external command, including cleanup on early failure, uses an absolute path or the fixed PATH established after re-exec. Keep the EXIT trap’s `/bin/rm` and cover both successful execution and refusal before tool setup completes. Apply the relevant section-5.14 Git invocation controls to the existing root-discovery probe; do not introduce new Git probes or arbitrary shell-command inputs.

Run the YAML-loading Python only through `uv run --no-config --no-project --offline --python "<abs>"`, retaining `--with pyyaml`, with `python -I` as the command. Run the reservation Python directly as `"<abs>" -I …`. Both use the resolver’s realpath, never a Python link in a temporary directory, another lookup, or an inherited virtual environment.

Set `UV_CACHE_DIR` to the protected anchored checkout’s `.agents/worklog/uv-cache`, not a caller-supplied location or the worker’s shared HOME cache. Preserve isolation from inherited `UV_*`, `VIRTUAL_ENV` and `PYTHON*` inputs. A fixture containing hostile `.venv`, `.python-version` and `uv.toml` must not change the executable or configuration consumed.

Read Makefile lines 185–200: its `--with pyyaml` probe explains why the cache is tried first. Preserve the working cached-PyYAML behavior, but the production helper now remains offline; remove its online retry. Missing offline dependencies fail visibly without rerunning a job. Do not edit the Makefile.

Retain the existing current-head checks, signature classification, per-run atomic reservation, ledger behavior, failure codes and no-double-rerun guarantees. Baseline changes remain limited to the predecessor’s D-024-24 authorization: normalise new comparisons; baseline only pre-existing comparisons moved by this PR.

## Item 3 — regressions and fixture migration

Write the failing regressions before the fix and paste red and green output. Add `tests/unit/test_trusted_interpreter.py` with class `TrustedInterpreterTest` and these tests:

- `test_pinned_interpreter_ignores_checkout_path_without_mise`: prepend a checkout’s marker-writing `.venv/bin/python3` to PATH with mise unavailable; the resolver prints only the valid pinned installation’s realpath, or refuses when no valid installation exists, and the marker remains absent.
- `test_missing_install_is_refused`: an exact declaration without its installation exits 2 with the named diagnostic and no stdout.
- `test_symlinked_install_is_refused`: redirect the installation through a symlink; refusal occurs before any candidate executes.
- `test_shell_metacharacter_in_declaration_is_refused`: a declaration containing a shell metacharacter exits 2 without executing it.
- `test_missing_or_nonexact_declaration_is_refused`: cover an absent declaration and `latest`, without selecting any installed version.
- `test_interpreter_in_worktree_cache_or_tmp_is_refused`: cover the forbidden roots and symlink escapes, with no marker written.
- `test_program_entry_discards_inherited_shell_state`: invoke the executable with hostile inherited shell state, PATH and a forged sanitization sentinel; nothing planted executes.

Extend `tests/unit/test_ci_rerun.py::CiRerunTest::test_ci_rerun_pins_its_interpreter_against_a_checkout_and_the_environment`, currently at line 273, with the marker-writing **`python3`** in `.venv/bin` **prepended to PATH**, with mise unavailable. Assert the marker is absent and that a valid trusted fixture installation still permits exactly one rerun. Also cover safe refusal when that installation is absent.

Retain and adapt `test_ci_rerun_starts_the_pinned_interpreter_by_its_own_path` and `test_ci_rerun_never_runs_a_path_resolved_command_before_the_pin`; their assertions must exercise the new trusted-path contract rather than preserve acceptance of arbitrary PATH wrappers or the removed shims mechanism. Add `test_ci_rerun_executes_as_a_sanitized_program` for hostile startup state and the forged-sentinel case.

Fixtures copy the resolver beside the consumer, supply an exact declaration and protected-installation layout, and execute both scripts as programs. Adapt fake-gh fixture data delivery to the clean environment; do not add production environment exemptions, executable-directory parameters or test-only resolver bypasses. Keep every existing behavioral assertion and keep all fixture calls off live GitHub.

exec
/bin/zsh -lc "nl -ba scripts/orchestrator/dispatch.sh | sed -n '250,340p'" in ~/Workspace/dotfiles
 succeeded in 0ms:
   250	import fcntl, json, os, re, shutil, sys, tempfile
   251	from pathlib import Path
   252	
   253	mode, path, line, sender, to, window, task = sys.argv[1:8]
   254	record = Path(path)
   255	rows = [r for r in sys.stdin.read().splitlines() if r]
   256	
   257	def refuse(pairs):
   258	    keys = [k for k, _ in pairs]
   259	    dup = next((k for k in keys if keys.count(k) > 1), None)
   260	    if dup is not None:
   261	        sys.exit(f"dispatch: {path}: duplicate key {dup}")
   262	    return dict(pairs)
   263	
   264	def constant(name):
   265	    sys.exit(f"dispatch: {path}: non-finite number {name}")
   266	
   267	def load():
   268	    # newline="": a CRLF record keeps its line endings (thread 4256987087).
   269	    with open(record, newline="") as f:
   270	        text = f.read()
   271	    block, rest = {}, text
   272	    if re.match(r"---\r?\n", text):
   273	        m = re.match(r"---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
   274	        if not m:
   275	            sys.exit(f"dispatch: {path}: the block between the first two --- lines is not closed")
   276	        try:
   277	            block = json.loads(m.group(1), object_pairs_hook=refuse, parse_constant=constant)
   278	        except json.JSONDecodeError as e:
   279	            sys.exit(f"dispatch: {path}: the block is not valid JSON: {e}")
   280	        rest = text[m.end():]
   281	        if not isinstance(block, dict):
   282	            sys.exit(f"dispatch: {path}: the block is not a JSON object")
   283	    if not isinstance(block.setdefault("dispatch", []), list):
   284	        sys.exit(f"dispatch: {path}: dispatch is not a list")
   285	    # Thread 4254844587: another task's record never takes this task's dispatch.
   286	    if "task" in block and block["task"] != task:
   287	        sys.exit(f"dispatch: {path} is the record of task {block['task']}, the line is task {task}")
   288	    return block, rest
   289	
   290	row = re.compile(r"^\s*(\S+)\s+\[([^\]]+)\]\s+(\S+)\s+→\s+(\S+):\s(.*)$")
   291	# (marker, [timestamp, sender, recipient, text]); the marker is left out of the alignment, a read flips it.
   292	seen = [(m.group(1), list(m.group(2, 3, 4, 5))) for m in map(row.match, rows) if m]
   293	if mode == "check":
   294	    load()
   295	    with open(window, "w") as f:
   296	        json.dump([fields for _, fields in seen], f)
   297	    sys.exit(0)
   298	with open(window) as f:
   299	    pre = json.load(f)
   300	post = [fields for _, fields in seen]
   301	n, m = len(pre), len(post)
   302	# Shift j: the post-send window without its j newest rows equals the pre-send one without its e = n + j - m oldest.
   303	fits = [m] if n == 0 else [j for j in range(m) if 0 <= n + j - m < n and post[: m - j] == pre[n + j - m :]]
   304	if len(fits) != 1:
   305	    sys.exit(
   306	        "dispatch: the post-send window does not align uniquely with the pre-send one; "
   307	        "the line may be on the bus unrecorded; raise BUS_READ_WINDOW or check the bus"
   308	    )
   309	if fits[0] == 0:
   310	    sys.exit(f"dispatch: this send added no bus row; {path} is unchanged")
   311	# Another seat's row may land after this send, so the send is the last new row equal to the line.
   312	marks = [mark for mark, (_, s, r, text) in seen[m - fits[0] :] if (s, r, text) == (sender, to, line)]
   313	if not marks:
   314	    sys.exit("dispatch: no new row equals the line; the line may be on the bus unrecorded; check the bus")
   315	# Thread 4255272797: the read-modify-write holds the record directory's lock, so a second dispatch waits.
   316	lock = os.open(record.parent, os.O_RDONLY)
   317	fcntl.flock(lock, fcntl.LOCK_EX)
   318	block, rest = load()
   319	block["dispatch"].append(f"{line} read_at={'read' if marks[-1] == '○' else 'unread'}")
   320	body = json.dumps(block, sort_keys=True, indent=2, ensure_ascii=False)
   321	# Thread 4254844595: the line is already sent, so the record is replaced whole or not at all.
   322	fd, tmp = tempfile.mkstemp(dir=record.parent, prefix=f".{record.name}.")
   323	try:
   324	    with os.fdopen(fd, "w", newline="") as f:
   325	        f.write(f"---\n{body}\n---\n{rest}")
   326	        f.flush()
   327	        os.fsync(f.fileno())
   328	    shutil.copymode(record, tmp)
   329	    os.replace(tmp, record)
   330	except BaseException:
   331	    Path(tmp).unlink(missing_ok=True)
   332	    raise
   333	PY
   334	[[ ${record} == /* ]] || record="${PWD}/${record}"
   335	# The local review of 0d199475 (C-32): a record mkstemp cannot replace would fail only after the send.
   336	if [[ ! -f ${record} || ! -w ${record} || ! -w "$(dirname -- "${record}")" ]]; then
   337	    echo "dispatch: the record ${record} cannot be written" >&2
   338	    exit 1
   339	fi
   340	limit=${BUS_READ_WINDOW:-200}

exec
/bin/zsh -lc "nl -ba .orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md | sed -n '125,166p'" in ~/Workspace/dotfiles
 succeeded in 0ms:
   125	
   126	Produce one schema-valid verdict from nine positively checked conditions without executing inherited shell startup code, accepting caller-selected executable directories, following output symlinks or treating invalid `security` metadata as an exemption.
   127	
   128	Retain the a03 gate-before-application behavior, complete feedback validation, amended-cap precedence, offline operation, finding counts and trusted-checkout refresh.
   129	
   130	## Files
   131	
   132	1. `scripts/orchestrator/verdict.sh <pr> [--apply] [--loop] [--shadow]` remains Bash with `set -Eeuo pipefail`, English shdoc documentation and `jq` for JSON. Its startup and executable selection follow the Reset design below. Each condition is `{id, ok, evidence}` and becomes true only through a positive check of parsed, validated input.
   133	
   134	   Inputs remain the PR view and checks, the acceptance record's JSON block and prose, the selected task or `--task <id>`, the audit JSON, a fresh feedback sweep, saved feedback dispositions, the task's allowed paths and caps, regime counters, the GitHub merge-base changeset and the head-specific security review. The acceptance block names the PR, task and current head and contains a ledger array. The PR is open, non-draft and based on `main`. Read `head.sha` and `base.sha` from `gh api repos/{owner}/{repo}/pulls/<pr>`, require both to be 40 lowercase hexadecimal characters, and bind all reads to those values. This task chooses GitHub API reads, not a local clone: read the changeset through `…/compare/<base40>...<head40>` and inspected PR bytes through `…/contents/<path>?ref=<head40>`. Repository identity is fixed from the trusted repository declaration, not caller environment or local Git configuration. Missing, incomplete, truncated or unreadable API data holds; no local-head fetch or shared-object fallback is allowed.
   135	
   136	   Condition 1 verifies that the GitHub contents response for `.orchestration/<task>/precheck.json?ref=<head40>` hashes to the record's `precheck:` value and names the head or an ancestor authenticated by GitHub compare data whose diff to the head contains only `.orchestration/<task>/` paths. The retained `PRECHECK_REQUIRED` setting is supplied explicitly as `--precheck-required 0|1`; absent or zero makes this condition's failure a warning. No environment exception is added for it.
   137	
   138	   Condition 2 requires every required check to be present with state `SUCCESS` for the head. Empty or unreadable checks hold. Every duplicate entry for a required name must also be `SUCCESS`.
   139	
   140	   Condition 3 requires an audit that validates against `.schemas/audit.json`, names the task and full head, has zero open P0/P1 findings, and has verdict `correct` or a non-empty set of remaining findings whose scopes are all `records`. A blocked audit holds. An incorrect audit without remaining findings fails this condition.
   141	
   142	   Condition 4 requires saved and fresh feedback documents to name the accepted head, complete feedback identity matching with multiplicity, and a valid disposition for every fresh item. Diagnostic URLs do not determine the result.
   143	
   144	   Condition 5 requires every path in the base-to-head diff to match an `allowed_files` entry and additions-plus-deletions totals to remain within the effective Check caps. The comparison is `gh api repos/{owner}/{repo}/compare/<base40>...<head40>` using the PR API's base and head, and its full `merge_base_commit.sha` identifies the merge base. Consume the complete authenticated file list and its additions/deletions; account for both names of a rename. An unreadable merge base or incomplete changeset holds. The main checkout's `.git`, including `origin/main`, replacement refs and objects, is not an evidence source. Backticked exclusions after `outside` leave the outside count; default exclusions remain `tests/` and `.orchestration/`. Item 7 retains amendment precedence.
   145	
   146	   Condition 6 reads one orchestrator-pasted INV-6 counters block in the acceptance record, bound there to this task, PR and full head. This task chooses the pasted record rather than a live store query so verdict executes no agmsg shell code and cannot follow worker-writable `drivers.partition`. It never invokes `scripts/regime-counters.sh` or sources the agmsg storage layer. No `S1:` line is present and the parsed decimal `revises` value is below 2. A missing ledger or counters block, duplicate block, mismatched binding or unreadable count holds; an absent count is never zero.
   147	
   148	   Condition 7 requires the numeric count of open P0/P1 findings to be zero. Findings with status `new`, `still-open` or absent count as open regardless of identifier or scope.
   149	
   150	   Condition 8 first validates `security` as an explicit boolean. Only boolean `false` permits the non-security branch. Boolean `true` requires the security review's front-matter `head:` to equal the verdict's own full 40-hex head and its last non-blank line to be `Verdict: correct`. A sha7 filename is never a head match. Missing, null or non-boolean metadata holds with the named reason specified below.
   151	
   152	   Condition 9 requires at least one `sha256:<hex> <path>` line in the acceptance record's prose and verifies every such line against its file. Every inspected evidence file, including audit, security, local review and saved or fresh sweep, is named with and matched against the verdict's full 40-hex head: Markdown uses front-matter `head:`, audit and local-review JSON use `head` (on every record for a JSON list), and feedback JSON uses `head_sha`. Missing, invalid or different full-head metadata holds even when a filename or sha7 prefix matches. Hashes preserve consumed bytes; they do not authenticate a local Git object or ref.
   153	
   154	   All nine conditions passing produces `accept`. Failure of condition 6 or 7, missing or unreadable input, schema-invalid input, invalid security metadata or an internal evaluation error produces `hold`. Other failed conditions produce `revise`. The revise line remains `AGMSG-ACCEPTANCE v1 task_id=<task> status=revise previous_head=<head> reason=<failed ids> next_action=<the first failed condition's evidence, shell-safe>`. The orchestrator supplies `check=` selectors.
   155	
   156	   The generated verdict is `.orchestration/validation/<task>-verdict-<head>.json`, using the full 40-character head under design 5.14 item 5. Its fields remain `verdict`, `pr`, `head`, `task_id`, `conditions[]`, `inputs_sha256{}`, `generated_at` and optional `revise_line`, validated against `.schemas/verdict.json`. Audit, security, local-review and sweep inputs use full-head-named verified snapshots with the metadata bindings above. External producers are not edited; the orchestrator supplies the full-head-named evidence and required metadata before evaluation, retaining original artifacts separately. Historical verdict files remain untouched.
   157	
   158	   Exit codes remain 0 for accept, 10 for revise, 20 for hold and 2 for usage or internal error, with internal error treated as hold. A destination or execution-boundary refusal holds with exit 20. Refusal before a usable task or head exists reports hold without inventing an output identity.
   159	
   160	   `--apply` requires the trusted execution context and scripts, schemas and task files whose consumed bytes and complete file inventory equal GitHub's `base40` tree, read through its API at that SHA, with no substituted or extra executable helper in those code directories. Do not use local tracking status, `origin/main` equality or shared objects to authenticate them. Execute verified snapshots as Reset design item 2 requires. The last four shadow rows must agree between machine and human and represent four distinct PRs. Four rows for one PR do not unlock application. Item 6 retains the integration gate before either application effect.
   161	
   162	   After accept and a successful gate, application writes the accepted line to a temporary file, sends it through `scripts/orchestrator/dispatch.sh <team> <from> <to> <pane> <file> <record>`, then invokes `gh pr merge <pr> --squash --match-head-commit <head>`. Its reason names `verdict-<head>`. Team, sender, recipient and placement remain explicit arguments. Arguments containing `--admin` or `--auto` anywhere are refused with exit 2 before input reads or tool calls other than mandatory startup sanitization.
   163	
   164	   `--shadow` writes the verdict JSON and, only for a non-hold verdict, appends `<pr>\t<head>\t<verdict>\t\t\t<generated_at>` to `.orchestration/validation/verdict-shadow.tsv`. Columns remain `pr`, `head`, `machine`, `human`, `agree` and `at`; the orchestrator supplies the human and agreement columns. Shadow mode sends nothing and merges nothing.
   165	
   166	   `--loop` retains PR-number order, eligible open non-draft PRs on `main`, and an acceptance record naming each current head. Each recursive verdict invocation uses the sanitized program-entry contract. The loop rereads GitHub's PR base and head between PRs and, with `--apply`, refreshes the trusted execution files from GitHub at the newly authenticated main/base SHA after each child, verifying their complete inventory and bytes before another child executes. Failed refresh holds with exit 20; a fetch or local fast-forward alone does not satisfy refresh. Neither evaluation nor refreshed execution uses the main checkout's shared refs or objects.

**Reviewing test coverage and dispatch logic**
codex
The revised text removes the five issues from its previous text review. I found two remaining concerns: it preserves caller-supplied `HOME` while the shared resolver derives its installation root from `HOME`, and it treats verified gate/dispatch scripts as safe to execute even though those scripts select further tools and read live state. I’m checking those paths before assigning findings.
exec
/bin/zsh -lc "nl -ba scripts/orchestrator/dispatch.sh | sed -n '230,250p;338,380p'" in ~/Workspace/dotfiles
 succeeded in 0ms:
   230	Loader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique)
   231	lines = open(sys.argv[1], encoding="utf-8").read().split("\n")
   232	end = lines.index("---", 1) if lines[0] == "---" else None
   233	front = yaml.load("\n".join(lines[1:end]), Loader) if end else None
   234	sys.exit(0 if isinstance(front, dict) and front.get("kind") == "review" else 1)
   235	PY
   236	    # Fail-closed: only a parsed front matter whose kind is review skips the checker.
   237	    if ! uvr python -I -c "${brief}" "${tf}" > /dev/null 2>&1; then
   238	        out="$(uvr python -I "${here}/task-consistency-check.py" --root "${root}" "${tf}" 2>&1)" || {
   239	            echo "dispatch: ${tf} fails the task-consistency check" >&2
   240	            printf '%s\n' "${out}" >&2
   241	            exit 1
   242	        }
   243	    fi
   244	fi
   245	[[ -n ${record} ]] || exec agmsg-dispatch "${team}" "${from}" "${to}" "${pane}" "${line}"
   246	
   247	# Modes: `check` parses the record and writes the pre-send window to the window file; `append` aligns
   248	# history.sh's post-send window on stdin with it, takes the sent row's read marker (● unread, ○ read) and appends it.
   249	read -r -d '' recorder << 'PY' || true
   250	import fcntl, json, os, re, shutil, sys, tempfile
   338	    exit 1
   339	fi
   340	limit=${BUS_READ_WINDOW:-200}
   341	[[ ${limit} =~ ^[1-9][0-9]*$ ]] || usage
   342	task="$(value_of task_id)"
   343	# A private window file (mode 0600, a fresh name), removed whatever the exit.
   344	window="$(mktemp "${TMPDIR:-/tmp}/dispatch-window.XXXXXX")"
   345	trap 'rm -f -- "${window}"' EXIT
   346	# Team-wide: history.sh renames the calling pane after an agent argument (thread 4254399805).
   347	bus() { "${AGMSG_SCRIPTS:-${HOME}/.agents/skills/agmsg/scripts}/history.sh" "${team}" "" "${limit}"; }
   348	bus | python3 -I -c "${recorder}" check "${record}" "${line}" "${from}" "${to}" "${window}" "${task}"
   349	rc=0
   350	agmsg-dispatch "${team}" "${from}" "${to}" "${pane}" "${line}" || rc=$?
   351	bus | python3 -I -c "${recorder}" append "${record}" "${line}" "${from}" "${to}" "${window}" "${task}"
   352	exit "${rc}"

exec
/bin/zsh -lc "nl -ba .orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md | sed -n '35,85p'" in ~/Workspace/dotfiles
 succeeded in 0ms:
    35	  - control: ".orchestration/dotfiles-T133-verdict-audit-pool-a04/learning.md"
    36	    disposition: "residual: reusable learning remains separate from executable policy and from predecessor evidence."
    37	  - control: ".orchestration/dotfiles-T133-verdict-audit-pool-a04/autoskill.md"
    38	    disposition: "residual: the run status or not-used record grants no execution or promotion authority."
    39	  - control: ".orchestration/dotfiles-T133-verdict-audit-pool-a04/revise.yaml"
    40	    disposition: "residual: revision instructions and selectors remain data, bounded by this task's files, caps and round allowance."
    41	  - control: "agmsg storage route (~/.agents/skills/agmsg/scripts/lib/storage.sh)"
    42	    disposition: "out-of-scope: dotfiles-T133-agmsg-hardening-a01 owns worker-writable drivers.partition and plugin sourcing; the orchestrator writes that owner task before dispatch. The compensating control here is no agmsg shell sourcing or counter-script execution: verdict reads only the orchestrator-pasted counters in the acceptance record."
    43	  - control: task metadata
    44	    disposition: "residual: the orchestrator checks format-2 consistency before dispatch and at acceptance, validates security as an explicit boolean, and compares the complete dispatched task with its branch copy."
    45	  - control: metadata separators
    46	    disposition: "residual: the first opening and closing document separators bound safe-loaded YAML; the byte comparison also covers the body and subsequent separators."
    47	  - control: in-process effects
    48	    disposition: "residual: the Python child contains verdict and shadow writes; hold never appends a shadow row, and application still requires accept, four distinct agreeing PRs and a successful integration gate before dispatch or merge."
    49	  - control: workflow and interpreter or environment inputs
    50	    disposition: "residual: program startup, sanitized callers and internally fixed executable paths remove the caller-bin interface; shared-UID access to installations, credentials and host state remains outside the isolation these controls provide."
    51	  - control: new or renamed scripts
    52	    disposition: "residual: verdict.sh remains the only implementation executable introduced by this PR; no pool executable, caller wrapper, dependency or production test-override interface is added."
    53	  - control: orchestrator effect merge
    54	    disposition: "residual: only the orchestrator performs the live head-matched squash merge after the prescribed evidence and integration gate; worker application tests use fixtures."
    55	  - control: orchestrator effect update-branch
    56	    disposition: "residual: an update-branch changes the head and invalidates head-bound evidence; the orchestrator repeats required CI, feedback collection, audit and security review for the resulting head."
    57	  - control: orchestrator effect forced worker removal
    58	    disposition: "residual: no forced removal is planned; any forced removal follows the existing dirty-worktree rule and records discarded uncommitted state."
    59	  - control: "design 5.14 item 1 (worker write boundary)"
    60	    disposition: "residual: the worker does not change its own execution boundary; Claude write isolation is not inferred from render-check, and the orchestrator verifies the deployed boundary separately."
    61	  - control: "design 5.14 item 2 (sanitized environment before execution)"
    62	    disposition: "residual: privileged program startup and env -i callers remove inherited startup functions and selectors before verdict processing; caller integration and shared-UID host execution remain separately assessed."
    63	  - control: "design 5.14 item 3 (trusted path boundaries)"
    64	    disposition: "residual: resolved executable and destination paths are checked against the declared trusted roots; a same-UID process outside a worker sandbox can still mutate host paths."
    65	  - control: "design 5.14 item 4 (execute verified identities and consume verified contents)"
    66	    disposition: "residual: executables run by verified realpath, consumed snapshots are rehashed immediately before use, and decision-input hashes enter the verdict; snapshots do not create a boundary against unrestricted same-UID mutation."
    67	  - control: "design 5.14 item 5 (output and reservation identity)"
    68	    disposition: "residual: verdict and evidence snapshot filenames and shadow rows use the full head; each audit, security, local-review and sweep input is also matched by its full-head metadata, and this verdict task introduces no reservation lock."
    69	  - control: "design 5.14 item 6 (honest residuals)"
    70	    disposition: "residual: startup, path and snapshot controls are reported as damage reduction; neither host isolation nor independent GitHub credentials is claimed."
    71	  - control: "design 5.14 item 7 (verification)"
    72	    disposition: "residual: this task supplies concrete regression selectors and final-head evidence; the shared trusted-execution test helper remains owned by P1-6 and is reused only if available without expanding this task's edit boundary."
    73	  - control: "design 5.14 item 8 (committed approval ledger)"
    74	    disposition: "residual: verdict evaluation supplies no permission approval; PR base, head, changeset and inspected PR bytes come from GitHub at full SHAs, never the main checkout's shared refs or objects; the integration gate remains authoritative and shared credentials remain a residual."
    75	  - control: "design 5.14 item 9 (private cache and absolute interpreter)"
    76	    disposition: "residual: the shared trusted-interpreter resolver and anchored private uv cache exclude worktrees, worker-writable caches and temporary directories; until the P1-3 resolver is available, verdict holds without a private resolver or PATH fallback."
    77	  - control: "design 5.14 item 10 (worker commands remain sandboxed)"
    78	    disposition: "residual: every worker gh command and git write runs individually inside the sandbox; a command that cannot complete there produces a blocked PONG rather than an escape or alternate execution route."
    79	premises: []
    80	---
    81	
    82	# AGMSG-TASK dotfiles-T133-verdict-audit-pool-a04 — INV-6 S1 re-plan of a03 (plan 024 P1-4a; PR #410)
    83	
    84	Worker: a008, Claude Code, worktree `worker-f`.
    85	

exec
/bin/zsh -lc "ls -l .orchestration/tasks/dotfiles-T133-agmsg-hardening-a01.md .orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md; rg -n 'gh|Linux|case|after:|deployment|deployed|Prerequi' .orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md" in ~/Workspace/dotfiles
 succeeded in 0ms:
ls: .orchestration/tasks/dotfiles-T133-agmsg-hardening-a01.md: No such file or directory
-rw-r--r--@ 1 a0004262  staff  88746 Oct 19 17:16 .orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md
29:after: []
41:  - control: "home/dot_claude-worker/modify_private_settings.json (deployment of the dedicated worker baseline without importing orchestrator policy)"
51:  - control: "scripts/validate-agent-assets.py (only the Linux and macOS excludedCommands policy check at base lines 349-355)"
52:    disposition: "residual: the check follows the manifest's new policy exactly as section 5.14 item 1 states it; tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_claude_sandbox_validator_refuses_each_forbidden_form supplies the updated macOS gh-exclusion and Linux extra-exclusion fixtures; validation checks rendered policy content without establishing live sandbox enforcement."
65:  - control: "tests/unit/test_validate_agent_assets.py (only the macOS gh-exclusion and Linux extra-exclusion fixtures)"
67:  - control: "tests/unit/test_claude_settings_merge.py (orchestrator baseline preservation and failure-policy rendering through the existing merge)"
71:  - control: "tests/unit/test_claude_worker_settings.py (dedicated settings deployment, static narrow denies, worktree configuration protection, project guard and hook failure configuration)"
72:    disposition: "residual: fixtures verify configured controls and credential-free deployment behavior; runtime permission checks and the remaining path-consumption window remain deployment and host residuals."
76:    disposition: "residual: artifacts distinguish documentation facts, historical probes, final-head fixture results and unperformed operator deployment; acceptance compares their claims with the diff and CI."
86:    disposition: "residual: generation and tests use repository files and temporary fixtures; the worker performs no live deployment, login, administrative installation, permission-policy mutation or operator-session restart."
90:    disposition: "residual: the worker settings modify script, orchestrator-only guard and repository-owned Herdr state helper have named source and installed paths; RESULT inventories their interpreter and descendant bindings without introducing a worker-write-boundary hook or gh wrapper."
92:    disposition: "residual: host controls reduce accidental and injected damage without isolating seats sharing one OS user; prevention of worker-initiated merges requires a separate OS user or host under D-024-23's future P1-16, which the operator decides; the GitHub boundary is detection, not prevention, through P1-11's regime check in the next records PR for missing acceptance or gate evidence; shared managed control-plane exclusions and the Herdr socket remain residual."
98:    disposition: "residual: canonical anchor and interpreter checks reduce worker-selected trusted paths and account for symlink components and filesystem case aliases; other consuming-helper checks remain with their owning hardening tasks."
108:    disposition: "residual: the regime reads the ledger through the GitHub contents API at the SHA returned by git ls-remote origin refs/heads/main; P1-14 a05 implements that read, and local refs, files and object traversal provide no approval authority; the GitHub boundary is detection, not prevention."
112:    disposition: "residual: empty worker user exclusions and disabled unsandboxed requests reduce escape routes; the worker rule forbids using shared managed control-plane exceptions, whose availability and Herdr socket access remain residual; the deterministic Codex permgate rule and live deployment remain operator steps."
130:      D-024-21 establishes the host threat model and dedicated Claude worker configuration. D-024-23 supersedes D-024-22's credential-separation claim because gh Keychain access is shared by seats running as the same macOS user. Prevention requires a separate OS user or host; the current GitHub boundary is detection, not prevention.
136:      The existing Claude settings modify script merges the orchestrator user baseline into current settings and appends an attachment hook. The dedicated worker renderer does not import that orchestrator settings merge or its attachment behavior. The administrative managed-settings file is a separate deployment destination.
142:      The current launcher constructs worker profile options separately from the pane environment. The dedicated Claude configuration directory and private cache variables reach the actual worker process on every launch route. This task adds no gh configuration directory or credential-separation mechanism.
172:This is the amendment-1 text of the task dispatched at 2026-10-19T05:42Z (the ninth-round text that passed its pre-dispatch security review). Amendment 1 folds in two interpretation notes the worker needed (the inherited make format clause; the portable tracked `.claude/settings.json` with host-specific paths only in the rendered guard) and removes the Codex worker profile item (a Codex seat edits no Codex-boundary source; it becomes the separate Claude-seat task dotfiles-T133-codex-worker-network-a01). Everything else is the dispatched text in meaning; the branch, the eight green tests and the fixtures stay; the worker swaps the task copy to this text at its next push.
174:The host is not a security boundary between seats sharing one OS user. gh keys Keychain credentials by host and user, so a worker running as the same macOS user can read the orchestrator's token regardless of `GH_CONFIG_DIR`. Prevention of a worker-initiated merge requires a separate OS user or host under D-024-23's future P1-16, which the operator decides whether to pursue. Until then the GitHub boundary is detection, not prevention. The regime detects missing acceptance or gate-passage evidence in the next records PR, not at main-push time, because the records reach main only with that boundary PR. On a PR touching `.orchestration/acceptance/**`, the regime job checks every main merge commit since the previous boundary for its corresponding acceptance record with gate-passage evidence and fails the PR when one is missing. P1-11 owns implementation of that check; this task states section 5.14 item 0's detection rule. Approvals and gate evidence of record are read from GitHub at a SHA through its API inside the sandbox. Host-local controls reduce accidental and injected damage without establishing isolation from a malicious same-UID process.
176:This task implements section 5.14 items 1, 9 and 10 through a dedicated Claude worker configuration directory, static Edit deny rules on trusted paths and worktree configuration, managed sandbox enforcement, guarded project hooks, hook interpreter and PATH bindings, private worker caches and the rule that worker commands run inside their sandbox. Every Claude seat has `sandbox.failIfUnavailable: true`.
180:[memory:decision] D-024-20 makes this task the dispatch prerequisite of P1-14 a05, P1-10 a02, audit-pool-a02 and P1-6. The orchestrator places this task in their `after:` fields before dispatch. This task has `after: []`. A Codex seat performs these Claude configuration edits under the routing rule, including the Worker Playbook step 4 sentence permitted by plan 021 step 8.3. This Codex seat edits no Codex-boundary source.
182:The design source is `.orchestration/plans/024-design-quality.md` section 5.14 items 0 through 10. D-024-21, D-024-23 and the amended items 0, 1 and 8 govern this revision. D-024-22's proposed gh credential separation is superseded. The acceptance record preserves documentation facts and earlier proposals as history.
188:The fifth C-80 text review is `.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-08e6ac7.md.last.md`. Its three P1 findings remain recorded. This revision removes the gh credential-separation mechanism, records the upstream agmsg store-driver residual and moves sandbox enforcement into administrative managed settings.
192:The 2026-10-19T03:45:06Z sandbox probe ran `gh api repos/mryfmo/dotfiles --jq .name` and returned `dotfiles`. The recorded sandbox proxy used CONNECT without TLS interception, and gh read the Keychain token. This historical observation confirms neither credential separation nor final-head deployment readiness.
194:The documentation facts recorded at 03:2xZ establish that Edit denies also affect the Bash sandbox, hooks reload during a session and an unavailable sandbox is fail-open by default. D-024-21's 04:0xZ decision establishes the dedicated Claude configuration mechanism, directory-specific Claude credentials, symlink coverage and `onFailure: "block"` support. These Claude credentials do not separate gh Keychain access.
202:   The manifest names `orchestrator_checkout` as the anchored primary checkout and supplies trusted deployment bindings for the guard, hook scripts and absolute interpreters. These bindings resolve outside worker worktrees and executable caches. Worker cwd, tool input, worktree configuration and inherited command variables do not select them. The manifest also supplies the trusted bindings from which the render resolves the absolute directories holding `ruff`, `prettier` and `terminal-browser`, without using mise shims.
214:   The orchestrator retains its existing permissions, cache allowances and hook functions within the administrative managed policy. Its user baseline receives `failIfUnavailable: true`, `onFailure: "block"` on its hooks and the interpreter and PATH bindings below. Its exclusion entries match the three control-plane entries specified below; the former Linux `gh *` exclusion is removed.
228:   Edit denies cover Write, MultiEdit and NotebookEdit through Claude's permission system. Requested-path and resolved-target matching supply the documented symlink coverage. The generator creates no `executable_worker-write-boundary.py` or replacement PreToolUse path validator.
248:   Every generated hook entry carries `onFailure: "block"`. Every generated command hook starts with `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}"` before its trusted installed entrypoint. The prefix re-exports HOME from the launcher environment before any HOME-relative entrypoint path. Host-specific interpreter, private-link-directory, anchored-checkout and tool-directory bindings remain in the per-host rendered guard and rendered worker settings. The formatter and project-map hooks run through the installed orchestrator-only guard and receive the role-specific pinned PATH specified below. Merge evidence identifies hooks appended by the existing modify script and distinguishes them from generated baseline entries. The report accounts for the effective deployed hook set without equating baseline coverage with coverage of runtime-added entries.
254:   It renders the static trusted-path Edit denies, the worktree `.claude` and `.mcp.json` Edit denies, retained native merge denials, empty user `excludedCommands`, `allowUnsandboxedCommands: false`, restricted `allowWrite`, no user Herdr socket allowance and `failIfUnavailable: true` for both Darwin and Linux.
270:   The rendered `sandbox.excludedCommands` list contains exactly `agmsg-dispatch *`, `herdr-agents *` and `<absolute-home>/.agents/skills/agmsg/scripts/actas-claim.sh *`. These are the orchestrator's three control-plane entries. It contains no `gh *`, `git push *` or authenticated-fetch exemption.
284:   The target selects `/Library/Application Support/ClaudeCode/managed-settings.json` on macOS and `/etc/claude-code/managed-settings.json` on Linux and prints the exact command `sudo install -m 0644 "<absolute-home>/.claude/managed-settings.rendered.json" "<detected-managed-settings-path>"` with the actual staging path and detected destination substituted and shell quoting preserved. The printed command is ready for the operator to run.
288:   `tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_install_target_stages_and_prints_without_running_sudo` covers both macOS and Linux, uses a temporary home, verifies the staged JSON and exact printed command with the detected destination, includes a home path containing spaces and asserts that a planted sudo marker remains absent.
296:   Rendering handles empty and malformed input through the repository's existing baseline behavior and is idempotent. It neither reads credentials nor initiates authentication.
298:   `tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_settings_replace_stale_policy_idempotently` exercises repeated deployment in temporary homes. `tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_settings_do_not_import_orchestrator_hooks` plants orchestrator hook and plugin markers and verifies their absence.
304:   The guard compares canonical `CLAUDE_PROJECT_DIR` with the anchored checkout. Equality executes the fixed operation supplied by the caller through the guard's trusted interpreter and anchored-script bindings, subject to the formatter and project-map tool-input check below. Every other launch root exits 0 without executing it. `CLAUDE_PROJECT_DIR` supplies launch identity and never selects an executable.
314:   `tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_project_guard_uses_launch_root_and_never_runs_worker_payloads` plants worker Stop, contextdb and formatter payloads. Worker and unrelated-root invocations leave all markers absent. The positive-path case runs the complete rendered command in a subprocess with a fake `CLAUDE_PROJECT_DIR` equal to the anchored checkout and asserts that the guarded script executed while preserving its arguments and status. A second case runs the complete rendered command with a worktree `CLAUDE_PROJECT_DIR` and asserts that the guarded script did not execute. A planted `BASH_ENV` in the outer environment remains unexecuted in both cases. Formatter and project-map reload cases keep `CLAUDE_PROJECT_DIR` anchored and supply hook tool input for an outside file and a worker-repository file under `.claude/worktrees/`; both exit 0 with command and planted configuration markers absent. Matching anchored-file inputs run both commands normally. The guard tests execute the portable HOME-relative hook command against separately rendered per-host guards, assert the `HOME="$HOME"` re-export and verify that interpreter and anchor selection occurs only inside the rendered guard. Changing `CLAUDE_PROJECT_DIR` never changes the selected executable.
316:9. `.claude/settings.json` retains its tracked project hooks and rewrites every command through the installed orchestrator-only guard.
328:    Every Claude worker pane starts with `CLAUDE_CONFIG_DIR=<absolute-home>/.claude-worker`. This value reaches the actual worker process through the pane command and environment construction. Setting it only in the parent spawn process does not satisfy this requirement.
330:    Managed-workspace and standalone-worker routes receive the same binding. Repeated starts do not inherit a conflicting caller Claude configuration directory. This task introduces no worker gh configuration directory, gh templates or credential-separation claim.
340:    The launcher also regenerates its managed hooks in the main checkout's `.claude/settings.local.json`. Every local agmsg delivery and orchestrator attachment command that it writes runs through the installed orchestrator-only guard. The existing permissions object and unrelated non-hook settings remain stored. Their effective sandbox interpretation follows the administrative managed policy.
356:    `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_every_settings_hook_has_system_path_prefix` exhaustively traverses both settings files after initial preparation and repeated starts. It asserts the literal `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}"` prefix on every command hook, checks the split between absolute bindings in rendered worker settings and HOME-relative main-local guard calls, and asserts that a planted `BASH_ENV` in the hook's inherited environment does not run. The planted-`BASH_ENV` case is red against the current PATH-only form. The test also asserts `AGMSG_RESOLVE_PROJECT=0` in every agmsg delivery prefix and preservation of `AGMSG_STORAGE_PATH` when set in the launcher environment. It invokes the delivery resolver through the rendered prefix with an explicit worker path and a conflicting writable `run/proj.<pid>.project` marker and asserts that the resolver retains the explicit worker path.
360:    The currently installed `~/.claude/hooks/herdr-agent-state.sh` is generated by Herdr and is not a tracked source in this repository. Its bare `python3` descendant is not retained as a trusted worker hook. The repository-owned helper preserves the required state-reporting function and receives its absolute Python interpreter through the rendered invocation.
362:    Every hook command reaches a selected absolute interpreter and absolute script path through trusted installed bindings. The tracked settings name only the HOME-relative guard and fixed operation identifiers. Host-specific interpreter and anchor bindings reside inside the per-host rendered guard or rendered worker settings. Repository-owned shell descendants use absolute shebangs or explicit absolute shell invocations. Python descendants use the selected absolute interpreter with `-I`.
378:    The replacement sentence is: “Every worker command, including gh, git push and authenticated git fetch, runs inside the worker's sandbox; no worker command runs outside it.”
400:    Path fixtures cover symlink components and filesystem case aliases. They verify inventory and configuration identities without presenting a simulated permission matcher as proof of Claude runtime enforcement.
402:    Hook tests cover every generated and tracked entry's failure policy, worker user settings, guarded main-local settings, the `/usr/bin/env -i` prefix with explicit hook-variable re-exports, complete rendered-command positive and worktree-negative cases, role-specific pinned PATH bindings, suppression of a planted inherited `BASH_ENV` and actual descendant execution. They distinguish synchronous policy hooks from background delivery and post-action events.
410:    The report maps each of the third C-80 review's five findings, fourth C-80 review's six findings and fifth C-80 review's three findings to the revised mechanism, its tests and its remaining residual or owning task. It distinguishes policy configuration from live enforcement and deployment.
412:16. `scripts/validate-agent-assets.py` changes only the Linux and macOS `excludedCommands` policy check at base lines 349-355, together with the two corresponding fixtures in `tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_claude_sandbox_validator_refuses_each_forbidden_form`.
414:    After this task, the validator requires the same exact ordered `sandbox.excludedCommands` list on macOS and Linux: `agmsg-dispatch *`, `herdr-agents *`, `{{ .chezmoi.homeDir }}/.agents/skills/agmsg/scripts/actas-claim.sh *`. These are the three entries derived from the manifest this task renders; the last entry becomes `<absolute-home>/.agents/skills/agmsg/scripts/actas-claim.sh *` after chezmoi expansion. Neither platform permits `gh *` or any additional exclusion. This follows `~/Workspace/dotfiles/.orchestration/plans/024-design-quality.md` section 5.14 item 1, read from the uncommitted main-checkout design (C-86). No other validator behavior changes.
426:The worker-write-boundary Python hook, its hook entries and `tests/unit/test_worker_write_boundary.py` are dropped. The gh-trusted wrapper remains dropped. The worker gh configuration directory, its templates and the dedicated-identity implementation are removed from this task.
430:The permission guard and merge gate remain P1-14 a05's work. P1-14 a05 and P1-6 implement the regime rule that approvals and gate evidence of record come from GitHub at a SHA through its API inside the sandbox. The GitHub boundary is detection, not prevention.
432:For the committed approval ledger, the regime obtains the commit SHA returned by `git ls-remote origin refs/heads/main` and reads `gh api repos/<owner>/<repo>/contents/.orchestration/decisions.tsv?ref=<sha>` inside the sandbox. The consuming implementation reads the API response's file content at that exact SHA. It does not fall back to local files, local refs or local object traversal.
440:The operator logs into Claude once with `CLAUDE_CONFIG_DIR=<absolute-home>/.claude-worker` selected. The Claude Keychain entry is keyed to that directory. This Claude login does not authenticate or isolate gh.
442:Administrative installation of `/Library/Application Support/ClaudeCode/managed-settings.json` on macOS and `/etc/claude-code/managed-settings.json` on Linux is the operator's step. The worker implements rendering, staging and the printed installation command without running sudo or installing live managed settings.
452:In `scripts/validate-agent-assets.py`, changes outside the Linux and macOS `excludedCommands` policy check remain out of scope. In `tests/unit/test_validate_agent_assets.py`, changes outside the two named fixtures remain out of scope.
474:Staging evidence shows the home-directory output and exact printed `sudo install -m 0644` command with the detected administrative destination on both macOS and Linux. The temporary-HOME test proves that the target executes no sudo command.
482:Guard markers also show that worker project scripts, contextdb hooks, Stop gates and formatter payloads do not execute through tracked hooks. Descendant markers show that planted PATH interpreters do not execute on the tested hook routes, including an upstream-style `/usr/bin/env bash` descendant.
496:One implementation PR continues the existing branch `tools/worker-write-boundary-a01`, created from clean base `205fe85c`, on the Codex seat a010. The eight green tests, fixtures and evidence stay. The first push deletes the predecessor copy `.orchestration/dotfiles-T133-worker-write-boundary-a01/task.md` and adds the byte-identical dispatched a02 task at `.orchestration/dotfiles-T133-worker-write-boundary-a01/task.md`. This predecessor-copy deletion is the sole authorized edit to the predecessor's artifact directory.
504:Every gh write and every git write runs as a separate command without shell chaining. Every worker command remains inside its sandbox. An operation that cannot complete there produces a blocked PONG with the exact command and boundary.
512:Administrative managed settings require sandboxing for the orchestrator as well as workers and disable unsandboxed retries. The former Linux gh exemption is removed. The orchestrator retains its existing functions within those requirements and the specified hook failure, guarding and interpreter/PATH-binding changes.
514:The report states that no gh credential separation is established. Shared credentials permit worker-initiated API merges despite native command denials. The GitHub boundary is detection, not prevention, with the required next-records-PR regime check owned by P1-11.
520:The permission-surface change receives the required operator-backed approval through the repository's existing process. The worker writes no approval row and treats no candidate-tree decision as authority.
522:Live deployment is the operator's post-merge `make update`. The operator runs `make install-managed-settings`, inspects the rendered staging file and executes its printed `sudo install -m 0644 "<absolute-home>/.claude/managed-settings.rendered.json" "<detected-managed-settings-path>"` command with `/Library/Application Support/ClaudeCode/managed-settings.json` detected on macOS and `/etc/claude-code/managed-settings.json` detected on Linux. Administrative installation is recorded separately from staging and ordinary chezmoi application.
528:The deployment record checks effective settings after `make update` and administrative installation, including hooks added by merge scripts or integration installers. It verifies the installed managed-settings content, admin-required sandbox scope, worker directory, both platform policy outputs, static deny inventory, worktree-configuration denies, writable agmsg stores, worker-user and main-local hook placement, hook PATH and interpreter descendants, failure-policy coverage and sandbox startup without exposing credentials.
532:Merge alone does not establish deployment readiness. The orchestrator records `make update`, the managed-settings installation with sudo, the Claude worker-directory login, effective startup checks and the Codex permgate rule before releasing dependent hardening tasks for live operation. The upstream agmsg store-driver route remains a named residual until its owning task is implemented. GitHub remains detection, not prevention, until the operator pursues separate-user or separate-host isolation under future P1-16.
542:Local Bats, live enforcement, administrative installation, worker-directory login, permgate policy changes and deployment are not performed by the worker.

web search: 
web search: site.cli.github.com/manual/gh_pr_merge --repo match-head-commit ...
**Ensuring secure directory handling**
**Analyzing gate integrity risks**
exec
/bin/zsh -lc "rg -n 'source|storage|drivers|partition' ~/.agents/skills/agmsg/scripts/history.sh ~/.agents/skills/agmsg/scripts/lib/storage.sh" in ~/Workspace/dotfiles
 succeeded in 0ms:
~/.agents/skills/agmsg/scripts/lib/storage.sh:2:# storage.sh — resolve the path to the sqlite message store (messages.db).
~/.agents/skills/agmsg/scripts/lib/storage.sh:4:# Scope: the storage axis only — where messages are persisted. This is NOT a
~/.agents/skills/agmsg/scripts/lib/storage.sh:5:# storage-driver interface; it just centralizes the path resolution that was
~/.agents/skills/agmsg/scripts/lib/storage.sh:14:# and the built-in default once the storage-driver work lands; the intended
~/.agents/skills/agmsg/scripts/lib/storage.sh:18:# Guard against double-source. This used to be genuinely harmless to skip
~/.agents/skills/agmsg/scripts/lib/storage.sh:21:# own comment on its unconditional ". storage.sh" says so explicitly. That
~/.agents/skills/agmsg/scripts/lib/storage.sh:23:# (agmsg_storage_dir, _agmsg_partition_load): re-sourcing reset them to their
~/.agents/skills/agmsg/scripts/lib/storage.sh:25:# warmed (measured: watch.sh's own top-level warm of agmsg_storage_dir was
~/.agents/skills/agmsg/scripts/lib/storage.sh:26:# being wiped by resolve-project.sh's re-source moments later, #1330 second
~/.agents/skills/agmsg/scripts/lib/storage.sh:27:# stage). Every existing caller already tolerates a no-op re-source (that
~/.agents/skills/agmsg/scripts/lib/storage.sh:37:# validate.sh guards against double-sourcing, so a caller that sources it too is
~/.agents/skills/agmsg/scripts/lib/storage.sh:43:    source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/validate.sh"
~/.agents/skills/agmsg/scripts/lib/storage.sh:45:    # BASH_SOURCE empty — see agmsg_storage_dir for when that happens.
~/.agents/skills/agmsg/scripts/lib/storage.sh:47:    source "$SKILL_DIR/scripts/lib/validate.sh"
~/.agents/skills/agmsg/scripts/lib/storage.sh:51:# Built-in storage drivers use the shared UUIDv7 generator. Keep it available
~/.agents/skills/agmsg/scripts/lib/storage.sh:52:# through the storage facade so direct and registry-driven loads use one
~/.agents/skills/agmsg/scripts/lib/storage.sh:57:    source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/compat.sh"
~/.agents/skills/agmsg/scripts/lib/storage.sh:60:    source "$SKILL_DIR/scripts/lib/compat.sh"
~/.agents/skills/agmsg/scripts/lib/storage.sh:69:# storage driver choice (see _agmsg_partition_load's own comment for that
~/.agents/skills/agmsg/scripts/lib/storage.sh:75:agmsg_storage_dir() {
~/.agents/skills/agmsg/scripts/lib/storage.sh:96:    echo "Error: cannot resolve storage dir (BASH_SOURCE and SKILL_DIR both empty)" >&2
~/.agents/skills/agmsg/scripts/lib/storage.sh:107:# WHICH store depends on the team's partition driver, and teams choose separately:
~/.agents/skills/agmsg/scripts/lib/storage.sh:111:# that moves out. See scripts/drivers/partition/.
~/.agents/skills/agmsg/scripts/lib/storage.sh:127:  _agmsg_partition_load "$team" || return 1
~/.agents/skills/agmsg/scripts/lib/storage.sh:128:  _agmsg_db_file "$(partition_store_relpath "$team")"
~/.agents/skills/agmsg/scripts/lib/storage.sh:141:# Source the partition driver this team uses, memoized so repeated resolution in
~/.agents/skills/agmsg/scripts/lib/storage.sh:142:# one process costs nothing. Re-sources when a caller moves between teams on
~/.agents/skills/agmsg/scripts/lib/storage.sh:143:# different partitions — watch.sh loops over a subscription that can contain both.
~/.agents/skills/agmsg/scripts/lib/storage.sh:147:# not for the life of the process: a team's partition CAN change under a
~/.agents/skills/agmsg/scripts/lib/storage.sh:154:# a single cycle (the same pair's storage_init/read_cursor_get/watch_after/
~/.agents/skills/agmsg/scripts/lib/storage.sh:164:_agmsg_partition_load() {
~/.agents/skills/agmsg/scripts/lib/storage.sh:165:  # The registry may not be sourced yet — agmsg_db_path is reachable without
~/.agents/skills/agmsg/scripts/lib/storage.sh:166:  # going through agmsg_storage_load. Same guarded pull-in that uses.
~/.agents/skills/agmsg/scripts/lib/storage.sh:196:    name="$(agmsg_driver_for_team partition "$team" shared)"
~/.agents/skills/agmsg/scripts/lib/storage.sh:210:    file="$base/partition/$name.sh"
~/.agents/skills/agmsg/scripts/lib/storage.sh:213:    if [ "$kind" = external ] && ! agmsg_driver_is_trusted partition "$name" "$file"; then
~/.agents/skills/agmsg/scripts/lib/storage.sh:221:    # Loud rather than falling back to shared: a team recorded a partition, and
~/.agents/skills/agmsg/scripts/lib/storage.sh:224:    echo "Error: no partition driver '$name' for team '$1'" >&2
~/.agents/skills/agmsg/scripts/lib/storage.sh:234:# table (its resources are project-scoped — there is no team to pass), and the
~/.agents/skills/agmsg/scripts/lib/storage.sh:242:# Join a store-relative path onto the storage directory. Defaults to the
~/.agents/skills/agmsg/scripts/lib/storage.sh:254:  db="$(agmsg_storage_dir)/${1:-messages.db}"
~/.agents/skills/agmsg/scripts/lib/storage.sh:261:# The storage selector for a list of <team>:<agent> pairs, shared by every
~/.agents/skills/agmsg/scripts/lib/storage.sh:275:    [ -n "$t" ] && [ "$t" != "$p" ] || { echo "storage: not a team:agent pair: $p" >&2; return 1; }
~/.agents/skills/agmsg/scripts/lib/storage.sh:278:      echo "storage: one call cannot span teams ($first, $t)" >&2
~/.agents/skills/agmsg/scripts/lib/storage.sh:282:  [ -n "$first" ] || { echo "storage: no team:agent pair given" >&2; return 1; }
~/.agents/skills/agmsg/scripts/lib/storage.sh:366:  # inbox.sh run, because storage_mark_read_batch's ids no longer matched
~/.agents/skills/agmsg/scripts/lib/storage.sh:371:  # _sqlite_data_stdin in drivers/storage/sqlite.sh, wrapping calls to THIS
~/.agents/skills/agmsg/scripts/lib/storage.sh:382:  # drivers/storage/sqlite.sh).
~/.agents/skills/agmsg/scripts/lib/storage.sh:406:# Only the sync driver adapter sets it (scripts/internal/storage-sync-driver.sh),
~/.agents/skills/agmsg/scripts/lib/storage.sh:453:# caller -- and only there: storage-sync-driver.sh sets `-o pipefail`
~/.agents/skills/agmsg/scripts/lib/storage.sh:491:# Runtime ownership seam. This is the first run/-state-in-storage primitive for
~/.agents/skills/agmsg/scripts/lib/storage.sh:492:# the storage 1.2 direction: a future remote driver can preserve these acquire /
~/.agents/skills/agmsg/scripts/lib/storage.sh:494:# `locks` is intentionally resource-generic; Codex dispatchers are merely the
~/.agents/skills/agmsg/scripts/lib/storage.sh:497:_agmsg_runtime_lock_resource_sql() {
~/.agents/skills/agmsg/scripts/lib/storage.sh:501:agmsg_storage_ensure_initialized() {
~/.agents/skills/agmsg/scripts/lib/storage.sh:505:  AGMSG_STORAGE_PATH="$(agmsg_storage_dir)" bash "$init_script" >/dev/null
~/.agents/skills/agmsg/scripts/lib/storage.sh:509:  local resource owner_pid expected_owner db resource_sql
~/.agents/skills/agmsg/scripts/lib/storage.sh:510:  resource="$1"; owner_pid="$2"; expected_owner="${3:-}"
~/.agents/skills/agmsg/scripts/lib/storage.sh:512:  agmsg_storage_ensure_initialized || return 1
~/.agents/skills/agmsg/scripts/lib/storage.sh:514:  resource_sql="$(_agmsg_runtime_lock_resource_sql "$resource")"
~/.agents/skills/agmsg/scripts/lib/storage.sh:517:  resource TEXT PRIMARY KEY,
~/.agents/skills/agmsg/scripts/lib/storage.sh:522:$(if [ -n "$expected_owner" ]; then printf "DELETE FROM locks WHERE resource = '%s' AND owner_pid = %s;" "$resource_sql" "$expected_owner"; fi)
~/.agents/skills/agmsg/scripts/lib/storage.sh:523:INSERT OR IGNORE INTO locks(resource, owner_pid, acquired_at)
~/.agents/skills/agmsg/scripts/lib/storage.sh:524:VALUES('$resource_sql', $owner_pid, strftime('%Y-%m-%dT%H:%M:%SZ','now'));
~/.agents/skills/agmsg/scripts/lib/storage.sh:525:SELECT owner_pid FROM locks WHERE resource = '$resource_sql';
~/.agents/skills/agmsg/scripts/lib/storage.sh:531:  local resource_sql
~/.agents/skills/agmsg/scripts/lib/storage.sh:532:  resource_sql="$(_agmsg_runtime_lock_resource_sql "$1")"
~/.agents/skills/agmsg/scripts/lib/storage.sh:534:    "SELECT owner_pid FROM locks WHERE resource = '$resource_sql';" 2>/dev/null \
~/.agents/skills/agmsg/scripts/lib/storage.sh:544:  local resource_sql
~/.agents/skills/agmsg/scripts/lib/storage.sh:546:  resource_sql="$(_agmsg_runtime_lock_resource_sql "$1")"
~/.agents/skills/agmsg/scripts/lib/storage.sh:548:    "DELETE FROM locks WHERE resource = '$resource_sql' AND owner_pid = $2;" \
~/.agents/skills/agmsg/scripts/lib/storage.sh:570:  source "$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)/sqlpath.sh"
~/.agents/skills/agmsg/scripts/lib/storage.sh:575:# _sqlite_lit / storage_send escaping, but driver-agnostic and available to the
~/.agents/skills/agmsg/scripts/lib/storage.sh:584:# ── Storage driver facade (storage axis) ─────────────────────────────────────
~/.agents/skills/agmsg/scripts/lib/storage.sh:587:# resolves the *active* storage driver, sources it, and makes the storage_*
~/.agents/skills/agmsg/scripts/lib/storage.sh:592:_agmsg_storage_config_path() {
~/.agents/skills/agmsg/scripts/lib/storage.sh:596:# Active storage driver name: env override > config "storage" key > built-in.
~/.agents/skills/agmsg/scripts/lib/storage.sh:597:agmsg_storage_driver() {
~/.agents/skills/agmsg/scripts/lib/storage.sh:603:  cfg="$(_agmsg_storage_config_path)"
~/.agents/skills/agmsg/scripts/lib/storage.sh:606:      "SELECT COALESCE(json_extract(readfile('$(agmsg_sql_readfile_path "$cfg")'), '\$.storage'), '')" \
~/.agents/skills/agmsg/scripts/lib/storage.sh:616:# Locate and source the active storage driver's storage_* functions. Idempotent.
~/.agents/skills/agmsg/scripts/lib/storage.sh:620:agmsg_storage_load() {
~/.agents/skills/agmsg/scripts/lib/storage.sh:622:  # Pull in the axis-generic registry once (its functions may not be sourced yet).
~/.agents/skills/agmsg/scripts/lib/storage.sh:630:  name="$(agmsg_storage_driver)"
~/.agents/skills/agmsg/scripts/lib/storage.sh:633:    file="$base/storage/$name.sh"
~/.agents/skills/agmsg/scripts/lib/storage.sh:635:    if [ "$kind" = external ] && ! agmsg_driver_is_trusted storage "$name" "$file"; then
~/.agents/skills/agmsg/scripts/lib/storage.sh:645:  printf 'agmsg: no trusted storage driver "%s" found\n' "$name" >&2
~/.agents/skills/agmsg/scripts/history.sh:17:source "$SCRIPT_DIR/lib/storage.sh"
~/.agents/skills/agmsg/scripts/history.sh:18:agmsg_storage_load
~/.agents/skills/agmsg/scripts/history.sh:25:  source "$SCRIPT_DIR/lib/self-name.sh"
~/.agents/skills/agmsg/scripts/history.sh:29:  source "$SCRIPT_DIR/lib/self-rename.sh"
~/.agents/skills/agmsg/scripts/history.sh:37:if ! storage_store_exists "$TEAM"; then
~/.agents/skills/agmsg/scripts/history.sh:45:HIST_JSONL=$(storage_history "$TEAM" "$AGENT" --limit "$LIMIT")
~/.agents/skills/agmsg/scripts/history.sh:83:# storage_list_unread over the distinct recipients in this slice. (Phase 1:
~/.agents/skills/agmsg/scripts/history.sh:92:  u=$(storage_list_unread "$TEAM" "$r") || continue
~/.agents/skills/agmsg/scripts/history.sh:106:  # Pass the statement on stdin instead, mirroring drivers/storage/sqlite-sync.sh:1082.

exec
/bin/zsh -lc "nl -ba .orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md | sed -n '100,114p'; nl -ba scripts/orchestrator/orch-gate.sh | sed -n '43,96p'" in ~/Workspace/dotfiles
 succeeded in 0ms:
   100	
   101	## Item 1 — one trusted interpreter resolver
   102	
   103	Add executable `scripts/orchestrator/trusted-interpreter.sh`, with English shdoc comments and `#!/bin/bash -p`. Execute it as a program; do not source it or invoke it as `bash <file>`. Its first statement implements the quoted environment check and re-exec, before assignments, traps, tool discovery or declaration reads. Check the actual environment through absolute paths; a caller-provided sentinel is not proof. The clean invocation must terminate normally rather than repeatedly re-execing because Bash maintains its own environment entries.
   104	
   105	Read only the repository’s exact Python declaration established by the dispatch prerequisite, anchored to the trusted script/repository location rather than the caller’s cwd. Parse its fixed grammar as data with trusted absolute tools, without `source`, `eval`, shell interpolation of declaration content, or an interpreter selected from that content. Refuse missing, duplicate, malformed, non-exact or metacharacter-bearing declarations; `latest` is invalid.
   106	
   107	Derive the installation root from HOME as `$HOME/.local/share/mise/installs` and construct only `<install root>/python/<version>/bin/python3`. Resolve and validate the candidate before printing it. Require an executable regular file after `realpath`, within the expected protected installation, outside the worktree, manifest worker roots, worker-writable caches and `$TMPDIR`. Check resolved path boundaries, including filesystem case behavior where applicable. Refuse a symlinked installation rather than accepting a redirected install directory.
   108	
   109	On success print exactly one absolute interpreter realpath and exit 0. On every refusal print a named `trusted-interpreter:` diagnostic to stderr, print no interpreter on stdout, and exit 2. There is no `command -v`, `mise which`, PATH search, version-alias selection, download or fallback. Do not execute a candidate to discover whether it is trustworthy.
   110	
   111	This is the common resolver required by item 9. This PR migrates its first consumer only; it does not authorize edits to other orchestrator scripts.
   112	
   113	## Item 2 — consume the resolver in ci-rerun.sh
   114	
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

web search: 
web search: https://cli.github.com/manual/gh_config
**Finalizing root cause and validation**
**Examining git snapshot and gate constraints**
web search: 
web search: https://sourceware.org/glibc/manual/latest/html_node/Dynamic-Linker-Invocation.html
exec
/bin/zsh -lc "git show 3f240b12:scripts/orchestrator/orch-gate.sh | sed -n '43,90p'" in ~/Workspace/dotfiles
 succeeded in 0ms:
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

**Analyzing Linux startup environment risks**
web search: 
web search: site.sourceware.org/glibc/manual "LD_PRELOAD" "secure" ...
**Finalizing update approach**
**Summarizing test results and threat findings**

I’m organizing the five main findings with their severity levels, clarifying skipped tests, and noting remaining risks and justifications for ratings while keeping the user’s format and adding a clear summary line before the verdict.
codex
- [P1] High confidence [.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:222](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:222) — Sanitization preserves attacker-supplied `HOME`, while the required resolver derives its trusted installation root from `$HOME/.local/share/mise/installs`; validating a candidate against that caller-selected root recreates executable selection through an environment variable.

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:220](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:220) — On Linux, inherited `LD_PRELOAD`/`LD_AUDIT` can execute before Bash’s first statement—or before `/usr/bin/env` clears the environment—because `bash -p` does not enable the loader’s secure-execution mode; the startup regression omits this route. [Loader semantics](https://man7.org/linux/man-pages/man8/ld.so.8.html)

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:42](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:42) — The “no agmsg shell sourcing” compensating control covers counters but fails during application: retained `dispatch.sh` invokes `history.sh`, which sources storage and partition drivers; verifying dispatch’s bytes does not bind this worker-influenced descendant execution, and application has no agmsg-hardening prerequisite.

- [P2] High confidence [.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:202](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:202) — The retained gate independently runs `uv python find`, rediscovers tools, and rereads shared refs and live evidence; snapshotting its script and testing a fake gate’s exit/order cannot establish the promised execution/input binding, so application needs an explicit compliant-gate prerequisite beyond the acknowledged argument-mismatch hold.

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:162](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:162) — Reads use a fixed repository, but the prescribed merge command omits `--repo` or a qualified PR URL, allowing local repository configuration to select another repository; matching the head SHA does not bind repository identity because forks can contain the same commit. [Merge options](https://cli.github.com/manual/gh_pr_merge)

📝 まとめ: Reviewed every threat row and the cited acceptance/review context; five findings remain for orchestrator disposition.

Not run: implementation tests, live application or deployment checks; no files changed. The execution-binding risks above remain unresolved.
Verdict: incorrect
hook: Stop
hook: Stop Completed
tokens used
108,696
- [P1] High confidence [.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:222](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:222) — Sanitization preserves attacker-supplied `HOME`, while the required resolver derives its trusted installation root from `$HOME/.local/share/mise/installs`; validating a candidate against that caller-selected root recreates executable selection through an environment variable.

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:220](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:220) — On Linux, inherited `LD_PRELOAD`/`LD_AUDIT` can execute before Bash’s first statement—or before `/usr/bin/env` clears the environment—because `bash -p` does not enable the loader’s secure-execution mode; the startup regression omits this route. [Loader semantics](https://man7.org/linux/man-pages/man8/ld.so.8.html)

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:42](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:42) — The “no agmsg shell sourcing” compensating control covers counters but fails during application: retained `dispatch.sh` invokes `history.sh`, which sources storage and partition drivers; verifying dispatch’s bytes does not bind this worker-influenced descendant execution, and application has no agmsg-hardening prerequisite.

- [P2] High confidence [.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:202](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:202) — The retained gate independently runs `uv python find`, rediscovers tools, and rereads shared refs and live evidence; snapshotting its script and testing a fake gate’s exit/order cannot establish the promised execution/input binding, so application needs an explicit compliant-gate prerequisite beyond the acknowledged argument-mismatch hold.

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:162](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:162) — Reads use a fixed repository, but the prescribed merge command omits `--repo` or a qualified PR URL, allowing local repository configuration to select another repository; matching the head SHA does not bind repository identity because forks can contain the same commit. [Merge options](https://cli.github.com/manual/gh_pr_merge)

📝 まとめ: Reviewed every threat row and the cited acceptance/review context; five findings remain for orchestrator disposition.

Not run: implementation tests, live application or deployment checks; no files changed. The execution-binding risks above remain unresolved.
Verdict: incorrect
