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
session id: 01a157fb-a7e5-78e2-be1a-0bb16df04a27
--------
user
Pre-dispatch security review (read-only, security profile) of the task text .orchestration/tasks/dotfiles-T133-records-sync-pr-a01.md and its threat_table, before any implementation exists. Judge the design the text states: can the controls it names bind what actually executes on this host (mise shims first on PATH, same-user worker processes, gh outside the sandbox on Linux, symlinks and case-insensitive filesystems, inherited GIT_* environment)? Check every threat row: a closed row whose named test cannot close it, a residual row whose control does not mitigate the risk, a missing row for a file or non-path control, and any gap of the class decision-not-bound-to-execution (a decision made on text or on a validated copy while the execution resolves binaries, files or ledgers from an attacker-influenced place). Read the related acceptance records and reviews the text cites for context. Report each finding as [P0-P3] <confidence> <file:line> <one line>; findings are input for the orchestrator, who decides. End with exactly one line: Verdict: correct or Verdict: incorrect.
warning: loading hooks from both /Users/a0004262/.codex/hooks.json and /Users/a0004262/.codex/config.toml; prefer a single representation for this layer
hook: SessionStart
hook: SessionStart
hook: SessionStart Completed
hook: SessionStart Completed
hook: UserPromptSubmit
hook: UserPromptSubmit Completed
codex
🤖 I read the AGENTS.md for mryfmo/dotfiles.
`agmsg-orchestration` と Ponytail のレビュー手順を読み、タスク本文・脅威表・参照記録を読み取り専用で確認します。制御の判断と、このホストで実際に実行される対象が結び付いているかを重点的に調べます。
exec
/bin/zsh -lc 'cat /Users/a0004262/.agents/skills/agmsg-orchestration/SKILL.md /Users/a0004262/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail/SKILL.md /Users/a0004262/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail-review/SKILL.md' in /Users/a0004262/Workspace/dotfiles
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
/bin/zsh -lc 'nl -ba .orchestration/tasks/dotfiles-T133-records-sync-pr-a01.md' in /Users/a0004262/Workspace/dotfiles
 succeeded in 0ms:
     1	---
     2	format: 2
     3	task_id: dotfiles-T133-records-sync-pr-a01
     4	kind: code
     5	security: true
     6	allowed_files:
     7	  - scripts/orchestrator/records-sync.sh
     8	  - tests/unit/test_records_sync.py
     9	  - .orchestration/dotfiles-T133-records-sync-pr-a01/**
    10	after: []
    11	threat_table:
    12	  - control: the PR edits scripts/orchestrator/records-sync.sh
    13	    disposition: "closed: tests/unit/test_records_sync.py::RecordsSyncTest::test_happy_path"
    14	  - control: the PR edits tests/unit/test_records_sync.py
    15	    disposition: "residual: fixtures use temporary repositories and fake service executables; the audit checks that assertions exercise the production script without contacting GitHub"
    16	  - control: the PR edits .orchestration/dotfiles-T133-records-sync-pr-a01/**
    17	    disposition: "residual: this directory holds task data and evidence only; the audit checks its complete diff and rejects executable payloads"
    18	  - control: the task copy .orchestration/dotfiles-T133-records-sync-pr-a01/task.md
    19	    disposition: "residual: the orchestrator compares all bytes and sha256 with the dispatched text at acceptance"
    20	  - control: the evidence records report.md, validation.md, sandbox.md, learning.md and autoskill.md
    21	    disposition: "residual: evidence is a claim until checked against command output, the diff and final-head CI; refusals and omissions stay visible"
    22	  - control: task metadata
    23	    disposition: "residual: the task-consistency checker parses the front matter before dispatch and acceptance; the task-copy comparison detects metadata changes"
    24	  - control: metadata separators
    25	    disposition: "residual: the checker parses the first YAML document and the byte comparison covers separators and the complete task text"
    26	  - control: in-process effects
    27	    disposition: "residual: production creates a dedicated proposal branch and PR; development uses fixture transports and never runs a live records sync"
    28	  - control: workflow and interpreter or environment inputs
    29	    disposition: "residual: no workflow or interpreter configuration is editable; design 5.14 governs the trusted parent and executable inputs"
    30	  - control: new or renamed scripts
    31	    disposition: "closed: tests/unit/test_records_sync.py::RecordsSyncTest::test_happy_path"
    32	  - control: orchestrator effect merge
    33	    disposition: "residual: the script never merges or queues auto-merge; written operator approval and the head-bound integration command remain with the orchestrator"
    34	  - control: orchestrator effect update-branch
    35	    disposition: "residual: only the orchestrator updates an implementation PR; a moved head requires fresh CI, feedback sweep and audit before the gate"
    36	  - control: orchestrator effect forced worker removal
    37	    disposition: "residual: none is requested; only herdr-agents removes a worker and any forced discard is recorded by the orchestrator"
    38	  - control: "design 5.14 item 0: 脅威モデル（D-024-21）"
    39	    disposition: "residual: same-UID writers can forge bus rows and local objects; these checks suppress mistakes, while approval stays with the orchestrator and detection is at the next records PR, not prevention"
    40	  - control: "design 5.14 item 1: 書き込み境界（前提 6、ランタイム別に正直に）"
    41	    disposition: "residual: seat configuration enforces its actual boundary; this task neither changes permissions nor claims isolation from other same-UID host processes"
    42	  - control: "design 5.14 item 2: 無害化した環境を最初に"
    43	    disposition: "closed: tests/unit/test_records_sync.py::RecordsSyncTest::test_trusted_exec_contract"
    44	  - control: "design 5.14 item 3: 信頼パスの境界検査"
    45	    disposition: "closed: tests/unit/test_records_sync.py::RecordsSyncTest::test_trusted_exec_contract"
    46	  - control: "design 5.14 item 4: 検証したものを実行し、検証した内容を渡す"
    47	    disposition: "closed: tests/unit/test_records_sync.py::RecordsSyncTest::test_replaced_input"
    48	  - control: "design 5.14 item 5: 出力と予約の同一性"
    49	    disposition: "residual: suffixes identify proposal branches, not approval evidence; record the full head and serialize invocations for each suffix, with no merge-slot reservation"
    50	  - control: "design 5.14 item 6: 正直な残余"
    51	    disposition: "residual: local sender and hash checks do not authenticate the shared store; the report states this limit and any unverified contract prerequisite"
    52	  - control: "design 5.14 item 7: 検証"
    53	    disposition: "closed: tests/unit/test_records_sync.py::RecordsSyncTest::test_trusted_exec_contract"
    54	  - control: "design 5.14 item 8: 承認はコミット済み台帳から読む"
    55	    disposition: "residual: origin/main seeds a proposal only; local task texts and bus rows grant no permission or merge approval, and every GitHub operation binds the fixed repository and host"
    56	  - control: "design 5.14 item 9: 私設キャッシュ"
    57	    disposition: "residual: consume the frozen executable-resolution contract, never source agmsg shell code or execute shims; any unavailable trusted prerequisite is a blocked PONG"
    58	  - control: "design 5.14 item 10: worker は sandbox 外でコマンドを実行しない（D-024-17 の改訂）"
    59	    disposition: "residual: every worker command, including gh and push, stays inside its sandbox; a refusal is recorded and reported without escalation"
    60	premises:
    61	  - claim: regime-ci uses the base's dispatched task text as policy, so each dispatch or amendment must reach main before its implementation PR can pass regime
    62	    command: |-
    63	      sed -n '7p' scripts/orchestrator/regime-ci.py
    64	    output: |-
    65	      on the base's dispatched text, the copy against the dispatched `.orchestration/tasks/<t>.md` at the base, whose text is the policy
    66	  - claim: the three supplied records-sync commits list the dispatched texts carried in PR 438
    67	    command: |-
    68	      git show -s --format='%h %s' 8bf7e6ac c58cf432 88add881
    69	    output: |-
    70	      8bf7e6ac chore(orchestration): sync the dispatched task texts of trusted-exec-contract-tests-a01 and loop-limits-a01 to main
    71	      c58cf432 chore(orchestration): add the dispatched texts of lint-followup-a04 and task-generator-plan-check-a05-checker
    72	      88add881 chore(orchestration): add the dispatched texts of chain-review a07, python-pin a01/a02 and worker-write-boundary a03
    73	  - claim: the repository's dispatch sender is claude-deep-dot; a body claiming to be the orchestrator is insufficient
    74	    command: |-
    75	      sqlite3 -readonly "$HOME/.agents/skills/agmsg/db/messages.db" "SELECT from_agent,COUNT(*) FROM messages WHERE from_agent='claude-deep-dot' AND body LIKE 'AGMSG-TASK v1 %' GROUP BY from_agent;"
    76	    output: |-
    77	      claude-deep-dot|594
    78	---
    79	
    80	# AGMSG-TASK dotfiles-T133-records-sync-pr-a01 — synchronize dispatched task texts through a records-only PR
    81	
    82	Read `.orchestration/learning/mistakes/M-20261020-02-boundary-carried-pre-dispatch-snapshots.md`: boundary preparation copied pre-dispatch bytes and never compared them with the bus; this task implements its records-sync corollary, not the separate boundary-wide in-flight scan. Design `.orchestration/plans/024-design-quality.md` 5.14 items 0–10 apply by reference, especially items 2, 3, 4, 7, 8 and 9; the design is frozen by D-024-29 and is not restated or amended here (D-024-30).
    83	
    84	## Item 1
    85	
    86	Write executable `scripts/orchestrator/records-sync.sh <branch-suffix> <task-id>...`. Require at least one distinct task id; accept only nonempty alphanumeric-led tokens containing alphanumerics, hyphens or underscores, so no option, traversal, SQL or ref injection is possible. Read only the named `.orchestration/tasks/<id>.md` regular files from the anchored source checkout; refuse symlink escapes and literal macOS/Linux user-home paths matching `/(Users|home)/[^/[:space:]]+`, without masking or changing dispatched bytes.
    87	For each id use `sqlite3 -readonly "$HOME/.agents/skills/agmsg/db/messages.db"` and the `messages` columns `from_agent`, `body`, `id`: select the greatest id from `claude-deep-dot` whose body starts with the exact tokens `AGMSG-TASK v1` and has exactly one `task_id=<id>` token; require exactly one `task_sha256=<64 hex>` token, never an older fallback or another sender. Compare full sha256 with the file; missing, malformed or unequal dispatch data exits 2 naming the task, `dispatched=<hash-or-missing/invalid>` and `local=<hash>`. Validate all requested inputs before worktree, commit, push or PR mutations; unreadable store/files fail closed.
    88	Snapshot validated bytes under the trusted root, recheck snapshot hashes and the latest dispatch rows immediately before committing, and copy those bytes rather than reopening mutable sources; a later mismatch stops before commit/push/PR and leaves the worktree for inspection. Create `.claude/worktrees/records-sync-<suffix>` with `git worktree add --no-track -b records/sync-dispatched-texts-<suffix> <path> origin/main`; reuse only that registered worktree on that exact branch with a clean tree; require the proposed PR diff to contain only the named text paths. Refuse collisions, dirty trees and unrequested changes without resetting or deleting anything; the worktree is a proposal output, never a trusted executable or approval input. Stage exactly the named texts and verify their staged blob sha256 values; no blanket add, masker, task-copy directory or unrelated records.
    89	Commit with `-c commit.gpgsign=false` and an English message listing every text and its first 12 sha256 hex digits. Push using `GIT_CONFIG_GLOBAL=/dev/null git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push https://github.com/mryfmo/dotfiles.git HEAD:records/sync-dispatched-texts-<suffix>`. Create the PR with `gh pr create --repo mryfmo/dotfiles --base main --head <branch>` and an English title/body, or find that branch's existing open PR in this repository and update its body with `gh pr edit <number> --repo mryfmo/dotfiles --body-file <file>`; query errors are failures, not absence. The English body has a Markdown table of every text and its 12-digit sha256 prefix and the exact sentence `This PR is records-only.`; use a body file. An unchanged repeat skips an empty commit and refreshes the existing PR body. Print the PR URL and full 40-hex head; never merge, enable auto-merge, update another branch or push main.
    90	Apply the frozen trusted-entrypoint contract, including the trusted clean parent and `#!/bin/bash -p`; resolve git and gh once to absolute regular executables from clean `PATH=/usr/bin:/bin` plus anchored mise install directories, never shims or a caller-supplied executable directory, and execute those resolved paths throughout. Bind every gh call explicitly to `mryfmo/dotfiles` and github.com: use `--hostname github.com` where accepted, fixed `repos/mryfmo/dotfiles/...` API paths, and `--repo github.com/mryfmo/dotfiles` for PR calls when needed to bind the host; a hostile GH_HOST must not redirect them. The credential helper must reach the same validated gh through the clean PATH. Do not source the agmsg storage layer or copy executable-resolution helpers into new files; use existing trusted helpers where available and block on an unmet prerequisite. English shdoc comments include `@file`, `@brief`, `@description`, `@arg` and `@exitcode`.
    91	
    92	## Check
    93	
    94	Write `tests/unit/test_records_sync.py`, ending in `unittest.main()`, with `RecordsSyncTest`: `test_sha_mismatch`, `test_missing_row`, `test_home_path`, `test_happy_path`, `test_body_table`, `test_reuse`, `test_bad_arguments`, `test_host_binding`, `test_replaced_input` and `test_trusted_exec_contract`. Use fake gh, fake sqlite3 or a Python-built temporary SQLite store, and a temporary bare origin; fixture transport captures the fixed HTTPS push and redirects only inside the fixture, with no production remote/executable override. Assert exit 2 and both hash fields with no mutation for hash/missing-row refusals; home-path and argument refusals also exit 2 before mutations; cover multiple tasks, latest amendment, wrong sender, exact id boundaries, malformed hashes and both home-path forms. Verify committed paths equal the named texts, copied bytes/hashes match, signing is disabled, push arguments are fixed, the body table/sentence are complete, reuse edits the existing PR, and no merge command occurs. The contract test covers hostile PATH shims, planted GIT_* and git config, worker-root trusted inputs, and replacement between validation and use; reuse the shared contract helper if present, otherwise keep fixtures in this module. Each new behavior is red before implementation (including the absent-script run) and green after; report.md names the tests and both runs.
    95	Run exactly `/usr/bin/env -i PATH="$(dirname "$(command -v uv)"):/usr/bin:/bin" HOME="$HOME" TMPDIR="$TMPDIR" HTTPS_PROXY="${HTTPS_PROXY-}" HTTP_PROXY="${HTTP_PROXY-}" NO_PROXY="${NO_PROXY-}" LANG=C.UTF-8 "$HOME/.local/share/mise/installs/python/3.15.0/bin/python3" -I tests/unit/test_records_sync.py` from the checkout root; no discovery. Run `shellcheck scripts/orchestrator/records-sync.sh`, `shfmt -d scripts/orchestrator/records-sync.sh`, `ruff check tests/unit/test_records_sync.py` and `ruff format --check tests/unit/test_records_sync.py`; paste commands, complete outputs and exit codes into validation.md. Caps: at most 160 changed lines outside `tests/` and `.orchestration/`; at most 300 changed lines under `tests/`, measured as additions plus deletions with `git diff --numstat <base40>...<head40>` (base pasted at dispatch; head from RESULT). No Bats locally; verify final-head GitHub Actions and fix in-scope failures before RESULT.
    96	
    97	## Completion
    98	
    99	Use a fresh `tools/records-sync-pr-a01` branch from `origin/main`. Keep `.orchestration/dotfiles-T133-records-sync-pr-a01/task.md` byte-identical to the dispatched text; put report.md, validation.md, sandbox.md, learning.md and autoskill.md beside it, with red/green selectors, full heads, command outputs, sandbox refusals, learning/AutoSkill status and `cost:`. Worker Playbook step 4 applies to every command: stay inside the sandbox; a refusal means `AGMSG-PONG v1 task_id=dotfiles-T133-records-sync-pr-a01 status=blocked` with the exact command and boundary, never escalation. No live records-sync run is required; tests must not contact GitHub.
   100	Push the implementation branch with `GIT_CONFIG_GLOBAL=/dev/null git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push -u https://github.com/mryfmo/dotfiles.git <branch>` and open its PR with `gh pr create --repo mryfmo/dotfiles` using an English title/body and the same explicit host binding. Follow Worker Playbook step 15 and the repository's agent review evidence/gate rules, then send `AGMSG-RESULT v1 task_id=dotfiles-T133-records-sync-pr-a01 status=ready_for_review pr=<url> head=<40-hex> task_copy=<sha256>` with the artifact paths. The script and worker never merge: written operator approval and `gh pr merge --repo mryfmo/dotfiles --squash --match-head-commit <audited-head40>` remain orchestrator actions (design 5.14 item 8; D-024-33). Residual risk: local bus hashes detect stale bytes, not a malicious same-UID writer or approval authority.
   101	
   102	## Checks (pasted by the orchestrator before each send)
   103	
   104	```
   105	```

exec
/bin/zsh -lc 'git status --short; git rev-parse HEAD; cat .ua/meta.json; nl -ba .orchestration/learning/mistakes/M-20261020-02-boundary-carried-pre-dispatch-snapshots.md' in /Users/a0004262/Workspace/dotfiles
exec
/bin/zsh -lc "python3 -c 'import json; d=json.load(open(\".ua/knowledge-graph.json\")); print(json.dumps([n for n in d.get(\"nodes\",[]) if any(s in str(n.get(\"filePath\",\"\")) for s in (\"trusted\",\"records-sync\",\"agent-config\",\"regime-ci\"))],ensure_ascii=False)[:22000])'" in /Users/a0004262/Workspace/dotfiles
exec
/bin/zsh -lc "rg -n '5\\.14|D-024-(21|29|30|33)|trusted|shim|acceptance|review' .orchestration/plans/024-design-quality.md; command -v crit; crit status --json" in /Users/a0004262/Workspace/dotfiles
 succeeded in 259ms:
 M .orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a06.md
 M .orchestration/acceptance/dotfiles-T129-normalised-comparison-lint-followup-a02.md
 M .orchestration/acceptance/dotfiles-T133-loop-limits-a01.md
 M .orchestration/acceptance/dotfiles-T133-record-ledger-carry-a01.md
 M .orchestration/acceptance/dotfiles-T133-regime-ci-followup-a01.md
 M .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a04.md
 M .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a02.md
 M .orchestration/decisions.tsv
 M .orchestration/learning/corrections-inventory.tsv
 M .orchestration/plans/024-design-quality.md
 M .orchestration/plans/024-progress.tsv
 M .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a06.md
 M .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a07.md
 M .orchestration/tasks/dotfiles-T129-assets-omp-hcom-followup-a06.md
 M .orchestration/tasks/dotfiles-T133-loop-limits-a01.md
 M .orchestration/tasks/dotfiles-T133-record-ledger-carry-a01.md
 M .orchestration/tasks/dotfiles-T133-trusted-exec-contract-tests-a01.md
 M .orchestration/tasks/dotfiles-T133-worker-write-boundary-a02.md
 M .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-chain-34cc889.log
 M .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-crit.json
 M .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-pr-feedback.json
 M .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-review-receipt.md
 M .orchestration/validation/dotfiles-T129-assets-omp-hcom-followup-a04-pr-feedback.json
 M .orchestration/validation/dotfiles-T129-assets-omp-hcom-followup-a05-pr-feedback.json
 M .orchestration/validation/dotfiles-T129-normalised-comparison-lint-followup-a02-pr-feedback.json
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
?? .orchestration/acceptance/dotfiles-T129-assets-omp-hcom-followup-a06.md
?? .orchestration/acceptance/dotfiles-T129-normalised-comparison-lint-followup-a04.md
?? .orchestration/acceptance/dotfiles-T133-permission-guard-gate-a05-slice1.md
?? .orchestration/acceptance/dotfiles-T133-python-pin-a01.md
?? .orchestration/acceptance/dotfiles-T133-python-pin-a02.md
?? .orchestration/acceptance/dotfiles-T133-record-json-sync-a01.md
?? .orchestration/acceptance/dotfiles-T133-records-sync-pr-a01.md
?? .orchestration/acceptance/dotfiles-T133-regime-ci-fixture-grammar-a01.md
?? .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a05-checker.md
?? .orchestration/acceptance/dotfiles-T133-trusted-exec-contract-tests-a01.md
?? .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a03.md
?? .orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a02/
?? .orchestration/dotfiles-T131-claude-pinned-merge-gate-review-a01/
?? .orchestration/dotfiles-T133-ci-efficiency-a01/task.md
?? .orchestration/dotfiles-T133-result-precheck-a01/
?? .orchestration/dotfiles-T133-result-precheck-a02/
?? .orchestration/dotfiles-T133-verdict-audit-pool-a01/
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a01/
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a02/
?? .orchestration/dotfiles-T133-worker-cap-hookspath-followup-a01/
?? .orchestration/learning/mistakes/M-20261020-01-amendment-note-reproduces-refused-string.md
?? .orchestration/learning/mistakes/M-20261020-02-boundary-carried-pre-dispatch-snapshots.md
?? .orchestration/learning/mistakes/M-20261020-03-dispatch-after-failed-script.md
?? .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md
?? .orchestration/tasks/dotfiles-T129-normalised-comparison-lint-followup-a04.md
?? .orchestration/tasks/dotfiles-T129-normalised-comparison-lint-followup-a05.md
?? .orchestration/tasks/dotfiles-T133-permission-guard-gate-a05-slice1.md
?? .orchestration/tasks/dotfiles-T133-python-pin-a01.md
?? .orchestration/tasks/dotfiles-T133-python-pin-a02.md
?? .orchestration/tasks/dotfiles-T133-python-pin-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-record-json-sync-a01.md
?? .orchestration/tasks/dotfiles-T133-records-sync-pr-a01.md
?? .orchestration/tasks/dotfiles-T133-regime-ci-fixture-grammar-a01.md
?? .orchestration/tasks/dotfiles-T133-regime-ci-fixture-grammar-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a05-checker.md
?? .orchestration/tasks/dotfiles-T133-trusted-exec-contract-tests-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-a03.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-followup-a01.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-audit-34cc889.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-audit-34cc889.md.last.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-audit-af86233.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-audit-af86233.md.last.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-chain-af86233.log
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-local-review-af86233.md
?? .orchestration/validation/dotfiles-T133-permission-guard-gate-a05-slice1-text-security-1293d6b.md
?? .orchestration/validation/dotfiles-T133-permission-guard-gate-a05-slice1-text-security-1293d6b.md.last.md
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
?? .orchestration/validation/dotfiles-T133-python-pin-a02-text-security-68fd5f2.md
?? .orchestration/validation/dotfiles-T133-python-pin-a02-text-security-68fd5f2.md.last.md
?? .orchestration/validation/dotfiles-T133-python-pin-a02-text-security-906e395.md
?? .orchestration/validation/dotfiles-T133-python-pin-a02-text-security-906e395.md.last.md
?? .orchestration/validation/dotfiles-T133-record-json-sync-a01-text-security-4e3ec93.md
?? .orchestration/validation/dotfiles-T133-record-ledger-carry-a01-text-security-f3bfcc6.md
?? .orchestration/validation/dotfiles-T133-record-ledger-carry-a01-text-security-f3bfcc6.md.last.md
?? .orchestration/validation/dotfiles-T133-records-sync-pr-a01-text-security-801ad66.md
?? .orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a01-chain-cd47e1b.log
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-audit-7a201ea.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-audit-7a201ea.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-chain-7a201ea.log
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-chain-e68fb33.log
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-crit.json
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-local-review-7a201ea.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-review-receipt.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a05-checker-text-security-1368f71.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a05-checker-text-security-1368f71.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a05-checker-text-security-cd37b74.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a05-checker-text-security-cd37b74.md.last.md
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-audit-9545e59.md
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-audit-9545e59.md.last.md
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-chain-25dd01e.log
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-chain-9545e59.log
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-chain-a2f4744.log
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-chain-b3c5076.log
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-crit.json
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-local-review-9545e59.md
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-local-review-b3c5076.md
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-review-receipt.md
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
60a6fb2b324d0381c4a6e539b37c650105154a7e
{
  "lastAnalyzedAt": "2026-10-02T14:12:51Z",
  "gitCommitHash": "940a3a2b07adfd14140a0acff96784ef53a0a509",
  "version": "1.0.0",
  "analyzedFiles": 368
}
     1	---
     2	id: M-20261020-02
     3	date: 2026-10-20
     4	classes: [hash-binding, records-form]
     5	severity: P2
     6	---
     7	
     8	# Boundary 25 carried task texts older than their dispatched bytes
     9	
    10	**What happened.** The regime verifier (`scripts/orchestrator/regime-ci.py`) treats the base's `.orchestration/tasks/<task>.md` as the dispatched policy and refuses a PR whose task copy differs from it. PR #436's update-branched head b3c50768 failed `regime` (run 39364553764, 2026-10-20T03:29Z) because main's text of `dotfiles-T133-trusted-exec-contract-tests-a01` lacks the `dispatch to a011 …` line pasted into its Checks block before the 23:29:38Z dispatch (task_sha256 dd754911…, which the worker's copy and the local text both equal). Boundary 25 (#435) was committed at 00:19:29Z from a file copy made earlier in the boundary's long preparation (masker, validator and push retries), and `dotfiles-T133-loop-limits-a01` was dispatched at 00:55:43Z, after the commit; both texts on main are pre-dispatch snapshots. Fix: records PR #438 (`records/sync-dispatched-texts-26`) replaces both with the dispatched bytes.
    11	
    12	**What the rules say.** Design 5.14 item 8: the committed records are the authority, read at the 40-hex sha; regime-ci reads the policy from the base. C-87/C-100: figures and prerequisites are run, not recalled.
    13	
    14	**Why the rules did not fire.** Nothing compared the boundary's copies with the bus: the boundary script copied files, masked paths and validated, but never checked that an in-flight task text equalled the `task_sha256` of its latest `AGMSG-TASK` message, and nothing re-copied after the preparation stalled.
    15	
    16	**Mechanism.** Before a boundary pushes, it lists every in-flight task (`AGMSG-TASK` messages on the bus without a merged PR) and refuses when the sha256 of the copied `.orchestration/tasks/<task>.md` differs from the latest `task_sha256` dispatched for that task, printing both; the copy step runs immediately before the commit. Glue first (`boundary-26` preparation), tracked home `scripts/orchestrator/boundary.sh` (the boundary lineage's follow-up text). Corollary for planning: every post-dispatch amendment implies a records PR before the worker's PR can pass `regime`, so amendments are batched and their records PR is opened as soon as the amendment is dispatched.

 succeeded in 260ms:
[{"id": "config:home/dot_agents/agent-config.yaml", "type": "config", "name": "agent-config.yaml", "filePath": "home/dot_agents/agent-config.yaml", "summary": "Canonical hand-edited manifest for Codex and Claude Code: model profiles (express/standard/review/deep/security/audit/adh), herdr-agents worker kind/profile/worktree, Codex and Claude settings, sandboxes, permissions, hooks, plugins, disabled-by-default MCP servers, and pinned install assets. All agent-native config files are rendered from it.", "tags": ["configuration", "single-source-of-truth", "agent-configuration", "model-profiles", "security"], "complexity": "complex", "languageNotes": "Embeds chezmoi template placeholders such as {{ .chezmoi.homeDir }} inside YAML string values, resolved later by the generator and chezmoi."}, {"id": "file:scripts/generate-agent-configs.py", "type": "file", "name": "generate-agent-configs.py", "filePath": "scripts/generate-agent-configs.py", "summary": "Generator that renders agent-native configuration (Codex config.toml, Claude settings/sandbox/MCP, plugin marketplace, model-profile TOML and modify scripts, profiles env, express-explorer agent, asset pin constants) from home/dot_agents/agent-config.yaml, with --check and --set-asset modes.", "tags": ["code-generation", "agent-config", "manifest", "toml", "cli", "tested"], "complexity": "complex"}, {"id": "function:scripts/generate-agent-configs.py:parse_manifest", "type": "function", "name": "parse_manifest", "filePath": "scripts/generate-agent-configs.py", "lineRange": [43, 54], "summary": "Parses the agent manifest YAML with PyYAML, failing clearly when PyYAML is missing or the document is not a mapping.", "tags": ["parsing", "yaml", "manifest"], "complexity": "simple"}, {"id": "function:scripts/generate-agent-configs.py:quote_toml", "type": "function", "name": "quote_toml", "filePath": "scripts/generate-agent-configs.py", "lineRange": [61, 79], "summary": "Serializes Python scalars, lists, and tables into TOML literal syntax.", "tags": ["serialization", "toml", "utility"], "complexity": "simple"}, {"id": "function:scripts/generate-agent-configs.py:model_profiles", "type": "function", "name": "model_profiles", "filePath": "scripts/generate-agent-configs.py", "lineRange": [112, 141], "summary": "Validates the model_profiles mapping (required express/standard profiles, claude/codex fields) and returns it.", "tags": ["validation", "model-profiles", "manifest"], "complexity": "simple"}, {"id": "function:scripts/generate-agent-configs.py:set_asset_field", "type": "function", "name": "set_asset_field", "filePath": "scripts/generate-agent-configs.py", "lineRange": [210, 235], "summary": "Rewrites one scalar under assets.<name> in the manifest text while preserving comments and layout.", "tags": ["manifest", "text-rewrite", "pins"], "complexity": "simple"}, {"id": "function:scripts/generate-agent-configs.py:render_asset_constants", "type": "function", "name": "render_asset_constants", "filePath": "scripts/generate-agent-configs.py", "lineRange": [238, 258], "summary": "Rewrites each asset's NAME=\"...\" pin assignment in its render target file (e.g. installer-pins.sh), enforcing plain pin values and exactly one assignment.", "tags": ["code-generation", "pins", "supply-chain"], "complexity": "simple"}, {"id": "function:scripts/generate-agent-configs.py:render_codex", "type": "function", "name": "render_codex", "filePath": "scripts/generate-agent-configs.py", "lineRange": [261, 399], "summary": "Renders the managed Codex config.toml: models, sandbox and writable roots, features, hooks, MCP servers, plugins, and projects.", "tags": ["code-generation", "codex", "toml"], "complexity": "complex"}, {"id": "function:scripts/generate-agent-configs.py:render_claude_sandbox", "type": "function", "name": "render_claude_sandbox", "filePath": "scripts/generate-agent-configs.py", "lineRange": [402, 422], "summary": "Renders the Claude sandbox settings block, reusing the Codex agmsg writable roots for allowWrite.", "tags": ["code-generation", "claude-code", "sandbox"], "complexity": "simple"}, {"id": "function:scripts/generate-agent-configs.py:render_claude_settings", "type": "function", "name": "render_claude_settings", "filePath": "scripts/generate-agent-configs.py", "lineRange": [425, 508], "summary": "Renders the managed Claude Code settings JSON: hooks, permissions, sandbox, env, plugins, statusline, and model defaults.", "tags": ["code-generation", "claude-code", "settings"], "complexity": "complex"}, {"id": "function:scripts/generate-agent-configs.py:claude_mcp_entry", "type": "function", "name": "claude_mcp_entry", "filePath": "scripts/generate-agent-configs.py", "lineRange": [511, 529], "summary": "Builds one Claude MCP server entry for stdio or HTTP transports from the manifest definition.", "tags": ["mcp", "claude-code", "serialization"], "complexity": "simple"}, {"id": "function:scripts/generate-agent-configs.py:render_marketplace", "type": "function", "name": "render_marketplace", "filePath": "scripts/generate-agent-configs.py", "lineRange": [543, 561], "summary": "Renders the local Codex plugin marketplace JSON from manifest plugin entries.", "tags": ["code-generation", "codex", "plugins"], "complexity": "simple"}, {"id": "function:scripts/generate-agent-configs.py:render_codex_plugin", "type": "function", "name": "render_codex_plugin", "filePath": "scripts/generate-agent-configs.py", "lineRange": [564, 582], "summary": "Renders one managed Codex plugin manifest, failing when required plugin keys are missing.", "tags": ["code-generation", "codex", "plugins"], "complexity": "simple"}, {"id": "function:scripts/generate-agent-configs.py:claude_skill_symlink_outputs", "type": "function", "name": "claude_skill_symlink_outputs", "filePath": "scripts/generate-agent-configs.py", "lineRange": [594, 611], "summary": "Produces chezmoi symlink_ outputs mirroring every shared skill file into home/dot_claude/skills.", "tags": ["code-generation", "skills", "symlinks"], "complexity": "simple"}, {"id": "function:scripts/generate-agent-configs.py:render_codex_profile", "type": "function", "name": "render_codex_profile", "filePath": "scripts/generate-agent-configs.py", "lineRange": [615, 636], "summary": "Renders a per-profile Codex TOML (model, reasoning effort, notify) launched via `codex --profile <name>`.", "tags": ["code-generation", "codex", "model-profiles"], "complexity": "simple"}, {"id": "function:scripts/generate-agent-configs.py:render_codex_profile_modify", "type": "function", "name": "render_codex_profile_modify", "filePath": "scripts/generate-agent-configs.py", "lineRange": [639, 805], "summary": "Generates a chezmoi modify_ Python script that merges the managed profile keys into an existing ~/.codex/<profile>.config.toml without clobbering user keys.", "tags": ["code-generation", "chezmoi", "modify-script", "codex"], "complexity": "complex"}, {"id": "function:scripts/generate-agent-configs.py:render_model_profiles_env", "type": "function", "name": "render_model_profiles_env", "filePath": "scripts/generate-agent-configs.py", "lineRange": [808, 829], "summary": "Renders the model-profiles.env shell fragment (interactive profile, worker kind/profile/worktree, per-profile CLI args) for agent launchers.", "tags": ["code-generation", "model-profiles", "shell-env"], "complexity": "simple"}, {"id": "function:scripts/generate-agent-configs.py:render_claude_express_agent", "type": "function", "name": "render_claude_express_agent", "filePath": "scripts/generate-agent-configs.py", "lineRange": [832, 850], "summary": "Renders the express-explorer Claude subagent definition pinned to the express profile model.", "tags": ["code-generation", "claude-code", "subagent"], "complexity": "simple"}, {"id": "function:scripts/generate-agent-configs.py:expected_outputs", "type": "function", "name": "expected_outputs", "filePath": "scripts/generate-agent-configs.py", "lineRange": [853, 875], "summary": "Collects every generated output path and rendered content derived from the manifest.", "tags": ["code-generation", "outputs", "orchestrator"], "complexity": "simple"}, {"id": "function:scripts/generate-agent-configs.py:remove_stale_generated_outputs", "type": "function", "name": "remove_stale_generated_outputs", "filePath": "scripts/generate-agent-configs.py", "lineRange": [878, 893], "summary": "Deletes generated files and empty directories under home/dot_claude/skills that are no longer expected.", "tags": ["cleanup", "code-generation", "skills"], "complexity": "simple"}, {"id": "function:scripts/generate-agent-configs.py:main", "type": "function", "name": "main", "filePath": "scripts/generate-agent-configs.py", "lineRange": [912, 979], "summary": "CLI entry handling --set-asset pin rewrites, --check drift verification, stale output removal, and writing all generated files.", "tags": ["entry-point", "cli", "code-generation"], "complexity": "moderate"}]

 succeeded in 303ms:
9:| S1 | orchestrator の受け入れ判定と最終マージが 1 席の直列 | P1-4〜P1-6 の後、1 RESULT の受け入れは verdict ファイル確認 + 記録生成 + `gh pr merge` で約 2〜5 分 → 12〜20 件/時。6 席が同時に RESULT を出すと最大 30 分待ち | 受け入れは RESULT 到着順で 1 件ずつ、判定に要る情報は P1-5 の precheck 証跡と review verdict に集約して読む量を固定。第 2 段階 H3 で review verdict を両ベンダーの席が返す。受け入れ権限は orchestrator に残す（rules） | 受け入れ待ち時間の分布を bus 履歴から出す（RESULT → ACCEPTANCE の時刻差） |
28:| Q5 | PR あたりの push 回数を減らす | P1-5 の precheck（local review・unit・render-check を RESULT 前に）で revise ラウンドを減らす。目標: PR 1 本の CI run ≤ 3 | revise 率 ≤ 20%（DoD-P1-f） | — |
29:| Q6 | Codex Bot | 自動 review は Codex 側設定のまま（P0/P1 のみ）。chain は Bot を待たない（repo rule: optional、never gated）。sweep は最終 head の 1 回、`scripts/pr-feedback.py` で全スレッドを取得し、disposition は `PR_FEEDBACK_EVIDENCE` の gate で必須のまま。review 直後は数秒待って再取得（race）。GitHub 上の解決は不要（D2） | Bot の所見は 1 件残らず disposition（fixed か not-applicable）。品質装置としては強化されこそすれ弱まらない | learn.chatgpt.com/docs/third-party/github、pr-integration rule |
43:| M4 | タスク文の作成（10〜20 分）と presend チェッカーの往復（最大 107 分） | `task-from-plan.py`: todo の 1 行から task.md の骨格を生成。allowed_files は `git grep` で触れる箇所を列挙して提案、premises は command を実行して output を貼る（recall しない）、trust-boundary ファイルなら threat_table の雛形を 1 行ずつ出す。`task-consistency-check.py` に 3 つの形の規則（test selector、sentence、owning task id）と threat_table の単位規則を追加し、レビュー席の 1 ラウンドは trust-boundary タスクだけに | premises が実行結果になる。チェッカーがレビューで繰り返し出た指摘を吸収（mistakes into mechanisms） | タスク文 3〜5 分、presend 失敗ほぼ 0、review 席の往復が減る | 採用。新 P1-12 |
64:| Q-D 品質指標を gate に | 連続 2 波ごとに計測し、閾値を超えたらマージ凍結と根本原因の記録（plan 第 7 節 STOP に追加済み）: main の push CI 赤 ≤ 1 回/2 波（かつ根本原因が記録されている）、マージ後 24 時間以内の hotfix PR（escaped defect）= 0、監査 P0/P1 のマージ後検出 = 0、revise 率 ≤ 20%、disposition の not-applicable 比率 ≤ 30%（高ければ Bot の所見を軽視している兆候として review） | 024-checklists.md P1-j、P1-k、progress.tsv の列 |
87:| 〃 | 内容のレビュー（threat の見落とし、制御の妥当性） | AI（独立モデル、1 ラウンド固定） | 既存の headless review（Codex review profile）を `security: true` のタスクだけに限定。停止条件は SKILL の既定 | 既存 |
95:### 5.14 残余（凍結後の計測事実、D-024-29）
99:5.12 **プログラム仕様** は `024-design-programs.md` に分離（17 項目: verdict.sh、audit-pool.sh と orch-audit.sh --json、schemas、result-precheck.sh、dispositions.py、regime.yml、dispatch.sh --next、acceptance-front-matter.py、git hooks、handoff.sh、flakes、task-from-plan.py）。
103:## 5.14 信頼ホスト実行契約（trusted-host execution contract、D-024-18）
107:1. **書き込み境界（前提 6、ランタイム別に正直に）** Claude worker 席は専用の設定ディレクトリ `CLAUDE_CONFIG_DIR=~/.claude-worker`（chezmoi が描画、operator が一度 login）で起動し、orchestrator の `~/.claude` と設定を共有しない。worker 設定：除外コマンド無し、Herdr socket 無し、sandbox の allowWrite は自席 worktree と agmsg store と席別キャッシュだけ、`failIfUnavailable: true`、信頼パス（anchored checkout の `.claude/worktrees/` 以外、`~/.agents`、`~/.claude*`、`~/.local`、`~/.config`）への Edit deny（公式文書：file tool の permission 検査は要求パスと symlink 解決後のパスの両方に deny を適用し、symlink そのものへの書き込みは拒否する）、sandbox の強制範囲はユーザー設定ではなく **managed settings**（`/Library/Application Support/ClaudeCode/managed-settings.json`、公式文書 "Repository settings under an admin-required sandbox"：project/local 設定は sandbox を無効化したり除外・socket を足したりできない）に置く。chezmoi は user ではこのファイルを書けないので、描画した内容を操作者が `sudo` で一度配置する（操作者手順）。worker 設定は worktree 自身の `.claude/**` と `.mcp.json` への Edit deny（`//<anchored>/.claude/worktrees/*/.claude/**`）を持つ（Bash 側は sandbox 既定の settings/hooks の denyWithinAllow）。agmsg store（全席が書く）から配送 hook が driver や plugin を source する上流の経路（storage.sh の `drivers.partition` traversal、`db/trusted-plugins` と `plugins/partition/shared.sh` による差し替え承認）は別タスク（agmsg hardening）の行で、worker 設定は `~/.agents/skills/agmsg/plugins/**` と `~/.agents/skills/agmsg/db/trusted-plugins` への書き込みを deny し（Edit deny は sandbox の deny にも合流する）、hook 側は store 由来の設定値を検証するまで残余と書く。managed settings の配置先は OS で異なる（macOS `/Library/Application Support/ClaudeCode/managed-settings.json`、Linux `/etc/claude-code/managed-settings.json`）。hook は agmsg 配送だけを、hook コマンドを `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<home> …` で始めて（`BASH_ENV` などの継承環境を bash 起動前に消す；PATH 固定だけでは BASH_ENV が先に走る）絶対パスのインタプリタで呼び（上流の agmsg スクリプトは `/usr/bin/env bash` の shebang を持つので、hook 実行環境の PATH が shim を含まないことで束縛する）、各 hook に `onFailure: "block"`。公式文書：linked worktree の session は **main checkout の `.claude/settings.local.json` を読む**ので、worker 向けの hook を worktree の settings.local.json に書いても読まれず、逆に orchestrator の local hooks が worker session でも走る。したがって orchestrator 側の local hooks も guard 経由にし、worker 側の hook は worker config dir の settings に置く。Edit deny の一覧は `git ls-tree` ではなく描画時の静的一覧（manifest に列挙、`.agents/worklog/**` と `.agents/worklog/uv-cache/**` を含む）とし、`~/.agents/**` の全面 deny は agmsg store の書き込みと矛盾するので、`~/.agents/agent-config.yaml`、`~/.agents/skills/**/scripts/**`、`~/.agents/model-profiles.env` などストア以外を列挙する。公式文書で確認した事実（2026-10-19）：`Edit(path)` の deny は Write/MultiEdit/NotebookEdit にも効き、deny → ask → allow の順で最初の一致が決まる；ただし Read/Edit の deny は **Bash sandbox の設定にも合流する**（"Paths and domains from both sandbox settings and permission rules are merged into the final sandbox configuration"）ので、ユーザー設定（全席共有）に `.orchestration/**` の Edit deny を書くと orchestrator の Bash による記録書き込みも止まる。hook は起動時に固定されず、設定ファイルの編集は file watcher が即座に反映する。`sandbox.failIfUnavailable` の既定は fail-open（依存が無ければ sandbox 無しで実行）。したがって Claude 席の境界は Edit deny 規則ではなく、**ユーザーレベルの PreToolUse hook**（`~/.claude/hooks/worker-write-boundary`、chezmoi が描画、`/bin/sh` または絶対パスの `python3 -I`）で作る：cwd の realpath が `<anchored>/.claude/worktrees/` 配下の session では、Write/Edit/MultiEdit/NotebookEdit の対象が cwd の外、または `<cwd>/.claude/**`・`<cwd>/.mcp.json` のとき `permissionDecision: deny` を返す。Bash 側は sandbox の既定 `denyWithinAllow`（settings、hooks）と `allowWrite`（自席 worktree）が担う。`failIfUnavailable: true` を全席に置く。 Codex 席は sandbox（workspace-write）がツールの書き込み全部を自席の worktree と列挙パスに限る。Claude 席は Seatbelt sandbox が Bash を限るだけで、Write/Edit/MultiEdit/NotebookEdit、hook、MCP プロセスは sandbox 外で動き、permission policy（permgate の決定論ポリシー）が path で拒否しない限り anchored checkout や `~/.agents` にも書ける（2026-10-19 時点、描画済み設定にその deny は無い）。したがって前提 6 は「Codex 席は成立、Claude 席は P1-15 が描画設定に Edit の path deny を入れるまで残余」と書く。P1-15 以前に「worker は信頼ルートに書けない」と書く文は誤りで、C-80 が拒否する。P1-15 が入るまで、承認の出所は項目 8 の「コミット済み台帳」で守る。書き込みは自席の worktree（`.claude/worktrees/<name>`）、scratch、列挙されたツールキャッシュに限る。anchored checkout（`.claude/worktrees/` 以外）、`~/.agents/agent-config.yaml`、`~/.claude/hooks`、信頼ルートのバイナリ、orchestrator の証跡・スナップショット・lock は worker から書けない。render テストが描画後の deny を検証する。残余は「どの席 sandbox にも属さない同一 UID プロセス」と、Worker Playbook step 4 が sandbox 外に出す少数のコマンド（gh）。後者は D-024-17（P1-15）で絶対パスの実行体に束縛する。 The protected-path inventory a seat's Edit denies cover is enumerated from the inputs of every trusted executable, not only the executables: it includes `~/.agents/permgate-policy.yaml` (permgate rereads it for every decision), `~/.local/lib/python*/site-packages` and every other user-site or startup-hook location of the interpreters in use (`.pth`, `usercustomize.py`, `sitecustomize.py`), `~/.claude-worker`'s hook and settings files, and the rendered guard; a text that binds an executable names its inputs in the same inventory (P1-15 amendment 5 C-80, 2026-10-19). The inventory of executable configuration sources a worker start screens is the documented loading list of the installed Claude Code version, enumerated once from the documentation (settings: user, project, local and managed `settings.json`; project `.mcp.json`; the configuration directory's global state `.claude.json` with user-scoped and project-local MCP servers; plugins and skills directories (`.claude/skills/*/.claude-plugin/plugin.json`, enabled plugins); hook handlers of every documented type (`command`, `http` and any other `type` value the hooks reference lists: a handler is an executable input whether it names a command or a URL, and a worker start refuses every handler type but `command`), `apiKeyHelper`, `statusLine.command`, MCP server commands), and the launcher screens or disables every source before accepting workspace trust, refusing any executable payload it did not write; adding sources one review at a time is the anti-pattern (P1-15 a02 reviews 2ae9e2c and ebbb71b, 2026-10-19). The enumeration quotes the documentation's values (the page, its fetched_at and the listed values) in the text's premises so a reviewer can check them against the live page; naming a source by one of its fields ("hook commands" for hook handlers) is the same anti-pattern one level down (a02 review b2a186e, 2026-10-19T20:36Z; C-95).
108:2. **無害化した環境を最初に** 最初の処理として `env -i` に入り、PATH は信頼ルートで解決した絶対バイナリへのリンクだけの私設ディレクトリ（shims、空、相対は拒否）。git は毎回 `GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null -c core.hooksPath=/dev/null -c core.fsmonitor=false -c protocol.allow=never -c protocol.https.allow=always` と明示 `-C`（https だけ許す。`protocol.allow=never` 単独は必要な fetch を止める）。 検査の読み取りは `GIT_NO_LAZY_FETCH=1` で部分クローンの遅延 fetch（checkout 設定の credential.helper を起動しうる）を止め、`-c submodule.recurse=false --ignore-submodules=all` で submodule 内の status/diff（submodule 自身の設定が filter を有効化しうる）を止める。`.gitmodules` を持つ checkout は検査対象として拒否する。 `-C` は作業木を束縛しないので（repo-local の `core.worktree` が読み先を checkout 外へ向けられる）、git は `--git-dir=<checkout>/.git --work-tree=<checkout>` を明示し、`git rev-parse --show-toplevel` の realpath が checkout と一致しないときは拒否する。 premise や検査の「コマンド実行」は、固定語彙の読み取り専用プローブ（`git rev-parse <ref>`、`test -e <path>`、`grep -c <pattern> <file>` のように検査器自身が解釈する形）だけを許し、任意のシェル文字列は実行しない（本文のハッシュはコマンド文を認証するだけで、`python -I scripts/x.py` のファイル被演算子や `source ./x.sh` の中身は認証しない）。diff と show は `--no-ext-diff --no-textconv` と `-c core.attributesFile=/dev/null -c core.sshCommand=false` を付け、PR 側の `.gitattributes`（external diff、textconv、filter）が検査内容や実行物を変えないようにする。Python は `-I`。PATH 探索で実行するものは無い。 A shell script that runs under a PR-controlled or worker-controlled environment (verdict.sh, the chain glue, CI steps) is executed as a program with `#!/bin/bash -p`, never as `bash <file>`, and only by a trusted parent that supplies the clean environment before the exec: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<passwd home> LANG=C.UTF-8 /bin/bash --noprofile --norc -p <absolute script path> …` (long options before `-p`). Privileged mode discards inherited functions, `BASH_ENV`/`ENV`, `SHELLOPTS`, `BASHOPTS`, `CDPATH` and `GLOBIGNORE`, but on Linux an inherited `LD_PRELOAD`/`LD_AUDIT` already executes while the loader maps `/bin/bash`, before `-p` or any statement runs, so a self re-exec inside the script is not a boundary and re-executing `"$0"` would reopen the caller's pathname (a worker-owned symlink can be swapped between the two executions); the program therefore verifies and refuses instead of repairing: its environment must consist of exactly the allowed names (checked through absolute paths `/usr/bin/env`, `/usr/bin/grep`), `$0` resolved with `realpath` must be a regular file under the repository root, and HOME must equal the passwd home of the real uid (`/usr/bin/dscl . -read /Users/<user> NFSHomeDirectory` on macOS, `/usr/bin/getent passwd <uid>` on Linux), otherwise exit 2 with a named message. A caller-set sentinel variable is not a sanitization proof, because the caller controls it (ci-efficiency a04 and verdict a04 C-80 reviews, 2026-10-19). No script accepts a caller-supplied executable directory; interpreters are the fixed absolute paths item 9 names.
113:0. **脅威モデル（D-024-21）** 席は同じ OS ユーザで動き、ホストは席間の信頼境界ではない（同一 UID のプロセスは symlink 差し替え、共有 `.git` の object 差し替え、hook の子プロセス、Herdr socket 経由の host 実行で、ホスト内のどの検査も迂回できる）。regime の硬い境界は GitHub（保護された main、必須チェック、orchestrator の identity によるマージ）。ただしこの境界は **worker 席が orchestrator の GitHub 資格情報を共有しない**ときだけ成立する（D-024-22：worker 席は専用の GitHub identity（別アカウントまたは App のトークン）で `gh` に login し、ruleset の bypass 一覧に入らない。orchestrator の keychain トークンを worker の config dir に持ち込まない。identity が分かれるまで「GitHub が境界」は未成立と書く）。**同一 macOS ユーザでは資格情報は分離できない**（gh は keychain の項目を host/user で引き、同じ UID の gh は orchestrator のトークンを読める。`GH_CONFIG_DIR` は設定を分けるだけ）。防止には worker 席を別の OS ユーザ（または別ホスト）で動かすしかなく、それは D-024-23 の将来項目（P1-16、操作者の判断）。それまで GitHub 境界は **検知**で守る：記録は boundary の記録 PR まで main に無いので、検知は次の記録 PR の regime ジョブで行う（`.orchestration/acceptance/**` に触れる PR で、前回 boundary 以降の main の各マージ commit に、gate 通過の証跡を持つ受け入れ記録が対応することを検査し、無ければその PR を失敗させる；P1-11 owner a02 の行 `ci:detection:1`）。main push 時点の検知は記録が無いので不可能であり、文は「次の記録 PR で検知、防止ではない」と書く。悪意ある worker に耐えるべき入力（承認台帳、gate が読む証跡 of record）は GitHub から sha 指定で API 経由（sandbox 内）に読み、ローカルファイルやローカル object database からは読まない。ホスト内の制御（本節 1〜10）は事故と prompt injection による損害の抑制であり、文はそう書く。
114:8. **承認はコミット済み台帳から読む** permission の決定行（`scope=permission approved_by=user diff_sha256=…`）は anchored checkout の作業コピーではなく、コミット済みの台帳から読む。読み方は `git ls-remote origin refs/heads/main` が返す commit sha を取り、GitHub API（`gh api repos/<owner>/<repo>/contents/.orchestration/decisions.tsv?ref=<sha>`、sandbox 内）でその sha の内容を取得する。ローカルの `git show` は共有 object database が書けるため中間 tree の差し替えで偽物を返しうる（第 3 回審査の所見 2）（ローカルの ref 名 `origin/main` は経由しない。`refs/replace/` も書けるので replacement を無効にする。Codex worker は `.git/objects` と `.git/refs` に書けるので ref は差し替えられるが、sha で指した object は内容アドレスで偽造できない）。作業コピーの行は提案で、記録 PR が main にマージされて初めて承認になる（PR の承認は操作者の操作）。偽造には main へのマージが要る。 The same applies to the PR content a mechanism evaluates (the verdict, the audit precheck, the counters): the changeset is read from GitHub at the 40-hex head (`gh api repos/{owner}/{repo}/compare/<base40>...<head40>`, `…/contents/<path>?ref=<head40>`) or from a private clone whose object store no worker can write; the main checkout's shared `.git/objects` and its `origin/main` ref are not evidence sources, because Codex workers write them (a04 C-80 round 1, 2026-10-19). Evidence files are named and matched by the full 40-hex head, never by a 7-character prefix. Every `gh` invocation names the repository explicitly: `gh pr`, `gh run` and `gh issue` subcommands take `--repo mryfmo/dotfiles` or the full pull-request URL, and `gh api` (which has no `--repo` flag) takes the explicit `repos/mryfmo/dotfiles/…` endpoint path, never a `{owner}/{repo}` placeholder; a `gh api graphql` call binds the repository through fixed query variables (`owner: "mryfmo"`, `name: "dotfiles"` as constants in the script, passed with `-f`/`-F`) and uses only node ids obtained from a query bound by those variables (verdict a04 C-80 round 5, 2026-10-19): the local repository configuration selects the default repository otherwise, and a matching head sha does not bind the repository because a fork can hold the same commit (verdict a04 C-80 round 2, 2026-10-19). A mechanism whose application path runs code this contract does not yet cover (the agmsg storage layer sourced by `dispatch.sh`/`history.sh`; the integration gate until its own hardening task lands) names that task as the prerequisite of its `--apply` mode and runs shadow-only until the prerequisite is merged. The sha of canonical `main` comes from the fixed repository's API (`gh api repos/mryfmo/dotfiles/git/ref/heads/main --jq .object.sha`), never from `git ls-remote origin`, whose destination the local remote and URL-rewrite configuration control (P1-12 a04 C-80, 2026-10-19T20:01Z); the content read at that sha comes from `repos/mryfmo/dotfiles/contents/<path>?ref=<sha40>`. Every `gh api` call that decides also binds the host with `--hostname github.com` (`GH_HOST` and the hosts configuration select the API host otherwise), a subcommand binds it through the `github.com/mryfmo/dotfiles` form of `--repo`, and a test that exports a hostile `GH_HOST` shows the call still names github.com or refuses (a02 review b2a186e, 2026-10-19T20:36Z).
115:9. **私設キャッシュ** orchestrator 側の実行は worker と共有するキャッシュ（`~/.cache/uv`、`~/.local/share/uv`、mise）から実行可能物を読まない。`UV_CACHE_DIR` を anchored checkout 配下（`.agents/worklog/uv-cache`、gitignored、worker 書き込み不可）に固定し、`uv run --no-config --no-project --offline --python <信頼ルートの絶対パスのインタプリタ>` で起動する（`--no-config` で uv の設定探索を止め、`--python` の絶対パスで cwd や親の `.venv` の発見を止める；敵対的な `.venv` と `uv.toml` を置いた fixture で検証）。hook は uv を使わず jq と python 標準ライブラリだけで動く。 One trusted interpreter resolver (`scripts/orchestrator/trusted-interpreter.sh`, P1-3 lineage) resolves `<abs>` from the repository's pinned declaration to a regular file under the tool manager's install root (the install root is anchored to the passwd home of the real uid, never to the HOME variable, which a caller can forge), refuses anything else, and every orchestrator-side script consumes it; no script keeps its own `command -v`, `mise which` or PATH fallback (ci-rerun.sh security review 44cb835, 2026-10-19). Shell code of other projects (the agmsg storage layer and its `drivers.partition` sourcing) is never sourced by an orchestrator-side mechanism; counters are read from the agmsg SQLite store read-only with a fixed query or from the pasted record. Every Python child of a trusted entrypoint runs with `-I` (isolated: no user site, no `PYTHON*` environment, no script directory on `sys.path`), so `uv run … python -I <script>` rather than `--script` for a script without declared dependencies; a test plants a `.pth` and a `usercustomize.py` in a fake user site and asserts they never execute (P1-15 amendment 5 C-80, 2026-10-19). A program takes `UV_CACHE_DIR` from the environment the trusted parent supplies and refuses when it is absent or not an absolute path; it never computes a default from its own root. The orchestrator's parent prefix sets the main checkout's `.agents/worklog/uv-cache`; a worker's launcher sets `<worktree>/.uv-cache` (the P1-15 worker launch value: `.agents/` is read-only in the Codex permission profile, so a root-derived `.agents/worklog/uv-cache` cannot be created by a worker; P1-12 a03, 2026-10-19T11:28Z); tests set a temporary directory.
117:7. **検証** threat_table は本節の項目 1〜10 に 1 行ずつ対応させる（参照だけでは足りない）。共通テスト補助 `tests/unit/trusted_exec_contract.py`（P1-6 で作る）を使い、仕組みごとに 4 つの red→green テストを持つ：PATH 先頭の shim が実行されない、植え付けた GIT_* と git 設定が効かない、worker ルート配下の信頼パスが拒否される、検証後に差し替えたファイルが消費側に届かない。
/Users/a0004262/.local/bin/crit
{
  "branch": "main",
  "daemon": {
    "running": false
  },
  "review_file": "/Users/a0004262/.crit/reviews/c06a520c1f9b/review.json",
  "review_file_exists": false,
  "sessions": [],
  "vcs": "git"
}

**Setting time budget and focus**
exec
/bin/zsh -lc "git diff --name-only 940a3a2b07adfd14140a0acff96784ef53a0a509..HEAD -- scripts home tests; cat .orchestration/acceptance/dotfiles-T133-trusted-exec-contract-tests-a01.md .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a03.md; rg -n 'excludedCommands|gh|GIT_CONFIG|PATH|shim' home/dot_agents/agent-config.yaml scripts/orchestrator/trusted-interpreter.sh tests/unit/trusted_exec_contract.py" in /Users/a0004262/Workspace/dotfiles
exec
/bin/zsh -lc "sed -n '101,118p' .orchestration/plans/024-design-quality.md; rg -n 'D-024-(21|29|30|33)' .orchestration/decisions.tsv; cat .orchestration/acceptance/dotfiles-T133-records-sync-pr-a01.md .orchestration/validation/dotfiles-T133-records-sync-pr-a01-text-security-801ad66.md" in /Users/a0004262/Workspace/dotfiles
 succeeded in 52ms:
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
67:D-024-21	2026-10-19T04:0xZ	threat model and mechanism of the worker boundary: the host is not a security boundary between seats sharing one OS user; the hard boundary is GitHub (protected main, required checks, the orchestrator identity merge); approvals and gate evidence of record are read from GitHub at a sha through the API inside the sandbox; Claude worker seats run under their own CLAUDE_CONFIG_DIR (~/.claude-worker: no excluded commands, no Herdr socket, Edit denies on trusted paths with symlink coverage, failIfUnavailable true, minimal trusted hooks with onFailure block); host-local controls target accidental and injected damage and the texts say so (design 5.14 items 0, 1, 8)	three C-80 reviews of the P1-15 text (03:24Z, 03:42Z, 03:58Z) found host-level escapes no in-process check closes (symlink swap race, writable object database, hook descendants through shims, Herdr socket RPC, hook timeout fail-open); the documentation confirms per-directory settings and credentials (one operator login for the worker directory), onFailure block (>= 2.1.295; installed 2.1.300), and symlink-aware file-tool deny rules	default under the autonomy directive, reported 2026-10-19 13:0x JST; the worker-directory login is an operator step at the P1-15 deployment; scope=design,permission	applied-to-the-P1-15-text
77:D-024-29	2026-10-19T21:39Z	Design 5.14 is frozen (plan 006 A1: three review rounds, then freeze with a residual list): items 0-10 are the contract; a text review finding that needs a new design sentence is recorded in the design's residual list and as an owner row, not as an amendment of the item and of the text under review, unless it names a P0/P1 that is exploitable in the proposed implementation.	items 1, 2, 3, 8 and 9 were amended five times on 10-19/20 (one per review round of P1-15 and P1-12), each amendment re-opening the texts that quote the item (C-88) and costing a review round each; the texts chased a moving design.	plan 006 A1; M-20261019-05; C-92	applied from 06:40 JST; the residual list is a new subsection `5.14 残余` in 024-design-quality.md (written at the next design edit)
78:D-024-30	2026-10-19T23:16Z	A task text applies design 5.14 by reference: it names the items it relies on (`design: 5.14 items 2, 3, 8, 9`) and carries one threat row per item 0-10 in the item's own words, never a restated or paraphrased copy of the item; C-88 is narrowed to the exact contract sentences a test asserts; the task-consistency check gains a rule (C16) that a security: true orchestrator-side text names 5.14 and has the per-item rows (owner: the P1-12 follow-up after a04 frees task-consistency-check.py).	restated design text drifted in every reset text and re-opened a review round at each design amendment (P1-15: 23 review rounds; P1-12: 4); by-reference texts stay within proposal 1's caps and a mechanical check replaces the reviewer's paraphrase comparison; the operator's direction of 2026-10-19T22:59Z (relayed by a011) asks for the same.	plan 006 A1; D-024-29; M-20261019-05; proposal 1	applied from 08:15 JST to new texts (trusted-exec-contract-tests-a01 first); existing correct texts are not rewritten
81:D-024-33	2026-10-20T03:07Z	Records boundary PR #435 (head 8f7b97690df6060a73959a06fc6622a2beaf5029) is approved by the operator's written instruction in the orchestrator session at 2026-10-20 12:0x JST ("承認するので作業を継続"); the orchestrator merges it with gh pr merge --squash --match-head-commit 8f7b9769… right after PR #431 merges (or at once if #431 fails or resets), so the P1-15 chain and audit already running at edd824ea are not invalidated by a base move.	design 5.14 item 8 makes the operator's approval the authority of the recorded decisions (D-024-25..32); GitHub's ruleset 24397953 has no approval rule (rules: deletion, non_fast_forward, required_status_checks), so the written instruction is the operative approval; sequencing after #431 saves one CI run and one re-audit on the critical path.	design 5.14 item 8; ruleset 24397953; the 11:55 JST report	applied; merge pending #431
82:D-024-34	2026-10-20T04:12Z	The files the worker's loader consumes at start and the regime need not preserve are launcher-generated at every start: the global state file `CLAUDE_CONFIG_DIR/.claude.json` is written from the declared shape (empty `mcpServers`, `projects` with exactly the validated identities and Boolean trust, `hasCompletedOnboarding: true`) plus identity fields carried from the previous file after screening (`oauthAccount` string members, `userID`); native persisted state (`numStartups`, onboarding, tips and changelog caches, per-project history, allowedTools, cost counters) is neither screened nor preserved; refusal with a named message stays for declared-structure violations (non-empty top-level `mcpServers`, undeclared project keys, non-Boolean trust flags, undeclared object or array members), as evidence of tampering. `CLAUDE_ENV_FILE` (amendment 1) belongs to the same family. A loader that requires another preserved field blocks and retasks (the text's rule), never widens silently.	a010's probe of the installed loader (2.1.300, sha256 475517ca…; reproduced by the orchestrator at 04:10Z) shows the loader itself writes fields outside any exact schema, so the allowlist re-plan's closed schema (D-024-29/30 lineage, a02 -> a03) refuses the worker's own state at the next start; a per-version native-field table would block every loader update until re-probed; generating the file realises design 5.14 item 1 (refuse any executable payload it did not write) by writing the whole file. Second re-plan of the input-inventory family (rows text-security:f7af699:1, worker:5067ed0:1 after the allowlist re-plan).	design 5.14 item 1; D-024-29; D-024-30; a03 record rows; M-20261019-05	applied 13:12 JST as a03 amendment 2 (review-profile text, C-80 round 3); the operator may redirect it once per class (the 13:15 JST report)
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
  "task": "dotfiles-T133-records-sync-pr-a01"
}
---

# Acceptance record: dotfiles-T133-records-sync-pr-a01

- 2026-10-20T06:24Z: text written whole by the review profile from the orchestrator's brief (`dotfiles-T133-records-sync-pr-a01-prompt.md`; security: true; the mechanism of M-20261020-02: scripts/orchestrator/records-sync.sh verifies each dispatched text against the bus task_sha256 and opens or updates the records-sync PR (never merges)); trailing authoring commentary stripped by the orchestrator; pre-send.sh: checker OK, SECRET_PATTERN 0, home paths 0; sha256 801ad66b… before the Checks paste. C-80 round 1 running; dispatch to an idle Claude seat after a correct verdict (files disjoint from every in-flight task).
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
session id: 01a157fb-a7e5-78e2-be1a-0bb16df04a27
--------
user
Pre-dispatch security review (read-only, security profile) of the task text .orchestration/tasks/dotfiles-T133-records-sync-pr-a01.md and its threat_table, before any implementation exists. Judge the design the text states: can the controls it names bind what actually executes on this host (mise shims first on PATH, same-user worker processes, gh outside the sandbox on Linux, symlinks and case-insensitive filesystems, inherited GIT_* environment)? Check every threat row: a closed row whose named test cannot close it, a residual row whose control does not mitigate the risk, a missing row for a file or non-path control, and any gap of the class decision-not-bound-to-execution (a decision made on text or on a validated copy while the execution resolves binaries, files or ledgers from an attacker-influenced place). Read the related acceptance records and reviews the text cites for context. Report each finding as [P0-P3] <confidence> <file:line> <one line>; findings are input for the orchestrator, who decides. End with exactly one line: Verdict: correct or Verdict: incorrect.
warning: loading hooks from both /Users/a0004262/.codex/hooks.json and /Users/a0004262/.codex/config.toml; prefer a single representation for this layer
hook: SessionStart
hook: SessionStart
hook: SessionStart Completed
hook: SessionStart Completed
hook: UserPromptSubmit
hook: UserPromptSubmit Completed
codex
🤖 I read the AGENTS.md for mryfmo/dotfiles.
`agmsg-orchestration` と Ponytail のレビュー手順を読み、タスク本文・脅威表・参照記録を読み取り専用で確認します。制御の判断と、このホストで実際に実行される対象が結び付いているかを重点的に調べます。
exec
/bin/zsh -lc 'cat /Users/a0004262/.agents/skills/agmsg-orchestration/SKILL.md /Users/a0004262/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail/SKILL.md /Users/a0004262/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail-review/SKILL.md' in /Users/a0004262/Workspace/dotfiles
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
/bin/zsh -lc 'nl -ba .orchestration/tasks/dotfiles-T133-records-sync-pr-a01.md' in /Users/a0004262/Workspace/dotfiles
 succeeded in 0ms:
     1	---
     2	format: 2
     3	task_id: dotfiles-T133-records-sync-pr-a01
     4	kind: code
     5	security: true
     6	allowed_files:
     7	  - scripts/orchestrator/records-sync.sh
     8	  - tests/unit/test_records_sync.py
     9	  - .orchestration/dotfiles-T133-records-sync-pr-a01/**
    10	after: []
    11	threat_table:
    12	  - control: the PR edits scripts/orchestrator/records-sync.sh
    13	    disposition: "closed: tests/unit/test_records_sync.py::RecordsSyncTest::test_happy_path"
    14	  - control: the PR edits tests/unit/test_records_sync.py
    15	    disposition: "residual: fixtures use temporary repositories and fake service executables; the audit checks that assertions exercise the production script without contacting GitHub"
    16	  - control: the PR edits .orchestration/dotfiles-T133-records-sync-pr-a01/**
    17	    disposition: "residual: this directory holds task data and evidence only; the audit checks its complete diff and rejects executable payloads"
    18	  - control: the task copy .orchestration/dotfiles-T133-records-sync-pr-a01/task.md
    19	    disposition: "residual: the orchestrator compares all bytes and sha256 with the dispatched text at acceptance"
    20	  - control: the evidence records report.md, validation.md, sandbox.md, learning.md and autoskill.md
    21	    disposition: "residual: evidence is a claim until checked against command output, the diff and final-head CI; refusals and omissions stay visible"
    22	  - control: task metadata
    23	    disposition: "residual: the task-consistency checker parses the front matter before dispatch and acceptance; the task-copy comparison detects metadata changes"
    24	  - control: metadata separators
    25	    disposition: "residual: the checker parses the first YAML document and the byte comparison covers separators and the complete task text"
    26	  - control: in-process effects
    27	    disposition: "residual: production creates a dedicated proposal branch and PR; development uses fixture transports and never runs a live records sync"
    28	  - control: workflow and interpreter or environment inputs
    29	    disposition: "residual: no workflow or interpreter configuration is editable; design 5.14 governs the trusted parent and executable inputs"
    30	  - control: new or renamed scripts
    31	    disposition: "closed: tests/unit/test_records_sync.py::RecordsSyncTest::test_happy_path"
    32	  - control: orchestrator effect merge
    33	    disposition: "residual: the script never merges or queues auto-merge; written operator approval and the head-bound integration command remain with the orchestrator"
    34	  - control: orchestrator effect update-branch
    35	    disposition: "residual: only the orchestrator updates an implementation PR; a moved head requires fresh CI, feedback sweep and audit before the gate"
    36	  - control: orchestrator effect forced worker removal
    37	    disposition: "residual: none is requested; only herdr-agents removes a worker and any forced discard is recorded by the orchestrator"
    38	  - control: "design 5.14 item 0: 脅威モデル（D-024-21）"
    39	    disposition: "residual: same-UID writers can forge bus rows and local objects; these checks suppress mistakes, while approval stays with the orchestrator and detection is at the next records PR, not prevention"
    40	  - control: "design 5.14 item 1: 書き込み境界（前提 6、ランタイム別に正直に）"
    41	    disposition: "residual: seat configuration enforces its actual boundary; this task neither changes permissions nor claims isolation from other same-UID host processes"
    42	  - control: "design 5.14 item 2: 無害化した環境を最初に"
    43	    disposition: "closed: tests/unit/test_records_sync.py::RecordsSyncTest::test_trusted_exec_contract"
    44	  - control: "design 5.14 item 3: 信頼パスの境界検査"
    45	    disposition: "closed: tests/unit/test_records_sync.py::RecordsSyncTest::test_trusted_exec_contract"
    46	  - control: "design 5.14 item 4: 検証したものを実行し、検証した内容を渡す"
    47	    disposition: "closed: tests/unit/test_records_sync.py::RecordsSyncTest::test_replaced_input"
    48	  - control: "design 5.14 item 5: 出力と予約の同一性"
    49	    disposition: "residual: suffixes identify proposal branches, not approval evidence; record the full head and serialize invocations for each suffix, with no merge-slot reservation"
    50	  - control: "design 5.14 item 6: 正直な残余"
    51	    disposition: "residual: local sender and hash checks do not authenticate the shared store; the report states this limit and any unverified contract prerequisite"
    52	  - control: "design 5.14 item 7: 検証"
    53	    disposition: "closed: tests/unit/test_records_sync.py::RecordsSyncTest::test_trusted_exec_contract"
    54	  - control: "design 5.14 item 8: 承認はコミット済み台帳から読む"
    55	    disposition: "residual: origin/main seeds a proposal only; local task texts and bus rows grant no permission or merge approval, and every GitHub operation binds the fixed repository and host"
    56	  - control: "design 5.14 item 9: 私設キャッシュ"
    57	    disposition: "residual: consume the frozen executable-resolution contract, never source agmsg shell code or execute shims; any unavailable trusted prerequisite is a blocked PONG"
    58	  - control: "design 5.14 item 10: worker は sandbox 外でコマンドを実行しない（D-024-17 の改訂）"
    59	    disposition: "residual: every worker command, including gh and push, stays inside its sandbox; a refusal is recorded and reported without escalation"
    60	premises:
    61	  - claim: regime-ci uses the base's dispatched task text as policy, so each dispatch or amendment must reach main before its implementation PR can pass regime
    62	    command: |-
    63	      sed -n '7p' scripts/orchestrator/regime-ci.py
    64	    output: |-
    65	      on the base's dispatched text, the copy against the dispatched `.orchestration/tasks/<t>.md` at the base, whose text is the policy
    66	  - claim: the three supplied records-sync commits list the dispatched texts carried in PR 438
    67	    command: |-
    68	      git show -s --format='%h %s' 8bf7e6ac c58cf432 88add881
    69	    output: |-
    70	      8bf7e6ac chore(orchestration): sync the dispatched task texts of trusted-exec-contract-tests-a01 and loop-limits-a01 to main
    71	      c58cf432 chore(orchestration): add the dispatched texts of lint-followup-a04 and task-generator-plan-check-a05-checker
    72	      88add881 chore(orchestration): add the dispatched texts of chain-review a07, python-pin a01/a02 and worker-write-boundary a03
    73	  - claim: the repository's dispatch sender is claude-deep-dot; a body claiming to be the orchestrator is insufficient
    74	    command: |-
    75	      sqlite3 -readonly "$HOME/.agents/skills/agmsg/db/messages.db" "SELECT from_agent,COUNT(*) FROM messages WHERE from_agent='claude-deep-dot' AND body LIKE 'AGMSG-TASK v1 %' GROUP BY from_agent;"
    76	    output: |-
    77	      claude-deep-dot|594
    78	---
    79	
    80	# AGMSG-TASK dotfiles-T133-records-sync-pr-a01 — synchronize dispatched task texts through a records-only PR
    81	
    82	Read `.orchestration/learning/mistakes/M-20261020-02-boundary-carried-pre-dispatch-snapshots.md`: boundary preparation copied pre-dispatch bytes and never compared them with the bus; this task implements its records-sync corollary, not the separate boundary-wide in-flight scan. Design `.orchestration/plans/024-design-quality.md` 5.14 items 0–10 apply by reference, especially items 2, 3, 4, 7, 8 and 9; the design is frozen by D-024-29 and is not restated or amended here (D-024-30).
    83	
    84	## Item 1
    85	
    86	Write executable `scripts/orchestrator/records-sync.sh <branch-suffix> <task-id>...`. Require at least one distinct task id; accept only nonempty alphanumeric-led tokens containing alphanumerics, hyphens or underscores, so no option, traversal, SQL or ref injection is possible. Read only the named `.orchestration/tasks/<id>.md` regular files from the anchored source checkout; refuse symlink escapes and literal macOS/Linux user-home paths matching `/(Users|home)/[^/[:space:]]+`, without masking or changing dispatched bytes.
    87	For each id use `sqlite3 -readonly "$HOME/.agents/skills/agmsg/db/messages.db"` and the `messages` columns `from_agent`, `body`, `id`: select the greatest id from `claude-deep-dot` whose body starts with the exact tokens `AGMSG-TASK v1` and has exactly one `task_id=<id>` token; require exactly one `task_sha256=<64 hex>` token, never an older fallback or another sender. Compare full sha256 with the file; missing, malformed or unequal dispatch data exits 2 naming the task, `dispatched=<hash-or-missing/invalid>` and `local=<hash>`. Validate all requested inputs before worktree, commit, push or PR mutations; unreadable store/files fail closed.
    88	Snapshot validated bytes under the trusted root, recheck snapshot hashes and the latest dispatch rows immediately before committing, and copy those bytes rather than reopening mutable sources; a later mismatch stops before commit/push/PR and leaves the worktree for inspection. Create `.claude/worktrees/records-sync-<suffix>` with `git worktree add --no-track -b records/sync-dispatched-texts-<suffix> <path> origin/main`; reuse only that registered worktree on that exact branch with a clean tree; require the proposed PR diff to contain only the named text paths. Refuse collisions, dirty trees and unrequested changes without resetting or deleting anything; the worktree is a proposal output, never a trusted executable or approval input. Stage exactly the named texts and verify their staged blob sha256 values; no blanket add, masker, task-copy directory or unrelated records.
    89	Commit with `-c commit.gpgsign=false` and an English message listing every text and its first 12 sha256 hex digits. Push using `GIT_CONFIG_GLOBAL=/dev/null git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push https://github.com/mryfmo/dotfiles.git HEAD:records/sync-dispatched-texts-<suffix>`. Create the PR with `gh pr create --repo mryfmo/dotfiles --base main --head <branch>` and an English title/body, or find that branch's existing open PR in this repository and update its body with `gh pr edit <number> --repo mryfmo/dotfiles --body-file <file>`; query errors are failures, not absence. The English body has a Markdown table of every text and its 12-digit sha256 prefix and the exact sentence `This PR is records-only.`; use a body file. An unchanged repeat skips an empty commit and refreshes the existing PR body. Print the PR URL and full 40-hex head; never merge, enable auto-merge, update another branch or push main.
    90	Apply the frozen trusted-entrypoint contract, including the trusted clean parent and `#!/bin/bash -p`; resolve git and gh once to absolute regular executables from clean `PATH=/usr/bin:/bin` plus anchored mise install directories, never shims or a caller-supplied executable directory, and execute those resolved paths throughout. Bind every gh call explicitly to `mryfmo/dotfiles` and github.com: use `--hostname github.com` where accepted, fixed `repos/mryfmo/dotfiles/...` API paths, and `--repo github.com/mryfmo/dotfiles` for PR calls when needed to bind the host; a hostile GH_HOST must not redirect them. The credential helper must reach the same validated gh through the clean PATH. Do not source the agmsg storage layer or copy executable-resolution helpers into new files; use existing trusted helpers where available and block on an unmet prerequisite. English shdoc comments include `@file`, `@brief`, `@description`, `@arg` and `@exitcode`.
    91	
    92	## Check
    93	
    94	Write `tests/unit/test_records_sync.py`, ending in `unittest.main()`, with `RecordsSyncTest`: `test_sha_mismatch`, `test_missing_row`, `test_home_path`, `test_happy_path`, `test_body_table`, `test_reuse`, `test_bad_arguments`, `test_host_binding`, `test_replaced_input` and `test_trusted_exec_contract`. Use fake gh, fake sqlite3 or a Python-built temporary SQLite store, and a temporary bare origin; fixture transport captures the fixed HTTPS push and redirects only inside the fixture, with no production remote/executable override. Assert exit 2 and both hash fields with no mutation for hash/missing-row refusals; home-path and argument refusals also exit 2 before mutations; cover multiple tasks, latest amendment, wrong sender, exact id boundaries, malformed hashes and both home-path forms. Verify committed paths equal the named texts, copied bytes/hashes match, signing is disabled, push arguments are fixed, the body table/sentence are complete, reuse edits the existing PR, and no merge command occurs. The contract test covers hostile PATH shims, planted GIT_* and git config, worker-root trusted inputs, and replacement between validation and use; reuse the shared contract helper if present, otherwise keep fixtures in this module. Each new behavior is red before implementation (including the absent-script run) and green after; report.md names the tests and both runs.
    95	Run exactly `/usr/bin/env -i PATH="$(dirname "$(command -v uv)"):/usr/bin:/bin" HOME="$HOME" TMPDIR="$TMPDIR" HTTPS_PROXY="${HTTPS_PROXY-}" HTTP_PROXY="${HTTP_PROXY-}" NO_PROXY="${NO_PROXY-}" LANG=C.UTF-8 "$HOME/.local/share/mise/installs/python/3.15.0/bin/python3" -I tests/unit/test_records_sync.py` from the checkout root; no discovery. Run `shellcheck scripts/orchestrator/records-sync.sh`, `shfmt -d scripts/orchestrator/records-sync.sh`, `ruff check tests/unit/test_records_sync.py` and `ruff format --check tests/unit/test_records_sync.py`; paste commands, complete outputs and exit codes into validation.md. Caps: at most 160 changed lines outside `tests/` and `.orchestration/`; at most 300 changed lines under `tests/`, measured as additions plus deletions with `git diff --numstat <base40>...<head40>` (base pasted at dispatch; head from RESULT). No Bats locally; verify final-head GitHub Actions and fix in-scope failures before RESULT.
    96	
    97	## Completion
    98	
    99	Use a fresh `tools/records-sync-pr-a01` branch from `origin/main`. Keep `.orchestration/dotfiles-T133-records-sync-pr-a01/task.md` byte-identical to the dispatched text; put report.md, validation.md, sandbox.md, learning.md and autoskill.md beside it, with red/green selectors, full heads, command outputs, sandbox refusals, learning/AutoSkill status and `cost:`. Worker Playbook step 4 applies to every command: stay inside the sandbox; a refusal means `AGMSG-PONG v1 task_id=dotfiles-T133-records-sync-pr-a01 status=blocked` with the exact command and boundary, never escalation. No live records-sync run is required; tests must not contact GitHub.
   100	Push the implementation branch with `GIT_CONFIG_GLOBAL=/dev/null git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push -u https://github.com/mryfmo/dotfiles.git <branch>` and open its PR with `gh pr create --repo mryfmo/dotfiles` using an English title/body and the same explicit host binding. Follow Worker Playbook step 15 and the repository's agent review evidence/gate rules, then send `AGMSG-RESULT v1 task_id=dotfiles-T133-records-sync-pr-a01 status=ready_for_review pr=<url> head=<40-hex> task_copy=<sha256>` with the artifact paths. The script and worker never merge: written operator approval and `gh pr merge --repo mryfmo/dotfiles --squash --match-head-commit <audited-head40>` remain orchestrator actions (design 5.14 item 8; D-024-33). Residual risk: local bus hashes detect stale bytes, not a malicious same-UID writer or approval authority.
   101	
   102	## Checks (pasted by the orchestrator before each send)
   103	
   104	```
   105	```

exec
/bin/zsh -lc 'git status --short; git rev-parse HEAD; cat .ua/meta.json; nl -ba .orchestration/learning/mistakes/M-20261020-02-boundary-carried-pre-dispatch-snapshots.md' in /Users/a0004262/Workspace/dotfiles
exec
/bin/zsh -lc "python3 -c 'import json; d=json.load(open(\".ua/knowledge-graph.json\")); print(json.dumps([n for n in d.get(\"nodes\",[]) if any(s in str(n.get(\"filePath\",\"\")) for s in (\"trusted\",\"records-sync\",\"agent-config\",\"regime-ci\"))],ensure_ascii=False)[:22000])'" in /Users/a0004262/Workspace/dotfiles
exec
/bin/zsh -lc "rg -n '5\\.14|D-024-(21|29|30|33)|trusted|shim|acceptance|review' .orchestration/plans/024-design-quality.md; command -v crit; crit status --json" in /Users/a0004262/Workspace/dotfiles
 succeeded in 259ms:
 M .orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a06.md
 M .orchestration/acceptance/dotfiles-T129-normalised-comparison-lint-followup-a02.md
 M .orchestration/acceptance/dotfiles-T133-loop-limits-a01.md
 M .orchestration/acceptance/dotfiles-T133-record-ledger-carry-a01.md
 M .orchestration/acceptance/dotfiles-T133-regime-ci-followup-a01.md
 M .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a04.md
 M .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a02.md
 M .orchestration/decisions.tsv
 M .orchestration/learning/corrections-inventory.tsv
 M .orchestration/plans/024-design-quality.md
 M .orchestration/plans/024-progress.tsv
 M .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a06.md
 M .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a07.md
 M .orchestration/tasks/dotfiles-T129-assets-omp-hcom-followup-a06.md
 M .orchestration/tasks/dotfiles-T133-loop-limits-a01.md
 M .orchestration/tasks/dotfiles-T133-record-ledger-carry-a01.md
 M .orchestration/tasks/dotfiles-T133-trusted-exec-contract-tests-a01.md
 M .orchestration/tasks/dotfiles-T133-worker-write-boundary-a02.md
 M .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-chain-34cc889.log
 M .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-crit.json
 M .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-pr-feedback.json
 M .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-review-receipt.md
 M .orchestration/validation/dotfiles-T129-assets-omp-hcom-followup-a04-pr-feedback.json
 M .orchestration/validation/dotfiles-T129-assets-omp-hcom-followup-a05-pr-feedback.json
 M .orchestration/validation/dotfiles-T129-normalised-comparison-lint-followup-a02-pr-feedback.json
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
?? .orchestration/acceptance/dotfiles-T129-assets-omp-hcom-followup-a06.md
?? .orchestration/acceptance/dotfiles-T129-normalised-comparison-lint-followup-a04.md
?? .orchestration/acceptance/dotfiles-T133-permission-guard-gate-a05-slice1.md
?? .orchestration/acceptance/dotfiles-T133-python-pin-a01.md
?? .orchestration/acceptance/dotfiles-T133-python-pin-a02.md
?? .orchestration/acceptance/dotfiles-T133-record-json-sync-a01.md
?? .orchestration/acceptance/dotfiles-T133-records-sync-pr-a01.md
?? .orchestration/acceptance/dotfiles-T133-regime-ci-fixture-grammar-a01.md
?? .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a05-checker.md
?? .orchestration/acceptance/dotfiles-T133-trusted-exec-contract-tests-a01.md
?? .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a03.md
?? .orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a02/
?? .orchestration/dotfiles-T131-claude-pinned-merge-gate-review-a01/
?? .orchestration/dotfiles-T133-ci-efficiency-a01/task.md
?? .orchestration/dotfiles-T133-result-precheck-a01/
?? .orchestration/dotfiles-T133-result-precheck-a02/
?? .orchestration/dotfiles-T133-verdict-audit-pool-a01/
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a01/
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a02/
?? .orchestration/dotfiles-T133-worker-cap-hookspath-followup-a01/
?? .orchestration/learning/mistakes/M-20261020-01-amendment-note-reproduces-refused-string.md
?? .orchestration/learning/mistakes/M-20261020-02-boundary-carried-pre-dispatch-snapshots.md
?? .orchestration/learning/mistakes/M-20261020-03-dispatch-after-failed-script.md
?? .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md
?? .orchestration/tasks/dotfiles-T129-normalised-comparison-lint-followup-a04.md
?? .orchestration/tasks/dotfiles-T129-normalised-comparison-lint-followup-a05.md
?? .orchestration/tasks/dotfiles-T133-permission-guard-gate-a05-slice1.md
?? .orchestration/tasks/dotfiles-T133-python-pin-a01.md
?? .orchestration/tasks/dotfiles-T133-python-pin-a02.md
?? .orchestration/tasks/dotfiles-T133-python-pin-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-record-json-sync-a01.md
?? .orchestration/tasks/dotfiles-T133-records-sync-pr-a01.md
?? .orchestration/tasks/dotfiles-T133-regime-ci-fixture-grammar-a01.md
?? .orchestration/tasks/dotfiles-T133-regime-ci-fixture-grammar-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a05-checker.md
?? .orchestration/tasks/dotfiles-T133-trusted-exec-contract-tests-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-a03.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-followup-a01.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-audit-34cc889.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-audit-34cc889.md.last.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-audit-af86233.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-audit-af86233.md.last.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-chain-af86233.log
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-local-review-af86233.md
?? .orchestration/validation/dotfiles-T133-permission-guard-gate-a05-slice1-text-security-1293d6b.md
?? .orchestration/validation/dotfiles-T133-permission-guard-gate-a05-slice1-text-security-1293d6b.md.last.md
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
?? .orchestration/validation/dotfiles-T133-python-pin-a02-text-security-68fd5f2.md
?? .orchestration/validation/dotfiles-T133-python-pin-a02-text-security-68fd5f2.md.last.md
?? .orchestration/validation/dotfiles-T133-python-pin-a02-text-security-906e395.md
?? .orchestration/validation/dotfiles-T133-python-pin-a02-text-security-906e395.md.last.md
?? .orchestration/validation/dotfiles-T133-record-json-sync-a01-text-security-4e3ec93.md
?? .orchestration/validation/dotfiles-T133-record-ledger-carry-a01-text-security-f3bfcc6.md
?? .orchestration/validation/dotfiles-T133-record-ledger-carry-a01-text-security-f3bfcc6.md.last.md
?? .orchestration/validation/dotfiles-T133-records-sync-pr-a01-text-security-801ad66.md
?? .orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a01-chain-cd47e1b.log
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-audit-7a201ea.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-audit-7a201ea.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-chain-7a201ea.log
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-chain-e68fb33.log
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-crit.json
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-local-review-7a201ea.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-review-receipt.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a05-checker-text-security-1368f71.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a05-checker-text-security-1368f71.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a05-checker-text-security-cd37b74.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a05-checker-text-security-cd37b74.md.last.md
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-audit-9545e59.md
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-audit-9545e59.md.last.md
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-chain-25dd01e.log
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-chain-9545e59.log
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-chain-a2f4744.log
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-chain-b3c5076.log
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-crit.json
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-local-review-9545e59.md
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-local-review-b3c5076.md
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-review-receipt.md
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
60a6fb2b324d0381c4a6e539b37c650105154a7e
{
  "lastAnalyzedAt": "2026-10-02T14:12:51Z",
  "gitCommitHash": "940a3a2b07adfd14140a0acff96784ef53a0a509",
  "version": "1.0.0",
  "analyzedFiles": 368
}
     1	---
     2	id: M-20261020-02
     3	date: 2026-10-20
     4	classes: [hash-binding, records-form]
     5	severity: P2
     6	---
     7	
     8	# Boundary 25 carried task texts older than their dispatched bytes
     9	
    10	**What happened.** The regime verifier (`scripts/orchestrator/regime-ci.py`) treats the base's `.orchestration/tasks/<task>.md` as the dispatched policy and refuses a PR whose task copy differs from it. PR #436's update-branched head b3c50768 failed `regime` (run 39364553764, 2026-10-20T03:29Z) because main's text of `dotfiles-T133-trusted-exec-contract-tests-a01` lacks the `dispatch to a011 …` line pasted into its Checks block before the 23:29:38Z dispatch (task_sha256 dd754911…, which the worker's copy and the local text both equal). Boundary 25 (#435) was committed at 00:19:29Z from a file copy made earlier in the boundary's long preparation (masker, validator and push retries), and `dotfiles-T133-loop-limits-a01` was dispatched at 00:55:43Z, after the commit; both texts on main are pre-dispatch snapshots. Fix: records PR #438 (`records/sync-dispatched-texts-26`) replaces both with the dispatched bytes.
    11	
    12	**What the rules say.** Design 5.14 item 8: the committed records are the authority, read at the 40-hex sha; regime-ci reads the policy from the base. C-87/C-100: figures and prerequisites are run, not recalled.
    13	
    14	**Why the rules did not fire.** Nothing compared the boundary's copies with the bus: the boundary script copied files, masked paths and validated, but never checked that an in-flight task text equalled the `task_sha256` of its latest `AGMSG-TASK` message, and nothing re-copied after the preparation stalled.
    15	
    16	**Mechanism.** Before a boundary pushes, it lists every in-flight task (`AGMSG-TASK` messages on the bus without a merged PR) and refuses when the sha256 of the copied `.orchestration/tasks/<task>.md` differs from the latest `task_sha256` dispatched for that task, printing both; the copy step runs immediately before the commit. Glue first (`boundary-26` preparation), tracked home `scripts/orchestrator/boundary.sh` (the boundary lineage's follow-up text). Corollary for planning: every post-dispatch amendment implies a records PR before the worker's PR can pass `regime`, so amendments are batched and their records PR is opened as soon as the amendment is dispatched.

 succeeded in 260ms:
[{"id": "config:home/dot_agents/agent-config.yaml", "type": "config", "name": "agent-config.yaml", "filePath": "home/dot_agents/agent-config.yaml", "summary": "Canonical hand-edited manifest for Codex and Claude Code: model profiles (express/standard/review/deep/security/audit/adh), herdr-agents worker kind/profile/worktree, Codex and Claude settings, sandboxes, permissions, hooks, plugins, disabled-by-default MCP servers, and pinned install assets. All agent-native config files are rendered from it.", "tags": ["configuration", "single-source-of-truth", "agent-configuration", "model-profiles", "security"], "complexity": "complex", "languageNotes": "Embeds chezmoi template placeholders such as {{ .chezmoi.homeDir }} inside YAML string values, resolved later by the generator and chezmoi."}, {"id": "file:scripts/generate-agent-configs.py", "type": "file", "name": "generate-agent-configs.py", "filePath": "scripts/generate-agent-configs.py", "summary": "Generator that renders agent-native configuration (Codex config.toml, Claude settings/sandbox/MCP, plugin marketplace, model-profile TOML and modify scripts, profiles env, express-explorer agent, asset pin constants) from home/dot_agents/agent-config.yaml, with --check and --set-asset modes.", "tags": ["code-generation", "agent-config", "manifest", "toml", "cli", "tested"], "complexity": "complex"}, {"id": "function:scripts/generate-agent-configs.py:parse_manifest", "type": "function", "name": "parse_manifest", "filePath": "scripts/generate-agent-configs.py", "lineRange": [43, 54], "summary": "Parses the agent manifest YAML with PyYAML, failing clearly when PyYAML is missing or the document is not a mapping.", "tags": ["parsing", "yaml", "manifest"], "complexity": "simple"}, {"id": "function:scripts/generate-agent-configs.py:quote_toml", "type": "function", "name": "quote_toml", "filePath": "scripts/generate-agent-configs.py", "lineRange": [61, 79], "summary": "Serializes Python scalars, lists, and tables into TOML literal syntax.", "tags": ["serialization", "toml", "utility"], "complexity": "simple"}, {"id": "function:scripts/generate-agent-configs.py:model_profiles", "type": "function", "name": "model_profiles", "filePath": "scripts/generate-agent-configs.py", "lineRange": [112, 141], "summary": "Validates the model_profiles mapping (required express/standard profiles, claude/codex fields) and returns it.", "tags": ["validation", "model-profiles", "manifest"], "complexity": "simple"}, {"id": "function:scripts/generate-agent-configs.py:set_asset_field", "type": "function", "name": "set_asset_field", "filePath": "scripts/generate-agent-configs.py", "lineRange": [210, 235], "summary": "Rewrites one scalar under assets.<name> in the manifest text while preserving comments and layout.", "tags": ["manifest", "text-rewrite", "pins"], "complexity": "simple"}, {"id": "function:scripts/generate-agent-configs.py:render_asset_constants", "type": "function", "name": "render_asset_constants", "filePath": "scripts/generate-agent-configs.py", "lineRange": [238, 258], "summary": "Rewrites each asset's NAME=\"...\" pin assignment in its render target file (e.g. installer-pins.sh), enforcing plain pin values and exactly one assignment.", "tags": ["code-generation", "pins", "supply-chain"], "complexity": "simple"}, {"id": "function:scripts/generate-agent-configs.py:render_codex", "type": "function", "name": "render_codex", "filePath": "scripts/generate-agent-configs.py", "lineRange": [261, 399], "summary": "Renders the managed Codex config.toml: models, sandbox and writable roots, features, hooks, MCP servers, plugins, and projects.", "tags": ["code-generation", "codex", "toml"], "complexity": "complex"}, {"id": "function:scripts/generate-agent-configs.py:render_claude_sandbox", "type": "function", "name": "render_claude_sandbox", "filePath": "scripts/generate-agent-configs.py", "lineRange": [402, 422], "summary": "Renders the Claude sandbox settings block, reusing the Codex agmsg writable roots for allowWrite.", "tags": ["code-generation", "claude-code", "sandbox"], "complexity": "simple"}, {"id": "function:scripts/generate-agent-configs.py:render_claude_settings", "type": "function", "name": "render_claude_settings", "filePath": "scripts/generate-agent-configs.py", "lineRange": [425, 508], "summary": "Renders the managed Claude Code settings JSON: hooks, permissions, sandbox, env, plugins, statusline, and model defaults.", "tags": ["code-generation", "claude-code", "settings"], "complexity": "complex"}, {"id": "function:scripts/generate-agent-configs.py:claude_mcp_entry", "type": "function", "name": "claude_mcp_entry", "filePath": "scripts/generate-agent-configs.py", "lineRange": [511, 529], "summary": "Builds one Claude MCP server entry for stdio or HTTP transports from the manifest definition.", "tags": ["mcp", "claude-code", "serialization"], "complexity": "simple"}, {"id": "function:scripts/generate-agent-configs.py:render_marketplace", "type": "function", "name": "render_marketplace", "filePath": "scripts/generate-agent-configs.py", "lineRange": [543, 561], "summary": "Renders the local Codex plugin marketplace JSON from manifest plugin entries.", "tags": ["code-generation", "codex", "plugins"], "complexity": "simple"}, {"id": "function:scripts/generate-agent-configs.py:render_codex_plugin", "type": "function", "name": "render_codex_plugin", "filePath": "scripts/generate-agent-configs.py", "lineRange": [564, 582], "summary": "Renders one managed Codex plugin manifest, failing when required plugin keys are missing.", "tags": ["code-generation", "codex", "plugins"], "complexity": "simple"}, {"id": "function:scripts/generate-agent-configs.py:claude_skill_symlink_outputs", "type": "function", "name": "claude_skill_symlink_outputs", "filePath": "scripts/generate-agent-configs.py", "lineRange": [594, 611], "summary": "Produces chezmoi symlink_ outputs mirroring every shared skill file into home/dot_claude/skills.", "tags": ["code-generation", "skills", "symlinks"], "complexity": "simple"}, {"id": "function:scripts/generate-agent-configs.py:render_codex_profile", "type": "function", "name": "render_codex_profile", "filePath": "scripts/generate-agent-configs.py", "lineRange": [615, 636], "summary": "Renders a per-profile Codex TOML (model, reasoning effort, notify) launched via `codex --profile <name>`.", "tags": ["code-generation", "codex", "model-profiles"], "complexity": "simple"}, {"id": "function:scripts/generate-agent-configs.py:render_codex_profile_modify", "type": "function", "name": "render_codex_profile_modify", "filePath": "scripts/generate-agent-configs.py", "lineRange": [639, 805], "summary": "Generates a chezmoi modify_ Python script that merges the managed profile keys into an existing ~/.codex/<profile>.config.toml without clobbering user keys.", "tags": ["code-generation", "chezmoi", "modify-script", "codex"], "complexity": "complex"}, {"id": "function:scripts/generate-agent-configs.py:render_model_profiles_env", "type": "function", "name": "render_model_profiles_env", "filePath": "scripts/generate-agent-configs.py", "lineRange": [808, 829], "summary": "Renders the model-profiles.env shell fragment (interactive profile, worker kind/profile/worktree, per-profile CLI args) for agent launchers.", "tags": ["code-generation", "model-profiles", "shell-env"], "complexity": "simple"}, {"id": "function:scripts/generate-agent-configs.py:render_claude_express_agent", "type": "function", "name": "render_claude_express_agent", "filePath": "scripts/generate-agent-configs.py", "lineRange": [832, 850], "summary": "Renders the express-explorer Claude subagent definition pinned to the express profile model.", "tags": ["code-generation", "claude-code", "subagent"], "complexity": "simple"}, {"id": "function:scripts/generate-agent-configs.py:expected_outputs", "type": "function", "name": "expected_outputs", "filePath": "scripts/generate-agent-configs.py", "lineRange": [853, 875], "summary": "Collects every generated output path and rendered content derived from the manifest.", "tags": ["code-generation", "outputs", "orchestrator"], "complexity": "simple"}, {"id": "function:scripts/generate-agent-configs.py:remove_stale_generated_outputs", "type": "function", "name": "remove_stale_generated_outputs", "filePath": "scripts/generate-agent-configs.py", "lineRange": [878, 893], "summary": "Deletes generated files and empty directories under home/dot_claude/skills that are no longer expected.", "tags": ["cleanup", "code-generation", "skills"], "complexity": "simple"}, {"id": "function:scripts/generate-agent-configs.py:main", "type": "function", "name": "main", "filePath": "scripts/generate-agent-configs.py", "lineRange": [912, 979], "summary": "CLI entry handling --set-asset pin rewrites, --check drift verification, stale output removal, and writing all generated files.", "tags": ["entry-point", "cli", "code-generation"], "complexity": "moderate"}]

 succeeded in 303ms:
9:| S1 | orchestrator の受け入れ判定と最終マージが 1 席の直列 | P1-4〜P1-6 の後、1 RESULT の受け入れは verdict ファイル確認 + 記録生成 + `gh pr merge` で約 2〜5 分 → 12〜20 件/時。6 席が同時に RESULT を出すと最大 30 分待ち | 受け入れは RESULT 到着順で 1 件ずつ、判定に要る情報は P1-5 の precheck 証跡と review verdict に集約して読む量を固定。第 2 段階 H3 で review verdict を両ベンダーの席が返す。受け入れ権限は orchestrator に残す（rules） | 受け入れ待ち時間の分布を bus 履歴から出す（RESULT → ACCEPTANCE の時刻差） |
28:| Q5 | PR あたりの push 回数を減らす | P1-5 の precheck（local review・unit・render-check を RESULT 前に）で revise ラウンドを減らす。目標: PR 1 本の CI run ≤ 3 | revise 率 ≤ 20%（DoD-P1-f） | — |
29:| Q6 | Codex Bot | 自動 review は Codex 側設定のまま（P0/P1 のみ）。chain は Bot を待たない（repo rule: optional、never gated）。sweep は最終 head の 1 回、`scripts/pr-feedback.py` で全スレッドを取得し、disposition は `PR_FEEDBACK_EVIDENCE` の gate で必須のまま。review 直後は数秒待って再取得（race）。GitHub 上の解決は不要（D2） | Bot の所見は 1 件残らず disposition（fixed か not-applicable）。品質装置としては強化されこそすれ弱まらない | learn.chatgpt.com/docs/third-party/github、pr-integration rule |
43:| M4 | タスク文の作成（10〜20 分）と presend チェッカーの往復（最大 107 分） | `task-from-plan.py`: todo の 1 行から task.md の骨格を生成。allowed_files は `git grep` で触れる箇所を列挙して提案、premises は command を実行して output を貼る（recall しない）、trust-boundary ファイルなら threat_table の雛形を 1 行ずつ出す。`task-consistency-check.py` に 3 つの形の規則（test selector、sentence、owning task id）と threat_table の単位規則を追加し、レビュー席の 1 ラウンドは trust-boundary タスクだけに | premises が実行結果になる。チェッカーがレビューで繰り返し出た指摘を吸収（mistakes into mechanisms） | タスク文 3〜5 分、presend 失敗ほぼ 0、review 席の往復が減る | 採用。新 P1-12 |
64:| Q-D 品質指標を gate に | 連続 2 波ごとに計測し、閾値を超えたらマージ凍結と根本原因の記録（plan 第 7 節 STOP に追加済み）: main の push CI 赤 ≤ 1 回/2 波（かつ根本原因が記録されている）、マージ後 24 時間以内の hotfix PR（escaped defect）= 0、監査 P0/P1 のマージ後検出 = 0、revise 率 ≤ 20%、disposition の not-applicable 比率 ≤ 30%（高ければ Bot の所見を軽視している兆候として review） | 024-checklists.md P1-j、P1-k、progress.tsv の列 |
87:| 〃 | 内容のレビュー（threat の見落とし、制御の妥当性） | AI（独立モデル、1 ラウンド固定） | 既存の headless review（Codex review profile）を `security: true` のタスクだけに限定。停止条件は SKILL の既定 | 既存 |
95:### 5.14 残余（凍結後の計測事実、D-024-29）
99:5.12 **プログラム仕様** は `024-design-programs.md` に分離（17 項目: verdict.sh、audit-pool.sh と orch-audit.sh --json、schemas、result-precheck.sh、dispositions.py、regime.yml、dispatch.sh --next、acceptance-front-matter.py、git hooks、handoff.sh、flakes、task-from-plan.py）。
103:## 5.14 信頼ホスト実行契約（trusted-host execution contract、D-024-18）
107:1. **書き込み境界（前提 6、ランタイム別に正直に）** Claude worker 席は専用の設定ディレクトリ `CLAUDE_CONFIG_DIR=~/.claude-worker`（chezmoi が描画、operator が一度 login）で起動し、orchestrator の `~/.claude` と設定を共有しない。worker 設定：除外コマンド無し、Herdr socket 無し、sandbox の allowWrite は自席 worktree と agmsg store と席別キャッシュだけ、`failIfUnavailable: true`、信頼パス（anchored checkout の `.claude/worktrees/` 以外、`~/.agents`、`~/.claude*`、`~/.local`、`~/.config`）への Edit deny（公式文書：file tool の permission 検査は要求パスと symlink 解決後のパスの両方に deny を適用し、symlink そのものへの書き込みは拒否する）、sandbox の強制範囲はユーザー設定ではなく **managed settings**（`/Library/Application Support/ClaudeCode/managed-settings.json`、公式文書 "Repository settings under an admin-required sandbox"：project/local 設定は sandbox を無効化したり除外・socket を足したりできない）に置く。chezmoi は user ではこのファイルを書けないので、描画した内容を操作者が `sudo` で一度配置する（操作者手順）。worker 設定は worktree 自身の `.claude/**` と `.mcp.json` への Edit deny（`//<anchored>/.claude/worktrees/*/.claude/**`）を持つ（Bash 側は sandbox 既定の settings/hooks の denyWithinAllow）。agmsg store（全席が書く）から配送 hook が driver や plugin を source する上流の経路（storage.sh の `drivers.partition` traversal、`db/trusted-plugins` と `plugins/partition/shared.sh` による差し替え承認）は別タスク（agmsg hardening）の行で、worker 設定は `~/.agents/skills/agmsg/plugins/**` と `~/.agents/skills/agmsg/db/trusted-plugins` への書き込みを deny し（Edit deny は sandbox の deny にも合流する）、hook 側は store 由来の設定値を検証するまで残余と書く。managed settings の配置先は OS で異なる（macOS `/Library/Application Support/ClaudeCode/managed-settings.json`、Linux `/etc/claude-code/managed-settings.json`）。hook は agmsg 配送だけを、hook コマンドを `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<home> …` で始めて（`BASH_ENV` などの継承環境を bash 起動前に消す；PATH 固定だけでは BASH_ENV が先に走る）絶対パスのインタプリタで呼び（上流の agmsg スクリプトは `/usr/bin/env bash` の shebang を持つので、hook 実行環境の PATH が shim を含まないことで束縛する）、各 hook に `onFailure: "block"`。公式文書：linked worktree の session は **main checkout の `.claude/settings.local.json` を読む**ので、worker 向けの hook を worktree の settings.local.json に書いても読まれず、逆に orchestrator の local hooks が worker session でも走る。したがって orchestrator 側の local hooks も guard 経由にし、worker 側の hook は worker config dir の settings に置く。Edit deny の一覧は `git ls-tree` ではなく描画時の静的一覧（manifest に列挙、`.agents/worklog/**` と `.agents/worklog/uv-cache/**` を含む）とし、`~/.agents/**` の全面 deny は agmsg store の書き込みと矛盾するので、`~/.agents/agent-config.yaml`、`~/.agents/skills/**/scripts/**`、`~/.agents/model-profiles.env` などストア以外を列挙する。公式文書で確認した事実（2026-10-19）：`Edit(path)` の deny は Write/MultiEdit/NotebookEdit にも効き、deny → ask → allow の順で最初の一致が決まる；ただし Read/Edit の deny は **Bash sandbox の設定にも合流する**（"Paths and domains from both sandbox settings and permission rules are merged into the final sandbox configuration"）ので、ユーザー設定（全席共有）に `.orchestration/**` の Edit deny を書くと orchestrator の Bash による記録書き込みも止まる。hook は起動時に固定されず、設定ファイルの編集は file watcher が即座に反映する。`sandbox.failIfUnavailable` の既定は fail-open（依存が無ければ sandbox 無しで実行）。したがって Claude 席の境界は Edit deny 規則ではなく、**ユーザーレベルの PreToolUse hook**（`~/.claude/hooks/worker-write-boundary`、chezmoi が描画、`/bin/sh` または絶対パスの `python3 -I`）で作る：cwd の realpath が `<anchored>/.claude/worktrees/` 配下の session では、Write/Edit/MultiEdit/NotebookEdit の対象が cwd の外、または `<cwd>/.claude/**`・`<cwd>/.mcp.json` のとき `permissionDecision: deny` を返す。Bash 側は sandbox の既定 `denyWithinAllow`（settings、hooks）と `allowWrite`（自席 worktree）が担う。`failIfUnavailable: true` を全席に置く。 Codex 席は sandbox（workspace-write）がツールの書き込み全部を自席の worktree と列挙パスに限る。Claude 席は Seatbelt sandbox が Bash を限るだけで、Write/Edit/MultiEdit/NotebookEdit、hook、MCP プロセスは sandbox 外で動き、permission policy（permgate の決定論ポリシー）が path で拒否しない限り anchored checkout や `~/.agents` にも書ける（2026-10-19 時点、描画済み設定にその deny は無い）。したがって前提 6 は「Codex 席は成立、Claude 席は P1-15 が描画設定に Edit の path deny を入れるまで残余」と書く。P1-15 以前に「worker は信頼ルートに書けない」と書く文は誤りで、C-80 が拒否する。P1-15 が入るまで、承認の出所は項目 8 の「コミット済み台帳」で守る。書き込みは自席の worktree（`.claude/worktrees/<name>`）、scratch、列挙されたツールキャッシュに限る。anchored checkout（`.claude/worktrees/` 以外）、`~/.agents/agent-config.yaml`、`~/.claude/hooks`、信頼ルートのバイナリ、orchestrator の証跡・スナップショット・lock は worker から書けない。render テストが描画後の deny を検証する。残余は「どの席 sandbox にも属さない同一 UID プロセス」と、Worker Playbook step 4 が sandbox 外に出す少数のコマンド（gh）。後者は D-024-17（P1-15）で絶対パスの実行体に束縛する。 The protected-path inventory a seat's Edit denies cover is enumerated from the inputs of every trusted executable, not only the executables: it includes `~/.agents/permgate-policy.yaml` (permgate rereads it for every decision), `~/.local/lib/python*/site-packages` and every other user-site or startup-hook location of the interpreters in use (`.pth`, `usercustomize.py`, `sitecustomize.py`), `~/.claude-worker`'s hook and settings files, and the rendered guard; a text that binds an executable names its inputs in the same inventory (P1-15 amendment 5 C-80, 2026-10-19). The inventory of executable configuration sources a worker start screens is the documented loading list of the installed Claude Code version, enumerated once from the documentation (settings: user, project, local and managed `settings.json`; project `.mcp.json`; the configuration directory's global state `.claude.json` with user-scoped and project-local MCP servers; plugins and skills directories (`.claude/skills/*/.claude-plugin/plugin.json`, enabled plugins); hook handlers of every documented type (`command`, `http` and any other `type` value the hooks reference lists: a handler is an executable input whether it names a command or a URL, and a worker start refuses every handler type but `command`), `apiKeyHelper`, `statusLine.command`, MCP server commands), and the launcher screens or disables every source before accepting workspace trust, refusing any executable payload it did not write; adding sources one review at a time is the anti-pattern (P1-15 a02 reviews 2ae9e2c and ebbb71b, 2026-10-19). The enumeration quotes the documentation's values (the page, its fetched_at and the listed values) in the text's premises so a reviewer can check them against the live page; naming a source by one of its fields ("hook commands" for hook handlers) is the same anti-pattern one level down (a02 review b2a186e, 2026-10-19T20:36Z; C-95).
108:2. **無害化した環境を最初に** 最初の処理として `env -i` に入り、PATH は信頼ルートで解決した絶対バイナリへのリンクだけの私設ディレクトリ（shims、空、相対は拒否）。git は毎回 `GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null -c core.hooksPath=/dev/null -c core.fsmonitor=false -c protocol.allow=never -c protocol.https.allow=always` と明示 `-C`（https だけ許す。`protocol.allow=never` 単独は必要な fetch を止める）。 検査の読み取りは `GIT_NO_LAZY_FETCH=1` で部分クローンの遅延 fetch（checkout 設定の credential.helper を起動しうる）を止め、`-c submodule.recurse=false --ignore-submodules=all` で submodule 内の status/diff（submodule 自身の設定が filter を有効化しうる）を止める。`.gitmodules` を持つ checkout は検査対象として拒否する。 `-C` は作業木を束縛しないので（repo-local の `core.worktree` が読み先を checkout 外へ向けられる）、git は `--git-dir=<checkout>/.git --work-tree=<checkout>` を明示し、`git rev-parse --show-toplevel` の realpath が checkout と一致しないときは拒否する。 premise や検査の「コマンド実行」は、固定語彙の読み取り専用プローブ（`git rev-parse <ref>`、`test -e <path>`、`grep -c <pattern> <file>` のように検査器自身が解釈する形）だけを許し、任意のシェル文字列は実行しない（本文のハッシュはコマンド文を認証するだけで、`python -I scripts/x.py` のファイル被演算子や `source ./x.sh` の中身は認証しない）。diff と show は `--no-ext-diff --no-textconv` と `-c core.attributesFile=/dev/null -c core.sshCommand=false` を付け、PR 側の `.gitattributes`（external diff、textconv、filter）が検査内容や実行物を変えないようにする。Python は `-I`。PATH 探索で実行するものは無い。 A shell script that runs under a PR-controlled or worker-controlled environment (verdict.sh, the chain glue, CI steps) is executed as a program with `#!/bin/bash -p`, never as `bash <file>`, and only by a trusted parent that supplies the clean environment before the exec: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<passwd home> LANG=C.UTF-8 /bin/bash --noprofile --norc -p <absolute script path> …` (long options before `-p`). Privileged mode discards inherited functions, `BASH_ENV`/`ENV`, `SHELLOPTS`, `BASHOPTS`, `CDPATH` and `GLOBIGNORE`, but on Linux an inherited `LD_PRELOAD`/`LD_AUDIT` already executes while the loader maps `/bin/bash`, before `-p` or any statement runs, so a self re-exec inside the script is not a boundary and re-executing `"$0"` would reopen the caller's pathname (a worker-owned symlink can be swapped between the two executions); the program therefore verifies and refuses instead of repairing: its environment must consist of exactly the allowed names (checked through absolute paths `/usr/bin/env`, `/usr/bin/grep`), `$0` resolved with `realpath` must be a regular file under the repository root, and HOME must equal the passwd home of the real uid (`/usr/bin/dscl . -read /Users/<user> NFSHomeDirectory` on macOS, `/usr/bin/getent passwd <uid>` on Linux), otherwise exit 2 with a named message. A caller-set sentinel variable is not a sanitization proof, because the caller controls it (ci-efficiency a04 and verdict a04 C-80 reviews, 2026-10-19). No script accepts a caller-supplied executable directory; interpreters are the fixed absolute paths item 9 names.
113:0. **脅威モデル（D-024-21）** 席は同じ OS ユーザで動き、ホストは席間の信頼境界ではない（同一 UID のプロセスは symlink 差し替え、共有 `.git` の object 差し替え、hook の子プロセス、Herdr socket 経由の host 実行で、ホスト内のどの検査も迂回できる）。regime の硬い境界は GitHub（保護された main、必須チェック、orchestrator の identity によるマージ）。ただしこの境界は **worker 席が orchestrator の GitHub 資格情報を共有しない**ときだけ成立する（D-024-22：worker 席は専用の GitHub identity（別アカウントまたは App のトークン）で `gh` に login し、ruleset の bypass 一覧に入らない。orchestrator の keychain トークンを worker の config dir に持ち込まない。identity が分かれるまで「GitHub が境界」は未成立と書く）。**同一 macOS ユーザでは資格情報は分離できない**（gh は keychain の項目を host/user で引き、同じ UID の gh は orchestrator のトークンを読める。`GH_CONFIG_DIR` は設定を分けるだけ）。防止には worker 席を別の OS ユーザ（または別ホスト）で動かすしかなく、それは D-024-23 の将来項目（P1-16、操作者の判断）。それまで GitHub 境界は **検知**で守る：記録は boundary の記録 PR まで main に無いので、検知は次の記録 PR の regime ジョブで行う（`.orchestration/acceptance/**` に触れる PR で、前回 boundary 以降の main の各マージ commit に、gate 通過の証跡を持つ受け入れ記録が対応することを検査し、無ければその PR を失敗させる；P1-11 owner a02 の行 `ci:detection:1`）。main push 時点の検知は記録が無いので不可能であり、文は「次の記録 PR で検知、防止ではない」と書く。悪意ある worker に耐えるべき入力（承認台帳、gate が読む証跡 of record）は GitHub から sha 指定で API 経由（sandbox 内）に読み、ローカルファイルやローカル object database からは読まない。ホスト内の制御（本節 1〜10）は事故と prompt injection による損害の抑制であり、文はそう書く。
114:8. **承認はコミット済み台帳から読む** permission の決定行（`scope=permission approved_by=user diff_sha256=…`）は anchored checkout の作業コピーではなく、コミット済みの台帳から読む。読み方は `git ls-remote origin refs/heads/main` が返す commit sha を取り、GitHub API（`gh api repos/<owner>/<repo>/contents/.orchestration/decisions.tsv?ref=<sha>`、sandbox 内）でその sha の内容を取得する。ローカルの `git show` は共有 object database が書けるため中間 tree の差し替えで偽物を返しうる（第 3 回審査の所見 2）（ローカルの ref 名 `origin/main` は経由しない。`refs/replace/` も書けるので replacement を無効にする。Codex worker は `.git/objects` と `.git/refs` に書けるので ref は差し替えられるが、sha で指した object は内容アドレスで偽造できない）。作業コピーの行は提案で、記録 PR が main にマージされて初めて承認になる（PR の承認は操作者の操作）。偽造には main へのマージが要る。 The same applies to the PR content a mechanism evaluates (the verdict, the audit precheck, the counters): the changeset is read from GitHub at the 40-hex head (`gh api repos/{owner}/{repo}/compare/<base40>...<head40>`, `…/contents/<path>?ref=<head40>`) or from a private clone whose object store no worker can write; the main checkout's shared `.git/objects` and its `origin/main` ref are not evidence sources, because Codex workers write them (a04 C-80 round 1, 2026-10-19). Evidence files are named and matched by the full 40-hex head, never by a 7-character prefix. Every `gh` invocation names the repository explicitly: `gh pr`, `gh run` and `gh issue` subcommands take `--repo mryfmo/dotfiles` or the full pull-request URL, and `gh api` (which has no `--repo` flag) takes the explicit `repos/mryfmo/dotfiles/…` endpoint path, never a `{owner}/{repo}` placeholder; a `gh api graphql` call binds the repository through fixed query variables (`owner: "mryfmo"`, `name: "dotfiles"` as constants in the script, passed with `-f`/`-F`) and uses only node ids obtained from a query bound by those variables (verdict a04 C-80 round 5, 2026-10-19): the local repository configuration selects the default repository otherwise, and a matching head sha does not bind the repository because a fork can hold the same commit (verdict a04 C-80 round 2, 2026-10-19). A mechanism whose application path runs code this contract does not yet cover (the agmsg storage layer sourced by `dispatch.sh`/`history.sh`; the integration gate until its own hardening task lands) names that task as the prerequisite of its `--apply` mode and runs shadow-only until the prerequisite is merged. The sha of canonical `main` comes from the fixed repository's API (`gh api repos/mryfmo/dotfiles/git/ref/heads/main --jq .object.sha`), never from `git ls-remote origin`, whose destination the local remote and URL-rewrite configuration control (P1-12 a04 C-80, 2026-10-19T20:01Z); the content read at that sha comes from `repos/mryfmo/dotfiles/contents/<path>?ref=<sha40>`. Every `gh api` call that decides also binds the host with `--hostname github.com` (`GH_HOST` and the hosts configuration select the API host otherwise), a subcommand binds it through the `github.com/mryfmo/dotfiles` form of `--repo`, and a test that exports a hostile `GH_HOST` shows the call still names github.com or refuses (a02 review b2a186e, 2026-10-19T20:36Z).
115:9. **私設キャッシュ** orchestrator 側の実行は worker と共有するキャッシュ（`~/.cache/uv`、`~/.local/share/uv`、mise）から実行可能物を読まない。`UV_CACHE_DIR` を anchored checkout 配下（`.agents/worklog/uv-cache`、gitignored、worker 書き込み不可）に固定し、`uv run --no-config --no-project --offline --python <信頼ルートの絶対パスのインタプリタ>` で起動する（`--no-config` で uv の設定探索を止め、`--python` の絶対パスで cwd や親の `.venv` の発見を止める；敵対的な `.venv` と `uv.toml` を置いた fixture で検証）。hook は uv を使わず jq と python 標準ライブラリだけで動く。 One trusted interpreter resolver (`scripts/orchestrator/trusted-interpreter.sh`, P1-3 lineage) resolves `<abs>` from the repository's pinned declaration to a regular file under the tool manager's install root (the install root is anchored to the passwd home of the real uid, never to the HOME variable, which a caller can forge), refuses anything else, and every orchestrator-side script consumes it; no script keeps its own `command -v`, `mise which` or PATH fallback (ci-rerun.sh security review 44cb835, 2026-10-19). Shell code of other projects (the agmsg storage layer and its `drivers.partition` sourcing) is never sourced by an orchestrator-side mechanism; counters are read from the agmsg SQLite store read-only with a fixed query or from the pasted record. Every Python child of a trusted entrypoint runs with `-I` (isolated: no user site, no `PYTHON*` environment, no script directory on `sys.path`), so `uv run … python -I <script>` rather than `--script` for a script without declared dependencies; a test plants a `.pth` and a `usercustomize.py` in a fake user site and asserts they never execute (P1-15 amendment 5 C-80, 2026-10-19). A program takes `UV_CACHE_DIR` from the environment the trusted parent supplies and refuses when it is absent or not an absolute path; it never computes a default from its own root. The orchestrator's parent prefix sets the main checkout's `.agents/worklog/uv-cache`; a worker's launcher sets `<worktree>/.uv-cache` (the P1-15 worker launch value: `.agents/` is read-only in the Codex permission profile, so a root-derived `.agents/worklog/uv-cache` cannot be created by a worker; P1-12 a03, 2026-10-19T11:28Z); tests set a temporary directory.
117:7. **検証** threat_table は本節の項目 1〜10 に 1 行ずつ対応させる（参照だけでは足りない）。共通テスト補助 `tests/unit/trusted_exec_contract.py`（P1-6 で作る）を使い、仕組みごとに 4 つの red→green テストを持つ：PATH 先頭の shim が実行されない、植え付けた GIT_* と git 設定が効かない、worker ルート配下の信頼パスが拒否される、検証後に差し替えたファイルが消費側に届かない。
/Users/a0004262/.local/bin/crit
{
  "branch": "main",
  "daemon": {
    "running": false
  },
  "review_file": "/Users/a0004262/.crit/reviews/c06a520c1f9b/review.json",
  "review_file_exists": false,
  "sessions": [],
  "vcs": "git"
}

**Setting time budget and focus**
exec
/bin/zsh -lc "git diff --name-only 940a3a2b07adfd14140a0acff96784ef53a0a509..HEAD -- scripts home tests; cat .orchestration/acceptance/dotfiles-T133-trusted-exec-contract-tests-a01.md .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a03.md; rg -n 'excludedCommands|gh|GIT_CONFIG|PATH|shim' home/dot_agents/agent-config.yaml scripts/orchestrator/trusted-interpreter.sh tests/unit/trusted_exec_contract.py" in /Users/a0004262/Workspace/dotfiles
exec
/bin/zsh -lc "sed -n '101,118p' .orchestration/plans/024-design-quality.md; rg -n 'D-024-(21|29|30|33)' .orchestration/decisions.tsv; cat .orchestration/acceptance/dotfiles-T133-records-sync-pr-a01.md .orchestration/validation/dotfiles-T133-records-sync-pr-a01-text-security-801ad66.md" in /Users/a0004262/Workspace/dotfiles

 exited 2 in 80ms:
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
---
{
  "audit_findings": [],
  "dispatch": [
    "AGMSG-TASK v1 task_id=dotfiles-T133-trusted-exec-contract-tests-a01 round=1 repo=~/Workspace/dotfiles/.claude/worktrees/worker-d task_file=.orchestration/tasks/dotfiles-T133-trusted-exec-contract-tests-a01.md task_sha256=dd7549118bd470af98f52096ee668165a53727981eba4cb8466550641e2dc12c deadline=none done_signal=AGMSG-RESULT note=a011:test-only-helper-of-design-5.14-item-7(tests/unit/trusted_exec_contract.py-and-its-own-tests;no-production-consumer-yet);fresh-branch-from-origin/main;keep-tools/chain-review-scripts-followup-a06-untouched-for-its-pending-integration;security:false;the-Checks-block-at-the-end-carries-the-counters"
  ],
  "format": 1,
  "head": "9545e59f4a91aae36cd850c4645d29c366845844",
  "ledger": [
    {
      "class": "happy-path-closing-test",
      "id": "audit:9545e59:1"
    },
    {
      "class": "evidence",
      "id": "audit:9545e59:2"
    },
    {
      "class": "evidence",
      "id": "audit:9545e59:3"
    },
    {
      "class": "evidence",
      "id": "audit:9545e59:4"
    },
    {
      "class": "acceptance-dispositions",
      "id": "audit:9545e59:5"
    },
    {
      "class": "missing-owner-task",
      "id": "audit:9545e59:6"
    }
  ],
  "pr": 436,
  "replans": {},
  "searches": [],
  "task": "dotfiles-T133-trusted-exec-contract-tests-a01"
}
---

# Acceptance record: dotfiles-T133-trusted-exec-contract-tests-a01

Design 5.14 item 7 shared test helper (test-only; D-024-30 by-reference text). Authored by the review profile (`p-tec-author-prompt.md` -> `redesign/p-tec.md`), 197 lines, 3 files, checker OK, no C-80 (security: false).

- 2026-10-19T23:29:36Z: dispatched to a011 (worker-d); text sha256 dd7549118bd470af98f52096ee668165a53727981eba4cb8466550641e2dc12c.
- 2026-10-20T01:48:10Z: a011 RESULT round 1 `status=ready_for_review`: PR #436 (draft) head 25dd01e582f5bfa867e4cc9d306e03e529afe607, code head f4eed1cc, base ba318e53, task_copy dd754911…; tests/unit/trusted_exec_contract.py 242/250 lines, tests/unit/test_trusted_exec_contract.py 324/350; nine selectors (each probe detects its condition; shim, hostile git, worker root, swapped file, sanitised environment, trusted parent, passwd home per platform, cleanup after an exception); red at 755d9002 then green at f4eed1cc under uv offline on the exact python 3.15.0 and under the seat's default 3.10; per-probe red on a non-compliant stub then green; 12 wrong implementations each red; the case-alias case ran on APFS and skips on Linux CI with the measured reason; the real dscl was not run (exit 70 inside the sandbox; mocked); the worker's own review: 5 P2 fixed in one worker-side round (f4eed1cc). Adversarial check next: CI on 25dd01e5, caps by numstat in the chain, the owner text written (C-51), the PR marked ready.
- 2026-10-20T01:53:16Z: measured: 7 required checks, the canary and regime pass on 25dd01e5; GitGuardian (non-required) reports one `Generic Password` in commit 755d9002 at test_trusted_exec_contract.py:299: the synthetic passwd entry `name:x:uid:20:Probe:/home/probe:/bin/bash` of the getent mock, no credential (refutation in 436-extra.tsv with the git show evidence); PR marked ready; ACCEPTANCE pending-integration sent; owner text trusted-exec-contract-tests-followup-a01 written (checker OK); chain next.
- 2026-10-20T02:1xZ: the chain on #436: the base had moved (ba318e53 -> 118daafa), update-branched to 9545e59f; the chain refused at the required-checks step (rc 12: a required check failed on the new head); the failing job read next.


## Owned by dotfiles-T133-trusted-exec-contract-tests-followup-a01 (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)

local:9545e59:1	advisory-p2
local-finding: 9545e59:1 not-applicable:advisory P2 owned by dotfiles-T133-trusted-exec-contract-tests-followup-a01 (- [P2] Give worker-root writes a distinct timestamp baseline — tests/unit/trusted_exec_contract.py:109-111); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-trusted-exec-contract-tests-followup-a01.md (0c36290491e31ae2ccdbba12fb5321e3c1300c3951838d90b07756bfc6c5a65d)
- 2026-10-20T02:29:42Z: the chain on 9545e59f: every required check passes; the sweep found the GitGuardian check-run of the new head (a new run id, the same synthetic-passwd finding) and one CI download-retry annotation without rows; both dispositioned not-applicable with evidence; chain re-run.
- 2026-10-20T02:36:37Z: the chain on 9545e59f: sweep 0 gaps; task-level audit `…-audit-9545e59.md` `Verdict: incorrect`: P2 implementation (a same-length overwrite evades assert_untouched: INV-3 violated); P2 evidence (mutation M16 never ran; the twelve-mutation claim invalid); P3 evidence x2 (the 3.10 claim unsupported; the macOS CI claim wrong: test.yaml:119 skips unit tests for a Python-only diff); P2 orchestration (the known timestamp defect was deferred although small: a bounded revise is required); P3 orchestration (the owner text described PR #430: the orchestrator's clone from the assets template, fixed now). Plus the orchestrator's measured finding: passwd_home() calls dscl, which fails inside both seat sandboxes. Revise round 1 to a011 (= the second and last worker round under the inherited clause) with four selectors; the owner text corrected.
audit:9545e59:1	happy-path-closing-test
audit:9545e59:2	evidence
audit:9545e59:3	evidence
audit:9545e59:4	evidence
audit:9545e59:5	acceptance-dispositions
audit:9545e59:6	missing-owner-task
- 2026-10-20T03:27:48Z: a011 RESULT `round=1 revise=1`: head a2f47445a0d1d42802ab1afe958e21cd485118f6 (code 7d3ecd4f; fast-forward from 9545e59f; four commits: tests red, fix, the non-absolute-home case, the P3 fixes); (1) same-length overwrite detected (fixed past mtime + whole-content compare from the same inode and mode, access time put back), red at bb539aa7 then green; (2) 17 mutation blocks each red with unique anchors (M16 anchored on the runner check=False call); (3) the report states only pasted output (3.10.22 by absolute path: 10 OK; macOS CI skips the unit suite for this diff); (4) passwd_home() reads pwd.getpwuid first, dscl/getent only as a cross-check when they run (red at bb539aa7 in 6 subtests, green at 7d3ecd4f; live: dscl exit 70, passwd_home = the getpwuid home); caps 247/250 and 350/350 (reached exactly); the worker's own review of the round: correct, 5 P3 fixed; declared follow-ups (older worker-root gaps: sibling file, output read, rename-away-and-back, identical bytes with mtime put back; the newline half of the home check; one unexplained failure in a mutant run). ACCEPTANCE pending-integration at 2026-10-20T03:29:06Z; chain next (the GitGuardian run id changes per head; the sweep names it).
- 2026-10-20T03:42:21Z: chain on the update-branched head b3c50768 stopped at the sweep (rc=14, 3 gaps). (1) `regime` run 39364553764 failed: `regime-ci: … task-copy: .orchestration/dotfiles-T133-trusted-exec-contract-tests-a01/task.md differs from the base's dispatched .orchestration/tasks/…` — root cause: boundary 25 (#435, committed 2026-10-20T00:19:29Z) carried a snapshot of the task text taken before its dispatch line was pasted (dispatch 2026-10-19T23:29:38Z, task_sha256 dd754911…; the PR copy and the local text both equal it; main's copy lacks the one `dispatch to a011 …` line inside the Checks block); the same staleness holds for loop-limits-a01 (dispatched 00:55:43Z after the boundary commit). Proper state: main's tracked text equals the dispatched bytes, which regime-ci treats as the policy. Fix: records PR #438 (`records/sync-dispatched-texts-26`, head 8bf7e6ac) replaces both texts with the dispatched bytes; after its merge (operator approval per design 5.14 item 8, D-024-33) #436 takes the new base with `gh pr update-branch`, then CI, sweep and chain again. (2) GitGuardian check run 118438279783 re-reports the synthetic passwd fixture (four test-file occurrences and one in result.txt): refuted in `436-extra.tsv`. (3) the regime job's `Process completed with exit code 1` annotation is the same failure as (1). Mechanism: the boundary procedure must verify, before pushing, that every in-flight task text it carries equals the latest `task_sha256` dispatched on the bus (M-20261020-02 to be written with the boundary-26 preparation).
- 2026-10-20T04:39Z: PR #438 extended (head c58cf432) with the lint a04 and a05-checker texts; CI rerunning; the operator's approval is still the pending step; then update-branch #436.
- 2026-10-20T05:05Z: PR #438 extended again (head 88add881): eight texts (T128 a07, python-pin a01/a02 and P1-15 a03 added); CI rerunning; approval pending.

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
      "id": "text-security:f7af699:1"
    },
    {
      "class": "correct",
      "id": "text-security:9bd6198:0"
    },
    {
      "class": "input-inventory",
      "id": "worker:5067ed0:1"
    },
    {
      "class": "input-inventory",
      "id": "text-security:efa211d:1"
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

rg: scripts/orchestrator/trusted-interpreter.sh: No such file or directory (os error 2)
rg: tests/unit/trusted_exec_contract.py: No such file or directory (os error 2)
home/dot_agents/agent-config.yaml:34:    claude: { model: claude-opus-5-5, effort: xhigh, advisor: fable }
home/dot_agents/agent-config.yaml:37:      model_reasoning_effort: xhigh
home/dot_agents/agent-config.yaml:42:    claude: { model: claude-fable-5-1, effort: xhigh }
home/dot_agents/agent-config.yaml:43:    codex: { model: gpt-6.1-sol, model_reasoning_effort: xhigh }
home/dot_agents/agent-config.yaml:45:    claude: { model: claude-fable-5-1, effort: xhigh, advisor: fable }
home/dot_agents/agent-config.yaml:48:      model_reasoning_effort: xhigh
home/dot_agents/agent-config.yaml:52:    claude: { model: claude-fable-5, effort: high }
home/dot_agents/agent-config.yaml:56:      model_reasoning_effort: high
home/dot_agents/agent-config.yaml:60:    # at xhigh reasoning effort (operator pin 2026-10-09, T115).
home/dot_agents/agent-config.yaml:61:    claude: { model: claude-fable-5-1, effort: high }
home/dot_agents/agent-config.yaml:64:      model_reasoning_effort: xhigh
home/dot_agents/agent-config.yaml:124:      PATH: '{{ .chezmoi.homeDir }}/.local/share/mise/installs/node/lts/bin:{{ .chezmoi.homeDir }}/.local/share/mise/shims:{{ .chezmoi.homeDir }}/.local/bin:{{ .chezmoi.homeDir }}/.local/bin/common:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin'
home/dot_agents/agent-config.yaml:223:      - Bash(gh release:*)
home/dot_agents/agent-config.yaml:230:      - Bash(gh pr merge:*)
home/dot_agents/agent-config.yaml:231:      - Bash(gh pr create:*)
home/dot_agents/agent-config.yaml:232:      - Bash(gh pr comment:*)
home/dot_agents/agent-config.yaml:233:      - Bash(gh pr review:*)
home/dot_agents/agent-config.yaml:234:      - Bash(gh pr close:*)
home/dot_agents/agent-config.yaml:235:      - Bash(gh pr edit:*)
home/dot_agents/agent-config.yaml:236:      - Bash(gh pr update-branch:*)
home/dot_agents/agent-config.yaml:237:      - Bash(gh issue:*)
home/dot_agents/agent-config.yaml:238:      - Bash(gh api -X POST:*)
home/dot_agents/agent-config.yaml:239:      - Bash(gh api --method POST:*)
home/dot_agents/agent-config.yaml:240:      - Bash(gh api -XPOST:*)
home/dot_agents/agent-config.yaml:241:      - Bash(gh api --method=POST:*)
home/dot_agents/agent-config.yaml:242:      - Bash(gh api -X PATCH:*)
home/dot_agents/agent-config.yaml:243:      - Bash(gh api --method PATCH:*)
home/dot_agents/agent-config.yaml:244:      - Bash(gh api -XPATCH:*)
home/dot_agents/agent-config.yaml:245:      - Bash(gh api --method=PATCH:*)
home/dot_agents/agent-config.yaml:246:      - Bash(gh api -X PUT:*)
home/dot_agents/agent-config.yaml:247:      - Bash(gh api --method PUT:*)
home/dot_agents/agent-config.yaml:248:      - Bash(gh api -XPUT:*)
home/dot_agents/agent-config.yaml:249:      - Bash(gh api --method=PUT:*)
home/dot_agents/agent-config.yaml:250:      - Bash(gh api -X DELETE:*)
home/dot_agents/agent-config.yaml:251:      - Bash(gh api --method DELETE:*)
home/dot_agents/agent-config.yaml:252:      - Bash(gh api -XDELETE:*)
home/dot_agents/agent-config.yaml:253:      - Bash(gh api --method=DELETE:*)
home/dot_agents/agent-config.yaml:254:      - Bash(gh api -f:*)
home/dot_agents/agent-config.yaml:255:      - Bash(gh api -F:*)
home/dot_agents/agent-config.yaml:256:      - Bash(gh api --raw-field:*)
home/dot_agents/agent-config.yaml:257:      - Bash(gh api --field:*)
home/dot_agents/agent-config.yaml:258:      - Bash(gh api -f*)
home/dot_agents/agent-config.yaml:259:      - Bash(gh api -F*)
home/dot_agents/agent-config.yaml:260:      - Bash(gh api --raw-field=*)
home/dot_agents/agent-config.yaml:261:      - Bash(gh api --field=*)
home/dot_agents/agent-config.yaml:285:    excludedCommands:
home/dot_agents/agent-config.yaml:291:    # Linux blocks gh's keyring and herdr-agents -> actas-claim.sh socket calls;
home/dot_agents/agent-config.yaml:294:      - gh *
home/dot_agents/agent-config.yaml:397:# pins here only, through generate-agent-configs.py --set-asset. `pin: unknown`
home/dot_agents/agent-config.yaml:405:    attestation: when-gh-authenticated
home/dot_agents/agent-config.yaml:407:    note: the newest cooled-down release installs only when gpg and gpgv (SHASUMS256.asc checked against the release key with gpg_fingerprint, fetched from keys.openpgp.org as mise documents) or an authenticated gh (the release attestation) can verify it before it runs; otherwise the fallback release does, and mise self-update moves it forward afterwards.
home/dot_agents/agent-config.yaml:415:      reason: a host without gpg and without an authenticated gh (a fresh macOS) can check neither the release key's signature nor the release attestation before mise runs, and SHASUMS256.txt comes from the same release; so it bootstraps this reviewed release, SHASUMS256.txt kept as a second check.
home/dot_agents/agent-config.yaml:481:    attestation: when-gh-authenticated
home/dot_agents/agent-config.yaml:482:    note: chezmoi signs its checksums with cosign only, which a fresh host cannot run; the newest cooled-down release installs only when an authenticated gh can check its release attestation before it runs, otherwise the fallback release does, and mise's own chezmoi takes over after the bootstrap.
home/dot_agents/agent-config.yaml:490:      reason: setup.sh runs before gh is installed or logged in, so a fresh host cannot check chezmoi's release attestation before chezmoi runs, and its cosign signature needs cosign; it bootstraps this reviewed release, the release's checksums file kept as a second check.
home/dot_agents/agent-config.yaml:555:    note: PyPI read 2026-10-17T10:33Z; eight platform wheels, no sdist or universal wheel; these four cover Mac and glibc Linux on amd64/arm64.
home/dot_agents/agent-config.yaml:627:      behind that tag (lightweight tag, c487be2), and sha256 is the digest of
home/dot_agents/agent-config.yaml:669:  gh-extensions:
home/dot_agents/agent-config.yaml:670:    source: gh-extension
home/dot_agents/agent-config.yaml:671:    upstream: https://github.com/seachicken/gh-poi
home/dot_agents/agent-config.yaml:674:    installer: install/common/gh_extensions.sh
home/dot_agents/agent-config.yaml:675:    note: install/common/gh_extensions.sh installs seachicken/gh-poi unpinned

**Reviewing large record output**
codex
参照契約は、同一 UID への防御を「防止ではなく被害抑制」と明記しています。その限界自体は指摘せず、タスクが `closed` とする制御や、実際の起動・push 手順との食い違いを確認しています。Crit の既存データはありません。読み取り専用の指定に従い、worklog やレビュー証跡は書き込みません。
exec
/bin/zsh -lc "wc -l .orchestration/acceptance/dotfiles-T133-records-sync-pr-a01.md .orchestration/validation/dotfiles-T133-records-sync-pr-a01-text-security-801ad66.md; tail -n 22 .orchestration/acceptance/dotfiles-T133-records-sync-pr-a01.md; tail -n 45 .orchestration/validation/dotfiles-T133-records-sync-pr-a01-text-security-801ad66.md; sed -n '116,119p' .orchestration/plans/024-design-quality.md; sed -n '280,301p' home/dot_agents/agent-config.yaml" in /Users/a0004262/Workspace/dotfiles
 succeeded in 21ms:
      17 .orchestration/acceptance/dotfiles-T133-records-sync-pr-a01.md
    2045 .orchestration/validation/dotfiles-T133-records-sync-pr-a01-text-security-801ad66.md
    2062 total
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
  "task": "dotfiles-T133-records-sync-pr-a01"
}
---

# Acceptance record: dotfiles-T133-records-sync-pr-a01

- 2026-10-20T06:24Z: text written whole by the review profile from the orchestrator's brief (`dotfiles-T133-records-sync-pr-a01-prompt.md`; security: true; the mechanism of M-20261020-02: scripts/orchestrator/records-sync.sh verifies each dispatched text against the bus task_sha256 and opens or updates the records-sync PR (never merges)); trailing authoring commentary stripped by the orchestrator; pre-send.sh: checker OK, SECRET_PATTERN 0, home paths 0; sha256 801ad66b… before the Checks paste. C-80 round 1 running; dispatch to an idle Claude seat after a correct verdict (files disjoint from every in-flight task).
home/dot_agents/agent-config.yaml:238:      - Bash(gh api -X POST:*)
home/dot_agents/agent-config.yaml:239:      - Bash(gh api --method POST:*)
home/dot_agents/agent-config.yaml:240:      - Bash(gh api -XPOST:*)
home/dot_agents/agent-config.yaml:241:      - Bash(gh api --method=POST:*)
home/dot_agents/agent-config.yaml:242:      - Bash(gh api -X PATCH:*)
home/dot_agents/agent-config.yaml:243:      - Bash(gh api --method PATCH:*)
home/dot_agents/agent-config.yaml:244:      - Bash(gh api -XPATCH:*)
home/dot_agents/agent-config.yaml:245:      - Bash(gh api --method=PATCH:*)
home/dot_agents/agent-config.yaml:246:      - Bash(gh api -X PUT:*)
home/dot_agents/agent-config.yaml:247:      - Bash(gh api --method PUT:*)
home/dot_agents/agent-config.yaml:248:      - Bash(gh api -XPUT:*)
home/dot_agents/agent-config.yaml:249:      - Bash(gh api --method=PUT:*)
home/dot_agents/agent-config.yaml:250:      - Bash(gh api -X DELETE:*)
home/dot_agents/agent-config.yaml:251:      - Bash(gh api --method DELETE:*)
home/dot_agents/agent-config.yaml:252:      - Bash(gh api -XDELETE:*)
home/dot_agents/agent-config.yaml:253:      - Bash(gh api --method=DELETE:*)
home/dot_agents/agent-config.yaml:254:      - Bash(gh api -f:*)
home/dot_agents/agent-config.yaml:255:      - Bash(gh api -F:*)
home/dot_agents/agent-config.yaml:256:      - Bash(gh api --raw-field:*)
home/dot_agents/agent-config.yaml:257:      - Bash(gh api --field:*)
home/dot_agents/agent-config.yaml:258:      - Bash(gh api -f*)
home/dot_agents/agent-config.yaml:259:      - Bash(gh api -F*)
home/dot_agents/agent-config.yaml:260:      - Bash(gh api --raw-field=*)
home/dot_agents/agent-config.yaml:261:      - Bash(gh api --field=*)
home/dot_agents/agent-config.yaml:285:    excludedCommands:
home/dot_agents/agent-config.yaml:291:    # Linux blocks gh's keyring and herdr-agents -> actas-claim.sh socket calls;
home/dot_agents/agent-config.yaml:294:      - gh *
home/dot_agents/agent-config.yaml:397:# pins here only, through generate-agent-configs.py --set-asset. `pin: unknown`
home/dot_agents/agent-config.yaml:405:    attestation: when-gh-authenticated
home/dot_agents/agent-config.yaml:407:    note: the newest cooled-down release installs only when gpg and gpgv (SHASUMS256.asc checked against the release key with gpg_fingerprint, fetched from keys.openpgp.org as mise documents) or an authenticated gh (the release attestation) can verify it before it runs; otherwise the fallback release does, and mise self-update moves it forward afterwards.
home/dot_agents/agent-config.yaml:415:      reason: a host without gpg and without an authenticated gh (a fresh macOS) can check neither the release key's signature nor the release attestation before mise runs, and SHASUMS256.txt comes from the same release; so it bootstraps this reviewed release, SHASUMS256.txt kept as a second check.
home/dot_agents/agent-config.yaml:481:    attestation: when-gh-authenticated
home/dot_agents/agent-config.yaml:482:    note: chezmoi signs its checksums with cosign only, which a fresh host cannot run; the newest cooled-down release installs only when an authenticated gh can check its release attestation before it runs, otherwise the fallback release does, and mise's own chezmoi takes over after the bootstrap.
home/dot_agents/agent-config.yaml:490:      reason: setup.sh runs before gh is installed or logged in, so a fresh host cannot check chezmoi's release attestation before chezmoi runs, and its cosign signature needs cosign; it bootstraps this reviewed release, the release's checksums file kept as a second check.
home/dot_agents/agent-config.yaml:555:    note: PyPI read 2026-10-17T10:33Z; eight platform wheels, no sdist or universal wheel; these four cover Mac and glibc Linux on amd64/arm64.
home/dot_agents/agent-config.yaml:627:      behind that tag (lightweight tag, c487be2), and sha256 is the digest of
home/dot_agents/agent-config.yaml:669:  gh-extensions:
home/dot_agents/agent-config.yaml:670:    source: gh-extension
home/dot_agents/agent-config.yaml:671:    upstream: https://github.com/seachicken/gh-poi
home/dot_agents/agent-config.yaml:674:    installer: install/common/gh_extensions.sh
home/dot_agents/agent-config.yaml:675:    note: install/common/gh_extensions.sh installs seachicken/gh-poi unpinned

**Reviewing large record output**
codex
参照契約は、同一 UID への防御を「防止ではなく被害抑制」と明記しています。その限界自体は指摘せず、タスクが `closed` とする制御や、実際の起動・push 手順との食い違いを確認しています。Crit の既存データはありません。読み取り専用の指定に従い、worklog やレビュー証跡は書き込みません。
10. **worker は sandbox 外でコマンドを実行しない（D-024-17 の改訂）** 2026-10-19T03:45Z の実測で `gh api` は Claude sandbox の中から成功した（sandbox の proxy は CONNECT 型で TLS を終端しない；keychain のトークンも読めた）。worker 席の除外コマンドは空にし、gh も git push も sandbox 内の proxy 経由で実行する。Codex 席は `sandbox_workspace_write.network_access = true` で同じ状態にし、permgate の codex ポリシーは sandbox 外への escape を承認しない（permgate の変更は操作者の手順）。wrapper 方式（絶対パス、env -i、固定 GH_CONFIG_DIR）は LD_PRELOAD と引数転送（`gh repo clone -- --config`）を閉じられないので採らない。
7. **検証** threat_table は本節の項目 1〜10 に 1 行ずつ対応させる（参照だけでは足りない）。共通テスト補助 `tests/unit/trusted_exec_contract.py`（P1-6 で作る）を使い、仕組みごとに 4 つの red→green テストを持つ：PATH 先頭の shim が実行されない、植え付けた GIT_* と git 設定が効かない、worker ルート配下の信頼パスが拒否される、検証後に差し替えたファイルが消費側に届かない。
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

**Planning independent review agent**
exec
/bin/zsh -lc "python3 -c 'from pathlib import Path
for line in Path(\".orchestration/decisions.tsv\").read_text().splitlines():
 if line.startswith((\"D-024-21\\t\",\"D-024-29\\t\",\"D-024-30\\t\",\"D-024-33\\t\")): print(line)
for name in [\"dotfiles-T133-trusted-exec-contract-tests-a01\",\"dotfiles-T133-trusted-entrypoint-binding-a01\"]:
 p=Path(\".orchestration/acceptance\")/(name+\".md\")
 print(\"RECORD\",p)
 if p.exists():
  for line in p.read_text().splitlines():
   if line.startswith((\"- 2026\",\"# Acceptance\",\"text-security:\",\"re-plan:\")): print(line[:1600])'" in /Users/a0004262/Workspace/dotfiles
 succeeded in 8ms:
D-024-21	2026-10-19T04:0xZ	threat model and mechanism of the worker boundary: the host is not a security boundary between seats sharing one OS user; the hard boundary is GitHub (protected main, required checks, the orchestrator identity merge); approvals and gate evidence of record are read from GitHub at a sha through the API inside the sandbox; Claude worker seats run under their own CLAUDE_CONFIG_DIR (~/.claude-worker: no excluded commands, no Herdr socket, Edit denies on trusted paths with symlink coverage, failIfUnavailable true, minimal trusted hooks with onFailure block); host-local controls target accidental and injected damage and the texts say so (design 5.14 items 0, 1, 8)	three C-80 reviews of the P1-15 text (03:24Z, 03:42Z, 03:58Z) found host-level escapes no in-process check closes (symlink swap race, writable object database, hook descendants through shims, Herdr socket RPC, hook timeout fail-open); the documentation confirms per-directory settings and credentials (one operator login for the worker directory), onFailure block (>= 2.1.295; installed 2.1.300), and symlink-aware file-tool deny rules	default under the autonomy directive, reported 2026-10-19 13:0x JST; the worker-directory login is an operator step at the P1-15 deployment; scope=design,permission	applied-to-the-P1-15-text
D-024-29	2026-10-19T21:39Z	Design 5.14 is frozen (plan 006 A1: three review rounds, then freeze with a residual list): items 0-10 are the contract; a text review finding that needs a new design sentence is recorded in the design's residual list and as an owner row, not as an amendment of the item and of the text under review, unless it names a P0/P1 that is exploitable in the proposed implementation.	items 1, 2, 3, 8 and 9 were amended five times on 10-19/20 (one per review round of P1-15 and P1-12), each amendment re-opening the texts that quote the item (C-88) and costing a review round each; the texts chased a moving design.	plan 006 A1; M-20261019-05; C-92	applied from 06:40 JST; the residual list is a new subsection `5.14 残余` in 024-design-quality.md (written at the next design edit)
D-024-30	2026-10-19T23:16Z	A task text applies design 5.14 by reference: it names the items it relies on (`design: 5.14 items 2, 3, 8, 9`) and carries one threat row per item 0-10 in the item's own words, never a restated or paraphrased copy of the item; C-88 is narrowed to the exact contract sentences a test asserts; the task-consistency check gains a rule (C16) that a security: true orchestrator-side text names 5.14 and has the per-item rows (owner: the P1-12 follow-up after a04 frees task-consistency-check.py).	restated design text drifted in every reset text and re-opened a review round at each design amendment (P1-15: 23 review rounds; P1-12: 4); by-reference texts stay within proposal 1's caps and a mechanical check replaces the reviewer's paraphrase comparison; the operator's direction of 2026-10-19T22:59Z (relayed by a011) asks for the same.	plan 006 A1; D-024-29; M-20261019-05; proposal 1	applied from 08:15 JST to new texts (trusted-exec-contract-tests-a01 first); existing correct texts are not rewritten
D-024-33	2026-10-20T03:07Z	Records boundary PR #435 (head 8f7b97690df6060a73959a06fc6622a2beaf5029) is approved by the operator's written instruction in the orchestrator session at 2026-10-20 12:0x JST ("承認するので作業を継続"); the orchestrator merges it with gh pr merge --squash --match-head-commit 8f7b9769… right after PR #431 merges (or at once if #431 fails or resets), so the P1-15 chain and audit already running at edd824ea are not invalidated by a base move.	design 5.14 item 8 makes the operator's approval the authority of the recorded decisions (D-024-25..32); GitHub's ruleset 24397953 has no approval rule (rules: deletion, non_fast_forward, required_status_checks), so the written instruction is the operative approval; sequencing after #431 saves one CI run and one re-audit on the critical path.	design 5.14 item 8; ruleset 24397953; the 11:55 JST report	applied; merge pending #431
RECORD .orchestration/acceptance/dotfiles-T133-trusted-exec-contract-tests-a01.md
# Acceptance record: dotfiles-T133-trusted-exec-contract-tests-a01
- 2026-10-19T23:29:36Z: dispatched to a011 (worker-d); text sha256 dd7549118bd470af98f52096ee668165a53727981eba4cb8466550641e2dc12c.
- 2026-10-20T01:48:10Z: a011 RESULT round 1 `status=ready_for_review`: PR #436 (draft) head 25dd01e582f5bfa867e4cc9d306e03e529afe607, code head f4eed1cc, base ba318e53, task_copy dd754911…; tests/unit/trusted_exec_contract.py 242/250 lines, tests/unit/test_trusted_exec_contract.py 324/350; nine selectors (each probe detects its condition; shim, hostile git, worker root, swapped file, sanitised environment, trusted parent, passwd home per platform, cleanup after an exception); red at 755d9002 then green at f4eed1cc under uv offline on the exact python 3.15.0 and under the seat's default 3.10; per-probe red on a non-compliant stub then green; 12 wrong implementations each red; the case-alias case ran on APFS and skips on Linux CI with the measured reason; the real dscl was not run (exit 70 inside the sandbox; mocked); the worker's own review: 5 P2 fixed in one worker-side round (f4eed1cc). Adversarial check next: CI on 25dd01e5, caps by numstat in the chain, the owner text written (C-51), the PR marked ready.
- 2026-10-20T01:53:16Z: measured: 7 required checks, the canary and regime pass on 25dd01e5; GitGuardian (non-required) reports one `Generic Password` in commit 755d9002 at test_trusted_exec_contract.py:299: the synthetic passwd entry `name:x:uid:20:Probe:/home/probe:/bin/bash` of the getent mock, no credential (refutation in 436-extra.tsv with the git show evidence); PR marked ready; ACCEPTANCE pending-integration sent; owner text trusted-exec-contract-tests-followup-a01 written (checker OK); chain next.
- 2026-10-20T02:1xZ: the chain on #436: the base had moved (ba318e53 -> 118daafa), update-branched to 9545e59f; the chain refused at the required-checks step (rc 12: a required check failed on the new head); the failing job read next.
- 2026-10-20T02:29:42Z: the chain on 9545e59f: every required check passes; the sweep found the GitGuardian check-run of the new head (a new run id, the same synthetic-passwd finding) and one CI download-retry annotation without rows; both dispositioned not-applicable with evidence; chain re-run.
- 2026-10-20T02:36:37Z: the chain on 9545e59f: sweep 0 gaps; task-level audit `…-audit-9545e59.md` `Verdict: incorrect`: P2 implementation (a same-length overwrite evades assert_untouched: INV-3 violated); P2 evidence (mutation M16 never ran; the twelve-mutation claim invalid); P3 evidence x2 (the 3.10 claim unsupported; the macOS CI claim wrong: test.yaml:119 skips unit tests for a Python-only diff); P2 orchestration (the known timestamp defect was deferred although small: a bounded revise is required); P3 orchestration (the owner text described PR #430: the orchestrator's clone from the assets template, fixed now). Plus the orchestrator's measured finding: passwd_home() calls dscl, which fails inside both seat sandboxes. Revise round 1 to a011 (= the second and last worker round under the inherited clause) with four selectors; the owner text corrected.
- 2026-10-20T03:27:48Z: a011 RESULT `round=1 revise=1`: head a2f47445a0d1d42802ab1afe958e21cd485118f6 (code 7d3ecd4f; fast-forward from 9545e59f; four commits: tests red, fix, the non-absolute-home case, the P3 fixes); (1) same-length overwrite detected (fixed past mtime + whole-content compare from the same inode and mode, access time put back), red at bb539aa7 then green; (2) 17 mutation blocks each red with unique anchors (M16 anchored on the runner check=False call); (3) the report states only pasted output (3.10.22 by absolute path: 10 OK; macOS CI skips the unit suite for this diff); (4) passwd_home() reads pwd.getpwuid first, dscl/getent only as a cross-check when they run (red at bb539aa7 in 6 subtests, green at 7d3ecd4f; live: dscl exit 70, passwd_home = the getpwuid home); caps 247/250 and 350/350 (reached exactly); the worker's own review of the round: correct, 5 P3 fixed; declared follow-ups (older worker-root gaps: sibling file, output read, rename-away-and-back, identical bytes with mtime put back; the newline half of the home check; one unexplained failure in a mutant run). ACCEPTANCE pending-integration at 2026-10-20T03:29:06Z; chain next (the GitGuardian run id changes per head; the sweep names it).
- 2026-10-20T03:42:21Z: chain on the update-branched head b3c50768 stopped at the sweep (rc=14, 3 gaps). (1) `regime` run 39364553764 failed: `regime-ci: … task-copy: .orchestration/dotfiles-T133-trusted-exec-contract-tests-a01/task.md differs from the base's dispatched .orchestration/tasks/…` — root cause: boundary 25 (#435, committed 2026-10-20T00:19:29Z) carried a snapshot of the task text taken before its dispatch line was pasted (dispatch 2026-10-19T23:29:38Z, task_sha256 dd754911…; the PR copy and the local text both equal it; main's copy lacks the one `dispatch to a011 …` line inside the Checks block); the same staleness holds for loop-limits-a01 (dispatched 00:55:43Z after the boundary commit). Proper state: main's tracked text equals the dispatched bytes, which regime-ci treats as the policy. Fix: records PR #438 (`records/sync-dispatched-texts-26`, head 8bf7e6ac) replaces both texts with the dispatched bytes; after its merge (operator approval per design 5.14 item 8, D-024-33) #436 takes the new base with `gh pr update-branch`, then CI, sweep and chain again. (2) GitGuardian check run 118438279783 re-reports the synthetic passwd fixture (four test-file occurrences and one in result.txt): refuted in `436-extra.tsv`. (3) the regime job's `Process completed with exit code 1` annotation is the same failure as (1). Mechanism: the boundary procedure must verify, before pushing, that every in-flight task text it carries equals the latest `task_sha256` dispatched on the bus (M-20261020-02 to be written with the boundary-26 preparation).
- 2026-10-20T04:39Z: PR #438 extended (head c58cf432) with the lint a04 and a05-checker texts; CI rerunning; the operator's approval is still the pending step; then update-branch #436.
- 2026-10-20T05:05Z: PR #438 extended again (head 88add881): eight texts (T128 a07, python-pin a01/a02 and P1-15 a03 added); CI rerunning; approval pending.
RECORD .orchestration/acceptance/dotfiles-T133-trusted-entrypoint-binding-a01.md
# Acceptance record: dotfiles-T133-trusted-entrypoint-binding-a01
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

**Searching for official git filter URL rewrites**
web search: 
web search: site.git-scm.com/docs/git-config url insteadOf pushInsteadOf core.hooksPath filter clean ...
**Summarizing key security findings**
**Listing additional technical issues**
web search: 
web search: https://git-scm.com/docs/git-config
**Reviewing documentation carefully**
exec
/bin/zsh -lc "cat .orchestration/validation/dotfiles-T133-trusted-entrypoint-binding-a01-text-security-1cc2a02.md.last.md .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-audit-9545e59.md.last.md; sed -n '119,140p' .orchestration/plans/024-design-quality.md; rg -n 'step 4|Linux|excluded|sandbox|gh' /Users/a0004262/.agents/skills/agmsg-orchestration/SKILL.md | tail -n 12; /usr/bin/which -a git gh uv sqlite3 dirname" in /Users/a0004262/Workspace/dotfiles
 succeeded in 174ms:
No reportable findings. Reviewed all **55 threat rows** across both task texts and the cited acceptance/review history; required controls have rows, and none claims `closed`. The independent review agreed.

Production wiring fixes the manifest operand, prohibits fixture overrides, and requires binary checks before execution. The clean prefix removes inherited `GIT_*`; P1-15 supplies path protection, case-alias coverage and removal of Linux’s `gh` exemption. The exec-form contract avoids shell reinterpretation, consistent with [Claude’s documentation](https://code.claude.com/docs/en/hooks#exec-form-and-shell-form).

Reviewed SHA-256: `1cc2a02b0876caf8892c1a16f5ece5d20784c34cc48e8b880175ec98db81e4e0`.

📝 まとめ: Completed the read-only pre-dispatch design review; no files changed. Dispatch remains conditional on the stated prerequisites.

Not checked: implementation, runtime tests, CI or deployment; documented same-UID replacement, loader-environment and shared-credential risks remain.
Verdict: correctAudited [PR #436](https://github.com/mryfmo/dotfiles/pull/436) at `9545e59f4a91aae36cd850c4645d29c366845844`. Missing legacy report/validation/sandbox paths were replaced by their committed task-directory counterparts.

- [P2] high implementation tests/unit/trusted_exec_contract.py:111 An immediate same-length overwrite can preserve inode, size and coarse-grained mtime, causing `assert_untouched()` to miss a worker-root write; initialize a distinct mtime baseline and test that overwrite.
- [P2] high evidence .orchestration/dotfiles-T133-trusted-exec-contract-tests-a01/validation.md:253 M16 never reaches its tests: its replacement matches twice and fails the uniqueness assertion; the subsequently printed failures reuse M15’s output, invalidating the claimed twelve successful mutation checks.
- [P3] high evidence .orchestration/dotfiles-T133-trusted-exec-contract-tests-a01/report.md:84 The claimed Python 3.10 pass is unsupported: the cited validation command prints Python 3.15.0.
- [P3] high evidence .orchestration/dotfiles-T133-trusted-exec-contract-tests-a01/report.md:94 The macOS CI coverage claim is inaccurate for this PR: `.github/workflows/test.yaml:119` skips unit tests for this Python-only diff.
- [P2] high orchestration .orchestration/acceptance/dotfiles-T133-trusted-exec-contract-tests-a01.md:30 The known timestamp defect is deferred despite being a small fix within `allowed_files`; Playbook step 10 requires a bounded revise for such findings, and the record provides no exhausted-counter justification.
- [P3] high orchestration .orchestration/tasks/dotfiles-T133-trusted-exec-contract-tests-followup-a01.md:45 The designated owner describes findings from PR #430 and dispatch after #430 merges, conflicting with this PR #436 lineage; correct the ownership instructions before relying on that disposition.

`INV-1`–`INV-6` correspond to the task’s six numbered helper requirements.

INV-1: holds tests/unit/test_trusted_exec_contract.py:183 — shim execution and complete argv recording checked.  
INV-2: holds tests/unit/test_trusted_exec_contract.py:192 — Git environment and local-config attacks exercised separately.  
INV-3: violated tests/unit/trusted_exec_contract.py:111 — same-length writes can escape detection.  
INV-4: holds tests/unit/test_trusted_exec_contract.py:241 — deterministic swap and measured case-alias coverage.  
INV-5: holds tests/unit/trusted_exec_contract.py:181 — exact environment names and PATH enforced.  
INV-6: holds tests/unit/trusted_exec_contract.py:216 — trusted-parent argv, environment and path refusals implemented.

Orchestration findings: 2

📝 まとめ: Read-only audit completed; two non-mutating tests passed, task-copy hash and line caps matched, and no files were modified. Findings remain unresolved.

Not rerun: filesystem fixture tests; live GitHub verification failed via gh and web. Saved CI results do not eliminate the probe’s false-negative risk.  
Verdict: incorrect198:2. Switch to the `repo` and read `task_file` before editing or running validations. Create the task branch without touching the shared `.git/config`, which is read-only for a Codex seat by design (T64 writable roots): `git switch -c <branch> --no-track origin/main`, push with `git push origin <branch>` (no `-u`), and open the PR as a draft with `gh pr create --draft --head <branch>`. Commit inside the sandbox, with `git -c commit.gpgsign=false` when the signing key is unreadable there; for a Claude seat only the push leaves the sandbox, and a Codex seat pushes from inside it (step 4). A Claude seat's sandbox can leave the same failed write behind, so it uses the same commands. A leftover `.git/config.lock` from a failed attempt is removed by the orchestrator. Remove a scratch worktree (for example one that proves a test fails on `origin/main`) with `git worktree remove <path>` only; never run `git worktree prune` from a sandboxed seat, because other worktrees' paths look missing inside the sandbox and prune then targets their admin directories in the shared `.git/worktrees`.
200:4. Do not perform any `forbidden_actions`. Complete every command inside the sandbox and allowlist; never escalate an action outside that boundary for approval. Fail it instead, send `AGMSG-PONG v1 status=blocked` with the exact command and the boundary it crosses, and wait for the orchestrator to re-task. Agent-to-agent permission approval is forbidden: only the human operator answers a permission prompt. A Claude Code auto-mode classifier denial (for example Self-Modification) is such a boundary: stop without a diff, send `AGMSG-PONG v1 status=blocked` naming the classifier reason, and never pursue the same outcome through another tool. Fetch and fast-forward inside the sandbox; a public remote needs no credential. For Claude seats on macOS, Seatbelt denies the Mach lookup of `com.apple.trustd.agent`, so Go-based CLIs (`gh`, `gcloud`, `terraform`) fail TLS verification with `x509: OSStatus -26276` (`errSecInternal`); `git` uses Apple libcurl, LibreSSL and `/etc/ssl/cert.pem` and succeeds. On Linux, the bubblewrap sandbox denies the AF_UNIX keyring socket, so `gh` answers HTTP 401; `allowUnixSockets` cannot grant a path. Monitor and process visibility limits are in "Identity, delivery, and storage". On both platforms a Claude seat runs three commands outside the sandbox through the permission gate: `gh`, `git push`, and an authenticated `git fetch` (a private HTTPS remote, whose credential helper is `gh`); `excludedCommands` and `enableWeakerNetworkIsolation` are operator options, not selected alternatives. Look up a VERIFY item's external reference (upstream documentation, release notes, an API schema) with the WebFetch tool, not Bash `curl`. Three documented cases run outside the sandbox too: the task's main-checkout CompactionDB `memory add`, through the permission gate because that state directory is read-only from a worktree sandbox; writing the task's artifacts at their expected main-checkout paths and masking them with the repository masker, through the permission gate because the main checkout is not writable from a worktree sandbox; and `agmsg-dispatch`, through `excludedCommands` (step 11). Every other out-of-sandbox action stays a blocked PONG. A Codex seat has in-sandbox network (T64) and never leaves its sandbox.
201:5. Write artifacts to the exact expected paths (a Claude seat writes them through the permission gate, step 4). Do not invent alternate paths. A seat whose sandbox cannot write the main checkout (a Codex seat) writes them at the same relative paths in its own worktree, untracked, and the RESULT says so; the orchestrator moves them into the main checkout by absolute path before review. Worker-side review evidence carries a `-worker-` infix (`<task>-worker-crit.json`, `<task>-worker-review-receipt.md`), so it never collides with the orchestrator's own files.
203:7. Put the isolation status or fallback rationale in `expected_sandbox_file`.
207:11. Reply with the requested `done_signal`, normally `AGMSG-RESULT v1`, and include all artifact paths. To a herdr-paned orchestrator, send RESULT and PONG with `agmsg-dispatch <team> <worker> <orchestrator> <pane_id>` (for example `wN:p1`; single-line, shell-safe text) rather than bare `send.sh`, so the wake starts the idle orchestrator's turn and its Stop hook delivers the message. The Claude sandbox manifest lists `agmsg-dispatch` in `claude.sandbox.excludedCommands`, so a Claude worker runs it outside the sandbox from the first attempt: no failed sandboxed run, no unsandboxed retry, and no escalation. Claude Code still applies its permission rules to excluded commands, so the managed settings allow `Bash(agmsg-dispatch:*)` (the only managed `permissions.allow` entry) and the dispatch runs without a prompt. A Codex seat runs under Codex's own sandbox, which this setting does not cover.
210:14. Before sending RESULT, a worker whose session started a Crit plan review accounts for its Crit review server. A Claude seat starts one through Plan Mode's ExitPlanMode hook, and a Codex seat through the Crit plugin's Stop hook (`crit plan-hook --mode codex`). `make check-regime-boundary` treats a running `crit _serve` as a violation, and unit tests that read the host `pgrep` fail while one runs.
211:    - A worker cannot reliably stop the server itself (verified with crit v0.21.1 on a scratch `crit plan`). Inside the sandbox, `crit stop` always reports no running daemon. Outside it, `crit stop` stops the plan server only on the branch the server was started on, so it misses a server started before `git switch -c <task-branch>`, which is the common worker case. `crit stop <plan-file>` does not match a plan session on any branch. An unsandboxed `crit stop` is also not pre-approved.
212:    - A worker cannot inspect the host for the server either. Neither seat may leave its sandbox for host commands, because that would be an escalation, which step 4 forbids. For a Claude seat on macOS or Linux, the platform-specific process limits in "Identity, delivery, and storage" also apply here; no sandboxed host inspection is attempted.
214:    - The orchestrator handles it as control-plane hygiene on the host. It runs these `pgrep`/`ps`/`kill` calls outside its own sandbox through the permission gate (`dangerouslyDisableSandbox`, answered by the operator or the auto-mode classifier) under its control-plane exemption, as it already does for `agmsg-dispatch` and `herdr-agents --audit`. It lists servers with `pgrep -fl _serve`, where a process named `crit` is a Crit server and the calling shell is listed under its own name. It reads each server's session record (`~/.crit/sessions/*.json` holds `pid`, `cwd` and `branch`) and confirms the server is live before acting: `ps -o args= -p <pid>` must show `crit _serve`, and the record's `cwd` must be that worker's worktree. The live process's own cwd must also match: `readlink /proc/<pid>/cwd` on Linux (`lsof -a -d cwd -p <pid> -Fn` on macOS) must equal the record's `cwd`. A mismatch means the pid was reused, and the record is stale. Only then does it stop the server with `kill <pid>`. A record whose pid is gone or runs another command is stale; it is removed, never killed. Never use `crit stop --all`, which stops every seat's server.
216:    - Mark the PR ready for review with `gh pr ready <n>` before the first wait, while it is still a draft (`gh pr ready` exits non-zero on a PR that is already ready, so a later head's wait skips it): the Codex Bot reviews non-draft PRs, and a draft only on an explicit `@codex review` comment. When no Bot review of the final head arrives within 10 minutes, post `@codex review` on the PR and wait out the rest of the window.
217:    - Run `gh pr checks <pr> --watch` in the background and the Bot wait below at the same time: the 10-minute and 15-minute marks count from `gh pr ready` (from the push, for a later head), never from the end of CI. Right after a push GitHub can report no checks yet, and the watcher then exits 1 with `no checks reported`: start it once a check is listed, and restart it on that message instead of reading it as a CI failure. Wait for that watcher's exit status before the RESULT: a non-zero exit means no RESULT until CI passes.
218:    - Then list the Bot's reviews of the final head with `gh api --paginate repos/{owner}/{repo}/pulls/<n>/reviews --jq '.[]|select(.user.login=="chatgpt-codex-connector[bot]" and .commit_id=="<head-sha>")|[.commit_id,.submitted_at]|@tsv'` and the Bot's top-level review comments raised on it with `gh api --paginate repos/{owner}/{repo}/pulls/<n>/comments --jq '.[]|select(.in_reply_to_id == null and .user.login=="chatgpt-codex-connector[bot]" and .original_commit_id=="<head-sha>")|[.id,.original_commit_id,.path]|@tsv'`. A human comment, a CodeRabbit review or an earlier head's review never ends the wait. A comment's `commit_id` moves to the newest head, so findings are matched by `original_commit_id`. Repeat until a review of the final head appears or 15 minutes pass; the report records the latter as `bot: none`. The final head here is the diff head, the last commit that changes the PR's content: a head that only merges the new base with `gh pr update-branch` needs green CI but no new Bot wait. Both endpoints return 30 items per page by default, so keep `--paginate`.
/opt/homebrew/bin/git
/usr/bin/git
/Users/a0004262/.local/share/mise/shims/gh
/Users/a0004262/.local/share/mise/shims/uv
/usr/bin/sqlite3
/usr/bin/dirname

**Noticing elapsed time**
codex
具体的には、固定した push URL が Git のローカル設定で書き換わる経路と、checkout・stage 時に属性フィルタが実行される経路が残っています。また、Linux の `gh` 除外設定は、本文の「全コマンドを sandbox 内で実行する」という宣言だけでは解除されません。独立レビューでも照合しています。
web search: 
web search: 'url.<base>.insteadOf'
**Ensuring safe git command execution**
**Reviewing task-level command safeguards**
**Verifying SQLite suitability**
web search: 
web search: https://sqlite.org/cli.html
**Checking CLI help behavior**
exec
/bin/zsh -lc '/usr/bin/sqlite3 -help; /usr/bin/env -i PATH=/usr/bin:/bin GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null /usr/bin/git -c core.hooksPath=/dev/null -c core.fsmonitor=false -c protocol.allow=never -c protocol.https.allow=always -c url.https://example.invalid/.insteadOf=https://github.com/mryfmo/ ls-remote --get-url https://github.com/mryfmo/dotfiles.git; /usr/bin/shasum -a 256 .orchestration/tasks/dotfiles-T133-records-sync-pr-a01.md' in /Users/a0004262/Workspace/dotfiles
 succeeded in 53ms:
Usage: /usr/bin/sqlite3 [OPTIONS] [FILENAME [SQL...]]
FILENAME is the name of an SQLite database. A new database is created
if the file does not previously exist. Defaults to :memory:.
OPTIONS include:
   --                   treat no subsequent arguments as options
   -A ARGS...           run ".archive ARGS" and exit
   -alg ALGORITHM       Use ALGORITHM as the encryption algorithm
   -append              append the database to the end of the file
   -ascii               set output mode to 'ascii'
   -bail                stop after hitting an error
   -batch               force batch I/O
   -box                 set output mode to 'box'
   -cmd COMMAND         run "COMMAND" before reading stdin
   -column              set output mode to 'column'
   -csv                 set output mode to 'csv'
   -deserialize         open the database using sqlite3_deserialize()
   -echo                print inputs before execution
   -escape T            ctrl-char escape; T is one of: symbol, ascii, off
   -init FILENAME       read/process named file
   -[no]header          turn headers on or off
   -help                show this message
   -hexkey KEY          hexadecimal encryption key
   -html                set output mode to HTML
   -ifexists            only open if database already exists
   -interactive         force interactive I/O
   -key KEY             raw encryption key
   -json                set output mode to 'json'
   -line                set output mode to 'line'
   -list                set output mode to 'list'
   -lookaside SIZE N    use N entries of SZ bytes for lookaside memory
   -markdown            set output mode to 'markdown'
   -maxsize N           maximum size for a --deserialize database
   -memtrace            trace all memory allocations and deallocations
   -newline SEP         set output row separator. Default: '\n'
   -nofollow            refuse to open symbolic links to database files
   -noinit              Do not read the ~/.sqliterc file at startup
   -nonce STRING        set the safe-mode escape nonce
   -no-rowid-in-view    Disable rowid-in-view using sqlite3_config()
   -nullvalue TEXT      set text string for NULL values. Default ''
   -pagecache SIZE N    use N slots of SZ bytes each for page cache memory
   -pcachetrace         trace all page cache operations
   -quote               set output mode to 'quote'
   -readonly            open the database read-only
   -safe                enable safe-mode
   -screenwidth N       use N as the default screenwidth 
   -separator SEP       set output column separator. Default: '|'
   -stats               print memory stats before each finalize
   -textkey PASSPHRASE  text to be hashed into the encryption key
   -table               set output mode to 'table'
   -tabs                set output mode to 'tabs'
   -unsafe-testing      allow unsafe commands and modes for testing
   -version             show SQLite version
   -vfs NAME            use NAME as the default VFS
   -vfstrace            enable tracing of all VFS calls
   -zip                 open the file as a ZIP Archive
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
https://example.invalid/dotfiles.git
801ad66b8389ccd8babb25780dcb843b00ed7843e4206ac586da3c853ce80df8  .orchestration/tasks/dotfiles-T133-records-sync-pr-a01.md

**Assessing commit risks and worker sandbox limitations**
**Summarizing security findings and environment verification**

I'm reviewing all 24 threat entries with citations and checking the security priorities between P1 and P2 levels. I want to confirm assumptions about the local git environment and note specific risks like unqualified execution of git/gh commands and potential unsafe test runner behavior, aiming to provide a clear, comprehensive summary.
**Reviewing configuration and user progress**

I’m checking recent user progress and validating referenced reviews to focus on representative evidence without overloading on every citation. I’m also inspecting local config files cautiously to ensure the correct settings apply and to catch any sandbox or worker configuration that might affect the current environment.
exec
/bin/zsh -lc "python3 -c 'import json; from pathlib import Path
for p in [Path.home()/\".claude/settings.json\",Path.home()/\".claude-worker/settings.json\"]:
 print(p.name, str(p.parent.name), \"exists=\",p.exists())
 if p.exists():
  d=json.loads(p.read_text()); s=d.get(\"sandbox\",{}); print({k:s.get(k) for k in (\"enabled\",\"excludedCommands\",\"failIfUnavailable\",\"allowUnsandboxedCommands\")})'; rg -n 'linux_excluded_commands' scripts/generate-agent-configs.py; rg -n 'noinit|sqliterc' /usr/share/man/man1/sqlite3.1" in /Users/a0004262/Workspace/dotfiles
 succeeded in 118ms:
settings.json .claude exists= True
{'enabled': True, 'excludedCommands': ['agmsg-dispatch *'], 'failIfUnavailable': False, 'allowUnsandboxedCommands': True}
settings.json .claude-worker exists= False
388:        + (sandbox.get("linux_excluded_commands", []) if os_name == "linux" else []),
286:.B ${XDG_CONFIG_HOME}/sqlite3/sqliterc
288:.B ~/.config/sqlite3/sqliterc
290:.B ~/.sqliterc

**Noticing SQLite init file behavior**
exec
/bin/zsh -lc "sed -n '270,302p' /usr/share/man/man1/sqlite3.1; sed -n '375,393p' scripts/generate-agent-configs.py" in /Users/a0004262/Workspace/dotfiles
 succeeded in 0ms:
as follows:

o The default configuration is established as follows:

.sp
.nf
.cc |
mode            = LIST
separator       = "|"
main prompt     = "sqlite> "
continue prompt = "   ...> "
|cc .
.sp
.fi

o If the environment variable XDG_CONFIG_HOME is set then
.B ${XDG_CONFIG_HOME}/sqlite3/sqliterc
is checked, else
.B ~/.config/sqlite3/sqliterc
is checked. If the selected file does not exist then the fallback of
.B ~/.sqliterc
is used. It should generally only contain meta-commands.

o If the -init option is present, the specified file is processed.

o All other command line options are processed.

.SH HISTORY FILE
.B sqlite3
may be configured to use a history file to save SQL statements and
meta-commands entered interactively. These statements and commands can be
retrieved, edited and, reused at the main and continue prompts. If the
environment variable

def render_claude_sandbox(manifest: dict[str, Any], os_name: str = "darwin") -> dict[str, Any]:
    """Render the Claude sandbox; allowWrite reuses the Codex agmsg writable roots."""
    sandbox = manifest["claude"]["sandbox"]
    network = dict(sandbox["network"])
    if os_name != "darwin":
        network.pop("allowMachLookup", None)
    return {
        "enabled": sandbox["enabled"],
        "failIfUnavailable": sandbox["failIfUnavailable"],
        "autoAllowBashIfSandboxed": sandbox["autoAllowBashIfSandboxed"],
        "allowUnsandboxedCommands": sandbox["allowUnsandboxedCommands"],
        "excludedCommands": sandbox["excludedCommands"]
        + (sandbox.get("linux_excluded_commands", []) if os_name == "linux" else []),
        "filesystem": {
            "allowWrite": [
                *manifest["codex"]["sandbox_workspace_write"]["writable_roots"],
                *sandbox.get("filesystem", {}).get("extra_allow_write", []),
                *(sandbox.get("filesystem", {}).get("darwin_extra_allow_write", []) if os_name == "darwin" else []),

**Analyzing sandbox and environment risks**
**Evaluating PATH and shim issues**
codex
24 行の脅威表を確認し、追加で SQLite の起動設定ファイルも見つかりました。`-readonly` はデータベースの書き込みを制限しますが、起動設定中の `.shell` 実行は止めません。最終報告は、参照契約で既に認めている残余リスクと重複しない、具体的な実行経路に絞ります。
web search: 
web search: 'GIT_CONFIG_COUNT'
**Finalizing summary with verdict**
**Ensuring message completion**
**Analyzing git push and environment handling**
**Evaluating command execution and environment isolation**
**Summarizing test case references**
**Reviewing test count consistency**
codex
Reviewed all 24 threat rows, the referenced contract, and related acceptance/review records.

- [P1] high .orchestration/tasks/dotfiles-T133-records-sync-pr-a01.md:88 Checkout and staging can execute repository-configured `filter.*.smudge`, `clean`, or `process` through `.gitattributes` or `.git/info/attributes`; the imported controls do not disable these, and a malicious filter preserving bytes passes staged-hash verification. Disable this execution path before checkout/staging and test it. [Git documentation](https://git-scm.com/docs/gitattributes#_filter)

- [P1] high .orchestration/tasks/dotfiles-T133-records-sync-pr-a01.md:59 The sandbox-only claim lacks an enforced prerequisite: the current renderer adds Linux’s `gh *` exclusion, while `after: []` permits immediate dispatch; excluded calls execute outside the sandbox without triggering the promised refusal. Require verified worker configuration with that exclusion removed before dispatch. [Sandbox documentation](https://code.claude.com/docs/en/sandboxing#run-commands-outside-the-sandbox-with-excludedcommands)

- [P2] high .orchestration/tasks/dotfiles-T133-records-sync-pr-a01.md:87 `sqlite3 -readonly` still consumes startup configuration, including `~/.sqliterc`, which can execute `.shell` commands; neither the threat table nor tests control this executable input. Disable startup-file loading and add a planted-initialization regression; database read-only mode is insufficient. [SQLite documentation](https://sqlite.org/cli.html)

- [P2] high .orchestration/tasks/dotfiles-T133-records-sync-pr-a01.md:89 Repository-local `url.*.insteadOf` or `pushInsteadOf` can redirect the fixed HTTPS push to another HTTPS repository despite the imported global/system isolation; capturing the original push arguments does not verify its destination. Isolate transport configuration and test the effective destination. [Git documentation](https://git-scm.com/docs/git-config#Documentation/git-config.txt-urlbaseinsteadOf)

📝 まとめ: Completed the read-only design review; four findings remain for orchestrator disposition. No files changed.

Not checked: implementation, exploit execution or CI; the documented same-UID limitations remain.
Verdict: incorrect
hook: Stop
hook: Stop Completed
tokens used
97,701
Reviewed all 24 threat rows, the referenced contract, and related acceptance/review records.

- [P1] high .orchestration/tasks/dotfiles-T133-records-sync-pr-a01.md:88 Checkout and staging can execute repository-configured `filter.*.smudge`, `clean`, or `process` through `.gitattributes` or `.git/info/attributes`; the imported controls do not disable these, and a malicious filter preserving bytes passes staged-hash verification. Disable this execution path before checkout/staging and test it. [Git documentation](https://git-scm.com/docs/gitattributes#_filter)

- [P1] high .orchestration/tasks/dotfiles-T133-records-sync-pr-a01.md:59 The sandbox-only claim lacks an enforced prerequisite: the current renderer adds Linux’s `gh *` exclusion, while `after: []` permits immediate dispatch; excluded calls execute outside the sandbox without triggering the promised refusal. Require verified worker configuration with that exclusion removed before dispatch. [Sandbox documentation](https://code.claude.com/docs/en/sandboxing#run-commands-outside-the-sandbox-with-excludedcommands)

- [P2] high .orchestration/tasks/dotfiles-T133-records-sync-pr-a01.md:87 `sqlite3 -readonly` still consumes startup configuration, including `~/.sqliterc`, which can execute `.shell` commands; neither the threat table nor tests control this executable input. Disable startup-file loading and add a planted-initialization regression; database read-only mode is insufficient. [SQLite documentation](https://sqlite.org/cli.html)

- [P2] high .orchestration/tasks/dotfiles-T133-records-sync-pr-a01.md:89 Repository-local `url.*.insteadOf` or `pushInsteadOf` can redirect the fixed HTTPS push to another HTTPS repository despite the imported global/system isolation; capturing the original push arguments does not verify its destination. Isolate transport configuration and test the effective destination. [Git documentation](https://git-scm.com/docs/git-config#Documentation/git-config.txt-urlbaseinsteadOf)

📝 まとめ: Completed the read-only design review; four findings remain for orchestrator disposition. No files changed.

Not checked: implementation, exploit execution or CI; the documented same-UID limitations remain.
Verdict: incorrect
