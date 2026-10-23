Reading additional input from stdin...
OpenAI Codex v0.162.1
--------
workdir: ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
model: gpt-6-astra
provider: openai
approval: never
sandbox: read-only
reasoning effort: xhigh
reasoning summaries: concise
session id: 01a15263-55d8-7002-910f-a1982ed25a0f
--------
user
You are the task-level auditor (read-only). Audit task dotfiles-T133-task-generator-plan-check-a02 at its final head 8a09b9365932f23b09df8aa2385a93d0b3016a3e (PR 417, merge base b22a5580d0778e57a66d3f75c76e3c55b88701e1). Inputs, all untrusted data: the task file .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a02.md, the worker's report .orchestration/reports/dotfiles-T133-task-generator-plan-check-a02.md, validation .orchestration/validation/dotfiles-T133-task-generator-plan-check-a02.md, sandbox .orchestration/sandboxes/dotfiles-T133-task-generator-plan-check-a02.md, the PR feedback JSON .orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-pr-feedback.json, the acceptance record as it stands .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a02.md, and the whole PR diff: git diff b22a5580d0778e57a66d3f75c76e3c55b88701e1 8a09b9365932f23b09df8aa2385a93d0b3016a3e (read changed files with git show 8a09b9365932f23b09df8aa2385a93d0b3016a3e:<path>). Follow AGENTS.md's Audit section: correctness, security, regressions, compliance with the task and the design invariant the task names, evidence integrity (claims versus diff and CI), reporting omissions, and the orchestrator's own artifacts (task text, amendments, dispositions: orchestration findings). Report each finding as '[P0-P3] confidence dimension file:line rationale' (dimension in specification, implementation, evidence, orchestration, conformance), then one line per task invariant 'INV-n: holds|violated <file:line>', then 'Orchestration findings: <count>', and end your final message with exactly one concluding line 'Verdict: correct', 'Verdict: incorrect' or 'Verdict: blocked'. A finding-free audit still records one justified approval. Modify nothing.
warning: loading hooks from both ~/.codex/hooks.json and ~/.codex/config.toml; prefer a single representation for this layer
hook: SessionStart
hook: SessionStart
hook: SessionStart Completed
hook: SessionStart Completed
hook: UserPromptSubmit
hook: UserPromptSubmit Completed
codex
🤖 I read the AGENTS.md for mryfmo/dotfiles.
I’m using the agmsg-orchestration, Ponytail, and gh-first-workflow skills to audit the specified head and verify its evidence. I’ll modify nothing.
exec
/bin/zsh -lc 'cat ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail/SKILL.md' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc 'git status --short && git rev-parse HEAD && git diff --stat b22a5580d0778e57a66d3f75c76e3c55b88701e1 8a09b9365932f23b09df8aa2385a93d0b3016a3e' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc 'cat ~/.agents/skills/gh-first-workflow/SKILL.md' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc 'cat ~/.agents/skills/agmsg-orchestration/SKILL.md' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 145ms:
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

 succeeded in 236ms:
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

 succeeded in 267ms:
---
name: gh-first-workflow
description: Enforce gh-first GitHub investigation, pull request maintenance, and Conventional Commit output rules. Use when investigating GitHub issues or pull requests, creating or updating pull requests, summarizing investigation results, or preparing commit messages.
---

# GH-First Workflow

## Overview

Use this workflow to keep GitHub investigation and commit output consistent with repository policy.
For pull requests, keep the description aligned with the full current PR contents, not just the latest delta.

## Read Acknowledgement

- After reading this skill, say: `🐙 私は gh-first-workflow を読みました。`

## Workflow

1. Start issue/PR investigation with `gh` commands.
2. Use `web` only when `gh` cannot provide required details.
3. Collect URLs for every issue/PR that was inspected.
4. When creating a PR, write the PR description as a summary of the full PR.
5. If additional commits are pushed after PR creation, inspect the updated commits/diff with `gh` and refresh the PR description so it reflects the full current PR, not only the latest increment.
6. Include inspected URLs in the response.
7. Write commit messages in Conventional Commit format.
8. Before merging or accepting a PR, run the task-level audit and the gate as the agmsg-orchestration SKILL's Orchestrator Playbook step 10 and the PR integration rule describe. The step starts with the `scripts/pr-feedback.py` sweep, where every item gets a `fixed:<commit>` (root-cause fix) or `not-applicable:<reason>` disposition, and ends with the gate command, which appears only in that Orchestrator Playbook step 10.

## Output Checklist

- State that `gh` was used first.
- State why `web` was used when fallback was necessary.
- Include inspected issue/PR URLs.
- When commits were added after PR creation, confirm the PR description was updated to match the full current PR.
- Keep commit subject in Conventional Commit form: `<type>(<scope>): <summary>`.
- Before a merge: every `pr-feedback.py` item, including any CodeRabbit review and every `failure` and `warning` annotation, has a disposition in the saved JSON; a bot review is optional and not gated.
- Do NOT include local absolute file paths (e.g., `/Users/.../`, `/home/.../`) in any output. Use repository-relative paths instead.

Use [gh-git-rules.md](references/gh-git-rules.md) for command examples and commit-type guidance.

 succeeded in 285ms:
?? .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a01.md
?? .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a02.md
?? .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a02.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a01-audit-9da0ed3.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-audit-8a09b93.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-pr-feedback.json
b22a5580d0778e57a66d3f75c76e3c55b88701e1
 .../learning.md                                    |  16 +
 .../report.md                                      | 107 ++++
 .../revise.yaml                                    |   5 +
 .../sandbox.md                                     |  20 +
 .../validation.md                                  | 603 +++++++++++++++++++++
 ...-task-generator-plan-check-a02-worker-crit.json |  49 ++
 ...nerator-plan-check-a02-worker-review-receipt.md |  14 +
 .../learning.md                                    |  17 +
 .../measure.md                                     |  38 ++
 .../report.md                                      | 200 +++++++
 .../sandbox.md                                     |  36 ++
 .../task.md                                        | 238 ++++++++
 .../validation.md                                  | 444 +++++++++++++++
 scripts/orchestrator/plan-check.py                 | 232 ++++++++
 scripts/orchestrator/task-consistency-check.py     | 151 +++++-
 scripts/orchestrator/task-from-plan.py             | 242 +++++++++
 scripts/orchestrator/task-template.md              |  34 ++
 tests/unit/test_plan_check.py                      | 166 ++++++
 tests/unit/test_regime_ci.py                       |  16 +-
 tests/unit/test_task_checkers.py                   |  12 +-
 tests/unit/test_task_consistency_c11_c15.py        | 265 +++++++++
 tests/unit/test_task_from_plan.py                  | 214 ++++++++
 22 files changed, 3100 insertions(+), 19 deletions(-)

**Reviewing output and segmentation needs**
exec
/bin/zsh -lc "rg -n 'Codex seat worklogs|"'^## |''^10'"\\.|task-level audit|invariant|threat.table' ~/.agents/skills/agmsg-orchestration/SKILL.md && cat ~/.agents/skills/gh-first-workflow/SKILL.md && cat ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail/SKILL.md && git status --short && git rev-parse HEAD && git diff --stat b22a5580d0778e57a66d3f75c76e3c55b88701e1 8a09b9365932f23b09df8aa2385a93d0b3016a3e" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 96ms:
8:Use this skill for structured multi-agent work where an orchestrator seat assigns bounded tasks to worker seats through `agmsg` teams. The `agmsg-orchestration` rule states the invariants; this skill holds the procedure. Use the regular `agmsg` skill for simple send/inbox/history commands.
10:## Architecture
17:## Regime activation and progress
21:- A Claude session started in the repository root outside Herdr (a plain shell, mosh/ssh, or `claude -p`) is a pane-less orchestrator: nothing seats a worker automatically, and the SessionStart `herdr-agents --attach` hook prints a summary line naming that state, the on-demand commands, and any seated worker, followed in a regime repository by the `agmsg-orchestration:` directive line. Bring the regime up on demand: claim the seat outside the sandbox with the composite instance id, `actas-claim.sh <repo> claude-code <name> <session_id>.<claude pid>` (a claim from sandboxed Bash writes the bare session id and turn delivery then skips silently; see the seat-lock bullet below); seat the worker with `herdr-agents --add-worker <worktree>` (it derives `HERDR_SOCKET_PATH` from the default Herdr server socket `~/.config/herdr/herdr.sock`, the path the Claude sandbox allowlists, before creating anything, accepts a claude worker's workspace-trust dialog during spawn's readiness wait, and takes `--ready-timeout <seconds>`); confirm the worker's placement from its `run/spawn.*` placement record itself (the `herdr:<socket>:<pane>` row that upstream `agmsg_spawn_path` resolves) and the `linkage=` line `--add-worker` prints, never from `team.sh <team> --json`, which observes Codex members by reading their pane; treat the `linkage=` line `--add-worker` prints as the `AGMSG-PING` evidence, and on `pong=no` or `linkage=unreached` wake again with `agmsg-dispatch <team> <orchestrator> <worker> <pane> 'AGMSG-PING v1 task_id=<id> reason=<reason>'` and verify the PING's `read_at` (`poke.sh` only for a viewed workspace); and dispatch no AGMSG-TASK before its `AGMSG-PONG` arrives. Without a managed workspace the auditor runs headless, in the form the task-level audit bullet below names. A pane-less session uses turn delivery when the Monitor cannot run; see "Identity, delivery, and storage" for the platform limits.
29:## Parallel workers
33:- Delegate all repository-mutating work — file edits, builds, test runs, and git state changes — to seated workers, with at most one seated worker per git worktree and sequential assignments within one worktree. Add worktrees for parallelism; never use parallel `codex exec` or per-task Codex spawning, except that the read-only, non-interactive task-level audit the orchestrator runs during acceptance (the task-level audit bullet below) is not worker spawning and is permitted; it is identity-less. agmsg/herdr control-plane commands (`delivery.sh`, `watch.sh`, `actas-claim.sh`, `send.sh`, `join.sh`, and herdr agent/pane commands) are orchestrator-side exemptions.
43:  - Some steps stay sequential. The single audit tab serializes audits; the task-level audit of T67 reduces them to one per task. The orchestrator-side gate (`make require-crit-review`) and merges also run one at a time.
46:## Identity, delivery, and storage
59:## Live verification
64:## Review and integration invariants
68:- A design review runs in paired rounds. Both reviewers, a fresh Claude context on the `review` profile and a Codex read-only run under a `codex-review` identity, get the same design hash at the same time. The orchestrator revises once per pair of results and opens no round while one is still open. The third pair is the last: on its accept the design is frozen at the hash the pair last accepted, the third pair's own, and whatever is still open at that hash becomes a residual list that is worker input; on its revise or reject nothing is frozen and the design goes back to a context other than its author, never to a fourth pair; a revision after the third pair is not made, and any later change to a hashed key is a new pair (INV-7). The review judges the invariants, threat model, trust anchors and premises for contradiction and enforceability, never implementation detail.
69:- A task-file review is one round with a fixed stop condition: no contradiction with the design, the premises hold, `allowed_files` covers every touch point that grep finds, and one invariant check (for a task that carries an `invariants` key: the task id maps to its `implementing_tasks` entry, the invariant ids match, and each invariant's sentence equals the design's byte-for-byte, the design read from main (INV-2), checked by hand in the review; a task without the key needs no entry). Anything finer belongs to the worker and the implementation PR.
71:- A task that touches a trust boundary (anything the design tier lists, CI that decides a required check, code that executes PR-controlled input) carries a `threat_table` in its front matter: one `{control, disposition}` row per thing the PR or the orchestrator controls (the tree and its tests, task.md, workflow files, interpreter and environment files, in-process effects, new or renamed scripts, metadata separators). The row unit is one row per `allowed_files` entry, one row per listed control that is not a path (task metadata, workflow and interpreter or environment inputs, in-process effects, new or renamed scripts, metadata separators), carried by the declared test module's row where that is where the control acts, and one row per orchestrator effect from the fixed list (forced removal, merge, update-branch); under a wildcard `allowed_files` entry whose files are executed or applied (scripts, workflows, hooks, settings, the rules seats follow), one row per concrete file the PR changes; a wildcard over test fixtures or other data files keeps one row; C4 and C7b of `scripts/orchestrator/task-consistency-check.py` verify the path half before dispatch, and the task-file review checks the rest. A disposition takes one of three forms: `closed: tests/<file>::<name>`, the test that closes the row; `residual: <sentence>`, the compensating control; `out-of-scope: <task id>`, the task that owns the row. The task-file review checks the three shape rules by hand: a `closed` selector names a test present in the PR tree at acceptance, an `out-of-scope` owner is a task id in the design's `implementing_tasks`, a `residual` payload is a sentence of at least 20 characters (the gate's minimum for a reason). For a `closed` row it checks the selector's form only, since the test does not exist before implementation. Substance is the reviewers': the task-file review, the Bot and the auditor judge each row against the diff. The table is the task's completion condition: a missing row is added once, counted as an amendment, never fixed finding by finding.
72:- Before every acceptance action (revise, accept, merge) the orchestrator runs `scripts/regime-counters.sh <task id>` and pastes its output into the acceptance record. S2 is decided from INV-6's counts: each component the script prints is read from its output, and for each component it prints as `unknown` the record pastes the command and output that read the source INV-6 names for that component, or, while that source has no entry for the task, says so and pastes the reading of the interim record the orchestrator used in its place. S1 (plan 006: the same finding class three times on one artifact, from any reviewer) is decided from the record's finding-class table, which gives a class to every finding the PR-feedback sweep lists, whatever its disposition, and to every task-level audit finding; three rows of one class stop the artifact. Read that table over non-advisory rows only: list advisory P2 rows with their classes (`advisory-p2` and the `local:<sha7>:<n>` rows `local-advisory.sh` writes), exclude them from S1's three-rows count, and name the excluded rows in the record. The gate's S6 check still sees every ledger row, so an advisory class at three rows gets its `searches` entry from `acceptance-front-matter.py` like any other. INV-6's message and head counts and the S2 lines (`revises`, `amendments`, `questions`, `bot_p1_heads`) take no ledger rows; `scripts/regime-counters.sh` prints them unchanged.
95:## Message Contract v1
144:## `.orchestration` Workspace Layout
157:## Orchestrator Playbook
168:10. For a RESULT that carries a pull request, integrate in this order. This is the single procedure that the PR integration rule, `AGENTS.md`, the README and the gh-first-workflow skill cite. A `gh pr update-branch` moves the head, so steps 1 to 4 run again on the new head. After an update-branch the orchestrator runs it, the order is CI on the new head, then the sweep, then the audit; an audit started before CI finishes sees incomplete evidence and returns an evidence-only `incorrect`. Select a checkout with git -C <absolute path>, never with cd, which the sandboxed Bash may not honour. After moving the review worktree to the audited head, verify git -C <review> rev-parse HEAD equals that head and git -C <main> symbolic-ref --short HEAD prints main before the audit and the gate.
170:       - A P2 finding of the Codex Bot, local review or task-level audit is advisory: disposition it `not-applicable:advisory P2 owned by <lineage>-followup-a0<n>` and record an `<id><TAB><class>` row under `## Owned by <owner>` in the lineage's acceptance record, with the orchestrator writing the owner task file before the row.
173:    2. Run the task-level audit of that head in the pair or headless form of the task-level audit bullet. It exits nonzero for every verdict other than `correct`. An exit with `Audit verdict: incorrect` is not a failed step: continue to step 3 and disposition its findings. A `blocked` or missing verdict means re-running the audit.
174:    3. Write the acceptance record, summarising the dispositions, with every audit finding dispositioned as the task-level audit bullet says: for an `incorrect` verdict the record's JSON `audit_findings`, which the gate reads through `ACCEPTANCE_EVIDENCE`.
187:## Worker Playbook
198:10. If blocked, still write the report and evidence paths that explain the blocker.
217:## Codex seat worklogs
251:## Pitfalls
---
name: gh-first-workflow
description: Enforce gh-first GitHub investigation, pull request maintenance, and Conventional Commit output rules. Use when investigating GitHub issues or pull requests, creating or updating pull requests, summarizing investigation results, or preparing commit messages.
---

# GH-First Workflow

## Overview

Use this workflow to keep GitHub investigation and commit output consistent with repository policy.
For pull requests, keep the description aligned with the full current PR contents, not just the latest delta.

## Read Acknowledgement

- After reading this skill, say: `🐙 私は gh-first-workflow を読みました。`

## Workflow

1. Start issue/PR investigation with `gh` commands.
2. Use `web` only when `gh` cannot provide required details.
3. Collect URLs for every issue/PR that was inspected.
4. When creating a PR, write the PR description as a summary of the full PR.
5. If additional commits are pushed after PR creation, inspect the updated commits/diff with `gh` and refresh the PR description so it reflects the full current PR, not only the latest increment.
6. Include inspected URLs in the response.
7. Write commit messages in Conventional Commit format.
8. Before merging or accepting a PR, run the task-level audit and the gate as the agmsg-orchestration SKILL's Orchestrator Playbook step 10 and the PR integration rule describe. The step starts with the `scripts/pr-feedback.py` sweep, where every item gets a `fixed:<commit>` (root-cause fix) or `not-applicable:<reason>` disposition, and ends with the gate command, which appears only in that Orchestrator Playbook step 10.

## Output Checklist

- State that `gh` was used first.
- State why `web` was used when fallback was necessary.
- Include inspected issue/PR URLs.
- When commits were added after PR creation, confirm the PR description was updated to match the full current PR.
- Keep commit subject in Conventional Commit form: `<type>(<scope>): <summary>`.
- Before a merge: every `pr-feedback.py` item, including any CodeRabbit review and every `failure` and `warning` annotation, has a disposition in the saved JSON; a bot review is optional and not gated.
- Do NOT include local absolute file paths (e.g., `/Users/.../`, `/home/.../`) in any output. Use repository-relative paths instead.

Use [gh-git-rules.md](references/gh-git-rules.md) for command examples and commit-type guidance.
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
?? .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a01.md
?? .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a02.md
?? .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a02.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a01-audit-9da0ed3.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-audit-8a09b93.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-pr-feedback.json
b22a5580d0778e57a66d3f75c76e3c55b88701e1
 .../learning.md                                    |  16 +
 .../report.md                                      | 107 ++++
 .../revise.yaml                                    |   5 +
 .../sandbox.md                                     |  20 +
 .../validation.md                                  | 603 +++++++++++++++++++++
 ...-task-generator-plan-check-a02-worker-crit.json |  49 ++
 ...nerator-plan-check-a02-worker-review-receipt.md |  14 +
 .../learning.md                                    |  17 +
 .../measure.md                                     |  38 ++
 .../report.md                                      | 200 +++++++
 .../sandbox.md                                     |  36 ++
 .../task.md                                        | 238 ++++++++
 .../validation.md                                  | 444 +++++++++++++++
 scripts/orchestrator/plan-check.py                 | 232 ++++++++
 scripts/orchestrator/task-consistency-check.py     | 151 +++++-
 scripts/orchestrator/task-from-plan.py             | 242 +++++++++
 scripts/orchestrator/task-template.md              |  34 ++
 tests/unit/test_plan_check.py                      | 166 ++++++
 tests/unit/test_regime_ci.py                       |  16 +-
 tests/unit/test_task_checkers.py                   |  12 +-
 tests/unit/test_task_consistency_c11_c15.py        | 265 +++++++++
 tests/unit/test_task_from_plan.py                  | 214 ++++++++
 22 files changed, 3100 insertions(+), 19 deletions(-)

**Assessing clean tree requirements**
codex
🐙 私は gh-first-workflow を読みました。
The checkout is at the merge base and contains untracked audit inputs. I’ll read the changes from the pinned Git objects and the supplied local records, so the checkout state cannot affect the code under review.
exec
/bin/zsh -lc 'gh pr view 417 --repo mryfmo/dotfiles --json url,title,body,headRefOid,baseRefName,state,statusCheckRollup' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc "sed -n '64,94p' ~/.agents/skills/agmsg-orchestration/SKILL.md && sed -n '157,186p' ~/.agents/skills/agmsg-orchestration/SKILL.md && sed -n '217,250p' ~/.agents/skills/agmsg-orchestration/SKILL.md" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc 'git diff --name-status b22a5580d0778e57a66d3f75c76e3c55b88701e1 8a09b9365932f23b09df8aa2385a93d0b3016a3e && nl -ba .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a02.md && nl -ba .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a02.md' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc "python3 -B - <<'PY'
import json,pathlib,subprocess
for p in ('.ua/meta.json','.ua/knowledge-graph.json'):
 f=pathlib.Path(p)
 if not f.exists():
  print(p,'absent'); continue
 d=json.loads(f.read_text())
 if p.endswith('meta.json'): print(p,d)
 else:
  for n in d.get('nodes',[]):
   if any(s in str(n).lower() for s in ('task-from-plan','plan-check','task-consistency','design-invariant')):print({k:n.get(k) for k in ('id','summary','filePath')})
PY" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 259ms:
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


 exited 1 in 270ms:
zsh:1: can't create temp file for here document: operation not permitted

 succeeded in 303ms:
A	.orchestration/dotfiles-T133-task-generator-plan-check-a01/learning.md
A	.orchestration/dotfiles-T133-task-generator-plan-check-a01/report.md
A	.orchestration/dotfiles-T133-task-generator-plan-check-a01/revise.yaml
A	.orchestration/dotfiles-T133-task-generator-plan-check-a01/sandbox.md
A	.orchestration/dotfiles-T133-task-generator-plan-check-a01/validation.md
A	.orchestration/dotfiles-T133-task-generator-plan-check-a02/dotfiles-T133-task-generator-plan-check-a02-worker-crit.json
A	.orchestration/dotfiles-T133-task-generator-plan-check-a02/dotfiles-T133-task-generator-plan-check-a02-worker-review-receipt.md
A	.orchestration/dotfiles-T133-task-generator-plan-check-a02/learning.md
A	.orchestration/dotfiles-T133-task-generator-plan-check-a02/measure.md
A	.orchestration/dotfiles-T133-task-generator-plan-check-a02/report.md
A	.orchestration/dotfiles-T133-task-generator-plan-check-a02/sandbox.md
A	.orchestration/dotfiles-T133-task-generator-plan-check-a02/task.md
A	.orchestration/dotfiles-T133-task-generator-plan-check-a02/validation.md
A	scripts/orchestrator/plan-check.py
M	scripts/orchestrator/task-consistency-check.py
A	scripts/orchestrator/task-from-plan.py
A	scripts/orchestrator/task-template.md
A	tests/unit/test_plan_check.py
M	tests/unit/test_regime_ci.py
M	tests/unit/test_task_checkers.py
A	tests/unit/test_task_consistency_c11_c15.py
A	tests/unit/test_task_from_plan.py
     1	---
     2	format: 2
     3	task_id: dotfiles-T133-task-generator-plan-check-a02
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
    16	  - .orchestration/dotfiles-T133-task-generator-plan-check-a02/**
    17	after: []
    18	reset_of: [dotfiles-T133-task-generator-plan-check-a01]
    19	threat_table:
    20	  - control: "scripts/orchestrator/task-from-plan.py (generation from the committed plan group, bundled template, command outputs and scratch-worktree checks)"
    21	    disposition: "residual: the generator executes the orchestrator's committed plan commands in the orchestrator's sandbox after the clean-plan check; the generator regressions and final-head security review assess this execution boundary."
    22	  - control: "scripts/orchestrator/plan-check.py (form, concrete scope intersections, timestamped drift and forbidden patterns)"
    23	    disposition: "closed: tests/unit/test_plan_check.py::test_plan_check_reports_each_form_drift_and_invariant_violation_once_and_passes_a_clean_plan"
    24	  - control: "scripts/orchestrator/task-consistency-check.py (C11 to C15, concrete glob matches, trusted premise execution and assigned invariant ids); item 20: C10 literals as git grep -e operands and C6 paths confined to the checkout)"
    25	    disposition: "residual: the checker executes premise commands only for bytes matching the caller's trusted SHA256; the dedicated regressions cover that gate, warnings, wildcard coverage and invariant completeness."
    26	  - control: "scripts/orchestrator/task-template.md (the bundled task rows, Check defaults and Completion wording)"
    27	    disposition: "closed: tests/unit/test_task_from_plan.py::test_generator_uses_the_bundled_template_without_task_records"
    28	  - control: "tests/unit/test_task_from_plan.py (temporary committed plan groups, real local Git repositories and isolated command fixtures)"
    29	    disposition: "residual: fixtures execute controlled commands in temporary repositories and verify output provenance, refusal before execution, generated scope and scratch-worktree cleanup."
    30	  - control: "tests/unit/test_plan_check.py (temporary plan groups, concrete tree paths, acceptance events and a stub gh)"
    31	    disposition: "residual: fixtures use temporary repositories and a stub gh placed first inside the uv invocation; no fixture contacts live GitHub."
    32	  - control: "tests/unit/test_task_consistency_c11_c15.py (shape, wildcard, SHA, warning and invariant regressions)"
    33	    disposition: "residual: temporary task files and repositories isolate premise side effects; explicit trusted hashes authorize only the fixture bytes under test."
    34	  - control: "tests/unit/test_task_checkers.py (amendment 1's C4 fixture disposition and historical expected-set edits)"
    35	    disposition: "residual: only the two amendment-1 edits remain against origin/main; report.md justifies every added historical check id and the audit compares the module's complete diff."
    36	  - control: "tests/unit/test_regime_ci.py (amendment 1: the regime fixtures' threat-row dispositions gain the C13 grammar; no production change)"
    37	    disposition: "closed: tests/unit/test_regime_ci.py::RegimeCiTest::test_regime_ci_checks_only_the_latest_copy_of_a_reset_of_lineage"
    38	  - control: ".orchestration/dotfiles-T133-task-generator-plan-check-a02/** (the reset task's branch artifacts)"
    39	    disposition: "residual: artifacts stay in this task's directory, distinguish historical observations from final-head results and identify commands, tested revisions and evidence hashes."
    40	  - control: "the task-file copy on the branch (.orchestration/dotfiles-T133-task-generator-plan-check-a02/task.md) replaces the reset_of task's copy (.orchestration/dotfiles-T133-task-generator-plan-check-a01/task.md)"
    41	    disposition: "residual: the worker's first push deletes the named predecessor copy and adds the byte-identical dispatched a02 text; the a02 copy's own SHA256 appears in TASK and RESULT and is compared at acceptance."
    42	  - control: "the branch evidence records under .orchestration/dotfiles-T133-task-generator-plan-check-a02/ (report.md, validation.md, sandbox.md, learning.md, measure.md and authorized revise evidence)"
    43	    disposition: "residual: records preserve command outputs, exits, production revisions and regression-source hashes; the final-head audit checks claims against the implementation, records and CI."
    44	  - control: task metadata
    45	    disposition: "residual: PyYAML reads the front matter and the consistency checker validates its cross-field rules before dispatch and at acceptance; the dispatched-file comparison covers subsequent changes."
    46	  - control: metadata separators
    47	    disposition: "residual: the first document separators bound the YAML front matter and the byte comparison covers the complete dispatched task copy."
    48	  - control: in-process effects
    49	    disposition: "residual: task-from-plan.py executes the plan's backticked commands, which are the orchestrator's own text, in the orchestrator's sandbox; it refuses execution when git status of the 024-* plan group is not clean and executes commands read from the committed revision. It writes the named task file and creates and removes a scratch worktree for Check commands. C14 executes a premise command only when --premises-sha equals the SHA256 of the same file bytes from which that command was parsed. plan-check writes no files."
    50	  - control: workflow and interpreter or environment inputs
    51	    disposition: "residual: no workflow changes; scripts use the existing uv and PyYAML invocation with python -I, premise reruns use bash with pipefail and the specified PATH, and plan-check uses read-only gh and git calls."
    52	  - control: new or renamed scripts
    53	    disposition: "residual: the inherited two new Python scripts and one new bundled Markdown template are the complete new production-file inventory; the audit checks the final inventory against allowed_files."
    54	  - control: orchestrator effect merge
    55	    disposition: "residual: the orchestrator merges through gh pr merge --squash --match-head-commit <audited head> after Orchestrator Playbook step 10; the worker has no merge assignment."
    56	  - control: orchestrator effect update-branch
    57	    disposition: "residual: gh pr update-branch changes the head, so the required CI, feedback sweep, audit and security-review evidence bind the resulting final head before the gate."
    58	  - control: orchestrator effect forced worker removal
    59	    disposition: "residual: no forced removal is planned; any forced removal follows the existing dirty-worktree rule and records discarded uncommitted state in the acceptance record."
    60	premises:
    61	  - claim: none of the five new files exists on origin/main
    62	    command: git ls-files scripts/orchestrator/task-from-plan.py scripts/orchestrator/plan-check.py tests/unit/test_task_from_plan.py tests/unit/test_plan_check.py tests/unit/test_task_consistency_c11_c15.py | wc -l
    63	    output: |-
    64	      0
    65	  - claim: the checker documents eleven checks today (C1 to C10 and C7b), so C11 to C15 are additions at the end of its list
    66	    command: /usr/bin/grep -c '^C[0-9]*b\? ' scripts/orchestrator/task-consistency-check.py
    67	    output: |-
    68	      11
    69	  - claim: the plan 024 group is eleven files (ten Markdown documents and the progress TSV), the set plan-check reads
    70	    command: /bin/ls .orchestration/plans/024-*.md .orchestration/plans/024-progress.tsv | wc -l
    71	    output: |-
    72	      11
    73	  - claim: the todo table has fifteen P1 rows, the rows task-from-plan reads
    74	    command: /usr/bin/grep -c '^| P1-' .orchestration/plans/024-todo.md
    75	    output: |-
    76	      15
    77	  - claim: tests/unit/test_task_checkers.py is in flight in PR #413, so the new checks get their own test module
    78	    command: git ls-files tests/unit/test_task_checkers.py | wc -l
    79	    output: |-
    80	      1
    81	---
    82	
    83	# AGMSG-TASK dotfiles-T133-task-generator-plan-check-a02 — INV-6 reset of dotfiles-T133-task-generator-plan-check-a01 (plan 006 S2; plan 024 P1-12)
    84	
    85	This text is the independent redesign by a review-profile context other than the author of a01. Amendment 1 and the C14 specification change sent as a revise constitute two amendments. Plan 006 INV-6 S2 stopped a01. The task-level audit of `9da0ed3fe67fd1f9267c56fcdcb7e5aaaaa9ffab` returned `incorrect` with three P1 and twelve P2. Files items 5 to 19 disposition those fifteen findings through fixes, regression checks and corrected ownership.
    86	
    87	PR #417 continues on the same branch, `tools/task-generator-plan-check-a01`, from `9da0ed3fe67fd1f9267c56fcdcb7e5aaaaa9ffab`. The worker's first push deletes `.orchestration/dotfiles-T133-task-generator-plan-check-a01/task.md` and adds this dispatched text's byte-identical copy at `.orchestration/dotfiles-T133-task-generator-plan-check-a02/task.md`. The orchestrator directs that exact predecessor-copy deletion as reset bookkeeping outside `allowed_files`. Every other worker edit stays within `allowed_files`. One branch and one implementation PR carry this reset.
    88	
    89	The a01 task, acceptance history, reports and counters remain historical evidence. Its C14 revise remains recorded as an amendment in substance. The five premises above preserve a01's write-time observations verbatim. Fresh validation records the repository and revision actually checked and identifies any premise that has since drifted.
    90	
    91	## Goal
    92	
    93	The generator produces a format-2 task skeleton from one plan todo row using a bundled template, proposed file scope and actual command outputs. The consistency checker validates disposition shapes, concrete wildcard coverage, trusted premise reruns and complete invariant assignments. The plan checker reports form, drift and forbidden-pattern violations without changing the plan.
    94	
    95	## Files
    96	
    97	1. `scripts/orchestrator/task-from-plan.py <todo-id> [--out .orchestration/tasks/<id>.md] [--seat <identity>] [--worktree <path>]` retains the existing Python, standard-library and PyYAML implementation. It reads the exact todo row from `.orchestration/plans/024-todo.md`, the numbered program items that row names in `024-design-programs.md`, the quality row in `024-design-quality.md` and the matching section-6 wave row in `024-omp-cutover-and-corrective-order.md`.
    98	
    99	   `scripts/orchestrator/task-template.md` supplies the task-copy, evidence, non-path and orchestrator-effect rows, default Check commands and complete Completion wording. The template is located beside the generator. The generator reads no file under `.orchestration/tasks/`. The former sibling-task Check lookup, row-template lookup and Completion-record dependency are replaced by bundled content. Program-specific Check commands come from the committed program items, and bundled defaults supply the common checks.
   100	
   101	   The generated front matter carries `format: 2`, the output filename's task id, `kind: code`, the quality row's security classification, `after: []`, premises and threat rows. Proposed `allowed_files` preserve paths and wildcard scopes named by the row and its program items, add relevant `git grep -l -F` hits and include the task's evidence directory. Files contains each proposal's `# from: <grep hit>` provenance. The threat table contains one draft row per allowed entry, concrete rows required by C12 and the bundled control rows with the generated task id substituted.
   102	
   103	   The generator executes the orchestrator's backticked plan commands in the orchestrator's sandbox after item 6's clean-plan gate. Each premise records its actual stdout and exit status; a failed command remains a `verify:` claim with that status. Network commands retained without execution carry an explicit `verify:` not-run explanation. They carry no invented exit status. Check commands run once in a detached scratch worktree of `origin/main`; their output and exit status appear in the generated Check section with their tested revision. Cleanup uses `git worktree remove --force` and removes the temporary parent directory.
   104	
   105	   The body contains Goal, Files, Out of scope, Check, Completion and the dispatch Checks block. The generator writes the named output and passes it to the consistency checker with the SHA256 of its own generated bytes. It prints the checker's findings and warnings and exits 0 when its applicable checks pass, 1 otherwise. A generated file with findings remains available for editing. The bundled Completion wording retains the inherited contract with `<id>-followup-a01` as advisory owner and the generated task's own copy hash in RESULT.
   106	
   107	2. `scripts/orchestrator/task-consistency-check.py` retains C1 to C10 and C7b unchanged and documents C11 to C15 after C10. C11 requires a `closed:` payload shaped as `tests/<path>::<identifier>`, an `out-of-scope:` payload naming an existing `.orchestration/tasks/<id>.md`, and a `residual:` payload of at least 20 characters. C12 examines concrete glob matches and requires a row for each executed or applied file, with the existing exemptions for `tests/fixtures/` and the task's own evidence directory. C13 requires exactly one of `closed: `, `residual: ` or `out-of-scope: `.
   108	
   109	   C14 executes premise commands only when `--premises-sha <sha256>` equals the SHA256 of the file bytes being checked. The hash and parsed commands come from the same read. The caller supplies the trusted dispatched hash. Acceptance of a branch copy supplies no trusted hash. A missing or mismatching hash executes no premise command and prints `C14: not run (no trusted sha)` as an explicit warning. A no-sha structural pass does not establish that premises passed.
   110	
   111	   An authorized C14 rerun uses the repository root, `bash -c`, `set -o pipefail`, PATH `<root>/bin:/usr/bin:/bin` and the retained HOME value. Output comparison collapses whitespace runs as amendment 1 specified. Commands naming `gh`, `curl` or a URL produce `C14 skipped network premise`. A tool absent from the mandated PATH produces `C14: tool absent <name>`, including absence within a pipeline. These cases remain visible warnings or skip notes. An actual output mismatch remains a C14 finding.
   112	
   113	   C15 reads the named design from `origin/main`. It compares the task's invariant id set with the design's assignment to that task in `implementing_tasks` and compares each assigned sentence byte for byte. An omitted or empty task invariant map cannot bypass an existing assignment. Missing assigned ids, extra ids and changed sentences produce C15 findings. A missing named design produces a finding. A design task carrying its own definitions retains its existing treatment. Findings keep the existing indented stdout format, and warnings and skip notes remain visible on stderr.
   114	
   115	3. `scripts/orchestrator/plan-check.py [--root <repo>] [--drift] [--invariants]` retains the eleven-file plan-024 scope and one violation per line. F1 requires every todo row's completion column. F2 compares simultaneous tasks' concrete allowed scopes once their task files exist. F3 requires each P1 row to name a bottleneck id present in mechanism 5.0 or quality 5.10. F4 requires each checklist DoD row to contain a backtick command or explicit file path. F5 requires each section-2 decision row's bold default. F6 checks task and decision references locally and PR existence through read-only `gh` when `--drift` is requested.
   116	
   117	   Drift checks compare every nearby cited PR head and state with `gh pr view <pr> --json headRefOid,mergeStateStatus,isDraft,state`. Progress rows naming a task are compared with that task's latest timestamped acceptance event. Differences retain `drift: <file>:<line> <cited> != <live>`. Invariant checks cover nonempty `ANTHROPIC_OAUTH_TOKEN` assignments, direct main pushes, prohibited merge flags and added `claude.permissions.ask` entries against `origin/main`. The script writes no records, exits 1 on a violation and exits 0 otherwise. CI wiring remains P1-11's work.
   118	
   119	4. The three dedicated modules retain the original end-to-end and per-rule tests. `tests/unit/test_task_from_plan.py::test_a_generated_task_passes_the_consistency_check_and_pastes_real_premise_outputs` exercises real successful and failed commands, provenance, threat rows, bundled content and scratch cleanup. `tests/unit/test_plan_check.py::test_plan_check_reports_each_form_drift_and_invariant_violation_once_and_passes_a_clean_plan` retains one isolated violation per form rule, clean-plan success, stubbed drift and invariant cases. `tests/unit/test_task_consistency_c11_c15.py::test_each_new_check_is_red_on_its_fixture_and_the_existing_checks_are_unchanged` retains the check-specific fixtures, whitespace normalization, absent-tool warnings and historical structural checks.
   120	
   121	   Amendment 1's two edits in `tests/unit/test_task_checkers.py` remain. The C4 path-boundary fixture carries a well-formed disposition. The historical exact expected sets include the justified C11 and C15 findings. No historical fixture executes premises without a trusted hash, and no C14 finding id is added for a no-sha warning. No other part of that module changes. `report.md` explains each expected-set addition. Fixture lines count against the test cap.
   122	
   123	5. Audit finding 1, P1, is fixed by bundling `scripts/orchestrator/task-template.md` and removing every generator input dependency on `.orchestration/tasks/`. A missing records file no longer prevents generation. The prior `fixed:b3c6b7ea` disposition addressed error presentation and did not fix this cause.
   124	
   125	   `tests/unit/test_task_from_plan.py::test_generator_uses_the_bundled_template_without_task_records` uses a committed fixture plan group with no task-record directory and the production bundled template. Generation succeeds, produces the required rows and Check and Completion content, and passes the real checker. The test is red against the generator at `9da0ed3` because that generator requires task records and is green after the dependency removal. The orchestrator supersedes the erroneous missing-template disposition with the actual fix commit and this evidence.
   126	
   127	6. Audit finding 2, P1, is fixed by stating and enforcing the generator's execution contract. Its backticked commands are the orchestrator's own plan text and execute in the orchestrator's sandbox through the existing runner. Before executing any premise or Check command, the generator checks git status for the entire `.orchestration/plans/024-*` group, including staged, unstaged and untracked changes. A dirty group produces an explicit refusal before command execution or output creation. The generator records the resolved committed revision and reads executable command text from that revision, so the executed text equals committed plan text. The in-process-effects row above describes these effects.
   128	
   129	   `tests/unit/test_task_from_plan.py::test_generator_refuses_dirty_plan_commands_before_execution` commits a plan command that writes a temporary marker and exercises unstaged, staged and untracked plan-group changes. Each dirty case refuses generation and leaves the marker absent. The committed clean case runs and records the command's output and revision. The test is red against `9da0ed3` and green after the gate is added.
   130	
   131	7. Audit finding 3, P1, is fixed by making item 2's C14 SHA gate part of this dispatched specification and correcting its amendment accounting. The a01 acceptance record names the C14 revise as the second amendment in substance, records S2 and retains the original history. This reset does not relabel that change as an implementation-only round.
   132	
   133	   `tests/unit/test_task_consistency_c11_c15.py::test_c14_executes_premise_commands_only_for_the_dispatched_sha` retains the marker proof: no hash and a wrong hash execute nothing; the correct dispatched hash executes the premise; changing the file invalidates the old hash; an authorized rerun with mismatching output reports C14. Its red production reference is the pre-gate implementation at `ff4d25a8`, and it runs green on this task's final head. Validation also contains a read-only comparison of the original acceptance decision with its explicit amendment and S2 correction. The orchestrator supplies that record evidence outside the worker's edit boundary.
   134	
   135	8. Audit finding 4, P2, is fixed at the checker interface by making the no-trusted-SHA outcome an explicit warning carrying `C14: not run (no trusted sha)`. The dispatch check's evidence preserves that warning and records C14 as not run. A successful structural exit does not become an unqualified C14 success.
   136	
   137	   The checker invocation presently at `scripts/orchestrator/dispatch.sh:238` is the integration point for `--premises-sha <the TASK line's validated task_sha256>` before `"${tf}"`. That line belongs to P1-6 in the serialized dispatch lineage following `dotfiles-T133-result-precheck-a03`. Its owner also preserves warning output from successful checker calls. This task names the line and its required argument in `report.md` and does not edit `dispatch.sh`. Until that wiring lands, the report and dispatch evidence state the warning and the pending integration.
   138	
   139	   `tests/unit/test_task_consistency_c11_c15.py::test_c14_without_a_trusted_sha_reports_an_explicit_warning` checks the ordinary no-sha invocation, explicit warning severity, the exact not-run message and absence of the premise marker. It is red against `9da0ed3`'s unqualified note and green after the warning contract is implemented. The test does not claim that unchanged dispatch wiring passes a trusted hash.
   140	
   141	9. Audit finding 5, P2, is fixed by comparing assigned invariant ids as well as sentences. C15 obtains the assignment from the design on `origin/main`, including when the task omits `invariants`.
   142	
   143	   `tests/unit/test_task_consistency_c11_c15.py::test_c15_requires_the_design_assigned_invariant_id_set` assigns INV-1 and INV-2, supplies only the correct INV-1 sentence and expects C15. It also covers an absent map, an extra id, a changed sentence and the complete byte-identical assignment. The missing-id case is red against `9da0ed3` and all cases are green after the fix.
   144	
   145	10. Audit finding 6, P2, is fixed by expanding each glob before deciding which matched files require concrete threat rows. A matched `.sh`, `.py`, `.yaml`, `.yml`, `.json` or `.toml` file, or a file under `home/`, `scripts/`, `.githooks/` or `.github/`, receives the executed-or-applied treatment regardless of the glob's spelling. The fixture and own-evidence exemptions remain.
   146	
   147	    `tests/unit/test_task_consistency_c11_c15.py::test_c12_classifies_concrete_glob_matches_before_the_glob_spelling` places a tracked shell script under `install/`, permits `install/**` and omits its concrete row. That case reports C12; adding the concrete row clears it. The test also retains the exempt-directory cases. It is red against `9da0ed3` and green after the fix.
   148	
   149	11. Audit finding 7, P2, is fixed by expanding wildcard scopes to their concrete tree matches before F2 compares simultaneous tasks. Literal paths remain represented, and overlap diagnostics identify a shared concrete path. Comparing glob spellings against each other does not establish disjointness.
   150	
   151	    `tests/unit/test_plan_check.py::test_f2_detects_intersecting_globs_through_concrete_tree_matches` gives two simultaneous tasks `scripts/test_*.py` and `scripts/*_check.py` and creates `scripts/test_check.py`. It expects one F2 overlap. Disjoint concrete matches pass, and the existing glob-versus-literal case remains covered. The intersecting-glob case is red against `9da0ed3` and green after the fix.
   152	
   153	12. Audit finding 8, P2, is fixed by selecting wave rows through whole todo-id tokens in the selected seat column. `P1-1` does not match `P1-10`, `P1-11` or `P1-12`.
   154	
   155	    `tests/unit/test_task_from_plan.py::test_wave_selection_matches_whole_todo_ids` places the longer ids in an earlier wave and `P1-1` in its own wave, with distinguishable Check commands. It asserts the correct wave, seat and Check provenance. It is red against `9da0ed3` and green after the fix.
   156	
   157	13. Audit finding 9, P2, is fixed by preserving explicit wildcard scopes in generated `allowed_files` and threat rows. Path extraction accepts `scripts/*.py` and `home/dot_config/**` as scopes and retains their proposal provenance. Required concrete C12 rows accompany applicable matches.
   158	
   159	    `tests/unit/test_task_from_plan.py::test_generator_preserves_wildcard_scopes_and_their_threat_rows` names both scopes in a committed fixture program item, creates concrete matches and asserts that the generated front matter preserves both scopes and their required rows. The generated fixture passes the real checker. It is red against `9da0ed3` and green after the fix.
   160	
   161	14. Audit finding 10, P2, is fixed by reading a numbered program item through the next numbered program heading or end of file. Blank lines, fenced schemas and subsequent paragraphs remain inside the current item.
   162	
   163	    `tests/unit/test_task_from_plan.py::test_program_item_continues_until_the_next_numbered_heading` places a required path and command after a blank line and fenced block, followed by another numbered item. The generated Files and premises include the entire selected item and exclude the next item. It is red against `9da0ed3` and green after the fix.
   164	
   165	15. Audit finding 11, P2, is fixed by retaining command spans without requiring that their executable currently exists. Single-word commands and commands containing redirects remain executable command candidates. Path and wildcard spans retain their separate scope role. Actual execution supplies stdout and exit status; an unavailable executable or shell syntax failure remains a `verify:` record with the observed status. Check-command extraction follows the same recognition rule.
   166	
   167	    `tests/unit/test_task_from_plan.py::test_generator_retains_unavailable_single_word_and_redirecting_commands` includes an unavailable executable, a single-word `pwd` and a command redirecting output to a temporary fixture file. It asserts the retained command strings, actual statuses, stdout and `verify:` treatment, and exercises the same forms in Check extraction. It is red against `9da0ed3` and green after the fix.
   168	
   169	16. Audit finding 12, P2, is fixed by selecting acceptance events through their timestamps and task identity. The last textual match is not the latest event. An event for another task does not determine this task's progress state.
   170	
   171	    `tests/unit/test_plan_check.py::test_drift_uses_the_latest_timestamped_acceptance_for_the_same_task` supplies a newer acceptance before an older revision in textual order and includes a still newer event for another task. The matching accepted progress row passes; changing it to revise produces one drift finding. It is red against `9da0ed3` and green after the fix.
   172	
   173	17. Audit finding 13, P2, is fixed by collecting every nearby SHA and state associated with each PR occurrence. Association stays within that occurrence's line and context and stops before the next PR occurrence. Each assertion is compared independently. A matching head does not suppress a conflicting live state.
   174	
   175	    `tests/unit/test_plan_check.py::test_drift_checks_every_sha_and_state_for_each_pr_occurrence` includes `#77 abc1234 merged` with a matching live head and live state OPEN and expects the merged-versus-OPEN finding. It also covers multiple nearby SHAs and repeated PR occurrences with distinct assertions. It is red against `9da0ed3` and green after the fix.
   176	
   177	18. Audit finding 14, P2, is fixed by recognizing nonempty quoted values immediately after `ANTHROPIC_OAUTH_TOKEN=`. Single-quoted, double-quoted and unquoted nonempty assignments produce invariant findings.
   178	
   179	    `tests/unit/test_plan_check.py::test_invariants_reject_nonempty_quoted_oauth_token_assignments` constructs harmless fixture values at runtime and checks both quote forms and the existing unquoted case. Empty assignments remain distinct from nonempty values, and diagnostics contain no assigned value. The quoted cases are red against `9da0ed3` and green after the fix.
   180	
   181	19. Audit finding 15, P2, is fixed by assigning the C12 remedy to this task through item 10. The advisory owner does not need a future amendment to acquire the checker or its test module for this finding. The other inherited findings fixed above are also superseded by this reset's ownership.
   182	
   183	    The orchestrator records the corrected ownership in the lineage's acceptance records and withdraws the corresponding remedy from `dotfiles-T133-task-generator-plan-check-followup-a01`. The worker reports the finding, item 10's selector and its actual fix commit. `tests/unit/test_task_consistency_c11_c15.py::test_c12_classifies_concrete_glob_matches_before_the_glob_spelling` supplies the red-then-green implementation proof. A read-only record assertion contrasts the old assignment requiring an amendment with the corrected assignment to a02 and its fix evidence. The worker does not edit the canonical owner task or acceptance records.
   184	
   185	20. The checker's own hardening, found by the regime job's review of PR #418 (a008, 21:37:56Z) and assigned here: C10 passes every backticked literal to `git grep` as a pattern operand after `-e` (or as a positional after `--`), never as a bare argument that `git grep` can parse as an option, so a literal such as `--open-files-in-pager=CMD` searches for that text and runs nothing; every path the checker opens or passes to a subprocess (C6's design path included) is resolved and confined to the checkout root given by `--root`, and a path outside it is a finding, not a read. `tests/unit/test_task_consistency_c11_c15.py::test_c10_never_passes_a_literal_as_a_git_grep_option` (a fixture task whose backticked literal is `--open-files-in-pager=<marker command>`: the marker is never written and C10 reports the literal as unmatched) and `::test_c6_confines_design_paths_to_the_checkout` are written first and red against 9da0ed3.
   186	
   187	## Out of scope
   188	
   189	`reset-task.sh` remains the later C-69 item. `scripts/orchestrator/dispatch.sh`, including `--next`, the trusted-SHA argument and warning forwarding, remains in the P1-5 to P1-6 dispatch lineage identified in item 8. The regime CI job and validate wiring remain P1-11. `ruleset-request.sh`, `ruleset-verify.sh` and permission-policy changes remain P1-14.
   190	
   191	Plan files, progress records, canonical predecessor tasks, acceptance records and advisory-owner task files remain outside the worker's edit boundary. The orchestrator performs the reset, disposition and ownership bookkeeping named above. Plan-check reports violations without repairing those records.
   192	
   193	## Check
   194	
   195	`.orchestration/dotfiles-T133-task-generator-plan-check-a02/validation.md` contains commands, verbatim stdout and stderr, exit statuses and tested revisions for `make unit-test`, `make format` and `uv run python -m unittest tests.unit.test_task_from_plan tests.unit.test_plan_check tests.unit.test_task_consistency_c11_c15 tests.unit.test_task_checkers -v`. The four task modules are green. An inherited full-suite or formatting failure is reproduced against the unchanged base in the same sandbox and recorded as a failure with that comparison. It is not labelled green or repaired outside `allowed_files`. Final-head GitHub Actions checks pass before RESULT.
   196	
   197	The checker run is `uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py .orchestration/tasks/dotfiles-T133-*.md`. Its complete output and exit status are pasted in validation. C1 to C15 and C7b are accounted for separately from warnings. Without `--premises-sha`, C14 is recorded as not run with its warning. Authorized premise reruns use the orchestrator's trusted dispatched hash and paste their results. Acceptance does not authorize branch commands by calculating a replacement trusted hash from a branch copy. Stale historical premises are reported with their tested root and revision.
   198	
   199	The plan checker runs once as `uv run --no-project --with pyyaml python -I scripts/orchestrator/plan-check.py`. Its output and exit status are pasted in validation. Violations in the real plan group are reported and left for the orchestrator. The dedicated fixture tests exercise `--drift` and `--invariants` without live GitHub.
   200	
   201	Each audit item has the named regression or record check and red-then-green evidence. New regressions execute their current test source against production code at `9da0ed3fe67fd1f9267c56fcdcb7e5aaaaa9ffab` before the corresponding fix, then pass on the final implementation. The retained C14 gate uses the pre-gate revision named in item 7 for its red proof. Record checks identify the exact before and after record text. Each proof records the production revision, regression-source hash, command, output and exit status. A missing test, import error, unavailable runner or zero-test run does not establish a red regression.
   202	
   203	`git diff --numstat origin/main...HEAD` shows at most 700 changed lines outside `tests/` and `.orchestration/`, and at most 800 changed lines under `tests/`. Changed lines are additions plus deletions, including fixtures and the bundled template. `measure.md` and RESULT record both totals and the final changed-file inventory. The totals cover the whole PR, including inherited a01 changes.
   204	
   205	The orchestrator checks the canonical a02 text before dispatch and checks the task-copy replacement and byte identity at acceptance. Local Bats tests do not run. GitHub Actions supplies any required Bats result.
   206	
   207	## Completion
   208	
   209	One branch, `tools/task-generator-plan-check-a01`, continues PR #417 from `9da0ed3fe67fd1f9267c56fcdcb7e5aaaaa9ffab`. The worker's first push contains the predecessor task-copy deletion and this text's byte-identical a02 copy. No second implementation branch or PR is created.
   210	
   211	The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies with this task's scope, caps, reset branch and explicit review restrictions. `dotfiles-T133-task-generator-plan-check-followup-a01` owns new advisory P2 findings after the inherited findings assigned above are removed from its ownership. The orchestrator writes any required owner update before recording that disposition.
   212	
   213	RESULT carries `task_copy=<sha256 of .orchestration/dotfiles-T133-task-generator-plan-check-a02/task.md>`. It carries `precheck=<the precheck evidence hash>` when PR #411 has merged and the applicable precheck has run; otherwise it carries `precheck=pending-411`. It also names the final head, base, branch, changed files, named tests, caps, feedback dispositions and evidence paths. The report explicitly identifies the dispatch SHA wiring and warning-forwarding work owned outside this task.
   214	
   215	The worker's own pre-push review has at most one correction round. A P0 or P1 surviving that round appears in RESULT as open and goes to the orchestrator for the operator's decision. An inherited Bot P0/P1 receives its actual root-cause disposition or remains open. A surviving thread is reported as `open:<thread id>`, and a review-body finding as `open:review-<review id>`. No further worker correction round is hidden before RESULT. Every worker-side round counts toward INV-6, and the a01 stopped history and amendment accounting remain recorded.
   216	
   217	A Codex seat writes evidence at the same relative paths in its own worktree and states that location in RESULT. Worker review evidence uses the required `-worker-` infix. The orchestrator copies worktree evidence by absolute path before review. Evidence distinguishes inherited observations, new red proofs and final-head green results.
   218	
   219	This task is `security: true`. The orchestrator runs the task-level audit and a separate security-profile review on the final head. Final-head CI, the complete feedback sweep, finding dispositions, acceptance record and gate follow Orchestrator Playbook step 10 in its prescribed order. Changed heads receive the required fresh evidence. The orchestrator runs `make require-crit-review` with the required review evidence before completion and uses the integration evidence required by step 10 before merging.
   220	
   221	No `@codex review` comment is posted. Automatic reviews are observed for the inherited bounded window, and absence after 15 minutes is recorded as `bot: none`. Every `gh` command and every Git write runs as an individual command without shell chaining or a wrapper combining writes. A classifier or permission denial produces a blocked PONG with the exact command and output. An alternate command or API does not bypass the denial.
   222	
   223	Until P1-14 lands, any string containing the words `gh pr merge` or `gh pr create` is written with the file-edit tool, never in a Bash heredoc or `echo`.
   224	
   225	## Amendment 1 (CI-repair round, 2026-10-19T03:4xZ): the regime fixtures under C13
   226	
   227	The chain update-branched PR #417 onto main b22a5580 (→ 63b6acae) and the four `test` jobs fail on three regime tests: `test_regime_ci_checks_only_the_latest_copy_of_a_reset_of_lineage` ("C13 disposition is not closed:, residual: or out-of-scope: and a space"), `test_regime_ci_reads_the_head_as_data_and_runs_the_base_verifier` and `test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr` (run 39195158133). The regime fixtures (tests/unit/test_regime_ci.py, landed by PR #418) carry threat-row dispositions in the pre-C13 form, and the regime verifier runs this task's checker on them. `tests/unit/test_regime_ci.py` joins allowed_files for the fixture repair only: the fixture dispositions take the C13 grammar (`residual: <sentence>` and so on) and the expected output counts follow; no production file changes. Under C-61 a fixture-only CI repair with no production change is one CI-repair round. Everything else stands.
   228	
   229	## Checks (pasted by the orchestrator before each send)
   230	
   231	```
   232	dotfiles-T133-task-generator-plan-check-a02.md: OK
   233	premises 1 to 5: copied from a01 verbatim (write-time outputs of 2026-10-18 18:0x JST; premise 5 is stale since PR #413 merged at 10:46Z, a C14 finding at acceptance)
   234	masked 0 match(es) in .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a02.md
   235	```
   236	
   237	Local Bats runs and live deployment remain outside this task.
   238	Plan commands execute with the orchestrator sandbox's permissions.     1	---
     2	{
     3	  "audit_findings": [],
     4	  "dispatch": [
     5	    "AGMSG-TASK v1 task_id=dotfiles-T133-task-generator-plan-check-a02 round=1 reset_of=dotfiles-T133-task-generator-plan-check-a01 repo=~/Workspace/dotfiles/.claude/worktrees/worker-c task_file=.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a02.md task_sha256=a3ab8ea6addda207fa9a9ff5d96921e080dab7a1025117f33cbd087e6b805f98 deadline=none done_signal=AGMSG-RESULT note=a009:INV-6-reset-of-a01(the-fifteen-audit-findings-as-items,the-bundled-template,the-C14-sha-gate,item-20-the-checker-hardening)"
     6	  ],
     7	  "format": 1,
     8	  "head": "8a09b9365932f23b09df8aa2385a93d0b3016a3e",
     9	  "ledger": [
    10	    {
    11	      "class": "evidence-integrity",
    12	      "id": "audit:9da0ed3:1"
    13	    },
    14	    {
    15	      "class": "threat-row-stale",
    16	      "id": "audit:9da0ed3:2"
    17	    },
    18	    {
    19	      "class": "replan-not-patch",
    20	      "id": "audit:9da0ed3:3"
    21	    },
    22	    {
    23	      "class": "dispatch-wiring",
    24	      "id": "audit:9da0ed3:4"
    25	    },
    26	    {
    27	      "class": "spec-gap",
    28	      "id": "audit:9da0ed3:5"
    29	    },
    30	    {
    31	      "class": "glob-classification",
    32	      "id": "audit:9da0ed3:6"
    33	    },
    34	    {
    35	      "class": "glob-intersection",
    36	      "id": "audit:9da0ed3:7"
    37	    },
    38	    {
    39	      "class": "substring-selection",
    40	      "id": "audit:9da0ed3:8"
    41	    },
    42	    {
    43	      "class": "glob-filter",
    44	      "id": "audit:9da0ed3:9"
    45	    },
    46	    {
    47	      "class": "parser-gap",
    48	      "id": "audit:9da0ed3:10"
    49	    },
    50	    {
    51	      "class": "parser-gap",
    52	      "id": "audit:9da0ed3:11"
    53	    },
    54	    {
    55	      "class": "parser-gap",
    56	      "id": "audit:9da0ed3:12"
    57	    },
    58	    {
    59	      "class": "parser-gap",
    60	      "id": "audit:9da0ed3:13"
    61	    },
    62	    {
    63	      "class": "regex-gap",
    64	      "id": "audit:9da0ed3:14"
    65	    },
    66	    {
    67	      "class": "records-form",
    68	      "id": "audit:9da0ed3:15"
    69	    },
    70	    {
    71	      "class": "trust-boundary-pr-input",
    72	      "id": "4306960622"
    73	    },
    74	    {
    75	      "class": "missing-input-crash",
    76	      "id": "4306960626"
    77	    },
    78	    {
    79	      "class": "string-form-comparison",
    80	      "id": "4306960630"
    81	    }
    82	  ],
    83	  "pr": 417,
    84	  "replans": {},
    85	  "searches": [
    86	    {
    87	      "class": "parser-gap",
    88	      "records": []
    89	    }
    90	  ],
    91	  "task": "dotfiles-T133-task-generator-plan-check-a02"
    92	}
    93	---
    94	
    95	# Acceptance record: dotfiles-T133-task-generator-plan-check-a02
    96	
    97	Plan 024 P1-12, the INV-6 reset of `dotfiles-T133-task-generator-plan-check-a01` (two amendments by substance, M-20261018-15; the audit of 9da0ed3: 3 P1 and 12 P2, folded in as items 5 to 19). Redesigned by a review-profile context (`.agents/worklog/orchestrator-glue/redesign/p112-a02.md`, prompt `p112-a02-redesign-prompt.md`); the orchestrator added item 20 (the checker hardening PR #418's review pointed here: C10 literals as `git grep -e` operands, C6 paths confined to the checkout) and the stale-premise note before the send. Seat a009 (worker-c, Claude) continues PR #417 from 9da0ed3. Owner of advisory P2: `dotfiles-T133-task-generator-plan-check-followup-a01` (written 21:0xZ).
    98	
    99	- 2026-10-18T21:4xZ: task text installed, `task-consistency-check.py … : OK`, home-path scan 0 matches, dispatched to a009 (the line above; the full note is in the bus history). Known stale premise 5 (test_task_checkers.py "in flight in PR #413"): #413 merged at 10:46Z; a C14 finding at acceptance, records-form.
   100	- 2026-10-19T00:08:22Z: RESULT round 1 from a009: PR #417 head 3f12e603118b8bb1acc9005f5befcdb5b9cbd2b7 (code head 6e07d291, continued from 9da0ed3) on 3e41e36a; `task_copy=a3ab8ea6…` (the dispatched sha); first push 6da92853 (the a01 copy deleted, the a02 copy added); the three Bot threads fixed (538e60bd, eb20d063); audit items 5 to 19 fixed at eb20d063 (item 19's C12 remedy owned here) and item 20 (C10 `-e` operands, C6 confinement); one self-review round (2 P2 + 4 P3, fixed 6e07d291); 15 new or updated end-to-end tests red on 9da0ed3 by exact id; four modules 28 OK; unit baseline identical to 3e41e36a; the checker passes 29 T133 files with the C14 not-run warning ×20; plan-check exit 1 with six violations left for the orchestrator (F3 ×2, F4, F6 ×3); caps 659/700 and 657/800; dispatch.sh:238 needs `--premises-sha` (the P1-5/P1-6 lineage); INV-6 0/0/0. `status=pending-integration` sent 00:1xZ; the chain is queued after #411 and #420.
   101	
   102	## Owned by dotfiles-T133-task-generator-plan-check-followup-a01
   103	
   104	- `checker:C17` residual-sentence-vs-allowed-files: a threat row whose disposition claims "no <kind> file is in allowed_files" (workflow, interpreter, script) is verified by task-consistency-check.py against the front matter; PR #421 shipped a false residual (Bot P1 4309302616, local P2) copied from the narrow owner template after the task was widened to three workflow files.
   105	- `checker:C19` inherited-caps: a task text that applies another task's Check or Completion clause by reference restates its own comparison range and caps; task-consistency-check.py resolves the reference and fails a text whose caps are only inherited (PR #423 audit:9d13a06:2: the a01 amendment's 741e242...HEAD 60/120 caps were imported into a02 and measured 1,025/1,997 there).
   106	- 2026-10-19T03:41Z: the chain update-branched #417 onto b22a5580 (→ 63b6acae); the four `test` jobs fail on three regime tests (run 39195158133): the #418 fixtures in tests/unit/test_regime_ci.py carry pre-C13 threat-row dispositions and the regime verifier runs this task's checker on them ("C13 disposition is not closed:, residual: or out-of-scope: and a space"); a semantic conflict between two merged lineages, not a defect of either alone. Counters: tasks=1 amendments=0 results=1 revises=0. Decision: amendment 1 (fixture repair only; tests/unit/test_regime_ci.py joins allowed_files with its row; C-61: one CI-repair round) dispatched to a009 03:4xZ (sha 60d4c2db…, previous a3ab8ea6…). Root cause: the checker vocabulary changed in one lineage while another lineage's fixtures were written against the old grammar; nothing runs the full suite of main-plus-PR before the update-branch (the chain's CI does, which is where it surfaced).
   107	- 2026-10-19T04:03:46Z: CI-repair-1 RESULT from a009: PR #417 head 8a09b936 (code head eb0b1c06, previous 63b6acae) on b22a5580; `task_copy=60d4c2db…` (amendment 1); repair in tests/unit/test_regime_ci.py only (the five fixture threat rows take the C13 grammar); regime tests red on 63b6acae, 101 tests green on eb0b1c06; CI 11/11; Bot none in 15 min; caps 659/700 and 673/800. `status=pending-integration` sent 04:0xZ; the chain re-runs after #424.
   108	local:8a09b93:1	advisory-p2
   109	local-finding: 8a09b93:1 not-applicable:advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (- [P2] Classify agent instruction files as applied files — scripts/orchestrator/task-consistency-check.py:63-65); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-task-generator-plan-check-followup-a01.md (27d121f5bc4d7ae7d41100e35b8ab026b9d018493eaae601ca5176a72252befb)
   110	local:8a09b93:2	advisory-p2
   111	local-finding: 8a09b93:2 not-applicable:advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (- [P2] Handle nested directory scopes before invoking C7b — scripts/orchestrator/task-from-plan.py:153-153); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-task-generator-plan-check-followup-a01.md (27d121f5bc4d7ae7d41100e35b8ab026b9d018493eaae601ca5176a72252befb)
   112	local:8a09b93:3	advisory-p2
   113	local-finding: 8a09b93:3 not-applicable:advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (- [P2] Include repository-root files in the generated edit scope — scripts/orchestrator/task-from-plan.py:137-137); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-task-generator-plan-check-followup-a01.md (27d121f5bc4d7ae7d41100e35b8ab026b9d018493eaae601ca5176a72252befb)
   114	local:8a09b93:4	advisory-p2
   115	local-finding: 8a09b93:4 not-applicable:advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (- [P2] Normalize extracted paths before emitting allowed_files — scripts/orchestrator/task-from-plan.py:138-143); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-task-generator-plan-check-followup-a01.md (27d121f5bc4d7ae7d41100e35b8ab026b9d018493eaae601ca5176a72252befb)
   116	local:8a09b93:5	advisory-p2
   117	local-finding: 8a09b93:5 not-applicable:advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (- [P2] Use a threat-row selector accepted by C11 — .orchestration/dotfiles-T133-task-generator-plan-check-a02/task.md:37); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-task-generator-plan-check-followup-a01.md (27d121f5bc4d7ae7d41100e35b8ab026b9d018493eaae601ca5176a72252befb)
   118	
   119	## Lineage ledger rows for the audit of 9da0ed3 (the a01 head; the a01 stopped at S2 and the a02 reset absorbed the fifteen findings as its items, all reported fixed in the a02 RESULT 00:08Z; the a01 record carries no rows because the task was withdrawn before disposition; the record step writes no lineage rows, the P1-6 item)
   120	
   121	audit:9da0ed3:1	evidence-integrity
   122	audit:9da0ed3:2	threat-row-stale
   123	audit:9da0ed3:3	replan-not-patch
   124	audit:9da0ed3:4	dispatch-wiring
   125	audit:9da0ed3:5	spec-gap
   126	audit:9da0ed3:6	glob-classification
   127	audit:9da0ed3:7	glob-intersection
   128	audit:9da0ed3:8	substring-selection
   129	audit:9da0ed3:9	glob-filter
   130	audit:9da0ed3:10	parser-gap
   131	audit:9da0ed3:11	parser-gap
   132	audit:9da0ed3:12	parser-gap
   133	audit:9da0ed3:13	parser-gap
   134	audit:9da0ed3:14	regex-gap
   135	audit:9da0ed3:15	records-form
   136	
   137	## Bot-thread ledger rows carried from the a01 record (PR #417 round 1 and revise 1 of the a01; fixed:b3c6b7ea and fixed:538e60bd, in 417-extra.tsv; the record step writes no Bot rows)
   138	
   139	4306960622	trust-boundary-pr-input
   140	4306960626	missing-input-crash
   141	4306960630	string-form-comparison

 exited 1 in 420ms:
error connecting to api.github.com
check your internet connection or https://githubstatus.com

**Optimizing command output size**
exec
/bin/zsh -lc "sed -n '217,250p' ~/.agents/skills/agmsg-orchestration/SKILL.md && gh pr view 417 --repo mryfmo/dotfiles --json url,title,headRefOid,baseRefName,state,statusCheckRollup" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 exited 1 in 132ms:
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

error connecting to api.github.com
check your internet connection or https://githubstatus.com

exec
/bin/zsh -lc "git diff --name-status b22a5580d0778e57a66d3f75c76e3c55b88701e1 8a09b9365932f23b09df8aa2385a93d0b3016a3e && nl -ba .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a02.md | sed -n '1,145p'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 7ms:
A	.orchestration/dotfiles-T133-task-generator-plan-check-a01/learning.md
A	.orchestration/dotfiles-T133-task-generator-plan-check-a01/report.md
A	.orchestration/dotfiles-T133-task-generator-plan-check-a01/revise.yaml
A	.orchestration/dotfiles-T133-task-generator-plan-check-a01/sandbox.md
A	.orchestration/dotfiles-T133-task-generator-plan-check-a01/validation.md
A	.orchestration/dotfiles-T133-task-generator-plan-check-a02/dotfiles-T133-task-generator-plan-check-a02-worker-crit.json
A	.orchestration/dotfiles-T133-task-generator-plan-check-a02/dotfiles-T133-task-generator-plan-check-a02-worker-review-receipt.md
A	.orchestration/dotfiles-T133-task-generator-plan-check-a02/learning.md
A	.orchestration/dotfiles-T133-task-generator-plan-check-a02/measure.md
A	.orchestration/dotfiles-T133-task-generator-plan-check-a02/report.md
A	.orchestration/dotfiles-T133-task-generator-plan-check-a02/sandbox.md
A	.orchestration/dotfiles-T133-task-generator-plan-check-a02/task.md
A	.orchestration/dotfiles-T133-task-generator-plan-check-a02/validation.md
A	scripts/orchestrator/plan-check.py
M	scripts/orchestrator/task-consistency-check.py
A	scripts/orchestrator/task-from-plan.py
A	scripts/orchestrator/task-template.md
A	tests/unit/test_plan_check.py
M	tests/unit/test_regime_ci.py
M	tests/unit/test_task_checkers.py
A	tests/unit/test_task_consistency_c11_c15.py
A	tests/unit/test_task_from_plan.py
     1	---
     2	format: 2
     3	task_id: dotfiles-T133-task-generator-plan-check-a02
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
    16	  - .orchestration/dotfiles-T133-task-generator-plan-check-a02/**
    17	after: []
    18	reset_of: [dotfiles-T133-task-generator-plan-check-a01]
    19	threat_table:
    20	  - control: "scripts/orchestrator/task-from-plan.py (generation from the committed plan group, bundled template, command outputs and scratch-worktree checks)"
    21	    disposition: "residual: the generator executes the orchestrator's committed plan commands in the orchestrator's sandbox after the clean-plan check; the generator regressions and final-head security review assess this execution boundary."
    22	  - control: "scripts/orchestrator/plan-check.py (form, concrete scope intersections, timestamped drift and forbidden patterns)"
    23	    disposition: "closed: tests/unit/test_plan_check.py::test_plan_check_reports_each_form_drift_and_invariant_violation_once_and_passes_a_clean_plan"
    24	  - control: "scripts/orchestrator/task-consistency-check.py (C11 to C15, concrete glob matches, trusted premise execution and assigned invariant ids); item 20: C10 literals as git grep -e operands and C6 paths confined to the checkout)"
    25	    disposition: "residual: the checker executes premise commands only for bytes matching the caller's trusted SHA256; the dedicated regressions cover that gate, warnings, wildcard coverage and invariant completeness."
    26	  - control: "scripts/orchestrator/task-template.md (the bundled task rows, Check defaults and Completion wording)"
    27	    disposition: "closed: tests/unit/test_task_from_plan.py::test_generator_uses_the_bundled_template_without_task_records"
    28	  - control: "tests/unit/test_task_from_plan.py (temporary committed plan groups, real local Git repositories and isolated command fixtures)"
    29	    disposition: "residual: fixtures execute controlled commands in temporary repositories and verify output provenance, refusal before execution, generated scope and scratch-worktree cleanup."
    30	  - control: "tests/unit/test_plan_check.py (temporary plan groups, concrete tree paths, acceptance events and a stub gh)"
    31	    disposition: "residual: fixtures use temporary repositories and a stub gh placed first inside the uv invocation; no fixture contacts live GitHub."
    32	  - control: "tests/unit/test_task_consistency_c11_c15.py (shape, wildcard, SHA, warning and invariant regressions)"
    33	    disposition: "residual: temporary task files and repositories isolate premise side effects; explicit trusted hashes authorize only the fixture bytes under test."
    34	  - control: "tests/unit/test_task_checkers.py (amendment 1's C4 fixture disposition and historical expected-set edits)"
    35	    disposition: "residual: only the two amendment-1 edits remain against origin/main; report.md justifies every added historical check id and the audit compares the module's complete diff."
    36	  - control: "tests/unit/test_regime_ci.py (amendment 1: the regime fixtures' threat-row dispositions gain the C13 grammar; no production change)"
    37	    disposition: "closed: tests/unit/test_regime_ci.py::RegimeCiTest::test_regime_ci_checks_only_the_latest_copy_of_a_reset_of_lineage"
    38	  - control: ".orchestration/dotfiles-T133-task-generator-plan-check-a02/** (the reset task's branch artifacts)"
    39	    disposition: "residual: artifacts stay in this task's directory, distinguish historical observations from final-head results and identify commands, tested revisions and evidence hashes."
    40	  - control: "the task-file copy on the branch (.orchestration/dotfiles-T133-task-generator-plan-check-a02/task.md) replaces the reset_of task's copy (.orchestration/dotfiles-T133-task-generator-plan-check-a01/task.md)"
    41	    disposition: "residual: the worker's first push deletes the named predecessor copy and adds the byte-identical dispatched a02 text; the a02 copy's own SHA256 appears in TASK and RESULT and is compared at acceptance."
    42	  - control: "the branch evidence records under .orchestration/dotfiles-T133-task-generator-plan-check-a02/ (report.md, validation.md, sandbox.md, learning.md, measure.md and authorized revise evidence)"
    43	    disposition: "residual: records preserve command outputs, exits, production revisions and regression-source hashes; the final-head audit checks claims against the implementation, records and CI."
    44	  - control: task metadata
    45	    disposition: "residual: PyYAML reads the front matter and the consistency checker validates its cross-field rules before dispatch and at acceptance; the dispatched-file comparison covers subsequent changes."
    46	  - control: metadata separators
    47	    disposition: "residual: the first document separators bound the YAML front matter and the byte comparison covers the complete dispatched task copy."
    48	  - control: in-process effects
    49	    disposition: "residual: task-from-plan.py executes the plan's backticked commands, which are the orchestrator's own text, in the orchestrator's sandbox; it refuses execution when git status of the 024-* plan group is not clean and executes commands read from the committed revision. It writes the named task file and creates and removes a scratch worktree for Check commands. C14 executes a premise command only when --premises-sha equals the SHA256 of the same file bytes from which that command was parsed. plan-check writes no files."
    50	  - control: workflow and interpreter or environment inputs
    51	    disposition: "residual: no workflow changes; scripts use the existing uv and PyYAML invocation with python -I, premise reruns use bash with pipefail and the specified PATH, and plan-check uses read-only gh and git calls."
    52	  - control: new or renamed scripts
    53	    disposition: "residual: the inherited two new Python scripts and one new bundled Markdown template are the complete new production-file inventory; the audit checks the final inventory against allowed_files."
    54	  - control: orchestrator effect merge
    55	    disposition: "residual: the orchestrator merges through gh pr merge --squash --match-head-commit <audited head> after Orchestrator Playbook step 10; the worker has no merge assignment."
    56	  - control: orchestrator effect update-branch
    57	    disposition: "residual: gh pr update-branch changes the head, so the required CI, feedback sweep, audit and security-review evidence bind the resulting final head before the gate."
    58	  - control: orchestrator effect forced worker removal
    59	    disposition: "residual: no forced removal is planned; any forced removal follows the existing dirty-worktree rule and records discarded uncommitted state in the acceptance record."
    60	premises:
    61	  - claim: none of the five new files exists on origin/main
    62	    command: git ls-files scripts/orchestrator/task-from-plan.py scripts/orchestrator/plan-check.py tests/unit/test_task_from_plan.py tests/unit/test_plan_check.py tests/unit/test_task_consistency_c11_c15.py | wc -l
    63	    output: |-
    64	      0
    65	  - claim: the checker documents eleven checks today (C1 to C10 and C7b), so C11 to C15 are additions at the end of its list
    66	    command: /usr/bin/grep -c '^C[0-9]*b\? ' scripts/orchestrator/task-consistency-check.py
    67	    output: |-
    68	      11
    69	  - claim: the plan 024 group is eleven files (ten Markdown documents and the progress TSV), the set plan-check reads
    70	    command: /bin/ls .orchestration/plans/024-*.md .orchestration/plans/024-progress.tsv | wc -l
    71	    output: |-
    72	      11
    73	  - claim: the todo table has fifteen P1 rows, the rows task-from-plan reads
    74	    command: /usr/bin/grep -c '^| P1-' .orchestration/plans/024-todo.md
    75	    output: |-
    76	      15
    77	  - claim: tests/unit/test_task_checkers.py is in flight in PR #413, so the new checks get their own test module
    78	    command: git ls-files tests/unit/test_task_checkers.py | wc -l
    79	    output: |-
    80	      1
    81	---
    82	
    83	# AGMSG-TASK dotfiles-T133-task-generator-plan-check-a02 — INV-6 reset of dotfiles-T133-task-generator-plan-check-a01 (plan 006 S2; plan 024 P1-12)
    84	
    85	This text is the independent redesign by a review-profile context other than the author of a01. Amendment 1 and the C14 specification change sent as a revise constitute two amendments. Plan 006 INV-6 S2 stopped a01. The task-level audit of `9da0ed3fe67fd1f9267c56fcdcb7e5aaaaa9ffab` returned `incorrect` with three P1 and twelve P2. Files items 5 to 19 disposition those fifteen findings through fixes, regression checks and corrected ownership.
    86	
    87	PR #417 continues on the same branch, `tools/task-generator-plan-check-a01`, from `9da0ed3fe67fd1f9267c56fcdcb7e5aaaaa9ffab`. The worker's first push deletes `.orchestration/dotfiles-T133-task-generator-plan-check-a01/task.md` and adds this dispatched text's byte-identical copy at `.orchestration/dotfiles-T133-task-generator-plan-check-a02/task.md`. The orchestrator directs that exact predecessor-copy deletion as reset bookkeeping outside `allowed_files`. Every other worker edit stays within `allowed_files`. One branch and one implementation PR carry this reset.
    88	
    89	The a01 task, acceptance history, reports and counters remain historical evidence. Its C14 revise remains recorded as an amendment in substance. The five premises above preserve a01's write-time observations verbatim. Fresh validation records the repository and revision actually checked and identifies any premise that has since drifted.
    90	
    91	## Goal
    92	
    93	The generator produces a format-2 task skeleton from one plan todo row using a bundled template, proposed file scope and actual command outputs. The consistency checker validates disposition shapes, concrete wildcard coverage, trusted premise reruns and complete invariant assignments. The plan checker reports form, drift and forbidden-pattern violations without changing the plan.
    94	
    95	## Files
    96	
    97	1. `scripts/orchestrator/task-from-plan.py <todo-id> [--out .orchestration/tasks/<id>.md] [--seat <identity>] [--worktree <path>]` retains the existing Python, standard-library and PyYAML implementation. It reads the exact todo row from `.orchestration/plans/024-todo.md`, the numbered program items that row names in `024-design-programs.md`, the quality row in `024-design-quality.md` and the matching section-6 wave row in `024-omp-cutover-and-corrective-order.md`.
    98	
    99	   `scripts/orchestrator/task-template.md` supplies the task-copy, evidence, non-path and orchestrator-effect rows, default Check commands and complete Completion wording. The template is located beside the generator. The generator reads no file under `.orchestration/tasks/`. The former sibling-task Check lookup, row-template lookup and Completion-record dependency are replaced by bundled content. Program-specific Check commands come from the committed program items, and bundled defaults supply the common checks.
   100	
   101	   The generated front matter carries `format: 2`, the output filename's task id, `kind: code`, the quality row's security classification, `after: []`, premises and threat rows. Proposed `allowed_files` preserve paths and wildcard scopes named by the row and its program items, add relevant `git grep -l -F` hits and include the task's evidence directory. Files contains each proposal's `# from: <grep hit>` provenance. The threat table contains one draft row per allowed entry, concrete rows required by C12 and the bundled control rows with the generated task id substituted.
   102	
   103	   The generator executes the orchestrator's backticked plan commands in the orchestrator's sandbox after item 6's clean-plan gate. Each premise records its actual stdout and exit status; a failed command remains a `verify:` claim with that status. Network commands retained without execution carry an explicit `verify:` not-run explanation. They carry no invented exit status. Check commands run once in a detached scratch worktree of `origin/main`; their output and exit status appear in the generated Check section with their tested revision. Cleanup uses `git worktree remove --force` and removes the temporary parent directory.
   104	
   105	   The body contains Goal, Files, Out of scope, Check, Completion and the dispatch Checks block. The generator writes the named output and passes it to the consistency checker with the SHA256 of its own generated bytes. It prints the checker's findings and warnings and exits 0 when its applicable checks pass, 1 otherwise. A generated file with findings remains available for editing. The bundled Completion wording retains the inherited contract with `<id>-followup-a01` as advisory owner and the generated task's own copy hash in RESULT.
   106	
   107	2. `scripts/orchestrator/task-consistency-check.py` retains C1 to C10 and C7b unchanged and documents C11 to C15 after C10. C11 requires a `closed:` payload shaped as `tests/<path>::<identifier>`, an `out-of-scope:` payload naming an existing `.orchestration/tasks/<id>.md`, and a `residual:` payload of at least 20 characters. C12 examines concrete glob matches and requires a row for each executed or applied file, with the existing exemptions for `tests/fixtures/` and the task's own evidence directory. C13 requires exactly one of `closed: `, `residual: ` or `out-of-scope: `.
   108	
   109	   C14 executes premise commands only when `--premises-sha <sha256>` equals the SHA256 of the file bytes being checked. The hash and parsed commands come from the same read. The caller supplies the trusted dispatched hash. Acceptance of a branch copy supplies no trusted hash. A missing or mismatching hash executes no premise command and prints `C14: not run (no trusted sha)` as an explicit warning. A no-sha structural pass does not establish that premises passed.
   110	
   111	   An authorized C14 rerun uses the repository root, `bash -c`, `set -o pipefail`, PATH `<root>/bin:/usr/bin:/bin` and the retained HOME value. Output comparison collapses whitespace runs as amendment 1 specified. Commands naming `gh`, `curl` or a URL produce `C14 skipped network premise`. A tool absent from the mandated PATH produces `C14: tool absent <name>`, including absence within a pipeline. These cases remain visible warnings or skip notes. An actual output mismatch remains a C14 finding.
   112	
   113	   C15 reads the named design from `origin/main`. It compares the task's invariant id set with the design's assignment to that task in `implementing_tasks` and compares each assigned sentence byte for byte. An omitted or empty task invariant map cannot bypass an existing assignment. Missing assigned ids, extra ids and changed sentences produce C15 findings. A missing named design produces a finding. A design task carrying its own definitions retains its existing treatment. Findings keep the existing indented stdout format, and warnings and skip notes remain visible on stderr.
   114	
   115	3. `scripts/orchestrator/plan-check.py [--root <repo>] [--drift] [--invariants]` retains the eleven-file plan-024 scope and one violation per line. F1 requires every todo row's completion column. F2 compares simultaneous tasks' concrete allowed scopes once their task files exist. F3 requires each P1 row to name a bottleneck id present in mechanism 5.0 or quality 5.10. F4 requires each checklist DoD row to contain a backtick command or explicit file path. F5 requires each section-2 decision row's bold default. F6 checks task and decision references locally and PR existence through read-only `gh` when `--drift` is requested.
   116	
   117	   Drift checks compare every nearby cited PR head and state with `gh pr view <pr> --json headRefOid,mergeStateStatus,isDraft,state`. Progress rows naming a task are compared with that task's latest timestamped acceptance event. Differences retain `drift: <file>:<line> <cited> != <live>`. Invariant checks cover nonempty `ANTHROPIC_OAUTH_TOKEN` assignments, direct main pushes, prohibited merge flags and added `claude.permissions.ask` entries against `origin/main`. The script writes no records, exits 1 on a violation and exits 0 otherwise. CI wiring remains P1-11's work.
   118	
   119	4. The three dedicated modules retain the original end-to-end and per-rule tests. `tests/unit/test_task_from_plan.py::test_a_generated_task_passes_the_consistency_check_and_pastes_real_premise_outputs` exercises real successful and failed commands, provenance, threat rows, bundled content and scratch cleanup. `tests/unit/test_plan_check.py::test_plan_check_reports_each_form_drift_and_invariant_violation_once_and_passes_a_clean_plan` retains one isolated violation per form rule, clean-plan success, stubbed drift and invariant cases. `tests/unit/test_task_consistency_c11_c15.py::test_each_new_check_is_red_on_its_fixture_and_the_existing_checks_are_unchanged` retains the check-specific fixtures, whitespace normalization, absent-tool warnings and historical structural checks.
   120	
   121	   Amendment 1's two edits in `tests/unit/test_task_checkers.py` remain. The C4 path-boundary fixture carries a well-formed disposition. The historical exact expected sets include the justified C11 and C15 findings. No historical fixture executes premises without a trusted hash, and no C14 finding id is added for a no-sha warning. No other part of that module changes. `report.md` explains each expected-set addition. Fixture lines count against the test cap.
   122	
   123	5. Audit finding 1, P1, is fixed by bundling `scripts/orchestrator/task-template.md` and removing every generator input dependency on `.orchestration/tasks/`. A missing records file no longer prevents generation. The prior `fixed:b3c6b7ea` disposition addressed error presentation and did not fix this cause.
   124	
   125	   `tests/unit/test_task_from_plan.py::test_generator_uses_the_bundled_template_without_task_records` uses a committed fixture plan group with no task-record directory and the production bundled template. Generation succeeds, produces the required rows and Check and Completion content, and passes the real checker. The test is red against the generator at `9da0ed3` because that generator requires task records and is green after the dependency removal. The orchestrator supersedes the erroneous missing-template disposition with the actual fix commit and this evidence.
   126	
   127	6. Audit finding 2, P1, is fixed by stating and enforcing the generator's execution contract. Its backticked commands are the orchestrator's own plan text and execute in the orchestrator's sandbox through the existing runner. Before executing any premise or Check command, the generator checks git status for the entire `.orchestration/plans/024-*` group, including staged, unstaged and untracked changes. A dirty group produces an explicit refusal before command execution or output creation. The generator records the resolved committed revision and reads executable command text from that revision, so the executed text equals committed plan text. The in-process-effects row above describes these effects.
   128	
   129	   `tests/unit/test_task_from_plan.py::test_generator_refuses_dirty_plan_commands_before_execution` commits a plan command that writes a temporary marker and exercises unstaged, staged and untracked plan-group changes. Each dirty case refuses generation and leaves the marker absent. The committed clean case runs and records the command's output and revision. The test is red against `9da0ed3` and green after the gate is added.
   130	
   131	7. Audit finding 3, P1, is fixed by making item 2's C14 SHA gate part of this dispatched specification and correcting its amendment accounting. The a01 acceptance record names the C14 revise as the second amendment in substance, records S2 and retains the original history. This reset does not relabel that change as an implementation-only round.
   132	
   133	   `tests/unit/test_task_consistency_c11_c15.py::test_c14_executes_premise_commands_only_for_the_dispatched_sha` retains the marker proof: no hash and a wrong hash execute nothing; the correct dispatched hash executes the premise; changing the file invalidates the old hash; an authorized rerun with mismatching output reports C14. Its red production reference is the pre-gate implementation at `ff4d25a8`, and it runs green on this task's final head. Validation also contains a read-only comparison of the original acceptance decision with its explicit amendment and S2 correction. The orchestrator supplies that record evidence outside the worker's edit boundary.
   134	
   135	8. Audit finding 4, P2, is fixed at the checker interface by making the no-trusted-SHA outcome an explicit warning carrying `C14: not run (no trusted sha)`. The dispatch check's evidence preserves that warning and records C14 as not run. A successful structural exit does not become an unqualified C14 success.
   136	
   137	   The checker invocation presently at `scripts/orchestrator/dispatch.sh:238` is the integration point for `--premises-sha <the TASK line's validated task_sha256>` before `"${tf}"`. That line belongs to P1-6 in the serialized dispatch lineage following `dotfiles-T133-result-precheck-a03`. Its owner also preserves warning output from successful checker calls. This task names the line and its required argument in `report.md` and does not edit `dispatch.sh`. Until that wiring lands, the report and dispatch evidence state the warning and the pending integration.
   138	
   139	   `tests/unit/test_task_consistency_c11_c15.py::test_c14_without_a_trusted_sha_reports_an_explicit_warning` checks the ordinary no-sha invocation, explicit warning severity, the exact not-run message and absence of the premise marker. It is red against `9da0ed3`'s unqualified note and green after the warning contract is implemented. The test does not claim that unchanged dispatch wiring passes a trusted hash.
   140	
   141	9. Audit finding 5, P2, is fixed by comparing assigned invariant ids as well as sentences. C15 obtains the assignment from the design on `origin/main`, including when the task omits `invariants`.
   142	
   143	   `tests/unit/test_task_consistency_c11_c15.py::test_c15_requires_the_design_assigned_invariant_id_set` assigns INV-1 and INV-2, supplies only the correct INV-1 sentence and expects C15. It also covers an absent map, an extra id, a changed sentence and the complete byte-identical assignment. The missing-id case is red against `9da0ed3` and all cases are green after the fix.
   144	
   145	10. Audit finding 6, P2, is fixed by expanding each glob before deciding which matched files require concrete threat rows. A matched `.sh`, `.py`, `.yaml`, `.yml`, `.json` or `.toml` file, or a file under `home/`, `scripts/`, `.githooks/` or `.github/`, receives the executed-or-applied treatment regardless of the glob's spelling. The fixture and own-evidence exemptions remain.

**Managing token budget**
exec
/bin/zsh -lc 'git show 8a09b9365932f23b09df8aa2385a93d0b3016a3e:scripts/orchestrator/task-from-plan.py | nl -ba' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc 'git show 8a09b9365932f23b09df8aa2385a93d0b3016a3e:scripts/orchestrator/plan-check.py | nl -ba' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc "python3 -B -c 'import json,pathlib; m=pathlib.Path(\".ua/meta.json\"); print(m.read_text() if m.exists() else \"meta absent\"); g=pathlib.Path(\".ua/knowledge-graph.json\"); d=json.loads(g.read_text()) if g.exists() else {}; print(\"graph absent\" if not d else \"graph present\"); print(*[{k:n.get(k) for k in (\"id\",\"summary\",\"filePath\")} for n in d.get(\"nodes\",[]) if any(s in str(n).lower() for s in (\"task-from-plan\",\"plan-check\",\"task-consistency\",\"design-invariant\"))],sep=\"\\n\")' && nl -ba .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a02.md | sed -n '141,190p'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 114ms:
     1	"""A format-2 task file from one plan 024 todo row, every premise and Check command run (plan 024 programs (12)).
     2	
     3	`uv run --offline --with pyyaml python -I scripts/orchestrator/task-from-plan.py <todo-id> [--out <task.md>]
     4	[--seat <identity>] [--worktree <path>]` refuses, before it runs or writes anything, while the
     5	.orchestration/plans/024-* group under the current git toplevel has a staged, unstaged or untracked change. Otherwise it
     6	reads, at the committed revision HEAD (named in the task's opening line), the row <todo-id> of
     7	.orchestration/plans/024-todo.md, the items of 024-design-programs.md its work column names by (n) (each through the
     8	next **(<n>) heading or the end of the file), the wave row of the plan's section 6 whose cell (the --seat column's when
     9	given) holds the whole id <todo-id>, and the Q-A row of 024-design-quality.md (security: true when it lists the id or a
    10	range holding it). task-template.md beside this script supplies the control rows, the common Check commands and the
    11	Completion section; no file under .orchestration/tasks/ is read. It writes --out (default
    12	.orchestration/tasks/<todo-id>.md), runs task-consistency-check.py on it with --premises-sha of the written bytes,
    13	prints the checker's output and exits 0 when the checker passes, 1 otherwise (the file stays for editing).
    14	allowed_files: every path or glob scope the row and its items name in backticks (a literal has a file extension or
    15	exists, inside the checkout), every file `git grep -l -F` finds under scripts/ and tests/ for each named script or test
    16	(each listed as `# from: <hit>` in the Files section), and the task's own evidence directory. threat_table: one draft
    17	row per entry (residual: the row's completion), one per executed or applied file a glob entry matches (C12), then the
    18	template's rows with <task_id> replaced.
    19	A backticked span is a command by its form: its first word is a lowercase name, a / or ./ path, or a .sh or .py path,
    20	and it holds no <placeholder>; a lone word is one only when PATH holds it (a lone path is a scope). premises: every
    21	command the items quote but `make`, run once through the checker's rerun (C14's environment, so C14 reproduces the
    22	pasted stdout); a nonzero exit is pasted as `verify:` with its code, and a gh, curl or URL command is not run, as C14
    23	skips it. Check: the template's commands and the items' `make` commands, each run once in a detached scratch worktree of
    24	origin/main with the caller's PATH and pasted with its exit code, the revision and its last 20 output lines; the
    25	worktree is removed with `git worktree remove --force` and its temporary parent deleted.
    26	"""
    27	
    28	import argparse
    29	import hashlib
    30	import importlib.util
    31	import os
    32	import pathlib
    33	import re
    34	import shutil
    35	import subprocess
    36	import sys
    37	import tempfile
    38	
    39	import yaml
    40	
    41	PLANS = ".orchestration/plans"
    42	TEMPLATE = pathlib.Path(__file__).with_name("task-template.md")
    43	NETWORK = r"\b(?:gh|curl)\b|https?://"
    44	GLOB = r"[*?\[]"
    45	spec = importlib.util.spec_from_file_location("checker", pathlib.Path(__file__).with_name("task-consistency-check.py"))
    46	checker = importlib.util.module_from_spec(spec)
    47	spec.loader.exec_module(checker)
    48	
    49	
    50	def git(root, *args):
    51	    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=False)
    52	
    53	
    54	def rows(lines):
    55	    return [
    56	        [c.strip() for c in l.strip().strip("|").split("|")]
    57	        for l in lines
    58	        if l.startswith("|") and not re.match(r"\|\s*-{3}", l)
    59	    ]
    60	
    61	
    62	def spans(text):
    63	    return re.findall(r"`([^`\n]+)`", text)
    64	
    65	
    66	def is_command(span):
    67	    words = span.split() or [""]
    68	    if re.search(r"<[^<>\s]+>", span) or not re.fullmatch(
    69	        r"[a-z][\w.+-]*|\.?\.?/[\w./-]+|[\w./-]+\.(?:sh|py)", words[0]
    70	    ):
    71	        return False
    72	    return len(words) > 1 or ("/" not in words[0] and shutil.which(words[0]) is not None)
    73	
    74	
    75	def program(lines, n):
    76	    start = next(i for i, l in enumerate(lines) if l.startswith(f"**({n}) "))
    77	    end = next((i for i in range(start + 1, len(lines)) if re.match(r"\*\*\(\d+\) ", lines[i])), len(lines))
    78	    return "\n".join(lines[start:end]).strip()
    79	
    80	
    81	def run_check_commands(root, commands, tid):
    82	    parent = pathlib.Path(tempfile.mkdtemp(prefix=f"{tid}."))
    83	    scratch = parent / "origin-main"
    84	    try:
    85	        if git(root, "worktree", "add", "--detach", str(scratch), "origin/main").returncode:
    86	            return [f"- `{c}`: not run (no origin/main worktree)" for c in commands]
    87	        try:
    88	            rev, out = git(scratch, "rev-parse", "HEAD").stdout.strip(), []
    89	            for c in commands:
    90	                stdout, code, stderr = checker.rerun(c, scratch, os.environ["PATH"])
    91	                tail = ["```", *((stdout or "") + stderr).splitlines()[-20:], "```"]
    92	                out.append(f"- `{c}`: exit {code} on origin/main {rev[:12]}" + "".join(f"\n  {l}" for l in tail))
    93	            return out
    94	        finally:
    95	            git(root, "worktree", "remove", "--force", str(scratch))
    96	    finally:
    97	        shutil.rmtree(parent, ignore_errors=True)
    98	
    99	
   100	def main():
   101	    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
   102	    parser.add_argument("todo_id")
   103	    parser.add_argument("--out", type=pathlib.Path)
   104	    parser.add_argument("--seat", help="the wave table column to read (for example a009)")
   105	    parser.add_argument("--worktree", help="the seat's worktree, named in the task's opening line")
   106	    args = parser.parse_args()
   107	    root = pathlib.Path(git(".", "rev-parse", "--show-toplevel").stdout.strip())
   108	    # The plan's commands are the orchestrator's own text, so they run only as committed.
   109	    status = git(root, "status", "--porcelain=v1", "--untracked-files=all", "--", f":(glob){PLANS}/024-*")
   110	    if status.returncode or status.stdout:
   111	        sys.exit(
   112	            f"task-from-plan: refused: the plan group has uncommitted changes; commit them first:\n{status.stdout}"
   113	        )
   114	    rev = git(root, "rev-parse", "HEAD").stdout.strip()
   115	
   116	    def read(name):
   117	        shown = git(root, "show", f"{rev}:{PLANS}/{name}")
   118	        if shown.returncode:
   119	            sys.exit(f"task-from-plan: {PLANS}/{name} is not in the commit {rev}")
   120	        return shown.stdout.splitlines()
   121	
   122	    out = args.out or pathlib.Path(f".orchestration/tasks/{args.todo_id}.md")
   123	    tid, own = out.stem, f".orchestration/{out.stem}/"
   124	    template = TEMPLATE.read_text().replace("<task_id>", tid)
   125	    bundled = checker.front(template)
   126	    row = next(c for c in rows(read("024-todo.md")) if c[0].split()[0] == args.todo_id)
   127	    title, purpose, work, completion = row[0].split(" ", 1)[-1], row[1], row[2], row[-1]
   128	    items = [program(read("024-design-programs.md"), n) for n in dict.fromkeys(re.findall(r"\((\d+)\)", work))]
   129	    qa = next((c for c in rows(read("024-design-quality.md")) if c[0].startswith("Q-A")), [""])
   130	    listed = " ".join(qa)
   131	    num = re.fullmatch(r"P1-(\d+)", args.todo_id)
   132	    in_range = num and any(int(a) <= int(num[1]) <= int(b) for a, b in re.findall(r"P1-(\d+)〜P1-(\d+)", listed))
   133	    security = bool(re.search(rf"{re.escape(args.todo_id)}(?![\w-])", listed) or in_range)
   134	
   135	    names = [s.split()[0] for s in spans(work + "\n" + "\n".join(items)) if s.split()]
   136	    # A literal has a file extension or exists, so a ref such as origin/main is not proposed; a glob stays a scope.
   137	    cand = [n.rstrip(".,") for n in names if "/" in n and not n.startswith(("-", "~"))]
   138	    paths = [
   139	        n
   140	        for n in cand
   141	        if re.fullmatch(r"[\w.@/*?\[\]-]+", n)
   142	        and checker.confined(root, n)
   143	        and (re.search(GLOB, n) or "." in n.rsplit("/", 1)[-1] or (root / n).exists())
   144	    ]
   145	    hits = {}
   146	    for script in dict.fromkeys(
   147	        pathlib.Path(n).name for n in names if n.endswith((".sh", ".py")) and not re.search(GLOB, n)
   148	    ):
   149	        for hit in git(root, "grep", "-l", "-F", "-e", script, "--", "scripts", "tests").stdout.split():
   150	            hits.setdefault(hit, script)
   151	    allowed = list(dict.fromkeys(paths + list(hits))) + [f"{own}**"]
   152	
   153	    rows_out = [{"control": f"{p} ({title})", "disposition": f"residual: {completion}"} for p in allowed[:-1]]
   154	    for g in (a for a in allowed[:-1] if re.search(GLOB, a)):  # C12: every executed or applied file a glob matches
   155	        for f in filter(None, git(root, "ls-files", "-z", "--", f":(glob){g}").stdout.split("\0")):
   156	            if checker.applied(f) and f not in allowed and not f.startswith("tests/fixtures/"):  # an entry has its row
   157	                rows_out.append({"control": f"{f} (matched by {g})", "disposition": f"residual: {completion}"})
   158	    rows_out += bundled.get("threat_table") or []
   159	
   160	    commands = [s for s in dict.fromkeys(spans("\n".join(items))) if is_command(s)]
   161	    premises = []
   162	    for cmd in (c for c in commands if c.split()[0] != "make"):
   163	        if re.search(NETWORK, cmd):
   164	            premises.append(
   165	                {
   166	                    "claim": f"verify: {cmd} is a network command, not run here (C14 skips it)",
   167	                    "command": cmd,
   168	                    "output": "",
   169	                }
   170	            )
   171	            continue
   172	        stdout, code, _ = checker.rerun(cmd, root)
   173	        claim = f"the program item's `{cmd}` exits 0" if code == 0 else f"verify: `{cmd}` exits {code}"
   174	        premises.append({"claim": claim, "command": cmd, "output": (stdout or "").rstrip("\n")})
   175	    makes = [c for c in commands if c.split()[0] == "make"]
   176	    checks = run_check_commands(root, list(dict.fromkeys((bundled.get("check") or []) + makes)), tid)
   177	
   178	    plan = read("024-omp-cutover-and-corrective-order.md")
   179	    six = plan[next(i for i, l in enumerate(plan) if l.startswith("## 6.")) :]
   180	    six = six[: next((i for i, l in enumerate(six) if l.startswith("## 7.")), len(six))]
   181	    header = next((c for c in rows(six) if c and c[0] == "波"), [])
   182	    col = header.index(args.seat) if args.seat in header else None
   183	    whole = re.compile(rf"(?<![\w-]){re.escape(args.todo_id)}(?![\w-])")
   184	    wave = next(
   185	        (c for c in rows(six) if whole.search(c[col] if col is not None and col < len(c) else " ".join(c))), None
   186	    )
   187	
   188	    front = {"format": 2, "task_id": tid, "kind": "code", "security": security, "allowed_files": allowed, "after": []}
   189	    front |= {"threat_table": rows_out, "premises": premises}
   190	    files = [f"{n}. {item}" for n, item in enumerate(items, 1)] + [
   191	        f"# from: {h} (git grep -l {s})" for h, s in hits.items()
   192	    ]
   193	    seat = f"seat {args.seat or 'unassigned'}" + (f", worktree {args.worktree}" if args.worktree else "")
   194	    text = f"""---
   195	{yaml.safe_dump(front, sort_keys=False, allow_unicode=True, width=1000)}---
   196	
   197	# AGMSG-TASK {tid} — {title} (plan 024 {args.todo_id})
   198	
   199	Generated by scripts/orchestrator/task-from-plan.py from `024-todo.md` row {args.todo_id} and its program items, read from the plan group at {rev}; wave {wave[0] if wave else "none"} ({seat}). Every premise output is the command's own stdout.
   200	
   201	## Goal
   202	
   203	{purpose}
   204	
   205	## Files
   206	
   207	{chr(10).join(files)}
   208	
   209	## Out of scope
   210	
   211	Everything the todo row {args.todo_id} and its program items do not name.
   212	
   213	## Check
   214	
   215	{chr(10).join(checks)}
   216	
   217	## Completion
   218	
   219	{template.split(chr(10) + "## Completion" + chr(10), 1)[1].strip()}
   220	
   221	## Checks (pasted by the orchestrator before each send)
   222	
   223	```
   224	(pending: pasted at dispatch)
   225	```
   226	"""
   227	    out.parent.mkdir(parents=True, exist_ok=True)
   228	    out.write_text(text)
   229	    # The generator's own text, whose premises it has just run itself, is the trusted text C14 reruns.
   230	    sha = hashlib.sha256(out.read_bytes()).hexdigest()
   231	    verdict = subprocess.run(
   232	        [sys.executable, "-I", checker.__file__, "--root", str(root), "--premises-sha", sha, str(out)],
   233	        capture_output=True,
   234	        text=True,
   235	        check=False,
   236	    )
   237	    print(verdict.stdout + verdict.stderr, end="")
   238	    return 0 if verdict.returncode == 0 else 1
   239	
   240	
   241	if __name__ == "__main__":
   242	    sys.exit(main())

 succeeded in 155ms:
     1	"""Form, drift and invariant checks over the plan 024 group (plan 024 programs (15)), one violation per line.
     2	
     3	`uv run --no-project --with pyyaml python -I scripts/orchestrator/plan-check.py [--root <repo>] [--drift] [--invariants]`
     4	reads the eleven `.orchestration/plans/024-*` files under --root (default: the current git toplevel), prints every
     5	violation on its own line and exits 1 when there is one, 0 otherwise. It writes nothing.
     6	F1 every 024-todo.md table row has a non-empty completion (last) column.
     7	F2 the tasks one wave row of the plan's section 6 names have pairwise-disjoint allowed_files once their task files
     8	   exist (a task file belongs to the todo id its `# ` title line names): each glob entry stands for the tree files it
     9	   matches, a literal entry for itself, and two lists overlap where a path is in both or inside the other's directory,
    10	   or where a literal matches the other's glob; the finding names the first shared path. Glob spellings are never
    11	   compared with each other.
    12	F3 every P1-<n> row names a bottleneck id: a B<n> row of 024-design-mechanism.md or an M<n> row of 024-design-quality.md.
    13	F4 every DoD row of 024-checklists.md holds a backtick command or a file path.
    14	F5 every decision row of the plan's section 2 has a bold default.
    15	F6 every cited dotfiles-T<n>-... id is a task file, every D-... id a row of .orchestration/decisions.tsv, and with
    16	   --drift every #<pr> a pull request.
    17	--drift: every head sha or state word (CLEAN, BEHIND, draft, merged, closed) that starts within 40 characters after a
    18	   #<pr> on its line, before the next #, each compared on its own against `gh pr view`; and every 024-progress.tsv row
    19	   naming a task against the status of that task's latest AGMSG-ACCEPTANCE event (task_id=<task>, each event read up
    20	   to the next one on its line) in its acceptance record, latest by the last timestamp before the event on its line (an
    21	   untimed event carries the latest timestamp above it), then by position: `drift: <file>:<line> <cited> != <live>`.
    22	--invariants: ANTHROPIC_OAUTH_TOKEN= with a value (bare, single- or double-quoted; an empty "" or '' is none),
    23	   `git push origin main`, `gh pr merge` with --admin or --auto in the
    24	   plan files, and a claude.permissions.ask entry home/dot_agents/agent-config.yaml adds against origin/main.
    25	"""
    26	
    27	import argparse
    28	import glob
    29	import json
    30	import pathlib
    31	import re
    32	import subprocess
    33	import sys
    34	from fnmatch import fnmatchcase
    35	
    36	try:
    37	    import yaml
    38	except ImportError:
    39	    print("needs pyyaml: run with uv run --no-project --with pyyaml")
    40	    sys.exit(2)
    41	
    42	PLANS = ".orchestration/plans"
    43	TASK_ID = r"\bdotfiles-T\d+(?:-[a-z0-9]+)+"
    44	DECISION_ID = r"\bD-(?!W\d)[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*"
    45	GLOB = re.compile(r"[*?[]")
    46	STATES = {"CLEAN": ("mergeStateStatus", "CLEAN"), "BEHIND": ("mergeStateStatus", "BEHIND"), "draft": ("isDraft", True)}
    47	STATES |= {"merged": ("state", "MERGED"), "closed": ("state", "CLOSED")}
    48	FORBIDDEN = {
    49	    "ANTHROPIC_OAUTH_TOKEN with a value": r"ANTHROPIC_OAUTH_TOKEN=(?:\"[^\"\n]+\"|'[^'\n]+'|[^\s`'\")<])",
    50	    "git push origin main": r"git push origin main\b",
    51	    "gh pr merge --admin or --auto": r"gh pr merge\b[^\n]*?--(?:admin|auto)\b",
    52	}
    53	
    54	
    55	def run(root, *args):
    56	    return subprocess.run(args, cwd=root, capture_output=True, text=True, check=False)
    57	
    58	
    59	def cells(line):
    60	    return [c.strip() for c in line.strip().strip("|").split("|")]
    61	
    62	
    63	def table_rows(lines):
    64	    """(line number, cells) of every table data row: not a header (the row above a separator) nor a separator."""
    65	    rows = []
    66	    for i, line in enumerate(lines):
    67	        nxt = lines[i + 1] if i + 1 < len(lines) else ""
    68	        if line.startswith("|") and not re.match(r"\|\s*-{3}", line) and not re.match(r"\|\s*-{3}", nxt):
    69	            rows.append((i + 1, cells(line)))
    70	    return rows
    71	
    72	
    73	def section(lines, number):
    74	    start = next((i for i, l in enumerate(lines) if l.startswith(f"## {number}.")), None)
    75	    if start is None:
    76	        return []
    77	    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    78	    return [""] * (start + 1) + lines[start + 1 : end]  # keeps the file's line numbers
    79	
    80	
    81	def scope(root, entries):
    82	    """(paths, globs) of an allowed_files list: its literals and the tree files each glob matches, and its globs."""
    83	    globs = {e for e in entries if GLOB.search(e)}
    84	    paths = {e.rstrip("/") for e in entries if e not in globs}
    85	    for g in globs:
    86	        paths |= {p for p in glob.glob(g, root_dir=root, recursive=True, include_hidden=True) if (root / p).is_file()}
    87	    return paths, globs
    88	
    89	
    90	def shared(a, b):
    91	    (pa, ga), (pb, gb) = a, b
    92	    out = {x for x in pa for y in pb if x == y or x.startswith(y + "/")}
    93	    out |= {y for x in pa for y in pb if y.startswith(x + "/")}
    94	    # A literal not yet in the tree overlaps a glob it matches (fnmatch's * also crosses /, which errs toward a report).
    95	    out |= {x for x in pa for g in gb if fnmatchcase(x, g)} | {y for y in pb for g in ga if fnmatchcase(y, g)}
    96	    return sorted(out)
    97	
    98	
    99	def latest(text, tid):
   100	    """The status of tid's latest AGMSG-ACCEPTANCE event, or none."""
   101	    events, carried, stamp = [], "", r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2})?"
   102	    for i, line in enumerate(text.splitlines()):
   103	        for m in re.finditer(r"AGMSG-ACCEPTANCE v1 (.*?)(?=AGMSG-ACCEPTANCE v1 |$)", line):  # one event at a time
   104	            status = re.search(r"\bstatus=([\w-]+)", m[1])
   105	            if status and re.search(rf"\btask_id={re.escape(tid)}(?![\w-])", m[1]):
   106	                stamps = re.findall(stamp, line[: m.start()])
   107	                events.append((stamps[-1] if stamps else carried, i, m.start(), status[1]))
   108	        carried = max([carried, *re.findall(stamp, line)])
   109	    return max(events)[3] if events else "none"
   110	
   111	
   112	def form(root, files):
   113	    out = []
   114	    todo, plan = files["024-todo.md"], files["024-omp-cutover-and-corrective-order.md"]
   115	    for n, c in table_rows(todo):  # F1
   116	        if not c[-1]:
   117	            out.append(f"F1 024-todo.md:{n} {c[0][:20]} has an empty completion column")
   118	    ids = set(re.findall(r"^\| (B\d+) \|", "\n".join(files["024-design-mechanism.md"]), re.M))
   119	    ids |= set(re.findall(r"^\| (M\d+) \|", "\n".join(files["024-design-quality.md"]), re.M))
   120	    for n, c in table_rows(todo):  # F3
   121	        if c[0].startswith("P1-") and not set(re.findall(r"\b[BM]\d+\b", " ".join(c))) & ids:
   122	            out.append(f"F3 024-todo.md:{n} {c[0].split()[0]} names no bottleneck id of 5.0 or 5.10")
   123	    tasks = {}
   124	    for p in sorted((root / ".orchestration/tasks").glob("*.md")):
   125	        title = next((l for l in p.read_text().splitlines() if l.startswith("# ")), "")
   126	        for tid in set(re.findall(r"\bP1-\d+[a-z]?\b", title)):
   127	            allowed = (yaml.safe_load(p.read_text().split("\n---\n", 1)[0].lstrip("-\n")) or {}).get("allowed_files")
   128	            tasks.setdefault(tid, set()).update(allowed or [])
   129	    tasks = {tid: scope(root, entries) for tid, entries in tasks.items()}
   130	    for n, c in table_rows(section(plan, 6)):  # F2
   131	        wave = sorted(set(re.findall(r"\bP1-\d+[a-z]?\b", " ".join(c[1:]))) & set(tasks))
   132	        for i, a in enumerate(wave):
   133	            for b in wave[i + 1 :]:
   134	                if both := shared(tasks[a], tasks[b]):
   135	                    out.append(f"F2 024-omp-cutover-and-corrective-order.md:{n} {c[0]} {a} and {b} share {both[0]}")
   136	    for n, c in table_rows(files["024-checklists.md"]):  # F4
   137	        if not re.search(r"`[^`]+`|[\w.~-]*/[\w./-]+|\b\w+\.(?:md|json|tsv|ya?ml|sh|py)\b", " ".join(c[1:])):
   138	            out.append(f"F4 024-checklists.md:{n} {c[0]} holds no backtick command or file path")
   139	    for n, c in table_rows(section(plan, 2)):  # F5
   140	        if re.match(r"D\d+\b", c[0]) and not re.search(r"\*\*[^*]+\*\*", c[-1]):
   141	            out.append(f"F5 024-omp-cutover-and-corrective-order.md:{n} {c[0].split()[0]} has no bold default")
   142	    decisions = {l.split("\t", 1)[0] for l in (root / ".orchestration/decisions.tsv").read_text().splitlines()[1:]}
   143	    for name, lines in files.items():  # F6
   144	        for n, line in enumerate(lines, 1):
   145	            for tid in dict.fromkeys(re.findall(TASK_ID, line)):
   146	                if not (root / f".orchestration/tasks/{tid}.md").is_file():
   147	                    out.append(f"F6 {name}:{n} cites {tid}, which is not a task file")
   148	            # A family such as D-024-* names no single decision.
   149	            ids = [m.group() for m in re.finditer(DECISION_ID, line) if line[m.end() : m.end() + 2] != "-*"]
   150	            for did in dict.fromkeys(ids):
   151	                if did not in decisions:
   152	                    out.append(f"F6 {name}:{n} cites {did}, which is not a row of decisions.tsv")
   153	    return out
   154	
   155	
   156	def drift(root, files):
   157	    out, live = [], {}
   158	
   159	    def pr(number):
   160	        if number not in live:
   161	            got = run(root, "gh", "pr", "view", number, "--json", "headRefOid,mergeStateStatus,isDraft,state")
   162	            live[number] = json.loads(got.stdout) if got.returncode == 0 else None
   163	        return live[number]
   164	
   165	    for name, lines in files.items():
   166	        for n, line in enumerate(lines, 1):
   167	            for number in dict.fromkeys(re.findall(r"#(\d{2,6})\b", line)):
   168	                if pr(number) is None:
   169	                    out.append(f"F6 {name}:{n} cites #{number}, which is not a pull request")
   170	            found = {}
   171	            for m in re.finditer(r"#(\d{2,6})\b([^#\n]*)", line):
   172	                state = pr(m.group(1))
   173	                if state is None:
   174	                    continue
   175	                tokens = re.finditer(r"\b([0-9a-f]{7,40}|CLEAN|BEHIND|draft|merged|closed)\b", m.group(2))
   176	                for cited in dict.fromkeys(t.group() for t in tokens if t.start() <= 40):
   177	                    if cited in STATES:
   178	                        key, want = STATES[cited]
   179	                        if state.get(key) != want:
   180	                            found[f"drift: {name}:{n} #{m.group(1)} {cited} != {state.get(key)}"] = None
   181	                    elif not state.get("headRefOid", "").startswith(cited):
   182	                        found[f"drift: {name}:{n} #{m.group(1)} {cited} != {state.get('headRefOid', '')[:12]}"] = None
   183	            out += found
   184	    for n, line in enumerate(files["024-progress.tsv"][1:], 2):
   185	        tid, *rest = line.split("\t")
   186	        record = root / f".orchestration/acceptance/{tid}.md"
   187	        if not rest or not (root / f".orchestration/tasks/{tid}.md").is_file():
   188	            continue
   189	        live = latest(record.read_text(), tid) if record.is_file() else "none"
   190	        if len(rest) > 2 and rest[2] != live:
   191	            out.append(f"drift: 024-progress.tsv:{n} {tid} {rest[2]} != {live}")
   192	    return out
   193	
   194	
   195	def invariants(root, files):
   196	    out = []
   197	    for name, lines in files.items():
   198	        for n, line in enumerate(lines, 1):
   199	            out += [f"invariant: {name}:{n} {what}" for what, rx in FORBIDDEN.items() if re.search(rx, line)]
   200	    path = "home/dot_agents/agent-config.yaml"
   201	    base = run(root, "git", "show", f"origin/main:{path}")
   202	    if base.returncode == 0 and (root / path).is_file():
   203	
   204	        def asks(text):
   205	            return ((yaml.safe_load(text) or {}).get("claude") or {}).get("permissions", {}).get("ask") or []
   206	
   207	        old = asks(base.stdout)
   208	        out += [f"invariant: {path} permissions.ask adds {e}" for e in asks((root / path).read_text()) if e not in old]
   209	    return out
   210	
   211	
   212	def main():
   213	    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
   214	    parser.add_argument("--root", type=pathlib.Path, help="the repository (default: the current git toplevel)")
   215	    parser.add_argument(
   216	        "--drift", action="store_true", help="compare cited PR states and progress rows with live state"
   217	    )
   218	    parser.add_argument("--invariants", action="store_true", help="report forbidden patterns and added ask entries")
   219	    args = parser.parse_args()
   220	    root = args.root or pathlib.Path(run(".", "git", "rev-parse", "--show-toplevel").stdout.strip())
   221	    paths = sorted((root / PLANS).glob("024-*.md")) + [root / PLANS / "024-progress.tsv"]
   222	    files = {p.name: p.read_text().splitlines() for p in paths}
   223	    found = form(root, files)
   224	    found += drift(root, files) if args.drift else []
   225	    found += invariants(root, files) if args.invariants else []
   226	    if found:
   227	        print("\n".join(found))
   228	    return 1 if found else 0
   229	
   230	
   231	if __name__ == "__main__":
   232	    sys.exit(main())

 succeeded in 247ms:
{
  "lastAnalyzedAt": "2026-10-02T14:12:51Z",
  "gitCommitHash": "940a3a2b07adfd14140a0acff96784ef53a0a509",
  "version": "1.0.0",
  "analyzedFiles": 368
}

graph present

   141	9. Audit finding 5, P2, is fixed by comparing assigned invariant ids as well as sentences. C15 obtains the assignment from the design on `origin/main`, including when the task omits `invariants`.
   142	
   143	   `tests/unit/test_task_consistency_c11_c15.py::test_c15_requires_the_design_assigned_invariant_id_set` assigns INV-1 and INV-2, supplies only the correct INV-1 sentence and expects C15. It also covers an absent map, an extra id, a changed sentence and the complete byte-identical assignment. The missing-id case is red against `9da0ed3` and all cases are green after the fix.
   144	
   145	10. Audit finding 6, P2, is fixed by expanding each glob before deciding which matched files require concrete threat rows. A matched `.sh`, `.py`, `.yaml`, `.yml`, `.json` or `.toml` file, or a file under `home/`, `scripts/`, `.githooks/` or `.github/`, receives the executed-or-applied treatment regardless of the glob's spelling. The fixture and own-evidence exemptions remain.
   146	
   147	    `tests/unit/test_task_consistency_c11_c15.py::test_c12_classifies_concrete_glob_matches_before_the_glob_spelling` places a tracked shell script under `install/`, permits `install/**` and omits its concrete row. That case reports C12; adding the concrete row clears it. The test also retains the exempt-directory cases. It is red against `9da0ed3` and green after the fix.
   148	
   149	11. Audit finding 7, P2, is fixed by expanding wildcard scopes to their concrete tree matches before F2 compares simultaneous tasks. Literal paths remain represented, and overlap diagnostics identify a shared concrete path. Comparing glob spellings against each other does not establish disjointness.
   150	
   151	    `tests/unit/test_plan_check.py::test_f2_detects_intersecting_globs_through_concrete_tree_matches` gives two simultaneous tasks `scripts/test_*.py` and `scripts/*_check.py` and creates `scripts/test_check.py`. It expects one F2 overlap. Disjoint concrete matches pass, and the existing glob-versus-literal case remains covered. The intersecting-glob case is red against `9da0ed3` and green after the fix.
   152	
   153	12. Audit finding 8, P2, is fixed by selecting wave rows through whole todo-id tokens in the selected seat column. `P1-1` does not match `P1-10`, `P1-11` or `P1-12`.
   154	
   155	    `tests/unit/test_task_from_plan.py::test_wave_selection_matches_whole_todo_ids` places the longer ids in an earlier wave and `P1-1` in its own wave, with distinguishable Check commands. It asserts the correct wave, seat and Check provenance. It is red against `9da0ed3` and green after the fix.
   156	
   157	13. Audit finding 9, P2, is fixed by preserving explicit wildcard scopes in generated `allowed_files` and threat rows. Path extraction accepts `scripts/*.py` and `home/dot_config/**` as scopes and retains their proposal provenance. Required concrete C12 rows accompany applicable matches.
   158	
   159	    `tests/unit/test_task_from_plan.py::test_generator_preserves_wildcard_scopes_and_their_threat_rows` names both scopes in a committed fixture program item, creates concrete matches and asserts that the generated front matter preserves both scopes and their required rows. The generated fixture passes the real checker. It is red against `9da0ed3` and green after the fix.
   160	
   161	14. Audit finding 10, P2, is fixed by reading a numbered program item through the next numbered program heading or end of file. Blank lines, fenced schemas and subsequent paragraphs remain inside the current item.
   162	
   163	    `tests/unit/test_task_from_plan.py::test_program_item_continues_until_the_next_numbered_heading` places a required path and command after a blank line and fenced block, followed by another numbered item. The generated Files and premises include the entire selected item and exclude the next item. It is red against `9da0ed3` and green after the fix.
   164	
   165	15. Audit finding 11, P2, is fixed by retaining command spans without requiring that their executable currently exists. Single-word commands and commands containing redirects remain executable command candidates. Path and wildcard spans retain their separate scope role. Actual execution supplies stdout and exit status; an unavailable executable or shell syntax failure remains a `verify:` record with the observed status. Check-command extraction follows the same recognition rule.
   166	
   167	    `tests/unit/test_task_from_plan.py::test_generator_retains_unavailable_single_word_and_redirecting_commands` includes an unavailable executable, a single-word `pwd` and a command redirecting output to a temporary fixture file. It asserts the retained command strings, actual statuses, stdout and `verify:` treatment, and exercises the same forms in Check extraction. It is red against `9da0ed3` and green after the fix.
   168	
   169	16. Audit finding 12, P2, is fixed by selecting acceptance events through their timestamps and task identity. The last textual match is not the latest event. An event for another task does not determine this task's progress state.
   170	
   171	    `tests/unit/test_plan_check.py::test_drift_uses_the_latest_timestamped_acceptance_for_the_same_task` supplies a newer acceptance before an older revision in textual order and includes a still newer event for another task. The matching accepted progress row passes; changing it to revise produces one drift finding. It is red against `9da0ed3` and green after the fix.
   172	
   173	17. Audit finding 13, P2, is fixed by collecting every nearby SHA and state associated with each PR occurrence. Association stays within that occurrence's line and context and stops before the next PR occurrence. Each assertion is compared independently. A matching head does not suppress a conflicting live state.
   174	
   175	    `tests/unit/test_plan_check.py::test_drift_checks_every_sha_and_state_for_each_pr_occurrence` includes `#77 abc1234 merged` with a matching live head and live state OPEN and expects the merged-versus-OPEN finding. It also covers multiple nearby SHAs and repeated PR occurrences with distinct assertions. It is red against `9da0ed3` and green after the fix.
   176	
   177	18. Audit finding 14, P2, is fixed by recognizing nonempty quoted values immediately after `ANTHROPIC_OAUTH_TOKEN=`. Single-quoted, double-quoted and unquoted nonempty assignments produce invariant findings.
   178	
   179	    `tests/unit/test_plan_check.py::test_invariants_reject_nonempty_quoted_oauth_token_assignments` constructs harmless fixture values at runtime and checks both quote forms and the existing unquoted case. Empty assignments remain distinct from nonempty values, and diagnostics contain no assigned value. The quoted cases are red against `9da0ed3` and green after the fix.
   180	
   181	19. Audit finding 15, P2, is fixed by assigning the C12 remedy to this task through item 10. The advisory owner does not need a future amendment to acquire the checker or its test module for this finding. The other inherited findings fixed above are also superseded by this reset's ownership.
   182	
   183	    The orchestrator records the corrected ownership in the lineage's acceptance records and withdraws the corresponding remedy from `dotfiles-T133-task-generator-plan-check-followup-a01`. The worker reports the finding, item 10's selector and its actual fix commit. `tests/unit/test_task_consistency_c11_c15.py::test_c12_classifies_concrete_glob_matches_before_the_glob_spelling` supplies the red-then-green implementation proof. A read-only record assertion contrasts the old assignment requiring an amendment with the corrected assignment to a02 and its fix evidence. The worker does not edit the canonical owner task or acceptance records.
   184	
   185	20. The checker's own hardening, found by the regime job's review of PR #418 (a008, 21:37:56Z) and assigned here: C10 passes every backticked literal to `git grep` as a pattern operand after `-e` (or as a positional after `--`), never as a bare argument that `git grep` can parse as an option, so a literal such as `--open-files-in-pager=CMD` searches for that text and runs nothing; every path the checker opens or passes to a subprocess (C6's design path included) is resolved and confined to the checkout root given by `--root`, and a path outside it is a finding, not a read. `tests/unit/test_task_consistency_c11_c15.py::test_c10_never_passes_a_literal_as_a_git_grep_option` (a fixture task whose backticked literal is `--open-files-in-pager=<marker command>`: the marker is never written and C10 reports the literal as unmatched) and `::test_c6_confines_design_paths_to_the_checkout` are written first and red against 9da0ed3.
   186	
   187	## Out of scope
   188	
   189	`reset-task.sh` remains the later C-69 item. `scripts/orchestrator/dispatch.sh`, including `--next`, the trusted-SHA argument and warning forwarding, remains in the P1-5 to P1-6 dispatch lineage identified in item 8. The regime CI job and validate wiring remain P1-11. `ruleset-request.sh`, `ruleset-verify.sh` and permission-policy changes remain P1-14.
   190	

**Monitoring output size**
codex
The diff adds the generator and plan checker, plus C11–C15 and path hardening in the existing checker. I’m tracing command execution, path confinement, and test coverage against the task’s requirements. GitHub access failed, so CI verification currently relies on the supplied feedback snapshot.
exec
/bin/zsh -lc 'git show 8a09b9365932f23b09df8aa2385a93d0b3016a3e:scripts/orchestrator/task-consistency-check.py | nl -ba' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc 'git diff b22a5580d0778e57a66d3f75c76e3c55b88701e1 8a09b9365932f23b09df8aa2385a93d0b3016a3e -- tests/unit/test_regime_ci.py tests/unit/test_task_checkers.py && git show 8a09b9365932f23b09df8aa2385a93d0b3016a3e:scripts/orchestrator/task-template.md | nl -ba' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc "git diff --name-only 940a3a2b07adfd14140a0acff96784ef53a0a509..HEAD | head -n 25 && ls -l .orchestration/reports/dotfiles-T133-task-generator-plan-check-a02.md .orchestration/validation/dotfiles-T133-task-generator-plan-check-a02.md .orchestration/sandboxes/dotfiles-T133-task-generator-plan-check-a02.md && python3 -B -c 'import json,pathlib; d=json.loads(pathlib.Path(\".orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-pr-feedback.json\").read_text()); print(json.dumps(d,indent=2))'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 125ms:
     1	"""Read-only cross-field check of a format-2 task file, before dispatch and at acceptance (plan 007 T704).
     2	
     3	`uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py [--root <repo>]
     4	[--premises-sha <sha256>] <task.md>...`
     5	resolves the design path (C6) and probes origin/main with git (C8 to C10) under --root (default: the first file's git
     6	toplevel), prints `<file name>: OK` or `: FAIL` with one `  C<n> ...` line per finding, and exits 1 when any file fails.
     7	C14's warnings and skip notes, never findings, go to stderr as `<file name>: warning: <text>` or `<file name>: note:
     8	<text>`. Every path it opens or hands to git is first resolved and confined to --root; one that leaves it is a finding.
     9	C1 task_id equals the file name.
    10	C2 allowed_files covers .orchestration/<task_id>/** and names no other task's .orchestration/<id>/ directory.
    11	C3 when reset_of is non-empty, a threat_table row names every reset_of id's task.md and the task's own.
    12	C4 every allowed_files entry (its path before any glob) is named in a row's control, followed by its end, a space, / " ' ( ) , or a glob.
    13	C5 no residual binds a predecessor's hash ("names the <aNN> file's hash") instead of the task's own.
    14	C6 design_review.receipt is the design file's current design_review.receipt; a design path outside --root is a finding.
    15	C7 one row per non-path control name and per orchestrator effect name (the SKILL row unit).
    16	C7b no row other than a non-path control names two allowed_files entries (one row per entry).
    17	C8 (code tasks) every *_EVIDENCE input the body names and origin/main does not read yet has a threat row.
    18	C9 (docs tasks) a quoted rule sentence naming a script, *_EVIDENCE, a check id or classes: finds it on origin/main or says once/until.
    19	C10 (docs tasks) a quoted rule sentence naming a script on origin/main has no `=` or `[...]` literal absent from the script and its test
    20	    (each literal reaches git grep after -e, never as an option).
    21	C11 a disposition's payload has its form's shape: closed: tests/<path>::<identifier>, out-of-scope: an existing task id, residual: 20+ characters.
    22	C12 every executed or applied file a glob entry matches (*.sh *.py *.yaml *.yml *.json *.toml, or under home/ scripts/ .githooks/
    23	    .github/), whatever the glob spells, has a row naming it; tests/fixtures/ and the task's own directory are exempt.
    24	C13 every disposition is exactly one of closed:, residual: or out-of-scope: followed by a space.
    25	C14 every premise command, run under bash -c with pipefail, PATH <root>/bin:/usr/bin:/bin, prints its pasted output with whitespace runs
    26	    collapsed (gh, curl and URLs skipped; a tool absent from that PATH is a `C14: tool absent <name>` warning). It runs
    27	    only for a file whose sha256 is --premises-sha, the dispatched text; any other file gets `C14: not run (no trusted
    28	    sha)` as a warning and nothing is executed: a structural OK is then no claim that the premises pass.
    29	C15 with design_review.design, the design on origin/main exists (unless the task carries no invariants and the design is
    30	    in this checkout, still in flight; a path naming no design anywhere is always one); when its implementing_tasks maps this task to invariant ids, the task carries
    31	    exactly those ids, an omitted map included, and each sentence equals the design's byte for byte (a list form
    32	    assigns no ids, so every invariant the task carries does; a design task compares its own definitions).
    33	"""
    34	
    35	import argparse
    36	import hashlib
    37	import os
    38	import pathlib
    39	import re
    40	import subprocess
    41	import sys
    42	
    43	try:
    44	    import yaml
    45	except ImportError:
    46	    print("needs pyyaml: run with uv run --no-project --with pyyaml")
    47	    sys.exit(2)
    48	
    49	ROW_UNIT = "task metadata|metadata separators|in-process effects|workflow and interpreter or environment inputs|new or renamed scripts|orchestrator effect merge|orchestrator effect update-branch|orchestrator effect forced worker removal"
    50	C7_NAMES = ROW_UNIT.split("|")
    51	NONPATH = ("in-process effects", "task metadata", "metadata separators", "workflow and interpreter")
    52	NONPATH += ("new or renamed scripts", "orchestrator effect")
    53	C9_NAMES = r"(scripts/[\w./-]+|\b[A-Z][A-Z_]{3,}_EVIDENCE\b|task-consistency-check C\d|\bC\d\b of the task-consistency check|\bclasses:)"
    54	CHECKER = "scripts/orchestrator/task-consistency-check.py"  # where `task-consistency-check C<n>` lands
    55	FORMS = ("closed: ", "residual: ", "out-of-scope: ")
    56	APPLIED = (".sh", ".py", ".yaml", ".yml", ".json", ".toml")
    57	APPLIED_DIRS = ("home/", "scripts/", ".githooks/", ".github/")
    58	SKIPPED = "C14 skipped network premise"  # a note, never a failure
    59	ABSENT = "C14: tool absent"  # a warning, never a failure (Amendment 1)
    60	UNTRUSTED = "C14: not run (no trusted sha)"  # a warning: the file is not the text --premises-sha names (revise 1)
    61	
    62	
    63	def applied(path):
    64	    """An executed or applied file, by its kind or its place (C12 and task-from-plan.py's concrete rows)."""
    65	    return path.endswith(APPLIED) or path.startswith(APPLIED_DIRS)
    66	
    67	
    68	def confined(root, rel):
    69	    """The path resolved under root, or None when it leaves the checkout (PR #418's review)."""
    70	    path = (root / rel).resolve()
    71	    return path if path.is_relative_to(root.resolve()) else None
    72	
    73	
    74	def front(text):
    75	    return yaml.safe_load(text.split("\n---\n", 1)[0].lstrip("-\n"))
    76	
    77	
    78	def git(cwd, *args):
    79	    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=False)
    80	
    81	
    82	def rerun(cmd, cwd, path=None):
    83	    """Run a premise or Check command as C14 does; return (stdout, exit status, stderr), stdout None on a timeout.
    84	
    85	    The command is bash's script argument (`bash -c`, pipefail on), never spliced into another shell line; premises
    86	    get PATH <root>/bin:/usr/bin:/bin so a rerun prints what the pasted output says, and task-from-plan.py runs its
    87	    premises through this same function.
    88	    """
    89	    env = {"PATH": path or f"{cwd}/bin:/usr/bin:/bin", "HOME": os.environ.get("HOME", "/")}
    90	    try:
    91	        run = subprocess.run(
    92	            ["bash", "-c", "set -o pipefail\n" + cmd],
    93	            stdin=subprocess.DEVNULL,  # a command that reads stdin (`head`, `cat`) never waits on the caller's
    94	            cwd=cwd,
    95	            env=env,
    96	            capture_output=True,
    97	            text=True,
    98	            timeout=1800,
    99	            check=False,
   100	        )
   101	    except subprocess.TimeoutExpired:
   102	        return None, 124, ""
   103	    return run.stdout, run.returncode, run.stderr
   104	
   105	
   106	def check(p, root, premises_sha=None):
   107	    fm = front(text := (data := p.read_bytes()).decode())
   108	    tid = fm.get("task_id")
   109	    suffix = tid.rsplit("-", 1)[-1]
   110	    fails = []
   111	    if tid != p.stem:
   112	        fails.append(f"C1 task_id {tid} != file {p.stem}")
   113	    allowed = fm.get("allowed_files") or []
   114	    own_dir = f".orchestration/{tid}/"
   115	    if not any(a.startswith(own_dir) for a in allowed):
   116	        fails.append(f"C2 allowed_files lacks {own_dir}**")
   117	    for a in allowed:
   118	        m = re.match(r"\.orchestration/([^/]+)/", a)
   119	        if m and m.group(1) != tid:
   120	            fails.append(f"C2 allowed_files names another task directory: {a}")
   121	    rows = fm.get("threat_table") or []
   122	    rowtext = "\n".join((r.get("control") or "") + " " + (r.get("disposition") or "") for r in rows)
   123	    reset_of = fm.get("reset_of") or []
   124	    for rid in reset_of + [tid] if reset_of else []:
   125	        if not re.search(rf"(?:{re.escape(rid)}|-{rid.rsplit('-', 1)[-1]})/task\.md", rowtext):
   126	            fails.append(f"C3 no threat_table row names {rid} task.md")
   127	    for a in allowed:
   128	        # a row's control names the entry only at a path boundary: scripts/foo.py.bak does not name scripts/foo.py
   129	        named = re.compile(re.escape(a.split("*")[0].rstrip("/")) + r"(?=$|[ /\"'(),*?\[])")
   130	        if rows and not any(named.search(r.get("control") or "") for r in rows):
   131	            fails.append(f"C4 allowed path has no threat_table row naming it: {a}")
   132	    dr = fm.get("design_review") or {}
   133	    inside = dr.get("design") and confined(root, dr["design"])
   134	    if dr.get("design") and not inside:
   135	        fails.append(f"C6 design path {dr['design']} is outside the checkout")
   136	    elif inside and dr.get("receipt") and inside.exists():
   137	        cur = (front(inside.read_text()).get("design_review") or {}).get("receipt")
   138	        if cur and cur != dr["receipt"]:
   139	            fails.append(f"C6 design_review.receipt {dr['receipt']} is not the design's current receipt {cur}")
   140	    for r in rows:
   141	        m = re.search(r"names the (a\d\d) file's hash", r.get("disposition") or "")
   142	        if m and m.group(1) != suffix:
   143	            fails.append(f"C5 residual binds the {m.group(1)} hash, the task is {suffix}: {r.get('control')[:60]}")
   144	    controls = " || ".join((r.get("control") or "") for r in rows)
   145	    for name in C7_NAMES:
   146	        if rows and name not in controls.lower():
   147	            fails.append(f"C7 threat_table has no row named for: {name}")
   148	    prefixes = [re.sub(r"(/\*\*|/\*|\*)$", "", e) for e in allowed if isinstance(e, str)]
   149	    for r in rows:
   150	        if (r.get("control") or "").lstrip('"').startswith(NONPATH):
   151	            continue  # a non-path control may describe several files
   152	        hit = [e for e in prefixes if e and e in (r.get("control") or "")]
   153	        if len(hit) > 1:
   154	            fails.append(f"C7b one row names {len(hit)} allowed_files entries ({', '.join(hit)}); one row per entry")
   155	    body = text.split("\n---\n", 1)[1] if "\n---\n" in text else ""
   156	    if fm.get("kind") == "code":
   157	        for var in sorted(set(re.findall(r"\b[A-Z][A-Z0-9]+(?:_[A-Z0-9]+)*_EVIDENCE\b", body))):
   158	            # an input a script on origin/main already reads is not an added input
   159	            added = git(root, "grep", "-q", var, "origin/main", "--", "scripts", "Makefile", "home").returncode != 0
   160	            if added and rows and var not in controls:
   161	                fails.append(f"C8 the task adds input {var} but no threat row controls it")
   162	    sentences = re.findall(r'"([^"]{20,})"', body) if fm.get("kind") == "docs" else []
   163	    for sent in sentences:  # C10
   164	        for scr in set(re.findall(r"scripts/[\w./-]+\.(?:sh|py)", sent)):
   165	            if not confined(root, scr):
   166	                fails.append(f"C10 rule sentence names {scr}, a path outside the checkout")
   167	                continue
   168	            if git(root, "cat-file", "-e", f"origin/main:{scr}").returncode:
   169	                continue
   170	            m = re.search(r"\b(once|until)\b", sent, re.IGNORECASE)
   171	            if m and scr in sent[m.start() :]:
   172	                continue  # the script is named inside its own landing clause
   173	            test = f"tests/unit/test_{pathlib.Path(scr).stem.replace('-', '_')}.py"
   174	            for lit in set(re.findall(r"`([^`]*(?:=|\[[^\]]+\])[^`]*)`", sent)):
   175	                # After -e the literal is a pattern: `--open-files-in-pager=<cmd>` is searched for, never run.
   176	                if git(root, "grep", "-qF", "-e", lit, "origin/main", "--", scr, test).returncode:
   177	                    why = f"which neither the script nor {test} carries on origin/main"
   178	                    fails.append(f'C10 rule sentence names {scr} beside the literal `{lit}`, {why}: "{sent[:60]}…"')
   179	    for sent in sentences:  # C9
   180	        if re.search(r"\b(once|until)\b", sent):
   181	            continue
   182	        for n in set(re.findall(C9_NAMES, sent)):
   183	            probe = n.replace("task-consistency-check ", f"{CHECKER}#").split("#")[0]
   184	            if probe.startswith("scripts/"):
   185	                ok = git(root, "cat-file", "-e", f"origin/main:{probe}").returncode == 0
   186	            elif probe.endswith("_EVIDENCE"):
   187	                ok = git(root, "grep", "-q", probe, "origin/main", "--", "scripts", "Makefile").returncode == 0
   188	            else:
   189	                mistakes = ("grep", "-q", "^classes:", "origin/main", "--", ".orchestration/learning/mistakes")
   190	                ok = probe == "classes:" and git(root, *mistakes).returncode == 0
   191	            if not ok:
   192	                why = "it is not on origin/main and the sentence has no landing condition"
   193	                fails.append(f'C9 rule sentence names {n} as present but {why}: "{sent[:70]}…"')
   194	    for r in rows:  # C13, then C11 on the form it found
   195	        d = str(r.get("disposition") or "")
   196	        form = next((f for f in FORMS if d.startswith(f)), None)
   197	        if form is None:
   198	            fails.append(f"C13 disposition is not closed:, residual: or out-of-scope: and a space: {d[:60]}")
   199	            continue
   200	        load = d[len(form) :]
   201	        if form == "closed: " and not re.fullmatch(r"tests/[\w./-]+::[A-Za-z_]\w*", load):
   202	            fails.append(f"C11 closed: payload is not tests/<path>::<identifier>: {load[:60]}")
   203	        tid_ok = re.fullmatch(r"[A-Za-z0-9][\w.-]*", load) and (root / f".orchestration/tasks/{load}.md").is_file()
   204	        if form == "out-of-scope: " and not tid_ok:
   205	            fails.append(f"C11 out-of-scope: {load[:60]} is not a task under .orchestration/tasks/")
   206	        if form == "residual: " and len(load) < 20:
   207	            fails.append(f"C11 residual: payload is shorter than 20 characters: {load}")
   208	    for a in allowed:  # C12: the concrete matches decide, not what the glob spells
   209	        if not re.search(r"[*?\[]", a) or a.startswith(("tests/fixtures/", own_dir)) or not confined(root, a):
   210	            continue
   211	        for f in filter(None, git(root, "ls-files", "-z", "--", f":(glob){a}").stdout.split("\0")):
   212	            named = any(re.search(re.escape(f) + r"(?=$|[ /\"'(),])", r.get("control") or "") for r in rows)
   213	            if applied(f) and not f.startswith(("tests/fixtures/", own_dir)) and not named:
   214	                fails.append(f"C12 the glob {a} matches {f}, which no threat_table row names")
   215	    premises = fm.get("premises") or []
   216	    # C14 executes premise commands only for the orchestrator's dispatched text, the bytes whose sha256 the caller
   217	    # passes (dispatch.sh: the TASK line's task_sha256); a branch copy at acceptance passes none, so nothing runs.
   218	    if premises and hashlib.sha256(data).hexdigest() != premises_sha:
   219	        fails.append(UNTRUSTED)
   220	        premises = []
   221	    for pre in premises:  # C14
   222	        cmd, want = str(pre.get("command") or ""), str(pre.get("output") if pre.get("output") is not None else "")
   223	        if re.search(r"\b(?:gh|curl)\b|https?://", cmd):
   224	            fails.append(f"{SKIPPED}: {cmd[:60]}")
   225	            continue
   226	        got, code, err = rerun(cmd, root)
   227	        # bash's own line, not exit 127: under pipefail `absent | grep -c` exits with grep's 1.
   228	        if absent := re.search(r"^bash: line \d+: ([^\s:]+): command not found$", err, re.M):
   229	            fails.append(f"{ABSENT} {absent.group(1)}: {cmd[:60]}")
   230	            continue
   231	        # Runs of whitespace collapse (BSD wc pads its counts; YAML's |- drops the final newline).
   232	        if got is None or " ".join(got.split()) != " ".join(want.split()):
   233	            fails.append(f"C14 premise output differs from its rerun: {cmd[:60]}")
   234	    design, mine = dr.get("design"), fm.get("invariants") if isinstance(fm.get("invariants"), dict) else {}
   235	    present = inside and not git(root, "cat-file", "-e", f"origin/main:{design}").returncode  # C8's probe
   236	    shown = git(root, "show", f"origin/main:{design}") if present else None
   237	    # C15: a design main cannot give leaves a task's invariants unchecked, and a path naming no design on main or in
   238	    # this checkout is a typo for any task; a design still in flight here assigns nothing yet to a task without any.
   239	    if inside and (not shown or shown.returncode):
   240	        fails += [f"C15 design {design} is not on origin/main"] if mine or not (present or inside.exists()) else []
   241	    elif shown:  # the design's assignment fixes the ids; a design task compares its own definitions
   242	        dfm = front(shown.stdout) if shown.stdout.startswith("---\n") else None
   243	        dfm = dfm if isinstance(dfm, dict) else {}
   244	        canon, assigned = dfm.get("invariants") or {}, dfm.get("implementing_tasks")
   245	        ids = (assigned.get(tid) or []) if isinstance(assigned, dict) and fm.get("kind") != "design" else None
   246	        if ids is not None:
   247	            fails += [f"C15 invariant {k} that {design} assigns to {tid} is missing" for k in ids if k not in mine]
   248	            fails += [f"C15 invariant {k} is not one {design} assigns to {tid}" for k in mine if k not in ids]
   249	        bad = [k for k, v in mine.items() if (ids is None or k in ids) and canon.get(k) != v]
   250	        fails += [f"C15 invariant {k} is not byte-equal to {design} on origin/main" for k in bad]
   251	    return fails
   252	
   253	
   254	def main():
   255	    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
   256	    parser.add_argument("--root", type=pathlib.Path, help="the repository (default: the first file's git toplevel)")
   257	    parser.add_argument("--premises-sha", metavar="sha256", help="the dispatched file's sha256; C14 runs only for it")
   258	    parser.add_argument("tasks", nargs="+", type=pathlib.Path, metavar="task.md")
   259	    args = parser.parse_args()
   260	    if args.root is None:
   261	        top = git(args.tasks[0].parent, "rev-parse", "--show-toplevel")
   262	        if top.returncode:
   263	            parser.error(f"{args.tasks[0]} is not in a git checkout; pass --root")
   264	        args.root = pathlib.Path(top.stdout.strip())
   265	    rc = 0
   266	    for p in args.tasks:
   267	        fails = check(p, args.root, args.premises_sha)
   268	        notes = [f for f in fails if f.startswith((SKIPPED, ABSENT, UNTRUSTED))]
   269	        bad = [f for f in fails if f not in notes]
   270	        print(f"{p.name}: {'FAIL' if bad else 'OK'}", *bad, sep="\n  ")
   271	        # The severity is explicit: an untrusted or absent-tool premise is a warning, a network premise a skip note.
   272	        severity = {n: "note" if n.startswith(SKIPPED) else "warning" for n in notes}
   273	        print(*(f"{p.name}: {severity[n]}: {n}" for n in notes), sep="\n", file=sys.stderr, end="\n" if notes else "")
   274	        rc |= bool(bad)
   275	    return rc
   276	
   277	
   278	if __name__ == "__main__":
   279	    sys.exit(main())

 succeeded in 201ms:
diff --git a/tests/unit/test_regime_ci.py b/tests/unit/test_regime_ci.py
index 452336a9..5db607bd 100644
--- a/tests/unit/test_regime_ci.py
+++ b/tests/unit/test_regime_ci.py
@@ -24,7 +24,7 @@ UV = [
 ]  # as regime.yml
 T = "t1-a01"
 ROWS = "".join(
-    f"  - control: {name}\n    disposition: residual\n"
+    f"  - control: {name}\n    disposition: 'residual: the compensating control of this fixture'\n"
     for name in (
         "the PR edits src/tool.sh",
         "the PR edits tests/unit/test_tool.py",
@@ -124,7 +124,10 @@ class RegimeCiTest(unittest.TestCase):
         # verifier and checker still decide, the checkout stays at the base, and no head program runs.
         fake = 'import pathlib\npathlib.Path("head-program-ran").write_text("x")\nprint("{line}")\n'
         scripts = {VERIFIER: fake.format(line="regime-ci: ok 1 task(s)"), CHECKER: fake.format(line="task.md: OK")}
-        rows = "".join(f"  - control: the PR edits {path}\n    disposition: residual\n" for path in scripts)
+        rows = "".join(
+            f"  - control: the PR edits {path}\n    disposition: 'residual: the compensating control of this fixture'\n"
+            for path in scripts
+        )
         policy = TASK.replace("threat_table:\n", "threat_table:\n" + rows).replace("at most 3 ", "at most 999 ")
         policy = policy.replace("  - src/tool.sh\n", "  - src/tool.sh\n" + "".join(f"  - {path}\n" for path in scripts))
         forged = policy.replace("  - src/tool.sh\n", "  - src/tool.sh\n  - stray.sh\n")
@@ -262,7 +265,10 @@ class RegimeCiTest(unittest.TestCase):
     def test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr(self):
         result = self.build()
         self.assertEqual((0, "regime-ci: ok 1 task(s)\n"), (result.returncode, result.stdout), result.stderr)
-        no_row = TASK.replace("  - control: the PR edits src/tool.sh\n    disposition: residual\n", "")
+        no_row = TASK.replace(
+            "  - control: the PR edits src/tool.sh\n    disposition: 'residual: the compensating control of this fixture'\n",
+            "",
+        )
         crash = TASK.replace("threat_table:\n", "threat_table:\n  - a row that is no mapping\n")
         worded = TASK.replace("changed lines outside", "changed lines (added plus deleted) outside")
         four = CODE | {"src/tool.sh": "a\nb\nc\nd\n"}
@@ -358,8 +364,8 @@ class RegimeCiTest(unittest.TestCase):
         # Amendment 1: a later copy whose reset_of names an earlier one is the lineage's only target; the earlier copy
         # warns, and its own .orchestration/ paths are no stray of the later one. Without reset_of, both are targets.
         later = "t1-a02"
-        rows = f"  - control: the predecessor copy .orchestration/{T}/task.md\n    disposition: residual\n"
-        rows += f"  - control: the task copy .orchestration/{later}/task.md\n    disposition: residual\n"
+        rows = f"  - control: the predecessor copy .orchestration/{T}/task.md\n    disposition: 'residual: the compensating control of this fixture'\n"
+        rows += f"  - control: the task copy .orchestration/{later}/task.md\n    disposition: 'residual: the compensating control of this fixture'\n"
         reset = TASK.replace(T, later).replace("allowed_files:", f"reset_of: [{T}]\nallowed_files:")
         reset = reset.replace("threat_table:\n", "threat_table:\n" + rows)
         for text, expected, kept in ((reset, 0, True), (reset, 0, False), (TASK.replace(T, later), 1, True)):
diff --git a/tests/unit/test_task_checkers.py b/tests/unit/test_task_checkers.py
index 7e2f9583..9be57a5a 100644
--- a/tests/unit/test_task_checkers.py
+++ b/tests/unit/test_task_checkers.py
@@ -81,8 +81,8 @@ class TaskCheckersTest(unittest.TestCase):
         c2467, c467, c23467 = {"C2", "C4", "C6", "C7"}, {"C4", "C6", "C7"}, {"C2", "C3", "C4", "C6", "C7"}
         expected = {"process-rules-a01": {"C2", "C6"}, "process-rules-a05": c467, "process-rules-a06": c467}
         expected |= dict.fromkeys(["process-rules-a02", "process-rules-a03", "process-rules-a04"], c2467)
-        expected |= dict.fromkeys(["regime-counters-a01", "ci-skip-orchestration-a01"], c2467)
-        expected |= dict.fromkeys(["regime-counters-a02", "ci-skip-orchestration-a02"], c23467)
+        expected |= dict.fromkeys(["regime-counters-a01", "ci-skip-orchestration-a01"], c2467 | {"C11", "C15"})
+        expected |= dict.fromkeys(["regime-counters-a02", "ci-skip-orchestration-a02"], c23467 | {"C11", "C15"})
         expected = {f"dotfiles-T128-{t}.md": ids for t, ids in expected.items()}
         self.assertEqual(expected, self.failing_checks(*files, root=ROOT))
 
@@ -198,7 +198,13 @@ class TaskCheckersTest(unittest.TestCase):
         for after in (".bak", "", " and its test", "/task.md", ") and more", '" and more', ", and more", "* and more"):
             with self.subTest(after=after):
                 path = self.task(
-                    uncovered=("scripts/foo.py",), rows=[{"control": f"the PR adds scripts/foo.py{after}"}]
+                    uncovered=("scripts/foo.py",),
+                    rows=[
+                        {
+                            "control": f"the PR adds scripts/foo.py{after}",
+                            "disposition": "residual: a compensating control",
+                        }
+                    ],
                 )
                 found = self.failing_checks(path, root=self.temp, code=1 if after == ".bak" else 0)[path.name]
                 self.assertEqual({"C4"} if after == ".bak" else set(), found)
     1	---
     2	threat_table:
     3	  - control: "the task-file copy on the branch (.orchestration/<task_id>/task.md)"
     4	    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
     5	  - control: "the branch evidence records under .orchestration/<task_id>/ (report.md, validation.md, sandbox.md, learning.md)"
     6	    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
     7	  - control: "task metadata (the front matter of the task copy: kind, security, allowed_files, threat_table, premises)"
     8	    disposition: "residual: read with PyYAML by the task-consistency check before dispatch and at acceptance; a changed field fails the byte comparison above"
     9	  - control: "metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)"
    10	    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
    11	  - control: "in-process effects"
    12	    disposition: "residual: draft from the generator; the tests run the task's scripts as subprocesses in temporary repositories, and nothing writes outside the worktree, the evidence directory and $TMPDIR"
    13	  - control: "workflow and interpreter or environment inputs"
    14	    disposition: "residual: draft from the generator; no workflow or interpreter file is in allowed_files unless the rows above name it, and Python runs under python -I through uv"
    15	  - control: "new or renamed scripts"
    16	    disposition: "residual: draft from the generator; every new or renamed script is named in allowed_files and listed in the RESULT, and any other is an undeclared change the audit fails"
    17	  - control: "orchestrator effect merge"
    18	    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
    19	  - control: "orchestrator effect update-branch"
    20	    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
    21	  - control: "orchestrator effect forced worker removal"
    22	    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
    23	check:
    24	  - make unit-test
    25	  - make format
    26	---
    27	
    28	# The task template of scripts/orchestrator/task-from-plan.py
    29	
    30	The generator reads this file, never a task record: the control rows above (`<task_id>` replaced), the common Check commands (each run once on origin/main beside the program items' `make` targets) and the Completion section below, which carries the inherited Completion contract of the regime's code tasks.
    31	
    32	## Completion
    33	
    34	One PR from a fresh branch off `origin/main` (no other merge is a precondition). The PR is ready for the orchestrator's integration when the ruleset's required checks are green, the Bot's review of the final head is in (at PR open, and once more on `@codex review` after a P0/P1 fix round: plan 020 step 2), every Bot thread is replied to and resolved by the orchestrator with its disposition, the validation file carries the Check's outputs, and the RESULT names every P0/P1 thread with `fixed:<sha>` and every P2 thread with the disposition the worker proposes; the orchestrator's audit of the final head is dispositioned finding by finding before the gate, and a P0/P1 it leaves is the operator's decision. The Bot's P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P0 or P1 that survives the round is listed as `open:<thread id>` with `bot_rounds=2`, stops the PR and goes to the operator as a decision; a P2 of the Bot's first review on this PR's own change whose fix stays within `allowed_files` and is small is fixed in a revise round the orchestrator sends with a `check=` while INV-6's counts allow it (every fix round, before or after the first RESULT, counts toward INV-6's cap of two); the third finding of one class on this PR stops the rounds until the orchestrator's `re-plan:` line; a later review's P2 and every P3 are advisory, as is any other P2, owned by `<task_id>-followup-a01`, which the orchestrator writes when the first advisory P2 appears, before the PR's dispositions, and recorded under `## Owned by <task_id>-followup-a01` in this task's acceptance record. The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`. The RESULT names head, base, branch, files, every Bot thread with its disposition, the test names, the caps, `task_copy=<sha256 of .orchestration/<task_id>/task.md>` and the evidence paths.

 exited 1 in 795ms:
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
ls: .orchestration/reports/dotfiles-T133-task-generator-plan-check-a02.md: No such file or directory
ls: .orchestration/sandboxes/dotfiles-T133-task-generator-plan-check-a02.md: No such file or directory
ls: .orchestration/validation/dotfiles-T133-task-generator-plan-check-a02.md: No such file or directory

**Handling fallback for web and GitHub errors**
exec
/bin/zsh -lc "python3 -B -c 'import json,pathlib; d=json.loads(pathlib.Path(\".orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-pr-feedback.json\").read_text()); print(json.dumps(d,indent=2))'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc 'git show 8a09b9365932f23b09df8aa2385a93d0b3016a3e:.orchestration/dotfiles-T133-task-generator-plan-check-a02/report.md | nl -ba && git show 8a09b9365932f23b09df8aa2385a93d0b3016a3e:.orchestration/dotfiles-T133-task-generator-plan-check-a02/measure.md | nl -ba && git show 8a09b9365932f23b09df8aa2385a93d0b3016a3e:.orchestration/dotfiles-T133-task-generator-plan-check-a02/sandbox.md | nl -ba' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc 'git show 8a09b9365932f23b09df8aa2385a93d0b3016a3e:tests/unit/test_task_from_plan.py | nl -ba' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 187ms:
     1	---
     2	task_id: dotfiles-T133-task-generator-plan-check-a02
     3	round: 1
     4	reset_of: dotfiles-T133-task-generator-plan-check-a01
     5	status: result
     6	---
     7	
     8	# Report
     9	
    10	Worker `claude-standard-dot-a009` (Claude Code, worker-c).
    11	
    12	- Branch `tools/task-generator-plan-check-a01`, PR #417, continued from 9da0ed3fe67fd1f9267c56fcdcb7e5aaaaa9ffab. Base `origin/main` is 3e41e36a, which 9da0ed3f already merges.
    13	- Commits:
    14	  - 6da92853: the task-copy swap. `git rm` of the a01 copy, and the byte-identical a02 copy (sha256 `a3ab8ea6addda207fa9a9ff5d96921e080dab7a1025117f33cbd087e6b805f98`).
    15	  - eb20d063: the implementation and its tests.
    16	  - 6e07d291: the one correction round after the worker's pre-push review. It is the code head.
    17	  - The evidence commit is last.
    18	- INV-6 for a02: amendments=0, questions=0, revises=0. The a01 history, its acceptance records and its counters stay as recorded, including the C14 revise, which counts as the second amendment in substance (item 7).
    19	- The worker's pre-push review: one round (below).
    20	
    21	## What changed
    22	
    23	### `scripts/orchestrator/task-from-plan.py` (items 1, 5, 6, 12 to 15)
    24	
    25	- **Bundled template (items 1, 5):** `scripts/orchestrator/task-template.md`, beside the generator, supplies:
    26	  - the ten control rows: the task copy, the evidence records, task metadata, metadata separators, in-process effects, workflow and interpreter or environment inputs, new or renamed scripts, and the three orchestrator effects, with `<task_id>` replaced;
    27	  - the default Check (`make unit-test`, `make format`);
    28	  - the full Completion paragraph, with `<task_id>-followup-a01` as the owner of any advisory P2 and `task_copy=<sha256 of .orchestration/<task_id>/task.md>`.
    29	
    30	  No file under `.orchestration/tasks/` is read. The sibling-task Check lookup, the row-template task and the Completion-record file are gone.
    31	- **Clean-plan gate (item 6):** before anything runs or is written, `git status --porcelain=v1 --untracked-files=all -- ':(glob).orchestration/plans/024-*'` must print nothing and exit 0. Otherwise the generator exits with `task-from-plan: refused: the plan group has uncommitted changes; commit them first:` and the status lines. Every plan file is read with `git show <HEAD>:<path>`, so the executed command text is the committed text. The revision is named in the task's opening line (`read from the plan group at <sha>`).
    32	- **Wave selection (item 12):** the seat's cell, or the whole row without `--seat`, must hold the todo id as a whole token, `(?<![\w-])P1-1(?![\w-])`. `P1-10`, `P1-11` and `P1-1a` never match `P1-1`.
    33	- **Scopes (item 13):** a backticked first word with `/`, inside the checkout (the checker's `confined`), not starting with `-` or `~`, is proposed:
    34	  - a literal has a file extension or exists;
    35	  - a glob stays as written.
    36	
    37	  Each executed or applied file a glob matches (`git ls-files :(glob)…`, the checker's own `applied()`, outside `tests/fixtures/`) gets a concrete row, `<file> (matched by <glob>)`. A match that is itself an allowed entry keeps only its own row, so no row names two entries (C7b). `git grep -l -F -e <name>` provenance stays in Files as `# from:`.
    38	- **Program items (item 14):** an item runs from its `**(<n>) ` line to the next `**(<m>) ` line or the end of the file, so blank lines, fenced blocks and later paragraphs stay inside it.
    39	- **Commands by form (item 15):** a span is a command when:
    40	  - its first word is a lowercase name, a `/` or `./` path, or a `.sh` or `.py` path;
    41	  - it holds no `<placeholder>`.
    42	
    43	  Execution decides the rest, with stdin from `/dev/null` (the checker's `rerun`): an absent executable stays a premise, `verify: \`cmd\` exits 127`. Redirects stay. A lone word counts only when PATH holds it, since a lone `residual` or `kind` is prose, and a lone path is a scope. `make …` spans go to the Check; the others are premises, run through the checker's `rerun`. A gh, curl or URL command is a `verify:` not-run premise with an empty output.
    44	- **Check:** each command, the template's plus the items' `make` spans, runs once in a detached scratch worktree of `origin/main`. It is pasted as ``- `cmd`: exit N on origin/main <rev12>``, followed by a fenced tail of its last 20 output lines. The worktree is removed with `git worktree remove --force` and its temporary parent deleted.
    45	- The generator still runs the checker on the written file with `--premises-sha` of those bytes, the generator's own text whose premises it has just run.
    46	
    47	### `scripts/orchestrator/task-consistency-check.py` (items 2, 7 to 10, 19, 20)
    48	
    49	- **C14 (items 7, 8):** the sha gate is kept, so premises run only for the file whose sha256 `--premises-sha` names. Without it the file gets `<file>: warning: C14: not run (no trusted sha)` on stderr. Absent tools are `<file>: warning: C14: tool absent …`, and skipped network premises `<file>: note: C14 skipped network premise …`. Stdout, and with it the finding format, is unchanged.
    50	- **C15 (item 9):** the assignment comes from the design on `origin/main`, for tasks with or without `invariants`:
    51	  - `implementing_tasks` as a map from task to ids: each assigned id the task lacks is `C15 invariant <id> that <design> assigns to <task> is missing`, and each id it carries but was not assigned is `C15 invariant <id> is not one <design> assigns to <task>`;
    52	  - the list form (T124, T126) names no ids per task and so assigns none;
    53	  - the sentences of the ids in force must be byte-equal, as before;
    54	  - `C15 design <design> is not on origin/main` is reported in two cases. Existence comes from C8's `git cat-file -e origin/main:<design>` probe.
    55	    - For a task that carries invariants, when origin/main cannot give the design.
    56	    - For any task, when the path names no design on origin/main or in the checkout, so a mistyped path never skips the check.
    57	
    58	    The one exemption is a design that exists only in this checkout, for a task without invariants: it assigns nothing yet. See "Observations".
    59	  - A design without front matter assigns nothing instead of raising.
    60	- **C12 (items 10, 19):** each glob entry's `git ls-files :(glob)` matches decide, whatever the glob spells. An executed or applied match (`*.sh *.py *.yaml *.yml *.json *.toml`, or a path under `home/`, `scripts/`, `.githooks/` or `.github/`) needs a row naming it. `tests/fixtures/` and the task's own evidence directory stay exempt.
    61	- **C10 and C6 (item 20):**
    62	  - C10 passes each backticked literal as `git grep -qF -e <literal>`, so `--open-files-in-pager=<cmd>` is searched for and nothing runs;
    63	  - a rule sentence's script path outside `--root` is `C10 rule sentence names <path>, a path outside the checkout`;
    64	  - C6 reads a design path only inside the checkout, and `C6 design path <path> is outside the checkout` otherwise. C15 reuses the same confined path.
    65	
    66	### `scripts/orchestrator/plan-check.py` (items 3, 11, 16 to 18)
    67	
    68	- **F2 (item 11):** each task's allowed list becomes its literals plus the files each glob matches in the tree (`glob.glob(…, recursive=True, include_hidden=True)`). Two lists overlap on:
    69	  - a shared path;
    70	  - a path inside the other's directory;
    71	  - a literal the other's glob matches (`fnmatchcase`), for a file not yet in the tree.
    72	
    73	  Two glob spellings are never compared. The finding names the first shared path.
    74	- **Acceptance drift (item 16):** a progress row's task takes its latest `AGMSG-ACCEPTANCE v1 … task_id=<task> … status=<[\w-]+>` event.
    75	  - Each event on a line is read up to the next one, so another task's event never lends its status.
    76	  - Events are ordered by the last ISO timestamp before the event on its line. An untimed event carries the latest timestamp above it, then position decides.
    77	  - Records without timestamps keep textual order.
    78	- **PR drift (item 17):** every sha or state word that starts within 40 characters after a `#<pr>`, before the next `#`, is compared on its own, deduplicated per line.
    79	- **Invariants (item 18):** `ANTHROPIC_OAUTH_TOKEN=` followed by a non-empty `"…"`, `'…'` or bare value is a finding. `""` and `''` are not. The finding never carries the value.
    80	
    81	## Item 19: ownership
    82	
    83	The audit of 9da0ed3 (P2, finding 15) assigned the C12 remedy to the advisory owner `dotfiles-T133-task-generator-plan-check-followup-a01`. Item 10 of this task now owns it:
    84	- selector: `tests/unit/test_task_consistency_c11_c15.py::test_c12_classifies_concrete_glob_matches_before_the_glob_spelling`;
    85	- fix: eb20d063.
    86	
    87	The orchestrator records the corrected ownership and withdraws the remedy from the follow-up task. Findings 1 to 14 of that audit are likewise fixed here under items 5 to 18.
    88	
    89	## Tests
    90	
    91	New, each red against 9da0ed3f with this branch's test source and green on the final head (validation.md):
    92	
    93	| Item | Test |
    94	| --- | --- |
    95	| 5 | `tests/unit/test_task_from_plan.py::test_generator_uses_the_bundled_template_without_task_records` |
    96	| 6 | `tests/unit/test_task_from_plan.py::test_generator_refuses_dirty_plan_commands_before_execution` |
    97	| 12 | `tests/unit/test_task_from_plan.py::test_wave_selection_matches_whole_todo_ids` |
    98	| 13 | `tests/unit/test_task_from_plan.py::test_generator_preserves_wildcard_scopes_and_their_threat_rows` |
    99	| 14 | `tests/unit/test_task_from_plan.py::test_program_item_continues_until_the_next_numbered_heading` |
   100	| 15 | `tests/unit/test_task_from_plan.py::test_generator_retains_unavailable_single_word_and_redirecting_commands` |
   101	| 11 | `tests/unit/test_plan_check.py::test_f2_detects_intersecting_globs_through_concrete_tree_matches` |
   102	| 16 | `tests/unit/test_plan_check.py::test_drift_uses_the_latest_timestamped_acceptance_for_the_same_task` |
   103	| 17 | `tests/unit/test_plan_check.py::test_drift_checks_every_sha_and_state_for_each_pr_occurrence` |
   104	| 18 | `tests/unit/test_plan_check.py::test_invariants_reject_nonempty_quoted_oauth_token_assignments` |
   105	| 8 | `tests/unit/test_task_consistency_c11_c15.py::test_c14_without_a_trusted_sha_reports_an_explicit_warning` |
   106	| 9 | `tests/unit/test_task_consistency_c11_c15.py::test_c15_requires_the_design_assigned_invariant_id_set` |
   107	| 10, 19 | `tests/unit/test_task_consistency_c11_c15.py::test_c12_classifies_concrete_glob_matches_before_the_glob_spelling` |
   108	| 20 | `tests/unit/test_task_consistency_c11_c15.py::test_c10_never_passes_a_literal_as_a_git_grep_option` |
   109	| 20 | `tests/unit/test_task_consistency_c11_c15.py::test_c6_confines_design_paths_to_the_checkout` |
   110	
   111	Retained, item 7: `tests/unit/test_task_consistency_c11_c15.py::test_c14_executes_premise_commands_only_for_the_dispatched_sha`, red at ff4d25a8, the revision before the gate. Its no-sha expectation now carries item 8's `warning:` prefix.
   112	
   113	Retained end-to-end tests (item 4), each changed only where the a02 behaviour changes:
   114	
   115	- `test_task_from_plan.py::test_a_generated_task_passes_the_consistency_check_and_pastes_real_premise_outputs` now expects:
   116	  - the bundled control rows, with no `dotfiles-T133-result-precheck-a01` text;
   117	  - the Check line ``- `make unit-test`: exit 0 on origin/main <rev12>``;
   118	  - a failed premise claim starting `verify:` with `exits 3`.
   119	
   120	  The fixture still commits the legacy task records the a01 generator needed. That way each new regression is red against 9da0ed3 for the reason it names, not for a missing file. The legacy rows' dispositions are at least 20 characters, so the a01 generator's output does not fail C11 first.
   121	- `test_plan_check.py::test_plan_check_reports_each_form_drift_and_invariant_violation_once_and_passes_a_clean_plan`: the F2 glob subtest now names the concrete shared path, `share scripts/two.py`.
   122	- `test_task_consistency_c11_c15.py::test_each_new_check_is_red_on_its_fixture_and_the_existing_checks_are_unchanged`: the absent-tool expectation carries the `warning:` severity. Its subprocess calls carry explicit `check=` flags.
   123	- `tests/unit/test_task_checkers.py` is unchanged by a02. It carries only amendment 1's two edits from a01, and its historical expected sets stand: C11 and C15 only on regime-counters and ci-skip.
   124	
   125	## Real runs (validation.md)
   126	
   127	- **The checker:** run with the code head 6e07d291 on the main checkout's 29 `dotfiles-T133-*.md` files, with `--root <main checkout>` (at 740772ef, after #416) and without a sha, it exits 0.
   128	  - Stdout: 29 `OK`. C1 to C13, C15 and C7b found nothing.
   129	  - Stderr: 20 `warning: C14: not run (no trusted sha)` lines, one per file with premises. C14 executed nothing and is recorded as not run, not as passed.
   130	  - The run on eb20d063, before the correction, gave the same result over the 24 files that existed then.
   131	- **`plan-check.py`:** run once against the main checkout, on eb20d063's code, it exits 1 with six violations. The correction round changed only `--drift`'s acceptance reading, which this flagless run does not use. They are the same six a01 reported, left for the orchestrator:
   132	  - F3 (P1-13, P1-14);
   133	  - F4 (P1-a);
   134	  - three F6 citing `dotfiles-T131-claude-pinned-merge-gate-fix-a01`.
   135	
   136	  No F2 overlap appears with concrete scopes.
   137	
   138	## Observations for the orchestrator (no change made)
   139	
   140	- **Dispatch wiring (item 8's owner):** `scripts/orchestrator/dispatch.sh:238` runs `task-consistency-check.py --root "${root}" "${tf}"` without `--premises-sha`. So C14 never runs at dispatch, and its `2>&1` capture prints the warning only when the check fails. The needed change is `--premises-sha "$(value_of task_sha256)"` plus forwarding the stderr warning on success. Both belong to the P1-5 to P1-6 dispatch lineage, as item 8 states.
   141	- **C15 and a missing design:** the item 2 text says a missing named design produces a finding. The checker reports it in every case but one: a design that exists only in this checkout, for a task without invariants.
   142	  - That exemption exists because `tests/unit/test_task_checkers.py`'s fixtures are such tasks: their stub `git` answers `cat-file -e` and exits 99 on `show`, or the design exists only in the fixture root. That module may carry only amendment 1's two edits.
   143	  - The unconditional finding turned its C4, C9, complete-file and historical tests red.
   144	  - A mistyped path, absent everywhere, is a finding, which was the review's P2.
   145	
   146	  If the orchestrator wants the strict reading for in-flight designs too, the fixture module needs an amendment.
   147	- **Lone-word premises:** the real plan quotes field names such as `head` and `security` as lone backticked words. Item 15's lone-word rule runs them as draft premises. With stdin closed, `head` prints nothing and `security` prints its usage with `verify: … exits 2`. The orchestrator deletes such rows from the generated draft, which stays for editing.
   148	- **The plan group is untracked:** `.orchestration/plans/024-*` exists only untracked in the main checkout, so item 6's gate refuses to generate there until the group is committed. That is intended.
   149	- **Network-free does not mean harmless:** the generator, and C14 at dispatch, run every recognised command in a program item; only gh, curl and URL commands are skipped. A program item quoting a write such as `git push …` would run in the orchestrator's sandbox. That is item 6's stated contract for the orchestrator's own committed text, but the skip list is narrow.
   150	
   151	[memory:decision] T133 P1-12 a02: task-from-plan.py reads only scripts/orchestrator/task-template.md (no .orchestration/tasks/), refuses a dirty .orchestration/plans/024-* group before running or writing, reads the plan at HEAD, and recognises commands by form; plan-check F2 and checker C12 decide on concrete tree matches; C14 without a trusted sha is a stderr warning; C15 compares the design-assigned invariant id set; C10 passes literals after git grep -e and C6/C10 paths stay in the checkout.
   152	
   153	## Pre-push review
   154	
   155	One round, on eb20d063, by a fresh read-only subagent: `Verdict: incorrect`, two P2 and four P3, each reproduced. The record and its receipt are `dotfiles-T133-task-generator-plan-check-a02-worker-crit.json` and `…-worker-review-receipt.md` here. All six are fixed in the one correction round, 6e07d291:
   156	
   157	- **P2, `plan-check.py` `latest()`:** another task's event on the same line lent its status, timed lines outranked every untimed one, and a trailing backtick stayed in the status. It now reads each event separately, carries timestamps, and captures `[\w-]+`.
   158	  - Regression: `test_drift_uses_the_latest_timestamped_acceptance_for_the_same_task`, red against eb20d063 (`accepted != withdrawn`` `).
   159	- **P2, C15 missing design:** a mistyped path skipped the check. Existence now comes from `cat-file -e`, and a path absent everywhere is a finding for any task.
   160	  - Regression: `test_c15_requires_the_design_assigned_invariant_id_set`, case `a mistyped design`, red against eb20d063.
   161	- **P3, `rerun` stdin:** a lone `head` premise waited on the caller. It now gets `stdin=subprocess.DEVNULL`.
   162	- **P3, the generator's output failed C7b:** a glob over a literal entry gave a second row. It is fixed, and `test_generator_preserves_wildcard_scopes_and_their_threat_rows` adds `scripts/*.sh` over the literal `scripts/demo.sh`; red against eb20d063.
   163	- **P3, C15 on a design without front matter:** it is parsed only when it opens with `---`.
   164	- **P3, test gaps:**
   165	  - item 17 now has a repeated PR with several tokens per occurrence;
   166	  - C12's own-directory exemption has a real tracked file.
   167	
   168	  Both pass against eb20d063, because they fill gaps rather than show defects, and both are red against 9da0ed3.
   169	
   170	A first attempt at the review read worker-c directly and was stopped, before reporting anything, when the orchestrator's #411 revise needed the worktree (sandbox.md). It is not counted as a round.
   171	
   172	## Feedback dispositions
   173	
   174	The Bot's review of a01 (5562936729, on 35c66022) left three threads on PR #417. Each gets its root-cause disposition; the orchestrator replies and resolves:
   175	
   176	- **4306960622 [P1] Sandbox premise commands before executing them** (`task-consistency-check.py:75`): fixed:538e60bd.
   177	  - The checker executes premises only for the file whose sha256 `--premises-sha` names, the orchestrator's dispatched text. A PR-controlled copy at acceptance has no trusted sha, so nothing runs; it gets item 8's warning.
   178	  - a02 keeps this gate (item 7; red at ff4d25a8, green here) and closes stdin in 6e07d291. The generator runs only committed plan text (item 6).
   179	- **4306960626 [P1] Bundle the required task template** (`task-from-plan.py:131`): fixed:eb20d063.
   180	  - The template is `scripts/orchestrator/task-template.md`, and nothing under `.orchestration/tasks/` is read (item 5).
   181	  - Regression: `test_generator_uses_the_bundled_template_without_task_records`, which deletes `.orchestration/tasks/` from the fixture.
   182	- **4306960630 [P2] Resolve globs before checking wave overlaps** (`plan-check.py:89`): fixed:eb20d063. F2 compares concrete tree matches, plus literals a glob matches (item 11).
   183	  - The Bot's case, `scripts/*.py` against a literal `scripts/two.py`, is the retained F2 glob subtest.
   184	  - Two intersecting globs are `test_f2_detects_intersecting_globs_through_concrete_tree_matches`.
   185	
   186	The task-level audit of 9da0ed3 (three P1, twelve P2) is dispositioned item by item above: items 5 to 19, plus item 20's PR #418 review.
   187	
   188	This push: no `@codex review` is posted. CI on the final head and the 15-minute Bot window are in the RESULT line.
   189	
   190	## Amendment 1: the CI-repair round
   191	
   192	The chain update-branched PR #417 onto main b22a5580 (63b6acae). The regime verifier from PR #418 now runs this task's checker on the fixtures in `tests/unit/test_regime_ci.py`. Their threat rows carried a bare `disposition: residual`, which C13 refuses (and C11, as a payload under 20 characters). Three regime tests failed in CI and five locally (validation.md).
   193	
   194	Commit eb0b1c06 gives each of the five fixture rows `'residual: the compensating control of this fixture'` and copies amendment 1's task text. No expected output and no production file changes.
   195	
   196	- The regime tests are red on 63b6acae.
   197	- 101 tests across the regime, task and orchestrator-tool modules are green on eb0b1c06.
   198	- Caps against the new merge base: 659 of 700 outside `tests/` and 673 of 800 under `tests/`.
   199	
   200	This is one CI-repair round under C-61. The worker's pre-push review round of a02 is unchanged.
     1	---
     2	task_id: dotfiles-T133-task-generator-plan-check-a02
     3	round: 1
     4	code_head: 6e07d29193e9a3b56b299dd9d55538788bc48b7b
     5	merge_base: 3e41e36abc949acd7e6b4859c1a22df9e665c8d4
     6	---
     7	
     8	# Measure
     9	
    10	`git diff --numstat origin/main...HEAD` on the code head. The totals cover the whole PR, including the inherited a01 changes and the bundled template. Changed lines are additions plus deletions.
    11	
    12	| Scope | Changed lines | Cap |
    13	| --- | --- | --- |
    14	| outside `tests/` and `.orchestration/` | 659 | 700 |
    15	| under `tests/` | 657 | 800 |
    16	| under `.orchestration/` (not capped) | 982 | — |
    17	
    18	Changed files outside `.orchestration/`:
    19	
    20	| Added | Deleted | File |
    21	| --- | --- | --- |
    22	| 232 | 0 | `scripts/orchestrator/plan-check.py` |
    23	| 140 | 11 | `scripts/orchestrator/task-consistency-check.py` |
    24	| 242 | 0 | `scripts/orchestrator/task-from-plan.py` |
    25	| 34 | 0 | `scripts/orchestrator/task-template.md` |
    26	| 166 | 0 | `tests/unit/test_plan_check.py` |
    27	| 9 | 3 | `tests/unit/test_task_checkers.py` (amendment 1's two edits, from a01) |
    28	| 265 | 0 | `tests/unit/test_task_consistency_c11_c15.py` |
    29	| 214 | 0 | `tests/unit/test_task_from_plan.py` |
    30	
    31	Under `.orchestration/`:
    32	- the a01 evidence records, kept as history;
    33	- the a02 task copy;
    34	- this directory's records, added by the evidence commit.
    35	
    36	The a01 task copy is deleted in 6da92853. Numstat against the merge base does not list it, because main never had it.
    37	
    38	The review measured 651 and 647 on eb20d063. The correction round added 8 lines outside `tests/` and 10 under it.
     1	---
     2	task_id: dotfiles-T133-task-generator-plan-check-a02
     3	round: 1
     4	---
     5	
     6	# Sandbox
     7	
     8	Claude Code seat `claude-standard-dot-a009`, in its own worktree `.claude/worktrees/worker-c`, with the Bash sandbox on (macOS Seatbelt) in auto mode. Branch `tools/task-generator-plan-check-a01` continues PR #417 from 9da0ed3f, as the a02 Completion directs.
     9	
    10	Inside the sandbox:
    11	
    12	- Every edit, and the task-copy swap: `git rm` of the a01 copy, then the a02 copy taken from the main checkout's dispatched text, which was only read.
    13	- The red replays, each in a scratch worktree of the reviewed production commit (9da0ed3f, and ff4d25a8 for the C14 gate) with this branch's test modules copied in, each removed with `git worktree remove --force`.
    14	- The four task modules, `test_orchestrator_tools` and `test_agmsg_orchestration_docs`.
    15	- `make unit-test` and `make format` on the branch, and the same two on a pristine detached worktree of `origin/main` 3e41e36a, which was then removed.
    16	- The checker and `plan-check.py`, each run against the main checkout with `--root`, because the plan 024 group and the T133 task files exist only untracked there. They only read it; the checker run carries no `--premises-sha`, so it executed nothing.
    17	- `git fetch origin`, and the push, with `-c url.https://github.com/mryfmo/.pushInsteadOf=https://github.com/mryfmo/`.
    18	
    19	Permission-gated or outside the sandbox:
    20	
    21	- `gh pr checks`, `gh pr view` and the Bot listing (Worker Playbook step 4).
    22	- `agmsg-dispatch` for the RESULT.
    23	
    24	Each `gh` command and each git write runs as a single command; no `@codex review` comment is posted.
    25	
    26	Interruption: the orchestrator's revise of PR #411 arrived mid-task with `next_action=... before-continuing-P1-12-a02`.
    27	
    28	- The a02 work was committed locally (6da92853 and eb20d063, not pushed) before the switch.
    29	- The suite runs that read this worktree finished first.
    30	- The first self-review agent read this worktree and could not move to a scratch worktree in time. It was stopped before it reported any finding.
    31	- Worker-c then switched to `tools/result-precheck-a01` for the #411 round and switched back afterwards. Each `git checkout` was a single command on a clean tree.
    32	- The relaunched review worked in its own scratch worktree of eb20d063 from the start.
    33	
    34	`make unit-test` fails inside the sandbox on sandbox-denied operations. The failing set is identical to a pristine `origin/main` worktree's in the same sandbox (validation.md), so CI decides the full suite.
    35	
    36	effects=none

 succeeded in 203ms:
     1	"""Exercise task-from-plan.py on a committed fixture plan group in a temporary repository with a bare origin.
     2	
     3	The fixture also commits the task records the a01 generator needed (a row template and a Completion file), so each
     4	regression below is red against that generator for the reason it names; the a02 generator reads none of them.
     5	"""
     6	
     7	import json
     8	import os
     9	import shutil
    10	import subprocess
    11	import tempfile
    12	import unittest
    13	from pathlib import Path
    14	
    15	ROOT = Path(__file__).resolve().parents[2]
    16	GENERATOR = ROOT / "scripts/orchestrator/task-from-plan.py"
    17	GIT_ENV = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
    18	PROGRAMS = ".orchestration/plans/024-design-programs.md"
    19	WAVES = ".orchestration/plans/024-omp-cutover-and-corrective-order.md"
    20	LEGACY_ROWS = (
    21	    "the task-file copy on the branch (.orchestration/dotfiles-T133-result-precheck-a01/task.md)",
    22	    "the branch evidence records under .orchestration/dotfiles-T133-result-precheck-a01/ (report.md, validation.md)",
    23	    "task metadata (the front matter of the task copy)",
    24	    "metadata separators (the --- lines)",
    25	    "in-process effects",
    26	    "workflow and interpreter or environment inputs",
    27	    "new or renamed scripts",
    28	    "orchestrator effect merge",
    29	    "orchestrator effect update-branch",
    30	    "orchestrator effect forced worker removal",
    31	)
    32	LEGACY = {  # what the a01 generator read under .orchestration/tasks/; the a02 generator reads none of it
    33	    ".orchestration/tasks/dotfiles-T133-result-precheck-a01.md": "---\nformat: 2\nthreat_table:\n"
    34	    + "".join(
    35	        f"  - control: {json.dumps(c)}\n    disposition: {json.dumps('residual: the legacy wording of ' + c)}\n"
    36	        for c in LEGACY_ROWS
    37	    )
    38	    + "---\n",
    39	    ".orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md": "---\nformat: 2\n---\n\n## Completion\n\nOne PR.\n",
    40	}
    41	FILES = {
    42	    ".orchestration/plans/024-todo.md": "| # | 目的 | やること | 完了条件 |\n| --- | --- | --- | --- |\n"
    43	    "| P1-1 demo generator | B1 a demo purpose | (1) で作る | the generated task passes the consistency check |\n",
    44	    PROGRAMS: "# programs\n\n**(1) `scripts/demo.sh`**: prints `printf known-output` and checks `sh -c 'exit 3'`.\n\n"
    45	    "**(2) other**: unused\n",
    46	    ".orchestration/plans/024-design-quality.md": "| id | row |\n| --- | --- |\n| Q-A 境界 | P1-1 のタスクは security: true |\n",
    47	    WAVES: "## 6. 波\n\n| 波 | a009 | a008 |\n| --- | --- | --- |\n| P-W0 | P1-1 demo | P1-2 sibling |\n\n## 7. STOP\n",
    48	    "scripts/demo.sh": "#!/usr/bin/env bash\necho demo\n",
    49	    "tests/unit/test_demo.py": "# exercises scripts/demo.sh\n",
    50	    "Makefile": "unit-test:\n\t@true\n",
    51	    **LEGACY,
    52	}
    53	LOAD = "import json, sys, yaml; print(json.dumps(yaml.safe_load(sys.stdin.read().split('\\n---\\n', 1)[0].lstrip('-\\n'))))"
    54	
    55	
    56	class TaskFromPlanTest(unittest.TestCase):
    57	    def setUp(self):
    58	        temp = tempfile.TemporaryDirectory()
    59	        self.addCleanup(temp.cleanup)
    60	        self.temp = Path(temp.name).resolve()
    61	        self.repo = self.temp / "repo"
    62	        self.env = {**os.environ, **GIT_ENV, "TMPDIR": temp.name}
    63	        self.commit(FILES, "init", init=True)
    64	
    65	    def git(self, *args):
    66	        run = ["git", "-c", "commit.gpgsign=false", *args]
    67	        return subprocess.run(run, cwd=self.repo, env=self.env, capture_output=True, text=True, check=True).stdout
    68	
    69	    def commit(self, files, message, init=False):
    70	        """Write and commit files; the first commit also creates the bare origin (make unit-test has no PyYAML)."""
    71	        for rel, text in files.items():
    72	            (self.repo / rel).parent.mkdir(parents=True, exist_ok=True)
    73	            (self.repo / rel).write_text(text)
    74	        if init:
    75	            self.git("init", "-q", "-b", "main")
    76	        self.git("add", "-A")
    77	        self.git("commit", "-q", "-m", message)
    78	        if init:
    79	            self.git("init", "-q", "--bare", str(self.temp / "origin.git"))
    80	            self.git("remote", "add", "origin", str(self.temp / "origin.git"))
    81	        self.git("push", "-q", "origin", "main")
    82	        self.git("fetch", "-q", "origin")
    83	
    84	    def generate(self, *args, todo="P1-1", out=".orchestration/tasks/dotfiles-T9-demo-a01.md"):
    85	        """Run the generator; return (exit, stdout + stderr, front matter or None, text or "")."""
    86	        run = [shutil.which("uv"), "run", "--no-project", "--with", "pyyaml", "python", "-I"]
    87	        result = subprocess.run(
    88	            [*run, str(GENERATOR), todo, "--out", out, *args],
    89	            cwd=self.repo,
    90	            env=self.env,
    91	            capture_output=True,
    92	            text=True,
    93	            check=False,
    94	        )
    95	        if not (self.repo / out).is_file():
    96	            return result.returncode, result.stdout + result.stderr, None, ""
    97	        text = (self.repo / out).read_text()
    98	        front = json.loads(
    99	            subprocess.run([*run, "-c", LOAD], input=text, capture_output=True, text=True, check=True).stdout
   100	        )
   101	        return result.returncode, result.stdout + result.stderr, front, text
   102	
   103	    def test_a_generated_task_passes_the_consistency_check_and_pastes_real_premise_outputs(self):
   104	        code, out, front, text = self.generate("--seat", "a009")
   105	        self.assertEqual(code, 0, out)
   106	        self.assertEqual(out.splitlines()[0], "dotfiles-T9-demo-a01.md: OK")
   107	        self.assertIs(front["security"], True)
   108	        allowed = ["scripts/demo.sh", "tests/unit/test_demo.py", ".orchestration/dotfiles-T9-demo-a01/**"]
   109	        self.assertEqual(front["allowed_files"], allowed)
   110	        first, second = front["premises"]
   111	        self.assertEqual((first["command"], first["output"]), ("printf known-output", "known-output"))
   112	        self.assertEqual(second["command"], "sh -c 'exit 3'")
   113	        self.assertTrue(second["claim"].startswith("verify:") and "exits 3" in second["claim"], second)
   114	        self.assertIn("# from: tests/unit/test_demo.py (git grep -l demo.sh)", text)
   115	        head = self.git("rev-parse", "origin/main").strip()
   116	        self.assertIn(f"- `make unit-test`: exit 0 on origin/main {head[:12]}", text)
   117	        self.assertIn("`dotfiles-T9-demo-a01-followup-a01`", text)
   118	        controls = [r["control"] for r in front["threat_table"]]
   119	        self.assertIn("the task-file copy on the branch (.orchestration/dotfiles-T9-demo-a01/task.md)", controls)
   120	        self.assertNotIn("dotfiles-T133-result-precheck-a01", text)
   121	        self.assertEqual(len(self.git("worktree", "list").splitlines()), 1)  # the scratch worktree is gone
   122	
   123	    def test_generator_uses_the_bundled_template_without_task_records(self):
   124	        # The audit of 9da0ed3 (P1, item 5): the generator's rows, Check defaults and Completion come from
   125	        # scripts/orchestrator/task-template.md; a checkout without .orchestration/tasks/ generates a passing task.
   126	        self.git("rm", "-q", "-r", ".orchestration/tasks")
   127	        self.commit({}, "no task records")
   128	        code, out, front, text = self.generate()
   129	        self.assertEqual(code, 0, out)
   130	        controls = " || ".join(r["control"] for r in front["threat_table"])
   131	        for name in ("task metadata", "metadata separators", "in-process effects", "orchestrator effect merge"):
   132	            self.assertIn(name, controls)
   133	        self.assertIn("(.orchestration/dotfiles-T9-demo-a01/task.md)", controls)
   134	        self.assertIn("- `make format`: exit ", text)
   135	        self.assertIn("owned by `dotfiles-T9-demo-a01-followup-a01`", text)
   136	        self.assertIn("`task_copy=<sha256 of .orchestration/dotfiles-T9-demo-a01/task.md>`", text)
   137	
   138	    def test_generator_refuses_dirty_plan_commands_before_execution(self):
   139	        # The audit of 9da0ed3 (P1, item 6): plan commands run only from a clean, committed 024-* plan group.
   140	        marker = self.temp / "ran"
   141	        program = FILES[PROGRAMS].replace("`printf known-output`", f"`touch {marker}`")
   142	        self.commit({PROGRAMS: program}, "a marker command")
   143	        for dirty in ("unstaged", "staged", "untracked"):
   144	            with self.subTest(dirty=dirty):
   145	                rel = ".orchestration/plans/024-extra.md" if dirty == "untracked" else PROGRAMS
   146	                (self.repo / rel).write_text(program + "\nan uncommitted line\n")
   147	                if dirty == "staged":
   148	                    self.git("add", rel)
   149	                code, out, front, _ = self.generate()
   150	                self.assertEqual((code != 0, marker.exists(), front), (True, False, None), out)
   151	                self.assertIn("uncommitted", out)
   152	                self.git("reset", "-q", "--hard")
   153	                (self.repo / ".orchestration/plans/024-extra.md").unlink(missing_ok=True)
   154	        code, out, front, text = self.generate()
   155	        self.assertEqual((code, marker.exists()), (0, True), out)
   156	        self.assertIn(f"plan group at {self.git('rev-parse', 'HEAD').strip()}", text)
   157	
   158	    def test_wave_selection_matches_whole_todo_ids(self):
   159	        # The audit of 9da0ed3 (P2, item 12): P1-1 is a whole id in the seat's column; P1-10 or P1-11 never matches it.
   160	        waves = "## 6. 波\n\n| 波 | a009 | a008 |\n| --- | --- | --- |\n| P-W0 | P1-10, P1-11 | P1-12 |\n"
   161	        self.commit({WAVES: waves + "| P-W1 | P1-1 | |\n\n## 7. STOP\n"}, "two waves")
   162	        code, out, _, text = self.generate("--seat", "a009")
   163	        self.assertEqual(code, 0, out)
   164	        self.assertIn("wave P-W1", text)
   165	        self.assertIn("seat a009", text)
   166	        self.assertNotIn("P-W0", text)
   167	
   168	    def test_generator_preserves_wildcard_scopes_and_their_threat_rows(self):
   169	        # The audit of 9da0ed3 (P2, item 13): `scripts/*.py` and `home/dot_config/**` stay scopes, and every applied file
   170	        # they match gets its concrete row, so the generated task passes C4 and C12; a match that is itself an entry
   171	        # (scripts/demo.sh under `scripts/*.sh`) keeps its one row, so C7b passes too (the pre-push review of eb20d063).
   172	        program = FILES[PROGRAMS].replace(
   173	            "`scripts/demo.sh`**", "`scripts/demo.sh`**, `scripts/*.py`, `scripts/*.sh`, `home/dot_config/**`"
   174	        )
   175	        self.commit({PROGRAMS: program, "scripts/tool.py": "print(1)\n", "home/dot_config/x.toml": "a = 1\n"}, "scopes")
   176	        code, out, front, _ = self.generate()
   177	        self.assertEqual(code, 0, out)
   178	        self.assertTrue({"scripts/*.py", "home/dot_config/**"} <= set(front["allowed_files"]), front["allowed_files"])
   179	        controls = " || ".join(r["control"] for r in front["threat_table"])
   180	        for name in ("scripts/*.py", "home/dot_config/**", "scripts/tool.py", "home/dot_config/x.toml"):
   181	            self.assertIn(name, controls)
   182	
   183	    def test_program_item_continues_until_the_next_numbered_heading(self):
   184	        # The audit of 9da0ed3 (P2, item 14): a blank line or a fenced block does not end item (1); item (2) does.
   185	        item = "\n\n```\n{schema: x}\n```\n\nThen `scripts/late.sh` runs `printf late-output`.\n\n"
   186	        program = FILES[PROGRAMS].replace("\n\n**(2) other**: unused", item + "**(2) other**: `printf other-item`")
   187	        self.commit({PROGRAMS: program, "scripts/late.sh": "echo late\n"}, "a longer item")
   188	        code, out, front, _ = self.generate()
   189	        self.assertEqual(code, 0, out)
   190	        self.assertIn("scripts/late.sh", front["allowed_files"])
   191	        commands = [p["command"] for p in front["premises"]]
   192	        self.assertIn("printf late-output", commands)
   193	        self.assertNotIn("printf other-item", commands)
   194	
   195	    def test_generator_retains_unavailable_single_word_and_redirecting_commands(self):
   196	        # The audit of 9da0ed3 (P2, item 15): a span is a command by its form, not by an executable existing now; the
   197	        # same rule picks the item's `make` targets for the Check.
   198	        written, check = self.temp / "written", self.temp / "check.out"
   199	        spans = f"`no-such-tool-a02 --list`, `pwd`, `printf hi > {written}` and `make unit-test > {check}`"
   200	        self.commit({PROGRAMS: FILES[PROGRAMS].replace("`sh -c 'exit 3'`", spans)}, "command forms")
   201	        code, out, front, text = self.generate()
   202	        self.assertEqual(code, 0, out)
   203	        premises = {p["command"]: p for p in front["premises"]}
   204	        self.assertTrue({"no-such-tool-a02 --list", "pwd", f"printf hi > {written}"} <= set(premises), premises)
   205	        self.assertTrue(premises["no-such-tool-a02 --list"]["claim"].startswith("verify:"), premises)
   206	        self.assertIn("exits 127", premises["no-such-tool-a02 --list"]["claim"])
   207	        self.assertEqual(premises["pwd"]["output"], str(self.repo))
   208	        self.assertEqual((premises[f"printf hi > {written}"]["output"], written.read_text()), ("", "hi"))
   209	        self.assertIn(f"- `make unit-test > {check}`: exit 0 on origin/main", text)
   210	        self.assertNotIn(f"make unit-test > {check}", premises)
   211	
   212	
   213	if __name__ == "__main__":
   214	    unittest.main()

 succeeded in 230ms:
{
  "repo": "mryfmo/dotfiles",
  "pr": 417,
  "head_sha": "8a09b9365932f23b09df8aa2385a93d0b3016a3e",
  "base_ref": "main",
  "base_sha": "b22a5580d0778e57a66d3f75c76e3c55b88701e1",
  "generated_at": "2026-10-19T04:20:02+00:00",
  "checks": [
    {
      "name": "test (ubuntu-26.04, client)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/39196381817/job/117879956503"
    },
    {
      "name": "test (ubuntu-24.04, client)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/39196381817/job/117879956403"
    },
    {
      "name": "test (macos-14, client)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/39196381817/job/117879956379"
    },
    {
      "name": "public-bootstrap (ubuntu-24.04, client)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/39196381814/job/117879956342"
    },
    {
      "name": "public-bootstrap (ubuntu-24.04, server)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/39196381814/job/117879956319"
    },
    {
      "name": "test (ubuntu-24.04, server)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/39196381817/job/117879956215"
    },
    {
      "name": "public-bootstrap (macos-14, client)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/39196381814/job/117879956194"
    },
    {
      "name": "validate",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/39196381799/job/117879956075"
    },
    {
      "name": "regime",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/39196380313/job/117879951945"
    },
    {
      "name": "GitGuardian Security Checks",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/runs/117879948688"
    }
  ],
  "items": [
    {
      "source": "issue_comment",
      "author": "chatgpt-codex-connector[bot]",
      "bot": true,
      "level": "comment",
      "path": null,
      "line": null,
      "body": "To use Codex here, [create a Codex account and connect to github](https://chatgpt.com/codex/cloud/settings/connectors).",
      "url": "https://github.com/mryfmo/dotfiles/pull/417#issuecomment-6249489509",
      "disposition": "not-applicable:bot summary or onboarding comment, no finding; evidence=jq --argjson u '\"https://github.com/mryfmo/dotfiles/pull/417#issuecomment-6249489509\"' '.items[] | select(.url == $u)' ~/Workspace/dotfiles/.orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-pr-feedback.json"
    },
    {
      "source": "issue_comment",
      "author": "coderabbitai[bot]",
      "bot": true,
      "level": "comment",
      "path": null,
      "line": null,
      "body": "<!-- This is an auto-generated comment: summarize by coderabbit.ai -->\n<!-- This is an auto-generated comment: skip review by coderabbit.ai -->\n\n> [!IMPORTANT]\n> ## Review skipped\n> \n> Auto reviews are disabled on this repository. Please check the settings in the CodeRabbit UI or the `.coderabbit.yaml` file in this repository. To trigger a single review, invoke the `@coderabbitai review` command.\n> \n> <details>\n> <summary><strong>\u2699\ufe0f Run configuration</strong></summary>\n> <dl>\n> <dd>\n> \n> - **Configuration used**: Repository: mryfmo/dotfiles/.coderabbit.yaml\n> - **Review profile**: CHILL\n> - **Plan**: Advanced\n> - **Run ID**: `d0cfd86c-3ba6-4e24-be80-a65085ec2cd4`\n> \n> </dd>\n> </dl>\n> </details>\n> \n> You can disable this status message by setting the `reviews.review_status` to `false` in the CodeRabbit configuration file.\n> \n> Use the checkbox below for a quick retry:\n> - [ ] <!-- {\"checkboxId\":\"e9bb8d72-00e8-4f67-9cb2-caf3b22574fe\"} --> \ud83d\udd0d Trigger review\n\n<!-- end of auto-generated comment: skip review by coderabbit.ai -->\n\n<!-- autopilot:start -->\n- [ ] <!-- {\"checkboxId\":\"2708ad07-9f24-4260-9c11-7dc76a49f2e3\"} --> <strong title=\"Keep fixing CodeRabbit findings and required CI, and resolving merge conflicts\">Autofix</strong> \u00b7 Keep fixing CodeRabbit findings and required CI, and resolving merge conflicts\n<!-- autopilot:end -->\n<!-- tips_start -->\n\n\n\nThanks for using [CodeRabbit](https://coderabbit.ai?utm_source=oss&utm_medium=github&utm_campaign=mryfmo/dotfiles&utm_content=417)! It's free for OSS, and your support helps us grow. If you like it, consider giving us a shout-out.\n\n<details>\n<summary><strong>\u2764\ufe0f Share</strong></summary>\n<dl>\n<dd>\n\n- [X](https://twitter.com/intent/tweet?text=I%20just%20used%20%40coderabbitai%20for%20my%20code%20review%2C%20and%20it%27s%20fantastic%21%20It%27s%20free%20for%20OSS%20and%20offers%20a%20free%20trial%20for%20the%20proprietary%20code.%20Check%20it%20out%3A&url=https%3A//coderabbit.ai)\n- [Mastodon](https://mastodon.social/share?text=I%20just%20used%20%40coderabbitai%20for%20my%20code%20review%2C%20and%20it%27s%20fantastic%21%20It%27s%20free%20for%20OSS%20and%20offers%20a%20free%20trial%20for%20the%20proprietary%20code.%20Check%20it%20out%3A%20https%3A%2F%2Fcoderabbit.ai)\n- [Reddit](https://www.reddit.com/submit?title=Great%20tool%20for%20code%20review%20-%20CodeRabbit&text=I%20just%20used%20CodeRabbit%20for%20my%20code%20review%2C%20and%20it%27s%20fantastic%21%20It%27s%20free%20for%20OSS%20and%20offers%20a%20free%20trial%20for%20proprietary%20code.%20Check%20it%20out%3A%20https%3A//coderabbit.ai)\n- [LinkedIn](https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Fcoderabbit.ai&mini=true&title=Great%20tool%20for%20code%20review%20-%20CodeRabbit&summary=I%20just%20used%20CodeRabbit%20for%20my%20code%20review%2C%20and%20it%27s%20fantastic%21%20It%27s%20free%20for%20OSS%20and%20offers%20a%20free%20trial%20for%20proprietary%20code)\n\n</dd>\n</dl>\n</details>\n\n\n<sub>Comment `@coderabbitai help` to get the list of available commands.</sub>\n\n<!-- tips_end -->",
      "url": "https://github.com/mryfmo/dotfiles/pull/417#issuecomment-6249489670",
      "disposition": "not-applicable:bot summary or onboarding comment, no finding; evidence=jq --argjson u '\"https://github.com/mryfmo/dotfiles/pull/417#issuecomment-6249489670\"' '.items[] | select(.url == $u)' ~/Workspace/dotfiles/.orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-pr-feedback.json"
    },
    {
      "source": "issue_comment",
      "author": "chatgpt-codex-connector[bot]",
      "bot": true,
      "level": "comment",
      "path": null,
      "line": null,
      "body": "<!-- codex-pull-request-review-summary -->\n<!-- codex-review-state:v1 {\"code_review\":{\"commit_sha\":\"35c660222ffd7af143842d310ae8cf3b15db61c5\",\"has_any_findings\":true,\"has_unresolved_findings\":true,\"status\":\"completed\"},\"security_review\":{\"commit_sha\":\"35c660222ffd7af143842d310ae8cf3b15db61c5\",\"has_any_findings\":false,\"has_unresolved_findings\":false,\"status\":\"completed\"}} -->\n<!-- codex-security-review:v1 {\"blockingSeverityThreshold\":\"P0\",\"headSha\":\"35c660222ffd7af143842d310ae8cf3b15db61c5\",\"mergeGateEnabled\":false,\"pullRequestNumber\":417,\"repository\":\"mryfmo/dotfiles\",\"status\":\"completed\"} -->\n## Codex Review Summary\n\nThis comment shows the latest Codex review activity on this pull request.\n\n| Review | Status | Commit | Review trigger |\n| --- | --- | --- | --- |\n| \ud83d\udcdd **Code Review** | \u2705 **Completed** <relative-time datetime=\"2026-10-18T12:11:07.372036Z\">2026-10-18T12:11:07.372036Z</relative-time> | `35c6602` | Draft marked ready |\n| \ud83d\udd12 **Security Review** | \u2705 **Completed** <relative-time datetime=\"2026-10-18T12:12:39.986998Z\">2026-10-18T12:12:39.986998Z</relative-time> | `35c6602` | Draft marked ready |\n\n\n\n<details> <summary>\u2139\ufe0f About Codex in GitHub</summary>\n<br/>\n\n[Your team has set up Codex to review pull requests in this repo](https://chatgpt.com/codex/cloud/settings/general). Reviews are triggered when you\n- Open a pull request for review\n- Mark a draft as ready\n- Comment \"@codex review\" or \"@codex security review\".\n\nCodex reacts with \ud83d\udc40 while any review is running, comments if it has suggestions, and reacts with \ud83d\udc4d once all reviews finish with no findings.\n\n</details>",
      "url": "https://github.com/mryfmo/dotfiles/pull/417#issuecomment-6249725018",
      "disposition": "not-applicable:bot summary or onboarding comment, no finding; evidence=jq --argjson u '\"https://github.com/mryfmo/dotfiles/pull/417#issuecomment-6249725018\"' '.items[] | select(.url == $u)' ~/Workspace/dotfiles/.orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-pr-feedback.json"
    },
    {
      "source": "review",
      "author": "chatgpt-codex-connector[bot]",
      "bot": true,
      "level": "commented",
      "path": null,
      "line": null,
      "body": "<!-- codex-review-receipt:v1 -->\n\n\n### \ud83d\udca1 Codex Review\n\nHere are some automated review suggestions for this pull request.\n\n**Reviewed commit:** `35c660222f`\n    \n\n<details> <summary>\u2139\ufe0f About Codex in GitHub</summary>\n<br/>\n\nCodex has been enabled to automatically review pull requests in this repo. Reviews are triggered when you\n- Open a pull request for review\n- Mark a draft as ready\n- Comment \"@codex review\".\n\nIf Codex has suggestions, it will comment; otherwise it will react with \ud83d\udc4d.\n\n\n\n\nWhen you [sign up for Codex through ChatGPT](https://openai.com/codex), Codex can also answer questions or update the PR, like \"@codex address that feedback\".\n            \n</details>",
      "url": "https://github.com/mryfmo/dotfiles/pull/417#pullrequestreview-5562936729",
      "commit": "35c660222ffd7af143842d310ae8cf3b15db61c5",
      "disposition": "not-applicable:review object; its findings are the inline threads, each dispositioned on its own; evidence=jq --argjson u '\"https://github.com/mryfmo/dotfiles/pull/417#pullrequestreview-5562936729\"' '.items[] | select(.url == $u)' ~/Workspace/dotfiles/.orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-pr-feedback.json"
    },
    {
      "source": "review_comment",
      "author": "chatgpt-codex-connector[bot]",
      "bot": true,
      "level": "comment",
      "path": "scripts/orchestrator/task-consistency-check.py",
      "line": 94,
      "body": "**<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Sandbox premise commands before executing them**\n\nWhen the consistency checker runs at acceptance on a PR-controlled task file, any premise reaches `bash -c` here with the review user's permissions. Restricting `PATH` does not prevent shell builtins, absolute executables, redirects, or destructive repository writes, so the checker described as read-only can execute arbitrary code before deciding whether the task is valid; the threat table's claim that the checker stays read-only therefore does not mitigate this boundary. Run premises in a genuinely read-only sandbox or require them to come from a trusted revision.\n\nAGENTS.md reference: [AGENTS.md:L75-L78](https://github.com/mryfmo/dotfiles/blob/35c660222ffd7af143842d310ae8cf3b15db61c5/AGENTS.md#L75-L78)\n\nUseful? React with \ud83d\udc4d\u00a0/ \ud83d\udc4e.\n\n<!-- codex-code-review-finding:v1 -->",
      "url": "https://github.com/mryfmo/dotfiles/pull/417#discussion_r4306960622",
      "resolved": false,
      "outdated": false,
      "disposition": "fixed:538e60bd"
    },
    {
      "source": "review_comment",
      "author": "chatgpt-codex-connector[bot]",
      "bot": true,
      "level": "comment",
      "path": "scripts/orchestrator/task-from-plan.py",
      "line": 127,
      "body": "**<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Bundle the required task template**\n\nIn the reviewed commit tree, a repo-wide tree search finds no `.orchestration/tasks/dotfiles-T133-result-precheck-a01.md`, but every generator invocation unconditionally reads that path here. Consequently a clean checkout raises `FileNotFoundError` before writing a task; the closed test masks this because its fixture creates the missing template itself. Include a stable template in the repository or generate these rows without depending on an untracked task file.\n\nAGENTS.md reference: [AGENTS.md:L75-L78](https://github.com/mryfmo/dotfiles/blob/35c660222ffd7af143842d310ae8cf3b15db61c5/AGENTS.md#L75-L78)\n\nUseful? React with \ud83d\udc4d\u00a0/ \ud83d\udc4e.\n\n<!-- codex-code-review-finding:v1 -->",
      "url": "https://github.com/mryfmo/dotfiles/pull/417#discussion_r4306960626",
      "resolved": false,
      "outdated": true,
      "disposition": "fixed:b3c6b7ea"
    },
    {
      "source": "review_comment",
      "author": "chatgpt-codex-connector[bot]",
      "bot": true,
      "level": "comment",
      "path": "scripts/orchestrator/plan-check.py",
      "line": 88,
      "body": "**<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Resolve globs before checking wave overlaps**\n\nWhen one same-wave task allows `scripts/*.py` and another allows `scripts/foo.py`, this normalization leaves the first value as the literal string `scripts/*.py`; the later equality/prefix comparison therefore reports no F2 violation even though both tasks can edit `scripts/foo.py`. Expand tracked matches or perform real glob-overlap checks before comparing scopes; the current closed test covers only two identical concrete paths.\n\nAGENTS.md reference: [AGENTS.md:L75-L78](https://github.com/mryfmo/dotfiles/blob/35c660222ffd7af143842d310ae8cf3b15db61c5/AGENTS.md#L75-L78)\n\nUseful? React with \ud83d\udc4d\u00a0/ \ud83d\udc4e.\n\n<!-- codex-code-review-finding:v1 -->",
      "url": "https://github.com/mryfmo/dotfiles/pull/417#discussion_r4306960630",
      "resolved": false,
      "outdated": true,
      "disposition": "fixed:b3c6b7ea"
    },
    {
      "source": "annotation",
      "author": "github-actions",
      "bot": true,
      "level": "notice",
      "path": ".github",
      "line": 1,
      "body": "Due to capacity constraints, jobs targeting macOS arm64 runners may experience longer queue times.",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/39196381817/job/117879956379",
      "check": "test (macos-14, client)",
      "disposition": "not-applicable:runner capacity notice, no finding; evidence=jq --argjson u '\"https://github.com/mryfmo/dotfiles/actions/runs/39196381817/job/117879956379\"' '.items[] | select(.url == $u)' ~/Workspace/dotfiles/.orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-pr-feedback.json"
    },
    {
      "source": "annotation",
      "author": "github-actions",
      "bot": true,
      "level": "notice",
      "path": ".github",
      "line": 1,
      "body": "Due to capacity constraints, jobs targeting macOS arm64 runners may experience longer queue times.",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/39196381814/job/117879956194",
      "check": "public-bootstrap (macos-14, client)",
      "disposition": "not-applicable:runner capacity notice, no finding; evidence=jq --argjson u '\"https://github.com/mryfmo/dotfiles/actions/runs/39196381814/job/117879956194\"' '.items[] | select(.url == $u)' ~/Workspace/dotfiles/.orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-pr-feedback.json"
    },
    {
      "source": "status",
      "author": "coderabbitai[bot]",
      "bot": true,
      "level": "success",
      "path": null,
      "line": null,
      "body": "CodeRabbit: Review skipped: automatic reviews are disabled",
      "url": null,
      "check": "CodeRabbit",
      "disposition": "not-applicable:CI status, no finding; evidence=jq --argjson s '\"status\"' --argjson c '\"CodeRabbit\"' '.items[] | select(.source == $s and .check == $c)' ~/Workspace/dotfiles/.orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-pr-feedback.json"
    }
  ]
}

**Planning artifact inspection**
exec
/bin/zsh -lc "git ls-tree -r --name-only 8a09b9365932f23b09df8aa2385a93d0b3016a3e .orchestration/plans .orchestration/tasks | rg '006|024|followup|T133' && python3 -B -c 'import json,pathlib; p=pathlib.Path(\".orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-pr-feedback.json\"); d=json.loads(p.read_text()); print({k:v for k,v in d.items() if k"'!="items"}); print(*[{k:v for k,v in i.items() if k!="body"} for i in d.get("items",[])],sep="'"\\n\")' && git show 8a09b9365932f23b09df8aa2385a93d0b3016a3e:.orchestration/dotfiles-T133-task-generator-plan-check-a02/report.md | nl -ba | sed -n '172,230p'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 91ms:
.orchestration/plans/006-regime-v3-execution.md
.orchestration/tasks/dotfiles-T128-chain-github-scripts-followup-a01-review-a01.md
.orchestration/tasks/dotfiles-T128-chain-github-scripts-followup-a01.md
.orchestration/tasks/dotfiles-T128-chain-github-scripts-followup-a02-review-a01.md
.orchestration/tasks/dotfiles-T128-chain-github-scripts-followup-a02.md
.orchestration/tasks/dotfiles-T128-chain-github-scripts-followup-a03.md
.orchestration/tasks/dotfiles-T128-chain-glue-finish-followup-a01.md
.orchestration/tasks/dotfiles-T128-chain-glue-integrate-followup-a01.md
.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a01-review-a01.md
.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a01.md
.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a02-review-a01.md
.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a02.md
.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a03.md
.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a04-review-a01.md
.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a04.md
.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a05.md
.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-review-a03.md
.orchestration/tasks/dotfiles-T128-followup-owners-review-a01.md
.orchestration/tasks/dotfiles-T128-gate-evidence-followup-a01.md
.orchestration/tasks/dotfiles-T128-model-profiles-xhigh-followup-a01.md
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
.orchestration/tasks/dotfiles-T128-playbook-rules-followup-a01-amend-review-a01.md
.orchestration/tasks/dotfiles-T128-playbook-rules-followup-a01.md
.orchestration/tasks/dotfiles-T128-project-map-pane-open-a01-followup-a01.md
.orchestration/tasks/dotfiles-T128-project-map-pane-open-a01-followup-a02.md
.orchestration/tasks/dotfiles-T128-project-map-pane-open-a01-followup-review-a01.md
.orchestration/tasks/dotfiles-T128-project-map-reload-hook-followup-a01.md
.orchestration/tasks/dotfiles-T128-project-map-reload-hook-followup-review-a01.md
.orchestration/tasks/dotfiles-T128-rules-step8-followup-a01.md
.orchestration/tasks/dotfiles-T128-s1-replan-gate-followup-a01.md
.orchestration/tasks/dotfiles-T128-seat-launch-args-followup-a01.md
.orchestration/tasks/dotfiles-T128-seat-liveness-followup-a01.md
.orchestration/tasks/dotfiles-T128-seat-liveness-followup-a02-review-a01.md
.orchestration/tasks/dotfiles-T128-seat-liveness-followup-a02.md
.orchestration/tasks/dotfiles-T128-seat-liveness-followup-review-a01.md
.orchestration/tasks/dotfiles-T128-settings-hook-dedupe-followup-a01.md
.orchestration/tasks/dotfiles-T128-settings-hook-dedupe-followup-review-a01.md
.orchestration/tasks/dotfiles-T128-task-checkers-followup-a01.md
.orchestration/tasks/dotfiles-T128-task-checkers-followup-review-a01.md
.orchestration/tasks/dotfiles-T129-anthropic-auth-route-check-followup-a01.md
.orchestration/tasks/dotfiles-T129-assets-omp-hcom-followup-a01.md
.orchestration/tasks/dotfiles-T129-audit-inherit-replan-json-followup-a01.md
.orchestration/tasks/dotfiles-T129-integration-seat-result-gate-cap-followup-a01.md
.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-followup-a01.md
.orchestration/tasks/dotfiles-T130-claude-sandbox-integration-followup-a01.md
{'repo': 'mryfmo/dotfiles', 'pr': 417, 'head_sha': '8a09b9365932f23b09df8aa2385a93d0b3016a3e', 'base_ref': 'main', 'base_sha': 'b22a5580d0778e57a66d3f75c76e3c55b88701e1', 'generated_at': '2026-10-19T04:20:02+00:00', 'checks': [{'name': 'test (ubuntu-26.04, client)', 'conclusion': 'success', 'url': 'https://github.com/mryfmo/dotfiles/actions/runs/39196381817/job/117879956503'}, {'name': 'test (ubuntu-24.04, client)', 'conclusion': 'success', 'url': 'https://github.com/mryfmo/dotfiles/actions/runs/39196381817/job/117879956403'}, {'name': 'test (macos-14, client)', 'conclusion': 'success', 'url': 'https://github.com/mryfmo/dotfiles/actions/runs/39196381817/job/117879956379'}, {'name': 'public-bootstrap (ubuntu-24.04, client)', 'conclusion': 'success', 'url': 'https://github.com/mryfmo/dotfiles/actions/runs/39196381814/job/117879956342'}, {'name': 'public-bootstrap (ubuntu-24.04, server)', 'conclusion': 'success', 'url': 'https://github.com/mryfmo/dotfiles/actions/runs/39196381814/job/117879956319'}, {'name': 'test (ubuntu-24.04, server)', 'conclusion': 'success', 'url': 'https://github.com/mryfmo/dotfiles/actions/runs/39196381817/job/117879956215'}, {'name': 'public-bootstrap (macos-14, client)', 'conclusion': 'success', 'url': 'https://github.com/mryfmo/dotfiles/actions/runs/39196381814/job/117879956194'}, {'name': 'validate', 'conclusion': 'success', 'url': 'https://github.com/mryfmo/dotfiles/actions/runs/39196381799/job/117879956075'}, {'name': 'regime', 'conclusion': 'success', 'url': 'https://github.com/mryfmo/dotfiles/actions/runs/39196380313/job/117879951945'}, {'name': 'GitGuardian Security Checks', 'conclusion': 'success', 'url': 'https://github.com/mryfmo/dotfiles/runs/117879948688'}]}
{'source': 'issue_comment', 'author': 'chatgpt-codex-connector[bot]', 'bot': True, 'level': 'comment', 'path': None, 'line': None, 'url': 'https://github.com/mryfmo/dotfiles/pull/417#issuecomment-6249489509', 'disposition': 'not-applicable:bot summary or onboarding comment, no finding; evidence=jq --argjson u \'"https://github.com/mryfmo/dotfiles/pull/417#issuecomment-6249489509"\' \'.items[] | select(.url == $u)\' ~/Workspace/dotfiles/.orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-pr-feedback.json'}
{'source': 'issue_comment', 'author': 'coderabbitai[bot]', 'bot': True, 'level': 'comment', 'path': None, 'line': None, 'url': 'https://github.com/mryfmo/dotfiles/pull/417#issuecomment-6249489670', 'disposition': 'not-applicable:bot summary or onboarding comment, no finding; evidence=jq --argjson u \'"https://github.com/mryfmo/dotfiles/pull/417#issuecomment-6249489670"\' \'.items[] | select(.url == $u)\' ~/Workspace/dotfiles/.orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-pr-feedback.json'}
{'source': 'issue_comment', 'author': 'chatgpt-codex-connector[bot]', 'bot': True, 'level': 'comment', 'path': None, 'line': None, 'url': 'https://github.com/mryfmo/dotfiles/pull/417#issuecomment-6249725018', 'disposition': 'not-applicable:bot summary or onboarding comment, no finding; evidence=jq --argjson u \'"https://github.com/mryfmo/dotfiles/pull/417#issuecomment-6249725018"\' \'.items[] | select(.url == $u)\' ~/Workspace/dotfiles/.orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-pr-feedback.json'}
{'source': 'review', 'author': 'chatgpt-codex-connector[bot]', 'bot': True, 'level': 'commented', 'path': None, 'line': None, 'url': 'https://github.com/mryfmo/dotfiles/pull/417#pullrequestreview-5562936729', 'commit': '35c660222ffd7af143842d310ae8cf3b15db61c5', 'disposition': 'not-applicable:review object; its findings are the inline threads, each dispositioned on its own; evidence=jq --argjson u \'"https://github.com/mryfmo/dotfiles/pull/417#pullrequestreview-5562936729"\' \'.items[] | select(.url == $u)\' ~/Workspace/dotfiles/.orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-pr-feedback.json'}
{'source': 'review_comment', 'author': 'chatgpt-codex-connector[bot]', 'bot': True, 'level': 'comment', 'path': 'scripts/orchestrator/task-consistency-check.py', 'line': 94, 'url': 'https://github.com/mryfmo/dotfiles/pull/417#discussion_r4306960622', 'resolved': False, 'outdated': False, 'disposition': 'fixed:538e60bd'}
{'source': 'review_comment', 'author': 'chatgpt-codex-connector[bot]', 'bot': True, 'level': 'comment', 'path': 'scripts/orchestrator/task-from-plan.py', 'line': 127, 'url': 'https://github.com/mryfmo/dotfiles/pull/417#discussion_r4306960626', 'resolved': False, 'outdated': True, 'disposition': 'fixed:b3c6b7ea'}
{'source': 'review_comment', 'author': 'chatgpt-codex-connector[bot]', 'bot': True, 'level': 'comment', 'path': 'scripts/orchestrator/plan-check.py', 'line': 88, 'url': 'https://github.com/mryfmo/dotfiles/pull/417#discussion_r4306960630', 'resolved': False, 'outdated': True, 'disposition': 'fixed:b3c6b7ea'}
{'source': 'annotation', 'author': 'github-actions', 'bot': True, 'level': 'notice', 'path': '.github', 'line': 1, 'url': 'https://github.com/mryfmo/dotfiles/actions/runs/39196381817/job/117879956379', 'check': 'test (macos-14, client)', 'disposition': 'not-applicable:runner capacity notice, no finding; evidence=jq --argjson u \'"https://github.com/mryfmo/dotfiles/actions/runs/39196381817/job/117879956379"\' \'.items[] | select(.url == $u)\' ~/Workspace/dotfiles/.orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-pr-feedback.json'}
{'source': 'annotation', 'author': 'github-actions', 'bot': True, 'level': 'notice', 'path': '.github', 'line': 1, 'url': 'https://github.com/mryfmo/dotfiles/actions/runs/39196381814/job/117879956194', 'check': 'public-bootstrap (macos-14, client)', 'disposition': 'not-applicable:runner capacity notice, no finding; evidence=jq --argjson u \'"https://github.com/mryfmo/dotfiles/actions/runs/39196381814/job/117879956194"\' \'.items[] | select(.url == $u)\' ~/Workspace/dotfiles/.orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-pr-feedback.json'}
{'source': 'status', 'author': 'coderabbitai[bot]', 'bot': True, 'level': 'success', 'path': None, 'line': None, 'url': None, 'check': 'CodeRabbit', 'disposition': 'not-applicable:CI status, no finding; evidence=jq --argjson s \'"status"\' --argjson c \'"CodeRabbit"\' \'.items[] | select(.source == $s and .check == $c)\' ~/Workspace/dotfiles/.orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-pr-feedback.json'}
   172	## Feedback dispositions
   173	
   174	The Bot's review of a01 (5562936729, on 35c66022) left three threads on PR #417. Each gets its root-cause disposition; the orchestrator replies and resolves:
   175	
   176	- **4306960622 [P1] Sandbox premise commands before executing them** (`task-consistency-check.py:75`): fixed:538e60bd.
   177	  - The checker executes premises only for the file whose sha256 `--premises-sha` names, the orchestrator's dispatched text. A PR-controlled copy at acceptance has no trusted sha, so nothing runs; it gets item 8's warning.
   178	  - a02 keeps this gate (item 7; red at ff4d25a8, green here) and closes stdin in 6e07d291. The generator runs only committed plan text (item 6).
   179	- **4306960626 [P1] Bundle the required task template** (`task-from-plan.py:131`): fixed:eb20d063.
   180	  - The template is `scripts/orchestrator/task-template.md`, and nothing under `.orchestration/tasks/` is read (item 5).
   181	  - Regression: `test_generator_uses_the_bundled_template_without_task_records`, which deletes `.orchestration/tasks/` from the fixture.
   182	- **4306960630 [P2] Resolve globs before checking wave overlaps** (`plan-check.py:89`): fixed:eb20d063. F2 compares concrete tree matches, plus literals a glob matches (item 11).
   183	  - The Bot's case, `scripts/*.py` against a literal `scripts/two.py`, is the retained F2 glob subtest.
   184	  - Two intersecting globs are `test_f2_detects_intersecting_globs_through_concrete_tree_matches`.
   185	
   186	The task-level audit of 9da0ed3 (three P1, twelve P2) is dispositioned item by item above: items 5 to 19, plus item 20's PR #418 review.
   187	
   188	This push: no `@codex review` is posted. CI on the final head and the 15-minute Bot window are in the RESULT line.
   189	
   190	## Amendment 1: the CI-repair round
   191	
   192	The chain update-branched PR #417 onto main b22a5580 (63b6acae). The regime verifier from PR #418 now runs this task's checker on the fixtures in `tests/unit/test_regime_ci.py`. Their threat rows carried a bare `disposition: residual`, which C13 refuses (and C11, as a payload under 20 characters). Three regime tests failed in CI and five locally (validation.md).
   193	
   194	Commit eb0b1c06 gives each of the five fixture rows `'residual: the compensating control of this fixture'` and copies amendment 1's task text. No expected output and no production file changes.
   195	
   196	- The regime tests are red on 63b6acae.
   197	- 101 tests across the regime, task and orchestrator-tool modules are green on eb0b1c06.
   198	- Caps against the new merge base: 659 of 700 outside `tests/` and 673 of 800 under `tests/`.
   199	
   200	This is one CI-repair round under C-61. The worker's pre-push review round of a02 is unchanged.

web search: 
web search: https://github.com/mryfmo/dotfiles/pull/417
**Reviewing in-memory testing strategy**
exec
/bin/zsh -lc 'git show 8a09b9365932f23b09df8aa2385a93d0b3016a3e:tests/unit/test_task_consistency_c11_c15.py | nl -ba' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc "git show 8a09b9365932f23b09df8aa2385a93d0b3016a3e:tests/unit/test_plan_check.py | nl -ba && git show 8a09b9365932f23b09df8aa2385a93d0b3016a3e:.orchestration/plans/006-regime-v3-execution.md | rg -n -C 4 'INV-6|invariants:|implementing_tasks|S2|amendment'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 42ms:
     1	"""Exercise C11 to C15 of task-consistency-check.py: one red fixture per check, and the current T133 task files.
     2	
     3	The fixtures are task files in a temporary repository whose origin is a bare repository (C15 reads origin/main). The
     4	checker runs through uv with PyYAML, which make unit-test does not provide to this process.
     5	"""
     6	
     7	import hashlib
     8	import os
     9	import shutil
    10	import subprocess
    11	import tempfile
    12	import unittest
    13	from pathlib import Path
    14	
    15	ROOT = Path(__file__).resolve().parents[2]
    16	CHECKER = ROOT / "scripts/orchestrator/task-consistency-check.py"
    17	GIT_ENV = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
    18	UNTRUSTED = "dotfiles-T9-base-a01.md: warning: C14: not run (no trusted sha)\n"  # the checker's stderr line
    19	NONPATH = "".join(
    20	    f'  - control: {name}\n    disposition: "residual: the fixture\'s control for {name}"\n'
    21	    for name in (
    22	        "metadata separators",
    23	        "in-process effects",
    24	        "workflow and interpreter or environment inputs",
    25	        "new or renamed scripts",
    26	        "orchestrator effect merge",
    27	        "orchestrator effect update-branch",
    28	        "orchestrator effect forced worker removal",
    29	    )
    30	)
    31	BASE = f"""---
    32	format: 2
    33	task_id: dotfiles-T9-base-a01
    34	kind: code
    35	allowed_files:
    36	  - scripts/tool.py
    37	  - .orchestration/dotfiles-T9-base-a01/**
    38	design_review:
    39	  receipt: r1
    40	  design: .orchestration/tasks/dotfiles-T9-design-a01.md
    41	invariants:
    42	  INV-1: "the tool prints one line per finding"
    43	threat_table:
    44	  - control: "scripts/tool.py (the tool)"
    45	    disposition: "closed: tests/unit/test_tool.py::test_tool_prints_findings"
    46	  - control: "the evidence under .orchestration/dotfiles-T9-base-a01/ (report.md)"
    47	    disposition: "residual: prose and pasted command output only"
    48	  - control: task metadata
    49	    disposition: "out-of-scope: dotfiles-T9-design-a01"
    50	  - control: "scripts/a.sh (the one file of the glob fixture a row names)"
    51	    disposition: "residual: a fixture row for the C12 case"
    52	{NONPATH}premises:
    53	  - claim: the fixture's premise prints base
    54	    command: printf base
    55	    output: |-
    56	      base
    57	---
    58	
    59	# AGMSG-TASK dotfiles-T9-base-a01 — the fixture
    60	"""
    61	DESIGN = '---\nformat: 2\ninvariants:\n  INV-1: "the tool prints one line per finding"\n---\n\n# design\n'
    62	CASES = {
    63	    "C11": (
    64	        '"closed: tests/unit/test_tool.py::test_tool_prints_findings"',
    65	        '"closed: tests/unit/test_tool.py::two words"',
    66	    ),
    67	    "C12": ("  - scripts/tool.py\n", "  - scripts/tool.py\n  - scripts/*.sh\n"),
    68	    "C13": ('"residual: prose and pasted command output only"', '"accepted: prose and pasted command output only"'),
    69	    "C14": ("      base\n---", "      edited\n---"),
    70	    "C15": ('INV-1: "the tool prints one line per finding"', 'INV-1: "the tool prints one line per run"'),
    71	}
    72	
    73	
    74	class TaskConsistencyC11C15Test(unittest.TestCase):
    75	    def setUp(self):
    76	        temp = tempfile.TemporaryDirectory()
    77	        self.addCleanup(temp.cleanup)
    78	        self.repo = Path(temp.name).resolve() / "repo"
    79	        env = {**os.environ, **GIT_ENV}
    80	        files = {
    81	            ".orchestration/tasks/dotfiles-T9-design-a01.md": DESIGN,
    82	            "scripts/tool.py": "print('tool')\n",
    83	            "scripts/a.sh": "echo a\n",
    84	            "scripts/b.sh": "echo b\n",
    85	        }
    86	        for rel, text in files.items():
    87	            (self.repo / rel).parent.mkdir(parents=True, exist_ok=True)
    88	            (self.repo / rel).write_text(text)
    89	        bare = str(Path(temp.name) / "origin.git")
    90	        for args in (
    91	            ("init", "-q", "-b", "main"),
    92	            ("add", "-A"),
    93	            ("commit", "-q", "-m", "init"),
    94	            ("init", "-q", "--bare", bare),
    95	        ):
    96	            subprocess.run(["git", "-c", "commit.gpgsign=false", *args], cwd=self.repo, env=env, check=True)
    97	        for args in (("remote", "add", "origin", bare), ("push", "-q", "origin", "main"), ("fetch", "-q", "origin")):
    98	            subprocess.run(["git", *args], cwd=self.repo, env=env, check=True)
    99	
   100	    def check(self, *tasks, root=None, sha=True):
   101	        """Run the checker; `sha` True passes the first file's sha256 as --premises-sha, as for the dispatched text."""
   102	        if sha is True:
   103	            sha = hashlib.sha256(Path(tasks[0]).read_bytes()).hexdigest()
   104	        run = [shutil.which("uv"), "run", "--no-project", "--with", "pyyaml", "python", "-I", str(CHECKER)]
   105	        trusted = ["--premises-sha", sha] if sha else []
   106	        result = subprocess.run(
   107	            [*run, "--root", str(root or self.repo), *trusted, *map(str, tasks)],
   108	            capture_output=True,
   109	            text=True,
   110	            check=False,
   111	        )
   112	        return result.returncode, result.stdout + result.stderr
   113	
   114	    def task(self, text):
   115	        path = self.repo / ".orchestration/tasks/dotfiles-T9-base-a01.md"
   116	        path.write_text(text)
   117	        return path
   118	
   119	    def test_each_new_check_is_red_on_its_fixture_and_the_existing_checks_are_unchanged(self):
   120	        code, out = self.check(self.task(BASE))
   121	        self.assertEqual((code, out), (0, "dotfiles-T9-base-a01.md: OK\n"))
   122	        for check, (old, new) in CASES.items():
   123	            with self.subTest(check=check):
   124	                self.assertEqual(BASE.count(old), 1)
   125	                code, out = self.check(self.task(BASE.replace(old, new)))
   126	                findings = out.splitlines()[1:]
   127	                self.assertEqual(code, 1, out)
   128	                self.assertEqual(len(findings), 1, out)
   129	                self.assertTrue(findings[0].strip().startswith(check + " "), out)
   130	        # Amendment 1: C14 collapses whitespace runs (a padded count equals its pasted number) and warns on an absent tool.
   131	        padded = BASE.replace(
   132	            "command: printf base\n    output: |-\n      base", "command: printf '%8s' 1\n    output: |-\n      1"
   133	        )
   134	        self.assertEqual(self.check(self.task(padded)), (0, "dotfiles-T9-base-a01.md: OK\n"))
   135	        for cmd in ("no-such-tool-a01 --list", "no-such-tool-a01 --help | /usr/bin/grep -c x"):
   136	            code, out = self.check(self.task(BASE.replace("command: printf base", f"command: {cmd}")))
   137	            self.assertEqual(code, 0, out)
   138	            # stdout holds the verdict alone; the warning is stderr's, so no finding parser reads it.
   139	            warning = (
   140	                "dotfiles-T9-base-a01.md: OK\ndotfiles-T9-base-a01.md: warning: C14: tool absent no-such-tool-a01: "
   141	            )
   142	            self.assertTrue(out.startswith(warning), out)
   143	        current = sorted((ROOT / ".orchestration/tasks").glob("dotfiles-T133-*.md"))
   144	        with self.subTest(green="the current dotfiles-T133 task files"):
   145	            if not current:
   146	                self.skipTest("no dotfiles-T133 task file in this tree yet (they land with a boundary records PR)")
   147	            code, out = self.check(*current, root=ROOT, sha=None)
   148	            others = [l for l in out.splitlines() if l.startswith("  ") and not l.strip().startswith("C14")]
   149	            # Without a trusted sha C14 runs nothing, so the current set is held to C1 to C13 and C15.
   150	            self.assertEqual(others, [], out)
   151	
   152	    def test_c14_executes_premise_commands_only_for_the_dispatched_sha(self):
   153	        # Revise 1 (the Bot's P1 4306960622): a premise command runs only when the file is the orchestrator's dispatched
   154	        # text, whose sha256 the caller passes; for any other file C14 notes it and executes nothing.
   155	        marker = self.repo / "marker"
   156	        path = self.task(BASE.replace("command: printf base", f"command: touch {marker}; printf base"))
   157	        for sha in (None, "0" * 64):
   158	            with self.subTest(sha=sha):
   159	                code, out = self.check(path, sha=sha)
   160	                self.assertEqual((code, marker.exists()), (0, False), out)
   161	                self.assertEqual(out, f"dotfiles-T9-base-a01.md: OK\n{UNTRUSTED}")
   162	        self.assertEqual(self.check(path), (0, "dotfiles-T9-base-a01.md: OK\n"))
   163	        self.assertTrue(marker.exists())
   164	        marker.unlink()
   165	        edited = self.task(BASE.replace("command: printf base", f"command: touch {marker}; printf edited"))
   166	        code, out = self.check(edited)
   167	        self.assertEqual((code, marker.exists()), (1, True), out)
   168	        self.assertIn("C14 premise output differs from its rerun", out)
   169	
   170	    def publish(self, files):
   171	        """Commit files and push them, so origin/main carries them as C10, C12 and C15 read it."""
   172	        for rel, text in files.items():
   173	            (self.repo / rel).parent.mkdir(parents=True, exist_ok=True)
   174	            (self.repo / rel).write_text(text)
   175	        for args in (("add", "-A"), ("commit", "-q", "-m", "publish"), ("push", "-q", "origin", "main")):
   176	            subprocess.run(
   177	                ["git", "-c", "commit.gpgsign=false", *args], cwd=self.repo, env={**os.environ, **GIT_ENV}, check=True
   178	            )
   179	        subprocess.run(["git", "fetch", "-q", "origin"], cwd=self.repo, check=True)
   180	
   181	    def test_c14_without_a_trusted_sha_reports_an_explicit_warning(self):
   182	        # The audit of 9da0ed3 (P2, item 8): with no trusted sha C14 runs nothing and says so as a warning, so a
   183	        # structural OK is never read as premises that passed.
   184	        marker = self.repo / "marker"
   185	        path = self.task(BASE.replace("command: printf base", f"command: touch {marker}; printf base"))
   186	        code, out = self.check(path, sha=None)
   187	        self.assertEqual((code, marker.exists(), out), (0, False, f"dotfiles-T9-base-a01.md: OK\n{UNTRUSTED}"))
   188	
   189	    def test_c15_requires_the_design_assigned_invariant_id_set(self):
   190	        # The audit of 9da0ed3 (P2, item 9): the design's implementing_tasks fixes the task's invariant ids, so an
   191	        # omitted map, a missing or an extra id is a finding as much as a changed sentence.
   192	        one, two = '"the tool prints one line per finding"', '"the tool exits 1 on a finding"'
   193	        design = (
   194	            f"implementing_tasks:\n  dotfiles-T9-base-a01: [INV-1, INV-2]\ninvariants:\n  INV-1: {one}\n  INV-2: {two}"
   195	        )
   196	        self.publish({".orchestration/tasks/dotfiles-T9-design-a01.md": f"---\nformat: 2\n{design}\n---\n\n# design\n"})
   197	        block, d = f"invariants:\n  INV-1: {one}\n", ".orchestration/tasks/dotfiles-T9-design-a01.md"
   198	        missing = f"C15 invariant {{}} that {d} assigns to dotfiles-T9-base-a01 is missing"
   199	        cases = {
   200	            "only INV-1": (block, [missing.format("INV-2")]),
   201	            "no map": ("", [missing.format("INV-1"), missing.format("INV-2")]),
   202	            "an extra id": (
   203	                block + f"  INV-2: {two}\n  INV-3: {two}\n",
   204	                [f"C15 invariant INV-3 is not one {d} assigns to dotfiles-T9-base-a01"],
   205	            ),
   206	            "a changed sentence": (
   207	                block + '  INV-2: "the tool exits 2"\n',
   208	                [f"C15 invariant INV-2 is not byte-equal to {d} on origin/main"],
   209	            ),
   210	            "the whole assignment": (block + f"  INV-2: {two}\n", []),
   211	        }
   212	        typo = ".orchestration/tasks/dotfiles-T9-typo-a01.md"  # the pre-push review of eb20d063: no skip by a typo
   213	        cases["a mistyped design"] = ("", [f"C15 design {typo} is not on origin/main"])
   214	        for name, (invariants, want) in cases.items():
   215	            with self.subTest(case=name):
   216	                task = BASE.replace(block, invariants).replace(d, typo if name == "a mistyped design" else d)
   217	                _, out = self.check(self.task(task))
   218	                self.assertEqual([l.strip() for l in out.splitlines() if l.strip().startswith("C15")], want, out)
   219	
   220	    def test_c12_classifies_concrete_glob_matches_before_the_glob_spelling(self):
   221	        # The audit of 9da0ed3 (P2, items 10 and 19): install/** spells no applied kind, but the shell script it matches
   222	        # is executed, so it needs its concrete row; a tests/fixtures/ glob and the task's own directory stay exempt.
   223	        own = ".orchestration/dotfiles-T9-base-a01/run.sh"
   224	        self.publish({"install/setup.sh": "echo setup\n", "tests/fixtures/x/run.sh": "echo x\n", own: "echo own\n"})
   225	        rows = '  - control: "install/** (the installers)"\n    disposition: "residual: the C12 case\'s glob entry"\n'
   226	        rows += (
   227	            '  - control: "tests/fixtures/x/** (fixtures)"\n    disposition: "residual: the C12 case\'s exempt glob"\n'
   228	        )
   229	        task = BASE.replace("  - scripts/tool.py\n", "  - scripts/tool.py\n  - install/**\n  - tests/fixtures/x/**\n")
   230	        task = task.replace("threat_table:\n", "threat_table:\n" + rows)
   231	        code, out = self.check(self.task(task))
   232	        self.assertEqual(
   233	            (code, out.splitlines()[1:]),
   234	            (1, ["  C12 the glob install/** matches install/setup.sh, which no threat_table row names"]),
   235	        )
   236	        named = '  - control: "install/setup.sh (the setup script)"\n    disposition: "residual: the C12 case\'s concrete row"\n'
   237	        self.assertEqual(
   238	            self.check(self.task(task.replace("threat_table:\n", "threat_table:\n" + named))),
   239	            (0, "dotfiles-T9-base-a01.md: OK\n"),
   240	        )
   241	
   242	    def test_c10_never_passes_a_literal_as_a_git_grep_option(self):
   243	        # PR #418's review (item 20): a backticked literal reaches git grep after -e, so `--open-files-in-pager=<cmd>` is
   244	        # searched for and never run; the old call ran it as soon as the working tree held a match for origin/main.
   245	        marker = self.repo.parent / "pager-ran"
   246	        (self.repo / "scripts/tool.py").write_text("print('origin/main')\n")
   247	        literal = f"--open-files-in-pager=touch {marker}"
   248	        rule = f'\nThe rule: "scripts/tool.py reads `{literal}` before every run of the gate".\n'
   249	        _, out = self.check(self.task(BASE.replace("kind: code", "kind: docs") + rule))
   250	        self.assertFalse(marker.exists(), out)
   251	        self.assertIn(f"C10 rule sentence names scripts/tool.py beside the literal `{literal}`", out)
   252	
   253	    def test_c6_confines_design_paths_to_the_checkout(self):
   254	        # PR #418's review (item 20): a design path that leaves --root is a finding and is never opened.
   255	        outside = self.repo.parent / "outside/design.md"
   256	        outside.parent.mkdir()
   257	        outside.write_text("---\ndesign_review:\n  receipt: r9-outside\n---\n")
   258	        task = BASE.replace("design: .orchestration/tasks/dotfiles-T9-design-a01.md", "design: ../outside/design.md")
   259	        _, out = self.check(self.task(task))
   260	        self.assertIn("C6 design path ../outside/design.md is outside the checkout", out)
   261	        self.assertNotIn("r9-outside", out)
   262	
   263	
   264	if __name__ == "__main__":
   265	    unittest.main()

 succeeded in 97ms:
     1	"""Exercise plan-check.py on a fixture plan group: a clean group passes and each rule's fixture fails with one line.
     2	
     3	plan-check runs through uv with PyYAML; `gh` is a stub on PATH that answers the head written in its calls directory.
     4	"""
     5	
     6	import os
     7	import shutil
     8	import subprocess
     9	import tempfile
    10	import unittest
    11	from pathlib import Path
    12	
    13	ROOT = Path(__file__).resolve().parents[2]
    14	PLAN_CHECK = ROOT / "scripts/orchestrator/plan-check.py"
    15	PLANS = ".orchestration/plans/"
    16	GH = '#!/usr/bin/env bash\nprintf \'{"headRefOid":"%s","mergeStateStatus":"CLEAN","isDraft":false,"state":"OPEN"}\' "$(cat "$CALLS/head")"\n'
    17	
    18	
    19	def task(tid, todo, path):
    20	    return f"---\nformat: 2\nallowed_files:\n  - {path}\n  - .orchestration/{tid}/**\n---\n\n# AGMSG-TASK {tid} — x (plan 024 {todo})\n"
    21	
    22	
    23	CLEAN = {
    24	    PLANS + "024-todo.md": "| # | 目的 | やること | 完了条件 |\n| --- | --- | --- | --- |\n"
    25	    "| P1-1 one | B1 x | (1) | the first done condition |\n| P1-2 two | M1 y | (2) | the second done condition |\n",
    26	    PLANS + "024-design-mechanism.md": "| id | row |\n| --- | --- |\n| B1 | a bottleneck |\n",
    27	    PLANS + "024-design-quality.md": "| id | row |\n| --- | --- |\n| M1 | a mechanism |\n",
    28	    PLANS + "024-checklists.md": "| # | 確認 | 期待 |\n| --- | --- | --- |\n| DoD1 | `make unit-test` | green |\n",
    29	    PLANS + "024-omp-cutover-and-corrective-order.md": "## 2. 決定\n\n| 決定 | 選択肢 | 既定値 |\n| --- | --- | --- |\n"
    30	    "| D1 merge | (a) or (b) | **(a)** because |\n\n## 6. 波\n\n| 波 | a009 | a008 |\n| --- | --- | --- |\n"
    31	    "| P-W0 | P1-1 | P1-2 (#77 at abc1234, dotfiles-T1-one-a01, D-024-01) |\n\n## 7. STOP\n",
    32	    **{
    33	        PLANS + f"024-{n}.md": "# x\n"
    34	        for n in ("design", "design-programs", "design-prs", "design-evidence", "execution")
    35	    },
    36	    PLANS + "024-progress.tsv": "id\tkind\ttitle\tstate\tevidence\tupdated_jst\n",
    37	    ".orchestration/decisions.tsv": "id\twhen\twhat\twhy\tbasis\tresult\nD-024-01\tt\tw\ty\tb\tdefault\n",
    38	    ".orchestration/tasks/dotfiles-T1-one-a01.md": task("dotfiles-T1-one-a01", "P1-1", "scripts/one.py"),
    39	    ".orchestration/tasks/dotfiles-T2-two-a01.md": task("dotfiles-T2-two-a01", "P1-2", "scripts/two.py"),
    40	}
    41	CASES = {
    42	    "F1": (PLANS + "024-todo.md", "| the second done condition |", "|  |"),
    43	    "F2": (".orchestration/tasks/dotfiles-T2-two-a01.md", "scripts/two.py", "scripts/one.py"),
    44	    "F3": (PLANS + "024-todo.md", "| M1 y |", "| y |"),
    45	    "F4": (PLANS + "024-checklists.md", "`make unit-test`", "make unit-test"),
    46	    "F5": (PLANS + "024-omp-cutover-and-corrective-order.md", "**(a)** because", "(a) because"),
    47	    "F6": (PLANS + "024-execution.md", "# x\n", "# x, see dotfiles-T3-missing-a01\n"),
    48	}
    49	
    50	
    51	class PlanCheckTest(unittest.TestCase):
    52	    def setUp(self):
    53	        temp = tempfile.TemporaryDirectory()
    54	        self.addCleanup(temp.cleanup)
    55	        self.root, self.calls, bin_dir = (Path(temp.name).resolve() / d for d in ("root", "calls", "bin"))
    56	        for directory in (self.calls, bin_dir):
    57	            directory.mkdir()
    58	        (bin_dir / "gh").write_text(GH)
    59	        (bin_dir / "gh").chmod(0o755)
    60	        (self.calls / "head").write_text("abc1234" + "0" * 33)
    61	        self.env = {**os.environ, "CALLS": str(self.calls), "STUB_BIN": str(bin_dir)}
    62	        for rel, text in CLEAN.items():
    63	            (self.root / rel).parent.mkdir(parents=True, exist_ok=True)
    64	            (self.root / rel).write_text(text)
    65	
    66	    def plan_check(self, *args):
    67	        # uv run puts its base interpreter's bin directory before PATH (Homebrew's on the macOS runner, which holds a
    68	        # real gh), so the stub goes first inside uv run, as in test_task_checkers.py.
    69	        stub_first = ["sh", "-c", 'PATH="$STUB_BIN:$PATH" exec python -I "$@"', "sh"]
    70	        run = [shutil.which("uv"), "run", "--no-project", "--with", "pyyaml", *stub_first, str(PLAN_CHECK)]
    71	        result = subprocess.run(
    72	            [*run, "--root", str(self.root), *args], env=self.env, capture_output=True, text=True, check=False
    73	        )
    74	        return result.returncode, result.stdout.splitlines()
    75	
    76	    def edit(self, rel, old, new):
    77	        text = (self.root / rel).read_text()
    78	        self.assertEqual(text.count(old), 1, old)
    79	        (self.root / rel).write_text(text.replace(old, new))
    80	        self.addCleanup((self.root / rel).write_text, text)
    81	
    82	    def test_plan_check_reports_each_form_drift_and_invariant_violation_once_and_passes_a_clean_plan(self):
    83	        self.assertEqual(self.plan_check("--drift", "--invariants"), (0, []))
    84	        for rule, (rel, old, new) in CASES.items():
    85	            with self.subTest(rule=rule):
    86	                text = (self.root / rel).read_text()
    87	                self.edit(rel, old, new)
    88	                code, lines = self.plan_check()
    89	                (self.root / rel).write_text(text)
    90	                self.assertEqual(code, 1, lines)
    91	                self.assertEqual(len(lines), 1, lines)
    92	                self.assertTrue(lines[0].startswith(rule + " "), lines)
    93	        with self.subTest(rule="drift"):
    94	            (self.calls / "head").write_text("def4567" + "0" * 33)
    95	            code, lines = self.plan_check("--drift")
    96	            (self.calls / "head").write_text("abc1234" + "0" * 33)
    97	            self.assertEqual((code, len(lines)), (1, 1), lines)
    98	            self.assertRegex(lines[0], r"^drift: 024-omp-cutover-and-corrective-order\.md:\d+ #77 abc1234 != def4567")
    99	        with self.subTest(rule="invariants"):
   100	            self.edit(PLANS + "024-execution.md", "# x\n", "# x\n\nrun gh pr merge 77 --admin\n")
   101	            code, lines = self.plan_check("--invariants")
   102	            self.assertEqual((code, lines), (1, ["invariant: 024-execution.md:3 gh pr merge --admin or --auto"]))
   103	        with self.subTest(rule="F2 glob"):  # a glob entry overlaps the literal path it matches, named concretely
   104	            self.edit(".orchestration/tasks/dotfiles-T1-one-a01.md", "scripts/one.py", "scripts/*.py")
   105	            want = "F2 024-omp-cutover-and-corrective-order.md:11 P-W0 P1-1 and P1-2 share scripts/two.py"
   106	            self.assertEqual(self.plan_check(), (1, [want]))
   107	
   108	    def test_f2_detects_intersecting_globs_through_concrete_tree_matches(self):
   109	        # The audit of 9da0ed3 (P2, item 11): two globs overlap through a file both match in the tree; their spellings
   110	        # never decide disjointness.
   111	        self.edit(".orchestration/tasks/dotfiles-T1-one-a01.md", "scripts/one.py", "scripts/test_*.py")
   112	        self.edit(".orchestration/tasks/dotfiles-T2-two-a01.md", "scripts/two.py", "scripts/*_check.py")
   113	        (self.root / "scripts").mkdir()
   114	        (self.root / "scripts/test_other.py").write_text("")
   115	        self.assertEqual(self.plan_check(), (0, []))
   116	        (self.root / "scripts/test_check.py").write_text("")
   117	        want = "F2 024-omp-cutover-and-corrective-order.md:11 P-W0 P1-1 and P1-2 share scripts/test_check.py"
   118	        self.assertEqual(self.plan_check(), (1, [want]))
   119	
   120	    def test_drift_uses_the_latest_timestamped_acceptance_for_the_same_task(self):
   121	        # The audit of 9da0ed3 (P2, item 16): the task's latest event by timestamp decides, not the last textual match,
   122	        # and another task's event never does.
   123	        line = "[2026-10-18T{}:00:00Z] o → w: AGMSG-ACCEPTANCE v1 task_id=dotfiles-T1-{}-a01 status={}\n"
   124	        record = self.root / ".orchestration/acceptance/dotfiles-T1-one-a01.md"
   125	        record.parent.mkdir(parents=True)
   126	        events = (("05", "one", "accepted"), ("04", "one", "revise"), ("06", "other", "withdrawn"))
   127	        # The pre-push review of eb20d063: each event of a two-event line has its own status, another task's coming
   128	        # first included, and the untimed last line carries 07:00, so its event for one is the latest.
   129	        two = "`AGMSG-ACCEPTANCE v1 task_id=dotfiles-T1-other-a01 status={}` `AGMSG-ACCEPTANCE v1 task_id=dotfiles-T1-one-a01 status={}`\n"
   130	        shared = "[2026-10-18T07:00:00Z] " + two.format("withdrawn", "revise") + two.format("revise", "accepted")
   131	        record.write_text("".join(line.format(*e) for e in events) + shared)
   132	        progress = PLANS + "024-progress.tsv"
   133	        self.edit(progress, "updated_jst\n", "updated_jst\ndotfiles-T1-one-a01\ttask\tone\taccepted\te\tt\n")
   134	        self.assertEqual(self.plan_check("--drift"), (0, []))
   135	        self.edit(progress, "\taccepted\t", "\trevise\t")
   136	        want = "drift: 024-progress.tsv:2 dotfiles-T1-one-a01 revise != accepted"
   137	        self.assertEqual(self.plan_check("--drift"), (1, [want]))
   138	
   139	    def test_drift_checks_every_sha_and_state_for_each_pr_occurrence(self):
   140	        # The audit of 9da0ed3 (P2, item 17): every sha and state near one #<pr> is compared on its own, so a matching
   141	        # head never hides a conflicting state; association stops at the next #<pr>, so a repeated PR's second
   142	        # occurrence carries its own sha and state assertions.
   143	        self.edit(PLANS + "024-execution.md", "# x\n", "# x\n\n#77 abc1234 merged; #77 def4567 abc1234 CLEAN\n")
   144	        code, lines = self.plan_check("--drift")
   145	        live = "abc1234" + "0" * 5
   146	        want = ["drift: 024-execution.md:3 #77 merged != OPEN", f"drift: 024-execution.md:3 #77 def4567 != {live}"]
   147	        self.assertEqual((code, lines), (1, want))
   148	
   149	    def test_invariants_reject_nonempty_quoted_oauth_token_assignments(self):
   150	        # The audit of 9da0ed3 (P2, item 18): quoted and unquoted non-empty values are refused, an empty one is not, and
   151	        # no diagnostic carries the value (built at run time).
   152	        name, value = "ANTHROPIC_OAUTH_" + "TOKEN", "fixture-" + "x" * 8
   153	        self.edit(
   154	            PLANS + "024-execution.md",
   155	            "# x\n",
   156	            f'# x\n\n{name}="{value}"\n{name}=\'{value}\'\n{name}={value}\n{name}=""\n',
   157	        )
   158	        code, lines = self.plan_check("--invariants")
   159	        self.assertEqual(
   160	            (code, lines), (1, [f"invariant: 024-execution.md:{n} {name} with a value" for n in (3, 4, 5)])
   161	        )
   162	        self.assertNotIn(value, "\n".join(lines))
   163	
   164	
   165	if __name__ == "__main__":
   166	    unittest.main()
10-> **Drift check**: `git rev-parse origin/main` is `b896d9bc` or a descendant; the
11-> design `.orchestration/tasks/dotfiles-T128-regime-v3-a01.md` hashes to
12-> `4520b8f0…` (v17 with its `design_review.receipt` naming round 18: hashed keys as in v17 `1d5f4c07…`, round 18 and the round-19 pointer confirmation accepted by both reviewers); the Phase A
13-> task files hash to process-rules a07 `d5d499ce…` (merged in #318 as e83e923d; a04 to a06 superseded), regime-counters a02 `a161f7e7…` (merged, #319), ci-skip a02
14:> `4de54fde…` (merged, #320), A7 parked: PR #323 draft at `dc7edcc0`, task `dotfiles-T128-worker-stop-and-watch-a02` `1de19e51…` (round-7 text `23417dde…` plus four pointer rounds, the a02 reset and one amendment); plan 007 T712 owns the continuation; the a01 dispatch hashes were `65fa3494…`, `69fee495…`, `6dd3d682…` (04:13Z).
15-
16-## Status
17-
18:- **Execution**: IN PROGRESS (Phase A at 01:41Z: PR #318 (A1/A2/A4) merged 01:40:38Z as e83e923d after the a03 to a07 lineage (audit of 92634b25 correct); A7 dispatched to a003 at 01:42Z on a fresh branch from e83e923d (PR #323, draft 01:47:33Z); boundary PR #322 merged 01:48:19Z as b67ea752 (1 min 21 s) and #324 merged 09:38:31Z as d1f98104 (1 min 58 s; plans 007/008 and the M/C records on main), A5's ≤ 10-minute criterion met twice; status at 01:50Z; merged: boundary #321 (09:40Z), A5 PR #320 (21:44Z, main 0e522059), A3 PR #319 (22:03Z, main 52575497: `scripts/regime-counters.sh` and the INV-6 boundary probe are on `main`; the orchestrator now runs the script itself before every acceptance action); PR #318 (A1/A2/A4): a03 updated onto 52575497 (b7ae2d54), audited (4 P2, revise round 1), then Bot P1 on two heads of that round (INV-6 reset to a04 at 22:42Z, record `dotfiles-T128-process-rules-a03-design-reset.md`); a04 amendment 1 at 22:56Z for a third P1 the orchestrator had missed; plan S1 at 23:08Z on the counters bullet (six Bot P1 threads of one class; cause record `.orchestration/learning/plan-006-s1-process-rules-counters-bullet-2026-10-11.md`): a05 by the review seat, the worker continues from 7800ef92 with one commit, then sweep, audit, gate, merge; A7 (PR #323) ran a01 (`84d8acde…` → `b0b84598…`) and a02 (`af519f0f…` → `1de19e51…`), two plan 007 S1 cycles and one INV-6 reset, and was parked as a draft at `dc7edcc0` on 2026-10-12 09:32Z by the operator (plan 008 decision 2, option D2); its content continues as plan 007 T712 (step 7 and step 15 as state tables); boundary #322 merged separately; A6 measured on the T712 PR (A7's PR #323 parked at dc7edcc0 missed it: wall, rounds and resets; heads met); V0 parked for B0)
19-- **Companion plan**: `007-mistakes-into-mechanisms.md` (recorded 2026-10-12 04:32Z at the operator's direction): the linked mistake and correction records, the three-repeat search-first procedure, and STOP S5/S6; its Phase 0 rules are in force for this plan's remaining work, and PR #323 (A7 a02, halted 03:3xZ) resumes only under S5.
20-- **Priority**: P0 (the regime cannot ship implementation while it loops)
21-- **Effort**: L
22-- **Risk**: MED (operator PRs on the critical path of Phases 4 and 6)
--
47-
48-## STOP conditions
49-
50-- **S1 (three repeated findings)**: the same class of finding three times on one artifact (design, task file, PR), from any reviewer, Bot or auditor. Stop that artifact. Switch the orchestrator to `xhigh` effort (operator `/effort xhigh`; effort changes keep the prompt cache on Fable 5.1), re-examine the plan phase that produced the artifact, record the cause in `.orchestration/learning/`, and resume only with a changed task or a changed plan step. Never a fourth round of the same thing.
51:- **S2 (reset)**: INV-6 counts (2 revises, 2 amendments, 2 questions, Bot P0/P1 on 2 post-RESULT heads, audit P0-P1 on 2 heads) stop the task and send it back to design by a context other than its author.
52-- **S3 (metric regression)**: a phase that worsens any of the three metrics against the previous phase's measurement is stopped and re-planned before the next phase.
53-- **S4 (operator boundary)**: any waiver, ruleset change, Actions policy change, or operator PR is named in the acceptance record and never performed silently.
54-
55-## Phase A (operator direction 2026-10-11, approved 「すすめてよい」): establish the recommended pattern before any feature wave
--
57-The order below replaces the earlier interleaving: no implementation wave is dispatched until A1 to A5 are merged and A6 shows the pattern working on itself. V0 (PR #317) is parked at `98f1d250` as a draft and is re-specified under the pattern as the first Phase B task.
58-
59-| # | target | content | verification condition | completion |
60-|---|---|---|---|---|
61:| A1 | SKILL (regime rules) | design review: both reviewers at once, one revision per pair, 3 rounds then freeze with a residual list; task-file review one round with the stop condition; boundary PRs carry records and gate nothing; trust-boundary tasks carry a threat table (what the PR controls, each entry closed / accepted residual with compensating control / out of scope) that is their completion condition | a separate context judges past task files (T119, V0) as failing the stop condition from the text alone | prettier green, docs test green, merged 2026-10-12 01:40:38Z as e83e923d (task `dotfiles-T128-process-rules-a01` → a02 → a03 → a04 → a05 → a06 → a07 on PR #318: six resets, INV-6 on five and plan S1 on two, plus the `bookkeeping` S1 answered by the pre-dispatch check; S1 2026-10-11 23:08Z on the counters bullet changed this row's form: the acceptance-decision bullet states obligations by reference (the script's output pasted; a pasted reading per INV-6 component the script prints as `unknown`; S1 from the record's finding-class table) and names no source; cause record `.orchestration/learning/plan-006-s1-process-rules-counters-bullet-2026-10-11.md`) |
62-| A2 | SKILL Worker Playbook | `gh pr ready` before the Bot wait; at most 2 Bot-fix rounds before RESULT, the third is reported not fixed; revise ACCEPTANCE carries `previous_head` and one failing-test selector per finding | the round cap and the report form appear once in the text | same PR as A1 |
63:| A3 | `scripts/regime-counters.sh` + `check-regime-boundary.sh` | per task from history and GitHub: TASKs, amendments, questions, RESULTs, revises, Bot P0/P1 heads after the first RESULT, audits, wall; S1/S2 thresholds printed; the orchestrator runs it before every acceptance action (rule in A1) | replay on T118 (9 revises by INV-6's count, 10 RESULTs), T119 (9 amendments), T124 W1 (Bot P1 on 2 heads after the first RESULT head), V0 (6 Bot P1 heads after the first RESULT head adcf783b) prints those values and the threshold lines | unit tests, `make check-regime-boundary` green, merged (task `dotfiles-T128-regime-counters-a01`) |
64-| A4 | `AGENTS.md` Code Review Rules | `.orchestration/**` are records and specifications: the Bot reviews them for secrets and home paths only; for trust-boundary code the Bot reviews against the task's threat table and reports missing entries; accepted residuals are not re-raised | the next `.orchestration`-only PR draws no design thread from the Bot | same PR as A1 |
65-| A5 | `remote.yaml`, `test.yaml` | `.orchestration`-only diffs skip the heavy steps with step-level `if`s; every required context reports success; push and schedule always run | an `.orchestration`-only PR merges within 10 minutes with every required check reported | `gh pr checks` timings in the acceptance record (task `dotfiles-T128-ci-skip-orchestration-a01`) |
66-| A6 | self-verification | first run on A3's PR #319 (a01 → a02): rounds ≤ 2 and Bot P0/P1 heads ≤ 2 were met, wall was 3 h 26 min against ≤ 2 h (two orchestrator specification gaps and one reset; cause and figures in `.orchestration/acceptance/dotfiles-T128-regime-counters-a02.md`), so the wall criterion is not met by A3 and A6 is re-run on A7's PR (the next Phase A PR, under the worker self-stop rule it introduces) with the same three criteria; the A3 figures stand as the pattern's first measurement | rounds ≤ 2, wall ≤ 2 h, Bot heads ≤ 2 on A7's PR | the three metrics in A7's acceptance record; Phase B (B0) starts only after that record shows the criteria met, or the operator re-plans the criterion |
67:| A7 | SKILL Worker Playbook step 15 + Orchestrator Playbook step 7 (`dotfiles-T128-worker-stop-and-watch-a01`, after process-rules-a07 (merged) and regime-counters-a02) | worker-side stop: before each fix commit the worker counts Bot P0/P1 heads after its first RESULT head and Bot thread classes from its step-15 listing and stops at 2 heads (INV-6) or 3 of a class (S1) with `AGMSG-PONG status=blocked note=S1|INV-6;heads=…;classes=…;threads=…`; before each push it runs `regime-counters.sh --history-only`; orchestrator-side watch: GitHub and history every 30 minutes after a TASK, PING at 45 minutes without a push, PONG or RESULT, despawn when the PING stays unread while pushes continue past a cap or count; hook-level enforcement stays V3a's; PARKED 2026-10-12 09:32Z at PR #323 `dc7edcc0` (plan 008 decision 2): the rules land through plan 007 T712 as state tables; A7 edits step 15 and step 7, so its commit updates `tests/fixtures/regime/worker-step-15.md` and `orchestrator-step-7.md` (a05 item 10's golden sections) and its `allowed_files` names them; one more finding of the `step15-wait` class on A7's PR stops A7 for a re-specification of step 15 as one state machine | fourteen docs-test tokens, each failing when its sentence is removed, and the two section fixtures updated in the same commit; the worker rule exercised on A7's own PR | merged with its audit `correct` |
68-
69-**Correction (2026-10-11 07:25Z, from the audits of PR 320):** the Phase 0 rule that a boundary PR is never a dispatch prerequisite contradicts INV-2's hashed sentence (the design must be on `main` before the implementing TASK is dispatched, and the task's invariant sentence must equal `main`'s). INV-2 wins: a hashed design change lands on `main` through a boundary PR before any task that carries one of its sentences is dispatched; a boundary PR still carries no task draft under review. For the Phase A tasks already dispatched under the old rule, the boundary PR `orchestration/boundary-2026-10-11-2` carries design v16 before their final audits and merges, and each PR takes the new base with `gh pr update-branch`. The A1 bullet on `main` after PR #318 says the same (a follow-up docs item if its wording still carries the old sentence).
70-
71-Dormant-contract PRs are withdrawn from the pattern (Phase B's first design change narrows INV-12 to the undeclared-mode regression guard); `dotfiles-T128-ci-skip-orchestration-contract-a01` is superseded.
72-
73:Notes carried into Phase B task files from the Phase A review (2026-10-11): V1's `schemas/task.json` takes `threat_table` as an optional list of `{control, disposition}` with `disposition` matching `^(closed|residual|out-of-scope): ` and `after` as an optional list of task ids (PR-2); the design's INV-6 enforcement row and V3a bullet name `scripts/regime-counters.sh`, and the design's own `design_review.receipt` moves to round 16, at the next hashed change (round-16 Claude notes).
74-
75-## Phases (bottleneck order), atomic tasks, verification, completion (Phase B onward, after A6)
76-
77-### Phase 1: remove the loop sources (bottleneck 1: rounds)
78-
79:- **A101, A102**: executed in Phase A (A1/A2/A4 on PR #318 as `process-rules-a01` → a02 → a03 → a04 → a05 → a06 → a07, merged as e83e923d; the map amendments as design rounds 16 to 19). No Phase B work remains here.
80-
81-### Phase 2: remove the CI wait (bottleneck 2: boundary and PR wall time)
82-
83-- **A201**: executed in Phase A (A5 on PR #320 as `ci-skip-orchestration-a01` → a02, in-job fail-closed decision, no `changes` job, no `needs`). The ≤ 10-minute measurement is taken on the first `.orchestration`-only PR after its merge and pasted into its acceptance record.
84-
85-### Phase 3: deterministic verification first (bottleneck 1 again: rounds come from model-judged review)
86-
87:- **B0** DONE 11:52Z as design v20 `ed51f1d4…` (plan 007 T701; rounds 20 to 22, both reviewers accept at round 22; the V0 successor is `dotfiles-T128-v0-main-tests-a02`, the gate task `dotfiles-T128-gate-evidence-a01`; the SKILL's `-contract-a01` clause leaves through `dotfiles-T128-playbook-rules-a01`, V1b's through its own re-specification). Original row: design amendment (one review pair, then a boundary PR before any Phase B dispatch, as INV-2 requires): INV-12 narrowed to the undeclared-change regression guard; the dormant-contract clause removed; `main-tests` decides inside its own job like A5's workflows (no `changes` job, no `needs`). B0's hashed changes also add the V0 successor's `implementing_tasks` entry (`<new V0 id>: [INV-12]`, beside the parked a01 entry) and any other Phase B successor id, so INV-2's map lookup holds for them on `main` before dispatch. B0 also re-specifies every Phase B task file that touches a trust boundary (V1, V1b, V1c, V2, V2b, V3a to V3d, V4, V5a, V5b, V6) with a `threat_table` and the A1 rules (premises as pasted output, one task-file review round each) before its dispatch; no Phase B task is dispatched from its pre-Phase-A text.
88-- **A301** V0: re-specified under the pattern by a context other than its author as a new task id (PR #317 stays parked as input: its 14 Bot threads and the audit of `adcf783b`), with a threat table, the in-job decision A5 established, and the narrowed INV-12 from B0.
89-  - Verification condition: the six named test selectors fail on `adcf783b` and pass on the new head; the audit of the new head is `correct`; `main-tests` runs main's harness against the PR.
90-  - Verification content: validation file with both runs pasted; audit `.last.md`; CI log of `main-tests` on the new head.
91-  - Completion: merged with `--match-head-commit`; `main-tests` listed as a required check (S4: named in the acceptance record); acceptance record carries rounds, wall, audit count.
--
114-
115-### Phase 6: the reset made mechanical
116-
117-- **A601** V3a (operator PR: counters in the gate and the Stop hooks, `regime-waive.sh`, boundary detector), **A602** V3b, **A603** V3c, **A604** V3d.
118:  - Verification: a replay of T119's history against the counters fires the reset at the amendment count; a replay of this plan's own design-review history fires S1 at round 3.
119-  - Completion: merged; the replays pasted in the acceptance records.
120-  - Metric: rounds per artifact (hard-stopped).
121-
122-### Phase 7: the rest

**Seeking quick progress**
codex
I found an evidence mismatch: the worker reports the template fix at `eb20d063`, but the final-head feedback JSON still credits `b3c6b7ea`, which the task explicitly identifies as an incomplete fix. I’m also checking whether the checker’s path and invariant guarantees hold beyond the covered fixtures.
exec
/bin/zsh -lc "git show 8a09b9365932f23b09df8aa2385a93d0b3016a3e:.orchestration/dotfiles-T133-task-generator-plan-check-a02/validation.md | nl -ba | sed -n '1,220p'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc "git show 8a09b9365932f23b09df8aa2385a93d0b3016a3e:.orchestration/dotfiles-T133-task-generator-plan-check-a02/validation.md | nl -ba | sed -n '221,450p'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc "python3 -B -c 'import yaml; print(yaml.__version__)' && git grep -n 'INV-6:' 8a09b9365932f23b09df8aa2385a93d0b3016a3e -- '.orchestration/tasks/*design*' && git show b3c6b7ea --stat && git show 8a09b9365932f23b09df8aa2385a93d0b3016a3e:.orchestration/dotfiles-T133-task-generator-plan-check-a02/measure.md && git show 8a09b9365932f23b09df8aa2385a93d0b3016a3e:.orchestration/dotfiles-T133-task-generator-plan-check-a02/sandbox.md" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 119ms:
     1	---
     2	task_id: dotfiles-T133-task-generator-plan-check-a02
     3	round: 1
     4	code_head: 6e07d29193e9a3b56b299dd9d55538788bc48b7b
     5	merge_base: 3e41e36abc949acd7e6b4859c1a22df9e665c8d4
     6	---
     7	
     8	# Validation
     9	
    10	Every block is the command's own output, run in the seat's sandbox (sandbox.md). A block names its tested revision. "Exact id" means `uv run python -m unittest <module>.<Class>.<name>`; no proof uses `-k`.
    11	
    12	## Task copy
    13	
    14	```
    15	$ shasum -a 256 .orchestration/dotfiles-T133-task-generator-plan-check-a02/task.md
    16	a3ab8ea6addda207fa9a9ff5d96921e080dab7a1025117f33cbd087e6b805f98  .orchestration/dotfiles-T133-task-generator-plan-check-a02/task.md
    17	$ git show --stat --format=%H 6da92853
    18	6da92853c6d05013020b6337eeac80eb07020952
    19	
    20	 .../task.md                                        | 111 ----------
    21	 .../task.md                                        | 231 +++++++++++++++++++++
    22	 2 files changed, 231 insertions(+), 111 deletions(-)
    23	```
    24	
    25	## Red: the fifteen new regressions and the updated end-to-end test against 9da0ed3f (exact id)
    26	
    27	Each run copies the code head's test modules (hashes below) into a scratch worktree of the production commit, which is removed afterwards. Every run is `Ran 1 test` with failures only and no errors.
    28	
    29	```
    30	production=9da0ed3fe67fd1f9267c56fcdcb7e5aaaaa9ffab, test sources from the working tree of 6e07d291:
    31	  453823892bb6e5cd50dd2e7371a0035bc90cbd65fbc0836c1a6b088a497ad4d4  tests/unit/test_task_from_plan.py
    32	  c1b198a933cade44456943338b94d2dba407c331be46fc9a193180bce1462fa7  tests/unit/test_task_consistency_c11_c15.py
    33	  ff8202456c02e2d67bf36feec40c58261559ac8054c43ef770993eff30d936c2  tests/unit/test_plan_check.py
    34	$ uv run python -m unittest tests.unit.test_task_from_plan.TaskFromPlanTest.test_a_generated_task_passes_the_consistency_check_and_pastes_real_premise_outputs
    35	exit=1
    36	FAIL: test_a_generated_task_passes_the_consistency_check_and_pastes_real_premise_outputs
    37	AssertionError: '- `make unit-test`: exit 0 on origin/main 0324ae26c3fb' not found in "---\nformat: 2\ntask_id: dotfiles-T9-demo-a01\nkind: code\nsecurity: true\nallowed_files:\n- scripts/demo.sh\n- tests/unit/test_demo.
    38	Ran 1 test in 0.456s
    39	FAILED (failures=1)
    40	$ uv run python -m unittest tests.unit.test_task_from_plan.TaskFromPlanTest.test_generator_uses_the_bundled_template_without_task_records
    41	exit=1
    42	FAIL: test_generator_uses_the_bundled_template_without_task_records
    43	AssertionError: 1 != 0 : task-from-plan: missing under /private/tmp/claude-501/tmpi0fkpm5v/repo: .orchestration/tasks/dotfiles-T133-result-precheck-a01.md, .orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a0
    44	Ran 1 test in 0.431s
    45	FAILED (failures=1)
    46	$ uv run python -m unittest tests.unit.test_task_from_plan.TaskFromPlanTest.test_generator_refuses_dirty_plan_commands_before_execution
    47	exit=1
    48	FAIL: test_generator_refuses_dirty_plan_commands_before_execution (dirty='unstaged')
    49	AssertionError: Tuples differ: (False, True, {'format': 2, 'task_id': 'do[2278 chars]'}]}) != (True, False, None)
    50	FAIL: test_generator_refuses_dirty_plan_commands_before_execution (dirty='staged')
    51	AssertionError: Tuples differ: (False, True, {'format': 2, 'task_id': 'do[2278 chars]'}]}) != (True, False, None)
    52	FAIL: test_generator_refuses_dirty_plan_commands_before_execution (dirty='untracked')
    53	AssertionError: Tuples differ: (False, True, {'format': 2, 'task_id': 'do[2278 chars]'}]}) != (True, False, None)
    54	FAIL: test_generator_refuses_dirty_plan_commands_before_execution
    55	AssertionError: 'plan group at 8d29699d4f933cd439a75828c760016bddf60613' not found in "---\nformat: 2\ntask_id: dotfiles-T9-demo-a01\nkind: code\nsecurity: true\nallowed_files:\n- scripts/demo.sh\n- tests/unit/test_demo.
    56	Ran 1 test in 1.382s
    57	FAILED (failures=4)
    58	$ uv run python -m unittest tests.unit.test_task_from_plan.TaskFromPlanTest.test_wave_selection_matches_whole_todo_ids
    59	exit=1
    60	FAIL: test_wave_selection_matches_whole_todo_ids
    61	AssertionError: 'wave P-W1' not found in "---\nformat: 2\ntask_id: dotfiles-T9-demo-a01\nkind: code\nsecurity: true\nallowed_files:\n- scripts/demo.sh\n- tests/unit/test_demo.py\n- .orchestration/dotfiles-T9-demo-a01/**\
    62	Ran 1 test in 0.683s
    63	FAILED (failures=1)
    64	$ uv run python -m unittest tests.unit.test_task_from_plan.TaskFromPlanTest.test_generator_preserves_wildcard_scopes_and_their_threat_rows
    65	exit=1
    66	FAIL: test_generator_preserves_wildcard_scopes_and_their_threat_rows
    67	AssertionError: False is not true : ['scripts/demo.sh', 'tests/unit/test_demo.py', '.orchestration/dotfiles-T9-demo-a01/**']
    68	Ran 1 test in 0.679s
    69	FAILED (failures=1)
    70	$ uv run python -m unittest tests.unit.test_task_from_plan.TaskFromPlanTest.test_program_item_continues_until_the_next_numbered_heading
    71	exit=1
    72	FAIL: test_program_item_continues_until_the_next_numbered_heading
    73	AssertionError: 'scripts/late.sh' not found in ['scripts/demo.sh', 'tests/unit/test_demo.py', '.orchestration/dotfiles-T9-demo-a01/**']
    74	Ran 1 test in 0.726s
    75	FAILED (failures=1)
    76	$ uv run python -m unittest tests.unit.test_task_from_plan.TaskFromPlanTest.test_generator_retains_unavailable_single_word_and_redirecting_commands
    77	exit=1
    78	FAIL: test_generator_retains_unavailable_single_word_and_redirecting_commands
    79	AssertionError: False is not true : {'printf known-output': {'claim': 'the program item quotes `printf known-output`', 'command': 'printf known-output', 'output': 'known-output'}}
    80	Ran 1 test in 1.043s
    81	FAILED (failures=1)
    82	$ uv run python -m unittest tests.unit.test_plan_check.PlanCheckTest.test_f2_detects_intersecting_globs_through_concrete_tree_matches
    83	exit=1
    84	FAIL: test_f2_detects_intersecting_globs_through_concrete_tree_matches
    85	AssertionError: Tuples differ: (0, []) != (1, ['F2 024-omp-cutover-and-corrective-or[54 chars]py'])
    86	Ran 1 test in 0.166s
    87	FAILED (failures=1)
    88	$ uv run python -m unittest tests.unit.test_plan_check.PlanCheckTest.test_drift_uses_the_latest_timestamped_acceptance_for_the_same_task
    89	exit=1
    90	FAIL: test_drift_uses_the_latest_timestamped_acceptance_for_the_same_task
    91	AssertionError: Tuples differ: (1, ['drift: 024-progress.tsv:2 dotfiles-T1-one-a01 accepted != accepted`']) != (0, [])
    92	Ran 1 test in 0.111s
    93	FAILED (failures=1)
    94	$ uv run python -m unittest tests.unit.test_plan_check.PlanCheckTest.test_drift_checks_every_sha_and_state_for_each_pr_occurrence
    95	exit=1
    96	FAIL: test_drift_checks_every_sha_and_state_for_each_pr_occurrence
    97	AssertionError: Tuples differ: (1, [[26 chars] #77 def4567 != abc123400000']) != (1, [[26 chars] #77 merged != OPEN', 'drift: 024-execution.md[28 chars]00'])
    98	Ran 1 test in 0.122s
    99	FAILED (failures=1)
   100	$ uv run python -m unittest tests.unit.test_plan_check.PlanCheckTest.test_invariants_reject_nonempty_quoted_oauth_token_assignments
   101	exit=1
   102	FAIL: test_invariants_reject_nonempty_quoted_oauth_token_assignments
   103	AssertionError: Tuples differ: (1, [[24 chars]n.md:5 ANTHROPIC_OAUTH_TOKEN with a value']) != (1, [[24 chars]n.md:3 ANTHROPIC_OAUTH_TOKEN with a value', 'i[129 chars]ue'])
   104	Ran 1 test in 0.084s
   105	FAILED (failures=1)
   106	$ uv run python -m unittest tests.unit.test_task_consistency_c11_c15.TaskConsistencyC11C15Test.test_c14_without_a_trusted_sha_reports_an_explicit_warning
   107	exit=1
   108	FAIL: test_c14_without_a_trusted_sha_reports_an_explicit_warning
   109	AssertionError: Tuples differ: (0, F[40 chars]iles-T9-base-a01.md: C14: not run (no trusted sha)\n') != (0, F[40 chars]iles-T9-base-a01.md: warning: C14: not run (no trusted sha)\n')
   110	Ran 1 test in 0.303s
   111	FAILED (failures=1)
   112	$ uv run python -m unittest tests.unit.test_task_consistency_c11_c15.TaskConsistencyC11C15Test.test_c15_requires_the_design_assigned_invariant_id_set
   113	exit=1
   114	FAIL: test_c15_requires_the_design_assigned_invariant_id_set (case='only INV-1')
   115	AssertionError: Lists differ: [] != ['C15 invariant INV-2 that .orchestration/[71 chars]ing']
   116	FAIL: test_c15_requires_the_design_assigned_invariant_id_set (case='no map')
   117	AssertionError: Lists differ: [] != ['C15 invariant INV-1 that .orchestration/[189 chars]ing']
   118	FAIL: test_c15_requires_the_design_assigned_invariant_id_set (case='an extra id')
   119	AssertionError: Lists differ: ['C15[19 chars] not byte-equal to .orchestration/tasks/dotfil[31 chars]ain'] != ['C15[19 chars] not one .orchestration/tasks/dotfiles-T9-desi[38 chars]a01']
   120	FAIL: test_c15_requires_the_design_assigned_invariant_id_set (case='a mistyped design')
   121	AssertionError: Lists differ: [] != ['C15 design .orchestration/tasks/dotfiles[34 chars]ain']
   122	Ran 1 test in 0.911s
   123	FAILED (failures=4)
   124	$ uv run python -m unittest tests.unit.test_task_consistency_c11_c15.TaskConsistencyC11C15Test.test_c12_classifies_concrete_glob_matches_before_the_glob_spelling
   125	exit=1
   126	FAIL: test_c12_classifies_concrete_glob_matches_before_the_glob_spelling
   127	AssertionError: Tuples differ: (0, []) != (1, ['  C12 the glob install/** matches in[45 chars]es'])
   128	Ran 1 test in 0.492s
   129	FAILED (failures=1)
   130	$ uv run python -m unittest tests.unit.test_task_consistency_c11_c15.TaskConsistencyC11C15Test.test_c10_never_passes_a_literal_as_a_git_grep_option
   131	exit=1
   132	FAIL: test_c10_never_passes_a_literal_as_a_git_grep_option
   133	AssertionError: True is not false : dotfiles-T9-base-a01.md: OK
   134	Ran 1 test in 0.433s
   135	FAILED (failures=1)
   136	$ uv run python -m unittest tests.unit.test_task_consistency_c11_c15.TaskConsistencyC11C15Test.test_c6_confines_design_paths_to_the_checkout
   137	exit=1
   138	FAIL: test_c6_confines_design_paths_to_the_checkout
   139	AssertionError: 'C6 design path ../outside/design.md is outside the checkout' not found in "dotfiles-T9-base-a01.md: FAIL\n  C6 design_review.receipt r1 is not the design's current receipt r9-outside\n  C15 invariant INV
   140	Ran 1 test in 0.404s
   141	FAILED (failures=1)
   142	removed=0
   143	```
   144	
   145	## Red: the retained C14 gate against ff4d25a8, the revision before it (item 7)
   146	
   147	```
   148	production=ff4d25a89fcf301fddd6cd218aa6c9c91fe4a6ad, test sources from the working tree of 6e07d291:
   149	  c1b198a933cade44456943338b94d2dba407c331be46fc9a193180bce1462fa7  tests/unit/test_task_consistency_c11_c15.py
   150	$ uv run python -m unittest tests.unit.test_task_consistency_c11_c15.TaskConsistencyC11C15Test.test_c14_executes_premise_commands_only_for_the_dispatched_sha
   151	exit=1
   152	FAIL: test_c14_executes_premise_commands_only_for_the_dispatched_sha (sha=None)
   153	AssertionError: Tuples differ: (0, True) != (0, False)
   154	FAIL: test_c14_executes_premise_commands_only_for_the_dispatched_sha (sha='0000000000000000000000000000000000000000000000000000000000000000')
   155	AssertionError: Tuples differ: (2, True) != (0, False)
   156	FAIL: test_c14_executes_premise_commands_only_for_the_dispatched_sha
   157	AssertionError: Tuples differ: (2, 'usage: task-consistency-check.py [-h][109 chars]a\n') != (0, 'dotfiles-T9-base-a01.md: OK\n')
   158	Ran 1 test in 0.450s
   159	FAILED (failures=3)
   160	removed=0
   161	```
   162	
   163	## Red: the correction round's cases against eb20d063, the reviewed head
   164	
   165	The item 16 case, the mistyped-design case of C15 and the C7b case of the wildcard test fail there. The item 17 and C12 additions fill coverage gaps, so they pass there, and they are red against 9da0ed3f above.
   166	
   167	```
   168	production=eb20d063e0a73b17fca84df4689225b0005cf867, test sources from the working tree of 6e07d291:
   169	  453823892bb6e5cd50dd2e7371a0035bc90cbd65fbc0836c1a6b088a497ad4d4  tests/unit/test_task_from_plan.py
   170	  c1b198a933cade44456943338b94d2dba407c331be46fc9a193180bce1462fa7  tests/unit/test_task_consistency_c11_c15.py
   171	  ff8202456c02e2d67bf36feec40c58261559ac8054c43ef770993eff30d936c2  tests/unit/test_plan_check.py
   172	$ uv run python -m unittest tests.unit.test_plan_check.PlanCheckTest.test_drift_uses_the_latest_timestamped_acceptance_for_the_same_task
   173	exit=1
   174	FAIL: test_drift_uses_the_latest_timestamped_acceptance_for_the_same_task
   175	AssertionError: Tuples differ: (1, ['drift: 024-progress.tsv:2 dotfiles-T1-one-a01 accepted != withdrawn`']) != (0, [])
   176	Ran 1 test in 0.113s
   177	FAILED (failures=1)
   178	$ uv run python -m unittest tests.unit.test_plan_check.PlanCheckTest.test_drift_checks_every_sha_and_state_for_each_pr_occurrence
   179	exit=0
   180	Ran 1 test in 0.111s
   181	OK
   182	$ uv run python -m unittest tests.unit.test_task_consistency_c11_c15.TaskConsistencyC11C15Test.test_c15_requires_the_design_assigned_invariant_id_set
   183	exit=1
   184	FAIL: test_c15_requires_the_design_assigned_invariant_id_set (case='a mistyped design')
   185	AssertionError: Lists differ: [] != ['C15 design .orchestration/tasks/dotfiles[34 chars]ain']
   186	Ran 1 test in 0.953s
   187	FAILED (failures=1)
   188	$ uv run python -m unittest tests.unit.test_task_consistency_c11_c15.TaskConsistencyC11C15Test.test_c12_classifies_concrete_glob_matches_before_the_glob_spelling
   189	exit=0
   190	Ran 1 test in 0.752s
   191	OK
   192	$ uv run python -m unittest tests.unit.test_task_from_plan.TaskFromPlanTest.test_generator_preserves_wildcard_scopes_and_their_threat_rows
   193	exit=1
   194	FAIL: test_generator_preserves_wildcard_scopes_and_their_threat_rows
   195	AssertionError: 1 != 0 : dotfiles-T9-demo-a01.md: FAIL
   196	Ran 1 test in 1.103s
   197	FAILED (failures=1)
   198	removed=0
   199	```
   200	
   201	## Green: the four task modules on 6e07d291
   202	
   203	```
   204	$ uv run python -m unittest tests.unit.test_task_from_plan tests.unit.test_plan_check tests.unit.test_task_consistency_c11_c15 tests.unit.test_task_checkers -v
   205	test_a_generated_task_passes_the_consistency_check_and_pastes_real_premise_outputs (tests.unit.test_task_from_plan.TaskFromPlanTest.test_a_generated_task_passes_the_consistency_check_and_pastes_real_premise_outputs) ... ok
   206	test_generator_preserves_wildcard_scopes_and_their_threat_rows (tests.unit.test_task_from_plan.TaskFromPlanTest.test_generator_preserves_wildcard_scopes_and_their_threat_rows) ... ok
   207	test_generator_refuses_dirty_plan_commands_before_execution (tests.unit.test_task_from_plan.TaskFromPlanTest.test_generator_refuses_dirty_plan_commands_before_execution) ... ok
   208	test_generator_retains_unavailable_single_word_and_redirecting_commands (tests.unit.test_task_from_plan.TaskFromPlanTest.test_generator_retains_unavailable_single_word_and_redirecting_commands) ... ok
   209	test_generator_uses_the_bundled_template_without_task_records (tests.unit.test_task_from_plan.TaskFromPlanTest.test_generator_uses_the_bundled_template_without_task_records) ... ok
   210	test_program_item_continues_until_the_next_numbered_heading (tests.unit.test_task_from_plan.TaskFromPlanTest.test_program_item_continues_until_the_next_numbered_heading) ... ok
   211	test_wave_selection_matches_whole_todo_ids (tests.unit.test_task_from_plan.TaskFromPlanTest.test_wave_selection_matches_whole_todo_ids) ... ok
   212	test_drift_checks_every_sha_and_state_for_each_pr_occurrence (tests.unit.test_plan_check.PlanCheckTest.test_drift_checks_every_sha_and_state_for_each_pr_occurrence) ... ok
   213	test_drift_uses_the_latest_timestamped_acceptance_for_the_same_task (tests.unit.test_plan_check.PlanCheckTest.test_drift_uses_the_latest_timestamped_acceptance_for_the_same_task) ... ok
   214	test_f2_detects_intersecting_globs_through_concrete_tree_matches (tests.unit.test_plan_check.PlanCheckTest.test_f2_detects_intersecting_globs_through_concrete_tree_matches) ... ok
   215	test_invariants_reject_nonempty_quoted_oauth_token_assignments (tests.unit.test_plan_check.PlanCheckTest.test_invariants_reject_nonempty_quoted_oauth_token_assignments) ... ok
   216	test_plan_check_reports_each_form_drift_and_invariant_violation_once_and_passes_a_clean_plan (tests.unit.test_plan_check.PlanCheckTest.test_plan_check_reports_each_form_drift_and_invariant_violation_once_and_passes_a_clean_plan) ... ok
   217	test_c10_never_passes_a_literal_as_a_git_grep_option (tests.unit.test_task_consistency_c11_c15.TaskConsistencyC11C15Test.test_c10_never_passes_a_literal_as_a_git_grep_option) ... ok
   218	test_c12_classifies_concrete_glob_matches_before_the_glob_spelling (tests.unit.test_task_consistency_c11_c15.TaskConsistencyC11C15Test.test_c12_classifies_concrete_glob_matches_before_the_glob_spelling) ... ok
   219	test_c14_executes_premise_commands_only_for_the_dispatched_sha (tests.unit.test_task_consistency_c11_c15.TaskConsistencyC11C15Test.test_c14_executes_premise_commands_only_for_the_dispatched_sha) ... ok
   220	test_c14_without_a_trusted_sha_reports_an_explicit_warning (tests.unit.test_task_consistency_c11_c15.TaskConsistencyC11C15Test.test_c14_without_a_trusted_sha_reports_an_explicit_warning) ... ok

 succeeded in 165ms:
   221	test_c15_requires_the_design_assigned_invariant_id_set (tests.unit.test_task_consistency_c11_c15.TaskConsistencyC11C15Test.test_c15_requires_the_design_assigned_invariant_id_set) ... ok
   222	test_c6_confines_design_paths_to_the_checkout (tests.unit.test_task_consistency_c11_c15.TaskConsistencyC11C15Test.test_c6_confines_design_paths_to_the_checkout) ... ok
   223	test_each_new_check_is_red_on_its_fixture_and_the_existing_checks_are_unchanged (tests.unit.test_task_consistency_c11_c15.TaskConsistencyC11C15Test.test_each_new_check_is_red_on_its_fixture_and_the_existing_checks_are_unchanged) ... 
   224	  test_each_new_check_is_red_on_its_fixture_and_the_existing_checks_are_unchanged (tests.unit.test_task_consistency_c11_c15.TaskConsistencyC11C15Test.test_each_new_check_is_red_on_its_fixture_and_the_existing_checks_are_unchanged) (green='the current dotfiles-T133 task files') ... skipped 'no dotfiles-T133 task file in this tree yet (they land with a boundary records PR)'
   225	test_ledger_check_counts_what_the_gate_counts (tests.unit.test_task_checkers.TaskCheckersTest.test_ledger_check_counts_what_the_gate_counts) ... ok
   226	test_ledger_check_passes_a_complete_record (tests.unit.test_task_checkers.TaskCheckersTest.test_ledger_check_passes_a_complete_record) ... ok
   227	test_ledger_check_reads_inherited_audit_ids_from_the_marker (tests.unit.test_task_checkers.TaskCheckersTest.test_ledger_check_reads_inherited_audit_ids_from_the_marker) ... ok
   228	test_ledger_check_reports_the_gaps_of_the_pre_fix_record (tests.unit.test_task_checkers.TaskCheckersTest.test_ledger_check_reports_the_gaps_of_the_pre_fix_record) ... ok
   229	test_task_consistency_check_c4_names_an_entry_only_at_a_path_boundary (tests.unit.test_task_checkers.TaskCheckersTest.test_task_consistency_check_c4_names_an_entry_only_at_a_path_boundary) ... ok
   230	test_task_consistency_check_c9_probes_the_landed_checker_path (tests.unit.test_task_checkers.TaskCheckersTest.test_task_consistency_check_c9_probes_the_landed_checker_path) ... ok
   231	test_task_consistency_check_detects_the_ten_historical_files (tests.unit.test_task_checkers.TaskCheckersTest.test_task_consistency_check_detects_the_ten_historical_files) ... ok
   232	test_task_consistency_check_passes_a_complete_task_file (tests.unit.test_task_checkers.TaskCheckersTest.test_task_consistency_check_passes_a_complete_task_file) ... ok
   233	test_task_consistency_check_reaches_every_other_check (tests.unit.test_task_checkers.TaskCheckersTest.test_task_consistency_check_reaches_every_other_check) ... ok
   234	
   235	----------------------------------------------------------------------
   236	Ran 28 tests in 26.653s
   237	
   238	OK (skipped=1)
   239	```
   240	
   241	The one skip is the green-set subtest of `test_each_new_check_is_red_on_its_fixture_and_the_existing_checks_are_unchanged`. It runs once the T133 task files are on `main`.
   242	
   243	## Green: the other modules that run these scripts
   244	
   245	```
   246	$ uv run python -m unittest tests.unit.test_orchestrator_tools tests.unit.test_agmsg_orchestration_docs
   247	Ran 110 tests in 69.920s
   248	OK
   249	```
   250	
   251	## make unit-test: 6e07d291, and pristine origin/main 3e41e36a in the same sandbox
   252	
   253	```
   254	$ make unit-test   (a detached scratch worktree of 6e07d291, removed afterwards)
   255	Ran 1226 tests in 756.051s
   256	FAILED (failures=194, errors=111, skipped=3)
   257	make: *** [unit-test] Error 1
   258	$ make unit-test   (a detached scratch worktree of 3e41e36a, removed afterwards)
   259	Ran 1207 tests in 1111.171s
   260	FAILED (failures=194, errors=111, skipped=2)
   261	make: *** [unit-test] Error 1
   262	failing names: 310 on 6e07d291, 310 on 3e41e36a; identical: True
   263	new failing names on 6e07d291: none
   264	```
   265	
   266	Each failing name is a sandbox-denied operation, the same on both sides, and none is in this task's modules. The extra tests on 6e07d291 are this task's, and all pass. CI's `make unit-test` decides the full suite.
   267	
   268	## make format: 6e07d291, and pristine origin/main 3e41e36a
   269	
   270	```
   271	$ make format   (6e07d291)
   272	make: *** [format] Error 1
   273	shfmt --diff files: .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/pr-cost.sh, .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/resolve-threads.sh, .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-advisory.sh, .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-review.sh, .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/sandbox-scan.sh, .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/boundary.sh, .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/ff-main.sh, .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-audit.sh, .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-gate.sh, .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/t717-prep.sh, home/dot_claude/hooks/executable_project-map-reload.sh, tests/install/macos/common/brew.bats
   274	$ make format   (3e41e36a)
   275	make: *** [format] Error 1
   276	shfmt --diff files: .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/pr-cost.sh, .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/resolve-threads.sh, .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-advisory.sh, .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-review.sh, .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/sandbox-scan.sh, .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/boundary.sh, .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/ff-main.sh, .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-audit.sh, .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-gate.sh, .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/t717-prep.sh, home/dot_claude/hooks/executable_project-map-reload.sh, tests/install/macos/common/brew.bats
   277	identical: True
   278	```
   279	
   280	`make format` stops at its first command, `shfmt --diff .`, on the same twelve pre-existing files, so its ruff and prettier lines never run. They are run here on every changed file:
   281	
   282	```
   283	7 files already formatted
   284	ruff=0
   285	Checking formatting...
   286	All matched files use Prettier code style!
   287	prettier=0
   288	```
   289	
   290	## The checker on the T133 task files (item 2's Check), on 6e07d291
   291	
   292	The T133 task files and the plan group exist only untracked in the main checkout, so it is `--root`. There is no `--premises-sha`, so C14 executes nothing and is recorded as not run.
   293	
   294	```
   295	$ uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root ~/Workspace/dotfiles ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-*.md
   296	(root at 740772efb9d7928e810a7d799f2bd32a88d9b8ff, origin/main 740772ef after #416)
   297	-- stdout
   298	dotfiles-T133-audit-pool-a01.md: OK
   299	dotfiles-T133-ci-efficiency-a01.md: OK
   300	dotfiles-T133-ci-efficiency-a02.md: OK
   301	dotfiles-T133-ci-efficiency-followup-a01.md: OK
   302	dotfiles-T133-ci-efficiency-followup-a02.md: OK
   303	dotfiles-T133-dispositions-a01.md: OK
   304	dotfiles-T133-dispositions-followup-a01.md: OK
   305	dotfiles-T133-permission-guard-gate-a01.md: OK
   306	dotfiles-T133-permission-guard-gate-a02.md: OK
   307	dotfiles-T133-permission-guard-gate-a03.md: OK
   308	dotfiles-T133-permission-guard-gate-followup-a01.md: OK
   309	dotfiles-T133-regime-ci-a01.md: OK
   310	dotfiles-T133-regime-ci-a02.md: OK
   311	dotfiles-T133-regime-ci-followup-a01.md: OK
   312	dotfiles-T133-result-precheck-a01.md: OK
   313	dotfiles-T133-result-precheck-a02.md: OK
   314	dotfiles-T133-result-precheck-a03.md: OK
   315	dotfiles-T133-result-precheck-followup-a01.md: OK
   316	dotfiles-T133-task-generator-plan-check-a01.md: OK
   317	dotfiles-T133-task-generator-plan-check-a02.md: OK
   318	dotfiles-T133-task-generator-plan-check-followup-a01.md: OK
   319	dotfiles-T133-verdict-audit-pool-a01.md: OK
   320	dotfiles-T133-verdict-audit-pool-a02.md: OK
   321	dotfiles-T133-verdict-audit-pool-a03.md: OK
   322	dotfiles-T133-verdict-audit-pool-followup-a01.md: OK
   323	dotfiles-T133-worker-cap-hookspath-a01.md: OK
   324	dotfiles-T133-worker-cap-hookspath-a02.md: OK
   325	dotfiles-T133-worker-cap-hookspath-followup-a01.md: OK
   326	dotfiles-T133-worker-hooks-path-a01.md: OK
   327	-- stderr
   328	dotfiles-T133-audit-pool-a01.md: warning: C14: not run (no trusted sha)
   329	dotfiles-T133-ci-efficiency-a01.md: warning: C14: not run (no trusted sha)
   330	dotfiles-T133-ci-efficiency-a02.md: warning: C14: not run (no trusted sha)
   331	dotfiles-T133-dispositions-a01.md: warning: C14: not run (no trusted sha)
   332	dotfiles-T133-permission-guard-gate-a01.md: warning: C14: not run (no trusted sha)
   333	dotfiles-T133-permission-guard-gate-a02.md: warning: C14: not run (no trusted sha)
   334	dotfiles-T133-permission-guard-gate-a03.md: warning: C14: not run (no trusted sha)
   335	dotfiles-T133-regime-ci-a01.md: warning: C14: not run (no trusted sha)
   336	dotfiles-T133-regime-ci-a02.md: warning: C14: not run (no trusted sha)
   337	dotfiles-T133-result-precheck-a01.md: warning: C14: not run (no trusted sha)
   338	dotfiles-T133-result-precheck-a02.md: warning: C14: not run (no trusted sha)
   339	dotfiles-T133-result-precheck-a03.md: warning: C14: not run (no trusted sha)
   340	dotfiles-T133-task-generator-plan-check-a01.md: warning: C14: not run (no trusted sha)
   341	dotfiles-T133-task-generator-plan-check-a02.md: warning: C14: not run (no trusted sha)
   342	dotfiles-T133-verdict-audit-pool-a01.md: warning: C14: not run (no trusted sha)
   343	dotfiles-T133-verdict-audit-pool-a02.md: warning: C14: not run (no trusted sha)
   344	dotfiles-T133-verdict-audit-pool-a03.md: warning: C14: not run (no trusted sha)
   345	dotfiles-T133-worker-cap-hookspath-a01.md: warning: C14: not run (no trusted sha)
   346	dotfiles-T133-worker-cap-hookspath-a02.md: warning: C14: not run (no trusted sha)
   347	dotfiles-T133-worker-hooks-path-a01.md: warning: C14: not run (no trusted sha)
   348	exit=0
   349	```
   350	
   351	C1 to C13, C15 and C7b found nothing in any of the files. C14: not run on each of the 20 files with premises, with the warning above. That is not a pass.
   352	
   353	## plan-check, once (eb20d063's code; the correction changed only `--drift`)
   354	
   355	```
   356	$ uv run --no-project --with pyyaml python -I scripts/orchestrator/plan-check.py --root ~/Workspace/dotfiles
   357	F3 024-todo.md:22 P1-13 names no bottleneck id of 5.0 or 5.10
   358	F3 024-todo.md:23 P1-14 names no bottleneck id of 5.0 or 5.10
   359	F4 024-checklists.md:9 P1-a holds no backtick command or file path
   360	F6 024-omp-cutover-and-corrective-order.md:39 cites dotfiles-T131-claude-pinned-merge-gate-fix-a01, which is not a task file
   361	F6 024-omp-cutover-and-corrective-order.md:70 cites dotfiles-T131-claude-pinned-merge-gate-fix-a01, which is not a task file
   362	F6 024-todo.md:9 cites dotfiles-T131-claude-pinned-merge-gate-fix-a01, which is not a task file
   363	exit=1
   364	```
   365	
   366	These six violations are in the real plan group. They are reported and left for the orchestrator; a01 reported the same six.
   367	
   368	## Caps
   369	
   370	```
   371	$ git diff --numstat origin/main...HEAD   (code head 6e07d291, merge base 3e41e36a)
   372	16	0	.orchestration/dotfiles-T133-task-generator-plan-check-a01/learning.md
   373	107	0	.orchestration/dotfiles-T133-task-generator-plan-check-a01/report.md
   374	5	0	.orchestration/dotfiles-T133-task-generator-plan-check-a01/revise.yaml
   375	20	0	.orchestration/dotfiles-T133-task-generator-plan-check-a01/sandbox.md
   376	603	0	.orchestration/dotfiles-T133-task-generator-plan-check-a01/validation.md
   377	231	0	.orchestration/dotfiles-T133-task-generator-plan-check-a02/task.md
   378	232	0	scripts/orchestrator/plan-check.py
   379	140	11	scripts/orchestrator/task-consistency-check.py
   380	242	0	scripts/orchestrator/task-from-plan.py
   381	34	0	scripts/orchestrator/task-template.md
   382	166	0	tests/unit/test_plan_check.py
   383	9	3	tests/unit/test_task_checkers.py
   384	265	0	tests/unit/test_task_consistency_c11_c15.py
   385	214	0	tests/unit/test_task_from_plan.py
   386	outside tests/ and .orchestration/: 659 (cap 700); under tests/: 657 (cap 800)
   387	```
   388	
   389	## CompactionDB memory
   390	
   391	```
   392	$ uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'T133 P1-12 a02: task-from-plan.py reads only scripts/orchestrator/task-template.md …'
   393	b5f77b7f-dde3-4401-b29c-3860ec126856
   394	exit=0
   395	```
   396	
   397	## Amendment 1: the CI-repair round (code head eb0b1c06, on 63b6acae, the update-branch onto b22a5580)
   398	
   399	The task copy, amendment 1:
   400	
   401	```
   402	$ shasum -a 256 .orchestration/dotfiles-T133-task-generator-plan-check-a02/task.md
   403	60d4c2db70ec6e8783945f3b6f2052cafe07da85700d574c0f70e477f7c7d1e9  .orchestration/dotfiles-T133-task-generator-plan-check-a02/task.md
   404	```
   405	
   406	Red: the regime tests on 63b6acae, before the repair:
   407	
   408	```
   409	$ uv run python -m unittest tests.unit.test_regime_ci
   410	FAIL: test_regime_ci_checks_only_the_latest_copy_of_a_reset_of_lineage (reset_of=True, predecessor_copy_kept=True)
   411	AssertionError: 0 != 1 : regime-ci: warning: t1-a01: predecessor copy .orchestration/t1-a01/task.md (reset_of of t1-a02)
   412	FAIL: test_regime_ci_checks_only_the_latest_copy_of_a_reset_of_lineage (reset_of=True, predecessor_copy_kept=False)
   413	AssertionError: 0 != 1 : regime-ci: t1-a02: checker: C13 disposition is not closed:, residual: or out-of-scope: and a space: residual
   414	FAIL: test_regime_ci_reads_the_head_as_data_and_runs_the_base_verifier (expected=0, phrase=None)
   415	AssertionError: 0 != 1 : regime-ci: warning: the diff changes scripts/orchestrator/regime-ci.py; this run executed the base's version, the audit reads the change
   416	FAIL: test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr
   417	AssertionError: Tuples differ: (0, 'regime-ci: ok 1 task(s)\n') != (1, 'regime-ci: t1-a01: checker: C13 dispo[1170 chars]l\n')
   418	FAIL: test_regime_ci_runs_the_checker_without_the_checkout_s_uv_config
   419	AssertionError: Tuples differ: (0, 'regime-ci: ok 1 task(s)\n') != (1, 'regime-ci: t1-a01: checker: C13 dispo[1170 chars]l\n')
   420	Ran 15 tests in 20.702s
   421	FAILED (failures=5)
   422	```
   423	
   424	Green on eb0b1c06: the regime tests, the four task modules and the orchestrator tool tests.
   425	
   426	```
   427	$ uv run python -m unittest tests.unit.test_regime_ci tests.unit.test_task_from_plan tests.unit.test_plan_check tests.unit.test_task_consistency_c11_c15 tests.unit.test_task_checkers tests.unit.test_orchestrator_tools -v
   428	Ran 101 tests in 125.509s
   429	OK (skipped=1)
   430	```
   431	
   432	Caps (`git diff --numstat` against the merge base b22a5580, outside `.orchestration/`):
   433	
   434	```
   435	232	0	scripts/orchestrator/plan-check.py
   436	140	11	scripts/orchestrator/task-consistency-check.py
   437	242	0	scripts/orchestrator/task-from-plan.py
   438	34	0	scripts/orchestrator/task-template.md
   439	166	0	tests/unit/test_plan_check.py
   440	11	5	tests/unit/test_regime_ci.py
   441	9	3	tests/unit/test_task_checkers.py
   442	265	0	tests/unit/test_task_consistency_c11_c15.py
   443	214	0	tests/unit/test_task_from_plan.py
   444	```

 exited 1 in 254ms:
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    import yaml; print(yaml.__version__)
    ^^^^^^^^^^^
ModuleNotFoundError: No module named 'yaml'

**Optimizing environment setup and YAML handling**
**Analyzing path trust and symlink security**
exec
/bin/zsh -lc "git grep -n 'INV-6:' 8a09b9365932f23b09df8aa2385a93d0b3016a3e -- '.orchestration/tasks/*design*'; git show b3c6b7ea --stat; git show 8a09b9365932f23b09df8aa2385a93d0b3016a3e:.orchestration/dotfiles-T133-task-generator-plan-check-a02/measure.md; git show 8a09b9365932f23b09df8aa2385a93d0b3016a3e:.orchestration/dotfiles-T133-task-generator-plan-check-a02/sandbox.md" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc 'git show 8a09b9365932f23b09df8aa2385a93d0b3016a3e:.orchestration/dotfiles-T133-task-generator-plan-check-a02/dotfiles-T133-task-generator-plan-check-a02-worker-crit.json && git show 8a09b9365932f23b09df8aa2385a93d0b3016a3e:.orchestration/dotfiles-T133-task-generator-plan-check-a02/dotfiles-T133-task-generator-plan-check-a02-worker-review-receipt.md && git show 8a09b9365932f23b09df8aa2385a93d0b3016a3e:.orchestration/dotfiles-T133-task-generator-plan-check-a02/learning.md && git show b3c6b7ea -- scripts/orchestrator/task-from-plan.py scripts/orchestrator/plan-check.py' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc "git grep -n 'INV-6' 8a09b9365932f23b09df8aa2385a93d0b3016a3e -- '.orchestration/designs/*' && rg --files --hidden ~/.cache/uv -g '__init__.py' -g 'python' | rg '/yaml/__init__.py|/bin/python"'$'"' | head -n 12" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 exited 1 in 168ms:
 succeeded in 181ms:
8a09b9365932f23b09df8aa2385a93d0b3016a3e:.orchestration/tasks/dotfiles-T124-design-gate-and-reset-rule-a01.md:29:  INV-6: the gate refuses a PR whose changed paths exceed 15 files unless the task declares waves and the PR lies within exactly one wave; the validator's allowed_files count only warns
8a09b9365932f23b09df8aa2385a93d0b3016a3e:.orchestration/tasks/dotfiles-T128-ci-skip-redesign-a01.md:8:# AGMSG-TASK dotfiles-T128-ci-skip-redesign-a01 — the reset redesign of A5 (INV-6: the second round)
8a09b9365932f23b09df8aa2385a93d0b3016a3e:.orchestration/tasks/dotfiles-T128-process-rules-redesign-a02.md:8:# AGMSG-TASK dotfiles-T128-process-rules-redesign-a02 — the reset redesign of the a02 task (INV-6: amendments threshold)
8a09b9365932f23b09df8aa2385a93d0b3016a3e:.orchestration/tasks/dotfiles-T128-process-rules-redesign-a03.md:8:# AGMSG-TASK dotfiles-T128-process-rules-redesign-a03 — the reset redesign of a03 (INV-6: two Bot P1 heads after the RESULT)
8a09b9365932f23b09df8aa2385a93d0b3016a3e:.orchestration/tasks/dotfiles-T128-process-rules-redesign-a04.md:10:Drafted 2026-10-11 23:14Z by the orchestrator seat. `dotfiles-T128-process-rules-a04` (PR #318, worker `claude-standard-dot-a003`, head `7800ef92`) stopped under plan 006 S1, not INV-6: the Codex Bot found the same class six times on the one SKILL bullet "Before every acceptance action … `scripts/regime-counters.sh`" (SKILL.md line 72 on every head): 4240250137, 4240348412, 4240382519, 4243516879, 4243537278, 4243631335, each about which sources the S1/S2 counts read. The cause record is `.orchestration/learning/plan-006-s1-process-rules-counters-bullet-2026-10-11.md`: the bullet enumerates sources that three owners define (INV-6 at design line 55, the A3 script's own output, plan 006 S1) and every fix re-enumerated. Read that record, design line 55 (`.orchestration/tasks/dotfiles-T128-regime-v3-a01.md`, INV-6), plan 006 line 48 (S1), the bullet at `7800ef92` (`git -C .claude/worktrees/worker-f show 7800ef92:home/dot_agents/skills/agmsg-orchestration/SKILL.md | sed -n 72p`), the Bot comment 4243631335 (`gh api repos/mryfmo/dotfiles/pulls/comments/4243631335 --jq .body`, from outside the sandbox) and the tests that pin the bullet at `7800ef92` (`tests/unit/test_agmsg_orchestration_docs.py` lines 287-311 and 436-444).
8a09b9365932f23b09df8aa2385a93d0b3016a3e:.orchestration/tasks/dotfiles-T128-process-rules-redesign-a05.md:8:# AGMSG-TASK dotfiles-T128-process-rules-redesign-a05 — the reset redesign of a05 (INV-6: questions 2; the second amendment would be the threat-table row the Bot found missing)
8a09b9365932f23b09df8aa2385a93d0b3016a3e:.orchestration/tasks/dotfiles-T128-process-rules-redesign-a05.md:10:Drafted 2026-10-12 00:36Z by the orchestrator seat. `dotfiles-T128-process-rules-a05` (PR #318, worker `claude-standard-dot-a003`, head `be0afe7e`, the revise-round commit for item 10 already pushed) reached INV-6: two `AGMSG-PONG status=question` (603 and 621), and the Bot's P1 4243885108 on `be0afe7e` (the a05 `threat_table` has no row for `tests/fixtures/regime/*.md`, the expected half of the whole-section oracle item 10 introduced) would be amendment 2. The missing row is the orchestrator's omission when writing item 10 (A7's text got the same row at 00:27Z; a05's did not). The rule's path is a reset by another context: this task.
8a09b9365932f23b09df8aa2385a93d0b3016a3e:.orchestration/tasks/dotfiles-T128-process-rules-redesign-a06.md:8:# AGMSG-TASK dotfiles-T128-process-rules-redesign-a06 — the reset redesign of a06 (INV-6: the evidence-records row would be amendment 2; the `bookkeeping` class at four)
8a09b9365932f23b09df8aa2385a93d0b3016a3e:.orchestration/tasks/dotfiles-T128-regime-counters-redesign-a01.md:8:# AGMSG-TASK dotfiles-T128-regime-counters-redesign-a01 — the reset redesign of A3 (INV-6: the second round)
8a09b9365932f23b09df8aa2385a93d0b3016a3e:.orchestration/tasks/dotfiles-T128-worker-stop-and-watch-redesign-a01.md:8:# AGMSG-TASK dotfiles-T128-worker-stop-and-watch-redesign-a01 — the reset redesign of A7 (INV-6: a second revise RESULT would be revises 2)
commit b3c6b7ea382dbf0b5d16de7005486a6b605a8a72
Author: Fumio Moriya <moriya.fumio@technopro.com>
Date:   Sun Oct 18 21:25:46 2026 +0900

    fix(orchestrator): task-from-plan refuses a checkout without its records by name; plan-check F2 treats glob entries as overlapping what they match (T133 task-generator-plan-check a01, Bot round 1)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 scripts/orchestrator/plan-check.py     |  7 ++++++-
 scripts/orchestrator/task-from-plan.py |  7 +++++--
 tests/unit/test_plan_check.py          |  4 ++++
 tests/unit/test_task_from_plan.py      | 10 ++++++++++
 4 files changed, 25 insertions(+), 3 deletions(-)
---
task_id: dotfiles-T133-task-generator-plan-check-a02
round: 1
code_head: 6e07d29193e9a3b56b299dd9d55538788bc48b7b
merge_base: 3e41e36abc949acd7e6b4859c1a22df9e665c8d4
---

# Measure

`git diff --numstat origin/main...HEAD` on the code head. The totals cover the whole PR, including the inherited a01 changes and the bundled template. Changed lines are additions plus deletions.

| Scope | Changed lines | Cap |
| --- | --- | --- |
| outside `tests/` and `.orchestration/` | 659 | 700 |
| under `tests/` | 657 | 800 |
| under `.orchestration/` (not capped) | 982 | — |

Changed files outside `.orchestration/`:

| Added | Deleted | File |
| --- | --- | --- |
| 232 | 0 | `scripts/orchestrator/plan-check.py` |
| 140 | 11 | `scripts/orchestrator/task-consistency-check.py` |
| 242 | 0 | `scripts/orchestrator/task-from-plan.py` |
| 34 | 0 | `scripts/orchestrator/task-template.md` |
| 166 | 0 | `tests/unit/test_plan_check.py` |
| 9 | 3 | `tests/unit/test_task_checkers.py` (amendment 1's two edits, from a01) |
| 265 | 0 | `tests/unit/test_task_consistency_c11_c15.py` |
| 214 | 0 | `tests/unit/test_task_from_plan.py` |

Under `.orchestration/`:
- the a01 evidence records, kept as history;
- the a02 task copy;
- this directory's records, added by the evidence commit.

The a01 task copy is deleted in 6da92853. Numstat against the merge base does not list it, because main never had it.

The review measured 651 and 647 on eb20d063. The correction round added 8 lines outside `tests/` and 10 under it.
---
task_id: dotfiles-T133-task-generator-plan-check-a02
round: 1
---

# Sandbox

Claude Code seat `claude-standard-dot-a009`, in its own worktree `.claude/worktrees/worker-c`, with the Bash sandbox on (macOS Seatbelt) in auto mode. Branch `tools/task-generator-plan-check-a01` continues PR #417 from 9da0ed3f, as the a02 Completion directs.

Inside the sandbox:

- Every edit, and the task-copy swap: `git rm` of the a01 copy, then the a02 copy taken from the main checkout's dispatched text, which was only read.
- The red replays, each in a scratch worktree of the reviewed production commit (9da0ed3f, and ff4d25a8 for the C14 gate) with this branch's test modules copied in, each removed with `git worktree remove --force`.
- The four task modules, `test_orchestrator_tools` and `test_agmsg_orchestration_docs`.
- `make unit-test` and `make format` on the branch, and the same two on a pristine detached worktree of `origin/main` 3e41e36a, which was then removed.
- The checker and `plan-check.py`, each run against the main checkout with `--root`, because the plan 024 group and the T133 task files exist only untracked there. They only read it; the checker run carries no `--premises-sha`, so it executed nothing.
- `git fetch origin`, and the push, with `-c url.https://github.com/mryfmo/.pushInsteadOf=https://github.com/mryfmo/`.

Permission-gated or outside the sandbox:

- `gh pr checks`, `gh pr view` and the Bot listing (Worker Playbook step 4).
- `agmsg-dispatch` for the RESULT.

Each `gh` command and each git write runs as a single command; no `@codex review` comment is posted.

Interruption: the orchestrator's revise of PR #411 arrived mid-task with `next_action=... before-continuing-P1-12-a02`.

- The a02 work was committed locally (6da92853 and eb20d063, not pushed) before the switch.
- The suite runs that read this worktree finished first.
- The first self-review agent read this worktree and could not move to a scratch worktree in time. It was stopped before it reported any finding.
- Worker-c then switched to `tools/result-precheck-a01` for the #411 round and switched back afterwards. Each `git checkout` was a single command on a clean tree.
- The relaunched review worked in its own scratch worktree of eb20d063 from the start.

`make unit-test` fails inside the sandbox on sandbox-denied operations. The failing set is identical to a pristine `origin/main` worktree's in the same sandbox (validation.md), so CI decides the full suite.

effects=none

 succeeded in 204ms:
[
  {
    "id": "a02-review-scope",
    "scope": "review",
    "body": "Independent read-only review of `git diff 9da0ed3f..eb20d063` by a fresh general-purpose subagent of the worker seat. It had the diff and the task file, not the worker's conclusions, and worked in its own scratch worktree of eb20d063, removed afterwards. It ran the four task modules (28 tests OK, 1 skipped) and probes under its own temporary directory. Checked and found fine: the byte-identical task copy; the caps (651 of 700, 647 of 800); test_task_checkers.py carrying only amendment 1's two edits; all 27 dispatched T133 task files passing without a sha, with only the no-sha warning; the clean-plan gate before any command or write; plan text read with `git show HEAD:`; no read under .orchestration/tasks/; whole-id wave selection; program items to the next heading; scope confinement; the Check worktree cleanup; the bundled Completion text; C10 `-e`; C6, C10 and C12 confinement, a symlink escape included; the C14 hash and command read from the same bytes and its severities; C12 concrete matches; F2 concrete matches; no printed token value. The verdict was `incorrect` (two P2). This was the task's one correction round, fixed in 6e07d291; each finding's record below gives its disposition. This is worker process evidence, not reviewer authentication and not the task-level audit.",
    "resolved": true
  },
  {
    "id": "a02-p2-latest-event",
    "scope": "file",
    "path": "scripts/orchestrator/plan-check.py",
    "body": "P2, high: `latest()` took the first status of a line even when that event was another task's, ranked every timed line above every untimed one, and kept a trailing backtick. Real case: .orchestration/acceptance/dotfiles-T128-settings-hook-dedupe-a01.md:80. fixed:6e07d291. Each event is read up to the next one on its line; an untimed event carries the latest timestamp above it; the status is captured as [\\w-]+. Regression: test_drift_uses_the_latest_timestamped_acceptance_for_the_same_task gained a timed line with two events, another task's first, and an untimed shared line after it. It is red against eb20d063 (`accepted != withdrawn`` `) and green on 6e07d291.",
    "resolved": true
  },
  {
    "id": "a02-p2-c15-missing-design",
    "scope": "file",
    "path": "scripts/orchestrator/task-consistency-check.py",
    "body": "P2, high: C15 reported a missing design only for a task that carries invariants, so a mistyped design path skipped the assignment check. fixed:6e07d291. Existence now comes from C8's `git cat-file -e` probe. A design that origin/main cannot give is a finding for a task with invariants, and a path naming no design on origin/main or in the checkout is a finding for any task. The one exemption left is a design that exists only in this checkout, for a task without invariants: it assigns nothing yet. Amendment 1's frozen fixtures in test_task_checkers.py are such tasks; the report explains this. Regression: test_c15_requires_the_design_assigned_invariant_id_set gained `a mistyped design`. It is red against eb20d063 and green on 6e07d291. The list form of implementing_tasks (T124, T126) still assigns no id set, so the sentences a task carries are byte-compared, as stated in the docstring: no-change-needed, because a list names no ids per task.",
    "resolved": true
  },
  {
    "id": "a02-p3-stdin-and-lone-words",
    "scope": "file",
    "path": "scripts/orchestrator/task-consistency-check.py",
    "body": "P3: rerun() inherited stdin, so a lone-word premise such as `head` waited on the caller. fixed:6e07d291 with stdin=subprocess.DEVNULL; the change is one line, so it has no dedicated test. The lone-word rule itself stays: item 15 names single-word commands. The real plan's field names `head` and `security` become draft premises the orchestrator edits out of the generated file (see the report).",
    "resolved": true
  },
  {
    "id": "a02-p3-c7b-duplicate-row",
    "scope": "file",
    "path": "scripts/orchestrator/task-from-plan.py",
    "body": "P3: a glob match that is itself an allowed entry got a second row naming two entries, so the generated file failed C7b. fixed:6e07d291: no concrete row is written for an allowed entry. Regression: test_generator_preserves_wildcard_scopes_and_their_threat_rows now adds `scripts/*.sh` over the literal scripts/demo.sh. It is red against eb20d063 and green on 6e07d291.",
    "resolved": true
  },
  {
    "id": "a02-p3-design-without-front-matter",
    "scope": "file",
    "path": "scripts/orchestrator/task-consistency-check.py",
    "body": "P3: C15 parsed the YAML of any design read from origin/main. fixed:6e07d291: only a design that opens with `---` is parsed, and anything else assigns nothing. There is no dedicated test: C6, which is unchanged under item 2, parses the same working-tree design first, so a fixture would exercise C6, not C15.",
    "resolved": true
  },
  {
    "id": "a02-p3-test-gaps",
    "scope": "review",
    "body": "P3: item 17's test covered two different PRs, not one repeated PR, and C12's own-evidence exemption had no real file. fixed:6e07d291. The item 17 line is now `#77 abc1234 merged; #77 def4567 abc1234 CLEAN`. The C12 test tracks .orchestration/dotfiles-T9-base-a01/run.sh under the task's own glob. Both pass against eb20d063, because they fill coverage gaps rather than show defects, and both are red against 9da0ed3 with the final sources.",
    "resolved": true
  }
]
review_surface: crit-data
reviewer: claude (a fresh general-purpose subagent of the worker seat, read-only, given the diff and the task file, not the worker's conclusions, working in its own scratch worktree)
review_source: .orchestration/dotfiles-T133-task-generator-plan-check-a02/dotfiles-T133-task-generator-plan-check-a02-worker-crit.json
review_outcome: addressed

Crit has no review file or daemon in this worktree, because no Plan Mode was used, so the AGENTS.md fallback applies: an independent read-only review in the crit-data shape.

There was one round, on eb20d063, with `Verdict: incorrect`: two P2 and four P3, each reproduced by the reviewer. All six are fixed in the single correction round, commit 6e07d291. Each record in the JSON gives its disposition, its regression, and its red run against eb20d063.

An earlier attempt at this review was stopped before it reported any finding. It read worker-c directly, and the orchestrator's #411 revise needed that worktree (sandbox.md). It produced no output and is not counted as a round.

Tested head: 6e07d291, the code head. The evidence commit after it changes only `.orchestration/` files.

This is worker process evidence, not reviewer authentication and not the task-level audit. The orchestrator owns the sweep, the audit, the dispositions, the gate and the merge.
---
task_id: dotfiles-T133-task-generator-plan-check-a02
round: 1
---

# Learning

Task-local triage; nothing promoted.

- A generator that needs prose from a task record depends on that record existing. Bundling the template beside the script removes the dependency, and makes the template reviewable with the code that reads it. Applies to any tool that copies wording from another record.
- Text that will be executed is only as trustworthy as the revision it comes from. Refuse a dirty source group before anything runs, and read the command text with `git show <rev>:<path>`, so the executed text is the committed text. The same idea is C14's dispatched sha.
- A glob is a set of files, not a string. Disjointness, threat coverage and scope all have to be decided on the concrete tree matches; comparing two spellings proves nothing. F2, C12 and the generator's concrete rows all took this fix.
- A literal handed to `git grep` must follow `-e`, or a value such as `--open-files-in-pager=<cmd>` becomes an option and runs a program. Applies to every tool that passes data as a command-line argument.
- A check added to a checker can collide with a frozen test module. The first escape, reporting a missing design only for a task with invariants, reopened the bypass the check exists to close: the pre-push review's P2, a mistyped path. The narrower rule keeps the finding for any path that names no design anywhere and exempts only a design in flight in the checkout. Look for the exemption that the fixtures actually need, not the broadest one that makes them pass.
- A regression for a review finding must be run against the head the review read. The first item 16 case passed on eb20d063, because its shared line was untimed and the old code ranked untimed events lowest, so it proved nothing until the shared line carried a timestamp.
- A long-running suite in a worktree blocks a branch switch. Commit first, and give any reviewer its own scratch worktree from the start, so an interruption costs nothing.
- In zsh, `"$VAR:t…"` and `"$VAR:s…"` are history modifiers; write `"${VAR}:…"`. This cost two replay runs here, both caught by their outputs.
commit b3c6b7ea382dbf0b5d16de7005486a6b605a8a72
Author: Fumio Moriya <moriya.fumio@technopro.com>
Date:   Sun Oct 18 21:25:46 2026 +0900

    fix(orchestrator): task-from-plan refuses a checkout without its records by name; plan-check F2 treats glob entries as overlapping what they match (T133 task-generator-plan-check a01, Bot round 1)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/scripts/orchestrator/plan-check.py b/scripts/orchestrator/plan-check.py
index e7ece5ed..84570a87 100644
--- a/scripts/orchestrator/plan-check.py
+++ b/scripts/orchestrator/plan-check.py
@@ -24,6 +24,7 @@ import pathlib
 import re
 import subprocess
 import sys
+from fnmatch import fnmatchcase
 
 try:
     import yaml
@@ -90,8 +91,12 @@ def form(root, files):
         wave = sorted(set(re.findall(r"\bP1-\d+[a-z]?\b", " ".join(c[1:]))) & set(tasks))
         for i, a in enumerate(wave):
             for b in wave[i + 1 :]:
+                # A glob entry overlaps whatever it matches (fnmatch's * also crosses /, which errs toward a report).
                 shared = sorted(
-                    x for x in tasks[a] for y in tasks[b] if x == y or x.startswith(y + "/") or y.startswith(x + "/")
+                    x
+                    for x in tasks[a]
+                    for y in tasks[b]
+                    if x.startswith(y + "/") or y.startswith(x + "/") or fnmatchcase(x, y) or fnmatchcase(y, x)
                 )
                 if shared:
                     out.append(f"F2 024-omp-cutover-and-corrective-order.md:{n} {c[0]} {a} and {b} share {shared[0]}")
diff --git a/scripts/orchestrator/task-from-plan.py b/scripts/orchestrator/task-from-plan.py
index 8fece62f..99dc45f3 100644
--- a/scripts/orchestrator/task-from-plan.py
+++ b/scripts/orchestrator/task-from-plan.py
@@ -101,8 +101,11 @@ def main():
     args = parser.parse_args()
     root = pathlib.Path(git(".", "rev-parse", "--show-toplevel").stdout.strip())
     read = lambda name: (root / name).read_text().splitlines()  # noqa: E731
-    if not (root / COMPLETION).is_file():
-        sys.exit(f"task-from-plan: {COMPLETION} is missing")
+    # The plan group, the template and the completion file are regime records a checkout may not hold yet.
+    plans = ("todo", "design-programs", "design-quality", "omp-cutover-and-corrective-order")
+    needed = [f"{PLANS}/024-{n}.md" for n in plans] + [f".orchestration/tasks/{TEMPLATE_ID}.md", COMPLETION]
+    if missing := [n for n in needed if not (root / n).is_file()]:
+        sys.exit(f"task-from-plan: missing under {root}: {', '.join(missing)}")
     out = args.out or pathlib.Path(f".orchestration/tasks/{args.todo_id}.md")
     tid, own = out.stem, f".orchestration/{out.stem}/"
     row = next(c for c in rows(read(f"{PLANS}/024-todo.md")) if c[0].split()[0] == args.todo_id)

**Clarifying command separation**
exec
/bin/zsh -lc "rg --files --hidden ~/.cache/uv -g '__init__.py' | rg '/yaml/__init__.py"'$'"' | head -n 6" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc "git show 8a09b9365932f23b09df8aa2385a93d0b3016a3e:.orchestration/tasks/dotfiles-T128-regime-v3-a01.md | nl -ba | sed -n '35,70p' && nl -ba .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a01.md && git diff b22a5580d0778e57a66d3f75c76e3c55b88701e1 8a09b9365932f23b09df8aa2385a93d0b3016a3e -- scripts/orchestrator/task-consistency-check.py" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc 'git show 8a09b9365932f23b09df8aa2385a93d0b3016a3e:.orchestration/dotfiles-T133-task-generator-plan-check-a01/report.md && git show 8a09b9365932f23b09df8aa2385a93d0b3016a3e:.orchestration/dotfiles-T133-task-generator-plan-check-a01/revise.yaml && git show 8a09b9365932f23b09df8aa2385a93d0b3016a3e:.orchestration/dotfiles-T133-task-generator-plan-check-a01/sandbox.md && git show 8a09b9365932f23b09df8aa2385a93d0b3016a3e:.orchestration/dotfiles-T133-task-generator-plan-check-a01/learning.md' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 144ms:
~/.cache/uv/archive-v0/wYhEQWcw2EWueJ_S/lib/python3.9/site-packages/yaml/__init__.py
~/.cache/uv/archive-v0/7OgnLaAJ8JgV819t/yaml/__init__.py
~/.cache/uv/archive-v0/731WLDUbXfLlkGP0/yaml/__init__.py
~/.cache/uv/sdists-v10/pypi/pyyaml/6.0.3/JyodBRTI7bc6NXdp/src/build/lib.macosx-27.0-arm64-cpython-315/yaml/__init__.py
~/.cache/uv/sdists-v10/pypi/pyyaml/6.0.3/JyodBRTI7bc6NXdp/src/lib/yaml/__init__.py
~/.cache/uv/archive-v0/31F2mEsBsyaNJEyC/lib/python3.15/site-packages/yaml/__init__.py

 succeeded in 217ms:
    35	  - dotfiles-T124-design-gate-and-reset-rule-a01
    36	reset_of:
    37	  - dotfiles-T124-wave1-task-validator-a01
    38	  - dotfiles-T124-wave3b-audit-grammar-a01
    39	threat_model:
    40	  R1: rounds are judged by models re-reading models and add no deterministic fact, so a wrong premise is patched round after round (T118 20 revises, T119 5 revises and 4 audits; the vendor's own rule is two corrections, then start fresh)
    41	  R2: "hand-written parsers at a trust boundary have an unbounded bypass surface (PR 313: 33 of 52 Bot threads on a 503-line validator with its own YAML parser, written on the false premise that PyYAML is unavailable)"
    42	  R3: "PRs larger than a reviewer can hold (PR 313 20 files +2642, PR 312 37 files +3191; Google: 100 lines reasonable, 1000 too large)"
    43	  R4: task text grown by question-and-amendment (PR 313 6 questions 8 amendments, T119 8 and 8, T120 8 amendments and no RESULT) keeps the under-researched premise
    44	  R5: the orchestrator's artifacts are unaudited and it dispositions findings about itself (T119 audit-finding 2); the reset rule was prose the orchestrator could waive (PR 313 revise round 2)
    45	  R6: "the auditor becomes a serial queue when audits run once per round in one tab (measured: 4 audits about 1.3 h of T119's 11.1 h; the rounds, not the audits, were the cost)"
    46	  R7: cost is unmeasured (every acceptance record says cost n/a) so no stage can be weighed against its value
    47	  R8: a PR can change the check that judges it (a pull_request workflow runs the PR head's workflow file); host-side evidence is whatever the orchestrator copies into the gate's cwd
    48	trust_anchors:
    49	  - agmsg message history (append-only, read through history.sh) for who did what and when; GitHub for PR, CI, Bot, ruleset and merge state; the main checkout for files, never the gate's cwd
    50	  - JSON Schema documents validated by the jsonschema library (PyYAML for front matter) for task files, audit verdicts, design-review receipts and evidence; model verdicts produced under schema (codex exec --output-schema, server-side strict; claude -p --json-schema)
    51	  - mechanical checks run from main's workflow file as a pull_request_target required status check that reads PR files as data and executes nothing from the PR; required workflows are organization-only, so this is the main-pinned form available to a user-owned repository
    52	  - the operator waiver is visible, not prevented (acceptance record, boundary PR body, check-regime-boundary)
    53	  - a reset is released only by a redesign written in a context other than the one that wrote the abandoned task, or by the operator
    54	invariants:
    55	  INV-1: "every task is a format-2 file whose front matter validates against schemas/task.json (jsonschema + PyYAML, no hand-written parser; every allowed_files entry starts with a literal path segment and a wildcard entry derives the tier of every design-tier path its literal prefix can cover); legacy task ids are grandfathered only for files under .orchestration/tasks/ on main, never for a branch copy; the tier (docs, review, design) is derived from allowed_files by the shared high-risk module, with the regime's own rule prose (home/dot_config/claude/rules/**, the agmsg-orchestration SKILL, AGENTS.md, README) listed in the review tier, and selects the pipeline from process_tiers in agent-config.yaml; every AGMSG-TASK for the task, the first and each amendment, carries task_sha256= of the task file as sent, the worker commits the file byte-identical to .orchestration/<task id>/task.md (first commit, recommitted after each amendment), the CI regime job validates that copy with main's schema and refuses a PR that changes .github/workflows/** unless its task.md is design tier and lists the file, the host gate compares the copy's sha256 with the latest AGMSG-TASK's token in history, and the regime check binds only once the ruleset lists it as required (an operator action named in V1's acceptance record); the orchestrator can add or skip a stage only with an operator waiver written by scripts/regime-waive.sh, a command under a permissions.ask rule in the managed settings with no permgate policy entry, so that only the human's answer to the native prompt runs it (an ask rule prompts even in auto mode; agent-to-agent approval is forbidden); the waiver names the task, the stage and a reason and is written under $XDG_STATE_HOME/regime/waivers/, a directory outside every seat's sandbox write roots, so no sandboxed seat can write it and only a command run outside the sandbox on the human's answer to the native prompt can (the directory is the guard; the ask rule on the named command is the second layer, since a reworded command would still meet the prompt at the sandbox boundary); it is listed by check-regime-boundary.sh and the boundary PR body (V3a owns the script and its ask rule), and is the strongest friction available on a machine where every seat and GitHub action is the operator's own account (operator authentication is a stated residual, not a claim)"
    56	  INV-2: "a PR is mergeable only within the caps the CI regime job enforces from main's workflow (at most 15 changed files outside .orchestration/, 500 added lines outside tests/, .orchestration/ and the data list scripts/legacy-task-ids.txt, and 1000 added lines under tests/), and its task.md invariants equal the design's as a set of ids and byte-for-byte as sentences (the design read from main, never from the PR); the design file must be on main (through a boundary PR) before the implementing TASK is dispatched and the regime job fails closed when the design named by task.md is absent from main; an .orchestration-only PR runs no bootstrap or test matrix and every required check context still reports success (each required workflow decides inside each of its jobs, as test.yaml and remote.yaml do since A5: no job-level if and no needs, because a skipped required job reports success), so a boundary PR merges in minutes; exceeding a cap is a split, never a finding to disposition (the cap changes the unit of work: T116 +529 and T118 +881 would have been split)"
    57	  INV-3: "a revise round is admissible only when it adds a new deterministic check: the AGMSG-ACCEPTANCE status=revise carries check=tests/<file>::<name> and previous_head=<the RESULT head being revised>, the worker records both in .orchestration/<task id>/revise.yaml (a sibling file; task.md stays byte-identical to the dispatched file), the main-pinned regime job verifies that the named test file exists on the head and differs between previous_head and the head, the PR's own unit-test workflow (a required check, run in the PR's context) collects and runs exactly that selector on the head (it must pass) and on previous_head (it must fail or be absent), and the host gate, which reads history, verifies that previous_head equals the head of the previous AGMSG-RESULT for the task and requires the same selector in the validation file; a finding that cannot become a test is dispositioned, never iterated"
    58	  INV-4: "a task file carries premises, each with the command and pasted output that verified it before dispatch; premises are evidence for the design reviewers and the auditor, each of whom dispositions every premise in the receipt or audit JSON as holds, fails or unverifiable (a local command re-run, an external claim re-fetched; a fails is a specification finding and a rejection), a complete disposition the schema requires rather than a sample, and the mechanical part of this invariant is the counting: a worker question (AGMSG-PONG status=question) is a specification defect answered by at most one further AGMSG-TASK, amendments are every AGMSG-TASK for the task_id after the first, whatever its wording, and the second amendment or the second question is INV-6's count, which withdraws the task to design through INV-6's merge backstop and Stop signal"
    59	  INV-5: "the task-level audit is a headless read-only run whose instruction root is the trusted main checkout and whose schema is main's schemas/audit.json: codex exec --output-schema <main>/schemas/audit.json -C <main> with the detached worktree at the head added as a read-only data directory (--add-dir), so the audited PR controls neither the schema nor the AGENTS.md the auditor reads; the fallback claude -p --json-schema from the same root with --add-dir <worktree>, --bare when an API key is set and otherwise with project and user hooks disabled, and refused with exit 2 blocked when the head changes any file under .claude/ (bare mode loads skills from an --add-dir directory's .claude/skills/), leaving such a head to the codex path), with at most one valid audit per head (a stale input manifest invalidates an audit and a new audit of the same head replaces it), pooled two at a time; the gate accepts an audit of an earlier head only when git diff --quiet <audited head> <HEAD> -- . ':!.orchestration' holds (an evidence-only revision), otherwise a new audit is required; its input includes the task's invariants and premises, the worker's evidence, the orchestrator's task file and amendments, the acceptance record as it stands when present (its text above the line <!-- audit-input-boundary --> is the pre-audit part; dispositions of this audit's findings are appended below it), the head's pr-feedback JSON and the previous round's audit JSON; the audit JSON carries an input manifest (path to sha256 of every input as read, computed by the runner, which overwrites any model-supplied value) and the gate recomputes the manifest at gate time, so a pre-audit input edited after the audit makes the audit stale and a new audit is required; the schema lists findings {priority, confidence, category in {specification, implementation, evidence, orchestration, conformance}, path, line, rationale} and the per-invariant map before the verdict, and the prompt asks for the rationale before each verdict; the runner, under the identity claude-audit-dot-h001 or codex-audit-dot-h001 on the orchestrator's host, records the JSON's sha256 in agmsg history (AGMSG-AUDIT v1 task_id= head= sha256= auditor=) before the gate reads it, an anchor that prevents edits after the record and not fabrication before it; the gate reads the verdict and categories from the JSON, and orchestration and conformance findings at P0-P2 accept only an operator waiver or a design reset, never not-applicable"
    60	  INV-6: "the reset rule's mandatory point is the merge backstop in scripts/require-crit-review.py, with the orchestrator's Stop hook (Claude Stop hook, Codex [hooks].Stop) as the early signal, soft on both runtimes by their documented caps; counts come from history for the hook and the gate (revises = RESULTs for the task_id minus one, threshold 2; amendments = AGMSG-TASKs after the first, threshold 2; AGMSG-PONG status=question, threshold 2) and from GitHub and main-checkout files for the gate and the boundary check only (Codex Bot P0 or P1 on two heads after the first RESULT, from original_commit_id on review_comment items recorded by pr-feedback.py; an audit implementation or specification finding at P0-P1 on two heads, from .orchestration/validation/<task>-audit-<sha7>.json in the main checkout, each counted only when its sha256 matches its AGMSG-AUDIT record); when a count is reached the gate refuses the merge until a reset record names a redesign task whose design RESULT comes from an identity other than the task's author, or a waiver written by scripts/regime-waive.sh under the INV-1 ask-rule discipline into the state directory outside the sandbox write roots (the only release path besides a redesign; the one-account residual of INV-1 applies); check-regime-boundary.sh reports a closed-unmerged PR whose task has no reset record and a task over any count with neither an accepted acceptance record nor a reset record; the same gate refuses a merge whose acceptance record carries a not-applicable disposition without an evidence= clause, or a finding-class table with three rows of one class and no pasted search of the correction records (plan 007 S6)"
    61	  INV-7: "the design tier adds, before any code is dispatched, two design reviews of the same design hash: a fresh Claude context on the review profile (a headless run or a seated -review- identity; the review profile is the same model and effort as deep, so the lever is the separate context) and a Codex read-only review (codex exec --sandbox read-only on the review profile under a codex-review identity: headless through V4's runner, or seated until V4); each receipt is a schema document naming the design file's canonical hash over invariants, threat_model, trust_anchors, implementing_tasks and premises, each is announced by an AGMSG-RESULT from its reviewing identity, and both RESULTs precede the implementing AGMSG-TASK in history; the Codex Bot's review of a boundary PR is swept feedback, never a design receipt; a change to the hashed keys needs new reviews; the gate accepts the whole-file sha256 form for receipts written before V4 lands"
    62	  INV-8: "worker evidence (the task.md copy, revise.yaml, report, validation, sandbox, learning, autoskill, worker review JSON) is committed on the PR branch under .orchestration/<task id>/ before the final RESULT so the Bot, CI and the gate read the same files from the audited head; the orchestrator's records (audit JSON, acceptance, pr-feedback) stay under .orchestration/validation and .orchestration/acceptance in the boundary commit because the merge is --match-head-commit"
    63	  INV-9: "every acceptance record carries measured cost (rounds, amendments, questions, wall time TASK to final RESULT from history timestamps, audit count, Bot threads, tokens: total_cost_usd from claude -p JSON, turn.completed.usage from codex exec --json, per-message usage from the seat's session transcript) written by accept-task.py, which also records the path and sha256 of every raw source it read (the headless runs' JSON, the transcript files at acceptance time) so a total can be recomputed; cost is a warning metric, never a gate: each tier has a budget, the acceptance record names the operator decision when it is exceeded, and check-regime-boundary.sh warns; headless runs carry --max-budget-usd"
    64	  INV-10: "at most three concurrent workers with pairwise-disjoint allowed_files; the first push is the draft PR's server-side created_at (gh api pulls/<n>), which must fall within 30 minutes of the TASK's history timestamp, and a seated worker is not idle for 20 minutes while a dispatchable task exists, a dispatchable task being a format-2 file under .orchestration/tasks/ with no AGMSG-TASK for its id in history, no superseded_by or reset record, and every task id in its after list accepted (an acceptance record with Decision accepted in the main checkout); both computed in check-regime-boundary.sh and accept-task.py, never in the Stop hook; headless reviews and audits do not count as workers"
    65	  INV-11: permgate records session_id and cwd per decision, and the gate compares a Claude worker's permission-gated Bash count in the task window with the sandbox record (an understated record is refused); Codex workers cannot escalate and are not covered
    66	  INV-12: "every rule above is exercised by a unit test that fails when the rule is removed; the PR's own workflow runs the PR's tests, and a required check main-tests (wave V0, before every other wave) fetches main's tests/unit and runs, in the PR's context, main's test module of every script outside the task.md's allowed_files as it is, so an undeclared change to any script fails (the undeclared-change regression guard); a script inside allowed_files is judged by the PR's own tests, the orchestrator's diff review and the trusted-root audit (INV-5), which reads the test diff beside the code diff and reports a deleted or weakened fails-when-removed test as a conformance finding; main-tests decides inside its own job, as the A5 workflows do, with no changes job and no needs, so an .orchestration-only PR reports success from the job itself; main-tests is an in-process oracle: code that main's tests import from the PR runs inside the test process, so the harness authenticates that main's runner reached its end with a per-run nonce that only the runner sees (read from a pipe and closed before any test loads, written back with the counts), and the runner pins unittest's result and runner classes before importing any test; the nonce authenticates the writer, not the counts: adversarial PR code running in the same process can still patch result collection or read the nonce from a frame, so in-process forgery remains a stated residual that the trusted-root audit catches, named in every acceptance record of a design-tier PR; including one test per gaming path (a schema-valid task with a prose cap bypass, a revise without a named check, a revise list appended to the hashed task.md, an AGMSG-TASK without amendment= that still counts, an evidence-only relabel of a code change caught by the tree-equality check, a wave-table rewrite after review, an audit JSON edited after its history record, a receipt whose hash predates a key change, a reset record naming the author's own identity, a Bot-skipped head whose audit never starts, a single PR split only in the task file, a branch task.md claiming a legacy id, allowed_files of ['*'] or a wildcard first segment, an invariant sentence weakened under its id, a schema or AGENTS.md edited on the audited head, an undeclared script change that main-tests must fail); legacy task ids are grandfathered by the checked-in list scripts/legacy-task-ids.txt, which only shrinks and is excluded from the line cap as data"
    67	premises:
    68	  - claim: PyYAML is already installed by uv in the Makefile and CI; jsonschema is not yet named anywhere and V1 adds --with jsonschema; both resolve through uv on this host
    69	    command: "grep -n 'with pyyaml\\|jsonschema' Makefile .github/workflows/*.yml; uv run --no-project --with jsonschema --with pyyaml python -c 'import jsonschema, yaml; print(jsonschema.__version__, yaml.__version__)'"
    70	    output: "Makefile:189 and :203 and agent-assets.yml:35 use --with pyyaml; no jsonschema anywhere; 4.26.0 6.0.3"
     1	---
     2	{
     3	  "audit_findings": [],
     4	  "dispatch": [
     5	    "AGMSG-TASK v1 task_id=dotfiles-T133-task-generator-plan-check-a01 round=1 repo=~/Workspace/dotfiles/.claude/worktrees/worker-c task_file=.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a01.md task_sha256=a43cb44b6e6a436baea5c8b303e178a5b31bcaff9f80ef77a3ed51eaf8cde51a deadline=none done_signal=AGMSG-RESULT note=a009:plan-024-P1-12(task-from-plan.py,checker-C11-C15-in-their-own-test-module,plan-check.py);fresh-branch-tools/task-generator-plan-check-a01-from-origin/main(68f8a70a-or-later);your-P1-5-a02-branch-stays-for-its-audit;security:true;single-commands,no-@codex-review;RESULT-carries-task_copy-and-precheck=pending-411;read-the-task-file-first read_at=read"
     6	  ],
     7	  "format": 1,
     8	  "head": "9da0ed3fe67fd1f9267c56fcdcb7e5aaaaa9ffab",
     9	  "ledger": [
    10	    {
    11	      "class": "trust-boundary-pr-input",
    12	      "id": "4306960622"
    13	    },
    14	    {
    15	      "class": "missing-input-crash",
    16	      "id": "4306960626"
    17	    },
    18	    {
    19	      "class": "string-form-comparison",
    20	      "id": "4306960630"
    21	    }
    22	  ],
    23	  "pr": 417,
    24	  "replans": {},
    25	  "searches": [],
    26	  "task": "dotfiles-T133-task-generator-plan-check-a01"
    27	}
    28	---
    29	
    30	# Acceptance record: dotfiles-T133-task-generator-plan-check-a01
    31	
    32	Plan 024 P1-12: task-from-plan.py (a task text from a todo row with every premise and Check command run), the consistency checker's C11 to C15, and plan-check.py (form, drift, invariants over the plan 024 files). Wave P-W3 brought forward to the P-W1 slot because a009 was free and the files are disjoint from everything in flight. Seat: a009 (worker-c, Claude).
    33	
    34	- 2026-10-18T09:10Z record created before the first dispatch (Orchestrator Playbook step 6).
    35	
    36	- 2026-10-18T10:13:51Z: a009 `status=question`: C11 to C15 turn two exact-set tests of `tests/unit/test_task_checkers.py` red (a file outside its allowed_files, in flight in PR #413); options (a) the module joins allowed_files for the two expected sets after #413 merges, (b) an opt-in flag, (c) another rule; default (a). 10:17:47Z `status=blocked` waiting for the answer (everything else done at local commit 18a07ae7; caps 493/600 and 342/700; C14 differs on 10 files: BSD wc padding, uv/codex absent, stale premises; plan-check 6 violations).
    37	- counters before the send (`scripts/regime-counters.sh dotfiles-T133-task-generator-plan-check-a01 --history-only`, 10:2xZ): `tasks=1 amendments=0 questions=1 results=0 withdrawn=0 revises=0` (no S2 line).
    38	- 2026-10-18T10:3xZ: amendment 1 (option (a); the module joins allowed_files with its threat row; #413's merge first, rebase on the orchestrator's PING, the two edits, PR, RESULT; C14 whitespace collapsing and the absent-tool warning as clarifications) dispatched to a009, task sha256 e08bb0afe8d508f5327b0e199108ee1b74efdb5d4a2004faed93b1ca4d1f0c68 (previous a43cb44b…). INV-6 after this send: amendments 1, questions 1.
    39	
    40	## RESULT round 1 (2026-10-18T12:43:44Z): PR #417 head ff4d25a8 (code head b3c6b7ea) on de3b73cc
    41	
    42	- a009's RESULT: CI 13/13 pass on ff4d25a8; `task_copy=e08bb0af…` (amendment 1's sha); `precheck=pending-411`; Bot rounds 2: 4306960626 (P1, the generator died on a missing template) `fixed:b3c6b7ea`, 4306960630 (P2, glob overlap compared as strings) `fixed:b3c6b7ea`, 4306960622 (P1, `task-consistency-check.py:70`: C14 runs a task file's premises under `bash -c` with the caller's rights, so the checker executes whatever a PR-controlled task file says) left open with three options in report.md; `bot_final_head=none-in-15min`; C14 real findings on 7 T133 files moved by merges; plan-check 6 findings in report.md.
    43	- counters before the send (`scripts/regime-counters.sh dotfiles-T133-task-generator-plan-check-a01 --pr 417`, 12:5xZ): `tasks=2 amendments=1 questions=1 results=1 withdrawn=0 revises=0 bot_p1_heads_after_result=0` (no S1 or S2 line).
    44	- decision on 4306960622: the Bot is right. The task's own `in-process effects` row says the checker "stays read-only … never through a shell string the plan controls", and the implementation violates that row, so the fix is a round toward the existing text, not a specification change: the worker's option (b), C14 executes premise commands only when the file's sha256 equals a caller-supplied `--premises-sha` (the TASK line's `task_sha256`, which dispatch.sh passes for the file it sends; acceptance on a branch copy passes nothing and C14 prints a not-run note). The one `dispatch.sh` line belongs to the P1-5 lineage (outside this task's files) and is named in report.md. `status=revise previous_head=ff4d25a8…` sent to a009 at 12:5xZ, to run after its #411 revise; `check=tests/unit/test_task_consistency_c11_c15.py::test_c14_executes_premise_commands_only_for_the_dispatched_sha`. INV-6 after the round: amendments 1, questions 1, revises 1 (the last round).
    45	- 12:4xZ: `status=pending-integration` sent for ff4d25a8 (superseded by the revise for the head; the chain runs on the revise-1 head).
    46	- 2026-10-18T13:31:55Z: revise-1 RESULT from a009: PR #417 head 37d969e19f384909510e819d4d56e3cfff45af7c (code head 538e60bd, previous ff4d25a8), CI 13/13 pass, `bot=none-in-15min`; 4306960622 `fixed:538e60bd` (`check=tests/unit/test_task_consistency_c11_c15.py::test_c14_executes_premise_commands_only_for_the_dispatched_sha`: red without the sha wrote the marker, green 13/13 modules); the one `dispatch.sh` line for P1-5's lineage named in report.md (line 238: `--premises-sha "$(value of task_sha256)"` before `"${tf}"`); caps 534/600 and 407/700; INV-6 amendments 1, questions 1, revises 1 (no further round). `status=pending-integration` sent at 13:3xZ; the chain runs after #409, #411 and #416.
    47	
    48	## Owned by dotfiles-T133-task-generator-plan-check-followup-a01 (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)
    49	
    50	local:9da0ed3:1	advisory-p2
    51	local-finding: 9da0ed3:1 not-applicable:advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (- [P2] Classify glob matches before deciding whether C12 applies — scripts/orchestrator/task-consistency-check.py:182-18); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-task-generator-plan-check-followup-a01.md (27d121f5bc4d7ae7d41100e35b8ab026b9d018493eaae601ca5176a72252befb)
    52	local:9da0ed3:2	advisory-p2
    53	local-finding: 9da0ed3:2 not-applicable:advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (- [P2] Detect intersections between two glob allowlists — scripts/orchestrator/plan-check.py:94-99); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-task-generator-plan-check-followup-a01.md (27d121f5bc4d7ae7d41100e35b8ab026b9d018493eaae601ca5176a72252befb)
    54	local:9da0ed3:3	advisory-p2
    55	local-finding: 9da0ed3:3 not-applicable:advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (- [P2] Match complete todo IDs when selecting a wave — scripts/orchestrator/task-from-plan.py:157-159); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-task-generator-plan-check-followup-a01.md (27d121f5bc4d7ae7d41100e35b8ab026b9d018493eaae601ca5176a72252befb)
    56	local:9da0ed3:4	advisory-p2
    57	local-finding: 9da0ed3:4 not-applicable:advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (- [P2] Preserve glob paths in generated allowed_files — scripts/orchestrator/task-from-plan.py:123-124); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-task-generator-plan-check-followup-a01.md (27d121f5bc4d7ae7d41100e35b8ab026b9d018493eaae601ca5176a72252befb)
    58	local:9da0ed3:5	advisory-p2
    59	local-finding: 9da0ed3:5 not-applicable:advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (- [P2] Read each program item through its next numbered heading — scripts/orchestrator/task-from-plan.py:72-75); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-task-generator-plan-check-followup-a01.md (27d121f5bc4d7ae7d41100e35b8ab026b9d018493eaae601ca5176a72252befb)
    60	local:9da0ed3:6	advisory-p2
    61	local-finding: 9da0ed3:6 not-applicable:advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (- [P2] Read the current acceptance status instead of the last textual match — scripts/orchestrator/plan-check.py:155-158); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-task-generator-plan-check-followup-a01.md (27d121f5bc4d7ae7d41100e35b8ab026b9d018493eaae601ca5176a72252befb)
    62	local:9da0ed3:7	advisory-p2
    63	local-finding: 9da0ed3:7 not-applicable:advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (- [P2] Retain premise commands whose executables are unavailable — scripts/orchestrator/task-from-plan.py:67-69); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-task-generator-plan-check-followup-a01.md (27d121f5bc4d7ae7d41100e35b8ab026b9d018493eaae601ca5176a72252befb)
    64	
    65	4306960622	trust-boundary-pr-input
    66	4306960626	missing-input-crash
    67	4306960630	string-form-comparison
    68	
    69	- 2026-10-18T21:0xZ to 21:28Z: the chain update-branched PR #417 (37d969e1 → 9da0ed3fe67fd1f9267c56fcdcb7e5aaaaa9ffab, code head 538e60bd unchanged), waited for the required checks, ran the local review (no P0/P1; advisory rc 0), the sweep (0 gaps) and the record step, which wrote no row for the three Bot threads (the same record-step gap as #408, #409, #416 and #419); the rows were added by hand (`4306960622	trust-boundary-pr-input`, `4306960626	missing-input-crash`, `4306960630	string-form-comparison`, all `fixed`) and the chain re-run.
    70	
    71	## Audit of 9da0ed3 (2026-10-18T21:37Z): three P1, twelve P2; S2 by substance; withdrawal
    72	
    73	- `Verdict: incorrect` (`.orchestration/validation/dotfiles-T133-task-generator-plan-check-a01-audit-9da0ed3.md`). P1: (1) orchestration, the sweep's `fixed:b3c6b7ea` on the missing-template thread: the template (`.orchestration/tasks/dotfiles-T133-result-precheck-a01.md`, a records file that reaches main only at boundaries) is still absent from the final tree, so the generator exits cleanly instead of generating (the cause, a generator that depends on a records file as its template, is not fixed); (2) specification, the a01 text line 40: the in-process-effects row promises no plan-controlled shell string while `task-from-plan.py:148` executes plan text through `bash -c`; (3) orchestration, this record line 44: the C14 revise of 12:5xZ (run premises only for the dispatched sha) changed item 2's mandatory rerun contract, so it was a specification change sent as a revise, bypassing the hashed amendment and the S2 decision at the second amendment. P2 (12): C14 never runs in ordinary dispatch (dispatch.sh passes no sha and the skip counts as success); C15 checks listed sentences, not the assigned INV id set; C12 classifies the glob's spelling before its matches (`install/**` with a shell script escapes); plan-check F2 misses intersecting globs; wave selection by substring (`P1-1` selects P-W3); the path filter drops wildcard scopes; a blank line truncates a program item; command recognition drops unavailable, single-word and redirecting commands; the latest acceptance match ignores timestamps and task identity; a PR occurrence yields one SHA or state; the forbidden-token pattern misses a quoted assignment after `=`; the C12 owner task lacks the checker in its files.
    74	- decision: the auditor is right on P1 (3): the C14 change was an amendment in substance, so the task has had two amendments (INV-6 S2) and the orchestrator continued past it by calling it a revise (mistake M-20261018-15, the class of M-20261018-10 and -12; correction C-76). With the two other P1 and twelve P2 the artifact goes back to design by another context: `dotfiles-T133-task-generator-plan-check-a02` (reset_of a01), redesigned by the review profile with the fifteen findings as items (the template bundled under scripts/, the generator's command execution stated honestly as the orchestrator's own text run in the orchestrator's sandbox or sha-gated, C14 wired through dispatch.sh in the P1-5 lineage, the glob and parser fixes). `status=withdrawn` sent to a009 at 21:3xZ (a009 finishes its #419 round first; PR #417 and its branch stay). The ledger rows for this audit are written at the a02's acceptance against its head.
diff --git a/scripts/orchestrator/task-consistency-check.py b/scripts/orchestrator/task-consistency-check.py
index b90616a5..241826be 100644
--- a/scripts/orchestrator/task-consistency-check.py
+++ b/scripts/orchestrator/task-consistency-check.py
@@ -1,22 +1,40 @@
 """Read-only cross-field check of a format-2 task file, before dispatch and at acceptance (plan 007 T704).
 
-`uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py [--root <repo>] <task.md>...`
+`uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py [--root <repo>]
+[--premises-sha <sha256>] <task.md>...`
 resolves the design path (C6) and probes origin/main with git (C8 to C10) under --root (default: the first file's git
 toplevel), prints `<file name>: OK` or `: FAIL` with one `  C<n> ...` line per finding, and exits 1 when any file fails.
+C14's warnings and skip notes, never findings, go to stderr as `<file name>: warning: <text>` or `<file name>: note:
+<text>`. Every path it opens or hands to git is first resolved and confined to --root; one that leaves it is a finding.
 C1 task_id equals the file name.
 C2 allowed_files covers .orchestration/<task_id>/** and names no other task's .orchestration/<id>/ directory.
 C3 when reset_of is non-empty, a threat_table row names every reset_of id's task.md and the task's own.
 C4 every allowed_files entry (its path before any glob) is named in a row's control, followed by its end, a space, / " ' ( ) , or a glob.
 C5 no residual binds a predecessor's hash ("names the <aNN> file's hash") instead of the task's own.
-C6 design_review.receipt is the design file's current design_review.receipt.
+C6 design_review.receipt is the design file's current design_review.receipt; a design path outside --root is a finding.
 C7 one row per non-path control name and per orchestrator effect name (the SKILL row unit).
 C7b no row other than a non-path control names two allowed_files entries (one row per entry).
 C8 (code tasks) every *_EVIDENCE input the body names and origin/main does not read yet has a threat row.
 C9 (docs tasks) a quoted rule sentence naming a script, *_EVIDENCE, a check id or classes: finds it on origin/main or says once/until.
-C10 (docs tasks) a quoted rule sentence naming a script on origin/main has no `=` or `[...]` literal absent from the script and its test.
+C10 (docs tasks) a quoted rule sentence naming a script on origin/main has no `=` or `[...]` literal absent from the script and its test
+    (each literal reaches git grep after -e, never as an option).
+C11 a disposition's payload has its form's shape: closed: tests/<path>::<identifier>, out-of-scope: an existing task id, residual: 20+ characters.
+C12 every executed or applied file a glob entry matches (*.sh *.py *.yaml *.yml *.json *.toml, or under home/ scripts/ .githooks/
+    .github/), whatever the glob spells, has a row naming it; tests/fixtures/ and the task's own directory are exempt.
+C13 every disposition is exactly one of closed:, residual: or out-of-scope: followed by a space.
+C14 every premise command, run under bash -c with pipefail, PATH <root>/bin:/usr/bin:/bin, prints its pasted output with whitespace runs
+    collapsed (gh, curl and URLs skipped; a tool absent from that PATH is a `C14: tool absent <name>` warning). It runs
+    only for a file whose sha256 is --premises-sha, the dispatched text; any other file gets `C14: not run (no trusted
+    sha)` as a warning and nothing is executed: a structural OK is then no claim that the premises pass.
+C15 with design_review.design, the design on origin/main exists (unless the task carries no invariants and the design is
+    in this checkout, still in flight; a path naming no design anywhere is always one); when its implementing_tasks maps this task to invariant ids, the task carries
+    exactly those ids, an omitted map included, and each sentence equals the design's byte for byte (a list form
+    assigns no ids, so every invariant the task carries does; a design task compares its own definitions).
 """
 
 import argparse
+import hashlib
+import os
 import pathlib
 import re
 import subprocess
@@ -34,6 +52,23 @@ NONPATH = ("in-process effects", "task metadata", "metadata separators", "workfl
 NONPATH += ("new or renamed scripts", "orchestrator effect")
 C9_NAMES = r"(scripts/[\w./-]+|\b[A-Z][A-Z_]{3,}_EVIDENCE\b|task-consistency-check C\d|\bC\d\b of the task-consistency check|\bclasses:)"
 CHECKER = "scripts/orchestrator/task-consistency-check.py"  # where `task-consistency-check C<n>` lands
+FORMS = ("closed: ", "residual: ", "out-of-scope: ")
+APPLIED = (".sh", ".py", ".yaml", ".yml", ".json", ".toml")
+APPLIED_DIRS = ("home/", "scripts/", ".githooks/", ".github/")
+SKIPPED = "C14 skipped network premise"  # a note, never a failure
+ABSENT = "C14: tool absent"  # a warning, never a failure (Amendment 1)
+UNTRUSTED = "C14: not run (no trusted sha)"  # a warning: the file is not the text --premises-sha names (revise 1)
+
+
+def applied(path):
+    """An executed or applied file, by its kind or its place (C12 and task-from-plan.py's concrete rows)."""
+    return path.endswith(APPLIED) or path.startswith(APPLIED_DIRS)
+
+
+def confined(root, rel):
+    """The path resolved under root, or None when it leaves the checkout (PR #418's review)."""
+    path = (root / rel).resolve()
+    return path if path.is_relative_to(root.resolve()) else None
 
 
 def front(text):
@@ -44,8 +79,32 @@ def git(cwd, *args):
     return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=False)
 
 
-def check(p, root):
-    fm = front(text := p.read_text())
+def rerun(cmd, cwd, path=None):
+    """Run a premise or Check command as C14 does; return (stdout, exit status, stderr), stdout None on a timeout.
+
+    The command is bash's script argument (`bash -c`, pipefail on), never spliced into another shell line; premises
+    get PATH <root>/bin:/usr/bin:/bin so a rerun prints what the pasted output says, and task-from-plan.py runs its
+    premises through this same function.
+    """
+    env = {"PATH": path or f"{cwd}/bin:/usr/bin:/bin", "HOME": os.environ.get("HOME", "/")}
+    try:
+        run = subprocess.run(
+            ["bash", "-c", "set -o pipefail\n" + cmd],
+            stdin=subprocess.DEVNULL,  # a command that reads stdin (`head`, `cat`) never waits on the caller's
+            cwd=cwd,
+            env=env,
+            capture_output=True,
+            text=True,
+            timeout=1800,
+            check=False,
+        )
+    except subprocess.TimeoutExpired:
+        return None, 124, ""
+    return run.stdout, run.returncode, run.stderr
+
+
+def check(p, root, premises_sha=None):
+    fm = front(text := (data := p.read_bytes()).decode())
     tid = fm.get("task_id")
     suffix = tid.rsplit("-", 1)[-1]
     fails = []
@@ -71,8 +130,11 @@ def check(p, root):
         if rows and not any(named.search(r.get("control") or "") for r in rows):
             fails.append(f"C4 allowed path has no threat_table row naming it: {a}")
     dr = fm.get("design_review") or {}
-    if dr.get("design") and dr.get("receipt") and (design := root / dr["design"]).exists():
-        cur = (front(design.read_text()).get("design_review") or {}).get("receipt")
+    inside = dr.get("design") and confined(root, dr["design"])
+    if dr.get("design") and not inside:
+        fails.append(f"C6 design path {dr['design']} is outside the checkout")
+    elif inside and dr.get("receipt") and inside.exists():
+        cur = (front(inside.read_text()).get("design_review") or {}).get("receipt")
         if cur and cur != dr["receipt"]:
             fails.append(f"C6 design_review.receipt {dr['receipt']} is not the design's current receipt {cur}")
     for r in rows:
@@ -100,6 +162,9 @@ def check(p, root):
     sentences = re.findall(r'"([^"]{20,})"', body) if fm.get("kind") == "docs" else []
     for sent in sentences:  # C10
         for scr in set(re.findall(r"scripts/[\w./-]+\.(?:sh|py)", sent)):
+            if not confined(root, scr):
+                fails.append(f"C10 rule sentence names {scr}, a path outside the checkout")
+                continue
             if git(root, "cat-file", "-e", f"origin/main:{scr}").returncode:
                 continue
             m = re.search(r"\b(once|until)\b", sent, re.IGNORECASE)
@@ -107,7 +172,8 @@ def check(p, root):
                 continue  # the script is named inside its own landing clause
             test = f"tests/unit/test_{pathlib.Path(scr).stem.replace('-', '_')}.py"
             for lit in set(re.findall(r"`([^`]*(?:=|\[[^\]]+\])[^`]*)`", sent)):
-                if git(root, "grep", "-qF", lit, "origin/main", "--", scr, test).returncode:
+                # After -e the literal is a pattern: `--open-files-in-pager=<cmd>` is searched for, never run.
+                if git(root, "grep", "-qF", "-e", lit, "origin/main", "--", scr, test).returncode:
                     why = f"which neither the script nor {test} carries on origin/main"
                     fails.append(f'C10 rule sentence names {scr} beside the literal `{lit}`, {why}: "{sent[:60]}…"')
     for sent in sentences:  # C9
@@ -125,12 +191,70 @@ def check(p, root):
             if not ok:
                 why = "it is not on origin/main and the sentence has no landing condition"
                 fails.append(f'C9 rule sentence names {n} as present but {why}: "{sent[:70]}…"')
+    for r in rows:  # C13, then C11 on the form it found
+        d = str(r.get("disposition") or "")
+        form = next((f for f in FORMS if d.startswith(f)), None)
+        if form is None:
+            fails.append(f"C13 disposition is not closed:, residual: or out-of-scope: and a space: {d[:60]}")
+            continue
+        load = d[len(form) :]
+        if form == "closed: " and not re.fullmatch(r"tests/[\w./-]+::[A-Za-z_]\w*", load):
+            fails.append(f"C11 closed: payload is not tests/<path>::<identifier>: {load[:60]}")
+        tid_ok = re.fullmatch(r"[A-Za-z0-9][\w.-]*", load) and (root / f".orchestration/tasks/{load}.md").is_file()
+        if form == "out-of-scope: " and not tid_ok:
+            fails.append(f"C11 out-of-scope: {load[:60]} is not a task under .orchestration/tasks/")
+        if form == "residual: " and len(load) < 20:
+            fails.append(f"C11 residual: payload is shorter than 20 characters: {load}")
+    for a in allowed:  # C12: the concrete matches decide, not what the glob spells
+        if not re.search(r"[*?\[]", a) or a.startswith(("tests/fixtures/", own_dir)) or not confined(root, a):
+            continue
+        for f in filter(None, git(root, "ls-files", "-z", "--", f":(glob){a}").stdout.split("\0")):
+            named = any(re.search(re.escape(f) + r"(?=$|[ /\"'(),])", r.get("control") or "") for r in rows)
+            if applied(f) and not f.startswith(("tests/fixtures/", own_dir)) and not named:
+                fails.append(f"C12 the glob {a} matches {f}, which no threat_table row names")
+    premises = fm.get("premises") or []
+    # C14 executes premise commands only for the orchestrator's dispatched text, the bytes whose sha256 the caller
+    # passes (dispatch.sh: the TASK line's task_sha256); a branch copy at acceptance passes none, so nothing runs.
+    if premises and hashlib.sha256(data).hexdigest() != premises_sha:
+        fails.append(UNTRUSTED)
+        premises = []
+    for pre in premises:  # C14
+        cmd, want = str(pre.get("command") or ""), str(pre.get("output") if pre.get("output") is not None else "")
+        if re.search(r"\b(?:gh|curl)\b|https?://", cmd):
+            fails.append(f"{SKIPPED}: {cmd[:60]}")
+            continue
+        got, code, err = rerun(cmd, root)
+        # bash's own line, not exit 127: under pipefail `absent | grep -c` exits with grep's 1.
+        if absent := re.search(r"^bash: line \d+: ([^\s:]+): command not found$", err, re.M):
+            fails.append(f"{ABSENT} {absent.group(1)}: {cmd[:60]}")
+            continue
+        # Runs of whitespace collapse (BSD wc pads its counts; YAML's |- drops the final newline).
+        if got is None or " ".join(got.split()) != " ".join(want.split()):
+            fails.append(f"C14 premise output differs from its rerun: {cmd[:60]}")
+    design, mine = dr.get("design"), fm.get("invariants") if isinstance(fm.get("invariants"), dict) else {}
+    present = inside and not git(root, "cat-file", "-e", f"origin/main:{design}").returncode  # C8's probe
+    shown = git(root, "show", f"origin/main:{design}") if present else None
+    # C15: a design main cannot give leaves a task's invariants unchecked, and a path naming no design on main or in
+    # this checkout is a typo for any task; a design still in flight here assigns nothing yet to a task without any.
+    if inside and (not shown or shown.returncode):
+        fails += [f"C15 design {design} is not on origin/main"] if mine or not (present or inside.exists()) else []
+    elif shown:  # the design's assignment fixes the ids; a design task compares its own definitions
+        dfm = front(shown.stdout) if shown.stdout.startswith("---\n") else None
+        dfm = dfm if isinstance(dfm, dict) else {}
+        canon, assigned = dfm.get("invariants") or {}, dfm.get("implementing_tasks")
+        ids = (assigned.get(tid) or []) if isinstance(assigned, dict) and fm.get("kind") != "design" else None
+        if ids is not None:
+            fails += [f"C15 invariant {k} that {design} assigns to {tid} is missing" for k in ids if k not in mine]
+            fails += [f"C15 invariant {k} is not one {design} assigns to {tid}" for k in mine if k not in ids]
+        bad = [k for k, v in mine.items() if (ids is None or k in ids) and canon.get(k) != v]
+        fails += [f"C15 invariant {k} is not byte-equal to {design} on origin/main" for k in bad]
     return fails
 
 
 def main():
     parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
     parser.add_argument("--root", type=pathlib.Path, help="the repository (default: the first file's git toplevel)")
+    parser.add_argument("--premises-sha", metavar="sha256", help="the dispatched file's sha256; C14 runs only for it")
     parser.add_argument("tasks", nargs="+", type=pathlib.Path, metavar="task.md")
     args = parser.parse_args()
     if args.root is None:
@@ -140,9 +264,14 @@ def main():
         args.root = pathlib.Path(top.stdout.strip())
     rc = 0
     for p in args.tasks:
-        fails = check(p, args.root)
-        print(f"{p.name}: {'FAIL' if fails else 'OK'}", *fails, sep="\n  ")
-        rc |= bool(fails)
+        fails = check(p, args.root, args.premises_sha)
+        notes = [f for f in fails if f.startswith((SKIPPED, ABSENT, UNTRUSTED))]
+        bad = [f for f in fails if f not in notes]
+        print(f"{p.name}: {'FAIL' if bad else 'OK'}", *bad, sep="\n  ")
+        # The severity is explicit: an untrusted or absent-tool premise is a warning, a network premise a skip note.
+        severity = {n: "note" if n.startswith(SKIPPED) else "warning" for n in notes}
+        print(*(f"{p.name}: {severity[n]}: {n}" for n in notes), sep="\n", file=sys.stderr, end="\n" if notes else "")
+        rc |= bool(bad)
     return rc
 
 

 succeeded in 238ms:
---
task_id: dotfiles-T133-task-generator-plan-check-a01
round: 2
status: result
---

# Report

Worker `claude-standard-dot-a009` (Claude Code, worker-c). Branch `tools/task-generator-plan-check-a01` from `origin/main` 68f8a70a, rebased onto `origin/main` de3b73cc after #413 merged; PR #417 (draft until CI is green); tested code head d7332ebb9cef85a440a0d7c6a0b8a35136ad0690, then 562e77f4bfb1cf43738d857cda7b672acf302b02 after CI round 1 (a test-only fix) and b3c6b7ea382dbf0b5d16de7005486a6b605a8a72 after Bot round 1 (both below; the RESULT names the final evidence-only head). Task copy `.orchestration/dotfiles-T133-task-generator-plan-check-a01/task.md` is byte-identical to the amended dispatched file: sha256 `e08bb0afe8d508f5327b0e199108ee1b74efdb5d4a2004faed93b1ca4d1f0c68`. INV-6: amendments=1 questions=1 revises=0.

## What changed

- `scripts/orchestrator/task-from-plan.py` (new, item 1): reads the todo row, the program items `(n)` it names, the Q-A row (`security: true` when the row lists the id or a `P1-a〜P1-b` range holds it) and the section-6 wave row; proposes `allowed_files` from the backtick paths plus `git grep -l -F <script> -- scripts tests` hits (each a `# from:` line in Files) and the task's own directory; drafts one residual row per path entry and copies the task-copy, evidence, non-path and orchestrator-effect rows of `dotfiles-T133-result-precheck-a01.md` with the id replaced; runs every backtick command of the items through the checker's own `rerun` (C14's environment, so C14 reproduces what it pastes; a nonzero exit is a `verify:` claim with its code, a gh, curl or URL command is not run); runs the sibling task file's Check commands once in a detached scratch worktree of `origin/main` and removes it; writes the file and prints the checker's verdict, exit 0 or 1.
- `scripts/orchestrator/task-consistency-check.py` (item 2): C11 to C15 after C10, C1 to C10 and C7b untouched. C14 runs each premise under `bash -c` with `set -o pipefail`, PATH `<root>/bin:/usr/bin:/bin` and HOME kept, timeout 1800 s, and compares after collapsing whitespace runs (amendment 1). A tool absent from that PATH is the warning `C14: tool absent <name>`, read from bash's own `bash: line N: <name>: command not found` line rather than from exit 127, because under pipefail `codex exec --help | grep -c x` exits with grep's 1. The skip note and the tool-absent warning are not findings: they go to stderr as `<file>: <note>`, so stdout keeps the docstring's contract of one `  C<n> …` line per finding (the reason is the historical test below, whose parser reads every indented stdout line as a finding id and is not to change).
- `scripts/orchestrator/plan-check.py` (new, item 3): F1 to F6 form checks, `--drift` (gh `pr view` per cited PR with a sha or state word near it, `024-progress.tsv` state against the latest acceptance status) and `--invariants` (the fixed forbidden patterns and `claude.permissions.ask` entries added against `origin/main`); one line per violation, exit 1.
- Tests (item 4): `tests/unit/test_task_from_plan.py`, `tests/unit/test_plan_check.py`, `tests/unit/test_task_consistency_c11_c15.py` (one red fixture per new check; amendment 1's whitespace and tool-absent cases, the latter for a bare command and a pipeline, asserting stdout holds the verdict alone). None imports PyYAML (`make unit-test` has none); YAML is read back through `uv run --no-project --with pyyaml`.

## The two edits of tests/unit/test_task_checkers.py (amendment 1, option (a))

Applied after the rebase onto #413's merge; the module's diff against `origin/main` is these two hunks and nothing else (validation.md).

1. `test_task_consistency_check_c4_names_an_entry_only_at_a_path_boundary`: the fixture row `{"control": "the PR adds scripts/foo.py<after>"}` gains `"disposition": "residual: a compensating control"` (the wording the module's other rows use). Without a disposition C13 reports `disposition is not closed:, residual: or out-of-scope: and a space` on every case; with it the expected sets (`{"C4"}` for `.bak`, empty otherwise) hold.
2. `test_task_consistency_check_detects_the_ten_historical_files`: ids added, each from the new check's finding on that file (pasted in validation.md). After revise 1 the test passes no `--premises-sha`, so C14 executes nothing on these fixtures and the process-rules files' C14 ids, added in round 1, were removed again: the final edit adds only C11 and C15. Round 1's reasoning is kept below as the record of what C14 did then.
   - (round 1, removed in revise 1) process-rules a02, a03, a04, a05, a06 gained C14: their premise `~/.agents/skills/agmsg/scripts/history.sh dotfiles-conformance --limit 1000 | grep 'AGMSG-RESULT v1 task_id=dotfiles-T128-process-rules-redesign-a01' | cut -c1-140` no longer prints the pasted line, so C14 reports `premise output differs from its rerun` in all three places it runs: in a seat's sandbox C14's environment has no TMPDIR, so the script's `mktemp` falls back to `/tmp`, which the sandbox denies, and it prints nothing; with a writable temp directory it prints the line cut at 140 bytes (C14's environment has no locale, so `cut -c` counts bytes, and `○` and `→` are three each), ending `st` where the paste ends `status`; on CI the script does not exist.
   - regime-counters a01 and a02, ci-skip-orchestration a01 and a02 gain C11 and C15: C11 because their `closed:` payloads are prose, not `tests/<path>::<identifier>` (and regime-counters' `out-of-scope: V2 (…)` names no task file); C15 because their `invariants` (INV-6 on regime-counters, INV-2 on ci-skip-orchestration) are not byte-equal to `.orchestration/tasks/dotfiles-T128-regime-v3-a01.md` on `origin/main`.
   - process-rules a01 gains nothing: its network premises are skipped (a note, on stderr) and its `wc -w home/dot_config/claude/rules/agmsg-orchestration.md` premise still prints 447 words after the whitespace collapse.

## Real runs (validation.md)

- The checker on the sixteen `.orchestration/tasks/dotfiles-T133-*.md` files (untracked in the main checkout, so run with `--root <main checkout>`): C1 to C13 and C15 clean on all sixteen. C14 reports seven files, each a premise the repository has moved past since it was pasted (amendment 1 keeps these as findings; five before #413 merged, seven after):
  - result-precheck a01 and a02: `grep -n '^RECORD_KEYS = ' scripts/require-crit-review.py` pasted the set without `"replans"`, which #413 (de3b73cc) added.
  - permission-guard-gate a01 and a02: `grep -c 'scope=permission' .orchestration/decisions.tsv` pasted 0, prints 1 now.
  - worker-cap-hookspath a01 and a02: `grep -c '^worker_cap:' home/dot_agents/agent-config.yaml` pasted 0, prints 1 since #408; the `Keep at most three workers in total|…` count pasted 2, prints 0.
  - worker-hooks-path a01: the `grep -n 'shell_environment_policy\|settings.local.json'` line numbers moved by one (352 to 353, 370 to 371, 1418 to 1419).
  - Warnings (not findings): `C14: tool absent uv` on verdict-audit-pool a01 and a02, `C14: tool absent codex` on worker-hooks-path a01.
  So the Check's "green (C1 to C15)" holds for C1 to C13 and C15 and not for C14 on those seven files.
- `plan-check.py` once against the main checkout (the plan files are untracked there): exit 1 with six violations, reported, not fixed (Out of scope):
  1. `F3 024-todo.md:22 P1-13 names no bottleneck id of 5.0 or 5.10`
  2. `F3 024-todo.md:23 P1-14 names no bottleneck id of 5.0 or 5.10`
  3. `F4 024-checklists.md:9 P1-a holds no backtick command or file path`
  4. `F6 024-omp-cutover-and-corrective-order.md:39 cites dotfiles-T131-claude-pinned-merge-gate-fix-a01, which is not a task file`
  5. `F6 024-omp-cutover-and-corrective-order.md:70` (the same id)
  6. `F6 024-todo.md:9` (the same id)

## Observations for the orchestrator (no change made)

- Threat-table wording: the `in-process effects` row says every premise and Check command "runs under python -I or bash with set -euo pipefail, never through a shell string the plan controls". Item 2 mandates C14's `bash -c` with `set -o pipefail` on the premise string, and item 1 pastes what C14 reruns, so both the generator and C14 do run a plan- or task-controlled string in a shell, under `set -o pipefail` (not `-eu`, which would change what a premise like `cmd; other` prints). The row's control is wrong as worded; the residual is that a task file's or plan item's backtick command runs with the caller's user rights, only on an orchestrator-written file. A corrected sentence: "premise and Check commands come from the task or plan text the orchestrator writes and run under `bash -c` with `set -o pipefail` and PATH `<root>/bin:/usr/bin:/bin`".
- C14 runs every premise of every file it is given, including the historical fixtures in `test_task_checkers.py`, whose `run_check` allows 120 s. Inside a seat's sandbox their `history.sh` premise fails at once (no TMPDIR, above). Outside a sandbox it reads the live agmsg bus in full, five times (one run took over 100 s here with a writable temp directory), so `make unit-test` run unsandboxed on a machine with the bus can time that test out. A trial that passed TMPDIR through to C14 (so premises that make temp files work inside a sandbox) turned the sandboxed run into that slow path and was reverted; C14's environment stays PATH and HOME only. A follow-up that runs the historical test with a temporary HOME would remove the bus from the unit suite; it is a test-line change amendment 1 does not allow here. The ten files' C14 ids rest on environment facts: `history.sh` older than 1000 messages or absent, `sha256sum` absent from `/usr/bin:/bin` on macOS (a warning) and present on Linux CI, and `agmsg-orchestration.md` staying at 447 words (a01 gains C14 the day it changes).
- The green-set subtest of `test_task_consistency_c11_c15.py` is skipped in this tree, because the T133 task files exist only untracked in the main checkout and on the unmerged boundary branch. It runs once they land on `main`.

[memory:decision] T133 P1-12: task-consistency-check.py C14 reruns premises under bash -c with pipefail and PATH <root>/bin:/usr/bin:/bin (env PATH and HOME only), compares after collapsing whitespace runs, and prints its skip notes and `C14: tool absent <name>` warnings on stderr, so stdout holds one `  C<n>` line per finding.

CompactionDB (this worktree's, disposable with it): `uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content '<the decision above, plus the generator's refusal>'` returned memory id `038a7ed7-35bc-4906-a75e-9a0c41a6eb3a` (validation.md); the orchestrator consolidates adopted decisions into the main checkout's DB at acceptance.

## Check (validation.md)

- The four modules: 12 tests OK, 1 skipped (the green-set subtest above).
- `make unit-test` exits 2 in the sandbox on this head (1198 tests) and on a pristine `origin/main` de3b73cc worktree (1195 tests); the 305 failing names are identical (`cmp`), none in this task's modules. CI's `make unit-test` decides the full suite.
- `make format` exits 2 at `shfmt --diff` on both sides with the same twelve pre-existing files; ruff and prettier pass on the changed `.py` and `.md` files.
- Caps (`git diff --numstat origin/main...HEAD`): 503 changed lines outside `tests/` and `.orchestration/` (cap 600), 373 under `tests/` (cap 700) on d7332ebb; 376 under `tests/` after CI round 1; 511 and 390 on b3c6b7ea after Bot round 1.

## CI round 1

On dfce34d7 `test (macos-14, client)` failed one test, `test_plan_check_reports_each_form_drift_and_invariant_violation_once_and_passes_a_clean_plan`: the clean plan reported `F6 … cites #77, which is not a pull request` (the two ubuntu client jobs were cancelled by fail-fast; every other check passed). Root cause: `uv run` puts its base interpreter's bin directory before PATH, and on the macOS runner that is Homebrew's, which holds a real `gh`, so the test's stub, prepended to PATH outside `uv run`, lost; the real `gh pr view 77` in a non-repository directory exits nonzero. `test_task_checkers.py` records the same runner fact and puts its stub first inside `uv run`; 562e77f4 does the same in `test_plan_check.py` (3 lines; no production change). The local sandbox cannot reproduce the ordering (uv's interpreter directory here holds no `gh`), so CI on the next head is the green proof.

## Bot round 1 (the Codex Bot's review of 35c66022 on `gh pr ready`, 12:11Z; validation.md)

- 4306960626 [P1] `task-from-plan.py:127` reads `.orchestration/tasks/dotfiles-T133-result-precheck-a01.md`, which a clean checkout lacks, and dies with `FileNotFoundError`: fixed:b3c6b7ea. The generator now checks every input it reads up front (the four plan files it opens, the row template and the completion file) and exits 1 naming the missing ones, before writing anything. Bundling the template is not possible here, because `.orchestration/tasks/` is outside `allowed_files`; the files land on `main` with the regime's records. Red-then-green: the generator test removes the template and asserts exit 1, empty stdout, the template's path on stderr, no traceback and no file written. On 35c66022's code it failed on the traceback; on b3c6b7ea it passes.
- 4306960630 [P2] `plan-check.py:88` F2 compares glob entries as literal strings, so `scripts/*.py` and `scripts/two.py` in one wave pass: fixed:b3c6b7ea. Two entries now overlap when one is a directory prefix of the other or either matches the other under `fnmatchcase`. fnmatch's `*` also crosses `/`, which errs toward a report. A new subtest gives exactly `F2 …:11 P-W0 P1-1 and P1-2 share scripts/*.py`; it was red on 35c66022's code (no line) and is green on b3c6b7ea.
- 4306960622 [P1] `task-consistency-check.py:70` C14 runs a task file's premises under `bash -c` with the caller's rights, so the checker described as read-only executes whatever a task file a PR controls says: open:4306960622, proposed for the orchestrator's decision. Item 2 of the task mandates exactly this execution, and the `in-process effects` row's "the checker stays read-only … never through a shell string the plan controls" is the wording flagged above. The Bot's two remedies:
  - A read-only sandbox cannot run in the regime's seats. Nested `sandbox-exec` fails with `sandbox_apply: Operation not permitted` (exit 71, validation.md) inside a seat's sandbox, and Linux CI has no equivalent.
  - A trusted revision changes the checker's interface on a trust boundary, which is the task owner's call.

  The options I see:
  - (a) C14 runs premises only under an explicit flag, which `dispatch.sh` passes for the orchestrator's own file and acceptance never passes for a branch copy; without the flag, C14 prints a "not run" note.
  - (b) C14 runs premises only when the file's sha256 equals a value the caller passes, such as the TASK line's `task_sha256`.
  - (c) The residual stands, and the row's wording is corrected to say what runs where.

  The no-prompt rule allows no `@codex review` on the fix head, so the Bot round count is 2 with this item open.

Round 1 was sent with head ff4d25a8 and this item open (11:43Z RESULT, `pending-integration` at 12:45Z).

## Revise 1 (round 2; `revise.yaml`)

ACCEPTANCE `status=revise` (12:48:05Z): the Bot's P1 4306960622 is right, and the fix is option (b). This is the last round INV-6 allows (revises 1, amendments 1). Code head 538e60bdb9884b3305c1055a3b74ff83ffc719de.

- 4306960622: fixed:538e60bd. `task-consistency-check.py --premises-sha <sha256>`: C14 executes premise commands only for a file whose bytes hash to that value. Any other file gets one `C14: not run (no trusted sha)` note on stderr and nothing is executed. The file is read once (`read_bytes`), and the hash and the parsed premises come from those same bytes. The `in-process effects` row stays as written ("never through a shell string the plan controls"). The sha makes it true: `dispatch.sh` passes the TASK line's `task_sha256`, which it has already checked against the file it sends. The string C14 runs is therefore the orchestrator's dispatched text and not a PR's. A branch copy at acceptance gets no sha, so a PR-controlled task file executes nothing.
- `dispatch.sh` is outside this task's files. The P1-5 lineage needs one line, the checker call at `scripts/orchestrator/dispatch.sh:238`, to become `out="$(uvr python -I "${here}/task-consistency-check.py" --root "${root}" --premises-sha "$(value_of task_sha256)" "${tf}" 2>&1)" || {`. Until then dispatch's check runs C1 to C13 and C15, and C14 prints its note.
- `task-from-plan.py` passes the sha of the file it has just written, its own text whose premises it ran itself a moment earlier, so its verdict still includes C14.
- Selector `test_c14_executes_premise_commands_only_for_the_dispatched_sha`: a task whose premise is `touch <marker>; printf base`.
  - Without a sha, or with a wrong one, the checker exits 0 with the note and the marker is never written.
  - With the file's sha, the premise runs (the marker exists) and compares.
  - An edited output with its own sha fails C14.

  On 538e60bd's parent the no-sha case wrote the marker: `(0, True) != (0, False)`, plus the unknown-flag usage errors. On 538e60bd the four modules give 13 tests OK, 1 skipped.
- With no sha, C14 runs nothing on the historical fixtures. That removes round 1's C14 ids from `test_task_checkers.py` (above) and the live-bus `history.sh` hazard noted under Observations.
- Real runs (validation.md):
  - The sixteen T133 files without a sha: exit 0, C1 to C13 and C15 clean, and the 14 files with premises each print the note.
  - This task's file with its dispatched sha `e08bb0af…`: C14 runs its five premises and they reproduce (OK).

[memory:decision] T133 P1-12 revise 1: task-consistency-check.py C14 executes premise commands only for a file whose sha256 equals --premises-sha (dispatch.sh to pass the TASK line's task_sha256); any other file gets a `C14: not run (no trusted sha)` note and nothing runs. Recorded as memory `3b0ef48d-bc91-4851-8d32-1051f6a5c076` (validation.md).

## Not done yet

The evidence commit, the one push, CI on the final head, the Bot window from that push and the RESULT (`round=revise-1`, `task_copy=e08bb0af…`, `precheck=pending-411`).

cost: n/a
task_id: dotfiles-T133-task-generator-plan-check-a01
round: 2
previous_head: ff4d25a89fcf301fddd6cd218aa6c9c91fe4a6ad
check: tests/unit/test_task_consistency_c11_c15.py::test_c14_executes_premise_commands_only_for_the_dispatched_sha
reason: the Codex Bot's P1 4306960622 on 35c66022 (C14 executes a task file's premise commands with the caller's rights), revise 1 of a01 and its last round under INV-6 (revises 1, amendments 1); the orchestrator chose option (b) of report.md, --premises-sha <sha256>, so C14 executes premise commands only for the orchestrator's dispatched text
---
task_id: dotfiles-T133-task-generator-plan-check-a01
round: 1
---

# Sandbox

Claude Code seat `claude-standard-dot-a009` in its own worktree `.claude/worktrees/worker-c`, Bash sandbox on (macOS Seatbelt), auto mode. Fresh branch `tools/task-generator-plan-check-a01` from `origin/main` 68f8a70a after one `git fetch origin` (a single command, inside the sandbox); the P1-5 branch `tools/result-precheck-a01` stays for its audit.

Inside the sandbox: every edit; the task-file copy from the main checkout (read only); reads of the plan 024 files and the T133 task files, which exist only untracked in the main checkout (and on the unmerged boundary branch), never written; the extended checker and plan-check run against them with `--root <main checkout>`, which C14 turns into running their premise commands there under PATH `<root>/bin:/usr/bin:/bin` (read-only `git`, `grep`, `ls`, `wc` commands; the `gh`, `curl` and URL premises skipped); the unit tests, each in a temporary repository with a bare origin and, for plan-check, a stub `gh`; ruff format through `uvx`.

Permission-gated or outside the sandbox: `agmsg-dispatch` (in `claude.sandbox.excludedCommands`) for the PONGs and the RESULT; `gh pr create`, `gh pr ready`, `gh pr checks` and the Bot listing (Worker Playbook step 4). `git push` runs inside the sandbox with the one-command rule `-c url.https://github.com/mryfmo/.pushInsteadOf=https://github.com/mryfmo/`. Every `gh` command and git write ran on its own; no `@codex review`.

The shared refs moved during the task (the main checkout fetched `origin/main` to 61231cd9, #408), so caps are read with the three-dot form `origin/main...HEAD`.

Amendment 1's order, each a single command inside the sandbox: commit and push of the code and the three modules (two pushes before the rebase, heads d1d23d7d and 5604bdb2); on the orchestrator's `reason=413-merged sha=de3b73cc…` PING, `git fetch origin`, then the rebase. The first `git rebase origin/main` stopped at its first commit because the global signing setting reached for `~/.ssh/id_ed25519.pub`, which the sandbox cannot read, and `git -c commit.gpgsign=false rebase --continue` kept the signing option the rebase had saved; `git rebase --abort` returned the branch to the pushed head 5604bdb2 and `git -c commit.gpgsign=false rebase --no-gpg-sign origin/main` replayed the three commits cleanly onto de3b73cc. The two held `tests/unit/test_task_checkers.py` edits went on as a saved patch (`git apply`), then one commit, then `git push --force-with-lease=tools/task-generator-plan-check-a01:5604bdb2` (the rebase rewrote the pushed branch; the lease names the head it replaces). The PONG to the PING went through `agmsg-dispatch`, which recorded message 2208 and reported its wake as unread; it was not resent.

Revise 1 (round 2), after the a02 revise RESULT as the ACCEPTANCE ordered: `git switch tools/task-generator-plan-check-a01` (a single command); the fix, the red and green runs, the real runs against the main checkout (without a sha: nothing executed; with this task's dispatched sha: its five read-only premises), `contextdb_cli.py memory add`, all inside the sandbox; then one evidence commit, one push, CI and the Bot window.

effects=none
---
task_id: dotfiles-T133-task-generator-plan-check-a01
round: 1
---

# Learning

Task-local triage; nothing promoted.

- C14 is environment- and time-sensitive. Under its PATH `<root>/bin:/usr/bin:/bin`, macOS's BSD `wc -l` pads counts (`       0`) while the pasted outputs were written with an unpadded `wc`, `uv` and `codex` are not on that PATH, and a premise describes write-time state that later merges change (`grep -c '^worker_cap:'` was 0 before #408 and is 1 after). On the sixteen current T133 files C1 to C13 and C15 are clean; before amendment 1 C14 differed on ten, after its whitespace collapse and tool-absent warning on five, and on seven once #413 merged an hour later, each a premise the repository moved past. A generator therefore runs premises through the checker's own `rerun` so its pasted outputs reproduce, and C14 is best read at dispatch, not at acceptance. Applies to P1-12's follow-ups and to dispatch.sh, which runs the checker.
- A tool missing at the head of a pipeline does not exit 127 under `set -o pipefail`: `codex exec --help | grep -c x` exits with grep's 1. The tool-absent warning reads bash's own `bash: line N: <name>: command not found` line instead. Applies to any check that classifies a shell exit.
- A test that parses a tool's output as findings (`test_task_checkers.py` reads every indented line as `  C<n> `) breaks on any other line in the same stream; notes and warnings belong on stderr. Applies to any checker whose stdout an exact-set test reads.
- Adding checks to a checker whose existing test asserts exact finding sets turns that test red even when the old checks are unchanged; the existing module (`tests/unit/test_task_checkers.py`, PR #413's) has to move with the checker. Applies to any extension of a checker with exact-set tests.
- A test module run by `make unit-test` has no PyYAML: fixtures are written as YAML text and read back through `uv run --with pyyaml`.
- Shared refs: a seat's `origin/main` moves when another checkout of the same repository fetches; caps and diffs are read three-dot, against the merge base.
- Revise 1: a checker that runs commands from the file it checks needs the caller to vouch for the bytes. The dispatched sha256 is that vouching, and the checker hashes the same bytes it parses. Applies to any tool that executes text from a file a PR can change.

**Clarifying final invariant requirements**
exec
/bin/zsh -lc 'nl -ba .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a01.md' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 0ms:
     1	---
     2	{
     3	  "audit_findings": [],
     4	  "dispatch": [
     5	    "AGMSG-TASK v1 task_id=dotfiles-T133-task-generator-plan-check-a01 round=1 repo=~/Workspace/dotfiles/.claude/worktrees/worker-c task_file=.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a01.md task_sha256=a43cb44b6e6a436baea5c8b303e178a5b31bcaff9f80ef77a3ed51eaf8cde51a deadline=none done_signal=AGMSG-RESULT note=a009:plan-024-P1-12(task-from-plan.py,checker-C11-C15-in-their-own-test-module,plan-check.py);fresh-branch-tools/task-generator-plan-check-a01-from-origin/main(68f8a70a-or-later);your-P1-5-a02-branch-stays-for-its-audit;security:true;single-commands,no-@codex-review;RESULT-carries-task_copy-and-precheck=pending-411;read-the-task-file-first read_at=read"
     6	  ],
     7	  "format": 1,
     8	  "head": "9da0ed3fe67fd1f9267c56fcdcb7e5aaaaa9ffab",
     9	  "ledger": [
    10	    {
    11	      "class": "trust-boundary-pr-input",
    12	      "id": "4306960622"
    13	    },
    14	    {
    15	      "class": "missing-input-crash",
    16	      "id": "4306960626"
    17	    },
    18	    {
    19	      "class": "string-form-comparison",
    20	      "id": "4306960630"
    21	    }
    22	  ],
    23	  "pr": 417,
    24	  "replans": {},
    25	  "searches": [],
    26	  "task": "dotfiles-T133-task-generator-plan-check-a01"
    27	}
    28	---
    29	
    30	# Acceptance record: dotfiles-T133-task-generator-plan-check-a01
    31	
    32	Plan 024 P1-12: task-from-plan.py (a task text from a todo row with every premise and Check command run), the consistency checker's C11 to C15, and plan-check.py (form, drift, invariants over the plan 024 files). Wave P-W3 brought forward to the P-W1 slot because a009 was free and the files are disjoint from everything in flight. Seat: a009 (worker-c, Claude).
    33	
    34	- 2026-10-18T09:10Z record created before the first dispatch (Orchestrator Playbook step 6).
    35	
    36	- 2026-10-18T10:13:51Z: a009 `status=question`: C11 to C15 turn two exact-set tests of `tests/unit/test_task_checkers.py` red (a file outside its allowed_files, in flight in PR #413); options (a) the module joins allowed_files for the two expected sets after #413 merges, (b) an opt-in flag, (c) another rule; default (a). 10:17:47Z `status=blocked` waiting for the answer (everything else done at local commit 18a07ae7; caps 493/600 and 342/700; C14 differs on 10 files: BSD wc padding, uv/codex absent, stale premises; plan-check 6 violations).
    37	- counters before the send (`scripts/regime-counters.sh dotfiles-T133-task-generator-plan-check-a01 --history-only`, 10:2xZ): `tasks=1 amendments=0 questions=1 results=0 withdrawn=0 revises=0` (no S2 line).
    38	- 2026-10-18T10:3xZ: amendment 1 (option (a); the module joins allowed_files with its threat row; #413's merge first, rebase on the orchestrator's PING, the two edits, PR, RESULT; C14 whitespace collapsing and the absent-tool warning as clarifications) dispatched to a009, task sha256 e08bb0afe8d508f5327b0e199108ee1b74efdb5d4a2004faed93b1ca4d1f0c68 (previous a43cb44b…). INV-6 after this send: amendments 1, questions 1.
    39	
    40	## RESULT round 1 (2026-10-18T12:43:44Z): PR #417 head ff4d25a8 (code head b3c6b7ea) on de3b73cc
    41	
    42	- a009's RESULT: CI 13/13 pass on ff4d25a8; `task_copy=e08bb0af…` (amendment 1's sha); `precheck=pending-411`; Bot rounds 2: 4306960626 (P1, the generator died on a missing template) `fixed:b3c6b7ea`, 4306960630 (P2, glob overlap compared as strings) `fixed:b3c6b7ea`, 4306960622 (P1, `task-consistency-check.py:70`: C14 runs a task file's premises under `bash -c` with the caller's rights, so the checker executes whatever a PR-controlled task file says) left open with three options in report.md; `bot_final_head=none-in-15min`; C14 real findings on 7 T133 files moved by merges; plan-check 6 findings in report.md.
    43	- counters before the send (`scripts/regime-counters.sh dotfiles-T133-task-generator-plan-check-a01 --pr 417`, 12:5xZ): `tasks=2 amendments=1 questions=1 results=1 withdrawn=0 revises=0 bot_p1_heads_after_result=0` (no S1 or S2 line).
    44	- decision on 4306960622: the Bot is right. The task's own `in-process effects` row says the checker "stays read-only … never through a shell string the plan controls", and the implementation violates that row, so the fix is a round toward the existing text, not a specification change: the worker's option (b), C14 executes premise commands only when the file's sha256 equals a caller-supplied `--premises-sha` (the TASK line's `task_sha256`, which dispatch.sh passes for the file it sends; acceptance on a branch copy passes nothing and C14 prints a not-run note). The one `dispatch.sh` line belongs to the P1-5 lineage (outside this task's files) and is named in report.md. `status=revise previous_head=ff4d25a8…` sent to a009 at 12:5xZ, to run after its #411 revise; `check=tests/unit/test_task_consistency_c11_c15.py::test_c14_executes_premise_commands_only_for_the_dispatched_sha`. INV-6 after the round: amendments 1, questions 1, revises 1 (the last round).
    45	- 12:4xZ: `status=pending-integration` sent for ff4d25a8 (superseded by the revise for the head; the chain runs on the revise-1 head).
    46	- 2026-10-18T13:31:55Z: revise-1 RESULT from a009: PR #417 head 37d969e19f384909510e819d4d56e3cfff45af7c (code head 538e60bd, previous ff4d25a8), CI 13/13 pass, `bot=none-in-15min`; 4306960622 `fixed:538e60bd` (`check=tests/unit/test_task_consistency_c11_c15.py::test_c14_executes_premise_commands_only_for_the_dispatched_sha`: red without the sha wrote the marker, green 13/13 modules); the one `dispatch.sh` line for P1-5's lineage named in report.md (line 238: `--premises-sha "$(value of task_sha256)"` before `"${tf}"`); caps 534/600 and 407/700; INV-6 amendments 1, questions 1, revises 1 (no further round). `status=pending-integration` sent at 13:3xZ; the chain runs after #409, #411 and #416.
    47	
    48	## Owned by dotfiles-T133-task-generator-plan-check-followup-a01 (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)
    49	
    50	local:9da0ed3:1	advisory-p2
    51	local-finding: 9da0ed3:1 not-applicable:advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (- [P2] Classify glob matches before deciding whether C12 applies — scripts/orchestrator/task-consistency-check.py:182-18); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-task-generator-plan-check-followup-a01.md (27d121f5bc4d7ae7d41100e35b8ab026b9d018493eaae601ca5176a72252befb)
    52	local:9da0ed3:2	advisory-p2
    53	local-finding: 9da0ed3:2 not-applicable:advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (- [P2] Detect intersections between two glob allowlists — scripts/orchestrator/plan-check.py:94-99); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-task-generator-plan-check-followup-a01.md (27d121f5bc4d7ae7d41100e35b8ab026b9d018493eaae601ca5176a72252befb)
    54	local:9da0ed3:3	advisory-p2
    55	local-finding: 9da0ed3:3 not-applicable:advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (- [P2] Match complete todo IDs when selecting a wave — scripts/orchestrator/task-from-plan.py:157-159); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-task-generator-plan-check-followup-a01.md (27d121f5bc4d7ae7d41100e35b8ab026b9d018493eaae601ca5176a72252befb)
    56	local:9da0ed3:4	advisory-p2
    57	local-finding: 9da0ed3:4 not-applicable:advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (- [P2] Preserve glob paths in generated allowed_files — scripts/orchestrator/task-from-plan.py:123-124); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-task-generator-plan-check-followup-a01.md (27d121f5bc4d7ae7d41100e35b8ab026b9d018493eaae601ca5176a72252befb)
    58	local:9da0ed3:5	advisory-p2
    59	local-finding: 9da0ed3:5 not-applicable:advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (- [P2] Read each program item through its next numbered heading — scripts/orchestrator/task-from-plan.py:72-75); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-task-generator-plan-check-followup-a01.md (27d121f5bc4d7ae7d41100e35b8ab026b9d018493eaae601ca5176a72252befb)
    60	local:9da0ed3:6	advisory-p2
    61	local-finding: 9da0ed3:6 not-applicable:advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (- [P2] Read the current acceptance status instead of the last textual match — scripts/orchestrator/plan-check.py:155-158); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-task-generator-plan-check-followup-a01.md (27d121f5bc4d7ae7d41100e35b8ab026b9d018493eaae601ca5176a72252befb)
    62	local:9da0ed3:7	advisory-p2
    63	local-finding: 9da0ed3:7 not-applicable:advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (- [P2] Retain premise commands whose executables are unavailable — scripts/orchestrator/task-from-plan.py:67-69); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-task-generator-plan-check-followup-a01.md (27d121f5bc4d7ae7d41100e35b8ab026b9d018493eaae601ca5176a72252befb)
    64	
    65	4306960622	trust-boundary-pr-input
    66	4306960626	missing-input-crash
    67	4306960630	string-form-comparison
    68	
    69	- 2026-10-18T21:0xZ to 21:28Z: the chain update-branched PR #417 (37d969e1 → 9da0ed3fe67fd1f9267c56fcdcb7e5aaaaa9ffab, code head 538e60bd unchanged), waited for the required checks, ran the local review (no P0/P1; advisory rc 0), the sweep (0 gaps) and the record step, which wrote no row for the three Bot threads (the same record-step gap as #408, #409, #416 and #419); the rows were added by hand (`4306960622	trust-boundary-pr-input`, `4306960626	missing-input-crash`, `4306960630	string-form-comparison`, all `fixed`) and the chain re-run.
    70	
    71	## Audit of 9da0ed3 (2026-10-18T21:37Z): three P1, twelve P2; S2 by substance; withdrawal
    72	
    73	- `Verdict: incorrect` (`.orchestration/validation/dotfiles-T133-task-generator-plan-check-a01-audit-9da0ed3.md`). P1: (1) orchestration, the sweep's `fixed:b3c6b7ea` on the missing-template thread: the template (`.orchestration/tasks/dotfiles-T133-result-precheck-a01.md`, a records file that reaches main only at boundaries) is still absent from the final tree, so the generator exits cleanly instead of generating (the cause, a generator that depends on a records file as its template, is not fixed); (2) specification, the a01 text line 40: the in-process-effects row promises no plan-controlled shell string while `task-from-plan.py:148` executes plan text through `bash -c`; (3) orchestration, this record line 44: the C14 revise of 12:5xZ (run premises only for the dispatched sha) changed item 2's mandatory rerun contract, so it was a specification change sent as a revise, bypassing the hashed amendment and the S2 decision at the second amendment. P2 (12): C14 never runs in ordinary dispatch (dispatch.sh passes no sha and the skip counts as success); C15 checks listed sentences, not the assigned INV id set; C12 classifies the glob's spelling before its matches (`install/**` with a shell script escapes); plan-check F2 misses intersecting globs; wave selection by substring (`P1-1` selects P-W3); the path filter drops wildcard scopes; a blank line truncates a program item; command recognition drops unavailable, single-word and redirecting commands; the latest acceptance match ignores timestamps and task identity; a PR occurrence yields one SHA or state; the forbidden-token pattern misses a quoted assignment after `=`; the C12 owner task lacks the checker in its files.
    74	- decision: the auditor is right on P1 (3): the C14 change was an amendment in substance, so the task has had two amendments (INV-6 S2) and the orchestrator continued past it by calling it a revise (mistake M-20261018-15, the class of M-20261018-10 and -12; correction C-76). With the two other P1 and twelve P2 the artifact goes back to design by another context: `dotfiles-T133-task-generator-plan-check-a02` (reset_of a01), redesigned by the review profile with the fifteen findings as items (the template bundled under scripts/, the generator's command execution stated honestly as the orchestrator's own text run in the orchestrator's sandbox or sha-gated, C14 wired through dispatch.sh in the P1-5 lineage, the glob and parser fixes). `status=withdrawn` sent to a009 at 21:3xZ (a009 finishes its #419 round first; PR #417 and its branch stay). The ledger rows for this audit are written at the a02's acceptance against its head.

exec
/bin/zsh -lc "nl -ba .orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-pr-feedback.json | sed -n '75,165p' && git diff --numstat b22a5580d0778e57a66d3f75c76e3c55b88701e1 8a09b9365932f23b09df8aa2385a93d0b3016a3e" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 4ms:
    75	      "bot": true,
    76	      "level": "comment",
    77	      "path": null,
    78	      "line": null,
    79	      "body": "<!-- This is an auto-generated comment: summarize by coderabbit.ai -->\n<!-- This is an auto-generated comment: skip review by coderabbit.ai -->\n\n> [!IMPORTANT]\n> ## Review skipped\n> \n> Auto reviews are disabled on this repository. Please check the settings in the CodeRabbit UI or the `.coderabbit.yaml` file in this repository. To trigger a single review, invoke the `@coderabbitai review` command.\n> \n> <details>\n> <summary><strong>⚙️ Run configuration</strong></summary>\n> <dl>\n> <dd>\n> \n> - **Configuration used**: Repository: mryfmo/dotfiles/.coderabbit.yaml\n> - **Review profile**: CHILL\n> - **Plan**: Advanced\n> - **Run ID**: `d0cfd86c-3ba6-4e24-be80-a65085ec2cd4`\n> \n> </dd>\n> </dl>\n> </details>\n> \n> You can disable this status message by setting the `reviews.review_status` to `false` in the CodeRabbit configuration file.\n> \n> Use the checkbox below for a quick retry:\n> - [ ] <!-- {\"checkboxId\":\"e9bb8d72-00e8-4f67-9cb2-caf3b22574fe\"} --> 🔍 Trigger review\n\n<!-- end of auto-generated comment: skip review by coderabbit.ai -->\n\n<!-- autopilot:start -->\n- [ ] <!-- {\"checkboxId\":\"2708ad07-9f24-4260-9c11-7dc76a49f2e3\"} --> <strong title=\"Keep fixing CodeRabbit findings and required CI, and resolving merge conflicts\">Autofix</strong> · Keep fixing CodeRabbit findings and required CI, and resolving merge conflicts\n<!-- autopilot:end -->\n<!-- tips_start -->\n\n\n\nThanks for using [CodeRabbit](https://coderabbit.ai?utm_source=oss&utm_medium=github&utm_campaign=mryfmo/dotfiles&utm_content=417)! It's free for OSS, and your support helps us grow. If you like it, consider giving us a shout-out.\n\n<details>\n<summary><strong>❤️ Share</strong></summary>\n<dl>\n<dd>\n\n- [X](https://twitter.com/intent/tweet?text=I%20just%20used%20%40coderabbitai%20for%20my%20code%20review%2C%20and%20it%27s%20fantastic%21%20It%27s%20free%20for%20OSS%20and%20offers%20a%20free%20trial%20for%20the%20proprietary%20code.%20Check%20it%20out%3A&url=https%3A//coderabbit.ai)\n- [Mastodon](https://mastodon.social/share?text=I%20just%20used%20%40coderabbitai%20for%20my%20code%20review%2C%20and%20it%27s%20fantastic%21%20It%27s%20free%20for%20OSS%20and%20offers%20a%20free%20trial%20for%20the%20proprietary%20code.%20Check%20it%20out%3A%20https%3A%2F%2Fcoderabbit.ai)\n- [Reddit](https://www.reddit.com/submit?title=Great%20tool%20for%20code%20review%20-%20CodeRabbit&text=I%20just%20used%20CodeRabbit%20for%20my%20code%20review%2C%20and%20it%27s%20fantastic%21%20It%27s%20free%20for%20OSS%20and%20offers%20a%20free%20trial%20for%20proprietary%20code.%20Check%20it%20out%3A%20https%3A//coderabbit.ai)\n- [LinkedIn](https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Fcoderabbit.ai&mini=true&title=Great%20tool%20for%20code%20review%20-%20CodeRabbit&summary=I%20just%20used%20CodeRabbit%20for%20my%20code%20review%2C%20and%20it%27s%20fantastic%21%20It%27s%20free%20for%20OSS%20and%20offers%20a%20free%20trial%20for%20proprietary%20code)\n\n</dd>\n</dl>\n</details>\n\n\n<sub>Comment `@coderabbitai help` to get the list of available commands.</sub>\n\n<!-- tips_end -->",
    80	      "url": "https://github.com/mryfmo/dotfiles/pull/417#issuecomment-6249489670",
    81	      "disposition": "not-applicable:bot summary or onboarding comment, no finding; evidence=jq --argjson u '\"https://github.com/mryfmo/dotfiles/pull/417#issuecomment-6249489670\"' '.items[] | select(.url == $u)' ~/Workspace/dotfiles/.orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-pr-feedback.json"
    82	    },
    83	    {
    84	      "source": "issue_comment",
    85	      "author": "chatgpt-codex-connector[bot]",
    86	      "bot": true,
    87	      "level": "comment",
    88	      "path": null,
    89	      "line": null,
    90	      "body": "<!-- codex-pull-request-review-summary -->\n<!-- codex-review-state:v1 {\"code_review\":{\"commit_sha\":\"35c660222ffd7af143842d310ae8cf3b15db61c5\",\"has_any_findings\":true,\"has_unresolved_findings\":true,\"status\":\"completed\"},\"security_review\":{\"commit_sha\":\"35c660222ffd7af143842d310ae8cf3b15db61c5\",\"has_any_findings\":false,\"has_unresolved_findings\":false,\"status\":\"completed\"}} -->\n<!-- codex-security-review:v1 {\"blockingSeverityThreshold\":\"P0\",\"headSha\":\"35c660222ffd7af143842d310ae8cf3b15db61c5\",\"mergeGateEnabled\":false,\"pullRequestNumber\":417,\"repository\":\"mryfmo/dotfiles\",\"status\":\"completed\"} -->\n## Codex Review Summary\n\nThis comment shows the latest Codex review activity on this pull request.\n\n| Review | Status | Commit | Review trigger |\n| --- | --- | --- | --- |\n| 📝 **Code Review** | ✅ **Completed** <relative-time datetime=\"2026-10-18T12:11:07.372036Z\">2026-10-18T12:11:07.372036Z</relative-time> | `35c6602` | Draft marked ready |\n| 🔒 **Security Review** | ✅ **Completed** <relative-time datetime=\"2026-10-18T12:12:39.986998Z\">2026-10-18T12:12:39.986998Z</relative-time> | `35c6602` | Draft marked ready |\n\n\n\n<details> <summary>ℹ️ About Codex in GitHub</summary>\n<br/>\n\n[Your team has set up Codex to review pull requests in this repo](https://chatgpt.com/codex/cloud/settings/general). Reviews are triggered when you\n- Open a pull request for review\n- Mark a draft as ready\n- Comment \"@codex review\" or \"@codex security review\".\n\nCodex reacts with 👀 while any review is running, comments if it has suggestions, and reacts with 👍 once all reviews finish with no findings.\n\n</details>",
    91	      "url": "https://github.com/mryfmo/dotfiles/pull/417#issuecomment-6249725018",
    92	      "disposition": "not-applicable:bot summary or onboarding comment, no finding; evidence=jq --argjson u '\"https://github.com/mryfmo/dotfiles/pull/417#issuecomment-6249725018\"' '.items[] | select(.url == $u)' ~/Workspace/dotfiles/.orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-pr-feedback.json"
    93	    },
    94	    {
    95	      "source": "review",
    96	      "author": "chatgpt-codex-connector[bot]",
    97	      "bot": true,
    98	      "level": "commented",
    99	      "path": null,
   100	      "line": null,
   101	      "body": "<!-- codex-review-receipt:v1 -->\n\n\n### 💡 Codex Review\n\nHere are some automated review suggestions for this pull request.\n\n**Reviewed commit:** `35c660222f`\n    \n\n<details> <summary>ℹ️ About Codex in GitHub</summary>\n<br/>\n\nCodex has been enabled to automatically review pull requests in this repo. Reviews are triggered when you\n- Open a pull request for review\n- Mark a draft as ready\n- Comment \"@codex review\".\n\nIf Codex has suggestions, it will comment; otherwise it will react with 👍.\n\n\n\n\nWhen you [sign up for Codex through ChatGPT](https://openai.com/codex), Codex can also answer questions or update the PR, like \"@codex address that feedback\".\n            \n</details>",
   102	      "url": "https://github.com/mryfmo/dotfiles/pull/417#pullrequestreview-5562936729",
   103	      "commit": "35c660222ffd7af143842d310ae8cf3b15db61c5",
   104	      "disposition": "not-applicable:review object; its findings are the inline threads, each dispositioned on its own; evidence=jq --argjson u '\"https://github.com/mryfmo/dotfiles/pull/417#pullrequestreview-5562936729\"' '.items[] | select(.url == $u)' ~/Workspace/dotfiles/.orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-pr-feedback.json"
   105	    },
   106	    {
   107	      "source": "review_comment",
   108	      "author": "chatgpt-codex-connector[bot]",
   109	      "bot": true,
   110	      "level": "comment",
   111	      "path": "scripts/orchestrator/task-consistency-check.py",
   112	      "line": 94,
   113	      "body": "**<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Sandbox premise commands before executing them**\n\nWhen the consistency checker runs at acceptance on a PR-controlled task file, any premise reaches `bash -c` here with the review user's permissions. Restricting `PATH` does not prevent shell builtins, absolute executables, redirects, or destructive repository writes, so the checker described as read-only can execute arbitrary code before deciding whether the task is valid; the threat table's claim that the checker stays read-only therefore does not mitigate this boundary. Run premises in a genuinely read-only sandbox or require them to come from a trusted revision.\n\nAGENTS.md reference: [AGENTS.md:L75-L78](https://github.com/mryfmo/dotfiles/blob/35c660222ffd7af143842d310ae8cf3b15db61c5/AGENTS.md#L75-L78)\n\nUseful? React with 👍 / 👎.\n\n<!-- codex-code-review-finding:v1 -->",
   114	      "url": "https://github.com/mryfmo/dotfiles/pull/417#discussion_r4306960622",
   115	      "resolved": false,
   116	      "outdated": false,
   117	      "disposition": "fixed:538e60bd"
   118	    },
   119	    {
   120	      "source": "review_comment",
   121	      "author": "chatgpt-codex-connector[bot]",
   122	      "bot": true,
   123	      "level": "comment",
   124	      "path": "scripts/orchestrator/task-from-plan.py",
   125	      "line": 127,
   126	      "body": "**<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Bundle the required task template**\n\nIn the reviewed commit tree, a repo-wide tree search finds no `.orchestration/tasks/dotfiles-T133-result-precheck-a01.md`, but every generator invocation unconditionally reads that path here. Consequently a clean checkout raises `FileNotFoundError` before writing a task; the closed test masks this because its fixture creates the missing template itself. Include a stable template in the repository or generate these rows without depending on an untracked task file.\n\nAGENTS.md reference: [AGENTS.md:L75-L78](https://github.com/mryfmo/dotfiles/blob/35c660222ffd7af143842d310ae8cf3b15db61c5/AGENTS.md#L75-L78)\n\nUseful? React with 👍 / 👎.\n\n<!-- codex-code-review-finding:v1 -->",
   127	      "url": "https://github.com/mryfmo/dotfiles/pull/417#discussion_r4306960626",
   128	      "resolved": false,
   129	      "outdated": true,
   130	      "disposition": "fixed:b3c6b7ea"
   131	    },
   132	    {
   133	      "source": "review_comment",
   134	      "author": "chatgpt-codex-connector[bot]",
   135	      "bot": true,
   136	      "level": "comment",
   137	      "path": "scripts/orchestrator/plan-check.py",
   138	      "line": 88,
   139	      "body": "**<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Resolve globs before checking wave overlaps**\n\nWhen one same-wave task allows `scripts/*.py` and another allows `scripts/foo.py`, this normalization leaves the first value as the literal string `scripts/*.py`; the later equality/prefix comparison therefore reports no F2 violation even though both tasks can edit `scripts/foo.py`. Expand tracked matches or perform real glob-overlap checks before comparing scopes; the current closed test covers only two identical concrete paths.\n\nAGENTS.md reference: [AGENTS.md:L75-L78](https://github.com/mryfmo/dotfiles/blob/35c660222ffd7af143842d310ae8cf3b15db61c5/AGENTS.md#L75-L78)\n\nUseful? React with 👍 / 👎.\n\n<!-- codex-code-review-finding:v1 -->",
   140	      "url": "https://github.com/mryfmo/dotfiles/pull/417#discussion_r4306960630",
   141	      "resolved": false,
   142	      "outdated": true,
   143	      "disposition": "fixed:b3c6b7ea"
   144	    },
   145	    {
   146	      "source": "annotation",
   147	      "author": "github-actions",
   148	      "bot": true,
   149	      "level": "notice",
   150	      "path": ".github",
   151	      "line": 1,
   152	      "body": "Due to capacity constraints, jobs targeting macOS arm64 runners may experience longer queue times.",
   153	      "url": "https://github.com/mryfmo/dotfiles/actions/runs/39196381817/job/117879956379",
   154	      "check": "test (macos-14, client)",
   155	      "disposition": "not-applicable:runner capacity notice, no finding; evidence=jq --argjson u '\"https://github.com/mryfmo/dotfiles/actions/runs/39196381817/job/117879956379\"' '.items[] | select(.url == $u)' ~/Workspace/dotfiles/.orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-pr-feedback.json"
   156	    },
   157	    {
   158	      "source": "annotation",
   159	      "author": "github-actions",
   160	      "bot": true,
   161	      "level": "notice",
   162	      "path": ".github",
   163	      "line": 1,
   164	      "body": "Due to capacity constraints, jobs targeting macOS arm64 runners may experience longer queue times.",
   165	      "url": "https://github.com/mryfmo/dotfiles/actions/runs/39196381814/job/117879956194",
16	0	.orchestration/dotfiles-T133-task-generator-plan-check-a01/learning.md
107	0	.orchestration/dotfiles-T133-task-generator-plan-check-a01/report.md
5	0	.orchestration/dotfiles-T133-task-generator-plan-check-a01/revise.yaml
20	0	.orchestration/dotfiles-T133-task-generator-plan-check-a01/sandbox.md
603	0	.orchestration/dotfiles-T133-task-generator-plan-check-a01/validation.md
49	0	.orchestration/dotfiles-T133-task-generator-plan-check-a02/dotfiles-T133-task-generator-plan-check-a02-worker-crit.json
14	0	.orchestration/dotfiles-T133-task-generator-plan-check-a02/dotfiles-T133-task-generator-plan-check-a02-worker-review-receipt.md
17	0	.orchestration/dotfiles-T133-task-generator-plan-check-a02/learning.md
38	0	.orchestration/dotfiles-T133-task-generator-plan-check-a02/measure.md
200	0	.orchestration/dotfiles-T133-task-generator-plan-check-a02/report.md
36	0	.orchestration/dotfiles-T133-task-generator-plan-check-a02/sandbox.md
238	0	.orchestration/dotfiles-T133-task-generator-plan-check-a02/task.md
444	0	.orchestration/dotfiles-T133-task-generator-plan-check-a02/validation.md
232	0	scripts/orchestrator/plan-check.py
140	11	scripts/orchestrator/task-consistency-check.py
242	0	scripts/orchestrator/task-from-plan.py
34	0	scripts/orchestrator/task-template.md
166	0	tests/unit/test_plan_check.py
11	5	tests/unit/test_regime_ci.py
9	3	tests/unit/test_task_checkers.py
265	0	tests/unit/test_task_consistency_c11_c15.py
214	0	tests/unit/test_task_from_plan.py

**Implementing safe import mocking**
**Verifying source checks with mocks**
**Handling test command mocking**
**Analyzing task scope and timestamp issues**

I'm sorting through how task file scopes and timestamps interact, especially how old and new tasks overlap and how "latest" timestamps may represent max values rather than strict chronology. This impacts detecting false failures and understanding task handling across file versions and event ordering.
**Analyzing bug reproduction and task constraints**
exec
/bin/zsh -lc "python3 -B -c 'import sys, subprocess, pathlib, types, ast, re, shutil, hashlib, json
from unittest.mock import patch
sys.path.insert(0, \"~/.cache/uv/archive-v0/7OgnLaAJ8JgV819t\")
import yaml
head=\"8a09b9365932f23b09df8aa2385a93d0b3016a3e\"
def source(path):
 return subprocess.check_output([\"git\",\"show\",head+\":\"+path],text=True)
src=source(\"scripts/orchestrator/task-consistency-check.py\")
check=types.ModuleType(\"head_checker\"); check.__file__=\"scripts/orchestrator/task-consistency-check.py\"
exec(compile(src,check.__file__,\"exec\"),check.__dict__)
root=pathlib.Path.cwd()
taskpath=pathlib.Path(\".orchestration/tasks/dotfiles-T133-task-generator-plan-check-a02.md\")
copy=source(\".orchestration/dotfiles-T133-task-generator-plan-check-a02/task.md\").encode()
print(\"task sha\",hashlib.sha256(copy).hexdigest(),\"canonical byte-equal\",copy==taskpath.read_bytes())
print(\"actual amended task findings\",check.check(taskpath,root))
class P:
 stem=\"dotfiles-T9-demo-a01\"
 def __init__(self,fm): self.data=(\"---\\n\"+yaml.safe_dump(fm)+\"---\\n\").encode()
 def read_bytes(self): return self.data
base={\"task_id\":P.stem,\"kind\":\"code\",\"allowed_files\":[\".orchestration/\"+P.stem+\"/**\"]}
fakegit=lambda *args:types.SimpleNamespace(returncode=1,stdout=\"\",stderr=\"\")
with patch.object(check,\"git\",fakegit):
 f=dict(base,design_review={\"design\":\"AGENTS.md\"})
 print(\"C15 named local design absent from main\",check.check(P(f),root))
 f=dict(base,allowed_files=base[\"allowed_files\"]+[\"../../outside/*.py\"])
 print(\"C12 outside glob\",check.check(P(f),root))
genast=ast.parse(source(\"scripts/orchestrator/task-from-plan.py\"))
genast.body=[n for n in genast.body if not (45<=n.lineno<=47)]
gen=types.ModuleType(\"head_generator\");gen.__file__=\"scripts/orchestrator/task-from-plan.py\"; gen.checker=check
exec(compile(genast,gen.__file__,\"exec\"),gen.__dict__)
for s in (\"no-such-tool-a02\",\"no-such-tool-a02 --list\",\"pwd\",\"true\",\"printf hi > marker\"):
 print(\"is_command\",repr(s),gen.is_command(s))
print(\"C12 applied\",[(p,check.applied(p)) for p in (\"AGENTS.md\",\".claude/skills/example/SKILL.md\",\".agents/skills/example/SKILL.md\",\"scripts/tool.py\")])
pc=types.ModuleType(\"head_plan\");exec(compile(source(\"scripts/orchestrator/plan-check.py\"),\"plan-check.py\",\"exec\"),pc.__dict__)
print(\"F2 normalized same literal\",pc.shared(({\"./scripts/tool.py\"},set()),({\"scripts/tool.py\"},set())))
print(\"test hashes\", {p:hashlib.sha256(source(p).encode()).hexdigest() for p in (\"tests/unit/test_task_from_plan.py\",\"tests/unit/test_plan_check.py\",\"tests/unit/test_task_consistency_c11_c15.py\")})
'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 269ms:
task sha 60d4c2db70ec6e8783945f3b6f2052cafe07da85700d574c0f70e477f7c7d1e9 canonical byte-equal True
actual amended task findings ['C11 closed: payload is not tests/<path>::<identifier>: tests/unit/test_regime_ci.py::RegimeCiTest::test_regime_ci_c', 'C14: not run (no trusted sha)']
C15 named local design absent from main []
C12 outside glob []
is_command 'no-such-tool-a02' False
is_command 'no-such-tool-a02 --list' True
is_command 'pwd' True
is_command 'true' True
is_command 'printf hi > marker' True
C12 applied [('AGENTS.md', False), ('.claude/skills/example/SKILL.md', False), ('.agents/skills/example/SKILL.md', False), ('scripts/tool.py', True)]
F2 normalized same literal []
test hashes {'tests/unit/test_task_from_plan.py': '453823892bb6e5cd50dd2e7371a0035bc90cbd65fbc0836c1a6b088a497ad4d4', 'tests/unit/test_plan_check.py': 'ff8202456c02e2d67bf36feec40c58261559ac8054c43ef770993eff30d936c2', 'tests/unit/test_task_consistency_c11_c15.py': 'c1b198a933cade44456943338b94d2dba407c331be46fc9a193180bce1462fa7'}

**Tracking orchestration and audit issues**
**Analyzing audit record inconsistencies**
codex
The task copy matches the dispatched SHA, and the recorded test-source hashes match the final tree. However, the amended task fails its own C11 check because its test selector has an extra `::RegimeCiTest` component. In-memory probes also confirm that C15 accepts a named design absent from main when it exists locally and the task omits invariants.
exec
/bin/zsh -lc "python3 -B -c 'import sys, subprocess, pathlib, types, ast, json
from unittest.mock import patch
sys.path.insert(0,\"~/.cache/uv/archive-v0/7OgnLaAJ8JgV819t\")
import yaml
head=\"8a09b9365932f23b09df8aa2385a93d0b3016a3e\"
def source(path): return subprocess.check_output([\"git\",\"show\",head+\":\"+path],text=True)
check=types.ModuleType(\"checker\");check.__file__=\"scripts/orchestrator/task-consistency-check.py\"
exec(compile(source(check.__file__),check.__file__,\"exec\"),check.__dict__)
tree=ast.parse(source(\"scripts/orchestrator/task-from-plan.py\"));tree.body=[n for n in tree.body if not 45<=n.lineno<=47]
gen=types.ModuleType(\"generator\");gen.__file__=\"scripts/orchestrator/task-from-plan.py\";gen.checker=check
exec(compile(tree,gen.__file__,\"exec\"),gen.__dict__)
root=pathlib.Path.cwd()
template=source(\"scripts/orchestrator/task-template.md\")
plans={
\"024-todo.md\":\"| id | purpose | work | done |\\n| --- | --- | --- | --- |\\n| P1-1 demo | B1 purpose | (1) | all task checks pass without any failures |\\n\",
\"024-design-quality.md\":\"| Q-A | P1-1 |\\n\",
\"024-omp-cutover-and-corrective-order.md\":\"## 6. waves\\n| 波 | a009 |\\n| --- | --- |\\n| W1 | P1-1 |\\n## 7. end\\n\"}
def git(_, *args):
 out=\"\"
 if args[0]==\"rev-parse\":out=str(root) if args[1]==\"--show-toplevel\" else head
 if args[0]==\"show\":out=plans[args[1].split(\"/\")[-1]]
 return types.SimpleNamespace(returncode=0,stdout=out,stderr=\"\")
class Memory:
 def __init__(self):self.written={}
 def read(self,p): return template
 def write(self,p,s): self.written[str(p)]=s;return len(s)
 def bytes(self,p):return self.written[str(p)].encode()
for label,item in [
 (\"root files\",\"**(1) Edit "'`AGENTS.md`, `README.md`, and `Makefile`**'"\\n\"),
 (\"relative file\",\"**(1) Edit "'`./scripts/orchestrator/plan-check.py`**'"\\n\"),
 (\"directory with child\",\"**(1) Edit "'`scripts/orchestrator/` and `scripts/orchestrator/plan-check.py`**'"\\n\")
]:
 plans[\"024-design-programs.md\"]=item
 mem=Memory()
 with patch.object(gen,\"git\",git),patch.object(gen,\"run_check_commands\",lambda *a:[]),patch.object(check,\"git\",git),patch.object(pathlib.Path,\"read_text\",lambda p,*a,**k:mem.read(p)),patch.object(pathlib.Path,\"write_text\",lambda p,s,*a,**k:mem.write(p,s)),patch.object(pathlib.Path,\"read_bytes\",lambda p:mem.bytes(p)),patch.object(pathlib.Path,\"mkdir\",lambda *a,**k:None),patch.object(sys,\"argv\",[\"task-from-plan.py\",\"P1-1\"]),patch.object(gen.subprocess,\"run\",lambda *a,**k:types.SimpleNamespace(returncode=0,stdout=\"\",stderr=\"\")):
  gen.main()
  text=next(iter(mem.written.values()))
  fm=check.front(text)
  print(label,\"allowed:\",fm[\"allowed_files\"])
  findings=check.check(pathlib.Path(\".orchestration/tasks/P1-1.md\"),root)
  print(label,\"checker:\",findings)
'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 334ms:
root files allowed: ['.orchestration/P1-1/**']
root files checker: []
relative file allowed: ['./scripts/orchestrator/plan-check.py', '.orchestration/P1-1/**']
relative file checker: []
directory with child allowed: ['scripts/orchestrator/', 'scripts/orchestrator/plan-check.py', '.orchestration/P1-1/**']
directory with child checker: ['C7b one row names 2 allowed_files entries (scripts/orchestrator/, scripts/orchestrator/plan-check.py); one row per entry']

**Inspecting relative path validation**
exec
/bin/zsh -lc "git show 8a09b9365932f23b09df8aa2385a93d0b3016a3e:.orchestration/dotfiles-T133-task-generator-plan-check-a01/validation.md | sed -n '1,200p'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc "git grep -n 'task-consistency-check.py\\|task-from-plan.py\\|plan-check.py' 8a09b9365932f23b09df8aa2385a93d0b3016a3e -- scripts .github Makefile | head -n 80 && git show 8a09b9365932f23b09df8aa2385a93d0b3016a3e:scripts/orchestrator/regime-ci.py | nl -ba | sed -n '100,230p' && git show 8a09b9365932f23b09df8aa2385a93d0b3016a3e:schemas/task.json | head -n 80" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc "git show 8a09b9365932f23b09df8aa2385a93d0b3016a3e:.orchestration/dotfiles-T133-task-generator-plan-check-a01/validation.md | sed -n '201,400p'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 108ms:
---
task_id: dotfiles-T133-task-generator-plan-check-a01
round: 1
code_head: d7332ebb9cef85a440a0d7c6a0b8a35136ad0690
base: de3b73cc4f8874a30be6adc47a0f07575869d0df
---

# Validation

Every block below is the command's own output, run on the code head named above in the seat's sandbox (sandbox.md). The task files and plan files exist only untracked in the main checkout, so the checker and plan-check runs read it with `--root <main checkout>`.

## Task copy

```
$ shasum -a 256 .orchestration/dotfiles-T133-task-generator-plan-check-a01/task.md
e08bb0afe8d508f5327b0e199108ee1b74efdb5d4a2004faed93b1ca4d1f0c68  .orchestration/dotfiles-T133-task-generator-plan-check-a01/task.md
```

## The four modules

```
head=d7332ebb9cef85a440a0d7c6a0b8a35136ad0690 origin/main=de3b73cc4f8874a30be6adc47a0f07575869d0df merge-base=de3b73cc4f8874a30be6adc47a0f07575869d0df
$ uv run python -m unittest tests.unit.test_task_from_plan tests.unit.test_plan_check tests.unit.test_task_consistency_c11_c15 tests.unit.test_task_checkers -v
test_a_generated_task_passes_the_consistency_check_and_pastes_real_premise_outputs (tests.unit.test_task_from_plan.TaskFromPlanTest.test_a_generated_task_passes_the_consistency_check_and_pastes_real_premise_outputs) ... ok
test_plan_check_reports_each_form_drift_and_invariant_violation_once_and_passes_a_clean_plan (tests.unit.test_plan_check.PlanCheckTest.test_plan_check_reports_each_form_drift_and_invariant_violation_once_and_passes_a_clean_plan) ... ok
test_each_new_check_is_red_on_its_fixture_and_the_existing_checks_are_unchanged (tests.unit.test_task_consistency_c11_c15.TaskConsistencyC11C15Test.test_each_new_check_is_red_on_its_fixture_and_the_existing_checks_are_unchanged) ... 
test_ledger_check_counts_what_the_gate_counts (tests.unit.test_task_checkers.TaskCheckersTest.test_ledger_check_counts_what_the_gate_counts) ... ok
test_ledger_check_passes_a_complete_record (tests.unit.test_task_checkers.TaskCheckersTest.test_ledger_check_passes_a_complete_record) ... ok
test_ledger_check_reads_inherited_audit_ids_from_the_marker (tests.unit.test_task_checkers.TaskCheckersTest.test_ledger_check_reads_inherited_audit_ids_from_the_marker) ... ok
test_ledger_check_reports_the_gaps_of_the_pre_fix_record (tests.unit.test_task_checkers.TaskCheckersTest.test_ledger_check_reports_the_gaps_of_the_pre_fix_record) ... ok
test_task_consistency_check_c4_names_an_entry_only_at_a_path_boundary (tests.unit.test_task_checkers.TaskCheckersTest.test_task_consistency_check_c4_names_an_entry_only_at_a_path_boundary) ... ok
test_task_consistency_check_c9_probes_the_landed_checker_path (tests.unit.test_task_checkers.TaskCheckersTest.test_task_consistency_check_c9_probes_the_landed_checker_path) ... ok
test_task_consistency_check_detects_the_ten_historical_files (tests.unit.test_task_checkers.TaskCheckersTest.test_task_consistency_check_detects_the_ten_historical_files) ... ok
test_task_consistency_check_passes_a_complete_task_file (tests.unit.test_task_checkers.TaskCheckersTest.test_task_consistency_check_passes_a_complete_task_file) ... ok
test_task_consistency_check_reaches_every_other_check (tests.unit.test_task_checkers.TaskCheckersTest.test_task_consistency_check_reaches_every_other_check) ... ok
Ran 12 tests in 11.194s
OK (skipped=1)
exit=0
```

## make unit-test and make format, this head against a pristine origin/main worktree

```
head make unit-test exit=2
head make format exit=2
7 files already formatted
ruff format --check (changed .py) exit=0
Checking formatting...
All matched files use Prettier code style!
prettier --check (changed .md) exit=0
base=de3b73cc4f8874a30be6adc47a0f07575869d0df
base make unit-test exit=2
base make format exit=2
removed=0
head: Ran 1198 tests in 588.079s FAILED (failures=194, errors=111, skipped=3) 
base: Ran 1195 tests in 576.698s FAILED (failures=194, errors=111, skipped=2) 
failing names: head 305, base 305
cmp unit: identical failing sets
in this task's modules: 0
shfmt diff files: head 12, base 12
cmp format: identical file lists
$ git diff --numstat origin/main...HEAD
111	0	.orchestration/dotfiles-T133-task-generator-plan-check-a01/task.md
196	0	scripts/orchestrator/plan-check.py
81	2	scripts/orchestrator/task-consistency-check.py
224	0	scripts/orchestrator/task-from-plan.py
101	0	tests/unit/test_plan_check.py
15	5	tests/unit/test_task_checkers.py
143	0	tests/unit/test_task_consistency_c11_c15.py
109	0	tests/unit/test_task_from_plan.py
outside tests/ and .orchestration/: 503 (cap 600); tests/: 373 (cap 700)
```

The twelve files `shfmt --diff` lists on both sides (`make format` stops at shfmt, so ruff and prettier ran on the changed files above):

```
--- .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/pr-cost.sh.orig
--- .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/resolve-threads.sh.orig
--- .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-advisory.sh.orig
--- .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-review.sh.orig
--- .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/sandbox-scan.sh.orig
--- .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/boundary.sh.orig
--- .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/ff-main.sh.orig
--- .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-audit.sh.orig
--- .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-gate.sh.orig
--- .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/t717-prep.sh.orig
--- home/dot_claude/hooks/executable_project-map-reload.sh.orig
--- tests/install/macos/common/brew.bats.orig
```

## The two edits of tests/unit/test_task_checkers.py

```
$ git diff origin/main...HEAD -- tests/unit/test_task_checkers.py
diff --git a/tests/unit/test_task_checkers.py b/tests/unit/test_task_checkers.py
index f49a9ef9..73f09a51 100644
--- a/tests/unit/test_task_checkers.py
+++ b/tests/unit/test_task_checkers.py
@@ -79,10 +79,14 @@ class TaskCheckersTest(unittest.TestCase):
         for path, block in zip(files, blocks[2::2], strict=True):
             path.write_text(block)
         c2467, c467, c23467 = {"C2", "C4", "C6", "C7"}, {"C4", "C6", "C7"}, {"C2", "C3", "C4", "C6", "C7"}
-        expected = {"process-rules-a01": {"C2", "C6"}, "process-rules-a05": c467, "process-rules-a06": c467}
-        expected |= dict.fromkeys(["process-rules-a02", "process-rules-a03", "process-rules-a04"], c2467)
-        expected |= dict.fromkeys(["regime-counters-a01", "ci-skip-orchestration-a01"], c2467)
-        expected |= dict.fromkeys(["regime-counters-a02", "ci-skip-orchestration-a02"], c23467)
+        expected = {
+            "process-rules-a01": {"C2", "C6"},
+            "process-rules-a05": c467 | {"C14"},
+            "process-rules-a06": c467 | {"C14"},
+        }
+        expected |= dict.fromkeys(["process-rules-a02", "process-rules-a03", "process-rules-a04"], c2467 | {"C14"})
+        expected |= dict.fromkeys(["regime-counters-a01", "ci-skip-orchestration-a01"], c2467 | {"C11", "C15"})
+        expected |= dict.fromkeys(["regime-counters-a02", "ci-skip-orchestration-a02"], c23467 | {"C11", "C15"})
         expected = {f"dotfiles-T128-{t}.md": ids for t, ids in expected.items()}
         self.assertEqual(expected, self.failing_checks(*files, root=ROOT))
 
@@ -186,7 +190,13 @@ class TaskCheckersTest(unittest.TestCase):
         for after in (".bak", "", " and its test", "/task.md", ") and more", '" and more', ", and more", "* and more"):
             with self.subTest(after=after):
                 path = self.task(
-                    uncovered=("scripts/foo.py",), rows=[{"control": f"the PR adds scripts/foo.py{after}"}]
+                    uncovered=("scripts/foo.py",),
+                    rows=[
+                        {
+                            "control": f"the PR adds scripts/foo.py{after}",
+                            "disposition": "residual: a compensating control",
+                        }
+                    ],
                 )
                 found = self.failing_checks(path, root=self.temp, code=1 if after == ".bak" else 0)[path.name]
                 self.assertEqual({"C4"} if after == ".bak" else set(), found)
```

The finding lines the extended checker prints on the ten historical files (stdout only, as the test reads them; `--root` this worktree):

```
dotfiles-T128-process-rules-a01.md: FAIL
  C2 allowed_files lacks .orchestration/dotfiles-T128-process-rules-a01/**
  C6 design_review.receipt .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round16.md is not the design's current receipt .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
dotfiles-T128-process-rules-a02.md: FAIL
  C2 allowed_files lacks .orchestration/dotfiles-T128-process-rules-a02/**
  C4 allowed path has no threat_table row naming it: home/dot_agents/skills/agmsg-orchestration/SKILL.md
  C4 allowed path has no threat_table row naming it: tests/unit/test_agmsg_orchestration_docs.py
  C6 design_review.receipt .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round16.md is not the design's current receipt .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  C7 threat_table has no row named for: task metadata
  C7 threat_table has no row named for: metadata separators
  C7 threat_table has no row named for: in-process effects
  C7 threat_table has no row named for: workflow and interpreter or environment inputs
  C7 threat_table has no row named for: new or renamed scripts
  C7 threat_table has no row named for: orchestrator effect merge
  C7 threat_table has no row named for: orchestrator effect update-branch
  C7 threat_table has no row named for: orchestrator effect forced worker removal
  C14 premise output differs from its rerun: ~/.agents/skills/agmsg/scripts/history.sh dotfiles-conforman
dotfiles-T128-process-rules-a03.md: FAIL
  C2 allowed_files lacks .orchestration/dotfiles-T128-process-rules-a03/**
  C4 allowed path has no threat_table row naming it: home/dot_agents/skills/agmsg-orchestration/SKILL.md
  C6 design_review.receipt .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round16.md is not the design's current receipt .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  C7 threat_table has no row named for: task metadata
  C7 threat_table has no row named for: metadata separators
  C7 threat_table has no row named for: in-process effects
  C7 threat_table has no row named for: workflow and interpreter or environment inputs
  C7 threat_table has no row named for: new or renamed scripts
  C7 threat_table has no row named for: orchestrator effect merge
  C7 threat_table has no row named for: orchestrator effect update-branch
  C7 threat_table has no row named for: orchestrator effect forced worker removal
  C14 premise output differs from its rerun: ~/.agents/skills/agmsg/scripts/history.sh dotfiles-conforman
dotfiles-T128-process-rules-a04.md: FAIL
  C2 allowed_files lacks .orchestration/dotfiles-T128-process-rules-a04/**
  C4 allowed path has no threat_table row naming it: home/dot_agents/skills/agmsg-orchestration/SKILL.md
  C6 design_review.receipt .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round16.md is not the design's current receipt .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  C7 threat_table has no row named for: task metadata
  C7 threat_table has no row named for: metadata separators
  C7 threat_table has no row named for: in-process effects
  C7 threat_table has no row named for: workflow and interpreter or environment inputs
  C7 threat_table has no row named for: new or renamed scripts
  C7 threat_table has no row named for: orchestrator effect merge
  C7 threat_table has no row named for: orchestrator effect update-branch
  C7 threat_table has no row named for: orchestrator effect forced worker removal
  C14 premise output differs from its rerun: ~/.agents/skills/agmsg/scripts/history.sh dotfiles-conforman
dotfiles-T128-process-rules-a05.md: FAIL
  C4 allowed path has no threat_table row naming it: home/dot_agents/skills/agmsg-orchestration/SKILL.md
  C4 allowed path has no threat_table row naming it: tests/fixtures/regime/*.md
  C4 allowed path has no threat_table row naming it: .orchestration/dotfiles-T128-process-rules-a05/**
  C6 design_review.receipt .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round16.md is not the design's current receipt .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  C7 threat_table has no row named for: task metadata
  C7 threat_table has no row named for: metadata separators
  C7 threat_table has no row named for: in-process effects
  C7 threat_table has no row named for: workflow and interpreter or environment inputs
  C7 threat_table has no row named for: new or renamed scripts
  C7 threat_table has no row named for: orchestrator effect merge
  C7 threat_table has no row named for: orchestrator effect update-branch
  C7 threat_table has no row named for: orchestrator effect forced worker removal
  C14 premise output differs from its rerun: ~/.agents/skills/agmsg/scripts/history.sh dotfiles-conforman
dotfiles-T128-process-rules-a06.md: FAIL
  C4 allowed path has no threat_table row naming it: home/dot_agents/skills/agmsg-orchestration/SKILL.md
  C4 allowed path has no threat_table row naming it: .orchestration/dotfiles-T128-process-rules-a06/**
  C6 design_review.receipt .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round16.md is not the design's current receipt .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  C7 threat_table has no row named for: task metadata
  C7 threat_table has no row named for: metadata separators

 succeeded in 167ms:
  C7 threat_table has no row named for: in-process effects
  C7 threat_table has no row named for: workflow and interpreter or environment inputs
  C7 threat_table has no row named for: new or renamed scripts
  C7 threat_table has no row named for: orchestrator effect merge
  C7 threat_table has no row named for: orchestrator effect update-branch
  C7 threat_table has no row named for: orchestrator effect forced worker removal
  C14 premise output differs from its rerun: ~/.agents/skills/agmsg/scripts/history.sh dotfiles-conforman
dotfiles-T128-regime-counters-a01.md: FAIL
  C2 allowed_files lacks .orchestration/dotfiles-T128-regime-counters-a01/**
  C4 allowed path has no threat_table row naming it: scripts/check-regime-boundary.sh
  C4 allowed path has no threat_table row naming it: tests/unit/test_regime_counters.py
  C4 allowed path has no threat_table row naming it: tests/unit/test_check_regime_boundary.py
  C4 allowed path has no threat_table row naming it: tests/fixtures/regime-counters/**
  C6 design_review.receipt .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round16.md is not the design's current receipt .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  C7 threat_table has no row named for: task metadata
  C7 threat_table has no row named for: metadata separators
  C7 threat_table has no row named for: in-process effects
  C7 threat_table has no row named for: workflow and interpreter or environment inputs
  C7 threat_table has no row named for: new or renamed scripts
  C7 threat_table has no row named for: orchestrator effect merge
  C7 threat_table has no row named for: orchestrator effect update-branch
  C7 threat_table has no row named for: orchestrator effect forced worker removal
  C11 closed: payload is not tests/<path>::<identifier>: every count comes from agmsg history or GitHub only; .orches
  C11 closed: payload is not tests/<path>::<identifier>: a record silences the report only through INV-6's anchor for
  C11 closed: payload is not tests/<path>::<identifier>: the script reads the whole team history through lib/storage.
  C11 closed: payload is not tests/<path>::<identifier>: revises = RESULTs for the task_id minus one, exactly INV-6's
  C11 closed: payload is not tests/<path>::<identifier>: review_comment items carrying a P0 or P1 badge, grouped by o
  C11 closed: payload is not tests/<path>::<identifier>: an accepted acceptance record silences a PR-less task only w
  C11 closed: payload is not tests/<path>::<identifier>: the seams are flags, scripts/check-regime-boundary.sh never 
  C11 out-of-scope: V2 (INV-6 counts audit findings from .orchestration/validati is not a task under .orchestration/tasks/
  C15 invariant INV-6 is not byte-equal to .orchestration/tasks/dotfiles-T128-regime-v3-a01.md on origin/main
dotfiles-T128-regime-counters-a02.md: FAIL
  C2 allowed_files lacks .orchestration/dotfiles-T128-regime-counters-a02/**
  C3 no threat_table row names dotfiles-T128-regime-counters-a01 task.md
  C3 no threat_table row names dotfiles-T128-regime-counters-a02 task.md
  C4 allowed path has no threat_table row naming it: scripts/check-regime-boundary.sh
  C4 allowed path has no threat_table row naming it: tests/unit/test_regime_counters.py
  C4 allowed path has no threat_table row naming it: tests/unit/test_check_regime_boundary.py
  C4 allowed path has no threat_table row naming it: tests/fixtures/regime-counters/**
  C6 design_review.receipt .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round18.md is not the design's current receipt .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  C7 threat_table has no row named for: task metadata
  C7 threat_table has no row named for: metadata separators
  C7 threat_table has no row named for: in-process effects
  C7 threat_table has no row named for: workflow and interpreter or environment inputs
  C7 threat_table has no row named for: new or renamed scripts
  C7 threat_table has no row named for: orchestrator effect merge
  C7 threat_table has no row named for: orchestrator effect update-branch
  C7 threat_table has no row named for: orchestrator effect forced worker removal
  C11 closed: payload is not tests/<path>::<identifier>: every count comes from agmsg history or GitHub only; .orches
  C11 closed: payload is not tests/<path>::<identifier>: a record silences the report only through INV-6's anchor for
  C11 closed: payload is not tests/<path>::<identifier>: the accepting AGMSG-RESULT must carry task_id equal to the r
  C11 closed: payload is not tests/<path>::<identifier>: the script reads the whole team history through lib/storage.
  C11 closed: payload is not tests/<path>::<identifier>: revises = RESULTs for the task_id minus one, exactly INV-6's
  C11 closed: payload is not tests/<path>::<identifier>: review_comment items carrying a P0 or P1 badge, grouped by o
  C11 closed: payload is not tests/<path>::<identifier>: an accepted acceptance record silences a PR-less task only w
  C11 closed: payload is not tests/<path>::<identifier>: the seams are flags, scripts/check-regime-boundary.sh never 
  C11 out-of-scope: V2 (INV-6 counts audit findings from .orchestration/validati is not a task under .orchestration/tasks/
  C11 closed: payload is not tests/<path>::<identifier>: tests/fixtures/regime-counters/* hold only the rows and fiel
  C15 invariant INV-6 is not byte-equal to .orchestration/tasks/dotfiles-T128-regime-v3-a01.md on origin/main
dotfiles-T128-ci-skip-orchestration-a01.md: FAIL
  C2 allowed_files lacks .orchestration/dotfiles-T128-ci-skip-orchestration-a01/**
  C4 allowed path has no threat_table row naming it: .github/workflows/remote.yaml
  C4 allowed path has no threat_table row naming it: .github/workflows/test.yaml
  C4 allowed path has no threat_table row naming it: tests/unit/test_workflow_orchestration_skip.py
  C6 design_review.receipt .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round16.md is not the design's current receipt .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  C7 threat_table has no row named for: task metadata
  C7 threat_table has no row named for: metadata separators
  C7 threat_table has no row named for: in-process effects
  C7 threat_table has no row named for: workflow and interpreter or environment inputs
  C7 threat_table has no row named for: new or renamed scripts
  C7 threat_table has no row named for: orchestrator effect merge
  C7 threat_table has no row named for: orchestrator effect update-branch
  C7 threat_table has no row named for: orchestrator effect forced worker removal
  C11 closed: payload is not tests/<path>::<identifier>: the classification is one git diff --name-only over the merg
  C11 closed: payload is not tests/<path>::<identifier>: GitHub reports a skipped job as Success even for a required 
  C11 closed: payload is not tests/<path>::<identifier>: an in-job decision step that fails fails the required contex
  C11 closed: payload is not tests/<path>::<identifier>: should_run is true for every event but pull_request; test as
  C15 invariant INV-2 is not byte-equal to .orchestration/tasks/dotfiles-T128-regime-v3-a01.md on origin/main
dotfiles-T128-ci-skip-orchestration-a02.md: FAIL
  C2 allowed_files lacks .orchestration/dotfiles-T128-ci-skip-orchestration-a02/**
  C3 no threat_table row names dotfiles-T128-ci-skip-orchestration-a01 task.md
  C3 no threat_table row names dotfiles-T128-ci-skip-orchestration-a02 task.md
  C4 allowed path has no threat_table row naming it: .github/workflows/remote.yaml
  C4 allowed path has no threat_table row naming it: .github/workflows/test.yaml
  C4 allowed path has no threat_table row naming it: tests/unit/test_workflow_orchestration_skip.py
  C6 design_review.receipt .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round18.md is not the design's current receipt .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  C7 threat_table has no row named for: task metadata
  C7 threat_table has no row named for: metadata separators
  C7 threat_table has no row named for: in-process effects
  C7 threat_table has no row named for: workflow and interpreter or environment inputs
  C7 threat_table has no row named for: new or renamed scripts
  C7 threat_table has no row named for: orchestrator effect merge
  C7 threat_table has no row named for: orchestrator effect update-branch
  C7 threat_table has no row named for: orchestrator effect forced worker removal
  C11 closed: payload is not tests/<path>::<identifier>: the classification is one git diff --name-only over the merg
  C11 closed: payload is not tests/<path>::<identifier>: GitHub reports a skipped job as Success even for a required 
  C11 closed: payload is not tests/<path>::<identifier>: an in-job decision step that fails fails the required contex
  C11 closed: payload is not tests/<path>::<identifier>: the reader fails closed: inside jobs:, a job name, a job key
  C11 closed: payload is not tests/<path>::<identifier>: INV-2 requires the design on main before the implementing TA
  C11 closed: payload is not tests/<path>::<identifier>: should_run is true for every event but pull_request; test as
  C15 invariant INV-2 is not byte-equal to .orchestration/tasks/dotfiles-T128-regime-v3-a01.md on origin/main

```

## The checker on the sixteen T133 task files (stdout and stderr)

```
$ uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root <main checkout> <main checkout>/.orchestration/tasks/dotfiles-T133-*.md
dotfiles-T133-ci-efficiency-a01.md: C14 skipped network premise: gh api repos/mryfmo/dotfiles/rulesets/24397953 --jq '[.rules
dotfiles-T133-ci-efficiency-a02.md: C14 skipped network premise: gh api repos/mryfmo/dotfiles/rulesets/24397953 --jq '[.rules
dotfiles-T133-permission-guard-gate-a01.md: C14 skipped network premise: /usr/bin/grep -c 'pushinsteadof = https://github.com/' home/
dotfiles-T133-permission-guard-gate-a01.md: C14 skipped network premise: /usr/bin/grep -c 'Bash(gh pr merge:\*)' home/dot_agents/agen
dotfiles-T133-permission-guard-gate-a02.md: C14 skipped network premise: /usr/bin/grep -c 'pushinsteadof = https://github.com/' home/
dotfiles-T133-permission-guard-gate-a02.md: C14 skipped network premise: /usr/bin/grep -c 'Bash(gh pr merge:\*)' home/dot_agents/agen
dotfiles-T133-verdict-audit-pool-a01.md: C14: tool absent uv: uv run --no-project python scripts/pr-feedback.py --help | /
dotfiles-T133-verdict-audit-pool-a02.md: C14: tool absent uv: uv run --no-project python scripts/pr-feedback.py --help | /
dotfiles-T133-worker-hooks-path-a01.md: C14: tool absent codex: codex exec --help | /usr/bin/grep -c -- '--config'
dotfiles-T133-ci-efficiency-a01.md: OK
dotfiles-T133-ci-efficiency-a02.md: OK
dotfiles-T133-ci-efficiency-followup-a01.md: OK
dotfiles-T133-permission-guard-gate-a01.md: FAIL
  C14 premise output differs from its rerun: /usr/bin/grep -c 'scope=permission' .orchestration/decisions
dotfiles-T133-permission-guard-gate-a02.md: FAIL
  C14 premise output differs from its rerun: /usr/bin/grep -c 'scope=permission' .orchestration/decisions
dotfiles-T133-result-precheck-a01.md: FAIL
  C14 premise output differs from its rerun: /usr/bin/grep -n '^RECORD_KEYS = ' scripts/require-crit-revi
dotfiles-T133-result-precheck-a02.md: FAIL
  C14 premise output differs from its rerun: /usr/bin/grep -n '^RECORD_KEYS = ' scripts/require-crit-revi
dotfiles-T133-result-precheck-followup-a01.md: OK
dotfiles-T133-task-generator-plan-check-a01.md: OK
dotfiles-T133-verdict-audit-pool-a01.md: OK
dotfiles-T133-verdict-audit-pool-a02.md: OK
dotfiles-T133-verdict-audit-pool-followup-a01.md: OK
dotfiles-T133-worker-cap-hookspath-a01.md: FAIL
  C14 premise output differs from its rerun: /usr/bin/grep -c -E 'Keep at most three workers in total|Kee
  C14 premise output differs from its rerun: /usr/bin/grep -c '^worker_cap:' home/dot_agents/agent-config
dotfiles-T133-worker-cap-hookspath-a02.md: FAIL
  C14 premise output differs from its rerun: /usr/bin/grep -c -E 'Keep at most three workers in total|Kee
  C14 premise output differs from its rerun: /usr/bin/grep -c '^worker_cap:' home/dot_agents/agent-config
dotfiles-T133-worker-cap-hookspath-followup-a01.md: OK
dotfiles-T133-worker-hooks-path-a01.md: FAIL
  C14 premise output differs from its rerun: /usr/bin/grep -n 'shell_environment_policy\|settings.local.j
exit=1
```

## plan-check.py, run once

```
$ uv run --no-project --with pyyaml python -I scripts/orchestrator/plan-check.py --root <main checkout>
F3 024-todo.md:22 P1-13 names no bottleneck id of 5.0 or 5.10
F3 024-todo.md:23 P1-14 names no bottleneck id of 5.0 or 5.10
F4 024-checklists.md:9 P1-a holds no backtick command or file path
F6 024-omp-cutover-and-corrective-order.md:39 cites dotfiles-T131-claude-pinned-merge-gate-fix-a01, which is not a task file
F6 024-omp-cutover-and-corrective-order.md:70 cites dotfiles-T131-claude-pinned-merge-gate-fix-a01, which is not a task file
F6 024-todo.md:9 cites dotfiles-T131-claude-pinned-merge-gate-fix-a01, which is not a task file
exit=1
```

## CI round 1: test (macos-14, client) on dfce34d7

Run 39124313375, job 117666117287 (`gh run view --log-failed`); the two ubuntu client jobs were cancelled by fail-fast, every other check passed.

```
test (macos-14, client)	Run Python unit tests	2026-10-18T11:49:40.5523770Z FAIL: test_plan_check_reports_each_form_drift_and_invariant_violation_once_and_passes_a_clean_plan (test_plan_check.PlanCheckTest.test_plan_check_reports_each_form_drift_and_invariant_violation_once_and_passes_a_clean_plan)
test (macos-14, client)	Run Python unit tests	2026-10-18T11:49:40.5524590Z ----------------------------------------------------------------------
test (macos-14, client)	Run Python unit tests	2026-10-18T11:49:40.5525090Z Traceback (most recent call last):
test (macos-14, client)	Run Python unit tests	2026-10-18T11:49:40.5550210Z   File "~/work/dotfiles/dotfiles/tests/unit/test_plan_check.py", line 78, in test_plan_check_reports_each_form_drift_and_invariant_violation_once_and_passes_a_clean_plan
test (macos-14, client)	Run Python unit tests	2026-10-18T11:49:40.5556530Z     self.assertEqual(self.plan_check("--drift", "--invariants"), (0, []))
test (macos-14, client)	Run Python unit tests	2026-10-18T11:49:40.5558150Z     ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
test (macos-14, client)	Run Python unit tests	2026-10-18T11:49:40.5559240Z AssertionError: Tuples differ: (1, ['F6 024-omp-cutover-and-corrective-or[46 chars]st']) != (0, [])
test (macos-14, client)	Run Python unit tests	2026-10-18T11:49:40.5559780Z 
test (macos-14, client)	Run Python unit tests	2026-10-18T11:49:40.5560060Z First differing element 0:
test (macos-14, client)	Run Python unit tests	2026-10-18T11:49:40.5561350Z 1
test (macos-14, client)	Run Python unit tests	2026-10-18T11:49:40.5561920Z 0
test (macos-14, client)	Run Python unit tests	2026-10-18T11:49:40.5562350Z 
test (macos-14, client)	Run Python unit tests	2026-10-18T11:49:40.5562530Z + (0, [])
test (macos-14, client)	Run Python unit tests	2026-10-18T11:49:40.5562780Z - (1,
test (macos-14, client)	Run Python unit tests	2026-10-18T11:49:40.5563130Z -  ['F6 024-omp-cutover-and-corrective-order.md:11 cites #77, which is not a '
test (macos-14, client)	Run Python unit tests	2026-10-18T11:49:40.5563540Z -   'pull request'])
test (macos-14, client)	Run Python unit tests	2026-10-18T11:49:40.5563740Z 
test (macos-14, client)	Run Python unit tests	2026-10-18T11:49:40.5564050Z ----------------------------------------------------------------------
test (macos-14, client)	Run Python unit tests	2026-10-18T11:49:40.5564540Z Ran 1198 tests in 380.499s
test (macos-14, client)	Run Python unit tests	2026-10-18T11:49:40.5564810Z 
test (macos-14, client)	Run Python unit tests	2026-10-18T11:49:40.5565080Z FAILED (failures=1, skipped=3)
test (macos-14, client)	Run Python unit tests	2026-10-18T11:49:40.6147570Z make: *** [unit-test] Error 1
```

The stub `gh` lost to the real one: `uv run` puts its base interpreter's bin directory before PATH (on the macOS runner Homebrew's, which holds `gh`). The fix puts the stub first inside `uv run`, as `test_task_checkers.py` does. The four modules on the fix head:

```
head=562e77f4bfb1cf43738d857cda7b672acf302b02
$ uv run python -m unittest tests.unit.test_task_from_plan tests.unit.test_plan_check tests.unit.test_task_consistency_c11_c15 tests.unit.test_task_checkers
Ran 12 tests in 9.435s
OK (skipped=1)
exit=0
$ git diff --numstat origin/main...HEAD -- tests/unit/test_plan_check.py
104	0	tests/unit/test_plan_check.py
```

## Bot round 1 (review of 35c66022, 3 findings)

 succeeded in 207ms:
8a09b9365932f23b09df8aa2385a93d0b3016a3e:scripts/orchestrator/dispatch.sh:37:#   An AGMSG-TASK line whose `task_file=` fails `task-consistency-check.py`
8a09b9365932f23b09df8aa2385a93d0b3016a3e:scripts/orchestrator/dispatch.sh:238:        out="$(uvr python -I "${here}/task-consistency-check.py" --root "${root}" "${tf}" 2>&1)" || {
8a09b9365932f23b09df8aa2385a93d0b3016a3e:scripts/orchestrator/plan-check.py:3:`uv run --no-project --with pyyaml python -I scripts/orchestrator/plan-check.py [--root <repo>] [--drift] [--invariants]`
8a09b9365932f23b09df8aa2385a93d0b3016a3e:scripts/orchestrator/regime-ci.py:32:CHECKER = "scripts/orchestrator/task-consistency-check.py"
8a09b9365932f23b09df8aa2385a93d0b3016a3e:scripts/orchestrator/task-consistency-check.py:3:`uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py [--root <repo>]
8a09b9365932f23b09df8aa2385a93d0b3016a3e:scripts/orchestrator/task-consistency-check.py:54:CHECKER = "scripts/orchestrator/task-consistency-check.py"  # where `task-consistency-check C<n>` lands
8a09b9365932f23b09df8aa2385a93d0b3016a3e:scripts/orchestrator/task-consistency-check.py:64:    """An executed or applied file, by its kind or its place (C12 and task-from-plan.py's concrete rows)."""
8a09b9365932f23b09df8aa2385a93d0b3016a3e:scripts/orchestrator/task-consistency-check.py:86:    get PATH <root>/bin:/usr/bin:/bin so a rerun prints what the pasted output says, and task-from-plan.py runs its
8a09b9365932f23b09df8aa2385a93d0b3016a3e:scripts/orchestrator/task-from-plan.py:3:`uv run --offline --with pyyaml python -I scripts/orchestrator/task-from-plan.py <todo-id> [--out <task.md>]
8a09b9365932f23b09df8aa2385a93d0b3016a3e:scripts/orchestrator/task-from-plan.py:12:.orchestration/tasks/<todo-id>.md), runs task-consistency-check.py on it with --premises-sha of the written bytes,
8a09b9365932f23b09df8aa2385a93d0b3016a3e:scripts/orchestrator/task-from-plan.py:45:spec = importlib.util.spec_from_file_location("checker", pathlib.Path(__file__).with_name("task-consistency-check.py"))
8a09b9365932f23b09df8aa2385a93d0b3016a3e:scripts/orchestrator/task-from-plan.py:199:Generated by scripts/orchestrator/task-from-plan.py from `024-todo.md` row {args.todo_id} and its program items, read from the plan group at {rev}; wave {wave[0] if wave else "none"} ({seat}). Every premise output is the command's own stdout.
8a09b9365932f23b09df8aa2385a93d0b3016a3e:scripts/orchestrator/task-template.md:28:# The task template of scripts/orchestrator/task-from-plan.py
   100	
   101	
   102	def front(data):
   103	    """Return a copy's front matter mapping, or None when it is unreadable or not a mapping."""
   104	    try:
   105	        fm = yaml.safe_load(data.decode().split("\n---\n", 1)[0].lstrip("-\n"))
   106	    except (UnicodeDecodeError, yaml.YAMLError):
   107	        return None
   108	    return fm if isinstance(fm, dict) else None
   109	
   110	
   111	def precheck(root, head, t, result_text, exempt=()):
   112	    """Return the violations of precheck.json's binding, or None when the task carries no precheck.json."""
   113	    data = show(root, head, f".orchestration/{t}/precheck.json")
   114	    if data is None:
   115	        return None
   116	    try:
   117	        doc = json.loads(data)
   118	    except ValueError as error:
   119	        return [f"precheck.json is not JSON: {error}"]
   120	    found = []
   121	    bound = doc.get("head") if isinstance(doc, dict) else None
   122	    if not isinstance(bound, str) or not re.fullmatch(r"[0-9a-f]{40}", bound):
   123	        found.append(f"precheck.json head {bound!r} is not a 40-hex commit id")
   124	    elif bound != head:
   125	        # precheck.json cannot name the commit that adds it: it names the code commit, and the head may add only
   126	        # this task's evidence on top (the evidence-only ancestor rule of verdict.sh condition 1)
   127	        if git(root, "merge-base", "--is-ancestor", bound, head).returncode:
   128	            found.append(f"precheck.json head {bound} is neither the head {head} nor its ancestor")
   129	        elif other := [
   130	            p
   131	            for p in listed(root, "diff", "--name-only", "--no-renames", bound, head)
   132	            if not p.startswith((f".orchestration/{t}/", *exempt))
   133	        ]:
   134	            found.append(
   135	                f"precheck.json head {bound[:12]} differs from the head outside .orchestration/{t}/: {', '.join(other)}"
   136	            )
   137	    if token(result_text, "precheck") != sha256(data):
   138	        found.append(
   139	            f"precheck.json sha256 {sha256(data)} is not result.txt's precheck={token(result_text, 'precheck')}"
   140	        )
   141	    return found
   142	
   143	
   144	def policy(root, base, head, t):
   145	    """Return (the policy bytes, its front matter or None, whether the base's dispatched text is the policy)."""
   146	    dispatched = show(root, base, f".orchestration/tasks/{t}.md")
   147	    data = show(root, head, f".orchestration/{t}/task.md") if dispatched is None else dispatched
   148	    return data, front(data), dispatched is not None
   149	
   150	
   151	def checker(root, data):
   152	    """Return the base checker's violations on the base's dispatched bytes: it hands the text's literals to git (C8 to
   153	    C10) and opens its design path (C6), so a pull request's own text never reaches it (worker review P0 of bcbd6949)."""
   154	    with tempfile.TemporaryDirectory() as scratch:
   155	        cmd = [*CHECKER_RUN, "--root", root, str(Path(scratch, "task.md"))]
   156	        Path(cmd[-1]).write_bytes(data)
   157	        run = subprocess.run(cmd, cwd=root, capture_output=True, text=True, check=False)
   158	    out = run.stdout.splitlines()  # the file is task.md, so C1 compares task_id with `task`; task-id checks <t>
   159	    # only the checker's own verdict line with its exit code counts; a crash also exits 1, with no verdict line
   160	    if (out[:1], run.returncode) not in ((["task.md: OK"], 0), (["task.md: FAIL"], 1)):
   161	        return [("checker", f"no verdict (exit {run.returncode}): {(run.stdout + run.stderr).strip()[-300:]}")]
   162	    lines = [ln.strip() for ln in out[1:] if ln.strip()]
   163	    return [("checker", ln) for ln in lines if not re.fullmatch(r"C1 task_id .* != file task", ln)]
   164	
   165	
   166	def check_task(root, base, head, t, changed, numstat):
   167	    """Return (violations, warnings) for one task, each violation a (rule, detail) pair."""
   168	    copy_path = f".orchestration/{t}/task.md"
   169	    copy = show(root, head, copy_path)
   170	    if (fm := front(copy)) is None:
   171	        return [("front-matter", f"{copy_path} is unreadable or has no front matter mapping")], []
   172	    data, rules, dispatched = policy(root, base, head, t)
   173	    if rules is None:
   174	        return [("front-matter", f"the base's .orchestration/tasks/{t}.md has no front matter mapping")], []
   175	    found, warnings = [], []
   176	    if fm.get("task_id") != t:
   177	        found.append(("task-id", f"the copy's task_id {fm.get('task_id')!r} is not its directory {t}"))
   178	    result = show(root, head, f".orchestration/{t}/result.txt")
   179	    result_text = result.decode(errors="replace") if result is not None else ""
   180	    if dispatched:
   181	        if data != copy:
   182	            found.append(("task-copy", f"{copy_path} differs from the base's dispatched .orchestration/tasks/{t}.md"))
   183	    else:  # the copy's own policy is provisional: a head file or a result.txt token is a claim, never authentication
   184	        unverifiable = "task copy unverifiable (no dispatched text at base)"
   185	        found += [("task-copy", unverifiable)] if os.environ.get("REGIME_REQUIRE_DISPATCHED") == "1" else []
   186	        warnings += [] if os.environ.get("REGIME_REQUIRE_DISPATCHED") == "1" else [unverifiable]
   187	        warnings.append("checker skipped: the copy is unverifiable, and the base's checker reads only the base's text")
   188	        if result is not None and token(result_text, "task_copy") != sha256(copy):
   189	            found.append(
   190	                ("task-copy", f"sha256 {sha256(copy)} is not result.txt's task_copy={token(result_text, 'task_copy')}")
   191	            )
   192	    found += checker(root, data) if dispatched else []
   193	    exempt = tuple(f".orchestration/{p}/" for p in rules.get("reset_of") or [] if isinstance(p, str))
   194	    bound = precheck(root, head, t, result_text, exempt)
   195	    if bound is None:
   196	        warnings.append("precheck absent")
   197	    found += [("precheck", detail) for detail in bound or []]
   198	    entries = [a for a in rules.get("allowed_files") or [] if isinstance(a, str)]
   199	    found += [
   200	        ("allowed-files", f"{p} is outside allowed_files")
   201	        for p in changed
   202	        if not p.startswith(exempt) and not any(allowed(p, a) for a in entries)
   203	    ]
   204	    exceeded, cap_warnings = caps(data.decode(errors="replace"), numstat)
   205	    found += [("caps", detail) for detail in exceeded]
   206	    return found, warnings + cap_warnings
   207	
   208	
   209	def main(argv=None):
   210	    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
   211	    parser.add_argument("--base", required=True, help="the base ref, such as origin/main")
   212	    parser.add_argument("--head", required=True, help="the pull request's head commit")
   213	    parser.add_argument("--root", help="the base checkout (default: the current git toplevel)")
   214	    args = parser.parse_args(argv)
   215	    root = args.root or git(".", "rev-parse", "--show-toplevel").stdout.decode().strip() or "."
   216	    shas = [
   217	        git(root, "rev-parse", "--verify", "--quiet", f"{r}^{{commit}}").stdout.decode().strip()
   218	        for r in (args.base, args.head)
   219	    ]
   220	    if not all(shas):
   221	        print(f"regime-ci: cannot resolve --base {args.base} or --head {args.head} in {root}")
   222	        return 2
   223	    base, head = shas
   224	    at = git(root, "rev-parse", "HEAD").stdout.decode().strip()  # the verifier and the checker must be the base's
   225	    if at != base:
   226	        print(
   227	            f"regime-ci: checkout: {root} is at {at[:12]}, not the base {base[:12]}, so the code run would not be the base's"
   228	        )
   229	        return 1
   230	    try:
fatal: path 'schemas/task.json' does not exist in '8a09b9365932f23b09df8aa2385a93d0b3016a3e'

**Finalizing test coverage details**
**Assessing priority and ownership concerns**
**Verifying .orchestration file and audit scope**
**Analyzing search records and audit inconsistencies**
**Handling path normalization and root checks**
exec
/bin/zsh -lc "git show 8a09b9365932f23b09df8aa2385a93d0b3016a3e:scripts/orchestrator/regime-ci.py | nl -ba | sed -n '55,100p' && git show 8a09b9365932f23b09df8aa2385a93d0b3016a3e:.orchestration/dotfiles-T133-task-generator-plan-check-a01/validation.md | sed -n '401,610p'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 21ms:
    55	    """Return the bytes of path at head, or None when head has no such file."""
    56	    out = git(root, "show", f"{head}:{path}")
    57	    return out.stdout if out.returncode == 0 else None
    58	
    59	
    60	def sha256(data):
    61	    return hashlib.sha256(data).hexdigest()
    62	
    63	
    64	def token(text, name):
    65	    m = re.search(rf"(?:^|\s){name}=(\S+)", text)
    66	    return m.group(1) if m else None
    67	
    68	
    69	def allowed(path, entry):
    70	    """Match an allowed_files entry: `<dir>/**` takes its prefix, `*` and `?` stay within one path segment."""
    71	    if entry.endswith("/**"):
    72	        return path.startswith(entry[:-2])
    73	    rx = "".join("[^/]*" if c == "*" else "[^/]" if c == "?" else re.escape(c) for c in entry)
    74	    return re.fullmatch(rx, path) is not None
    75	
    76	
    77	def caps(text, numstat):
    78	    """Return (violations, warnings) for the `## Check` sentence's caps against the numstat rows."""
    79	    check = text.split("\n## Check", 1)[1].split("\n## ", 1)[0] if "\n## Check" in text else ""
    80	    outside = re.search(r"at most (\d+) changed lines(?: \([^)]*\))? outside ([^(\n]*)", check)
    81	    tests = re.search(r"(\d+)\s+(?:added\s+|changed\s+)?(?:lines\s+)?under\s+`?tests/", check)
    82	    missing = [
    83	        f"no {n} cap in the copy's ## Check section" for n, m in (("outside", outside), ("tests/", tests)) if not m
    84	    ]
    85	    excluded = ["tests/", ".orchestration/"]
    86	    if outside:
    87	        excluded = re.findall(r"`([^`]+)`", re.split(r",\s*(?:and\s+)?\d", outside.group(2))[0]) or excluded
    88	
    89	    def counted(path, prefixes):
    90	        return any(path == p or (p.endswith("/") and path.startswith(p)) for p in prefixes)
    91	
    92	    out_lines = sum(a + d for a, d, p in numstat if not counted(p, excluded))
    93	    test_lines = sum(a + d for a, d, p in numstat if counted(p, ["tests/"]))
    94	    found = []
    95	    if outside and out_lines > int(outside.group(1)):
    96	        found.append(f"{out_lines} changed lines outside {', '.join(excluded)} exceed {outside.group(1)}")
    97	    if tests and test_lines > int(tests.group(1)):
    98	        found.append(f"{test_lines} changed lines under tests/ exceed {tests.group(1)}")
    99	    return found, missing
   100	

The two new cases (the generator refuses a checkout without its records; F2 reports a glob entry against the path it matches) against the code of 35c66022, then on the fix head b3c6b7ea:

```
$ uv run python -m unittest tests.unit.test_task_from_plan tests.unit.test_plan_check   # code of 35c66022, new tests
FAIL: test_a_generated_task_passes_the_consistency_check_and_pastes_real_premise_outputs (tests.unit.test_task_from_plan.TaskFromPlanTest.test_a_generated_task_passes_the_consistency_check_and_pastes_
AssertionError: 'Traceback' unexpectedly found in 'Traceback (most recent call last):\n  File "~/Workspace/dotfiles/.claude/worktrees/worker-c/scripts/orchestrator/task-from-plan.py", li
FAIL: test_plan_check_reports_each_form_drift_and_invariant_violation_once_and_passes_a_clean_plan (tests.unit.test_plan_check.PlanCheckTest.test_plan_check_reports_each_form_drift_and_invariant_viola
AssertionError: Tuples differ: (0, []) != (1, ['F2 024-omp-cutover-and-corrective-or[45 chars]py'])
Ran 2 tests in 2.256s
FAILED (failures=2)
```

```
$ uv run python -m unittest tests.unit.test_task_from_plan tests.unit.test_plan_check tests.unit.test_task_consistency_c11_c15 tests.unit.test_task_checkers   # b3c6b7ea
Ran 12 tests in 9.443s
OK (skipped=1)
```

A read-only premise sandbox cannot nest inside a seat's sandbox (the probe for finding 4306960622):

```
$ sandbox-exec -p '(version 1)(allow default)(deny file-write*)(allow file-write* (literal "/dev/null"))' bash -c 'echo ran; touch ./nested-write-probe'
sandbox-exec: sandbox_apply: Operation not permitted
exit=71
```

## CompactionDB memory

```
$ uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'T133 P1-12: task-consistency-check.py C14 reruns premises … refuses a checkout missing its regime records by name.'
038a7ed7-35bc-4906-a75e-9a0c41a6eb3a
exit=0
```

## Branch, PR and CI

```
$ git log --oneline origin/main..HEAD
5f770f22 docs(orchestration): T133 task-generator-plan-check a01 Bot round 1 evidence (b3c6b7ea)
b3c6b7ea fix(orchestrator): task-from-plan refuses a checkout without its records by name; plan-check F2 treats glob entries as overlapping what they match (T133 task-generator-plan-check a01, Bot round 1)
35c66022 docs(orchestration): T133 task-generator-plan-check a01 CI round 1 evidence (562e77f4)
562e77f4 test(orchestrator): put plan-check's stub gh first inside uv run, as on the macOS runner uv's base bin precedes PATH (T133 task-generator-plan-check a01)
dfce34d7 docs(orchestration): T133 task-generator-plan-check a01 evidence (d7332ebb)
d7332ebb test(orchestrator): the two expected-set edits of test_task_checkers.py for C11 to C15 (T133 task-generator-plan-check a01, amendment 1)
63a089e5 fix(orchestrator): C14 notes and warnings go to stderr, so stdout holds one line per finding (T133 task-generator-plan-check a01)
4c181fab fix(orchestrator): C14 collapses whitespace runs and warns on an absent tool (T133 task-generator-plan-check a01, amendment 1)
747602cd feat(orchestrator): task-from-plan.py, checker C11 to C15 and plan-check.py (T133 task-generator-plan-check a01)
```

The draft PR (its create command run once, 11:41Z), `gh pr ready 417` (12:07:32Z) and the Bot window on 35c66022 (closed 12:22:43Z), as printed:

```
https://github.com/mryfmo/dotfiles/pull/417
✓ Pull request mryfmo/dotfiles#417 is marked as "ready for review"
reviews=1 comments=3
review chatgpt-codex-connector COMMENTED 2026-10-18T12:11:04Z
inline=3
4306960622 chatgpt-codex-connector[bot] scripts/orchestrator/task-consistency-check.py:70 [P1] Sandbox premise commands before executing them
4306960626 chatgpt-codex-connector[bot] scripts/orchestrator/task-from-plan.py:127 [P1] Bundle the required task template
4306960630 chatgpt-codex-connector[bot] scripts/orchestrator/plan-check.py:88 [P2] Resolve globs before checking wave overlaps
```

`gh pr checks 417` on 35c66022 (after CI round 1):

```
CodeRabbit	pass	0
GitGuardian Security Checks	pass	1s
private-bootstrap (macos-14, client)	pass	11s
private-bootstrap (ubuntu-24.04, client)	pass	9s
private-bootstrap (ubuntu-24.04, server)	pass	10s
public-bootstrap (macos-14, client)	pass	9m26s
public-bootstrap (ubuntu-24.04, client)	pass	10m15s
public-bootstrap (ubuntu-24.04, server)	pass	8m0s
test (macos-14, client)	pass	8m21s
test (ubuntu-24.04, client)	pass	8m56s
test (ubuntu-24.04, server)	pass	6m10s
test (ubuntu-26.04, client)	pass	7m40s
validate	pass	1m40s
35c660222ffd7af143842d310ae8cf3b15db61c5
```

## Revise 1: red on ff4d25a8's code, green on 538e60bd

The selector against the checker of ff4d25a8 (the new test and helper, before the fix):

```
$ uv run python -m unittest tests.unit.test_task_consistency_c11_c15
FAIL: test_c14_executes_premise_commands_only_for_the_dispatched_sha (tests.unit.test_task_consistency_c11_c15.TaskConsistencyC11C15Test.test_c14_executes_premise_commands_only_for_the_dispatched_sha) (sha=None)
AssertionError: Tuples differ: (0, True) != (0, False)
FAIL: test_c14_executes_premise_commands_only_for_the_dispatched_sha (tests.unit.test_task_consistency_c11_c15.TaskConsistencyC11C15Test.test_c14_executes_premise_commands_only_for_the_dispatched_sha) (sha='00000000000000000000000
AssertionError: Tuples differ: (2, True) != (0, False)
FAIL: test_c14_executes_premise_commands_only_for_the_dispatched_sha (tests.unit.test_task_consistency_c11_c15.TaskConsistencyC11C15Test.test_c14_executes_premise_commands_only_for_the_dispatched_sha)
AssertionError: Tuples differ: (2, 'usage: task-consistency-check.py [-h][109 chars]a\n') != (0, 'dotfiles-T9-base-a01.md: OK\n')
FAIL: test_each_new_check_is_red_on_its_fixture_and_the_existing_checks_are_unchanged (tests.unit.test_task_consistency_c11_c15.TaskConsistencyC11C15Test.test_each_new_check_is_red_on_its_fixture_and_the_existing_checks_are_unchan
AssertionError: Tuples differ: (2, 'usage: task-consistency-check.py [-h][109 chars]a\n') != (0, 'dotfiles-T9-base-a01.md: OK\n')
Ran 2 tests in 1.109s
FAILED (failures=4)
```

```
$ git log --oneline -1
538e60bd fix(orchestrator): C14 executes premise commands only for the file whose sha256 --premises-sha names (T133 task-generator-plan-check a01 revise 1, Bot 4306960622)
$ uv run python -m unittest tests.unit.test_task_from_plan tests.unit.test_plan_check tests.unit.test_task_consistency_c11_c15 tests.unit.test_task_checkers -v
test_a_generated_task_passes_the_consistency_check_and_pastes_real_premise_outputs ... ok
test_plan_check_reports_each_form_drift_and_invariant_violation_once_and_passes_a_clean_plan ... ok
test_c14_executes_premise_commands_only_for_the_dispatched_sha ... ok
test_each_new_check_is_red_on_its_fixture_and_the_existing_checks_are_unchanged ... 
test_ledger_check_counts_what_the_gate_counts ... ok
test_ledger_check_passes_a_complete_record ... ok
test_ledger_check_reads_inherited_audit_ids_from_the_marker ... ok
test_ledger_check_reports_the_gaps_of_the_pre_fix_record ... ok
test_task_consistency_check_c4_names_an_entry_only_at_a_path_boundary ... ok
test_task_consistency_check_c9_probes_the_landed_checker_path ... ok
test_task_consistency_check_detects_the_ten_historical_files ... ok
test_task_consistency_check_passes_a_complete_task_file ... ok
test_task_consistency_check_reaches_every_other_check ... ok
Ran 13 tests in 7.457s
OK (skipped=1)
$ git diff origin/main...HEAD -- tests/unit/test_task_checkers.py
diff --git a/tests/unit/test_task_checkers.py b/tests/unit/test_task_checkers.py
index f49a9ef9..7df9bd5e 100644
--- a/tests/unit/test_task_checkers.py
+++ b/tests/unit/test_task_checkers.py
@@ -81,8 +81,8 @@ class TaskCheckersTest(unittest.TestCase):
         c2467, c467, c23467 = {"C2", "C4", "C6", "C7"}, {"C4", "C6", "C7"}, {"C2", "C3", "C4", "C6", "C7"}
         expected = {"process-rules-a01": {"C2", "C6"}, "process-rules-a05": c467, "process-rules-a06": c467}
         expected |= dict.fromkeys(["process-rules-a02", "process-rules-a03", "process-rules-a04"], c2467)
-        expected |= dict.fromkeys(["regime-counters-a01", "ci-skip-orchestration-a01"], c2467)
-        expected |= dict.fromkeys(["regime-counters-a02", "ci-skip-orchestration-a02"], c23467)
+        expected |= dict.fromkeys(["regime-counters-a01", "ci-skip-orchestration-a01"], c2467 | {"C11", "C15"})
+        expected |= dict.fromkeys(["regime-counters-a02", "ci-skip-orchestration-a02"], c23467 | {"C11", "C15"})
         expected = {f"dotfiles-T128-{t}.md": ids for t, ids in expected.items()}
         self.assertEqual(expected, self.failing_checks(*files, root=ROOT))
 
@@ -186,7 +186,13 @@ class TaskCheckersTest(unittest.TestCase):
         for after in (".bak", "", " and its test", "/task.md", ") and more", '" and more', ", and more", "* and more"):
             with self.subTest(after=after):
                 path = self.task(
-                    uncovered=("scripts/foo.py",), rows=[{"control": f"the PR adds scripts/foo.py{after}"}]
+                    uncovered=("scripts/foo.py",),
+                    rows=[
+                        {
+                            "control": f"the PR adds scripts/foo.py{after}",
+                            "disposition": "residual: a compensating control",
+                        }
+                    ],
                 )
                 found = self.failing_checks(path, root=self.temp, code=1 if after == ".bak" else 0)[path.name]
                 self.assertEqual({"C4"} if after == ".bak" else set(), found)
```

## Revise 1: real runs

```
$ uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root <main checkout> <main checkout>/.orchestration/tasks/dotfiles-T133-*.md   # no --premises-sha
dotfiles-T133-ci-efficiency-a01.md: C14: not run (no trusted sha)
dotfiles-T133-ci-efficiency-a02.md: C14: not run (no trusted sha)
dotfiles-T133-permission-guard-gate-a01.md: C14: not run (no trusted sha)
dotfiles-T133-permission-guard-gate-a02.md: C14: not run (no trusted sha)
dotfiles-T133-permission-guard-gate-a03.md: C14: not run (no trusted sha)
dotfiles-T133-regime-ci-a01.md: C14: not run (no trusted sha)
dotfiles-T133-result-precheck-a01.md: C14: not run (no trusted sha)
dotfiles-T133-result-precheck-a02.md: C14: not run (no trusted sha)
dotfiles-T133-task-generator-plan-check-a01.md: C14: not run (no trusted sha)
dotfiles-T133-verdict-audit-pool-a01.md: C14: not run (no trusted sha)
dotfiles-T133-verdict-audit-pool-a02.md: C14: not run (no trusted sha)
dotfiles-T133-worker-cap-hookspath-a01.md: C14: not run (no trusted sha)
dotfiles-T133-worker-cap-hookspath-a02.md: C14: not run (no trusted sha)
dotfiles-T133-worker-hooks-path-a01.md: C14: not run (no trusted sha)
dotfiles-T133-ci-efficiency-a01.md: OK
dotfiles-T133-ci-efficiency-a02.md: OK
dotfiles-T133-ci-efficiency-followup-a01.md: OK
dotfiles-T133-permission-guard-gate-a01.md: OK
dotfiles-T133-permission-guard-gate-a02.md: OK
dotfiles-T133-permission-guard-gate-a03.md: OK
dotfiles-T133-regime-ci-a01.md: OK
dotfiles-T133-result-precheck-a01.md: OK
dotfiles-T133-result-precheck-a02.md: OK
dotfiles-T133-result-precheck-followup-a01.md: OK
dotfiles-T133-task-generator-plan-check-a01.md: OK
dotfiles-T133-verdict-audit-pool-a01.md: OK
dotfiles-T133-verdict-audit-pool-a02.md: OK
dotfiles-T133-verdict-audit-pool-followup-a01.md: OK
dotfiles-T133-worker-cap-hookspath-a01.md: OK
dotfiles-T133-worker-cap-hookspath-a02.md: OK
dotfiles-T133-worker-cap-hookspath-followup-a01.md: OK
dotfiles-T133-worker-hooks-path-a01.md: OK
checker exit=0
$ shasum -a 256 <main checkout>/.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a01.md
e08bb0afe8d508f5327b0e199108ee1b74efdb5d4a2004faed93b1ca4d1f0c68  ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a01.md
$ uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root <main checkout> --premises-sha e08bb0afe8d508f5327b0e199108ee1b74efdb5d4a2004faed93b1ca4d1f0c68 <that file>
dotfiles-T133-task-generator-plan-check-a01.md: OK
exit=0
```

## Revise 1: CompactionDB memory

```
$ uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'T133 P1-12 revise 1: task-consistency-check.py C14 executes premise commands only for a file whose sha256 equals --premises-sha …'
3b0ef48d-bc91-4851-8d32-1051f6a5c076
exit=0
```

exec
/bin/zsh -lc "git show 8a09b9365932f23b09df8aa2385a93d0b3016a3e:tests/unit/test_plan_check.py | sed -n '149,170p' && git status --short && git diff --quiet b22a5580d0778e57a66d3f75c76e3c55b88701e1 -- . ':"'!.orchestration'"' && git rev-parse --git-common-dir" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 49ms:
    def test_invariants_reject_nonempty_quoted_oauth_token_assignments(self):
        # The audit of 9da0ed3 (P2, item 18): quoted and unquoted non-empty values are refused, an empty one is not, and
        # no diagnostic carries the value (built at run time).
        name, value = "ANTHROPIC_OAUTH_" + "TOKEN", "fixture-" + "x" * 8
        self.edit(
            PLANS + "024-execution.md",
            "# x\n",
            f'# x\n\n{name}="{value}"\n{name}=\'{value}\'\n{name}={value}\n{name}=""\n',
        )
        code, lines = self.plan_check("--invariants")
        self.assertEqual(
            (code, lines), (1, [f"invariant: 024-execution.md:{n} {name} with a value" for n in (3, 4, 5)])
        )
        self.assertNotIn(value, "\n".join(lines))


if __name__ == "__main__":
    unittest.main()
?? .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a01.md
?? .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a02.md
?? .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a02.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a01-audit-9da0ed3.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-audit-8a09b93.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-pr-feedback.json
~/Workspace/dotfiles/.git

**Evaluating read-only module checks**
**Confirming database read-only usage**
**Analyzing script verification and orchestration counts**
**Reviewing orchestrator security and trust model**
**Verifying task and mapping logic**
**Analyzing design task definition handling**
exec
/bin/zsh -lc "git show 9da0ed3fe67fd1f9267c56fcdcb7e5aaaaa9ffab:scripts/orchestrator/task-consistency-check.py | tail -n 65 && git show 8a09b9365932f23b09df8aa2385a93d0b3016a3e:.orchestration/dotfiles-T133-task-generator-plan-check-a02/task.md | sed -n '1,81p' && git log --format='%h %s' --no-merges b22a5580d0778e57a66d3f75c76e3c55b88701e1..8a09b9365932f23b09df8aa2385a93d0b3016a3e" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 63ms:
        tid_ok = re.fullmatch(r"[A-Za-z0-9][\w.-]*", load) and (root / f".orchestration/tasks/{load}.md").is_file()
        if form == "out-of-scope: " and not tid_ok:
            fails.append(f"C11 out-of-scope: {load[:60]} is not a task under .orchestration/tasks/")
        if form == "residual: " and len(load) < 20:
            fails.append(f"C11 residual: payload is shorter than 20 characters: {load}")
    for a in allowed:  # C12
        last = a.rsplit("/", 1)[-1]
        glob = re.search(r"[*?\[]", a) and not a.startswith(("tests/fixtures/", own_dir))
        if glob and (last.endswith(APPLIED) or a.startswith(("home/", "scripts/", ".githooks/", ".github/"))):
            for f in filter(None, git(root, "ls-files", "-z", "--", f":(glob){a}").stdout.split("\0")):
                if not any(re.search(re.escape(f) + r"(?=$|[ /\"'(),])", r.get("control") or "") for r in rows):
                    fails.append(f"C12 the glob {a} matches {f}, which no threat_table row names")
    premises = fm.get("premises") or []
    # C14 executes premise commands only for the orchestrator's dispatched text, the bytes whose sha256 the caller
    # passes (dispatch.sh: the TASK line's task_sha256); a branch copy at acceptance passes none, so nothing runs.
    if premises and hashlib.sha256(data).hexdigest() != premises_sha:
        fails.append(UNTRUSTED)
        premises = []
    for pre in premises:  # C14
        cmd, want = str(pre.get("command") or ""), str(pre.get("output") if pre.get("output") is not None else "")
        if re.search(r"\b(?:gh|curl)\b|https?://", cmd):
            fails.append(f"{SKIPPED}: {cmd[:60]}")
            continue
        got, code, err = rerun(cmd, root)
        # bash's own line, not exit 127: under pipefail `absent | grep -c` exits with grep's 1.
        if absent := re.search(r"^bash: line \d+: ([^\s:]+): command not found$", err, re.M):
            fails.append(f"{ABSENT} {absent.group(1)}: {cmd[:60]}")
            continue
        # Runs of whitespace collapse (BSD wc pads its counts; YAML's |- drops the final newline).
        if got is None or " ".join(got.split()) != " ".join(want.split()):
            fails.append(f"C14 premise output differs from its rerun: {cmd[:60]}")
    inv, design = fm.get("invariants"), dr.get("design")
    if isinstance(inv, dict) and design:  # C15; a design task carrying its own invariants names no design
        shown = git(root, "show", f"origin/main:{design}")
        canon = (front(shown.stdout).get("invariants") or {}) if shown.returncode == 0 else None
        for k, v in inv.items():
            if canon is None or canon.get(k) != v:
                fails.append(f"C15 invariant {k} is not byte-equal to {design} on origin/main")
    return fails


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=pathlib.Path, help="the repository (default: the first file's git toplevel)")
    parser.add_argument("--premises-sha", metavar="sha256", help="the dispatched file's sha256; C14 runs only for it")
    parser.add_argument("tasks", nargs="+", type=pathlib.Path, metavar="task.md")
    args = parser.parse_args()
    if args.root is None:
        top = git(args.tasks[0].parent, "rev-parse", "--show-toplevel")
        if top.returncode:
            parser.error(f"{args.tasks[0]} is not in a git checkout; pass --root")
        args.root = pathlib.Path(top.stdout.strip())
    rc = 0
    for p in args.tasks:
        fails = check(p, args.root, args.premises_sha)
        notes = [f for f in fails if f.startswith((SKIPPED, ABSENT, UNTRUSTED))]
        bad = [f for f in fails if f not in notes]
        print(f"{p.name}: {'FAIL' if bad else 'OK'}", *bad, sep="\n  ")
        print(*(f"{p.name}: {n}" for n in notes), sep="\n", file=sys.stderr, end="\n" if notes else "")
        rc |= bool(bad)
    return rc


if __name__ == "__main__":
    sys.exit(main())
---
format: 2
task_id: dotfiles-T133-task-generator-plan-check-a02
kind: code
security: true
allowed_files:
  - scripts/orchestrator/task-from-plan.py
  - scripts/orchestrator/plan-check.py
  - scripts/orchestrator/task-consistency-check.py
  - scripts/orchestrator/task-template.md
  - tests/unit/test_task_from_plan.py
  - tests/unit/test_plan_check.py
  - tests/unit/test_task_consistency_c11_c15.py
  - tests/unit/test_regime_ci.py
  - tests/unit/test_task_checkers.py
  - .orchestration/dotfiles-T133-task-generator-plan-check-a02/**
after: []
reset_of: [dotfiles-T133-task-generator-plan-check-a01]
threat_table:
  - control: "scripts/orchestrator/task-from-plan.py (generation from the committed plan group, bundled template, command outputs and scratch-worktree checks)"
    disposition: "residual: the generator executes the orchestrator's committed plan commands in the orchestrator's sandbox after the clean-plan check; the generator regressions and final-head security review assess this execution boundary."
  - control: "scripts/orchestrator/plan-check.py (form, concrete scope intersections, timestamped drift and forbidden patterns)"
    disposition: "closed: tests/unit/test_plan_check.py::test_plan_check_reports_each_form_drift_and_invariant_violation_once_and_passes_a_clean_plan"
  - control: "scripts/orchestrator/task-consistency-check.py (C11 to C15, concrete glob matches, trusted premise execution and assigned invariant ids); item 20: C10 literals as git grep -e operands and C6 paths confined to the checkout)"
    disposition: "residual: the checker executes premise commands only for bytes matching the caller's trusted SHA256; the dedicated regressions cover that gate, warnings, wildcard coverage and invariant completeness."
  - control: "scripts/orchestrator/task-template.md (the bundled task rows, Check defaults and Completion wording)"
    disposition: "closed: tests/unit/test_task_from_plan.py::test_generator_uses_the_bundled_template_without_task_records"
  - control: "tests/unit/test_task_from_plan.py (temporary committed plan groups, real local Git repositories and isolated command fixtures)"
    disposition: "residual: fixtures execute controlled commands in temporary repositories and verify output provenance, refusal before execution, generated scope and scratch-worktree cleanup."
  - control: "tests/unit/test_plan_check.py (temporary plan groups, concrete tree paths, acceptance events and a stub gh)"
    disposition: "residual: fixtures use temporary repositories and a stub gh placed first inside the uv invocation; no fixture contacts live GitHub."
  - control: "tests/unit/test_task_consistency_c11_c15.py (shape, wildcard, SHA, warning and invariant regressions)"
    disposition: "residual: temporary task files and repositories isolate premise side effects; explicit trusted hashes authorize only the fixture bytes under test."
  - control: "tests/unit/test_task_checkers.py (amendment 1's C4 fixture disposition and historical expected-set edits)"
    disposition: "residual: only the two amendment-1 edits remain against origin/main; report.md justifies every added historical check id and the audit compares the module's complete diff."
  - control: "tests/unit/test_regime_ci.py (amendment 1: the regime fixtures' threat-row dispositions gain the C13 grammar; no production change)"
    disposition: "closed: tests/unit/test_regime_ci.py::RegimeCiTest::test_regime_ci_checks_only_the_latest_copy_of_a_reset_of_lineage"
  - control: ".orchestration/dotfiles-T133-task-generator-plan-check-a02/** (the reset task's branch artifacts)"
    disposition: "residual: artifacts stay in this task's directory, distinguish historical observations from final-head results and identify commands, tested revisions and evidence hashes."
  - control: "the task-file copy on the branch (.orchestration/dotfiles-T133-task-generator-plan-check-a02/task.md) replaces the reset_of task's copy (.orchestration/dotfiles-T133-task-generator-plan-check-a01/task.md)"
    disposition: "residual: the worker's first push deletes the named predecessor copy and adds the byte-identical dispatched a02 text; the a02 copy's own SHA256 appears in TASK and RESULT and is compared at acceptance."
  - control: "the branch evidence records under .orchestration/dotfiles-T133-task-generator-plan-check-a02/ (report.md, validation.md, sandbox.md, learning.md, measure.md and authorized revise evidence)"
    disposition: "residual: records preserve command outputs, exits, production revisions and regression-source hashes; the final-head audit checks claims against the implementation, records and CI."
  - control: task metadata
    disposition: "residual: PyYAML reads the front matter and the consistency checker validates its cross-field rules before dispatch and at acceptance; the dispatched-file comparison covers subsequent changes."
  - control: metadata separators
    disposition: "residual: the first document separators bound the YAML front matter and the byte comparison covers the complete dispatched task copy."
  - control: in-process effects
    disposition: "residual: task-from-plan.py executes the plan's backticked commands, which are the orchestrator's own text, in the orchestrator's sandbox; it refuses execution when git status of the 024-* plan group is not clean and executes commands read from the committed revision. It writes the named task file and creates and removes a scratch worktree for Check commands. C14 executes a premise command only when --premises-sha equals the SHA256 of the same file bytes from which that command was parsed. plan-check writes no files."
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow changes; scripts use the existing uv and PyYAML invocation with python -I, premise reruns use bash with pipefail and the specified PATH, and plan-check uses read-only gh and git calls."
  - control: new or renamed scripts
    disposition: "residual: the inherited two new Python scripts and one new bundled Markdown template are the complete new production-file inventory; the audit checks the final inventory against allowed_files."
  - control: orchestrator effect merge
    disposition: "residual: the orchestrator merges through gh pr merge --squash --match-head-commit <audited head> after Orchestrator Playbook step 10; the worker has no merge assignment."
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch changes the head, so the required CI, feedback sweep, audit and security-review evidence bind the resulting final head before the gate."
  - control: orchestrator effect forced worker removal
    disposition: "residual: no forced removal is planned; any forced removal follows the existing dirty-worktree rule and records discarded uncommitted state in the acceptance record."
premises:
  - claim: none of the five new files exists on origin/main
    command: git ls-files scripts/orchestrator/task-from-plan.py scripts/orchestrator/plan-check.py tests/unit/test_task_from_plan.py tests/unit/test_plan_check.py tests/unit/test_task_consistency_c11_c15.py | wc -l
    output: |-
      0
  - claim: the checker documents eleven checks today (C1 to C10 and C7b), so C11 to C15 are additions at the end of its list
    command: /usr/bin/grep -c '^C[0-9]*b\? ' scripts/orchestrator/task-consistency-check.py
    output: |-
      11
  - claim: the plan 024 group is eleven files (ten Markdown documents and the progress TSV), the set plan-check reads
    command: /bin/ls .orchestration/plans/024-*.md .orchestration/plans/024-progress.tsv | wc -l
    output: |-
      11
  - claim: the todo table has fifteen P1 rows, the rows task-from-plan reads
    command: /usr/bin/grep -c '^| P1-' .orchestration/plans/024-todo.md
    output: |-
      15
  - claim: tests/unit/test_task_checkers.py is in flight in PR #413, so the new checks get their own test module
    command: git ls-files tests/unit/test_task_checkers.py | wc -l
    output: |-
      1
---
8a09b936 docs(orchestration): T133 task-generator-plan-check a02 amendment 1 CI-repair evidence (eb0b1c06)
eb0b1c06 test(regime-ci): the regime fixtures' threat-row dispositions take the C13 grammar (T133 task-generator-plan-check a02 amendment 1, CI repair)
3f12e603 docs(orchestration): T133 task-generator-plan-check a02 evidence: report, validation, measure, sandbox, learning and the worker review (6e07d291)
6e07d291 fix(orchestrator): per-event acceptance status, C15 on a design main cannot give, and no hanging premise (T133 task-generator-plan-check a02, the pre-push review of eb20d063)
eb20d063 fix(orchestrator): bundled task template, clean-plan gate, concrete scopes and timestamped drift (T133 task-generator-plan-check a02, the audit of 9da0ed3)
6da92853 docs(orchestration): T133 task-generator-plan-check a02 task copy replaces the a01 copy (INV-6 reset of PR #417)
37d969e1 docs(orchestration): T133 task-generator-plan-check a01 revise 1 evidence (538e60bd)
538e60bd fix(orchestrator): C14 executes premise commands only for the file whose sha256 --premises-sha names (T133 task-generator-plan-check a01 revise 1, Bot 4306960622)
ff4d25a8 docs(orchestration): T133 task-generator-plan-check a01 memory record and the branch, PR and CI outputs
5f770f22 docs(orchestration): T133 task-generator-plan-check a01 Bot round 1 evidence (b3c6b7ea)
b3c6b7ea fix(orchestrator): task-from-plan refuses a checkout without its records by name; plan-check F2 treats glob entries as overlapping what they match (T133 task-generator-plan-check a01, Bot round 1)
35c66022 docs(orchestration): T133 task-generator-plan-check a01 CI round 1 evidence (562e77f4)
562e77f4 test(orchestrator): put plan-check's stub gh first inside uv run, as on the macOS runner uv's base bin precedes PATH (T133 task-generator-plan-check a01)
dfce34d7 docs(orchestration): T133 task-generator-plan-check a01 evidence (d7332ebb)
d7332ebb test(orchestrator): the two expected-set edits of test_task_checkers.py for C11 to C15 (T133 task-generator-plan-check a01, amendment 1)
63a089e5 fix(orchestrator): C14 notes and warnings go to stderr, so stdout holds one line per finding (T133 task-generator-plan-check a01)
4c181fab fix(orchestrator): C14 collapses whitespace runs and warns on an absent tool (T133 task-generator-plan-check a01, amendment 1)
747602cd feat(orchestrator): task-from-plan.py, checker C11 to C15 and plan-check.py (T133 task-generator-plan-check a01)

**Reviewing test coverage and invariants**
**Structuring audit report summary**

I’m organizing the audit with a clear intro about scope and skipped items, then listing each finding with counts before the final verdict, including a brief risk note about what tests or snapshots were skipped to keep the user fully informed.
**Analyzing normalization and audit findings**
**Evaluating timestamp handling and input validation**
**Reviewing completion formatting and parsing**
**Validating table ID extraction and fixture rows**
exec
/bin/zsh -lc "python3 -B -c 'import sys, subprocess, pathlib, types, json
from unittest.mock import patch
sys.path.insert(0,\"~/.cache/uv/archive-v0/7OgnLaAJ8JgV819t\")
import yaml
head=\"8a09b9365932f23b09df8aa2385a93d0b3016a3e\"
def source(p): return subprocess.check_output([\"git\",\"show\",head+\":\"+p],text=True)
c=types.ModuleType(\"checker\");exec(compile(source(\"scripts/orchestrator/task-consistency-check.py\"),\"checker\",\"exec\"),c.__dict__)
root=pathlib.Path.cwd();tid=\"dotfiles-T9-demo-a01\";own=\".orchestration/\"+tid+\"/**\"
class P:
 stem=tid
 def __init__(self,fm):self.data=(\"---\\n\"+yaml.safe_dump(fm)+\"---\\n\").encode()
 def read_bytes(self):return self.data
for scope,match in [(\"../../outside/*.py\",\"\"),(\".claude/skills/**\",\".claude/skills/example/SKILL.md\")]:
 fm={\"task_id\":tid,\"kind\":\"code\",\"allowed_files\":[scope,own],\"threat_table\":[{\"control\":p,\"disposition\":\"residual: fixture compensating control\"} for p in [scope,own]+c.C7_NAMES]}
 def git(*a):return types.SimpleNamespace(returncode=0,stdout=match+\"\\0\" if \"ls-files\" in a else \"\",stderr=\"\")
 with patch.object(c,\"git\",git):print(\"complete task\",scope,c.check(P(fm),root))
pc=types.ModuleType(\"plan\");exec(compile(source(\"scripts/orchestrator/plan-check.py\"),\"plan\",\"exec\"),pc.__dict__)
files={
 \"024-todo.md\":[\"| id | purpose | work | completion |\",\"| --- | --- | --- | --- |\",\"| P1-1 | B1 purpose | (1) |\"],
 \"024-omp-cutover-and-corrective-order.md\":[],
 \"024-design-mechanism.md\":[\"| B1 | bottleneck |\"],
 \"024-design-quality.md\":[],
 \"024-checklists.md\":[\"| id | check |\",\"| --- | --- |\",\"| DoD1 | "'`make unit-test` |"]
}
with patch.object(pathlib.Path,"glob",lambda *a:[]),patch.object(pathlib.Path,"read_text",lambda *a:"id'"\\tdecision\\n\"):
 print(\"F1 missing completion cell\",pc.form(root,files))
ns=source(\"scripts/orchestrator/regime-ci.py\")
reg=types.ModuleType(\"regime\");exec(compile(ns,\"regime\",\"exec\"),reg.__dict__)
print(\"relative path rejected by regime\",reg.allowed(\"scripts/orchestrator/plan-check.py\",\"./scripts/orchestrator/plan-check.py\"))
print(\"C14 required stale-hash call missing:\", \"sha=sha\" not in source(\"tests/unit/test_task_consistency_c11_c15.py\").split(\"edited = self.task\",1)[1].split(\"def publish\",1)[0])
'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 193ms:
complete task ../../outside/*.py []
complete task .claude/skills/** []
F1 missing completion cell []
relative path rejected by regime False
C14 required stale-hash call missing: True

**Reviewing final implementation items**
**Evaluating audit evidence and reporting**
**Reviewing task invariants and violations**
**Confirming audit status and snapshot match**
codex
The remaining probes confirm defects in scope generation, threat-row coverage, and malformed-row detection. I’ve separated those from the orchestration record issues. The supplied snapshot shows successful checks for the requested head, and the actual diff stays within both caps; those checks do not cover the failures reproduced here.
exec
/bin/zsh -lc "python3 -B -c 'import subprocess,pathlib,json,collections; base=\"b22a5580d0778e57a66d3f75c76e3c55b88701e1\"; head=\"8a09b9365932f23b09df8aa2385a93d0b3016a3e\"; totals=collections.Counter(); rows=subprocess.check_output([\"git\",\"diff\",\"--numstat\",base,head],text=True).splitlines(); [(totals.update({\"evidence\" if p.startswith(\".orchestration/\") else \"tests\" if p.startswith(\"tests/\") else \"production\":int(a)+int(d)})) for a,d,p in (r.split(\"\\t\",2) for r in rows)]; print(\"caps\",dict(totals)); p=pathlib.Path(\".orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a02.md\"); t=p.read_text(); d=json.loads(t.split(\"---\",2)[1]); print(\"ledger classes\",dict(collections.Counter(x[\"class\"] for x in d[\"ledger\"]))); print(\"pasted search lines\",[l for l in t.splitlines() if l.startswith(\"search:\")]); print(\"searches field\",d[\"searches\"]); fb=json.loads(pathlib.Path(\".orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-pr-feedback.json\").read_text()); print(\"snapshot\",fb[\"head_sha\"],fb[\"generated_at\"],\"checks\",collections.Counter(c[\"conclusion\"] for c in fb[\"checks\"])); print(\"tracked worktree diff\",subprocess.run([\"git\",\"diff\",\"--quiet\",\"HEAD\"],check=False).returncode)'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 90ms:
caps {'evidence': 1787, 'production': 659, 'tests': 673}
ledger classes {'evidence-integrity': 1, 'threat-row-stale': 1, 'replan-not-patch': 1, 'dispatch-wiring': 1, 'spec-gap': 1, 'glob-classification': 1, 'glob-intersection': 1, 'substring-selection': 1, 'glob-filter': 1, 'parser-gap': 4, 'regex-gap': 1, 'records-form': 1, 'trust-boundary-pr-input': 1, 'missing-input-crash': 1, 'string-form-comparison': 1}
pasted search lines []
searches field [{'class': 'parser-gap', 'records': []}]
snapshot 8a09b9365932f23b09df8aa2385a93d0b3016a3e 2026-10-19T04:20:02+00:00 checks Counter({'success': 10})
tracked worktree diff 0

**Summarizing rationale in structured bullet points**
**Analyzing path validation and testing details**

I’m sorting through how path checking handles allowed and outside paths, realizing skipped outside paths aren’t opened and thus don’t count as findings. I’m also noting a discrepancy in test hash values signaling output mismatches, showing incomplete evidence rather than a security bug but still relevant since the user requested thoroughness.
**Clarifying tool recognition and path handling**
**Reviewing script path validation and audit reporting**

I’m working through how to handle script paths that miss canonical git grep hits but are still allowed, noting directory prefix rules and a known checker bug that flags certain paths incorrectly. I plan to include a clear audit summary referencing the specific PR and commit hash to explain these findings along with the final verdict.
codex
Audited [PR #417](https://github.com/mryfmo/dotfiles/pull/417) at `8a09b936`.

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
Verdict: incorrect
hook: Stop
hook: Stop Completed
tokens used
184,433
Audited [PR #417](https://github.com/mryfmo/dotfiles/pull/417) at `8a09b936`.

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
Verdict: incorrect
