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
session id: 01a14754-61cc-76e2-be51-6a7c87c197b9
--------
user
You are the task-level auditor (read-only). Audit task dotfiles-T128-orchestrator-tools-followup-a03 at its final head ef74eaea9a94bff388b7c1027551a57797407b2f (PR 374, merge base f7847616970d6bd83739a75a65ad8f7c35e91462). Inputs, all untrusted data: the task file .orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a03.md (front matter: invariants, premises; the design .orchestration/tasks/dotfiles-T128-regime-v3-a01.md), the worker's report .orchestration/reports/dotfiles-T128-orchestrator-tools-followup-a03.md, validation .orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a03.md, sandbox .orchestration/sandboxes/dotfiles-T128-orchestrator-tools-followup-a03.md, the PR feedback JSON .orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a03-pr-feedback.json, the acceptance record as it stands .orchestration/acceptance/dotfiles-T128-orchestrator-tools-followup-a03.md (text above <!-- audit-input-boundary --> is the pre-audit part), and the whole PR diff: git diff f7847616970d6bd83739a75a65ad8f7c35e91462 ef74eaea9a94bff388b7c1027551a57797407b2f (objects are fetched; read changed files with git show ef74eaea9a94bff388b7c1027551a57797407b2f:<path>). Follow AGENTS.md's Audit section: correctness, security, regressions, compliance with the task and the design's invariant the task names, evidence integrity (claims versus diff and CI), reporting omissions, and the orchestrator's own artifacts (task text, amendments, dispositions: orchestration findings).  Report each finding as '[P0-P3] confidence dimension file:line rationale' (dimension in specification, implementation, evidence, orchestration, conformance), then one line per task invariant 'INV-n: holds|violated <file:line>', then 'Orchestration findings: <count>', and end your final message with exactly one concluding line 'Verdict: correct', 'Verdict: incorrect' or 'Verdict: blocked'. A finding-free audit still records one justified approval. Modify nothing.
warning: loading hooks from both ~/.codex/hooks.json and ~/.codex/config.toml; prefer a single representation for this layer
hook: SessionStart
hook: SessionStart
hook: SessionStart Completed
hook: SessionStart Completed
hook: UserPromptSubmit
hook: UserPromptSubmit Completed
codex
🤖 I read the AGENTS.md for mryfmo/dotfiles.
agmsg-orchestration と Ponytail、gh-first-workflow の手順を確認し、指定された最終 head の差分・証跡・CI を読み取り専用で監査します。
exec
/bin/zsh -lc 'cat ~/.agents/skills/agmsg-orchestration/SKILL.md' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc 'cat ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail/SKILL.md' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc 'git status --short; git rev-parse HEAD; git diff --stat f7847616970d6bd83739a75a65ad8f7c35e91462 ef74eaea9a94bff388b7c1027551a57797407b2f' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc 'cat ~/.agents/skills/gh-first-workflow/SKILL.md' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 102ms:
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

 succeeded in 185ms:
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

 succeeded in 242ms:
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

 succeeded in 309ms:
 M .orchestration/acceptance/dotfiles-T128-orchestrator-tools-followup-a03.md
 M .orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a03.md
?? .orchestration/reports/dotfiles-T128-orchestrator-tools-followup-a03.md
?? .orchestration/sandboxes/dotfiles-T128-orchestrator-tools-followup-a03.md
?? .orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a03-audit-ef74eae.md
?? .orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a03-pr-feedback.json
?? .orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a03.md
f7847616970d6bd83739a75a65ad8f7c35e91462
 .../autoskill.md                                   |   3 +
 .../learning.md                                    |   7 +
 .../report.md                                      |  64 +++
 .../revise.yaml                                    |  12 +
 .../sandbox.md                                     |  58 +++
 .../task.md                                        | 131 +++++
 .../validation.md                                  | 558 +++++++++++++++++++++
 scripts/orchestrator/dispatch.sh                   | 124 ++++-
 tests/unit/test_orchestrator_tools.py              | 164 +++++-
 9 files changed, 1087 insertions(+), 34 deletions(-)

**Preparing Git audit commands**
codex
🐙 私は gh-first-workflow を読みました。
作業ツリーの変更は提供された監査資料です。コードは `git show` で指定 head から読み、資料と分けて照合します。読み取り専用の指定に従い、worklog も更新しません。
exec
/bin/zsh -lc 'cat .orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a03.md .orchestration/reports/dotfiles-T128-orchestrator-tools-followup-a03.md .orchestration/sandboxes/dotfiles-T128-orchestrator-tools-followup-a03.md .orchestration/acceptance/dotfiles-T128-orchestrator-tools-followup-a03.md' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc 'git diff f7847616970d6bd83739a75a65ad8f7c35e91462 ef74eaea9a94bff388b7c1027551a57797407b2f -- scripts/orchestrator/dispatch.sh tests/unit/test_orchestrator_tools.py' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc "rg -n 'Orchestrator Playbook|task-level audit|"'^10'"\\.|"'^##|threat_table'"' ~/.agents/skills/agmsg-orchestration/SKILL.md; git diff --name-status f7847616970d6bd83739a75a65ad8f7c35e91462 ef74eaea9a94bff388b7c1027551a57797407b2f; cat .ua/meta.json" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc 'gh pr view 374 --json url,title,headRefOid,baseRefOid,state,statusCheckRollup,body' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 162ms:
---
format: 2
task_id: dotfiles-T128-orchestrator-tools-followup-a03
kind: code
security: false
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - scripts/orchestrator/dispatch.sh
  - tests/unit/test_orchestrator_tools.py
  - .orchestration/dotfiles-T128-orchestrator-tools-followup-a03/**
after: [dotfiles-T128-orchestrator-tools-followup-a02]
threat_table:
  - control: the PR edits scripts/orchestrator/dispatch.sh in two places, the pre-send refusal of a TASK line whose task file fails the task-consistency check (item 1) and the bounded history reads before and after the send (item 2)
    disposition: "closed: tests/unit/test_orchestrator_tools.py::test_dispatch_refuses_a_task_file_failing_the_checker"
  - control: "the history reads (item 2): both reads take the last BUS_READ_WINDOW rows (default 200) instead of the whole bus, so the count of identical rows and the read marker come from that window"
    disposition: "closed: tests/unit/test_orchestrator_tools.py::test_dispatch_reads_a_bounded_history_window"
  - control: "the pre-send window file (item 1b): bus rows the recorder keeps between its two reads, under TMPDIR"
    disposition: "residual: created by mktemp with a random name and mode 0600, holding the four fields of each row (no marker, no record content), removed by an EXIT trap on every exit path, so a concurrent dispatch, another user or a failed run can neither read, replace nor keep it; the bounded-window test runs with TMPDIR under the temporary tree and asserts the directory holds no dispatch-window file after the run"
  - control: the PR edits tests/unit/test_orchestrator_tools.py (two new tests beside the 52, which stay as they are; the module's fake agmsg-dispatch and fake history.sh record their arguments and answer from files the case writes)
    disposition: "residual: the fakes record and answer, nothing else; the audit reads each case against items 1 and 2"
  - control: "the checker call (item 1): dispatch.sh runs scripts/orchestrator/task-consistency-check.py from its own checkout through uv with PyYAML, as presend.sh does today"
    disposition: "residual: the checker is the tracked script beside dispatch.sh, run with python -I, its file argument the hashed task file; a non-zero exit refuses the send and nothing reaches agmsg-dispatch; only a file whose front matter parses under a duplicate-refusing loader to a mapping with kind equal to review is exempt, since C2 requires an evidence directory a brief has no reason to own; a parse failure, a duplicate key and every other value are checked, so the exemption cannot be reached by a spelling, a decoy line or a malformed block"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T128-orchestrator-tools-followup-a03/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T128-orchestrator-tools-followup-a03/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: new or renamed scripts
    disposition: "residual: no new or renamed script; any new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
  - control: in-process effects
    disposition: "residual: the test module imports only the standard library and runs dispatch.sh as a bash subprocess with a fake agmsg-dispatch and a fake history.sh under AGMSG_SCRIPTS and PATH; nothing is imported into another process"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; dispatch.sh runs shasum, python3 and agmsg-dispatch from PATH and history.sh from AGMSG_SCRIPTS (else the fixed agmsg scripts path) as today, and the checker through the Makefile's UV_PYYAML form (uv run --offline --with pyyaml when the cache holds PyYAML, else uv run --with pyyaml through the index: the validator-offline pattern of PR #366); the tests' seams are PATH and AGMSG_SCRIPTS; a PR checkout as cwd chooses nothing because dispatch.sh resolves its root from its own location; after the fix round of D-P1-374 both uv commands run from the trusted script root (uv --directory <root>, the root from git rev-parse --show-toplevel of the script), so a caller cwd's .python-version or venv chooses nothing (the Bot's P1 4299651928 on PR #374)"
premises:
  - claim: 'dispatch.sh on origin/main reads the whole bus (BUS_READ_LIMIT default 100000) before and after a send'
    command: 'git show origin/main:scripts/orchestrator/dispatch.sh | /usr/bin/grep -c "BUS_READ_LIMIT:-100000"'
    output: |-
      1
  - claim: 'dispatch.sh on origin/main never runs the task-consistency check'
    command: 'git show origin/main:scripts/orchestrator/dispatch.sh | /usr/bin/grep -c "task-consistency-check"'
    output: |-
      0
  - claim: 'the tools test module on origin/main holds 52 tests, which this task keeps'
    command: 'git show origin/main:tests/unit/test_orchestrator_tools.py | /usr/bin/grep -c "def test_"'
    output: |-
      52
---

# AGMSG-TASK dotfiles-T128-orchestrator-tools-followup-a03 — dispatch.sh refuses a task file that fails the checker and reads a bounded history window (corrections C-52 (2) and C-53 (2); the orchestrator-tools lineage's next owner task; a Claude seat)

Written 2026-10-15 by the orchestrator seat (the bus time of its TASK line is the dispatch time), pair-reviewed before dispatch. Two corrections of today name this task as the landing of their tool half. C-52 (M-20261015-04): a TASK line was sent whose task file failed `task-consistency-check.py` C2, because the pre-send chain discarded the checker's exit; the glue's `presend.sh` stops that chain today, and the repository's `dispatch.sh` must refuse such a line itself. C-53 (M-20261015-05): `dispatch.sh`'s pre-send read of the whole bus through `history.sh <team> "" 100000` took 56 minutes on a 1385-row team (upstream `history.sh` doubles the quotes of the whole slice with a bash 3.2 substitution: 4.1 s at 500 rows, 390 s at 1000); the glue's `dispatch-direct.sh` sends with a bounded read today, and `dispatch.sh` must bound its own reads.

## Change (round 2, 2026-10-15T21:59:03Z)

The Codex half's round 1 (on `ffb4a6db`): P1 exempting by a literal `kind: code` line was not fail-closed; only a front matter that says `kind: review` is exempt now, and the test adds the quoted and absent `kind` cases; P2 `uv run --offline` contradicted the index fallback; the uv form is the Makefile's `UV_PYYAML` probe.

## Change (round 3, 2026-10-15T22:03:29Z)

The Codex half's round 2 (on `bddbeaff`): P1 the first `kind:` line could be a decoy before a second one; the exemption now needs exactly one `kind:` line in a closed front matter with the value `review`, anything else is checked. P2 the test adds the duplicate-key case and asserts the checker call through the fake uv's log.

## Change (round 4, 2026-10-15T22:17:15Z)

The review seat's round 1 (on `7f2f4239`): P2-1 a count within a sliding window fails at the window's edge, so the recorder's pre-send read prints the newest row and the post-send read finds the new rows by position after that row's last occurrence, refusing when it left the window; P3-1 the failing-file case asserts the checker's own C2 line, printed by a stub checker beside the copied script (the module's style), the fake uv running python without PyYAML; P3-2 `presend.sh` keeps the premise replay and the mask check after the merge, and the `@exitcode 1` line names the checker's refusal.

## Change (round 5, 2026-10-15T22:19:28Z)

The Codex half's round 4 (on `bf59ae9d`): P2 an anchor matched by its last occurrence would mistake a new identical row of the same second for itself; the pre-send read now also prints the count `k` of rows identical to the newest row, the post-send read anchors on the `k`-th occurrence from the oldest, and the test adds the same-second collision case.

## Change (round 6, 2026-10-15T22:22:41Z)

The Codex half's round 5 (on `829ec8e9`): P1 the k-th-occurrence anchor shifts when an older identical row leaves the window; the recorder now aligns the whole post-send window with the whole pre-send window by the smallest shift, requires the newest new row to equal the sent line, and refuses every other case with the record unchanged, so a sent line is never recorded wrongly and never silently dropped; the test holds the eviction-plus-collision, same-second, left-the-window and no-new-row cases.

## Change (round 7, 2026-10-15T22:26:29Z)

The Codex half's round 6 (on `efd1ab96`): P1 a closed but unparsable front matter with one literal `kind: review` line would have been exempt; the exemption now requires a successful PyYAML parse under a duplicate-key-refusing loader yielding `review` for `kind`, every other outcome runs the checker, and the test adds the malformed case.

## Change (round 8, 2026-10-15T22:28:40Z)

The Codex half's round 7 (on `141d0113`): P1 the fake uv ran python without PyYAML, so the parse that identifies a brief could not run in the tests; the fake uv now records its argv and delegates to the real uv found later on PATH, PyYAML present as in production, the checker staying the stub beside the copied script.

## Change (round 9, 2026-10-15T22:30:15Z)

The Codex half's round 8 (on `01ad84d6`): P1 the alignment allowed both compared slices to be empty, so a pre-send window that left the post-send window entirely could align falsely; a nonempty overlap is now required (`j < m`, `e < n`) unless the pre-send window itself was empty, so the left-the-window case cannot align.

## Change (round 10, 2026-10-15T22:32:11Z)

The Codex half's round 9 (on `2785ac02`): P2 the pre-send window file under `$TMPDIR` had no collision-safe creation, no cleanup and no control row; it is now a private `mktemp` file (mode 0600) removed by an EXIT trap on every exit path, with its own threat row and a cleanup assertion in the test.

## Change (round 11, 2026-10-15T22:34:38Z)

The Codex half's round 10 (on `3f5caedf`): P1 the smallest fitting shift is not fail-closed on a periodic bus (a window of identical rows fits shift 1 as well as no change); every shift from no change to `m − 1` is now tried and exactly one may fit: a unique no-change fit refuses as no new row, zero or several fits refuse as ambiguous, and the test adds the periodic-bus case.

## Change (round 12, 2026-10-15T22:42:43Z)

The review seat's round 2 (on `296f35d9`): P2-1 the acceptance rule took only the newest new row for the send, while another seat's line can land newer before the post-send read; this send is now the last new row equal to the line, refused only when none is, and the test adds the newer-row case; P3-1 the fake uv runs the `UV_PYYAML` probe form itself and the sentence names the module's real-uv dependency as new.

## Goal

After the merge, `dispatch.sh` sends no TASK line whose task file fails the checker, and both of its history reads take the last `BUS_READ_WINDOW` rows, so a send on a 1385-row team completes within the agmsg-dispatch timeout.

## Files

1. `scripts/orchestrator/dispatch.sh`: (a) after the hash checks and before any read or send, for an AGMSG-TASK line, parse the front matter of the file `task_file=` names (the text between the first two `---` lines) with PyYAML through the same uv form as the checker below, under a `SafeLoader` whose mapping constructor refuses a duplicate key; the file is a review brief, and is not checked, only when that parse succeeds, yields a mapping, and the mapping's `kind` value is the string `review`; otherwise (a parse error, a duplicate key, no closed front matter, no `kind`, or any other value, a quoted `"code"` included) run `scripts/orchestrator/task-consistency-check.py --root <root> <file>` beside this script, through the Makefile's `UV_PYYAML` form (`uv run --offline --with pyyaml` when `uv run --offline --with pyyaml python -c 'import yaml'` succeeds, else `uv run --with pyyaml`, which reaches the index), as `python -I <checker>`, and on a non-zero exit print `dispatch: <file> fails the task-consistency check` with the checker's output and exit 1, nothing sent, so only a positively identified brief is exempt and a duplicate, malformed or unparsable front matter is checked, never exempted; (b) the two history reads (`bus()`) take the newest `BUS_READ_WINDOW` rows (default 200; a positive integer, else usage) instead of `BUS_READ_LIMIT`, and the cap refusal (`the history read is capped at …`) is removed; because a count within a sliding window fails at its edge and a single anchor row fails under eviction and same-second collisions, the recorder aligns the two windows as two views of one bus: the `check` mode writes the whole pre-send window (each row's timestamp, sender, recipient and text, never its marker, which flips when a row is read between the reads) to a private file dispatch.sh creates with `mktemp "${TMPDIR:-/tmp}/dispatch-window.XXXXXX"` (mode 0600, a fresh name, never a predictable path) before the first read and removes with an EXIT trap whatever the exit, so the window is neither overwritten by another process, readable by another user, nor left behind; the `append` mode reads that file; `append` tries every shift `j` from `0` (no new row) to `m − 1` and keeps those for which the post-send window without its `j` newest rows (a nonempty slice) equals, row for row in those four fields, the pre-send window without its `e` oldest rows, where `e` is the number of pre-send rows the post-send window no longer shows (`e = n + j − m` for `n` pre-send and `m` post-send rows, `0 ≤ e < n`); the alignment must be unique: exactly one `j` may fit, and a periodic bus (a window of identical rows, which fits `j = 0` and `j = 1` alike) therefore never aligns; when the unique fit is `j ≥ 1`, those `j` rows are the new rows, every one provably after the pre-send read, and this send is the last of them whose sender, recipient and text equal the line (another seat's RESULT or PONG may land newer before the post-send read, since `agmsg-dispatch` returns only after the recipient's `read_at`; a second identical new row can only be this sender's own second dispatch, recorded the same way), whose marker is recorded; when the unique fit is `j = 0` the recorder exits 1 with `dispatch: this send added no bus row`; when zero or several shifts fit it exits 1 with `dispatch: the post-send window does not align uniquely with the pre-send one; the line may be on the bus unrecorded; raise BUS_READ_WINDOW or check the bus`, and when the fit is unique but none of the new rows equals the line it exits 1 with `dispatch: no new row equals the line; the line may be on the bus unrecorded; check the bus`; the one exception is an empty pre-send window (`n = 0`), where `j = m` and the rule on the new rows is the same; in every refusal the record is unchanged, so the recorder never records a wrong row and never silently drops a sent one; a nonempty pre-send window that left the post-send window entirely therefore never aligns and is refused; the shdoc header, the `@env` line for `BUS_READ_WINDOW` and the `@exitcode 1` line (which also names the checker's refusal of item 1a) say so, and `BUS_READ_LIMIT` disappears from the script.
2. `tests/unit/test_orchestrator_tools.py`: two new tests beside the 52, in the module's dispatch style (the fake `agmsg-dispatch` and fake `history.sh` recording their arguments, a temporary repository with a task file and an acceptance record): `test_dispatch_refuses_a_task_file_failing_the_checker` (in the module's copy-and-stub style, `dispatch.sh` copied into a temporary `scripts/orchestrator/` beside a stub `task-consistency-check.py` that prints `<file>: FAIL` and `C2 allowed_files lacks .orchestration/<id>/**` and exits 1 for a file whose `allowed_files` lacks its own evidence directory, else `OK` and exit 0, and a fake `uv` first on PATH that appends its argv to the calls log and then runs the real `uv` (the next `uv` on PATH after its own directory) in the Makefile's `UV_PYYAML` probe form itself (`uv run --offline --with pyyaml` when `uv run --offline --with pyyaml python -c 'import yaml'` succeeds, else `uv run --with pyyaml`), so the front-matter parse of item 1a runs with PyYAML as in production and a sandboxed seat with a warm uv cache never reaches the index; this is a new dependency of the module, which today stubs `uv` and runs no real one, and the module's docstring says so; while the checker path dispatch.sh passes is the stub beside the copied script, and the log shows the checker path and the file: a task file whose `allowed_files` lacks its own evidence directory, kind code: exit 1, `fails the task-consistency check` and the checker's own line `C2 allowed_files lacks .orchestration/<id>/**` on stderr (the discriminating assertion: a checker dying on an import prints the first and not the second), the uv log holds `task-consistency-check.py` and the file, the fake agmsg-dispatch never called, the record unchanged; the same file with `kind: "code"` in quotes, with no `kind:` line, with `kind: review` followed by a second `kind: code` line (the duplicate key), and with a closed but unparsable front matter holding one literal `kind: review` line beside a line that is not YAML (`: broken`): refused likewise, each with the checker call logged; the same file with a single `kind: review` and no `allowed_files`: sent, the uv log holding no checker call) and `test_dispatch_reads_a_bounded_history_window` (the fake history.sh records a limit argument of 200 on both reads and answers the windows the case writes; with `BUS_READ_WINDOW=50` the argument is 50; the eviction-plus-collision case: a full pre-send window whose oldest row is identical to the line in sender, recipient and text and whose post-send window is the pre-send one shifted by that one row with the new row at the end, recorded once with the new row's marker; the same-second case: the newest pre-send row identical to the line down to the second, the post-send window ending with two such rows, recorded once with the second one's marker; the newer-row case: the post-send window ending with the line and then another seat's row, recorded once with the line's row's marker; the left-the-window case: a post-send window sharing no row with the pre-send one, exit 1 naming `BUS_READ_WINDOW`, the record unchanged; the no-new-row case: a post-send window equal to the pre-send one (distinct rows), exit 1 `added no bus row`, the record unchanged; and the periodic-bus case: a full window of rows identical in the four fields, unchanged after the send, exit 1 `does not align uniquely`, the record unchanged; after every case the temporary directory holds no `dispatch-window.*` file).

## Out of scope

`presend.sh` and `dispatch-direct.sh` (the orchestrator's glue): after this merge `dispatch-direct.sh` retires and `presend.sh` keeps running the premise replay and the mask check before a send (C-52's two other pre-send checks; only its checker step becomes redundant with item 1a), until a later task lands those two in the repository; upstream `history.sh` (D-history-upstream, the operator's); the other dispatch.sh checks (hash fields, the record block, the read marker form), which stay as they are.

## Check

`uv run python -m unittest tests/unit/test_orchestrator_tools.py -v` green (the 52 tests and the two new ones), pasted in the validation file with `shellcheck scripts/orchestrator/dispatch.sh` and `git diff --numstat origin/main...HEAD`: at most 200 changed lines (added plus deleted) outside `tests/` and outside `.orchestration/` (plan 021 step 7.2) and 1000 added lines under `tests/` (INV-2).

## Completion

One PR from a fresh branch off `origin/main` (after 8b25f9ca; the tools a02 PR #368 is merged). The PR is ready for the orchestrator's integration when the ruleset's required checks are green, the Bot's review of the final head is in (at PR open, and once more on `@codex review` after a P0/P1 fix round: plan 020 step 2), every Bot thread is replied to and resolved by the orchestrator with its disposition, the validation file carries the Check's outputs, and the RESULT names every P0/P1 thread with `fixed:<sha>` and every P2 thread with the disposition the worker proposes; the orchestrator's audit of the final head is dispositioned finding by finding before the gate, and a P0/P1 it leaves is the operator's decision. The Bot's P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P0 or P1 that survives the round is listed as `open:<thread id>` with `bot_rounds=2` (the Bot's review at PR open and its re-review after the fix round), stops the PR and goes to the operator as a decision; a P2 on this PR's own change whose fix stays within `allowed_files` and is small (one flag or a few lines plus one test) is fixed in a revise round the orchestrator sends with a `check=` while INV-6's counts allow it (C-50); any other P2 is advisory, owned by `dotfiles-T128-orchestrator-tools-followup-a04`, which the orchestrator writes when the first advisory P2 appears, before the PR's dispositions (C-51), and recorded under `## Owned by dotfiles-T128-orchestrator-tools-followup-a04` in this task's acceptance record. The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`. The RESULT names head, base, branch, files, every Bot thread with its disposition, the test names, the caps, `task_copy=<sha256 of .orchestration/dotfiles-T128-orchestrator-tools-followup-a03/task.md>` and the evidence paths.

## Change (bot_rounds, 2026-10-16T06:21:47Z)

The Completion clause's `bot_rounds=1` becomes the template's `bot_rounds=2` form (the Bot's review at PR open and its re-review after the fix round): T13's amendment 6 after the Bot's P2 4290644781 on PR #371, applied to every undispatched task text right before its dispatch and re-confirmed Codex first (C-54). Nothing else changes from the pair-confirmed hash `5a741e63`.

## Change (threat row, 2026-10-16T22:07:03Z, after the RESULT)

The Codex Bot's P1 4299651928 on PR #374's head 57d3577c: uv run from the caller's cwd executes a caller-controlled `.python-version` or venv interpreter even with `--no-project`, which the environment threat row's claim that the cwd chooses nothing did not cover. Operator decision D-P1-374 A: the fix round runs uv from the trusted script root; the row now says so. The dispatched hash `b291ba85` stands (the branch's task copy is byte-identical to it by design); this row is the orchestrator's record, carried by the next boundary.

# Report: dotfiles-T128-orchestrator-tools-followup-a03

- **Seat and branch.** `claude-standard-dot-a003` in `.claude/worktrees/worker-c`, on the fresh branch `tools/dispatch-checker-window`, cut with `--no-track` from `origin/main` at `1d418126`. The earlier branches are left as they are.
- **Task copy.** Byte-identical to the dispatched main-checkout file, sha256 `b291ba85…`, the TASK's `task_sha256` (validation §1).
- **Commits.** `766c1491`: the change, its tests and the task copy; `aeb4a0fb`: this evidence; `c8e813ea`: the Bot's P1 fix; then this evidence's fix-round update.
- cost: n/a (the runtime exposes no token or cost figures to the seat).

## Item 1a: the checker refusal (C-52)

- For an AGMSG-TASK line, after the hash checks and before any read or send, `dispatch.sh` picks the Makefile's `UV_PYYAML` form: `uv run --offline --with pyyaml` when that form imports yaml, else `uv run --with pyyaml`.
- **The brief exemption.** It parses the task file's front matter (the lines between the first two `---` lines) with PyYAML under a `SafeLoader` whose mapping constructor refuses a duplicate key. Only a mapping whose `kind` is the string `review` skips the checker. A parse error, a duplicate key, no closed front matter, no `kind` or any other value runs it.
- **The checker.** `task-consistency-check.py --root <root> <file>` beside the script, as `python -I`. A non-zero exit prints `dispatch: <file> fails the task-consistency check` and the checker's output on stderr, exits 1 and sends nothing.

## Item 1b: the bounded window (C-53)

- Both reads are `history.sh <team> "" <BUS_READ_WINDOW>` (default 200, a positive integer, else usage). `BUS_READ_LIMIT` and the cap refusal are gone.
- **The window file.** `mktemp "${TMPDIR:-/tmp}/dispatch-window.XXXXXX"` (mode 0600), removed by an EXIT trap. The `check` mode writes the pre-send window there: each row's timestamp, sender, recipient and text, never its marker.
- **The alignment.** The `append` mode tries every shift `j` from 0 to `m − 1` and keeps those where the post-send window without its `j` newest rows equals the pre-send window without its `e = n + j − m` oldest (`0 ≤ e < n`). An empty pre-send window takes `j = m`.
- **Outcomes.** Zero or several fits: `does not align uniquely … raise BUS_READ_WINDOW or check the bus`. A unique `j = 0`: `this send added no bus row`. Otherwise the send is the last of the `j` new rows equal to the line, sender and recipient, and none equal: `no new row equals the line`. Every refusal exits 1 with the record unchanged.
- The shdoc header, the `@env BUS_READ_WINDOW` line and the `@exitcode 1` line say so.

## Tests

- `test_dispatch_refuses_a_task_file_failing_the_checker`: the stub checker beside the copied script, a fake `uv` that logs its argv and runs the real `uv` next on PATH. Refused, each with the checker call logged and the C2 line on stderr: `kind: code`, `kind: "code"`, no `kind`, the duplicate key in both orders, and a closed but unparsable front matter with one `kind: review` line. Sent with no checker call: a single `kind: review`. The log's first call is the `UV_PYYAML` probe.
- `test_dispatch_reads_a_bounded_history_window`: the limit argument is 200 on both reads, 50 with `BUS_READ_WINDOW=50`. Recorded once with the right marker: eviction plus collision, same second, and another seat's newer row. Refused with the record unchanged: left the window, no new row, a periodic bus. No `dispatch-window.*` file is left after any case.
- **The module.** 54 tests pass (validation §1). Eight mutants, all killed (validation §2 and §4).
- **Two of the 52 changed.** The cap's removal forced it; the names and edits are in validation §3. The module docstring names its new dependency on a real uv for the checker case.

## Notes

- **The uv form.** The Makefile's `UV_PYYAML` form plus `--no-project`, the Bot's P1 (below): a caller's `pyproject.toml` is never discovered, synced or built.
- **Size.** 105 changed lines outside `tests/` and `.orchestration/` (of 200), 114 added under `tests/` (of 1000), 2 files (validation §4).

## The Bot

- **Code review of `aeb4a0fb`** (review 5545290170): one P1, thread 4292675906, `dispatch.sh:181`, "Isolate uv from the caller's project". `fixed:c8e813ea`: `--no-project` on both uv forms, and the checker test's review brief sent from a directory with an unresolvable `pyproject.toml` (validation §4). The fix round is the PR's one round; the Bot's re-review is asked with `@codex review` on the fix head.
- **Security review of `aeb4a0fb`:** completed, no finding.
- **The PING** of 2026-10-16T21:38:05Z (the host slept overnight) was answered with a PONG, `status=alive`.

## Final state (main-checkout copy only)

- **CI.** All 13 checks pass on `57d3577c`, the final head (validation §5); `mergeStateStatus` is `BLOCKED`, waiting for review.
- **The Bot's re-review of `57d3577c`** (review 5554058212, asked with `@codex review`): one new P1, thread 4299651928, `dispatch.sh:182`, "Run uv outside the caller-controlled directory". `open:4299651928`, `bot_rounds=2`: the one fix round is spent, so it stops the PR and goes to the operator. P1 4292675906 is `fixed:c8e813ea`.
- **The memory add:**

```text
$ uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dotfiles-T128-orchestrator-tools-followup-a03 (PR #374, head 57d3577c): dispatch.sh refuses an AGMSG-TASK whose task file fails task-consistency-check.py (python -I via the UV_PYYAML uv form; only a front matter PyYAML parses, duplicate keys refused, to kind: review is exempt) and both history reads take the newest BUS_READ_WINDOW rows (default 200), the recorder aligning the post-send window with the pre-send one (kept in a mktemp 0600 file, EXIT trap) by the unique fitting shift and recording the last new row equal to the line. Bot: P1 4292675906 (uv discovered the callers pyproject.toml) fixed:c8e813ea with --no-project; the re-review of 57d3577c left P1 4299651928 open (uv still runs a caller .python-version or venv interpreter; fix: run uv from the trusted script root or pin the interpreter), bot_rounds=2, the operators decision. Two of the 52 tests changed with the cap removal (limit 200; the capped-history case dropped, test renamed).'
f603f433-3d66-40c2-9925-a7cb82a4501b
rc=0
```

## Revise round 2 (`8adf74bb`)

- **The P1.** The Bot's re-review of `57d3577c`, thread 4299651928, `dispatch.sh:182`: `--no-project` keeps a caller's `pyproject.toml` out, but a `.python-version` or virtual environment in the caller's directory still chooses uv's interpreter. The operator's decision D-P1-374 A: one more fix round.
- **The fix.** `fixed:8adf74bb`. Both uv forms run in a subshell that changes to the script's checkout root (`uvr`); the checker is named by the script directory's absolute path.
- **The test.** `test_dispatch_refuses_a_task_file_failing_the_checker` plants a `.python-version` naming an executable in the caller's directory: it never runs, and the fake uv records the root as every call's directory. Mutant M9 (no `cd`) is killed; all nine mutants are killed, and 54 tests pass (validation §6).
- **Size after the round.** 108 changed lines outside `tests/` and `.orchestration/` (of 200), 122 added under `tests/` (of 1000), 2 files.
- **The Bot.** Its re-review is asked with `@codex review` on this round's head.

## Round 2: CI and the Bot on `9df6b0c7`, the final head

- **CI.** All 13 checks pass on `9df6b0c7` (validation §7); `mergeStateStatus` is `BLOCKED`, waiting for review.
- **The Bot.** Its code re-review of `9df6b0c7` completed with no finding and a 👍 reaction. Both P1 threads are fixed: 4292675906 `fixed:c8e813ea`, 4299651928 `fixed:8adf74bb`.

## Revise round 3 (`411c7d68`)

- **The P1.** The local review of `9df6b0c7`, `local:9df6b0c:1` (`dispatch.sh:183-185`): an inherited `VIRTUAL_ENV` still chose uv's interpreter after the `cd`. The third finding of one class, the interpreter chosen from caller state. The operator's decision D-S2-374-2 A: one round that closes the class (C-57).
- **The fix.** `fixed:411c7d68`. Both uv forms name `--python`, `python3` as `mise which` answers it under `env -i` at the root (else `python3` on PATH; a non-absolute answer refuses), and run under `env -u` for `VIRTUAL_ENV`, `VIRTUAL_ENV_PROMPT`, `CONDA_PREFIX` and every inherited `UV_*` variable. `--no-project` and the `cd` to the root stay.
- **The test.** `test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state` sets a caller project, a caller `.python-version`, `VIRTUAL_ENV`, `CONDA_PREFIX` and `UV_PYTHON` at once; none is used (validation §8). The checker test's setup is now the shared helper `checker_dispatch`, and its probe assertion expects the pinned `--python`.
- **Checks.** 55 tests pass; twelve mutants, all killed (validation §8).
- **Size after the round.** 120 changed lines outside `tests/` and `.orchestration/` (of 200), 145 added under `tests/` (of 1000), 2 files.
- **The Bot.** Its re-review is asked with `@codex review` on this round's head.

## Round 3: CI and the Bot on `6ae8cf75`, the final head

- **CI.** All 13 checks pass on `6ae8cf75` (validation §9).
- **The Bot.** Its code re-review of `6ae8cf75` left one new P1, thread 4300102967 (`dispatch.sh:197`): the PyYAML probe runs without `-I`, so an inherited `PYTHONPATH` can load a caller's `yaml.py`. `open:4300102967`; the proposed fix is `-I` on the probe (one flag) or `PYTHONPATH` and the `PYTHON*` overrides added to the `env -u` list, with one test planting `yaml.py` on `PYTHONPATH`. `local:9df6b0c:1` is `fixed:411c7d68`; the Bot's earlier P1s stay `fixed:c8e813ea` and `fixed:8adf74bb`.

## Revise round 4 (`b18698d5`)

- **The P1.** The Bot's re-review of `6ae8cf75`, thread 4300102967, `dispatch.sh:197`: the `import yaml` probe ran without `-I`, so an inherited `PYTHONPATH` could load a caller's `yaml.py`. The fourth finding of the class; the operator's decision D-S2-374-3 A: one round that ends the class by an allowlist.
- **The fix.** `fixed:b18698d5`. Both uv forms run under `env -i` with `PATH`, `HOME`, `LANG` and `LC_ALL` when set, and the `AGMSG_*` variables, nothing else; the probe runs `python -I`. The pinned `--python`, `--no-project` and the `cd` to the root stay.
- **The test.** `test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state`, extended: every caller-state source at once, now with a `yaml.py` on `PYTHONPATH`; the fake uv inherits only the allowlisted names (validation §10).
- **Checks.** 55 tests pass; thirteen mutants, all killed (validation §10).
- **Size after the round.** 124 changed lines outside `tests/` and `.orchestration/` (of 200), 153 added under `tests/` (of 1000), 2 files.
- **The Bot.** Its re-review is asked with `@codex review` on this round's head.

## Round 4: CI and the Bot on `9cf65c02`, the final head

- **CI.** All 13 checks pass on `9cf65c02` (validation §11); `mergeStateStatus` is `BEHIND`, since `main` moved.
- **The Bot.** Its code re-review of `9cf65c02` completed with no finding and a 👍 reaction. Every P1 is fixed: 4292675906 `fixed:c8e813ea`, 4299651928 `fixed:8adf74bb`, `local:9df6b0c:1` `fixed:411c7d68`, 4300102967 `fixed:b18698d5`.
---
task_id: dotfiles-T128-orchestrator-tools-followup-a03
seat: claude-standard-dot-a003
permission_gated_commands: 30
---

# Sandbox record: dotfiles-T128-orchestrator-tools-followup-a03

Period: from the AGMSG-TASK (2026-10-16T08:28:10Z) to the RESULT. These ran inside the sandbox: the fetch, the branch, the task copy with its hash (read from the main checkout), the reads, the edits, the tests, shellcheck, shfmt, ruff, the mutation proofs, the repository validator and the commits.

`permission_gated_commands` counts every Bash call made with `dangerouslyDisableSandbox`, one per call, and each `agmsg-dispatch`. This is the main-checkout copy with the final count: fourteen calls. Calls 1 to 13 have run when this copy is written (this copy is call 13), and call 14 is the RESULT that follows it.

| # | Command | Step 4 case |
|--:|---|---|
| 1 | the HTTPS push of `tools/dispatch-checker-window` | `git push` |
| 2 | `gh pr create --draft` and `gh pr ready` (PR #374) | `gh` |
| 3 | `gh pr checks 374 --watch` with the Bot wait beside it (background) | `gh` |
| 4 | `gh api` read of the Bot's summary, review comments and reactions (the security review still running) | `gh` |
| 5 | `gh api` wait until the Bot's security review of `aeb4a0fb` completed, and the re-read | `gh` |
| 6 | `agmsg-dispatch … AGMSG-PONG v1 task_id=dotfiles-T128-orchestrator-tools-followup-a03 status=alive …`, the answer to the PING of 21:38:05Z | `agmsg-dispatch` |
| 7 | the HTTPS push of the fix round's head | `git push` |
| 8 | `gh pr comment 374 --body '@codex review'` | `gh` |
| 9 | `gh pr checks 374 --watch` with the Bot wait beside it on the fix head (background) | `gh` |
| 10 | `gh api` wait until the Bot's code re-review of `57d3577c` completed (the wait script ended on the summary comment first), and the read of the reviews, comments and reactions | `gh` |
| 11 | `gh api repos/mryfmo/dotfiles/pulls/comments/4299651928` (the new P1's body) | `gh` |
| 12 | main-checkout `memory add` | main-checkout `memory add` |
| 13 | the masked copy of the evidence files to the main checkout | artifact copy with the repository masker |
| 14 | `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T128-orchestrator-tools-followup-a03 …` | `agmsg-dispatch` |

**Revise round 2, the final count: nineteen calls.** Round 1's fourteen, and round 2's five: the branch copy counted six in advance, but the re-check of the Bot (its row 18) ran inside the wait call (row 17), so it is not a call of its own.

| # | Command | Step 4 case |
|--:|---|---|
| 15 | the HTTPS push of `9df6b0c7` | `git push` |
| 16 | `gh pr comment 374 --body '@codex review'` (issue comment 6225721682) | `gh` |
| 17 | `gh pr checks 374 --watch`, then the `gh api` wait until the Bot's code re-review of `9df6b0c7` completed, and the read of its reviews, comments and reactions (background) | `gh` |
| 18 | the round-2 sections copied into the main-checkout records, masked again | artifact copy with the repository masker |
| 19 | `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T128-orchestrator-tools-followup-a03 round=2 …` | `agmsg-dispatch` |

**Revise round 3, the final count: twenty-five calls.** Round 2's nineteen, and round 3's six: the branch copy counted five in advance, and the read of the new P1 thread's body (row 23) is the sixth.

| # | Command | Step 4 case |
|--:|---|---|
| 20 | the HTTPS push of `6ae8cf75` | `git push` |
| 21 | `gh pr comment 374 --body '@codex review'` (issue comment 6226303513) | `gh` |
| 22 | `gh pr checks 374 --watch`, then the `gh api` wait until the Bot's code re-review of `6ae8cf75` completed, and the read of its reviews, comments and reactions (background) | `gh` |
| 23 | `gh api repos/mryfmo/dotfiles/pulls/comments/4300102967` (the new P1's body) and the non-passing check filter | `gh` |
| 24 | the round-3 sections copied into the main-checkout records, masked again | artifact copy with the repository masker |
| 25 | `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T128-orchestrator-tools-followup-a03 round=3 …` | `agmsg-dispatch` |

**Revise round 4, the final count: thirty calls.** Round 3's twenty-five, and round 4's five, as the branch copy counted them in advance (the Bot left no new thread, so there was no thread body to read).

| # | Command | Step 4 case |
|--:|---|---|
| 26 | the HTTPS push of `9cf65c02` | `git push` |
| 27 | `gh pr comment 374 --body '@codex review'` (issue comment 6226597044) | `gh` |
| 28 | `gh pr checks 374 --watch`, then the `gh api` wait until the Bot's code re-review of `9cf65c02` completed, and the read of its reviews, comments, reactions and any new thread's body (background) | `gh` |
| 29 | the round-4 sections copied into the main-checkout records, masked again | artifact copy with the repository masker |
| 30 | `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T128-orchestrator-tools-followup-a03 round=4 …` | `agmsg-dispatch` |
---
{
  "format": 1,
  "task": "dotfiles-T128-orchestrator-tools-followup-a03",
  "head": "ef74eaea9a94bff388b7c1027551a57797407b2f",
  "pr": 374,
  "ledger": [
    {
      "id": "4292675906",
      "class": "uv-caller-state-interpreter"
    },
    {
      "id": "4299651928",
      "class": "uv-caller-state-interpreter"
    },
    {
      "id": "4300102967",
      "class": "uv-caller-state-interpreter"
    }
  ],
  "searches": [
    {
      "class": "uv-caller-state-interpreter",
      "records": []
    }
  ],
  "audit_findings": []
}
---

# Acceptance record: dotfiles-T128-orchestrator-tools-followup-a03 (the owner task corrections C-52 (2) and C-53 (2) name)

- 2026-10-15T13:06:18Z record created before the first dispatch; the Codex half of the task-text review runs first, the seat after its confirm (C-54); dispatch waits for the merged tools a02 task and its PR #368 (no wait).
- 2026-10-15T14:41:09Z Codex half round 1 (on ffb4a6db) stalled: the three reviews started 13:07Z together, each transcript (`.agents/worklog/orchestrator-glue/codex-tools-a03-r1.log`) stopped growing at 13:07Z with no final message, and the processes were still alive at 14:24Z (77 minutes); stopped and re-run one at a time, T7 first.
- 2026-10-15T21:59:03Z Codex half round 1 (`…-codex-r1.md`, on ffb4a6db, 76 s, run alone after the stalled run of 13:07Z): `revise`: P1 exempting files by a literal `kind: code` line is not fail-closed (`kind: "code"` would slip past); P2 `uv run --offline` contradicts the index fallback. Round 2: only a file whose front matter is positively a review brief (`kind: review`) is exempt, every other hashed task file is checked; the uv form is the Makefile's `UV_PYYAML` probe (offline when the cache holds PyYAML, else `uv run --with pyyaml`): task sha256 `bddbeaffb85e15ee092c91f44c54ba2d7ffb13df0df1459b12ac7603e5562286`, brief `e3887a695c9e8d2a9def4df8ad20454bfb6ebf570848107428ddae83bb3a93ed`, `presend.sh` OK; Codex round 2 next (C-54).
- 2026-10-15T22:03:29Z Codex half round 2 (`…-codex-r2.md`, on bddbeaff, 80 s): `revise`: P1 the first `kind:` line could be a decoy before a second one; P2 the test lacked a duplicate-key case and an assertion that the checker ran. Round 3: the exemption needs exactly one `kind:` line in the front matter and its value `review`, anything else is checked; the test adds the duplicate case and asserts the checker call through the fake uv's log: task sha256 `7f2f42392809b909eea3f3110d7378e61ea1725c32105aa2a8824dc2843463d8`, brief `a328b9871e0591f16a451d228823c5528791abb67c639623d7c7deb0804a5b3b`, `presend.sh` OK; Codex round 3 next (C-54).
- 2026-10-15T22:05:19Z Codex half round 3 (`…-codex-r3.md`, on 7f2f4239, 79 s): `confirm`, no finding. The seat's round 1 on this hash follows its chain-review-a03 round (one task at a time on the review seat; C-54).
- 2026-10-15T22:17:15Z review seat round 1 (bus 22:15:52Z, on 7f2f4239): `revise`: P2-1 a count within a sliding window fails at the window's edge (an identical row leaving as the new one enters); P3-1 the failing-file case passed for the wrong reason (a checker dying on import yaml prints the same stderr) and the fake uv had no PyYAML; P3-2 presend.sh's premise replay and mask check had no holder after the retirement, and the exitcode line. Round 4: the pre-send read prints the newest row and the post-send read finds the new rows by position after it (refusing when it left the window); a stub checker beside the copied script prints the C2 line, asserted; presend.sh keeps the two other checks; the `@exitcode 1` line names the refusal: task sha256 `bf59ae9d7bbec317fa0507711ce83c986d320a7d6ec6d6f07fd8c4d6e6fe4ef6`, brief `29400b639e49b8c17513dc537d409e89b38a1bd2c6dcdb6f480b7f741df86d05`, `presend.sh` OK; `ACCEPTANCE round=1 status=accepted` sent; Codex round 4 first, the seat's round 2 after its confirm (C-54).
- 2026-10-15T22:19:28Z Codex half round 4 (`…-codex-r4.md`, on bf59ae9d, 70 s): `revise`, P2 the anchor matched by its last occurrence would take a new identical row of the same second for the anchor. Round 5: the pre-send read also prints how many rows identical to the newest row the window holds (k), the post-send read takes the k-th occurrence from the oldest as the anchor, and the test adds the same-second collision case: task sha256 `829ec8e973a868e8021bf75b461a8865ed34426502f08dd82b9739ecf5213f85`, brief `3a6eec3638fc33a63cd488c587385b6535d62ab4f1ba16e9ee789224efe08870`, `presend.sh` OK; Codex round 5 next (C-54).
- 2026-10-15T22:22:41Z Codex half round 5 (`…-codex-r5.md`, on 829ec8e9, 88 s): `revise`, P1 the k-th-occurrence anchor shifts when an older identical row leaves the window (eviction plus collision). Round 6 drops the single-row anchor: the pre-send read keeps its whole window, the post-send window is aligned with it as two views of one bus by the smallest shift j ≥ 1, the last of the j new rows must equal the sent line, and no alignment (more than the window arrived, or the bus does not align), no new row, or an unequal last row refuses with the record unchanged; the test holds the eviction-plus-collision, same-second, left-the-window and no-new-row cases: task sha256 `efd1ab960bdbe47f841e4b616654a115fd49896a111868c921ee66deefd98542`, brief `2ef4535ae8fa4fd77940b6b5991fbc367b962ddb1a6d6107c605e9fffde3cf96`, `presend.sh` OK; Codex round 6 next (C-54).
- 2026-10-15T22:26:29Z Codex half round 6 (`…-codex-r6.md`, on efd1ab96, 69 s): `revise`, P1 a closed but invalid front matter with one literal `kind: review` line was exempt without a YAML parse. Round 7: the exemption needs a successful PyYAML parse under a duplicate-key-refusing loader yielding `review` for `kind`, through the same uv form; a parse failure, a duplicate key or another value runs the checker; the test adds the malformed case: task sha256 `141d0113657964a4f864b0e2428faf256615f778c365cc0dcb599969d394c987`, brief `6fcc481790ac41b2b840e882dbfafbcd2521e0f8d6751144b0454b392c43e396`, `presend.sh` OK; Codex round 7 next (C-54).
- 2026-10-15T22:28:40Z Codex half round 7 (`…-codex-r7.md`, on 141d0113, 67 s): `revise`, P1 the fake uv ran python without PyYAML, so the YAML parse that identifies a brief could not run in the tests. Round 8: the fake uv records its argv and delegates to the real uv found later on PATH (PyYAML as in production, the Makefile's probe form), the checker staying the stub beside the copied script: task sha256 `01ad84d61ab5740621cb030f7ff5cc88e8f0375390fead9c6492b55f096c064b`, brief `dd0776da84221cbd9eb0774ee15af991f3a03ce8b94657fc3727ea28bc53cfc0`, `presend.sh` OK; Codex round 8 next (C-54).
- 2026-10-15T22:30:15Z Codex half round 8 (`…-codex-r8.md`, on 01ad84d6, 48 s): `revise`, P1 the alignment allowed empty compared slices (j = m, e = n), so a pre-send window that left entirely could align falsely. Round 9: a nonempty overlap is required (j < m) unless the pre-send window was empty: task sha256 `2785ac025f16a09051a9bcd5524891478205c426623cccc620fb26d1678ebbe2`, brief `da31b3595b2e830e8b0139fbf480ffd92934247632a77ad827f513386d2775e7`, `presend.sh` OK; Codex round 9 next (C-54).
- 2026-10-15T22:32:11Z Codex half round 9 (`…-codex-r9.md`, on 2785ac02, 64 s): `revise`, P2 the pre-send window file under `$TMPDIR` had no collision-safe creation, cleanup or control row. Round 10: a private `mktemp` file (mode 0600) removed by an EXIT trap whatever the exit, holding the four fields only, with its own threat row: task sha256 `3f5caedf626ec1644df113e7404a132af2c60693efe9f445d5f8c23edecec086`, brief `2a93b6ec58bbf33685a795fb2a10f0cc5b63e675bab9bd3522b5e2534f457650`, `presend.sh` OK; Codex round 10 next (C-54).
- 2026-10-15T22:34:38Z Codex half round 10 (`…-codex-r10.md`, on 3f5caedf, 80 s): `revise`, P1 the smallest fitting shift is not fail-closed on a periodic bus (a full window of identical rows fits shift 1 as well as no change). Round 11: every shift from no change to m minus 1 is tried and exactly one may fit; a unique no-change fit refuses as no new row, zero or several fits refuse as ambiguous; the test adds the periodic-bus case: task sha256 `296f35d9c815a33d3873b9abca0ee4d70546383fb34ed8be3d5707708a99a089`, brief `8bec237cac18e2cc81512a9ac803ee01a53f551da946f4417f1d0fe4207f807f`, `presend.sh` OK; Codex round 11 next (C-54).
- 2026-10-15T22:37:04Z Codex half round 11 (`…-codex-r11.md`, on 296f35d9, 112 s): `confirm`, no finding (eleven Codex rounds, each a distinct defect of the recorder's window logic or the exemption; M-20261015-06's class, Codex-first keeping the seat to two rounds). The seat's round 2 on the same hash dispatched through `dispatch-direct.sh` (C-54).
- 2026-10-15T22:42:43Z review seat round 2 (bus 22:41:42Z, on 296f35d9): `revise`: P2-1 the acceptance rule took only the newest new row for the send, while another seat's line can land newest before the post-send read (agmsg-dispatch returns after the read); P3-1 the fake uv made the module's first real uv call and the sentence called the dependency existing. Round 12: among the new rows the last one equal to the line in sender, recipient and text is the send, refused only when none is; the fake uv runs the `UV_PYYAML` probe form itself (`--offline` when the cache holds PyYAML) and the sentence names the dependency as new: task sha256 `5a741e63e619ad31f83f10516be178f0ba63490bca2d4e16f9e45c14d4070b0a`, brief `5a189d71db69b6a482b01decec362514f370dec364977a9b662b34281cb0487e`, `presend.sh` OK; `ACCEPTANCE round=2 status=accepted` sent; Codex round 12 first, the seat's round 3 after its confirm (C-54).
- 2026-10-15T22:44:43Z Codex half round 12 (`…-codex-r12.md`, on 5a741e63, 87 s): `confirm`, no finding. The seat's round 3 on the same hash dispatched through `dispatch-direct.sh` (C-54).
- 2026-10-15T22:46:33Z review seat round 3 (bus 22:46:06Z, on 5a741e63): `confirm`; the Codex half confirmed the same hash (`…-codex-r12.md`). **Pair-confirmed: task sha256 `5a741e63e619ad31f83f10516be178f0ba63490bca2d4e16f9e45c14d4070b0a`** (Codex rounds 1 to 12, seat rounds 1 to 3; C-54 held throughout). `ACCEPTANCE round=3 status=accepted` sent. Dispatch after boundary (16), to a free Claude seat (the tools a02 PR is merged, `after:` is satisfied).
- 2026-10-16T08:28:22Z review seat round 4 (bus 08:27:35Z, on b291ba85): `confirm`; with the Codex confirm (round 13) **tools-a03 is pair-confirmed again at `b291ba85f89d46877f74969d4e33ce994ff875f83454df58dbd8037a7d745da7`**; presend rc 0 (premises hold on 1d418126); the TASK line to `claude-standard-dot-a003` (worker-c, wA:p3) by dispatch-direct at 2026-10-16T08:28:22Z.

## Ledger of the Bot reviews on PR #374 (rows id<TAB>class)

4292675906	uv-caller-state-interpreter
4299651928	uv-caller-state-interpreter
4300102967	uv-caller-state-interpreter

- 2026-10-16T21:57:29Z RESULT round 1 `status=done` (bus 21:56:07Z): PR #374 `tools/dispatch-checker-window`, head 57d3577c on base 1d418126 (766c1491 change and task copy, aeb4a0fb evidence, c8e813ea the Bot P1 fix, 57d3577c fix-round evidence); dispatch.sh refuses a task file failing the checker and reads a bounded history window; tests `test_dispatch_refuses_a_task_file_failing_the_checker` and `test_dispatch_reads_a_bounded_history_window`, two existing tests edited for the cap removal, 54 of 54, 8 of 8 mutants; caps 105 / 114; CI 13 pass; security review on aeb4a0fb clean; task_copy b291ba85. Bot: 4292675906 (P1, uv without --no-project discovering the caller's pyproject) `fixed:c8e813ea`; the re-review of 57d3577c left 4299651928 (P1): uv still executes a caller cwd's `.python-version` interpreter (`./pwn`) even with `run --no-project` (uv 0.7.22), and `--no-project` still uses a venv found in the current or parent directory; remedy: run uv from the trusted script root or pin the interpreter; the threat row claiming the caller cwd chooses nothing is contradicted. The one fix round is spent (`bot_rounds=2`), so the Completion clause sends the PR to the operator: D-P1-374 in plan 022 (default A), ACCEPTANCE `pending-integration` hold at 2026-10-16T21:57:29Z.
- 2026-10-16T22:06:27Z operator decision D-P1-374 (AskUserQuestion, answer A, recorded in plan 022): one more fix round for 4299651928 (uv run from the trusted script root, one test; the task text's threat row corrected by the orchestrator); revise line to a003 at 2026-10-16T22:06:27Z; `4299651928` becomes `fixed:<sha>` with the RESULT.
- 2026-10-16T22:27:40Z RESULT round 2 `status=done` (bus 22:25:43Z): head 9df6b0c7 (fix 8adf74bb: both uv forms run in a subshell cd'd to the script's checkout root; the checker named by the script directory's absolute path); `4299651928 fixed:8adf74bb`; the Bot's re-review of 9df6b0c7 without findings; 54 of 54 tests, 9 of 9 mutants, caps 108 / 122, CI 13 pass; `374-extra.tsv` holds both P1 rows as fixed. ACCEPTANCE `pending-integration` at 22:26:54Z; the owner task `dotfiles-T128-orchestrator-tools-followup-a04` written (C-51) and the chain (`374-chain1.log`, Bot wait 5 min) starts now; PR #372's chain resumes after a002's fix round.

## Local review of 9df6b0c (the fix-round head): one P1 (rows id<TAB>class)

local:9df6b0c:1	uv-caller-state-interpreter
local-finding: 9df6b0c:1 fixed:411c7d68

- 2026-10-16T22:38:10Z the chain on 9df6b0c7 (`374-chain1.log`): CI pass, no Bot review in the 5-minute wait, sandbox scan clean, sweep 13 items / 0 gaps; the local review (`…-local-review-9df6b0c.md`) found a P1: an inherited `VIRTUAL_ENV` pointing at a PR checkout's `.venv` still selects uv's interpreter after the cd, so its site-packages can run during the `import yaml` probe before validation. The third finding of one class (the interpreter chosen from caller state), so the three rows carry one slug, `uv-caller-state-interpreter`, and the S6 search ran (M-20261017-02, C-57: name the interpreter, strip the inherited environment):

```
search: uv-caller-state-interpreter -> M-20261017-02.md
search-body: uv-caller-state-interpreter -> M-20261017-02.md
compactiondb: uv-caller-state-interpreter -> 0 matches
```

- 2026-10-16T22:38:10Z a further fix round makes INV-6 read `revises 2` (S2): D-S2-374-2 (default A: one round that closes the class, pinning the interpreter and stripping VIRTUAL_ENV and the UV_* overrides, with one test setting every caller-state source at once); hold ACCEPTANCE at 2026-10-16T22:38:10Z.
- 2026-10-16T22:42:38Z operator decision D-S2-374-2 (AskUserQuestion, answer A, recorded in plan 022): the class-closing fix round (pin the interpreter, strip the inherited environment, one test with every caller-state source set) sent to a003 at 2026-10-16T22:42:38Z; `local:9df6b0c:1` becomes `fixed:<sha>` with the RESULT.
- 2026-10-16T23:14:12Z RESULT round 3 `status=done` (bus 23:13:19Z): head 6ae8cf75 (fix 411c7d68: both uv forms name `--python` (python3 from `mise which` under `env -i` at the root, else python3 on PATH; a non-absolute path refuses) and run under `env -u VIRTUAL_ENV, VIRTUAL_ENV_PROMPT, CONDA_PREFIX` and every inherited `UV_*`, keeping `--no-project` and the cd); test `test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state`; 12 of 12 mutants, 55 of 55 tests, caps 120 / 145, CI 13 pass; `local:9df6b0c:1 fixed:411c7d68`. The Bot's re-review of 6ae8cf75: P1 4300102967, the `import yaml` probe runs without `-I`, so an inherited PYTHONPATH loads a caller's yaml.py (the fourth finding of the class: the environment was stripped by a denylist, and PYTHON* was not on it). A further round makes INV-6 read `revises 3`: D-S2-374-3 (default A: end the class by allowlist, `env -i` with PATH, HOME and the agmsg variables for the probe and the checker, plus `-I` on the probe; one test planting yaml.py on PYTHONPATH and every earlier source at once); hold ACCEPTANCE at 2026-10-16T23:14:12Z.
- 2026-10-16T23:16:22Z operator decision D-S2-374-3 (AskUserQuestion, answer A, recorded in plan 022): the allowlist round (env -i with an explicit allowlist for the probe and the checker, -I on the probe, one test planting every source at once) sent to a003 at 2026-10-16T23:16:22Z; `4300102967` becomes `fixed:<sha>` with the RESULT. C-57's method gains the allowlist form.
- 2026-10-16T23:59:11Z RESULT round 4 `status=done` (bus 23:38:46Z): head 9cf65c02 (fix b18698d5: both uv forms run under `env -i` with PATH, HOME, LANG/LC_ALL when set and the AGMSG_* variables only; the probe runs `python -I`; the pinned `--python`, `--no-project` and the cd kept); `4300102967 fixed:b18698d5`; the Bot's re-review of 9cf65c02 without findings; the test extended to every caller-state source at once (the fake uv inherits only the allowlisted variables); 13 of 13 mutants, 55 of 55 tests, caps 124 / 153, CI 13 pass (BEHIND: main moved). ACCEPTANCE `pending-integration` at 2026-10-16T23:59:11Z; the chain runs after PR #376's.


## Owned by dotfiles-T128-orchestrator-tools-followup-a04 (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)

local:ef74eae:1	advisory-p2
local-finding: ef74eae:1 not-applicable:advisory P2 owned by dotfiles-T128-orchestrator-tools-followup-a04 (- [P2] Allow concurrent rows to interleave in timestamp-ordered history — scripts/orchestrator/dispatch.sh:283-284); evidence=git show origin/main:.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a04.md | grep -n 'item 1'
local:ef74eae:2	advisory-p2
local-finding: ef74eae:2 not-applicable:advisory P2 owned by dotfiles-T128-orchestrator-tools-followup-a04 (- [P2] Exclude impossible evictions from underfull history windows — scripts/orchestrator/dispatch.sh:284-285); evidence=git show origin/main:.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a04.md | grep -n 'item 1'

## Dispatch (bus lines)

- AGMSG-TASK v1 task_id=dotfiles-T128-orchestrator-tools-followup-review-a03 round=1 repo=~/Workspace/dotfiles task_file=.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-review-a03.md task_sha256=a328b9871e0591f16a451d228823c5528791abb67c639623d7c7deb0804a5b3b tools_task_file=.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a03.md tools_task_sha256=7f2f42392809b909eea3f3110d7378e61ea1725c32105aa2a8824dc2843463d8 deadline=none note=one-round-review-of-the-owner-task-corrections-C-52-(2)-and-C-53-(2)-name(the-Codex-half-confirmed-first,C-54);answer-with-AGMSG-RESULT-verdict=confirm|revise-tools_task_sha256=<sha> read_at=read
- AGMSG-TASK v1 task_id=dotfiles-T128-orchestrator-tools-followup-review-a03 round=2 repo=~/Workspace/dotfiles task_file=.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-review-a03.md task_sha256=8bec237cac18e2cc81512a9ac803ee01a53f551da946f4417f1d0fe4207f807f tools_task_file=.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a03.md tools_task_sha256=296f35d9c815a33d3873b9abca0ee4d70546383fb34ed8be3d5707708a99a089 deadline=none note=one-round-review-of-the-owner-task-corrections-C-52-(2)-and-C-53-(2)-name(the-Codex-half-confirmed-first,C-54;your-round-1-applied:the-window-read-anchored-on-the-newest-pre-send-row-not-a-count,the-checker-s-own-line-asserted-through-a-stub-checker-beside-the-copied-script,presend.sh-keeps-the-premise-replay-and-the-mask-check,the-exitcode-line;the-Codex-rounds-4-and-5:the-two-windows-are-aligned-as-views-of-one-bus-by-the-smallest-shift,the-last-new-row-must-equal-the-line,anything-else-refused,with-eviction-and-collision-cases;the-Codex-round-6-P1:the-exemption-needs-a-successful-duplicate-rejecting-YAML-parse-yielding-review,a-malformed-front-matter-is-checked;the-Codex-round-7-P1:the-fake-uv-delegates-to-the-real-uv-so-PyYAML-is-present-as-in-production;the-Codex-round-8-P1:a-nonempty-overlap-is-required-unless-the-pre-send-window-was-empty;the-Codex-round-9-P2:the-pre-send-window-file-is-a-private-mktemp-file-removed-by-a-trap,with-its-own-row;the-Codex-round-10-P1:the-alignment-must-be-unique-across-every-shift-including-no-change,else-refused,with-a-periodic-bus-case);answer-with-AGMSG-RESULT-verdict=confirm|revise-tools_task_sha256=<sha> read_at=read
- AGMSG-TASK v1 task_id=dotfiles-T128-orchestrator-tools-followup-review-a03 round=3 repo=~/Workspace/dotfiles task_file=.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-review-a03.md task_sha256=5a189d71db69b6a482b01decec362514f370dec364977a9b662b34281cb0487e tools_task_file=.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a03.md tools_task_sha256=5a741e63e619ad31f83f10516be178f0ba63490bca2d4e16f9e45c14d4070b0a deadline=none note=one-round-review-of-the-owner-task-corrections-C-52-(2)-and-C-53-(2)-name(the-Codex-half-confirmed-first,C-54;your-round-1-applied:the-window-read-anchored-on-the-newest-pre-send-row-not-a-count,the-checker-s-own-line-asserted-through-a-stub-checker-beside-the-copied-script,presend.sh-keeps-the-premise-replay-and-the-mask-check,the-exitcode-line;the-Codex-rounds-4-and-5:the-two-windows-are-aligned-as-views-of-one-bus-by-the-smallest-shift,the-last-new-row-must-equal-the-line,anything-else-refused,with-eviction-and-collision-cases;the-Codex-round-6-P1:the-exemption-needs-a-successful-duplicate-rejecting-YAML-parse-yielding-review,a-malformed-front-matter-is-checked;the-Codex-round-7-P1:the-fake-uv-delegates-to-the-real-uv-so-PyYAML-is-present-as-in-production;the-Codex-round-8-P1:a-nonempty-overlap-is-required-unless-the-pre-send-window-was-empty;the-Codex-round-9-P2:the-pre-send-window-file-is-a-private-mktemp-file-removed-by-a-trap,with-its-own-row;the-Codex-round-10-P1:the-alignment-must-be-unique-across-every-shift-including-no-change,else-refused,with-a-periodic-bus-case;your-round-2:among-the-new-rows-the-last-one-equal-to-the-line-is-the-send,the-fake-uv-runs-the-probe-form-itself,the-module-s-uv-dependency-named-as-new);answer-with-AGMSG-RESULT-verdict=confirm|revise-tools_task_sha256=<sha> read_at=read
- AGMSG-TASK v1 task_id=dotfiles-T128-orchestrator-tools-followup-review-a03 round=4 repo=~/Workspace/dotfiles task_file=.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-review-a03.md task_sha256=5a189d71db69b6a482b01decec362514f370dec364977a9b662b34281cb0487e tools_task_file=.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a03.md tools_task_sha256=b291ba85f89d46877f74969d4e33ce994ff875f83454df58dbd8037a7d745da7 deadline=none note=round-4-a-re-confirm-after-one-change-since-the-pair-confirmed-5a741e63:the-Change(bot_rounds)section-names-it,the-Completion-clause-s-bot_rounds=1-becoming-the-template-s-bot_rounds=2-form(the-Bot-s-review-at-PR-open-and-its-re-review-after-the-fix-round;T13-amendment-6);judge-that-nothing-else-changed-and-the-clause-reads-consistently;the-Codex-half-confirmed(round-13);answer-with-AGMSG-RESULT-verdict=confirm|revise-tools_task_sha256=<sha> read_at=read
- AGMSG-TASK v1 task_id=dotfiles-T128-orchestrator-tools-followup-a03 round=1 repo=~/Workspace/dotfiles/.claude/worktrees/worker-c task_file=.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a03.md task_sha256=b291ba85f89d46877f74969d4e33ce994ff875f83454df58dbd8037a7d745da7 deadline=none note=plan-022-tools-a03(dispatch.sh:the-checker-refusal-and-the-bounded-aligned-window-reads,C-52/C-53-tool-halves);pair-confirmed-at-this-hash(Codex-round-13,seat-round-4);read-the-task-file-first,fresh-branch-from-origin/main(1d418126-or-later),one-PR,the-Bot-reviews-once-at-PR-open,RESULT-per-Worker-Playbook-step-15 read_at=read
- AGMSG-ACCEPTANCE v1 task_id=dotfiles-T128-orchestrator-tools-followup-a03 round=1 status=pending-integration reason=RESULT-read:head-57d3577c,CI-13-pass,4292675906-fixed:c8e813ea,the-Bot-s-re-review-P1-4299651928(uv-runs-a-caller-cwd-interpreter)survives-the-one-fix-round,so-the-Completion-clause-sends-it-to-the-operator(D-P1-374,default-A:one-more-fix-round,uv-run-from-the-trusted-script-root);hold-until-the-decision;nothing-to-do-on-your-side previous_head=57d3577ca780248f573fd26c4fa460e2b5e2d510 next_action=none-until-the-decision read_at=read
- AGMSG-ACCEPTANCE v1 task_id=dotfiles-T128-orchestrator-tools-followup-a03 round=1 status=revise reason=operator-decision-D-P1-374-A(AskUserQuestion,plan-022):one-more-fix-round-for-the-Bot-s-P1-4299651928-on-57d3577c:run-both-uv-commands-from-the-trusted-script-root(uv---directory-<root>-or-a-cd-subshell-to-git-rev-parse---show-toplevel-of-the-script)so-a-caller-cwd-s-.python-version-or-venv-chooses-nothing,one-test(the-uv-shim-records-the-directory-it-ran-in-or-a-caller-cwd-.python-version-./pwn-is-not-executed);the-task-text-s-threat-row-is-corrected-by-the-orchestrator(Change-note);commit,push,@codex-review,RESULT-naming-4299651928-fixed:<sha> check=tests/unit/test_orchestrator_tools.py(the-new-test,named-in-the-RESULT) previous_head=57d3577ca780248f573fd26c4fa460e2b5e2d510 next_action=fix-round,commit,push,@codex-review,RESULT read_at=read
- AGMSG-ACCEPTANCE v1 task_id=dotfiles-T128-orchestrator-tools-followup-a03 round=2 status=pending-integration reason=RESULT-round-2-read:head-9df6b0c7,both-Bot-P1-fixed(4292675906:c8e813ea,4299651928:8adf74bb:uv-in-a-subshell-cd-to-the-script-s-checkout-root);the-chain-runs-on-this-head(CI,Bot-wait,sandbox-scan,local-review,sweep,receipt,audit);the-orchestrator-replies-to-and-resolves-the-threads;nothing-to-do-on-your-side previous_head=9df6b0c7594cef7f42e9a43faa3e08d0f035e329 next_action=none-until-the-integration-result read_at=read
- AGMSG-ACCEPTANCE v1 task_id=dotfiles-T128-orchestrator-tools-followup-a03 round=2 status=pending-integration reason=the-local-review-of-9df6b0c7-found-a-P1(dispatch.sh-183-185:an-inherited-VIRTUAL_ENV-still-selects-uv-s-interpreter-after-the-cd,so-a-PR-checkout-s-.venv-can-run-during-the-import-yaml-probe);the-third-finding-of-one-class(the-interpreter-chosen-from-caller-state:pyproject,.python-version,VIRTUAL_ENV);the-chain-stopped-before-the-audit;a-further-fix-round-makes-INV-6-read-revises-2,so-it-waits-for-the-operator-s-decision-D-S2-374-2(default-A:one-round-that-closes-the-class:pin-the-interpreter-and-strip-the-inherited-env);hold previous_head=9df6b0c7594cef7f42e9a43faa3e08d0f035e329 next_action=none-until-the-decision read_at=unread
- AGMSG-ACCEPTANCE v1 task_id=dotfiles-T128-orchestrator-tools-followup-a03 round=2 status=revise reason=operator-decision-D-S2-374-2-A(AskUserQuestion,plan-022:S2-waived):one-round-that-closes-the-class(C-57,identity-over-shape):both-uv-invocations-name-the-interpreter(--python-<the-trusted-interpreter-resolved-at-the-script-s-checkout-root,e.g.-the-python3-mise-provides-there>)and-run-under-an-environment-without-VIRTUAL_ENV,VIRTUAL_ENV_PROMPT,UV_PROJECT_ENVIRONMENT,UV_PYTHON-and-the-other-UV_*-overrides(env--u-…-or-an-explicit-allowlisted-env),keeping---no-project-and-the-cd-to-the-root;one-test-that-sets-a-caller-pyproject,a-caller-cwd-.python-version-and-VIRTUAL_ENV-at-once-and-asserts-none-is-used(the-fake-uv-records-its-env-and-args);nothing-else;commit,push,@codex-review,RESULT-naming-local:9df6b0c:1-fixed:<sha>-and-the-test check=tests/unit/test_orchestrator_tools.py(the-new-test,named-in-the-RESULT) previous_head=9df6b0c7594cef7f42e9a43faa3e08d0f035e329 next_action=fix-round,commit,push,@codex-review,RESULT read_at=unread
- AGMSG-ACCEPTANCE v1 task_id=dotfiles-T128-orchestrator-tools-followup-a03 round=3 status=pending-integration reason=RESULT-round-3-read:head-6ae8cf75,local:9df6b0c:1-fixed:411c7d68(pinned---python,env--u-VIRTUAL_ENV/CONDA_PREFIX/UV_*),12-mutants,CI-13-pass;the-Bot-s-re-review-P1-4300102967(the-import-yaml-probe-without--I,an-inherited-PYTHONPATH-loads-a-caller-s-yaml.py)is-the-fourth-finding-of-the-class;a-further-round-makes-INV-6-read-revises-3,so-it-waits-for-the-operator-s-decision-D-S2-374-3(default-A:one-round-that-ends-the-class-by-allowlist:env--i-with-an-explicit-PATH/HOME/agmsg-variable-allowlist-for-the-probe-and-the-checker,plus--I-on-the-probe);hold previous_head=6ae8cf75df74bb54eb3b724ea7c94e16b70759ef next_action=none-until-the-decision read_at=read
- AGMSG-ACCEPTANCE v1 task_id=dotfiles-T128-orchestrator-tools-followup-a03 round=3 status=revise reason=operator-decision-D-S2-374-3-A(AskUserQuestion,plan-022:S2-waived):one-round-that-ends-the-class-by-allowlist,not-denylist:run-the-import-yaml-probe-and-the-checker-under-env--i-with-an-explicit-allowlist(PATH-as-the-script-computes-it,HOME,LANG/LC_ALL-if-needed,the-AGMSG_*-variables-the-scripts-read,and-nothing-else),the-probe-with-python-s--I,keeping-the-pinned---python,--no-project-and-the-cd-to-the-root;one-test-that-plants-every-caller-state-source-at-once(a-caller-pyproject,a-cwd-.python-version,VIRTUAL_ENV,CONDA_PREFIX,UV_PYTHON-and-a-yaml.py-on-PYTHONPATH)and-asserts-the-fake-uv-and-the-probe-see-only-the-allowlisted-variables;nothing-else;commit,push,@codex-review,RESULT-naming-4300102967-fixed:<sha>-and-the-test check=tests/unit/test_orchestrator_tools.py(the-new-or-extended-test,named-in-the-RESULT) previous_head=6ae8cf75df74bb54eb3b724ea7c94e16b70759ef next_action=fix-round,commit,push,@codex-review,RESULT read_at=read
- AGMSG-ACCEPTANCE v1 task_id=dotfiles-T128-orchestrator-tools-followup-a03 round=4 status=pending-integration reason=RESULT-round-4-read:head-9cf65c02,4300102967-fixed:b18698d5(the-allowlist-form:env--i-with-PATH,HOME,LANG/LC_ALL,AGMSG_*;python--I-on-the-probe),13-mutants,CI-13-pass,the-Bot-s-re-review-clean;the-chain-runs-after-PR-376-s(one-chain-at-a-time;main-moved,so-update-branch-first);nothing-to-do-on-your-side;you-are-free previous_head=9cf65c0299645e30e54419668ba523eff9c4897e next_action=none-for-this-task read_at=read

 succeeded in 239ms:
diff --git a/scripts/orchestrator/dispatch.sh b/scripts/orchestrator/dispatch.sh
index a93367c5..89ecb72e 100755
--- a/scripts/orchestrator/dispatch.sh
+++ b/scripts/orchestrator/dispatch.sh
@@ -34,15 +34,28 @@
 #   (thread 4255272797). A record that is not an existing regular file writable in a
 #   writable directory, or whose `task` is not the line's `task_id`, is refused
 #   before the send, and nothing is sent.
-#   Only a bus row this send created is recorded: the rows matching the line,
-#   sender and recipient are counted before and after the send, and a send that
-#   added none leaves the record unchanged and exits 1. The read state is the
-#   marker the team-wide `history.sh <team> "" <BUS_READ_LIMIT>` prints for the new row
+#   An AGMSG-TASK line whose `task_file=` fails `task-consistency-check.py`
+#   (beside this script, run as `python -I` through the Makefile's `UV_PYYAML`
+#   uv form with `--no-project` and a pinned `--python`, from the root, under `env -i` with only `PATH`, `HOME`,
+#   `LANG`, `LC_ALL` and the `AGMSG_*` variables) is refused with the checker's output, and nothing is sent (C-52).
+#   Only a review brief is exempt: a front matter (the text between the first
+#   two `---` lines) that PyYAML parses, refusing a duplicate key, to a mapping
+#   whose `kind` is the string `review`; every other outcome runs the checker.
+#   Only a bus row this send created is recorded. Both reads of the team-wide
+#   `history.sh <team> "" <BUS_READ_WINDOW>` take the newest rows (C-53: a
+#   whole-bus read took 56 minutes on a 1385-row team), and the recorder aligns
+#   them as two views of one bus: the pre-send window (each row's timestamp,
+#   sender, recipient and text) goes to a private `mktemp` file removed on exit;
+#   after the send every shift j from 0 to m-1 of the m post-send rows is tried,
+#   and exactly one may leave the post-send window, without its j newest rows,
+#   equal to the pre-send window without the rows that left it (all m new rows
+#   when the pre-send window was empty). This send is the last of those j new
+#   rows equal to the line, sender and recipient. No fit, several fits (a
+#   periodic bus), j = 0 or no equal new row leaves the record unchanged and
+#   exits 1. The read state is the marker history.sh prints for that row
 #   (`●` unread, `○` read): agmsg's scripts expose no read_at time, this script
 #   never reads the message database, and it never passes an agent to
-#   history.sh, whose agent argument renames the caller's pane after it. A read
-#   whose non-empty lines reach the limit may have lost its oldest rows, so it
-#   is refused before the send (thread 4255272803).
+#   history.sh, whose agent argument renames the caller's pane after it.
 # @arg $1 string agmsg team.
 # @arg $2 string Sender identity.
 # @arg $3 string Recipient identity.
@@ -50,9 +63,9 @@
 # @arg $5 path File holding the line.
 # @arg $6 path Optional acceptance record (`.orchestration/acceptance/<task>.md`), relative to the current directory.
 # @env AGMSG_SCRIPTS The agmsg scripts directory (default `$HOME/.agents/skills/agmsg/scripts`).
-# @env BUS_READ_LIMIT The row limit of the history read (default 100000).
+# @env BUS_READ_WINDOW The newest rows each history read takes (default 200, a positive integer).
 # @exitcode 0 Sent, and recorded when a record was given (agmsg-dispatch's own status otherwise).
-# @exitcode 1 A field check failed, the record is malformed, or the sent line was not recorded.
+# @exitcode 1 A field check failed, the task file fails the task-consistency check, the record is malformed, or the sent line was not recorded.
 # @exitcode 2 Usage error, or the file is not one AGMSG-TASK, AGMSG-ACCEPTANCE or AGMSG-PING v1 line.
 # @example
 #   scripts/orchestrator/dispatch.sh dotfiles-conformance claude-deep-dot claude-standard-dot-a003 w5:pA \
@@ -162,15 +175,63 @@ for t in "${tokens[@]}"; do
         exit 1
     }
 done
+if [[ ${tokens[0]} == AGMSG-TASK ]]; then
+    tf="$(value_of task_file)" && [[ ${tf} == /* ]] || tf="${root}/${tf}"
+    # The Makefile's UV_PYYAML: offline when the cache holds PyYAML, else through the index. --no-project: a
+    # pyproject.toml in the caller's directory is never discovered, synced or built (the Bot's P1 4292675906).
+    # The interpreter is named, python3 as mise answers it under env -i at the root, else python3 on PATH, and uv
+    # runs under env -i with an allowlist, so no VIRTUAL_ENV, CONDA_PREFIX, UV_* or PYTHON* variable reaches it
+    # (local:9df6b0c:1, C-57, the Bot's P1 4300102967).
+    py="$(cd -- "${root}" && { env -i PATH="${PATH}" HOME="${HOME}" mise which python3 2> /dev/null || command -v python3; })" || py=
+    [[ ${py} == /* ]] || {
+        echo "dispatch: no python3 interpreter to pin for uv" >&2
+        exit 1
+    }
+    clean=(env -i PATH="${PATH}" HOME="${HOME}")
+    for v in LANG LC_ALL; do
+        [[ -z ${!v:-} ]] || clean+=("${v}=${!v}")
+    done
+    while IFS= read -r v; do
+        [[ ${v} != AGMSG_* ]] || clean+=("${v}=${!v}")
+    done < <(compgen -e)
+    uvy=(uv run --no-project --offline --python "${py}" --with pyyaml)
+    here="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
+    # Run from the trusted root, so a caller's .python-version or virtual environment picks no interpreter (4299651928).
+    uvr() { (cd -- "${root}" && "${clean[@]}" "${uvy[@]}" "$@"); }
+    uvr python -I -c 'import yaml' > /dev/null 2>&1 || uvy=(uv run --no-project --python "${py}" --with pyyaml)
+    read -r -d '' brief << 'PY' || true
+import sys, yaml
+def unique(loader, node, deep=False):
+    keys = [loader.construct_object(k, deep=deep) for k, _ in node.value]
+    if len(keys) != len(set(keys)):
+        raise yaml.YAMLError("duplicate key")
+    return loader.construct_mapping(node, deep)
+class Loader(yaml.SafeLoader):
+    pass
+Loader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique)
+lines = open(sys.argv[1], encoding="utf-8").read().split("\n")
+end = lines.index("---", 1) if lines[0] == "---" else None
+front = yaml.load("\n".join(lines[1:end]), Loader) if end else None
+sys.exit(0 if isinstance(front, dict) and front.get("kind") == "review" else 1)
+PY
+    # Fail-closed: only a parsed front matter whose kind is review skips the checker.
+    if ! uvr python -I -c "${brief}" "${tf}" > /dev/null 2>&1; then
+        out="$(uvr python -I "${here}/task-consistency-check.py" --root "${root}" "${tf}" 2>&1)" || {
+            echo "dispatch: ${tf} fails the task-consistency check" >&2
+            printf '%s\n' "${out}" >&2
+            exit 1
+        }
+    fi
+fi
 [[ -n ${record} ]] || exec agmsg-dispatch "${team}" "${from}" "${to}" "${pane}" "${line}"
 
-# Modes: `check` parses the record; `append` finds the sent line in history.sh's
-# output on stdin, takes its read marker (● unread, ○ read) and appends it.
+# Modes: `check` parses the record and writes the pre-send window to the window file; `append` aligns
+# history.sh's post-send window on stdin with it, takes the sent row's read marker (● unread, ○ read) and appends it.
 read -r -d '' recorder << 'PY' || true
 import fcntl, json, os, re, shutil, sys, tempfile
 from pathlib import Path
 
-mode, path, line, sender, to, before, task, limit = sys.argv[1:9]
+mode, path, line, sender, to, window, task = sys.argv[1:8]
 record = Path(path)
 rows = [r for r in sys.stdin.read().splitlines() if r]
 
@@ -207,21 +268,35 @@ def load():
         sys.exit(f"dispatch: {path} is the record of task {block['task']}, the line is task {task}")
     return block, rest
 
-row = re.compile(r"^\s*(\S+)\s+\[[^\]]+\]\s+(\S+)\s+→\s+(\S+):\s(.*)$")
-marks = [m.group(1) for m in map(row.match, rows) if m and (m.group(2), m.group(3), m.group(4)) == (sender, to, line)]
+row = re.compile(r"^\s*(\S+)\s+\[([^\]]+)\]\s+(\S+)\s+→\s+(\S+):\s(.*)$")
+# (marker, [timestamp, sender, recipient, text]); the marker is left out of the alignment, a read flips it.
+seen = [(m.group(1), list(m.group(2, 3, 4, 5))) for m in map(row.match, rows) if m]
 if mode == "check":
     load()
-    if len(rows) >= int(limit):
-        sys.exit(f"dispatch: the history read is capped at {limit} rows; raise BUS_READ_LIMIT")
-    print(len(marks))
+    with open(window, "w") as f:
+        json.dump([fields for _, fields in seen], f)
     sys.exit(0)
+with open(window) as f:
+    pre = json.load(f)
+post = [fields for _, fields in seen]
+n, m = len(pre), len(post)
+# Shift j: the post-send window without its j newest rows equals the pre-send one without its e = n + j - m oldest.
+fits = [m] if n == 0 else [j for j in range(m) if 0 <= n + j - m < n and post[: m - j] == pre[n + j - m :]]
+if len(fits) != 1:
+    sys.exit(
+        "dispatch: the post-send window does not align uniquely with the pre-send one; "
+        "the line may be on the bus unrecorded; raise BUS_READ_WINDOW or check the bus"
+    )
+if fits[0] == 0:
+    sys.exit(f"dispatch: this send added no bus row; {path} is unchanged")
+# Another seat's row may land after this send, so the send is the last new row equal to the line.
+marks = [mark for mark, (_, s, r, text) in seen[m - fits[0] :] if (s, r, text) == (sender, to, line)]
+if not marks:
+    sys.exit("dispatch: no new row equals the line; the line may be on the bus unrecorded; check the bus")
 # Thread 4255272797: the read-modify-write holds the record directory's lock, so a second dispatch waits.
 lock = os.open(record.parent, os.O_RDONLY)
 fcntl.flock(lock, fcntl.LOCK_EX)
 block, rest = load()
-# Thread 4254399807: an older identical row is not this send.
-if len(marks) <= int(before):
-    sys.exit(f"dispatch: this send added no bus row; {path} is unchanged")
 block["dispatch"].append(f"{line} read_at={'read' if marks[-1] == '○' else 'unread'}")
 body = json.dumps(block, sort_keys=True, indent=2, ensure_ascii=False)
 # Thread 4254844595: the line is already sent, so the record is replaced whole or not at all.
@@ -243,13 +318,16 @@ if [[ ! -f ${record} || ! -w ${record} || ! -w "$(dirname -- "${record}")" ]]; t
     echo "dispatch: the record ${record} cannot be written" >&2
     exit 1
 fi
-limit=${BUS_READ_LIMIT:-100000}
+limit=${BUS_READ_WINDOW:-200}
 [[ ${limit} =~ ^[1-9][0-9]*$ ]] || usage
 task="$(value_of task_id)"
+# A private window file (mode 0600, a fresh name), removed whatever the exit.
+window="$(mktemp "${TMPDIR:-/tmp}/dispatch-window.XXXXXX")"
+trap 'rm -f -- "${window}"' EXIT
 # Team-wide: history.sh renames the calling pane after an agent argument (thread 4254399805).
 bus() { "${AGMSG_SCRIPTS:-${HOME}/.agents/skills/agmsg/scripts}/history.sh" "${team}" "" "${limit}"; }
-before="$(bus | python3 -I -c "${recorder}" check "${record}" "${line}" "${from}" "${to}" 0 "${task}" "${limit}")"
+bus | python3 -I -c "${recorder}" check "${record}" "${line}" "${from}" "${to}" "${window}" "${task}"
 rc=0
 agmsg-dispatch "${team}" "${from}" "${to}" "${pane}" "${line}" || rc=$?
-bus | python3 -I -c "${recorder}" append "${record}" "${line}" "${from}" "${to}" "${before}" "${task}" "${limit}"
+bus | python3 -I -c "${recorder}" append "${record}" "${line}" "${from}" "${to}" "${window}" "${task}"
 exit "${rc}"
diff --git a/tests/unit/test_orchestrator_tools.py b/tests/unit/test_orchestrator_tools.py
index 9e535be6..607dbb76 100644
--- a/tests/unit/test_orchestrator_tools.py
+++ b/tests/unit/test_orchestrator_tools.py
@@ -4,6 +4,8 @@ Each script runs as a subprocess from its copy in a temporary git repository, wi
 `uv`, `gh`, `make`, `codex` and an interpreter `gate-python` stubbed on PATH and `history.sh` stubbed in the directory `AGMSG_SCRIPTS` names;
 git is the real one, against a bare repository standing in for `origin`. A stub records its argv NUL-separated,
 so an argument is compared byte for byte (`gh` and `make` append one line per call).
+The dispatch checker case alone replaces the `uv` stub with a logging wrapper around the real `uv` next on PATH, so
+the module needs a real uv with PyYAML in its cache or reachable index for that case.
 """
 
 import fcntl
@@ -257,7 +259,7 @@ class OrchestratorToolsTest(unittest.TestCase):
         self.assertEqual({"dispatch": [f"{ping} read_at=read"], "format": 1, "ledger": [], "task": "t"}, block)
         self.assertEqual("\nProse.\n", prose)
         # Thread 4254399805: team-wide, never with an agent, which would rename the calling pane.
-        self.assertEqual(["team", "", "100000"], self.call("history.sh"))
+        self.assertEqual(["team", "", "200"], self.call("history.sh"))
         # A record without a block gets one holding only dispatch; an unread message says so.
         plain = self.write(".orchestration/acceptance/u.md", "Prose only.\n")
         (self.calls / "dispatch-marker").write_text("●")
@@ -367,7 +369,7 @@ class OrchestratorToolsTest(unittest.TestCase):
                 self.assertIn(needle, self.dispatch(line, code=1).stderr)
                 self.assertIsNone(self.call("agmsg-dispatch"))
 
-    def test_dispatch_record_path_tokenizes_locks_and_refuses_a_capped_history(self):
+    def test_dispatch_record_path_tokenizes_and_locks(self):
         record = self.write(".orchestration/acceptance/t.md", '---\n{"task": "t"}\n---\n')
         (self.calls / "history").write_text("")
         (self.calls / "dispatch-marker").write_text("○")
@@ -409,15 +411,155 @@ class OrchestratorToolsTest(unittest.TestCase):
         self.assertEqual(
             sorted(f"{line} read_at=read" for line in lines), sorted(self.gate_block(record)[0]["dispatch"])
         )
-        # Thread 4255272803: a read whose lines reach the limit may have lost its oldest rows; nothing is sent.
-        (self.calls / "agmsg-dispatch").unlink()
-        (self.calls / "history").write_text("  ○ [2026-10-13T00:00:00Z] a → b: AGMSG-PING v1 task_id=x\n" * 3)
-        before = record.read_text()
-        result = self.run_tool("dispatch.sh", *args, "line0.txt", str(record), code=1, env={"BUS_READ_LIMIT": "3"})
-        self.assertIn("the history read is capped at 3 rows; raise BUS_READ_LIMIT", result.stderr)
-        self.assertIsNone(self.call("agmsg-dispatch"))
-        self.assertEqual(["team", "", "3"], self.call("history.sh"))
-        self.assertEqual(before, record.read_text())
+
+    def checker_dispatch(self):
+        """A stub checker beside the copied dispatch.sh and a fake uv that logs, then runs the real uv next on PATH."""
+        self.write(
+            "scripts/orchestrator/task-consistency-check.py",
+            "import re, sys\nf = sys.argv[-1]\ntid = re.search(r'^task_id: (\\S+)', open(f).read(), re.M)[1]\n"
+            "if f'.orchestration/{tid}/**' in open(f).read():\n    sys.exit(print(f'{f}: OK'))\n"
+            "print(f'{f}: FAIL')\nprint(f'  C2 allowed_files lacks .orchestration/{tid}/**')\nsys.exit(1)\n",
+        )
+        # The fake records its argv, its directory and the name of every variable it inherits; uv runs under env -i,
+        # so the calls directory is written into it.
+        (self.temp / "bin/uv").unlink()
+        fake = self.temp / "fake-uv/uv"
+        fake.parent.mkdir()
+        fake.write_text(
+            f'#!/usr/bin/env bash\necho "$*" >> "{self.calls}/uv.log"\npwd -P >> "{self.calls}/uv-cwd.log"\n'
+            f'/usr/bin/env | /usr/bin/sed -n "s/^\\([A-Za-z_][A-Za-z0-9_]*\\)=.*/\\1/p" >> "{self.calls}/uv-env.log"\n'
+            'here="$(cd "$(dirname "$0")" && pwd -P)"\n'
+            'p=":${PATH}:" && p=${p//:${here}:/:}\nexec "$(PATH=${p} command -v uv)" "$@"\n'
+        )
+        fake.chmod(0o755)
+        env = {"PATH": f"{fake.parent}{os.pathsep}{self.env['PATH']}"}
+        record = self.write(".orchestration/acceptance/t.md", '---\n{"task": "t"}\n---\n')
+        (self.calls / "history").write_text("")
+        (self.calls / "dispatch-marker").write_text("○")
+        rel = ".orchestration/tasks/t.md"
+
+        def send(front, code, cwd=None, extra=None):
+            text = self.write(rel, f"---\nformat: 2\ntask_id: t\n{front}---\n\nBody.\n").read_text()
+            line = self.write("line.txt", f"AGMSG-TASK v1 task_id=t task_file={rel} task_sha256={sha(text)}\n")
+            for name in ("uv.log", "uv-cwd.log", "uv-env.log"):
+                (self.calls / name).unlink(missing_ok=True)
+            args = ["team", "orch", "worker", "w5:pA", line, record]
+            result = self.run_tool("dispatch.sh", *args, code=code, env={**env, **(extra or {})}, cwd=cwd)
+            return result, (self.calls / "uv.log").read_text()
+
+        return rel, record, send
+
+    def test_dispatch_refuses_a_task_file_failing_the_checker(self):
+        # C-52: the checker beside the script is a stub that fails a file lacking its own evidence directory.
+        rel, record, send = self.checker_dispatch()
+        lacking = "allowed_files:\n  - scripts/x.sh\n"
+        # Both orders of the duplicate key: PyYAML alone would keep the last value, review in the second.
+        duplicates = ("kind: review\nkind: code\n", "kind: code\nkind: review\n")
+        for kind in ("kind: code\n", 'kind: "code"\n', "", *duplicates, "kind: review\n: broken\n"):
+            with self.subTest(kind=kind):
+                result, log = send(kind + lacking, 1)
+                self.assertIn(f"dispatch: {self.repo / rel} fails the task-consistency check", result.stderr)
+                self.assertIn("C2 allowed_files lacks .orchestration/t/**", result.stderr)
+                self.assertIn(f"task-consistency-check.py --root {self.repo} {self.repo / rel}", log)
+                self.assertIsNone(self.call("agmsg-dispatch"))
+                self.assertEqual('---\n{"task": "t"}\n---\n', record.read_text())
+        _, log = send("kind: review\n", 0)
+        # The Makefile's UV_PYYAML probe comes first, then the brief parse in the form it chose.
+        self.assertRegex(
+            log.splitlines()[0], r"^run --no-project --offline --python /\S+ --with pyyaml python -I -c import yaml$"
+        )
+        self.assertNotIn("task-consistency-check.py", log)
+        self.assertIn("python -I -c", log)
+        self.assertEqual(1, len(self.gate_block(record)[0]["dispatch"]))
+
+    def test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state(self):
+        # local:9df6b0c:1 (C-57), with the Bot's P1s 4292675906, 4299651928 and 4300102967: a caller's project, its
+        # .python-version, an inherited virtual environment, uv override or PYTHONPATH, all at once, choose nothing.
+        _, record, send = self.checker_dispatch()
+        pwn = self.write("pwn", f'#!/bin/sh\ntouch "{self.calls}/pwned"\nexit 1\n')
+        pwn.chmod(0o755)
+        caller = self.temp / "caller"
+        (caller / ".venv/bin").mkdir(parents=True)
+        (caller / ".venv/bin/python").symlink_to(pwn)
+        (caller / ".venv/pyvenv.cfg").write_text("home = /nonexistent\n")
+        (caller / "pyproject.toml").write_text(
+            '[project]\nname = "caller"\nversion = "0"\ndependencies = ["no-such-package-dispatch-a03"]\n'
+        )
+        (caller / ".python-version").write_text(f"{pwn}\n")
+        (caller / "pylib").mkdir()
+        (caller / "pylib/yaml.py").write_text(f"open({str(self.calls / 'pwned')!r}, 'w')\n")
+        state = {"VIRTUAL_ENV": str(caller / ".venv"), "CONDA_PREFIX": str(caller / ".venv"), "UV_PYTHON": str(pwn)}
+        state |= {"PYTHONPATH": str(caller / "pylib"), "AGMSG_STORAGE_PATH": str(self.temp / "store")}
+        _, log = send("kind: review\n", 0, cwd=caller, extra=state)
+        self.assertFalse((self.calls / "pwned").exists())
+        self.assertEqual({str(self.repo)}, set((self.calls / "uv-cwd.log").read_text().splitlines()))
+        # The allowlist (PATH, HOME, LANG, LC_ALL, AGMSG_*), plus what bash itself sets in the fake.
+        names = set((self.calls / "uv-env.log").read_text().split())
+        others = {n for n in names if not n.startswith("AGMSG_")}
+        self.assertLessEqual(others, {"PATH", "HOME", "LANG", "LC_ALL", "PWD", "SHLVL", "_", "OLDPWD"})
+        self.assertLessEqual({"PATH", "HOME", "AGMSG_STORAGE_PATH"}, names)
+        # Each call starts a "run" line; the brief script it passes with -c spans the lines after it.
+        calls = [line for line in log.splitlines() if line.startswith("run ")]
+        self.assertEqual(2, len(calls))  # the probe and the brief parse; a brief runs no checker
+        pinned = {re.search(r" --python (/\S+) ", call)[1] for call in calls}
+        self.assertEqual(1, len(pinned))
+        self.assertNotEqual(str(pwn), pinned.pop())
+        self.assertEqual(1, len(self.gate_block(record)[0]["dispatch"]))
+
+    def test_dispatch_reads_a_bounded_history_window(self):
+        # C-53: each read answers the window the case writes, window-1 before the send and window-2 after it.
+        (self.temp / "agmsg/history.sh").write_text(
+            '#!/usr/bin/env bash\necho "$*" >> "$CALLS/history.log"\n'
+            'n=$(($(cat "$CALLS/reads" 2> /dev/null || echo 0) + 1)) && echo "${n}" > "$CALLS/reads"\n'
+            'cat "$CALLS/window-${n}"\n'
+        )
+        ping = "AGMSG-PING v1 task_id=t reason=check"
+        self.write("line.txt", ping + "\n")
+        empty = '---\n{"task": "t"}\n---\n'
+        record = self.write(".orchestration/acceptance/t.md", empty)
+
+        def row(ts, text=ping, mark="●", sender="orch", to="worker"):
+            return f"  {mark} [2026-10-15T00:{ts}Z] {sender} → {to}: {text}"
+
+        def send(pre, post, code=0, window=None):
+            for n, rows in ((1, pre), (2, post)):
+                (self.calls / f"window-{n}").write_text("".join(r + "\n" for r in rows))
+            for name in ("reads", "history.log"):
+                (self.calls / name).unlink(missing_ok=True)
+            record.write_text(empty)
+            env = {"BUS_READ_WINDOW": window} if window else None
+            result = self.run_tool(
+                "dispatch.sh", "team", "orch", "worker", "w5:pA", "line.txt", record, code=code, env=env
+            )
+            self.assertEqual([], list(self.temp.glob("dispatch-window.*")))
+            return result
+
+        def recorded():
+            return self.gate_block(record)[0]["dispatch"]
+
+        # Eviction plus collision: the oldest row of a full window equals the line and leaves it.
+        full = [row("00:00")] + [row(f"{i // 60:02}:{i % 60:02}", f"x{i}") for i in range(1, 200)]
+        send(full, full[1:] + [row("59:00", mark="○")])
+        self.assertEqual([f"{ping} read_at=read"], recorded())
+        self.assertEqual(["team  200", "team  200"], (self.calls / "history.log").read_text().splitlines())
+        send(full[150:], full[151:] + [row("59:00", mark="○")], window="50")
+        self.assertEqual(["team  50", "team  50"], (self.calls / "history.log").read_text().splitlines())
+        # Same second: the newest pre-send row equals the line; the second such row is this send.
+        a, b = row("01:00", "a"), row("02:00", "b")
+        send([a, b, row("03:00")], [a, b, row("03:00"), row("03:00", mark="○")])
+        self.assertEqual([f"{ping} read_at=read"], recorded())
+        # Another seat's row lands after this send: the line's row is still the one recorded.
+        send([a, b], [a, b, row("03:00", mark="○"), row("03:01", "AGMSG-PONG v1 task_id=t", "●", "worker", "orch")])
+        self.assertEqual([f"{ping} read_at=read"], recorded())
+        refusals = (
+            ([a, b], [row("04:00", "c"), row("05:00", "d"), row("06:00")], "raise BUS_READ_WINDOW"),
+            ([a, b], [a, b], "this send added no bus row"),
+            ([row("07:00", "p")] * 200, [row("07:00", "p")] * 200, "does not align uniquely"),
+        )
+        for pre, post, message in refusals:
+            with self.subTest(message=message):
+                self.assertIn(message, send(pre, post, code=1).stderr)
+                self.assertEqual(empty, record.read_text())
 
     # three-repeat.sh
 

 succeeded in 240ms:
10:## Architecture
17:## Regime activation and progress
21:- A Claude session started in the repository root outside Herdr (a plain shell, mosh/ssh, or `claude -p`) is a pane-less orchestrator: nothing seats a worker automatically, and the SessionStart `herdr-agents --attach` hook prints a summary line naming that state, the on-demand commands, and any seated worker, followed in a regime repository by the `agmsg-orchestration:` directive line. Bring the regime up on demand: claim the seat outside the sandbox with the composite instance id, `actas-claim.sh <repo> claude-code <name> <session_id>.<claude pid>` (a claim from sandboxed Bash writes the bare session id and turn delivery then skips silently; see the seat-lock bullet below); seat the worker with `herdr-agents --add-worker <worktree>` (it derives `HERDR_SOCKET_PATH` from the default Herdr server socket `~/.config/herdr/herdr.sock`, the path the Claude sandbox allowlists, before creating anything, accepts a claude worker's workspace-trust dialog during spawn's readiness wait, and takes `--ready-timeout <seconds>`); confirm the worker's placement from its `run/spawn.*` placement record itself (the `herdr:<socket>:<pane>` row that upstream `agmsg_spawn_path` resolves) and the `linkage=` line `--add-worker` prints, never from `team.sh <team> --json`, which observes Codex members by reading their pane; treat the `linkage=` line `--add-worker` prints as the `AGMSG-PING` evidence, and on `pong=no` or `linkage=unreached` wake again with `agmsg-dispatch <team> <orchestrator> <worker> <pane> 'AGMSG-PING v1 task_id=<id> reason=<reason>'` and verify the PING's `read_at` (`poke.sh` only for a viewed workspace); and dispatch no AGMSG-TASK before its `AGMSG-PONG` arrives. Without a managed workspace the auditor runs headless, in the form the task-level audit bullet below names. A pane-less session uses turn delivery when the Monitor cannot run; see "Identity, delivery, and storage" for the platform limits.
29:## Parallel workers
33:- Delegate all repository-mutating work — file edits, builds, test runs, and git state changes — to seated workers, with at most one seated worker per git worktree and sequential assignments within one worktree. Add worktrees for parallelism; never use parallel `codex exec` or per-task Codex spawning, except that the read-only, non-interactive task-level audit the orchestrator runs during acceptance (the task-level audit bullet below) is not worker spawning and is permitted; it is identity-less. agmsg/herdr control-plane commands (`delivery.sh`, `watch.sh`, `actas-claim.sh`, `send.sh`, `join.sh`, and herdr agent/pane commands) are orchestrator-side exemptions.
43:  - Some steps stay sequential. The single audit tab serializes audits; the task-level audit of T67 reduces them to one per task. The orchestrator-side gate (`make require-crit-review`) and merges also run one at a time.
46:## Identity, delivery, and storage
59:## Live verification
64:## Review and integration invariants
71:- A task that touches a trust boundary (anything the design tier lists, CI that decides a required check, code that executes PR-controlled input) carries a `threat_table` in its front matter: one `{control, disposition}` row per thing the PR or the orchestrator controls (the tree and its tests, task.md, workflow files, interpreter and environment files, in-process effects, new or renamed scripts, metadata separators). The row unit is one row per `allowed_files` entry, one row per listed control that is not a path (task metadata, workflow and interpreter or environment inputs, in-process effects, new or renamed scripts, metadata separators), carried by the declared test module's row where that is where the control acts, and one row per orchestrator effect from the fixed list (forced removal, merge, update-branch); under a wildcard `allowed_files` entry whose files are executed or applied (scripts, workflows, hooks, settings, the rules seats follow), one row per concrete file the PR changes; a wildcard over test fixtures or other data files keeps one row; C4 and C7b of `scripts/orchestrator/task-consistency-check.py` verify the path half before dispatch, and the task-file review checks the rest. A disposition takes one of three forms: `closed: tests/<file>::<name>`, the test that closes the row; `residual: <sentence>`, the compensating control; `out-of-scope: <task id>`, the task that owns the row. The task-file review checks the three shape rules by hand: a `closed` selector names a test present in the PR tree at acceptance, an `out-of-scope` owner is a task id in the design's `implementing_tasks`, a `residual` payload is a sentence of at least 20 characters (the gate's minimum for a reason). For a `closed` row it checks the selector's form only, since the test does not exist before implementation. Substance is the reviewers': the task-file review, the Bot and the auditor judge each row against the diff. The table is the task's completion condition: a missing row is added once, counted as an amendment, never fixed finding by finding.
72:- Before every acceptance action (revise, accept, merge) the orchestrator runs `scripts/regime-counters.sh <task id>` and pastes its output into the acceptance record. S2 is decided from INV-6's counts: each component the script prints is read from its output, and for each component it prints as `unknown` the record pastes the command and output that read the source INV-6 names for that component, or, while that source has no entry for the task, says so and pastes the reading of the interim record the orchestrator used in its place. S1 (plan 006: the same finding class three times on one artifact, from any reviewer) is decided from the record's finding-class table, which gives a class to every finding the PR-feedback sweep lists, whatever its disposition, and to every task-level audit finding; three rows of one class stop the artifact. Read that table over non-advisory rows only: list advisory P2 rows with their classes (`advisory-p2` and the `local:<sha7>:<n>` rows `local-advisory.sh` writes), exclude them from S1's three-rows count, and name the excluded rows in the record. The gate's S6 check still sees every ledger row, so an advisory class at three rows gets its `searches` entry from `acceptance-front-matter.py` like any other. INV-6's message and head counts and the S2 lines (`revises`, `amendments`, `questions`, `bot_p1_heads`) take no ledger rows; `scripts/regime-counters.sh` prints them unchanged.
90:  - The orchestrator dispositions every `[P0-P3]` finding in the acceptance record, whatever the verdict, numbered 1..N in the audit's order of `[P0-P3]` lines (the audit's finding lines may be bulleted). For an `incorrect` verdict the dispositions are the record's JSON `audit_findings`, the only form the gate reads: one `{n, reason, evidence}` entry per finding, `n` the number as a string and `reason` at least 20 characters, written with `scripts/orchestrator/acceptance-front-matter.py --audit-dispositions <tsv>`; an entry never cites a fix, since a fix moves the head and needs its own audit. A finding under `Verdict: correct` is dispositioned all the same, as an `audit-finding: <n> …` line in the record's prose: `fixed:<sha>` with a fresh audit of that sha, otherwise `not-applicable:<reason of at least 20 characters>`. Deferral ("later", a follow-up task, a stopgap or a suppression) is not a disposition except under the advisory-P2 policy in Orchestrator Playbook step 10.
95:## Message Contract v1
144:## `.orchestration` Workspace Layout
157:## Orchestrator Playbook
168:10. For a RESULT that carries a pull request, integrate in this order. This is the single procedure that the PR integration rule, `AGENTS.md`, the README and the gh-first-workflow skill cite. A `gh pr update-branch` moves the head, so steps 1 to 4 run again on the new head. After an update-branch the orchestrator runs it, the order is CI on the new head, then the sweep, then the audit; an audit started before CI finishes sees incomplete evidence and returns an evidence-only `incorrect`. Select a checkout with git -C <absolute path>, never with cd, which the sandboxed Bash may not honour. After moving the review worktree to the audited head, verify git -C <review> rev-parse HEAD equals that head and git -C <main> symbolic-ref --short HEAD prints main before the audit and the gate.
170:       - A P2 finding of the Codex Bot, local review or task-level audit is advisory: disposition it `not-applicable:advisory P2 owned by <lineage>-followup-a0<n>` and record an `<id><TAB><class>` row under `## Owned by <owner>` in the lineage's acceptance record, with the orchestrator writing the owner task file before the row.
173:    2. Run the task-level audit of that head in the pair or headless form of the task-level audit bullet. It exits nonzero for every verdict other than `correct`. An exit with `Audit verdict: incorrect` is not a failed step: continue to step 3 and disposition its findings. A `blocked` or missing verdict means re-running the audit.
174:    3. Write the acceptance record, summarising the dispositions, with every audit finding dispositioned as the task-level audit bullet says: for an `incorrect` verdict the record's JSON `audit_findings`, which the gate reads through `ACCEPTANCE_EVIDENCE`.
187:## Worker Playbook
198:10. If blocked, still write the report and evidence paths that explain the blocker.
215:    - Apart from those surviving P0/P1 items, the RESULT names every unresolved thread id with `fixed:<sha>` or a proposed `not-applicable:<reason>` under Orchestrator Playbook step 10. The worker resolves no thread.
217:## Codex seat worklogs
251:## Pitfalls
A	.orchestration/dotfiles-T128-orchestrator-tools-followup-a03/autoskill.md
A	.orchestration/dotfiles-T128-orchestrator-tools-followup-a03/learning.md
A	.orchestration/dotfiles-T128-orchestrator-tools-followup-a03/report.md
A	.orchestration/dotfiles-T128-orchestrator-tools-followup-a03/revise.yaml
A	.orchestration/dotfiles-T128-orchestrator-tools-followup-a03/sandbox.md
A	.orchestration/dotfiles-T128-orchestrator-tools-followup-a03/task.md
A	.orchestration/dotfiles-T128-orchestrator-tools-followup-a03/validation.md
M	scripts/orchestrator/dispatch.sh
M	tests/unit/test_orchestrator_tools.py
{
  "lastAnalyzedAt": "2026-10-02T14:12:51Z",
  "gitCommitHash": "940a3a2b07adfd14140a0acff96784ef53a0a509",
  "version": "1.0.0",
  "analyzedFiles": 368
}

 exited 1 in 310ms:
error connecting to api.github.com
check your internet connection or https://githubstatus.com

**Managing output within token limits**
exec
/bin/zsh -lc "nl -ba .orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a03.md | sed -n '90,240p'; nl -ba .orchestration/reports/dotfiles-T128-orchestrator-tools-followup-a03.md" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 0ms:
    90	The Codex half's round 7 (on `141d0113`): P1 the fake uv ran python without PyYAML, so the parse that identifies a brief could not run in the tests; the fake uv now records its argv and delegates to the real uv found later on PATH, PyYAML present as in production, the checker staying the stub beside the copied script.
    91	
    92	## Change (round 9, 2026-10-15T22:30:15Z)
    93	
    94	The Codex half's round 8 (on `01ad84d6`): P1 the alignment allowed both compared slices to be empty, so a pre-send window that left the post-send window entirely could align falsely; a nonempty overlap is now required (`j < m`, `e < n`) unless the pre-send window itself was empty, so the left-the-window case cannot align.
    95	
    96	## Change (round 10, 2026-10-15T22:32:11Z)
    97	
    98	The Codex half's round 9 (on `2785ac02`): P2 the pre-send window file under `$TMPDIR` had no collision-safe creation, no cleanup and no control row; it is now a private `mktemp` file (mode 0600) removed by an EXIT trap on every exit path, with its own threat row and a cleanup assertion in the test.
    99	
   100	## Change (round 11, 2026-10-15T22:34:38Z)
   101	
   102	The Codex half's round 10 (on `3f5caedf`): P1 the smallest fitting shift is not fail-closed on a periodic bus (a window of identical rows fits shift 1 as well as no change); every shift from no change to `m − 1` is now tried and exactly one may fit: a unique no-change fit refuses as no new row, zero or several fits refuse as ambiguous, and the test adds the periodic-bus case.
   103	
   104	## Change (round 12, 2026-10-15T22:42:43Z)
   105	
   106	The review seat's round 2 (on `296f35d9`): P2-1 the acceptance rule took only the newest new row for the send, while another seat's line can land newer before the post-send read; this send is now the last new row equal to the line, refused only when none is, and the test adds the newer-row case; P3-1 the fake uv runs the `UV_PYYAML` probe form itself and the sentence names the module's real-uv dependency as new.
   107	
   108	## Goal
   109	
   110	After the merge, `dispatch.sh` sends no TASK line whose task file fails the checker, and both of its history reads take the last `BUS_READ_WINDOW` rows, so a send on a 1385-row team completes within the agmsg-dispatch timeout.
   111	
   112	## Files
   113	
   114	1. `scripts/orchestrator/dispatch.sh`: (a) after the hash checks and before any read or send, for an AGMSG-TASK line, parse the front matter of the file `task_file=` names (the text between the first two `---` lines) with PyYAML through the same uv form as the checker below, under a `SafeLoader` whose mapping constructor refuses a duplicate key; the file is a review brief, and is not checked, only when that parse succeeds, yields a mapping, and the mapping's `kind` value is the string `review`; otherwise (a parse error, a duplicate key, no closed front matter, no `kind`, or any other value, a quoted `"code"` included) run `scripts/orchestrator/task-consistency-check.py --root <root> <file>` beside this script, through the Makefile's `UV_PYYAML` form (`uv run --offline --with pyyaml` when `uv run --offline --with pyyaml python -c 'import yaml'` succeeds, else `uv run --with pyyaml`, which reaches the index), as `python -I <checker>`, and on a non-zero exit print `dispatch: <file> fails the task-consistency check` with the checker's output and exit 1, nothing sent, so only a positively identified brief is exempt and a duplicate, malformed or unparsable front matter is checked, never exempted; (b) the two history reads (`bus()`) take the newest `BUS_READ_WINDOW` rows (default 200; a positive integer, else usage) instead of `BUS_READ_LIMIT`, and the cap refusal (`the history read is capped at …`) is removed; because a count within a sliding window fails at its edge and a single anchor row fails under eviction and same-second collisions, the recorder aligns the two windows as two views of one bus: the `check` mode writes the whole pre-send window (each row's timestamp, sender, recipient and text, never its marker, which flips when a row is read between the reads) to a private file dispatch.sh creates with `mktemp "${TMPDIR:-/tmp}/dispatch-window.XXXXXX"` (mode 0600, a fresh name, never a predictable path) before the first read and removes with an EXIT trap whatever the exit, so the window is neither overwritten by another process, readable by another user, nor left behind; the `append` mode reads that file; `append` tries every shift `j` from `0` (no new row) to `m − 1` and keeps those for which the post-send window without its `j` newest rows (a nonempty slice) equals, row for row in those four fields, the pre-send window without its `e` oldest rows, where `e` is the number of pre-send rows the post-send window no longer shows (`e = n + j − m` for `n` pre-send and `m` post-send rows, `0 ≤ e < n`); the alignment must be unique: exactly one `j` may fit, and a periodic bus (a window of identical rows, which fits `j = 0` and `j = 1` alike) therefore never aligns; when the unique fit is `j ≥ 1`, those `j` rows are the new rows, every one provably after the pre-send read, and this send is the last of them whose sender, recipient and text equal the line (another seat's RESULT or PONG may land newer before the post-send read, since `agmsg-dispatch` returns only after the recipient's `read_at`; a second identical new row can only be this sender's own second dispatch, recorded the same way), whose marker is recorded; when the unique fit is `j = 0` the recorder exits 1 with `dispatch: this send added no bus row`; when zero or several shifts fit it exits 1 with `dispatch: the post-send window does not align uniquely with the pre-send one; the line may be on the bus unrecorded; raise BUS_READ_WINDOW or check the bus`, and when the fit is unique but none of the new rows equals the line it exits 1 with `dispatch: no new row equals the line; the line may be on the bus unrecorded; check the bus`; the one exception is an empty pre-send window (`n = 0`), where `j = m` and the rule on the new rows is the same; in every refusal the record is unchanged, so the recorder never records a wrong row and never silently drops a sent one; a nonempty pre-send window that left the post-send window entirely therefore never aligns and is refused; the shdoc header, the `@env` line for `BUS_READ_WINDOW` and the `@exitcode 1` line (which also names the checker's refusal of item 1a) say so, and `BUS_READ_LIMIT` disappears from the script.
   115	2. `tests/unit/test_orchestrator_tools.py`: two new tests beside the 52, in the module's dispatch style (the fake `agmsg-dispatch` and fake `history.sh` recording their arguments, a temporary repository with a task file and an acceptance record): `test_dispatch_refuses_a_task_file_failing_the_checker` (in the module's copy-and-stub style, `dispatch.sh` copied into a temporary `scripts/orchestrator/` beside a stub `task-consistency-check.py` that prints `<file>: FAIL` and `C2 allowed_files lacks .orchestration/<id>/**` and exits 1 for a file whose `allowed_files` lacks its own evidence directory, else `OK` and exit 0, and a fake `uv` first on PATH that appends its argv to the calls log and then runs the real `uv` (the next `uv` on PATH after its own directory) in the Makefile's `UV_PYYAML` probe form itself (`uv run --offline --with pyyaml` when `uv run --offline --with pyyaml python -c 'import yaml'` succeeds, else `uv run --with pyyaml`), so the front-matter parse of item 1a runs with PyYAML as in production and a sandboxed seat with a warm uv cache never reaches the index; this is a new dependency of the module, which today stubs `uv` and runs no real one, and the module's docstring says so; while the checker path dispatch.sh passes is the stub beside the copied script, and the log shows the checker path and the file: a task file whose `allowed_files` lacks its own evidence directory, kind code: exit 1, `fails the task-consistency check` and the checker's own line `C2 allowed_files lacks .orchestration/<id>/**` on stderr (the discriminating assertion: a checker dying on an import prints the first and not the second), the uv log holds `task-consistency-check.py` and the file, the fake agmsg-dispatch never called, the record unchanged; the same file with `kind: "code"` in quotes, with no `kind:` line, with `kind: review` followed by a second `kind: code` line (the duplicate key), and with a closed but unparsable front matter holding one literal `kind: review` line beside a line that is not YAML (`: broken`): refused likewise, each with the checker call logged; the same file with a single `kind: review` and no `allowed_files`: sent, the uv log holding no checker call) and `test_dispatch_reads_a_bounded_history_window` (the fake history.sh records a limit argument of 200 on both reads and answers the windows the case writes; with `BUS_READ_WINDOW=50` the argument is 50; the eviction-plus-collision case: a full pre-send window whose oldest row is identical to the line in sender, recipient and text and whose post-send window is the pre-send one shifted by that one row with the new row at the end, recorded once with the new row's marker; the same-second case: the newest pre-send row identical to the line down to the second, the post-send window ending with two such rows, recorded once with the second one's marker; the newer-row case: the post-send window ending with the line and then another seat's row, recorded once with the line's row's marker; the left-the-window case: a post-send window sharing no row with the pre-send one, exit 1 naming `BUS_READ_WINDOW`, the record unchanged; the no-new-row case: a post-send window equal to the pre-send one (distinct rows), exit 1 `added no bus row`, the record unchanged; and the periodic-bus case: a full window of rows identical in the four fields, unchanged after the send, exit 1 `does not align uniquely`, the record unchanged; after every case the temporary directory holds no `dispatch-window.*` file).
   116	
   117	## Out of scope
   118	
   119	`presend.sh` and `dispatch-direct.sh` (the orchestrator's glue): after this merge `dispatch-direct.sh` retires and `presend.sh` keeps running the premise replay and the mask check before a send (C-52's two other pre-send checks; only its checker step becomes redundant with item 1a), until a later task lands those two in the repository; upstream `history.sh` (D-history-upstream, the operator's); the other dispatch.sh checks (hash fields, the record block, the read marker form), which stay as they are.
   120	
   121	## Check
   122	
   123	`uv run python -m unittest tests/unit/test_orchestrator_tools.py -v` green (the 52 tests and the two new ones), pasted in the validation file with `shellcheck scripts/orchestrator/dispatch.sh` and `git diff --numstat origin/main...HEAD`: at most 200 changed lines (added plus deleted) outside `tests/` and outside `.orchestration/` (plan 021 step 7.2) and 1000 added lines under `tests/` (INV-2).
   124	
   125	## Completion
   126	
   127	One PR from a fresh branch off `origin/main` (after 8b25f9ca; the tools a02 PR #368 is merged). The PR is ready for the orchestrator's integration when the ruleset's required checks are green, the Bot's review of the final head is in (at PR open, and once more on `@codex review` after a P0/P1 fix round: plan 020 step 2), every Bot thread is replied to and resolved by the orchestrator with its disposition, the validation file carries the Check's outputs, and the RESULT names every P0/P1 thread with `fixed:<sha>` and every P2 thread with the disposition the worker proposes; the orchestrator's audit of the final head is dispositioned finding by finding before the gate, and a P0/P1 it leaves is the operator's decision. The Bot's P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P0 or P1 that survives the round is listed as `open:<thread id>` with `bot_rounds=2` (the Bot's review at PR open and its re-review after the fix round), stops the PR and goes to the operator as a decision; a P2 on this PR's own change whose fix stays within `allowed_files` and is small (one flag or a few lines plus one test) is fixed in a revise round the orchestrator sends with a `check=` while INV-6's counts allow it (C-50); any other P2 is advisory, owned by `dotfiles-T128-orchestrator-tools-followup-a04`, which the orchestrator writes when the first advisory P2 appears, before the PR's dispositions (C-51), and recorded under `## Owned by dotfiles-T128-orchestrator-tools-followup-a04` in this task's acceptance record. The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`. The RESULT names head, base, branch, files, every Bot thread with its disposition, the test names, the caps, `task_copy=<sha256 of .orchestration/dotfiles-T128-orchestrator-tools-followup-a03/task.md>` and the evidence paths.
   128	
   129	## Change (bot_rounds, 2026-10-16T06:21:47Z)
   130	
   131	The Completion clause's `bot_rounds=1` becomes the template's `bot_rounds=2` form (the Bot's review at PR open and its re-review after the fix round): T13's amendment 6 after the Bot's P2 4290644781 on PR #371, applied to every undispatched task text right before its dispatch and re-confirmed Codex first (C-54). Nothing else changes from the pair-confirmed hash `5a741e63`.
   132	
   133	## Change (threat row, 2026-10-16T22:07:03Z, after the RESULT)
   134	
   135	The Codex Bot's P1 4299651928 on PR #374's head 57d3577c: uv run from the caller's cwd executes a caller-controlled `.python-version` or venv interpreter even with `--no-project`, which the environment threat row's claim that the cwd chooses nothing did not cover. Operator decision D-P1-374 A: the fix round runs uv from the trusted script root; the row now says so. The dispatched hash `b291ba85` stands (the branch's task copy is byte-identical to it by design); this row is the orchestrator's record, carried by the next boundary.
   136	
     1	# Report: dotfiles-T128-orchestrator-tools-followup-a03
     2	
     3	- **Seat and branch.** `claude-standard-dot-a003` in `.claude/worktrees/worker-c`, on the fresh branch `tools/dispatch-checker-window`, cut with `--no-track` from `origin/main` at `1d418126`. The earlier branches are left as they are.
     4	- **Task copy.** Byte-identical to the dispatched main-checkout file, sha256 `b291ba85…`, the TASK's `task_sha256` (validation §1).
     5	- **Commits.** `766c1491`: the change, its tests and the task copy; `aeb4a0fb`: this evidence; `c8e813ea`: the Bot's P1 fix; then this evidence's fix-round update.
     6	- cost: n/a (the runtime exposes no token or cost figures to the seat).
     7	
     8	## Item 1a: the checker refusal (C-52)
     9	
    10	- For an AGMSG-TASK line, after the hash checks and before any read or send, `dispatch.sh` picks the Makefile's `UV_PYYAML` form: `uv run --offline --with pyyaml` when that form imports yaml, else `uv run --with pyyaml`.
    11	- **The brief exemption.** It parses the task file's front matter (the lines between the first two `---` lines) with PyYAML under a `SafeLoader` whose mapping constructor refuses a duplicate key. Only a mapping whose `kind` is the string `review` skips the checker. A parse error, a duplicate key, no closed front matter, no `kind` or any other value runs it.
    12	- **The checker.** `task-consistency-check.py --root <root> <file>` beside the script, as `python -I`. A non-zero exit prints `dispatch: <file> fails the task-consistency check` and the checker's output on stderr, exits 1 and sends nothing.
    13	
    14	## Item 1b: the bounded window (C-53)
    15	
    16	- Both reads are `history.sh <team> "" <BUS_READ_WINDOW>` (default 200, a positive integer, else usage). `BUS_READ_LIMIT` and the cap refusal are gone.
    17	- **The window file.** `mktemp "${TMPDIR:-/tmp}/dispatch-window.XXXXXX"` (mode 0600), removed by an EXIT trap. The `check` mode writes the pre-send window there: each row's timestamp, sender, recipient and text, never its marker.
    18	- **The alignment.** The `append` mode tries every shift `j` from 0 to `m − 1` and keeps those where the post-send window without its `j` newest rows equals the pre-send window without its `e = n + j − m` oldest (`0 ≤ e < n`). An empty pre-send window takes `j = m`.
    19	- **Outcomes.** Zero or several fits: `does not align uniquely … raise BUS_READ_WINDOW or check the bus`. A unique `j = 0`: `this send added no bus row`. Otherwise the send is the last of the `j` new rows equal to the line, sender and recipient, and none equal: `no new row equals the line`. Every refusal exits 1 with the record unchanged.
    20	- The shdoc header, the `@env BUS_READ_WINDOW` line and the `@exitcode 1` line say so.
    21	
    22	## Tests
    23	
    24	- `test_dispatch_refuses_a_task_file_failing_the_checker`: the stub checker beside the copied script, a fake `uv` that logs its argv and runs the real `uv` next on PATH. Refused, each with the checker call logged and the C2 line on stderr: `kind: code`, `kind: "code"`, no `kind`, the duplicate key in both orders, and a closed but unparsable front matter with one `kind: review` line. Sent with no checker call: a single `kind: review`. The log's first call is the `UV_PYYAML` probe.
    25	- `test_dispatch_reads_a_bounded_history_window`: the limit argument is 200 on both reads, 50 with `BUS_READ_WINDOW=50`. Recorded once with the right marker: eviction plus collision, same second, and another seat's newer row. Refused with the record unchanged: left the window, no new row, a periodic bus. No `dispatch-window.*` file is left after any case.
    26	- **The module.** 54 tests pass (validation §1). Eight mutants, all killed (validation §2 and §4).
    27	- **Two of the 52 changed.** The cap's removal forced it; the names and edits are in validation §3. The module docstring names its new dependency on a real uv for the checker case.
    28	
    29	## Notes
    30	
    31	- **The uv form.** The Makefile's `UV_PYYAML` form plus `--no-project`, the Bot's P1 (below): a caller's `pyproject.toml` is never discovered, synced or built.
    32	- **Size.** 105 changed lines outside `tests/` and `.orchestration/` (of 200), 114 added under `tests/` (of 1000), 2 files (validation §4).
    33	
    34	## The Bot
    35	
    36	- **Code review of `aeb4a0fb`** (review 5545290170): one P1, thread 4292675906, `dispatch.sh:181`, "Isolate uv from the caller's project". `fixed:c8e813ea`: `--no-project` on both uv forms, and the checker test's review brief sent from a directory with an unresolvable `pyproject.toml` (validation §4). The fix round is the PR's one round; the Bot's re-review is asked with `@codex review` on the fix head.
    37	- **Security review of `aeb4a0fb`:** completed, no finding.
    38	- **The PING** of 2026-10-16T21:38:05Z (the host slept overnight) was answered with a PONG, `status=alive`.
    39	
    40	## Final state (main-checkout copy only)
    41	
    42	- **CI.** All 13 checks pass on `57d3577c`, the final head (validation §5); `mergeStateStatus` is `BLOCKED`, waiting for review.
    43	- **The Bot's re-review of `57d3577c`** (review 5554058212, asked with `@codex review`): one new P1, thread 4299651928, `dispatch.sh:182`, "Run uv outside the caller-controlled directory". `open:4299651928`, `bot_rounds=2`: the one fix round is spent, so it stops the PR and goes to the operator. P1 4292675906 is `fixed:c8e813ea`.
    44	- **The memory add:**
    45	
    46	```text
    47	$ uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dotfiles-T128-orchestrator-tools-followup-a03 (PR #374, head 57d3577c): dispatch.sh refuses an AGMSG-TASK whose task file fails task-consistency-check.py (python -I via the UV_PYYAML uv form; only a front matter PyYAML parses, duplicate keys refused, to kind: review is exempt) and both history reads take the newest BUS_READ_WINDOW rows (default 200), the recorder aligning the post-send window with the pre-send one (kept in a mktemp 0600 file, EXIT trap) by the unique fitting shift and recording the last new row equal to the line. Bot: P1 4292675906 (uv discovered the callers pyproject.toml) fixed:c8e813ea with --no-project; the re-review of 57d3577c left P1 4299651928 open (uv still runs a caller .python-version or venv interpreter; fix: run uv from the trusted script root or pin the interpreter), bot_rounds=2, the operators decision. Two of the 52 tests changed with the cap removal (limit 200; the capped-history case dropped, test renamed).'
    48	f603f433-3d66-40c2-9925-a7cb82a4501b
    49	rc=0
    50	```
    51	
    52	## Revise round 2 (`8adf74bb`)
    53	
    54	- **The P1.** The Bot's re-review of `57d3577c`, thread 4299651928, `dispatch.sh:182`: `--no-project` keeps a caller's `pyproject.toml` out, but a `.python-version` or virtual environment in the caller's directory still chooses uv's interpreter. The operator's decision D-P1-374 A: one more fix round.
    55	- **The fix.** `fixed:8adf74bb`. Both uv forms run in a subshell that changes to the script's checkout root (`uvr`); the checker is named by the script directory's absolute path.
    56	- **The test.** `test_dispatch_refuses_a_task_file_failing_the_checker` plants a `.python-version` naming an executable in the caller's directory: it never runs, and the fake uv records the root as every call's directory. Mutant M9 (no `cd`) is killed; all nine mutants are killed, and 54 tests pass (validation §6).
    57	- **Size after the round.** 108 changed lines outside `tests/` and `.orchestration/` (of 200), 122 added under `tests/` (of 1000), 2 files.
    58	- **The Bot.** Its re-review is asked with `@codex review` on this round's head.
    59	
    60	## Round 2: CI and the Bot on `9df6b0c7`, the final head
    61	
    62	- **CI.** All 13 checks pass on `9df6b0c7` (validation §7); `mergeStateStatus` is `BLOCKED`, waiting for review.
    63	- **The Bot.** Its code re-review of `9df6b0c7` completed with no finding and a 👍 reaction. Both P1 threads are fixed: 4292675906 `fixed:c8e813ea`, 4299651928 `fixed:8adf74bb`.
    64	
    65	## Revise round 3 (`411c7d68`)
    66	
    67	- **The P1.** The local review of `9df6b0c7`, `local:9df6b0c:1` (`dispatch.sh:183-185`): an inherited `VIRTUAL_ENV` still chose uv's interpreter after the `cd`. The third finding of one class, the interpreter chosen from caller state. The operator's decision D-S2-374-2 A: one round that closes the class (C-57).
    68	- **The fix.** `fixed:411c7d68`. Both uv forms name `--python`, `python3` as `mise which` answers it under `env -i` at the root (else `python3` on PATH; a non-absolute answer refuses), and run under `env -u` for `VIRTUAL_ENV`, `VIRTUAL_ENV_PROMPT`, `CONDA_PREFIX` and every inherited `UV_*` variable. `--no-project` and the `cd` to the root stay.
    69	- **The test.** `test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state` sets a caller project, a caller `.python-version`, `VIRTUAL_ENV`, `CONDA_PREFIX` and `UV_PYTHON` at once; none is used (validation §8). The checker test's setup is now the shared helper `checker_dispatch`, and its probe assertion expects the pinned `--python`.
    70	- **Checks.** 55 tests pass; twelve mutants, all killed (validation §8).
    71	- **Size after the round.** 120 changed lines outside `tests/` and `.orchestration/` (of 200), 145 added under `tests/` (of 1000), 2 files.
    72	- **The Bot.** Its re-review is asked with `@codex review` on this round's head.
    73	
    74	## Round 3: CI and the Bot on `6ae8cf75`, the final head
    75	
    76	- **CI.** All 13 checks pass on `6ae8cf75` (validation §9).
    77	- **The Bot.** Its code re-review of `6ae8cf75` left one new P1, thread 4300102967 (`dispatch.sh:197`): the PyYAML probe runs without `-I`, so an inherited `PYTHONPATH` can load a caller's `yaml.py`. `open:4300102967`; the proposed fix is `-I` on the probe (one flag) or `PYTHONPATH` and the `PYTHON*` overrides added to the `env -u` list, with one test planting `yaml.py` on `PYTHONPATH`. `local:9df6b0c:1` is `fixed:411c7d68`; the Bot's earlier P1s stay `fixed:c8e813ea` and `fixed:8adf74bb`.
    78	
    79	## Revise round 4 (`b18698d5`)
    80	
    81	- **The P1.** The Bot's re-review of `6ae8cf75`, thread 4300102967, `dispatch.sh:197`: the `import yaml` probe ran without `-I`, so an inherited `PYTHONPATH` could load a caller's `yaml.py`. The fourth finding of the class; the operator's decision D-S2-374-3 A: one round that ends the class by an allowlist.
    82	- **The fix.** `fixed:b18698d5`. Both uv forms run under `env -i` with `PATH`, `HOME`, `LANG` and `LC_ALL` when set, and the `AGMSG_*` variables, nothing else; the probe runs `python -I`. The pinned `--python`, `--no-project` and the `cd` to the root stay.
    83	- **The test.** `test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state`, extended: every caller-state source at once, now with a `yaml.py` on `PYTHONPATH`; the fake uv inherits only the allowlisted names (validation §10).
    84	- **Checks.** 55 tests pass; thirteen mutants, all killed (validation §10).
    85	- **Size after the round.** 124 changed lines outside `tests/` and `.orchestration/` (of 200), 153 added under `tests/` (of 1000), 2 files.
    86	- **The Bot.** Its re-review is asked with `@codex review` on this round's head.
    87	
    88	## Round 4: CI and the Bot on `9cf65c02`, the final head
    89	
    90	- **CI.** All 13 checks pass on `9cf65c02` (validation §11); `mergeStateStatus` is `BEHIND`, since `main` moved.
    91	- **The Bot.** Its code re-review of `9cf65c02` completed with no finding and a 👍 reaction. Every P1 is fixed: 4292675906 `fixed:c8e813ea`, 4299651928 `fixed:8adf74bb`, `local:9df6b0c:1` `fixed:411c7d68`, 4300102967 `fixed:b18698d5`.

**Checking design invariants**
exec
/bin/zsh -lc 'git show ef74eaea9a94bff388b7c1027551a57797407b2f:scripts/orchestrator/dispatch.sh | nl -ba' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc 'nl -ba .orchestration/acceptance/dotfiles-T128-orchestrator-tools-followup-a03.md' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc "nl -ba .orchestration/tasks/dotfiles-T128-regime-v3-a01.md | sed -n '1,240p'; sed -n '175,225p' ~/.agents/skills/agmsg-orchestration/SKILL.md" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 74ms:
     1	---
     2	{
     3	  "format": 1,
     4	  "task": "dotfiles-T128-orchestrator-tools-followup-a03",
     5	  "head": "ef74eaea9a94bff388b7c1027551a57797407b2f",
     6	  "pr": 374,
     7	  "ledger": [
     8	    {
     9	      "id": "4292675906",
    10	      "class": "uv-caller-state-interpreter"
    11	    },
    12	    {
    13	      "id": "4299651928",
    14	      "class": "uv-caller-state-interpreter"
    15	    },
    16	    {
    17	      "id": "4300102967",
    18	      "class": "uv-caller-state-interpreter"
    19	    }
    20	  ],
    21	  "searches": [
    22	    {
    23	      "class": "uv-caller-state-interpreter",
    24	      "records": []
    25	    }
    26	  ],
    27	  "audit_findings": []
    28	}
    29	---
    30	
    31	# Acceptance record: dotfiles-T128-orchestrator-tools-followup-a03 (the owner task corrections C-52 (2) and C-53 (2) name)
    32	
    33	- 2026-10-15T13:06:18Z record created before the first dispatch; the Codex half of the task-text review runs first, the seat after its confirm (C-54); dispatch waits for the merged tools a02 task and its PR #368 (no wait).
    34	- 2026-10-15T14:41:09Z Codex half round 1 (on ffb4a6db) stalled: the three reviews started 13:07Z together, each transcript (`.agents/worklog/orchestrator-glue/codex-tools-a03-r1.log`) stopped growing at 13:07Z with no final message, and the processes were still alive at 14:24Z (77 minutes); stopped and re-run one at a time, T7 first.
    35	- 2026-10-15T21:59:03Z Codex half round 1 (`…-codex-r1.md`, on ffb4a6db, 76 s, run alone after the stalled run of 13:07Z): `revise`: P1 exempting files by a literal `kind: code` line is not fail-closed (`kind: "code"` would slip past); P2 `uv run --offline` contradicts the index fallback. Round 2: only a file whose front matter is positively a review brief (`kind: review`) is exempt, every other hashed task file is checked; the uv form is the Makefile's `UV_PYYAML` probe (offline when the cache holds PyYAML, else `uv run --with pyyaml`): task sha256 `bddbeaffb85e15ee092c91f44c54ba2d7ffb13df0df1459b12ac7603e5562286`, brief `e3887a695c9e8d2a9def4df8ad20454bfb6ebf570848107428ddae83bb3a93ed`, `presend.sh` OK; Codex round 2 next (C-54).
    36	- 2026-10-15T22:03:29Z Codex half round 2 (`…-codex-r2.md`, on bddbeaff, 80 s): `revise`: P1 the first `kind:` line could be a decoy before a second one; P2 the test lacked a duplicate-key case and an assertion that the checker ran. Round 3: the exemption needs exactly one `kind:` line in the front matter and its value `review`, anything else is checked; the test adds the duplicate case and asserts the checker call through the fake uv's log: task sha256 `7f2f42392809b909eea3f3110d7378e61ea1725c32105aa2a8824dc2843463d8`, brief `a328b9871e0591f16a451d228823c5528791abb67c639623d7c7deb0804a5b3b`, `presend.sh` OK; Codex round 3 next (C-54).
    37	- 2026-10-15T22:05:19Z Codex half round 3 (`…-codex-r3.md`, on 7f2f4239, 79 s): `confirm`, no finding. The seat's round 1 on this hash follows its chain-review-a03 round (one task at a time on the review seat; C-54).
    38	- 2026-10-15T22:17:15Z review seat round 1 (bus 22:15:52Z, on 7f2f4239): `revise`: P2-1 a count within a sliding window fails at the window's edge (an identical row leaving as the new one enters); P3-1 the failing-file case passed for the wrong reason (a checker dying on import yaml prints the same stderr) and the fake uv had no PyYAML; P3-2 presend.sh's premise replay and mask check had no holder after the retirement, and the exitcode line. Round 4: the pre-send read prints the newest row and the post-send read finds the new rows by position after it (refusing when it left the window); a stub checker beside the copied script prints the C2 line, asserted; presend.sh keeps the two other checks; the `@exitcode 1` line names the refusal: task sha256 `bf59ae9d7bbec317fa0507711ce83c986d320a7d6ec6d6f07fd8c4d6e6fe4ef6`, brief `29400b639e49b8c17513dc537d409e89b38a1bd2c6dcdb6f480b7f741df86d05`, `presend.sh` OK; `ACCEPTANCE round=1 status=accepted` sent; Codex round 4 first, the seat's round 2 after its confirm (C-54).
    39	- 2026-10-15T22:19:28Z Codex half round 4 (`…-codex-r4.md`, on bf59ae9d, 70 s): `revise`, P2 the anchor matched by its last occurrence would take a new identical row of the same second for the anchor. Round 5: the pre-send read also prints how many rows identical to the newest row the window holds (k), the post-send read takes the k-th occurrence from the oldest as the anchor, and the test adds the same-second collision case: task sha256 `829ec8e973a868e8021bf75b461a8865ed34426502f08dd82b9739ecf5213f85`, brief `3a6eec3638fc33a63cd488c587385b6535d62ab4f1ba16e9ee789224efe08870`, `presend.sh` OK; Codex round 5 next (C-54).
    40	- 2026-10-15T22:22:41Z Codex half round 5 (`…-codex-r5.md`, on 829ec8e9, 88 s): `revise`, P1 the k-th-occurrence anchor shifts when an older identical row leaves the window (eviction plus collision). Round 6 drops the single-row anchor: the pre-send read keeps its whole window, the post-send window is aligned with it as two views of one bus by the smallest shift j ≥ 1, the last of the j new rows must equal the sent line, and no alignment (more than the window arrived, or the bus does not align), no new row, or an unequal last row refuses with the record unchanged; the test holds the eviction-plus-collision, same-second, left-the-window and no-new-row cases: task sha256 `efd1ab960bdbe47f841e4b616654a115fd49896a111868c921ee66deefd98542`, brief `2ef4535ae8fa4fd77940b6b5991fbc367b962ddb1a6d6107c605e9fffde3cf96`, `presend.sh` OK; Codex round 6 next (C-54).
    41	- 2026-10-15T22:26:29Z Codex half round 6 (`…-codex-r6.md`, on efd1ab96, 69 s): `revise`, P1 a closed but invalid front matter with one literal `kind: review` line was exempt without a YAML parse. Round 7: the exemption needs a successful PyYAML parse under a duplicate-key-refusing loader yielding `review` for `kind`, through the same uv form; a parse failure, a duplicate key or another value runs the checker; the test adds the malformed case: task sha256 `141d0113657964a4f864b0e2428faf256615f778c365cc0dcb599969d394c987`, brief `6fcc481790ac41b2b840e882dbfafbcd2521e0f8d6751144b0454b392c43e396`, `presend.sh` OK; Codex round 7 next (C-54).
    42	- 2026-10-15T22:28:40Z Codex half round 7 (`…-codex-r7.md`, on 141d0113, 67 s): `revise`, P1 the fake uv ran python without PyYAML, so the YAML parse that identifies a brief could not run in the tests. Round 8: the fake uv records its argv and delegates to the real uv found later on PATH (PyYAML as in production, the Makefile's probe form), the checker staying the stub beside the copied script: task sha256 `01ad84d61ab5740621cb030f7ff5cc88e8f0375390fead9c6492b55f096c064b`, brief `dd0776da84221cbd9eb0774ee15af991f3a03ce8b94657fc3727ea28bc53cfc0`, `presend.sh` OK; Codex round 8 next (C-54).
    43	- 2026-10-15T22:30:15Z Codex half round 8 (`…-codex-r8.md`, on 01ad84d6, 48 s): `revise`, P1 the alignment allowed empty compared slices (j = m, e = n), so a pre-send window that left entirely could align falsely. Round 9: a nonempty overlap is required (j < m) unless the pre-send window was empty: task sha256 `2785ac025f16a09051a9bcd5524891478205c426623cccc620fb26d1678ebbe2`, brief `da31b3595b2e830e8b0139fbf480ffd92934247632a77ad827f513386d2775e7`, `presend.sh` OK; Codex round 9 next (C-54).
    44	- 2026-10-15T22:32:11Z Codex half round 9 (`…-codex-r9.md`, on 2785ac02, 64 s): `revise`, P2 the pre-send window file under `$TMPDIR` had no collision-safe creation, cleanup or control row. Round 10: a private `mktemp` file (mode 0600) removed by an EXIT trap whatever the exit, holding the four fields only, with its own threat row: task sha256 `3f5caedf626ec1644df113e7404a132af2c60693efe9f445d5f8c23edecec086`, brief `2a93b6ec58bbf33685a795fb2a10f0cc5b63e675bab9bd3522b5e2534f457650`, `presend.sh` OK; Codex round 10 next (C-54).
    45	- 2026-10-15T22:34:38Z Codex half round 10 (`…-codex-r10.md`, on 3f5caedf, 80 s): `revise`, P1 the smallest fitting shift is not fail-closed on a periodic bus (a full window of identical rows fits shift 1 as well as no change). Round 11: every shift from no change to m minus 1 is tried and exactly one may fit; a unique no-change fit refuses as no new row, zero or several fits refuse as ambiguous; the test adds the periodic-bus case: task sha256 `296f35d9c815a33d3873b9abca0ee4d70546383fb34ed8be3d5707708a99a089`, brief `8bec237cac18e2cc81512a9ac803ee01a53f551da946f4417f1d0fe4207f807f`, `presend.sh` OK; Codex round 11 next (C-54).
    46	- 2026-10-15T22:37:04Z Codex half round 11 (`…-codex-r11.md`, on 296f35d9, 112 s): `confirm`, no finding (eleven Codex rounds, each a distinct defect of the recorder's window logic or the exemption; M-20261015-06's class, Codex-first keeping the seat to two rounds). The seat's round 2 on the same hash dispatched through `dispatch-direct.sh` (C-54).
    47	- 2026-10-15T22:42:43Z review seat round 2 (bus 22:41:42Z, on 296f35d9): `revise`: P2-1 the acceptance rule took only the newest new row for the send, while another seat's line can land newest before the post-send read (agmsg-dispatch returns after the read); P3-1 the fake uv made the module's first real uv call and the sentence called the dependency existing. Round 12: among the new rows the last one equal to the line in sender, recipient and text is the send, refused only when none is; the fake uv runs the `UV_PYYAML` probe form itself (`--offline` when the cache holds PyYAML) and the sentence names the dependency as new: task sha256 `5a741e63e619ad31f83f10516be178f0ba63490bca2d4e16f9e45c14d4070b0a`, brief `5a189d71db69b6a482b01decec362514f370dec364977a9b662b34281cb0487e`, `presend.sh` OK; `ACCEPTANCE round=2 status=accepted` sent; Codex round 12 first, the seat's round 3 after its confirm (C-54).
    48	- 2026-10-15T22:44:43Z Codex half round 12 (`…-codex-r12.md`, on 5a741e63, 87 s): `confirm`, no finding. The seat's round 3 on the same hash dispatched through `dispatch-direct.sh` (C-54).
    49	- 2026-10-15T22:46:33Z review seat round 3 (bus 22:46:06Z, on 5a741e63): `confirm`; the Codex half confirmed the same hash (`…-codex-r12.md`). **Pair-confirmed: task sha256 `5a741e63e619ad31f83f10516be178f0ba63490bca2d4e16f9e45c14d4070b0a`** (Codex rounds 1 to 12, seat rounds 1 to 3; C-54 held throughout). `ACCEPTANCE round=3 status=accepted` sent. Dispatch after boundary (16), to a free Claude seat (the tools a02 PR is merged, `after:` is satisfied).
    50	- 2026-10-16T08:28:22Z review seat round 4 (bus 08:27:35Z, on b291ba85): `confirm`; with the Codex confirm (round 13) **tools-a03 is pair-confirmed again at `b291ba85f89d46877f74969d4e33ce994ff875f83454df58dbd8037a7d745da7`**; presend rc 0 (premises hold on 1d418126); the TASK line to `claude-standard-dot-a003` (worker-c, wA:p3) by dispatch-direct at 2026-10-16T08:28:22Z.
    51	
    52	## Ledger of the Bot reviews on PR #374 (rows id<TAB>class)
    53	
    54	4292675906	uv-caller-state-interpreter
    55	4299651928	uv-caller-state-interpreter
    56	4300102967	uv-caller-state-interpreter
    57	
    58	- 2026-10-16T21:57:29Z RESULT round 1 `status=done` (bus 21:56:07Z): PR #374 `tools/dispatch-checker-window`, head 57d3577c on base 1d418126 (766c1491 change and task copy, aeb4a0fb evidence, c8e813ea the Bot P1 fix, 57d3577c fix-round evidence); dispatch.sh refuses a task file failing the checker and reads a bounded history window; tests `test_dispatch_refuses_a_task_file_failing_the_checker` and `test_dispatch_reads_a_bounded_history_window`, two existing tests edited for the cap removal, 54 of 54, 8 of 8 mutants; caps 105 / 114; CI 13 pass; security review on aeb4a0fb clean; task_copy b291ba85. Bot: 4292675906 (P1, uv without --no-project discovering the caller's pyproject) `fixed:c8e813ea`; the re-review of 57d3577c left 4299651928 (P1): uv still executes a caller cwd's `.python-version` interpreter (`./pwn`) even with `run --no-project` (uv 0.7.22), and `--no-project` still uses a venv found in the current or parent directory; remedy: run uv from the trusted script root or pin the interpreter; the threat row claiming the caller cwd chooses nothing is contradicted. The one fix round is spent (`bot_rounds=2`), so the Completion clause sends the PR to the operator: D-P1-374 in plan 022 (default A), ACCEPTANCE `pending-integration` hold at 2026-10-16T21:57:29Z.
    59	- 2026-10-16T22:06:27Z operator decision D-P1-374 (AskUserQuestion, answer A, recorded in plan 022): one more fix round for 4299651928 (uv run from the trusted script root, one test; the task text's threat row corrected by the orchestrator); revise line to a003 at 2026-10-16T22:06:27Z; `4299651928` becomes `fixed:<sha>` with the RESULT.
    60	- 2026-10-16T22:27:40Z RESULT round 2 `status=done` (bus 22:25:43Z): head 9df6b0c7 (fix 8adf74bb: both uv forms run in a subshell cd'd to the script's checkout root; the checker named by the script directory's absolute path); `4299651928 fixed:8adf74bb`; the Bot's re-review of 9df6b0c7 without findings; 54 of 54 tests, 9 of 9 mutants, caps 108 / 122, CI 13 pass; `374-extra.tsv` holds both P1 rows as fixed. ACCEPTANCE `pending-integration` at 22:26:54Z; the owner task `dotfiles-T128-orchestrator-tools-followup-a04` written (C-51) and the chain (`374-chain1.log`, Bot wait 5 min) starts now; PR #372's chain resumes after a002's fix round.
    61	
    62	## Local review of 9df6b0c (the fix-round head): one P1 (rows id<TAB>class)
    63	
    64	local:9df6b0c:1	uv-caller-state-interpreter
    65	local-finding: 9df6b0c:1 fixed:411c7d68
    66	
    67	- 2026-10-16T22:38:10Z the chain on 9df6b0c7 (`374-chain1.log`): CI pass, no Bot review in the 5-minute wait, sandbox scan clean, sweep 13 items / 0 gaps; the local review (`…-local-review-9df6b0c.md`) found a P1: an inherited `VIRTUAL_ENV` pointing at a PR checkout's `.venv` still selects uv's interpreter after the cd, so its site-packages can run during the `import yaml` probe before validation. The third finding of one class (the interpreter chosen from caller state), so the three rows carry one slug, `uv-caller-state-interpreter`, and the S6 search ran (M-20261017-02, C-57: name the interpreter, strip the inherited environment):
    68	
    69	```
    70	search: uv-caller-state-interpreter -> M-20261017-02.md
    71	search-body: uv-caller-state-interpreter -> M-20261017-02.md
    72	compactiondb: uv-caller-state-interpreter -> 0 matches
    73	```
    74	
    75	- 2026-10-16T22:38:10Z a further fix round makes INV-6 read `revises 2` (S2): D-S2-374-2 (default A: one round that closes the class, pinning the interpreter and stripping VIRTUAL_ENV and the UV_* overrides, with one test setting every caller-state source at once); hold ACCEPTANCE at 2026-10-16T22:38:10Z.
    76	- 2026-10-16T22:42:38Z operator decision D-S2-374-2 (AskUserQuestion, answer A, recorded in plan 022): the class-closing fix round (pin the interpreter, strip the inherited environment, one test with every caller-state source set) sent to a003 at 2026-10-16T22:42:38Z; `local:9df6b0c:1` becomes `fixed:<sha>` with the RESULT.
    77	- 2026-10-16T23:14:12Z RESULT round 3 `status=done` (bus 23:13:19Z): head 6ae8cf75 (fix 411c7d68: both uv forms name `--python` (python3 from `mise which` under `env -i` at the root, else python3 on PATH; a non-absolute path refuses) and run under `env -u VIRTUAL_ENV, VIRTUAL_ENV_PROMPT, CONDA_PREFIX` and every inherited `UV_*`, keeping `--no-project` and the cd); test `test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state`; 12 of 12 mutants, 55 of 55 tests, caps 120 / 145, CI 13 pass; `local:9df6b0c:1 fixed:411c7d68`. The Bot's re-review of 6ae8cf75: P1 4300102967, the `import yaml` probe runs without `-I`, so an inherited PYTHONPATH loads a caller's yaml.py (the fourth finding of the class: the environment was stripped by a denylist, and PYTHON* was not on it). A further round makes INV-6 read `revises 3`: D-S2-374-3 (default A: end the class by allowlist, `env -i` with PATH, HOME and the agmsg variables for the probe and the checker, plus `-I` on the probe; one test planting yaml.py on PYTHONPATH and every earlier source at once); hold ACCEPTANCE at 2026-10-16T23:14:12Z.
    78	- 2026-10-16T23:16:22Z operator decision D-S2-374-3 (AskUserQuestion, answer A, recorded in plan 022): the allowlist round (env -i with an explicit allowlist for the probe and the checker, -I on the probe, one test planting every source at once) sent to a003 at 2026-10-16T23:16:22Z; `4300102967` becomes `fixed:<sha>` with the RESULT. C-57's method gains the allowlist form.
    79	- 2026-10-16T23:59:11Z RESULT round 4 `status=done` (bus 23:38:46Z): head 9cf65c02 (fix b18698d5: both uv forms run under `env -i` with PATH, HOME, LANG/LC_ALL when set and the AGMSG_* variables only; the probe runs `python -I`; the pinned `--python`, `--no-project` and the cd kept); `4300102967 fixed:b18698d5`; the Bot's re-review of 9cf65c02 without findings; the test extended to every caller-state source at once (the fake uv inherits only the allowlisted variables); 13 of 13 mutants, 55 of 55 tests, caps 124 / 153, CI 13 pass (BEHIND: main moved). ACCEPTANCE `pending-integration` at 2026-10-16T23:59:11Z; the chain runs after PR #376's.
    80	
    81	
    82	## Owned by dotfiles-T128-orchestrator-tools-followup-a04 (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)
    83	
    84	local:ef74eae:1	advisory-p2
    85	local-finding: ef74eae:1 not-applicable:advisory P2 owned by dotfiles-T128-orchestrator-tools-followup-a04 (- [P2] Allow concurrent rows to interleave in timestamp-ordered history — scripts/orchestrator/dispatch.sh:283-284); evidence=git show origin/main:.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a04.md | grep -n 'item 1'
    86	local:ef74eae:2	advisory-p2
    87	local-finding: ef74eae:2 not-applicable:advisory P2 owned by dotfiles-T128-orchestrator-tools-followup-a04 (- [P2] Exclude impossible evictions from underfull history windows — scripts/orchestrator/dispatch.sh:284-285); evidence=git show origin/main:.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a04.md | grep -n 'item 1'
    88	
    89	## Dispatch (bus lines)
    90	
    91	- AGMSG-TASK v1 task_id=dotfiles-T128-orchestrator-tools-followup-review-a03 round=1 repo=~/Workspace/dotfiles task_file=.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-review-a03.md task_sha256=a328b9871e0591f16a451d228823c5528791abb67c639623d7c7deb0804a5b3b tools_task_file=.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a03.md tools_task_sha256=7f2f42392809b909eea3f3110d7378e61ea1725c32105aa2a8824dc2843463d8 deadline=none note=one-round-review-of-the-owner-task-corrections-C-52-(2)-and-C-53-(2)-name(the-Codex-half-confirmed-first,C-54);answer-with-AGMSG-RESULT-verdict=confirm|revise-tools_task_sha256=<sha> read_at=read
    92	- AGMSG-TASK v1 task_id=dotfiles-T128-orchestrator-tools-followup-review-a03 round=2 repo=~/Workspace/dotfiles task_file=.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-review-a03.md task_sha256=8bec237cac18e2cc81512a9ac803ee01a53f551da946f4417f1d0fe4207f807f tools_task_file=.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a03.md tools_task_sha256=296f35d9c815a33d3873b9abca0ee4d70546383fb34ed8be3d5707708a99a089 deadline=none note=one-round-review-of-the-owner-task-corrections-C-52-(2)-and-C-53-(2)-name(the-Codex-half-confirmed-first,C-54;your-round-1-applied:the-window-read-anchored-on-the-newest-pre-send-row-not-a-count,the-checker-s-own-line-asserted-through-a-stub-checker-beside-the-copied-script,presend.sh-keeps-the-premise-replay-and-the-mask-check,the-exitcode-line;the-Codex-rounds-4-and-5:the-two-windows-are-aligned-as-views-of-one-bus-by-the-smallest-shift,the-last-new-row-must-equal-the-line,anything-else-refused,with-eviction-and-collision-cases;the-Codex-round-6-P1:the-exemption-needs-a-successful-duplicate-rejecting-YAML-parse-yielding-review,a-malformed-front-matter-is-checked;the-Codex-round-7-P1:the-fake-uv-delegates-to-the-real-uv-so-PyYAML-is-present-as-in-production;the-Codex-round-8-P1:a-nonempty-overlap-is-required-unless-the-pre-send-window-was-empty;the-Codex-round-9-P2:the-pre-send-window-file-is-a-private-mktemp-file-removed-by-a-trap,with-its-own-row;the-Codex-round-10-P1:the-alignment-must-be-unique-across-every-shift-including-no-change,else-refused,with-a-periodic-bus-case);answer-with-AGMSG-RESULT-verdict=confirm|revise-tools_task_sha256=<sha> read_at=read
    93	- AGMSG-TASK v1 task_id=dotfiles-T128-orchestrator-tools-followup-review-a03 round=3 repo=~/Workspace/dotfiles task_file=.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-review-a03.md task_sha256=5a189d71db69b6a482b01decec362514f370dec364977a9b662b34281cb0487e tools_task_file=.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a03.md tools_task_sha256=5a741e63e619ad31f83f10516be178f0ba63490bca2d4e16f9e45c14d4070b0a deadline=none note=one-round-review-of-the-owner-task-corrections-C-52-(2)-and-C-53-(2)-name(the-Codex-half-confirmed-first,C-54;your-round-1-applied:the-window-read-anchored-on-the-newest-pre-send-row-not-a-count,the-checker-s-own-line-asserted-through-a-stub-checker-beside-the-copied-script,presend.sh-keeps-the-premise-replay-and-the-mask-check,the-exitcode-line;the-Codex-rounds-4-and-5:the-two-windows-are-aligned-as-views-of-one-bus-by-the-smallest-shift,the-last-new-row-must-equal-the-line,anything-else-refused,with-eviction-and-collision-cases;the-Codex-round-6-P1:the-exemption-needs-a-successful-duplicate-rejecting-YAML-parse-yielding-review,a-malformed-front-matter-is-checked;the-Codex-round-7-P1:the-fake-uv-delegates-to-the-real-uv-so-PyYAML-is-present-as-in-production;the-Codex-round-8-P1:a-nonempty-overlap-is-required-unless-the-pre-send-window-was-empty;the-Codex-round-9-P2:the-pre-send-window-file-is-a-private-mktemp-file-removed-by-a-trap,with-its-own-row;the-Codex-round-10-P1:the-alignment-must-be-unique-across-every-shift-including-no-change,else-refused,with-a-periodic-bus-case;your-round-2:among-the-new-rows-the-last-one-equal-to-the-line-is-the-send,the-fake-uv-runs-the-probe-form-itself,the-module-s-uv-dependency-named-as-new);answer-with-AGMSG-RESULT-verdict=confirm|revise-tools_task_sha256=<sha> read_at=read
    94	- AGMSG-TASK v1 task_id=dotfiles-T128-orchestrator-tools-followup-review-a03 round=4 repo=~/Workspace/dotfiles task_file=.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-review-a03.md task_sha256=5a189d71db69b6a482b01decec362514f370dec364977a9b662b34281cb0487e tools_task_file=.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a03.md tools_task_sha256=b291ba85f89d46877f74969d4e33ce994ff875f83454df58dbd8037a7d745da7 deadline=none note=round-4-a-re-confirm-after-one-change-since-the-pair-confirmed-5a741e63:the-Change(bot_rounds)section-names-it,the-Completion-clause-s-bot_rounds=1-becoming-the-template-s-bot_rounds=2-form(the-Bot-s-review-at-PR-open-and-its-re-review-after-the-fix-round;T13-amendment-6);judge-that-nothing-else-changed-and-the-clause-reads-consistently;the-Codex-half-confirmed(round-13);answer-with-AGMSG-RESULT-verdict=confirm|revise-tools_task_sha256=<sha> read_at=read
    95	- AGMSG-TASK v1 task_id=dotfiles-T128-orchestrator-tools-followup-a03 round=1 repo=~/Workspace/dotfiles/.claude/worktrees/worker-c task_file=.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a03.md task_sha256=b291ba85f89d46877f74969d4e33ce994ff875f83454df58dbd8037a7d745da7 deadline=none note=plan-022-tools-a03(dispatch.sh:the-checker-refusal-and-the-bounded-aligned-window-reads,C-52/C-53-tool-halves);pair-confirmed-at-this-hash(Codex-round-13,seat-round-4);read-the-task-file-first,fresh-branch-from-origin/main(1d418126-or-later),one-PR,the-Bot-reviews-once-at-PR-open,RESULT-per-Worker-Playbook-step-15 read_at=read
    96	- AGMSG-ACCEPTANCE v1 task_id=dotfiles-T128-orchestrator-tools-followup-a03 round=1 status=pending-integration reason=RESULT-read:head-57d3577c,CI-13-pass,4292675906-fixed:c8e813ea,the-Bot-s-re-review-P1-4299651928(uv-runs-a-caller-cwd-interpreter)survives-the-one-fix-round,so-the-Completion-clause-sends-it-to-the-operator(D-P1-374,default-A:one-more-fix-round,uv-run-from-the-trusted-script-root);hold-until-the-decision;nothing-to-do-on-your-side previous_head=57d3577ca780248f573fd26c4fa460e2b5e2d510 next_action=none-until-the-decision read_at=read
    97	- AGMSG-ACCEPTANCE v1 task_id=dotfiles-T128-orchestrator-tools-followup-a03 round=1 status=revise reason=operator-decision-D-P1-374-A(AskUserQuestion,plan-022):one-more-fix-round-for-the-Bot-s-P1-4299651928-on-57d3577c:run-both-uv-commands-from-the-trusted-script-root(uv---directory-<root>-or-a-cd-subshell-to-git-rev-parse---show-toplevel-of-the-script)so-a-caller-cwd-s-.python-version-or-venv-chooses-nothing,one-test(the-uv-shim-records-the-directory-it-ran-in-or-a-caller-cwd-.python-version-./pwn-is-not-executed);the-task-text-s-threat-row-is-corrected-by-the-orchestrator(Change-note);commit,push,@codex-review,RESULT-naming-4299651928-fixed:<sha> check=tests/unit/test_orchestrator_tools.py(the-new-test,named-in-the-RESULT) previous_head=57d3577ca780248f573fd26c4fa460e2b5e2d510 next_action=fix-round,commit,push,@codex-review,RESULT read_at=read
    98	- AGMSG-ACCEPTANCE v1 task_id=dotfiles-T128-orchestrator-tools-followup-a03 round=2 status=pending-integration reason=RESULT-round-2-read:head-9df6b0c7,both-Bot-P1-fixed(4292675906:c8e813ea,4299651928:8adf74bb:uv-in-a-subshell-cd-to-the-script-s-checkout-root);the-chain-runs-on-this-head(CI,Bot-wait,sandbox-scan,local-review,sweep,receipt,audit);the-orchestrator-replies-to-and-resolves-the-threads;nothing-to-do-on-your-side previous_head=9df6b0c7594cef7f42e9a43faa3e08d0f035e329 next_action=none-until-the-integration-result read_at=read
    99	- AGMSG-ACCEPTANCE v1 task_id=dotfiles-T128-orchestrator-tools-followup-a03 round=2 status=pending-integration reason=the-local-review-of-9df6b0c7-found-a-P1(dispatch.sh-183-185:an-inherited-VIRTUAL_ENV-still-selects-uv-s-interpreter-after-the-cd,so-a-PR-checkout-s-.venv-can-run-during-the-import-yaml-probe);the-third-finding-of-one-class(the-interpreter-chosen-from-caller-state:pyproject,.python-version,VIRTUAL_ENV);the-chain-stopped-before-the-audit;a-further-fix-round-makes-INV-6-read-revises-2,so-it-waits-for-the-operator-s-decision-D-S2-374-2(default-A:one-round-that-closes-the-class:pin-the-interpreter-and-strip-the-inherited-env);hold previous_head=9df6b0c7594cef7f42e9a43faa3e08d0f035e329 next_action=none-until-the-decision read_at=unread
   100	- AGMSG-ACCEPTANCE v1 task_id=dotfiles-T128-orchestrator-tools-followup-a03 round=2 status=revise reason=operator-decision-D-S2-374-2-A(AskUserQuestion,plan-022:S2-waived):one-round-that-closes-the-class(C-57,identity-over-shape):both-uv-invocations-name-the-interpreter(--python-<the-trusted-interpreter-resolved-at-the-script-s-checkout-root,e.g.-the-python3-mise-provides-there>)and-run-under-an-environment-without-VIRTUAL_ENV,VIRTUAL_ENV_PROMPT,UV_PROJECT_ENVIRONMENT,UV_PYTHON-and-the-other-UV_*-overrides(env--u-…-or-an-explicit-allowlisted-env),keeping---no-project-and-the-cd-to-the-root;one-test-that-sets-a-caller-pyproject,a-caller-cwd-.python-version-and-VIRTUAL_ENV-at-once-and-asserts-none-is-used(the-fake-uv-records-its-env-and-args);nothing-else;commit,push,@codex-review,RESULT-naming-local:9df6b0c:1-fixed:<sha>-and-the-test check=tests/unit/test_orchestrator_tools.py(the-new-test,named-in-the-RESULT) previous_head=9df6b0c7594cef7f42e9a43faa3e08d0f035e329 next_action=fix-round,commit,push,@codex-review,RESULT read_at=unread
   101	- AGMSG-ACCEPTANCE v1 task_id=dotfiles-T128-orchestrator-tools-followup-a03 round=3 status=pending-integration reason=RESULT-round-3-read:head-6ae8cf75,local:9df6b0c:1-fixed:411c7d68(pinned---python,env--u-VIRTUAL_ENV/CONDA_PREFIX/UV_*),12-mutants,CI-13-pass;the-Bot-s-re-review-P1-4300102967(the-import-yaml-probe-without--I,an-inherited-PYTHONPATH-loads-a-caller-s-yaml.py)is-the-fourth-finding-of-the-class;a-further-round-makes-INV-6-read-revises-3,so-it-waits-for-the-operator-s-decision-D-S2-374-3(default-A:one-round-that-ends-the-class-by-allowlist:env--i-with-an-explicit-PATH/HOME/agmsg-variable-allowlist-for-the-probe-and-the-checker,plus--I-on-the-probe);hold previous_head=6ae8cf75df74bb54eb3b724ea7c94e16b70759ef next_action=none-until-the-decision read_at=read
   102	- AGMSG-ACCEPTANCE v1 task_id=dotfiles-T128-orchestrator-tools-followup-a03 round=3 status=revise reason=operator-decision-D-S2-374-3-A(AskUserQuestion,plan-022:S2-waived):one-round-that-ends-the-class-by-allowlist,not-denylist:run-the-import-yaml-probe-and-the-checker-under-env--i-with-an-explicit-allowlist(PATH-as-the-script-computes-it,HOME,LANG/LC_ALL-if-needed,the-AGMSG_*-variables-the-scripts-read,and-nothing-else),the-probe-with-python-s--I,keeping-the-pinned---python,--no-project-and-the-cd-to-the-root;one-test-that-plants-every-caller-state-source-at-once(a-caller-pyproject,a-cwd-.python-version,VIRTUAL_ENV,CONDA_PREFIX,UV_PYTHON-and-a-yaml.py-on-PYTHONPATH)and-asserts-the-fake-uv-and-the-probe-see-only-the-allowlisted-variables;nothing-else;commit,push,@codex-review,RESULT-naming-4300102967-fixed:<sha>-and-the-test check=tests/unit/test_orchestrator_tools.py(the-new-or-extended-test,named-in-the-RESULT) previous_head=6ae8cf75df74bb54eb3b724ea7c94e16b70759ef next_action=fix-round,commit,push,@codex-review,RESULT read_at=read
   103	- AGMSG-ACCEPTANCE v1 task_id=dotfiles-T128-orchestrator-tools-followup-a03 round=4 status=pending-integration reason=RESULT-round-4-read:head-9cf65c02,4300102967-fixed:b18698d5(the-allowlist-form:env--i-with-PATH,HOME,LANG/LC_ALL,AGMSG_*;python--I-on-the-probe),13-mutants,CI-13-pass,the-Bot-s-re-review-clean;the-chain-runs-after-PR-376-s(one-chain-at-a-time;main-moved,so-update-branch-first);nothing-to-do-on-your-side;you-are-free previous_head=9cf65c0299645e30e54419668ba523eff9c4897e next_action=none-for-this-task read_at=read

 succeeded in 130ms:
     1	#!/usr/bin/env bash
     2	# @file dispatch.sh
     3	# @brief Send one AGMSG-TASK, AGMSG-ACCEPTANCE or AGMSG-PING line after checking its sha256 fields, and record it.
     4	# @description
     5	#   Plan 007 T718 (C-20). Reads exactly one physical line from a file (a second
     6	#   line, blank or not, or a NUL byte is refused). Every `<name>_sha256=<64
     7	#   hex>` token is recomputed from the file its sibling token names,
     8	#   `<name>_file=` or else `<name>=` (`task_sha256` from `task_file=`,
     9	#   `design_sha256` from `design=`, `amended_task_sha256` from `amended_task=`;
    10	#   a line naming the file both ways, or repeating one of these keys, is
    11	#   refused), except a `previous_<name>_sha256=` reference to an earlier
    12	#   version, which is checked as 64 lowercase hex only; every line must carry
    13	#   exactly one non-empty `task_id=`, and an AGMSG-TASK line must carry
    14	#   `task_file=` and `task_sha256=`. Tokens are separated by any run of spaces
    15	#   and tabs, and every token after `v1` is `<key>=<value>` (exit 2 otherwise,
    16	#   so a repeated prefix or a value split by a space is refused); the
    17	#   recorder takes `task_id` from that one parse (thread 4255272793). A relative path is read from the root of
    18	#   the checkout this script lives in (`git rev-parse --show-toplevel` there),
    19	#   never from the caller's directory. A missing field or file, a malformed value
    20	#   or a mismatch exits 1 naming the field, and nothing is sent. Otherwise the
    21	#   line goes to `agmsg-dispatch` as one argument, byte for byte.
    22	#   With an acceptance record, the record is checked before the send and, once
    23	#   the line is on the bus, `<the line> read_at=<read|unread>` is appended to
    24	#   the `dispatch` list of
    25	#   the record's JSON block, the object between its first two `---` lines. The
    26	#   block is read and written with Python's standard json (malformed JSON, a
    27	#   duplicate key, NaN or Infinity, a block that is not an object or a
    28	#   `dispatch` that is not a list is refused; `sort_keys`, `indent=2`); the key
    29	#   is created when absent, and a record without a block gets a block holding
    30	#   only `dispatch`. The prose after the block is kept byte for byte, CRLF
    31	#   included (thread 4256987087), and the record is replaced atomically (a
    32	#   temporary file in its directory, fsync, rename) under an exclusive `flock`
    33	#   of that directory, so two dispatches to one record never lose an entry
    34	#   (thread 4255272797). A record that is not an existing regular file writable in a
    35	#   writable directory, or whose `task` is not the line's `task_id`, is refused
    36	#   before the send, and nothing is sent.
    37	#   An AGMSG-TASK line whose `task_file=` fails `task-consistency-check.py`
    38	#   (beside this script, run as `python -I` through the Makefile's `UV_PYYAML`
    39	#   uv form with `--no-project` and a pinned `--python`, from the root, under `env -i` with only `PATH`, `HOME`,
    40	#   `LANG`, `LC_ALL` and the `AGMSG_*` variables) is refused with the checker's output, and nothing is sent (C-52).
    41	#   Only a review brief is exempt: a front matter (the text between the first
    42	#   two `---` lines) that PyYAML parses, refusing a duplicate key, to a mapping
    43	#   whose `kind` is the string `review`; every other outcome runs the checker.
    44	#   Only a bus row this send created is recorded. Both reads of the team-wide
    45	#   `history.sh <team> "" <BUS_READ_WINDOW>` take the newest rows (C-53: a
    46	#   whole-bus read took 56 minutes on a 1385-row team), and the recorder aligns
    47	#   them as two views of one bus: the pre-send window (each row's timestamp,
    48	#   sender, recipient and text) goes to a private `mktemp` file removed on exit;
    49	#   after the send every shift j from 0 to m-1 of the m post-send rows is tried,
    50	#   and exactly one may leave the post-send window, without its j newest rows,
    51	#   equal to the pre-send window without the rows that left it (all m new rows
    52	#   when the pre-send window was empty). This send is the last of those j new
    53	#   rows equal to the line, sender and recipient. No fit, several fits (a
    54	#   periodic bus), j = 0 or no equal new row leaves the record unchanged and
    55	#   exits 1. The read state is the marker history.sh prints for that row
    56	#   (`●` unread, `○` read): agmsg's scripts expose no read_at time, this script
    57	#   never reads the message database, and it never passes an agent to
    58	#   history.sh, whose agent argument renames the caller's pane after it.
    59	# @arg $1 string agmsg team.
    60	# @arg $2 string Sender identity.
    61	# @arg $3 string Recipient identity.
    62	# @arg $4 string Recipient pane id (for example `w5:pA`).
    63	# @arg $5 path File holding the line.
    64	# @arg $6 path Optional acceptance record (`.orchestration/acceptance/<task>.md`), relative to the current directory.
    65	# @env AGMSG_SCRIPTS The agmsg scripts directory (default `$HOME/.agents/skills/agmsg/scripts`).
    66	# @env BUS_READ_WINDOW The newest rows each history read takes (default 200, a positive integer).
    67	# @exitcode 0 Sent, and recorded when a record was given (agmsg-dispatch's own status otherwise).
    68	# @exitcode 1 A field check failed, the task file fails the task-consistency check, the record is malformed, or the sent line was not recorded.
    69	# @exitcode 2 Usage error, or the file is not one AGMSG-TASK, AGMSG-ACCEPTANCE or AGMSG-PING v1 line.
    70	# @example
    71	#   scripts/orchestrator/dispatch.sh dotfiles-conformance claude-deep-dot claude-standard-dot-a003 w5:pA \
    72	#     "$TMPDIR/task-line.txt" .orchestration/acceptance/dotfiles-T128-orchestrator-tools-a01.md
    73	set -euo pipefail
    74	
    75	usage() {
    76	    echo "usage: dispatch.sh <team> <from> <to> <pane> <line-file> [<acceptance-record>]" >&2
    77	    exit 2
    78	}
    79	(($# == 5 || $# == 6)) || usage
    80	team=$1 from=$2 to=$3 pane=$4 file=$5 record=${6:-}
    81	[[ -f ${file} ]] || usage
    82	# Thread 4256541716: command substitution drops a NUL byte, so the line sent would not be the file's.
    83	if (($(tr -d '\0' < "${file}" | wc -c) != $(wc -c < "${file}"))); then
    84	    echo "dispatch: ${file} holds a NUL byte" >&2
    85	    exit 2
    86	fi
    87	# The sentinel keeps every trailing newline, which $( ) alone would drop (thread 4254107304).
    88	line="$(cat -- "${file}" && printf x)" && line=${line%x} && line=${line%$'\n'}
    89	[[ ${line} != *$'\n'* ]] || {
    90	    echo "dispatch: ${file} holds more than one line" >&2
    91	    exit 2
    92	}
    93	[[ ${line} =~ ^AGMSG-(TASK|ACCEPTANCE|PING)[[:blank:]]+v1[[:blank:]] ]] || {
    94	    echo "dispatch: not an AGMSG-TASK, AGMSG-ACCEPTANCE or AGMSG-PING v1 line" >&2
    95	    exit 2
    96	}
    97	root="$(git -C "$(dirname -- "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
    98	
    99	read -ra tokens <<< "${line}"
   100	for t in "${tokens[@]:2}"; do
   101	    [[ ${t} == *=* ]] || {
   102	        echo "dispatch: ${t} is not a <key>=<value> token" >&2
   103	        exit 2
   104	    }
   105	done
   106	# @description Print the value of the first `<key>=` token, or fail.
   107	# @arg $1 string Key.
   108	value_of() {
   109	    local t
   110	    for t in "${tokens[@]}"; do
   111	        [[ ${t} == "$1="* ]] && printf '%s' "${t#*=}" && return 0
   112	    done
   113	    return 1
   114	}
   115	# @description Print how many tokens carry `<key>=`.
   116	# @arg $1 string Key.
   117	count_of() {
   118	    local t n=0
   119	    for t in "${tokens[@]}"; do
   120	        [[ ${t} == "$1="* ]] && n=$((n + 1))
   121	    done
   122	    printf '%s' "${n}"
   123	}
   124	# Thread 4254893065: every message names exactly one task, before any hash or record work.
   125	if (($(count_of task_id) != 1)) || [[ -z "$(value_of task_id)" ]]; then
   126	    echo "dispatch: the line needs exactly one non-empty task_id=" >&2
   127	    exit 1
   128	fi
   129	# Thread 4254163604: a TASK whose file is not hash-bound is never sent. The kind is the parsed
   130	# first token, so a tab after it does not skip this check (thread 4260535901).
   131	if [[ ${tokens[0]} == AGMSG-TASK ]]; then
   132	    for field in task_file task_sha256; do
   133	        value_of "${field}" > /dev/null || {
   134	            echo "dispatch: an AGMSG-TASK line needs ${field}=" >&2
   135	            exit 1
   136	        }
   137	    done
   138	fi
   139	for t in "${tokens[@]}"; do
   140	    # Thread 4254771302: any name before _sha256=, digits included (a02_expected_sha256=).
   141	    [[ ${t} =~ ^([^=]+)_sha256=(.*)$ ]] || continue
   142	    name=${BASH_REMATCH[1]} want=${BASH_REMATCH[2]}
   143	    field="${name}_sha256"
   144	    [[ ${want} =~ ^[0-9a-f]{64}$ ]] || {
   145	        echo "dispatch: ${field} is not 64 lowercase hex digits" >&2
   146	        exit 1
   147	    }
   148	    # Thread 4256541725: a previous_<name>_sha256= reference names no file here (a02 item 4's grammar row).
   149	    if [[ ${name} == previous_* ]]; then
   150	        continue
   151	    fi
   152	    # Thread 4254494989: a repeated key leaves a second, unhashed value in the line.
   153	    for key in "${field}" "${name}_file" "${name}"; do
   154	        (($(count_of "${key}") <= 1)) || {
   155	            echo "dispatch: ${field}: ${key}= appears more than once" >&2
   156	            exit 1
   157	        }
   158	    done
   159	    if value_of "${name}_file" > /dev/null && value_of "${name}" > /dev/null; then
   160	        echo "dispatch: ${field}: both ${name}_file= and ${name}= name a file" >&2
   161	        exit 1
   162	    fi
   163	    path="$(value_of "${name}_file" || value_of "${name}")" || {
   164	        echo "dispatch: ${field} has no ${name}_file= or ${name}= field naming its file" >&2
   165	        exit 1
   166	    }
   167	    [[ ${path} == /* ]] || path="${root}/${path}"
   168	    [[ -f ${path} ]] || {
   169	        echo "dispatch: ${field}: ${path} does not exist" >&2
   170	        exit 1
   171	    }
   172	    got="$(shasum -a 256 "${path}")" && got=${got%% *}
   173	    [[ ${got} == "${want}" ]] || {
   174	        echo "dispatch: ${field} mismatch: the line has ${want}, ${path} hashes to ${got}" >&2
   175	        exit 1
   176	    }
   177	done
   178	if [[ ${tokens[0]} == AGMSG-TASK ]]; then
   179	    tf="$(value_of task_file)" && [[ ${tf} == /* ]] || tf="${root}/${tf}"
   180	    # The Makefile's UV_PYYAML: offline when the cache holds PyYAML, else through the index. --no-project: a
   181	    # pyproject.toml in the caller's directory is never discovered, synced or built (the Bot's P1 4292675906).
   182	    # The interpreter is named, python3 as mise answers it under env -i at the root, else python3 on PATH, and uv
   183	    # runs under env -i with an allowlist, so no VIRTUAL_ENV, CONDA_PREFIX, UV_* or PYTHON* variable reaches it
   184	    # (local:9df6b0c:1, C-57, the Bot's P1 4300102967).
   185	    py="$(cd -- "${root}" && { env -i PATH="${PATH}" HOME="${HOME}" mise which python3 2> /dev/null || command -v python3; })" || py=
   186	    [[ ${py} == /* ]] || {
   187	        echo "dispatch: no python3 interpreter to pin for uv" >&2
   188	        exit 1
   189	    }
   190	    clean=(env -i PATH="${PATH}" HOME="${HOME}")
   191	    for v in LANG LC_ALL; do
   192	        [[ -z ${!v:-} ]] || clean+=("${v}=${!v}")
   193	    done
   194	    while IFS= read -r v; do
   195	        [[ ${v} != AGMSG_* ]] || clean+=("${v}=${!v}")
   196	    done < <(compgen -e)
   197	    uvy=(uv run --no-project --offline --python "${py}" --with pyyaml)
   198	    here="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
   199	    # Run from the trusted root, so a caller's .python-version or virtual environment picks no interpreter (4299651928).
   200	    uvr() { (cd -- "${root}" && "${clean[@]}" "${uvy[@]}" "$@"); }
   201	    uvr python -I -c 'import yaml' > /dev/null 2>&1 || uvy=(uv run --no-project --python "${py}" --with pyyaml)
   202	    read -r -d '' brief << 'PY' || true
   203	import sys, yaml
   204	def unique(loader, node, deep=False):
   205	    keys = [loader.construct_object(k, deep=deep) for k, _ in node.value]
   206	    if len(keys) != len(set(keys)):
   207	        raise yaml.YAMLError("duplicate key")
   208	    return loader.construct_mapping(node, deep)
   209	class Loader(yaml.SafeLoader):
   210	    pass
   211	Loader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique)
   212	lines = open(sys.argv[1], encoding="utf-8").read().split("\n")
   213	end = lines.index("---", 1) if lines[0] == "---" else None
   214	front = yaml.load("\n".join(lines[1:end]), Loader) if end else None
   215	sys.exit(0 if isinstance(front, dict) and front.get("kind") == "review" else 1)
   216	PY
   217	    # Fail-closed: only a parsed front matter whose kind is review skips the checker.
   218	    if ! uvr python -I -c "${brief}" "${tf}" > /dev/null 2>&1; then
   219	        out="$(uvr python -I "${here}/task-consistency-check.py" --root "${root}" "${tf}" 2>&1)" || {
   220	            echo "dispatch: ${tf} fails the task-consistency check" >&2
   221	            printf '%s\n' "${out}" >&2
   222	            exit 1
   223	        }
   224	    fi
   225	fi
   226	[[ -n ${record} ]] || exec agmsg-dispatch "${team}" "${from}" "${to}" "${pane}" "${line}"
   227	
   228	# Modes: `check` parses the record and writes the pre-send window to the window file; `append` aligns
   229	# history.sh's post-send window on stdin with it, takes the sent row's read marker (● unread, ○ read) and appends it.
   230	read -r -d '' recorder << 'PY' || true
   231	import fcntl, json, os, re, shutil, sys, tempfile
   232	from pathlib import Path
   233	
   234	mode, path, line, sender, to, window, task = sys.argv[1:8]
   235	record = Path(path)
   236	rows = [r for r in sys.stdin.read().splitlines() if r]
   237	
   238	def refuse(pairs):
   239	    keys = [k for k, _ in pairs]
   240	    dup = next((k for k in keys if keys.count(k) > 1), None)
   241	    if dup is not None:
   242	        sys.exit(f"dispatch: {path}: duplicate key {dup}")
   243	    return dict(pairs)
   244	
   245	def constant(name):
   246	    sys.exit(f"dispatch: {path}: non-finite number {name}")
   247	
   248	def load():
   249	    # newline="": a CRLF record keeps its line endings (thread 4256987087).
   250	    with open(record, newline="") as f:
   251	        text = f.read()
   252	    block, rest = {}, text
   253	    if re.match(r"---\r?\n", text):
   254	        m = re.match(r"---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
   255	        if not m:
   256	            sys.exit(f"dispatch: {path}: the block between the first two --- lines is not closed")
   257	        try:
   258	            block = json.loads(m.group(1), object_pairs_hook=refuse, parse_constant=constant)
   259	        except json.JSONDecodeError as e:
   260	            sys.exit(f"dispatch: {path}: the block is not valid JSON: {e}")
   261	        rest = text[m.end():]
   262	        if not isinstance(block, dict):
   263	            sys.exit(f"dispatch: {path}: the block is not a JSON object")
   264	    if not isinstance(block.setdefault("dispatch", []), list):
   265	        sys.exit(f"dispatch: {path}: dispatch is not a list")
   266	    # Thread 4254844587: another task's record never takes this task's dispatch.
   267	    if "task" in block and block["task"] != task:
   268	        sys.exit(f"dispatch: {path} is the record of task {block['task']}, the line is task {task}")
   269	    return block, rest
   270	
   271	row = re.compile(r"^\s*(\S+)\s+\[([^\]]+)\]\s+(\S+)\s+→\s+(\S+):\s(.*)$")
   272	# (marker, [timestamp, sender, recipient, text]); the marker is left out of the alignment, a read flips it.
   273	seen = [(m.group(1), list(m.group(2, 3, 4, 5))) for m in map(row.match, rows) if m]
   274	if mode == "check":
   275	    load()
   276	    with open(window, "w") as f:
   277	        json.dump([fields for _, fields in seen], f)
   278	    sys.exit(0)
   279	with open(window) as f:
   280	    pre = json.load(f)
   281	post = [fields for _, fields in seen]
   282	n, m = len(pre), len(post)
   283	# Shift j: the post-send window without its j newest rows equals the pre-send one without its e = n + j - m oldest.
   284	fits = [m] if n == 0 else [j for j in range(m) if 0 <= n + j - m < n and post[: m - j] == pre[n + j - m :]]
   285	if len(fits) != 1:
   286	    sys.exit(
   287	        "dispatch: the post-send window does not align uniquely with the pre-send one; "
   288	        "the line may be on the bus unrecorded; raise BUS_READ_WINDOW or check the bus"
   289	    )
   290	if fits[0] == 0:
   291	    sys.exit(f"dispatch: this send added no bus row; {path} is unchanged")
   292	# Another seat's row may land after this send, so the send is the last new row equal to the line.
   293	marks = [mark for mark, (_, s, r, text) in seen[m - fits[0] :] if (s, r, text) == (sender, to, line)]
   294	if not marks:
   295	    sys.exit("dispatch: no new row equals the line; the line may be on the bus unrecorded; check the bus")
   296	# Thread 4255272797: the read-modify-write holds the record directory's lock, so a second dispatch waits.
   297	lock = os.open(record.parent, os.O_RDONLY)
   298	fcntl.flock(lock, fcntl.LOCK_EX)
   299	block, rest = load()
   300	block["dispatch"].append(f"{line} read_at={'read' if marks[-1] == '○' else 'unread'}")
   301	body = json.dumps(block, sort_keys=True, indent=2, ensure_ascii=False)
   302	# Thread 4254844595: the line is already sent, so the record is replaced whole or not at all.
   303	fd, tmp = tempfile.mkstemp(dir=record.parent, prefix=f".{record.name}.")
   304	try:
   305	    with os.fdopen(fd, "w", newline="") as f:
   306	        f.write(f"---\n{body}\n---\n{rest}")
   307	        f.flush()
   308	        os.fsync(f.fileno())
   309	    shutil.copymode(record, tmp)
   310	    os.replace(tmp, record)
   311	except BaseException:
   312	    Path(tmp).unlink(missing_ok=True)
   313	    raise
   314	PY
   315	[[ ${record} == /* ]] || record="${PWD}/${record}"
   316	# The local review of 0d199475 (C-32): a record mkstemp cannot replace would fail only after the send.
   317	if [[ ! -f ${record} || ! -w ${record} || ! -w "$(dirname -- "${record}")" ]]; then
   318	    echo "dispatch: the record ${record} cannot be written" >&2
   319	    exit 1
   320	fi
   321	limit=${BUS_READ_WINDOW:-200}
   322	[[ ${limit} =~ ^[1-9][0-9]*$ ]] || usage
   323	task="$(value_of task_id)"
   324	# A private window file (mode 0600, a fresh name), removed whatever the exit.
   325	window="$(mktemp "${TMPDIR:-/tmp}/dispatch-window.XXXXXX")"
   326	trap 'rm -f -- "${window}"' EXIT
   327	# Team-wide: history.sh renames the calling pane after an agent argument (thread 4254399805).
   328	bus() { "${AGMSG_SCRIPTS:-${HOME}/.agents/skills/agmsg/scripts}/history.sh" "${team}" "" "${limit}"; }
   329	bus | python3 -I -c "${recorder}" check "${record}" "${line}" "${from}" "${to}" "${window}" "${task}"
   330	rc=0
   331	agmsg-dispatch "${team}" "${from}" "${to}" "${pane}" "${line}" || rc=$?
   332	bus | python3 -I -c "${recorder}" append "${record}" "${line}" "${from}" "${to}" "${window}" "${task}"
   333	exit "${rc}"

 succeeded in 139ms:
     1	---
     2	format: 2
     3	task_id: dotfiles-T128-regime-v3-a01
     4	kind: design
     5	security: true
     6	design_review:
     7	  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
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
    28	  dotfiles-T128-v0-main-tests-a02: [INV-12]
    29	  dotfiles-T128-gate-evidence-a01: [INV-6]
    30	  dotfiles-T128-gate-evidence-a02: [INV-6]
    31	  dotfiles-T128-gate-evidence-a03: [INV-6]
    32	  dotfiles-T128-gate-evidence-a04: [INV-6]
    33	supersedes:
    34	  - dotfiles-T126-regime-v2-a01
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
    71	  - claim: required workflows are organization-only; pull_request_target runs the base branch's workflow file and is eligible as a required status check
    72	    command: "WebFetch docs.github.com available-rules-for-rulesets (enterprise-cloud) and troubleshooting-required-status-checks"
    73	    output: "Ruleset workflows can be configured at the organization or enterprise level; required checks count when triggered by push, pull_request, pull_request_review, pull_request_target, deployment, deployment_status; pull_request_target runs in the context of the default branch of the base repository"
    74	  - claim: codex exec --output-schema is enforced server-side as a strict JSON schema; codex 0.161.0 rejects --full-auto and -a on exec
    75	    command: "codex exec --help; read codex-rs/exec/src/lib.rs and codex-api/src/common.rs at rust-v0.161.0"
    76	    output: "text.format = {type: json_schema, strict: true, schema}; error: unexpected argument '--full-auto' found; approval policy for exec is set with -c approval_policy=never"
    77	  - claim: claude -p --bare requires an API key and skips hooks; without --bare a -p run executes the project's hooks; --json-schema returns structured_output; --max-budget-usd caps spend
    78	    command: "WebFetch code.claude.com/docs/en/headless and cli-reference"
    79	    output: "--bare never reads OAuth credentials or the system keychain; set ANTHROPIC_API_KEY; without --bare -p runs the hooks in a project's .claude/settings.json; the structured output is in the structured_output field; spend can pass the cap, so leave headroom"
    80	  - claim: the vendor's own reset rule is two corrections
    81	    command: "WebFetch code.claude.com/docs/en/best-practices"
    82	    output: "If you've corrected Claude more than twice on the same issue in one session, the context is cluttered with failed approaches. Run /clear and start fresh with a more specific prompt"
    83	  - claim: the audit was not the wall-clock bottleneck
    84	    command: "stat .orchestration/validation/dotfiles-T119-*-audit-*.md; history.sh dotfiles-conformance (TASK 2026-10-09T21:26Z to ACCEPTANCE 2026-10-10T08:32Z)"
    85	    output: "four audit files written 11:48, 13:55, 15:52, 17:23 local, each run 15-25 minutes, about 1.3 h of an 11.1 h task"
    86	  - claim: both runtimes' Stop hooks are soft signals, not hard stops, so the merge gate is the mandatory point
    87	    command: "WebFetch learn.chatgpt.com/docs/hooks; WebFetch code.claude.com/docs/en/hooks (Stop section)"
    88	    output: "Codex: decision block doesn't reject the turn but injects a continuation prompt; Claude: 8-consecutive-continuation cap that resets each time Claude calls a tool"
    89	  - claim: the seat's session transcript carries per-message token usage on this host
    90	    command: "grep -o '\"usage\":{[^}]*}' ~/.claude/projects/-Users-a0004262-Workspace-dotfiles--claude-worktrees-worker-c/3747b995-3bb1-4c51-8421-4b1e672b442a.jsonl | tail -1; grep -c '\"usage\"' <same file>"
    91	    output: "usage with input_tokens, cache_creation_input_tokens, cache_read_input_tokens, output_tokens; 5168 usage entries (format internal to Claude Code per its docs)"
    92	  - claim: history.sh truncates to 20 rows by default, so counters read the storage facade or pass a limit
    93	    command: "history.sh dotfiles-conformance | wc -l; history.sh dotfiles-conformance --limit 600 | wc -l"
    94	    output: "20; 256 (the whole team history)"
    95	  - claim: "workflow_dispatch runs a workflow only once its file is on the default branch, so regime.yml is merged unlisted, dry-run from main against a closed PR, then listed as required"
    96	    command: "WebFetch docs.github.com events-that-trigger-workflows (workflow_dispatch)"
    97	    output: "This event will only trigger a workflow run if the workflow file exists on the default branch"
    98	  - claim: "bare mode loads skills from the .claude/skills/ folder of a directory named with --add-dir, so the claude fallback must refuse a head that changes .claude/skills/**"
    99	    command: "WebFetch code.claude.com/docs/en/headless (bare mode section)"
   100	    output: "bare mode loads skills from its .claude/skills/ folder (of directories named with --add-dir)"
   101	  - claim: "a permissions.ask rule forces a native prompt even in auto mode, and only the human operator answers a permission prompt, so a command under such a rule runs only on a human answer"
   102	    command: "WebFetch code.claude.com/docs/en/auto-mode-config; home/dot_config/claude/rules/agmsg-orchestration.md (Permissions)"
   103	    output: "permissions.ask rules always force a permission prompt, even in auto mode; Agent-to-agent permission approval is forbidden; only the human operator answers a permission prompt"
   104	  - claim: "GitHub's default Actions policy will block pull_request_target on public repositories from 2026-11-02 unless an applicable event policy explicitly allows it; it runs in evaluate mode now"
   105	    command: "WebFetch docs.github.com/en/actions/reference/security/securely-using-pull_request_target"
   106	    output: "On November 2, 2026, GitHub will enforce the default policy for affected repositories; create or update an applicable Actions event policy that explicitly allows pull_request_target; Currently runs in evaluate mode"
   107	
   108	---
   109	
   110	# AGMSG-TASK dotfiles-T128-regime-v3-a01 — DESIGN: regime v3, the redesign after the 2026-10-10 halt
   111	
   112	Drafted 2026-10-11 (local) by the orchestrator seat `claude-deep-dot` under a recorded bootstrap exception (operator decision 2026-10-11: the orchestrator drafts, a fresh context on the review profile must accept before any implementing task is dispatched). Operator direction (pasted 2026-10-11): when substantive findings repeat, the design, implementation or verification is wrong and a mechanism must force the redo; prose alone repeats the mistake; the auditor must be able to find the orchestrator's and the worker's mistakes; efficiency, quality and cost are optimised together; the auditor must not become the bottleneck and the audit stages must be chosen; all of it grounded in the tools' official documentation and current practice. Research inputs: fact sheets on Claude Code 2.1.293, Codex CLI 0.161.0, GitHub rulesets and Actions, and the research literature, read 2026-10-11; the measured baseline below.
   113	
   114	## 1. Finding: the fix program tripped its own rule
   115	
   116	By T126 INV-6 as written: wave 1 (PR #313) 8 amendments (limit 4) and 2 revises (limit 2); wave 3b (PR #314) Bot P1 on two post-RESULT heads. The orchestrator was drafting a waiver for #313. T120 was reset only on the operator's question. The regime is therefore reset here by its own rule; this document is the redesign, and T126 and T124 are superseded (their accepted ideas are kept where named).
   117	
   118	Measured baseline (history + GitHub):
   119	
   120	| task | PR | files | +lines | amendments | questions | revises | audits (incorrect) | Bot threads (heads) | P0/P1 | wall |
   121	|---|---|---|---|---|---|---|---|---|---|---|
   122	| T114 | - | - | - | 0 | 0 | 6 | 3 (3) | - | - | 21.5h |
   123	| T118 | 310 | 35 | 881 | 7 | 0 | 20 | 8 (7) | 16 (7) | 0 | 10.6h |
   124	| T119 | 312 | 37 | 3191 | 8 | 8 | 5 | 4 (4) | 25 (11) | 7 | 11.1h |
   125	| T120 | 315 | 19 | 1489 | 8 | 1 | 0 | 0 | 15 (5) | 8 | reset |
   126	| T124 W1 | 313 | 20 | 2642 | 8 | 6 | 2 | 0 | 52 (10) | 31 | halted, reset |
   127	| T124 W3b | 314 | 9 | 1462 | 5 | 0 | 0 | 0 | 24 (4) | 2 | halted, reset |
   128	
   129	Every acceptance record to date says `cost: n/a`.
   130	
   131	## 2. Root causes, each with its evidence
   132	
   133	R1 to R8 in the front matter. The literature behind R1: intrinsic self-correction without an external signal degrades after the first round (Huang et al. 2023); a second review round on the same artifact raised recall slightly and false positives by 62% (arXiv 2603.16244); multi-round review degrades with rounds (MCR-Bench); revising an already-correct state loses correct work unless verifier evidence is bound to the exact code state (arXiv 2607.24604). Behind R3: Google's review study (median change 24 lines, ~90% under 10 files) and its CL-size guidance. Behind R5 and R6: a judge without a reference is lenient and a reference flips 9-85% of verdicts toward correct (2607.12885); format-restricted generation degrades reasoning, so verdicts reason first and then fill the schema (2408.02442); Anthropic's harness-design post: a standalone skeptical evaluator is tractable where a self-critical generator is not, and the evaluator is worth its cost only where the task exceeds the model's reliable solo capability, which is what the tier table encodes.
   134	
   135	## 3. Principles (each names what it reuses and what it deletes)
   136	
   137	- **P1 One deterministic fact per round (INV-3).** Reuses tests/unit, CI, `pr-feedback.py`. Deletes free-form revise rounds and the audit-per-round habit.
   138	- **P2 Declarative over imperative at trust boundaries (INV-1, INV-5, INV-7).** Reuses `jsonschema`, PyYAML, `codex exec --output-schema`, `claude -p --json-schema`. Deletes the bespoke YAML parser, the glob NFA, the prose verdict grammar, regex parsing of `.last.md`, and the T126 "process_tiers.json next to the module" indirection (the validator reads the manifest with PyYAML).
   139	- **P3 Small one-invariant PRs enforced in CI (INV-2).** Reuses GitHub required checks and the strict up-to-date ruleset already in force. Deletes waves declared inside a task file.
   140	- **P4 Main-pinned mechanical checks in CI; host gate only for history-anchored rules (INV-1, INV-2, INV-8 in CI; INV-3, INV-5 record, INV-6, INV-7 anchor, INV-11 on the host).** Reuses `pull_request_target`, the `changes` job pattern that reports success for an `.orchestration`-only diff. Deletes PR #313's `REVIEW_TREE` idea (never on `main`) and the copy step of untracked evidence into the gate's cwd. The host gate `make require-crit-review` keeps its evidence rules and changes three of them in named waves: the audit verdict and categories come from the schema JSON with the `AGMSG-AUDIT` record and the category lock (V2b), the reset backstop and the Bot-head count (V3a), the history-anchored design review (V4); it continues to run from the orchestrator's main checkout.
   141	- **P5 Research before dispatch; a question ends the task, not amends it (INV-4).** Reuses history (`amendment=`, `status=question`). Deletes the amendment-per-question practice. The task file's `premises` block is the mechanical residue of "verify every CLI constraint by running the real command".
   142	- **P6 Reset is mechanical, loop-time, and released only by another context or the operator (INV-6).** Reuses `scripts/require-crit-review.py` as the mandatory point, `agent-stop-gate.sh` and the Codex `[hooks].Stop` as the early signal (both soft by their documented caps: Claude's 8-continuation cap, Codex's continuation prompt), `check-regime-boundary.sh` for the re-dispatch detector. Deletes the orchestrator-written redesign (the redesign author is a `review`-profile seat or a fresh headless context; the `redesign` profile of T124 v4 is dropped: `review` is the same model and effort as `deep`, so independence of context is the whole lever, and T124 round 1 showed it works).
   143	- **P7 Audit staging by tier; the auditor never serializes the pipeline (INV-5, process_tiers).** See section 4.
   144	- **P8 Cost measured, budgets per tier (INV-9).** Reuses the JSON cost fields the runtimes already emit and the session transcripts. Deletes `cost: n/a`.
   145	- **P9 Parallelism with disjoint files and early push (INV-10).** Reuses `herdr-agents --add-worker`, draft PRs.
   146	- **P10 Routing stays by boundary.** Claude-boundary sources to a Codex seat, Codex-boundary to a Claude seat, permgate and shared gate sources to the operator, as the agmsg-orchestration skill's step 3 states; nothing here changes that.
   147	
   148	## 4. Audit stages (process_tiers; the one table the validator reads)
   149	
   150	| stage | who | when | tier docs | tier review | tier design | cost |
   151	|---|---|---|---|---|---|---|
   152	| 0 design review | a fresh Claude context on the review profile and a Codex read-only review of the same hash, schema receipts (INV-7) | before any code | - | - | required | minutes |
   153	| 1 worker checks | worker in its sandbox: invariant tests first, shellcheck, unit tests | before every push | required | required | required | none for the regime |
   154	| 2 CI + Bot | main-pinned `regime` check (schema, caps, evidence shape) + unit tests + Codex Bot | every push, in parallel | required | required | required | none |
   155	| 3 schema audit | headless read-only `codex exec --output-schema`, pooled 2, started by `make audit-head` once CI is green and the Bot reviewed or 15 min passed, once per RESULT head, reused for an evidence-only head by tree equality (INV-5) | per RESULT head | - | required | required, with invariant map and permgate window | the scarce resource, now off the critical path |
   156	| 4 acceptance | orchestrator: sweep, dispositions, record, host gate, merge `--match-head-commit` | per RESULT | required | required | required | minutes |
   157	
   158	Tier derivation: docs = prose-only `allowed_files` outside the regime's own rule prose (`home/dot_config/claude/rules/**`, the agmsg-orchestration SKILL, `AGENTS.md`, README), which is review tier by explicit list; review = the existing review-tier paths (scripts, hooks, tests, templates); design = the explicit design-tier list from T124 INV-2 v3 (install/**, setup.sh, the gate scripts, `executable_herdr-agents`, `executable_permgate`, Codex and Claude policy, sandbox and permission settings, credential helpers). Round limits: docs 1 revise; review and design 2 revises then reset. Profiles: worker `standard` (docs `express`), review `review`, audit `audit`.
   159	
   160	Why stage 3 is not the queue: the orchestrator starts it with `make audit-head` when the RESULT arrives (the wait on CI and the Bot is inside the target), it runs concurrently (pool of two, each in its own detached worktree), once per head, and an evidence-only head reuses the earlier audit by tree equality; the measured cost of the old serial form was 1.3 h of 11.1 h, so the throughput levers are P1 and P6, and the pool removes the residual queue.
   161	
   162	## 5. Enforcement map
   163	
   164	| invariant | enforcement point |
   165	|---|---|
   166	| INV-1 | `.github/workflows/regime.yml` (`pull_request_target`, required check `regime`: validates `.orchestration/<task id>/task.md` from the PR head read as data, refuses workflow edits outside a design-tier task; an explicit Actions event policy allowing `pull_request_target` is set by the operator before 2026-11-02, named in V1c's acceptance record), `scripts/validate-task.py` (schema + PyYAML, about 80 lines), `schemas/task.json`, `scripts/lib/high_risk_paths.py` (new module: tier lists and `tier_of`), `scripts/legacy-task-ids.txt` (grandfather list), `process_tiers` in the manifest; host gate compares the copy's sha256 with `task_sha256=` in history (V3a); stage waivers by `scripts/regime-waive.sh` under its `permissions.ask` rule, written outside the sandbox write roots (V3a) |
   167	| INV-2 | `regime.yml` step with `scripts/pr-caps.sh` and the task.md invariant-id comparison against the design's `implementing_tasks` |
   168	| INV-3 | `regime-check.sh` step: the test selector named in `.orchestration/<task id>/revise.yaml` (sibling of the byte-identical task.md) exists on the head and its file differs between `previous_head` and the head; a `revise-check` job in `test.yaml` (PR context, required) runs exactly that selector on both heads; the host gate's `previous_head` history check and validation-file line are V2b's |
   169	| INV-4 | `scripts/validate-task.py` (premises required for code and design tasks); `agent-stop-gate.sh` early signal on the second AGMSG-TASK or second PONG question; the merge backstop is INV-6's |
   170	| INV-5 | `schemas/audit.json` (findings and invariant map before verdict), `scripts/audit-head.sh` (about 100 lines: detached worktree, `codex exec`, fallback, sha256 to history under the audit identity, `.last.md` render; PR #314's hardening kept), `make audit-head` target around `gh pr checks --watch` and the SKILL's Bot list loop with its 15-minute `bot: none` rule (no daemon), `AGENTS.md` Audit section; gate: JSON verdict and categories, `AGMSG-AUDIT` lookup, category lock, tree-equality acceptance of an earlier head (V2b) |
   171	| INV-6 | `scripts/require-crit-review.py` (mandatory: history counts, Bot heads from `original_commit_id` recorded by `scripts/pr-feedback.py`, audit heads from the main checkout's audit JSONs whose sha256 matches their `AGMSG-AUDIT` record, reset record or a `scripts/regime-waive.sh` waiver), `scripts/agent-stop-gate.sh` and the manifest's `codex.hooks` Stop entry (early signal, history counts only, within the 3 s history budget), `scripts/check-regime-boundary.sh` (closed-unmerged PR without a reset record; over-count task without an accepted or reset record; waiver listing) |
   172	| INV-7 | `scripts/design-review.sh` + `schemas/design-review.json`: two headless runs per design hash, `claude -p` under `claude-review-dot-hNNN` and `codex exec --sandbox read-only` under `codex-review-dot-hNNN`, each joining for the run and sending its RESULT; gate: both RESULTs precede the implementing TASK, both hashes recomputed, whole-file form accepted for pre-V4 receipts |
   173	| INV-8 | worker writes under `.orchestration/<task id>/` on the branch (task.md copy first); `regime.yml` validates the evidence JSON shapes; the gate's existing path rules keep the orchestrator's records under `validation/` and `acceptance/` |
   174	| INV-9 | `scripts/accept-task.py` (sweep, dispositions scaffold, record rows, gate invocation, merge command, cost fields), budgets in `process_tiers`, `check-regime-boundary.sh` warning |
   175	| INV-10 | `scripts/check-regime-boundary.sh` and `scripts/accept-task.py` from `history.sh` timestamps (storage facade or `--limit`, never the 20-row default), the draft PR's `created_at` from `gh api pulls/<n>`, and the task's `after` list against acceptance records |
   176	| INV-11 | `executable_permgate` (operator-routed, Codex security review) + gate cross-check |
   177	| INV-12 | one test module per script; `make unit-test` in CI; the `main-tests` required job (V0): main's test modules for every script outside the PR's `allowed_files`, deciding inside its own job; the trusted-root audit reads the test diff beside the code diff for scripts inside it; the auditor checks per PR that no new hand-written parser sits at a trust boundary (a `conformance` finding) |
   178	| prose | SKILL, `agmsg-orchestration.md`, `pr-integration.md`, `crit-review.md`, `model-selection.md`, README: each wave edits only the sections it implements |
   179	
   180	## 6. Waves (one PR, one invariant, within INV-2's caps; each task file reviewed by a fresh context before dispatch)
   181	
   182	- **V0** INV-12: the `main-tests` required job in `test.yaml` (main's `tests/unit` modules of every script outside the PR's `allowed_files`, run in the PR's context, deciding inside the job as the A5 workflows do) and the protocol in the Worker Playbook; lands before every other wave as `dotfiles-T128-v0-main-tests-a02` (A301; PR #317 and the audit of `adcf783b` are its input). Claude seat; design tier (workflow); the operator lists the check at its acceptance.
   183	- **V1** INV-1, validation only (operator direction 2026-10-11, relayed through the review seat; also the cap: the undivided V1 sat at 500 added lines): `schemas/task.json`, `scripts/validate-task.py`, `scripts/lib/high_risk_paths.py`, `scripts/legacy-task-ids.txt` (from PR #313; data, excluded from the line cap), `tests/unit/test_validate_task.py`. Claude seat. Design tier: this review is its stage 0. Precondition: this design is on `main` through a boundary PR before V1's TASK is dispatched.
   184	- **V1c** INV-1, the CI check (after V1): `scripts/regime-check.sh`, `.github/workflows/regime.yml` (task.md validation, workflow-edit refusal, `workflow_dispatch` dry run), `tests/unit/test_regime_check.py`, `process_tiers` in the manifest, SKILL step 3 paragraph, README sentence. Claude seat. Acceptance names the operator action that lists `regime` as a required check, after the dry run from `main` against a closed PR. Two tasks map to INV-1 as V2 and V2b map to INV-5.
   185	- **V1b** INV-2 (after V1c): `scripts/pr-caps.sh`, the caps and invariant-id steps in `regime-check.sh`, tests, one SKILL sentence.
   186	- **V2** INV-5 runner: `schemas/audit.json` (PR #314's, reordered), `scripts/audit-head.sh` with PR #314's hardening, `make audit-head`, `AGENTS.md` Audit section, tests, the SKILL's task-level audit bullet. Claude seat.
   187	- **V2b** INV-5 gate: `scripts/require-crit-review.py` reads the JSON verdict and categories, requires the `AGMSG-AUDIT` record, locks orchestration and conformance at P0-P2 to waiver or reset, accepts an earlier audited head by tree equality, and requires the INV-3 `check=` line in the validation file; tests. Operator-routed gate source (delegable to a Claude seat with recorded opt-in).
   188	- **A3** INV-6 (plan 006 Phase A, `dotfiles-T128-regime-counters-a01`): `scripts/regime-counters.sh` computes every INV-6 count from history and GitHub and prints the thresholds reached; `check-regime-boundary.sh` reports a reached threshold without a reset record or waiver; the orchestrator runs it before every acceptance action. V3a wires that script into the hook and the gate.
   189	- **V3a** INV-6: `scripts/pr-feedback.py` (`original_commit_id` on review_comment items), `require-crit-review.py` reset backstop and `task_sha256` comparison, `agent-stop-gate.sh` history counts (revises, amendments, questions) as the early signal, the Codex Stop entry in the manifest and its rendered template, `scripts/regime-waive.sh` with its `permissions.ask` rule in the manifest's Claude permissions block (no permgate policy entry), `check-regime-boundary.sh` detector and waiver listing; tests. Four boundaries in one PR (gate source, Claude hook and permission source, Codex hook source): an operator PR by construction, reviewed by a Codex `security`-profile seat before acceptance.
   190	- **V3b** INV-4: premises in the schema and validator, SKILL text (questions end the task; one answering TASK at most). Claude seat; no hook source (the counting is V3a's).
   191	- **V3c** INV-3: `check=` and `previous_head=` in the ACCEPTANCE contract (SKILL), `revise.yaml` beside task.md in the Worker Playbook, the `regime-check.sh` step, the `revise-check` job in `test.yaml`; tests. Claude seat (no gate source: the history check and validation-file line are V2b's).
   192	- **V3d** INV-10: idle and first-push computations in `check-regime-boundary.sh` and `accept-task.py` (the latter lands in V5b; V3d adds them to the boundary check only). Claude seat.
   193	- **V4** INV-7: `scripts/design-review.sh` (Claude and Codex runs under their `-review-dot-hNNN` identities), `schemas/design-review.json`, the history anchor and hash check in the gate (two RESULTs, both forms), SKILL paragraph. Operator-routed for the gate part.
   194	- **V5a** INV-8: `.orchestration/<task id>/` paths in the Worker Playbook, task.md copy as the first commit, evidence-shape validation in `regime.yml`, boundary commit reduced to orchestrator records. Claude seat.
   195	- **V5b** INV-9: `scripts/accept-task.py`, cost fields with source digests, budgets in `process_tiers`, `check-regime-boundary.sh` budget warning. Claude seat. Size: the sweep, scaffold and gate invocation already exist as commands; the script sequences them, about 200 lines.
   196	- **V6** INV-11: `executable_permgate` session_id and cwd; gate cross-check. Operator-routed, Codex `security` profile review.
   197	
   198	Order: V0, then the design-tier code waves V1, V1c, V1b, V2, V2b, V3a, V3b, V3c, V3d, V4, V5a, V5b, V6, one PR each. File-disjoint pairs may run concurrently (V1 with V2; V3b with V3d); the gate-source waves (V2b, V3a, V4's gate part) run serially.
   199	
   200	## 7. Thresholds (operator confirmed 2026-10-11)
   201	
   202	revise 2; amendments 2; questions 2; Bot P0/P1 heads 2 (post-RESULT); audit implementation or specification P0-P1 heads 2; PR 15 changed files (the file count excludes `.orchestration/` only) and 500 added lines outside `tests/`, `.orchestration/` and the data list `scripts/legacy-task-ids.txt`; first push 30 minutes; idle 20 minutes; workers 3; audit pool 2; audit once per head; docs tier 1 revise.
   203	
   204	## 8. Disposition of the halted work
   205	
   206	PR #313 and #314 closed unmerged as reference branches (reset records in `.orchestration/acceptance/…-design-reset.md`); PR #315 is a draft per T120's reset record; the four worker seats are removed. Salvaged: the format-2 key set, the tier table, `scripts/legacy-task-ids.txt` and the test ideas of `tests/unit/test_validate_task.py` (V1); `scripts/schemas/audit.json`, the AGENTS.md Audit text, the pre-push hardening and the `AGMSG-AUDIT` record (V2). Dropped with the `redesign` profile: PR #313's `home/dot_codex/modify_private_redesign.config.toml`. T127 (T120's redesign) follows V1 under this regime.
   207	
   208	## 9. Residuals, stated
   209	
   210	- Workers' conduct is checked mechanically only for Claude seats and only after V6; until then the sandbox record is self-reported.
   211	- `pull_request_target` runs with the base repository's token on a public repository: the `regime` job reads PR files as data with `contents: read` only, checks out `main`'s scripts, and never executes anything from the PR; a change to `.github/workflows/regime.yml` itself is a design-tier change under INV-1.
   212	- A repository admin can edit the ruleset; that path is visible on GitHub, not prevented, consistent with the waiver anchor.
   213	- Operator authentication does not exist on this machine: every seat runs as the one user and every GitHub action as the one account, so no record can prove that the operator rather than the orchestrator wrote it. The regime therefore makes every waiver pass through a native permission prompt (`permissions.ask`, which no classifier, hook or agent may answer) and makes every waiver visible in three places; it does not claim more. The Codex design review of round 7 asked for authenticated operator events; this is the honest limit of what the machine offers.
   214	- The design-review receipt's anchor in history is only as strong as the `-review-` identity's independence; a fresh headless context per review (V4) is the mitigation, and until V4 lands a seated `review`-profile identity reviews.
   215	- GitHub's default Actions policy blocks `pull_request_target` on public repositories from 2026-11-02 (evaluate mode today); the operator sets an explicit event policy allowing it before then, or the `regime` job loses its main-pinned form and the host gate becomes the only gate again. Named in V1c's acceptance record.
   216	- The `regime` job runs `main`'s workflow file, so a change to `regime.yml` is never exercised by its own PR; its logic therefore lives in scripts with unit tests, and a `workflow_dispatch` dry run precedes listing it as required.
   217	- `regime.yml` discipline, stated once: `main` stays at the workspace root (`actions/checkout` default ref under `pull_request_target`); the PR head is fetched as data and read with `git show <head sha>:<path>` into a directory never on `PATH`; the diff range is the merge-base of `github.event.pull_request.head.sha` with `main`, never `github.sha`; `uv run --no-project`; `yaml.safe_load`; no `make`, no script, no dependency file from the PR tree; `permissions: contents: read`; no secrets.
   218	- The seven existing required checks still run on `pull_request` from the PR's own workflow files; INV-1's workflow-edit refusal in the `regime` job is what closes R8 for them.
   219	- Bootstrap: this design was written by the orchestrator that dispatched the abandoned tasks. The reset records carry the operator's waiver form (`DESIGN_RESET_WAIVED_BY=operator`, decision 2026-10-11), this review is the only release, and no further orchestrator-authored design follows under T128; T127 (T120's redesign) is written by another context.
   220	
   221	## 10. Design review (round 15 requested: plan 006 A102, second pair)
   222	
   223	Round 1 (`.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review.md`, `claude-review-dot-a001`, 2026-10-10T21:15Z, verdict `revise`): INV-7, INV-8, INV-11, INV-12 accepted with notes; INV-1, 2, 3, 4, 5, 6, 9, 10 rejected with corrections; findings F1-F9. v2 adopts every item: the task.md copy and `task_sha256` anchor (F1), the per-task invariant-set rule and the workflow-edit refusal (F2), the gate changes assigned to V2b/V3a/V4 with the category lock, the Bot-wait timeout and the tree-equality rule (F3), the merge backstop as the mandatory point, `original_commit_id`, the audit-JSON source, the Stop-hook budget split and the boundary detector (F4), the single amendment count over every TASK (F5), INV-9/INV-10 moved out of the Stop hook (F6), the reset records corrected to `claude-review-dot-a001` with the waiver form and the thread ids (F7), rule prose in the review tier (F8), premise 1 restated and three premises added (F9); plus the Q5 salvage list, the `make audit-head` target in place of a daemon, the `regime.yml` discipline and the hash note.
   224	
   225	Round 2 (`…-design-review-round2.md`, 21:29Z, verdict `revise`): every round-1 correction confirmed applied; INV-2, INV-3, INV-6 rejected for contradictions v2 introduced, plus routing, cap and premise notes. v3 adopts all of them: `implementing_tasks` is a map of task id to invariant ids inside the hashed keys and the design-on-main precondition is stated (INV-2); `revise.yaml` is a sibling of the byte-identical task.md (INV-3, INV-8, INV-12, V3c, V2b); the question threshold is 2 and audit JSONs count only when their sha256 matches their record (INV-6); V3a is an operator PR with all hook counting, V3b has no hook source, V3c no gate source; the legacy list is excluded from the line cap as data; the `workflow_dispatch` premise is added; the stage-3 sentence names the orchestrator's `make audit-head`; INV-1 names the latest TASK's token and the recommit after each amendment. Round 3 (`…-design-review-round3.md`, 21:33Z, verdict `accept`) confirmed the five edits; its two notes are carried in the acceptance record. v4 (operator direction 2026-10-11, relayed by the review seat's PONG at 22:01Z) splits V1 by responsibility into V1 (validation only) and V1c (the CI check), adds `dotfiles-T128-v1c-regime-ci-check-a01: [INV-1]` to `implementing_tasks` (a hashed key, hence this round), reorders the waves (V1, V1c, V1b, …) and aligns section 7's cap wording with INV-2. Round 4 (`…-design-review-round4.md`, 22:06Z, verdict `accept`) confirmed the split; its note (INV-1's ruleset action is V1c's acceptance record) is carried. v5 answers the Codex Bot's finding on boundary PR #316 (thread 4239305441): INV-3's `ci:<job>` form had no enforcement, so `check=` is now a test selector or a `repro:<id>` whose command and output live in revise.yaml, each with its own regime-job verification. Round 5 (`…-design-review-round5.md`, 22:12Z, verdict `accept`) confirmed it. The Codex Bot then reviewed the second boundary head (c1e2582b) and raised six P1 and four P2 findings that three same-vendor accepts had not: the auditor read the schema and AGENTS.md from the audited head (INV-5 now runs from main as the instruction root with the worktree as data), the CI job had no previous RESULT head (INV-3 now records previous_head in the ACCEPTANCE and revise.yaml, cross-checked by the host gate), ids were compared without sentences (INV-2), `allowed_files: ['*']` derived a cheap tier and a branch copy could claim a legacy id (INV-1, INV-12), and two task records pointed at an abandoned prerequisite. v6 adopts all ten and, because a cross-vendor reviewer found what a same-vendor fresh context did not, INV-7 now requires both a Claude and a Codex review of each design hash. Round 6 (`…-design-review-round6.md`, 22:28Z, verdict `revise`) accepted INV-1, 2, 3, 5, 12 and rejected INV-7: the Bot form produced no receipt, hash or RESULT, so it would have been an orchestrator-written receipt for a review it did not perform (R5). v7 makes the Codex review a `codex exec --sandbox read-only` run under a `codex-review` identity with its own receipt and RESULT, names it in the enforcement row and V4, keeps the Bot's review as swept feedback, and adds the bare-mode skills premise (round-6 INV-5 note, acted on in V2). Round 7 (Claude, 22:31Z, `accept`) confirmed INV-7. The first Codex review (`…-design-review-round7-codex.md`, `codex-review-dot-h001`, 22:34Z, `reject`) rejected INV-1, 3, 4, 5, 6, 9, 10, 12, all on one theme: evidence the orchestrator authors. v8 answers each: the waiver becomes a command under a `permissions.ask` rule (INV-1, INV-6) with the one-account residual stated in section 9; `repro:` is dropped and `check=` is a test selector only (INV-3); premises are reviewer and auditor evidence and the counting is the mechanical part (INV-4); the audit carries an input manifest and the acceptance record has an audit-input boundary (INV-5); cost records name their raw sources and stay a warning metric (INV-9); first push is the first commit's committer date and dispatchability is defined (INV-10); the independent oracle for gate-script PRs is the trusted-root audit (INV-12). The Codex P2 on the bare-mode skills premise is not adopted: the headless page says verbatim that "A directory you name with --add-dir is a partial exception: bare mode loads skills from its .claude/skills/ folder". Codex round 8 (`…-design-review-round8-codex.md`, 22:39Z, `reject`) accepted INV-1, 6, 7, 8, 9, 11 and the one-account residual, withdrew its bare-mode P2, and rejected INV-2 (tests unbounded), INV-3 (a changed file is not a run selector), INV-4 (sampling), INV-5 (the skills refusal was a premise, not a rule), INV-10 (committer date is not a push time; dependencies), INV-12 (a model audit is not a deterministic oracle), plus two stale enforcement rows. v9 adopts all: a 1000-line cap under tests/; the exact selector run on both heads in the PR's required `revise-check` job; every premise dispositioned by each reviewer and the auditor; the `.claude/**` refusal inside INV-5; the draft PR's `created_at` and an `after` list for dispatchability; a `main-tests` required job running main's tests against the PR's scripts (V5c); the two rows fixed. Claude round 8 (`…-design-review-round8.md`, 22:41Z, `revise`) rejected INV-1 (the waive script had no owner or row), INV-5 (once-per-head versus re-audit on a stale manifest) and INV-10 (fixed in v9), and offered a stronger anchor: the waiver record in a directory outside the sandbox write roots. Codex round 9 (`…-design-review-round9-codex.md`, 22:46Z, `reject`) accepted ten, rejected INV-5 (the `.claude/**` refusal that v9 claimed was silently lost by a failed edit, confirmed by grep) and INV-12 (the oracle must precede the waves), dispositioned all twelve premises (nine hold, three unverifiable in its read-only sandbox), and raised GitHub's 2026-11-02 `pull_request_target` policy. v10: the refusal is in INV-5 and verified by grep; one valid audit per head with stale-manifest replacement; the runner computes the manifest; the waiver record lives outside the sandbox write roots and V3a owns the script (map entry `[INV-6, INV-1]`); `main-tests` is wave V0 and every code wave is contract-first (INV-12, INV-2); the policy premise and residual. Claude round 9 (`…-design-review-round9.md`, 22:46Z, `revise`) found that `main-tests` as drafted would fail every intentional change and proposed running main's modules only for scripts outside `allowed_files`; Codex round 10 (`…-design-review-round10-codex.md`, 22:50Z, `reject`) accepted INV-1..11 and found that contract-first tests cannot merge ahead of an implementation that changes an existing script, proposing dormant contracts that `main-tests` activates on the implementation PR. v11's INV-12 is the union: main's modules as they are for undeclared scripts, main's dormant contracts (`REGIME_CONTRACT=1`) for declared ones, contract PRs required for design-tier waves; INV-1 states that the record's location is the guard and the ask rule the second layer (Claude round 9). Codex round 11 (`…-design-review-round11-codex.md`, 22:52Z) accepted INV-1..12 with no findings. Claude round 11 (`…-design-review-round11.md`, 22:54Z, `revise`) accepted everything but two INV-12 clauses: contracts must not stay dormant forever (the implementation PR removes the decorator; main-tests judges it against main's dormant copy) and an empty contract must fail a design-tier implementation PR. v12 adds both sentences to INV-12 and V0. Claude round 12 (`…-design-review-round12.md`, 22:57Z) accepted v12; Codex round 12 (`…-design-review-round12-codex.md`, 22:57Z, `revise`) accepted INV-1..11 and asked for a failing check behind the decorator-removal clause. v13 adds it to INV-12 (main-tests fails an implementation PR whose declared test module still carries a contract marker) and V0 carries it with the task-file reviewer's three V0 items (main's tests overlaid on a copy of the PR tree, module selection from the task's declared tests/ entries, task.md read with PyYAML). Round 13 (Claude 23:01Z, Codex 23:01Z and the premise map 23:17Z) accepted v13. Plan 006 (approved 2026-10-11) A102 amends two hashed keys: INV-12 states the in-process oracle's authenticated completion (nonce runner) and its residual, after the Codex Bot's P1 on V0's round-1 head repeated the class of the round-0 audit's finding 3; INV-2 and the map gain the .orchestration-only CI skip (`dotfiles-T128-ci-skip-orchestration-a01`, plan A201) that plan 006 orders as Phase 2. Round 14 (Codex 02:42Z `accept`; Claude 02:43Z `revise`): INV-12's residual clause understated the gap (the nonce authenticates the writer, not the counts; in-process patching of unittest's result collection forges counts with a genuine nonce) and INV-2 should cover every required check. v15 states the residual as it is, adds the runner's pinning of unittest classes, and words INV-2 for every required workflow. Round 15 asks both reviewers at once for one verdict each on this hash. Sources are the repository paths under `.orchestration/validation/dotfiles-T128-regime-v3-a01-research/` (`baseline.md`, `practice-evidence.md`, `claude-code-factsheet.md`, `codex-factsheet.md`, `github-factsheet.md`, `method-draft.md`). Receipt: `.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round15.md` (Claude) and `…-design-review-round15-codex.md` (Codex); the whole-file sha256 of this file in both headers.
   226	
   227	v18 (plan 006 B0, plan 007 T701; written by the orchestrator under the records exemption, 2026-10-12): INV-12 narrowed to the undeclared-change regression guard: `main-tests` runs main's test module of every script outside `allowed_files`; a script inside `allowed_files` is judged by the PR's tests, the diff review and the trusted-root audit; the dormant-contract clauses, `REGIME_CONTRACT` and the `<task>-contract-a01` PRs are removed (A302 withdrew V1's contract PR under the Phase A correction and no wave has used one); `main-tests` decides inside its own job as the A5 workflows do. INV-2 loses the dead `-contract-a01` comparison and names A5's in-job form. `implementing_tasks` gains the V0 successor `dotfiles-T128-v0-main-tests-a02: [INV-12]` (A301) and `dotfiles-T128-gate-evidence-a01: [INV-6]` (plan 007 T702: the gate's `evidence=` grammar and the S6 refusal at INV-6's mandatory point). The INV-12 enforcement row, the V0 wave row and the wave order follow. Round 20 asks both reviewers at once for one verdict each on this hash: receipts `.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round20.md` (Claude) and `…-design-review-round20-codex.md` (Codex); the whole-file sha256 of this file in both headers.
   228	
   229	v19 (round 20's one revision, 11:43Z): INV-6 gains the clause the Claude round-20 receipt asked for (the Codex round-20 receipt accepted v18 with no rejection), so `dotfiles-T128-gate-evidence-a01: [INV-6]` maps to a sentence that states the two refusals; nothing else changes. Round 21 asks both reviewers at once for one verdict each on this hash: receipts `…-design-review-round21.md` (Claude) and `…-design-review-round21-codex.md` (Codex).
   230	
   231	v20 (11:46Z): the Codex round-21 receipt found the v19 clause appended to INV-4 (a stale line number after v18's two map insertions), so v20 moves that exact clause to the end of INV-6; INV-4 returns to its v18 text; nothing else changes. Round 22 asks both reviewers at once for one verdict each on this hash (round 21 was never sent to the Claude seat): receipts `…-design-review-round22.md` (Claude) and `…-design-review-round22-codex.md` (Codex).
   232	
   233	Round 22 (Claude 11:49:16Z `accept`, receipt `…-design-review-round22.md`; Codex 11:49:21Z `accept`, `…-design-review-round22-codex.md`) accepted v20 at `ed51f1d4…`; the unhashed `design_review.receipt` line now names the round-22 receipt (this edit), confirmed by a Codex pointer-only read as round 23.
   234	
   235	v21 (13:08Z, the orchestrator under the records exemption): `implementing_tasks` gains `dotfiles-T128-gate-evidence-a02: [INV-6]`, the INV-6 successor of `dotfiles-T128-gate-evidence-a01` (withdrawn 13:02Z under INV-6 before its second amendment; reset record `dotfiles-T128-gate-evidence-a01-design-reset.md`), beside the a01 entry that stays as parked history, as the V0 and round-18 successors did; nothing else changes. Round 24 asks both reviewers at once for one verdict each on this hash: receipts `…-design-review-round24.md` (Claude) and `…-design-review-round24-codex.md` (Codex).
   236	
   237	v22 (15:28Z, the orchestrator under the records exemption): `implementing_tasks` gains `dotfiles-T128-gate-evidence-a03: [INV-6]`, the INV-6 successor of a02 (withdrawn 15:25Z after its second S1 cycle; plan 011 option F: the acceptance record's machine-read parts as YAML front matter), beside the a01 and a02 entries kept as parked history; nothing else changes. Round 25 asks both reviewers at once for one verdict each on this hash: receipts `…-design-review-round25.md` (Claude) and `…-design-review-round25-codex.md` (Codex).
   238	
   239	v23 (2026-10-13 02:55Z, the orchestrator under the records exemption): `implementing_tasks` gains `dotfiles-T128-gate-evidence-a04: [INV-6]`, the INV-6 successor of a03 (withdrawn 02:3xZ after the fourth binding row; plan 014 option A: the acceptance record's `ledger` must cover every swept Codex finding id and every audit finding `audit:<sha7>:<n>`, a set difference the gate computes; the a04 file's hash is in the reset record `dotfiles-T128-gate-evidence-a03-design-reset.md`, not here), beside the a01 to a03 entries kept as parked history; nothing else changes. Round 26 asks both reviewers at once for one verdict each on this hash: receipts `…-design-review-round26.md` (Claude) and `…-design-review-round26-codex.md` (Codex).
   240	
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

**Managing output token limits**
exec
/bin/zsh -lc "rg -n 'INV-|invariant|S[1-6]|threat|audit|invariants' .orchestration/tasks/dotfiles-T128-regime-v3-a01.md .orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a03.md; sed -n '120,165p' .orchestration/acceptance/dotfiles-T128-orchestrator-tools-followup-a03.md; cat .ua/meta.json; rg -n 'Orchestrator Playbook|task-level audit|"'^10'"\\.|"'^##|threat_table'"' ~/.agents/skills/agmsg-orchestration/SKILL.md" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 16ms:
.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a03.md:14:threat_table:
.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a03.md:22:    disposition: "residual: the fakes record and answer, nothing else; the audit reads each case against items 1 and 2"
.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a03.md:28:    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a03.md:29:  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a03.md:34:    disposition: "residual: no new or renamed script; any new or renamed script is an undeclared change the audit fails"
.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a03.md:36:    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a03.md:38:    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a03.md:98:The Codex half's round 9 (on `2785ac02`): P2 the pre-send window file under `$TMPDIR` had no collision-safe creation, no cleanup and no control row; it is now a private `mktemp` file (mode 0600) removed by an EXIT trap on every exit path, with its own threat row and a cleanup assertion in the test.
.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a03.md:123:`uv run python -m unittest tests/unit/test_orchestrator_tools.py -v` green (the 52 tests and the two new ones), pasted in the validation file with `shellcheck scripts/orchestrator/dispatch.sh` and `git diff --numstat origin/main...HEAD`: at most 200 changed lines (added plus deleted) outside `tests/` and outside `.orchestration/` (plan 021 step 7.2) and 1000 added lines under `tests/` (INV-2).
.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a03.md:127:One PR from a fresh branch off `origin/main` (after 8b25f9ca; the tools a02 PR #368 is merged). The PR is ready for the orchestrator's integration when the ruleset's required checks are green, the Bot's review of the final head is in (at PR open, and once more on `@codex review` after a P0/P1 fix round: plan 020 step 2), every Bot thread is replied to and resolved by the orchestrator with its disposition, the validation file carries the Check's outputs, and the RESULT names every P0/P1 thread with `fixed:<sha>` and every P2 thread with the disposition the worker proposes; the orchestrator's audit of the final head is dispositioned finding by finding before the gate, and a P0/P1 it leaves is the operator's decision. The Bot's P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P0 or P1 that survives the round is listed as `open:<thread id>` with `bot_rounds=2` (the Bot's review at PR open and its re-review after the fix round), stops the PR and goes to the operator as a decision; a P2 on this PR's own change whose fix stays within `allowed_files` and is small (one flag or a few lines plus one test) is fixed in a revise round the orchestrator sends with a `check=` while INV-6's counts allow it (C-50); any other P2 is advisory, owned by `dotfiles-T128-orchestrator-tools-followup-a04`, which the orchestrator writes when the first advisory P2 appears, before the PR's dispositions (C-51), and recorded under `## Owned by dotfiles-T128-orchestrator-tools-followup-a04` in this task's acceptance record. The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`. The RESULT names head, base, branch, files, every Bot thread with its disposition, the test names, the caps, `task_copy=<sha256 of .orchestration/dotfiles-T128-orchestrator-tools-followup-a03/task.md>` and the evidence paths.
.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a03.md:133:## Change (threat row, 2026-10-16T22:07:03Z, after the RESULT)
.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a03.md:135:The Codex Bot's P1 4299651928 on PR #374's head 57d3577c: uv run from the caller's cwd executes a caller-controlled `.python-version` or venv interpreter even with `--no-project`, which the environment threat row's claim that the cwd chooses nothing did not cover. Operator decision D-P1-374 A: the fix round runs uv from the trusted script root; the row now says so. The dispatched hash `b291ba85` stands (the branch's task copy is byte-identical to it by design); this row is the orchestrator's record, carried by the next boundary.
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:10:  dotfiles-T128-v0-main-tests-a01: [INV-12]
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:11:  dotfiles-T128-v1-task-schema-a01: [INV-1]
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:12:  dotfiles-T128-v1c-regime-ci-check-a01: [INV-1]
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:13:  dotfiles-T128-v1b-pr-caps-a01: [INV-2]
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:14:  dotfiles-T128-ci-skip-orchestration-a01: [INV-2]
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:15:  dotfiles-T128-ci-skip-orchestration-a02: [INV-2]
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:16:  dotfiles-T128-v2-audit-schema-and-runner-a01: [INV-5]
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:17:  dotfiles-T128-v2b-audit-gate-a01: [INV-5]
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:18:  dotfiles-T128-regime-counters-a01: [INV-6]
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:19:  dotfiles-T128-regime-counters-a02: [INV-6]
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:20:  dotfiles-T128-v3a-reset-counters-a01: [INV-6, INV-1]
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:21:  dotfiles-T128-v3b-premises-and-amendments-a01: [INV-4]
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:22:  dotfiles-T128-v3c-one-fact-per-round-a01: [INV-3]
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:23:  dotfiles-T128-v3d-idle-and-first-push-a01: [INV-10]
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:24:  dotfiles-T128-v4-design-review-runner-a01: [INV-7]
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:25:  dotfiles-T128-v5a-evidence-on-branch-a01: [INV-8]
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:26:  dotfiles-T128-v5b-cost-fields-a01: [INV-9]
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:27:  dotfiles-T128-v6-permgate-session-a01: [INV-11]
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:28:  dotfiles-T128-v0-main-tests-a02: [INV-12]
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:29:  dotfiles-T128-gate-evidence-a01: [INV-6]
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:30:  dotfiles-T128-gate-evidence-a02: [INV-6]
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:31:  dotfiles-T128-gate-evidence-a03: [INV-6]
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:32:  dotfiles-T128-gate-evidence-a04: [INV-6]
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:38:  - dotfiles-T124-wave3b-audit-grammar-a01
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:39:threat_model:
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:40:  R1: rounds are judged by models re-reading models and add no deterministic fact, so a wrong premise is patched round after round (T118 20 revises, T119 5 revises and 4 audits; the vendor's own rule is two corrections, then start fresh)
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:44:  R5: the orchestrator's artifacts are unaudited and it dispositions findings about itself (T119 audit-finding 2); the reset rule was prose the orchestrator could waive (PR 313 revise round 2)
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:45:  R6: "the auditor becomes a serial queue when audits run once per round in one tab (measured: 4 audits about 1.3 h of T119's 11.1 h; the rounds, not the audits, were the cost)"
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:50:  - JSON Schema documents validated by the jsonschema library (PyYAML for front matter) for task files, audit verdicts, design-review receipts and evidence; model verdicts produced under schema (codex exec --output-schema, server-side strict; claude -p --json-schema)
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:54:invariants:
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:55:  INV-1: "every task is a format-2 file whose front matter validates against schemas/task.json (jsonschema + PyYAML, no hand-written parser; every allowed_files entry starts with a literal path segment and a wildcard entry derives the tier of every design-tier path its literal prefix can cover); legacy task ids are grandfathered only for files under .orchestration/tasks/ on main, never for a branch copy; the tier (docs, review, design) is derived from allowed_files by the shared high-risk module, with the regime's own rule prose (home/dot_config/claude/rules/**, the agmsg-orchestration SKILL, AGENTS.md, README) listed in the review tier, and selects the pipeline from process_tiers in agent-config.yaml; every AGMSG-TASK for the task, the first and each amendment, carries task_sha256= of the task file as sent, the worker commits the file byte-identical to .orchestration/<task id>/task.md (first commit, recommitted after each amendment), the CI regime job validates that copy with main's schema and refuses a PR that changes .github/workflows/** unless its task.md is design tier and lists the file, the host gate compares the copy's sha256 with the latest AGMSG-TASK's token in history, and the regime check binds only once the ruleset lists it as required (an operator action named in V1's acceptance record); the orchestrator can add or skip a stage only with an operator waiver written by scripts/regime-waive.sh, a command under a permissions.ask rule in the managed settings with no permgate policy entry, so that only the human's answer to the native prompt runs it (an ask rule prompts even in auto mode; agent-to-agent approval is forbidden); the waiver names the task, the stage and a reason and is written under $XDG_STATE_HOME/regime/waivers/, a directory outside every seat's sandbox write roots, so no sandboxed seat can write it and only a command run outside the sandbox on the human's answer to the native prompt can (the directory is the guard; the ask rule on the named command is the second layer, since a reworded command would still meet the prompt at the sandbox boundary); it is listed by check-regime-boundary.sh and the boundary PR body (V3a owns the script and its ask rule), and is the strongest friction available on a machine where every seat and GitHub action is the operator's own account (operator authentication is a stated residual, not a claim)"
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:56:  INV-2: "a PR is mergeable only within the caps the CI regime job enforces from main's workflow (at most 15 changed files outside .orchestration/, 500 added lines outside tests/, .orchestration/ and the data list scripts/legacy-task-ids.txt, and 1000 added lines under tests/), and its task.md invariants equal the design's as a set of ids and byte-for-byte as sentences (the design read from main, never from the PR); the design file must be on main (through a boundary PR) before the implementing TASK is dispatched and the regime job fails closed when the design named by task.md is absent from main; an .orchestration-only PR runs no bootstrap or test matrix and every required check context still reports success (each required workflow decides inside each of its jobs, as test.yaml and remote.yaml do since A5: no job-level if and no needs, because a skipped required job reports success), so a boundary PR merges in minutes; exceeding a cap is a split, never a finding to disposition (the cap changes the unit of work: T116 +529 and T118 +881 would have been split)"
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:57:  INV-3: "a revise round is admissible only when it adds a new deterministic check: the AGMSG-ACCEPTANCE status=revise carries check=tests/<file>::<name> and previous_head=<the RESULT head being revised>, the worker records both in .orchestration/<task id>/revise.yaml (a sibling file; task.md stays byte-identical to the dispatched file), the main-pinned regime job verifies that the named test file exists on the head and differs between previous_head and the head, the PR's own unit-test workflow (a required check, run in the PR's context) collects and runs exactly that selector on the head (it must pass) and on previous_head (it must fail or be absent), and the host gate, which reads history, verifies that previous_head equals the head of the previous AGMSG-RESULT for the task and requires the same selector in the validation file; a finding that cannot become a test is dispositioned, never iterated"
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:58:  INV-4: "a task file carries premises, each with the command and pasted output that verified it before dispatch; premises are evidence for the design reviewers and the auditor, each of whom dispositions every premise in the receipt or audit JSON as holds, fails or unverifiable (a local command re-run, an external claim re-fetched; a fails is a specification finding and a rejection), a complete disposition the schema requires rather than a sample, and the mechanical part of this invariant is the counting: a worker question (AGMSG-PONG status=question) is a specification defect answered by at most one further AGMSG-TASK, amendments are every AGMSG-TASK for the task_id after the first, whatever its wording, and the second amendment or the second question is INV-6's count, which withdraws the task to design through INV-6's merge backstop and Stop signal"
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:59:  INV-5: "the task-level audit is a headless read-only run whose instruction root is the trusted main checkout and whose schema is main's schemas/audit.json: codex exec --output-schema <main>/schemas/audit.json -C <main> with the detached worktree at the head added as a read-only data directory (--add-dir), so the audited PR controls neither the schema nor the AGENTS.md the auditor reads; the fallback claude -p --json-schema from the same root with --add-dir <worktree>, --bare when an API key is set and otherwise with project and user hooks disabled, and refused with exit 2 blocked when the head changes any file under .claude/ (bare mode loads skills from an --add-dir directory's .claude/skills/), leaving such a head to the codex path), with at most one valid audit per head (a stale input manifest invalidates an audit and a new audit of the same head replaces it), pooled two at a time; the gate accepts an audit of an earlier head only when git diff --quiet <audited head> <HEAD> -- . ':!.orchestration' holds (an evidence-only revision), otherwise a new audit is required; its input includes the task's invariants and premises, the worker's evidence, the orchestrator's task file and amendments, the acceptance record as it stands when present (its text above the line <!-- audit-input-boundary --> is the pre-audit part; dispositions of this audit's findings are appended below it), the head's pr-feedback JSON and the previous round's audit JSON; the audit JSON carries an input manifest (path to sha256 of every input as read, computed by the runner, which overwrites any model-supplied value) and the gate recomputes the manifest at gate time, so a pre-audit input edited after the audit makes the audit stale and a new audit is required; the schema lists findings {priority, confidence, category in {specification, implementation, evidence, orchestration, conformance}, path, line, rationale} and the per-invariant map before the verdict, and the prompt asks for the rationale before each verdict; the runner, under the identity claude-audit-dot-h001 or codex-audit-dot-h001 on the orchestrator's host, records the JSON's sha256 in agmsg history (AGMSG-AUDIT v1 task_id= head= sha256= auditor=) before the gate reads it, an anchor that prevents edits after the record and not fabrication before it; the gate reads the verdict and categories from the JSON, and orchestration and conformance findings at P0-P2 accept only an operator waiver or a design reset, never not-applicable"
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:60:  INV-6: "the reset rule's mandatory point is the merge backstop in scripts/require-crit-review.py, with the orchestrator's Stop hook (Claude Stop hook, Codex [hooks].Stop) as the early signal, soft on both runtimes by their documented caps; counts come from history for the hook and the gate (revises = RESULTs for the task_id minus one, threshold 2; amendments = AGMSG-TASKs after the first, threshold 2; AGMSG-PONG status=question, threshold 2) and from GitHub and main-checkout files for the gate and the boundary check only (Codex Bot P0 or P1 on two heads after the first RESULT, from original_commit_id on review_comment items recorded by pr-feedback.py; an audit implementation or specification finding at P0-P1 on two heads, from .orchestration/validation/<task>-audit-<sha7>.json in the main checkout, each counted only when its sha256 matches its AGMSG-AUDIT record); when a count is reached the gate refuses the merge until a reset record names a redesign task whose design RESULT comes from an identity other than the task's author, or a waiver written by scripts/regime-waive.sh under the INV-1 ask-rule discipline into the state directory outside the sandbox write roots (the only release path besides a redesign; the one-account residual of INV-1 applies); check-regime-boundary.sh reports a closed-unmerged PR whose task has no reset record and a task over any count with neither an accepted acceptance record nor a reset record; the same gate refuses a merge whose acceptance record carries a not-applicable disposition without an evidence= clause, or a finding-class table with three rows of one class and no pasted search of the correction records (plan 007 S6)"
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:61:  INV-7: "the design tier adds, before any code is dispatched, two design reviews of the same design hash: a fresh Claude context on the review profile (a headless run or a seated -review- identity; the review profile is the same model and effort as deep, so the lever is the separate context) and a Codex read-only review (codex exec --sandbox read-only on the review profile under a codex-review identity: headless through V4's runner, or seated until V4); each receipt is a schema document naming the design file's canonical hash over invariants, threat_model, trust_anchors, implementing_tasks and premises, each is announced by an AGMSG-RESULT from its reviewing identity, and both RESULTs precede the implementing AGMSG-TASK in history; the Codex Bot's review of a boundary PR is swept feedback, never a design receipt; a change to the hashed keys needs new reviews; the gate accepts the whole-file sha256 form for receipts written before V4 lands"
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:62:  INV-8: "worker evidence (the task.md copy, revise.yaml, report, validation, sandbox, learning, autoskill, worker review JSON) is committed on the PR branch under .orchestration/<task id>/ before the final RESULT so the Bot, CI and the gate read the same files from the audited head; the orchestrator's records (audit JSON, acceptance, pr-feedback) stay under .orchestration/validation and .orchestration/acceptance in the boundary commit because the merge is --match-head-commit"
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:63:  INV-9: "every acceptance record carries measured cost (rounds, amendments, questions, wall time TASK to final RESULT from history timestamps, audit count, Bot threads, tokens: total_cost_usd from claude -p JSON, turn.completed.usage from codex exec --json, per-message usage from the seat's session transcript) written by accept-task.py, which also records the path and sha256 of every raw source it read (the headless runs' JSON, the transcript files at acceptance time) so a total can be recomputed; cost is a warning metric, never a gate: each tier has a budget, the acceptance record names the operator decision when it is exceeded, and check-regime-boundary.sh warns; headless runs carry --max-budget-usd"
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:64:  INV-10: "at most three concurrent workers with pairwise-disjoint allowed_files; the first push is the draft PR's server-side created_at (gh api pulls/<n>), which must fall within 30 minutes of the TASK's history timestamp, and a seated worker is not idle for 20 minutes while a dispatchable task exists, a dispatchable task being a format-2 file under .orchestration/tasks/ with no AGMSG-TASK for its id in history, no superseded_by or reset record, and every task id in its after list accepted (an acceptance record with Decision accepted in the main checkout); both computed in check-regime-boundary.sh and accept-task.py, never in the Stop hook; headless reviews and audits do not count as workers"
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:65:  INV-11: permgate records session_id and cwd per decision, and the gate compares a Claude worker's permission-gated Bash count in the task window with the sandbox record (an understated record is refused); Codex workers cannot escalate and are not covered
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:66:  INV-12: "every rule above is exercised by a unit test that fails when the rule is removed; the PR's own workflow runs the PR's tests, and a required check main-tests (wave V0, before every other wave) fetches main's tests/unit and runs, in the PR's context, main's test module of every script outside the task.md's allowed_files as it is, so an undeclared change to any script fails (the undeclared-change regression guard); a script inside allowed_files is judged by the PR's own tests, the orchestrator's diff review and the trusted-root audit (INV-5), which reads the test diff beside the code diff and reports a deleted or weakened fails-when-removed test as a conformance finding; main-tests decides inside its own job, as the A5 workflows do, with no changes job and no needs, so an .orchestration-only PR reports success from the job itself; main-tests is an in-process oracle: code that main's tests import from the PR runs inside the test process, so the harness authenticates that main's runner reached its end with a per-run nonce that only the runner sees (read from a pipe and closed before any test loads, written back with the counts), and the runner pins unittest's result and runner classes before importing any test; the nonce authenticates the writer, not the counts: adversarial PR code running in the same process can still patch result collection or read the nonce from a frame, so in-process forgery remains a stated residual that the trusted-root audit catches, named in every acceptance record of a design-tier PR; including one test per gaming path (a schema-valid task with a prose cap bypass, a revise without a named check, a revise list appended to the hashed task.md, an AGMSG-TASK without amendment= that still counts, an evidence-only relabel of a code change caught by the tree-equality check, a wave-table rewrite after review, an audit JSON edited after its history record, a receipt whose hash predates a key change, a reset record naming the author's own identity, a Bot-skipped head whose audit never starts, a single PR split only in the task file, a branch task.md claiming a legacy id, allowed_files of ['*'] or a wildcard first segment, an invariant sentence weakened under its id, a schema or AGENTS.md edited on the audited head, an undeclared script change that main-tests must fail); legacy task ids are grandfathered by the checked-in list scripts/legacy-task-ids.txt, which only shrinks and is excluded from the line cap as data"
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:83:  - claim: the audit was not the wall-clock bottleneck
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:84:    command: "stat .orchestration/validation/dotfiles-T119-*-audit-*.md; history.sh dotfiles-conformance (TASK 2026-10-09T21:26Z to ACCEPTANCE 2026-10-10T08:32Z)"
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:85:    output: "four audit files written 11:48, 13:55, 15:52, 17:23 local, each run 15-25 minutes, about 1.3 h of an 11.1 h task"
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:112:Drafted 2026-10-11 (local) by the orchestrator seat `claude-deep-dot` under a recorded bootstrap exception (operator decision 2026-10-11: the orchestrator drafts, a fresh context on the review profile must accept before any implementing task is dispatched). Operator direction (pasted 2026-10-11): when substantive findings repeat, the design, implementation or verification is wrong and a mechanism must force the redo; prose alone repeats the mistake; the auditor must be able to find the orchestrator's and the worker's mistakes; efficiency, quality and cost are optimised together; the auditor must not become the bottleneck and the audit stages must be chosen; all of it grounded in the tools' official documentation and current practice. Research inputs: fact sheets on Claude Code 2.1.293, Codex CLI 0.161.0, GitHub rulesets and Actions, and the research literature, read 2026-10-11; the measured baseline below.
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:116:By T126 INV-6 as written: wave 1 (PR #313) 8 amendments (limit 4) and 2 revises (limit 2); wave 3b (PR #314) Bot P1 on two post-RESULT heads. The orchestrator was drafting a waiver for #313. T120 was reset only on the operator's question. The regime is therefore reset here by its own rule; this document is the redesign, and T126 and T124 are superseded (their accepted ideas are kept where named).
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:120:| task | PR | files | +lines | amendments | questions | revises | audits (incorrect) | Bot threads (heads) | P0/P1 | wall |
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:137:- **P1 One deterministic fact per round (INV-3).** Reuses tests/unit, CI, `pr-feedback.py`. Deletes free-form revise rounds and the audit-per-round habit.
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:138:- **P2 Declarative over imperative at trust boundaries (INV-1, INV-5, INV-7).** Reuses `jsonschema`, PyYAML, `codex exec --output-schema`, `claude -p --json-schema`. Deletes the bespoke YAML parser, the glob NFA, the prose verdict grammar, regex parsing of `.last.md`, and the T126 "process_tiers.json next to the module" indirection (the validator reads the manifest with PyYAML).
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:139:- **P3 Small one-invariant PRs enforced in CI (INV-2).** Reuses GitHub required checks and the strict up-to-date ruleset already in force. Deletes waves declared inside a task file.
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:140:- **P4 Main-pinned mechanical checks in CI; host gate only for history-anchored rules (INV-1, INV-2, INV-8 in CI; INV-3, INV-5 record, INV-6, INV-7 anchor, INV-11 on the host).** Reuses `pull_request_target`, the `changes` job pattern that reports success for an `.orchestration`-only diff. Deletes PR #313's `REVIEW_TREE` idea (never on `main`) and the copy step of untracked evidence into the gate's cwd. The host gate `make require-crit-review` keeps its evidence rules and changes three of them in named waves: the audit verdict and categories come from the schema JSON with the `AGMSG-AUDIT` record and the category lock (V2b), the reset backstop and the Bot-head count (V3a), the history-anchored design review (V4); it continues to run from the orchestrator's main checkout.
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:141:- **P5 Research before dispatch; a question ends the task, not amends it (INV-4).** Reuses history (`amendment=`, `status=question`). Deletes the amendment-per-question practice. The task file's `premises` block is the mechanical residue of "verify every CLI constraint by running the real command".
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:142:- **P6 Reset is mechanical, loop-time, and released only by another context or the operator (INV-6).** Reuses `scripts/require-crit-review.py` as the mandatory point, `agent-stop-gate.sh` and the Codex `[hooks].Stop` as the early signal (both soft by their documented caps: Claude's 8-continuation cap, Codex's continuation prompt), `check-regime-boundary.sh` for the re-dispatch detector. Deletes the orchestrator-written redesign (the redesign author is a `review`-profile seat or a fresh headless context; the `redesign` profile of T124 v4 is dropped: `review` is the same model and effort as `deep`, so independence of context is the whole lever, and T124 round 1 showed it works).
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:143:- **P7 Audit staging by tier; the auditor never serializes the pipeline (INV-5, process_tiers).** See section 4.
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:144:- **P8 Cost measured, budgets per tier (INV-9).** Reuses the JSON cost fields the runtimes already emit and the session transcripts. Deletes `cost: n/a`.
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:145:- **P9 Parallelism with disjoint files and early push (INV-10).** Reuses `herdr-agents --add-worker`, draft PRs.
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:152:| 0 design review | a fresh Claude context on the review profile and a Codex read-only review of the same hash, schema receipts (INV-7) | before any code | - | - | required | minutes |
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:153:| 1 worker checks | worker in its sandbox: invariant tests first, shellcheck, unit tests | before every push | required | required | required | none for the regime |
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:155:| 3 schema audit | headless read-only `codex exec --output-schema`, pooled 2, started by `make audit-head` once CI is green and the Bot reviewed or 15 min passed, once per RESULT head, reused for an evidence-only head by tree equality (INV-5) | per RESULT head | - | required | required, with invariant map and permgate window | the scarce resource, now off the critical path |
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:158:Tier derivation: docs = prose-only `allowed_files` outside the regime's own rule prose (`home/dot_config/claude/rules/**`, the agmsg-orchestration SKILL, `AGENTS.md`, README), which is review tier by explicit list; review = the existing review-tier paths (scripts, hooks, tests, templates); design = the explicit design-tier list from T124 INV-2 v3 (install/**, setup.sh, the gate scripts, `executable_herdr-agents`, `executable_permgate`, Codex and Claude policy, sandbox and permission settings, credential helpers). Round limits: docs 1 revise; review and design 2 revises then reset. Profiles: worker `standard` (docs `express`), review `review`, audit `audit`.
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:160:Why stage 3 is not the queue: the orchestrator starts it with `make audit-head` when the RESULT arrives (the wait on CI and the Bot is inside the target), it runs concurrently (pool of two, each in its own detached worktree), once per head, and an evidence-only head reuses the earlier audit by tree equality; the measured cost of the old serial form was 1.3 h of 11.1 h, so the throughput levers are P1 and P6, and the pool removes the residual queue.
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:164:| invariant | enforcement point |
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:166:| INV-1 | `.github/workflows/regime.yml` (`pull_request_target`, required check `regime`: validates `.orchestration/<task id>/task.md` from the PR head read as data, refuses workflow edits outside a design-tier task; an explicit Actions event policy allowing `pull_request_target` is set by the operator before 2026-11-02, named in V1c's acceptance record), `scripts/validate-task.py` (schema + PyYAML, about 80 lines), `schemas/task.json`, `scripts/lib/high_risk_paths.py` (new module: tier lists and `tier_of`), `scripts/legacy-task-ids.txt` (grandfather list), `process_tiers` in the manifest; host gate compares the copy's sha256 with `task_sha256=` in history (V3a); stage waivers by `scripts/regime-waive.sh` under its `permissions.ask` rule, written outside the sandbox write roots (V3a) |
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:167:| INV-2 | `regime.yml` step with `scripts/pr-caps.sh` and the task.md invariant-id comparison against the design's `implementing_tasks` |
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:168:| INV-3 | `regime-check.sh` step: the test selector named in `.orchestration/<task id>/revise.yaml` (sibling of the byte-identical task.md) exists on the head and its file differs between `previous_head` and the head; a `revise-check` job in `test.yaml` (PR context, required) runs exactly that selector on both heads; the host gate's `previous_head` history check and validation-file line are V2b's |
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:169:| INV-4 | `scripts/validate-task.py` (premises required for code and design tasks); `agent-stop-gate.sh` early signal on the second AGMSG-TASK or second PONG question; the merge backstop is INV-6's |
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:170:| INV-5 | `schemas/audit.json` (findings and invariant map before verdict), `scripts/audit-head.sh` (about 100 lines: detached worktree, `codex exec`, fallback, sha256 to history under the audit identity, `.last.md` render; PR #314's hardening kept), `make audit-head` target around `gh pr checks --watch` and the SKILL's Bot list loop with its 15-minute `bot: none` rule (no daemon), `AGENTS.md` Audit section; gate: JSON verdict and categories, `AGMSG-AUDIT` lookup, category lock, tree-equality acceptance of an earlier head (V2b) |
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:171:| INV-6 | `scripts/require-crit-review.py` (mandatory: history counts, Bot heads from `original_commit_id` recorded by `scripts/pr-feedback.py`, audit heads from the main checkout's audit JSONs whose sha256 matches their `AGMSG-AUDIT` record, reset record or a `scripts/regime-waive.sh` waiver), `scripts/agent-stop-gate.sh` and the manifest's `codex.hooks` Stop entry (early signal, history counts only, within the 3 s history budget), `scripts/check-regime-boundary.sh` (closed-unmerged PR without a reset record; over-count task without an accepted or reset record; waiver listing) |
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:172:| INV-7 | `scripts/design-review.sh` + `schemas/design-review.json`: two headless runs per design hash, `claude -p` under `claude-review-dot-hNNN` and `codex exec --sandbox read-only` under `codex-review-dot-hNNN`, each joining for the run and sending its RESULT; gate: both RESULTs precede the implementing TASK, both hashes recomputed, whole-file form accepted for pre-V4 receipts |
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:173:| INV-8 | worker writes under `.orchestration/<task id>/` on the branch (task.md copy first); `regime.yml` validates the evidence JSON shapes; the gate's existing path rules keep the orchestrator's records under `validation/` and `acceptance/` |
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:174:| INV-9 | `scripts/accept-task.py` (sweep, dispositions scaffold, record rows, gate invocation, merge command, cost fields), budgets in `process_tiers`, `check-regime-boundary.sh` warning |
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:175:| INV-10 | `scripts/check-regime-boundary.sh` and `scripts/accept-task.py` from `history.sh` timestamps (storage facade or `--limit`, never the 20-row default), the draft PR's `created_at` from `gh api pulls/<n>`, and the task's `after` list against acceptance records |
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:176:| INV-11 | `executable_permgate` (operator-routed, Codex security review) + gate cross-check |
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:177:| INV-12 | one test module per script; `make unit-test` in CI; the `main-tests` required job (V0): main's test modules for every script outside the PR's `allowed_files`, deciding inside its own job; the trusted-root audit reads the test diff beside the code diff for scripts inside it; the auditor checks per PR that no new hand-written parser sits at a trust boundary (a `conformance` finding) |
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:180:## 6. Waves (one PR, one invariant, within INV-2's caps; each task file reviewed by a fresh context before dispatch)
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:182:- **V0** INV-12: the `main-tests` required job in `test.yaml` (main's `tests/unit` modules of every script outside the PR's `allowed_files`, run in the PR's context, deciding inside the job as the A5 workflows do) and the protocol in the Worker Playbook; lands before every other wave as `dotfiles-T128-v0-main-tests-a02` (A301; PR #317 and the audit of `adcf783b` are its input). Claude seat; design tier (workflow); the operator lists the check at its acceptance.
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:183:- **V1** INV-1, validation only (operator direction 2026-10-11, relayed through the review seat; also the cap: the undivided V1 sat at 500 added lines): `schemas/task.json`, `scripts/validate-task.py`, `scripts/lib/high_risk_paths.py`, `scripts/legacy-task-ids.txt` (from PR #313; data, excluded from the line cap), `tests/unit/test_validate_task.py`. Claude seat. Design tier: this review is its stage 0. Precondition: this design is on `main` through a boundary PR before V1's TASK is dispatched.
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:184:- **V1c** INV-1, the CI check (after V1): `scripts/regime-check.sh`, `.github/workflows/regime.yml` (task.md validation, workflow-edit refusal, `workflow_dispatch` dry run), `tests/unit/test_regime_check.py`, `process_tiers` in the manifest, SKILL step 3 paragraph, README sentence. Claude seat. Acceptance names the operator action that lists `regime` as a required check, after the dry run from `main` against a closed PR. Two tasks map to INV-1 as V2 and V2b map to INV-5.
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:185:- **V1b** INV-2 (after V1c): `scripts/pr-caps.sh`, the caps and invariant-id steps in `regime-check.sh`, tests, one SKILL sentence.
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:186:- **V2** INV-5 runner: `schemas/audit.json` (PR #314's, reordered), `scripts/audit-head.sh` with PR #314's hardening, `make audit-head`, `AGENTS.md` Audit section, tests, the SKILL's task-level audit bullet. Claude seat.
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:187:- **V2b** INV-5 gate: `scripts/require-crit-review.py` reads the JSON verdict and categories, requires the `AGMSG-AUDIT` record, locks orchestration and conformance at P0-P2 to waiver or reset, accepts an earlier audited head by tree equality, and requires the INV-3 `check=` line in the validation file; tests. Operator-routed gate source (delegable to a Claude seat with recorded opt-in).
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:188:- **A3** INV-6 (plan 006 Phase A, `dotfiles-T128-regime-counters-a01`): `scripts/regime-counters.sh` computes every INV-6 count from history and GitHub and prints the thresholds reached; `check-regime-boundary.sh` reports a reached threshold without a reset record or waiver; the orchestrator runs it before every acceptance action. V3a wires that script into the hook and the gate.
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:189:- **V3a** INV-6: `scripts/pr-feedback.py` (`original_commit_id` on review_comment items), `require-crit-review.py` reset backstop and `task_sha256` comparison, `agent-stop-gate.sh` history counts (revises, amendments, questions) as the early signal, the Codex Stop entry in the manifest and its rendered template, `scripts/regime-waive.sh` with its `permissions.ask` rule in the manifest's Claude permissions block (no permgate policy entry), `check-regime-boundary.sh` detector and waiver listing; tests. Four boundaries in one PR (gate source, Claude hook and permission source, Codex hook source): an operator PR by construction, reviewed by a Codex `security`-profile seat before acceptance.
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:190:- **V3b** INV-4: premises in the schema and validator, SKILL text (questions end the task; one answering TASK at most). Claude seat; no hook source (the counting is V3a's).
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:191:- **V3c** INV-3: `check=` and `previous_head=` in the ACCEPTANCE contract (SKILL), `revise.yaml` beside task.md in the Worker Playbook, the `regime-check.sh` step, the `revise-check` job in `test.yaml`; tests. Claude seat (no gate source: the history check and validation-file line are V2b's).
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:192:- **V3d** INV-10: idle and first-push computations in `check-regime-boundary.sh` and `accept-task.py` (the latter lands in V5b; V3d adds them to the boundary check only). Claude seat.
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:193:- **V4** INV-7: `scripts/design-review.sh` (Claude and Codex runs under their `-review-dot-hNNN` identities), `schemas/design-review.json`, the history anchor and hash check in the gate (two RESULTs, both forms), SKILL paragraph. Operator-routed for the gate part.
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:194:- **V5a** INV-8: `.orchestration/<task id>/` paths in the Worker Playbook, task.md copy as the first commit, evidence-shape validation in `regime.yml`, boundary commit reduced to orchestrator records. Claude seat.
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:195:- **V5b** INV-9: `scripts/accept-task.py`, cost fields with source digests, budgets in `process_tiers`, `check-regime-boundary.sh` budget warning. Claude seat. Size: the sweep, scaffold and gate invocation already exist as commands; the script sequences them, about 200 lines.
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:196:- **V6** INV-11: `executable_permgate` session_id and cwd; gate cross-check. Operator-routed, Codex `security` profile review.
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:202:revise 2; amendments 2; questions 2; Bot P0/P1 heads 2 (post-RESULT); audit implementation or specification P0-P1 heads 2; PR 15 changed files (the file count excludes `.orchestration/` only) and 500 added lines outside `tests/`, `.orchestration/` and the data list `scripts/legacy-task-ids.txt`; first push 30 minutes; idle 20 minutes; workers 3; audit pool 2; audit once per head; docs tier 1 revise.
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:206:PR #313 and #314 closed unmerged as reference branches (reset records in `.orchestration/acceptance/…-design-reset.md`); PR #315 is a draft per T120's reset record; the four worker seats are removed. Salvaged: the format-2 key set, the tier table, `scripts/legacy-task-ids.txt` and the test ideas of `tests/unit/test_validate_task.py` (V1); `scripts/schemas/audit.json`, the AGENTS.md Audit text, the pre-push hardening and the `AGMSG-AUDIT` record (V2). Dropped with the `redesign` profile: PR #313's `home/dot_codex/modify_private_redesign.config.toml`. T127 (T120's redesign) follows V1 under this regime.
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:211:- `pull_request_target` runs with the base repository's token on a public repository: the `regime` job reads PR files as data with `contents: read` only, checks out `main`'s scripts, and never executes anything from the PR; a change to `.github/workflows/regime.yml` itself is a design-tier change under INV-1.
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:218:- The seven existing required checks still run on `pull_request` from the PR's own workflow files; INV-1's workflow-edit refusal in the `regime` job is what closes R8 for them.
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:223:Round 1 (`.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review.md`, `claude-review-dot-a001`, 2026-10-10T21:15Z, verdict `revise`): INV-7, INV-8, INV-11, INV-12 accepted with notes; INV-1, 2, 3, 4, 5, 6, 9, 10 rejected with corrections; findings F1-F9. v2 adopts every item: the task.md copy and `task_sha256` anchor (F1), the per-task invariant-set rule and the workflow-edit refusal (F2), the gate changes assigned to V2b/V3a/V4 with the category lock, the Bot-wait timeout and the tree-equality rule (F3), the merge backstop as the mandatory point, `original_commit_id`, the audit-JSON source, the Stop-hook budget split and the boundary detector (F4), the single amendment count over every TASK (F5), INV-9/INV-10 moved out of the Stop hook (F6), the reset records corrected to `claude-review-dot-a001` with the waiver form and the thread ids (F7), rule prose in the review tier (F8), premise 1 restated and three premises added (F9); plus the Q5 salvage list, the `make audit-head` target in place of a daemon, the `regime.yml` discipline and the hash note.
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:225:Round 2 (`…-design-review-round2.md`, 21:29Z, verdict `revise`): every round-1 correction confirmed applied; INV-2, INV-3, INV-6 rejected for contradictions v2 introduced, plus routing, cap and premise notes. v3 adopts all of them: `implementing_tasks` is a map of task id to invariant ids inside the hashed keys and the design-on-main precondition is stated (INV-2); `revise.yaml` is a sibling of the byte-identical task.md (INV-3, INV-8, INV-12, V3c, V2b); the question threshold is 2 and audit JSONs count only when their sha256 matches their record (INV-6); V3a is an operator PR with all hook counting, V3b has no hook source, V3c no gate source; the legacy list is excluded from the line cap as data; the `workflow_dispatch` premise is added; the stage-3 sentence names the orchestrator's `make audit-head`; INV-1 names the latest TASK's token and the recommit after each amendment. Round 3 (`…-design-review-round3.md`, 21:33Z, verdict `accept`) confirmed the five edits; its two notes are carried in the acceptance record. v4 (operator direction 2026-10-11, relayed by the review seat's PONG at 22:01Z) splits V1 by responsibility into V1 (validation only) and V1c (the CI check), adds `dotfiles-T128-v1c-regime-ci-check-a01: [INV-1]` to `implementing_tasks` (a hashed key, hence this round), reorders the waves (V1, V1c, V1b, …) and aligns section 7's cap wording with INV-2. Round 4 (`…-design-review-round4.md`, 22:06Z, verdict `accept`) confirmed the split; its note (INV-1's ruleset action is V1c's acceptance record) is carried. v5 answers the Codex Bot's finding on boundary PR #316 (thread 4239305441): INV-3's `ci:<job>` form had no enforcement, so `check=` is now a test selector or a `repro:<id>` whose command and output live in revise.yaml, each with its own regime-job verification. Round 5 (`…-design-review-round5.md`, 22:12Z, verdict `accept`) confirmed it. The Codex Bot then reviewed the second boundary head (c1e2582b) and raised six P1 and four P2 findings that three same-vendor accepts had not: the auditor read the schema and AGENTS.md from the audited head (INV-5 now runs from main as the instruction root with the worktree as data), the CI job had no previous RESULT head (INV-3 now records previous_head in the ACCEPTANCE and revise.yaml, cross-checked by the host gate), ids were compared without sentences (INV-2), `allowed_files: ['*']` derived a cheap tier and a branch copy could claim a legacy id (INV-1, INV-12), and two task records pointed at an abandoned prerequisite. v6 adopts all ten and, because a cross-vendor reviewer found what a same-vendor fresh context did not, INV-7 now requires both a Claude and a Codex review of each design hash. Round 6 (`…-design-review-round6.md`, 22:28Z, verdict `revise`) accepted INV-1, 2, 3, 5, 12 and rejected INV-7: the Bot form produced no receipt, hash or RESULT, so it would have been an orchestrator-written receipt for a review it did not perform (R5). v7 makes the Codex review a `codex exec --sandbox read-only` run under a `codex-review` identity with its own receipt and RESULT, names it in the enforcement row and V4, keeps the Bot's review as swept feedback, and adds the bare-mode skills premise (round-6 INV-5 note, acted on in V2). Round 7 (Claude, 22:31Z, `accept`) confirmed INV-7. The first Codex review (`…-design-review-round7-codex.md`, `codex-review-dot-h001`, 22:34Z, `reject`) rejected INV-1, 3, 4, 5, 6, 9, 10, 12, all on one theme: evidence the orchestrator authors. v8 answers each: the waiver becomes a command under a `permissions.ask` rule (INV-1, INV-6) with the one-account residual stated in section 9; `repro:` is dropped and `check=` is a test selector only (INV-3); premises are reviewer and auditor evidence and the counting is the mechanical part (INV-4); the audit carries an input manifest and the acceptance record has an audit-input boundary (INV-5); cost records name their raw sources and stay a warning metric (INV-9); first push is the first commit's committer date and dispatchability is defined (INV-10); the independent oracle for gate-script PRs is the trusted-root audit (INV-12). The Codex P2 on the bare-mode skills premise is not adopted: the headless page says verbatim that "A directory you name with --add-dir is a partial exception: bare mode loads skills from its .claude/skills/ folder". Codex round 8 (`…-design-review-round8-codex.md`, 22:39Z, `reject`) accepted INV-1, 6, 7, 8, 9, 11 and the one-account residual, withdrew its bare-mode P2, and rejected INV-2 (tests unbounded), INV-3 (a changed file is not a run selector), INV-4 (sampling), INV-5 (the skills refusal was a premise, not a rule), INV-10 (committer date is not a push time; dependencies), INV-12 (a model audit is not a deterministic oracle), plus two stale enforcement rows. v9 adopts all: a 1000-line cap under tests/; the exact selector run on both heads in the PR's required `revise-check` job; every premise dispositioned by each reviewer and the auditor; the `.claude/**` refusal inside INV-5; the draft PR's `created_at` and an `after` list for dispatchability; a `main-tests` required job running main's tests against the PR's scripts (V5c); the two rows fixed. Claude round 8 (`…-design-review-round8.md`, 22:41Z, `revise`) rejected INV-1 (the waive script had no owner or row), INV-5 (once-per-head versus re-audit on a stale manifest) and INV-10 (fixed in v9), and offered a stronger anchor: the waiver record in a directory outside the sandbox write roots. Codex round 9 (`…-design-review-round9-codex.md`, 22:46Z, `reject`) accepted ten, rejected INV-5 (the `.claude/**` refusal that v9 claimed was silently lost by a failed edit, confirmed by grep) and INV-12 (the oracle must precede the waves), dispositioned all twelve premises (nine hold, three unverifiable in its read-only sandbox), and raised GitHub's 2026-11-02 `pull_request_target` policy. v10: the refusal is in INV-5 and verified by grep; one valid audit per head with stale-manifest replacement; the runner computes the manifest; the waiver record lives outside the sandbox write roots and V3a owns the script (map entry `[INV-6, INV-1]`); `main-tests` is wave V0 and every code wave is contract-first (INV-12, INV-2); the policy premise and residual. Claude round 9 (`…-design-review-round9.md`, 22:46Z, `revise`) found that `main-tests` as drafted would fail every intentional change and proposed running main's modules only for scripts outside `allowed_files`; Codex round 10 (`…-design-review-round10-codex.md`, 22:50Z, `reject`) accepted INV-1..11 and found that contract-first tests cannot merge ahead of an implementation that changes an existing script, proposing dormant contracts that `main-tests` activates on the implementation PR. v11's INV-12 is the union: main's modules as they are for undeclared scripts, main's dormant contracts (`REGIME_CONTRACT=1`) for declared ones, contract PRs required for design-tier waves; INV-1 states that the record's location is the guard and the ask rule the second layer (Claude round 9). Codex round 11 (`…-design-review-round11-codex.md`, 22:52Z) accepted INV-1..12 with no findings. Claude round 11 (`…-design-review-round11.md`, 22:54Z, `revise`) accepted everything but two INV-12 clauses: contracts must not stay dormant forever (the implementation PR removes the decorator; main-tests judges it against main's dormant copy) and an empty contract must fail a design-tier implementation PR. v12 adds both sentences to INV-12 and V0. Claude round 12 (`…-design-review-round12.md`, 22:57Z) accepted v12; Codex round 12 (`…-design-review-round12-codex.md`, 22:57Z, `revise`) accepted INV-1..11 and asked for a failing check behind the decorator-removal clause. v13 adds it to INV-12 (main-tests fails an implementation PR whose declared test module still carries a contract marker) and V0 carries it with the task-file reviewer's three V0 items (main's tests overlaid on a copy of the PR tree, module selection from the task's declared tests/ entries, task.md read with PyYAML). Round 13 (Claude 23:01Z, Codex 23:01Z and the premise map 23:17Z) accepted v13. Plan 006 (approved 2026-10-11) A102 amends two hashed keys: INV-12 states the in-process oracle's authenticated completion (nonce runner) and its residual, after the Codex Bot's P1 on V0's round-1 head repeated the class of the round-0 audit's finding 3; INV-2 and the map gain the .orchestration-only CI skip (`dotfiles-T128-ci-skip-orchestration-a01`, plan A201) that plan 006 orders as Phase 2. Round 14 (Codex 02:42Z `accept`; Claude 02:43Z `revise`): INV-12's residual clause understated the gap (the nonce authenticates the writer, not the counts; in-process patching of unittest's result collection forges counts with a genuine nonce) and INV-2 should cover every required check. v15 states the residual as it is, adds the runner's pinning of unittest classes, and words INV-2 for every required workflow. Round 15 asks both reviewers at once for one verdict each on this hash. Sources are the repository paths under `.orchestration/validation/dotfiles-T128-regime-v3-a01-research/` (`baseline.md`, `practice-evidence.md`, `claude-code-factsheet.md`, `codex-factsheet.md`, `github-factsheet.md`, `method-draft.md`). Receipt: `.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round15.md` (Claude) and `…-design-review-round15-codex.md` (Codex); the whole-file sha256 of this file in both headers.
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:227:v18 (plan 006 B0, plan 007 T701; written by the orchestrator under the records exemption, 2026-10-12): INV-12 narrowed to the undeclared-change regression guard: `main-tests` runs main's test module of every script outside `allowed_files`; a script inside `allowed_files` is judged by the PR's tests, the diff review and the trusted-root audit; the dormant-contract clauses, `REGIME_CONTRACT` and the `<task>-contract-a01` PRs are removed (A302 withdrew V1's contract PR under the Phase A correction and no wave has used one); `main-tests` decides inside its own job as the A5 workflows do. INV-2 loses the dead `-contract-a01` comparison and names A5's in-job form. `implementing_tasks` gains the V0 successor `dotfiles-T128-v0-main-tests-a02: [INV-12]` (A301) and `dotfiles-T128-gate-evidence-a01: [INV-6]` (plan 007 T702: the gate's `evidence=` grammar and the S6 refusal at INV-6's mandatory point). The INV-12 enforcement row, the V0 wave row and the wave order follow. Round 20 asks both reviewers at once for one verdict each on this hash: receipts `.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round20.md` (Claude) and `…-design-review-round20-codex.md` (Codex); the whole-file sha256 of this file in both headers.
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:229:v19 (round 20's one revision, 11:43Z): INV-6 gains the clause the Claude round-20 receipt asked for (the Codex round-20 receipt accepted v18 with no rejection), so `dotfiles-T128-gate-evidence-a01: [INV-6]` maps to a sentence that states the two refusals; nothing else changes. Round 21 asks both reviewers at once for one verdict each on this hash: receipts `…-design-review-round21.md` (Claude) and `…-design-review-round21-codex.md` (Codex).
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:231:v20 (11:46Z): the Codex round-21 receipt found the v19 clause appended to INV-4 (a stale line number after v18's two map insertions), so v20 moves that exact clause to the end of INV-6; INV-4 returns to its v18 text; nothing else changes. Round 22 asks both reviewers at once for one verdict each on this hash (round 21 was never sent to the Claude seat): receipts `…-design-review-round22.md` (Claude) and `…-design-review-round22-codex.md` (Codex).
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:235:v21 (13:08Z, the orchestrator under the records exemption): `implementing_tasks` gains `dotfiles-T128-gate-evidence-a02: [INV-6]`, the INV-6 successor of `dotfiles-T128-gate-evidence-a01` (withdrawn 13:02Z under INV-6 before its second amendment; reset record `dotfiles-T128-gate-evidence-a01-design-reset.md`), beside the a01 entry that stays as parked history, as the V0 and round-18 successors did; nothing else changes. Round 24 asks both reviewers at once for one verdict each on this hash: receipts `…-design-review-round24.md` (Claude) and `…-design-review-round24-codex.md` (Codex).
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:237:v22 (15:28Z, the orchestrator under the records exemption): `implementing_tasks` gains `dotfiles-T128-gate-evidence-a03: [INV-6]`, the INV-6 successor of a02 (withdrawn 15:25Z after its second S1 cycle; plan 011 option F: the acceptance record's machine-read parts as YAML front matter), beside the a01 and a02 entries kept as parked history; nothing else changes. Round 25 asks both reviewers at once for one verdict each on this hash: receipts `…-design-review-round25.md` (Claude) and `…-design-review-round25-codex.md` (Codex).
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:239:v23 (2026-10-13 02:55Z, the orchestrator under the records exemption): `implementing_tasks` gains `dotfiles-T128-gate-evidence-a04: [INV-6]`, the INV-6 successor of a03 (withdrawn 02:3xZ after the fourth binding row; plan 014 option A: the acceptance record's `ledger` must cover every swept Codex finding id and every audit finding `audit:<sha7>:<n>`, a set difference the gate computes; the a04 file's hash is in the reset record `dotfiles-T128-gate-evidence-a03-design-reset.md`, not here), beside the a01 to a03 entries kept as parked history; nothing else changes. Round 26 asks both reviewers at once for one verdict each on this hash: receipts `…-design-review-round26.md` (Claude) and `…-design-review-round26-codex.md` (Codex).
.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:241:v24 (2026-10-13 03:05Z, the orchestrator under the records exemption): the v23 line named the a04 file's hash, which moved when round 26's Codex half found the coverage sentence omitted badged Codex review bodies (a04 round 4 after round 3; no a04 hash appears in this design, the reset record `dotfiles-T128-gate-evidence-a03-design-reset.md` is the sole anchor, so later a04 rounds do not move the design); the map entry `dotfiles-T128-gate-evidence-a04: [INV-6]` is unchanged; nothing else changes. Rounds 27 and 28 ask both reviewers at once for one verdict each on this hash: receipts `…-design-review-round28.md` (Claude) and `…-design-review-round28-codex.md` (Codex); round 27's Codex half found the two hash mentions this text removed.
{
  "lastAnalyzedAt": "2026-10-02T14:12:51Z",
  "gitCommitHash": "940a3a2b07adfd14140a0acff96784ef53a0a509",
  "version": "1.0.0",
  "analyzedFiles": 368
}
10:## Architecture
17:## Regime activation and progress
21:- A Claude session started in the repository root outside Herdr (a plain shell, mosh/ssh, or `claude -p`) is a pane-less orchestrator: nothing seats a worker automatically, and the SessionStart `herdr-agents --attach` hook prints a summary line naming that state, the on-demand commands, and any seated worker, followed in a regime repository by the `agmsg-orchestration:` directive line. Bring the regime up on demand: claim the seat outside the sandbox with the composite instance id, `actas-claim.sh <repo> claude-code <name> <session_id>.<claude pid>` (a claim from sandboxed Bash writes the bare session id and turn delivery then skips silently; see the seat-lock bullet below); seat the worker with `herdr-agents --add-worker <worktree>` (it derives `HERDR_SOCKET_PATH` from the default Herdr server socket `~/.config/herdr/herdr.sock`, the path the Claude sandbox allowlists, before creating anything, accepts a claude worker's workspace-trust dialog during spawn's readiness wait, and takes `--ready-timeout <seconds>`); confirm the worker's placement from its `run/spawn.*` placement record itself (the `herdr:<socket>:<pane>` row that upstream `agmsg_spawn_path` resolves) and the `linkage=` line `--add-worker` prints, never from `team.sh <team> --json`, which observes Codex members by reading their pane; treat the `linkage=` line `--add-worker` prints as the `AGMSG-PING` evidence, and on `pong=no` or `linkage=unreached` wake again with `agmsg-dispatch <team> <orchestrator> <worker> <pane> 'AGMSG-PING v1 task_id=<id> reason=<reason>'` and verify the PING's `read_at` (`poke.sh` only for a viewed workspace); and dispatch no AGMSG-TASK before its `AGMSG-PONG` arrives. Without a managed workspace the auditor runs headless, in the form the task-level audit bullet below names. A pane-less session uses turn delivery when the Monitor cannot run; see "Identity, delivery, and storage" for the platform limits.
29:## Parallel workers
33:- Delegate all repository-mutating work — file edits, builds, test runs, and git state changes — to seated workers, with at most one seated worker per git worktree and sequential assignments within one worktree. Add worktrees for parallelism; never use parallel `codex exec` or per-task Codex spawning, except that the read-only, non-interactive task-level audit the orchestrator runs during acceptance (the task-level audit bullet below) is not worker spawning and is permitted; it is identity-less. agmsg/herdr control-plane commands (`delivery.sh`, `watch.sh`, `actas-claim.sh`, `send.sh`, `join.sh`, and herdr agent/pane commands) are orchestrator-side exemptions.
43:  - Some steps stay sequential. The single audit tab serializes audits; the task-level audit of T67 reduces them to one per task. The orchestrator-side gate (`make require-crit-review`) and merges also run one at a time.
46:## Identity, delivery, and storage
59:## Live verification
64:## Review and integration invariants
71:- A task that touches a trust boundary (anything the design tier lists, CI that decides a required check, code that executes PR-controlled input) carries a `threat_table` in its front matter: one `{control, disposition}` row per thing the PR or the orchestrator controls (the tree and its tests, task.md, workflow files, interpreter and environment files, in-process effects, new or renamed scripts, metadata separators). The row unit is one row per `allowed_files` entry, one row per listed control that is not a path (task metadata, workflow and interpreter or environment inputs, in-process effects, new or renamed scripts, metadata separators), carried by the declared test module's row where that is where the control acts, and one row per orchestrator effect from the fixed list (forced removal, merge, update-branch); under a wildcard `allowed_files` entry whose files are executed or applied (scripts, workflows, hooks, settings, the rules seats follow), one row per concrete file the PR changes; a wildcard over test fixtures or other data files keeps one row; C4 and C7b of `scripts/orchestrator/task-consistency-check.py` verify the path half before dispatch, and the task-file review checks the rest. A disposition takes one of three forms: `closed: tests/<file>::<name>`, the test that closes the row; `residual: <sentence>`, the compensating control; `out-of-scope: <task id>`, the task that owns the row. The task-file review checks the three shape rules by hand: a `closed` selector names a test present in the PR tree at acceptance, an `out-of-scope` owner is a task id in the design's `implementing_tasks`, a `residual` payload is a sentence of at least 20 characters (the gate's minimum for a reason). For a `closed` row it checks the selector's form only, since the test does not exist before implementation. Substance is the reviewers': the task-file review, the Bot and the auditor judge each row against the diff. The table is the task's completion condition: a missing row is added once, counted as an amendment, never fixed finding by finding.
72:- Before every acceptance action (revise, accept, merge) the orchestrator runs `scripts/regime-counters.sh <task id>` and pastes its output into the acceptance record. S2 is decided from INV-6's counts: each component the script prints is read from its output, and for each component it prints as `unknown` the record pastes the command and output that read the source INV-6 names for that component, or, while that source has no entry for the task, says so and pastes the reading of the interim record the orchestrator used in its place. S1 (plan 006: the same finding class three times on one artifact, from any reviewer) is decided from the record's finding-class table, which gives a class to every finding the PR-feedback sweep lists, whatever its disposition, and to every task-level audit finding; three rows of one class stop the artifact. Read that table over non-advisory rows only: list advisory P2 rows with their classes (`advisory-p2` and the `local:<sha7>:<n>` rows `local-advisory.sh` writes), exclude them from S1's three-rows count, and name the excluded rows in the record. The gate's S6 check still sees every ledger row, so an advisory class at three rows gets its `searches` entry from `acceptance-front-matter.py` like any other. INV-6's message and head counts and the S2 lines (`revises`, `amendments`, `questions`, `bot_p1_heads`) take no ledger rows; `scripts/regime-counters.sh` prints them unchanged.
90:  - The orchestrator dispositions every `[P0-P3]` finding in the acceptance record, whatever the verdict, numbered 1..N in the audit's order of `[P0-P3]` lines (the audit's finding lines may be bulleted). For an `incorrect` verdict the dispositions are the record's JSON `audit_findings`, the only form the gate reads: one `{n, reason, evidence}` entry per finding, `n` the number as a string and `reason` at least 20 characters, written with `scripts/orchestrator/acceptance-front-matter.py --audit-dispositions <tsv>`; an entry never cites a fix, since a fix moves the head and needs its own audit. A finding under `Verdict: correct` is dispositioned all the same, as an `audit-finding: <n> …` line in the record's prose: `fixed:<sha>` with a fresh audit of that sha, otherwise `not-applicable:<reason of at least 20 characters>`. Deferral ("later", a follow-up task, a stopgap or a suppression) is not a disposition except under the advisory-P2 policy in Orchestrator Playbook step 10.
95:## Message Contract v1
144:## `.orchestration` Workspace Layout
157:## Orchestrator Playbook
168:10. For a RESULT that carries a pull request, integrate in this order. This is the single procedure that the PR integration rule, `AGENTS.md`, the README and the gh-first-workflow skill cite. A `gh pr update-branch` moves the head, so steps 1 to 4 run again on the new head. After an update-branch the orchestrator runs it, the order is CI on the new head, then the sweep, then the audit; an audit started before CI finishes sees incomplete evidence and returns an evidence-only `incorrect`. Select a checkout with git -C <absolute path>, never with cd, which the sandboxed Bash may not honour. After moving the review worktree to the audited head, verify git -C <review> rev-parse HEAD equals that head and git -C <main> symbolic-ref --short HEAD prints main before the audit and the gate.
170:       - A P2 finding of the Codex Bot, local review or task-level audit is advisory: disposition it `not-applicable:advisory P2 owned by <lineage>-followup-a0<n>` and record an `<id><TAB><class>` row under `## Owned by <owner>` in the lineage's acceptance record, with the orchestrator writing the owner task file before the row.
173:    2. Run the task-level audit of that head in the pair or headless form of the task-level audit bullet. It exits nonzero for every verdict other than `correct`. An exit with `Audit verdict: incorrect` is not a failed step: continue to step 3 and disposition its findings. A `blocked` or missing verdict means re-running the audit.
174:    3. Write the acceptance record, summarising the dispositions, with every audit finding dispositioned as the task-level audit bullet says: for an `incorrect` verdict the record's JSON `audit_findings`, which the gate reads through `ACCEPTANCE_EVIDENCE`.
187:## Worker Playbook
198:10. If blocked, still write the report and evidence paths that explain the blocker.
215:    - Apart from those surviving P0/P1 items, the RESULT names every unresolved thread id with `fixed:<sha>` or a proposed `not-applicable:<reason>` under Orchestrator Playbook step 10. The worker resolves no thread.
217:## Codex seat worklogs
251:## Pitfalls

**Refining data extraction approach**
codex
差分の中心は、TASK 送信前の検査と履歴 200 行の照合です。履歴の並び順や行の重複が記録判定に与える影響と、修正後の Python 起動が呼び出し元の状態から隔離されているかを確認しています。GitHub CLI は接続に失敗したため、保存済み CI 証跡と別経路での取得を照合します。
exec
/bin/zsh -lc "python3 -I -B - <<'PY'
import json,subprocess
from pathlib import Path
g=json.loads(Path('.ua/knowledge-graph.json').read_text())
print('graph matches', [{k:n.get(k) for k in ('filePath','summary')} for n in g.get('nodes',[]) if 'orchestrator' in str(n.get('filePath',''))])
h=json.loads(Path('.ua/meta.json').read_text())['gitCommitHash']
changes=subprocess.check_output(['git','diff','--name-only',h+'..HEAD'],text=True).splitlines()
print('graph stale:', any(not p.startswith(('.ua/','.orchestration/')) for p in changes))
f=json.loads(Path('.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a03-pr-feedback.json').read_text())
print(json.dumps(f,indent=2))
PY" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc "sed -n '64,94p' ~/.agents/skills/agmsg-orchestration/SKILL.md; sed -n '168,186p' ~/.agents/skills/agmsg-orchestration/SKILL.md" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 exited 1 in 27ms:
zsh:1: can't create temp file for here document: operation not permitted

 succeeded in 34ms:
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


**Planning command execution safely**
exec
/bin/zsh -lc "python3 -I -B -c 'import json, subprocess
from pathlib import Path
g=json.loads(Path('\\''.ua/knowledge-graph.json'\\'').read_text())
print('\\''graph matches'\\'', [{k:n.get(k) for k in ('\\''filePath'\\'','\\''summary'\\'')} for n in g.get('\\''nodes'\\'',[]) if '\\''orchestrator'\\'' in str(n.get('\\''filePath'\\'','\\'''\\''))])
h=json.loads(Path('\\''.ua/meta.json'\\'').read_text())['\\''gitCommitHash'\\'']
changes=subprocess.check_output(['\\''git'\\'','\\''diff'\\'','\\''--name-only'\\'',h+'\\''..HEAD'\\''],text=True).splitlines()
print('\\''graph stale:'\\'', any(not p.startswith(('\\''.ua/'\\'','\\''.orchestration/'\\'')) for p in changes))
f=json.loads(Path('\\''.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a03-pr-feedback.json'\\'').read_text())
print(json.dumps(f,indent=2))
'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 583ms:
graph matches []
graph stale: True
{
  "repo": "mryfmo/dotfiles",
  "pr": 374,
  "head_sha": "ef74eaea9a94bff388b7c1027551a57797407b2f",
  "base_ref": "main",
  "base_sha": "f7847616970d6bd83739a75a65ad8f7c35e91462",
  "generated_at": "2026-10-17T00:47:52+00:00",
  "checks": [
    {
      "name": "private-bootstrap (macos-14, client)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38986083571/job/117257758156"
    },
    {
      "name": "public-bootstrap (macos-14, client)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38986083571/job/117257758131"
    },
    {
      "name": "private-bootstrap (ubuntu-24.04, client)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38986083571/job/117257758089"
    },
    {
      "name": "public-bootstrap (ubuntu-24.04, server)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38986083571/job/117257758029"
    },
    {
      "name": "public-bootstrap (ubuntu-24.04, client)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38986083571/job/117257757986"
    },
    {
      "name": "private-bootstrap (ubuntu-24.04, server)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38986083571/job/117257757831"
    },
    {
      "name": "test (ubuntu-24.04, client)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38986083514/job/117257757660"
    },
    {
      "name": "test (macos-14, client)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38986083514/job/117257757611"
    },
    {
      "name": "validate",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38986083491/job/117257757590"
    },
    {
      "name": "test (ubuntu-26.04, client)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38986083514/job/117257757585"
    },
    {
      "name": "test (ubuntu-24.04, server)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38986083514/job/117257757434"
    },
    {
      "name": "GitGuardian Security Checks",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/runs/117257752663"
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
      "body": "<!-- This is an auto-generated comment: summarize by coderabbit.ai -->\n<!-- This is an auto-generated comment: skip review by coderabbit.ai -->\n\n> [!IMPORTANT]\n> ## Review skipped\n> \n> Auto reviews are disabled on this repository. Please check the settings in the CodeRabbit UI or the `.coderabbit.yaml` file in this repository. To trigger a single review, invoke the `@coderabbitai review` command.\n> \n> <details>\n> <summary><strong>\u2699\ufe0f Run configuration</strong></summary>\n> <dl>\n> <dd>\n> \n> - **Configuration used**: Repository: mryfmo/dotfiles/.coderabbit.yaml\n> - **Review profile**: CHILL\n> - **Plan**: Advanced\n> - **Run ID**: `e1c44281-c34f-44e1-a9e1-224dbbd5c514`\n> \n> </dd>\n> </dl>\n> </details>\n> \n> You can disable this status message by setting the `reviews.review_status` to `false` in the CodeRabbit configuration file.\n> \n> Use the checkbox below for a quick retry:\n> - [ ] <!-- {\"checkboxId\":\"e9bb8d72-00e8-4f67-9cb2-caf3b22574fe\"} --> \ud83d\udd0d Trigger review\n\n<!-- end of auto-generated comment: skip review by coderabbit.ai -->\n\n<!-- autopilot:start -->\n- [ ] <!-- {\"checkboxId\":\"2708ad07-9f24-4260-9c11-7dc76a49f2e3\"} --> <strong title=\"Keep fixing CodeRabbit findings and required CI, and resolving merge conflicts\">Autofix</strong> \u00b7 Keep fixing CodeRabbit findings and required CI, and resolving merge conflicts\n<!-- autopilot:end -->\n<!-- tips_start -->\n\n\n\nThanks for using [CodeRabbit](https://coderabbit.ai?utm_source=oss&utm_medium=github&utm_campaign=mryfmo/dotfiles&utm_content=374)! It's free for OSS, and your support helps us grow. If you like it, consider giving us a shout-out.\n\n<details>\n<summary><strong>\u2764\ufe0f Share</strong></summary>\n<dl>\n<dd>\n\n- [X](https://twitter.com/intent/tweet?text=I%20just%20used%20%40coderabbitai%20for%20my%20code%20review%2C%20and%20it%27s%20fantastic%21%20It%27s%20free%20for%20OSS%20and%20offers%20a%20free%20trial%20for%20the%20proprietary%20code.%20Check%20it%20out%3A&url=https%3A//coderabbit.ai)\n- [Mastodon](https://mastodon.social/share?text=I%20just%20used%20%40coderabbitai%20for%20my%20code%20review%2C%20and%20it%27s%20fantastic%21%20It%27s%20free%20for%20OSS%20and%20offers%20a%20free%20trial%20for%20the%20proprietary%20code.%20Check%20it%20out%3A%20https%3A%2F%2Fcoderabbit.ai)\n- [Reddit](https://www.reddit.com/submit?title=Great%20tool%20for%20code%20review%20-%20CodeRabbit&text=I%20just%20used%20CodeRabbit%20for%20my%20code%20review%2C%20and%20it%27s%20fantastic%21%20It%27s%20free%20for%20OSS%20and%20offers%20a%20free%20trial%20for%20proprietary%20code.%20Check%20it%20out%3A%20https%3A//coderabbit.ai)\n- [LinkedIn](https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Fcoderabbit.ai&mini=true&title=Great%20tool%20for%20code%20review%20-%20CodeRabbit&summary=I%20just%20used%20CodeRabbit%20for%20my%20code%20review%2C%20and%20it%27s%20fantastic%21%20It%27s%20free%20for%20OSS%20and%20offers%20a%20free%20trial%20for%20proprietary%20code)\n\n</dd>\n</dl>\n</details>\n\n\n<sub>Comment `@coderabbitai help` to get the list of available commands.</sub>\n\n<!-- tips_end -->",
      "url": "https://github.com/mryfmo/dotfiles/pull/374#issuecomment-6211755266",
      "disposition": "not-applicable:bot summary or onboarding comment, no finding; evidence=jq --argjson u '\"https://github.com/mryfmo/dotfiles/pull/374#issuecomment-6211755266\"' '.items[] | select(.url == $u)' .orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a03-pr-feedback.json"
    },
    {
      "source": "issue_comment",
      "author": "chatgpt-codex-connector[bot]",
      "bot": true,
      "level": "comment",
      "path": null,
      "line": null,
      "body": "<!-- codex-pull-request-review-summary -->\n<!-- codex-review-state:v1 {\"code_review\":{\"commit_sha\":\"9cf65c0299645e30e54419668ba523eff9c4897e\",\"has_any_findings\":false,\"has_unresolved_findings\":false,\"status\":\"completed\"},\"security_review\":{\"commit_sha\":\"aeb4a0fbe9c4e88b6d95a4f3aa91f1f85e52d601\",\"has_any_findings\":false,\"has_unresolved_findings\":false,\"status\":\"completed\"}} -->\n<!-- codex-security-review:v1 {\"blockingSeverityThreshold\":\"P0\",\"headSha\":\"aeb4a0fbe9c4e88b6d95a4f3aa91f1f85e52d601\",\"mergeGateEnabled\":false,\"pullRequestNumber\":374,\"repository\":\"mryfmo/dotfiles\",\"status\":\"completed\"} -->\n## Codex Review Summary\n\nThis comment shows the latest Codex review activity on this pull request.\n\n| Review | Status | Commit | Review trigger |\n| --- | --- | --- | --- |\n| \ud83d\udcdd **Code Review** | \u2705 **Completed** <relative-time datetime=\"2026-10-16T23:32:53.621034Z\">2026-10-16T23:32:53.621034Z</relative-time> | `9cf65c0` | Manual request |\n| \ud83d\udd12 **Security Review** | \u2705 **Completed** <relative-time datetime=\"2026-10-16T09:00:45.836851Z\">2026-10-16T09:00:45.836851Z</relative-time> | `aeb4a0f` | Draft marked ready |\n\n\n\n<details> <summary>\u2139\ufe0f About Codex in GitHub</summary>\n<br/>\n\n[Your team has set up Codex to review pull requests in this repo](https://chatgpt.com/codex/cloud/settings/general). Reviews are triggered when you\n- Open a pull request for review\n- Mark a draft as ready\n- Comment \"@codex review\" or \"@codex security review\".\n\nCodex reacts with \ud83d\udc40 while any review is running, comments if it has suggestions, and reacts with \ud83d\udc4d once all reviews finish with no findings.\n\n</details>",
      "url": "https://github.com/mryfmo/dotfiles/pull/374#issuecomment-6211756067",
      "disposition": "not-applicable:bot summary or onboarding comment, no finding; evidence=jq --argjson u '\"https://github.com/mryfmo/dotfiles/pull/374#issuecomment-6211756067\"' '.items[] | select(.url == $u)' .orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a03-pr-feedback.json"
    },
    {
      "source": "issue_comment",
      "author": "moriya-fumio-thd",
      "bot": false,
      "level": "comment",
      "path": null,
      "line": null,
      "body": "@codex review",
      "url": "https://github.com/mryfmo/dotfiles/pull/374#issuecomment-6225256851",
      "disposition": "not-applicable:bot summary or onboarding comment, no finding; evidence=jq --argjson u '\"https://github.com/mryfmo/dotfiles/pull/374#issuecomment-6225256851\"' '.items[] | select(.url == $u)' .orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a03-pr-feedback.json"
    },
    {
      "source": "issue_comment",
      "author": "moriya-fumio-thd",
      "bot": false,
      "level": "comment",
      "path": null,
      "line": null,
      "body": "@codex review",
      "url": "https://github.com/mryfmo/dotfiles/pull/374#issuecomment-6225721682",
      "disposition": "not-applicable:bot summary or onboarding comment, no finding; evidence=jq --argjson u '\"https://github.com/mryfmo/dotfiles/pull/374#issuecomment-6225721682\"' '.items[] | select(.url == $u)' .orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a03-pr-feedback.json"
    },
    {
      "source": "issue_comment",
      "author": "chatgpt-codex-connector[bot]",
      "bot": true,
      "level": "comment",
      "path": null,
      "line": null,
      "body": "<!-- codex-review-receipt:v1 -->\n\nCodex Review: Didn't find any major issues. Delightful!\n\n**Reviewed commit:** `9df6b0c759`\n\n<details> <summary>\u2139\ufe0f About Codex in GitHub</summary>\n<br/>\n\nCodex has been enabled to automatically review pull requests in this repo. Reviews are triggered when you\n- Open a pull request for review\n- Mark a draft as ready\n- Comment \"@codex review\".\n\nIf Codex has suggestions, it will comment; otherwise it will react with \ud83d\udc4d.\n\n\n\n\nWhen you [sign up for Codex through ChatGPT](https://openai.com/codex), Codex can also answer questions or update the PR, like \"@codex address that feedback\".\n            \n</details>",
      "url": "https://github.com/mryfmo/dotfiles/pull/374#issuecomment-6225762121",
      "disposition": "not-applicable:bot summary or onboarding comment, no finding; evidence=jq --argjson u '\"https://github.com/mryfmo/dotfiles/pull/374#issuecomment-6225762121\"' '.items[] | select(.url == $u)' .orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a03-pr-feedback.json"
    },
    {
      "source": "issue_comment",
      "author": "moriya-fumio-thd",
      "bot": false,
      "level": "comment",
      "path": null,
      "line": null,
      "body": "@codex review",
      "url": "https://github.com/mryfmo/dotfiles/pull/374#issuecomment-6226303513",
      "disposition": "not-applicable:bot summary or onboarding comment, no finding; evidence=jq --argjson u '\"https://github.com/mryfmo/dotfiles/pull/374#issuecomment-6226303513\"' '.items[] | select(.url == $u)' .orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a03-pr-feedback.json"
    },
    {
      "source": "issue_comment",
      "author": "moriya-fumio-thd",
      "bot": false,
      "level": "comment",
      "path": null,
      "line": null,
      "body": "@codex review",
      "url": "https://github.com/mryfmo/dotfiles/pull/374#issuecomment-6226597044",
      "disposition": "not-applicable:bot summary or onboarding comment, no finding; evidence=jq --argjson u '\"https://github.com/mryfmo/dotfiles/pull/374#issuecomment-6226597044\"' '.items[] | select(.url == $u)' .orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a03-pr-feedback.json"
    },
    {
      "source": "issue_comment",
      "author": "chatgpt-codex-connector[bot]",
      "bot": true,
      "level": "comment",
      "path": null,
      "line": null,
      "body": "<!-- codex-review-receipt:v1 -->\n\nCodex Review: Didn't find any major issues. Swish!\n\n**Reviewed commit:** `9cf65c0299`\n\n<details> <summary>\u2139\ufe0f About Codex in GitHub</summary>\n<br/>\n\nCodex has been enabled to automatically review pull requests in this repo. Reviews are triggered when you\n- Open a pull request for review\n- Mark a draft as ready\n- Comment \"@codex review\".\n\nIf Codex has suggestions, it will comment; otherwise it will react with \ud83d\udc4d.\n\n\n\n\nWhen you [sign up for Codex through ChatGPT](https://openai.com/codex), Codex can also answer questions or update the PR, like \"@codex address that feedback\".\n            \n</details>",
      "url": "https://github.com/mryfmo/dotfiles/pull/374#issuecomment-6226653561",
      "disposition": "not-applicable:bot summary or onboarding comment, no finding; evidence=jq --argjson u '\"https://github.com/mryfmo/dotfiles/pull/374#issuecomment-6226653561\"' '.items[] | select(.url == $u)' .orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a03-pr-feedback.json"
    },
    {
      "source": "review",
      "author": "chatgpt-codex-connector[bot]",
      "bot": true,
      "level": "commented",
      "path": null,
      "line": null,
      "body": "<!-- codex-review-receipt:v1 -->\n\n\n### \ud83d\udca1 Codex Review\n\nHere are some automated review suggestions for this pull request.\n\n**Reviewed commit:** `aeb4a0fbe9`\n    \n\n<details> <summary>\u2139\ufe0f About Codex in GitHub</summary>\n<br/>\n\nCodex has been enabled to automatically review pull requests in this repo. Reviews are triggered when you\n- Open a pull request for review\n- Mark a draft as ready\n- Comment \"@codex review\".\n\nIf Codex has suggestions, it will comment; otherwise it will react with \ud83d\udc4d.\n\n\n\n\nWhen you [sign up for Codex through ChatGPT](https://openai.com/codex), Codex can also answer questions or update the PR, like \"@codex address that feedback\".\n            \n</details>",
      "url": "https://github.com/mryfmo/dotfiles/pull/374#pullrequestreview-5545290170",
      "commit": "aeb4a0fbe9c4e88b6d95a4f3aa91f1f85e52d601",
      "disposition": "not-applicable:review object; its findings are the inline threads, each dispositioned on its own; evidence=jq --argjson u '\"https://github.com/mryfmo/dotfiles/pull/374#pullrequestreview-5545290170\"' '.items[] | select(.url == $u)' .orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a03-pr-feedback.json"
    },
    {
      "source": "review",
      "author": "chatgpt-codex-connector[bot]",
      "bot": true,
      "level": "commented",
      "path": null,
      "line": null,
      "body": "<!-- codex-review-receipt:v1 -->\n\n\n### \ud83d\udca1 Codex Review\n\nHere are some automated review suggestions for this pull request.\n\n**Reviewed commit:** `57d3577ca7`\n    \n\n<details> <summary>\u2139\ufe0f About Codex in GitHub</summary>\n<br/>\n\nCodex has been enabled to automatically review pull requests in this repo. Reviews are triggered when you\n- Open a pull request for review\n- Mark a draft as ready\n- Comment \"@codex review\".\n\nIf Codex has suggestions, it will comment; otherwise it will react with \ud83d\udc4d.\n\n\n\n\nWhen you [sign up for Codex through ChatGPT](https://openai.com/codex), Codex can also answer questions or update the PR, like \"@codex address that feedback\".\n            \n</details>",
      "url": "https://github.com/mryfmo/dotfiles/pull/374#pullrequestreview-5554058212",
      "commit": "57d3577ca780248f573fd26c4fa460e2b5e2d510",
      "disposition": "not-applicable:review object; its findings are the inline threads, each dispositioned on its own; evidence=jq --argjson u '\"https://github.com/mryfmo/dotfiles/pull/374#pullrequestreview-5554058212\"' '.items[] | select(.url == $u)' .orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a03-pr-feedback.json"
    },
    {
      "source": "review",
      "author": "chatgpt-codex-connector[bot]",
      "bot": true,
      "level": "commented",
      "path": null,
      "line": null,
      "body": "<!-- codex-review-receipt:v1 -->\n\n\n### \ud83d\udca1 Codex Review\n\nHere are some automated review suggestions for this pull request.\n\n**Reviewed commit:** `6ae8cf75df`\n    \n\n<details> <summary>\u2139\ufe0f About Codex in GitHub</summary>\n<br/>\n\nCodex has been enabled to automatically review pull requests in this repo. Reviews are triggered when you\n- Open a pull request for review\n- Mark a draft as ready\n- Comment \"@codex review\".\n\nIf Codex has suggestions, it will comment; otherwise it will react with \ud83d\udc4d.\n\n\n\n\nWhen you [sign up for Codex through ChatGPT](https://openai.com/codex), Codex can also answer questions or update the PR, like \"@codex address that feedback\".\n            \n</details>",
      "url": "https://github.com/mryfmo/dotfiles/pull/374#pullrequestreview-5554562648",
      "commit": "6ae8cf75df74bb54eb3b724ea7c94e16b70759ef",
      "disposition": "not-applicable:review object; its findings are the inline threads, each dispositioned on its own; evidence=jq --argjson u '\"https://github.com/mryfmo/dotfiles/pull/374#pullrequestreview-5554562648\"' '.items[] | select(.url == $u)' .orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a03-pr-feedback.json"
    },
    {
      "source": "review_comment",
      "author": "chatgpt-codex-connector[bot]",
      "bot": true,
      "level": "comment",
      "path": "scripts/orchestrator/dispatch.sh",
      "line": 181,
      "body": "**<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Isolate uv from the caller's project**\n\nWhen `dispatch.sh` is invoked from a directory containing an untrusted `pyproject.toml`, both `uv run` forms discover and synchronize that caller-controlled project before the task is validated; a local build backend can therefore execute during this probe. `uv run --help` defines `--no-project` as \u201cAvoid discovering the project or workspace,\u201d but it is omitted here. Add `--no-project` to both the offline and fallback forms (or run from a fixed trusted directory); otherwise the threat-table claim that the caller's working directory controls nothing is false.\n\nAGENTS.md reference: [AGENTS.md:L78-L78](https://github.com/mryfmo/dotfiles/blob/aeb4a0fbe9c4e88b6d95a4f3aa91f1f85e52d601/AGENTS.md#L78-L78)\n\nUseful? React with \ud83d\udc4d\u00a0/ \ud83d\udc4e.\n\n<!-- codex-code-review-finding:v1 -->",
      "url": "https://github.com/mryfmo/dotfiles/pull/374#discussion_r4292675906",
      "resolved": false,
      "outdated": true,
      "disposition": "fixed:c8e813eaf423ed396467b9db7ff5fc243c54762c"
    },
    {
      "source": "review_comment",
      "author": "chatgpt-codex-connector[bot]",
      "bot": true,
      "level": "comment",
      "path": "scripts/orchestrator/dispatch.sh",
      "line": 182,
      "body": "**<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Run uv outside the caller-controlled directory**\n\nWhen `dispatch.sh` is invoked from an untrusted directory containing `.python-version` with a path such as `./pwn`, both commands still let uv execute that caller-controlled interpreter with the orchestrator's credentials before validating the task. Fresh evidence beyond the earlier `pyproject.toml` report is that uv 0.7.22 executes `./pwn` even with `run --no-project`, while `uv help run` says `--no-project` still uses a virtual environment \u201cfound in a current or parent directory\u201d; the existing uv test shim also models `.python-version` execution at `tests/unit/test_orchestrator_tools.py:40-43`. Run these commands from the trusted script root or resolve and pin a trusted interpreter first; the current behavior also contradicts the threat-table residual claiming the caller cwd chooses nothing.\n\nAGENTS.md reference: [AGENTS.md:L78-L78](https://github.com/mryfmo/dotfiles/blob/57d3577ca780248f573fd26c4fa460e2b5e2d510/AGENTS.md#L78-L78)\n\nUseful? React with \ud83d\udc4d\u00a0/ \ud83d\udc4e.\n\n<!-- codex-code-review-finding:v1 -->",
      "url": "https://github.com/mryfmo/dotfiles/pull/374#discussion_r4299651928",
      "resolved": false,
      "outdated": true,
      "disposition": "fixed:8adf74bb3d804c917b5bbe5f4f806c8b1ceaabb7"
    },
    {
      "source": "review_comment",
      "author": "chatgpt-codex-connector[bot]",
      "bot": true,
      "level": "comment",
      "path": "scripts/orchestrator/dispatch.sh",
      "line": 197,
      "body": "**<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Isolate the PyYAML probe from inherited Python paths**\n\nWhen a trusted invocation inherits `PYTHONPATH` pointing to a caller-writable directory containing `yaml.py`, this probe runs `python -c 'import yaml'` without isolated mode, so uv preserves the variable and executes that module before the task is validated. I confirmed this behavior with uv 0.7.22; the later `python -I` calls do not prevent the initial execution. Use `python -I -c 'import yaml'` for the probe or remove Python override variables as part of the sanitized environment; otherwise the task's environment-input residual does not close this trust boundary.\n\nAGENTS.md reference: [AGENTS.md:L78-L78](https://github.com/mryfmo/dotfiles/blob/6ae8cf75df74bb54eb3b724ea7c94e16b70759ef/AGENTS.md#L78-L78)\n\nUseful? React with \ud83d\udc4d\u00a0/ \ud83d\udc4e.\n\n<!-- codex-code-review-finding:v1 -->",
      "url": "https://github.com/mryfmo/dotfiles/pull/374#discussion_r4300102967",
      "resolved": false,
      "outdated": true,
      "disposition": "fixed:b18698d500581ec2fead4e4628da7889f40845bf"
    },
    {
      "source": "annotation",
      "author": "github-actions",
      "bot": true,
      "level": "notice",
      "path": ".github",
      "line": 1,
      "body": "Due to capacity constraints, jobs targeting macOS arm64 runners may experience longer queue times.",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38986083571/job/117257758156",
      "check": "private-bootstrap (macos-14, client)",
      "disposition": "not-applicable:runner capacity notice, no finding; evidence=jq --argjson u '\"https://github.com/mryfmo/dotfiles/actions/runs/38986083571/job/117257758156\"' '.items[] | select(.url == $u)' .orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a03-pr-feedback.json"
    },
    {
      "source": "annotation",
      "author": "github-actions",
      "bot": true,
      "level": "notice",
      "path": ".github",
      "line": 1,
      "body": "Due to capacity constraints, jobs targeting macOS arm64 runners may experience longer queue times.",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38986083571/job/117257758131",
      "check": "public-bootstrap (macos-14, client)",
      "disposition": "not-applicable:runner capacity notice, no finding; evidence=jq --argjson u '\"https://github.com/mryfmo/dotfiles/actions/runs/38986083571/job/117257758131\"' '.items[] | select(.url == $u)' .orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a03-pr-feedback.json"
    },
    {
      "source": "annotation",
      "author": "github-actions",
      "bot": true,
      "level": "notice",
      "path": ".github",
      "line": 1,
      "body": "Due to capacity constraints, jobs targeting macOS arm64 runners may experience longer queue times.",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38986083514/job/117257757611",
      "check": "test (macos-14, client)",
      "disposition": "not-applicable:runner capacity notice, no finding; evidence=jq --argjson u '\"https://github.com/mryfmo/dotfiles/actions/runs/38986083514/job/117257757611\"' '.items[] | select(.url == $u)' .orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a03-pr-feedback.json"
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
      "disposition": "not-applicable:CI status, no finding; evidence=jq --argjson s '\"status\"' --argjson c '\"CodeRabbit\"' '.items[] | select(.source == $s and .check == $c)' .orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a03-pr-feedback.json"
    }
  ]
}

**Considering GitHub tool usage**
exec
/bin/zsh -lc "nl -ba .orchestration/tasks/dotfiles-T128-regime-v3-a01.md | sed -n '54,67p'; nl -ba .orchestration/acceptance/dotfiles-T128-orchestrator-tools-followup-a03.md | tail -n 16; nl -ba .orchestration/sandboxes/dotfiles-T128-orchestrator-tools-followup-a03.md" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 17ms:
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
    88	
    89	## Dispatch (bus lines)
    90	
    91	- AGMSG-TASK v1 task_id=dotfiles-T128-orchestrator-tools-followup-review-a03 round=1 repo=~/Workspace/dotfiles task_file=.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-review-a03.md task_sha256=a328b9871e0591f16a451d228823c5528791abb67c639623d7c7deb0804a5b3b tools_task_file=.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a03.md tools_task_sha256=7f2f42392809b909eea3f3110d7378e61ea1725c32105aa2a8824dc2843463d8 deadline=none note=one-round-review-of-the-owner-task-corrections-C-52-(2)-and-C-53-(2)-name(the-Codex-half-confirmed-first,C-54);answer-with-AGMSG-RESULT-verdict=confirm|revise-tools_task_sha256=<sha> read_at=read
    92	- AGMSG-TASK v1 task_id=dotfiles-T128-orchestrator-tools-followup-review-a03 round=2 repo=~/Workspace/dotfiles task_file=.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-review-a03.md task_sha256=8bec237cac18e2cc81512a9ac803ee01a53f551da946f4417f1d0fe4207f807f tools_task_file=.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a03.md tools_task_sha256=296f35d9c815a33d3873b9abca0ee4d70546383fb34ed8be3d5707708a99a089 deadline=none note=one-round-review-of-the-owner-task-corrections-C-52-(2)-and-C-53-(2)-name(the-Codex-half-confirmed-first,C-54;your-round-1-applied:the-window-read-anchored-on-the-newest-pre-send-row-not-a-count,the-checker-s-own-line-asserted-through-a-stub-checker-beside-the-copied-script,presend.sh-keeps-the-premise-replay-and-the-mask-check,the-exitcode-line;the-Codex-rounds-4-and-5:the-two-windows-are-aligned-as-views-of-one-bus-by-the-smallest-shift,the-last-new-row-must-equal-the-line,anything-else-refused,with-eviction-and-collision-cases;the-Codex-round-6-P1:the-exemption-needs-a-successful-duplicate-rejecting-YAML-parse-yielding-review,a-malformed-front-matter-is-checked;the-Codex-round-7-P1:the-fake-uv-delegates-to-the-real-uv-so-PyYAML-is-present-as-in-production;the-Codex-round-8-P1:a-nonempty-overlap-is-required-unless-the-pre-send-window-was-empty;the-Codex-round-9-P2:the-pre-send-window-file-is-a-private-mktemp-file-removed-by-a-trap,with-its-own-row;the-Codex-round-10-P1:the-alignment-must-be-unique-across-every-shift-including-no-change,else-refused,with-a-periodic-bus-case);answer-with-AGMSG-RESULT-verdict=confirm|revise-tools_task_sha256=<sha> read_at=read
    93	- AGMSG-TASK v1 task_id=dotfiles-T128-orchestrator-tools-followup-review-a03 round=3 repo=~/Workspace/dotfiles task_file=.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-review-a03.md task_sha256=5a189d71db69b6a482b01decec362514f370dec364977a9b662b34281cb0487e tools_task_file=.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a03.md tools_task_sha256=5a741e63e619ad31f83f10516be178f0ba63490bca2d4e16f9e45c14d4070b0a deadline=none note=one-round-review-of-the-owner-task-corrections-C-52-(2)-and-C-53-(2)-name(the-Codex-half-confirmed-first,C-54;your-round-1-applied:the-window-read-anchored-on-the-newest-pre-send-row-not-a-count,the-checker-s-own-line-asserted-through-a-stub-checker-beside-the-copied-script,presend.sh-keeps-the-premise-replay-and-the-mask-check,the-exitcode-line;the-Codex-rounds-4-and-5:the-two-windows-are-aligned-as-views-of-one-bus-by-the-smallest-shift,the-last-new-row-must-equal-the-line,anything-else-refused,with-eviction-and-collision-cases;the-Codex-round-6-P1:the-exemption-needs-a-successful-duplicate-rejecting-YAML-parse-yielding-review,a-malformed-front-matter-is-checked;the-Codex-round-7-P1:the-fake-uv-delegates-to-the-real-uv-so-PyYAML-is-present-as-in-production;the-Codex-round-8-P1:a-nonempty-overlap-is-required-unless-the-pre-send-window-was-empty;the-Codex-round-9-P2:the-pre-send-window-file-is-a-private-mktemp-file-removed-by-a-trap,with-its-own-row;the-Codex-round-10-P1:the-alignment-must-be-unique-across-every-shift-including-no-change,else-refused,with-a-periodic-bus-case;your-round-2:among-the-new-rows-the-last-one-equal-to-the-line-is-the-send,the-fake-uv-runs-the-probe-form-itself,the-module-s-uv-dependency-named-as-new);answer-with-AGMSG-RESULT-verdict=confirm|revise-tools_task_sha256=<sha> read_at=read
    94	- AGMSG-TASK v1 task_id=dotfiles-T128-orchestrator-tools-followup-review-a03 round=4 repo=~/Workspace/dotfiles task_file=.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-review-a03.md task_sha256=5a189d71db69b6a482b01decec362514f370dec364977a9b662b34281cb0487e tools_task_file=.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a03.md tools_task_sha256=b291ba85f89d46877f74969d4e33ce994ff875f83454df58dbd8037a7d745da7 deadline=none note=round-4-a-re-confirm-after-one-change-since-the-pair-confirmed-5a741e63:the-Change(bot_rounds)section-names-it,the-Completion-clause-s-bot_rounds=1-becoming-the-template-s-bot_rounds=2-form(the-Bot-s-review-at-PR-open-and-its-re-review-after-the-fix-round;T13-amendment-6);judge-that-nothing-else-changed-and-the-clause-reads-consistently;the-Codex-half-confirmed(round-13);answer-with-AGMSG-RESULT-verdict=confirm|revise-tools_task_sha256=<sha> read_at=read
    95	- AGMSG-TASK v1 task_id=dotfiles-T128-orchestrator-tools-followup-a03 round=1 repo=~/Workspace/dotfiles/.claude/worktrees/worker-c task_file=.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a03.md task_sha256=b291ba85f89d46877f74969d4e33ce994ff875f83454df58dbd8037a7d745da7 deadline=none note=plan-022-tools-a03(dispatch.sh:the-checker-refusal-and-the-bounded-aligned-window-reads,C-52/C-53-tool-halves);pair-confirmed-at-this-hash(Codex-round-13,seat-round-4);read-the-task-file-first,fresh-branch-from-origin/main(1d418126-or-later),one-PR,the-Bot-reviews-once-at-PR-open,RESULT-per-Worker-Playbook-step-15 read_at=read
    96	- AGMSG-ACCEPTANCE v1 task_id=dotfiles-T128-orchestrator-tools-followup-a03 round=1 status=pending-integration reason=RESULT-read:head-57d3577c,CI-13-pass,4292675906-fixed:c8e813ea,the-Bot-s-re-review-P1-4299651928(uv-runs-a-caller-cwd-interpreter)survives-the-one-fix-round,so-the-Completion-clause-sends-it-to-the-operator(D-P1-374,default-A:one-more-fix-round,uv-run-from-the-trusted-script-root);hold-until-the-decision;nothing-to-do-on-your-side previous_head=57d3577ca780248f573fd26c4fa460e2b5e2d510 next_action=none-until-the-decision read_at=read
    97	- AGMSG-ACCEPTANCE v1 task_id=dotfiles-T128-orchestrator-tools-followup-a03 round=1 status=revise reason=operator-decision-D-P1-374-A(AskUserQuestion,plan-022):one-more-fix-round-for-the-Bot-s-P1-4299651928-on-57d3577c:run-both-uv-commands-from-the-trusted-script-root(uv---directory-<root>-or-a-cd-subshell-to-git-rev-parse---show-toplevel-of-the-script)so-a-caller-cwd-s-.python-version-or-venv-chooses-nothing,one-test(the-uv-shim-records-the-directory-it-ran-in-or-a-caller-cwd-.python-version-./pwn-is-not-executed);the-task-text-s-threat-row-is-corrected-by-the-orchestrator(Change-note);commit,push,@codex-review,RESULT-naming-4299651928-fixed:<sha> check=tests/unit/test_orchestrator_tools.py(the-new-test,named-in-the-RESULT) previous_head=57d3577ca780248f573fd26c4fa460e2b5e2d510 next_action=fix-round,commit,push,@codex-review,RESULT read_at=read
    98	- AGMSG-ACCEPTANCE v1 task_id=dotfiles-T128-orchestrator-tools-followup-a03 round=2 status=pending-integration reason=RESULT-round-2-read:head-9df6b0c7,both-Bot-P1-fixed(4292675906:c8e813ea,4299651928:8adf74bb:uv-in-a-subshell-cd-to-the-script-s-checkout-root);the-chain-runs-on-this-head(CI,Bot-wait,sandbox-scan,local-review,sweep,receipt,audit);the-orchestrator-replies-to-and-resolves-the-threads;nothing-to-do-on-your-side previous_head=9df6b0c7594cef7f42e9a43faa3e08d0f035e329 next_action=none-until-the-integration-result read_at=read
    99	- AGMSG-ACCEPTANCE v1 task_id=dotfiles-T128-orchestrator-tools-followup-a03 round=2 status=pending-integration reason=the-local-review-of-9df6b0c7-found-a-P1(dispatch.sh-183-185:an-inherited-VIRTUAL_ENV-still-selects-uv-s-interpreter-after-the-cd,so-a-PR-checkout-s-.venv-can-run-during-the-import-yaml-probe);the-third-finding-of-one-class(the-interpreter-chosen-from-caller-state:pyproject,.python-version,VIRTUAL_ENV);the-chain-stopped-before-the-audit;a-further-fix-round-makes-INV-6-read-revises-2,so-it-waits-for-the-operator-s-decision-D-S2-374-2(default-A:one-round-that-closes-the-class:pin-the-interpreter-and-strip-the-inherited-env);hold previous_head=9df6b0c7594cef7f42e9a43faa3e08d0f035e329 next_action=none-until-the-decision read_at=unread
   100	- AGMSG-ACCEPTANCE v1 task_id=dotfiles-T128-orchestrator-tools-followup-a03 round=2 status=revise reason=operator-decision-D-S2-374-2-A(AskUserQuestion,plan-022:S2-waived):one-round-that-closes-the-class(C-57,identity-over-shape):both-uv-invocations-name-the-interpreter(--python-<the-trusted-interpreter-resolved-at-the-script-s-checkout-root,e.g.-the-python3-mise-provides-there>)and-run-under-an-environment-without-VIRTUAL_ENV,VIRTUAL_ENV_PROMPT,UV_PROJECT_ENVIRONMENT,UV_PYTHON-and-the-other-UV_*-overrides(env--u-…-or-an-explicit-allowlisted-env),keeping---no-project-and-the-cd-to-the-root;one-test-that-sets-a-caller-pyproject,a-caller-cwd-.python-version-and-VIRTUAL_ENV-at-once-and-asserts-none-is-used(the-fake-uv-records-its-env-and-args);nothing-else;commit,push,@codex-review,RESULT-naming-local:9df6b0c:1-fixed:<sha>-and-the-test check=tests/unit/test_orchestrator_tools.py(the-new-test,named-in-the-RESULT) previous_head=9df6b0c7594cef7f42e9a43faa3e08d0f035e329 next_action=fix-round,commit,push,@codex-review,RESULT read_at=unread
   101	- AGMSG-ACCEPTANCE v1 task_id=dotfiles-T128-orchestrator-tools-followup-a03 round=3 status=pending-integration reason=RESULT-round-3-read:head-6ae8cf75,local:9df6b0c:1-fixed:411c7d68(pinned---python,env--u-VIRTUAL_ENV/CONDA_PREFIX/UV_*),12-mutants,CI-13-pass;the-Bot-s-re-review-P1-4300102967(the-import-yaml-probe-without--I,an-inherited-PYTHONPATH-loads-a-caller-s-yaml.py)is-the-fourth-finding-of-the-class;a-further-round-makes-INV-6-read-revises-3,so-it-waits-for-the-operator-s-decision-D-S2-374-3(default-A:one-round-that-ends-the-class-by-allowlist:env--i-with-an-explicit-PATH/HOME/agmsg-variable-allowlist-for-the-probe-and-the-checker,plus--I-on-the-probe);hold previous_head=6ae8cf75df74bb54eb3b724ea7c94e16b70759ef next_action=none-until-the-decision read_at=read
   102	- AGMSG-ACCEPTANCE v1 task_id=dotfiles-T128-orchestrator-tools-followup-a03 round=3 status=revise reason=operator-decision-D-S2-374-3-A(AskUserQuestion,plan-022:S2-waived):one-round-that-ends-the-class-by-allowlist,not-denylist:run-the-import-yaml-probe-and-the-checker-under-env--i-with-an-explicit-allowlist(PATH-as-the-script-computes-it,HOME,LANG/LC_ALL-if-needed,the-AGMSG_*-variables-the-scripts-read,and-nothing-else),the-probe-with-python-s--I,keeping-the-pinned---python,--no-project-and-the-cd-to-the-root;one-test-that-plants-every-caller-state-source-at-once(a-caller-pyproject,a-cwd-.python-version,VIRTUAL_ENV,CONDA_PREFIX,UV_PYTHON-and-a-yaml.py-on-PYTHONPATH)and-asserts-the-fake-uv-and-the-probe-see-only-the-allowlisted-variables;nothing-else;commit,push,@codex-review,RESULT-naming-4300102967-fixed:<sha>-and-the-test check=tests/unit/test_orchestrator_tools.py(the-new-or-extended-test,named-in-the-RESULT) previous_head=6ae8cf75df74bb54eb3b724ea7c94e16b70759ef next_action=fix-round,commit,push,@codex-review,RESULT read_at=read
   103	- AGMSG-ACCEPTANCE v1 task_id=dotfiles-T128-orchestrator-tools-followup-a03 round=4 status=pending-integration reason=RESULT-round-4-read:head-9cf65c02,4300102967-fixed:b18698d5(the-allowlist-form:env--i-with-PATH,HOME,LANG/LC_ALL,AGMSG_*;python--I-on-the-probe),13-mutants,CI-13-pass,the-Bot-s-re-review-clean;the-chain-runs-after-PR-376-s(one-chain-at-a-time;main-moved,so-update-branch-first);nothing-to-do-on-your-side;you-are-free previous_head=9cf65c0299645e30e54419668ba523eff9c4897e next_action=none-for-this-task read_at=read
     1	---
     2	task_id: dotfiles-T128-orchestrator-tools-followup-a03
     3	seat: claude-standard-dot-a003
     4	permission_gated_commands: 30
     5	---
     6	
     7	# Sandbox record: dotfiles-T128-orchestrator-tools-followup-a03
     8	
     9	Period: from the AGMSG-TASK (2026-10-16T08:28:10Z) to the RESULT. These ran inside the sandbox: the fetch, the branch, the task copy with its hash (read from the main checkout), the reads, the edits, the tests, shellcheck, shfmt, ruff, the mutation proofs, the repository validator and the commits.
    10	
    11	`permission_gated_commands` counts every Bash call made with `dangerouslyDisableSandbox`, one per call, and each `agmsg-dispatch`. This is the main-checkout copy with the final count: fourteen calls. Calls 1 to 13 have run when this copy is written (this copy is call 13), and call 14 is the RESULT that follows it.
    12	
    13	| # | Command | Step 4 case |
    14	|--:|---|---|
    15	| 1 | the HTTPS push of `tools/dispatch-checker-window` | `git push` |
    16	| 2 | `gh pr create --draft` and `gh pr ready` (PR #374) | `gh` |
    17	| 3 | `gh pr checks 374 --watch` with the Bot wait beside it (background) | `gh` |
    18	| 4 | `gh api` read of the Bot's summary, review comments and reactions (the security review still running) | `gh` |
    19	| 5 | `gh api` wait until the Bot's security review of `aeb4a0fb` completed, and the re-read | `gh` |
    20	| 6 | `agmsg-dispatch … AGMSG-PONG v1 task_id=dotfiles-T128-orchestrator-tools-followup-a03 status=alive …`, the answer to the PING of 21:38:05Z | `agmsg-dispatch` |
    21	| 7 | the HTTPS push of the fix round's head | `git push` |
    22	| 8 | `gh pr comment 374 --body '@codex review'` | `gh` |
    23	| 9 | `gh pr checks 374 --watch` with the Bot wait beside it on the fix head (background) | `gh` |
    24	| 10 | `gh api` wait until the Bot's code re-review of `57d3577c` completed (the wait script ended on the summary comment first), and the read of the reviews, comments and reactions | `gh` |
    25	| 11 | `gh api repos/mryfmo/dotfiles/pulls/comments/4299651928` (the new P1's body) | `gh` |
    26	| 12 | main-checkout `memory add` | main-checkout `memory add` |
    27	| 13 | the masked copy of the evidence files to the main checkout | artifact copy with the repository masker |
    28	| 14 | `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T128-orchestrator-tools-followup-a03 …` | `agmsg-dispatch` |
    29	
    30	**Revise round 2, the final count: nineteen calls.** Round 1's fourteen, and round 2's five: the branch copy counted six in advance, but the re-check of the Bot (its row 18) ran inside the wait call (row 17), so it is not a call of its own.
    31	
    32	| # | Command | Step 4 case |
    33	|--:|---|---|
    34	| 15 | the HTTPS push of `9df6b0c7` | `git push` |
    35	| 16 | `gh pr comment 374 --body '@codex review'` (issue comment 6225721682) | `gh` |
    36	| 17 | `gh pr checks 374 --watch`, then the `gh api` wait until the Bot's code re-review of `9df6b0c7` completed, and the read of its reviews, comments and reactions (background) | `gh` |
    37	| 18 | the round-2 sections copied into the main-checkout records, masked again | artifact copy with the repository masker |
    38	| 19 | `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T128-orchestrator-tools-followup-a03 round=2 …` | `agmsg-dispatch` |
    39	
    40	**Revise round 3, the final count: twenty-five calls.** Round 2's nineteen, and round 3's six: the branch copy counted five in advance, and the read of the new P1 thread's body (row 23) is the sixth.
    41	
    42	| # | Command | Step 4 case |
    43	|--:|---|---|
    44	| 20 | the HTTPS push of `6ae8cf75` | `git push` |
    45	| 21 | `gh pr comment 374 --body '@codex review'` (issue comment 6226303513) | `gh` |
    46	| 22 | `gh pr checks 374 --watch`, then the `gh api` wait until the Bot's code re-review of `6ae8cf75` completed, and the read of its reviews, comments and reactions (background) | `gh` |
    47	| 23 | `gh api repos/mryfmo/dotfiles/pulls/comments/4300102967` (the new P1's body) and the non-passing check filter | `gh` |
    48	| 24 | the round-3 sections copied into the main-checkout records, masked again | artifact copy with the repository masker |
    49	| 25 | `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T128-orchestrator-tools-followup-a03 round=3 …` | `agmsg-dispatch` |
    50	
    51	**Revise round 4, the final count: thirty calls.** Round 3's twenty-five, and round 4's five, as the branch copy counted them in advance (the Bot left no new thread, so there was no thread body to read).
    52	
    53	| # | Command | Step 4 case |
    54	|--:|---|---|
    55	| 26 | the HTTPS push of `9cf65c02` | `git push` |
    56	| 27 | `gh pr comment 374 --body '@codex review'` (issue comment 6226597044) | `gh` |
    57	| 28 | `gh pr checks 374 --watch`, then the `gh api` wait until the Bot's code re-review of `9cf65c02` completed, and the read of its reviews, comments, reactions and any new thread's body (background) | `gh` |
    58	| 29 | the round-4 sections copied into the main-checkout records, masked again | artifact copy with the repository masker |
    59	| 30 | `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T128-orchestrator-tools-followup-a03 round=4 …` | `agmsg-dispatch` |

**Ensuring output hygiene and environment safety**
**Analyzing PATH alignment and audit independence**
mcp: codex_apps/github.fetch started
mcp: codex_apps/github.fetch_commit_workflow_runs started
mcp: codex_apps/github.fetch_commit_workflow_runs (completed)
mcp: codex_apps/github.fetch (completed)
**Assessing token usage and code comparison**
exec
/bin/zsh -lc "git show ef74eaea9a94bff388b7c1027551a57797407b2f:tests/unit/test_orchestrator_tools.py | sed -n '1,260p'; git show ef74eaea9a94bff388b7c1027551a57797407b2f:scripts/orchestrator/task-consistency-check.py | sed -n '1,260p'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc "nl -ba ~/.agents/skills/agmsg/scripts/history.sh | sed -n '1,240p'; git show ef74eaea9a94bff388b7c1027551a57797407b2f:.orchestration/dotfiles-T128-orchestrator-tools-followup-a03/revise.yaml; nl -ba .orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a04.md | tail -n 70" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 54ms:
"""Exercise the scripts under scripts/orchestrator/ with stubbed host binaries.

Each script runs as a subprocess from its copy in a temporary git repository, with `agmsg-dispatch`, `shasum`,
`uv`, `gh`, `make`, `codex` and an interpreter `gate-python` stubbed on PATH and `history.sh` stubbed in the directory `AGMSG_SCRIPTS` names;
git is the real one, against a bare repository standing in for `origin`. A stub records its argv NUL-separated,
so an argument is compared byte for byte (`gh` and `make` append one line per call).
The dispatch checker case alone replaces the `uv` stub with a logging wrapper around the real `uv` next on PATH, so
the module needs a real uv with PyYAML in its cache or reachable index for that case.
"""

import fcntl
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from datetime import UTC, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "scripts/orchestrator"
RECORD = 'printf \'%s\\0\' "$@" > "$CALLS/{name}"\n'
# A run records its argv, cwd and environment, prints {name}-output and fails while {name}-fails exists.
RUN = RECORD + 'pwd -P > "$CALLS/{name}-cwd"\n/usr/bin/env > "$CALLS/{name}-env"\n'
RUN += '/bin/cat "$CALLS/{name}-output" 2> /dev/null\n[[ ! -f "$CALLS/{name}-fails" ]] || exit 2\n'
STUBS = {
    "agmsg-dispatch": "#!/usr/bin/env bash\n"
    + RECORD.format(name="agmsg-dispatch")
    # A send puts its row on the stub bus with the marker in dispatch-marker; dispatch-fails sends nothing.
    + '[[ -f "$CALLS/dispatch-fails" ]] && exit 1\n'
    + '[[ -f "$CALLS/dispatch-marker" ]] && printf "  %s [2026-10-13T03:00:00Z] %s → %s: %s\\n" '
    + '"$(cat "$CALLS/dispatch-marker")" "$2" "$3" "$5" >> "$CALLS/history"\nexit 0\n',
    "shasum": '#!/usr/bin/env python3\nimport hashlib, sys\np = sys.argv[-1]\nprint(hashlib.sha256(open(p, "rb").read()).hexdigest() + "  " + p)\n',
    # As uv does, a .python-version in the cwd that names an executable runs it.
    "uv": "#!/bin/bash\n"
    + 'pv="$(cat .python-version 2> /dev/null)" && [[ -x ${pv} ]] && exec "${pv}" "$@"\n'
    + RUN.format(name="uv"),
    "gate-python": "#!/bin/bash\n" + RUN.format(name="gate-python"),
    "gh": '#!/usr/bin/env bash\necho "$*" >> "$CALLS/gh.log"\n[[ "$1 $2" != "pr create" ]] || echo https://github.test/pull/9\n',
    "make": '#!/usr/bin/env bash\necho "$*" >> "$CALLS/make.log"\n[[ ! -f "$CALLS/make-fails" ]] || exit 2\n',
    # codex reads its stdin to the end (empty when the caller closed it) and writes its -o file.
    "codex": "#!/usr/bin/env bash\n"
    + RECORD.format(name="codex")
    + 'cat > "$CALLS/codex-stdin"\nwhile (($#)); do [[ $1 != -o ]] || out=$2; shift; done\n'
    # codex-silent writes no -o file; codex-stale writes one dated 2000.
    + '[[ -z ${out:-} || -f "$CALLS/codex-silent" ]] || echo "Verdict: correct" > "$out"\n'
    + '[[ -z ${out:-} || ! -f "$CALLS/codex-stale" ]] || touch -t 200001010000 "$out"\n'
    + 'echo transcript\nexit "$(cat "$CALLS/codex-status" 2> /dev/null || echo 0)"\n',
}
GIT_ENV = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
HISTORY_SH = "#!/usr/bin/env bash\n" + RECORD.format(name="history.sh") + 'cat "$CALLS/history"\n'


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


class OrchestratorToolsTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.temp = Path(temp.name).resolve()
        self.repo = self.temp / "repo"
        self.repo.mkdir()
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        shutil.copytree(TOOLS, self.repo / "scripts/orchestrator")
        self.calls = self.temp / "calls"
        self.calls.mkdir()
        bin_dir, agmsg = self.temp / "bin", self.temp / "agmsg"
        for directory, stubs in ((bin_dir, STUBS), (agmsg, {"history.sh": HISTORY_SH})):
            directory.mkdir()
            for name, text in stubs.items():
                (directory / name).write_text(text)
                (directory / name).chmod(0o755)
        self.env = {
            **os.environ,
            "CALLS": str(self.calls),
            "AGMSG_SCRIPTS": str(agmsg),
            "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}",
            "TMPDIR": str(self.temp),
            **GIT_ENV,
        }

    def run_tool(self, name, *args, code=0, env=None, cwd=None, stdin=None):
        result = subprocess.run(
            ["bash", str(self.repo / "scripts/orchestrator" / name), *map(str, args)],
            capture_output=True,
            text=True,
            input=stdin,
            cwd=cwd or self.repo,
            env={**self.env, **(env or {})},
            timeout=30,
            check=False,
        )
        self.assertEqual(result.returncode, code, result.stderr)
        return result

    def call(self, name):
        path = self.calls / name
        return path.read_text().split("\0")[:-1] if path.exists() else None

    def git(self, *args, cwd=None):
        return subprocess.run(
            ["git", "-c", "commit.gpgsign=false", *args],
            cwd=cwd or self.repo,
            env={**os.environ, **GIT_ENV},
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()

    def origin(self, *files):
        """Commit the given repo files as main, and push it to a bare repository that is `origin`."""
        self.git("add", "--", *files)
        self.git("commit", "-q", "--allow-empty", "-m", "init")
        self.git("branch", "-M", "main")
        self.git("init", "-q", "--bare", str(self.temp / "origin.git"))
        self.git("remote", "add", "origin", str(self.temp / "origin.git"))
        self.git("push", "-q", "origin", "main")
        self.git("fetch", "-q", "origin")

    def write(self, rel, text):
        path = self.repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    # dispatch.sh

    def dispatch(self, line, code=0):
        self.write("line.txt", line + "\n")
        return self.run_tool("dispatch.sh", "team", "orch", "worker", "w5:pA", "line.txt", code=code)

    def test_dispatch_refuses_a_line_whose_sha256_field_does_not_match_its_file(self):
        self.write(".orchestration/tasks/t.md", "task\n")
        line = f"AGMSG-TASK v1 task_id=t task_file=.orchestration/tasks/t.md task_sha256={sha('other')}"
        result = self.dispatch(line, code=1)
        self.assertIn("task_sha256 mismatch", result.stderr)
        self.assertIsNone(self.call("agmsg-dispatch"))

    def test_dispatch_refuses_a_task_line_without_task_sha256_or_with_a_second_line(self):
        self.write(".orchestration/tasks/t.md", "task\n")
        for line, code, needle in (
            # Thread 4254163604: a TASK whose file is not hash-bound is never sent.
            ("AGMSG-TASK v1 task_id=t task_file=.orchestration/tasks/t.md", 1, "needs task_sha256="),
            (f"AGMSG-TASK v1 task_id=t task_sha256={sha('task' + chr(10))}", 1, "needs task_file="),
            ("AGMSG-TASK v1 task_id=t\nAGMSG-TASK v1 task_id=u", 2, "more than one line"),
            # Thread 4254107304: a blank line after the message is a second line, not a trailing newline.
            ("AGMSG-PING v1 task_id=t\n", 2, "more than one line"),
            # Thread 4256541716: command substitution would drop the NUL and send another line.
            ("AGMSG-PING v1 task_id=t\0 reason=check", 2, "holds a NUL byte"),
        ):
            with self.subTest(needle=needle, code=code):
                self.assertIn(needle, self.dispatch(line, code=code).stderr)
                self.assertIsNone(self.call("agmsg-dispatch"))

    def test_dispatch_passes_the_line_byte_identical(self):
        # Run from another checkout: a relative task_file= is the script's own checkout's (thread 4253994697).
        pr = self.temp / "pr"
        subprocess.run(["git", "init", "-q", str(pr)], check=True)
        self.write(".orchestration/tasks/t.md", "task\n")
        self.write("design.md", "design\n")
        line = (
            f"AGMSG-TASK v1 task_id=t task_file=.orchestration/tasks/t.md task_sha256={sha('task' + chr(10))}"
            f" design=design.md design_sha256={sha('design' + chr(10))}"
            # Thread 4256541725: a reference to the previous design, checked as hex and never recomputed.
            f" previous_design_sha256={sha('old design')} note=a;b(c)`d`$(e)"
        )
        self.write("line.txt", line + "\n")
        self.run_tool("dispatch.sh", "team", "orch", "worker", "w5:pA", str(self.repo / "line.txt"), cwd=pr)
        self.assertEqual(["team", "orch", "worker", "w5:pA", line], self.call("agmsg-dispatch"))

    def test_dispatch_refuses_a_line_without_a_task_id(self):
        # Thread 4254893065: a message without exactly one non-empty task_id= is never sent, nor recorded.
        record = self.write(".orchestration/acceptance/t.md", '---\n{"task": "t"}\n---\n')
        before = record.read_text()
        for line in (
            "AGMSG-PING v1 reason=check",
            "AGMSG-PING v1 task_id= reason=check",
            "AGMSG-ACCEPTANCE v1 task_id=t task_id=u status=accepted",
        ):
            with self.subTest(line=line):
                self.write("line.txt", line + "\n")
                result = self.run_tool(
                    "dispatch.sh", "team", "orch", "worker", "w5:pA", "line.txt", str(record), code=1
                )
                self.assertIn("exactly one non-empty task_id=", result.stderr)
                self.assertIsNone(self.call("agmsg-dispatch"))
                self.assertEqual(before, record.read_text())

    def test_dispatch_refuses_malformed_lines(self):
        for line, code, needle in (
            ("hello task_id=t", 2, "not an AGMSG-TASK"),
            (f"AGMSG-ACCEPTANCE v1 task_id=t amended_task_sha256={sha('x')}", 1, "amended_task_sha256 has no"),
            ("AGMSG-ACCEPTANCE v1 task_id=t design=d.md design_sha256=abc", 1, "not 64 lowercase hex"),
            ("AGMSG-ACCEPTANCE v1 task_id=t previous_design_sha256=abc", 1, "previous_design_sha256 is not 64"),
            # Thread 4254771302: a hash field whose name has a digit is checked like any other.
            (
                f"AGMSG-ACCEPTANCE v1 task_id=t a02_expected=x.md a02_expected_sha256={sha('x')}",
                1,
                "a02_expected_sha256: ",
            ),
            # Thread 4254494989: a repeated source key leaves an unhashed second path in the line.
            (
                f"AGMSG-TASK v1 task_id=t task_file=.orchestration/tasks/t.md task_file=other.md task_sha256={sha('task' + chr(10))}",
                1,
                "task_file= appears more than once",
            ),
            # Thread 4254399800: a line naming the file both ways could bind the wrong artifact.
            (
                f"AGMSG-ACCEPTANCE v1 task_id=t design=d.md design_file=e.md design_sha256={sha('x')}",
                1,
                "both design_file= and design=",
            ),
        ):
            with self.subTest(needle=needle):
                self.assertIn(needle, self.dispatch(line, code=code).stderr)
                self.assertIsNone(self.call("agmsg-dispatch"))

    @staticmethod
    def gate_block(path):
        """The record's block, loaded as the gate does: standard json, duplicate keys and NaN refused."""

        def refuse(pairs):
            keys = [k for k, _ in pairs]
            assert len(keys) == len(set(keys)), keys
            return dict(pairs)

        def constant(name):
            raise AssertionError(f"non-finite number {name}")

        text = path.read_text()
        assert text.startswith("---\n"), text
        end = text.index("\n---\n", 3)
        return json.loads(text[4:end], object_pairs_hook=refuse, parse_constant=constant), text[end + 5 :]

    def test_dispatch_records_the_sent_line_with_its_read_marker(self):
        # Thread 4254107312: the a04 rule's dispatch: key, written after the send.
        record = self.write(
            ".orchestration/acceptance/t.md", '---\n{"format": 1, "task": "t", "ledger": []}\n---\n\nProse.\n'
        )
        ping = "AGMSG-PING v1 task_id=t reason=check"
        # Thread 4254399807: an older identical row on the bus is not this send.
        (self.calls / "history").write_text(f"  ● [2026-10-12T00:00:00Z] orch → worker: {ping}\n")
        (self.calls / "dispatch-marker").write_text("○")
        self.write("line.txt", ping + "\n")
        inode = record.stat().st_ino
        self.run_tool("dispatch.sh", "team", "orch", "worker", "w5:pA", "line.txt", str(record))
        # Thread 4254844595: the record is replaced whole (a new inode), never rewritten in place.
        self.assertNotEqual(inode, record.stat().st_ino)
        self.assertEqual(["t.md"], sorted(p.name for p in record.parent.iterdir()))
        block, prose = self.gate_block(record)
        self.assertEqual({"dispatch": [f"{ping} read_at=read"], "format": 1, "ledger": [], "task": "t"}, block)
        self.assertEqual("\nProse.\n", prose)
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
    for sent in sentences:  # C10
        for scr in set(re.findall(r"scripts/[\w./-]+\.(?:sh|py)", sent)):
            if git(root, "cat-file", "-e", f"origin/main:{scr}").returncode:
                continue
            m = re.search(r"\b(once|until)\b", sent, re.IGNORECASE)
            if m and scr in sent[m.start() :]:
                continue  # the script is named inside its own landing clause
            test = f"tests/unit/test_{pathlib.Path(scr).stem.replace('-', '_')}.py"
            for lit in set(re.findall(r"`([^`]*(?:=|\[[^\]]+\])[^`]*)`", sent)):
                if git(root, "grep", "-qF", lit, "origin/main", "--", scr, test).returncode:
                    why = f"which neither the script nor {test} carries on origin/main"
                    fails.append(f'C10 rule sentence names {scr} beside the literal `{lit}`, {why}: "{sent[:60]}…"')
    for sent in sentences:  # C9
        if re.search(r"\b(once|until)\b", sent):
            continue
        for n in set(re.findall(C9_NAMES, sent)):
            probe = n.replace("task-consistency-check ", f"{CHECKER}#").split("#")[0]
            if probe.startswith("scripts/"):
                ok = git(root, "cat-file", "-e", f"origin/main:{probe}").returncode == 0
            elif probe.endswith("_EVIDENCE"):
                ok = git(root, "grep", "-q", probe, "origin/main", "--", "scripts", "Makefile").returncode == 0
            else:
                mistakes = ("grep", "-q", "^classes:", "origin/main", "--", ".orchestration/learning/mistakes")
                ok = probe == "classes:" and git(root, *mistakes).returncode == 0
            if not ok:
                why = "it is not on origin/main and the sentence has no landing condition"
                fails.append(f'C9 rule sentence names {n} as present but {why}: "{sent[:70]}…"')
    return fails


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=pathlib.Path, help="the repository (default: the first file's git toplevel)")
    parser.add_argument("tasks", nargs="+", type=pathlib.Path, metavar="task.md")
    args = parser.parse_args()
    if args.root is None:
        top = git(args.tasks[0].parent, "rev-parse", "--show-toplevel")
        if top.returncode:
            parser.error(f"{args.tasks[0]} is not in a git checkout; pass --root")
        args.root = pathlib.Path(top.stdout.strip())
    rc = 0
    for p in args.tasks:
        fails = check(p, args.root)
        print(f"{p.name}: {'FAIL' if fails else 'OK'}", *fails, sep="\n  ")
        rc |= bool(fails)
    return rc


if __name__ == "__main__":
    sys.exit(main())

 succeeded in 103ms:
     1	#!/usr/bin/env bash
     2	set -euo pipefail
     3	
     4	# Usage: history.sh <team> [agent_id] [limit]
     5	# Shows message history. If agent_id given, shows only that agent's messages.
     6	
     7	TEAM="${1:?Usage: history.sh <team> [agent_id] [limit]}"
     8	AGENT="${2:-}"
     9	LIMIT="${3:-20}"
    10	# A non-numeric limit would otherwise be interpolated straight into the SQL
    11	# text below (e.g. "1; DELETE FROM messages; --"); fall back to the default
    12	# rather than passing it through, mirroring the interval-validation idiom
    13	# used elsewhere (config.sh, watch.sh).
    14	case "$LIMIT" in ''|*[!0-9]*) LIMIT=20 ;; esac
    15	
    16	SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
    17	source "$SCRIPT_DIR/lib/storage.sh"
    18	agmsg_storage_load
    19	
    20	# A seat that reads history as itself names its own pane if it is not named
    21	# (self-name.sh); see send.sh. Only when an agent is given: without one this
    22	# is a team-wide read by nobody in particular.
    23	if [ -n "$AGENT" ]; then
    24	  # shellcheck disable=SC1091
    25	  source "$SCRIPT_DIR/lib/self-name.sh"
    26	  agmsg_self_name_on_action "$TEAM" "$AGENT"
    27	  # Fix its own CLI session name once, early (self-rename.sh, #1081). Best-effort.
    28	  # shellcheck disable=SC1091
    29	  source "$SCRIPT_DIR/lib/self-rename.sh"
    30	  agmsg_self_rename_on_action "$TEAM" "$AGENT"
    31	fi
    32	
    33	# A history read must not create a store, so a team that has never been written
    34	# to has no file yet. Since the stores split per team that is the ordinary state
    35	# of a freshly joined team rather than a broken install, and it reads out the
    36	# same as an empty history. Driver-level, so it works for jsonl too.
    37	if ! storage_store_exists "$TEAM"; then
    38	  echo "No message history."
    39	  exit 0
    40	fi
    41	
    42	# History (events ∪ legacy) via the facade; <agent> optional — omitted = whole
    43	# team (§2.1). The driver returns the most recent --limit records already in
    44	# chronological order, so no reversal here.
    45	HIST_JSONL=$(storage_history "$TEAM" "$AGENT" --limit "$LIMIT")
    46	
    47	if [ -z "$HIST_JSONL" ]; then
    48	  echo "No message history."
    49	  exit 0
    50	fi
    51	
    52	# Parse to "from \x1f to \x1f body \x1f at \x1f id" rows (no jq; cf. lib/hooks-json.sh).
    53	# The quote is held in a variable, never written as \' in the pattern: bash 3.2
    54	# (macOS /bin/bash) keeps the backslash of a \' REPLACEMENT, so the inline form
    55	# doubles a quote into \'\' there while producing '' on bash 4+. Same shape as
    56	# _sqlite_sync_lit_into in sqlite-sync.sh, which documents the same hazard.
    57	_AGMSG_SQ="'"
    58	_arr="[$(printf '%s' "$HIST_JSONL" | paste -sd, -)]"
    59	# #777: same argv-length exposure on the display path. Capping --limit does not bound this
    60	# one either, because a single long body can carry it past the ceiling on its own.
    61	_agmsg_rows_sql=$(mktemp "${TMPDIR:-/tmp}/agmsg-history-rows.XXXXXX") || exit 13
    62	trap 'rm -f "$_agmsg_rows_sql"' EXIT HUP INT TERM
    63	{
    64	  printf "%s\n" "SELECT json_extract(value,'\$.from') || char(31) ||"
    65	  printf "%s\n" "       json_extract(value,'\$.to') || char(31) ||"
    66	  printf "%s\n" "       replace(replace(json_extract(value,'\$.body'), char(10), '\n'), char(9), '\t') || char(31) ||"
    67	  printf "%s\n" "       json_extract(value,'\$.at') || char(31) ||"
    68	  printf "%s\n" "       json_extract(value,'\$.id')"
    69	  printf "FROM json_each('"
    70	  printf '%s' "${_arr//$_AGMSG_SQ/$_AGMSG_SQ$_AGMSG_SQ}"
    71	  printf "');\n"
    72	} > "$_agmsg_rows_sql"
    73	# Windows sqlite3.exe may treat redirected stdin as interactive input unless
    74	# batch mode is explicit, returning success without evaluating the SQL. Keep
    75	# the stdin path (it avoids command-line length limits) and make the mode
    76	# explicit on every platform.
    77	ROWS=$(agmsg_sqlite -batch ':memory:' < "$_agmsg_rows_sql")
    78	rm -f "$_agmsg_rows_sql"
    79	trap - EXIT HUP INT TERM
    80	
    81	# Read-state for the ●(unread)/○(read) marker (G2(c)): read-state is
    82	# recipient-scoped and not carried on a history record, so derive it by unioning
    83	# storage_list_unread over the distinct recipients in this slice. (Phase 1:
    84	# mark-read still lands in legacy read_at, which the facade UNION reflects.)
    85	RECIPIENTS=$(while IFS=$'\x1f' read -r _f to _rest; do
    86	  [ -n "$to" ] && printf '%s\n' "$to"
    87	done <<< "$ROWS" | sort -u)
    88	
    89	UNREAD_IDS=""
    90	while IFS= read -r r; do
    91	  [ -n "$r" ] || continue
    92	  u=$(storage_list_unread "$TEAM" "$r") || continue
    93	  [ -n "$u" ] || continue
    94	  uarr="[$(printf '%s' "$u" | paste -sd, -)]"
    95	  # #777: a recipient's unread backlog grows independently of the display limit, so
    96	  # interpolating it into one argv element eventually exceeds the ceiling on a SINGLE
    97	  # argument -- on Linux `MAX_ARG_STRLEN`, 131,072 bytes. Measured: the failing
    98	  # statement for a 2,079-message team was 125,945 bytes, which is nowhere near
    99	  # `ARG_MAX` (2,097,152 here) because ARG_MAX bounds argv plus environment in total,
   100	  # not any one element of it. The distinction decides the repair: splitting one long
   101	  # statement into several shorter arguments satisfies MAX_ARG_STRLEN and leaves
   102	  # ARG_MAX untouched, and a reader who has the wrong limit in mind reaches for the
   103	  # wrong fix. Note also that MAX_ARG_STRLEN is a kernel constant with no getconf key,
   104	  # so the limit that bites is the one the tools cannot show you.
   105	  #
   106	  # Pass the statement on stdin instead, mirroring drivers/storage/sqlite-sync.sh:1082.
   107	  # printf is a bash builtin, so feeding it a large value does not exec at all and can
   108	  # hit neither ceiling.
   109	  _agmsg_unread_sql=$(mktemp "${TMPDIR:-/tmp}/agmsg-history-unread.XXXXXX") || continue
   110	  trap 'rm -f "$_agmsg_unread_sql"' EXIT HUP INT TERM
   111	  {
   112	    printf "SELECT json_extract(value,'\$.id') FROM json_each('"
   113	    printf '%s' "${uarr//$_AGMSG_SQ/$_AGMSG_SQ$_AGMSG_SQ}"
   114	    printf "');\n"
   115	  } > "$_agmsg_unread_sql"
   116	  ids=$(agmsg_sqlite -batch ':memory:' < "$_agmsg_unread_sql")
   117	  rm -f "$_agmsg_unread_sql"
   118	  trap - EXIT HUP INT TERM
   119	  UNREAD_IDS+="$ids"$'\n'
   120	done <<< "$RECIPIENTS"
   121	
   122	while IFS=$'\x1f' read -r from to body ts id; do
   123	  [ -n "$ts$from$to$body" ] || continue
   124	  if printf '%s\n' "$UNREAD_IDS" | grep -Fxq "$id"; then status='●'; else status='○'; fi
   125	  echo "  $status [$ts] $from → $to: $body"
   126	done <<< "$ROWS"
task_id: dotfiles-T128-orchestrator-tools-followup-a03
round: 4
previous_head: 6ae8cf75df74bb54eb3b724ea7c94e16b70759ef
check: tests/unit/test_orchestrator_tools.py::test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state
reason: the Bot's P1 4300102967 on 6ae8cf75, the operator's decision D-S2-374-3 A; the import yaml probe ran without -I, so an inherited PYTHONPATH could load a caller's yaml.py, the fourth finding of the class; both uv forms now run under an env -i allowlist and the probe with -I
earlier:
  - round: 3
    previous_head: 9df6b0c7594cef7f42e9a43faa3e08d0f035e329
    check: tests/unit/test_orchestrator_tools.py::test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state
  - round: 2
    previous_head: 57d3577ca780248f573fd26c4fa460e2b5e2d510
    check: tests/unit/test_orchestrator_tools.py::test_dispatch_refuses_a_task_file_failing_the_checker
nl: .orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a04.md: No such file or directory

**Investigating missing task file in git refs**
exec
/bin/zsh -lc "git show ef74eaea9a94bff388b7c1027551a57797407b2f:.orchestration/dotfiles-T128-orchestrator-tools-followup-a03/validation.md | sed -n '1,220p'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc "git rev-parse origin/main; git ls-tree -r --name-only origin/main .orchestration/tasks/ | rg 'orchestrator-tools-followup-a04'; git log --oneline --decorate f7847616970d6bd83739a75a65ad8f7c35e91462..ef74eaea9a94bff388b7c1027551a57797407b2f; git diff --numstat f7847616970d6bd83739a75a65ad8f7c35e91462 ef74eaea9a94bff388b7c1027551a57797407b2f; rg -n 'storage_history|ORDER BY.*(at|created|timestamp)|sort_by|_at|at DESC' ~/.agents/skills/agmsg/scripts/drivers/storage/{sqlite.sh,sqlite-sync.sh,jsonl.sh}" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 30ms:
---
task_id: dotfiles-T128-orchestrator-tools-followup-a03
seat: claude-standard-dot-a003
commit: 766c1491
---

# Validation: dotfiles-T128-orchestrator-tools-followup-a03

## 1. Task copy, premises, tests, linters and size

The task copy hashes to the TASK line's `task_sha256`. The task file on `origin/main` (`1d418126`) hashes to `5a741e63…`, the pair-confirmed text before the `bot_rounds` change the task's last section records; the dispatched file is the main checkout's, which the Worker Playbook says to copy. The three premises replay with the task's outputs (1, 0, 52); on HEAD the same counts are 0, 2 and 54.

```text
$ shasum -a 256 .orchestration/dotfiles-T128-orchestrator-tools-followup-a03/task.md
b291ba85f89d46877f74969d4e33ce994ff875f83454df58dbd8037a7d745da7  .orchestration/dotfiles-T128-orchestrator-tools-followup-a03/task.md
$ git log --oneline -1; git merge-base HEAD origin/main
766c1491 fix(orchestrator): dispatch.sh refuses a task file that fails the checker and rea
1d418126
$ the three premises (origin/main)
1
0
52
$ the same counts on HEAD
0
2
54

$ GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false UV_OFFLINE=1 uv run --no-project python -m unittest tests/unit/test_orchestrator_tools.py -v
(rc=0)
test_acceptance_front_matter_binds_head_and_pr_and_keeps_the_record ... ok
test_acceptance_front_matter_takes_audit_findings_only_for_an_incorrect_audit ... ok
test_boundary_commits_pushes_and_queues_the_pr ... ok
test_boundary_deletes_a_deleted_file_and_a_renamed_files_old_path ... ok
test_boundary_deletes_a_name_with_glob_characters_literally ... ok
test_boundary_keeps_a_name_with_a_newline_one_path ... ok
test_boundary_stops_before_commit_when_the_validator_fails ... ok
test_bus_read_closes_a_task_on_any_non_revise_acceptance ... ok
test_bus_read_ignores_closers_between_other_endpoints ... ok
test_bus_read_lists_an_open_task_with_minutes_since_its_latest_event ... ok
test_bus_read_refuses_a_read_that_reaches_its_limit ... ok
test_bus_read_skips_and_counts_malformed_rows ... ok
test_codex_review_closes_stdin_fixes_the_profile_and_needs_the_hash ... ok
test_design_keydiff_names_the_changed_invariant ... ok
test_dispatch_line_grammar_table ... ok
test_dispatch_passes_the_line_byte_identical ... ok
test_dispatch_reads_a_bounded_history_window ... ok
test_dispatch_record_path_tokenizes_and_locks ... ok
test_dispatch_records_the_sent_line_with_its_read_marker ... ok
test_dispatch_refuses_a_line_whose_sha256_field_does_not_match_its_file ... ok
test_dispatch_refuses_a_line_without_a_task_id ... ok
test_dispatch_refuses_a_malformed_record_block_before_sending ... ok
test_dispatch_refuses_a_tab_separated_task_without_its_hash_fields ... ok
test_dispatch_refuses_a_task_file_failing_the_checker ... ok
test_dispatch_refuses_a_task_line_without_task_sha256_or_with_a_second_line ... ok
test_dispatch_refuses_an_unwritable_record_before_sending ... ok
test_dispatch_refuses_malformed_lines ... ok
test_ff_main_keeps_a_local_deletion_across_the_fast_forward ... ok
test_ff_main_keeps_local_edits_across_the_fast_forward ... ok
test_fill_sweep_fills_only_a_commented_review ... ok
test_fill_sweep_fills_only_notice_annotations_and_success_statuses ... ok
test_fill_sweep_ignores_a_disposition_reply_from_another_login ... ok
test_fill_sweep_leaves_a_badged_review_body_a_gap ... ok
test_fill_sweep_quotes_the_url_form_evidence ... ok
test_fill_sweep_refuses_a_not_applicable_without_evidence ... ok
test_fill_sweep_refuses_a_shared_url_key_and_takes_an_item_id ... ok
test_fill_sweep_sees_a_collision_after_the_discussion_r_strip ... ok
test_fill_sweep_selects_a_null_url_status_by_source_and_check ... ok
test_orch_audit_refuses_a_ledger_check_that_differs_from_head ... ok
test_orch_audit_refuses_a_run_that_leaves_no_fresh_receipt ... ok
test_orch_audit_runs_the_ledger_check_by_default_and_refuses_a_gap ... ok
test_orch_audit_runs_the_ledger_check_isolated_from_sibling_modules ... ok
test_orch_gate_leaves_the_review_worktree_as_it_was_on_a_refusal_before_the_checkout ... ok
test_orch_gate_pins_the_interpreter_before_entering_the_review_worktree ... ok
test_orch_gate_refuses_a_head_that_tracks_a_symlink_under_orchestration ... ok
test_orch_gate_refuses_another_prs_sweep_or_a_changed_gate_before_the_review_worktree_moves ... ok
test_orch_gate_restores_the_review_worktree_when_setup_fails ... ok
test_orch_gate_returns_the_gate_status_and_restores_the_review_worktree ... ok
test_orch_gate_runs_the_gate_under_an_explicit_environment ... ok
test_orch_gate_runs_this_checkouts_gate_on_the_review_worktree_with_the_gate_inputs ... ok
test_replay_propagates_the_command_status ... ok
test_three_repeat_prints_body_matches_and_states_a_capped_memory_count ... ok
test_three_repeat_prints_the_records_search_line ... ok
test_three_repeat_rejects_a_class_that_is_not_a_slug_and_runs_the_cli_from_its_own_checkout ... ok
Ran 54 tests in 46.271s
OK

$ shellcheck scripts/orchestrator/dispatch.sh; shfmt --indent 4 --space-redirects -d scripts/orchestrator/dispatch.sh
(rc=0)
$ ruff check tests/unit/test_orchestrator_tools.py; ruff format --check tests/unit/test_orchestrator_tools.py
All checks passed!
1 file already formatted
(rc=0)

$ git diff --numstat origin/main...HEAD -- . ':!.orchestration'
81	23	scripts/orchestrator/dispatch.sh
107	11	tests/unit/test_orchestrator_tools.py
files: 2; changed lines outside tests/ and .orchestration/: 104; added under tests/: 107
```

## 2. Mutation proofs

Each mutant of `scripts/orchestrator/dispatch.sh` runs against the two new tests, and the file is restored after each (`a03-mutate.py`, a scratch script outside the repository).

```text
M1 the dispatch.sh of origin/main -> killed by test_dispatch_reads_a_bounded_history_window, test_dispatch_refuses_a_task_file_failing_the_checker
M2 the brief found by a literal kind: review line -> killed by test_dispatch_refuses_a_task_file_failing_the_checker
M3 no duplicate-key refusal -> killed by test_dispatch_refuses_a_task_file_failing_the_checker
M4 the first fitting shift, not a unique one -> killed by test_dispatch_reads_a_bounded_history_window
M5 the newest new row taken as the send -> killed by test_dispatch_reads_a_bounded_history_window
M6 the whole bus read again -> killed by test_dispatch_reads_a_bounded_history_window
M7 no EXIT trap -> killed by test_dispatch_reads_a_bounded_history_window
file restored (git diff --quiet HEAD): True
```

## 3. The two existing tests the change touches

The task keeps the 52 tests, and item 1b removes the cap refusal and `BUS_READ_LIMIT`. Two of the 52 asserted exactly those, so each changes as little as the removal needs:

- `test_dispatch_records_the_sent_line_with_its_read_marker`: the history limit it asserts is `200`, the new default, instead of `100000`.
- `test_dispatch_record_path_tokenizes_locks_and_refuses_a_capped_history`: its last case (a read that reaches `BUS_READ_LIMIT` is refused) is removed with the refusal, and the test is renamed `test_dispatch_record_path_tokenizes_and_locks`, since it no longer refuses a capped history. Its other cases stay as they were.

Neither change weakens a check that still exists; the bounded window is covered by the new `test_dispatch_reads_a_bounded_history_window`.

## 4. The Bot's fix round (`c8e813ea`): `--no-project`

The Bot's code review of `aeb4a0fb` (review 5545290170) left one P1, thread 4292675906 at `scripts/orchestrator/dispatch.sh:181`: without `--no-project`, both `uv run` forms discover and sync a `pyproject.toml` in the caller's directory before the task file is checked, so a build backend there could run. Its security review of the same head completed with no finding. `c8e813ea` adds `--no-project` to both forms. The checker test now sends the review brief from a directory whose `pyproject.toml` depends on a package that does not exist, and pins the probe as `run --no-project --offline --with pyyaml python -c import yaml`. Mutant M8 drops `--no-project`; the send is then refused because the brief parse cannot run, so the test fails on the exit code, not only on the probe string.

```text
$ shasum -a 256 .orchestration/dotfiles-T128-orchestrator-tools-followup-a03/task.md
b291ba85f89d46877f74969d4e33ce994ff875f83454df58dbd8037a7d745da7  .orchestration/dotfiles-T128-orchestrator-tools-followup-a03/task.md
$ git log --oneline -1; git merge-base HEAD origin/main
c8e813ea fix(orchestrator): dispatch.sh runs uv with --no-project (the Bot's P1 4292675906
1d418126
$ the three premises (origin/main)
1
0
52
$ the same counts on HEAD
0
2
54

$ GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false UV_OFFLINE=1 uv run --no-project python -m unittest tests/unit/test_orchestrator_tools.py -v
(rc=0)
test_acceptance_front_matter_binds_head_and_pr_and_keeps_the_record ... ok
test_acceptance_front_matter_takes_audit_findings_only_for_an_incorrect_audit ... ok
test_boundary_commits_pushes_and_queues_the_pr ... ok
test_boundary_deletes_a_deleted_file_and_a_renamed_files_old_path ... ok
test_boundary_deletes_a_name_with_glob_characters_literally ... ok
test_boundary_keeps_a_name_with_a_newline_one_path ... ok
test_boundary_stops_before_commit_when_the_validator_fails ... ok
test_bus_read_closes_a_task_on_any_non_revise_acceptance ... ok
test_bus_read_ignores_closers_between_other_endpoints ... ok
test_bus_read_lists_an_open_task_with_minutes_since_its_latest_event ... ok
test_bus_read_refuses_a_read_that_reaches_its_limit ... ok
test_bus_read_skips_and_counts_malformed_rows ... ok
test_codex_review_closes_stdin_fixes_the_profile_and_needs_the_hash ... ok
test_design_keydiff_names_the_changed_invariant ... ok
test_dispatch_line_grammar_table ... ok
test_dispatch_passes_the_line_byte_identical ... ok
test_dispatch_reads_a_bounded_history_window ... ok
test_dispatch_record_path_tokenizes_and_locks ... ok
test_dispatch_records_the_sent_line_with_its_read_marker ... ok
test_dispatch_refuses_a_line_whose_sha256_field_does_not_match_its_file ... ok
test_dispatch_refuses_a_line_without_a_task_id ... ok
test_dispatch_refuses_a_malformed_record_block_before_sending ... ok
test_dispatch_refuses_a_tab_separated_task_without_its_hash_fields ... ok
test_dispatch_refuses_a_task_file_failing_the_checker ... ok
test_dispatch_refuses_a_task_line_without_task_sha256_or_with_a_second_line ... ok
test_dispatch_refuses_an_unwritable_record_before_sending ... ok
test_dispatch_refuses_malformed_lines ... ok
test_ff_main_keeps_a_local_deletion_across_the_fast_forward ... ok
test_ff_main_keeps_local_edits_across_the_fast_forward ... ok
test_fill_sweep_fills_only_a_commented_review ... ok
test_fill_sweep_fills_only_notice_annotations_and_success_statuses ... ok
test_fill_sweep_ignores_a_disposition_reply_from_another_login ... ok
test_fill_sweep_leaves_a_badged_review_body_a_gap ... ok
test_fill_sweep_quotes_the_url_form_evidence ... ok
test_fill_sweep_refuses_a_not_applicable_without_evidence ... ok
test_fill_sweep_refuses_a_shared_url_key_and_takes_an_item_id ... ok
test_fill_sweep_sees_a_collision_after_the_discussion_r_strip ... ok
test_fill_sweep_selects_a_null_url_status_by_source_and_check ... ok
test_orch_audit_refuses_a_ledger_check_that_differs_from_head ... ok
test_orch_audit_refuses_a_run_that_leaves_no_fresh_receipt ... ok
test_orch_audit_runs_the_ledger_check_by_default_and_refuses_a_gap ... ok
test_orch_audit_runs_the_ledger_check_isolated_from_sibling_modules ... ok
test_orch_gate_leaves_the_review_worktree_as_it_was_on_a_refusal_before_the_checkout ... ok
test_orch_gate_pins_the_interpreter_before_entering_the_review_worktree ... ok
test_orch_gate_refuses_a_head_that_tracks_a_symlink_under_orchestration ... ok
test_orch_gate_refuses_another_prs_sweep_or_a_changed_gate_before_the_review_worktree_moves ... ok
test_orch_gate_restores_the_review_worktree_when_setup_fails ... ok
test_orch_gate_returns_the_gate_status_and_restores_the_review_worktree ... ok
test_orch_gate_runs_the_gate_under_an_explicit_environment ... ok
test_orch_gate_runs_this_checkouts_gate_on_the_review_worktree_with_the_gate_inputs ... ok
test_replay_propagates_the_command_status ... ok
test_three_repeat_prints_body_matches_and_states_a_capped_memory_count ... ok
test_three_repeat_prints_the_records_search_line ... ok
test_three_repeat_rejects_a_class_that_is_not_a_slug_and_runs_the_cli_from_its_own_checkout ... ok
Ran 54 tests in 41.307s
OK

$ shellcheck scripts/orchestrator/dispatch.sh; shfmt --indent 4 --space-redirects -d scripts/orchestrator/dispatch.sh
(rc=0)
$ ruff check tests/unit/test_orchestrator_tools.py; ruff format --check tests/unit/test_orchestrator_tools.py
All checks passed!
1 file already formatted
(rc=0)

$ git diff --numstat origin/main...HEAD -- . ':!.orchestration'
82	23	scripts/orchestrator/dispatch.sh
114	11	tests/unit/test_orchestrator_tools.py
files: 2; changed lines outside tests/ and .orchestration/: 105; added under tests/: 114
```

```text
M1 the dispatch.sh of origin/main -> killed by test_dispatch_reads_a_bounded_history_window, test_dispatch_refuses_a_task_file_failing_the_checker
M2 the brief found by a literal kind: review line -> killed by test_dispatch_refuses_a_task_file_failing_the_checker
M3 no duplicate-key refusal -> killed by test_dispatch_refuses_a_task_file_failing_the_checker
M4 the first fitting shift, not a unique one -> killed by test_dispatch_reads_a_bounded_history_window
M5 the newest new row taken as the send -> killed by test_dispatch_reads_a_bounded_history_window

 succeeded in 140ms:
f7847616970d6bd83739a75a65ad8f7c35e91462
ef74eaea (pr/374, origin/tools/dispatch-checker-window) Merge branch 'main' into tools/dispatch-checker-window
9cf65c02 (tools/dispatch-checker-window) chore(orchestration): dotfiles-T128-orchestrator-tools-followup-a03 revise round 4 evidence
b18698d5 fix(orchestrator): dispatch.sh runs uv under an env -i allowlist and the PyYAML probe with -I (the Bot's P1 4300102967, operator decision D-S2-374-3 A)
6ae8cf75 chore(orchestration): dotfiles-T128-orchestrator-tools-followup-a03 revise round 3 evidence
411c7d68 fix(orchestrator): dispatch.sh runs uv on a pinned interpreter without the caller's environment (local:9df6b0c:1, operator decision D-S2-374-2 A)
9df6b0c7 chore(orchestration): dotfiles-T128-orchestrator-tools-followup-a03 revise round 2 evidence
8adf74bb fix(orchestrator): dispatch.sh runs uv from the trusted root (the Bot's P1 4299651928, operator decision D-P1-374 A)
57d3577c chore(orchestration): dotfiles-T128-orchestrator-tools-followup-a03 the Bot's fix round evidence
c8e813ea fix(orchestrator): dispatch.sh runs uv with --no-project (the Bot's P1 4292675906)
aeb4a0fb chore(orchestration): dotfiles-T128-orchestrator-tools-followup-a03 evidence
766c1491 fix(orchestrator): dispatch.sh refuses a task file that fails the checker and reads a bounded history window (T128 orchestrator-tools followup a03)
3	0	.orchestration/dotfiles-T128-orchestrator-tools-followup-a03/autoskill.md
7	0	.orchestration/dotfiles-T128-orchestrator-tools-followup-a03/learning.md
64	0	.orchestration/dotfiles-T128-orchestrator-tools-followup-a03/report.md
12	0	.orchestration/dotfiles-T128-orchestrator-tools-followup-a03/revise.yaml
58	0	.orchestration/dotfiles-T128-orchestrator-tools-followup-a03/sandbox.md
131	0	.orchestration/dotfiles-T128-orchestrator-tools-followup-a03/task.md
558	0	.orchestration/dotfiles-T128-orchestrator-tools-followup-a03/validation.md
101	23	scripts/orchestrator/dispatch.sh
153	11	tests/unit/test_orchestrator_tools.py
~/.agents/skills/agmsg/scripts/drivers/storage/sqlite.sh:228:      created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now')),
~/.agents/skills/agmsg/scripts/drivers/storage/sqlite.sh:229:      read_at TEXT
~/.agents/skills/agmsg/scripts/drivers/storage/sqlite.sh:233:    -- an exact audit marker without mutating read_at; event-log recipients start
~/.agents/skills/agmsg/scripts/drivers/storage/sqlite.sh:310:    INSERT INTO messages (team,from_agent,to_agent,body,created_at)
~/.agents/skills/agmsg/scripts/drivers/storage/sqlite.sh:375:      UPDATE messages SET read_at='$(_sqlite_lit "$at")'
~/.agents/skills/agmsg/scripts/drivers/storage/sqlite.sh:376:       WHERE read_at IS NULL
~/.agents/skills/agmsg/scripts/drivers/storage/sqlite.sh:454:               'from',m.from_agent,'to',m.to_agent,'body',m.body,'at',m.created_at) AS j,
~/.agents/skills/agmsg/scripts/drivers/storage/sqlite.sh:455:             m.created_at AS ts, 0 AS src, m.id AS ord
~/.agents/skills/agmsg/scripts/drivers/storage/sqlite.sh:457:      WHERE m.team='$tl' AND m.to_agent='$al' AND m.read_at IS NULL
~/.agents/skills/agmsg/scripts/drivers/storage/sqlite.sh:533:# storage_history <team> [agent] [--limit N]  — events ∪ legacy in time order.
~/.agents/skills/agmsg/scripts/drivers/storage/sqlite.sh:536:storage_history() {
~/.agents/skills/agmsg/scripts/drivers/storage/sqlite.sh:541:  # agent was given. This is what makes `storage_history <team> --limit N` and
~/.agents/skills/agmsg/scripts/drivers/storage/sqlite.sh:542:  # `storage_history <team>` parse correctly per the §2.1 contract (review).
~/.agents/skills/agmsg/scripts/drivers/storage/sqlite.sh:565:                 'from',from_agent,'to',to_agent,'body',body,'at',created_at) AS j,
~/.agents/skills/agmsg/scripts/drivers/storage/sqlite.sh:566:               created_at AS ts, 0 AS src, id AS ord
~/.agents/skills/agmsg/scripts/drivers/storage/sqlite.sh:624:        UPDATE messages SET read_at='$(_sqlite_lit "$at")'
~/.agents/skills/agmsg/scripts/drivers/storage/sqlite.sh:625:         WHERE read_at IS NULL
~/.agents/skills/agmsg/scripts/drivers/storage/sqlite-sync.sh:328:      server_received_at TEXT NOT NULL,
~/.agents/skills/agmsg/scripts/drivers/storage/sqlite-sync.sh:354:      observed_at TEXT NOT NULL,
~/.agents/skills/agmsg/scripts/drivers/storage/sqlite-sync.sh:369:      accepted_at TEXT NOT NULL,
~/.agents/skills/agmsg/scripts/drivers/storage/sqlite-sync.sh:530:       gap_end,reason,accepted_at)
~/.agents/skills/agmsg/scripts/drivers/storage/sqlite-sync.sh:606:             m.team,m.from_agent,m.to_agent,m.body,m.created_at,
~/.agents/skills/agmsg/scripts/drivers/storage/sqlite-sync.sh:817:           projection:{body:$row.body,created_at:$created,
~/.agents/skills/agmsg/scripts/drivers/storage/sqlite-sync.sh:1095:    def fields: ["type","next_after","server_seq","id","server_received_at",
~/.agents/skills/agmsg/scripts/drivers/storage/sqlite-sync.sh:1099:                 "projection.body","projection.created_at"];
~/.agents/skills/agmsg/scripts/drivers/storage/sqlite-sync.sh:1119:       elif $name == "server_received_at"      then $r.server_received_at // ""
~/.agents/skills/agmsg/scripts/drivers/storage/sqlite-sync.sh:1138:       else                                         $r.projection.created_at // ""
~/.agents/skills/agmsg/scripts/drivers/storage/sqlite-sync.sh:1220:         reason,observed_at)
~/.agents/skills/agmsg/scripts/drivers/storage/sqlite-sync.sh:1236:         reason,observed_at)
~/.agents/skills/agmsg/scripts/drivers/storage/sqlite-sync.sh:1257:         driver_generation,server_seq,wire_id,server_received_at,envelope_v,
~/.agents/skills/agmsg/scripts/drivers/storage/sqlite-sync.sh:1356:        INSERT INTO messages(team,from_agent,to_agent,body,created_at)
~/.agents/skills/agmsg/scripts/drivers/storage/sqlite-sync.sh:1479:      SELECT server_seq,wire_id,server_received_at,envelope_v,cipher,key_id,blob,status
~/.agents/skills/agmsg/scripts/drivers/storage/sqlite-sync.sh:1490:          'id',wire_id,'server_received_at',server_received_at,
~/.agents/skills/agmsg/scripts/drivers/storage/jsonl.sh:421:storage_history() {

**Parsing and summarizing GitHub job logs**
**Reviewing design scope and implementation status**
exec
/bin/zsh -lc "nl -ba .orchestration/tasks/dotfiles-T128-regime-v3-a01.md | sed -n '1,54p'; sed -n '60p' .orchestration/tasks/dotfiles-T128-regime-v3-a01.md; sed -n '92,141p' .orchestration/tasks/dotfiles-T128-regime-v3-a01.md; nl -ba ~/.agents/skills/agmsg/scripts/drivers/storage/sqlite.sh | sed -n '533,580p'; nl -ba ~/.agents/skills/agmsg/scripts/drivers/storage/jsonl.sh | sed -n '421,462p'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 56ms:
     1	---
     2	format: 2
     3	task_id: dotfiles-T128-regime-v3-a01
     4	kind: design
     5	security: true
     6	design_review:
     7	  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
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
    28	  dotfiles-T128-v0-main-tests-a02: [INV-12]
    29	  dotfiles-T128-gate-evidence-a01: [INV-6]
    30	  dotfiles-T128-gate-evidence-a02: [INV-6]
    31	  dotfiles-T128-gate-evidence-a03: [INV-6]
    32	  dotfiles-T128-gate-evidence-a04: [INV-6]
    33	supersedes:
    34	  - dotfiles-T126-regime-v2-a01
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
  INV-6: "the reset rule's mandatory point is the merge backstop in scripts/require-crit-review.py, with the orchestrator's Stop hook (Claude Stop hook, Codex [hooks].Stop) as the early signal, soft on both runtimes by their documented caps; counts come from history for the hook and the gate (revises = RESULTs for the task_id minus one, threshold 2; amendments = AGMSG-TASKs after the first, threshold 2; AGMSG-PONG status=question, threshold 2) and from GitHub and main-checkout files for the gate and the boundary check only (Codex Bot P0 or P1 on two heads after the first RESULT, from original_commit_id on review_comment items recorded by pr-feedback.py; an audit implementation or specification finding at P0-P1 on two heads, from .orchestration/validation/<task>-audit-<sha7>.json in the main checkout, each counted only when its sha256 matches its AGMSG-AUDIT record); when a count is reached the gate refuses the merge until a reset record names a redesign task whose design RESULT comes from an identity other than the task's author, or a waiver written by scripts/regime-waive.sh under the INV-1 ask-rule discipline into the state directory outside the sandbox write roots (the only release path besides a redesign; the one-account residual of INV-1 applies); check-regime-boundary.sh reports a closed-unmerged PR whose task has no reset record and a task over any count with neither an accepted acceptance record nor a reset record; the same gate refuses a merge whose acceptance record carries a not-applicable disposition without an evidence= clause, or a finding-class table with three rows of one class and no pasted search of the correction records (plan 007 S6)"
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
   533	# storage_history <team> [agent] [--limit N]  — events ∪ legacy in time order.
   534	# With <agent>, only rows where that agent is sender or recipient; omit it (empty)
   535	# for the whole team (§2.1 G3 — an additive widening, existing callers unchanged).
   536	storage_history() {
   537	  local team="$1"; shift
   538	  local agent="" limit=""
   539	  # <agent> is optional: consume a leading NON-flag argument as the agent (an
   540	  # empty string is allowed and also means team-wide). A leading --flag means no
   541	  # agent was given. This is what makes `storage_history <team> --limit N` and
   542	  # `storage_history <team>` parse correctly per the §2.1 contract (review).
   543	  if [ $# -gt 0 ] && [ "${1#-}" = "$1" ]; then agent="$1"; shift; fi
   544	  while [ $# -gt 0 ]; do case "$1" in --limit) limit="$2"; shift 2 ;; *) shift ;; esac; done
   545	  case "$limit" in ''|*[!0-9]*) limit="" ;; esac
   546	  storage_init "$team" >/dev/null
   547	  local tl al afilter; tl="$(_sqlite_lit "$team")"; al="$(_sqlite_lit "$agent")"
   548	  if [ -n "$agent" ]; then
   549	    afilter="AND (to_agent='$al' OR from_agent='$al')"
   550	  else
   551	    afilter=""
   552	  fi
   553	  # --limit returns the most RECENT N (inner DESC + LIMIT), re-sorted to
   554	  # chronological order for output — the intuitive "recent history" semantics,
   555	  # not the oldest N.
   556	  _sqlite_data "$team" "
   557	    SELECT j FROM (
   558	      SELECT j, ts, src, ord FROM (
   559	        SELECT json_object('type','message_sent','id',id,'team',team,'from',from_agent,
   560	                 'to',to_agent,'body',body,'at',at) AS j, at AS ts, 1 AS src, seq AS ord
   561	        FROM events
   562	        WHERE type='message_sent' AND team='$tl' $afilter
   563	        UNION ALL
   564	        SELECT json_object('type','message_sent','id',CAST(id AS TEXT),'team',team,
   565	                 'from',from_agent,'to',to_agent,'body',body,'at',created_at) AS j,
   566	               created_at AS ts, 0 AS src, id AS ord
   567	        FROM messages
   568	        WHERE team='$tl' $afilter
   569	          -- The event log already carries the mirrored copy (#689); listing
   570	          -- both shows one message twice.
   571	          AND NOT EXISTS (SELECT 1 FROM events e2 WHERE e2.legacy_id = messages.id)
   572	      )
   573	      ORDER BY ts DESC, src DESC, ord DESC ${limit:+LIMIT $limit}
   574	    )
   575	    ORDER BY ts ASC, src ASC, ord ASC;
   576	  "
   577	}
   578	
   579	# --- contract: export / import / compact -----------------------------------
   580	
   421	storage_history() {
   422	  _JSONL_TEAM="$1"
   423	  _jsonl_init_file || return 1
   424	  _jsonl_with_lock _jsonl_history_locked "$@"
   425	}
   426	
   427	_jsonl_history_locked() {
   428	  local team="$1"; shift
   429	  local agent="" limit=""
   430	  if [ $# -gt 0 ] && [ "${1#-}" = "$1" ]; then agent="$1"; shift; fi
   431	  while [ $# -gt 0 ]; do case "$1" in --limit) limit="$2"; shift 2 ;; *) shift ;; esac; done
   432	  case "$limit" in ''|*[!0-9]*) limit="-1" ;; esac
   433	  jq -c --arg team "$team" --arg agent "$agent" --argjson limit "$limit" -s '
   434	    def logical_events: .[] | if .type=="sync_pull_commit" then
   435	    .messages[]? | select(.status=="imported") | .local_event // empty else . end;
   436	    [logical_events | select(.type=="message_sent" and .team==$team
   437	            and ($agent=="" or .to==$agent or .from==$agent))
   438	     | {type:"message_sent",id:.id,team:.team,from:.from,to:.to,body:.body,at:.at}]
   439	    | (if $limit >= 0 and (length > $limit) then .[length-$limit:] else . end)
   440	    | .[]
   441	  ' "$(_jsonl_log)" 2>/dev/null
   442	}
   443	
   444	# --- contract: export / import / compact ------------------------------------
   445	
   446	storage_export() {
   447	  _JSONL_TEAM="$1"; shift
   448	  _jsonl_init_file || return 1
   449	  _jsonl_with_lock _jsonl_export_locked "$@"
   450	}
   451	
   452	_jsonl_export_locked() {
   453	  # Forward-compat (§2.3): only the v1 event types are projected; unknown types
   454	  # are dropped rather than leaked.
   455	  jq -c -s 'def logical_events: .[] | if .type=="sync_pull_commit" then
   456	    .messages[]? | select(.status=="imported") | .local_event // empty else . end;
   457	    logical_events | select(.type=="message_sent" or .type=="message_read")' \
   458	    "$(_jsonl_log)" > "$1"
   459	}
   460	
   461	storage_import() {
   462	  _JSONL_TEAM="$1"; shift

**Reviewing checker and test details**
**Analyzing environment and security concerns**

I’m digging into how environment variables like GIT_DIR and execution contexts might introduce security risks, especially around inherited settings and command execution paths. The complexity around bash traps and file parsing adds to the challenge, and I’m weighing existing behaviors against potential vulnerabilities carefully.
**Analyzing environment variable risks**
**Reviewing environment and config trust assumptions**
codex
GitHub コネクターで、PR の head/base と最終 head の CI 成功を確認できました。履歴照合には、送信が成功していても記録を拒むケースが見つかっています。既存の advisory P2 と独立に再現し、受入記録にある引継ぎ先と修正回数の扱いも確認します。
exec
/bin/zsh -lc "python3 -I -B -c 'import subprocess, hashlib, difflib
from pathlib import Path
head='\\''ef74eaea9a94bff388b7c1027551a57797407b2f'\\''
prefix='\\''.orchestration/dotfiles-T128-orchestrator-tools-followup-a03/'\\''
for name in ['\\''report.md'\\'','\\''sandbox.md'\\'','\\''learning.md'\\'','\\''autoskill.md'\\'']:
 print('\\''BRANCH '\\''+name+'\\''\\n'\\''+subprocess.check_output(['\\''git'\\'','\\''show'\\'',head+'\\'':'\\''+prefix+name],text=True))
task=subprocess.check_output(['\\''git'\\'','\\''show'\\'',head+'\\'':'\\''+prefix+'\\''task.md'\\''])
print('\\''task sha256'\\'',hashlib.sha256(task).hexdigest())
local=Path('\\''.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a03.md'\\'').read_text()
print('\\''task local difference:'\\'')
print('\\'''\\''.join(difflib.unified_diff(task.decode().splitlines(True),local.splitlines(True))))
'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 131ms:
BRANCH report.md
# Report: dotfiles-T128-orchestrator-tools-followup-a03

- **Seat and branch.** `claude-standard-dot-a003` in `.claude/worktrees/worker-c`, on the fresh branch `tools/dispatch-checker-window`, cut with `--no-track` from `origin/main` at `1d418126`. The earlier branches are left as they are.
- **Task copy.** Byte-identical to the dispatched main-checkout file, sha256 `b291ba85…`, the TASK's `task_sha256` (validation §1).
- **Commits.** `766c1491`: the change, its tests and the task copy; `aeb4a0fb`: this evidence; `c8e813ea`: the Bot's P1 fix; then this evidence's fix-round update.
- cost: n/a (the runtime exposes no token or cost figures to the seat).

## Item 1a: the checker refusal (C-52)

- For an AGMSG-TASK line, after the hash checks and before any read or send, `dispatch.sh` picks the Makefile's `UV_PYYAML` form: `uv run --offline --with pyyaml` when that form imports yaml, else `uv run --with pyyaml`.
- **The brief exemption.** It parses the task file's front matter (the lines between the first two `---` lines) with PyYAML under a `SafeLoader` whose mapping constructor refuses a duplicate key. Only a mapping whose `kind` is the string `review` skips the checker. A parse error, a duplicate key, no closed front matter, no `kind` or any other value runs it.
- **The checker.** `task-consistency-check.py --root <root> <file>` beside the script, as `python -I`. A non-zero exit prints `dispatch: <file> fails the task-consistency check` and the checker's output on stderr, exits 1 and sends nothing.

## Item 1b: the bounded window (C-53)

- Both reads are `history.sh <team> "" <BUS_READ_WINDOW>` (default 200, a positive integer, else usage). `BUS_READ_LIMIT` and the cap refusal are gone.
- **The window file.** `mktemp "${TMPDIR:-/tmp}/dispatch-window.XXXXXX"` (mode 0600), removed by an EXIT trap. The `check` mode writes the pre-send window there: each row's timestamp, sender, recipient and text, never its marker.
- **The alignment.** The `append` mode tries every shift `j` from 0 to `m − 1` and keeps those where the post-send window without its `j` newest rows equals the pre-send window without its `e = n + j − m` oldest (`0 ≤ e < n`). An empty pre-send window takes `j = m`.
- **Outcomes.** Zero or several fits: `does not align uniquely … raise BUS_READ_WINDOW or check the bus`. A unique `j = 0`: `this send added no bus row`. Otherwise the send is the last of the `j` new rows equal to the line, sender and recipient, and none equal: `no new row equals the line`. Every refusal exits 1 with the record unchanged.
- The shdoc header, the `@env BUS_READ_WINDOW` line and the `@exitcode 1` line say so.

## Tests

- `test_dispatch_refuses_a_task_file_failing_the_checker`: the stub checker beside the copied script, a fake `uv` that logs its argv and runs the real `uv` next on PATH. Refused, each with the checker call logged and the C2 line on stderr: `kind: code`, `kind: "code"`, no `kind`, the duplicate key in both orders, and a closed but unparsable front matter with one `kind: review` line. Sent with no checker call: a single `kind: review`. The log's first call is the `UV_PYYAML` probe.
- `test_dispatch_reads_a_bounded_history_window`: the limit argument is 200 on both reads, 50 with `BUS_READ_WINDOW=50`. Recorded once with the right marker: eviction plus collision, same second, and another seat's newer row. Refused with the record unchanged: left the window, no new row, a periodic bus. No `dispatch-window.*` file is left after any case.
- **The module.** 54 tests pass (validation §1). Eight mutants, all killed (validation §2 and §4).
- **Two of the 52 changed.** The cap's removal forced it; the names and edits are in validation §3. The module docstring names its new dependency on a real uv for the checker case.

## Notes

- **The uv form.** The Makefile's `UV_PYYAML` form plus `--no-project`, the Bot's P1 (below): a caller's `pyproject.toml` is never discovered, synced or built.
- **Size.** 105 changed lines outside `tests/` and `.orchestration/` (of 200), 114 added under `tests/` (of 1000), 2 files (validation §4).

## The Bot

- **Code review of `aeb4a0fb`** (review 5545290170): one P1, thread 4292675906, `dispatch.sh:181`, "Isolate uv from the caller's project". `fixed:c8e813ea`: `--no-project` on both uv forms, and the checker test's review brief sent from a directory with an unresolvable `pyproject.toml` (validation §4). The fix round is the PR's one round; the Bot's re-review is asked with `@codex review` on the fix head.
- **Security review of `aeb4a0fb`:** completed, no finding.
- **The PING** of 2026-10-16T21:38:05Z (the host slept overnight) was answered with a PONG, `status=alive`.

## Revise round 2 (`8adf74bb`)

- **The P1.** The Bot's re-review of `57d3577c`, thread 4299651928, `dispatch.sh:182`: `--no-project` keeps a caller's `pyproject.toml` out, but a `.python-version` or virtual environment in the caller's directory still chooses uv's interpreter. The operator's decision D-P1-374 A: one more fix round.
- **The fix.** `fixed:8adf74bb`. Both uv forms run in a subshell that changes to the script's checkout root (`uvr`); the checker is named by the script directory's absolute path.
- **The test.** `test_dispatch_refuses_a_task_file_failing_the_checker` plants a `.python-version` naming an executable in the caller's directory: it never runs, and the fake uv records the root as every call's directory. Mutant M9 (no `cd`) is killed; all nine mutants are killed, and 54 tests pass (validation §6).
- **Size after the round.** 108 changed lines outside `tests/` and `.orchestration/` (of 200), 122 added under `tests/` (of 1000), 2 files.
- **The Bot.** Its re-review is asked with `@codex review` on this round's head.

## Revise round 3 (`411c7d68`)

- **The P1.** The local review of `9df6b0c7`, `local:9df6b0c:1` (`dispatch.sh:183-185`): an inherited `VIRTUAL_ENV` still chose uv's interpreter after the `cd`. The third finding of one class, the interpreter chosen from caller state. The operator's decision D-S2-374-2 A: one round that closes the class (C-57).
- **The fix.** `fixed:411c7d68`. Both uv forms name `--python`, `python3` as `mise which` answers it under `env -i` at the root (else `python3` on PATH; a non-absolute answer refuses), and run under `env -u` for `VIRTUAL_ENV`, `VIRTUAL_ENV_PROMPT`, `CONDA_PREFIX` and every inherited `UV_*` variable. `--no-project` and the `cd` to the root stay.
- **The test.** `test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state` sets a caller project, a caller `.python-version`, `VIRTUAL_ENV`, `CONDA_PREFIX` and `UV_PYTHON` at once; none is used (validation §8). The checker test's setup is now the shared helper `checker_dispatch`, and its probe assertion expects the pinned `--python`.
- **Checks.** 55 tests pass; twelve mutants, all killed (validation §8).
- **Size after the round.** 120 changed lines outside `tests/` and `.orchestration/` (of 200), 145 added under `tests/` (of 1000), 2 files.
- **The Bot.** Its re-review is asked with `@codex review` on this round's head.

## Revise round 4 (`b18698d5`)

- **The P1.** The Bot's re-review of `6ae8cf75`, thread 4300102967, `dispatch.sh:197`: the `import yaml` probe ran without `-I`, so an inherited `PYTHONPATH` could load a caller's `yaml.py`. The fourth finding of the class; the operator's decision D-S2-374-3 A: one round that ends the class by an allowlist.
- **The fix.** `fixed:b18698d5`. Both uv forms run under `env -i` with `PATH`, `HOME`, `LANG` and `LC_ALL` when set, and the `AGMSG_*` variables, nothing else; the probe runs `python -I`. The pinned `--python`, `--no-project` and the `cd` to the root stay.
- **The test.** `test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state`, extended: every caller-state source at once, now with a `yaml.py` on `PYTHONPATH`; the fake uv inherits only the allowlisted names (validation §10).
- **Checks.** 55 tests pass; thirteen mutants, all killed (validation §10).
- **Size after the round.** 124 changed lines outside `tests/` and `.orchestration/` (of 200), 153 added under `tests/` (of 1000), 2 files.
- **The Bot.** Its re-review is asked with `@codex review` on this round's head.

BRANCH sandbox.md
---
task_id: dotfiles-T128-orchestrator-tools-followup-a03
seat: claude-standard-dot-a003
permission_gated_commands: 30
---

# Sandbox record: dotfiles-T128-orchestrator-tools-followup-a03

Period: from the AGMSG-TASK (2026-10-16T08:28:10Z) to the RESULT. These ran inside the sandbox: the fetch, the branch, the task copy with its hash (read from the main checkout), the reads, the edits, the tests, shellcheck, shfmt, ruff, the mutation proofs, the repository validator and the commits.

`permission_gated_commands` counts every Bash call made with `dangerouslyDisableSandbox`, one per call, and each `agmsg-dispatch`. Calls 1 to 6 have run. The Bot's P1 opened the fix round, so calls 7 to 13 are counted in advance; the main-checkout copy gives the final count.

| # | Command | Step 4 case |
|--:|---|---|
| 1 | the HTTPS push of `tools/dispatch-checker-window` | `git push` |
| 2 | `gh pr create --draft` and `gh pr ready` (PR #374) | `gh` |
| 3 | `gh pr checks 374 --watch` with the Bot wait beside it (background) | `gh` |
| 4 | `gh api` read of the Bot's summary, review comments and reactions (the security review still running) | `gh` |
| 5 | `gh api` wait until the Bot's security review of `aeb4a0fb` completed, and the re-read | `gh` |
| 6 | `agmsg-dispatch … AGMSG-PONG v1 task_id=dotfiles-T128-orchestrator-tools-followup-a03 status=alive …`, the answer to the PING of 21:38:05Z | `agmsg-dispatch` |
| 7 | the HTTPS push of the fix round's head | `git push` |
| 8 | `gh pr comment 374 --body '@codex review'` | `gh` |
| 9 | `gh pr checks 374 --watch` with the Bot wait beside it on the fix head (background) | `gh` |
| 10 | the re-check of the Bot's review, its comments and its summary on the final head (`gh api`) | `gh` |
| 11 | main-checkout `memory add` | main-checkout `memory add` |
| 12 | the masked copy of the evidence files to the main checkout | artifact copy with the repository masker |
| 13 | `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T128-orchestrator-tools-followup-a03 …` | `agmsg-dispatch` |

**Revise round 2.** Round 1 ran fourteen calls; its main-checkout copy records them, with rows 10 to 14 as they ran (the wait for the code re-review, the read of thread 4299651928, the memory add, the main copy and the RESULT). Round 2 adds rows 15 to 20, counted in advance; the main-checkout copy gives the final count.

| # | Command | Step 4 case |
|--:|---|---|
| 15 | the HTTPS push of round 2's head | `git push` |
| 16 | `gh pr comment 374 --body '@codex review'` | `gh` |
| 17 | `gh pr checks 374 --watch` with the Bot wait beside it (background) | `gh` |
| 18 | the re-check of the Bot's review, its comments and its summary on the final head (`gh api`) | `gh` |
| 19 | the round-2 sections copied into the main-checkout records, masked again | artifact copy with the repository masker |
| 20 | `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T128-orchestrator-tools-followup-a03 round=2 …` | `agmsg-dispatch` |

**Revise round 3.** Round 2 ran five calls, not six: its re-check of the Bot ran inside the wait call, as its main-checkout copy records (rows 15 to 19, nineteen in all). Round 3 adds rows 20 to 24, counted in advance; the main-checkout copy gives the final count.

| # | Command | Step 4 case |
|--:|---|---|
| 20 | the HTTPS push of round 3's head | `git push` |
| 21 | `gh pr comment 374 --body '@codex review'` | `gh` |
| 22 | `gh pr checks 374 --watch`, then the `gh api` wait until the Bot's code re-review completed, and the read of its reviews, comments and reactions (background) | `gh` |
| 23 | the round-3 sections copied into the main-checkout records, masked again | artifact copy with the repository masker |
| 24 | `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T128-orchestrator-tools-followup-a03 round=3 …` | `agmsg-dispatch` |

**Revise round 4.** Round 3 ran six calls, as its main-checkout copy records (rows 20 to 25, twenty-five in all; the read of thread 4300102967's body is its row 23). Round 4 adds rows 26 to 30, counted in advance; the main-checkout copy gives the final count.

| # | Command | Step 4 case |
|--:|---|---|
| 26 | the HTTPS push of round 4's head | `git push` |
| 27 | `gh pr comment 374 --body '@codex review'` | `gh` |
| 28 | `gh pr checks 374 --watch`, then the `gh api` wait until the Bot's code re-review completed, and the read of its reviews, comments and reactions (background) | `gh` |
| 29 | the round-4 sections copied into the main-checkout records, masked again | artifact copy with the repository masker |
| 30 | `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T128-orchestrator-tools-followup-a03 round=4 …` | `agmsg-dispatch` |

BRANCH learning.md
# Learning triage: dotfiles-T128-orchestrator-tools-followup-a03

These are candidates only; nothing is promoted.

1. [memory:failure] A test fixture for a duplicate-key refusal must put the exempt value last: PyYAML's default loader keeps the last value, so `kind: review` then `kind: code` is checked even without the refusal, and only `kind: code` then `kind: review` proves it. The mutant without the refusal survived until the second order was added.
2. [memory:decision] A recorder that finds its own row in a sliding window aligns the two windows as two views of one bus and requires a unique shift; a count or a single anchor row fails at the window's edge, under eviction, and on a periodic bus.
3. [memory:failure] `scripts/validate-agent-assets.py` now takes several minutes in the worker sandbox (the secret scan and the regime-boundary report); a gated commit needs a timeout above the default two minutes.

BRANCH autoskill.md
# AutoSkill run: dotfiles-T128-orchestrator-tools-followup-a03

- Status: not used. The task names no AutoSkill run.

task sha256 b291ba85f89d46877f74969d4e33ce994ff875f83454df58dbd8037a7d745da7
task local difference:
--- 
+++ 
@@ -41,7 +41,7 @@
   - control: in-process effects
     disposition: "residual: the test module imports only the standard library and runs dispatch.sh as a bash subprocess with a fake agmsg-dispatch and a fake history.sh under AGMSG_SCRIPTS and PATH; nothing is imported into another process"
   - control: workflow and interpreter or environment inputs
-    disposition: "residual: no workflow or interpreter file is in allowed_files; dispatch.sh runs shasum, python3 and agmsg-dispatch from PATH and history.sh from AGMSG_SCRIPTS (else the fixed agmsg scripts path) as today, and the checker through the Makefile's UV_PYYAML form (uv run --offline --with pyyaml when the cache holds PyYAML, else uv run --with pyyaml through the index: the validator-offline pattern of PR #366); the tests' seams are PATH and AGMSG_SCRIPTS; a PR checkout as cwd chooses nothing because dispatch.sh resolves its root from its own location"
+    disposition: "residual: no workflow or interpreter file is in allowed_files; dispatch.sh runs shasum, python3 and agmsg-dispatch from PATH and history.sh from AGMSG_SCRIPTS (else the fixed agmsg scripts path) as today, and the checker through the Makefile's UV_PYYAML form (uv run --offline --with pyyaml when the cache holds PyYAML, else uv run --with pyyaml through the index: the validator-offline pattern of PR #366); the tests' seams are PATH and AGMSG_SCRIPTS; a PR checkout as cwd chooses nothing because dispatch.sh resolves its root from its own location; after the fix round of D-P1-374 both uv commands run from the trusted script root (uv --directory <root>, the root from git rev-parse --show-toplevel of the script), so a caller cwd's .python-version or venv chooses nothing (the Bot's P1 4299651928 on PR #374)"
 premises:
   - claim: 'dispatch.sh on origin/main reads the whole bus (BUS_READ_LIMIT default 100000) before and after a send'
     command: 'git show origin/main:scripts/orchestrator/dispatch.sh | /usr/bin/grep -c "BUS_READ_LIMIT:-100000"'
@@ -129,3 +129,8 @@
 ## Change (bot_rounds, 2026-10-16T06:21:47Z)
 
 The Completion clause's `bot_rounds=1` becomes the template's `bot_rounds=2` form (the Bot's review at PR open and its re-review after the fix round): T13's amendment 6 after the Bot's P2 4290644781 on PR #371, applied to every undispatched task text right before its dispatch and re-confirmed Codex first (C-54). Nothing else changes from the pair-confirmed hash `5a741e63`.
+
+## Change (threat row, 2026-10-16T22:07:03Z, after the RESULT)
+
+The Codex Bot's P1 4299651928 on PR #374's head 57d3577c: uv run from the caller's cwd executes a caller-controlled `.python-version` or venv interpreter even with `--no-project`, which the environment threat row's claim that the cwd chooses nothing did not cover. Operator decision D-P1-374 A: the fix round runs uv from the trusted script root; the row now says so. The dispatched hash `b291ba85` stands (the branch's task copy is byte-identical to it by design); this row is the orchestrator's record, carried by the next boundary.
+


exec
/bin/zsh -lc "git worktree list --porcelain; git show ef74eaea9a94bff388b7c1027551a57797407b2f:.orchestration/dotfiles-T128-orchestrator-tools-followup-a03/validation.md | sed -n '220,405p'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 0ms:
worktree ~/Workspace/dotfiles
HEAD f7847616970d6bd83739a75a65ad8f7c35e91462
branch refs/heads/main

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles--claude-worktrees-worker-c/3747b995-3bb1-4c51-8421-4b1e672b442a/scratchpad/t124/mut
HEAD 52bb69fc0f2085e290f242e9145f74ba84f2a25c
detached
prunable gitdir file points to non-existent location

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/a3-replay
HEAD e87a52fc42eb4595c28585af6742e2c403302eee
detached
prunable gitdir file points to non-existent location

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/boundary-10
HEAD 014be44d0414492058d08d67b68e2a0eea23c17b
branch refs/heads/orchestration/boundary-10
prunable gitdir file points to non-existent location

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/boundary-11
HEAD fd3728be2127064803b956845a9a41efb18f6088
branch refs/heads/orchestration/boundary-11
prunable gitdir file points to non-existent location

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/boundary-12
HEAD 1e5d213a6be4a2df993240fe8463296ee9f8b29d
branch refs/heads/orchestration/boundary-12
prunable gitdir file points to non-existent location

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/boundary-13
HEAD e04dd19654b48aaca289059093484fde0bbf0511
branch refs/heads/orchestration/boundary-13
prunable gitdir file points to non-existent location

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/boundary-14
HEAD 5cb3757f73ddb44d94b0c3cf213bc89370b8eeff
branch refs/heads/orchestration/boundary-14
prunable gitdir file points to non-existent location

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/boundary-2026-10-11-2
HEAD 024826982257f6d9a6a8a74c2e6b2b743e5be55e
branch refs/heads/orchestration/boundary-2026-10-11-2
prunable gitdir file points to non-existent location

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/boundary-2026-10-12
HEAD bdf60419ad055a92f5048824482f3f94f1be61e1
branch refs/heads/orchestration/boundary-2026-10-12
prunable gitdir file points to non-existent location

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/boundary-2026-10-12-2
HEAD 8003a8d5222d899a208d89886051aba881397fe6
branch refs/heads/orchestration/boundary-2026-10-12-2
prunable gitdir file points to non-existent location

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/boundary-2026-10-12-3
HEAD b1230e7c86b81745366a834cbc86cad259c06d43
branch refs/heads/orchestration/boundary-2026-10-12-3
prunable gitdir file points to non-existent location

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/boundary-2026-10-12-4
HEAD bfe3161eba36109aa34c78f695020da81c9b03b8
branch refs/heads/orchestration/boundary-2026-10-12-4
prunable gitdir file points to non-existent location

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/boundary-2026-10-12-5
HEAD 9b56596c9d16922642ec4a319babde5d52ebe2f8
branch refs/heads/orchestration/boundary-2026-10-12-5
prunable gitdir file points to non-existent location

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/boundary-2026-10-12-6
HEAD cf9e1f89b01e6cb1fb37461e0b7a1ef0fc1a5be4
branch refs/heads/orchestration/boundary-2026-10-12-6
prunable gitdir file points to non-existent location

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/boundary-2026-10-12-7
HEAD 6a5acc0c6f67484a47babf6c33c69d07d6edade4
branch refs/heads/orchestration/boundary-2026-10-12-7
prunable gitdir file points to non-existent location

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/boundary-2026-10-12-8
HEAD 7db67953a360c2652edad5f7ae07ca087e0f7017
branch refs/heads/orchestration/boundary-2026-10-12-8
prunable gitdir file points to non-existent location

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/boundary-2026-10-12-9
HEAD 47f18670088b19be384cf0245f88fd5480d076d3
branch refs/heads/orchestration/boundary-2026-10-12-9
prunable gitdir file points to non-existent location

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/boundary-2026-10-13-1
HEAD 0103aefc3124f826aeedfc45da6f93ad17245cd4
branch refs/heads/orchestration/boundary-2026-10-13-1
prunable gitdir file points to non-existent location

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/boundary-2026-10-13-2
HEAD 961f47e1fd055d04df87a43b3d6d6bda6f772b19
branch refs/heads/orchestration/boundary-2026-10-13-2
prunable gitdir file points to non-existent location

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/boundary-2026-10-13-3
HEAD 1762ae0a0640e137f245f1af370c3a9d61a3bfb8
branch refs/heads/orchestration/boundary-2026-10-13-3
prunable gitdir file points to non-existent location

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/boundary-2026-10-13-4
HEAD 110471561c1697b98a17290d7235184dc9955784
branch refs/heads/orchestration/boundary-2026-10-13-4
prunable gitdir file points to non-existent location

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/boundary-2026-10-13-5
HEAD 1c2e4cc4cd7d94e43a731161f3d00d8d0250eabf
branch refs/heads/orchestration/boundary-2026-10-13-5
prunable gitdir file points to non-existent location

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/boundary-2026-10-13-6
HEAD 9c23147aa6d3ea0e1c6f6d4e08e533aa457e4a35
branch refs/heads/orchestration/boundary-2026-10-13-6
prunable gitdir file points to non-existent location

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/boundary-2026-10-13-7
HEAD 967251263b2655b1b3325fe070dcedbe8c3493b6
branch refs/heads/orchestration/boundary-2026-10-13-7
prunable gitdir file points to non-existent location

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/boundary-2026-10-13-8
HEAD 7491de0377e7ce4753916297129b24933980fdcb
branch refs/heads/orchestration/boundary-2026-10-13-8
prunable gitdir file points to non-existent location

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/boundary-2026-10-13-9
HEAD e86c38cb11fda50d25cd453f50e50a6dfc0fb9c1
branch refs/heads/orchestration/boundary-2026-10-13-9
prunable gitdir file points to non-existent location

worktree /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/t717-prep
HEAD 683384eaabd7a77a09f4452f518d2faa13c5123c
detached
prunable gitdir file points to non-existent location

worktree /private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/t717b
HEAD af7e91051cef494ce75af3beec73251f11412948
branch refs/heads/chore/model-profiles-xhigh

worktree ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
HEAD f7847616970d6bd83739a75a65ad8f7c35e91462
detached

worktree ~/Workspace/dotfiles/.claude/worktrees/worker-c
HEAD 3a952537a29567a7b0cfb4b9ff587ec34be71a9f
branch refs/heads/tools/settings-hook-dedupe-followup

worktree ~/Workspace/dotfiles/.claude/worktrees/worker-d
HEAD 4f9627ac316cacd879dfe08f0269f4205946dac0
branch refs/heads/receipt/canonical

worktree ~/Workspace/dotfiles/.claude/worktrees/worker-e
HEAD c0c3ff05f50846d8f880b7ccfb54d0c74630adf4
branch refs/heads/fix/project-map-owned-followups

worktree ~/Workspace/dotfiles/.claude/worktrees/worker-f
HEAD d2b33025d05f00b8dca947b54f9bbe0d16f1991b
branch refs/heads/tools/chain-review-scripts-followup-a03

M5 the newest new row taken as the send -> killed by test_dispatch_reads_a_bounded_history_window
M6 the whole bus read again -> killed by test_dispatch_reads_a_bounded_history_window
M7 no EXIT trap -> killed by test_dispatch_reads_a_bounded_history_window
M8 uv without --no-project (the Bot's P1) -> killed by test_dispatch_refuses_a_task_file_failing_the_checker
file restored (git diff --quiet HEAD): True
```

## 6. Revise round 2 (`8adf74bb`): uv runs from the trusted root

(§5 is the main-checkout copy's: CI and the Bot on `57d3577c`.) The Bot's re-review of `57d3577c` left P1 4299651928: with `--no-project`, uv still lets a `.python-version` or a virtual environment in the caller's directory choose the interpreter. The operator's decision D-P1-374 A gave this PR one more fix round. `8adf74bb` runs both uv forms through `uvr`, a subshell that changes to the script's checkout root, and names the checker by the script directory's absolute path (`here`), since a relative `BASH_SOURCE` would no longer resolve from the root.

The check `test_dispatch_refuses_a_task_file_failing_the_checker` sends the review brief from a caller directory whose `.python-version` names an executable that touches a marker and exits 1. The marker never appears, and the fake uv records the repository root as the directory of every call. Mutant M9 drops the `cd`; the planted interpreter then runs, the brief parse fails, and the send is refused, so the test fails on the exit code.

```text
$ shasum -a 256 .orchestration/dotfiles-T128-orchestrator-tools-followup-a03/task.md
b291ba85f89d46877f74969d4e33ce994ff875f83454df58dbd8037a7d745da7  .orchestration/dotfiles-T128-orchestrator-tools-followup-a03/task.md
$ git log --oneline -1; git merge-base HEAD origin/main
8adf74bb fix(orchestrator): dispatch.sh runs uv from the trusted root (the Bot's P1 429965
1d418126
$ the three premises (origin/main)
1
0
52
$ the same counts on HEAD
0
2
54

$ GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false UV_OFFLINE=1 uv run --no-project python -m unittest tests/unit/test_orchestrator_tools.py -v
(rc=0)
test_acceptance_front_matter_binds_head_and_pr_and_keeps_the_record ... ok
test_acceptance_front_matter_takes_audit_findings_only_for_an_incorrect_audit ... ok
test_boundary_commits_pushes_and_queues_the_pr ... ok
test_boundary_deletes_a_deleted_file_and_a_renamed_files_old_path ... ok
test_boundary_deletes_a_name_with_glob_characters_literally ... ok
test_boundary_keeps_a_name_with_a_newline_one_path ... ok
test_boundary_stops_before_commit_when_the_validator_fails ... ok
test_bus_read_closes_a_task_on_any_non_revise_acceptance ... ok
test_bus_read_ignores_closers_between_other_endpoints ... ok
test_bus_read_lists_an_open_task_with_minutes_since_its_latest_event ... ok
test_bus_read_refuses_a_read_that_reaches_its_limit ... ok
test_bus_read_skips_and_counts_malformed_rows ... ok
test_codex_review_closes_stdin_fixes_the_profile_and_needs_the_hash ... ok
test_design_keydiff_names_the_changed_invariant ... ok
test_dispatch_line_grammar_table ... ok
test_dispatch_passes_the_line_byte_identical ... ok
test_dispatch_reads_a_bounded_history_window ... ok
test_dispatch_record_path_tokenizes_and_locks ... ok
test_dispatch_records_the_sent_line_with_its_read_marker ... ok
test_dispatch_refuses_a_line_whose_sha256_field_does_not_match_its_file ... ok
test_dispatch_refuses_a_line_without_a_task_id ... ok
test_dispatch_refuses_a_malformed_record_block_before_sending ... ok
test_dispatch_refuses_a_tab_separated_task_without_its_hash_fields ... ok
test_dispatch_refuses_a_task_file_failing_the_checker ... ok
test_dispatch_refuses_a_task_line_without_task_sha256_or_with_a_second_line ... ok
test_dispatch_refuses_an_unwritable_record_before_sending ... ok
test_dispatch_refuses_malformed_lines ... ok
test_ff_main_keeps_a_local_deletion_across_the_fast_forward ... ok
test_ff_main_keeps_local_edits_across_the_fast_forward ... ok
test_fill_sweep_fills_only_a_commented_review ... ok
test_fill_sweep_fills_only_notice_annotations_and_success_statuses ... ok
test_fill_sweep_ignores_a_disposition_reply_from_another_login ... ok
test_fill_sweep_leaves_a_badged_review_body_a_gap ... ok
test_fill_sweep_quotes_the_url_form_evidence ... ok
test_fill_sweep_refuses_a_not_applicable_without_evidence ... ok
test_fill_sweep_refuses_a_shared_url_key_and_takes_an_item_id ... ok
test_fill_sweep_sees_a_collision_after_the_discussion_r_strip ... ok
test_fill_sweep_selects_a_null_url_status_by_source_and_check ... ok
test_orch_audit_refuses_a_ledger_check_that_differs_from_head ... ok
test_orch_audit_refuses_a_run_that_leaves_no_fresh_receipt ... ok
test_orch_audit_runs_the_ledger_check_by_default_and_refuses_a_gap ... ok
test_orch_audit_runs_the_ledger_check_isolated_from_sibling_modules ... ok
test_orch_gate_leaves_the_review_worktree_as_it_was_on_a_refusal_before_the_checkout ... ok
test_orch_gate_pins_the_interpreter_before_entering_the_review_worktree ... ok
test_orch_gate_refuses_a_head_that_tracks_a_symlink_under_orchestration ... ok
test_orch_gate_refuses_another_prs_sweep_or_a_changed_gate_before_the_review_worktree_moves ... ok
test_orch_gate_restores_the_review_worktree_when_setup_fails ... ok
test_orch_gate_returns_the_gate_status_and_restores_the_review_worktree ... ok
test_orch_gate_runs_the_gate_under_an_explicit_environment ... ok
test_orch_gate_runs_this_checkouts_gate_on_the_review_worktree_with_the_gate_inputs ... ok
test_replay_propagates_the_command_status ... ok
test_three_repeat_prints_body_matches_and_states_a_capped_memory_count ... ok
test_three_repeat_prints_the_records_search_line ... ok
test_three_repeat_rejects_a_class_that_is_not_a_slug_and_runs_the_cli_from_its_own_checkout ... ok
Ran 54 tests in 39.296s
OK

$ shellcheck scripts/orchestrator/dispatch.sh; shfmt --indent 4 --space-redirects -d scripts/orchestrator/dispatch.sh
(rc=0)
$ ruff check tests/unit/test_orchestrator_tools.py; ruff format --check tests/unit/test_orchestrator_tools.py
All checks passed!
1 file already formatted
(rc=0)

$ git diff --numstat origin/main...HEAD -- . ':!.orchestration'
85	23	scripts/orchestrator/dispatch.sh
122	11	tests/unit/test_orchestrator_tools.py
files: 2; changed lines outside tests/ and .orchestration/: 108; added under tests/: 122
```

```text
M1 the dispatch.sh of origin/main -> killed by test_dispatch_reads_a_bounded_history_window, test_dispatch_refuses_a_task_file_failing_the_checker
M2 the brief found by a literal kind: review line -> killed by test_dispatch_refuses_a_task_file_failing_the_checker
M3 no duplicate-key refusal -> killed by test_dispatch_refuses_a_task_file_failing_the_checker
M4 the first fitting shift, not a unique one -> killed by test_dispatch_reads_a_bounded_history_window
M5 the newest new row taken as the send -> killed by test_dispatch_reads_a_bounded_history_window
M6 the whole bus read again -> killed by test_dispatch_reads_a_bounded_history_window
M7 no EXIT trap -> killed by test_dispatch_reads_a_bounded_history_window
M8 uv without --no-project (the Bot's P1) -> killed by test_dispatch_refuses_a_task_file_failing_the_checker
M9 uv run from the caller's directory (the Bot's P1 4299651928) -> killed by test_dispatch_refuses_a_task_file_failing_the_checker
file restored (git diff --quiet HEAD): True
```

## 8. Revise round 3 (`411c7d68`): a pinned interpreter, no inherited environment

(§7 is the main-checkout copy's: CI and the Bot on `9df6b0c7`.) The local review of `9df6b0c7` found a P1, `local:9df6b0c:1` at `dispatch.sh:183-185`: after the `cd` to the root, an inherited `VIRTUAL_ENV` still chose uv's interpreter, so a PR checkout's `.venv` could run during the probe. It is the third finding of one class, the interpreter chosen from caller state (`pyproject.toml`, `.python-version`, `VIRTUAL_ENV`), and the operator's decision D-S2-374-2 A gave one round that closes the class (C-57).

`411c7d68` names the interpreter on both uv forms with `--python`: `python3` as `mise which` answers it under `env -i` at the root, else `python3` on PATH, and a non-absolute answer refuses. Both forms run under `env -u VIRTUAL_ENV -u VIRTUAL_ENV_PROMPT -u CONDA_PREFIX` plus `-u` for every inherited `UV_*` variable, keeping `--no-project` and the `cd` to the root.

The checker test's setup moved into a helper, `checker_dispatch`, which the new test `test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state` shares. That test sets, all at once, a caller `pyproject.toml` with an unresolvable dependency, a caller `.python-version` naming an executable, `VIRTUAL_ENV` and `CONDA_PREFIX` naming a caller `.venv` whose `python` is that executable, and `UV_PYTHON` naming it. It asserts that the executable never runs, that every uv call runs at the root and inherits no `VIRTUAL_ENV`, `CONDA_PREFIX` or `UV_*` variable (the fake uv records them), that both calls name one `--python` path other than the planted one, and that the send is recorded. The probe assertion in the checker test now expects `--python /<path>`. M10 to M12 are this round's mutants: the environment kept, only the non-`UV_*` variables stripped, and no `--python`.

```text
$ shasum -a 256 .orchestration/dotfiles-T128-orchestrator-tools-followup-a03/task.md
b291ba85f89d46877f74969d4e33ce994ff875f83454df58dbd8037a7d745da7  .orchestration/dotfiles-T128-orchestrator-tools-followup-a03/task.md
$ git log --oneline -1; git merge-base HEAD origin/main
411c7d68 fix(orchestrator): dispatch.sh runs uv on a pinned interpreter without the caller
1d418126
$ the three premises (origin/main)
1
0
52
$ the same counts on HEAD
0
2
55

$ GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false UV_OFFLINE=1 uv run --no-project python -m unittest tests/unit/test_orchestrator_tools.py -v
(rc=0)
test_acceptance_front_matter_binds_head_and_pr_and_keeps_the_record ... ok
test_acceptance_front_matter_takes_audit_findings_only_for_an_incorrect_audit ... ok
test_boundary_commits_pushes_and_queues_the_pr ... ok
test_boundary_deletes_a_deleted_file_and_a_renamed_files_old_path ... ok
test_boundary_deletes_a_name_with_glob_characters_literally ... ok
test_boundary_keeps_a_name_with_a_newline_one_path ... ok
test_boundary_stops_before_commit_when_the_validator_fails ... ok
test_bus_read_closes_a_task_on_any_non_revise_acceptance ... ok
test_bus_read_ignores_closers_between_other_endpoints ... ok
test_bus_read_lists_an_open_task_with_minutes_since_its_latest_event ... ok
test_bus_read_refuses_a_read_that_reaches_its_limit ... ok
test_bus_read_skips_and_counts_malformed_rows ... ok
test_codex_review_closes_stdin_fixes_the_profile_and_needs_the_hash ... ok
test_design_keydiff_names_the_changed_invariant ... ok
test_dispatch_line_grammar_table ... ok
test_dispatch_passes_the_line_byte_identical ... ok
test_dispatch_reads_a_bounded_history_window ... ok
test_dispatch_record_path_tokenizes_and_locks ... ok
test_dispatch_records_the_sent_line_with_its_read_marker ... ok
test_dispatch_refuses_a_line_whose_sha256_field_does_not_match_its_file ... ok
test_dispatch_refuses_a_line_without_a_task_id ... ok
test_dispatch_refuses_a_malformed_record_block_before_sending ... ok
test_dispatch_refuses_a_tab_separated_task_without_its_hash_fields ... ok
test_dispatch_refuses_a_task_file_failing_the_checker ... ok
test_dispatch_refuses_a_task_line_without_task_sha256_or_with_a_second_line ... ok
test_dispatch_refuses_an_unwritable_record_before_sending ... ok
test_dispatch_refuses_malformed_lines ... ok
test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state ... ok
test_ff_main_keeps_a_local_deletion_across_the_fast_forward ... ok
test_ff_main_keeps_local_edits_across_the_fast_forward ... ok
test_fill_sweep_fills_only_a_commented_review ... ok
test_fill_sweep_fills_only_notice_annotations_and_success_statuses ... ok
test_fill_sweep_ignores_a_disposition_reply_from_another_login ... ok
test_fill_sweep_leaves_a_badged_review_body_a_gap ... ok
test_fill_sweep_quotes_the_url_form_evidence ... ok
test_fill_sweep_refuses_a_not_applicable_without_evidence ... ok
test_fill_sweep_refuses_a_shared_url_key_and_takes_an_item_id ... ok
test_fill_sweep_sees_a_collision_after_the_discussion_r_strip ... ok
test_fill_sweep_selects_a_null_url_status_by_source_and_check ... ok
test_orch_audit_refuses_a_ledger_check_that_differs_from_head ... ok
test_orch_audit_refuses_a_run_that_leaves_no_fresh_receipt ... ok
test_orch_audit_runs_the_ledger_check_by_default_and_refuses_a_gap ... ok
test_orch_audit_runs_the_ledger_check_isolated_from_sibling_modules ... ok
test_orch_gate_leaves_the_review_worktree_as_it_was_on_a_refusal_before_the_checkout ... ok
test_orch_gate_pins_the_interpreter_before_entering_the_review_worktree ... ok
test_orch_gate_refuses_a_head_that_tracks_a_symlink_under_orchestration ... ok
test_orch_gate_refuses_another_prs_sweep_or_a_changed_gate_before_the_review_worktree_moves ... ok
test_orch_gate_restores_the_review_worktree_when_setup_fails ... ok

**Streamlining worktree data extraction**
mcp: codex_apps/github.fetch started
mcp: codex_apps/github.fetch_workflow_job_logs started
mcp: codex_apps/github.get_commit_combined_status started
mcp: codex_apps/github.fetch (completed)
mcp: codex_apps/github.get_commit_combined_status (completed)
mcp: codex_apps/github.fetch_workflow_job_logs (completed)
**Reviewing CI test logs**
exec
/bin/zsh -lc "python3 -I -B -c 'import subprocess,re,difflib
from pathlib import Path
h='\\''ef74eaea9a94bff388b7c1027551a57797407b2f'\\''
p='\\''.orchestration/dotfiles-T128-orchestrator-tools-followup-a03/validation.md'\\''
b=subprocess.check_output(['\\''git'\\'','\\''show'\\'',h+'\\'':'\\''+p],text=True)
print('\\''BRANCH validation rest'\\'')
for i,line in enumerate(b.splitlines(),1):
 if i>=220 and not re.match('\\''test_.* \\.\\.\\. ok"'$'"'\\'',line): print(f'\\''{i}: {line}'\\'')
l=Path('\\''.orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a03.md'\\'').read_text()
print('\\''LOCAL validation additions'\\'')
for line in difflib.unified_diff(b.splitlines(),l.splitlines(),n=1):
 print(line)
'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 57ms:
<string>:8: SyntaxWarning: "\." is an invalid escape sequence. Such sequences will not work in the future. Did you mean "\\."? A raw string is also an option.
BRANCH validation rest
220: M5 the newest new row taken as the send -> killed by test_dispatch_reads_a_bounded_history_window
221: M6 the whole bus read again -> killed by test_dispatch_reads_a_bounded_history_window
222: M7 no EXIT trap -> killed by test_dispatch_reads_a_bounded_history_window
223: M8 uv without --no-project (the Bot's P1) -> killed by test_dispatch_refuses_a_task_file_failing_the_checker
224: file restored (git diff --quiet HEAD): True
225: ```
226: 
227: ## 6. Revise round 2 (`8adf74bb`): uv runs from the trusted root
228: 
229: (§5 is the main-checkout copy's: CI and the Bot on `57d3577c`.) The Bot's re-review of `57d3577c` left P1 4299651928: with `--no-project`, uv still lets a `.python-version` or a virtual environment in the caller's directory choose the interpreter. The operator's decision D-P1-374 A gave this PR one more fix round. `8adf74bb` runs both uv forms through `uvr`, a subshell that changes to the script's checkout root, and names the checker by the script directory's absolute path (`here`), since a relative `BASH_SOURCE` would no longer resolve from the root.
230: 
231: The check `test_dispatch_refuses_a_task_file_failing_the_checker` sends the review brief from a caller directory whose `.python-version` names an executable that touches a marker and exits 1. The marker never appears, and the fake uv records the repository root as the directory of every call. Mutant M9 drops the `cd`; the planted interpreter then runs, the brief parse fails, and the send is refused, so the test fails on the exit code.
232: 
233: ```text
234: $ shasum -a 256 .orchestration/dotfiles-T128-orchestrator-tools-followup-a03/task.md
235: b291ba85f89d46877f74969d4e33ce994ff875f83454df58dbd8037a7d745da7  .orchestration/dotfiles-T128-orchestrator-tools-followup-a03/task.md
236: $ git log --oneline -1; git merge-base HEAD origin/main
237: 8adf74bb fix(orchestrator): dispatch.sh runs uv from the trusted root (the Bot's P1 429965
238: 1d418126
239: $ the three premises (origin/main)
240: 1
241: 0
242: 52
243: $ the same counts on HEAD
244: 0
245: 2
246: 54
247: 
248: $ GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false UV_OFFLINE=1 uv run --no-project python -m unittest tests/unit/test_orchestrator_tools.py -v
249: (rc=0)
304: Ran 54 tests in 39.296s
305: OK
306: 
307: $ shellcheck scripts/orchestrator/dispatch.sh; shfmt --indent 4 --space-redirects -d scripts/orchestrator/dispatch.sh
308: (rc=0)
309: $ ruff check tests/unit/test_orchestrator_tools.py; ruff format --check tests/unit/test_orchestrator_tools.py
310: All checks passed!
311: 1 file already formatted
312: (rc=0)
313: 
314: $ git diff --numstat origin/main...HEAD -- . ':!.orchestration'
315: 85	23	scripts/orchestrator/dispatch.sh
316: 122	11	tests/unit/test_orchestrator_tools.py
317: files: 2; changed lines outside tests/ and .orchestration/: 108; added under tests/: 122
318: ```
319: 
320: ```text
321: M1 the dispatch.sh of origin/main -> killed by test_dispatch_reads_a_bounded_history_window, test_dispatch_refuses_a_task_file_failing_the_checker
322: M2 the brief found by a literal kind: review line -> killed by test_dispatch_refuses_a_task_file_failing_the_checker
323: M3 no duplicate-key refusal -> killed by test_dispatch_refuses_a_task_file_failing_the_checker
324: M4 the first fitting shift, not a unique one -> killed by test_dispatch_reads_a_bounded_history_window
325: M5 the newest new row taken as the send -> killed by test_dispatch_reads_a_bounded_history_window
326: M6 the whole bus read again -> killed by test_dispatch_reads_a_bounded_history_window
327: M7 no EXIT trap -> killed by test_dispatch_reads_a_bounded_history_window
328: M8 uv without --no-project (the Bot's P1) -> killed by test_dispatch_refuses_a_task_file_failing_the_checker
329: M9 uv run from the caller's directory (the Bot's P1 4299651928) -> killed by test_dispatch_refuses_a_task_file_failing_the_checker
330: file restored (git diff --quiet HEAD): True
331: ```
332: 
333: ## 8. Revise round 3 (`411c7d68`): a pinned interpreter, no inherited environment
334: 
335: (§7 is the main-checkout copy's: CI and the Bot on `9df6b0c7`.) The local review of `9df6b0c7` found a P1, `local:9df6b0c:1` at `dispatch.sh:183-185`: after the `cd` to the root, an inherited `VIRTUAL_ENV` still chose uv's interpreter, so a PR checkout's `.venv` could run during the probe. It is the third finding of one class, the interpreter chosen from caller state (`pyproject.toml`, `.python-version`, `VIRTUAL_ENV`), and the operator's decision D-S2-374-2 A gave one round that closes the class (C-57).
336: 
337: `411c7d68` names the interpreter on both uv forms with `--python`: `python3` as `mise which` answers it under `env -i` at the root, else `python3` on PATH, and a non-absolute answer refuses. Both forms run under `env -u VIRTUAL_ENV -u VIRTUAL_ENV_PROMPT -u CONDA_PREFIX` plus `-u` for every inherited `UV_*` variable, keeping `--no-project` and the `cd` to the root.
338: 
339: The checker test's setup moved into a helper, `checker_dispatch`, which the new test `test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state` shares. That test sets, all at once, a caller `pyproject.toml` with an unresolvable dependency, a caller `.python-version` naming an executable, `VIRTUAL_ENV` and `CONDA_PREFIX` naming a caller `.venv` whose `python` is that executable, and `UV_PYTHON` naming it. It asserts that the executable never runs, that every uv call runs at the root and inherits no `VIRTUAL_ENV`, `CONDA_PREFIX` or `UV_*` variable (the fake uv records them), that both calls name one `--python` path other than the planted one, and that the send is recorded. The probe assertion in the checker test now expects `--python /<path>`. M10 to M12 are this round's mutants: the environment kept, only the non-`UV_*` variables stripped, and no `--python`.
340: 
341: ```text
342: $ shasum -a 256 .orchestration/dotfiles-T128-orchestrator-tools-followup-a03/task.md
343: b291ba85f89d46877f74969d4e33ce994ff875f83454df58dbd8037a7d745da7  .orchestration/dotfiles-T128-orchestrator-tools-followup-a03/task.md
344: $ git log --oneline -1; git merge-base HEAD origin/main
345: 411c7d68 fix(orchestrator): dispatch.sh runs uv on a pinned interpreter without the caller
346: 1d418126
347: $ the three premises (origin/main)
348: 1
349: 0
350: 52
351: $ the same counts on HEAD
352: 0
353: 2
354: 55
355: 
356: $ GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false UV_OFFLINE=1 uv run --no-project python -m unittest tests/unit/test_orchestrator_tools.py -v
357: (rc=0)
413: Ran 55 tests in 40.016s
414: OK
415: 
416: $ shellcheck scripts/orchestrator/dispatch.sh; shfmt --indent 4 --space-redirects -d scripts/orchestrator/dispatch.sh
417: (rc=0)
418: $ ruff check tests/unit/test_orchestrator_tools.py; ruff format --check tests/unit/test_orchestrator_tools.py
419: All checks passed!
420: 1 file already formatted
421: (rc=0)
422: 
423: $ git diff --numstat origin/main...HEAD -- . ':!.orchestration'
424: 97	23	scripts/orchestrator/dispatch.sh
425: 145	11	tests/unit/test_orchestrator_tools.py
426: files: 2; changed lines outside tests/ and .orchestration/: 120; added under tests/: 145
427: ```
428: 
429: ```text
430: M1 the dispatch.sh of origin/main -> killed by test_dispatch_reads_a_bounded_history_window, test_dispatch_refuses_a_task_file_failing_the_checker, test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state
431: M2 the brief found by a literal kind: review line -> killed by test_dispatch_refuses_a_task_file_failing_the_checker, test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state
432: M3 no duplicate-key refusal -> killed by test_dispatch_refuses_a_task_file_failing_the_checker
433: M4 the first fitting shift, not a unique one -> killed by test_dispatch_reads_a_bounded_history_window
434: M5 the newest new row taken as the send -> killed by test_dispatch_reads_a_bounded_history_window
435: M6 the whole bus read again -> killed by test_dispatch_reads_a_bounded_history_window
436: M7 no EXIT trap -> killed by test_dispatch_reads_a_bounded_history_window
437: M8 uv without --no-project (the Bot's P1) -> killed by test_dispatch_refuses_a_task_file_failing_the_checker
438: M9 uv run from the caller's directory (the Bot's P1 4299651928) -> killed by test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state
439: M10 the inherited environment kept (local:9df6b0c:1) -> killed by test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state
440: M11 only VIRTUAL_ENV stripped, the UV_* overrides kept -> killed by test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state
441: M12 no pinned --python -> killed by test_dispatch_refuses_a_task_file_failing_the_checker, test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state
442: file restored (git diff --quiet HEAD): True
443: ```
444: 
445: ## 10. Revise round 4 (`b18698d5`): an env -i allowlist and the probe with -I
446: 
447: (§9 is the main-checkout copy's: CI and the Bot on `6ae8cf75`.) The Bot's re-review of `6ae8cf75` left P1 4300102967 at `dispatch.sh:197`: the PyYAML probe ran `python -c 'import yaml'` without `-I`, so an inherited `PYTHONPATH` naming a caller-writable directory with a `yaml.py` would run that module before the task is validated. It is the fourth finding of the class, and the operator's decision D-S2-374-3 A gave one round that ends the class by an allowlist instead of a denylist.
448: 
449: `b18698d5` replaces round 3's `env -u` denylist with `env -i PATH=… HOME=…`, plus `LANG` and `LC_ALL` when set and every `AGMSG_*` variable, nothing else, for both uv forms; the probe runs `python -I -c 'import yaml'`. The pinned `--python`, `--no-project` and the `cd` to the root stay.
450: 
451: The test `test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state` now plants every source at once: a caller `pyproject.toml`, a caller `.python-version`, `VIRTUAL_ENV` and `CONDA_PREFIX` naming a caller `.venv`, `UV_PYTHON`, and a `yaml.py` on `PYTHONPATH` that writes the marker file, plus `AGMSG_STORAGE_PATH`. The fake uv, which has the calls directory written into it since `env -i` drops `CALLS`, records the name of every variable it inherits. The test asserts that the marker never appears, that apart from the `AGMSG_*` names the fake sees only `PATH`, `HOME`, `LANG`, `LC_ALL` and what bash sets itself (`PWD`, `SHLVL`, `_`, `OLDPWD`), and that `PATH`, `HOME` and `AGMSG_STORAGE_PATH` arrive. The checker test's probe form now expects `-I`.
452: 
453: M10 (no `env -i`) and M13 (`PYTHONPATH` let through) are killed by the new assertions. M11 (the probe without `-I`) is killed only by the checker test's probe-form assertion, since under `env -i` no `PYTHONPATH` reaches the probe; `-I` is the second layer.
454: 
455: ```text
456: $ shasum -a 256 .orchestration/dotfiles-T128-orchestrator-tools-followup-a03/task.md
457: b291ba85f89d46877f74969d4e33ce994ff875f83454df58dbd8037a7d745da7  .orchestration/dotfiles-T128-orchestrator-tools-followup-a03/task.md
458: $ git log --oneline -1; git merge-base HEAD origin/main
459: b18698d5 fix(orchestrator): dispatch.sh runs uv under an env -i allowlist and the PyYAML p
460: 1d418126
461: $ the three premises (origin/main)
462: 1
463: 0
464: 52
465: $ the same counts on HEAD
466: 0
467: 2
468: 55
469: 
470: $ GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false UV_OFFLINE=1 uv run --no-project python -m unittest tests/unit/test_orchestrator_tools.py -v
471: (rc=0)
527: Ran 55 tests in 40.461s
528: OK
529: 
530: $ shellcheck scripts/orchestrator/dispatch.sh; shfmt --indent 4 --space-redirects -d scripts/orchestrator/dispatch.sh
531: (rc=0)
532: $ ruff check tests/unit/test_orchestrator_tools.py; ruff format --check tests/unit/test_orchestrator_tools.py
533: All checks passed!
534: 1 file already formatted
535: (rc=0)
536: 
537: $ git diff --numstat origin/main...HEAD -- . ':!.orchestration'
538: 101	23	scripts/orchestrator/dispatch.sh
539: 153	11	tests/unit/test_orchestrator_tools.py
540: files: 2; changed lines outside tests/ and .orchestration/: 124; added under tests/: 153
541: ```
542: 
543: ```text
544: M1 the dispatch.sh of origin/main -> killed by test_dispatch_reads_a_bounded_history_window, test_dispatch_refuses_a_task_file_failing_the_checker, test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state
545: M2 the brief found by a literal kind: review line -> killed by test_dispatch_refuses_a_task_file_failing_the_checker, test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state
546: M3 no duplicate-key refusal -> killed by test_dispatch_refuses_a_task_file_failing_the_checker
547: M4 the first fitting shift, not a unique one -> killed by test_dispatch_reads_a_bounded_history_window
548: M5 the newest new row taken as the send -> killed by test_dispatch_reads_a_bounded_history_window
549: M6 the whole bus read again -> killed by test_dispatch_reads_a_bounded_history_window
550: M7 no EXIT trap -> killed by test_dispatch_reads_a_bounded_history_window
551: M8 uv without --no-project (the Bot's P1) -> killed by test_dispatch_refuses_a_task_file_failing_the_checker
552: M9 uv run from the caller's directory (the Bot's P1 4299651928) -> killed by test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state
553: M10 the inherited environment kept (no env -i) -> killed by test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state
554: M11 the probe without -I (the Bot's P1 4300102967) -> killed by test_dispatch_refuses_a_task_file_failing_the_checker
555: M12 no pinned --python -> killed by test_dispatch_refuses_a_task_file_failing_the_checker, test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state
556: M13 PYTHONPATH let through the allowlist -> killed by test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state
557: file restored (git diff --quiet HEAD): True
558: ```
LOCAL validation additions
--- 

+++ 

@@ -226,2 +226,36 @@

 
+## 5. CI and the Bot on `57d3577c`, the final head (main-checkout copy only)
+
+The fix head was pushed and `@codex review` asked at 2026-10-16T21:43Z (issue comment 6225256851).
+
+```text
+$ gh pr checks 374 --repo mryfmo/dotfiles --watch --interval 30; gh pr checks 374 --repo mryfmo/dotfiles; gh pr view 374 --repo mryfmo/dotfiles --json headRefOid,mergeStateStatus
+CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
+GitGuardian Security Checks	pass	2s	https://dashboard.gitguardian.com	
+private-bootstrap (macos-14, client)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/38971232744/job/117209825806	
+private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/38971232744/job/117209826124	
+private-bootstrap (ubuntu-24.04, server)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/38971232744/job/117209825845	
+public-bootstrap (macos-14, client)	pass	10m38s	https://github.com/mryfmo/dotfiles/actions/runs/38971232744/job/117209825896	
+public-bootstrap (ubuntu-24.04, client)	pass	10m25s	https://github.com/mryfmo/dotfiles/actions/runs/38971232744/job/117209825602	
+public-bootstrap (ubuntu-24.04, server)	pass	7m17s	https://github.com/mryfmo/dotfiles/actions/runs/38971232744/job/117209825758	
+test (macos-14, client)	pass	7m2s	https://github.com/mryfmo/dotfiles/actions/runs/38971232740/job/117209825693	
+test (ubuntu-24.04, client)	pass	7m36s	https://github.com/mryfmo/dotfiles/actions/runs/38971232740/job/117209825712	
+test (ubuntu-24.04, server)	pass	5m31s	https://github.com/mryfmo/dotfiles/actions/runs/38971232740/job/117209825382	
+test (ubuntu-26.04, client)	pass	9m11s	https://github.com/mryfmo/dotfiles/actions/runs/38971232740/job/117209825795	
+validate	pass	2m0s	https://github.com/mryfmo/dotfiles/actions/runs/38971232759/job/117209825144	
+ci-final rc=0
+{"headRefOid":"57d3577ca780248f573fd26c4fa460e2b5e2d510","mergeStateStatus":"BLOCKED"}
+```
+
+```text
+$ gh api repos/mryfmo/dotfiles/pulls/374/reviews --jq '.[]|"\(.id) \(.commit_id[0:8]) \(.state) \(.submitted_at)"'
+5545290170 aeb4a0fb COMMENTED 2026-10-16T08:51:20Z
+5554058212 57d3577c COMMENTED 2026-10-16T21:45:04Z
+$ gh api repos/mryfmo/dotfiles/pulls/374/comments --jq '.[]|"\(.id) \(.commit_id[0:8]) \(.path):\(.line) <title>"'
+4292675906 aeb4a0fb scripts/orchestrator/dispatch.sh:null Isolate uv from the caller's project
+4299651928 57d3577c scripts/orchestrator/dispatch.sh:182 Run uv outside the caller-controlled directory
+```
+
+The code re-review of `57d3577c` left one P1, thread 4299651928: with `--no-project`, uv still runs an interpreter that a `.python-version` (for example `./pwn`) or a virtual environment in the caller's directory names, before the task file is validated. The PR's one fix round is spent, so it stays open for the operator's decision (`bot_rounds=2`). The fix it names is one line: run both uv forms from the trusted script root (`cd "${root}"` in a subshell, or `uv --directory "${root}"`), or pin a trusted interpreter first. The module's own uv stub already models `.python-version` execution, so a test can plant one in the caller's directory.
+
 ## 6. Revise round 2 (`8adf74bb`): uv runs from the trusted root
@@ -331,2 +365,34 @@

 ```
+
+## 7. CI and the Bot on `9df6b0c7`, the final head (main-checkout copy only)
+
+```text
+$ gh pr checks 374; gh pr view 374 --json headRefOid,mergeStateStatus
+CodeRabbit: pass
+GitGuardian Security Checks: pass
+private-bootstrap (macos-14, client): pass
+private-bootstrap (ubuntu-24.04, client): pass
+private-bootstrap (ubuntu-24.04, server): pass
+public-bootstrap (macos-14, client): pass
+public-bootstrap (ubuntu-24.04, client): pass
+public-bootstrap (ubuntu-24.04, server): pass
+test (macos-14, client): pass
+test (ubuntu-24.04, client): pass
+test (ubuntu-24.04, server): pass
+test (ubuntu-26.04, client): pass
+validate: pass
+{"headRefOid":"9df6b0c7594cef7f42e9a43faa3e08d0f035e329","mergeStateStatus":"BLOCKED"}
+```
+
+```text
+$ the code_review state of the Bot's summary; gh api …/pulls/374/reviews; …/pulls/374/comments; …/issues/374/reactions
+"code_review":{"commit_sha":"9df6b0c7594cef7f42e9a43faa3e08d0f035e329","has_any_findings":false,"has_unresolved_findings":false,"status":"completed"}
+5545290170 aeb4a0fb COMMENTED 2026-10-16T08:51:20Z
+5554058212 57d3577c COMMENTED 2026-10-16T21:45:04Z
+4292675906 aeb4a0fb scripts/orchestrator/dispatch.sh:null **<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Isolate uv from the caller's project**
+4299651928 57d3577c scripts/orchestrator/dispatch.sh:null **<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Run uv outside the caller-controlled directory**
+chatgpt-codex-connector[bot] +1
+```
+
+The Bot's code re-review of `9df6b0c7`, asked with `@codex review`, completed with no finding and a 👍 reaction: no new review and no new thread. Threads 4292675906 and 4299651928 are on earlier heads (their `line` is now null).
 
@@ -444,2 +510,35 @@

 
+## 9. CI and the Bot on `6ae8cf75`, the final head (main-checkout copy only)
+
+```text
+$ gh pr checks 374; gh pr view 374 --json headRefOid,mergeStateStatus
+CodeRabbit: pass
+GitGuardian Security Checks: pass
+private-bootstrap (macos-14, client): pass
+private-bootstrap (ubuntu-24.04, client): pass
+private-bootstrap (ubuntu-24.04, server): pass
+public-bootstrap (macos-14, client): pass
+public-bootstrap (ubuntu-24.04, client): pass
+public-bootstrap (ubuntu-24.04, server): pass
+test (macos-14, client): pass
+test (ubuntu-24.04, client): pass
+test (ubuntu-24.04, server): pass
+test (ubuntu-26.04, client): pass
+validate: pass
+{"headRefOid":"6ae8cf75df74bb54eb3b724ea7c94e16b70759ef","mergeStateStatus":"UNKNOWN"}
+```
+
+```text
+$ the code_review state of the Bot's summary; gh api …/pulls/374/reviews; …/pulls/374/comments; …/issues/374/reactions
+"code_review":{"commit_sha":"6ae8cf75df74bb54eb3b724ea7c94e16b70759ef","has_any_findings":true,"has_unresolved_findings":true,"status":"completed"}
+5545290170 aeb4a0fb COMMENTED 2026-10-16T08:51:20Z
+5554058212 57d3577c COMMENTED 2026-10-16T21:45:04Z
+5554562648 6ae8cf75 COMMENTED 2026-10-16T23:04:34Z
+4292675906 aeb4a0fb scripts/orchestrator/dispatch.sh:null **<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Isolate uv from the caller's project**
+4299651928 57d3577c scripts/orchestrator/dispatch.sh:null **<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Run uv outside the caller-controlled directory**
+4300102967 6ae8cf75 scripts/orchestrator/dispatch.sh:197 **<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Isolate the PyYAML probe from inherited Python paths**
+```
+
+The Bot's code re-review of `6ae8cf75` (review 5554562648) left one P1, thread 4300102967 at `dispatch.sh:197`, "Isolate the PyYAML probe from inherited Python paths": the probe `uvr python -c 'import yaml'` runs without `-I`, so an inherited `PYTHONPATH` naming a caller-writable directory holding `yaml.py` executes that module before the task is validated; the later `python -I` calls do not cover the probe. The fix it names is one flag (`python -I -c 'import yaml'`), or stripping `PYTHONPATH` and the other `PYTHON*` overrides with the `env -u` list. This round's scope said nothing else, so it stays open for the orchestrator's decision.
+
 ## 10. Revise round 4 (`b18698d5`): an env -i allowlist and the probe with -I
@@ -558 +657,35 @@

 ```
+
+## 11. CI and the Bot on `9cf65c02`, the final head (main-checkout copy only)
+
+```text
+$ gh pr checks 374; gh pr view 374 --json headRefOid,mergeStateStatus
+CodeRabbit: pass
+GitGuardian Security Checks: pass
+private-bootstrap (macos-14, client): pass
+private-bootstrap (ubuntu-24.04, client): pass
+private-bootstrap (ubuntu-24.04, server): pass
+public-bootstrap (macos-14, client): pass
+public-bootstrap (ubuntu-24.04, client): pass
+public-bootstrap (ubuntu-24.04, server): pass
+test (macos-14, client): pass
+test (ubuntu-24.04, client): pass
+test (ubuntu-24.04, server): pass
+test (ubuntu-26.04, client): pass
+validate: pass
+{"headRefOid":"9cf65c0299645e30e54419668ba523eff9c4897e","mergeStateStatus":"BEHIND"}
+```
+
+```text
+$ the code_review state of the Bot's summary; gh api …/pulls/374/reviews; …/pulls/374/comments; …/issues/374/reactions; the body of any thread on the head
+"code_review":{"commit_sha":"9cf65c0299645e30e54419668ba523eff9c4897e","has_any_findings":false,"has_unresolved_findings":false,"status":"completed"}
+5545290170 aeb4a0fb COMMENTED 2026-10-16T08:51:20Z
+5554058212 57d3577c COMMENTED 2026-10-16T21:45:04Z
+5554562648 6ae8cf75 COMMENTED 2026-10-16T23:04:34Z
+4292675906 aeb4a0fb scripts/orchestrator/dispatch.sh:null **<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Isolate uv from the caller's project**
+4299651928 57d3577c scripts/orchestrator/dispatch.sh:null **<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Run uv outside the caller-controlled directory**
+4300102967 6ae8cf75 scripts/orchestrator/dispatch.sh:null **<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Isolate the PyYAML probe from inherited Python paths**
+chatgpt-codex-connector[bot] +1
+```
+
+The Bot's code re-review of `9cf65c02`, asked with `@codex review`, completed with no finding and a 👍 reaction: no new review and no new thread. `mergeStateStatus` is `BEHIND` because `main` moved after the branch was cut (`1d418126`); the orchestrator's update-branch takes the new base.

**Ensuring safe code execution**
**Analyzing timestamp and task consistency**
**Analyzing event timestamp handling**
**Reviewing root trust and config risks**
exec
/bin/zsh -lc "python3 -I -B -c 'import ast, subprocess, json
from pathlib import Path
h='\\''ef74eaea9a94bff388b7c1027551a57797407b2f'\\''
src=subprocess.check_output(['\\''git'\\'','\\''show'\\'',h+'\\'':scripts/orchestrator/dispatch.sh'\\''],text=True)
expr=next(x.partition('\\''='\\'')[2].strip() for x in src.splitlines() if x.startswith('\\''fits ='\\''))
cases=[('\\''underfull identical rows'\\'',['\\''X'\\'','\\''X'\\''],['\\''X'\\'','\\''X'\\'','\\''X'\\'']),('\\''interleaved concurrent row'\\'',['\\''A'\\'','\\''B'\\''],['\\''A'\\'','\\''C'\\'','\\''B'\\'','\\''sent'\\'']),('\\''ordinary append'\\'',['\\''A'\\'','\\''B'\\''],['\\''A'\\'','\\''B'\\'','\\''sent'\\''])]
for name,pre,post in cases:
 scope=dict(pre=pre,post=post,n=len(pre),m=len(post))
 print(name,'\\''pre='\\'',pre,'\\''post='\\'',post,'\\''fits='\\'',eval(compile(ast.parse(expr,mode='\\''eval'\\''),'\\''<head fits expression>'\\'','\\''eval'\\''),scope))
base='\\''f7847616970d6bd83739a75a65ad8f7c35e91462'\\''
d=subprocess.check_output(['\\''git'\\'','\\''show'\\'',base+'\\'':scripts/orchestrator/dispatch.sh'\\''],text=True)
t=subprocess.check_output(['\\''git'\\'','\\''show'\\'',base+'\\'':tests/unit/test_orchestrator_tools.py'\\''],text=True)
print('\\''premise counts:'\\'',sum('\\''BUS_READ_LIMIT:-100000'\\'' in x for x in d.splitlines()),sum('\\''task-consistency-check'\\'' in x for x in d.splitlines()),sum('\\''def test_'\\'' in x for x in t.splitlines()))
main=Path('\\''~/Workspace/dotfiles'\\'')
owner=main/'\\''.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a04.md'\\''
print('\\''main checkout owner exists:'\\'', owner.exists())
if owner.exists():
 print('\\''\\n'\\''.join(f'\\''{i}: {l}'\\'' for i,l in enumerate(owner.read_text().splitlines(),1)))
print('\\''waiver script exists:'\\'', (main/'\\''scripts/regime-waive.sh'\\'').exists())
state=Path.home()/'\\''.local/state/regime/waivers'\\''
print('\\''default waiver state dir exists:'\\'', state.exists())
if state.exists(): print('\\''task waiver filenames:'\\'',[p.name for p in state.glob('\\''*'\\'') if '\\''tools-followup-a03'\\'' in p.name])
'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 102ms:
underfull identical rows pre= ['X', 'X'] post= ['X', 'X', 'X'] fits= [1, 2]
interleaved concurrent row pre= ['A', 'B'] post= ['A', 'C', 'B', 'sent'] fits= []
ordinary append pre= ['A', 'B'] post= ['A', 'B', 'sent'] fits= [1]
premise counts: 1 0 52
main checkout owner exists: True
1: ---
2: format: 2
3: task_id: dotfiles-T128-orchestrator-tools-followup-a04
4: kind: code
5: security: false
6: design_review:
7:   receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
8:   design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
9: allowed_files:
10:   - scripts/orchestrator/dispatch.sh
11:   - tests/unit/test_orchestrator_tools.py
12:   - .orchestration/dotfiles-T128-orchestrator-tools-followup-a04/**
13: after: [dotfiles-T128-orchestrator-tools-followup-a03]
14: threat_table:
15:   - control: the PR edits scripts/orchestrator/dispatch.sh only within the owned rows (item 1)
16:     disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the orchestrator's diff review and the task-level audit from main compare the diff against those rows; an edit outside them is an undeclared change the audit fails"
17:   - control: the PR edits tests/unit/test_orchestrator_tools.py only within the owned rows (item 1)
18:     disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the orchestrator's diff review and the task-level audit from main compare the diff against those rows; an edit outside them is an undeclared change the audit fails"
19:   - control: "the commands dispatch.sh runs before a send (shasum, python3, agmsg-dispatch from PATH, history.sh from AGMSG_SCRIPTS, the task-consistency checker through uv)"
20:     disposition: "residual: the lineage's controls (PR #374): the checker runs before any send and refuses a failing task file; both uv forms run with --no-project from the script's checkout root, so a caller cwd chooses nothing (the Bot's P1s 4292675906 and 4299651928, fixed in c8e813ea and 8adf74bb, tests in tests/unit/test_orchestrator_tools.py on main); the owned rows change other lines and each carries its own test"
21:   - control: the task-file copy on the branch (.orchestration/dotfiles-T128-orchestrator-tools-followup-a04/task.md)
22:     disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
23:   - control: the branch evidence records under .orchestration/dotfiles-T128-orchestrator-tools-followup-a04/ (report.md, validation.md, sandbox.md, learning.md)
24:     disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
25:   - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
26:     disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
27:   - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
28:     disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
29:   - control: in-process effects
30:     disposition: "residual: the tests run dispatch.sh as a subprocess with stub agmsg scripts and a fake uv on PATH in a temporary directory, and import only the standard library; nothing is imported into another process"
31:   - control: workflow and interpreter or environment inputs
32:     disposition: "residual: no workflow or interpreter file is in allowed_files; dispatch.sh runs the agmsg scripts, shasum, python3 and uv (the checker) from the script's checkout root and reads the task file and the record as data; nothing from a PR head runs"
33:   - control: new or renamed scripts
34:     disposition: "residual: no new or renamed script: the owned rows name edits to the two files the lineage landed; any new or renamed script is an undeclared change the audit fails"
35:   - control: orchestrator effect merge
36:     disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
37:   - control: orchestrator effect update-branch
38:     disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
39:   - control: orchestrator effect forced worker removal
40:     disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
41: premises:
42:   - claim: 'the lineage task file is on origin/main at dispatch (present since boundary (16), 1d418126, which carried the a03 task file)'
43:     command: 'git cat-file -e origin/main:.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a03.md && echo present || echo absent'
44:     output: |-
45:       present
46:   - claim: 'the lineage acceptance record''s Owned-by section is on origin/main at dispatch (absent today: it lands with the boundary after PR #374 merges; a dispatch before the section would read no rows)'
47:     command: 'git show origin/main:.orchestration/acceptance/dotfiles-T128-orchestrator-tools-followup-a03.md 2>/dev/null | /usr/bin/grep -q "^## Owned by dotfiles-T128-orchestrator-tools-followup-a04" && echo present || echo absent'
48:     output: |-
49:       absent
50: ---
51: 
52: # AGMSG-TASK dotfiles-T128-orchestrator-tools-followup-a04 — the advisory findings of PR #374 (the owner task of the orchestrator-tools lineage; plan 020 step 1, C-51's owner-first rule)
53: 
54: Written 2026-10-16 by the orchestrator seat before the lineage's integration chain runs (C-51: an advisory P2 disposition is written only when its owner task file exists), pair-reviewed before dispatch. Under plan 020 step 4 a P2 finding (the Codex Bot, the orchestrator's local review, the task-level audit or the worker's own report) on a head of PR #374 that is not fixed in a C-50 revise round is advisory: it is dispositioned on the PR as `not-applicable:advisory P2 owned by dotfiles-T128-orchestrator-tools-followup-a04` and recorded as a row of `.orchestration/acceptance/dotfiles-T128-orchestrator-tools-followup-a03.md` under the heading `## Owned by dotfiles-T128-orchestrator-tools-followup-a04`; this task implements those rows after the lineage's PR merges.
55: 
56: ## What to do
57: 
58: 1. The owned rows: the `<id>\t<class>` rows under the heading `## Owned by dotfiles-T128-orchestrator-tools-followup-a04` in `.orchestration/acceptance/dotfiles-T128-orchestrator-tools-followup-a03.md` as read from `origin/main`; each row's finding text is in the record (the Bot thread, the local review file or the audit receipt the id names). Implement each, with one test per row named in report.md. A missing or empty section at dispatch makes this task a no-op: report `no owned rows` and stop; the orchestrator dispatches only after both premises replay `present`.
59: 2. Nothing else changes: no file outside the owned rows' files, no behaviour the rows do not name (dispatch.sh still sends one line after the checker and records it from a bounded history window).
60: 
61: ## Validation
62: 
63: - `uv run python -m unittest tests/unit/test_orchestrator_tools.py -v` green in the validation file, with the new tests named; `shellcheck scripts/orchestrator/dispatch.sh`.
64: - `git diff --numstat origin/main...HEAD` in the validation file: at most 200 changed lines outside `tests/` and outside `.orchestration/` (plan 021 step 7.2) and 1000 added lines under `tests/` (INV-2).
65: 
66: ## Completion
67: 
68: One PR from a fresh branch off `origin/main` (after PR #374 merges). The PR is ready for the orchestrator's integration when the ruleset's required checks are green, the Bot's review of the final head is in (at PR open, and once more after a P0/P1 fix round), every Bot thread is replied to and resolved by the orchestrator with its disposition, the validation file carries the outputs above, and the RESULT names every P0/P1 thread with `fixed:<sha>` and every P2 as fixed in a C-50 round or advisory; the orchestrator's audit of the final head is dispositioned finding by finding before the gate. The Bot reviews once, at PR open; its P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P0 or P1 that survives the round is listed as `open:<thread id>` with `bot_rounds=2` (the Bot's review at PR open and its re-review after the fix round), stops the PR and goes to the operator as a decision; a P2 on this PR's own change whose fix stays within allowed_files gets C-50's revise round while INV-6's counts allow it, else it is advisory and recorded under the same heading for the lineage's next owner task. The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`. The RESULT names head, base, branch, files, every Bot thread with its disposition, the test names per row, the caps, `task_copy=<sha256 of .orchestration/dotfiles-T128-orchestrator-tools-followup-a04/task.md>` and the evidence paths.
waiver script exists: False
default waiver state dir exists: False

exec
/bin/zsh -lc "GIT_WORK_TREE=/tmp git -C scripts/orchestrator rev-parse --show-toplevel; uv help run | rg -n -A6 'no-config|--python <|--no-project|--config-file'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 14ms:
/private/tmp
222:      --no-project
223-          Avoid discovering the project or workspace.
224-
225-          Instead of searching for projects in the current directory and parent directories, run in
226-          an isolated, ephemeral environment populated by the `--with` requirements.
227-
228-          If a virtual environment is active or found in a current or parent directory, it will be
--
669:  -p, --python <PYTHON>
670-          The Python interpreter to use for the run environment.
671-
672-          If the interpreter request is satisfied by a discovered environment, the environment will
673-          be
674-          used.
675-
--
787:      --config-file <CONFIG_FILE>
788-          The path to a `uv.toml` file to use for configuration.
789-
790-          While uv configuration can be included in a `pyproject.toml` file, it is not allowed in
791-          this context.
792-
793-          [env: UV_CONFIG_FILE=]
--
795:      --no-config
796-          Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
797-
798-          Normally, configuration files are discovered in the current directory, parent directories,
799-          or user configuration directories.
800-
801-          [env: UV_NO_CONFIG=]

**Assessing Python environment security risks**
**Investigating git environment boundary issues**
exec
/bin/zsh -lc "python3 -I -B -c 'from pathlib import Path
main=Path('\\''~/Workspace/dotfiles'\\'')
for name in ['\\''.orchestration/learning/mistakes/M-20261017-02.md'\\'','\\''.orchestration/acceptance/dotfiles-T128-orchestrator-tools-followup-a03.md'\\'']:
 p=main/name
 print(name, '\\''exists='\\'',p.exists())
 if p.exists() and '\\''mistakes'\\'' in name:
  print(p.read_text())
print('\\''plan 022 files:'\\'',[str(x.relative_to(main)) for x in (main/'\\''.agents/worklog'\\'').rglob('\\''*022*'\\'')][:30])
'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 65ms:
.orchestration/learning/mistakes/M-20261017-02.md exists= True
---
id: M-20261017-02
artifact: "dispatch.sh's checker invocation in dotfiles-T128-orchestrator-tools-followup-a03 (PR #374): three heads each let uv choose its interpreter from caller state (the caller's pyproject at aeb4a0fb, the caller cwd's .python-version at 57d3577c, an inherited VIRTUAL_ENV at 9df6b0c7)"
classes: [uv-caller-state-interpreter]
found_at: "2026-10-16T22:38:10Z (the orchestrator, after the local review of 9df6b0c7 named the third shape)"
detector: "the Codex Bot twice (P1 4292675906, P1 4299651928) and the orchestrator's local review (P1 on 9df6b0c7), one caller-state source each; the two fix rounds each removed one source (--no-project, then a cd to the script root)"
count_at_detection: "uv-caller-state-interpreter: three findings on one artifact under three slugs (uv-project-discovery, uv-caller-interpreter, uv-inherited-venv), unified at this record"
corrections: [C-57]
status: open
recorded_at: "2026-10-16T22:38:10Z"
---

# M-20261017-02

- **Evidence:** PR #374's threads 4292675906 and 4299651928 and the local review `…-local-review-9df6b0c.md`; the task's record rows; `uv help run` ("--no-project still uses a virtual environment found in a current or parent directory" and the active VIRTUAL_ENV).
- **Detection and why not earlier:** each fix removed the one caller-state source the finding named; uv has several (project discovery, .python-version, VIRTUAL_ENV, UV_* variables), so the next review found the next one; the rows carried three slugs, so S6 saw no repeat (M-20261016-01's pattern).
- **Root cause:** the invocation let uv select the interpreter (a discovery, a shape of the caller's environment) instead of naming it: the trusted interpreter is an identity (the one mise provides at the script's checkout root), and the inherited environment is input that must be stripped, not partly avoided.
- **Should have been:** at the first finding, pin the interpreter (`--python <trusted path>`, resolved at the script root) and run under an environment without VIRTUAL_ENV, UV_PROJECT_ENVIRONMENT and the other UV_* overrides (`env -u …` or an explicit allowlisted env), with one test that sets every caller-state source at once; class the findings under one slug.
- **Corrections:** C-57.

.orchestration/acceptance/dotfiles-T128-orchestrator-tools-followup-a03.md exists= True
plan 022 files: ['.agents/worklog/orchestrator-glue/ff-aside-002223', '.agents/worklog/orchestrator-glue/ff-aside-055819/.orchestration/plans/022-stabilise-and-operate.md', '.agents/worklog/orchestrator-glue/ff-aside-092025/.orchestration/plans/022-stabilise-and-operate.md', '.agents/worklog/orchestrator-glue/ff-aside-002149/.orchestration/plans/022-stabilise-and-operate.md', '.agents/worklog/orchestrator-glue/ff-aside-061040/.orchestration/plans/022-stabilise-and-operate.md', '.agents/worklog/orchestrator-glue/ff-aside-035355/.orchestration/plans/022-stabilise-and-operate.md', '.agents/worklog/orchestrator-glue/ff-aside-054133/.orchestration/plans/022-stabilise-and-operate.md', '.agents/worklog/orchestrator-glue/ff-aside-035309/.orchestration/plans/022-stabilise-and-operate.md', '.agents/worklog/orchestrator-glue/ff-aside-011909/.orchestration/plans/022-stabilise-and-operate.md', '.agents/worklog/orchestrator-glue/ff-aside-220806/.orchestration/plans/022-stabilise-and-operate.md', '.agents/worklog/orchestrator-glue/ff-aside-055337/.orchestration/plans/022-stabilise-and-operate.md', '.agents/worklog/orchestrator-glue/ff-aside-000706/.orchestration/plans/022-stabilise-and-operate.md', '.agents/worklog/orchestrator-glue/ff-aside-040845/.orchestration/plans/022-stabilise-and-operate.md', '.agents/worklog/orchestrator-glue/ff-aside-050626/.orchestration/plans/022-stabilise-and-operate.md', '.agents/worklog/orchestrator-glue/ff-aside-041908/.orchestration/plans/022-stabilise-and-operate.md', '.agents/worklog/orchestrator-glue/ff-aside-225726/.orchestration/plans/022-stabilise-and-operate.md', '.agents/worklog/orchestrator-glue/ff-aside-055520/.orchestration/plans/022-stabilise-and-operate.md', '.agents/worklog/orchestrator-glue/ff-aside-062101/.orchestration/plans/022-stabilise-and-operate.md', '.agents/worklog/orchestrator-glue/ff-aside-062333/.orchestration/plans/022-stabilise-and-operate.md', '.agents/worklog/orchestrator-glue/ff-aside-063240/.orchestration/plans/022-stabilise-and-operate.md', '.agents/worklog/orchestrator-glue/ff-aside-044039/.orchestration/plans/022-stabilise-and-operate.md', '.agents/worklog/orchestrator-glue/ff-aside-002223/.orchestration/plans/022-stabilise-and-operate.md', '.agents/worklog/orchestrator-glue/ff-aside-055544/.orchestration/plans/022-stabilise-and-operate.md', '.agents/worklog/orchestrator-glue/ff-aside-052933/.orchestration/plans/022-stabilise-and-operate.md', '.agents/worklog/orchestrator-glue/ff-aside-231018/.orchestration/plans/022-stabilise-and-operate.md', '.agents/worklog/orchestrator-glue/ff-aside-011544/.orchestration/plans/022-stabilise-and-operate.md', '.agents/worklog/orchestrator-glue/ff-aside-224538/.orchestration/plans/022-stabilise-and-operate.md', '.agents/worklog/orchestrator-glue/ff-aside-081647/.orchestration/plans/022-stabilise-and-operate.md', '.agents/worklog/orchestrator-glue/ff-aside-230332/.orchestration/plans/022-stabilise-and-operate.md', '.agents/worklog/orchestrator-glue/ff-aside-004232/.orchestration/plans/022-stabilise-and-operate.md']

**Analyzing audit evidence and ledger issues**
**Evaluating audit reporting and environment control**
**Assessing Git hook environment risks**
**Analyzing file descriptor exploits in subprocesses**
**Analyzing task invariants and security validation**
**Reviewing operator decision audit and invariant compliance**
exec
/bin/zsh -lc "rg -n 'storage_append|_at=|at=|created_at|date|storage_send' ~/.agents/skills/agmsg/scripts/send.sh ~/.agents/skills/agmsg/scripts/drivers/storage/sqlite.sh | head -n 65; git diff --check f7847616970d6bd83739a75a65ad8f7c35e91462 ef74eaea9a94bff388b7c1027551a57797407b2f" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc "rg -n 'searches|mistake|ledger|local' scripts/orchestrator/acceptance-front-matter.py scripts/require-crit-review.py scripts/orchestrator/regime_lookup.py; rg -n 'D-S2-374|D-P1-374|waiv|counter' ~/Workspace/dotfiles/.orchestration/plans/022-stabilise-and-operate.md | tail -n 25; git show origin/main:.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a04.md" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 exited 128 in 86ms:
rg: scripts/orchestrator/regime_lookup.py: No such file or directory (os error 2)
scripts/orchestrator/acceptance-front-matter.py:1:"""acceptance-front-matter.py <task> <sweep-json> <pr-worktree> [--ledger <tsv>] [--audit-dispositions <tsv>]
scripts/orchestrator/acceptance-front-matter.py:6:`ledger` keeps every row the record has and adds each `--ledger` row (`id<TAB>class`) whose id is new; a row whose
scripts/orchestrator/acceptance-front-matter.py:7:id is present is printed as kept-ledger-row. `searches` is recomputed by the gate's rule: each class with three or
scripts/orchestrator/acceptance-front-matter.py:8:more rows, with the sorted basenames of the mistake records naming it. `audit_findings` come from
scripts/orchestrator/acceptance-front-matter.py:50:    parser.add_argument("--ledger")
scripts/orchestrator/acceptance-front-matter.py:78:    ledger = list(record.get("ledger", []))
scripts/orchestrator/acceptance-front-matter.py:79:    present = {str(row.get("id")) for row in ledger if isinstance(row, dict)}
scripts/orchestrator/acceptance-front-matter.py:80:    for row_id, cls in rows(args.ledger, 2):
scripts/orchestrator/acceptance-front-matter.py:82:            print("kept-ledger-row", row_id)
scripts/orchestrator/acceptance-front-matter.py:84:            ledger.append({"id": row_id, "class": cls})
scripts/orchestrator/acceptance-front-matter.py:102:        row["class"] for row in ledger if isinstance(row, dict) and isinstance(row.get("class"), str)
scripts/orchestrator/acceptance-front-matter.py:104:    searches = []
scripts/orchestrator/acceptance-front-matter.py:106:        found = gate.mistake_records(root, cls)
scripts/orchestrator/acceptance-front-matter.py:109:        searches.append({"class": cls, "records": sorted(found)})
scripts/orchestrator/acceptance-front-matter.py:112:    block.update(ledger=ledger, searches=searches, audit_findings=findings)
scripts/orchestrator/acceptance-front-matter.py:120:    print("written", path.relative_to(root), "head", head[:7], "pr", block["pr"], "ledger", len(ledger))
scripts/require-crit-review.py:41:RECORD_KEYS = {"format", "task", "head", "pr", "ledger", "searches", "audit_findings", "dispatch"}
scripts/require-crit-review.py:42:# The swept finding ids the ledger must cover: Codex review comments, and Codex review bodies carrying a badge.
scripts/require-crit-review.py:46:MISTAKE_RECORDS = ".orchestration/learning/mistakes/"
scripts/require-crit-review.py:87:    "home/dot_local/bin/common/executable_herdr-agents",
scripts/require-crit-review.py:190:        return f"{PR_FEEDBACK_ENV} must point to a repo-local JSON file"
scripts/require-crit-review.py:351:        return [f"{CRIT_DATA_SOURCE_FIELD} must point to a repo-local JSON evidence file"]
scripts/require-crit-review.py:487:    record's ledger must cover, so it is matched against the live collection too.
scripts/require-crit-review.py:532:                f"{PR_FEEDBACK_ENV} does not match the local GitHub repository {repo}; rerun scripts/pr-feedback.py"
scripts/require-crit-review.py:558:        return [f"PR #{pr} head on GitHub is {metadata.get('headRefOid')}, not the local HEAD {head}; push first"]
scripts/require-crit-review.py:602:        # An advanced local base may contain untrusted code despite a safe merge-base.
scripts/require-crit-review.py:622:        return [f"PR #{pr} head on GitHub is {collected.get('head_sha')}, not the local HEAD {head}; push first"]
scripts/require-crit-review.py:624:        return [f"collected feedback does not match the local GitHub repository {evidence['repo']}"]
scripts/require-crit-review.py:635:    """Apply feedback_path_error's rule (repo-local, also after resolving links) to another .orchestration dir."""
scripts/require-crit-review.py:639:        return f"{env} must point to a repo-local file under .orchestration/{directory}/"
scripts/require-crit-review.py:771:    """Check the identity triple (task, head, pr) first, then format, ledger, searches and audit_findings."""
scripts/require-crit-review.py:792:    ledger = record.get("ledger")
scripts/require-crit-review.py:793:    if not isinstance(ledger, list):
scripts/require-crit-review.py:794:        errors.append("ledger must be a list of {id, class} rows")
scripts/require-crit-review.py:796:        for index, row in enumerate(ledger):
scripts/require-crit-review.py:808:                    f"ledger row {index} must be {{id: <thread id or audit:<sha7>:<n>>, class: <[a-z0-9-] slug>}}: {row!r}"
scripts/require-crit-review.py:810:    searches = record.get("searches")
scripts/require-crit-review.py:811:    if not isinstance(searches, list):
scripts/require-crit-review.py:812:        errors.append("searches must be a list of {class, records} entries")
scripts/require-crit-review.py:815:        for index, entry in enumerate(searches):
scripts/require-crit-review.py:825:                    f"searches entry {index} must be {{class: <slug>, records: [<file basename>, …]}}: {entry!r}"
scripts/require-crit-review.py:828:                errors.append(f"searches names class {entry['class']} more than once")
scripts/require-crit-review.py:855:    """The ids a ledger must cover: the sweep's Codex findings and the audit's numbered findings (a set, no regex)."""
scripts/require-crit-review.py:919:    missing = swept_finding_ids(items, summary, head) - {str(row["id"]) for row in record["ledger"]}
scripts/require-crit-review.py:921:        errors.append(f"S6: ledger lacks {', '.join(sorted(missing))}")
scripts/require-crit-review.py:922:    classes = Counter(row["class"] for row in record["ledger"])
scripts/require-crit-review.py:923:    stated = {entry["class"]: set(entry["records"]) for entry in record["searches"]}
scripts/require-crit-review.py:927:        found = mistake_records(root, cls)
scripts/require-crit-review.py:935:def mistake_records(root: Path, slug: str) -> set[str] | str:
scripts/require-crit-review.py:1073:        "For agent judgment, locate the review with `crit status --json`, then save `crit comments --all --json <review.json>` to a repo-local JSON file."
scripts/require-crit-review.py:1078:    print("This local evidence is process evidence, not reviewer authentication.")
59:| `dotfiles-T128-orchestrator-tools-followup-a01` | a003 worker-c, Claude | task-checkers-followup on `orch-audit.sh`, `test_orchestrator_tools.py`; counters task on `regime-counters.sh`, `test_regime_counters.py` | 1 |
71:| `dotfiles-T128-counters-review-kind-a01` (new) | first free Claude seat | tools-followup and seat-liveness (above); depends on the INV-6 amendment on main | 4 (last) |
158:Already drafted (hash `ae208bef…`); 22 owned rows in the a02 record on `origin/main` after boundary (15). Work: the rows' fixes across the twelve `scripts/orchestrator/*` files it names and `regime-counters.sh`, tests in `tests/unit/test_orchestrator_tools.py` and `tests/unit/test_regime_counters.py`. Check: `uv run python -m unittest tests/unit/test_orchestrator_tools.py tests/unit/test_regime_counters.py -v` green; caps. Completion: the clause; merge; no `home/` path, no `make update`.
204:- [ ] 1. The design `.orchestration/tasks/dotfiles-T128-regime-v3-a01.md`: INV-6's sentence replaced by the step-8 inventory wording (resets only on a failed deterministic check or an unfixed P0/P1 after the one round; P2 never counts; review-brief task ids excluded from every count; the counts read from the bus and GitHub as today); `implementing_tasks` gains `dotfiles-T128-gate-evidence-followup-a01: [INV-6]` and `dotfiles-T128-counters-review-kind-a01: [INV-6]`; version v25. `scripts/orchestrator/design-keydiff.py <design> origin/main` pasted into the round request.
207:- [ ] 4. Verify: both halves `accept` on one hash; the receipt pointer in the design; `make check-regime-boundary` still fails only on S2 lines (the counter changes in T14).
215:### T14 `dotfiles-T128-counters-review-kind-a01` (new, wave 4, after T2, T6 and T12's boundary; Claude seat)
217:Files: `scripts/regime-counters.sh`, `tests/unit/test_regime_counters.py`, `scripts/check-regime-boundary.sh`, `tests/unit/test_check_regime_boundary.py`, `tests/fixtures/regime-counters/**`, `.orchestration/dotfiles-T128-counters-review-kind-a01/**`. Work (aligned on 2026-10-15 with the INV-6 recalibration under redesign, `dotfiles-T128-regime-v3-inv6-redesign-a01`; final wording follows the accepted proposal): `regime-counters.sh` counts as today (raw history and GitHub counts) and skips a task id whose task file has `kind: review`, printing `excluded=review` for it; `check-regime-boundary.sh` reads an acceptance record's `threshold_dispositions` rows (the record block key the proposal names, written by `acceptance-front-matter.py`, T16) and reports a reached count with no row, a row whose trigger is not `none` with neither a reset record nor a waiver, and nothing for a reached count whose row's trigger is `none`. Tests: `test_a_review_brief_is_excluded_from_the_counts`, `test_a_dispositioned_threshold_silences_the_line`, `test_a_trigger_row_without_a_reset_is_reported`, with fixtures. Check: both modules green. Completion: the clause; merge; D1: `make check-regime-boundary` rc 0 on the main checkout with the records on `origin/main`.
221:Files: `scripts/orchestrator/acceptance-front-matter.py`, `scripts/require-crit-review.py`, `tests/unit/test_orchestrator_tools.py`, `tests/unit/test_require_crit_review.py`, `tests/fixtures/gate-evidence/*`, `.orchestration/dotfiles-T128-gate-reset-trigger-a01/**` (serial with `dotfiles-T128-gate-evidence-followup-a01` on `require-crit-review.py`). Work: `acceptance-front-matter.py` gains `--threshold-dispositions <tsv>` (`count<TAB>n<TAB>trigger<TAB>evidence`) and writes the block key `threshold_dispositions` as the accepted proposal names it; `require-crit-review.py` appends one `gate_refusals` entry `{check, head, at}` to the record block on every refusal it issues (the only writer of that key), reads the counters' output for the task and refuses a merge whose record has a reached count with no row, a `det-check` row with fewer than two `gate_refusals` entries naming its check on two heads, a `p0p1` row whose finding id is in neither the sweep's Bot items nor the audit JSONs, or a row whose trigger is not none without a reset record or waiver. Tests: `test_threshold_dispositions_are_written_from_the_tsv`, `test_the_gate_appends_its_own_refusal_entry`, `test_the_gate_refuses_a_reached_count_without_a_row`, `test_a_det_check_row_needs_two_gate_refusals`, `test_a_trigger_row_needs_a_reset_record`. Check: both modules green. Completion: the clause; merge; D1 then reads the rows.
246:| wave 3 | T13 rules-step8 (after T10; against v24 under D-T12-redesign, pair-confirmed `b04f9df6` 12:34Z, dispatch after a004's re-seat), then T15 settings-hook-dedupe | T11 doctor-codex-trust (after T9) | (wave 4) T14 counters (after T2, T6, v25) | | OP `make update` + restart after T9 and T13 |
280:- 2026-10-15T06:51:44Z T10 `dotfiles-T128-task-checkers-followup-a01` merged: PR #365 → `907522c2` (round 2 fixed the Bot/local/audit P2 at its root with `python -I`; a second audit raised one P2 on this orchestrator's counters line, readings pasted; two CI flakes rerun). Main: 907522c2. In flight: #364 round 3 (a003), T6 (a003), T15 blocked on a004's re-seat (operator). a002 free: next dispatchable task is T7 chain-glue-integrate (after T4 merges) or T11 doctor-codex-trust (not written).
288:- 2026-10-15T09:00:38Z T12: round 32 on the review seat's proposal (installed as v25, 10e5a900) revised on both halves (Codex: no class token on the audit finding line; the headless Claude fresh context: the gate resolves the record path under the review worktree's root so a main-checkout path is refused, no release for the no-row state so D1 is unattainable, the pre-block prose records, the gate's source for earlier audit texts, the advisory predicate on the JSON the gate reads, INV-5 versus the gate's own key, four P3). The author (a001) revises once (redesign round 2 dispatched); round 33 is the second of at most three pairs. The design file is back at v24 on disk until a pair accepts. #368 (tools a02): audit P2 on the url-form evidence template → revise round to a002; the counter sources pasted. chain-review a02: round 2 (the four env -S features) in review.
309:- **D-S2-369 (2026-10-16T01:16:22Z):** INV-6 v24 reads `revises 2 >= 2` and `amendments 2 >= 2` on T15 (`regime-counters.sh`, pasted in the record): three RESULTs (two `blocked` by the seat's lost network, one `ready_for_review`) and three TASK lines of the same hash (re-sent after the re-seats). Default A: proceed (the revise round for the audit's P2 on the predicate, then the integration), the counters and this reading in the record; B: stop and reset. The default applies now, since the same reading applied to D-S2-364 at this boundary; the operator may overrule.
310:- **D-S2-371 (2026-10-16T01:46:27Z):** INV-6 v24 reads `questions 3 >= 2`, `amendments 2 >= 2`, `revises 2 >= 2` on T13 (`regime-counters.sh`, pasted in the record): one question restated with a correction (the word budget), two amendments answering the budget and the Bot's P2, two RESULTs of which one `blocked` on the budget. Default A: proceed with amendment 3 and its revise round (the audit's three P2 on the SKILL cadence sentences, the missing test and the uncommitted evidence), the counters and this reading in the record; B: stop and reset. The default applies now, as for D-S2-364 and D-S2-369; the operator may overrule.
312:- **Operator waiver (2026-10-16T03:02:02Z):** asked through AskUserQuestion with the three S2 readings (D-S2-364, D-S2-369, D-S2-371), the operator chose A: the three continuations are waived as INV-6 v24's operator release condition. Recorded here as the waiver the audits of bf6beb5 (#369), 4d3d639 (#371) and the coming heads disposition against.
313:- 2026-10-16T03:02:40Z the operator waived INV-6 S2 for #364, #369 and #371 (answer A); #364's chain resumed (update-branch onto 8b25f9ca, CI, local review, sweep, audit); #369 in an evidence-only revise round (validation.md of the final head); #371 at amendment 4 (the cadence binds the merge; Codex review running); #370 waits for the operator's second commit (t717c.patch). Boundary (16) after the merges.
318:- **D-S2-372 (2026-10-16T21:46:37Z):** T7's PR #372 has had one Bot fix round (P1, d8bc67d4) and one C-50 revise round (two P2, d23cb50c); the local review of the update-branch head 2fe135c5 found a P1 (the audit leaves the shared review worktree at the base, so the gate reads the wrong head) and a P2 (no freshness recheck after a base move), both small in-scope fixes with tests. A second revise round makes INV-6 v24 read `revises 2 >= 2` (S2). Default A: waive S2 for this PR and send the one revise round (both findings, `check=` the two tests); B: stop the PR at 2fe135c5 and send the P1 to the owner task `dotfiles-T128-chain-glue-integrate-followup-a01` (a known broken audit-to-gate handoff would land on main); C: close PR #372 and re-task. Asked through AskUserQuestion. **DECIDED 2026-10-16T21:49:04Z: A (operator, AskUserQuestion).**
319:- **D-P1-374 (2026-10-16T21:57:29Z):** tools-a03's PR #374 (dispatch.sh) carries a P1 after the one fix round: the Bot's 4299651928, uv run from the caller's cwd still executes a caller-controlled `.python-version` or venv interpreter even with `--no-project` (the earlier P1 4292675906, project discovery, is fixed in c8e813ea). Default A: one more fix round, running uv from the trusted script root (`uv --directory <root>` or a `cd` subshell) with one test and the threat row corrected; B: stop at 57d3577c and integrate with the P1 owned by the next owner task (the orchestrator's dispatch would keep executing a cwd interpreter); C: close PR #374 and re-task. Asked through AskUserQuestion. **DECIDED 2026-10-16T22:06:27Z: A (operator, AskUserQuestion).**
320:- **D-S2-375 (2026-10-16T22:09:11Z):** the chain-github owner task's PR #375 (resolve-threads.sh) needs one revise round: the Bot's P2 4299756161 (a small in-scope C-50 fix with its test) and the five evidence files, which the worker left untracked in its worktree instead of committing them. INV-6 v24 reads `revises 2 >= 2` only because the orchestrator's two unblock answers (the fresh-branch refusal) went out as `status=revise`; no work was revised (M-20261017-01, C-56). Default A: treat the count as the artefact it is, waive S2 for this PR and send the one revise round; B: stop at a250b1cb, disposition the P2 as advisory under the a03 owner and accept a PR without committed evidence (against the Completion clause); C: close and re-task. Asked through AskUserQuestion. **DECIDED 2026-10-16T22:23:21Z: A (operator, AskUserQuestion).**
321:- **D-S2-372-2 (2026-10-16T22:24:34Z):** PR #372's waived revise round (6e4e9aa1) drew four new local-review findings on the 180-line chain-integrate.sh: a P1 (gh calls inherit CLICOLOR_FORCE=1 under Herdr, so the comments JSON can carry ANSI and fill_sweep aborts) and three P2 (a checks-not-yet-reported race after update-branch, an independent review clone's stale local main, a threat row the orchestrator's record now carries). A further fix round makes INV-6 read `revises 3`. Default A: waive S2 once more for the P1 only (one env line for the gh calls plus one test, as pr-feedback.py's gh_env does) and record the three P2 as advisory under `dotfiles-T128-chain-glue-integrate-followup-a01`; B: stop at 6e4e9aa1 and integrate with the P1 owned by the follow-up (the chain would fail under Herdr until then); C: close and re-task the script with the findings folded in. Asked through AskUserQuestion. **DECIDED 2026-10-16T22:26:15Z: A (operator, AskUserQuestion).**
322:- **D-S2-374-2 (2026-10-16T22:38:10Z):** PR #374's fix round (9df6b0c7) drew a third finding of one class from the local review: an inherited `VIRTUAL_ENV` still selects uv's interpreter after the cd (after the caller's pyproject and the caller cwd's .python-version); the three rows now share the slug `uv-caller-state-interpreter` (M-20261017-02, C-57: name the interpreter, strip the environment). A further fix round makes INV-6 read `revises 2`. Default A: waive S2 and send one round that closes the class (pin `--python` to the trusted interpreter resolved at the script root, run under an environment without VIRTUAL_ENV and the UV_* overrides, one test setting pyproject, .python-version and VIRTUAL_ENV at once); B: stop at 9df6b0c7 and integrate with the P1 owned by `dotfiles-T128-orchestrator-tools-followup-a04`; C: close and re-task. Asked through AskUserQuestion. **DECIDED 2026-10-16T22:42:38Z: A (operator, AskUserQuestion).**
323:- **D-S2-374-3 (2026-10-16T23:14:12Z):** PR #374's class-closing round (6ae8cf75) still drew the Bot's P1 4300102967: the `import yaml` probe runs without `-I`, so an inherited PYTHONPATH loads a caller's yaml.py; the round stripped the environment by a denylist (VIRTUAL_ENV, CONDA_PREFIX, UV_*) and PYTHON* was not on it. A further round makes INV-6 read `revises 3`. Default A: waive S2 and send one round that ends the class by allowlist rather than denylist (`env -i` with an explicit PATH, HOME and the agmsg variables for the probe and the checker; `-I` on the probe; one test planting a caller pyproject, .python-version, VIRTUAL_ENV, UV_PYTHON and a yaml.py on PYTHONPATH at once); B: stop at 6ae8cf75 and integrate with the P1 owned by `dotfiles-T128-orchestrator-tools-followup-a04`; C: close and re-task. Asked through AskUserQuestion. **DECIDED 2026-10-16T23:16:22Z: A (operator, AskUserQuestion).**
324:- **D-S2-375-2 (2026-10-16T23:39:09Z):** PR #375's audit of 59eca2af found two worker-side P2: resolve-threads.sh:33 lets an empty-ID TSV row with a backtick bypass the rejection (a one-line guard plus a test), and the C-50 round's `revise.yaml` was not committed (the SKILL requires previous_head and selector committed together); the third P2 is the orchestrator's counter note (corrected in the record; INV-6 counts RESULTs minus one, so the task reads revises 2 after its third RESULT, not the two unblock answers). A further round is S2 either way. Default A: waive S2 and send one round that commits revise.yaml and rejects malformed IDs with a test; B: stop at 59eca2af and integrate, the awk guard advisory under `dotfiles-T128-chain-github-scripts-followup-a03` and revise.yaml absent; C: close and re-task. Asked through AskUserQuestion. **DECIDED 2026-10-16T23:58:34Z: A (operator, AskUserQuestion).**
326:- 2026-10-16T04:17:21Z **T13 done**: PR #371 → `3b60d6da` (amendments 1 to 6; the audit of 07400690 incorrect with one P1 and two P2, dispositioned: the operator's recorded INV-6 waiver, the red-first reading of INV-3, the owner task's `allowed_files` repaired; the Bot's P2 4290741790 on the task copy's stale test name corrected in the task text's `## Change (test name)`). Operator step at that moment: `make update` and a Claude Code restart.
328:- 2026-10-16T05:53:45Z **T4 done**: PR #364 → `fdef3ceb` under the operator's S2 waiver (the evidence round 2f4ce7e9, the local review's P1 on the owner id fixed in 070ca0ea; the audit of 40f3be41 incorrect with two advisory P2 (env -S quoting → a02, the heading-test fixture → a03) and one P3 corrected in the record). T7 `dotfiles-T128-chain-glue-integrate-a01` dispatched to a002 at 05:54:58Z (PR #372 opened by the worker).
336:- 2026-10-16T23:11:15Z **T7 done**: PR #372 → `5fd4fe0c` (chain-integrate.sh; one Bot fix round, one C-50 round and two operator-waived rounds D-S2-372 and D-S2-372-2 for the local review's P1s; the audit's remaining P2 advisory under `dotfiles-T128-chain-glue-integrate-followup-a01`). PR #375's chain running (chain-github a02, a004); then #376 (chain-review a02, a003) and #374 (tools-a03, after its class-closing fix round). Owner tasks in flight: seat-liveness followup (a002, PR #377, one Bot P2 proposed as C-50); pane-open followup pair-confirmed, to a004 after #375. T8 next to a free Claude seat.
fatal: path '.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a04.md' does not exist in 'origin/main'

 succeeded in 98ms:
~/.agents/skills/agmsg/scripts/drivers/storage/sqlite.sh:21:_sqlite_now() { date -u +%Y-%m-%dT%H:%M:%SZ; }
~/.agents/skills/agmsg/scripts/drivers/storage/sqlite.sh:228:      created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now')),
~/.agents/skills/agmsg/scripts/drivers/storage/sqlite.sh:289:#   * Rows that predate this are unmirrored in the other direction -- they exist
~/.agents/skills/agmsg/scripts/drivers/storage/sqlite.sh:293:# WHEN IT ENDS. Not on a date, and not "once everyone upgrades": the readers are
~/.agents/skills/agmsg/scripts/drivers/storage/sqlite.sh:304:  local team="$1" from="$2" to="$3" body="$4" id="$5" at="$6"
~/.agents/skills/agmsg/scripts/drivers/storage/sqlite.sh:310:    INSERT INTO messages (team,from_agent,to_agent,body,created_at)
~/.agents/skills/agmsg/scripts/drivers/storage/sqlite.sh:318:storage_send() {
~/.agents/skills/agmsg/scripts/drivers/storage/sqlite.sh:320:  local id at db; id="$(compat_uuid7)"; at="$(_sqlite_now)"; db="$(_sqlite_db "$team")"
~/.agents/skills/agmsg/scripts/drivers/storage/sqlite.sh:363:  at="$(_sqlite_now)"
~/.agents/skills/agmsg/scripts/drivers/storage/sqlite.sh:375:      UPDATE messages SET read_at='$(_sqlite_lit "$at")'
~/.agents/skills/agmsg/scripts/drivers/storage/sqlite.sh:454:               'from',m.from_agent,'to',m.to_agent,'body',m.body,'at',m.created_at) AS j,
~/.agents/skills/agmsg/scripts/drivers/storage/sqlite.sh:455:             m.created_at AS ts, 0 AS src, m.id AS ord
~/.agents/skills/agmsg/scripts/drivers/storage/sqlite.sh:565:                 'from',from_agent,'to',to_agent,'body',body,'at',created_at) AS j,
~/.agents/skills/agmsg/scripts/drivers/storage/sqlite.sh:566:               created_at AS ts, 0 AS src, id AS ord
~/.agents/skills/agmsg/scripts/drivers/storage/sqlite.sh:611:    t=$(j type); id=$(j id); team=$(j team); at=$(j at)
~/.agents/skills/agmsg/scripts/drivers/storage/sqlite.sh:624:        UPDATE messages SET read_at='$(_sqlite_lit "$at")'
~/.agents/skills/agmsg/scripts/send.sh:61:source "$SCRIPT_DIR/lib/validate.sh"
~/.agents/skills/agmsg/scripts/send.sh:66:# not --force is given, so validate it unconditionally, before any config-path
~/.agents/skills/agmsg/scripts/send.sh:69:agmsg_validate_team_name "$TEAM" || exit 1
~/.agents/skills/agmsg/scripts/send.sh:93:# per-type message plug after storage_send needs this path regardless of
~/.agents/skills/agmsg/scripts/send.sh:137:# Write through the storage axis (§2.1 storage_send) — the active driver now owns
~/.agents/skills/agmsg/scripts/send.sh:139:# storage_send re-inits its schema idempotently before writing, which subsumes the
~/.agents/skills/agmsg/scripts/send.sh:142:MSG_ID="$(storage_send "$TEAM" "$FROM" "$TO" "$BODY")"

**Reviewing source command and task linkage**
exec
/bin/zsh -lc "sed -n '914,970p' scripts/require-crit-review.py; sed -n '43,120p' scripts/orchestrator/acceptance-front-matter.py; nl -ba ~/.agents/skills/agmsg/scripts/drivers/storage/sqlite.sh | sed -n '318,351p'; git status --short" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 45ms:
    if errors:
        return errors, record
    summary, summary_error = audit_summary(root)
    if summary_error is not None:
        return [summary_error], record
    missing = swept_finding_ids(items, summary, head) - {str(row["id"]) for row in record["ledger"]}
    if missing:
        errors.append(f"S6: ledger lacks {', '.join(sorted(missing))}")
    classes = Counter(row["class"] for row in record["ledger"])
    stated = {entry["class"]: set(entry["records"]) for entry in record["searches"]}
    for cls, count in classes.items():
        if count < S6_CLASS_LIMIT:
            continue
        found = mistake_records(root, cls)
        if isinstance(found, str):
            errors.append(f"S6: class {cls} at {count}: {found}")
        elif stated.get(cls) != found:
            errors.append(f"S6: class {cls} at {count} without a matching records search")
    return errors, record


def mistake_records(root: Path, slug: str) -> set[str] | str:
    """Recompute S6's records search with pathlib: the files with a `classes:` line naming the class.

    The same match as `grep -rl 'classes:.*<class>'`, without a subprocess; the gate reads its result, never
    pasted command text.
    """
    directory = root / MISTAKE_RECORDS
    if not directory.is_dir():
        return f"the records directory {MISTAKE_RECORDS} is missing"
    found: set[str] = set()
    for path in directory.rglob("*"):
        if path.is_file() and not path.is_symlink():
            lines = path.read_text(errors="replace").splitlines()
            if any(line.startswith("classes:") and slug in line[len("classes:") :] for line in lines):
                found.add(path.name)
    return found


def evidence_field(text: str, field: str) -> str | None:
    prefix = f"{field}:"
    for line in text.splitlines():
        if line.startswith(prefix):
            return line[len(prefix) :].strip()
    return None


def review_marker() -> str | None:
    if os.environ.get(REVIEWED_ENV) == "1":
        return f"{REVIEWED_ENV}=1"
    if os.environ.get(NATIVE_REVIEWED_ENV) == "1":
        return f"{NATIVE_REVIEWED_ENV}=1"
    return None


def base_ref_error(root: Path, base: str) -> str | None:
    """Fail closed: an unresolvable or option-like --base must not silently skip the base checks."""


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("task")
    parser.add_argument("sweep")
    parser.add_argument("pr_worktree")
    parser.add_argument("--ledger")
    parser.add_argument("--audit-dispositions")
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", args.task):
        parser.error(f"not a task id: {args.task!r}")
    root = Path(git("-C", str(Path(__file__).resolve().parent), "rev-parse", "--show-toplevel"))
    spec = importlib.util.spec_from_file_location("require_crit_review", root / "scripts/require-crit-review.py")
    gate = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gate)

    try:
        sweep = json.loads(Path(args.sweep).read_text(), object_pairs_hook=gate.refuse_duplicate_keys)
    except ValueError as error:
        refuse(f"{args.sweep}: {error}")
    head = git("-C", args.pr_worktree, "rev-parse", "HEAD")
    if sweep.get("head_sha") != head:
        refuse(f"the sweep was collected for head {sweep.get('head_sha')!r}, not {args.pr_worktree}'s HEAD {head}")

    path = root / ".orchestration/acceptance" / f"{args.task}.md"
    text = path.read_text() if path.is_file() else ""
    record, rest = {}, text
    if text.split("\n")[0] == "---":
        record, error = gate.read_acceptance_record(path)
        if error:
            refuse(error)
        lines = text.split("\n")
        rest = "\n".join(lines[lines.index("---", 1) + 1 :])

    ledger = list(record.get("ledger", []))
    present = {str(row.get("id")) for row in ledger if isinstance(row, dict)}
    for row_id, cls in rows(args.ledger, 2):
        if row_id in present:
            print("kept-ledger-row", row_id)
        else:
            ledger.append({"id": row_id, "class": cls})
            present.add(row_id)

    summary = root / f".orchestration/validation/{args.task}-audit-{head[:7]}.md.last.md"
    audit = summary.read_text() if summary.is_file() else ""
    # The gate's verdict rule: the summary's last non-blank line.
    last = [line for line in audit.splitlines() if line.strip()][-1:]
    verdict = (match := gate.AUDIT_VERDICT.fullmatch(last[0]) if last else None) and match.group(1)
    incorrect = verdict == "incorrect"
    if incorrect != (args.audit_dispositions is not None):
        refuse(
            f"--audit-dispositions is {'required' if incorrect else 'refused'}: {summary.name} {verdict or 'missing'}"
        )
    findings = [
        {"n": n, "reason": reason, "evidence": evidence} for n, reason, evidence in rows(args.audit_dispositions, 3)
    ]

    classes = collections.Counter(
        row["class"] for row in ledger if isinstance(row, dict) and isinstance(row.get("class"), str)
    )
    searches = []
    for cls in sorted(c for c, count in classes.items() if count >= gate.S6_CLASS_LIMIT):
        found = gate.mistake_records(root, cls)
        if isinstance(found, str):
            refuse(found)
        searches.append({"class": cls, "records": sorted(found)})

    block = {**record, "format": gate.RECORD_FORMAT, "task": args.task, "head": head, "pr": sweep.get("pr")}
    block.update(ledger=ledger, searches=searches, audit_findings=findings)
    errors = gate.record_field_errors(block, args.task, head, sweep.get("pr"))
    if not errors and incorrect:
        errors = gate.audit_findings_errors(block, len(gate.AUDIT_FINDING.findall(audit)))
    if errors:
        refuse("; ".join(errors))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("---\n" + json.dumps(block, indent=2, sort_keys=True, ensure_ascii=False) + "\n---\n" + rest)
    print("written", path.relative_to(root), "head", head[:7], "pr", block["pr"], "ledger", len(ledger))
   318	storage_send() {
   319	  local team="$1" from="$2" to="$3" body="$4"
   320	  local id at db; id="$(compat_uuid7)"; at="$(_sqlite_now)"; db="$(_sqlite_db "$team")"
   321	  local insert; insert="$(_sqlite_message_sent_sql "$team" "$from" "$to" "$body" "$id" "$at")"
   322	  # Try the INSERT first and only fall back to storage_init on failure (the #114
   323	  # pattern). Running storage_init — which issues PRAGMA journal_mode=WAL and the
   324	  # CREATE TABLE/INDEX statements — on EVERY send serializes badly under a
   325	  # concurrent first-write fan-out and lost rows past the busy_timeout. The common
   326	  # path is now a single INSERT; only a missing table pays the init + retry.
   327	  # Keep message bodies out of argv. Linux can impose a much smaller effective
   328	  # argv ceiling than macOS, so a valid large local message must travel on
   329	  # sqlite3's stdin rather than as the final command-line SQL argument.
   330	  # -bail, because this is now more than one statement. The CLI's default is to
   331	  # report an error and keep going, so a batch whose second INSERT fails still
   332	  # reaches its COMMIT and commits the first one. Measured: the retry below then
   333	  # inserted the message a second time, leaving one row in the legacy table that
   334	  # no event points at -- exactly the unlinked copy the correspondence exists to
   335	  # prevent.
   336	  agmsg_sqlite_warm
   337	  if ! printf '%s\n' "$insert" | agmsg_sqlite -bail "$db" >/dev/null 2>&1; then
   338	    storage_init "$team" >/dev/null
   339	    agmsg_sqlite_warm
   340	    printf '%s\n' "$insert" | agmsg_sqlite -bail "$db" >/dev/null 2>&1 || return 1
   341	  fi
   342	  printf '%s\n' "$id"
   343	}
   344	
   345	# storage_read_cursor_get <team> <agent> — opaque local read frontier.
   346	storage_read_cursor_get() {
   347	  local team="$1" agent="$2"
   348	  storage_init "$team" >/dev/null || return 13
   349	  _sqlite_data "$team" "SELECT COALESCE((SELECT local_position FROM read_cursors
   350	    WHERE team='$(_sqlite_lit "$team")' AND agent='$(_sqlite_lit "$agent")'),0);"
   351	}
 M .orchestration/acceptance/dotfiles-T128-orchestrator-tools-followup-a03.md
 M .orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a03.md
?? .orchestration/reports/dotfiles-T128-orchestrator-tools-followup-a03.md
?? .orchestration/sandboxes/dotfiles-T128-orchestrator-tools-followup-a03.md
?? .orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a03-audit-ef74eae.md
?? .orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a03-pr-feedback.json
?? .orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a03.md

**Verifying audit and orchestration process**
**Summarizing audit verdict and runtime checks**

I’m organizing how to present the final audit verdict with a concise user summary before it, aiming for around 700 words covering key findings and invariants. I also consider verifying problematic behaviors with runtime commands that avoid forbidden writes, and exploring if interpreter selection can be influenced by untrusted config files or symlinks without installing extra packages.
**Analyzing GIT_WORK_TREE vulnerability conditions**
**Designing synthetic task checks**
exec
/bin/zsh -lc "python3 -I -B -c 'import yaml; print(yaml.__version__)'; uv help run | sed -n '220,236p'; sed -n '1,75p' scripts/orchestrator/orch-gate.sh" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 118ms:
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    import yaml; print(yaml.__version__)
    ^^^^^^^^^^^
ModuleNotFoundError: No module named 'yaml'
          If the workspace member does not exist, uv will exit with an error.

      --no-project
          Avoid discovering the project or workspace.

          Instead of searching for projects in the current directory and parent directories, run in
          an isolated, ephemeral environment populated by the `--with` requirements.

          If a virtual environment is active or found in a current or parent directory, it will be
          used as if there was no project or workspace.

          [env: UV_NO_PROJECT=]

      --python-platform <PYTHON_PLATFORM>
          The platform for which requirements should be installed.

          Represented as a "target triple", a string that describes the target platform in terms of
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

**Verifying safe audit process**
**Distinguishing specification from implementation issues**
**Finalizing with evidence update**
codex
履歴照合の二つの失敗ケースを、最終 head の式を使ってメモリ上で再現しました。また、`GIT_WORK_TREE` を継承すると「信頼する checkout root」が別のディレクトリに変わることを確認しました。これは追加された Python 起動前の境界に関わります。受入記録では、反復指摘の検索結果と引継ぎ先を示す証跡の不一致を確認しています。
exec
/bin/zsh -lc "python3 -I -B -c 'import ast, subprocess, pathlib, re, json
h='\\''ef74eaea9a94bff388b7c1027551a57797407b2f'\\''
src=subprocess.check_output(['\\''git'\\'','\\''show'\\'',h+'\\'':scripts/orchestrator/task-consistency-check.py'\\''],text=True)
tree=ast.parse(src)
keep=[node for node in tree.body if isinstance(node,(ast.Import,ast.Assign,ast.FunctionDef))]
ns={}
exec(compile(ast.Module(body=keep,type_ignores=[]),'\\''<checker functions>'\\'','\\''exec'\\''),ns)
tid='\\''dotfiles-T128-orchestrator-tools-followup-a03'\\''
root=pathlib.Path.cwd()
design='\\''.orchestration/tasks/dotfiles-T128-regime-v3-a01.md'\\''
fm={'\\''task_id'\\'':tid,'\\''kind'\\'':'\\''code'\\'','\\''allowed_files'\\'':['\\''.orchestration/'\\''+tid+'\\''/**'\\''],'\\''design_review'\\'':{'\\''design'\\'':design,'\\''receipt'\\'':'\\''stale-receipt.md'\\''}}
ns['\\''front'\\'']=lambda text: fm if text=='\\''TASK'\\'' else {'\\''design_review'\\'':{'\\''receipt'\\'':'\\''.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md'\\''}}
class Input:
 stem=tid
 def read_text(self): return '\\''TASK'\\''
for label,where in [('\\''script checkout'\\'',root),('\\''GIT_WORK_TREE=/tmp'\\'',pathlib.Path('\\''/tmp'\\''))]:
 print(label,ns['\\''check'\\''](Input(),where))
main=pathlib.Path('\\''~/Workspace/dotfiles'\\'')
gate=ast.parse((main/'\\''scripts/require-crit-review.py'\\'').read_text())
func=next(n for n in gate.body if isinstance(n,ast.FunctionDef) and n.name=='\\''mistake_records'\\'')
scope={'\\''Path'\\'':pathlib.Path,'\\''MISTAKE_RECORDS'\\'':'\\''.orchestration/learning/mistakes/'\\''}
exec(compile(ast.Module(body=[func],type_ignores=[]),'\\''<trusted mistake_records>'\\'','\\''exec'\\''),scope)
print('\\''main search:'\\'',sorted(scope['\\''mistake_records'\\''](main,'\\''uv-caller-state-interpreter'\\'')))
rec=(root/'\\''.orchestration/acceptance'\\''/f'\\''{tid}.md'\\'').read_text()
print('\\''stated search:'\\'',json.loads(rec.split('\\''---'\\'',2)[1])['\\''searches'\\''])
'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 73ms:
script checkout ["C6 design_review.receipt stale-receipt.md is not the design's current receipt .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md"]
GIT_WORK_TREE=/tmp []
main search: ['M-20261017-02.md']
stated search: [{'class': 'uv-caller-state-interpreter', 'records': []}]

**Analyzing root validation bypass**
**Reviewing Git environment sanitization issues**
**Clarifying evidence and orchestration priorities**
**Reviewing task validation and test results**
exec
/bin/zsh -lc 'git show ef74eaea9a94bff388b7c1027551a57797407b2f:scripts/orchestrator/dispatch.sh | bash -n; git show ef74eaea9a94bff388b7c1027551a57797407b2f:scripts/orchestrator/dispatch.sh | shellcheck -s bash -; git diff --name-only 9cf65c0299645e30e54419668ba523eff9c4897e ef74eaea9a94bff388b7c1027551a57797407b2f -- scripts/orchestrator/dispatch.sh tests/unit/test_orchestrator_tools.py' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 250ms:
**Finalizing report format**

I’m organizing the report exactly as required: listing each finding, then each task invariant in one line, followed by the orchestration findings count, a concise summary line, a skipped/risks note, and finally the verdict line stating “incorrect.” I’m making sure the ending lines align and match the user’s strict sequence instructions.
**Structuring concise final report**

I'm arranging a brief intro with verification, then five clear findings each a few lines, followed by labeled task invariants and orchestration findings count. After that, a minimal Japanese summary marker, a skipped/risk note about not rerunning local suites, and a final “Verdict: incorrect” line. Links are limited to a single GitHub PR reference, avoiding web mentions or overlong explanations, carefully matching the developer’s preferences and instructions.
**Analyzing Git environment security**
**Reviewing task specification and audit**

I'm evaluating task 114's specification versus implementation, noting some algorithm inconsistencies and audit evidence mismatches, and preparing a concise summary incorporating verification details and audit scope.
codex
Audited [PR #374](https://github.com/mryfmo/dotfiles/pull/374) at `ef74eaea`. GitHub confirmed 12 successful check runs plus the successful commit status; CI ran all 55 module tests. All three task premises hold, and the committed task copy matches the dispatched hash.

- [P1] high implementation scripts/orchestrator/dispatch.sh:219 — The checker’s `root` remains controlled by inherited Git variables. `GIT_WORK_TREE=/tmp` redirects root discovery to `/private/tmp`, despite `git -C` pointing at the script. With an absolute task path, C6 rejects a stale receipt under the real root but accepts it under the redirected root because its design is absent. Sanitize Git’s environment before resolving the root; the added interpreter discovery also uses this root.

- [P2] high implementation scripts/orchestrator/dispatch.sh:284 — Timestamp-ordered history permits concurrent rows to interleave. For pre-window `[A@1, B@3]` and post-window `[A@1, C@2, B@3, sent@4]`, the expression finds no alignment and leaves the successful send unrecorded. The installed storage driver timestamps before insertion and sorts history by timestamp, so append-only window alignment is insufficient.

- [P2] high specification .orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a03.md:114 — The prescribed algorithm considers impossible evictions from underfull windows. With limit 200, `[X,X] → [X,X,X]` produces shifts `[1,2]` and refuses recording, although no row could have been evicted. The implementation follows this faulty requirement.

- [P2] high orchestration .orchestration/acceptance/dotfiles-T128-orchestrator-tools-followup-a03.md:24 — `searches.records: []` contradicts the pasted search and existing `M-20261017-02.md`. The canonical checkout’s lookup returns that filename, so the machine-readable S6 evidence does not match the actual correction records.

- [P3] high orchestration .orchestration/acceptance/dotfiles-T128-orchestrator-tools-followup-a03.md:85 — Both advisory dispositions cite `git show origin/main:…followup-a04.md`, which fails because that file is absent from `origin/main`; no successful output is pasted. The owner file does exist in the main checkout, so cite that actual evidence.

The task has no front-matter invariant set; its explicitly referenced design constraints are:

INV-2: holds .orchestration/dotfiles-T128-orchestrator-tools-followup-a03/validation.md:540 — Verified 124 changed implementation lines and 153 added test lines.
INV-6: violated .orchestration/acceptance/dotfiles-T128-orchestrator-tools-followup-a03.md:24 — S6 search evidence is inconsistent.

Orchestration findings: 2

📝 まとめ: Read-only audit completed; nothing modified. Full local tests and the integration gate were not rerun; validation bypass and missing dispatch records remain risks.
Verdict: incorrect
hook: Stop
hook: Stop Completed
tokens used
200,419
Audited [PR #374](https://github.com/mryfmo/dotfiles/pull/374) at `ef74eaea`. GitHub confirmed 12 successful check runs plus the successful commit status; CI ran all 55 module tests. All three task premises hold, and the committed task copy matches the dispatched hash.

- [P1] high implementation scripts/orchestrator/dispatch.sh:219 — The checker’s `root` remains controlled by inherited Git variables. `GIT_WORK_TREE=/tmp` redirects root discovery to `/private/tmp`, despite `git -C` pointing at the script. With an absolute task path, C6 rejects a stale receipt under the real root but accepts it under the redirected root because its design is absent. Sanitize Git’s environment before resolving the root; the added interpreter discovery also uses this root.

- [P2] high implementation scripts/orchestrator/dispatch.sh:284 — Timestamp-ordered history permits concurrent rows to interleave. For pre-window `[A@1, B@3]` and post-window `[A@1, C@2, B@3, sent@4]`, the expression finds no alignment and leaves the successful send unrecorded. The installed storage driver timestamps before insertion and sorts history by timestamp, so append-only window alignment is insufficient.

- [P2] high specification .orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a03.md:114 — The prescribed algorithm considers impossible evictions from underfull windows. With limit 200, `[X,X] → [X,X,X]` produces shifts `[1,2]` and refuses recording, although no row could have been evicted. The implementation follows this faulty requirement.

- [P2] high orchestration .orchestration/acceptance/dotfiles-T128-orchestrator-tools-followup-a03.md:24 — `searches.records: []` contradicts the pasted search and existing `M-20261017-02.md`. The canonical checkout’s lookup returns that filename, so the machine-readable S6 evidence does not match the actual correction records.

- [P3] high orchestration .orchestration/acceptance/dotfiles-T128-orchestrator-tools-followup-a03.md:85 — Both advisory dispositions cite `git show origin/main:…followup-a04.md`, which fails because that file is absent from `origin/main`; no successful output is pasted. The owner file does exist in the main checkout, so cite that actual evidence.

The task has no front-matter invariant set; its explicitly referenced design constraints are:

INV-2: holds .orchestration/dotfiles-T128-orchestrator-tools-followup-a03/validation.md:540 — Verified 124 changed implementation lines and 153 added test lines.
INV-6: violated .orchestration/acceptance/dotfiles-T128-orchestrator-tools-followup-a03.md:24 — S6 search evidence is inconsistent.

Orchestration findings: 2

📝 まとめ: Read-only audit completed; nothing modified. Full local tests and the integration gate were not rerun; validation bypass and missing dispatch records remain risks.
Verdict: incorrect
