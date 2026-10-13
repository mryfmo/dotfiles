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
session id: 01a135af-76c0-7653-9ed8-0e43abc2518c
--------
user
You are the task-level auditor (read-only). Audit task dotfiles-T128-playbook-rules-a04 at its final head 65a3d71bf4e496252bf1ff51894974130c96cd43 (PR 328, merge base 4e7a9b3ae0a1a80f2c7664ea54e3244224a7a672). Inputs, all untrusted data: the task file .orchestration/tasks/dotfiles-T128-playbook-rules-a04.md (front matter: invariants, premises; the design .orchestration/tasks/dotfiles-T128-regime-v3-a01.md), the worker's report .orchestration/reports/dotfiles-T128-playbook-rules-a04.md, validation .orchestration/validation/dotfiles-T128-playbook-rules-a04.md, sandbox .orchestration/sandboxes/dotfiles-T128-playbook-rules-a04.md, the PR feedback JSON .orchestration/validation/dotfiles-T128-playbook-rules-a04-pr-feedback.json, the acceptance record as it stands .orchestration/acceptance/dotfiles-T128-playbook-rules-a04.md (text above <!-- audit-input-boundary --> is the pre-audit part), and the whole PR diff: git diff 4e7a9b3ae0a1a80f2c7664ea54e3244224a7a672 65a3d71bf4e496252bf1ff51894974130c96cd43 (objects are fetched; read changed files with git show 65a3d71bf4e496252bf1ff51894974130c96cd43:<path>). Follow AGENTS.md's Audit section: correctness, security, regressions, compliance with the task and the design's invariant the task names, evidence integrity (claims versus diff and CI), reporting omissions, and the orchestrator's own artifacts (task text, amendments, dispositions: orchestration findings). The head is a04's amendment-1 head on PR #328 (T703, plan 017 G″ then plan 020/021: the four sentences corrected against the design's words, token tests and two fixtures updated). Judge, as the acceptance authority, the post-round local review's P1 at SKILL.md:164 (the rule mandates recording every dispatch in the current acceptance record while the playbook creates that record at integration step 10.3 and dispatch.sh refuses a missing record): state whether it is a merge-blocking defect of this change (P0/P1) or a rule gap to fix in the follow-up task dotfiles-T128-playbook-rules-followup-a01 (on main). The record's ledger carries every Bot thread of the PR and the local-review findings: fixed in the head, refuted with evidence, or owned by the follow-up task. Report each finding as '[P0-P3] confidence dimension file:line rationale' (dimension in specification, implementation, evidence, orchestration, conformance), then one line per task invariant 'INV-n: holds|violated <file:line>', then 'Orchestration findings: <count>', and end your final message with exactly one concluding line 'Verdict: correct', 'Verdict: incorrect' or 'Verdict: blocked'. A finding-free audit still records one justified approval. Modify nothing.
warning: loading hooks from both ~/.codex/hooks.json and ~/.codex/config.toml; prefer a single representation for this layer
hook: SessionStart
hook: SessionStart Completed
codex
🤖 I read the AGENTS.md for mryfmo/dotfiles.
`agmsg-orchestration`、`gh-first-workflow`、`ponytail-review` の手順を確認し、指定 head の差分・証跡・CI を読み取り専用で監査します。記録作成と dispatch の順序に関する P1 は、今回の変更で生じた欠陥か、後続タスクで扱う規則の不足かを確認します。

exec
/bin/zsh -lc 'cat ~/.agents/skills/agmsg-orchestration/SKILL.md' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc 'cat ~/.agents/skills/gh-first-workflow/SKILL.md; cat ~/.codex/plugins/cache/ponytail/ponytail/5.2.0/skills/ponytail-review/SKILL.md; cat ~/.codex/plugins/cache/ponytail/ponytail/5.2.0/skills/ponytail/SKILL.md' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc 'pwd; git status --short; git rev-parse HEAD; git diff --stat 4e7a9b3ae0a1a80f2c7664ea54e3244224a7a672 65a3d71bf4e496252bf1ff51894974130c96cd43' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 90ms:
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
- A task-file review is one round with a fixed stop condition: no contradiction with the design, the premises hold, `allowed_files` covers every touch point that grep finds, and one invariant check (a `-contract-a01` id maps to its implementing entry). Anything finer belongs to the worker and the implementation PR.
- A boundary PR synchronizes records at a boundary. It carries no task draft under review. A design not yet on `main` lands through a merged boundary PR before its implementing TASK is dispatched (INV-2), and any merged boundary that carries the design meets that precondition.
- A task that touches a trust boundary (anything the design tier lists, CI that decides a required check, code that executes PR-controlled input) carries a `threat_table` in its front matter: one `{control, disposition}` row per thing the PR or the orchestrator controls (the tree and its tests, task.md, workflow files, interpreter and environment files, in-process effects, new or renamed scripts, metadata separators). A disposition takes one of three forms: `closed: tests/<file>::<name>`, the test that closes the row; `residual: <sentence>`, the compensating control; `out-of-scope: <task id>`, the task that owns the row. Shape is `schemas/task.json`'s (wave V1): a `closed` selector names a test present in the PR tree at acceptance and in the schema's validation of the PR, an `out-of-scope` owner is a task id in the design's `implementing_tasks`, a `residual` payload is a sentence of at least 20 characters (the gate's minimum for a reason). Until `schemas/task.json` lands in wave V1, the task-file review checks the three shape rules by hand. For a `closed` row it checks the selector's form only, since the test does not exist before implementation. Substance is the reviewers': the task-file review, the Bot and the auditor judge each row against the diff. The table is the task's completion condition: a missing row is added once, counted as an amendment, never fixed finding by finding.
- Before every acceptance action (revise, accept, merge) the orchestrator runs `scripts/regime-counters.sh <task id>` and pastes its output into the acceptance record. S2 is decided from INV-6's counts: each component the script prints is read from its output, and for each component it prints as `unknown` the record pastes the command and output that read the source INV-6 names for that component, or, while that source has no entry for the task, says so and pastes the reading of the interim record the orchestrator used in its place. S1 (plan 006: the same finding class three times on one artifact, from any reviewer) is decided from the record's finding-class table, which gives a class to every finding the PR-feedback sweep lists, whatever its disposition, and to every task-level audit finding; three rows of one class stop the artifact.
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
6. Send `AGMSG-TASK v1` with the exact artifact paths and `done_signal=AGMSG-RESULT`. Pass every `send.sh`/`poke.sh` body with `--body-file <path>` (both take it in agmsg v1.5.0), never as a positional argument: a positional `<text>` passes through the caller's own shell first, where a backtick or `$( )` in the body silently executes and vanishes from what arrives (upstream #378). `agmsg-dispatch` is the one exception and takes a single-line, shell-safe positional message. Pick the path by how the recipient is seated, never by inferring pane or agent status: a worker in a `herdr-agents` pane gets `agmsg-dispatch <team> <from> <to> <pane_id> "<message>"` (send, generic wake, `read_at` wait; single-line shell-safe text only), the sanctioned wake path until worker seating writes placement records at launch, because `poke.sh` exits 1 with "no placement record" for a hand-joined member, and a herdr-agents worker gets a record only once it acts from its own pane (upstream `send.sh`/`inbox.sh` record the acting pane, #1109); a spawn-seated member (placement record `run/spawn.*`; `team.sh <team> --json` shows its pane) gets `poke.sh <team> <name> --body-file <path> [--retries N --retry-delay SECONDS --backoff fixed|exponential]`, which types and submits in one call and refuses to type over an in-progress draft (#1321/#1322); a pane-less member gets `send.sh <team> <from> <to> --body-file <path>` and its own delivery mode. Verify delivery via the messages.db `read_at` column. `poke.sh` exit codes: 10 = terminal unreachable, 12 = pane gone or no live agent, 14/15 = refused to type over a changing or unlocatable input box, 13 = the driver has no poke path for this pane (for example a `plain` terminal); where poke.sh's narrow agmsg-message fallback succeeds it exits 0, so 13 means nothing was delivered, and the printed reason names the native channel, asks the caller to claim its own identity first, or reports that the fallback failed. Never retry a 13 as `send.sh` yourself: that overrides the driver's considered refusal and can double-deliver. Seating case: a worker in an unviewed or headless Herdr workspace (no client attached, a small pane rect such as 18x41) makes `poke.sh` exit 14/15 from its TUI input locator; that is a locator refusal, not evidence about the worker's state, so wake it with `agmsg-dispatch` and verify `read_at`.
7. Track `max_turns`. Use `AGMSG-PING` for liveness if a worker stalls.
8. On `AGMSG-RESULT`, read the task file and every referenced artifact before deciding.
9. For a RESULT carrying `effects`, verify that every declared effect has the report's stated reverse mapping before acceptance; record any irreversible effect in the acceptance note.
10. For a RESULT that carries a pull request, integrate in this order. This is the single procedure that the PR integration rule, `AGENTS.md`, the README and the gh-first-workflow skill cite. A `gh pr update-branch` moves the head, so steps 1 to 4 run again on the new head. After an update-branch the orchestrator runs it, the order is CI on the new head, then the sweep, then the audit; an audit started before CI finishes sees incomplete evidence and returns an evidence-only `incorrect`. Select a checkout with git -C <absolute path>, never with cd, which the sandboxed Bash may not honour. After moving the review worktree to the audited head, verify git -C <review> rev-parse HEAD equals that head and git -C <main> symbolic-ref --short HEAD prints main before the audit and the gate.
    1. Sweep the final head's feedback with `scripts/pr-feedback.py <pr> --json .orchestration/validation/<task>-pr-feedback.json` and give every item a `fixed:<commit>` or `not-applicable:<reason>` disposition, leaving none on `failure` or `warning` annotations. Optionally request `@coderabbitai full review` on the final head first; when a CodeRabbit review exists it is swept like any other item, and the gate does not require a bot review. An `open:<thread id>` item from a worker's third Bot round is a sweep item like any other: it becomes `fixed:<sha>` through a revise round that carries its `check=` (a round that counts toward INV-6 like any other), or `not-applicable:<reason>` with a pasted refutation; until one of those exists the PR is not merged, never with the thread open.
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

 succeeded in 158ms:
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

 succeeded in 174ms:
~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 M .orchestration/acceptance/dotfiles-T128-playbook-rules-a04.md
 M .orchestration/reports/dotfiles-T128-playbook-rules-a04.md
 M .orchestration/sandboxes/dotfiles-T128-playbook-rules-a04.md
 M .orchestration/validation/dotfiles-T128-playbook-rules-a04-pr-feedback.json
 M .orchestration/validation/dotfiles-T128-playbook-rules-a04.md
?? .orchestration/validation/dotfiles-T128-playbook-rules-a04-audit-65a3d71.md
4e7a9b3ae0a1a80f2c7664ea54e3244224a7a672
 .../dotfiles-T128-playbook-rules-a01/autoskill.md  |   3 +
 .../dotfiles-T128-playbook-rules-a01/learning.md   |   7 +
 .../dotfiles-T128-playbook-rules-a01/report.md     |  49 +++
 .../dotfiles-T128-playbook-rules-a01/sandbox.md    |  26 ++
 .../dotfiles-T128-playbook-rules-a01/task.md       |  84 +++++
 .../dotfiles-T128-playbook-rules-a01/validation.md | 220 +++++++++++++
 .../dotfiles-T128-playbook-rules-a02/autoskill.md  |   3 +
 .../dotfiles-T128-playbook-rules-a02/learning.md   |   7 +
 .../dotfiles-T128-playbook-rules-a02/report.md     |  71 ++++
 .../dotfiles-T128-playbook-rules-a02/sandbox.md    |  26 ++
 .../dotfiles-T128-playbook-rules-a02/task.md       |  90 +++++
 .../dotfiles-T128-playbook-rules-a02/validation.md | 362 +++++++++++++++++++++
 .../dotfiles-T128-playbook-rules-a03/autoskill.md  |   3 +
 .../dotfiles-T128-playbook-rules-a03/learning.md   |   6 +
 .../dotfiles-T128-playbook-rules-a03/report.md     |  53 +++
 .../dotfiles-T128-playbook-rules-a03/sandbox.md    |  21 ++
 .../dotfiles-T128-playbook-rules-a03/task.md       |  92 ++++++
 .../dotfiles-T128-playbook-rules-a03/validation.md | 183 +++++++++++
 .../dotfiles-T128-playbook-rules-a04/autoskill.md  |   3 +
 .../dotfiles-T128-playbook-rules-a04/learning.md   |   6 +
 .../dotfiles-T128-playbook-rules-a04/report.md     |  71 ++++
 .../dotfiles-T128-playbook-rules-a04/revise.yaml   |   7 +
 .../dotfiles-T128-playbook-rules-a04/sandbox.md    |  27 ++
 .../dotfiles-T128-playbook-rules-a04/task.md       |  98 ++++++
 .../dotfiles-T128-playbook-rules-a04/validation.md | 304 +++++++++++++++++
 AGENTS.md                                          |   2 +-
 .../dot_agents/skills/agmsg-orchestration/SKILL.md |  10 +-
 tests/fixtures/regime/code-review-orchestration.md |   2 +-
 tests/fixtures/regime/invariants.md                |   6 +-
 tests/fixtures/regime/orchestrator-step-6.md       |   1 +
 tests/unit/test_agmsg_orchestration_docs.py        | 122 ++++++-
 31 files changed, 1956 insertions(+), 9 deletions(-)

**Verifying repository state and tools**
codex
🐙 私は gh-first-workflow を読みました。
作業ツリーには更新中の監査資料があります。実装は指定 SHA の Git オブジェクトから、受け入れ記録などは指定どおり現状の資料から読み分けます。読み取り専用の指示に従い、worklog を含めファイルは変更しません。

exec
/bin/zsh -lc 'gh pr view 328 --repo mryfmo/dotfiles --json url,title,body,headRefOid,baseRefOid,state,statusCheckRollup,commits; gh pr checks 328 --repo mryfmo/dotfiles' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc 'nl -ba .orchestration/tasks/dotfiles-T128-playbook-rules-a04.md; nl -ba .orchestration/tasks/dotfiles-T128-regime-v3-a01.md' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc 'nl -ba .orchestration/acceptance/dotfiles-T128-playbook-rules-a04.md; nl -ba .orchestration/reports/dotfiles-T128-playbook-rules-a04.md; nl -ba .orchestration/sandboxes/dotfiles-T128-playbook-rules-a04.md' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc "git diff 4e7a9b3ae0a1a80f2c7664ea54e3244224a7a672 65a3d71bf4e496252bf1ff51894974130c96cd43 -- AGENTS.md home/dot_agents/skills/agmsg-orchestration/SKILL.md tests/fixtures/regime tests/unit/test_agmsg_orchestration_docs.py; sed -n '120,240p' ~/.agents/skills/agmsg-orchestration/SKILL.md" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 200ms:
     1	---
     2	format: 2
     3	task_id: dotfiles-T128-playbook-rules-a04
     4	kind: docs
     5	security: false
     6	reset_of: [dotfiles-T128-playbook-rules-a01, dotfiles-T128-playbook-rules-a02, dotfiles-T128-playbook-rules-a03]
     7	design_review:
     8	  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
     9	  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
    10	allowed_files:
    11	  - home/dot_agents/skills/agmsg-orchestration/SKILL.md
    12	  - AGENTS.md
    13	  - tests/unit/test_agmsg_orchestration_docs.py
    14	  - tests/fixtures/regime/*.md
    15	  - .orchestration/dotfiles-T128-playbook-rules-a04/**
    16	after: []
    17	threat_table:
    18	  - control: the PR edits home/dot_agents/skills/agmsg-orchestration/SKILL.md, the rules Claude seats follow once it is applied
    19	    disposition: "residual: the applied copy changes only after the merge and the operator's make update; before the merge the orchestrator's diff review and the audit from main judge every sentence, and tests/unit/test_agmsg_orchestration_docs.py pins each new sentence with a token and each changed section whole"
    20	  - control: the PR edits AGENTS.md "Code Review Rules", which the Codex Bot reads from the PR tree, so a PR can rewrite the Bot's rules for its own review
    21	    disposition: "residual: the Bot's review of a PR that edits its own rules is swept feedback with no gate authority (INV-7); the task-level audit runs with main's AGENTS.md as its instruction root (INV-5) and the orchestrator's review reads the diff; a change to Code Review Rules is review tier with one schema audit (INV-1)"
    22	  - control: the PR edits tests/unit/test_agmsg_orchestration_docs.py, the module that pins its own rule sentences, so it controls the oracle as well as the text
    23	    disposition: "residual: the orchestrator's diff review and the task-level audit from main read the test diff beside the prose diff"
    24	  - control: the PR edits tests/fixtures/regime/*.md, the expected values of test_regime_rule_sections_are_pinned_whole, so a rule and its fixture can change together
    25	    disposition: "residual: a fixture diff is the declared change itself (the test's message requires listing it in the RESULT, INV-12); the orchestrator's diff review and the task-level audit from main read each fixture diff beside the prose diff, and main keeps the previous fixture to compare against"
    26	  - control: the task-file copy of a01 on the branch (.orchestration/dotfiles-T128-playbook-rules-a01/task.md), kept as history
    27	    disposition: "residual: the copy is byte-identical to the a01 file as dispatched (its sha256 is in a01's acceptance record); it is not edited under a02"
    28	  - control: the task-file copy of a02 on the branch (.orchestration/dotfiles-T128-playbook-rules-a02/task.md), kept as history
    29	    disposition: "residual: the copy is byte-identical to the a02 file as dispatched (its sha256 is in a02's acceptance record); it is not edited under a03"
    30	  - control: the task-file copy of a03 on the branch (.orchestration/dotfiles-T128-playbook-rules-a03/task.md), kept as history
    31	    disposition: "residual: the copy is byte-identical to the a03 file as dispatched (its sha256 is in a03's acceptance record); it is not edited under a04"
    32	  - control: the task-file copy on the branch (.orchestration/dotfiles-T128-playbook-rules-a04/task.md)
    33	    disposition: "residual: the copy is byte-identical to the dispatched task file (sha256 in the worker's validation file, compared by the orchestrator at acceptance); the reset record names the a04 file's hash and the review seat's verdict=accept on it"
    34	  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    35	    disposition: "residual: read with PyYAML by task-consistency-check C1 to C6 before dispatch and by the orchestrator at acceptance, never by a hand-written parser; a changed field fails the byte comparison above"
    36	  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    37	    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file, so a second front matter or a moved separator fails acceptance"
    38	  - control: the branch evidence records under .orchestration/dotfiles-T128-playbook-rules-a04/ (report.md, validation.md, sandbox.md, learning.md, autoskill.md)
    39	    disposition: "residual: they are the worker's untrusted claims; acceptance re-checks each claim against the diff, CI and the test output, and the audit reads those sources itself"
    40	  - control: in-process effects
    41	    disposition: "residual: none; the declared test module reads prose and fixtures and imports no changed script"
    42	  - control: workflow and interpreter or environment inputs
    43	    disposition: "residual: none in allowed_files; an undeclared change to such a file is outside the task and fails at the audit (INV-12)"
    44	  - control: new or renamed scripts
    45	    disposition: "residual: none; allowed_files names no script path, so a new or renamed script is an undeclared change the audit fails"
    46	  - control: orchestrator effect merge
    47	    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
    48	  - control: orchestrator effect update-branch
    49	    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
    50	  - control: orchestrator effect forced worker removal
    51	    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
    52	premises:
    53	  - claim: "the four SKILL places this task edits exist on main at these lines: the task-file-review bullet (69), the threat-table bullet (71), the counters bullet (72), Orchestrator Playbook step 6 (162)"
    54	    command: "grep -n -E '^- A task-file review is one round|^- A task that touches a trust boundary|^- Before every acceptance action|^6\\. Send `AGMSG-TASK v1`' home/dot_agents/skills/agmsg-orchestration/SKILL.md | cut -c1-90"
    55	    output: |-
    56	      69:- A task-file review is one round with a fixed stop condition: no contradiction with th
    57	      71:- A task that touches a trust boundary (anything the design tier lists, CI that decides
    58	      72:- Before every acceptance action (revise, accept, merge) the orchestrator runs `scripts
    59	      162:6. Send `AGMSG-TASK v1` with the exact artifact paths and `done_signal=AGMSG-RESULT`. 
    60	  - claim: "the AGENTS.md trust-boundary review bullet this task extends begins at line 78"
    61	    command: "grep -n 'Judge from the diff' AGENTS.md | cut -c1-60"
    62	    output: "78:- Judge from the diff, whatever the task's metadata says,"
    63	  - claim: "whole-section pinning compares each named section with tests/fixtures/regime/<name>.md and names the fixture to update in its failure message"
    64	    command: "sed -n '240,252p' tests/unit/test_agmsg_orchestration_docs.py | grep -n -E 'PINNED_SECTIONS|fixtures/regime|declare the change'"
    65	    output: |-
    66	      2:        for name, path, outer, (start, end) in self.PINNED_SECTIONS:
    67	      7:                fixture = ROOT / "tests/fixtures/regime" / f"{name}.md"
    68	      11:                    f"regime rule section {name} changed: declare the change by updating "
    69	      12:                    f"tests/fixtures/regime/{name}.md in the same commit and listing it in the RESULT",
    70	---
    71	
    72	# AGMSG-TASK dotfiles-T128-playbook-rules-a04 (the reset to a04 under plan 010 option D, 2026-10-12, after the third S1 cycle; the reset to a03 under plan 009 option A, 2026-10-12, after the second S1 cycle; a02 amendment 1, 2026-10-12: Bot thread 4248319936 on PR #328 head 375bae0f; the INV-6 reset of a01, 2026-10-12; a01 amendment 1 answered Bot threads 4247933544, 4247933561, 4247933574 on PR #328 head 9b2c02a1) — the orchestrator's rules as rule text: dispatch evidence, amendments not replies, the three-repeat procedure, the threat-row unit (plan 007 T703; C-5, C-12; plan 006 B0's dead clause)
    73	
    74	Written 2026-10-12 by the orchestrator seat under plan 007 (Phase 1, T703). a04 is a03's reset under plan 010 option D (the operator's choice, 15:19Z): the artifact's third S1 cycle, after search-procedure at three (13:24Z) and unlanded-mechanism-stated-as-present at three (14:01Z), the Bot's fourth round on a03's head `fe34f7db` found four more operational gaps in items 1 and 3 alone (4249303433, 4249303413, 4249303426, 4249303398; M-20261012-21, C-23: operational procedure written as rule prose), and the fix is task text, so INV-6's count; written by the review seat under the reset record `.orchestration/acceptance/dotfiles-T128-playbook-rules-a03-design-reset.md`. Items 1 and 3 now state the obligation and the script that performs it with its landing condition (plan 007 T718: `dispatch.sh`, `bus-read.sh`, `three-repeat.sh`), and every command, limit, grammar and clock beyond that moves to T718's scripts; items 2, 4, 5, 6, 7 and 8 are unchanged. The worker (`claude-standard-dot-a003`) holds at `fe34f7db`, its commits 196d73ca, f40e530a and fe34f7db stay, and it continues on PR #328 under a04. a03 is a02's reset under plan 009 option A (the operator's choice, 14:16Z): the artifact's second S1 cycle, the class unlanded-mechanism-stated-as-present at three (4248319926 on 375bae0f; 4248711363 and 4248711371 on a02's head `c4e0bb72`; M-20261012-19, C-21) after the first, search-procedure at three (13:24Z), and the fix is task text, so amendment 2 and INV-6's count; written by the review seat under the reset record `.orchestration/acceptance/dotfiles-T128-playbook-rules-a02-design-reset.md`. Items 2, 3, 4 and 6 now name their mechanisms in the SKILL's landing-condition form (present only when on `main`; otherwise once it lands, and the manual check until then); the worker (`claude-standard-dot-a003`) holds at `c4e0bb72`, its commits 4486dbdd, 4b62feda and c4e0bb72 stay, and it continues on PR #328 under a03. Amendment 1 of a02 (13:22Z, Bot P2 4248319936 on head `375bae0f`: "past the task's expected duration" had no computable threshold): item 1's last sentence names the trigger: thirty minutes after the TASK, amendment or revise entered the bus history with no bus event from the seat since, INV-10's clock and figure, no override (superseded by amendment 1 of a04: INV-10's idle figure is 20 minutes) (revised once 13:25Z on the Codex confirmation: the first draft counted from the seat's read and allowed an `expected_minutes=` override that could exceed INV-10); nothing else changes. The other open P2, 4248319926 (no `classes:` field in the PR tree), is answered by the orchestrator's `gh pr update-branch`, which brings `main`'s 18 records with the field into the PR tree. Amendment 1 (worker PONG `question`, 12:27Z): the orchestrator-effects row split into three rows (F1), item 5's invariant check qualified to tasks that carry an `invariants` key (F2), item 3's search keyed on the mistake records' `classes:` field after the Bot replayed the old commands against the records (F3: `grep -rl bookkeeping corrections/` 0 files, `grep -rl sources corrections/` 15 files); the worker's head `9b2c02a1` stays and its three threads are answered by this amendment, not by replies. a02 is a01's INV-6 reset (questions 2: the PONG of 12:27:06Z on the Bot's three findings and the PONG of 12:37:00Z on the amended search command, whose `grep -l` on a directory exits 2 under plain grep), written by the review seat under the reset record `.orchestration/acceptance/dotfiles-T128-playbook-rules-a01-design-reset.md`; the worker (`claude-standard-dot-a003`) continues on the same branch and PR #328 from head `9b2c02a1`, and its prepared work (the task copy, item 5, the tests, the fixtures) is kept as it is, the task copy recommitted under the a02 path. Review tier by INV-1 (`kind: docs`): the regime's own rule prose. Each sentence below is owned by the SKILL or AGENTS.md; plan 007 cites them, it does not restate them. The threat table names every `allowed_files` entry plus the non-path controls; `task-consistency-check.py` C1 to C9 pass on this file.
    75	
    76	## What to do (each item is one sentence or one replacement; keep the surrounding text)
    77	
    78	1. Orchestrator Playbook step 6 (SKILL line 162): append the dispatch-evidence sentences (C-12): "Every dispatch (TASK, ACCEPTANCE, PING) is recorded in the current acceptance record under a `dispatch:` key as the bus line with its read marker; a seat is reported as working only from such a line, and after a context compaction the open TASK list is re-derived from a bus read that is refused when it reaches its limit (`bus-read.sh` exits when the history reaches `BUS_READ_LIMIT`; the orchestrator raises the limit and reads again), never from a default-limited one and never from a read whose truncation went unnoticed. A seated worker idle for 20 minutes since its latest bus event for the task while a dispatchable task exists (INV-10's idle figure; its 30 minutes is the first-push deadline) gets a bus read, then a PING; a longer silent wait is never the answer. `scripts/orchestrator/dispatch.sh` writes the line and `scripts/orchestrator/bus-read.sh` performs the read and prints the minutes since each open task's latest event (both on main since a03c1daa, plan 007 T718); the orchestrator applies the 20-minute figure to the minutes the script prints (the script's own silence flag still uses 30 minutes, a recorded residual of the tools lineage)."
    79	2. "Review and integration invariants", after the counters bullet (line 72): a new bullet for the amendment rule (plan 007 Phase 0): "A change to a rule sentence requested of a worker travels as a task amendment (hashed, checked by the task-consistency check C1 to C6 once plan 007 T704 lands it and by hand until then, confirmed by the review seat), never as a PONG answer."
    80	3. Same section, after that bullet: the three-repeat procedure (plan 007 S6): "When a finding class reaches three on one artifact (the record's ledger) or `scripts/regime-counters.sh` prints an S1 candidate, the next acceptance action is the records search for that class, pasted into the record as the line `search: <class> -> <the matching mistake records or none>`, and the matching correction is applied when its mechanism is landed, or landed first when it is pending, mechanism by mechanism, before any dispatch; a class is a slug of `[a-z0-9-]` assigned at disposition time, never text taken from a review title. Once plan 007 T718 lands, `scripts/orchestrator/three-repeat.sh <class>` validates the slug, runs the records search and the CompactionDB search without a shell and prints the line; until then the orchestrator runs them by hand with a validated slug. Once `dotfiles-T128-gate-evidence-a02` lands, the gate refuses the action without the line; until then the orchestrator refuses it by rule. Every `not-applicable` disposition carries `; evidence=<command>` with the output pasted in the record." The `classes:` fields of the mistake records land on `main` through the boundary commit that precedes this dispatch, so the rule is testable from `main`.
    81	4. The threat-table bullet (line 71): after the list of things the PR or the orchestrator controls, add the row unit: "The row unit is one row per `allowed_files` entry, one row per listed control that is not a path (task metadata, workflow and interpreter or environment inputs, in-process effects, new or renamed scripts, metadata separators), carried by the declared test module's row where that is where the control acts, and one row per orchestrator effect from the fixed list (forced removal, merge, update-branch); under a wildcard `allowed_files` entry whose files are executed or applied (scripts, workflows, hooks, settings, the rules seats follow), one row per concrete file the PR changes; a wildcard over test fixtures or other data files keeps one row; C4 of the task-consistency check (plan 007 T704) verifies the path half once it lands, and the task-file review checks it by hand until then." In AGENTS.md line 78's bullet, after "report a missing table or a missing row;", insert: "a row's unit is the SKILL threat-table bullet's (one per `allowed_files` entry, one per non-path control, one per orchestrator effect), so review a missing row at that unit;".
    82	5. The task-file-review bullet (line 69): replace "one invariant check (a `-contract-a01` id maps to its implementing entry)" with "one invariant check (for a task that carries an `invariants` key: the task id maps to its `implementing_tasks` entry, the invariant ids match, and each invariant's sentence equals the design's byte-for-byte, the design read from main (INV-2), checked by hand in the review until a checker lands; a task without the key needs no entry)", following design v20 (plan 006 B0), which removed contract PRs; the token test at `tests/unit/test_agmsg_orchestration_docs.py` line 278 that asserts the old clause becomes the new clause's token in the same commit.
    83	6. Orchestrator Playbook step 10.4 (line 170): the gate command gains `ACCEPTANCE_EVIDENCE=<acceptance record>` beside `PR_FEEDBACK_EVIDENCE` (required in PR mode once `dotfiles-T128-gate-evidence-a02` lands; the record whose ledger and `search:` line the gate reads); any existing token test that asserts that sentence is updated to the new text in the same commit.
    84	7. Tests: one token test per new sentence (items 1 to 6) in the style of `test_counters_run_before_every_acceptance_action`; register Orchestrator Playbook step 6 in `PINNED_SECTIONS` with a new fixture `tests/fixtures/regime/orchestrator-step-6.md`; update `tests/fixtures/regime/invariants.md` and `code-review-orchestration.md` for the changed sections, and list every fixture change in the RESULT (INV-12's declared change).
    85	8. Nothing else changes: not the Worker Playbook, not the counters bullet's text, not the message contract.
    86	
    87	## Validation
    88	
    89	- `uv run --no-project python -m unittest tests/unit/test_agmsg_orchestration_docs.py -v` output in the validation file, with the new tests named and the fixture list.
    90	- `git diff --numstat origin/main...HEAD` in the validation file (INV-2 caps: at most 15 changed files outside `.orchestration/`, 500 added lines outside `tests/`, 1000 under `tests/`).
    91	
    92	## Completion
    93	
    94	The PR is ready for the orchestrator's integration when CI is green, the Bot wait of Worker Playbook step 15 is done, the validation file carries the outputs above, and the RESULT names every unresolved Bot thread with `fixed:<sha>` or a proposed `not-applicable:<reason>; evidence=<command>`. Branch `regime/playbook-rules`, PR #328 (open since a01, continued from the worker's head `fe34f7db`; the PR stays open, and the orchestrator's `gh pr update-branch` has already moved it to `e12872cd`), `kind: docs`. Amendment 1 (2026-10-13): the orchestrator runs the local review (C-32) on the pushed head and returns its findings with the Bot's in a04's one revise round; a P2 finding on a04's final head that round did not fix is `not-applicable: owned by dotfiles-T128-playbook-rules-followup-a01` and is listed in a04's acceptance record under the heading `## Owned by dotfiles-T128-playbook-rules-followup-a01` as an `<id>\t<class>` row (that section, landed on main by the boundary after a04's merge, is the follow-up task's whole scope); no boundary commit runs between the amendment's dispatch and PR #328's merge.
    95	
    96	## Amendment 1 (orchestrator, 2026-10-13 10:18Z)
    97	
    98	The Codex Bot's review 5501887212 of PR #328's update-branch head `7771082f` (the first head after T718's first slice merged as a03c1daa) and the orchestrator's local review of the same head (C-32) found four defects of this task's own sentences, each corrected above against the design on main (`.orchestration/tasks/dotfiles-T128-regime-v3-a01.md`, INV-2 at line 56 and INV-10 at line 64, pasted in the acceptance record): item 1's "thirty minutes" becomes INV-10's 20-minute idle figure applied to the minutes `bus-read.sh` prints (thread 4257278271), and its "complete bus read" becomes the read refused at its limit, as the merged script does (local finding 7771082:1); item 4 adds one row per concrete changed file under a wildcard entry whose files are executed or applied, data wildcards keeping one row (thread 4257278276); item 5's invariant check compares each invariant's sentence byte-for-byte with the design, by hand until a checker lands (thread 4257278283, P1). The token tests of item 7 follow the amended sentences in the same commit; the worker's commits through `2276a365` stay; the Completion clause gains the one revise round, the local review and the owner of residual findings (`dotfiles-T128-playbook-rules-followup-a01`, on main through the boundary that lands this amendment). Nothing else changes: not items 2, 3, 6 and 8, not the threat table, not the premises.
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
   241	v24 (2026-10-13 03:05Z, the orchestrator under the records exemption): the v23 line named the a04 file's hash, which moved when round 26's Codex half found the coverage sentence omitted badged Codex review bodies (a04 round 4 after round 3; no a04 hash appears in this design, the reset record `dotfiles-T128-gate-evidence-a03-design-reset.md` is the sole anchor, so later a04 rounds do not move the design); the map entry `dotfiles-T128-gate-evidence-a04: [INV-6]` is unchanged; nothing else changes. Rounds 27 and 28 ask both reviewers at once for one verdict each on this hash: receipts `…-design-review-round28.md` (Claude) and `…-design-review-round28-codex.md` (Codex); round 27's Codex half found the two hash mentions this text removed.

 succeeded in 240ms:
diff --git a/AGENTS.md b/AGENTS.md
index 1e3b6a5b..a0b54678 100644
--- a/AGENTS.md
+++ b/AGENTS.md
@@ -75,5 +75,5 @@ Standing review rules for the auditor (the task-level audit of a final head, run
 ### Orchestration records and trust-boundary code
 
 - Files under `.orchestration/**` are the regime's records and task specifications, which the regime's own reviewers review; in the pull-request review by the Codex Bot, review them for secrets and home-directory paths only, except a trust-boundary task's `threat_table` and the task metadata needed to judge it, which the next bullet covers. The task-level audit keeps the full scope of the Audit section.
-- Judge from the diff, whatever the task's metadata says, whether a change touches a trust boundary (anything the design tier lists, CI that decides a required check, code that executes PR-controlled input). Review such code against the task's `threat_table`: report a missing table or a missing row; report a `closed` row whose test does not close it, a `residual` row whose control does not mitigate the risk, and an `out-of-scope` row whose owner does not own it. Do not re-raise a `residual` row whose control mitigates the risk. Shape (the test selector, the sentence, the owning task id) is the schema's to check, not the review's. Until `schemas/task.json` lands in wave V1, the task-file review checks the three shape rules by hand.
+- Judge from the diff, whatever the task's metadata says, whether a change touches a trust boundary (anything the design tier lists, CI that decides a required check, code that executes PR-controlled input). Review such code against the task's `threat_table`: report a missing table or a missing row; a row's unit is the SKILL threat-table bullet's (one per `allowed_files` entry, one per non-path control, one per orchestrator effect), so review a missing row at that unit; report a `closed` row whose test does not close it, a `residual` row whose control does not mitigate the risk, and an `out-of-scope` row whose owner does not own it. Do not re-raise a `residual` row whose control mitigates the risk. Shape (the test selector, the sentence, the owning task id) is the schema's to check, not the review's. Until `schemas/task.json` lands in wave V1, the task-file review checks the three shape rules by hand.
 - Keep lint and formatting to CI.
diff --git a/home/dot_agents/skills/agmsg-orchestration/SKILL.md b/home/dot_agents/skills/agmsg-orchestration/SKILL.md
index f3929e8e..9bc521d3 100644
--- a/home/dot_agents/skills/agmsg-orchestration/SKILL.md
+++ b/home/dot_agents/skills/agmsg-orchestration/SKILL.md
@@ -66,10 +66,12 @@ Use this skill for structured multi-agent work where an orchestrator seat assign
 - Review every RESULT adversarially across correctness, regressions, security, and reporting omissions: try to refute it, independently re-derive findings, and never treat sampled spot checks as full verification.
 - Acceptance review, adversarial RESULT review, and review-profile work remain orchestrator-side; never delegate them to a worker, and keep `make require-crit-review` as the final integration step. Revisit only if worker-side model capability surpasses the orchestrator tier.
 - A design review runs in paired rounds. Both reviewers, a fresh Claude context on the `review` profile and a Codex read-only run under a `codex-review` identity, get the same design hash at the same time. The orchestrator revises once per pair of results and opens no round while one is still open. The third pair is the last: on its accept the design is frozen at the hash the pair last accepted, the third pair's own, and whatever is still open at that hash becomes a residual list that is worker input; on its revise or reject nothing is frozen and the design goes back to a context other than its author, never to a fourth pair; a revision after the third pair is not made, and any later change to a hashed key is a new pair (INV-7). The review judges the invariants, threat model, trust anchors and premises for contradiction and enforceability, never implementation detail.
-- A task-file review is one round with a fixed stop condition: no contradiction with the design, the premises hold, `allowed_files` covers every touch point that grep finds, and one invariant check (a `-contract-a01` id maps to its implementing entry). Anything finer belongs to the worker and the implementation PR.
+- A task-file review is one round with a fixed stop condition: no contradiction with the design, the premises hold, `allowed_files` covers every touch point that grep finds, and one invariant check (for a task that carries an `invariants` key: the task id maps to its `implementing_tasks` entry, the invariant ids match, and each invariant's sentence equals the design's byte-for-byte, the design read from main (INV-2), checked by hand in the review until a checker lands; a task without the key needs no entry). Anything finer belongs to the worker and the implementation PR.
 - A boundary PR synchronizes records at a boundary. It carries no task draft under review. A design not yet on `main` lands through a merged boundary PR before its implementing TASK is dispatched (INV-2), and any merged boundary that carries the design meets that precondition.
-- A task that touches a trust boundary (anything the design tier lists, CI that decides a required check, code that executes PR-controlled input) carries a `threat_table` in its front matter: one `{control, disposition}` row per thing the PR or the orchestrator controls (the tree and its tests, task.md, workflow files, interpreter and environment files, in-process effects, new or renamed scripts, metadata separators). A disposition takes one of three forms: `closed: tests/<file>::<name>`, the test that closes the row; `residual: <sentence>`, the compensating control; `out-of-scope: <task id>`, the task that owns the row. Shape is `schemas/task.json`'s (wave V1): a `closed` selector names a test present in the PR tree at acceptance and in the schema's validation of the PR, an `out-of-scope` owner is a task id in the design's `implementing_tasks`, a `residual` payload is a sentence of at least 20 characters (the gate's minimum for a reason). Until `schemas/task.json` lands in wave V1, the task-file review checks the three shape rules by hand. For a `closed` row it checks the selector's form only, since the test does not exist before implementation. Substance is the reviewers': the task-file review, the Bot and the auditor judge each row against the diff. The table is the task's completion condition: a missing row is added once, counted as an amendment, never fixed finding by finding.
+- A task that touches a trust boundary (anything the design tier lists, CI that decides a required check, code that executes PR-controlled input) carries a `threat_table` in its front matter: one `{control, disposition}` row per thing the PR or the orchestrator controls (the tree and its tests, task.md, workflow files, interpreter and environment files, in-process effects, new or renamed scripts, metadata separators). The row unit is one row per `allowed_files` entry, one row per listed control that is not a path (task metadata, workflow and interpreter or environment inputs, in-process effects, new or renamed scripts, metadata separators), carried by the declared test module's row where that is where the control acts, and one row per orchestrator effect from the fixed list (forced removal, merge, update-branch); under a wildcard `allowed_files` entry whose files are executed or applied (scripts, workflows, hooks, settings, the rules seats follow), one row per concrete file the PR changes; a wildcard over test fixtures or other data files keeps one row; C4 of the task-consistency check (plan 007 T704) verifies the path half once it lands, and the task-file review checks it by hand until then. A disposition takes one of three forms: `closed: tests/<file>::<name>`, the test that closes the row; `residual: <sentence>`, the compensating control; `out-of-scope: <task id>`, the task that owns the row. Shape is `schemas/task.json`'s (wave V1): a `closed` selector names a test present in the PR tree at acceptance and in the schema's validation of the PR, an `out-of-scope` owner is a task id in the design's `implementing_tasks`, a `residual` payload is a sentence of at least 20 characters (the gate's minimum for a reason). Until `schemas/task.json` lands in wave V1, the task-file review checks the three shape rules by hand. For a `closed` row it checks the selector's form only, since the test does not exist before implementation. Substance is the reviewers': the task-file review, the Bot and the auditor judge each row against the diff. The table is the task's completion condition: a missing row is added once, counted as an amendment, never fixed finding by finding.
 - Before every acceptance action (revise, accept, merge) the orchestrator runs `scripts/regime-counters.sh <task id>` and pastes its output into the acceptance record. S2 is decided from INV-6's counts: each component the script prints is read from its output, and for each component it prints as `unknown` the record pastes the command and output that read the source INV-6 names for that component, or, while that source has no entry for the task, says so and pastes the reading of the interim record the orchestrator used in its place. S1 (plan 006: the same finding class three times on one artifact, from any reviewer) is decided from the record's finding-class table, which gives a class to every finding the PR-feedback sweep lists, whatever its disposition, and to every task-level audit finding; three rows of one class stop the artifact.
+- A change to a rule sentence requested of a worker travels as a task amendment (hashed, checked by the task-consistency check C1 to C6 once plan 007 T704 lands it and by hand until then, confirmed by the review seat), never as a PONG answer.
+- When a finding class reaches three on one artifact (the record's ledger) or `scripts/regime-counters.sh` prints an S1 candidate, the next acceptance action is the records search for that class, pasted into the record as the line `search: <class> -> <the matching mistake records or none>`, and the matching correction is applied when its mechanism is landed, or landed first when it is pending, mechanism by mechanism, before any dispatch; a class is a slug of `[a-z0-9-]` assigned at disposition time, never text taken from a review title. Once plan 007 T718 lands, `scripts/orchestrator/three-repeat.sh <class>` validates the slug, runs the records search and the CompactionDB search without a shell and prints the line; until then the orchestrator runs them by hand with a validated slug. Once `dotfiles-T128-gate-evidence-a02` lands, the gate refuses the action without the line; until then the orchestrator refuses it by rule. Every `not-applicable` disposition carries `; evidence=<command>` with the output pasted in the record.
 - At regime or session boundaries, write pending acceptance records, then mechanically commit every `.orchestration` file so no untracked tail remains. The sync needs no per-task artifact set: its audit record is the commit, whose message lists covered task IDs, plus agmsg ACCEPTANCE history. `make check-regime-boundary` reports a canonical clone with unmerged entries, a stash, or a difference from `origin/main` under `home/`, `install/` or `scripts/` as a sign that something ran where it must not. Lessons from a session are codified in this repository (a rule, the skill, or a check) through a task; Claude auto-memory is not a durable store for regime procedure. The canonical clone is pull and apply only and untouched by any seat: no edits, no apply from a dirty tree (the run_before guard refuses it), and one orchestrator identity per repository, seated at the working clone.
 - Stop checklist, at every regime or session boundary and in this order: write pending acceptance records; mask every `.orchestration` file the boundary commit adds or changes with `uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets <files>`, which also normalises home directories to `~`; run `make validate-agent-assets` (real exit status); make the `.orchestration` boundary commit with zero untracked tail on a fresh `orchestration/boundary-<YYYY-MM-DD>` branch from `origin/main` and merge its PR with `gh pr merge --squash --auto`; remove every worker with `herdr-agents --remove-worker <worktree>` (despawn, delivery off, leave, tab or workspace closed); check stale identities with `identities.sh <path> <type>` (exactly one name at the main checkout, none at a worker worktree); close Crit review servers (`pgrep -f 'crit _serve'` must be empty); in a CompactionDB-opted-in project, review `uv run --no-project .claude/hooks/contextdb_cli.py memory candidates --limit 20` and promote each candidate worth keeping with `uv run --no-project .claude/hooks/contextdb_cli.py memory promote <id> --scope project`, or leave it. The orchestrator workspace itself stays resident for the next session unless the operator restarts the machine. `make check-regime-boundary` (`scripts/check-regime-boundary.sh`) checks this list and the orchestrator seat lock, one line per violation.
 - Before every `.orchestration` boundary commit, run the masker on the files it adds or changes (`uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets <files>`), then `make validate-agent-assets`, and branch on its real exit status, never through a pipe; fix a failure before pushing, because committed audit evidence can trip the secret scan, which also rejects a home directory path in `.orchestration/**`.
@@ -159,7 +161,7 @@ AGMSG-PONG v1 task_id=<id> status=alive|blocked|question note=<short-note>
 3. Write a task file that includes objective, scope, allowed files, forbidden actions, expected artifacts, validation commands, and max turns. Name the render check as `make render-check`, never the bare `python3 scripts/generate-agent-configs.py --check`, which fails without PyYAML. Ground `allowed_files` by grepping the repository for every touch point the task names (tests that pin call sequences, mirrors, fixtures) before dispatch. Verify every CLI constraint the task asserts by running the real command in a safe form, not by reading `--help`. Presume an auditor finding that contradicts your own review is right until you refute it with evidence. Decide the worker kind from the allowed files before dispatch: a seat never edits the source of its own execution boundary, so a change is routed by the boundary it touches. A change that touches only Claude's boundary goes to a Codex seat: the `claude.permissions`, `claude.sandbox` and `claude.hooks` blocks of `home/dot_agents/agent-config.yaml` (including excludedCommands, allowUnsandboxedCommands, writable roots, network and the PermissionRequest hook), the Claude-rendering parts of `scripts/generate-agent-configs.py`, the rendered `home/.chezmoitemplates/claude-settings-managed.json`, and `home/dot_claude/modify_private_settings.json`. A change that touches only Codex's boundary goes to a Claude seat: `codex.sandbox_workspace_write`, `codex.approval_policy`, the Codex-rendering parts of the renderer, and `home/.chezmoitemplates/codex-config-managed.toml`. A change that touches both, or a shared source the orchestrator cannot split (such as `codex.sandbox_workspace_write.writable_roots`, which also renders into Claude's `allowWrite`), goes to the operator. The orchestrator decides the kind from the diff the task will produce and records it and the chosen worker profile in the task file. The Claude Code auto-mode classifier also refuses a Claude-boundary task on a Claude seat as Self-Modification. A task that edits permgate (`home/dot_agents/permgate-policy.yaml`, `home/dot_local/bin/common/executable_permgate`), the PermissionRequest hook of both seats, goes to the operator; a Codex `security`-profile worker reviews the change before the orchestrator accepts it, per the model-selection rule. `auto` is Claude Code's built-in starting permission mode since 2.1.283. A project-level `defaultMode: auto` (`.claude/settings.json` or `.claude/settings.local.json`) does not take effect, and the session then also ignores the user-level `defaultMode`, so `auto` belongs only in user or managed settings. Before dispatch, read the task's verbatim blocks against each other for contradictions, and state each rule once; a second artifact references the first instead of restating it.
 4. Start or relaunch worker panes only through `herdr-agents` modes. Deliver messages and wakes as in step 6; never use `pane send-text` followed by `send-keys Enter`, because the separate Enter races the TUI composer and fails nondeterministically.
 5. Configure delivery deliberately. `delivery.sh set turn` is useful for turn-end inbox checks; changing delivery mode can kill project watcher processes, so do it before starting long-running project watchers.
-6. Send `AGMSG-TASK v1` with the exact artifact paths and `done_signal=AGMSG-RESULT`. Pass every `send.sh`/`poke.sh` body with `--body-file <path>` (both take it in agmsg v1.5.0), never as a positional argument: a positional `<text>` passes through the caller's own shell first, where a backtick or `$( )` in the body silently executes and vanishes from what arrives (upstream #378). `agmsg-dispatch` is the one exception and takes a single-line, shell-safe positional message. Pick the path by how the recipient is seated, never by inferring pane or agent status: a worker in a `herdr-agents` pane gets `agmsg-dispatch <team> <from> <to> <pane_id> "<message>"` (send, generic wake, `read_at` wait; single-line shell-safe text only), the sanctioned wake path until worker seating writes placement records at launch, because `poke.sh` exits 1 with "no placement record" for a hand-joined member, and a herdr-agents worker gets a record only once it acts from its own pane (upstream `send.sh`/`inbox.sh` record the acting pane, #1109); a spawn-seated member (placement record `run/spawn.*`; `team.sh <team> --json` shows its pane) gets `poke.sh <team> <name> --body-file <path> [--retries N --retry-delay SECONDS --backoff fixed|exponential]`, which types and submits in one call and refuses to type over an in-progress draft (#1321/#1322); a pane-less member gets `send.sh <team> <from> <to> --body-file <path>` and its own delivery mode. Verify delivery via the messages.db `read_at` column. `poke.sh` exit codes: 10 = terminal unreachable, 12 = pane gone or no live agent, 14/15 = refused to type over a changing or unlocatable input box, 13 = the driver has no poke path for this pane (for example a `plain` terminal); where poke.sh's narrow agmsg-message fallback succeeds it exits 0, so 13 means nothing was delivered, and the printed reason names the native channel, asks the caller to claim its own identity first, or reports that the fallback failed. Never retry a 13 as `send.sh` yourself: that overrides the driver's considered refusal and can double-deliver. Seating case: a worker in an unviewed or headless Herdr workspace (no client attached, a small pane rect such as 18x41) makes `poke.sh` exit 14/15 from its TUI input locator; that is a locator refusal, not evidence about the worker's state, so wake it with `agmsg-dispatch` and verify `read_at`.
+6. Send `AGMSG-TASK v1` with the exact artifact paths and `done_signal=AGMSG-RESULT`. Pass every `send.sh`/`poke.sh` body with `--body-file <path>` (both take it in agmsg v1.5.0), never as a positional argument: a positional `<text>` passes through the caller's own shell first, where a backtick or `$( )` in the body silently executes and vanishes from what arrives (upstream #378). `agmsg-dispatch` is the one exception and takes a single-line, shell-safe positional message. Pick the path by how the recipient is seated, never by inferring pane or agent status: a worker in a `herdr-agents` pane gets `agmsg-dispatch <team> <from> <to> <pane_id> "<message>"` (send, generic wake, `read_at` wait; single-line shell-safe text only), the sanctioned wake path until worker seating writes placement records at launch, because `poke.sh` exits 1 with "no placement record" for a hand-joined member, and a herdr-agents worker gets a record only once it acts from its own pane (upstream `send.sh`/`inbox.sh` record the acting pane, #1109); a spawn-seated member (placement record `run/spawn.*`; `team.sh <team> --json` shows its pane) gets `poke.sh <team> <name> --body-file <path> [--retries N --retry-delay SECONDS --backoff fixed|exponential]`, which types and submits in one call and refuses to type over an in-progress draft (#1321/#1322); a pane-less member gets `send.sh <team> <from> <to> --body-file <path>` and its own delivery mode. Verify delivery via the messages.db `read_at` column. `poke.sh` exit codes: 10 = terminal unreachable, 12 = pane gone or no live agent, 14/15 = refused to type over a changing or unlocatable input box, 13 = the driver has no poke path for this pane (for example a `plain` terminal); where poke.sh's narrow agmsg-message fallback succeeds it exits 0, so 13 means nothing was delivered, and the printed reason names the native channel, asks the caller to claim its own identity first, or reports that the fallback failed. Never retry a 13 as `send.sh` yourself: that overrides the driver's considered refusal and can double-deliver. Seating case: a worker in an unviewed or headless Herdr workspace (no client attached, a small pane rect such as 18x41) makes `poke.sh` exit 14/15 from its TUI input locator; that is a locator refusal, not evidence about the worker's state, so wake it with `agmsg-dispatch` and verify `read_at`. Every dispatch (TASK, ACCEPTANCE, PING) is recorded in the current acceptance record under a `dispatch:` key as the bus line with its read marker; a seat is reported as working only from such a line, and after a context compaction the open TASK list is re-derived from a bus read that is refused when it reaches its limit (`bus-read.sh` exits when the history reaches `BUS_READ_LIMIT`; the orchestrator raises the limit and reads again), never from a default-limited one and never from a read whose truncation went unnoticed. A seated worker idle for 20 minutes since its latest bus event for the task while a dispatchable task exists (INV-10's idle figure; its 30 minutes is the first-push deadline) gets a bus read, then a PING; a longer silent wait is never the answer. `scripts/orchestrator/dispatch.sh` writes the line and `scripts/orchestrator/bus-read.sh` performs the read and prints the minutes since each open task's latest event (both on main since a03c1daa, plan 007 T718); the orchestrator applies the 20-minute figure to the minutes the script prints (the script's own silence flag still uses 30 minutes, a recorded residual of the tools lineage).
 7. Track `max_turns`. Use `AGMSG-PING` for liveness if a worker stalls.
 8. On `AGMSG-RESULT`, read the task file and every referenced artifact before deciding.
 9. For a RESULT carrying `effects`, verify that every declared effect has the report's stated reverse mapping before acceptance; record any irreversible effect in the acceptance note.
@@ -167,7 +169,7 @@ AGMSG-PONG v1 task_id=<id> status=alive|blocked|question note=<short-note>
     1. Sweep the final head's feedback with `scripts/pr-feedback.py <pr> --json .orchestration/validation/<task>-pr-feedback.json` and give every item a `fixed:<commit>` or `not-applicable:<reason>` disposition, leaving none on `failure` or `warning` annotations. Optionally request `@coderabbitai full review` on the final head first; when a CodeRabbit review exists it is swept like any other item, and the gate does not require a bot review. An `open:<thread id>` item from a worker's third Bot round is a sweep item like any other: it becomes `fixed:<sha>` through a revise round that carries its `check=` (a round that counts toward INV-6 like any other), or `not-applicable:<reason>` with a pasted refutation; until one of those exists the PR is not merged, never with the thread open.
     2. Run the task-level audit of that head in the pair or headless form of the task-level audit bullet. It exits nonzero for every verdict other than `correct`. An exit with `Audit verdict: incorrect` is not a failed step: continue to step 3 and disposition its findings. A `blocked` or missing verdict means re-running the audit.
     3. Write the acceptance record, summarising the dispositions, with an `audit-finding:` line for every audit finding whatever the verdict (the gate needs them, through `AUDIT_DISPOSITIONS`, when it is `incorrect`).
-    4. Run the gate: `AUDIT_EVIDENCE=<audit> [AUDIT_DISPOSITIONS=<acceptance record>] AGENT_REVIEWED=1 REVIEW_EVIDENCE=<receipt> BASE=origin/main PR_FEEDBACK_EVIDENCE=<json> make require-crit-review`.
+    4. Run the gate: `AUDIT_EVIDENCE=<audit> [AUDIT_DISPOSITIONS=<acceptance record>] AGENT_REVIEWED=1 REVIEW_EVIDENCE=<receipt> ACCEPTANCE_EVIDENCE=<acceptance record> BASE=origin/main PR_FEEDBACK_EVIDENCE=<json> make require-crit-review`.
        - A `review` sweep item whose body carries a `P0`–`P3` badge is a finding with its own `fixed:<commit>` or `not-applicable:<reason>` disposition, never a container for its inline threads.
        - The sweep covers issue comments, reviews, inline review comments with thread resolution, non-passing check runs, check-run annotations at every level (`notice`, `warning`, `failure`), and commit statuses. A `failure` marked `not-applicable` needs a concrete reason of at least 20 characters.
        - A CodeRabbit full review is optional, at most once on the final head: the plan allows one review per hour and every review event spends one (docs.coderabbit.ai/management/rate-limits).
diff --git a/tests/fixtures/regime/code-review-orchestration.md b/tests/fixtures/regime/code-review-orchestration.md
index 22d0e3c7..d7586157 100644
--- a/tests/fixtures/regime/code-review-orchestration.md
+++ b/tests/fixtures/regime/code-review-orchestration.md
@@ -1,5 +1,5 @@
 ### Orchestration records and trust-boundary code
 
 - Files under `.orchestration/**` are the regime's records and task specifications, which the regime's own reviewers review; in the pull-request review by the Codex Bot, review them for secrets and home-directory paths only, except a trust-boundary task's `threat_table` and the task metadata needed to judge it, which the next bullet covers. The task-level audit keeps the full scope of the Audit section.
-- Judge from the diff, whatever the task's metadata says, whether a change touches a trust boundary (anything the design tier lists, CI that decides a required check, code that executes PR-controlled input). Review such code against the task's `threat_table`: report a missing table or a missing row; report a `closed` row whose test does not close it, a `residual` row whose control does not mitigate the risk, and an `out-of-scope` row whose owner does not own it. Do not re-raise a `residual` row whose control mitigates the risk. Shape (the test selector, the sentence, the owning task id) is the schema's to check, not the review's. Until `schemas/task.json` lands in wave V1, the task-file review checks the three shape rules by hand.
+- Judge from the diff, whatever the task's metadata says, whether a change touches a trust boundary (anything the design tier lists, CI that decides a required check, code that executes PR-controlled input). Review such code against the task's `threat_table`: report a missing table or a missing row; a row's unit is the SKILL threat-table bullet's (one per `allowed_files` entry, one per non-path control, one per orchestrator effect), so review a missing row at that unit; report a `closed` row whose test does not close it, a `residual` row whose control does not mitigate the risk, and an `out-of-scope` row whose owner does not own it. Do not re-raise a `residual` row whose control mitigates the risk. Shape (the test selector, the sentence, the owning task id) is the schema's to check, not the review's. Until `schemas/task.json` lands in wave V1, the task-file review checks the three shape rules by hand.
 - Keep lint and formatting to CI.
diff --git a/tests/fixtures/regime/invariants.md b/tests/fixtures/regime/invariants.md
index 90eb9ddc..8c5989d9 100644
--- a/tests/fixtures/regime/invariants.md
+++ b/tests/fixtures/regime/invariants.md
@@ -3,10 +3,12 @@
 - Review every RESULT adversarially across correctness, regressions, security, and reporting omissions: try to refute it, independently re-derive findings, and never treat sampled spot checks as full verification.
 - Acceptance review, adversarial RESULT review, and review-profile work remain orchestrator-side; never delegate them to a worker, and keep `make require-crit-review` as the final integration step. Revisit only if worker-side model capability surpasses the orchestrator tier.
 - A design review runs in paired rounds. Both reviewers, a fresh Claude context on the `review` profile and a Codex read-only run under a `codex-review` identity, get the same design hash at the same time. The orchestrator revises once per pair of results and opens no round while one is still open. The third pair is the last: on its accept the design is frozen at the hash the pair last accepted, the third pair's own, and whatever is still open at that hash becomes a residual list that is worker input; on its revise or reject nothing is frozen and the design goes back to a context other than its author, never to a fourth pair; a revision after the third pair is not made, and any later change to a hashed key is a new pair (INV-7). The review judges the invariants, threat model, trust anchors and premises for contradiction and enforceability, never implementation detail.
-- A task-file review is one round with a fixed stop condition: no contradiction with the design, the premises hold, `allowed_files` covers every touch point that grep finds, and one invariant check (a `-contract-a01` id maps to its implementing entry). Anything finer belongs to the worker and the implementation PR.
+- A task-file review is one round with a fixed stop condition: no contradiction with the design, the premises hold, `allowed_files` covers every touch point that grep finds, and one invariant check (for a task that carries an `invariants` key: the task id maps to its `implementing_tasks` entry, the invariant ids match, and each invariant's sentence equals the design's byte-for-byte, the design read from main (INV-2), checked by hand in the review until a checker lands; a task without the key needs no entry). Anything finer belongs to the worker and the implementation PR.
 - A boundary PR synchronizes records at a boundary. It carries no task draft under review. A design not yet on `main` lands through a merged boundary PR before its implementing TASK is dispatched (INV-2), and any merged boundary that carries the design meets that precondition.
-- A task that touches a trust boundary (anything the design tier lists, CI that decides a required check, code that executes PR-controlled input) carries a `threat_table` in its front matter: one `{control, disposition}` row per thing the PR or the orchestrator controls (the tree and its tests, task.md, workflow files, interpreter and environment files, in-process effects, new or renamed scripts, metadata separators). A disposition takes one of three forms: `closed: tests/<file>::<name>`, the test that closes the row; `residual: <sentence>`, the compensating control; `out-of-scope: <task id>`, the task that owns the row. Shape is `schemas/task.json`'s (wave V1): a `closed` selector names a test present in the PR tree at acceptance and in the schema's validation of the PR, an `out-of-scope` owner is a task id in the design's `implementing_tasks`, a `residual` payload is a sentence of at least 20 characters (the gate's minimum for a reason). Until `schemas/task.json` lands in wave V1, the task-file review checks the three shape rules by hand. For a `closed` row it checks the selector's form only, since the test does not exist before implementation. Substance is the reviewers': the task-file review, the Bot and the auditor judge each row against the diff. The table is the task's completion condition: a missing row is added once, counted as an amendment, never fixed finding by finding.
+- A task that touches a trust boundary (anything the design tier lists, CI that decides a required check, code that executes PR-controlled input) carries a `threat_table` in its front matter: one `{control, disposition}` row per thing the PR or the orchestrator controls (the tree and its tests, task.md, workflow files, interpreter and environment files, in-process effects, new or renamed scripts, metadata separators). The row unit is one row per `allowed_files` entry, one row per listed control that is not a path (task metadata, workflow and interpreter or environment inputs, in-process effects, new or renamed scripts, metadata separators), carried by the declared test module's row where that is where the control acts, and one row per orchestrator effect from the fixed list (forced removal, merge, update-branch); under a wildcard `allowed_files` entry whose files are executed or applied (scripts, workflows, hooks, settings, the rules seats follow), one row per concrete file the PR changes; a wildcard over test fixtures or other data files keeps one row; C4 of the task-consistency check (plan 007 T704) verifies the path half once it lands, and the task-file review checks it by hand until then. A disposition takes one of three forms: `closed: tests/<file>::<name>`, the test that closes the row; `residual: <sentence>`, the compensating control; `out-of-scope: <task id>`, the task that owns the row. Shape is `schemas/task.json`'s (wave V1): a `closed` selector names a test present in the PR tree at acceptance and in the schema's validation of the PR, an `out-of-scope` owner is a task id in the design's `implementing_tasks`, a `residual` payload is a sentence of at least 20 characters (the gate's minimum for a reason). Until `schemas/task.json` lands in wave V1, the task-file review checks the three shape rules by hand. For a `closed` row it checks the selector's form only, since the test does not exist before implementation. Substance is the reviewers': the task-file review, the Bot and the auditor judge each row against the diff. The table is the task's completion condition: a missing row is added once, counted as an amendment, never fixed finding by finding.
 - Before every acceptance action (revise, accept, merge) the orchestrator runs `scripts/regime-counters.sh <task id>` and pastes its output into the acceptance record. S2 is decided from INV-6's counts: each component the script prints is read from its output, and for each component it prints as `unknown` the record pastes the command and output that read the source INV-6 names for that component, or, while that source has no entry for the task, says so and pastes the reading of the interim record the orchestrator used in its place. S1 (plan 006: the same finding class three times on one artifact, from any reviewer) is decided from the record's finding-class table, which gives a class to every finding the PR-feedback sweep lists, whatever its disposition, and to every task-level audit finding; three rows of one class stop the artifact.
+- A change to a rule sentence requested of a worker travels as a task amendment (hashed, checked by the task-consistency check C1 to C6 once plan 007 T704 lands it and by hand until then, confirmed by the review seat), never as a PONG answer.
+- When a finding class reaches three on one artifact (the record's ledger) or `scripts/regime-counters.sh` prints an S1 candidate, the next acceptance action is the records search for that class, pasted into the record as the line `search: <class> -> <the matching mistake records or none>`, and the matching correction is applied when its mechanism is landed, or landed first when it is pending, mechanism by mechanism, before any dispatch; a class is a slug of `[a-z0-9-]` assigned at disposition time, never text taken from a review title. Once plan 007 T718 lands, `scripts/orchestrator/three-repeat.sh <class>` validates the slug, runs the records search and the CompactionDB search without a shell and prints the line; until then the orchestrator runs them by hand with a validated slug. Once `dotfiles-T128-gate-evidence-a02` lands, the gate refuses the action without the line; until then the orchestrator refuses it by rule. Every `not-applicable` disposition carries `; evidence=<command>` with the output pasted in the record.
 - At regime or session boundaries, write pending acceptance records, then mechanically commit every `.orchestration` file so no untracked tail remains. The sync needs no per-task artifact set: its audit record is the commit, whose message lists covered task IDs, plus agmsg ACCEPTANCE history. `make check-regime-boundary` reports a canonical clone with unmerged entries, a stash, or a difference from `origin/main` under `home/`, `install/` or `scripts/` as a sign that something ran where it must not. Lessons from a session are codified in this repository (a rule, the skill, or a check) through a task; Claude auto-memory is not a durable store for regime procedure. The canonical clone is pull and apply only and untouched by any seat: no edits, no apply from a dirty tree (the run_before guard refuses it), and one orchestrator identity per repository, seated at the working clone.
 - Stop checklist, at every regime or session boundary and in this order: write pending acceptance records; mask every `.orchestration` file the boundary commit adds or changes with `uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets <files>`, which also normalises home directories to `~`; run `make validate-agent-assets` (real exit status); make the `.orchestration` boundary commit with zero untracked tail on a fresh `orchestration/boundary-<YYYY-MM-DD>` branch from `origin/main` and merge its PR with `gh pr merge --squash --auto`; remove every worker with `herdr-agents --remove-worker <worktree>` (despawn, delivery off, leave, tab or workspace closed); check stale identities with `identities.sh <path> <type>` (exactly one name at the main checkout, none at a worker worktree); close Crit review servers (`pgrep -f 'crit _serve'` must be empty); in a CompactionDB-opted-in project, review `uv run --no-project .claude/hooks/contextdb_cli.py memory candidates --limit 20` and promote each candidate worth keeping with `uv run --no-project .claude/hooks/contextdb_cli.py memory promote <id> --scope project`, or leave it. The orchestrator workspace itself stays resident for the next session unless the operator restarts the machine. `make check-regime-boundary` (`scripts/check-regime-boundary.sh`) checks this list and the orchestrator seat lock, one line per violation.
 - Before every `.orchestration` boundary commit, run the masker on the files it adds or changes (`uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets <files>`), then `make validate-agent-assets`, and branch on its real exit status, never through a pipe; fix a failure before pushing, because committed audit evidence can trip the secret scan, which also rejects a home directory path in `.orchestration/**`.
diff --git a/tests/fixtures/regime/orchestrator-step-6.md b/tests/fixtures/regime/orchestrator-step-6.md
new file mode 100644
index 00000000..dd36748b
--- /dev/null
+++ b/tests/fixtures/regime/orchestrator-step-6.md
@@ -0,0 +1 @@
+6. Send `AGMSG-TASK v1` with the exact artifact paths and `done_signal=AGMSG-RESULT`. Pass every `send.sh`/`poke.sh` body with `--body-file <path>` (both take it in agmsg v1.5.0), never as a positional argument: a positional `<text>` passes through the caller's own shell first, where a backtick or `$( )` in the body silently executes and vanishes from what arrives (upstream #378). `agmsg-dispatch` is the one exception and takes a single-line, shell-safe positional message. Pick the path by how the recipient is seated, never by inferring pane or agent status: a worker in a `herdr-agents` pane gets `agmsg-dispatch <team> <from> <to> <pane_id> "<message>"` (send, generic wake, `read_at` wait; single-line shell-safe text only), the sanctioned wake path until worker seating writes placement records at launch, because `poke.sh` exits 1 with "no placement record" for a hand-joined member, and a herdr-agents worker gets a record only once it acts from its own pane (upstream `send.sh`/`inbox.sh` record the acting pane, #1109); a spawn-seated member (placement record `run/spawn.*`; `team.sh <team> --json` shows its pane) gets `poke.sh <team> <name> --body-file <path> [--retries N --retry-delay SECONDS --backoff fixed|exponential]`, which types and submits in one call and refuses to type over an in-progress draft (#1321/#1322); a pane-less member gets `send.sh <team> <from> <to> --body-file <path>` and its own delivery mode. Verify delivery via the messages.db `read_at` column. `poke.sh` exit codes: 10 = terminal unreachable, 12 = pane gone or no live agent, 14/15 = refused to type over a changing or unlocatable input box, 13 = the driver has no poke path for this pane (for example a `plain` terminal); where poke.sh's narrow agmsg-message fallback succeeds it exits 0, so 13 means nothing was delivered, and the printed reason names the native channel, asks the caller to claim its own identity first, or reports that the fallback failed. Never retry a 13 as `send.sh` yourself: that overrides the driver's considered refusal and can double-deliver. Seating case: a worker in an unviewed or headless Herdr workspace (no client attached, a small pane rect such as 18x41) makes `poke.sh` exit 14/15 from its TUI input locator; that is a locator refusal, not evidence about the worker's state, so wake it with `agmsg-dispatch` and verify `read_at`. Every dispatch (TASK, ACCEPTANCE, PING) is recorded in the current acceptance record under a `dispatch:` key as the bus line with its read marker; a seat is reported as working only from such a line, and after a context compaction the open TASK list is re-derived from a bus read that is refused when it reaches its limit (`bus-read.sh` exits when the history reaches `BUS_READ_LIMIT`; the orchestrator raises the limit and reads again), never from a default-limited one and never from a read whose truncation went unnoticed. A seated worker idle for 20 minutes since its latest bus event for the task while a dispatchable task exists (INV-10's idle figure; its 30 minutes is the first-push deadline) gets a bus read, then a PING; a longer silent wait is never the answer. `scripts/orchestrator/dispatch.sh` writes the line and `scripts/orchestrator/bus-read.sh` performs the read and prints the minutes since each open task's latest event (both on main since a03c1daa, plan 007 T718); the orchestrator applies the 20-minute figure to the minutes the script prints (the script's own silence flag still uses 30 minutes, a recorded residual of the tools lineage).
diff --git a/tests/unit/test_agmsg_orchestration_docs.py b/tests/unit/test_agmsg_orchestration_docs.py
index e4862721..86d0178f 100644
--- a/tests/unit/test_agmsg_orchestration_docs.py
+++ b/tests/unit/test_agmsg_orchestration_docs.py
@@ -223,6 +223,7 @@ class AgmsgRegimePatternTest(unittest.TestCase):
         # name, file, outer slice or None, (start, end): the start marker is part of the pinned text.
         ("invariants", SKILL, None, ("## Review and integration invariants", "\n## ")),
         ("worker-step-15", SKILL, None, ("\n15. After the final push", "\n## ")),
+        ("orchestrator-step-6", SKILL, ("## Orchestrator Playbook", "\n## "), ("\n6. ", "\n7. ")),
         ("orchestrator-step-7", SKILL, ("## Orchestrator Playbook", "\n## "), ("\n7. ", "\n8. ")),
         ("message-contract", SKILL, None, ("## Message Contract v1", "\n## ")),
         (
@@ -275,10 +276,17 @@ class AgmsgRegimePatternTest(unittest.TestCase):
             "no contradiction with the design",
             "the premises hold",
             "`allowed_files` covers every touch point that grep finds",
-            "one invariant check (a `-contract-a01` id maps to its implementing entry)",
+            # Plan 006 B0: design v20 removed contract PRs, so the check names the implementing_tasks entry;
+            # thread 4247933561: a task without an `invariants` key (a docs or review task) needs no entry;
+            # thread 4257278283: matching ids is not enough, so each sentence is compared with the design's.
+            "one invariant check (for a task that carries an `invariants` key: the task id maps to its "
+            "`implementing_tasks` entry, the invariant ids match, and each invariant's sentence equals the design's "
+            "byte-for-byte, the design read from main (INV-2), checked by hand in the review until a checker lands; "
+            "a task without the key needs no entry)",
         ):
             with self.subTest(token=token):
                 self.assertIn(token, text)
+        self.assertNotIn("-contract-a01", text)
 
     def test_a_design_lands_on_main_before_its_task(self) -> None:
         # Thread 4243537281: a boundary PR carrying the design is INV-2's dispatch prerequisite.
@@ -508,6 +516,118 @@ class AgmsgRegimePatternTest(unittest.TestCase):
             with self.subTest(token=token):
                 self.assertIn(token, step)
 
+    def test_dispatches_are_recorded_from_the_bus(self) -> None:
+        # Plan 007 T703 item 1 (C-12): a seat's status comes from a bus line, never from memory; plan 010 option D:
+        # the obligation stays here, and the commands move to plan 007 T718's scripts.
+        step = self.section(self.section(SKILL.read_text(), "## Orchestrator Playbook"), "\n6. ", "\n7. ")
+        for token in (
+            "Every dispatch (TASK, ACCEPTANCE, PING) is recorded in the current acceptance record under a "
+            "`dispatch:` key as the bus line with its read marker; a seat is reported as working only from such a "
+            # The local review of 7771082f: the merged bus-read.sh refuses a read at its limit; nothing reads all.
+            "line, and after a context compaction the open TASK list is re-derived from a bus read that is refused "
+            "when it reaches its limit (`bus-read.sh` exits when the history reaches `BUS_READ_LIMIT`; the "
+            "orchestrator raises the limit and reads again), never from a default-limited one and never from a read "
+            "whose truncation went unnoticed.",
+            # Threads 4248319936 and 4249303426: the clock runs from the seat's latest event for the task;
+            # thread 4257278271: INV-10's idle figure is 20 minutes, its 30 minutes the first-push deadline.
+            "A seated worker idle for 20 minutes since its latest bus event for the task while a dispatchable task "
+            "exists (INV-10's idle figure; its 30 minutes is the first-push deadline) gets a bus read, then a PING; "
+            "a longer silent wait is never the answer.",
+            # Thread 4249303413: history.sh shows the latest 20 rows unless given a limit.
+            "`scripts/orchestrator/dispatch.sh` writes the line and `scripts/orchestrator/bus-read.sh` performs the "
+            "read and prints the minutes since each open task's latest event (both on main since a03c1daa, plan 007 "
+            "T718); the orchestrator applies the 20-minute figure to the minutes the script prints (the script's own "
+            "silence flag still uses 30 minutes, a recorded residual of the tools lineage).",
+        ):
+            with self.subTest(token=token[:40]):
+                self.assertIn(token, step)
+        for stale in (
+            "expected duration",
+            "the bus line `history.sh <team>` prints",
+            "no bus event from its seat since",
+            "complete bus read",
+            "silent for thirty minutes",
+        ):
+            with self.subTest(stale=stale):
+                self.assertNotIn(stale, step)
+
+    def test_rule_changes_travel_as_task_amendments(self) -> None:
+        # Plan 007 Phase 0: a rule sentence changed through a PONG answer bypasses the hash and C1 to C6;
+        # plan 009 option A: the checker is not on main yet, so the sentence names its landing condition.
+        self.assertIn(
+            "A change to a rule sentence requested of a worker travels as a task amendment (hashed, checked by "
+            "the task-consistency check C1 to C6 once plan 007 T704 lands it and by hand until then, confirmed by "
+            "the review seat), never as a PONG answer.",
+            self.invariants(),
+        )
+
+    def test_three_repeats_start_with_a_pasted_correction_search(self) -> None:
+        # Plan 007 S6: the third repeat of a class is answered by a recorded correction, never by another fix round;
+        # plan 010 option D: the obligation stays here, and the commands move to plan 007 T718's three-repeat.sh.
+        bullet = self.section(self.invariants(), "\n- When a finding class reaches three on one artifact", "\n- ")
+        for token in (
+            # Threads 4247933574 and 4249303398: the records search, and a correction applied mechanism by mechanism.
+            " (the record's ledger) or `scripts/regime-counters.sh` prints an S1 candidate, the next acceptance "
+            "action is the records search for that class, pasted into the record as the line "
+            "`search: <class> -> <the matching mistake records or none>`, and the matching correction is applied "
+            "when its mechanism is landed, or landed first when it is pending, mechanism by mechanism, before any "
+            "dispatch; a class is a slug of `[a-z0-9-]` assigned at disposition time, never text taken from a review "
+            "title.",
+            # Thread 4249303433: review-derived text never reaches a shell.
+            "Once plan 007 T718 lands, `scripts/orchestrator/three-repeat.sh <class>` validates the slug, runs the "
+            "records search and the CompactionDB search without a shell and prints the line; until then the "
+            "orchestrator runs them by hand with a validated slug.",
+            # Thread 4248711363: the gate does not read the line yet, so the sentence names its landing condition.
+            "Once `dotfiles-T128-gate-evidence-a02` lands, the gate refuses the action without the line; until then "
+            "the orchestrator refuses it by rule.",
+            "Every `not-applicable` disposition carries `; evidence=<command>` with the output pasted in the record.",
+        ):
+            with self.subTest(token=token[:40]):
+                self.assertIn(token, bullet)
+        for stale in (
+            "`grep -rl <class slug> .orchestration/learning/corrections/`",
+            "`grep -l 'classes:",
+            "gate-evidence-a01",
+            "memory search <class slug>",
+        ):
+            with self.subTest(stale=stale):
+                self.assertNotIn(stale, bullet)
+
+    def test_threat_table_rows_have_a_fixed_unit(self) -> None:
+        # Plan 007 T703 item 4: without a unit, a missing row is a judgment call for each reviewer.
+        bullet = self.section(self.invariants(), "\n- A task that touches a trust boundary", "\n- ")
+        self.assertIn(
+            "metadata separators). The row unit is one row per `allowed_files` entry, one row per listed control "
+            "that is not a path (task metadata, workflow and interpreter or environment inputs, in-process effects, "
+            "new or renamed scripts, metadata separators), carried by the declared test module's row where that is "
+            "where the control acts, and one row per orchestrator effect from the fixed list (forced removal, merge, "
+            # Thread 4248711371: C4 is not on main yet, so the sentence names its landing condition.
+            # Thread 4257278276: an executed wildcard entry gets a row per changed file; a data wildcard keeps one.
+            "update-branch); under a wildcard `allowed_files` entry whose files are executed or applied (scripts, "
+            "workflows, hooks, settings, the rules seats follow), one row per concrete file the PR changes; a "
+            "wildcard over test fixtures or other data files keeps one row; C4 of the task-consistency check (plan "
+            "007 T704) verifies the path half once it lands, and the task-file review checks it by hand until then.",
+            bullet,
+        )
+        self.assertNotIn("C4 verifies the path half before dispatch", bullet)
+        rules = self.section((ROOT / "AGENTS.md").read_text(), "## Code Review Rules")
+        subsection = self.section(rules, "### Orchestration records and trust-boundary code", "\n### ")
+        self.assertIn(
+            "report a missing table or a missing row; a row's unit is the SKILL threat-table bullet's (one per "
+            "`allowed_files` entry, one per non-path control, one per orchestrator effect), so review a missing "
+            "row at that unit; report a `closed` row",
+            subsection,
+        )
+
+    def test_the_gate_reads_the_acceptance_record(self) -> None:
+        # Plan 007 T703 item 6: the gate reads the record's ledger and `search:` line once gate-evidence-a02 lands.
+        step = self.section(self.section(SKILL.read_text(), "## Orchestrator Playbook"), "\n10. ", "\n11. ")
+        self.assertIn(
+            "REVIEW_EVIDENCE=<receipt> ACCEPTANCE_EVIDENCE=<acceptance record> BASE=origin/main "
+            "PR_FEEDBACK_EVIDENCE=<json> make require-crit-review",
+            step,
+        )
+
 
 class AgmsgOrchestrationSingleSourceTest(unittest.TestCase):
     """The audit command appears once, in the SKILL's task-level audit bullet; everything else points there."""

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
6. Send `AGMSG-TASK v1` with the exact artifact paths and `done_signal=AGMSG-RESULT`. Pass every `send.sh`/`poke.sh` body with `--body-file <path>` (both take it in agmsg v1.5.0), never as a positional argument: a positional `<text>` passes through the caller's own shell first, where a backtick or `$( )` in the body silently executes and vanishes from what arrives (upstream #378). `agmsg-dispatch` is the one exception and takes a single-line, shell-safe positional message. Pick the path by how the recipient is seated, never by inferring pane or agent status: a worker in a `herdr-agents` pane gets `agmsg-dispatch <team> <from> <to> <pane_id> "<message>"` (send, generic wake, `read_at` wait; single-line shell-safe text only), the sanctioned wake path until worker seating writes placement records at launch, because `poke.sh` exits 1 with "no placement record" for a hand-joined member, and a herdr-agents worker gets a record only once it acts from its own pane (upstream `send.sh`/`inbox.sh` record the acting pane, #1109); a spawn-seated member (placement record `run/spawn.*`; `team.sh <team> --json` shows its pane) gets `poke.sh <team> <name> --body-file <path> [--retries N --retry-delay SECONDS --backoff fixed|exponential]`, which types and submits in one call and refuses to type over an in-progress draft (#1321/#1322); a pane-less member gets `send.sh <team> <from> <to> --body-file <path>` and its own delivery mode. Verify delivery via the messages.db `read_at` column. `poke.sh` exit codes: 10 = terminal unreachable, 12 = pane gone or no live agent, 14/15 = refused to type over a changing or unlocatable input box, 13 = the driver has no poke path for this pane (for example a `plain` terminal); where poke.sh's narrow agmsg-message fallback succeeds it exits 0, so 13 means nothing was delivered, and the printed reason names the native channel, asks the caller to claim its own identity first, or reports that the fallback failed. Never retry a 13 as `send.sh` yourself: that overrides the driver's considered refusal and can double-deliver. Seating case: a worker in an unviewed or headless Herdr workspace (no client attached, a small pane rect such as 18x41) makes `poke.sh` exit 14/15 from its TUI input locator; that is a locator refusal, not evidence about the worker's state, so wake it with `agmsg-dispatch` and verify `read_at`.
7. Track `max_turns`. Use `AGMSG-PING` for liveness if a worker stalls.
8. On `AGMSG-RESULT`, read the task file and every referenced artifact before deciding.
9. For a RESULT carrying `effects`, verify that every declared effect has the report's stated reverse mapping before acceptance; record any irreversible effect in the acceptance note.
10. For a RESULT that carries a pull request, integrate in this order. This is the single procedure that the PR integration rule, `AGENTS.md`, the README and the gh-first-workflow skill cite. A `gh pr update-branch` moves the head, so steps 1 to 4 run again on the new head. After an update-branch the orchestrator runs it, the order is CI on the new head, then the sweep, then the audit; an audit started before CI finishes sees incomplete evidence and returns an evidence-only `incorrect`. Select a checkout with git -C <absolute path>, never with cd, which the sandboxed Bash may not honour. After moving the review worktree to the audited head, verify git -C <review> rev-parse HEAD equals that head and git -C <main> symbolic-ref --short HEAD prints main before the audit and the gate.
    1. Sweep the final head's feedback with `scripts/pr-feedback.py <pr> --json .orchestration/validation/<task>-pr-feedback.json` and give every item a `fixed:<commit>` or `not-applicable:<reason>` disposition, leaving none on `failure` or `warning` annotations. Optionally request `@coderabbitai full review` on the final head first; when a CodeRabbit review exists it is swept like any other item, and the gate does not require a bot review. An `open:<thread id>` item from a worker's third Bot round is a sweep item like any other: it becomes `fixed:<sha>` through a revise round that carries its `check=` (a round that counts toward INV-6 like any other), or `not-applicable:<reason>` with a pasted refutation; until one of those exists the PR is not merged, never with the thread open.
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

 succeeded in 266ms:
     1	# Acceptance: dotfiles-T128-playbook-rules-a04 (plan 007 T703, INV-6 successor of a03 after plan 010 option D) — in progress
     2	
     3	- **Task:** `.orchestration/tasks/dotfiles-T128-playbook-rules-a04.md` sha256 `e64ee6912c33d98305e70b4206f4d0f55bd4236730131a080f0fd81e7227f254`, written by the review seat (`dotfiles-T128-playbook-rules-redesign-a03`, anchor 15:23:59Z); reset record `dotfiles-T128-playbook-rules-a03-design-reset.md`; C1 to C9 OK.
     4	- **Worker:** `claude-standard-dot-a003` at `.claude/worktrees/worker-c`, continuing on `regime/playbook-rules` (PR #328, held at `fe34f7db`; PR head `e12872cd`).
     5	- **Precondition:** the boundary commit that lands a04 and the reset record (INV-2).
     6	- counters: run before the first acceptance action.
     7	- cost: n/a (pending)
     8	- dispatch (C-12 form; pasted 15:41Z): `  ○ [2026-10-12T15:40:52Z] claude-deep-dot → claude-standard-dot-a003: AGMSG-TASK v1 task_id=dotfiles-T128-playbook-rules-a04 repo=~/Workspace/dotfiles/.claude/worktrees/worker-c task_fi`; preconditions met: boundary PR #333 merged 15:39:49Z as `3709a6d8` (a04 and the a03 reset record on main).
     9	- 2026-10-12 16:04:45Z RESULT (bus 779): `status=ready_for_review head=2276a365`; CI 12 green; the worker's four a03 threads `fixed:beee078a`. 16:03:26Z Bot review 5493270947 on 2276a365: thread 4250028600 P1 (`SKILL.md:74`: the counters' S1 candidate is review-title text, the rule wants a slug). Class at disposition time: `search-procedure` (also `unlanded-mechanism-stated-as-present`), the next row after the third S1 cycle → S7, plan 012; M-20261012-23 / C-25. Counters 16:07:36Z: `tasks=1 amendments=0 questions=0 results=1 withdrawn=0 revises=0`.
    10	- 2026-10-13 01:05Z operator: plan 012 option B. No ACCEPTANCE line to the worker yet: a04 is held unchanged until `dotfiles-T128-orchestrator-tools-a01` (T718's first slice: counters slug, three-repeat.sh, bus-read.sh, dispatch.sh) merges; then `gh pr update-branch 328`, Bot, sweep (4250028600 → `fixed:<T718 squash sha>`), audit, gate. The worker a003 takes T718 on a fresh branch meanwhile (its worktree keeps `regime/playbook-rules`).
    11	
    12	- 01:45Z ACCEPTANCE sent to a003 (bus 809, created 01:48:18Z): `status=accepted` (head 2276a365 is the final text under plan 012 B; thread 4250028600 closes when T718 a01 lands; integration by the orchestrator after that merge; no worker action on a04). Sent because the Stop gate requires one ACCEPTANCE per RESULT and the deliverable itself needs no change.
    13	
    14	- 10:12Z T718 first slice merged (a03c1daa); `integrate-328.sh a03c1daa`: update-branch to `7771082f` (09:58:25Z), CI 13 green, Bot review 5501887212 (10:03:30Z) with three new threads on the a04 rule text: 4257278283 (P1, SKILL.md:69, the task-file review's invariant check compares ids only where the design (regime-v3-a01:56) requires byte-for-byte sentence equality), 4257278271 (P2, SKILL.md:164, "thirty minutes" where the design (:64) limits worker idleness to 20; INV-10's 30 is the first-push deadline), 4257278276 (P2, SKILL.md:71, the row unit per `allowed_files` entry lets one wildcard row cover several trust-boundary scripts); the C-32 local review of 7771082f (`dotfiles-T128-playbook-rules-a04-local-review-7771082.md`): one P2 (SKILL.md:164, `history.sh --limit 1000` is not a complete read after compaction; a read at its limit must be refused or paginated). Lines 69, 71 and 164 follow the a04 task text (line 78: "thirty minutes", the "complete bus read … --limit"; the invariant check as ids), so the fixes need amendment 1 of a04 (INV-6: amendments=0, revises=0 before it) and one revise round; the G′ pattern of plan 016 applies: owner first (a follow-up rules task on main owns the residual P2 of the final head by ledger reference), then the fix under the guards on the same PR. S6 searches pasted below.
    15	
    16	4257278283	design-mismatch
    17	4257278271	design-mismatch
    18	4257278276	threat-row-unit
    19	local:7771082:1	default-limited-read
    20	
    21	```text
    22	$ /usr/bin/grep -rl 'classes:.*design-mismatch' .orchestration/learning/mistakes/
    23	(no file)
    24	$ /usr/bin/grep -rli -- 'design-mismatch' .orchestration/learning/mistakes/
    25	(no file)
    26	$ uv run --no-project .claude/hooks/contextdb_cli.py memory search --limit 1000 -- design-mismatch | grep -cE '^[0-9a-f]{8}-'
    27	0
    28	$ /usr/bin/grep -rl 'classes:.*threat-row-unit' .orchestration/learning/mistakes/
    29	.orchestration/learning/mistakes/M-20261012-14.md
    30	$ /usr/bin/grep -rli -- 'threat-row-unit' .orchestration/learning/mistakes/
    31	.orchestration/learning/mistakes/M-20261012-29.md
    32	.orchestration/learning/mistakes/M-20261012-14.md
    33	$ uv run --no-project .claude/hooks/contextdb_cli.py memory search --limit 1000 -- threat-row-unit | grep -cE '^[0-9a-f]{8}-'
    34	0
    35	$ /usr/bin/grep -rl 'classes:.*default-limited-read' .orchestration/learning/mistakes/
    36	.orchestration/learning/mistakes/M-20261012-33.md
    37	$ /usr/bin/grep -rli -- 'default-limited-read' .orchestration/learning/mistakes/
    38	.orchestration/learning/mistakes/M-20261012-33.md
    39	$ uv run --no-project .claude/hooks/contextdb_cli.py memory search --limit 1000 -- default-limited-read | grep -cE '^[0-9a-f]{8}-'
    40	0
    41	$ scripts/regime-counters.sh dotfiles-T128-playbook-rules-a04 --pr 328
    42	task=dotfiles-T128-playbook-rules-a04 tasks=1 amendments=0 questions=0 results=1 withdrawn=0 revises=0 first_result_head=2276a365cba9f104cadd7cd82f3fb0bfec7dac21 bot_p1_heads_after_result=unknown audits=unknown wall=2026-10-12T15:40:52Z..2026-10-12T16:04:45Z (0:23) source=live
    43	```
    44	
    45	## Ledger (machine rows id<TAB>class; the lineage a01 → a04 on PR #328, classes assigned from the thread titles at 10:17Z; the four rows of 7771082f are above)
    46	
    47	4247933544	threat-row-unit
    48	4247933561	design-mismatch
    49	4247933574	search-procedure
    50	4248319926	search-procedure
    51	4248319936	wall-clock
    52	4248711363	unlanded-mechanism-stated-as-present
    53	4248711371	unlanded-mechanism-stated-as-present
    54	4249303398	search-procedure
    55	4249303413	default-limited-read
    56	4249303426	wall-clock
    57	4249303433	search-procedure
    58	4249414388	search-procedure
    59	4250028600	search-procedure
    60	- 10:21Z decision pending (plan 017; S7 by the letter: `design-mismatch` at three on the lineage ledger beside `search-procedure` at six): the G′ pattern as the default (amendment 1 + the owner task `dotfiles-T128-playbook-rules-followup-a01` + one revise), the pair review of both drafts running (seat TASK and Codex half). The checker's C10 hit on item 3 (`regime-counters.sh` beside `; evidence=<command>`) is on main's copy too (pre-existing, outside the amendment). The awaiting-merge marker for #328 was removed deliberately: the head moves with the amendment round, so boundary (11) may run before it.
    61	- 10:30Z operator: plan 017 option G″ (the G′ pattern on this PR): amendment 1 + the owner task first on main, one revise round, residual P2 owned by `dotfiles-T128-playbook-rules-followup-a01`.
    62	- 10:32Z pair round 1 on the drafts: seat `revise` (P2 the owner task's premise 2 counted rows that exist only in the working tree and item 1 named no greppable source; P3 the history paragraph's "thirty minutes" without a superseded marker; P3 item 4's clause vs the fixtures wildcard row), Codex `revise` on the amendment (the same history leftover) and `confirm` on the owner task. Applied: premise 2 is a presence check on origin/main; item 1 is the `## Owned by dotfiles-T128-playbook-rules-followup-a01` section of this record (`<id>\t<class>` rows) landed by the boundary after a04's merge, the dispatch condition stated; the superseded parenthetical on line 74; item 4's clause scoped to executed or applied wildcards (data wildcards keep one row). Round 2 sent 10:32:02Z (a04 `c5dbc2c3…`, owner `cb32794d…`).
    63	- 10:33Z INV-6 with GitHub: `bot_p1_heads_after_result=1` (7771082f); a P1 on the amendment head would reach two (reset). The map agent's record check raised it; the counters inside the sandbox print `unknown` (no gh), outside they print the figure.
    64	- 10:34Z pair-confirmed: a04 amendment 1 at `c5dbc2c3d3514707870c2146ac4acfd6e96279d50f0f6bf04bd8921cd242a6fa`, the owner task at `cb32794d2bb939456e747230e012729d47c327946fbe07fe97d644969dc4fa42` (seat round 2, bus 933; Codex round 2). ACCEPTANCE sent; boundary (11) runs now, then the amendment line to a003.
    65	- 14:01Z plan 021 step 5.1: resume line (bus 945, revise referencing RESULT 779) read 13:57:31Z; the worker merges origin/main (4e7a9b3a), applies amendment 1 (items 1, 4, 5, Completion) with the token tests, pushes; the Bot reviews on PR open only now (operator setting 13:3xZ), so the new head gets no Bot round; the local review runs once on it; dispositions: the P1 and two P2 threads and the local finding `fixed:<sha>`; any new P2 → advisory, owned by `dotfiles-T128-playbook-rules-followup-a01`.
    66	
    67	local-finding: 7771082:1 fixed:e6602ca1 (local review of 7771082f, SKILL.md:164: the read refused at its limit, never a default-limited or silently truncated one)
    68	
    69	## Owned by dotfiles-T128-playbook-rules-followup-a01 (advisory findings of the final head; plan 020 step 1.2; rows id<TAB>class)
    70	
    71	local:65a3d71:1	rule-gap-pending-audit
    72	
    73	local-finding: 65a3d71:1 not-applicable:P1 by the post-round local review (SKILL.md:164: the rule requires dispatch logging into the current acceptance record and the tools refuse a missing record, but no sentence says the orchestrator creates the record before the first dispatch); plan 021 S21: the local review is a sampler and not the acceptance authority, so this finding is referred as input to the audit of this head, which decides; if the audit raises it as P0/P1 the PR stops (plan 020 step 4.2), otherwise it is advisory and owned by dotfiles-T128-playbook-rules-followup-a01; evidence=sed -n 1,20p .orchestration/validation/dotfiles-T128-playbook-rules-a04-local-review-65a3d71.md
     1	# Report: dotfiles-T128-playbook-rules-a04
     2	
     3	- Seat: `claude-standard-dot-a003` in `.claude/worktrees/worker-c`, branch `regime/playbook-rules`, PR #328. a04 is a03's reset under plan 010 option D (`reset_of: [a01, a02, a03]`).
     4	- Before any edit, the branch was fast-forwarded from the worker's `fe34f7db` to the orchestrator's update-branch head `e12872cd`. `fe34f7db` is an ancestor, so nothing was rebased (validation §1).
     5	- Task file sha256 `e64ee691…` matches the TASK's `task_sha256`. It is copied byte-identical in `ff2e7156` to `.orchestration/dotfiles-T128-playbook-rules-a04/task.md`. The a01, a02 and a03 copies are unchanged since `1083a8c1`, `4486dbdd` and `196d73ca` (§1).
     6	
     7	## Commit `beee078a`: items 1 and 3 as obligation, script and landing condition
     8	
     9	Both sentences were spliced into the SKILL from the task's quoted spans, not retyped, and every quoted span of items 1 to 6 is present verbatim (§3).
    10	
    11	| Item | Now | Test |
    12	|---|---|---|
    13	| 1 (step 6) | the dispatch line "as the bus line with its read marker"; the open TASK list "re-derived from a complete bus read, never from a default-limited one"; "A seat silent for thirty minutes since its latest bus event for the task (INV-10's figure) gets a bus read, then a PING"; once T718 lands, `dispatch.sh` and `bus-read.sh`, until then `history.sh <team> --limit 1000` | `test_dispatches_are_recorded_from_the_bus`: one token per sentence; `assertNotIn` for "expected duration", "the bus line `history.sh <team>` prints" and "no bus event from its seat since" |
    14	| 3 (three-repeat) | the records search pasted as `search: <class> -> <…>`; corrections applied mechanism by mechanism; a class is an `[a-z0-9-]` slug assigned at disposition time, never review-title text; once T718 lands, `three-repeat.sh <class>` runs both searches without a shell; once `gate-evidence-a02` lands, the gate refuses without the line | `test_three_repeats_start_with_a_pasted_correction_search`: one token per sentence; `assertNotIn` adds `memory search <class slug>` (the unquoted interpolation) to the earlier stale forms |
    15	
    16	Items 2, 4, 5, 6, 7 and 8 are unchanged, as the task says.
    17	
    18	## A premise worth knowing: `history.sh <team> --limit 1000`
    19	
    20	Item 1's interim command reads the complete history: 778 rows, against 20 by default, the same count as the positional `history.sh <team> '' 1000` (§2). It does so by accident, though. `history.sh`'s usage is `<team> [agent_id] [limit]`, so `--limit` lands in the agent slot. `storage_history` skips a dash-led agent and then reads `--limit --limit 1000`, taking the second `--limit` as the limit value; a non-numeric limit becomes -1, which means no limit (§2 quotes both scripts). So the sentence's obligation, a complete read, holds, but `1000` is not the limit that applies. I wrote it verbatim, and T718's `bus-read.sh` is meant to replace it. If the orchestrator wants the interim form to be literal, the positional `history.sh <team> '' 1000` reads the same rows by design, and changing it is an amendment.
    21	
    22	## Declared fixture changes (INV-12)
    23	
    24	- `tests/fixtures/regime/orchestrator-step-6.md`: item 1 (`beee078a`).
    25	- `tests/fixtures/regime/invariants.md`: item 3 (`beee078a`).
    26	- `code-review-orchestration.md` was regenerated and is unchanged (§7).
    27	
    28	## Results
    29	
    30	- Docs module 47 OK (§4). `test_pr_feedback.py` OK, ruff clean (§5).
    31	- 20 mutants, 20 failures (§6): 1c and 1e put back a03's item-1 wording, 3d a03's whole bullet, 3f a03's "without the paste".
    32	- Size (§7): 6 files outside `.orchestration/`; 7 added lines outside `tests/`; 113 under `tests/` (caps 500 and 1000).
    33	- Premises (§2): `main` moved only under `.orchestration/` since the merge-base; `scripts/orchestrator/` does not exist on `main`, so T718 has not landed; `regime/gate-evidence` is open.
    34	
    35	## Bot threads from a03's head `fe34f7db`
    36	
    37	| Thread | Disposition |
    38	|---|---|
    39	| 4249303413 (P1, default-limited read) | `fixed:beee078a`: "a complete bus read, never … a default-limited one" |
    40	| 4249303433 (P1, review title into a shell) | `fixed:beee078a`: a class is an `[a-z0-9-]` slug assigned at disposition time; `three-repeat.sh` runs without a shell; the command with `<class slug>` is gone |
    41	| 4249303426 (P2, clock stopped by one early PONG) | `fixed:beee078a`: "since its latest bus event for the task" |
    42	| 4249303398 (P2, partial correction status) | `fixed:beee078a`: "applied when its mechanism is landed, or landed first when it is pending, mechanism by mechanism" |
    43	
    44	The earlier threads stand as the a03 report tables them. 4248319926 is answered by the update-branch already taken (`e12872cd`). The worker resolves no thread.
    45	
    46	## CI and the Codex Bot on the a04 head `2276a365` (main-checkout copy)
    47	
    48	- CI: all 12 check runs on `2276a365` are `completed success`, and the watcher exited 0 (validation §9).
    49	- Bot: no review within 10 minutes of the push, so `@codex review` was posted at 15:59:59Z. Review 5493270947 of `2276a365` arrived at 16:03:26Z with one P1 and no P2. Counts: Bot reviews on PR #328 = 5 (`9b2c02a1`, `375bae0f`, `c4e0bb72`, `fe34f7db`, `2276a365`); worker P0/P1 fix rounds = 0.
    50	
    51	| Thread | Finding | Verified premise (§9) | Proposed handling |
    52	|---|---|---|---|
    53	| 4250028600 | P1, SKILL.md:74 (item 3): the two trigger paths use different class formats. `scripts/regime-counters.sh` prints its S1 candidate as the first three words of a review title, while the rule says a class is an `[a-z0-9-]` slug assigned at disposition time, so "the records search for that class" has no defined input when the counter path fires | `regime-counters.sh:147` prints `S1: candidate class=<title words>`; `tests/unit/test_regime_counters.py:451` expects `class=reject skipped contract` | `open:4250028600`: not fixable here. The fix is either the script (forbidden: edit-scripts; `scripts/regime-counters.sh` is outside `allowed_files`) or the sentence (an amendment). Two options for the orchestrator: (a) make the counter emit, or resolve its candidate to, the ledger's assigned slug (a T718 or regime-counters task); (b) say in the sentence that a counter candidate is mapped to its ledger slug before the search |
    54	
    55	## Not done, or outside scope
    56	
    57	- `tests/unit/test_regime_counters.py` and `test_require_crit_review.py` were not run locally (PyPI is unreachable from the sandbox); neither reads the changed files.
    58	- Understand-Anything hook: did not fire. plan-mode-used: no.
    59	
    60	## CompactionDB
    61	
    62	`memory add` printed `a3ae0494-87a7-437c-b39a-2a08ecfcd170` (§8), with the `history.sh --limit` mechanism above.
    63	
    64	cost: n/a
    65	
    66	## Revise round 1 with amendment 1 (ACCEPTANCE of 13:57:09Z; task file sha256 `c5dbc2c3…`)
    67	
    68	The orchestrator's line lifted the operator's 10:36Z stop and superseded TASK 935. The branch fast-forwarded to the remote head `7771082f`, merged `origin/main` (`4e7a9b3a`) in `87bce51e`, and the task copy now matches the amended file byte for byte (validation §10). `e6602ca1` puts the amended sentences of items 1, 4 and 5 in the SKILL verbatim, as the task file quotes them (§10 checks all three):
    69	
    70	| Thread | Finding | Disposition |
    71	|---|---|---|
    72	| 4257278283 (P1) | the invariant check compared ids only | `fixed:e6602ca1`. Each invariant's sentence equals the design's byte for byte, the design read from main (INV-2), by hand until a checker lands. Test: `test_task_file_review_is_one_round_with_a_fixed_stop_condition` (P4) |
    73	| 4257278271 (P2) | step 6 used thirty minutes as INV-10's figure | `fixed:e6602ca1`. A seated worker idle for 20 minutes (INV-10's idle figure; 30 minutes is the first-push deadline). The orchestrator applies it to the minutes `bus-read.sh` prints. Test: `test_dispatches_are_recorded_from_the_bus` (P2) |
    74	| 4257278276 (P2) | the row unit had no rule for a wildcard entry | `fixed:e6602ca1`. One row per concrete changed file under an executed or applied wildcard entry; a data wildcard keeps one row. Test: `test_threat_table_rows_have_a_fixed_unit` (P3) |
    75	| local review of `7771082f`, finding 1 | "a complete bus read", which the merged script does not do | `fixed:e6602ca1`. The read is refused when it reaches its limit, and the orchestrator raises `BUS_READ_LIMIT` and reads again. Test: `test_dispatches_are_recorded_from_the_bus` (P1) |
    76	
    77	- Declared fixture changes (INV-12): `tests/fixtures/regime/invariants.md` (the task-file-review and threat-table bullets) and `tests/fixtures/regime/orchestrator-step-6.md` (step 6). `test_regime_rule_sections_are_pinned_whole` fails on a changed fixture (P5).
    78	- The `test_dispatches_are_recorded_from_the_bus` stale list also refuses `complete bus read` and `silent for thirty minutes`.
    79	- Results (§10): 47 docs tests OK; Prettier and ruff clean; 5 mutants, 5 failures. Size: 6 files outside `.orchestration/`; added lines outside and under `tests/`: 7 and 127.
    80	- The orchestrator's line says the Bot reviews on PR open only now, so there is no Bot wait; the pushed head's CI is in the RESULT and in the main-checkout copy.
    81	
    82	## CI on the revise head `65a3d71b` (main-checkout copy only)
    83	
    84	- Pushed at 2026-10-13T14:04:00Z. CI: all 13 checks pass (validation §11). There is no Bot wait, per the orchestrator's line of 13:57:09Z.
     1	---
     2	task_id: dotfiles-T128-playbook-rules-a04
     3	seat: claude-standard-dot-a003
     4	permission_gated_commands: 11
     5	---
     6	
     7	# Sandbox record: dotfiles-T128-playbook-rules-a04
     8	
     9	- Period: from the AGMSG-TASK (2026-10-12T15:40:52Z) to the RESULT. These ran inside the sandbox: the fetch of the branch over public HTTPS and the fast-forward to `e12872cd`, the `history.sh` premise runs, the edits, fixture generation, the tests, ruff, the verbatim check, the mutation proofs, and the commits.
    10	
    11	`permission_gated_commands` counts every Bash call made with `dangerouslyDisableSandbox`, one per call. This is the final count; the seven calls of round 0 ran as tabled, and #8 to #11 below are revise round 1's. The PR is already ready, so there is no `gh pr ready`.
    12	
    13	| # | Command | Step 4 case |
    14	|--:|---|---|
    15	| 1 | main-checkout `memory add` | main-checkout `memory add` |
    16	| 2 | the HTTPS push | `git push` |
    17	| 3 | `gh pr checks 328 --watch` (background, exit status joined) | `gh` |
    18	| 4 | Bot wait from the push | `gh` |
    19	| 5 | reading the Bot review and the check runs of the final head | `gh` |
    20	| 6 | the masked copy of the five evidence files to the main checkout | artifact copy with the repository masker |
    21	| 7 | `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T128-playbook-rules-a04 …` | `agmsg-dispatch` |
    22	| 8 | the revise round's HTTPS push | `git push` |
    23	| 9 | `gh pr checks 328 --watch` on the revise head | `gh` |
    24	| 10 | the masked copy of the evidence files to the main checkout | artifact copy with the repository masker |
    25	| 11 | `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T128-playbook-rules-a04 revise=1 …` | `agmsg-dispatch` |
    26	
    27	Revise round 1 (amendment 1): this main-checkout copy gives the final count, eleven calls, all run; there is no Bot wait (the orchestrator's line of 13:57:09Z).

 exited 1 in 405ms:
error connecting to api.github.com
check your internet connection or https://githubstatus.com
error connecting to api.github.com
check your internet connection or https://githubstatus.com

**Managing large JSON output**
exec
/bin/zsh -lc 'git diff 4e7a9b3ae0a1a80f2c7664ea54e3244224a7a672 65a3d71bf4e496252bf1ff51894974130c96cd43 -- AGENTS.md home/dot_agents/skills/agmsg-orchestration/SKILL.md tests/fixtures/regime tests/unit/test_agmsg_orchestration_docs.py' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 50ms:
diff --git a/AGENTS.md b/AGENTS.md
index 1e3b6a5b..a0b54678 100644
--- a/AGENTS.md
+++ b/AGENTS.md
@@ -75,5 +75,5 @@ Standing review rules for the auditor (the task-level audit of a final head, run
 ### Orchestration records and trust-boundary code
 
 - Files under `.orchestration/**` are the regime's records and task specifications, which the regime's own reviewers review; in the pull-request review by the Codex Bot, review them for secrets and home-directory paths only, except a trust-boundary task's `threat_table` and the task metadata needed to judge it, which the next bullet covers. The task-level audit keeps the full scope of the Audit section.
-- Judge from the diff, whatever the task's metadata says, whether a change touches a trust boundary (anything the design tier lists, CI that decides a required check, code that executes PR-controlled input). Review such code against the task's `threat_table`: report a missing table or a missing row; report a `closed` row whose test does not close it, a `residual` row whose control does not mitigate the risk, and an `out-of-scope` row whose owner does not own it. Do not re-raise a `residual` row whose control mitigates the risk. Shape (the test selector, the sentence, the owning task id) is the schema's to check, not the review's. Until `schemas/task.json` lands in wave V1, the task-file review checks the three shape rules by hand.
+- Judge from the diff, whatever the task's metadata says, whether a change touches a trust boundary (anything the design tier lists, CI that decides a required check, code that executes PR-controlled input). Review such code against the task's `threat_table`: report a missing table or a missing row; a row's unit is the SKILL threat-table bullet's (one per `allowed_files` entry, one per non-path control, one per orchestrator effect), so review a missing row at that unit; report a `closed` row whose test does not close it, a `residual` row whose control does not mitigate the risk, and an `out-of-scope` row whose owner does not own it. Do not re-raise a `residual` row whose control mitigates the risk. Shape (the test selector, the sentence, the owning task id) is the schema's to check, not the review's. Until `schemas/task.json` lands in wave V1, the task-file review checks the three shape rules by hand.
 - Keep lint and formatting to CI.
diff --git a/home/dot_agents/skills/agmsg-orchestration/SKILL.md b/home/dot_agents/skills/agmsg-orchestration/SKILL.md
index f3929e8e..9bc521d3 100644
--- a/home/dot_agents/skills/agmsg-orchestration/SKILL.md
+++ b/home/dot_agents/skills/agmsg-orchestration/SKILL.md
@@ -66,10 +66,12 @@ Use this skill for structured multi-agent work where an orchestrator seat assign
 - Review every RESULT adversarially across correctness, regressions, security, and reporting omissions: try to refute it, independently re-derive findings, and never treat sampled spot checks as full verification.
 - Acceptance review, adversarial RESULT review, and review-profile work remain orchestrator-side; never delegate them to a worker, and keep `make require-crit-review` as the final integration step. Revisit only if worker-side model capability surpasses the orchestrator tier.
 - A design review runs in paired rounds. Both reviewers, a fresh Claude context on the `review` profile and a Codex read-only run under a `codex-review` identity, get the same design hash at the same time. The orchestrator revises once per pair of results and opens no round while one is still open. The third pair is the last: on its accept the design is frozen at the hash the pair last accepted, the third pair's own, and whatever is still open at that hash becomes a residual list that is worker input; on its revise or reject nothing is frozen and the design goes back to a context other than its author, never to a fourth pair; a revision after the third pair is not made, and any later change to a hashed key is a new pair (INV-7). The review judges the invariants, threat model, trust anchors and premises for contradiction and enforceability, never implementation detail.
-- A task-file review is one round with a fixed stop condition: no contradiction with the design, the premises hold, `allowed_files` covers every touch point that grep finds, and one invariant check (a `-contract-a01` id maps to its implementing entry). Anything finer belongs to the worker and the implementation PR.
+- A task-file review is one round with a fixed stop condition: no contradiction with the design, the premises hold, `allowed_files` covers every touch point that grep finds, and one invariant check (for a task that carries an `invariants` key: the task id maps to its `implementing_tasks` entry, the invariant ids match, and each invariant's sentence equals the design's byte-for-byte, the design read from main (INV-2), checked by hand in the review until a checker lands; a task without the key needs no entry). Anything finer belongs to the worker and the implementation PR.
 - A boundary PR synchronizes records at a boundary. It carries no task draft under review. A design not yet on `main` lands through a merged boundary PR before its implementing TASK is dispatched (INV-2), and any merged boundary that carries the design meets that precondition.
-- A task that touches a trust boundary (anything the design tier lists, CI that decides a required check, code that executes PR-controlled input) carries a `threat_table` in its front matter: one `{control, disposition}` row per thing the PR or the orchestrator controls (the tree and its tests, task.md, workflow files, interpreter and environment files, in-process effects, new or renamed scripts, metadata separators). A disposition takes one of three forms: `closed: tests/<file>::<name>`, the test that closes the row; `residual: <sentence>`, the compensating control; `out-of-scope: <task id>`, the task that owns the row. Shape is `schemas/task.json`'s (wave V1): a `closed` selector names a test present in the PR tree at acceptance and in the schema's validation of the PR, an `out-of-scope` owner is a task id in the design's `implementing_tasks`, a `residual` payload is a sentence of at least 20 characters (the gate's minimum for a reason). Until `schemas/task.json` lands in wave V1, the task-file review checks the three shape rules by hand. For a `closed` row it checks the selector's form only, since the test does not exist before implementation. Substance is the reviewers': the task-file review, the Bot and the auditor judge each row against the diff. The table is the task's completion condition: a missing row is added once, counted as an amendment, never fixed finding by finding.
+- A task that touches a trust boundary (anything the design tier lists, CI that decides a required check, code that executes PR-controlled input) carries a `threat_table` in its front matter: one `{control, disposition}` row per thing the PR or the orchestrator controls (the tree and its tests, task.md, workflow files, interpreter and environment files, in-process effects, new or renamed scripts, metadata separators). The row unit is one row per `allowed_files` entry, one row per listed control that is not a path (task metadata, workflow and interpreter or environment inputs, in-process effects, new or renamed scripts, metadata separators), carried by the declared test module's row where that is where the control acts, and one row per orchestrator effect from the fixed list (forced removal, merge, update-branch); under a wildcard `allowed_files` entry whose files are executed or applied (scripts, workflows, hooks, settings, the rules seats follow), one row per concrete file the PR changes; a wildcard over test fixtures or other data files keeps one row; C4 of the task-consistency check (plan 007 T704) verifies the path half once it lands, and the task-file review checks it by hand until then. A disposition takes one of three forms: `closed: tests/<file>::<name>`, the test that closes the row; `residual: <sentence>`, the compensating control; `out-of-scope: <task id>`, the task that owns the row. Shape is `schemas/task.json`'s (wave V1): a `closed` selector names a test present in the PR tree at acceptance and in the schema's validation of the PR, an `out-of-scope` owner is a task id in the design's `implementing_tasks`, a `residual` payload is a sentence of at least 20 characters (the gate's minimum for a reason). Until `schemas/task.json` lands in wave V1, the task-file review checks the three shape rules by hand. For a `closed` row it checks the selector's form only, since the test does not exist before implementation. Substance is the reviewers': the task-file review, the Bot and the auditor judge each row against the diff. The table is the task's completion condition: a missing row is added once, counted as an amendment, never fixed finding by finding.
 - Before every acceptance action (revise, accept, merge) the orchestrator runs `scripts/regime-counters.sh <task id>` and pastes its output into the acceptance record. S2 is decided from INV-6's counts: each component the script prints is read from its output, and for each component it prints as `unknown` the record pastes the command and output that read the source INV-6 names for that component, or, while that source has no entry for the task, says so and pastes the reading of the interim record the orchestrator used in its place. S1 (plan 006: the same finding class three times on one artifact, from any reviewer) is decided from the record's finding-class table, which gives a class to every finding the PR-feedback sweep lists, whatever its disposition, and to every task-level audit finding; three rows of one class stop the artifact.
+- A change to a rule sentence requested of a worker travels as a task amendment (hashed, checked by the task-consistency check C1 to C6 once plan 007 T704 lands it and by hand until then, confirmed by the review seat), never as a PONG answer.
+- When a finding class reaches three on one artifact (the record's ledger) or `scripts/regime-counters.sh` prints an S1 candidate, the next acceptance action is the records search for that class, pasted into the record as the line `search: <class> -> <the matching mistake records or none>`, and the matching correction is applied when its mechanism is landed, or landed first when it is pending, mechanism by mechanism, before any dispatch; a class is a slug of `[a-z0-9-]` assigned at disposition time, never text taken from a review title. Once plan 007 T718 lands, `scripts/orchestrator/three-repeat.sh <class>` validates the slug, runs the records search and the CompactionDB search without a shell and prints the line; until then the orchestrator runs them by hand with a validated slug. Once `dotfiles-T128-gate-evidence-a02` lands, the gate refuses the action without the line; until then the orchestrator refuses it by rule. Every `not-applicable` disposition carries `; evidence=<command>` with the output pasted in the record.
 - At regime or session boundaries, write pending acceptance records, then mechanically commit every `.orchestration` file so no untracked tail remains. The sync needs no per-task artifact set: its audit record is the commit, whose message lists covered task IDs, plus agmsg ACCEPTANCE history. `make check-regime-boundary` reports a canonical clone with unmerged entries, a stash, or a difference from `origin/main` under `home/`, `install/` or `scripts/` as a sign that something ran where it must not. Lessons from a session are codified in this repository (a rule, the skill, or a check) through a task; Claude auto-memory is not a durable store for regime procedure. The canonical clone is pull and apply only and untouched by any seat: no edits, no apply from a dirty tree (the run_before guard refuses it), and one orchestrator identity per repository, seated at the working clone.
 - Stop checklist, at every regime or session boundary and in this order: write pending acceptance records; mask every `.orchestration` file the boundary commit adds or changes with `uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets <files>`, which also normalises home directories to `~`; run `make validate-agent-assets` (real exit status); make the `.orchestration` boundary commit with zero untracked tail on a fresh `orchestration/boundary-<YYYY-MM-DD>` branch from `origin/main` and merge its PR with `gh pr merge --squash --auto`; remove every worker with `herdr-agents --remove-worker <worktree>` (despawn, delivery off, leave, tab or workspace closed); check stale identities with `identities.sh <path> <type>` (exactly one name at the main checkout, none at a worker worktree); close Crit review servers (`pgrep -f 'crit _serve'` must be empty); in a CompactionDB-opted-in project, review `uv run --no-project .claude/hooks/contextdb_cli.py memory candidates --limit 20` and promote each candidate worth keeping with `uv run --no-project .claude/hooks/contextdb_cli.py memory promote <id> --scope project`, or leave it. The orchestrator workspace itself stays resident for the next session unless the operator restarts the machine. `make check-regime-boundary` (`scripts/check-regime-boundary.sh`) checks this list and the orchestrator seat lock, one line per violation.
 - Before every `.orchestration` boundary commit, run the masker on the files it adds or changes (`uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets <files>`), then `make validate-agent-assets`, and branch on its real exit status, never through a pipe; fix a failure before pushing, because committed audit evidence can trip the secret scan, which also rejects a home directory path in `.orchestration/**`.
@@ -159,7 +161,7 @@ AGMSG-PONG v1 task_id=<id> status=alive|blocked|question note=<short-note>
 3. Write a task file that includes objective, scope, allowed files, forbidden actions, expected artifacts, validation commands, and max turns. Name the render check as `make render-check`, never the bare `python3 scripts/generate-agent-configs.py --check`, which fails without PyYAML. Ground `allowed_files` by grepping the repository for every touch point the task names (tests that pin call sequences, mirrors, fixtures) before dispatch. Verify every CLI constraint the task asserts by running the real command in a safe form, not by reading `--help`. Presume an auditor finding that contradicts your own review is right until you refute it with evidence. Decide the worker kind from the allowed files before dispatch: a seat never edits the source of its own execution boundary, so a change is routed by the boundary it touches. A change that touches only Claude's boundary goes to a Codex seat: the `claude.permissions`, `claude.sandbox` and `claude.hooks` blocks of `home/dot_agents/agent-config.yaml` (including excludedCommands, allowUnsandboxedCommands, writable roots, network and the PermissionRequest hook), the Claude-rendering parts of `scripts/generate-agent-configs.py`, the rendered `home/.chezmoitemplates/claude-settings-managed.json`, and `home/dot_claude/modify_private_settings.json`. A change that touches only Codex's boundary goes to a Claude seat: `codex.sandbox_workspace_write`, `codex.approval_policy`, the Codex-rendering parts of the renderer, and `home/.chezmoitemplates/codex-config-managed.toml`. A change that touches both, or a shared source the orchestrator cannot split (such as `codex.sandbox_workspace_write.writable_roots`, which also renders into Claude's `allowWrite`), goes to the operator. The orchestrator decides the kind from the diff the task will produce and records it and the chosen worker profile in the task file. The Claude Code auto-mode classifier also refuses a Claude-boundary task on a Claude seat as Self-Modification. A task that edits permgate (`home/dot_agents/permgate-policy.yaml`, `home/dot_local/bin/common/executable_permgate`), the PermissionRequest hook of both seats, goes to the operator; a Codex `security`-profile worker reviews the change before the orchestrator accepts it, per the model-selection rule. `auto` is Claude Code's built-in starting permission mode since 2.1.283. A project-level `defaultMode: auto` (`.claude/settings.json` or `.claude/settings.local.json`) does not take effect, and the session then also ignores the user-level `defaultMode`, so `auto` belongs only in user or managed settings. Before dispatch, read the task's verbatim blocks against each other for contradictions, and state each rule once; a second artifact references the first instead of restating it.
 4. Start or relaunch worker panes only through `herdr-agents` modes. Deliver messages and wakes as in step 6; never use `pane send-text` followed by `send-keys Enter`, because the separate Enter races the TUI composer and fails nondeterministically.
 5. Configure delivery deliberately. `delivery.sh set turn` is useful for turn-end inbox checks; changing delivery mode can kill project watcher processes, so do it before starting long-running project watchers.
-6. Send `AGMSG-TASK v1` with the exact artifact paths and `done_signal=AGMSG-RESULT`. Pass every `send.sh`/`poke.sh` body with `--body-file <path>` (both take it in agmsg v1.5.0), never as a positional argument: a positional `<text>` passes through the caller's own shell first, where a backtick or `$( )` in the body silently executes and vanishes from what arrives (upstream #378). `agmsg-dispatch` is the one exception and takes a single-line, shell-safe positional message. Pick the path by how the recipient is seated, never by inferring pane or agent status: a worker in a `herdr-agents` pane gets `agmsg-dispatch <team> <from> <to> <pane_id> "<message>"` (send, generic wake, `read_at` wait; single-line shell-safe text only), the sanctioned wake path until worker seating writes placement records at launch, because `poke.sh` exits 1 with "no placement record" for a hand-joined member, and a herdr-agents worker gets a record only once it acts from its own pane (upstream `send.sh`/`inbox.sh` record the acting pane, #1109); a spawn-seated member (placement record `run/spawn.*`; `team.sh <team> --json` shows its pane) gets `poke.sh <team> <name> --body-file <path> [--retries N --retry-delay SECONDS --backoff fixed|exponential]`, which types and submits in one call and refuses to type over an in-progress draft (#1321/#1322); a pane-less member gets `send.sh <team> <from> <to> --body-file <path>` and its own delivery mode. Verify delivery via the messages.db `read_at` column. `poke.sh` exit codes: 10 = terminal unreachable, 12 = pane gone or no live agent, 14/15 = refused to type over a changing or unlocatable input box, 13 = the driver has no poke path for this pane (for example a `plain` terminal); where poke.sh's narrow agmsg-message fallback succeeds it exits 0, so 13 means nothing was delivered, and the printed reason names the native channel, asks the caller to claim its own identity first, or reports that the fallback failed. Never retry a 13 as `send.sh` yourself: that overrides the driver's considered refusal and can double-deliver. Seating case: a worker in an unviewed or headless Herdr workspace (no client attached, a small pane rect such as 18x41) makes `poke.sh` exit 14/15 from its TUI input locator; that is a locator refusal, not evidence about the worker's state, so wake it with `agmsg-dispatch` and verify `read_at`.
+6. Send `AGMSG-TASK v1` with the exact artifact paths and `done_signal=AGMSG-RESULT`. Pass every `send.sh`/`poke.sh` body with `--body-file <path>` (both take it in agmsg v1.5.0), never as a positional argument: a positional `<text>` passes through the caller's own shell first, where a backtick or `$( )` in the body silently executes and vanishes from what arrives (upstream #378). `agmsg-dispatch` is the one exception and takes a single-line, shell-safe positional message. Pick the path by how the recipient is seated, never by inferring pane or agent status: a worker in a `herdr-agents` pane gets `agmsg-dispatch <team> <from> <to> <pane_id> "<message>"` (send, generic wake, `read_at` wait; single-line shell-safe text only), the sanctioned wake path until worker seating writes placement records at launch, because `poke.sh` exits 1 with "no placement record" for a hand-joined member, and a herdr-agents worker gets a record only once it acts from its own pane (upstream `send.sh`/`inbox.sh` record the acting pane, #1109); a spawn-seated member (placement record `run/spawn.*`; `team.sh <team> --json` shows its pane) gets `poke.sh <team> <name> --body-file <path> [--retries N --retry-delay SECONDS --backoff fixed|exponential]`, which types and submits in one call and refuses to type over an in-progress draft (#1321/#1322); a pane-less member gets `send.sh <team> <from> <to> --body-file <path>` and its own delivery mode. Verify delivery via the messages.db `read_at` column. `poke.sh` exit codes: 10 = terminal unreachable, 12 = pane gone or no live agent, 14/15 = refused to type over a changing or unlocatable input box, 13 = the driver has no poke path for this pane (for example a `plain` terminal); where poke.sh's narrow agmsg-message fallback succeeds it exits 0, so 13 means nothing was delivered, and the printed reason names the native channel, asks the caller to claim its own identity first, or reports that the fallback failed. Never retry a 13 as `send.sh` yourself: that overrides the driver's considered refusal and can double-deliver. Seating case: a worker in an unviewed or headless Herdr workspace (no client attached, a small pane rect such as 18x41) makes `poke.sh` exit 14/15 from its TUI input locator; that is a locator refusal, not evidence about the worker's state, so wake it with `agmsg-dispatch` and verify `read_at`. Every dispatch (TASK, ACCEPTANCE, PING) is recorded in the current acceptance record under a `dispatch:` key as the bus line with its read marker; a seat is reported as working only from such a line, and after a context compaction the open TASK list is re-derived from a bus read that is refused when it reaches its limit (`bus-read.sh` exits when the history reaches `BUS_READ_LIMIT`; the orchestrator raises the limit and reads again), never from a default-limited one and never from a read whose truncation went unnoticed. A seated worker idle for 20 minutes since its latest bus event for the task while a dispatchable task exists (INV-10's idle figure; its 30 minutes is the first-push deadline) gets a bus read, then a PING; a longer silent wait is never the answer. `scripts/orchestrator/dispatch.sh` writes the line and `scripts/orchestrator/bus-read.sh` performs the read and prints the minutes since each open task's latest event (both on main since a03c1daa, plan 007 T718); the orchestrator applies the 20-minute figure to the minutes the script prints (the script's own silence flag still uses 30 minutes, a recorded residual of the tools lineage).
 7. Track `max_turns`. Use `AGMSG-PING` for liveness if a worker stalls.
 8. On `AGMSG-RESULT`, read the task file and every referenced artifact before deciding.
 9. For a RESULT carrying `effects`, verify that every declared effect has the report's stated reverse mapping before acceptance; record any irreversible effect in the acceptance note.
@@ -167,7 +169,7 @@ AGMSG-PONG v1 task_id=<id> status=alive|blocked|question note=<short-note>
     1. Sweep the final head's feedback with `scripts/pr-feedback.py <pr> --json .orchestration/validation/<task>-pr-feedback.json` and give every item a `fixed:<commit>` or `not-applicable:<reason>` disposition, leaving none on `failure` or `warning` annotations. Optionally request `@coderabbitai full review` on the final head first; when a CodeRabbit review exists it is swept like any other item, and the gate does not require a bot review. An `open:<thread id>` item from a worker's third Bot round is a sweep item like any other: it becomes `fixed:<sha>` through a revise round that carries its `check=` (a round that counts toward INV-6 like any other), or `not-applicable:<reason>` with a pasted refutation; until one of those exists the PR is not merged, never with the thread open.
     2. Run the task-level audit of that head in the pair or headless form of the task-level audit bullet. It exits nonzero for every verdict other than `correct`. An exit with `Audit verdict: incorrect` is not a failed step: continue to step 3 and disposition its findings. A `blocked` or missing verdict means re-running the audit.
     3. Write the acceptance record, summarising the dispositions, with an `audit-finding:` line for every audit finding whatever the verdict (the gate needs them, through `AUDIT_DISPOSITIONS`, when it is `incorrect`).
-    4. Run the gate: `AUDIT_EVIDENCE=<audit> [AUDIT_DISPOSITIONS=<acceptance record>] AGENT_REVIEWED=1 REVIEW_EVIDENCE=<receipt> BASE=origin/main PR_FEEDBACK_EVIDENCE=<json> make require-crit-review`.
+    4. Run the gate: `AUDIT_EVIDENCE=<audit> [AUDIT_DISPOSITIONS=<acceptance record>] AGENT_REVIEWED=1 REVIEW_EVIDENCE=<receipt> ACCEPTANCE_EVIDENCE=<acceptance record> BASE=origin/main PR_FEEDBACK_EVIDENCE=<json> make require-crit-review`.
        - A `review` sweep item whose body carries a `P0`–`P3` badge is a finding with its own `fixed:<commit>` or `not-applicable:<reason>` disposition, never a container for its inline threads.
        - The sweep covers issue comments, reviews, inline review comments with thread resolution, non-passing check runs, check-run annotations at every level (`notice`, `warning`, `failure`), and commit statuses. A `failure` marked `not-applicable` needs a concrete reason of at least 20 characters.
        - A CodeRabbit full review is optional, at most once on the final head: the plan allows one review per hour and every review event spends one (docs.coderabbit.ai/management/rate-limits).
diff --git a/tests/fixtures/regime/code-review-orchestration.md b/tests/fixtures/regime/code-review-orchestration.md
index 22d0e3c7..d7586157 100644
--- a/tests/fixtures/regime/code-review-orchestration.md
+++ b/tests/fixtures/regime/code-review-orchestration.md
@@ -1,5 +1,5 @@
 ### Orchestration records and trust-boundary code
 
 - Files under `.orchestration/**` are the regime's records and task specifications, which the regime's own reviewers review; in the pull-request review by the Codex Bot, review them for secrets and home-directory paths only, except a trust-boundary task's `threat_table` and the task metadata needed to judge it, which the next bullet covers. The task-level audit keeps the full scope of the Audit section.
-- Judge from the diff, whatever the task's metadata says, whether a change touches a trust boundary (anything the design tier lists, CI that decides a required check, code that executes PR-controlled input). Review such code against the task's `threat_table`: report a missing table or a missing row; report a `closed` row whose test does not close it, a `residual` row whose control does not mitigate the risk, and an `out-of-scope` row whose owner does not own it. Do not re-raise a `residual` row whose control mitigates the risk. Shape (the test selector, the sentence, the owning task id) is the schema's to check, not the review's. Until `schemas/task.json` lands in wave V1, the task-file review checks the three shape rules by hand.
+- Judge from the diff, whatever the task's metadata says, whether a change touches a trust boundary (anything the design tier lists, CI that decides a required check, code that executes PR-controlled input). Review such code against the task's `threat_table`: report a missing table or a missing row; a row's unit is the SKILL threat-table bullet's (one per `allowed_files` entry, one per non-path control, one per orchestrator effect), so review a missing row at that unit; report a `closed` row whose test does not close it, a `residual` row whose control does not mitigate the risk, and an `out-of-scope` row whose owner does not own it. Do not re-raise a `residual` row whose control mitigates the risk. Shape (the test selector, the sentence, the owning task id) is the schema's to check, not the review's. Until `schemas/task.json` lands in wave V1, the task-file review checks the three shape rules by hand.
 - Keep lint and formatting to CI.
diff --git a/tests/fixtures/regime/invariants.md b/tests/fixtures/regime/invariants.md
index 90eb9ddc..8c5989d9 100644
--- a/tests/fixtures/regime/invariants.md
+++ b/tests/fixtures/regime/invariants.md
@@ -3,10 +3,12 @@
 - Review every RESULT adversarially across correctness, regressions, security, and reporting omissions: try to refute it, independently re-derive findings, and never treat sampled spot checks as full verification.
 - Acceptance review, adversarial RESULT review, and review-profile work remain orchestrator-side; never delegate them to a worker, and keep `make require-crit-review` as the final integration step. Revisit only if worker-side model capability surpasses the orchestrator tier.
 - A design review runs in paired rounds. Both reviewers, a fresh Claude context on the `review` profile and a Codex read-only run under a `codex-review` identity, get the same design hash at the same time. The orchestrator revises once per pair of results and opens no round while one is still open. The third pair is the last: on its accept the design is frozen at the hash the pair last accepted, the third pair's own, and whatever is still open at that hash becomes a residual list that is worker input; on its revise or reject nothing is frozen and the design goes back to a context other than its author, never to a fourth pair; a revision after the third pair is not made, and any later change to a hashed key is a new pair (INV-7). The review judges the invariants, threat model, trust anchors and premises for contradiction and enforceability, never implementation detail.
-- A task-file review is one round with a fixed stop condition: no contradiction with the design, the premises hold, `allowed_files` covers every touch point that grep finds, and one invariant check (a `-contract-a01` id maps to its implementing entry). Anything finer belongs to the worker and the implementation PR.
+- A task-file review is one round with a fixed stop condition: no contradiction with the design, the premises hold, `allowed_files` covers every touch point that grep finds, and one invariant check (for a task that carries an `invariants` key: the task id maps to its `implementing_tasks` entry, the invariant ids match, and each invariant's sentence equals the design's byte-for-byte, the design read from main (INV-2), checked by hand in the review until a checker lands; a task without the key needs no entry). Anything finer belongs to the worker and the implementation PR.
 - A boundary PR synchronizes records at a boundary. It carries no task draft under review. A design not yet on `main` lands through a merged boundary PR before its implementing TASK is dispatched (INV-2), and any merged boundary that carries the design meets that precondition.
-- A task that touches a trust boundary (anything the design tier lists, CI that decides a required check, code that executes PR-controlled input) carries a `threat_table` in its front matter: one `{control, disposition}` row per thing the PR or the orchestrator controls (the tree and its tests, task.md, workflow files, interpreter and environment files, in-process effects, new or renamed scripts, metadata separators). A disposition takes one of three forms: `closed: tests/<file>::<name>`, the test that closes the row; `residual: <sentence>`, the compensating control; `out-of-scope: <task id>`, the task that owns the row. Shape is `schemas/task.json`'s (wave V1): a `closed` selector names a test present in the PR tree at acceptance and in the schema's validation of the PR, an `out-of-scope` owner is a task id in the design's `implementing_tasks`, a `residual` payload is a sentence of at least 20 characters (the gate's minimum for a reason). Until `schemas/task.json` lands in wave V1, the task-file review checks the three shape rules by hand. For a `closed` row it checks the selector's form only, since the test does not exist before implementation. Substance is the reviewers': the task-file review, the Bot and the auditor judge each row against the diff. The table is the task's completion condition: a missing row is added once, counted as an amendment, never fixed finding by finding.
+- A task that touches a trust boundary (anything the design tier lists, CI that decides a required check, code that executes PR-controlled input) carries a `threat_table` in its front matter: one `{control, disposition}` row per thing the PR or the orchestrator controls (the tree and its tests, task.md, workflow files, interpreter and environment files, in-process effects, new or renamed scripts, metadata separators). The row unit is one row per `allowed_files` entry, one row per listed control that is not a path (task metadata, workflow and interpreter or environment inputs, in-process effects, new or renamed scripts, metadata separators), carried by the declared test module's row where that is where the control acts, and one row per orchestrator effect from the fixed list (forced removal, merge, update-branch); under a wildcard `allowed_files` entry whose files are executed or applied (scripts, workflows, hooks, settings, the rules seats follow), one row per concrete file the PR changes; a wildcard over test fixtures or other data files keeps one row; C4 of the task-consistency check (plan 007 T704) verifies the path half once it lands, and the task-file review checks it by hand until then. A disposition takes one of three forms: `closed: tests/<file>::<name>`, the test that closes the row; `residual: <sentence>`, the compensating control; `out-of-scope: <task id>`, the task that owns the row. Shape is `schemas/task.json`'s (wave V1): a `closed` selector names a test present in the PR tree at acceptance and in the schema's validation of the PR, an `out-of-scope` owner is a task id in the design's `implementing_tasks`, a `residual` payload is a sentence of at least 20 characters (the gate's minimum for a reason). Until `schemas/task.json` lands in wave V1, the task-file review checks the three shape rules by hand. For a `closed` row it checks the selector's form only, since the test does not exist before implementation. Substance is the reviewers': the task-file review, the Bot and the auditor judge each row against the diff. The table is the task's completion condition: a missing row is added once, counted as an amendment, never fixed finding by finding.
 - Before every acceptance action (revise, accept, merge) the orchestrator runs `scripts/regime-counters.sh <task id>` and pastes its output into the acceptance record. S2 is decided from INV-6's counts: each component the script prints is read from its output, and for each component it prints as `unknown` the record pastes the command and output that read the source INV-6 names for that component, or, while that source has no entry for the task, says so and pastes the reading of the interim record the orchestrator used in its place. S1 (plan 006: the same finding class three times on one artifact, from any reviewer) is decided from the record's finding-class table, which gives a class to every finding the PR-feedback sweep lists, whatever its disposition, and to every task-level audit finding; three rows of one class stop the artifact.
+- A change to a rule sentence requested of a worker travels as a task amendment (hashed, checked by the task-consistency check C1 to C6 once plan 007 T704 lands it and by hand until then, confirmed by the review seat), never as a PONG answer.
+- When a finding class reaches three on one artifact (the record's ledger) or `scripts/regime-counters.sh` prints an S1 candidate, the next acceptance action is the records search for that class, pasted into the record as the line `search: <class> -> <the matching mistake records or none>`, and the matching correction is applied when its mechanism is landed, or landed first when it is pending, mechanism by mechanism, before any dispatch; a class is a slug of `[a-z0-9-]` assigned at disposition time, never text taken from a review title. Once plan 007 T718 lands, `scripts/orchestrator/three-repeat.sh <class>` validates the slug, runs the records search and the CompactionDB search without a shell and prints the line; until then the orchestrator runs them by hand with a validated slug. Once `dotfiles-T128-gate-evidence-a02` lands, the gate refuses the action without the line; until then the orchestrator refuses it by rule. Every `not-applicable` disposition carries `; evidence=<command>` with the output pasted in the record.
 - At regime or session boundaries, write pending acceptance records, then mechanically commit every `.orchestration` file so no untracked tail remains. The sync needs no per-task artifact set: its audit record is the commit, whose message lists covered task IDs, plus agmsg ACCEPTANCE history. `make check-regime-boundary` reports a canonical clone with unmerged entries, a stash, or a difference from `origin/main` under `home/`, `install/` or `scripts/` as a sign that something ran where it must not. Lessons from a session are codified in this repository (a rule, the skill, or a check) through a task; Claude auto-memory is not a durable store for regime procedure. The canonical clone is pull and apply only and untouched by any seat: no edits, no apply from a dirty tree (the run_before guard refuses it), and one orchestrator identity per repository, seated at the working clone.
 - Stop checklist, at every regime or session boundary and in this order: write pending acceptance records; mask every `.orchestration` file the boundary commit adds or changes with `uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets <files>`, which also normalises home directories to `~`; run `make validate-agent-assets` (real exit status); make the `.orchestration` boundary commit with zero untracked tail on a fresh `orchestration/boundary-<YYYY-MM-DD>` branch from `origin/main` and merge its PR with `gh pr merge --squash --auto`; remove every worker with `herdr-agents --remove-worker <worktree>` (despawn, delivery off, leave, tab or workspace closed); check stale identities with `identities.sh <path> <type>` (exactly one name at the main checkout, none at a worker worktree); close Crit review servers (`pgrep -f 'crit _serve'` must be empty); in a CompactionDB-opted-in project, review `uv run --no-project .claude/hooks/contextdb_cli.py memory candidates --limit 20` and promote each candidate worth keeping with `uv run --no-project .claude/hooks/contextdb_cli.py memory promote <id> --scope project`, or leave it. The orchestrator workspace itself stays resident for the next session unless the operator restarts the machine. `make check-regime-boundary` (`scripts/check-regime-boundary.sh`) checks this list and the orchestrator seat lock, one line per violation.
 - Before every `.orchestration` boundary commit, run the masker on the files it adds or changes (`uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets <files>`), then `make validate-agent-assets`, and branch on its real exit status, never through a pipe; fix a failure before pushing, because committed audit evidence can trip the secret scan, which also rejects a home directory path in `.orchestration/**`.
diff --git a/tests/fixtures/regime/orchestrator-step-6.md b/tests/fixtures/regime/orchestrator-step-6.md
new file mode 100644
index 00000000..dd36748b
--- /dev/null
+++ b/tests/fixtures/regime/orchestrator-step-6.md
@@ -0,0 +1 @@
+6. Send `AGMSG-TASK v1` with the exact artifact paths and `done_signal=AGMSG-RESULT`. Pass every `send.sh`/`poke.sh` body with `--body-file <path>` (both take it in agmsg v1.5.0), never as a positional argument: a positional `<text>` passes through the caller's own shell first, where a backtick or `$( )` in the body silently executes and vanishes from what arrives (upstream #378). `agmsg-dispatch` is the one exception and takes a single-line, shell-safe positional message. Pick the path by how the recipient is seated, never by inferring pane or agent status: a worker in a `herdr-agents` pane gets `agmsg-dispatch <team> <from> <to> <pane_id> "<message>"` (send, generic wake, `read_at` wait; single-line shell-safe text only), the sanctioned wake path until worker seating writes placement records at launch, because `poke.sh` exits 1 with "no placement record" for a hand-joined member, and a herdr-agents worker gets a record only once it acts from its own pane (upstream `send.sh`/`inbox.sh` record the acting pane, #1109); a spawn-seated member (placement record `run/spawn.*`; `team.sh <team> --json` shows its pane) gets `poke.sh <team> <name> --body-file <path> [--retries N --retry-delay SECONDS --backoff fixed|exponential]`, which types and submits in one call and refuses to type over an in-progress draft (#1321/#1322); a pane-less member gets `send.sh <team> <from> <to> --body-file <path>` and its own delivery mode. Verify delivery via the messages.db `read_at` column. `poke.sh` exit codes: 10 = terminal unreachable, 12 = pane gone or no live agent, 14/15 = refused to type over a changing or unlocatable input box, 13 = the driver has no poke path for this pane (for example a `plain` terminal); where poke.sh's narrow agmsg-message fallback succeeds it exits 0, so 13 means nothing was delivered, and the printed reason names the native channel, asks the caller to claim its own identity first, or reports that the fallback failed. Never retry a 13 as `send.sh` yourself: that overrides the driver's considered refusal and can double-deliver. Seating case: a worker in an unviewed or headless Herdr workspace (no client attached, a small pane rect such as 18x41) makes `poke.sh` exit 14/15 from its TUI input locator; that is a locator refusal, not evidence about the worker's state, so wake it with `agmsg-dispatch` and verify `read_at`. Every dispatch (TASK, ACCEPTANCE, PING) is recorded in the current acceptance record under a `dispatch:` key as the bus line with its read marker; a seat is reported as working only from such a line, and after a context compaction the open TASK list is re-derived from a bus read that is refused when it reaches its limit (`bus-read.sh` exits when the history reaches `BUS_READ_LIMIT`; the orchestrator raises the limit and reads again), never from a default-limited one and never from a read whose truncation went unnoticed. A seated worker idle for 20 minutes since its latest bus event for the task while a dispatchable task exists (INV-10's idle figure; its 30 minutes is the first-push deadline) gets a bus read, then a PING; a longer silent wait is never the answer. `scripts/orchestrator/dispatch.sh` writes the line and `scripts/orchestrator/bus-read.sh` performs the read and prints the minutes since each open task's latest event (both on main since a03c1daa, plan 007 T718); the orchestrator applies the 20-minute figure to the minutes the script prints (the script's own silence flag still uses 30 minutes, a recorded residual of the tools lineage).
diff --git a/tests/unit/test_agmsg_orchestration_docs.py b/tests/unit/test_agmsg_orchestration_docs.py
index e4862721..86d0178f 100644
--- a/tests/unit/test_agmsg_orchestration_docs.py
+++ b/tests/unit/test_agmsg_orchestration_docs.py
@@ -223,6 +223,7 @@ class AgmsgRegimePatternTest(unittest.TestCase):
         # name, file, outer slice or None, (start, end): the start marker is part of the pinned text.
         ("invariants", SKILL, None, ("## Review and integration invariants", "\n## ")),
         ("worker-step-15", SKILL, None, ("\n15. After the final push", "\n## ")),
+        ("orchestrator-step-6", SKILL, ("## Orchestrator Playbook", "\n## "), ("\n6. ", "\n7. ")),
         ("orchestrator-step-7", SKILL, ("## Orchestrator Playbook", "\n## "), ("\n7. ", "\n8. ")),
         ("message-contract", SKILL, None, ("## Message Contract v1", "\n## ")),
         (
@@ -275,10 +276,17 @@ class AgmsgRegimePatternTest(unittest.TestCase):
             "no contradiction with the design",
             "the premises hold",
             "`allowed_files` covers every touch point that grep finds",
-            "one invariant check (a `-contract-a01` id maps to its implementing entry)",
+            # Plan 006 B0: design v20 removed contract PRs, so the check names the implementing_tasks entry;
+            # thread 4247933561: a task without an `invariants` key (a docs or review task) needs no entry;
+            # thread 4257278283: matching ids is not enough, so each sentence is compared with the design's.
+            "one invariant check (for a task that carries an `invariants` key: the task id maps to its "
+            "`implementing_tasks` entry, the invariant ids match, and each invariant's sentence equals the design's "
+            "byte-for-byte, the design read from main (INV-2), checked by hand in the review until a checker lands; "
+            "a task without the key needs no entry)",
         ):
             with self.subTest(token=token):
                 self.assertIn(token, text)
+        self.assertNotIn("-contract-a01", text)
 
     def test_a_design_lands_on_main_before_its_task(self) -> None:
         # Thread 4243537281: a boundary PR carrying the design is INV-2's dispatch prerequisite.
@@ -508,6 +516,118 @@ class AgmsgRegimePatternTest(unittest.TestCase):
             with self.subTest(token=token):
                 self.assertIn(token, step)
 
+    def test_dispatches_are_recorded_from_the_bus(self) -> None:
+        # Plan 007 T703 item 1 (C-12): a seat's status comes from a bus line, never from memory; plan 010 option D:
+        # the obligation stays here, and the commands move to plan 007 T718's scripts.
+        step = self.section(self.section(SKILL.read_text(), "## Orchestrator Playbook"), "\n6. ", "\n7. ")
+        for token in (
+            "Every dispatch (TASK, ACCEPTANCE, PING) is recorded in the current acceptance record under a "
+            "`dispatch:` key as the bus line with its read marker; a seat is reported as working only from such a "
+            # The local review of 7771082f: the merged bus-read.sh refuses a read at its limit; nothing reads all.
+            "line, and after a context compaction the open TASK list is re-derived from a bus read that is refused "
+            "when it reaches its limit (`bus-read.sh` exits when the history reaches `BUS_READ_LIMIT`; the "
+            "orchestrator raises the limit and reads again), never from a default-limited one and never from a read "
+            "whose truncation went unnoticed.",
+            # Threads 4248319936 and 4249303426: the clock runs from the seat's latest event for the task;
+            # thread 4257278271: INV-10's idle figure is 20 minutes, its 30 minutes the first-push deadline.
+            "A seated worker idle for 20 minutes since its latest bus event for the task while a dispatchable task "
+            "exists (INV-10's idle figure; its 30 minutes is the first-push deadline) gets a bus read, then a PING; "
+            "a longer silent wait is never the answer.",
+            # Thread 4249303413: history.sh shows the latest 20 rows unless given a limit.
+            "`scripts/orchestrator/dispatch.sh` writes the line and `scripts/orchestrator/bus-read.sh` performs the "
+            "read and prints the minutes since each open task's latest event (both on main since a03c1daa, plan 007 "
+            "T718); the orchestrator applies the 20-minute figure to the minutes the script prints (the script's own "
+            "silence flag still uses 30 minutes, a recorded residual of the tools lineage).",
+        ):
+            with self.subTest(token=token[:40]):
+                self.assertIn(token, step)
+        for stale in (
+            "expected duration",
+            "the bus line `history.sh <team>` prints",
+            "no bus event from its seat since",
+            "complete bus read",
+            "silent for thirty minutes",
+        ):
+            with self.subTest(stale=stale):
+                self.assertNotIn(stale, step)
+
+    def test_rule_changes_travel_as_task_amendments(self) -> None:
+        # Plan 007 Phase 0: a rule sentence changed through a PONG answer bypasses the hash and C1 to C6;
+        # plan 009 option A: the checker is not on main yet, so the sentence names its landing condition.
+        self.assertIn(
+            "A change to a rule sentence requested of a worker travels as a task amendment (hashed, checked by "
+            "the task-consistency check C1 to C6 once plan 007 T704 lands it and by hand until then, confirmed by "
+            "the review seat), never as a PONG answer.",
+            self.invariants(),
+        )
+
+    def test_three_repeats_start_with_a_pasted_correction_search(self) -> None:
+        # Plan 007 S6: the third repeat of a class is answered by a recorded correction, never by another fix round;
+        # plan 010 option D: the obligation stays here, and the commands move to plan 007 T718's three-repeat.sh.
+        bullet = self.section(self.invariants(), "\n- When a finding class reaches three on one artifact", "\n- ")
+        for token in (
+            # Threads 4247933574 and 4249303398: the records search, and a correction applied mechanism by mechanism.
+            " (the record's ledger) or `scripts/regime-counters.sh` prints an S1 candidate, the next acceptance "
+            "action is the records search for that class, pasted into the record as the line "
+            "`search: <class> -> <the matching mistake records or none>`, and the matching correction is applied "
+            "when its mechanism is landed, or landed first when it is pending, mechanism by mechanism, before any "
+            "dispatch; a class is a slug of `[a-z0-9-]` assigned at disposition time, never text taken from a review "
+            "title.",
+            # Thread 4249303433: review-derived text never reaches a shell.
+            "Once plan 007 T718 lands, `scripts/orchestrator/three-repeat.sh <class>` validates the slug, runs the "
+            "records search and the CompactionDB search without a shell and prints the line; until then the "
+            "orchestrator runs them by hand with a validated slug.",
+            # Thread 4248711363: the gate does not read the line yet, so the sentence names its landing condition.
+            "Once `dotfiles-T128-gate-evidence-a02` lands, the gate refuses the action without the line; until then "
+            "the orchestrator refuses it by rule.",
+            "Every `not-applicable` disposition carries `; evidence=<command>` with the output pasted in the record.",
+        ):
+            with self.subTest(token=token[:40]):
+                self.assertIn(token, bullet)
+        for stale in (
+            "`grep -rl <class slug> .orchestration/learning/corrections/`",
+            "`grep -l 'classes:",
+            "gate-evidence-a01",
+            "memory search <class slug>",
+        ):
+            with self.subTest(stale=stale):
+                self.assertNotIn(stale, bullet)
+
+    def test_threat_table_rows_have_a_fixed_unit(self) -> None:
+        # Plan 007 T703 item 4: without a unit, a missing row is a judgment call for each reviewer.
+        bullet = self.section(self.invariants(), "\n- A task that touches a trust boundary", "\n- ")
+        self.assertIn(
+            "metadata separators). The row unit is one row per `allowed_files` entry, one row per listed control "
+            "that is not a path (task metadata, workflow and interpreter or environment inputs, in-process effects, "
+            "new or renamed scripts, metadata separators), carried by the declared test module's row where that is "
+            "where the control acts, and one row per orchestrator effect from the fixed list (forced removal, merge, "
+            # Thread 4248711371: C4 is not on main yet, so the sentence names its landing condition.
+            # Thread 4257278276: an executed wildcard entry gets a row per changed file; a data wildcard keeps one.
+            "update-branch); under a wildcard `allowed_files` entry whose files are executed or applied (scripts, "
+            "workflows, hooks, settings, the rules seats follow), one row per concrete file the PR changes; a "
+            "wildcard over test fixtures or other data files keeps one row; C4 of the task-consistency check (plan "
+            "007 T704) verifies the path half once it lands, and the task-file review checks it by hand until then.",
+            bullet,
+        )
+        self.assertNotIn("C4 verifies the path half before dispatch", bullet)
+        rules = self.section((ROOT / "AGENTS.md").read_text(), "## Code Review Rules")
+        subsection = self.section(rules, "### Orchestration records and trust-boundary code", "\n### ")
+        self.assertIn(
+            "report a missing table or a missing row; a row's unit is the SKILL threat-table bullet's (one per "
+            "`allowed_files` entry, one per non-path control, one per orchestrator effect), so review a missing "
+            "row at that unit; report a `closed` row",
+            subsection,
+        )
+
+    def test_the_gate_reads_the_acceptance_record(self) -> None:
+        # Plan 007 T703 item 6: the gate reads the record's ledger and `search:` line once gate-evidence-a02 lands.
+        step = self.section(self.section(SKILL.read_text(), "## Orchestrator Playbook"), "\n10. ", "\n11. ")
+        self.assertIn(
+            "REVIEW_EVIDENCE=<receipt> ACCEPTANCE_EVIDENCE=<acceptance record> BASE=origin/main "
+            "PR_FEEDBACK_EVIDENCE=<json> make require-crit-review",
+            step,
+        )
+
 
 class AgmsgOrchestrationSingleSourceTest(unittest.TestCase):
     """The audit command appears once, in the SKILL's task-level audit bullet; everything else points there."""

**Adjusting output settings**
exec
/bin/zsh -lc 'nl -ba .orchestration/acceptance/dotfiles-T128-playbook-rules-a04.md' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 42ms:
     1	# Acceptance: dotfiles-T128-playbook-rules-a04 (plan 007 T703, INV-6 successor of a03 after plan 010 option D) — in progress
     2	
     3	- **Task:** `.orchestration/tasks/dotfiles-T128-playbook-rules-a04.md` sha256 `e64ee6912c33d98305e70b4206f4d0f55bd4236730131a080f0fd81e7227f254`, written by the review seat (`dotfiles-T128-playbook-rules-redesign-a03`, anchor 15:23:59Z); reset record `dotfiles-T128-playbook-rules-a03-design-reset.md`; C1 to C9 OK.
     4	- **Worker:** `claude-standard-dot-a003` at `.claude/worktrees/worker-c`, continuing on `regime/playbook-rules` (PR #328, held at `fe34f7db`; PR head `e12872cd`).
     5	- **Precondition:** the boundary commit that lands a04 and the reset record (INV-2).
     6	- counters: run before the first acceptance action.
     7	- cost: n/a (pending)
     8	- dispatch (C-12 form; pasted 15:41Z): `  ○ [2026-10-12T15:40:52Z] claude-deep-dot → claude-standard-dot-a003: AGMSG-TASK v1 task_id=dotfiles-T128-playbook-rules-a04 repo=~/Workspace/dotfiles/.claude/worktrees/worker-c task_fi`; preconditions met: boundary PR #333 merged 15:39:49Z as `3709a6d8` (a04 and the a03 reset record on main).
     9	- 2026-10-12 16:04:45Z RESULT (bus 779): `status=ready_for_review head=2276a365`; CI 12 green; the worker's four a03 threads `fixed:beee078a`. 16:03:26Z Bot review 5493270947 on 2276a365: thread 4250028600 P1 (`SKILL.md:74`: the counters' S1 candidate is review-title text, the rule wants a slug). Class at disposition time: `search-procedure` (also `unlanded-mechanism-stated-as-present`), the next row after the third S1 cycle → S7, plan 012; M-20261012-23 / C-25. Counters 16:07:36Z: `tasks=1 amendments=0 questions=0 results=1 withdrawn=0 revises=0`.
    10	- 2026-10-13 01:05Z operator: plan 012 option B. No ACCEPTANCE line to the worker yet: a04 is held unchanged until `dotfiles-T128-orchestrator-tools-a01` (T718's first slice: counters slug, three-repeat.sh, bus-read.sh, dispatch.sh) merges; then `gh pr update-branch 328`, Bot, sweep (4250028600 → `fixed:<T718 squash sha>`), audit, gate. The worker a003 takes T718 on a fresh branch meanwhile (its worktree keeps `regime/playbook-rules`).
    11	
    12	- 01:45Z ACCEPTANCE sent to a003 (bus 809, created 01:48:18Z): `status=accepted` (head 2276a365 is the final text under plan 012 B; thread 4250028600 closes when T718 a01 lands; integration by the orchestrator after that merge; no worker action on a04). Sent because the Stop gate requires one ACCEPTANCE per RESULT and the deliverable itself needs no change.
    13	
    14	- 10:12Z T718 first slice merged (a03c1daa); `integrate-328.sh a03c1daa`: update-branch to `7771082f` (09:58:25Z), CI 13 green, Bot review 5501887212 (10:03:30Z) with three new threads on the a04 rule text: 4257278283 (P1, SKILL.md:69, the task-file review's invariant check compares ids only where the design (regime-v3-a01:56) requires byte-for-byte sentence equality), 4257278271 (P2, SKILL.md:164, "thirty minutes" where the design (:64) limits worker idleness to 20; INV-10's 30 is the first-push deadline), 4257278276 (P2, SKILL.md:71, the row unit per `allowed_files` entry lets one wildcard row cover several trust-boundary scripts); the C-32 local review of 7771082f (`dotfiles-T128-playbook-rules-a04-local-review-7771082.md`): one P2 (SKILL.md:164, `history.sh --limit 1000` is not a complete read after compaction; a read at its limit must be refused or paginated). Lines 69, 71 and 164 follow the a04 task text (line 78: "thirty minutes", the "complete bus read … --limit"; the invariant check as ids), so the fixes need amendment 1 of a04 (INV-6: amendments=0, revises=0 before it) and one revise round; the G′ pattern of plan 016 applies: owner first (a follow-up rules task on main owns the residual P2 of the final head by ledger reference), then the fix under the guards on the same PR. S6 searches pasted below.
    15	
    16	4257278283	design-mismatch
    17	4257278271	design-mismatch
    18	4257278276	threat-row-unit
    19	local:7771082:1	default-limited-read
    20	
    21	```text
    22	$ /usr/bin/grep -rl 'classes:.*design-mismatch' .orchestration/learning/mistakes/
    23	(no file)
    24	$ /usr/bin/grep -rli -- 'design-mismatch' .orchestration/learning/mistakes/
    25	(no file)
    26	$ uv run --no-project .claude/hooks/contextdb_cli.py memory search --limit 1000 -- design-mismatch | grep -cE '^[0-9a-f]{8}-'
    27	0
    28	$ /usr/bin/grep -rl 'classes:.*threat-row-unit' .orchestration/learning/mistakes/
    29	.orchestration/learning/mistakes/M-20261012-14.md
    30	$ /usr/bin/grep -rli -- 'threat-row-unit' .orchestration/learning/mistakes/
    31	.orchestration/learning/mistakes/M-20261012-29.md
    32	.orchestration/learning/mistakes/M-20261012-14.md
    33	$ uv run --no-project .claude/hooks/contextdb_cli.py memory search --limit 1000 -- threat-row-unit | grep -cE '^[0-9a-f]{8}-'
    34	0
    35	$ /usr/bin/grep -rl 'classes:.*default-limited-read' .orchestration/learning/mistakes/
    36	.orchestration/learning/mistakes/M-20261012-33.md
    37	$ /usr/bin/grep -rli -- 'default-limited-read' .orchestration/learning/mistakes/
    38	.orchestration/learning/mistakes/M-20261012-33.md
    39	$ uv run --no-project .claude/hooks/contextdb_cli.py memory search --limit 1000 -- default-limited-read | grep -cE '^[0-9a-f]{8}-'
    40	0
    41	$ scripts/regime-counters.sh dotfiles-T128-playbook-rules-a04 --pr 328
    42	task=dotfiles-T128-playbook-rules-a04 tasks=1 amendments=0 questions=0 results=1 withdrawn=0 revises=0 first_result_head=2276a365cba9f104cadd7cd82f3fb0bfec7dac21 bot_p1_heads_after_result=unknown audits=unknown wall=2026-10-12T15:40:52Z..2026-10-12T16:04:45Z (0:23) source=live
    43	```
    44	
    45	## Ledger (machine rows id<TAB>class; the lineage a01 → a04 on PR #328, classes assigned from the thread titles at 10:17Z; the four rows of 7771082f are above)
    46	
    47	4247933544	threat-row-unit
    48	4247933561	design-mismatch
    49	4247933574	search-procedure
    50	4248319926	search-procedure
    51	4248319936	wall-clock
    52	4248711363	unlanded-mechanism-stated-as-present
    53	4248711371	unlanded-mechanism-stated-as-present
    54	4249303398	search-procedure
    55	4249303413	default-limited-read
    56	4249303426	wall-clock
    57	4249303433	search-procedure
    58	4249414388	search-procedure
    59	4250028600	search-procedure
    60	- 10:21Z decision pending (plan 017; S7 by the letter: `design-mismatch` at three on the lineage ledger beside `search-procedure` at six): the G′ pattern as the default (amendment 1 + the owner task `dotfiles-T128-playbook-rules-followup-a01` + one revise), the pair review of both drafts running (seat TASK and Codex half). The checker's C10 hit on item 3 (`regime-counters.sh` beside `; evidence=<command>`) is on main's copy too (pre-existing, outside the amendment). The awaiting-merge marker for #328 was removed deliberately: the head moves with the amendment round, so boundary (11) may run before it.
    61	- 10:30Z operator: plan 017 option G″ (the G′ pattern on this PR): amendment 1 + the owner task first on main, one revise round, residual P2 owned by `dotfiles-T128-playbook-rules-followup-a01`.
    62	- 10:32Z pair round 1 on the drafts: seat `revise` (P2 the owner task's premise 2 counted rows that exist only in the working tree and item 1 named no greppable source; P3 the history paragraph's "thirty minutes" without a superseded marker; P3 item 4's clause vs the fixtures wildcard row), Codex `revise` on the amendment (the same history leftover) and `confirm` on the owner task. Applied: premise 2 is a presence check on origin/main; item 1 is the `## Owned by dotfiles-T128-playbook-rules-followup-a01` section of this record (`<id>\t<class>` rows) landed by the boundary after a04's merge, the dispatch condition stated; the superseded parenthetical on line 74; item 4's clause scoped to executed or applied wildcards (data wildcards keep one row). Round 2 sent 10:32:02Z (a04 `c5dbc2c3…`, owner `cb32794d…`).
    63	- 10:33Z INV-6 with GitHub: `bot_p1_heads_after_result=1` (7771082f); a P1 on the amendment head would reach two (reset). The map agent's record check raised it; the counters inside the sandbox print `unknown` (no gh), outside they print the figure.
    64	- 10:34Z pair-confirmed: a04 amendment 1 at `c5dbc2c3d3514707870c2146ac4acfd6e96279d50f0f6bf04bd8921cd242a6fa`, the owner task at `cb32794d2bb939456e747230e012729d47c327946fbe07fe97d644969dc4fa42` (seat round 2, bus 933; Codex round 2). ACCEPTANCE sent; boundary (11) runs now, then the amendment line to a003.
    65	- 14:01Z plan 021 step 5.1: resume line (bus 945, revise referencing RESULT 779) read 13:57:31Z; the worker merges origin/main (4e7a9b3a), applies amendment 1 (items 1, 4, 5, Completion) with the token tests, pushes; the Bot reviews on PR open only now (operator setting 13:3xZ), so the new head gets no Bot round; the local review runs once on it; dispositions: the P1 and two P2 threads and the local finding `fixed:<sha>`; any new P2 → advisory, owned by `dotfiles-T128-playbook-rules-followup-a01`.
    66	
    67	local-finding: 7771082:1 fixed:e6602ca1 (local review of 7771082f, SKILL.md:164: the read refused at its limit, never a default-limited or silently truncated one)
    68	
    69	## Owned by dotfiles-T128-playbook-rules-followup-a01 (advisory findings of the final head; plan 020 step 1.2; rows id<TAB>class)
    70	
    71	local:65a3d71:1	rule-gap-pending-audit
    72	
    73	local-finding: 65a3d71:1 not-applicable:P1 by the post-round local review (SKILL.md:164: the rule requires dispatch logging into the current acceptance record and the tools refuse a missing record, but no sentence says the orchestrator creates the record before the first dispatch); plan 021 S21: the local review is a sampler and not the acceptance authority, so this finding is referred as input to the audit of this head, which decides; if the audit raises it as P0/P1 the PR stops (plan 020 step 4.2), otherwise it is advisory and owned by dotfiles-T128-playbook-rules-followup-a01; evidence=sed -n 1,20p .orchestration/validation/dotfiles-T128-playbook-rules-a04-local-review-65a3d71.md

**Noticing incomplete file read**
exec
/bin/zsh -lc "nl -ba .orchestration/tasks/dotfiles-T128-regime-v3-a01.md | sed -n '1,98p'; nl -ba .orchestration/tasks/dotfiles-T128-playbook-rules-followup-a01.md" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc 'nl -ba .orchestration/tasks/dotfiles-T128-playbook-rules-a04.md | tail -25; nl -ba .orchestration/reports/dotfiles-T128-playbook-rules-a04.md; nl -ba .orchestration/sandboxes/dotfiles-T128-playbook-rules-a04.md; nl -ba .orchestration/validation/dotfiles-T128-playbook-rules-a04-local-review-65a3d71.md' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc "nl -ba .orchestration/validation/dotfiles-T128-playbook-rules-a04.md | sed -n '1,165p'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 121ms:
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
     1	---
     2	format: 2
     3	task_id: dotfiles-T128-playbook-rules-followup-a01
     4	kind: docs
     5	security: false
     6	design_review:
     7	  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
     8	  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
     9	allowed_files:
    10	  - home/dot_agents/skills/agmsg-orchestration/SKILL.md
    11	  - AGENTS.md
    12	  - tests/unit/test_agmsg_orchestration_docs.py
    13	  - tests/fixtures/regime/*.md
    14	  - .orchestration/dotfiles-T128-playbook-rules-followup-a01/**
    15	after: [dotfiles-T128-playbook-rules-a04]
    16	threat_table:
    17	  - control: the PR edits home/dot_agents/skills/agmsg-orchestration/SKILL.md, the rules Claude seats follow once it is applied
    18	    disposition: "residual: the applied copy changes only after the merge and the operator's make update; before the merge the orchestrator's diff review and the audit from main judge every sentence, and tests/unit/test_agmsg_orchestration_docs.py pins each new sentence with a token and each changed section whole"
    19	  - control: the PR edits AGENTS.md "Code Review Rules", which the Codex Bot reads from the PR tree, so a PR can rewrite the Bot's rules for its own review
    20	    disposition: "residual: the Bot's review of a PR that edits its own rules is swept feedback with no gate authority (INV-7); the task-level audit runs with main's AGENTS.md as its instruction root (INV-5) and the orchestrator's review reads the diff; a change to Code Review Rules is review tier with one schema audit (INV-1)"
    21	  - control: the PR edits tests/unit/test_agmsg_orchestration_docs.py, the module that pins its own rule sentences, so it controls the oracle as well as the text
    22	    disposition: "residual: the orchestrator's diff review and the task-level audit from main read the test diff beside the prose diff"
    23	  - control: the PR edits tests/fixtures/regime/*.md, the expected values of test_regime_rule_sections_are_pinned_whole, so a rule and its fixture can change together
    24	    disposition: "residual: a fixture diff is the declared change itself (the test's message requires listing it in the RESULT, INV-12); the orchestrator's diff review and the task-level audit from main read each fixture diff beside the prose diff, and main keeps the previous fixture to compare against"
    25	  - control: the task-file copy on the branch (.orchestration/dotfiles-T128-playbook-rules-followup-a01/task.md)
    26	    disposition: "residual: the copy is byte-identical to the dispatched task file (sha256 in the worker's validation file, compared by the orchestrator at acceptance); the pair's receipts name this file's hash"
    27	  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    28	    disposition: "residual: read with PyYAML by task-consistency-check C1 to C6 before dispatch and by the orchestrator at acceptance, never by a hand-written parser; a changed field fails the byte comparison above"
    29	  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    30	    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file, so a second front matter or a moved separator fails acceptance"
    31	  - control: the branch evidence records under .orchestration/dotfiles-T128-playbook-rules-followup-a01/ (report.md, validation.md, sandbox.md, learning.md, autoskill.md)
    32	    disposition: "residual: they are the worker's untrusted claims; acceptance re-checks each claim against the diff, CI and the test output, and the audit reads those sources itself"
    33	  - control: in-process effects
    34	    disposition: "residual: none; the declared test module reads prose and fixtures and imports no changed script"
    35	  - control: workflow and interpreter or environment inputs
    36	    disposition: "residual: none in allowed_files; an undeclared change to such a file is outside the task and fails at the audit (INV-12)"
    37	  - control: new or renamed scripts
    38	    disposition: "residual: none; allowed_files names no script path, so a new or renamed script is an undeclared change the audit fails"
    39	  - control: orchestrator effect merge
    40	    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
    41	  - control: orchestrator effect update-branch
    42	    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
    43	  - control: orchestrator effect forced worker removal
    44	    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
    45	premises:
    46	  - claim: "the a04 task names this task as the owner of the residual findings of PR #328's final head"
    47	    command: "grep -c 'owned by dotfiles-T128-playbook-rules-followup-a01' .orchestration/tasks/dotfiles-T128-playbook-rules-a04.md"
    48	    output: "1"
    49	  - claim: "the a04 acceptance record is on origin/main (the owned section is appended to it by the boundary after a04's merge, before this task dispatches)"
    50	    command: "git cat-file -e origin/main:.orchestration/acceptance/dotfiles-T128-playbook-rules-a04.md && echo present"
    51	    output: "present"
    52	
    53	---
    54	
    55	# AGMSG-TASK dotfiles-T128-playbook-rules-followup-a01 — the residual findings of PR #328's final head (the owner task of T703 a04's Completion clause, plan 017; C-32's owner-first pattern)
    56	
    57	Written 2026-10-13 10:19Z by the orchestrator seat, pair-reviewed before dispatch. T703's a04 (PR #328) gets one revise round for the findings of its amendment-1 head (the Bot's and the C-32 local review's); a P2 finding on the final head that round did not fix is dispositioned on PR #328 as `not-applicable:advisory P2 owned by dotfiles-T128-playbook-rules-followup-a01; evidence=git show origin/main:.orchestration/tasks/dotfiles-T128-playbook-rules-followup-a01.md | grep -n 'item 1'` (the gate's full form once PR #329 lands) and recorded as a row of `.orchestration/acceptance/dotfiles-T128-playbook-rules-a04.md`'s ledger. This task fixes exactly those rows in the rule text after a04 merges; it exists on `main` before the findings do, so no boundary commit is needed between a04's final head and its merge. Review tier by INV-1 (`kind: docs`; the same files as a04). The threat table names every `allowed_files` entry plus the non-path controls; `task-consistency-check.py` C1 to C10 and C7b pass on this file.
    58	
    59	## What to do
    60	
    61	1. The owned rows: the `<id>\t<class>` rows under the heading `## Owned by dotfiles-T128-playbook-rules-followup-a01` in `.orchestration/acceptance/dotfiles-T128-playbook-rules-a04.md` as read from `origin/main` (Codex Bot P2 threads and local-review findings on a04's final head after its one revise round, each dispositioned on PR #328 as `not-applicable:advisory P2 owned by dotfiles-T128-playbook-rules-followup-a01; evidence=git show origin/main:.orchestration/tasks/dotfiles-T128-playbook-rules-followup-a01.md | grep -n 'item 1'` (the gate's full form once PR #329 lands)). That section is this item's whole definition, closed at a04's acceptance and landed by the boundary after a04's merge; this task dispatches only after that boundary (the dispatch line names the record's hash); a finding outside the section is not owned here, and a missing or empty section at dispatch makes this task a no-op that report.md states (the section is created at the lineage's acceptance, so it does not exist before that). For each row: the rule sentence it names is corrected against the design on `main` (`.orchestration/tasks/dotfiles-T128-regime-v3-a01.md`, read from main) and the thread's text, with one token test per changed sentence in `tests/unit/test_agmsg_orchestration_docs.py` (and the fixture under `tests/fixtures/regime/` when the pinned section changes), in the style of a04's item 7; the RESULT lists each row with `fixed:<sha>`.
    62	2. Nothing else changes: not the Worker Playbook, not the message contract, not any sentence outside the owned rows.
    63	
    64	## Validation
    65	
    66	- `uv run --no-project python -m unittest tests/unit/test_agmsg_orchestration_docs.py -v` output in the validation file, with the changed tests named and the fixture list.
    67	- `git diff --numstat origin/main...HEAD` in the validation file (INV-2 caps: at most 15 changed files outside `.orchestration/`, 500 added lines outside `tests/`, 1000 under `tests/`).
    68	
    69	## Completion
    70	
    71	The PR is ready for the orchestrator's integration when CI is green, the Bot wait of Worker Playbook step 15 is done, the validation file carries the outputs above, and the RESULT names every unresolved Bot thread with `fixed:<sha>` or a proposed `not-applicable:<reason>; evidence=<command>`. A fresh branch `regime/playbook-rules-followup` from `origin/main` after a04 merges, a new PR, `kind: docs`; the orchestrator runs the local review (C-32) on the pushed head and returns its findings with the Bot's in one revise round at most.

 succeeded in 163ms:
     1	# Validation: dotfiles-T128-playbook-rules-a04
     2	
     3	Seat `claude-standard-dot-a003` in `.claude/worktrees/worker-c`, branch `regime/playbook-rules`, PR #328. The branch was fast-forwarded from the worker's `fe34f7db` to the orchestrator's update-branch head `e12872cd` before any edit. `origin/main` is `3709a6d8`, and the merge-base is `e0e2fe62`. Every block is verbatim command output; `mise WARN` sandbox cache lines are filtered out.
     4	
     5	## 1. Branch and task copies
     6	
     7	```text
     8	$ git merge-base --is-ancestor fe34f7db e12872cd && echo "fast-forward"; git log --oneline e12872cd..HEAD
     9	fast-forward
    10	beee078a docs(regime): state the dispatch and three-repeat obligations, and leave their commands to T718's scripts
    11	ff2e7156 chore(orchestration): record the dotfiles-T128-playbook-rules-a04 task
    12	$ shasum -a 256 <main checkout>/.orchestration/tasks/dotfiles-T128-playbook-rules-a04.md .orchestration/dotfiles-T128-playbook-rules-a04/task.md
    13	e64ee6912c33d98305e70b4206f4d0f55bd4236730131a080f0fd81e7227f254  <main checkout>/.orchestration/tasks/dotfiles-T128-playbook-rules-a04.md
    14	e64ee6912c33d98305e70b4206f4d0f55bd4236730131a080f0fd81e7227f254  .orchestration/dotfiles-T128-playbook-rules-a04/task.md
    15	$ cmp <main checkout>/.orchestration/tasks/dotfiles-T128-playbook-rules-a04.md .orchestration/dotfiles-T128-playbook-rules-a04/task.md && echo identical
    16	identical
    17	$ for t in a01:1083a8c1 a02:4486dbdd a03:196d73ca; do git diff --quiet ${t#*:} HEAD -- .orchestration/dotfiles-T128-playbook-rules-${t%%:*}/task.md && echo "${t%%:*} copy unchanged since ${t#*:}"; done
    18	a01 copy unchanged since 1083a8c1
    19	a02 copy unchanged since 4486dbdd
    20	a03 copy unchanged since 196d73ca
    21	```
    22	
    23	## 2. Premises of the new sentences
    24	
    25	```text
    26	$ git diff --stat $(git merge-base HEAD origin/main) origin/main -- home/ AGENTS.md tests/ scripts/ Makefile | tail -1; echo "(empty: main moved only under .orchestration)"
    27	(empty: main moved only under .orchestration)
    28	$ git ls-tree -r --name-only origin/main scripts/orchestrator/ | wc -l   # T718 has not landed
    29	       0
    30	$ git ls-remote https://github.com/mryfmo/dotfiles 'refs/heads/regime/gate-evidence*'
    31	4e2266aae7cddb692a9d56d8a8d2c83e48cc8303	refs/heads/regime/gate-evidence
    32	$ history.sh dotfiles-conformance 2>/dev/null | wc -l; history.sh dotfiles-conformance --limit 1000 2>/dev/null | wc -l; history.sh dotfiles-conformance "" 1000 2>/dev/null | wc -l   # item 1 interim form
    33	      20
    34	     778
    35	     778
    36	$ sed -n "7,9p;45p" ~/.agents/skills/agmsg/scripts/history.sh; awk '/^(function )?storage_history/{p=1} p{n++; if(n>=8 && n<=12) print} n>12{exit}' ~/.agents/skills/agmsg/scripts/drivers/storage/jsonl.sh   # why --limit 1000 reads everything: history.sh passes --limit as the agent, storage_history skips a dash-led agent, then takes the second --limit as the limit value, which is non-numeric, so the limit is -1 (none)
    37	TEAM="${1:?Usage: history.sh <team> [agent_id] [limit]}"
    38	AGENT="${2:-}"
    39	LIMIT="${3:-20}"
    40	HIST_JSONL=$(storage_history "$TEAM" "$AGENT" --limit "$LIMIT")
    41	  local team="$1"; shift
    42	  local agent="" limit=""
    43	  if [ $# -gt 0 ] && [ "${1#-}" = "$1" ]; then agent="$1"; shift; fi
    44	  while [ $# -gt 0 ]; do case "$1" in --limit) limit="$2"; shift 2 ;; *) shift ;; esac; done
    45	  case "$limit" in ''|*[!0-9]*) limit="-1" ;; esac
    46	```
    47	
    48	## 3. Every quoted sentence of the task is in the prose verbatim
    49	
    50	```text
    51	$ uv run --no-project python "$TMPDIR/verbatim.py" "$PWD" .orchestration/dotfiles-T128-playbook-rules-a04/task.md
    52	item 1 quote 1: present (ok) 730 chars
    53	item 2 quote 1: present (ok) 33 chars
    54	item 2 quote 2: present (ok) 240 chars
    55	item 3 quote 1: present (ok) 1035 chars
    56	item 4 quote 1: present (ok) 544 chars
    57	item 4 quote 2: present (ok) 40 chars
    58	item 4 quote 3: present (ok) 173 chars
    59	item 5 quote 1: absent (ok) 73 chars
    60	item 5 quote 2: present (ok) 184 chars
    61	```
    62	
    63	## 4. Docs tests
    64	
    65	```text
    66	$ uv run --no-project python -m unittest tests/unit/test_agmsg_orchestration_docs.py -v
    67	test_docs_no_longer_name_codex_review_commit ... ok
    68	test_rule_and_skill_name_worker_seats_not_codex_workers ... ok
    69	test_rule_drops_the_worker_network_escalation ... ok
    70	test_skill_drops_the_pane_status_gate_and_raw_pane_wakes ... ok
    71	test_rule_pointers_name_real_skill_sections ... ok
    72	test_rule_states_the_invariants ... ok
    73	test_word_budgets ... ok
    74	test_audit_command_lives_only_in_the_task_level_audit_bullet ... ok
    75	test_codex_agents_points_at_the_worklog_section ... ok
    76	test_contextdb_cli_is_invoked_with_uv_run ... ok
    77	test_skill_masks_evidence_with_a_runnable_command ... ok
    78	test_claude_worker_merge_denials_and_prefix_limits_are_documented ... ok
    79	test_codex_worker_profile_defaults_to_standard ... ok
    80	test_skill_carries_the_audit_gate_and_bot_wait_mechanics ... ok
    81	test_skill_carries_the_parallel_execution_and_routing_mechanics ... ok
    82	test_skill_carries_the_registration_and_delivery_mechanics ... ok
    83	test_skill_carries_the_session_lessons ... ok
    84	test_a_design_lands_on_main_before_its_task ... ok
    85	test_a_revise_acceptance_names_the_previous_head_and_a_check ... ok
    86	test_a_trust_boundary_task_carries_a_threat_table ... ok
    87	test_bot_fix_rounds_are_capped_and_the_pr_is_ready_first ... ok
    88	test_boundary_merge_sentence_names_the_in_job_decision ... ok
    89	test_closed_selector_existence_is_checked_at_acceptance ... ok
    90	test_code_review_rules_cover_orchestration_records_and_threat_tables ... ok
    91	test_counters_bullet_names_owners_not_sources ... ok
    92	test_counters_run_before_every_acceptance_action ... ok
    93	test_design_review_runs_in_paired_rounds_with_a_cap ... ok
    94	test_dispatches_are_recorded_from_the_bus ... ok
    95	test_open_review_body_findings_have_an_identifier ... ok
    96	test_open_third_round_threads_have_an_integration_outcome ... ok
    97	test_orchestration_records_rule_binds_the_bot_review_only ... ok
    98	test_pattern_rules_pin_their_safeguards ... ok
    99	test_question_pongs_are_in_the_contract ... ok
   100	test_regime_rule_sections_are_pinned_whole ... ok
   101	test_rule_changes_travel_as_task_amendments ... ok
   102	test_shape_is_checked_by_hand_until_the_schema_lands ... ok
   103	test_shape_rules_and_the_decision_sentence_are_pinned ... ok
   104	test_task_file_review_is_one_round_with_a_fixed_stop_condition ... ok
   105	test_the_bot_wait_filters_the_codex_bot ... ok
   106	test_the_ci_watch_is_joined_before_the_result ... ok
   107	test_the_ci_watcher_survives_the_no_checks_race ... ok
   108	test_the_gate_reads_the_acceptance_record ... ok
   109	test_threat_table_rows_have_a_fixed_unit ... ok
   110	test_threat_table_rule_carries_no_grammar ... ok
   111	test_three_repeats_start_with_a_pasted_correction_search ... ok
   112	test_workers_commit_inside_the_sandbox ... ok
   113	test_workers_open_the_pr_as_a_draft ... ok
   114	
   115	----------------------------------------------------------------------
   116	Ran 47 tests in 0.009s
   117	
   118	OK
   119	```
   120	
   121	## 5. The module that pins the gate command, and format
   122	
   123	```text
   124	$ uv run --no-project python -m unittest tests/unit/test_pr_feedback.py 2>&1 | tail -n 3
   125	Ran 16 tests in 0.017s
   126	
   127	OK
   128	$ ruff format --config ruff.toml --check tests/unit/test_agmsg_orchestration_docs.py
   129	1 file already formatted
   130	```
   131	
   132	## 6. Each sentence fails its test when removed or put back to its previous form
   133	
   134	`mutate.py` (session scratch) restores each file with `git checkout --` on the committed tree. a04's mutants for item 1: 1a to 1e (1c puts back a03's silence sentence, 1e a03's re-derivation clause). For item 3: 3a to 3f (3d puts back a03's whole bullet, 3f a03's "without the paste"). The output names the failing test and its FAIL-line count, not the subTest label.
   135	
   136	```text
   137	$ uv run --no-project python "$TMPDIR/mutate.py" "$PWD"; git status --short
   138	mutant 1a home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_dispatches_are_recorded_from_the_bus -> rc=1 FAILED (failures=1) fail_lines=1
   139	mutant 1b home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_dispatches_are_recorded_from_the_bus -> rc=1 FAILED (failures=1) fail_lines=1
   140	mutant 1c home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_dispatches_are_recorded_from_the_bus -> rc=1 FAILED (failures=2) fail_lines=2
   141	mutant 1d home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_dispatches_are_recorded_from_the_bus -> rc=1 FAILED (failures=1) fail_lines=1
   142	mutant 1e home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_dispatches_are_recorded_from_the_bus -> rc=1 FAILED (failures=1) fail_lines=1
   143	mutant 2 home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_rule_changes_travel_as_task_amendments -> rc=1 FAILED (failures=1) fail_lines=1
   144	mutant 2b home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_rule_changes_travel_as_task_amendments -> rc=1 FAILED (failures=1) fail_lines=1
   145	mutant 3a home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_three_repeats_start_with_a_pasted_correction_search -> rc=1 FAILED (failures=1) fail_lines=1
   146	mutant 3b home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_three_repeats_start_with_a_pasted_correction_search -> rc=1 FAILED (failures=1) fail_lines=1
   147	mutant 3c home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_three_repeats_start_with_a_pasted_correction_search -> rc=1 FAILED (failures=1) fail_lines=1
   148	mutant 3d home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_three_repeats_start_with_a_pasted_correction_search -> rc=1 FAILED (failures=4) fail_lines=4
   149	mutant 3e home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_three_repeats_start_with_a_pasted_correction_search -> rc=1 FAILED (failures=1) fail_lines=1
   150	mutant 3f home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_three_repeats_start_with_a_pasted_correction_search -> rc=1 FAILED (failures=1) fail_lines=1
   151	mutant 4a home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_threat_table_rows_have_a_fixed_unit -> rc=1 FAILED (failures=1) fail_lines=1
   152	mutant 4c home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_threat_table_rows_have_a_fixed_unit -> rc=1 FAILED (failures=1) fail_lines=1
   153	mutant 4b AGENTS.md: test_threat_table_rows_have_a_fixed_unit -> rc=1 FAILED (failures=1) fail_lines=1
   154	mutant 5 home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_task_file_review_is_one_round_with_a_fixed_stop_condition -> rc=1 FAILED (failures=2) fail_lines=2
   155	mutant 5b home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_task_file_review_is_one_round_with_a_fixed_stop_condition -> rc=1 FAILED (failures=1) fail_lines=1
   156	mutant 6 home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_the_gate_reads_the_acceptance_record -> rc=1 FAILED (failures=1) fail_lines=1
   157	mutant 7 home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_regime_rule_sections_are_pinned_whole -> rc=1 FAILED (failures=1) fail_lines=1
   158	```
   159	
   160	## 7. Fixtures and size
   161	
   162	```text
   163	$ git show --stat --format=%h beee078a | tail -n 5
   164	 .../dot_agents/skills/agmsg-orchestration/SKILL.md |  4 +-
   165	 tests/fixtures/regime/invariants.md                |  2 +-

 exited 1 in 196ms:
    74	Written 2026-10-12 by the orchestrator seat under plan 007 (Phase 1, T703). a04 is a03's reset under plan 010 option D (the operator's choice, 15:19Z): the artifact's third S1 cycle, after search-procedure at three (13:24Z) and unlanded-mechanism-stated-as-present at three (14:01Z), the Bot's fourth round on a03's head `fe34f7db` found four more operational gaps in items 1 and 3 alone (4249303433, 4249303413, 4249303426, 4249303398; M-20261012-21, C-23: operational procedure written as rule prose), and the fix is task text, so INV-6's count; written by the review seat under the reset record `.orchestration/acceptance/dotfiles-T128-playbook-rules-a03-design-reset.md`. Items 1 and 3 now state the obligation and the script that performs it with its landing condition (plan 007 T718: `dispatch.sh`, `bus-read.sh`, `three-repeat.sh`), and every command, limit, grammar and clock beyond that moves to T718's scripts; items 2, 4, 5, 6, 7 and 8 are unchanged. The worker (`claude-standard-dot-a003`) holds at `fe34f7db`, its commits 196d73ca, f40e530a and fe34f7db stay, and it continues on PR #328 under a04. a03 is a02's reset under plan 009 option A (the operator's choice, 14:16Z): the artifact's second S1 cycle, the class unlanded-mechanism-stated-as-present at three (4248319926 on 375bae0f; 4248711363 and 4248711371 on a02's head `c4e0bb72`; M-20261012-19, C-21) after the first, search-procedure at three (13:24Z), and the fix is task text, so amendment 2 and INV-6's count; written by the review seat under the reset record `.orchestration/acceptance/dotfiles-T128-playbook-rules-a02-design-reset.md`. Items 2, 3, 4 and 6 now name their mechanisms in the SKILL's landing-condition form (present only when on `main`; otherwise once it lands, and the manual check until then); the worker (`claude-standard-dot-a003`) holds at `c4e0bb72`, its commits 4486dbdd, 4b62feda and c4e0bb72 stay, and it continues on PR #328 under a03. Amendment 1 of a02 (13:22Z, Bot P2 4248319936 on head `375bae0f`: "past the task's expected duration" had no computable threshold): item 1's last sentence names the trigger: thirty minutes after the TASK, amendment or revise entered the bus history with no bus event from the seat since, INV-10's clock and figure, no override (superseded by amendment 1 of a04: INV-10's idle figure is 20 minutes) (revised once 13:25Z on the Codex confirmation: the first draft counted from the seat's read and allowed an `expected_minutes=` override that could exceed INV-10); nothing else changes. The other open P2, 4248319926 (no `classes:` field in the PR tree), is answered by the orchestrator's `gh pr update-branch`, which brings `main`'s 18 records with the field into the PR tree. Amendment 1 (worker PONG `question`, 12:27Z): the orchestrator-effects row split into three rows (F1), item 5's invariant check qualified to tasks that carry an `invariants` key (F2), item 3's search keyed on the mistake records' `classes:` field after the Bot replayed the old commands against the records (F3: `grep -rl bookkeeping corrections/` 0 files, `grep -rl sources corrections/` 15 files); the worker's head `9b2c02a1` stays and its three threads are answered by this amendment, not by replies. a02 is a01's INV-6 reset (questions 2: the PONG of 12:27:06Z on the Bot's three findings and the PONG of 12:37:00Z on the amended search command, whose `grep -l` on a directory exits 2 under plain grep), written by the review seat under the reset record `.orchestration/acceptance/dotfiles-T128-playbook-rules-a01-design-reset.md`; the worker (`claude-standard-dot-a003`) continues on the same branch and PR #328 from head `9b2c02a1`, and its prepared work (the task copy, item 5, the tests, the fixtures) is kept as it is, the task copy recommitted under the a02 path. Review tier by INV-1 (`kind: docs`): the regime's own rule prose. Each sentence below is owned by the SKILL or AGENTS.md; plan 007 cites them, it does not restate them. The threat table names every `allowed_files` entry plus the non-path controls; `task-consistency-check.py` C1 to C9 pass on this file.
    75	
    76	## What to do (each item is one sentence or one replacement; keep the surrounding text)
    77	
    78	1. Orchestrator Playbook step 6 (SKILL line 162): append the dispatch-evidence sentences (C-12): "Every dispatch (TASK, ACCEPTANCE, PING) is recorded in the current acceptance record under a `dispatch:` key as the bus line with its read marker; a seat is reported as working only from such a line, and after a context compaction the open TASK list is re-derived from a bus read that is refused when it reaches its limit (`bus-read.sh` exits when the history reaches `BUS_READ_LIMIT`; the orchestrator raises the limit and reads again), never from a default-limited one and never from a read whose truncation went unnoticed. A seated worker idle for 20 minutes since its latest bus event for the task while a dispatchable task exists (INV-10's idle figure; its 30 minutes is the first-push deadline) gets a bus read, then a PING; a longer silent wait is never the answer. `scripts/orchestrator/dispatch.sh` writes the line and `scripts/orchestrator/bus-read.sh` performs the read and prints the minutes since each open task's latest event (both on main since a03c1daa, plan 007 T718); the orchestrator applies the 20-minute figure to the minutes the script prints (the script's own silence flag still uses 30 minutes, a recorded residual of the tools lineage)."
    79	2. "Review and integration invariants", after the counters bullet (line 72): a new bullet for the amendment rule (plan 007 Phase 0): "A change to a rule sentence requested of a worker travels as a task amendment (hashed, checked by the task-consistency check C1 to C6 once plan 007 T704 lands it and by hand until then, confirmed by the review seat), never as a PONG answer."
    80	3. Same section, after that bullet: the three-repeat procedure (plan 007 S6): "When a finding class reaches three on one artifact (the record's ledger) or `scripts/regime-counters.sh` prints an S1 candidate, the next acceptance action is the records search for that class, pasted into the record as the line `search: <class> -> <the matching mistake records or none>`, and the matching correction is applied when its mechanism is landed, or landed first when it is pending, mechanism by mechanism, before any dispatch; a class is a slug of `[a-z0-9-]` assigned at disposition time, never text taken from a review title. Once plan 007 T718 lands, `scripts/orchestrator/three-repeat.sh <class>` validates the slug, runs the records search and the CompactionDB search without a shell and prints the line; until then the orchestrator runs them by hand with a validated slug. Once `dotfiles-T128-gate-evidence-a02` lands, the gate refuses the action without the line; until then the orchestrator refuses it by rule. Every `not-applicable` disposition carries `; evidence=<command>` with the output pasted in the record." The `classes:` fields of the mistake records land on `main` through the boundary commit that precedes this dispatch, so the rule is testable from `main`.
    81	4. The threat-table bullet (line 71): after the list of things the PR or the orchestrator controls, add the row unit: "The row unit is one row per `allowed_files` entry, one row per listed control that is not a path (task metadata, workflow and interpreter or environment inputs, in-process effects, new or renamed scripts, metadata separators), carried by the declared test module's row where that is where the control acts, and one row per orchestrator effect from the fixed list (forced removal, merge, update-branch); under a wildcard `allowed_files` entry whose files are executed or applied (scripts, workflows, hooks, settings, the rules seats follow), one row per concrete file the PR changes; a wildcard over test fixtures or other data files keeps one row; C4 of the task-consistency check (plan 007 T704) verifies the path half once it lands, and the task-file review checks it by hand until then." In AGENTS.md line 78's bullet, after "report a missing table or a missing row;", insert: "a row's unit is the SKILL threat-table bullet's (one per `allowed_files` entry, one per non-path control, one per orchestrator effect), so review a missing row at that unit;".
    82	5. The task-file-review bullet (line 69): replace "one invariant check (a `-contract-a01` id maps to its implementing entry)" with "one invariant check (for a task that carries an `invariants` key: the task id maps to its `implementing_tasks` entry, the invariant ids match, and each invariant's sentence equals the design's byte-for-byte, the design read from main (INV-2), checked by hand in the review until a checker lands; a task without the key needs no entry)", following design v20 (plan 006 B0), which removed contract PRs; the token test at `tests/unit/test_agmsg_orchestration_docs.py` line 278 that asserts the old clause becomes the new clause's token in the same commit.
    83	6. Orchestrator Playbook step 10.4 (line 170): the gate command gains `ACCEPTANCE_EVIDENCE=<acceptance record>` beside `PR_FEEDBACK_EVIDENCE` (required in PR mode once `dotfiles-T128-gate-evidence-a02` lands; the record whose ledger and `search:` line the gate reads); any existing token test that asserts that sentence is updated to the new text in the same commit.
    84	7. Tests: one token test per new sentence (items 1 to 6) in the style of `test_counters_run_before_every_acceptance_action`; register Orchestrator Playbook step 6 in `PINNED_SECTIONS` with a new fixture `tests/fixtures/regime/orchestrator-step-6.md`; update `tests/fixtures/regime/invariants.md` and `code-review-orchestration.md` for the changed sections, and list every fixture change in the RESULT (INV-12's declared change).
    85	8. Nothing else changes: not the Worker Playbook, not the counters bullet's text, not the message contract.
    86	
    87	## Validation
    88	
    89	- `uv run --no-project python -m unittest tests/unit/test_agmsg_orchestration_docs.py -v` output in the validation file, with the new tests named and the fixture list.
    90	- `git diff --numstat origin/main...HEAD` in the validation file (INV-2 caps: at most 15 changed files outside `.orchestration/`, 500 added lines outside `tests/`, 1000 under `tests/`).
    91	
    92	## Completion
    93	
    94	The PR is ready for the orchestrator's integration when CI is green, the Bot wait of Worker Playbook step 15 is done, the validation file carries the outputs above, and the RESULT names every unresolved Bot thread with `fixed:<sha>` or a proposed `not-applicable:<reason>; evidence=<command>`. Branch `regime/playbook-rules`, PR #328 (open since a01, continued from the worker's head `fe34f7db`; the PR stays open, and the orchestrator's `gh pr update-branch` has already moved it to `e12872cd`), `kind: docs`. Amendment 1 (2026-10-13): the orchestrator runs the local review (C-32) on the pushed head and returns its findings with the Bot's in a04's one revise round; a P2 finding on a04's final head that round did not fix is `not-applicable: owned by dotfiles-T128-playbook-rules-followup-a01` and is listed in a04's acceptance record under the heading `## Owned by dotfiles-T128-playbook-rules-followup-a01` as an `<id>\t<class>` row (that section, landed on main by the boundary after a04's merge, is the follow-up task's whole scope); no boundary commit runs between the amendment's dispatch and PR #328's merge.
    95	
    96	## Amendment 1 (orchestrator, 2026-10-13 10:18Z)
    97	
    98	The Codex Bot's review 5501887212 of PR #328's update-branch head `7771082f` (the first head after T718's first slice merged as a03c1daa) and the orchestrator's local review of the same head (C-32) found four defects of this task's own sentences, each corrected above against the design on main (`.orchestration/tasks/dotfiles-T128-regime-v3-a01.md`, INV-2 at line 56 and INV-10 at line 64, pasted in the acceptance record): item 1's "thirty minutes" becomes INV-10's 20-minute idle figure applied to the minutes `bus-read.sh` prints (thread 4257278271), and its "complete bus read" becomes the read refused at its limit, as the merged script does (local finding 7771082:1); item 4 adds one row per concrete changed file under a wildcard entry whose files are executed or applied, data wildcards keeping one row (thread 4257278276); item 5's invariant check compares each invariant's sentence byte-for-byte with the design, by hand until a checker lands (thread 4257278283, P1). The token tests of item 7 follow the amended sentences in the same commit; the worker's commits through `2276a365` stay; the Completion clause gains the one revise round, the local review and the owner of residual findings (`dotfiles-T128-playbook-rules-followup-a01`, on main through the boundary that lands this amendment). Nothing else changes: not items 2, 3, 6 and 8, not the threat table, not the premises.
     1	# Report: dotfiles-T128-playbook-rules-a04
     2	
     3	- Seat: `claude-standard-dot-a003` in `.claude/worktrees/worker-c`, branch `regime/playbook-rules`, PR #328. a04 is a03's reset under plan 010 option D (`reset_of: [a01, a02, a03]`).
     4	- Before any edit, the branch was fast-forwarded from the worker's `fe34f7db` to the orchestrator's update-branch head `e12872cd`. `fe34f7db` is an ancestor, so nothing was rebased (validation §1).
     5	- Task file sha256 `e64ee691…` matches the TASK's `task_sha256`. It is copied byte-identical in `ff2e7156` to `.orchestration/dotfiles-T128-playbook-rules-a04/task.md`. The a01, a02 and a03 copies are unchanged since `1083a8c1`, `4486dbdd` and `196d73ca` (§1).
     6	
     7	## Commit `beee078a`: items 1 and 3 as obligation, script and landing condition
     8	
     9	Both sentences were spliced into the SKILL from the task's quoted spans, not retyped, and every quoted span of items 1 to 6 is present verbatim (§3).
    10	
    11	| Item | Now | Test |
    12	|---|---|---|
    13	| 1 (step 6) | the dispatch line "as the bus line with its read marker"; the open TASK list "re-derived from a complete bus read, never from a default-limited one"; "A seat silent for thirty minutes since its latest bus event for the task (INV-10's figure) gets a bus read, then a PING"; once T718 lands, `dispatch.sh` and `bus-read.sh`, until then `history.sh <team> --limit 1000` | `test_dispatches_are_recorded_from_the_bus`: one token per sentence; `assertNotIn` for "expected duration", "the bus line `history.sh <team>` prints" and "no bus event from its seat since" |
    14	| 3 (three-repeat) | the records search pasted as `search: <class> -> <…>`; corrections applied mechanism by mechanism; a class is an `[a-z0-9-]` slug assigned at disposition time, never review-title text; once T718 lands, `three-repeat.sh <class>` runs both searches without a shell; once `gate-evidence-a02` lands, the gate refuses without the line | `test_three_repeats_start_with_a_pasted_correction_search`: one token per sentence; `assertNotIn` adds `memory search <class slug>` (the unquoted interpolation) to the earlier stale forms |
    15	
    16	Items 2, 4, 5, 6, 7 and 8 are unchanged, as the task says.
    17	
    18	## A premise worth knowing: `history.sh <team> --limit 1000`
    19	
    20	Item 1's interim command reads the complete history: 778 rows, against 20 by default, the same count as the positional `history.sh <team> '' 1000` (§2). It does so by accident, though. `history.sh`'s usage is `<team> [agent_id] [limit]`, so `--limit` lands in the agent slot. `storage_history` skips a dash-led agent and then reads `--limit --limit 1000`, taking the second `--limit` as the limit value; a non-numeric limit becomes -1, which means no limit (§2 quotes both scripts). So the sentence's obligation, a complete read, holds, but `1000` is not the limit that applies. I wrote it verbatim, and T718's `bus-read.sh` is meant to replace it. If the orchestrator wants the interim form to be literal, the positional `history.sh <team> '' 1000` reads the same rows by design, and changing it is an amendment.
    21	
    22	## Declared fixture changes (INV-12)
    23	
    24	- `tests/fixtures/regime/orchestrator-step-6.md`: item 1 (`beee078a`).
    25	- `tests/fixtures/regime/invariants.md`: item 3 (`beee078a`).
    26	- `code-review-orchestration.md` was regenerated and is unchanged (§7).
    27	
    28	## Results
    29	
    30	- Docs module 47 OK (§4). `test_pr_feedback.py` OK, ruff clean (§5).
    31	- 20 mutants, 20 failures (§6): 1c and 1e put back a03's item-1 wording, 3d a03's whole bullet, 3f a03's "without the paste".
    32	- Size (§7): 6 files outside `.orchestration/`; 7 added lines outside `tests/`; 113 under `tests/` (caps 500 and 1000).
    33	- Premises (§2): `main` moved only under `.orchestration/` since the merge-base; `scripts/orchestrator/` does not exist on `main`, so T718 has not landed; `regime/gate-evidence` is open.
    34	
    35	## Bot threads from a03's head `fe34f7db`
    36	
    37	| Thread | Disposition |
    38	|---|---|
    39	| 4249303413 (P1, default-limited read) | `fixed:beee078a`: "a complete bus read, never … a default-limited one" |
    40	| 4249303433 (P1, review title into a shell) | `fixed:beee078a`: a class is an `[a-z0-9-]` slug assigned at disposition time; `three-repeat.sh` runs without a shell; the command with `<class slug>` is gone |
    41	| 4249303426 (P2, clock stopped by one early PONG) | `fixed:beee078a`: "since its latest bus event for the task" |
    42	| 4249303398 (P2, partial correction status) | `fixed:beee078a`: "applied when its mechanism is landed, or landed first when it is pending, mechanism by mechanism" |
    43	
    44	The earlier threads stand as the a03 report tables them. 4248319926 is answered by the update-branch already taken (`e12872cd`). The worker resolves no thread.
    45	
    46	## CI and the Codex Bot on the a04 head `2276a365` (main-checkout copy)
    47	
    48	- CI: all 12 check runs on `2276a365` are `completed success`, and the watcher exited 0 (validation §9).
    49	- Bot: no review within 10 minutes of the push, so `@codex review` was posted at 15:59:59Z. Review 5493270947 of `2276a365` arrived at 16:03:26Z with one P1 and no P2. Counts: Bot reviews on PR #328 = 5 (`9b2c02a1`, `375bae0f`, `c4e0bb72`, `fe34f7db`, `2276a365`); worker P0/P1 fix rounds = 0.
    50	
    51	| Thread | Finding | Verified premise (§9) | Proposed handling |
    52	|---|---|---|---|
    53	| 4250028600 | P1, SKILL.md:74 (item 3): the two trigger paths use different class formats. `scripts/regime-counters.sh` prints its S1 candidate as the first three words of a review title, while the rule says a class is an `[a-z0-9-]` slug assigned at disposition time, so "the records search for that class" has no defined input when the counter path fires | `regime-counters.sh:147` prints `S1: candidate class=<title words>`; `tests/unit/test_regime_counters.py:451` expects `class=reject skipped contract` | `open:4250028600`: not fixable here. The fix is either the script (forbidden: edit-scripts; `scripts/regime-counters.sh` is outside `allowed_files`) or the sentence (an amendment). Two options for the orchestrator: (a) make the counter emit, or resolve its candidate to, the ledger's assigned slug (a T718 or regime-counters task); (b) say in the sentence that a counter candidate is mapped to its ledger slug before the search |
    54	
    55	## Not done, or outside scope
    56	
    57	- `tests/unit/test_regime_counters.py` and `test_require_crit_review.py` were not run locally (PyPI is unreachable from the sandbox); neither reads the changed files.
    58	- Understand-Anything hook: did not fire. plan-mode-used: no.
    59	
    60	## CompactionDB
    61	
    62	`memory add` printed `a3ae0494-87a7-437c-b39a-2a08ecfcd170` (§8), with the `history.sh --limit` mechanism above.
    63	
    64	cost: n/a
    65	
    66	## Revise round 1 with amendment 1 (ACCEPTANCE of 13:57:09Z; task file sha256 `c5dbc2c3…`)
    67	
    68	The orchestrator's line lifted the operator's 10:36Z stop and superseded TASK 935. The branch fast-forwarded to the remote head `7771082f`, merged `origin/main` (`4e7a9b3a`) in `87bce51e`, and the task copy now matches the amended file byte for byte (validation §10). `e6602ca1` puts the amended sentences of items 1, 4 and 5 in the SKILL verbatim, as the task file quotes them (§10 checks all three):
    69	
    70	| Thread | Finding | Disposition |
    71	|---|---|---|
    72	| 4257278283 (P1) | the invariant check compared ids only | `fixed:e6602ca1`. Each invariant's sentence equals the design's byte for byte, the design read from main (INV-2), by hand until a checker lands. Test: `test_task_file_review_is_one_round_with_a_fixed_stop_condition` (P4) |
    73	| 4257278271 (P2) | step 6 used thirty minutes as INV-10's figure | `fixed:e6602ca1`. A seated worker idle for 20 minutes (INV-10's idle figure; 30 minutes is the first-push deadline). The orchestrator applies it to the minutes `bus-read.sh` prints. Test: `test_dispatches_are_recorded_from_the_bus` (P2) |
    74	| 4257278276 (P2) | the row unit had no rule for a wildcard entry | `fixed:e6602ca1`. One row per concrete changed file under an executed or applied wildcard entry; a data wildcard keeps one row. Test: `test_threat_table_rows_have_a_fixed_unit` (P3) |
    75	| local review of `7771082f`, finding 1 | "a complete bus read", which the merged script does not do | `fixed:e6602ca1`. The read is refused when it reaches its limit, and the orchestrator raises `BUS_READ_LIMIT` and reads again. Test: `test_dispatches_are_recorded_from_the_bus` (P1) |
    76	
    77	- Declared fixture changes (INV-12): `tests/fixtures/regime/invariants.md` (the task-file-review and threat-table bullets) and `tests/fixtures/regime/orchestrator-step-6.md` (step 6). `test_regime_rule_sections_are_pinned_whole` fails on a changed fixture (P5).
    78	- The `test_dispatches_are_recorded_from_the_bus` stale list also refuses `complete bus read` and `silent for thirty minutes`.
    79	- Results (§10): 47 docs tests OK; Prettier and ruff clean; 5 mutants, 5 failures. Size: 6 files outside `.orchestration/`; added lines outside and under `tests/`: 7 and 127.
    80	- The orchestrator's line says the Bot reviews on PR open only now, so there is no Bot wait; the pushed head's CI is in the RESULT and in the main-checkout copy.
    81	
    82	## CI on the revise head `65a3d71b` (main-checkout copy only)
    83	
    84	- Pushed at 2026-10-13T14:04:00Z. CI: all 13 checks pass (validation §11). There is no Bot wait, per the orchestrator's line of 13:57:09Z.
     1	---
     2	task_id: dotfiles-T128-playbook-rules-a04
     3	seat: claude-standard-dot-a003
     4	permission_gated_commands: 11
     5	---
     6	
     7	# Sandbox record: dotfiles-T128-playbook-rules-a04
     8	
     9	- Period: from the AGMSG-TASK (2026-10-12T15:40:52Z) to the RESULT. These ran inside the sandbox: the fetch of the branch over public HTTPS and the fast-forward to `e12872cd`, the `history.sh` premise runs, the edits, fixture generation, the tests, ruff, the verbatim check, the mutation proofs, and the commits.
    10	
    11	`permission_gated_commands` counts every Bash call made with `dangerouslyDisableSandbox`, one per call. This is the final count; the seven calls of round 0 ran as tabled, and #8 to #11 below are revise round 1's. The PR is already ready, so there is no `gh pr ready`.
    12	
    13	| # | Command | Step 4 case |
    14	|--:|---|---|
    15	| 1 | main-checkout `memory add` | main-checkout `memory add` |
    16	| 2 | the HTTPS push | `git push` |
    17	| 3 | `gh pr checks 328 --watch` (background, exit status joined) | `gh` |
    18	| 4 | Bot wait from the push | `gh` |
    19	| 5 | reading the Bot review and the check runs of the final head | `gh` |
    20	| 6 | the masked copy of the five evidence files to the main checkout | artifact copy with the repository masker |
    21	| 7 | `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T128-playbook-rules-a04 …` | `agmsg-dispatch` |
    22	| 8 | the revise round's HTTPS push | `git push` |
    23	| 9 | `gh pr checks 328 --watch` on the revise head | `gh` |
    24	| 10 | the masked copy of the evidence files to the main checkout | artifact copy with the repository masker |
    25	| 11 | `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T128-playbook-rules-a04 revise=1 …` | `agmsg-dispatch` |
    26	
    27	Revise round 1 (amendment 1): this main-checkout copy gives the final count, eleven calls, all run; there is no Bot wait (the orchestrator's line of 13:57:09Z).
nl: .orchestration/validation/dotfiles-T128-playbook-rules-a04-local-review-65a3d71.md: No such file or directory

**Managing output limits**
exec
/bin/zsh -lc "nl -ba .orchestration/tasks/dotfiles-T128-regime-v3-a01.md | sed -n '1,80p'; nl -ba .orchestration/reports/dotfiles-T128-playbook-rules-a04.md | sed -n '66,110p'; nl -ba .orchestration/sandboxes/dotfiles-T128-playbook-rules-a04.md; cat .orchestration/validation/dotfiles-T128-playbook-rules-a04-local-review-65a3d71.md" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 exited 1 in 107ms:
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
    66	## Revise round 1 with amendment 1 (ACCEPTANCE of 13:57:09Z; task file sha256 `c5dbc2c3…`)
    67	
    68	The orchestrator's line lifted the operator's 10:36Z stop and superseded TASK 935. The branch fast-forwarded to the remote head `7771082f`, merged `origin/main` (`4e7a9b3a`) in `87bce51e`, and the task copy now matches the amended file byte for byte (validation §10). `e6602ca1` puts the amended sentences of items 1, 4 and 5 in the SKILL verbatim, as the task file quotes them (§10 checks all three):
    69	
    70	| Thread | Finding | Disposition |
    71	|---|---|---|
    72	| 4257278283 (P1) | the invariant check compared ids only | `fixed:e6602ca1`. Each invariant's sentence equals the design's byte for byte, the design read from main (INV-2), by hand until a checker lands. Test: `test_task_file_review_is_one_round_with_a_fixed_stop_condition` (P4) |
    73	| 4257278271 (P2) | step 6 used thirty minutes as INV-10's figure | `fixed:e6602ca1`. A seated worker idle for 20 minutes (INV-10's idle figure; 30 minutes is the first-push deadline). The orchestrator applies it to the minutes `bus-read.sh` prints. Test: `test_dispatches_are_recorded_from_the_bus` (P2) |
    74	| 4257278276 (P2) | the row unit had no rule for a wildcard entry | `fixed:e6602ca1`. One row per concrete changed file under an executed or applied wildcard entry; a data wildcard keeps one row. Test: `test_threat_table_rows_have_a_fixed_unit` (P3) |
    75	| local review of `7771082f`, finding 1 | "a complete bus read", which the merged script does not do | `fixed:e6602ca1`. The read is refused when it reaches its limit, and the orchestrator raises `BUS_READ_LIMIT` and reads again. Test: `test_dispatches_are_recorded_from_the_bus` (P1) |
    76	
    77	- Declared fixture changes (INV-12): `tests/fixtures/regime/invariants.md` (the task-file-review and threat-table bullets) and `tests/fixtures/regime/orchestrator-step-6.md` (step 6). `test_regime_rule_sections_are_pinned_whole` fails on a changed fixture (P5).
    78	- The `test_dispatches_are_recorded_from_the_bus` stale list also refuses `complete bus read` and `silent for thirty minutes`.
    79	- Results (§10): 47 docs tests OK; Prettier and ruff clean; 5 mutants, 5 failures. Size: 6 files outside `.orchestration/`; added lines outside and under `tests/`: 7 and 127.
    80	- The orchestrator's line says the Bot reviews on PR open only now, so there is no Bot wait; the pushed head's CI is in the RESULT and in the main-checkout copy.
    81	
    82	## CI on the revise head `65a3d71b` (main-checkout copy only)
    83	
    84	- Pushed at 2026-10-13T14:04:00Z. CI: all 13 checks pass (validation §11). There is no Bot wait, per the orchestrator's line of 13:57:09Z.
     1	---
     2	task_id: dotfiles-T128-playbook-rules-a04
     3	seat: claude-standard-dot-a003
     4	permission_gated_commands: 11
     5	---
     6	
     7	# Sandbox record: dotfiles-T128-playbook-rules-a04
     8	
     9	- Period: from the AGMSG-TASK (2026-10-12T15:40:52Z) to the RESULT. These ran inside the sandbox: the fetch of the branch over public HTTPS and the fast-forward to `e12872cd`, the `history.sh` premise runs, the edits, fixture generation, the tests, ruff, the verbatim check, the mutation proofs, and the commits.
    10	
    11	`permission_gated_commands` counts every Bash call made with `dangerouslyDisableSandbox`, one per call. This is the final count; the seven calls of round 0 ran as tabled, and #8 to #11 below are revise round 1's. The PR is already ready, so there is no `gh pr ready`.
    12	
    13	| # | Command | Step 4 case |
    14	|--:|---|---|
    15	| 1 | main-checkout `memory add` | main-checkout `memory add` |
    16	| 2 | the HTTPS push | `git push` |
    17	| 3 | `gh pr checks 328 --watch` (background, exit status joined) | `gh` |
    18	| 4 | Bot wait from the push | `gh` |
    19	| 5 | reading the Bot review and the check runs of the final head | `gh` |
    20	| 6 | the masked copy of the five evidence files to the main checkout | artifact copy with the repository masker |
    21	| 7 | `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T128-playbook-rules-a04 …` | `agmsg-dispatch` |
    22	| 8 | the revise round's HTTPS push | `git push` |
    23	| 9 | `gh pr checks 328 --watch` on the revise head | `gh` |
    24	| 10 | the masked copy of the evidence files to the main checkout | artifact copy with the repository masker |
    25	| 11 | `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T128-playbook-rules-a04 revise=1 …` | `agmsg-dispatch` |
    26	
    27	Revise round 1 (amendment 1): this main-checkout copy gives the final count, eleven calls, all run; there is no Bot wait (the orchestrator's line of 13:57:09Z).
cat: .orchestration/validation/dotfiles-T128-playbook-rules-a04-local-review-65a3d71.md: No such file or directory

**Checking available tools**
codex
4つの修正文は、設計の「不変条件の文面一致」「20分の idle 上限」と、既存スクリプトの読取り上限に沿っています。争点の P1 については、`dispatch.sh` が不足した記録を拒否する箇所と、playbook が記録の作成時点を定めているかを照合中です。GitHub API への接続は失敗したため、保存済みの CI・feedback 証跡を確認し、別の読取り経路も試します。

exec
/bin/zsh -lc "python3 - <<'PY'
import json, pathlib
p=pathlib.Path('.ua/knowledge-graph.json')
if p.exists():
 d=json.loads(p.read_text()); print('graph nodes',len(d.get('nodes',[])))
 for n in d.get('nodes',[]):
  if any(t in str(n.get('filePath','')) for t in ('orchestrator/dispatch','bus-read','three-repeat','agmsg-orchestration','require-crit-review')): print(n.get('filePath'), n.get('summary'))
p=pathlib.Path('.ua/meta.json'); print(p.read_text() if p.exists() else 'no meta')
p=pathlib.Path('.orchestration/validation/dotfiles-T128-playbook-rules-a04-pr-feedback.json'); d=json.loads(p.read_text());print('Feedback keys:',list(d)); print('metadata:',{k:v for k,v in d.items() if k"'!='"'items'});print('items:',len(d.get('items',[])))
PY" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 exited 1 in 31ms:
zsh:1: can't create temp file for here document: operation not permitted

**Handling shell quoting workaround**
exec
/bin/zsh -lc "python3 -c 'import json,pathlib
p=pathlib.Path('\\''.ua/knowledge-graph.json'\\'')
if p.exists():
 d=json.loads(p.read_text());print('\\''graph nodes'\\'',len(d.get('\\''nodes'\\'',[])))
 for n in d.get('\\''nodes'\\'',[]):
  if any(t in str(n.get('\\''filePath'\\'','\\'''\\'')) for t in ('\\''orchestrator/dispatch'\\'','\\''bus-read'\\'','\\''three-repeat'\\'','\\''agmsg-orchestration'\\'','\\''require-crit-review'\\'')):print(n.get('\\''filePath'\\''),n.get('\\''summary'\\''))
p=pathlib.Path('\\''.ua/meta.json'\\'');print(p.read_text() if p.exists() else '\\''no meta'\\'')
p=pathlib.Path('\\''.orchestration/validation/dotfiles-T128-playbook-rules-a04-pr-feedback.json'\\'');d=json.loads(p.read_text());print('\\''Feedback keys:'\\'',list(d)); print('\\''metadata:'\\'',{k:v for k,v in d.items() if k"'!='"'\\''items'\\''});print('\\''items:'\\'',len(d.get('\\''items'\\'',[])))'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 107ms:
graph nodes 984
home/dot_config/claude/rules/agmsg-orchestration.md Global Claude rule defining the agmsg orchestration regime: when it activates, delegation of repository mutations to resident Codex workers, herdr-agents worker seating, independent Codex audits, main-push guarding, and session-boundary duties.
home/dot_agents/skills/agmsg-orchestration/SKILL.md Agent skill defining the agmsg orchestration protocol between a Claude orchestrator and Codex workers: architecture, regime activation, parallel workers, identity/delivery, Message Contract v1, .orchestration layout, orchestrator/worker playbooks, worklogs and pitfalls.
home/dot_claude/rules/symlink_agmsg-orchestration.md.tmpl chezmoi symlink template that links ~/.claude/rules/agmsg-orchestration.md to the shared rule at dot_config/claude/rules/agmsg-orchestration.md in the source directory.
home/dot_claude/skills/agmsg-orchestration/symlink_SKILL.md.tmpl Chezmoi symlink template that exposes the shared agmsg-orchestration skill definition (SKILL.md) from dot_agents/skills to ~/.claude/skills/agmsg-orchestration/SKILL.md, keeping one canonical copy for Claude Code and Codex.
scripts/require-crit-review.py Integration guard that requires native agent or Crit review evidence for meaningful diffs and, for PR integration, re-collects GitHub feedback from the authenticated base's pr-feedback.py and requires a root-cause disposition for every item.
scripts/require-crit-review.py Skips worklogs and the PR feedback evidence file itself when sizing a diff.
scripts/require-crit-review.py Rejects PR feedback evidence outside .orchestration/validation/ or without the -pr-feedback.json suffix.
scripts/require-crit-review.py Lists unstaged, staged, untracked, and optionally base...HEAD changed paths, excluding ignored files.
scripts/require-crit-review.py Sums added and removed line counts across working, staged, and base...HEAD diffs via git numstat.
scripts/require-crit-review.py Classifies a path as high risk (policy/config file, agent lifecycle prefix, or risky token) and returns the reason.
scripts/require-crit-review.py Aggregates reasons that make review mandatory: high-risk paths, many files, or large line counts.
scripts/require-crit-review.py Validates the review receipt file and its required fields, dispatching to agent or Crit evidence checks.
scripts/require-crit-review.py Checks agent reviewer receipts require the crit-data surface, an allowed outcome, and valid Crit JSON evidence.
scripts/require-crit-review.py Validates repo-local Crit JSON evidence: inside the repo, a list of well-formed resolved records with at least one review/line/file scope.
scripts/require-crit-review.py Checks the filled pr-feedback JSON: correct head, valid fixed:<commit> or not-applicable:<reason> dispositions, failure reasons long enough, and fixed commits in range.
scripts/require-crit-review.py Binds the evidence's base to the PR's GitHub base and local repository before running any collector, rejecting stale or rewritten bases.
scripts/require-crit-review.py Re-runs the GitHub base's pr-feedback.py and requires every currently collected item to be present in the evidence.
scripts/require-crit-review.py CLI entry that decides whether review is required, validates base, review receipts, and PR feedback evidence, and exits non-zero on any error.
{
  "lastAnalyzedAt": "2026-10-02T14:12:51Z",
  "gitCommitHash": "940a3a2b07adfd14140a0acff96784ef53a0a509",
  "version": "1.0.0",
  "analyzedFiles": 368
}

Feedback keys: ['repo', 'pr', 'head_sha', 'base_ref', 'base_sha', 'generated_at', 'checks', 'items']
metadata: {'repo': 'mryfmo/dotfiles', 'pr': 328, 'head_sha': '65a3d71bf4e496252bf1ff51894974130c96cd43', 'base_ref': 'main', 'base_sha': '4e7a9b3ae0a1a80f2c7664ea54e3244224a7a672', 'generated_at': '2026-10-13T14:32:32+00:00', 'checks': [{'name': 'GitGuardian Security Checks', 'conclusion': 'success', 'url': 'https://github.com/mryfmo/dotfiles/runs/115340387974'}, {'name': 'validate', 'conclusion': 'success', 'url': 'https://github.com/mryfmo/dotfiles/actions/runs/38410198913/job/115340184055'}, {'name': 'public-bootstrap (ubuntu-24.04, client)', 'conclusion': 'success', 'url': 'https://github.com/mryfmo/dotfiles/actions/runs/38410198303/job/115340182144'}, {'name': 'private-bootstrap (macos-14, client)', 'conclusion': 'success', 'url': 'https://github.com/mryfmo/dotfiles/actions/runs/38410198303/job/115340181995'}, {'name': 'private-bootstrap (ubuntu-24.04, server)', 'conclusion': 'success', 'url': 'https://github.com/mryfmo/dotfiles/actions/runs/38410198303/job/115340181888'}, {'name': 'private-bootstrap (ubuntu-24.04, client)', 'conclusion': 'success', 'url': 'https://github.com/mryfmo/dotfiles/actions/runs/38410198303/job/115340181810'}, {'name': 'public-bootstrap (macos-14, client)', 'conclusion': 'success', 'url': 'https://github.com/mryfmo/dotfiles/actions/runs/38410198303/job/115340181793'}, {'name': 'public-bootstrap (ubuntu-24.04, server)', 'conclusion': 'success', 'url': 'https://github.com/mryfmo/dotfiles/actions/runs/38410198303/job/115340181466'}, {'name': 'test (ubuntu-24.04, server)', 'conclusion': 'success', 'url': 'https://github.com/mryfmo/dotfiles/actions/runs/38410197390/job/115340179833'}, {'name': 'test (macos-14, client)', 'conclusion': 'success', 'url': 'https://github.com/mryfmo/dotfiles/actions/runs/38410197390/job/115340179776'}, {'name': 'test (ubuntu-26.04, client)', 'conclusion': 'success', 'url': 'https://github.com/mryfmo/dotfiles/actions/runs/38410197390/job/115340179532'}, {'name': 'test (ubuntu-24.04, client)', 'conclusion': 'success', 'url': 'https://github.com/mryfmo/dotfiles/actions/runs/38410197390/job/115340179442'}]}
items: 31

mcp: codex_apps/github.fetch_commit_workflow_runs started
mcp: codex_apps/github.list_pull_request_review_threads started
mcp: codex_apps/github.get_pr_info started
mcp: codex_apps/github.fetch_commit_workflow_runs (completed)
mcp: codex_apps/github.list_pull_request_review_threads (completed)
mcp: codex_apps/github.get_pr_info (completed)
**Evaluating token budget**
exec
/bin/zsh -lc 'nl -ba scripts/orchestrator/dispatch.sh; nl -ba scripts/orchestrator/bus-read.sh; nl -ba scripts/orchestrator/three-repeat.sh' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc "nl -ba .orchestration/validation/dotfiles-T128-playbook-rules-a04.md | sed -n '165,345p'; git show 65a3d71bf4e496252bf1ff51894974130c96cd43:.orchestration/dotfiles-T128-playbook-rules-a04/revise.yaml; git diff --name-only 940a3a2b07adfd14140a0acff96784ef53a0a509 HEAD -- scripts home | head -12" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 86ms:
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
    14	#   `task_file=` and `task_sha256=`. A relative path is read from the root of
    15	#   the checkout this script lives in (`git rev-parse --show-toplevel` there),
    16	#   never from the caller's directory. A missing field or file, a malformed value
    17	#   or a mismatch exits 1 naming the field, and nothing is sent. Otherwise the
    18	#   line goes to `agmsg-dispatch` as one argument, byte for byte.
    19	#   With an acceptance record, the record is checked before the send and, once
    20	#   the line is on the bus, `<the line> read_at=<read|unread>` is appended to
    21	#   the `dispatch` list of
    22	#   the record's JSON block, the object between its first two `---` lines. The
    23	#   block is read and written with Python's standard json (malformed JSON, a
    24	#   duplicate key, NaN or Infinity, a block that is not an object or a
    25	#   `dispatch` that is not a list is refused; `sort_keys`, `indent=2`); the key
    26	#   is created when absent, and a record without a block gets a block holding
    27	#   only `dispatch`. The prose after the block is kept byte for byte, and the
    28	#   record is replaced atomically (a temporary file in its directory, fsync,
    29	#   rename). A record that is not an existing regular file writable in a
    30	#   writable directory, or whose `task` is not the line's `task_id`, is refused
    31	#   before the send, and nothing is sent.
    32	#   Only a bus row this send created is recorded: the rows matching the line,
    33	#   sender and recipient are counted before and after the send, and a send that
    34	#   added none leaves the record unchanged and exits 1. The read state is the
    35	#   marker the team-wide `history.sh <team> "" 100000` prints for the new row
    36	#   (`●` unread, `○` read): agmsg's scripts expose no read_at time, this script
    37	#   never reads the message database, and it never passes an agent to
    38	#   history.sh, whose agent argument renames the caller's pane after it.
    39	# @arg $1 string agmsg team.
    40	# @arg $2 string Sender identity.
    41	# @arg $3 string Recipient identity.
    42	# @arg $4 string Recipient pane id (for example `w5:pA`).
    43	# @arg $5 path File holding the line.
    44	# @arg $6 path Optional acceptance record (`.orchestration/acceptance/<task>.md`), relative to the current directory.
    45	# @env AGMSG_SCRIPTS The agmsg scripts directory (default `$HOME/.agents/skills/agmsg/scripts`).
    46	# @exitcode 0 Sent, and recorded when a record was given (agmsg-dispatch's own status otherwise).
    47	# @exitcode 1 A field check failed, the record is malformed, or the sent line was not recorded.
    48	# @exitcode 2 Usage error, or the file is not one AGMSG-TASK, AGMSG-ACCEPTANCE or AGMSG-PING v1 line.
    49	# @example
    50	#   scripts/orchestrator/dispatch.sh dotfiles-conformance claude-deep-dot claude-standard-dot-a003 w5:pA \
    51	#     "$TMPDIR/task-line.txt" .orchestration/acceptance/dotfiles-T128-orchestrator-tools-a01.md
    52	set -euo pipefail
    53	
    54	usage() {
    55	    echo "usage: dispatch.sh <team> <from> <to> <pane> <line-file> [<acceptance-record>]" >&2
    56	    exit 2
    57	}
    58	(($# == 5 || $# == 6)) || usage
    59	team=$1 from=$2 to=$3 pane=$4 file=$5 record=${6:-}
    60	[[ -f ${file} ]] || usage
    61	# Thread 4256541716: command substitution drops a NUL byte, so the line sent would not be the file's.
    62	if (($(tr -d '\0' < "${file}" | wc -c) != $(wc -c < "${file}"))); then
    63	    echo "dispatch: ${file} holds a NUL byte" >&2
    64	    exit 2
    65	fi
    66	# The sentinel keeps every trailing newline, which $( ) alone would drop (thread 4254107304).
    67	line="$(cat -- "${file}" && printf x)" && line=${line%x} && line=${line%$'\n'}
    68	[[ ${line} != *$'\n'* ]] || {
    69	    echo "dispatch: ${file} holds more than one line" >&2
    70	    exit 2
    71	}
    72	[[ ${line} =~ ^AGMSG-(TASK|ACCEPTANCE|PING)\ v1\  ]] || {
    73	    echo "dispatch: not an AGMSG-TASK, AGMSG-ACCEPTANCE or AGMSG-PING v1 line" >&2
    74	    exit 2
    75	}
    76	root="$(git -C "$(dirname -- "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
    77	
    78	read -ra tokens <<< "${line}"
    79	# @description Print the value of the first `<key>=` token, or fail.
    80	# @arg $1 string Key.
    81	value_of() {
    82	    local t
    83	    for t in "${tokens[@]}"; do
    84	        [[ ${t} == "$1="* ]] && printf '%s' "${t#*=}" && return 0
    85	    done
    86	    return 1
    87	}
    88	# @description Print how many tokens carry `<key>=`.
    89	# @arg $1 string Key.
    90	count_of() {
    91	    local t n=0
    92	    for t in "${tokens[@]}"; do
    93	        [[ ${t} == "$1="* ]] && n=$((n + 1))
    94	    done
    95	    printf '%s' "${n}"
    96	}
    97	# Thread 4254893065: every message names exactly one task, before any hash or record work.
    98	if (($(count_of task_id) != 1)) || [[ -z "$(value_of task_id)" ]]; then
    99	    echo "dispatch: the line needs exactly one non-empty task_id=" >&2
   100	    exit 1
   101	fi
   102	# Thread 4254163604: a TASK whose file is not hash-bound is never sent.
   103	if [[ ${line} == "AGMSG-TASK "* ]]; then
   104	    for field in task_file task_sha256; do
   105	        value_of "${field}" > /dev/null || {
   106	            echo "dispatch: an AGMSG-TASK line needs ${field}=" >&2
   107	            exit 1
   108	        }
   109	    done
   110	fi
   111	for t in "${tokens[@]}"; do
   112	    # Thread 4254771302: any name before _sha256=, digits included (a02_expected_sha256=).
   113	    [[ ${t} =~ ^([^=]+)_sha256=(.*)$ ]] || continue
   114	    name=${BASH_REMATCH[1]} want=${BASH_REMATCH[2]}
   115	    field="${name}_sha256"
   116	    [[ ${want} =~ ^[0-9a-f]{64}$ ]] || {
   117	        echo "dispatch: ${field} is not 64 lowercase hex digits" >&2
   118	        exit 1
   119	    }
   120	    # Thread 4256541725: a previous_<name>_sha256= reference names no file here (a02 item 4's grammar row).
   121	    if [[ ${name} == previous_* ]]; then
   122	        continue
   123	    fi
   124	    # Thread 4254494989: a repeated key leaves a second, unhashed value in the line.
   125	    for key in "${field}" "${name}_file" "${name}"; do
   126	        (($(count_of "${key}") <= 1)) || {
   127	            echo "dispatch: ${field}: ${key}= appears more than once" >&2
   128	            exit 1
   129	        }
   130	    done
   131	    if value_of "${name}_file" > /dev/null && value_of "${name}" > /dev/null; then
   132	        echo "dispatch: ${field}: both ${name}_file= and ${name}= name a file" >&2
   133	        exit 1
   134	    fi
   135	    path="$(value_of "${name}_file" || value_of "${name}")" || {
   136	        echo "dispatch: ${field} has no ${name}_file= or ${name}= field naming its file" >&2
   137	        exit 1
   138	    }
   139	    [[ ${path} == /* ]] || path="${root}/${path}"
   140	    [[ -f ${path} ]] || {
   141	        echo "dispatch: ${field}: ${path} does not exist" >&2
   142	        exit 1
   143	    }
   144	    got="$(shasum -a 256 "${path}")" && got=${got%% *}
   145	    [[ ${got} == "${want}" ]] || {
   146	        echo "dispatch: ${field} mismatch: the line has ${want}, ${path} hashes to ${got}" >&2
   147	        exit 1
   148	    }
   149	done
   150	[[ -n ${record} ]] || exec agmsg-dispatch "${team}" "${from}" "${to}" "${pane}" "${line}"
   151	
   152	# Modes: `check` parses the record; `append` finds the sent line in history.sh's
   153	# output on stdin, takes its read marker (● unread, ○ read) and appends it.
   154	read -r -d '' recorder << 'PY' || true
   155	import json, os, re, shutil, sys, tempfile
   156	from pathlib import Path
   157	
   158	mode, path, line, sender, to, before = sys.argv[1:7]
   159	record = Path(path)
   160	
   161	def refuse(pairs):
   162	    keys = [k for k, _ in pairs]
   163	    dup = next((k for k in keys if keys.count(k) > 1), None)
   164	    if dup is not None:
   165	        sys.exit(f"dispatch: {path}: duplicate key {dup}")
   166	    return dict(pairs)
   167	
   168	def constant(name):
   169	    sys.exit(f"dispatch: {path}: non-finite number {name}")
   170	
   171	text = record.read_text()
   172	block, rest = {}, text
   173	if text.startswith("---\n"):
   174	    end = text.find("\n---\n", 3)
   175	    if end < 0:
   176	        sys.exit(f"dispatch: {path}: the block between the first two --- lines is not closed")
   177	    try:
   178	        block = json.loads(text[4:end], object_pairs_hook=refuse, parse_constant=constant)
   179	    except json.JSONDecodeError as e:
   180	        sys.exit(f"dispatch: {path}: the block is not valid JSON: {e}")
   181	    rest = text[end + 5:]
   182	    if not isinstance(block, dict):
   183	        sys.exit(f"dispatch: {path}: the block is not a JSON object")
   184	entries = block.setdefault("dispatch", [])
   185	if not isinstance(entries, list):
   186	    sys.exit(f"dispatch: {path}: dispatch is not a list")
   187	# Thread 4254844587: another task's record never takes this task's dispatch.
   188	task = next((t[len("task_id="):] for t in line.split(" ") if t.startswith("task_id=")), None)
   189	if task is not None and "task" in block and block["task"] != task:
   190	    sys.exit(f"dispatch: {path} is the record of task {block['task']}, the line is task {task}")
   191	row = re.compile(r"^\s*(\S+)\s+\[[^\]]+\]\s+(\S+)\s+→\s+(\S+):\s(.*)$")
   192	marks = [m.group(1) for m in map(row.match, sys.stdin.read().splitlines())
   193	         if m and (m.group(2), m.group(3), m.group(4)) == (sender, to, line)]
   194	if mode == "check":
   195	    print(len(marks))
   196	    sys.exit(0)
   197	# Thread 4254399807: an older identical row is not this send.
   198	if len(marks) <= int(before):
   199	    sys.exit(f"dispatch: this send added no bus row; {path} is unchanged")
   200	entries.append(f"{line} read_at={'read' if marks[-1] == '○' else 'unread'}")
   201	body = json.dumps(block, sort_keys=True, indent=2, ensure_ascii=False)
   202	# Thread 4254844595: the line is already sent, so the record is replaced whole or not at all.
   203	fd, tmp = tempfile.mkstemp(dir=record.parent, prefix=f".{record.name}.")
   204	try:
   205	    with os.fdopen(fd, "w") as f:
   206	        f.write(f"---\n{body}\n---\n{rest}")
   207	        f.flush()
   208	        os.fsync(f.fileno())
   209	    shutil.copymode(record, tmp)
   210	    os.replace(tmp, record)
   211	except BaseException:
   212	    Path(tmp).unlink(missing_ok=True)
   213	    raise
   214	PY
   215	[[ ${record} == /* ]] || record="${PWD}/${record}"
   216	# The local review of 0d199475 (C-32): a record mkstemp cannot replace would fail only after the send.
   217	if [[ ! -f ${record} || ! -w ${record} || ! -w "$(dirname -- "${record}")" ]]; then
   218	    echo "dispatch: the record ${record} cannot be written" >&2
   219	    exit 1
   220	fi
   221	# Team-wide: history.sh renames the calling pane after an agent argument (thread 4254399805).
   222	bus() { "${AGMSG_SCRIPTS:-${HOME}/.agents/skills/agmsg/scripts}/history.sh" "${team}" "" 100000; }
   223	before="$(bus | python3 -I -c "${recorder}" check "${record}" "${line}" "${from}" "${to}" 0)"
   224	rc=0
   225	agmsg-dispatch "${team}" "${from}" "${to}" "${pane}" "${line}" || rc=$?
   226	bus | python3 -I -c "${recorder}" append "${record}" "${line}" "${from}" "${to}" "${before}"
   227	exit "${rc}"
     1	#!/usr/bin/env bash
     2	# @file bus-read.sh
     3	# @brief Read the whole agmsg team history and print every open task with its minutes of silence.
     4	# @description
     5	#   Plan 007 T718 (C-23). Reads the history through agmsg's `history.sh <team>
     6	#   "" <limit>` (its documented positional form; never the database file) with
     7	#   a limit far above the team's size, and refuses a read whose rows reach the
     8	#   limit, so a truncated view is never taken for the whole bus. The open rule
     9	#   is the stop gate's worker-seat branch (`scripts/agent-stop-gate.sh`; threads
    10	#   4255494133, 4255494139): a task's latest opener, its latest AGMSG-TASK (X
    11	#   to Y) or a later AGMSG-ACCEPTANCE `status=revise` between the same X and Y
    12	#   (a revise between other endpoints opens nothing: the orchestrator's local
    13	#   review of 5b99a744), keeps it open until a later AGMSG-RESULT or AGMSG-PONG
    14	#   `status=blocked` from Y to X, or a later AGMSG-ACCEPTANCE from X to Y with
    15	#   any other status or none; a row between other endpoints neither opens nor
    16	#   closes it. A row counts only in the form `<marker> [<at>] <from> → <to>:
    17	#   <body>`, with the marker `●` or `○` (thread 4256541723), an `<at>` jq's
    18	#   `fromdateiso8601` parses and a body of AGMSG-TASK, -ACCEPTANCE, -RESULT or
    19	#   -PONG, then `v1`, exactly one non-empty `task_id=` and at most one
    20	#   `status=`; any other non-empty line is skipped and counted, never an exit.
    21	#   For each open task it prints the seat the opener went to, the time of the
    22	#   task's latest counted row, the whole minutes since then, and `silent=yes`
    23	#   at thirty minutes or more (INV-10's figure), else `silent=no`; `open: none`
    24	#   when no task (or not the named one) is open; then `skipped=<n>`.
    25	# @arg $1 string agmsg team.
    26	# @arg $2 string Optional task id: report only that task.
    27	# @env AGMSG_SCRIPTS The agmsg scripts directory (default `$HOME/.agents/skills/agmsg/scripts`).
    28	# @env BUS_READ_LIMIT The row limit of the read (default 100000).
    29	# @exitcode 0 Read and reported.
    30	# @exitcode 1 The history is unreadable, or the read reached the limit.
    31	# @exitcode 2 Usage error.
    32	# @example
    33	#   scripts/orchestrator/bus-read.sh dotfiles-conformance dotfiles-T128-orchestrator-tools-a01
    34	set -euo pipefail
    35	
    36	(($# == 1 || $# == 2)) || {
    37	    echo "usage: bus-read.sh <team> [<task id>]" >&2
    38	    exit 2
    39	}
    40	team=$1 only=${2:-}
    41	limit=${BUS_READ_LIMIT:-100000}
    42	[[ ${limit} =~ ^[1-9][0-9]*$ ]] || {
    43	    echo "bus-read: BUS_READ_LIMIT must be a positive integer" >&2
    44	    exit 2
    45	}
    46	history="$("${AGMSG_SCRIPTS:-${HOME}/.agents/skills/agmsg/scripts}/history.sh" "${team}" "" "${limit}")" || {
    47	    echo "bus-read: the history of ${team} is unreadable" >&2
    48	    exit 1
    49	}
    50	report="$(jq -nrR --arg only "${only}" --argjson limit "${limit}" '
    51	  def count($k): [.toks[] | select(startswith($k + "="))] | length;
    52	  def tok($k): [.toks[] | select(startswith($k + "="))][0] // null | if . then .[($k | length) + 1:] else null end;
    53	  [inputs | select(. != "")] as $lines
    54	  | [$lines[] | capture("^\\s*[●○]\\s+\\[(?<at>[^\\]]+)\\]\\s+(?<from>\\S+)\\s+→\\s+(?<to>\\S+):\\s(?<body>.*)$")] as $all
    55	  | if ($all | length) >= $limit then error("bus-read: the read reached its limit of \($limit) rows; raise BUS_READ_LIMIT") else . end
    56	  | [$all | to_entries[] | .value + {i: .key} | .toks = (.body | split(" ")) | .kind = .toks[0]
    57	      | select((.kind | IN("AGMSG-TASK", "AGMSG-ACCEPTANCE", "AGMSG-RESULT", "AGMSG-PONG")) and .toks[1] == "v1"
    58	          and count("task_id") == 1 and tok("task_id") != "" and count("status") <= 1
    59	          and (.at | try fromdateiso8601 catch null) != null)
    60	      | .task = tok("task_id") | .status = tok("status")] as $rows
    61	  | [$rows | group_by(.task)[]
    62	      | (map(select(.kind == "AGMSG-TASK")) | max_by(.i)) as $t
    63	      | select($t != null and ($only == "" or $t.task == $only))
    64	      | ([$t] + map(select(.kind == "AGMSG-ACCEPTANCE" and .status == "revise" and .i > $t.i
    65	          and .from == $t.from and .to == $t.to)) | max_by(.i)) as $o
    66	      | select(any(.[]; .i > $o.i and (
    67	          (.from == $o.to and .to == $o.from and (.kind == "AGMSG-RESULT" or (.kind == "AGMSG-PONG" and .status == "blocked")))
    68	          or (.from == $o.from and .to == $o.to and .kind == "AGMSG-ACCEPTANCE" and .status != "revise"))) | not)
    69	      | max_by(.i).at as $last | ((now - ($last | fromdateiso8601)) / 60 | floor) as $min
    70	      | "open: task=\($o.task) seat=\($o.to) last_event=\($last) minutes=\($min) silent=\(if $min >= 30 then "yes" else "no" end)"]
    71	  | (if length == 0 then "open: none" else .[] end), "skipped=\(($lines | length) - ($rows | length))"' <<< "${history}")" || exit 1
    72	printf '%s\n' "${report}"
     1	#!/usr/bin/env bash
     2	# @file three-repeat.sh
     3	# @brief Run the three-repeat records search for one finding class and print the record's search line.
     4	# @description
     5	#   Plan 007 T718 (C-23). The class must be a slug of `[a-z0-9-]` (exit 2
     6	#   otherwise), so no review text reaches a command. The records search is the
     7	#   gate's own match: the files under `.orchestration/learning/mistakes/` with a
     8	#   line that begins with `classes:` and contains the class (`grep -rl
     9	#   '^classes:.*<class>'`), printed as `search: <class> -> <basenames, sorted,
    10	#   or none>`; beside it, the files that mention the class anywhere (`grep -rli
    11	#   <class>`), printed as `search-body: <class> -> <basenames or none>`. The
    12	#   CompactionDB search runs `uv run --no-project .claude/hooks/contextdb_cli.py
    13	#   memory search --limit 1000 -- <class>` with the class as one argument after
    14	#   `--` (no shell; a slug like `--help` is a query, never an option: thread
    15	#   4254771284), and prints its match count, `>=1000 matches (capped)` when the
    16	#   count reaches that limit (the CLI's default is 30: thread 4255494137). All
    17	#   run in the checkout this script lives in (`git rev-parse --show-toplevel`
    18	#   there), never the caller's: a PR worktree's CLI is PR-controlled code
    19	#   (thread 4253994697).
    20	# @arg $1 string Class slug.
    21	# @exitcode 0 Every search ran.
    22	# @exitcode 1 A search failed (the lines of the searches before it are printed).
    23	# @exitcode 2 Usage error, or the class is not a slug.
    24	# @example
    25	#   scripts/orchestrator/three-repeat.sh bookkeeping
    26	set -euo pipefail
    27	
    28	if (($# != 1)) || [[ ! $1 =~ ^[a-z0-9-]+$ ]]; then
    29	    echo "usage: three-repeat.sh <class>   (a slug of [a-z0-9-])" >&2
    30	    exit 2
    31	fi
    32	class=$1
    33	root="$(git -C "$(dirname -- "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
    34	dir="${root}/.orchestration/learning/mistakes"
    35	[[ -d ${dir} ]] || {
    36	    echo "three-repeat: ${dir} does not exist" >&2
    37	    exit 1
    38	}
    39	# @description Print the sorted basenames of the records grep matches, or `none`.
    40	# @arg $1 string grep options (`-rl` or `-rli`).
    41	# @arg $2 string Pattern.
    42	# @exitcode 1 grep failed (exit 2).
    43	matches() {
    44	    local files rc=0
    45	    files="$(/usr/bin/grep "$1" -- "$2" "${dir}")" || rc=$?
    46	    ((rc <= 1)) || return 1
    47	    files="$(awk -F/ 'NF {print $NF}' <<< "${files}" | LC_ALL=C sort | paste -sd, - | sed 's/,/, /g')"
    48	    printf '%s' "${files:-none}"
    49	}
    50	records="$(matches -rl "^classes:.*${class}")" || exit 1
    51	echo "search: ${class} -> ${records}"
    52	records="$(matches -rli "${class}")" || exit 1
    53	echo "search-body: ${class} -> ${records}"
    54	
    55	limit=1000
    56	memory="$(cd -- "${root}" && uv run --no-project "${root}/.claude/hooks/contextdb_cli.py" memory search --limit "${limit}" -- "${class}")" || {
    57	    echo "three-repeat: the CompactionDB search failed" >&2
    58	    exit 1
    59	}
    60	n="$(/usr/bin/grep -cE '^[0-9a-f]{8}-' <<< "${memory}" || true)"
    61	if ((n >= limit)); then
    62	    echo "compactiondb: ${class} -> >=${limit} matches (capped)"
    63	else
    64	    echo "compactiondb: ${class} -> ${n} matches"
    65	fi

 succeeded in 127ms:
   165	 tests/fixtures/regime/invariants.md                |  2 +-
   166	 tests/fixtures/regime/orchestrator-step-6.md       |  2 +-
   167	 tests/unit/test_agmsg_orchestration_docs.py        | 57 +++++++++++++---------
   168	 4 files changed, 39 insertions(+), 26 deletions(-)
   169	$ git diff --numstat origin/main...HEAD -- . ":!.orchestration"
   170	1	1	AGENTS.md
   171	6	4	home/dot_agents/skills/agmsg-orchestration/SKILL.md
   172	1	1	tests/fixtures/regime/code-review-orchestration.md
   173	4	2	tests/fixtures/regime/invariants.md
   174	1	0	tests/fixtures/regime/orchestrator-step-6.md
   175	107	1	tests/unit/test_agmsg_orchestration_docs.py
   176	```
   177	
   178	## 8. CompactionDB
   179	
   180	```text
   181	$ uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "[memory:decision] dotfiles-T128-playbook-rules-a04 (plan 010 option D): SKILL Orchestrator Playbook step 6 and the three-repeat bullet state the obligation ..."   # main checkout, permission gate
   182	a3ae0494-87a7-437c-b39a-2a08ecfcd170
   183	```
   184	
   185	## 9. CI and the Bot on `2276a365`
   186	
   187	```text
   188	$ scratchpad/ci-watch.sh
   189	ci-watch exit status: 0
   190	GitGuardian Security Checks	completed	success
   191	private-bootstrap (macos-14, client)	completed	success
   192	private-bootstrap (ubuntu-24.04, client)	completed	success
   193	private-bootstrap (ubuntu-24.04, server)	completed	success
   194	public-bootstrap (macos-14, client)	completed	success
   195	public-bootstrap (ubuntu-24.04, client)	completed	success
   196	public-bootstrap (ubuntu-24.04, server)	completed	success
   197	test (macos-14, client)	completed	success
   198	test (ubuntu-24.04, client)	completed	success
   199	test (ubuntu-24.04, server)	completed	success
   200	test (ubuntu-26.04, client)	completed	success
   201	validate	completed	success
   202	$ scratchpad/bot-wait.sh   # from the push, 15:49:28Z
   203	https://github.com/mryfmo/dotfiles/pull/328#issuecomment-6127877830
   204	posted @codex review at 2026-10-12T15:59:59Z
   205	elapsed=845s reviews:
   206	5493270947	2276a365cba9f104cadd7cd82f3fb0bfec7dac21	2026-10-12T16:03:26Z
   207	top-level comments:
   208	4250028600	2276a365cba9f104cadd7cd82f3fb0bfec7dac21	home/dot_agents/skills/agmsg-orchestration/SKILL.md
   209	
   210	[exited with code 0]
   211	$ git grep -n 'candidate class=' origin/main -- scripts/regime-counters.sh tests/ | cut -c1-170   # thread 4250028600
   212	origin/main:scripts/regime-counters.sh:147:      | group_by(.)[] | select(length >= 3) | "S1: candidate class=\(.[0]) count=\(length) source=\($s)" else empty end),
   213	origin/main:tests/unit/test_regime_counters.py:451:            ["S1: candidate class=reject skipped contract count=3 source=fixture"],
   214	```
   215	
   216	## 10. Revise round 1, amendment 1 (ACCEPTANCE `status=revise` of 2026-10-13T13:57:09Z on `2276a365`)
   217	
   218	The branch fast-forwarded to the remote head `7771082f` and merged `origin/main` (`4e7a9b3a`) in `87bce51e`. The amended sentences are in `e6602ca1`.
   219	
   220	```text
   221	$ git show origin/main:.orchestration/tasks/dotfiles-T128-playbook-rules-a04.md | shasum -a 256; shasum -a 256 .orchestration/dotfiles-T128-playbook-rules-a04/task.md
   222	c5dbc2c3d3514707870c2146ac4acfd6e96279d50f0f6bf04bd8921cd242a6fa  -
   223	c5dbc2c3d3514707870c2146ac4acfd6e96279d50f0f6bf04bd8921cd242a6fa  .orchestration/dotfiles-T128-playbook-rules-a04/task.md
   224	$ git log --oneline -4
   225	e6602ca1 docs(agmsg-orchestration): playbook-rules a04 amendment 1 sentences
   226	87bce51e Merge remote-tracking branch 'origin/main' into regime/playbook-rules
   227	4e7a9b3a chore(orchestration): boundary commit 2026-10-13 (12): plan 020/021 (the by-construction order), the three owner tasks, the cost ledger, plans 018 and 019 (#348)
   228	a1d33849 chore(orchestration): boundary commit 2026-10-13 (11): T718 first slice merged (a04 records), a02 dispatched, T703 a04 amendment 1 and its owner task, M-20261012-34/35, C-33/34, plan 017 (#347)
   229	$ uv run --no-project python -I <the check below>   # each quoted sentence of the amended items 1, 4 and 5, as the task file quotes it, is in the SKILL verbatim
   230	item 1: 1161 characters, in the SKILL: True
   231	item 4: 789 characters, in the SKILL: True
   232	item 5: 334 characters, in the SKILL: True
   233	$ uv run --no-project python -m unittest tests/unit/test_agmsg_orchestration_docs.py -v 2>&1 | sed -E 's/ \(tests\.unit\.[a-z_]+\.[A-Za-z]+\.[a-z0-9_]+\)//'   # drops each test's repeated dotted id
   234	test_docs_no_longer_name_codex_review_commit ... ok
   235	test_rule_and_skill_name_worker_seats_not_codex_workers ... ok
   236	test_rule_drops_the_worker_network_escalation ... ok
   237	test_skill_drops_the_pane_status_gate_and_raw_pane_wakes ... ok
   238	test_rule_pointers_name_real_skill_sections ... ok
   239	test_rule_states_the_invariants ... ok
   240	test_word_budgets ... ok
   241	test_audit_command_lives_only_in_the_task_level_audit_bullet ... ok
   242	test_codex_agents_points_at_the_worklog_section ... ok
   243	test_contextdb_cli_is_invoked_with_uv_run ... ok
   244	test_skill_masks_evidence_with_a_runnable_command ... ok
   245	test_claude_worker_merge_denials_and_prefix_limits_are_documented ... ok
   246	test_codex_worker_profile_defaults_to_standard ... ok
   247	test_skill_carries_the_audit_gate_and_bot_wait_mechanics ... ok
   248	test_skill_carries_the_parallel_execution_and_routing_mechanics ... ok
   249	test_skill_carries_the_registration_and_delivery_mechanics ... ok
   250	test_skill_carries_the_session_lessons ... ok
   251	test_a_design_lands_on_main_before_its_task ... ok
   252	test_a_revise_acceptance_names_the_previous_head_and_a_check ... ok
   253	test_a_trust_boundary_task_carries_a_threat_table ... ok
   254	test_bot_fix_rounds_are_capped_and_the_pr_is_ready_first ... ok
   255	test_boundary_merge_sentence_names_the_in_job_decision ... ok
   256	test_closed_selector_existence_is_checked_at_acceptance ... ok
   257	test_code_review_rules_cover_orchestration_records_and_threat_tables ... ok
   258	test_counters_bullet_names_owners_not_sources ... ok
   259	test_counters_run_before_every_acceptance_action ... ok
   260	test_design_review_runs_in_paired_rounds_with_a_cap ... ok
   261	test_dispatches_are_recorded_from_the_bus ... ok
   262	test_open_review_body_findings_have_an_identifier ... ok
   263	test_open_third_round_threads_have_an_integration_outcome ... ok
   264	test_orchestration_records_rule_binds_the_bot_review_only ... ok
   265	test_pattern_rules_pin_their_safeguards ... ok
   266	test_question_pongs_are_in_the_contract ... ok
   267	test_regime_rule_sections_are_pinned_whole ... ok
   268	test_rule_changes_travel_as_task_amendments ... ok
   269	test_shape_is_checked_by_hand_until_the_schema_lands ... ok
   270	test_shape_rules_and_the_decision_sentence_are_pinned ... ok
   271	test_task_file_review_is_one_round_with_a_fixed_stop_condition ... ok
   272	test_the_bot_wait_filters_the_codex_bot ... ok
   273	test_the_ci_watch_is_joined_before_the_result ... ok
   274	test_the_ci_watcher_survives_the_no_checks_race ... ok
   275	test_the_gate_reads_the_acceptance_record ... ok
   276	test_threat_table_rows_have_a_fixed_unit ... ok
   277	test_threat_table_rule_carries_no_grammar ... ok
   278	test_three_repeats_start_with_a_pasted_correction_search ... ok
   279	test_workers_commit_inside_the_sandbox ... ok
   280	test_workers_open_the_pr_as_a_draft ... ok
   281	
   282	----------------------------------------------------------------------
   283	Ran 47 tests in 0.009s
   284	
   285	OK
   286	$ prettier --check home/dot_agents/skills/agmsg-orchestration/SKILL.md tests/fixtures/regime/*.md; ruff format --config ruff.toml --check tests/unit/test_agmsg_orchestration_docs.py
   287	Checking formatting...
   288	All matched files use Prettier code style!
   289	1 file already formatted
   290	$ git diff --stat 87bce51e HEAD -- home tests AGENTS.md   # the fixture changes of this round: invariants.md and orchestrator-step-6.md
   291	 .../dot_agents/skills/agmsg-orchestration/SKILL.md |  6 ++--
   292	 tests/fixtures/regime/invariants.md                |  4 +--
   293	 tests/fixtures/regime/orchestrator-step-6.md       |  2 +-
   294	 tests/unit/test_agmsg_orchestration_docs.py        | 38 +++++++++++++++-------
   295	 4 files changed, 32 insertions(+), 18 deletions(-)
   296	$ uv run --no-project python <scratchpad>/mutate-pr328.py   # each amended sentence put back to its previous form, in the SKILL and its fixture
   297	P1 step 6: complete bus read: test_dispatches_are_recorded_from_the_bus -> FAILED (killed) | AssertionError: 'Every dispatch (TASK, ACCEPTANCE, PING) is recorded in the current acceptance record under a `dispatch:` key as the bus line with its read mark
   298	P2 step 6: thirty minutes: test_dispatches_are_recorded_from_the_bus -> FAILED (killed) | AssertionError: "A seated worker idle for 20 minutes since its latest bus event for the task while a dispatchable task exists (INV-10's idle figure; its 30 minu
   299	P3 row unit: no wildcard rule: test_threat_table_rows_have_a_fixed_unit -> FAILED (killed) | AssertionError: "metadata separators). The row unit is one row per `allowed_files` entry, one row per listed control that is not a path (task metadata, workflow
   300	P4 invariant check: ids only: test_task_file_review_is_one_round_with_a_fixed_stop_condition -> FAILED (killed) | AssertionError: "one invariant check (for a task that carries an `invariants` key: the task id maps to its `implementing_tasks` entry, the invariant ids match, 
   301	P5 fixture only (pinning): test_regime_rule_sections_are_pinned_whole -> FAILED (killed) | AssertionError: '6. S[2911 chars] for 20 minutes since its latest bus event for[568 chars]ge).' != '6. S[2911 chars] for 30 minutes since its latest bus event f
   302	$ git diff --numstat origin/main...HEAD
   303	3	0	.orchestration/dotfiles-T128-playbook-rules-a01/autoskill.md
   304	7	0	.orchestration/dotfiles-T128-playbook-rules-a01/learning.md
   305	49	0	.orchestration/dotfiles-T128-playbook-rules-a01/report.md
   306	26	0	.orchestration/dotfiles-T128-playbook-rules-a01/sandbox.md
   307	84	0	.orchestration/dotfiles-T128-playbook-rules-a01/task.md
   308	220	0	.orchestration/dotfiles-T128-playbook-rules-a01/validation.md
   309	3	0	.orchestration/dotfiles-T128-playbook-rules-a02/autoskill.md
   310	7	0	.orchestration/dotfiles-T128-playbook-rules-a02/learning.md
   311	71	0	.orchestration/dotfiles-T128-playbook-rules-a02/report.md
   312	26	0	.orchestration/dotfiles-T128-playbook-rules-a02/sandbox.md
   313	90	0	.orchestration/dotfiles-T128-playbook-rules-a02/task.md
   314	362	0	.orchestration/dotfiles-T128-playbook-rules-a02/validation.md
   315	3	0	.orchestration/dotfiles-T128-playbook-rules-a03/autoskill.md
   316	6	0	.orchestration/dotfiles-T128-playbook-rules-a03/learning.md
   317	53	0	.orchestration/dotfiles-T128-playbook-rules-a03/report.md
   318	21	0	.orchestration/dotfiles-T128-playbook-rules-a03/sandbox.md
   319	92	0	.orchestration/dotfiles-T128-playbook-rules-a03/task.md
   320	183	0	.orchestration/dotfiles-T128-playbook-rules-a03/validation.md
   321	3	0	.orchestration/dotfiles-T128-playbook-rules-a04/autoskill.md
   322	6	0	.orchestration/dotfiles-T128-playbook-rules-a04/learning.md
   323	55	0	.orchestration/dotfiles-T128-playbook-rules-a04/report.md
   324	21	0	.orchestration/dotfiles-T128-playbook-rules-a04/sandbox.md
   325	94	0	.orchestration/dotfiles-T128-playbook-rules-a04/task.md
   326	183	0	.orchestration/dotfiles-T128-playbook-rules-a04/validation.md
   327	1	1	AGENTS.md
   328	6	4	home/dot_agents/skills/agmsg-orchestration/SKILL.md
   329	1	1	tests/fixtures/regime/code-review-orchestration.md
   330	4	2	tests/fixtures/regime/invariants.md
   331	1	0	tests/fixtures/regime/orchestrator-step-6.md
   332	121	1	tests/unit/test_agmsg_orchestration_docs.py
   333	$ git diff --numstat origin/main...HEAD | awk '$3 !~ /^\.orchestration\// {f++} $3 !~ /^\.orchestration\// && $3 !~ /^tests\// {o+=$1} $3 ~ /^tests\// {t+=$1} END {print "files outside .orchestration/:", f, "added outside tests/:", o, "added under tests/:", t}'
   334	files outside .orchestration/: 6 added outside tests/: 7 added under tests/: 127
   335	```
   336	
   337	## 11. CI on `65a3d71b` (main-checkout copy only)
   338	
   339	```text
   340	$ gh pr checks 328 --watch --interval 30   # the final listing
   341	CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
   342	GitGuardian Security Checks	pass	37s	https://dashboard.gitguardian.com	
   343	private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/38410198303/job/115340181995	
   344	private-bootstrap (ubuntu-24.04, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/38410198303/job/115340181810	
   345	private-bootstrap (ubuntu-24.04, server)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/38410198303/job/115340181888	
round: 1
previous_head: 2276a365cba9f104cadd7cd82f3fb0bfec7dac21
checks:
  - tests/unit/test_agmsg_orchestration_docs.py::AgmsgRegimePatternTest::test_dispatches_are_recorded_from_the_bus
  - tests/unit/test_agmsg_orchestration_docs.py::AgmsgRegimePatternTest::test_threat_table_rows_have_a_fixed_unit
  - tests/unit/test_agmsg_orchestration_docs.py::AgmsgRegimePatternTest::test_task_file_review_is_one_round_with_a_fixed_stop_condition
  - tests/unit/test_agmsg_orchestration_docs.py::AgmsgRegimePatternTest::test_regime_rule_sections_are_pinned_whole
home/.chezmoiexternal.yaml.tmpl
home/.chezmoiremove
home/.chezmoiscripts/common/run_after_03-install-sheldon.sh.tmpl
home/.chezmoiscripts/common/run_before_00-refuse-dirty-source.sh.tmpl
home/.chezmoiscripts/common/run_once_after_02-install-mise.sh.tmpl
home/.chezmoiscripts/ubuntu/run_after_04-install-aws-cli.sh.tmpl
home/.chezmoiscripts/ubuntu/run_after_05-client-install-zed.sh.tmpl
home/.chezmoiscripts/ubuntu/run_after_10-install-starship.sh.tmpl
home/.chezmoitemplates/chezmoiexternal.d/macos.yaml.tmpl
home/.chezmoitemplates/chezmoiexternal.d/ubuntu.yaml.tmpl
home/.chezmoitemplates/claude-settings-managed.json
home/.chezmoitemplates/codex-config-managed.toml

**Reviewing diff record comparisons**
exec
/bin/zsh -lc "python3 -c 'import json,pathlib
p=pathlib.Path('\\''.orchestration/validation/dotfiles-T128-playbook-rules-a04-pr-feedback.json'\\'');d=json.loads(p.read_text())
for i,x in enumerate(d['\\''items'\\'']):
 print(i,repr(x))'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 114ms:
0 {'source': 'issue_comment', 'author': 'coderabbitai[bot]', 'bot': True, 'level': 'comment', 'path': None, 'line': None, 'body': '<!-- This is an auto-generated comment: summarize by coderabbit.ai -->\n<!-- This is an auto-generated comment: skip review by coderabbit.ai -->\n\n> [!IMPORTANT]\n> ## Review skipped\n> \n> Auto reviews are disabled on this repository. Please check the settings in the CodeRabbit UI or the `.coderabbit.yaml` file in this repository. To trigger a single review, invoke the `@coderabbitai review` command.\n> \n> <details>\n> <summary><strong>⚙️ Run configuration</strong></summary>\n> <dl>\n> <dd>\n> \n> - **Configuration used**: Repository: mryfmo/dotfiles/.coderabbit.yaml\n> - **Review profile**: CHILL\n> - **Plan**: Advanced\n> - **Run ID**: `33fc13c7-a603-47a6-b86c-13014d230b99`\n> \n> </dd>\n> </dl>\n> </details>\n> \n> You can disable this status message by setting the `reviews.review_status` to `false` in the CodeRabbit configuration file.\n> \n> Use the checkbox below for a quick retry:\n> - [ ] <!-- {"checkboxId":"e9bb8d72-00e8-4f67-9cb2-caf3b22574fe"} --> 🔍 Trigger review\n\n<!-- end of auto-generated comment: skip review by coderabbit.ai -->\n\n<!-- autopilot:start -->\n- [ ] <!-- {"checkboxId":"2708ad07-9f24-4260-9c11-7dc76a49f2e3"} --> <strong title="Keep fixing CodeRabbit findings and required CI, and resolving merge conflicts">Autofix</strong> · Keep fixing CodeRabbit findings and required CI, and resolving merge conflicts\n<!-- autopilot:end -->\n<!-- tips_start -->\n\n\n\nThanks for using [CodeRabbit](https://coderabbit.ai?utm_source=oss&utm_medium=github&utm_campaign=mryfmo/dotfiles&utm_content=328)! It\'s free for OSS, and your support helps us grow. If you like it, consider giving us a shout-out.\n\n<details>\n<summary><strong>❤️ Share</strong></summary>\n<dl>\n<dd>\n\n- [X](https://twitter.com/intent/tweet?text=I%20just%20used%20%40coderabbitai%20for%20my%20code%20review%2C%20and%20it%27s%20fantastic%21%20It%27s%20free%20for%20OSS%20and%20offers%20a%20free%20trial%20for%20the%20proprietary%20code.%20Check%20it%20out%3A&url=https%3A//coderabbit.ai)\n- [Mastodon](https://mastodon.social/share?text=I%20just%20used%20%40coderabbitai%20for%20my%20code%20review%2C%20and%20it%27s%20fantastic%21%20It%27s%20free%20for%20OSS%20and%20offers%20a%20free%20trial%20for%20the%20proprietary%20code.%20Check%20it%20out%3A%20https%3A%2F%2Fcoderabbit.ai)\n- [Reddit](https://www.reddit.com/submit?title=Great%20tool%20for%20code%20review%20-%20CodeRabbit&text=I%20just%20used%20CodeRabbit%20for%20my%20code%20review%2C%20and%20it%27s%20fantastic%21%20It%27s%20free%20for%20OSS%20and%20offers%20a%20free%20trial%20for%20proprietary%20code.%20Check%20it%20out%3A%20https%3A//coderabbit.ai)\n- [LinkedIn](https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Fcoderabbit.ai&mini=true&title=Great%20tool%20for%20code%20review%20-%20CodeRabbit&summary=I%20just%20used%20CodeRabbit%20for%20my%20code%20review%2C%20and%20it%27s%20fantastic%21%20It%27s%20free%20for%20OSS%20and%20offers%20a%20free%20trial%20for%20proprietary%20code)\n\n</dd>\n</dl>\n</details>\n\n\n<sub>Comment `@coderabbitai help` to get the list of available commands.</sub>\n\n<!-- tips_end -->', 'url': 'https://github.com/mryfmo/dotfiles/pull/328#issuecomment-6123947425', 'disposition': "not-applicable:bot summary or onboarding comment, no finding; evidence=gh api repos/mryfmo/dotfiles/issues/comments/6123947425 --jq '.user.login,.body'"}
1 {'source': 'issue_comment', 'author': 'chatgpt-codex-connector[bot]', 'bot': True, 'level': 'comment', 'path': None, 'line': None, 'body': '<!-- codex-pull-request-review-summary -->\n<!-- codex-security-review:v1 {"blockingSeverityThreshold":"P0","headSha":"9b2c02a1a8763816b8774914541c6fef47e9f2a9","mergeGateEnabled":false,"pullRequestNumber":328,"repository":"mryfmo/dotfiles","status":"completed"} -->\n## Codex Review Summary\n\nThis comment shows the latest Codex review activity on this pull request.\n\n| Review | Status | Commit | Review trigger |\n| --- | --- | --- | --- |\n| 📝 **Code Review** | ✅ **Completed** <relative-time datetime="2026-10-13T10:03:33.563923Z">2026-10-13T10:03:33.563923Z</relative-time> | `7771082` | New commits |\n| 🔒 **Security Review** | ✅ **Completed** <relative-time datetime="2026-10-12T12:20:30.156256Z">2026-10-12T12:20:30.156256Z</relative-time> | `9b2c02a` | Draft marked ready |\n\n\n\n<details> <summary>ℹ️ About Codex in GitHub</summary>\n<br/>\n\n[Your team has set up Codex to review pull requests in this repo](https://chatgpt.com/codex/cloud/settings/general). Reviews are triggered when you\n- Open a pull request for review\n- Mark a draft as ready\n- Comment "@codex review" or "@codex security review".\n\nCodex reacts with 👀 while any review is running, comments if it has suggestions, and reacts with 👍 once all reviews finish with no findings.\n\n</details>', 'url': 'https://github.com/mryfmo/dotfiles/pull/328#issuecomment-6124048407', 'disposition': "not-applicable:bot summary or onboarding comment, no finding; evidence=gh api repos/mryfmo/dotfiles/issues/comments/6124048407 --jq '.user.login,.body'"}
2 {'source': 'issue_comment', 'author': 'moriya-fumio-thd', 'bot': False, 'level': 'comment', 'path': None, 'line': None, 'body': '@codex review', 'url': 'https://github.com/mryfmo/dotfiles/pull/328#issuecomment-6125487230', 'disposition': "not-applicable:bot summary or onboarding comment, no finding; evidence=gh api repos/mryfmo/dotfiles/issues/comments/6125487230 --jq '.user.login,.body'"}
3 {'source': 'issue_comment', 'author': 'moriya-fumio-thd', 'bot': False, 'level': 'comment', 'path': None, 'line': None, 'body': '@codex review', 'url': 'https://github.com/mryfmo/dotfiles/pull/328#issuecomment-6127877830', 'disposition': "not-applicable:bot summary or onboarding comment, no finding; evidence=gh api repos/mryfmo/dotfiles/issues/comments/6127877830 --jq '.user.login,.body'"}
4 {'source': 'review', 'author': 'chatgpt-codex-connector[bot]', 'bot': True, 'level': 'commented', 'path': None, 'line': None, 'body': '\n### 💡 Codex Review\n\nHere are some automated review suggestions for this pull request.\n\n**Reviewed commit:** `9b2c02a1a8`\n    \n\n<details> <summary>ℹ️ About Codex in GitHub</summary>\n<br/>\n\nCodex has been enabled to automatically review pull requests in this repo. Reviews are triggered when you\n- Open a pull request for review\n- Mark a draft as ready\n- Comment "@codex review".\n\nIf Codex has suggestions, it will comment; otherwise it will react with 👍.\n\n\n\n\nWhen you [sign up for Codex through ChatGPT](https://openai.com/codex), Codex can also answer questions or update the PR, like "@codex address that feedback".\n            \n</details>', 'url': 'https://github.com/mryfmo/dotfiles/pull/328#pullrequestreview-5490674624', 'commit': '9b2c02a1a8763816b8774914541c6fef47e9f2a9', 'disposition': "not-applicable:review object, its findings are the inline threads, each dispositioned on its own; evidence=gh api repos/mryfmo/dotfiles/pulls/328/reviews/5490674624 --jq '.state,.body'"}
5 {'source': 'review', 'author': 'chatgpt-codex-connector[bot]', 'bot': True, 'level': 'commented', 'path': None, 'line': None, 'body': '\n### 💡 Codex Review\n\nHere are some automated review suggestions for this pull request.\n\n**Reviewed commit:** `375bae0f90`\n    \n\n<details> <summary>ℹ️ About Codex in GitHub</summary>\n<br/>\n\nCodex has been enabled to automatically review pull requests in this repo. Reviews are triggered when you\n- Open a pull request for review\n- Mark a draft as ready\n- Comment "@codex review".\n\nIf Codex has suggestions, it will comment; otherwise it will react with 👍.\n\n\n\n\nWhen you [sign up for Codex through ChatGPT](https://openai.com/codex), Codex can also answer questions or update the PR, like "@codex address that feedback".\n            \n</details>', 'url': 'https://github.com/mryfmo/dotfiles/pull/328#pullrequestreview-5491172156', 'commit': '375bae0f90bd167c0393be8088b92cf338657608', 'disposition': "not-applicable:review object, its findings are the inline threads, each dispositioned on its own; evidence=gh api repos/mryfmo/dotfiles/pulls/328/reviews/5491172156 --jq '.state,.body'"}
6 {'source': 'review', 'author': 'chatgpt-codex-connector[bot]', 'bot': True, 'level': 'commented', 'path': None, 'line': None, 'body': '\n### 💡 Codex Review\n\nHere are some automated review suggestions for this pull request.\n\n**Reviewed commit:** `c4e0bb72ab`\n    \n\n<details> <summary>ℹ️ About Codex in GitHub</summary>\n<br/>\n\nCodex has been enabled to automatically review pull requests in this repo. Reviews are triggered when you\n- Open a pull request for review\n- Mark a draft as ready\n- Comment "@codex review".\n\nIf Codex has suggestions, it will comment; otherwise it will react with 👍.\n\n\n\n\nWhen you [sign up for Codex through ChatGPT](https://openai.com/codex), Codex can also answer questions or update the PR, like "@codex address that feedback".\n            \n</details>', 'url': 'https://github.com/mryfmo/dotfiles/pull/328#pullrequestreview-5491652266', 'commit': 'c4e0bb72ab045b8a9d4d013fa2c4eacdc5c3589b', 'disposition': "not-applicable:review object, its findings are the inline threads, each dispositioned on its own; evidence=gh api repos/mryfmo/dotfiles/pulls/328/reviews/5491652266 --jq '.state,.body'"}
7 {'source': 'review', 'author': 'chatgpt-codex-connector[bot]', 'bot': True, 'level': 'commented', 'path': None, 'line': None, 'body': '\n### 💡 Codex Review\n\nHere are some automated review suggestions for this pull request.\n\n**Reviewed commit:** `fe34f7db03`\n    \n\n<details> <summary>ℹ️ About Codex in GitHub</summary>\n<br/>\n\nCodex has been enabled to automatically review pull requests in this repo. Reviews are triggered when you\n- Open a pull request for review\n- Mark a draft as ready\n- Comment "@codex review".\n\nIf Codex has suggestions, it will comment; otherwise it will react with 👍.\n\n\n\n\nWhen you [sign up for Codex through ChatGPT](https://openai.com/codex), Codex can also answer questions or update the PR, like "@codex address that feedback".\n            \n</details>', 'url': 'https://github.com/mryfmo/dotfiles/pull/328#pullrequestreview-5492353166', 'commit': 'fe34f7db0311fd5503104abe1a4b8ddec509c547', 'disposition': "not-applicable:review object, its findings are the inline threads, each dispositioned on its own; evidence=gh api repos/mryfmo/dotfiles/pulls/328/reviews/5492353166 --jq '.state,.body'"}
8 {'source': 'review', 'author': 'chatgpt-codex-connector[bot]', 'bot': True, 'level': 'commented', 'path': None, 'line': None, 'body': '\n### 💡 Codex Review\n\nHere are some automated review suggestions for this pull request.\n\n**Reviewed commit:** `e12872cd99`\n    \n\n<details> <summary>ℹ️ About Codex in GitHub</summary>\n<br/>\n\nCodex has been enabled to automatically review pull requests in this repo. Reviews are triggered when you\n- Open a pull request for review\n- Mark a draft as ready\n- Comment "@codex review".\n\nIf Codex has suggestions, it will comment; otherwise it will react with 👍.\n\n\n\n\nWhen you [sign up for Codex through ChatGPT](https://openai.com/codex), Codex can also answer questions or update the PR, like "@codex address that feedback".\n            \n</details>', 'url': 'https://github.com/mryfmo/dotfiles/pull/328#pullrequestreview-5492486970', 'commit': 'e12872cd992853b927812f545e0df24afa4d78b6', 'disposition': "not-applicable:review object, its findings are the inline threads, each dispositioned on its own; evidence=gh api repos/mryfmo/dotfiles/pulls/328/reviews/5492486970 --jq '.state,.body'"}
9 {'source': 'review', 'author': 'chatgpt-codex-connector[bot]', 'bot': True, 'level': 'commented', 'path': None, 'line': None, 'body': '\n### 💡 Codex Review\n\nHere are some automated review suggestions for this pull request.\n\n**Reviewed commit:** `2276a365cb`\n    \n\n<details> <summary>ℹ️ About Codex in GitHub</summary>\n<br/>\n\nCodex has been enabled to automatically review pull requests in this repo. Reviews are triggered when you\n- Open a pull request for review\n- Mark a draft as ready\n- Comment "@codex review".\n\nIf Codex has suggestions, it will comment; otherwise it will react with 👍.\n\n\n\n\nWhen you [sign up for Codex through ChatGPT](https://openai.com/codex), Codex can also answer questions or update the PR, like "@codex address that feedback".\n            \n</details>', 'url': 'https://github.com/mryfmo/dotfiles/pull/328#pullrequestreview-5493270947', 'commit': '2276a365cba9f104cadd7cd82f3fb0bfec7dac21', 'disposition': "not-applicable:review object, its findings are the inline threads, each dispositioned on its own; evidence=gh api repos/mryfmo/dotfiles/pulls/328/reviews/5493270947 --jq '.state,.body'"}
10 {'source': 'review', 'author': 'chatgpt-codex-connector[bot]', 'bot': True, 'level': 'commented', 'path': None, 'line': None, 'body': '\n### 💡 Codex Review\n\nHere are some automated review suggestions for this pull request.\n\n**Reviewed commit:** `7771082f7d`\n    \n\n<details> <summary>ℹ️ About Codex in GitHub</summary>\n<br/>\n\nCodex has been enabled to automatically review pull requests in this repo. Reviews are triggered when you\n- Open a pull request for review\n- Mark a draft as ready\n- Comment "@codex review".\n\nIf Codex has suggestions, it will comment; otherwise it will react with 👍.\n\n\n\n\nWhen you [sign up for Codex through ChatGPT](https://openai.com/codex), Codex can also answer questions or update the PR, like "@codex address that feedback".\n            \n</details>', 'url': 'https://github.com/mryfmo/dotfiles/pull/328#pullrequestreview-5501887212', 'commit': '7771082f7db20a6ea1b53c5e95817aee6e23e177', 'disposition': "not-applicable:review object, its findings are the inline threads, each dispositioned on its own; evidence=gh api repos/mryfmo/dotfiles/pulls/328/reviews/5501887212 --jq '.state,.body'"}
11 {'source': 'review_comment', 'author': 'chatgpt-codex-connector[bot]', 'bot': True, 'level': 'comment', 'path': '.orchestration/dotfiles-T128-playbook-rules-a01/task.md', 'line': 40, 'body': '**<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Split the orchestrator effects into separate threat rows**\n\nThis task changes trust-boundary review rules, but its threat table combines merge, update-branch, and forced removal in one row. The newly established unit requires one row per orchestrator effect, so these three controls must be independently dispositioned rather than grouped; otherwise the task violates the exact completeness rule this commit adds.\n\nAGENTS.md reference: [AGENTS.md:L78-L78](https://github.com/mryfmo/dotfiles/blob/9b2c02a1a8763816b8774914541c6fef47e9f2a9/AGENTS.md#L78-L78)\n\nUseful? React with 👍\xa0/ 👎.', 'url': 'https://github.com/mryfmo/dotfiles/pull/328#discussion_r4247933544', 'resolved': False, 'outdated': False, 'disposition': 'fixed:95ba4e4c'}
12 {'source': 'review_comment', 'author': 'chatgpt-codex-connector[bot]', 'bot': True, 'level': 'comment', 'path': 'home/dot_agents/skills/agmsg-orchestration/SKILL.md', 'line': 69, 'body': "**<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Limit the mapping check to invariant-bearing tasks**\n\nThe new fixed stop condition unconditionally requires every task ID to occur in the design's `implementing_tasks` and have matching invariant IDs. This commit's own `kind: docs` task has no `invariants` field and `dotfiles-T128-playbook-rules-a01` is absent from the referenced design's map, so applying the rule literally makes this task—and other non-implementation docs/review tasks—impossible to approve. Qualify this check for tasks that actually claim design invariants.\n\nUseful? React with 👍\xa0/ 👎.", 'url': 'https://github.com/mryfmo/dotfiles/pull/328#discussion_r4247933561', 'resolved': False, 'outdated': True, 'disposition': 'fixed:8b1dbefc'}
13 {'source': 'review_comment', 'author': 'chatgpt-codex-connector[bot]', 'bot': True, 'level': 'comment', 'path': 'home/dot_agents/skills/agmsg-orchestration/SKILL.md', 'line': 74, 'body': '**<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Search the correction index instead of raw correction text**\n\nThe mandated lookup cannot reliably determine whether a matching correction exists. For the existing repeated class `bookkeeping`, both prescribed searches return no matches even though `M-20261012-4.md` links the failure to corrections C-3 and C-6; conversely, searching the existing class `sources` makes `grep -rl` return every correction because each file has a generic `sources:` field. This can incorrectly force creation of a duplicate correction or select an unrelated one, so the procedure should query the mistake/index mapping or require an explicit class field in correction records.\n\nUseful? React with 👍\xa0/ 👎.', 'url': 'https://github.com/mryfmo/dotfiles/pull/328#discussion_r4247933574', 'resolved': False, 'outdated': True, 'disposition': 'fixed:8b1dbefc'}
14 {'source': 'review_comment', 'author': 'chatgpt-codex-connector[bot]', 'bot': True, 'level': 'comment', 'path': 'home/dot_agents/skills/agmsg-orchestration/SKILL.md', 'line': 74, 'body': "**<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Add class fields before searching them**\n\nFresh evidence after the earlier correction-search finding is that the amended head still has no `classes:` field in any of the 14 files under `.orchestration/learning/mistakes/` (`git grep '^classes:' ee2d5e1 -- .orchestration/learning/mistakes` returns no matches). Consequently, when an S1 class reaches three, this prescribed command always reports no match and the following rule incorrectly requires creating a duplicate mistake and correction instead of following the existing `corrections:` links; add/populate the class index in the same changeset or search an existing source that actually maps ledger classes.\n\nUseful? React with 👍\xa0/ 👎.", 'url': 'https://github.com/mryfmo/dotfiles/pull/328#discussion_r4248319926', 'resolved': False, 'outdated': True, 'disposition': 'fixed:e12872cd'}
15 {'source': 'review_comment', 'author': 'chatgpt-codex-connector[bot]', 'bot': True, 'level': 'comment', 'path': 'home/dot_agents/skills/agmsg-orchestration/SKILL.md', 'line': 164, 'body': "**<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Define a wall-clock trigger for stalled-result checks**\n\nWhen a worker goes silent after reading a TASK, “past the task's expected duration” has no computable threshold: the message contract supplies only `max_turns`, and step 7 merely says to track that turn count, which cannot advance or be observed while no messages arrive. The failure mode this sentence is intended to prevent can therefore still result in an arbitrarily long silent wait; define a concrete elapsed-time limit or add an explicit duration field to TASKs before requiring the bus read and PING.\n\nUseful? React with 👍\xa0/ 👎.", 'url': 'https://github.com/mryfmo/dotfiles/pull/328#discussion_r4248319936', 'resolved': False, 'outdated': True, 'disposition': 'fixed:4b62feda'}
16 {'source': 'review_comment', 'author': 'chatgpt-codex-connector[bot]', 'bot': True, 'level': 'comment', 'path': 'home/dot_agents/skills/agmsg-orchestration/SKILL.md', 'line': 74, 'body': "**<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Land the gate check before claiming S6 enforcement**\n\nIn this commit's tree, `scripts/require-crit-review.py` never reads `ACCEPTANCE_EVIDENCE`, and the Makefile does not forward it, so when a finding class reaches three the documented gate command can still succeed without any acceptance record or pasted correction search. The added token test only verifies this sentence, not the merge backstop; either land `dotfiles-T128-gate-evidence-a01` first/in this changeset or avoid stating that the gate refuses the action.\n\nAGENTS.md reference: [AGENTS.md:L78-L78](https://github.com/mryfmo/dotfiles/blob/c4e0bb72ab045b8a9d4d013fa2c4eacdc5c3589b/AGENTS.md#L78-L78)\n\nUseful? React with 👍\xa0/ 👎.", 'url': 'https://github.com/mryfmo/dotfiles/pull/328#discussion_r4248711363', 'resolved': False, 'outdated': True, 'disposition': 'fixed:f40e530a'}
17 {'source': 'review_comment', 'author': 'chatgpt-codex-connector[bot]', 'bot': True, 'level': 'comment', 'path': 'home/dot_agents/skills/agmsg-orchestration/SKILL.md', 'line': 71, 'body': '**<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Implement C4 before relying on its threat-row check**\n\nThis commit says C4 mechanically verifies every `allowed_files` row before dispatch, but the reviewed tree contains no task-consistency checker implementation—only prose/tests containing its name—and the checked-in learning index still records `task-consistency-check C4` as pending. Consequently a task can omit an allowed-file threat row while reviewers are told that this half is already verified; land the validator with this rule or keep the check explicitly manual until it exists.\n\nAGENTS.md reference: [AGENTS.md:L78-L78](https://github.com/mryfmo/dotfiles/blob/c4e0bb72ab045b8a9d4d013fa2c4eacdc5c3589b/AGENTS.md#L78-L78)\n\nUseful? React with 👍\xa0/ 👎.', 'url': 'https://github.com/mryfmo/dotfiles/pull/328#discussion_r4248711371', 'resolved': False, 'outdated': True, 'disposition': 'fixed:f40e530a'}
18 {'source': 'review_comment', 'author': 'chatgpt-codex-connector[bot]', 'bot': True, 'level': 'comment', 'path': 'home/dot_agents/skills/agmsg-orchestration/SKILL.md', 'line': 74, 'body': '**<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Handle partially landed correction statuses**\n\nWhen the search resolves to C-2, the prescribed branch is ambiguous because `.orchestration/learning/corrections/C-2.md:13` records `status: "landed for fixtures and the bullet; pending for C4 and T701"`, rather than either state this procedure recognizes. Treating it as landed applies a correction whose validator is still absent, while treating it as pending gives no definition of which remaining mechanisms must land; define partial status handling or normalize correction records to the two states before making this the acceptance procedure.\n\nUseful? React with 👍\xa0/ 👎.', 'url': 'https://github.com/mryfmo/dotfiles/pull/328#discussion_r4249303398', 'resolved': False, 'outdated': True, 'disposition': 'fixed:beee078a'}
19 {'source': 'review_comment', 'author': 'chatgpt-codex-connector[bot]', 'bot': True, 'level': 'comment', 'path': 'home/dot_agents/skills/agmsg-orchestration/SKILL.md', 'line': 164, 'body': '**<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Read the complete bus before rebuilding open tasks**\n\nWhen more than 20 messages follow an open task, the shown `history.sh <team>` read omits its TASK because that CLI defaults to the latest 20 rows, a limitation already documented in `.orchestration/tasks/dotfiles-T128-regime-counters-a02.md:28-29`; the governing design likewise requires a storage-facade or explicit-`--limit` read at `.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:172`. After a compaction, rebuilding the open-task list from the truncated view can therefore drop active work and produce false status or duplicate dispatches, so this procedure needs to require a complete-history read.\n\nUseful? React with 👍\xa0/ 👎.', 'url': 'https://github.com/mryfmo/dotfiles/pull/328#discussion_r4249303413', 'resolved': False, 'outdated': True, 'disposition': 'fixed:beee078a'}
20 {'source': 'review_comment', 'author': 'chatgpt-codex-connector[bot]', 'bot': True, 'level': 'comment', 'path': 'home/dot_agents/skills/agmsg-orchestration/SKILL.md', 'line': 164, 'body': '**<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Measure stalls from the latest task event**\n\nFresh evidence in this amended head is that the new fixed-duration clause tests whether any seat event occurred since the TASK, rather than measuring inactivity since the latest relevant event. A worker that sends one early PONG and then goes silent—or emits an event for an older task while this task is stalled—will always have “a bus event from its seat since,” so the 30-minute condition never becomes true and no PING is required; reset the inactivity clock from the latest event for this task.\n\nUseful? React with 👍\xa0/ 👎.', 'url': 'https://github.com/mryfmo/dotfiles/pull/328#discussion_r4249303426', 'resolved': False, 'outdated': True, 'disposition': 'fixed:beee078a'}
21 {'source': 'review_comment', 'author': 'chatgpt-codex-connector[bot]', 'bot': True, 'level': 'comment', 'path': 'home/dot_agents/skills/agmsg-orchestration/SKILL.md', 'line': 74, 'body': '**<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Normalize the class before executing search commands**\n\nWhen this path is triggered by `scripts/regime-counters.sh`, the class is derived from the first three words of a review-comment title with no shell-safe normalization (`scripts/regime-counters.sh:143-147`). Such a title can contain backticks, `$()`, apostrophes, or other metacharacters; substituting it into the unquoted `memory search <class slug>` command can execute text on the orchestrator host, while an apostrophe also breaks the single-quoted grep pattern. Require a defined `[a-z0-9-]` normalization or safely pass the value as a quoted argument rather than interpolating review-derived text into shell commands.\n\nAGENTS.md reference: [AGENTS.md:L78-L78](https://github.com/mryfmo/dotfiles/blob/fe34f7db0311fd5503104abe1a4b8ddec509c547/AGENTS.md#L78-L78)\n\nUseful? React with 👍\xa0/ 👎.', 'url': 'https://github.com/mryfmo/dotfiles/pull/328#discussion_r4249303433', 'resolved': False, 'outdated': True, 'disposition': 'fixed:beee078a'}
22 {'source': 'review_comment', 'author': 'chatgpt-codex-connector[bot]', 'bot': True, 'level': 'comment', 'path': 'home/dot_agents/skills/agmsg-orchestration/SKILL.md', 'line': 74, 'body': "**<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Match complete class values in the correction lookup**\n\nFresh evidence in the amended head is that the prescribed lookup still conflates distinct classes: for the existing S1 class `scope`, `grep -rl 'classes:.*scope' .orchestration/learning/mistakes/` returns both records whose class is `scope` and `M-20261012-3.md`, whose class is only `class-count-scope`. Because the next step follows every returned record's correction IDs, a substring collision can surface unrelated corrections or make a class with no exact record appear to have a match; parse the YAML list or require delimiter-aware exact matching.\n\nUseful? React with 👍\xa0/ 👎.", 'url': 'https://github.com/mryfmo/dotfiles/pull/328#discussion_r4249414388', 'resolved': False, 'outdated': True, 'disposition': 'not-applicable:the accepted a04 text prescribes no grep for the correction lookup (2276a365 SKILL.md:74: once T718 lands the lookup is three-repeat.sh, now on main a03c1daa), so the substring collision is no longer a property of this rule text, and the script side is tracked as residual R1 of the tools lineage (acceptance record of dotfiles-T128-orchestrator-tools-a04); evidence=git show 2276a365:home/dot_agents/skills/agmsg-orchestration/SKILL.md | grep -n three-repeat.sh'}
23 {'source': 'review_comment', 'author': 'chatgpt-codex-connector[bot]', 'bot': True, 'level': 'comment', 'path': 'home/dot_agents/skills/agmsg-orchestration/SKILL.md', 'line': 74, 'body': '**<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Reconcile counter candidates with slugged classes**\n\nFresh evidence in the amended head is that the two trigger paths still use incompatible class formats: `scripts/regime-counters.sh:145-147` emits the first three title words verbatim (the existing unit test expects `class=reject skipped contract`), while this rule requires the triggered class to be a `[a-z0-9-]` slug assigned during disposition. When that counter path reaches three, “search for that class” therefore supplies a non-slug with no defined mapping to the ledger class, so the required manual validation/search cannot proceed. Make the counter emit the assigned slug or explicitly resolve its candidate against the disposition ledger before searching.\n\nUseful? React with 👍\xa0/ 👎.', 'url': 'https://github.com/mryfmo/dotfiles/pull/328#discussion_r4250028600', 'resolved': False, 'outdated': False, 'disposition': 'fixed:a03c1daa'}
24 {'source': 'review_comment', 'author': 'chatgpt-codex-connector[bot]', 'bot': True, 'level': 'comment', 'path': 'home/dot_agents/skills/agmsg-orchestration/SKILL.md', 'line': 164, 'body': "**<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Use INV-10's 20-minute idle threshold**\n\nFor a seated worker that emits no task event for 20–29 minutes, this rule delays the bus read and PING even though `.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:64` explicitly limits worker idleness to 20 minutes. INV-10's 30-minute figure applies to the first-push deadline, not idle detection; align this sentence and the referenced `bus-read.sh` behavior with the 20-minute threshold.\n\nUseful? React with 👍\xa0/ 👎.", 'url': 'https://github.com/mryfmo/dotfiles/pull/328#discussion_r4257278271', 'resolved': False, 'outdated': True, 'disposition': 'fixed:e6602ca1'}
25 {'source': 'review_comment', 'author': 'chatgpt-codex-connector[bot]', 'bot': True, 'level': 'comment', 'path': 'home/dot_agents/skills/agmsg-orchestration/SKILL.md', 'line': 71, 'body': '**<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Define threat rows per concrete changed path**\n\nWhen an `allowed_files` entry is a permitted wildcard such as `scripts/orchestrator/*`, one generic row now satisfies the stated unit even if the PR changes several independently executable trust-boundary scripts. The existing T718 task demonstrates why the distinction matters: its single wildcard covers `dispatch.sh`, `three-repeat.sh`, and `bus-read.sh`, which require three different controls. Defining completeness per concrete changed file, or forbidding multi-file globs at trust boundaries, prevents a broad entry from hiding missing threat analysis.\n\nAGENTS.md reference: [AGENTS.md:L78-L78](https://github.com/mryfmo/dotfiles/blob/7771082f7db20a6ea1b53c5e95817aee6e23e177/AGENTS.md#L78-L78)\n\nUseful? React with 👍\xa0/ 👎.', 'url': 'https://github.com/mryfmo/dotfiles/pull/328#discussion_r4257278276', 'resolved': False, 'outdated': True, 'disposition': 'fixed:e6602ca1'}
26 {'source': 'review_comment', 'author': 'chatgpt-codex-connector[bot]', 'bot': True, 'level': 'comment', 'path': 'home/dot_agents/skills/agmsg-orchestration/SKILL.md', 'line': 69, 'body': '**<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Compare invariant sentences as well as IDs**\n\nFor an implementation task that carries the correct invariant IDs but weakens or replaces their text, this stop condition passes even though `.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:56` requires task invariants to equal the trusted design both as an ID set and byte-for-byte as sentences. Because the worker receives and follows the task copy, checking only IDs can dispatch work against a modified contract; require each invariant value to match the design in addition to matching the map entry.\n\nUseful? React with 👍\xa0/ 👎.', 'url': 'https://github.com/mryfmo/dotfiles/pull/328#discussion_r4257278283', 'resolved': False, 'outdated': True, 'disposition': 'fixed:e6602ca1'}
27 {'source': 'annotation', 'author': 'github-actions', 'bot': True, 'level': 'notice', 'path': '.github', 'line': 1, 'body': 'Due to capacity constraints, jobs targeting macOS arm64 runners may experience longer queue times.', 'url': 'https://github.com/mryfmo/dotfiles/actions/runs/38410198303/job/115340181995', 'check': 'private-bootstrap (macos-14, client)', 'disposition': 'not-applicable:runner capacity notice, no finding; evidence=gh run view 38410198303 --repo mryfmo/dotfiles --job 115340181995'}
28 {'source': 'annotation', 'author': 'github-actions', 'bot': True, 'level': 'notice', 'path': '.github', 'line': 1, 'body': 'Due to capacity constraints, jobs targeting macOS arm64 runners may experience longer queue times.', 'url': 'https://github.com/mryfmo/dotfiles/actions/runs/38410198303/job/115340181793', 'check': 'public-bootstrap (macos-14, client)', 'disposition': 'not-applicable:runner capacity notice, no finding; evidence=gh run view 38410198303 --repo mryfmo/dotfiles --job 115340181793'}
29 {'source': 'annotation', 'author': 'github-actions', 'bot': True, 'level': 'notice', 'path': '.github', 'line': 1, 'body': 'Due to capacity constraints, jobs targeting macOS arm64 runners may experience longer queue times.', 'url': 'https://github.com/mryfmo/dotfiles/actions/runs/38410197390/job/115340179776', 'check': 'test (macos-14, client)', 'disposition': 'not-applicable:runner capacity notice, no finding; evidence=gh run view 38410197390 --repo mryfmo/dotfiles --job 115340179776'}
30 {'source': 'status', 'author': 'coderabbitai[bot]', 'bot': True, 'level': 'success', 'path': None, 'line': None, 'body': 'CodeRabbit: Review skipped: automatic reviews are disabled', 'url': None, 'check': 'CodeRabbit', 'disposition': 'not-applicable:CI status, no finding; evidence=gh pr checks 328 --repo mryfmo/dotfiles'}

**Analyzing commit guard range issue**
exec
/bin/zsh -lc "rg -n 'fixed:|base.*head|rev-list|ancestor|disposition|ACCEPTANCE_EVIDENCE' scripts/require-crit-review.py | tail -55; git show --stat --oneline 95ba4e4c; git show --stat --oneline 8b1dbefc; git show --format=fuller --no-patch 65a3d71bf4e496252bf1ff51894974130c96cd43; git diff --numstat 4e7a9b3ae0a1a80f2c7664ea54e3244224a7a672 65a3d71bf4e496252bf1ff51894974130c96cd43 -- . ':"'!.orchestration'"'; git show 65a3d71bf4e496252bf1ff51894974130c96cd43:tests/unit/test_agmsg_orchestration_docs.py | sed -n '1,115p'; git show 65a3d71bf4e496252bf1ff51894974130c96cd43:home/dot_agents/skills/agmsg-orchestration/SKILL.md | nl -ba | sed -n '167,178p'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 190ms:
26:PR_FEEDBACK_DISPOSITION = re.compile(r"(?:fixed:(?P<commit>[0-9a-f]{7,40})|not-applicable:(?P<reason>.*\S.*))", re.S)
34:# Levels whose not-applicable disposition needs a concrete reason: failures and
360:def commit_in_range(root: Path, commit: str, base: str, head: str) -> bool:
361:    """Return whether commit is in base..head: reachable from head, not from base."""
363:        run_git(["merge-base", "--is-ancestor", commit, head], root).returncode == 0
364:        and run_git(["merge-base", "--is-ancestor", commit, base], root).returncode != 0
369:    """Check the filled pr-feedback.py JSON: every item needs a root-cause disposition."""
406:        disposition = item.get("disposition")
407:        match = PR_FEEDBACK_DISPOSITION.fullmatch(disposition) if isinstance(disposition, str) else None
409:            errors.append(f"{label} needs a disposition `fixed:<commit>` or `not-applicable:<reason>`")
418:            and not commit_in_range(root, commit, data["base_sha"], head)
475:def pr_base_errors(root: Path, evidence: dict, pr: int, head: str, base: str) -> list[str]:
532:        if run_git(["merge-base", "--is-ancestor", base_sha, github_base], root).returncode == 0:
533:            first_parents = run_git(["rev-list", "--first-parent", head], root)
537:        if run_git(["merge-base", "--is-ancestor", github_base, base_sha], root).returncode == 0:
538:            actual = run_git(["merge-base", base_sha, head], root)
539:            expected = run_git(["merge-base", github_base, head], root)
554:    required; when one exists it is collected and must be dispositioned like any
560:    errors = pr_base_errors(root, evidence, pr, head, base)
592:            f"{PR_FEEDBACK_ENV} lacks {sum(missing.values())} current feedback item(s) for PR #{pr}, e.g. {sample[0]}:{sample[2]} {sample[1]}; rerun scripts/pr-feedback.py and disposition them"
664:        return [f"{AUDIT_ENV} verdict is incorrect but {source} lists no [P0-P3] finding to disposition"]
665:    return audit_disposition_errors(root, findings)
668:def audit_disposition_errors(root: Path, findings: int) -> list[str]:
672:            f"{AUDIT_ENV} verdict is incorrect: {AUDIT_DISPOSITIONS_ENV} must name the acceptance record that dispositions its {findings} finding(s)"
696:            errors.append(f"{AUDIT_DISPOSITIONS_ENV} dispositions finding {finding} more than once: {line}")
703:                f"{AUDIT_DISPOSITIONS_ENV} line cites fixed:{match.group('commit')}; a fix moves HEAD, so audit the new head instead: {line}"
714:            f"{AUDIT_DISPOSITIONS_ENV} leaves audit finding(s) {', '.join(map(str, missing))} of {findings} without a disposition; add one `{AUDIT_FINDING_DISPOSITION_PREFIX} <n> … not-applicable:<reason>` line per finding, numbered in audit order"
763:    feedback_errors = pr_feedback_errors(root, required=args.base is not None, head=head, base=args.base)
765:        print("PR feedback evidence is incomplete; run scripts/pr-feedback.py and disposition every item.")
775:                " (set BASE=<ref> to bind it to HEAD, re-collect it, and check fixed: commits)"
95ba4e4c chore(orchestration): record the dotfiles-T128-playbook-rules-a02 task
 .../dotfiles-T128-playbook-rules-a02/task.md       | 90 ++++++++++++++++++++++
 1 file changed, 90 insertions(+)
8b1dbefc docs(regime): key the three-repeat search on the mistake records, qualify the invariant check
 home/dot_agents/skills/agmsg-orchestration/SKILL.md |  4 ++--
 tests/fixtures/regime/invariants.md                 |  4 ++--
 tests/unit/test_agmsg_orchestration_docs.py         | 20 ++++++++++++++------
 3 files changed, 18 insertions(+), 10 deletions(-)
commit 65a3d71bf4e496252bf1ff51894974130c96cd43
Author:     Fumio Moriya <moriya.fumio@technopro.com>
AuthorDate: Tue Oct 13 23:03:49 2026 +0900
Commit:     Fumio Moriya <moriya.fumio@technopro.com>
CommitDate: Tue Oct 13 23:03:49 2026 +0900

    chore(orchestration): dotfiles-T128-playbook-rules-a04 amendment 1 task copy and revise 1 evidence
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
1	1	AGENTS.md
6	4	home/dot_agents/skills/agmsg-orchestration/SKILL.md
1	1	tests/fixtures/regime/code-review-orchestration.md
4	2	tests/fixtures/regime/invariants.md
1	0	tests/fixtures/regime/orchestrator-step-6.md
121	1	tests/unit/test_agmsg_orchestration_docs.py
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RULES = ROOT / "home/dot_config/claude/rules"
RULE = RULES / "agmsg-orchestration.md"
SKILL = ROOT / "home/dot_agents/skills/agmsg-orchestration/SKILL.md"
# The always-loaded Claude rules; gpu.md, latex.md and python.md load only for matching paths.
ALWAYS_LOADED_RULES = (
    "agmsg-orchestration.md",
    "ask-user-question.md",
    "compactiondb.md",
    "crit-review.md",
    "model-selection.md",
    "ponytail.md",
    "pr-integration.md",
    "understand-anything.md",
)
PAIR_AUDIT = "herdr-agents --audit <head-sha> --task <id>"
HEADLESS_AUDIT = "codex <MODEL_PROFILE_AUDIT_CODEX_ARGS> exec --sandbox read-only -C <repo> -o <out>.last.md"


def words(path: Path) -> int:
    return len(path.read_text().split())


class AgmsgOrchestrationRuleTest(unittest.TestCase):
    """The rule carries the regime's invariants within its word budget; the SKILL carries the procedure."""

    def test_rule_states_the_invariants(self) -> None:
        text = RULE.read_text()
        for invariant in (
            "invoke the `agmsg-orchestration` skill",
            "Only the operator opts out",
            "is never an implicit opt-out",
            "Every repository mutation goes to a seated worker of the manifest's `worker_kind`",
            "or after the operator's explicit opt-out for the current task",
            "`make require-crit-review` stay with the orchestrator and are never delegated",
            "one task-level audit of its final head",
            "AGMSG-PONG v1 status=blocked",
            "except the few commands Worker Playbook step 4 sends through the permission gate",
            "Agent-to-agent permission approval is forbidden",
            "never pushes a repository change to `main` directly",
            "gh pr merge --squash",
            "--match-head-commit <audited head sha>",
            "AGMSG_RESOLVE_PROJECT=0 join.sh <team> <name> <type> <worktree>",
            "pairwise-disjoint",
            "disjoint code tasks run concurrently while overlapping code files run serially",
            "gh pr update-branch",
            "never edits the source of its own execution boundary",
            "make check-regime-boundary",
            # Pinned registration and wake tokens; their procedure is in the SKILL.
            "agmsg-dispatch",
            "poke.sh",
            "send.sh",
            "--body-file",
            "inbox.sh",
            "exit 13",
        ):
            with self.subTest(invariant=invariant):
                self.assertIn(invariant, text)

    def test_rule_pointers_name_real_skill_sections(self) -> None:
        rule = RULE.read_text()
        skill = SKILL.read_text()
        # Quoted capitalised names are SKILL headings, except the task-level audit bullet checked below.
        for heading in set(re.findall(r'"([A-Z][^"]+)"', rule)) - {"Task-level audit"}:
            with self.subTest(heading=heading):
                self.assertIn(f"\n## {heading}\n", skill)
        playbooks = {
            "Orchestrator": skill.split("## Orchestrator Playbook", 1)[1].split("\n## ", 1)[0],
            "Worker": skill.split("## Worker Playbook", 1)[1].split("\n## ", 1)[0],
        }
        for playbook, step in re.findall(r"(Orchestrator|Worker) Playbook step (\d+)", rule):
            with self.subTest(playbook=playbook, step=step):
                self.assertRegex(playbooks[playbook], rf"(?m)^{step}\. ")
        self.assertIn('the "Task-level audit" bullet', rule)
        self.assertIn("\n- Task-level audit:", skill)

    def test_word_budgets(self) -> None:
        self.assertLessEqual(words(RULE), 450)
        self.assertLessEqual(sum(words(RULES / name) for name in ALWAYS_LOADED_RULES), 1800)


class AgmsgOrchestrationSkillTest(unittest.TestCase):
    """The SKILL holds the mechanics the rule points at."""

    def test_claude_worker_merge_denials_and_prefix_limits_are_documented(self) -> None:
        for path in (ROOT / "README.md", SKILL):
            text = " ".join(path.read_text().split())
            with self.subTest(path=path.name):
                for token in (
                    "Bash(gh pr merge:*)",
                    "Bash(gh api -X PUT:*)",
                    "Bash(gh api --method PUT:*)",
                    "Bash(gh api graphql:*)",
                    "herdr-agents",
                    ".claude/settings.local.json",
                    "deny rules",
                    "nested subcommands",
                    "permission mode",
                    "flag after the path",
                    "integration gate",
                    "https://code.claude.com/docs/en/permissions",
                ):
                    self.assertIn(token, text)
                self.assertNotIn("Claude worker seats have no such denial yet", text)
                self.assertNotIn("Claude seats get their deny rules in a separate task", text)

    def test_skill_carries_the_registration_and_delivery_mechanics(self) -> None:
        text = SKILL.read_text()
        for token in (
            "AGMSG_RESOLVE_PROJECT=0 join.sh <team> <name> <type> <worktree>",
            "poke.sh",
   167	9. For a RESULT carrying `effects`, verify that every declared effect has the report's stated reverse mapping before acceptance; record any irreversible effect in the acceptance note.
   168	10. For a RESULT that carries a pull request, integrate in this order. This is the single procedure that the PR integration rule, `AGENTS.md`, the README and the gh-first-workflow skill cite. A `gh pr update-branch` moves the head, so steps 1 to 4 run again on the new head. After an update-branch the orchestrator runs it, the order is CI on the new head, then the sweep, then the audit; an audit started before CI finishes sees incomplete evidence and returns an evidence-only `incorrect`. Select a checkout with git -C <absolute path>, never with cd, which the sandboxed Bash may not honour. After moving the review worktree to the audited head, verify git -C <review> rev-parse HEAD equals that head and git -C <main> symbolic-ref --short HEAD prints main before the audit and the gate.
   169	    1. Sweep the final head's feedback with `scripts/pr-feedback.py <pr> --json .orchestration/validation/<task>-pr-feedback.json` and give every item a `fixed:<commit>` or `not-applicable:<reason>` disposition, leaving none on `failure` or `warning` annotations. Optionally request `@coderabbitai full review` on the final head first; when a CodeRabbit review exists it is swept like any other item, and the gate does not require a bot review. An `open:<thread id>` item from a worker's third Bot round is a sweep item like any other: it becomes `fixed:<sha>` through a revise round that carries its `check=` (a round that counts toward INV-6 like any other), or `not-applicable:<reason>` with a pasted refutation; until one of those exists the PR is not merged, never with the thread open.
   170	    2. Run the task-level audit of that head in the pair or headless form of the task-level audit bullet. It exits nonzero for every verdict other than `correct`. An exit with `Audit verdict: incorrect` is not a failed step: continue to step 3 and disposition its findings. A `blocked` or missing verdict means re-running the audit.
   171	    3. Write the acceptance record, summarising the dispositions, with an `audit-finding:` line for every audit finding whatever the verdict (the gate needs them, through `AUDIT_DISPOSITIONS`, when it is `incorrect`).
   172	    4. Run the gate: `AUDIT_EVIDENCE=<audit> [AUDIT_DISPOSITIONS=<acceptance record>] AGENT_REVIEWED=1 REVIEW_EVIDENCE=<receipt> ACCEPTANCE_EVIDENCE=<acceptance record> BASE=origin/main PR_FEEDBACK_EVIDENCE=<json> make require-crit-review`.
   173	       - A `review` sweep item whose body carries a `P0`–`P3` badge is a finding with its own `fixed:<commit>` or `not-applicable:<reason>` disposition, never a container for its inline threads.
   174	       - The sweep covers issue comments, reviews, inline review comments with thread resolution, non-passing check runs, check-run annotations at every level (`notice`, `warning`, `failure`), and commit statuses. A `failure` marked `not-applicable` needs a concrete reason of at least 20 characters.
   175	       - A CodeRabbit full review is optional, at most once on the final head: the plan allows one review per hour and every review event spends one (docs.coderabbit.ai/management/rate-limits).
   176	       - The feedback JSON may be masked with `uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets`, which masks its keys and string values; the gate identifies an item by its source, url, level, path, line and body, and accepts a body or path that is verbatim or exactly that masked form.
   177	       - The gate rejects evidence outside `.orchestration/validation/` or without the `-pr-feedback.json` suffix. It binds `BASE` to the PR's GitHub base before running the collector from that authenticated SHA: an older base must be outside HEAD's first-parent chain, an advanced base must preserve the merge-base with the PR head, and PR branch commits (including `HEAD`) cannot substitute for the base. Evidence must match the local GitHub repository independently of `GH_REPO`, and `fixed:` commits must be in the authenticated GitHub base-to-head range whatever `BASE` is selected.
   178	       - `AUDIT_EVIDENCE` must be the task-level file `.orchestration/validation/<task>-audit-<sha7>.md` (the same `<task>` as the feedback JSON); a per-commit `audit-<sha>.md` is rejected. Its verdict comes only from the non-empty `<file>.last.md` and must be `correct`, or `incorrect` with `AUDIT_DISPOSITIONS`. PRs that change only `.orchestration/` files need no audit.

**Clarifying disposition and audit rules**
**Reviewing residual findings and running read-only tests**
exec
/bin/zsh -lc "python3 -B -c 'import json,subprocess,pathlib,hashlib,re
base='\\''4e7a9b3ae0a1a80f2c7664ea54e3244224a7a672'\\''; head='\\''65a3d71bf4e496252bf1ff51894974130c96cd43'\\''
def git(*a):return subprocess.check_output(['\\''git'\\'',*a],text=True)
d=json.loads(pathlib.Path('\\''.orchestration/validation/dotfiles-T128-playbook-rules-a04-pr-feedback.json'\\'').read_text())
for x in d['\\''items'\\'']:
 disp=x['\\''disposition'\\'']
 if disp.startswith('\\''fixed:'\\''):
  c=disp[6:];a=subprocess.run(['\\''git'\\'','\\''merge-base'\\'','\\''--is-ancestor'\\'',c,head]).returncode;b=subprocess.run(['\\''git'\\'','\\''merge-base'\\'','\\''--is-ancestor'\\'',c,base]).returncode
  print(x['\\''url'\\''].rsplit('\\''_'\\'',1)[-1],disp,'\\''head_ancestor'\\'',a==0,'\\''base_ancestor'\\'',b==0,'\\''eligible'\\'',a==0 and b"'!=0)
for ver in ('"'\\''a01'\\'','\\''a02'\\'','\\''a03'\\'','\\''a04'\\''):
 p=f'\\''.orchestration/dotfiles-T128-playbook-rules-{ver}/task.md'\\'';data=git('\\''show'\\'',head+'\\'':'\\''+p).encode();s=pathlib.Path(f'\\''.orchestration/tasks/dotfiles-T128-playbook-rules-{ver}.md'\\'').read_bytes();print(ver,'\\''task SHA'\\'',hashlib.sha256(data).hexdigest(),'\\''equals main task'\\'',data==s)
for file in ('\\''report.md'\\'','\\''validation.md'\\'','\\''sandbox.md'\\''):
 p='\\''.orchestration/dotfiles-T128-playbook-rules-a04/'\\''+file;data=git('\\''show'\\'',head+'\\'':'\\''+p);print(p,'\\''\\n'\\''+data[-2300:])
'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 792ms:
r4247933544 fixed:95ba4e4c head_ancestor True base_ancestor False eligible True
r4247933561 fixed:8b1dbefc head_ancestor True base_ancestor False eligible True
r4247933574 fixed:8b1dbefc head_ancestor True base_ancestor False eligible True
r4248319926 fixed:e12872cd head_ancestor True base_ancestor False eligible True
r4248319936 fixed:4b62feda head_ancestor True base_ancestor False eligible True
r4248711363 fixed:f40e530a head_ancestor True base_ancestor False eligible True
r4248711371 fixed:f40e530a head_ancestor True base_ancestor False eligible True
r4249303398 fixed:beee078a head_ancestor True base_ancestor False eligible True
r4249303413 fixed:beee078a head_ancestor True base_ancestor False eligible True
r4249303426 fixed:beee078a head_ancestor True base_ancestor False eligible True
r4249303433 fixed:beee078a head_ancestor True base_ancestor False eligible True
r4250028600 fixed:a03c1daa head_ancestor True base_ancestor True eligible False
r4257278271 fixed:e6602ca1 head_ancestor True base_ancestor False eligible True
r4257278276 fixed:e6602ca1 head_ancestor True base_ancestor False eligible True
r4257278283 fixed:e6602ca1 head_ancestor True base_ancestor False eligible True
a01 task SHA b035ebd79add64b0cd9977e154b30746757d64782e65089541a79627b1020c0d equals main task False
a02 task SHA 07b78f643bc5a488614bca59d195d45da93defb7d7c0acf5fc8a4820e00f4f33 equals main task True
a03 task SHA ee6385184e3db246df45970bf71862525d5fd990aa41f92b2b9d03654d45adb2 equals main task True
a04 task SHA c5dbc2c3d3514707870c2146ac4acfd6e96279d50f0f6bf04bd8921cd242a6fa equals main task True
.orchestration/dotfiles-T128-playbook-rules-a04/report.md 
rchestrator's line lifted the operator's 10:36Z stop and superseded TASK 935. The branch fast-forwarded to the remote head `7771082f`, merged `origin/main` (`4e7a9b3a`) in `87bce51e`, and the task copy now matches the amended file byte for byte (validation §9). `e6602ca1` puts the amended sentences of items 1, 4 and 5 in the SKILL verbatim, as the task file quotes them (§9 checks all three):

| Thread | Finding | Disposition |
|---|---|---|
| 4257278283 (P1) | the invariant check compared ids only | `fixed:e6602ca1`. Each invariant's sentence equals the design's byte for byte, the design read from main (INV-2), by hand until a checker lands. Test: `test_task_file_review_is_one_round_with_a_fixed_stop_condition` (P4) |
| 4257278271 (P2) | step 6 used thirty minutes as INV-10's figure | `fixed:e6602ca1`. A seated worker idle for 20 minutes (INV-10's idle figure; 30 minutes is the first-push deadline). The orchestrator applies it to the minutes `bus-read.sh` prints. Test: `test_dispatches_are_recorded_from_the_bus` (P2) |
| 4257278276 (P2) | the row unit had no rule for a wildcard entry | `fixed:e6602ca1`. One row per concrete changed file under an executed or applied wildcard entry; a data wildcard keeps one row. Test: `test_threat_table_rows_have_a_fixed_unit` (P3) |
| local review of `7771082f`, finding 1 | "a complete bus read", which the merged script does not do | `fixed:e6602ca1`. The read is refused when it reaches its limit, and the orchestrator raises `BUS_READ_LIMIT` and reads again. Test: `test_dispatches_are_recorded_from_the_bus` (P1) |

- Declared fixture changes (INV-12): `tests/fixtures/regime/invariants.md` (the task-file-review and threat-table bullets) and `tests/fixtures/regime/orchestrator-step-6.md` (step 6). `test_regime_rule_sections_are_pinned_whole` fails on a changed fixture (P5).
- The `test_dispatches_are_recorded_from_the_bus` stale list also refuses `complete bus read` and `silent for thirty minutes`.
- Results (§9): 47 docs tests OK; Prettier and ruff clean; 5 mutants, 5 failures. Size: 6 files outside `.orchestration/`; added lines outside and under `tests/`: 7 and 127.
- The orchestrator's line says the Bot reviews on PR open only now, so there is no Bot wait; the pushed head's CI is in the RESULT and in the main-checkout copy.

.orchestration/dotfiles-T128-playbook-rules-a04/validation.md 
ce its latest bus event for[568 chars]ge).' != '6. S[2911 chars] for 30 minutes since its latest bus event f
$ git diff --numstat origin/main...HEAD
3	0	.orchestration/dotfiles-T128-playbook-rules-a01/autoskill.md
7	0	.orchestration/dotfiles-T128-playbook-rules-a01/learning.md
49	0	.orchestration/dotfiles-T128-playbook-rules-a01/report.md
26	0	.orchestration/dotfiles-T128-playbook-rules-a01/sandbox.md
84	0	.orchestration/dotfiles-T128-playbook-rules-a01/task.md
220	0	.orchestration/dotfiles-T128-playbook-rules-a01/validation.md
3	0	.orchestration/dotfiles-T128-playbook-rules-a02/autoskill.md
7	0	.orchestration/dotfiles-T128-playbook-rules-a02/learning.md
71	0	.orchestration/dotfiles-T128-playbook-rules-a02/report.md
26	0	.orchestration/dotfiles-T128-playbook-rules-a02/sandbox.md
90	0	.orchestration/dotfiles-T128-playbook-rules-a02/task.md
362	0	.orchestration/dotfiles-T128-playbook-rules-a02/validation.md
3	0	.orchestration/dotfiles-T128-playbook-rules-a03/autoskill.md
6	0	.orchestration/dotfiles-T128-playbook-rules-a03/learning.md
53	0	.orchestration/dotfiles-T128-playbook-rules-a03/report.md
21	0	.orchestration/dotfiles-T128-playbook-rules-a03/sandbox.md
92	0	.orchestration/dotfiles-T128-playbook-rules-a03/task.md
183	0	.orchestration/dotfiles-T128-playbook-rules-a03/validation.md
3	0	.orchestration/dotfiles-T128-playbook-rules-a04/autoskill.md
6	0	.orchestration/dotfiles-T128-playbook-rules-a04/learning.md
55	0	.orchestration/dotfiles-T128-playbook-rules-a04/report.md
21	0	.orchestration/dotfiles-T128-playbook-rules-a04/sandbox.md
94	0	.orchestration/dotfiles-T128-playbook-rules-a04/task.md
183	0	.orchestration/dotfiles-T128-playbook-rules-a04/validation.md
1	1	AGENTS.md
6	4	home/dot_agents/skills/agmsg-orchestration/SKILL.md
1	1	tests/fixtures/regime/code-review-orchestration.md
4	2	tests/fixtures/regime/invariants.md
1	0	tests/fixtures/regime/orchestrator-step-6.md
121	1	tests/unit/test_agmsg_orchestration_docs.py
$ git diff --numstat origin/main...HEAD | awk '$3 !~ /^\.orchestration\// {f++} $3 !~ /^\.orchestration\// && $3 !~ /^tests\// {o+=$1} $3 ~ /^tests\// {t+=$1} END {print "files outside .orchestration/:", f, "added outside tests/:", o, "added under tests/:", t}'
files outside .orchestration/: 6 added outside tests/: 7 added under tests/: 127
```

.orchestration/dotfiles-T128-playbook-rules-a04/sandbox.md 
---
task_id: dotfiles-T128-playbook-rules-a04
seat: claude-standard-dot-a003
permission_gated_commands: 11
---

# Sandbox record: dotfiles-T128-playbook-rules-a04

- Period: from the AGMSG-TASK (2026-10-12T15:40:52Z) to the RESULT. These ran inside the sandbox: the fetch of the branch over public HTTPS and the fast-forward to `e12872cd`, the `history.sh` premise runs, the edits, fixture generation, the tests, ruff, the verbatim check, the mutation proofs, and the commits.

`permission_gated_commands` counts every Bash call made with `dangerouslyDisableSandbox`, one per call. This copy was written before #2, so #2 to #7 are counted in advance; the main-checkout copy gives the final count. The PR is already ready, so there is no `gh pr ready`.

| # | Command | Step 4 case |
|--:|---|---|
| 1 | main-checkout `memory add` | main-checkout `memory add` |
| 2 | the HTTPS push | `git push` |
| 3 | `gh pr checks 328 --watch` (background, exit status joined) | `gh` |
| 4 | Bot wait from the push | `gh` |
| 5 | reading the Bot review and the check runs of the final head | `gh` |
| 6 | the masked copy of the five evidence files to the main checkout | artifact copy with the repository masker |
| 7 | `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T128-playbook-rules-a04 …` | `agmsg-dispatch` |
| 8 | the revise round's HTTPS push | `git push` |
| 9 | `gh pr checks 328 --watch` on the revise head | `gh` |
| 10 | the masked copy of the evidence files to the main checkout | artifact copy with the repository masker |
| 11 | `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T128-playbook-rules-a04 revise=1 …` | `agmsg-dispatch` |

Revise round 1 (amendment 1): #8 to #11 are counted in advance in this copy; there is no Bot wait (the orchestrator's line of 13:57:09Z).


exec
/bin/zsh -lc "sed -n '354,432p' scripts/require-crit-review.py; rg -n 'fixed:a03c1daa|4250028600|local-finding|audit-input' .orchestration/validation/dotfiles-T128-playbook-rules-a04-pr-feedback.json .orchestration/acceptance/dotfiles-T128-playbook-rules-a04.md; git show 65a3d71bf4e496252bf1ff51894974130c96cd43:tests/unit/test_agmsg_orchestration_docs.py | tail -95" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 6ms:
        )
    if not has_review_record:
        errors.append(f"{CRIT_DATA_SOURCE_FIELD} requires a review-scope or path-bound line/file comment")
    return errors


def commit_in_range(root: Path, commit: str, base: str, head: str) -> bool:
    """Return whether commit is in base..head: reachable from head, not from base."""
    return (
        run_git(["merge-base", "--is-ancestor", commit, head], root).returncode == 0
        and run_git(["merge-base", "--is-ancestor", commit, base], root).returncode != 0
    )


def pr_feedback_errors(root: Path, required: bool, head: str | None = None, base: str | None = None) -> list[str]:
    """Check the filled pr-feedback.py JSON: every item needs a root-cause disposition."""
    evidence = os.environ.get(PR_FEEDBACK_ENV, "").strip()
    if not evidence:
        if required:
            return [f"{PR_FEEDBACK_ENV} must point to the filled scripts/pr-feedback.py JSON for PR integration"]
        return []
    path = Path(evidence)
    if not path.is_absolute():
        path = root / path
    path_error = feedback_path_error(root, path)
    if path_error:
        return [path_error]
    if not path.is_file():
        return [f"{PR_FEEDBACK_ENV} file does not exist: {path}"]
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as error:
        return [f"{PR_FEEDBACK_ENV} must be valid JSON: {error}"]
    items = data.get("items") if isinstance(data, dict) else None
    if not isinstance(items, list):
        return [f"{PR_FEEDBACK_ENV} must be a pr-feedback.py document with an items list"]

    errors: list[str] = []
    if head is not None and data.get("head_sha") != head:
        errors.append(
            f"{PR_FEEDBACK_ENV} was collected for head {data.get('head_sha')!r}, not the current HEAD {head}; rerun scripts/pr-feedback.py"
        )
    if head is not None and base is not None:
        errors.extend(collected_feedback_errors(root, data, head, base))
        if errors:
            return errors
    for index, item in enumerate(items):
        label = f"{PR_FEEDBACK_ENV} item {index}"
        if not isinstance(item, dict):
            errors.append(f"{label} must be an object")
            continue
        label += f" ({item.get('source')}:{item.get('level')} {item.get('url') or ''})".rstrip()
        disposition = item.get("disposition")
        match = PR_FEEDBACK_DISPOSITION.fullmatch(disposition) if isinstance(disposition, str) else None
        if not match:
            errors.append(f"{label} needs a disposition `fixed:<commit>` or `not-applicable:<reason>`")
            continue
        commit = match.group("commit")
        if commit and run_git(["cat-file", "-e", f"{commit}^{{commit}}"], root).returncode != 0:
            errors.append(f"{label} cites an unknown commit: {commit}")
        elif (
            commit
            and head is not None
            and base is not None
            and not commit_in_range(root, commit, data["base_sha"], head)
        ):
            errors.append(
                f"{label} cites commit {commit} outside GitHub base {data['base_sha']}..HEAD; cite the fix commit in this PR"
            )
        reason = (match.group("reason") or "").strip()
        if item.get("level") in STRICT_REASON_LEVELS and not commit and len(reason) < FAILURE_REASON_MIN_CHARS:
            errors.append(
                f"{label} is {item.get('level')}-level; not-applicable needs a reason of at least {FAILURE_REASON_MIN_CHARS} characters"
            )
    return errors


@cache
def validator():
.orchestration/validation/dotfiles-T128-playbook-rules-a04-pr-feedback.json:363:      "url": "https://github.com/mryfmo/dotfiles/pull/328#discussion_r4250028600",
.orchestration/validation/dotfiles-T128-playbook-rules-a04-pr-feedback.json:366:      "disposition": "fixed:a03c1daa"
.orchestration/acceptance/dotfiles-T128-playbook-rules-a04.md:9:- 2026-10-12 16:04:45Z RESULT (bus 779): `status=ready_for_review head=2276a365`; CI 12 green; the worker's four a03 threads `fixed:beee078a`. 16:03:26Z Bot review 5493270947 on 2276a365: thread 4250028600 P1 (`SKILL.md:74`: the counters' S1 candidate is review-title text, the rule wants a slug). Class at disposition time: `search-procedure` (also `unlanded-mechanism-stated-as-present`), the next row after the third S1 cycle → S7, plan 012; M-20261012-23 / C-25. Counters 16:07:36Z: `tasks=1 amendments=0 questions=0 results=1 withdrawn=0 revises=0`.
.orchestration/acceptance/dotfiles-T128-playbook-rules-a04.md:10:- 2026-10-13 01:05Z operator: plan 012 option B. No ACCEPTANCE line to the worker yet: a04 is held unchanged until `dotfiles-T128-orchestrator-tools-a01` (T718's first slice: counters slug, three-repeat.sh, bus-read.sh, dispatch.sh) merges; then `gh pr update-branch 328`, Bot, sweep (4250028600 → `fixed:<T718 squash sha>`), audit, gate. The worker a003 takes T718 on a fresh branch meanwhile (its worktree keeps `regime/playbook-rules`).
.orchestration/acceptance/dotfiles-T128-playbook-rules-a04.md:12:- 01:45Z ACCEPTANCE sent to a003 (bus 809, created 01:48:18Z): `status=accepted` (head 2276a365 is the final text under plan 012 B; thread 4250028600 closes when T718 a01 lands; integration by the orchestrator after that merge; no worker action on a04). Sent because the Stop gate requires one ACCEPTANCE per RESULT and the deliverable itself needs no change.
.orchestration/acceptance/dotfiles-T128-playbook-rules-a04.md:59:4250028600	search-procedure
.orchestration/acceptance/dotfiles-T128-playbook-rules-a04.md:67:local-finding: 7771082:1 fixed:e6602ca1 (local review of 7771082f, SKILL.md:164: the read refused at its limit, never a default-limited or silently truncated one)
.orchestration/acceptance/dotfiles-T128-playbook-rules-a04.md:73:local-finding: 65a3d71:1 not-applicable:P1 by the post-round local review (SKILL.md:164: the rule requires dispatch logging into the current acceptance record and the tools refuse a missing record, but no sentence says the orchestrator creates the record before the first dispatch); plan 021 S21: the local review is a sampler and not the acceptance authority, so this finding is referred as input to the audit of this head, which decides; if the audit raises it as P0/P1 the PR stops (plan 020 step 4.2), otherwise it is advisory and owned by dotfiles-T128-playbook-rules-followup-a01; evidence=sed -n 1,20p .orchestration/validation/dotfiles-T128-playbook-rules-a04-local-review-65a3d71.md
    POINTERS = (
        ROOT / "AGENTS.md",
        ROOT / "README.md",
        RULE,
        RULES / "model-selection.md",
        RULES / "pr-integration.md",
        ROOT / "home/dot_config/codex/AGENTS.md",
        ROOT / "home/dot_agents/skills/gh-first-workflow/SKILL.md",
    )

    def test_audit_command_lives_only_in_the_task_level_audit_bullet(self) -> None:
        skill = SKILL.read_text()
        bullet = skill.split("\n- Task-level audit:", 1)[1].split("\n- ", 1)[0]
        for command in (PAIR_AUDIT, HEADLESS_AUDIT):
            with self.subTest(command=command):
                self.assertEqual(skill.count(command), 1)
                self.assertIn(command, bullet)
                for path in self.POINTERS:
                    with self.subTest(path=path.name):
                        self.assertNotIn(command, path.read_text())
        for path in self.POINTERS:
            with self.subTest(path=path.name):
                self.assertNotIn("exec --sandbox read-only", path.read_text())

    def test_codex_agents_points_at_the_worklog_section(self) -> None:
        codex = (ROOT / "home/dot_config/codex/AGENTS.md").read_text()
        self.assertIn("「Codex seat worklogs」", codex)
        self.assertIn("\n## Codex seat worklogs\n", SKILL.read_text())

    def test_skill_masks_evidence_with_a_runnable_command(self) -> None:
        # The validator is not executable (mode 100644), so the SKILL names it only through uv run.
        text = SKILL.read_text()
        runnable = "`uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets"
        self.assertGreaterEqual(text.count(runnable), 3)
        self.assertEqual(text.count("scripts/validate-agent-assets.py --mask-secrets"), text.count(runnable))

    def test_contextdb_cli_is_invoked_with_uv_run(self) -> None:
        paths = [
            ROOT / "CLAUDE.md",
            ROOT / "AGENTS.md",
            SKILL,
            ROOT / "home/dot_config/codex/AGENTS.md",
            *sorted(RULES.glob("*.md")),
        ]
        for path in paths:
            text = path.read_text()
            with self.subTest(path=path.name):
                self.assertNotIn("python3 .claude/hooks/contextdb_cli.py", text)
                # Without --no-project, uv would create or sync the target project's environment first.
                self.assertNotIn("uv run .claude/hooks/contextdb_cli.py", text)
        for path in (ROOT / "CLAUDE.md", SKILL, RULES / "compactiondb.md", ROOT / "home/dot_config/codex/AGENTS.md"):
            with self.subTest(path=path.name):
                self.assertIn("uv run --no-project .claude/hooks/contextdb_cli.py", path.read_text())


class AgmsgOrchestrationForbiddenPhrasesTest(unittest.TestCase):
    def test_docs_no_longer_name_codex_review_commit(self) -> None:
        for path in (
            ROOT / "AGENTS.md",
            ROOT / "README.md",
            RULE,
            SKILL,
            RULES / "model-selection.md",
        ):
            text = path.read_text()
            lines = [line for line in text.splitlines() if "review --commit" in line]
            with self.subTest(path=path.name):
                self.assertNotIn("audit review --commit", text)
                # README keeps one sentence explaining why `codex review --commit` is not used.
                self.assertEqual(
                    [line for line in lines if not line.startswith("`codex review --commit` is not used")], []
                )

    def test_rule_and_skill_name_worker_seats_not_codex_workers(self) -> None:
        # The worker kind comes from the manifest; model-selection.md's security-profile sentence is exempt.
        for path in (RULE, SKILL):
            with self.subTest(path=path.name):
                self.assertNotIn("Codex worker", path.read_text())

    def test_rule_drops_the_worker_network_escalation(self) -> None:
        self.assertNotIn("network access stays off", RULE.read_text())

    def test_skill_drops_the_pane_status_gate_and_raw_pane_wakes(self) -> None:
        text = SKILL.read_text()
        for stale in (
            "isn't already `working`",
            "wake or prompt a worker with `herdr pane run",
            "upstream's own default) and Claude Code",
        ):
            with self.subTest(stale=stale):
                self.assertNotIn(stale, text)


if __name__ == "__main__":
    unittest.main()

**Confirming safe test execution**
exec
/bin/zsh -lc "git worktree list --porcelain; rg --files .orchestration/validation | rg 'playbook-rules-a04.*(local|crit|review)|regime-v3-a01-design-review-round22'; git show 65a3d71bf4e496252bf1ff51894974130c96cd43:.orchestration/dotfiles-T128-playbook-rules-a01/report.md; git show 65a3d71bf4e496252bf1ff51894974130c96cd43:.orchestration/dotfiles-T128-playbook-rules-a02/report.md; git show 65a3d71bf4e496252bf1ff51894974130c96cd43:.orchestration/dotfiles-T128-playbook-rules-a03/report.md" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc "rg -n '017|020|021' .orchestration/plans --glob '*.md' -l | tail -20; rg -n 'R1|scope|4250028600|residual' .orchestration/acceptance/dotfiles-T128-orchestrator-tools-a04.md; nl -ba .orchestration/tasks/dotfiles-T128-regime-v3-a01.md | sed -n '126,198p'; git show 65a3d71bf4e496252bf1ff51894974130c96cd43:tests/unit/test_agmsg_orchestration_docs.py | sed -n '115,275p'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 138ms:
worktree ~/Workspace/dotfiles
HEAD 4e7a9b3ae0a1a80f2c7664ea54e3244224a7a672
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
HEAD 4e7a9b3ae0a1a80f2c7664ea54e3244224a7a672
detached

worktree ~/Workspace/dotfiles/.claude/worktrees/worker-c
HEAD 1287af3435e4847ef819e43972b0da4bfe156e60
branch refs/heads/tools/orchestrator-scripts-2

worktree ~/Workspace/dotfiles/.claude/worktrees/worker-d
HEAD 4f9627ac316cacd879dfe08f0269f4205946dac0
branch refs/heads/receipt/canonical

worktree ~/Workspace/dotfiles/.claude/worktrees/worker-e
HEAD 61c8e7dae099410ac40aa3cad4020467bb116b04
branch refs/heads/feat/npm-provenance-and-claude-channel

worktree ~/Workspace/dotfiles/.claude/worktrees/worker-f
HEAD 2239c2eb3f7000155224e3b29c2556d9536e423f
branch refs/heads/regime/gate-evidence

.orchestration/validation/dotfiles-T128-playbook-rules-a04-amend-review-a01.md
.orchestration/validation/dotfiles-T128-playbook-rules-a04-local-review-7771082.md
.orchestration/validation/dotfiles-T128-playbook-rules-a04-amend-review-a01-codex.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22-codex.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
.orchestration/validation/dotfiles-T128-playbook-rules-a04-amend-review-a01-codex-r2.md
# Report: dotfiles-T128-playbook-rules-a01

- Seat: `claude-standard-dot-a003` in `.claude/worktrees/worker-c`, branch `regime/playbook-rules` from `origin/main` `683384ea`, draft PR #328.
- Task file sha256 `b035ebd7…` matches the TASK's `task_sha256` and is copied byte-identical in `1083a8c1` to `.orchestration/dotfiles-T128-playbook-rules-a01/task.md` (validation §1). The four premises hold on `origin/main` (validation §2).

## Commit `0158b866`: items 1 to 7

| Item | Where | Change | Test |
|---|---|---|---|
| 1 | SKILL Orchestrator Playbook step 6 | the two dispatch-evidence sentences appended verbatim | `test_dispatches_are_recorded_from_the_bus` (one subTest per sentence) |
| 2 | SKILL invariants, after the counters bullet | the amendment bullet, verbatim | `test_rule_changes_travel_as_task_amendments` |
| 3 | SKILL invariants, after item 2's bullet | the three-repeat bullet, verbatim | `test_three_repeats_start_with_a_pasted_correction_search` (one subTest per sentence) |
| 4 | SKILL threat-table bullet, after "…metadata separators)."; `AGENTS.md` line 78 after "report a missing table or a missing row;" | the row-unit sentence and the AGENTS.md clause, verbatim | `test_threat_table_rows_have_a_fixed_unit` (both files) |
| 5 | SKILL task-file-review bullet | the clause replaced verbatim | `test_task_file_review_is_one_round_with_a_fixed_stop_condition`: the line-278 token is now the new clause, plus `assertNotIn("-contract-a01")` |
| 6 | SKILL step 10.4 | `ACCEPTANCE_EVIDENCE=<acceptance record>` in the gate command | `test_the_gate_reads_the_acceptance_record` |
| 7 | `PINNED_SECTIONS` | new row `orchestrator-step-6` (`("## Orchestrator Playbook", "\n## ")`, `("\n6. ", "\n7. ")`, the step-7 row's shape) | `test_regime_rule_sections_are_pinned_whole` |

Item 6's placement: the variable sits right after `REVIEW_EVIDENCE=<receipt>`, before `BASE=origin/main`, not directly after `PR_FEEDBACK_EVIDENCE=<json>`. `tests/unit/test_pr_feedback.py` `PrIntegrationRuleParityTest.GATE` pins `BASE=origin/main PR_FEEDBACK_EVIDENCE=<json> make require-crit-review` as one substring that appears once in the SKILL, and that module is outside `allowed_files`. Any position after `BASE=` breaks it; this one keeps it green without editing the module (validation §4). The item's parenthetical (required in PR mode once `dotfiles-T128-gate-evidence-a01` lands; what the gate reads) is the task's rationale, so it was not added as rule text. When gate-evidence-a01 lands, it either keeps this order or edits `GATE` within its own `allowed_files`.

## Declared fixture changes (INV-12)

- `tests/fixtures/regime/orchestrator-step-6.md`: new; step 6 is pinned whole.
- `tests/fixtures/regime/invariants.md`: items 2, 3, 4 and 5.
- `tests/fixtures/regime/code-review-orchestration.md`: item 4's AGENTS.md clause.

All three were generated by the test's own `section` and `normalized` logic from the edited prose, not transcribed, and `test_regime_rule_sections_are_pinned_whole` passes on them (validation §3). `worker-step-15.md`, `message-contract.md` and `orchestrator-step-7.md` are unchanged (validation §10).

## Results

- Docs module: 47 tests, OK (validation §3). `test_pr_feedback.py`: 16 tests, OK, and the pinned gate substring still appears once (§4). `ruff format --check`: clean (§5).
- Every new sentence fails its test when removed: 11 mutants, 11 failures, tree restored (§6). That covers both item-1 sentences, all three item-3 sentences, both item-4 files, item 5's old clause pasted back, item 6's variable, and one word of step 6 against the new fixture.
- Item 8: every SKILL hunk lands in the invariants or the Orchestrator Playbook; the counters bullet hashes the same as on `main` (§10).
- Size (§7): 6 changed files outside `.orchestration/`; 7 added lines outside `tests/` (cap 500); 78 under `tests/` (cap 1000).

## Not done, or outside scope

- `tests/unit/test_regime_counters.py` and `tests/unit/test_require_crit_review.py` were not run locally: `--with pyyaml` needs PyPI, which the sandbox refuses. Neither reads the files this PR changes (the first uses `tests/fixtures/regime-counters/`; the second writes its own temporary AGENTS.md). CI runs both.
- Other places that print the gate command were left alone: the README, `pr-integration.md`, the Codex mirror and gh-first-workflow point at step 10 and do not quote it (`test_gate_command_appears_once_in_skill_step_10`). AGENTS.md "Agent Review Evidence" names the evidence variables in prose; item 8 limits this task to the six items.
- Understand-Anything hook: did not fire. plan-mode-used: no.

## CI and the Codex Bot

They run on the head that carries this evidence. The results are in the RESULT and in the main-checkout copy of this report.

## CompactionDB

`memory add` printed `e187a179-a202-4697-b671-71df72581733` (validation §8): [memory:decision] the step 10.4 placement above and why.

cost: n/a
# Report: dotfiles-T128-playbook-rules-a02

- Seat: `claude-standard-dot-a003` in `.claude/worktrees/worker-c`, branch `regime/playbook-rules`, PR #328, continued from a01's head `9b2c02a1`. a02 is a01's INV-6 reset (`reset_of: [dotfiles-T128-playbook-rules-a01]`).
- Task file sha256 `7929fe7a…` matches the TASK's `task_sha256`. It is copied byte-identical in `95ba4e4c` to `.orchestration/dotfiles-T128-playbook-rules-a02/task.md`. The a01 copy keeps `b035ebd7…`, the hash a01's acceptance record names, unchanged since `1083a8c1` (validation §1). My held edit of the a01 copy to amendment 1 was discarded before the a02 copy was written, so the a01 copy is not edited under a02. The premises hold on `origin/main` `4cf1d4e2`, and `main` moved only under `.orchestration/` since the branch's base `683384ea` (§2).

## Carried over from a01 (`0158b866`, unchanged)

Items 1, 2, 4, 6 and 7 and their tests stand as a01 reported them (`.orchestration/dotfiles-T128-playbook-rules-a01/report.md`). Item 6's `ACCEPTANCE_EVIDENCE` sits before `BASE=origin/main` because `tests/unit/test_pr_feedback.py` pins the gate substring (§5).

## Commit `8b1dbefc`: a02's changes

| Item | Change | Test |
|---|---|---|
| 3 | the three-repeat bullet now reads a02's text verbatim: `grep -rl 'classes:.*<class slug>' .orchestration/learning/mistakes/` (with the `corrections:`/`index.yaml` parenthesis) and the CompactionDB search; "no match means a new mistake record carrying the class and a new correction are researched…" | `test_three_repeats_start_with_a_pasted_correction_search`: tokens for the new sentences, plus `assertNotIn` for a01's corrections grep and for `grep -l 'classes:` (the directory form without `-r`) |
| 5 | the task-file-review clause is qualified: "(for a task that carries an `invariants` key: … ; a task without the key needs no entry)" | `test_task_file_review_is_one_round_with_a_fixed_stop_condition`: the token is the qualified clause; `-contract-a01` stays asserted absent |

The sentence after item 3's closing quote in the task ("The `classes:` fields … land on `main` through the boundary commit …") describes the dispatch. It is not rule text and is not in the SKILL.

## Declared fixture changes (INV-12)

- `tests/fixtures/regime/invariants.md`: items 3 and 5 again (`8b1dbefc`), over a01's change (`0158b866`).
- `tests/fixtures/regime/orchestrator-step-6.md` and `tests/fixtures/regime/code-review-orchestration.md`: a01's changes, unchanged.

The fixture was regenerated by the test's own `section`/`normalized` logic, and `test_regime_rule_sections_are_pinned_whole` passes (§4).

## The a01 Bot round on `9b2c02a1` (review 5490674624)

The orchestrator answered these threads through a01 amendment 1 and this reset, not through thread replies. The worker resolves no thread.

| Thread | Finding | Disposition |
|---|---|---|
| 4247933544 | P1: the task's threat table groups merge, update-branch and forced removal in one row | `fixed:95ba4e4c`: the a02 task copy has one row per effect (§9) |
| 4247933561 | P1: the invariant check is unconditional, so a docs task fails its own review | `fixed:8b1dbefc`: qualified to tasks with an `invariants` key; this task has none and is not in `implementing_tasks` (§9) |
| 4247933574 | P2: the corrections grep misses `bookkeeping` and matches every record for `sources` | `fixed:8b1dbefc`: the search keys on the mistake records' `classes:`. On `main`, `bookkeeping` finds `M-20261012-4` (corrections C-3, C-6 through `index.yaml`), and `sources` finds 2 records, not 15 (§8) |

## Results

- Every double-quoted span of items 1 to 6 is in SKILL.md or AGENTS.md verbatim, and item 5's replaced clause is absent (§3).
- Docs module: 47 tests, OK (§4). `test_pr_feedback.py`: 16 tests, OK, and the pinned gate substring appears once (§5). `ruff format --check`: clean (§6).
- 13 mutants, 13 failures, tree restored (§7). They include a01 amendment 1's `grep -l` (3a), a01's corrections grep (3d), the `-contract-a01` clause (5) and a01's unqualified clause (5b).
- Item 3's search, run with `/usr/bin/grep` on an export of `origin/main` `4cf1d4e2`: `-rl` returns `M-20261012-4.md` (rc 0); amendment 1's `-l` exits 2 with "Is a directory" (§8).
- Item 8: every SKILL hunk lands in the invariants or the Orchestrator Playbook, the counters bullet hashes the same as on `main`, and the step 7, step 15 and message-contract fixtures are unchanged (§11).
- Size (§10): 6 changed files outside `.orchestration/`; 7 added lines outside `tests/` (cap 500); 86 under `tests/` (cap 1000).

## Not done, or outside scope

- `gh pr update-branch`: the PR's base is `683384ea` while `main` is `4cf1d4e2`. The task's threat table lists update-branch as an orchestrator effect, so the branch is not updated here. `main` moved only under `.orchestration/` (§2).
- `tests/unit/test_regime_counters.py` and `tests/unit/test_require_crit_review.py` were not run locally (`--with pyyaml` needs PyPI, which the sandbox refuses). Neither reads the changed files, and CI runs both.
- Understand-Anything hook: did not fire. plan-mode-used: no.

## CI and the Codex Bot

They run on the head that carries this evidence. The results are in the RESULT and in the main-checkout copy of this report.

## CompactionDB

`memory add` printed `8bbacd66-762a-4abb-9ae7-7944c4aceb2c` (§12): [memory:decision] item 3's search keys on the mistake records' `classes:` with `grep -rl`, and item 5's check applies only to tasks with an `invariants` key. a01's `e187a179-a202-4697-b671-71df72581733` (the step 10.4 placement) stands.

cost: n/a

## Amendment 1 of a02 (TASK 13:28:30Z, sha256 `07b78f64…`)

The amendment answers Bot thread 4248319936 (P2, "past the task's expected duration" had no computable threshold). Only item 1's last sentence changes.

- `4486dbdd`: the a02 task copy, recommitted byte-identical at amendment 1 (validation §16).
- `4b62feda`: Orchestrator Playbook step 6 ends with the amendment's sentence verbatim: "Thirty minutes after a TASK, an amendment or a revise enters the bus history with no bus event from its seat since (the clock and the figure of INV-10's first-push rule) trigger a bus read, then a PING; a longer silent wait is never the answer." `test_dispatches_are_recorded_from_the_bus` asserts it, plus `assertNotIn("expected duration")` for step 6.
- Declared fixture change (INV-12): `tests/fixtures/regime/orchestrator-step-6.md`, regenerated by the test's own logic.
- Every quoted span of items 1 to 6 is present verbatim. Docs module 47 OK, pr_feedback OK, ruff clean, 14 of 14 mutants fail (1c puts the "expected duration" sentence back) (§16).
- Thread 4248319936 → `fixed:4b62feda`. Thread 4248319926 (no `classes:` field in the PR tree) is answered by the orchestrator's `gh pr update-branch`, as the amendment states.
- Before the push, the remote branch was still at `375bae0f`, so no update-branch merge had to be taken first.
- CompactionDB: `aa6c26f7-275d-4e89-8458-d4bca1cc96a0`.
# Report: dotfiles-T128-playbook-rules-a03

- Seat: `claude-standard-dot-a003` in `.claude/worktrees/worker-c`, branch `regime/playbook-rules`, PR #328, continued from a02's head `c4e0bb72`. a03 is a02's reset under plan 009 option A (`reset_of: [a01, a02]`).
- Task file sha256 `ee638518…` matches the TASK's `task_sha256`. It is copied byte-identical in `196d73ca` to `.orchestration/dotfiles-T128-playbook-rules-a03/task.md` (validation §1).
- History copies are not edited under a03. The a01 copy is unchanged since `1083a8c1`, and the a02 copy since `4486dbdd`. The a02 copy holds `07b78f64…`, a02 as last dispatched (amendment 1), which a02's acceptance record names at lines 24 and 25; its line 3 names the first dispatch `7929fe7a…` (§1).

## Commit `f40e530a`: items 2, 3 and 4 in the landing-condition form

| Item | Sentence now (verbatim from a03) | Test |
|---|---|---|
| 2 | "… (hashed, checked by the task-consistency check C1 to C6 once plan 007 T704 lands it and by hand until then, confirmed by the review seat), never as a PONG answer." | `test_rule_changes_travel_as_task_amendments` |
| 3 | "Once `dotfiles-T128-gate-evidence-a02` lands, the gate refuses the action without the paste; until then the orchestrator refuses it by rule. Every `not-applicable` disposition carries `; evidence=<command>` with the output pasted in the record." | `test_three_repeats_start_with_a_pasted_correction_search`: one token per sentence, plus `assertNotIn("gate-evidence-a01")` on the bullet |
| 4 | "…; C4 of the task-consistency check (plan 007 T704) verifies the path half once it lands, and the task-file review checks it by hand until then." | `test_threat_table_rows_have_a_fixed_unit`, plus `assertNotIn("C4 verifies the path half before dispatch")`; the AGENTS.md clause is unchanged |

Each landing condition holds on `main` `e0e2fe62` (§2). Nothing in `scripts/` or the Makefile reads `ACCEPTANCE_EVIDENCE`; no task-consistency checker is in the tree; `regime/gate-evidence` is open on the remote.

Item 6: the SKILL text is unchanged, and step 10.4's gate command carries `ACCEPTANCE_EVIDENCE=<acceptance record>` as before (§3). a03 renames `gate-evidence-a01` to `-a02` inside item 6's parenthetical. As in a01, the parenthetical is the task's rationale, not quoted rule text: items 2, 3 and 4 quote their sentences, and item 6 never has. Neither the task nor the operator's option A ("the three sentences") quotes a sentence for step 10.4. The Bot reviewed that command on three heads without a finding, and a SKILL sentence the task does not quote would be an undeclared change (INV-12). If the orchestrator wants the landing condition stated in step 10.4, that is a quoted sentence in an amendment. The test comment on `test_the_gate_reads_the_acceptance_record` now names `gate-evidence-a02`.

## Declared fixture changes (INV-12)

- `tests/fixtures/regime/invariants.md`: items 2, 3 and 4 (`f40e530a`).
- `tests/fixtures/regime/orchestrator-step-6.md` and `code-review-orchestration.md` were regenerated and are unchanged (`f40e530a` touches three files, §7).

## Results

- Every quoted span of items 1 to 6 is in the prose verbatim, and item 5's replaced clause is absent (§3).
- Docs module 47 OK (§4). `test_pr_feedback.py` OK, ruff clean (§5).
- 17 mutants, 17 failures (§6), including each a02 sentence put back (2b, 3e, 4c).
- Size (§7): 6 files outside `.orchestration/`; 7 added lines outside `tests/`; 100 under `tests/` (caps 500 and 1000). Every SKILL hunk lands where it did in a02.

## Bot threads

| Thread | Head | Disposition |
|---|---|---|
| 4248711363 | `c4e0bb72` | `fixed:f40e530a` (the gate sentence names its landing condition) |
| 4248711371 | `c4e0bb72` | `fixed:f40e530a` (the C4 clause names its landing condition) |
| 4248319936 | `375bae0f` | `fixed:4b62feda` (a02 amendment 1) |
| 4248319926 | `375bae0f` | the orchestrator's `gh pr update-branch` brings `main`'s `classes:` fields into the PR tree |
| 4247933544, 4247933561, 4247933574 | `9b2c02a1` | `fixed:95ba4e4c`, `fixed:8b1dbefc`, `fixed:8b1dbefc` (a02 report) |

The worker resolves no thread. The CI and the Bot on the a03 head are in the RESULT and in the main-checkout copy of this report.

## Not done, or outside scope

- `gh pr update-branch`: the orchestrator's, after the a03 head (task Completion).
- `tests/unit/test_regime_counters.py` and `test_require_crit_review.py` were not run locally (PyPI is unreachable from the sandbox); neither reads the changed files.
- Understand-Anything hook: did not fire. plan-mode-used: no.

## CompactionDB

`memory add` printed `651f5fce-7002-4db5-9d48-b9af40a34601` (§8). The earlier ids stand: `aa6c26f7…`, `8bbacd66…`, `e187a179…`.

cost: n/a

 succeeded in 154ms:
.orchestration/plans/018-stop-and-situation.md
.orchestration/plans/019-root-causes-and-corrective-order.md
.orchestration/plans/021-execution-detail-and-scrutiny.md
.orchestration/plans/017-resume-t703-a04-after-t718.md
.orchestration/plans/007-mistakes-into-mechanisms.md
.orchestration/plans/020-certain-order.md
5:- Integration after its RESULT (`finish-336c.sh <extra.tsv>`): update-branch by ancestry, CI, Bot, the C-32 local review (`local-review.sh`), the sweep with the dispositions (the 20 rows of a03's ledger, the three threads and the local finding as `fixed:<sha>`), one revise round at most, residual P2 owned by a02 item 6 (on main), review receipt, one audit of the final head, gate, `gh pr merge --squash --match-head-commit`, ff, then `integrate-328.sh <squash>` and `integrate-329.sh <T703 squash>`. No boundary while PR #336 is between its update-branch and its merge (`awaiting-merge/336` marker).
12:- 08:46Z Bot review on `5b99a744` (CI still running): four P2 threads: 4256541708 (`test_orchestrator_tools.py:234`, the unwritable-directory test passes as root: make the denial deterministic), 4256541716 (`dispatch.sh:60`, a NUL byte in the line file is dropped by command substitution: reject it), 4256541723 (`bus-read.sh:52`, the row regex accepts any first token, the grammar allows only `●` and `○`), 4256541725 (`dispatch.sh:126`, a `previous_design_sha256=` reference is treated as an artifact binding: a02 item 4's grammar row, on main, owns it). Under plan 016 G′ the one revise round of a04 carries the local finding and the first three; 4256541725 is `not-applicable: owned by dotfiles-T128-orchestrator-tools-a02 item 4`. Class counts on the lineage after these rows: `input-validation` reaches 5; plan 016 G′ (07:16Z) governs the residual path (no further revise; residual P2 of the revise head owned by a02 item 6), so no new S7 is raised for the same artifact (08:48Z).
18:- 08:55:15Z RESULT (bus 920): head `5b99a744` (3d131215 origin/main merged; 05e3292f the four fixes; 5b99a744 the task copy and evidence), CI 13 of 13, Bot review 5500993250 (08:46:05Z, four P2, no P0/P1), `bot_rounds=1`; threads 4255494133, 4255494139, 4255494137 and the local finding on 0d199475 `fixed:05e3292f`; the four new threads reported open and valid for the revise round; tests 16 OK, counters 26 OK, mutants 15 of 15 killed; caps 6 files, 378 lines outside tests, 468 under tests; counters logic unchanged. 08:56:12Z ACCEPTANCE `status=revise` (bus 921 read_at=2026-10-13T08:56:07Z): a04's one revise round carries the local finding (bus-read.sh:60, revise openers bound to the task's endpoints) and all four Bot threads, 4256541725 included (fixed per a02 item 4's grammar row rather than owned: a fix beats an owner; the worker reports seven design-review TASK lines on the bus that dispatch.sh would refuse). INV-6 for a04 after this: `revises=1`; residual P2 of the revise head are owned by a02 item 6.
47:- 09:36:36Z revise RESULT (bus 924): head `3e5cad37` (fix commit `e2e67de8`), CI 13 of 13, Bot review 5501536934 (09:32:57Z, three P2, no P0/P1), `bot_rounds=2`; the five findings of the round `fixed:e2e67de8` with their tests (the local finding by `test_bus_read_ignores_closers_between_other_endpoints`; 4256541708 by `test_dispatch_refuses_an_unwritable_record_before_sending`; 4256541716 by `test_dispatch_refuses_a_task_line_without_task_sha256_or_with_a_second_line`; 4256541723 by `test_bus_read_skips_and_counts_malformed_rows`; 4256541725 by `test_dispatch_passes_the_line_byte_identical` and `test_dispatch_refuses_malformed_lines`); 16 tests OK, counters 26 OK, 21 of 21 mutants killed; caps 6 files, 393 outside tests, 485 under tests. The Bot's round on the final head: 4256987062 (bus-read.sh: the limit checked after the shape filter), 4256987076 (the silence clock counts rows between other endpoints), 4256987087 (dispatch.sh: CRLF record prose rewritten as LF): the residual P2 of a04's final head after its one revise round, each `not-applicable: owned by dotfiles-T128-orchestrator-tools-a02 item 6` (a02 on main `d25c3df8`), as the Completion clause and plan 016 G′ define; no further revise (INV-6: `revises=1`).
56:-  C-32 local review of the final head `3e5cad37` (`dotfiles-T128-orchestrator-tools-a04-local-review-3e5cad3.md`, one sample): one P2, `regime-counters.sh:130-132`, malformed ledger rows used before validation: the ledger-shape guard a02 item 3 owns on main (thread 4255079204). The 0d199475 local review (dispatch.sh:187) gets its row and line here too (the audit's finding 3). Audit of 3e5cad37 (`dotfiles-T128-orchestrator-tools-a04-audit-3e5cad3.md`): `Verdict: incorrect`, three P2: (1) `bus-read.sh:56` splits the body on literal spaces while the stop gate tokenizes runs of whitespace (a residual P2 of the final head, owned by a02 item 6 with the three Bot threads of the same head); (2) the revise lacked the pasted counters and the S6 searches; (3) the ledger omitted the 0d199475 local finding. Findings 2 and 3 are addressed below in this record; finding 1 is owned. The gate refused the first pass on exactly these dispositions (`AUDIT_DISPOSITIONS leaves audit findings 1, 2, 3 without a disposition`), as designed; the chain's own verdict match (`*correct)` matching `incorrect`) let it reach the gate and is fixed in the scripts (M-20261012-35 candidate: a glob that matched its negation).
67:audit-finding: 1 not-applicable:owned by dotfiles-T128-orchestrator-tools-a02 item 6 as a residual P2 of a04 final head 3e5cad37 after its one revise round (bus-read.sh:56 tokenizes the row body on runs of whitespace as the stop gate does; the same script and class as the three Bot threads of that head owned by item 6; ledger row audit:3e5cad3:1); evidence=git show origin/main:.orchestration/tasks/dotfiles-T128-orchestrator-tools-a02.md | grep -n 'item 6'
68:audit-finding: 2 not-applicable:addressed in this record at 09:51Z: the counters of a04 and a03 and the S6 searches for the four classes at three or more on the lineage (record-association 6, input-validation 6, hash-binding 4, duplicated-state-machine 4) are pasted below; every search returns M-20261012-32 or M-20261012-33, the records of this artifact own cycles (C-31, C-32), and plan 016 G′ (operator, 07:16Z) is the decision taken after them for this artifact: one revise round, residual P2 owned by a02 item 6; evidence=sed -n "/S6 searches for the final head/,/^```$/p" .orchestration/acceptance/dotfiles-T128-orchestrator-tools-a04.md
120:-  residual R1 of the tools lineage (from PR #328 thread 4249414388, raised against T703's rule text and refuted there because the text no longer prescribes a grep): `three-repeat.sh` matches the class as a substring (`^classes:.*<class>`: `scope` also matches `class-count-scope`); the body search of a04 (`grep -rli -- <class>`) has the same property by design. Owner: the tools task after a02 (not yet written; a02 item 6 is defined by this ledger's owned rows only), named here so the next task text carries it.
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
            "poke.sh",
            "send.sh",
            "--body-file",
            "agmsg-dispatch",
            "13 =",
            "inbox.sh",
            "gh pr merge --squash",
            "--match-head-commit <audited head sha>",
            "never pushes a repository change to `main` directly",
            "is never an implicit opt-out",
            "actas.<team>__<name>.session",
            "`<common>/objects`",
            "messages.db `read_at`/PONG query",
            "Never run full mode from inside an existing managed workspace",
            "`--restart-worker` is retired and exits 2",
            "herdr-agents --add-worker [<worktree>]",
            "remove every worker with `herdr-agents --remove-worker <worktree>`",
            "machine-state hygiene that touches no repository",
        ):
            with self.subTest(token=token):
                self.assertIn(token, text)

    def test_skill_carries_the_parallel_execution_and_routing_mechanics(self) -> None:
        text = SKILL.read_text()
        for token in (
            "pairwise-disjoint",
            "--add-worker",
            "re-tasked immediately",
            "acceptance follows RESULT arrival order",
            "gh pr update-branch",
            "Self-Modification",
            "home/dot_claude/modify_private_settings.json",
            "`claude.sandbox`",
            "home/dot_agents/permgate-policy.yaml",
            "PermissionRequest hook of both seats, goes to the operator",
            "AGMSG-PONG v1 status=blocked",
            "--ask-for-approval never",
        ):
            with self.subTest(token=token):
                self.assertIn(token, text)

    def test_codex_worker_profile_defaults_to_standard(self) -> None:
        text = SKILL.read_text()
        parallel = text.split("## Parallel workers", 1)[1].split("\n## ", 1)[0]
        for token in (
            "For Codex, seat ordinary tasks with `--profile standard`",
            "use `--profile security` only for trust-boundary tasks",
            "permgate, redaction or secret handling, sandbox or permission policy",
            "`codex-security-dot-aNNN`",
        ):
            with self.subTest(token=token):
                self.assertIn(token, parallel)
        routing = text.split("## Orchestrator Playbook", 1)[1].split("\n4. ", 1)[0]
        self.assertIn("records it and the chosen worker profile in the task file", routing)

    def test_skill_carries_the_audit_gate_and_bot_wait_mechanics(self) -> None:
        text = SKILL.read_text()
        for token in (
            "--audit",
            "--task",
            "-audit-<sha7>.md",
            "AUDIT_EVIDENCE",
            "in_reply_to_id",
            "until a review of the final head appears or 15 minutes pass",
            "needs green CI but no new Bot wait",
            "CI on the new head, then the sweep, then the audit",
            "audit-finding: <n>",
            "Such a review-body finding is listed alongside the top-level inline comments and fixed or dispositioned the same way.",
            "A `review` sweep item whose body carries a `P0`–`P3` badge is a finding with its own `fixed:<commit>` or `not-applicable:<reason>` disposition, never a container for its inline threads.",
            "Deferral",
            "is not a disposition",
        ):
            with self.subTest(token=token):
                self.assertIn(token, text)

    def test_skill_carries_the_session_lessons(self) -> None:
        text = SKILL.read_text()
        for token in (
            "WebFetch tool, not Bash `curl`",
            "Fetch and fast-forward inside the sandbox",
            "So a Claude seat runs three commands outside the sandbox through the permission gate:",
            "`gh`, `git push`, and an authenticated `git fetch`",
            "-worker-crit.json",
            "writing the task's artifacts at their expected main-checkout paths and masking them with the repository masker, through the permission gate because the main checkout is not writable from a worktree sandbox",
            "(a Claude seat writes them through the permission gate, step 4)",
            "never run `git worktree prune` from a sandboxed seat",
            "`git worktree remove <path>` only",
            "the orchestrator moves them into the main checkout",
            "uv run --no-project .claude/hooks/contextdb_cli.py memory candidates --limit 20",
            "uv run --no-project .claude/hooks/contextdb_cli.py memory promote <id> --scope project",
        ):
            with self.subTest(token=token):
                self.assertIn(token, text)


class AgmsgRegimePatternTest(unittest.TestCase):
    """Plan 006 Phase A: the review and fix pattern, each rule in the section that owns it."""

    @staticmethod
    def section(text: str, start: str, end: str = "\n## ") -> str:
        return text.split(start, 1)[1].split(end, 1)[0]

    def invariants(self) -> str:
        return self.section(SKILL.read_text(), "## Review and integration invariants")

    # Plan 006 S1 on the docs tests (class unpinned): token tests pin only the clauses their author chose, so
    # each regime rule section is also pinned whole; a rule changes only together with its fixture (INV-12).
    PINNED_SECTIONS = (
        # name, file, outer slice or None, (start, end): the start marker is part of the pinned text.
        ("invariants", SKILL, None, ("## Review and integration invariants", "\n## ")),
        ("worker-step-15", SKILL, None, ("\n15. After the final push", "\n## ")),
        ("orchestrator-step-6", SKILL, ("## Orchestrator Playbook", "\n## "), ("\n6. ", "\n7. ")),
        ("orchestrator-step-7", SKILL, ("## Orchestrator Playbook", "\n## "), ("\n7. ", "\n8. ")),
        ("message-contract", SKILL, None, ("## Message Contract v1", "\n## ")),
        (
            "code-review-orchestration",
            ROOT / "AGENTS.md",
            None,
            ("### Orchestration records and trust-boundary code", "\n## "),
        ),
    )

    @staticmethod
    def normalized(text: str) -> str:
        return "\n".join(line.rstrip() for line in text.split("\n")).strip()

    def test_regime_rule_sections_are_pinned_whole(self) -> None:
        for name, path, outer, (start, end) in self.PINNED_SECTIONS:
            with self.subTest(section=name):
                text = path.read_text()
                if outer:
                    text = self.section(text, *outer)
                fixture = ROOT / "tests/fixtures/regime" / f"{name}.md"
                self.assertEqual(
                    self.normalized(start + self.section(text, start, end)),
                    self.normalized(fixture.read_text()),
                    f"regime rule section {name} changed: declare the change by updating "
                    f"tests/fixtures/regime/{name}.md in the same commit and listing it in the RESULT",
                )

    def test_design_review_runs_in_paired_rounds_with_a_cap(self) -> None:
        text = self.invariants()
        for token in (
            "get the same design hash at the same time",
            "The orchestrator revises once per pair of results",
            "opens no round while one is still open",
            "frozen at the hash the pair last accepted",
            # Thread 4243537279: a revision after the third pair would freeze an unreviewed hash.
            "any later change to a hashed key is a new pair (INV-7)",
            # Thread 4243732324: a third pair that returns revise or reject has no accepted hash to freeze.
            "on its revise or reject nothing is frozen",
            "becomes a residual list that is worker input",
            "never implementation detail",
        ):
            with self.subTest(token=token):
                self.assertIn(token, text)

    def test_task_file_review_is_one_round_with_a_fixed_stop_condition(self) -> None:
        text = self.invariants()
        for token in (
            "A task-file review is one round with a fixed stop condition",

**Analyzing task invariants error reporting**
**Reviewing error reporting and auditing**
codex
GitHub コネクタで指定 head と CI の成功を確認できました。記録作成時点の指摘は、現時点では後続タスクで扱える規則の不足と判断しています。step 10.3 はそれ以前の記録作成を禁止しておらず、既存の規則も受け入れ前の追記を求めています。

一方、feedback 証跡にゲートで拒否される disposition が1件ありました。`fixed:a03c1daa` は今回の base より前のコミットで、必須の `base..head` 範囲外です。残りの証跡とテストを確認して結論をまとめます。

mcp: codex_apps/github.get_commit_combined_status started
mcp: codex_apps/github.fetch_workflow_run_jobs started
mcp: codex_apps/github.fetch_workflow_run_jobs started
mcp: codex_apps/github.fetch_workflow_run_jobs started
exec
/bin/zsh -lc "python3 -B -c 'import pathlib,subprocess,types,unittest,io
root=pathlib.Path.cwd(); head=\"65a3d71bf4e496252bf1ff51894974130c96cd43\"
cache={}
def blob(path):
 key=path.relative_to(root).as_posix()
 if key not in cache: cache[key]=subprocess.check_output([\"git\",\"show\",head+\":\"+key]).decode()
 return cache[key]
original=pathlib.Path.read_text
def read_text(p,*a,**kw):
 try:p.relative_to(root)
 except ValueError:return original(p,*a,**kw)
 return blob(p)
pathlib.Path.read_text=read_text
p=root/\"tests/unit/test_agmsg_orchestration_docs.py\"
m=types.ModuleType(\"audited_docs\");m.__file__=str(p)
exec(compile(blob(p),str(p),\"exec\"),m.__dict__)
suite=unittest.defaultTestLoader.loadTestsFromModule(m)
r=unittest.TextTestRunner(verbosity=1).run(suite)
print(\"Snapshot test files read:\",len(cache),\"head:\",head,\"tests:\",r.testsRun,\"success:\",r.wasSuccessful())
raise SystemExit(not r.wasSuccessful())'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
mcp: codex_apps/github.fetch_workflow_run_jobs (completed)
mcp: codex_apps/github.get_commit_combined_status (completed)
 succeeded in 608ms:
...............................................
----------------------------------------------------------------------
Ran 47 tests in 0.450s

OK
Snapshot test files read: 25 head: 65a3d71bf4e496252bf1ff51894974130c96cd43 tests: 47 success: True

mcp: codex_apps/github.fetch_workflow_run_jobs (completed)
mcp: codex_apps/github.fetch_workflow_run_jobs (completed)
**Summarizing test and audit status**
**Verifying code and audit integrity**

I'm confirming that secret scanning, diff inspections, and invariant checks hold true for the task, focusing on safe execution and codebase integrity without unexpected changes.
exec
/bin/zsh -lc "git show 65a3d71bf4e496252bf1ff51894974130c96cd43:home/dot_agents/skills/agmsg-orchestration/SKILL.md | nl -ba | sed -n '55,66p'; nl -ba .orchestration/plans/020-certain-order.md | sed -n '1,160p'; nl -ba .orchestration/plans/021-execution-detail-and-scrutiny.md | sed -n '1,160p'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 37ms:
    55	- A codex worker in a nested worktree gets `<common>/objects`, `<common>/refs`, `<common>/logs` and `<common>/worktrees/<name>` (`<common>` from `git -C <worktree> rev-parse --git-common-dir`) as writable roots from `herdr-agents` (`-c sandbox_workspace_write.writable_roots`, with the configured agmsg roots kept first), so local git operations need no escalation. The common dir itself, `config`, `hooks`, `info`, `HEAD` and `packed-refs` stay read-only. The worker seat runs with `--ask-for-approval never` and `sandbox_workspace_write.network_access=true`, so a GitHub fetch, push or `gh` call works inside the sandbox and the worker never prompts: there is no escalation for a worker, and an action outside the sandbox or forbidden by the execpolicy fails and is reported as `AGMSG-PONG v1 status=blocked`. The `sandbox_workspace_write.network_access` switch is a boolean, so the worker reaches any host (no domain allowlist is configured, unlike Claude Code's `allowedDomains`), and the permgate PermissionRequest hook never fires for the worker seat; it stays live for interactive Codex sessions, which keep on-request approvals and no sandbox network.
    56	- The orchestrator's actas seat lock must hold the composite instance id `<sid>.<pid>`; check it with `cat ~/.agents/skills/agmsg/run/actas.<team>__<name>.session`. `actas-claim.sh` run from sandboxed Bash cannot see the claude pid (the Linux sandbox has its own pid namespace), writes the bare session id, and the Stop-hook inbox check then skips delivery silently (`other:<sid>`). `herdr-agents` therefore claims the seat outside the sandbox when it starts the orchestrator pane and from its SessionStart `--attach` hook, printing `seat_claim=ok owner=<sid>.<pid>` (or `seat_claim=unresolved`, never a bare-id lock), and `make doctor` warns on a bare-id orchestrator lock while a claude session runs in the repository. A `watch.sh` Monitor cannot run under that sandbox either: it sees the claude pid as dead and exits "no longer alive". Until upstream offers a liveness override, turn delivery is the working path, and an idle orchestrator is woken by the worker's `agmsg-dispatch` to the orchestrator pane.
    57	- Reserve store separation for concurrent regimes in different projects, such as flue-pi. When using it, set the same `AGMSG_STORAGE_PATH` in the worker pane and on orchestrator send/watch/history calls or tasks, results, and pongs become unreachable. Same-repository parallel workers always share the default store.
    58	
    59	## Live verification
    60	
    61	- Accept changes to live desktop behavior — herdr layout/session, pane lifecycle, or delivery hooks — only after live end-to-end verification covers both a fresh session and a persisted-session restore; unit and static tests alone are insufficient.
    62	- Launch orchestrator-driven E2E test-subject panes with express-profile arguments from `~/.agents/model-profiles.env` (`MODEL_PROFILE_EXPRESS_CLAUDE_ARGS` / `MODEL_PROFILE_EXPRESS_CODEX_ARGS`), never ad-hoc `--model` flags.
    63	
    64	## Review and integration invariants
    65	
    66	- Review every RESULT adversarially across correctness, regressions, security, and reporting omissions: try to refute it, independently re-derive findings, and never treat sampled spot checks as full verification.
     1	# Plan 020: the order that removes the causes by construction (operator's question 13:04Z: "does the proposal make the essential improvement certain? one by one, in what order, how, with the least redo and cost")
     2	
     3	> Draft for the operator. Principle: a step counts as certain only when it removes a cause **by construction** (a classification, a setting, a cap, a sequence rule) rather than by hoping a reviewer or a worker behaves; each step's proof is one observable on the next PR. Steps that only lower probability (smaller PRs, shorter texts) come after the structural ones and are never the thing the plan relies on.
     4	
     5	## Why the earlier proposals were not certain
     6	
     7	Plans 012 to 018 added mechanisms of the same kind that caused the loop: more rules, more scripts, more reviews, more records. None of them bounded the loop; each new head could still generate work. The essential change is the opposite: **acceptance is decided by deterministic checks, and LLM reviews become advice.** Everything below follows from that one change.
     8	
     9	## The order
    10	
    11	| # | Step (what, how) | Why it is certain (by construction) | Proof on the next PR | Cost / redo |
    12	|---|---|---|---|---|
    13	| 1 | **Reclassify.** P2 findings from the Codex Bot, the local review and the audit are advisory: recorded in the acceptance record with their id, never a fix round, never a disposition the gate waits for, never an INV-6 count. Only P0/P1 can require work, and at most one fix round per PR. Done by a rule sentence and a filter on the badge in `fill_sweep.py` (deterministic: the badge is in the comment body). | The loop's fuel was P2 (21 of 30 threads on #336, 8 of 16 on #328). A classification applied by us cannot be "found" again by a reviewer; the number of P2-driven rounds becomes zero by definition. | zero rounds caused by P2; the record lists them | minutes; nothing to redo later (the rule stays under every later step) |
    14	| 2 | **Stop re-sampling.** Set the Codex review trigger to "On PR open" (operator, app.chatgpt.com/settings/code-review); re-review only by `@codex review` after a P0/P1 fix. Observed: 13 reviews on 30 commits of one PR. | A reviewer that does not run cannot add findings. A setting, not a behaviour. | review count per PR = 1 + number of P0/P1 fix rounds | one setting; operator-only |
    15	| 3 | **Stop moving main under open PRs.** Records go to main once per day at most, and never while a PR is between its final head and its merge; one PR in integration at a time. | The update-branch → CI → review cascade needs main to move; with main still, it cannot start. A sequence rule. | zero update-branch-triggered CI runs or reviews | zero; the cadence rule only |
    16	| 4 | **Deterministic merge rule.** A PR merges when: required checks green, threads resolved (ruleset), one audit run with its P0/P1 dispositioned (P2 advisory per step 1), the gate's evidence present. No pair review of task text for in-flight PRs. | Every term is a boolean the machine reads; none depends on a reviewer finding nothing. | the chain reaches the merge without a judgment stop | zero; this is what the scripts already do once steps 1–3 remove the extra stops |
    17	| 5 | **Close the three open PRs under 1–4** (#328: the one P1 round already confirmed as the amendment; #329: merge the accepted head; #346: the worker's RESULT). This is the first measurement, not a new plan. | Steps 1–4 are the environment; the PRs are the test. | three ledger lines: rounds, threads by priority, wall | the worker rounds already owed; no new text |
    18	| 6 | **Land the tools before any new rule** (a02 PR-B, then T704's checkers), retire the scratchpad chain, forbid rule sentences that name an unlanded mechanism. | A rule enforced by a script that exists is checked the same way every time; a rule enforced by hand is re-litigated every round (M-26, M-35). | the next integration runs only repository scripts | the PRs are already scoped; done under steps 1–4 so they cannot loop |
    19	| 7 | **Shrink the unit** (after 6, because the checker generates the threat table): one mechanism per PR, ≤ 200 changed lines outside tests; task text one page with one end-to-end check; text review one round, seat and Codex in parallel; findings beyond it become the next PR's items. | Reduces findings per round (probabilistic) on top of the caps from 1–4 (structural); it is not what bounds the loop. Doing it before 6 would mean hand-written tables again, redone after 6. | text ≤ 60 lines, ≤ 1 text round | one template; no redo because the checker exists |
    20	| 8 | **Recalibrate INV-6 and the asks from data** (one design amendment, after three PRs of ledger lines): resets only on a failed deterministic check or an unfixed P0/P1; operator decisions asynchronous with a default, blocking only for P0. | Changing thresholds before the data exists risks a second amendment; after it, one amendment. | resets per week; ask wait time | one design round |
    21	| 9 | **Merge queue evaluation** (optional, last): if available for this user-owned public repository, CI on `merge_group`, "Require merge queue", strict off. | Official replacement for the strict/update-branch cost; only worth a CI change once steps 3 and 6 have made PRs cheap to re-run. | update-branch count 0 without the cadence rule | one CI PR |
    22	
    23	## What stops immediately (no cost, no redo)
    24	
    25	No new task texts in the current format (they would be rewritten at step 7); no new M/C records for process slips (one retrospective at step 8); no boundary until step 5 is done; no pair review of in-flight texts; no plan file per incident.
    26	
    27	## What stays uncertain, and its guard
    28	
    29	LLM reviewers remain non-deterministic; a defect a reviewer would have found as P2 can reach main. The guards are the tests in the same PR, the required checks, the single audit for P0/P1, and the follow-up items that carry the advisory findings. This is the same guarantee every human code-review process gives: correctness from tests and checks, judgment from review, no claim that review finds everything.
    30	
    31	## Operator-only steps and when
    32	
    33	- Step 2: the Codex review trigger (now, before step 5).
    34	- Step 9: the merge-queue decision (later, optional).
    35	- Nothing else; steps 1, 3–8 are the orchestrator's.
     1	# Plan 021: plan 020 subdivided (who does what, in what order), with the scrutiny for contradictions, ambiguities, errors and omissions
     2	
     3	> Draft for the operator (2026-10-13 13:10Z). Nothing executed. "O" = orchestrator seat (me, under the regime's exemptions: task files, records, acceptance, integration, control plane). "W" = a seated worker (repository mutations). "OP" = the operator only (settings outside the repository, Claude-boundary rule text by the routing rule, `make update`, restarts, decisions on standing rules). Every OP item is listed once, at the moment it is due.
     4	
     5	## Part A: the subdivided steps
     6	
     7	### Step 1: P2 becomes advisory without changing any standing rule yet
     8	
     9	| # | Sub-step | Who | Detail | Verifiable output |
    10	|---|---|---|---|---|
    11	| 1.1 | Owner task per lineage | O | Three one-page task files from one template: `dotfiles-T128-playbook-rules-followup-a01` (exists, pair-confirmed), `dotfiles-T128-orchestrator-tools-followup-a01`, `dotfiles-T128-gate-evidence-followup-a01`; item 1 = the rows under the heading `## Owned by <task id>` in the lineage's acceptance record; `after:` the lineage's last task | checker C1–C10 OK; one parallel pair round (seat + Codex) |
    12	| 1.2 | Advisory section in acceptance records | O | Every P2 (Bot, local review, audit) goes under `## Owned by <followup id>` as `<id>\t<class>`; the sweep disposition reads `not-applicable:advisory P2 owned by <followup id>; evidence=git show origin/main:<task file> \| grep -n 'item 1'`; the reply on the thread says the same; the thread is resolved | sweep gaps 0; threads resolved |
    13	| 1.3 | Automatic disposition | O | `fill_sweep.py`: a Codex review comment whose badge is P2 or P3 and whose PR maps to a follow-up id (a 3-line map file) gets the 1.2 disposition; P0/P1 stay manual | the fill prints the count of advisory rows |
    14	| 1.4 | Counting | O (interim) → OP (rule) | Until plan 007's S6/S7 wording is amended, the orchestrator counts classes over non-advisory rows only and says so in each record; the amendment itself is OP's decision in step 8 | the record's class table names the rows it excludes |
    15	| 1.5 | One boundary | O | Boundary (12) lands 1.1's two new files and the template; nothing else waits on it except step 5's dispositions | PR merged; `git show origin/main:<file>` for both |
    16	
    17	### Step 2: the Codex Bot reviews once
    18	
    19	| # | Sub-step | Who | Detail | Verifiable output |
    20	|---|---|---|---|---|
    21	| 2.1 | Read the current trigger | OP | app.chatgpt.com/settings/code-review → repository `mryfmo/dotfiles` → "Review trigger" (and Personal preferences → Automatic review, if the repository follows it); tell the orchestrator the current value | the value, pasted into the record by O |
    22	| 2.2 | Set "On PR open" | OP | the repository trigger (not "every push", not "Smart"); the security review trigger set to "Whenever code review runs" or off | the value |
    23	| 2.3 | Verify | O | the next pushed head of an open PR gets no review within 20 minutes; a manual `@codex review` still works | the ledger line |
    24	
    25	### Step 3: main stays still under open PRs
    26	
    27	| # | Sub-step | Who | Detail | Verifiable output |
    28	|---|---|---|---|---|
    29	| 3.1 | Cadence | O | records reach main once per day at most (boundary (12) in step 1 is today's; boundary (13) after the three PRs merge is tomorrow's unless the operator asks otherwise) | boundary count |
    30	| 3.2 | Serial integration | O | one PR in integration at a time: #328 → #329 → #346; the next starts only after the previous merge and its fast-forward | the ledger shows no overlap |
    31	| 3.3 | Expected update-branch cost | O | #328: none (the worker merges main in its round); #329: one; #346: one (after #329). Each is one CI run; no review (step 2) | CI runs per PR |
    32	
    33	### Step 4: the deterministic merge rule, applied as the chain's stop conditions
    34	
    35	| # | Sub-step | Who | Detail | Verifiable output |
    36	|---|---|---|---|---|
    37	| 4.1 | Conditions | O | required checks green; every review thread resolved; one audit of the final head with each P0/P1 finding dispositioned (fixed in the one round, or the PR stops); P2 advisory per step 1; the gate's four evidence files present | gate rc=0 |
    38	| 4.2 | The one fix round | O/W | all P0/P1 known at the time (Bot's single review, the local review's single run, the pre-round audit) go in one `status=revise`; the post-round audit's new P0/P1, if any, stop the PR (INV-6's reset path), never a second round | revises ≤ 1 per PR |
    39	| 4.3 | No text review for in-flight PRs | O | the confirmed texts stand; the only text change in flight is #328's amendment 1 (already confirmed) | — |
    40	
    41	### Step 5: close the three PRs (the first measurement)
    42	
    43	| # | Sub-step | Who | Detail | Verifiable output |
    44	|---|---|---|---|---|
    45	| 5.0 | Ledger script | O | `pr-cost.sh <pr>`: rounds (Bot reviews, local reviews, revises), threads by priority, resets, first push → merge wall; one line appended to `.orchestration/metrics/pr-cost.tsv` | three lines by the end of step 5 |
    46	| 5.1 | #328 resume | O → W | lift the hold with `AGMSG-ACCEPTANCE v1 task_id=dotfiles-T128-playbook-rules-a04 status=revise` referencing the first RESULT (2026-10-12 16:04Z) and the amendment file already on main (TASK 935's hash); never a second TASK line (that would count as amendment 2 under INV-6) | the worker's RESULT with the new head |
    47	| 5.2 | #328 integrate | O | update-branch none (the worker merges main); CI; no Bot review (step 2); local review once; sweep (13 old rows + 3 new `fixed:` + advisory rows); receipt; audit; dispositions; thread resolution; sweep re-run; gate; `gh pr merge --squash --match-head-commit`; ff; ACCEPTANCE accepted | merged sha |
    48	| 5.3 | #329 integrate | O | a002 holds at 21badcd7: update-branch (one CI run); local review once; the record gets its 20 ledger rows (classes from titles) and advisory rows; receipt; audit; dispositions; resolution; sweep; gate; merge; ff; ACCEPTANCE accepted to a002 | merged sha |
    49	| 5.4 | #346 resume and integrate | O → W → O | lift a002/a003's hold for a02 PR-A with a PING ("resume: send your RESULT"); mark the draft ready (the Bot's one review); the same chain | merged sha |
    50	| 5.5 | Daily boundary (13) | O | the three acceptance records, the ledger, the receipts | merged |
    51	| 5.6 | Apply | OP | `make update` (needs the clean checkout 5.5 leaves) then restart Claude Code: #328's SKILL text takes effect only then | the applied SKILL contains the 20-minute sentence |
    52	
    53	### Step 6: tools before any further rule
    54	
    55	| # | Sub-step | Who | Detail | Verifiable output |
    56	|---|---|---|---|---|
    57	| 6.1 | a02 PR-B | W (a003) | acceptance-front-matter.py + orch-gate.sh + tests on the new gate; the orchestrator writes the a02 record's JSON block by hand once (the writer does not exist yet) | merged under steps 1–4 |
    58	| 6.2 | T704 | O (text) → W | the checkers promoted into `scripts/`; its task text in the step-7 short format with a hand-written minimal threat table (the exception: the generator is what it builds) | merged |
    59	| 6.3 | Retire the scratchpad chain | O | each chain step replaced by `scripts/orchestrator/*`; the scratchpad keeps only glue with no logic | the next integration's log names repository scripts only |
    60	
    61	### Step 7: the unit of change (after 6.2)
    62	
    63	| # | Sub-step | Who | Detail | Verifiable output |
    64	|---|---|---|---|---|
    65	| 7.1 | Template | O | `.orchestration/templates/task-short.md`: goal (one sentence), files, out of scope, one end-to-end check command, the checker-generated threat table | file on main |
    66	| 7.2 | Caps | O (practice) → OP (rule, step 8) | one mechanism per PR, ≤ 200 changed lines outside tests; text review one parallel round; overflow becomes the next PR's items | ledger |
    67	
    68	### Step 8: one amendment of the standing rules and the design (one operator action)
    69	
    70	| # | Sub-step | Who | Detail | Verifiable output |
    71	|---|---|---|---|---|
    72	| 8.1 | Draft | O | one patch with: plan 007 S6/S7 (advisory rows excluded; S7 asks asynchronous with a default; blocking only for P0), SKILL step 10 and 15 and `pr-integration.md` (P2 advisory with owner, one fix round, the merge rule, "no rule names an unlanded mechanism"), AGENTS.md's review bullet, and the design's INV-6 (resets only on a failed deterministic check or an unfixed P0/P1; P2 never counts) | patch file + `make render-check` |
    73	| 8.2 | Design review | O | one design-review round (seat + Codex in parallel) on the INV-6 sentence | receipt |
    74	| 8.3 | Apply | OP | the rules files are Claude-boundary (routing rule): the operator applies the patch and opens the PR, or seats a Codex worker for it; one PR | merged; `make update`; restart |
    75	
    76	### Step 9: merge queue (optional, last)
    77	
    78	| # | Sub-step | Who | Detail |
    79	|---|---|---|---|
    80	| 9.1 | Availability | OP | Settings → Rules → the ruleset: is "Require merge queue" offered for this user-owned public repository? |
    81	| 9.2 | CI | W | `merge_group` trigger in the required workflows (workflow files: threat rows) |
    82	| 9.3 | Ruleset | OP | Require merge queue on; strict up-to-date off |
    83	
    84	## Part B: scrutiny (what would have broken, and the fix in the plan)
    85	
    86	| # | Issue found | Kind | Resolution in Part A |
    87	|---|---|---|---|
    88	| S1 | "P2 advisory" conflicts with the operator's standing rule "not-applicable only with a refutation or an owner on main" | contradiction | 1.1–1.2: every advisory P2 has an owner task on main; no rule changes until 8.1 |
    89	| S2 | Plan 007 S6/S7 count ledger classes regardless of priority, so advisory rows would still trigger S1/S7 | contradiction | 1.4 interim exclusion stated in each record; 8.1 amends the rule (OP decision) |
    90	| S3 | Re-sending TASK 935 to lift the hold would be amendment 2 under INV-6 ("AGMSG-TASKs after the first") and trip the reset | error | 5.1 uses a revise ACCEPTANCE referencing the first RESULT; no second TASK line |
    91	| S4 | "One fix round" and "audit of the final head" conflict when the post-round audit finds a P0/P1 | ambiguity | 4.2: a surviving P0/P1 stops the PR (reset), never a second round |
    92	| S5 | If step 2 is not done before 5.1, #328's amendment head gets a Bot review; one more P1 head reaches INV-6's two (count now 1) | risk | 2.2 before 5.1; if OP declines, the risk is stated in the record and #328 proceeds anyway |
    93	| S6 | Step 7's generated threat table needs T704, whose own task text cannot use it | circularity | 6.2 exception stated |
    94	| S7 | Rule text (SKILL, rules, AGENTS.md) is Claude-boundary: the orchestrator and Claude workers may not edit it | routing | 8.3 one operator patch, batched, instead of per-step rule edits |
    95	| S8 | `make update` refuses a dirty main checkout; records are dirty between boundaries | mechanics | 5.6 after 5.5; `make update` only after a boundary |
    96	| S9 | The local review is a second sampler; running it on every head re-adds findings | consistency | 4.2: once per PR final head; its P2 advisory; idempotent per head already |
    97	| S10 | a002 idle since 05:39Z | omission | 5.3 uses it for #329's acceptance lines; after that it takes T704 or is removed |
    98	| S11 | Draft PRs are not reviewed by the Bot; marking #346 ready triggers its one review | mechanics | 5.4 marks it ready deliberately |
    99	| S12 | "At most one fix round per PR" is ambiguous for PRs with history | ambiguity | counted from the step's adoption; #328's amendment round is its one |
   100	| S13 | The gate's audit grammar has no `fixed:`; an audit P2 needs a `not-applicable:` line | consistency | 1.2's wording fits the grammar |
   101	| S14 | `resolve-threads.sh` replies must carry the owner wording | consistency | 1.2 |
   102	| S15 | The strict rule forces one CI run per PR after each merge of a sibling | cost, bounded | 3.3 lists them: two runs in total |
   103	| S16 | The scratchpad scripts remain the chain until 6.3, with known debts (the ff masker log) | debt | 6.3; no new scratchpad logic meanwhile |
   104	| S17 | INV-2 caps for #329 | check | the fixtures split (#340) kept #329 within the caps per its validation; re-checked at 5.3 |
   105	| S18 | Owner task files are orchestrator-authored | rule check | task files are the orchestrator's by the regime; boundaries are its exemption |
   106	| S19 | After step 2, the chain's Bot wait must not block on a review that will never come | mechanics | integrate-prep's `BOT_WAIT_MAX` set low for update-branch heads; the sweep still lists old threads |
   107	| S20 | Records staying local for a day | risk | files on disk, committed daily; acceptable |
   108	
   109	## Part C: the operator's items, each at its moment
   110	
   111	1. Now, before 5.1: read and set the Codex review trigger (2.1, 2.2) and tell me the values.
   112	2. Now: decide 1.4's interim counting (advisory rows excluded from class counts until 8.1) — yes or no.
   113	3. After 5.5: `make update` and restart Claude Code (5.6).
   114	4. At step 8: apply the one patch of rules and design (8.3), then `make update` and restart.
   115	5. At step 9 (optional): check merge-queue availability and set the ruleset.
   116	
   117	Everything else is the orchestrator's or a worker's.
   118	
   119	## Status
   120	
   121	- 13:33Z Step 2 done by the operator (screenshot 22:29 JST before, "変更済" after): Codex code review for this repository: automatic review on, scope all PRs, trigger **Smart detection (experimental) → On PR open**, comprehensive review **on → off** (the source of the P2 threads: 31 of 66; Codex's default scope is P0/P1). Security review unchanged (automatic on, trigger on PR creation, severity floor high / manual medium). Verification 2.3 pending on the next pushed head.
   122	- 13:33Z Step 1.4 (advisory rows excluded from the S7 class count until step 8 amends plan 007): no answer from the operator after two asks; proceeding on the stated default (excluded), recorded here and in each affected record; the operator may overrule at any time.
   123	- Waiting for the operator's go to start step 1.
   124	
   125	- 13:37Z Step 1.1 done: `dotfiles-T128-orchestrator-tools-followup-a01` and `dotfiles-T128-gate-evidence-followup-a01` written from their lineages' front matter, checker OK; 1.3 done: `fill_sweep.py` dispositions Codex P2/P3 as advisory owned by the PR's follow-up (map `followup-owners.tsv`: 328, 329, 346); step 5.0 `pr-cost.sh` written. The one pair round on the two files dispatched (seat + Codex in parallel).
   126	- 13:41Z Codex round 1 on the owner tasks: two P1 (the owned section does not exist before acceptance; "empty" did not cover "missing"); applied to all three owner tasks; round 2 prepared (three hashes); Codex round 2 running; the seat's round 1 RESULT pending.
   127	- 13:43Z Codex round 2: confirm on all three owner tasks (tools 44f746ce…, gate 4f68d63c…, playbook cb1d918a…; premises re-run match). The seat's round 1 (old hashes) still pending; round 2 (three hashes) goes to the seat on its RESULT. PR #329's record gained its 20 ledger rows (classes from titles).
   128	- 13:50Z seat round 2: confirm on all three (bus 943; two P3 notes recorded as items for the next change: the brief's stop condition 1 did not list the path-row rewrite; the inherited non-path rows name a02's binaries and #329's tests, true once those land). Codex round 3 confirmed tools and gate and asked revise on the playbook file only because my prompt described its diff as one sentence; round 4 runs with the corrected prompt.
   129	- 13:51Z step 1 done: the three owner tasks pair-confirmed (seat round 2, bus 943; Codex rounds 1 revise, 2 confirm, 3 confirm): tools ae208bef, gate 51c983df, playbook e22e0cc4. Boundary (12) runs now, then step 5.1.

**Reviewing task scope and data verification**
**Fixing JavaScript template literals**
exec
/bin/zsh -lc "python3 -B -c 'import subprocess,pathlib,hashlib,re,json
base=\"4e7a9b3ae0a1a80f2c7664ea54e3244224a7a672\"; head=\"65a3d71bf4e496252bf1ff51894974130c96cd43\"
def show(ref,path):return subprocess.check_output([\"git\",\"show\",ref+\":\"+path]).decode()
skill=\"home/dot_agents/skills/agmsg-orchestration/SKILL.md\";text=show(base,skill)
for i,l in enumerate(text.splitlines(),1):
 if any(l.startswith(s) for s in (\"- A task-file review is one round\",\"- A task that touches a trust boundary\",\"- Before every acceptance action\",\"6. Send \")):print(\"premise1\",i,l[:90])
for i,l in enumerate(show(base,\"AGENTS.md\").splitlines(),1):
 if \"Judge from the diff\" in l: print(\"premise2\",i,l[:60])
t=show(base,\"tests/unit/test_agmsg_orchestration_docs.py\").splitlines()
print(\"premise3\",\"\\n\".join(t[239:252]))
paths=subprocess.check_output([\"git\",\"diff\",\"--name-only\",base,head],text=True).splitlines()
print(\"changed paths\",len(paths))
for p in paths:
 s=show(head,p)
 if p.startswith(\".orchestration/\"):
  leaks=[i for i,l in enumerate(s.splitlines(),1) if re.search(r\"/(?:Users|home)/[A-Za-z0-9_-]+/\",l)]
  if leaks:print(\"HOME_PATH\",p,leaks)
  print(\"record\",p,\"lines\",len(s.splitlines()),\"sha256\",hashlib.sha256(s.encode()).hexdigest()[:12])
old=show(base,skill);new=show(head,skill)
for title in (\"## Worker Playbook\",\"## Message Contract v1\"):
 a=old.split(title,1)[1].split(\"\\n## \",1)[0];b=new.split(title,1)[1].split(\"\\n## \",1)[0];print(\"unchanged\",title,a==b)
prefix=\"- Before every acceptance action\"
print(\"counters unchanged\",next(l for l in old.splitlines() if l.startswith(prefix))==next(l for l in new.splitlines() if l.startswith(prefix)))
for v,c in ((\"a01\",\"1083a8c1\"),(\"a02\",\"4486dbdd\"),(\"a03\",\"196d73ca\")):
 p=f\".orchestration/dotfiles-T128-playbook-rules-{v}/task.md\"; print(\"historical task\",v,\"unchanged from\",c,show(head,p)==show(c,p))
'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 870ms:
premise1 69 - A task-file review is one round with a fixed stop condition: no contradiction with the d
premise1 71 - A task that touches a trust boundary (anything the design tier lists, CI that decides a 
premise1 72 - Before every acceptance action (revise, accept, merge) the orchestrator runs `scripts/re
premise1 162 6. Send `AGMSG-TASK v1` with the exact artifact paths and `done_signal=AGMSG-RESULT`. Pass
premise2 78 - Judge from the diff, whatever the task's metadata says, wh
premise3     def test_regime_rule_sections_are_pinned_whole(self) -> None:
        for name, path, outer, (start, end) in self.PINNED_SECTIONS:
            with self.subTest(section=name):
                text = path.read_text()
                if outer:
                    text = self.section(text, *outer)
                fixture = ROOT / "tests/fixtures/regime" / f"{name}.md"
                self.assertEqual(
                    self.normalized(start + self.section(text, start, end)),
                    self.normalized(fixture.read_text()),
                    f"regime rule section {name} changed: declare the change by updating "
                    f"tests/fixtures/regime/{name}.md in the same commit and listing it in the RESULT",
                )
changed paths 31
record .orchestration/dotfiles-T128-playbook-rules-a01/autoskill.md lines 3 sha256 236361ae7ba8
record .orchestration/dotfiles-T128-playbook-rules-a01/learning.md lines 7 sha256 18137b6f2b5e
record .orchestration/dotfiles-T128-playbook-rules-a01/report.md lines 49 sha256 bc1fd691e6c2
record .orchestration/dotfiles-T128-playbook-rules-a01/sandbox.md lines 26 sha256 ad61d4d4993f
record .orchestration/dotfiles-T128-playbook-rules-a01/task.md lines 84 sha256 b035ebd79add
record .orchestration/dotfiles-T128-playbook-rules-a01/validation.md lines 220 sha256 1001d405680f
record .orchestration/dotfiles-T128-playbook-rules-a02/autoskill.md lines 3 sha256 e71bb7806f41
record .orchestration/dotfiles-T128-playbook-rules-a02/learning.md lines 7 sha256 2209bc5bffb2
record .orchestration/dotfiles-T128-playbook-rules-a02/report.md lines 71 sha256 bc1b9c8f3056
record .orchestration/dotfiles-T128-playbook-rules-a02/sandbox.md lines 26 sha256 94c5a8afdcd9
record .orchestration/dotfiles-T128-playbook-rules-a02/task.md lines 90 sha256 07b78f643bc5
record .orchestration/dotfiles-T128-playbook-rules-a02/validation.md lines 362 sha256 18ca30b69be8
record .orchestration/dotfiles-T128-playbook-rules-a03/autoskill.md lines 3 sha256 a3a3cfe29d9a
record .orchestration/dotfiles-T128-playbook-rules-a03/learning.md lines 6 sha256 87536070fdbb
record .orchestration/dotfiles-T128-playbook-rules-a03/report.md lines 53 sha256 b17196c0797c
record .orchestration/dotfiles-T128-playbook-rules-a03/sandbox.md lines 21 sha256 7eeaaceb3c8f
record .orchestration/dotfiles-T128-playbook-rules-a03/task.md lines 92 sha256 ee6385184e3d
record .orchestration/dotfiles-T128-playbook-rules-a03/validation.md lines 183 sha256 8917cc2b84f7
record .orchestration/dotfiles-T128-playbook-rules-a04/autoskill.md lines 3 sha256 eb21fb19668d
record .orchestration/dotfiles-T128-playbook-rules-a04/learning.md lines 6 sha256 4556e853f825
record .orchestration/dotfiles-T128-playbook-rules-a04/report.md lines 71 sha256 aa5f5ff8c849
record .orchestration/dotfiles-T128-playbook-rules-a04/revise.yaml lines 7 sha256 24a7acff17d3
record .orchestration/dotfiles-T128-playbook-rules-a04/sandbox.md lines 27 sha256 4f1a19e3c61f
record .orchestration/dotfiles-T128-playbook-rules-a04/task.md lines 98 sha256 c5dbc2c3d351
record .orchestration/dotfiles-T128-playbook-rules-a04/validation.md lines 304 sha256 cd2682baad31
unchanged ## Worker Playbook True
unchanged ## Message Contract v1 True
counters unchanged True
historical task a01 unchanged from 1083a8c1 True
historical task a02 unchanged from 4486dbdd True
historical task a03 unchanged from 196d73ca True

**Reviewing test data and code diffs**
**Clarifying acceptance and invariants**
mcp: codex_apps/github.fetch_pr_comments started
mcp: codex_apps/github.fetch_pr_comments (completed)
exec
/bin/zsh -lc "git status --short; git show 65a3d71bf4e496252bf1ff51894974130c96cd43:home/dot_agents/skills/agmsg-orchestration/SKILL.md | nl -ba | sed -n '71,74p'; git log -1 --format='%h %s' a03c1daa; nl -ba .orchestration/validation/dotfiles-T128-playbook-rules-a04-pr-feedback.json | sed -n '358,370p'; sed -n '1,85p' scripts/require-crit-review.py" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 164ms:
 M .orchestration/acceptance/dotfiles-T128-playbook-rules-a04.md
 M .orchestration/reports/dotfiles-T128-playbook-rules-a04.md
 M .orchestration/sandboxes/dotfiles-T128-playbook-rules-a04.md
 M .orchestration/validation/dotfiles-T128-playbook-rules-a04-pr-feedback.json
 M .orchestration/validation/dotfiles-T128-playbook-rules-a04.md
?? .orchestration/validation/dotfiles-T128-playbook-rules-a04-audit-65a3d71.md
    71	- A task that touches a trust boundary (anything the design tier lists, CI that decides a required check, code that executes PR-controlled input) carries a `threat_table` in its front matter: one `{control, disposition}` row per thing the PR or the orchestrator controls (the tree and its tests, task.md, workflow files, interpreter and environment files, in-process effects, new or renamed scripts, metadata separators). The row unit is one row per `allowed_files` entry, one row per listed control that is not a path (task metadata, workflow and interpreter or environment inputs, in-process effects, new or renamed scripts, metadata separators), carried by the declared test module's row where that is where the control acts, and one row per orchestrator effect from the fixed list (forced removal, merge, update-branch); under a wildcard `allowed_files` entry whose files are executed or applied (scripts, workflows, hooks, settings, the rules seats follow), one row per concrete file the PR changes; a wildcard over test fixtures or other data files keeps one row; C4 of the task-consistency check (plan 007 T704) verifies the path half once it lands, and the task-file review checks it by hand until then. A disposition takes one of three forms: `closed: tests/<file>::<name>`, the test that closes the row; `residual: <sentence>`, the compensating control; `out-of-scope: <task id>`, the task that owns the row. Shape is `schemas/task.json`'s (wave V1): a `closed` selector names a test present in the PR tree at acceptance and in the schema's validation of the PR, an `out-of-scope` owner is a task id in the design's `implementing_tasks`, a `residual` payload is a sentence of at least 20 characters (the gate's minimum for a reason). Until `schemas/task.json` lands in wave V1, the task-file review checks the three shape rules by hand. For a `closed` row it checks the selector's form only, since the test does not exist before implementation. Substance is the reviewers': the task-file review, the Bot and the auditor judge each row against the diff. The table is the task's completion condition: a missing row is added once, counted as an amendment, never fixed finding by finding.
    72	- Before every acceptance action (revise, accept, merge) the orchestrator runs `scripts/regime-counters.sh <task id>` and pastes its output into the acceptance record. S2 is decided from INV-6's counts: each component the script prints is read from its output, and for each component it prints as `unknown` the record pastes the command and output that read the source INV-6 names for that component, or, while that source has no entry for the task, says so and pastes the reading of the interim record the orchestrator used in its place. S1 (plan 006: the same finding class three times on one artifact, from any reviewer) is decided from the record's finding-class table, which gives a class to every finding the PR-feedback sweep lists, whatever its disposition, and to every task-level audit finding; three rows of one class stop the artifact.
    73	- A change to a rule sentence requested of a worker travels as a task amendment (hashed, checked by the task-consistency check C1 to C6 once plan 007 T704 lands it and by hand until then, confirmed by the review seat), never as a PONG answer.
    74	- When a finding class reaches three on one artifact (the record's ledger) or `scripts/regime-counters.sh` prints an S1 candidate, the next acceptance action is the records search for that class, pasted into the record as the line `search: <class> -> <the matching mistake records or none>`, and the matching correction is applied when its mechanism is landed, or landed first when it is pending, mechanism by mechanism, before any dispatch; a class is a slug of `[a-z0-9-]` assigned at disposition time, never text taken from a review title. Once plan 007 T718 lands, `scripts/orchestrator/three-repeat.sh <class>` validates the slug, runs the records search and the CompactionDB search without a shell and prints the line; until then the orchestrator runs them by hand with a validated slug. Once `dotfiles-T128-gate-evidence-a02` lands, the gate refuses the action without the line; until then the orchestrator refuses it by rule. Every `not-applicable` disposition carries `; evidence=<command>` with the output pasted in the record.
a03c1daa feat(orchestrator): add dispatch, three-repeat and bus-read scripts; read S1 classes from the acceptance record (#336)
   358	      "bot": true,
   359	      "level": "comment",
   360	      "path": "home/dot_agents/skills/agmsg-orchestration/SKILL.md",
   361	      "line": 74,
   362	      "body": "**<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Reconcile counter candidates with slugged classes**\n\nFresh evidence in the amended head is that the two trigger paths still use incompatible class formats: `scripts/regime-counters.sh:145-147` emits the first three title words verbatim (the existing unit test expects `class=reject skipped contract`), while this rule requires the triggered class to be a `[a-z0-9-]` slug assigned during disposition. When that counter path reaches three, “search for that class” therefore supplies a non-slug with no defined mapping to the ledger class, so the required manual validation/search cannot proceed. Make the counter emit the assigned slug or explicitly resolve its candidate against the disposition ledger before searching.\n\nUseful? React with 👍 / 👎.",
   363	      "url": "https://github.com/mryfmo/dotfiles/pull/328#discussion_r4250028600",
   364	      "resolved": false,
   365	      "outdated": false,
   366	      "disposition": "fixed:a03c1daa"
   367	    },
   368	    {
   369	      "source": "review_comment",
   370	      "author": "chatgpt-codex-connector[bot]",
#!/usr/bin/env python3
"""Require native agent review for meaningful repository changes."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import subprocess
import tempfile
from collections import Counter
from functools import cache
import sys
from pathlib import Path


REVIEWED_ENV = "CRIT_REVIEWED"
NATIVE_REVIEWED_ENV = "AGENT_REVIEWED"
EVIDENCE_ENV = "REVIEW_EVIDENCE"
DISABLE_ENV = "CRIT_REVIEW"
PR_FEEDBACK_ENV = "PR_FEEDBACK_EVIDENCE"
AUDIT_ENV = "AUDIT_EVIDENCE"
AUDIT_DISPOSITIONS_ENV = "AUDIT_DISPOSITIONS"
PR_FEEDBACK_DISPOSITION = re.compile(r"(?:fixed:(?P<commit>[0-9a-f]{7,40})|not-applicable:(?P<reason>.*\S.*))", re.S)
FAILURE_REASON_MIN_CHARS = 20
# herdr-agents --audit names and concludes the task-level audit this way.
AUDIT_NAME = re.compile(r"(?P<task>.+)-audit-(?P<sha>[0-9a-f]{7,40})\.md")
AUDIT_VERDICT = re.compile(r"\s*Verdict: (correct|incorrect|blocked)\s*")
AUDIT_FINDING = re.compile(r"^\s*(?:[-*+]\s+)?\[P[0-3]\]", re.M)
AUDIT_FINDING_DISPOSITION_PREFIX = "audit-finding:"
AUDIT_FINDING_NUMBER = re.compile(rf"{AUDIT_FINDING_DISPOSITION_PREFIX}\s*(?P<number>\d+)\b")
# Levels whose not-applicable disposition needs a concrete reason: failures and
# runs that did not finish, so a work-in-progress run cannot be waved through.
STRICT_REASON_LEVELS = {
    "failure",
    "error",
    "cancelled",
    "timed_out",
    "action_required",
    "startup_failure",
    "stale",
    "in_progress",
    "queued",
    "pending",
}
BROAD_DIFF_FILE_LIMIT = 5
BROAD_DIFF_LINE_LIMIT = 200

IGNORED_PREFIXES = (".agents/worklog/",)

HIGH_RISK_PREFIXES = (
    ".codex/",
    ".claude/",
    "home/dot_agents/plugins/",
    "home/dot_agents/skills/",
    "home/dot_claude/",
    "home/dot_codex/",
    "home/dot_config/claude/",
    "home/dot_config/codex/",
    "home/dot_config/herdr/",
    "scripts/",
)

HIGH_RISK_FILES = {
    "AGENTS.md",
    "home/.chezmoiscripts/common/run_once_after_06-install-agent-assets.sh.tmpl",
    "home/dot_agents/agent-config.yaml",
    "home/dot_local/bin/common/executable_herdr-agents",
    "home/dot_zshrc",
    "tests/install/common/lifecycle.bats",
}

HIGH_RISK_TOKENS = (
    "ccgate",
    "crit",
    "agmsg",
    "herdr",
    "hook",
    "hooks",
    "plugin",
    "permission",
    "ponytail",
    "superpowers",

**Verifying audit data consistency**
**Drafting audit summary report**
mcp: codex_apps/github.fetch started
mcp: codex_apps/github.fetch (completed)
**Completing final verification steps**
**Finalizing verdict statement and formatting**
codex
Audited [PR #328](https://github.com/mryfmo/dotfiles/pull/328) at `65a3d71bf4e496252bf1ff51894974130c96cd43`. No P0/P1 defect found in the changed rules. The supplied integration evidence needs one correction.

- [P2] confidence=1.00 orchestration `.orchestration/validation/dotfiles-T128-playbook-rules-a04-pr-feedback.json:366` — `fixed:a03c1daa` cites an ancestor of base `4e7a9b3a`, outside the required `base..head` range; `scripts/require-crit-review.py:418` rejects it. Use an evidence-backed `not-applicable` disposition explaining that the base already contains the fix. This requires correcting the orchestrator’s evidence, not another implementation round.
- [P2] confidence=0.94 specification `home/dot_agents/skills/agmsg-orchestration/SKILL.md:164` — Initial acceptance-record creation is implicit. This is an advisory rule gap owned by `dotfiles-T128-playbook-rules-followup-a01`, **not a merge-blocking P0/P1**. Step 10.3 says to write the disposition summary; it does not prohibit earlier initialization. The existing counters rule already requires earlier record updates, and `dispatch.sh:217` rejects a missing supplied record before sending. The follow-up should explicitly require initialization before the first dispatch.

Verification: all three task premises hold; the amended task copy matches its recorded hash; the four corrections and fixtures match the task. All 47 documentation tests passed against Git objects at the specified head. GitHub confirms 12 successful check runs plus the successful CodeRabbit skip status. The sweep includes all 27 discussion items and all 16 Bot threads. Nothing was modified; local Bats tests were not run.

The task declares no `invariants` key. These are scoped checks of the design obligations directly changed by this task:

INV-2: holds home/dot_agents/skills/agmsg-orchestration/SKILL.md:69 — sentence equality is explicit; the diff stays within the caps.

INV-10: holds home/dot_agents/skills/agmsg-orchestration/SKILL.md:164 — the rule uses 20 minutes and explicitly distinguishes the script’s existing 30-minute flag.

INV-12: holds tests/unit/test_agmsg_orchestration_docs.py:519 — revised sentences have assertions and whole-section fixtures; existing protections remain.

Orchestration findings: 1

📝 まとめ: 読み取り専用監査を完了。記録作成時点の不足は後続タスク扱いで妥当ですが、統合前に範囲外コミットを指す disposition の修正が必要です。

Verdict: incorrect
hook: Stop
hook: Stop Completed
tokens used
168,877
Audited [PR #328](https://github.com/mryfmo/dotfiles/pull/328) at `65a3d71bf4e496252bf1ff51894974130c96cd43`. No P0/P1 defect found in the changed rules. The supplied integration evidence needs one correction.

- [P2] confidence=1.00 orchestration `.orchestration/validation/dotfiles-T128-playbook-rules-a04-pr-feedback.json:366` — `fixed:a03c1daa` cites an ancestor of base `4e7a9b3a`, outside the required `base..head` range; `scripts/require-crit-review.py:418` rejects it. Use an evidence-backed `not-applicable` disposition explaining that the base already contains the fix. This requires correcting the orchestrator’s evidence, not another implementation round.
- [P2] confidence=0.94 specification `home/dot_agents/skills/agmsg-orchestration/SKILL.md:164` — Initial acceptance-record creation is implicit. This is an advisory rule gap owned by `dotfiles-T128-playbook-rules-followup-a01`, **not a merge-blocking P0/P1**. Step 10.3 says to write the disposition summary; it does not prohibit earlier initialization. The existing counters rule already requires earlier record updates, and `dispatch.sh:217` rejects a missing supplied record before sending. The follow-up should explicitly require initialization before the first dispatch.

Verification: all three task premises hold; the amended task copy matches its recorded hash; the four corrections and fixtures match the task. All 47 documentation tests passed against Git objects at the specified head. GitHub confirms 12 successful check runs plus the successful CodeRabbit skip status. The sweep includes all 27 discussion items and all 16 Bot threads. Nothing was modified; local Bats tests were not run.

The task declares no `invariants` key. These are scoped checks of the design obligations directly changed by this task:

INV-2: holds home/dot_agents/skills/agmsg-orchestration/SKILL.md:69 — sentence equality is explicit; the diff stays within the caps.

INV-10: holds home/dot_agents/skills/agmsg-orchestration/SKILL.md:164 — the rule uses 20 minutes and explicitly distinguishes the script’s existing 30-minute flag.

INV-12: holds tests/unit/test_agmsg_orchestration_docs.py:519 — revised sentences have assertions and whole-section fixtures; existing protections remain.

Orchestration findings: 1

📝 まとめ: 読み取り専用監査を完了。記録作成時点の不足は後続タスク扱いで妥当ですが、統合前に範囲外コミットを指す disposition の修正が必要です。

Verdict: incorrect
