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
session id: 01a1579d-8e5d-7690-b985-7a761840f89f
--------
user
Pre-dispatch security review (read-only, security profile) of the task text .orchestration/tasks/dotfiles-T133-python-pin-a02.md and its threat_table, before any implementation exists. Judge the design the text states: can the controls it names bind what actually executes on this host (mise shims first on PATH, same-user worker processes, gh outside the sandbox on Linux, symlinks and case-insensitive filesystems, inherited GIT_* environment)? Check every threat row: a closed row whose named test cannot close it, a residual row whose control does not mitigate the risk, a missing row for a file or non-path control, and any gap of the class decision-not-bound-to-execution (a decision made on text or on a validated copy while the execution resolves binaries, files or ledgers from an attacker-influenced place). Read the related acceptance records and reviews the text cites for context. Report each finding as [P0-P3] <confidence> <file:line> <one line>; findings are input for the orchestrator, who decides. End with exactly one line: Verdict: correct or Verdict: incorrect.
warning: loading hooks from both ~/.codex/hooks.json and ~/.codex/config.toml; prefer a single representation for this layer
hook: SessionStart
hook: SessionStart
hook: SessionStart Completed
hook: SessionStart Completed
hook: UserPromptSubmit
hook: UserPromptSubmit Completed
codex
🤖 I read the AGENTS.md for mryfmo/dotfiles.
対象タスクと参照先の acceptance・review を読み、各 threat row の制御が実行時にも効くかを確認します。agmsg-orchestration と Ponytail のスキルを参照し、読み取り専用で進めます。
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
/bin/zsh -lc 'nl -ba .orchestration/tasks/dotfiles-T133-python-pin-a02.md' in ~/Workspace/dotfiles
exec
/bin/zsh -lc 'git status --short; git rev-parse HEAD; command -v crit; command -v python3; command -v git; command -v gh; print -r -- "$PATH"' in ~/Workspace/dotfiles
exec
/bin/zsh -lc 'cat ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail-review/SKILL.md; if test -f .ua/meta.json; then cat .ua/meta.json; fi' in ~/Workspace/dotfiles
 succeeded in 139ms:
     1	---
     2	format: 2
     3	task_id: dotfiles-T133-python-pin-a02
     4	reset_of: [dotfiles-T133-python-pin-a01]
     5	kind: code
     6	security: true
     7	allowed_files:
     8	  - home/dot_mise/config.toml
     9	  - tests/unit/test_mise_config.py
    10	  - .orchestration/dotfiles-T133-python-pin-a02/**
    11	after: []
    12	threat_table:
    13	  - {control: "home/dot_mise/config.toml", disposition: "closed: tests/unit/test_mise_config.py::MiseConfigTest::test_python_is_exact_version"}
    14	  - {control: "tests/unit/test_mise_config.py", disposition: "closed: tests/unit/test_mise_config.py::MiseConfigTest::test_python_is_exact_version"}
    15	  - {control: ".orchestration/dotfiles-T133-python-pin-a02/**", disposition: "residual: these are untrusted records; the orchestrator compares the dispatched text, final diff, evidence and CI before acceptance."}
    16	  - {control: "operator post-merge deployment: make update + mise install", disposition: "residual: the operator deploys after merge and records commands, output and installed version in the acceptance record; the worker never writes the host installation."}
    17	  - {control: "workflow and interpreter or environment inputs", disposition: "residual: Commands bind the parent environment, interpreter and gh; dotfiles-T133-ci-efficiency-followup-a04 owns the deployed resolver, and CI retains its current interpreter setup."}
    18	  - {control: "new or renamed scripts", disposition: "residual: no new or renamed script is authorized; Commands (d) executes only the inherited intended test module."}
    19	  - {control: "task metadata: kind, allowed_files, threat_table and premises", disposition: "residual: the task-consistency check validates metadata before dispatch and acceptance; whole-file comparison detects changes to the worker copy."}
    20	  - {control: "metadata separators: task-copy and evidence front matter", disposition: "residual: front-matter parsing and whole-file comparison expose changed separators; evidence remains untrusted input to review."}
    21	  - {control: "in-process effects", disposition: "residual: Commands (d) executes only the intended repository test file, using standard-library imports and TOML data; it does not discover packages or run the supply-chain test's PATH-resolved chezmoi launch."}
    22	  - {control: "evidence records under .orchestration/dotfiles-T133-python-pin-a02/", disposition: "residual: records identify Commands sections, operands, exit statuses and output; the orchestrator compares them with the final changeset and CI."}
    23	  - {control: "task copy: .orchestration/dotfiles-T133-python-pin-a02/task.md", disposition: "residual: the copy must match the dispatched text byte-for-byte and its dispatch SHA-256; the orchestrator compares both before acceptance."}
    24	  - {control: "predecessor copy: .orchestration/dotfiles-T133-python-pin-a01/task.md", disposition: "residual: unchanged on the branch at its a01 dispatched bytes (SHA-256 30185a5a…); regime-ci checks only the latest copy of a reset_of lineage, and the orchestrator compares the predecessor copy with the a01 dispatch at acceptance."}
    25	  - {control: "design 5.14 item 0: 脅威モデル（D-024-21）", disposition: "residual: shared credentials and unrestricted same-UID replacement remain possible; host checks reduce accidents and prompt injection, and missing acceptance evidence is detected at the next records PR rather than prevented."}
    26	  - {control: "design 5.14 item 1: 書き込み境界（前提 6、ランタイム別に正直に）", disposition: "residual: only a sandboxed Codex seat executes this task; it does not deploy or write trusted host inputs, and no unrestricted same-UID boundary is claimed."}
    27	  - {control: "design 5.14 item 2: 無害化した環境を最初に", disposition: "residual: Commands establish the clean parent before bootstrap and use Commands (b) for validation children; deployed enforcement remains with dotfiles-T133-ci-efficiency-followup-a04."}
    28	  - {control: "design 5.14 item 3: 信頼パスの境界検査", disposition: "residual: Commands (c) records the declared executable's realpath; deployed worker-root, symlink and case-alias rejection remains with dotfiles-T133-ci-efficiency-followup-a04."}
    29	  - {control: "design 5.14 item 4: 検証したものを実行し、検証した内容を渡す", disposition: "residual: Commands (c) and (d) use the same fixed PY binding without rediscovery; same-UID replacement between probe and execution remains possible."}
    30	  - {control: "design 5.14 item 5: 出力と予約の同一性", disposition: "residual: Commands (f) evidence records full base and head SHAs; no reservation or lock is introduced, and acceptance verifies the final head."}
    31	  - {control: "design 5.14 item 6: 正直な残余", disposition: "residual: the declaration test checks syntax, not executable provenance, deployment or protection against unrestricted same-UID replacement."}
    32	  - {control: "design 5.14 item 7: 検証", disposition: "residual: Commands (d) supplies declaration red/green evidence; the four execution-contract fixture tests remain the responsibility of dotfiles-T133-ci-efficiency-followup-a04."}
    33	  - {control: "design 5.14 item 8: 承認はコミット済み台帳から読む", disposition: "residual: Commands (e) binds the base and Commands (f) obtains cap evidence from github.com's fixed repository API at full 40-hex SHAs; acceptance verifies the final head against GitHub content."}
    34	  - {control: "design 5.14 item 9: 私設キャッシュ", disposition: "residual: Commands (c) and (d) use the installed interpreter directly without uv or provisioning; authenticating deployed executable inputs remains with dotfiles-T133-ci-efficiency-followup-a04."}
    35	  - {control: "design 5.14 item 10: worker は sandbox 外でコマンドを実行しない（D-024-17 の改訂）", disposition: "residual: every worker command stays sandboxed; a denial produces a blocked PONG without escalation or a substitute tool."}
    36	  - {control: "orchestrator effect merge", disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"}
    37	  - {control: "orchestrator effect update-branch", disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"}
    38	  - {control: "orchestrator effect forced worker removal", disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"}
    39	premises:
    40	  - claim: "Commands (a), successfully probed read-only by the orchestrator at 2026-10-20T04:31:20Z against a01 sha 30185a5a…."
    41	    command: |-
    42	      case "$(/usr/bin/uname -s)" in
    43	        Darwin) home=$(/usr/bin/id -P | cut -d: -f9);;
    44	        Linux) home=$(getent passwd "$(id -un)" | cut -d: -f6);;
    45	        *) printf '%s\n' 'home: refused: unsupported-platform' >&2; exit 1;;
    46	      esac
    47	      rc=$?; [ "$rc" -eq 0 ] || { printf 'home: refused: lookup-failed (exit %s)\n' "$rc" >&2; exit "$rc"; }
    48	      case "$home" in /*) ;; *) printf '%s\n' 'home: refused: not-absolute' >&2; exit 1;; esac
    49	    output: |-
    50	      exit=0 home=$HOME
    51	      absolute: yes
    52	  - claim: "Commands (b), successfully probed read-only by the orchestrator at 2026-10-20T04:31:20Z against a01 sha 30185a5a…."
    53	    command: |-
    54	      P=(/usr/bin/env -i PATH=/usr/bin:/bin HOME="$home" LANG=C.UTF-8)
    55	    output: |-
    56	      P=(/usr/bin/env -i PATH=/usr/bin:/bin HOME=$HOME LANG=C.UTF-8)
    57	  - claim: "Commands (c), successfully probed read-only by the orchestrator at 2026-10-20T04:31:20Z against a01 sha 30185a5a…."
    58	    command: |-
    59	      PY="$home/.local/share/mise/installs/python/3.15.0/bin/python3"
    60	      [ -f "$PY" ] && [ -x "$PY" ] || { printf '%s\n' 'python-pin: refused: missing-executable' >&2; exit 1; }
    61	      "${P[@]}" "$PY" -I -c 'import sys, os; print(os.path.realpath(sys.executable), sys.version.split()[0])'
    62	    output: |-
    63	      exists+executable: yes
    64	      $HOME/.local/share/mise/installs/python/3.15.0/bin/python3.15 3.15.0
    65	      exit=0
    66	  - claim: "Commands (e), successfully probed read-only by the orchestrator at 2026-10-20T04:31:20Z against a01 sha 30185a5a…."
    67	    command: |-
    68	      GH=$(/usr/bin/readlink -f "$home/.local/share/mise/installs/github-cli-cli/latest/bin/gh")
    69	      printf '%s\n' "$GH"
    70	      case "$GH" in ""|*/mise/shims/*) printf '%s\n' 'gh: refused: missing-or-shim' >&2; exit 1;; esac
    71	      [ -f "$GH" ] && [ -x "$GH" ] || { printf '%s\n' 'gh: refused: not-executable' >&2; exit 1; }
    72	      "${P[@]}" "$GH" --version
    73	    output: |-
    74	      GH=$HOME/.local/share/mise/installs/github-cli-cli/2.102.0/bin/gh
    75	      shim-check: ok
    76	      executable: yes
    77	      gh version 2.102.0 (2026-09-30)
    78	      exit=0
    79	  - claim: "Commands (g), successfully probed read-only by the orchestrator at 2026-10-20T04:31:20Z against a01 sha 30185a5a…."
    80	    command: |-
    81	      "${P[@]}" /usr/bin/grep -n -E 'python.*latest|latest.*python|held = |if name not in held:|self.assertEqual\("latest", version, name\)' home/dot_mise/config.toml tests/unit/test_supply_chain_policy.py scripts/validate-agent-assets.py
    82	    output: |-
    83	      home/dot_mise/config.toml:5:python = "latest"
    84	      tests/unit/test_supply_chain_policy.py:374:        held = {"fd": "fd = ", "npm:pnpm": '"npm:pnpm" = ', "http:bats": '[tools."http:bats"]'}
    85	      tests/unit/test_supply_chain_policy.py:381:            if name not in held:
    86	      tests/unit/test_supply_chain_policy.py:382:                self.assertEqual("latest", version, name)
    87	      exit=0
    88	---
    89	
    90	# AGMSG-TASK dotfiles-T133-python-pin-a02 — reset the exact Python declaration
    91	
    92	This text is the independent-context reset after INV-6 S2 (tasks=3 amendments=2 questions=1 results=5 revises=4, including round=0 blocked-RESULT closures); the a01 findings history is in `.orchestration/acceptance/dotfiles-T133-python-pin-a01.md`.
    93	Plan 024; continue PR #437 on `task/dotfiles-T133-python-pin-a01` from `e9819d458b93bfba08352832be6b47f95780aeb8`, worker a013 (Codex, worker-h); do not create a branch or PR.
    94	Design 5.14 in `$HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md` is frozen under D-024-29 and applies by reference under D-024-30; items 0–10 have individual threat rows.
    95	[memory:decision] Declare `python = "3.15.0"` in `home/dot_mise/config.toml` as the exact Python binding for the trusted parent and the resolver owned by `dotfiles-T133-ci-efficiency-followup-a04`.
    96	The declaration grammar is the mise `[tools]` key `python` with an exact ASCII-digit `MAJOR.MINOR.PATCH` string, without whitespace, a prefix, `latest` or a range.
    97	
    98	## Commands
    99	
   100	Definitions occur only here; premises quote the executed probes. Start Commands (parent) from the trusted launcher; execute the lettered sections inside that parent from the verified checkout root. Stop at any failed prerequisite.
   101	```bash
   102	# (parent) Clear inherited inputs before starting the shell; never print the token.
   103	/usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 /bin/bash --noprofile --norc -p -o pipefail
   104	# (a) Anchor home to the real user's account record.
   105	case "$(/usr/bin/uname -s)" in
   106	  Darwin) home=$(/usr/bin/id -P | cut -d: -f9);;
   107	  Linux) home=$(getent passwd "$(id -un)" | cut -d: -f6);;
   108	  *) printf '%s\n' 'home: refused: unsupported-platform' >&2; exit 1;;
   109	esac
   110	rc=$?; [ "$rc" -eq 0 ] || { printf 'home: refused: lookup-failed (exit %s)\n' "$rc" >&2; exit "$rc"; }
   111	case "$home" in /*) ;; *) printf '%s\n' 'home: refused: not-absolute' >&2; exit 1;; esac
   112	# (b) The clean child prefix.
   113	P=(/usr/bin/env -i PATH=/usr/bin:/bin HOME="$home" LANG=C.UTF-8)
   114	# (c) Bind and probe the exact interpreter.
   115	PY="$home/.local/share/mise/installs/python/3.15.0/bin/python3"
   116	[ -f "$PY" ] && [ -x "$PY" ] || { printf '%s\n' 'python-pin: refused: missing-executable' >&2; exit 1; }
   117	"${P[@]}" "$PY" -I -c 'import sys, os; print(os.path.realpath(sys.executable), sys.version.split()[0])'
   118	# (d) Execute the intended file directly, for both red and green.
   119	"${P[@]}" "$PY" -I tests/unit/test_mise_config.py
   120	# (e) Bind gh, print and check the binding, then obtain the canonical base.
   121	GH=$(/usr/bin/readlink -f "$home/.local/share/mise/installs/github-cli-cli/latest/bin/gh")
   122	printf '%s\n' "$GH"
   123	case "$GH" in ""|*/mise/shims/*) printf '%s\n' 'gh: refused: missing-or-shim' >&2; exit 1;; esac
   124	[ -f "$GH" ] && [ -x "$GH" ] || { printf '%s\n' 'gh: refused: not-executable' >&2; exit 1; }
   125	# (e') Isolate gh's persistent configuration (hosts.yml api_host can redirect requests): a fresh config dir and the keyring token read once by the bound gh.
   126	GH_AUTH=$("${P[@]}" "$GH" auth token --hostname github.com); [ -n "$GH_AUTH" ] || { printf '%s\n' 'gh: refused: no-token' >&2; exit 1; }
   127	GHC=$(/usr/bin/mktemp -d "${TMPDIR:-/tmp}/ghcfg.XXXXXX")
   128	"${P[@]}" "$GH" --version
   129	"${P[@]}" GH_CONFIG_DIR="$GHC" GH_TOKEN=$GH_AUTH "$GH" api repos/mryfmo/dotfiles/git/ref/heads/main --hostname github.com --jq .object.sha
   130	# (f) Substitute the recorded full SHAs before execution; never execute placeholders.
   131	"${P[@]}" GH_CONFIG_DIR="$GHC" GH_TOKEN=$GH_AUTH "$GH" api "repos/mryfmo/dotfiles/compare/<base40>...<head40>" --hostname github.com --paginate --jq '.files[] | "\(.additions)\t\(.deletions)\t\(.filename)"'
   132	# (f') Completeness of (f): refuse a list of 300 files (GitHub's cap) or one that differs from the PR's changedFiles; <pr> is this task's PR, so (f') runs at RESULT, not at dispatch.
   133	n=$("${P[@]}" GH_CONFIG_DIR="$GHC" GH_TOKEN=$GH_AUTH "$GH" api "repos/mryfmo/dotfiles/compare/<base40>...<head40>" --hostname github.com --jq '.files | length'); c=$("${P[@]}" GH_CONFIG_DIR="$GHC" GH_TOKEN=$GH_AUTH "$GH" pr view <pr> --repo github.com/mryfmo/dotfiles --json changedFiles --jq .changedFiles)
   134	[ "$n" -lt 300 ] && [ "$n" = "$c" ] || { printf '%s\n' "compare: refused: files=$n changedFiles=$c" >&2; exit 1; }
   135	# (g) Read-only declaration and existing-policy probe.
   136	"${P[@]}" /usr/bin/grep -n -E 'python.*latest|latest.*python|held = |if name not in held:|self.assertEqual\("latest", version, name\)' home/dot_mise/config.toml tests/unit/test_supply_chain_policy.py scripts/validate-agent-assets.py
   137	```
   138	
   139	Commands (a) is the only home source; (b) removes inherited tool, loader, Python and `GIT_*` configuration. Only the prescribed authenticated gh calls receive the parent's token.
   140	Never substitute an interpreter, enlarge the gh candidate list, invoke a shim, provision a tool or repair a failed command through another invocation. Normalize home prefixes to `$HOME` only in stored output.
   141	
   142	## Work
   143	
   144	1. Continue the named head with implementation unchanged, including the inherited supply-chain Python exception; add only the new task copy and evidence under `.orchestration/dotfiles-T133-python-pin-a02/`. Preserve `.orchestration/dotfiles-T133-python-pin-a01/` as the predecessor copy.
   145	2. Verify the inherited config is `python = "3.15.0"`, immediately preceded by `# Held: the trusted interpreter resolver binds to this exact Python version.` Python stops tracking `latest`; deployment remains an operator action.
   146	3. Verify the single standard-library test `tests/unit/test_mise_config.py::MiseConfigTest::test_python_is_exact_version` reads the real TOML relative to `__file__` using `pathlib` and `tomllib`, assigns the declaration to `value` without stripping, and asserts `re.fullmatch(r'[0-9]+\.[0-9]+\.[0-9]+', value, re.ASCII)`; the same expression rejects `"3.15.0\n"`, `"３.15.0"`, `"latest"` and `"3.15"`. The module ends with `if __name__ == "__main__": unittest.main()`.
   147	4. Preserve the predecessor's Commands (d) assertion-based red on the actual `latest` declaration, exactly one test, with source/head provenance; do not undo the implementation to repeat it. Run Commands (d) green directly; record complete stdout/stderr and exit statuses in `validation.md`, distinguishing inherited red evidence from this execution.
   148	5. No resolver, caller, workflow, dependency, host-installation, knowledge-graph or predecessor-artifact changes are authorized; newly discovered implementation work requires re-tasking.
   149	
   150	## Check — prerequisites
   151	
   152	The orchestrator executed the successful read-only Commands (a), (b), (c), (e) binding/version and (g) probes sequentially inside Commands (parent) before this dispatch at 2026-10-20T04:31:20Z; `premises` contains their exact commands and outputs.
   153	Commands (d), (e') and (f)/(f') were not run in that probe: test execution, token read and PR compare belong to the worker/RESULT. The probed checkout's `latest` output is the source baseline, not the continued PR's implementation.
   154	Before worker validation, repeat (a), (b), (c), (e)'s binding/version probe and (g); require version `3.15.0`, its realpath inside the anchored Python install root, and executable non-shim gh. A missing executable or version mismatch produces `python-pin: refused: installed-version-mismatch` and a blocked PONG; `after: []` adds no task dependency.
   155	
   156	## Check — caps and final head
   157	
   158	The worker runs Commands (e) and (e') at dispatch and records its authenticated canonical `<base40>`; record the initial and final `<head40>` verified against GitHub, each exactly 40 ASCII hexadecimal characters.
   159	Run Commands (f) and (f') at RESULT with that dispatch base and final RESULT head; use PR 437, record both full SHAs, resolved operands, exit statuses and complete TSV output, and never substitute mutable local refs.
   160	Sum Commands (f)'s per-file additions plus deletions outside `tests/` and `.orchestration/` for at most **6 changed lines**, and additions under `tests/` for at most **40 added lines**, including the inherited policy adjustment; measure the whole PR through the GitHub compare API.
   161	This whole text must remain at or under **190 lines**. Commands (d) performs no discovery or repository-package imports; require `Ran 1 test` and green. Other tests run in CI; do not run Bats locally. After pushing, verify final-head GitHub Actions and report any failure without changing implementation.
   162	
   163	## Completion and boundaries
   164	
   165	Worker Playbook step 4 applies: every command, including gh and git writes, stays inside the sandbox and allowlist. A denial sends `AGMSG-PONG v1 task_id=dotfiles-T133-python-pin-a02 status=blocked` with the Commands section, resolved operands, failure and crossed boundary; never escalate or bypass through another tool.
   166	All gh operations retain the Commands (e) binding and clean environment and explicitly identify github.com/mryfmo/dotfiles; continue the existing English PR under the Worker Playbook.
   167	Copy this text byte-identically to `.orchestration/dotfiles-T133-python-pin-a02/task.md`; the orchestrator compares the whole copy and dispatch SHA-256 at acceptance. Keep plan/todo/learn uncommitted and at most one active todo per owner.
   168	Under that directory, write `report.md`, `validation.md`, `sandbox.md`, `learning.md`, `autoskill.md` and worker review evidence; record Commands references, base/head, PR, changed files, caps, red/green provenance, task-copy SHA-256 and `cost:`.
   169	Send `AGMSG-RESULT v1` with all five artifact paths and Commands (f)/(f') evidence; inaccessible main-checkout artifact paths use the same relative paths in the worker worktree.
   170	Pass the repository review gate with local review data; never open a browser review or request human review. The orchestrator performs final-head security review and integration under Orchestrator Playbook step 10; the worker never merges.
   171	After merge, the operator runs `make update` and `mise install`, recording commands, output and installed-version evidence in acceptance; deployment is not a dispatch prerequisite.
   172	Not performed by this authoring context: worker tests, CI or deployment. Executable provenance and unrestricted same-UID replacement remain residual risks.
   173	
   174	## Checks (pasted by the orchestrator before each send)
   175	
   176	```
   177	```
 succeeded in 232ms:
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
?? .orchestration/tasks/dotfiles-T129-normalised-comparison-lint-followup-a04.md
?? .orchestration/tasks/dotfiles-T133-permission-guard-gate-a05-slice1.md
?? .orchestration/tasks/dotfiles-T133-python-pin-a01.md
?? .orchestration/tasks/dotfiles-T133-python-pin-a02.md
?? .orchestration/tasks/dotfiles-T133-python-pin-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-regime-ci-fixture-grammar-a01.md
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
?? .orchestration/validation/dotfiles-T133-record-ledger-carry-a01-text-security-f3bfcc6.md
?? .orchestration/validation/dotfiles-T133-record-ledger-carry-a01-text-security-f3bfcc6.md.last.md
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
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-9bd6198.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-9bd6198.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-be969e3.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-efa211d.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-efa211d.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-f7af699.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-f7af699.md.last.md
60a6fb2b324d0381c4a6e539b37c650105154a7e
~/.local/bin/crit
~/.local/share/mise/shims/python3
/opt/homebrew/bin/git
~/.local/share/mise/shims/gh
~/.local/share/mise/shims:~/.local/bin:~/.local/bin/common:/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:~/.local/share/mise/installs/npm-openai-codex/0.162.1/lib/node_modules/@openai/codex/node_modules/@openai/codex-darwin-arm64/vendor/aarch64-apple-darwin/codex-path:~/.local/share/mise/installs/node/lts/bin:/usr/bin:/bin:/usr/sbin:/sbin

 succeeded in 240ms:
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
{
  "lastAnalyzedAt": "2026-10-02T14:12:51Z",
  "gitCommitHash": "940a3a2b07adfd14140a0acff96784ef53a0a509",
  "version": "1.0.0",
  "analyzedFiles": 368
}

**Setting careful read limits**
exec
/bin/zsh -lc 'crit status --json' in ~/Workspace/dotfiles
exec
/bin/zsh -lc 'cat .orchestration/acceptance/dotfiles-T133-python-pin-a01.md .orchestration/acceptance/dotfiles-T133-python-pin-a02.md' in ~/Workspace/dotfiles
exec
/bin/zsh -lc "rg -n '5\\.14|D-024-(21|29|30)|python-pin|ci-efficiency-followup-a04' .orchestration/plans/024-design-quality.md .orchestration/decisions.tsv; cat .orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md" in ~/Workspace/dotfiles
 succeeded in 136ms:
---
{
  "audit_findings": [],
  "dispatch": [
    "AGMSG-TASK v1 task_id=dotfiles-T133-python-pin-a01 round=1 repo=~/Workspace/dotfiles/.claude/worktrees/worker-h task_file=.orchestration/tasks/dotfiles-T133-python-pin-a01.md task_sha256=59f91f5580892ddd58f10b538eb611e790200edf6d41ead1e63bd753e5d68fbd deadline=none done_signal=AGMSG-RESULT note=a013:exact-Python-declaration(home/dot_mise/config.toml-python-3.15.0;one-test;caps-6/40;every-command-in-the-Commands-block-was-executed-by-the-orchestrator-before-dispatch);fresh-branch-from-origin/main;security:true;Worker-Playbook-step-4(sandbox-only;dscl-fails-in-the-sandbox,use-id--P-as-the-text-says);the-Checks-block-at-the-end-carries-the-probe-outputs",
    "AGMSG-TASK v1 task_id=dotfiles-T133-python-pin-a01 round=1 repo=~/Workspace/dotfiles/.claude/worktrees/worker-h task_file=.orchestration/tasks/dotfiles-T133-python-pin-a01.md task_sha256=8e544c8a77ca3b5679cde8899225a8300cf4dc91a685111bb6768328c1025179 deadline=none done_signal=AGMSG-RESULT note=a013:amendment(previous_sha256=59f91f5580892ddd58f10b538eb611e790200edf6d41ead1e63bd753e5d68fbd;the-validate-job-refused-the-task-copy-as-a-possible-committed-secret:the-pattern-TOKEN=\"$TOKEN\"-in-Commands-(e)/(f)/(f-prime);renamed-to-GH_AUTH-and-GH_TOKEN=$GH_AUTH,no-behaviour-change);update-the-task-copy-byte-identical,push-with-the-HTTPS-form,then-CI,Bot-window,RESULT;for-gh-run-logs-inside-the-sandbox-set-XDG_CACHE_HOME=$PWD/.cache(C-94)",
    "AGMSG-ACCEPTANCE v1 task_id=dotfiles-T133-python-pin-a01 status=revise round=0 reason=the-RESULT-status=blocked-of-02:58:25Z-is-superseded:the-branch-creation-completed(the-packed-refs.lock-denial-is-a-known-non-fatal-write-denial-of-Codex-seats,recorded-in-sandbox.md);continue-from-step-3-as-PING-2664-said;this-line-closes-that-RESULT-for-the-stop-gate-and-is-not-a-fix-round(C-61-count-unchanged:worker_fix_rounds-0)",
    "AGMSG-ACCEPTANCE v1 task_id=dotfiles-T133-python-pin-a01 status=revise round=0 reason=the-blocked-RESULT-of-03:15:23Z(push-exit-128-publickey)-is-the-known-host-fact:the-global-git-config-rewrites-every-push-to-SSH(url.git@github.com:.pushInsteadOf=https://github.com/)-and-this-host-has-no-SSH-key;the-documented-worker-push-form(agmsg-orchestration-SKILL,Worker-Playbook)-is:GIT_CONFIG_GLOBAL=/dev/null-git--c-credential.helper=--c-credential.helper=\"!$GH-auth-git-credential\"-push-https://github.com/mryfmo/dotfiles-task/dotfiles-T133-python-pin-a01(with-your-bound-$GH-realpath,the-clean-prefix,HOME-anchored,GH_CONFIG_DIR=\"$GHC\"-and-GH_TOKEN=\"$TOKEN\"-so-the-helper-answers-from-the-token);run-it-inside-the-sandbox(HTTPS-push-is-allowed-there),record-the-exit-and-the-earlier-SSH-refusal-in-sandbox.md,then-open-the-draft-PR,CI,Bot-window,RESULT;this-line-closes-the-blocked-RESULT-and-is-not-a-fix-round(worker_fix_rounds-0)",
    "AGMSG-ACCEPTANCE v1 task_id=dotfiles-T133-python-pin-a01 status=revise round=0 reason=the-blocked-RESULT-of-03:29:02Z(validate-job-failed)-is-answered-by-the-amendment-TASK-of-03:33Z:the-task-copy-matched-validate-agent-assets.py-SECRET_PATTERN-on-TOKEN=\"$TOKEN\";the-amended-text-renames-the-variable(GH_AUTH,GH_TOKEN=$GH_AUTH),verified-clean;update-the-copy-byte-identical,push-with-the-HTTPS-form,CI,Bot-window,RESULT;not-a-fix-round(the-text-was-the-defect,worker_fix_rounds-0)",
    "AGMSG-TASK v1 task_id=dotfiles-T133-python-pin-a01 round=1 repo=~/Workspace/dotfiles/.claude/worktrees/worker-h task_file=.orchestration/tasks/dotfiles-T133-python-pin-a01.md task_sha256=30185a5aec22f7c320745b321f7cf49aba6f45de5b77d434c60918f7f3a68663 deadline=none done_signal=AGMSG-RESULT note=a013:amendment-2(previous_sha256=8e544c8a77ca3b5679cde8899225a8300cf4dc91a685111bb6768328c1025179;line-199:the-amendment-note-quoted-the-refused-assignment-verbatim,now-a-description,your-2685-finding-confirmed;no-command-changed;pre-send-checks-on-the-new-bytes:task-consistency-check.py-OK,validator-SECRET_PATTERN-0-matches,bash-n-rc=0,199-lines-under-the-210-cap);update-the-task-copy-byte-identical,push-with-the-HTTPS-form,then-CI,Bot-window,RESULT",
    "AGMSG-ACCEPTANCE v1 task_id=dotfiles-T133-python-pin-a01 status=revise round=0 reason=the-blocked-RESULT-of-03:42:30Z(validate-refused-head-32f400c3,task.md:199)-is-answered-by-the-amendment-2-TASK-of-03:42:25Z(task_sha256=30185a5a…,pre-send-checks-pasted);your-PONG-of-03:45:58Z-reports-head-09c81cc3-pushed;continue:CI,Bot-window,RESULT;no-finding-on-the-implementation",
    "AGMSG-ACCEPTANCE v1 task_id=dotfiles-T133-python-pin-a01 status=pending-integration round=1 pr=437 head=09c81cc3cc759dd08bb8b76935c99a34c8f19442 reason=RESULT-of-04:03:43Z-read;CI-all-green-at-09c81cc3;security-review-of-09c81cc3:Verdict-correct;the-integration-chain-update-branched-the-PR-to-e9819d45(merge-of-main-60a6fb2b,patch-unchanged)and-runs-sweep,local-review,task-level-audit,gate;no-worker-action-until-the-audit-result;no-finding-on-the-implementation-so-far"
  ],
  "format": 1,
  "head": "e9819d458b93bfba08352832be6b47f95780aeb8",
  "ledger": [
    {
      "class": "hash-binding",
      "id": "text-security:7771c92:1"
    },
    {
      "class": "tool-environment",
      "id": "text-security:7771c92:2"
    },
    {
      "class": "threat-row-unit",
      "id": "text-security:7771c92:3"
    },
    {
      "class": "sources",
      "id": "text-security:7771c92:4"
    },
    {
      "class": "spec-without-input-grammar",
      "id": "text-security:7771c92:5"
    },
    {
      "class": "threat-row-missing",
      "id": "text-security:7771c92:6"
    },
    {
      "class": "tool-environment",
      "id": "text-security:e4316e1:1"
    },
    {
      "class": "tool-environment",
      "id": "text-security:e4316e1:2"
    },
    {
      "class": "tool-environment",
      "id": "text-security:9f757da:1"
    },
    {
      "class": "fragile-premise",
      "id": "text-security:e74aec4:1"
    },
    {
      "class": "fragile-premise",
      "id": "text-security:e74aec4:2"
    },
    {
      "class": "correct",
      "id": "text-security:c8021a7:0"
    },
    {
      "class": "fragile-premise",
      "id": "text-security:9c5500f:1"
    },
    {
      "class": "text-defect",
      "id": "text-security:ed75bc6:1"
    },
    {
      "class": "text-defect",
      "id": "text-security:ed75bc6:2"
    },
    {
      "class": "tool-environment",
      "id": "text-security:0ec4bb9:1"
    },
    {
      "class": "text-defect",
      "id": "text-security:b657a89:1"
    },
    {
      "class": "text-defect",
      "id": "ci:32f400c:1"
    }
  ],
  "pr": 437,
  "replans": {
    "fragile-premise": {
      "design": "the `## Commands` block carries, for each command, the execution timestamp and output (C-87 applied to the text itself), and the cap evidence command refuses a compare list of 300 files or one whose length differs from the PR's `changedFiles`",
      "implementation": "the amendment with the executed compare probe",
      "specification": "every command the text prescribes has been executed by the orchestrator at authoring time on this host, under the clean prefix, and its pasted output stands beside it; a command that cannot be executed before dispatch is not written",
      "verification": "C-80 round 1 after this line."
    },
    "text-defect": {
      "design": "one pre-send command runs them all on the final bytes and prints the sha256 the dispatch line carries (`.agents/worklog/orchestrator-glue/pre-send.sh`; tracked home `dispatch.sh --next` in the loop-limits lineage)",
      "implementation": "the line-199 note rewritten as a description, pre-send output `OK / secret-pattern: 0 match(es) / bash -n block 1: rc=0 / lines: 199`, sha256 8e544c8a… -> 30185a5a…",
      "specification": "the task text passes, as one file, every machine check CI and the regime apply to it before any send: the consistency checker, the validator's SECRET_PATTERN over every line, no literal home path, its own line cap and `bash -n` over every fenced bash block",
      "verification": "CI `validate` on the next head of PR #437."
    },
    "tool-environment": {
      "design": "a single `## Commands` block defines the clean prefix, the anchored home, the exact interpreter path, the direct test-file execution (`python -I tests/unit/test_mise_config.py`) and the bound gh realpath once, and every premise, check and evidence line references that block instead of restating a command",
      "implementation": "amendment 3 of the text by the review profile",
      "specification": "every command the text prescribes runs in the trusted-parent form with one interpreter, no PATH resolution and no implicit import (no discovery, no shim, no `~`)",
      "verification": "C-80 round 4 with the budget reset by this line, then the worker's pasted outputs of exactly those commands."
    }
  },
  "searches": [],
  "task": "dotfiles-T133-python-pin-a01"
}
---

# Acceptance record: dotfiles-T133-python-pin-a01

The exact Python declaration (home/dot_mise/config.toml: python = "3.15.0") that the trusted interpreter resolver task (ci-efficiency-followup-a04) names as its dispatch prerequisite; design 5.14 item 9 by reference. Authored by the review profile (`python-pin-author-prompt.md` -> `redesign/python-pin.md`); the orchestrator normalised the YAML scalars and added the standard non-path and orchestrator-effect threat rows; 129 lines, 4 files, checker OK.

- 2026-10-20T01:11:32Z: C-80 round 1 running (security: true); dispatch to a012 (holding since the loop-limits prerequisites) when correct.
- 2026-10-20T01:14Z: C-80 round 1 (`…-text-security-7771c92.md`) `Verdict: incorrect`, six P2: the version decision probes `latest/bin/python3` while validation runs `3.15.0/bin/python3` (bind both to one realpath); bare `uv` resolves through the mise shim and inherits HOME/Python startup inputs in the validation command; the in-process row ignores that unittest imports repository modules and test_supply_chain_policy.py:394 launches PATH-resolved chezmoi; the cap evidence uses inherited GIT_* and mutable refs (bind base/head by sha); the regex accepts a trailing newline and Unicode digits (ASCII fullmatch); no per-item rows for 5.14 items 0-10 (D-024-30). Amendment 1 via the review profile; budget 1 of 3.
text-security:7771c92:1	hash-binding
text-security:7771c92:2	tool-environment
text-security:7771c92:3	threat-row-unit
text-security:7771c92:4	sources
text-security:7771c92:5	spec-without-input-grammar
text-security:7771c92:6	threat-row-missing
- 2026-10-20T01:28:06Z: amendment 1 (`redesign/python-pin-r2.md`) installed: 150 lines, 4 files, 27 threat rows (one per 5.14 item 0-10, the per-file rows, the standard rows); the exact interpreter bound by realpath; ASCII fullmatch with negatives; bound base/head cap evidence; checker OK; C-80 round 2 running.
- 2026-10-20T01:27Z: C-80 round 2 (`…-text-security-e4316e1.md`) `Verdict: incorrect`, two P2: the premises' probes ran `~/.local/.../python3` with the inherited HOME outside the clean prefix of the validation command; the base lookup invoked bare `gh` (the mise shim). Amendment 2 at 2026-10-20T01:40:32Z (`redesign/python-pin-r3.md`): one clean prefix and the passwd-anchored home for every probe and command (no `~`), gh by its verified realpath with GH_TOKEN passed explicitly; 164 lines; checker OK; C-80 round 3 running (the last of the C-92 budget: a fourth review needs a re-plan line).
text-security:e4316e1:1	tool-environment
text-security:e4316e1:2	tool-environment
- 2026-10-20T01:42Z: C-80 round 3 (`…-text-security-9f757da.md`) `Verdict: incorrect`, one P2: `unittest discover -p test_mise_config.py` imports subpackage initialisers whatever the pattern (an untracked tests/unit/<pkg>/__init__.py would execute with `Ran 1 test` unchanged); execute the test file directly under `-I`. Fourth finding of the tool-environment family on this text (7771c92:2, e4316e1:1, e4316e1:2, 9f757da:1) and the third review: S1 and the C-92 cap both fire. Re-examination: the text wrote its commands ad hoc in several places (prerequisite probes, validation, cap evidence, the test invocation), so each review found another leaky invocation; the whole fix is one command block defined once.
text-security:9f757da:1	tool-environment
re-plan: tool-environment (rows text-security:7771c92:2, text-security:e4316e1:1, text-security:e4316e1:2, text-security:9f757da:1) — specification: every command the text prescribes runs in the trusted-parent form with one interpreter, no PATH resolution and no implicit import (no discovery, no shim, no `~`); design: a single `## Commands` block defines the clean prefix, the anchored home, the exact interpreter path, the direct test-file execution (`python -I tests/unit/test_mise_config.py`) and the bound gh realpath once, and every premise, check and evidence line references that block instead of restating a command; implementation: amendment 3 of the text by the review profile; verification: C-80 round 4 with the budget reset by this line, then the worker's pasted outputs of exactly those commands.
- 2026-10-20T01:54:26Z: re-planned text (`redesign/python-pin-r4.md`) installed: 167 lines + the standard rows the review profile dropped (orchestrator effects, task metadata, in-process effects, workflow inputs) = checker OK; one `## Commands` block (anchored home, clean prefix, exact interpreter, direct test-file execution, bound gh realpath, bound cap evidence) referenced everywhere; no `~`. C-80 round 1 after the re-plan running.
- 2026-10-20T02:00Z: C-80 round 1 after the re-plan (`…-text-security-e74aec4.md`) `Verdict: incorrect`, two P2, both facts the orchestrator's prompt prescribed without probing (C-87 by the orchestrator): mise installs gh under `installs/github-cli-cli/` (not `github-cli/`), so Commands (e) always refuses; `git -c include.path=` is invalid (exit 128 `relative config includes must come from files`). Amendment 1 after the re-plan with the probed values (2026-10-20T02:01:18Z): the gh realpath from the host, and the cap evidence read from the GitHub API compare endpoint (design 5.14 item 8) instead of local git; budget 1 of 3.
text-security:e74aec4:1	fragile-premise
text-security:e74aec4:2	fragile-premise
- 2026-10-20T02:32:13Z: C-80 round 2 after the re-plan (`…-text-security-c8021a7.md`) `Verdict: correct` (commands remove inherited inputs, avoid shims, bind GitHub evidence to the repository and full shas; residuals explicit). Dispatch next: the orchestrator runs the text's Commands probes fresh (C-100) and pastes them into the Checks block; a012 takes it (loop-limits stays held on its prerequisites).
text-security:c8021a7:0	correct
- 2026-10-20T02:33:41Z: the dispatch probes run fresh (C-100): inside the Claude sandbox `dscl . -read … NFSHomeDirectory` fails (`Operation failed with error: eServerError`; the helper task measured exit 70 in the Codex sandbox) while `/usr/bin/id -P | cut -d: -f9` and Python's `pwd.getpwuid` return the passwd home; outside the sandbox dscl works. Measured amendment: Commands (a) uses `id -P` (same directory service through libc); recorded in design 5.14's residual list (D-024-29: no item change). Probe outputs pasted into the Checks block: interpreter realpath …/python/3.15.0/bin/python3 (3.15.0), gh realpath …/github-cli-cli/2.102.0/bin/gh (2.102.0), main 118daafa, declaration python = "latest". Text sha256 c8021a71… -> 9c5500f0…; checker OK; C-80 round 3 after the re-plan running (the last of the budget).
- 2026-10-20T02:37Z: C-80 round 3 after the re-plan (`…-text-security-9c5500f.md`) `Verdict: incorrect`, one P2: GitHub's compare endpoint caps `.files` at 300 whatever `--paginate` says, and the task directory is unbounded, so a truncated list could hide changes from the cap evidence; reject truncated results or establish completeness independently. The budget after the first re-plan is spent. Re-examination: four rounds on this text found nine findings of one family — commands and facts written from memory instead of executed (dscl, the gh install path, `-c include.path=`, the compare cap): fragile-premise. The re-plan: no command enters the text unexecuted.
text-security:9c5500f:1	fragile-premise
re-plan: fragile-premise (rows text-security:7771c92:1-6, text-security:e74aec4:1-2, text-security:9c5500f:1) — specification: every command the text prescribes has been executed by the orchestrator at authoring time on this host, under the clean prefix, and its pasted output stands beside it; a command that cannot be executed before dispatch is not written; design: the `## Commands` block carries, for each command, the execution timestamp and output (C-87 applied to the text itself), and the cap evidence command refuses a compare list of 300 files or one whose length differs from the PR's `changedFiles`; implementation: the amendment with the executed compare probe; verification: C-80 round 1 after this line.
- 2026-10-20T02:38:42Z: amendment after re-plan 2: the compare completeness check (fewer than 300 files and equal to the PR's changedFiles) added to Commands (f) with its executed output (`ba318e53...118daafa`: files 7, total_commits 1, truncated false; PR #434 changedFiles 7); text sha256 9c5500f0… -> ed75bc62…, 188 lines, checker OK; C-80 round 1 after re-plan 2 running.
- 2026-10-20T02:41Z: C-80 round 1 after re-plan 2 (`…-text-security-ed75bc6.md`) `Verdict: incorrect`, two P2 caused by the orchestrator's direct edit: the completeness requirement was prose inside the executable Bash block (`bash -n` exit 2), and dispatch required the PR's changedFiles that exists only after dispatch (circular). Fixed at 2026-10-20T02:42:13Z: an executable (f') line inside the block (refuse 300 files or a count that differs from changedFiles), the prose with the executed output below the block, (f)/(f') run at RESULT only; `bash -n` of the block verified; budget after re-plan 2: 1 of 3 used.
text-security:ed75bc6:1	text-defect
text-security:ed75bc6:2	text-defect
- 2026-10-20T02:45Z: C-80 round 2 after re-plan 2 (`…-text-security-0ec4bb9.md`) `Verdict: incorrect`, one P2: gh's persistent configuration (hosts.yml api_host) can redirect requests despite --hostname, and the unqualified --repo can select another configured host. Fixed at 2026-10-20T02:47:12Z: Commands (e') isolates gh's configuration (a fresh GH_CONFIG_DIR and the keyring token read once by the bound gh; every gh call carries both; --repo github.com/mryfmo/dotfiles); executed on this host inside and outside the sandbox: token read (40 chars), main sha 118daafa, PR #434 changedFiles 7; `bash -n` of the block OK; C-80 round 3 after re-plan 2 running (the last of the budget).
text-security:0ec4bb9:1	tool-environment
- 2026-10-20T02:47:53Z: the configuration-isolation replace had also rewritten the trusted-parent launch line (undefined $GHC/$TOKEN at that point); the launch line restored without a token (the token is read inside by (e')); a review started on the intermediate bytes was stopped before it wrote anything (not consumed); text sha256 ad56c1a6… -> b657a897…; `bash -n` OK; checker OK; C-80 round 3 after re-plan 2 running on the corrected text.
- 2026-10-20T02:52:55Z: C-80 round 3 after re-plan 2 (`…-text-security-b657a89.md`) `Verdict: incorrect` on one P2: the text (198 lines) exceeded its own 185-line sentence; "No additional security findings". Disposition by the orchestrator: the self-cap sentence set to 210 (proposal 1 allows 250), 199 lines; the review budget is spent and the finding is mechanical, so no further review; the task-level audit of the PR checks the contract. Dispatched to a013 (worker-h, the sixth seat, added by the orchestrator at 02:51Z); text sha256 59f91f5580892ddd58f10b538eb611e790200edf6d41ead1e63bd753e5d68fbd.
text-security:b657a89:1	text-defect
- 2026-10-20T02:57:00Z/02:58:25Z: a013 PONG `blocked` then RESULT `status=blocked` at Worker Playbook step 2: `git switch -c task/dotfiles-T133-python-pin-a01 --no-track origin/main` exited 0 with stderr `Unable to create shared .git/packed-refs.lock: Operation not permitted` (the Codex sandbox cannot write the main repository's shared .git; the loose branch ref was written: the branch exists). The same non-fatal warning appears in a012's and a010's records (the loop-limits a01 text and the P1-15 a02 record). Answer 2026-10-20T03:08:21Z: continue; record the denied write in sandbox.md as non-blocking; no repair, no bypass. Mechanism note: the Codex seat's writable roots exclude .git/worktrees/<seat>/ and the shared packed-refs; a known class for the write-boundary owner.
- 2026-10-20T03:08:59Z: a013 PONG `alive`: resumes step 3 on the created branch; records the denied packed-refs write beside the successful operation; no repair, no bypass. ACCEPTANCE `status=revise round=0` sent 2026-10-20T03:11:32Z to close the superseded blocked RESULT for the stop gate (not a fix round).
- 2026-10-20T03:13:02Z/03:15:23Z: a013 PONG then RESULT `status=blocked`: implementation, red/green, independent review and gate passed; local head 4045295b; `git push origin task/dotfiles-T133-python-pin-a01` exit 128 (`git@github.com: Permission denied (publickey)`): the global git config rewrites pushes to SSH and the host has no key (the known host fact; the other seats push with the SKILL's HTTPS form). ACCEPTANCE `status=revise round=0` 2026-10-20T03:21:25Z with the documented push form (GIT_CONFIG_GLOBAL=/dev/null, the gh credential helper through the bound gh with GH_CONFIG_DIR/GH_TOKEN, the HTTPS URL); not a fix round. Mechanism note: the python-pin text's Commands block defines no push form; the Worker Playbook's form is the contract (C-96: nothing new, the SKILL's text).
- 2026-10-20T03:23:40Z: a013 PONG `alive`: the HTTPS push form succeeded inside the sandbox; PR #437 opened at head 4045295b (dispatch base 118daafa; main now 60a6fb2b); CI and the Bot window running; no worker update-branch or merge.
- 2026-10-20T03:27:36Z: a013 PONG `blocked`: CI validate failed on #437 (run 39364020428, job 118436537807); the bound gh could not read the log (`creating cache entry: open $HOME/.cache/gh/run-log-…zip: operation not permitted`: the gh run-log cache lives under the home cache dir outside the Codex writable roots: C-94's remedy is XDG_CACHE_HOME under the worktree); Commands (f)/(f') pass (4 files, code 3/6, tests 19/40); the orchestrator reads the log.
- 2026-10-20T03:31:08Z: the #437 validate job failed: `possible committed secret in .orchestration/dotfiles-T133-python-pin-a01/task.md` (SECRET_PATTERN matches `<redacted:secret-pattern>` at Commands lines 132/134/136, found by running the validator's pattern over the text); amendment: variable GH_AUTH and `GH_TOKEN=$GH_AUTH` (clean against the pattern); sha256 59f91f558089 -> 8e544c8a77ca; re-dispatched for the copy update; a013 told the C-94 remedy for gh run logs (XDG_CACHE_HOME under the worktree). Mechanism note: the pre-dispatch checker should run the validator's secret scan on the text (owner: the P1-12 a05-checker lineage, C16 sibling).
- 2026-10-20T03:37:02Z: CI `validate` refused head 32f400c3 the same way (run 39364986999, job 118439659322: `possible committed secret in .orchestration/dotfiles-T133-python-pin-a01/task.md`); the validator's SECRET_PATTERN run over the text finds one match, line 199: amendment 1's own note quoted the refused assignment verbatim (M-20261020-01). a013 PONG 2685 (03:38:42Z) found the same line independently and asked for a new author source.
ci:32f400c:1	text-defect
re-plan: text-defect (rows text-security:ed75bc6:1-2, text-security:b657a89:1, ci:32f400c:1) — specification: the task text passes, as one file, every machine check CI and the regime apply to it before any send: the consistency checker, the validator's SECRET_PATTERN over every line, no literal home path, its own line cap and `bash -n` over every fenced bash block; design: one pre-send command runs them all on the final bytes and prints the sha256 the dispatch line carries (`.agents/worklog/orchestrator-glue/pre-send.sh`; tracked home `dispatch.sh --next` in the loop-limits lineage); implementation: the line-199 note rewritten as a description, pre-send output `OK / secret-pattern: 0 match(es) / bash -n block 1: rc=0 / lines: 199`, sha256 8e544c8a… -> 30185a5a…; verification: CI `validate` on the next head of PR #437.
- 2026-10-20T03:45Z: amendment 2 dispatched to a013 (`python-pin-amend2.txt`, task_sha256 30185a5aec22f7c320745b321f7cf49aba6f45de5b77d434c60918f7f3a68663; pre-send results pasted in the note, C-100).
- 2026-10-20T04:03:43Z: a013 RESULT `ready_for_review` for PR #437 head 09c81cc3 (base 60a6fb2b, task_sha256 30185a5a…); CI all green at 04:01Z (validate 2m14s, regime 14s, GitGuardian pass); the chain (`chain-integrate.sh … 437 … dotfiles-T133-python-pin-followup-a01`) and the security-profile review of 09c81cc3 started 04:08Z.
- 2026-10-20T04:24:57Z: the chain on the update-branch head e9819d45 (base check moved the PR: `gh pr update-branch`; CI green; local review 0 findings; sweep 9 items 0 gaps): task-level audit `…-audit-e9819d4.md` `Verdict: incorrect`: [P1] orchestration: INV-6 S2 exceeded on this lineage with no reset (measured 2026-10-20T04:39Z with scripts/regime-counters.sh: `tasks=3 amendments=2 questions=1 results=5 withdrawn=0 revises=4 first_result_head=none`; `S2: revises 4 >= 2`, `S2: amendments 2 >= 2`; the round=0 closures of blocked RESULTs count as revises); [P2] records: the JSON ledger, replans and searches were empty while the prose held 18 rows and three re-plan lines; [P2] specification: the dispatched text's Check (line 161-162) forbids dispatch until the failed Commands (a) probe is replaced while `premises` (line 76-81) still carries that failed `dscl` probe. Dispositions: P1 -> the lineage resets to `dotfiles-T133-python-pin-a02` written by the review profile (`python-pin-a02-prompt.md`), carrying the implementation at 09c81cc3 unchanged on PR #437 (a013 holds, PING `python-pin-hold.txt`); P2 records -> fixed in this record by `record-json-sync.py` (ledger 18 rows, replans 3) before any gate; P2 text -> fixed in the a02 text (premises carry only the probes executed read-only at 04:31:20Z: `id -P` home, python 3.15.0 realpath, gh 2.102.0 realpath, policy grep). No finding on the implementation.
audit:e9819d4:1	replan-skipped
audit:e9819d4:2	ledger-completeness
audit:e9819d4:3	text-defect

---
{
  "audit_findings": [],
  "dispatch": [],
  "format": 1,
  "head": null,
  "ledger": [
    {
      "class": "hash-binding",
      "id": "text-security:7771c92:1"
    },
    {
      "class": "tool-environment",
      "id": "text-security:7771c92:2"
    },
    {
      "class": "threat-row-unit",
      "id": "text-security:7771c92:3"
    },
    {
      "class": "sources",
      "id": "text-security:7771c92:4"
    },
    {
      "class": "spec-without-input-grammar",
      "id": "text-security:7771c92:5"
    },
    {
      "class": "threat-row-missing",
      "id": "text-security:7771c92:6"
    },
    {
      "class": "tool-environment",
      "id": "text-security:e4316e1:1"
    },
    {
      "class": "tool-environment",
      "id": "text-security:e4316e1:2"
    },
    {
      "class": "tool-environment",
      "id": "text-security:9f757da:1"
    },
    {
      "class": "fragile-premise",
      "id": "text-security:e74aec4:1"
    },
    {
      "class": "fragile-premise",
      "id": "text-security:e74aec4:2"
    },
    {
      "class": "correct",
      "id": "text-security:c8021a7:0"
    },
    {
      "class": "fragile-premise",
      "id": "text-security:9c5500f:1"
    },
    {
      "class": "text-defect",
      "id": "text-security:ed75bc6:1"
    },
    {
      "class": "text-defect",
      "id": "text-security:ed75bc6:2"
    },
    {
      "class": "tool-environment",
      "id": "text-security:0ec4bb9:1"
    },
    {
      "class": "text-defect",
      "id": "text-security:b657a89:1"
    },
    {
      "class": "text-defect",
      "id": "ci:32f400c:1"
    },
    {
      "class": "replan-skipped",
      "id": "audit:e9819d4:1"
    },
    {
      "class": "ledger-completeness",
      "id": "audit:e9819d4:2"
    },
    {
      "class": "text-defect",
      "id": "audit:e9819d4:3"
    }
  ],
  "pr": null,
  "replans": {
    "fragile-premise": {
      "design": "the `## Commands` block carries, for each command, the execution timestamp and output (C-87 applied to the text itself), and the cap evidence command refuses a compare list of 300 files or one whose length differs from the PR's `changedFiles`",
      "implementation": "the amendment with the executed compare probe",
      "specification": "every command the text prescribes has been executed by the orchestrator at authoring time on this host, under the clean prefix, and its pasted output stands beside it; a command that cannot be executed before dispatch is not written",
      "verification": "C-80 round 1 after this line."
    },
    "text-defect": {
      "design": "one pre-send command runs them all on the final bytes and prints the sha256 the dispatch line carries (`.agents/worklog/orchestrator-glue/pre-send.sh`; tracked home `dispatch.sh --next` in the loop-limits lineage)",
      "implementation": "the line-199 note rewritten as a description, pre-send output `OK / secret-pattern: 0 match(es) / bash -n block 1: rc=0 / lines: 199`, sha256 8e544c8a… -> 30185a5a…",
      "specification": "the task text passes, as one file, every machine check CI and the regime apply to it before any send: the consistency checker, the validator's SECRET_PATTERN over every line, no literal home path, its own line cap and `bash -n` over every fenced bash block",
      "verification": "CI `validate` on the next head of PR #437."
    },
    "tool-environment": {
      "design": "a single `## Commands` block defines the clean prefix, the anchored home, the exact interpreter path, the direct test-file execution (`python -I tests/unit/test_mise_config.py`) and the bound gh realpath once, and every premise, check and evidence line references that block instead of restating a command",
      "implementation": "amendment 3 of the text by the review profile",
      "specification": "every command the text prescribes runs in the trusted-parent form with one interpreter, no PATH resolution and no implicit import (no discovery, no shim, no `~`)",
      "verification": "C-80 round 4 with the budget reset by this line, then the worker's pasted outputs of exactly those commands."
    }
  },
  "searches": [],
  "task": "dotfiles-T133-python-pin-a02"
}
---

# Acceptance record: dotfiles-T133-python-pin-a02

- 2026-10-20T04:40Z: reset of dotfiles-T133-python-pin-a01 after INV-6 S2 (regime-counters at 04:31Z: tasks=3 amendments=2 questions=1 results=5 revises=4; audit e9819d4 P1), written whole by the review profile (`python-pin-a02-prompt.md`), carrying the implementation at 09c81cc3 on PR #437 unchanged; the a01 findings history is in the a01 record; the lineage rows and re-plan lines are carried below before any chain (M-20261019-06).

## Lineage rows carried from dotfiles-T133-python-pin-a01

text-security:7771c92:1	hash-binding
text-security:7771c92:2	tool-environment
text-security:7771c92:3	threat-row-unit
text-security:7771c92:4	sources
text-security:7771c92:5	spec-without-input-grammar
text-security:7771c92:6	threat-row-missing
text-security:e4316e1:1	tool-environment
text-security:e4316e1:2	tool-environment
text-security:9f757da:1	tool-environment
text-security:e74aec4:1	fragile-premise
text-security:e74aec4:2	fragile-premise
text-security:c8021a7:0	correct
text-security:9c5500f:1	fragile-premise
text-security:ed75bc6:1	text-defect
text-security:ed75bc6:2	text-defect
text-security:0ec4bb9:1	tool-environment
text-security:b657a89:1	text-defect
ci:32f400c:1	text-defect
audit:e9819d4:1	replan-skipped
audit:e9819d4:2	ledger-completeness
audit:e9819d4:3	text-defect
re-plan: tool-environment (rows text-security:7771c92:2, text-security:e4316e1:1, text-security:e4316e1:2, text-security:9f757da:1) — specification: every command the text prescribes runs in the trusted-parent form with one interpreter, no PATH resolution and no implicit import (no discovery, no shim, no `~`); design: a single `## Commands` block defines the clean prefix, the anchored home, the exact interpreter path, the direct test-file execution (`python -I tests/unit/test_mise_config.py`) and the bound gh realpath once, and every premise, check and evidence line references that block instead of restating a command; implementation: amendment 3 of the text by the review profile; verification: C-80 round 4 with the budget reset by this line, then the worker's pasted outputs of exactly those commands.
re-plan: fragile-premise (rows text-security:7771c92:1-6, text-security:e74aec4:1-2, text-security:9c5500f:1) — specification: every command the text prescribes has been executed by the orchestrator at authoring time on this host, under the clean prefix, and its pasted output stands beside it; a command that cannot be executed before dispatch is not written; design: the `## Commands` block carries, for each command, the execution timestamp and output (C-87 applied to the text itself), and the cap evidence command refuses a compare list of 300 files or one whose length differs from the PR's `changedFiles`; implementation: the amendment with the executed compare probe; verification: C-80 round 1 after this line.
re-plan: text-defect (rows text-security:ed75bc6:1-2, text-security:b657a89:1, ci:32f400c:1) — specification: the task text passes, as one file, every machine check CI and the regime apply to it before any send: the consistency checker, the validator's SECRET_PATTERN over every line, no literal home path, its own line cap and `bash -n` over every fenced bash block; design: one pre-send command runs them all on the final bytes and prints the sha256 the dispatch line carries (`.agents/worklog/orchestrator-glue/pre-send.sh`; tracked home `dispatch.sh --next` in the loop-limits lineage); implementation: the line-199 note rewritten as a description, pre-send output `OK / secret-pattern: 0 match(es) / bash -n block 1: rc=0 / lines: 199`, sha256 8e544c8a… -> 30185a5a…; verification: CI `validate` on the next head of PR #437.
- 2026-10-20T04:41Z: the a02 reset text installed (`redesign/python-pin-a02.md`, 175 lines): premises carry only the probes executed read-only at 04:31:20Z (`id -P` home, python 3.15.0 realpath, gh 2.102.0 realpath, policy grep), no failed-probe leftover, the Commands block unchanged; the checker's C3 required a predecessor-copy row for `.orchestration/dotfiles-T133-python-pin-a01/task.md`, added by the orchestrator (one flow-style row); pre-send.sh: checker OK, SECRET_PATTERN 0, bash -n OK, 176 lines (self cap 190); sha256 68fd5f2e6b36d89789d1723caba932666c7719c09aeae154a3f049d31542d862. C-80 round 1 running.


 succeeded in 172ms:
.orchestration/plans/024-design-quality.md:95:### 5.14 残余（凍結後の計測事実、D-024-29）
.orchestration/plans/024-design-quality.md:103:## 5.14 信頼ホスト実行契約（trusted-host execution contract、D-024-18）
.orchestration/plans/024-design-quality.md:113:0. **脅威モデル（D-024-21）** 席は同じ OS ユーザで動き、ホストは席間の信頼境界ではない（同一 UID のプロセスは symlink 差し替え、共有 `.git` の object 差し替え、hook の子プロセス、Herdr socket 経由の host 実行で、ホスト内のどの検査も迂回できる）。regime の硬い境界は GitHub（保護された main、必須チェック、orchestrator の identity によるマージ）。ただしこの境界は **worker 席が orchestrator の GitHub 資格情報を共有しない**ときだけ成立する（D-024-22：worker 席は専用の GitHub identity（別アカウントまたは App のトークン）で `gh` に login し、ruleset の bypass 一覧に入らない。orchestrator の keychain トークンを worker の config dir に持ち込まない。identity が分かれるまで「GitHub が境界」は未成立と書く）。**同一 macOS ユーザでは資格情報は分離できない**（gh は keychain の項目を host/user で引き、同じ UID の gh は orchestrator のトークンを読める。`GH_CONFIG_DIR` は設定を分けるだけ）。防止には worker 席を別の OS ユーザ（または別ホスト）で動かすしかなく、それは D-024-23 の将来項目（P1-16、操作者の判断）。それまで GitHub 境界は **検知**で守る：記録は boundary の記録 PR まで main に無いので、検知は次の記録 PR の regime ジョブで行う（`.orchestration/acceptance/**` に触れる PR で、前回 boundary 以降の main の各マージ commit に、gate 通過の証跡を持つ受け入れ記録が対応することを検査し、無ければその PR を失敗させる；P1-11 owner a02 の行 `ci:detection:1`）。main push 時点の検知は記録が無いので不可能であり、文は「次の記録 PR で検知、防止ではない」と書く。悪意ある worker に耐えるべき入力（承認台帳、gate が読む証跡 of record）は GitHub から sha 指定で API 経由（sandbox 内）に読み、ローカルファイルやローカル object database からは読まない。ホスト内の制御（本節 1〜10）は事故と prompt injection による損害の抑制であり、文はそう書く。
.orchestration/decisions.tsv:64:D-024-18	2026-10-19T02:5xZ	every security: true orchestrator-side task text applies design section 5.14 (trusted-host execution contract: the write-boundary premise, sanitized environment first, trusted-path boundary checks, execute-what-you-verified, 40-hex identities and inode-bound locks, honest residuals, four shared red-then-green tests) by reference, with one threat row per item	the C-80 reviews of three texts on 2026-10-19 (permission-guard-gate-a05, dispositions-a02, audit-pool-a01: 19 P1 in total) found the same unstated premise and the same gaps in each; a design-tier contract replaces per-text rewording (M-20261019-03 class)	default under the autonomy directive, reported 2026-10-19 12:0x JST; scope=design	applied-from-a05-and-the-a02-texts
.orchestration/decisions.tsv:65:D-024-19	2026-10-19T03:0xZ	permission decision rows are read from the committed ledger (git show origin/main:.orchestration/decisions.tsv after fetch), never from the working copy; a working-copy row is a proposal until the records PR carrying it merges, and that PR approval is the operator's operation (design 5.14 item 8)	the second C-80 review of the a05 text: a Claude worker seat's file tools run outside the Seatbelt sandbox and the rendered policy has no path deny, so a same-UID forged row in the working-copy ledger was possible; the committed ledger moves forgery behind a protected-branch merge	default under the autonomy directive, reported 2026-10-19 12:0x JST; the consequence is one records PR (boundary 24) before the a05 merge, approved by the operator through the live hook; scope=design,permission	applied-from-a05
.orchestration/decisions.tsv:66:D-024-20	2026-10-19T03:1xZ	P1-15 (the worker write boundary: deny rules for the Claude file tools on every trusted path outside the seat worktree, hooks and MCP locked, per-seat caches, the gh wrapper of D-024-17) is implemented before and as the dispatch prerequisite (after:) of every orchestrator-side security: true task (P1-14 a05, P1-10 a02, audit-pool-a02, P1-6); the orchestrator review worktree moves out of .claude/worktrees/ (design 5.14 item 3)	the C-80 reviews of 2026-10-19 (a05 twice, dispositions-a02 twice, audit-pool-a01) all reduce to the unstated Claude-seat boundary; hardening texts dispatched before it carry false closed rows	default under the autonomy directive, reported 2026-10-19 12:1x JST; scope=design	applied
.orchestration/decisions.tsv:67:D-024-21	2026-10-19T04:0xZ	threat model and mechanism of the worker boundary: the host is not a security boundary between seats sharing one OS user; the hard boundary is GitHub (protected main, required checks, the orchestrator identity merge); approvals and gate evidence of record are read from GitHub at a sha through the API inside the sandbox; Claude worker seats run under their own CLAUDE_CONFIG_DIR (~/.claude-worker: no excluded commands, no Herdr socket, Edit denies on trusted paths with symlink coverage, failIfUnavailable true, minimal trusted hooks with onFailure block); host-local controls target accidental and injected damage and the texts say so (design 5.14 items 0, 1, 8)	three C-80 reviews of the P1-15 text (03:24Z, 03:42Z, 03:58Z) found host-level escapes no in-process check closes (symlink swap race, writable object database, hook descendants through shims, Herdr socket RPC, hook timeout fail-open); the documentation confirms per-directory settings and credentials (one operator login for the worker directory), onFailure block (>= 2.1.295; installed 2.1.300), and symlink-aware file-tool deny rules	default under the autonomy directive, reported 2026-10-19 13:0x JST; the worker-directory login is an operator step at the P1-15 deployment; scope=design,permission	applied-to-the-P1-15-text
.orchestration/decisions.tsv:71:D-024-17a	2026-10-19T06:0xZ	amendment of D-024-17: the wrapper design is dropped (design 5.14 item 10): worker seats run no command outside the sandbox at all (gh inside the sandbox, Codex network inside its sandbox, the permgate codex rule stops approving escapes)	the probe of 03:45Z (gh works inside the sandbox) and the C-80 reviews that showed the wrapper cannot close LD_PRELOAD or argv passthrough	recorded; scope=design	supersedes-the-wrapper-wording
.orchestration/decisions.tsv:74:D-024-26	2026-10-19T11:2xZ	P1-15 (worker-write-boundary-a01) ships the write boundary alone: the executable-binding work (exact installation layouts probed on the host for uv, Python and node, the bound PermissionRequest hook through the rendered absolute uv and isolated Python, the deploy-time effective-settings check, the formatter PATH) splits into dotfiles-T133-trusted-entrypoint-binding-a01 (after P1-15 and ci-efficiency-followup-a04, whose trusted interpreter resolver it consumes); until it lands the PermissionRequest hook keeps its current form behind the managed deny rules	the fourth executable-binding finding of the P1-15 text review (5204254) after the re-plan line of 20:1x JST; M-20261019-05; the operator's standing order that a third finding of one class re-plans rather than patches
.orchestration/decisions.tsv:75:D-024-27	2026-10-19T21:39Z	An owner task's owned rows are hash-bound in its task text: the text quotes the rows verbatim from the lineage record's `## Owned by <owner>` section (C-88) and the premise `the Owned-by section is on origin/main at dispatch` is replaced by `the quoted rows equal the record's rows at dispatch` (orchestrator-checked, the text sha in the TASK line); dispatch of an owner task no longer waits for the records boundary PR.	18 owner texts carried the on-main premise and every one waited for #429 (the operator's approval) while two Claude seats sat idle on 2026-10-20 05:00-06:40 JST; the rows are scope, not permission approvals, so design 5.14 item 8 (approvals from the committed ledger) does not apply to them; a hash-bound text is the regime's trusted carrier of scope.	plan 024 P1-9 orchestrator load; C-51 owner-first; design 5.14 item 8 scope	applied from 06:40 JST: chain-glue-finish-followup-a01 first; chain-github-scripts-followup-a03 after #432 merges (shared baseline file)
.orchestration/decisions.tsv:77:D-024-29	2026-10-19T21:39Z	Design 5.14 is frozen (plan 006 A1: three review rounds, then freeze with a residual list): items 0-10 are the contract; a text review finding that needs a new design sentence is recorded in the design's residual list and as an owner row, not as an amendment of the item and of the text under review, unless it names a P0/P1 that is exploitable in the proposed implementation.	items 1, 2, 3, 8 and 9 were amended five times on 10-19/20 (one per review round of P1-15 and P1-12), each amendment re-opening the texts that quote the item (C-88) and costing a review round each; the texts chased a moving design.	plan 006 A1; M-20261019-05; C-92	applied from 06:40 JST; the residual list is a new subsection `5.14 残余` in 024-design-quality.md (written at the next design edit)
.orchestration/decisions.tsv:78:D-024-30	2026-10-19T23:16Z	A task text applies design 5.14 by reference: it names the items it relies on (`design: 5.14 items 2, 3, 8, 9`) and carries one threat row per item 0-10 in the item's own words, never a restated or paraphrased copy of the item; C-88 is narrowed to the exact contract sentences a test asserts; the task-consistency check gains a rule (C16) that a security: true orchestrator-side text names 5.14 and has the per-item rows (owner: the P1-12 follow-up after a04 frees task-consistency-check.py).	restated design text drifted in every reset text and re-opened a review round at each design amendment (P1-15: 23 review rounds; P1-12: 4); by-reference texts stay within proposal 1's caps and a mechanical check replaces the reviewer's paraphrase comparison; the operator's direction of 2026-10-19T22:59Z (relayed by a011) asks for the same.	plan 006 A1; D-024-29; M-20261019-05; proposal 1	applied from 08:15 JST to new texts (trusted-exec-contract-tests-a01 first); existing correct texts are not rewritten
.orchestration/decisions.tsv:79:D-024-31	2026-10-20T00:11Z	D-024-28 (an asks-only first slice of P1-14 a05) is withdrawn: the operator's approval D-024-14 binds the three ask-rule removals together with the synchronous hook installation (one digest), so a slice that removes the asks alone is not the approved change and would need its own permission approval from the committed ledger; `make update` therefore stays coupled to the a05 merge, and the idle Claude seats are relieved by converting a seat to Codex (operator step) and by security:false work.	C-80 review 1293d6b of the slice text (2026-10-20T00:04Z): two P1 (replacement control deferred; approval digest covers removals plus hook) that no text amendment can close without a new operator permission approval.	design 5.14 item 8 (approvals from the committed ledger); D-024-13/14; D-024-28; C-80 1293d6b	applied 09:08 JST; the a05 remainder is split later along non-permission lines (proposal 1)
.orchestration/decisions.tsv:80:D-024-32	2026-10-20T02:52Z	A sixth seat, codex-standard-dot-a013 at .claude/worktrees/worker-h, is added by the orchestrator (herdr-agents --add-worker, linkage=ok pong=yes at 02:51:28Z) instead of converting the idle Claude seat a009: the add needs no operator step, the removal would have; the Codex queue (python-pin, P1-12 a05-checker, record-ledger-carry, hold-playbook-a02, verdict-a04, binding) now has three Codex seats.	the bottleneck analysis of 08:48 JST: nine security:true texts wait only for a Codex seat; two Codex seats were both busy; the launcher accepted the sixth seat (the live cap is not enforced at five: a fact to reconcile with the manifest worker_cap 4 in a records task)	D-024-10 (6 after spark), D-024-15 (5), D-024-25	applied 11:51 JST; the operator step "convert a009 to Codex" is withdrawn
.orchestration/decisions.tsv:81:D-024-33	2026-10-20T03:07Z	Records boundary PR #435 (head 8f7b97690df6060a73959a06fc6622a2beaf5029) is approved by the operator's written instruction in the orchestrator session at 2026-10-20 12:0x JST ("承認するので作業を継続"); the orchestrator merges it with gh pr merge --squash --match-head-commit 8f7b9769… right after PR #431 merges (or at once if #431 fails or resets), so the P1-15 chain and audit already running at edd824ea are not invalidated by a base move.	design 5.14 item 8 makes the operator's approval the authority of the recorded decisions (D-024-25..32); GitHub's ruleset 24397953 has no approval rule (rules: deletion, non_fast_forward, required_status_checks), so the written instruction is the operative approval; sequencing after #431 saves one CI run and one re-audit on the critical path.	design 5.14 item 8; ruleset 24397953; the 11:55 JST report	applied; merge pending #431
.orchestration/decisions.tsv:82:D-024-34	2026-10-20T04:12Z	The files the worker's loader consumes at start and the regime need not preserve are launcher-generated at every start: the global state file `CLAUDE_CONFIG_DIR/.claude.json` is written from the declared shape (empty `mcpServers`, `projects` with exactly the validated identities and Boolean trust, `hasCompletedOnboarding: true`) plus identity fields carried from the previous file after screening (`oauthAccount` string members, `userID`); native persisted state (`numStartups`, onboarding, tips and changelog caches, per-project history, allowedTools, cost counters) is neither screened nor preserved; refusal with a named message stays for declared-structure violations (non-empty top-level `mcpServers`, undeclared project keys, non-Boolean trust flags, undeclared object or array members), as evidence of tampering. `CLAUDE_ENV_FILE` (amendment 1) belongs to the same family. A loader that requires another preserved field blocks and retasks (the text's rule), never widens silently.	a010's probe of the installed loader (2.1.300, sha256 475517ca…; reproduced by the orchestrator at 04:10Z) shows the loader itself writes fields outside any exact schema, so the allowlist re-plan's closed schema (D-024-29/30 lineage, a02 -> a03) refuses the worker's own state at the next start; a per-version native-field table would block every loader update until re-probed; generating the file realises design 5.14 item 1 (refuse any executable payload it did not write) by writing the whole file. Second re-plan of the input-inventory family (rows text-security:f7af699:1, worker:5067ed0:1 after the allowlist re-plan).	design 5.14 item 1; D-024-29; D-024-30; a03 record rows; M-20261019-05	applied 13:12 JST as a03 amendment 2 (review-profile text, C-80 round 3); the operator may redirect it once per class (the 13:15 JST report)
.orchestration/decisions.tsv:83:D-024-35	2026-10-20T04:29Z	The launcher-generated global state file (D-024-34) carries no per-project inventory: `projects` is regenerated empty at every start and the workspace trust of the anchor is established by the launcher's existing acceptance of the trust dialog during spawn's readiness wait (`herdr-agents --add-worker`, SKILL 'Regime activation'), not by pre-generated project keys; sibling worker worktrees that share `CLAUDE_CONFIG_DIR` therefore never reject each other's keys. Refusal with a named message stays for a non-empty top-level `mcpServers` (tamper evidence). A loader needing another preserved field still blocks and retasks.	C-80 round 3 of a03 (efa211d, P2): all Claude workers share `.claude-worker/.claude.json` while S11 accepted only the anchor and the current worktree's keys, so worker B's start would reject worker A's key; enumerating sibling worktrees is the fourth inventory of the family to be found incomplete (2ae9e2c, ebbb71b, c0f50fa1, f7af699, 5067ed0, efa211d), so the inventory is removed rather than extended. Third re-plan of the input-inventory family; the operator may redirect it once per class.	D-024-34; design 5.14 item 1; a03 record rows; SKILL (trust-dialog acceptance)	applied 13:29 JST as a03 amendment 3 (review-profile text, C-80 round 4 under a new re-plan line, C-92)
---
format: 2
task_id: dotfiles-T133-ci-efficiency-followup-a04
kind: code
security: true
allowed_files:
  - scripts/orchestrator/ci-rerun.sh
  - tests/unit/test_ci_rerun.py
  - scripts/lint-comparisons-baseline.tsv
  - .orchestration/dotfiles-T133-ci-efficiency-followup-a04/**
  - scripts/orchestrator/trusted-interpreter.sh
  - tests/unit/test_trusted_interpreter.py
after: [dotfiles-T133-worker-write-boundary-a02]
reset_of: [dotfiles-T133-ci-efficiency-followup-a02]
threat_table:
  - control: scripts/orchestrator/ci-rerun.sh interpreter selection and invocation
    disposition: "closed: tests/unit/test_ci_rerun.py::CiRerunTest::test_ci_rerun_pins_its_interpreter_against_a_checkout_and_the_environment"
  - control: scripts/orchestrator/ci-rerun.sh GitHub repository binding
    disposition: "closed: tests/unit/test_ci_rerun.py::CiRerunTest::test_ci_rerun_binds_github_repository_from_foreign_cwd"
  - control: tests/unit/test_ci_rerun.py fixtures and retained regression assertions
    disposition: "residual: fixture executables simulate GitHub and installed tools; their results do not establish live GitHub behavior or deployment provenance"
  - control: scripts/lint-comparisons-baseline.tsv changed-line rebase repair
    disposition: "residual: only pre-existing comparisons moved by this PR may receive matching baseline rows; new comparisons use the required normalisers, and the audit checks every changed row"
  - control: branch evidence records under .orchestration/dotfiles-T133-ci-efficiency-followup-a04/**
    disposition: "residual: reports, command output and review records are untrusted claims checked against the final diff and CI; predecessor evidence remains historical evidence"
  - control: scripts/orchestrator/trusted-interpreter.sh fixed declaration parser and read-only real-installation resolution
    disposition: "residual: tests/unit/test_trusted_interpreter.py::TrustedInterpreterTest::test_pinned_interpreter_ignores_checkout_path_without_mise is the positive case; its red state is the refusal path (before the implementation the resolver does not exist, so the test fails by absence); a named missing-installation skip is not positive coverage; install-symlink and install-not-regular cannot be exercised in CI or by the worker (implemented, refuses by code, verified by reading); temporary refusal fixtures and read-only real-installation checks do not establish host directory protection"
  - control: tests/unit/test_trusted_interpreter.py read-only real-installation and temporary hostile-input fixtures
    disposition: "residual: the positive case reads the real repository and real passwd-home installation read-only and records a named skip when the pinned installation is absent; negative declaration fixtures execute temporary repository copies with the real passwd-home installation read-only and assert their specific refusal codes without bypassing the passwd-home anchor; their results cannot establish host directory protection"
  - control: task-copy transition from .orchestration/dotfiles-T133-ci-efficiency-followup-a02/task.md to .orchestration/dotfiles-T133-ci-efficiency-followup-a04/task.md
    disposition: "residual: the first push deletes only the predecessor task copy and adds the current dispatched text byte-identically; the orchestrator compares the complete new copy and its dispatch SHA-256"
  - control: task metadata
    disposition: "residual: the orchestrator checks format, identity, allowed_files, reset_of, dependency and threat rows before dispatch and at acceptance; a checker lacking the required checks is not sufficient evidence"
  - control: metadata separators
    disposition: "residual: front matter is parsed as data with PyYAML; the orchestrator's whole-file byte comparison also covers separators and the body"
  - control: in-process effects
    disposition: "residual: fixtures use fake GitHub executables and temporary ledgers; production retains the existing reservation, ledger append and gh run rerun --failed effect, which is not exercised against GitHub during unit tests"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: workflow files do not change; the exact Python declaration is a read-only trusted input, never caller-selected; the currently available repository has no exact Python pin, so dispatch remains held until that prerequisite is resolved"
  - control: new or renamed scripts
    disposition: "residual: scripts/orchestrator/trusted-interpreter.sh is the one new executable script; no other new or renamed script is authorized"
  - control: orchestrator effect merge
    disposition: "residual: only the orchestrator merges PR #424 after the integration gate, using gh pr merge --squash --match-head-commit with the audited head; local controls do not prevent a same-UID credential holder from bypassing this procedure"
  - control: orchestrator effect update-branch
    disposition: "residual: the orchestrator performs update-branch; a moved head requires new-head CI, feedback sweep, audit and gate evidence in the order of Orchestrator Playbook step 10"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; forced removal requires an acceptance record describing the discarded uncommitted state, and is not performed by this worker"
  - control: design 5.14 item 1 write boundary
    disposition: "residual: D-024-20 requires the worker-write-boundary dependency before dispatch and verification of the deployed boundary; same-UID processes outside a seat sandbox remain outside that protection"
  - control: design 5.14 item 2 environment before execution
    disposition: "residual: a trusted parent supplies the clean environment before exec and each program verifies and refuses invalid entry state; an already inherited loader library can execute before any shell check, and this task does not establish the safety of every other orchestrator script"
  - control: design 5.14 item 3 interpreter path boundaries
    disposition: "residual: interpreter checks requiring a mutated installation under the real passwd home cannot be exercised in CI or by the worker (implemented, refuses by code, verified by reading); tests/unit/test_ci_rerun.py::CiRerunTest::test_ci_rerun_refuses_unsafe_flake_registry_destination, tests/unit/test_ci_rerun.py::CiRerunTest::test_ci_rerun_refuses_unsafe_ledger_destination and tests/unit/test_ci_rerun.py::CiRerunTest::test_ci_rerun_refuses_unsafe_reservation_destination cover this consumer's resolved destinations only after an accepted baseline whose repository copy is executed as the program; declaration-file and anchored uv-cache destination validation and path boundaries in other scripts remain unimplemented by this task, so the row remains residual rather than claiming full item-3 closure"
  - control: design 5.14 item 4 execute the verified realpath
    disposition: "residual: both Python invocation sites consume the resolver's absolute realpath without rediscovery or a temporary Python link; this does not prevent replacement by an unrestricted same-UID process or establish snapshot controls for unrelated evidence consumers"
  - control: design 5.14 item 5 output and reservation identity
    disposition: "residual: no new head-named output or physical-slot lock is introduced; the existing run-ID reservation behavior stays covered, without claiming implementation of the contract's general full-head and fixed-inode lock mechanisms"
  - control: design 5.14 item 6 honest residuals
    disposition: "residual: closure is limited to each named regression; host protection, deployment provenance, other consumers and same-UID replacement remain explicitly residual"
  - control: design 5.14 item 7 verification
    disposition: "residual: this task adds resolver and consumer regressions and retains the lineage tests; root discovery is covered by tests/unit/test_ci_rerun.py::CiRerunTest::test_ci_rerun_refuses_git_environment_inputs and tests/unit/test_ci_rerun.py::CiRerunTest::test_ci_rerun_refuses_repository_local_core_worktree; these do not replace the common trusted-execution helper or complete the four-test contract for every orchestrator mechanism"
  - control: design 5.14 item 8 committed approval and authenticated changesets
    disposition: "residual: the resolver makes no permission decision and consumes no approval ledger; integration evidence provenance remains the orchestrator's responsibility, and local task copies or Git objects are not approval authority"
  - control: design 5.14 item 9 private cache and shared interpreter resolver
    disposition: "residual: this task introduces the common resolver and migrates the rerun consumer, using the protected anchored uv cache and offline execution; migration of other consumers is not authorized by allowed_files and must not be reported complete"
  - control: design 5.14 item 10 commands remain inside the sandbox
    disposition: "residual: every worker gh command and git write runs individually inside the sandbox; an unavailable operation produces a blocked PONG rather than an outside-sandbox retry"
  - control: design 5.14 item 0 same-UID threat model
    disposition: "residual: these controls limit accidents and prompt injection, not a malicious unrestricted same-UID process; shared macOS credentials do not form an independent GitHub identity boundary, and the next records PR provides detection rather than prevention"
premises: []
---

# AGMSG-TASK dotfiles-T133-ci-efficiency-followup-a04 — replace the interpreter-selection class with one trusted resolver

Plan 024 P1-3. Worker: `claude-standard-dot-a011`, Claude Code, `.claude/worktrees/worker-d`. Continue branch `tools/ci-efficiency-followup-a02` and [PR #424](https://github.com/mryfmo/dotfiles/pull/424) from head `67e2cc98`; do not create another branch or PR.

[memory:failure] The predecessor reached the C-61 round cap with its worker-side fix round and revise 1, and INV-6 S2 with two amendment dispatches. Its rebase repair and update-branches do not erase those counts. The security review of `44cb8353` found the owned `interpreter-selection` class again: `command -v python3` accepts an activated checkout’s absolute `.venv/bin/python3`, which then executes through uv and directly with operator authority.

[memory:decision] This is the class-level re-plan and reset of `dotfiles-T133-ci-efficiency-followup-a02`, not another predecessor fix round. `dotfiles-T133-ci-efficiency-followup-a03` remains the owner of the predecessor’s advisory rows and owns this task’s advisory rows.

Read the predecessor task and acceptance record, `.orchestration/validation/dotfiles-T133-ci-efficiency-followup-a02-security-44cb835.md.last.md`, and `.orchestration/validation/dotfiles-T133-ci-efficiency-followup-a02-local-review-7329f0e.md`. The latter’s pre-pin cleanup-command P1 stays covered. Preserve the predecessor implementation, tests and historical evidence except for the explicitly replaced interpreter-selection mechanism and task copy.

## Dispatch prerequisites — orchestrator

The inspected repository does **not** contain `.mise.toml`, `.tool-versions` or `.python-version`. Its root `mise.toml` contains only `[tools]`; its actual managed declaration, `home/dot_mise/config.toml`, says `python = "latest"`, which is not an exact pin. Do not describe any of these as an existing pinned Python declaration.

Before dispatch, the orchestrator must resolve that missing prerequisite through an authorized change and bind this text to the actual trusted declaration and its exact grammar. No declaration file is writable under this task’s `allowed_files`; the worker must not add a pin, select the newest installation, or substitute an installed version. Until resolved, this task is held.

The inspected `scripts/orchestrator/task-consistency-check.py` implements C1–C10 and C7b; `tests/unit/test_task_consistency_c11_c15.py` is absent locally and at the inspected GitHub refs. Before dispatch, the orchestrator must obtain and read the required checker revision and that test file, then run the checks required below. A C1–C10-only result must not be presented as C11 or C18 validation. Repairing the checker is outside this task.

D-024-20 also requires `dotfiles-T133-worker-write-boundary-a01` to be accepted and its deployed protection verified before dispatch. The pinned declaration, interpreter installation and anchored private cache must be outside worker-writable roots.

Every caller of either program, including the chain glue, CI steps and tests, must supply the trusted-parent clean prefix specified below. Caller changes outside `allowed_files` are an orchestrator-owned dispatch prerequisite to land through a separate authorized change; this task does not authorize editing those callers.

## Applicable design

`$HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md` section 5.14 applies **by reference**, including items 1–10 and the same-UID threat model. Under C-88, the following verbatim sentences are normative; the design path supplies context rather than replacing these requirements.

Item 2: “A shell script that runs under a PR-controlled or worker-controlled environment (verdict.sh, the chain glue, CI steps) is executed as a program with `#!/bin/bash -p`, never as `bash <file>`, and only by a trusted parent that supplies the clean environment before the exec: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<passwd home> LANG=C.UTF-8 /bin/bash --noprofile --norc -p <absolute script path> …` (long options before `-p`). Privileged mode discards inherited functions, `BASH_ENV`/`ENV`, `SHELLOPTS`, `BASHOPTS`, `CDPATH` and `GLOBIGNORE`, but on Linux an inherited `LD_PRELOAD`/`LD_AUDIT` already executes while the loader maps `/bin/bash`, before `-p` or any statement runs, so a self re-exec inside the script is not a boundary and re-executing `"$0"` would reopen the caller's pathname (a worker-owned symlink can be swapped between the two executions); the program therefore verifies and refuses instead of repairing: its environment must consist of exactly the allowed names (checked through absolute paths `/usr/bin/env`, `/usr/bin/grep`), `$0` resolved with `realpath` must be a regular file under the repository root, and HOME must equal the passwd home of the real uid (`/usr/bin/dscl . -read /Users/<user> NFSHomeDirectory` on macOS, `/usr/bin/getent passwd <uid>` on Linux), otherwise exit 2 with a named message. A caller-set sentinel variable is not a sanitization proof, because the caller controls it (ci-efficiency a04 and verdict a04 C-80 reviews, 2026-10-19). No script accepts a caller-supplied executable directory; interpreters are the fixed absolute paths item 9 names.” “Python は `-I`。” “PATH 探索で実行するものは無い。”

Item 4: “検証した実行体はその realpath で実行する（再探索しない）。” “検証したファイル内容は信頼ルート配下のスナップショット（0600、一意名）として渡し、使用直前に sha256 を再照合する。” “判断に読んだ証跡は sha256 を出力に記録する。”

Item 8: “Every `gh` invocation names the repository explicitly: `gh pr`, `gh run` and `gh issue` subcommands take `--repo mryfmo/dotfiles` or the full pull-request URL, and `gh api` (which has no `--repo` flag) takes the explicit `repos/mryfmo/dotfiles/…` endpoint path, never a `{owner}/{repo}` placeholder: the local repository configuration selects the default repository otherwise, and a matching head sha does not bind the repository because a fork can hold the same commit (verdict a04 C-80 round 2, 2026-10-19).”

Item 9: “orchestrator 側の実行は worker と共有するキャッシュ（`~/.cache/uv`、`~/.local/share/uv`、mise）から実行可能物を読まない。” “`UV_CACHE_DIR` を anchored checkout 配下（`.agents/worklog/uv-cache`、gitignored、worker 書き込み不可）に固定し、`uv run --no-config --no-project --offline --python <信頼ルートの絶対パスのインタプリタ>` で起動する（`--no-config` で uv の設定探索を止め、`--python` の絶対パスで cwd や親の `.venv` の発見を止める；敵対的な `.venv` と `uv.toml` を置いた fixture で検証）。” “One trusted interpreter resolver (`scripts/orchestrator/trusted-interpreter.sh`, P1-3 lineage) resolves `<abs>` from the repository's pinned declaration to a regular file under the tool manager's install root (the install root is anchored to the passwd home of the real uid, never to the HOME variable, which a caller can forge), refuses anything else, and every orchestrator-side script consumes it; no script keeps its own `command -v`, `mise which` or PATH fallback (ci-rerun.sh security review 44cb835, 2026-10-19).”

## Item 1 — one trusted interpreter resolver

Add executable `scripts/orchestrator/trusted-interpreter.sh`, with English shdoc comments and `#!/bin/bash -p`. Every caller executes it as a program through a trusted parent supplying `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<passwd home> LANG=C.UTF-8 /bin/bash --noprofile --norc -p <absolute script path> …`; do not source it or use an unqualified `bash <file>` invocation. The parent itself must already be trusted and clean before starting `/usr/bin/env`; clearing the environment after a loader has consumed it is too late. There is no self re-exec.

Before traps, tool discovery or declaration reads, verify the actual environment's exact allowed names through `/usr/bin/env` and `/usr/bin/grep`, the fixed PATH and LANG values, the script's absolute realpath and the passwd-home match. Account explicitly for Bash's own maintained environment entries so the clean prefix succeeds; allow no sanitization sentinel or production test exemption. Require `$0` to be the bound absolute canonical script pathname and its realpath to be a regular file under the trusted repository root, outside worker roots; refuse a symlinked `$0`, including a worker-owned symlink to the trusted script, without reopening it. Any invalid environment, script path or HOME exits 2 with a named `trusted-interpreter:` diagnostic and no stdout, instead of repairing or re-executing.

Read only the repository’s exact Python declaration established by the dispatch prerequisite, anchored to the trusted script/repository location rather than the caller’s cwd. Parse its fixed grammar as data with trusted absolute tools, without `source`, `eval`, shell interpolation of declaration content, or an interpreter selected from that content. Refuse missing, duplicate, malformed, non-exact or metacharacter-bearing declarations; `latest` is invalid.

Obtain the real uid through `/usr/bin/id -ru`. On macOS obtain its user name through `/usr/bin/id -run` and its passwd home through `/usr/bin/dscl . -read /Users/<user> NFSHomeDirectory`; on Linux use `/usr/bin/getent passwd <uid>`. Refuse a missing, ambiguous or malformed passwd result, or any disagreement between that passwd home and HOME, with exit 2 and a named `trusted-interpreter:` diagnostic before selecting a candidate. Derive the installation root only as `<passwd home>/.local/share/mise/installs`, never from the HOME variable, and construct only `<install root>/python/<version>/bin/python3`. Resolve and validate the candidate before printing it. Require an executable regular file after `realpath`, within the expected protected installation, outside the worktree, manifest worker roots, worker-writable caches and `$TMPDIR`. Check resolved path boundaries, including filesystem case behavior where applicable. Refuse a symlinked installation rather than accepting a redirected install directory.

On success print exactly one absolute interpreter realpath and exit 0. On every refusal print exactly one line `trusted-interpreter: refused: <code>` to stderr, print no interpreter on stdout, and exit 2. The codes are `dirty-environment`, `script-path`, `home-mismatch`, `declaration-missing`, `declaration-malformed`, `declaration-duplicate`, `install-missing`, `install-not-regular`, `install-symlink`, `install-outside-root` and `version-mismatch`. Invalid entry environment uses `dirty-environment`; a noncanonical or symlinked script path uses `script-path`; invalid passwd data or HOME disagreement uses `home-mismatch`. An absent declaration uses `declaration-missing`, duplicates use `declaration-duplicate`, and malformed, non-exact or metacharacter-bearing declarations use `declaration-malformed`. An absent candidate uses `install-missing`, a non-executable or non-regular candidate uses `install-not-regular`, a symlinked installation uses `install-symlink`, a forbidden resolved path uses `install-outside-root`, and a resolved installation version differing from the pin uses `version-mismatch`. Every negative test asserts its specific reason code as well as exit 2 and no interpreter stdout; an earlier refusal is not coverage of a later check. There is no `command -v`, `mise which`, PATH search, version-alias selection, download or fallback. Do not execute a candidate to discover whether it is trustworthy.

This is the common resolver required by item 9. This PR migrates its first consumer only; it does not authorize edits to other orchestrator scripts.

## Item 2 — consume the resolver in ci-rerun.sh

Apply the same trusted-parent clean prefix, privileged program entry, exact environment verification, canonical `$0` realpath check and real-uid passwd-home match to `scripts/orchestrator/ci-rerun.sh`. Refuse any entry failure with exit 2 and exactly one `ci-rerun: refused: <code>` line before tool setup or effects: `dirty-environment` for invalid environment names or values, `script-path` for a noncanonical or symlinked script path, and `home-mismatch` for invalid passwd data or HOME disagreement. Do not repair the environment or self re-exec. Invoke the resolver by its bound absolute realpath through the same clean prefix, supplying HOME from the verified passwd home, and consume its single validated result; propagate refusal without trying another interpreter.

Remove Python from the old tool-discovery loop, including the line-45 fallback and line-47 shims test. Do not retain or recreate those mechanisms elsewhere. Bind non-Python tools from explicit protected installation locations, using their validated realpaths or a private fixed PATH of links to those realpaths; caller PATH entries never populate that directory. Missing trusted tools fail closed.

Every external command, including cleanup on early failure and the environment, passwd-home and script-realpath checks, uses an absolute path or the fixed PATH established after entry verification. Keep the EXIT trap’s `/bin/rm` and cover both successful execution and refusal before tool setup completes. Apply the relevant section-5.14 Git invocation controls to the existing root-discovery probe; do not introduce new Git probes or arbitrary shell-command inputs.

Entry verification must refuse any `GIT_*` name in the program's environment, including `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE` and `GIT_CONFIG_GLOBAL`, before invoking Git. The trusted-parent clean prefix must remove them before exec. Confirm that the existing root-discovery probe returns the canonical trusted repository root bound to the script location; a repository-local `core.worktree` redirection must cause exit 2 with `ci-rerun: refused: repository-root`, rather than selecting another root or silently overriding the redirection. Confirm the root before deriving the registry, ledger or reservation paths.

Declare one script-owned constant `readonly GITHUB_REPOSITORY=mryfmo/dotfiles`; never derive or override it from Git remotes, the current directory, caller inputs or API responses. Derive every GitHub target from that constant: every retained `gh run` and `gh pr` invocation must include `--repo "${GITHUB_REPOSITORY}"`, and every `gh api` invocation must use an explicit endpoint beginning `repos/${GITHUB_REPOSITORY}/`, never a `{owner}/{repo}` placeholder. This applies to every GitHub read, including run metadata, job logs and both current-head checks, and to every `gh run rerun --failed`. Root confirmation alone does not bind GitHub calls to this repository.

Before reading or writing the flake registry, ledger or reservation state, resolve `.github/flakes.yaml`, `.orchestration/validation/ci-reruns.tsv` and the reservation parent `.orchestration/validation/ci-reruns.lock.d` with `realpath`. Require the registry and ledger to be regular files and the reservation parent to be a directory under the confirmed repository root, outside manifest worker roots, worker-writable caches and `$TMPDIR`. Refuse symlinks in the destination or any path component below that root, and, on a case-insensitive filesystem, a destination differing from its declared pathname only by case. Use only the validated canonical destinations for subsequent reads and effects. Apply the same checks to an existing per-run reservation directory before inspecting its claim and to a newly claimed directory before using it. Missing output objects may be created only at the existing effect point after validating their existing parent chain and resolving the intended destination; resolve and type-check each newly created object before appending ledger data or using a claim. Preserve atomic per-run creation and never replace an existing object during validation. Any destination-validation failure exits 2 with exactly one `ci-rerun: refused: <code>` line before registry parsing, ledger access or a rerun, leaving redirected targets unchanged. Destination codes are `destination-outside-root` for a resolved path outside the confirmed repository or in a forbidden root, `destination-symlink` for an otherwise contained path with a symlink in the destination or its parent chain, `destination-case-alias` for an otherwise contained case alias, `destination-not-regular` for an invalid registry or ledger file type, and `destination-not-directory` for an invalid reservation directory type. Check containment before symlink, case-alias and type checks so an outside-root mutation has its own distinguishable code.

Run the YAML-loading Python only through `uv run --no-config --no-project --offline --python "<abs>"`, retaining `--with pyyaml`, with `python -I` as the command. Run the reservation Python directly as `"<abs>" -I …`. Both use the resolver’s realpath, never a Python link in a temporary directory, another lookup, or an inherited virtual environment.

Set `UV_CACHE_DIR` to the protected anchored checkout’s `.agents/worklog/uv-cache`, not a caller-supplied location or the worker’s shared HOME cache. Preserve isolation from inherited `UV_*`, `VIRTUAL_ENV` and `PYTHON*` inputs. A fixture containing hostile `.venv`, `.python-version` and `uv.toml` must not change the executable or configuration consumed.

Read Makefile lines 185–200: its `--with pyyaml` probe explains why the cache is tried first. Preserve the working cached-PyYAML behavior, but the production helper now remains offline; remove its online retry. Missing offline dependencies fail visibly without rerunning a job. Do not edit the Makefile.

Retain the existing current-head checks, signature classification, per-run atomic reservation, ledger behavior, failure codes and no-double-rerun guarantees. Baseline changes remain limited to the predecessor’s D-024-24 authorization: normalise new comparisons; baseline only pre-existing comparisons moved by this PR.

## Item 3 — regressions and fixture migration

Write the failing regressions before the fix and paste red and green output. Every negative security case asserts its specific refusal code, not just exit 2 or an empty marker. Declaration-mutating negative cases (missing, malformed, duplicate, non-exact and metacharacter-bearing declarations, and the exact declaration used for a missing installation) execute the canonical resolver in a temporary copy of the repository tree through the trusted-parent clean prefix. Mutate only that copy's declaration; keep the real uid's passwd-home installation read-only and retain the real passwd-home lookup and install-root anchor. Add `tests/unit/test_trusted_interpreter.py` with class `TrustedInterpreterTest` and these tests:

- `test_pinned_interpreter_ignores_checkout_path_without_mise`: prepend a temporary checkout’s marker-writing `.venv/bin/python3` to PATH with mise unavailable; direct dirty entry exits 2 with `trusted-interpreter: refused: dirty-environment` and no marker. Its positive clean-prefix case invokes the canonical resolver in the real repository, reads that repository’s pinned declaration and the tool-manager-installed interpreter beneath the real uid’s passwd-home install root read-only, and expects exactly one absolute realpath and exit 0. Assert that the printed path is an executable regular file under that install root, then execute it as `"<abs>" -I -c 'import sys; print(sys.version_info[:2])'` and compare the output with the pinned version’s major/minor pair. Assert the resolver exists before considering a skip: its red state is the refusal path, failing by absence before implementation. If the pinned installation is absent, skip only this positive case with the named reason `pinned-installation-unavailable`, including the pin and expected install root, and record the skip in `report.md` and `validation.md`; do not skip dirty-entry or other negative cases. An existing installation that fails validation or version matching is a test failure, not a skip; the marker remains absent in every case.
- `test_missing_install_is_refused`: in the temporary repository copy, declare an exact version whose installation under the real passwd-home root is confirmed absent without creating or modifying it; assert exit 2, `trusted-interpreter: refused: install-missing` and no stdout.
- `test_shell_metacharacter_in_declaration_is_refused`: a copied declaration containing a shell metacharacter exits 2 with `trusted-interpreter: refused: declaration-malformed`, no interpreter stdout and no marker, without executing it.
- `test_duplicate_malformed_nonexact_or_metacharacter_declarations_are_refused`: through the clean prefix in the temporary repository copy, cover duplicate declarations with `trusted-interpreter: refused: declaration-duplicate`; malformed grammar, non-exact versions including `latest`, prefix or suffix lookalikes, and metacharacter-bearing values each assert `trusted-interpreter: refused: declaration-malformed`. Every case exits 2 with no interpreter stdout and no marker.
- `test_missing_or_nonexact_declaration_is_refused`: in the temporary repository copy, an absent declaration asserts `trusted-interpreter: refused: declaration-missing` and `latest` asserts `trusted-interpreter: refused: declaration-malformed`, both with exit 2, no interpreter stdout and no selection of an installed version.
- `test_program_entry_refuses_dirty_environment_or_symlinked_script`: invoke the program with exported functions, `BASH_ENV`/`ENV`, `LD_PRELOAD` and `LD_AUDIT` naming a marker-library path, planted PATH, a forged sanitization sentinel and a symlinked `$0`; dirty-entry cases assert `trusted-interpreter: refused: dirty-environment` and the symlinked-script case asserts `trusted-interpreter: refused: script-path`, each with exit 2, no interpreter stdout and no marker. The trusted-parent clean-prefix success assertion uses the read-only positive case above, with the real repository’s canonical script path and no marker. For direct dirty-entry refusal tests use a non-loadable marker-library path; a loadable library can execute before the script, so test its absence only with the trusted parent's pre-exec clean environment, never as a shell-entry guarantee.
- `test_forged_home_is_refused`: set HOME to a forged directory containing a marker-writing interpreter at the expected mise layout, retaining an otherwise allowed environment; assert exit 2 with `trusted-interpreter: refused: home-mismatch`, no interpreter stdout and no marker before that interpreter can execute. The clean-prefix success assertion with the real uid's passwd home is the read-only positive case above.

`install-symlink` and `install-not-regular` cannot be exercised in CI or by the worker (implemented, refuses by code, verified by reading). Their threat-table row remains `residual`, not `closed`. Do not manufacture symlinked, non-regular, forbidden-root or case-aliased installed candidates under the real passwd home, redirect its install root, or count an earlier refusal as runtime coverage of these checks.

Extend `tests/unit/test_ci_rerun.py::CiRerunTest::test_ci_rerun_pins_its_interpreter_against_a_checkout_and_the_environment`, currently at line 273, with the marker-writing **`python3`** in `.venv/bin` **prepended to PATH**, with mise unavailable. Assert dirty entry exits 2 with `ci-rerun: refused: dirty-environment` and no marker or rerun; then, in a CI-provisioned successful consumer fixture as specified below, use the trusted-parent clean prefix and assert the marker is absent and that the real pinned installation permits exactly one rerun with the pinned interpreter. Also cover safe refusal in a temporary repository copy declaring an exact version whose real passwd-home installation is confirmed absent, asserting the propagated `trusted-interpreter: refused: install-missing` code without modifying that installation.

Retain and adapt `test_ci_rerun_starts_the_pinned_interpreter_by_its_own_path` and `test_ci_rerun_never_runs_a_path_resolved_command_before_the_pin`; their assertions must exercise the new trusted-path contract rather than preserve acceptance of arbitrary PATH wrappers or the removed shims mechanism. Add `test_ci_rerun_executes_as_a_sanitized_program` for exported functions, `BASH_ENV`/`ENV`, `LD_PRELOAD` and `LD_AUDIT` naming a marker-library path, planted PATH, the forged-sentinel case, forged HOME and a worker-owned symlinked `$0`; assert `ci-rerun: refused: dirty-environment` for hostile environment inputs, `ci-rerun: refused: home-mismatch` for forged HOME and `ci-rerun: refused: script-path` for symlinked `$0`, each with exit 2, no marker and no rerun. Apply the same non-loadable-path limitation to direct dirty-loader refusal cases; with a loadable marker library, only the trusted-parent clean-prefix case asserts no marker. Clean-prefix execution in a CI-provisioned successful consumer fixture with the canonical script path and real passwd home must still use the pinned interpreter for both Python invocation sites and permit the expected rerun.

Add these tests to `tests/unit/test_ci_rerun.py::CiRerunTest`. Each destination test starts from an accepted baseline: a temporary copy of the repository tree whose own `scripts/orchestrator/ci-rerun.sh` is executed as the program through the trusted-parent clean prefix. The copy must be the program's confirmed repository root, with its registry, ledger and reservation paths accepted; make one positive assertion of exit 0 and the expected fixture-only behavior first. The CI runner provisions these temporary copies outside the forbidden worker/cache/tmp roots, using the real pinned installation read-only; the sandboxed worker records blocked local evidence when that baseline is unavailable. Executing the original script against paths in another temporary tree is not an accepted baseline.

For each independent negative invocation, restore the accepted baseline state and apply exactly one mutation: an otherwise in-root symlink at the destination or a parent (including a symlinked ledger and a symlinked reservation parent), a case-aliased in-root pathname (including the registry on a case-insensitive filesystem), or a parent redirected to a path outside the copy, including worker-writable cache and temporary destinations. Assert exactly `ci-rerun: refused: destination-symlink`, `ci-rerun: refused: destination-case-alias` or `ci-rerun: refused: destination-outside-root`, respectively, as well as exit 2, no registry parsing, no ledger append or reservation change, no rerun and an untouched target compared with its state immediately before the mutation. Keep symlink and case-alias subcases otherwise contained so an earlier containment refusal cannot satisfy them. Report an explicit skip for the case-alias subcase on a case-sensitive filesystem; do not claim that subcase ran.

- `test_ci_rerun_refuses_unsafe_flake_registry_destination`: exercise all destination-refusal subcases for `.github/flakes.yaml`.
- `test_ci_rerun_refuses_unsafe_ledger_destination`: exercise all destination-refusal subcases for `.orchestration/validation/ci-reruns.tsv`, including a redirected ledger parent.
- `test_ci_rerun_refuses_unsafe_reservation_destination`: exercise all destination-refusal subcases for `.orchestration/validation/ci-reruns.lock.d` and an existing per-run reservation, including a redirected reservation parent.
- `test_ci_rerun_refuses_git_environment_inputs`: start with `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE` and `GIT_CONFIG_GLOBAL` pointing at planted locations in the outer environment, run through the trusted-parent clean prefix and assert that no `GIT_*` name survives at program entry, the confirmed root is the trusted fixture repository and the planted locations remain unused and unchanged. In separate subcases deliberately introduce each of those four names, plus another `GIT_*` name, after the prefix; the program must refuse at entry with exit 2 and `ci-rerun: refused: dirty-environment` before Git, registry reads, ledger or reservation access or any rerun.
- `test_ci_rerun_refuses_repository_local_core_worktree`: set `core.worktree` in the fixture repository's local configuration to a planted worktree, invoke the consumer through the trusted-parent clean prefix with no `GIT_*` names and assert exit 2 at root confirmation with `ci-rerun: refused: repository-root`, before registry reads, ledger or reservation access or any rerun; the planted worktree remains unchanged.
- `test_ci_rerun_binds_github_repository_from_foreign_cwd`: use a CI-provisioned accepted consumer fixture and a fake `gh` that records every argument and serves a completed pull-request run whose failures match the fixture signatures. Execute the fixture's canonical `ci-rerun.sh` as a program through the trusted-parent clean prefix with its current directory set to a temporary copy of another repository whose remote identifies `foreign-owner/foreign-repo`. Assert exit 0 and exactly one fixture-only rerun; require recorded run-metadata, job-log, API, PR-head and rerun calls so an empty log or earlier refusal cannot pass. Assert `--repo mryfmo/dotfiles` on every recorded `gh run` and `gh pr` call and an explicit endpoint beginning `repos/mryfmo/dotfiles/` on every recorded `gh api` call; no call may carry a `{owner}/{repo}` placeholder or the foreign checkout's identity.

The positive resolver case reads the real repository and real installation read-only; it does not copy or rewrite the declaration, provision an installation, or create a repository outside the worker boundary. Every executable negative case, including forged HOME, malformed declaration, dirty environment, planted PATH and redirected destinations, uses temporary fixtures; declaration mutations use repository copies, and destination mutations require the accepted copied-repository baseline above. No negative case modifies the real passwd-home installation; symlinked and non-regular installation checks remain residual and are verified by reading. The passwd-home lookup always remains anchored to the real uid: do not substitute an account database, intercept that lookup, redirect the install root, or add a test seam that bypasses it.

The inspected unit-test workflow `.github/workflows/test.yaml`, job `test`, has the existing mise setup step `Setup mise for statusline smoke` using `jdx/mise-action`, followed by `Install statusline tools` and later `Run Python unit tests`. The setup currently has `install: false`, and the listed tool-install commands do not install Python. Before dispatch, the orchestrator must arrange through a separate authorized prerequisite that this existing mise setup provisions the repository’s exact pinned Python under the runner’s real passwd-home mise install root before the Python tests. This task does not authorize workflow edits or worker writes beneath that root. CI runs the positive resolver case against its real checkout outside forbidden roots and its actual mise installation; it must record a passing case, not a missing-installation skip, for acceptance.

Successful consumer fixture repositories outside worker/cache/tmp roots are created and exercised by the CI runner, using the same real pinned installation read-only; the sandboxed worker must not provision them or modify the real repository, installation or protected cache. Copy the resolver beside the consumer only in fixture repositories, supply fixture declarations there, and execute both scripts as programs through the trusted-parent clean prefix except for the explicit refusal cases. Obtain the successful consumer assertions’ red/green evidence in CI; record any locally unavailable fixture as blocked local evidence rather than claiming a pass or weakening the write boundary. Adapt fake-gh fixture data delivery to the clean environment; do not add production environment exemptions, executable-directory parameters or test-only resolver bypasses. Keep every existing behavioral assertion and keep all fixture calls off live GitHub.

## Measurement and caps

The requested `git diff --numstat 69dccca9 67e2cc98` was attempted in the read-only authoring checkout but failed because that head is absent from its local object store. The [GitHub comparison](https://github.com/mryfmo/dotfiles/compare/69dccca9...67e2cc98) reports `31` additions and `5` deletions for the source script, and `67` additions and `1` deletion for its tests; the available `22a280c4` versions produce the same local numstat. The orchestrator must paste the requested command’s successful output before dispatch rather than describe the failed attempt as a completed measurement.

Source budget: the retained a02 source delta is `31 + 5 = 36` changed lines, plus about `60` for the resolver, `60` for consumer integration and `30` for destination validation and Git-root confirmation, giving `36 + 60 + 60 + 30 = 186`, with `24` lines of allowance and a resulting cap of **210 changed lines outside `tests/` and `.orchestration/`**.

Test budget: the retained a02 test delta is `67 + 1 = 68` changed lines, plus about `130` for resolver tests including parser, forged-HOME, dirty-entry and reason-code cases, `110` for consumer regressions and clean-prefix fixture migration, and `90` for the three destination tests and two hostile-Git regressions, plus `20` for the foreign-cwd GitHub repository-binding regression, giving `68 + 130 + 110 + 90 + 20 = 418`, with `2` lines of allowance and a resulting cap of **420 changed lines under `tests/`**.

These replace the inherited 250/350 caps. Count additions plus deletions, including fixture lines and any baseline delta; do not exclude a new helper or split work to conceal the count.

## Check

Retain the predecessor’s checks: `make unit-test`, `make format`, ShellCheck and repository-style `shfmt -i 4 -sr -d` on the changed shell scripts, and the workflow-orchestration, workflow-security and ci-rerun unit modules. Add the trusted-interpreter module, the new startup and hostile-PATH cases, and the changed-file comparison lint. Do not run bats locally.

Paste the exact commands, exit statuses and full output in `.orchestration/dotfiles-T133-ci-efficiency-followup-a04/validation.md`. Existing baseline failures are reported as failures, with equivalent base/head evidence; do not relabel them green. Cached PyYAML checks use the Makefile’s cache-first lesson without weakening the production helper’s offline contract.

After pushing, paste `gh run list --branch tools/ci-efficiency-followup-a02 --json name,event,conclusion` and final-head required-check evidence, showing the seven required contexts and no pull-request private-bootstrap run.

With `git diff --numstat origin/main...HEAD`, at most **210 changed lines outside `tests/` and `.orchestration/`** are permitted.

With the same diff, at most **420 changed lines under `tests/`** are permitted.

The **orchestrator**, before dispatch and at acceptance, runs the format-2 task-consistency checker on `.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md`, including C1–C10, C7b, C11 and C18; reads and runs `tests/unit/test_task_consistency_c11_c15.py`; and checks that each closed row has exactly one existing or explicitly added `tests/<path>::<Class>::<test>` selector. Use the required checker revision, not the currently incomplete one.

The **orchestrator** performs the C-80 pre-dispatch security review of this exact text after the prerequisite corrections and before sending it; a surviving P0/P1 holds dispatch.

The **orchestrator** compares the branch’s a04 task copy byte-for-byte with the dispatched a04 task text, verifies its SHA-256 against the TASK line, and checks the first push’s deletion of the a02 task copy. A reported hash alone is not the comparison.

## Completion

One existing PR, #424, on `tools/ci-efficiency-followup-a02`, continuing from `67e2cc98`; the predecessor’s fresh-branch requirement is superseded. Keep its implementation, tests, commits and historical evidence. In the first a04 push delete `.orchestration/dotfiles-T133-ci-efficiency-followup-a02/task.md` and add `.orchestration/dotfiles-T133-ci-efficiency-followup-a04/task.md` byte-identically to the dispatched a04 text. That single predecessor-file deletion is the reset transition authorized by C3; do not rewrite or move the predecessor’s other evidence.

Write current `report.md`, `validation.md`, `sandbox.md`, `learning.md`, `autoskill.md` and worker review evidence under `.orchestration/dotfiles-T133-ci-efficiency-followup-a04/`. Record the predecessor head, exact final head and base, branch, PR, changed files, row-to-test mapping, red/green commits, cap totals, evidence paths and `task_copy=<sha256 of .orchestration/dotfiles-T133-ci-efficiency-followup-a04/task.md>`. Preserve historical claims as historical; they do not approve the new head.

The inherited Completion rules apply with these explicit bindings: advisory P2 and P3 belong to `dotfiles-T133-ci-efficiency-followup-a03`, with rows recorded by the orchestrator before disposition. Do not reopen that owner’s advisory work in this task unless a narrow revise explicitly authorizes it.

Every fix round counts toward INV-6, including worker-side fixes before the first RESULT; C-61 permits at most two in this task, and amendments and questions retain their own counters. A rebase repair qualifies only under D-024-24 and cannot hide a security fix. Another repeated-class finding or exhausted counter stops work for the orchestrator’s recorded re-plan; do not continue under a new label.

A P0/P1 surviving the permitted worker-side fix round is sent as `open:<id>` in the RESULT, including `open:review-<id>` for a review-body finding, with the applicable round count. It stops integration for the operator’s decision; never convert it into an advisory disposition or perform another unauthorized fix round.

Wait for final-head CI and the bounded automatic Bot-review window. Record `bot: none` if the window expires. **Do not post `@codex review`**, at the ten-minute mark or after a fix. The orchestrator replies to and resolves GitHub review threads.

Every `gh` command and every `git` write is an individual command **inside the sandbox**, including pushes and authenticated fetches. No compound write commands, outside-sandbox retries, excluded-command workaround, permission escalation or alternate tool to bypass a denial. Anything that cannot complete there produces `AGMSG-PONG v1 task_id=dotfiles-T133-ci-efficiency-followup-a04 status=blocked` naming the exact command, failure and crossed boundary; preserve the evidence and wait.

The orchestrator performs final-head review and the security-profile review, then follows Orchestrator Playbook step 10 for CI, feedback sweep, task-level audit, finding dispositions, acceptance, gate and head-bound merge. The worker does not merge or remove workers.

Implementation, runtime tests and CI are not claimed checked by this task draft; dispatch remains held on the stated prerequisites. Same-UID replacement and shared-credential risks remain residual.

## Checks (pasted by the orchestrator before each send)

```
(pasted at dispatch)
```
 succeeded in 288ms:
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

**Planning read segmentation**
codex
通常の PATH は mise shims が先頭ですが、タスク本文は clean parent と固定パスを指定しています。この点と明示された same-UID の残余リスクを踏まえ、先行レビューの指摘が解消されているかを照合します。読み取り専用のため、worklog・レビュー証跡は書き込みません。
exec
/bin/zsh -lc "cat .orchestration/acceptance/dotfiles-T133-python-pin-a02.md; sed -n '190,270p' .orchestration/acceptance/dotfiles-T133-python-pin-a01.md; rg -n '"'^## .*5.14|''^### .*5.14|''^#### |D-024-29|D-024-30'"' .orchestration/plans/024-design-quality.md" in ~/Workspace/dotfiles
 succeeded in 8ms:
---
{
  "audit_findings": [],
  "dispatch": [],
  "format": 1,
  "head": null,
  "ledger": [
    {
      "class": "hash-binding",
      "id": "text-security:7771c92:1"
    },
    {
      "class": "tool-environment",
      "id": "text-security:7771c92:2"
    },
    {
      "class": "threat-row-unit",
      "id": "text-security:7771c92:3"
    },
    {
      "class": "sources",
      "id": "text-security:7771c92:4"
    },
    {
      "class": "spec-without-input-grammar",
      "id": "text-security:7771c92:5"
    },
    {
      "class": "threat-row-missing",
      "id": "text-security:7771c92:6"
    },
    {
      "class": "tool-environment",
      "id": "text-security:e4316e1:1"
    },
    {
      "class": "tool-environment",
      "id": "text-security:e4316e1:2"
    },
    {
      "class": "tool-environment",
      "id": "text-security:9f757da:1"
    },
    {
      "class": "fragile-premise",
      "id": "text-security:e74aec4:1"
    },
    {
      "class": "fragile-premise",
      "id": "text-security:e74aec4:2"
    },
    {
      "class": "correct",
      "id": "text-security:c8021a7:0"
    },
    {
      "class": "fragile-premise",
      "id": "text-security:9c5500f:1"
    },
    {
      "class": "text-defect",
      "id": "text-security:ed75bc6:1"
    },
    {
      "class": "text-defect",
      "id": "text-security:ed75bc6:2"
    },
    {
      "class": "tool-environment",
      "id": "text-security:0ec4bb9:1"
    },
    {
      "class": "text-defect",
      "id": "text-security:b657a89:1"
    },
    {
      "class": "text-defect",
      "id": "ci:32f400c:1"
    },
    {
      "class": "replan-skipped",
      "id": "audit:e9819d4:1"
    },
    {
      "class": "ledger-completeness",
      "id": "audit:e9819d4:2"
    },
    {
      "class": "text-defect",
      "id": "audit:e9819d4:3"
    }
  ],
  "pr": null,
  "replans": {
    "fragile-premise": {
      "design": "the `## Commands` block carries, for each command, the execution timestamp and output (C-87 applied to the text itself), and the cap evidence command refuses a compare list of 300 files or one whose length differs from the PR's `changedFiles`",
      "implementation": "the amendment with the executed compare probe",
      "specification": "every command the text prescribes has been executed by the orchestrator at authoring time on this host, under the clean prefix, and its pasted output stands beside it; a command that cannot be executed before dispatch is not written",
      "verification": "C-80 round 1 after this line."
    },
    "text-defect": {
      "design": "one pre-send command runs them all on the final bytes and prints the sha256 the dispatch line carries (`.agents/worklog/orchestrator-glue/pre-send.sh`; tracked home `dispatch.sh --next` in the loop-limits lineage)",
      "implementation": "the line-199 note rewritten as a description, pre-send output `OK / secret-pattern: 0 match(es) / bash -n block 1: rc=0 / lines: 199`, sha256 8e544c8a… -> 30185a5a…",
      "specification": "the task text passes, as one file, every machine check CI and the regime apply to it before any send: the consistency checker, the validator's SECRET_PATTERN over every line, no literal home path, its own line cap and `bash -n` over every fenced bash block",
      "verification": "CI `validate` on the next head of PR #437."
    },
    "tool-environment": {
      "design": "a single `## Commands` block defines the clean prefix, the anchored home, the exact interpreter path, the direct test-file execution (`python -I tests/unit/test_mise_config.py`) and the bound gh realpath once, and every premise, check and evidence line references that block instead of restating a command",
      "implementation": "amendment 3 of the text by the review profile",
      "specification": "every command the text prescribes runs in the trusted-parent form with one interpreter, no PATH resolution and no implicit import (no discovery, no shim, no `~`)",
      "verification": "C-80 round 4 with the budget reset by this line, then the worker's pasted outputs of exactly those commands."
    }
  },
  "searches": [],
  "task": "dotfiles-T133-python-pin-a02"
}
---

# Acceptance record: dotfiles-T133-python-pin-a02

- 2026-10-20T04:40Z: reset of dotfiles-T133-python-pin-a01 after INV-6 S2 (regime-counters at 04:31Z: tasks=3 amendments=2 questions=1 results=5 revises=4; audit e9819d4 P1), written whole by the review profile (`python-pin-a02-prompt.md`), carrying the implementation at 09c81cc3 on PR #437 unchanged; the a01 findings history is in the a01 record; the lineage rows and re-plan lines are carried below before any chain (M-20261019-06).

## Lineage rows carried from dotfiles-T133-python-pin-a01

text-security:7771c92:1	hash-binding
text-security:7771c92:2	tool-environment
text-security:7771c92:3	threat-row-unit
text-security:7771c92:4	sources
text-security:7771c92:5	spec-without-input-grammar
text-security:7771c92:6	threat-row-missing
text-security:e4316e1:1	tool-environment
text-security:e4316e1:2	tool-environment
text-security:9f757da:1	tool-environment
text-security:e74aec4:1	fragile-premise
text-security:e74aec4:2	fragile-premise
text-security:c8021a7:0	correct
text-security:9c5500f:1	fragile-premise
text-security:ed75bc6:1	text-defect
text-security:ed75bc6:2	text-defect
text-security:0ec4bb9:1	tool-environment
text-security:b657a89:1	text-defect
ci:32f400c:1	text-defect
audit:e9819d4:1	replan-skipped
audit:e9819d4:2	ledger-completeness
audit:e9819d4:3	text-defect
re-plan: tool-environment (rows text-security:7771c92:2, text-security:e4316e1:1, text-security:e4316e1:2, text-security:9f757da:1) — specification: every command the text prescribes runs in the trusted-parent form with one interpreter, no PATH resolution and no implicit import (no discovery, no shim, no `~`); design: a single `## Commands` block defines the clean prefix, the anchored home, the exact interpreter path, the direct test-file execution (`python -I tests/unit/test_mise_config.py`) and the bound gh realpath once, and every premise, check and evidence line references that block instead of restating a command; implementation: amendment 3 of the text by the review profile; verification: C-80 round 4 with the budget reset by this line, then the worker's pasted outputs of exactly those commands.
re-plan: fragile-premise (rows text-security:7771c92:1-6, text-security:e74aec4:1-2, text-security:9c5500f:1) — specification: every command the text prescribes has been executed by the orchestrator at authoring time on this host, under the clean prefix, and its pasted output stands beside it; a command that cannot be executed before dispatch is not written; design: the `## Commands` block carries, for each command, the execution timestamp and output (C-87 applied to the text itself), and the cap evidence command refuses a compare list of 300 files or one whose length differs from the PR's `changedFiles`; implementation: the amendment with the executed compare probe; verification: C-80 round 1 after this line.
re-plan: text-defect (rows text-security:ed75bc6:1-2, text-security:b657a89:1, ci:32f400c:1) — specification: the task text passes, as one file, every machine check CI and the regime apply to it before any send: the consistency checker, the validator's SECRET_PATTERN over every line, no literal home path, its own line cap and `bash -n` over every fenced bash block; design: one pre-send command runs them all on the final bytes and prints the sha256 the dispatch line carries (`.agents/worklog/orchestrator-glue/pre-send.sh`; tracked home `dispatch.sh --next` in the loop-limits lineage); implementation: the line-199 note rewritten as a description, pre-send output `OK / secret-pattern: 0 match(es) / bash -n block 1: rc=0 / lines: 199`, sha256 8e544c8a… -> 30185a5a…; verification: CI `validate` on the next head of PR #437.
- 2026-10-20T04:41Z: the a02 reset text installed (`redesign/python-pin-a02.md`, 175 lines): premises carry only the probes executed read-only at 04:31:20Z (`id -P` home, python 3.15.0 realpath, gh 2.102.0 realpath, policy grep), no failed-probe leftover, the Commands block unchanged; the checker's C3 required a predecessor-copy row for `.orchestration/dotfiles-T133-python-pin-a01/task.md`, added by the orchestrator (one flow-style row); pre-send.sh: checker OK, SECRET_PATTERN 0, bash -n OK, 176 lines (self cap 190); sha256 68fd5f2e6b36d89789d1723caba932666c7719c09aeae154a3f049d31542d862. C-80 round 1 running.

95:### 5.14 残余（凍結後の計測事実、D-024-29）
103:## 5.14 信頼ホスト実行契約（trusted-host execution contract、D-024-18）

exec
/bin/zsh -lc "sed -n '80,225p' .orchestration/plans/024-design-quality.md; tail -n 35 .orchestration/acceptance/dotfiles-T133-python-pin-a01.md; for f in .orchestration/validation/dotfiles-T133-python-pin-a01-text-security-*.md.last.md; do printf '%s\\n' \""'$f"; cat "$f"; done' in ~/Workspace/dotfiles
 succeeded in 109ms:
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
- 2026-10-20T01:54:26Z: re-planned text (`redesign/python-pin-r4.md`) installed: 167 lines + the standard rows the review profile dropped (orchestrator effects, task metadata, in-process effects, workflow inputs) = checker OK; one `## Commands` block (anchored home, clean prefix, exact interpreter, direct test-file execution, bound gh realpath, bound cap evidence) referenced everywhere; no `~`. C-80 round 1 after the re-plan running.
- 2026-10-20T02:00Z: C-80 round 1 after the re-plan (`…-text-security-e74aec4.md`) `Verdict: incorrect`, two P2, both facts the orchestrator's prompt prescribed without probing (C-87 by the orchestrator): mise installs gh under `installs/github-cli-cli/` (not `github-cli/`), so Commands (e) always refuses; `git -c include.path=` is invalid (exit 128 `relative config includes must come from files`). Amendment 1 after the re-plan with the probed values (2026-10-20T02:01:18Z): the gh realpath from the host, and the cap evidence read from the GitHub API compare endpoint (design 5.14 item 8) instead of local git; budget 1 of 3.
text-security:e74aec4:1	fragile-premise
text-security:e74aec4:2	fragile-premise
- 2026-10-20T02:32:13Z: C-80 round 2 after the re-plan (`…-text-security-c8021a7.md`) `Verdict: correct` (commands remove inherited inputs, avoid shims, bind GitHub evidence to the repository and full shas; residuals explicit). Dispatch next: the orchestrator runs the text's Commands probes fresh (C-100) and pastes them into the Checks block; a012 takes it (loop-limits stays held on its prerequisites).
text-security:c8021a7:0	correct
- 2026-10-20T02:33:41Z: the dispatch probes run fresh (C-100): inside the Claude sandbox `dscl . -read … NFSHomeDirectory` fails (`Operation failed with error: eServerError`; the helper task measured exit 70 in the Codex sandbox) while `/usr/bin/id -P | cut -d: -f9` and Python's `pwd.getpwuid` return the passwd home; outside the sandbox dscl works. Measured amendment: Commands (a) uses `id -P` (same directory service through libc); recorded in design 5.14's residual list (D-024-29: no item change). Probe outputs pasted into the Checks block: interpreter realpath …/python/3.15.0/bin/python3 (3.15.0), gh realpath …/github-cli-cli/2.102.0/bin/gh (2.102.0), main 118daafa, declaration python = "latest". Text sha256 c8021a71… -> 9c5500f0…; checker OK; C-80 round 3 after the re-plan running (the last of the budget).
- 2026-10-20T02:37Z: C-80 round 3 after the re-plan (`…-text-security-9c5500f.md`) `Verdict: incorrect`, one P2: GitHub's compare endpoint caps `.files` at 300 whatever `--paginate` says, and the task directory is unbounded, so a truncated list could hide changes from the cap evidence; reject truncated results or establish completeness independently. The budget after the first re-plan is spent. Re-examination: four rounds on this text found nine findings of one family — commands and facts written from memory instead of executed (dscl, the gh install path, `-c include.path=`, the compare cap): fragile-premise. The re-plan: no command enters the text unexecuted.
text-security:9c5500f:1	fragile-premise
re-plan: fragile-premise (rows text-security:7771c92:1-6, text-security:e74aec4:1-2, text-security:9c5500f:1) — specification: every command the text prescribes has been executed by the orchestrator at authoring time on this host, under the clean prefix, and its pasted output stands beside it; a command that cannot be executed before dispatch is not written; design: the `## Commands` block carries, for each command, the execution timestamp and output (C-87 applied to the text itself), and the cap evidence command refuses a compare list of 300 files or one whose length differs from the PR's `changedFiles`; implementation: the amendment with the executed compare probe; verification: C-80 round 1 after this line.
- 2026-10-20T02:38:42Z: amendment after re-plan 2: the compare completeness check (fewer than 300 files and equal to the PR's changedFiles) added to Commands (f) with its executed output (`ba318e53...118daafa`: files 7, total_commits 1, truncated false; PR #434 changedFiles 7); text sha256 9c5500f0… -> ed75bc62…, 188 lines, checker OK; C-80 round 1 after re-plan 2 running.
- 2026-10-20T02:41Z: C-80 round 1 after re-plan 2 (`…-text-security-ed75bc6.md`) `Verdict: incorrect`, two P2 caused by the orchestrator's direct edit: the completeness requirement was prose inside the executable Bash block (`bash -n` exit 2), and dispatch required the PR's changedFiles that exists only after dispatch (circular). Fixed at 2026-10-20T02:42:13Z: an executable (f') line inside the block (refuse 300 files or a count that differs from changedFiles), the prose with the executed output below the block, (f)/(f') run at RESULT only; `bash -n` of the block verified; budget after re-plan 2: 1 of 3 used.
text-security:ed75bc6:1	text-defect
text-security:ed75bc6:2	text-defect
- 2026-10-20T02:45Z: C-80 round 2 after re-plan 2 (`…-text-security-0ec4bb9.md`) `Verdict: incorrect`, one P2: gh's persistent configuration (hosts.yml api_host) can redirect requests despite --hostname, and the unqualified --repo can select another configured host. Fixed at 2026-10-20T02:47:12Z: Commands (e') isolates gh's configuration (a fresh GH_CONFIG_DIR and the keyring token read once by the bound gh; every gh call carries both; --repo github.com/mryfmo/dotfiles); executed on this host inside and outside the sandbox: token read (40 chars), main sha 118daafa, PR #434 changedFiles 7; `bash -n` of the block OK; C-80 round 3 after re-plan 2 running (the last of the budget).
text-security:0ec4bb9:1	tool-environment
- 2026-10-20T02:47:53Z: the configuration-isolation replace had also rewritten the trusted-parent launch line (undefined $GHC/$TOKEN at that point); the launch line restored without a token (the token is read inside by (e')); a review started on the intermediate bytes was stopped before it wrote anything (not consumed); text sha256 ad56c1a6… -> b657a897…; `bash -n` OK; checker OK; C-80 round 3 after re-plan 2 running on the corrected text.
- 2026-10-20T02:52:55Z: C-80 round 3 after re-plan 2 (`…-text-security-b657a89.md`) `Verdict: incorrect` on one P2: the text (198 lines) exceeded its own 185-line sentence; "No additional security findings". Disposition by the orchestrator: the self-cap sentence set to 210 (proposal 1 allows 250), 199 lines; the review budget is spent and the finding is mechanical, so no further review; the task-level audit of the PR checks the contract. Dispatched to a013 (worker-h, the sixth seat, added by the orchestrator at 02:51Z); text sha256 59f91f5580892ddd58f10b538eb611e790200edf6d41ead1e63bd753e5d68fbd.
text-security:b657a89:1	text-defect
- 2026-10-20T02:57:00Z/02:58:25Z: a013 PONG `blocked` then RESULT `status=blocked` at Worker Playbook step 2: `git switch -c task/dotfiles-T133-python-pin-a01 --no-track origin/main` exited 0 with stderr `Unable to create shared .git/packed-refs.lock: Operation not permitted` (the Codex sandbox cannot write the main repository's shared .git; the loose branch ref was written: the branch exists). The same non-fatal warning appears in a012's and a010's records (the loop-limits a01 text and the P1-15 a02 record). Answer 2026-10-20T03:08:21Z: continue; record the denied write in sandbox.md as non-blocking; no repair, no bypass. Mechanism note: the Codex seat's writable roots exclude .git/worktrees/<seat>/ and the shared packed-refs; a known class for the write-boundary owner.
- 2026-10-20T03:08:59Z: a013 PONG `alive`: resumes step 3 on the created branch; records the denied packed-refs write beside the successful operation; no repair, no bypass. ACCEPTANCE `status=revise round=0` sent 2026-10-20T03:11:32Z to close the superseded blocked RESULT for the stop gate (not a fix round).
- 2026-10-20T03:13:02Z/03:15:23Z: a013 PONG then RESULT `status=blocked`: implementation, red/green, independent review and gate passed; local head 4045295b; `git push origin task/dotfiles-T133-python-pin-a01` exit 128 (`git@github.com: Permission denied (publickey)`): the global git config rewrites pushes to SSH and the host has no key (the known host fact; the other seats push with the SKILL's HTTPS form). ACCEPTANCE `status=revise round=0` 2026-10-20T03:21:25Z with the documented push form (GIT_CONFIG_GLOBAL=/dev/null, the gh credential helper through the bound gh with GH_CONFIG_DIR/GH_TOKEN, the HTTPS URL); not a fix round. Mechanism note: the python-pin text's Commands block defines no push form; the Worker Playbook's form is the contract (C-96: nothing new, the SKILL's text).
- 2026-10-20T03:23:40Z: a013 PONG `alive`: the HTTPS push form succeeded inside the sandbox; PR #437 opened at head 4045295b (dispatch base 118daafa; main now 60a6fb2b); CI and the Bot window running; no worker update-branch or merge.
- 2026-10-20T03:27:36Z: a013 PONG `blocked`: CI validate failed on #437 (run 39364020428, job 118436537807); the bound gh could not read the log (`creating cache entry: open $HOME/.cache/gh/run-log-…zip: operation not permitted`: the gh run-log cache lives under the home cache dir outside the Codex writable roots: C-94's remedy is XDG_CACHE_HOME under the worktree); Commands (f)/(f') pass (4 files, code 3/6, tests 19/40); the orchestrator reads the log.
- 2026-10-20T03:31:08Z: the #437 validate job failed: `possible committed secret in .orchestration/dotfiles-T133-python-pin-a01/task.md` (SECRET_PATTERN matches `<redacted:secret-pattern>` at Commands lines 132/134/136, found by running the validator's pattern over the text); amendment: variable GH_AUTH and `GH_TOKEN=$GH_AUTH` (clean against the pattern); sha256 59f91f558089 -> 8e544c8a77ca; re-dispatched for the copy update; a013 told the C-94 remedy for gh run logs (XDG_CACHE_HOME under the worktree). Mechanism note: the pre-dispatch checker should run the validator's secret scan on the text (owner: the P1-12 a05-checker lineage, C16 sibling).
- 2026-10-20T03:37:02Z: CI `validate` refused head 32f400c3 the same way (run 39364986999, job 118439659322: `possible committed secret in .orchestration/dotfiles-T133-python-pin-a01/task.md`); the validator's SECRET_PATTERN run over the text finds one match, line 199: amendment 1's own note quoted the refused assignment verbatim (M-20261020-01). a013 PONG 2685 (03:38:42Z) found the same line independently and asked for a new author source.
ci:32f400c:1	text-defect
re-plan: text-defect (rows text-security:ed75bc6:1-2, text-security:b657a89:1, ci:32f400c:1) — specification: the task text passes, as one file, every machine check CI and the regime apply to it before any send: the consistency checker, the validator's SECRET_PATTERN over every line, no literal home path, its own line cap and `bash -n` over every fenced bash block; design: one pre-send command runs them all on the final bytes and prints the sha256 the dispatch line carries (`.agents/worklog/orchestrator-glue/pre-send.sh`; tracked home `dispatch.sh --next` in the loop-limits lineage); implementation: the line-199 note rewritten as a description, pre-send output `OK / secret-pattern: 0 match(es) / bash -n block 1: rc=0 / lines: 199`, sha256 8e544c8a… -> 30185a5a…; verification: CI `validate` on the next head of PR #437.
- 2026-10-20T03:45Z: amendment 2 dispatched to a013 (`python-pin-amend2.txt`, task_sha256 30185a5aec22f7c320745b321f7cf49aba6f45de5b77d434c60918f7f3a68663; pre-send results pasted in the note, C-100).
- 2026-10-20T04:03:43Z: a013 RESULT `ready_for_review` for PR #437 head 09c81cc3 (base 60a6fb2b, task_sha256 30185a5a…); CI all green at 04:01Z (validate 2m14s, regime 14s, GitGuardian pass); the chain (`chain-integrate.sh … 437 … dotfiles-T133-python-pin-followup-a01`) and the security-profile review of 09c81cc3 started 04:08Z.
- 2026-10-20T04:24:57Z: the chain on the update-branch head e9819d45 (base check moved the PR: `gh pr update-branch`; CI green; local review 0 findings; sweep 9 items 0 gaps): task-level audit `…-audit-e9819d4.md` `Verdict: incorrect`: [P1] orchestration: INV-6 S2 exceeded on this lineage with no reset (measured 2026-10-20T04:39Z with scripts/regime-counters.sh: `tasks=3 amendments=2 questions=1 results=5 withdrawn=0 revises=4 first_result_head=none`; `S2: revises 4 >= 2`, `S2: amendments 2 >= 2`; the round=0 closures of blocked RESULTs count as revises); [P2] records: the JSON ledger, replans and searches were empty while the prose held 18 rows and three re-plan lines; [P2] specification: the dispatched text's Check (line 161-162) forbids dispatch until the failed Commands (a) probe is replaced while `premises` (line 76-81) still carries that failed `dscl` probe. Dispositions: P1 -> the lineage resets to `dotfiles-T133-python-pin-a02` written by the review profile (`python-pin-a02-prompt.md`), carrying the implementation at 09c81cc3 unchanged on PR #437 (a013 holds, PING `python-pin-hold.txt`); P2 records -> fixed in this record by `record-json-sync.py` (ledger 18 rows, replans 3) before any gate; P2 text -> fixed in the a02 text (premises carry only the probes executed read-only at 04:31:20Z: `id -P` home, python 3.15.0 realpath, gh 2.102.0 realpath, policy grep). No finding on the implementation.
audit:e9819d4:1	replan-skipped
audit:e9819d4:2	ledger-completeness
audit:e9819d4:3	text-defect

.orchestration/validation/dotfiles-T133-python-pin-a01-text-security-0ec4bb9.md.last.md
[P2] High confidence .orchestration/tasks/dotfiles-T133-python-pin-a01.md:129 — The clean environment still loads gh’s persistent configuration: `hosts.github.com.api_host` can redirect requests and credentials despite `--hostname github.com`, while line 133’s unqualified `--repo` can select another configured host; row 62’s authenticated-evidence mitigation therefore needs configuration isolation or validation, not just executable and argument binding. [GitHub CLI implementation](https://github.com/cli/cli/blob/v2.102.0/pkg/cmd/api/api.go), [credential handling](https://github.com/cli/cli/blob/v2.102.0/api/http_client.go).

All required threat-row units are present. The closed tests cover declaration syntax and policy consistency. Codex-only execution excludes the Linux unsandboxed-gh exception; executable provenance, symlink/case-alias protection and unrestricted same-user replacement remain explicitly residual. Independent review confirmed the finding.

📝 まとめ: Completed the read-only task-text and cited-record review; one finding awaits orchestrator disposition. No files changed.
Not checked: implementation, CI, deployment or fresh host prerequisites; persistent gh configuration can invalidate evidence authenticity.
Verdict: incorrect.orchestration/validation/dotfiles-T133-python-pin-a01-text-security-7771c92.md.last.md
- [P2] High confidence .orchestration/tasks/dotfiles-T133-python-pin-a01.md:90 — The prerequisite checks `latest/bin/python3`, but validation executes `3.15.0/bin/python3`; listing the directory does not establish that these resolve to the same executable, so the version decision is not bound to execution.
- [P2] High confidence .orchestration/tasks/dotfiles-T133-python-pin-a01.md:103 — Bare `uv` resolves through this host’s mise shim before its flags apply, while `$HOME` and Python startup inputs remain inherited; the future resolver does not constrain this validation command, leaving the environment row’s mitigation incomplete. [Mise resolution](https://mise.jdx.dev/dev-tools/shims.html), [Python environment](https://docs.python.org/3/using/cmdline.html).
- [P2] High confidence .orchestration/tasks/dotfiles-T133-python-pin-a01.md:40 — The in-process residual omits actual execution: unittest imports repository test modules, and the required supply-chain test launches PATH-resolved `chezmoi` at `tests/unit/test_supply_chain_policy.py:394`; “standard library” does not constrain those executable inputs.
- [P2] High confidence .orchestration/tasks/dotfiles-T133-python-pin-a01.md:106 — Cap evidence uses inherited `GIT_*` inputs and mutable local refs without binding the repository or base/head; redirected Git storage can produce measurements for a different changeset while the declaration test reads this checkout. [Git environment controls](https://git-scm.com/docs/git#_environment_variables).
- [P2] High confidence .orchestration/tasks/dotfiles-T133-python-pin-a01.md:91 — The prescribed regex accepts a trailing newline and Unicode digits, so the named test cannot close the exact-version grammar row; both counterexamples were reproduced read-only—require an ASCII full-string match. [Python regex semantics](https://docs.python.org/3/library/re.html).
- [P2] High confidence .orchestration/tasks/dotfiles-T133-python-pin-a01.md:82 — D-024-30 requires individual threat rows for design items 0–10, but none are supplied; generic rows leave the referenced cache/interpreter contract and symlink/case-alias, authenticated-evidence and execution-binding controls without explicit dispositions.

All four allowed-file entries have rows. The Codex-only worker and explicit sandbox restriction exclude the Claude/Linux `gh` exception; unrestricted same-UID replacement is correctly acknowledged as residual.

📝 まとめ: Completed the read-only task-text and related-record review; six findings are submitted for orchestrator disposition.
Not checked: implementation, CI or deployed protections; no files were changed, and execution/evidence binding remains incomplete.
Verdict: incorrect.orchestration/validation/dotfiles-T133-python-pin-a01-text-security-9c5500f.md.last.md
[P2] High confidence .orchestration/tasks/dotfiles-T133-python-pin-a01.md:131 — GitHub’s compare endpoint limits `.files` to 300 despite `--paginate`; the allowed artifact directory is unbounded, so omitted configuration/test changes can escape the cap calculation—reject potentially truncated results or establish completeness independently. [GitHub documentation](https://docs.github.com/en/rest/commits/commits#compare-two-commits).

All required threat-row units are present. The closed tests match their stated scope; Codex-only sandbox execution excludes the Linux unsandboxed-`gh` exception. Symlink/case-alias enforcement, executable provenance and unrestricted same-UID replacement remain explicitly residual.

📝 まとめ: Completed the read-only design and cited-record review; one finding requires orchestrator disposition.
Not checked: implementation, CI or deployment; no files changed, and cap-evidence completeness remains unverified.
Verdict: incorrect.orchestration/validation/dotfiles-T133-python-pin-a01-text-security-9f757da.md.last.md
[P2] High confidence .orchestration/tasks/dotfiles-T133-python-pin-a01.md:136 — `unittest discover -p test_mise_config.py` also imports subpackage initializers regardless of the pattern: an untracked `tests/unit/extra_package/__init__.py` can execute while contributing zero tests, preserving `Ran 1 test` and contradicting the in-process mitigation at line 40; execute the intended file directly under `-I` instead. Confirmed with the installed interpreter’s loader using an in-memory probe. [Python documentation](https://docs.python.org/3.15/library/unittest.html#unittest.TestLoader.discover).

All required threat-row units are present. Earlier environment and bare-`gh` findings are addressed; same-UID replacement and deferred symlink/case-alias protections remain explicitly residual.

📝 まとめ: Completed the read-only design and cited-record review; one finding remains for orchestrator disposition.
Not checked: implementation, CI or deployment; no files changed. The discovery command still permits unintended imports.
Verdict: incorrect.orchestration/validation/dotfiles-T133-python-pin-a01-text-security-b657a89.md.last.md
[P2] High confidence .orchestration/tasks/dotfiles-T133-python-pin-a01.md:175 — The task contains 198 lines but requires the whole text to remain within 185; line 181’s byte-identical copy requirement prevents the worker from satisfying both constraints—shorten the dispatched text before implementation.

No additional security findings. All required threat-row units are present, and the closed tests cover their stated declaration and policy scope. The clean environment and explicit executable bindings avoid shim and inherited `GIT_*` selection. Fresh `GH_CONFIG_DIR` plus explicit credentials addresses the previous persistent-configuration issue. [GitHub CLI environment documentation](https://cli.github.com/manual/gh_help_environment)

Codex-only execution and the no-escalation rule exclude the Linux unsandboxed-gh exception. Symlink/case-alias enforcement, executable provenance and unrestricted same-user replacement remain explicitly residual, rather than claimed closed.

📝 まとめ: Completed the read-only task, threat-table and cited-record review; one task-contract finding awaits orchestrator disposition. No files changed.
Not checked: implementation, CI, deployment or fresh host prerequisites; the disclosed host execution risks remain.
Verdict: incorrect.orchestration/validation/dotfiles-T133-python-pin-a01-text-security-c8021a7.md.last.md
No findings. All required threat rows are present; the closed rows cover declaration syntax and policy consistency. Commands remove inherited environment inputs, avoid shim resolution, and bind GitHub evidence to the explicit repository and full SHAs. Codex-only sandbox execution excludes the Linux unsandboxed-`gh` exception.

Symlink/case-alias enforcement, executable provenance, and unrestricted same-UID replacement remain explicitly residual. Independent review reached the same conclusion. Dispatch remains blocked pending successful fresh prerequisites.

📝 まとめ: Completed the read-only task-text, threat-table, and cited-record review; no files changed.
Not checked: implementation, CI, deployment, or fresh host prerequisites; disclosed execution-provenance risks remain.
Verdict: correct.orchestration/validation/dotfiles-T133-python-pin-a01-text-security-e4316e1.md.last.md
- [P2] High confidence .orchestration/tasks/dotfiles-T133-python-pin-a01.md:114 — Repeating the premises executes `~/.local/…/python3` without the clean environment used at line 127; `~` follows inherited HOME (confirmed read-only), so the prerequisite can inspect a different interpreter from the passwd-home-bound validation command. Rewrite the probes with the same anchored path and clean prefix.

- [P2] High confidence .orchestration/tasks/dotfiles-T133-python-pin-a01.md:129 — The authoritative base lookup still invokes bare `gh`, which resolves to this host’s mise shim; fixing the API endpoint and hostname does not bind the executable or its environment, leaving the “authenticated GitHub evidence” mitigation incomplete. Bind this invocation to a verified executable under the clean parent environment. [Mise shim behavior](https://mise.jdx.dev/dev-tools/shims.html).

All four allowed-file entries and required non-path controls have rows. The narrowed closed rows cover declaration syntax and policy consistency. The Codex-only, no-escalation requirement excludes the Claude/Linux unsandboxed `gh` exception; same-UID replacement and deferred symlink/case-alias protections remain explicitly residual.

📝 まとめ: Completed the read-only task-text, threat-table and related acceptance/review-record review; two findings are submitted for orchestrator disposition.

Not checked: implementation, CI or deployment; no files changed. The prescribed prerequisite and evidence commands retain execution-binding gaps.
Verdict: incorrect.orchestration/validation/dotfiles-T133-python-pin-a01-text-security-e74aec4.md.last.md
- [P2] High confidence .orchestration/tasks/dotfiles-T133-python-pin-a01.md:116 — The gh candidate list excludes this host’s installed executable: mise uses `installs/github-cli-cli/`, while the prescribed `github-cli/` and both fallback paths are absent; Commands (e) necessarily refuses, and the prohibition on substitutions prevents completing the authenticated-base prerequisite.
- [P2] High confidence .orchestration/tasks/dotfiles-T133-python-pin-a01.md:122 — `-c include.path=` does not disable configuration includes: the prescribed Git options reproduce exit 128 with “relative config includes must come from files,” preventing the mandatory dispatch/RESULT cap evidence; replace this with valid configuration isolation. [Git include semantics](https://git-scm.com/docs/git-config#_includes).

All required threat-row units are present. The narrowed declaration tests match their stated scope; same-UID replacement and deferred symlink/case-alias protections are explicitly residual. The Codex-only, no-escalation restriction excludes the Claude/Linux unsandboxed-gh exception.

📝 まとめ: Completed the read-only task-text and cited-record review; two findings require orchestrator disposition.
Not checked: implementation, CI or deployment; no files changed, and dispatch remains blocked.

Verdict: incorrect.orchestration/validation/dotfiles-T133-python-pin-a01-text-security-ed75bc6.md.last.md
- [P2] High confidence .orchestration/tasks/dotfiles-T133-python-pin-a01.md:132 — The completeness requirement is uncommented prose inside the executable Bash block; `bash -n` reproduces exit 2, so Commands (f) cannot execute its required completeness check as written.
- [P2] High confidence .orchestration/tasks/dotfiles-T133-python-pin-a01.md:166 — Dispatch requires Commands (f), which now requires this task’s PR `changedFiles`, but the worker creates that PR after dispatch at line 173; the prerequisite is circular, and historical PR #434 cannot establish this task’s completeness.

All required threat-row units are present. The closed tests cover declaration grammar and policy consistency. Absolute bindings and the clean parent address shim and inherited `GIT_*` inputs; Codex-only sandbox execution excludes the Linux unsandboxed-`gh` exception. Symlink/case-alias enforcement, executable provenance and unrestricted same-user replacement remain explicitly residual.

📝 まとめ: Completed the read-only task-text and cited-record review; two findings await orchestrator disposition.
Not checked: implementation, CI or deployment; no files changed, and disclosed host-provenance risks remain.
Verdict: incorrect
**Reviewing supply chain exception scope**
exec
/bin/zsh -lc "sed -n '112,135p' .orchestration/plans/024-design-quality.md; rg -n 'threat.table|threat table|residual|Pre-dispatch' ~/.agents/skills/agmsg-orchestration/SKILL.md; cat .orchestration/validation/dotfiles-T133-python-pin-a01-audit-e9819d4.md.last.md" in ~/Workspace/dotfiles
 succeeded in 0ms:
6. **正直な残余** 境界だけが緩和するリスクを `closed` と書かない。各文は残余を 1 行で明記する。
0. **脅威モデル（D-024-21）** 席は同じ OS ユーザで動き、ホストは席間の信頼境界ではない（同一 UID のプロセスは symlink 差し替え、共有 `.git` の object 差し替え、hook の子プロセス、Herdr socket 経由の host 実行で、ホスト内のどの検査も迂回できる）。regime の硬い境界は GitHub（保護された main、必須チェック、orchestrator の identity によるマージ）。ただしこの境界は **worker 席が orchestrator の GitHub 資格情報を共有しない**ときだけ成立する（D-024-22：worker 席は専用の GitHub identity（別アカウントまたは App のトークン）で `gh` に login し、ruleset の bypass 一覧に入らない。orchestrator の keychain トークンを worker の config dir に持ち込まない。identity が分かれるまで「GitHub が境界」は未成立と書く）。**同一 macOS ユーザでは資格情報は分離できない**（gh は keychain の項目を host/user で引き、同じ UID の gh は orchestrator のトークンを読める。`GH_CONFIG_DIR` は設定を分けるだけ）。防止には worker 席を別の OS ユーザ（または別ホスト）で動かすしかなく、それは D-024-23 の将来項目（P1-16、操作者の判断）。それまで GitHub 境界は **検知**で守る：記録は boundary の記録 PR まで main に無いので、検知は次の記録 PR の regime ジョブで行う（`.orchestration/acceptance/**` に触れる PR で、前回 boundary 以降の main の各マージ commit に、gate 通過の証跡を持つ受け入れ記録が対応することを検査し、無ければその PR を失敗させる；P1-11 owner a02 の行 `ci:detection:1`）。main push 時点の検知は記録が無いので不可能であり、文は「次の記録 PR で検知、防止ではない」と書く。悪意ある worker に耐えるべき入力（承認台帳、gate が読む証跡 of record）は GitHub から sha 指定で API 経由（sandbox 内）に読み、ローカルファイルやローカル object database からは読まない。ホスト内の制御（本節 1〜10）は事故と prompt injection による損害の抑制であり、文はそう書く。
8. **承認はコミット済み台帳から読む** permission の決定行（`scope=permission approved_by=user diff_sha256=…`）は anchored checkout の作業コピーではなく、コミット済みの台帳から読む。読み方は `git ls-remote origin refs/heads/main` が返す commit sha を取り、GitHub API（`gh api repos/<owner>/<repo>/contents/.orchestration/decisions.tsv?ref=<sha>`、sandbox 内）でその sha の内容を取得する。ローカルの `git show` は共有 object database が書けるため中間 tree の差し替えで偽物を返しうる（第 3 回審査の所見 2）（ローカルの ref 名 `origin/main` は経由しない。`refs/replace/` も書けるので replacement を無効にする。Codex worker は `.git/objects` と `.git/refs` に書けるので ref は差し替えられるが、sha で指した object は内容アドレスで偽造できない）。作業コピーの行は提案で、記録 PR が main にマージされて初めて承認になる（PR の承認は操作者の操作）。偽造には main へのマージが要る。 The same applies to the PR content a mechanism evaluates (the verdict, the audit precheck, the counters): the changeset is read from GitHub at the 40-hex head (`gh api repos/{owner}/{repo}/compare/<base40>...<head40>`, `…/contents/<path>?ref=<head40>`) or from a private clone whose object store no worker can write; the main checkout's shared `.git/objects` and its `origin/main` ref are not evidence sources, because Codex workers write them (a04 C-80 round 1, 2026-10-19). Evidence files are named and matched by the full 40-hex head, never by a 7-character prefix. Every `gh` invocation names the repository explicitly: `gh pr`, `gh run` and `gh issue` subcommands take `--repo mryfmo/dotfiles` or the full pull-request URL, and `gh api` (which has no `--repo` flag) takes the explicit `repos/mryfmo/dotfiles/…` endpoint path, never a `{owner}/{repo}` placeholder; a `gh api graphql` call binds the repository through fixed query variables (`owner: "mryfmo"`, `name: "dotfiles"` as constants in the script, passed with `-f`/`-F`) and uses only node ids obtained from a query bound by those variables (verdict a04 C-80 round 5, 2026-10-19): the local repository configuration selects the default repository otherwise, and a matching head sha does not bind the repository because a fork can hold the same commit (verdict a04 C-80 round 2, 2026-10-19). A mechanism whose application path runs code this contract does not yet cover (the agmsg storage layer sourced by `dispatch.sh`/`history.sh`; the integration gate until its own hardening task lands) names that task as the prerequisite of its `--apply` mode and runs shadow-only until the prerequisite is merged. The sha of canonical `main` comes from the fixed repository's API (`gh api repos/mryfmo/dotfiles/git/ref/heads/main --jq .object.sha`), never from `git ls-remote origin`, whose destination the local remote and URL-rewrite configuration control (P1-12 a04 C-80, 2026-10-19T20:01Z); the content read at that sha comes from `repos/mryfmo/dotfiles/contents/<path>?ref=<sha40>`. Every `gh api` call that decides also binds the host with `--hostname github.com` (`GH_HOST` and the hosts configuration select the API host otherwise), a subcommand binds it through the `github.com/mryfmo/dotfiles` form of `--repo`, and a test that exports a hostile `GH_HOST` shows the call still names github.com or refuses (a02 review b2a186e, 2026-10-19T20:36Z).
9. **私設キャッシュ** orchestrator 側の実行は worker と共有するキャッシュ（`~/.cache/uv`、`~/.local/share/uv`、mise）から実行可能物を読まない。`UV_CACHE_DIR` を anchored checkout 配下（`.agents/worklog/uv-cache`、gitignored、worker 書き込み不可）に固定し、`uv run --no-config --no-project --offline --python <信頼ルートの絶対パスのインタプリタ>` で起動する（`--no-config` で uv の設定探索を止め、`--python` の絶対パスで cwd や親の `.venv` の発見を止める；敵対的な `.venv` と `uv.toml` を置いた fixture で検証）。hook は uv を使わず jq と python 標準ライブラリだけで動く。 One trusted interpreter resolver (`scripts/orchestrator/trusted-interpreter.sh`, P1-3 lineage) resolves `<abs>` from the repository's pinned declaration to a regular file under the tool manager's install root (the install root is anchored to the passwd home of the real uid, never to the HOME variable, which a caller can forge), refuses anything else, and every orchestrator-side script consumes it; no script keeps its own `command -v`, `mise which` or PATH fallback (ci-rerun.sh security review 44cb835, 2026-10-19). Shell code of other projects (the agmsg storage layer and its `drivers.partition` sourcing) is never sourced by an orchestrator-side mechanism; counters are read from the agmsg SQLite store read-only with a fixed query or from the pasted record. Every Python child of a trusted entrypoint runs with `-I` (isolated: no user site, no `PYTHON*` environment, no script directory on `sys.path`), so `uv run … python -I <script>` rather than `--script` for a script without declared dependencies; a test plants a `.pth` and a `usercustomize.py` in a fake user site and asserts they never execute (P1-15 amendment 5 C-80, 2026-10-19). A program takes `UV_CACHE_DIR` from the environment the trusted parent supplies and refuses when it is absent or not an absolute path; it never computes a default from its own root. The orchestrator's parent prefix sets the main checkout's `.agents/worklog/uv-cache`; a worker's launcher sets `<worktree>/.uv-cache` (the P1-15 worker launch value: `.agents/` is read-only in the Codex permission profile, so a root-derived `.agents/worklog/uv-cache` cannot be created by a worker; P1-12 a03, 2026-10-19T11:28Z); tests set a temporary directory.
10. **worker は sandbox 外でコマンドを実行しない（D-024-17 の改訂）** 2026-10-19T03:45Z の実測で `gh api` は Claude sandbox の中から成功した（sandbox の proxy は CONNECT 型で TLS を終端しない；keychain のトークンも読めた）。worker 席の除外コマンドは空にし、gh も git push も sandbox 内の proxy 経由で実行する。Codex 席は `sandbox_workspace_write.network_access = true` で同じ状態にし、permgate の codex ポリシーは sandbox 外への escape を承認しない（permgate の変更は操作者の手順）。wrapper 方式（絶対パス、env -i、固定 GH_CONFIG_DIR）は LD_PRELOAD と引数転送（`gh repo clone -- --config`）を閉じられないので採らない。
7. **検証** threat_table は本節の項目 1〜10 に 1 行ずつ対応させる（参照だけでは足りない）。共通テスト補助 `tests/unit/trusted_exec_contract.py`（P1-6 で作る）を使い、仕組みごとに 4 つの red→green テストを持つ：PATH 先頭の shim が実行されない、植え付けた GIT_* と git 設定が効かない、worker ルート配下の信頼パスが拒否される、検証後に差し替えたファイルが消費側に届かない。
68:- A design review runs in paired rounds. Both reviewers, a fresh Claude context on the `review` profile and a Codex read-only run under a `codex-review` identity, get the same design hash at the same time. The orchestrator revises once per pair of results and opens no round while one is still open. The third pair is the last: on its accept the design is frozen at the hash the pair last accepted, the third pair's own, and whatever is still open at that hash becomes a residual list that is worker input; on its revise or reject nothing is frozen and the design goes back to a context other than its author, never to a fourth pair; a revision after the third pair is not made, and any later change to a hashed key is a new pair (INV-7). The review judges the invariants, threat model, trust anchors and premises for contradiction and enforceability, never implementation detail.
71:- A task that touches a trust boundary (anything the design tier lists, CI that decides a required check, code that executes PR-controlled input) carries a `threat_table` in its front matter: one `{control, disposition}` row per thing the PR or the orchestrator controls (the tree and its tests, task.md, workflow files, interpreter and environment files, in-process effects, new or renamed scripts, metadata separators). The row unit is one row per `allowed_files` entry, one row per listed control that is not a path (task metadata, workflow and interpreter or environment inputs, in-process effects, new or renamed scripts, metadata separators), carried by the declared test module's row where that is where the control acts, and one row per orchestrator effect from the fixed list (forced removal, merge, update-branch); under a wildcard `allowed_files` entry whose files are executed or applied (scripts, workflows, hooks, settings, the rules seats follow), one row per concrete file the PR changes; a wildcard over test fixtures or other data files keeps one row; C4 and C7b of `scripts/orchestrator/task-consistency-check.py` verify the path half before dispatch, and the task-file review checks the rest. A disposition takes one of three forms: `closed: tests/<file>::<name>`, the test that closes the row; `residual: <sentence>`, the compensating control; `out-of-scope: <task id>`, the task that owns the row. The task-file review checks the three shape rules by hand: a `closed` selector names a test present in the PR tree at acceptance, an `out-of-scope` owner is a task id in the design's `implementing_tasks`, a `residual` payload is a sentence of at least 20 characters (the gate's minimum for a reason). For a `closed` row it checks the selector's form only, since the test does not exist before implementation. Substance is the reviewers': the task-file review, the Bot and the auditor judge each row against the diff. The table is the task's completion condition: a missing row is added once, counted as an amendment, never fixed finding by finding.
164:6. Send `AGMSG-TASK v1` with the exact artifact paths and `done_signal=AGMSG-RESULT`. Pass every `send.sh`/`poke.sh` body with `--body-file <path>` (both take it in agmsg v1.5.0), never as a positional argument: a positional `<text>` passes through the caller's own shell first, where a backtick or `$( )` in the body silently executes and vanishes from what arrives (upstream #378). `agmsg-dispatch` is the one exception and takes a single-line, shell-safe positional message. Pick the path by how the recipient is seated, never by inferring pane or agent status: a worker in a `herdr-agents` pane gets `agmsg-dispatch <team> <from> <to> <pane_id> "<message>"` (send, generic wake, `read_at` wait; single-line shell-safe text only), the sanctioned wake path until worker seating writes placement records at launch, because `poke.sh` exits 1 with "no placement record" for a hand-joined member, and a herdr-agents worker gets a record only once it acts from its own pane (upstream `send.sh`/`inbox.sh` record the acting pane, #1109); a spawn-seated member (placement record `run/spawn.*`; `team.sh <team> --json` shows its pane) gets `poke.sh <team> <name> --body-file <path> [--retries N --retry-delay SECONDS --backoff fixed|exponential]`, which types and submits in one call and refuses to type over an in-progress draft (#1321/#1322); a pane-less member gets `send.sh <team> <from> <to> --body-file <path>` and its own delivery mode. Verify delivery via the messages.db `read_at` column. `poke.sh` exit codes: 10 = terminal unreachable, 12 = pane gone or no live agent, 14/15 = refused to type over a changing or unlocatable input box, 13 = the driver has no poke path for this pane (for example a `plain` terminal); where poke.sh's narrow agmsg-message fallback succeeds it exits 0, so 13 means nothing was delivered, and the printed reason names the native channel, asks the caller to claim its own identity first, or reports that the fallback failed. Never retry a 13 as `send.sh` yourself: that overrides the driver's considered refusal and can double-deliver. Seating case: a worker in an unviewed or headless Herdr workspace (no client attached, a small pane rect such as 18x41) makes `poke.sh` exit 14/15 from its TUI input locator; that is a locator refusal, not evidence about the worker's state, so wake it with `agmsg-dispatch` and verify `read_at`. Every dispatch (TASK, ACCEPTANCE, PING) is recorded in the current acceptance record under a `dispatch:` key as the bus line with its read marker, so the orchestrator creates that record, `.orchestration/acceptance/<task>.md`, before the task's first dispatch (`scripts/orchestrator/dispatch.sh` refuses a record that does not exist or that names another task); a seat is reported as working only from such a line, and after a context compaction the open TASK list is re-derived from a bus read that is refused when it reaches its limit (`bus-read.sh` exits when the history reaches `BUS_READ_LIMIT`; the orchestrator raises the limit and reads again), never from a default-limited one and never from a read whose truncation went unnoticed. A seated worker idle for 20 minutes since its latest bus event for the task while a dispatchable task exists (INV-10's idle figure; its 30 minutes is the first-push deadline) gets a bus read, then a PING; a longer silent wait is never the answer. `scripts/orchestrator/dispatch.sh` writes the line and `scripts/orchestrator/bus-read.sh` performs the read and prints the minutes since each open task's latest event (both on main since a03c1daa, plan 007 T718); the orchestrator applies the 20-minute figure to the minutes the script prints (the script's own silence flag still uses 30 minutes, a recorded residual of the tools lineage).
The implementation matches the requested pin and tests; three defects remain in the orchestrator’s artifacts.

[P1] high orchestration .orchestration/acceptance/dotfiles-T133-python-pin-a01.md:9 The record documents at least five RESULTs and three TASK dispatches, exceeding INV-6’s two-revise/two-amendment thresholds, but contains no counter snapshot or required independent design reset; marking continuations `round=0` does not exclude blocked RESULTs from those counts.

[P2] high orchestration .orchestration/acceptance/dotfiles-T133-python-pin-a01.md:15 The machine-readable `ledger`, `replans`, and `searches` are empty despite repeated findings and three prose replans; the gate reads these JSON fields, so it cannot enforce S1/S6 against the recorded history.

[P2] high specification .orchestration/dotfiles-T133-python-pin-a01/task.md:162 The dispatched specification still prohibits dispatch until its failed prerequisite evidence is replaced, while `premises` retains that failure; appended successful probes do not reconcile this contradictory completion condition.

The task declares no numbered invariants; these audit labels enumerate its explicit obligations:

INV-1: holds home/dot_mise/config.toml:5 — exact `3.15.0` pin and required reason.
INV-2: holds tests/unit/test_mise_config.py:8 — one test, ASCII fullmatch, four required negatives; recorded red/green matches the implementation.
INV-3: holds tests/unit/test_supply_chain_policy.py:375 — Python exception preserves other tools’ policy.
INV-4: holds .orchestration/dotfiles-T133-python-pin-a01/task.md:174 — four allowed paths, 3/6 code lines, 19/40 test additions, 200/210 task lines.
INV-5: holds .orchestration/dotfiles-T133-python-pin-a01/task.md:181 — dispatched copy and SHA-256 match.
INV-6: violated .orchestration/acceptance/dotfiles-T133-python-pin-a01.md:9 — regime reset thresholds were not handled.
INV-7: violated .orchestration/dotfiles-T133-python-pin-a01/task.md:162 — prerequisite evidence remains contradictory.

[PR #437](https://github.com/mryfmo/dotfiles/pull/437)’s final-head CI passed. Design §5.14’s declaration requirement is satisfied; executable provenance and deployment remain explicitly residual.

Orchestration findings: 3

📝 まとめ: Read-only audit completed; implementation checks passed, with three artifact findings requiring disposition.
Not rerun: full tests, Bats, or deployment. Runtime provenance remains unverified; nothing was modified.
Verdict: incorrect
**Verifying technical details**
web search: 
web search: https://cli.github.com/manual/gh_help_environment
**Verifying line counts and commit hashes**
**Assessing syntax and path handling issues**
**Reviewing task verification and command parsing**
codex
先行レビューの PATH・環境変数・gh 設定・比較 API の件数上限に関する指摘は、本文に対策が反映されています。Codex 席で全コマンドを sandbox 内に限定するため、Linux の sandbox 外 gh 例外もこのタスクには適用されません。残る照合は、継承した変更を含む threat row の網羅性です。
**Confirming task completion and source verification**
web search: 
web search: 'GH_CONFIG_DIR'
exec
/bin/zsh -c '/usr/bin/shasum -a 256 .orchestration/tasks/dotfiles-T133-python-pin-a02.md; /usr/bin/wc -l .orchestration/tasks/dotfiles-T133-python-pin-a02.md' in ~/Workspace/dotfiles
 succeeded in 0ms:
68fd5f2e6b36d89789d1723caba932666c7719c09aeae154a3f049d31542d862  .orchestration/tasks/dotfiles-T133-python-pin-a02.md
     176 .orchestration/tasks/dotfiles-T133-python-pin-a02.md

**Concluding review summary**
codex
No findings in the reviewed task text (`68fd5f2e…`). Independent review agreed.

All required threat-row units are present. The closed rows cover declaration syntax only. The clean parent removes inherited `GIT_*` inputs; fixed executable bindings avoid mise shims; GitHub evidence names the repository and full SHAs. Fresh `GH_CONFIG_DIR` and explicit credentials address the earlier configuration-redirection finding. [GitHub CLI documentation](https://cli.github.com/manual/gh_help_environment)

Codex-only, sandbox-only execution excludes the Linux unsandboxed-gh exception. Executable provenance, symlink/case-alias enforcement and unrestricted same-UID replacement remain explicitly residual; the text does not claim to close them. No additional decision-to-execution gap was identified within that stated scope.

📝 まとめ: Completed the read-only task-text, threat-table and cited acceptance/review assessment; no files changed.
Not checked: implementation, CI, deployment or fresh prerequisite execution; the disclosed host-execution risks remain.
Verdict: correct
hook: Stop
hook: Stop Completed
tokens used
78,644
No findings in the reviewed task text (`68fd5f2e…`). Independent review agreed.

All required threat-row units are present. The closed rows cover declaration syntax only. The clean parent removes inherited `GIT_*` inputs; fixed executable bindings avoid mise shims; GitHub evidence names the repository and full SHAs. Fresh `GH_CONFIG_DIR` and explicit credentials address the earlier configuration-redirection finding. [GitHub CLI documentation](https://cli.github.com/manual/gh_help_environment)

Codex-only, sandbox-only execution excludes the Linux unsandboxed-gh exception. Executable provenance, symlink/case-alias enforcement and unrestricted same-UID replacement remain explicitly residual; the text does not claim to close them. No additional decision-to-execution gap was identified within that stated scope.

📝 まとめ: Completed the read-only task-text, threat-table and cited acceptance/review assessment; no files changed.
Not checked: implementation, CI, deployment or fresh prerequisite execution; the disclosed host-execution risks remain.
Verdict: correct
