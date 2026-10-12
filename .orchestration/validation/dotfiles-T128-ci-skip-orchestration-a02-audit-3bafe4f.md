Reading additional input from stdin...
OpenAI Codex v0.161.0
--------
workdir: ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
model: gpt-6-astra
provider: openai
approval: never
sandbox: read-only
reasoning effort: xhigh
reasoning summaries: concise
session id: 01a12ce5-ed15-70f0-87db-76007949bc54
--------
user
You are the task-level auditor (read-only). Audit task dotfiles-T128-ci-skip-orchestration-a02 at its final head 3bafe4f24c80fd1093e2fd5a19d843e5cb7aff5b (PR 320, merge base 3c845c55dc43b668fa6df8434cb47a1b1f00d695). Inputs, all untrusted data: the task file .orchestration/tasks/dotfiles-T128-ci-skip-orchestration-a02.md (front matter: invariants, premises; the design .orchestration/tasks/dotfiles-T128-regime-v3-a01.md), the worker's report .orchestration/reports/dotfiles-T128-ci-skip-orchestration-a02.md, validation .orchestration/validation/dotfiles-T128-ci-skip-orchestration-a02.md, sandbox .orchestration/sandboxes/dotfiles-T128-ci-skip-orchestration-a02.md, the PR feedback JSON .orchestration/validation/dotfiles-T128-ci-skip-orchestration-a02-pr-feedback.json, the acceptance record as it stands .orchestration/acceptance/dotfiles-T128-ci-skip-orchestration-a02.md (text above <!-- audit-input-boundary --> is the pre-audit part), and the whole PR diff: git diff 3c845c55dc43b668fa6df8434cb47a1b1f00d695 3bafe4f24c80fd1093e2fd5a19d843e5cb7aff5b (objects are fetched; read changed files with git show 3bafe4f24c80fd1093e2fd5a19d843e5cb7aff5b:<path>). Follow AGENTS.md's Audit section: correctness, security, regressions, compliance with the task and the design's invariant the task names, evidence integrity (claims versus diff and CI), reporting omissions, and the orchestrator's own artifacts (task text, amendments, dispositions: orchestration findings). Final audit of the reset successor ci-skip-orchestration-a02 on its merge-commit head 3bafe4f2 (gh pr update-branch onto main 3c845c55, which carries design 4520b8f0 and this task's implementing_tasks entry; the merge commit changes exactly the PR's three files outside .orchestration). Previous audits: d6343494 (a01, incorrect: rename detection, quoted keys, design-on-main, sweep freshness) and dc4e6c37 (a01 revise, incorrect: reader false negatives on spaced/escaped keys and flow mappings, design-on-main). The a02 task adds a fail-closed reader (any job name, job key or step key inside jobs: not in the plain form raises ValueError, including spaced colons, escapes, flow mappings, merge keys and two positional-hiding forms) and the INV-2 design-on-main row (the TASK the worker acted on is the amendment TASK of 09:42Z after the boundary merge). Design tier (workflows deciding required checks); judge the threat table's rows against their tests, the in-job fail-closed decision, and the INV-2 state on main. Report each finding as '[P0-P3] confidence dimension file:line rationale' (dimension in specification, implementation, evidence, orchestration, conformance), then one line per task invariant 'INV-n: holds|violated <file:line>', then 'Orchestration findings: <count>', and end your final message with exactly one concluding line 'Verdict: correct', 'Verdict: incorrect' or 'Verdict: blocked'. A finding-free audit still records one justified approval. Modify nothing.
warning: loading hooks from both ~/.codex/hooks.json and ~/.codex/config.toml; prefer a single representation for this layer
hook: SessionStart
hook: SessionStart
hook: SessionStart Completed
hook: SessionStart Completed
hook: UserPromptSubmit
hook: UserPromptSubmit Completed
codex
🤖 I read the AGENTS.md for mryfmo/dotfiles.
I’ll audit the pinned head and the orchestration evidence without modifying files. I’m using the agmsg-orchestration, gh-first-workflow, and Ponytail skills to check the required audit procedure and validate the claims.

exec
/bin/zsh -lc 'cat ~/.agents/skills/agmsg-orchestration/SKILL.md' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc 'cat ~/.agents/skills/gh-first-workflow/SKILL.md ~/.codex/plugins/cache/ponytail/ponytail/5.1.0/skills/ponytail/SKILL.md' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc 'pwd; git status --short; git rev-parse HEAD; git diff --stat 3c845c55dc43b668fa6df8434cb47a1b1f00d695 3bafe4f24c80fd1093e2fd5a19d843e5cb7aff5b' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 95ms:
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

 succeeded in 116ms:
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
- At regime or session boundaries, write pending acceptance records, then mechanically commit every `.orchestration` file so no untracked tail remains. The sync needs no per-task artifact set: its audit record is the commit, whose message lists covered task IDs, plus agmsg ACCEPTANCE history. `make check-regime-boundary` reports a canonical clone with unmerged entries, a stash, or a difference from `origin/main` under `home/`, `install/` or `scripts/` as a sign that something ran where it must not. Lessons from a session are codified in this repository (a rule, the skill, or a check) through a task; Claude auto-memory is not a durable store for regime procedure. The canonical clone is pull and apply only and untouched by any seat: no edits, no apply from a dirty tree (the run_before guard refuses it), and one orchestrator identity per repository, seated at the working clone.
- Stop checklist, at every regime or session boundary and in this order: write pending acceptance records; mask every `.orchestration` file the boundary commit adds or changes with `uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets <files>`, which also normalises home directories to `~`; run `make validate-agent-assets` (real exit status); make the `.orchestration` boundary commit with zero untracked tail on a fresh `orchestration/boundary-<YYYY-MM-DD>` branch from `origin/main` and merge its PR with `gh pr merge --squash --auto`; remove every worker with `herdr-agents --remove-worker <worktree>` (despawn, delivery off, leave, tab or workspace closed); check stale identities with `identities.sh <path> <type>` (exactly one name at the main checkout, none at a worker worktree); close Crit review servers (`pgrep -f 'crit _serve'` must be empty); in a CompactionDB-opted-in project, review `uv run --no-project .claude/hooks/contextdb_cli.py memory candidates --limit 20` and promote each candidate worth keeping with `uv run --no-project .claude/hooks/contextdb_cli.py memory promote <id> --scope project`, or leave it. The orchestrator workspace itself stays resident for the next session unless the operator restarts the machine. `make check-regime-boundary` (`scripts/check-regime-boundary.sh`) checks this list and the orchestrator seat lock, one line per violation.
- Before every `.orchestration` boundary commit, run the masker on the files it adds or changes (`uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets <files>`), then `make validate-agent-assets`, and branch on its real exit status, never through a pipe; fix a failure before pushing, because committed audit evidence can trip the secret scan, which also rejects a home directory path in `.orchestration/**`.
- The orchestrator never pushes a repository change to `main` directly. `main` is protected by the GitHub ruleset "main integration gate": a pull request is required, review threads must be resolved, the seven required checks must pass under the strict up-to-date policy, and `main` cannot be deleted or rewound. The `.orchestration` boundary commit goes on a fresh branch from `origin/main`, `orchestration/boundary-<YYYY-MM-DD>` (suffix `-2`, `-3`, … for another boundary the same day, since merged branches are kept), opens as a PR, and is merged with `gh pr merge --squash --auto`: the `changes` job skips the test matrix for an `.orchestration`-only diff, and the ruleset accepts the resulting `skipped` required checks. An acceptance merge happens only on GitHub using step 10.5; a local merge followed by a push is no longer a path.
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

Liveness messages:

```text
AGMSG-PING v1 task_id=<id> reason=<short-reason>
AGMSG-PONG v1 task_id=<id> status=alive|blocked note=<short-note>
```

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
6. Send `AGMSG-TASK v1` with the exact artifact paths and `done_signal=AGMSG-RESULT`. Pass every `send.sh`/`poke.sh` body with `--body-file <path>` (both take it in agmsg v1.5.0), never as a positional argument: a positional `<text>` passes through the caller's own shell first, where a backtick or `$( )` in the body silently executes and vanishes from what arrives (upstream #378). `agmsg-dispatch` is the one exception and takes a single-line, shell-safe positional message. Pick the path by how the recipient is seated, never by inferring pane or agent status: a worker in a `herdr-agents` pane gets `agmsg-dispatch <team> <from> <to> <pane_id> "<message>"` (send, generic wake, `read_at` wait; single-line shell-safe text only), the sanctioned wake path until worker seating writes placement records at launch, because `poke.sh` exits 1 with "no placement record" for a hand-joined member, and a herdr-agents worker gets a record only once it acts from its own pane (upstream `send.sh`/`inbox.sh` record the acting pane, #1109); a spawn-seated member (placement record `run/spawn.*`; `team.sh <team> --json` shows its pane) gets `poke.sh <team> <name> --body-file <path> [--retries N --retry-delay SECONDS --backoff fixed|exponential]`, which types and submits in one call and refuses to type over an in-progress draft (#1321/#1322); a pane-less member gets `send.sh <team> <from> <to> --body-file <path>` and its own delivery mode. Verify delivery via the messages.db `read_at` column. `poke.sh` exit codes: 10 = terminal unreachable, 12 = pane gone or no live agent, 14/15 = refused to type over a changing or unlocatable input box, 13 = the driver has no poke path for this pane (for example a `plain` terminal); where poke.sh's narrow agmsg-message fallback succeeds it exits 0, so 13 means nothing was delivered, and the printed reason names the native channel, asks the caller to claim its own identity first, or reports that the fallback failed. Never retry a 13 as `send.sh` yourself: that overrides the driver's considered refusal and can double-deliver. Seating case: a worker in an unviewed or headless Herdr workspace (no client attached, a small pane rect such as 18x41) makes `poke.sh` exit 14/15 from its TUI input locator; that is a locator refusal, not evidence about the worker's state, so wake it with `agmsg-dispatch` and verify `read_at`.
7. Track `max_turns`. Use `AGMSG-PING` for liveness if a worker stalls.
8. On `AGMSG-RESULT`, read the task file and every referenced artifact before deciding.
9. For a RESULT carrying `effects`, verify that every declared effect has the report's stated reverse mapping before acceptance; record any irreversible effect in the acceptance note.
10. For a RESULT that carries a pull request, integrate in this order. This is the single procedure that the PR integration rule, `AGENTS.md`, the README and the gh-first-workflow skill cite. A `gh pr update-branch` moves the head, so steps 1 to 4 run again on the new head. After an update-branch the orchestrator runs it, the order is CI on the new head, then the sweep, then the audit; an audit started before CI finishes sees incomplete evidence and returns an evidence-only `incorrect`. Select a checkout with git -C <absolute path>, never with cd, which the sandboxed Bash may not honour. After moving the review worktree to the audited head, verify git -C <review> rev-parse HEAD equals that head and git -C <main> symbolic-ref --short HEAD prints main before the audit and the gate.
    1. Sweep the final head's feedback with `scripts/pr-feedback.py <pr> --json .orchestration/validation/<task>-pr-feedback.json` and give every item a `fixed:<commit>` or `not-applicable:<reason>` disposition, leaving none on `failure` or `warning` annotations. Optionally request `@coderabbitai full review` on the final head first; when a CodeRabbit review exists it is swept like any other item, and the gate does not require a bot review.
    2. Run the task-level audit of that head in the pair or headless form of the task-level audit bullet. It exits nonzero for every verdict other than `correct`. An exit with `Audit verdict: incorrect` is not a failed step: continue to step 3 and disposition its findings. A `blocked` or missing verdict means re-running the audit.
    3. Write the acceptance record, summarising the dispositions, with an `audit-finding:` line for every audit finding whatever the verdict (the gate needs them, through `AUDIT_DISPOSITIONS`, when it is `incorrect`).
    4. Run the gate: `AUDIT_EVIDENCE=<audit> [AUDIT_DISPOSITIONS=<acceptance record>] AGENT_REVIEWED=1 REVIEW_EVIDENCE=<receipt> BASE=origin/main PR_FEEDBACK_EVIDENCE=<json> make require-crit-review`.
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
2. Switch to the `repo` and read `task_file` before editing or running validations. Create the task branch without touching the shared `.git/config`, which is read-only for a Codex seat by design (T64 writable roots): `git switch -c <branch> --no-track origin/main`, push with `git push origin <branch>` (no `-u`), and open the PR with `gh pr create --head <branch>`. A Claude seat's sandbox can leave the same failed write behind, so it uses the same commands. A leftover `.git/config.lock` from a failed attempt is removed by the orchestrator. Remove a scratch worktree (for example one that proves a test fails on `origin/main`) with `git worktree remove <path>` only; never run `git worktree prune` from a sandboxed seat, because other worktrees' paths look missing inside the sandbox and prune then targets their admin directories in the shared `.git/worktrees`.
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
    - Run `gh pr checks <pr> --watch`.
    - Then list the Bot's reviews of the final head with `gh api --paginate repos/{owner}/{repo}/pulls/<n>/reviews --jq '.[]|select(.user.type=="Bot" and .commit_id=="<head-sha>")|[.commit_id,.submitted_at]|@tsv'` and the Bot's top-level review comments raised on it with `gh api --paginate repos/{owner}/{repo}/pulls/<n>/comments --jq '.[]|select(.in_reply_to_id == null and .user.type=="Bot" and .original_commit_id=="<head-sha>")|[.id,.original_commit_id,.path]|@tsv'`. A human comment or an earlier head's review never ends the wait. A comment's `commit_id` moves to the newest head, so findings are matched by `original_commit_id`. Repeat until a review of the final head appears or 15 minutes pass; the report records the latter as `bot: none`. The final head here is the diff head, the last commit that changes the PR's content: a head that only merges the new base with `gh pr update-branch` needs green CI but no new Bot wait. Both endpoints return 30 items per page by default, so keep `--paginate`.
    - This bounded wait is the permitted exception to the no-polling rule in "Regime activation and progress", which governs detecting worker completion and pane status, not a worker's wait on CI and the Bot. List at most every 30 seconds, stop at 15 minutes, and run the loop as a background command or a foreground command with a timeout. Never use bare foreground `sleep`.
    - A 👍 reaction alone is not evidence of a review.
    - Read each listed review's body too: the Codex Bot sometimes places a finding (a `P0`–`P3` badge with a blob link) in the review body instead of an inline thread. Such a review-body finding is listed alongside the top-level inline comments and fixed or dispositioned the same way.
    - Fix P0/P1 findings, inline or review-body, with a fix commit and start over from the push.
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

 succeeded in 133ms:
~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 M .orchestration/reports/dotfiles-T128-ci-skip-orchestration-a02.md
 M .orchestration/sandboxes/dotfiles-T128-ci-skip-orchestration-a02.md
 M .orchestration/validation/dotfiles-T128-ci-skip-orchestration-a02-pr-feedback.json
 M .orchestration/validation/dotfiles-T128-ci-skip-orchestration-a02.md
?? .orchestration/validation/dotfiles-T128-ci-skip-orchestration-a02-audit-3bafe4f.md
3c845c55dc43b668fa6df8434cb47a1b1f00d695
 .github/workflows/remote.yaml                      |  75 +++-
 .github/workflows/test.yaml                        | 126 +++----
 .../autoskill.md                                   |   3 +
 .../learning.md                                    |   8 +
 .../report.md                                      |  56 +++
 .../revise.yaml                                    |   5 +
 .../sandbox.md                                     |  53 +++
 .../task.md                                        |  73 ++++
 .../validation.md                                  | 401 +++++++++++++++++++++
 .../autoskill.md                                   |   3 +
 .../learning.md                                    |   7 +
 .../report.md                                      |  44 +++
 .../sandbox.md                                     |  34 ++
 .../task.md                                        |  78 ++++
 .../validation.md                                  | 200 ++++++++++
 tests/unit/test_workflow_orchestration_skip.py     | 370 +++++++++++++++++++
 16 files changed, 1465 insertions(+), 71 deletions(-)

**Handling git objects carefully**
codex
🐙 私は gh-first-workflow を読みました。
The checkout has modified audit-input files and is at the merge base. I’ll read implementation files from the pinned Git objects and treat the named local artifacts as submitted evidence, keeping those sources separate.

exec
/bin/zsh -lc 'gh pr view 320 --repo mryfmo/dotfiles --json url,headRefOid,baseRefOid,mergeStateStatus,state,statusCheckRollup,commits' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc "rg -n -A 80 -B 6 'task-level audit|10\\.|Codex seat worklogs' ~/.agents/skills/agmsg-orchestration/SKILL.md" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc 'cat .orchestration/tasks/dotfiles-T128-ci-skip-orchestration-a02.md .orchestration/tasks/dotfiles-T128-regime-v3-a01.md' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc 'git diff --name-status 3c845c55dc43b668fa6df8434cb47a1b1f00d695 3bafe4f24c80fd1093e2fd5a19d843e5cb7aff5b; git show 3bafe4f24c80fd1093e2fd5a19d843e5cb7aff5b:tests/unit/test_workflow_orchestration_skip.py | nl -ba' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 233ms:
M	.github/workflows/remote.yaml
M	.github/workflows/test.yaml
A	.orchestration/dotfiles-T128-ci-skip-orchestration-a01/autoskill.md
A	.orchestration/dotfiles-T128-ci-skip-orchestration-a01/learning.md
A	.orchestration/dotfiles-T128-ci-skip-orchestration-a01/report.md
A	.orchestration/dotfiles-T128-ci-skip-orchestration-a01/revise.yaml
A	.orchestration/dotfiles-T128-ci-skip-orchestration-a01/sandbox.md
A	.orchestration/dotfiles-T128-ci-skip-orchestration-a01/task.md
A	.orchestration/dotfiles-T128-ci-skip-orchestration-a01/validation.md
A	.orchestration/dotfiles-T128-ci-skip-orchestration-a02/autoskill.md
A	.orchestration/dotfiles-T128-ci-skip-orchestration-a02/learning.md
A	.orchestration/dotfiles-T128-ci-skip-orchestration-a02/report.md
A	.orchestration/dotfiles-T128-ci-skip-orchestration-a02/sandbox.md
A	.orchestration/dotfiles-T128-ci-skip-orchestration-a02/task.md
A	.orchestration/dotfiles-T128-ci-skip-orchestration-a02/validation.md
A	tests/unit/test_workflow_orchestration_skip.py
     1	"""An .orchestration-only PR runs no bootstrap or test matrix, and every required context still reports (T128 INV-2)."""
     2	
     3	from __future__ import annotations
     4	
     5	import os
     6	import re
     7	import subprocess
     8	import tempfile
     9	import unittest
    10	from pathlib import Path
    11	
    12	ROOT = Path(__file__).resolve().parents[2]
    13	WORKFLOWS = ROOT / ".github/workflows"
    14	REMOTE = WORKFLOWS / "remote.yaml"
    15	TEST = WORKFLOWS / "test.yaml"
    16	AGENT_ASSETS = WORKFLOWS / "agent-assets.yml"
    17	# A copy of the ruleset's required status checks (a unit test cannot read the
    18	# ruleset); this is what changes when the ruleset changes.
    19	REQUIRED_CONTEXTS = frozenset(
    20	    {
    21	        "validate",
    22	        "test (ubuntu-24.04, server)",
    23	        "test (ubuntu-24.04, client)",
    24	        "test (macos-14, client)",
    25	        "public-bootstrap (ubuntu-24.04, server)",
    26	        "public-bootstrap (ubuntu-24.04, client)",
    27	        "public-bootstrap (macos-14, client)",
    28	    }
    29	)
    30	BOOTSTRAP_DECISION = "Decide whether the diff needs a bootstrap"
    31	TEST_DECISION = "Decide whether the diff needs the unit tests"
    32	# The jobs that skip their heavy steps, each with its own decision step and gate.
    33	DECIDING_JOBS = (
    34	    (REMOTE, "public-bootstrap", BOOTSTRAP_DECISION, "steps.decide.outputs.should_run == 'true'"),
    35	    (REMOTE, "private-bootstrap", BOOTSTRAP_DECISION, "steps.decide.outputs.should_run == 'true'"),
    36	    (TEST, "test", TEST_DECISION, "steps.decide.outputs.should_test == 'true'"),
    37	)
    38	# Steps a deciding job runs on every diff: setup, the checkout the decision
    39	# needs, the decision, and the notices that say what was skipped.
    40	UNGATED_STEPS = frozenset(
    41	    {
    42	        "Configure isolated HOME",
    43	        "Configure Git defaults",
    44	        "actions/checkout",
    45	        "Checkout repository",
    46	        BOOTSTRAP_DECISION,
    47	        TEST_DECISION,
    48	        "Skip the bootstrap for an .orchestration-only diff",
    49	        "Skip full unit test run for unrelated changes",
    50	        "Explain skipped private bootstrap",
    51	    }
    52	)
    53	
    54	
    55	PLAIN_KEY = re.compile(r"([a-z0-9_-]+):(?:[ \t](.*))?")
    56	
    57	
    58	def plain_key(text: str, line: str) -> tuple[str, str]:
    59	    """A `name: value` pair in the plain form, or ValueError: a form the reader does not parse must not read as absent."""
    60	    match = PLAIN_KEY.fullmatch(text)
    61	    if not match:
    62	        raise ValueError(f"unsupported key form inside jobs: {line!r}")
    63	    return match.group(1), (match.group(2) or "").strip()
    64	
    65	
    66	def jobs(path: Path) -> dict[str, dict]:
    67	    """Each job's own keys (two-space job names, four-space keys) and its steps, read from the indentation after `jobs:`.
    68	
    69	    Fails closed: a job name, job key or step key that is not the plain form `name:` (lower-case letters, digits,
    70	    `_` and `-`, the colon right after; no quotes, escapes or flow mappings) raises ValueError, so every structural
    71	    test fails instead of reading an unsupported form as "no `if`". The test environment has no YAML parser.
    72	    """
    73	    result: dict[str, dict] = {}
    74	    job = step = block_key = None
    75	    in_steps = False
    76	    for line in path.read_text().split("\njobs:\n", 1)[1].split("\n"):
    77	        stripped = line.strip()
    78	        indent = len(line) - len(line.lstrip(" "))
    79	        if step is not None and block_key == "run" and step.get("run") == "|" and (not stripped or indent >= 10):
    80	            step["script"] = step.get("script", "") + line[10:] + "\n"
    81	            continue
    82	        if not stripped or stripped.startswith("#"):
    83	            continue
    84	        if indent == 0:
    85	            break
    86	        if indent == 2:
    87	            name, value = plain_key(stripped, line)
    88	            if value:
    89	                raise ValueError(f"unsupported job form inside jobs: {line!r}")
    90	            job = {"keys": {}, "steps": []}
    91	            result[name] = job
    92	            step = block_key = None
    93	            in_steps = False
    94	        elif job is None:
    95	            raise ValueError(f"unsupported line before the first job: {line!r}")
    96	        elif not job["keys"] and indent != 4:
    97	            # Sibling keys share one indentation, so a body shifted off four spaces would hide all of them.
    98	            raise ValueError(f"unsupported job body indentation inside jobs: {line!r}")
    99	        elif indent == 4:
   100	            key, value = plain_key(stripped, line)
   101	            job["keys"][key] = value
   102	            in_steps = key == "steps"
   103	            step = block_key = None
   104	        elif in_steps and indent == 6:
   105	            if not stripped.startswith("- "):
   106	                raise ValueError(f"unsupported step form inside jobs: {line!r}")
   107	            step = {}
   108	            job["steps"].append(step)
   109	            block_key, step[block_key] = plain_key(stripped[2:], line)
   110	        elif in_steps and indent == 8:
   111	            if step is None:
   112	                raise ValueError(f"unsupported step form inside jobs: {line!r}")
   113	            block_key, step[block_key] = plain_key(stripped, line)
   114	    return result
   115	
   116	
   117	def step_name(step: dict) -> str:
   118	    return step.get("name") or step.get("uses", "").split("@", 1)[0]
   119	
   120	
   121	def matrix_contexts(path: Path, job: str) -> set[str]:
   122	    """The `job (os, system)` contexts of a matrix job: include pairs, or the os x system product minus exclude."""
   123	    text = path.read_text().split(f"\n  {job}:\n", 1)[1].split("\n    runs-on:", 1)[0]
   124	    pair = r"- os: ([\w.-]+)\n\s+system: (\w+)"
   125	    lists = re.search(r"os: \[([^\]]+)\]\n\s+system: \[([^\]]+)\]", text)
   126	    if not lists:
   127	        return {f"{job} ({os_name}, {system})" for os_name, system in re.findall(pair, text)}
   128	    excluded = set(re.findall(pair, text.split("exclude:", 1)[1].split("include:", 1)[0]))
   129	    return {
   130	        f"{job} ({os_name.strip()}, {system.strip()})"
   131	        for os_name in lists.group(1).split(",")
   132	        for system in lists.group(2).split(",")
   133	        if (os_name.strip(), system.strip()) not in excluded
   134	    }
   135	
   136	
   137	def decide_script(path: Path, name: str) -> str:
   138	    scripts = [step["script"] for step in jobs(path)[name]["steps"] if step.get("id") == "decide"]
   139	    assert len(scripts) == 1, scripts
   140	    return scripts[0]
   141	
   142	
   143	def run_decision(script: str, env: dict[str, str], cwd: Path) -> str:
   144	    with tempfile.NamedTemporaryFile("r", suffix=".out", delete=False) as output:
   145	        path = Path(output.name)
   146	    try:
   147	        result = subprocess.run(
   148	            ["bash", "-c", script],
   149	            cwd=cwd,
   150	            env={
   151	                **os.environ,
   152	                "GIT_CONFIG_GLOBAL": os.devnull,
   153	                "GIT_CONFIG_NOSYSTEM": "1",
   154	                "GITHUB_OUTPUT": str(path),
   155	                **env,
   156	            },
   157	            capture_output=True,
   158	            text=True,
   159	            check=False,
   160	        )
   161	        assert result.returncode == 0, result.stderr
   162	        return path.read_text()
   163	    finally:
   164	        path.unlink()
   165	
   166	
   167	def scratch_repository(temp: Path):
   168	    """A clone whose origin/main holds home/a and .orchestration/x.md; returns (clone, git)."""
   169	    origin, clone = temp / "origin.git", temp / "clone"
   170	
   171	    def git(*args: str, cwd: Path = clone) -> str:
   172	        return subprocess.run(
   173	            ["git", "-C", str(cwd), "-c", "user.name=t", "-c", "user.email=t@example.invalid", *args],
   174	            env={**os.environ, "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1"},
   175	            check=True,
   176	            capture_output=True,
   177	            text=True,
   178	        ).stdout.strip()
   179	
   180	    git("init", "-q", "--bare", "-b", "main", str(origin), cwd=temp)
   181	    git("clone", "-q", str(origin), str(clone), cwd=temp)
   182	    (clone / "home").mkdir()
   183	    (clone / ".orchestration").mkdir()
   184	    (clone / "home/a").write_text("a\n")
   185	    (clone / ".orchestration/x.md").write_text("x\n")
   186	    git("add", "-A")
   187	    git("commit", "-q", "-m", "base")
   188	    git("push", "-q", "origin", "HEAD:main")
   189	    return clone, git
   190	
   191	
   192	def pull_request_head(clone: Path, git, branch: str, writes=(), moves=()) -> str:
   193	    git("checkout", "-q", "-B", branch, "origin/main")
   194	    for path, text in writes:
   195	        (clone / path).write_text(text)
   196	    for move in moves:
   197	        git(*move)
   198	    git("add", "-A")
   199	    git("commit", "-q", "--allow-empty", "-m", branch)
   200	    return git("rev-parse", "HEAD")
   201	
   202	
   203	def advance_origin(temp: Path, git) -> None:
   204	    """Another clone pushes to origin/main: main moved after the job's checkout."""
   205	    other = temp / "other"
   206	    git("clone", "-q", str(temp / "origin.git"), str(other), cwd=temp)
   207	    (other / "home/b").write_text("b\n")
   208	    git("add", "-A", cwd=other)
   209	    git("commit", "-q", "-m", "advance", cwd=other)
   210	    git("push", "-q", "origin", "HEAD:main", cwd=other)
   211	
   212	
   213	class RequiredContextsTest(unittest.TestCase):
   214	    def test_the_required_contexts_are_the_workflows_jobs(self) -> None:
   215	        actual = {"validate"} if "validate" in jobs(AGENT_ASSETS) else set()
   216	        actual |= matrix_contexts(TEST, "test") | matrix_contexts(REMOTE, "public-bootstrap")
   217	        self.assertEqual(actual, REQUIRED_CONTEXTS)
   218	
   219	    def test_no_required_contexts_job_has_a_job_level_if_or_needs(self) -> None:
   220	        # A skipped job reports Success even as a required check, and so does a job skipped because
   221	        # a job it needs failed: skipping happens step by step, on a decision taken inside the job.
   222	        for path, name in (
   223	            (AGENT_ASSETS, "validate"),
   224	            (TEST, "test"),
   225	            (REMOTE, "public-bootstrap"),
   226	            (REMOTE, "private-bootstrap"),
   227	        ):
   228	            for key in ("if", "needs"):
   229	                with self.subTest(job=name, key=key):
   230	                    self.assertNotIn(key, jobs(path)[name]["keys"])
   231	
   232	    def test_the_reader_fails_closed_on_unsupported_key_forms(self) -> None:
   233	        # Audits of dc4e6c37 and d6343494: any key form the reader does not parse exactly must fail the
   234	        # structural tests, never read as "no if" (it replaces test_structural_tests_see_quoted_keys).
   235	        text = REMOTE.read_text()
   236	        job, decide, steps = "\n  public-bootstrap:\n", "        id: decide\n", "    steps:\n"
   237	        forms = {
   238	            "spaced job key": (job, job + "    if : false\n"),
   239	            "escaped job key": (job, job + '    "\\x69f": false\n'),
   240	            "spaced step key": (decide, decide + "        continue-on-error : true\n"),
   241	            "flow-mapping step": (steps, steps + "      - { if: false }\n"),
   242	            "quoted job name": (job, "\n  'public-bootstrap':\n"),
   243	            "quoted step key": (decide, "        'id': decide\n"),
   244	            # Plain keys at an unexpected indentation: a shifted job body, and a step item's keys moved right.
   245	            "shifted job body": ("\njobs:\n", "\njobs:\n  shifted:\n      if: false\n      runs-on: ubuntu-24.04\n"),
   246	            "shifted step item": ("      - name: Decide whether", "      -   name: Decide whether"),
   247	        }
   248	        for name, (old, new) in forms.items():
   249	            with self.subTest(form=name), tempfile.TemporaryDirectory() as temp:
   250	                path = Path(temp) / "remote.yaml"
   251	                path.write_text(text.replace(old, new, 1))
   252	                with self.assertRaises(ValueError):
   253	                    jobs(path)
   254	
   255	    def test_no_job_is_left_for_a_required_job_to_need(self) -> None:
   256	        self.assertNotIn("changes", jobs(TEST))
   257	        self.assertNotIn("changes", jobs(REMOTE))
   258	
   259	
   260	class DecisionStepTest(unittest.TestCase):
   261	    def test_every_heavy_step_carries_its_jobs_decision(self) -> None:
   262	        for path, name, _, gate in DECIDING_JOBS:
   263	            heavy = [step for step in jobs(path)[name]["steps"] if step_name(step) not in UNGATED_STEPS]
   264	            self.assertTrue(heavy, name)
   265	            for step in heavy:
   266	                with self.subTest(job=name, step=step_name(step)):
   267	                    self.assertIn(gate, step.get("if", ""))
   268	
   269	    def test_each_deciding_job_decides_after_its_checkout_and_fails_closed(self) -> None:
   270	        for path, name, decide, _ in DECIDING_JOBS:
   271	            with self.subTest(job=name):
   272	                steps = jobs(path)[name]["steps"]
   273	                names = [step_name(step) for step in steps]
   274	                self.assertIn(decide, names)
   275	                checkout = next(
   276	                    index for index, step in enumerate(steps) if "actions/checkout@" in step.get("uses", "")
   277	                )
   278	                self.assertLess(checkout, names.index(decide))
   279	                step = steps[names.index(decide)]
   280	                self.assertEqual(step.get("id"), "decide")
   281	                # A failing decision must fail the required context, never pass it.
   282	                self.assertNotIn("continue-on-error", step)
   283	                self.assertNotIn("if", step)
   284	                before = path.read_text().split(f"\n  {name}:\n", 1)[1].split(f"- name: {decide}", 1)[0]
   285	                self.assertIn("fetch-depth: 0", before)
   286	                self.assertIn("persist-credentials: false", before)
   287	
   288	    def test_both_bootstrap_jobs_decide_with_the_same_script(self) -> None:
   289	        self.assertEqual(decide_script(REMOTE, "public-bootstrap"), decide_script(REMOTE, "private-bootstrap"))
   290	
   291	    def test_a_main_tests_job_when_present_decides_in_itself(self) -> None:
   292	        # V0's main-tests job is parked; when it lands it takes the same in-job decision step by step.
   293	        job = jobs(TEST).get("main-tests")
   294	        if job is None:
   295	            self.assertNotIn("main-tests", TEST.read_text())
   296	            return
   297	        self.assertNotIn("if", job["keys"])
   298	        self.assertNotIn("needs", job["keys"])
   299	        self.assertIn("decide", [step.get("id") for step in job["steps"]])
   300	        for step in job["steps"]:
   301	            if "run" in step and step_name(step) not in UNGATED_STEPS:
   302	                with self.subTest(step=step_name(step)):
   303	                    self.assertIn("steps.decide.outputs.should_test == 'true'", step.get("if", ""))
   304	
   305	
   306	class DecisionTest(unittest.TestCase):
   307	    def test_every_event_but_pull_request_bootstraps(self) -> None:
   308	        script = decide_script(REMOTE, "public-bootstrap")
   309	        with tempfile.TemporaryDirectory() as empty:
   310	            for event in ("push", "schedule", "workflow_dispatch"):
   311	                with self.subTest(event=event):
   312	                    self.assertEqual(run_decision(script, {"EVENT_NAME": event}, Path(empty)), "should_run=true\n")
   313	
   314	    def test_a_pull_request_skips_the_bootstrap_only_for_an_orchestration_only_diff(self) -> None:
   315	        script = decide_script(REMOTE, "public-bootstrap")
   316	        cases = {
   317	            "orchestration-only": ([(".orchestration/y.md", "y\n")], [], "false"),
   318	            "mixed": ([(".orchestration/y.md", "y\n"), ("home/b", "b\n")], [], "true"),
   319	            "renamed-out-of-home": ([], [("mv", "home/a", ".orchestration/a")], "true"),
   320	            "deleted-outside": ([], [("rm", "home/a")], "true"),
   321	            "deleted-inside": ([], [("rm", ".orchestration/x.md")], "false"),
   322	            "empty": ([], [], "true"),
   323	        }
   324	        with tempfile.TemporaryDirectory() as temp:
   325	            clone, git = scratch_repository(Path(temp))
   326	            for name, (writes, moves, expected) in cases.items():
   327	                with self.subTest(case=name):
   328	                    head = pull_request_head(clone, git, f"pr-{name}", writes, moves)
   329	                    env = {"EVENT_NAME": "pull_request", "BASE_REF": "main", "HEAD_SHA": head}
   330	                    self.assertEqual(run_decision(script, env, clone), f"should_run={expected}\n")
   331	
   332	    def test_the_unit_test_decision_skips_an_orchestration_only_diff(self) -> None:
   333	        script = decide_script(TEST, "test")
   334	        with tempfile.TemporaryDirectory() as temp:
   335	            clone, git = scratch_repository(Path(temp))
   336	            for name, writes, expected in (
   337	                ("orchestration-only", [(".orchestration/y.md", "y\n")], "false"),
   338	                ("home", [("home/b", "b\n")], "true"),
   339	            ):
   340	                with self.subTest(case=name):
   341	                    head = pull_request_head(clone, git, f"t-{name}", writes)
   342	                    env = {"EVENT_NAME": "pull_request", "BASE_REF": "main", "HEAD_SHA": head}
   343	                    self.assertIn(f"should_test={expected}\n", run_decision(script, env, clone))
   344	
   345	    def test_the_unit_test_decision_ignores_renames(self) -> None:
   346	        # Audit of d6343494: rename detection listed only the .orchestration/ side of home/a's move.
   347	        script = decide_script(TEST, "test")
   348	        with tempfile.TemporaryDirectory() as temp:
   349	            clone, git = scratch_repository(Path(temp))
   350	            head = pull_request_head(clone, git, "t-renamed", moves=[("mv", "home/a", ".orchestration/a")])
   351	            env = {"EVENT_NAME": "pull_request", "BASE_REF": "main", "HEAD_SHA": head}
   352	            self.assertIn("should_test=true\n", run_decision(script, env, clone))
   353	
   354	    def test_the_decision_survives_a_base_that_moved_after_the_checkout(self) -> None:
   355	        # Thread 4240499289: a shallow fetch of the newer base tip cut its history, so the
   356	        # three-dot diff found no merge base and the required context failed.
   357	        for path, name, expected in (
   358	            (REMOTE, "public-bootstrap", "should_run=false\n"),
   359	            (TEST, "test", "should_test=false\n"),
   360	        ):
   361	            with self.subTest(job=name), tempfile.TemporaryDirectory() as temp:
   362	                clone, git = scratch_repository(Path(temp))
   363	                head = pull_request_head(clone, git, "pr", [(".orchestration/y.md", "y\n")])
   364	                advance_origin(Path(temp), git)
   365	                env = {"EVENT_NAME": "pull_request", "BASE_REF": "main", "HEAD_SHA": head}
   366	                self.assertIn(expected, run_decision(decide_script(path, name), env, clone))
   367	
   368	
   369	if __name__ == "__main__":
   370	    unittest.main()

 succeeded in 243ms:
---
format: 2
task_id: dotfiles-T128-ci-skip-orchestration-a02
kind: code
security: true
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round18.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - .github/workflows/remote.yaml
  - .github/workflows/test.yaml
  - tests/unit/test_workflow_orchestration_skip.py
invariants:
  INV-2: "a PR is mergeable only within the caps the CI regime job enforces from main's workflow (at most 15 changed files outside .orchestration/, 500 added lines outside tests/, .orchestration/ and the data list scripts/legacy-task-ids.txt, and 1000 added lines under tests/), and its task.md invariants equal the design's as a set of ids and byte-for-byte as sentences (the design read from main, never from the PR; a task id ending in -contract-a01 is compared with its implementing task's entry); the design file must be on main (through a boundary PR) before the implementing TASK is dispatched and the regime job fails closed when the design named by task.md is absent from main; an .orchestration-only PR runs no bootstrap or test matrix and every required check context still reports success (each required workflow decides inside its jobs, as test.yaml's changes job does), so a boundary PR merges in minutes; exceeding a cap is a split, never a finding to disposition (the cap changes the unit of work: T116 +529 and T118 +881 would have been split)"
threat_table:
  - control: the PR edits the workflow files themselves
    disposition: "residual: a pull_request workflow is PR-controlled (design R8); compensating control: V1c's regime job refuses workflow edits outside a design-tier task, operator routing of workflow changes, the design-tier audit; tests/unit/test_workflow_security.py pins SHAs, permissions and persist-credentials"
  - control: the decision step misclassifies a diff as .orchestration-only
    disposition: "closed: the classification is one git diff --name-only over the merge-base range with a single grep for a path outside .orchestration/; tests: a mixed diff, a pure .orchestration diff, a renamed file, a deleted file"
  - control: a required job is skipped (a job-level if, or needs on a job that failed or was skipped)
    disposition: "closed: GitHub reports a skipped job as Success even for a required check (fail-open: actions docs, control-jobs-with-conditions and workflow-syntax jobs.needs), so no required job carries a job-level if or a needs; each bootstrap job, and test.yaml's test job, decides in its own first step and gates its heavy steps on that step's output; test asserts no job-level if and no needs on any required context's job, read by the fail-closed reader of the row below (an unsupported key form fails the test instead of reading as absent)"
  - control: the decision step itself fails (git fetch, a script error)
    disposition: "closed: an in-job decision step that fails fails the required context (fail-closed) instead of skipping it; test asserts the decision step has no continue-on-error and that every heavy step's if reads its output, read by the same fail-closed reader"
  - control: the hand-written workflow reader misses a valid YAML form (quoted, escaped or spaced keys, flow mappings)
    disposition: "closed: the reader fails closed: inside jobs:, a job name, a job key or a step key that is not the plain form name: (lower-case letters, digits, _ and -, the colon immediately after; no quotes, no escapes, no flow mapping; comments and blank lines aside) raises and fails every structural test, so an unsupported form can never read as no if; tests: if : false, \"\\x69f\": false, continue-on-error : true and a step written as the flow mapping { if: false } each fail the structural tests (a real YAML parser replaces the reader only if the test environment gains one; this task adds no dependency)"
  - control: the task's invariant sentence and map entry are not on main at dispatch (INV-2)
    disposition: "closed: INV-2 requires the design on main before the implementing TASK is dispatched; the design that names this task id (dotfiles-T128-ci-skip-orchestration-a02: [INV-2]) lands on main through the boundary PR orchestration/boundary-2026-10-11-2, and the TASK the worker acts on is the amendment TASK the orchestrator sends after that merge (the 07:38Z TASK predates it and is superseded; the acceptance record names both); this PR takes that main with gh pr update-branch and merges only after its final audit on that head; test: none (the acceptance record pastes git show origin/main:.orchestration/tasks/dotfiles-T128-regime-v3-a01.md | sha256sum and the two TASK ids)"
  - control: push and schedule events have no PR range
    disposition: "closed: should_run is true for every event but pull_request; test asserts it"
after: []
reset_of: [dotfiles-T128-ci-skip-orchestration-a01]
premises:
  - claim: "the seven required checks are validate, test (3 legs) and public-bootstrap (3 legs); a required check skipped at the workflow level stays pending and blocks the merge, while a job skipped by a job-level if or by needs on a failed or skipped job reports Success even when required (fail-open), so each required job decides inside itself with a step that fails closed"
    command: "gh api repos/mryfmo/dotfiles/rulesets/24397953 --jq '[.rules[]|select(.type==\"required_status_checks\")|.parameters.required_status_checks[].context]|join(\"; \")'; sed -n 1,12p .github/workflows/test.yaml"
    output: |-
      validate; test (ubuntu-24.04, server); test (ubuntu-24.04, client); test (macos-14, client); public-bootstrap (ubuntu-24.04, server); public-bootstrap (ubuntu-24.04, client); public-bootstrap (macos-14, client)
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
  - claim: "boundary PR 316 (.orchestration files only) ran the three public-bootstrap legs on each of its six heads, 7 to 9 minutes per leg on the final head c264c7d1 plus queue time; an .orchestration-only PR needs none of them"
    command: "gh api repos/mryfmo/dotfiles/commits/c264c7d1/check-runs --paginate --jq '.check_runs[]|select(.name|startswith(\"public-bootstrap\"))|[.name,.started_at,.completed_at]|@tsv'; gh api repos/mryfmo/dotfiles/pulls/316/commits --paginate --jq 'length'"
    output: |-
      public-bootstrap (macos-14, client)	2026-10-10T23:51:13Z	2026-10-10T23:58:20Z
      public-bootstrap (ubuntu-24.04, client)	2026-10-10T23:51:09Z	2026-10-11T00:00:07Z
      public-bootstrap (ubuntu-24.04, server)	2026-10-10T23:51:09Z	2026-10-10T23:58:50Z
      6
---

# AGMSG-TASK dotfiles-T128-ci-skip-orchestration-a02 — plan 006 A201: an .orchestration-only PR runs no bootstrap or test matrix (reset of a01)

Phase A5 (design tier: workflows); the reset successor of `dotfiles-T128-ci-skip-orchestration-a01` under INV-6 (reset record `.orchestration/acceptance/dotfiles-T128-ci-skip-orchestration-a01-design-reset.md`). The same Claude seat (`claude-standard-dot-a003`), the same branch `feat/ci-skip-orchestration` and PR #320, continuing from `dc4e6c37`; the implementation on that head stays. Implements INV-2's CI clause (design v16, unchanged sentence).

## What to build

1. `.github/workflows/remote.yaml`: each of `public-bootstrap` and `private-bootstrap` computes `should_run` in its own first step (no separate `changes` job and no `needs`: a job that `needs` a failed or skipped job is skipped and a skipped required job reports Success) for the event: on `pull_request` from the base-to-head diff (`false` only when every changed path is under `.orchestration/`), and on `push`, `schedule` and `workflow_dispatch` always `true` (those events have no PR range to judge and must keep bootstrapping `main`). `public-bootstrap` and `private-bootstrap` keep their job names and matrix; every heavy step carries a step-level `if: steps.decide.outputs.should_run == 'true'` (never a job-level `if` or a `needs`, which turn a failed decision into a passing required check; never an early-exit step, which cannot skip later steps), so the job completes with success and reports its context on an `.orchestration`-only PR. `test.yaml`'s `test` job already gates its heavy steps but through `needs: changes` (fail-open today, on main): it takes the same in-job decision step and drops the `needs`; the `changes` job goes when nothing needs it; a `main-tests` job, when present (V0 is parked and A5 precedes it, so the test must not require the job), takes the same in-job decision with step-level `if`s. The steps keep the pins `tests/unit/test_workflow_security.py` asserts (action SHAs, `permissions`, `persist-credentials: false`); `agent-assets.yml` is cheap and unchanged.
2. `tests/unit/test_workflow_orchestration_skip.py`: YAML-level checks that every required context's job has no job-level `if` and no `needs`, that each carries the decision step without `continue-on-error`, that each heavy step of `public-bootstrap`, `private-bootstrap` and, when the job exists, `main-tests` carries the `should_run` (or `should_test`) step-level `if`, that the decision yields `true` for `push`, `schedule` and `workflow_dispatch`, and that the context names equal a named constant `REQUIRED_CONTEXTS` that copies premise 1's seven contexts (a unit test cannot read the ruleset; the constant is what changes when the ruleset changes); each fails when its rule is removed. The reader fails closed: inside `jobs:`, a job name, a job key or a step key that is not the plain form `name:` (lower-case letters, digits, `_` and `-`, the colon immediately after; no quotes, no escapes, no flow mapping; comments and blank lines aside) raises, so an unsupported form fails every structural test instead of reading as "no `if`"; the test environment has no YAML parser (`make unit-test` runs bare `uv run python`) and this task adds no dependency. `tests/unit/test_workflow_security.py` must keep passing.
3. Validation: YAML-parse the workflows; the module under `make unit-test`; the four unsupported-form mutations (`if : false`, `"\x69f": false`, `continue-on-error : true`, a step written as `{ if: false }`) each fail the structural tests, pasted into validation.md; after the merge the orchestrator pastes `gh pr checks` timings of the next `.orchestration`-only PR into the acceptance record (A201's completion condition: ≤ 10 minutes with every required check reported).

## History

a01: Amendment 1 (2026-10-11 05:50Z, after the worker's PONG with the GitHub doc evidence) turned the `changes`-job pattern into the in-job fail-closed decision: the two rows on skipped jobs and failed decision steps, items 1 and 2 and premise 1 reworded, `test.yaml`'s `test` job fixed in the same PR. Revise round 1 (`dc4e6c37`) closed rename detection (`--no-renames`) and quoted keys. The audit of `dc4e6c37` found the reader class a second time (spaced and escaped keys, flow mappings) and re-raised the design-on-main prerequisite; this reset closes the reader class as a whole (fail closed on any unsupported form) and the design-on-main prerequisite (the two new rows), and changes nothing else.

## First commit

Copy this task file byte-identical to `.orchestration/dotfiles-T128-ci-skip-orchestration-a02/task.md` (the a01 directory stays as it is); evidence beside it, on the same branch from `dc4e6c37`. Phase A5 of plan 006; dormant contracts are withdrawn from the pattern, so this PR carries its tests directly.

## Completion

PR #320 stays the PR (no new draft); once the boundary PR `orchestration/boundary-2026-10-11-2` is merged, `gh pr update-branch` before the final audit; CI, Bot wait (`@codex review` if nothing in 10 minutes), artifacts, RESULT via `agmsg-dispatch … claude-deep-dot w5:p1`. max_turns=8. Forbidden: anything outside `allowed_files`; `make update`; thread resolution.
---
format: 2
task_id: dotfiles-T128-regime-v3-a01
kind: design
security: true
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round18.md
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
  INV-2: "a PR is mergeable only within the caps the CI regime job enforces from main's workflow (at most 15 changed files outside .orchestration/, 500 added lines outside tests/, .orchestration/ and the data list scripts/legacy-task-ids.txt, and 1000 added lines under tests/), and its task.md invariants equal the design's as a set of ids and byte-for-byte as sentences (the design read from main, never from the PR; a task id ending in -contract-a01 is compared with its implementing task's entry); the design file must be on main (through a boundary PR) before the implementing TASK is dispatched and the regime job fails closed when the design named by task.md is absent from main; an .orchestration-only PR runs no bootstrap or test matrix and every required check context still reports success (each required workflow decides inside its jobs, as test.yaml's changes job does), so a boundary PR merges in minutes; exceeding a cap is a split, never a finding to disposition (the cap changes the unit of work: T116 +529 and T118 +881 would have been split)"
  INV-3: "a revise round is admissible only when it adds a new deterministic check: the AGMSG-ACCEPTANCE status=revise carries check=tests/<file>::<name> and previous_head=<the RESULT head being revised>, the worker records both in .orchestration/<task id>/revise.yaml (a sibling file; task.md stays byte-identical to the dispatched file), the main-pinned regime job verifies that the named test file exists on the head and differs between previous_head and the head, the PR's own unit-test workflow (a required check, run in the PR's context) collects and runs exactly that selector on the head (it must pass) and on previous_head (it must fail or be absent), and the host gate, which reads history, verifies that previous_head equals the head of the previous AGMSG-RESULT for the task and requires the same selector in the validation file; a finding that cannot become a test is dispositioned, never iterated"
  INV-4: "a task file carries premises, each with the command and pasted output that verified it before dispatch; premises are evidence for the design reviewers and the auditor, each of whom dispositions every premise in the receipt or audit JSON as holds, fails or unverifiable (a local command re-run, an external claim re-fetched; a fails is a specification finding and a rejection), a complete disposition the schema requires rather than a sample, and the mechanical part of this invariant is the counting: a worker question (AGMSG-PONG status=question) is a specification defect answered by at most one further AGMSG-TASK, amendments are every AGMSG-TASK for the task_id after the first, whatever its wording, and the second amendment or the second question is INV-6's count, which withdraws the task to design through INV-6's merge backstop and Stop signal"
  INV-5: "the task-level audit is a headless read-only run whose instruction root is the trusted main checkout and whose schema is main's schemas/audit.json: codex exec --output-schema <main>/schemas/audit.json -C <main> with the detached worktree at the head added as a read-only data directory (--add-dir), so the audited PR controls neither the schema nor the AGENTS.md the auditor reads; the fallback claude -p --json-schema from the same root with --add-dir <worktree>, --bare when an API key is set and otherwise with project and user hooks disabled, and refused with exit 2 blocked when the head changes any file under .claude/ (bare mode loads skills from an --add-dir directory's .claude/skills/), leaving such a head to the codex path), with at most one valid audit per head (a stale input manifest invalidates an audit and a new audit of the same head replaces it), pooled two at a time; the gate accepts an audit of an earlier head only when git diff --quiet <audited head> <HEAD> -- . ':!.orchestration' holds (an evidence-only revision), otherwise a new audit is required; its input includes the task's invariants and premises, the worker's evidence, the orchestrator's task file and amendments, the acceptance record as it stands when present (its text above the line <!-- audit-input-boundary --> is the pre-audit part; dispositions of this audit's findings are appended below it), the head's pr-feedback JSON and the previous round's audit JSON; the audit JSON carries an input manifest (path to sha256 of every input as read, computed by the runner, which overwrites any model-supplied value) and the gate recomputes the manifest at gate time, so a pre-audit input edited after the audit makes the audit stale and a new audit is required; the schema lists findings {priority, confidence, category in {specification, implementation, evidence, orchestration, conformance}, path, line, rationale} and the per-invariant map before the verdict, and the prompt asks for the rationale before each verdict; the runner, under the identity claude-audit-dot-h001 or codex-audit-dot-h001 on the orchestrator's host, records the JSON's sha256 in agmsg history (AGMSG-AUDIT v1 task_id= head= sha256= auditor=) before the gate reads it, an anchor that prevents edits after the record and not fabrication before it; the gate reads the verdict and categories from the JSON, and orchestration and conformance findings at P0-P2 accept only an operator waiver or a design reset, never not-applicable"
  INV-6: "the reset rule's mandatory point is the merge backstop in scripts/require-crit-review.py, with the orchestrator's Stop hook (Claude Stop hook, Codex [hooks].Stop) as the early signal, soft on both runtimes by their documented caps; counts come from history for the hook and the gate (revises = RESULTs for the task_id minus one, threshold 2; amendments = AGMSG-TASKs after the first, threshold 2; AGMSG-PONG status=question, threshold 2) and from GitHub and main-checkout files for the gate and the boundary check only (Codex Bot P0 or P1 on two heads after the first RESULT, from original_commit_id on review_comment items recorded by pr-feedback.py; an audit implementation or specification finding at P0-P1 on two heads, from .orchestration/validation/<task>-audit-<sha7>.json in the main checkout, each counted only when its sha256 matches its AGMSG-AUDIT record); when a count is reached the gate refuses the merge until a reset record names a redesign task whose design RESULT comes from an identity other than the task's author, or a waiver written by scripts/regime-waive.sh under the INV-1 ask-rule discipline into the state directory outside the sandbox write roots (the only release path besides a redesign; the one-account residual of INV-1 applies); check-regime-boundary.sh reports a closed-unmerged PR whose task has no reset record and a task over any count with neither an accepted acceptance record nor a reset record"
  INV-7: "the design tier adds, before any code is dispatched, two design reviews of the same design hash: a fresh Claude context on the review profile (a headless run or a seated -review- identity; the review profile is the same model and effort as deep, so the lever is the separate context) and a Codex read-only review (codex exec --sandbox read-only on the review profile under a codex-review identity: headless through V4's runner, or seated until V4); each receipt is a schema document naming the design file's canonical hash over invariants, threat_model, trust_anchors, implementing_tasks and premises, each is announced by an AGMSG-RESULT from its reviewing identity, and both RESULTs precede the implementing AGMSG-TASK in history; the Codex Bot's review of a boundary PR is swept feedback, never a design receipt; a change to the hashed keys needs new reviews; the gate accepts the whole-file sha256 form for receipts written before V4 lands"
  INV-8: "worker evidence (the task.md copy, revise.yaml, report, validation, sandbox, learning, autoskill, worker review JSON) is committed on the PR branch under .orchestration/<task id>/ before the final RESULT so the Bot, CI and the gate read the same files from the audited head; the orchestrator's records (audit JSON, acceptance, pr-feedback) stay under .orchestration/validation and .orchestration/acceptance in the boundary commit because the merge is --match-head-commit"
  INV-9: "every acceptance record carries measured cost (rounds, amendments, questions, wall time TASK to final RESULT from history timestamps, audit count, Bot threads, tokens: total_cost_usd from claude -p JSON, turn.completed.usage from codex exec --json, per-message usage from the seat's session transcript) written by accept-task.py, which also records the path and sha256 of every raw source it read (the headless runs' JSON, the transcript files at acceptance time) so a total can be recomputed; cost is a warning metric, never a gate: each tier has a budget, the acceptance record names the operator decision when it is exceeded, and check-regime-boundary.sh warns; headless runs carry --max-budget-usd"
  INV-10: "at most three concurrent workers with pairwise-disjoint allowed_files; the first push is the draft PR's server-side created_at (gh api pulls/<n>), which must fall within 30 minutes of the TASK's history timestamp, and a seated worker is not idle for 20 minutes while a dispatchable task exists, a dispatchable task being a format-2 file under .orchestration/tasks/ with no AGMSG-TASK for its id in history, no superseded_by or reset record, and every task id in its after list accepted (an acceptance record with Decision accepted in the main checkout); both computed in check-regime-boundary.sh and accept-task.py, never in the Stop hook; headless reviews and audits do not count as workers"
  INV-11: permgate records session_id and cwd per decision, and the gate compares a Claude worker's permission-gated Bash count in the task window with the sandbox record (an understated record is refused); Codex workers cannot escalate and are not covered
  INV-12: "every rule above is exercised by a unit test that fails when the rule is removed; the PR's own workflow runs the PR's tests, and a required check main-tests (wave V0, before every other wave) fetches main's tests/unit and runs them in the PR's context in two modes: for a script outside the task.md's allowed_files it runs main's module as it is, so an undeclared change to any script fails; for a script inside allowed_files it runs only main's dormant contract tests for that module (tests marked with the regime's contract decorator, which skip in ordinary CI and run when REGIME_CONTRACT=1), so an intentional change is judged by the contract that was reviewed and merged on main before the implementation; the implementation PR promotes those contracts by removing the decorator in its own tree (main-tests judges it against main's dormant copy, so nothing stays dormant after the wave lands), main-tests fails an implementation PR (any task id not ending in -contract-a01) whose declared test module in the PR tree still carries a contract marker, and main-tests fails a design-tier implementation PR whose declared script has no dormant contract on main (an empty contract is not a pass); a design-tier code wave lands its contract tests first in a <task>-contract-a01 PR (dormant, hence mergeable), a review-tier wave may; the design-tier audit from the trusted root reads the diff; a deleted or weakened fails-when-removed test is a conformance finding; main-tests is an in-process oracle: code that main's tests import from the PR runs inside the test process, so the harness authenticates that main's runner reached its end with a per-run nonce that only the runner sees (read from a pipe and closed before any test loads, written back with the counts), and the runner pins unittest's result and runner classes before importing any test; the nonce authenticates the writer, not the counts: adversarial PR code running in the same process can still patch result collection or read the nonce from a frame, so in-process forgery remains a stated residual that the trusted-root audit catches, named in every acceptance record of a design-tier PR; including one test per gaming path (a schema-valid task with a prose cap bypass, a revise without a named check, a revise list appended to the hashed task.md, an AGMSG-TASK without amendment= that still counts, an evidence-only relabel of a code change caught by the tree-equality check, a wave-table rewrite after review, an audit JSON edited after its history record, a receipt whose hash predates a key change, a reset record naming the author's own identity, a Bot-skipped head whose audit never starts, a single PR split only in the task file, a branch task.md claiming a legacy id, allowed_files of ['*'] or a wildcard first segment, an invariant sentence weakened under its id, a schema or AGENTS.md edited on the audited head, an undeclared script change that main-tests must fail); legacy task ids are grandfathered by the checked-in list scripts/legacy-task-ids.txt, which only shrinks and is excluded from the line cap as data"
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
| INV-12 | one test module per script; `make unit-test` in CI; the `main-tests` required job (V0): main's modules for scripts outside the PR's `allowed_files`, main's dormant contracts (`REGIME_CONTRACT=1`) for scripts inside it; contract PRs (`<task>-contract-a01`, dormant tests, merged before a design-tier implementation); the auditor checks per PR that no new hand-written parser sits at a trust boundary (a `conformance` finding) |
| prose | SKILL, `agmsg-orchestration.md`, `pr-integration.md`, `crit-review.md`, `model-selection.md`, README: each wave edits only the sections it implements |

## 6. Waves (one PR, one invariant, within INV-2's caps; each task file reviewed by a fresh context before dispatch)

- **V0** INV-12: the `main-tests` required job in `test.yaml` (main's `tests/unit` in the PR's context: modules of scripts outside the PR's `allowed_files` as they are, dormant contract tests of scripts inside it with `REGIME_CONTRACT=1`), the contract decorator in `tests/unit/regime_contract.py`, and the two-mode protocol in the Worker Playbook; lands before every other wave. Claude seat; design tier (workflow); the operator lists the check at its acceptance.
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

Order: V0, then each design-tier code wave as `<task>-contract-a01` (dormant contract tests) followed by its implementation: V1, V1c, V1b, V2, V2b, V3a, V3b, V3c, V3d, V4, V5a, V5b, V6. File-disjoint pairs may run concurrently (V1 with V2; V3b with V3d); the gate-source waves (V2b, V3a, V4's gate part) run serially.

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

 exited 1 in 296ms:
error connecting to api.github.com
check your internet connection or https://githubstatus.com

 succeeded in 347ms:
15-- `herdr` panes are optional worker terminals; they are a launch surface, not the protocol.
16-
17-## Regime activation and progress
18-
19-- Activate this regime when the operator requests agmsg/Codex collaboration, or when the agmsg bus is available and a seated worker exists for the repository, such as in a herdr-managed workspace. agmsg is then the always-on communication path and Claude acts only as orchestrator: lightweight grep/read, judgment, task authoring, and acceptance review. The operator may opt out for the current task; only then may the orchestrator mutate the repository directly. When the bus exists but no worker is seated, seat one before any repository mutation (`herdr-agents --add-worker [<worktree>]`, default the manifest `worker_worktree`), and remove it with `herdr-agents --remove-worker <worktree>` once its task is accepted; "no worker" is never an implicit opt-out. In a regime repository the SessionStart `herdr-agents --attach` hook prints this directive as an `agmsg-orchestration:` line after `seat_claim=` in the orchestrator's Herdr pane, or after the summary line in a pane-less session.
20-- On activation, verify CompactionDB opt-in for the active repository and install it with `compactiondb-install` if missing. Regime start is operator-initiated consent to the install; acceptance-time decision consolidation then applies.
21:- A Claude session started in the repository root outside Herdr (a plain shell, mosh/ssh, or `claude -p`) is a pane-less orchestrator: nothing seats a worker automatically, and the SessionStart `herdr-agents --attach` hook prints a summary line naming that state, the on-demand commands, and any seated worker, followed in a regime repository by the `agmsg-orchestration:` directive line. Bring the regime up on demand: claim the seat outside the sandbox with the composite instance id, `actas-claim.sh <repo> claude-code <name> <session_id>.<claude pid>` (a claim from sandboxed Bash writes the bare session id and turn delivery then skips silently; see the seat-lock bullet below); seat the worker with `herdr-agents --add-worker <worktree>` (it derives `HERDR_SOCKET_PATH` from the default Herdr server socket `~/.config/herdr/herdr.sock`, the path the Claude sandbox allowlists, before creating anything, accepts a claude worker's workspace-trust dialog during spawn's readiness wait, and takes `--ready-timeout <seconds>`); confirm the worker's placement from its `run/spawn.*` placement record itself (the `herdr:<socket>:<pane>` row that upstream `agmsg_spawn_path` resolves) and the `linkage=` line `--add-worker` prints, never from `team.sh <team> --json`, which observes Codex members by reading their pane; treat the `linkage=` line `--add-worker` prints as the `AGMSG-PING` evidence, and on `pong=no` or `linkage=unreached` wake again with `agmsg-dispatch <team> <orchestrator> <worker> <pane> 'AGMSG-PING v1 task_id=<id> reason=<reason>'` and verify the PING's `read_at` (`poke.sh` only for a viewed workspace); and dispatch no AGMSG-TASK before its `AGMSG-PONG` arrives. Without a managed workspace the auditor runs headless, in the form the task-level audit bullet below names. A sandboxed pane-less session cannot keep a Monitor watch (the sandbox's pid namespace), so RESULTs arrive by turn delivery.
22-- Start checklist (operator or orchestrator, repository cwd, plain shell or Herdr): the workspace created by `herdr-agents <DIR>` full mode holds the orchestrator pane only, and only the operator creates or relaunches it; inside a Herdr pane the SessionStart `--attach` hook claims the orchestrator seat and prints the directive, and never seats, restarts or repairs a worker. Inside Herdr or outside it, the orchestrator seats a worker on demand with `herdr-agents --add-worker [<worktree>]` (its own tab of the managed workspace, or its own workspace for a pane-less orchestrator), confirms it by PING/PONG before any task, and removes it with `--remove-worker` when the task is done. A Claude that finds itself outside Herdr is the pane-less orchestrator of the bullet above: its SessionStart line reports the state, and it brings the regime up on demand exactly as that bullet describes (composite seat claim outside the sandbox, `--add-worker`, PING/PONG before any task, headless auditor); anything neither bullet describes is not improvised.
23-- Seat and remove a worker only with `herdr-agents --add-worker` and `herdr-agents --remove-worker`; `--restart-worker` is retired and exits 2. Never run full mode from inside an existing managed workspace; the orchestrator and its worker tabs share one workspace. Activate a worker model or profile change by removing the worker with `herdr-agents --remove-worker <worktree>` and seating it again with `herdr-agents --add-worker <worktree>`, which sources launch args from `~/.agents/model-profiles.env`; never pass ad-hoc flags.
24-- Do not idle-wait while worker work is in flight; prepare or delegate independent work.
25-- A blocker reported to the operator carries attached evidence: the exact command, its exit code, and the messages.db `read_at`/PONG query, after the wake path that worked in earlier sessions (`agmsg-dispatch`) has been tried. An inference (for example "trust dialog" from a `poke.sh` exit 15 plus a spawn readiness timeout) is not a reportable blocker. `herdr-agents --add-worker` ends with that evidence for a fresh seat: one `linkage=ok read_at=<ts> pong=<yes|no>` or `linkage=unreached rc=<n> hint=<agmsg-dispatch|poke|attach-a-client>` line from an `agmsg-dispatch` PING, and it exits non-zero only when the PING was not read.
26-- Detect worker completion only when an `AGMSG-RESULT` arrives through monitor/turn delivery. Send liveness checks only as `AGMSG-PING`/`AGMSG-PONG`; never read worker panes or screens (including read-only probes such as `pane read`/`pane wait-output` against another agent's pane, even to learn output shapes; use `--help` and fake CLIs), infer completion from pane/agent status, or use ad-hoc polling sleep loops. Limit pane interaction to prompt injection and the submit key.
27-- If an out-of-band Codex completion signal is needed, use the official `notify` config: the `agent-turn-complete` event sends a JSON payload to an external command.
28-
29-## Parallel workers
30-
31-- Add and remove parallel workers only with `herdr-agents --add-worker <worktree> [--kind codex|claude] [--profile NAME]` and `herdr-agents --remove-worker <worktree> [--force]` (worktree under `.claude/worktrees/`). For Codex, seat ordinary tasks with `--profile standard`; use `--profile security` only for trust-boundary tasks (permgate, redaction or secret handling, sandbox or permission policy), per the model-selection rule, with an identity such as `codex-security-dot-aNNN`. Add-worker seats the worker in its own tab of the pair workspace, labeled `<team>:<name>` with the pair tab untouched (in its own workspace only when no pair workspace exists, as in the pane-less bring-up), through upstream `spawn.sh --project <worktree> --terminal-driver herdr` with the profile's launch args in a generated spawn options file, so a placement record exists and `poke.sh`/`despawn.sh` work. Remove-worker despawns it, then turns delivery off, leaves, and closes that tab (or workspace), refusing a dirty worktree without `--force`. Keep about three concurrent workers at most; raw herdr topology commands stay forbidden (T21 G7).
32-- Under upstream agmsg 1.5.0 self-naming, a pair's panes carry `<team>:<name>` labels rather than `claude-orchestrator`/`<kind>-worker`; `herdr-agents` recognizes the pair through the repository's agmsg seats (the orchestrator identity at the main checkout and the pair's own worker seat, never other team members) and never relabels a self-named pane.
33:- Delegate all repository-mutating work — file edits, builds, test runs, and git state changes — to seated workers, with at most one seated worker per git worktree and sequential assignments within one worktree. Add worktrees for parallelism; never use parallel `codex exec` or per-task Codex spawning, except that the read-only, non-interactive task-level audit the orchestrator runs during acceptance (the task-level audit bullet below) is not worker spawning and is permitted; it is identity-less. agmsg/herdr control-plane commands (`delivery.sh`, `watch.sh`, `actas-claim.sh`, `send.sh`, `join.sh`, and herdr agent/pane commands) are orchestrator-side exemptions.
34-- The orchestrator acts directly, without delegation, only under these exemptions: agmsg/herdr control-plane operations and evidence-sync bookkeeping; acceptance and final integration, including merging an already-reviewed, CI-green PR; and machine-state hygiene that touches no repository (tool-manager operations such as `mise install`/`mise prune`, removal of unmanaged `$HOME` files), provided tracked worktrees stay diff-clean throughout. It declares which exemption applies in one line before mutating anything.
35-- A parallel assignment is valid only when every concurrent worker has all four of: (1) its own git worktree registered as its agmsg `project`; (2) the shared default agmsg store for same-repository work, never a per-worker `AGMSG_STORAGE_PATH`, because identity-addressed delivery and worktree-specific `whoami` already isolate inboxes and one activation watcher observes every RESULT/PONG without extra watchers (which `watch.sh` actas locking cannot support for one claimed identity); (3) an `-aNNN` identity suffix on every concurrent worker, including the first; and (4) an AGMSG-TASK whose expanded `allowed_files` are pairwise-disjoint from all other in-flight tasks for code files; a shared prose file (README, SKILL) may appear in two in-flight tasks only when their sections do not overlap. The orchestrator verifies disjointness and performs all cross-worktree merge, rebase, and conflict integration.
36-- Parallel execution procedure:
37-  - At plan approval, partition the approved tasks into waves by dependency and file overlap: code files pairwise-disjoint, and shared prose files in disjoint sections. Write the wave table into the plan file.
38-  - Keep at most three workers in total. Seat workers with `herdr-agents --add-worker` only up to that cap. Dispatch at once as many tasks of the current wave as there are free seats, each with a distinct `-aNNN` identity and its own worktree, and queue the rest of the wave.
39-  - When a RESULT arrives, run acceptance for that task while the others continue; acceptance follows RESULT arrival order.
40-  - A freed worker is re-tasked immediately with the next dependency-free task whose files overlap no in-flight task. Never leave a seated worker idle while a dispatchable task exists. The next task starts on a fresh branch from `origin/main`, and the previous task's branch stays in the worktree, untouched, for its revise rounds and until its acceptance. The worker commits and pushes everything before each RESULT, and before every branch switch it commits the newer task's work (or stashes it under a named tag and restores it afterwards), so a switch never carries edits across branches. When a `status=revise` arrives for the earlier task, it checks that branch out again, does the round, and returns to the newer task's branch, so the worktree is reused sequentially and nothing uncommitted is ever left behind.
41-  - When a merge moves `main`, every in-flight PR whose base moved, prose or code, merges the new base into its branch with `gh pr update-branch` before its CI, Bot wait and gate. The ruleset's strict up-to-date policy refuses the merge otherwise. `gh pr update-branch` creates a merge commit by default, not a rebase. A real conflict blocks only that PR.
42-  - Record the wave table and the per-task worker in the acceptance records.
43:  - Some steps stay sequential. The single audit tab serializes audits; the task-level audit of T67 reduces them to one per task. The orchestrator-side gate (`make require-crit-review`) and merges also run one at a time.
44-- At parallel-worker teardown, run `delivery.sh set off <type> <worker worktree path>` to stop every watcher on that exact path, then `leave.sh <team> <worker identity>` for each finished worker. The last member of a task-scoped team leaves so the team is deleted while message history remains. Verify with `identities.sh <project> <type>` by counting distinct identity names in the second TSV column: while a worker is seated, one distinct name per type at its worktree is healthy, including multiple rows for that name across teams; the only active seat, the main checkout, holds exactly one name across both types, and a worker worktree holds none once its worker is removed, which `make check-regime-boundary` enforces. More than one distinct name indicates leftover identities that trigger the herdr-agents ambiguity warning at attach and must be cleaned with `leave.sh`; preserve legitimate multi-team memberships of the retained name. Zero names for a project that should remain active must be restored with `join.sh`, never leave-side edits.
45-
46-## Identity, delivery, and storage
47-
48-- Give each physical agent one unique identity: `<runtime>-<profile>-<project-suffix>` (for example, `codex-standard-dot`, or a `-flue` suffix for flue-pi). The project suffix derives from the repository, not the checkout; model IDs belong only in `model_profiles` in `agent-config.yaml`. A solo worker has no instance suffix. For parallel workers, rename the incumbent to `-a001` so team registration and message history follow, give every worker an `-aNNN` suffix, re-claim actas locks after rename, and never mix suffixed and unsuffixed identities.
49-- Before joining, search every `~/.agents/skills/agmsg/teams/*/config.json` for the candidate name. On collision, choose a unique suffix; never reuse one identity for different physical agents.
50-- Register `project` as the worker's real working-tree path (the dedicated worktree for parallel workers), byte-identical across join, delivery setup, and hook arguments. Trailing slashes and unresolved symlinks orphan inboxes through exact-string mismatch. `$HOME` registrations are forbidden because they create Codex-hook ambiguity and steal inbox messages.
51-- Register a worker identity at its own worktree path with resolution off: `AGMSG_RESOLVE_PROJECT=0 join.sh <team> <name> <type> <worktree>`, and point its delivery at the same path with `delivery.sh set <mode> <type> <worktree>` so the hook bakes the worktree into the session's project marker. Every `join.sh`/`whoami.sh`/`actas-claim.sh`/`reset.sh`/`watch.sh` call a worker makes runs with `AGMSG_RESOLVE_PROJECT=0` (herdr-agents sets it in every worker pane it creates; `spawn.sh --project` sets it for agmsg-spawned seats). Upstream project resolution (#92, `docs/design.md` "Project resolution") otherwise rewrites the path in order: the live SessionStart marker `run/proj.<agent_pid>.project`, then the nearest registered ancestor, then the registered main checkout via `git rev-parse --git-common-dir`. Verified against a scratch v1.5.0 install: a `join.sh` from inside `.claude/worktrees/<x>` without the opt-out registers at the main checkout; a session whose marker names the main checkout (a seat launched from the main path) makes `whoami.sh` inside the worktree answer with the main checkout's identities; the opt-out restores the worktree in both cases. `session-start.sh` exits before the watcher and marker for any session whose cwd is under `.claude/worktrees/` (#367), so a Claude seat launched inside a nested worktree gets no Monitor watch from that hook: the herdr-agents pair worker relies on turn delivery (a spawn-seated worker starts its Monitor through its actas boot) or the inbox checks below. `identities.sh` stays a pure lookup of the exact path.
52-- On activation, check `delivery.sh status <type> <repo>`. This repo runs Claude Code seats on `both` (monitor's push plus turn's pull), one notch more redundant than upstream's Claude Code default `monitor`, since an unattended worker pane has no one to notice a Monitor watch that silently failed to re-arm; Codex seats run on `turn` (see the next bullet). If weaker than that, run `delivery.sh set both claude-code <repo>` (or `delivery.sh set turn codex <repo>` for a Codex identity), start the SessionStart-provided `watch.sh <session_id> <repo> <type>` as a persistent in-session monitor, and claim exclusivity with `actas-claim.sh <project> <type> <name> <session_id>`. A Claude worker seated by `--add-worker` gets its Monitor watch through its actas boot; when it is seated in its own workspace (no managed workspace exists), `herdr-agents` also sets `AGMSG_CC_MONITOR_KEEP_ALIVE=1` in that workspace's environment so the watch re-arms unconditionally on expiry, not only when the expired watch delivered something (upstream's default).
53-- `herdr-agents --bootstrap-agmsg` (and full or attach mode) sets the main checkout's orchestrator hooks, Claude Code on `both`; a worker seat gets its own hooks from `herdr-agents --add-worker`, Codex on `turn` and Claude Code on `both`, so the Stop/SessionStart hook in the worktree's tree-scoped, gitignored `.codex/hooks.json` or `.claude/settings.local.json` delivers inbox messages. Codex deliberately stays on `turn` instead of upstream's shim-based `monitor` bridge (the upstream README names `monitor` as the Codex default in one place and `turn` in its delivery table): as of agmsg v1.5.0 that bridge has open reliability defects an unattended resident worker cannot risk — no teardown on session end (upstream #149), a mode switch that does not start the bridge in a live session (#151), and a bridge that restarts forever while its status reports it alive (#1236), all still open. Storage resolution is env-only: keep `AGMSG_STORAGE_PATH` unset for same-repository default-store workers, or set it to the regime's dedicated store for separate cross-project regimes; a wrong or stray value silently reroutes the worker to another database. Pane nudges are only generic wakes; message content always travels over agmsg.
54-- Worker panes run in their worktree: `herdr-agents --add-worker [<worktree>]` seats the worker in that worktree (default the manifest's `worker_worktree`, created from `origin/main` when missing), registers its identity there with `AGMSG_RESOLVE_PROJECT=0`, sets delivery on that path, and starts it through upstream `spawn.sh`, so turn delivery reaches the worker directly through the worktree's Stop hook and its Monitor watch comes from the actas boot (upstream `session-start.sh` skips sessions under `.claude/worktrees/`, #367). The interim worker inbox discipline (running `~/.agents/skills/agmsg/scripts/inbox.sh <team> <identity>` at each milestone: task start, push, CI green, before RESULT, after any PONG) is retired for a worktree-seated worker; it applies only to a worker still acting under a worktree-registered identity from a main-path pane, until `herdr-agents --remove-worker` and `--add-worker` re-seat it.
55-- A codex worker in a nested worktree gets `<common>/objects`, `<common>/refs`, `<common>/logs` and `<common>/worktrees/<name>` (`<common>` from `git -C <worktree> rev-parse --git-common-dir`) as writable roots from `herdr-agents` (`-c sandbox_workspace_write.writable_roots`, with the configured agmsg roots kept first), so local git operations need no escalation. The common dir itself, `config`, `hooks`, `info`, `HEAD` and `packed-refs` stay read-only. The worker seat runs with `--ask-for-approval never` and `sandbox_workspace_write.network_access=true`, so a GitHub fetch, push or `gh` call works inside the sandbox and the worker never prompts: there is no escalation for a worker, and an action outside the sandbox or forbidden by the execpolicy fails and is reported as `AGMSG-PONG v1 status=blocked`. The `sandbox_workspace_write.network_access` switch is a boolean, so the worker reaches any host (no domain allowlist is configured, unlike Claude Code's `allowedDomains`), and the permgate PermissionRequest hook never fires for the worker seat; it stays live for interactive Codex sessions, which keep on-request approvals and no sandbox network.
56-- The orchestrator's actas seat lock must hold the composite instance id `<sid>.<pid>`; check it with `cat ~/.agents/skills/agmsg/run/actas.<team>__<name>.session`. `actas-claim.sh` run from sandboxed Bash cannot see the claude pid (the Linux sandbox has its own pid namespace), writes the bare session id, and the Stop-hook inbox check then skips delivery silently (`other:<sid>`). `herdr-agents` therefore claims the seat outside the sandbox when it starts the orchestrator pane and from its SessionStart `--attach` hook, printing `seat_claim=ok owner=<sid>.<pid>` (or `seat_claim=unresolved`, never a bare-id lock), and `make doctor` warns on a bare-id orchestrator lock while a claude session runs in the repository. A `watch.sh` Monitor cannot run under that sandbox either: it sees the claude pid as dead and exits "no longer alive". Until upstream offers a liveness override, turn delivery is the working path, and an idle orchestrator is woken by the worker's `agmsg-dispatch` to the orchestrator pane.
57-- Reserve store separation for concurrent regimes in different projects, such as flue-pi. When using it, set the same `AGMSG_STORAGE_PATH` in the worker pane and on orchestrator send/watch/history calls or tasks, results, and pongs become unreachable. Same-repository parallel workers always share the default store.
58-
59-## Live verification
60-
61-- Accept changes to live desktop behavior — herdr layout/session, pane lifecycle, or delivery hooks — only after live end-to-end verification covers both a fresh session and a persisted-session restore; unit and static tests alone are insufficient.
62-- Launch orchestrator-driven E2E test-subject panes with express-profile arguments from `~/.agents/model-profiles.env` (`MODEL_PROFILE_EXPRESS_CLAUDE_ARGS` / `MODEL_PROFILE_EXPRESS_CODEX_ARGS`), never ad-hoc `--model` flags.
63-
64-## Review and integration invariants
65-
66-- Review every RESULT adversarially across correctness, regressions, security, and reporting omissions: try to refute it, independently re-derive findings, and never treat sampled spot checks as full verification.
67-- Acceptance review, adversarial RESULT review, and review-profile work remain orchestrator-side; never delegate them to a worker, and keep `make require-crit-review` as the final integration step. Revisit only if worker-side model capability surpasses the orchestrator tier.
68-- At regime or session boundaries, write pending acceptance records, then mechanically commit every `.orchestration` file so no untracked tail remains. The sync needs no per-task artifact set: its audit record is the commit, whose message lists covered task IDs, plus agmsg ACCEPTANCE history. `make check-regime-boundary` reports a canonical clone with unmerged entries, a stash, or a difference from `origin/main` under `home/`, `install/` or `scripts/` as a sign that something ran where it must not. Lessons from a session are codified in this repository (a rule, the skill, or a check) through a task; Claude auto-memory is not a durable store for regime procedure. The canonical clone is pull and apply only and untouched by any seat: no edits, no apply from a dirty tree (the run_before guard refuses it), and one orchestrator identity per repository, seated at the working clone.
69-- Stop checklist, at every regime or session boundary and in this order: write pending acceptance records; mask every `.orchestration` file the boundary commit adds or changes with `uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets <files>`, which also normalises home directories to `~`; run `make validate-agent-assets` (real exit status); make the `.orchestration` boundary commit with zero untracked tail on a fresh `orchestration/boundary-<YYYY-MM-DD>` branch from `origin/main` and merge its PR with `gh pr merge --squash --auto`; remove every worker with `herdr-agents --remove-worker <worktree>` (despawn, delivery off, leave, tab or workspace closed); check stale identities with `identities.sh <path> <type>` (exactly one name at the main checkout, none at a worker worktree); close Crit review servers (`pgrep -f 'crit _serve'` must be empty); in a CompactionDB-opted-in project, review `uv run --no-project .claude/hooks/contextdb_cli.py memory candidates --limit 20` and promote each candidate worth keeping with `uv run --no-project .claude/hooks/contextdb_cli.py memory promote <id> --scope project`, or leave it. The orchestrator workspace itself stays resident for the next session unless the operator restarts the machine. `make check-regime-boundary` (`scripts/check-regime-boundary.sh`) checks this list and the orchestrator seat lock, one line per violation.
70-- Before every `.orchestration` boundary commit, run the masker on the files it adds or changes (`uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets <files>`), then `make validate-agent-assets`, and branch on its real exit status, never through a pipe; fix a failure before pushing, because committed audit evidence can trip the secret scan, which also rejects a home directory path in `.orchestration/**`.
71:- The orchestrator never pushes a repository change to `main` directly. `main` is protected by the GitHub ruleset "main integration gate": a pull request is required, review threads must be resolved, the seven required checks must pass under the strict up-to-date policy, and `main` cannot be deleted or rewound. The `.orchestration` boundary commit goes on a fresh branch from `origin/main`, `orchestration/boundary-<YYYY-MM-DD>` (suffix `-2`, `-3`, … for another boundary the same day, since merged branches are kept), opens as a PR, and is merged with `gh pr merge --squash --auto`: the `changes` job skips the test matrix for an `.orchestration`-only diff, and the ruleset accepts the resulting `skipped` required checks. An acceptance merge happens only on GitHub using step 10.5; a local merge followed by a push is no longer a path.
72-- For CompactionDB-opted-in projects, verify during the sync that every accepted task has a consolidated decision record.
73-- A `.ua/` graph RESULT is accepted only when its validation file pastes the table from `ua-symbol-coverage <previous-graph> <new-graph> --old-ref <previous-graph-rev> --repo-ref <new-graph-rev>` (on PATH from `~/.local/bin/common`; each rev is that graph's `.ua/meta.json` `gitCommitHash`, the new one normally `HEAD` and never the pre-change base; `--old-ref` tells renames from deletions) with zero regressions, or cites the source change behind each decrease; `validateGraph` passing does not prove extraction completeness.
74-- Task-level audit: every RESULT that changes repository code gets one audit of the task on its final head, covering the whole PR diff (`git diff <merge-base> <head>`).
75-  - Pair form, in the pair workspace's dedicated audit tab: `herdr-agents --audit <head-sha> --task <id> [--out <path>] <main DIR>`. It writes `.orchestration/validation/<id>-audit-<sha7>.md` and codex's final message to that file's `.last.md` companion, whose last non-blank line is the verdict.
76-  - Headless form, without a pair workspace, with `<out>` = `.orchestration/validation/<id>-audit-<sha7>.md`, run from the orchestrator's own checkout (never one that sits at the audited head):
77-    - Give codex the same task-level inputs the pair form builds: the task file `.orchestration/tasks/<id>.md` (required), the worker's report, validation and sandbox files and `<id>-pr-feedback.json` (those present), the final head `<head-sha>` and the PR diff `git diff $(git merge-base origin/main <head-sha>) <head-sha>`. Ask for findings as `[P0-P3] confidence dimension file:line rationale` and exactly one concluding `Verdict: correct|incorrect|blocked` line.
78-    - Run `rm -f <out> <out>.last.md && set -o pipefail && codex <MODEL_PROFILE_AUDIT_CODEX_ARGS> exec --sandbox read-only -C <repo> -o <out>.last.md '<that prompt>' 2>&1 | tee <out>`. Removing both files first means a failed rerun can never leave an earlier `Verdict: correct` behind, as the pair form also ensures, and `pipefail` keeps codex's exit status through `tee`. A nonzero codex exit means no audit: there is nothing to gate, so rerun it.
79-    - Only after a zero exit, mask both files with `uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets <out> <out>.last.md` from a trusted checkout. Like the pair form, refuse when that checkout's HEAD is the audited commit, or when its validator is missing, untracked, or changed against HEAD (`git diff --quiet HEAD -- scripts/validate-agent-assets.py`), so a PR can never run its own validator on the orchestrator. Treat a refused or failed masking as a failed audit.
80-    - The gate needs both the transcript file and its non-empty `.last.md` companion.
81-  - Run either form from a clean tree: the only untracked content in the audited checkout is this task's `.orchestration` evidence that the audit prompt names (task file, report, validation, sandbox file, feedback JSON). Otherwise run it from a dedicated clean checkout, so no other edit can reach the auditor.
82-  - A new push, including a `gh pr update-branch` merge, needs a new audit of the new head.
83-  - The orchestrator dispositions every `[P0-P3]` finding in the acceptance record, whatever the verdict: exactly one `audit-finding: <n> …` line per finding, numbered 1..N in the audit's order of `[P0-P3]` lines. The audit's finding lines may be bulleted; a disposition line may be indented but never starts with a list marker, or the gate skips it. `fixed:<sha>` needs a fresh audit of that sha; otherwise `not-applicable:<reason of at least 20 characters>`. Deferral ("later", a follow-up task, a stopgap or a suppression) is not a disposition. The gate enforces these lines only for an `incorrect` verdict (T68), but a finding under `Verdict: correct` is dispositioned all the same.
84-  - The audit evidence and the PR-feedback JSON quote reviewed content, so mask them with `uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets <files>` before they are committed. The gate compares PR-feedback bodies after the same masking, so masked feedback evidence still matches the live collection (T93, #251).
85-  - Audit findings are input, never approval; acceptance authority stays with the orchestrator, and each RESULT gets its own acceptance record.
86-- Crit is agent-side only for Claude Code and Codex alike, as in `home/dot_config/claude/rules/crit-review.md`: record crit-data evidence (`crit status --json`, `crit comments --all --json <review.json>`) and never open a browser review to ask the user. When Crit data is unavailable, save the independent agent review as the same repo-local JSON list (objects with non-empty string `id`, `body`, `scope` and `resolved: true`, at least one `scope: "review"` or path-bound `line`/`file` record; hand-written records are acceptable because the guard validates shape, not provenance) and reference it from a `review_surface: crit-data` receipt with `reviewer: claude-code`, `claude`, or `codex`, `review_source: <that JSON>`, and `review_outcome: approved` or `addressed`. Run `crit share` or any other publish step only when the user explicitly asks for it. Close a Crit session opened by the Plan Mode hook once its review is done, so no local Crit web server stays resident.
87-
88-## Message Contract v1
89-
90-Send messages as single-line records so inbox/history output stays parseable.
91-
92-`AGMSG-TASK v1` fields:
93-
94-```text
95-AGMSG-TASK v1 task_id=<id> repo=<absolute-repo-path> task_file=<path>
96-allowed_files=<paths-or-see-task-file-section> forbidden_actions=<semicolon-list>
97-expected_result_file=<path> expected_validation_file=<path>
98-expected_sandbox_file=<path> expected_learning_file=<path>
99-expected_autoskill_file=<path> done_signal=AGMSG-RESULT max_turns=<n>
100-note=act-as-worker-<task-or-role>
101-```
102-
103-Task files must state durable facts with `[memory:decision]` or `[memory:failure]` markers using the tag form, bracket form, and kind aliases defined by the vendored CompactionDB README.
104-
105-`AGMSG-RESULT v1` fields:
106-
107-```text
108-AGMSG-RESULT v1 task_id=<id> status=ready_for_review|blocked
109-report=<path> validation=<path> sandbox=<path> learning=<path> autoskill=<path>
110-```
111-
112-Tasks that create persistent side effects outside the repository working tree, such as global asset installs, writes under `$HOME`, or external service registrations, include the optional field `effects=<semicolon-list-of-short-ids>`. In-repository edits within `allowed_files` are not effects. For each declared effect, the report must state its reverse mapping: a named `~/.agents/.installed-manifest.json` step removable with `remove-agent-asset`, a documented removal procedure, or an `irreversible:` statement with rationale.
113-
114-RESULT reports must mark durable facts with the same CompactionDB marker contract. In CompactionDB-opted-in projects, the worker runs `uv run --no-project .claude/hooks/contextdb_cli.py memory add` before completion and includes the exact command or commands in the RESULT report.
115-
116-RESULT validation files must contain the verbatim output of every validation command actually executed — not summaries or PASS labels alone — and any identifier the report claims to have created (commit hash, PR number, CompactionDB memory/decision ID) must appear in that pasted output. A claim without its pasted output is treated as unexecuted and grounds for `status=revise`.
117-
118-`AGMSG-ACCEPTANCE v1` fields:
119-
120-```text
121-AGMSG-ACCEPTANCE v1 task_id=<id> status=accepted|revise reason=<short-reason> next_action=<action>
122-```
123-
124-Each acceptance record also includes a `cost:` line with worker-reported token/cost figures when available, otherwise `cost: n/a`.
125-
126-Liveness messages:
127-
128-```text
129-AGMSG-PING v1 task_id=<id> reason=<short-reason>
130-AGMSG-PONG v1 task_id=<id> status=alive|blocked note=<short-note>
131-```
132-
133-## `.orchestration` Workspace Layout
134-
135-- `tasks/`: orchestrator-authored task specs.
136-- `reports/`: worker reports and blocked-task reports.
137-- `validation/`: command output and validation evidence.
138-- `acceptance/`: orchestrator acceptance, revision, or rejection records.
139-- `sandboxes/`: per-task isolation records (sandbox/worktree evidence).
140-- `autoskill/config/`, `autoskill/inputs/`, `autoskill/runs/`, `autoskill/outputs/`: redacted AutoSkill artifacts.
141-- `learning/`: task learning triage records.
142-- `learning/rule_candidates/`: candidate reusable rules only.
143-- `skills/candidates/`, `skills/promoted/`, `skills/rejected/`, `skills/merged/`: separated skill registry states.
144-- `agmsg/`: exported or summarized agmsg history when needed for review.
145-
146-## Orchestrator Playbook
147-
148-1. Join or confirm the agmsg team and identities with the `agmsg` scripts.
149-2. Create the `.orchestration` directories before assigning work.
150-3. Write a task file that includes objective, scope, allowed files, forbidden actions, expected artifacts, validation commands, and max turns. Name the render check as `make render-check`, never the bare `python3 scripts/generate-agent-configs.py --check`, which fails without PyYAML. Ground `allowed_files` by grepping the repository for every touch point the task names (tests that pin call sequences, mirrors, fixtures) before dispatch. Verify every CLI constraint the task asserts by running the real command in a safe form, not by reading `--help`. Presume an auditor finding that contradicts your own review is right until you refute it with evidence. Decide the worker kind from the allowed files before dispatch: a seat never edits the source of its own execution boundary, so a change is routed by the boundary it touches. A change that touches only Claude's boundary goes to a Codex seat: the `claude.permissions`, `claude.sandbox` and `claude.hooks` blocks of `home/dot_agents/agent-config.yaml` (including excludedCommands, allowUnsandboxedCommands, writable roots, network and the PermissionRequest hook), the Claude-rendering parts of `scripts/generate-agent-configs.py`, the rendered `home/.chezmoitemplates/claude-settings-managed.json`, and `home/dot_claude/modify_private_settings.json`. A change that touches only Codex's boundary goes to a Claude seat: `codex.sandbox_workspace_write`, `codex.approval_policy`, the Codex-rendering parts of the renderer, and `home/.chezmoitemplates/codex-config-managed.toml`. A change that touches both, or a shared source the orchestrator cannot split (such as `codex.sandbox_workspace_write.writable_roots`, which also renders into Claude's `allowWrite`), goes to the operator. The orchestrator decides the kind from the diff the task will produce and records it and the chosen worker profile in the task file. The Claude Code auto-mode classifier also refuses a Claude-boundary task on a Claude seat as Self-Modification. A task that edits permgate (`home/dot_agents/permgate-policy.yaml`, `home/dot_local/bin/common/executable_permgate`), the PermissionRequest hook of both seats, goes to the operator; a Codex `security`-profile worker reviews the change before the orchestrator accepts it, per the model-selection rule. `auto` is Claude Code's built-in starting permission mode since 2.1.283. A project-level `defaultMode: auto` (`.claude/settings.json` or `.claude/settings.local.json`) does not take effect, and the session then also ignores the user-level `defaultMode`, so `auto` belongs only in user or managed settings. Before dispatch, read the task's verbatim blocks against each other for contradictions, and state each rule once; a second artifact references the first instead of restating it.
151-4. Start or relaunch worker panes only through `herdr-agents` modes. Deliver messages and wakes as in step 6; never use `pane send-text` followed by `send-keys Enter`, because the separate Enter races the TUI composer and fails nondeterministically.
152-5. Configure delivery deliberately. `delivery.sh set turn` is useful for turn-end inbox checks; changing delivery mode can kill project watcher processes, so do it before starting long-running project watchers.
153-6. Send `AGMSG-TASK v1` with the exact artifact paths and `done_signal=AGMSG-RESULT`. Pass every `send.sh`/`poke.sh` body with `--body-file <path>` (both take it in agmsg v1.5.0), never as a positional argument: a positional `<text>` passes through the caller's own shell first, where a backtick or `$( )` in the body silently executes and vanishes from what arrives (upstream #378). `agmsg-dispatch` is the one exception and takes a single-line, shell-safe positional message. Pick the path by how the recipient is seated, never by inferring pane or agent status: a worker in a `herdr-agents` pane gets `agmsg-dispatch <team> <from> <to> <pane_id> "<message>"` (send, generic wake, `read_at` wait; single-line shell-safe text only), the sanctioned wake path until worker seating writes placement records at launch, because `poke.sh` exits 1 with "no placement record" for a hand-joined member, and a herdr-agents worker gets a record only once it acts from its own pane (upstream `send.sh`/`inbox.sh` record the acting pane, #1109); a spawn-seated member (placement record `run/spawn.*`; `team.sh <team> --json` shows its pane) gets `poke.sh <team> <name> --body-file <path> [--retries N --retry-delay SECONDS --backoff fixed|exponential]`, which types and submits in one call and refuses to type over an in-progress draft (#1321/#1322); a pane-less member gets `send.sh <team> <from> <to> --body-file <path>` and its own delivery mode. Verify delivery via the messages.db `read_at` column. `poke.sh` exit codes: 10 = terminal unreachable, 12 = pane gone or no live agent, 14/15 = refused to type over a changing or unlocatable input box, 13 = the driver has no poke path for this pane (for example a `plain` terminal); where poke.sh's narrow agmsg-message fallback succeeds it exits 0, so 13 means nothing was delivered, and the printed reason names the native channel, asks the caller to claim its own identity first, or reports that the fallback failed. Never retry a 13 as `send.sh` yourself: that overrides the driver's considered refusal and can double-deliver. Seating case: a worker in an unviewed or headless Herdr workspace (no client attached, a small pane rect such as 18x41) makes `poke.sh` exit 14/15 from its TUI input locator; that is a locator refusal, not evidence about the worker's state, so wake it with `agmsg-dispatch` and verify `read_at`.
154-7. Track `max_turns`. Use `AGMSG-PING` for liveness if a worker stalls.
155-8. On `AGMSG-RESULT`, read the task file and every referenced artifact before deciding.
156-9. For a RESULT carrying `effects`, verify that every declared effect has the report's stated reverse mapping before acceptance; record any irreversible effect in the acceptance note.
157:10. For a RESULT that carries a pull request, integrate in this order. This is the single procedure that the PR integration rule, `AGENTS.md`, the README and the gh-first-workflow skill cite. A `gh pr update-branch` moves the head, so steps 1 to 4 run again on the new head. After an update-branch the orchestrator runs it, the order is CI on the new head, then the sweep, then the audit; an audit started before CI finishes sees incomplete evidence and returns an evidence-only `incorrect`. Select a checkout with git -C <absolute path>, never with cd, which the sandboxed Bash may not honour. After moving the review worktree to the audited head, verify git -C <review> rev-parse HEAD equals that head and git -C <main> symbolic-ref --short HEAD prints main before the audit and the gate.
158-    1. Sweep the final head's feedback with `scripts/pr-feedback.py <pr> --json .orchestration/validation/<task>-pr-feedback.json` and give every item a `fixed:<commit>` or `not-applicable:<reason>` disposition, leaving none on `failure` or `warning` annotations. Optionally request `@coderabbitai full review` on the final head first; when a CodeRabbit review exists it is swept like any other item, and the gate does not require a bot review.
159:    2. Run the task-level audit of that head in the pair or headless form of the task-level audit bullet. It exits nonzero for every verdict other than `correct`. An exit with `Audit verdict: incorrect` is not a failed step: continue to step 3 and disposition its findings. A `blocked` or missing verdict means re-running the audit.
160-    3. Write the acceptance record, summarising the dispositions, with an `audit-finding:` line for every audit finding whatever the verdict (the gate needs them, through `AUDIT_DISPOSITIONS`, when it is `incorrect`).
161-    4. Run the gate: `AUDIT_EVIDENCE=<audit> [AUDIT_DISPOSITIONS=<acceptance record>] AGENT_REVIEWED=1 REVIEW_EVIDENCE=<receipt> BASE=origin/main PR_FEEDBACK_EVIDENCE=<json> make require-crit-review`.
162-       - A `review` sweep item whose body carries a `P0`–`P3` badge is a finding with its own `fixed:<commit>` or `not-applicable:<reason>` disposition, never a container for its inline threads.
163-       - The sweep covers issue comments, reviews, inline review comments with thread resolution, non-passing check runs, check-run annotations at every level (`notice`, `warning`, `failure`), and commit statuses. A `failure` marked `not-applicable` needs a concrete reason of at least 20 characters.
164-       - A CodeRabbit full review is optional, at most once on the final head: the plan allows one review per hour and every review event spends one (docs.coderabbit.ai/management/rate-limits).
165-       - The feedback JSON may be masked with `uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets`, which masks its keys and string values; the gate identifies an item by its source, url, level, path, line and body, and accepts a body or path that is verbatim or exactly that masked form.
166-       - The gate rejects evidence outside `.orchestration/validation/` or without the `-pr-feedback.json` suffix. It binds `BASE` to the PR's GitHub base before running the collector from that authenticated SHA: an older base must be outside HEAD's first-parent chain, an advanced base must preserve the merge-base with the PR head, and PR branch commits (including `HEAD`) cannot substitute for the base. Evidence must match the local GitHub repository independently of `GH_REPO`, and `fixed:` commits must be in the authenticated GitHub base-to-head range whatever `BASE` is selected.
167-       - `AUDIT_EVIDENCE` must be the task-level file `.orchestration/validation/<task>-audit-<sha7>.md` (the same `<task>` as the feedback JSON); a per-commit `audit-<sha>.md` is rejected. Its verdict comes only from the non-empty `<file>.last.md` and must be `correct`, or `incorrect` with `AUDIT_DISPOSITIONS`. PRs that change only `.orchestration/` files need no audit.
168-       - A boundary PR (`orchestration/boundary-<date>[-n]`, `.orchestration` files only) skips the gate, the sweep JSON and the audit (with `BASE` set the gate would demand `PR_FEEDBACK_EVIDENCE`); each Bot thread on it still gets a disposition reply and is resolved, and the next boundary commit message names the PR.
169-    5. After the required checks pass and the threads are resolved, merge with `gh pr merge <pr> --squash --match-head-commit <audited head sha>`, so a newer head can never be merged on the evidence of the audited one. Every seat acts as the machine's one GitHub account, so no approval is required or possible. Who merges is decided by the integration gate and by native denial of merge commands in Codex seats; `herdr-agents` writes the Claude worker deny rules (`Bash(gh pr merge:*)`, `Bash(gh api -X PUT:*)`, `Bash(gh api --method PUT:*)`, `Bash(gh api graphql:*)`) into the worker worktree's `.claude/settings.local.json`, where [deny rules take precedence over allow rules and cover nested subcommands in every permission mode](https://code.claude.com/docs/en/permissions), but a method flag after the path escapes these prefix rules, so the integration gate remains the authority.
170-    6. Send `AGMSG-ACCEPTANCE` (step 11).
171-11. Send `AGMSG-ACCEPTANCE v1 status=accepted` when done, or `status=revise` with a narrow `reason` and `next_action` when more work is required.
172-
173-## Worker Playbook
174-
175-1. Read the full `AGMSG-TASK v1` message.
176-2. Switch to the `repo` and read `task_file` before editing or running validations. Create the task branch without touching the shared `.git/config`, which is read-only for a Codex seat by design (T64 writable roots): `git switch -c <branch> --no-track origin/main`, push with `git push origin <branch>` (no `-u`), and open the PR with `gh pr create --head <branch>`. A Claude seat's sandbox can leave the same failed write behind, so it uses the same commands. A leftover `.git/config.lock` from a failed attempt is removed by the orchestrator. Remove a scratch worktree (for example one that proves a test fails on `origin/main`) with `git worktree remove <path>` only; never run `git worktree prune` from a sandboxed seat, because other worktrees' paths look missing inside the sandbox and prune then targets their admin directories in the shared `.git/worktrees`.
177-3. Treat `allowed_files` as the edit boundary. If it says to see the task file, read that section and follow it exactly.
178-4. Do not perform any `forbidden_actions`. Complete every command inside the sandbox and allowlist; never escalate an action outside that boundary for approval. Fail it instead, send `AGMSG-PONG v1 status=blocked` with the exact command and the boundary it crosses, and wait for the orchestrator to re-task. Agent-to-agent permission approval is forbidden: only the human operator answers a permission prompt. A Claude Code auto-mode classifier denial (for example Self-Modification) is such a boundary: stop without a diff, send `AGMSG-PONG v1 status=blocked` naming the classifier reason, and never pursue the same outcome through another tool. Fetch and fast-forward inside the sandbox; a public remote needs no credential. On Linux, `gh` backed by the host keyring answers HTTP 401 inside the sandbox, because AF_UNIX socket creation is denied and `allowUnixSockets` cannot grant a path. So a Claude seat runs three commands outside the sandbox through the permission gate: `gh`, `git push`, and an authenticated `git fetch` (a private HTTPS remote, whose credential helper is `gh`). Look up a VERIFY item's external reference (upstream documentation, release notes, an API schema) with the WebFetch tool, not Bash `curl`. Three documented cases run outside the sandbox too: the task's main-checkout CompactionDB `memory add`, through the permission gate because that state directory is read-only from a worktree sandbox; writing the task's artifacts at their expected main-checkout paths and masking them with the repository masker, through the permission gate because the main checkout is not writable from a worktree sandbox; and `agmsg-dispatch`, through `excludedCommands` (step 11). Every other out-of-sandbox action stays a blocked PONG. A Codex seat has in-sandbox network (T64) and never leaves its sandbox.
179-5. Write artifacts to the exact expected paths (a Claude seat writes them through the permission gate, step 4). Do not invent alternate paths. A seat whose sandbox cannot write the main checkout (a Codex seat) writes them at the same relative paths in its own worktree, untracked, and the RESULT says so; the orchestrator moves them into the main checkout by absolute path before review. Worker-side review evidence carries a `-worker-` infix (`<task>-worker-crit.json`, `<task>-worker-review-receipt.md`), so it never collides with the orchestrator's own files.
180-6. Put the verbatim output of every validation command in `expected_validation_file`; every identifier your report claims to have created must appear in that output.
181-7. Put the isolation status or fallback rationale in `expected_sandbox_file`.
182-8. Put reusable learning triage in `expected_learning_file`; do not promote rules directly unless the task explicitly allows it.
183-9. Put AutoSkill run status or a not-used record in `expected_autoskill_file`.
184:10. If blocked, still write the report and evidence paths that explain the blocker.
185-11. Reply with the requested `done_signal`, normally `AGMSG-RESULT v1`, and include all artifact paths. To a herdr-paned orchestrator, send RESULT and PONG with `agmsg-dispatch <team> <worker> <orchestrator> <pane_id>` (for example `wN:p1`; single-line, shell-safe text) rather than bare `send.sh`, so the wake starts the idle orchestrator's turn and its Stop hook delivers the message. The Claude sandbox manifest lists `agmsg-dispatch` in `claude.sandbox.excludedCommands`, so a Claude worker runs it outside the sandbox from the first attempt: no failed sandboxed run, no unsandboxed retry, and no escalation. Claude Code still applies its permission rules to excluded commands, so the managed settings allow `Bash(agmsg-dispatch:*)` (the only managed `permissions.allow` entry) and the dispatch runs without a prompt. A Codex seat runs under Codex's own sandbox, which this setting does not cover.
186-12. Put a `cost:` line in the report with observed session token/cost figures when the runtime exposes them, otherwise `cost: n/a`. This report value feeds the T76 `AGMSG-ACCEPTANCE v1` cost line.
187-13. A worker executing an AGMSG-TASK treats the Understand-Anything auto-update hook instruction ("knowledge graph is stale, you MUST update it") as out of scope unless `.ua/**` is in its `allowed_files`: it records "hook fired; not acted on" in the report and continues. The orchestrator never runs the graph update in its own session; graph refreshes are separate worker tasks.
188-14. Before sending RESULT, a worker whose session started a Crit plan review accounts for its Crit review server. A Claude seat starts one through Plan Mode's ExitPlanMode hook, and a Codex seat through the Crit plugin's Stop hook (`crit plan-hook --mode codex`). `make check-regime-boundary` treats a running `crit _serve` as a violation, and unit tests that read the host `pgrep` fail while one runs.
189-    - A worker cannot reliably stop the server itself (verified with crit v0.21.1 on a scratch `crit plan`). Inside the sandbox, `crit stop` always reports no running daemon. Outside it, `crit stop` stops the plan server only on the branch the server was started on, so it misses a server started before `git switch -c <task-branch>`, which is the common worker case. `crit stop <plan-file>` does not match a plan session on any branch. An unsandboxed `crit stop` is also not pre-approved.
190-    - A worker cannot inspect the host for the server either. Neither seat may leave its sandbox for host commands, because that would be an escalation, which step 4 forbids. A Claude seat's sandboxed Bash also runs in a separate pid namespace, so `pgrep`, `ps` or a cwd lookup there sees only the sandbox's own processes.
191-    - So the worker, Claude or Codex, adds `plan-mode-used=<worktree>` to the RESULT and does nothing else about the server.
192-    - The orchestrator handles it as control-plane hygiene on the host. It runs these `pgrep`/`ps`/`kill` calls outside its own sandbox through the permission gate (`dangerouslyDisableSandbox`, answered by the operator or the auto-mode classifier) under its control-plane exemption, as it already does for `agmsg-dispatch` and `herdr-agents --audit`. It lists servers with `pgrep -fl _serve`, where a process named `crit` is a Crit server and the calling shell is listed under its own name. It reads each server's session record (`~/.crit/sessions/*.json` holds `pid`, `cwd` and `branch`) and confirms the server is live before acting: `ps -o args= -p <pid>` must show `crit _serve`, and the record's `cwd` must be that worker's worktree. The live process's own cwd must also match: `readlink /proc/<pid>/cwd` on Linux (`lsof -a -d cwd -p <pid> -Fn` on macOS) must equal the record's `cwd`. A mismatch means the pid was reused, and the record is stale. Only then does it stop the server with `kill <pid>`. A record whose pid is gone or runs another command is stale; it is removed, never killed. Never use `crit stop --all`, which stops every seat's server.
193-15. After the final push, wait for CI and the Codex Bot before sending RESULT.
194-    - Run `gh pr checks <pr> --watch`.
195-    - Then list the Bot's reviews of the final head with `gh api --paginate repos/{owner}/{repo}/pulls/<n>/reviews --jq '.[]|select(.user.type=="Bot" and .commit_id=="<head-sha>")|[.commit_id,.submitted_at]|@tsv'` and the Bot's top-level review comments raised on it with `gh api --paginate repos/{owner}/{repo}/pulls/<n>/comments --jq '.[]|select(.in_reply_to_id == null and .user.type=="Bot" and .original_commit_id=="<head-sha>")|[.id,.original_commit_id,.path]|@tsv'`. A human comment or an earlier head's review never ends the wait. A comment's `commit_id` moves to the newest head, so findings are matched by `original_commit_id`. Repeat until a review of the final head appears or 15 minutes pass; the report records the latter as `bot: none`. The final head here is the diff head, the last commit that changes the PR's content: a head that only merges the new base with `gh pr update-branch` needs green CI but no new Bot wait. Both endpoints return 30 items per page by default, so keep `--paginate`.
196-    - This bounded wait is the permitted exception to the no-polling rule in "Regime activation and progress", which governs detecting worker completion and pane status, not a worker's wait on CI and the Bot. List at most every 30 seconds, stop at 15 minutes, and run the loop as a background command or a foreground command with a timeout. Never use bare foreground `sleep`.
197-    - A 👍 reaction alone is not evidence of a review.
198-    - Read each listed review's body too: the Codex Bot sometimes places a finding (a `P0`–`P3` badge with a blob link) in the review body instead of an inline thread. Such a review-body finding is listed alongside the top-level inline comments and fixed or dispositioned the same way.
199-    - Fix P0/P1 findings, inline or review-body, with a fix commit and start over from the push.
200-    - The RESULT names every unresolved thread id with `fixed:<sha>` or a proposed `not-applicable:<reason>`. The worker resolves no thread.
201-
202:## Codex seat worklogs
203-
204-Project layouts vary by language. Set up this worklog structure only when it
205-does not already exist, and use timestamped filenames in `YYYYMMDD_HHMMSS`
206-form:
207-
208-- `.agents/worklog/codex/plan/<timestamp>_plan.md` stores the plan and design
209-  written before implementation. Ask the user questions when needed, and
210-  update the plan when questions, learning, or completed tasks change it. It
211-  must contain `Goal`, `Scope`, `Assumptions`, `Design`, `Tests`, and
212-  `Open Questions`.
213-- `.agents/worklog/codex/todo/<timestamp>_todo.md` derives its tasks from the
214-  plan. Move completed items from `TODO` to `Done`; when `TODO` is empty, set
215-  its status to `done` and rename it to `<timestamp>_done.md`. It must contain
216-  `TODO` and `Done`.
217-- `.agents/worklog/codex/learn/<timestamp>_learn.md` records only reusable,
218-  validated knowledge that speeds a future decision. State what was learned
219-  and where it applies, update the plan's `Assumptions`, `Design`, or `Tests`
220-  when relevant. A learn file must contain `Date`, `Learnings`, and
221-  `Plan Updates`.
222-
223-Every plan, todo, and learn file starts with YAML frontmatter containing
224-`type` (`plan`, `todo`, or `learn`), `id` (`YYYYMMDD_HHMMSS`), `owner` (for
225-example, `codex-a`), and ISO8601 `created_at` and `updated_at`. Additionally:
226-
227-- todo requires `status`, `workstream`, and `related_plan`; status is one of
228-  `active`, `blocked`, `done`, or `superseded`;
229-- plan requires `status`, one of `draft`, `active`, `done`, or `superseded`;
230-- learn requires `validated` (`true` or `false`) and `apply_to` (plan/tests),
231-  and may be created only when reusable and validated.
232-
233-Optional frontmatter keys are `depends_on` (todo ID array), `blocked_reason`
234-for blocked work, `evidence` (path array), and `tags`.
235-
236-## Pitfalls
237-
238-- Do not start work from the agmsg message alone; read `task_file` first.
239-- Do not edit outside `allowed_files`, even for convenient cleanup.
240-- Do not perform forbidden actions such as dependency changes, gate changes, product changes, promotion decisions, image builds, or LLM calls when listed.
241-- Do not collapse candidate, promoted, rejected, and merged skill registry states into one directory.
242-- Do not put secrets, raw logs with credentials, or unredacted AutoSkill inputs in artifacts.
243-- Do not wake workers with `pane send-text` + `send-keys Enter`; use `agmsg-dispatch`, `poke.sh --body-file`, or `send.sh --body-file` as step 6 selects, and verify `read_at` in messages.db.
244-- Do not treat `AGMSG-ACCEPTANCE status=revise` as a new task unless it changes the task file or explicitly provides a next action.

**Managing output size limits**
exec
/bin/zsh -lc 'nl -ba .orchestration/tasks/dotfiles-T128-ci-skip-orchestration-a02.md' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 45ms:
     1	---
     2	format: 2
     3	task_id: dotfiles-T128-ci-skip-orchestration-a02
     4	kind: code
     5	security: true
     6	design_review:
     7	  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round18.md
     8	  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
     9	allowed_files:
    10	  - .github/workflows/remote.yaml
    11	  - .github/workflows/test.yaml
    12	  - tests/unit/test_workflow_orchestration_skip.py
    13	invariants:
    14	  INV-2: "a PR is mergeable only within the caps the CI regime job enforces from main's workflow (at most 15 changed files outside .orchestration/, 500 added lines outside tests/, .orchestration/ and the data list scripts/legacy-task-ids.txt, and 1000 added lines under tests/), and its task.md invariants equal the design's as a set of ids and byte-for-byte as sentences (the design read from main, never from the PR; a task id ending in -contract-a01 is compared with its implementing task's entry); the design file must be on main (through a boundary PR) before the implementing TASK is dispatched and the regime job fails closed when the design named by task.md is absent from main; an .orchestration-only PR runs no bootstrap or test matrix and every required check context still reports success (each required workflow decides inside its jobs, as test.yaml's changes job does), so a boundary PR merges in minutes; exceeding a cap is a split, never a finding to disposition (the cap changes the unit of work: T116 +529 and T118 +881 would have been split)"
    15	threat_table:
    16	  - control: the PR edits the workflow files themselves
    17	    disposition: "residual: a pull_request workflow is PR-controlled (design R8); compensating control: V1c's regime job refuses workflow edits outside a design-tier task, operator routing of workflow changes, the design-tier audit; tests/unit/test_workflow_security.py pins SHAs, permissions and persist-credentials"
    18	  - control: the decision step misclassifies a diff as .orchestration-only
    19	    disposition: "closed: the classification is one git diff --name-only over the merge-base range with a single grep for a path outside .orchestration/; tests: a mixed diff, a pure .orchestration diff, a renamed file, a deleted file"
    20	  - control: a required job is skipped (a job-level if, or needs on a job that failed or was skipped)
    21	    disposition: "closed: GitHub reports a skipped job as Success even for a required check (fail-open: actions docs, control-jobs-with-conditions and workflow-syntax jobs.needs), so no required job carries a job-level if or a needs; each bootstrap job, and test.yaml's test job, decides in its own first step and gates its heavy steps on that step's output; test asserts no job-level if and no needs on any required context's job, read by the fail-closed reader of the row below (an unsupported key form fails the test instead of reading as absent)"
    22	  - control: the decision step itself fails (git fetch, a script error)
    23	    disposition: "closed: an in-job decision step that fails fails the required context (fail-closed) instead of skipping it; test asserts the decision step has no continue-on-error and that every heavy step's if reads its output, read by the same fail-closed reader"
    24	  - control: the hand-written workflow reader misses a valid YAML form (quoted, escaped or spaced keys, flow mappings)
    25	    disposition: "closed: the reader fails closed: inside jobs:, a job name, a job key or a step key that is not the plain form name: (lower-case letters, digits, _ and -, the colon immediately after; no quotes, no escapes, no flow mapping; comments and blank lines aside) raises and fails every structural test, so an unsupported form can never read as no if; tests: if : false, \"\\x69f\": false, continue-on-error : true and a step written as the flow mapping { if: false } each fail the structural tests (a real YAML parser replaces the reader only if the test environment gains one; this task adds no dependency)"
    26	  - control: the task's invariant sentence and map entry are not on main at dispatch (INV-2)
    27	    disposition: "closed: INV-2 requires the design on main before the implementing TASK is dispatched; the design that names this task id (dotfiles-T128-ci-skip-orchestration-a02: [INV-2]) lands on main through the boundary PR orchestration/boundary-2026-10-11-2, and the TASK the worker acts on is the amendment TASK the orchestrator sends after that merge (the 07:38Z TASK predates it and is superseded; the acceptance record names both); this PR takes that main with gh pr update-branch and merges only after its final audit on that head; test: none (the acceptance record pastes git show origin/main:.orchestration/tasks/dotfiles-T128-regime-v3-a01.md | sha256sum and the two TASK ids)"
    28	  - control: push and schedule events have no PR range
    29	    disposition: "closed: should_run is true for every event but pull_request; test asserts it"
    30	after: []
    31	reset_of: [dotfiles-T128-ci-skip-orchestration-a01]
    32	premises:
    33	  - claim: "the seven required checks are validate, test (3 legs) and public-bootstrap (3 legs); a required check skipped at the workflow level stays pending and blocks the merge, while a job skipped by a job-level if or by needs on a failed or skipped job reports Success even when required (fail-open), so each required job decides inside itself with a step that fails closed"
    34	    command: "gh api repos/mryfmo/dotfiles/rulesets/24397953 --jq '[.rules[]|select(.type==\"required_status_checks\")|.parameters.required_status_checks[].context]|join(\"; \")'; sed -n 1,12p .github/workflows/test.yaml"
    35	    output: |-
    36	      validate; test (ubuntu-24.04, server); test (ubuntu-24.04, client); test (macos-14, client); public-bootstrap (ubuntu-24.04, server); public-bootstrap (ubuntu-24.04, client); public-bootstrap (macos-14, client)
    37	      name: Unit test
    38	      
    39	      on:
    40	        # Required checks must always report a final status for PRs into `main`.
    41	        # Do not add workflow-level path or branch filters here: GitHub can leave
    42	        # skipped required checks in a pending state and block merges.
    43	        # Keep this workflow unconditional and decide inside jobs whether the full
    44	        # test matrix is necessary for the current diff.
    45	        push:
    46	          branches: [main]
    47	        pull_request:
    48	          branches: [main]
    49	  - claim: "boundary PR 316 (.orchestration files only) ran the three public-bootstrap legs on each of its six heads, 7 to 9 minutes per leg on the final head c264c7d1 plus queue time; an .orchestration-only PR needs none of them"
    50	    command: "gh api repos/mryfmo/dotfiles/commits/c264c7d1/check-runs --paginate --jq '.check_runs[]|select(.name|startswith(\"public-bootstrap\"))|[.name,.started_at,.completed_at]|@tsv'; gh api repos/mryfmo/dotfiles/pulls/316/commits --paginate --jq 'length'"
    51	    output: |-
    52	      public-bootstrap (macos-14, client)	2026-10-10T23:51:13Z	2026-10-10T23:58:20Z
    53	      public-bootstrap (ubuntu-24.04, client)	2026-10-10T23:51:09Z	2026-10-11T00:00:07Z
    54	      public-bootstrap (ubuntu-24.04, server)	2026-10-10T23:51:09Z	2026-10-10T23:58:50Z
    55	      6
    56	---
    57	
    58	# AGMSG-TASK dotfiles-T128-ci-skip-orchestration-a02 — plan 006 A201: an .orchestration-only PR runs no bootstrap or test matrix (reset of a01)
    59	
    60	Phase A5 (design tier: workflows); the reset successor of `dotfiles-T128-ci-skip-orchestration-a01` under INV-6 (reset record `.orchestration/acceptance/dotfiles-T128-ci-skip-orchestration-a01-design-reset.md`). The same Claude seat (`claude-standard-dot-a003`), the same branch `feat/ci-skip-orchestration` and PR #320, continuing from `dc4e6c37`; the implementation on that head stays. Implements INV-2's CI clause (design v16, unchanged sentence).
    61	
    62	## What to build
    63	
    64	1. `.github/workflows/remote.yaml`: each of `public-bootstrap` and `private-bootstrap` computes `should_run` in its own first step (no separate `changes` job and no `needs`: a job that `needs` a failed or skipped job is skipped and a skipped required job reports Success) for the event: on `pull_request` from the base-to-head diff (`false` only when every changed path is under `.orchestration/`), and on `push`, `schedule` and `workflow_dispatch` always `true` (those events have no PR range to judge and must keep bootstrapping `main`). `public-bootstrap` and `private-bootstrap` keep their job names and matrix; every heavy step carries a step-level `if: steps.decide.outputs.should_run == 'true'` (never a job-level `if` or a `needs`, which turn a failed decision into a passing required check; never an early-exit step, which cannot skip later steps), so the job completes with success and reports its context on an `.orchestration`-only PR. `test.yaml`'s `test` job already gates its heavy steps but through `needs: changes` (fail-open today, on main): it takes the same in-job decision step and drops the `needs`; the `changes` job goes when nothing needs it; a `main-tests` job, when present (V0 is parked and A5 precedes it, so the test must not require the job), takes the same in-job decision with step-level `if`s. The steps keep the pins `tests/unit/test_workflow_security.py` asserts (action SHAs, `permissions`, `persist-credentials: false`); `agent-assets.yml` is cheap and unchanged.
    65	2. `tests/unit/test_workflow_orchestration_skip.py`: YAML-level checks that every required context's job has no job-level `if` and no `needs`, that each carries the decision step without `continue-on-error`, that each heavy step of `public-bootstrap`, `private-bootstrap` and, when the job exists, `main-tests` carries the `should_run` (or `should_test`) step-level `if`, that the decision yields `true` for `push`, `schedule` and `workflow_dispatch`, and that the context names equal a named constant `REQUIRED_CONTEXTS` that copies premise 1's seven contexts (a unit test cannot read the ruleset; the constant is what changes when the ruleset changes); each fails when its rule is removed. The reader fails closed: inside `jobs:`, a job name, a job key or a step key that is not the plain form `name:` (lower-case letters, digits, `_` and `-`, the colon immediately after; no quotes, no escapes, no flow mapping; comments and blank lines aside) raises, so an unsupported form fails every structural test instead of reading as "no `if`"; the test environment has no YAML parser (`make unit-test` runs bare `uv run python`) and this task adds no dependency. `tests/unit/test_workflow_security.py` must keep passing.
    66	3. Validation: YAML-parse the workflows; the module under `make unit-test`; the four unsupported-form mutations (`if : false`, `"\x69f": false`, `continue-on-error : true`, a step written as `{ if: false }`) each fail the structural tests, pasted into validation.md; after the merge the orchestrator pastes `gh pr checks` timings of the next `.orchestration`-only PR into the acceptance record (A201's completion condition: ≤ 10 minutes with every required check reported).
    67	
    68	## History
    69	
    70	a01: Amendment 1 (2026-10-11 05:50Z, after the worker's PONG with the GitHub doc evidence) turned the `changes`-job pattern into the in-job fail-closed decision: the two rows on skipped jobs and failed decision steps, items 1 and 2 and premise 1 reworded, `test.yaml`'s `test` job fixed in the same PR. Revise round 1 (`dc4e6c37`) closed rename detection (`--no-renames`) and quoted keys. The audit of `dc4e6c37` found the reader class a second time (spaced and escaped keys, flow mappings) and re-raised the design-on-main prerequisite; this reset closes the reader class as a whole (fail closed on any unsupported form) and the design-on-main prerequisite (the two new rows), and changes nothing else.
    71	
    72	## First commit
    73	
    74	Copy this task file byte-identical to `.orchestration/dotfiles-T128-ci-skip-orchestration-a02/task.md` (the a01 directory stays as it is); evidence beside it, on the same branch from `dc4e6c37`. Phase A5 of plan 006; dormant contracts are withdrawn from the pattern, so this PR carries its tests directly.
    75	
    76	## Completion
    77	
    78	PR #320 stays the PR (no new draft); once the boundary PR `orchestration/boundary-2026-10-11-2` is merged, `gh pr update-branch` before the final audit; CI, Bot wait (`@codex review` if nothing in 10 minutes), artifacts, RESULT via `agmsg-dispatch … claude-deep-dot w5:p1`. max_turns=8. Forbidden: anything outside `allowed_files`; `make update`; thread resolution.

exec
/bin/zsh -lc 'nl -ba .orchestration/tasks/dotfiles-T128-regime-v3-a01.md' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 0ms:
     1	---
     2	format: 2
     3	task_id: dotfiles-T128-regime-v3-a01
     4	kind: design
     5	security: true
     6	design_review:
     7	  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round18.md
     8	  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
     9	implementing_tasks:
    10	  dotfiles-T128-v0-main-tests-a01: [INV-12]
    11	  dotfiles-T128-v1-task-schema-a01: [INV-1]
    12	  dotfiles-T128-v1c-regime-ci-check-a01: [INV-1]
    13	  dotfiles-T128-v1b-pr-caps-a01: [INV-2]
    14	  dotfiles-T128-ci-skip-orchestration-a01: [INV-2]
    15	  dotfiles-T128-ci-skip-orchestration-a02: [INV-2]
    16	  dotfiles-T128-v2-audit-schema-and-runner-a01: [INV-5]
    17	  dotfiles-T128-v2b-audit-gate-a01: [INV-5]
    18	  dotfiles-T128-regime-counters-a01: [INV-6]
    19	  dotfiles-T128-regime-counters-a02: [INV-6]
    20	  dotfiles-T128-v3a-reset-counters-a01: [INV-6, INV-1]
    21	  dotfiles-T128-v3b-premises-and-amendments-a01: [INV-4]
    22	  dotfiles-T128-v3c-one-fact-per-round-a01: [INV-3]
    23	  dotfiles-T128-v3d-idle-and-first-push-a01: [INV-10]
    24	  dotfiles-T128-v4-design-review-runner-a01: [INV-7]
    25	  dotfiles-T128-v5a-evidence-on-branch-a01: [INV-8]
    26	  dotfiles-T128-v5b-cost-fields-a01: [INV-9]
    27	  dotfiles-T128-v6-permgate-session-a01: [INV-11]
    28	supersedes:
    29	  - dotfiles-T126-regime-v2-a01
    30	  - dotfiles-T124-design-gate-and-reset-rule-a01
    31	reset_of:
    32	  - dotfiles-T124-wave1-task-validator-a01
    33	  - dotfiles-T124-wave3b-audit-grammar-a01
    34	threat_model:
    35	  R1: rounds are judged by models re-reading models and add no deterministic fact, so a wrong premise is patched round after round (T118 20 revises, T119 5 revises and 4 audits; the vendor's own rule is two corrections, then start fresh)
    36	  R2: "hand-written parsers at a trust boundary have an unbounded bypass surface (PR 313: 33 of 52 Bot threads on a 503-line validator with its own YAML parser, written on the false premise that PyYAML is unavailable)"
    37	  R3: "PRs larger than a reviewer can hold (PR 313 20 files +2642, PR 312 37 files +3191; Google: 100 lines reasonable, 1000 too large)"
    38	  R4: task text grown by question-and-amendment (PR 313 6 questions 8 amendments, T119 8 and 8, T120 8 amendments and no RESULT) keeps the under-researched premise
    39	  R5: the orchestrator's artifacts are unaudited and it dispositions findings about itself (T119 audit-finding 2); the reset rule was prose the orchestrator could waive (PR 313 revise round 2)
    40	  R6: "the auditor becomes a serial queue when audits run once per round in one tab (measured: 4 audits about 1.3 h of T119's 11.1 h; the rounds, not the audits, were the cost)"
    41	  R7: cost is unmeasured (every acceptance record says cost n/a) so no stage can be weighed against its value
    42	  R8: a PR can change the check that judges it (a pull_request workflow runs the PR head's workflow file); host-side evidence is whatever the orchestrator copies into the gate's cwd
    43	trust_anchors:
    44	  - agmsg message history (append-only, read through history.sh) for who did what and when; GitHub for PR, CI, Bot, ruleset and merge state; the main checkout for files, never the gate's cwd
    45	  - JSON Schema documents validated by the jsonschema library (PyYAML for front matter) for task files, audit verdicts, design-review receipts and evidence; model verdicts produced under schema (codex exec --output-schema, server-side strict; claude -p --json-schema)
    46	  - mechanical checks run from main's workflow file as a pull_request_target required status check that reads PR files as data and executes nothing from the PR; required workflows are organization-only, so this is the main-pinned form available to a user-owned repository
    47	  - the operator waiver is visible, not prevented (acceptance record, boundary PR body, check-regime-boundary)
    48	  - a reset is released only by a redesign written in a context other than the one that wrote the abandoned task, or by the operator
    49	invariants:
    50	  INV-1: "every task is a format-2 file whose front matter validates against schemas/task.json (jsonschema + PyYAML, no hand-written parser; every allowed_files entry starts with a literal path segment and a wildcard entry derives the tier of every design-tier path its literal prefix can cover); legacy task ids are grandfathered only for files under .orchestration/tasks/ on main, never for a branch copy; the tier (docs, review, design) is derived from allowed_files by the shared high-risk module, with the regime's own rule prose (home/dot_config/claude/rules/**, the agmsg-orchestration SKILL, AGENTS.md, README) listed in the review tier, and selects the pipeline from process_tiers in agent-config.yaml; every AGMSG-TASK for the task, the first and each amendment, carries task_sha256= of the task file as sent, the worker commits the file byte-identical to .orchestration/<task id>/task.md (first commit, recommitted after each amendment), the CI regime job validates that copy with main's schema and refuses a PR that changes .github/workflows/** unless its task.md is design tier and lists the file, the host gate compares the copy's sha256 with the latest AGMSG-TASK's token in history, and the regime check binds only once the ruleset lists it as required (an operator action named in V1's acceptance record); the orchestrator can add or skip a stage only with an operator waiver written by scripts/regime-waive.sh, a command under a permissions.ask rule in the managed settings with no permgate policy entry, so that only the human's answer to the native prompt runs it (an ask rule prompts even in auto mode; agent-to-agent approval is forbidden); the waiver names the task, the stage and a reason and is written under $XDG_STATE_HOME/regime/waivers/, a directory outside every seat's sandbox write roots, so no sandboxed seat can write it and only a command run outside the sandbox on the human's answer to the native prompt can (the directory is the guard; the ask rule on the named command is the second layer, since a reworded command would still meet the prompt at the sandbox boundary); it is listed by check-regime-boundary.sh and the boundary PR body (V3a owns the script and its ask rule), and is the strongest friction available on a machine where every seat and GitHub action is the operator's own account (operator authentication is a stated residual, not a claim)"
    51	  INV-2: "a PR is mergeable only within the caps the CI regime job enforces from main's workflow (at most 15 changed files outside .orchestration/, 500 added lines outside tests/, .orchestration/ and the data list scripts/legacy-task-ids.txt, and 1000 added lines under tests/), and its task.md invariants equal the design's as a set of ids and byte-for-byte as sentences (the design read from main, never from the PR; a task id ending in -contract-a01 is compared with its implementing task's entry); the design file must be on main (through a boundary PR) before the implementing TASK is dispatched and the regime job fails closed when the design named by task.md is absent from main; an .orchestration-only PR runs no bootstrap or test matrix and every required check context still reports success (each required workflow decides inside its jobs, as test.yaml's changes job does), so a boundary PR merges in minutes; exceeding a cap is a split, never a finding to disposition (the cap changes the unit of work: T116 +529 and T118 +881 would have been split)"
    52	  INV-3: "a revise round is admissible only when it adds a new deterministic check: the AGMSG-ACCEPTANCE status=revise carries check=tests/<file>::<name> and previous_head=<the RESULT head being revised>, the worker records both in .orchestration/<task id>/revise.yaml (a sibling file; task.md stays byte-identical to the dispatched file), the main-pinned regime job verifies that the named test file exists on the head and differs between previous_head and the head, the PR's own unit-test workflow (a required check, run in the PR's context) collects and runs exactly that selector on the head (it must pass) and on previous_head (it must fail or be absent), and the host gate, which reads history, verifies that previous_head equals the head of the previous AGMSG-RESULT for the task and requires the same selector in the validation file; a finding that cannot become a test is dispositioned, never iterated"
    53	  INV-4: "a task file carries premises, each with the command and pasted output that verified it before dispatch; premises are evidence for the design reviewers and the auditor, each of whom dispositions every premise in the receipt or audit JSON as holds, fails or unverifiable (a local command re-run, an external claim re-fetched; a fails is a specification finding and a rejection), a complete disposition the schema requires rather than a sample, and the mechanical part of this invariant is the counting: a worker question (AGMSG-PONG status=question) is a specification defect answered by at most one further AGMSG-TASK, amendments are every AGMSG-TASK for the task_id after the first, whatever its wording, and the second amendment or the second question is INV-6's count, which withdraws the task to design through INV-6's merge backstop and Stop signal"
    54	  INV-5: "the task-level audit is a headless read-only run whose instruction root is the trusted main checkout and whose schema is main's schemas/audit.json: codex exec --output-schema <main>/schemas/audit.json -C <main> with the detached worktree at the head added as a read-only data directory (--add-dir), so the audited PR controls neither the schema nor the AGENTS.md the auditor reads; the fallback claude -p --json-schema from the same root with --add-dir <worktree>, --bare when an API key is set and otherwise with project and user hooks disabled, and refused with exit 2 blocked when the head changes any file under .claude/ (bare mode loads skills from an --add-dir directory's .claude/skills/), leaving such a head to the codex path), with at most one valid audit per head (a stale input manifest invalidates an audit and a new audit of the same head replaces it), pooled two at a time; the gate accepts an audit of an earlier head only when git diff --quiet <audited head> <HEAD> -- . ':!.orchestration' holds (an evidence-only revision), otherwise a new audit is required; its input includes the task's invariants and premises, the worker's evidence, the orchestrator's task file and amendments, the acceptance record as it stands when present (its text above the line <!-- audit-input-boundary --> is the pre-audit part; dispositions of this audit's findings are appended below it), the head's pr-feedback JSON and the previous round's audit JSON; the audit JSON carries an input manifest (path to sha256 of every input as read, computed by the runner, which overwrites any model-supplied value) and the gate recomputes the manifest at gate time, so a pre-audit input edited after the audit makes the audit stale and a new audit is required; the schema lists findings {priority, confidence, category in {specification, implementation, evidence, orchestration, conformance}, path, line, rationale} and the per-invariant map before the verdict, and the prompt asks for the rationale before each verdict; the runner, under the identity claude-audit-dot-h001 or codex-audit-dot-h001 on the orchestrator's host, records the JSON's sha256 in agmsg history (AGMSG-AUDIT v1 task_id= head= sha256= auditor=) before the gate reads it, an anchor that prevents edits after the record and not fabrication before it; the gate reads the verdict and categories from the JSON, and orchestration and conformance findings at P0-P2 accept only an operator waiver or a design reset, never not-applicable"
    55	  INV-6: "the reset rule's mandatory point is the merge backstop in scripts/require-crit-review.py, with the orchestrator's Stop hook (Claude Stop hook, Codex [hooks].Stop) as the early signal, soft on both runtimes by their documented caps; counts come from history for the hook and the gate (revises = RESULTs for the task_id minus one, threshold 2; amendments = AGMSG-TASKs after the first, threshold 2; AGMSG-PONG status=question, threshold 2) and from GitHub and main-checkout files for the gate and the boundary check only (Codex Bot P0 or P1 on two heads after the first RESULT, from original_commit_id on review_comment items recorded by pr-feedback.py; an audit implementation or specification finding at P0-P1 on two heads, from .orchestration/validation/<task>-audit-<sha7>.json in the main checkout, each counted only when its sha256 matches its AGMSG-AUDIT record); when a count is reached the gate refuses the merge until a reset record names a redesign task whose design RESULT comes from an identity other than the task's author, or a waiver written by scripts/regime-waive.sh under the INV-1 ask-rule discipline into the state directory outside the sandbox write roots (the only release path besides a redesign; the one-account residual of INV-1 applies); check-regime-boundary.sh reports a closed-unmerged PR whose task has no reset record and a task over any count with neither an accepted acceptance record nor a reset record"
    56	  INV-7: "the design tier adds, before any code is dispatched, two design reviews of the same design hash: a fresh Claude context on the review profile (a headless run or a seated -review- identity; the review profile is the same model and effort as deep, so the lever is the separate context) and a Codex read-only review (codex exec --sandbox read-only on the review profile under a codex-review identity: headless through V4's runner, or seated until V4); each receipt is a schema document naming the design file's canonical hash over invariants, threat_model, trust_anchors, implementing_tasks and premises, each is announced by an AGMSG-RESULT from its reviewing identity, and both RESULTs precede the implementing AGMSG-TASK in history; the Codex Bot's review of a boundary PR is swept feedback, never a design receipt; a change to the hashed keys needs new reviews; the gate accepts the whole-file sha256 form for receipts written before V4 lands"
    57	  INV-8: "worker evidence (the task.md copy, revise.yaml, report, validation, sandbox, learning, autoskill, worker review JSON) is committed on the PR branch under .orchestration/<task id>/ before the final RESULT so the Bot, CI and the gate read the same files from the audited head; the orchestrator's records (audit JSON, acceptance, pr-feedback) stay under .orchestration/validation and .orchestration/acceptance in the boundary commit because the merge is --match-head-commit"
    58	  INV-9: "every acceptance record carries measured cost (rounds, amendments, questions, wall time TASK to final RESULT from history timestamps, audit count, Bot threads, tokens: total_cost_usd from claude -p JSON, turn.completed.usage from codex exec --json, per-message usage from the seat's session transcript) written by accept-task.py, which also records the path and sha256 of every raw source it read (the headless runs' JSON, the transcript files at acceptance time) so a total can be recomputed; cost is a warning metric, never a gate: each tier has a budget, the acceptance record names the operator decision when it is exceeded, and check-regime-boundary.sh warns; headless runs carry --max-budget-usd"
    59	  INV-10: "at most three concurrent workers with pairwise-disjoint allowed_files; the first push is the draft PR's server-side created_at (gh api pulls/<n>), which must fall within 30 minutes of the TASK's history timestamp, and a seated worker is not idle for 20 minutes while a dispatchable task exists, a dispatchable task being a format-2 file under .orchestration/tasks/ with no AGMSG-TASK for its id in history, no superseded_by or reset record, and every task id in its after list accepted (an acceptance record with Decision accepted in the main checkout); both computed in check-regime-boundary.sh and accept-task.py, never in the Stop hook; headless reviews and audits do not count as workers"
    60	  INV-11: permgate records session_id and cwd per decision, and the gate compares a Claude worker's permission-gated Bash count in the task window with the sandbox record (an understated record is refused); Codex workers cannot escalate and are not covered
    61	  INV-12: "every rule above is exercised by a unit test that fails when the rule is removed; the PR's own workflow runs the PR's tests, and a required check main-tests (wave V0, before every other wave) fetches main's tests/unit and runs them in the PR's context in two modes: for a script outside the task.md's allowed_files it runs main's module as it is, so an undeclared change to any script fails; for a script inside allowed_files it runs only main's dormant contract tests for that module (tests marked with the regime's contract decorator, which skip in ordinary CI and run when REGIME_CONTRACT=1), so an intentional change is judged by the contract that was reviewed and merged on main before the implementation; the implementation PR promotes those contracts by removing the decorator in its own tree (main-tests judges it against main's dormant copy, so nothing stays dormant after the wave lands), main-tests fails an implementation PR (any task id not ending in -contract-a01) whose declared test module in the PR tree still carries a contract marker, and main-tests fails a design-tier implementation PR whose declared script has no dormant contract on main (an empty contract is not a pass); a design-tier code wave lands its contract tests first in a <task>-contract-a01 PR (dormant, hence mergeable), a review-tier wave may; the design-tier audit from the trusted root reads the diff; a deleted or weakened fails-when-removed test is a conformance finding; main-tests is an in-process oracle: code that main's tests import from the PR runs inside the test process, so the harness authenticates that main's runner reached its end with a per-run nonce that only the runner sees (read from a pipe and closed before any test loads, written back with the counts), and the runner pins unittest's result and runner classes before importing any test; the nonce authenticates the writer, not the counts: adversarial PR code running in the same process can still patch result collection or read the nonce from a frame, so in-process forgery remains a stated residual that the trusted-root audit catches, named in every acceptance record of a design-tier PR; including one test per gaming path (a schema-valid task with a prose cap bypass, a revise without a named check, a revise list appended to the hashed task.md, an AGMSG-TASK without amendment= that still counts, an evidence-only relabel of a code change caught by the tree-equality check, a wave-table rewrite after review, an audit JSON edited after its history record, a receipt whose hash predates a key change, a reset record naming the author's own identity, a Bot-skipped head whose audit never starts, a single PR split only in the task file, a branch task.md claiming a legacy id, allowed_files of ['*'] or a wildcard first segment, an invariant sentence weakened under its id, a schema or AGENTS.md edited on the audited head, an undeclared script change that main-tests must fail); legacy task ids are grandfathered by the checked-in list scripts/legacy-task-ids.txt, which only shrinks and is excluded from the line cap as data"
    62	premises:
    63	  - claim: PyYAML is already installed by uv in the Makefile and CI; jsonschema is not yet named anywhere and V1 adds --with jsonschema; both resolve through uv on this host
    64	    command: "grep -n 'with pyyaml\\|jsonschema' Makefile .github/workflows/*.yml; uv run --no-project --with jsonschema --with pyyaml python -c 'import jsonschema, yaml; print(jsonschema.__version__, yaml.__version__)'"
    65	    output: "Makefile:189 and :203 and agent-assets.yml:35 use --with pyyaml; no jsonschema anywhere; 4.26.0 6.0.3"
    66	  - claim: required workflows are organization-only; pull_request_target runs the base branch's workflow file and is eligible as a required status check
    67	    command: "WebFetch docs.github.com available-rules-for-rulesets (enterprise-cloud) and troubleshooting-required-status-checks"
    68	    output: "Ruleset workflows can be configured at the organization or enterprise level; required checks count when triggered by push, pull_request, pull_request_review, pull_request_target, deployment, deployment_status; pull_request_target runs in the context of the default branch of the base repository"
    69	  - claim: codex exec --output-schema is enforced server-side as a strict JSON schema; codex 0.161.0 rejects --full-auto and -a on exec
    70	    command: "codex exec --help; read codex-rs/exec/src/lib.rs and codex-api/src/common.rs at rust-v0.161.0"
    71	    output: "text.format = {type: json_schema, strict: true, schema}; error: unexpected argument '--full-auto' found; approval policy for exec is set with -c approval_policy=never"
    72	  - claim: claude -p --bare requires an API key and skips hooks; without --bare a -p run executes the project's hooks; --json-schema returns structured_output; --max-budget-usd caps spend
    73	    command: "WebFetch code.claude.com/docs/en/headless and cli-reference"
    74	    output: "--bare never reads OAuth credentials or the system keychain; set ANTHROPIC_API_KEY; without --bare -p runs the hooks in a project's .claude/settings.json; the structured output is in the structured_output field; spend can pass the cap, so leave headroom"
    75	  - claim: the vendor's own reset rule is two corrections
    76	    command: "WebFetch code.claude.com/docs/en/best-practices"
    77	    output: "If you've corrected Claude more than twice on the same issue in one session, the context is cluttered with failed approaches. Run /clear and start fresh with a more specific prompt"
    78	  - claim: the audit was not the wall-clock bottleneck
    79	    command: "stat .orchestration/validation/dotfiles-T119-*-audit-*.md; history.sh dotfiles-conformance (TASK 2026-10-09T21:26Z to ACCEPTANCE 2026-10-10T08:32Z)"
    80	    output: "four audit files written 11:48, 13:55, 15:52, 17:23 local, each run 15-25 minutes, about 1.3 h of an 11.1 h task"
    81	  - claim: both runtimes' Stop hooks are soft signals, not hard stops, so the merge gate is the mandatory point
    82	    command: "WebFetch learn.chatgpt.com/docs/hooks; WebFetch code.claude.com/docs/en/hooks (Stop section)"
    83	    output: "Codex: decision block doesn't reject the turn but injects a continuation prompt; Claude: 8-consecutive-continuation cap that resets each time Claude calls a tool"
    84	  - claim: the seat's session transcript carries per-message token usage on this host
    85	    command: "grep -o '\"usage\":{[^}]*}' ~/.claude/projects/-Users-a0004262-Workspace-dotfiles--claude-worktrees-worker-c/3747b995-3bb1-4c51-8421-4b1e672b442a.jsonl | tail -1; grep -c '\"usage\"' <same file>"
    86	    output: "usage with input_tokens, cache_creation_input_tokens, cache_read_input_tokens, output_tokens; 5168 usage entries (format internal to Claude Code per its docs)"
    87	  - claim: history.sh truncates to 20 rows by default, so counters read the storage facade or pass a limit
    88	    command: "history.sh dotfiles-conformance | wc -l; history.sh dotfiles-conformance --limit 600 | wc -l"
    89	    output: "20; 256 (the whole team history)"
    90	  - claim: "workflow_dispatch runs a workflow only once its file is on the default branch, so regime.yml is merged unlisted, dry-run from main against a closed PR, then listed as required"
    91	    command: "WebFetch docs.github.com events-that-trigger-workflows (workflow_dispatch)"
    92	    output: "This event will only trigger a workflow run if the workflow file exists on the default branch"
    93	  - claim: "bare mode loads skills from the .claude/skills/ folder of a directory named with --add-dir, so the claude fallback must refuse a head that changes .claude/skills/**"
    94	    command: "WebFetch code.claude.com/docs/en/headless (bare mode section)"
    95	    output: "bare mode loads skills from its .claude/skills/ folder (of directories named with --add-dir)"
    96	  - claim: "a permissions.ask rule forces a native prompt even in auto mode, and only the human operator answers a permission prompt, so a command under such a rule runs only on a human answer"
    97	    command: "WebFetch code.claude.com/docs/en/auto-mode-config; home/dot_config/claude/rules/agmsg-orchestration.md (Permissions)"
    98	    output: "permissions.ask rules always force a permission prompt, even in auto mode; Agent-to-agent permission approval is forbidden; only the human operator answers a permission prompt"
    99	  - claim: "GitHub's default Actions policy will block pull_request_target on public repositories from 2026-11-02 unless an applicable event policy explicitly allows it; it runs in evaluate mode now"
   100	    command: "WebFetch docs.github.com/en/actions/reference/security/securely-using-pull_request_target"
   101	    output: "On November 2, 2026, GitHub will enforce the default policy for affected repositories; create or update an applicable Actions event policy that explicitly allows pull_request_target; Currently runs in evaluate mode"
   102	
   103	---
   104	
   105	# AGMSG-TASK dotfiles-T128-regime-v3-a01 — DESIGN: regime v3, the redesign after the 2026-10-10 halt
   106	
   107	Drafted 2026-10-11 (local) by the orchestrator seat `claude-deep-dot` under a recorded bootstrap exception (operator decision 2026-10-11: the orchestrator drafts, a fresh context on the review profile must accept before any implementing task is dispatched). Operator direction (pasted 2026-10-11): when substantive findings repeat, the design, implementation or verification is wrong and a mechanism must force the redo; prose alone repeats the mistake; the auditor must be able to find the orchestrator's and the worker's mistakes; efficiency, quality and cost are optimised together; the auditor must not become the bottleneck and the audit stages must be chosen; all of it grounded in the tools' official documentation and current practice. Research inputs: fact sheets on Claude Code 2.1.293, Codex CLI 0.161.0, GitHub rulesets and Actions, and the research literature, read 2026-10-11; the measured baseline below.
   108	
   109	## 1. Finding: the fix program tripped its own rule
   110	
   111	By T126 INV-6 as written: wave 1 (PR #313) 8 amendments (limit 4) and 2 revises (limit 2); wave 3b (PR #314) Bot P1 on two post-RESULT heads. The orchestrator was drafting a waiver for #313. T120 was reset only on the operator's question. The regime is therefore reset here by its own rule; this document is the redesign, and T126 and T124 are superseded (their accepted ideas are kept where named).
   112	
   113	Measured baseline (history + GitHub):
   114	
   115	| task | PR | files | +lines | amendments | questions | revises | audits (incorrect) | Bot threads (heads) | P0/P1 | wall |
   116	|---|---|---|---|---|---|---|---|---|---|---|
   117	| T114 | - | - | - | 0 | 0 | 6 | 3 (3) | - | - | 21.5h |
   118	| T118 | 310 | 35 | 881 | 7 | 0 | 20 | 8 (7) | 16 (7) | 0 | 10.6h |
   119	| T119 | 312 | 37 | 3191 | 8 | 8 | 5 | 4 (4) | 25 (11) | 7 | 11.1h |
   120	| T120 | 315 | 19 | 1489 | 8 | 1 | 0 | 0 | 15 (5) | 8 | reset |
   121	| T124 W1 | 313 | 20 | 2642 | 8 | 6 | 2 | 0 | 52 (10) | 31 | halted, reset |
   122	| T124 W3b | 314 | 9 | 1462 | 5 | 0 | 0 | 0 | 24 (4) | 2 | halted, reset |
   123	
   124	Every acceptance record to date says `cost: n/a`.
   125	
   126	## 2. Root causes, each with its evidence
   127	
   128	R1 to R8 in the front matter. The literature behind R1: intrinsic self-correction without an external signal degrades after the first round (Huang et al. 2023); a second review round on the same artifact raised recall slightly and false positives by 62% (arXiv 2603.16244); multi-round review degrades with rounds (MCR-Bench); revising an already-correct state loses correct work unless verifier evidence is bound to the exact code state (arXiv 2607.24604). Behind R3: Google's review study (median change 24 lines, ~90% under 10 files) and its CL-size guidance. Behind R5 and R6: a judge without a reference is lenient and a reference flips 9-85% of verdicts toward correct (2607.12885); format-restricted generation degrades reasoning, so verdicts reason first and then fill the schema (2408.02442); Anthropic's harness-design post: a standalone skeptical evaluator is tractable where a self-critical generator is not, and the evaluator is worth its cost only where the task exceeds the model's reliable solo capability, which is what the tier table encodes.
   129	
   130	## 3. Principles (each names what it reuses and what it deletes)
   131	
   132	- **P1 One deterministic fact per round (INV-3).** Reuses tests/unit, CI, `pr-feedback.py`. Deletes free-form revise rounds and the audit-per-round habit.
   133	- **P2 Declarative over imperative at trust boundaries (INV-1, INV-5, INV-7).** Reuses `jsonschema`, PyYAML, `codex exec --output-schema`, `claude -p --json-schema`. Deletes the bespoke YAML parser, the glob NFA, the prose verdict grammar, regex parsing of `.last.md`, and the T126 "process_tiers.json next to the module" indirection (the validator reads the manifest with PyYAML).
   134	- **P3 Small one-invariant PRs enforced in CI (INV-2).** Reuses GitHub required checks and the strict up-to-date ruleset already in force. Deletes waves declared inside a task file.
   135	- **P4 Main-pinned mechanical checks in CI; host gate only for history-anchored rules (INV-1, INV-2, INV-8 in CI; INV-3, INV-5 record, INV-6, INV-7 anchor, INV-11 on the host).** Reuses `pull_request_target`, the `changes` job pattern that reports success for an `.orchestration`-only diff. Deletes PR #313's `REVIEW_TREE` idea (never on `main`) and the copy step of untracked evidence into the gate's cwd. The host gate `make require-crit-review` keeps its evidence rules and changes three of them in named waves: the audit verdict and categories come from the schema JSON with the `AGMSG-AUDIT` record and the category lock (V2b), the reset backstop and the Bot-head count (V3a), the history-anchored design review (V4); it continues to run from the orchestrator's main checkout.
   136	- **P5 Research before dispatch; a question ends the task, not amends it (INV-4).** Reuses history (`amendment=`, `status=question`). Deletes the amendment-per-question practice. The task file's `premises` block is the mechanical residue of "verify every CLI constraint by running the real command".
   137	- **P6 Reset is mechanical, loop-time, and released only by another context or the operator (INV-6).** Reuses `scripts/require-crit-review.py` as the mandatory point, `agent-stop-gate.sh` and the Codex `[hooks].Stop` as the early signal (both soft by their documented caps: Claude's 8-continuation cap, Codex's continuation prompt), `check-regime-boundary.sh` for the re-dispatch detector. Deletes the orchestrator-written redesign (the redesign author is a `review`-profile seat or a fresh headless context; the `redesign` profile of T124 v4 is dropped: `review` is the same model and effort as `deep`, so independence of context is the whole lever, and T124 round 1 showed it works).
   138	- **P7 Audit staging by tier; the auditor never serializes the pipeline (INV-5, process_tiers).** See section 4.
   139	- **P8 Cost measured, budgets per tier (INV-9).** Reuses the JSON cost fields the runtimes already emit and the session transcripts. Deletes `cost: n/a`.
   140	- **P9 Parallelism with disjoint files and early push (INV-10).** Reuses `herdr-agents --add-worker`, draft PRs.
   141	- **P10 Routing stays by boundary.** Claude-boundary sources to a Codex seat, Codex-boundary to a Claude seat, permgate and shared gate sources to the operator, as the agmsg-orchestration skill's step 3 states; nothing here changes that.
   142	
   143	## 4. Audit stages (process_tiers; the one table the validator reads)
   144	
   145	| stage | who | when | tier docs | tier review | tier design | cost |
   146	|---|---|---|---|---|---|---|
   147	| 0 design review | a fresh Claude context on the review profile and a Codex read-only review of the same hash, schema receipts (INV-7) | before any code | - | - | required | minutes |
   148	| 1 worker checks | worker in its sandbox: invariant tests first, shellcheck, unit tests | before every push | required | required | required | none for the regime |
   149	| 2 CI + Bot | main-pinned `regime` check (schema, caps, evidence shape) + unit tests + Codex Bot | every push, in parallel | required | required | required | none |
   150	| 3 schema audit | headless read-only `codex exec --output-schema`, pooled 2, started by `make audit-head` once CI is green and the Bot reviewed or 15 min passed, once per RESULT head, reused for an evidence-only head by tree equality (INV-5) | per RESULT head | - | required | required, with invariant map and permgate window | the scarce resource, now off the critical path |
   151	| 4 acceptance | orchestrator: sweep, dispositions, record, host gate, merge `--match-head-commit` | per RESULT | required | required | required | minutes |
   152	
   153	Tier derivation: docs = prose-only `allowed_files` outside the regime's own rule prose (`home/dot_config/claude/rules/**`, the agmsg-orchestration SKILL, `AGENTS.md`, README), which is review tier by explicit list; review = the existing review-tier paths (scripts, hooks, tests, templates); design = the explicit design-tier list from T124 INV-2 v3 (install/**, setup.sh, the gate scripts, `executable_herdr-agents`, `executable_permgate`, Codex and Claude policy, sandbox and permission settings, credential helpers). Round limits: docs 1 revise; review and design 2 revises then reset. Profiles: worker `standard` (docs `express`), review `review`, audit `audit`.
   154	
   155	Why stage 3 is not the queue: the orchestrator starts it with `make audit-head` when the RESULT arrives (the wait on CI and the Bot is inside the target), it runs concurrently (pool of two, each in its own detached worktree), once per head, and an evidence-only head reuses the earlier audit by tree equality; the measured cost of the old serial form was 1.3 h of 11.1 h, so the throughput levers are P1 and P6, and the pool removes the residual queue.
   156	
   157	## 5. Enforcement map
   158	
   159	| invariant | enforcement point |
   160	|---|---|
   161	| INV-1 | `.github/workflows/regime.yml` (`pull_request_target`, required check `regime`: validates `.orchestration/<task id>/task.md` from the PR head read as data, refuses workflow edits outside a design-tier task; an explicit Actions event policy allowing `pull_request_target` is set by the operator before 2026-11-02, named in V1c's acceptance record), `scripts/validate-task.py` (schema + PyYAML, about 80 lines), `schemas/task.json`, `scripts/lib/high_risk_paths.py` (new module: tier lists and `tier_of`), `scripts/legacy-task-ids.txt` (grandfather list), `process_tiers` in the manifest; host gate compares the copy's sha256 with `task_sha256=` in history (V3a); stage waivers by `scripts/regime-waive.sh` under its `permissions.ask` rule, written outside the sandbox write roots (V3a) |
   162	| INV-2 | `regime.yml` step with `scripts/pr-caps.sh` and the task.md invariant-id comparison against the design's `implementing_tasks` |
   163	| INV-3 | `regime-check.sh` step: the test selector named in `.orchestration/<task id>/revise.yaml` (sibling of the byte-identical task.md) exists on the head and its file differs between `previous_head` and the head; a `revise-check` job in `test.yaml` (PR context, required) runs exactly that selector on both heads; the host gate's `previous_head` history check and validation-file line are V2b's |
   164	| INV-4 | `scripts/validate-task.py` (premises required for code and design tasks); `agent-stop-gate.sh` early signal on the second AGMSG-TASK or second PONG question; the merge backstop is INV-6's |
   165	| INV-5 | `schemas/audit.json` (findings and invariant map before verdict), `scripts/audit-head.sh` (about 100 lines: detached worktree, `codex exec`, fallback, sha256 to history under the audit identity, `.last.md` render; PR #314's hardening kept), `make audit-head` target around `gh pr checks --watch` and the SKILL's Bot list loop with its 15-minute `bot: none` rule (no daemon), `AGENTS.md` Audit section; gate: JSON verdict and categories, `AGMSG-AUDIT` lookup, category lock, tree-equality acceptance of an earlier head (V2b) |
   166	| INV-6 | `scripts/require-crit-review.py` (mandatory: history counts, Bot heads from `original_commit_id` recorded by `scripts/pr-feedback.py`, audit heads from the main checkout's audit JSONs whose sha256 matches their `AGMSG-AUDIT` record, reset record or a `scripts/regime-waive.sh` waiver), `scripts/agent-stop-gate.sh` and the manifest's `codex.hooks` Stop entry (early signal, history counts only, within the 3 s history budget), `scripts/check-regime-boundary.sh` (closed-unmerged PR without a reset record; over-count task without an accepted or reset record; waiver listing) |
   167	| INV-7 | `scripts/design-review.sh` + `schemas/design-review.json`: two headless runs per design hash, `claude -p` under `claude-review-dot-hNNN` and `codex exec --sandbox read-only` under `codex-review-dot-hNNN`, each joining for the run and sending its RESULT; gate: both RESULTs precede the implementing TASK, both hashes recomputed, whole-file form accepted for pre-V4 receipts |
   168	| INV-8 | worker writes under `.orchestration/<task id>/` on the branch (task.md copy first); `regime.yml` validates the evidence JSON shapes; the gate's existing path rules keep the orchestrator's records under `validation/` and `acceptance/` |
   169	| INV-9 | `scripts/accept-task.py` (sweep, dispositions scaffold, record rows, gate invocation, merge command, cost fields), budgets in `process_tiers`, `check-regime-boundary.sh` warning |
   170	| INV-10 | `scripts/check-regime-boundary.sh` and `scripts/accept-task.py` from `history.sh` timestamps (storage facade or `--limit`, never the 20-row default), the draft PR's `created_at` from `gh api pulls/<n>`, and the task's `after` list against acceptance records |
   171	| INV-11 | `executable_permgate` (operator-routed, Codex security review) + gate cross-check |
   172	| INV-12 | one test module per script; `make unit-test` in CI; the `main-tests` required job (V0): main's modules for scripts outside the PR's `allowed_files`, main's dormant contracts (`REGIME_CONTRACT=1`) for scripts inside it; contract PRs (`<task>-contract-a01`, dormant tests, merged before a design-tier implementation); the auditor checks per PR that no new hand-written parser sits at a trust boundary (a `conformance` finding) |
   173	| prose | SKILL, `agmsg-orchestration.md`, `pr-integration.md`, `crit-review.md`, `model-selection.md`, README: each wave edits only the sections it implements |
   174	
   175	## 6. Waves (one PR, one invariant, within INV-2's caps; each task file reviewed by a fresh context before dispatch)
   176	
   177	- **V0** INV-12: the `main-tests` required job in `test.yaml` (main's `tests/unit` in the PR's context: modules of scripts outside the PR's `allowed_files` as they are, dormant contract tests of scripts inside it with `REGIME_CONTRACT=1`), the contract decorator in `tests/unit/regime_contract.py`, and the two-mode protocol in the Worker Playbook; lands before every other wave. Claude seat; design tier (workflow); the operator lists the check at its acceptance.
   178	- **V1** INV-1, validation only (operator direction 2026-10-11, relayed through the review seat; also the cap: the undivided V1 sat at 500 added lines): `schemas/task.json`, `scripts/validate-task.py`, `scripts/lib/high_risk_paths.py`, `scripts/legacy-task-ids.txt` (from PR #313; data, excluded from the line cap), `tests/unit/test_validate_task.py`. Claude seat. Design tier: this review is its stage 0. Precondition: this design is on `main` through a boundary PR before V1's TASK is dispatched.
   179	- **V1c** INV-1, the CI check (after V1): `scripts/regime-check.sh`, `.github/workflows/regime.yml` (task.md validation, workflow-edit refusal, `workflow_dispatch` dry run), `tests/unit/test_regime_check.py`, `process_tiers` in the manifest, SKILL step 3 paragraph, README sentence. Claude seat. Acceptance names the operator action that lists `regime` as a required check, after the dry run from `main` against a closed PR. Two tasks map to INV-1 as V2 and V2b map to INV-5.
   180	- **V1b** INV-2 (after V1c): `scripts/pr-caps.sh`, the caps and invariant-id steps in `regime-check.sh`, tests, one SKILL sentence.
   181	- **V2** INV-5 runner: `schemas/audit.json` (PR #314's, reordered), `scripts/audit-head.sh` with PR #314's hardening, `make audit-head`, `AGENTS.md` Audit section, tests, the SKILL's task-level audit bullet. Claude seat.
   182	- **V2b** INV-5 gate: `scripts/require-crit-review.py` reads the JSON verdict and categories, requires the `AGMSG-AUDIT` record, locks orchestration and conformance at P0-P2 to waiver or reset, accepts an earlier audited head by tree equality, and requires the INV-3 `check=` line in the validation file; tests. Operator-routed gate source (delegable to a Claude seat with recorded opt-in).
   183	- **A3** INV-6 (plan 006 Phase A, `dotfiles-T128-regime-counters-a01`): `scripts/regime-counters.sh` computes every INV-6 count from history and GitHub and prints the thresholds reached; `check-regime-boundary.sh` reports a reached threshold without a reset record or waiver; the orchestrator runs it before every acceptance action. V3a wires that script into the hook and the gate.
   184	- **V3a** INV-6: `scripts/pr-feedback.py` (`original_commit_id` on review_comment items), `require-crit-review.py` reset backstop and `task_sha256` comparison, `agent-stop-gate.sh` history counts (revises, amendments, questions) as the early signal, the Codex Stop entry in the manifest and its rendered template, `scripts/regime-waive.sh` with its `permissions.ask` rule in the manifest's Claude permissions block (no permgate policy entry), `check-regime-boundary.sh` detector and waiver listing; tests. Four boundaries in one PR (gate source, Claude hook and permission source, Codex hook source): an operator PR by construction, reviewed by a Codex `security`-profile seat before acceptance.
   185	- **V3b** INV-4: premises in the schema and validator, SKILL text (questions end the task; one answering TASK at most). Claude seat; no hook source (the counting is V3a's).
   186	- **V3c** INV-3: `check=` and `previous_head=` in the ACCEPTANCE contract (SKILL), `revise.yaml` beside task.md in the Worker Playbook, the `regime-check.sh` step, the `revise-check` job in `test.yaml`; tests. Claude seat (no gate source: the history check and validation-file line are V2b's).
   187	- **V3d** INV-10: idle and first-push computations in `check-regime-boundary.sh` and `accept-task.py` (the latter lands in V5b; V3d adds them to the boundary check only). Claude seat.
   188	- **V4** INV-7: `scripts/design-review.sh` (Claude and Codex runs under their `-review-dot-hNNN` identities), `schemas/design-review.json`, the history anchor and hash check in the gate (two RESULTs, both forms), SKILL paragraph. Operator-routed for the gate part.
   189	- **V5a** INV-8: `.orchestration/<task id>/` paths in the Worker Playbook, task.md copy as the first commit, evidence-shape validation in `regime.yml`, boundary commit reduced to orchestrator records. Claude seat.
   190	- **V5b** INV-9: `scripts/accept-task.py`, cost fields with source digests, budgets in `process_tiers`, `check-regime-boundary.sh` budget warning. Claude seat. Size: the sweep, scaffold and gate invocation already exist as commands; the script sequences them, about 200 lines.
   191	- **V6** INV-11: `executable_permgate` session_id and cwd; gate cross-check. Operator-routed, Codex `security` profile review.
   192	
   193	Order: V0, then each design-tier code wave as `<task>-contract-a01` (dormant contract tests) followed by its implementation: V1, V1c, V1b, V2, V2b, V3a, V3b, V3c, V3d, V4, V5a, V5b, V6. File-disjoint pairs may run concurrently (V1 with V2; V3b with V3d); the gate-source waves (V2b, V3a, V4's gate part) run serially.
   194	
   195	## 7. Thresholds (operator confirmed 2026-10-11)
   196	
   197	revise 2; amendments 2; questions 2; Bot P0/P1 heads 2 (post-RESULT); audit implementation or specification P0-P1 heads 2; PR 15 changed files (the file count excludes `.orchestration/` only) and 500 added lines outside `tests/`, `.orchestration/` and the data list `scripts/legacy-task-ids.txt`; first push 30 minutes; idle 20 minutes; workers 3; audit pool 2; audit once per head; docs tier 1 revise.
   198	
   199	## 8. Disposition of the halted work
   200	
   201	PR #313 and #314 closed unmerged as reference branches (reset records in `.orchestration/acceptance/…-design-reset.md`); PR #315 is a draft per T120's reset record; the four worker seats are removed. Salvaged: the format-2 key set, the tier table, `scripts/legacy-task-ids.txt` and the test ideas of `tests/unit/test_validate_task.py` (V1); `scripts/schemas/audit.json`, the AGENTS.md Audit text, the pre-push hardening and the `AGMSG-AUDIT` record (V2). Dropped with the `redesign` profile: PR #313's `home/dot_codex/modify_private_redesign.config.toml`. T127 (T120's redesign) follows V1 under this regime.
   202	
   203	## 9. Residuals, stated
   204	
   205	- Workers' conduct is checked mechanically only for Claude seats and only after V6; until then the sandbox record is self-reported.
   206	- `pull_request_target` runs with the base repository's token on a public repository: the `regime` job reads PR files as data with `contents: read` only, checks out `main`'s scripts, and never executes anything from the PR; a change to `.github/workflows/regime.yml` itself is a design-tier change under INV-1.
   207	- A repository admin can edit the ruleset; that path is visible on GitHub, not prevented, consistent with the waiver anchor.
   208	- Operator authentication does not exist on this machine: every seat runs as the one user and every GitHub action as the one account, so no record can prove that the operator rather than the orchestrator wrote it. The regime therefore makes every waiver pass through a native permission prompt (`permissions.ask`, which no classifier, hook or agent may answer) and makes every waiver visible in three places; it does not claim more. The Codex design review of round 7 asked for authenticated operator events; this is the honest limit of what the machine offers.
   209	- The design-review receipt's anchor in history is only as strong as the `-review-` identity's independence; a fresh headless context per review (V4) is the mitigation, and until V4 lands a seated `review`-profile identity reviews.
   210	- GitHub's default Actions policy blocks `pull_request_target` on public repositories from 2026-11-02 (evaluate mode today); the operator sets an explicit event policy allowing it before then, or the `regime` job loses its main-pinned form and the host gate becomes the only gate again. Named in V1c's acceptance record.
   211	- The `regime` job runs `main`'s workflow file, so a change to `regime.yml` is never exercised by its own PR; its logic therefore lives in scripts with unit tests, and a `workflow_dispatch` dry run precedes listing it as required.
   212	- `regime.yml` discipline, stated once: `main` stays at the workspace root (`actions/checkout` default ref under `pull_request_target`); the PR head is fetched as data and read with `git show <head sha>:<path>` into a directory never on `PATH`; the diff range is the merge-base of `github.event.pull_request.head.sha` with `main`, never `github.sha`; `uv run --no-project`; `yaml.safe_load`; no `make`, no script, no dependency file from the PR tree; `permissions: contents: read`; no secrets.
   213	- The seven existing required checks still run on `pull_request` from the PR's own workflow files; INV-1's workflow-edit refusal in the `regime` job is what closes R8 for them.
   214	- Bootstrap: this design was written by the orchestrator that dispatched the abandoned tasks. The reset records carry the operator's waiver form (`DESIGN_RESET_WAIVED_BY=operator`, decision 2026-10-11), this review is the only release, and no further orchestrator-authored design follows under T128; T127 (T120's redesign) is written by another context.
   215	
   216	## 10. Design review (round 15 requested: plan 006 A102, second pair)
   217	
   218	Round 1 (`.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review.md`, `claude-review-dot-a001`, 2026-10-10T21:15Z, verdict `revise`): INV-7, INV-8, INV-11, INV-12 accepted with notes; INV-1, 2, 3, 4, 5, 6, 9, 10 rejected with corrections; findings F1-F9. v2 adopts every item: the task.md copy and `task_sha256` anchor (F1), the per-task invariant-set rule and the workflow-edit refusal (F2), the gate changes assigned to V2b/V3a/V4 with the category lock, the Bot-wait timeout and the tree-equality rule (F3), the merge backstop as the mandatory point, `original_commit_id`, the audit-JSON source, the Stop-hook budget split and the boundary detector (F4), the single amendment count over every TASK (F5), INV-9/INV-10 moved out of the Stop hook (F6), the reset records corrected to `claude-review-dot-a001` with the waiver form and the thread ids (F7), rule prose in the review tier (F8), premise 1 restated and three premises added (F9); plus the Q5 salvage list, the `make audit-head` target in place of a daemon, the `regime.yml` discipline and the hash note.
   219	
   220	Round 2 (`…-design-review-round2.md`, 21:29Z, verdict `revise`): every round-1 correction confirmed applied; INV-2, INV-3, INV-6 rejected for contradictions v2 introduced, plus routing, cap and premise notes. v3 adopts all of them: `implementing_tasks` is a map of task id to invariant ids inside the hashed keys and the design-on-main precondition is stated (INV-2); `revise.yaml` is a sibling of the byte-identical task.md (INV-3, INV-8, INV-12, V3c, V2b); the question threshold is 2 and audit JSONs count only when their sha256 matches their record (INV-6); V3a is an operator PR with all hook counting, V3b has no hook source, V3c no gate source; the legacy list is excluded from the line cap as data; the `workflow_dispatch` premise is added; the stage-3 sentence names the orchestrator's `make audit-head`; INV-1 names the latest TASK's token and the recommit after each amendment. Round 3 (`…-design-review-round3.md`, 21:33Z, verdict `accept`) confirmed the five edits; its two notes are carried in the acceptance record. v4 (operator direction 2026-10-11, relayed by the review seat's PONG at 22:01Z) splits V1 by responsibility into V1 (validation only) and V1c (the CI check), adds `dotfiles-T128-v1c-regime-ci-check-a01: [INV-1]` to `implementing_tasks` (a hashed key, hence this round), reorders the waves (V1, V1c, V1b, …) and aligns section 7's cap wording with INV-2. Round 4 (`…-design-review-round4.md`, 22:06Z, verdict `accept`) confirmed the split; its note (INV-1's ruleset action is V1c's acceptance record) is carried. v5 answers the Codex Bot's finding on boundary PR #316 (thread 4239305441): INV-3's `ci:<job>` form had no enforcement, so `check=` is now a test selector or a `repro:<id>` whose command and output live in revise.yaml, each with its own regime-job verification. Round 5 (`…-design-review-round5.md`, 22:12Z, verdict `accept`) confirmed it. The Codex Bot then reviewed the second boundary head (c1e2582b) and raised six P1 and four P2 findings that three same-vendor accepts had not: the auditor read the schema and AGENTS.md from the audited head (INV-5 now runs from main as the instruction root with the worktree as data), the CI job had no previous RESULT head (INV-3 now records previous_head in the ACCEPTANCE and revise.yaml, cross-checked by the host gate), ids were compared without sentences (INV-2), `allowed_files: ['*']` derived a cheap tier and a branch copy could claim a legacy id (INV-1, INV-12), and two task records pointed at an abandoned prerequisite. v6 adopts all ten and, because a cross-vendor reviewer found what a same-vendor fresh context did not, INV-7 now requires both a Claude and a Codex review of each design hash. Round 6 (`…-design-review-round6.md`, 22:28Z, verdict `revise`) accepted INV-1, 2, 3, 5, 12 and rejected INV-7: the Bot form produced no receipt, hash or RESULT, so it would have been an orchestrator-written receipt for a review it did not perform (R5). v7 makes the Codex review a `codex exec --sandbox read-only` run under a `codex-review` identity with its own receipt and RESULT, names it in the enforcement row and V4, keeps the Bot's review as swept feedback, and adds the bare-mode skills premise (round-6 INV-5 note, acted on in V2). Round 7 (Claude, 22:31Z, `accept`) confirmed INV-7. The first Codex review (`…-design-review-round7-codex.md`, `codex-review-dot-h001`, 22:34Z, `reject`) rejected INV-1, 3, 4, 5, 6, 9, 10, 12, all on one theme: evidence the orchestrator authors. v8 answers each: the waiver becomes a command under a `permissions.ask` rule (INV-1, INV-6) with the one-account residual stated in section 9; `repro:` is dropped and `check=` is a test selector only (INV-3); premises are reviewer and auditor evidence and the counting is the mechanical part (INV-4); the audit carries an input manifest and the acceptance record has an audit-input boundary (INV-5); cost records name their raw sources and stay a warning metric (INV-9); first push is the first commit's committer date and dispatchability is defined (INV-10); the independent oracle for gate-script PRs is the trusted-root audit (INV-12). The Codex P2 on the bare-mode skills premise is not adopted: the headless page says verbatim that "A directory you name with --add-dir is a partial exception: bare mode loads skills from its .claude/skills/ folder". Codex round 8 (`…-design-review-round8-codex.md`, 22:39Z, `reject`) accepted INV-1, 6, 7, 8, 9, 11 and the one-account residual, withdrew its bare-mode P2, and rejected INV-2 (tests unbounded), INV-3 (a changed file is not a run selector), INV-4 (sampling), INV-5 (the skills refusal was a premise, not a rule), INV-10 (committer date is not a push time; dependencies), INV-12 (a model audit is not a deterministic oracle), plus two stale enforcement rows. v9 adopts all: a 1000-line cap under tests/; the exact selector run on both heads in the PR's required `revise-check` job; every premise dispositioned by each reviewer and the auditor; the `.claude/**` refusal inside INV-5; the draft PR's `created_at` and an `after` list for dispatchability; a `main-tests` required job running main's tests against the PR's scripts (V5c); the two rows fixed. Claude round 8 (`…-design-review-round8.md`, 22:41Z, `revise`) rejected INV-1 (the waive script had no owner or row), INV-5 (once-per-head versus re-audit on a stale manifest) and INV-10 (fixed in v9), and offered a stronger anchor: the waiver record in a directory outside the sandbox write roots. Codex round 9 (`…-design-review-round9-codex.md`, 22:46Z, `reject`) accepted ten, rejected INV-5 (the `.claude/**` refusal that v9 claimed was silently lost by a failed edit, confirmed by grep) and INV-12 (the oracle must precede the waves), dispositioned all twelve premises (nine hold, three unverifiable in its read-only sandbox), and raised GitHub's 2026-11-02 `pull_request_target` policy. v10: the refusal is in INV-5 and verified by grep; one valid audit per head with stale-manifest replacement; the runner computes the manifest; the waiver record lives outside the sandbox write roots and V3a owns the script (map entry `[INV-6, INV-1]`); `main-tests` is wave V0 and every code wave is contract-first (INV-12, INV-2); the policy premise and residual. Claude round 9 (`…-design-review-round9.md`, 22:46Z, `revise`) found that `main-tests` as drafted would fail every intentional change and proposed running main's modules only for scripts outside `allowed_files`; Codex round 10 (`…-design-review-round10-codex.md`, 22:50Z, `reject`) accepted INV-1..11 and found that contract-first tests cannot merge ahead of an implementation that changes an existing script, proposing dormant contracts that `main-tests` activates on the implementation PR. v11's INV-12 is the union: main's modules as they are for undeclared scripts, main's dormant contracts (`REGIME_CONTRACT=1`) for declared ones, contract PRs required for design-tier waves; INV-1 states that the record's location is the guard and the ask rule the second layer (Claude round 9). Codex round 11 (`…-design-review-round11-codex.md`, 22:52Z) accepted INV-1..12 with no findings. Claude round 11 (`…-design-review-round11.md`, 22:54Z, `revise`) accepted everything but two INV-12 clauses: contracts must not stay dormant forever (the implementation PR removes the decorator; main-tests judges it against main's dormant copy) and an empty contract must fail a design-tier implementation PR. v12 adds both sentences to INV-12 and V0. Claude round 12 (`…-design-review-round12.md`, 22:57Z) accepted v12; Codex round 12 (`…-design-review-round12-codex.md`, 22:57Z, `revise`) accepted INV-1..11 and asked for a failing check behind the decorator-removal clause. v13 adds it to INV-12 (main-tests fails an implementation PR whose declared test module still carries a contract marker) and V0 carries it with the task-file reviewer's three V0 items (main's tests overlaid on a copy of the PR tree, module selection from the task's declared tests/ entries, task.md read with PyYAML). Round 13 (Claude 23:01Z, Codex 23:01Z and the premise map 23:17Z) accepted v13. Plan 006 (approved 2026-10-11) A102 amends two hashed keys: INV-12 states the in-process oracle's authenticated completion (nonce runner) and its residual, after the Codex Bot's P1 on V0's round-1 head repeated the class of the round-0 audit's finding 3; INV-2 and the map gain the .orchestration-only CI skip (`dotfiles-T128-ci-skip-orchestration-a01`, plan A201) that plan 006 orders as Phase 2. Round 14 (Codex 02:42Z `accept`; Claude 02:43Z `revise`): INV-12's residual clause understated the gap (the nonce authenticates the writer, not the counts; in-process patching of unittest's result collection forges counts with a genuine nonce) and INV-2 should cover every required check. v15 states the residual as it is, adds the runner's pinning of unittest classes, and words INV-2 for every required workflow. Round 15 asks both reviewers at once for one verdict each on this hash. Sources are the repository paths under `.orchestration/validation/dotfiles-T128-regime-v3-a01-research/` (`baseline.md`, `practice-evidence.md`, `claude-code-factsheet.md`, `codex-factsheet.md`, `github-factsheet.md`, `method-draft.md`). Receipt: `.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round15.md` (Claude) and `…-design-review-round15-codex.md` (Codex); the whole-file sha256 of this file in both headers.

exec
/bin/zsh -lc "git diff 3c845c55dc43b668fa6df8434cb47a1b1f00d695 3bafe4f24c80fd1093e2fd5a19d843e5cb7aff5b -- .github/workflows; git show 3bafe4f24c80fd1093e2fd5a19d843e5cb7aff5b:tests/unit/test_workflow_orchestration_skip.py | sed -n '1,140p'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc 'nl -ba .orchestration/reports/dotfiles-T128-ci-skip-orchestration-a02.md; nl -ba .orchestration/sandboxes/dotfiles-T128-ci-skip-orchestration-a02.md; nl -ba .orchestration/acceptance/dotfiles-T128-ci-skip-orchestration-a02.md' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 65ms:
diff --git a/.github/workflows/remote.yaml b/.github/workflows/remote.yaml
index 15a6c78a..54b30264 100644
--- a/.github/workflows/remote.yaml
+++ b/.github/workflows/remote.yaml
@@ -37,9 +37,45 @@ jobs:
 
       - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7
         with:
+          fetch-depth: 0
           persist-credentials: false
 
+      - name: Decide whether the diff needs a bootstrap
+        id: decide
+        env:
+          EVENT_NAME: ${{ github.event_name }}
+          BASE_REF: ${{ github.base_ref }}
+          HEAD_SHA: ${{ github.sha }}
+        shell: bash
+        run: |
+          set -euo pipefail
+          # Decided in this job, never in a job it needs: a job skipped because
+          # a needed job failed reports Success even as a required check, so a
+          # failed decision has to fail this job instead. Only a pull request has
+          # a base-to-head range to judge; push, schedule and workflow_dispatch
+          # keep bootstrapping main.
+          if [ "${EVENT_NAME}" != pull_request ]; then
+            echo "should_run=true" >> "${GITHUB_OUTPUT}"
+            exit 0
+          fi
+          # A full fetch: a shallow one cuts the history of a base tip that
+          # moved after the checkout, and the diff then has no merge base.
+          git fetch --no-tags origin "${BASE_REF}"
+          # --no-renames lists both sides of a rename; core.quotePath off keeps
+          # non-ASCII paths raw. An empty diff runs the bootstrap.
+          changed="$(git -c core.quotePath=false diff --no-renames --name-only "origin/${BASE_REF}...${HEAD_SHA}")"
+          if grep -qv '^\.orchestration/' <<< "${changed}"; then
+            echo "should_run=true" >> "${GITHUB_OUTPUT}"
+          else
+            echo "should_run=false" >> "${GITHUB_OUTPUT}"
+          fi
+
+      - name: Skip the bootstrap for an .orchestration-only diff
+        if: ${{ steps.decide.outputs.should_run != 'true' }}
+        run: echo "Only .orchestration/ files changed; the job reports success without bootstrapping."
+
       - name: Bootstrap the checked-out public source
+        if: ${{ steps.decide.outputs.should_run == 'true' }}
         env:
           GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
         shell: bash
@@ -99,20 +135,55 @@ jobs:
 
       - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7
         with:
+          fetch-depth: 0
           persist-credentials: false
 
+      - name: Decide whether the diff needs a bootstrap
+        id: decide
+        env:
+          EVENT_NAME: ${{ github.event_name }}
+          BASE_REF: ${{ github.base_ref }}
+          HEAD_SHA: ${{ github.sha }}
+        shell: bash
+        run: |
+          set -euo pipefail
+          # Decided in this job, never in a job it needs: a job skipped because
+          # a needed job failed reports Success even as a required check, so a
+          # failed decision has to fail this job instead. Only a pull request has
+          # a base-to-head range to judge; push, schedule and workflow_dispatch
+          # keep bootstrapping main.
+          if [ "${EVENT_NAME}" != pull_request ]; then
+            echo "should_run=true" >> "${GITHUB_OUTPUT}"
+            exit 0
+          fi
+          # A full fetch: a shallow one cuts the history of a base tip that
+          # moved after the checkout, and the diff then has no merge base.
+          git fetch --no-tags origin "${BASE_REF}"
+          # --no-renames lists both sides of a rename; core.quotePath off keeps
+          # non-ASCII paths raw. An empty diff runs the bootstrap.
+          changed="$(git -c core.quotePath=false diff --no-renames --name-only "origin/${BASE_REF}...${HEAD_SHA}")"
+          if grep -qv '^\.orchestration/' <<< "${changed}"; then
+            echo "should_run=true" >> "${GITHUB_OUTPUT}"
+          else
+            echo "should_run=false" >> "${GITHUB_OUTPUT}"
+          fi
+
+      - name: Skip the bootstrap for an .orchestration-only diff
+        if: ${{ steps.decide.outputs.should_run != 'true' }}
+        run: echo "Only .orchestration/ files changed; the job reports success without bootstrapping."
+
       - name: Explain skipped private bootstrap
         if: ${{ contains(github.actor, '[bot]') || env.HAS_EMAIL_ADDRESS != 'true' || env.HAS_PRIVATE_DEPLOY_KEY != 'true' }}
         run: echo "Private bootstrap is optional and secrets are unavailable in this context."
 
       - name: Set up the private deploy key
-        if: ${{ !contains(github.actor, '[bot]') && env.HAS_EMAIL_ADDRESS == 'true' && env.HAS_PRIVATE_DEPLOY_KEY == 'true' }}
+        if: ${{ steps.decide.outputs.should_run == 'true' && !contains(github.actor, '[bot]') && env.HAS_EMAIL_ADDRESS == 'true' && env.HAS_PRIVATE_DEPLOY_KEY == 'true' }}
         uses: webfactory/ssh-agent@e83874834305fe9a4a2997156cb26c5de65a8555 # v0.10.0
         with:
           ssh-private-key: ${{ secrets.PRIVATE_DOTFILES_PRIVATE_DEPLOY_KEY }}
 
       - name: Bootstrap with private restoration
-        if: ${{ !contains(github.actor, '[bot]') && env.HAS_EMAIL_ADDRESS == 'true' && env.HAS_PRIVATE_DEPLOY_KEY == 'true' }}
+        if: ${{ steps.decide.outputs.should_run == 'true' && !contains(github.actor, '[bot]') && env.HAS_EMAIL_ADDRESS == 'true' && env.HAS_PRIVATE_DEPLOY_KEY == 'true' }}
         env:
           GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
           EMAIL_ADDRESS: ${{ secrets.EMAIL_ADDRESS }}
diff --git a/.github/workflows/test.yaml b/.github/workflows/test.yaml
index e022be94..1d8bba9f 100644
--- a/.github/workflows/test.yaml
+++ b/.github/workflows/test.yaml
@@ -14,11 +14,36 @@ permissions:
   contents: read
 
 jobs:
-  changes:
-    runs-on: ubuntu-24.04
-    outputs:
-      should_test: ${{ steps.filter.outputs.should_test }}
-      diff_range: ${{ steps.filter.outputs.diff_range }}
+  test:
+    # Run the same test suite on each target OS/system pair.
+    # We intentionally keep macOS as `client` only because this repository
+    # does not define a macOS `server` test target.
+    strategy:
+      matrix:
+        os: [ubuntu-24.04, macos-14]
+        system: [client, server]
+        exclude:
+          - os: macos-14
+            system: server
+        # Non-required canary for the next Ubuntu image: it shows how the suite
+        # fares there without blocking merges. Adopt it by changing the
+        # explicit label above once it is green.
+        include:
+          - os: ubuntu-26.04
+            system: client
+
+    runs-on: ${{ matrix.os }}
+    continue-on-error: ${{ matrix.os == 'ubuntu-26.04' }}
+    env:
+      # Export matrix values to shell scripts so existing test helpers can use
+      # simple `OS`/`SYSTEM` checks without depending on GitHub expression syntax.
+      OS: ${{ matrix.os }}
+      SYSTEM: ${{ matrix.system }}
+      # Keep Codecov naming deterministic per job. This makes it easy to trace
+      # upload sessions in Codecov API/UI and avoids accidental session overlap.
+      CODECOV_FLAGS: ${{ matrix.os }}-${{ matrix.system }}
+      CODECOV_NAME: codecov-dotfiles-${{ matrix.os }}-${{ matrix.system }}
+      GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
 
     steps:
       - name: Configure Git defaults
@@ -30,8 +55,8 @@ jobs:
           fetch-depth: 0
           persist-credentials: false
 
-      - name: Detect unit-test-relevant changes
-        id: filter
+      - name: Decide whether the diff needs the unit tests
+        id: decide
         env:
           EVENT_NAME: ${{ github.event_name }}
           BASE_REF: ${{ github.base_ref }}
@@ -40,11 +65,13 @@ jobs:
         run: |
           set -euo pipefail
 
-          # Keep the diff calculation here so the required workflow can always
-          # start and report a final status before we decide whether to run the
-          # heavier test steps.
+          # Decided in this job, never in a job it needs: a job skipped because
+          # a needed job failed reports Success even as a required check, so a
+          # failed decision has to fail this job instead.
           if [ "${EVENT_NAME}" = "pull_request" ]; then
-            git fetch --no-tags --depth=1 origin "${BASE_REF}"
+            # A full fetch: a shallow one cuts the history of a base tip that
+            # moved after the checkout, and the diff then has no merge base.
+            git fetch --no-tags origin "${BASE_REF}"
             diff_range="origin/${BASE_REF}...${HEAD_SHA}"
           elif [ -n "${BEFORE_SHA}" ] && [ "${BEFORE_SHA}" != "0000000000000000000000000000000000000000" ]; then
             diff_range="${BEFORE_SHA}...${HEAD_SHA}"
@@ -68,7 +95,9 @@ jobs:
           # No pipe into grep -q: under pipefail its early exit could SIGPIPE
           # the writer and turn a match into a false negative. core.quotePath
           # off keeps non-ASCII paths raw instead of "\343..."-quoted.
-          changed="$(git -c core.quotePath=false diff --name-only "${diff_range}")"
+          # --no-renames lists both sides of a rename, so a file moved out of
+          # home/ into .orchestration/ still runs the tests.
+          changed="$(git -c core.quotePath=false diff --no-renames --name-only "${diff_range}")"
           relevant="$(grep -v '^\.orchestration/' <<< "${changed}" || true)"
           if grep -Eq '^(\.github/workflows/|home/|install/|scripts/|tests/|plans/|docs/|setup\.sh$|Makefile$|ruff\.toml$|\.prettierignore$)|(^|/)[^/]+\.(py|md)$' <<< "${relevant}"; then
             echo "should_test=true" >> "${GITHUB_OUTPUT}"
@@ -76,55 +105,14 @@ jobs:
             echo "should_test=false" >> "${GITHUB_OUTPUT}"
           fi
 
-  test:
-    needs: changes
-    # Run the same test suite on each target OS/system pair.
-    # We intentionally keep macOS as `client` only because this repository
-    # does not define a macOS `server` test target.
-    strategy:
-      matrix:
-        os: [ubuntu-24.04, macos-14]
-        system: [client, server]
-        exclude:
-          - os: macos-14
-            system: server
-        # Non-required canary for the next Ubuntu image: it shows how the suite
-        # fares there without blocking merges. Adopt it by changing the
-        # explicit label above once it is green.
-        include:
-          - os: ubuntu-26.04
-            system: client
-
-    runs-on: ${{ matrix.os }}
-    continue-on-error: ${{ matrix.os == 'ubuntu-26.04' }}
-    env:
-      # Export matrix values to shell scripts so existing test helpers can use
-      # simple `OS`/`SYSTEM` checks without depending on GitHub expression syntax.
-      OS: ${{ matrix.os }}
-      SYSTEM: ${{ matrix.system }}
-      # Keep Codecov naming deterministic per job. This makes it easy to trace
-      # upload sessions in Codecov API/UI and avoids accidental session overlap.
-      CODECOV_FLAGS: ${{ matrix.os }}-${{ matrix.system }}
-      CODECOV_NAME: codecov-dotfiles-${{ matrix.os }}-${{ matrix.system }}
-      GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
-
-    steps:
-      - name: Configure Git defaults
-        run: git config --global init.defaultBranch main
-
-      - name: Checkout repository
-        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7
-        with:
-          persist-credentials: false
-
       - name: Skip full unit test run for unrelated changes
-        if: ${{ needs.changes.outputs.should_test != 'true' }}
+        if: ${{ steps.decide.outputs.should_test != 'true' }}
         run: |
           echo "No unit-test-relevant files changed."
-          echo "Compared diff range: ${{ needs.changes.outputs.diff_range }}"
+          echo "Compared diff range: ${{ steps.decide.outputs.diff_range }}"
 
       - name: Install tools
-        if: ${{ needs.changes.outputs.should_test == 'true' }}
+        if: ${{ steps.decide.outputs.should_test == 'true' }}
         run: |
           if [ "${OS}" == "macos-14" ]; then
             # The macos-14 runner image ships third-party taps tapped but
@@ -205,14 +193,14 @@ jobs:
           gem install --user-install --no-document simplecov-cobertura --version 3.1.0
 
       - name: Prepare statusline tool config
-        if: ${{ needs.changes.outputs.should_test == 'true' }}
+        if: ${{ steps.decide.outputs.should_test == 'true' }}
         run: |
           statusline_mise_dir="${RUNNER_TEMP}/statusline-mise"
           mkdir -p "${statusline_mise_dir}"
           cp home/dot_mise/config.toml "${statusline_mise_dir}/mise.toml"
 
       - name: Setup mise for statusline smoke
-        if: ${{ needs.changes.outputs.should_test == 'true' }}
+        if: ${{ steps.decide.outputs.should_test == 'true' }}
         uses: jdx/mise-action@c2a87611a18de5b3828c5652fe268e992400cb5c # v4
         with:
           # The newest mise at least 72 hours old, as hosts get it (minimum_release_age).
@@ -221,7 +209,7 @@ jobs:
           cache: true
 
       - name: Install statusline tools
-        if: ${{ needs.changes.outputs.should_test == 'true' }}
+        if: ${{ steps.decide.outputs.should_test == 'true' }}
         run: |
           mise trust --yes "${RUNNER_TEMP}/statusline-mise/mise.toml"
           mise -C "${RUNNER_TEMP}/statusline-mise" install node
@@ -230,7 +218,7 @@ jobs:
           mise -C "${RUNNER_TEMP}/statusline-mise" install ruff npm:prettier
 
       - name: Smoke-test statusline tools without network
-        if: ${{ needs.changes.outputs.should_test == 'true' }}
+        if: ${{ steps.decide.outputs.should_test == 'true' }}
         run: |
           set -euo pipefail
 
@@ -297,14 +285,14 @@ jobs:
           fi
 
       - name: Run `shfmt`
-        if: ${{ needs.changes.outputs.should_test == 'true' }}
+        if: ${{ steps.decide.outputs.should_test == 'true' }}
         run: |
           # shfmt is version-pinned via mise: brew/apt ship divergent versions
           # (3.14 changed heredoc-in-if formatting) and unpinned runners disagree.
           git ls-files -- ':(glob)install/**/*.sh' ':(glob)scripts/**/*.sh' | xargs mise x shfmt@3.14.1 -- shfmt -i 4 -sr -d
 
       - name: Check Python and Markdown formatting
-        if: ${{ needs.changes.outputs.should_test == 'true' }}
+        if: ${{ steps.decide.outputs.should_test == 'true' }}
         run: |
           # ruff and prettier come from home/dot_mise/config.toml (latest behind the cooldown).
           # mise -C resolves those versions and changes directory, so each check
@@ -317,18 +305,18 @@ jobs:
             sh -c 'cd "${GITHUB_WORKSPACE}" && git ls-files -z "*.md" | xargs -0 prettier --check'
 
       - name: Run `ShellCheck`
-        if: ${{ needs.changes.outputs.should_test == 'true' }}
+        if: ${{ steps.decide.outputs.should_test == 'true' }}
         run: |
           git ls-files -z 'setup.sh' 'install/*.sh' 'install/**/*.sh' 'scripts/*.sh' | xargs -0 shellcheck -x
 
       - name: Setup uv
-        if: ${{ needs.changes.outputs.should_test == 'true' }}
+        if: ${{ steps.decide.outputs.should_test == 'true' }}
         uses: astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7 # v10.2.0
         with:
           enable-cache: false
 
       - name: Run Python unit tests
-        if: ${{ needs.changes.outputs.should_test == 'true' }}
+        if: ${{ steps.decide.outputs.should_test == 'true' }}
         run: |
           if [[ "${OS}" == ubuntu-* ]]; then
             sudo apt-get update && sudo apt-get install -y jq zsh
@@ -340,7 +328,7 @@ jobs:
           make unit-test
 
       - name: Prepare public dotfiles fixture
-        if: ${{ needs.changes.outputs.should_test == 'true' }}
+        if: ${{ steps.decide.outputs.should_test == 'true' }}
         run: |
           set -euo pipefail
 
@@ -380,7 +368,7 @@ jobs:
           } >> "${GITHUB_ENV}"
 
       - name: Run unit test
-        if: ${{ needs.changes.outputs.should_test == 'true' }}
+        if: ${{ steps.decide.outputs.should_test == 'true' }}
         run: |
           if [ "${OS}" == "macos-14" ]; then
             # Bats uses its own tracing internals on macOS, and bashcov can
@@ -403,14 +391,14 @@ jobs:
             ruby ./scripts/run_bashcov_unit_test.rb "${bashcov_args[@]}" -- ./scripts/run_unit_test.sh
 
       - name: Setup for Codecov
-        if: ${{ needs.changes.outputs.should_test == 'true' && matrix.os == 'ubuntu-24.04' && !endsWith(github.actor, '[bot]') }}
+        if: ${{ steps.decide.outputs.should_test == 'true' && matrix.os == 'ubuntu-24.04' && !endsWith(github.actor, '[bot]') }}
         run: |
           # codecov-action uses these tools while preparing and uploading the
           # explicit Cobertura report in this repository setup.
           sudo apt-get install -y jq curl
 
       - name: Upload coverage to Codecov
-        if: ${{ needs.changes.outputs.should_test == 'true' && matrix.os == 'ubuntu-24.04' && !endsWith(github.actor, '[bot]') }}
+        if: ${{ steps.decide.outputs.should_test == 'true' && matrix.os == 'ubuntu-24.04' && !endsWith(github.actor, '[bot]') }}
         uses: codecov/codecov-action@303a32d7a59b442fa8d48b6a1cc6825c09c847a5 # v7
         env:
           CODECOV_TOKEN: ${{ secrets.CODECOV_TOKEN }}
"""An .orchestration-only PR runs no bootstrap or test matrix, and every required context still reports (T128 INV-2)."""

from __future__ import annotations

import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = ROOT / ".github/workflows"
REMOTE = WORKFLOWS / "remote.yaml"
TEST = WORKFLOWS / "test.yaml"
AGENT_ASSETS = WORKFLOWS / "agent-assets.yml"
# A copy of the ruleset's required status checks (a unit test cannot read the
# ruleset); this is what changes when the ruleset changes.
REQUIRED_CONTEXTS = frozenset(
    {
        "validate",
        "test (ubuntu-24.04, server)",
        "test (ubuntu-24.04, client)",
        "test (macos-14, client)",
        "public-bootstrap (ubuntu-24.04, server)",
        "public-bootstrap (ubuntu-24.04, client)",
        "public-bootstrap (macos-14, client)",
    }
)
BOOTSTRAP_DECISION = "Decide whether the diff needs a bootstrap"
TEST_DECISION = "Decide whether the diff needs the unit tests"
# The jobs that skip their heavy steps, each with its own decision step and gate.
DECIDING_JOBS = (
    (REMOTE, "public-bootstrap", BOOTSTRAP_DECISION, "steps.decide.outputs.should_run == 'true'"),
    (REMOTE, "private-bootstrap", BOOTSTRAP_DECISION, "steps.decide.outputs.should_run == 'true'"),
    (TEST, "test", TEST_DECISION, "steps.decide.outputs.should_test == 'true'"),
)
# Steps a deciding job runs on every diff: setup, the checkout the decision
# needs, the decision, and the notices that say what was skipped.
UNGATED_STEPS = frozenset(
    {
        "Configure isolated HOME",
        "Configure Git defaults",
        "actions/checkout",
        "Checkout repository",
        BOOTSTRAP_DECISION,
        TEST_DECISION,
        "Skip the bootstrap for an .orchestration-only diff",
        "Skip full unit test run for unrelated changes",
        "Explain skipped private bootstrap",
    }
)


PLAIN_KEY = re.compile(r"([a-z0-9_-]+):(?:[ \t](.*))?")


def plain_key(text: str, line: str) -> tuple[str, str]:
    """A `name: value` pair in the plain form, or ValueError: a form the reader does not parse must not read as absent."""
    match = PLAIN_KEY.fullmatch(text)
    if not match:
        raise ValueError(f"unsupported key form inside jobs: {line!r}")
    return match.group(1), (match.group(2) or "").strip()


def jobs(path: Path) -> dict[str, dict]:
    """Each job's own keys (two-space job names, four-space keys) and its steps, read from the indentation after `jobs:`.

    Fails closed: a job name, job key or step key that is not the plain form `name:` (lower-case letters, digits,
    `_` and `-`, the colon right after; no quotes, escapes or flow mappings) raises ValueError, so every structural
    test fails instead of reading an unsupported form as "no `if`". The test environment has no YAML parser.
    """
    result: dict[str, dict] = {}
    job = step = block_key = None
    in_steps = False
    for line in path.read_text().split("\njobs:\n", 1)[1].split("\n"):
        stripped = line.strip()
        indent = len(line) - len(line.lstrip(" "))
        if step is not None and block_key == "run" and step.get("run") == "|" and (not stripped or indent >= 10):
            step["script"] = step.get("script", "") + line[10:] + "\n"
            continue
        if not stripped or stripped.startswith("#"):
            continue
        if indent == 0:
            break
        if indent == 2:
            name, value = plain_key(stripped, line)
            if value:
                raise ValueError(f"unsupported job form inside jobs: {line!r}")
            job = {"keys": {}, "steps": []}
            result[name] = job
            step = block_key = None
            in_steps = False
        elif job is None:
            raise ValueError(f"unsupported line before the first job: {line!r}")
        elif not job["keys"] and indent != 4:
            # Sibling keys share one indentation, so a body shifted off four spaces would hide all of them.
            raise ValueError(f"unsupported job body indentation inside jobs: {line!r}")
        elif indent == 4:
            key, value = plain_key(stripped, line)
            job["keys"][key] = value
            in_steps = key == "steps"
            step = block_key = None
        elif in_steps and indent == 6:
            if not stripped.startswith("- "):
                raise ValueError(f"unsupported step form inside jobs: {line!r}")
            step = {}
            job["steps"].append(step)
            block_key, step[block_key] = plain_key(stripped[2:], line)
        elif in_steps and indent == 8:
            if step is None:
                raise ValueError(f"unsupported step form inside jobs: {line!r}")
            block_key, step[block_key] = plain_key(stripped, line)
    return result


def step_name(step: dict) -> str:
    return step.get("name") or step.get("uses", "").split("@", 1)[0]


def matrix_contexts(path: Path, job: str) -> set[str]:
    """The `job (os, system)` contexts of a matrix job: include pairs, or the os x system product minus exclude."""
    text = path.read_text().split(f"\n  {job}:\n", 1)[1].split("\n    runs-on:", 1)[0]
    pair = r"- os: ([\w.-]+)\n\s+system: (\w+)"
    lists = re.search(r"os: \[([^\]]+)\]\n\s+system: \[([^\]]+)\]", text)
    if not lists:
        return {f"{job} ({os_name}, {system})" for os_name, system in re.findall(pair, text)}
    excluded = set(re.findall(pair, text.split("exclude:", 1)[1].split("include:", 1)[0]))
    return {
        f"{job} ({os_name.strip()}, {system.strip()})"
        for os_name in lists.group(1).split(",")
        for system in lists.group(2).split(",")
        if (os_name.strip(), system.strip()) not in excluded
    }


def decide_script(path: Path, name: str) -> str:
    scripts = [step["script"] for step in jobs(path)[name]["steps"] if step.get("id") == "decide"]
    assert len(scripts) == 1, scripts
    return scripts[0]

 succeeded in 95ms:
     1	# Report: dotfiles-T128-ci-skip-orchestration-a02
     2	
     3	- Seat: `claude-standard-dot-a003` in `.claude/worktrees/worker-f`, branch `feat/ci-skip-orchestration`, PR #320, continuing from `dc4e6c37`. Reset successor of `dotfiles-T128-ci-skip-orchestration-a01` under INV-6 (reset record `.orchestration/acceptance/dotfiles-T128-ci-skip-orchestration-a01-design-reset.md`); the implementation on `dc4e6c37` stays.
     4	- Task file sha256 `2c3a5ee2…` checked against TASK 07:35:34Z and copied byte-identical in `406ca746` to `.orchestration/dotfiles-T128-ci-skip-orchestration-a02/task.md` (the a01 directory stays as it is). Content commit `a35a751e`; then this evidence.
     5	
     6	## What changed (`a35a751e`, `tests/unit/test_workflow_orchestration_skip.py` only)
     7	
     8	The hand-written workflow reader now fails closed. The test environment has no YAML parser (`make unit-test` runs bare `uv run python`), and no dependency is added. Inside `jobs:`:
     9	
    10	- a job name, a job key or a step key must be the plain form `name:` (`[a-z0-9_-]+`, the colon right after, then end of line or a space). Anything else raises `ValueError`: quotes, escapes, a space before the colon, a flow mapping, `<<` merge keys. A job name must carry no value, so `job: {…}` raises too. Comments and blank lines are skipped, and `run: |` script lines are captured as before.
    11	- a job body's first line must sit at four spaces, and a step item's first key must follow `- ` directly. Sibling keys share one indentation, so this pins every job and step key to its column. A body shifted to six spaces, or `-   name:` with its keys at ten, would otherwise hide every key from the reader while GitHub reads them (validation §3, the two positional rows).
    12	- a line at six spaces inside `steps:` that is not a `- ` item, or a step key before any item, raises.
    13	
    14	`test_the_reader_fails_closed_on_unsupported_key_forms` replaces `test_structural_tests_see_quoted_keys` (a01's revise check): under the reset, quoted keys raise instead of reading as bare ones, so a01's `revise.yaml` selector no longer resolves. a01 is reset history. The new test has eight subTests: the task's four forms (`if : false`, `"\x69f": false`, `continue-on-error : true`, a step written as `{ if: false }`), a quoted job name, a quoted step key, a shifted job body and a shifted step item. Each must raise.
    15	
    16	## Threat table (the completion condition)
    17	
    18	| Row | Disposition | Where |
    19	|---|---|---|
    20	| The PR edits the workflow files themselves | residual, as the task states | `tests/unit/test_workflow_security.py` passes unchanged (validation §2) |
    21	| The decision step misclassifies a diff | closed | `DecisionTest.test_a_pull_request_skips_the_bootstrap_only_for_an_orchestration_only_diff`, `…test_the_unit_test_decision_skips_an_orchestration_only_diff`, `…test_the_unit_test_decision_ignores_renames` |
    22	| A required job is skipped | closed | `RequiredContextsTest.test_no_required_contexts_job_has_a_job_level_if_or_needs` and `…test_no_job_is_left_for_a_required_job_to_need`, read by the fail-closed reader: each of the six unsupported-form mutations errors them (validation §3) |
    23	| The decision step itself fails | closed | `DecisionStepTest.test_each_deciding_job_decides_after_its_checkout_and_fails_closed`, `…test_every_heavy_step_carries_its_jobs_decision`, read by the same reader |
    24	| The reader misses a valid YAML form | closed | `RequiredContextsTest.test_the_reader_fails_closed_on_unsupported_key_forms`. The task's four mutations, and the two positional ones found while checking the reader, each hide a real key from GitHub's YAML parser and fail every structural test that reads the mutated job (validation §3). The lenient reader, and the reader without the indentation check, each fail the test |
    25	| The design is not on `main` at dispatch | closed by the orchestrator, as the task states | the boundary PR `orchestration/boundary-2026-10-11-2` and `gh pr update-branch` before the final audit. The worker runs no `gh pr update-branch` |
    26	| Push and schedule have no PR range | closed | `DecisionTest.test_every_event_but_pull_request_bootstraps` |
    27	
    28	The earlier proofs still fail against the new reader at `a35a751e`: 16 of 16 from a01, and 3 of 3 from a01's revise. a01's fourth revise row targeted the removed quoted-key regex and no longer applies; the lenient-reader row replaces it (validation §4).
    29	
    30	## Notes
    31	
    32	- The full local `make unit-test` fails in the sandbox the same way on `origin/main`: the same failing ids, none only at this head (validation §5). This module passes under it, and CI's `Run Python unit tests` step is the verdict.
    33	- The final head's CI and Bot wait are in the RESULT and the main-checkout copy of this report.
    34	- Understand-Anything hook: did not fire. plan-mode-used: no.
    35	
    36	## CompactionDB
    37	
    38	`memory add` printed `c62781a9-a65b-4484-925c-383fddb9a114` (validation §6).
    39	
    40	cost: n/a
    41	
    42	## Final head `fca44b4c` (main-checkout copy)
    43	
    44	- Commits: `406ca746` (task copy), `a35a751e` (the fail-closed reader), `fca44b4c` (evidence), pushed together at 07:53:53Z. No `gh pr update-branch` was run here: the orchestrator runs it after the boundary PR merges.
    45	- CI: 13 of 13 pass on `fca44b4c`, the seven required contexts among them; the watcher exited 0 and was joined before the RESULT (validation §7).
    46	- Bot: one round on `fca44b4c`. The code review completed at 07:56:00Z with no review object and no comment, and the Bot reacted 👍 at 07:56:03Z (the security review last ran on `9fcd2b0`). `bot_rounds=1`, no fix round. No thread opened under a02; 4240499289 (a01, `fixed:e872f69f`) is the PR's only Bot thread.
    47	## Amendment 1 (TASK 09:41:42Z, sha256 `4de54fde…`)
    48	
    49	The boundary PR 321 merged at 09:40Z, so design `4520b8f0…` and this task id's `implementing_tasks` entry are on `main`; this is the TASK the worker acts on (INV-2), and the 07:35Z one is superseded. The task file changed only in `design_review.receipt` (round 18) and the design-on-main row of the threat table. The copy at `.orchestration/dotfiles-T128-ci-skip-orchestration-a02/task.md` is re-made byte-identical (validation §8). No content change; no `gh pr update-branch` here, as the orchestrator runs it after this RESULT.
    50	
    51	## Final head `a8c2bed9` (main-checkout copy, Amendment 1)
    52	
    53	- Commit: `a8c2bed9` (the Amendment 1 task copy and the evidence note), pushed at 09:43:15Z.
    54	- CI: 13 of 13 pass on `a8c2bed9`; the watcher exited 0 and was joined before the RESULT (validation §9).
    55	- Bot: code review completed at 09:44:38Z with no review object and no comment, 👍 at 09:44:41Z. `bot_rounds=2` under a02, no fix round; no thread opened under a02.
     1	---
     2	task_id: dotfiles-T128-ci-skip-orchestration-a02
     3	seat: claude-standard-dot-a003
     4	permission_gated_commands: 13
     5	---
     6	
     7	# Sandbox record: dotfiles-T128-ci-skip-orchestration-a02
     8	
     9	- Period: from the AGMSG-TASK (2026-10-11T07:35:34Z) to the RESULT. Edits, the unit tests, the YAML parse (`--with pyyaml`, offline), ruff, prettier, every proof, the `-v` listings, the full-suite comparison and the commits ran inside the sandbox (`git -c commit.gpgsign=false`, `UV_OFFLINE=1`). No `allowed_domains`, no refusal.
    10	
    11	`permission_gated_commands` counts every Bash call with `dangerouslyDisableSandbox`, one per call (`agmsg-dispatch` included; each Bot loop is one call). Main-checkout copy: the count is final, every row ran.
    12	
    13	| # | Command | Step 4 case |
    14	|--:|---|---|
    15	| 1 | `cd ~/Workspace/dotfiles && uv run --no-project .claude/hooks/contextdb_cli.py memory add …` | main-checkout `memory add` |
    16	| 2 | the authorized push (`406ca746`, `a35a751e` and this evidence) | `git push` |
    17	| 3 | `gh pr checks 320 … --watch` on the pushed head (background, exit status joined) | `gh` |
    18	| 4 | Bot wait on the pushed head, `scratchpad/bot-wait.sh`, timed from the push (the PR is already ready) | `gh` only |
    19	| 5 | final recheck of reviews, review comments and the connector summary right before the RESULT (`gh` only) | `gh` |
    20	| 6 | the masked copy of the five evidence files to the TASK's `expected_*` paths in the main checkout | artifact copy with the repository masker |
    21	| 7 | `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T128-ci-skip-orchestration-a02 …` | `agmsg-dispatch` |
    22	
    23	## Amendment 1
    24	
    25	Calls #1–#7 ran for the first RESULT (main-checkout copy). The task copy commit was made inside the sandbox; only the push leaves it. Main-checkout copy: the count is final, every row ran.
    26	
    27	| # | Command | Step 4 case |
    28	|--:|---|---|
    29	| A1 | the authorized push (the Amendment 1 task copy and this evidence) | `git push` |
    30	| A2 | `gh pr checks 320 … --watch` on the pushed head (background, exit status joined) | `gh` |
    31	| A3 | Bot wait on the pushed head, `scratchpad/bot-wait.sh`, timed from the push | `gh` only |
    32	| A4 | final recheck of reviews, review comments and the connector summary right before the RESULT (`gh` only) | `gh` |
    33	| A5 | the masked copy of the five evidence files to the TASK's `expected_*` paths in the main checkout | artifact copy with the repository masker |
    34	| A6 | `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T128-ci-skip-orchestration-a02 …` | `agmsg-dispatch` |
     1	# Acceptance: dotfiles-T128-ci-skip-orchestration-a02 (reset continuation of A5; plan 006 Phase A5)
     2	
     3	- **Decision:** pending (INV-2 re-dispatch after boundary PR #321 merges, `gh pr update-branch`, the final audit on that head, then the merge; PR #320 merges before PR #318).
     4	- pr=320
     5	- **Worker:** `claude-standard-dot-a003`, `.claude/worktrees/worker-f`, branch `feat/ci-skip-orchestration`. a02 TASK at 07:38Z (task file `2c3a5ee2…`, written by the review seat as the reset redesign of a01, anchored by RESULT 502), RESULT 516 at 08:04:51Z on `fca44b4c`: commits `406ca746` (task.md), `a35a751e` (the fail-closed reader), `fca44b4c` (evidence). CI 13 of 13, watcher joined; `bot_rounds=1`, no fix round, no thread under a02.
     6	- **Orchestrator review (diff `dc4e6c37..fca44b4c`):** the workflow reader raises `ValueError` for any job name, job key or step key inside `jobs:` that is not the plain form `name:` (no quotes, escapes, spaced colon, flow mapping or merge key), for a job body whose first line is not at four spaces and for a step item with extra spaces after the dash (two positional-hiding forms the worker found: a body shifted to six spaces hid `if: false` from the reader while GitHub reads it); `test_the_reader_fails_closed_on_unsupported_key_forms` replaces the a01 revise's quoted-key test (its selector retired; quoted keys now raise); the four task forms plus the two positional forms each hide a real key per PyYAML and fail every structural test that reads the mutated job; a lenient reader and a missing indentation check each fail the reader test; the earlier proofs still fail. Approved.
     7	- **Sweep (`…-ci-skip-orchestration-a02-pr-feedback.json`, head `fca44b4c`):** the a01 thread 4240499289 `fixed:e872f69f` (resolved), the orchestrator's reply objects, the containers and notices `not-applicable`; 0 unresolved threads.
     8	- **INV-2 (the design on `main` before the TASK the worker acts on):** the 07:38Z TASK predates design v17 on `main`; after boundary PR #321 merges, an amendment TASK carrying the current task file (`6457b81f…`, the INV-2 row reworded on the Bot's P1 4240758696) is sent and the worker re-copies task.md and re-sends its RESULT; the acceptance record names both TASK ids. The branch then takes the new base with `gh pr update-branch` and the final audit runs on that head.
     9	- **Exemption declared:** acceptance and evidence-sync bookkeeping; agmsg control plane.
    10	
    11	<!-- audit-input-boundary -->

**Debugging YAML indentation issues**
**Examining alias and job parsing limitations**
codex
The pinned workflows make the decision inside each job, use a full-history fetch, and disable rename detection. I’m now checking whether unsupported YAML can evade the reader and whether the submitted evidence supports the post-boundary dispatch and final-head CI claims.

mcp: codex_apps/github.fetch_pr started
mcp: codex_apps/github.fetch_commit_workflow_runs started
exec
/bin/zsh -lc "nl -ba .orchestration/validation/dotfiles-T128-ci-skip-orchestration-a02.md | sed -n '1,245p'; python3 -B - <<'PY'
import json
p='.orchestration/validation/dotfiles-T128-ci-skip-orchestration-a02-pr-feedback.json'
d=json.load(open(p))
print(json.dumps(d,ensure_ascii=False,indent=2))
PY" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc "sed -n '125,182p' ~/.agents/skills/agmsg-orchestration/SKILL.md" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 exited 1 in 72ms:
     1	# Validation: dotfiles-T128-ci-skip-orchestration-a02
     2	
     3	Every block is the verbatim output of the command shown, run in `.claude/worktrees/worker-f` on `feat/ci-skip-orchestration` (PR #320). This main-checkout copy covers `a35a751e`, §7 the final head `fca44b4c`, §8 and §9 Amendment 1 and its head `a8c2bed9` (design INV-8).
     4	
     5	## 1. Task file
     6	
     7	```
     8	$ shasum -a 256 ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T128-ci-skip-orchestration-a02.md .orchestration/dotfiles-T128-ci-skip-orchestration-a02/task.md | cut -c1-64
     9	2c3a5ee2439a4c8e0aa16e0013e9b8acfcbb82fc330b259f7748f34938d5d9bc
    10	2c3a5ee2439a4c8e0aa16e0013e9b8acfcbb82fc330b259f7748f34938d5d9bc
    11	```
    12	
    13	## 2. Checks at `a35a751e` (task validation: the YAML parse, the module; plus formatting and the security pins)
    14	
    15	```
    16	$ git log --oneline -3; git show --stat --format= a35a751e
    17	a35a751e test(ci): the workflow reader fails closed on any key form it does not parse
    18	406ca746 chore(orchestration): task file for dotfiles-T128-ci-skip-orchestration-a02
    19	dc4e6c37 fix(ci): the unit-test decision lists both sides of a rename; the workflow reader sees quoted keys
    20	 tests/unit/test_workflow_orchestration_skip.py | 109 ++++++++++++++++---------
    21	 1 file changed, 70 insertions(+), 39 deletions(-)
    22	$ UV_OFFLINE=1 uv run python -m unittest tests.unit.test_workflow_orchestration_skip tests.unit.test_workflow_security 2>&1 | tail -3; ruff format --config ruff.toml --check tests/unit/test_workflow_orchestration_skip.py; ruff check --config ruff.toml tests/unit/test_workflow_orchestration_skip.py
    23	Ran 21 tests in 4.718s
    24	
    25	OK
    26	1 file already formatted
    27	All checks passed!
    28	$ UV_OFFLINE=1 uv run --no-project --with pyyaml python -I -c "import sys, yaml; [print(p, sorted(yaml.safe_load(open(p))[\"jobs\"])) for p in sys.argv[1:]]" .github/workflows/remote.yaml .github/workflows/test.yaml .github/workflows/agent-assets.yml
    29	.github/workflows/remote.yaml ['private-bootstrap', 'public-bootstrap']
    30	.github/workflows/test.yaml ['test']
    31	.github/workflows/agent-assets.yml ['validate']
    32	```
    33	
    34	## 3. The unsupported forms (`scratchpad/mutate-a5-a02.sh` at `a35a751e`, a `git archive HEAD` copy)
    35	
    36	Each row inserts one form into a workflow. "YAML reads" is GitHub's view of it, from PyYAML on the mutated file: every form hides a real `if` or `continue-on-error`. The next lines run `RequiredContextsTest`, `DecisionStepTest` and `DecisionTest` (13 tests) and count the summary and `ValueError` lines. `errors=N` counts failing subTests, not tests. The task's four forms come first; the two positional rows (a shifted job body, a shifted step item) were found while checking the reader.
    37	
    38	```
    39	== unsupported form: spaced-job-key (remote.yaml): if : false
    40	   YAML reads: False
    41	   1 FAILED (errors=12)
    42	   1 Ran 13 tests in 1.732s
    43	  12 ValueError: unsupported key form inside jobs: '    if : false'
    44	== unsupported form: escaped-job-key (remote.yaml): "\x69f": false
    45	   YAML reads: False
    46	   1 FAILED (errors=12)
    47	   1 Ran 13 tests in 2.220s
    48	  12 ValueError: unsupported key form inside jobs: '    "\\x69f": false'
    49	== unsupported form: spaced-step-key (test.yaml): continue-on-error : true
    50	   YAML reads: True
    51	   1 FAILED (errors=9)
    52	   1 Ran 13 tests in 2.040s
    53	   9 ValueError: unsupported key form inside jobs: '        continue-on-error : true'
    54	== unsupported form: shifted-job-body (agent-assets.yml): if: false|runs-on: ubuntu-24.04
    55	   YAML reads: False
    56	   1 FAILED (errors=3)
    57	   1 Ran 13 tests in 3.463s
    58	   3 ValueError: unsupported job body indentation inside jobs: '      if: false'
    59	== unsupported form: shifted-step-item (remote.yaml): -   name: Decide whether the diff needs a bootstrap|continue-on-error: true
    60	   YAML reads: True
    61	   1 FAILED (errors=12)
    62	   1 Ran 13 tests in 1.583s
    63	  12 ValueError: unsupported key form inside jobs: '      -   name: Decide whether the diff needs a bootstrap'
    64	== unsupported form: flow-mapping-step (remote.yaml): - { if: false }
    65	   YAML reads: {'if': False}
    66	   1 FAILED (errors=12)
    67	   1 Ran 13 tests in 1.550s
    68	  12 ValueError: unsupported key form inside jobs: '      - { if: false }'
    69	== reader made lenient again (plain_key returns instead of raising) -> test_the_reader_fails_closed_on_unsupported_key_forms
    70	FAIL: test_the_reader_fails_closed_on_unsupported_key_forms (tests.unit.test_workflow_orchestration_skip.RequiredContextsTest.test_the_reader_fails_closed_on_unsupported_key_forms) (form='spaced job key')
    71	AssertionError: ValueError not raised
    72	FAIL: test_the_reader_fails_closed_on_unsupported_key_forms (tests.unit.test_workflow_orchestration_skip.RequiredContextsTest.test_the_reader_fails_closed_on_unsupported_key_forms) (form='escaped job key')
    73	== restored: OK
    74	== reader without the job-body indentation check -> test_the_reader_fails_closed_on_unsupported_key_forms
    75	FAIL: test_the_reader_fails_closed_on_unsupported_key_forms (tests.unit.test_workflow_orchestration_skip.RequiredContextsTest.test_the_reader_fails_closed_on_unsupported_key_forms) (form='shifted job body')
    76	AssertionError: ValueError not raised
    77	FAILED (failures=1)
    78	```
    79	
    80	The tests that still pass under each form (the same harness with `-v`). Each is either the reader test itself (it rebuilds its own forms), or a test that never reads the mutated job's keys through `jobs()`: the context-name check reads job names by regex, and the rest read the other workflow file.
    81	
    82	```
    83	== unsupported form: spaced-job-key (remote.yaml): if : false
    84	test_the_reader_fails_closed_on_unsupported_key_forms ... ok
    85	test_the_required_contexts_are_the_workflows_jobs ... ok
    86	test_a_main_tests_job_when_present_decides_in_itself ... ok
    87	test_the_unit_test_decision_ignores_renames ... ok
    88	test_the_unit_test_decision_skips_an_orchestration_only_diff ... ok
    89	== unsupported form: escaped-job-key (remote.yaml): "\x69f": false
    90	test_the_reader_fails_closed_on_unsupported_key_forms ... ok
    91	test_the_required_contexts_are_the_workflows_jobs ... ok
    92	test_a_main_tests_job_when_present_decides_in_itself ... ok
    93	test_the_unit_test_decision_ignores_renames ... ok
    94	test_the_unit_test_decision_skips_an_orchestration_only_diff ... ok
    95	== unsupported form: spaced-step-key (test.yaml): continue-on-error : true
    96	test_the_reader_fails_closed_on_unsupported_key_forms ... ok
    97	test_the_required_contexts_are_the_workflows_jobs ... ok
    98	test_both_bootstrap_jobs_decide_with_the_same_script ... ok
    99	test_a_pull_request_skips_the_bootstrap_only_for_an_orchestration_only_diff ... ok
   100	test_every_event_but_pull_request_bootstraps ... ok
   101	== unsupported form: shifted-job-body (agent-assets.yml): if: false|runs-on: ubuntu-24.04
   102	test_no_job_is_left_for_a_required_job_to_need ... ok
   103	test_the_reader_fails_closed_on_unsupported_key_forms ... ok
   104	test_a_main_tests_job_when_present_decides_in_itself ... ok
   105	test_both_bootstrap_jobs_decide_with_the_same_script ... ok
   106	test_each_deciding_job_decides_after_its_checkout_and_fails_closed ... ok
   107	test_every_heavy_step_carries_its_jobs_decision ... ok
   108	test_a_pull_request_skips_the_bootstrap_only_for_an_orchestration_only_diff ... ok
   109	test_every_event_but_pull_request_bootstraps ... ok
   110	test_the_decision_survives_a_base_that_moved_after_the_checkout ... ok
   111	test_the_unit_test_decision_ignores_renames ... ok
   112	test_the_unit_test_decision_skips_an_orchestration_only_diff ... ok
   113	== unsupported form: shifted-step-item (remote.yaml): -   name: Decide whether the diff needs a bootstrap|continue-on-error: true
   114	test_the_reader_fails_closed_on_unsupported_key_forms ... ok
   115	test_the_required_contexts_are_the_workflows_jobs ... ok
   116	test_a_main_tests_job_when_present_decides_in_itself ... ok
   117	test_the_unit_test_decision_ignores_renames ... ok
   118	test_the_unit_test_decision_skips_an_orchestration_only_diff ... ok
   119	== unsupported form: flow-mapping-step (remote.yaml): - { if: false }
   120	test_the_reader_fails_closed_on_unsupported_key_forms ... ok
   121	test_the_required_contexts_are_the_workflows_jobs ... ok
   122	test_a_main_tests_job_when_present_decides_in_itself ... ok
   123	test_the_unit_test_decision_ignores_renames ... ok
   124	test_the_unit_test_decision_skips_an_orchestration_only_diff ... ok
   125	== restored: OK
   126	```
   127	
   128	## 4. The earlier proofs against the new reader (`scratchpad/mutate-a5.sh` and `scratchpad/mutate-a5-r1.sh` at `a35a751e`)
   129	
   130	```
   131	$ awk '/^== broken rule/{if(n!="")print n, f; n=$4; f="no"} /^(FAIL|ERROR):/{f="fails"} END{print n, f}' mutate-a5.log mutate-a5-r1.log; grep -E 'DID NOT APPLY|restored' mutate-a5.log mutate-a5-r1.log
   132	public-bootstrap-step-ungated fails
   133	private-deploy-key-ungated fails
   134	unit-test-step-ungated fails
   135	needs-on-a-required-job fails
   136	job-level-if-on-a-required-job fails
   137	changes-job-back fails
   138	decision-continue-on-error fails
   139	decision-before-checkout-history fails
   140	private-script-drift fails
   141	non-pr-events-judged fails
   142	renames-collapsed fails
   143	classification-inverted fails
   144	unit-test-decision-ignores-orchestration fails
   145	required-leg-dropped fails
   146	shallow-base-fetch-remote fails
   147	shallow-base-fetch-test fails
   148	unit-test-diff-detects-renames fails
   149	quoted-job-level-if fails
   150	quoted-continue-on-error-on-decide fails
   151	== reader-sees-bare-keys-only: MUTATION DID NOT APPLY
   152	== restored: OK
   153	== restored: OK
   154	```
   155	
   156	`reader-sees-bare-keys-only` targeted the quoted-key regex that this commit removes; the lenient-reader row of §3 replaces it.
   157	
   158	## 5. The full suite locally, this head against `origin/main` (`git archive origin/main` copy; failing ids from the `FAIL:`/`ERROR:` lines)
   159	
   160	```
   161	$ UV_OFFLINE=1 make unit-test   # at this head; the same discover in the origin/main copy; then comm on the sorted ids
   162	base (origin/main b896d9bc): FAILED (failures=114, errors=103, skipped=2)  failing ids: 188
   163	head (a35a751e, make unit-test): FAILED (failures=114, errors=103, skipped=2) (make exits 2)  failing ids: 188
   164	only at head:
   165	only at base:
   166	this module under make unit-test:
   167	test_a_main_tests_job_when_present_decides_in_itself ... ok
   168	test_both_bootstrap_jobs_decide_with_the_same_script ... ok
   169	test_each_deciding_job_decides_after_its_checkout_and_fails_closed ... ok
   170	test_every_heavy_step_carries_its_jobs_decision ... ok
   171	test_a_pull_request_skips_the_bootstrap_only_for_an_orchestration_only_diff ... ok
   172	test_every_event_but_pull_request_bootstraps ... ok
   173	test_the_decision_survives_a_base_that_moved_after_the_checkout ... ok
   174	test_the_unit_test_decision_ignores_renames ... ok
   175	test_the_unit_test_decision_skips_an_orchestration_only_diff ... ok
   176	test_no_job_is_left_for_a_required_job_to_need ... ok
   177	test_no_required_contexts_job_has_a_job_level_if_or_needs ... ok
   178	test_the_reader_fails_closed_on_unsupported_key_forms ... ok
   179	test_the_required_contexts_are_the_workflows_jobs ... ok
   180	```
   181	
   182	The local failures are the sandbox's, as on a01 (test commits that inherit the global signing setting, `mktemp` outside the writable paths, no pty devices, no local `main` ref). They are identical on `origin/main`. CI's `Run Python unit tests` step is the verdict.
   183	
   184	## 6. CompactionDB (main checkout, outside the sandbox through the permission gate)
   185	
   186	```
   187	$ cd ~/Workspace/dotfiles && uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content '[memory:decision] dotfiles-T128-ci-skip-orchestration-a02 …'
   188	c62781a9-a65b-4484-925c-383fddb9a114
   189	```
   190	
   191	## 7. Final head `fca44b4c` (main-checkout copy)
   192	
   193	```
   194	$ gh pr checks 320 --repo mryfmo/dotfiles --watch --interval 30   # final table; exit 0
   195	CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
   196	GitGuardian Security Checks	pass	0	https://dashboard.gitguardian.com	
   197	private-bootstrap (macos-14, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/38122927319/job/114421200472	
   198	private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/38122927319/job/114421200388	
   199	private-bootstrap (ubuntu-24.04, server)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/38122927319/job/114421200263	
   200	public-bootstrap (macos-14, client)	pass	6m51s	https://github.com/mryfmo/dotfiles/actions/runs/38122927319/job/114421200408	
   201	public-bootstrap (ubuntu-24.04, client)	pass	9m57s	https://github.com/mryfmo/dotfiles/actions/runs/38122927319/job/114421200432	
   202	public-bootstrap (ubuntu-24.04, server)	pass	6m46s	https://github.com/mryfmo/dotfiles/actions/runs/38122927319/job/114421200378	
   203	test (macos-14, client)	pass	5m52s	https://github.com/mryfmo/dotfiles/actions/runs/38122927273/job/114421199766	
   204	test (ubuntu-24.04, client)	pass	8m0s	https://github.com/mryfmo/dotfiles/actions/runs/38122927273/job/114421199949	
   205	test (ubuntu-24.04, server)	pass	5m8s	https://github.com/mryfmo/dotfiles/actions/runs/38122927273/job/114421199892	
   206	test (ubuntu-26.04, client)	pass	8m22s	https://github.com/mryfmo/dotfiles/actions/runs/38122927273/job/114421199888	
   207	validate	pass	51s	https://github.com/mryfmo/dotfiles/actions/runs/38122927329/job/114421200195	
   208	$ bash scratchpad/bot-wait.sh 320 fca44b4c25d4b20d0b029dc5d8dd16f9c37a7dbf 2026-10-11T07:53:53Z   # last poll
   209	poll 5 07:56:08Z head fca44b4c25d4b20d0b029dc5d8dd16f9c37a7dbf asked=no
   210	reviews: 
   211	comments: 
   212	code-review-completed: | 📝 **Code Review** | ✅ **Completed** <relative-time datetime="2026-10-11T07:56:00.911325Z">2026-10-11T07:56:00.911325Z</relative-time> | `fca44b4` | New commits |
   213	DONE
   214	$ # final recheck right before the RESULT
   215	2026-10-11T08:04:16Z
   216	$ gh pr view 320 --json headRefOid,state,isDraft
   217	fca44b4c25d4b20d0b029dc5d8dd16f9c37a7dbf	OPEN	false
   218	$ gh api --paginate repos/mryfmo/dotfiles/pulls/320/reviews --jq '.[]|select(.user.type=="Bot")|[.id,.commit_id[0:8],.submitted_at]|@tsv'
   219	5482144676	b3f88beb	2026-10-11T06:15:10Z
   220	$ gh api --paginate repos/mryfmo/dotfiles/pulls/320/comments --jq '.[]|select(.in_reply_to_id == null and .user.type=="Bot")|[.id,.original_commit_id[0:8],.path,(.original_line|tostring)]|@tsv'
   221	4240499289	b3f88beb	.github/workflows/remote.yaml	61
   222	$ gh api repos/mryfmo/dotfiles/issues/comments/6105983720 --jq .body | grep -E 'Code Review|Security Review'
   223	| 📝 **Code Review** | ✅ **Completed** <relative-time datetime="2026-10-11T07:56:00.911325Z">2026-10-11T07:56:00.911325Z</relative-time> | `fca44b4` | New commits |
   224	| 🔒 **Security Review** | ✅ **Completed** <relative-time datetime="2026-10-11T05:55:43.193970Z">2026-10-11T05:55:43.193970Z</relative-time> | `9fcd2b0` | Draft marked ready |
   225	$ gh api repos/mryfmo/dotfiles/issues/320/reactions --jq '.[]|[.user.login,.content,.created_at]|@tsv'
   226	chatgpt-codex-connector[bot]	+1	2026-10-11T07:56:03Z
   227	```
   228	## 8. Amendment 1: the task copy
   229	
   230	```
   231	$ shasum -a 256 ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T128-ci-skip-orchestration-a02.md .orchestration/dotfiles-T128-ci-skip-orchestration-a02/task.md | cut -c1-64
   232	4de54fdec5db667e940365703ee5e16cd1d91f52794c79c75b48aad7eb0a8763
   233	4de54fdec5db667e940365703ee5e16cd1d91f52794c79c75b48aad7eb0a8763
   234	$ git diff --stat HEAD -- .orchestration/dotfiles-T128-ci-skip-orchestration-a02/task.md
   235	 .orchestration/dotfiles-T128-ci-skip-orchestration-a02/task.md | 4 ++--
   236	 1 file changed, 2 insertions(+), 2 deletions(-)
   237	```
   238	
   239	## 9. Final head `a8c2bed9` (main-checkout copy, Amendment 1)
   240	
   241	```
   242	$ gh pr checks 320 --repo mryfmo/dotfiles --watch --interval 30   # final table; exit 0
   243	CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
   244	GitGuardian Security Checks	pass	0	https://dashboard.gitguardian.com	
   245	private-bootstrap (macos-14, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/38129377997/job/114440329188	
zsh:1: can't create temp file for here document: operation not permitted

 succeeded in 94ms:

Liveness messages:

```text
AGMSG-PING v1 task_id=<id> reason=<short-reason>
AGMSG-PONG v1 task_id=<id> status=alive|blocked note=<short-note>
```

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
6. Send `AGMSG-TASK v1` with the exact artifact paths and `done_signal=AGMSG-RESULT`. Pass every `send.sh`/`poke.sh` body with `--body-file <path>` (both take it in agmsg v1.5.0), never as a positional argument: a positional `<text>` passes through the caller's own shell first, where a backtick or `$( )` in the body silently executes and vanishes from what arrives (upstream #378). `agmsg-dispatch` is the one exception and takes a single-line, shell-safe positional message. Pick the path by how the recipient is seated, never by inferring pane or agent status: a worker in a `herdr-agents` pane gets `agmsg-dispatch <team> <from> <to> <pane_id> "<message>"` (send, generic wake, `read_at` wait; single-line shell-safe text only), the sanctioned wake path until worker seating writes placement records at launch, because `poke.sh` exits 1 with "no placement record" for a hand-joined member, and a herdr-agents worker gets a record only once it acts from its own pane (upstream `send.sh`/`inbox.sh` record the acting pane, #1109); a spawn-seated member (placement record `run/spawn.*`; `team.sh <team> --json` shows its pane) gets `poke.sh <team> <name> --body-file <path> [--retries N --retry-delay SECONDS --backoff fixed|exponential]`, which types and submits in one call and refuses to type over an in-progress draft (#1321/#1322); a pane-less member gets `send.sh <team> <from> <to> --body-file <path>` and its own delivery mode. Verify delivery via the messages.db `read_at` column. `poke.sh` exit codes: 10 = terminal unreachable, 12 = pane gone or no live agent, 14/15 = refused to type over a changing or unlocatable input box, 13 = the driver has no poke path for this pane (for example a `plain` terminal); where poke.sh's narrow agmsg-message fallback succeeds it exits 0, so 13 means nothing was delivered, and the printed reason names the native channel, asks the caller to claim its own identity first, or reports that the fallback failed. Never retry a 13 as `send.sh` yourself: that overrides the driver's considered refusal and can double-deliver. Seating case: a worker in an unviewed or headless Herdr workspace (no client attached, a small pane rect such as 18x41) makes `poke.sh` exit 14/15 from its TUI input locator; that is a locator refusal, not evidence about the worker's state, so wake it with `agmsg-dispatch` and verify `read_at`.
7. Track `max_turns`. Use `AGMSG-PING` for liveness if a worker stalls.
8. On `AGMSG-RESULT`, read the task file and every referenced artifact before deciding.
9. For a RESULT carrying `effects`, verify that every declared effect has the report's stated reverse mapping before acceptance; record any irreversible effect in the acceptance note.
10. For a RESULT that carries a pull request, integrate in this order. This is the single procedure that the PR integration rule, `AGENTS.md`, the README and the gh-first-workflow skill cite. A `gh pr update-branch` moves the head, so steps 1 to 4 run again on the new head. After an update-branch the orchestrator runs it, the order is CI on the new head, then the sweep, then the audit; an audit started before CI finishes sees incomplete evidence and returns an evidence-only `incorrect`. Select a checkout with git -C <absolute path>, never with cd, which the sandboxed Bash may not honour. After moving the review worktree to the audited head, verify git -C <review> rev-parse HEAD equals that head and git -C <main> symbolic-ref --short HEAD prints main before the audit and the gate.
    1. Sweep the final head's feedback with `scripts/pr-feedback.py <pr> --json .orchestration/validation/<task>-pr-feedback.json` and give every item a `fixed:<commit>` or `not-applicable:<reason>` disposition, leaving none on `failure` or `warning` annotations. Optionally request `@coderabbitai full review` on the final head first; when a CodeRabbit review exists it is swept like any other item, and the gate does not require a bot review.
    2. Run the task-level audit of that head in the pair or headless form of the task-level audit bullet. It exits nonzero for every verdict other than `correct`. An exit with `Audit verdict: incorrect` is not a failed step: continue to step 3 and disposition its findings. A `blocked` or missing verdict means re-running the audit.
    3. Write the acceptance record, summarising the dispositions, with an `audit-finding:` line for every audit finding whatever the verdict (the gate needs them, through `AUDIT_DISPOSITIONS`, when it is `incorrect`).
    4. Run the gate: `AUDIT_EVIDENCE=<audit> [AUDIT_DISPOSITIONS=<acceptance record>] AGENT_REVIEWED=1 REVIEW_EVIDENCE=<receipt> BASE=origin/main PR_FEEDBACK_EVIDENCE=<json> make require-crit-review`.
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
2. Switch to the `repo` and read `task_file` before editing or running validations. Create the task branch without touching the shared `.git/config`, which is read-only for a Codex seat by design (T64 writable roots): `git switch -c <branch> --no-track origin/main`, push with `git push origin <branch>` (no `-u`), and open the PR with `gh pr create --head <branch>`. A Claude seat's sandbox can leave the same failed write behind, so it uses the same commands. A leftover `.git/config.lock` from a failed attempt is removed by the orchestrator. Remove a scratch worktree (for example one that proves a test fails on `origin/main`) with `git worktree remove <path>` only; never run `git worktree prune` from a sandboxed seat, because other worktrees' paths look missing inside the sandbox and prune then targets their admin directories in the shared `.git/worktrees`.
3. Treat `allowed_files` as the edit boundary. If it says to see the task file, read that section and follow it exactly.
4. Do not perform any `forbidden_actions`. Complete every command inside the sandbox and allowlist; never escalate an action outside that boundary for approval. Fail it instead, send `AGMSG-PONG v1 status=blocked` with the exact command and the boundary it crosses, and wait for the orchestrator to re-task. Agent-to-agent permission approval is forbidden: only the human operator answers a permission prompt. A Claude Code auto-mode classifier denial (for example Self-Modification) is such a boundary: stop without a diff, send `AGMSG-PONG v1 status=blocked` naming the classifier reason, and never pursue the same outcome through another tool. Fetch and fast-forward inside the sandbox; a public remote needs no credential. On Linux, `gh` backed by the host keyring answers HTTP 401 inside the sandbox, because AF_UNIX socket creation is denied and `allowUnixSockets` cannot grant a path. So a Claude seat runs three commands outside the sandbox through the permission gate: `gh`, `git push`, and an authenticated `git fetch` (a private HTTPS remote, whose credential helper is `gh`). Look up a VERIFY item's external reference (upstream documentation, release notes, an API schema) with the WebFetch tool, not Bash `curl`. Three documented cases run outside the sandbox too: the task's main-checkout CompactionDB `memory add`, through the permission gate because that state directory is read-only from a worktree sandbox; writing the task's artifacts at their expected main-checkout paths and masking them with the repository masker, through the permission gate because the main checkout is not writable from a worktree sandbox; and `agmsg-dispatch`, through `excludedCommands` (step 11). Every other out-of-sandbox action stays a blocked PONG. A Codex seat has in-sandbox network (T64) and never leaves its sandbox.
5. Write artifacts to the exact expected paths (a Claude seat writes them through the permission gate, step 4). Do not invent alternate paths. A seat whose sandbox cannot write the main checkout (a Codex seat) writes them at the same relative paths in its own worktree, untracked, and the RESULT says so; the orchestrator moves them into the main checkout by absolute path before review. Worker-side review evidence carries a `-worker-` infix (`<task>-worker-crit.json`, `<task>-worker-review-receipt.md`), so it never collides with the orchestrator's own files.
6. Put the verbatim output of every validation command in `expected_validation_file`; every identifier your report claims to have created must appear in that output.
7. Put the isolation status or fallback rationale in `expected_sandbox_file`.
8. Put reusable learning triage in `expected_learning_file`; do not promote rules directly unless the task explicitly allows it.

mcp: codex_apps/github.fetch_commit_workflow_runs (completed)
mcp: codex_apps/github.fetch_pr (completed)
**Managing output size**
exec
/bin/zsh -lc "nl -ba .orchestration/validation/dotfiles-T128-ci-skip-orchestration-a02.md | sed -n '1,185p'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 0ms:
     1	# Validation: dotfiles-T128-ci-skip-orchestration-a02
     2	
     3	Every block is the verbatim output of the command shown, run in `.claude/worktrees/worker-f` on `feat/ci-skip-orchestration` (PR #320). This main-checkout copy covers `a35a751e`, §7 the final head `fca44b4c`, §8 and §9 Amendment 1 and its head `a8c2bed9` (design INV-8).
     4	
     5	## 1. Task file
     6	
     7	```
     8	$ shasum -a 256 ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T128-ci-skip-orchestration-a02.md .orchestration/dotfiles-T128-ci-skip-orchestration-a02/task.md | cut -c1-64
     9	2c3a5ee2439a4c8e0aa16e0013e9b8acfcbb82fc330b259f7748f34938d5d9bc
    10	2c3a5ee2439a4c8e0aa16e0013e9b8acfcbb82fc330b259f7748f34938d5d9bc
    11	```
    12	
    13	## 2. Checks at `a35a751e` (task validation: the YAML parse, the module; plus formatting and the security pins)
    14	
    15	```
    16	$ git log --oneline -3; git show --stat --format= a35a751e
    17	a35a751e test(ci): the workflow reader fails closed on any key form it does not parse
    18	406ca746 chore(orchestration): task file for dotfiles-T128-ci-skip-orchestration-a02
    19	dc4e6c37 fix(ci): the unit-test decision lists both sides of a rename; the workflow reader sees quoted keys
    20	 tests/unit/test_workflow_orchestration_skip.py | 109 ++++++++++++++++---------
    21	 1 file changed, 70 insertions(+), 39 deletions(-)
    22	$ UV_OFFLINE=1 uv run python -m unittest tests.unit.test_workflow_orchestration_skip tests.unit.test_workflow_security 2>&1 | tail -3; ruff format --config ruff.toml --check tests/unit/test_workflow_orchestration_skip.py; ruff check --config ruff.toml tests/unit/test_workflow_orchestration_skip.py
    23	Ran 21 tests in 4.718s
    24	
    25	OK
    26	1 file already formatted
    27	All checks passed!
    28	$ UV_OFFLINE=1 uv run --no-project --with pyyaml python -I -c "import sys, yaml; [print(p, sorted(yaml.safe_load(open(p))[\"jobs\"])) for p in sys.argv[1:]]" .github/workflows/remote.yaml .github/workflows/test.yaml .github/workflows/agent-assets.yml
    29	.github/workflows/remote.yaml ['private-bootstrap', 'public-bootstrap']
    30	.github/workflows/test.yaml ['test']
    31	.github/workflows/agent-assets.yml ['validate']
    32	```
    33	
    34	## 3. The unsupported forms (`scratchpad/mutate-a5-a02.sh` at `a35a751e`, a `git archive HEAD` copy)
    35	
    36	Each row inserts one form into a workflow. "YAML reads" is GitHub's view of it, from PyYAML on the mutated file: every form hides a real `if` or `continue-on-error`. The next lines run `RequiredContextsTest`, `DecisionStepTest` and `DecisionTest` (13 tests) and count the summary and `ValueError` lines. `errors=N` counts failing subTests, not tests. The task's four forms come first; the two positional rows (a shifted job body, a shifted step item) were found while checking the reader.
    37	
    38	```
    39	== unsupported form: spaced-job-key (remote.yaml): if : false
    40	   YAML reads: False
    41	   1 FAILED (errors=12)
    42	   1 Ran 13 tests in 1.732s
    43	  12 ValueError: unsupported key form inside jobs: '    if : false'
    44	== unsupported form: escaped-job-key (remote.yaml): "\x69f": false
    45	   YAML reads: False
    46	   1 FAILED (errors=12)
    47	   1 Ran 13 tests in 2.220s
    48	  12 ValueError: unsupported key form inside jobs: '    "\\x69f": false'
    49	== unsupported form: spaced-step-key (test.yaml): continue-on-error : true
    50	   YAML reads: True
    51	   1 FAILED (errors=9)
    52	   1 Ran 13 tests in 2.040s
    53	   9 ValueError: unsupported key form inside jobs: '        continue-on-error : true'
    54	== unsupported form: shifted-job-body (agent-assets.yml): if: false|runs-on: ubuntu-24.04
    55	   YAML reads: False
    56	   1 FAILED (errors=3)
    57	   1 Ran 13 tests in 3.463s
    58	   3 ValueError: unsupported job body indentation inside jobs: '      if: false'
    59	== unsupported form: shifted-step-item (remote.yaml): -   name: Decide whether the diff needs a bootstrap|continue-on-error: true
    60	   YAML reads: True
    61	   1 FAILED (errors=12)
    62	   1 Ran 13 tests in 1.583s
    63	  12 ValueError: unsupported key form inside jobs: '      -   name: Decide whether the diff needs a bootstrap'
    64	== unsupported form: flow-mapping-step (remote.yaml): - { if: false }
    65	   YAML reads: {'if': False}
    66	   1 FAILED (errors=12)
    67	   1 Ran 13 tests in 1.550s
    68	  12 ValueError: unsupported key form inside jobs: '      - { if: false }'
    69	== reader made lenient again (plain_key returns instead of raising) -> test_the_reader_fails_closed_on_unsupported_key_forms
    70	FAIL: test_the_reader_fails_closed_on_unsupported_key_forms (tests.unit.test_workflow_orchestration_skip.RequiredContextsTest.test_the_reader_fails_closed_on_unsupported_key_forms) (form='spaced job key')
    71	AssertionError: ValueError not raised
    72	FAIL: test_the_reader_fails_closed_on_unsupported_key_forms (tests.unit.test_workflow_orchestration_skip.RequiredContextsTest.test_the_reader_fails_closed_on_unsupported_key_forms) (form='escaped job key')
    73	== restored: OK
    74	== reader without the job-body indentation check -> test_the_reader_fails_closed_on_unsupported_key_forms
    75	FAIL: test_the_reader_fails_closed_on_unsupported_key_forms (tests.unit.test_workflow_orchestration_skip.RequiredContextsTest.test_the_reader_fails_closed_on_unsupported_key_forms) (form='shifted job body')
    76	AssertionError: ValueError not raised
    77	FAILED (failures=1)
    78	```
    79	
    80	The tests that still pass under each form (the same harness with `-v`). Each is either the reader test itself (it rebuilds its own forms), or a test that never reads the mutated job's keys through `jobs()`: the context-name check reads job names by regex, and the rest read the other workflow file.
    81	
    82	```
    83	== unsupported form: spaced-job-key (remote.yaml): if : false
    84	test_the_reader_fails_closed_on_unsupported_key_forms ... ok
    85	test_the_required_contexts_are_the_workflows_jobs ... ok
    86	test_a_main_tests_job_when_present_decides_in_itself ... ok
    87	test_the_unit_test_decision_ignores_renames ... ok
    88	test_the_unit_test_decision_skips_an_orchestration_only_diff ... ok
    89	== unsupported form: escaped-job-key (remote.yaml): "\x69f": false
    90	test_the_reader_fails_closed_on_unsupported_key_forms ... ok
    91	test_the_required_contexts_are_the_workflows_jobs ... ok
    92	test_a_main_tests_job_when_present_decides_in_itself ... ok
    93	test_the_unit_test_decision_ignores_renames ... ok
    94	test_the_unit_test_decision_skips_an_orchestration_only_diff ... ok
    95	== unsupported form: spaced-step-key (test.yaml): continue-on-error : true
    96	test_the_reader_fails_closed_on_unsupported_key_forms ... ok
    97	test_the_required_contexts_are_the_workflows_jobs ... ok
    98	test_both_bootstrap_jobs_decide_with_the_same_script ... ok
    99	test_a_pull_request_skips_the_bootstrap_only_for_an_orchestration_only_diff ... ok
   100	test_every_event_but_pull_request_bootstraps ... ok
   101	== unsupported form: shifted-job-body (agent-assets.yml): if: false|runs-on: ubuntu-24.04
   102	test_no_job_is_left_for_a_required_job_to_need ... ok
   103	test_the_reader_fails_closed_on_unsupported_key_forms ... ok
   104	test_a_main_tests_job_when_present_decides_in_itself ... ok
   105	test_both_bootstrap_jobs_decide_with_the_same_script ... ok
   106	test_each_deciding_job_decides_after_its_checkout_and_fails_closed ... ok
   107	test_every_heavy_step_carries_its_jobs_decision ... ok
   108	test_a_pull_request_skips_the_bootstrap_only_for_an_orchestration_only_diff ... ok
   109	test_every_event_but_pull_request_bootstraps ... ok
   110	test_the_decision_survives_a_base_that_moved_after_the_checkout ... ok
   111	test_the_unit_test_decision_ignores_renames ... ok
   112	test_the_unit_test_decision_skips_an_orchestration_only_diff ... ok
   113	== unsupported form: shifted-step-item (remote.yaml): -   name: Decide whether the diff needs a bootstrap|continue-on-error: true
   114	test_the_reader_fails_closed_on_unsupported_key_forms ... ok
   115	test_the_required_contexts_are_the_workflows_jobs ... ok
   116	test_a_main_tests_job_when_present_decides_in_itself ... ok
   117	test_the_unit_test_decision_ignores_renames ... ok
   118	test_the_unit_test_decision_skips_an_orchestration_only_diff ... ok
   119	== unsupported form: flow-mapping-step (remote.yaml): - { if: false }
   120	test_the_reader_fails_closed_on_unsupported_key_forms ... ok
   121	test_the_required_contexts_are_the_workflows_jobs ... ok
   122	test_a_main_tests_job_when_present_decides_in_itself ... ok
   123	test_the_unit_test_decision_ignores_renames ... ok
   124	test_the_unit_test_decision_skips_an_orchestration_only_diff ... ok
   125	== restored: OK
   126	```
   127	
   128	## 4. The earlier proofs against the new reader (`scratchpad/mutate-a5.sh` and `scratchpad/mutate-a5-r1.sh` at `a35a751e`)
   129	
   130	```
   131	$ awk '/^== broken rule/{if(n!="")print n, f; n=$4; f="no"} /^(FAIL|ERROR):/{f="fails"} END{print n, f}' mutate-a5.log mutate-a5-r1.log; grep -E 'DID NOT APPLY|restored' mutate-a5.log mutate-a5-r1.log
   132	public-bootstrap-step-ungated fails
   133	private-deploy-key-ungated fails
   134	unit-test-step-ungated fails
   135	needs-on-a-required-job fails
   136	job-level-if-on-a-required-job fails
   137	changes-job-back fails
   138	decision-continue-on-error fails
   139	decision-before-checkout-history fails
   140	private-script-drift fails
   141	non-pr-events-judged fails
   142	renames-collapsed fails
   143	classification-inverted fails
   144	unit-test-decision-ignores-orchestration fails
   145	required-leg-dropped fails
   146	shallow-base-fetch-remote fails
   147	shallow-base-fetch-test fails
   148	unit-test-diff-detects-renames fails
   149	quoted-job-level-if fails
   150	quoted-continue-on-error-on-decide fails
   151	== reader-sees-bare-keys-only: MUTATION DID NOT APPLY
   152	== restored: OK
   153	== restored: OK
   154	```
   155	
   156	`reader-sees-bare-keys-only` targeted the quoted-key regex that this commit removes; the lenient-reader row of §3 replaces it.
   157	
   158	## 5. The full suite locally, this head against `origin/main` (`git archive origin/main` copy; failing ids from the `FAIL:`/`ERROR:` lines)
   159	
   160	```
   161	$ UV_OFFLINE=1 make unit-test   # at this head; the same discover in the origin/main copy; then comm on the sorted ids
   162	base (origin/main b896d9bc): FAILED (failures=114, errors=103, skipped=2)  failing ids: 188
   163	head (a35a751e, make unit-test): FAILED (failures=114, errors=103, skipped=2) (make exits 2)  failing ids: 188
   164	only at head:
   165	only at base:
   166	this module under make unit-test:
   167	test_a_main_tests_job_when_present_decides_in_itself ... ok
   168	test_both_bootstrap_jobs_decide_with_the_same_script ... ok
   169	test_each_deciding_job_decides_after_its_checkout_and_fails_closed ... ok
   170	test_every_heavy_step_carries_its_jobs_decision ... ok
   171	test_a_pull_request_skips_the_bootstrap_only_for_an_orchestration_only_diff ... ok
   172	test_every_event_but_pull_request_bootstraps ... ok
   173	test_the_decision_survives_a_base_that_moved_after_the_checkout ... ok
   174	test_the_unit_test_decision_ignores_renames ... ok
   175	test_the_unit_test_decision_skips_an_orchestration_only_diff ... ok
   176	test_no_job_is_left_for_a_required_job_to_need ... ok
   177	test_no_required_contexts_job_has_a_job_level_if_or_needs ... ok
   178	test_the_reader_fails_closed_on_unsupported_key_forms ... ok
   179	test_the_required_contexts_are_the_workflows_jobs ... ok
   180	```
   181	
   182	The local failures are the sandbox's, as on a01 (test commits that inherit the global signing setting, `mktemp` outside the writable paths, no pty devices, no local `main` ref). They are identical on `origin/main`. CI's `Run Python unit tests` step is the verdict.
   183	
   184	## 6. CompactionDB (main checkout, outside the sandbox through the permission gate)
   185	

**Optimizing execution method**
exec
/bin/zsh -lc "python3 -B -c 'import json, pathlib, hashlib, subprocess, importlib.util
p=pathlib.Path(\".orchestration/validation/dotfiles-T128-ci-skip-orchestration-a02-pr-feedback.json\")
d=json.loads(p.read_text())
print(json.dumps(d,indent=2))
for module in (\"yaml\",\"pytest\"):
 print(\"module\",module,importlib.util.find_spec(module))
root=pathlib.Path(\".ua\")
if root.joinpath(\"meta.json\").exists():
 meta=json.loads(root.joinpath(\"meta.json\").read_text());print(\"UA meta\",meta)
 g=json.loads(root.joinpath(\"knowledge-graph.json\").read_text())
 print(\"UA nodes\",[(n.get(\"filePath\"),n.get(\"summary\")) for n in g.get(\"nodes\",[]) if any(t in n.get(\"filePath\",\"\") for t in (\"workflow\",\"pr-feedback\",\"require-crit\"))][:30])
base=\"3c845c55dc43b668fa6df8434cb47a1b1f00d695\";head=\"3bafe4f24c80fd1093e2fd5a19d843e5cb7aff5b\"
for ref,p in [(base,\".orchestration/tasks/dotfiles-T128-regime-v3-a01.md\"),(head,\".orchestration/dotfiles-T128-ci-skip-orchestration-a02/task.md\")]:
 b=subprocess.check_output([\"git\",\"show\",ref+\":\"+p]);print(\"HASH\",ref,p,hashlib.sha256(b).hexdigest())
'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 114ms:
{
  "repo": "mryfmo/dotfiles",
  "pr": 320,
  "head_sha": "3bafe4f24c80fd1093e2fd5a19d843e5cb7aff5b",
  "base_ref": "main",
  "base_sha": "3c845c55dc43b668fa6df8434cb47a1b1f00d695",
  "generated_at": "2026-10-11T10:05:02+00:00",
  "checks": [
    {
      "name": "GitGuardian Security Checks",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/runs/114442344011"
    },
    {
      "name": "private-bootstrap (ubuntu-24.04, server)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38130057799/job/114442342458"
    },
    {
      "name": "public-bootstrap (ubuntu-24.04, server)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38130057799/job/114442342452"
    },
    {
      "name": "validate",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38130057840/job/114442342439"
    },
    {
      "name": "private-bootstrap (macos-14, client)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38130057799/job/114442342418"
    },
    {
      "name": "public-bootstrap (macos-14, client)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38130057799/job/114442342413"
    },
    {
      "name": "private-bootstrap (ubuntu-24.04, client)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38130057799/job/114442342395"
    },
    {
      "name": "test (ubuntu-24.04, client)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38130057786/job/114442342318"
    },
    {
      "name": "test (ubuntu-26.04, client)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38130057786/job/114442342302"
    },
    {
      "name": "test (macos-14, client)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38130057786/job/114442342288"
    },
    {
      "name": "public-bootstrap (ubuntu-24.04, client)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38130057799/job/114442342274"
    },
    {
      "name": "test (ubuntu-24.04, server)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38130057786/job/114442342186"
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
      "body": "<!-- This is an auto-generated comment: summarize by coderabbit.ai -->\n<!-- This is an auto-generated comment: skip review by coderabbit.ai -->\n\n> [!IMPORTANT]\n> ## Review skipped\n> \n> Auto reviews are disabled on this repository. Please check the settings in the CodeRabbit UI or the `.coderabbit.yaml` file in this repository. To trigger a single review, invoke the `@coderabbitai review` command.\n> \n> <details>\n> <summary><strong>\u2699\ufe0f Run configuration</strong></summary>\n> <dl>\n> <dd>\n> \n> - **Configuration used**: Repository: mryfmo/dotfiles/.coderabbit.yaml\n> - **Review profile**: CHILL\n> - **Plan**: Advanced\n> - **Run ID**: `4142dffa-96b9-4347-b1d8-ddfc30b94b69`\n> \n> \n> <hr>\n> \n> </dd>\n> </dl>\n> </details>\n> \n> You can disable this status message by setting the `reviews.review_status` to `false` in the CodeRabbit configuration file.\n> \n> Use the checkbox below for a quick retry:\n> - [ ] <!-- {\"checkboxId\":\"e9bb8d72-00e8-4f67-9cb2-caf3b22574fe\"} --> \ud83d\udd0d Trigger review\n\n<!-- end of auto-generated comment: skip review by coderabbit.ai -->\n\n<!-- autopilot:start -->\n- [ ] <!-- {\"checkboxId\":\"2708ad07-9f24-4260-9c11-7dc76a49f2e3\"} --> <strong title=\"Keep fixing CodeRabbit findings and required CI, and resolving merge conflicts\">Autofix</strong> \u00b7 Keep fixing CodeRabbit findings and required CI, and resolving merge conflicts\n<!-- autopilot:end -->\n<!-- tips_start -->\n\n---\n\nThanks for using [CodeRabbit](https://coderabbit.ai?utm_source=oss&utm_medium=github&utm_campaign=mryfmo/dotfiles&utm_content=320)! It's free for OSS, and your support helps us grow. If you like it, consider giving us a shout-out.\n\n<details>\n<summary><strong>\u2764\ufe0f Share</strong></summary>\n<dl>\n<dd>\n\n- [X](https://twitter.com/intent/tweet?text=I%20just%20used%20%40coderabbitai%20for%20my%20code%20review%2C%20and%20it%27s%20fantastic%21%20It%27s%20free%20for%20OSS%20and%20offers%20a%20free%20trial%20for%20the%20proprietary%20code.%20Check%20it%20out%3A&url=https%3A//coderabbit.ai)\n- [Mastodon](https://mastodon.social/share?text=I%20just%20used%20%40coderabbitai%20for%20my%20code%20review%2C%20and%20it%27s%20fantastic%21%20It%27s%20free%20for%20OSS%20and%20offers%20a%20free%20trial%20for%20the%20proprietary%20code.%20Check%20it%20out%3A%20https%3A%2F%2Fcoderabbit.ai)\n- [Reddit](https://www.reddit.com/submit?title=Great%20tool%20for%20code%20review%20-%20CodeRabbit&text=I%20just%20used%20CodeRabbit%20for%20my%20code%20review%2C%20and%20it%27s%20fantastic%21%20It%27s%20free%20for%20OSS%20and%20offers%20a%20free%20trial%20for%20proprietary%20code.%20Check%20it%20out%3A%20https%3A//coderabbit.ai)\n- [LinkedIn](https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Fcoderabbit.ai&mini=true&title=Great%20tool%20for%20code%20review%20-%20CodeRabbit&summary=I%20just%20used%20CodeRabbit%20for%20my%20code%20review%2C%20and%20it%27s%20fantastic%21%20It%27s%20free%20for%20OSS%20and%20offers%20a%20free%20trial%20for%20proprietary%20code)\n\n<hr>\n\n</dd>\n</dl>\n</details>\n\n\n<sub>Comment `@coderabbitai help` to get the list of available commands.</sub>\n\n<!-- tips_end -->",
      "url": "https://github.com/mryfmo/dotfiles/pull/320#issuecomment-6105933748",
      "disposition": "not-applicable:CodeRabbit auto-generated summary and skip notice, no finding"
    },
    {
      "source": "issue_comment",
      "author": "chatgpt-codex-connector[bot]",
      "bot": true,
      "level": "comment",
      "path": null,
      "line": null,
      "body": "<!-- codex-pull-request-review-summary -->\n<!-- codex-security-review:v1 {\"blockingSeverityThreshold\":\"P0\",\"headSha\":\"9fcd2b0482bd9c3c27e39b687e3503271f49a154\",\"mergeGateEnabled\":false,\"pullRequestNumber\":320,\"repository\":\"mryfmo/dotfiles\",\"status\":\"completed\"} -->\n## Codex Review Summary\n\nThis comment shows the latest Codex review activity on this pull request.\n\n| Review | Status | Commit | Review trigger |\n| --- | --- | --- | --- |\n| \ud83d\udcdd **Code Review** | \u2705 **Completed** <relative-time datetime=\"2026-10-11T09:56:14.290900Z\">2026-10-11T09:56:14.290900Z</relative-time> | `3bafe4f` | New commits |\n| \ud83d\udd12 **Security Review** | \u2705 **Completed** <relative-time datetime=\"2026-10-11T05:55:43.193970Z\">2026-10-11T05:55:43.193970Z</relative-time> | `9fcd2b0` | Draft marked ready |\n\n\n\n<details> <summary>\u2139\ufe0f About Codex in GitHub</summary>\n<br/>\n\n[Your team has set up Codex to review pull requests in this repo](https://chatgpt.com/codex/cloud/settings/general). Reviews are triggered when you\n- Open a pull request for review\n- Mark a draft as ready\n- Comment \"@codex review\" or \"@codex security review\".\n\nCodex reacts with \ud83d\udc40 while any review is running, comments if it has suggestions, and reacts with \ud83d\udc4d once all reviews finish with no findings.\n\n</details>",
      "url": "https://github.com/mryfmo/dotfiles/pull/320#issuecomment-6105983720",
      "disposition": "not-applicable:Codex review summary comment with no finding of its own"
    },
    {
      "source": "review",
      "author": "chatgpt-codex-connector[bot]",
      "bot": true,
      "level": "commented",
      "path": null,
      "line": null,
      "body": "\n### \ud83d\udca1 Codex Review\n\nHere are some automated review suggestions for this pull request.\n\n**Reviewed commit:** `b3f88beb03`\n    \n\n<details> <summary>\u2139\ufe0f About Codex in GitHub</summary>\n<br/>\n\nCodex has been enabled to automatically review pull requests in this repo. Reviews are triggered when you\n- Open a pull request for review\n- Mark a draft as ready\n- Comment \"@codex review\".\n\nIf Codex has suggestions, it will comment; otherwise it will react with \ud83d\udc4d.\n\n\n\n\nWhen you [sign up for Codex through ChatGPT](https://openai.com/codex), Codex can also answer questions or update the PR, like \"@codex address that feedback\".\n            \n</details>",
      "url": "https://github.com/mryfmo/dotfiles/pull/320#pullrequestreview-5482144676",
      "commit": "b3f88beb0390af9fcc9701b4fbb8f04590cf7c01",
      "disposition": "not-applicable:Codex review container whose body carries no P0-P3 badge; its one inline thread (a01) has its own fixed:<sha> disposition and a reply on GitHub"
    },
    {
      "source": "review",
      "author": "moriya-fumio-thd",
      "bot": false,
      "level": "commented",
      "path": null,
      "line": null,
      "body": "",
      "url": "https://github.com/mryfmo/dotfiles/pull/320#pullrequestreview-5482187594",
      "commit": "d6343494f08b14e5d33be01ed24029baef34d206",
      "disposition": "not-applicable:the review object GitHub created for the orchestrator's reply, empty body, not a finding"
    },
    {
      "source": "review_comment",
      "author": "chatgpt-codex-connector[bot]",
      "bot": true,
      "level": "comment",
      "path": ".github/workflows/remote.yaml",
      "line": 61,
      "body": "**<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Preserve history when refreshing the PR base**\n\nWhen `main` advances after GitHub creates the pull-request merge SHA but before this job runs, `git fetch --depth=1` marks the new `origin/${BASE_REF}` tip as a shallow boundary, undoing the preceding full-history checkout. The subsequent three-dot diff then fails with `fatal: ... no merge base`, so all three required public-bootstrap contexts fail instead of classifying the PR; the identical fetch in `private-bootstrap` has the same problem. This is reproducible in a full clone by advancing the base and fetching it with this command, and `git fetch -h` describes `--depth` as changing shallow history. Fetch without the depth limit, or diff against the event's fixed base SHA.\n\nUseful? React with \ud83d\udc4d\u00a0/ \ud83d\udc4e.",
      "url": "https://github.com/mryfmo/dotfiles/pull/320#discussion_r4240499289",
      "resolved": true,
      "outdated": true,
      "disposition": "fixed:e872f69f"
    },
    {
      "source": "review_comment",
      "author": "moriya-fumio-thd",
      "bot": false,
      "level": "comment",
      "path": ".github/workflows/remote.yaml",
      "line": 61,
      "body": "Disposition (orchestrator, final head d6343494): `fixed:e872f69f` \u2014 every fetch keeps full history (no `--depth=1` on the base refresh), so the three-dot diff always has a merge-base; reproduced (rc 128) and covered by the new test that moves origin/main after the head.",
      "url": "https://github.com/mryfmo/dotfiles/pull/320#discussion_r4240542203",
      "resolved": true,
      "outdated": true,
      "disposition": "not-applicable:the orchestrator's own disposition reply on the resolved thread, not a finding"
    },
    {
      "source": "annotation",
      "author": "github-actions",
      "bot": true,
      "level": "notice",
      "path": ".github",
      "line": 1,
      "body": "Due to capacity constraints, jobs targeting macOS arm64 runners may experience longer queue times.",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38130057799/job/114442342418",
      "check": "private-bootstrap (macos-14, client)",
      "disposition": "not-applicable:GitHub notice about macOS arm64 runner queue times, no code impact"
    },
    {
      "source": "annotation",
      "author": "github-actions",
      "bot": true,
      "level": "notice",
      "path": ".github",
      "line": 1,
      "body": "Due to capacity constraints, jobs targeting macOS arm64 runners may experience longer queue times.",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38130057799/job/114442342413",
      "check": "public-bootstrap (macos-14, client)",
      "disposition": "not-applicable:GitHub notice about macOS arm64 runner queue times, no code impact"
    },
    {
      "source": "annotation",
      "author": "github-actions",
      "bot": true,
      "level": "notice",
      "path": ".github",
      "line": 1,
      "body": "Due to capacity constraints, jobs targeting macOS arm64 runners may experience longer queue times.",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38130057786/job/114442342288",
      "check": "test (macos-14, client)",
      "disposition": "not-applicable:GitHub notice about macOS arm64 runner queue times, no code impact"
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
      "disposition": "not-applicable:CodeRabbit success status (review skipped by repository configuration)"
    }
  ]
}
module yaml None
module pytest None
UA meta {'lastAnalyzedAt': '2026-10-02T14:12:51Z', 'gitCommitHash': '940a3a2b07adfd14140a0acff96784ef53a0a509', 'version': '1.0.0', 'analyzedFiles': 368}
UA nodes [('.github/workflows/agent-assets.yml', 'GitHub Actions workflow that validates agent, MCP, plugin and skill assets with validate-agent-assets.py and parses .coderabbit.yaml on PRs/pushes to main, plus a weekly scheduled check of upstream Codex/Claude documentation links and npm package versions.'), ('.github/workflows/docs.yml', 'GitHub Actions workflow that, on pushes to main touching docs-relevant paths, installs uv and mise tools and runs `make deploy` to build and publish the MkDocs reference site to GitHub Pages.'), ('.github/workflows/macos.yaml', 'macOS (M1) CI workflow that bootstraps the dotfiles via setup.sh with private dotfiles secrets, verifies a rerun refuses local drift, runs and publishes a shell startup benchmark, and checks deployed files with bats.'), ('.github/workflows/remote.yaml', 'Weekly and PR workflow that exercises the remote setup.sh bootstrap against the checked-out commit in an isolated HOME across Ubuntu client/server and macOS client matrices, asserting unmanaged sentinel files keep their content and modes, with an optional private-dotfiles bootstrap job.'), ('.github/workflows/test.yaml', 'Required unit-test workflow: a change-detection job gates a macOS/Ubuntu matrix that installs tools, smoke-tests statusline tools offline, runs shfmt/ShellCheck, Python unittests (make unit-test) and bats unit tests with bashcov coverage uploaded to Codecov, plus a Nix job evaluating flake home-manager and nix-darwin outputs.'), ('.github/workflows/ubuntu.yaml', 'Ubuntu CI workflow that bootstraps the dotfiles via setup.sh for client and server systems, verifies a rerun rejects local drift, and validates deployed files with tag-filtered bats suites.'), ('home/dot_agents/plugins/mryfmo-dev-workflows/.codex-plugin/plugin.json', 'Codex plugin manifest for mryfmo-dev-workflows that exposes the shared ~/.agents/skills tree as reusable personal workflows (GitHub, shell docs, uv, Japanese writing, transformers, review).'), ('home/dot_agents/skills/gh-first-workflow/SKILL.md', 'Agent skill enforcing gh-first GitHub issue/PR investigation, keeping PR descriptions in sync with the full PR, the pr-feedback.py disposition gate before merge, and Conventional Commit output.'), ('home/dot_agents/skills/gh-first-workflow/references/gh-git-rules.md', 'Reference for the gh-first skill listing typical gh commands, the web-fallback pattern, and Conventional Commit type guidance.'), ('home/dot_agents/skills/gh-first-workflow/agents/openai.yaml', 'Codex interface metadata (display name, short description, default prompt) for the gh-first-workflow skill.'), ('home/dot_agents/skills/python-uv-workflow/SKILL.md', 'Agent skill defining the uv-first Python workflow: uv run, test-first behavior changes, dev dependencies, pre-commit hooks, Makefile setup target, and refactoring parity expectations.'), ('home/dot_agents/skills/python-uv-workflow/references/python-uv-rules.md', 'Reference with exact uv commands, dev dependency list, the canonical .pre-commit-config.yaml template, Makefile setup target, and refactoring-from-original guidance.'), ('home/dot_agents/skills/python-uv-workflow/agents/openai.yaml', 'Codex interface metadata (display name, short description, default prompt) for the python-uv-workflow skill.'), ('home/dot_claude/skills/gh-first-workflow/agents/symlink_openai.yaml.tmpl', 'Chezmoi symlink template that exposes the shared gh-first-workflow Codex/OpenAI agent metadata (agents/openai.yaml) from dot_agents/skills to ~/.claude/skills/gh-first-workflow/agents/openai.yaml, keeping one canonical copy for Claude Code and Codex.'), ('home/dot_claude/skills/gh-first-workflow/references/symlink_gh-git-rules.md.tmpl', 'Chezmoi symlink template that exposes the shared gh-first-workflow reference document (references/gh-git-rules.md) from dot_agents/skills to ~/.claude/skills/gh-first-workflow/references/gh-git-rules.md, keeping one canonical copy for Claude Code and Codex.'), ('home/dot_claude/skills/gh-first-workflow/symlink_SKILL.md.tmpl', 'Chezmoi symlink template that exposes the shared gh-first-workflow skill definition (SKILL.md) from dot_agents/skills to ~/.claude/skills/gh-first-workflow/SKILL.md, keeping one canonical copy for Claude Code and Codex.'), ('home/dot_claude/skills/python-uv-workflow/agents/symlink_openai.yaml.tmpl', 'Chezmoi symlink template that exposes the shared python-uv-workflow Codex/OpenAI agent metadata (agents/openai.yaml) from dot_agents/skills to ~/.claude/skills/python-uv-workflow/agents/openai.yaml, keeping one canonical copy for Claude Code and Codex.'), ('home/dot_claude/skills/python-uv-workflow/references/symlink_python-uv-rules.md.tmpl', 'Chezmoi symlink template that exposes the shared python-uv-workflow reference document (references/python-uv-rules.md) from dot_agents/skills to ~/.claude/skills/python-uv-workflow/references/python-uv-rules.md, keeping one canonical copy for Claude Code and Codex.'), ('home/dot_claude/skills/python-uv-workflow/symlink_SKILL.md.tmpl', 'Chezmoi symlink template that exposes the shared python-uv-workflow skill definition (SKILL.md) from dot_agents/skills to ~/.claude/skills/python-uv-workflow/SKILL.md, keeping one canonical copy for Claude Code and Codex.'), ('scripts/pr-feedback.py', 'Collector that gathers every piece of GitHub feedback on a PR head (issue comments, reviews, inline comments with thread state, non-passing checks, annotations, commit statuses) into one JSON document with empty dispositions for the PR integration gate.'), ('scripts/pr-feedback.py', 'Exits with guidance when `gh auth status` reports the GitHub CLI is not authenticated.'), ('scripts/pr-feedback.py', 'Builds one normalized feedback item (source, actor, bot flag, level, body, url, path/line, thread state) with an empty disposition.'), ('scripts/pr-feedback.py', 'Queries review threads over GraphQL and maps each review comment id to its resolved and outdated state.'), ('scripts/pr-feedback.py', 'Fetches all PR feedback sources for the head commit via REST/GraphQL and assembles the item list with repo, PR, head and base metadata.'), ('scripts/pr-feedback.py', 'CLI entry that resolves the repo, requires gh auth, collects feedback, and writes JSON to stdout or a file.'), ('scripts/require-crit-review.py', "Integration guard that requires native agent or Crit review evidence for meaningful diffs and, for PR integration, re-collects GitHub feedback from the authenticated base's pr-feedback.py and requires a root-cause disposition for every item."), ('scripts/require-crit-review.py', 'Skips worklogs and the PR feedback evidence file itself when sizing a diff.'), ('scripts/require-crit-review.py', 'Rejects PR feedback evidence outside .orchestration/validation/ or without the -pr-feedback.json suffix.'), ('scripts/require-crit-review.py', 'Lists unstaged, staged, untracked, and optionally base...HEAD changed paths, excluding ignored files.'), ('scripts/require-crit-review.py', 'Sums added and removed line counts across working, staged, and base...HEAD diffs via git numstat.')]
HASH 3c845c55dc43b668fa6df8434cb47a1b1f00d695 .orchestration/tasks/dotfiles-T128-regime-v3-a01.md 4520b8f0ac5663a0879acd4eb0fe5a5bc585bdca6c53aac6dae1d5de94bf07a8
HASH 3bafe4f24c80fd1093e2fd5a19d843e5cb7aff5b .orchestration/dotfiles-T128-ci-skip-orchestration-a02/task.md 4de54fdec5db667e940365703ee5e16cd1d91f52794c79c75b48aad7eb0a8763

mcp: codex_apps/github.fetch_workflow_run_jobs started
mcp: codex_apps/github.fetch_workflow_run_jobs started
mcp: codex_apps/github.fetch_workflow_run_jobs started
mcp: codex_apps/github.fetch_workflow_run_jobs (completed)
mcp: codex_apps/github.fetch_workflow_run_jobs (completed)
mcp: codex_apps/github.fetch_workflow_run_jobs (completed)
**Analyzing YAML job parsing issues**
**Examining job-level continue-on-error behavior**
exec
/bin/zsh -lc "python3 -B -c 'import subprocess,pathlib,types,unittest,io
from unittest.mock import patch
head=\"3bafe4f24c80fd1093e2fd5a19d843e5cb7aff5b\"
def show(p): return subprocess.check_output([\"git\",\"show\",head+\":\"+p],text=True)
p=\"tests/unit/test_workflow_orchestration_skip.py\"
m=types.ModuleType(\"audit_target\");m.__file__=str(pathlib.Path(p).resolve());exec(compile(show(p),p,\"exec\"),m.__dict__)
texts={str(pathlib.Path(p).resolve()):show(p) for p in [\".github/workflows/remote.yaml\",\".github/workflows/test.yaml\",\".github/workflows/agent-assets.yml\"]}
def read(self,*a,**k): return texts[str(self.resolve())]
suite=unittest.TestSuite()
for c in (m.RequiredContextsTest,m.DecisionStepTest):
 for name in unittest.defaultTestLoader.getTestCaseNames(c):
  if name"'!="test_the_reader_fails_closed_on_unsupported_key_forms":suite.addTest(c(name))
with patch.object(pathlib.Path,"read_text",read):unittest.TextTestRunner(verbosity=2).run(suite)
base=show(".orchestration/dotfiles-T128-ci-skip-orchestration-a02/task.md")
local=pathlib.Path(".orchestration/tasks/dotfiles-T128-ci-skip-orchestration-a02.md").read_text()
print("task copy equals local:",base==local)
print("UA freshness changed paths outside metadata:",sum(not p.startswith((".ua/",".orchestration/")) for p in subprocess.check_output(["git","diff","--name-only","940a3a2b07adfd14140a0acff96784ef53a0a509..HEAD"],text=True).splitlines()))
'"'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 606ms:
test_no_job_is_left_for_a_required_job_to_need (audit_target.RequiredContextsTest.test_no_job_is_left_for_a_required_job_to_need) ... ok
test_no_required_contexts_job_has_a_job_level_if_or_needs (audit_target.RequiredContextsTest.test_no_required_contexts_job_has_a_job_level_if_or_needs) ... ok
test_the_required_contexts_are_the_workflows_jobs (audit_target.RequiredContextsTest.test_the_required_contexts_are_the_workflows_jobs) ... ok
test_a_main_tests_job_when_present_decides_in_itself (audit_target.DecisionStepTest.test_a_main_tests_job_when_present_decides_in_itself) ... ok
test_both_bootstrap_jobs_decide_with_the_same_script (audit_target.DecisionStepTest.test_both_bootstrap_jobs_decide_with_the_same_script) ... ok
test_each_deciding_job_decides_after_its_checkout_and_fails_closed (audit_target.DecisionStepTest.test_each_deciding_job_decides_after_its_checkout_and_fails_closed) ... ok
test_every_heavy_step_carries_its_jobs_decision (audit_target.DecisionStepTest.test_every_heavy_step_carries_its_jobs_decision) ... ok

----------------------------------------------------------------------
Ran 7 tests in 0.002s

OK
task copy equals local: True
UA freshness changed paths outside metadata: 408

exec
/bin/zsh -lc "nl -ba .orchestration/validation/dotfiles-T128-ci-skip-orchestration-a02.md | sed -n '184,290p'; git show 3bafe4f24c80fd1093e2fd5a19d843e5cb7aff5b:.github/workflows/remote.yaml | nl -ba; git show 3bafe4f24c80fd1093e2fd5a19d843e5cb7aff5b:.github/workflows/test.yaml | nl -ba | sed -n '1,125p'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 45ms:
   184	## 6. CompactionDB (main checkout, outside the sandbox through the permission gate)
   185	
   186	```
   187	$ cd ~/Workspace/dotfiles && uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content '[memory:decision] dotfiles-T128-ci-skip-orchestration-a02 …'
   188	c62781a9-a65b-4484-925c-383fddb9a114
   189	```
   190	
   191	## 7. Final head `fca44b4c` (main-checkout copy)
   192	
   193	```
   194	$ gh pr checks 320 --repo mryfmo/dotfiles --watch --interval 30   # final table; exit 0
   195	CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
   196	GitGuardian Security Checks	pass	0	https://dashboard.gitguardian.com	
   197	private-bootstrap (macos-14, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/38122927319/job/114421200472	
   198	private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/38122927319/job/114421200388	
   199	private-bootstrap (ubuntu-24.04, server)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/38122927319/job/114421200263	
   200	public-bootstrap (macos-14, client)	pass	6m51s	https://github.com/mryfmo/dotfiles/actions/runs/38122927319/job/114421200408	
   201	public-bootstrap (ubuntu-24.04, client)	pass	9m57s	https://github.com/mryfmo/dotfiles/actions/runs/38122927319/job/114421200432	
   202	public-bootstrap (ubuntu-24.04, server)	pass	6m46s	https://github.com/mryfmo/dotfiles/actions/runs/38122927319/job/114421200378	
   203	test (macos-14, client)	pass	5m52s	https://github.com/mryfmo/dotfiles/actions/runs/38122927273/job/114421199766	
   204	test (ubuntu-24.04, client)	pass	8m0s	https://github.com/mryfmo/dotfiles/actions/runs/38122927273/job/114421199949	
   205	test (ubuntu-24.04, server)	pass	5m8s	https://github.com/mryfmo/dotfiles/actions/runs/38122927273/job/114421199892	
   206	test (ubuntu-26.04, client)	pass	8m22s	https://github.com/mryfmo/dotfiles/actions/runs/38122927273/job/114421199888	
   207	validate	pass	51s	https://github.com/mryfmo/dotfiles/actions/runs/38122927329/job/114421200195	
   208	$ bash scratchpad/bot-wait.sh 320 fca44b4c25d4b20d0b029dc5d8dd16f9c37a7dbf 2026-10-11T07:53:53Z   # last poll
   209	poll 5 07:56:08Z head fca44b4c25d4b20d0b029dc5d8dd16f9c37a7dbf asked=no
   210	reviews: 
   211	comments: 
   212	code-review-completed: | 📝 **Code Review** | ✅ **Completed** <relative-time datetime="2026-10-11T07:56:00.911325Z">2026-10-11T07:56:00.911325Z</relative-time> | `fca44b4` | New commits |
   213	DONE
   214	$ # final recheck right before the RESULT
   215	2026-10-11T08:04:16Z
   216	$ gh pr view 320 --json headRefOid,state,isDraft
   217	fca44b4c25d4b20d0b029dc5d8dd16f9c37a7dbf	OPEN	false
   218	$ gh api --paginate repos/mryfmo/dotfiles/pulls/320/reviews --jq '.[]|select(.user.type=="Bot")|[.id,.commit_id[0:8],.submitted_at]|@tsv'
   219	5482144676	b3f88beb	2026-10-11T06:15:10Z
   220	$ gh api --paginate repos/mryfmo/dotfiles/pulls/320/comments --jq '.[]|select(.in_reply_to_id == null and .user.type=="Bot")|[.id,.original_commit_id[0:8],.path,(.original_line|tostring)]|@tsv'
   221	4240499289	b3f88beb	.github/workflows/remote.yaml	61
   222	$ gh api repos/mryfmo/dotfiles/issues/comments/6105983720 --jq .body | grep -E 'Code Review|Security Review'
   223	| 📝 **Code Review** | ✅ **Completed** <relative-time datetime="2026-10-11T07:56:00.911325Z">2026-10-11T07:56:00.911325Z</relative-time> | `fca44b4` | New commits |
   224	| 🔒 **Security Review** | ✅ **Completed** <relative-time datetime="2026-10-11T05:55:43.193970Z">2026-10-11T05:55:43.193970Z</relative-time> | `9fcd2b0` | Draft marked ready |
   225	$ gh api repos/mryfmo/dotfiles/issues/320/reactions --jq '.[]|[.user.login,.content,.created_at]|@tsv'
   226	chatgpt-codex-connector[bot]	+1	2026-10-11T07:56:03Z
   227	```
   228	## 8. Amendment 1: the task copy
   229	
   230	```
   231	$ shasum -a 256 ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T128-ci-skip-orchestration-a02.md .orchestration/dotfiles-T128-ci-skip-orchestration-a02/task.md | cut -c1-64
   232	4de54fdec5db667e940365703ee5e16cd1d91f52794c79c75b48aad7eb0a8763
   233	4de54fdec5db667e940365703ee5e16cd1d91f52794c79c75b48aad7eb0a8763
   234	$ git diff --stat HEAD -- .orchestration/dotfiles-T128-ci-skip-orchestration-a02/task.md
   235	 .orchestration/dotfiles-T128-ci-skip-orchestration-a02/task.md | 4 ++--
   236	 1 file changed, 2 insertions(+), 2 deletions(-)
   237	```
   238	
   239	## 9. Final head `a8c2bed9` (main-checkout copy, Amendment 1)
   240	
   241	```
   242	$ gh pr checks 320 --repo mryfmo/dotfiles --watch --interval 30   # final table; exit 0
   243	CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
   244	GitGuardian Security Checks	pass	0	https://dashboard.gitguardian.com	
   245	private-bootstrap (macos-14, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/38129377997/job/114440329188	
   246	private-bootstrap (ubuntu-24.04, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/38129377997/job/114440329081	
   247	private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/38129377997/job/114440329196	
   248	public-bootstrap (macos-14, client)	pass	8m7s	https://github.com/mryfmo/dotfiles/actions/runs/38129377997/job/114440329125	
   249	public-bootstrap (ubuntu-24.04, client)	pass	9m42s	https://github.com/mryfmo/dotfiles/actions/runs/38129377997/job/114440329150	
   250	public-bootstrap (ubuntu-24.04, server)	pass	7m17s	https://github.com/mryfmo/dotfiles/actions/runs/38129377997/job/114440329256	
   251	test (macos-14, client)	pass	6m15s	https://github.com/mryfmo/dotfiles/actions/runs/38129378007/job/114440329292	
   252	test (ubuntu-24.04, client)	pass	7m49s	https://github.com/mryfmo/dotfiles/actions/runs/38129378007/job/114440329219	
   253	test (ubuntu-24.04, server)	pass	5m2s	https://github.com/mryfmo/dotfiles/actions/runs/38129378007/job/114440329374	
   254	test (ubuntu-26.04, client)	pass	8m13s	https://github.com/mryfmo/dotfiles/actions/runs/38129378007/job/114440329357	
   255	validate	pass	1m36s	https://github.com/mryfmo/dotfiles/actions/runs/38129377998/job/114440328928	
   256	$ bash scratchpad/bot-wait.sh 320 a8c2bed92559e2d9855f78154a4181363893c3f5 2026-10-11T09:43:15Z   # last poll
   257	poll 4 09:44:58Z head a8c2bed92559e2d9855f78154a4181363893c3f5 asked=no
   258	reviews: 
   259	comments: 
   260	code-review-completed: | 📝 **Code Review** | ✅ **Completed** <relative-time datetime="2026-10-11T09:44:38.538540Z">2026-10-11T09:44:38.538540Z</relative-time> | `a8c2bed` | New commits |
   261	DONE
   262	$ # final recheck right before the RESULT
   263	2026-10-11T09:53:40Z
   264	$ gh pr view 320 --json headRefOid,state,isDraft
   265	a8c2bed92559e2d9855f78154a4181363893c3f5	OPEN	false
   266	$ gh api --paginate repos/mryfmo/dotfiles/pulls/320/reviews --jq '.[]|select(.user.type=="Bot")|[.id,.commit_id[0:8],.submitted_at]|@tsv'
   267	5482144676	b3f88beb	2026-10-11T06:15:10Z
   268	$ gh api --paginate repos/mryfmo/dotfiles/pulls/320/comments --jq '.[]|select(.in_reply_to_id == null and .user.type=="Bot")|[.id,.original_commit_id[0:8],.path,(.original_line|tostring)]|@tsv'
   269	4240499289	b3f88beb	.github/workflows/remote.yaml	61
   270	$ gh api repos/mryfmo/dotfiles/issues/comments/6105983720 --jq .body | grep -E 'Code Review|Security Review'
   271	| 📝 **Code Review** | ✅ **Completed** <relative-time datetime="2026-10-11T09:44:38.538540Z">2026-10-11T09:44:38.538540Z</relative-time> | `a8c2bed` | New commits |
   272	| 🔒 **Security Review** | ✅ **Completed** <relative-time datetime="2026-10-11T05:55:43.193970Z">2026-10-11T05:55:43.193970Z</relative-time> | `9fcd2b0` | Draft marked ready |
   273	$ gh api repos/mryfmo/dotfiles/issues/320/reactions --jq '.[]|[.user.login,.content,.created_at]|@tsv'
   274	chatgpt-codex-connector[bot]	+1	2026-10-11T09:44:41Z
   275	```
     1	name: Snippet install
     2	
     3	on:
     4	  push:
     5	    branches: [main]
     6	  pull_request:
     7	    branches: [main]
     8	  workflow_dispatch:
     9	  schedule:
    10	    - cron: "0 0 * * 5"
    11	
    12	permissions:
    13	  contents: read
    14	
    15	jobs:
    16	  public-bootstrap:
    17	    strategy:
    18	      matrix:
    19	        include:
    20	          - os: ubuntu-24.04
    21	            system: client
    22	          - os: ubuntu-24.04
    23	            system: server
    24	          - os: macos-14
    25	            system: client
    26	
    27	    runs-on: ${{ matrix.os }}
    28	    env:
    29	      CI: true
    30	      SYSTEM: ${{ matrix.system }}
    31	
    32	    steps:
    33	      - name: Configure isolated HOME
    34	        run: |
    35	          mkdir -p "${RUNNER_TEMP}/dotfiles-home"
    36	          printf 'HOME=%s/dotfiles-home\n' "${RUNNER_TEMP}" >> "${GITHUB_ENV}"
    37	
    38	      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7
    39	        with:
    40	          fetch-depth: 0
    41	          persist-credentials: false
    42	
    43	      - name: Decide whether the diff needs a bootstrap
    44	        id: decide
    45	        env:
    46	          EVENT_NAME: ${{ github.event_name }}
    47	          BASE_REF: ${{ github.base_ref }}
    48	          HEAD_SHA: ${{ github.sha }}
    49	        shell: bash
    50	        run: |
    51	          set -euo pipefail
    52	          # Decided in this job, never in a job it needs: a job skipped because
    53	          # a needed job failed reports Success even as a required check, so a
    54	          # failed decision has to fail this job instead. Only a pull request has
    55	          # a base-to-head range to judge; push, schedule and workflow_dispatch
    56	          # keep bootstrapping main.
    57	          if [ "${EVENT_NAME}" != pull_request ]; then
    58	            echo "should_run=true" >> "${GITHUB_OUTPUT}"
    59	            exit 0
    60	          fi
    61	          # A full fetch: a shallow one cuts the history of a base tip that
    62	          # moved after the checkout, and the diff then has no merge base.
    63	          git fetch --no-tags origin "${BASE_REF}"
    64	          # --no-renames lists both sides of a rename; core.quotePath off keeps
    65	          # non-ASCII paths raw. An empty diff runs the bootstrap.
    66	          changed="$(git -c core.quotePath=false diff --no-renames --name-only "origin/${BASE_REF}...${HEAD_SHA}")"
    67	          if grep -qv '^\.orchestration/' <<< "${changed}"; then
    68	            echo "should_run=true" >> "${GITHUB_OUTPUT}"
    69	          else
    70	            echo "should_run=false" >> "${GITHUB_OUTPUT}"
    71	          fi
    72	
    73	      - name: Skip the bootstrap for an .orchestration-only diff
    74	        if: ${{ steps.decide.outputs.should_run != 'true' }}
    75	        run: echo "Only .orchestration/ files changed; the job reports success without bootstrapping."
    76	
    77	      - name: Bootstrap the checked-out public source
    78	        if: ${{ steps.decide.outputs.should_run == 'true' }}
    79	        env:
    80	          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    81	        shell: bash
    82	        run: |
    83	          set -euo pipefail
    84	          git checkout -b bootstrap-under-test
    85	          mkdir -p "${HOME}/.local/bin" "${HOME}/.ssh"
    86	          printf 'local-bin-sentinel\n' > "${HOME}/.local/bin/sentinel"
    87	          printf 'ssh-sentinel\n' > "${HOME}/.ssh/sentinel"
    88	          printf 'home-sentinel\n' > "${HOME}/unmanaged-sentinel"
    89	          chmod 640 "${HOME}/.local/bin/sentinel"
    90	          chmod 600 "${HOME}/.ssh/sentinel"
    91	          chmod 644 "${HOME}/unmanaged-sentinel"
    92	
    93	          checksum() { cksum "$@"; }
    94	          mode() { stat -c '%a' "$@" 2> /dev/null || stat -f '%Lp' "$@"; }
    95	          before_checksum="$(checksum "${HOME}/.local/bin/sentinel" "${HOME}/.ssh/sentinel" "${HOME}/unmanaged-sentinel")"
    96	          before_mode="$(mode "${HOME}/.local/bin/sentinel" "${HOME}/.ssh/sentinel" "${HOME}/unmanaged-sentinel")"
    97	
    98	          printf 'ci@example.invalid\n%s\n' "${SYSTEM}" | \
    99	            DOTFILES_REPO_URL="${GITHUB_WORKSPACE}" BRANCH_NAME=bootstrap-under-test \
   100	            bash "${GITHUB_WORKSPACE}/setup.sh"
   101	
   102	          test "$(git -C "${HOME}/.local/share/chezmoi" rev-parse HEAD)" = "${GITHUB_SHA}"
   103	          test "$(checksum "${HOME}/.local/bin/sentinel" "${HOME}/.ssh/sentinel" "${HOME}/unmanaged-sentinel")" = "${before_checksum}"
   104	          test "$(mode "${HOME}/.local/bin/sentinel" "${HOME}/.ssh/sentinel" "${HOME}/unmanaged-sentinel")" = "${before_mode}"
   105	          if [ "${SYSTEM}" = client ]; then
   106	            test -e "${HOME}/.zshrc"
   107	          else
   108	            test -e "${HOME}/.bashrc"
   109	          fi
   110	          printf 'Validated checkout SHA %s\n' "${GITHUB_SHA}"
   111	
   112	  private-bootstrap:
   113	    strategy:
   114	      matrix:
   115	        include:
   116	          - os: ubuntu-24.04
   117	            system: client
   118	          - os: ubuntu-24.04
   119	            system: server
   120	          - os: macos-14
   121	            system: client
   122	
   123	    runs-on: ${{ matrix.os }}
   124	    env:
   125	      CI: true
   126	      SYSTEM: ${{ matrix.system }}
   127	      HAS_EMAIL_ADDRESS: ${{ secrets.EMAIL_ADDRESS != '' }}
   128	      HAS_PRIVATE_DEPLOY_KEY: ${{ secrets.PRIVATE_DOTFILES_PRIVATE_DEPLOY_KEY != '' }}
   129	
   130	    steps:
   131	      - name: Configure isolated HOME
   132	        run: |
   133	          mkdir -p "${RUNNER_TEMP}/dotfiles-home"
   134	          printf 'HOME=%s/dotfiles-home\n' "${RUNNER_TEMP}" >> "${GITHUB_ENV}"
   135	
   136	      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7
   137	        with:
   138	          fetch-depth: 0
   139	          persist-credentials: false
   140	
   141	      - name: Decide whether the diff needs a bootstrap
   142	        id: decide
   143	        env:
   144	          EVENT_NAME: ${{ github.event_name }}
   145	          BASE_REF: ${{ github.base_ref }}
   146	          HEAD_SHA: ${{ github.sha }}
   147	        shell: bash
   148	        run: |
   149	          set -euo pipefail
   150	          # Decided in this job, never in a job it needs: a job skipped because
   151	          # a needed job failed reports Success even as a required check, so a
   152	          # failed decision has to fail this job instead. Only a pull request has
   153	          # a base-to-head range to judge; push, schedule and workflow_dispatch
   154	          # keep bootstrapping main.
   155	          if [ "${EVENT_NAME}" != pull_request ]; then
   156	            echo "should_run=true" >> "${GITHUB_OUTPUT}"
   157	            exit 0
   158	          fi
   159	          # A full fetch: a shallow one cuts the history of a base tip that
   160	          # moved after the checkout, and the diff then has no merge base.
   161	          git fetch --no-tags origin "${BASE_REF}"
   162	          # --no-renames lists both sides of a rename; core.quotePath off keeps
   163	          # non-ASCII paths raw. An empty diff runs the bootstrap.
   164	          changed="$(git -c core.quotePath=false diff --no-renames --name-only "origin/${BASE_REF}...${HEAD_SHA}")"
   165	          if grep -qv '^\.orchestration/' <<< "${changed}"; then
   166	            echo "should_run=true" >> "${GITHUB_OUTPUT}"
   167	          else
   168	            echo "should_run=false" >> "${GITHUB_OUTPUT}"
   169	          fi
   170	
   171	      - name: Skip the bootstrap for an .orchestration-only diff
   172	        if: ${{ steps.decide.outputs.should_run != 'true' }}
   173	        run: echo "Only .orchestration/ files changed; the job reports success without bootstrapping."
   174	
   175	      - name: Explain skipped private bootstrap
   176	        if: ${{ contains(github.actor, '[bot]') || env.HAS_EMAIL_ADDRESS != 'true' || env.HAS_PRIVATE_DEPLOY_KEY != 'true' }}
   177	        run: echo "Private bootstrap is optional and secrets are unavailable in this context."
   178	
   179	      - name: Set up the private deploy key
   180	        if: ${{ steps.decide.outputs.should_run == 'true' && !contains(github.actor, '[bot]') && env.HAS_EMAIL_ADDRESS == 'true' && env.HAS_PRIVATE_DEPLOY_KEY == 'true' }}
   181	        uses: webfactory/ssh-agent@e83874834305fe9a4a2997156cb26c5de65a8555 # v0.10.0
   182	        with:
   183	          ssh-private-key: ${{ secrets.PRIVATE_DOTFILES_PRIVATE_DEPLOY_KEY }}
   184	
   185	      - name: Bootstrap with private restoration
   186	        if: ${{ steps.decide.outputs.should_run == 'true' && !contains(github.actor, '[bot]') && env.HAS_EMAIL_ADDRESS == 'true' && env.HAS_PRIVATE_DEPLOY_KEY == 'true' }}
   187	        env:
   188	          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
   189	          EMAIL_ADDRESS: ${{ secrets.EMAIL_ADDRESS }}
   190	        shell: bash
   191	        run: |
   192	          set -euo pipefail
   193	          git checkout -b bootstrap-under-test
   194	          printf '%s\n%s\n' "${EMAIL_ADDRESS}" "${SYSTEM}" | \
   195	            DOTFILES_REPO_URL="${GITHUB_WORKSPACE}" BRANCH_NAME=bootstrap-under-test \
   196	            bash "${GITHUB_WORKSPACE}/setup.sh"
     1	name: Unit test
     2	
     3	on:
     4	  # Required checks must always report a final status for PRs into `main`.
     5	  # Do not add workflow-level path or branch filters here: GitHub can leave
     6	  # skipped required checks in a pending state and block merges.
     7	  # Keep this workflow unconditional and decide inside jobs whether the full
     8	  # test matrix is necessary for the current diff.
     9	  push:
    10	    branches: [main]
    11	  pull_request:
    12	    branches: [main]
    13	permissions:
    14	  contents: read
    15	
    16	jobs:
    17	  test:
    18	    # Run the same test suite on each target OS/system pair.
    19	    # We intentionally keep macOS as `client` only because this repository
    20	    # does not define a macOS `server` test target.
    21	    strategy:
    22	      matrix:
    23	        os: [ubuntu-24.04, macos-14]
    24	        system: [client, server]
    25	        exclude:
    26	          - os: macos-14
    27	            system: server
    28	        # Non-required canary for the next Ubuntu image: it shows how the suite
    29	        # fares there without blocking merges. Adopt it by changing the
    30	        # explicit label above once it is green.
    31	        include:
    32	          - os: ubuntu-26.04
    33	            system: client
    34	
    35	    runs-on: ${{ matrix.os }}
    36	    continue-on-error: ${{ matrix.os == 'ubuntu-26.04' }}
    37	    env:
    38	      # Export matrix values to shell scripts so existing test helpers can use
    39	      # simple `OS`/`SYSTEM` checks without depending on GitHub expression syntax.
    40	      OS: ${{ matrix.os }}
    41	      SYSTEM: ${{ matrix.system }}
    42	      # Keep Codecov naming deterministic per job. This makes it easy to trace
    43	      # upload sessions in Codecov API/UI and avoids accidental session overlap.
    44	      CODECOV_FLAGS: ${{ matrix.os }}-${{ matrix.system }}
    45	      CODECOV_NAME: codecov-dotfiles-${{ matrix.os }}-${{ matrix.system }}
    46	      GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    47	
    48	    steps:
    49	      - name: Configure Git defaults
    50	        run: git config --global init.defaultBranch main
    51	
    52	      - name: Checkout repository
    53	        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7
    54	        with:
    55	          fetch-depth: 0
    56	          persist-credentials: false
    57	
    58	      - name: Decide whether the diff needs the unit tests
    59	        id: decide
    60	        env:
    61	          EVENT_NAME: ${{ github.event_name }}
    62	          BASE_REF: ${{ github.base_ref }}
    63	          BEFORE_SHA: ${{ github.event.before }}
    64	          HEAD_SHA: ${{ github.sha }}
    65	        run: |
    66	          set -euo pipefail
    67	
    68	          # Decided in this job, never in a job it needs: a job skipped because
    69	          # a needed job failed reports Success even as a required check, so a
    70	          # failed decision has to fail this job instead.
    71	          if [ "${EVENT_NAME}" = "pull_request" ]; then
    72	            # A full fetch: a shallow one cuts the history of a base tip that
    73	            # moved after the checkout, and the diff then has no merge base.
    74	            git fetch --no-tags origin "${BASE_REF}"
    75	            diff_range="origin/${BASE_REF}...${HEAD_SHA}"
    76	          elif [ -n "${BEFORE_SHA}" ] && [ "${BEFORE_SHA}" != "0000000000000000000000000000000000000000" ]; then
    77	            diff_range="${BEFORE_SHA}...${HEAD_SHA}"
    78	          else
    79	            diff_range="${HEAD_SHA}^...${HEAD_SHA}"
    80	          fi
    81	
    82	          echo "diff_range=${diff_range}" >> "${GITHUB_OUTPUT}"
    83	
    84	          # One option would be to predefine CI-relevant path groups such as
    85	          # `.github/workflows/`, `home/`, `install/`, and `tests/` in an env-
    86	          # var-like form to make the rule reusable. For this workflow, keeping
    87	          # the pattern inline is still easier to read because the rule is only
    88	          # used once and only decides whether the expensive unit-test steps
    89	          # should run. It does not decide whether the required workflow itself
    90	          # reports a status. If more workflows need the same rule later,
    91	          # extract a shared script instead of hiding the pattern in env.
    92	          # The formatting check also runs here, so any .py or .md outside
    93	          # .orchestration/ counts, as do ruff.toml and .prettierignore.
    94	          # .orchestration-only diffs still skip the matrix.
    95	          # No pipe into grep -q: under pipefail its early exit could SIGPIPE
    96	          # the writer and turn a match into a false negative. core.quotePath
    97	          # off keeps non-ASCII paths raw instead of "\343..."-quoted.
    98	          # --no-renames lists both sides of a rename, so a file moved out of
    99	          # home/ into .orchestration/ still runs the tests.
   100	          changed="$(git -c core.quotePath=false diff --no-renames --name-only "${diff_range}")"
   101	          relevant="$(grep -v '^\.orchestration/' <<< "${changed}" || true)"
   102	          if grep -Eq '^(\.github/workflows/|home/|install/|scripts/|tests/|plans/|docs/|setup\.sh$|Makefile$|ruff\.toml$|\.prettierignore$)|(^|/)[^/]+\.(py|md)$' <<< "${relevant}"; then
   103	            echo "should_test=true" >> "${GITHUB_OUTPUT}"
   104	          else
   105	            echo "should_test=false" >> "${GITHUB_OUTPUT}"
   106	          fi
   107	
   108	      - name: Skip full unit test run for unrelated changes
   109	        if: ${{ steps.decide.outputs.should_test != 'true' }}
   110	        run: |
   111	          echo "No unit-test-relevant files changed."
   112	          echo "Compared diff range: ${{ steps.decide.outputs.diff_range }}"
   113	
   114	      - name: Install tools
   115	        if: ${{ steps.decide.outputs.should_test == 'true' }}
   116	        run: |
   117	          if [ "${OS}" == "macos-14" ]; then
   118	            # The macos-14 runner image ships third-party taps tapped but
   119	            # untrusted, and Homebrew warns on every `brew install` while one
   120	            # is present. The installs below come from homebrew/core, so
   121	            # resolve those taps with the brew installer's own CI handling
   122	            # rather than a second hard-coded copy of the tap list.
   123	            bash -c 'source install/macos/common/brew.sh; handle_ci_untrusted_taps'
   124	
   125	            # `bashcov` on macOS must use Homebrew Bash (>=5) to avoid the

exec
/bin/zsh -lc "rg --files ~/.cache/uv | rg '/yaml/__init__\\.py"'$'"' | head -5; sed -n '1,120p' ~/.agents/skills/agmsg/scripts/history.sh; git show -s --format=fuller 3bafe4f24c80fd1093e2fd5a19d843e5cb7aff5b; git diff --numstat 3c845c55dc43b668fa6df8434cb47a1b1f00d695 3bafe4f24c80fd1093e2fd5a19d843e5cb7aff5b" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 26ms:
~/.cache/uv/archive-v0/s3-h8CMAT4zYu88y/yaml/__init__.py
~/.cache/uv/archive-v0/-dngyL6-qyenGsFZ/yaml/__init__.py
~/.cache/uv/sdists-v9/pypi/pyyaml/6.0.3/9Siwrp7VRpSEaADr/src/build/lib.macosx-27.0-arm64-cpython-315/yaml/__init__.py
~/.cache/uv/archive-v0/0t5VBB-9uc_vGqxj/lib/python3.14/site-packages/yaml/__init__.py
~/.cache/uv/sdists-v9/pypi/pyyaml/6.0.3/9Siwrp7VRpSEaADr/src/lib/yaml/__init__.py
#!/usr/bin/env bash
set -euo pipefail

# Usage: history.sh <team> [agent_id] [limit]
# Shows message history. If agent_id given, shows only that agent's messages.

TEAM="${1:?Usage: history.sh <team> [agent_id] [limit]}"
AGENT="${2:-}"
LIMIT="${3:-20}"
# A non-numeric limit would otherwise be interpolated straight into the SQL
# text below (e.g. "1; DELETE FROM messages; --"); fall back to the default
# rather than passing it through, mirroring the interval-validation idiom
# used elsewhere (config.sh, watch.sh).
case "$LIMIT" in ''|*[!0-9]*) LIMIT=20 ;; esac

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/lib/storage.sh"
agmsg_storage_load

# A seat that reads history as itself names its own pane if it is not named
# (self-name.sh); see send.sh. Only when an agent is given: without one this
# is a team-wide read by nobody in particular.
if [ -n "$AGENT" ]; then
  # shellcheck disable=SC1091
  source "$SCRIPT_DIR/lib/self-name.sh"
  agmsg_self_name_on_action "$TEAM" "$AGENT"
  # Fix its own CLI session name once, early (self-rename.sh, #1081). Best-effort.
  # shellcheck disable=SC1091
  source "$SCRIPT_DIR/lib/self-rename.sh"
  agmsg_self_rename_on_action "$TEAM" "$AGENT"
fi

# A history read must not create a store, so a team that has never been written
# to has no file yet. Since the stores split per team that is the ordinary state
# of a freshly joined team rather than a broken install, and it reads out the
# same as an empty history. Driver-level, so it works for jsonl too.
if ! storage_store_exists "$TEAM"; then
  echo "No message history."
  exit 0
fi

# History (events ∪ legacy) via the facade; <agent> optional — omitted = whole
# team (§2.1). The driver returns the most recent --limit records already in
# chronological order, so no reversal here.
HIST_JSONL=$(storage_history "$TEAM" "$AGENT" --limit "$LIMIT")

if [ -z "$HIST_JSONL" ]; then
  echo "No message history."
  exit 0
fi

# Parse to "from \x1f to \x1f body \x1f at \x1f id" rows (no jq; cf. lib/hooks-json.sh).
# The quote is held in a variable, never written as \' in the pattern: bash 3.2
# (macOS /bin/bash) keeps the backslash of a \' REPLACEMENT, so the inline form
# doubles a quote into \'\' there while producing '' on bash 4+. Same shape as
# _sqlite_sync_lit_into in sqlite-sync.sh, which documents the same hazard.
_AGMSG_SQ="'"
_arr="[$(printf '%s' "$HIST_JSONL" | paste -sd, -)]"
# #777: same argv-length exposure on the display path. Capping --limit does not bound this
# one either, because a single long body can carry it past the ceiling on its own.
_agmsg_rows_sql=$(mktemp "${TMPDIR:-/tmp}/agmsg-history-rows.XXXXXX") || exit 13
trap 'rm -f "$_agmsg_rows_sql"' EXIT HUP INT TERM
{
  printf "%s\n" "SELECT json_extract(value,'\$.from') || char(31) ||"
  printf "%s\n" "       json_extract(value,'\$.to') || char(31) ||"
  printf "%s\n" "       replace(replace(json_extract(value,'\$.body'), char(10), '\n'), char(9), '\t') || char(31) ||"
  printf "%s\n" "       json_extract(value,'\$.at') || char(31) ||"
  printf "%s\n" "       json_extract(value,'\$.id')"
  printf "FROM json_each('"
  printf '%s' "${_arr//$_AGMSG_SQ/$_AGMSG_SQ$_AGMSG_SQ}"
  printf "');\n"
} > "$_agmsg_rows_sql"
# Windows sqlite3.exe may treat redirected stdin as interactive input unless
# batch mode is explicit, returning success without evaluating the SQL. Keep
# the stdin path (it avoids command-line length limits) and make the mode
# explicit on every platform.
ROWS=$(agmsg_sqlite -batch ':memory:' < "$_agmsg_rows_sql")
rm -f "$_agmsg_rows_sql"
trap - EXIT HUP INT TERM

# Read-state for the ●(unread)/○(read) marker (G2(c)): read-state is
# recipient-scoped and not carried on a history record, so derive it by unioning
# storage_list_unread over the distinct recipients in this slice. (Phase 1:
# mark-read still lands in legacy read_at, which the facade UNION reflects.)
RECIPIENTS=$(while IFS=$'\x1f' read -r _f to _rest; do
  [ -n "$to" ] && printf '%s\n' "$to"
done <<< "$ROWS" | sort -u)

UNREAD_IDS=""
while IFS= read -r r; do
  [ -n "$r" ] || continue
  u=$(storage_list_unread "$TEAM" "$r") || continue
  [ -n "$u" ] || continue
  uarr="[$(printf '%s' "$u" | paste -sd, -)]"
  # #777: a recipient's unread backlog grows independently of the display limit, so
  # interpolating it into one argv element eventually exceeds the ceiling on a SINGLE
  # argument -- on Linux `MAX_ARG_STRLEN`, 131,072 bytes. Measured: the failing
  # statement for a 2,079-message team was 125,945 bytes, which is nowhere near
  # `ARG_MAX` (2,097,152 here) because ARG_MAX bounds argv plus environment in total,
  # not any one element of it. The distinction decides the repair: splitting one long
  # statement into several shorter arguments satisfies MAX_ARG_STRLEN and leaves
  # ARG_MAX untouched, and a reader who has the wrong limit in mind reaches for the
  # wrong fix. Note also that MAX_ARG_STRLEN is a kernel constant with no getconf key,
  # so the limit that bites is the one the tools cannot show you.
  #
  # Pass the statement on stdin instead, mirroring drivers/storage/sqlite-sync.sh:1082.
  # printf is a bash builtin, so feeding it a large value does not exec at all and can
  # hit neither ceiling.
  _agmsg_unread_sql=$(mktemp "${TMPDIR:-/tmp}/agmsg-history-unread.XXXXXX") || continue
  trap 'rm -f "$_agmsg_unread_sql"' EXIT HUP INT TERM
  {
    printf "SELECT json_extract(value,'\$.id') FROM json_each('"
    printf '%s' "${uarr//$_AGMSG_SQ/$_AGMSG_SQ$_AGMSG_SQ}"
    printf "');\n"
  } > "$_agmsg_unread_sql"
  ids=$(agmsg_sqlite -batch ':memory:' < "$_agmsg_unread_sql")
  rm -f "$_agmsg_unread_sql"
  trap - EXIT HUP INT TERM
  UNREAD_IDS+="$ids"$'\n'
done <<< "$RECIPIENTS"
commit 3bafe4f24c80fd1093e2fd5a19d843e5cb7aff5b
Merge: a8c2bed9 3c845c55
Author:     moriya-fumio-thd <moriya.fumio@technopro.com>
AuthorDate: Sun Oct 11 18:54:46 2026 +0900
Commit:     GitHub <noreply@github.com>
CommitDate: Sun Oct 11 18:54:46 2026 +0900

    Merge branch 'main' into feat/ci-skip-orchestration
73	2	.github/workflows/remote.yaml
57	69	.github/workflows/test.yaml
3	0	.orchestration/dotfiles-T128-ci-skip-orchestration-a01/autoskill.md
8	0	.orchestration/dotfiles-T128-ci-skip-orchestration-a01/learning.md
56	0	.orchestration/dotfiles-T128-ci-skip-orchestration-a01/report.md
5	0	.orchestration/dotfiles-T128-ci-skip-orchestration-a01/revise.yaml
53	0	.orchestration/dotfiles-T128-ci-skip-orchestration-a01/sandbox.md
73	0	.orchestration/dotfiles-T128-ci-skip-orchestration-a01/task.md
401	0	.orchestration/dotfiles-T128-ci-skip-orchestration-a01/validation.md
3	0	.orchestration/dotfiles-T128-ci-skip-orchestration-a02/autoskill.md
7	0	.orchestration/dotfiles-T128-ci-skip-orchestration-a02/learning.md
44	0	.orchestration/dotfiles-T128-ci-skip-orchestration-a02/report.md
34	0	.orchestration/dotfiles-T128-ci-skip-orchestration-a02/sandbox.md
78	0	.orchestration/dotfiles-T128-ci-skip-orchestration-a02/task.md
200	0	.orchestration/dotfiles-T128-ci-skip-orchestration-a02/validation.md
370	0	tests/unit/test_workflow_orchestration_skip.py

**Reviewing YAML parsing concerns**
**Analyzing YAML parser behavior and orchestration state**
codex
GitHub’s connected API confirms that all seven required contexts passed on `3bafe4f2`; the test jobs actually ran their suites. The design hash on main and the amended task copy also match the report. The acceptance record still describes redispatch as future work, so I’m checking the dispatch evidence before deciding whether that is a documentation gap or an invariant failure.

exec
/bin/zsh -lc "python3 -B -c 'import pathlib,sys,subprocess,types,unittest,io
from unittest.mock import patch
sys.path.insert(0,\"~/.cache/uv/archive-v0/s3-h8CMAT4zYu88y\")
import yaml
head=\"3bafe4f24c80fd1093e2fd5a19d843e5cb7aff5b\"
def show(p):return subprocess.check_output([\"git\",\"show\",head+\":\"+p],text=True)
p=\"tests/unit/test_workflow_orchestration_skip.py\";m=types.ModuleType(\"audit_target\");m.__file__=str(pathlib.Path(p).resolve());exec(compile(show(p),p,\"exec\"),m.__dict__)
texts={str(pathlib.Path(p).resolve()):show(p) for p in [\".github/workflows/remote.yaml\",\".github/workflows/test.yaml\",\".github/workflows/agent-assets.yml\"]}
def read(self,*a,**k):return texts[str(self.resolve())]
for p,t in texts.items():print(\"YAML jobs\",p,list(yaml.safe_load(t)[\"jobs\"]))
task=yaml.safe_load(pathlib.Path(\".orchestration/tasks/dotfiles-T128-ci-skip-orchestration-a02.md\").read_text().split(\"---\")[1])
design=yaml.safe_load(subprocess.check_output([\"git\",\"show\",\"3c845c55:.orchestration/tasks/dotfiles-T128-regime-v3-a01.md\"],text=True).split(\"---\")[1])
print(\"Invariant ids\",list(task[\"invariants\"]),design[\"implementing_tasks\"][task[\"task_id\"]])
print(\"Invariant sentences identical\",all(v==design[\"invariants\"][k] for k,v in task[\"invariants\"].items()))
remote=texts[str(m.REMOTE)]
job,decide,steps=\"\\n  public-bootstrap:\\n\",\"        id: decide\\n\",\"    steps:\\n\"
forms={
\"spaced job key\":(job,job+\"    if : false\\n\"),
\"escaped job key\":(job,job+'\\''    \"\\\\x69f\": false\\n'\\''),
\"spaced step key\":(decide,decide+\"        continue-on-error : true\\n\"),
\"flow-mapping step\":(steps,steps+\"      - { if: false }\\n\"),
\"quoted job name\":(job,\"\\n  '\\''public-bootstrap'\\'':\\n\"),
\"quoted step key\":(decide,\"        '\\''id'\\'': decide\\n\"),
\"shifted job body\":(\"\\njobs:\\n\",\"\\njobs:\\n  shifted:\\n      if: false\\n      runs-on: ubuntu-24.04\\n\"),
\"shifted step item\":(\"      - name: Decide whether\",\"      -   name: Decide whether\"),
\"merge key\":(job,job+\"    <<: {if: false}\\n\"),
\"flow job\":(job,\"\\n  public-bootstrap: {if: false}\\n  extra:\\n\"),
}
for name,(old,new) in forms.items():
 mutated=remote.replace(old,new,1)
 yaml.safe_load(mutated)
 texts[str(m.REMOTE)]=mutated
 try:
  with patch.object(pathlib.Path,\"read_text\",read):m.jobs(m.REMOTE)
 except ValueError as e: print(name,\"RAISES\",e)
 else:print(name,\"ACCEPTED\")
texts[str(m.REMOTE)]=remote
'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 exited 1 in 281ms:
Traceback (most recent call last):
  File "<string>", line 31, in <module>
    yaml.safe_load(mutated)
    ~~~~~~~~~~~~~~^^^^^^^^^
  File "~/.cache/uv/archive-v0/s3-h8CMAT4zYu88y/yaml/__init__.py", line 125, in safe_load
    return load(stream, SafeLoader)
  File "~/.cache/uv/archive-v0/s3-h8CMAT4zYu88y/yaml/__init__.py", line 81, in load
    return loader.get_single_data()
           ~~~~~~~~~~~~~~~~~~~~~~^^
  File "~/.cache/uv/archive-v0/s3-h8CMAT4zYu88y/yaml/constructor.py", line 49, in get_single_data
    node = self.get_single_node()
  File "~/.cache/uv/archive-v0/s3-h8CMAT4zYu88y/yaml/composer.py", line 36, in get_single_node
    document = self.compose_document()
  File "~/.cache/uv/archive-v0/s3-h8CMAT4zYu88y/yaml/composer.py", line 55, in compose_document
    node = self.compose_node(None, None)
  File "~/.cache/uv/archive-v0/s3-h8CMAT4zYu88y/yaml/composer.py", line 84, in compose_node
    node = self.compose_mapping_node(anchor)
  File "~/.cache/uv/archive-v0/s3-h8CMAT4zYu88y/yaml/composer.py", line 133, in compose_mapping_node
    item_value = self.compose_node(node, item_key)
  File "~/.cache/uv/archive-v0/s3-h8CMAT4zYu88y/yaml/composer.py", line 84, in compose_node
    node = self.compose_mapping_node(anchor)
  File "~/.cache/uv/archive-v0/s3-h8CMAT4zYu88y/yaml/composer.py", line 133, in compose_mapping_node
    item_value = self.compose_node(node, item_key)
  File "~/.cache/uv/archive-v0/s3-h8CMAT4zYu88y/yaml/composer.py", line 84, in compose_node
    node = self.compose_mapping_node(anchor)
  File "~/.cache/uv/archive-v0/s3-h8CMAT4zYu88y/yaml/composer.py", line 133, in compose_mapping_node
    item_value = self.compose_node(node, item_key)
  File "~/.cache/uv/archive-v0/s3-h8CMAT4zYu88y/yaml/composer.py", line 82, in compose_node
    node = self.compose_sequence_node(anchor)
  File "~/.cache/uv/archive-v0/s3-h8CMAT4zYu88y/yaml/composer.py", line 110, in compose_sequence_node
    while not self.check_event(SequenceEndEvent):
              ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
  File "~/.cache/uv/archive-v0/s3-h8CMAT4zYu88y/yaml/parser.py", line 98, in check_event
    self.current_event = self.state()
                         ~~~~~~~~~~^^
  File "~/.cache/uv/archive-v0/s3-h8CMAT4zYu88y/yaml/parser.py", line 392, in parse_block_sequence_entry
    raise ParserError("while parsing a block collection", self.marks[-1],
            "expected <block end>, but found %r" % token.id, token.start_mark)
yaml.parser.ParserError: while parsing a block collection
  in "<unicode string>", line 33, column 7:
          - name: Configure isolated HOME
          ^
expected <block end>, but found '<block mapping start>'
  in "<unicode string>", line 44, column 9:
            id: decide
            ^
YAML jobs ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review/.github/workflows/remote.yaml ['public-bootstrap', 'private-bootstrap']
YAML jobs ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review/.github/workflows/test.yaml ['test']
YAML jobs ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review/.github/workflows/agent-assets.yml ['validate']
Invariant ids ['INV-2'] ['INV-2']
Invariant sentences identical True
spaced job key RAISES unsupported key form inside jobs: '    if : false'
escaped job key RAISES unsupported key form inside jobs: '    "\\x69f": false'
spaced step key RAISES unsupported key form inside jobs: '        continue-on-error : true'
flow-mapping step RAISES unsupported key form inside jobs: '      - { if: false }'
quoted job name RAISES unsupported key form inside jobs: "  'public-bootstrap':"
quoted step key RAISES unsupported key form inside jobs: "        'id': decide"
shifted job body RAISES unsupported job body indentation inside jobs: '      if: false'

exec
/bin/zsh -lc "rg -n '09:41|09:42|task_id=dotfiles-T128-ci-skip-orchestration-a02|4de54fde' .orchestration/agmsg .orchestration/acceptance/dotfiles-T128-ci-skip-orchestration-a01-design-reset.md .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round18.md .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round18-codex.md; sed -n '1,125p' ~/.agents/skills/agmsg/SKILL.md" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 0ms:
rg: .orchestration/agmsg: No such file or directory (os error 2)
.orchestration/acceptance/dotfiles-T128-ci-skip-orchestration-a01-design-reset.md:5:design_sha256: 4de54fdec5db667e940365703ee5e16cd1d91f52794c79c75b48aad7eb0a8763
.orchestration/acceptance/dotfiles-T128-ci-skip-orchestration-a01-design-reset.md:20:- **Anchor refresh 3 (08:32Z):** the successor's `design_review.receipt` now names round 18, the first receipt that reviews its map entry (Bot P2 4240827027 on PR #321); hash `4de54fde…`; the review seat's `verdict=accept` on it confirmed: RESULT at 08:31:07Z, round 4.
---
name: agmsg
description: Cross-agent messaging via SQLite. Send messages between Claude Code, Codex, Gemini CLI, and other agents. No daemon, no network, no dependencies beyond bash and sqlite3.
---

<!-- agmsg:render-root -->

Agent messaging command. **IMPORTANT: Always use the provided scripts. NEVER directly read or edit config files, DB, or team data. There is NO register.sh — use join.sh to join a team.**

**Use agmsg, not the host agent's own inter-session messaging.** Several agent
CLIs ship a native way for one session to message another on the same machine
(in Claude Code, the `SendMessage` / `ListAgents` tools over its peer-session
list). While a project is on agmsg, route agent-to-agent messages through agmsg
instead. A message sent natively does not exist as far as agmsg is concerned:
it is absent from `history.sh` and the team's export, it never reaches a member
on another machine through remote sync, it does not mark read or advance any
cursor, and it cannot address a member whose CLI is a different type. Half the
conversation living somewhere unrecorded is worse than either channel alone,
and the gap is invisible until someone reads the history and finds a decision
with no message behind it. The native channel stays fine for anything outside
the team — a subagent you spawned for your own task, or a session that has not
joined.

**Shell requirement:** All agmsg scripts are Bash scripts. Always execute them via `bash`, never via PowerShell or cmd directly. If your default shell is not Bash (e.g. PowerShell on Windows), wrap every command with `bash -lc '...'`. Example: `bash -lc '~/.agents/skills/agmsg/scripts/send.sh myteam alice bob "hello"'`. Do NOT construct DB paths manually — the scripts handle path resolution internally. If you need to redirect storage, use `AGMSG_STORAGE_PATH` (the supported override).

On Windows PowerShell, invoke Git Bash explicitly and keep the full `bash -lc` payload inside one single-quoted string:

`& 'C:\Program Files\Git\bin\bash.exe' -lc '~/.agents/skills/agmsg/scripts/whoami.sh "$(pwd)" codex'`

Do not use POSIX `'"'"'` quote splicing in PowerShell, and do not use escaped double quotes inside the wrapper.

## Identity

If you already know your AGENT and TEAMS from a previous `$agmsg` call in this session, skip to **Execute** below.

Otherwise, run: `~/.agents/skills/agmsg/scripts/whoami.sh "$(pwd)" codex`

Four possible outputs:

**A) Single identity:**
`agent=<name> teams=<t1,t2,...> type=codex project=<path>`
→ Remember AGENT and TEAMS, then go to **Execute**.

**B) Multiple identities:**
`multiple=true agents=<n1,n2,...> teams=<t1,t2,...> type=codex project=<path>`
→ Ask the user which agent name to use for this session, then go to **Execute**.

**C) Not in a team:**
`not_joined=true available_teams=<t1,t2,...>` (or `available_teams=none`)
→ Show the user the available teams from the output, then:

  Before first-time setup, inspect the user's request. If they ask to join, import, or bring in a team that already exists on a server, do not call `join.sh`. Go directly to `remote pull` under Execute. First run `~/.agents/skills/agmsg/scripts/team-list.sh --json --scope all`; if a same-named local team has `binding_state` `none` or `disconnected`, stop and ask the user how to proceed. After pull succeeds, return to Identity setup so the user can register a new local agent in the pulled team.

  > **First-time setup required.**
  > Joining a team so this agent can send and receive messages.
  > - **Team name**: a group of agents that can message each other (available: <list from output>)
  > - **Agent name**: this agent's identity within the team

  1. Ask: "Enter a team name (joins existing or creates new)"
  2. If the team name given already appears in `available_teams`, run `~/.agents/skills/agmsg/scripts/team.sh <team>` to see the current roster (name, type, project) and note the names already in use. Look for a naming convention already in play (e.g. a shared base name with role and number suffixes (`<base>-<role><n>`), or names derived from the team name) and, when one exists, propose 2-3 unused names that extend it; otherwise propose 2-3 short, distinctive identity names (not a bare tool-type label like `codex`/`cc`). Either way, names must not collide with the roster. Then ask: "Enter a name for this agent (suggestions: <name1>, <name2>, <name3> — or type your own)". For a brand-new team, skip the roster check and just ask: "Enter a name for this agent".
  3. **You MUST use join.sh** — run: `~/.agents/skills/agmsg/scripts/join.sh <team> <agent_name> codex "$(pwd)"`
  4. Show the result and explain:

  > **Joined!** You can now use `$agmsg` to check and send messages.
  > - `$agmsg` — check inbox
  > - `$agmsg send <agent> <message>` — send a message
  > - `$agmsg team` — list team members
  > - `$agmsg history` — message history

<!-- agmsg:render-overlay codex -->
  5. **REQUIRED — Do NOT skip this step.** Ask the user to pick `monitor`, `turn`, or `off` delivery. Empty input means `monitor`.
     Run `~/.agents/skills/agmsg/scripts/delivery.sh set <mode> codex "$(pwd)"`.
     Monitor uses the Codex app-server bridge; it changes how `codex` starts and is documented in `docs/codex-monitor-beta.md`.

  6. Then check inbox for the newly joined team.

**D) Suggestions for reuse:**
`suggest=true agents=<n1,n2,...> teams=<t1,t2,...> type=codex project=<path> available_teams=<t1,t2,...>`
→ No exact registration exists for this project, but there are same-type agent names registered elsewhere.

  1. Show the suggested agent names to the user.
  2. Ask whether to reuse one of those names or choose a new one.
  3. Ask for the team name to join (existing or new).
  4. Run: `~/.agents/skills/agmsg/scripts/join.sh <team> <agent_name> codex "$(pwd)"`
  5. Then continue with the normal post-join flow above.

## Execute

**Only use scripts in `~/.agents/skills/agmsg/scripts/` — do not read or modify files under `teams/` or `db/` directly.** Treat the storage layout as internal: never construct a database path or invoke `sqlite3` directly. The scripts resolve the active store, including `AGMSG_STORAGE_PATH` overrides.

**Terminal/pane self-awareness.** Asked about this session's own terminal, pane, or driver — or before using `arrange`, `peek`, or `poke` below — run `where.sh` (see the "where" argument below) first and answer from its `terminal=`/`capabilities=` fields. Never infer the driver from environment variables or a `grep`/`ps` guess: that is how a session under a real driver ends up reporting a false negative about its own placement, or claiming a capability or a whole driver does not exist when it does (#1171). Each driver's own operational detail lives in `~/.agents/skills/agmsg/scripts/drivers/terminals/<terminal>/README.md`, named by `where.sh`'s own `terminal=` field — never guessed at from a remembered syntax.

Asked about a *teammate's* placement or status, or what can be done to one, that is `team.sh <team>`'s question (see the "team" argument below), not something to infer from a stale memory of their last known pane. Act on a teammate with `peek.sh`/`poke.sh`/`arrange.sh <team> <name>` directly rather than guessing reachability first — its exit code says whether it worked and, if not, why (see the "peek"/"poke"/"arrange" arguments below).

**If no arguments provided (DEFAULT action — always do this when the command is invoked without arguments):**
1. **IMMEDIATELY** run inbox check for each TEAM: `~/.agents/skills/agmsg/scripts/inbox.sh $TEAM $AGENT`
2. Do NOT ask the user what to do — just run the inbox check.
3. If there are messages, read and respond appropriately. To reply:
   `~/.agents/skills/agmsg/scripts/send.sh $TEAM $AGENT <to_agent> "<message>"`


If argument is "history":
1. Run: `~/.agents/skills/agmsg/scripts/history.sh $TEAM $AGENT`

If argument starts with "team list" (e.g. "team list", "team list --json", "team list --scope project"):
1. Run: `~/.agents/skills/agmsg/scripts/team-list.sh <the rest of the args after "team list", unchanged>`
2. This is a distinct command from bare "team" below — check for "team list" FIRST so "list" is never mistaken for a team name.

If argument is "team" or "team --json":
1. For each TEAM, run: `~/.agents/skills/agmsg/scripts/team.sh $TEAM [--json]`, preserving the option when present. `--json` returns every observed field.
2. This is read-only. It reports each member's identity cells and whether they are consistent — including a member that does not answer at all — but writes nothing and pokes no one. A seat that is wrong or unresponsive is not something this command, or any other, repairs from the outside: typing into another seat's session to fix it is exactly the mistake that used to happen here, and it is gone on purpose, not replaced by another form of the same thing. A member repairs its own identity cells by running `fix` (below), from itself. A seat that cannot or will not do that gets despawned and restarted, or a person takes it — not patched over from another pane.

If argument starts with "send" (e.g. "send misaki check the server"):
1. Parse target agent and message from the arguments
2. Determine which team the target agent belongs to, then run:
   `~/.agents/skills/agmsg/scripts/send.sh $TEAM $AGENT <to_agent> "<message>"`

If argument is "config":
1. Run: `~/.agents/skills/agmsg/scripts/config.sh show`
2. Show the output to the user.

If argument starts with "config set" (e.g. "config set hook.check_interval 30"):
1. Parse key and value from the arguments.
2. Run: `~/.agents/skills/agmsg/scripts/config.sh set <key> <value>`


**Analyzing test validity and git diff behavior**
**Verifying job matrix and history access**
mcp: codex_apps/github.fetch started
mcp: codex_apps/github.fetch started
exec
/bin/zsh -lc 'git show 3bafe4f24c80fd1093e2fd5a19d843e5cb7aff5b:tests/unit/test_workflow_security.py; git diff 3c845c55dc43b668fa6df8434cb47a1b1f00d695 3bafe4f24c80fd1093e2fd5a19d843e5cb7aff5b -- .orchestration/dotfiles-T128-ci-skip-orchestration-a02/; nl -ba .orchestration/acceptance/dotfiles-T128-ci-skip-orchestration-a01-design-reset.md' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc 'bash ~/.agents/skills/agmsg/scripts/team-list.sh --json --scope all' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 79ms:
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = ROOT / ".github/workflows"
EXPECTED_PERMISSIONS = {
    "agent-assets.yml": {"contents": "read"},
    "docs.yml": {"contents": "write"},
    "macos.yaml": {"contents": "read"},
    "remote.yaml": {"contents": "read"},
    "test.yaml": {"contents": "read"},
    "ubuntu.yaml": {"contents": "read"},
}
CHECKOUT_CREDENTIAL_EXEMPTIONS = {
    (
        "docs.yml",
        "deploy",
        "Checkout repository",
    ): "make deploy pushes the generated documentation",
}


def top_level_permissions(text: str) -> dict[str, str]:
    lines = text.splitlines()
    try:
        start = lines.index("permissions:") + 1
    except ValueError:
        return {}
    permissions = {}
    for line in lines[start:]:
        if line and not line.startswith(" "):
            break
        if not line.strip():
            continue
        match = re.fullmatch(r"  ([a-z-]+): (read|write|none)", line)
        if match:
            permissions[match.group(1)] = match.group(2)
        else:
            permissions[f"invalid:{line}"] = "invalid"
    return permissions


def checkout_steps(text: str) -> list[tuple[str, str, str]]:
    lines = text.splitlines()
    steps = []
    for index, line in enumerate(lines):
        match = re.match(
            r"""(\s*)(-\s+)?uses:\s*(?P<quote>['"]?)actions/checkout@[^\s'"]+(?P=quote)(?:[ \t]+#.*)?[ \t]*$""",
            line,
        )
        if not match:
            continue
        step_indent = len(match.group(1)) - (0 if match.group(2) else 2)
        start = index if match.group(2) else index - 1
        while start >= 0 and not re.match(rf" {{{step_indent}}}-\s+", lines[start]):
            start -= 1
        if start < 0:
            continue
        end = index + 1
        while end < len(lines):
            candidate = lines[end]
            if candidate.strip() and len(candidate) - len(candidate.lstrip()) <= step_indent:
                break
            end += 1
        name_match = re.match(r"\s*-\s+name:\s*(.+)", lines[start])
        step_name = name_match.group(1) if name_match else ""
        job_name = ""
        for parent in reversed(lines[:start]):
            job_match = re.match(r"  ([A-Za-z0-9_-]+):\s*$", parent)
            if job_match:
                job_name = job_match.group(1)
                break
        steps.append((job_name, step_name, "\n".join(lines[start:end])))
    return steps


def checkout_step_disables_credentials(block: str) -> bool:
    lines = block.splitlines()
    step_indent = len(lines[0]) - len(lines[0].lstrip())
    values = []
    for index, line in enumerate(lines):
        match = re.match(rf"( {{{step_indent + 2}}})with:\s*$", line)
        if not match:
            continue
        indent = len(match.group(1))
        for option in lines[index + 1 :]:
            if option.strip() and len(option) - len(option.lstrip()) <= indent:
                break
            option_match = re.fullmatch(
                rf" {{{indent + 2}}}persist-credentials:\s*([^#\s]+)(?:\s+#.*)?",
                option,
            )
            if option_match:
                values.append(option_match.group(1))
    return values == ["false"]


class WorkflowSecurityTest(unittest.TestCase):
    def test_external_actions_use_full_commit_shas(self):
        mutable = []
        for path in sorted(WORKFLOWS.glob("*.y*ml")):
            for number, line in enumerate(path.read_text().splitlines(), 1):
                match = re.search(r"uses:\s+([^\s]+)", line)
                if not match:
                    continue
                reference = match.group(1)
                if reference.startswith(("./", "docker://")):
                    continue
                if not re.fullmatch(r"[^@]+@[0-9a-f]{40}", reference):
                    mutable.append(f"{path.name}:{number}: {reference}")
        self.assertEqual([], mutable)

    def test_workflows_have_exact_top_level_permissions(self):
        actual = {path.name: top_level_permissions(path.read_text()) for path in sorted(WORKFLOWS.glob("*.y*ml"))}
        self.assertEqual(EXPECTED_PERMISSIONS, actual)

    def test_workflows_have_no_job_level_permission_overrides(self):
        overrides = []
        for path in sorted(WORKFLOWS.glob("*.y*ml")):
            for number, line in enumerate(path.read_text().splitlines(), 1):
                if re.match(r" {4,}permissions\s*:", line):
                    overrides.append(f"{path.name}:{number}")
        self.assertEqual([], overrides)

    def test_checkout_does_not_persist_credentials_without_explicit_exemption(self):
        insecure = []
        stale_exemptions = []
        exemption_hits = dict.fromkeys(CHECKOUT_CREDENTIAL_EXEMPTIONS, 0)
        for path in sorted(WORKFLOWS.glob("*.y*ml")):
            for job_name, step_name, block in checkout_steps(path.read_text()):
                exemption = (path.name, job_name, step_name)
                if exemption in CHECKOUT_CREDENTIAL_EXEMPTIONS:
                    exemption_hits[exemption] += 1
                    if checkout_step_disables_credentials(block):
                        stale_exemptions.append(exemption)
                elif not checkout_step_disables_credentials(block):
                    insecure.append(f"{path.name}: {job_name}: {step_name}")
        self.assertEqual([], insecure)
        self.assertEqual([], stale_exemptions)
        self.assertEqual(dict.fromkeys(CHECKOUT_CREDENTIAL_EXEMPTIONS, 1), exemption_hits)
        self.assertTrue(all(reason.strip() for reason in CHECKOUT_CREDENTIAL_EXEMPTIONS.values()))

    def test_checkout_setting_does_not_leak_from_the_next_step(self):
        workflow = """jobs:
  test:
    steps:
      - name: Checkout repository
        uses: actions/checkout@0000000000000000000000000000000000000000
      - name: Unrelated step
        with:
          persist-credentials: false
"""
        [(_, _, block)] = checkout_steps(workflow)
        self.assertFalse(checkout_step_disables_credentials(block))

    def test_unnamed_checkout_setting_does_not_leak_from_the_next_step(self):
        workflow = """jobs:
  test:
    steps:
      - uses: actions/checkout@0000000000000000000000000000000000000000
      - name: Unrelated step
        with:
          persist-credentials: false
"""
        [(_, step_name, block)] = checkout_steps(workflow)
        self.assertEqual("", step_name)
        self.assertFalse(checkout_step_disables_credentials(block))

    def test_quoted_unnamed_checkout_is_detected(self):
        trailing_spaces = "   "
        for quote in ("'", '"'):
            with self.subTest(quote=quote):
                workflow = f"""jobs:
  test:
    steps:
      - uses: {quote}actions/checkout@0000000000000000000000000000000000000000{quote}{trailing_spaces}
"""
                [(_, step_name, block)] = checkout_steps(workflow)
                self.assertEqual("", step_name)
                self.assertFalse(checkout_step_disables_credentials(block))

    def test_checkout_rejects_duplicate_or_non_false_credential_settings(self):
        for settings in (
            "persist-credentials: true",
            "persist-credentials: false\n          persist-credentials: true",
            "persist-credentials: false\n          persist-credentials: false",
        ):
            with self.subTest(settings=settings):
                block = f"""      - uses: actions/checkout@0000000000000000000000000000000000000000
        with:
          {settings}
"""
                self.assertFalse(checkout_step_disables_credentials(block))


if __name__ == "__main__":
    unittest.main()
diff --git a/.orchestration/dotfiles-T128-ci-skip-orchestration-a02/autoskill.md b/.orchestration/dotfiles-T128-ci-skip-orchestration-a02/autoskill.md
new file mode 100644
index 00000000..b16fa1be
--- /dev/null
+++ b/.orchestration/dotfiles-T128-ci-skip-orchestration-a02/autoskill.md
@@ -0,0 +1,3 @@
+# AutoSkill run: dotfiles-T128-ci-skip-orchestration-a02
+
+- Status: not used. The task names no AutoSkill run.
diff --git a/.orchestration/dotfiles-T128-ci-skip-orchestration-a02/learning.md b/.orchestration/dotfiles-T128-ci-skip-orchestration-a02/learning.md
new file mode 100644
index 00000000..52007956
--- /dev/null
+++ b/.orchestration/dotfiles-T128-ci-skip-orchestration-a02/learning.md
@@ -0,0 +1,7 @@
+# Learning triage: dotfiles-T128-ci-skip-orchestration-a02
+
+These are candidates only; nothing is promoted.
+
+1. [memory:failure] A hand-written YAML reader that accepts some forms and skips the rest is fail-open: each skipped form is a key the test cannot see while GitHub obeys it (spaced, escaped and quoted keys, flow mappings, a body shifted off its column). Make the reader raise on anything outside the one form it parses, check positions as well as forms, and show the hidden key with a real parser (`uv run --with pyyaml`) beside each mutation.
+2. [memory:decision] A test that replaces a revise check under a reset is named in the report together with the selector it retires. The superseded task's `revise.yaml` stays as history, but its selector no longer resolves.
+3. [memory:failure] `FAILED (errors=N)` counts failing subTests, not tests. When a proof shows "13 tests, 12 errors", paste the `-v` list of the tests that still pass, and say why each passes, so no structural test looks like it slipped through.
diff --git a/.orchestration/dotfiles-T128-ci-skip-orchestration-a02/report.md b/.orchestration/dotfiles-T128-ci-skip-orchestration-a02/report.md
new file mode 100644
index 00000000..93aabffe
--- /dev/null
+++ b/.orchestration/dotfiles-T128-ci-skip-orchestration-a02/report.md
@@ -0,0 +1,44 @@
+# Report: dotfiles-T128-ci-skip-orchestration-a02
+
+- Seat: `claude-standard-dot-a003` in `.claude/worktrees/worker-f`, branch `feat/ci-skip-orchestration`, PR #320, continuing from `dc4e6c37`. Reset successor of `dotfiles-T128-ci-skip-orchestration-a01` under INV-6 (reset record `.orchestration/acceptance/dotfiles-T128-ci-skip-orchestration-a01-design-reset.md`); the implementation on `dc4e6c37` stays.
+- Task file sha256 `2c3a5ee2…` checked against TASK 07:35:34Z and copied byte-identical in `406ca746` to `.orchestration/dotfiles-T128-ci-skip-orchestration-a02/task.md` (the a01 directory stays as it is). Content commit `a35a751e`; then this evidence.
+
+## What changed (`a35a751e`, `tests/unit/test_workflow_orchestration_skip.py` only)
+
+The hand-written workflow reader now fails closed. The test environment has no YAML parser (`make unit-test` runs bare `uv run python`), and no dependency is added. Inside `jobs:`:
+
+- a job name, a job key or a step key must be the plain form `name:` (`[a-z0-9_-]+`, the colon right after, then end of line or a space). Anything else raises `ValueError`: quotes, escapes, a space before the colon, a flow mapping, `<<` merge keys. A job name must carry no value, so `job: {…}` raises too. Comments and blank lines are skipped, and `run: |` script lines are captured as before.
+- a job body's first line must sit at four spaces, and a step item's first key must follow `- ` directly. Sibling keys share one indentation, so this pins every job and step key to its column. A body shifted to six spaces, or `-   name:` with its keys at ten, would otherwise hide every key from the reader while GitHub reads them (validation §3, the two positional rows).
+- a line at six spaces inside `steps:` that is not a `- ` item, or a step key before any item, raises.
+
+`test_the_reader_fails_closed_on_unsupported_key_forms` replaces `test_structural_tests_see_quoted_keys` (a01's revise check): under the reset, quoted keys raise instead of reading as bare ones, so a01's `revise.yaml` selector no longer resolves. a01 is reset history. The new test has eight subTests: the task's four forms (`if : false`, `"\x69f": false`, `continue-on-error : true`, a step written as `{ if: false }`), a quoted job name, a quoted step key, a shifted job body and a shifted step item. Each must raise.
+
+## Threat table (the completion condition)
+
+| Row | Disposition | Where |
+|---|---|---|
+| The PR edits the workflow files themselves | residual, as the task states | `tests/unit/test_workflow_security.py` passes unchanged (validation §2) |
+| The decision step misclassifies a diff | closed | `DecisionTest.test_a_pull_request_skips_the_bootstrap_only_for_an_orchestration_only_diff`, `…test_the_unit_test_decision_skips_an_orchestration_only_diff`, `…test_the_unit_test_decision_ignores_renames` |
+| A required job is skipped | closed | `RequiredContextsTest.test_no_required_contexts_job_has_a_job_level_if_or_needs` and `…test_no_job_is_left_for_a_required_job_to_need`, read by the fail-closed reader: each of the six unsupported-form mutations errors them (validation §3) |
+| The decision step itself fails | closed | `DecisionStepTest.test_each_deciding_job_decides_after_its_checkout_and_fails_closed`, `…test_every_heavy_step_carries_its_jobs_decision`, read by the same reader |
+| The reader misses a valid YAML form | closed | `RequiredContextsTest.test_the_reader_fails_closed_on_unsupported_key_forms`. The task's four mutations, and the two positional ones found while checking the reader, each hide a real key from GitHub's YAML parser and fail every structural test that reads the mutated job (validation §3). The lenient reader, and the reader without the indentation check, each fail the test |
+| The design is not on `main` at dispatch | closed by the orchestrator, as the task states | the boundary PR `orchestration/boundary-2026-10-11-2` and `gh pr update-branch` before the final audit. The worker runs no `gh pr update-branch` |
+| Push and schedule have no PR range | closed | `DecisionTest.test_every_event_but_pull_request_bootstraps` |
+
+The earlier proofs still fail against the new reader at `a35a751e`: 16 of 16 from a01, and 3 of 3 from a01's revise. a01's fourth revise row targeted the removed quoted-key regex and no longer applies; the lenient-reader row replaces it (validation §4).
+
+## Notes
+
+- The full local `make unit-test` fails in the sandbox the same way on `origin/main`: the same failing ids, none only at this head (validation §5). This module passes under it, and CI's `Run Python unit tests` step is the verdict.
+- The final head's CI and Bot wait are in the RESULT and the main-checkout copy of this report.
+- Understand-Anything hook: did not fire. plan-mode-used: no.
+
+## CompactionDB
+
+`memory add` printed `c62781a9-a65b-4484-925c-383fddb9a114` (validation §6).
+
+cost: n/a
+
+## Amendment 1 (TASK 09:41:42Z, sha256 `4de54fde…`)
+
+The boundary PR 321 merged at 09:40Z, so design `4520b8f0…` and this task id's `implementing_tasks` entry are on `main`; this is the TASK the worker acts on (INV-2), and the 07:35Z one is superseded. The task file changed only in `design_review.receipt` (round 18) and the design-on-main row of the threat table. The copy at `.orchestration/dotfiles-T128-ci-skip-orchestration-a02/task.md` is re-made byte-identical (validation §8). No content change; no `gh pr update-branch` here, as the orchestrator runs it after this RESULT.
diff --git a/.orchestration/dotfiles-T128-ci-skip-orchestration-a02/sandbox.md b/.orchestration/dotfiles-T128-ci-skip-orchestration-a02/sandbox.md
new file mode 100644
index 00000000..caba5ed9
--- /dev/null
+++ b/.orchestration/dotfiles-T128-ci-skip-orchestration-a02/sandbox.md
@@ -0,0 +1,34 @@
+---
+task_id: dotfiles-T128-ci-skip-orchestration-a02
+seat: claude-standard-dot-a003
+permission_gated_commands: 13
+---
+
+# Sandbox record: dotfiles-T128-ci-skip-orchestration-a02
+
+- Period: from the AGMSG-TASK (2026-10-11T07:35:34Z) to the RESULT. Edits, the unit tests, the YAML parse (`--with pyyaml`, offline), ruff, prettier, every proof, the `-v` listings, the full-suite comparison and the commits ran inside the sandbox (`git -c commit.gpgsign=false`, `UV_OFFLINE=1`). No `allowed_domains`, no refusal.
+
+`permission_gated_commands` counts every Bash call with `dangerouslyDisableSandbox`, one per call (`agmsg-dispatch` included; each Bot loop is one call). This copy was written before #2, so #2 to #7 are counted in advance; the main-checkout copy states the final count.
+
+| # | Command | Step 4 case |
+|--:|---|---|
+| 1 | `cd ~/Workspace/dotfiles && uv run --no-project .claude/hooks/contextdb_cli.py memory add …` | main-checkout `memory add` |
+| 2 | the authorized push (`406ca746`, `a35a751e` and this evidence) | `git push` |
+| 3 | `gh pr checks 320 … --watch` on the pushed head (background, exit status joined) | `gh` |
+| 4 | Bot wait on the pushed head, `scratchpad/bot-wait.sh`, timed from the push (the PR is already ready) | `gh` only |
+| 5 | final recheck of reviews, review comments and the connector summary right before the RESULT (`gh` only) | `gh` |
+| 6 | the masked copy of the five evidence files to the TASK's `expected_*` paths in the main checkout | artifact copy with the repository masker |
+| 7 | `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T128-ci-skip-orchestration-a02 …` | `agmsg-dispatch` |
+
+## Amendment 1
+
+Calls #1–#7 ran for the first RESULT (main-checkout copy). The task copy commit was made inside the sandbox; only the push leaves it. These six are counted in advance in this copy; the main-checkout copy states the final count.
+
+| # | Command | Step 4 case |
+|--:|---|---|
+| A1 | the authorized push (the Amendment 1 task copy and this evidence) | `git push` |
+| A2 | `gh pr checks 320 … --watch` on the pushed head (background, exit status joined) | `gh` |
+| A3 | Bot wait on the pushed head, `scratchpad/bot-wait.sh`, timed from the push | `gh` only |
+| A4 | final recheck of reviews, review comments and the connector summary right before the RESULT (`gh` only) | `gh` |
+| A5 | the masked copy of the five evidence files to the TASK's `expected_*` paths in the main checkout | artifact copy with the repository masker |
+| A6 | `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T128-ci-skip-orchestration-a02 …` | `agmsg-dispatch` |
diff --git a/.orchestration/dotfiles-T128-ci-skip-orchestration-a02/task.md b/.orchestration/dotfiles-T128-ci-skip-orchestration-a02/task.md
new file mode 100644
index 00000000..0f14b2a0
--- /dev/null
+++ b/.orchestration/dotfiles-T128-ci-skip-orchestration-a02/task.md
@@ -0,0 +1,78 @@
+---
+format: 2
+task_id: dotfiles-T128-ci-skip-orchestration-a02
+kind: code
+security: true
+design_review:
+  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round18.md
+  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
+allowed_files:
+  - .github/workflows/remote.yaml
+  - .github/workflows/test.yaml
+  - tests/unit/test_workflow_orchestration_skip.py
+invariants:
+  INV-2: "a PR is mergeable only within the caps the CI regime job enforces from main's workflow (at most 15 changed files outside .orchestration/, 500 added lines outside tests/, .orchestration/ and the data list scripts/legacy-task-ids.txt, and 1000 added lines under tests/), and its task.md invariants equal the design's as a set of ids and byte-for-byte as sentences (the design read from main, never from the PR; a task id ending in -contract-a01 is compared with its implementing task's entry); the design file must be on main (through a boundary PR) before the implementing TASK is dispatched and the regime job fails closed when the design named by task.md is absent from main; an .orchestration-only PR runs no bootstrap or test matrix and every required check context still reports success (each required workflow decides inside its jobs, as test.yaml's changes job does), so a boundary PR merges in minutes; exceeding a cap is a split, never a finding to disposition (the cap changes the unit of work: T116 +529 and T118 +881 would have been split)"
+threat_table:
+  - control: the PR edits the workflow files themselves
+    disposition: "residual: a pull_request workflow is PR-controlled (design R8); compensating control: V1c's regime job refuses workflow edits outside a design-tier task, operator routing of workflow changes, the design-tier audit; tests/unit/test_workflow_security.py pins SHAs, permissions and persist-credentials"
+  - control: the decision step misclassifies a diff as .orchestration-only
+    disposition: "closed: the classification is one git diff --name-only over the merge-base range with a single grep for a path outside .orchestration/; tests: a mixed diff, a pure .orchestration diff, a renamed file, a deleted file"
+  - control: a required job is skipped (a job-level if, or needs on a job that failed or was skipped)
+    disposition: "closed: GitHub reports a skipped job as Success even for a required check (fail-open: actions docs, control-jobs-with-conditions and workflow-syntax jobs.needs), so no required job carries a job-level if or a needs; each bootstrap job, and test.yaml's test job, decides in its own first step and gates its heavy steps on that step's output; test asserts no job-level if and no needs on any required context's job, read by the fail-closed reader of the row below (an unsupported key form fails the test instead of reading as absent)"
+  - control: the decision step itself fails (git fetch, a script error)
+    disposition: "closed: an in-job decision step that fails fails the required context (fail-closed) instead of skipping it; test asserts the decision step has no continue-on-error and that every heavy step's if reads its output, read by the same fail-closed reader"
+  - control: the hand-written workflow reader misses a valid YAML form (quoted, escaped or spaced keys, flow mappings)
+    disposition: "closed: the reader fails closed: inside jobs:, a job name, a job key or a step key that is not the plain form name: (lower-case letters, digits, _ and -, the colon immediately after; no quotes, no escapes, no flow mapping; comments and blank lines aside) raises and fails every structural test, so an unsupported form can never read as no if; tests: if : false, \"\\x69f\": false, continue-on-error : true and a step written as the flow mapping { if: false } each fail the structural tests (a real YAML parser replaces the reader only if the test environment gains one; this task adds no dependency)"
+  - control: the task's invariant sentence and map entry are not on main at dispatch (INV-2)
+    disposition: "closed: INV-2 requires the design on main before the implementing TASK is dispatched; the design that names this task id (dotfiles-T128-ci-skip-orchestration-a02: [INV-2]) lands on main through the boundary PR orchestration/boundary-2026-10-11-2, and the TASK the worker acts on is the amendment TASK the orchestrator sends after that merge (the 07:38Z TASK predates it and is superseded; the acceptance record names both); this PR takes that main with gh pr update-branch and merges only after its final audit on that head; test: none (the acceptance record pastes git show origin/main:.orchestration/tasks/dotfiles-T128-regime-v3-a01.md | sha256sum and the two TASK ids)"
+  - control: push and schedule events have no PR range
+    disposition: "closed: should_run is true for every event but pull_request; test asserts it"
+after: []
+reset_of: [dotfiles-T128-ci-skip-orchestration-a01]
+premises:
+  - claim: "the seven required checks are validate, test (3 legs) and public-bootstrap (3 legs); a required check skipped at the workflow level stays pending and blocks the merge, while a job skipped by a job-level if or by needs on a failed or skipped job reports Success even when required (fail-open), so each required job decides inside itself with a step that fails closed"
+    command: "gh api repos/mryfmo/dotfiles/rulesets/24397953 --jq '[.rules[]|select(.type==\"required_status_checks\")|.parameters.required_status_checks[].context]|join(\"; \")'; sed -n 1,12p .github/workflows/test.yaml"
+    output: |-
+      validate; test (ubuntu-24.04, server); test (ubuntu-24.04, client); test (macos-14, client); public-bootstrap (ubuntu-24.04, server); public-bootstrap (ubuntu-24.04, client); public-bootstrap (macos-14, client)
+      name: Unit test
+      
+      on:
+        # Required checks must always report a final status for PRs into `main`.
+        # Do not add workflow-level path or branch filters here: GitHub can leave
+        # skipped required checks in a pending state and block merges.
+        # Keep this workflow unconditional and decide inside jobs whether the full
+        # test matrix is necessary for the current diff.
+        push:
+          branches: [main]
+        pull_request:
+          branches: [main]
+  - claim: "boundary PR 316 (.orchestration files only) ran the three public-bootstrap legs on each of its six heads, 7 to 9 minutes per leg on the final head c264c7d1 plus queue time; an .orchestration-only PR needs none of them"
+    command: "gh api repos/mryfmo/dotfiles/commits/c264c7d1/check-runs --paginate --jq '.check_runs[]|select(.name|startswith(\"public-bootstrap\"))|[.name,.started_at,.completed_at]|@tsv'; gh api repos/mryfmo/dotfiles/pulls/316/commits --paginate --jq 'length'"
+    output: |-
+      public-bootstrap (macos-14, client)	2026-10-10T23:51:13Z	2026-10-10T23:58:20Z
+      public-bootstrap (ubuntu-24.04, client)	2026-10-10T23:51:09Z	2026-10-11T00:00:07Z
+      public-bootstrap (ubuntu-24.04, server)	2026-10-10T23:51:09Z	2026-10-10T23:58:50Z
+      6
+---
+
+# AGMSG-TASK dotfiles-T128-ci-skip-orchestration-a02 — plan 006 A201: an .orchestration-only PR runs no bootstrap or test matrix (reset of a01)
+
+Phase A5 (design tier: workflows); the reset successor of `dotfiles-T128-ci-skip-orchestration-a01` under INV-6 (reset record `.orchestration/acceptance/dotfiles-T128-ci-skip-orchestration-a01-design-reset.md`). The same Claude seat (`claude-standard-dot-a003`), the same branch `feat/ci-skip-orchestration` and PR #320, continuing from `dc4e6c37`; the implementation on that head stays. Implements INV-2's CI clause (design v16, unchanged sentence).
+
+## What to build
+
+1. `.github/workflows/remote.yaml`: each of `public-bootstrap` and `private-bootstrap` computes `should_run` in its own first step (no separate `changes` job and no `needs`: a job that `needs` a failed or skipped job is skipped and a skipped required job reports Success) for the event: on `pull_request` from the base-to-head diff (`false` only when every changed path is under `.orchestration/`), and on `push`, `schedule` and `workflow_dispatch` always `true` (those events have no PR range to judge and must keep bootstrapping `main`). `public-bootstrap` and `private-bootstrap` keep their job names and matrix; every heavy step carries a step-level `if: steps.decide.outputs.should_run == 'true'` (never a job-level `if` or a `needs`, which turn a failed decision into a passing required check; never an early-exit step, which cannot skip later steps), so the job completes with success and reports its context on an `.orchestration`-only PR. `test.yaml`'s `test` job already gates its heavy steps but through `needs: changes` (fail-open today, on main): it takes the same in-job decision step and drops the `needs`; the `changes` job goes when nothing needs it; a `main-tests` job, when present (V0 is parked and A5 precedes it, so the test must not require the job), takes the same in-job decision with step-level `if`s. The steps keep the pins `tests/unit/test_workflow_security.py` asserts (action SHAs, `permissions`, `persist-credentials: false`); `agent-assets.yml` is cheap and unchanged.
+2. `tests/unit/test_workflow_orchestration_skip.py`: YAML-level checks that every required context's job has no job-level `if` and no `needs`, that each carries the decision step without `continue-on-error`, that each heavy step of `public-bootstrap`, `private-bootstrap` and, when the job exists, `main-tests` carries the `should_run` (or `should_test`) step-level `if`, that the decision yields `true` for `push`, `schedule` and `workflow_dispatch`, and that the context names equal a named constant `REQUIRED_CONTEXTS` that copies premise 1's seven contexts (a unit test cannot read the ruleset; the constant is what changes when the ruleset changes); each fails when its rule is removed. The reader fails closed: inside `jobs:`, a job name, a job key or a step key that is not the plain form `name:` (lower-case letters, digits, `_` and `-`, the colon immediately after; no quotes, no escapes, no flow mapping; comments and blank lines aside) raises, so an unsupported form fails every structural test instead of reading as "no `if`"; the test environment has no YAML parser (`make unit-test` runs bare `uv run python`) and this task adds no dependency. `tests/unit/test_workflow_security.py` must keep passing.
+3. Validation: YAML-parse the workflows; the module under `make unit-test`; the four unsupported-form mutations (`if : false`, `"\x69f": false`, `continue-on-error : true`, a step written as `{ if: false }`) each fail the structural tests, pasted into validation.md; after the merge the orchestrator pastes `gh pr checks` timings of the next `.orchestration`-only PR into the acceptance record (A201's completion condition: ≤ 10 minutes with every required check reported).
+
+## History
+
+a01: Amendment 1 (2026-10-11 05:50Z, after the worker's PONG with the GitHub doc evidence) turned the `changes`-job pattern into the in-job fail-closed decision: the two rows on skipped jobs and failed decision steps, items 1 and 2 and premise 1 reworded, `test.yaml`'s `test` job fixed in the same PR. Revise round 1 (`dc4e6c37`) closed rename detection (`--no-renames`) and quoted keys. The audit of `dc4e6c37` found the reader class a second time (spaced and escaped keys, flow mappings) and re-raised the design-on-main prerequisite; this reset closes the reader class as a whole (fail closed on any unsupported form) and the design-on-main prerequisite (the two new rows), and changes nothing else.
+
+## First commit
+
+Copy this task file byte-identical to `.orchestration/dotfiles-T128-ci-skip-orchestration-a02/task.md` (the a01 directory stays as it is); evidence beside it, on the same branch from `dc4e6c37`. Phase A5 of plan 006; dormant contracts are withdrawn from the pattern, so this PR carries its tests directly.
+
+## Completion
+
+PR #320 stays the PR (no new draft); once the boundary PR `orchestration/boundary-2026-10-11-2` is merged, `gh pr update-branch` before the final audit; CI, Bot wait (`@codex review` if nothing in 10 minutes), artifacts, RESULT via `agmsg-dispatch … claude-deep-dot w5:p1`. max_turns=8. Forbidden: anything outside `allowed_files`; `make update`; thread resolution.
diff --git a/.orchestration/dotfiles-T128-ci-skip-orchestration-a02/validation.md b/.orchestration/dotfiles-T128-ci-skip-orchestration-a02/validation.md
new file mode 100644
index 00000000..c518ed60
--- /dev/null
+++ b/.orchestration/dotfiles-T128-ci-skip-orchestration-a02/validation.md
@@ -0,0 +1,200 @@
+# Validation: dotfiles-T128-ci-skip-orchestration-a02
+
+Every block is the verbatim output of the command shown, run in `.claude/worktrees/worker-f` on `feat/ci-skip-orchestration` (PR #320). This branch copy covers `a35a751e`; the main-checkout copy adds the final head (design INV-8).
+
+## 1. Task file
+
+```
+$ shasum -a 256 ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T128-ci-skip-orchestration-a02.md .orchestration/dotfiles-T128-ci-skip-orchestration-a02/task.md | cut -c1-64
+2c3a5ee2439a4c8e0aa16e0013e9b8acfcbb82fc330b259f7748f34938d5d9bc
+2c3a5ee2439a4c8e0aa16e0013e9b8acfcbb82fc330b259f7748f34938d5d9bc
+```
+
+## 2. Checks at `a35a751e` (task validation: the YAML parse, the module; plus formatting and the security pins)
+
+```
+$ git log --oneline -3; git show --stat --format= a35a751e
+a35a751e test(ci): the workflow reader fails closed on any key form it does not parse
+406ca746 chore(orchestration): task file for dotfiles-T128-ci-skip-orchestration-a02
+dc4e6c37 fix(ci): the unit-test decision lists both sides of a rename; the workflow reader sees quoted keys
+ tests/unit/test_workflow_orchestration_skip.py | 109 ++++++++++++++++---------
+ 1 file changed, 70 insertions(+), 39 deletions(-)
+$ UV_OFFLINE=1 uv run python -m unittest tests.unit.test_workflow_orchestration_skip tests.unit.test_workflow_security 2>&1 | tail -3; ruff format --config ruff.toml --check tests/unit/test_workflow_orchestration_skip.py; ruff check --config ruff.toml tests/unit/test_workflow_orchestration_skip.py
+Ran 21 tests in 4.718s
+
+OK
+1 file already formatted
+All checks passed!
+$ UV_OFFLINE=1 uv run --no-project --with pyyaml python -I -c "import sys, yaml; [print(p, sorted(yaml.safe_load(open(p))[\"jobs\"])) for p in sys.argv[1:]]" .github/workflows/remote.yaml .github/workflows/test.yaml .github/workflows/agent-assets.yml
+.github/workflows/remote.yaml ['private-bootstrap', 'public-bootstrap']
+.github/workflows/test.yaml ['test']
+.github/workflows/agent-assets.yml ['validate']
+```
+
+## 3. The unsupported forms (`scratchpad/mutate-a5-a02.sh` at `a35a751e`, a `git archive HEAD` copy)
+
+Each row inserts one form into a workflow. "YAML reads" is GitHub's view of it, from PyYAML on the mutated file: every form hides a real `if` or `continue-on-error`. The next lines run `RequiredContextsTest`, `DecisionStepTest` and `DecisionTest` (13 tests) and count the summary and `ValueError` lines. `errors=N` counts failing subTests, not tests. The task's four forms come first; the two positional rows (a shifted job body, a shifted step item) were found while checking the reader.
+
+```
+== unsupported form: spaced-job-key (remote.yaml): if : false
+   YAML reads: False
+   1 FAILED (errors=12)
+   1 Ran 13 tests in 1.732s
+  12 ValueError: unsupported key form inside jobs: '    if : false'
+== unsupported form: escaped-job-key (remote.yaml): "\x69f": false
+   YAML reads: False
+   1 FAILED (errors=12)
+   1 Ran 13 tests in 2.220s
+  12 ValueError: unsupported key form inside jobs: '    "\\x69f": false'
+== unsupported form: spaced-step-key (test.yaml): continue-on-error : true
+   YAML reads: True
+   1 FAILED (errors=9)
+   1 Ran 13 tests in 2.040s
+   9 ValueError: unsupported key form inside jobs: '        continue-on-error : true'
+== unsupported form: shifted-job-body (agent-assets.yml): if: false|runs-on: ubuntu-24.04
+   YAML reads: False
+   1 FAILED (errors=3)
+   1 Ran 13 tests in 3.463s
+   3 ValueError: unsupported job body indentation inside jobs: '      if: false'
+== unsupported form: shifted-step-item (remote.yaml): -   name: Decide whether the diff needs a bootstrap|continue-on-error: true
+   YAML reads: True
+   1 FAILED (errors=12)
+   1 Ran 13 tests in 1.583s
+  12 ValueError: unsupported key form inside jobs: '      -   name: Decide whether the diff needs a bootstrap'
+== unsupported form: flow-mapping-step (remote.yaml): - { if: false }
+   YAML reads: {'if': False}
+   1 FAILED (errors=12)
+   1 Ran 13 tests in 1.550s
+  12 ValueError: unsupported key form inside jobs: '      - { if: false }'
+== reader made lenient again (plain_key returns instead of raising) -> test_the_reader_fails_closed_on_unsupported_key_forms
+FAIL: test_the_reader_fails_closed_on_unsupported_key_forms (tests.unit.test_workflow_orchestration_skip.RequiredContextsTest.test_the_reader_fails_closed_on_unsupported_key_forms) (form='spaced job key')
+AssertionError: ValueError not raised
+FAIL: test_the_reader_fails_closed_on_unsupported_key_forms (tests.unit.test_workflow_orchestration_skip.RequiredContextsTest.test_the_reader_fails_closed_on_unsupported_key_forms) (form='escaped job key')
+== restored: OK
+== reader without the job-body indentation check -> test_the_reader_fails_closed_on_unsupported_key_forms
+FAIL: test_the_reader_fails_closed_on_unsupported_key_forms (tests.unit.test_workflow_orchestration_skip.RequiredContextsTest.test_the_reader_fails_closed_on_unsupported_key_forms) (form='shifted job body')
+AssertionError: ValueError not raised
+FAILED (failures=1)
+```
+
+The tests that still pass under each form (the same harness with `-v`). Each is either the reader test itself (it rebuilds its own forms), or a test that never reads the mutated job's keys through `jobs()`: the context-name check reads job names by regex, and the rest read the other workflow file.
+
+```
+== unsupported form: spaced-job-key (remote.yaml): if : false
+test_the_reader_fails_closed_on_unsupported_key_forms ... ok
+test_the_required_contexts_are_the_workflows_jobs ... ok
+test_a_main_tests_job_when_present_decides_in_itself ... ok
+test_the_unit_test_decision_ignores_renames ... ok
+test_the_unit_test_decision_skips_an_orchestration_only_diff ... ok
+== unsupported form: escaped-job-key (remote.yaml): "\x69f": false
+test_the_reader_fails_closed_on_unsupported_key_forms ... ok
+test_the_required_contexts_are_the_workflows_jobs ... ok
+test_a_main_tests_job_when_present_decides_in_itself ... ok
+test_the_unit_test_decision_ignores_renames ... ok
+test_the_unit_test_decision_skips_an_orchestration_only_diff ... ok
+== unsupported form: spaced-step-key (test.yaml): continue-on-error : true
+test_the_reader_fails_closed_on_unsupported_key_forms ... ok
+test_the_required_contexts_are_the_workflows_jobs ... ok
+test_both_bootstrap_jobs_decide_with_the_same_script ... ok
+test_a_pull_request_skips_the_bootstrap_only_for_an_orchestration_only_diff ... ok
+test_every_event_but_pull_request_bootstraps ... ok
+== unsupported form: shifted-job-body (agent-assets.yml): if: false|runs-on: ubuntu-24.04
+test_no_job_is_left_for_a_required_job_to_need ... ok
+test_the_reader_fails_closed_on_unsupported_key_forms ... ok
+test_a_main_tests_job_when_present_decides_in_itself ... ok
+test_both_bootstrap_jobs_decide_with_the_same_script ... ok
+test_each_deciding_job_decides_after_its_checkout_and_fails_closed ... ok
+test_every_heavy_step_carries_its_jobs_decision ... ok
+test_a_pull_request_skips_the_bootstrap_only_for_an_orchestration_only_diff ... ok
+test_every_event_but_pull_request_bootstraps ... ok
+test_the_decision_survives_a_base_that_moved_after_the_checkout ... ok
+test_the_unit_test_decision_ignores_renames ... ok
+test_the_unit_test_decision_skips_an_orchestration_only_diff ... ok
+== unsupported form: shifted-step-item (remote.yaml): -   name: Decide whether the diff needs a bootstrap|continue-on-error: true
+test_the_reader_fails_closed_on_unsupported_key_forms ... ok
+test_the_required_contexts_are_the_workflows_jobs ... ok
+test_a_main_tests_job_when_present_decides_in_itself ... ok
+test_the_unit_test_decision_ignores_renames ... ok
+test_the_unit_test_decision_skips_an_orchestration_only_diff ... ok
+== unsupported form: flow-mapping-step (remote.yaml): - { if: false }
+test_the_reader_fails_closed_on_unsupported_key_forms ... ok
+test_the_required_contexts_are_the_workflows_jobs ... ok
+test_a_main_tests_job_when_present_decides_in_itself ... ok
+test_the_unit_test_decision_ignores_renames ... ok
+test_the_unit_test_decision_skips_an_orchestration_only_diff ... ok
+== restored: OK
+```
+
+## 4. The earlier proofs against the new reader (`scratchpad/mutate-a5.sh` and `scratchpad/mutate-a5-r1.sh` at `a35a751e`)
+
+```
+$ awk '/^== broken rule/{if(n!="")print n, f; n=$4; f="no"} /^(FAIL|ERROR):/{f="fails"} END{print n, f}' mutate-a5.log mutate-a5-r1.log; grep -E 'DID NOT APPLY|restored' mutate-a5.log mutate-a5-r1.log
+public-bootstrap-step-ungated fails
+private-deploy-key-ungated fails
+unit-test-step-ungated fails
+needs-on-a-required-job fails
+job-level-if-on-a-required-job fails
+changes-job-back fails
+decision-continue-on-error fails
+decision-before-checkout-history fails
+private-script-drift fails
+non-pr-events-judged fails
+renames-collapsed fails
+classification-inverted fails
+unit-test-decision-ignores-orchestration fails
+required-leg-dropped fails
+shallow-base-fetch-remote fails
+shallow-base-fetch-test fails
+unit-test-diff-detects-renames fails
+quoted-job-level-if fails
+quoted-continue-on-error-on-decide fails
+== reader-sees-bare-keys-only: MUTATION DID NOT APPLY
+== restored: OK
+== restored: OK
+```
+
+`reader-sees-bare-keys-only` targeted the quoted-key regex that this commit removes; the lenient-reader row of §3 replaces it.
+
+## 5. The full suite locally, this head against `origin/main` (`git archive origin/main` copy; failing ids from the `FAIL:`/`ERROR:` lines)
+
+```
+$ UV_OFFLINE=1 make unit-test   # at this head; the same discover in the origin/main copy; then comm on the sorted ids
+base (origin/main b896d9bc): FAILED (failures=114, errors=103, skipped=2)  failing ids: 188
+head (a35a751e, make unit-test): FAILED (failures=114, errors=103, skipped=2) (make exits 2)  failing ids: 188
+only at head:
+only at base:
+this module under make unit-test:
+test_a_main_tests_job_when_present_decides_in_itself ... ok
+test_both_bootstrap_jobs_decide_with_the_same_script ... ok
+test_each_deciding_job_decides_after_its_checkout_and_fails_closed ... ok
+test_every_heavy_step_carries_its_jobs_decision ... ok
+test_a_pull_request_skips_the_bootstrap_only_for_an_orchestration_only_diff ... ok
+test_every_event_but_pull_request_bootstraps ... ok
+test_the_decision_survives_a_base_that_moved_after_the_checkout ... ok
+test_the_unit_test_decision_ignores_renames ... ok
+test_the_unit_test_decision_skips_an_orchestration_only_diff ... ok
+test_no_job_is_left_for_a_required_job_to_need ... ok
+test_no_required_contexts_job_has_a_job_level_if_or_needs ... ok
+test_the_reader_fails_closed_on_unsupported_key_forms ... ok
+test_the_required_contexts_are_the_workflows_jobs ... ok
+```
+
+The local failures are the sandbox's, as on a01 (test commits that inherit the global signing setting, `mktemp` outside the writable paths, no pty devices, no local `main` ref). They are identical on `origin/main`. CI's `Run Python unit tests` step is the verdict.
+
+## 6. CompactionDB (main checkout, outside the sandbox through the permission gate)
+
+```
+$ cd ~/Workspace/dotfiles && uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content '[memory:decision] dotfiles-T128-ci-skip-orchestration-a02 …'
+c62781a9-a65b-4484-925c-383fddb9a114
+```
+
+## 8. Amendment 1: the task copy
+
+```
+$ shasum -a 256 ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T128-ci-skip-orchestration-a02.md .orchestration/dotfiles-T128-ci-skip-orchestration-a02/task.md | cut -c1-64
+4de54fdec5db667e940365703ee5e16cd1d91f52794c79c75b48aad7eb0a8763
+4de54fdec5db667e940365703ee5e16cd1d91f52794c79c75b48aad7eb0a8763
+$ git diff --stat HEAD -- .orchestration/dotfiles-T128-ci-skip-orchestration-a02/task.md
+ .orchestration/dotfiles-T128-ci-skip-orchestration-a02/task.md | 4 ++--
+ 1 file changed, 2 insertions(+), 2 deletions(-)
+```
     1	---
     2	format: 2
     3	reset_of: dotfiles-T128-ci-skip-orchestration-a01
     4	redesign_task: dotfiles-T128-ci-skip-orchestration-a02
     5	design_sha256: 4de54fdec5db667e940365703ee5e16cd1d91f52794c79c75b48aad7eb0a8763
     6	redesign_source: dotfiles-T128-ci-skip-redesign-a01
     7	redesign_seat: claude-review-dot-a001 (review profile, a context other than the task's author)
     8	reason: "design INV-6 on PR 320: two RESULTs (456, 485: revises=1) and one amendment; the second audit (dc4e6c37) found the hand-written workflow reader's class a second time (spaced, escaped and flow-mapping keys after the first audit's quoted keys) and re-raised the design-on-main prerequisite (main at b896d9bc holds neither the task's implementing_tasks entry nor its INV-2 sentence); a further round reaches a threshold, so the rule's path is a reset with a redesign by another context"
     9	---
    10	
    11	# Design reset: dotfiles-T128-ci-skip-orchestration-a01 (PR #320), 2026-10-11
    12	
    13	- **What stops:** task id a01's specification. The branch, PR #320, the worker `claude-standard-dot-a003` and the implementation (in-job fail-closed decision, no `needs`, no job-level `if`, `--no-renames`, the required-context constant) continue under `dotfiles-T128-ci-skip-orchestration-a02`.
    14	- **Why a reset:** the reader finding recurred as a class (quoted keys, then spaced and escaped keys and flow mappings); fixing it form by form is the pattern the operator's rule forbids, and the specification said nothing about unsupported syntax. The design-on-main finding is the orchestrator's: the task was dispatched under plan 006 Phase 0's rule that a boundary is never a dispatch prerequisite, which contradicts INV-2's hashed sentence ("the design file must be on main (through a boundary PR) before the implementing TASK is dispatched"); the auditor is right. The remedy is mechanical: design v16 goes to `main` by the boundary PR `orchestration/boundary-2026-10-11-2` before this PR's final audit, and the plan's Phase 0 rule is corrected to INV-2's text (recorded in plan 006).
    15	- **Redesign:** `dotfiles-T128-ci-skip-redesign-a01` on the review seat produces the whole a02 task file (fail-closed reader row with four mutation tests; the design-on-main row with the boundary PR in `after:`); the orchestrator writes it byte-identical from the receipt and the review seat confirms its hash (`verdict=accept design_sha256=<hash>`), the anchor.
    16	- **Counts carried:** A5 at the reset: tasks 2, amendments 1, questions 0, results 2, revises 1, Bot P0/P1 heads after the first RESULT 0, wall 05:42Z to 07:13Z (1 h 31 min).
    17	- **Waiver:** none.
    18	- **Anchor:** redesign RESULT 496 (`claude-review-dot-a001`, 07:33:43Z, receipt `c55e1585…`, `a02_expected_sha256=2c3a5ee2…`, matched on disk); the review seat's `verdict=accept design_sha256=2c3a5ee2…` is the anchor (confirmed: RESULT 502, 07:37:09Z, byte-for-byte). `after:` stays `[]` (V1 types it as task ids); the boundary dependency is the design-on-main row. The successor ids need `implementing_tasks` entries (v16 maps the a01 ids only): design v17 adds `dotfiles-T128-ci-skip-orchestration-a02: [INV-2]` and `dotfiles-T128-regime-counters-a02: [INV-6]`, reviewed as a pair (round 18) and carried by the next boundary PR.
    19	- **Anchor refresh (08:03Z):** the successor file changed (the design-on-main row now states INV-2's dispatch rule (Bot P1 4240758696 on PR #321)); its hash is now `6457b81f…`; the review seat's round-3 `verdict=accept design_sha256=6457b81f…` re-anchors it (confirmed: RESULT 519, 08:06:34Z).
    20	- **Anchor refresh 3 (08:32Z):** the successor's `design_review.receipt` now names round 18, the first receipt that reviews its map entry (Bot P2 4240827027 on PR #321); hash `4de54fde…`; the review seat's `verdict=accept` on it confirmed: RESULT at 08:31:07Z, round 4.

 exited 1 in 142ms:
mktemp: mkstemp failed on /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T//agmsg-team-list-work.jdGWty: Operation not permitted

mcp: codex_apps/github.fetch (completed)
mcp: codex_apps/github.fetch (completed)
**Assessing token usage and metadata needs**
exec
/bin/zsh -lc "git show 3bafe4f24c80fd1093e2fd5a19d843e5cb7aff5b:.orchestration/dotfiles-T128-ci-skip-orchestration-a01/report.md; git show 3bafe4f24c80fd1093e2fd5a19d843e5cb7aff5b:.orchestration/dotfiles-T128-ci-skip-orchestration-a01/sandbox.md; git show 3bafe4f24c80fd1093e2fd5a19d843e5cb7aff5b:.orchestration/dotfiles-T128-ci-skip-orchestration-a01/validation.md | sed -n '1,165p'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 39ms:
# Report: dotfiles-T128-ci-skip-orchestration-a01

- Seat: `claude-standard-dot-a003` in `.claude/worktrees/worker-f`, branch `feat/ci-skip-orchestration` from `origin/main` `b896d9bc`, PR #320. Plan 006 Phase A5 (INV-2's CI clause), with Amendment 1.
- Task file sha256 `6dd3d682…` checked against the TASK and copied byte-identical in `be935742`; Amendment 1's sha256 `8e9c23da…` checked and re-copied byte-identical in `f7393ee1`. Content commit `9fcd2b04`; evidence `b3f88beb`; Bot fix round 1 `e872f69f`.

## What changed (`9fcd2b04`)

1. `.github/workflows/remote.yaml`: `public-bootstrap` and `private-bootstrap` each decide `should_run` in their own step `decide`, right after the checkout (now `fetch-depth: 0`, still `persist-credentials: false`). On `pull_request` the step diffs `origin/<base>...<head>` with `--no-renames` (both sides of a rename are listed) and writes `false` only when no path is outside `.orchestration/`; an empty diff runs the bootstrap. Every other event writes `true` before any git call. The bootstrap step (public) and the deploy-key and bootstrap steps (private, prefixed to their existing secret gates) carry `steps.decide.outputs.should_run == 'true'`; a notice step reports the skip. Job names and matrices are unchanged; no `needs`, no job-level `if`.
2. `.github/workflows/test.yaml`: the `changes` job is gone and `test` no longer `needs` it. Its filter script moved, unchanged but for its comment, into the `test` job's own step `decide` after the checkout (now `fetch-depth: 0`); every `needs.changes.outputs.*` read became `steps.decide.outputs.*`. Lines 1–12 and the ubuntu-26.04 canary's job-level `continue-on-error` are unchanged.
3. `tests/unit/test_workflow_orchestration_skip.py` (stdlib only; PyYAML is not in the unit-test environment): the context names equal `REQUIRED_CONTEXTS` (premise 1's seven); no required context's job has a job-level `if` or `needs`, and no `changes` job is left; each deciding job's step `decide` follows a full-history, credential-free checkout and has no `continue-on-error` and no `if`; every heavy step carries its job's gate; both bootstrap jobs run the same script; a `main-tests` job, when present, decides in itself. The decision scripts are extracted from the workflows and run against a scratch repository: `push`, `schedule`, `workflow_dispatch` → `true`; `pull_request` with an `.orchestration`-only diff → `false`, a mixed diff, a rename out of `home/`, a deletion outside `.orchestration/`, an empty diff → `true`, a deletion inside → `false`; test.yaml's decision → `should_test=false` for `.orchestration` only, `true` for `home/`.

## Threat table (the completion condition)

| Row | Disposition | Where |
|---|---|---|
| The PR edits the workflow files themselves | residual, as the task states | `tests/unit/test_workflow_security.py` passes unchanged (validation §1) |
| The decision step misclassifies a diff | closed | `DecisionTest.test_a_pull_request_skips_the_bootstrap_only_for_an_orchestration_only_diff` (mixed, pure, renamed, deleted in and out, empty), `DecisionTest.test_the_unit_test_decision_skips_an_orchestration_only_diff`; since the revise, `DecisionTest.test_the_unit_test_decision_ignores_renames` |
| A required job is skipped (job-level `if`, or `needs`) | closed | `RequiredContextsTest.test_no_required_contexts_job_has_a_job_level_if_or_needs`, `…test_no_job_is_left_for_a_required_job_to_need`, `…test_the_required_contexts_are_the_workflows_jobs`; since the revise, `RequiredContextsTest.test_structural_tests_see_quoted_keys` (a quoted key no longer hides a job-level `if`) |
| The decision step itself fails | closed | `DecisionStepTest.test_each_deciding_job_decides_after_its_checkout_and_fails_closed`, `…test_every_heavy_step_carries_its_jobs_decision`; since `e872f69f` a base that moved after the checkout no longer fails it: `DecisionTest.test_the_decision_survives_a_base_that_moved_after_the_checkout`; since the revise, `RequiredContextsTest.test_structural_tests_see_quoted_keys` (a quoted `continue-on-error` no longer hides) |
| Push and schedule have no PR range | closed | `DecisionTest.test_every_event_but_pull_request_bootstraps` |

Each closing test fails when its rule is broken: 16 of 16 mutations in a `git archive HEAD` copy at `e872f69f` (validation §8; 14 of 14 at `9fcd2b04`, §3).

## CI and Bot (head `9fcd2b04`)

- CI: 13 of 13 pass, the seven required contexts among them; on this mixed diff the decision steps succeeded and the bootstrap and unit-test steps ran (validation §5). `private-bootstrap`'s deploy-key and bootstrap steps were skipped by their existing secret gate, as on PR 316 (≈12 s per leg there too).
- Bot round 1: the connector summary shows Code Review ✅ Completed at 05:52:35Z and Security Review ✅ Completed at 05:55:43Z on `9fcd2b0`, with 👍 at 05:55Z; no review object and no review comment. No fix round.

## Bot fix round 1 (`e872f69f`)

- Bot round 2, on the evidence head `b3f88beb` (review 5482144676, 06:15:10Z): thread 4240499289 (P2, `remote.yaml` line 61): when `main` moves after the job's checkout, `git fetch --depth=1` makes the new base tip a shallow boundary, the three-dot diff finds no merge base, and the fail-closed step fails all three required contexts → `fixed:e872f69f`.
- Reproduced before the fix in a scratch repository (validation §8): `fatal: origin/main...<head>: no merge base`, rc 128, with `.git/shallow` written; a full fetch gives the PR's own path. Root cause shared by three fetches: both remote.yaml decision steps and the test.yaml step, which inherited `--depth=1` from main's `changes` job, where a failure skipped the tests (fail-open) instead of failing them. All three now fetch the base in full; the checkout already holds the full history, so the fetch transfers only the new base commits.
- The new test moves `origin/main` after the pull request head is built and runs both workflows' decision scripts; putting `--depth=1` back fails it in either file (validation §8).
- The final head's CI and Bot wait are in the RESULT and the main-checkout copy of this report.

## Notes for the orchestrator

- Outside `allowed_files`, stale after this PR: SKILL.md line 71 says "the `changes` job skips the test matrix for an `.orchestration`-only diff, and the ruleset accepts the resulting `skipped` required checks". That is the fail-open mechanism this PR removes; the checks now report success from a completed job.
- The step `decide` now runs on every matrix leg, macOS included, so the remote.yaml script avoids `mapfile` and empty-array expansion (bash 3.2).
- A201's completion condition (≤ 10 minutes on the next `.orchestration`-only PR) is the orchestrator's post-merge check; this PR's own diff is mixed and ran the full matrix.
- Understand-Anything hook: did not fire. plan-mode-used: no.

## CompactionDB

`memory add` printed `a48481dc-7c94-40a9-9300-b01cafb77a48` (validation §6).

cost: n/a

## Revise round 1 (ACCEPTANCE 06:44:36Z, audit of `d6343494`: incorrect; `previous_head=d6343494`)

One commit, recorded in `revise.yaml` beside this report; the module has no `WorkflowOrchestrationSkipTest` class, so the two checks live in the classes that own their rule:

1. P2 `test.yaml:98`: the unit-test decision kept rename detection, so moving `home/a` to `.orchestration/a` listed only the destination and gave `should_test=false`. Its diff now runs with `--no-renames`, as the bootstrap decision's does → `DecisionTest.test_the_unit_test_decision_ignores_renames` moves `home/a` into `.orchestration/` and expects `should_test=true`.
2. P2 `tests/…:67`: the hand-written reader matched bare keys only, so a quoted `'if'` or `'continue-on-error'` slipped past every structural test. It now reads a quoted key, or a quoted job name, like a bare one, as YAML does (no PyYAML in the unit-test environment; the docstring names the block-style-only limit) → `RequiredContextsTest.test_structural_tests_see_quoted_keys` parses `remote.yaml` with a quoted job name, a quoted job-level `"if"` and a quoted `'continue-on-error'` on the decision step.

The two orchestration findings (the design-on-main deviation, the sweep's freshness) are the orchestrator's, as the ACCEPTANCE says. Each fix fails its test when broken, and the quoted-key mutations the audit describes now fail the existing structural tests: 4 of 4 (validation §9). The module runs 21 tests with `test_workflow_security`, OK. Threat-table rows 2 to 4 now name these tests beside the earlier ones. CompactionDB: `f6fe6ff0-f80d-4938-b15c-a66e1efd5d53`. The final head's CI and Bot wait are in the RESULT and the main-checkout copy of this report.
---
task_id: dotfiles-T128-ci-skip-orchestration-a01
seat: claude-standard-dot-a003
permission_gated_commands: 34
---

# Sandbox record: dotfiles-T128-ci-skip-orchestration-a01

- Period: from the AGMSG-TASK (2026-10-11T05:42:10Z) to the RESULT. Edits, the unit tests, the YAML parse, prettier, ruff, the removal proofs, the baseline comparison and the local premise (`sed -n 1,12p`) ran inside the sandbox; commits use `git -c commit.gpgsign=false`; `uv` ran with `UV_OFFLINE=1`. No `allowed_domains`.
- One permission-gate denial, not reworked: a sandboxed command that held `rm -rf "$P"` on a variable path was denied; the next run used `mktemp -d` scratch directories and no removal.

`permission_gated_commands` counts every Bash call with `dangerouslyDisableSandbox`, one per call (`agmsg-dispatch` included; each Bot loop is one call). The branch copy counts the planned calls 19–24; the main-checkout copy states the final count.

| # | Command | Step 4 case |
|--:|---|---|
| 1 | the authorized push (`be935742`) | `git push` |
| 2 | `gh pr create --draft` (#320) | `gh` |
| 3 | `agmsg-dispatch … AGMSG-PONG v1 …` (the fail-open evidence, default proposed) | `agmsg-dispatch` |
| 4 | the authorized push (`f7393ee1`, `9fcd2b04`) | `git push` |
| 5 | `gh pr ready 320` | `gh` |
| 6 | `gh pr checks 320 … --watch` on `9fcd2b04` (background, exit status joined) | `gh` |
| 7 | Bot wait on `9fcd2b04`, timed from `gh pr ready` (background) | `gh` only |
| 8 | the premises (`gh api` ruleset, PR 316 check runs and commits), with `echo` headers | `gh` |
| 9 | `cd ~/Workspace/dotfiles && uv run --no-project .claude/hooks/contextdb_cli.py memory add …` | main-checkout `memory add` |
| 10 | `gh api` reviews, review comments, issue comments and reactions of PR 320 | `gh` |
| 11 | `gh api` the connector summary comment's body and the reactions | `gh` |
| 12 | wait for the connector's security review row on `9fcd2b04` (background) | `gh` only |
| 13 | `gh api` step conclusions of three `9fcd2b04` jobs and PR 316's private-bootstrap legs | `gh` |
| 14 | the authorized push (`b3f88beb`, the first evidence) | `git push` |
| 15 | `gh pr checks 320 … --watch` on `b3f88beb` (background) | `gh` |
| 16 | Bot wait on `b3f88beb`, `scratchpad/bot-wait.sh` (background) | `gh` only |
| 17 | `gh api` thread 4240499289 and the PR's reviews (a `--jq` error ended it, exit 1; #18 re-read them) | `gh` |
| 18 | `gh api` the body and diff hunk of thread 4240499289 and the body of review 5482144676 | `gh` |
| 19 | the authorized push (`e872f69f`, Bot fix round 1, and this evidence) | `git push` |
| 20 | `gh pr checks 320 … --watch` on the final head (background, exit status joined) | `gh` |
| 21 | Bot wait on the final head, `scratchpad/bot-wait.sh` (background) | `gh` only |
| 22 | the masked copy of the five evidence files to the TASK's `expected_*` paths in the main checkout | artifact copy with the repository masker |
| 23 | final recheck of reviews, review comments and the connector summary right before the RESULT (`gh api` only) | `gh` |
| 24 | `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T128-ci-skip-orchestration-a01 …` | `agmsg-dispatch` |

## Revise round 1

Calls #1–#27 are the first round's final count (main-checkout copy of the first RESULT). The revise commit was made inside the sandbox with `git -c commit.gpgsign=false`; only the push leaves it. The count above is 27 plus these 7, counted in advance from R2 on in this copy; the main-checkout copy states the final count.

| # | Command | Step 4 case |
|--:|---|---|
| R1 | `cd ~/Workspace/dotfiles && uv run --no-project .claude/hooks/contextdb_cli.py memory add …` | main-checkout `memory add` |
| R2 | the authorized push (the revise commit) | `git push` |
| R3 | `gh pr checks 320 … --watch` on the revise head (background, exit status joined) | `gh` |
| R4 | Bot wait on the revise head, `scratchpad/bot-wait.sh` (background) | `gh` only |
| R5 | final recheck of reviews, review comments and the connector summary right before the RESULT (`gh` only) | `gh` |
| R6 | the masked copy of the five evidence files to the TASK's `expected_*` paths in the main checkout | artifact copy with the repository masker |
| R7 | `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T128-ci-skip-orchestration-a01 …` | `agmsg-dispatch` |
# Validation: dotfiles-T128-ci-skip-orchestration-a01

Every block is the verbatim output of the command shown, run in `.claude/worktrees/worker-f` on `feat/ci-skip-orchestration` (PR #320). This branch copy covers heads through the revise commit (§1–§7 at `9fcd2b04`, §8 the Bot fix round at `e872f69f`, §9 revise round 1); the main-checkout copy adds the final heads (design INV-8).

## 1. Checks at `9fcd2b04` (task validation: the YAML parse, the module under `make unit-test`; plus formatting)

```
$ git log --oneline -4; git status --porcelain | wc -l
9fcd2b04 feat(ci): an .orchestration-only PR runs no bootstrap or test matrix
f7393ee1 chore(orchestration): task file for dotfiles-T128-ci-skip-orchestration-a01, Amendment 1
be935742 chore(orchestration): task file for dotfiles-T128-ci-skip-orchestration-a01
b896d9bc chore(orchestration): boundary commit 2026-10-11 (regime v3 design accepted) (#316)
       0
$ UV_OFFLINE=1 make unit-test 2>&1 | grep -E "test_workflow_orchestration_skip|^Ran|^OK|^FAILED" | sed -E "s/ \(tests[^)]*\)//"
test_a_main_tests_job_when_present_decides_in_itself (test_workflow_orchestration_skip.DecisionStepTest.test_a_main_tests_job_when_present_decides_in_itself) ... ok
test_both_bootstrap_jobs_decide_with_the_same_script (test_workflow_orchestration_skip.DecisionStepTest.test_both_bootstrap_jobs_decide_with_the_same_script) ... ok
test_each_deciding_job_decides_after_its_checkout_and_fails_closed (test_workflow_orchestration_skip.DecisionStepTest.test_each_deciding_job_decides_after_its_checkout_and_fails_closed) ... ok
test_every_heavy_step_carries_its_jobs_decision (test_workflow_orchestration_skip.DecisionStepTest.test_every_heavy_step_carries_its_jobs_decision) ... ok
test_a_pull_request_skips_the_bootstrap_only_for_an_orchestration_only_diff (test_workflow_orchestration_skip.DecisionTest.test_a_pull_request_skips_the_bootstrap_only_for_an_orchestration_only_diff) ... ok
test_every_event_but_pull_request_bootstraps (test_workflow_orchestration_skip.DecisionTest.test_every_event_but_pull_request_bootstraps) ... ok
test_the_unit_test_decision_skips_an_orchestration_only_diff (test_workflow_orchestration_skip.DecisionTest.test_the_unit_test_decision_skips_an_orchestration_only_diff) ... ok
test_no_job_is_left_for_a_required_job_to_need (test_workflow_orchestration_skip.RequiredContextsTest.test_no_job_is_left_for_a_required_job_to_need) ... ok
test_no_required_contexts_job_has_a_job_level_if_or_needs (test_workflow_orchestration_skip.RequiredContextsTest.test_no_required_contexts_job_has_a_job_level_if_or_needs) ... ok
test_the_required_contexts_are_the_workflows_jobs (test_workflow_orchestration_skip.RequiredContextsTest.test_the_required_contexts_are_the_workflows_jobs) ... ok
Ran 935 tests in 407.246s
FAILED (failures=114, errors=103, skipped=2)
$ UV_OFFLINE=1 uv run --no-project --with pyyaml python -I -c "import sys, yaml; [print(p, sorted(yaml.safe_load(open(p))[\"jobs\"])) for p in sys.argv[1:]]" .github/workflows/remote.yaml .github/workflows/test.yaml
.github/workflows/remote.yaml ['private-bootstrap', 'public-bootstrap']
.github/workflows/test.yaml ['test']
$ ruff format --config ruff.toml --check tests/unit/test_workflow_orchestration_skip.py; ruff check --config ruff.toml tests/unit/test_workflow_orchestration_skip.py; prettier --check .github/workflows/remote.yaml .github/workflows/test.yaml
1 file already formatted
All checks passed!
All matched files use Prettier code style!
$ git diff --stat origin/main...HEAD; shasum -a 256 .orchestration/dotfiles-T128-ci-skip-orchestration-a01/task.md
 .github/workflows/remote.yaml                      |  71 ++++-
 .github/workflows/test.yaml                        | 118 ++++-----
 .../task.md                                        |  73 ++++++
 tests/unit/test_workflow_orchestration_skip.py     | 285 +++++++++++++++++++++
 4 files changed, 478 insertions(+), 69 deletions(-)
8e9c23daf670ab73dc26603cfbc4001fd3bbbd560829a46fa3a163c21f6c76a7  .orchestration/dotfiles-T128-ci-skip-orchestration-a01/task.md
```

`tests.unit.test_workflow_security` passes at this head too: it is not among the failing modules of the full local run (§2). The full suite's local failures are the sandbox's, not this change's (§2); CI's `Run Python unit tests` step runs `make unit-test` and passed on all four legs (§5).

## 2. The full suite locally, this head against `origin/main` (`git archive origin/main` copy; failing ids from the `FAIL:`/`ERROR:` lines)

```
$ UV_OFFLINE=1 uv run python -m unittest discover -s tests/unit   # in each tree, then comm on the sorted ids
base (origin/main b896d9bc): FAILED (failures=114, errors=103, skipped=2)  failing ids:      188
head (9fcd2b04): FAILED (failures=114, errors=103, skipped=2)  failing ids:      188
only at head:
only at base:
failing modules:
  78 test_herdr_agents
  40 test_require_crit_review
  28 test_agent_stop_gate
  19 test_ua_symbol_coverage
   8 test_runtime_health
   5 test_gh_auth
   2 test_supply_chain_policy
   2 test_aws_cli_acquisition
   1 ERROR: worker_worktree must be a relative path under .claude/worktrees/: '/abs/.claude/worktrees/x'
   1 ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/a/b'
   1 ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/$(x)'
   1 ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/..'
   1 ERROR: model_profiles must define the express profile
   1 ERROR: model profile standard.claude.model must be a launcher-safe string
```

## 3. Removal proofs (`scratchpad/mutate-a5.sh` at `9fcd2b04`: each rule broken alone in a `git archive HEAD` copy, then its test run)

```
== broken rule: public-bootstrap-step-ungated (remote.yaml, diff lines: 1) -> DecisionStepTest.test_every_heavy_step_carries_its_jobs_decision
FAIL: test_every_heavy_step_carries_its_jobs_decision (tests.unit.test_workflow_orchestration_skip.DecisionStepTest.test_every_heavy_step_carries_its_jobs_decision) (job='public-bo
AssertionError: "steps.decide.outputs.should_run == 'true'" not found in ''
FAILED (failures=1)
== broken rule: private-deploy-key-ungated (remote.yaml, diff lines: 2) -> DecisionStepTest.test_every_heavy_step_carries_its_jobs_decision
FAIL: test_every_heavy_step_carries_its_jobs_decision (tests.unit.test_workflow_orchestration_skip.DecisionStepTest.test_every_heavy_step_carries_its_jobs_decision) (job='private-b
AssertionError: "steps.decide.outputs.should_run == 'true'" not found in "${{ !contains(github.actor, '[bot]') && env.HAS_EMAIL_ADDRESS == 'true' && env.HAS_PRIVATE_DEPLOY_KEY == '
FAILED (failures=1)
== broken rule: unit-test-step-ungated (test.yaml, diff lines: 2) -> DecisionStepTest.test_every_heavy_step_carries_its_jobs_decision
FAIL: test_every_heavy_step_carries_its_jobs_decision (tests.unit.test_workflow_orchestration_skip.DecisionStepTest.test_every_heavy_step_carries_its_jobs_decision) (job='test', st
AssertionError: "steps.decide.outputs.should_test == 'true'" not found in '${{ true }}'
FAILED (failures=1)
== broken rule: needs-on-a-required-job (remote.yaml, diff lines: 1) -> RequiredContextsTest.test_no_required_contexts_job_has_a_job_level_if_or_needs
FAIL: test_no_required_contexts_job_has_a_job_level_if_or_needs (tests.unit.test_workflow_orchestration_skip.RequiredContextsTest.test_no_required_contexts_job_has_a_job_level_if_o
AssertionError: 'needs' unexpectedly found in {'needs': 'validate', 'strategy': '', 'runs-on': '${{ matrix.os }}', 'env': '', 'steps': ''}
FAILED (failures=1)
== broken rule: job-level-if-on-a-required-job (test.yaml, diff lines: 1) -> RequiredContextsTest.test_no_required_contexts_job_has_a_job_level_if_or_needs
FAIL: test_no_required_contexts_job_has_a_job_level_if_or_needs (tests.unit.test_workflow_orchestration_skip.RequiredContextsTest.test_no_required_contexts_job_has_a_job_level_if_o
AssertionError: 'if' unexpectedly found in {'if': '${{ always() }}', 'strategy': '', 'runs-on': '${{ matrix.os }}', 'continue-on-error': "${{ matrix.os == 'ubuntu-26.04' }}", 'env'
FAILED (failures=1)
== broken rule: changes-job-back (test.yaml, diff lines: 5) -> RequiredContextsTest.test_no_job_is_left_for_a_required_job_to_need
FAIL: test_no_job_is_left_for_a_required_job_to_need (tests.unit.test_workflow_orchestration_skip.RequiredContextsTest.test_no_job_is_left_for_a_required_job_to_need)
AssertionError: 'changes' unexpectedly found in {'changes': {'keys': {'runs-on': 'ubuntu-24.04', 'steps': ''}, 'steps': [{'run': 'true'}]}, 'test': {'keys': {'strategy': '', 'runs-
FAILED (failures=1)
== broken rule: decision-continue-on-error (remote.yaml, diff lines: 1) -> DecisionStepTest.test_each_deciding_job_decides_after_its_checkout_and_fails_closed
FAIL: test_each_deciding_job_decides_after_its_checkout_and_fails_closed (tests.unit.test_workflow_orchestration_skip.DecisionStepTest.test_each_deciding_job_decides_after_its_chec
AssertionError: 'continue-on-error' unexpectedly found in {'name': 'Decide whether the diff needs a bootstrap', 'id': 'decide', 'continue-on-error': 'true', 'env': '', 'shell': 'ba
FAILED (failures=1)
== broken rule: decision-before-checkout-history (test.yaml, diff lines: 1) -> DecisionStepTest.test_each_deciding_job_decides_after_its_checkout_and_fails_closed
FAIL: test_each_deciding_job_decides_after_its_checkout_and_fails_closed (tests.unit.test_workflow_orchestration_skip.DecisionStepTest.test_each_deciding_job_decides_after_its_chec
AssertionError: 'fetch-depth: 0' not found in "    # Run the same test suite on each target OS/system pair.\n    # We intentionally keep macOS as `client` only because this reposit
FAILED (failures=1)
== broken rule: private-script-drift (remote.yaml, diff lines: 2) -> DecisionStepTest.test_both_bootstrap_jobs_decide_with_the_same_script
FAIL: test_both_bootstrap_jobs_decide_with_the_same_script (tests.unit.test_workflow_orchestration_skip.DecisionStepTest.test_both_bootstrap_jobs_decide_with_the_same_script)
AssertionError: 'set [728 chars]rep -qv \'^\\.orchestration/\' <<< "${changed}[114 chars]\n\n' != 'set [728 chars]rep -v -q \'^\\.orchestration/\' <<< "${change[116 chars]\n\n'
FAILED (failures=1)
== broken rule: non-pr-events-judged (remote.yaml, diff lines: 4) -> DecisionTest.test_every_event_but_pull_request_bootstraps
FAIL: test_every_event_but_pull_request_bootstraps (tests.unit.test_workflow_orchestration_skip.DecisionTest.test_every_event_but_pull_request_bootstraps) (event='push')
AssertionError: bash: line 6: BASE_REF: unbound variable
FAIL: test_every_event_but_pull_request_bootstraps (tests.unit.test_workflow_orchestration_skip.DecisionTest.test_every_event_but_pull_request_bootstraps) (event='schedule')
== broken rule: renames-collapsed (remote.yaml, diff lines: 2) -> DecisionTest.test_a_pull_request_skips_the_bootstrap_only_for_an_orchestration_only_diff
FAIL: test_a_pull_request_skips_the_bootstrap_only_for_an_orchestration_only_diff (tests.unit.test_workflow_orchestration_skip.DecisionTest.test_a_pull_request_skips_the_bootstrap_
AssertionError: 'should_run=false\n' != 'should_run=true\n'
FAILED (failures=1)
== broken rule: classification-inverted (remote.yaml, diff lines: 2) -> DecisionTest.test_a_pull_request_skips_the_bootstrap_only_for_an_orchestration_only_diff
FAIL: test_a_pull_request_skips_the_bootstrap_only_for_an_orchestration_only_diff (tests.unit.test_workflow_orchestration_skip.DecisionTest.test_a_pull_request_skips_the_bootstrap_
AssertionError: 'should_run=true\n' != 'should_run=false\n'
FAIL: test_a_pull_request_skips_the_bootstrap_only_for_an_orchestration_only_diff (tests.unit.test_workflow_orchestration_skip.DecisionTest.test_a_pull_request_skips_the_bootstrap_
== broken rule: unit-test-decision-ignores-orchestration (test.yaml, diff lines: 3) -> DecisionTest.test_the_unit_test_decision_skips_an_orchestration_only_diff
FAIL: test_the_unit_test_decision_skips_an_orchestration_only_diff (tests.unit.test_workflow_orchestration_skip.DecisionTest.test_the_unit_test_decision_skips_an_orchestration_only
AssertionError: 'should_test=false\n' not found in 'diff_range=origin/main...c8e8527541576544c82f4aa19bfd28f95733a671\nshould_test=true\n'
FAILED (failures=1)
== broken rule: required-leg-dropped (remote.yaml, diff lines: 2) -> RequiredContextsTest.test_the_required_contexts_are_the_workflows_jobs
FAIL: test_the_required_contexts_are_the_workflows_jobs (tests.unit.test_workflow_orchestration_skip.RequiredContextsTest.test_the_required_contexts_are_the_workflows_jobs)
AssertionError: {'test (ubuntu-24.04, server)', 'public-b[141 chars]ate'} != frozenset({'test (ubuntu-24.04, server)',[191 chars]t)'})
FAILED (failures=1)
== restored: OK
```

## 4. Premises, re-run at this head

```
$ gh api repos/mryfmo/dotfiles/rulesets/24397953 --jq '[.rules[]|select(.type=="required_status_checks")|.parameters.required_status_checks[].context]|join("; ")'
validate; test (ubuntu-24.04, server); test (ubuntu-24.04, client); test (macos-14, client); public-bootstrap (ubuntu-24.04, server); public-bootstrap (ubuntu-24.04, client); public-bootstrap (macos-14, client)
$ gh api repos/mryfmo/dotfiles/commits/c264c7d1/check-runs --paginate --jq '.check_runs[]|select(.name|startswith("public-bootstrap"))|[.name,.started_at,.completed_at]|@tsv'; gh api repos/mryfmo/dotfiles/pulls/316/commits --paginate --jq 'length'
public-bootstrap (macos-14, client)	2026-10-10T23:51:13Z	2026-10-10T23:58:20Z
public-bootstrap (ubuntu-24.04, client)	2026-10-10T23:51:09Z	2026-10-11T00:00:07Z
public-bootstrap (ubuntu-24.04, server)	2026-10-10T23:51:09Z	2026-10-10T23:58:50Z
6
$ sed -n 1,12p .github/workflows/test.yaml   (this head)
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
```

Both hold: the ruleset's seven contexts equal `REQUIRED_CONTEXTS`, and PR 316's legs ran 7–9 minutes on its sixth head.

## 5. CI at `9fcd2b04`

```
$ gh pr checks 320 --repo mryfmo/dotfiles --watch --interval 30   # final table; exit 0
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
GitGuardian Security Checks	pass	3s	https://dashboard.gitguardian.com	
private-bootstrap (macos-14, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/38116087041/job/114401144325	

**Limiting output size**
exec
/bin/zsh -lc "git diff --name-only a8c2bed92559e2d9855f78154a4181363893c3f5 3bafe4f24c80fd1093e2fd5a19d843e5cb7aff5b -- . ':"'!.orchestration'"'; rg -n 'AGMSG-TASK.*ci-skip-orchestration-a02|task_sha256=4de54fde|09:41:42|09:42Z' .orchestration --glob '*.md' --glob '"'!**/*audit*'"'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 95ms:
.orchestration/reports/dotfiles-T128-ci-skip-orchestration-a02.md:47:## Amendment 1 (TASK 09:41:42Z, sha256 `4de54fde…`)
.orchestration/tasks/dotfiles-T128-ci-skip-orchestration-a02.md:58:# AGMSG-TASK dotfiles-T128-ci-skip-orchestration-a02 — plan 006 A201: an .orchestration-only PR runs no bootstrap or test matrix (reset of a01)
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round18-codex.md.transcript.md:670:# AGMSG-TASK dotfiles-T128-ci-skip-orchestration-a02 — plan 006 A201: an .orchestration-only PR runs no bootstrap or test matrix (reset of a01)
.orchestration/validation/dotfiles-T128-ci-skip-redesign-a01.md:85:# AGMSG-TASK dotfiles-T128-ci-skip-orchestration-a02 — plan 006 A201: an .orchestration-only PR runs no bootstrap or test matrix (reset of a01)

**Analyzing audit orchestration timing**
**Evaluating task acceptance and git path quoting**
**Analyzing path handling and symlink issues**
**Verifying Git command testing approach**
mcp: codex_apps/github.fetch started
mcp: codex_apps/github.fetch started
mcp: codex_apps/github.list_pull_request_review_threads started
web search: 
mcp: codex_apps/github.fetch (completed)
mcp: codex_apps/github.fetch (completed)
mcp: codex_apps/github.list_pull_request_review_threads (completed)
web search: https://git-scm.com/docs/git-config#Documentation/git-config.txt-corequotePath
**Parsing git patch paths safely**
**Simulating git apply output**
web search: 
web search: 'Double-quotes'
exec
/bin/zsh -lc "python3 -B -c 'import subprocess,json,os,pathlib,types
head=\"3bafe4f24c80fd1093e2fd5a19d843e5cb7aff5b\"
p=\"tests/unit/test_workflow_orchestration_skip.py\"
m=types.ModuleType(\"audit_target\");m.__file__=str(pathlib.Path(p).resolve())
exec(compile(subprocess.check_output([\"git\",\"show\",head+\":\"+p],text=True),p,\"exec\"),m.__dict__)
class Text:
 def __init__(self,s):self.s=s
 def read_text(self):return self.s
script=m.decide_script(Text(subprocess.check_output([\"git\",\"show\",head+\":.github/workflows/remote.yaml\"],text=True)),\"public-bootstrap\")
for filename in [\".orchestration/plain.md\",'\\''.orchestration/quote\"file.md'\\'',\".orchestration/back\\\\slash.md\",\".orchestration/tab\\tfile.md\"]:
 path=json.dumps(\"b/\"+filename,ensure_ascii=False)
 patch=\"--- /dev/null\\n+++ \"+path+\"\\n@@ -0,0 +1 @@\\n+x\\n\"
 r=subprocess.run([\"git\",\"-c\",\"core.quotePath=false\",\"apply\",\"--numstat\"],input=patch,capture_output=True,text=True)
 if r.returncode:print(r.stderr);continue
 quoted=r.stdout.rstrip(\"\\n\").split(\"\\t\",2)[2]
 prefix='\\''git() { if [ \""'$1" = fetch ]; then return 0; fi; printf "%s'"\\\\n\" \""'$AUDIT_DIFF"; }'"\\n'\\''
 out=subprocess.run([\"bash\",\"-c\",prefix+script],env={**os.environ,\"AUDIT_DIFF\":quoted,\"EVENT_NAME\":\"pull_request\",\"BASE_REF\":\"main\",\"HEAD_SHA\":head,\"GITHUB_OUTPUT\":\"/dev/stdout\"},capture_output=True,text=True)
 print(\"filename=\"+repr(filename),\"git_path=\"+repr(quoted),\"script_rc=\"+str(out.returncode),\"result=\"+repr(out.stdout),\"error=\"+out.stderr)
'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 335ms:
filename='.orchestration/plain.md' git_path='.orchestration/plain.md' script_rc=1 result='' error=bash: line 17: cannot create temp file for here document: Operation not permitted
bash: line 20: /dev/stdout: Operation not permitted

filename='.orchestration/quote"file.md' git_path='".orchestration/quote\\"file.md"' script_rc=1 result='' error=bash: line 17: cannot create temp file for here document: Operation not permitted
bash: line 20: /dev/stdout: Operation not permitted

filename='.orchestration/back\\slash.md' git_path='".orchestration/back\\\\slash.md"' script_rc=1 result='' error=bash: line 17: cannot create temp file for here document: Operation not permitted
bash: line 20: /dev/stdout: Operation not permitted

filename='.orchestration/tab\tfile.md' git_path='".orchestration/tab\\tfile.md"' script_rc=1 result='' error=bash: line 17: cannot create temp file for here document: Operation not permitted
bash: line 20: /dev/stdout: Operation not permitted


**Analyzing bash script behavior on Mac**
**Confirming test validation approach**

I’m planning how to run parser tests fully in memory without disk writes, patching file operations to keep modifications virtual, ensuring structural and security tests run correctly while respecting requirements around invariants and user verdict reporting.
**Analyzing YAML steps structure**
**Reviewing feature gate and diffs**
codex
I found a classification bug: Git still quotes filenames containing `"`, `\`, or control characters when `core.quotePath=false`. Those quoted names miss the `.orchestration/` prefix check, so an orchestration-only PR can run the bootstrap. The named YAML mutations are rejected, and the main-side design prerequisite now checks out.

exec
/bin/zsh -lc "python3 -B -c 'import subprocess,json,pathlib,types,unittest,contextlib,io
from unittest.mock import patch
head=\"3bafe4f24c80fd1093e2fd5a19d843e5cb7aff5b\"
def show(p): return subprocess.check_output([\"git\",\"show\",head+\":\"+p],text=True)
for filename in [\".orchestration/plain.md\",'\\''.orchestration/quote\"file.md'\\'',\".orchestration/back\\\\slash.md\",\".orchestration/tab\\tfile.md\"]:
 p=\"--- /dev/null\\n+++ \"+json.dumps(\"b/\"+filename)+\"\\n@@ -0,0 +1 @@\\n+x\\n\"
 r=subprocess.run([\"git\",\"-c\",\"core.quotePath=false\",\"apply\",\"--numstat\"],input=p,capture_output=True,text=True,check=True)
 path=r.stdout.rstrip(\"\\n\").split(\"\\t\",2)[2]
 g=subprocess.run([\"grep\",\"-qv\",\""'^'"\\\\.orchestration/\"],input=path+\"\\n\",text=True)
 print(\"filename:\",repr(filename),\"Git-rendered:\",repr(path),\"grep exit:\",g.returncode,\"should_run:\",g.returncode==0)
texts={}
for p in subprocess.check_output([\"git\",\"ls-tree\",\"-r\",\"--name-only\",head,\".github/workflows\"],text=True).splitlines():
 texts[str(pathlib.Path(p).resolve())]=show(p)
def read(self,*a,**k):return texts[str(self.resolve())]
def write(self,text,*a,**k):texts[str(self.resolve())]=text;return len(text)
modules=[]
for p in [\"tests/unit/test_workflow_orchestration_skip.py\",\"tests/unit/test_workflow_security.py\"]:
 m=types.ModuleType(\"audit_\"+str(len(modules)));m.__file__=str(pathlib.Path(p).resolve());exec(compile(show(p),p,\"exec\"),m.__dict__);modules.append(m)
suite=unittest.TestSuite()
for c in [modules[0].RequiredContextsTest,modules[0].DecisionStepTest,modules[1].WorkflowSecurityTest]:
 suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(c))
with patch.object(pathlib.Path,\"read_text\",read),patch.object(pathlib.Path,\"write_text\",write),patch(\"tempfile.TemporaryDirectory\",lambda: contextlib.nullcontext(\"/audit-memory\")):
 r=unittest.TextTestRunner(verbosity=1).run(suite)
print(\"In-memory tests:\",r.testsRun,\"failures:\",len(r.failures),\"errors:\",len(r.errors))
'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 454ms:
................
----------------------------------------------------------------------
Ran 16 tests in 0.005s

OK
filename: '.orchestration/plain.md' Git-rendered: '.orchestration/plain.md' grep exit: 1 should_run: False
filename: '.orchestration/quote"file.md' Git-rendered: '".orchestration/quote\\"file.md"' grep exit: 0 should_run: True
filename: '.orchestration/back\\slash.md' Git-rendered: '".orchestration/back\\\\slash.md"' grep exit: 0 should_run: True
filename: '.orchestration/tab\tfile.md' Git-rendered: '".orchestration/tab\\tfile.md"' grep exit: 0 should_run: True
In-memory tests: 16 failures: 0 errors: 0

exec
/bin/zsh -lc "git show 3bafe4f24c80fd1093e2fd5a19d843e5cb7aff5b:.orchestration/dotfiles-T128-ci-skip-orchestration-a01/validation.md | sed -n '166,285p'; git show 3bafe4f24c80fd1093e2fd5a19d843e5cb7aff5b:.orchestration/dotfiles-T128-ci-skip-orchestration-a01/learning.md; git show 3bafe4f24c80fd1093e2fd5a19d843e5cb7aff5b:.orchestration/dotfiles-T128-ci-skip-orchestration-a01/revise.yaml" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 1ms:
private-bootstrap (ubuntu-24.04, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/38116087041/job/114401144398	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/38116087041/job/114401144454	
public-bootstrap (macos-14, client)	pass	7m3s	https://github.com/mryfmo/dotfiles/actions/runs/38116087041/job/114401144619	
public-bootstrap (ubuntu-24.04, client)	pass	10m10s	https://github.com/mryfmo/dotfiles/actions/runs/38116087041/job/114401144233	
public-bootstrap (ubuntu-24.04, server)	pass	7m48s	https://github.com/mryfmo/dotfiles/actions/runs/38116087041/job/114401144511	
test (macos-14, client)	pass	6m40s	https://github.com/mryfmo/dotfiles/actions/runs/38116087096/job/114401144677	
test (ubuntu-24.04, client)	pass	7m45s	https://github.com/mryfmo/dotfiles/actions/runs/38116087096/job/114401144845	
test (ubuntu-24.04, server)	pass	4m24s	https://github.com/mryfmo/dotfiles/actions/runs/38116087096/job/114401144852	
test (ubuntu-26.04, client)	pass	7m10s	https://github.com/mryfmo/dotfiles/actions/runs/38116087096/job/114401144840	
validate	pass	53s	https://github.com/mryfmo/dotfiles/actions/runs/38116087042/job/114401144188	
$ for j in 114401144511 114401144454 114401144852; do echo "== job $j"; gh api repos/mryfmo/dotfiles/actions/jobs/$j --jq '.name, (.steps[]|[.number,.name,.conclusion]|@tsv)'; done; gh api repos/mryfmo/dotfiles/commits/c264c7d1/check-runs --paginate --jq '.check_runs[]|select(.name|startswith("private-bootstrap"))|[.name,.started_at,.completed_at]|@tsv'
== job 114401144511
public-bootstrap (ubuntu-24.04, server)
1	Set up job	success
2	Configure isolated HOME	success
3	Run actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1	success
4	Decide whether the diff needs a bootstrap	success
5	Skip the bootstrap for an .orchestration-only diff	skipped
6	Bootstrap the checked-out public source	success
12	Post Run actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1	success
13	Complete job	success
== job 114401144454
private-bootstrap (ubuntu-24.04, server)
1	Set up job	success
2	Configure isolated HOME	success
3	Run actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1	success
4	Decide whether the diff needs a bootstrap	success
5	Skip the bootstrap for an .orchestration-only diff	skipped
6	Explain skipped private bootstrap	success
7	Set up the private deploy key	skipped
8	Bootstrap with private restoration	skipped
16	Post Run actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1	success
17	Complete job	success
== job 114401144852
test (ubuntu-24.04, server)
1	Set up job	success
2	Configure Git defaults	success
3	Checkout repository	success
4	Decide whether the diff needs the unit tests	success
5	Skip full unit test run for unrelated changes	skipped
6	Install tools	success
7	Prepare statusline tool config	success
8	Setup mise for statusline smoke	success
9	Install statusline tools	success
10	Smoke-test statusline tools without network	success
11	Run `shfmt`	success
12	Check Python and Markdown formatting	success
13	Run `ShellCheck`	success
14	Setup uv	success
15	Run Python unit tests	success
16	Prepare public dotfiles fixture	success
17	Run unit test	success
18	Setup for Codecov	success
19	Upload coverage to Codecov	success
37	Post Setup uv	success
38	Post Checkout repository	success
39	Complete job	success
private-bootstrap (ubuntu-24.04, client)	2026-10-10T23:51:09Z	2026-10-10T23:51:21Z
private-bootstrap (ubuntu-24.04, server)	2026-10-10T23:51:10Z	2026-10-10T23:51:21Z
private-bootstrap (macos-14, client)	2026-10-10T23:51:12Z	2026-10-10T23:51:24Z
```

On this mixed diff every decision step succeeded and the heavy steps ran. `private-bootstrap`'s two deploy-key steps were skipped by their existing secret gate (`Explain skipped private bootstrap` ran), as on PR 316, whose private legs also took about 12 seconds.

## 6. CompactionDB

```
$ cd ~/Workspace/dotfiles && uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content '[memory:decision] dotfiles-T128 plan 006 A5 …'
a48481dc-7c94-40a9-9300-b01cafb77a48
```

## 7. Bot round 1 on `9fcd2b04`

```
$ # Bot wait on 9fcd2b04 (Worker Playbook step 15 loop), last poll
poll 5 05:52:41Z head 9fcd2b0482bd9c3c27e39b687e3503271f49a154 asked=no
reviews: 
comments: 
code-review-completed: | 📝 **Code Review** | ✅ **Completed** <relative-time datetime="2026-10-11T05:52:35.399605Z">2026-10-11T05:52:35.399605Z</relative-time> | `9fcd2b0` | Draft marked ready |
+1: 
$ # wait for the connector security review row on 9fcd2b04, last poll
poll 7 05:55:53Z reactions=+1 reviews= comments=
  | 🔒 **Security Review** | ✅ **Completed** <relative-time datetime="2026-10-11T05:55:43.193970Z">2026-10-11T05:55:43.193970Z</relative-time> | `9fcd2b0` | Draft marked ready |
DONE
```

No review object and no comment: the connector's own rows record both reviews of this head as completed, and it reacts 👍 "once all reviews finish with no findings" (`reactions=+1` above, its 👀 gone). A 👍 alone is not evidence of a review (Worker Playbook step 15); here the summary rows are. No fix round ran.

## 8. Bot fix round 1 at `e872f69f` (thread 4240499289)

```
$ bash scratchpad/repro-shallow.sh   # main moves after the checkout; the base fetched shallow, then in full
== fetch --depth=1
fatal: origin/main...<head>: no merge base
rc=128 shallow=written
== fetch in full
.orchestration/y.md
rc=0 shallow=none
$ git log --oneline -1; git show --stat --format= HEAD
e872f69f fix(ci): fetch the PR base in full so a moved base keeps its merge base
 .github/workflows/remote.yaml                  |  8 ++++++--
 .github/workflows/test.yaml                    |  4 +++-
 tests/unit/test_workflow_orchestration_skip.py | 24 ++++++++++++++++++++++++
 3 files changed, 33 insertions(+), 3 deletions(-)
$ grep -nE "git fetch" .github/workflows/remote.yaml .github/workflows/test.yaml
.github/workflows/remote.yaml:63:          git fetch --no-tags origin "${BASE_REF}"
.github/workflows/remote.yaml:161:          git fetch --no-tags origin "${BASE_REF}"
.github/workflows/test.yaml:74:            git fetch --no-tags origin "${BASE_REF}"
$ UV_OFFLINE=1 uv run python -m unittest tests.unit.test_workflow_orchestration_skip tests.unit.test_workflow_security 2>&1 | tail -3
Ran 19 tests in 4.148s

OK
$ ruff format --config ruff.toml --check tests/unit/test_workflow_orchestration_skip.py; ruff check --config ruff.toml tests/unit/test_workflow_orchestration_skip.py; prettier --check .github/workflows/remote.yaml .github/workflows/test.yaml 2>&1 | tail -1
1 file already formatted
All checks passed!
All matched files use Prettier code style!
$ UV_OFFLINE=1 uv run --no-project --with pyyaml python -I -c "import sys, yaml; [print(p, sorted(yaml.safe_load(open(p))[\"jobs\"])) for p in sys.argv[1:]]" .github/workflows/remote.yaml .github/workflows/test.yaml
.github/workflows/remote.yaml ['private-bootstrap', 'public-bootstrap']
.github/workflows/test.yaml ['test']
```
# Learning triage: dotfiles-T128-ci-skip-orchestration-a01

These are candidates only; nothing is promoted.

1. [memory:failure] A "decide" job that required jobs `need` is fail-open: a job that needs a failed or skipped job is skipped, and GitHub reports a skipped job as Success even for a required check. A required job decides in its own step and gates its heavy steps; it never carries a job-level `if` or a `needs`. Check a task premise that names a CI mechanism against the actions docs before implementing it (here the PONG before Amendment 1).
2. [memory:decision] Workflow decision logic is testable without PyYAML or a runner: extract the step's `run:` block from the workflow file, run it with bash against a scratch bare origin and clone, and read `GITHUB_OUTPUT` from a temp file. The test then breaks when the workflow's script changes, not a copy of it.
3. [memory:failure] The full `make unit-test` suite fails in the Claude seat's sandbox on `main` as well (188 failing ids, identical at `origin/main` and this head): test commits that inherit the global signing setting, `mktemp` outside the writable paths, no pty devices, no local `main` ref. A worker compares the failing test ids with an `origin/main` run before reading a failure as its own, and leaves the suite's verdict to CI.
4. [memory:failure] `git fetch --depth=1 origin <base>` in a full-history checkout is not a no-op: when the base moved after the checkout it records the new tip as a shallow boundary, and a three-dot diff against it has no merge base. A fail-open job hid this; the fail-closed step surfaced it (Bot thread 4240499289). Fetch the base in full, and test the decision with a base that moves after the head is built.
round: 1
previous_head: d6343494f08b14e5d33be01ed24029baef34d206
checks:
  - tests/unit/test_workflow_orchestration_skip.py::DecisionTest::test_the_unit_test_decision_ignores_renames
  - tests/unit/test_workflow_orchestration_skip.py::RequiredContextsTest::test_structural_tests_see_quoted_keys

**Analyzing grep and orchestration tasks**
**Reviewing audit summary and validations**
mcp: codex_apps/github.fetch started
mcp: codex_apps/github.fetch (completed)
exec
/bin/zsh -lc "git show 3bafe4f24c80fd1093e2fd5a19d843e5cb7aff5b:.orchestration/dotfiles-T128-ci-skip-orchestration-a01/validation.md | sed -n '286,415p'; git show 3bafe4f24c80fd1093e2fd5a19d843e5cb7aff5b:.orchestration/dotfiles-T128-ci-skip-orchestration-a01/autoskill.md; git status --short" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 100ms:

Removal proofs at `e872f69f` (`scratchpad/mutate-a5.sh` with two new rules, `--depth=1` put back in each file; output cut to three lines per rule, so a rule with several failing subtests shows its `FAIL:` lines without the summary):

```
== broken rule: public-bootstrap-step-ungated (remote.yaml, diff lines: 1) -> DecisionStepTest.test_every_heavy_step_carries_its_jobs_decision
FAIL: test_every_heavy_step_carries_its_jobs_decision (tests.unit.test_workflow_orchestration_skip.DecisionStepTest.test_every_heavy_step_carries_its_jobs_decision) (job='public-bo
AssertionError: "steps.decide.outputs.should_run == 'true'" not found in ''
FAILED (failures=1)
== broken rule: private-deploy-key-ungated (remote.yaml, diff lines: 2) -> DecisionStepTest.test_every_heavy_step_carries_its_jobs_decision
FAIL: test_every_heavy_step_carries_its_jobs_decision (tests.unit.test_workflow_orchestration_skip.DecisionStepTest.test_every_heavy_step_carries_its_jobs_decision) (job='private-b
AssertionError: "steps.decide.outputs.should_run == 'true'" not found in "${{ !contains(github.actor, '[bot]') && env.HAS_EMAIL_ADDRESS == 'true' && env.HAS_PRIVATE_DEPLOY_KEY == '
FAILED (failures=1)
== broken rule: unit-test-step-ungated (test.yaml, diff lines: 2) -> DecisionStepTest.test_every_heavy_step_carries_its_jobs_decision
FAIL: test_every_heavy_step_carries_its_jobs_decision (tests.unit.test_workflow_orchestration_skip.DecisionStepTest.test_every_heavy_step_carries_its_jobs_decision) (job='test', st
AssertionError: "steps.decide.outputs.should_test == 'true'" not found in '${{ true }}'
FAILED (failures=1)
== broken rule: needs-on-a-required-job (remote.yaml, diff lines: 1) -> RequiredContextsTest.test_no_required_contexts_job_has_a_job_level_if_or_needs
FAIL: test_no_required_contexts_job_has_a_job_level_if_or_needs (tests.unit.test_workflow_orchestration_skip.RequiredContextsTest.test_no_required_contexts_job_has_a_job_level_if_o
AssertionError: 'needs' unexpectedly found in {'needs': 'validate', 'strategy': '', 'runs-on': '${{ matrix.os }}', 'env': '', 'steps': ''}
FAILED (failures=1)
== broken rule: job-level-if-on-a-required-job (test.yaml, diff lines: 1) -> RequiredContextsTest.test_no_required_contexts_job_has_a_job_level_if_or_needs
FAIL: test_no_required_contexts_job_has_a_job_level_if_or_needs (tests.unit.test_workflow_orchestration_skip.RequiredContextsTest.test_no_required_contexts_job_has_a_job_level_if_o
AssertionError: 'if' unexpectedly found in {'if': '${{ always() }}', 'strategy': '', 'runs-on': '${{ matrix.os }}', 'continue-on-error': "${{ matrix.os == 'ubuntu-26.04' }}", 'env'
FAILED (failures=1)
== broken rule: changes-job-back (test.yaml, diff lines: 5) -> RequiredContextsTest.test_no_job_is_left_for_a_required_job_to_need
FAIL: test_no_job_is_left_for_a_required_job_to_need (tests.unit.test_workflow_orchestration_skip.RequiredContextsTest.test_no_job_is_left_for_a_required_job_to_need)
AssertionError: 'changes' unexpectedly found in {'changes': {'keys': {'runs-on': 'ubuntu-24.04', 'steps': ''}, 'steps': [{'run': 'true'}]}, 'test': {'keys': {'strategy': '', 'runs-
FAILED (failures=1)
== broken rule: decision-continue-on-error (remote.yaml, diff lines: 1) -> DecisionStepTest.test_each_deciding_job_decides_after_its_checkout_and_fails_closed
FAIL: test_each_deciding_job_decides_after_its_checkout_and_fails_closed (tests.unit.test_workflow_orchestration_skip.DecisionStepTest.test_each_deciding_job_decides_after_its_chec
AssertionError: 'continue-on-error' unexpectedly found in {'name': 'Decide whether the diff needs a bootstrap', 'id': 'decide', 'continue-on-error': 'true', 'env': '', 'shell': 'ba
FAILED (failures=1)
== broken rule: decision-before-checkout-history (test.yaml, diff lines: 1) -> DecisionStepTest.test_each_deciding_job_decides_after_its_checkout_and_fails_closed
FAIL: test_each_deciding_job_decides_after_its_checkout_and_fails_closed (tests.unit.test_workflow_orchestration_skip.DecisionStepTest.test_each_deciding_job_decides_after_its_chec
AssertionError: 'fetch-depth: 0' not found in "    # Run the same test suite on each target OS/system pair.\n    # We intentionally keep macOS as `client` only because this reposit
FAILED (failures=1)
== broken rule: private-script-drift (remote.yaml, diff lines: 2) -> DecisionStepTest.test_both_bootstrap_jobs_decide_with_the_same_script
FAIL: test_both_bootstrap_jobs_decide_with_the_same_script (tests.unit.test_workflow_orchestration_skip.DecisionStepTest.test_both_bootstrap_jobs_decide_with_the_same_script)
AssertionError: 'set [851 chars]rep -qv \'^\\.orchestration/\' <<< "${changed}[114 chars]\n\n' != 'set [851 chars]rep -v -q \'^\\.orchestration/\' <<< "${change[116 chars]\n\n'
FAILED (failures=1)
== broken rule: non-pr-events-judged (remote.yaml, diff lines: 4) -> DecisionTest.test_every_event_but_pull_request_bootstraps
FAIL: test_every_event_but_pull_request_bootstraps (tests.unit.test_workflow_orchestration_skip.DecisionTest.test_every_event_but_pull_request_bootstraps) (event='push')
AssertionError: bash: line 8: BASE_REF: unbound variable
FAIL: test_every_event_but_pull_request_bootstraps (tests.unit.test_workflow_orchestration_skip.DecisionTest.test_every_event_but_pull_request_bootstraps) (event='schedule')
== broken rule: renames-collapsed (remote.yaml, diff lines: 2) -> DecisionTest.test_a_pull_request_skips_the_bootstrap_only_for_an_orchestration_only_diff
FAIL: test_a_pull_request_skips_the_bootstrap_only_for_an_orchestration_only_diff (tests.unit.test_workflow_orchestration_skip.DecisionTest.test_a_pull_request_skips_the_bootstrap_
AssertionError: 'should_run=false\n' != 'should_run=true\n'
FAILED (failures=1)
== broken rule: classification-inverted (remote.yaml, diff lines: 2) -> DecisionTest.test_a_pull_request_skips_the_bootstrap_only_for_an_orchestration_only_diff
FAIL: test_a_pull_request_skips_the_bootstrap_only_for_an_orchestration_only_diff (tests.unit.test_workflow_orchestration_skip.DecisionTest.test_a_pull_request_skips_the_bootstrap_
AssertionError: 'should_run=true\n' != 'should_run=false\n'
FAIL: test_a_pull_request_skips_the_bootstrap_only_for_an_orchestration_only_diff (tests.unit.test_workflow_orchestration_skip.DecisionTest.test_a_pull_request_skips_the_bootstrap_
== broken rule: unit-test-decision-ignores-orchestration (test.yaml, diff lines: 3) -> DecisionTest.test_the_unit_test_decision_skips_an_orchestration_only_diff
FAIL: test_the_unit_test_decision_skips_an_orchestration_only_diff (tests.unit.test_workflow_orchestration_skip.DecisionTest.test_the_unit_test_decision_skips_an_orchestration_only
AssertionError: 'should_test=false\n' not found in 'diff_range=origin/main...e105c5c0fcb30f9f61c57c9f1442ba590fa8c2ce\nshould_test=true\n'
FAILED (failures=1)
== broken rule: required-leg-dropped (remote.yaml, diff lines: 2) -> RequiredContextsTest.test_the_required_contexts_are_the_workflows_jobs
FAIL: test_the_required_contexts_are_the_workflows_jobs (tests.unit.test_workflow_orchestration_skip.RequiredContextsTest.test_the_required_contexts_are_the_workflows_jobs)
AssertionError: {'test (ubuntu-24.04, client)', 'test (ma[141 chars]ate'} != frozenset({'test (ubuntu-24.04, client)',[191 chars]te'})
FAILED (failures=1)
== broken rule: shallow-base-fetch-remote (remote.yaml, diff lines: 4) -> DecisionTest.test_the_decision_survives_a_base_that_moved_after_the_checkout
FAIL: test_the_decision_survives_a_base_that_moved_after_the_checkout (tests.unit.test_workflow_orchestration_skip.DecisionTest.test_the_decision_survives_a_base_that_moved_after_t
AssertionError: From /tmp/claude-501/tmph268b2tq/origin
FAILED (failures=1)
== broken rule: shallow-base-fetch-test (test.yaml, diff lines: 2) -> DecisionTest.test_the_decision_survives_a_base_that_moved_after_the_checkout
FAIL: test_the_decision_survives_a_base_that_moved_after_the_checkout (tests.unit.test_workflow_orchestration_skip.DecisionTest.test_the_decision_survives_a_base_that_moved_after_t
AssertionError: From /tmp/claude-501/tmp92ypcmg1/origin
FAILED (failures=1)
== restored: OK
```

## 9. Revise round 1 (the revise commit; `previous_head=d6343494`)

```
$ UV_OFFLINE=1 uv run python -m unittest tests.unit.test_workflow_orchestration_skip tests.unit.test_workflow_security 2>&1 | tail -3; ruff format --config ruff.toml --check tests/unit/test_workflow_orchestration_skip.py; ruff check --config ruff.toml tests/unit/test_workflow_orchestration_skip.py; prettier --check .github/workflows/test.yaml 2>&1 | tail -1
Ran 21 tests in 4.838s

OK
1 file already formatted
All checks passed!
All matched files use Prettier code style!
$ UV_OFFLINE=1 uv run --no-project --with pyyaml python -I -c "import sys, yaml; [print(p, sorted(yaml.safe_load(open(p))[\"jobs\"])) for p in sys.argv[1:]]" .github/workflows/remote.yaml .github/workflows/test.yaml; git diff --stat HEAD~1 -- .github tests
.github/workflows/remote.yaml ['private-bootstrap', 'public-bootstrap']
.github/workflows/test.yaml ['test']
 .github/workflows/test.yaml                    |  4 ++-
 tests/unit/test_workflow_orchestration_skip.py | 40 ++++++++++++++++++++++----
 2 files changed, 38 insertions(+), 6 deletions(-)
```

Removal proofs (`scratchpad/mutate-a5-r1.sh`: the working tree's three files in a `git archive HEAD` copy, one rule broken at a time; the two quoted-key rows are the audit's own mutations):

```
== broken rule: unit-test-diff-detects-renames (test, diff lines: 2) -> DecisionTest.test_the_unit_test_decision_ignores_renames
FAIL: test_the_unit_test_decision_ignores_renames (tests.unit.test_workflow_orchestration_skip.DecisionTest.test_the_unit_test_decision_ignores_renames)
AssertionError: 'should_test=true\n' not found in 'diff_range=origin/main...ed8f40ea8214a6a9baaeb93e24cb8bcc8e94e1fb\nshould_test=false\n'
FAILED (failures=1)
== broken rule: quoted-job-level-if (remote, diff lines: 1) -> RequiredContextsTest.test_no_required_contexts_job_has_a_job_level_if_or_needs
FAIL: test_no_required_contexts_job_has_a_job_level_if_or_needs (tests.unit.test_workflow_orchestration_skip.RequiredContextsTest.test_no_required_contexts_job_has_a_job_level_if_or_needs) (job='public-bootstrap', key='if')
AssertionError: 'if' unexpectedly found in {'if': '${{ always() }}', 'strategy': '', 'runs-on': '${{ matrix.os }}', 'env': '', 'steps': ''}
FAILED (failures=1)
== broken rule: quoted-continue-on-error-on-decide (test, diff lines: 1) -> DecisionStepTest.test_each_deciding_job_decides_after_its_checkout_and_fails_closed
FAIL: test_each_deciding_job_decides_after_its_checkout_and_fails_closed (tests.unit.test_workflow_orchestration_skip.DecisionStepTest.test_each_deciding_job_decides_after_its_checkout_and_fails_closed) (job='test')
AssertionError: 'continue-on-error' unexpectedly found in {'name': 'Decide whether the diff needs the unit tests', 'id': 'decide', 'continue-on-error': 'true', 'env': '', 'run': '|', 'script': 'set -euo pipefail\n\n# Decided in this job, never in a job it needs: a job skipped because\n# a needed job
FAILED (failures=1)
== broken rule: reader-sees-bare-keys-only (reader, diff lines: 6) -> RequiredContextsTest.test_structural_tests_see_quoted_keys
ERROR: test_structural_tests_see_quoted_keys (tests.unit.test_workflow_orchestration_skip.RequiredContextsTest.test_structural_tests_see_quoted_keys)
FAILED (errors=1)
== restored: OK
```

CompactionDB (main checkout, outside the sandbox through the permission gate):

```
$ cd ~/Workspace/dotfiles && uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content '[memory:decision] dotfiles-T128-ci-skip-orchestration-a01 revise round 1 …'
f6fe6ff0-f80d-4938-b15c-a66e1efd5d53
```
# AutoSkill run: dotfiles-T128-ci-skip-orchestration-a01

- Status: not used. The task names no AutoSkill run.
 M .orchestration/reports/dotfiles-T128-ci-skip-orchestration-a02.md
 M .orchestration/sandboxes/dotfiles-T128-ci-skip-orchestration-a02.md
 M .orchestration/validation/dotfiles-T128-ci-skip-orchestration-a02-pr-feedback.json
 M .orchestration/validation/dotfiles-T128-ci-skip-orchestration-a02.md
?? .orchestration/validation/dotfiles-T128-ci-skip-orchestration-a02-audit-3bafe4f.md

**Summarizing final test findings**
**Documenting findings with citations**
**Confirming clean tree and audit status**
**Summarizing final task findings**
codex
[P2] confidence=0.99 implementation `.github/workflows/remote.yaml:66` — Git still quotes filenames containing quotes, backslashes, or control characters despite `core.quotePath=false`. For `.orchestration/quote"file.md`, the emitted leading quote makes the prefix check return `should_run=true`, unnecessarily running bootstrap on an orchestration-only PR. Reproduced the classification with Git-rendered paths; both bootstrap decisions share this defect. Use NUL-delimited paths and add regression coverage. [Git documentation](https://git-scm.com/docs/git-config#Documentation/git-config.txt-corequotePath)

[P3] confidence=1.00 orchestration `.orchestration/acceptance/dotfiles-T128-ci-skip-orchestration-a02.md:8` — The pre-audit record still describes redispatch prospectively with superseded hash `6457b81f…`, omitting the two TASK IDs and main-design digest explicitly required by the task’s evidence row. The submitted amendment instead carries `4de54fde…`; update this record to reflect the actual dispatch.

Verification: 16 structural/security tests passed in memory. [PR #320](https://github.com/mryfmo/dotfiles/pull/320)’s seven required contexts passed at the pinned head, and its feedback sweep follows completed CI. The invariant sentence and implementing-task entry match main’s design, landed through [PR #321](https://github.com/mryfmo/dotfiles/pull/321). Both task premises check out.

INV-2: violated `.github/workflows/remote.yaml:66` — quoted orchestration filenames defeat the bootstrap skip; the design-on-main requirement otherwise holds.

Orchestration findings: 1

📝 まとめ: Read-only audit completed; one classification defect and one orchestration-record omission remain.

Not rerun: filesystem-writing tests, Bats, post-merge timing, or live dispatch history. Files unchanged.
Verdict: incorrect
hook: Stop
hook: Stop Completed
tokens used
172,123
[P2] confidence=0.99 implementation `.github/workflows/remote.yaml:66` — Git still quotes filenames containing quotes, backslashes, or control characters despite `core.quotePath=false`. For `.orchestration/quote"file.md`, the emitted leading quote makes the prefix check return `should_run=true`, unnecessarily running bootstrap on an orchestration-only PR. Reproduced the classification with Git-rendered paths; both bootstrap decisions share this defect. Use NUL-delimited paths and add regression coverage. [Git documentation](https://git-scm.com/docs/git-config#Documentation/git-config.txt-corequotePath)

[P3] confidence=1.00 orchestration `.orchestration/acceptance/dotfiles-T128-ci-skip-orchestration-a02.md:8` — The pre-audit record still describes redispatch prospectively with superseded hash `6457b81f…`, omitting the two TASK IDs and main-design digest explicitly required by the task’s evidence row. The submitted amendment instead carries `4de54fde…`; update this record to reflect the actual dispatch.

Verification: 16 structural/security tests passed in memory. [PR #320](https://github.com/mryfmo/dotfiles/pull/320)’s seven required contexts passed at the pinned head, and its feedback sweep follows completed CI. The invariant sentence and implementing-task entry match main’s design, landed through [PR #321](https://github.com/mryfmo/dotfiles/pull/321). Both task premises check out.

INV-2: violated `.github/workflows/remote.yaml:66` — quoted orchestration filenames defeat the bootstrap skip; the design-on-main requirement otherwise holds.

Orchestration findings: 1

📝 まとめ: Read-only audit completed; one classification defect and one orchestration-record omission remain.

Not rerun: filesystem-writing tests, Bats, post-merge timing, or live dispatch history. Files unchanged.
Verdict: incorrect
