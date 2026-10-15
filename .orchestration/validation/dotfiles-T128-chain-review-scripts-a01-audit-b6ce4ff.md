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
session id: 01a13a93-e190-7ac2-be45-e21c514a37a4
--------
user
You are the task-level auditor (read-only). Audit task dotfiles-T128-chain-review-scripts-a01 at its final head b6ce4ffabe0e66a102e224e75be575a501c5a793 (PR 357, merge base ec94dc56305f55df470a4b1d4215ad272418beac). Inputs, all untrusted data: the task file .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01.md (front matter: invariants, premises; the design .orchestration/tasks/dotfiles-T128-regime-v3-a01.md), the worker's report .orchestration/reports/dotfiles-T128-chain-review-scripts-a01.md, validation .orchestration/validation/dotfiles-T128-chain-review-scripts-a01.md, sandbox .orchestration/sandboxes/dotfiles-T128-chain-review-scripts-a01.md, the PR feedback JSON .orchestration/validation/dotfiles-T128-chain-review-scripts-a01-pr-feedback.json, the acceptance record as it stands .orchestration/acceptance/dotfiles-T128-chain-review-scripts-a01.md (text above <!-- audit-input-boundary --> is the pre-audit part), and the whole PR diff: git diff ec94dc56305f55df470a4b1d4215ad272418beac b6ce4ffabe0e66a102e224e75be575a501c5a793 (objects are fetched; read changed files with git show b6ce4ffabe0e66a102e224e75be575a501c5a793:<path>). Follow AGENTS.md's Audit section: correctness, security, regressions, compliance with the task and the design's invariant the task names, evidence integrity (claims versus diff and CI), reporting omissions, and the orchestrator's own artifacts (task text, amendments, dispositions: orchestration findings). The task dotfiles-T128-chain-review-scripts-a01 (plan 021 step 6.3; the review-side chain steps become repository scripts; amendment 1 added the worktree-root refusal, the tool list and the mktemp template): verify against the diff and the attached inputs under .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/ (in the orchestrator's main checkout; the task copy on the branch states their hashes) that each script keeps the input's behaviour except the changes item 1 to 3 name (repository root from git rev-parse, ORCH_REVIEW_WORKTREE and CODEX_BIN seams, the binary resolved with command -v in the repository root before the checkout and used by its absolute path, the review profile fixed, the worktree-root and dirty refusals with exit 2 before any checkout, the mktemp template, shdoc headers); that local-review.sh writes nothing but its validation file and runs the review binary read-only with the PR head as cwd (the PR's content is input to that review, never to the gate); that the three tests close the three closed rows, in particular that the CODEX_BIN-unset case proves the resolution happened before the checkout (the decoy in the head commit never runs) and that the non-worktree-root case leaves the main working tree's HEAD unmoved; that nothing outside allowed_files changed. Say whether any input the scripts read (the head, the task name, the listing, the environment) can make them run anything other than the named commands or write anything other than the named files. Rate every finding with confidence and the exact line. Report each finding as '[P0-P3] confidence dimension file:line rationale' (dimension in specification, implementation, evidence, orchestration, conformance), then one line per task invariant 'INV-n: holds|violated <file:line>', then 'Orchestration findings: <count>', and end your final message with exactly one concluding line 'Verdict: correct', 'Verdict: incorrect' or 'Verdict: blocked'. A finding-free audit still records one justified approval. Modify nothing.
warning: loading hooks from both ~/.codex/hooks.json and ~/.codex/config.toml; prefer a single representation for this layer
hook: SessionStart
hook: SessionStart
hook: SessionStart Completed
hook: SessionStart Completed
hook: UserPromptSubmit
hook: UserPromptSubmit Completed
codex
🤖 I read the AGENTS.md for mryfmo/dotfiles.
Ponytail・agmsg-orchestration・gh-first-workflow の該当手順を読み、指定 head の差分、入力スクリプト、CI と証跡を読み取り専用で照合します。
exec
/bin/zsh -lc 'cat ~/.codex/plugins/cache/ponytail/ponytail/5.2.0/skills/ponytail/SKILL.md' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc 'cat ~/.agents/skills/agmsg-orchestration/SKILL.md' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc 'git status --short && git rev-parse HEAD && git worktree list --porcelain && git diff --stat ec94dc56305f55df470a4b1d4215ad272418beac b6ce4ffabe0e66a102e224e75be575a501c5a793' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc 'cat ~/.agents/skills/gh-first-workflow/SKILL.md' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 128ms:
---
name: ponytail
description: >
  Lazy senior dev mode: the smallest change that fully solves the task, and a
  reply a busy human understands in one read. Use on any coding task (writing,
  fixing, refactoring, reviewing, choosing dependencies) and when the user says
  "ponytail", "be lazy", "simplest solution", "yagni", or complains about
  over-engineering or bloat. Levels: lite, full (default), ultra.
argument-hint: "[lite|full|ultra]"
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

 succeeded in 198ms:
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
- A Claude session started in the repository root outside Herdr (a plain shell, mosh/ssh, or `claude -p`) is a pane-less orchestrator: nothing seats a worker automatically, and the SessionStart `herdr-agents --attach` hook prints a summary line naming that state, the on-demand commands, and any seated worker, followed in a regime repository by the `agmsg-orchestration:` directive line. Bring the regime up on demand: claim the seat outside the sandbox with the composite instance id, `actas-claim.sh <repo> claude-code <name> <session_id>.<claude pid>` (a claim from sandboxed Bash writes the bare session id and turn delivery then skips silently; see the seat-lock bullet below); seat the worker with `herdr-agents --add-worker <worktree>` (it derives `HERDR_SOCKET_PATH` from the default Herdr server socket `~/.config/herdr/herdr.sock`, the path the Claude sandbox allowlists, before creating anything, accepts a claude worker's workspace-trust dialog during spawn's readiness wait, and takes `--ready-timeout <seconds>`); confirm the worker's placement from its `run/spawn.*` placement record itself (the `herdr:<socket>:<pane>` row that upstream `agmsg_spawn_path` resolves) and the `linkage=` line `--add-worker` prints, never from `team.sh <team> --json`, which observes Codex members by reading their pane; treat the `linkage=` line `--add-worker` prints as the `AGMSG-PING` evidence, and on `pong=no` or `linkage=unreached` wake again with `agmsg-dispatch <team> <orchestrator> <worker> <pane> 'AGMSG-PING v1 task_id=<id> reason=<reason>'` and verify the PING's `read_at` (`poke.sh` only for a viewed workspace); and dispatch no AGMSG-TASK before its `AGMSG-PONG` arrives. Without a managed workspace the auditor runs headless, in the form the task-level audit bullet below names. A sandboxed pane-less session cannot keep a Monitor watch (the sandbox's pid namespace), so RESULTs arrive by turn delivery.
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
- On activation, check `delivery.sh status <type> <repo>`. This repo runs Claude Code seats on `both` (monitor's push plus turn's pull), one notch more redundant than upstream's Claude Code default `monitor`, since an unattended worker pane has no one to notice a Monitor watch that silently failed to re-arm; Codex seats run on `turn` (see the next bullet). If weaker than that, run `delivery.sh set both claude-code <repo>` (or `delivery.sh set turn codex <repo>` for a Codex identity), start the SessionStart-provided `watch.sh <session_id> <repo> <type>` as a persistent in-session monitor, and claim exclusivity with `actas-claim.sh <project> <type> <name> <session_id>`. A Claude worker seated by `--add-worker` gets its Monitor watch through its actas boot; when it is seated in its own workspace (no managed workspace exists), `herdr-agents` also sets `AGMSG_CC_MONITOR_KEEP_ALIVE=1` in that workspace's environment so the watch re-arms unconditionally on expiry, not only when the expired watch delivered something (upstream's default).
- `herdr-agents --bootstrap-agmsg` (and full or attach mode) sets the main checkout's orchestrator hooks, Claude Code on `both`; a worker seat gets its own hooks from `herdr-agents --add-worker`, Codex on `turn` and Claude Code on `both`, so the Stop/SessionStart hook in the worktree's tree-scoped, gitignored `.codex/hooks.json` or `.claude/settings.local.json` delivers inbox messages. Codex deliberately stays on `turn` instead of upstream's shim-based `monitor` bridge (the upstream README names `monitor` as the Codex default in one place and `turn` in its delivery table): as of agmsg v1.5.0 that bridge has open reliability defects an unattended resident worker cannot risk — no teardown on session end (upstream #149), a mode switch that does not start the bridge in a live session (#151), and a bridge that restarts forever while its status reports it alive (#1236), all still open. Storage resolution is env-only: keep `AGMSG_STORAGE_PATH` unset for same-repository default-store workers, or set it to the regime's dedicated store for separate cross-project regimes; a wrong or stray value silently reroutes the worker to another database. Pane nudges are only generic wakes; message content always travels over agmsg.
- Worker panes run in their worktree: `herdr-agents --add-worker [<worktree>]` seats the worker in that worktree (default the manifest's `worker_worktree`, created from `origin/main` when missing), registers its identity there with `AGMSG_RESOLVE_PROJECT=0`, sets delivery on that path, and starts it through upstream `spawn.sh`, so turn delivery reaches the worker directly through the worktree's Stop hook and its Monitor watch comes from the actas boot (upstream `session-start.sh` skips sessions under `.claude/worktrees/`, #367). The interim worker inbox discipline (running `~/.agents/skills/agmsg/scripts/inbox.sh <team> <identity>` at each milestone: task start, push, CI green, before RESULT, after any PONG) is retired for a worktree-seated worker; it applies only to a worker still acting under a worktree-registered identity from a main-path pane, until `herdr-agents --remove-worker` and `--add-worker` re-seat it.
- A codex worker in a nested worktree gets `<common>/objects`, `<common>/refs`, `<common>/logs` and `<common>/worktrees/<name>` (`<common>` from `git -C <worktree> rev-parse --git-common-dir`) as writable roots from `herdr-agents` (`-c sandbox_workspace_write.writable_roots`, with the configured agmsg roots kept first), so local git operations need no escalation. The common dir itself, `config`, `hooks`, `info`, `HEAD` and `packed-refs` stay read-only. The worker seat runs with `--ask-for-approval never` and `sandbox_workspace_write.network_access=true`, so a GitHub fetch, push or `gh` call works inside the sandbox and the worker never prompts: there is no escalation for a worker, and an action outside the sandbox or forbidden by the execpolicy fails and is reported as `AGMSG-PONG v1 status=blocked`. The `sandbox_workspace_write.network_access` switch is a boolean, so the worker reaches any host (no domain allowlist is configured, unlike Claude Code's `allowedDomains`), and the permgate PermissionRequest hook never fires for the worker seat; it stays live for interactive Codex sessions, which keep on-request approvals and no sandbox network.
- The orchestrator's actas seat lock must hold the composite instance id `<sid>.<pid>`; check it with `cat ~/.agents/skills/agmsg/run/actas.<team>__<name>.session`. `actas-claim.sh` run from sandboxed Bash cannot see the claude pid (the Linux sandbox has its own pid namespace), writes the bare session id, and the Stop-hook inbox check then skips delivery silently (`other:<sid>`). `herdr-agents` therefore claims the seat outside the sandbox when it starts the orchestrator pane and from its SessionStart `--attach` hook, printing `seat_claim=ok owner=<sid>.<pid>` (or `seat_claim=unresolved`, never a bare-id lock), and `make doctor` warns on a bare-id orchestrator lock while a claude session runs in the repository. A `watch.sh` Monitor cannot run under that sandbox either: it sees the claude pid as dead and exits "no longer alive". Until upstream offers a liveness override, turn delivery is the working path, and an idle orchestrator is woken by the worker's `agmsg-dispatch` to the orchestrator pane.
- Reserve store separation for concurrent regimes in different projects, such as flue-pi. When using it, set the same `AGMSG_STORAGE_PATH` in the worker pane and on orchestrator send/watch/history calls or tasks, results, and pongs become unreachable. Same-repository parallel workers always share the default store.

## Live verification

- Accept changes to live desktop behavior — herdr layout/session, pane lifecycle, or delivery hooks — only after live end-to-end verification covers both a fresh session and a persisted-session restore; unit and static tests alone are insufficient.
- Launch orchestrator-driven E2E test-subject panes with express-profile arguments from `~/.agents/model-profiles.env` (`MODEL_PROFILE_EXPRESS_CLAUDE_ARGS` / `MODEL_PROFILE_EXPRESS_CODEX_ARGS`), never ad-hoc `--model` flags.

## Review and integration invariants

- Review every RESULT adversarially across correctness, regressions, security, and reporting omissions: try to refute it, independently re-derive findings, and never treat sampled spot checks as full verification.
- Acceptance review, adversarial RESULT review, and review-profile work remain orchestrator-side; never delegate them to a worker, and keep `make require-crit-review` as the final integration step. Revisit only if worker-side model capability surpasses the orchestrator tier.
- A design review runs in paired rounds. Both reviewers, a fresh Claude context on the `review` profile and a Codex read-only run under a `codex-review` identity, get the same design hash at the same time. The orchestrator revises once per pair of results and opens no round while one is still open. The third pair is the last: on its accept the design is frozen at the hash the pair last accepted, the third pair's own, and whatever is still open at that hash becomes a residual list that is worker input; on its revise or reject nothing is frozen and the design goes back to a context other than its author, never to a fourth pair; a revision after the third pair is not made, and any later change to a hashed key is a new pair (INV-7). The review judges the invariants, threat model, trust anchors and premises for contradiction and enforceability, never implementation detail.
- A task-file review is one round with a fixed stop condition: no contradiction with the design, the premises hold, `allowed_files` covers every touch point that grep finds, and one invariant check (for a task that carries an `invariants` key: the task id maps to its `implementing_tasks` entry, the invariant ids match, and each invariant's sentence equals the design's byte-for-byte, the design read from main (INV-2), checked by hand in the review until a checker lands; a task without the key needs no entry). Anything finer belongs to the worker and the implementation PR.
- A boundary PR synchronizes records at a boundary. It carries no task draft under review. A design not yet on `main` lands through a merged boundary PR before its implementing TASK is dispatched (INV-2), and any merged boundary that carries the design meets that precondition.
- A task that touches a trust boundary (anything the design tier lists, CI that decides a required check, code that executes PR-controlled input) carries a `threat_table` in its front matter: one `{control, disposition}` row per thing the PR or the orchestrator controls (the tree and its tests, task.md, workflow files, interpreter and environment files, in-process effects, new or renamed scripts, metadata separators). The row unit is one row per `allowed_files` entry, one row per listed control that is not a path (task metadata, workflow and interpreter or environment inputs, in-process effects, new or renamed scripts, metadata separators), carried by the declared test module's row where that is where the control acts, and one row per orchestrator effect from the fixed list (forced removal, merge, update-branch); under a wildcard `allowed_files` entry whose files are executed or applied (scripts, workflows, hooks, settings, the rules seats follow), one row per concrete file the PR changes; a wildcard over test fixtures or other data files keeps one row; C4 of the task-consistency check (plan 007 T704) verifies the path half once it lands, and the task-file review checks it by hand until then. A disposition takes one of three forms: `closed: tests/<file>::<name>`, the test that closes the row; `residual: <sentence>`, the compensating control; `out-of-scope: <task id>`, the task that owns the row. Shape is `schemas/task.json`'s (wave V1): a `closed` selector names a test present in the PR tree at acceptance and in the schema's validation of the PR, an `out-of-scope` owner is a task id in the design's `implementing_tasks`, a `residual` payload is a sentence of at least 20 characters (the gate's minimum for a reason). Until `schemas/task.json` lands in wave V1, the task-file review checks the three shape rules by hand. For a `closed` row it checks the selector's form only, since the test does not exist before implementation. Substance is the reviewers': the task-file review, the Bot and the auditor judge each row against the diff. The table is the task's completion condition: a missing row is added once, counted as an amendment, never fixed finding by finding.
- Before every acceptance action (revise, accept, merge) the orchestrator runs `scripts/regime-counters.sh <task id>` and pastes its output into the acceptance record. S2 is decided from INV-6's counts: each component the script prints is read from its output, and for each component it prints as `unknown` the record pastes the command and output that read the source INV-6 names for that component, or, while that source has no entry for the task, says so and pastes the reading of the interim record the orchestrator used in its place. S1 (plan 006: the same finding class three times on one artifact, from any reviewer) is decided from the record's finding-class table, which gives a class to every finding the PR-feedback sweep lists, whatever its disposition, and to every task-level audit finding; three rows of one class stop the artifact.
- A change to a rule sentence requested of a worker travels as a task amendment (hashed, checked by the task-consistency check C1 to C6 once plan 007 T704 lands it and by hand until then, confirmed by the review seat), never as a PONG answer.
- When a finding class reaches three on one artifact (the record's ledger) or `scripts/regime-counters.sh` prints an S1 candidate, the next acceptance action is the records search for that class, pasted into the record as the line `search: <class> -> <the matching mistake records or none>`, and the matching correction is applied when its mechanism is landed, or landed first when it is pending, mechanism by mechanism, before any dispatch; a class is a slug of `[a-z0-9-]` assigned at disposition time, never text taken from a review title. Once plan 007 T718 lands, `scripts/orchestrator/three-repeat.sh <class>` validates the slug, runs the records search and the CompactionDB search without a shell and prints the line; until then the orchestrator runs them by hand with a validated slug. Once `dotfiles-T128-gate-evidence-a02` lands, the gate refuses the action without the line; until then the orchestrator refuses it by rule. Every `not-applicable` disposition carries `; evidence=<command>` with the output pasted in the record.
- At regime or session boundaries, write pending acceptance records, then mechanically commit every `.orchestration` file so no untracked tail remains. The sync needs no per-task artifact set: its audit record is the commit, whose message lists covered task IDs, plus agmsg ACCEPTANCE history. `make check-regime-boundary` reports a canonical clone with unmerged entries, a stash, or a difference from `origin/main` under `home/`, `install/` or `scripts/` as a sign that something ran where it must not. Lessons from a session are codified in this repository (a rule, the skill, or a check) through a task; Claude auto-memory is not a durable store for regime procedure. The canonical clone is pull and apply only and untouched by any seat: no edits, no apply from a dirty tree (the run_before guard refuses it), and one orchestrator identity per repository, seated at the working clone.
- Stop checklist, at every regime or session boundary and in this order: write pending acceptance records; mask every `.orchestration` file the boundary commit adds or changes with `uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets <files>`, which also normalises home directories to `~`; run `make validate-agent-assets` (real exit status); make the `.orchestration` boundary commit with zero untracked tail on a fresh `orchestration/boundary-<YYYY-MM-DD>` branch from `origin/main` and merge its PR with `gh pr merge --squash --auto`; remove every worker with `herdr-agents --remove-worker <worktree>` (despawn, delivery off, leave, tab or workspace closed); check stale identities with `identities.sh <path> <type>` (exactly one name at the main checkout, none at a worker worktree); close Crit review servers (`pgrep -f 'crit _serve'` must be empty); in a CompactionDB-opted-in project, review `uv run --no-project .claude/hooks/contextdb_cli.py memory candidates --limit 20` and promote each candidate worth keeping with `uv run --no-project .claude/hooks/contextdb_cli.py memory promote <id> --scope project`, or leave it. The orchestrator workspace itself stays resident for the next session unless the operator restarts the machine. `make check-regime-boundary` (`scripts/check-regime-boundary.sh`) checks this list and the orchestrator seat lock, one line per violation.
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
  - The orchestrator dispositions every `[P0-P3]` finding in the acceptance record, whatever the verdict: exactly one `audit-finding: <n> …` line per finding, numbered 1..N in the audit's order of `[P0-P3]` lines. The audit's finding lines may be bulleted; a disposition line may be indented but never starts with a list marker, or the gate skips it. `fixed:<sha>` needs a fresh audit of that sha; otherwise `not-applicable:<reason of at least 20 characters>`. Deferral ("later", a follow-up task, a stopgap or a suppression) is not a disposition. The gate enforces these lines only for an `incorrect` verdict (T68), but a finding under `Verdict: correct` is dispositioned all the same.
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

A RESULT whose third Bot round was left unfixed carries `bot_rounds=3` and lists its open thread ids (Worker Playbook step 15). A `status=revise` ACCEPTANCE carries `previous_head=<the RESULT head being revised>` and one failing-test selector per finding (`check=tests/<file>::<name>`); the worker records both in `.orchestration/<task id>/revise.yaml`, beside the task.md copy.

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
6. Send `AGMSG-TASK v1` with the exact artifact paths and `done_signal=AGMSG-RESULT`. Pass every `send.sh`/`poke.sh` body with `--body-file <path>` (both take it in agmsg v1.5.0), never as a positional argument: a positional `<text>` passes through the caller's own shell first, where a backtick or `$( )` in the body silently executes and vanishes from what arrives (upstream #378). `agmsg-dispatch` is the one exception and takes a single-line, shell-safe positional message. Pick the path by how the recipient is seated, never by inferring pane or agent status: a worker in a `herdr-agents` pane gets `agmsg-dispatch <team> <from> <to> <pane_id> "<message>"` (send, generic wake, `read_at` wait; single-line shell-safe text only), the sanctioned wake path until worker seating writes placement records at launch, because `poke.sh` exits 1 with "no placement record" for a hand-joined member, and a herdr-agents worker gets a record only once it acts from its own pane (upstream `send.sh`/`inbox.sh` record the acting pane, #1109); a spawn-seated member (placement record `run/spawn.*`; `team.sh <team> --json` shows its pane) gets `poke.sh <team> <name> --body-file <path> [--retries N --retry-delay SECONDS --backoff fixed|exponential]`, which types and submits in one call and refuses to type over an in-progress draft (#1321/#1322); a pane-less member gets `send.sh <team> <from> <to> --body-file <path>` and its own delivery mode. Verify delivery via the messages.db `read_at` column. `poke.sh` exit codes: 10 = terminal unreachable, 12 = pane gone or no live agent, 14/15 = refused to type over a changing or unlocatable input box, 13 = the driver has no poke path for this pane (for example a `plain` terminal); where poke.sh's narrow agmsg-message fallback succeeds it exits 0, so 13 means nothing was delivered, and the printed reason names the native channel, asks the caller to claim its own identity first, or reports that the fallback failed. Never retry a 13 as `send.sh` yourself: that overrides the driver's considered refusal and can double-deliver. Seating case: a worker in an unviewed or headless Herdr workspace (no client attached, a small pane rect such as 18x41) makes `poke.sh` exit 14/15 from its TUI input locator; that is a locator refusal, not evidence about the worker's state, so wake it with `agmsg-dispatch` and verify `read_at`. Every dispatch (TASK, ACCEPTANCE, PING) is recorded in the current acceptance record under a `dispatch:` key as the bus line with its read marker; a seat is reported as working only from such a line, and after a context compaction the open TASK list is re-derived from a bus read that is refused when it reaches its limit (`bus-read.sh` exits when the history reaches `BUS_READ_LIMIT`; the orchestrator raises the limit and reads again), never from a default-limited one and never from a read whose truncation went unnoticed. A seated worker idle for 20 minutes since its latest bus event for the task while a dispatchable task exists (INV-10's idle figure; its 30 minutes is the first-push deadline) gets a bus read, then a PING; a longer silent wait is never the answer. `scripts/orchestrator/dispatch.sh` writes the line and `scripts/orchestrator/bus-read.sh` performs the read and prints the minutes since each open task's latest event (both on main since a03c1daa, plan 007 T718); the orchestrator applies the 20-minute figure to the minutes the script prints (the script's own silence flag still uses 30 minutes, a recorded residual of the tools lineage).
7. Track `max_turns`. Use `AGMSG-PING` for liveness if a worker stalls.
8. On `AGMSG-RESULT`, read the task file and every referenced artifact before deciding.
9. For a RESULT carrying `effects`, verify that every declared effect has the report's stated reverse mapping before acceptance; record any irreversible effect in the acceptance note.
10. For a RESULT that carries a pull request, integrate in this order. This is the single procedure that the PR integration rule, `AGENTS.md`, the README and the gh-first-workflow skill cite. A `gh pr update-branch` moves the head, so steps 1 to 4 run again on the new head. After an update-branch the orchestrator runs it, the order is CI on the new head, then the sweep, then the audit; an audit started before CI finishes sees incomplete evidence and returns an evidence-only `incorrect`. Select a checkout with git -C <absolute path>, never with cd, which the sandboxed Bash may not honour. After moving the review worktree to the audited head, verify git -C <review> rev-parse HEAD equals that head and git -C <main> symbolic-ref --short HEAD prints main before the audit and the gate.
    1. Sweep the final head's feedback with `scripts/pr-feedback.py <pr> --json .orchestration/validation/<task>-pr-feedback.json` and give every item a `fixed:<commit>` or `not-applicable:<reason>` disposition, leaving none on `failure` or `warning` annotations. Optionally request `@coderabbitai full review` on the final head first; when a CodeRabbit review exists it is swept like any other item, and the gate does not require a bot review. An `open:<thread id>` item from a worker's third Bot round is a sweep item like any other: it becomes `fixed:<sha>` through a revise round that carries its `check=` (a round that counts toward INV-6 like any other), or `not-applicable:<reason>` with a pasted refutation; until one of those exists the PR is not merged, never with the thread open.
    2. Run the task-level audit of that head in the pair or headless form of the task-level audit bullet. It exits nonzero for every verdict other than `correct`. An exit with `Audit verdict: incorrect` is not a failed step: continue to step 3 and disposition its findings. A `blocked` or missing verdict means re-running the audit.
    3. Write the acceptance record, summarising the dispositions, with an `audit-finding:` line for every audit finding whatever the verdict (the gate needs them, through `AUDIT_DISPOSITIONS`, when it is `incorrect`).
    4. Run the gate: `AUDIT_EVIDENCE=<audit> [AUDIT_DISPOSITIONS=<acceptance record>] AGENT_REVIEWED=1 REVIEW_EVIDENCE=<receipt> ACCEPTANCE_EVIDENCE=<acceptance record> BASE=origin/main PR_FEEDBACK_EVIDENCE=<json> make require-crit-review`.
       - A `review` sweep item whose body carries a `P0`–`P3` badge is a finding with its own `fixed:<commit>` or `not-applicable:<reason>` disposition, never a container for its inline threads.
       - The sweep covers issue comments, reviews, inline review comments with thread resolution, non-passing check runs, check-run annotations at every level (`notice`, `warning`, `failure`), and commit statuses. A `failure` marked `not-applicable` needs a concrete reason of at least 20 characters.
       - A CodeRabbit full review is optional, at most once on the final head: the plan allows one review per hour and every review event spends one (docs.coderabbit.ai/management/rate-limits).
       - The feedback JSON may be masked with `uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets`, which masks its keys and string values; the gate identifies an item by its source, url, level, path, line and body, and accepts a body or path that is verbatim or exactly that masked form.
       - The gate rejects evidence outside `.orchestration/validation/` or without the `-pr-feedback.json` suffix. It binds `BASE` to the PR's GitHub base before running the collector from that authenticated SHA: an older base must be outside HEAD's first-parent chain, an advanced base must preserve the merge-base with the PR head, and PR branch commits (including `HEAD`) cannot substitute for the base. Evidence must match the local GitHub repository independently of `GH_REPO`, and `fixed:` commits must be in the authenticated GitHub base-to-head range whatever `BASE` is selected.
       - `AUDIT_EVIDENCE` must be the task-level file `.orchestration/validation/<task>-audit-<sha7>.md` (the same `<task>` as the feedback JSON); a per-commit `audit-<sha>.md` is rejected. Its verdict comes only from the non-empty `<file>.last.md` and must be `correct`, or `incorrect` with `AUDIT_DISPOSITIONS`. PRs that change only `.orchestration/` files need no audit.
       - A boundary PR (`orchestration/boundary-<date>[-n]`, `.orchestration` files only) skips the gate, the sweep JSON and the audit (with `BASE` set the gate would demand `PR_FEEDBACK_EVIDENCE`); each Bot thread on it still gets a disposition reply and is resolved, and the next boundary commit message names the PR.
    5. After the required checks pass and the threads are resolved, merge with `gh pr merge <pr> --squash --match-head-commit <audited head sha>`, so a newer head can never be merged on the evidence of the audited one. Every seat acts as the machine's one GitHub account, so no approval is required or possible. Who merges is decided by the integration gate and by native denial of merge commands in Codex seats; `herdr-agents` writes the Claude worker deny rules (`Bash(gh pr merge:*)`, `Bash(gh api -X PUT:*)`, `Bash(gh api --method PUT:*)`, `Bash(gh api graphql:*)`) into the worker worktree's `.claude/settings.local.json`, where [deny rules take precedence over allow rules and cover nested subcommands in every permission mode](https://code.claude.com/docs/en/permissions), but a method flag after the path escapes these prefix rules, so the integration gate remains the authority.
    6. Send `AGMSG-ACCEPTANCE` (step 11).
11. Send `AGMSG-ACCEPTANCE v1 status=accepted` when done, or `status=revise` with a narrow `reason` and `next_action` when more work is required.

## Worker Playbook

1. Read the full `AGMSG-TASK v1` message.
2. Switch to the `repo` and read `task_file` before editing or running validations. Create the task branch without touching the shared `.git/config`, which is read-only for a Codex seat by design (T64 writable roots): `git switch -c <branch> --no-track origin/main`, push with `git push origin <branch>` (no `-u`), and open the PR as a draft with `gh pr create --draft --head <branch>`. Commit inside the sandbox, with `git -c commit.gpgsign=false` when the signing key is unreadable there; for a Claude seat only the push leaves the sandbox, and a Codex seat pushes from inside it (step 4). A Claude seat's sandbox can leave the same failed write behind, so it uses the same commands. A leftover `.git/config.lock` from a failed attempt is removed by the orchestrator. Remove a scratch worktree (for example one that proves a test fails on `origin/main`) with `git worktree remove <path>` only; never run `git worktree prune` from a sandboxed seat, because other worktrees' paths look missing inside the sandbox and prune then targets their admin directories in the shared `.git/worktrees`.
3. Treat `allowed_files` as the edit boundary. If it says to see the task file, read that section and follow it exactly.
4. Do not perform any `forbidden_actions`. Complete every command inside the sandbox and allowlist; never escalate an action outside that boundary for approval. Fail it instead, send `AGMSG-PONG v1 status=blocked` with the exact command and the boundary it crosses, and wait for the orchestrator to re-task. Agent-to-agent permission approval is forbidden: only the human operator answers a permission prompt. A Claude Code auto-mode classifier denial (for example Self-Modification) is such a boundary: stop without a diff, send `AGMSG-PONG v1 status=blocked` naming the classifier reason, and never pursue the same outcome through another tool. Fetch and fast-forward inside the sandbox; a public remote needs no credential. On Linux, `gh` backed by the host keyring answers HTTP 401 inside the sandbox, because AF_UNIX socket creation is denied and `allowUnixSockets` cannot grant a path. So a Claude seat runs three commands outside the sandbox through the permission gate: `gh`, `git push`, and an authenticated `git fetch` (a private HTTPS remote, whose credential helper is `gh`). Look up a VERIFY item's external reference (upstream documentation, release notes, an API schema) with the WebFetch tool, not Bash `curl`. Three documented cases run outside the sandbox too: the task's main-checkout CompactionDB `memory add`, through the permission gate because that state directory is read-only from a worktree sandbox; writing the task's artifacts at their expected main-checkout paths and masking them with the repository masker, through the permission gate because the main checkout is not writable from a worktree sandbox; and `agmsg-dispatch`, through `excludedCommands` (step 11). Every other out-of-sandbox action stays a blocked PONG. A Codex seat has in-sandbox network (T64) and never leaves its sandbox.
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
    - A worker cannot inspect the host for the server either. Neither seat may leave its sandbox for host commands, because that would be an escalation, which step 4 forbids. A Claude seat's sandboxed Bash also runs in a separate pid namespace, so `pgrep`, `ps` or a cwd lookup there sees only the sandbox's own processes.
    - So the worker, Claude or Codex, adds `plan-mode-used=<worktree>` to the RESULT and does nothing else about the server.
    - The orchestrator handles it as control-plane hygiene on the host. It runs these `pgrep`/`ps`/`kill` calls outside its own sandbox through the permission gate (`dangerouslyDisableSandbox`, answered by the operator or the auto-mode classifier) under its control-plane exemption, as it already does for `agmsg-dispatch` and `herdr-agents --audit`. It lists servers with `pgrep -fl _serve`, where a process named `crit` is a Crit server and the calling shell is listed under its own name. It reads each server's session record (`~/.crit/sessions/*.json` holds `pid`, `cwd` and `branch`) and confirms the server is live before acting: `ps -o args= -p <pid>` must show `crit _serve`, and the record's `cwd` must be that worker's worktree. The live process's own cwd must also match: `readlink /proc/<pid>/cwd` on Linux (`lsof -a -d cwd -p <pid> -Fn` on macOS) must equal the record's `cwd`. A mismatch means the pid was reused, and the record is stale. Only then does it stop the server with `kill <pid>`. A record whose pid is gone or runs another command is stale; it is removed, never killed. Never use `crit stop --all`, which stops every seat's server.
15. After the final push, wait for CI and the Codex Bot before sending RESULT.
    - Mark the PR ready for review with `gh pr ready <n>` before the first wait, while it is still a draft (`gh pr ready` exits non-zero on a PR that is already ready, so a later head's wait skips it): the Codex Bot reviews non-draft PRs, and a draft only on an explicit `@codex review` comment. When no Bot review of the final head arrives within 10 minutes, post `@codex review` on the PR and wait out the rest of the window.
    - Run `gh pr checks <pr> --watch` in the background and the Bot wait below at the same time: the 10-minute and 15-minute marks count from `gh pr ready` (from the push, for a later head), never from the end of CI. Right after a push GitHub can report no checks yet, and the watcher then exits 1 with `no checks reported`: start it once a check is listed, and restart it on that message instead of reading it as a CI failure. Wait for that watcher's exit status before the RESULT: a non-zero exit means no RESULT until CI passes.
    - Then list the Bot's reviews of the final head with `gh api --paginate repos/{owner}/{repo}/pulls/<n>/reviews --jq '.[]|select(.user.login=="chatgpt-codex-connector[bot]" and .commit_id=="<head-sha>")|[.commit_id,.submitted_at]|@tsv'` and the Bot's top-level review comments raised on it with `gh api --paginate repos/{owner}/{repo}/pulls/<n>/comments --jq '.[]|select(.in_reply_to_id == null and .user.login=="chatgpt-codex-connector[bot]" and .original_commit_id=="<head-sha>")|[.id,.original_commit_id,.path]|@tsv'`. A human comment, a CodeRabbit review or an earlier head's review never ends the wait. A comment's `commit_id` moves to the newest head, so findings are matched by `original_commit_id`. Repeat until a review of the final head appears or 15 minutes pass; the report records the latter as `bot: none`. The final head here is the diff head, the last commit that changes the PR's content: a head that only merges the new base with `gh pr update-branch` needs green CI but no new Bot wait. Both endpoints return 30 items per page by default, so keep `--paginate`.
    - This bounded wait is the permitted exception to the no-polling rule in "Regime activation and progress", which governs detecting worker completion and pane status, not a worker's wait on CI and the Bot. List at most every 30 seconds, stop at 15 minutes, and run the loop as a background command or a foreground command with a timeout. Never use bare foreground `sleep`.
    - A 👍 reaction alone is not evidence of a review.
    - Read each listed review's body too: the Codex Bot sometimes places a finding (a `P0`–`P3` badge with a blob link) in the review body instead of an inline thread. Such a review-body finding is listed alongside the top-level inline comments and fixed or dispositioned the same way.
    - Fix P0/P1 findings, inline or review-body, with a fix commit and start over from the push, at most twice. The third Bot round is not fixed: send `AGMSG-RESULT … bot_rounds=3` with each of its threads listed as `open:<thread id>` (`open:review-<review id>` for a review-body finding), an escalated label that the next bullet's `fixed:`/`not-applicable:` rule does not cover, and the orchestrator decides (a threat-table row, a disposition, or S1).
    - The RESULT names every unresolved thread id with `fixed:<sha>` or a proposed `not-applicable:<reason>`. The worker resolves no thread.

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

 succeeded in 215ms:
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

 succeeded in 300ms:
?? .orchestration/acceptance/dotfiles-T128-chain-review-scripts-a01.md
?? .orchestration/reports/dotfiles-T128-chain-review-scripts-a01.md
?? .orchestration/sandboxes/dotfiles-T128-chain-review-scripts-a01.md
?? .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-a01-audit-b6ce4ff.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-a01-pr-feedback.json
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-a01.md
ec94dc56305f55df470a4b1d4215ad272418beac
worktree ~/Workspace/dotfiles
HEAD ec94dc56305f55df470a4b1d4215ad272418beac
branch refs/heads/main

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles--claude-worktrees-worker-c/3747b995-3bb1-4c51-8421-4b1e672b442a/scratchpad/t124/mut
HEAD 52bb69fc0f2085e290f242e9145f74ba84f2a25c
detached

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/a3-replay
HEAD e87a52fc42eb4595c28585af6742e2c403302eee
detached

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/boundary-10
HEAD 014be44d0414492058d08d67b68e2a0eea23c17b
branch refs/heads/orchestration/boundary-10

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/boundary-11
HEAD fd3728be2127064803b956845a9a41efb18f6088
branch refs/heads/orchestration/boundary-11

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/boundary-12
HEAD 1e5d213a6be4a2df993240fe8463296ee9f8b29d
branch refs/heads/orchestration/boundary-12

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/boundary-13
HEAD e04dd19654b48aaca289059093484fde0bbf0511
branch refs/heads/orchestration/boundary-13

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/boundary-14
HEAD 5cb3757f73ddb44d94b0c3cf213bc89370b8eeff
branch refs/heads/orchestration/boundary-14

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/boundary-2026-10-11-2
HEAD 024826982257f6d9a6a8a74c2e6b2b743e5be55e
branch refs/heads/orchestration/boundary-2026-10-11-2

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/boundary-2026-10-12
HEAD bdf60419ad055a92f5048824482f3f94f1be61e1
branch refs/heads/orchestration/boundary-2026-10-12

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/boundary-2026-10-12-2
HEAD 8003a8d5222d899a208d89886051aba881397fe6
branch refs/heads/orchestration/boundary-2026-10-12-2

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/boundary-2026-10-12-3
HEAD b1230e7c86b81745366a834cbc86cad259c06d43
branch refs/heads/orchestration/boundary-2026-10-12-3

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/boundary-2026-10-12-4
HEAD bfe3161eba36109aa34c78f695020da81c9b03b8
branch refs/heads/orchestration/boundary-2026-10-12-4

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/boundary-2026-10-12-5
HEAD 9b56596c9d16922642ec4a319babde5d52ebe2f8
branch refs/heads/orchestration/boundary-2026-10-12-5

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/boundary-2026-10-12-6
HEAD cf9e1f89b01e6cb1fb37461e0b7a1ef0fc1a5be4
branch refs/heads/orchestration/boundary-2026-10-12-6

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/boundary-2026-10-12-7
HEAD 6a5acc0c6f67484a47babf6c33c69d07d6edade4
branch refs/heads/orchestration/boundary-2026-10-12-7

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/boundary-2026-10-12-8
HEAD 7db67953a360c2652edad5f7ae07ca087e0f7017
branch refs/heads/orchestration/boundary-2026-10-12-8

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/boundary-2026-10-12-9
HEAD 47f18670088b19be384cf0245f88fd5480d076d3
branch refs/heads/orchestration/boundary-2026-10-12-9

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/boundary-2026-10-13-1
HEAD 0103aefc3124f826aeedfc45da6f93ad17245cd4
branch refs/heads/orchestration/boundary-2026-10-13-1

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/boundary-2026-10-13-2
HEAD 961f47e1fd055d04df87a43b3d6d6bda6f772b19
branch refs/heads/orchestration/boundary-2026-10-13-2

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/boundary-2026-10-13-3
HEAD 1762ae0a0640e137f245f1af370c3a9d61a3bfb8
branch refs/heads/orchestration/boundary-2026-10-13-3

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/boundary-2026-10-13-4
HEAD 110471561c1697b98a17290d7235184dc9955784
branch refs/heads/orchestration/boundary-2026-10-13-4

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/boundary-2026-10-13-5
HEAD 1c2e4cc4cd7d94e43a731161f3d00d8d0250eabf
branch refs/heads/orchestration/boundary-2026-10-13-5

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/boundary-2026-10-13-6
HEAD 9c23147aa6d3ea0e1c6f6d4e08e533aa457e4a35
branch refs/heads/orchestration/boundary-2026-10-13-6

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/boundary-2026-10-13-7
HEAD 967251263b2655b1b3325fe070dcedbe8c3493b6
branch refs/heads/orchestration/boundary-2026-10-13-7

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/boundary-2026-10-13-8
HEAD 7491de0377e7ce4753916297129b24933980fdcb
branch refs/heads/orchestration/boundary-2026-10-13-8

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/boundary-2026-10-13-9
HEAD e86c38cb11fda50d25cd453f50e50a6dfc0fb9c1
branch refs/heads/orchestration/boundary-2026-10-13-9

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/t717-prep
HEAD 683384eaabd7a77a09f4452f518d2faa13c5123c
detached

worktree ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
HEAD ec94dc56305f55df470a4b1d4215ad272418beac
detached

worktree ~/Workspace/dotfiles/.claude/worktrees/worker-c
HEAD d15fa8779c298a841fe2791316f022228232a402
branch refs/heads/tools/chain-github-scripts

worktree ~/Workspace/dotfiles/.claude/worktrees/worker-d
HEAD 4f9627ac316cacd879dfe08f0269f4205946dac0
branch refs/heads/receipt/canonical

worktree ~/Workspace/dotfiles/.claude/worktrees/worker-e
HEAD 30cbfb4d226dbf71dfe1ca9fc17a8858ce3c939f
branch refs/heads/feat/project-map-reload-hook

worktree ~/Workspace/dotfiles/.claude/worktrees/worker-f
HEAD 04a7d02ad856eadab87ff54b383e65e806b0a5f3
branch refs/heads/regime/chain-review-scripts

 .../autoskill.md                                   |   3 +
 .../learning.md                                    |  18 +
 .../report.md                                      | 103 ++++++
 .../sandbox.md                                     |  40 +++
 .../dotfiles-T128-chain-review-scripts-a01/task.md |  94 ++++++
 .../validation.md                                  | 375 +++++++++++++++++++++
 scripts/orchestrator/local-advisory.sh             |  49 +++
 scripts/orchestrator/local-review.sh               |  75 +++++
 scripts/orchestrator/sandbox-scan.sh               |  24 ++
 tests/unit/test_chain_review_scripts.py            | 230 +++++++++++++
 10 files changed, 1011 insertions(+)

**Organizing output and reviewing code**
codex
🐙 私は gh-first-workflow を読みました。
作業ツリーには監査用の未追跡資料がありますが、追跡ファイルに変更はありません。コードは `git show` で指定 head に固定して読み、ファイル作成・checkout・テスト実行は行いません。
exec
/bin/zsh -lc "rg -n 'Codex seat worklogs|task-level audit|threat.table|"'^10'"\\.|"'^## '"' ~/.agents/skills/agmsg-orchestration/SKILL.md && sed -n '180,245p' ~/.agents/skills/agmsg-orchestration/SKILL.md && sed -n '270,360p' ~/.agents/skills/agmsg-orchestration/SKILL.md" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc 'gh pr view 357 --repo mryfmo/dotfiles --json url,headRefOid,baseRefOid,state,statusCheckRollup' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc 'cat ~/.codex/plugins/cache/ponytail/ponytail/5.2.0/skills/ponytail-review/SKILL.md && cat ~/.agents/skills/shdoc-shell-docs/SKILL.md' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc "python3 -B - <<'PY'
import subprocess
h='b6ce4ffabe0e66a102e224e75be575a501c5a793'
paths=['.orchestration/tasks/dotfiles-T128-chain-review-scripts-a01/task.md','scripts/orchestrator/local-review.sh','scripts/orchestrator/local-advisory.sh','scripts/orchestrator/sandbox-scan.sh','tests/unit/test_chain_review_scripts.py']
for p in paths:
 print('\\nFILE '+p)
 r=subprocess.run(['git','show',h+':'+p],capture_output=True,text=True)
 print('\\n'.join(f'{i}: {line}' for i,line in enumerate(r.stdout.splitlines(),1)) if r.returncode==0 else r.stderr)
PY" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 exited 1 in 186ms:
zsh:1: can't create temp file for here document: operation not permitted

 succeeded in 209ms:
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
---
name: shdoc-shell-docs
description: Write and review shellscript documentation with shdoc annotations. Use when Codex creates, edits, or reviews `.sh` files or shell executables and should add, repair, or normalize `@file`, `@brief`, `@description`, `@arg`, `@option`, and `@example` comments to match shdoc conventions.
---

# Shdoc Shell Docs

## Overview

Use this skill to make shellscript comments parseable by `shdoc` without bloating simple code with boilerplate. Inspect the file first, then document the script and the non-trivial functions that benefit from generated reference docs.

## Workflow

1. Inspect the target shell file before writing comments.
2. Read `references/shdoc-rules.md` before editing comments.
3. Use `scripts/generate-docs.sh` as the repo-local style example when working in this repository.
4. Add or repair file-level annotations near the top of the file:
   - Prefer `@file` for the script identifier.
   - Add `@brief` for a single-sentence summary.
   - Add multiline `@description` only when the script needs more context.
5. Add function-level annotations only where they help:
   - Start with `@description`.
   - Add `@arg` for positional parameters.
   - Add `@option` for flags and option-value pairs.
   - Add `@example` when the call shape is not obvious.
   - Add `@stdout`, `@stderr`, `@exitcode`, or `@see` only when they clarify observable behavior.
6. Rewrite existing free-form comments into valid `shdoc` annotations instead of keeping two parallel comment styles.

## Review Checklist

- Confirm the docs match the implementation instead of guessing arguments or options.
- Keep annotations immediately above the file header or function they describe.
- Prefer behavior and operator-facing intent over internal implementation notes.
- Skip boilerplate comments for trivial private helpers unless the user asks for exhaustive coverage.
- Keep multiline annotation blocks compact and easy to render as Markdown.

## References

- Read `references/shdoc-rules.md` for the minimal tag set, concise examples, and external reference policy.

 succeeded in 232ms:
10:## Architecture
17:## Regime activation and progress
21:- A Claude session started in the repository root outside Herdr (a plain shell, mosh/ssh, or `claude -p`) is a pane-less orchestrator: nothing seats a worker automatically, and the SessionStart `herdr-agents --attach` hook prints a summary line naming that state, the on-demand commands, and any seated worker, followed in a regime repository by the `agmsg-orchestration:` directive line. Bring the regime up on demand: claim the seat outside the sandbox with the composite instance id, `actas-claim.sh <repo> claude-code <name> <session_id>.<claude pid>` (a claim from sandboxed Bash writes the bare session id and turn delivery then skips silently; see the seat-lock bullet below); seat the worker with `herdr-agents --add-worker <worktree>` (it derives `HERDR_SOCKET_PATH` from the default Herdr server socket `~/.config/herdr/herdr.sock`, the path the Claude sandbox allowlists, before creating anything, accepts a claude worker's workspace-trust dialog during spawn's readiness wait, and takes `--ready-timeout <seconds>`); confirm the worker's placement from its `run/spawn.*` placement record itself (the `herdr:<socket>:<pane>` row that upstream `agmsg_spawn_path` resolves) and the `linkage=` line `--add-worker` prints, never from `team.sh <team> --json`, which observes Codex members by reading their pane; treat the `linkage=` line `--add-worker` prints as the `AGMSG-PING` evidence, and on `pong=no` or `linkage=unreached` wake again with `agmsg-dispatch <team> <orchestrator> <worker> <pane> 'AGMSG-PING v1 task_id=<id> reason=<reason>'` and verify the PING's `read_at` (`poke.sh` only for a viewed workspace); and dispatch no AGMSG-TASK before its `AGMSG-PONG` arrives. Without a managed workspace the auditor runs headless, in the form the task-level audit bullet below names. A sandboxed pane-less session cannot keep a Monitor watch (the sandbox's pid namespace), so RESULTs arrive by turn delivery.
29:## Parallel workers
33:- Delegate all repository-mutating work — file edits, builds, test runs, and git state changes — to seated workers, with at most one seated worker per git worktree and sequential assignments within one worktree. Add worktrees for parallelism; never use parallel `codex exec` or per-task Codex spawning, except that the read-only, non-interactive task-level audit the orchestrator runs during acceptance (the task-level audit bullet below) is not worker spawning and is permitted; it is identity-less. agmsg/herdr control-plane commands (`delivery.sh`, `watch.sh`, `actas-claim.sh`, `send.sh`, `join.sh`, and herdr agent/pane commands) are orchestrator-side exemptions.
43:  - Some steps stay sequential. The single audit tab serializes audits; the task-level audit of T67 reduces them to one per task. The orchestrator-side gate (`make require-crit-review`) and merges also run one at a time.
46:## Identity, delivery, and storage
59:## Live verification
64:## Review and integration invariants
71:- A task that touches a trust boundary (anything the design tier lists, CI that decides a required check, code that executes PR-controlled input) carries a `threat_table` in its front matter: one `{control, disposition}` row per thing the PR or the orchestrator controls (the tree and its tests, task.md, workflow files, interpreter and environment files, in-process effects, new or renamed scripts, metadata separators). The row unit is one row per `allowed_files` entry, one row per listed control that is not a path (task metadata, workflow and interpreter or environment inputs, in-process effects, new or renamed scripts, metadata separators), carried by the declared test module's row where that is where the control acts, and one row per orchestrator effect from the fixed list (forced removal, merge, update-branch); under a wildcard `allowed_files` entry whose files are executed or applied (scripts, workflows, hooks, settings, the rules seats follow), one row per concrete file the PR changes; a wildcard over test fixtures or other data files keeps one row; C4 of the task-consistency check (plan 007 T704) verifies the path half once it lands, and the task-file review checks it by hand until then. A disposition takes one of three forms: `closed: tests/<file>::<name>`, the test that closes the row; `residual: <sentence>`, the compensating control; `out-of-scope: <task id>`, the task that owns the row. Shape is `schemas/task.json`'s (wave V1): a `closed` selector names a test present in the PR tree at acceptance and in the schema's validation of the PR, an `out-of-scope` owner is a task id in the design's `implementing_tasks`, a `residual` payload is a sentence of at least 20 characters (the gate's minimum for a reason). Until `schemas/task.json` lands in wave V1, the task-file review checks the three shape rules by hand. For a `closed` row it checks the selector's form only, since the test does not exist before implementation. Substance is the reviewers': the task-file review, the Bot and the auditor judge each row against the diff. The table is the task's completion condition: a missing row is added once, counted as an amendment, never fixed finding by finding.
72:- Before every acceptance action (revise, accept, merge) the orchestrator runs `scripts/regime-counters.sh <task id>` and pastes its output into the acceptance record. S2 is decided from INV-6's counts: each component the script prints is read from its output, and for each component it prints as `unknown` the record pastes the command and output that read the source INV-6 names for that component, or, while that source has no entry for the task, says so and pastes the reading of the interim record the orchestrator used in its place. S1 (plan 006: the same finding class three times on one artifact, from any reviewer) is decided from the record's finding-class table, which gives a class to every finding the PR-feedback sweep lists, whatever its disposition, and to every task-level audit finding; three rows of one class stop the artifact.
95:## Message Contract v1
144:## `.orchestration` Workspace Layout
157:## Orchestrator Playbook
168:10. For a RESULT that carries a pull request, integrate in this order. This is the single procedure that the PR integration rule, `AGENTS.md`, the README and the gh-first-workflow skill cite. A `gh pr update-branch` moves the head, so steps 1 to 4 run again on the new head. After an update-branch the orchestrator runs it, the order is CI on the new head, then the sweep, then the audit; an audit started before CI finishes sees incomplete evidence and returns an evidence-only `incorrect`. Select a checkout with git -C <absolute path>, never with cd, which the sandboxed Bash may not honour. After moving the review worktree to the audited head, verify git -C <review> rev-parse HEAD equals that head and git -C <main> symbolic-ref --short HEAD prints main before the audit and the gate.
170:    2. Run the task-level audit of that head in the pair or headless form of the task-level audit bullet. It exits nonzero for every verdict other than `correct`. An exit with `Audit verdict: incorrect` is not a failed step: continue to step 3 and disposition its findings. A `blocked` or missing verdict means re-running the audit.
184:## Worker Playbook
195:10. If blocked, still write the report and evidence paths that explain the blocker.
211:    - Fix P0/P1 findings, inline or review-body, with a fix commit and start over from the push, at most twice. The third Bot round is not fixed: send `AGMSG-RESULT … bot_rounds=3` with each of its threads listed as `open:<thread id>` (`open:review-<review id>` for a review-body finding), an escalated label that the next bullet's `fixed:`/`not-applicable:` rule does not cover, and the orchestrator decides (a threat-table row, a disposition, or S1).
214:## Codex seat worklogs
248:## Pitfalls
    5. After the required checks pass and the threads are resolved, merge with `gh pr merge <pr> --squash --match-head-commit <audited head sha>`, so a newer head can never be merged on the evidence of the audited one. Every seat acts as the machine's one GitHub account, so no approval is required or possible. Who merges is decided by the integration gate and by native denial of merge commands in Codex seats; `herdr-agents` writes the Claude worker deny rules (`Bash(gh pr merge:*)`, `Bash(gh api -X PUT:*)`, `Bash(gh api --method PUT:*)`, `Bash(gh api graphql:*)`) into the worker worktree's `.claude/settings.local.json`, where [deny rules take precedence over allow rules and cover nested subcommands in every permission mode](https://code.claude.com/docs/en/permissions), but a method flag after the path escapes these prefix rules, so the integration gate remains the authority.
    6. Send `AGMSG-ACCEPTANCE` (step 11).
11. Send `AGMSG-ACCEPTANCE v1 status=accepted` when done, or `status=revise` with a narrow `reason` and `next_action` when more work is required.

## Worker Playbook

1. Read the full `AGMSG-TASK v1` message.
2. Switch to the `repo` and read `task_file` before editing or running validations. Create the task branch without touching the shared `.git/config`, which is read-only for a Codex seat by design (T64 writable roots): `git switch -c <branch> --no-track origin/main`, push with `git push origin <branch>` (no `-u`), and open the PR as a draft with `gh pr create --draft --head <branch>`. Commit inside the sandbox, with `git -c commit.gpgsign=false` when the signing key is unreadable there; for a Claude seat only the push leaves the sandbox, and a Codex seat pushes from inside it (step 4). A Claude seat's sandbox can leave the same failed write behind, so it uses the same commands. A leftover `.git/config.lock` from a failed attempt is removed by the orchestrator. Remove a scratch worktree (for example one that proves a test fails on `origin/main`) with `git worktree remove <path>` only; never run `git worktree prune` from a sandboxed seat, because other worktrees' paths look missing inside the sandbox and prune then targets their admin directories in the shared `.git/worktrees`.
3. Treat `allowed_files` as the edit boundary. If it says to see the task file, read that section and follow it exactly.
4. Do not perform any `forbidden_actions`. Complete every command inside the sandbox and allowlist; never escalate an action outside that boundary for approval. Fail it instead, send `AGMSG-PONG v1 status=blocked` with the exact command and the boundary it crosses, and wait for the orchestrator to re-task. Agent-to-agent permission approval is forbidden: only the human operator answers a permission prompt. A Claude Code auto-mode classifier denial (for example Self-Modification) is such a boundary: stop without a diff, send `AGMSG-PONG v1 status=blocked` naming the classifier reason, and never pursue the same outcome through another tool. Fetch and fast-forward inside the sandbox; a public remote needs no credential. On Linux, `gh` backed by the host keyring answers HTTP 401 inside the sandbox, because AF_UNIX socket creation is denied and `allowUnixSockets` cannot grant a path. So a Claude seat runs three commands outside the sandbox through the permission gate: `gh`, `git push`, and an authenticated `git fetch` (a private HTTPS remote, whose credential helper is `gh`). Look up a VERIFY item's external reference (upstream documentation, release notes, an API schema) with the WebFetch tool, not Bash `curl`. Three documented cases run outside the sandbox too: the task's main-checkout CompactionDB `memory add`, through the permission gate because that state directory is read-only from a worktree sandbox; writing the task's artifacts at their expected main-checkout paths and masking them with the repository masker, through the permission gate because the main checkout is not writable from a worktree sandbox; and `agmsg-dispatch`, through `excludedCommands` (step 11). Every other out-of-sandbox action stays a blocked PONG. A Codex seat has in-sandbox network (T64) and never leaves its sandbox.
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
    - A worker cannot inspect the host for the server either. Neither seat may leave its sandbox for host commands, because that would be an escalation, which step 4 forbids. A Claude seat's sandboxed Bash also runs in a separate pid namespace, so `pgrep`, `ps` or a cwd lookup there sees only the sandbox's own processes.
    - So the worker, Claude or Codex, adds `plan-mode-used=<worktree>` to the RESULT and does nothing else about the server.
    - The orchestrator handles it as control-plane hygiene on the host. It runs these `pgrep`/`ps`/`kill` calls outside its own sandbox through the permission gate (`dangerouslyDisableSandbox`, answered by the operator or the auto-mode classifier) under its control-plane exemption, as it already does for `agmsg-dispatch` and `herdr-agents --audit`. It lists servers with `pgrep -fl _serve`, where a process named `crit` is a Crit server and the calling shell is listed under its own name. It reads each server's session record (`~/.crit/sessions/*.json` holds `pid`, `cwd` and `branch`) and confirms the server is live before acting: `ps -o args= -p <pid>` must show `crit _serve`, and the record's `cwd` must be that worker's worktree. The live process's own cwd must also match: `readlink /proc/<pid>/cwd` on Linux (`lsof -a -d cwd -p <pid> -Fn` on macOS) must equal the record's `cwd`. A mismatch means the pid was reused, and the record is stale. Only then does it stop the server with `kill <pid>`. A record whose pid is gone or runs another command is stale; it is removed, never killed. Never use `crit stop --all`, which stops every seat's server.
15. After the final push, wait for CI and the Codex Bot before sending RESULT.
    - Mark the PR ready for review with `gh pr ready <n>` before the first wait, while it is still a draft (`gh pr ready` exits non-zero on a PR that is already ready, so a later head's wait skips it): the Codex Bot reviews non-draft PRs, and a draft only on an explicit `@codex review` comment. When no Bot review of the final head arrives within 10 minutes, post `@codex review` on the PR and wait out the rest of the window.
    - Run `gh pr checks <pr> --watch` in the background and the Bot wait below at the same time: the 10-minute and 15-minute marks count from `gh pr ready` (from the push, for a later head), never from the end of CI. Right after a push GitHub can report no checks yet, and the watcher then exits 1 with `no checks reported`: start it once a check is listed, and restart it on that message instead of reading it as a CI failure. Wait for that watcher's exit status before the RESULT: a non-zero exit means no RESULT until CI passes.
    - Then list the Bot's reviews of the final head with `gh api --paginate repos/{owner}/{repo}/pulls/<n>/reviews --jq '.[]|select(.user.login=="chatgpt-codex-connector[bot]" and .commit_id=="<head-sha>")|[.commit_id,.submitted_at]|@tsv'` and the Bot's top-level review comments raised on it with `gh api --paginate repos/{owner}/{repo}/pulls/<n>/comments --jq '.[]|select(.in_reply_to_id == null and .user.login=="chatgpt-codex-connector[bot]" and .original_commit_id=="<head-sha>")|[.id,.original_commit_id,.path]|@tsv'`. A human comment, a CodeRabbit review or an earlier head's review never ends the wait. A comment's `commit_id` moves to the newest head, so findings are matched by `original_commit_id`. Repeat until a review of the final head appears or 15 minutes pass; the report records the latter as `bot: none`. The final head here is the diff head, the last commit that changes the PR's content: a head that only merges the new base with `gh pr update-branch` needs green CI but no new Bot wait. Both endpoints return 30 items per page by default, so keep `--paginate`.
    - This bounded wait is the permitted exception to the no-polling rule in "Regime activation and progress", which governs detecting worker completion and pane status, not a worker's wait on CI and the Bot. List at most every 30 seconds, stop at 15 minutes, and run the loop as a background command or a foreground command with a timeout. Never use bare foreground `sleep`.
    - A 👍 reaction alone is not evidence of a review.
    - Read each listed review's body too: the Codex Bot sometimes places a finding (a `P0`–`P3` badge with a blob link) in the review body instead of an inline thread. Such a review-body finding is listed alongside the top-level inline comments and fixed or dispositioned the same way.
    - Fix P0/P1 findings, inline or review-body, with a fix commit and start over from the push, at most twice. The third Bot round is not fixed: send `AGMSG-RESULT … bot_rounds=3` with each of its threads listed as `open:<thread id>` (`open:review-<review id>` for a review-body finding), an escalated label that the next bullet's `fixed:`/`not-applicable:` rule does not cover, and the orchestrator decides (a threat-table row, a disposition, or S1).
    - The RESULT names every unresolved thread id with `fixed:<sha>` or a proposed `not-applicable:<reason>`. The worker resolves no thread.

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

 exited 1 in 374ms:
error connecting to api.github.com
check your internet connection or https://githubstatus.com

**Analyzing tool usage and GitHub metadata**
exec
/bin/zsh -lc 'git diff --name-status ec94dc56305f55df470a4b1d4215ad272418beac b6ce4ffabe0e66a102e224e75be575a501c5a793 && git diff --no-ext-diff ec94dc56305f55df470a4b1d4215ad272418beac b6ce4ffabe0e66a102e224e75be575a501c5a793 -- scripts/orchestrator tests/unit/test_chain_review_scripts.py' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc "python3 -B -c 'import pathlib,subprocess; h=\"b6ce4ffabe0e66a102e224e75be575a501c5a793\"; p=\".orchestration/tasks/dotfiles-T128-chain-review-scripts-a01.md\"; print(\"LOCAL TASK\\n\"+pathlib.Path(p).read_text()); paths=subprocess.check_output([\"git\",\"diff\",\"--name-only\",\"ec94dc56305f55df470a4b1d4215ad272418beac\",h],text=True).splitlines(); paths=[p for p in paths if p.endswith(\"task.md\")]; [(print(\"\\nBRANCH \"+p),print(\"\\n\".join(str(i)+\": \"+line for i,line in enumerate(subprocess.check_output([\"git\",\"show\",h+\":\"+p],text=True).splitlines(),1)))) for p in paths]'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc "python3 -B -c 'import json,pathlib,subprocess; p=pathlib.Path(\".ua/knowledge-graph.json\"); m=pathlib.Path(\".ua/meta.json\"); print(\"meta\",m.read_text() if m.exists() else \"missing\"); print(\"graph\",p.exists()); d=json.loads(p.read_text()) if p.exists() else {}; print(\"nodes\",[(n.get(\"filePath\"),n.get(\"summary\")) for n in d.get(\"nodes\",[]) if any(s in (n.get(\"filePath\",\"\")+n.get(\"summary\",\"\")) for s in [\"orchestrator/\", \"local-review\", \"chain-review\", \"021-\"])])' && sed -n '64,94p' ~/.agents/skills/agmsg-orchestration/SKILL.md && sed -n '157,181p' ~/.agents/skills/agmsg-orchestration/SKILL.md" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 130ms:
A	.orchestration/dotfiles-T128-chain-review-scripts-a01/autoskill.md
A	.orchestration/dotfiles-T128-chain-review-scripts-a01/learning.md
A	.orchestration/dotfiles-T128-chain-review-scripts-a01/report.md
A	.orchestration/dotfiles-T128-chain-review-scripts-a01/sandbox.md
A	.orchestration/dotfiles-T128-chain-review-scripts-a01/task.md
A	.orchestration/dotfiles-T128-chain-review-scripts-a01/validation.md
A	scripts/orchestrator/local-advisory.sh
A	scripts/orchestrator/local-review.sh
A	scripts/orchestrator/sandbox-scan.sh
A	tests/unit/test_chain_review_scripts.py
diff --git a/scripts/orchestrator/local-advisory.sh b/scripts/orchestrator/local-advisory.sh
new file mode 100755
index 00000000..90d57e15
--- /dev/null
+++ b/scripts/orchestrator/local-advisory.sh
@@ -0,0 +1,49 @@
+#!/usr/bin/env bash
+# @file local-advisory.sh
+# @brief Record a local review's P2/P3 findings as advisory rows of the acceptance record; stop on a P0/P1.
+# @description
+#   Plan 020 step 1.2 for the local review. Reads `.orchestration/validation/<task>-local-review-<sha7>.md`. Each
+#   unique finding, numbered from 1: a P0/P1 prints STOP (the PR's one round is over: the plan's step 4.2); any
+#   other appends the row `local:<sha7>:<n><TAB>advisory-p2` under the heading `## Owned by <owner>` of
+#   `.orchestration/acceptance/<task>.md` (created when missing) and a `local-finding: <sha7>:<n>
+#   not-applicable:advisory P2 owned by <owner> (…); evidence=…` line, each only when the record lacks it.
+# @arg $1 string Task id.
+# @arg $2 string The reviewed head, 40 hex characters.
+# @arg $3 string The task id that owns the advisory findings.
+# @exitcode 0 No P0/P1 finding.
+# @exitcode 2 No local review file.
+# @exitcode 3 A P0/P1 finding.
+# @example
+#   scripts/orchestrator/local-advisory.sh dotfiles-T128-x-a01 "$head" dotfiles-T128-x-followup-a01
+set -euo pipefail
+task=$1 head=$2 owner=$3
+cd "$(git rev-parse --show-toplevel)"
+h7=${head:0:7}
+LR=".orchestration/validation/$task-local-review-$h7.md"
+A=".orchestration/acceptance/$task.md"
+[ -s "$LR" ] || {
+    echo "no local review file $LR"
+    exit 2
+}
+n=$(sed -n 's/^findings: //p' "$LR" | head -1)
+[ "${n:-0}" != "0" ] || {
+    echo "local review of $h7: no findings"
+    exit 0
+}
+/usr/bin/grep -q "^## Owned by $owner" "$A" || printf '\n## Owned by %s (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)\n\n' "$owner" >> "$A"
+i=0 stop=0
+while IFS= read -r line; do
+    i=$((i + 1))
+    case "$line" in
+    *"[P0]"* | *"[P1]"*)
+        echo "STOP: local finding $i of $h7 is P0/P1: $line"
+        stop=1
+        ;;
+    *)
+        /usr/bin/grep -q "^local:$h7:$i	" "$A" || printf 'local:%s:%s\tadvisory-p2\n' "$h7" "$i" >> "$A"
+        /usr/bin/grep -q "^local-finding: $h7:$i " "$A" || printf 'local-finding: %s:%s not-applicable:advisory P2 owned by %s (%s); evidence=git show origin/main:.orchestration/tasks/%s.md | grep -n '"'"'item 1'"'"'\n' "$h7" "$i" "$owner" "$(printf '%s' "$line" | cut -c1-120 | tr -d '`')" "$owner" >> "$A"
+        ;;
+    esac
+done < <(/usr/bin/grep -E '^- \[P[0-3]\]' "$LR" | sort -u)
+echo "local review of $h7: $i finding(s) recorded as advisory under 'Owned by $owner' in $A"
+[ "$stop" = 0 ] || exit 3
diff --git a/scripts/orchestrator/local-review.sh b/scripts/orchestrator/local-review.sh
new file mode 100755
index 00000000..04806af5
--- /dev/null
+++ b/scripts/orchestrator/local-review.sh
@@ -0,0 +1,75 @@
+#!/usr/bin/env bash
+# @file local-review.sh
+# @brief Review a PR head's diff against main locally with the Bot's engine, once per head, before the audit (C-32).
+# @description
+#   Run outside the Bash sandbox: inside it codex exits 1 ("failed to initialize in-process app-server client:
+#   Operation not permitted"). An existing `.orchestration/validation/<task>-local-review-<sha7>.md` is reused and
+#   re-reported. Otherwise the clean review worktree (`$ORCH_REVIEW_WORKTREE`, else
+#   `.claude/worktrees/orchestrator-review`), a path with its own `.git` entry, is checked out detached at the head
+#   and left there, and the review binary (`$CODEX_BIN`, else codex) runs in it as `--profile review -s read-only
+#   review --base main`. The file gets the front matter, the unique `- [P0-3]` findings of the transcript's final
+#   message, and that message with the worktree prefix stripped; the findings are printed, then `local-review: <n>
+#   findings (<file>)`.
+# @arg $1 string Task id.
+# @arg $2 string The PR head commit, a local one.
+# @arg $3 int PR number.
+# @exitcode 0 No finding.
+# @exitcode 2 A precondition failed: the head is not a local commit, the review worktree is not a worktree root or not
+#   clean, or there is no review binary.
+# @exitcode 3 One or more findings.
+# @example
+#   scripts/orchestrator/local-review.sh dotfiles-T128-x-a01 "$(git rev-parse FETCH_HEAD)" 356
+set -euo pipefail
+task=$1 head=$2 pr=$3
+R="$(git rev-parse --show-toplevel)"
+cd -- "$R"
+W=${ORCH_REVIEW_WORKTREE:-$R/.claude/worktrees/orchestrator-review}
+out=$R/.orchestration/validation/$task-local-review-${head:0:7}.md
+if [ -s "$out" ]; then
+    # one sample per head (C-32): a review of this head exists; reuse it instead of sampling again
+    findings=$(/usr/bin/grep -E '^- \[P[0-3]\]' "$out" | sort -u || true)
+    n=$(sed -n 's/^findings: //p' "$out" | head -1)
+    printf '%s\n' "$findings"
+    echo "local-review: $n findings (existing $out)"
+    [ "${n:-0}" = 0 ] || exit 3
+    exit 0
+fi
+git -C "$R" cat-file -e "$head^{commit}" 2> /dev/null || {
+    echo "local-review: $head is not a local commit (fetch pull/$pr/head first)"
+    exit 2
+}
+# Without its own .git entry, git -C would act on an enclosing checkout and move that one to the head.
+[ -e "$W/.git" ] || {
+    echo "local-review: $W is not a worktree root"
+    exit 2
+}
+[ -z "$(git -C "$W" status --porcelain)" ] || {
+    echo "local-review: $W is not clean"
+    exit 2
+}
+# Resolved in the root before the checkout and run by its absolute path, so no relative PATH entry (./bin) picks a
+# binary from the PR head.
+codex=$(command -v "${CODEX_BIN:-codex}") || {
+    echo "local-review: no review binary ${CODEX_BIN:-codex}"
+    exit 2
+}
+[[ $codex == /* ]] || codex=$R/$codex
+git -C "$W" checkout -q --detach "$head"
+base=$(git -C "$W" merge-base main HEAD)
+t0=$(date -u +%FT%TZ)
+tmp=$(mktemp "${TMPDIR:-/tmp}/local-review.XXXXXX")
+(cd "$W" && "$codex" --profile review -s read-only review --base main < /dev/null > "$tmp" 2>&1) || echo "local-review: codex exited $? (see $out)"
+final=$(awk '/^codex$/{f=1; buf=""; next} f{buf=buf $0 "\n"} END{printf "%s", buf}' "$tmp" | sed "s#$W/##g")
+findings=$(printf '%s\n' "$final" | /usr/bin/grep -E '^- \[P[0-3]\]' | sort -u || true)
+n=$(printf '%s' "$findings" | /usr/bin/grep -c . || true)
+{
+    printf -- '---\ntask: %s\nhead: %s\npr: %s\nbase: %s\nstarted: %s\nfinished: %s\nfindings: %s\nengine: codex review --base main (profile review, read-only)\n---\n\n' "$task" "$head" "$pr" "$base" "$t0" "$(date -u +%FT%TZ)" "$n"
+    printf '%s\n\n' "$findings"
+    echo '```text'
+    printf '%s\n' "$final" | cut -c1-2000
+    echo '```'
+} > "$out"
+rm -f "$tmp"
+printf '%s\n' "$findings"
+echo "local-review: $n findings ($out)"
+[ "$n" = 0 ] || exit 3
diff --git a/scripts/orchestrator/sandbox-scan.sh b/scripts/orchestrator/sandbox-scan.sh
new file mode 100755
index 00000000..de757953
--- /dev/null
+++ b/scripts/orchestrator/sandbox-scan.sh
@@ -0,0 +1,24 @@
+#!/usr/bin/env bash
+# @file sandbox-scan.sh
+# @brief Print the unsandboxed mutation calls of a worker's sandbox record, so a hit is judged before the audit (C-29).
+# @description
+#   Reads `.orchestration/sandboxes/<task>.md`, a trailing `-fixtures` of the task id stripped. A line that names
+#   `dangerouslyDisableSandbox`, `outside the sandbox` or `unsandboxed` and a mutation (`git commit`, `git switch -c`,
+#   `git checkout`, `git add`, `git mv`, `git rm`, `cp `, `mv `, `> `, `tee `) but none of `counts`, `reads`, `lists`,
+#   matched case-insensitively, is printed with its line number, then the judge line; with no such line, one line says
+#   none. A missing record prints nothing.
+# @arg $1 string Task id.
+# @exitcode 0 Always.
+# @example
+#   scripts/orchestrator/sandbox-scan.sh dotfiles-T128-x-a01
+set -euo pipefail
+task=$1
+cd "$(git rev-parse --show-toplevel)"
+sb=".orchestration/sandboxes/${task%-fixtures}.md"
+if [ -f "$sb" ]; then
+    if /usr/bin/grep -n -i -E 'dangerouslyDisableSandbox|outside the sandbox|unsandboxed' "$sb" | /usr/bin/grep -i -E 'git (commit|switch -c|checkout|add|mv|rm)|cp |mv |> |tee ' | /usr/bin/grep -v -i 'counts\|reads\|lists'; then
+        echo "sandbox scan: unsandboxed mutation calls above (C-29); judge before the audit"
+    else
+        echo "sandbox scan: no unsandboxed mutation call in $sb"
+    fi
+fi
diff --git a/tests/unit/test_chain_review_scripts.py b/tests/unit/test_chain_review_scripts.py
new file mode 100644
index 00000000..9295cf9e
--- /dev/null
+++ b/tests/unit/test_chain_review_scripts.py
@@ -0,0 +1,230 @@
+"""Exercise the review-side chain scripts (plan 021 step 6.3) in a temporary git repository.
+
+Each script runs as a subprocess from this checkout with the temporary repository as its working directory, so the
+repository root it resolves is the temporary one. git is the real one. A stub review binary appends its argv, its
+working directory, the HEAD there, PATH and its stdin to `<calls>/<name>.log`, prints `<calls>/transcript` and exits with
+`<calls>/status` (0 when absent).
+"""
+
+import os
+import re
+import subprocess
+import tempfile
+import unittest
+from pathlib import Path
+
+TOOLS = Path(__file__).resolve().parents[2] / "scripts/orchestrator"
+GIT_ENV = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
+STUB = (
+    "#!/usr/bin/env bash\n"
+    '{{ printf "argv:"; printf " %s" "$@"; printf "\\ncwd: %s\\nhead: %s\\npath: %s\\nstdin: %s\\n" '
+    '"$(pwd -P)" "$(git rev-parse HEAD)" "$PATH" "$(cat)"; }} >> "$CALLS/{name}.log"\n'
+    'cat "$CALLS/transcript"\nexit "$(cat "$CALLS/status" 2> /dev/null || echo 0)"\n'
+)
+ARGV = "argv: --profile review -s read-only review --base main"
+SCAN_HIT = "sandbox scan: unsandboxed mutation calls above (C-29); judge before the audit"
+
+
+class ChainReviewScriptsTest(unittest.TestCase):
+    def setUp(self):
+        temp = tempfile.TemporaryDirectory()
+        self.addCleanup(temp.cleanup)
+        self.temp = Path(temp.name).resolve()
+        self.repo = self.temp / "repo"
+        self.calls = self.temp / "calls"
+        self.calls.mkdir()
+        self.git("init", "-q", "-b", "main", str(self.repo), cwd=self.temp)
+        self.write("a.txt", "a\n")
+        self.git("add", "a.txt")
+        self.git("commit", "-q", "-m", "main")
+        self.env = {**os.environ, **GIT_ENV, "CALLS": str(self.calls), "TMPDIR": str(self.temp)}
+        for name in ("CODEX_BIN", "ORCH_REVIEW_WORKTREE"):
+            self.env.pop(name, None)
+
+    def git(self, *args, cwd=None):
+        return subprocess.run(
+            ["git", "-c", "commit.gpgsign=false", *args],
+            cwd=cwd or self.repo,
+            env={**os.environ, **GIT_ENV},
+            capture_output=True,
+            text=True,
+            check=True,
+        ).stdout.strip()
+
+    def write(self, rel, text, root=None):
+        path = (root or self.repo) / rel
+        path.parent.mkdir(parents=True, exist_ok=True)
+        path.write_text(text)
+        return path
+
+    def stub(self, path, name):
+        path.parent.mkdir(parents=True, exist_ok=True)
+        path.write_text(STUB.format(name=name))
+        path.chmod(0o755)
+
+    def log(self, name):
+        path = self.calls / f"{name}.log"
+        return path.read_text() if path.exists() else ""
+
+    def run_tool(self, name, *args, code=0, env=None, cwd=None):
+        # The review binary must not read what the caller's stdin holds.
+        result = subprocess.run(
+            ["bash", str(TOOLS / name), *map(str, args)],
+            capture_output=True,
+            text=True,
+            input="caller stdin\n",
+            cwd=cwd or self.repo,
+            env={**self.env, **(env or {})},
+            timeout=30,
+            check=False,
+        )
+        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
+        return result.stdout
+
+    def test_local_review_runs_the_review_binary_read_only_at_the_head_and_writes_one_file(self):
+        review = self.temp / "review"
+        self.git("worktree", "add", "-q", "--detach", str(review), "main")
+        # The head commit, made in the review worktree, carries a decoy bin/codex; the main working tree never does.
+        self.stub(review / "bin/codex", "decoy")
+        self.write("b.txt", "b\n", root=review)
+        self.git("add", "bin/codex", "b.txt", cwd=review)
+        self.git("commit", "-q", "-m", "head", cwd=review)
+        head, base = self.git("rev-parse", "HEAD", cwd=review), self.git("rev-parse", "main")
+        self.git("checkout", "-q", "--detach", "main", cwd=review)
+        self.stub(self.temp / "bin/codex", "codex")
+        (self.repo / ".orchestration/validation").mkdir(parents=True)
+        path = f"./bin{os.pathsep}{self.temp / 'bin'}{os.pathsep}{os.environ['PATH']}"
+        env = {"ORCH_REVIEW_WORKTREE": str(review), "PATH": path}
+        # An earlier marker's message is not the final one; the worktree prefix is stripped; a repeated line counts once.
+        final = f"One finding.\n- [P2] {review}/b.txt:1 b is new\n- [P2] {review}/b.txt:1 b is new\n"
+        (self.calls / "transcript").write_text(f"codex\n- [P1] {review}/a.txt:1 superseded\ncodex\n{final}")
+        finding = "- [P2] b.txt:1 b is new"
+        call = f"{ARGV}\ncwd: {review}\nhead: {head}\npath: {path}\nstdin: \n"
+
+        def out(task):
+            return self.repo / f".orchestration/validation/{task}-local-review-{head[:7]}.md"
+
+        with self.subTest("a review worktree path without its own .git entry exits 2"):
+            # First, while the main working tree is clean: the dirty check alone would pass it.
+            (self.repo / "plain").mkdir()
+            plain = {**env, "ORCH_REVIEW_WORKTREE": str(self.repo / "plain")}
+            self.assertIn("is not a worktree root", self.run_tool("local-review.sh", "t-p", head, 9, code=2, env=plain))
+            self.assertEqual("", self.log("codex"))
+            self.assertEqual(base, self.git("rev-parse", "HEAD"))
+        with self.subTest("CODEX_BIN unset: codex resolved in the root before the checkout"):
+            stdout = self.run_tool("local-review.sh", "t-a", head, 9, code=3, env=env)
+            self.assertEqual(f"{finding}\nlocal-review: 1 findings ({out('t-a')})\n", stdout)
+            self.assertEqual(call, self.log("codex"))
+            self.assertEqual("", self.log("decoy"))
+            self.assertEqual(head, self.git("rev-parse", "HEAD", cwd=review))
+            status = self.git("status", "--porcelain", "--untracked-files=all")
+            self.assertEqual(f"?? .orchestration/validation/t-a-local-review-{head[:7]}.md", status)
+            text = out("t-a").read_text()
+            front = f"---\ntask: t-a\nhead: {head}\npr: 9\nbase: {base}\nstarted: .+\nfinished: .+\nfindings: 1\n"
+            self.assertRegex(text, "^" + re.escape(front).replace(r"\.\+", ".+"))
+            self.assertIn("engine: codex review --base main (profile review, read-only)\n---\n", text)
+            self.assertIn(f"\n{finding}\n\n```text\nOne finding.\n{finding}\n{finding}\n```\n", text)
+            self.assertNotIn("superseded", text)
+            self.assertEqual([], list(self.temp.glob("local-review.*")))
+        self.git("checkout", "-q", "--detach", "main", cwd=review)
+        with self.subTest("CODEX_BIN set: that binary runs, a relative path resolved in the root"):
+            self.stub(self.repo / "seam/review-binary", "seam")
+            seam = {**env, "CODEX_BIN": "seam/review-binary"}
+            self.run_tool("local-review.sh", "t-b", head, 9, code=3, env=seam, cwd=self.repo / ".orchestration")
+            self.assertEqual(call, self.log("seam"))
+            self.assertEqual(call, self.log("codex"))
+        with self.subTest("one review per head: the file is reused"):
+            stdout = self.run_tool("local-review.sh", "t-a", head, 9, code=3, env=env)
+            self.assertEqual(f"{finding}\nlocal-review: 1 findings (existing {out('t-a')})\n", stdout)
+            self.assertEqual(call, self.log("codex"))
+        (self.calls / "transcript").write_text("codex\nNo findings.\n")
+        (self.calls / "status").write_text("5")
+        with self.subTest("no finding exits 0, also when the binary fails"):
+            stdout = self.run_tool("local-review.sh", "t-c", head, 9, env=env)
+            file = out("t-c")
+            self.assertEqual(
+                f"local-review: codex exited 5 (see {file})\n\nlocal-review: 0 findings ({file})\n", stdout
+            )
+            self.assertIn("findings: 0\n", out("t-c").read_text())
+        missing = {**env, "CODEX_BIN": "seam/missing"}
+        self.assertIn("no review binary", self.run_tool("local-review.sh", "t-d", head, 9, code=2, env=missing))
+        self.write("dirty.txt", "x\n", root=review)
+        with self.subTest("a dirty review worktree or an unknown head exits 2 and runs nothing"):
+            self.assertIn("is not clean", self.run_tool("local-review.sh", "t-d", head, 9, code=2, env=env))
+            unknown = "0" * 40
+            self.assertIn("is not a local commit", self.run_tool("local-review.sh", "t-d", unknown, 9, code=2, env=env))
+            self.assertEqual(2, self.log("codex").count(ARGV))
+            self.assertFalse(out("t-d").exists())
+
+    def test_local_advisory_records_p2_rows_and_stops_on_p0_p1(self):
+        head, owner = "abcdef0" + "1" * 33, "t-followup-a01"
+        record = self.write(".orchestration/acceptance/t-a01.md", "# record\n")
+        heading = f"## Owned by {owner} (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)\n"
+        # Numbered in sort order; the second is cut to 120 characters, then loses its backticks.
+        first, long = "- [P2] `a.sh:1` first", "- [P2] `b.sh:3` " + "y" * 130
+
+        def review(*findings):
+            front = f"---\ntask: t-a01\nfindings: {len(findings)}\n---\n\n"
+            # Each finding appears twice, in the list and in the transcript, as the local review writes it.
+            text = "\n".join(findings)
+            self.write(f".orchestration/validation/t-a01-local-review-{head[:7]}.md", f"{front}{text}\n\n{text}\n")
+
+        def line(n, finding):
+            text = finding[:120].replace("`", "")
+            return (
+                f"local-finding: abcdef0:{n} not-applicable:advisory P2 owned by {owner} ({text}); "
+                f"evidence=git show origin/main:.orchestration/tasks/{owner}.md | grep -n 'item 1'\n"
+            )
+
+        review(long, first)
+        for _ in range(2):
+            stdout = self.run_tool("local-advisory.sh", "t-a01", head, owner)
+        self.assertEqual(
+            f"local review of abcdef0: 2 finding(s) recorded as advisory under 'Owned by {owner}' in .orchestration/acceptance/t-a01.md\n",
+            stdout,
+        )
+        rows = "local:abcdef0:1\tadvisory-p2\n" + line(1, first)
+        rows += "local:abcdef0:2\tadvisory-p2\n" + line(2, long)
+        self.assertEqual(f"# record\n\n{heading}\n{rows}", record.read_text())
+        record.write_text("# record\n")
+        review("- [P1] a.sh:1 blocks", "- [P2] b.sh:2 second")
+        stdout = self.run_tool("local-advisory.sh", "t-a01", head, owner, code=3)
+        self.assertIn("STOP: local finding 1 of abcdef0 is P0/P1: - [P1] a.sh:1 blocks\n", stdout)
+        rows = "local:abcdef0:2\tadvisory-p2\n" + line(2, "- [P2] b.sh:2 second")
+        self.assertEqual(f"# record\n\n{heading}\n{rows}", record.read_text())
+        record.write_text("# record\n")
+        review("- [P0] c.sh:1 breaks")
+        stdout = self.run_tool("local-advisory.sh", "t-a01", head, owner, code=3)
+        self.assertIn("STOP: local finding 1 of abcdef0 is P0/P1: - [P0] c.sh:1 breaks\n", stdout)
+        self.assertEqual(f"# record\n\n{heading}\n", record.read_text())
+        record.write_text("# record\n")
+        review()
+        self.assertEqual(
+            "local review of abcdef0: no findings\n", self.run_tool("local-advisory.sh", "t-a01", head, owner)
+        )
+        self.assertEqual("# record\n", record.read_text())
+        self.assertIn("no local review file", self.run_tool("local-advisory.sh", "t-b01", head, owner, code=2))
+
+    def test_sandbox_scan_prints_the_unsandboxed_mutation_calls(self):
+        sandboxes = ".orchestration/sandboxes"
+        hit = "| 2 | dangerouslyDisableSandbox: git commit -m wip |"
+        self.write(
+            f"{sandboxes}/t-a01.md", f"# sandbox\n{hit}\n- The unsandboxed table Counts every git commit > log.\n"
+        )
+        self.assertEqual(f"2:{hit}\n{SCAN_HIT}\n", self.run_tool("sandbox-scan.sh", "t-a01"))
+        # A trailing -fixtures is stripped, and the match ignores case.
+        self.write(f"{sandboxes}/t-b01.md", "Outside The Sandbox: GIT ADD x\n")
+        self.assertEqual(
+            f"1:Outside The Sandbox: GIT ADD x\n{SCAN_HIT}\n", self.run_tool("sandbox-scan.sh", "t-b01-fixtures")
+        )
+        reads = (
+            "| 1 | gh pr view 9 > pr.json (outside the sandbox; reads) |\n| 2 | unsandboxed tee log, lists the PRs |\n"
+        )
+        self.write(f"{sandboxes}/t-c01.md", reads)
+        none = f"sandbox scan: no unsandboxed mutation call in {sandboxes}/t-c01.md\n"
+        self.assertEqual(none, self.run_tool("sandbox-scan.sh", "t-c01"))
+        self.assertEqual("", self.run_tool("sandbox-scan.sh", "t-d01"))
+
+
+if __name__ == "__main__":
+    unittest.main()

 succeeded in 226ms:
LOCAL TASK
---
format: 2
task_id: dotfiles-T128-chain-review-scripts-a01
kind: code
security: false
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - scripts/orchestrator/local-review.sh
  - scripts/orchestrator/local-advisory.sh
  - scripts/orchestrator/sandbox-scan.sh
  - tests/unit/test_chain_review_scripts.py
  - .orchestration/dotfiles-T128-chain-review-scripts-a01/**
after: [dotfiles-T128-gate-wrapper-path-a01]
threat_table:
  - control: the PR adds scripts/orchestrator/local-review.sh, which checks the review worktree out at a PR head and runs the review binary there read-only, writing one validation file
    disposition: "closed: tests/unit/test_chain_review_scripts.py::test_local_review_runs_the_review_binary_read_only_at_the_head_and_writes_one_file"
  - control: the PR adds scripts/orchestrator/local-advisory.sh, which appends advisory rows and local-finding lines to an acceptance record and stops on a P0 or P1
    disposition: "closed: tests/unit/test_chain_review_scripts.py::test_local_advisory_records_p2_rows_and_stops_on_p0_p1"
  - control: the PR adds scripts/orchestrator/sandbox-scan.sh, which prints the unsandboxed mutation calls of a worker sandbox record
    disposition: "closed: tests/unit/test_chain_review_scripts.py::test_sandbox_scan_prints_the_unsandboxed_mutation_calls"
  - control: the PR adds tests/unit/test_chain_review_scripts.py, the oracle of the three rows above (a stub review binary on CODEX_BIN that records argv, cwd and environment and prints a canned transcript; a temporary git repository with a main branch and a head commit as the review worktree; fixture texts the tests write)
    disposition: "residual: the stubs record and print, nothing else; the audit reads each case against the Files items"
  - control: "the review worktree (the path ORCH_REVIEW_WORKTREE names when set, else <root>/.claude/worktrees/orchestrator-review): local-review.sh refuses with exit 2 a path that is not a worktree root (no .git entry at the path itself, so git -C cannot fall through to an enclosing checkout) and a dirty one, checks the head out detached and restores nothing (the chain's audit wrapper restores it)"
    disposition: "residual: the orchestrator's own worktree, detached at origin/main between runs; both refusals are covered by the first closed row's cases (amendment 1 adds the non-worktree case); the restore belongs to orch-audit.sh on main"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T128-chain-review-scripts-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T128-chain-review-scripts-a01/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the tests run the three scripts as subprocesses with the stub review binary on CODEX_BIN and real git in a temporary repository, and import only the standard library; nothing is imported into another process"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; local-review.sh runs git, mktemp and the review binary (the value of CODEX_BIN when the environment sets it, the test seam, else codex resolved with command -v in the repository root before the head checkout, its absolute path used afterwards; the profile review is fixed in the script, the model-selection rule); local-review.sh also runs awk, sed, date, cut, grep, sort, head and rm; local-advisory.sh runs git rev-parse, grep, sed, cut, tr, head and sort; sandbox-scan.sh runs git rev-parse and grep; the review binary runs with the PR head as its working directory under its own read-only sandbox, so the PR's content (its AGENTS.md, its configuration files) is input to that review and never to the gate: the review's findings are a sample the orchestrator judges (advisory rows or a stop), and the script writes nothing but the validation file"
  - control: new or renamed scripts
    disposition: "residual: three new scripts under scripts/orchestrator/, named in allowed_files and listed in the RESULT; any other new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: 'none of the three script names exists under scripts/orchestrator/ on origin/main (the task adds, it does not edit)'
    command: 'git ls-tree --name-only origin/main scripts/orchestrator/ | /usr/bin/grep -c -E "local-review|local-advisory|sandbox-scan" || true'
    output: |-
      0
---

# AGMSG-TASK dotfiles-T128-chain-review-scripts-a01 — the integration chain's review-side steps become repository scripts with tests (plan 021 step 6.3; the review half of the step's "next tools task")

Drafted 2026-10-14 by the orchestrator seat (the bus time of its TASK line is the dispatch time), in the step-7 short form. Plan 021's step 6.3 inventory names six chain steps whose logic lives only in the orchestrator's scratchpad; the hand-typed-chain class holds fourteen mistake records today, and the structural answer is repository scripts with tests. This task lands the three review-side scripts; its sibling `dotfiles-T128-chain-github-scripts-a01` lands the two GitHub-side scripts (`resolve-threads.sh`, `pr-cost.sh`) with its own test module, so the two run concurrently on disjoint files. The attached inputs under `.orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/` of the orchestrator's main checkout (the directory the TASK line's `task_file` is read from, untracked until the next boundary) are the scripts as the chain runs them today, with the repository root resolved by `git rev-parse --show-toplevel`; their sha256 prefixes (`shasum -a 256 <dir>/*.sh | cut -c1-16`): 2e44dabc23ea0397  local-advisory.sh; 2258e370b9ff2575  local-review.sh; 099f6c7534223cb4  sandbox-scan.sh; each item names what changes. The one premise is replayable from any checkout (it reads `origin/main`).

## Goal

The local review of a PR head, the recording of its advisory findings and the scan of a worker's sandbox record run from `scripts/orchestrator/` on `origin/main`, each with one test that closes its row, so the next integration's log names repository scripts for these steps.

## Files

1. `scripts/orchestrator/local-review.sh <task> <head> <pr>`: the input's behaviour (one review per head: an existing `.orchestration/validation/<task>-local-review-<sha7>.md` is reused and re-reported with its finding lines and `local-review: <n> findings (existing <file>)`; otherwise the head must be a local commit, exit 2 if not; the review worktree path must hold a `.git` entry of its own (a worktree root; a plain directory inside a checkout would let `git -C` act on the enclosing checkout), exit 2 if not, and be clean, exit 2 if not; the worktree is checked out detached at the head; the review binary runs there as `<binary> --profile review -s read-only review --base main` with stdin from `/dev/null`; the transcript's final message after the `codex` marker line is kept with the worktree prefix stripped; the unique lines matching `^- \[P[0-3]\]` are the findings; the file gets the front matter the input writes: task, head, pr, base, started, finished, findings, engine; the findings are printed, then `local-review: <n> findings (<file>)`; a non-zero exit of the review binary prints `local-review: codex exited <n> (see <file>)` and the file is still written from whatever transcript came back; exit 0 with no finding, 3 with findings, 2 on a precondition) with these changes: the repository root is `git rev-parse --show-toplevel`; the review worktree is `$ORCH_REVIEW_WORKTREE` when set, else `<root>/.claude/worktrees/orchestrator-review`; the review binary is `$CODEX_BIN` when set, else `codex` resolved with `command -v` in the repository root before the checkout and used by that absolute path afterwards; the profile `review` stays fixed in the script; the transcript's temporary file comes from `mktemp` with the template `${TMPDIR:-/tmp}/local-review.XXXXXX` (macOS `mktemp` without a template ignores `TMPDIR` and uses the per-user directory, which the Bash sandbox denies; the form `orch-gate.sh` uses); an shdoc header; `bash -n` and shellcheck clean.
2. `scripts/orchestrator/local-advisory.sh <task> <head40> <owner-task-id>`: the input's behaviour (reads `.orchestration/validation/<task>-local-review-<sha7>.md`, exit 2 when absent; `findings: 0` prints `local review of <sha7>: no findings` and exits 0; otherwise ensures the heading `## Owned by <owner> (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)` in `.orchestration/acceptance/<task>.md`; then for each unique finding line in order, numbered from 1: a `[P0]` or `[P1]` prints `STOP: local finding <n> of <sha7> is P0/P1: <line>` and makes the exit 3, any other appends the row `local:<sha7>:<n><TAB>advisory-p2` and the line `local-finding: <sha7>:<n> not-applicable:advisory P2 owned by <owner> (<the finding's first 120 characters, backticks removed>); evidence=git show origin/main:.orchestration/tasks/<owner>.md | grep -n 'item 1'`, each only when the record lacks it; last line `local review of <sha7>: <i> finding(s) recorded as advisory under 'Owned by <owner>' in <record>`) with the repository root from `git rev-parse --show-toplevel` and an shdoc header.
3. `scripts/orchestrator/sandbox-scan.sh <task>`: the input's behaviour (over `.orchestration/sandboxes/<task>.md`, where a trailing `-fixtures` of `<task>` is stripped as the input does with `${task%-fixtures}`: the lines matching, case-insensitively as the input's `grep -i` does, `dangerouslyDisableSandbox`, `outside the sandbox` or `unsandboxed` that also match a mutation, `git commit`, `git switch -c`, `git checkout`, `git add`, `git mv`, `git rm`, `cp `, `mv `, `> ` or `tee `, and none of `counts`, `reads`, `lists`, printed with their line numbers followed by `sandbox scan: unsandboxed mutation calls above (C-29); judge before the audit`; with no such line, `sandbox scan: no unsandboxed mutation call in <record>`; a missing record prints nothing; exit 0 in every case) with the repository root from `git rev-parse --show-toplevel` and an shdoc header.
4. `tests/unit/test_chain_review_scripts.py` (new), run by `uv run python -m unittest` without PyYAML, importing only the standard library, each test in a temporary directory holding a git repository with a `main` branch, a head commit and a second worktree for the review:
   - `test_local_review_runs_the_review_binary_read_only_at_the_head_and_writes_one_file`: the review worktree is a second worktree of the temporary repository created outside the repository root and named by `ORCH_REVIEW_WORKTREE`; a stub review binary records its argv, its working directory and `PATH` to a log and prints a transcript with a `codex` marker line followed by one `- [P2] …` finding. Case one, `CODEX_BIN` unset: the stub is `codex` in an absolute directory on PATH, PATH also holds the relative entry `./bin` before it, and the head commit (not the root's working tree) contains `bin/codex`, a decoy that logs to a second file; the test asserts the stub's log holds the call with the argv (`--profile review -s read-only review --base main`) and the working directory (the review worktree, whose HEAD is the given head), the decoy's log is empty (the binary was resolved in the repository root before the checkout and run by its absolute path), the repository's main working tree gained no path but the validation file (`git status --porcelain` there lists only it), the file holds the front matter and the finding, the exit is 3 with the finding line and the summary line printed. Case two, `CODEX_BIN` set to the stub: the same assertions on argv and working directory. Then: a second run on the same task and head does not run the stub (its log unchanged) and exits 3 again; a run under a second task name with a transcript of no finding exits 0; a dirty review worktree exits 2 with the stub's log unchanged; `ORCH_REVIEW_WORKTREE` naming a plain directory created inside the repository's main working tree (no `.git` entry of its own) exits 2 with the stub's log unchanged and the main working tree's HEAD unmoved.
   - `test_local_advisory_records_p2_rows_and_stops_on_p0_p1`: with a local-review file of two P2 findings, the record gains the heading, two rows and two lines once across two runs; with a P1 finding first and a P2 second, the STOP line is printed, the exit is 3, the P2's row and line are appended and the P1 gets none; with `findings: 0` nothing is appended and the exit is 0; with no file the exit is 2.
   - `test_sandbox_scan_prints_the_unsandboxed_mutation_calls`: a sandbox record with one `dangerouslyDisableSandbox … git commit` line and one `unsandboxed … counts` line prints the first with its line number and the judge line; a record with reads only prints the no-hit line; a missing record prints nothing; each exits 0.

## Out of scope

The GitHub-side scripts (the sibling task), the chain glue (`integrate-pr.sh`, `finish-pr.sh`; it stays outside the repository until every step it calls is a repository script, plan 021 step 6.3), `orch-audit.sh`, `orch-gate.sh`, `acceptance-front-matter.py`, `dispatch.sh`, any rule text, the Makefile.

## Check

`uv run python -m unittest tests/unit/test_chain_review_scripts.py -v` green, pasted in the validation file with `shellcheck scripts/orchestrator/local-review.sh scripts/orchestrator/local-advisory.sh scripts/orchestrator/sandbox-scan.sh` and `git diff --numstat origin/main...HEAD`: at most 200 changed lines (added plus deleted) outside `tests/` and outside `.orchestration/` (plan 021 step 7.2) and 1000 added lines under `tests/` (INV-2).

## Completion

One PR from a fresh branch off `origin/main` (after PR #355, merged 08:27Z as 5ec86052), pairwise-disjoint from the sibling task's files (`scripts/orchestrator/resolve-threads.sh`, `pr-cost.sh`, `tests/unit/test_chain_github_scripts.py`, its evidence directory). The PR is ready for the orchestrator's integration when the ruleset's required checks are green, the Bot's single review (on PR open) is in, every Bot thread is replied to and resolved by the orchestrator with its disposition, the validation file carries the Check's outputs, and the RESULT names every P0/P1 thread with `fixed:<sha>` and every P2 as advisory; the orchestrator's audit of the final head is dispositioned finding by finding before the gate, and a P0/P1 it leaves is the operator's decision. The Bot reviews once, at PR open; its P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P0 or P1 that survives the round stops the PR and goes to the operator as a decision; a P2 on this PR is advisory, owned by `dotfiles-T128-chain-review-scripts-followup-a01`, which the orchestrator writes when the first advisory P2 appears, before the PR's dispositions, and recorded under `## Owned by dotfiles-T128-chain-review-scripts-followup-a01` in this task's acceptance record. The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`. The RESULT names head, base, branch, files, every Bot thread with its disposition, the three test names, the caps, `task_copy=<sha256 of .orchestration/dotfiles-T128-chain-review-scripts-a01/task.md>` and the evidence paths.

## Change (round 2, 2026-10-14)

The Codex half's round 1: premise 3 counted a phrase across the whole plan file, which the orchestrator's own status line of 08:45Z changed from 8 to 9 within minutes; the premise now counts inside the step 6.3 inventory section only. Item 3 said `<task>.md` where the input reads `${task%-fixtures}.md`; the item now states the input's suffix stripping. The sibling task dropped `review-receipt.sh` (the inventory keeps the receipt as glue), so the sibling file list here names two scripts.

## Change (round 3, 2026-10-14)

The seat's round 1 (on the round-1 hash): premises 1 and 3 read untracked files of the orchestrator's checkout (the inputs, plan 021's inventory) that a worker replaying from its worktree on `origin/main` cannot see, so they are removed and the one premise left reads `origin/main`; the inputs' hashes are stated in the intro as facts. Item 4's first test gains the case that closes the row's resolution claim: `CODEX_BIN` unset, a relative `./bin` on PATH whose `codex` decoy exists only in the head commit, the decoy's log empty; the review worktree sits outside the repository root and the no-new-path assertion is on the main working tree; the no-finding run uses a second task name. Item 1 states the input's continuation on a non-zero review-binary exit; item 3 states the case-insensitive match; row 11 lists the tools each script runs.

## Change (amendment 1, 2026-10-14 09:05Z)

Why: the worker's question (bus 1149, 09:02:17Z): row 11 listed a subset of the tools the inputs run; and a review worktree path that is an existing directory but not a worktree root makes `git -C` fall through to the enclosing checkout, so a clean main checkout would pass the dirty check and be checked out detached at the PR head. What changed: row 11 lists the tools each input runs; item 1 requires the worktree path to hold its own `.git` entry (exit 2 otherwise) before the dirty check; the first test gains that case (a plain directory inside the main working tree: exit 2, the stub not run, the main HEAD unmoved); row 5 names both refusals. Nothing else. Round 2 (09:08Z, the worker's PONG of 09:05Z): item 1 also names the `mktemp` template `${TMPDIR:-/tmp}/local-review.XXXXXX`, a change to the input's behaviour the worker had to make under the sandbox.


BRANCH .orchestration/dotfiles-T128-chain-review-scripts-a01/task.md
1: ---
2: format: 2
3: task_id: dotfiles-T128-chain-review-scripts-a01
4: kind: code
5: security: false
6: design_review:
7:   receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
8:   design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
9: allowed_files:
10:   - scripts/orchestrator/local-review.sh
11:   - scripts/orchestrator/local-advisory.sh
12:   - scripts/orchestrator/sandbox-scan.sh
13:   - tests/unit/test_chain_review_scripts.py
14:   - .orchestration/dotfiles-T128-chain-review-scripts-a01/**
15: after: [dotfiles-T128-gate-wrapper-path-a01]
16: threat_table:
17:   - control: the PR adds scripts/orchestrator/local-review.sh, which checks the review worktree out at a PR head and runs the review binary there read-only, writing one validation file
18:     disposition: "closed: tests/unit/test_chain_review_scripts.py::test_local_review_runs_the_review_binary_read_only_at_the_head_and_writes_one_file"
19:   - control: the PR adds scripts/orchestrator/local-advisory.sh, which appends advisory rows and local-finding lines to an acceptance record and stops on a P0 or P1
20:     disposition: "closed: tests/unit/test_chain_review_scripts.py::test_local_advisory_records_p2_rows_and_stops_on_p0_p1"
21:   - control: the PR adds scripts/orchestrator/sandbox-scan.sh, which prints the unsandboxed mutation calls of a worker sandbox record
22:     disposition: "closed: tests/unit/test_chain_review_scripts.py::test_sandbox_scan_prints_the_unsandboxed_mutation_calls"
23:   - control: the PR adds tests/unit/test_chain_review_scripts.py, the oracle of the three rows above (a stub review binary on CODEX_BIN that records argv, cwd and environment and prints a canned transcript; a temporary git repository with a main branch and a head commit as the review worktree; fixture texts the tests write)
24:     disposition: "residual: the stubs record and print, nothing else; the audit reads each case against the Files items"
25:   - control: "the review worktree (the path ORCH_REVIEW_WORKTREE names when set, else <root>/.claude/worktrees/orchestrator-review): local-review.sh refuses with exit 2 a path that is not a worktree root (no .git entry at the path itself, so git -C cannot fall through to an enclosing checkout) and a dirty one, checks the head out detached and restores nothing (the chain's audit wrapper restores it)"
26:     disposition: "residual: the orchestrator's own worktree, detached at origin/main between runs; both refusals are covered by the first closed row's cases (amendment 1 adds the non-worktree case); the restore belongs to orch-audit.sh on main"
27:   - control: the task-file copy on the branch (.orchestration/dotfiles-T128-chain-review-scripts-a01/task.md)
28:     disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
29:   - control: the branch evidence records under .orchestration/dotfiles-T128-chain-review-scripts-a01/ (report.md, validation.md, sandbox.md, learning.md)
30:     disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
31:   - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
32:     disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
33:   - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
34:     disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
35:   - control: in-process effects
36:     disposition: "residual: the tests run the three scripts as subprocesses with the stub review binary on CODEX_BIN and real git in a temporary repository, and import only the standard library; nothing is imported into another process"
37:   - control: workflow and interpreter or environment inputs
38:     disposition: "residual: no workflow or interpreter file is in allowed_files; local-review.sh runs git, mktemp and the review binary (the value of CODEX_BIN when the environment sets it, the test seam, else codex resolved with command -v in the repository root before the head checkout, its absolute path used afterwards; the profile review is fixed in the script, the model-selection rule); local-review.sh also runs awk, sed, date, cut, grep, sort, head and rm; local-advisory.sh runs git rev-parse, grep, sed, cut, tr, head and sort; sandbox-scan.sh runs git rev-parse and grep; the review binary runs with the PR head as its working directory under its own read-only sandbox, so the PR's content (its AGENTS.md, its configuration files) is input to that review and never to the gate: the review's findings are a sample the orchestrator judges (advisory rows or a stop), and the script writes nothing but the validation file"
39:   - control: new or renamed scripts
40:     disposition: "residual: three new scripts under scripts/orchestrator/, named in allowed_files and listed in the RESULT; any other new or renamed script is an undeclared change the audit fails"
41:   - control: orchestrator effect merge
42:     disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
43:   - control: orchestrator effect update-branch
44:     disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
45:   - control: orchestrator effect forced worker removal
46:     disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
47: premises:
48:   - claim: 'none of the three script names exists under scripts/orchestrator/ on origin/main (the task adds, it does not edit)'
49:     command: 'git ls-tree --name-only origin/main scripts/orchestrator/ | /usr/bin/grep -c -E "local-review|local-advisory|sandbox-scan" || true'
50:     output: |-
51:       0
52: ---
53: 
54: # AGMSG-TASK dotfiles-T128-chain-review-scripts-a01 — the integration chain's review-side steps become repository scripts with tests (plan 021 step 6.3; the review half of the step's "next tools task")
55: 
56: Drafted 2026-10-14 by the orchestrator seat (the bus time of its TASK line is the dispatch time), in the step-7 short form. Plan 021's step 6.3 inventory names six chain steps whose logic lives only in the orchestrator's scratchpad; the hand-typed-chain class holds fourteen mistake records today, and the structural answer is repository scripts with tests. This task lands the three review-side scripts; its sibling `dotfiles-T128-chain-github-scripts-a01` lands the two GitHub-side scripts (`resolve-threads.sh`, `pr-cost.sh`) with its own test module, so the two run concurrently on disjoint files. The attached inputs under `.orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/` of the orchestrator's main checkout (the directory the TASK line's `task_file` is read from, untracked until the next boundary) are the scripts as the chain runs them today, with the repository root resolved by `git rev-parse --show-toplevel`; their sha256 prefixes (`shasum -a 256 <dir>/*.sh | cut -c1-16`): 2e44dabc23ea0397  local-advisory.sh; 2258e370b9ff2575  local-review.sh; 099f6c7534223cb4  sandbox-scan.sh; each item names what changes. The one premise is replayable from any checkout (it reads `origin/main`).
57: 
58: ## Goal
59: 
60: The local review of a PR head, the recording of its advisory findings and the scan of a worker's sandbox record run from `scripts/orchestrator/` on `origin/main`, each with one test that closes its row, so the next integration's log names repository scripts for these steps.
61: 
62: ## Files
63: 
64: 1. `scripts/orchestrator/local-review.sh <task> <head> <pr>`: the input's behaviour (one review per head: an existing `.orchestration/validation/<task>-local-review-<sha7>.md` is reused and re-reported with its finding lines and `local-review: <n> findings (existing <file>)`; otherwise the head must be a local commit, exit 2 if not; the review worktree path must hold a `.git` entry of its own (a worktree root; a plain directory inside a checkout would let `git -C` act on the enclosing checkout), exit 2 if not, and be clean, exit 2 if not; the worktree is checked out detached at the head; the review binary runs there as `<binary> --profile review -s read-only review --base main` with stdin from `/dev/null`; the transcript's final message after the `codex` marker line is kept with the worktree prefix stripped; the unique lines matching `^- \[P[0-3]\]` are the findings; the file gets the front matter the input writes: task, head, pr, base, started, finished, findings, engine; the findings are printed, then `local-review: <n> findings (<file>)`; a non-zero exit of the review binary prints `local-review: codex exited <n> (see <file>)` and the file is still written from whatever transcript came back; exit 0 with no finding, 3 with findings, 2 on a precondition) with these changes: the repository root is `git rev-parse --show-toplevel`; the review worktree is `$ORCH_REVIEW_WORKTREE` when set, else `<root>/.claude/worktrees/orchestrator-review`; the review binary is `$CODEX_BIN` when set, else `codex` resolved with `command -v` in the repository root before the checkout and used by that absolute path afterwards; the profile `review` stays fixed in the script; the transcript's temporary file comes from `mktemp` with the template `${TMPDIR:-/tmp}/local-review.XXXXXX` (macOS `mktemp` without a template ignores `TMPDIR` and uses the per-user directory, which the Bash sandbox denies; the form `orch-gate.sh` uses); an shdoc header; `bash -n` and shellcheck clean.
65: 2. `scripts/orchestrator/local-advisory.sh <task> <head40> <owner-task-id>`: the input's behaviour (reads `.orchestration/validation/<task>-local-review-<sha7>.md`, exit 2 when absent; `findings: 0` prints `local review of <sha7>: no findings` and exits 0; otherwise ensures the heading `## Owned by <owner> (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)` in `.orchestration/acceptance/<task>.md`; then for each unique finding line in order, numbered from 1: a `[P0]` or `[P1]` prints `STOP: local finding <n> of <sha7> is P0/P1: <line>` and makes the exit 3, any other appends the row `local:<sha7>:<n><TAB>advisory-p2` and the line `local-finding: <sha7>:<n> not-applicable:advisory P2 owned by <owner> (<the finding's first 120 characters, backticks removed>); evidence=git show origin/main:.orchestration/tasks/<owner>.md | grep -n 'item 1'`, each only when the record lacks it; last line `local review of <sha7>: <i> finding(s) recorded as advisory under 'Owned by <owner>' in <record>`) with the repository root from `git rev-parse --show-toplevel` and an shdoc header.
66: 3. `scripts/orchestrator/sandbox-scan.sh <task>`: the input's behaviour (over `.orchestration/sandboxes/<task>.md`, where a trailing `-fixtures` of `<task>` is stripped as the input does with `${task%-fixtures}`: the lines matching, case-insensitively as the input's `grep -i` does, `dangerouslyDisableSandbox`, `outside the sandbox` or `unsandboxed` that also match a mutation, `git commit`, `git switch -c`, `git checkout`, `git add`, `git mv`, `git rm`, `cp `, `mv `, `> ` or `tee `, and none of `counts`, `reads`, `lists`, printed with their line numbers followed by `sandbox scan: unsandboxed mutation calls above (C-29); judge before the audit`; with no such line, `sandbox scan: no unsandboxed mutation call in <record>`; a missing record prints nothing; exit 0 in every case) with the repository root from `git rev-parse --show-toplevel` and an shdoc header.
67: 4. `tests/unit/test_chain_review_scripts.py` (new), run by `uv run python -m unittest` without PyYAML, importing only the standard library, each test in a temporary directory holding a git repository with a `main` branch, a head commit and a second worktree for the review:
68:    - `test_local_review_runs_the_review_binary_read_only_at_the_head_and_writes_one_file`: the review worktree is a second worktree of the temporary repository created outside the repository root and named by `ORCH_REVIEW_WORKTREE`; a stub review binary records its argv, its working directory and `PATH` to a log and prints a transcript with a `codex` marker line followed by one `- [P2] …` finding. Case one, `CODEX_BIN` unset: the stub is `codex` in an absolute directory on PATH, PATH also holds the relative entry `./bin` before it, and the head commit (not the root's working tree) contains `bin/codex`, a decoy that logs to a second file; the test asserts the stub's log holds the call with the argv (`--profile review -s read-only review --base main`) and the working directory (the review worktree, whose HEAD is the given head), the decoy's log is empty (the binary was resolved in the repository root before the checkout and run by its absolute path), the repository's main working tree gained no path but the validation file (`git status --porcelain` there lists only it), the file holds the front matter and the finding, the exit is 3 with the finding line and the summary line printed. Case two, `CODEX_BIN` set to the stub: the same assertions on argv and working directory. Then: a second run on the same task and head does not run the stub (its log unchanged) and exits 3 again; a run under a second task name with a transcript of no finding exits 0; a dirty review worktree exits 2 with the stub's log unchanged; `ORCH_REVIEW_WORKTREE` naming a plain directory created inside the repository's main working tree (no `.git` entry of its own) exits 2 with the stub's log unchanged and the main working tree's HEAD unmoved.
69:    - `test_local_advisory_records_p2_rows_and_stops_on_p0_p1`: with a local-review file of two P2 findings, the record gains the heading, two rows and two lines once across two runs; with a P1 finding first and a P2 second, the STOP line is printed, the exit is 3, the P2's row and line are appended and the P1 gets none; with `findings: 0` nothing is appended and the exit is 0; with no file the exit is 2.
70:    - `test_sandbox_scan_prints_the_unsandboxed_mutation_calls`: a sandbox record with one `dangerouslyDisableSandbox … git commit` line and one `unsandboxed … counts` line prints the first with its line number and the judge line; a record with reads only prints the no-hit line; a missing record prints nothing; each exits 0.
71: 
72: ## Out of scope
73: 
74: The GitHub-side scripts (the sibling task), the chain glue (`integrate-pr.sh`, `finish-pr.sh`; it stays outside the repository until every step it calls is a repository script, plan 021 step 6.3), `orch-audit.sh`, `orch-gate.sh`, `acceptance-front-matter.py`, `dispatch.sh`, any rule text, the Makefile.
75: 
76: ## Check
77: 
78: `uv run python -m unittest tests/unit/test_chain_review_scripts.py -v` green, pasted in the validation file with `shellcheck scripts/orchestrator/local-review.sh scripts/orchestrator/local-advisory.sh scripts/orchestrator/sandbox-scan.sh` and `git diff --numstat origin/main...HEAD`: at most 200 changed lines (added plus deleted) outside `tests/` and outside `.orchestration/` (plan 021 step 7.2) and 1000 added lines under `tests/` (INV-2).
79: 
80: ## Completion
81: 
82: One PR from a fresh branch off `origin/main` (after PR #355, merged 08:27Z as 5ec86052), pairwise-disjoint from the sibling task's files (`scripts/orchestrator/resolve-threads.sh`, `pr-cost.sh`, `tests/unit/test_chain_github_scripts.py`, its evidence directory). The PR is ready for the orchestrator's integration when the ruleset's required checks are green, the Bot's single review (on PR open) is in, every Bot thread is replied to and resolved by the orchestrator with its disposition, the validation file carries the Check's outputs, and the RESULT names every P0/P1 thread with `fixed:<sha>` and every P2 as advisory; the orchestrator's audit of the final head is dispositioned finding by finding before the gate, and a P0/P1 it leaves is the operator's decision. The Bot reviews once, at PR open; its P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P0 or P1 that survives the round stops the PR and goes to the operator as a decision; a P2 on this PR is advisory, owned by `dotfiles-T128-chain-review-scripts-followup-a01`, which the orchestrator writes when the first advisory P2 appears, before the PR's dispositions, and recorded under `## Owned by dotfiles-T128-chain-review-scripts-followup-a01` in this task's acceptance record. The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`. The RESULT names head, base, branch, files, every Bot thread with its disposition, the three test names, the caps, `task_copy=<sha256 of .orchestration/dotfiles-T128-chain-review-scripts-a01/task.md>` and the evidence paths.
83: 
84: ## Change (round 2, 2026-10-14)
85: 
86: The Codex half's round 1: premise 3 counted a phrase across the whole plan file, which the orchestrator's own status line of 08:45Z changed from 8 to 9 within minutes; the premise now counts inside the step 6.3 inventory section only. Item 3 said `<task>.md` where the input reads `${task%-fixtures}.md`; the item now states the input's suffix stripping. The sibling task dropped `review-receipt.sh` (the inventory keeps the receipt as glue), so the sibling file list here names two scripts.
87: 
88: ## Change (round 3, 2026-10-14)
89: 
90: The seat's round 1 (on the round-1 hash): premises 1 and 3 read untracked files of the orchestrator's checkout (the inputs, plan 021's inventory) that a worker replaying from its worktree on `origin/main` cannot see, so they are removed and the one premise left reads `origin/main`; the inputs' hashes are stated in the intro as facts. Item 4's first test gains the case that closes the row's resolution claim: `CODEX_BIN` unset, a relative `./bin` on PATH whose `codex` decoy exists only in the head commit, the decoy's log empty; the review worktree sits outside the repository root and the no-new-path assertion is on the main working tree; the no-finding run uses a second task name. Item 1 states the input's continuation on a non-zero review-binary exit; item 3 states the case-insensitive match; row 11 lists the tools each script runs.
91: 
92: ## Change (amendment 1, 2026-10-14 09:05Z)
93: 
94: Why: the worker's question (bus 1149, 09:02:17Z): row 11 listed a subset of the tools the inputs run; and a review worktree path that is an existing directory but not a worktree root makes `git -C` fall through to the enclosing checkout, so a clean main checkout would pass the dirty check and be checked out detached at the PR head. What changed: row 11 lists the tools each input runs; item 1 requires the worktree path to hold its own `.git` entry (exit 2 otherwise) before the dirty check; the first test gains that case (a plain directory inside the main working tree: exit 2, the stub not run, the main HEAD unmoved); row 5 names both refusals. Nothing else. Round 2 (09:08Z, the worker's PONG of 09:05Z): item 1 also names the `mktemp` template `${TMPDIR:-/tmp}/local-review.XXXXXX`, a change to the input's behaviour the worker had to make under the sandbox.

 succeeded in 240ms:
meta {
  "lastAnalyzedAt": "2026-10-02T14:12:51Z",
  "gitCommitHash": "940a3a2b07adfd14140a0acff96784ef53a0a509",
  "version": "1.0.0",
  "analyzedFiles": 368
}

graph True
nodes [('home/dot_config/claude/rules/model-selection.md', 'Global Claude rule establishing model_profiles in agent-config.yaml as the single source of model IDs and efforts, the orchestrator/worker/auditor role constellation, and profile choice for exploration, reviews and security audits.'), ('home/dot_agents/skills/agmsg-orchestration/SKILL.md', 'Agent skill defining the agmsg orchestration protocol between a Claude orchestrator and Codex workers: architecture, regime activation, parallel workers, identity/delivery, Message Contract v1, .orchestration layout, orchestrator/worker playbooks, worklogs and pitfalls.')]
## Review and integration invariants

- Review every RESULT adversarially across correctness, regressions, security, and reporting omissions: try to refute it, independently re-derive findings, and never treat sampled spot checks as full verification.
- Acceptance review, adversarial RESULT review, and review-profile work remain orchestrator-side; never delegate them to a worker, and keep `make require-crit-review` as the final integration step. Revisit only if worker-side model capability surpasses the orchestrator tier.
- A design review runs in paired rounds. Both reviewers, a fresh Claude context on the `review` profile and a Codex read-only run under a `codex-review` identity, get the same design hash at the same time. The orchestrator revises once per pair of results and opens no round while one is still open. The third pair is the last: on its accept the design is frozen at the hash the pair last accepted, the third pair's own, and whatever is still open at that hash becomes a residual list that is worker input; on its revise or reject nothing is frozen and the design goes back to a context other than its author, never to a fourth pair; a revision after the third pair is not made, and any later change to a hashed key is a new pair (INV-7). The review judges the invariants, threat model, trust anchors and premises for contradiction and enforceability, never implementation detail.
- A task-file review is one round with a fixed stop condition: no contradiction with the design, the premises hold, `allowed_files` covers every touch point that grep finds, and one invariant check (for a task that carries an `invariants` key: the task id maps to its `implementing_tasks` entry, the invariant ids match, and each invariant's sentence equals the design's byte-for-byte, the design read from main (INV-2), checked by hand in the review until a checker lands; a task without the key needs no entry). Anything finer belongs to the worker and the implementation PR.
- A boundary PR synchronizes records at a boundary. It carries no task draft under review. A design not yet on `main` lands through a merged boundary PR before its implementing TASK is dispatched (INV-2), and any merged boundary that carries the design meets that precondition.
- A task that touches a trust boundary (anything the design tier lists, CI that decides a required check, code that executes PR-controlled input) carries a `threat_table` in its front matter: one `{control, disposition}` row per thing the PR or the orchestrator controls (the tree and its tests, task.md, workflow files, interpreter and environment files, in-process effects, new or renamed scripts, metadata separators). The row unit is one row per `allowed_files` entry, one row per listed control that is not a path (task metadata, workflow and interpreter or environment inputs, in-process effects, new or renamed scripts, metadata separators), carried by the declared test module's row where that is where the control acts, and one row per orchestrator effect from the fixed list (forced removal, merge, update-branch); under a wildcard `allowed_files` entry whose files are executed or applied (scripts, workflows, hooks, settings, the rules seats follow), one row per concrete file the PR changes; a wildcard over test fixtures or other data files keeps one row; C4 of the task-consistency check (plan 007 T704) verifies the path half once it lands, and the task-file review checks it by hand until then. A disposition takes one of three forms: `closed: tests/<file>::<name>`, the test that closes the row; `residual: <sentence>`, the compensating control; `out-of-scope: <task id>`, the task that owns the row. Shape is `schemas/task.json`'s (wave V1): a `closed` selector names a test present in the PR tree at acceptance and in the schema's validation of the PR, an `out-of-scope` owner is a task id in the design's `implementing_tasks`, a `residual` payload is a sentence of at least 20 characters (the gate's minimum for a reason). Until `schemas/task.json` lands in wave V1, the task-file review checks the three shape rules by hand. For a `closed` row it checks the selector's form only, since the test does not exist before implementation. Substance is the reviewers': the task-file review, the Bot and the auditor judge each row against the diff. The table is the task's completion condition: a missing row is added once, counted as an amendment, never fixed finding by finding.
- Before every acceptance action (revise, accept, merge) the orchestrator runs `scripts/regime-counters.sh <task id>` and pastes its output into the acceptance record. S2 is decided from INV-6's counts: each component the script prints is read from its output, and for each component it prints as `unknown` the record pastes the command and output that read the source INV-6 names for that component, or, while that source has no entry for the task, says so and pastes the reading of the interim record the orchestrator used in its place. S1 (plan 006: the same finding class three times on one artifact, from any reviewer) is decided from the record's finding-class table, which gives a class to every finding the PR-feedback sweep lists, whatever its disposition, and to every task-level audit finding; three rows of one class stop the artifact.
- A change to a rule sentence requested of a worker travels as a task amendment (hashed, checked by the task-consistency check C1 to C6 once plan 007 T704 lands it and by hand until then, confirmed by the review seat), never as a PONG answer.
- When a finding class reaches three on one artifact (the record's ledger) or `scripts/regime-counters.sh` prints an S1 candidate, the next acceptance action is the records search for that class, pasted into the record as the line `search: <class> -> <the matching mistake records or none>`, and the matching correction is applied when its mechanism is landed, or landed first when it is pending, mechanism by mechanism, before any dispatch; a class is a slug of `[a-z0-9-]` assigned at disposition time, never text taken from a review title. Once plan 007 T718 lands, `scripts/orchestrator/three-repeat.sh <class>` validates the slug, runs the records search and the CompactionDB search without a shell and prints the line; until then the orchestrator runs them by hand with a validated slug. Once `dotfiles-T128-gate-evidence-a02` lands, the gate refuses the action without the line; until then the orchestrator refuses it by rule. Every `not-applicable` disposition carries `; evidence=<command>` with the output pasted in the record.
- At regime or session boundaries, write pending acceptance records, then mechanically commit every `.orchestration` file so no untracked tail remains. The sync needs no per-task artifact set: its audit record is the commit, whose message lists covered task IDs, plus agmsg ACCEPTANCE history. `make check-regime-boundary` reports a canonical clone with unmerged entries, a stash, or a difference from `origin/main` under `home/`, `install/` or `scripts/` as a sign that something ran where it must not. Lessons from a session are codified in this repository (a rule, the skill, or a check) through a task; Claude auto-memory is not a durable store for regime procedure. The canonical clone is pull and apply only and untouched by any seat: no edits, no apply from a dirty tree (the run_before guard refuses it), and one orchestrator identity per repository, seated at the working clone.
- Stop checklist, at every regime or session boundary and in this order: write pending acceptance records; mask every `.orchestration` file the boundary commit adds or changes with `uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets <files>`, which also normalises home directories to `~`; run `make validate-agent-assets` (real exit status); make the `.orchestration` boundary commit with zero untracked tail on a fresh `orchestration/boundary-<YYYY-MM-DD>` branch from `origin/main` and merge its PR with `gh pr merge --squash --auto`; remove every worker with `herdr-agents --remove-worker <worktree>` (despawn, delivery off, leave, tab or workspace closed); check stale identities with `identities.sh <path> <type>` (exactly one name at the main checkout, none at a worker worktree); close Crit review servers (`pgrep -f 'crit _serve'` must be empty); in a CompactionDB-opted-in project, review `uv run --no-project .claude/hooks/contextdb_cli.py memory candidates --limit 20` and promote each candidate worth keeping with `uv run --no-project .claude/hooks/contextdb_cli.py memory promote <id> --scope project`, or leave it. The orchestrator workspace itself stays resident for the next session unless the operator restarts the machine. `make check-regime-boundary` (`scripts/check-regime-boundary.sh`) checks this list and the orchestrator seat lock, one line per violation.
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
  - The orchestrator dispositions every `[P0-P3]` finding in the acceptance record, whatever the verdict: exactly one `audit-finding: <n> …` line per finding, numbered 1..N in the audit's order of `[P0-P3]` lines. The audit's finding lines may be bulleted; a disposition line may be indented but never starts with a list marker, or the gate skips it. `fixed:<sha>` needs a fresh audit of that sha; otherwise `not-applicable:<reason of at least 20 characters>`. Deferral ("later", a follow-up task, a stopgap or a suppression) is not a disposition. The gate enforces these lines only for an `incorrect` verdict (T68), but a finding under `Verdict: correct` is dispositioned all the same.
  - The audit evidence and the PR-feedback JSON quote reviewed content, so mask them with `uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets <files>` before they are committed. The gate compares PR-feedback bodies after the same masking, so masked feedback evidence still matches the live collection (T93, #251).
  - Audit findings are input, never approval; acceptance authority stays with the orchestrator, and each RESULT gets its own acceptance record.
- Crit is agent-side only for Claude Code and Codex alike, as in `home/dot_config/claude/rules/crit-review.md`: record crit-data evidence (`crit status --json`, `crit comments --all --json <review.json>`) and never open a browser review to ask the user. When Crit data is unavailable, save the independent agent review as the same repo-local JSON list (objects with non-empty string `id`, `body`, `scope` and `resolved: true`, at least one `scope: "review"` or path-bound `line`/`file` record; hand-written records are acceptable because the guard validates shape, not provenance) and reference it from a `review_surface: crit-data` receipt with `reviewer: claude-code`, `claude`, or `codex`, `review_source: <that JSON>`, and `review_outcome: approved` or `addressed`. Run `crit share` or any other publish step only when the user explicitly asks for it. Close a Crit session opened by the Plan Mode hook once its review is done, so no local Crit web server stays resident.

## Orchestrator Playbook

1. Join or confirm the agmsg team and identities with the `agmsg` scripts.
2. Create the `.orchestration` directories before assigning work.
3. Write a task file that includes objective, scope, allowed files, forbidden actions, expected artifacts, validation commands, and max turns. Name the render check as `make render-check`, never the bare `python3 scripts/generate-agent-configs.py --check`, which fails without PyYAML. Ground `allowed_files` by grepping the repository for every touch point the task names (tests that pin call sequences, mirrors, fixtures) before dispatch. Verify every CLI constraint the task asserts by running the real command in a safe form, not by reading `--help`. Presume an auditor finding that contradicts your own review is right until you refute it with evidence. Decide the worker kind from the allowed files before dispatch: a seat never edits the source of its own execution boundary, so a change is routed by the boundary it touches. A change that touches only Claude's boundary goes to a Codex seat: the `claude.permissions`, `claude.sandbox` and `claude.hooks` blocks of `home/dot_agents/agent-config.yaml` (including excludedCommands, allowUnsandboxedCommands, writable roots, network and the PermissionRequest hook), the Claude-rendering parts of `scripts/generate-agent-configs.py`, the rendered `home/.chezmoitemplates/claude-settings-managed.json`, and `home/dot_claude/modify_private_settings.json`. A change that touches only Codex's boundary goes to a Claude seat: `codex.sandbox_workspace_write`, `codex.approval_policy`, the Codex-rendering parts of the renderer, and `home/.chezmoitemplates/codex-config-managed.toml`. A change that touches both, or a shared source the orchestrator cannot split (such as `codex.sandbox_workspace_write.writable_roots`, which also renders into Claude's `allowWrite`), goes to the operator. The orchestrator decides the kind from the diff the task will produce and records it and the chosen worker profile in the task file. The Claude Code auto-mode classifier also refuses a Claude-boundary task on a Claude seat as Self-Modification. A task that edits permgate (`home/dot_agents/permgate-policy.yaml`, `home/dot_local/bin/common/executable_permgate`), the PermissionRequest hook of both seats, goes to the operator; a Codex `security`-profile worker reviews the change before the orchestrator accepts it, per the model-selection rule. `auto` is Claude Code's built-in starting permission mode since 2.1.283. A project-level `defaultMode: auto` (`.claude/settings.json` or `.claude/settings.local.json`) does not take effect, and the session then also ignores the user-level `defaultMode`, so `auto` belongs only in user or managed settings. Before dispatch, read the task's verbatim blocks against each other for contradictions, and state each rule once; a second artifact references the first instead of restating it.
4. Start or relaunch worker panes only through `herdr-agents` modes. Deliver messages and wakes as in step 6; never use `pane send-text` followed by `send-keys Enter`, because the separate Enter races the TUI composer and fails nondeterministically.
5. Configure delivery deliberately. `delivery.sh set turn` is useful for turn-end inbox checks; changing delivery mode can kill project watcher processes, so do it before starting long-running project watchers.
6. Send `AGMSG-TASK v1` with the exact artifact paths and `done_signal=AGMSG-RESULT`. Pass every `send.sh`/`poke.sh` body with `--body-file <path>` (both take it in agmsg v1.5.0), never as a positional argument: a positional `<text>` passes through the caller's own shell first, where a backtick or `$( )` in the body silently executes and vanishes from what arrives (upstream #378). `agmsg-dispatch` is the one exception and takes a single-line, shell-safe positional message. Pick the path by how the recipient is seated, never by inferring pane or agent status: a worker in a `herdr-agents` pane gets `agmsg-dispatch <team> <from> <to> <pane_id> "<message>"` (send, generic wake, `read_at` wait; single-line shell-safe text only), the sanctioned wake path until worker seating writes placement records at launch, because `poke.sh` exits 1 with "no placement record" for a hand-joined member, and a herdr-agents worker gets a record only once it acts from its own pane (upstream `send.sh`/`inbox.sh` record the acting pane, #1109); a spawn-seated member (placement record `run/spawn.*`; `team.sh <team> --json` shows its pane) gets `poke.sh <team> <name> --body-file <path> [--retries N --retry-delay SECONDS --backoff fixed|exponential]`, which types and submits in one call and refuses to type over an in-progress draft (#1321/#1322); a pane-less member gets `send.sh <team> <from> <to> --body-file <path>` and its own delivery mode. Verify delivery via the messages.db `read_at` column. `poke.sh` exit codes: 10 = terminal unreachable, 12 = pane gone or no live agent, 14/15 = refused to type over a changing or unlocatable input box, 13 = the driver has no poke path for this pane (for example a `plain` terminal); where poke.sh's narrow agmsg-message fallback succeeds it exits 0, so 13 means nothing was delivered, and the printed reason names the native channel, asks the caller to claim its own identity first, or reports that the fallback failed. Never retry a 13 as `send.sh` yourself: that overrides the driver's considered refusal and can double-deliver. Seating case: a worker in an unviewed or headless Herdr workspace (no client attached, a small pane rect such as 18x41) makes `poke.sh` exit 14/15 from its TUI input locator; that is a locator refusal, not evidence about the worker's state, so wake it with `agmsg-dispatch` and verify `read_at`. Every dispatch (TASK, ACCEPTANCE, PING) is recorded in the current acceptance record under a `dispatch:` key as the bus line with its read marker; a seat is reported as working only from such a line, and after a context compaction the open TASK list is re-derived from a bus read that is refused when it reaches its limit (`bus-read.sh` exits when the history reaches `BUS_READ_LIMIT`; the orchestrator raises the limit and reads again), never from a default-limited one and never from a read whose truncation went unnoticed. A seated worker idle for 20 minutes since its latest bus event for the task while a dispatchable task exists (INV-10's idle figure; its 30 minutes is the first-push deadline) gets a bus read, then a PING; a longer silent wait is never the answer. `scripts/orchestrator/dispatch.sh` writes the line and `scripts/orchestrator/bus-read.sh` performs the read and prints the minutes since each open task's latest event (both on main since a03c1daa, plan 007 T718); the orchestrator applies the 20-minute figure to the minutes the script prints (the script's own silence flag still uses 30 minutes, a recorded residual of the tools lineage).
7. Track `max_turns`. Use `AGMSG-PING` for liveness if a worker stalls.
8. On `AGMSG-RESULT`, read the task file and every referenced artifact before deciding.
9. For a RESULT carrying `effects`, verify that every declared effect has the report's stated reverse mapping before acceptance; record any irreversible effect in the acceptance note.
10. For a RESULT that carries a pull request, integrate in this order. This is the single procedure that the PR integration rule, `AGENTS.md`, the README and the gh-first-workflow skill cite. A `gh pr update-branch` moves the head, so steps 1 to 4 run again on the new head. After an update-branch the orchestrator runs it, the order is CI on the new head, then the sweep, then the audit; an audit started before CI finishes sees incomplete evidence and returns an evidence-only `incorrect`. Select a checkout with git -C <absolute path>, never with cd, which the sandboxed Bash may not honour. After moving the review worktree to the audited head, verify git -C <review> rev-parse HEAD equals that head and git -C <main> symbolic-ref --short HEAD prints main before the audit and the gate.
    1. Sweep the final head's feedback with `scripts/pr-feedback.py <pr> --json .orchestration/validation/<task>-pr-feedback.json` and give every item a `fixed:<commit>` or `not-applicable:<reason>` disposition, leaving none on `failure` or `warning` annotations. Optionally request `@coderabbitai full review` on the final head first; when a CodeRabbit review exists it is swept like any other item, and the gate does not require a bot review. An `open:<thread id>` item from a worker's third Bot round is a sweep item like any other: it becomes `fixed:<sha>` through a revise round that carries its `check=` (a round that counts toward INV-6 like any other), or `not-applicable:<reason>` with a pasted refutation; until one of those exists the PR is not merged, never with the thread open.
    2. Run the task-level audit of that head in the pair or headless form of the task-level audit bullet. It exits nonzero for every verdict other than `correct`. An exit with `Audit verdict: incorrect` is not a failed step: continue to step 3 and disposition its findings. A `blocked` or missing verdict means re-running the audit.
    3. Write the acceptance record, summarising the dispositions, with an `audit-finding:` line for every audit finding whatever the verdict (the gate needs them, through `AUDIT_DISPOSITIONS`, when it is `incorrect`).
    4. Run the gate: `AUDIT_EVIDENCE=<audit> [AUDIT_DISPOSITIONS=<acceptance record>] AGENT_REVIEWED=1 REVIEW_EVIDENCE=<receipt> ACCEPTANCE_EVIDENCE=<acceptance record> BASE=origin/main PR_FEEDBACK_EVIDENCE=<json> make require-crit-review`.
       - A `review` sweep item whose body carries a `P0`–`P3` badge is a finding with its own `fixed:<commit>` or `not-applicable:<reason>` disposition, never a container for its inline threads.
       - The sweep covers issue comments, reviews, inline review comments with thread resolution, non-passing check runs, check-run annotations at every level (`notice`, `warning`, `failure`), and commit statuses. A `failure` marked `not-applicable` needs a concrete reason of at least 20 characters.
       - A CodeRabbit full review is optional, at most once on the final head: the plan allows one review per hour and every review event spends one (docs.coderabbit.ai/management/rate-limits).
       - The feedback JSON may be masked with `uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets`, which masks its keys and string values; the gate identifies an item by its source, url, level, path, line and body, and accepts a body or path that is verbatim or exactly that masked form.
       - The gate rejects evidence outside `.orchestration/validation/` or without the `-pr-feedback.json` suffix. It binds `BASE` to the PR's GitHub base before running the collector from that authenticated SHA: an older base must be outside HEAD's first-parent chain, an advanced base must preserve the merge-base with the PR head, and PR branch commits (including `HEAD`) cannot substitute for the base. Evidence must match the local GitHub repository independently of `GH_REPO`, and `fixed:` commits must be in the authenticated GitHub base-to-head range whatever `BASE` is selected.
       - `AUDIT_EVIDENCE` must be the task-level file `.orchestration/validation/<task>-audit-<sha7>.md` (the same `<task>` as the feedback JSON); a per-commit `audit-<sha>.md` is rejected. Its verdict comes only from the non-empty `<file>.last.md` and must be `correct`, or `incorrect` with `AUDIT_DISPOSITIONS`. PRs that change only `.orchestration/` files need no audit.
       - A boundary PR (`orchestration/boundary-<date>[-n]`, `.orchestration` files only) skips the gate, the sweep JSON and the audit (with `BASE` set the gate would demand `PR_FEEDBACK_EVIDENCE`); each Bot thread on it still gets a disposition reply and is resolved, and the next boundary commit message names the PR.
    5. After the required checks pass and the threads are resolved, merge with `gh pr merge <pr> --squash --match-head-commit <audited head sha>`, so a newer head can never be merged on the evidence of the audited one. Every seat acts as the machine's one GitHub account, so no approval is required or possible. Who merges is decided by the integration gate and by native denial of merge commands in Codex seats; `herdr-agents` writes the Claude worker deny rules (`Bash(gh pr merge:*)`, `Bash(gh api -X PUT:*)`, `Bash(gh api --method PUT:*)`, `Bash(gh api graphql:*)`) into the worker worktree's `.claude/settings.local.json`, where [deny rules take precedence over allow rules and cover nested subcommands in every permission mode](https://code.claude.com/docs/en/permissions), but a method flag after the path escapes these prefix rules, so the integration gate remains the authority.
    6. Send `AGMSG-ACCEPTANCE` (step 11).

**Adjusting output token limits**
exec
/bin/zsh -lc 'git diff --name-status ec94dc56305f55df470a4b1d4215ad272418beac b6ce4ffabe0e66a102e224e75be575a501c5a793 && git diff --no-ext-diff ec94dc56305f55df470a4b1d4215ad272418beac b6ce4ffabe0e66a102e224e75be575a501c5a793 -- scripts/orchestrator tests/unit/test_chain_review_scripts.py' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 71ms:
A	.orchestration/dotfiles-T128-chain-review-scripts-a01/autoskill.md
A	.orchestration/dotfiles-T128-chain-review-scripts-a01/learning.md
A	.orchestration/dotfiles-T128-chain-review-scripts-a01/report.md
A	.orchestration/dotfiles-T128-chain-review-scripts-a01/sandbox.md
A	.orchestration/dotfiles-T128-chain-review-scripts-a01/task.md
A	.orchestration/dotfiles-T128-chain-review-scripts-a01/validation.md
A	scripts/orchestrator/local-advisory.sh
A	scripts/orchestrator/local-review.sh
A	scripts/orchestrator/sandbox-scan.sh
A	tests/unit/test_chain_review_scripts.py
diff --git a/scripts/orchestrator/local-advisory.sh b/scripts/orchestrator/local-advisory.sh
new file mode 100755
index 00000000..90d57e15
--- /dev/null
+++ b/scripts/orchestrator/local-advisory.sh
@@ -0,0 +1,49 @@
+#!/usr/bin/env bash
+# @file local-advisory.sh
+# @brief Record a local review's P2/P3 findings as advisory rows of the acceptance record; stop on a P0/P1.
+# @description
+#   Plan 020 step 1.2 for the local review. Reads `.orchestration/validation/<task>-local-review-<sha7>.md`. Each
+#   unique finding, numbered from 1: a P0/P1 prints STOP (the PR's one round is over: the plan's step 4.2); any
+#   other appends the row `local:<sha7>:<n><TAB>advisory-p2` under the heading `## Owned by <owner>` of
+#   `.orchestration/acceptance/<task>.md` (created when missing) and a `local-finding: <sha7>:<n>
+#   not-applicable:advisory P2 owned by <owner> (…); evidence=…` line, each only when the record lacks it.
+# @arg $1 string Task id.
+# @arg $2 string The reviewed head, 40 hex characters.
+# @arg $3 string The task id that owns the advisory findings.
+# @exitcode 0 No P0/P1 finding.
+# @exitcode 2 No local review file.
+# @exitcode 3 A P0/P1 finding.
+# @example
+#   scripts/orchestrator/local-advisory.sh dotfiles-T128-x-a01 "$head" dotfiles-T128-x-followup-a01
+set -euo pipefail
+task=$1 head=$2 owner=$3
+cd "$(git rev-parse --show-toplevel)"
+h7=${head:0:7}
+LR=".orchestration/validation/$task-local-review-$h7.md"
+A=".orchestration/acceptance/$task.md"
+[ -s "$LR" ] || {
+    echo "no local review file $LR"
+    exit 2
+}
+n=$(sed -n 's/^findings: //p' "$LR" | head -1)
+[ "${n:-0}" != "0" ] || {
+    echo "local review of $h7: no findings"
+    exit 0
+}
+/usr/bin/grep -q "^## Owned by $owner" "$A" || printf '\n## Owned by %s (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)\n\n' "$owner" >> "$A"
+i=0 stop=0
+while IFS= read -r line; do
+    i=$((i + 1))
+    case "$line" in
+    *"[P0]"* | *"[P1]"*)
+        echo "STOP: local finding $i of $h7 is P0/P1: $line"
+        stop=1
+        ;;
+    *)
+        /usr/bin/grep -q "^local:$h7:$i	" "$A" || printf 'local:%s:%s\tadvisory-p2\n' "$h7" "$i" >> "$A"
+        /usr/bin/grep -q "^local-finding: $h7:$i " "$A" || printf 'local-finding: %s:%s not-applicable:advisory P2 owned by %s (%s); evidence=git show origin/main:.orchestration/tasks/%s.md | grep -n '"'"'item 1'"'"'\n' "$h7" "$i" "$owner" "$(printf '%s' "$line" | cut -c1-120 | tr -d '`')" "$owner" >> "$A"
+        ;;
+    esac
+done < <(/usr/bin/grep -E '^- \[P[0-3]\]' "$LR" | sort -u)
+echo "local review of $h7: $i finding(s) recorded as advisory under 'Owned by $owner' in $A"
+[ "$stop" = 0 ] || exit 3
diff --git a/scripts/orchestrator/local-review.sh b/scripts/orchestrator/local-review.sh
new file mode 100755
index 00000000..04806af5
--- /dev/null
+++ b/scripts/orchestrator/local-review.sh
@@ -0,0 +1,75 @@
+#!/usr/bin/env bash
+# @file local-review.sh
+# @brief Review a PR head's diff against main locally with the Bot's engine, once per head, before the audit (C-32).
+# @description
+#   Run outside the Bash sandbox: inside it codex exits 1 ("failed to initialize in-process app-server client:
+#   Operation not permitted"). An existing `.orchestration/validation/<task>-local-review-<sha7>.md` is reused and
+#   re-reported. Otherwise the clean review worktree (`$ORCH_REVIEW_WORKTREE`, else
+#   `.claude/worktrees/orchestrator-review`), a path with its own `.git` entry, is checked out detached at the head
+#   and left there, and the review binary (`$CODEX_BIN`, else codex) runs in it as `--profile review -s read-only
+#   review --base main`. The file gets the front matter, the unique `- [P0-3]` findings of the transcript's final
+#   message, and that message with the worktree prefix stripped; the findings are printed, then `local-review: <n>
+#   findings (<file>)`.
+# @arg $1 string Task id.
+# @arg $2 string The PR head commit, a local one.
+# @arg $3 int PR number.
+# @exitcode 0 No finding.
+# @exitcode 2 A precondition failed: the head is not a local commit, the review worktree is not a worktree root or not
+#   clean, or there is no review binary.
+# @exitcode 3 One or more findings.
+# @example
+#   scripts/orchestrator/local-review.sh dotfiles-T128-x-a01 "$(git rev-parse FETCH_HEAD)" 356
+set -euo pipefail
+task=$1 head=$2 pr=$3
+R="$(git rev-parse --show-toplevel)"
+cd -- "$R"
+W=${ORCH_REVIEW_WORKTREE:-$R/.claude/worktrees/orchestrator-review}
+out=$R/.orchestration/validation/$task-local-review-${head:0:7}.md
+if [ -s "$out" ]; then
+    # one sample per head (C-32): a review of this head exists; reuse it instead of sampling again
+    findings=$(/usr/bin/grep -E '^- \[P[0-3]\]' "$out" | sort -u || true)
+    n=$(sed -n 's/^findings: //p' "$out" | head -1)
+    printf '%s\n' "$findings"
+    echo "local-review: $n findings (existing $out)"
+    [ "${n:-0}" = 0 ] || exit 3
+    exit 0
+fi
+git -C "$R" cat-file -e "$head^{commit}" 2> /dev/null || {
+    echo "local-review: $head is not a local commit (fetch pull/$pr/head first)"
+    exit 2
+}
+# Without its own .git entry, git -C would act on an enclosing checkout and move that one to the head.
+[ -e "$W/.git" ] || {
+    echo "local-review: $W is not a worktree root"
+    exit 2
+}
+[ -z "$(git -C "$W" status --porcelain)" ] || {
+    echo "local-review: $W is not clean"
+    exit 2
+}
+# Resolved in the root before the checkout and run by its absolute path, so no relative PATH entry (./bin) picks a
+# binary from the PR head.
+codex=$(command -v "${CODEX_BIN:-codex}") || {
+    echo "local-review: no review binary ${CODEX_BIN:-codex}"
+    exit 2
+}
+[[ $codex == /* ]] || codex=$R/$codex
+git -C "$W" checkout -q --detach "$head"
+base=$(git -C "$W" merge-base main HEAD)
+t0=$(date -u +%FT%TZ)
+tmp=$(mktemp "${TMPDIR:-/tmp}/local-review.XXXXXX")
+(cd "$W" && "$codex" --profile review -s read-only review --base main < /dev/null > "$tmp" 2>&1) || echo "local-review: codex exited $? (see $out)"
+final=$(awk '/^codex$/{f=1; buf=""; next} f{buf=buf $0 "\n"} END{printf "%s", buf}' "$tmp" | sed "s#$W/##g")
+findings=$(printf '%s\n' "$final" | /usr/bin/grep -E '^- \[P[0-3]\]' | sort -u || true)
+n=$(printf '%s' "$findings" | /usr/bin/grep -c . || true)
+{
+    printf -- '---\ntask: %s\nhead: %s\npr: %s\nbase: %s\nstarted: %s\nfinished: %s\nfindings: %s\nengine: codex review --base main (profile review, read-only)\n---\n\n' "$task" "$head" "$pr" "$base" "$t0" "$(date -u +%FT%TZ)" "$n"
+    printf '%s\n\n' "$findings"
+    echo '```text'
+    printf '%s\n' "$final" | cut -c1-2000
+    echo '```'
+} > "$out"
+rm -f "$tmp"
+printf '%s\n' "$findings"
+echo "local-review: $n findings ($out)"
+[ "$n" = 0 ] || exit 3
diff --git a/scripts/orchestrator/sandbox-scan.sh b/scripts/orchestrator/sandbox-scan.sh
new file mode 100755
index 00000000..de757953
--- /dev/null
+++ b/scripts/orchestrator/sandbox-scan.sh
@@ -0,0 +1,24 @@
+#!/usr/bin/env bash
+# @file sandbox-scan.sh
+# @brief Print the unsandboxed mutation calls of a worker's sandbox record, so a hit is judged before the audit (C-29).
+# @description
+#   Reads `.orchestration/sandboxes/<task>.md`, a trailing `-fixtures` of the task id stripped. A line that names
+#   `dangerouslyDisableSandbox`, `outside the sandbox` or `unsandboxed` and a mutation (`git commit`, `git switch -c`,
+#   `git checkout`, `git add`, `git mv`, `git rm`, `cp `, `mv `, `> `, `tee `) but none of `counts`, `reads`, `lists`,
+#   matched case-insensitively, is printed with its line number, then the judge line; with no such line, one line says
+#   none. A missing record prints nothing.
+# @arg $1 string Task id.
+# @exitcode 0 Always.
+# @example
+#   scripts/orchestrator/sandbox-scan.sh dotfiles-T128-x-a01
+set -euo pipefail
+task=$1
+cd "$(git rev-parse --show-toplevel)"
+sb=".orchestration/sandboxes/${task%-fixtures}.md"
+if [ -f "$sb" ]; then
+    if /usr/bin/grep -n -i -E 'dangerouslyDisableSandbox|outside the sandbox|unsandboxed' "$sb" | /usr/bin/grep -i -E 'git (commit|switch -c|checkout|add|mv|rm)|cp |mv |> |tee ' | /usr/bin/grep -v -i 'counts\|reads\|lists'; then
+        echo "sandbox scan: unsandboxed mutation calls above (C-29); judge before the audit"
+    else
+        echo "sandbox scan: no unsandboxed mutation call in $sb"
+    fi
+fi
diff --git a/tests/unit/test_chain_review_scripts.py b/tests/unit/test_chain_review_scripts.py
new file mode 100644
index 00000000..9295cf9e
--- /dev/null
+++ b/tests/unit/test_chain_review_scripts.py
@@ -0,0 +1,230 @@
+"""Exercise the review-side chain scripts (plan 021 step 6.3) in a temporary git repository.
+
+Each script runs as a subprocess from this checkout with the temporary repository as its working directory, so the
+repository root it resolves is the temporary one. git is the real one. A stub review binary appends its argv, its
+working directory, the HEAD there, PATH and its stdin to `<calls>/<name>.log`, prints `<calls>/transcript` and exits with
+`<calls>/status` (0 when absent).
+"""
+
+import os
+import re
+import subprocess
+import tempfile
+import unittest
+from pathlib import Path
+
+TOOLS = Path(__file__).resolve().parents[2] / "scripts/orchestrator"
+GIT_ENV = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
+STUB = (
+    "#!/usr/bin/env bash\n"
+    '{{ printf "argv:"; printf " %s" "$@"; printf "\\ncwd: %s\\nhead: %s\\npath: %s\\nstdin: %s\\n" '
+    '"$(pwd -P)" "$(git rev-parse HEAD)" "$PATH" "$(cat)"; }} >> "$CALLS/{name}.log"\n'
+    'cat "$CALLS/transcript"\nexit "$(cat "$CALLS/status" 2> /dev/null || echo 0)"\n'
+)
+ARGV = "argv: --profile review -s read-only review --base main"
+SCAN_HIT = "sandbox scan: unsandboxed mutation calls above (C-29); judge before the audit"
+
+
+class ChainReviewScriptsTest(unittest.TestCase):
+    def setUp(self):
+        temp = tempfile.TemporaryDirectory()
+        self.addCleanup(temp.cleanup)
+        self.temp = Path(temp.name).resolve()
+        self.repo = self.temp / "repo"
+        self.calls = self.temp / "calls"
+        self.calls.mkdir()
+        self.git("init", "-q", "-b", "main", str(self.repo), cwd=self.temp)
+        self.write("a.txt", "a\n")
+        self.git("add", "a.txt")
+        self.git("commit", "-q", "-m", "main")
+        self.env = {**os.environ, **GIT_ENV, "CALLS": str(self.calls), "TMPDIR": str(self.temp)}
+        for name in ("CODEX_BIN", "ORCH_REVIEW_WORKTREE"):
+            self.env.pop(name, None)
+
+    def git(self, *args, cwd=None):
+        return subprocess.run(
+            ["git", "-c", "commit.gpgsign=false", *args],
+            cwd=cwd or self.repo,
+            env={**os.environ, **GIT_ENV},
+            capture_output=True,
+            text=True,
+            check=True,
+        ).stdout.strip()
+
+    def write(self, rel, text, root=None):
+        path = (root or self.repo) / rel
+        path.parent.mkdir(parents=True, exist_ok=True)
+        path.write_text(text)
+        return path
+
+    def stub(self, path, name):
+        path.parent.mkdir(parents=True, exist_ok=True)
+        path.write_text(STUB.format(name=name))
+        path.chmod(0o755)
+
+    def log(self, name):
+        path = self.calls / f"{name}.log"
+        return path.read_text() if path.exists() else ""
+
+    def run_tool(self, name, *args, code=0, env=None, cwd=None):
+        # The review binary must not read what the caller's stdin holds.
+        result = subprocess.run(
+            ["bash", str(TOOLS / name), *map(str, args)],
+            capture_output=True,
+            text=True,
+            input="caller stdin\n",
+            cwd=cwd or self.repo,
+            env={**self.env, **(env or {})},
+            timeout=30,
+            check=False,
+        )
+        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
+        return result.stdout
+
+    def test_local_review_runs_the_review_binary_read_only_at_the_head_and_writes_one_file(self):
+        review = self.temp / "review"
+        self.git("worktree", "add", "-q", "--detach", str(review), "main")
+        # The head commit, made in the review worktree, carries a decoy bin/codex; the main working tree never does.
+        self.stub(review / "bin/codex", "decoy")
+        self.write("b.txt", "b\n", root=review)
+        self.git("add", "bin/codex", "b.txt", cwd=review)
+        self.git("commit", "-q", "-m", "head", cwd=review)
+        head, base = self.git("rev-parse", "HEAD", cwd=review), self.git("rev-parse", "main")
+        self.git("checkout", "-q", "--detach", "main", cwd=review)
+        self.stub(self.temp / "bin/codex", "codex")
+        (self.repo / ".orchestration/validation").mkdir(parents=True)
+        path = f"./bin{os.pathsep}{self.temp / 'bin'}{os.pathsep}{os.environ['PATH']}"
+        env = {"ORCH_REVIEW_WORKTREE": str(review), "PATH": path}
+        # An earlier marker's message is not the final one; the worktree prefix is stripped; a repeated line counts once.
+        final = f"One finding.\n- [P2] {review}/b.txt:1 b is new\n- [P2] {review}/b.txt:1 b is new\n"
+        (self.calls / "transcript").write_text(f"codex\n- [P1] {review}/a.txt:1 superseded\ncodex\n{final}")
+        finding = "- [P2] b.txt:1 b is new"
+        call = f"{ARGV}\ncwd: {review}\nhead: {head}\npath: {path}\nstdin: \n"
+
+        def out(task):
+            return self.repo / f".orchestration/validation/{task}-local-review-{head[:7]}.md"
+
+        with self.subTest("a review worktree path without its own .git entry exits 2"):
+            # First, while the main working tree is clean: the dirty check alone would pass it.
+            (self.repo / "plain").mkdir()
+            plain = {**env, "ORCH_REVIEW_WORKTREE": str(self.repo / "plain")}
+            self.assertIn("is not a worktree root", self.run_tool("local-review.sh", "t-p", head, 9, code=2, env=plain))
+            self.assertEqual("", self.log("codex"))
+            self.assertEqual(base, self.git("rev-parse", "HEAD"))
+        with self.subTest("CODEX_BIN unset: codex resolved in the root before the checkout"):
+            stdout = self.run_tool("local-review.sh", "t-a", head, 9, code=3, env=env)
+            self.assertEqual(f"{finding}\nlocal-review: 1 findings ({out('t-a')})\n", stdout)
+            self.assertEqual(call, self.log("codex"))
+            self.assertEqual("", self.log("decoy"))
+            self.assertEqual(head, self.git("rev-parse", "HEAD", cwd=review))
+            status = self.git("status", "--porcelain", "--untracked-files=all")
+            self.assertEqual(f"?? .orchestration/validation/t-a-local-review-{head[:7]}.md", status)
+            text = out("t-a").read_text()
+            front = f"---\ntask: t-a\nhead: {head}\npr: 9\nbase: {base}\nstarted: .+\nfinished: .+\nfindings: 1\n"
+            self.assertRegex(text, "^" + re.escape(front).replace(r"\.\+", ".+"))
+            self.assertIn("engine: codex review --base main (profile review, read-only)\n---\n", text)
+            self.assertIn(f"\n{finding}\n\n```text\nOne finding.\n{finding}\n{finding}\n```\n", text)
+            self.assertNotIn("superseded", text)
+            self.assertEqual([], list(self.temp.glob("local-review.*")))
+        self.git("checkout", "-q", "--detach", "main", cwd=review)
+        with self.subTest("CODEX_BIN set: that binary runs, a relative path resolved in the root"):
+            self.stub(self.repo / "seam/review-binary", "seam")
+            seam = {**env, "CODEX_BIN": "seam/review-binary"}
+            self.run_tool("local-review.sh", "t-b", head, 9, code=3, env=seam, cwd=self.repo / ".orchestration")
+            self.assertEqual(call, self.log("seam"))
+            self.assertEqual(call, self.log("codex"))
+        with self.subTest("one review per head: the file is reused"):
+            stdout = self.run_tool("local-review.sh", "t-a", head, 9, code=3, env=env)
+            self.assertEqual(f"{finding}\nlocal-review: 1 findings (existing {out('t-a')})\n", stdout)
+            self.assertEqual(call, self.log("codex"))
+        (self.calls / "transcript").write_text("codex\nNo findings.\n")
+        (self.calls / "status").write_text("5")
+        with self.subTest("no finding exits 0, also when the binary fails"):
+            stdout = self.run_tool("local-review.sh", "t-c", head, 9, env=env)
+            file = out("t-c")
+            self.assertEqual(
+                f"local-review: codex exited 5 (see {file})\n\nlocal-review: 0 findings ({file})\n", stdout
+            )
+            self.assertIn("findings: 0\n", out("t-c").read_text())
+        missing = {**env, "CODEX_BIN": "seam/missing"}
+        self.assertIn("no review binary", self.run_tool("local-review.sh", "t-d", head, 9, code=2, env=missing))
+        self.write("dirty.txt", "x\n", root=review)
+        with self.subTest("a dirty review worktree or an unknown head exits 2 and runs nothing"):
+            self.assertIn("is not clean", self.run_tool("local-review.sh", "t-d", head, 9, code=2, env=env))
+            unknown = "0" * 40
+            self.assertIn("is not a local commit", self.run_tool("local-review.sh", "t-d", unknown, 9, code=2, env=env))
+            self.assertEqual(2, self.log("codex").count(ARGV))
+            self.assertFalse(out("t-d").exists())
+
+    def test_local_advisory_records_p2_rows_and_stops_on_p0_p1(self):
+        head, owner = "abcdef0" + "1" * 33, "t-followup-a01"
+        record = self.write(".orchestration/acceptance/t-a01.md", "# record\n")
+        heading = f"## Owned by {owner} (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)\n"
+        # Numbered in sort order; the second is cut to 120 characters, then loses its backticks.
+        first, long = "- [P2] `a.sh:1` first", "- [P2] `b.sh:3` " + "y" * 130
+
+        def review(*findings):
+            front = f"---\ntask: t-a01\nfindings: {len(findings)}\n---\n\n"
+            # Each finding appears twice, in the list and in the transcript, as the local review writes it.
+            text = "\n".join(findings)
+            self.write(f".orchestration/validation/t-a01-local-review-{head[:7]}.md", f"{front}{text}\n\n{text}\n")
+
+        def line(n, finding):
+            text = finding[:120].replace("`", "")
+            return (
+                f"local-finding: abcdef0:{n} not-applicable:advisory P2 owned by {owner} ({text}); "
+                f"evidence=git show origin/main:.orchestration/tasks/{owner}.md | grep -n 'item 1'\n"
+            )
+
+        review(long, first)
+        for _ in range(2):
+            stdout = self.run_tool("local-advisory.sh", "t-a01", head, owner)
+        self.assertEqual(
+            f"local review of abcdef0: 2 finding(s) recorded as advisory under 'Owned by {owner}' in .orchestration/acceptance/t-a01.md\n",
+            stdout,
+        )
+        rows = "local:abcdef0:1\tadvisory-p2\n" + line(1, first)
+        rows += "local:abcdef0:2\tadvisory-p2\n" + line(2, long)
+        self.assertEqual(f"# record\n\n{heading}\n{rows}", record.read_text())
+        record.write_text("# record\n")
+        review("- [P1] a.sh:1 blocks", "- [P2] b.sh:2 second")
+        stdout = self.run_tool("local-advisory.sh", "t-a01", head, owner, code=3)
+        self.assertIn("STOP: local finding 1 of abcdef0 is P0/P1: - [P1] a.sh:1 blocks\n", stdout)
+        rows = "local:abcdef0:2\tadvisory-p2\n" + line(2, "- [P2] b.sh:2 second")
+        self.assertEqual(f"# record\n\n{heading}\n{rows}", record.read_text())
+        record.write_text("# record\n")
+        review("- [P0] c.sh:1 breaks")
+        stdout = self.run_tool("local-advisory.sh", "t-a01", head, owner, code=3)
+        self.assertIn("STOP: local finding 1 of abcdef0 is P0/P1: - [P0] c.sh:1 breaks\n", stdout)
+        self.assertEqual(f"# record\n\n{heading}\n", record.read_text())
+        record.write_text("# record\n")
+        review()
+        self.assertEqual(
+            "local review of abcdef0: no findings\n", self.run_tool("local-advisory.sh", "t-a01", head, owner)
+        )
+        self.assertEqual("# record\n", record.read_text())
+        self.assertIn("no local review file", self.run_tool("local-advisory.sh", "t-b01", head, owner, code=2))
+
+    def test_sandbox_scan_prints_the_unsandboxed_mutation_calls(self):
+        sandboxes = ".orchestration/sandboxes"
+        hit = "| 2 | dangerouslyDisableSandbox: git commit -m wip |"
+        self.write(
+            f"{sandboxes}/t-a01.md", f"# sandbox\n{hit}\n- The unsandboxed table Counts every git commit > log.\n"
+        )
+        self.assertEqual(f"2:{hit}\n{SCAN_HIT}\n", self.run_tool("sandbox-scan.sh", "t-a01"))
+        # A trailing -fixtures is stripped, and the match ignores case.
+        self.write(f"{sandboxes}/t-b01.md", "Outside The Sandbox: GIT ADD x\n")
+        self.assertEqual(
+            f"1:Outside The Sandbox: GIT ADD x\n{SCAN_HIT}\n", self.run_tool("sandbox-scan.sh", "t-b01-fixtures")
+        )
+        reads = (
+            "| 1 | gh pr view 9 > pr.json (outside the sandbox; reads) |\n| 2 | unsandboxed tee log, lists the PRs |\n"
+        )
+        self.write(f"{sandboxes}/t-c01.md", reads)
+        none = f"sandbox scan: no unsandboxed mutation call in {sandboxes}/t-c01.md\n"
+        self.assertEqual(none, self.run_tool("sandbox-scan.sh", "t-c01"))
+        self.assertEqual("", self.run_tool("sandbox-scan.sh", "t-d01"))
+
+
+if __name__ == "__main__":
+    unittest.main()

exec
/bin/zsh -lc "python3 -B -c 'import pathlib,subprocess; h=\"b6ce4ffabe0e66a102e224e75be575a501c5a793\"; p=\".orchestration/tasks/dotfiles-T128-chain-review-scripts-a01.md\"; print(\"LOCAL TASK\\n\"+pathlib.Path(p).read_text()); p=\".orchestration/dotfiles-T128-chain-review-scripts-a01/task.md\"; print(\"\\nBRANCH \"+p); print(\"\\n\".join(str(i)+\": \"+line for i,line in enumerate(subprocess.check_output([\"git\",\"show\",h+\":\"+p],text=True).splitlines(),1)))'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 138ms:
LOCAL TASK
---
format: 2
task_id: dotfiles-T128-chain-review-scripts-a01
kind: code
security: false
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - scripts/orchestrator/local-review.sh
  - scripts/orchestrator/local-advisory.sh
  - scripts/orchestrator/sandbox-scan.sh
  - tests/unit/test_chain_review_scripts.py
  - .orchestration/dotfiles-T128-chain-review-scripts-a01/**
after: [dotfiles-T128-gate-wrapper-path-a01]
threat_table:
  - control: the PR adds scripts/orchestrator/local-review.sh, which checks the review worktree out at a PR head and runs the review binary there read-only, writing one validation file
    disposition: "closed: tests/unit/test_chain_review_scripts.py::test_local_review_runs_the_review_binary_read_only_at_the_head_and_writes_one_file"
  - control: the PR adds scripts/orchestrator/local-advisory.sh, which appends advisory rows and local-finding lines to an acceptance record and stops on a P0 or P1
    disposition: "closed: tests/unit/test_chain_review_scripts.py::test_local_advisory_records_p2_rows_and_stops_on_p0_p1"
  - control: the PR adds scripts/orchestrator/sandbox-scan.sh, which prints the unsandboxed mutation calls of a worker sandbox record
    disposition: "closed: tests/unit/test_chain_review_scripts.py::test_sandbox_scan_prints_the_unsandboxed_mutation_calls"
  - control: the PR adds tests/unit/test_chain_review_scripts.py, the oracle of the three rows above (a stub review binary on CODEX_BIN that records argv, cwd and environment and prints a canned transcript; a temporary git repository with a main branch and a head commit as the review worktree; fixture texts the tests write)
    disposition: "residual: the stubs record and print, nothing else; the audit reads each case against the Files items"
  - control: "the review worktree (the path ORCH_REVIEW_WORKTREE names when set, else <root>/.claude/worktrees/orchestrator-review): local-review.sh refuses with exit 2 a path that is not a worktree root (no .git entry at the path itself, so git -C cannot fall through to an enclosing checkout) and a dirty one, checks the head out detached and restores nothing (the chain's audit wrapper restores it)"
    disposition: "residual: the orchestrator's own worktree, detached at origin/main between runs; both refusals are covered by the first closed row's cases (amendment 1 adds the non-worktree case); the restore belongs to orch-audit.sh on main"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T128-chain-review-scripts-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T128-chain-review-scripts-a01/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the tests run the three scripts as subprocesses with the stub review binary on CODEX_BIN and real git in a temporary repository, and import only the standard library; nothing is imported into another process"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; local-review.sh runs git, mktemp and the review binary (the value of CODEX_BIN when the environment sets it, the test seam, else codex resolved with command -v in the repository root before the head checkout, its absolute path used afterwards; the profile review is fixed in the script, the model-selection rule); local-review.sh also runs awk, sed, date, cut, grep, sort, head and rm; local-advisory.sh runs git rev-parse, grep, sed, cut, tr, head and sort; sandbox-scan.sh runs git rev-parse and grep; the review binary runs with the PR head as its working directory under its own read-only sandbox, so the PR's content (its AGENTS.md, its configuration files) is input to that review and never to the gate: the review's findings are a sample the orchestrator judges (advisory rows or a stop), and the script writes nothing but the validation file"
  - control: new or renamed scripts
    disposition: "residual: three new scripts under scripts/orchestrator/, named in allowed_files and listed in the RESULT; any other new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: 'none of the three script names exists under scripts/orchestrator/ on origin/main (the task adds, it does not edit)'
    command: 'git ls-tree --name-only origin/main scripts/orchestrator/ | /usr/bin/grep -c -E "local-review|local-advisory|sandbox-scan" || true'
    output: |-
      0
---

# AGMSG-TASK dotfiles-T128-chain-review-scripts-a01 — the integration chain's review-side steps become repository scripts with tests (plan 021 step 6.3; the review half of the step's "next tools task")

Drafted 2026-10-14 by the orchestrator seat (the bus time of its TASK line is the dispatch time), in the step-7 short form. Plan 021's step 6.3 inventory names six chain steps whose logic lives only in the orchestrator's scratchpad; the hand-typed-chain class holds fourteen mistake records today, and the structural answer is repository scripts with tests. This task lands the three review-side scripts; its sibling `dotfiles-T128-chain-github-scripts-a01` lands the two GitHub-side scripts (`resolve-threads.sh`, `pr-cost.sh`) with its own test module, so the two run concurrently on disjoint files. The attached inputs under `.orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/` of the orchestrator's main checkout (the directory the TASK line's `task_file` is read from, untracked until the next boundary) are the scripts as the chain runs them today, with the repository root resolved by `git rev-parse --show-toplevel`; their sha256 prefixes (`shasum -a 256 <dir>/*.sh | cut -c1-16`): 2e44dabc23ea0397  local-advisory.sh; 2258e370b9ff2575  local-review.sh; 099f6c7534223cb4  sandbox-scan.sh; each item names what changes. The one premise is replayable from any checkout (it reads `origin/main`).

## Goal

The local review of a PR head, the recording of its advisory findings and the scan of a worker's sandbox record run from `scripts/orchestrator/` on `origin/main`, each with one test that closes its row, so the next integration's log names repository scripts for these steps.

## Files

1. `scripts/orchestrator/local-review.sh <task> <head> <pr>`: the input's behaviour (one review per head: an existing `.orchestration/validation/<task>-local-review-<sha7>.md` is reused and re-reported with its finding lines and `local-review: <n> findings (existing <file>)`; otherwise the head must be a local commit, exit 2 if not; the review worktree path must hold a `.git` entry of its own (a worktree root; a plain directory inside a checkout would let `git -C` act on the enclosing checkout), exit 2 if not, and be clean, exit 2 if not; the worktree is checked out detached at the head; the review binary runs there as `<binary> --profile review -s read-only review --base main` with stdin from `/dev/null`; the transcript's final message after the `codex` marker line is kept with the worktree prefix stripped; the unique lines matching `^- \[P[0-3]\]` are the findings; the file gets the front matter the input writes: task, head, pr, base, started, finished, findings, engine; the findings are printed, then `local-review: <n> findings (<file>)`; a non-zero exit of the review binary prints `local-review: codex exited <n> (see <file>)` and the file is still written from whatever transcript came back; exit 0 with no finding, 3 with findings, 2 on a precondition) with these changes: the repository root is `git rev-parse --show-toplevel`; the review worktree is `$ORCH_REVIEW_WORKTREE` when set, else `<root>/.claude/worktrees/orchestrator-review`; the review binary is `$CODEX_BIN` when set, else `codex` resolved with `command -v` in the repository root before the checkout and used by that absolute path afterwards; the profile `review` stays fixed in the script; the transcript's temporary file comes from `mktemp` with the template `${TMPDIR:-/tmp}/local-review.XXXXXX` (macOS `mktemp` without a template ignores `TMPDIR` and uses the per-user directory, which the Bash sandbox denies; the form `orch-gate.sh` uses); an shdoc header; `bash -n` and shellcheck clean.
2. `scripts/orchestrator/local-advisory.sh <task> <head40> <owner-task-id>`: the input's behaviour (reads `.orchestration/validation/<task>-local-review-<sha7>.md`, exit 2 when absent; `findings: 0` prints `local review of <sha7>: no findings` and exits 0; otherwise ensures the heading `## Owned by <owner> (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)` in `.orchestration/acceptance/<task>.md`; then for each unique finding line in order, numbered from 1: a `[P0]` or `[P1]` prints `STOP: local finding <n> of <sha7> is P0/P1: <line>` and makes the exit 3, any other appends the row `local:<sha7>:<n><TAB>advisory-p2` and the line `local-finding: <sha7>:<n> not-applicable:advisory P2 owned by <owner> (<the finding's first 120 characters, backticks removed>); evidence=git show origin/main:.orchestration/tasks/<owner>.md | grep -n 'item 1'`, each only when the record lacks it; last line `local review of <sha7>: <i> finding(s) recorded as advisory under 'Owned by <owner>' in <record>`) with the repository root from `git rev-parse --show-toplevel` and an shdoc header.
3. `scripts/orchestrator/sandbox-scan.sh <task>`: the input's behaviour (over `.orchestration/sandboxes/<task>.md`, where a trailing `-fixtures` of `<task>` is stripped as the input does with `${task%-fixtures}`: the lines matching, case-insensitively as the input's `grep -i` does, `dangerouslyDisableSandbox`, `outside the sandbox` or `unsandboxed` that also match a mutation, `git commit`, `git switch -c`, `git checkout`, `git add`, `git mv`, `git rm`, `cp `, `mv `, `> ` or `tee `, and none of `counts`, `reads`, `lists`, printed with their line numbers followed by `sandbox scan: unsandboxed mutation calls above (C-29); judge before the audit`; with no such line, `sandbox scan: no unsandboxed mutation call in <record>`; a missing record prints nothing; exit 0 in every case) with the repository root from `git rev-parse --show-toplevel` and an shdoc header.
4. `tests/unit/test_chain_review_scripts.py` (new), run by `uv run python -m unittest` without PyYAML, importing only the standard library, each test in a temporary directory holding a git repository with a `main` branch, a head commit and a second worktree for the review:
   - `test_local_review_runs_the_review_binary_read_only_at_the_head_and_writes_one_file`: the review worktree is a second worktree of the temporary repository created outside the repository root and named by `ORCH_REVIEW_WORKTREE`; a stub review binary records its argv, its working directory and `PATH` to a log and prints a transcript with a `codex` marker line followed by one `- [P2] …` finding. Case one, `CODEX_BIN` unset: the stub is `codex` in an absolute directory on PATH, PATH also holds the relative entry `./bin` before it, and the head commit (not the root's working tree) contains `bin/codex`, a decoy that logs to a second file; the test asserts the stub's log holds the call with the argv (`--profile review -s read-only review --base main`) and the working directory (the review worktree, whose HEAD is the given head), the decoy's log is empty (the binary was resolved in the repository root before the checkout and run by its absolute path), the repository's main working tree gained no path but the validation file (`git status --porcelain` there lists only it), the file holds the front matter and the finding, the exit is 3 with the finding line and the summary line printed. Case two, `CODEX_BIN` set to the stub: the same assertions on argv and working directory. Then: a second run on the same task and head does not run the stub (its log unchanged) and exits 3 again; a run under a second task name with a transcript of no finding exits 0; a dirty review worktree exits 2 with the stub's log unchanged; `ORCH_REVIEW_WORKTREE` naming a plain directory created inside the repository's main working tree (no `.git` entry of its own) exits 2 with the stub's log unchanged and the main working tree's HEAD unmoved.
   - `test_local_advisory_records_p2_rows_and_stops_on_p0_p1`: with a local-review file of two P2 findings, the record gains the heading, two rows and two lines once across two runs; with a P1 finding first and a P2 second, the STOP line is printed, the exit is 3, the P2's row and line are appended and the P1 gets none; with `findings: 0` nothing is appended and the exit is 0; with no file the exit is 2.
   - `test_sandbox_scan_prints_the_unsandboxed_mutation_calls`: a sandbox record with one `dangerouslyDisableSandbox … git commit` line and one `unsandboxed … counts` line prints the first with its line number and the judge line; a record with reads only prints the no-hit line; a missing record prints nothing; each exits 0.

## Out of scope

The GitHub-side scripts (the sibling task), the chain glue (`integrate-pr.sh`, `finish-pr.sh`; it stays outside the repository until every step it calls is a repository script, plan 021 step 6.3), `orch-audit.sh`, `orch-gate.sh`, `acceptance-front-matter.py`, `dispatch.sh`, any rule text, the Makefile.

## Check

`uv run python -m unittest tests/unit/test_chain_review_scripts.py -v` green, pasted in the validation file with `shellcheck scripts/orchestrator/local-review.sh scripts/orchestrator/local-advisory.sh scripts/orchestrator/sandbox-scan.sh` and `git diff --numstat origin/main...HEAD`: at most 200 changed lines (added plus deleted) outside `tests/` and outside `.orchestration/` (plan 021 step 7.2) and 1000 added lines under `tests/` (INV-2).

## Completion

One PR from a fresh branch off `origin/main` (after PR #355, merged 08:27Z as 5ec86052), pairwise-disjoint from the sibling task's files (`scripts/orchestrator/resolve-threads.sh`, `pr-cost.sh`, `tests/unit/test_chain_github_scripts.py`, its evidence directory). The PR is ready for the orchestrator's integration when the ruleset's required checks are green, the Bot's single review (on PR open) is in, every Bot thread is replied to and resolved by the orchestrator with its disposition, the validation file carries the Check's outputs, and the RESULT names every P0/P1 thread with `fixed:<sha>` and every P2 as advisory; the orchestrator's audit of the final head is dispositioned finding by finding before the gate, and a P0/P1 it leaves is the operator's decision. The Bot reviews once, at PR open; its P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P0 or P1 that survives the round stops the PR and goes to the operator as a decision; a P2 on this PR is advisory, owned by `dotfiles-T128-chain-review-scripts-followup-a01`, which the orchestrator writes when the first advisory P2 appears, before the PR's dispositions, and recorded under `## Owned by dotfiles-T128-chain-review-scripts-followup-a01` in this task's acceptance record. The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`. The RESULT names head, base, branch, files, every Bot thread with its disposition, the three test names, the caps, `task_copy=<sha256 of .orchestration/dotfiles-T128-chain-review-scripts-a01/task.md>` and the evidence paths.

## Change (round 2, 2026-10-14)

The Codex half's round 1: premise 3 counted a phrase across the whole plan file, which the orchestrator's own status line of 08:45Z changed from 8 to 9 within minutes; the premise now counts inside the step 6.3 inventory section only. Item 3 said `<task>.md` where the input reads `${task%-fixtures}.md`; the item now states the input's suffix stripping. The sibling task dropped `review-receipt.sh` (the inventory keeps the receipt as glue), so the sibling file list here names two scripts.

## Change (round 3, 2026-10-14)

The seat's round 1 (on the round-1 hash): premises 1 and 3 read untracked files of the orchestrator's checkout (the inputs, plan 021's inventory) that a worker replaying from its worktree on `origin/main` cannot see, so they are removed and the one premise left reads `origin/main`; the inputs' hashes are stated in the intro as facts. Item 4's first test gains the case that closes the row's resolution claim: `CODEX_BIN` unset, a relative `./bin` on PATH whose `codex` decoy exists only in the head commit, the decoy's log empty; the review worktree sits outside the repository root and the no-new-path assertion is on the main working tree; the no-finding run uses a second task name. Item 1 states the input's continuation on a non-zero review-binary exit; item 3 states the case-insensitive match; row 11 lists the tools each script runs.

## Change (amendment 1, 2026-10-14 09:05Z)

Why: the worker's question (bus 1149, 09:02:17Z): row 11 listed a subset of the tools the inputs run; and a review worktree path that is an existing directory but not a worktree root makes `git -C` fall through to the enclosing checkout, so a clean main checkout would pass the dirty check and be checked out detached at the PR head. What changed: row 11 lists the tools each input runs; item 1 requires the worktree path to hold its own `.git` entry (exit 2 otherwise) before the dirty check; the first test gains that case (a plain directory inside the main working tree: exit 2, the stub not run, the main HEAD unmoved); row 5 names both refusals. Nothing else. Round 2 (09:08Z, the worker's PONG of 09:05Z): item 1 also names the `mktemp` template `${TMPDIR:-/tmp}/local-review.XXXXXX`, a change to the input's behaviour the worker had to make under the sandbox.


BRANCH .orchestration/dotfiles-T128-chain-review-scripts-a01/task.md
1: ---
2: format: 2
3: task_id: dotfiles-T128-chain-review-scripts-a01
4: kind: code
5: security: false
6: design_review:
7:   receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
8:   design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
9: allowed_files:
10:   - scripts/orchestrator/local-review.sh
11:   - scripts/orchestrator/local-advisory.sh
12:   - scripts/orchestrator/sandbox-scan.sh
13:   - tests/unit/test_chain_review_scripts.py
14:   - .orchestration/dotfiles-T128-chain-review-scripts-a01/**
15: after: [dotfiles-T128-gate-wrapper-path-a01]
16: threat_table:
17:   - control: the PR adds scripts/orchestrator/local-review.sh, which checks the review worktree out at a PR head and runs the review binary there read-only, writing one validation file
18:     disposition: "closed: tests/unit/test_chain_review_scripts.py::test_local_review_runs_the_review_binary_read_only_at_the_head_and_writes_one_file"
19:   - control: the PR adds scripts/orchestrator/local-advisory.sh, which appends advisory rows and local-finding lines to an acceptance record and stops on a P0 or P1
20:     disposition: "closed: tests/unit/test_chain_review_scripts.py::test_local_advisory_records_p2_rows_and_stops_on_p0_p1"
21:   - control: the PR adds scripts/orchestrator/sandbox-scan.sh, which prints the unsandboxed mutation calls of a worker sandbox record
22:     disposition: "closed: tests/unit/test_chain_review_scripts.py::test_sandbox_scan_prints_the_unsandboxed_mutation_calls"
23:   - control: the PR adds tests/unit/test_chain_review_scripts.py, the oracle of the three rows above (a stub review binary on CODEX_BIN that records argv, cwd and environment and prints a canned transcript; a temporary git repository with a main branch and a head commit as the review worktree; fixture texts the tests write)
24:     disposition: "residual: the stubs record and print, nothing else; the audit reads each case against the Files items"
25:   - control: "the review worktree (the path ORCH_REVIEW_WORKTREE names when set, else <root>/.claude/worktrees/orchestrator-review): local-review.sh refuses with exit 2 a path that is not a worktree root (no .git entry at the path itself, so git -C cannot fall through to an enclosing checkout) and a dirty one, checks the head out detached and restores nothing (the chain's audit wrapper restores it)"
26:     disposition: "residual: the orchestrator's own worktree, detached at origin/main between runs; both refusals are covered by the first closed row's cases (amendment 1 adds the non-worktree case); the restore belongs to orch-audit.sh on main"
27:   - control: the task-file copy on the branch (.orchestration/dotfiles-T128-chain-review-scripts-a01/task.md)
28:     disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
29:   - control: the branch evidence records under .orchestration/dotfiles-T128-chain-review-scripts-a01/ (report.md, validation.md, sandbox.md, learning.md)
30:     disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
31:   - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
32:     disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
33:   - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
34:     disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
35:   - control: in-process effects
36:     disposition: "residual: the tests run the three scripts as subprocesses with the stub review binary on CODEX_BIN and real git in a temporary repository, and import only the standard library; nothing is imported into another process"
37:   - control: workflow and interpreter or environment inputs
38:     disposition: "residual: no workflow or interpreter file is in allowed_files; local-review.sh runs git, mktemp and the review binary (the value of CODEX_BIN when the environment sets it, the test seam, else codex resolved with command -v in the repository root before the head checkout, its absolute path used afterwards; the profile review is fixed in the script, the model-selection rule); local-review.sh also runs awk, sed, date, cut, grep, sort, head and rm; local-advisory.sh runs git rev-parse, grep, sed, cut, tr, head and sort; sandbox-scan.sh runs git rev-parse and grep; the review binary runs with the PR head as its working directory under its own read-only sandbox, so the PR's content (its AGENTS.md, its configuration files) is input to that review and never to the gate: the review's findings are a sample the orchestrator judges (advisory rows or a stop), and the script writes nothing but the validation file"
39:   - control: new or renamed scripts
40:     disposition: "residual: three new scripts under scripts/orchestrator/, named in allowed_files and listed in the RESULT; any other new or renamed script is an undeclared change the audit fails"
41:   - control: orchestrator effect merge
42:     disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
43:   - control: orchestrator effect update-branch
44:     disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
45:   - control: orchestrator effect forced worker removal
46:     disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
47: premises:
48:   - claim: 'none of the three script names exists under scripts/orchestrator/ on origin/main (the task adds, it does not edit)'
49:     command: 'git ls-tree --name-only origin/main scripts/orchestrator/ | /usr/bin/grep -c -E "local-review|local-advisory|sandbox-scan" || true'
50:     output: |-
51:       0
52: ---
53: 
54: # AGMSG-TASK dotfiles-T128-chain-review-scripts-a01 — the integration chain's review-side steps become repository scripts with tests (plan 021 step 6.3; the review half of the step's "next tools task")
55: 
56: Drafted 2026-10-14 by the orchestrator seat (the bus time of its TASK line is the dispatch time), in the step-7 short form. Plan 021's step 6.3 inventory names six chain steps whose logic lives only in the orchestrator's scratchpad; the hand-typed-chain class holds fourteen mistake records today, and the structural answer is repository scripts with tests. This task lands the three review-side scripts; its sibling `dotfiles-T128-chain-github-scripts-a01` lands the two GitHub-side scripts (`resolve-threads.sh`, `pr-cost.sh`) with its own test module, so the two run concurrently on disjoint files. The attached inputs under `.orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/` of the orchestrator's main checkout (the directory the TASK line's `task_file` is read from, untracked until the next boundary) are the scripts as the chain runs them today, with the repository root resolved by `git rev-parse --show-toplevel`; their sha256 prefixes (`shasum -a 256 <dir>/*.sh | cut -c1-16`): 2e44dabc23ea0397  local-advisory.sh; 2258e370b9ff2575  local-review.sh; 099f6c7534223cb4  sandbox-scan.sh; each item names what changes. The one premise is replayable from any checkout (it reads `origin/main`).
57: 
58: ## Goal
59: 
60: The local review of a PR head, the recording of its advisory findings and the scan of a worker's sandbox record run from `scripts/orchestrator/` on `origin/main`, each with one test that closes its row, so the next integration's log names repository scripts for these steps.
61: 
62: ## Files
63: 
64: 1. `scripts/orchestrator/local-review.sh <task> <head> <pr>`: the input's behaviour (one review per head: an existing `.orchestration/validation/<task>-local-review-<sha7>.md` is reused and re-reported with its finding lines and `local-review: <n> findings (existing <file>)`; otherwise the head must be a local commit, exit 2 if not; the review worktree path must hold a `.git` entry of its own (a worktree root; a plain directory inside a checkout would let `git -C` act on the enclosing checkout), exit 2 if not, and be clean, exit 2 if not; the worktree is checked out detached at the head; the review binary runs there as `<binary> --profile review -s read-only review --base main` with stdin from `/dev/null`; the transcript's final message after the `codex` marker line is kept with the worktree prefix stripped; the unique lines matching `^- \[P[0-3]\]` are the findings; the file gets the front matter the input writes: task, head, pr, base, started, finished, findings, engine; the findings are printed, then `local-review: <n> findings (<file>)`; a non-zero exit of the review binary prints `local-review: codex exited <n> (see <file>)` and the file is still written from whatever transcript came back; exit 0 with no finding, 3 with findings, 2 on a precondition) with these changes: the repository root is `git rev-parse --show-toplevel`; the review worktree is `$ORCH_REVIEW_WORKTREE` when set, else `<root>/.claude/worktrees/orchestrator-review`; the review binary is `$CODEX_BIN` when set, else `codex` resolved with `command -v` in the repository root before the checkout and used by that absolute path afterwards; the profile `review` stays fixed in the script; the transcript's temporary file comes from `mktemp` with the template `${TMPDIR:-/tmp}/local-review.XXXXXX` (macOS `mktemp` without a template ignores `TMPDIR` and uses the per-user directory, which the Bash sandbox denies; the form `orch-gate.sh` uses); an shdoc header; `bash -n` and shellcheck clean.
65: 2. `scripts/orchestrator/local-advisory.sh <task> <head40> <owner-task-id>`: the input's behaviour (reads `.orchestration/validation/<task>-local-review-<sha7>.md`, exit 2 when absent; `findings: 0` prints `local review of <sha7>: no findings` and exits 0; otherwise ensures the heading `## Owned by <owner> (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)` in `.orchestration/acceptance/<task>.md`; then for each unique finding line in order, numbered from 1: a `[P0]` or `[P1]` prints `STOP: local finding <n> of <sha7> is P0/P1: <line>` and makes the exit 3, any other appends the row `local:<sha7>:<n><TAB>advisory-p2` and the line `local-finding: <sha7>:<n> not-applicable:advisory P2 owned by <owner> (<the finding's first 120 characters, backticks removed>); evidence=git show origin/main:.orchestration/tasks/<owner>.md | grep -n 'item 1'`, each only when the record lacks it; last line `local review of <sha7>: <i> finding(s) recorded as advisory under 'Owned by <owner>' in <record>`) with the repository root from `git rev-parse --show-toplevel` and an shdoc header.
66: 3. `scripts/orchestrator/sandbox-scan.sh <task>`: the input's behaviour (over `.orchestration/sandboxes/<task>.md`, where a trailing `-fixtures` of `<task>` is stripped as the input does with `${task%-fixtures}`: the lines matching, case-insensitively as the input's `grep -i` does, `dangerouslyDisableSandbox`, `outside the sandbox` or `unsandboxed` that also match a mutation, `git commit`, `git switch -c`, `git checkout`, `git add`, `git mv`, `git rm`, `cp `, `mv `, `> ` or `tee `, and none of `counts`, `reads`, `lists`, printed with their line numbers followed by `sandbox scan: unsandboxed mutation calls above (C-29); judge before the audit`; with no such line, `sandbox scan: no unsandboxed mutation call in <record>`; a missing record prints nothing; exit 0 in every case) with the repository root from `git rev-parse --show-toplevel` and an shdoc header.
67: 4. `tests/unit/test_chain_review_scripts.py` (new), run by `uv run python -m unittest` without PyYAML, importing only the standard library, each test in a temporary directory holding a git repository with a `main` branch, a head commit and a second worktree for the review:
68:    - `test_local_review_runs_the_review_binary_read_only_at_the_head_and_writes_one_file`: the review worktree is a second worktree of the temporary repository created outside the repository root and named by `ORCH_REVIEW_WORKTREE`; a stub review binary records its argv, its working directory and `PATH` to a log and prints a transcript with a `codex` marker line followed by one `- [P2] …` finding. Case one, `CODEX_BIN` unset: the stub is `codex` in an absolute directory on PATH, PATH also holds the relative entry `./bin` before it, and the head commit (not the root's working tree) contains `bin/codex`, a decoy that logs to a second file; the test asserts the stub's log holds the call with the argv (`--profile review -s read-only review --base main`) and the working directory (the review worktree, whose HEAD is the given head), the decoy's log is empty (the binary was resolved in the repository root before the checkout and run by its absolute path), the repository's main working tree gained no path but the validation file (`git status --porcelain` there lists only it), the file holds the front matter and the finding, the exit is 3 with the finding line and the summary line printed. Case two, `CODEX_BIN` set to the stub: the same assertions on argv and working directory. Then: a second run on the same task and head does not run the stub (its log unchanged) and exits 3 again; a run under a second task name with a transcript of no finding exits 0; a dirty review worktree exits 2 with the stub's log unchanged; `ORCH_REVIEW_WORKTREE` naming a plain directory created inside the repository's main working tree (no `.git` entry of its own) exits 2 with the stub's log unchanged and the main working tree's HEAD unmoved.
69:    - `test_local_advisory_records_p2_rows_and_stops_on_p0_p1`: with a local-review file of two P2 findings, the record gains the heading, two rows and two lines once across two runs; with a P1 finding first and a P2 second, the STOP line is printed, the exit is 3, the P2's row and line are appended and the P1 gets none; with `findings: 0` nothing is appended and the exit is 0; with no file the exit is 2.
70:    - `test_sandbox_scan_prints_the_unsandboxed_mutation_calls`: a sandbox record with one `dangerouslyDisableSandbox … git commit` line and one `unsandboxed … counts` line prints the first with its line number and the judge line; a record with reads only prints the no-hit line; a missing record prints nothing; each exits 0.
71: 
72: ## Out of scope
73: 
74: The GitHub-side scripts (the sibling task), the chain glue (`integrate-pr.sh`, `finish-pr.sh`; it stays outside the repository until every step it calls is a repository script, plan 021 step 6.3), `orch-audit.sh`, `orch-gate.sh`, `acceptance-front-matter.py`, `dispatch.sh`, any rule text, the Makefile.
75: 
76: ## Check
77: 
78: `uv run python -m unittest tests/unit/test_chain_review_scripts.py -v` green, pasted in the validation file with `shellcheck scripts/orchestrator/local-review.sh scripts/orchestrator/local-advisory.sh scripts/orchestrator/sandbox-scan.sh` and `git diff --numstat origin/main...HEAD`: at most 200 changed lines (added plus deleted) outside `tests/` and outside `.orchestration/` (plan 021 step 7.2) and 1000 added lines under `tests/` (INV-2).
79: 
80: ## Completion
81: 
82: One PR from a fresh branch off `origin/main` (after PR #355, merged 08:27Z as 5ec86052), pairwise-disjoint from the sibling task's files (`scripts/orchestrator/resolve-threads.sh`, `pr-cost.sh`, `tests/unit/test_chain_github_scripts.py`, its evidence directory). The PR is ready for the orchestrator's integration when the ruleset's required checks are green, the Bot's single review (on PR open) is in, every Bot thread is replied to and resolved by the orchestrator with its disposition, the validation file carries the Check's outputs, and the RESULT names every P0/P1 thread with `fixed:<sha>` and every P2 as advisory; the orchestrator's audit of the final head is dispositioned finding by finding before the gate, and a P0/P1 it leaves is the operator's decision. The Bot reviews once, at PR open; its P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P0 or P1 that survives the round stops the PR and goes to the operator as a decision; a P2 on this PR is advisory, owned by `dotfiles-T128-chain-review-scripts-followup-a01`, which the orchestrator writes when the first advisory P2 appears, before the PR's dispositions, and recorded under `## Owned by dotfiles-T128-chain-review-scripts-followup-a01` in this task's acceptance record. The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`. The RESULT names head, base, branch, files, every Bot thread with its disposition, the three test names, the caps, `task_copy=<sha256 of .orchestration/dotfiles-T128-chain-review-scripts-a01/task.md>` and the evidence paths.
83: 
84: ## Change (round 2, 2026-10-14)
85: 
86: The Codex half's round 1: premise 3 counted a phrase across the whole plan file, which the orchestrator's own status line of 08:45Z changed from 8 to 9 within minutes; the premise now counts inside the step 6.3 inventory section only. Item 3 said `<task>.md` where the input reads `${task%-fixtures}.md`; the item now states the input's suffix stripping. The sibling task dropped `review-receipt.sh` (the inventory keeps the receipt as glue), so the sibling file list here names two scripts.
87: 
88: ## Change (round 3, 2026-10-14)
89: 
90: The seat's round 1 (on the round-1 hash): premises 1 and 3 read untracked files of the orchestrator's checkout (the inputs, plan 021's inventory) that a worker replaying from its worktree on `origin/main` cannot see, so they are removed and the one premise left reads `origin/main`; the inputs' hashes are stated in the intro as facts. Item 4's first test gains the case that closes the row's resolution claim: `CODEX_BIN` unset, a relative `./bin` on PATH whose `codex` decoy exists only in the head commit, the decoy's log empty; the review worktree sits outside the repository root and the no-new-path assertion is on the main working tree; the no-finding run uses a second task name. Item 1 states the input's continuation on a non-zero review-binary exit; item 3 states the case-insensitive match; row 11 lists the tools each script runs.
91: 
92: ## Change (amendment 1, 2026-10-14 09:05Z)
93: 
94: Why: the worker's question (bus 1149, 09:02:17Z): row 11 listed a subset of the tools the inputs run; and a review worktree path that is an existing directory but not a worktree root makes `git -C` fall through to the enclosing checkout, so a clean main checkout would pass the dirty check and be checked out detached at the PR head. What changed: row 11 lists the tools each input runs; item 1 requires the worktree path to hold its own `.git` entry (exit 2 otherwise) before the dirty check; the first test gains that case (a plain directory inside the main working tree: exit 2, the stub not run, the main HEAD unmoved); row 5 names both refusals. Nothing else. Round 2 (09:08Z, the worker's PONG of 09:05Z): item 1 also names the `mktemp` template `${TMPDIR:-/tmp}/local-review.XXXXXX`, a change to the input's behaviour the worker had to make under the sandbox.

**Analyzing security risks in environment and hooks**
**Verifying runtime binaries and config documentation**
codex
3 本の実装とテストを確認しました。`CODEX_BIN` 未設定時の decoy 回避と、`.git` を持たないディレクトリの拒否には明示的な検証があります。次に入力版との差分、書き込み先の制約、環境変数が実行先に与える影響を確認します。`gh` は接続に失敗したため、CI は保存済み証跡と GitHub コネクタで照合します。
exec
/bin/zsh -lc "python3 -B -c 'import pathlib,hashlib,subprocess,difflib; h=\"b6ce4ffabe0e66a102e224e75be575a501c5a793\"; root=pathlib.Path(\"~/Workspace/dotfiles\"); p=root/\".orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input\"; [(print(\"INPUT\",f.name,hashlib.sha256(f.read_bytes()).hexdigest()),print(\"\".join(difflib.unified_diff(f.read_text().splitlines(True),subprocess.check_output([\"git\",\"show\",h+\":scripts/orchestrator/\"+f.name],text=True).splitlines(True),fromfile=\"input/\"+f.name,tofile=\"head/\"+f.name)))) for f in sorted(p.glob(\"*.sh\"))]; p=\".orchestration/tasks/dotfiles-T128-chain-review-scripts-a01.md\"; a=pathlib.Path(p).read_bytes(); b=subprocess.check_output([\"git\",\"show\",h+\":.orchestration/dotfiles-T128-chain-review-scripts-a01/task.md\"]); print(\"Task copy equal\",a==b,\"sha256\",hashlib.sha256(b).hexdigest())'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc "python3 -B -c 'import pathlib; paths=[\".orchestration/reports/dotfiles-T128-chain-review-scripts-a01.md\",\".orchestration/sandboxes/dotfiles-T128-chain-review-scripts-a01.md\",\".orchestration/acceptance/dotfiles-T128-chain-review-scripts-a01.md\"]; [(print(\"\\nFILE \"+p),print(\"\\n\".join(str(i)+\": \"+line for i,line in enumerate(pathlib.Path(p).read_text().split(\"<"'!-- audit-input-boundary -->")[0].splitlines(),1)))) for p in paths]'"'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc "python3 -B -c 'import json,pathlib,subprocess; p=pathlib.Path(\".ua/knowledge-graph.json\"); m=pathlib.Path(\".ua/meta.json\"); meta=json.loads(m.read_text()) if m.exists() else {}; rev=meta.get(\"gitCommitHash\"); print(\"graph\",p.exists(),\"revision\",rev); d=json.loads(p.read_text()) if p.exists() else {}; nodes=[(n.get(\"filePath\"),n.get(\"summary\")) for n in d.get(\"nodes\",[]) if any(s in (n.get(\"filePath\",\"\")+n.get(\"summary\",\"\")) for s in [\"orchestrator/\", \"local-review\", \"chain-review\", \"021-\"])]; print(\"relevant nodes\",nodes[:15]); print(\"changes from graph\",subprocess.check_output([\"git\",\"diff\",\"--name-only\",rev+\"..HEAD\"],text=True)[:3000] if rev else \"no graph revision\")'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 177ms:

FILE .orchestration/reports/dotfiles-T128-chain-review-scripts-a01.md
1: ---
2: task_id: dotfiles-T128-chain-review-scripts-a01
3: seat: claude-standard-dot-a002
4: branch: regime/chain-review-scripts
5: base: 5ec86052ff0f8ef0fa7dbdbbd44e1e389ba9eb6c
6: code_commit: 1f307a6e
7: pr: 357
8: task_sha256: db9ff03a5eb720a4778fc357fb351926e7ecbb1d5af7a5f6cf11266232ba060b
9: ---
10: 
11: # Report: dotfiles-T128-chain-review-scripts-a01
12: 
13: - Seat: `claude-standard-dot-a002` in `.claude/worktrees/worker-f`, on a fresh branch `regime/chain-review-scripts` from `origin/main` `5ec86052` (PR #355 merged), PR #357.
14: - Task file: amendment 1, sha256 `db9ff03a…`, copied byte-identical to `.orchestration/dotfiles-T128-chain-review-scripts-a01/task.md` (validation §1). The attached inputs are untouched; their sha256 prefixes equal the intro's (validation §2).
15: - Round 1 was dispatched at 08:54:36Z. One question followed, at 09:02Z, before any commit:
16:   - row 11 listed a subset of the tools the inputs run;
17:   - a review-worktree path that exists but is not a worktree root lets `git -C` act on the enclosing checkout.
18: 
19:   A working PONG at 09:05Z declared the `mktemp` template. Amendment 1 (12:17:36Z, `db9ff03a`) answered all three: row 11's full tool list, item 1's `.git`-entry refusal with its test case, and item 1's `mktemp` template.
20: 
21: ## Commits
22: 
23: | Commit | What |
24: |---|---|
25: | `1f307a6e` | Items 1 to 4 with amendment 1 |
26: | `0da6be3e` | Task copy at `db9ff03a` and the first evidence; the Bot's one review was of this head |
27: | this commit | The evidence update: the Bot's threads, CI and the sandbox rows |
28: 
29: ## What landed
30: 
31: | Item | File | What it does |
32: |---|---|---|
33: | 1 | `scripts/orchestrator/local-review.sh` | The input, with item 1's changes, nothing else (validation §3 diffs it against the input):<br>- the root from `git rev-parse --show-toplevel`, and `cd` there;<br>- the review worktree `$ORCH_REVIEW_WORKTREE`, else `<root>/.claude/worktrees/orchestrator-review`, refused with exit 2 without its own `.git` entry, before the dirty check (amendment 1);<br>- the binary `command -v "${CODEX_BIN:-codex}"` in the root before the checkout, made absolute against the root when relative, exit 2 when none;<br>- `mktemp "${TMPDIR:-/tmp}/local-review.XXXXXX"` (amendment 1);<br>- the shdoc header. |
34: | 2 | `scripts/orchestrator/local-advisory.sh` | The input, shfmt-formatted, with the shdoc header. |
35: | 3 | `scripts/orchestrator/sandbox-scan.sh` | The input, shfmt-formatted, with the shdoc header. |
36: | 4 | `tests/unit/test_chain_review_scripts.py` (new) | The three tests item 4 names; see below. |
37: 
38: Notes on meaning:
39: 
40: - Item 1's binary reads as one resolution for both sources: the binary is `command -v` of `$CODEX_BIN`, else of `codex`, run in the root. An absolute `$CODEX_BIN` is used as it is. A relative one, like a relative PATH hit, is made absolute against the root, so nothing resolves inside the review worktree. A missing binary is a precondition, exit 2. The input would have run `codex` anyway and recorded exit 127.
41: - Every other line keeps the input's text and order. Validation §3 diffs each port against its input after running the input through CI's shfmt (`-i 4 -sr` on `scripts/**/*.sh`). Beyond item 1's changes and the headers, it shows three layout edits: `local-advisory.sh` takes its three arguments in one assignment and its two counters in another, and `sandbox-scan.sh`'s one-line `if … then … else … fi` spans five lines. None changes behaviour.
42: 
43: ## Tests
44: 
45: The Check: 3 tests OK (validation §4); the whole unit suite: the four modules that exercise `scripts/orchestrator/`, 53 tests OK; the whole suite is CI's (validation intro) (validation §7). The cases:
46: 
47: - **`test_local_review_runs_the_review_binary_read_only_at_the_head_and_writes_one_file`:** item 4's cases, in this order:
48:   - the plain-directory case (amendment 1), run first, while the main working tree is still clean, since otherwise the dirty check alone would refuse it;
49:   - case one (`CODEX_BIN` unset, `./bin` decoy in the head);
50:   - case two (`CODEX_BIN` set);
51:   - the reuse;
52:   - the no-finding run under a new task name;
53:   - the dirty worktree.
54: - **`test_local_advisory_records_p2_rows_and_stops_on_p0_p1`:** item 4's four cases.
55: - **`test_sandbox_scan_prints_the_unsandboxed_mutation_calls`:** item 4's three cases.
56: 
57: Cases beyond item 4's text, each added to close a mutation the listed cases left alive (validation §8):
58: 
59: - local-review:
60:   - The stub records its stdin, and the caller gives it some, so `< /dev/null` is checked.
61:   - The transcript holds an earlier `codex` marker with a `[P1]` line, so only the final message counts, and one finding twice, so the unique count is checked.
62:   - Every finding carries the worktree prefix, so the stripping is checked.
63:   - No `local-review.*` temporary file is left under `TMPDIR`.
64:   - Case two passes `CODEX_BIN` as a path relative to the root and runs from a subdirectory, so both the `cd` and the absolute path are checked.
65:   - The no-finding run's binary exits 5: `codex exited 5` is printed, the file is still written, and the exit is 0.
66:   - A missing `CODEX_BIN` and an unknown head each exit 2, and nothing runs.
67: - local-advisory:
68:   - The two P2 lines are written out of sort order, so the numbering follows `sort -u`.
69:   - One P2 line is longer than 120 characters and holds backticks, so the cut and the removal are checked.
70:   - A review with one `[P0]` line prints STOP and exits 3.
71: - sandbox-scan:
72:   - A `-fixtures` task id reads the stripped record, and its line is matched in other letter case.
73:   - The `counts` line is written `Counts`.
74:   - The reads-only record holds a `> ` line excluded by `reads` and a `tee ` line excluded by `lists`.
75: 
76: Mutation pass: 57 mutations, 57 caught, across every refusal and exit, each item-1 change, the front matter, the advisory row and line text, and each scan filter (validation §8).
77: 
78: ## Caps
79: 
80: Validation §6:
81: 
82: - outside `tests/` and `.orchestration/`: 3 files, 148 added + 0 deleted = 148 changed lines (cap 200);
83: - under `tests/`: 230 added lines (cap 1000);
84: - 4 files outside `.orchestration/`.
85: 
86: ## CI and the Bot
87: 
88: - **The Bot:** PR #357 was opened as a draft and marked ready (12:42:37Z) after the evidence commit, so the Bot's one review saw the whole PR. That review, 5518077170 at 12:45:21Z of `0da6be3e`, raised two inline threads, both P2, and its body holds no badge (validation §9). No P0 or P1, so there is no fix round. Each P2 is advisory, proposed for `dotfiles-T128-chain-review-scripts-followup-a01`:
89: 
90:   | Thread | Where | Finding | Proposed disposition |
91:   |---|---|---|---|
92:   | 4270918132 | `local-review.sh:61` | A non-zero review-binary exit still writes the file, with `findings: 0` when no finding came back, and the next run on that head reuses it as a review. | advisory P2: the input's continuation, which item 1 states (`the file is still written from whatever transcript came back`) |
93:   | 4270918140 | `local-review.sh:28` | The reuse is keyed by the head's first seven characters; the file's full `head:` is never compared, so a second head with the same prefix is not reviewed. | advisory P2: the input's file name and reuse, which item 1 states (`<task>-local-review-<sha7>.md` is reused) |
94: 
95:   The worker resolves no thread.
96: - **CI on `0da6be3e`:** 13 of 13 checks pass, the four `test` jobs (`make unit-test` and the bats suites) among them (validation §9). The suite's failures under the Claude sandbox (validation intro) are therefore environmental.
97: - **CI on the final head (this commit):** in the RESULT.
98: 
99: ## Not done, or outside scope
100: 
101: - `cut -c1-2000` of the transcript is checked only through mutation R26 (`cut -c1-20`); no case holds a line over 2000 characters.
102: - Understand-Anything hook: did not fire. plan-mode-used: no.
103: - cost: n/a (the runtime exposes no session figures to the seat).

FILE .orchestration/sandboxes/dotfiles-T128-chain-review-scripts-a01.md
1: ---
2: task_id: dotfiles-T128-chain-review-scripts-a01
3: seat: claude-standard-dot-a002
4: permission_gated_commands: see the table
5: ---
6: 
7: # Sandbox record: dotfiles-T128-chain-review-scripts-a01
8: 
9: - Period: from the AGMSG-TASK (08:54:36Z) to the RESULT.
10: - Inside the sandbox ran:
11:   - the HTTPS `git fetch` and `git push`;
12:   - the branch, the commit, the task copy and the evidence;
13:   - every test, lint and format run;
14:   - the mutation pass and the validation script.
15: - In the sandbox uv cannot reach pypi, so every uv run used `UV_OFFLINE=1` from the uv cache (validation, header). `uvx ruff` could not write uv's tool directory, so ruff ran as the installed `ruff` 0.17.0.
16: - macOS `mktemp` without a template writes under `/var/folders/…`, which the sandbox denies. That is why item 1 now names a template (amendment 1, learning 1).
17: - `diff` cannot open a `/dev/fd` process substitution in the sandbox, so validation §3 diffs scratch files instead.
18: - The whole unit suite fails in the sandbox (validation, intro); CI's run is the evidence.
19: - No local mutation was chained onto a call that ran outside the sandbox.
20: 
21: The table lists every call that ran outside the sandbox: `gh` through the permission gate (`dangerouslyDisableSandbox`, since `gh` fails TLS inside the sandbox) and `agmsg-dispatch` through `excludedCommands`. Rows after the evidence commit are completed in the evidence update.
22: 
23: | # | Command | Step 4 case |
24: |--:|---|---|
25: | 1 | `agmsg-dispatch … AGMSG-PONG v1 task_id=dotfiles-T128-chain-review-scripts-a01 status=question …` (09:02Z, row 11 and the worktree guard) | `agmsg-dispatch` |
26: | 2 | `agmsg-dispatch … AGMSG-PONG v1 … status=working …` (09:05Z, the `mktemp` template) | `agmsg-dispatch` |
27: | 3 | `agmsg-dispatch … AGMSG-PONG v1 … status=working …` (12:15Z, the branch state) | `agmsg-dispatch` |
28: | 4 | `gh pr create --draft --repo mryfmo/dotfiles --base main --head regime/chain-review-scripts …` (PR #357) | `gh` |
29: | 5 | `gh pr ready 357 --repo mryfmo/dotfiles; date +%s; date -u +%FT%TZ` (12:42:37Z) | `gh` |
30: | 6 | the Bot wait on `0da6be3e` (`scratchpad/bot-wait.sh`, background; `gh pr view` and `gh api` reads every 30 seconds) | `gh` |
31: | 7 | `gh pr checks 357 --watch` (background, after a `gh pr checks` poll for the first check; exit 0) | `gh` |
32: | 8 | `gh api` reads of the two Bot comments and of review 5518077170's body | `gh` |
33: | 9 | `gh api` re-list of the Bot's top-level comments (validation §9) | `gh` |
34: | 10 | `agmsg-dispatch … AGMSG-PONG v1 … status=alive …` (12:47Z, the Bot's two P2 threads) | `agmsg-dispatch` |
35: | 11 | `gh pr checks 357 --watch` on the final head (background, exit status joined) | `gh` |
36: | 12 | `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T128-chain-review-scripts-a01 …` | `agmsg-dispatch` |
37: 
38: One command was denied at the permission gate and not pursued: a re-list that ran four reads in one call, the Bot's comment count, the PR's reviews, its issue comments and a GraphQL listing of its review threads. The GraphQL thread listing is not needed, since the worker resolves no thread. Row 9 ran the comment re-list alone, the same `gh api …/pulls/357/comments` read that row 8 had already run.
39: 
40: The pushes of `1f307a6e`, `0da6be3e` and the evidence update ran inside the sandbox over HTTPS.

FILE .orchestration/acceptance/dotfiles-T128-chain-review-scripts-a01.md
1: ---
2: {
3:   "format": 1,
4:   "task": "dotfiles-T128-chain-review-scripts-a01",
5:   "head": "b6ce4ffabe0e66a102e224e75be575a501c5a793",
6:   "pr": 357,
7:   "ledger": [
8:     {
9:       "id": "4270918132",
10:       "class": "stale-review-file-on-error"
11:     },
12:     {
13:       "id": "4270918140",
14:       "class": "reuse-keyed-by-sha7"
15:     }
16:   ],
17:   "searches": [],
18:   "audit_findings": []
19: }
20: ---
21: 
22: # Acceptance record: dotfiles-T128-chain-review-scripts-a01 (plan 021 step 6.3, the review-side chain scripts with tests; step-7 short form; Claude seat)
23: 
24: - 2026-10-14 08:35Z task text written by the orchestrator seat (record created before the first dispatch, Orchestrator Playbook step 6); attached inputs under `.orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/` (three scripts, repository root resolved, masker clean, `bash -n` clean); input checker `dotfiles-T128-chain-review-scripts-a01.md: OK`; brief check clean (three premises re-run equal; mask clean; 15 controls, 3 claims); file hash `08e2db785d8dfb741651d6e605bc45209f8d45071e6dd8ceec349feca32e0987`; its paired one-round review (brief `dotfiles-T128-chain-review-scripts-a01-review-a01`, the review seat and the Codex half) dispatched next.
25: - 08:36Z the Codex half, round 1: `revise` (The Codex half's round 1: P1 premise 3 counted a phrase over the whole plan file, which the orchestrator's 08:45Z status line changed from 8 to 9 (now counted inside the step 6.3 inventory section; M-20261014-11, C-45); P1 item 3 said `<task>.md` where the input reads `${task%-fixtures}.md` (now stated). The sibling dropped `review-receipt.sh`, so the Completion's sibling list names two scripts.). Applied 08:41Z (the task's Change section); the seat's round 1 is pending on the old hash and is superseded by round 2, dispatched to both halves on the new hash `62e6035e1cacdc4a0caa725798c818b99f7bdde1d85f89d8380fdb42b3a4d453`.
26: - 08:41:17Z the Codex half, round 2: `confirm` on 62e6035e (receipt `validation/dotfiles-T128-chain-review-scripts-review-a01-codex-r2.md`); the seat's half pending (its round-1 line read 08:35:58Z, round 2 on the bus).
27: - 08:45Z round 3 on `af6556ba591a742f155fea5a649be9c579b95210dee56104babf4256018fcdd7`: The seat's round 1 (08:43:35Z, on the round-1 hash): P2 premise 3 read an uncommitted plan file (0 on origin/main) so a worker's replay would block; P2 the row-1 test could not close the resolve-before-checkout claim with CODEX_BIN set in every case; P3 item 3's dropped behaviours (suffix strip, case-insensitive match), P3 item 1's non-zero-exit continuation, P3 the only-path assertion against the default worktree under the repository and the reused file, P3 row 11's tool list. Applied: premises 1 and 3 removed (the inputs and the plan are untracked until the boundary; the inputs' hashes are stated as facts in the intro), the one premise left reads origin/main; the first test gains the CODEX_BIN-unset case with a relative ./bin decoy present only in the head commit, the worktree outside the repository root (ORCH_REVIEW_WORKTREE) and the no-new-path assertion on the main working tree, a second task name for the no-finding run; items 1 and 3 and row 11 state what the seat named.
28: - 08:47:11Z the Codex half, round 3: `confirm` on af6556ba (receipt `validation/dotfiles-T128-chain-review-scripts-review-a01-codex-r3.md`); the seat's round 3 pending.
29: - 08:51:24Z the seat, round 3: `confirm` on af6556ba. **Text pair-confirmed on `af6556ba591a742f155fea5a649be9c579b95210dee56104babf4256018fcdd7`** (three rounds: the Codex half's two P1 in round 1, the seat's two P2 and four P3 in its round 1 on the first hash; both halves confirm round 3). ACCEPTANCE accepted to the seat; the TASK line to `claude-standard-dot-a002` (worker-f, w5:p9) with this record (the line in the dispatch list above once read).
30: - **Dispatched 08:54:36Z to `claude-standard-dot-a002` (worker-f, w5:p9), bus 1143, read** (the line in the dispatch list above); ACCEPTANCE accepted for the review to the seat 08:54:31Z (bus 1142, read; a queued duplicate from the dispatch command may follow).
31: - 09:02:17Z a002 PONG `status=question` (bus 1149; branch `regime/chain-review-scripts` from 5ec86052; the premise replayed 0; the inputs' hashes match): q1 row 11 lists a subset of the tools the inputs run (local-review.sh also grep, sort, head, rm; local-advisory.sh also head, sort); q2 a review worktree path that exists but is not a worktree root makes `git -C` fall through to the enclosing checkout, so a clean main checkout would pass the dirty check and be checked out at the PR head; may it add one refusal line. Both are task text: PING hold 09:05Z; amendment 1 written (row 11; item 1's worktree-root refusal; the test case; row 5), checker OK, mask clean; its paired review dispatched to the seat and the Codex half; the pre-amendment copy at `.orchestration/validation/dotfiles-T128-chain-review-scripts-a01-pre-amend1.md`.
32: - 09:05:25Z a002 PONG (working; holding the PR; three scripts and the test module drafted, 141 script lines, 3 tests green): one more change beyond item 1, the `mktemp` template under the sandbox; PING 09:0xZ: it joins amendment 1 as round 2 (item 1 names the template); round 2 to both halves on the new hash.
33: - 12:13Z after the host slept (about 09:10Z to 12:12Z): amendment 1 round 2 (db9ff03a) has the Codex half's `confirm` (09:10:02Z, receipt `-codex-r2.md`) and the seat's round-2 line read 09:09:01Z with no RESULT yet; the seat's round-1 confirm (b875d247, 09:07:31Z) superseded; the hold PING of 09:06:37Z (bus 1153) unread by a002; wake PINGs to the seat and a002 at 12:13Z.
34: - 12:13:39Z the seat, round 2: `confirm` on db9ff03a (after the wake PING). **Amendment 1 pair-confirmed on `db9ff03a5eb720a4778fc357fb351926e7ecbb1d5af7a5f6cf11266232ba060b`** (round 1 b875d247 confirmed by both at 09:07Z, superseded by round 2 with the mktemp template: Codex 09:10:02Z, the seat 12:13:39Z); ACCEPTANCE accepted to the seat 12:14Z; the amended TASK line (`amendment=1`, `previous_task_sha256` af6556ba, the pre-amendment copy at `validation/dotfiles-T128-chain-review-scripts-a01-pre-amend1.md`) to a002 (the line in the dispatch list above once read).
35: - 12:17:36Z the amended TASK line (amendment 1, db9ff03a) read by a002 (bus 1163; the line in the dispatch list above).
36: - 12:46:40Z a002 PONG (alive): PR #357 open, head `0da6be3e`; the Bot's single review 5518077170 at 12:45:21Z (165 s after ready): two inline threads, both P2, no P0/P1, no badge in the body: 4270918132 (local-review.sh:61, a non-zero review-binary exit still writes a `findings: 0` file that the next run reuses, the input's continuation item 1 states) and 4270918140 (local-review.sh:28, the reuse is keyed by the sha7 prefix and never compares the recorded full head, the input's file name item 1 states); the worker proposes both as advisory for the follow-up (no fix round); CI running on 0da6be3e; next the evidence update and the RESULT; one `gh` read (a REST plus GraphQL thread listing) was denied at the permission gate and not retried, recorded in its sandbox file. 12:47Z: the owner task `dotfiles-T128-chain-review-scripts-followup-a01` written (the GitHub-side owner's shape; 15 controls, 2 premises each `absent` today; checker OK; mask clean; hash 2f7cd314) before any disposition (C-32); its paired review dispatched to the seat and the Codex half; `357-extra.tsv` holds both threads' advisory dispositions (no semicolon in a reason, C-47); the two rows below and the owner section opened now (C-42).
37: 
38: 4270918132	stale-review-file-on-error
39: 4270918140	reuse-keyed-by-sha7
40: 
41: - 13:21Z chain run 1 on PR #357: `update-branch` 13:08:33Z (main ec94dc56 was not an ancestor of 04a7d02a) gave the merge head `b6ce4ffabe0e66a102e224e75be575a501c5a793`; required checks green; no new Bot review; sweep 9 items filled (the two Bot threads from `357-extra.tsv`); the local review of b6ce4ff (`codex review --base main`, 13:1xZ) found two findings: a P1 (local-review.sh:61, fail closed when the review process exits non-zero: today a failed run writes a `findings: 0` file the next run reuses as a clean review) and a P2 (local-review.sh:27 to 28, verify the full commit before reusing a cached review). Both are the defects the Bot's single review rated P2 (threads 4270918132 and 4270918140), and item 1 of the task prescribes the first as the input's continuation, so the fix is a change of the task's own text owned by the follow-up; the local review is the second sampler (C-32), and its P1 rating goes to the audit as input (plan 021 S21). The chain stopped for the hand-filed lines below and resumes.
42: 
43: local:b6ce4ff:1	stale-review-file-on-error
44: local:b6ce4ff:2	reuse-keyed-by-sha7
45: local-finding: b6ce4ff:1 not-applicable:advisory P2 owned by dotfiles-T128-chain-review-scripts-followup-a01 (the same defect as Bot thread 4270918132, rated P2 by the Bot's single review, prescribed by item 1 as the input's continuation and fixed by the owner task's first row, the local review's P1 rating is input to the audit); evidence=grep -n 'Owned by dotfiles-T128-chain-review-scripts-followup-a01' .orchestration/acceptance/dotfiles-T128-chain-review-scripts-a01.md
46: local-finding: b6ce4ff:2 not-applicable:advisory P2 owned by dotfiles-T128-chain-review-scripts-followup-a01 (the same defect as Bot thread 4270918140, the reuse keyed by the sha7 prefix without comparing the recorded head, the owner task's second row); evidence=grep -n 'Owned by dotfiles-T128-chain-review-scripts-followup-a01' .orchestration/acceptance/dotfiles-T128-chain-review-scripts-a01.md
47: 
48: ## Owned by dotfiles-T128-chain-review-scripts-followup-a01 (advisory findings of the final head; plan 020 step 1.2; rows id<TAB>class)
49: 
50: 4270918132	stale-review-file-on-error
51: 4270918140	reuse-keyed-by-sha7
52: - 12:49:22Z the Codex half, round 1 on the owner task: `revise` (P2 the review-worktree row's control text was reworded, not verbatim). Applied 12:50Z (control verbatim, the disposition names the cover); round 2 to both halves on 0b10249e.
53: - 12:51:15Z the Codex half, round 2: `confirm` on 0b10249e; 12:51:36Z the seat, round 2: `confirm` on the same hash. **The owner task `dotfiles-T128-chain-review-scripts-followup-a01` is pair-confirmed on `0b10249e58b59d53c26da4468a264970cce7c41934c59bd9727899157147a3a7`** (two rounds); ACCEPTANCE accepted to the seat 12:52Z; it dispatches after PR #357 merges and the boundary lands this record's owner section and the task file.
54: - 13:07:31Z RESULT (bus 1181): `status=done`, PR #357 head `04a7d02ad856eadab87ff54b383e65e806b0a5f3` on base 5ec86052 (branch `regime/chain-review-scripts`; 1f307a6e the code, 0da6be3e the task copy and evidence and the Bot's head, 04a7d02a the evidence update); files the three scripts and the test module; the Bot's one review 5518077170 of 0da6be3e at 12:45:21Z, no badge in its body, no review or comment on 04a7d02a; threads 4270918132 and 4270918140 both `not-applicable:advisory P2 owned by dotfiles-T128-chain-review-scripts-followup-a01` (the stale review file on a non-zero exit, the input's continuation; the reuse keyed by sha7 without comparing the full head, the input's file name), no P0/P1, no fix round, no thread resolved by the worker; tests `test_local_review_runs_the_review_binary_read_only_at_the_head_and_writes_one_file`, `test_local_advisory_records_p2_rows_and_stops_on_p0_p1`, `test_sandbox_scan_prints_the_unsandboxed_mutation_calls` (3 OK; the four orchestrator modules 53 OK; 57 of 57 mutants caught); caps 148 of 200 changed lines outside tests and .orchestration (3 files), 230 of 1000 added under tests, 4 files outside .orchestration; CI 13 of 13 on 04a7d02a and on 0da6be3e; `task_copy` db9ff03a equals amendment 1; evidence on the branch under `.orchestration/dotfiles-T128-chain-review-scripts-a01/`; amendment=1, questions=1; fourteen cases beyond item 4 in the report; disclosures: the whole unit suite fails in the sandbox (no sandbox baseline; CI runs it green), one `gh` read denied at the permission gate and not retried, the sandbox record's row 11 names fewer `gh` reads than ran (left unfixed to keep the head). ACCEPTANCE `pending-integration head=04a7d02a` 13:08Z; the chain (`BOT_WAIT_MAX=0 integrate-pr.sh … 357 dotfiles-T128-chain-review-scripts-followup-a01`, `357-extra.tsv` with both threads' advisory dispositions) starts 13:08Z: update-branch onto ec94dc56, CI, local review, sweep, receipt, record block, audit.
55: local:b6ce4ff:1	stale-review-file-on-error
56: local:b6ce4ff:2	reuse-keyed-by-sha7
57: 
58: ## Dispatch (bus lines)
59: 
60: - AGMSG-TASK v1 task_id=dotfiles-T128-chain-review-scripts-a01 round=1 repo=~/Workspace/dotfiles/.claude/worktrees/worker-f task_file=.orchestration/tasks/dotfiles-T128-chain-review-scripts-a01.md task_sha256=af6556ba591a742f155fea5a649be9c579b95210dee56104babf4256018fcdd7 deadline=none note=plan-021-step-6.3,the-review-side-chain-scripts(local-review.sh,local-advisory.sh,sandbox-scan.sh)with-tests;attached-inputs-under-.orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/;text-pair-confirmed-on-af6556ba;fresh-branch-from-origin/main(after-5ec86052;your-playbook-branch-is-merged,leave-it);one-PR;the-Bot-reviews-once-at-PR-open;P0/P1-one-fix-round-before-the-RESULT;P2-advisory;the-sibling-task-runs-on-worker-c-concurrently-on-disjoint-files;RESULT-with-head,base,branch,files,threads,tests,caps,task_copy read_at=read
61: - AGMSG-TASK v1 task_id=dotfiles-T128-chain-review-scripts-a01 round=1 amendment=1 repo=~/Workspace/dotfiles/.claude/worktrees/worker-f task_file=.orchestration/tasks/dotfiles-T128-chain-review-scripts-a01.md task_sha256=db9ff03a5eb720a4778fc357fb351926e7ecbb1d5af7a5f6cf11266232ba060b previous_task_sha256=af6556ba591a742f155fea5a649be9c579b95210dee56104babf4256018fcdd7 deadline=none note=amendment-1-pair-confirmed(seat+Codex):row-11-lists-the-tools-each-input-runs;item-1-refuses-a-review-worktree-path-without-its-own-.git-entry(exit-2,before-the-dirty-check);the-first-test-gains-that-case(a-plain-directory-inside-the-main-working-tree:exit-2,stub-not-run,main-HEAD-unmoved);row-5-names-both-refusals;item-1-names-the-mktemp-template-you-declared;your-two-questions-of-09:02Z-answered-by-this-line;refresh-the-task-copy-to-this-hash;then-open-the-PR-and-RESULT read_at=read

 succeeded in 252ms:
INPUT local-advisory.sh 2e44dabc23ea03975ec568e0034e7f36956e5cd33e2bb2c74636902aa48fb03c
--- input/local-advisory.sh
+++ head/local-advisory.sh
@@ -1,23 +1,49 @@
 #!/usr/bin/env bash
-# local-advisory.sh <task> <head40> <owner-task-id>: plan 020 step 1.2 for the local review. Reads .orchestration/validation/<task>-local-review-<head7>.md; for each finding: a P0/P1 prints STOP (the PR's one round is over: the plan's step 4.2), a P2/P3 appends a row `local:<head7>:<n>\tadvisory-p2` under the heading `## Owned by <owner>` of the acceptance record (created when missing) and a `local-finding: <head7>:<n> not-applicable:advisory P2 owned by <owner>; evidence=…` line. Exit 3 on a P0/P1, 0 otherwise.
+# @file local-advisory.sh
+# @brief Record a local review's P2/P3 findings as advisory rows of the acceptance record; stop on a P0/P1.
+# @description
+#   Plan 020 step 1.2 for the local review. Reads `.orchestration/validation/<task>-local-review-<sha7>.md`. Each
+#   unique finding, numbered from 1: a P0/P1 prints STOP (the PR's one round is over: the plan's step 4.2); any
+#   other appends the row `local:<sha7>:<n><TAB>advisory-p2` under the heading `## Owned by <owner>` of
+#   `.orchestration/acceptance/<task>.md` (created when missing) and a `local-finding: <sha7>:<n>
+#   not-applicable:advisory P2 owned by <owner> (…); evidence=…` line, each only when the record lacks it.
+# @arg $1 string Task id.
+# @arg $2 string The reviewed head, 40 hex characters.
+# @arg $3 string The task id that owns the advisory findings.
+# @exitcode 0 No P0/P1 finding.
+# @exitcode 2 No local review file.
+# @exitcode 3 A P0/P1 finding.
+# @example
+#   scripts/orchestrator/local-advisory.sh dotfiles-T128-x-a01 "$head" dotfiles-T128-x-followup-a01
 set -euo pipefail
-task=$1; head=$2; owner=$3
+task=$1 head=$2 owner=$3
 cd "$(git rev-parse --show-toplevel)"
 h7=${head:0:7}
 LR=".orchestration/validation/$task-local-review-$h7.md"
 A=".orchestration/acceptance/$task.md"
-[ -s "$LR" ] || { echo "no local review file $LR"; exit 2; }
+[ -s "$LR" ] || {
+    echo "no local review file $LR"
+    exit 2
+}
 n=$(sed -n 's/^findings: //p' "$LR" | head -1)
-[ "${n:-0}" != "0" ] || { echo "local review of $h7: no findings"; exit 0; }
+[ "${n:-0}" != "0" ] || {
+    echo "local review of $h7: no findings"
+    exit 0
+}
 /usr/bin/grep -q "^## Owned by $owner" "$A" || printf '\n## Owned by %s (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)\n\n' "$owner" >> "$A"
-i=0; stop=0
+i=0 stop=0
 while IFS= read -r line; do
-  i=$((i+1))
-  case "$line" in
-    *"[P0]"*|*"[P1]"*) echo "STOP: local finding $i of $h7 is P0/P1: $line"; stop=1;;
-    *) /usr/bin/grep -q "^local:$h7:$i	" "$A" || printf 'local:%s:%s\tadvisory-p2\n' "$h7" "$i" >> "$A"
-       /usr/bin/grep -q "^local-finding: $h7:$i " "$A" || printf 'local-finding: %s:%s not-applicable:advisory P2 owned by %s (%s); evidence=git show origin/main:.orchestration/tasks/%s.md | grep -n '"'"'item 1'"'"'\n' "$h7" "$i" "$owner" "$(printf '%s' "$line" | cut -c1-120 | tr -d '`')" "$owner" >> "$A";;
-  esac
+    i=$((i + 1))
+    case "$line" in
+    *"[P0]"* | *"[P1]"*)
+        echo "STOP: local finding $i of $h7 is P0/P1: $line"
+        stop=1
+        ;;
+    *)
+        /usr/bin/grep -q "^local:$h7:$i	" "$A" || printf 'local:%s:%s\tadvisory-p2\n' "$h7" "$i" >> "$A"
+        /usr/bin/grep -q "^local-finding: $h7:$i " "$A" || printf 'local-finding: %s:%s not-applicable:advisory P2 owned by %s (%s); evidence=git show origin/main:.orchestration/tasks/%s.md | grep -n '"'"'item 1'"'"'\n' "$h7" "$i" "$owner" "$(printf '%s' "$line" | cut -c1-120 | tr -d '`')" "$owner" >> "$A"
+        ;;
+    esac
 done < <(/usr/bin/grep -E '^- \[P[0-3]\]' "$LR" | sort -u)
 echo "local review of $h7: $i finding(s) recorded as advisory under 'Owned by $owner' in $A"
 [ "$stop" = 0 ] || exit 3

INPUT local-review.sh 2258e370b9ff2575f9e55f72bc2071b86b6721c64ab57674f34b2be3de8ac501
--- input/local-review.sh
+++ head/local-review.sh
@@ -1,12 +1,29 @@
 #!/usr/bin/env bash
-# local-review.sh <task> <head> <pr>: C-32. Review a PR head's diff against main with the Bot's engine, locally, before the audit.
-# Run OUTSIDE the Bash sandbox (inside it codex exits 1: "failed to initialize in-process app-server client: Operation not permitted").
-# Writes .orchestration/validation/<task>-local-review-<sha7>.md (findings, then the transcript's final message with the worktree prefix stripped),
-# prints one line per unique finding and "local-review: <n> findings" last; exit 0 when n=0, 3 when n>0, 2 on a precondition.
+# @file local-review.sh
+# @brief Review a PR head's diff against main locally with the Bot's engine, once per head, before the audit (C-32).
+# @description
+#   Run outside the Bash sandbox: inside it codex exits 1 ("failed to initialize in-process app-server client:
+#   Operation not permitted"). An existing `.orchestration/validation/<task>-local-review-<sha7>.md` is reused and
+#   re-reported. Otherwise the clean review worktree (`$ORCH_REVIEW_WORKTREE`, else
+#   `.claude/worktrees/orchestrator-review`), a path with its own `.git` entry, is checked out detached at the head
+#   and left there, and the review binary (`$CODEX_BIN`, else codex) runs in it as `--profile review -s read-only
+#   review --base main`. The file gets the front matter, the unique `- [P0-3]` findings of the transcript's final
+#   message, and that message with the worktree prefix stripped; the findings are printed, then `local-review: <n>
+#   findings (<file>)`.
+# @arg $1 string Task id.
+# @arg $2 string The PR head commit, a local one.
+# @arg $3 int PR number.
+# @exitcode 0 No finding.
+# @exitcode 2 A precondition failed: the head is not a local commit, the review worktree is not a worktree root or not
+#   clean, or there is no review binary.
+# @exitcode 3 One or more findings.
+# @example
+#   scripts/orchestrator/local-review.sh dotfiles-T128-x-a01 "$(git rev-parse FETCH_HEAD)" 356
 set -euo pipefail
 task=$1 head=$2 pr=$3
 R="$(git rev-parse --show-toplevel)"
-W=$R/.claude/worktrees/orchestrator-review
+cd -- "$R"
+W=${ORCH_REVIEW_WORKTREE:-$R/.claude/worktrees/orchestrator-review}
 out=$R/.orchestration/validation/$task-local-review-${head:0:7}.md
 if [ -s "$out" ]; then
     # one sample per head (C-32): a review of this head exists; reuse it instead of sampling again
@@ -17,20 +34,40 @@
     [ "${n:-0}" = 0 ] || exit 3
     exit 0
 fi
-git -C "$R" cat-file -e "$head^{commit}" 2>/dev/null || { echo "local-review: $head is not a local commit (fetch pull/$pr/head first)"; exit 2; }
-[ -z "$(git -C "$W" status --porcelain)" ] || { echo "local-review: $W is not clean"; exit 2; }
+git -C "$R" cat-file -e "$head^{commit}" 2> /dev/null || {
+    echo "local-review: $head is not a local commit (fetch pull/$pr/head first)"
+    exit 2
+}
+# Without its own .git entry, git -C would act on an enclosing checkout and move that one to the head.
+[ -e "$W/.git" ] || {
+    echo "local-review: $W is not a worktree root"
+    exit 2
+}
+[ -z "$(git -C "$W" status --porcelain)" ] || {
+    echo "local-review: $W is not clean"
+    exit 2
+}
+# Resolved in the root before the checkout and run by its absolute path, so no relative PATH entry (./bin) picks a
+# binary from the PR head.
+codex=$(command -v "${CODEX_BIN:-codex}") || {
+    echo "local-review: no review binary ${CODEX_BIN:-codex}"
+    exit 2
+}
+[[ $codex == /* ]] || codex=$R/$codex
 git -C "$W" checkout -q --detach "$head"
 base=$(git -C "$W" merge-base main HEAD)
 t0=$(date -u +%FT%TZ)
-tmp=$(mktemp)
-(cd "$W" && codex --profile review -s read-only review --base main < /dev/null > "$tmp" 2>&1) || echo "local-review: codex exited $? (see $out)"
+tmp=$(mktemp "${TMPDIR:-/tmp}/local-review.XXXXXX")
+(cd "$W" && "$codex" --profile review -s read-only review --base main < /dev/null > "$tmp" 2>&1) || echo "local-review: codex exited $? (see $out)"
 final=$(awk '/^codex$/{f=1; buf=""; next} f{buf=buf $0 "\n"} END{printf "%s", buf}' "$tmp" | sed "s#$W/##g")
 findings=$(printf '%s\n' "$final" | /usr/bin/grep -E '^- \[P[0-3]\]' | sort -u || true)
 n=$(printf '%s' "$findings" | /usr/bin/grep -c . || true)
 {
     printf -- '---\ntask: %s\nhead: %s\npr: %s\nbase: %s\nstarted: %s\nfinished: %s\nfindings: %s\nengine: codex review --base main (profile review, read-only)\n---\n\n' "$task" "$head" "$pr" "$base" "$t0" "$(date -u +%FT%TZ)" "$n"
     printf '%s\n\n' "$findings"
-    echo '```text'; printf '%s\n' "$final" | cut -c1-2000; echo '```'
+    echo '```text'
+    printf '%s\n' "$final" | cut -c1-2000
+    echo '```'
 } > "$out"
 rm -f "$tmp"
 printf '%s\n' "$findings"

INPUT sandbox-scan.sh 099f6c7534223cb40623cc9be6ec063382476afaf2ca5d4405ad625f6480baec
--- input/sandbox-scan.sh
+++ head/sandbox-scan.sh
@@ -1,9 +1,24 @@
 #!/usr/bin/env bash
-# sandbox-scan.sh <task>: C-29 interim, extracted from the scratchpad integrate-prep.sh (lines 34 to 38). Prints the unsandboxed mutation calls found in the worker sandbox record .orchestration/sandboxes/<task>.md, or one line saying none; a hit is judged before the audit.
+# @file sandbox-scan.sh
+# @brief Print the unsandboxed mutation calls of a worker's sandbox record, so a hit is judged before the audit (C-29).
+# @description
+#   Reads `.orchestration/sandboxes/<task>.md`, a trailing `-fixtures` of the task id stripped. A line that names
+#   `dangerouslyDisableSandbox`, `outside the sandbox` or `unsandboxed` and a mutation (`git commit`, `git switch -c`,
+#   `git checkout`, `git add`, `git mv`, `git rm`, `cp `, `mv `, `> `, `tee `) but none of `counts`, `reads`, `lists`,
+#   matched case-insensitively, is printed with its line number, then the judge line; with no such line, one line says
+#   none. A missing record prints nothing.
+# @arg $1 string Task id.
+# @exitcode 0 Always.
+# @example
+#   scripts/orchestrator/sandbox-scan.sh dotfiles-T128-x-a01
 set -euo pipefail
 task=$1
 cd "$(git rev-parse --show-toplevel)"
 sb=".orchestration/sandboxes/${task%-fixtures}.md"
 if [ -f "$sb" ]; then
-  if /usr/bin/grep -n -i -E 'dangerouslyDisableSandbox|outside the sandbox|unsandboxed' "$sb" | /usr/bin/grep -i -E 'git (commit|switch -c|checkout|add|mv|rm)|cp |mv |> |tee ' | /usr/bin/grep -v -i 'counts\|reads\|lists'; then echo "sandbox scan: unsandboxed mutation calls above (C-29); judge before the audit"; else echo "sandbox scan: no unsandboxed mutation call in $sb"; fi
+    if /usr/bin/grep -n -i -E 'dangerouslyDisableSandbox|outside the sandbox|unsandboxed' "$sb" | /usr/bin/grep -i -E 'git (commit|switch -c|checkout|add|mv|rm)|cp |mv |> |tee ' | /usr/bin/grep -v -i 'counts\|reads\|lists'; then
+        echo "sandbox scan: unsandboxed mutation calls above (C-29); judge before the audit"
+    else
+        echo "sandbox scan: no unsandboxed mutation call in $sb"
+    fi
 fi

Task copy equal True sha256 db9ff03a5eb720a4778fc357fb351926e7ecbb1d5af7a5f6cf11266232ba060b

 succeeded in 627ms:
graph True revision 940a3a2b07adfd14140a0acff96784ef53a0a509
relevant nodes [('home/dot_config/claude/rules/model-selection.md', 'Global Claude rule establishing model_profiles in agent-config.yaml as the single source of model IDs and efforts, the orchestrator/worker/auditor role constellation, and profile choice for exploration, reviews and security audits.'), ('home/dot_agents/skills/agmsg-orchestration/SKILL.md', 'Agent skill defining the agmsg orchestration protocol between a Claude orchestrator and Codex workers: architecture, regime activation, parallel workers, identity/delivery, Message Contract v1, .orchestration layout, orchestrator/worker playbooks, worklogs and pitfalls.')]
changes from graph .claude/contextdb/contextdb/cli.py
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
.github/workflows/agent-assets.yml
.github/workflows/docs.yml
.github/workflows/macos.yaml
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
.orchestration/acceptance/dotfiles-T124-wav

**Checking token limits and design**
mcp: codex_apps/github.fetch_commit_workflow_runs started
mcp: codex_apps/github.list_pull_request_reviews started
mcp: codex_apps/github.list_pull_request_review_threads started
exec
/bin/zsh -lc "wc -l .orchestration/tasks/dotfiles-T128-regime-v3-a01.md .orchestration/validation/dotfiles-T128-chain-review-scripts-a01.md && rg -n 'INV-[0-9]|invariants:|chain-review-scripts|trust|S21|021|7\\.2' .orchestration/tasks/dotfiles-T128-regime-v3-a01.md && cat .orchestration/sandboxes/dotfiles-T128-chain-review-scripts-a01.md && cat .orchestration/validation/dotfiles-T128-chain-review-scripts-a01-pr-feedback.json" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 82ms:
     241 .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
     375 .orchestration/validation/dotfiles-T128-chain-review-scripts-a01.md
     616 total
10:  dotfiles-T128-v0-main-tests-a01: [INV-12]
11:  dotfiles-T128-v1-task-schema-a01: [INV-1]
12:  dotfiles-T128-v1c-regime-ci-check-a01: [INV-1]
13:  dotfiles-T128-v1b-pr-caps-a01: [INV-2]
14:  dotfiles-T128-ci-skip-orchestration-a01: [INV-2]
15:  dotfiles-T128-ci-skip-orchestration-a02: [INV-2]
16:  dotfiles-T128-v2-audit-schema-and-runner-a01: [INV-5]
17:  dotfiles-T128-v2b-audit-gate-a01: [INV-5]
18:  dotfiles-T128-regime-counters-a01: [INV-6]
19:  dotfiles-T128-regime-counters-a02: [INV-6]
20:  dotfiles-T128-v3a-reset-counters-a01: [INV-6, INV-1]
21:  dotfiles-T128-v3b-premises-and-amendments-a01: [INV-4]
22:  dotfiles-T128-v3c-one-fact-per-round-a01: [INV-3]
23:  dotfiles-T128-v3d-idle-and-first-push-a01: [INV-10]
24:  dotfiles-T128-v4-design-review-runner-a01: [INV-7]
25:  dotfiles-T128-v5a-evidence-on-branch-a01: [INV-8]
26:  dotfiles-T128-v5b-cost-fields-a01: [INV-9]
27:  dotfiles-T128-v6-permgate-session-a01: [INV-11]
28:  dotfiles-T128-v0-main-tests-a02: [INV-12]
29:  dotfiles-T128-gate-evidence-a01: [INV-6]
30:  dotfiles-T128-gate-evidence-a02: [INV-6]
31:  dotfiles-T128-gate-evidence-a03: [INV-6]
32:  dotfiles-T128-gate-evidence-a04: [INV-6]
41:  R2: "hand-written parsers at a trust boundary have an unbounded bypass surface (PR 313: 33 of 52 Bot threads on a 503-line validator with its own YAML parser, written on the false premise that PyYAML is unavailable)"
48:trust_anchors:
54:invariants:
55:  INV-1: "every task is a format-2 file whose front matter validates against schemas/task.json (jsonschema + PyYAML, no hand-written parser; every allowed_files entry starts with a literal path segment and a wildcard entry derives the tier of every design-tier path its literal prefix can cover); legacy task ids are grandfathered only for files under .orchestration/tasks/ on main, never for a branch copy; the tier (docs, review, design) is derived from allowed_files by the shared high-risk module, with the regime's own rule prose (home/dot_config/claude/rules/**, the agmsg-orchestration SKILL, AGENTS.md, README) listed in the review tier, and selects the pipeline from process_tiers in agent-config.yaml; every AGMSG-TASK for the task, the first and each amendment, carries task_sha256= of the task file as sent, the worker commits the file byte-identical to .orchestration/<task id>/task.md (first commit, recommitted after each amendment), the CI regime job validates that copy with main's schema and refuses a PR that changes .github/workflows/** unless its task.md is design tier and lists the file, the host gate compares the copy's sha256 with the latest AGMSG-TASK's token in history, and the regime check binds only once the ruleset lists it as required (an operator action named in V1's acceptance record); the orchestrator can add or skip a stage only with an operator waiver written by scripts/regime-waive.sh, a command under a permissions.ask rule in the managed settings with no permgate policy entry, so that only the human's answer to the native prompt runs it (an ask rule prompts even in auto mode; agent-to-agent approval is forbidden); the waiver names the task, the stage and a reason and is written under $XDG_STATE_HOME/regime/waivers/, a directory outside every seat's sandbox write roots, so no sandboxed seat can write it and only a command run outside the sandbox on the human's answer to the native prompt can (the directory is the guard; the ask rule on the named command is the second layer, since a reworded command would still meet the prompt at the sandbox boundary); it is listed by check-regime-boundary.sh and the boundary PR body (V3a owns the script and its ask rule), and is the strongest friction available on a machine where every seat and GitHub action is the operator's own account (operator authentication is a stated residual, not a claim)"
56:  INV-2: "a PR is mergeable only within the caps the CI regime job enforces from main's workflow (at most 15 changed files outside .orchestration/, 500 added lines outside tests/, .orchestration/ and the data list scripts/legacy-task-ids.txt, and 1000 added lines under tests/), and its task.md invariants equal the design's as a set of ids and byte-for-byte as sentences (the design read from main, never from the PR); the design file must be on main (through a boundary PR) before the implementing TASK is dispatched and the regime job fails closed when the design named by task.md is absent from main; an .orchestration-only PR runs no bootstrap or test matrix and every required check context still reports success (each required workflow decides inside each of its jobs, as test.yaml and remote.yaml do since A5: no job-level if and no needs, because a skipped required job reports success), so a boundary PR merges in minutes; exceeding a cap is a split, never a finding to disposition (the cap changes the unit of work: T116 +529 and T118 +881 would have been split)"
57:  INV-3: "a revise round is admissible only when it adds a new deterministic check: the AGMSG-ACCEPTANCE status=revise carries check=tests/<file>::<name> and previous_head=<the RESULT head being revised>, the worker records both in .orchestration/<task id>/revise.yaml (a sibling file; task.md stays byte-identical to the dispatched file), the main-pinned regime job verifies that the named test file exists on the head and differs between previous_head and the head, the PR's own unit-test workflow (a required check, run in the PR's context) collects and runs exactly that selector on the head (it must pass) and on previous_head (it must fail or be absent), and the host gate, which reads history, verifies that previous_head equals the head of the previous AGMSG-RESULT for the task and requires the same selector in the validation file; a finding that cannot become a test is dispositioned, never iterated"
58:  INV-4: "a task file carries premises, each with the command and pasted output that verified it before dispatch; premises are evidence for the design reviewers and the auditor, each of whom dispositions every premise in the receipt or audit JSON as holds, fails or unverifiable (a local command re-run, an external claim re-fetched; a fails is a specification finding and a rejection), a complete disposition the schema requires rather than a sample, and the mechanical part of this invariant is the counting: a worker question (AGMSG-PONG status=question) is a specification defect answered by at most one further AGMSG-TASK, amendments are every AGMSG-TASK for the task_id after the first, whatever its wording, and the second amendment or the second question is INV-6's count, which withdraws the task to design through INV-6's merge backstop and Stop signal"
59:  INV-5: "the task-level audit is a headless read-only run whose instruction root is the trusted main checkout and whose schema is main's schemas/audit.json: codex exec --output-schema <main>/schemas/audit.json -C <main> with the detached worktree at the head added as a read-only data directory (--add-dir), so the audited PR controls neither the schema nor the AGENTS.md the auditor reads; the fallback claude -p --json-schema from the same root with --add-dir <worktree>, --bare when an API key is set and otherwise with project and user hooks disabled, and refused with exit 2 blocked when the head changes any file under .claude/ (bare mode loads skills from an --add-dir directory's .claude/skills/), leaving such a head to the codex path), with at most one valid audit per head (a stale input manifest invalidates an audit and a new audit of the same head replaces it), pooled two at a time; the gate accepts an audit of an earlier head only when git diff --quiet <audited head> <HEAD> -- . ':!.orchestration' holds (an evidence-only revision), otherwise a new audit is required; its input includes the task's invariants and premises, the worker's evidence, the orchestrator's task file and amendments, the acceptance record as it stands when present (its text above the line <!-- audit-input-boundary --> is the pre-audit part; dispositions of this audit's findings are appended below it), the head's pr-feedback JSON and the previous round's audit JSON; the audit JSON carries an input manifest (path to sha256 of every input as read, computed by the runner, which overwrites any model-supplied value) and the gate recomputes the manifest at gate time, so a pre-audit input edited after the audit makes the audit stale and a new audit is required; the schema lists findings {priority, confidence, category in {specification, implementation, evidence, orchestration, conformance}, path, line, rationale} and the per-invariant map before the verdict, and the prompt asks for the rationale before each verdict; the runner, under the identity claude-audit-dot-h001 or codex-audit-dot-h001 on the orchestrator's host, records the JSON's sha256 in agmsg history (AGMSG-AUDIT v1 task_id= head= sha256= auditor=) before the gate reads it, an anchor that prevents edits after the record and not fabrication before it; the gate reads the verdict and categories from the JSON, and orchestration and conformance findings at P0-P2 accept only an operator waiver or a design reset, never not-applicable"
60:  INV-6: "the reset rule's mandatory point is the merge backstop in scripts/require-crit-review.py, with the orchestrator's Stop hook (Claude Stop hook, Codex [hooks].Stop) as the early signal, soft on both runtimes by their documented caps; counts come from history for the hook and the gate (revises = RESULTs for the task_id minus one, threshold 2; amendments = AGMSG-TASKs after the first, threshold 2; AGMSG-PONG status=question, threshold 2) and from GitHub and main-checkout files for the gate and the boundary check only (Codex Bot P0 or P1 on two heads after the first RESULT, from original_commit_id on review_comment items recorded by pr-feedback.py; an audit implementation or specification finding at P0-P1 on two heads, from .orchestration/validation/<task>-audit-<sha7>.json in the main checkout, each counted only when its sha256 matches its AGMSG-AUDIT record); when a count is reached the gate refuses the merge until a reset record names a redesign task whose design RESULT comes from an identity other than the task's author, or a waiver written by scripts/regime-waive.sh under the INV-1 ask-rule discipline into the state directory outside the sandbox write roots (the only release path besides a redesign; the one-account residual of INV-1 applies); check-regime-boundary.sh reports a closed-unmerged PR whose task has no reset record and a task over any count with neither an accepted acceptance record nor a reset record; the same gate refuses a merge whose acceptance record carries a not-applicable disposition without an evidence= clause, or a finding-class table with three rows of one class and no pasted search of the correction records (plan 007 S6)"
61:  INV-7: "the design tier adds, before any code is dispatched, two design reviews of the same design hash: a fresh Claude context on the review profile (a headless run or a seated -review- identity; the review profile is the same model and effort as deep, so the lever is the separate context) and a Codex read-only review (codex exec --sandbox read-only on the review profile under a codex-review identity: headless through V4's runner, or seated until V4); each receipt is a schema document naming the design file's canonical hash over invariants, threat_model, trust_anchors, implementing_tasks and premises, each is announced by an AGMSG-RESULT from its reviewing identity, and both RESULTs precede the implementing AGMSG-TASK in history; the Codex Bot's review of a boundary PR is swept feedback, never a design receipt; a change to the hashed keys needs new reviews; the gate accepts the whole-file sha256 form for receipts written before V4 lands"
62:  INV-8: "worker evidence (the task.md copy, revise.yaml, report, validation, sandbox, learning, autoskill, worker review JSON) is committed on the PR branch under .orchestration/<task id>/ before the final RESULT so the Bot, CI and the gate read the same files from the audited head; the orchestrator's records (audit JSON, acceptance, pr-feedback) stay under .orchestration/validation and .orchestration/acceptance in the boundary commit because the merge is --match-head-commit"
63:  INV-9: "every acceptance record carries measured cost (rounds, amendments, questions, wall time TASK to final RESULT from history timestamps, audit count, Bot threads, tokens: total_cost_usd from claude -p JSON, turn.completed.usage from codex exec --json, per-message usage from the seat's session transcript) written by accept-task.py, which also records the path and sha256 of every raw source it read (the headless runs' JSON, the transcript files at acceptance time) so a total can be recomputed; cost is a warning metric, never a gate: each tier has a budget, the acceptance record names the operator decision when it is exceeded, and check-regime-boundary.sh warns; headless runs carry --max-budget-usd"
64:  INV-10: "at most three concurrent workers with pairwise-disjoint allowed_files; the first push is the draft PR's server-side created_at (gh api pulls/<n>), which must fall within 30 minutes of the TASK's history timestamp, and a seated worker is not idle for 20 minutes while a dispatchable task exists, a dispatchable task being a format-2 file under .orchestration/tasks/ with no AGMSG-TASK for its id in history, no superseded_by or reset record, and every task id in its after list accepted (an acceptance record with Decision accepted in the main checkout); both computed in check-regime-boundary.sh and accept-task.py, never in the Stop hook; headless reviews and audits do not count as workers"
65:  INV-11: permgate records session_id and cwd per decision, and the gate compares a Claude worker's permission-gated Bash count in the task window with the sandbox record (an understated record is refused); Codex workers cannot escalate and are not covered
66:  INV-12: "every rule above is exercised by a unit test that fails when the rule is removed; the PR's own workflow runs the PR's tests, and a required check main-tests (wave V0, before every other wave) fetches main's tests/unit and runs, in the PR's context, main's test module of every script outside the task.md's allowed_files as it is, so an undeclared change to any script fails (the undeclared-change regression guard); a script inside allowed_files is judged by the PR's own tests, the orchestrator's diff review and the trusted-root audit (INV-5), which reads the test diff beside the code diff and reports a deleted or weakened fails-when-removed test as a conformance finding; main-tests decides inside its own job, as the A5 workflows do, with no changes job and no needs, so an .orchestration-only PR reports success from the job itself; main-tests is an in-process oracle: code that main's tests import from the PR runs inside the test process, so the harness authenticates that main's runner reached its end with a per-run nonce that only the runner sees (read from a pipe and closed before any test loads, written back with the counts), and the runner pins unittest's result and runner classes before importing any test; the nonce authenticates the writer, not the counts: adversarial PR code running in the same process can still patch result collection or read the nonce from a frame, so in-process forgery remains a stated residual that the trusted-root audit catches, named in every acceptance record of a design-tier PR; including one test per gaming path (a schema-valid task with a prose cap bypass, a revise without a named check, a revise list appended to the hashed task.md, an AGMSG-TASK without amendment= that still counts, an evidence-only relabel of a code change caught by the tree-equality check, a wave-table rewrite after review, an audit JSON edited after its history record, a receipt whose hash predates a key change, a reset record naming the author's own identity, a Bot-skipped head whose audit never starts, a single PR split only in the task file, a branch task.md claiming a legacy id, allowed_files of ['*'] or a wildcard first segment, an invariant sentence weakened under its id, a schema or AGENTS.md edited on the audited head, an undeclared script change that main-tests must fail); legacy task ids are grandfathered by the checked-in list scripts/legacy-task-ids.txt, which only shrinks and is excluded from the line cap as data"
116:By T126 INV-6 as written: wave 1 (PR #313) 8 amendments (limit 4) and 2 revises (limit 2); wave 3b (PR #314) Bot P1 on two post-RESULT heads. The orchestrator was drafting a waiver for #313. T120 was reset only on the operator's question. The regime is therefore reset here by its own rule; this document is the redesign, and T126 and T124 are superseded (their accepted ideas are kept where named).
133:R1 to R8 in the front matter. The literature behind R1: intrinsic self-correction without an external signal degrades after the first round (Huang et al. 2023); a second review round on the same artifact raised recall slightly and false positives by 62% (arXiv 2603.16244); multi-round review degrades with rounds (MCR-Bench); revising an already-correct state loses correct work unless verifier evidence is bound to the exact code state (arXiv 2607.24604). Behind R3: Google's review study (median change 24 lines, ~90% under 10 files) and its CL-size guidance. Behind R5 and R6: a judge without a reference is lenient and a reference flips 9-85% of verdicts toward correct (2607.12885); format-restricted generation degrades reasoning, so verdicts reason first and then fill the schema (2408.02442); Anthropic's harness-design post: a standalone skeptical evaluator is tractable where a self-critical generator is not, and the evaluator is worth its cost only where the task exceeds the model's reliable solo capability, which is what the tier table encodes.
137:- **P1 One deterministic fact per round (INV-3).** Reuses tests/unit, CI, `pr-feedback.py`. Deletes free-form revise rounds and the audit-per-round habit.
138:- **P2 Declarative over imperative at trust boundaries (INV-1, INV-5, INV-7).** Reuses `jsonschema`, PyYAML, `codex exec --output-schema`, `claude -p --json-schema`. Deletes the bespoke YAML parser, the glob NFA, the prose verdict grammar, regex parsing of `.last.md`, and the T126 "process_tiers.json next to the module" indirection (the validator reads the manifest with PyYAML).
139:- **P3 Small one-invariant PRs enforced in CI (INV-2).** Reuses GitHub required checks and the strict up-to-date ruleset already in force. Deletes waves declared inside a task file.
140:- **P4 Main-pinned mechanical checks in CI; host gate only for history-anchored rules (INV-1, INV-2, INV-8 in CI; INV-3, INV-5 record, INV-6, INV-7 anchor, INV-11 on the host).** Reuses `pull_request_target`, the `changes` job pattern that reports success for an `.orchestration`-only diff. Deletes PR #313's `REVIEW_TREE` idea (never on `main`) and the copy step of untracked evidence into the gate's cwd. The host gate `make require-crit-review` keeps its evidence rules and changes three of them in named waves: the audit verdict and categories come from the schema JSON with the `AGMSG-AUDIT` record and the category lock (V2b), the reset backstop and the Bot-head count (V3a), the history-anchored design review (V4); it continues to run from the orchestrator's main checkout.
141:- **P5 Research before dispatch; a question ends the task, not amends it (INV-4).** Reuses history (`amendment=`, `status=question`). Deletes the amendment-per-question practice. The task file's `premises` block is the mechanical residue of "verify every CLI constraint by running the real command".
142:- **P6 Reset is mechanical, loop-time, and released only by another context or the operator (INV-6).** Reuses `scripts/require-crit-review.py` as the mandatory point, `agent-stop-gate.sh` and the Codex `[hooks].Stop` as the early signal (both soft by their documented caps: Claude's 8-continuation cap, Codex's continuation prompt), `check-regime-boundary.sh` for the re-dispatch detector. Deletes the orchestrator-written redesign (the redesign author is a `review`-profile seat or a fresh headless context; the `redesign` profile of T124 v4 is dropped: `review` is the same model and effort as `deep`, so independence of context is the whole lever, and T124 round 1 showed it works).
143:- **P7 Audit staging by tier; the auditor never serializes the pipeline (INV-5, process_tiers).** See section 4.
144:- **P8 Cost measured, budgets per tier (INV-9).** Reuses the JSON cost fields the runtimes already emit and the session transcripts. Deletes `cost: n/a`.
145:- **P9 Parallelism with disjoint files and early push (INV-10).** Reuses `herdr-agents --add-worker`, draft PRs.
152:| 0 design review | a fresh Claude context on the review profile and a Codex read-only review of the same hash, schema receipts (INV-7) | before any code | - | - | required | minutes |
155:| 3 schema audit | headless read-only `codex exec --output-schema`, pooled 2, started by `make audit-head` once CI is green and the Bot reviewed or 15 min passed, once per RESULT head, reused for an evidence-only head by tree equality (INV-5) | per RESULT head | - | required | required, with invariant map and permgate window | the scarce resource, now off the critical path |
158:Tier derivation: docs = prose-only `allowed_files` outside the regime's own rule prose (`home/dot_config/claude/rules/**`, the agmsg-orchestration SKILL, `AGENTS.md`, README), which is review tier by explicit list; review = the existing review-tier paths (scripts, hooks, tests, templates); design = the explicit design-tier list from T124 INV-2 v3 (install/**, setup.sh, the gate scripts, `executable_herdr-agents`, `executable_permgate`, Codex and Claude policy, sandbox and permission settings, credential helpers). Round limits: docs 1 revise; review and design 2 revises then reset. Profiles: worker `standard` (docs `express`), review `review`, audit `audit`.
166:| INV-1 | `.github/workflows/regime.yml` (`pull_request_target`, required check `regime`: validates `.orchestration/<task id>/task.md` from the PR head read as data, refuses workflow edits outside a design-tier task; an explicit Actions event policy allowing `pull_request_target` is set by the operator before 2026-11-02, named in V1c's acceptance record), `scripts/validate-task.py` (schema + PyYAML, about 80 lines), `schemas/task.json`, `scripts/lib/high_risk_paths.py` (new module: tier lists and `tier_of`), `scripts/legacy-task-ids.txt` (grandfather list), `process_tiers` in the manifest; host gate compares the copy's sha256 with `task_sha256=` in history (V3a); stage waivers by `scripts/regime-waive.sh` under its `permissions.ask` rule, written outside the sandbox write roots (V3a) |
167:| INV-2 | `regime.yml` step with `scripts/pr-caps.sh` and the task.md invariant-id comparison against the design's `implementing_tasks` |
168:| INV-3 | `regime-check.sh` step: the test selector named in `.orchestration/<task id>/revise.yaml` (sibling of the byte-identical task.md) exists on the head and its file differs between `previous_head` and the head; a `revise-check` job in `test.yaml` (PR context, required) runs exactly that selector on both heads; the host gate's `previous_head` history check and validation-file line are V2b's |
169:| INV-4 | `scripts/validate-task.py` (premises required for code and design tasks); `agent-stop-gate.sh` early signal on the second AGMSG-TASK or second PONG question; the merge backstop is INV-6's |
170:| INV-5 | `schemas/audit.json` (findings and invariant map before verdict), `scripts/audit-head.sh` (about 100 lines: detached worktree, `codex exec`, fallback, sha256 to history under the audit identity, `.last.md` render; PR #314's hardening kept), `make audit-head` target around `gh pr checks --watch` and the SKILL's Bot list loop with its 15-minute `bot: none` rule (no daemon), `AGENTS.md` Audit section; gate: JSON verdict and categories, `AGMSG-AUDIT` lookup, category lock, tree-equality acceptance of an earlier head (V2b) |
171:| INV-6 | `scripts/require-crit-review.py` (mandatory: history counts, Bot heads from `original_commit_id` recorded by `scripts/pr-feedback.py`, audit heads from the main checkout's audit JSONs whose sha256 matches their `AGMSG-AUDIT` record, reset record or a `scripts/regime-waive.sh` waiver), `scripts/agent-stop-gate.sh` and the manifest's `codex.hooks` Stop entry (early signal, history counts only, within the 3 s history budget), `scripts/check-regime-boundary.sh` (closed-unmerged PR without a reset record; over-count task without an accepted or reset record; waiver listing) |
172:| INV-7 | `scripts/design-review.sh` + `schemas/design-review.json`: two headless runs per design hash, `claude -p` under `claude-review-dot-hNNN` and `codex exec --sandbox read-only` under `codex-review-dot-hNNN`, each joining for the run and sending its RESULT; gate: both RESULTs precede the implementing TASK, both hashes recomputed, whole-file form accepted for pre-V4 receipts |
173:| INV-8 | worker writes under `.orchestration/<task id>/` on the branch (task.md copy first); `regime.yml` validates the evidence JSON shapes; the gate's existing path rules keep the orchestrator's records under `validation/` and `acceptance/` |
174:| INV-9 | `scripts/accept-task.py` (sweep, dispositions scaffold, record rows, gate invocation, merge command, cost fields), budgets in `process_tiers`, `check-regime-boundary.sh` warning |
175:| INV-10 | `scripts/check-regime-boundary.sh` and `scripts/accept-task.py` from `history.sh` timestamps (storage facade or `--limit`, never the 20-row default), the draft PR's `created_at` from `gh api pulls/<n>`, and the task's `after` list against acceptance records |
176:| INV-11 | `executable_permgate` (operator-routed, Codex security review) + gate cross-check |
177:| INV-12 | one test module per script; `make unit-test` in CI; the `main-tests` required job (V0): main's test modules for every script outside the PR's `allowed_files`, deciding inside its own job; the trusted-root audit reads the test diff beside the code diff for scripts inside it; the auditor checks per PR that no new hand-written parser sits at a trust boundary (a `conformance` finding) |
180:## 6. Waves (one PR, one invariant, within INV-2's caps; each task file reviewed by a fresh context before dispatch)
182:- **V0** INV-12: the `main-tests` required job in `test.yaml` (main's `tests/unit` modules of every script outside the PR's `allowed_files`, run in the PR's context, deciding inside the job as the A5 workflows do) and the protocol in the Worker Playbook; lands before every other wave as `dotfiles-T128-v0-main-tests-a02` (A301; PR #317 and the audit of `adcf783b` are its input). Claude seat; design tier (workflow); the operator lists the check at its acceptance.
183:- **V1** INV-1, validation only (operator direction 2026-10-11, relayed through the review seat; also the cap: the undivided V1 sat at 500 added lines): `schemas/task.json`, `scripts/validate-task.py`, `scripts/lib/high_risk_paths.py`, `scripts/legacy-task-ids.txt` (from PR #313; data, excluded from the line cap), `tests/unit/test_validate_task.py`. Claude seat. Design tier: this review is its stage 0. Precondition: this design is on `main` through a boundary PR before V1's TASK is dispatched.
184:- **V1c** INV-1, the CI check (after V1): `scripts/regime-check.sh`, `.github/workflows/regime.yml` (task.md validation, workflow-edit refusal, `workflow_dispatch` dry run), `tests/unit/test_regime_check.py`, `process_tiers` in the manifest, SKILL step 3 paragraph, README sentence. Claude seat. Acceptance names the operator action that lists `regime` as a required check, after the dry run from `main` against a closed PR. Two tasks map to INV-1 as V2 and V2b map to INV-5.
185:- **V1b** INV-2 (after V1c): `scripts/pr-caps.sh`, the caps and invariant-id steps in `regime-check.sh`, tests, one SKILL sentence.
186:- **V2** INV-5 runner: `schemas/audit.json` (PR #314's, reordered), `scripts/audit-head.sh` with PR #314's hardening, `make audit-head`, `AGENTS.md` Audit section, tests, the SKILL's task-level audit bullet. Claude seat.
187:- **V2b** INV-5 gate: `scripts/require-crit-review.py` reads the JSON verdict and categories, requires the `AGMSG-AUDIT` record, locks orchestration and conformance at P0-P2 to waiver or reset, accepts an earlier audited head by tree equality, and requires the INV-3 `check=` line in the validation file; tests. Operator-routed gate source (delegable to a Claude seat with recorded opt-in).
188:- **A3** INV-6 (plan 006 Phase A, `dotfiles-T128-regime-counters-a01`): `scripts/regime-counters.sh` computes every INV-6 count from history and GitHub and prints the thresholds reached; `check-regime-boundary.sh` reports a reached threshold without a reset record or waiver; the orchestrator runs it before every acceptance action. V3a wires that script into the hook and the gate.
189:- **V3a** INV-6: `scripts/pr-feedback.py` (`original_commit_id` on review_comment items), `require-crit-review.py` reset backstop and `task_sha256` comparison, `agent-stop-gate.sh` history counts (revises, amendments, questions) as the early signal, the Codex Stop entry in the manifest and its rendered template, `scripts/regime-waive.sh` with its `permissions.ask` rule in the manifest's Claude permissions block (no permgate policy entry), `check-regime-boundary.sh` detector and waiver listing; tests. Four boundaries in one PR (gate source, Claude hook and permission source, Codex hook source): an operator PR by construction, reviewed by a Codex `security`-profile seat before acceptance.
190:- **V3b** INV-4: premises in the schema and validator, SKILL text (questions end the task; one answering TASK at most). Claude seat; no hook source (the counting is V3a's).
191:- **V3c** INV-3: `check=` and `previous_head=` in the ACCEPTANCE contract (SKILL), `revise.yaml` beside task.md in the Worker Playbook, the `regime-check.sh` step, the `revise-check` job in `test.yaml`; tests. Claude seat (no gate source: the history check and validation-file line are V2b's).
192:- **V3d** INV-10: idle and first-push computations in `check-regime-boundary.sh` and `accept-task.py` (the latter lands in V5b; V3d adds them to the boundary check only). Claude seat.
193:- **V4** INV-7: `scripts/design-review.sh` (Claude and Codex runs under their `-review-dot-hNNN` identities), `schemas/design-review.json`, the history anchor and hash check in the gate (two RESULTs, both forms), SKILL paragraph. Operator-routed for the gate part.
194:- **V5a** INV-8: `.orchestration/<task id>/` paths in the Worker Playbook, task.md copy as the first commit, evidence-shape validation in `regime.yml`, boundary commit reduced to orchestrator records. Claude seat.
195:- **V5b** INV-9: `scripts/accept-task.py`, cost fields with source digests, budgets in `process_tiers`, `check-regime-boundary.sh` budget warning. Claude seat. Size: the sweep, scaffold and gate invocation already exist as commands; the script sequences them, about 200 lines.
196:- **V6** INV-11: `executable_permgate` session_id and cwd; gate cross-check. Operator-routed, Codex `security` profile review.
211:- `pull_request_target` runs with the base repository's token on a public repository: the `regime` job reads PR files as data with `contents: read` only, checks out `main`'s scripts, and never executes anything from the PR; a change to `.github/workflows/regime.yml` itself is a design-tier change under INV-1.
218:- The seven existing required checks still run on `pull_request` from the PR's own workflow files; INV-1's workflow-edit refusal in the `regime` job is what closes R8 for them.
223:Round 1 (`.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review.md`, `claude-review-dot-a001`, 2026-10-10T21:15Z, verdict `revise`): INV-7, INV-8, INV-11, INV-12 accepted with notes; INV-1, 2, 3, 4, 5, 6, 9, 10 rejected with corrections; findings F1-F9. v2 adopts every item: the task.md copy and `task_sha256` anchor (F1), the per-task invariant-set rule and the workflow-edit refusal (F2), the gate changes assigned to V2b/V3a/V4 with the category lock, the Bot-wait timeout and the tree-equality rule (F3), the merge backstop as the mandatory point, `original_commit_id`, the audit-JSON source, the Stop-hook budget split and the boundary detector (F4), the single amendment count over every TASK (F5), INV-9/INV-10 moved out of the Stop hook (F6), the reset records corrected to `claude-review-dot-a001` with the waiver form and the thread ids (F7), rule prose in the review tier (F8), premise 1 restated and three premises added (F9); plus the Q5 salvage list, the `make audit-head` target in place of a daemon, the `regime.yml` discipline and the hash note.
225:Round 2 (`…-design-review-round2.md`, 21:29Z, verdict `revise`): every round-1 correction confirmed applied; INV-2, INV-3, INV-6 rejected for contradictions v2 introduced, plus routing, cap and premise notes. v3 adopts all of them: `implementing_tasks` is a map of task id to invariant ids inside the hashed keys and the design-on-main precondition is stated (INV-2); `revise.yaml` is a sibling of the byte-identical task.md (INV-3, INV-8, INV-12, V3c, V2b); the question threshold is 2 and audit JSONs count only when their sha256 matches their record (INV-6); V3a is an operator PR with all hook counting, V3b has no hook source, V3c no gate source; the legacy list is excluded from the line cap as data; the `workflow_dispatch` premise is added; the stage-3 sentence names the orchestrator's `make audit-head`; INV-1 names the latest TASK's token and the recommit after each amendment. Round 3 (`…-design-review-round3.md`, 21:33Z, verdict `accept`) confirmed the five edits; its two notes are carried in the acceptance record. v4 (operator direction 2026-10-11, relayed by the review seat's PONG at 22:01Z) splits V1 by responsibility into V1 (validation only) and V1c (the CI check), adds `dotfiles-T128-v1c-regime-ci-check-a01: [INV-1]` to `implementing_tasks` (a hashed key, hence this round), reorders the waves (V1, V1c, V1b, …) and aligns section 7's cap wording with INV-2. Round 4 (`…-design-review-round4.md`, 22:06Z, verdict `accept`) confirmed the split; its note (INV-1's ruleset action is V1c's acceptance record) is carried. v5 answers the Codex Bot's finding on boundary PR #316 (thread 4239305441): INV-3's `ci:<job>` form had no enforcement, so `check=` is now a test selector or a `repro:<id>` whose command and output live in revise.yaml, each with its own regime-job verification. Round 5 (`…-design-review-round5.md`, 22:12Z, verdict `accept`) confirmed it. The Codex Bot then reviewed the second boundary head (c1e2582b) and raised six P1 and four P2 findings that three same-vendor accepts had not: the auditor read the schema and AGENTS.md from the audited head (INV-5 now runs from main as the instruction root with the worktree as data), the CI job had no previous RESULT head (INV-3 now records previous_head in the ACCEPTANCE and revise.yaml, cross-checked by the host gate), ids were compared without sentences (INV-2), `allowed_files: ['*']` derived a cheap tier and a branch copy could claim a legacy id (INV-1, INV-12), and two task records pointed at an abandoned prerequisite. v6 adopts all ten and, because a cross-vendor reviewer found what a same-vendor fresh context did not, INV-7 now requires both a Claude and a Codex review of each design hash. Round 6 (`…-design-review-round6.md`, 22:28Z, verdict `revise`) accepted INV-1, 2, 3, 5, 12 and rejected INV-7: the Bot form produced no receipt, hash or RESULT, so it would have been an orchestrator-written receipt for a review it did not perform (R5). v7 makes the Codex review a `codex exec --sandbox read-only` run under a `codex-review` identity with its own receipt and RESULT, names it in the enforcement row and V4, keeps the Bot's review as swept feedback, and adds the bare-mode skills premise (round-6 INV-5 note, acted on in V2). Round 7 (Claude, 22:31Z, `accept`) confirmed INV-7. The first Codex review (`…-design-review-round7-codex.md`, `codex-review-dot-h001`, 22:34Z, `reject`) rejected INV-1, 3, 4, 5, 6, 9, 10, 12, all on one theme: evidence the orchestrator authors. v8 answers each: the waiver becomes a command under a `permissions.ask` rule (INV-1, INV-6) with the one-account residual stated in section 9; `repro:` is dropped and `check=` is a test selector only (INV-3); premises are reviewer and auditor evidence and the counting is the mechanical part (INV-4); the audit carries an input manifest and the acceptance record has an audit-input boundary (INV-5); cost records name their raw sources and stay a warning metric (INV-9); first push is the first commit's committer date and dispatchability is defined (INV-10); the independent oracle for gate-script PRs is the trusted-root audit (INV-12). The Codex P2 on the bare-mode skills premise is not adopted: the headless page says verbatim that "A directory you name with --add-dir is a partial exception: bare mode loads skills from its .claude/skills/ folder". Codex round 8 (`…-design-review-round8-codex.md`, 22:39Z, `reject`) accepted INV-1, 6, 7, 8, 9, 11 and the one-account residual, withdrew its bare-mode P2, and rejected INV-2 (tests unbounded), INV-3 (a changed file is not a run selector), INV-4 (sampling), INV-5 (the skills refusal was a premise, not a rule), INV-10 (committer date is not a push time; dependencies), INV-12 (a model audit is not a deterministic oracle), plus two stale enforcement rows. v9 adopts all: a 1000-line cap under tests/; the exact selector run on both heads in the PR's required `revise-check` job; every premise dispositioned by each reviewer and the auditor; the `.claude/**` refusal inside INV-5; the draft PR's `created_at` and an `after` list for dispatchability; a `main-tests` required job running main's tests against the PR's scripts (V5c); the two rows fixed. Claude round 8 (`…-design-review-round8.md`, 22:41Z, `revise`) rejected INV-1 (the waive script had no owner or row), INV-5 (once-per-head versus re-audit on a stale manifest) and INV-10 (fixed in v9), and offered a stronger anchor: the waiver record in a directory outside the sandbox write roots. Codex round 9 (`…-design-review-round9-codex.md`, 22:46Z, `reject`) accepted ten, rejected INV-5 (the `.claude/**` refusal that v9 claimed was silently lost by a failed edit, confirmed by grep) and INV-12 (the oracle must precede the waves), dispositioned all twelve premises (nine hold, three unverifiable in its read-only sandbox), and raised GitHub's 2026-11-02 `pull_request_target` policy. v10: the refusal is in INV-5 and verified by grep; one valid audit per head with stale-manifest replacement; the runner computes the manifest; the waiver record lives outside the sandbox write roots and V3a owns the script (map entry `[INV-6, INV-1]`); `main-tests` is wave V0 and every code wave is contract-first (INV-12, INV-2); the policy premise and residual. Claude round 9 (`…-design-review-round9.md`, 22:46Z, `revise`) found that `main-tests` as drafted would fail every intentional change and proposed running main's modules only for scripts outside `allowed_files`; Codex round 10 (`…-design-review-round10-codex.md`, 22:50Z, `reject`) accepted INV-1..11 and found that contract-first tests cannot merge ahead of an implementation that changes an existing script, proposing dormant contracts that `main-tests` activates on the implementation PR. v11's INV-12 is the union: main's modules as they are for undeclared scripts, main's dormant contracts (`REGIME_CONTRACT=1`) for declared ones, contract PRs required for design-tier waves; INV-1 states that the record's location is the guard and the ask rule the second layer (Claude round 9). Codex round 11 (`…-design-review-round11-codex.md`, 22:52Z) accepted INV-1..12 with no findings. Claude round 11 (`…-design-review-round11.md`, 22:54Z, `revise`) accepted everything but two INV-12 clauses: contracts must not stay dormant forever (the implementation PR removes the decorator; main-tests judges it against main's dormant copy) and an empty contract must fail a design-tier implementation PR. v12 adds both sentences to INV-12 and V0. Claude round 12 (`…-design-review-round12.md`, 22:57Z) accepted v12; Codex round 12 (`…-design-review-round12-codex.md`, 22:57Z, `revise`) accepted INV-1..11 and asked for a failing check behind the decorator-removal clause. v13 adds it to INV-12 (main-tests fails an implementation PR whose declared test module still carries a contract marker) and V0 carries it with the task-file reviewer's three V0 items (main's tests overlaid on a copy of the PR tree, module selection from the task's declared tests/ entries, task.md read with PyYAML). Round 13 (Claude 23:01Z, Codex 23:01Z and the premise map 23:17Z) accepted v13. Plan 006 (approved 2026-10-11) A102 amends two hashed keys: INV-12 states the in-process oracle's authenticated completion (nonce runner) and its residual, after the Codex Bot's P1 on V0's round-1 head repeated the class of the round-0 audit's finding 3; INV-2 and the map gain the .orchestration-only CI skip (`dotfiles-T128-ci-skip-orchestration-a01`, plan A201) that plan 006 orders as Phase 2. Round 14 (Codex 02:42Z `accept`; Claude 02:43Z `revise`): INV-12's residual clause understated the gap (the nonce authenticates the writer, not the counts; in-process patching of unittest's result collection forges counts with a genuine nonce) and INV-2 should cover every required check. v15 states the residual as it is, adds the runner's pinning of unittest classes, and words INV-2 for every required workflow. Round 15 asks both reviewers at once for one verdict each on this hash. Sources are the repository paths under `.orchestration/validation/dotfiles-T128-regime-v3-a01-research/` (`baseline.md`, `practice-evidence.md`, `claude-code-factsheet.md`, `codex-factsheet.md`, `github-factsheet.md`, `method-draft.md`). Receipt: `.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round15.md` (Claude) and `…-design-review-round15-codex.md` (Codex); the whole-file sha256 of this file in both headers.
227:v18 (plan 006 B0, plan 007 T701; written by the orchestrator under the records exemption, 2026-10-12): INV-12 narrowed to the undeclared-change regression guard: `main-tests` runs main's test module of every script outside `allowed_files`; a script inside `allowed_files` is judged by the PR's tests, the diff review and the trusted-root audit; the dormant-contract clauses, `REGIME_CONTRACT` and the `<task>-contract-a01` PRs are removed (A302 withdrew V1's contract PR under the Phase A correction and no wave has used one); `main-tests` decides inside its own job as the A5 workflows do. INV-2 loses the dead `-contract-a01` comparison and names A5's in-job form. `implementing_tasks` gains the V0 successor `dotfiles-T128-v0-main-tests-a02: [INV-12]` (A301) and `dotfiles-T128-gate-evidence-a01: [INV-6]` (plan 007 T702: the gate's `evidence=` grammar and the S6 refusal at INV-6's mandatory point). The INV-12 enforcement row, the V0 wave row and the wave order follow. Round 20 asks both reviewers at once for one verdict each on this hash: receipts `.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round20.md` (Claude) and `…-design-review-round20-codex.md` (Codex); the whole-file sha256 of this file in both headers.
229:v19 (round 20's one revision, 11:43Z): INV-6 gains the clause the Claude round-20 receipt asked for (the Codex round-20 receipt accepted v18 with no rejection), so `dotfiles-T128-gate-evidence-a01: [INV-6]` maps to a sentence that states the two refusals; nothing else changes. Round 21 asks both reviewers at once for one verdict each on this hash: receipts `…-design-review-round21.md` (Claude) and `…-design-review-round21-codex.md` (Codex).
231:v20 (11:46Z): the Codex round-21 receipt found the v19 clause appended to INV-4 (a stale line number after v18's two map insertions), so v20 moves that exact clause to the end of INV-6; INV-4 returns to its v18 text; nothing else changes. Round 22 asks both reviewers at once for one verdict each on this hash (round 21 was never sent to the Claude seat): receipts `…-design-review-round22.md` (Claude) and `…-design-review-round22-codex.md` (Codex).
235:v21 (13:08Z, the orchestrator under the records exemption): `implementing_tasks` gains `dotfiles-T128-gate-evidence-a02: [INV-6]`, the INV-6 successor of `dotfiles-T128-gate-evidence-a01` (withdrawn 13:02Z under INV-6 before its second amendment; reset record `dotfiles-T128-gate-evidence-a01-design-reset.md`), beside the a01 entry that stays as parked history, as the V0 and round-18 successors did; nothing else changes. Round 24 asks both reviewers at once for one verdict each on this hash: receipts `…-design-review-round24.md` (Claude) and `…-design-review-round24-codex.md` (Codex).
237:v22 (15:28Z, the orchestrator under the records exemption): `implementing_tasks` gains `dotfiles-T128-gate-evidence-a03: [INV-6]`, the INV-6 successor of a02 (withdrawn 15:25Z after its second S1 cycle; plan 011 option F: the acceptance record's machine-read parts as YAML front matter), beside the a01 and a02 entries kept as parked history; nothing else changes. Round 25 asks both reviewers at once for one verdict each on this hash: receipts `…-design-review-round25.md` (Claude) and `…-design-review-round25-codex.md` (Codex).
239:v23 (2026-10-13 02:55Z, the orchestrator under the records exemption): `implementing_tasks` gains `dotfiles-T128-gate-evidence-a04: [INV-6]`, the INV-6 successor of a03 (withdrawn 02:3xZ after the fourth binding row; plan 014 option A: the acceptance record's `ledger` must cover every swept Codex finding id and every audit finding `audit:<sha7>:<n>`, a set difference the gate computes; the a04 file's hash is in the reset record `dotfiles-T128-gate-evidence-a03-design-reset.md`, not here), beside the a01 to a03 entries kept as parked history; nothing else changes. Round 26 asks both reviewers at once for one verdict each on this hash: receipts `…-design-review-round26.md` (Claude) and `…-design-review-round26-codex.md` (Codex).
241:v24 (2026-10-13 03:05Z, the orchestrator under the records exemption): the v23 line named the a04 file's hash, which moved when round 26's Codex half found the coverage sentence omitted badged Codex review bodies (a04 round 4 after round 3; no a04 hash appears in this design, the reset record `dotfiles-T128-gate-evidence-a03-design-reset.md` is the sole anchor, so later a04 rounds do not move the design); the map entry `dotfiles-T128-gate-evidence-a04: [INV-6]` is unchanged; nothing else changes. Rounds 27 and 28 ask both reviewers at once for one verdict each on this hash: receipts `…-design-review-round28.md` (Claude) and `…-design-review-round28-codex.md` (Codex); round 27's Codex half found the two hash mentions this text removed.
---
task_id: dotfiles-T128-chain-review-scripts-a01
seat: claude-standard-dot-a002
permission_gated_commands: see the table
---

# Sandbox record: dotfiles-T128-chain-review-scripts-a01

- Period: from the AGMSG-TASK (08:54:36Z) to the RESULT.
- Inside the sandbox ran:
  - the HTTPS `git fetch` and `git push`;
  - the branch, the commit, the task copy and the evidence;
  - every test, lint and format run;
  - the mutation pass and the validation script.
- In the sandbox uv cannot reach pypi, so every uv run used `UV_OFFLINE=1` from the uv cache (validation, header). `uvx ruff` could not write uv's tool directory, so ruff ran as the installed `ruff` 0.17.0.
- macOS `mktemp` without a template writes under `/var/folders/…`, which the sandbox denies. That is why item 1 now names a template (amendment 1, learning 1).
- `diff` cannot open a `/dev/fd` process substitution in the sandbox, so validation §3 diffs scratch files instead.
- The whole unit suite fails in the sandbox (validation, intro); CI's run is the evidence.
- No local mutation was chained onto a call that ran outside the sandbox.

The table lists every call that ran outside the sandbox: `gh` through the permission gate (`dangerouslyDisableSandbox`, since `gh` fails TLS inside the sandbox) and `agmsg-dispatch` through `excludedCommands`. Rows after the evidence commit are completed in the evidence update.

| # | Command | Step 4 case |
|--:|---|---|
| 1 | `agmsg-dispatch … AGMSG-PONG v1 task_id=dotfiles-T128-chain-review-scripts-a01 status=question …` (09:02Z, row 11 and the worktree guard) | `agmsg-dispatch` |
| 2 | `agmsg-dispatch … AGMSG-PONG v1 … status=working …` (09:05Z, the `mktemp` template) | `agmsg-dispatch` |
| 3 | `agmsg-dispatch … AGMSG-PONG v1 … status=working …` (12:15Z, the branch state) | `agmsg-dispatch` |
| 4 | `gh pr create --draft --repo mryfmo/dotfiles --base main --head regime/chain-review-scripts …` (PR #357) | `gh` |
| 5 | `gh pr ready 357 --repo mryfmo/dotfiles; date +%s; date -u +%FT%TZ` (12:42:37Z) | `gh` |
| 6 | the Bot wait on `0da6be3e` (`scratchpad/bot-wait.sh`, background; `gh pr view` and `gh api` reads every 30 seconds) | `gh` |
| 7 | `gh pr checks 357 --watch` (background, after a `gh pr checks` poll for the first check; exit 0) | `gh` |
| 8 | `gh api` reads of the two Bot comments and of review 5518077170's body | `gh` |
| 9 | `gh api` re-list of the Bot's top-level comments (validation §9) | `gh` |
| 10 | `agmsg-dispatch … AGMSG-PONG v1 … status=alive …` (12:47Z, the Bot's two P2 threads) | `agmsg-dispatch` |
| 11 | `gh pr checks 357 --watch` on the final head (background, exit status joined) | `gh` |
| 12 | `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T128-chain-review-scripts-a01 …` | `agmsg-dispatch` |

One command was denied at the permission gate and not pursued: a re-list that ran four reads in one call, the Bot's comment count, the PR's reviews, its issue comments and a GraphQL listing of its review threads. The GraphQL thread listing is not needed, since the worker resolves no thread. Row 9 ran the comment re-list alone, the same `gh api …/pulls/357/comments` read that row 8 had already run.

The pushes of `1f307a6e`, `0da6be3e` and the evidence update ran inside the sandbox over HTTPS.
{
  "repo": "mryfmo/dotfiles",
  "pr": 357,
  "head_sha": "b6ce4ffabe0e66a102e224e75be575a501c5a793",
  "base_ref": "main",
  "base_sha": "ec94dc56305f55df470a4b1d4215ad272418beac",
  "generated_at": "2026-10-14T13:22:09+00:00",
  "checks": [
    {
      "name": "test (macos-14, client)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38569353137/job/115870143037"
    },
    {
      "name": "test (ubuntu-26.04, client)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38569353137/job/115870142793"
    },
    {
      "name": "validate",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38569353190/job/115870142550"
    },
    {
      "name": "public-bootstrap (ubuntu-24.04, client)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38569353120/job/115870142531"
    },
    {
      "name": "test (ubuntu-24.04, server)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38569353137/job/115870142461"
    },
    {
      "name": "private-bootstrap (ubuntu-24.04, server)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38569353120/job/115870142369"
    },
    {
      "name": "public-bootstrap (macos-14, client)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38569353120/job/115870142276"
    },
    {
      "name": "private-bootstrap (macos-14, client)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38569353120/job/115870142265"
    },
    {
      "name": "public-bootstrap (ubuntu-24.04, server)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38569353120/job/115870142251"
    },
    {
      "name": "test (ubuntu-24.04, client)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38569353137/job/115870142077"
    },
    {
      "name": "private-bootstrap (ubuntu-24.04, client)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38569353120/job/115870141871"
    },
    {
      "name": "GitGuardian Security Checks",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/runs/115870136403"
    }
  ],
  "items": [
    {
      "source": "issue_comment",
      "author": "coderabbitai[bot]",
      "bot": true,
      "level": "comment",
      "path": null,
      "line": null,
      "body": "<!-- This is an auto-generated comment: summarize by coderabbit.ai -->\n<!-- This is an auto-generated comment: skip review by coderabbit.ai -->\n\n> [!IMPORTANT]\n> ## Review skipped\n> \n> Auto reviews are disabled on this repository. Please check the settings in the CodeRabbit UI or the `.coderabbit.yaml` file in this repository. To trigger a single review, invoke the `@coderabbitai review` command.\n> \n> <details>\n> <summary><strong>⚙️ Run configuration</strong></summary>\n> <dl>\n> <dd>\n> \n> - **Configuration used**: Repository: mryfmo/dotfiles/.coderabbit.yaml\n> - **Review profile**: CHILL\n> - **Plan**: Advanced\n> - **Run ID**: `594cddb7-b017-40ee-bf8d-ca4224d24cca`\n> \n> </dd>\n> </dl>\n> </details>\n> \n> You can disable this status message by setting the `reviews.review_status` to `false` in the CodeRabbit configuration file.\n> \n> Use the checkbox below for a quick retry:\n> - [ ] <!-- {\"checkboxId\":\"e9bb8d72-00e8-4f67-9cb2-caf3b22574fe\"} --> 🔍 Trigger review\n\n<!-- end of auto-generated comment: skip review by coderabbit.ai -->\n\n<!-- autopilot:start -->\n- [ ] <!-- {\"checkboxId\":\"2708ad07-9f24-4260-9c11-7dc76a49f2e3\"} --> <strong title=\"Keep fixing CodeRabbit findings and required CI, and resolving merge conflicts\">Autofix</strong> · Keep fixing CodeRabbit findings and required CI, and resolving merge conflicts\n<!-- autopilot:end -->\n<!-- tips_start -->\n\n\n\nThanks for using [CodeRabbit](https://coderabbit.ai?utm_source=oss&utm_medium=github&utm_campaign=mryfmo/dotfiles&utm_content=357)! It's free for OSS, and your support helps us grow. If you like it, consider giving us a shout-out.\n\n<details>\n<summary><strong>❤️ Share</strong></summary>\n<dl>\n<dd>\n\n- [X](https://twitter.com/intent/tweet?text=I%20just%20used%20%40coderabbitai%20for%20my%20code%20review%2C%20and%20it%27s%20fantastic%21%20It%27s%20free%20for%20OSS%20and%20offers%20a%20free%20trial%20for%20the%20proprietary%20code.%20Check%20it%20out%3A&url=https%3A//coderabbit.ai)\n- [Mastodon](https://mastodon.social/share?text=I%20just%20used%20%40coderabbitai%20for%20my%20code%20review%2C%20and%20it%27s%20fantastic%21%20It%27s%20free%20for%20OSS%20and%20offers%20a%20free%20trial%20for%20the%20proprietary%20code.%20Check%20it%20out%3A%20https%3A%2F%2Fcoderabbit.ai)\n- [Reddit](https://www.reddit.com/submit?title=Great%20tool%20for%20code%20review%20-%20CodeRabbit&text=I%20just%20used%20CodeRabbit%20for%20my%20code%20review%2C%20and%20it%27s%20fantastic%21%20It%27s%20free%20for%20OSS%20and%20offers%20a%20free%20trial%20for%20proprietary%20code.%20Check%20it%20out%3A%20https%3A//coderabbit.ai)\n- [LinkedIn](https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Fcoderabbit.ai&mini=true&title=Great%20tool%20for%20code%20review%20-%20CodeRabbit&summary=I%20just%20used%20CodeRabbit%20for%20my%20code%20review%2C%20and%20it%27s%20fantastic%21%20It%27s%20free%20for%20OSS%20and%20offers%20a%20free%20trial%20for%20proprietary%20code)\n\n</dd>\n</dl>\n</details>\n\n\n<sub>Comment `@coderabbitai help` to get the list of available commands.</sub>\n\n<!-- tips_end -->",
      "url": "https://github.com/mryfmo/dotfiles/pull/357#issuecomment-6168583881",
      "disposition": "not-applicable:bot summary or onboarding comment, no finding; evidence=gh api repos/mryfmo/dotfiles/issues/comments/6168583881 --jq '.user.login,.body'"
    },
    {
      "source": "issue_comment",
      "author": "chatgpt-codex-connector[bot]",
      "bot": true,
      "level": "comment",
      "path": null,
      "line": null,
      "body": "<!-- codex-pull-request-review-summary -->\n<!-- codex-security-review:v1 {\"blockingSeverityThreshold\":\"P0\",\"headSha\":\"0da6be3e10964ff744262e835806fa8081e93ed7\",\"mergeGateEnabled\":false,\"pullRequestNumber\":357,\"repository\":\"mryfmo/dotfiles\",\"status\":\"completed\"} -->\n## Codex Review Summary\n\nThis comment shows the latest Codex review activity on this pull request.\n\n| Review | Status | Commit | Review trigger |\n| --- | --- | --- | --- |\n| 📝 **Code Review** | ✅ **Completed** <relative-time datetime=\"2026-10-14T12:45:24.915155Z\">2026-10-14T12:45:24.915155Z</relative-time> | `0da6be3` | Draft marked ready |\n| 🔒 **Security Review** | ✅ **Completed** <relative-time datetime=\"2026-10-14T12:55:10.117456Z\">2026-10-14T12:55:10.117456Z</relative-time> | `0da6be3` | Draft marked ready |\n\n\n\n<details> <summary>ℹ️ About Codex in GitHub</summary>\n<br/>\n\n[Your team has set up Codex to review pull requests in this repo](https://chatgpt.com/codex/cloud/settings/general). Reviews are triggered when you\n- Open a pull request for review\n- Mark a draft as ready\n- Comment \"@codex review\" or \"@codex security review\".\n\nCodex reacts with 👀 while any review is running, comments if it has suggestions, and reacts with 👍 once all reviews finish with no findings.\n\n</details>",
      "url": "https://github.com/mryfmo/dotfiles/pull/357#issuecomment-6168603632",
      "disposition": "not-applicable:bot summary or onboarding comment, no finding; evidence=gh api repos/mryfmo/dotfiles/issues/comments/6168603632 --jq '.user.login,.body'"
    },
    {
      "source": "review",
      "author": "chatgpt-codex-connector[bot]",
      "bot": true,
      "level": "commented",
      "path": null,
      "line": null,
      "body": "\n### 💡 Codex Review\n\nHere are some automated review suggestions for this pull request.\n\n**Reviewed commit:** `0da6be3e10`\n    \n\n<details> <summary>ℹ️ About Codex in GitHub</summary>\n<br/>\n\nCodex has been enabled to automatically review pull requests in this repo. Reviews are triggered when you\n- Open a pull request for review\n- Mark a draft as ready\n- Comment \"@codex review\".\n\nIf Codex has suggestions, it will comment; otherwise it will react with 👍.\n\n\n\n\nWhen you [sign up for Codex through ChatGPT](https://openai.com/codex), Codex can also answer questions or update the PR, like \"@codex address that feedback\".\n            \n</details>",
      "url": "https://github.com/mryfmo/dotfiles/pull/357#pullrequestreview-5518077170",
      "commit": "0da6be3e10964ff744262e835806fa8081e93ed7",
      "disposition": "not-applicable:review object, its findings are the inline threads, each dispositioned on its own; evidence=gh api repos/mryfmo/dotfiles/pulls/357/reviews/5518077170 --jq '.state,.body'"
    },
    {
      "source": "review_comment",
      "author": "chatgpt-codex-connector[bot]",
      "bot": true,
      "level": "comment",
      "path": "scripts/orchestrator/local-review.sh",
      "line": 61,
      "body": "**<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Reject failed review runs instead of caching them**\n\nWhen Codex exits nonzero because of authentication, configuration, or runtime failure before producing findings, this handler discards that status and writes a `findings: 0` validation file; subsequent invocations then reuse it as a successful review. The new test explicitly accepts exit 0 for a status-5 reviewer, so the local-review threat-table row does not fail closed. Preserve the reviewer failure status and do not cache the transcript as a completed review.\n\nAGENTS.md reference: [AGENTS.md:L78-L78](https://github.com/mryfmo/dotfiles/blob/0da6be3e10964ff744262e835806fa8081e93ed7/AGENTS.md#L78-L78)\n\nUseful? React with 👍 / 👎.",
      "url": "https://github.com/mryfmo/dotfiles/pull/357#discussion_r4270918132",
      "resolved": false,
      "outdated": false,
      "disposition": "not-applicable:advisory P2 owned by dotfiles-T128-chain-review-scripts-followup-a01 (local-review.sh:61 writes a findings-0 file on a non-zero review-binary exit and the next run reuses it, the input continuation item 1 states); evidence=grep -n 'Owned by dotfiles-T128-chain-review-scripts-followup-a01' .orchestration/acceptance/dotfiles-T128-chain-review-scripts-a01.md"
    },
    {
      "source": "review_comment",
      "author": "chatgpt-codex-connector[bot]",
      "bot": true,
      "level": "comment",
      "path": "scripts/orchestrator/local-review.sh",
      "line": 28,
      "body": "**<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Validate the full head before reusing a cached review**\n\nWhen two heads for the same task share their first seven hexadecimal characters, this branch reuses the earlier file without comparing its recorded full `head:` value to the requested commit; the newer head is therefore never reviewed. The closed test only repeats the identical head and does not establish the promised one-review-per-PR-head behavior. Key the file by the full hash or verify the stored full hash before reuse.\n\nAGENTS.md reference: [AGENTS.md:L78-L78](https://github.com/mryfmo/dotfiles/blob/0da6be3e10964ff744262e835806fa8081e93ed7/AGENTS.md#L78-L78)\n\nUseful? React with 👍 / 👎.",
      "url": "https://github.com/mryfmo/dotfiles/pull/357#discussion_r4270918140",
      "resolved": false,
      "outdated": false,
      "disposition": "not-applicable:advisory P2 owned by dotfiles-T128-chain-review-scripts-followup-a01 (local-review.sh:28 keys the reuse on the sha7 prefix and never compares the recorded full head, the input file name item 1 states); evidence=grep -n 'Owned by dotfiles-T128-chain-review-scripts-followup-a01' .orchestration/acceptance/dotfiles-T128-chain-review-scripts-a01.md"
    },
    {
      "source": "annotation",
      "author": "github-actions",
      "bot": true,
      "level": "notice",
      "path": ".github",
      "line": 1,
      "body": "Due to capacity constraints, jobs targeting macOS arm64 runners may experience longer queue times.",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38569353137/job/115870143037",
      "check": "test (macos-14, client)",
      "disposition": "not-applicable:runner capacity notice, no finding; evidence=gh run view 38569353137 --repo mryfmo/dotfiles --job 115870143037"
    },
    {
      "source": "annotation",
      "author": "github-actions",
      "bot": true,
      "level": "notice",
      "path": ".github",
      "line": 1,
      "body": "Due to capacity constraints, jobs targeting macOS arm64 runners may experience longer queue times.",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38569353120/job/115870142276",
      "check": "public-bootstrap (macos-14, client)",
      "disposition": "not-applicable:runner capacity notice, no finding; evidence=gh run view 38569353120 --repo mryfmo/dotfiles --job 115870142276"
    },
    {
      "source": "annotation",
      "author": "github-actions",
      "bot": true,
      "level": "notice",
      "path": ".github",
      "line": 1,
      "body": "Due to capacity constraints, jobs targeting macOS arm64 runners may experience longer queue times.",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38569353120/job/115870142265",
      "check": "private-bootstrap (macos-14, client)",
      "disposition": "not-applicable:runner capacity notice, no finding; evidence=gh run view 38569353120 --repo mryfmo/dotfiles --job 115870142265"
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
      "disposition": "not-applicable:CI status, no finding; evidence=gh pr checks 357 --repo mryfmo/dotfiles"
    }
  ]
}

mcp: codex_apps/github.fetch_commit_workflow_runs (completed)
mcp: codex_apps/github.list_pull_request_reviews (completed)
mcp: codex_apps/github.list_pull_request_review_threads (completed)
**Reading design file partially**
exec
/bin/zsh -lc "sed -n '1,80p' .orchestration/tasks/dotfiles-T128-regime-v3-a01.md" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 47ms:
---
format: 2
task_id: dotfiles-T128-regime-v3-a01
kind: design
security: true
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
implementing_tasks:
  dotfiles-T128-v0-main-tests-a01: [INV-12]
  dotfiles-T128-v1-task-schema-a01: [INV-1]
  dotfiles-T128-v1c-regime-ci-check-a01: [INV-1]
  dotfiles-T128-v1b-pr-caps-a01: [INV-2]
  dotfiles-T128-ci-skip-orchestration-a01: [INV-2]
  dotfiles-T128-ci-skip-orchestration-a02: [INV-2]
  dotfiles-T128-v2-audit-schema-and-runner-a01: [INV-5]
  dotfiles-T128-v2b-audit-gate-a01: [INV-5]
  dotfiles-T128-regime-counters-a01: [INV-6]
  dotfiles-T128-regime-counters-a02: [INV-6]
  dotfiles-T128-v3a-reset-counters-a01: [INV-6, INV-1]
  dotfiles-T128-v3b-premises-and-amendments-a01: [INV-4]
  dotfiles-T128-v3c-one-fact-per-round-a01: [INV-3]
  dotfiles-T128-v3d-idle-and-first-push-a01: [INV-10]
  dotfiles-T128-v4-design-review-runner-a01: [INV-7]
  dotfiles-T128-v5a-evidence-on-branch-a01: [INV-8]
  dotfiles-T128-v5b-cost-fields-a01: [INV-9]
  dotfiles-T128-v6-permgate-session-a01: [INV-11]
  dotfiles-T128-v0-main-tests-a02: [INV-12]
  dotfiles-T128-gate-evidence-a01: [INV-6]
  dotfiles-T128-gate-evidence-a02: [INV-6]
  dotfiles-T128-gate-evidence-a03: [INV-6]
  dotfiles-T128-gate-evidence-a04: [INV-6]
supersedes:
  - dotfiles-T126-regime-v2-a01
  - dotfiles-T124-design-gate-and-reset-rule-a01
reset_of:
  - dotfiles-T124-wave1-task-validator-a01
  - dotfiles-T124-wave3b-audit-grammar-a01
threat_model:
  R1: rounds are judged by models re-reading models and add no deterministic fact, so a wrong premise is patched round after round (T118 20 revises, T119 5 revises and 4 audits; the vendor's own rule is two corrections, then start fresh)
  R2: "hand-written parsers at a trust boundary have an unbounded bypass surface (PR 313: 33 of 52 Bot threads on a 503-line validator with its own YAML parser, written on the false premise that PyYAML is unavailable)"
  R3: "PRs larger than a reviewer can hold (PR 313 20 files +2642, PR 312 37 files +3191; Google: 100 lines reasonable, 1000 too large)"
  R4: task text grown by question-and-amendment (PR 313 6 questions 8 amendments, T119 8 and 8, T120 8 amendments and no RESULT) keeps the under-researched premise
  R5: the orchestrator's artifacts are unaudited and it dispositions findings about itself (T119 audit-finding 2); the reset rule was prose the orchestrator could waive (PR 313 revise round 2)
  R6: "the auditor becomes a serial queue when audits run once per round in one tab (measured: 4 audits about 1.3 h of T119's 11.1 h; the rounds, not the audits, were the cost)"
  R7: cost is unmeasured (every acceptance record says cost n/a) so no stage can be weighed against its value
  R8: a PR can change the check that judges it (a pull_request workflow runs the PR head's workflow file); host-side evidence is whatever the orchestrator copies into the gate's cwd
trust_anchors:
  - agmsg message history (append-only, read through history.sh) for who did what and when; GitHub for PR, CI, Bot, ruleset and merge state; the main checkout for files, never the gate's cwd
  - JSON Schema documents validated by the jsonschema library (PyYAML for front matter) for task files, audit verdicts, design-review receipts and evidence; model verdicts produced under schema (codex exec --output-schema, server-side strict; claude -p --json-schema)
  - mechanical checks run from main's workflow file as a pull_request_target required status check that reads PR files as data and executes nothing from the PR; required workflows are organization-only, so this is the main-pinned form available to a user-owned repository
  - the operator waiver is visible, not prevented (acceptance record, boundary PR body, check-regime-boundary)
  - a reset is released only by a redesign written in a context other than the one that wrote the abandoned task, or by the operator
invariants:
  INV-1: "every task is a format-2 file whose front matter validates against schemas/task.json (jsonschema + PyYAML, no hand-written parser; every allowed_files entry starts with a literal path segment and a wildcard entry derives the tier of every design-tier path its literal prefix can cover); legacy task ids are grandfathered only for files under .orchestration/tasks/ on main, never for a branch copy; the tier (docs, review, design) is derived from allowed_files by the shared high-risk module, with the regime's own rule prose (home/dot_config/claude/rules/**, the agmsg-orchestration SKILL, AGENTS.md, README) listed in the review tier, and selects the pipeline from process_tiers in agent-config.yaml; every AGMSG-TASK for the task, the first and each amendment, carries task_sha256= of the task file as sent, the worker commits the file byte-identical to .orchestration/<task id>/task.md (first commit, recommitted after each amendment), the CI regime job validates that copy with main's schema and refuses a PR that changes .github/workflows/** unless its task.md is design tier and lists the file, the host gate compares the copy's sha256 with the latest AGMSG-TASK's token in history, and the regime check binds only once the ruleset lists it as required (an operator action named in V1's acceptance record); the orchestrator can add or skip a stage only with an operator waiver written by scripts/regime-waive.sh, a command under a permissions.ask rule in the managed settings with no permgate policy entry, so that only the human's answer to the native prompt runs it (an ask rule prompts even in auto mode; agent-to-agent approval is forbidden); the waiver names the task, the stage and a reason and is written under $XDG_STATE_HOME/regime/waivers/, a directory outside every seat's sandbox write roots, so no sandboxed seat can write it and only a command run outside the sandbox on the human's answer to the native prompt can (the directory is the guard; the ask rule on the named command is the second layer, since a reworded command would still meet the prompt at the sandbox boundary); it is listed by check-regime-boundary.sh and the boundary PR body (V3a owns the script and its ask rule), and is the strongest friction available on a machine where every seat and GitHub action is the operator's own account (operator authentication is a stated residual, not a claim)"
  INV-2: "a PR is mergeable only within the caps the CI regime job enforces from main's workflow (at most 15 changed files outside .orchestration/, 500 added lines outside tests/, .orchestration/ and the data list scripts/legacy-task-ids.txt, and 1000 added lines under tests/), and its task.md invariants equal the design's as a set of ids and byte-for-byte as sentences (the design read from main, never from the PR); the design file must be on main (through a boundary PR) before the implementing TASK is dispatched and the regime job fails closed when the design named by task.md is absent from main; an .orchestration-only PR runs no bootstrap or test matrix and every required check context still reports success (each required workflow decides inside each of its jobs, as test.yaml and remote.yaml do since A5: no job-level if and no needs, because a skipped required job reports success), so a boundary PR merges in minutes; exceeding a cap is a split, never a finding to disposition (the cap changes the unit of work: T116 +529 and T118 +881 would have been split)"
  INV-3: "a revise round is admissible only when it adds a new deterministic check: the AGMSG-ACCEPTANCE status=revise carries check=tests/<file>::<name> and previous_head=<the RESULT head being revised>, the worker records both in .orchestration/<task id>/revise.yaml (a sibling file; task.md stays byte-identical to the dispatched file), the main-pinned regime job verifies that the named test file exists on the head and differs between previous_head and the head, the PR's own unit-test workflow (a required check, run in the PR's context) collects and runs exactly that selector on the head (it must pass) and on previous_head (it must fail or be absent), and the host gate, which reads history, verifies that previous_head equals the head of the previous AGMSG-RESULT for the task and requires the same selector in the validation file; a finding that cannot become a test is dispositioned, never iterated"
  INV-4: "a task file carries premises, each with the command and pasted output that verified it before dispatch; premises are evidence for the design reviewers and the auditor, each of whom dispositions every premise in the receipt or audit JSON as holds, fails or unverifiable (a local command re-run, an external claim re-fetched; a fails is a specification finding and a rejection), a complete disposition the schema requires rather than a sample, and the mechanical part of this invariant is the counting: a worker question (AGMSG-PONG status=question) is a specification defect answered by at most one further AGMSG-TASK, amendments are every AGMSG-TASK for the task_id after the first, whatever its wording, and the second amendment or the second question is INV-6's count, which withdraws the task to design through INV-6's merge backstop and Stop signal"
  INV-5: "the task-level audit is a headless read-only run whose instruction root is the trusted main checkout and whose schema is main's schemas/audit.json: codex exec --output-schema <main>/schemas/audit.json -C <main> with the detached worktree at the head added as a read-only data directory (--add-dir), so the audited PR controls neither the schema nor the AGENTS.md the auditor reads; the fallback claude -p --json-schema from the same root with --add-dir <worktree>, --bare when an API key is set and otherwise with project and user hooks disabled, and refused with exit 2 blocked when the head changes any file under .claude/ (bare mode loads skills from an --add-dir directory's .claude/skills/), leaving such a head to the codex path), with at most one valid audit per head (a stale input manifest invalidates an audit and a new audit of the same head replaces it), pooled two at a time; the gate accepts an audit of an earlier head only when git diff --quiet <audited head> <HEAD> -- . ':!.orchestration' holds (an evidence-only revision), otherwise a new audit is required; its input includes the task's invariants and premises, the worker's evidence, the orchestrator's task file and amendments, the acceptance record as it stands when present (its text above the line <!-- audit-input-boundary --> is the pre-audit part; dispositions of this audit's findings are appended below it), the head's pr-feedback JSON and the previous round's audit JSON; the audit JSON carries an input manifest (path to sha256 of every input as read, computed by the runner, which overwrites any model-supplied value) and the gate recomputes the manifest at gate time, so a pre-audit input edited after the audit makes the audit stale and a new audit is required; the schema lists findings {priority, confidence, category in {specification, implementation, evidence, orchestration, conformance}, path, line, rationale} and the per-invariant map before the verdict, and the prompt asks for the rationale before each verdict; the runner, under the identity claude-audit-dot-h001 or codex-audit-dot-h001 on the orchestrator's host, records the JSON's sha256 in agmsg history (AGMSG-AUDIT v1 task_id= head= sha256= auditor=) before the gate reads it, an anchor that prevents edits after the record and not fabrication before it; the gate reads the verdict and categories from the JSON, and orchestration and conformance findings at P0-P2 accept only an operator waiver or a design reset, never not-applicable"
  INV-6: "the reset rule's mandatory point is the merge backstop in scripts/require-crit-review.py, with the orchestrator's Stop hook (Claude Stop hook, Codex [hooks].Stop) as the early signal, soft on both runtimes by their documented caps; counts come from history for the hook and the gate (revises = RESULTs for the task_id minus one, threshold 2; amendments = AGMSG-TASKs after the first, threshold 2; AGMSG-PONG status=question, threshold 2) and from GitHub and main-checkout files for the gate and the boundary check only (Codex Bot P0 or P1 on two heads after the first RESULT, from original_commit_id on review_comment items recorded by pr-feedback.py; an audit implementation or specification finding at P0-P1 on two heads, from .orchestration/validation/<task>-audit-<sha7>.json in the main checkout, each counted only when its sha256 matches its AGMSG-AUDIT record); when a count is reached the gate refuses the merge until a reset record names a redesign task whose design RESULT comes from an identity other than the task's author, or a waiver written by scripts/regime-waive.sh under the INV-1 ask-rule discipline into the state directory outside the sandbox write roots (the only release path besides a redesign; the one-account residual of INV-1 applies); check-regime-boundary.sh reports a closed-unmerged PR whose task has no reset record and a task over any count with neither an accepted acceptance record nor a reset record; the same gate refuses a merge whose acceptance record carries a not-applicable disposition without an evidence= clause, or a finding-class table with three rows of one class and no pasted search of the correction records (plan 007 S6)"
  INV-7: "the design tier adds, before any code is dispatched, two design reviews of the same design hash: a fresh Claude context on the review profile (a headless run or a seated -review- identity; the review profile is the same model and effort as deep, so the lever is the separate context) and a Codex read-only review (codex exec --sandbox read-only on the review profile under a codex-review identity: headless through V4's runner, or seated until V4); each receipt is a schema document naming the design file's canonical hash over invariants, threat_model, trust_anchors, implementing_tasks and premises, each is announced by an AGMSG-RESULT from its reviewing identity, and both RESULTs precede the implementing AGMSG-TASK in history; the Codex Bot's review of a boundary PR is swept feedback, never a design receipt; a change to the hashed keys needs new reviews; the gate accepts the whole-file sha256 form for receipts written before V4 lands"
  INV-8: "worker evidence (the task.md copy, revise.yaml, report, validation, sandbox, learning, autoskill, worker review JSON) is committed on the PR branch under .orchestration/<task id>/ before the final RESULT so the Bot, CI and the gate read the same files from the audited head; the orchestrator's records (audit JSON, acceptance, pr-feedback) stay under .orchestration/validation and .orchestration/acceptance in the boundary commit because the merge is --match-head-commit"
  INV-9: "every acceptance record carries measured cost (rounds, amendments, questions, wall time TASK to final RESULT from history timestamps, audit count, Bot threads, tokens: total_cost_usd from claude -p JSON, turn.completed.usage from codex exec --json, per-message usage from the seat's session transcript) written by accept-task.py, which also records the path and sha256 of every raw source it read (the headless runs' JSON, the transcript files at acceptance time) so a total can be recomputed; cost is a warning metric, never a gate: each tier has a budget, the acceptance record names the operator decision when it is exceeded, and check-regime-boundary.sh warns; headless runs carry --max-budget-usd"
  INV-10: "at most three concurrent workers with pairwise-disjoint allowed_files; the first push is the draft PR's server-side created_at (gh api pulls/<n>), which must fall within 30 minutes of the TASK's history timestamp, and a seated worker is not idle for 20 minutes while a dispatchable task exists, a dispatchable task being a format-2 file under .orchestration/tasks/ with no AGMSG-TASK for its id in history, no superseded_by or reset record, and every task id in its after list accepted (an acceptance record with Decision accepted in the main checkout); both computed in check-regime-boundary.sh and accept-task.py, never in the Stop hook; headless reviews and audits do not count as workers"
  INV-11: permgate records session_id and cwd per decision, and the gate compares a Claude worker's permission-gated Bash count in the task window with the sandbox record (an understated record is refused); Codex workers cannot escalate and are not covered
  INV-12: "every rule above is exercised by a unit test that fails when the rule is removed; the PR's own workflow runs the PR's tests, and a required check main-tests (wave V0, before every other wave) fetches main's tests/unit and runs, in the PR's context, main's test module of every script outside the task.md's allowed_files as it is, so an undeclared change to any script fails (the undeclared-change regression guard); a script inside allowed_files is judged by the PR's own tests, the orchestrator's diff review and the trusted-root audit (INV-5), which reads the test diff beside the code diff and reports a deleted or weakened fails-when-removed test as a conformance finding; main-tests decides inside its own job, as the A5 workflows do, with no changes job and no needs, so an .orchestration-only PR reports success from the job itself; main-tests is an in-process oracle: code that main's tests import from the PR runs inside the test process, so the harness authenticates that main's runner reached its end with a per-run nonce that only the runner sees (read from a pipe and closed before any test loads, written back with the counts), and the runner pins unittest's result and runner classes before importing any test; the nonce authenticates the writer, not the counts: adversarial PR code running in the same process can still patch result collection or read the nonce from a frame, so in-process forgery remains a stated residual that the trusted-root audit catches, named in every acceptance record of a design-tier PR; including one test per gaming path (a schema-valid task with a prose cap bypass, a revise without a named check, a revise list appended to the hashed task.md, an AGMSG-TASK without amendment= that still counts, an evidence-only relabel of a code change caught by the tree-equality check, a wave-table rewrite after review, an audit JSON edited after its history record, a receipt whose hash predates a key change, a reset record naming the author's own identity, a Bot-skipped head whose audit never starts, a single PR split only in the task file, a branch task.md claiming a legacy id, allowed_files of ['*'] or a wildcard first segment, an invariant sentence weakened under its id, a schema or AGENTS.md edited on the audited head, an undeclared script change that main-tests must fail); legacy task ids are grandfathered by the checked-in list scripts/legacy-task-ids.txt, which only shrinks and is excluded from the line cap as data"
premises:
  - claim: PyYAML is already installed by uv in the Makefile and CI; jsonschema is not yet named anywhere and V1 adds --with jsonschema; both resolve through uv on this host
    command: "grep -n 'with pyyaml\\|jsonschema' Makefile .github/workflows/*.yml; uv run --no-project --with jsonschema --with pyyaml python -c 'import jsonschema, yaml; print(jsonschema.__version__, yaml.__version__)'"
    output: "Makefile:189 and :203 and agent-assets.yml:35 use --with pyyaml; no jsonschema anywhere; 4.26.0 6.0.3"
  - claim: required workflows are organization-only; pull_request_target runs the base branch's workflow file and is eligible as a required status check
    command: "WebFetch docs.github.com available-rules-for-rulesets (enterprise-cloud) and troubleshooting-required-status-checks"
    output: "Ruleset workflows can be configured at the organization or enterprise level; required checks count when triggered by push, pull_request, pull_request_review, pull_request_target, deployment, deployment_status; pull_request_target runs in the context of the default branch of the base repository"
  - claim: codex exec --output-schema is enforced server-side as a strict JSON schema; codex 0.161.0 rejects --full-auto and -a on exec
    command: "codex exec --help; read codex-rs/exec/src/lib.rs and codex-api/src/common.rs at rust-v0.161.0"
    output: "text.format = {type: json_schema, strict: true, schema}; error: unexpected argument '--full-auto' found; approval policy for exec is set with -c approval_policy=never"
  - claim: claude -p --bare requires an API key and skips hooks; without --bare a -p run executes the project's hooks; --json-schema returns structured_output; --max-budget-usd caps spend
    command: "WebFetch code.claude.com/docs/en/headless and cli-reference"
    output: "--bare never reads OAuth credentials or the system keychain; set ANTHROPIC_API_KEY; without --bare -p runs the hooks in a project's .claude/settings.json; the structured output is in the structured_output field; spend can pass the cap, so leave headroom"
  - claim: the vendor's own reset rule is two corrections

**Analyzing task invariant requirements**
**Assessing audit and environment risks**
exec
/bin/zsh -lc "sed -n '81,165p' .orchestration/tasks/dotfiles-T128-regime-v3-a01.md && sed -n '166,241p' .orchestration/tasks/dotfiles-T128-regime-v3-a01.md" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 56ms:
    command: "WebFetch code.claude.com/docs/en/best-practices"
    output: "If you've corrected Claude more than twice on the same issue in one session, the context is cluttered with failed approaches. Run /clear and start fresh with a more specific prompt"
  - claim: the audit was not the wall-clock bottleneck
    command: "stat .orchestration/validation/dotfiles-T119-*-audit-*.md; history.sh dotfiles-conformance (TASK 2026-10-09T21:26Z to ACCEPTANCE 2026-10-10T08:32Z)"
    output: "four audit files written 11:48, 13:55, 15:52, 17:23 local, each run 15-25 minutes, about 1.3 h of an 11.1 h task"
  - claim: both runtimes' Stop hooks are soft signals, not hard stops, so the merge gate is the mandatory point
    command: "WebFetch learn.chatgpt.com/docs/hooks; WebFetch code.claude.com/docs/en/hooks (Stop section)"
    output: "Codex: decision block doesn't reject the turn but injects a continuation prompt; Claude: 8-consecutive-continuation cap that resets each time Claude calls a tool"
  - claim: the seat's session transcript carries per-message token usage on this host
    command: "grep -o '\"usage\":{[^}]*}' ~/.claude/projects/-Users-a0004262-Workspace-dotfiles--claude-worktrees-worker-c/3747b995-3bb1-4c51-8421-4b1e672b442a.jsonl | tail -1; grep -c '\"usage\"' <same file>"
    output: "usage with input_tokens, cache_creation_input_tokens, cache_read_input_tokens, output_tokens; 5168 usage entries (format internal to Claude Code per its docs)"
  - claim: history.sh truncates to 20 rows by default, so counters read the storage facade or pass a limit
    command: "history.sh dotfiles-conformance | wc -l; history.sh dotfiles-conformance --limit 600 | wc -l"
    output: "20; 256 (the whole team history)"
  - claim: "workflow_dispatch runs a workflow only once its file is on the default branch, so regime.yml is merged unlisted, dry-run from main against a closed PR, then listed as required"
    command: "WebFetch docs.github.com events-that-trigger-workflows (workflow_dispatch)"
    output: "This event will only trigger a workflow run if the workflow file exists on the default branch"
  - claim: "bare mode loads skills from the .claude/skills/ folder of a directory named with --add-dir, so the claude fallback must refuse a head that changes .claude/skills/**"
    command: "WebFetch code.claude.com/docs/en/headless (bare mode section)"
    output: "bare mode loads skills from its .claude/skills/ folder (of directories named with --add-dir)"
  - claim: "a permissions.ask rule forces a native prompt even in auto mode, and only the human operator answers a permission prompt, so a command under such a rule runs only on a human answer"
    command: "WebFetch code.claude.com/docs/en/auto-mode-config; home/dot_config/claude/rules/agmsg-orchestration.md (Permissions)"
    output: "permissions.ask rules always force a permission prompt, even in auto mode; Agent-to-agent permission approval is forbidden; only the human operator answers a permission prompt"
  - claim: "GitHub's default Actions policy will block pull_request_target on public repositories from 2026-11-02 unless an applicable event policy explicitly allows it; it runs in evaluate mode now"
    command: "WebFetch docs.github.com/en/actions/reference/security/securely-using-pull_request_target"
    output: "On November 2, 2026, GitHub will enforce the default policy for affected repositories; create or update an applicable Actions event policy that explicitly allows pull_request_target; Currently runs in evaluate mode"

---

# AGMSG-TASK dotfiles-T128-regime-v3-a01 — DESIGN: regime v3, the redesign after the 2026-10-10 halt

Drafted 2026-10-11 (local) by the orchestrator seat `claude-deep-dot` under a recorded bootstrap exception (operator decision 2026-10-11: the orchestrator drafts, a fresh context on the review profile must accept before any implementing task is dispatched). Operator direction (pasted 2026-10-11): when substantive findings repeat, the design, implementation or verification is wrong and a mechanism must force the redo; prose alone repeats the mistake; the auditor must be able to find the orchestrator's and the worker's mistakes; efficiency, quality and cost are optimised together; the auditor must not become the bottleneck and the audit stages must be chosen; all of it grounded in the tools' official documentation and current practice. Research inputs: fact sheets on Claude Code 2.1.293, Codex CLI 0.161.0, GitHub rulesets and Actions, and the research literature, read 2026-10-11; the measured baseline below.

## 1. Finding: the fix program tripped its own rule

By T126 INV-6 as written: wave 1 (PR #313) 8 amendments (limit 4) and 2 revises (limit 2); wave 3b (PR #314) Bot P1 on two post-RESULT heads. The orchestrator was drafting a waiver for #313. T120 was reset only on the operator's question. The regime is therefore reset here by its own rule; this document is the redesign, and T126 and T124 are superseded (their accepted ideas are kept where named).

Measured baseline (history + GitHub):

| task | PR | files | +lines | amendments | questions | revises | audits (incorrect) | Bot threads (heads) | P0/P1 | wall |
|---|---|---|---|---|---|---|---|---|---|---|
| T114 | - | - | - | 0 | 0 | 6 | 3 (3) | - | - | 21.5h |
| T118 | 310 | 35 | 881 | 7 | 0 | 20 | 8 (7) | 16 (7) | 0 | 10.6h |
| T119 | 312 | 37 | 3191 | 8 | 8 | 5 | 4 (4) | 25 (11) | 7 | 11.1h |
| T120 | 315 | 19 | 1489 | 8 | 1 | 0 | 0 | 15 (5) | 8 | reset |
| T124 W1 | 313 | 20 | 2642 | 8 | 6 | 2 | 0 | 52 (10) | 31 | halted, reset |
| T124 W3b | 314 | 9 | 1462 | 5 | 0 | 0 | 0 | 24 (4) | 2 | halted, reset |

Every acceptance record to date says `cost: n/a`.

## 2. Root causes, each with its evidence

R1 to R8 in the front matter. The literature behind R1: intrinsic self-correction without an external signal degrades after the first round (Huang et al. 2023); a second review round on the same artifact raised recall slightly and false positives by 62% (arXiv 2603.16244); multi-round review degrades with rounds (MCR-Bench); revising an already-correct state loses correct work unless verifier evidence is bound to the exact code state (arXiv 2607.24604). Behind R3: Google's review study (median change 24 lines, ~90% under 10 files) and its CL-size guidance. Behind R5 and R6: a judge without a reference is lenient and a reference flips 9-85% of verdicts toward correct (2607.12885); format-restricted generation degrades reasoning, so verdicts reason first and then fill the schema (2408.02442); Anthropic's harness-design post: a standalone skeptical evaluator is tractable where a self-critical generator is not, and the evaluator is worth its cost only where the task exceeds the model's reliable solo capability, which is what the tier table encodes.

## 3. Principles (each names what it reuses and what it deletes)

- **P1 One deterministic fact per round (INV-3).** Reuses tests/unit, CI, `pr-feedback.py`. Deletes free-form revise rounds and the audit-per-round habit.
- **P2 Declarative over imperative at trust boundaries (INV-1, INV-5, INV-7).** Reuses `jsonschema`, PyYAML, `codex exec --output-schema`, `claude -p --json-schema`. Deletes the bespoke YAML parser, the glob NFA, the prose verdict grammar, regex parsing of `.last.md`, and the T126 "process_tiers.json next to the module" indirection (the validator reads the manifest with PyYAML).
- **P3 Small one-invariant PRs enforced in CI (INV-2).** Reuses GitHub required checks and the strict up-to-date ruleset already in force. Deletes waves declared inside a task file.
- **P4 Main-pinned mechanical checks in CI; host gate only for history-anchored rules (INV-1, INV-2, INV-8 in CI; INV-3, INV-5 record, INV-6, INV-7 anchor, INV-11 on the host).** Reuses `pull_request_target`, the `changes` job pattern that reports success for an `.orchestration`-only diff. Deletes PR #313's `REVIEW_TREE` idea (never on `main`) and the copy step of untracked evidence into the gate's cwd. The host gate `make require-crit-review` keeps its evidence rules and changes three of them in named waves: the audit verdict and categories come from the schema JSON with the `AGMSG-AUDIT` record and the category lock (V2b), the reset backstop and the Bot-head count (V3a), the history-anchored design review (V4); it continues to run from the orchestrator's main checkout.
- **P5 Research before dispatch; a question ends the task, not amends it (INV-4).** Reuses history (`amendment=`, `status=question`). Deletes the amendment-per-question practice. The task file's `premises` block is the mechanical residue of "verify every CLI constraint by running the real command".
- **P6 Reset is mechanical, loop-time, and released only by another context or the operator (INV-6).** Reuses `scripts/require-crit-review.py` as the mandatory point, `agent-stop-gate.sh` and the Codex `[hooks].Stop` as the early signal (both soft by their documented caps: Claude's 8-continuation cap, Codex's continuation prompt), `check-regime-boundary.sh` for the re-dispatch detector. Deletes the orchestrator-written redesign (the redesign author is a `review`-profile seat or a fresh headless context; the `redesign` profile of T124 v4 is dropped: `review` is the same model and effort as `deep`, so independence of context is the whole lever, and T124 round 1 showed it works).
- **P7 Audit staging by tier; the auditor never serializes the pipeline (INV-5, process_tiers).** See section 4.
- **P8 Cost measured, budgets per tier (INV-9).** Reuses the JSON cost fields the runtimes already emit and the session transcripts. Deletes `cost: n/a`.
- **P9 Parallelism with disjoint files and early push (INV-10).** Reuses `herdr-agents --add-worker`, draft PRs.
- **P10 Routing stays by boundary.** Claude-boundary sources to a Codex seat, Codex-boundary to a Claude seat, permgate and shared gate sources to the operator, as the agmsg-orchestration skill's step 3 states; nothing here changes that.

## 4. Audit stages (process_tiers; the one table the validator reads)

| stage | who | when | tier docs | tier review | tier design | cost |
|---|---|---|---|---|---|---|
| 0 design review | a fresh Claude context on the review profile and a Codex read-only review of the same hash, schema receipts (INV-7) | before any code | - | - | required | minutes |
| 1 worker checks | worker in its sandbox: invariant tests first, shellcheck, unit tests | before every push | required | required | required | none for the regime |
| 2 CI + Bot | main-pinned `regime` check (schema, caps, evidence shape) + unit tests + Codex Bot | every push, in parallel | required | required | required | none |
| 3 schema audit | headless read-only `codex exec --output-schema`, pooled 2, started by `make audit-head` once CI is green and the Bot reviewed or 15 min passed, once per RESULT head, reused for an evidence-only head by tree equality (INV-5) | per RESULT head | - | required | required, with invariant map and permgate window | the scarce resource, now off the critical path |
| 4 acceptance | orchestrator: sweep, dispositions, record, host gate, merge `--match-head-commit` | per RESULT | required | required | required | minutes |

Tier derivation: docs = prose-only `allowed_files` outside the regime's own rule prose (`home/dot_config/claude/rules/**`, the agmsg-orchestration SKILL, `AGENTS.md`, README), which is review tier by explicit list; review = the existing review-tier paths (scripts, hooks, tests, templates); design = the explicit design-tier list from T124 INV-2 v3 (install/**, setup.sh, the gate scripts, `executable_herdr-agents`, `executable_permgate`, Codex and Claude policy, sandbox and permission settings, credential helpers). Round limits: docs 1 revise; review and design 2 revises then reset. Profiles: worker `standard` (docs `express`), review `review`, audit `audit`.

Why stage 3 is not the queue: the orchestrator starts it with `make audit-head` when the RESULT arrives (the wait on CI and the Bot is inside the target), it runs concurrently (pool of two, each in its own detached worktree), once per head, and an evidence-only head reuses the earlier audit by tree equality; the measured cost of the old serial form was 1.3 h of 11.1 h, so the throughput levers are P1 and P6, and the pool removes the residual queue.

## 5. Enforcement map

| invariant | enforcement point |
|---|---|
| INV-1 | `.github/workflows/regime.yml` (`pull_request_target`, required check `regime`: validates `.orchestration/<task id>/task.md` from the PR head read as data, refuses workflow edits outside a design-tier task; an explicit Actions event policy allowing `pull_request_target` is set by the operator before 2026-11-02, named in V1c's acceptance record), `scripts/validate-task.py` (schema + PyYAML, about 80 lines), `schemas/task.json`, `scripts/lib/high_risk_paths.py` (new module: tier lists and `tier_of`), `scripts/legacy-task-ids.txt` (grandfather list), `process_tiers` in the manifest; host gate compares the copy's sha256 with `task_sha256=` in history (V3a); stage waivers by `scripts/regime-waive.sh` under its `permissions.ask` rule, written outside the sandbox write roots (V3a) |
| INV-2 | `regime.yml` step with `scripts/pr-caps.sh` and the task.md invariant-id comparison against the design's `implementing_tasks` |
| INV-3 | `regime-check.sh` step: the test selector named in `.orchestration/<task id>/revise.yaml` (sibling of the byte-identical task.md) exists on the head and its file differs between `previous_head` and the head; a `revise-check` job in `test.yaml` (PR context, required) runs exactly that selector on both heads; the host gate's `previous_head` history check and validation-file line are V2b's |
| INV-4 | `scripts/validate-task.py` (premises required for code and design tasks); `agent-stop-gate.sh` early signal on the second AGMSG-TASK or second PONG question; the merge backstop is INV-6's |
| INV-5 | `schemas/audit.json` (findings and invariant map before verdict), `scripts/audit-head.sh` (about 100 lines: detached worktree, `codex exec`, fallback, sha256 to history under the audit identity, `.last.md` render; PR #314's hardening kept), `make audit-head` target around `gh pr checks --watch` and the SKILL's Bot list loop with its 15-minute `bot: none` rule (no daemon), `AGENTS.md` Audit section; gate: JSON verdict and categories, `AGMSG-AUDIT` lookup, category lock, tree-equality acceptance of an earlier head (V2b) |
| INV-6 | `scripts/require-crit-review.py` (mandatory: history counts, Bot heads from `original_commit_id` recorded by `scripts/pr-feedback.py`, audit heads from the main checkout's audit JSONs whose sha256 matches their `AGMSG-AUDIT` record, reset record or a `scripts/regime-waive.sh` waiver), `scripts/agent-stop-gate.sh` and the manifest's `codex.hooks` Stop entry (early signal, history counts only, within the 3 s history budget), `scripts/check-regime-boundary.sh` (closed-unmerged PR without a reset record; over-count task without an accepted or reset record; waiver listing) |
| INV-7 | `scripts/design-review.sh` + `schemas/design-review.json`: two headless runs per design hash, `claude -p` under `claude-review-dot-hNNN` and `codex exec --sandbox read-only` under `codex-review-dot-hNNN`, each joining for the run and sending its RESULT; gate: both RESULTs precede the implementing TASK, both hashes recomputed, whole-file form accepted for pre-V4 receipts |
| INV-8 | worker writes under `.orchestration/<task id>/` on the branch (task.md copy first); `regime.yml` validates the evidence JSON shapes; the gate's existing path rules keep the orchestrator's records under `validation/` and `acceptance/` |
| INV-9 | `scripts/accept-task.py` (sweep, dispositions scaffold, record rows, gate invocation, merge command, cost fields), budgets in `process_tiers`, `check-regime-boundary.sh` warning |
| INV-10 | `scripts/check-regime-boundary.sh` and `scripts/accept-task.py` from `history.sh` timestamps (storage facade or `--limit`, never the 20-row default), the draft PR's `created_at` from `gh api pulls/<n>`, and the task's `after` list against acceptance records |
| INV-11 | `executable_permgate` (operator-routed, Codex security review) + gate cross-check |
| INV-12 | one test module per script; `make unit-test` in CI; the `main-tests` required job (V0): main's test modules for every script outside the PR's `allowed_files`, deciding inside its own job; the trusted-root audit reads the test diff beside the code diff for scripts inside it; the auditor checks per PR that no new hand-written parser sits at a trust boundary (a `conformance` finding) |
| prose | SKILL, `agmsg-orchestration.md`, `pr-integration.md`, `crit-review.md`, `model-selection.md`, README: each wave edits only the sections it implements |

## 6. Waves (one PR, one invariant, within INV-2's caps; each task file reviewed by a fresh context before dispatch)

- **V0** INV-12: the `main-tests` required job in `test.yaml` (main's `tests/unit` modules of every script outside the PR's `allowed_files`, run in the PR's context, deciding inside the job as the A5 workflows do) and the protocol in the Worker Playbook; lands before every other wave as `dotfiles-T128-v0-main-tests-a02` (A301; PR #317 and the audit of `adcf783b` are its input). Claude seat; design tier (workflow); the operator lists the check at its acceptance.
- **V1** INV-1, validation only (operator direction 2026-10-11, relayed through the review seat; also the cap: the undivided V1 sat at 500 added lines): `schemas/task.json`, `scripts/validate-task.py`, `scripts/lib/high_risk_paths.py`, `scripts/legacy-task-ids.txt` (from PR #313; data, excluded from the line cap), `tests/unit/test_validate_task.py`. Claude seat. Design tier: this review is its stage 0. Precondition: this design is on `main` through a boundary PR before V1's TASK is dispatched.
- **V1c** INV-1, the CI check (after V1): `scripts/regime-check.sh`, `.github/workflows/regime.yml` (task.md validation, workflow-edit refusal, `workflow_dispatch` dry run), `tests/unit/test_regime_check.py`, `process_tiers` in the manifest, SKILL step 3 paragraph, README sentence. Claude seat. Acceptance names the operator action that lists `regime` as a required check, after the dry run from `main` against a closed PR. Two tasks map to INV-1 as V2 and V2b map to INV-5.
- **V1b** INV-2 (after V1c): `scripts/pr-caps.sh`, the caps and invariant-id steps in `regime-check.sh`, tests, one SKILL sentence.
- **V2** INV-5 runner: `schemas/audit.json` (PR #314's, reordered), `scripts/audit-head.sh` with PR #314's hardening, `make audit-head`, `AGENTS.md` Audit section, tests, the SKILL's task-level audit bullet. Claude seat.
- **V2b** INV-5 gate: `scripts/require-crit-review.py` reads the JSON verdict and categories, requires the `AGMSG-AUDIT` record, locks orchestration and conformance at P0-P2 to waiver or reset, accepts an earlier audited head by tree equality, and requires the INV-3 `check=` line in the validation file; tests. Operator-routed gate source (delegable to a Claude seat with recorded opt-in).
- **A3** INV-6 (plan 006 Phase A, `dotfiles-T128-regime-counters-a01`): `scripts/regime-counters.sh` computes every INV-6 count from history and GitHub and prints the thresholds reached; `check-regime-boundary.sh` reports a reached threshold without a reset record or waiver; the orchestrator runs it before every acceptance action. V3a wires that script into the hook and the gate.
- **V3a** INV-6: `scripts/pr-feedback.py` (`original_commit_id` on review_comment items), `require-crit-review.py` reset backstop and `task_sha256` comparison, `agent-stop-gate.sh` history counts (revises, amendments, questions) as the early signal, the Codex Stop entry in the manifest and its rendered template, `scripts/regime-waive.sh` with its `permissions.ask` rule in the manifest's Claude permissions block (no permgate policy entry), `check-regime-boundary.sh` detector and waiver listing; tests. Four boundaries in one PR (gate source, Claude hook and permission source, Codex hook source): an operator PR by construction, reviewed by a Codex `security`-profile seat before acceptance.
- **V3b** INV-4: premises in the schema and validator, SKILL text (questions end the task; one answering TASK at most). Claude seat; no hook source (the counting is V3a's).
- **V3c** INV-3: `check=` and `previous_head=` in the ACCEPTANCE contract (SKILL), `revise.yaml` beside task.md in the Worker Playbook, the `regime-check.sh` step, the `revise-check` job in `test.yaml`; tests. Claude seat (no gate source: the history check and validation-file line are V2b's).
- **V3d** INV-10: idle and first-push computations in `check-regime-boundary.sh` and `accept-task.py` (the latter lands in V5b; V3d adds them to the boundary check only). Claude seat.
- **V4** INV-7: `scripts/design-review.sh` (Claude and Codex runs under their `-review-dot-hNNN` identities), `schemas/design-review.json`, the history anchor and hash check in the gate (two RESULTs, both forms), SKILL paragraph. Operator-routed for the gate part.
- **V5a** INV-8: `.orchestration/<task id>/` paths in the Worker Playbook, task.md copy as the first commit, evidence-shape validation in `regime.yml`, boundary commit reduced to orchestrator records. Claude seat.
- **V5b** INV-9: `scripts/accept-task.py`, cost fields with source digests, budgets in `process_tiers`, `check-regime-boundary.sh` budget warning. Claude seat. Size: the sweep, scaffold and gate invocation already exist as commands; the script sequences them, about 200 lines.
- **V6** INV-11: `executable_permgate` session_id and cwd; gate cross-check. Operator-routed, Codex `security` profile review.

Order: V0, then the design-tier code waves V1, V1c, V1b, V2, V2b, V3a, V3b, V3c, V3d, V4, V5a, V5b, V6, one PR each. File-disjoint pairs may run concurrently (V1 with V2; V3b with V3d); the gate-source waves (V2b, V3a, V4's gate part) run serially.

## 7. Thresholds (operator confirmed 2026-10-11)

revise 2; amendments 2; questions 2; Bot P0/P1 heads 2 (post-RESULT); audit implementation or specification P0-P1 heads 2; PR 15 changed files (the file count excludes `.orchestration/` only) and 500 added lines outside `tests/`, `.orchestration/` and the data list `scripts/legacy-task-ids.txt`; first push 30 minutes; idle 20 minutes; workers 3; audit pool 2; audit once per head; docs tier 1 revise.

## 8. Disposition of the halted work

PR #313 and #314 closed unmerged as reference branches (reset records in `.orchestration/acceptance/…-design-reset.md`); PR #315 is a draft per T120's reset record; the four worker seats are removed. Salvaged: the format-2 key set, the tier table, `scripts/legacy-task-ids.txt` and the test ideas of `tests/unit/test_validate_task.py` (V1); `scripts/schemas/audit.json`, the AGENTS.md Audit text, the pre-push hardening and the `AGMSG-AUDIT` record (V2). Dropped with the `redesign` profile: PR #313's `home/dot_codex/modify_private_redesign.config.toml`. T127 (T120's redesign) follows V1 under this regime.

## 9. Residuals, stated

- Workers' conduct is checked mechanically only for Claude seats and only after V6; until then the sandbox record is self-reported.
- `pull_request_target` runs with the base repository's token on a public repository: the `regime` job reads PR files as data with `contents: read` only, checks out `main`'s scripts, and never executes anything from the PR; a change to `.github/workflows/regime.yml` itself is a design-tier change under INV-1.
- A repository admin can edit the ruleset; that path is visible on GitHub, not prevented, consistent with the waiver anchor.
- Operator authentication does not exist on this machine: every seat runs as the one user and every GitHub action as the one account, so no record can prove that the operator rather than the orchestrator wrote it. The regime therefore makes every waiver pass through a native permission prompt (`permissions.ask`, which no classifier, hook or agent may answer) and makes every waiver visible in three places; it does not claim more. The Codex design review of round 7 asked for authenticated operator events; this is the honest limit of what the machine offers.
- The design-review receipt's anchor in history is only as strong as the `-review-` identity's independence; a fresh headless context per review (V4) is the mitigation, and until V4 lands a seated `review`-profile identity reviews.
- GitHub's default Actions policy blocks `pull_request_target` on public repositories from 2026-11-02 (evaluate mode today); the operator sets an explicit event policy allowing it before then, or the `regime` job loses its main-pinned form and the host gate becomes the only gate again. Named in V1c's acceptance record.
- The `regime` job runs `main`'s workflow file, so a change to `regime.yml` is never exercised by its own PR; its logic therefore lives in scripts with unit tests, and a `workflow_dispatch` dry run precedes listing it as required.
- `regime.yml` discipline, stated once: `main` stays at the workspace root (`actions/checkout` default ref under `pull_request_target`); the PR head is fetched as data and read with `git show <head sha>:<path>` into a directory never on `PATH`; the diff range is the merge-base of `github.event.pull_request.head.sha` with `main`, never `github.sha`; `uv run --no-project`; `yaml.safe_load`; no `make`, no script, no dependency file from the PR tree; `permissions: contents: read`; no secrets.
- The seven existing required checks still run on `pull_request` from the PR's own workflow files; INV-1's workflow-edit refusal in the `regime` job is what closes R8 for them.
- Bootstrap: this design was written by the orchestrator that dispatched the abandoned tasks. The reset records carry the operator's waiver form (`DESIGN_RESET_WAIVED_BY=operator`, decision 2026-10-11), this review is the only release, and no further orchestrator-authored design follows under T128; T127 (T120's redesign) is written by another context.

## 10. Design review (round 15 requested: plan 006 A102, second pair)

Round 1 (`.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review.md`, `claude-review-dot-a001`, 2026-10-10T21:15Z, verdict `revise`): INV-7, INV-8, INV-11, INV-12 accepted with notes; INV-1, 2, 3, 4, 5, 6, 9, 10 rejected with corrections; findings F1-F9. v2 adopts every item: the task.md copy and `task_sha256` anchor (F1), the per-task invariant-set rule and the workflow-edit refusal (F2), the gate changes assigned to V2b/V3a/V4 with the category lock, the Bot-wait timeout and the tree-equality rule (F3), the merge backstop as the mandatory point, `original_commit_id`, the audit-JSON source, the Stop-hook budget split and the boundary detector (F4), the single amendment count over every TASK (F5), INV-9/INV-10 moved out of the Stop hook (F6), the reset records corrected to `claude-review-dot-a001` with the waiver form and the thread ids (F7), rule prose in the review tier (F8), premise 1 restated and three premises added (F9); plus the Q5 salvage list, the `make audit-head` target in place of a daemon, the `regime.yml` discipline and the hash note.

Round 2 (`…-design-review-round2.md`, 21:29Z, verdict `revise`): every round-1 correction confirmed applied; INV-2, INV-3, INV-6 rejected for contradictions v2 introduced, plus routing, cap and premise notes. v3 adopts all of them: `implementing_tasks` is a map of task id to invariant ids inside the hashed keys and the design-on-main precondition is stated (INV-2); `revise.yaml` is a sibling of the byte-identical task.md (INV-3, INV-8, INV-12, V3c, V2b); the question threshold is 2 and audit JSONs count only when their sha256 matches their record (INV-6); V3a is an operator PR with all hook counting, V3b has no hook source, V3c no gate source; the legacy list is excluded from the line cap as data; the `workflow_dispatch` premise is added; the stage-3 sentence names the orchestrator's `make audit-head`; INV-1 names the latest TASK's token and the recommit after each amendment. Round 3 (`…-design-review-round3.md`, 21:33Z, verdict `accept`) confirmed the five edits; its two notes are carried in the acceptance record. v4 (operator direction 2026-10-11, relayed by the review seat's PONG at 22:01Z) splits V1 by responsibility into V1 (validation only) and V1c (the CI check), adds `dotfiles-T128-v1c-regime-ci-check-a01: [INV-1]` to `implementing_tasks` (a hashed key, hence this round), reorders the waves (V1, V1c, V1b, …) and aligns section 7's cap wording with INV-2. Round 4 (`…-design-review-round4.md`, 22:06Z, verdict `accept`) confirmed the split; its note (INV-1's ruleset action is V1c's acceptance record) is carried. v5 answers the Codex Bot's finding on boundary PR #316 (thread 4239305441): INV-3's `ci:<job>` form had no enforcement, so `check=` is now a test selector or a `repro:<id>` whose command and output live in revise.yaml, each with its own regime-job verification. Round 5 (`…-design-review-round5.md`, 22:12Z, verdict `accept`) confirmed it. The Codex Bot then reviewed the second boundary head (c1e2582b) and raised six P1 and four P2 findings that three same-vendor accepts had not: the auditor read the schema and AGENTS.md from the audited head (INV-5 now runs from main as the instruction root with the worktree as data), the CI job had no previous RESULT head (INV-3 now records previous_head in the ACCEPTANCE and revise.yaml, cross-checked by the host gate), ids were compared without sentences (INV-2), `allowed_files: ['*']` derived a cheap tier and a branch copy could claim a legacy id (INV-1, INV-12), and two task records pointed at an abandoned prerequisite. v6 adopts all ten and, because a cross-vendor reviewer found what a same-vendor fresh context did not, INV-7 now requires both a Claude and a Codex review of each design hash. Round 6 (`…-design-review-round6.md`, 22:28Z, verdict `revise`) accepted INV-1, 2, 3, 5, 12 and rejected INV-7: the Bot form produced no receipt, hash or RESULT, so it would have been an orchestrator-written receipt for a review it did not perform (R5). v7 makes the Codex review a `codex exec --sandbox read-only` run under a `codex-review` identity with its own receipt and RESULT, names it in the enforcement row and V4, keeps the Bot's review as swept feedback, and adds the bare-mode skills premise (round-6 INV-5 note, acted on in V2). Round 7 (Claude, 22:31Z, `accept`) confirmed INV-7. The first Codex review (`…-design-review-round7-codex.md`, `codex-review-dot-h001`, 22:34Z, `reject`) rejected INV-1, 3, 4, 5, 6, 9, 10, 12, all on one theme: evidence the orchestrator authors. v8 answers each: the waiver becomes a command under a `permissions.ask` rule (INV-1, INV-6) with the one-account residual stated in section 9; `repro:` is dropped and `check=` is a test selector only (INV-3); premises are reviewer and auditor evidence and the counting is the mechanical part (INV-4); the audit carries an input manifest and the acceptance record has an audit-input boundary (INV-5); cost records name their raw sources and stay a warning metric (INV-9); first push is the first commit's committer date and dispatchability is defined (INV-10); the independent oracle for gate-script PRs is the trusted-root audit (INV-12). The Codex P2 on the bare-mode skills premise is not adopted: the headless page says verbatim that "A directory you name with --add-dir is a partial exception: bare mode loads skills from its .claude/skills/ folder". Codex round 8 (`…-design-review-round8-codex.md`, 22:39Z, `reject`) accepted INV-1, 6, 7, 8, 9, 11 and the one-account residual, withdrew its bare-mode P2, and rejected INV-2 (tests unbounded), INV-3 (a changed file is not a run selector), INV-4 (sampling), INV-5 (the skills refusal was a premise, not a rule), INV-10 (committer date is not a push time; dependencies), INV-12 (a model audit is not a deterministic oracle), plus two stale enforcement rows. v9 adopts all: a 1000-line cap under tests/; the exact selector run on both heads in the PR's required `revise-check` job; every premise dispositioned by each reviewer and the auditor; the `.claude/**` refusal inside INV-5; the draft PR's `created_at` and an `after` list for dispatchability; a `main-tests` required job running main's tests against the PR's scripts (V5c); the two rows fixed. Claude round 8 (`…-design-review-round8.md`, 22:41Z, `revise`) rejected INV-1 (the waive script had no owner or row), INV-5 (once-per-head versus re-audit on a stale manifest) and INV-10 (fixed in v9), and offered a stronger anchor: the waiver record in a directory outside the sandbox write roots. Codex round 9 (`…-design-review-round9-codex.md`, 22:46Z, `reject`) accepted ten, rejected INV-5 (the `.claude/**` refusal that v9 claimed was silently lost by a failed edit, confirmed by grep) and INV-12 (the oracle must precede the waves), dispositioned all twelve premises (nine hold, three unverifiable in its read-only sandbox), and raised GitHub's 2026-11-02 `pull_request_target` policy. v10: the refusal is in INV-5 and verified by grep; one valid audit per head with stale-manifest replacement; the runner computes the manifest; the waiver record lives outside the sandbox write roots and V3a owns the script (map entry `[INV-6, INV-1]`); `main-tests` is wave V0 and every code wave is contract-first (INV-12, INV-2); the policy premise and residual. Claude round 9 (`…-design-review-round9.md`, 22:46Z, `revise`) found that `main-tests` as drafted would fail every intentional change and proposed running main's modules only for scripts outside `allowed_files`; Codex round 10 (`…-design-review-round10-codex.md`, 22:50Z, `reject`) accepted INV-1..11 and found that contract-first tests cannot merge ahead of an implementation that changes an existing script, proposing dormant contracts that `main-tests` activates on the implementation PR. v11's INV-12 is the union: main's modules as they are for undeclared scripts, main's dormant contracts (`REGIME_CONTRACT=1`) for declared ones, contract PRs required for design-tier waves; INV-1 states that the record's location is the guard and the ask rule the second layer (Claude round 9). Codex round 11 (`…-design-review-round11-codex.md`, 22:52Z) accepted INV-1..12 with no findings. Claude round 11 (`…-design-review-round11.md`, 22:54Z, `revise`) accepted everything but two INV-12 clauses: contracts must not stay dormant forever (the implementation PR removes the decorator; main-tests judges it against main's dormant copy) and an empty contract must fail a design-tier implementation PR. v12 adds both sentences to INV-12 and V0. Claude round 12 (`…-design-review-round12.md`, 22:57Z) accepted v12; Codex round 12 (`…-design-review-round12-codex.md`, 22:57Z, `revise`) accepted INV-1..11 and asked for a failing check behind the decorator-removal clause. v13 adds it to INV-12 (main-tests fails an implementation PR whose declared test module still carries a contract marker) and V0 carries it with the task-file reviewer's three V0 items (main's tests overlaid on a copy of the PR tree, module selection from the task's declared tests/ entries, task.md read with PyYAML). Round 13 (Claude 23:01Z, Codex 23:01Z and the premise map 23:17Z) accepted v13. Plan 006 (approved 2026-10-11) A102 amends two hashed keys: INV-12 states the in-process oracle's authenticated completion (nonce runner) and its residual, after the Codex Bot's P1 on V0's round-1 head repeated the class of the round-0 audit's finding 3; INV-2 and the map gain the .orchestration-only CI skip (`dotfiles-T128-ci-skip-orchestration-a01`, plan A201) that plan 006 orders as Phase 2. Round 14 (Codex 02:42Z `accept`; Claude 02:43Z `revise`): INV-12's residual clause understated the gap (the nonce authenticates the writer, not the counts; in-process patching of unittest's result collection forges counts with a genuine nonce) and INV-2 should cover every required check. v15 states the residual as it is, adds the runner's pinning of unittest classes, and words INV-2 for every required workflow. Round 15 asks both reviewers at once for one verdict each on this hash. Sources are the repository paths under `.orchestration/validation/dotfiles-T128-regime-v3-a01-research/` (`baseline.md`, `practice-evidence.md`, `claude-code-factsheet.md`, `codex-factsheet.md`, `github-factsheet.md`, `method-draft.md`). Receipt: `.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round15.md` (Claude) and `…-design-review-round15-codex.md` (Codex); the whole-file sha256 of this file in both headers.

v18 (plan 006 B0, plan 007 T701; written by the orchestrator under the records exemption, 2026-10-12): INV-12 narrowed to the undeclared-change regression guard: `main-tests` runs main's test module of every script outside `allowed_files`; a script inside `allowed_files` is judged by the PR's tests, the diff review and the trusted-root audit; the dormant-contract clauses, `REGIME_CONTRACT` and the `<task>-contract-a01` PRs are removed (A302 withdrew V1's contract PR under the Phase A correction and no wave has used one); `main-tests` decides inside its own job as the A5 workflows do. INV-2 loses the dead `-contract-a01` comparison and names A5's in-job form. `implementing_tasks` gains the V0 successor `dotfiles-T128-v0-main-tests-a02: [INV-12]` (A301) and `dotfiles-T128-gate-evidence-a01: [INV-6]` (plan 007 T702: the gate's `evidence=` grammar and the S6 refusal at INV-6's mandatory point). The INV-12 enforcement row, the V0 wave row and the wave order follow. Round 20 asks both reviewers at once for one verdict each on this hash: receipts `.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round20.md` (Claude) and `…-design-review-round20-codex.md` (Codex); the whole-file sha256 of this file in both headers.

v19 (round 20's one revision, 11:43Z): INV-6 gains the clause the Claude round-20 receipt asked for (the Codex round-20 receipt accepted v18 with no rejection), so `dotfiles-T128-gate-evidence-a01: [INV-6]` maps to a sentence that states the two refusals; nothing else changes. Round 21 asks both reviewers at once for one verdict each on this hash: receipts `…-design-review-round21.md` (Claude) and `…-design-review-round21-codex.md` (Codex).

v20 (11:46Z): the Codex round-21 receipt found the v19 clause appended to INV-4 (a stale line number after v18's two map insertions), so v20 moves that exact clause to the end of INV-6; INV-4 returns to its v18 text; nothing else changes. Round 22 asks both reviewers at once for one verdict each on this hash (round 21 was never sent to the Claude seat): receipts `…-design-review-round22.md` (Claude) and `…-design-review-round22-codex.md` (Codex).

Round 22 (Claude 11:49:16Z `accept`, receipt `…-design-review-round22.md`; Codex 11:49:21Z `accept`, `…-design-review-round22-codex.md`) accepted v20 at `ed51f1d4…`; the unhashed `design_review.receipt` line now names the round-22 receipt (this edit), confirmed by a Codex pointer-only read as round 23.

v21 (13:08Z, the orchestrator under the records exemption): `implementing_tasks` gains `dotfiles-T128-gate-evidence-a02: [INV-6]`, the INV-6 successor of `dotfiles-T128-gate-evidence-a01` (withdrawn 13:02Z under INV-6 before its second amendment; reset record `dotfiles-T128-gate-evidence-a01-design-reset.md`), beside the a01 entry that stays as parked history, as the V0 and round-18 successors did; nothing else changes. Round 24 asks both reviewers at once for one verdict each on this hash: receipts `…-design-review-round24.md` (Claude) and `…-design-review-round24-codex.md` (Codex).

v22 (15:28Z, the orchestrator under the records exemption): `implementing_tasks` gains `dotfiles-T128-gate-evidence-a03: [INV-6]`, the INV-6 successor of a02 (withdrawn 15:25Z after its second S1 cycle; plan 011 option F: the acceptance record's machine-read parts as YAML front matter), beside the a01 and a02 entries kept as parked history; nothing else changes. Round 25 asks both reviewers at once for one verdict each on this hash: receipts `…-design-review-round25.md` (Claude) and `…-design-review-round25-codex.md` (Codex).

v23 (2026-10-13 02:55Z, the orchestrator under the records exemption): `implementing_tasks` gains `dotfiles-T128-gate-evidence-a04: [INV-6]`, the INV-6 successor of a03 (withdrawn 02:3xZ after the fourth binding row; plan 014 option A: the acceptance record's `ledger` must cover every swept Codex finding id and every audit finding `audit:<sha7>:<n>`, a set difference the gate computes; the a04 file's hash is in the reset record `dotfiles-T128-gate-evidence-a03-design-reset.md`, not here), beside the a01 to a03 entries kept as parked history; nothing else changes. Round 26 asks both reviewers at once for one verdict each on this hash: receipts `…-design-review-round26.md` (Claude) and `…-design-review-round26-codex.md` (Codex).

v24 (2026-10-13 03:05Z, the orchestrator under the records exemption): the v23 line named the a04 file's hash, which moved when round 26's Codex half found the coverage sentence omitted badged Codex review bodies (a04 round 4 after round 3; no a04 hash appears in this design, the reset record `dotfiles-T128-gate-evidence-a03-design-reset.md` is the sole anchor, so later a04 rounds do not move the design); the map entry `dotfiles-T128-gate-evidence-a04: [INV-6]` is unchanged; nothing else changes. Rounds 27 and 28 ask both reviewers at once for one verdict each on this hash: receipts `…-design-review-round28.md` (Claude) and `…-design-review-round28-codex.md` (Codex); round 27's Codex half found the two hash mentions this text removed.

**Focusing on validation step**
exec
/bin/zsh -lc "nl -ba .orchestration/validation/dotfiles-T128-chain-review-scripts-a01.md | sed -n '1,210p'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 0ms:
     1	---
     2	task_id: dotfiles-T128-chain-review-scripts-a01
     3	seat: claude-standard-dot-a002
     4	code_commit: 1f307a6e
     5	---
     6	
     7	# Validation: dotfiles-T128-chain-review-scripts-a01
     8	
     9	Every command in §1 to §8 ran from the worktree `.claude/worktrees/worker-f`, inside the sandbox; §9's ran outside it, and `scratchpad/` there names the session scratchpad. `MAIN` names the main checkout, `IN` the task's input directory there, and `S` a scratch directory under `/tmp/claude-501`. `UV_OFFLINE=1` was set, since uv cannot reach pypi from the sandbox. The output is verbatim, with the main checkout's path removed, and each block ends with the command's exit status. §1 to §8 were captured at `1f307a6e`, before the PR was opened, and §9 after the Bot's review of `0da6be3e`.
    10	
    11	The whole unit suite, `make unit-test`'s `uv run python -m unittest discover -s tests/unit`, ran once in the sandbox and ended with `Ran 1082 tests in 471.510s` and `FAILED (failures=168, errors=103, skipped=2)`. No `origin/main` baseline was taken in the sandbox, so that run is evidence neither way; CI's `make unit-test` on the PR is. §7 runs the modules that exercise `scripts/orchestrator/`, and they all pass.
    12	
    13	## 1. Task file and task copy
    14	
    15	```console
    16	$ shasum -a 256 "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md"; cmp "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md" && echo byte-identical
    17	db9ff03a5eb720a4778fc357fb351926e7ecbb1d5af7a5f6cf11266232ba060b  .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01.md
    18	db9ff03a5eb720a4778fc357fb351926e7ecbb1d5af7a5f6cf11266232ba060b  .orchestration/dotfiles-T128-chain-review-scripts-a01/task.md
    19	byte-identical
    20	[exit 0]
    21	```
    22	
    23	## 2. Branch, the premise and the inputs
    24	
    25	```console
    26	$ git log --oneline origin/main..HEAD; git rev-parse origin/main
    27	1f307a6e feat(orchestrator): local-review.sh, local-advisory.sh and sandbox-scan.sh land with their tests (T128 chain-review-scripts a01)
    28	5ec860520075a2f0bbb551232de0f868e481a59c
    29	[exit 0]
    30	```
    31	```console
    32	$ git ls-tree --name-only origin/main scripts/orchestrator/ | /usr/bin/grep -c -E "local-review|local-advisory|sandbox-scan" || true
    33	0
    34	[exit 0]
    35	```
    36	```console
    37	$ cd "$IN" && shasum -a 256 *.sh | sed -E "s/^([0-9a-f]{16})[0-9a-f]+/\1/"
    38	2e44dabc23ea0397  local-advisory.sh
    39	2258e370b9ff2575  local-review.sh
    40	099f6c7534223cb4  sandbox-scan.sh
    41	[exit 0]
    42	```
    43	
    44	## 3. Each port against its input
    45	
    46	The input is formatted with the CI's shfmt first, so the diff shows the changes alone; `diff` exits 1 when the files differ.
    47	
    48	```console
    49	$ shfmt -i 4 -sr "$IN/local-review.sh" > "$S/input-local-review.sh" && diff -u --label input/local-review.sh --label scripts/orchestrator/local-review.sh "$S/input-local-review.sh" scripts/orchestrator/local-review.sh
    50	--- input/local-review.sh
    51	+++ scripts/orchestrator/local-review.sh
    52	@@ -1,12 +1,29 @@
    53	 #!/usr/bin/env bash
    54	-# local-review.sh <task> <head> <pr>: C-32. Review a PR head's diff against main with the Bot's engine, locally, before the audit.
    55	-# Run OUTSIDE the Bash sandbox (inside it codex exits 1: "failed to initialize in-process app-server client: Operation not permitted").
    56	-# Writes .orchestration/validation/<task>-local-review-<sha7>.md (findings, then the transcript's final message with the worktree prefix stripped),
    57	-# prints one line per unique finding and "local-review: <n> findings" last; exit 0 when n=0, 3 when n>0, 2 on a precondition.
    58	+# @file local-review.sh
    59	+# @brief Review a PR head's diff against main locally with the Bot's engine, once per head, before the audit (C-32).
    60	+# @description
    61	+#   Run outside the Bash sandbox: inside it codex exits 1 ("failed to initialize in-process app-server client:
    62	+#   Operation not permitted"). An existing `.orchestration/validation/<task>-local-review-<sha7>.md` is reused and
    63	+#   re-reported. Otherwise the clean review worktree (`$ORCH_REVIEW_WORKTREE`, else
    64	+#   `.claude/worktrees/orchestrator-review`), a path with its own `.git` entry, is checked out detached at the head
    65	+#   and left there, and the review binary (`$CODEX_BIN`, else codex) runs in it as `--profile review -s read-only
    66	+#   review --base main`. The file gets the front matter, the unique `- [P0-3]` findings of the transcript's final
    67	+#   message, and that message with the worktree prefix stripped; the findings are printed, then `local-review: <n>
    68	+#   findings (<file>)`.
    69	+# @arg $1 string Task id.
    70	+# @arg $2 string The PR head commit, a local one.
    71	+# @arg $3 int PR number.
    72	+# @exitcode 0 No finding.
    73	+# @exitcode 2 A precondition failed: the head is not a local commit, the review worktree is not a worktree root or not
    74	+#   clean, or there is no review binary.
    75	+# @exitcode 3 One or more findings.
    76	+# @example
    77	+#   scripts/orchestrator/local-review.sh dotfiles-T128-x-a01 "$(git rev-parse FETCH_HEAD)" 356
    78	 set -euo pipefail
    79	 task=$1 head=$2 pr=$3
    80	 R="$(git rev-parse --show-toplevel)"
    81	-W=$R/.claude/worktrees/orchestrator-review
    82	+cd -- "$R"
    83	+W=${ORCH_REVIEW_WORKTREE:-$R/.claude/worktrees/orchestrator-review}
    84	 out=$R/.orchestration/validation/$task-local-review-${head:0:7}.md
    85	 if [ -s "$out" ]; then
    86	     # one sample per head (C-32): a review of this head exists; reuse it instead of sampling again
    87	@@ -21,15 +38,27 @@
    88	     echo "local-review: $head is not a local commit (fetch pull/$pr/head first)"
    89	     exit 2
    90	 }
    91	+# Without its own .git entry, git -C would act on an enclosing checkout and move that one to the head.
    92	+[ -e "$W/.git" ] || {
    93	+    echo "local-review: $W is not a worktree root"
    94	+    exit 2
    95	+}
    96	 [ -z "$(git -C "$W" status --porcelain)" ] || {
    97	     echo "local-review: $W is not clean"
    98	     exit 2
    99	 }
   100	+# Resolved in the root before the checkout and run by its absolute path, so no relative PATH entry (./bin) picks a
   101	+# binary from the PR head.
   102	+codex=$(command -v "${CODEX_BIN:-codex}") || {
   103	+    echo "local-review: no review binary ${CODEX_BIN:-codex}"
   104	+    exit 2
   105	+}
   106	+[[ $codex == /* ]] || codex=$R/$codex
   107	 git -C "$W" checkout -q --detach "$head"
   108	 base=$(git -C "$W" merge-base main HEAD)
   109	 t0=$(date -u +%FT%TZ)
   110	-tmp=$(mktemp)
   111	-(cd "$W" && codex --profile review -s read-only review --base main < /dev/null > "$tmp" 2>&1) || echo "local-review: codex exited $? (see $out)"
   112	+tmp=$(mktemp "${TMPDIR:-/tmp}/local-review.XXXXXX")
   113	+(cd "$W" && "$codex" --profile review -s read-only review --base main < /dev/null > "$tmp" 2>&1) || echo "local-review: codex exited $? (see $out)"
   114	 final=$(awk '/^codex$/{f=1; buf=""; next} f{buf=buf $0 "\n"} END{printf "%s", buf}' "$tmp" | sed "s#$W/##g")
   115	 findings=$(printf '%s\n' "$final" | /usr/bin/grep -E '^- \[P[0-3]\]' | sort -u || true)
   116	 n=$(printf '%s' "$findings" | /usr/bin/grep -c . || true)
   117	[exit 1]
   118	```
   119	```console
   120	$ shfmt -i 4 -sr "$IN/local-advisory.sh" > "$S/input-local-advisory.sh" && diff -u --label input/local-advisory.sh --label scripts/orchestrator/local-advisory.sh "$S/input-local-advisory.sh" scripts/orchestrator/local-advisory.sh
   121	--- input/local-advisory.sh
   122	+++ scripts/orchestrator/local-advisory.sh
   123	@@ -1,9 +1,22 @@
   124	 #!/usr/bin/env bash
   125	-# local-advisory.sh <task> <head40> <owner-task-id>: plan 020 step 1.2 for the local review. Reads .orchestration/validation/<task>-local-review-<head7>.md; for each finding: a P0/P1 prints STOP (the PR's one round is over: the plan's step 4.2), a P2/P3 appends a row `local:<head7>:<n>\tadvisory-p2` under the heading `## Owned by <owner>` of the acceptance record (created when missing) and a `local-finding: <head7>:<n> not-applicable:advisory P2 owned by <owner>; evidence=…` line. Exit 3 on a P0/P1, 0 otherwise.
   126	+# @file local-advisory.sh
   127	+# @brief Record a local review's P2/P3 findings as advisory rows of the acceptance record; stop on a P0/P1.
   128	+# @description
   129	+#   Plan 020 step 1.2 for the local review. Reads `.orchestration/validation/<task>-local-review-<sha7>.md`. Each
   130	+#   unique finding, numbered from 1: a P0/P1 prints STOP (the PR's one round is over: the plan's step 4.2); any
   131	+#   other appends the row `local:<sha7>:<n><TAB>advisory-p2` under the heading `## Owned by <owner>` of
   132	+#   `.orchestration/acceptance/<task>.md` (created when missing) and a `local-finding: <sha7>:<n>
   133	+#   not-applicable:advisory P2 owned by <owner> (…); evidence=…` line, each only when the record lacks it.
   134	+# @arg $1 string Task id.
   135	+# @arg $2 string The reviewed head, 40 hex characters.
   136	+# @arg $3 string The task id that owns the advisory findings.
   137	+# @exitcode 0 No P0/P1 finding.
   138	+# @exitcode 2 No local review file.
   139	+# @exitcode 3 A P0/P1 finding.
   140	+# @example
   141	+#   scripts/orchestrator/local-advisory.sh dotfiles-T128-x-a01 "$head" dotfiles-T128-x-followup-a01
   142	 set -euo pipefail
   143	-task=$1
   144	-head=$2
   145	-owner=$3
   146	+task=$1 head=$2 owner=$3
   147	 cd "$(git rev-parse --show-toplevel)"
   148	 h7=${head:0:7}
   149	 LR=".orchestration/validation/$task-local-review-$h7.md"
   150	@@ -18,8 +31,7 @@
   151	     exit 0
   152	 }
   153	 /usr/bin/grep -q "^## Owned by $owner" "$A" || printf '\n## Owned by %s (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)\n\n' "$owner" >> "$A"
   154	-i=0
   155	-stop=0
   156	+i=0 stop=0
   157	 while IFS= read -r line; do
   158	     i=$((i + 1))
   159	     case "$line" in
   160	[exit 1]
   161	```
   162	```console
   163	$ shfmt -i 4 -sr "$IN/sandbox-scan.sh" > "$S/input-sandbox-scan.sh" && diff -u --label input/sandbox-scan.sh --label scripts/orchestrator/sandbox-scan.sh "$S/input-sandbox-scan.sh" scripts/orchestrator/sandbox-scan.sh
   164	--- input/sandbox-scan.sh
   165	+++ scripts/orchestrator/sandbox-scan.sh
   166	@@ -1,9 +1,24 @@
   167	 #!/usr/bin/env bash
   168	-# sandbox-scan.sh <task>: C-29 interim, extracted from the scratchpad integrate-prep.sh (lines 34 to 38). Prints the unsandboxed mutation calls found in the worker sandbox record .orchestration/sandboxes/<task>.md, or one line saying none; a hit is judged before the audit.
   169	+# @file sandbox-scan.sh
   170	+# @brief Print the unsandboxed mutation calls of a worker's sandbox record, so a hit is judged before the audit (C-29).
   171	+# @description
   172	+#   Reads `.orchestration/sandboxes/<task>.md`, a trailing `-fixtures` of the task id stripped. A line that names
   173	+#   `dangerouslyDisableSandbox`, `outside the sandbox` or `unsandboxed` and a mutation (`git commit`, `git switch -c`,
   174	+#   `git checkout`, `git add`, `git mv`, `git rm`, `cp `, `mv `, `> `, `tee `) but none of `counts`, `reads`, `lists`,
   175	+#   matched case-insensitively, is printed with its line number, then the judge line; with no such line, one line says
   176	+#   none. A missing record prints nothing.
   177	+# @arg $1 string Task id.
   178	+# @exitcode 0 Always.
   179	+# @example
   180	+#   scripts/orchestrator/sandbox-scan.sh dotfiles-T128-x-a01
   181	 set -euo pipefail
   182	 task=$1
   183	 cd "$(git rev-parse --show-toplevel)"
   184	 sb=".orchestration/sandboxes/${task%-fixtures}.md"
   185	 if [ -f "$sb" ]; then
   186	-    if /usr/bin/grep -n -i -E 'dangerouslyDisableSandbox|outside the sandbox|unsandboxed' "$sb" | /usr/bin/grep -i -E 'git (commit|switch -c|checkout|add|mv|rm)|cp |mv |> |tee ' | /usr/bin/grep -v -i 'counts\|reads\|lists'; then echo "sandbox scan: unsandboxed mutation calls above (C-29); judge before the audit"; else echo "sandbox scan: no unsandboxed mutation call in $sb"; fi
   187	+    if /usr/bin/grep -n -i -E 'dangerouslyDisableSandbox|outside the sandbox|unsandboxed' "$sb" | /usr/bin/grep -i -E 'git (commit|switch -c|checkout|add|mv|rm)|cp |mv |> |tee ' | /usr/bin/grep -v -i 'counts\|reads\|lists'; then
   188	+        echo "sandbox scan: unsandboxed mutation calls above (C-29); judge before the audit"
   189	+    else
   190	+        echo "sandbox scan: no unsandboxed mutation call in $sb"
   191	+    fi
   192	 fi
   193	[exit 1]
   194	```
   195	
   196	## 4. The Check: the test module
   197	
   198	```console
   199	$ uv run python -m unittest tests/unit/test_chain_review_scripts.py -v
   200	test_local_advisory_records_p2_rows_and_stops_on_p0_p1 (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_advisory_records_p2_rows_and_stops_on_p0_p1) ... ok
   201	test_local_review_runs_the_review_binary_read_only_at_the_head_and_writes_one_file (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_review_runs_the_review_binary_read_only_at_the_head_and_writes_one_file) ... ok
   202	test_sandbox_scan_prints_the_unsandboxed_mutation_calls (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_sandbox_scan_prints_the_unsandboxed_mutation_calls) ... ok
   203	
   204	----------------------------------------------------------------------
   205	Ran 3 tests in 3.359s
   206	
   207	OK
   208	[exit 0]
   209	```
   210	

**Analyzing potential sed injection risks**
**Evaluating input validation and injection risks**

I’m examining risks around symbolic refs, task names, and environment variables, focusing on potential injection via newlines or path traversal, and checking how validation or lack thereof might affect script execution and metadata integrity.
exec
/bin/zsh -lc "nl -ba .orchestration/validation/dotfiles-T128-chain-review-scripts-a01.md | sed -n '211,375p' && nl -ba .orchestration/sandboxes/dotfiles-T128-chain-review-scripts-a01.md" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc "git grep -n -E 'local-review\\.sh|local-advisory\\.sh|sandbox-scan\\.sh' b6ce4ffabe0e66a102e224e75be575a501c5a793 -- ':"'!.orchestration'"' && git diff --numstat ec94dc56305f55df470a4b1d4215ad272418beac b6ce4ffabe0e66a102e224e75be575a501c5a793 && git ls-tree --name-only origin/main scripts/orchestrator/" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 68ms:
   211	## 5. The Check: shellcheck, with bash -n, shfmt and ruff
   212	
   213	```console
   214	$ shellcheck scripts/orchestrator/local-review.sh scripts/orchestrator/local-advisory.sh scripts/orchestrator/sandbox-scan.sh && echo shellcheck-clean
   215	shellcheck-clean
   216	[exit 0]
   217	```
   218	```console
   219	$ for f in scripts/orchestrator/local-review.sh scripts/orchestrator/local-advisory.sh scripts/orchestrator/sandbox-scan.sh; do bash -n "$f" && echo "bash -n $f: ok"; done; shfmt -i 4 -sr -d scripts/orchestrator/local-review.sh scripts/orchestrator/local-advisory.sh scripts/orchestrator/sandbox-scan.sh && echo shfmt-clean; git ls-files -s scripts/orchestrator/local-review.sh scripts/orchestrator/local-advisory.sh scripts/orchestrator/sandbox-scan.sh | cut -c1-6
   220	bash -n scripts/orchestrator/local-review.sh: ok
   221	bash -n scripts/orchestrator/local-advisory.sh: ok
   222	bash -n scripts/orchestrator/sandbox-scan.sh: ok
   223	shfmt-clean
   224	100755
   225	100755
   226	100755
   227	[exit 0]
   228	```
   229	```console
   230	$ ruff --version; ruff format --check tests/unit/test_chain_review_scripts.py && ruff check tests/unit/test_chain_review_scripts.py && ruff check --preview --select FURB,PLW,SIM,ISC tests/unit/test_chain_review_scripts.py
   231	ruff 0.17.0
   232	1 file already formatted
   233	All checks passed!
   234	All checks passed!
   235	[exit 0]
   236	```
   237	
   238	## 6. The Check: caps
   239	
   240	```console
   241	$ git diff --numstat origin/main...HEAD
   242	49	0	scripts/orchestrator/local-advisory.sh
   243	75	0	scripts/orchestrator/local-review.sh
   244	24	0	scripts/orchestrator/sandbox-scan.sh
   245	230	0	tests/unit/test_chain_review_scripts.py
   246	[exit 0]
   247	```
   248	```console
   249	$ git diff --numstat origin/main...HEAD | awk '$3 !~ /^(tests|\.orchestration)\// {o += $1 + $2; f++} $3 ~ /^tests\// {t += $1} END {printf "outside tests/ and .orchestration/: %d changed lines (cap 200), %d files; under tests/: %d added lines (cap 1000)\n", o, f, t}'
   250	outside tests/ and .orchestration/: 148 changed lines (cap 200), 3 files; under tests/: 230 added lines (cap 1000)
   251	[exit 0]
   252	```
   253	
   254	## 7. The neighbouring test modules
   255	
   256	These modules exercise `scripts/orchestrator/` (test_orchestrator_tools.py copies the whole directory into its temporary repository).
   257	
   258	```console
   259	$ uv run python -m unittest tests/unit/test_orchestrator_tools.py tests/unit/test_task_checkers.py tests/unit/test_orch_gate_path.py tests/unit/test_chain_review_scripts.py 2>&1 | tail -3
   260	Ran 53 tests in 35.788s
   261	
   262	OK
   263	[exit 0]
   264	```
   265	
   266	## 8. Mutation pass
   267	
   268	`$S/mutate.py` applies one textual mutation at a time to one of the three scripts, runs the test module, and restores the script. A mutation counts as caught when the module fails. It skips any pattern that does not occur exactly once. The first full run (before amendment 1) caught 53 of 54, with S8 alive and R12/R13 skipped, since their patterns also matched the shdoc header. The fixture fix is in `1f307a6e`, and the narrowed patterns are in the runner. Below is the full run on the content `1f307a6e` commits (the scripts' hashes equal its blobs), G1, amendment 1's refusal, included:
   269	
   270	```console
   271	$ uv run --no-project python -I "$S/mutate.py" "$PWD"; shasum -a 256 -c "$S/before.sha"
   272	R1 reuse off: caught
   273	R2 reuse exit: caught
   274	R3 reuse msg: caught
   275	R4 local commit: caught
   276	R5 dirty: caught
   277	R6 no cd: caught
   278	R7 no absolutize: caught
   279	R8 lookup in W: caught
   280	R9 CODEX_BIN ignored: caught
   281	R10 ORCH_REVIEW_WORKTREE ignored: caught
   282	R11 no checkout: caught
   283	R12 profile: caught
   284	R13 sandbox: caught
   285	R14 stdin: caught
   286	R15 final message: caught
   287	R16 prefix: caught
   288	R17 unique: caught
   289	R18 codex exited: caught
   290	R19 base: caught
   291	R20 findings field: caught
   292	R21 rm tmp: caught
   293	R22 exit 3: caught
   294	R23 no binary exit: caught
   295	R24 file name: caught
   296	R25 merge-base: caught
   297	R26 cut 2000: caught
   298	G1 worktree root: caught
   299	A1 no file: caught
   300	A2 no findings: caught
   301	A3 heading guard: caught
   302	A4 row guard: caught
   303	A5 line guard: caught
   304	A6 P0: caught
   305	A7 P1: caught
   306	A8 stop exit: caught
   307	A9 unique: caught
   308	A10 cut 120: caught
   309	A11 backticks: caught
   310	A12 numbering: caught
   311	A13 evidence: caught
   312	A14 last line: caught
   313	A15 stop line: caught
   314	S1 fixtures: caught
   315	S2 grep1 -i: caught
   316	S3 grep2 -i: caught
   317	S4 grep3 -i: caught
   318	S5 grep3 off: caught
   319	S6 counts: caught
   320	S7 reads: caught
   321	S8 lists: caught
   322	S9 -n: caught
   323	S10 missing: caught
   324	S11 exit hit: caught
   325	S12 exit none: caught
   326	S13 git add: caught
   327	S14 outside: caught
   328	S15 judge line: caught
   329	mutations: 57, caught 57, survived 0
   330	scripts/orchestrator/local-advisory.sh: OK
   331	scripts/orchestrator/local-review.sh: OK
   332	scripts/orchestrator/sandbox-scan.sh: OK
   333	[exit 0]
   334	```
   335	
   336	## 9. CI and the Bot on `0da6be3e`
   337	
   338	Run outside the sandbox through the permission gate (sandbox record, rows 6 to 9).
   339	
   340	```console
   341	$ gh pr checks 357 --repo mryfmo/dotfiles --watch --interval 30 > /dev/null 2>&1; echo "checks-watch-exit=$?"; gh pr checks 357 --repo mryfmo/dotfiles
   342	checks-watch-exit=0
   343	CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
   344	GitGuardian Security Checks	pass	1s	https://dashboard.gitguardian.com	
   345	private-bootstrap (macos-14, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/38565876286/job/115858280156	
   346	private-bootstrap (ubuntu-24.04, client)	pass	13s	https://github.com/mryfmo/dotfiles/actions/runs/38565876286/job/115858280272	
   347	private-bootstrap (ubuntu-24.04, server)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/38565876286/job/115858279807	
   348	public-bootstrap (macos-14, client)	pass	10m44s	https://github.com/mryfmo/dotfiles/actions/runs/38565876286/job/115858280484	
   349	public-bootstrap (ubuntu-24.04, client)	pass	10m28s	https://github.com/mryfmo/dotfiles/actions/runs/38565876286/job/115858280216	
   350	public-bootstrap (ubuntu-24.04, server)	pass	6m16s	https://github.com/mryfmo/dotfiles/actions/runs/38565876286/job/115858280329	
   351	test (macos-14, client)	pass	6m47s	https://github.com/mryfmo/dotfiles/actions/runs/38565876361/job/115858280528	
   352	test (ubuntu-24.04, client)	pass	8m29s	https://github.com/mryfmo/dotfiles/actions/runs/38565876361/job/115858280070	
   353	test (ubuntu-24.04, server)	pass	5m42s	https://github.com/mryfmo/dotfiles/actions/runs/38565876361/job/115858280743	
   354	test (ubuntu-26.04, client)	pass	7m41s	https://github.com/mryfmo/dotfiles/actions/runs/38565876361/job/115858280869	
   355	validate	pass	1m12s	https://github.com/mryfmo/dotfiles/actions/runs/38565876334/job/115858279537	
   356	[exit 0]
   357	```
   358	```console
   359	$ bash scratchpad/bot-wait.sh 357 0da6be3e10964ff744262e835806fa8081e93ed7 1791981757
   360	elapsed=165s
   361	reviews:
   362	5518077170	0da6be3e10964ff744262e835806fa8081e93ed7	2026-10-14T12:45:21Z	COMMENTED
   363	comments:
   364	4270918132	0da6be3e10964ff744262e835806fa8081e93ed7	scripts/orchestrator/local-review.sh
   365	4270918140	0da6be3e10964ff744262e835806fa8081e93ed7	scripts/orchestrator/local-review.sh
   366	[exit 0]
   367	```
   368	```console
   369	$ gh api repos/mryfmo/dotfiles/pulls/357/comments --paginate --jq '.[]|select(.user.login=="chatgpt-codex-connector[bot]" and .in_reply_to_id==null)|[.id,.original_commit_id[0:8],.path,.line]|@tsv'
   370	4270918132	0da6be3e	scripts/orchestrator/local-review.sh	61
   371	4270918140	0da6be3e	scripts/orchestrator/local-review.sh	28
   372	[exit 0]
   373	```
   374	
   375	The two threads' titles, from row 8's read: 4270918132 `P2 Badge … Reject failed review runs instead of caching them`; 4270918140 `P2 Badge … Validate the full head before reusing a cached review`. Review 5518077170's body holds the summary text and `**Reviewed commit:** \`0da6be3e10\``, and no badge.
     1	---
     2	task_id: dotfiles-T128-chain-review-scripts-a01
     3	seat: claude-standard-dot-a002
     4	permission_gated_commands: see the table
     5	---
     6	
     7	# Sandbox record: dotfiles-T128-chain-review-scripts-a01
     8	
     9	- Period: from the AGMSG-TASK (08:54:36Z) to the RESULT.
    10	- Inside the sandbox ran:
    11	  - the HTTPS `git fetch` and `git push`;
    12	  - the branch, the commit, the task copy and the evidence;
    13	  - every test, lint and format run;
    14	  - the mutation pass and the validation script.
    15	- In the sandbox uv cannot reach pypi, so every uv run used `UV_OFFLINE=1` from the uv cache (validation, header). `uvx ruff` could not write uv's tool directory, so ruff ran as the installed `ruff` 0.17.0.
    16	- macOS `mktemp` without a template writes under `/var/folders/…`, which the sandbox denies. That is why item 1 now names a template (amendment 1, learning 1).
    17	- `diff` cannot open a `/dev/fd` process substitution in the sandbox, so validation §3 diffs scratch files instead.
    18	- The whole unit suite fails in the sandbox (validation, intro); CI's run is the evidence.
    19	- No local mutation was chained onto a call that ran outside the sandbox.
    20	
    21	The table lists every call that ran outside the sandbox: `gh` through the permission gate (`dangerouslyDisableSandbox`, since `gh` fails TLS inside the sandbox) and `agmsg-dispatch` through `excludedCommands`. Rows after the evidence commit are completed in the evidence update.
    22	
    23	| # | Command | Step 4 case |
    24	|--:|---|---|
    25	| 1 | `agmsg-dispatch … AGMSG-PONG v1 task_id=dotfiles-T128-chain-review-scripts-a01 status=question …` (09:02Z, row 11 and the worktree guard) | `agmsg-dispatch` |
    26	| 2 | `agmsg-dispatch … AGMSG-PONG v1 … status=working …` (09:05Z, the `mktemp` template) | `agmsg-dispatch` |
    27	| 3 | `agmsg-dispatch … AGMSG-PONG v1 … status=working …` (12:15Z, the branch state) | `agmsg-dispatch` |
    28	| 4 | `gh pr create --draft --repo mryfmo/dotfiles --base main --head regime/chain-review-scripts …` (PR #357) | `gh` |
    29	| 5 | `gh pr ready 357 --repo mryfmo/dotfiles; date +%s; date -u +%FT%TZ` (12:42:37Z) | `gh` |
    30	| 6 | the Bot wait on `0da6be3e` (`scratchpad/bot-wait.sh`, background; `gh pr view` and `gh api` reads every 30 seconds) | `gh` |
    31	| 7 | `gh pr checks 357 --watch` (background, after a `gh pr checks` poll for the first check; exit 0) | `gh` |
    32	| 8 | `gh api` reads of the two Bot comments and of review 5518077170's body | `gh` |
    33	| 9 | `gh api` re-list of the Bot's top-level comments (validation §9) | `gh` |
    34	| 10 | `agmsg-dispatch … AGMSG-PONG v1 … status=alive …` (12:47Z, the Bot's two P2 threads) | `agmsg-dispatch` |
    35	| 11 | `gh pr checks 357 --watch` on the final head (background, exit status joined) | `gh` |
    36	| 12 | `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T128-chain-review-scripts-a01 …` | `agmsg-dispatch` |
    37	
    38	One command was denied at the permission gate and not pursued: a re-list that ran four reads in one call, the Bot's comment count, the PR's reviews, its issue comments and a GraphQL listing of its review threads. The GraphQL thread listing is not needed, since the worker resolves no thread. Row 9 ran the comment re-list alone, the same `gh api …/pulls/357/comments` read that row 8 had already run.
    39	
    40	The pushes of `1f307a6e`, `0da6be3e` and the evidence update ran inside the sandbox over HTTPS.

 succeeded in 167ms:
b6ce4ffabe0e66a102e224e75be575a501c5a793:scripts/orchestrator/local-advisory.sh:2:# @file local-advisory.sh
b6ce4ffabe0e66a102e224e75be575a501c5a793:scripts/orchestrator/local-advisory.sh:17:#   scripts/orchestrator/local-advisory.sh dotfiles-T128-x-a01 "$head" dotfiles-T128-x-followup-a01
b6ce4ffabe0e66a102e224e75be575a501c5a793:scripts/orchestrator/local-review.sh:2:# @file local-review.sh
b6ce4ffabe0e66a102e224e75be575a501c5a793:scripts/orchestrator/local-review.sh:21:#   scripts/orchestrator/local-review.sh dotfiles-T128-x-a01 "$(git rev-parse FETCH_HEAD)" 356
b6ce4ffabe0e66a102e224e75be575a501c5a793:scripts/orchestrator/sandbox-scan.sh:2:# @file sandbox-scan.sh
b6ce4ffabe0e66a102e224e75be575a501c5a793:scripts/orchestrator/sandbox-scan.sh:13:#   scripts/orchestrator/sandbox-scan.sh dotfiles-T128-x-a01
b6ce4ffabe0e66a102e224e75be575a501c5a793:tests/unit/test_chain_review_scripts.py:111:            self.assertIn("is not a worktree root", self.run_tool("local-review.sh", "t-p", head, 9, code=2, env=plain))
b6ce4ffabe0e66a102e224e75be575a501c5a793:tests/unit/test_chain_review_scripts.py:115:            stdout = self.run_tool("local-review.sh", "t-a", head, 9, code=3, env=env)
b6ce4ffabe0e66a102e224e75be575a501c5a793:tests/unit/test_chain_review_scripts.py:133:            self.run_tool("local-review.sh", "t-b", head, 9, code=3, env=seam, cwd=self.repo / ".orchestration")
b6ce4ffabe0e66a102e224e75be575a501c5a793:tests/unit/test_chain_review_scripts.py:137:            stdout = self.run_tool("local-review.sh", "t-a", head, 9, code=3, env=env)
b6ce4ffabe0e66a102e224e75be575a501c5a793:tests/unit/test_chain_review_scripts.py:143:            stdout = self.run_tool("local-review.sh", "t-c", head, 9, env=env)
b6ce4ffabe0e66a102e224e75be575a501c5a793:tests/unit/test_chain_review_scripts.py:150:        self.assertIn("no review binary", self.run_tool("local-review.sh", "t-d", head, 9, code=2, env=missing))
b6ce4ffabe0e66a102e224e75be575a501c5a793:tests/unit/test_chain_review_scripts.py:153:            self.assertIn("is not clean", self.run_tool("local-review.sh", "t-d", head, 9, code=2, env=env))
b6ce4ffabe0e66a102e224e75be575a501c5a793:tests/unit/test_chain_review_scripts.py:155:            self.assertIn("is not a local commit", self.run_tool("local-review.sh", "t-d", unknown, 9, code=2, env=env))
b6ce4ffabe0e66a102e224e75be575a501c5a793:tests/unit/test_chain_review_scripts.py:181:            stdout = self.run_tool("local-advisory.sh", "t-a01", head, owner)
b6ce4ffabe0e66a102e224e75be575a501c5a793:tests/unit/test_chain_review_scripts.py:191:        stdout = self.run_tool("local-advisory.sh", "t-a01", head, owner, code=3)
b6ce4ffabe0e66a102e224e75be575a501c5a793:tests/unit/test_chain_review_scripts.py:197:        stdout = self.run_tool("local-advisory.sh", "t-a01", head, owner, code=3)
b6ce4ffabe0e66a102e224e75be575a501c5a793:tests/unit/test_chain_review_scripts.py:203:            "local review of abcdef0: no findings\n", self.run_tool("local-advisory.sh", "t-a01", head, owner)
b6ce4ffabe0e66a102e224e75be575a501c5a793:tests/unit/test_chain_review_scripts.py:206:        self.assertIn("no local review file", self.run_tool("local-advisory.sh", "t-b01", head, owner, code=2))
b6ce4ffabe0e66a102e224e75be575a501c5a793:tests/unit/test_chain_review_scripts.py:214:        self.assertEqual(f"2:{hit}\n{SCAN_HIT}\n", self.run_tool("sandbox-scan.sh", "t-a01"))
b6ce4ffabe0e66a102e224e75be575a501c5a793:tests/unit/test_chain_review_scripts.py:218:            f"1:Outside The Sandbox: GIT ADD x\n{SCAN_HIT}\n", self.run_tool("sandbox-scan.sh", "t-b01-fixtures")
b6ce4ffabe0e66a102e224e75be575a501c5a793:tests/unit/test_chain_review_scripts.py:225:        self.assertEqual(none, self.run_tool("sandbox-scan.sh", "t-c01"))
b6ce4ffabe0e66a102e224e75be575a501c5a793:tests/unit/test_chain_review_scripts.py:226:        self.assertEqual("", self.run_tool("sandbox-scan.sh", "t-d01"))
3	0	.orchestration/dotfiles-T128-chain-review-scripts-a01/autoskill.md
18	0	.orchestration/dotfiles-T128-chain-review-scripts-a01/learning.md
103	0	.orchestration/dotfiles-T128-chain-review-scripts-a01/report.md
40	0	.orchestration/dotfiles-T128-chain-review-scripts-a01/sandbox.md
94	0	.orchestration/dotfiles-T128-chain-review-scripts-a01/task.md
375	0	.orchestration/dotfiles-T128-chain-review-scripts-a01/validation.md
49	0	scripts/orchestrator/local-advisory.sh
75	0	scripts/orchestrator/local-review.sh
24	0	scripts/orchestrator/sandbox-scan.sh
230	0	tests/unit/test_chain_review_scripts.py
scripts/orchestrator/acceptance-front-matter.py
scripts/orchestrator/boundary.sh
scripts/orchestrator/bus-read.sh
scripts/orchestrator/codex-review.sh
scripts/orchestrator/design-keydiff.py
scripts/orchestrator/dispatch.sh
scripts/orchestrator/ff-main.sh
scripts/orchestrator/fill_sweep.py
scripts/orchestrator/ledger-check.py
scripts/orchestrator/orch-audit.sh
scripts/orchestrator/orch-gate.sh
scripts/orchestrator/pr-cost.sh
scripts/orchestrator/replay.sh
scripts/orchestrator/resolve-threads.sh
scripts/orchestrator/task-consistency-check.py
scripts/orchestrator/three-repeat.sh

mcp: codex_apps/github.fetch_workflow_run_jobs started
mcp: codex_apps/github.fetch_workflow_run_jobs (completed)
mcp: codex_apps/github.fetch_workflow_run_jobs started
mcp: codex_apps/github.fetch_workflow_run_jobs (completed)
mcp: codex_apps/github.fetch_workflow_run_jobs started
mcp: codex_apps/github.fetch_workflow_run_jobs (completed)
**Verifying evidence base discrepancies**
**Assessing test coverage and ordering**
**Analyzing test coverage and spec conformance**
**Reviewing test environment vulnerabilities**
**Verifying executable environment**
codex
添付入力の 3 つのハッシュ、task copy の一致、変更範囲と行数上限を確認しました。最終 head の CI も成功しています。一方、decoy テストは「root で解決したこと」は確認できますが、「checkout より前」という順序まで検証できるかを切り分けています。受入記録の既知不具合の処分と、sandbox 記録の省略も確認中です。
exec
/bin/zsh -lc "python3 -B -c 'import pathlib,subprocess,hashlib; h=\"b6ce4ffabe0e66a102e224e75be575a501c5a793\"; root=\".orchestration/dotfiles-T128-chain-review-scripts-a01/\"; mapping={\"report.md\":\"reports\",\"validation.md\":\"validation\",\"sandbox.md\":\"sandboxes\"};
for name,folder in mapping.items():
 b=subprocess.check_output([\"git\",\"show\",h+\":\"+root+name]); p=pathlib.Path(\".orchestration\")/folder/\"dotfiles-T128-chain-review-scripts-a01.md\"; print(name,\"matches supplied\",p.read_bytes()==b,\"sha256\",hashlib.sha256(b).hexdigest())
for name in (\"learning.md\",\"autoskill.md\"):
 print(root+name); print(subprocess.check_output([\"git\",\"show\",h+\":\"+root+name],text=True))
for rev in (\"5ec86052ff0f8ef0fa7dbdbbd44e1e389ba9eb6c\",\"5ec860520075a2f0bbb551232de0f868e481a59c\",h):
 r=subprocess.run([\"git\",\"show\",\"-s\",\"--format=%H %P %s\",rev],text=True,capture_output=True); print(rev,r.returncode,r.stdout,r.stderr)
'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc 'command -v codex && ls -l "$(command -v codex)" && file "$(command -v codex)" && git config --show-origin --get-regexp '"'"'^(core'"\\.(hooksPath|fsmonitor)|filter\\..*\\.(process|clean|smudge))"'$'"'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc "git show b6ce4ffabe0e66a102e224e75be575a501c5a793:.github/workflows/test.yaml | sed -n '1,155p' && git show b6ce4ffabe0e66a102e224e75be575a501c5a793:Makefile | sed -n '125,170p' && git diff --check ec94dc56305f55df470a4b1d4215ad272418beac b6ce4ffabe0e66a102e224e75be575a501c5a793" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 exited 2 in 245ms:
name: Unit test

on:
  # Required checks must always report a final status for PRs into `main`.
  # Do not add workflow-level path or branch filters here: GitHub can leave
  # skipped required checks in a pending state and block merges.
  # Keep this workflow unconditional and decide inside jobs whether the full
  # test matrix is necessary for the current diff.
  push:
    branches: [main]
  pull_request:
    branches: [main]
permissions:
  contents: read

jobs:
  test:
    # Run the same test suite on each target OS/system pair.
    # We intentionally keep macOS as `client` only because this repository
    # does not define a macOS `server` test target.
    strategy:
      matrix:
        os: [ubuntu-24.04, macos-14]
        system: [client, server]
        exclude:
          - os: macos-14
            system: server
        # Non-required canary for the next Ubuntu image: it shows how the suite
        # fares there without blocking merges. Adopt it by changing the
        # explicit label above once it is green.
        include:
          - os: ubuntu-26.04
            system: client

    runs-on: ${{ matrix.os }}
    continue-on-error: ${{ matrix.os == 'ubuntu-26.04' }}
    env:
      # Export matrix values to shell scripts so existing test helpers can use
      # simple `OS`/`SYSTEM` checks without depending on GitHub expression syntax.
      OS: ${{ matrix.os }}
      SYSTEM: ${{ matrix.system }}
      # Keep Codecov naming deterministic per job. This makes it easy to trace
      # upload sessions in Codecov API/UI and avoids accidental session overlap.
      CODECOV_FLAGS: ${{ matrix.os }}-${{ matrix.system }}
      CODECOV_NAME: codecov-dotfiles-${{ matrix.os }}-${{ matrix.system }}
      GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

    steps:
      - name: Configure Git defaults
        run: git config --global init.defaultBranch main

      - name: Checkout repository
        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7
        with:
          fetch-depth: 0
          persist-credentials: false

      - name: Decide whether the diff needs the unit tests
        id: decide
        env:
          EVENT_NAME: ${{ github.event_name }}
          BASE_REF: ${{ github.base_ref }}
          BEFORE_SHA: ${{ github.event.before }}
          HEAD_SHA: ${{ github.sha }}
        run: |
          set -euo pipefail

          # Decided in this job, never in a job it needs: a job skipped because
          # a needed job failed reports Success even as a required check, so a
          # failed decision has to fail this job instead.
          if [ "${EVENT_NAME}" = "pull_request" ]; then
            # A full fetch: a shallow one cuts the history of a base tip that
            # moved after the checkout, and the diff then has no merge base.
            git fetch --no-tags origin "${BASE_REF}"
            diff_range="origin/${BASE_REF}...${HEAD_SHA}"
          elif [ -n "${BEFORE_SHA}" ] && [ "${BEFORE_SHA}" != "0000000000000000000000000000000000000000" ]; then
            diff_range="${BEFORE_SHA}...${HEAD_SHA}"
          else
            diff_range="${HEAD_SHA}^...${HEAD_SHA}"
          fi

          echo "diff_range=${diff_range}" >> "${GITHUB_OUTPUT}"

          # One option would be to predefine CI-relevant path groups such as
          # `.github/workflows/`, `home/`, `install/`, and `tests/` in an env-
          # var-like form to make the rule reusable. For this workflow, keeping
          # the pattern inline is still easier to read because the rule is only
          # used once and only decides whether the expensive unit-test steps
          # should run. It does not decide whether the required workflow itself
          # reports a status. If more workflows need the same rule later,
          # extract a shared script instead of hiding the pattern in env.
          # The formatting check also runs here, so any .py or .md outside
          # .orchestration/ counts, as do ruff.toml and .prettierignore.
          # .orchestration-only diffs still skip the matrix.
          # No pipe into grep -q: under pipefail its early exit could SIGPIPE
          # the writer and turn a match into a false negative. core.quotePath
          # off keeps non-ASCII paths raw instead of "\343..."-quoted.
          # --no-renames lists both sides of a rename, so a file moved out of
          # home/ into .orchestration/ still runs the tests.
          changed="$(git -c core.quotePath=false diff --no-renames --name-only "${diff_range}")"
          relevant="$(grep -v '^\.orchestration/' <<< "${changed}" || true)"
          if grep -Eq '^(\.github/workflows/|home/|install/|scripts/|tests/|plans/|docs/|setup\.sh$|Makefile$|ruff\.toml$|\.prettierignore$)|(^|/)[^/]+\.(py|md)$' <<< "${relevant}"; then
            echo "should_test=true" >> "${GITHUB_OUTPUT}"
          else
            echo "should_test=false" >> "${GITHUB_OUTPUT}"
          fi

      - name: Skip full unit test run for unrelated changes
        if: ${{ steps.decide.outputs.should_test != 'true' }}
        run: |
          echo "No unit-test-relevant files changed."
          echo "Compared diff range: ${{ steps.decide.outputs.diff_range }}"

      - name: Install tools
        if: ${{ steps.decide.outputs.should_test == 'true' }}
        run: |
          if [ "${OS}" == "macos-14" ]; then
            # The macos-14 runner image ships third-party taps tapped but
            # untrusted, and Homebrew warns on every `brew install` while one
            # is present. The installs below come from homebrew/core, so
            # resolve those taps with the brew installer's own CI handling
            # rather than a second hard-coded copy of the tap list.
            bash -c 'source install/macos/common/brew.sh; handle_ci_untrusted_taps'

            # `bashcov` on macOS must use Homebrew Bash (>=5) to avoid the
            # system Bash 3.2 parser limitations that produced empty coverage.
            # `gawk` is available for shell tooling used by the test suite.
            brew install bash bats-core gawk parallel shellcheck

          elif [[ "${OS}" == ubuntu-* ]]; then
            # Ruby is required for bashcov/simplecov formatters.
            sudo apt-get update && sudo apt-get install -y bats curl iproute2 parallel ruby shellcheck

          else
            echo "${OS} and ${SYSTEM} are not supported" >&2
            exit 1
          fi

          # `chezmoi` is installed so Bats can render chezmoi templates
          # behaviorally instead of grepping template syntax. Both platforms
          # take the release setup.sh bootstraps: the newest one at least 72
          # hours old, resolved by scripts/lib/github-release.sh.
          source scripts/lib/github-release.sh
          chezmoi_version="$(github_release_tag twpayne/chezmoi)"
          chezmoi_version="${chezmoi_version#v}"
          case "$(uname -s)/$(uname -m)" in
            Darwin/arm64) chezmoi_platform=darwin_arm64 ;;
            Darwin/x86_64) chezmoi_platform=darwin_amd64 ;;
            Linux/x86_64) chezmoi_platform=linux_amd64 ;;
            *) echo "no chezmoi release for $(uname -s)/$(uname -m)" >&2; exit 1 ;;
          esac
          artifact="chezmoi_${chezmoi_version}_${chezmoi_platform}.tar.gz"
          base_url="https://github.com/twpayne/chezmoi/releases/download/v${chezmoi_version}"
          sha256_check=(sha256sum --check --strict)
          command -v sha256sum >/dev/null || sha256_check=(shasum -a 256 --check --strict)

.PHONY: apply
apply: update

.PHONY: gh-auth
# Interactive: log in this machine's GitHub account when gh holds no working login.
gh-auth:
	./scripts/gh-auth.sh

.PHONY: doctor
doctor:
	@tool_status=0; runtime_status=0; runtime_result=passed; \
	./scripts/check-tools.sh || tool_status=$$?; \
	if [ -d home/dot_agents ] && [ -d home/dot_claude ] && [ -d home/dot_codex ]; then \
		./scripts/check-agent-runtime.py || runtime_status=$$?; \
	else \
		echo "optional warning: agent runtime check skipped because source roots are incomplete"; \
		runtime_result=not-applicable; \
	fi; \
	[ "$$runtime_status" -eq 0 ] || runtime_result=failed; \
	tool_result=passed; [ "$$tool_status" -eq 0 ] || tool_result=failed; \
	printf '\nDoctor summary: tools=%s; runtime=%s\n' "$$tool_result" "$$runtime_result"; \
	[ "$$tool_status" -eq 0 ] && [ "$$runtime_status" -eq 0 ]

.PHONY: usage-snapshot
usage-snapshot:
	./scripts/usage-snapshot.sh

.PHONY: usage-report
usage-report:
	uv run python scripts/usage-report.py

.PHONY: agmsg-bootstrap
agmsg-bootstrap:
	@if [ -f home/dot_local/bin/common/executable_herdr-agents ]; then \
		bash home/dot_local/bin/common/executable_herdr-agents --bootstrap-agmsg "$(CURDIR)"; \
	else \
		echo "Herdr agents source helper not found; skipping agmsg bootstrap."; \
	fi

.PHONY: watch
watch:
	DOTFILES_DEBUG=1 watchexec -- chezmoi apply --verbose

.PHONY: reset
reset:
.orchestration/dotfiles-T128-chain-review-scripts-a01/validation.md:344: trailing whitespace.
+GitGuardian Security Checks	pass	1s	https://dashboard.gitguardian.com	
.orchestration/dotfiles-T128-chain-review-scripts-a01/validation.md:345: trailing whitespace.
+private-bootstrap (macos-14, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/38565876286/job/115858280156	
.orchestration/dotfiles-T128-chain-review-scripts-a01/validation.md:346: trailing whitespace.
+private-bootstrap (ubuntu-24.04, client)	pass	13s	https://github.com/mryfmo/dotfiles/actions/runs/38565876286/job/115858280272	
.orchestration/dotfiles-T128-chain-review-scripts-a01/validation.md:347: trailing whitespace.
+private-bootstrap (ubuntu-24.04, server)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/38565876286/job/115858279807	
.orchestration/dotfiles-T128-chain-review-scripts-a01/validation.md:348: trailing whitespace.
+public-bootstrap (macos-14, client)	pass	10m44s	https://github.com/mryfmo/dotfiles/actions/runs/38565876286/job/115858280484	
.orchestration/dotfiles-T128-chain-review-scripts-a01/validation.md:349: trailing whitespace.
+public-bootstrap (ubuntu-24.04, client)	pass	10m28s	https://github.com/mryfmo/dotfiles/actions/runs/38565876286/job/115858280216	
.orchestration/dotfiles-T128-chain-review-scripts-a01/validation.md:350: trailing whitespace.
+public-bootstrap (ubuntu-24.04, server)	pass	6m16s	https://github.com/mryfmo/dotfiles/actions/runs/38565876286/job/115858280329	
.orchestration/dotfiles-T128-chain-review-scripts-a01/validation.md:351: trailing whitespace.
+test (macos-14, client)	pass	6m47s	https://github.com/mryfmo/dotfiles/actions/runs/38565876361/job/115858280528	
.orchestration/dotfiles-T128-chain-review-scripts-a01/validation.md:352: trailing whitespace.
+test (ubuntu-24.04, client)	pass	8m29s	https://github.com/mryfmo/dotfiles/actions/runs/38565876361/job/115858280070	
.orchestration/dotfiles-T128-chain-review-scripts-a01/validation.md:353: trailing whitespace.
+test (ubuntu-24.04, server)	pass	5m42s	https://github.com/mryfmo/dotfiles/actions/runs/38565876361/job/115858280743	
.orchestration/dotfiles-T128-chain-review-scripts-a01/validation.md:354: trailing whitespace.
+test (ubuntu-26.04, client)	pass	7m41s	https://github.com/mryfmo/dotfiles/actions/runs/38565876361/job/115858280869	
.orchestration/dotfiles-T128-chain-review-scripts-a01/validation.md:355: trailing whitespace.
+validate	pass	1m12s	https://github.com/mryfmo/dotfiles/actions/runs/38565876334/job/115858279537	

 succeeded in 372ms:
report.md matches supplied True sha256 2a24a6c4d7f392ac87cd7d5369f9067f44993effa6bad9a59137e7ee402dac67
validation.md matches supplied True sha256 0acb314c38fdcb8c649a19a760b0a45a298a0f338ecac4a7777c7b1b361c53ad
sandbox.md matches supplied True sha256 56279f5957c024f0ec9a204219a0763dfc7aaf7931c054edd600c9815e505873
.orchestration/dotfiles-T128-chain-review-scripts-a01/learning.md
# Learning triage: dotfiles-T128-chain-review-scripts-a01

These are candidates only; nothing is promoted.

1. [memory:failure] macOS `mktemp` with no template, or with only `-t`, ignores `TMPDIR`. It takes `_CS_DARWIN_USER_TEMP_DIR` (`/var/folders/…/T/`) first, as `man mktemp` says, and the Claude sandbox denies writes there. The input's bare `mktemp` therefore worked outside the sandbox, where the chain runs it, and failed inside the sandbox, where the tests run. On Linux, `mktemp` follows `TMPDIR`.
   - Detected by the first test run: `mktemp: mkstemp failed on /var/folders/…: Operation not permitted`.
   - Mechanism candidate: a repository script takes its temporary file from an explicit template, `mktemp "${TMPDIR:-/tmp}/<name>.XXXXXX"`, as `orch-gate.sh` already does. A shellcheck-style grep in the test suite for a bare `$(mktemp)` under `scripts/` would catch the next one.
2. [memory:decision] A port that freezes an input's behaviour can still need a guard the input lacks. `git -C <dir>` falls through to the enclosing repository when `<dir>` exists but is not a worktree root. So a review-worktree path that names a plain directory inside a clean checkout would move that checkout to the PR head. I asked before the PR opened (09:02Z); the orchestrator answered with amendment 1 rather than a PONG answer. Ask about a guard beyond the frozen text before the first push, together with every other discrepancy found by reading the task's rows against the input (here, row 11's tool list).
3. [memory:failure] Two kinds of mutation-pass gap had nothing to do with the code under test:
   - A fixture line meant to exercise one filter was dropped earlier by another filter. `tee:` does not match the `tee ` pattern, so the `lists` exclusion never ran (mutation S8).
   - A mutation's pattern also matched the shdoc header, so the runner skipped it (R12, R13).

   Mechanism candidate: the mutation runner refuses a pattern that does not occur exactly once, which it already does, and the report lists every skip. A fixture line for a filter carries every token that the earlier filters require.
4. [memory:failure] Two behaviours that item 1 freezes from the input fail open, and neither my reading of the task nor the mutation pass flagged them. The Bot raised both, as P2s:
   - a failed review run is still written, with `findings: 0` when nothing came back, and then reused as a review;
   - the reuse is keyed by seven hex characters, and the recorded full head is never compared.

   A mutation pass checks that the tests pin the behaviour; it cannot ask whether the behaviour is safe. Mechanism candidate: before a port's PR opens, read each frozen behaviour for a fail-open path (an error that still fills a cache, a lossy key, a default that passes) and name each one in the early question. The owning follow-up task then exists before the Bot raises them.

.orchestration/dotfiles-T128-chain-review-scripts-a01/autoskill.md
# AutoSkill run: dotfiles-T128-chain-review-scripts-a01

- Status: not used. The task names no AutoSkill run.

5ec86052ff0f8ef0fa7dbdbbd44e1e389ba9eb6c 128  fatal: bad object 5ec86052ff0f8ef0fa7dbdbbd44e1e389ba9eb6c

5ec860520075a2f0bbb551232de0f868e481a59c 0 5ec860520075a2f0bbb551232de0f868e481a59c 983123fd74bf2d23012209d74e93266db14dd4f0 fix(orchestrator): orch-gate.sh runs the gate with a private PATH of resolved gh and git (T128 gate-wrapper-path a01) (#355)
 
b6ce4ffabe0e66a102e224e75be575a501c5a793 0 b6ce4ffabe0e66a102e224e75be575a501c5a793 04a7d02ad856eadab87ff54b383e65e806b0a5f3 ec94dc56305f55df470a4b1d4215ad272418beac Merge branch 'main' into regime/chain-review-scripts
 

 exited 1 in 861ms:
~/.local/share/mise/shims/codex
lrwxr-xr-x  1 a0004262  staff  31 Sep 30 13:43 ~/.local/share/mise/shims/codex -> ~/.local/bin/mise
~/.local/share/mise/shims/codex: Mach-O 64-bit executable arm64

**Analyzing mise shim path injection risks**
**Investigating configuration trust and shim execution**

I'm checking how mise handles trust for config files and executable paths, especially in PRs, and considering the risk of untrusted configs causing command injection through shims. I want to verify official docs, understand git filters and hooks behavior, and assess environment variable influence on execution trust.
**Verifying sed write injection feasibility**
**Analyzing unconventional command injection paths**
mcp: codex_apps/github.fetch_workflow_job_logs started
mcp: codex_apps/github.fetch_workflow_job_logs (completed)
mcp: codex_apps/github.fetch_pr started
mcp: codex_apps/github.fetch_pr (completed)
**Summarizing risk and scope**
**Analyzing sed injection and path handling**
exec
/bin/zsh -lc "git show b6ce4ffabe0e66a102e224e75be575a501c5a793:scripts/orchestrator/orch-gate.sh | sed -n '1,150p' && rg --files ~/Workspace/dotfiles/plans | rg '021|020'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc "python3 -B -c 'import pathlib,subprocess,posixpath; w=\"/tmp/review#review#;w /dev/stderr\\n#\"; expression=\"s#\"+w+\"/##g\"; r=subprocess.run([\"/usr/bin/sed\",expression],input=\"/tmp/review/file\\n\",capture_output=True,text=True); print(\"read-only sed proof\",{\"expression\":expression,\"rc\":r.returncode,\"stdout\":r.stdout,\"stderr\":r.stderr}); task=\"../../../escape\"; print(\"out traversal\",posixpath.normpath(\"/repo/.orchestration/validation/\"+task+\"-local-review-abcdef0.md\")); print(\"acceptance traversal\",posixpath.normpath(\"/repo/.orchestration/acceptance/\"+task+\".md\")); h=\"b6ce4ffabe0e66a102e224e75be575a501c5a793\";
for name in (\"local-review.sh\",\"local-advisory.sh\",\"sandbox-scan.sh\"):
 code=subprocess.check_output([\"git\",\"show\",h+\":scripts/orchestrator/\"+name],text=True); r=subprocess.run([\"bash\",\"-n\"],input=code,text=True,capture_output=True); print(name,\"bash-n\",r.returncode,r.stderr)
r=subprocess.run([\"git\",\"ls-tree\",\"--name-only\",\"origin/main\",\"scripts/orchestrator/\"],capture_output=True,text=True); print(\"premise count\",sum(any(x in s for x in [\"local-review\",\"local-advisory\",\"sandbox-scan\"]) for s in r.stdout.splitlines()))'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 exited 1 in 104ms:
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
#   directory is made and the head checked out removes it and restores the review worktree to origin/main whatever
#   fails or the gate says.
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
git -C "${review}" clean -fdq -- .orchestration; git -C "${review}" checkout -qf --detach origin/main' EXIT
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

 succeeded in 232ms:
read-only sed proof {'expression': 's#/tmp/review#review#;w /dev/stderr\n#/##g', 'rc': 1, 'stdout': '', 'stderr': 'sed: /dev/stderr: Operation not permitted\n'}
out traversal /escape-local-review-abcdef0.md
acceptance traversal /escape.md
local-review.sh bash-n 0 
local-advisory.sh bash-n 0 
sandbox-scan.sh bash-n 0 
premise count 0

**Analyzing sandbox restrictions and command execution**
**Reviewing gate-wrapper and sandbox behavior**
exec
/bin/zsh -lc "rg -n 'mise|shims|TRUSTED|CONFIG|path:' tests/unit/test_orch_gate_path.py home/dot_config/mise home/dot_agents/agent-config.yaml scripts/check-agent-runtime.py && rg --files ~/Workspace/dotfiles/.claude/plans ~/Workspace/dotfiles/.agents/worklog 2>/dev/null | rg '021|020' | head -15" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 91ms:
scripts/check-agent-runtime.py:57:    "ensure_mise_npm_agent_cli",
scripts/check-agent-runtime.py:74:UPDATER_SOURCE_COMMAND = 'source "$1"; export PATH="$HOME/.local/share/mise/shims:$PATH"; shift; "$@"'
scripts/check-agent-runtime.py:91:def render_template(path: Path) -> str:
scripts/check-agent-runtime.py:333:def normalized_path(path: Path) -> Path:
scripts/check-agent-runtime.py:343:def installed_manifest_error(manifest_path: Path) -> str | None:
scripts/check-agent-runtime.py:361:def manifest_path_owners(manifest_path: Path) -> dict[str, list[Path]]:
scripts/check-agent-runtime.py:417:    if step == "ensure_mise_npm_agent_cli":
scripts/check-agent-runtime.py:418:        mise_tool = MISE_STEP_IDENTITIES.get(identity) if separator else None
scripts/check-agent-runtime.py:419:        if mise_tool is None:
scripts/check-agent-runtime.py:421:        arguments = (identity, mise_tool)
scripts/check-agent-runtime.py:603:    The file is CONFIG_DIR/hosts.yml, by default gh's own
scripts/check-agent-runtime.py:604:    `${GH_CONFIG_DIR:-${XDG_CONFIG_HOME:-$HOME/.config}/gh}/hosts.yml`, whatever gh reports.
scripts/check-agent-runtime.py:607:        xdg = Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config")
scripts/check-agent-runtime.py:608:        config_dir = Path(os.environ.get("GH_CONFIG_DIR") or xdg / "gh")
home/dot_agents/agent-config.yaml:87:  config_path: home/.chezmoitemplates/codex-config-managed.toml
home/dot_agents/agent-config.yaml:120:      PATH: '{{ .chezmoi.homeDir }}/.local/share/mise/installs/node/lts/bin:{{ .chezmoi.homeDir }}/.local/share/mise/shims:{{ .chezmoi.homeDir }}/.local/bin:{{ .chezmoi.homeDir }}/.local/bin/common:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin'
home/dot_agents/agent-config.yaml:186:  settings_path: home/.chezmoitemplates/claude-settings-managed.json
home/dot_agents/agent-config.yaml:187:  mcp_config_path: home/dot_claude/private_mcp.json.tmpl
home/dot_agents/agent-config.yaml:305:  marketplace_path: home/dot_agents/plugins/create_marketplace.json
home/dot_agents/agent-config.yaml:316:      source_path: ./plugins/mryfmo-dev-workflows
home/dot_agents/agent-config.yaml:327:      source_path: ./.codex/plugins/crit
home/dot_agents/agent-config.yaml:341:# minimum_release_age in home/dot_mise/config.toml). Only a component whose
home/dot_agents/agent-config.yaml:348:  mise:
home/dot_agents/agent-config.yaml:350:    upstream: jdx/mise
home/dot_agents/agent-config.yaml:355:    note: the newest cooled-down release installs only when gpg and gpgv (SHASUMS256.asc checked against the release key with gpg_fingerprint, fetched from keys.openpgp.org as mise documents) or an authenticated gh (the release attestation) can verify it before it runs; otherwise the fallback release does, and mise self-update moves it forward afterwards.
home/dot_agents/agent-config.yaml:363:      reason: a host without gpg and without an authenticated gh (a fresh macOS) can check neither the release key's signature nor the release attestation before mise runs, and SHASUMS256.txt comes from the same release; so it bootstraps this reviewed release, SHASUMS256.txt kept as a second check.
home/dot_agents/agent-config.yaml:364:    install_path: ~/.local/bin/mise
home/dot_agents/agent-config.yaml:365:    installer: install/common/mise.sh
home/dot_agents/agent-config.yaml:367:      file: install/common/mise.sh
home/dot_agents/agent-config.yaml:380:    install_path: ~/.local/bin/sheldon
home/dot_agents/agent-config.yaml:391:    install_path: ~/.local/bin/starship
home/dot_agents/agent-config.yaml:405:    install_path: ~/.local/share/aws-cli
home/dot_agents/agent-config.yaml:417:    install_path: Homebrew default prefix (/opt/homebrew or /usr/local)
home/dot_agents/agent-config.yaml:430:    note: chezmoi signs its checksums with cosign only, which a fresh host cannot run; the newest cooled-down release installs only when an authenticated gh can check its release attestation before it runs, otherwise the fallback release does, and mise's own chezmoi takes over after the bootstrap.
home/dot_agents/agent-config.yaml:439:    install_path: ~/.local/bin/chezmoi
home/dot_agents/agent-config.yaml:457:    install_path: ~/.local/bin/tode
home/dot_agents/agent-config.yaml:470:    install_path: ~/.local/bin/terminal-browser
home/dot_agents/agent-config.yaml:486:    install_path: ~/.local/bin/crit
home/dot_agents/agent-config.yaml:501:    install_path: ~/.local/bin/zed
home/dot_agents/agent-config.yaml:510:    install_path: ~/.understand-anything/repo
home/dot_agents/agent-config.yaml:524:    install_path: ~/.agents/compactiondb
home/dot_agents/agent-config.yaml:536:    install_path: ~/.agents/skills/agmsg
tests/unit/test_orch_gate_path.py:3:orch-gate.sh runs from its copy in a temporary root with `uv`, `mise`, `gh` and `git` stubbed first on PATH. Every stub
tests/unit/test_orch_gate_path.py:4:appends one line `<name> <argv> <cwd>` to one log and runs nothing else: `uv` answers the gate stub's path, `mise
tests/unit/test_orch_gate_path.py:5:which <name>` answers `installs/<name>` (`payload/<name>` under the mise overrides every run exports, as a real mise
tests/unit/test_orch_gate_path.py:22:    "bin/mise": '[[ -z "$MISE_CONFIG_FILE$MISE_TRUSTED_CONFIG_PATHS" ]] && d=installs || d=payload\n'
tests/unit/test_orch_gate_path.py:60:        # A caller's mise overrides that would point mise which at a payload (PR #355 thread 4267889542).
tests/unit/test_orch_gate_path.py:61:        env |= {"MISE_CONFIG_FILE": f"{self.t}/payload.toml", "MISE_TRUSTED_CONFIG_PATHS": str(self.t)}
tests/unit/test_orch_gate_path.py:89:        mise = [i for i, (command, _) in enumerate(log) if command.startswith("mise ")]
tests/unit/test_orch_gate_path.py:91:            [("mise which gh", str(self.root)), ("mise which git", str(self.root))], [log[i] for i in mise]
tests/unit/test_orch_gate_path.py:94:        self.assertLess(mise[-1], checkout)
tests/unit/test_orch_gate_path.py:96:    def test_orch_gate_refuses_a_binary_resolved_under_a_shims_directory(self):
tests/unit/test_orch_gate_path.py:97:        for answer in ('printf "%s\\n" "{t}/mise/shims/$2"\n', "exit 0\n"):
tests/unit/test_orch_gate_path.py:99:                self.stub("bin/mise", answer)
tests/unit/test_orch_gate_path.py:101:                self.assertIn("no binary for gh outside a shims directory", self.stderr)
tests/unit/test_orch_gate_path.py:110:        self.stub("bin/mise", 'printf "%s\\n" "{t}/mise/shims/$2"\n')
home/dot_config/mise/config.toml.tmpl:1:{{ include "dot_mise/config.toml" -}}

web search: 
web search: https://mise.jdx.dev/dev-tools/shims.html
**Planning efficient tool usage**
exec
/bin/zsh -lc "rg -n 'trusted_config|codex|mise|path:' home/dot_mise/config.toml tests/unit/test_orch_gate_path.py && python3 -B -c 'import os; print({k:v for k,v in os.environ.items() if k in [\"MISE_TRUSTED_CONFIG_PATHS\",\"MISE_CONFIG_FILE\",\"MISE_PARANOID\"]})'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 109ms:
tests/unit/test_orch_gate_path.py:3:orch-gate.sh runs from its copy in a temporary root with `uv`, `mise`, `gh` and `git` stubbed first on PATH. Every stub
tests/unit/test_orch_gate_path.py:4:appends one line `<name> <argv> <cwd>` to one log and runs nothing else: `uv` answers the gate stub's path, `mise
tests/unit/test_orch_gate_path.py:5:which <name>` answers `installs/<name>` (`payload/<name>` under the mise overrides every run exports, as a real mise
tests/unit/test_orch_gate_path.py:22:    "bin/mise": '[[ -z "$MISE_CONFIG_FILE$MISE_TRUSTED_CONFIG_PATHS" ]] && d=installs || d=payload\n'
tests/unit/test_orch_gate_path.py:60:        # A caller's mise overrides that would point mise which at a payload (PR #355 thread 4267889542).
tests/unit/test_orch_gate_path.py:89:        mise = [i for i, (command, _) in enumerate(log) if command.startswith("mise ")]
tests/unit/test_orch_gate_path.py:91:            [("mise which gh", str(self.root)), ("mise which git", str(self.root))], [log[i] for i in mise]
tests/unit/test_orch_gate_path.py:94:        self.assertLess(mise[-1], checkout)
tests/unit/test_orch_gate_path.py:97:        for answer in ('printf "%s\\n" "{t}/mise/shims/$2"\n', "exit 0\n"):
tests/unit/test_orch_gate_path.py:99:                self.stub("bin/mise", answer)
tests/unit/test_orch_gate_path.py:110:        self.stub("bin/mise", 'printf "%s\\n" "{t}/mise/shims/$2"\n')
home/dot_mise/config.toml:27:"npm:@openai/codex" = "latest"
{}

web search: 
web search: https://mise.jdx.dev/security.html
**Confirming scope and environment concerns**
web search: 
web search: 'trust'
exec
/bin/zsh -lc "python3 -B -c 'import subprocess; cases=[(\"/tmp/review[1]\",\"/tmp/review[1]/file\\n\"),(\"/tmp/review#x#;p\\n#\",\"/tmp/review/file\\n\")];
for w,data in cases:
 r=subprocess.run([\"/usr/bin/sed\",\"s#\"+w+\"/##g\"],input=data,capture_output=True,text=True); print({\"W\":w,\"rc\":r.returncode,\"stdout\":r.stdout,\"stderr\":r.stderr})' && git status --porcelain --untracked-files=normal" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 163ms:
{'W': '/tmp/review[1]', 'rc': 0, 'stdout': '/tmp/review[1]/file\n', 'stderr': ''}
{'W': '/tmp/review#x#;p\n#', 'rc': 0, 'stdout': 'x/file\nx/file\n', 'stderr': ''}
?? .orchestration/acceptance/dotfiles-T128-chain-review-scripts-a01.md
?? .orchestration/reports/dotfiles-T128-chain-review-scripts-a01.md
?? .orchestration/sandboxes/dotfiles-T128-chain-review-scripts-a01.md
?? .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-a01-audit-b6ce4ff.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-a01-pr-feedback.json
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-a01.md

**Summarizing trust and environment checks**
**Reviewing orchestration and tooling findings**
**Auditing review priorities and dispositions**
codex
安全性の主張に隙間があります。既定の `codex` はこの環境では mise shim なので、絶対パスを確保しても、起動時に PR 側の設定で実体が選ばれます。また、task 名の `../` は書き込み先を指定ディレクトリ外へ移せます。仕様どおりの移植である点と、こうした境界の未検証部分を分けて報告します。
exec
/bin/zsh -lc "python3 -B -c 'import pathlib,json; p=pathlib.Path(\".orchestration/validation/dotfiles-T128-chain-review-scripts-a01-pr-feedback.json\"); d=json.loads(p.read_text()); print(\"feedback metadata\",{k:v for k,v in d.items() if k not in [\"items\",\"checks\"]}); print(\"checks\",[(x.get(\"name\"),x.get(\"conclusion\")) for x in d.get(\"checks\",[])]); print(\"item summaries\",[(x.get(\"source\"),x.get(\"level\"),x.get(\"path\"),x.get(\"line\"),bool(x.get(\"disposition\"))) for x in d[\"items\"]); print(\"disposition lines\"); [print(str(i)+\": \"+s) for i,s in enumerate(p.read_text().splitlines(),1) if \"advisory P2 owned\" in s]'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc "git show b6ce4ffabe0e66a102e224e75be575a501c5a793:tests/unit/test_chain_review_scripts.py | nl -ba | sed -n '80,157p' && git show b6ce4ffabe0e66a102e224e75be575a501c5a793:scripts/orchestrator/local-review.sh | nl -ba | sed -n '23,75p'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 113ms:
    80	        )
    81	        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
    82	        return result.stdout
    83	
    84	    def test_local_review_runs_the_review_binary_read_only_at_the_head_and_writes_one_file(self):
    85	        review = self.temp / "review"
    86	        self.git("worktree", "add", "-q", "--detach", str(review), "main")
    87	        # The head commit, made in the review worktree, carries a decoy bin/codex; the main working tree never does.
    88	        self.stub(review / "bin/codex", "decoy")
    89	        self.write("b.txt", "b\n", root=review)
    90	        self.git("add", "bin/codex", "b.txt", cwd=review)
    91	        self.git("commit", "-q", "-m", "head", cwd=review)
    92	        head, base = self.git("rev-parse", "HEAD", cwd=review), self.git("rev-parse", "main")
    93	        self.git("checkout", "-q", "--detach", "main", cwd=review)
    94	        self.stub(self.temp / "bin/codex", "codex")
    95	        (self.repo / ".orchestration/validation").mkdir(parents=True)
    96	        path = f"./bin{os.pathsep}{self.temp / 'bin'}{os.pathsep}{os.environ['PATH']}"
    97	        env = {"ORCH_REVIEW_WORKTREE": str(review), "PATH": path}
    98	        # An earlier marker's message is not the final one; the worktree prefix is stripped; a repeated line counts once.
    99	        final = f"One finding.\n- [P2] {review}/b.txt:1 b is new\n- [P2] {review}/b.txt:1 b is new\n"
   100	        (self.calls / "transcript").write_text(f"codex\n- [P1] {review}/a.txt:1 superseded\ncodex\n{final}")
   101	        finding = "- [P2] b.txt:1 b is new"
   102	        call = f"{ARGV}\ncwd: {review}\nhead: {head}\npath: {path}\nstdin: \n"
   103	
   104	        def out(task):
   105	            return self.repo / f".orchestration/validation/{task}-local-review-{head[:7]}.md"
   106	
   107	        with self.subTest("a review worktree path without its own .git entry exits 2"):
   108	            # First, while the main working tree is clean: the dirty check alone would pass it.
   109	            (self.repo / "plain").mkdir()
   110	            plain = {**env, "ORCH_REVIEW_WORKTREE": str(self.repo / "plain")}
   111	            self.assertIn("is not a worktree root", self.run_tool("local-review.sh", "t-p", head, 9, code=2, env=plain))
   112	            self.assertEqual("", self.log("codex"))
   113	            self.assertEqual(base, self.git("rev-parse", "HEAD"))
   114	        with self.subTest("CODEX_BIN unset: codex resolved in the root before the checkout"):
   115	            stdout = self.run_tool("local-review.sh", "t-a", head, 9, code=3, env=env)
   116	            self.assertEqual(f"{finding}\nlocal-review: 1 findings ({out('t-a')})\n", stdout)
   117	            self.assertEqual(call, self.log("codex"))
   118	            self.assertEqual("", self.log("decoy"))
   119	            self.assertEqual(head, self.git("rev-parse", "HEAD", cwd=review))
   120	            status = self.git("status", "--porcelain", "--untracked-files=all")
   121	            self.assertEqual(f"?? .orchestration/validation/t-a-local-review-{head[:7]}.md", status)
   122	            text = out("t-a").read_text()
   123	            front = f"---\ntask: t-a\nhead: {head}\npr: 9\nbase: {base}\nstarted: .+\nfinished: .+\nfindings: 1\n"
   124	            self.assertRegex(text, "^" + re.escape(front).replace(r"\.\+", ".+"))
   125	            self.assertIn("engine: codex review --base main (profile review, read-only)\n---\n", text)
   126	            self.assertIn(f"\n{finding}\n\n```text\nOne finding.\n{finding}\n{finding}\n```\n", text)
   127	            self.assertNotIn("superseded", text)
   128	            self.assertEqual([], list(self.temp.glob("local-review.*")))
   129	        self.git("checkout", "-q", "--detach", "main", cwd=review)
   130	        with self.subTest("CODEX_BIN set: that binary runs, a relative path resolved in the root"):
   131	            self.stub(self.repo / "seam/review-binary", "seam")
   132	            seam = {**env, "CODEX_BIN": "seam/review-binary"}
   133	            self.run_tool("local-review.sh", "t-b", head, 9, code=3, env=seam, cwd=self.repo / ".orchestration")
   134	            self.assertEqual(call, self.log("seam"))
   135	            self.assertEqual(call, self.log("codex"))
   136	        with self.subTest("one review per head: the file is reused"):
   137	            stdout = self.run_tool("local-review.sh", "t-a", head, 9, code=3, env=env)
   138	            self.assertEqual(f"{finding}\nlocal-review: 1 findings (existing {out('t-a')})\n", stdout)
   139	            self.assertEqual(call, self.log("codex"))
   140	        (self.calls / "transcript").write_text("codex\nNo findings.\n")
   141	        (self.calls / "status").write_text("5")
   142	        with self.subTest("no finding exits 0, also when the binary fails"):
   143	            stdout = self.run_tool("local-review.sh", "t-c", head, 9, env=env)
   144	            file = out("t-c")
   145	            self.assertEqual(
   146	                f"local-review: codex exited 5 (see {file})\n\nlocal-review: 0 findings ({file})\n", stdout
   147	            )
   148	            self.assertIn("findings: 0\n", out("t-c").read_text())
   149	        missing = {**env, "CODEX_BIN": "seam/missing"}
   150	        self.assertIn("no review binary", self.run_tool("local-review.sh", "t-d", head, 9, code=2, env=missing))
   151	        self.write("dirty.txt", "x\n", root=review)
   152	        with self.subTest("a dirty review worktree or an unknown head exits 2 and runs nothing"):
   153	            self.assertIn("is not clean", self.run_tool("local-review.sh", "t-d", head, 9, code=2, env=env))
   154	            unknown = "0" * 40
   155	            self.assertIn("is not a local commit", self.run_tool("local-review.sh", "t-d", unknown, 9, code=2, env=env))
   156	            self.assertEqual(2, self.log("codex").count(ARGV))
   157	            self.assertFalse(out("t-d").exists())
    23	task=$1 head=$2 pr=$3
    24	R="$(git rev-parse --show-toplevel)"
    25	cd -- "$R"
    26	W=${ORCH_REVIEW_WORKTREE:-$R/.claude/worktrees/orchestrator-review}
    27	out=$R/.orchestration/validation/$task-local-review-${head:0:7}.md
    28	if [ -s "$out" ]; then
    29	    # one sample per head (C-32): a review of this head exists; reuse it instead of sampling again
    30	    findings=$(/usr/bin/grep -E '^- \[P[0-3]\]' "$out" | sort -u || true)
    31	    n=$(sed -n 's/^findings: //p' "$out" | head -1)
    32	    printf '%s\n' "$findings"
    33	    echo "local-review: $n findings (existing $out)"
    34	    [ "${n:-0}" = 0 ] || exit 3
    35	    exit 0
    36	fi
    37	git -C "$R" cat-file -e "$head^{commit}" 2> /dev/null || {
    38	    echo "local-review: $head is not a local commit (fetch pull/$pr/head first)"
    39	    exit 2
    40	}
    41	# Without its own .git entry, git -C would act on an enclosing checkout and move that one to the head.
    42	[ -e "$W/.git" ] || {
    43	    echo "local-review: $W is not a worktree root"
    44	    exit 2
    45	}
    46	[ -z "$(git -C "$W" status --porcelain)" ] || {
    47	    echo "local-review: $W is not clean"
    48	    exit 2
    49	}
    50	# Resolved in the root before the checkout and run by its absolute path, so no relative PATH entry (./bin) picks a
    51	# binary from the PR head.
    52	codex=$(command -v "${CODEX_BIN:-codex}") || {
    53	    echo "local-review: no review binary ${CODEX_BIN:-codex}"
    54	    exit 2
    55	}
    56	[[ $codex == /* ]] || codex=$R/$codex
    57	git -C "$W" checkout -q --detach "$head"
    58	base=$(git -C "$W" merge-base main HEAD)
    59	t0=$(date -u +%FT%TZ)
    60	tmp=$(mktemp "${TMPDIR:-/tmp}/local-review.XXXXXX")
    61	(cd "$W" && "$codex" --profile review -s read-only review --base main < /dev/null > "$tmp" 2>&1) || echo "local-review: codex exited $? (see $out)"
    62	final=$(awk '/^codex$/{f=1; buf=""; next} f{buf=buf $0 "\n"} END{printf "%s", buf}' "$tmp" | sed "s#$W/##g")
    63	findings=$(printf '%s\n' "$final" | /usr/bin/grep -E '^- \[P[0-3]\]' | sort -u || true)
    64	n=$(printf '%s' "$findings" | /usr/bin/grep -c . || true)
    65	{
    66	    printf -- '---\ntask: %s\nhead: %s\npr: %s\nbase: %s\nstarted: %s\nfinished: %s\nfindings: %s\nengine: codex review --base main (profile review, read-only)\n---\n\n' "$task" "$head" "$pr" "$base" "$t0" "$(date -u +%FT%TZ)" "$n"
    67	    printf '%s\n\n' "$findings"
    68	    echo '```text'
    69	    printf '%s\n' "$final" | cut -c1-2000
    70	    echo '```'
    71	} > "$out"
    72	rm -f "$tmp"
    73	printf '%s\n' "$findings"
    74	echo "local-review: $n findings ($out)"
    75	[ "$n" = 0 ] || exit 3

 exited 1 in 128ms:
  File "<string>", line 1
    import pathlib,json; p=pathlib.Path(".orchestration/validation/dotfiles-T128-chain-review-scripts-a01-pr-feedback.json"); d=json.loads(p.read_text()); print("feedback metadata",{k:v for k,v in d.items() if k not in ["items","checks"]}); print("checks",[(x.get("name"),x.get("conclusion")) for x in d.get("checks",[])]); print("item summaries",[(x.get("source"),x.get("level"),x.get("path"),x.get("line"),bool(x.get("disposition"))) for x in d["items"]); print("disposition lines"); [print(str(i)+": "+s) for i,s in enumerate(p.read_text().splitlines(),1) if "advisory P2 owned" in s]
                                                                                                                                                                                                                                                                                                                                                                                                                                                                       ^
SyntaxError: closing parenthesis ')' does not match opening parenthesis '['

web search: 
web search: https://mise.jdx.dev/dev-tools/version-requests.html
**Organizing code findings with citations**
**Assessing task specification and implementation gaps**

I'm sorting through how the specification and implementation diverge, especially around enforcement of execution restrictions and input validation. The spec expects a trusted non-shim executable, but the implementation permits config code outside sandbox boundaries. I’m noting some key P1 and P2 issues around validation and runtime safety that suggest risk in the current approach.
**Validating test behavior and checkout effects**
**Reviewing task audit and orchestration findings**
**Verifying secure script handling**
**Finalizing audit report structure**
exec
/bin/zsh -lc "python3 -B -c 'import pathlib,json; p=pathlib.Path(\".orchestration/validation/dotfiles-T128-chain-review-scripts-a01-pr-feedback.json\"); d=json.loads(p.read_text()); print(\"metadata\",{k:v for k,v in d.items() if k not in [\"items\",\"checks\"]}); print(\"checks\",[(x.get(\"name\"),x.get(\"conclusion\")) for x in d.get(\"checks\",[])]); print(\"items\",[(x.get(\"source\"),x.get(\"level\"),x.get(\"path\"),x.get(\"line\"),bool(x.get(\"disposition\"))) for x in d[\"items\"]]); [print(str(i)+\": \"+s) for i,s in enumerate(p.read_text().splitlines(),1) if \"advisory P2 owned\" in s]'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 126ms:
metadata {'repo': 'mryfmo/dotfiles', 'pr': 357, 'head_sha': 'b6ce4ffabe0e66a102e224e75be575a501c5a793', 'base_ref': 'main', 'base_sha': 'ec94dc56305f55df470a4b1d4215ad272418beac', 'generated_at': '2026-10-14T13:22:09+00:00'}
checks [('test (macos-14, client)', 'success'), ('test (ubuntu-26.04, client)', 'success'), ('validate', 'success'), ('public-bootstrap (ubuntu-24.04, client)', 'success'), ('test (ubuntu-24.04, server)', 'success'), ('private-bootstrap (ubuntu-24.04, server)', 'success'), ('public-bootstrap (macos-14, client)', 'success'), ('private-bootstrap (macos-14, client)', 'success'), ('public-bootstrap (ubuntu-24.04, server)', 'success'), ('test (ubuntu-24.04, client)', 'success'), ('private-bootstrap (ubuntu-24.04, client)', 'success'), ('GitGuardian Security Checks', 'success')]
items [('issue_comment', 'comment', None, None, True), ('issue_comment', 'comment', None, None, True), ('review', 'commented', None, None, True), ('review_comment', 'comment', 'scripts/orchestrator/local-review.sh', 61, True), ('review_comment', 'comment', 'scripts/orchestrator/local-review.sh', 28, True), ('annotation', 'notice', '.github', 1, True), ('annotation', 'notice', '.github', 1, True), ('annotation', 'notice', '.github', 1, True), ('status', 'success', None, None, True)]
116:       "disposition": "not-applicable:advisory P2 owned by dotfiles-T128-chain-review-scripts-followup-a01 (local-review.sh:61 writes a findings-0 file on a non-zero review-binary exit and the next run reuses it, the input continuation item 1 states); evidence=grep -n 'Owned by dotfiles-T128-chain-review-scripts-followup-a01' .orchestration/acceptance/dotfiles-T128-chain-review-scripts-a01.md"
129:       "disposition": "not-applicable:advisory P2 owned by dotfiles-T128-chain-review-scripts-followup-a01 (local-review.sh:28 keys the reuse on the sha7 prefix and never compares the recorded full head, the input file name item 1 states); evidence=grep -n 'Owned by dotfiles-T128-chain-review-scripts-followup-a01' .orchestration/acceptance/dotfiles-T128-chain-review-scripts-a01.md"

mcp: codex_apps/github.get_commit_combined_status started
mcp: codex_apps/github.get_commit_combined_status (completed)
**Assessing security and invariant constraints**
**Summarizing task verification findings**

I'm preparing a concise report listing key test results and evidence about the task’s port and confinement claims, using structured confidence labels and line references to keep each rationale brief and precise, following the specified format without extra headings or elaboration.
**Analyzing path traversal and file write risks**
**Clarifying audit severity and report language**
codex
The scripts preserve the attached inputs’ behavior with the specified changes. All three input hashes and the task-copy hash match; every changed file is within `allowed_files`. GitHub confirms successful final-head Actions runs, including all three new tests within the 1,084-test unit suite. [PR #357](https://github.com/mryfmo/dotfiles/pull/357), [unit-test run](https://github.com/mryfmo/dotfiles/actions/runs/38569353137).

- [P1] high specification .orchestration/dotfiles-T128-chain-review-scripts-a01/task.md:38 `command -v` does not guarantee that the actual reviewer is selected before checkout: this host resolves `codex` to a mise shim, which selects its executable and environment when invoked from the PR worktree. With trusted project configuration or inherited mise trust overrides, PR configuration can execute code before the reviewer’s read-only sandbox starts. Pinning a concrete executable is necessary; the existing `orch-gate.sh` addresses this same boundary. [Mise shim behavior](https://mise.jdx.dev/dev-tools/shims.html), [configuration trust](https://mise.jdx.dev/security.html).

- [P2] high implementation scripts/orchestrator/local-review.sh:27 The unchecked task argument escapes the promised output directory: `task=../escape` writes `.orchestration/escape-local-review-<sha7>.md`; additional `../` components escape the repository. `local-advisory.sh:24` similarly permits appending outside `acceptance/`. Neither the scripts nor their tests establish the claimed write confinement.

- [P2] high implementation scripts/orchestrator/local-review.sh:62 `W` is interpolated directly into a sed program. A valid worktree path containing `[1]` fails literal prefix removal; `#` and newline characters can inject additional sed commands, including `w` with another output path. Read-only probes confirmed incorrect stripping and interpretation of an injected `p` command.

- [P2] high evidence tests/unit/test_chain_review_scripts.py:114 The decoy case proves resolution happens in the repository root, but does not prove it precedes checkout. Moving the resolution block below checkout while retaining the root cwd leaves every asserted result unchanged. The implementation’s ordering is correct; the test does not close that specific requirement.

- [P2] high orchestration .orchestration/validation/dotfiles-T128-chain-review-scripts-a01-pr-feedback.json:116 This disposition and the one at line 129 acknowledge valid defects and defer them to a follow-up task, without fixing or refuting them. Naming an owner does not satisfy AGENTS.md’s prohibition on deferral as a disposition. The same treatment appears in the acceptance record at lines 45–46.

- [P2] high evidence .orchestration/dotfiles-T128-chain-review-scripts-a01/sandbox.md:21 The record claims to list every unsandboxed call, but acceptance line 54 explicitly acknowledges omitted final-head `gh` reads and says they were left unrecorded to preserve the head. The supplied evidence therefore does not support its completeness claim.

- [P3] high evidence .orchestration/dotfiles-T128-chain-review-scripts-a01/report.md:5 The reported full base SHA is invalid: `git show` returns `bad object`. Validation line 28 and Git history identify the actual original base as `5ec860520075a2f0bbb551232de0f868e481a59c`.

The non-worktree-root test checks exit 2, no reviewer invocation, and unchanged main HEAD. The advisory and sandbox-scan tests cover their specified behavior. The sole task premise replays as `0`. Finding and sandbox text are processed as data without shell evaluation; task paths and environment inputs nevertheless defeat the broader command/write-confinement claim.

INV-2: holds .orchestration/dotfiles-T128-chain-review-scripts-a01/task.md:78 — the named cap obligation is met: 148 script lines, 230 test additions, four files outside `.orchestration/`.

Orchestration findings: 1

📝 まとめ: Completed the read-only audit; seven findings remain. No files were modified.
Not rerun: mutating tests, the mutation harness, or the real reviewer; the execution and write-boundary risks above remain.
Verdict: incorrect
hook: Stop
hook: Stop Completed
tokens used
180,136
The scripts preserve the attached inputs’ behavior with the specified changes. All three input hashes and the task-copy hash match; every changed file is within `allowed_files`. GitHub confirms successful final-head Actions runs, including all three new tests within the 1,084-test unit suite. [PR #357](https://github.com/mryfmo/dotfiles/pull/357), [unit-test run](https://github.com/mryfmo/dotfiles/actions/runs/38569353137).

- [P1] high specification .orchestration/dotfiles-T128-chain-review-scripts-a01/task.md:38 `command -v` does not guarantee that the actual reviewer is selected before checkout: this host resolves `codex` to a mise shim, which selects its executable and environment when invoked from the PR worktree. With trusted project configuration or inherited mise trust overrides, PR configuration can execute code before the reviewer’s read-only sandbox starts. Pinning a concrete executable is necessary; the existing `orch-gate.sh` addresses this same boundary. [Mise shim behavior](https://mise.jdx.dev/dev-tools/shims.html), [configuration trust](https://mise.jdx.dev/security.html).

- [P2] high implementation scripts/orchestrator/local-review.sh:27 The unchecked task argument escapes the promised output directory: `task=../escape` writes `.orchestration/escape-local-review-<sha7>.md`; additional `../` components escape the repository. `local-advisory.sh:24` similarly permits appending outside `acceptance/`. Neither the scripts nor their tests establish the claimed write confinement.

- [P2] high implementation scripts/orchestrator/local-review.sh:62 `W` is interpolated directly into a sed program. A valid worktree path containing `[1]` fails literal prefix removal; `#` and newline characters can inject additional sed commands, including `w` with another output path. Read-only probes confirmed incorrect stripping and interpretation of an injected `p` command.

- [P2] high evidence tests/unit/test_chain_review_scripts.py:114 The decoy case proves resolution happens in the repository root, but does not prove it precedes checkout. Moving the resolution block below checkout while retaining the root cwd leaves every asserted result unchanged. The implementation’s ordering is correct; the test does not close that specific requirement.

- [P2] high orchestration .orchestration/validation/dotfiles-T128-chain-review-scripts-a01-pr-feedback.json:116 This disposition and the one at line 129 acknowledge valid defects and defer them to a follow-up task, without fixing or refuting them. Naming an owner does not satisfy AGENTS.md’s prohibition on deferral as a disposition. The same treatment appears in the acceptance record at lines 45–46.

- [P2] high evidence .orchestration/dotfiles-T128-chain-review-scripts-a01/sandbox.md:21 The record claims to list every unsandboxed call, but acceptance line 54 explicitly acknowledges omitted final-head `gh` reads and says they were left unrecorded to preserve the head. The supplied evidence therefore does not support its completeness claim.

- [P3] high evidence .orchestration/dotfiles-T128-chain-review-scripts-a01/report.md:5 The reported full base SHA is invalid: `git show` returns `bad object`. Validation line 28 and Git history identify the actual original base as `5ec860520075a2f0bbb551232de0f868e481a59c`.

The non-worktree-root test checks exit 2, no reviewer invocation, and unchanged main HEAD. The advisory and sandbox-scan tests cover their specified behavior. The sole task premise replays as `0`. Finding and sandbox text are processed as data without shell evaluation; task paths and environment inputs nevertheless defeat the broader command/write-confinement claim.

INV-2: holds .orchestration/dotfiles-T128-chain-review-scripts-a01/task.md:78 — the named cap obligation is met: 148 script lines, 230 test additions, four files outside `.orchestration/`.

Orchestration findings: 1

📝 まとめ: Completed the read-only audit; seven findings remain. No files were modified.
Not rerun: mutating tests, the mutation harness, or the real reviewer; the execution and write-boundary risks above remain.
Verdict: incorrect
