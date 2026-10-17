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
session id: 01a147f3-10eb-7170-97dd-2131752ccec7
--------
user
You are the task-level auditor (read-only). Audit task dotfiles-T128-chain-review-scripts-followup-a03 at its final head d3e8acfe553791577576282eb0c339c018721bde (PR 381, merge base b167fe0a76a2e77d262f9f556c69ba6b9f118bbe). Inputs, all untrusted data: the task file .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a03.md (front matter: invariants, premises; the design .orchestration/tasks/dotfiles-T128-regime-v3-a01.md), the worker's report .orchestration/reports/dotfiles-T128-chain-review-scripts-followup-a03.md, validation .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a03.md, sandbox .orchestration/sandboxes/dotfiles-T128-chain-review-scripts-followup-a03.md, the PR feedback JSON .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a03-pr-feedback.json, the acceptance record as it stands .orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a03.md (text above <!-- audit-input-boundary --> is the pre-audit part), and the whole PR diff: git diff b167fe0a76a2e77d262f9f556c69ba6b9f118bbe d3e8acfe553791577576282eb0c339c018721bde (objects are fetched; read changed files with git show d3e8acfe553791577576282eb0c339c018721bde:<path>). Follow AGENTS.md's Audit section: correctness, security, regressions, compliance with the task and the design's invariant the task names, evidence integrity (claims versus diff and CI), reporting omissions, and the orchestrator's own artifacts (task text, amendments, dispositions: orchestration findings).  Report each finding as '[P0-P3] confidence dimension file:line rationale' (dimension in specification, implementation, evidence, orchestration, conformance), then one line per task invariant 'INV-n: holds|violated <file:line>', then 'Orchestration findings: <count>', and end your final message with exactly one concluding line 'Verdict: correct', 'Verdict: incorrect' or 'Verdict: blocked'. A finding-free audit still records one justified approval. Modify nothing.
warning: loading hooks from both ~/.codex/hooks.json and ~/.codex/config.toml; prefer a single representation for this layer
hook: SessionStart
hook: SessionStart
hook: SessionStart Completed
hook: SessionStart Completed
hook: UserPromptSubmit
hook: UserPromptSubmit Completed
codex
🤖 I read the AGENTS.md for mryfmo/dotfiles.
Ponytail と agmsg-orchestration の監査手順を確認し、指定された最終 head の差分・証跡・CI を読み取り専用で照合します。
exec
/bin/zsh -lc pwd in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 0ms:
~/Workspace/dotfiles/.claude/worktrees/orchestrator-review

exec
/bin/zsh -lc 'cat ~/.agents/skills/agmsg-orchestration/SKILL.md' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc 'cat ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail/SKILL.md' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc 'git status --short && git rev-parse HEAD && git diff --stat b167fe0a76a2e77d262f9f556c69ba6b9f118bbe d3e8acfe553791577576282eb0c339c018721bde' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc 'cat ~/.agents/skills/gh-first-workflow/SKILL.md' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 82ms:
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

 succeeded in 169ms:
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

 succeeded in 198ms:
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

 succeeded in 214ms:
 M .orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a02.md
 M .orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a03.md
 M .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a03.md
?? .orchestration/reports/dotfiles-T128-chain-review-scripts-followup-a03.md
?? .orchestration/sandboxes/dotfiles-T128-chain-review-scripts-followup-a03.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a02-audit-8afc458.md.last.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a03-audit-d3e8acf.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a03-pr-feedback.json
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a03.md
b167fe0a76a2e77d262f9f556c69ba6b9f118bbe
 .../autoskill.md                                   |   3 +
 .../learning.md                                    |   7 +
 .../report.md                                      |  75 +++++++
 .../sandbox.md                                     |  27 +++
 .../task.md                                        | 106 ++++++++++
 .../validation.md                                  | 228 +++++++++++++++++++++
 scripts/orchestrator/local-advisory.sh             |  43 +++-
 tests/unit/test_chain_review_scripts.py            |  62 +++++-
 8 files changed, 544 insertions(+), 7 deletions(-)

**Auditing git clean tree**
codex
🐙 私は gh-first-workflow を読みました。
作業ツリーには監査入力の未コミット差分があるため、実装は指定 SHA の Git オブジェクトから読みます。タスク・受け入れ記録は指定された現状を確認し、ファイルや worklog は変更しません。
exec
/bin/zsh -lc 'cat .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a03.md .orchestration/reports/dotfiles-T128-chain-review-scripts-followup-a03.md .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a03.md .orchestration/sandboxes/dotfiles-T128-chain-review-scripts-followup-a03.md' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc 'gh pr view 381 --repo mryfmo/dotfiles --json url,headRefOid,baseRefOid,state,statusCheckRollup,reviews' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc 'cat .orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a03.md .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a03-pr-feedback.json' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc "rg -n 'task-level audit|"'^10'"\\.|threat_table|"'^## Orchestrator|''^## Task'"' ~/.agents/skills/agmsg-orchestration/SKILL.md && cat .ua/meta.json" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc 'git diff b167fe0a76a2e77d262f9f556c69ba6b9f118bbe d3e8acfe553791577576282eb0c339c018721bde -- scripts/orchestrator/local-advisory.sh tests/unit/test_chain_review_scripts.py' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 191ms:
---
format: 2
task_id: dotfiles-T128-chain-review-scripts-followup-a03
kind: code
security: false
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - scripts/orchestrator/local-advisory.sh
  - tests/unit/test_chain_review_scripts.py
  - .orchestration/dotfiles-T128-chain-review-scripts-followup-a03/**
after: [dotfiles-T128-chain-review-scripts-followup-a02]
threat_table:
  - control: the PR edits scripts/orchestrator/local-advisory.sh in two places, the refusal of an absent owner task file with the evidence that hashes the file (item 1a) and the class of a repeated finding (item 1b)
    disposition: "closed: tests/unit/test_chain_review_scripts.py::test_local_advisory_refuses_an_absent_owner_task_and_hashes_the_file"
  - control: "the class of a repeated finding (item 1b): a finding whose path:line token matches an earlier local review's finding takes that finding's class from the record"
    disposition: "closed: tests/unit/test_chain_review_scripts.py::test_local_advisory_classes_a_repeat_by_the_earlier_row"
  - control: the PR edits tests/unit/test_chain_review_scripts.py (two new tests beside the three and the ones the a02 owner task adds, which stay as they are; the temporary repository holds the local review files, the record and the owner task file the case writes)
    disposition: "residual: the fixtures are files the case writes; the audit reads each case against items 1a and 1b"
  - control: "the acceptance record and the owner task file (.orchestration/acceptance/<task>.md, .orchestration/tasks/<owner>.md in the checkout the script runs from): the script appends rows and lines to the record and reads the owner file's existence and sha256"
    disposition: "residual: the record is appended only, each row and line once (as today); the owner file is read, never written; a missing owner file is exit 2 before any row is written"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T128-chain-review-scripts-followup-a03/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T128-chain-review-scripts-followup-a03/ (report.md, validation.md, sandbox.md, learning.md)
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
    disposition: "residual: the test module imports only the standard library and runs the script as a bash subprocess with real git in a temporary repository; nothing is imported into another process"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; local-advisory.sh runs git rev-parse, grep, sed, cut, tr, head, sort and now shasum from PATH, as the lineage's scripts do; the tests' seam is the temporary repository as cwd; a PR checkout as cwd chooses nothing new, since the script already resolves the record and the review file from the repository root it runs in"
premises:
  - claim: 'local-advisory.sh on origin/main writes an advisory row without checking that the owner task file exists'
    command: 'git show origin/main:scripts/orchestrator/local-advisory.sh | /usr/bin/grep -c "write the owner task"'
    output: |-
      0
  - claim: 'local-advisory.sh on origin/main names git show origin/main as the row evidence, replayable only after the boundary'
    command: 'git show origin/main:scripts/orchestrator/local-advisory.sh | /usr/bin/grep -c "git show origin/main"'
    output: |-
      1
  - claim: 'local-advisory.sh on origin/main gives every row the class advisory-p2'
    command: 'git show origin/main:scripts/orchestrator/local-advisory.sh | /usr/bin/grep -c "advisory-p2"'
    output: |-
      2
  - claim: 'the chain-review test module on origin/main holds fourteen tests after the a01 and a02 owner PRs (#364 merged as fdef3ceb, #376 merged as f7847616) landed theirs; this task adds its own beside them'
    command: 'git show origin/main:tests/unit/test_chain_review_scripts.py | /usr/bin/grep -c "def test_"'
    output: |-
      14
---

# AGMSG-TASK dotfiles-T128-chain-review-scripts-followup-a03 — local-advisory.sh refuses an absent owner task, hashes the owner file as evidence, and classes a repeated finding by the record's earlier row (corrections C-51 (2) and C-50 (3); the chain-review-scripts lineage's next owner task; a Claude seat)

Written 2026-10-15 by the orchestrator seat (the bus time of its TASK line is the dispatch time), pair-reviewed before dispatch. Two corrections name this task as the landing of their tool half. C-51 (M-20261015-03): the chain wrote advisory rows whose owner task existed only as a name, with an evidence command (`git show origin/main:.orchestration/tasks/<owner>.md …`) that replays only after a boundary, and two audits raised it. C-50 (M-20261015-02): the class table gives every local advisory row the generic class `advisory-p2`, so a defect found again on a later head is never counted as a repeat of the same class and the three-rows rule cannot fire on it.

## Change (round 2, 2026-10-15T22:08:38Z)

The review seat's round 1 (confirm on `0d82d7c4`, five P3 taken as text fixes since the task waits for the a02 owner task): the owner check sits after the no-findings exit and before the heading; both refusals exit 2 with distinct messages; the token grammar ignores backticks and allows a line range, and the earlier number is the loop's; the scope (local review files and `local:` rows only) is stated against C-50's wider sentence; a repeat row's line names its provenance.

## Change (round 3, 2026-10-15T22:11:13Z)

The Codex half's round 2 (on `5bd7e601`): P3 the absent-owner case now asserts the record byte-identical to its pre-run content; P3 the repeat test adds a line-range token and two matching earlier heads with different classes, the later head's class winning.

## Goal

After the merge, `local-advisory.sh` writes no row whose owner task file is absent, its evidence command hashes that file in the checkout it runs from, and a finding repeated from an earlier head of the task takes the class the record gave the earlier finding.

## Files

1. `scripts/orchestrator/local-advisory.sh`: (a) after the script's existing exit 0 for a review without findings and before it writes the `## Owned by <owner>` heading, `.orchestration/tasks/<owner>.md` must exist in the repository root the script runs from, else it prints `write the owner task <owner> first` and exits 2 as well (the missing review file keeps its exit 2; the two messages tell them apart and the `@exitcode 2` line names both), so a refused run leaves the record untouched and a review without findings needs no owner file; the `evidence=` tail of each `local-finding:` line becomes `shasum -a 256 .orchestration/tasks/<owner>.md` with the file's sha256 at the time of writing appended as `(<sha256>)`, so the line replays in the orchestrator's checkout before the boundary; (b) each finding's token, the first run of path characters, `:` and digits with an optional `-<digits>` range in the finding's line (backticks around it ignored, so `` `a.sh:1` `` and `resolve-threads.sh:48-52` both count), is compared with the findings of the task's earlier local review files (`.orchestration/validation/<task>-local-review-*.md` other than the current head's), each numbered as this script's own loop numbers them (`sort -u` order, P0 and P1 lines included); when an earlier finding has the same token and the record holds a row `local:<sha7'>:<n'><TAB><class>` for it with a class other than `advisory-p2`, the new row takes that class, the latest matching head's row winning when two earlier files match with different classes, and its `local-finding:` line's parenthesis gains `repeat of local:<sha7'>:<n'>` so the provenance is on the line; otherwise `advisory-p2`, as today. The scope is the local review files and the `local:` rows only: a repeat first classed by a Bot thread's row or an `audit:` row keeps `advisory-p2`, since those rows carry no `path:line` token (C-50's wider sentence is applied here to the one source that has tokens). Nothing else changes (the P0/P1 stop, the heading, the once-only writes).
2. `tests/unit/test_chain_review_scripts.py`: two new tests in the module's style (the temporary repository, the script as a subprocess): `test_local_advisory_refuses_an_absent_owner_task_and_hashes_the_file` (no owner file: exit 2, `write the owner task` on stdout or stderr, and the record byte-identical to what the case wrote before the run, so no heading and no row appeared; with the owner file: exit 0, the `local-finding:` line's evidence names `shasum -a 256 .orchestration/tasks/<owner>.md` and the file's actual sha256) and `test_local_advisory_classes_a_repeat_by_the_earlier_row` (two earlier review files: the older with a finding at `scripts/x.sh:12` whose record row carries the class `quoting`, the newer with the same token whose row carries `env-s-quoting`, and the older also with a finding at `scripts/y.sh:3-5` whose row carries `range-case`; a current review file with a P2 at `` `scripts/x.sh:12` `` in backticks, one at `scripts/y.sh:3-5` and one at another token: the new rows are `env-s-quoting` (the later head's class wins), `range-case` (the line-range token matches) and `advisory-p2` respectively, and the first two rows' `local-finding:` lines hold `repeat of local:<sha7'>:<n'>` naming the matched head and number; a review without findings and no owner file: exit 0 and no heading written).

## Out of scope

`local-review.sh` and `sandbox-scan.sh` (the a02 owner task's and the lineage's); the chain scripts that call this one (T7's `chain-integrate.sh`); the record's class table beyond the rows this script writes.

## Check

`uv run python -m unittest tests/unit/test_chain_review_scripts.py -v` green (the module's tests and the two new ones), pasted in the validation file with `shellcheck scripts/orchestrator/local-advisory.sh` and `git diff --numstat origin/main...HEAD`: at most 200 changed lines (added plus deleted) outside `tests/` and outside `.orchestration/` (plan 021 step 7.2) and 1000 added lines under `tests/` (INV-2).

## Completion

One PR from a fresh branch off `origin/main` (after PR #376, the a02 owner task's PR, merged as f7847616 on 2026-10-17). The PR is ready for the orchestrator's integration when the ruleset's required checks are green, the Bot's review of the final head is in (at PR open, and once more on `@codex review` after a P0/P1 fix round: plan 020 step 2), every Bot thread is replied to and resolved by the orchestrator with its disposition, the validation file carries the outputs above, and the RESULT names every P0/P1 thread with `fixed:<sha>` and every P2 thread with the disposition the worker proposes; the orchestrator's audit of the final head is dispositioned finding by finding before the gate, and a P0/P1 it leaves is the operator's decision. The Bot's P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P0 or P1 that survives the round is listed as `open:<thread id>` with `bot_rounds=2` (the Bot's review at PR open and its re-review after the fix round), stops the PR and goes to the operator as a decision; a P2 on this PR's own change whose fix stays within `allowed_files` and is small (one flag or a few lines plus one test) is fixed in a revise round the orchestrator sends with a `check=` while INV-6's counts allow it (C-50); any other P2 is advisory, owned by `dotfiles-T128-chain-review-scripts-followup-a04`, which the orchestrator writes when the first advisory P2 appears, before the PR's dispositions (C-51), and recorded under `## Owned by dotfiles-T128-chain-review-scripts-followup-a04` in this task's acceptance record. The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`. The RESULT names head, base, branch, files, every Bot thread with its disposition, the test names per row, the caps, `task_copy=<sha256 of .orchestration/dotfiles-T128-chain-review-scripts-followup-a03/task.md>` and the evidence paths.

## Owned row (2026-10-16T05:53:07Z)

`audit:40f3be4:2` (advisory P2 of PR #364's final head): `test_local_advisory_matches_the_owner_heading_literally` has no fixture that fails under an anchored regex match, so the literal match of the owner heading (df92b402) is not isolated; add the heading `tXfollowup-a01` against the owner id `t.followup-a01` and assert it does not match (the test module is in allowed_files).

## Change (premises, 2026-10-17T00:26:15Z, before dispatch)

PRs #364 (fdef3ceb) and #376 (f7847616) landed the a01 and a02 owner tasks' tests, so premise 4 records the module's fourteen tests and the Completion clause names the a02 PR's merge; the owned row `audit:40f3be4:2` (the heading-test fixture) was added on 2026-10-16 after the pair-confirmed hash `d6b2108b`. Nothing else changes from `33e1c301`; re-confirmed Codex first (C-54).

## Change (Completion, 2026-10-17T00:29:55Z, before dispatch)

The Codex half's re-confirm (P3): the Completion clause still read `bot_rounds=1`; it is now the task template's clause of 2026-10-16 (`open:<thread id>` with `bot_rounds=2`, the C-50 revise round, every other P2 advisory and owned by `dotfiles-T128-chain-review-scripts-followup-a04` under `## Owned by dotfiles-T128-chain-review-scripts-followup-a04` in this task's acceptance record). Nothing else changes from `fd1f800a`.

---
task_id: dotfiles-T128-chain-review-scripts-followup-a03
seat: claude-standard-dot-a002
branch: tools/chain-review-scripts-followup-a03
base: f7847616
code_commit: a311781d
test_commit: a1ddb211
lint_commit: 9da0897a
pr: 381
task_sha256: e328a3fb8036d4b29b1ed798f42a967d66204bde810b62b84dd7048715c79ee2
---

# Report: dotfiles-T128-chain-review-scripts-followup-a03

- Seat: `claude-standard-dot-a002` in `.claude/worktrees/worker-f`, on a fresh branch `tools/chain-review-scripts-followup-a03` from `origin/main` `f7847616` (PR #376). The PR #377 and #378 branches stay in the worktree, committed and pushed, until their acceptance.
- Task file: sha256 `e328a3fb…`, copied byte-identical; the task-consistency check passes on the dispatched file (validation §1). Dispatched 2026-10-17T00:43:08Z. All four premises replay equal (§2). No question and no amendment.

## What changed in `scripts/orchestrator/local-advisory.sh`

Validation §2a holds the diff.

- **(a), C-51:**
  - **Owner check:** after the exit 0 for a review without findings and before the heading, `.orchestration/tasks/<owner>.md` must exist. Otherwise the script prints `write the owner task <owner> first` and exits 2, and the record is untouched. The missing review file keeps its own exit 2 and message, and the `@exitcode 2` line names both.
  - **Evidence:** each `local-finding:` line's tail is `evidence=shasum -a 256 .orchestration/tasks/<owner>.md (<sha256>)`, with the file's hash at the time of writing.
- **(b), C-50:**
  - **Token:** a finding's token is the first match of `[A-Za-z0-9._/-]+:[0-9]+(-[0-9]+)?` in its line. The class excludes the backtick, so a backticked token reads as itself.
  - **Earlier findings:** the earlier files are the task's other `.orchestration/validation/<task>-local-review-*.md`, each numbered as the loop numbers its own (`grep -E '^- \[P[0-3]\]' | sort -u`, P0 and P1 included). Their findings are compared by exact token, through `awk '$1 == t'`.
  - **Class:** the new row takes the class of the last `local:<sha7'>:<n'>` row in the record for a matching finding, skipping rows classed `advisory-p2`. Its `local-finding:` parenthesis gains `; repeat of local:<sha7'>:<n'>`. Otherwise the class is `advisory-p2`, as before.
  - **Scope:** only the local review files and the `local:` rows.
- **The header** describes both. The P0/P1 stop, the heading and the once-only writes are unchanged.

## Tests

The module has 16 tests, all OK (validation §3): the fourteen on `origin/main` and two new ones.

| Row | Test |
|---|---|
| 1a | `test_local_advisory_refuses_an_absent_owner_task_and_hashes_the_file`. With no owner file: exit 2, `write the owner task t-followup-a01 first`, and the record byte-identical to the case's pre-run content. With the owner file: the line ends `; evidence=shasum -a 256 .orchestration/tasks/t-followup-a01.md (<sha256 of that file>)`. |
| 1b | `test_local_advisory_classes_a_repeat_by_the_earlier_row`. **Earlier reviews:** `aaaaaa1` has `scripts/x.sh:12` (row `quoting`) and `scripts/y.sh:3-5` (row `range-case`); `bbbbbb2` has `scripts/x.sh:12` (row `env-s-quoting`, later in the record). **Current review `cccccc3`:** `` `scripts/x.sh:12` `` gets `env-s-quoting`, the later row winning; `scripts/y.sh:3-5` gets `range-case`; `scripts/y.sh:3-9` gets `advisory-p2`, being another token; `scripts/z.sh:7` gets `advisory-p2`. The first two lines name `repeat of local:bbbbbb2:1` and `repeat of local:aaaaaa1:2`. A review without findings and no owner file exits 0 with no heading. |
| owned row `audit:40f3be4:2` | `test_local_advisory_matches_the_owner_heading_literally` gains the heading `## Owned by tXfollowup-a01 (x)` beside the near-misses. A regex match of `t.followup-a01` would take it as the owner's heading and write none; the literal match writes the owner's heading once. |

The two existing local-advisory tests, `test_local_advisory_records_p2_rows_and_stops_on_p0_p1` and the heading test, each gain the owner file the new check requires. The first one's expected `local-finding:` line takes the new evidence form. Nothing else in them changes.

**Mutation check** (validation §4): 6 mutants, each a literal replacement applied alone, all 6 caught; then the baseline of 16 tests passes. They are:
- the owner check off;
- the old `git show origin/main` evidence;
- the repeat class off;
- the first matching row winning instead of the last;
- the line-range part of the token removed;
- the heading matched as a regex.

The first pass, on `a311781d`, had two survivors:
- the range token, untested until the `y.sh:3-9` case was added in `a1ddb211`;
- a backtick strip with no effect, since the token class already excludes the backtick. The strip was removed in `a1ddb211`, so that mutant is gone.

## Readings, declared

- **The evidence's `(<sha256>)` tail** is item 1a's form, verbatim. Replayed as shell, the parenthesis is a syntax error, so a replay runs the command before it and compares with the hash in parenthesis.
- **"Latest matching head wins"** is read, per the TASK note, as the last matching `local:` row in the record. Rows are appended in review order, so the record's order is the heads' order.
- **A repeat row** is skipped when its class is `advisory-p2` itself, so an unclassed earlier row never overrides a classed one.

## Caps

Validation §5: outside `tests/` and `.orchestration/`, 1 file, 38 added and 5 deleted, so 43 changed lines (cap 200); under `tests/`, 60 added lines (cap 1000).

## CI and the Bot

- **The Bot:** PR #381 was marked ready at 00:48:01Z. No review came within 10 minutes, so `@codex review` was posted at 603 s (issue comment `6227663819`). The Bot answered with issue comment `6227679116` at 00:59:47Z, "Didn't find any major issues", Reviewed commit `d2b33025d0`, which was then the head. No thread.
- **CI on `d2b33025`:** `test (ubuntu-24.04, client)` failed at `Run ShellCheck` with SC2015 (info) on `local-advisory.sh:61`, the line `k=$((k + 1)) && t=$(token "$l") && earlier+=… || true`, and three `test` jobs were cancelled with it. The local ShellCheck 0.11.0 reports nothing there. `9da0897a` writes the line as an `if` with no change of behaviour. CI's own command, `git ls-files -z 'setup.sh' 'install/*.sh' 'install/**/*.sh' 'scripts/*.sh' | xargs -0 shellcheck -x`, exits 0 locally. The 16 tests and the 6 mutants were re-run on it (validation §3 and §4). CI on the final head is in the RESULT.

## Not done, or outside scope

- `local-review.sh`, `sandbox-scan.sh` and `chain-integrate.sh` are unchanged.
- Understand-Anything hook: did not fire. plan-mode-used: no.
- cost: n/a (the runtime exposes no session figures to the seat).
---
task_id: dotfiles-T128-chain-review-scripts-followup-a03
seat: claude-standard-dot-a002
code_commit: 9da0897a
---

# Validation: dotfiles-T128-chain-review-scripts-followup-a03

Every command ran from the worktree `.claude/worktrees/worker-f`, inside the sandbox; `MAIN` names the main checkout and `T` the task id. `UV_OFFLINE=1` was set for every uv call. The output is verbatim, with the main checkout's path replaced by `$MAIN`, and each block ends with the exit status of the command shown (a pipeline's is its last command's). Premise 1's `grep -c` prints `0` and exits 1 when it finds nothing, which is the premise's expected output. §4's block shows the mutant script and its output, and each mutant line carries its own `rc`. Captured at `9da0897a` (the code `a311781d`, the test round `a1ddb211`, the CI ShellCheck fix `9da0897a`).

## 1. Task file and task copy
```console
$ shasum -a 256 "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md"; cmp "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md" && echo byte-identical
e328a3fb8036d4b29b1ed798f42a967d66204bde810b62b84dd7048715c79ee2  $MAIN/.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a03.md
e328a3fb8036d4b29b1ed798f42a967d66204bde810b62b84dd7048715c79ee2  .orchestration/dotfiles-T128-chain-review-scripts-followup-a03/task.md
byte-identical
[exit 0]
```
```console
$ uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root "$PWD" "$MAIN/.orchestration/tasks/$T.md"
dotfiles-T128-chain-review-scripts-followup-a03.md: OK
[exit 0]
```
## 2. Branch and the four premises
```console
$ git log --oneline origin/main..HEAD; git rev-parse origin/main
9da0897a fix(orchestrator): local-advisory.sh numbers each earlier finding with an if, not A && B || C (CI ShellCheck SC2015)
d2b33025 docs(orchestration): chain-review-scripts followup a03 task copy and evidence (a311781d, a1ddb211)
a1ddb211 test(orchestrator): the repeat test tells a line range from a wider one; the token reads a backticked path as itself (T128 chain-review-scripts followup a03)
a311781d fix(orchestrator): local-advisory.sh refuses an absent owner task, hashes the owner file as evidence, and classes a repeated finding by the earlier row (T128 chain-review-scripts followup a03)
f7847616970d6bd83739a75a65ad8f7c35e91462
[exit 0]
```
```console
$ git show origin/main:scripts/orchestrator/local-advisory.sh | /usr/bin/grep -c "write the owner task"
0
[exit 1]
```
```console
$ git show origin/main:scripts/orchestrator/local-advisory.sh | /usr/bin/grep -c "git show origin/main"
1
[exit 0]
```
```console
$ git show origin/main:scripts/orchestrator/local-advisory.sh | /usr/bin/grep -c "advisory-p2"
2
[exit 0]
```
```console
$ git show origin/main:tests/unit/test_chain_review_scripts.py | /usr/bin/grep -c "def test_"
14
[exit 0]
```
## 2a. The diff outside tests and the evidence
```console
$ git diff origin/main...HEAD -- scripts/
diff --git a/scripts/orchestrator/local-advisory.sh b/scripts/orchestrator/local-advisory.sh
index 409035cc..5e67ace7 100755
--- a/scripts/orchestrator/local-advisory.sh
+++ b/scripts/orchestrator/local-advisory.sh
@@ -4,14 +4,19 @@
 # @description
 #   Plan 020 step 1.2 for the local review. Reads `.orchestration/validation/<task>-local-review-<sha7>.md`. Each
 #   unique finding, numbered from 1: a P0/P1 prints STOP (the PR's one round is over: the plan's step 4.2); any
-#   other appends the row `local:<sha7>:<n><TAB>advisory-p2` under the heading `## Owned by <owner>` of
+#   other appends the row `local:<sha7>:<n><TAB><class>` under the heading `## Owned by <owner>` of
 #   `.orchestration/acceptance/<task>.md` (created when missing) and a `local-finding: <sha7>:<n>
-#   not-applicable:advisory P2 owned by <owner> (…); evidence=…` line, each only when the record lacks it.
+#   not-applicable:advisory P2 owned by <owner> (…); evidence=shasum -a 256 .orchestration/tasks/<owner>.md
+#   (<sha256>)` line, each only when the record lacks it. A review with findings needs the owner task file. The
+#   class is `advisory-p2`, unless the finding's `path:line[-line]` token (backticks ignored) matches a finding of
+#   the task's earlier local review files whose `local:` row in the record has another class: then the last such
+#   row's class, and the line's parenthesis names it as `repeat of local:<sha7>:<n>` (C-50).
 # @arg $1 string Task id, letters, digits, `.`, `_` and `-`.
 # @arg $2 string The reviewed head, 40 hex characters.
 # @arg $3 string The task id that owns the advisory findings, in the task id's form.
 # @exitcode 0 No P0/P1 finding.
-# @exitcode 2 No local review file, or a malformed task id, head or owner task id.
+# @exitcode 2 No local review file, a malformed task id, head or owner task id, or (for a review with findings) no
+#   owner task file: `write the owner task <owner> first`.
 # @exitcode 3 A P0/P1 finding.
 # @example
 #   scripts/orchestrator/local-advisory.sh dotfiles-T128-x-a01 "$head" dotfiles-T128-x-followup-a01
@@ -37,6 +42,26 @@ n=$(sed -n 's/^findings: //p' "$LR" | head -1)
     echo "local review of $h7: no findings"
     exit 0
 }
+# The rows name the owner task, so it must exist; its hash is evidence that replays before the boundary (C-51).
+O=".orchestration/tasks/$owner.md"
+[ -f "$O" ] || {
+    echo "write the owner task $owner first"
+    exit 2
+}
+sha=$(shasum -a 256 "$O" | cut -d' ' -f1)
+# C-50: a finding repeated from an earlier head takes the class the record gave it. Each earlier review's findings,
+# numbered as the loop below numbers them, as `<path:line[-line]> local:<sha7>:<n>` lines.
+# The class excludes the backtick, so `a.sh:1` in backticks reads as a.sh:1.
+token() { [[ $1 =~ ([A-Za-z0-9._/-]+:[0-9]+(-[0-9]+)?) ]] && printf '%s\n' "${BASH_REMATCH[1]}"; }
+earlier=""
+for f in .orchestration/validation/"$task"-local-review-*.md; do
+    [[ -f $f && $f != "$LR" ]] || continue
+    e=${f%.md} && e=${e##*-local-review-} && k=0
+    while IFS= read -r l; do
+        k=$((k + 1))
+        if t=$(token "$l"); then earlier+="$t local:$e:$k"$'\n'; fi
+    done < <(/usr/bin/grep -E '^- \[P[0-3]\]' "$f" | sort -u)
+done
 # A literal heading match, ended by a space or the line's end: a . in the owner is no wildcard, a longer id no match.
 awk -v h="## Owned by $owner" 'substr($0, 1, length(h)) == h && substr($0, length(h) + 1, 1) ~ /^ ?$/ { f = 1 } END { exit !f }' "$A" 2> /dev/null || printf '\n## Owned by %s (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)\n\n' "$owner" >> "$A"
 i=0 stop=0
@@ -48,8 +73,16 @@ while IFS= read -r line; do
         stop=1
         ;;
     *)
-        /usr/bin/grep -q "^local:$h7:$i	" "$A" || printf 'local:%s:%s\tadvisory-p2\n' "$h7" "$i" >> "$A"
-        /usr/bin/grep -q "^local-finding: $h7:$i " "$A" || printf 'local-finding: %s:%s not-applicable:advisory P2 owned by %s (%s); evidence=git show origin/main:.orchestration/tasks/%s.md | grep -n '"'"'item 1'"'"'\n' "$h7" "$i" "$owner" "$(printf '%s' "$line" | cut -c1-120 | tr -d '`')" "$owner" >> "$A"
+        # The last row in the record of an earlier finding with this token, other than advisory-p2, wins.
+        class=advisory-p2 repeat=""
+        t=$(token "$line") || t=""
+        ids=$(printf '%s' "$earlier" | awk -v t="$t" '$1 == t { print $2 }' | tr '\n' '|')
+        if [[ -n $t && -n $ids ]]; then
+            row=$(/usr/bin/grep -E "^(${ids%|})	" "$A" | /usr/bin/grep -v '	advisory-p2$' | tail -1 || true)
+            [ -z "$row" ] || class=${row#*	} repeat="; repeat of ${row%%	*}"
+        fi
+        /usr/bin/grep -q "^local:$h7:$i	" "$A" || printf 'local:%s:%s\t%s\n' "$h7" "$i" "$class" >> "$A"
+        /usr/bin/grep -q "^local-finding: $h7:$i " "$A" || printf 'local-finding: %s:%s not-applicable:advisory P2 owned by %s (%s%s); evidence=shasum -a 256 %s (%s)\n' "$h7" "$i" "$owner" "$(printf '%s' "$line" | cut -c1-120 | tr -d '`')" "$repeat" "$O" "$sha" >> "$A"
         ;;
     esac
 done < <(/usr/bin/grep -E '^- \[P[0-3]\]' "$LR" | sort -u)
[exit 0]
```
## 3. The Check
```console
$ uv run python -m unittest tests/unit/test_chain_review_scripts.py -v
test_local_advisory_classes_a_repeat_by_the_earlier_row (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_advisory_classes_a_repeat_by_the_earlier_row) ... ok
test_local_advisory_matches_the_owner_heading_literally (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_advisory_matches_the_owner_heading_literally) ... ok
test_local_advisory_records_p2_rows_and_stops_on_p0_p1 (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_advisory_records_p2_rows_and_stops_on_p0_p1) ... ok
test_local_advisory_refuses_a_malformed_owner_id (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_advisory_refuses_a_malformed_owner_id) ... ok
test_local_advisory_refuses_an_absent_owner_task_and_hashes_the_file (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_advisory_refuses_an_absent_owner_task_and_hashes_the_file) ... ok
test_local_review_and_local_advisory_refuse_a_task_or_head_that_leaves_their_directory (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_review_and_local_advisory_refuse_a_task_or_head_that_leaves_their_directory) ... ok
test_local_review_keeps_env_S_shebang_arguments (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_review_keeps_env_S_shebang_arguments) ... ok
test_local_review_pins_the_review_binary_interpreter (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_review_pins_the_review_binary_interpreter) ... ok
test_local_review_refuses_a_quoted_env_S_shebang (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_review_refuses_a_quoted_env_S_shebang) ... ok
test_local_review_resolves_codex_through_mise_and_refuses_a_shim (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_review_resolves_codex_through_mise_and_refuses_a_shim) ... ok
test_local_review_resolves_the_review_binary_before_the_checkout (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_review_resolves_the_review_binary_before_the_checkout) ... ok
test_local_review_reuses_only_a_file_that_records_this_head (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_review_reuses_only_a_file_that_records_this_head) ... ok
test_local_review_runs_the_review_binary_read_only_at_the_head_and_writes_one_file (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_review_runs_the_review_binary_read_only_at_the_head_and_writes_one_file) ... ok
test_local_review_strips_a_worktree_path_holding_sed_syntax_literally (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_review_strips_a_worktree_path_holding_sed_syntax_literally) ... ok
test_local_review_writes_no_file_when_the_review_binary_fails (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_review_writes_no_file_when_the_review_binary_fails) ... ok
test_sandbox_scan_prints_the_unsandboxed_mutation_calls (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_sandbox_scan_prints_the_unsandboxed_mutation_calls) ... ok

----------------------------------------------------------------------
Ran 16 tests in 7.404s

OK
[exit 0]
```
```console
$ shellcheck scripts/orchestrator/local-advisory.sh && echo clean
clean
[exit 0]
```
```console
$ shfmt -i 4 -sr -d scripts/orchestrator/local-advisory.sh && echo clean
clean
[exit 0]
```
```console
$ ruff check --config ruff.toml tests/unit/test_chain_review_scripts.py && ruff format --config ruff.toml --check tests/unit/test_chain_review_scripts.py
All checks passed!
1 file already formatted
[exit 0]
```
## 4. Mutation check (each mutant a literal string replacement applied alone, its test run, the file restored with git checkout; then a baseline run)
```console
$ bash "$TMPDIR/crs3/mutate.sh" (the script, then its output)
S=scripts/orchestrator/local-advisory.sh T=tests/unit/test_chain_review_scripts.py
lrun() { # label old new test: a literal string replacement (python's str.replace, once), the test, the restore
    python3 -I -c 'import sys; p, a, b = sys.argv[1:]; t = open(p).read(); assert t.count(a) == 1, a; open(p, "w").write(t.replace(a, b))' "$S" "$2" "$3"
    git diff -U0 -- "$S" | /usr/bin/grep -v -E '^(---|\+\+\+|@@|diff|index)' || echo "(nothing changed)"
    UV_OFFLINE=1 uv run python -m unittest "$T" -k "$4" > "$TMPDIR/crs3/m.log" 2>&1
    echo "mutant=$1 test=$4 rc=$? $(tail -1 "$TMPDIR/crs3/m.log")"
    git checkout -- "$S"
}
A=test_local_advisory_refuses_an_absent_owner_task_and_hashes_the_file R=test_local_advisory_classes_a_repeat_by_the_earlier_row H=test_local_advisory_matches_the_owner_heading_literally
lrun owner-check-off '[ -f "$O" ] ||' 'true ||' $A
lrun old-evidence 'evidence=shasum -a 256 %s (%s)\n'"'"' "$h7" "$i" "$owner" "$(printf '"'"'%s'"'"' "$line" | cut -c1-120 | tr -d '"'"'`'"'"')" "$repeat" "$O" "$sha"' 'evidence=git show origin/main:%s | grep -n item\n'"'"' "$h7" "$i" "$owner" "$(printf '"'"'%s'"'"' "$line" | cut -c1-120 | tr -d '"'"'`'"'"')" "$repeat" "$O"' $A
lrun repeat-off '[ -z "$row" ] || class=' 'true || class=' $R
lrun first-row-wins '| tail -1 || true)' '| head -1 || true)' $R
lrun range-token-off ':[0-9]+(-[0-9]+)?)' ':[0-9]+)' $R
lrun heading-as-regex 'substr($0, 1, length(h)) == h && substr($0, length(h) + 1, 1) ~ /^ ?$/' '$0 ~ "^" h' $H
UV_OFFLINE=1 uv run python -m unittest "$T" > "$TMPDIR/crs3/m.log" 2>&1; echo "baseline rc=$? $(tail -1 "$TMPDIR/crs3/m.log")"
git status --short -- scripts/
--- output
-[ -f "$O" ] || {
+true || {
mutant=owner-check-off test=test_local_advisory_refuses_an_absent_owner_task_and_hashes_the_file rc=1 FAILED (failures=1)
-        /usr/bin/grep -q "^local-finding: $h7:$i " "$A" || printf 'local-finding: %s:%s not-applicable:advisory P2 owned by %s (%s%s); evidence=shasum -a 256 %s (%s)\n' "$h7" "$i" "$owner" "$(printf '%s' "$line" | cut -c1-120 | tr -d '`')" "$repeat" "$O" "$sha" >> "$A"
+        /usr/bin/grep -q "^local-finding: $h7:$i " "$A" || printf 'local-finding: %s:%s not-applicable:advisory P2 owned by %s (%s%s); evidence=git show origin/main:%s | grep -n item\n' "$h7" "$i" "$owner" "$(printf '%s' "$line" | cut -c1-120 | tr -d '`')" "$repeat" "$O" >> "$A"
mutant=old-evidence test=test_local_advisory_refuses_an_absent_owner_task_and_hashes_the_file rc=1 FAILED (failures=1)
-            [ -z "$row" ] || class=${row#*	} repeat="; repeat of ${row%%	*}"
+            true || class=${row#*	} repeat="; repeat of ${row%%	*}"
mutant=repeat-off test=test_local_advisory_classes_a_repeat_by_the_earlier_row rc=1 FAILED (failures=1)
-            row=$(/usr/bin/grep -E "^(${ids%|})	" "$A" | /usr/bin/grep -v '	advisory-p2$' | tail -1 || true)
+            row=$(/usr/bin/grep -E "^(${ids%|})	" "$A" | /usr/bin/grep -v '	advisory-p2$' | head -1 || true)
mutant=first-row-wins test=test_local_advisory_classes_a_repeat_by_the_earlier_row rc=1 FAILED (failures=1)
-token() { [[ $1 =~ ([A-Za-z0-9._/-]+:[0-9]+(-[0-9]+)?) ]] && printf '%s\n' "${BASH_REMATCH[1]}"; }
+token() { [[ $1 =~ ([A-Za-z0-9._/-]+:[0-9]+) ]] && printf '%s\n' "${BASH_REMATCH[1]}"; }
mutant=range-token-off test=test_local_advisory_classes_a_repeat_by_the_earlier_row rc=1 FAILED (failures=1)
-awk -v h="## Owned by $owner" 'substr($0, 1, length(h)) == h && substr($0, length(h) + 1, 1) ~ /^ ?$/ { f = 1 } END { exit !f }' "$A" 2> /dev/null || printf '\n## Owned by %s (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)\n\n' "$owner" >> "$A"
+awk -v h="## Owned by $owner" '$0 ~ "^" h { f = 1 } END { exit !f }' "$A" 2> /dev/null || printf '\n## Owned by %s (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)\n\n' "$owner" >> "$A"
mutant=heading-as-regex test=test_local_advisory_matches_the_owner_heading_literally rc=1 FAILED (failures=1)
baseline rc=0 OK
[exit 0]
```
## 5. Caps
```console
$ git diff --numstat origin/main...HEAD
3	0	.orchestration/dotfiles-T128-chain-review-scripts-followup-a03/autoskill.md
6	0	.orchestration/dotfiles-T128-chain-review-scripts-followup-a03/learning.md
72	0	.orchestration/dotfiles-T128-chain-review-scripts-followup-a03/report.md
27	0	.orchestration/dotfiles-T128-chain-review-scripts-followup-a03/sandbox.md
106	0	.orchestration/dotfiles-T128-chain-review-scripts-followup-a03/task.md
219	0	.orchestration/dotfiles-T128-chain-review-scripts-followup-a03/validation.md
38	5	scripts/orchestrator/local-advisory.sh
60	2	tests/unit/test_chain_review_scripts.py
[exit 0]
```
---
task_id: dotfiles-T128-chain-review-scripts-followup-a03
seat: claude-standard-dot-a002
permission_gated_commands: see the table
---

# Sandbox record: dotfiles-T128-chain-review-scripts-followup-a03

- Period: from the AGMSG-TASK (2026-10-17T00:43:08Z) to the RESULT.
- Inside the sandbox ran:
  - the HTTPS `git fetch` and `git push`;
  - the branch, the commits and the evidence;
  - every test, lint and mutation run.
- uv ran with `UV_OFFLINE=1`.
- No local mutation was chained onto a call that ran outside the sandbox.

Calls outside the sandbox: `gh` through the permission gate (`dangerouslyDisableSandbox`) and `agmsg-dispatch` through `excludedCommands`. These rows are planned in advance, so no evidence update moves the head after the Bot's review:

| # | Command | Step 4 case |
|--:|---|---|
| 1 | `gh pr create --draft --repo mryfmo/dotfiles --base main --head tools/chain-review-scripts-followup-a03 …` | `gh` |
| 2 | `gh pr ready <pr>` | `gh` |
| 3 | the Bot wait (`bot-wait.sh`, background; `gh pr view`, `gh api` reads, and `gh pr comment … '@codex review'` only at 10 minutes without a review) | `gh` |
| 4 | `gh pr checks <pr> --watch` (background, exit status joined) | `gh` |
| 5 | `gh api` reads of the Bot's review and comments on the head | `gh` |
| 6 | after a P0/P1 fix round only: the push, then `gh pr comment <pr> --body '@codex review'` and the same Bot wait for the re-review (`bot_rounds=2`) | `gh` |
| 7 | `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T128-chain-review-scripts-followup-a03 …` | `agmsg-dispatch` |

 succeeded in 254ms:
diff --git a/scripts/orchestrator/local-advisory.sh b/scripts/orchestrator/local-advisory.sh
index 409035cc..5e67ace7 100755
--- a/scripts/orchestrator/local-advisory.sh
+++ b/scripts/orchestrator/local-advisory.sh
@@ -4,14 +4,19 @@
 # @description
 #   Plan 020 step 1.2 for the local review. Reads `.orchestration/validation/<task>-local-review-<sha7>.md`. Each
 #   unique finding, numbered from 1: a P0/P1 prints STOP (the PR's one round is over: the plan's step 4.2); any
-#   other appends the row `local:<sha7>:<n><TAB>advisory-p2` under the heading `## Owned by <owner>` of
+#   other appends the row `local:<sha7>:<n><TAB><class>` under the heading `## Owned by <owner>` of
 #   `.orchestration/acceptance/<task>.md` (created when missing) and a `local-finding: <sha7>:<n>
-#   not-applicable:advisory P2 owned by <owner> (…); evidence=…` line, each only when the record lacks it.
+#   not-applicable:advisory P2 owned by <owner> (…); evidence=shasum -a 256 .orchestration/tasks/<owner>.md
+#   (<sha256>)` line, each only when the record lacks it. A review with findings needs the owner task file. The
+#   class is `advisory-p2`, unless the finding's `path:line[-line]` token (backticks ignored) matches a finding of
+#   the task's earlier local review files whose `local:` row in the record has another class: then the last such
+#   row's class, and the line's parenthesis names it as `repeat of local:<sha7>:<n>` (C-50).
 # @arg $1 string Task id, letters, digits, `.`, `_` and `-`.
 # @arg $2 string The reviewed head, 40 hex characters.
 # @arg $3 string The task id that owns the advisory findings, in the task id's form.
 # @exitcode 0 No P0/P1 finding.
-# @exitcode 2 No local review file, or a malformed task id, head or owner task id.
+# @exitcode 2 No local review file, a malformed task id, head or owner task id, or (for a review with findings) no
+#   owner task file: `write the owner task <owner> first`.
 # @exitcode 3 A P0/P1 finding.
 # @example
 #   scripts/orchestrator/local-advisory.sh dotfiles-T128-x-a01 "$head" dotfiles-T128-x-followup-a01
@@ -37,6 +42,26 @@ n=$(sed -n 's/^findings: //p' "$LR" | head -1)
     echo "local review of $h7: no findings"
     exit 0
 }
+# The rows name the owner task, so it must exist; its hash is evidence that replays before the boundary (C-51).
+O=".orchestration/tasks/$owner.md"
+[ -f "$O" ] || {
+    echo "write the owner task $owner first"
+    exit 2
+}
+sha=$(shasum -a 256 "$O" | cut -d' ' -f1)
+# C-50: a finding repeated from an earlier head takes the class the record gave it. Each earlier review's findings,
+# numbered as the loop below numbers them, as `<path:line[-line]> local:<sha7>:<n>` lines.
+# The class excludes the backtick, so `a.sh:1` in backticks reads as a.sh:1.
+token() { [[ $1 =~ ([A-Za-z0-9._/-]+:[0-9]+(-[0-9]+)?) ]] && printf '%s\n' "${BASH_REMATCH[1]}"; }
+earlier=""
+for f in .orchestration/validation/"$task"-local-review-*.md; do
+    [[ -f $f && $f != "$LR" ]] || continue
+    e=${f%.md} && e=${e##*-local-review-} && k=0
+    while IFS= read -r l; do
+        k=$((k + 1))
+        if t=$(token "$l"); then earlier+="$t local:$e:$k"$'\n'; fi
+    done < <(/usr/bin/grep -E '^- \[P[0-3]\]' "$f" | sort -u)
+done
 # A literal heading match, ended by a space or the line's end: a . in the owner is no wildcard, a longer id no match.
 awk -v h="## Owned by $owner" 'substr($0, 1, length(h)) == h && substr($0, length(h) + 1, 1) ~ /^ ?$/ { f = 1 } END { exit !f }' "$A" 2> /dev/null || printf '\n## Owned by %s (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)\n\n' "$owner" >> "$A"
 i=0 stop=0
@@ -48,8 +73,16 @@ while IFS= read -r line; do
         stop=1
         ;;
     *)
-        /usr/bin/grep -q "^local:$h7:$i	" "$A" || printf 'local:%s:%s\tadvisory-p2\n' "$h7" "$i" >> "$A"
-        /usr/bin/grep -q "^local-finding: $h7:$i " "$A" || printf 'local-finding: %s:%s not-applicable:advisory P2 owned by %s (%s); evidence=git show origin/main:.orchestration/tasks/%s.md | grep -n '"'"'item 1'"'"'\n' "$h7" "$i" "$owner" "$(printf '%s' "$line" | cut -c1-120 | tr -d '`')" "$owner" >> "$A"
+        # The last row in the record of an earlier finding with this token, other than advisory-p2, wins.
+        class=advisory-p2 repeat=""
+        t=$(token "$line") || t=""
+        ids=$(printf '%s' "$earlier" | awk -v t="$t" '$1 == t { print $2 }' | tr '\n' '|')
+        if [[ -n $t && -n $ids ]]; then
+            row=$(/usr/bin/grep -E "^(${ids%|})	" "$A" | /usr/bin/grep -v '	advisory-p2$' | tail -1 || true)
+            [ -z "$row" ] || class=${row#*	} repeat="; repeat of ${row%%	*}"
+        fi
+        /usr/bin/grep -q "^local:$h7:$i	" "$A" || printf 'local:%s:%s\t%s\n' "$h7" "$i" "$class" >> "$A"
+        /usr/bin/grep -q "^local-finding: $h7:$i " "$A" || printf 'local-finding: %s:%s not-applicable:advisory P2 owned by %s (%s%s); evidence=shasum -a 256 %s (%s)\n' "$h7" "$i" "$owner" "$(printf '%s' "$line" | cut -c1-120 | tr -d '`')" "$repeat" "$O" "$sha" >> "$A"
         ;;
     esac
 done < <(/usr/bin/grep -E '^- \[P[0-3]\]' "$LR" | sort -u)
diff --git a/tests/unit/test_chain_review_scripts.py b/tests/unit/test_chain_review_scripts.py
index e4c670d9..5fe61cb8 100644
--- a/tests/unit/test_chain_review_scripts.py
+++ b/tests/unit/test_chain_review_scripts.py
@@ -6,6 +6,7 @@ working directory, the HEAD there, PATH and its stdin to `<calls>/<name>.log`, p
 `<calls>/status` (0 when absent).
 """
 
+import hashlib
 import os
 import re
 import subprocess
@@ -351,6 +352,7 @@ class ChainReviewScriptsTest(unittest.TestCase):
     def test_local_advisory_records_p2_rows_and_stops_on_p0_p1(self):
         head, owner = "abcdef0" + "1" * 33, "t-followup-a01"
         record = self.write(".orchestration/acceptance/t-a01.md", "# record\n")
+        sha = hashlib.sha256(self.write(f".orchestration/tasks/{owner}.md", "owner\n").read_bytes()).hexdigest()
         heading = f"## Owned by {owner} (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)\n"
         # Numbered in sort order; the second is cut to 120 characters, then loses its backticks.
         first, long = "- [P2] `a.sh:1` first", "- [P2] `b.sh:3` " + "y" * 130
@@ -365,7 +367,7 @@ class ChainReviewScriptsTest(unittest.TestCase):
             text = finding[:120].replace("`", "")
             return (
                 f"local-finding: abcdef0:{n} not-applicable:advisory P2 owned by {owner} ({text}); "
-                f"evidence=git show origin/main:.orchestration/tasks/{owner}.md | grep -n 'item 1'\n"
+                f"evidence=shasum -a 256 .orchestration/tasks/{owner}.md ({sha})\n"
             )
 
         review(long, first)
@@ -410,14 +412,70 @@ class ChainReviewScriptsTest(unittest.TestCase):
         # A dotted owner is no wildcard, and a longer id that starts with the owner is another owner.
         head = "abcdef0" + "1" * 33
         self.write(f".orchestration/validation/t-a01-local-review-{head[:7]}.md", "---\nfindings: 1\n---\n\n- [P2] x\n")
-        near = "# record\n## Owned by t-followupXa01 (x)\n## Owned by t.followup-a01b (x)\n"
+        # tXfollowup-a01 matches t.followup-a01 as a regex, anchored or not (the audit of 40f3be4, finding 2).
+        near = "# record\n## Owned by t-followupXa01 (x)\n## Owned by t.followup-a01b (x)\n## Owned by tXfollowup-a01 (x)\n"
         record = self.write(".orchestration/acceptance/t-a01.md", near)
+        self.write(".orchestration/tasks/t.followup-a01.md", "owner\n")
         self.run_tool("local-advisory.sh", "t-a01", head, "t.followup-a01")
         self.assertEqual(1, record.read_text().count("\n## Owned by t.followup-a01 (advisory P2"))
         self.run_tool("local-advisory.sh", "t-a01", head, "t.followup-a01")
         self.assertEqual(1, record.read_text().count("\n## Owned by t.followup-a01 (advisory P2"))
         self.assertTrue(record.read_text().startswith(near))
 
+    def test_local_advisory_refuses_an_absent_owner_task_and_hashes_the_file(self):
+        # C-51: no row names an owner task that does not exist, and the evidence replays before the boundary.
+        head, owner = "abcdef0" + "1" * 33, "t-followup-a01"
+        self.write(f".orchestration/validation/t-a01-local-review-{head[:7]}.md", "---\nfindings: 1\n---\n\n- [P2] x\n")
+        record = self.write(".orchestration/acceptance/t-a01.md", "# record\n")
+        self.assertIn(
+            f"write the owner task {owner} first", self.run_tool("local-advisory.sh", "t-a01", head, owner, code=2)
+        )
+        self.assertEqual("# record\n", record.read_text())
+        owner_file = self.write(f".orchestration/tasks/{owner}.md", "# the owner task\n")
+        self.run_tool("local-advisory.sh", "t-a01", head, owner)
+        sha = hashlib.sha256(owner_file.read_bytes()).hexdigest()
+        [line] = [line for line in record.read_text().splitlines() if line.startswith("local-finding:")]
+        self.assertTrue(line.endswith(f"; evidence=shasum -a 256 .orchestration/tasks/{owner}.md ({sha})"), line)
+
+    def test_local_advisory_classes_a_repeat_by_the_earlier_row(self):
+        # C-50: a finding found again on a later head takes the class the record gave the earlier finding, so the
+        # three-rows rule can count it; the later head's row wins, and a line range is a token.
+        owner, v = "t-followup-a01", ".orchestration/validation"
+        self.write(f".orchestration/tasks/{owner}.md", "owner\n")
+        self.write(
+            f"{v}/t-a01-local-review-aaaaaa1.md",
+            "---\nfindings: 2\n---\n\n- [P2] scripts/x.sh:12 quoting\n- [P2] scripts/y.sh:3-5 range\n",
+        )
+        self.write(f"{v}/t-a01-local-review-bbbbbb2.md", "---\nfindings: 1\n---\n\n- [P3] scripts/x.sh:12 again\n")
+        rows = "local:aaaaaa1:1\tquoting\nlocal:aaaaaa1:2\trange-case\nlocal:bbbbbb2:1\tenv-s-quoting\n"
+        record = self.write(".orchestration/acceptance/t-a01.md", f"# record\n{rows}")
+        head = "cccccc3" + "1" * 33
+        current = "- [P2] `scripts/x.sh:12` once more\n- [P2] scripts/y.sh:3-5 again\n- [P2] scripts/y.sh:3-9 wider\n- [P2] scripts/z.sh:7 new\n"
+        self.write(f"{v}/t-a01-local-review-cccccc3.md", f"---\nfindings: 4\n---\n\n{current}")
+        self.run_tool("local-advisory.sh", "t-a01", head, owner)
+        text = record.read_text()
+        self.assertEqual(
+            [
+                "local:cccccc3:1\tenv-s-quoting",
+                "local:cccccc3:2\trange-case",
+                "local:cccccc3:3\tadvisory-p2",  # y.sh:3-9 is another token than y.sh:3-5
+                "local:cccccc3:4\tadvisory-p2",
+            ],
+            re.findall(r"^local:cccccc3:\d\t.*$", text, re.MULTILINE),
+        )
+        findings = re.findall(r"^local-finding: cccccc3:(\d) .*$", text, re.MULTILINE)
+        self.assertEqual(["1", "2", "3", "4"], findings)
+        lines = [line for line in text.splitlines() if line.startswith("local-finding: cccccc3:")]
+        self.assertIn("(- [P2] scripts/x.sh:12 once more; repeat of local:bbbbbb2:1)", lines[0])
+        self.assertIn("(- [P2] scripts/y.sh:3-5 again; repeat of local:aaaaaa1:2)", lines[1])
+        self.assertNotIn("repeat of", lines[2] + lines[3])
+        # A review without findings needs no owner file and writes no heading.
+        empty = "dddddd4" + "1" * 33
+        self.write(f"{v}/t-b01-local-review-dddddd4.md", "---\nfindings: 0\n---\n")
+        b = self.write(".orchestration/acceptance/t-b01.md", "# record\n")
+        self.run_tool("local-advisory.sh", "t-b01", empty, "t-nobody-a01")
+        self.assertEqual("# record\n", b.read_text())
+
     def test_sandbox_scan_prints_the_unsandboxed_mutation_calls(self):
         sandboxes = ".orchestration/sandboxes"
         hit = "| 2 | dangerouslyDisableSandbox: git commit -m wip |"

 succeeded in 296ms:
---
{
  "format": 1,
  "task": "dotfiles-T128-chain-review-scripts-followup-a03",
  "head": "d3e8acfe553791577576282eb0c339c018721bde",
  "pr": 381,
  "ledger": [],
  "searches": [],
  "audit_findings": []
}
---

# Acceptance record: dotfiles-T128-chain-review-scripts-followup-a03 (the owner task corrections C-51 (2) and C-50 (3) name)

- 2026-10-15T13:06:18Z record created before the first dispatch; the Codex half of the task-text review runs first, the seat after its confirm (C-54); dispatch waits for the a02 owner task dotfiles-T128-chain-review-scripts-followup-a02 (after.
- 2026-10-15T14:41:09Z Codex half round 1 (on 0d82d7c4) stalled: the three reviews started 13:07Z together, each transcript (`.agents/worklog/orchestrator-glue/codex-chain-a03-r1.log`) stopped growing at 13:17Z with no final message, and the processes were still alive at 14:24Z (77 minutes); stopped and re-run one at a time, T7 first.
- 2026-10-15T22:01:24Z Codex half round 1 (`…-codex-r1.md`, on 0d82d7c4, 81 s, run alone after the stalled run of 13:07Z): `confirm`, no finding. The seat's round 1 on the same hash dispatched through `dispatch-direct.sh` (C-54).
- 2026-10-15T22:07:56Z review seat round 1 (bus 22:07:26Z, on 0d82d7c4): `confirm`; the Codex half confirmed the same hash (`…-codex-r1.md`). **Pair-confirmed: task sha256 `0d82d7c45331733c77da412ade59e6ccfab84bee784a57b86c2c3fa7ec0fdaaf`** (one round each, C-54 held). `ACCEPTANCE round=1 status=accepted` sent. Dispatch waits for the a02 owner task's merge (`after:`), itself after boundary (16).
- 2026-10-15T22:08:38Z the seat's five round-1 P3s applied as round 2 rather than carried as worker input, since the task waits for the a02 owner task anyway: task sha256 `5bd7e6018fa045194eeedd33118dbb50c5c83611b55a235eeb890bddedd65190`, brief `8aadd78224c405ad3045a7d3af373b4a97c1194725e5ecb79c48fc2c7cc0c11a`, `presend.sh` OK; Codex round 2 first, the seat's round 2 after its confirm (C-54).
- 2026-10-15T22:11:13Z Codex half round 2 (`…-codex-r2.md`, on 5bd7e601, 104 s): `revise`, two P3: the absent-owner case asserted only a row-less record; the repeat test covered neither a line-range token nor two matching earlier heads. Round 3 adds both (the record compared byte for byte; a `scripts/y.sh:3-5` token; two earlier heads with different classes, the later head's winning): task sha256 `d6b2108bd4d1fba1e35d162f318dc377324c8f937ec826b87b6a44ce9d7e1775`, brief `fff04d67fd291c1de30b868f8b1bd68bcda00386d6aec1b42a38af2807da54cc`, `presend.sh` OK; Codex round 3 next (C-54).
- 2026-10-15T22:12:52Z Codex half round 3 (`…-codex-r3.md`, on d6b2108b, 68 s): `confirm`, no finding. The seat's round 2 on this hash follows its dispatch.sh-task round (one task at a time; C-54).
- 2026-10-15T22:19:49Z review seat round 2 (bus 22:19:07Z, on d6b2108b): `confirm`; the Codex half confirmed the same hash (`…-codex-r3.md`). **Pair-confirmed: task sha256 `d6b2108bd4d1fba1e35d162f318dc377324c8f937ec826b87b6a44ce9d7e1775`** (Codex rounds 1 to 3, seat rounds 1 and 2; supersedes the 0d82d7c4 confirmation). `ACCEPTANCE round=2 status=accepted` sent.
- 2026-10-15T22:20:07Z worker input carried into the dispatch note (the seat's round-2 P3-1 under its confirm): two earlier heads are ordered by their review files' `finished:` line (the line `local-review.sh` writes), the newer `finished:` winning, and the test fixtures write that line; a `<sha7>` carries no order and file times are not evidence.
- 2026-10-15T22:20:22Z correction of the line above, after reading the P3 in full: the key is the record's own row order (`local:` rows are appended as heads are reviewed, so the last matching `local:` row in the record wins), which needs no new fixture line; `finished:` is the alternative the seat named second. The dispatch note carries the record-order key.
- 2026-10-17T00:43:19Z review seat round 3 (bus 00:42:32Z, a005 on e328a3fb): `confirm`; **the owner task is pair-confirmed again at `e328a3fb8036d4b29b1ed798f42a967d66204bde810b62b84dd7048715c79ee2`** (Codex rounds 2 and 3 on the owned row, the premise and the Completion clause); C-58 boundary check: the allowed files are orchestrator scripts and their test module, no runtime boundary, so any seat kind; presend rc 0 (premises 0, 1, 2, 14); the TASK line to `claude-standard-dot-a002` (worker-f, wA:p4; free since T8's round-2 RESULT) by dispatch-direct.
- 2026-10-17T01:15:13Z RESULT `status=done` (bus 01:13:24Z): PR #381 `tools/chain-review-scripts-followup-a03`, head 1e0c2e92 on f7847616 (a311781d code, a1ddb211 the test round, 9da0897a the ShellCheck SC2015 fix); rows 1a (C-51's owner-file refusal and sha256 evidence), 1b (C-50's repeat classing) and `audit:40f3be4:2` (the heading fixture) with three tests; 16 of 16, 6 of 6 mutants, caps 43 / 60, CI 12 checks green, the Bot's no-findings comment after @codex review, no threads; task_copy e328a3fb. ACCEPTANCE `pending-integration` at 2026-10-17T01:15:13Z; the owner task `dotfiles-T128-chain-review-scripts-followup-a04` written (C-51) and registered; the chain runs after PRs #377, #375, #378, #380 and #379.

## Dispatch (bus lines)

- AGMSG-TASK v1 task_id=dotfiles-T128-chain-review-scripts-followup-review-a03 round=1 repo=~/Workspace/dotfiles task_file=.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-review-a03.md task_sha256=04c5c4245809bcaaee0b324fec75c9f1b22e63a0487cdc55a2afcba07e3cf901  it shares the test module):advisory_task_file=.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a03.md  it shares the test module):advisory_task_sha256=0d82d7c45331733c77da412ade59e6ccfab84bee784a57b86c2c3fa7ec0fdaaf deadline=none note=one-round-review-of-the-owner-task-corrections-C-51-(2)-and-C-50-(3)-name(the-Codex-half-confirmed-first,C-54);answer-with-AGMSG-RESULT-verdict=confirm|revise- it shares the test module):advisory_task_sha256=<sha> read_at=read
- AGMSG-TASK v1 task_id=dotfiles-T128-chain-review-scripts-followup-review-a03 round=2 repo=~/Workspace/dotfiles task_file=.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-review-a03.md task_sha256=fff04d67fd291c1de30b868f8b1bd68bcda00386d6aec1b42a38af2807da54cc  it shares the test module):advisory_task_file=.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a03.md  it shares the test module):advisory_task_sha256=d6b2108bd4d1fba1e35d162f318dc377324c8f937ec826b87b6a44ce9d7e1775 deadline=none note=one-round-review-of-the-owner-task-corrections-C-51-(2)-and-C-50-(3)-name(the-Codex-half-confirmed-first,C-54;your-round-1-P3s-applied:the-owner-check-after-the-no-findings-exit-and-before-the-heading,exit-2-for-both-refusals,the-token-grammar-with-backticks-and-ranges,the-local-rows-scope-stated,the-repeat-provenance-clause;the-Codex-round-2-P3s:the-untouched-record-asserted-byte-for-byte,the-range-token-and-two-earlier-heads-cases);answer-with-AGMSG-RESULT-verdict=confirm|revise- it shares the test module):advisory_task_sha256=<sha> read_at=read
- AGMSG-TASK v1 task_id=dotfiles-T128-chain-review-scripts-followup-review-a03 round=3 repo=~/Workspace/dotfiles task_file=.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-review-a03.md task_sha256=fff04d67fd291c1de30b868f8b1bd68bcda00386d6aec1b42a38af2807da54cc owner_task_file=.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a03.md owner_task_sha256=e328a3fb8036d4b29b1ed798f42a967d66204bde810b62b84dd7048715c79ee2 deadline=none note=round-3-a-re-confirm-after-three-changes-since-the-pair-confirmed-d6b2108b:the-Owned-row-section(audit:40f3be4:2,the-heading-test-fixture-from-PR-364-s-audit),the-premise-change(premise-4-records-the-module-s-fourteen-tests-after-PRs-364-and-376;the-Completion-names-the-a02-PR-s-merge-f7847616)and-the-Completion-clause-as-the-task-template-s-form-of-2026-10-16(open-thread-id-with-bot_rounds=2,the-C-50-revise-round,every-other-P2-advisory-owned-by-dotfiles-T128-chain-review-scripts-followup-a04);the-Codex-half-confirmed(round-3);judge-that-the-owned-row-matches-the-audit-finding-it-cites-and-that-nothing-else-changed;answer-with-AGMSG-RESULT-verdict=confirm|revise-owner_task_sha256=<sha> read_at=read
- AGMSG-TASK v1 task_id=dotfiles-T128-chain-review-scripts-followup-a03 round=1 repo=~/Workspace/dotfiles/.claude/worktrees/worker-f task_file=.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a03.md task_sha256=e328a3fb8036d4b29b1ed798f42a967d66204bde810b62b84dd7048715c79ee2 deadline=none note=the-third-owner-task-of-the-chain-review-scripts-lineage(local-advisory.sh:the-owner-file-refusal,hash-evidence,repeat-classing;plus-the-owned-row-audit:40f3be4:2,the-heading-test-fixture-in-tests/unit/test_chain_review_scripts.py;worker-input:the-last-matching-local:-row-in-the-record-wins);pair-confirmed-at-this-hash(Codex-round-3,seat-round-3;the-Completion-clause-is-the-template-s-form-of-2026-10-16);boundary-check:orchestrator-scripts,no-runtime-boundary(C-58);read-the-task-file-first,fresh-branch-from-origin/main(f7847616-or-later;your-earlier-branches-stay-in-the-worktree-until-acceptance),one-PR,the-Bot-reviews-once-at-PR-open,RESULT-per-Worker-Playbook-step-15 read_at=read
- AGMSG-ACCEPTANCE v1 task_id=dotfiles-T128-chain-review-scripts-followup-a03 round=1 status=pending-integration reason=RESULT-read:head-1e0c2e92,rows-1a-1b-and-audit:40f3be4:2-done-with-three-tests,16-tests,6-mutants,CI-green,no-Bot-thread;the-chain-runs-after-PRs-377,375,378,380-and-379(one-chain-at-a-time);you-are-free previous_head=1e0c2e9291ce75ae11156a916cc872f0b6db0e7a next_action=none-for-this-task read_at=read
{
  "repo": "mryfmo/dotfiles",
  "pr": 381,
  "head_sha": "d3e8acfe553791577576282eb0c339c018721bde",
  "base_ref": "main",
  "base_sha": "b167fe0a76a2e77d262f9f556c69ba6b9f118bbe",
  "generated_at": "2026-10-17T03:41:11+00:00",
  "checks": [
    {
      "name": "GitGuardian Security Checks",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/runs/117296704782"
    },
    {
      "name": "public-bootstrap (macos-14, client)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38998621128/job/117296597380"
    },
    {
      "name": "test (ubuntu-24.04, server)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38998621146/job/117296597345"
    },
    {
      "name": "private-bootstrap (ubuntu-24.04, client)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38998621128/job/117296597339"
    },
    {
      "name": "public-bootstrap (ubuntu-24.04, client)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38998621128/job/117296597266"
    },
    {
      "name": "test (macos-14, client)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38998621146/job/117296597250"
    },
    {
      "name": "public-bootstrap (ubuntu-24.04, server)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38998621128/job/117296597242"
    },
    {
      "name": "test (ubuntu-24.04, client)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38998621146/job/117296597222"
    },
    {
      "name": "private-bootstrap (ubuntu-24.04, server)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38998621128/job/117296597194"
    },
    {
      "name": "validate",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38998621149/job/117296597111"
    },
    {
      "name": "test (ubuntu-26.04, client)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38998621146/job/117296597103"
    },
    {
      "name": "private-bootstrap (macos-14, client)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38998621128/job/117296597094"
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
      "body": "<!-- codex-pull-request-review-summary -->\n<!-- codex-review-state:v1 {\"code_review\":{\"commit_sha\":\"d2b33025d05f00b8dca947b54f9bbe0d16f1991b\",\"has_any_findings\":false,\"has_unresolved_findings\":false,\"status\":\"completed\"},\"security_review\":{\"commit_sha\":\"d2b33025d05f00b8dca947b54f9bbe0d16f1991b\",\"has_any_findings\":false,\"has_unresolved_findings\":false,\"status\":\"completed\"}} -->\n<!-- codex-security-review:v1 {\"blockingSeverityThreshold\":\"P0\",\"headSha\":\"d2b33025d05f00b8dca947b54f9bbe0d16f1991b\",\"mergeGateEnabled\":false,\"pullRequestNumber\":381,\"repository\":\"mryfmo/dotfiles\",\"status\":\"completed\"} -->\n## Codex Review Summary\n\nThis comment shows the latest Codex review activity on this pull request.\n\n| Review | Status | Commit | Review trigger |\n| --- | --- | --- | --- |\n| 📝 **Code Review** | ✅ **Completed** <relative-time datetime=\"2026-10-17T00:59:48.920029Z\">2026-10-17T00:59:48.920029Z</relative-time> | `d2b3302` | Manual request |\n| 🔒 **Security Review** | ✅ **Completed** <relative-time datetime=\"2026-10-17T00:50:21.721589Z\">2026-10-17T00:50:21.721589Z</relative-time> | `d2b3302` | Draft marked ready |\n\n\n\n<details> <summary>ℹ️ About Codex in GitHub</summary>\n<br/>\n\n[Your team has set up Codex to review pull requests in this repo](https://chatgpt.com/codex/cloud/settings/general). Reviews are triggered when you\n- Open a pull request for review\n- Mark a draft as ready\n- Comment \"@codex review\" or \"@codex security review\".\n\nCodex reacts with 👀 while any review is running, comments if it has suggestions, and reacts with 👍 once all reviews finish with no findings.\n\n</details>",
      "url": "https://github.com/mryfmo/dotfiles/pull/381#issuecomment-6227560372",
      "disposition": "not-applicable:bot summary or onboarding comment, no finding; evidence=jq --argjson u '\"https://github.com/mryfmo/dotfiles/pull/381#issuecomment-6227560372\"' '.items[] | select(.url == $u)' .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a03-pr-feedback.json"
    },
    {
      "source": "issue_comment",
      "author": "coderabbitai[bot]",
      "bot": true,
      "level": "comment",
      "path": null,
      "line": null,
      "body": "<!-- This is an auto-generated comment: summarize by coderabbit.ai -->\n<!-- This is an auto-generated comment: skip review by coderabbit.ai -->\n\n> [!IMPORTANT]\n> ## Review skipped\n> \n> Auto reviews are disabled on this repository. Please check the settings in the CodeRabbit UI or the `.coderabbit.yaml` file in this repository. To trigger a single review, invoke the `@coderabbitai review` command.\n> \n> <details>\n> <summary><strong>⚙️ Run configuration</strong></summary>\n> <dl>\n> <dd>\n> \n> - **Configuration used**: Repository: mryfmo/dotfiles/.coderabbit.yaml\n> - **Review profile**: CHILL\n> - **Plan**: Advanced\n> - **Run ID**: `4a95c877-21ce-45e8-858c-5860e71f90d1`\n> \n> </dd>\n> </dl>\n> </details>\n> \n> You can disable this status message by setting the `reviews.review_status` to `false` in the CodeRabbit configuration file.\n> \n> Use the checkbox below for a quick retry:\n> - [ ] <!-- {\"checkboxId\":\"e9bb8d72-00e8-4f67-9cb2-caf3b22574fe\"} --> 🔍 Trigger review\n\n<!-- end of auto-generated comment: skip review by coderabbit.ai -->\n\n<!-- autopilot:start -->\n- [ ] <!-- {\"checkboxId\":\"2708ad07-9f24-4260-9c11-7dc76a49f2e3\"} --> <strong title=\"Keep fixing CodeRabbit findings and required CI, and resolving merge conflicts\">Autofix</strong> · Keep fixing CodeRabbit findings and required CI, and resolving merge conflicts\n<!-- autopilot:end -->\n<!-- tips_start -->\n\n\n\nThanks for using [CodeRabbit](https://coderabbit.ai?utm_source=oss&utm_medium=github&utm_campaign=mryfmo/dotfiles&utm_content=381)! It's free for OSS, and your support helps us grow. If you like it, consider giving us a shout-out.\n\n<details>\n<summary><strong>❤️ Share</strong></summary>\n<dl>\n<dd>\n\n- [X](https://twitter.com/intent/tweet?text=I%20just%20used%20%40coderabbitai%20for%20my%20code%20review%2C%20and%20it%27s%20fantastic%21%20It%27s%20free%20for%20OSS%20and%20offers%20a%20free%20trial%20for%20the%20proprietary%20code.%20Check%20it%20out%3A&url=https%3A//coderabbit.ai)\n- [Mastodon](https://mastodon.social/share?text=I%20just%20used%20%40coderabbitai%20for%20my%20code%20review%2C%20and%20it%27s%20fantastic%21%20It%27s%20free%20for%20OSS%20and%20offers%20a%20free%20trial%20for%20the%20proprietary%20code.%20Check%20it%20out%3A%20https%3A%2F%2Fcoderabbit.ai)\n- [Reddit](https://www.reddit.com/submit?title=Great%20tool%20for%20code%20review%20-%20CodeRabbit&text=I%20just%20used%20CodeRabbit%20for%20my%20code%20review%2C%20and%20it%27s%20fantastic%21%20It%27s%20free%20for%20OSS%20and%20offers%20a%20free%20trial%20for%20proprietary%20code.%20Check%20it%20out%3A%20https%3A//coderabbit.ai)\n- [LinkedIn](https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Fcoderabbit.ai&mini=true&title=Great%20tool%20for%20code%20review%20-%20CodeRabbit&summary=I%20just%20used%20CodeRabbit%20for%20my%20code%20review%2C%20and%20it%27s%20fantastic%21%20It%27s%20free%20for%20OSS%20and%20offers%20a%20free%20trial%20for%20proprietary%20code)\n\n</dd>\n</dl>\n</details>\n\n\n<sub>Comment `@coderabbitai help` to get the list of available commands.</sub>\n\n<!-- tips_end -->",
      "url": "https://github.com/mryfmo/dotfiles/pull/381#issuecomment-6227560380",
      "disposition": "not-applicable:bot summary or onboarding comment, no finding; evidence=jq --argjson u '\"https://github.com/mryfmo/dotfiles/pull/381#issuecomment-6227560380\"' '.items[] | select(.url == $u)' .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a03-pr-feedback.json"
    },
    {
      "source": "issue_comment",
      "author": "moriya-fumio-thd",
      "bot": false,
      "level": "comment",
      "path": null,
      "line": null,
      "body": "@codex review",
      "url": "https://github.com/mryfmo/dotfiles/pull/381#issuecomment-6227663819",
      "disposition": "not-applicable:bot summary or onboarding comment, no finding; evidence=jq --argjson u '\"https://github.com/mryfmo/dotfiles/pull/381#issuecomment-6227663819\"' '.items[] | select(.url == $u)' .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a03-pr-feedback.json"
    },
    {
      "source": "issue_comment",
      "author": "chatgpt-codex-connector[bot]",
      "bot": true,
      "level": "comment",
      "path": null,
      "line": null,
      "body": "<!-- codex-review-receipt:v1 -->\n\nCodex Review: Didn't find any major issues. What shall we delve into next?\n\n**Reviewed commit:** `d2b33025d0`\n\n<details> <summary>ℹ️ About Codex in GitHub</summary>\n<br/>\n\nCodex has been enabled to automatically review pull requests in this repo. Reviews are triggered when you\n- Open a pull request for review\n- Mark a draft as ready\n- Comment \"@codex review\".\n\nIf Codex has suggestions, it will comment; otherwise it will react with 👍.\n\n\n\n\nWhen you [sign up for Codex through ChatGPT](https://openai.com/codex), Codex can also answer questions or update the PR, like \"@codex address that feedback\".\n            \n</details>",
      "url": "https://github.com/mryfmo/dotfiles/pull/381#issuecomment-6227679116",
      "disposition": "not-applicable:bot summary or onboarding comment, no finding; evidence=jq --argjson u '\"https://github.com/mryfmo/dotfiles/pull/381#issuecomment-6227679116\"' '.items[] | select(.url == $u)' .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a03-pr-feedback.json"
    },
    {
      "source": "annotation",
      "author": "github-actions",
      "bot": true,
      "level": "notice",
      "path": ".github",
      "line": 1,
      "body": "Due to capacity constraints, jobs targeting macOS arm64 runners may experience longer queue times.",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38998621128/job/117296597380",
      "check": "public-bootstrap (macos-14, client)",
      "disposition": "not-applicable:runner capacity notice, no finding; evidence=jq --argjson u '\"https://github.com/mryfmo/dotfiles/actions/runs/38998621128/job/117296597380\"' '.items[] | select(.url == $u)' .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a03-pr-feedback.json"
    },
    {
      "source": "annotation",
      "author": "github-actions",
      "bot": true,
      "level": "notice",
      "path": ".github",
      "line": 1,
      "body": "Due to capacity constraints, jobs targeting macOS arm64 runners may experience longer queue times.",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38998621146/job/117296597250",
      "check": "test (macos-14, client)",
      "disposition": "not-applicable:runner capacity notice, no finding; evidence=jq --argjson u '\"https://github.com/mryfmo/dotfiles/actions/runs/38998621146/job/117296597250\"' '.items[] | select(.url == $u)' .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a03-pr-feedback.json"
    },
    {
      "source": "annotation",
      "author": "github-actions",
      "bot": true,
      "level": "notice",
      "path": ".github",
      "line": 1,
      "body": "Due to capacity constraints, jobs targeting macOS arm64 runners may experience longer queue times.",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38998621128/job/117296597094",
      "check": "private-bootstrap (macos-14, client)",
      "disposition": "not-applicable:runner capacity notice, no finding; evidence=jq --argjson u '\"https://github.com/mryfmo/dotfiles/actions/runs/38998621128/job/117296597094\"' '.items[] | select(.url == $u)' .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a03-pr-feedback.json"
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
      "disposition": "not-applicable:CI status, no finding; evidence=jq --argjson s '\"status\"' --argjson c '\"CodeRabbit\"' '.items[] | select(.source == $s and .check == $c)' .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a03-pr-feedback.json"
    }
  ]
}

 succeeded in 345ms:
21:- A Claude session started in the repository root outside Herdr (a plain shell, mosh/ssh, or `claude -p`) is a pane-less orchestrator: nothing seats a worker automatically, and the SessionStart `herdr-agents --attach` hook prints a summary line naming that state, the on-demand commands, and any seated worker, followed in a regime repository by the `agmsg-orchestration:` directive line. Bring the regime up on demand: claim the seat outside the sandbox with the composite instance id, `actas-claim.sh <repo> claude-code <name> <session_id>.<claude pid>` (a claim from sandboxed Bash writes the bare session id and turn delivery then skips silently; see the seat-lock bullet below); seat the worker with `herdr-agents --add-worker <worktree>` (it derives `HERDR_SOCKET_PATH` from the default Herdr server socket `~/.config/herdr/herdr.sock`, the path the Claude sandbox allowlists, before creating anything, accepts a claude worker's workspace-trust dialog during spawn's readiness wait, and takes `--ready-timeout <seconds>`); confirm the worker's placement from its `run/spawn.*` placement record itself (the `herdr:<socket>:<pane>` row that upstream `agmsg_spawn_path` resolves) and the `linkage=` line `--add-worker` prints, never from `team.sh <team> --json`, which observes Codex members by reading their pane; treat the `linkage=` line `--add-worker` prints as the `AGMSG-PING` evidence, and on `pong=no` or `linkage=unreached` wake again with `agmsg-dispatch <team> <orchestrator> <worker> <pane> 'AGMSG-PING v1 task_id=<id> reason=<reason>'` and verify the PING's `read_at` (`poke.sh` only for a viewed workspace); and dispatch no AGMSG-TASK before its `AGMSG-PONG` arrives. Without a managed workspace the auditor runs headless, in the form the task-level audit bullet below names. A pane-less session uses turn delivery when the Monitor cannot run; see "Identity, delivery, and storage" for the platform limits.
33:- Delegate all repository-mutating work — file edits, builds, test runs, and git state changes — to seated workers, with at most one seated worker per git worktree and sequential assignments within one worktree. Add worktrees for parallelism; never use parallel `codex exec` or per-task Codex spawning, except that the read-only, non-interactive task-level audit the orchestrator runs during acceptance (the task-level audit bullet below) is not worker spawning and is permitted; it is identity-less. agmsg/herdr control-plane commands (`delivery.sh`, `watch.sh`, `actas-claim.sh`, `send.sh`, `join.sh`, and herdr agent/pane commands) are orchestrator-side exemptions.
43:  - Some steps stay sequential. The single audit tab serializes audits; the task-level audit of T67 reduces them to one per task. The orchestrator-side gate (`make require-crit-review`) and merges also run one at a time.
71:- A task that touches a trust boundary (anything the design tier lists, CI that decides a required check, code that executes PR-controlled input) carries a `threat_table` in its front matter: one `{control, disposition}` row per thing the PR or the orchestrator controls (the tree and its tests, task.md, workflow files, interpreter and environment files, in-process effects, new or renamed scripts, metadata separators). The row unit is one row per `allowed_files` entry, one row per listed control that is not a path (task metadata, workflow and interpreter or environment inputs, in-process effects, new or renamed scripts, metadata separators), carried by the declared test module's row where that is where the control acts, and one row per orchestrator effect from the fixed list (forced removal, merge, update-branch); under a wildcard `allowed_files` entry whose files are executed or applied (scripts, workflows, hooks, settings, the rules seats follow), one row per concrete file the PR changes; a wildcard over test fixtures or other data files keeps one row; C4 and C7b of `scripts/orchestrator/task-consistency-check.py` verify the path half before dispatch, and the task-file review checks the rest. A disposition takes one of three forms: `closed: tests/<file>::<name>`, the test that closes the row; `residual: <sentence>`, the compensating control; `out-of-scope: <task id>`, the task that owns the row. The task-file review checks the three shape rules by hand: a `closed` selector names a test present in the PR tree at acceptance, an `out-of-scope` owner is a task id in the design's `implementing_tasks`, a `residual` payload is a sentence of at least 20 characters (the gate's minimum for a reason). For a `closed` row it checks the selector's form only, since the test does not exist before implementation. Substance is the reviewers': the task-file review, the Bot and the auditor judge each row against the diff. The table is the task's completion condition: a missing row is added once, counted as an amendment, never fixed finding by finding.
72:- Before every acceptance action (revise, accept, merge) the orchestrator runs `scripts/regime-counters.sh <task id>` and pastes its output into the acceptance record. S2 is decided from INV-6's counts: each component the script prints is read from its output, and for each component it prints as `unknown` the record pastes the command and output that read the source INV-6 names for that component, or, while that source has no entry for the task, says so and pastes the reading of the interim record the orchestrator used in its place. S1 (plan 006: the same finding class three times on one artifact, from any reviewer) is decided from the record's finding-class table, which gives a class to every finding the PR-feedback sweep lists, whatever its disposition, and to every task-level audit finding; three rows of one class stop the artifact. Read that table over non-advisory rows only: list advisory P2 rows with their classes (`advisory-p2` and the `local:<sha7>:<n>` rows `local-advisory.sh` writes), exclude them from S1's three-rows count, and name the excluded rows in the record. The gate's S6 check still sees every ledger row, so an advisory class at three rows gets its `searches` entry from `acceptance-front-matter.py` like any other. INV-6's message and head counts and the S2 lines (`revises`, `amendments`, `questions`, `bot_p1_heads`) take no ledger rows; `scripts/regime-counters.sh` prints them unchanged.
157:## Orchestrator Playbook
168:10. For a RESULT that carries a pull request, integrate in this order. This is the single procedure that the PR integration rule, `AGENTS.md`, the README and the gh-first-workflow skill cite. A `gh pr update-branch` moves the head, so steps 1 to 4 run again on the new head. After an update-branch the orchestrator runs it, the order is CI on the new head, then the sweep, then the audit; an audit started before CI finishes sees incomplete evidence and returns an evidence-only `incorrect`. Select a checkout with git -C <absolute path>, never with cd, which the sandboxed Bash may not honour. After moving the review worktree to the audited head, verify git -C <review> rev-parse HEAD equals that head and git -C <main> symbolic-ref --short HEAD prints main before the audit and the gate.
170:       - A P2 finding of the Codex Bot, local review or task-level audit is advisory: disposition it `not-applicable:advisory P2 owned by <lineage>-followup-a0<n>` and record an `<id><TAB><class>` row under `## Owned by <owner>` in the lineage's acceptance record, with the orchestrator writing the owner task file before the row.
173:    2. Run the task-level audit of that head in the pair or headless form of the task-level audit bullet. It exits nonzero for every verdict other than `correct`. An exit with `Audit verdict: incorrect` is not a failed step: continue to step 3 and disposition its findings. A `blocked` or missing verdict means re-running the audit.
174:    3. Write the acceptance record, summarising the dispositions, with every audit finding dispositioned as the task-level audit bullet says: for an `incorrect` verdict the record's JSON `audit_findings`, which the gate reads through `ACCEPTANCE_EVIDENCE`.
198:10. If blocked, still write the report and evidence paths that explain the blocker.
{
  "lastAnalyzedAt": "2026-10-02T14:12:51Z",
  "gitCommitHash": "940a3a2b07adfd14140a0acff96784ef53a0a509",
  "version": "1.0.0",
  "analyzedFiles": 368
}

 exited 1 in 347ms:
error connecting to api.github.com
check your internet connection or https://githubstatus.com

**Managing output truncation**
exec
/bin/zsh -lc 'cat .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a03-pr-feedback.json' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc 'nl -ba .orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a03.md' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc 'nl -ba .orchestration/reports/dotfiles-T128-chain-review-scripts-followup-a03.md && nl -ba .orchestration/sandboxes/dotfiles-T128-chain-review-scripts-followup-a03.md' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 95ms:
     1	---
     2	task_id: dotfiles-T128-chain-review-scripts-followup-a03
     3	seat: claude-standard-dot-a002
     4	branch: tools/chain-review-scripts-followup-a03
     5	base: f7847616
     6	code_commit: a311781d
     7	test_commit: a1ddb211
     8	lint_commit: 9da0897a
     9	pr: 381
    10	task_sha256: e328a3fb8036d4b29b1ed798f42a967d66204bde810b62b84dd7048715c79ee2
    11	---
    12	
    13	# Report: dotfiles-T128-chain-review-scripts-followup-a03
    14	
    15	- Seat: `claude-standard-dot-a002` in `.claude/worktrees/worker-f`, on a fresh branch `tools/chain-review-scripts-followup-a03` from `origin/main` `f7847616` (PR #376). The PR #377 and #378 branches stay in the worktree, committed and pushed, until their acceptance.
    16	- Task file: sha256 `e328a3fb…`, copied byte-identical; the task-consistency check passes on the dispatched file (validation §1). Dispatched 2026-10-17T00:43:08Z. All four premises replay equal (§2). No question and no amendment.
    17	
    18	## What changed in `scripts/orchestrator/local-advisory.sh`
    19	
    20	Validation §2a holds the diff.
    21	
    22	- **(a), C-51:**
    23	  - **Owner check:** after the exit 0 for a review without findings and before the heading, `.orchestration/tasks/<owner>.md` must exist. Otherwise the script prints `write the owner task <owner> first` and exits 2, and the record is untouched. The missing review file keeps its own exit 2 and message, and the `@exitcode 2` line names both.
    24	  - **Evidence:** each `local-finding:` line's tail is `evidence=shasum -a 256 .orchestration/tasks/<owner>.md (<sha256>)`, with the file's hash at the time of writing.
    25	- **(b), C-50:**
    26	  - **Token:** a finding's token is the first match of `[A-Za-z0-9._/-]+:[0-9]+(-[0-9]+)?` in its line. The class excludes the backtick, so a backticked token reads as itself.
    27	  - **Earlier findings:** the earlier files are the task's other `.orchestration/validation/<task>-local-review-*.md`, each numbered as the loop numbers its own (`grep -E '^- \[P[0-3]\]' | sort -u`, P0 and P1 included). Their findings are compared by exact token, through `awk '$1 == t'`.
    28	  - **Class:** the new row takes the class of the last `local:<sha7'>:<n'>` row in the record for a matching finding, skipping rows classed `advisory-p2`. Its `local-finding:` parenthesis gains `; repeat of local:<sha7'>:<n'>`. Otherwise the class is `advisory-p2`, as before.
    29	  - **Scope:** only the local review files and the `local:` rows.
    30	- **The header** describes both. The P0/P1 stop, the heading and the once-only writes are unchanged.
    31	
    32	## Tests
    33	
    34	The module has 16 tests, all OK (validation §3): the fourteen on `origin/main` and two new ones.
    35	
    36	| Row | Test |
    37	|---|---|
    38	| 1a | `test_local_advisory_refuses_an_absent_owner_task_and_hashes_the_file`. With no owner file: exit 2, `write the owner task t-followup-a01 first`, and the record byte-identical to the case's pre-run content. With the owner file: the line ends `; evidence=shasum -a 256 .orchestration/tasks/t-followup-a01.md (<sha256 of that file>)`. |
    39	| 1b | `test_local_advisory_classes_a_repeat_by_the_earlier_row`. **Earlier reviews:** `aaaaaa1` has `scripts/x.sh:12` (row `quoting`) and `scripts/y.sh:3-5` (row `range-case`); `bbbbbb2` has `scripts/x.sh:12` (row `env-s-quoting`, later in the record). **Current review `cccccc3`:** `` `scripts/x.sh:12` `` gets `env-s-quoting`, the later row winning; `scripts/y.sh:3-5` gets `range-case`; `scripts/y.sh:3-9` gets `advisory-p2`, being another token; `scripts/z.sh:7` gets `advisory-p2`. The first two lines name `repeat of local:bbbbbb2:1` and `repeat of local:aaaaaa1:2`. A review without findings and no owner file exits 0 with no heading. |
    40	| owned row `audit:40f3be4:2` | `test_local_advisory_matches_the_owner_heading_literally` gains the heading `## Owned by tXfollowup-a01 (x)` beside the near-misses. A regex match of `t.followup-a01` would take it as the owner's heading and write none; the literal match writes the owner's heading once. |
    41	
    42	The two existing local-advisory tests, `test_local_advisory_records_p2_rows_and_stops_on_p0_p1` and the heading test, each gain the owner file the new check requires. The first one's expected `local-finding:` line takes the new evidence form. Nothing else in them changes.
    43	
    44	**Mutation check** (validation §4): 6 mutants, each a literal replacement applied alone, all 6 caught; then the baseline of 16 tests passes. They are:
    45	- the owner check off;
    46	- the old `git show origin/main` evidence;
    47	- the repeat class off;
    48	- the first matching row winning instead of the last;
    49	- the line-range part of the token removed;
    50	- the heading matched as a regex.
    51	
    52	The first pass, on `a311781d`, had two survivors:
    53	- the range token, untested until the `y.sh:3-9` case was added in `a1ddb211`;
    54	- a backtick strip with no effect, since the token class already excludes the backtick. The strip was removed in `a1ddb211`, so that mutant is gone.
    55	
    56	## Readings, declared
    57	
    58	- **The evidence's `(<sha256>)` tail** is item 1a's form, verbatim. Replayed as shell, the parenthesis is a syntax error, so a replay runs the command before it and compares with the hash in parenthesis.
    59	- **"Latest matching head wins"** is read, per the TASK note, as the last matching `local:` row in the record. Rows are appended in review order, so the record's order is the heads' order.
    60	- **A repeat row** is skipped when its class is `advisory-p2` itself, so an unclassed earlier row never overrides a classed one.
    61	
    62	## Caps
    63	
    64	Validation §5: outside `tests/` and `.orchestration/`, 1 file, 38 added and 5 deleted, so 43 changed lines (cap 200); under `tests/`, 60 added lines (cap 1000).
    65	
    66	## CI and the Bot
    67	
    68	- **The Bot:** PR #381 was marked ready at 00:48:01Z. No review came within 10 minutes, so `@codex review` was posted at 603 s (issue comment `6227663819`). The Bot answered with issue comment `6227679116` at 00:59:47Z, "Didn't find any major issues", Reviewed commit `d2b33025d0`, which was then the head. No thread.
    69	- **CI on `d2b33025`:** `test (ubuntu-24.04, client)` failed at `Run ShellCheck` with SC2015 (info) on `local-advisory.sh:61`, the line `k=$((k + 1)) && t=$(token "$l") && earlier+=… || true`, and three `test` jobs were cancelled with it. The local ShellCheck 0.11.0 reports nothing there. `9da0897a` writes the line as an `if` with no change of behaviour. CI's own command, `git ls-files -z 'setup.sh' 'install/*.sh' 'install/**/*.sh' 'scripts/*.sh' | xargs -0 shellcheck -x`, exits 0 locally. The 16 tests and the 6 mutants were re-run on it (validation §3 and §4). CI on the final head is in the RESULT.
    70	
    71	## Not done, or outside scope
    72	
    73	- `local-review.sh`, `sandbox-scan.sh` and `chain-integrate.sh` are unchanged.
    74	- Understand-Anything hook: did not fire. plan-mode-used: no.
    75	- cost: n/a (the runtime exposes no session figures to the seat).
     1	---
     2	task_id: dotfiles-T128-chain-review-scripts-followup-a03
     3	seat: claude-standard-dot-a002
     4	permission_gated_commands: see the table
     5	---
     6	
     7	# Sandbox record: dotfiles-T128-chain-review-scripts-followup-a03
     8	
     9	- Period: from the AGMSG-TASK (2026-10-17T00:43:08Z) to the RESULT.
    10	- Inside the sandbox ran:
    11	  - the HTTPS `git fetch` and `git push`;
    12	  - the branch, the commits and the evidence;
    13	  - every test, lint and mutation run.
    14	- uv ran with `UV_OFFLINE=1`.
    15	- No local mutation was chained onto a call that ran outside the sandbox.
    16	
    17	Calls outside the sandbox: `gh` through the permission gate (`dangerouslyDisableSandbox`) and `agmsg-dispatch` through `excludedCommands`. These rows are planned in advance, so no evidence update moves the head after the Bot's review:
    18	
    19	| # | Command | Step 4 case |
    20	|--:|---|---|
    21	| 1 | `gh pr create --draft --repo mryfmo/dotfiles --base main --head tools/chain-review-scripts-followup-a03 …` | `gh` |
    22	| 2 | `gh pr ready <pr>` | `gh` |
    23	| 3 | the Bot wait (`bot-wait.sh`, background; `gh pr view`, `gh api` reads, and `gh pr comment … '@codex review'` only at 10 minutes without a review) | `gh` |
    24	| 4 | `gh pr checks <pr> --watch` (background, exit status joined) | `gh` |
    25	| 5 | `gh api` reads of the Bot's review and comments on the head | `gh` |
    26	| 6 | after a P0/P1 fix round only: the push, then `gh pr comment <pr> --body '@codex review'` and the same Bot wait for the re-review (`bot_rounds=2`) | `gh` |
    27	| 7 | `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T128-chain-review-scripts-followup-a03 …` | `agmsg-dispatch` |

 succeeded in 113ms:
     1	---
     2	{
     3	  "format": 1,
     4	  "task": "dotfiles-T128-chain-review-scripts-followup-a03",
     5	  "head": "d3e8acfe553791577576282eb0c339c018721bde",
     6	  "pr": 381,
     7	  "ledger": [],
     8	  "searches": [],
     9	  "audit_findings": []
    10	}
    11	---
    12	
    13	# Acceptance record: dotfiles-T128-chain-review-scripts-followup-a03 (the owner task corrections C-51 (2) and C-50 (3) name)
    14	
    15	- 2026-10-15T13:06:18Z record created before the first dispatch; the Codex half of the task-text review runs first, the seat after its confirm (C-54); dispatch waits for the a02 owner task dotfiles-T128-chain-review-scripts-followup-a02 (after.
    16	- 2026-10-15T14:41:09Z Codex half round 1 (on 0d82d7c4) stalled: the three reviews started 13:07Z together, each transcript (`.agents/worklog/orchestrator-glue/codex-chain-a03-r1.log`) stopped growing at 13:17Z with no final message, and the processes were still alive at 14:24Z (77 minutes); stopped and re-run one at a time, T7 first.
    17	- 2026-10-15T22:01:24Z Codex half round 1 (`…-codex-r1.md`, on 0d82d7c4, 81 s, run alone after the stalled run of 13:07Z): `confirm`, no finding. The seat's round 1 on the same hash dispatched through `dispatch-direct.sh` (C-54).
    18	- 2026-10-15T22:07:56Z review seat round 1 (bus 22:07:26Z, on 0d82d7c4): `confirm`; the Codex half confirmed the same hash (`…-codex-r1.md`). **Pair-confirmed: task sha256 `0d82d7c45331733c77da412ade59e6ccfab84bee784a57b86c2c3fa7ec0fdaaf`** (one round each, C-54 held). `ACCEPTANCE round=1 status=accepted` sent. Dispatch waits for the a02 owner task's merge (`after:`), itself after boundary (16).
    19	- 2026-10-15T22:08:38Z the seat's five round-1 P3s applied as round 2 rather than carried as worker input, since the task waits for the a02 owner task anyway: task sha256 `5bd7e6018fa045194eeedd33118dbb50c5c83611b55a235eeb890bddedd65190`, brief `8aadd78224c405ad3045a7d3af373b4a97c1194725e5ecb79c48fc2c7cc0c11a`, `presend.sh` OK; Codex round 2 first, the seat's round 2 after its confirm (C-54).
    20	- 2026-10-15T22:11:13Z Codex half round 2 (`…-codex-r2.md`, on 5bd7e601, 104 s): `revise`, two P3: the absent-owner case asserted only a row-less record; the repeat test covered neither a line-range token nor two matching earlier heads. Round 3 adds both (the record compared byte for byte; a `scripts/y.sh:3-5` token; two earlier heads with different classes, the later head's winning): task sha256 `d6b2108bd4d1fba1e35d162f318dc377324c8f937ec826b87b6a44ce9d7e1775`, brief `fff04d67fd291c1de30b868f8b1bd68bcda00386d6aec1b42a38af2807da54cc`, `presend.sh` OK; Codex round 3 next (C-54).
    21	- 2026-10-15T22:12:52Z Codex half round 3 (`…-codex-r3.md`, on d6b2108b, 68 s): `confirm`, no finding. The seat's round 2 on this hash follows its dispatch.sh-task round (one task at a time; C-54).
    22	- 2026-10-15T22:19:49Z review seat round 2 (bus 22:19:07Z, on d6b2108b): `confirm`; the Codex half confirmed the same hash (`…-codex-r3.md`). **Pair-confirmed: task sha256 `d6b2108bd4d1fba1e35d162f318dc377324c8f937ec826b87b6a44ce9d7e1775`** (Codex rounds 1 to 3, seat rounds 1 and 2; supersedes the 0d82d7c4 confirmation). `ACCEPTANCE round=2 status=accepted` sent.
    23	- 2026-10-15T22:20:07Z worker input carried into the dispatch note (the seat's round-2 P3-1 under its confirm): two earlier heads are ordered by their review files' `finished:` line (the line `local-review.sh` writes), the newer `finished:` winning, and the test fixtures write that line; a `<sha7>` carries no order and file times are not evidence.
    24	- 2026-10-15T22:20:22Z correction of the line above, after reading the P3 in full: the key is the record's own row order (`local:` rows are appended as heads are reviewed, so the last matching `local:` row in the record wins), which needs no new fixture line; `finished:` is the alternative the seat named second. The dispatch note carries the record-order key.
    25	- 2026-10-17T00:43:19Z review seat round 3 (bus 00:42:32Z, a005 on e328a3fb): `confirm`; **the owner task is pair-confirmed again at `e328a3fb8036d4b29b1ed798f42a967d66204bde810b62b84dd7048715c79ee2`** (Codex rounds 2 and 3 on the owned row, the premise and the Completion clause); C-58 boundary check: the allowed files are orchestrator scripts and their test module, no runtime boundary, so any seat kind; presend rc 0 (premises 0, 1, 2, 14); the TASK line to `claude-standard-dot-a002` (worker-f, wA:p4; free since T8's round-2 RESULT) by dispatch-direct.
    26	- 2026-10-17T01:15:13Z RESULT `status=done` (bus 01:13:24Z): PR #381 `tools/chain-review-scripts-followup-a03`, head 1e0c2e92 on f7847616 (a311781d code, a1ddb211 the test round, 9da0897a the ShellCheck SC2015 fix); rows 1a (C-51's owner-file refusal and sha256 evidence), 1b (C-50's repeat classing) and `audit:40f3be4:2` (the heading fixture) with three tests; 16 of 16, 6 of 6 mutants, caps 43 / 60, CI 12 checks green, the Bot's no-findings comment after @codex review, no threads; task_copy e328a3fb. ACCEPTANCE `pending-integration` at 2026-10-17T01:15:13Z; the owner task `dotfiles-T128-chain-review-scripts-followup-a04` written (C-51) and registered; the chain runs after PRs #377, #375, #378, #380 and #379.
    27	
    28	## Dispatch (bus lines)
    29	
    30	- AGMSG-TASK v1 task_id=dotfiles-T128-chain-review-scripts-followup-review-a03 round=1 repo=~/Workspace/dotfiles task_file=.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-review-a03.md task_sha256=04c5c4245809bcaaee0b324fec75c9f1b22e63a0487cdc55a2afcba07e3cf901  it shares the test module):advisory_task_file=.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a03.md  it shares the test module):advisory_task_sha256=0d82d7c45331733c77da412ade59e6ccfab84bee784a57b86c2c3fa7ec0fdaaf deadline=none note=one-round-review-of-the-owner-task-corrections-C-51-(2)-and-C-50-(3)-name(the-Codex-half-confirmed-first,C-54);answer-with-AGMSG-RESULT-verdict=confirm|revise- it shares the test module):advisory_task_sha256=<sha> read_at=read
    31	- AGMSG-TASK v1 task_id=dotfiles-T128-chain-review-scripts-followup-review-a03 round=2 repo=~/Workspace/dotfiles task_file=.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-review-a03.md task_sha256=fff04d67fd291c1de30b868f8b1bd68bcda00386d6aec1b42a38af2807da54cc  it shares the test module):advisory_task_file=.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a03.md  it shares the test module):advisory_task_sha256=d6b2108bd4d1fba1e35d162f318dc377324c8f937ec826b87b6a44ce9d7e1775 deadline=none note=one-round-review-of-the-owner-task-corrections-C-51-(2)-and-C-50-(3)-name(the-Codex-half-confirmed-first,C-54;your-round-1-P3s-applied:the-owner-check-after-the-no-findings-exit-and-before-the-heading,exit-2-for-both-refusals,the-token-grammar-with-backticks-and-ranges,the-local-rows-scope-stated,the-repeat-provenance-clause;the-Codex-round-2-P3s:the-untouched-record-asserted-byte-for-byte,the-range-token-and-two-earlier-heads-cases);answer-with-AGMSG-RESULT-verdict=confirm|revise- it shares the test module):advisory_task_sha256=<sha> read_at=read
    32	- AGMSG-TASK v1 task_id=dotfiles-T128-chain-review-scripts-followup-review-a03 round=3 repo=~/Workspace/dotfiles task_file=.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-review-a03.md task_sha256=fff04d67fd291c1de30b868f8b1bd68bcda00386d6aec1b42a38af2807da54cc owner_task_file=.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a03.md owner_task_sha256=e328a3fb8036d4b29b1ed798f42a967d66204bde810b62b84dd7048715c79ee2 deadline=none note=round-3-a-re-confirm-after-three-changes-since-the-pair-confirmed-d6b2108b:the-Owned-row-section(audit:40f3be4:2,the-heading-test-fixture-from-PR-364-s-audit),the-premise-change(premise-4-records-the-module-s-fourteen-tests-after-PRs-364-and-376;the-Completion-names-the-a02-PR-s-merge-f7847616)and-the-Completion-clause-as-the-task-template-s-form-of-2026-10-16(open-thread-id-with-bot_rounds=2,the-C-50-revise-round,every-other-P2-advisory-owned-by-dotfiles-T128-chain-review-scripts-followup-a04);the-Codex-half-confirmed(round-3);judge-that-the-owned-row-matches-the-audit-finding-it-cites-and-that-nothing-else-changed;answer-with-AGMSG-RESULT-verdict=confirm|revise-owner_task_sha256=<sha> read_at=read
    33	- AGMSG-TASK v1 task_id=dotfiles-T128-chain-review-scripts-followup-a03 round=1 repo=~/Workspace/dotfiles/.claude/worktrees/worker-f task_file=.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a03.md task_sha256=e328a3fb8036d4b29b1ed798f42a967d66204bde810b62b84dd7048715c79ee2 deadline=none note=the-third-owner-task-of-the-chain-review-scripts-lineage(local-advisory.sh:the-owner-file-refusal,hash-evidence,repeat-classing;plus-the-owned-row-audit:40f3be4:2,the-heading-test-fixture-in-tests/unit/test_chain_review_scripts.py;worker-input:the-last-matching-local:-row-in-the-record-wins);pair-confirmed-at-this-hash(Codex-round-3,seat-round-3;the-Completion-clause-is-the-template-s-form-of-2026-10-16);boundary-check:orchestrator-scripts,no-runtime-boundary(C-58);read-the-task-file-first,fresh-branch-from-origin/main(f7847616-or-later;your-earlier-branches-stay-in-the-worktree-until-acceptance),one-PR,the-Bot-reviews-once-at-PR-open,RESULT-per-Worker-Playbook-step-15 read_at=read
    34	- AGMSG-ACCEPTANCE v1 task_id=dotfiles-T128-chain-review-scripts-followup-a03 round=1 status=pending-integration reason=RESULT-read:head-1e0c2e92,rows-1a-1b-and-audit:40f3be4:2-done-with-three-tests,16-tests,6-mutants,CI-green,no-Bot-thread;the-chain-runs-after-PRs-377,375,378,380-and-379(one-chain-at-a-time);you-are-free previous_head=1e0c2e9291ce75ae11156a916cc872f0b6db0e7a next_action=none-for-this-task read_at=read

 succeeded in 123ms:
{
  "repo": "mryfmo/dotfiles",
  "pr": 381,
  "head_sha": "d3e8acfe553791577576282eb0c339c018721bde",
  "base_ref": "main",
  "base_sha": "b167fe0a76a2e77d262f9f556c69ba6b9f118bbe",
  "generated_at": "2026-10-17T03:41:11+00:00",
  "checks": [
    {
      "name": "GitGuardian Security Checks",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/runs/117296704782"
    },
    {
      "name": "public-bootstrap (macos-14, client)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38998621128/job/117296597380"
    },
    {
      "name": "test (ubuntu-24.04, server)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38998621146/job/117296597345"
    },
    {
      "name": "private-bootstrap (ubuntu-24.04, client)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38998621128/job/117296597339"
    },
    {
      "name": "public-bootstrap (ubuntu-24.04, client)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38998621128/job/117296597266"
    },
    {
      "name": "test (macos-14, client)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38998621146/job/117296597250"
    },
    {
      "name": "public-bootstrap (ubuntu-24.04, server)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38998621128/job/117296597242"
    },
    {
      "name": "test (ubuntu-24.04, client)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38998621146/job/117296597222"
    },
    {
      "name": "private-bootstrap (ubuntu-24.04, server)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38998621128/job/117296597194"
    },
    {
      "name": "validate",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38998621149/job/117296597111"
    },
    {
      "name": "test (ubuntu-26.04, client)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38998621146/job/117296597103"
    },
    {
      "name": "private-bootstrap (macos-14, client)",
      "conclusion": "success",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38998621128/job/117296597094"
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
      "body": "<!-- codex-pull-request-review-summary -->\n<!-- codex-review-state:v1 {\"code_review\":{\"commit_sha\":\"d2b33025d05f00b8dca947b54f9bbe0d16f1991b\",\"has_any_findings\":false,\"has_unresolved_findings\":false,\"status\":\"completed\"},\"security_review\":{\"commit_sha\":\"d2b33025d05f00b8dca947b54f9bbe0d16f1991b\",\"has_any_findings\":false,\"has_unresolved_findings\":false,\"status\":\"completed\"}} -->\n<!-- codex-security-review:v1 {\"blockingSeverityThreshold\":\"P0\",\"headSha\":\"d2b33025d05f00b8dca947b54f9bbe0d16f1991b\",\"mergeGateEnabled\":false,\"pullRequestNumber\":381,\"repository\":\"mryfmo/dotfiles\",\"status\":\"completed\"} -->\n## Codex Review Summary\n\nThis comment shows the latest Codex review activity on this pull request.\n\n| Review | Status | Commit | Review trigger |\n| --- | --- | --- | --- |\n| 📝 **Code Review** | ✅ **Completed** <relative-time datetime=\"2026-10-17T00:59:48.920029Z\">2026-10-17T00:59:48.920029Z</relative-time> | `d2b3302` | Manual request |\n| 🔒 **Security Review** | ✅ **Completed** <relative-time datetime=\"2026-10-17T00:50:21.721589Z\">2026-10-17T00:50:21.721589Z</relative-time> | `d2b3302` | Draft marked ready |\n\n\n\n<details> <summary>ℹ️ About Codex in GitHub</summary>\n<br/>\n\n[Your team has set up Codex to review pull requests in this repo](https://chatgpt.com/codex/cloud/settings/general). Reviews are triggered when you\n- Open a pull request for review\n- Mark a draft as ready\n- Comment \"@codex review\" or \"@codex security review\".\n\nCodex reacts with 👀 while any review is running, comments if it has suggestions, and reacts with 👍 once all reviews finish with no findings.\n\n</details>",
      "url": "https://github.com/mryfmo/dotfiles/pull/381#issuecomment-6227560372",
      "disposition": "not-applicable:bot summary or onboarding comment, no finding; evidence=jq --argjson u '\"https://github.com/mryfmo/dotfiles/pull/381#issuecomment-6227560372\"' '.items[] | select(.url == $u)' .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a03-pr-feedback.json"
    },
    {
      "source": "issue_comment",
      "author": "coderabbitai[bot]",
      "bot": true,
      "level": "comment",
      "path": null,
      "line": null,
      "body": "<!-- This is an auto-generated comment: summarize by coderabbit.ai -->\n<!-- This is an auto-generated comment: skip review by coderabbit.ai -->\n\n> [!IMPORTANT]\n> ## Review skipped\n> \n> Auto reviews are disabled on this repository. Please check the settings in the CodeRabbit UI or the `.coderabbit.yaml` file in this repository. To trigger a single review, invoke the `@coderabbitai review` command.\n> \n> <details>\n> <summary><strong>⚙️ Run configuration</strong></summary>\n> <dl>\n> <dd>\n> \n> - **Configuration used**: Repository: mryfmo/dotfiles/.coderabbit.yaml\n> - **Review profile**: CHILL\n> - **Plan**: Advanced\n> - **Run ID**: `4a95c877-21ce-45e8-858c-5860e71f90d1`\n> \n> </dd>\n> </dl>\n> </details>\n> \n> You can disable this status message by setting the `reviews.review_status` to `false` in the CodeRabbit configuration file.\n> \n> Use the checkbox below for a quick retry:\n> - [ ] <!-- {\"checkboxId\":\"e9bb8d72-00e8-4f67-9cb2-caf3b22574fe\"} --> 🔍 Trigger review\n\n<!-- end of auto-generated comment: skip review by coderabbit.ai -->\n\n<!-- autopilot:start -->\n- [ ] <!-- {\"checkboxId\":\"2708ad07-9f24-4260-9c11-7dc76a49f2e3\"} --> <strong title=\"Keep fixing CodeRabbit findings and required CI, and resolving merge conflicts\">Autofix</strong> · Keep fixing CodeRabbit findings and required CI, and resolving merge conflicts\n<!-- autopilot:end -->\n<!-- tips_start -->\n\n\n\nThanks for using [CodeRabbit](https://coderabbit.ai?utm_source=oss&utm_medium=github&utm_campaign=mryfmo/dotfiles&utm_content=381)! It's free for OSS, and your support helps us grow. If you like it, consider giving us a shout-out.\n\n<details>\n<summary><strong>❤️ Share</strong></summary>\n<dl>\n<dd>\n\n- [X](https://twitter.com/intent/tweet?text=I%20just%20used%20%40coderabbitai%20for%20my%20code%20review%2C%20and%20it%27s%20fantastic%21%20It%27s%20free%20for%20OSS%20and%20offers%20a%20free%20trial%20for%20the%20proprietary%20code.%20Check%20it%20out%3A&url=https%3A//coderabbit.ai)\n- [Mastodon](https://mastodon.social/share?text=I%20just%20used%20%40coderabbitai%20for%20my%20code%20review%2C%20and%20it%27s%20fantastic%21%20It%27s%20free%20for%20OSS%20and%20offers%20a%20free%20trial%20for%20the%20proprietary%20code.%20Check%20it%20out%3A%20https%3A%2F%2Fcoderabbit.ai)\n- [Reddit](https://www.reddit.com/submit?title=Great%20tool%20for%20code%20review%20-%20CodeRabbit&text=I%20just%20used%20CodeRabbit%20for%20my%20code%20review%2C%20and%20it%27s%20fantastic%21%20It%27s%20free%20for%20OSS%20and%20offers%20a%20free%20trial%20for%20proprietary%20code.%20Check%20it%20out%3A%20https%3A//coderabbit.ai)\n- [LinkedIn](https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Fcoderabbit.ai&mini=true&title=Great%20tool%20for%20code%20review%20-%20CodeRabbit&summary=I%20just%20used%20CodeRabbit%20for%20my%20code%20review%2C%20and%20it%27s%20fantastic%21%20It%27s%20free%20for%20OSS%20and%20offers%20a%20free%20trial%20for%20proprietary%20code)\n\n</dd>\n</dl>\n</details>\n\n\n<sub>Comment `@coderabbitai help` to get the list of available commands.</sub>\n\n<!-- tips_end -->",
      "url": "https://github.com/mryfmo/dotfiles/pull/381#issuecomment-6227560380",
      "disposition": "not-applicable:bot summary or onboarding comment, no finding; evidence=jq --argjson u '\"https://github.com/mryfmo/dotfiles/pull/381#issuecomment-6227560380\"' '.items[] | select(.url == $u)' .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a03-pr-feedback.json"
    },
    {
      "source": "issue_comment",
      "author": "moriya-fumio-thd",
      "bot": false,
      "level": "comment",
      "path": null,
      "line": null,
      "body": "@codex review",
      "url": "https://github.com/mryfmo/dotfiles/pull/381#issuecomment-6227663819",
      "disposition": "not-applicable:bot summary or onboarding comment, no finding; evidence=jq --argjson u '\"https://github.com/mryfmo/dotfiles/pull/381#issuecomment-6227663819\"' '.items[] | select(.url == $u)' .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a03-pr-feedback.json"
    },
    {
      "source": "issue_comment",
      "author": "chatgpt-codex-connector[bot]",
      "bot": true,
      "level": "comment",
      "path": null,
      "line": null,
      "body": "<!-- codex-review-receipt:v1 -->\n\nCodex Review: Didn't find any major issues. What shall we delve into next?\n\n**Reviewed commit:** `d2b33025d0`\n\n<details> <summary>ℹ️ About Codex in GitHub</summary>\n<br/>\n\nCodex has been enabled to automatically review pull requests in this repo. Reviews are triggered when you\n- Open a pull request for review\n- Mark a draft as ready\n- Comment \"@codex review\".\n\nIf Codex has suggestions, it will comment; otherwise it will react with 👍.\n\n\n\n\nWhen you [sign up for Codex through ChatGPT](https://openai.com/codex), Codex can also answer questions or update the PR, like \"@codex address that feedback\".\n            \n</details>",
      "url": "https://github.com/mryfmo/dotfiles/pull/381#issuecomment-6227679116",
      "disposition": "not-applicable:bot summary or onboarding comment, no finding; evidence=jq --argjson u '\"https://github.com/mryfmo/dotfiles/pull/381#issuecomment-6227679116\"' '.items[] | select(.url == $u)' .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a03-pr-feedback.json"
    },
    {
      "source": "annotation",
      "author": "github-actions",
      "bot": true,
      "level": "notice",
      "path": ".github",
      "line": 1,
      "body": "Due to capacity constraints, jobs targeting macOS arm64 runners may experience longer queue times.",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38998621128/job/117296597380",
      "check": "public-bootstrap (macos-14, client)",
      "disposition": "not-applicable:runner capacity notice, no finding; evidence=jq --argjson u '\"https://github.com/mryfmo/dotfiles/actions/runs/38998621128/job/117296597380\"' '.items[] | select(.url == $u)' .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a03-pr-feedback.json"
    },
    {
      "source": "annotation",
      "author": "github-actions",
      "bot": true,
      "level": "notice",
      "path": ".github",
      "line": 1,
      "body": "Due to capacity constraints, jobs targeting macOS arm64 runners may experience longer queue times.",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38998621146/job/117296597250",
      "check": "test (macos-14, client)",
      "disposition": "not-applicable:runner capacity notice, no finding; evidence=jq --argjson u '\"https://github.com/mryfmo/dotfiles/actions/runs/38998621146/job/117296597250\"' '.items[] | select(.url == $u)' .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a03-pr-feedback.json"
    },
    {
      "source": "annotation",
      "author": "github-actions",
      "bot": true,
      "level": "notice",
      "path": ".github",
      "line": 1,
      "body": "Due to capacity constraints, jobs targeting macOS arm64 runners may experience longer queue times.",
      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38998621128/job/117296597094",
      "check": "private-bootstrap (macos-14, client)",
      "disposition": "not-applicable:runner capacity notice, no finding; evidence=jq --argjson u '\"https://github.com/mryfmo/dotfiles/actions/runs/38998621128/job/117296597094\"' '.items[] | select(.url == $u)' .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a03-pr-feedback.json"
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
      "disposition": "not-applicable:CI status, no finding; evidence=jq --argjson s '\"status\"' --argjson c '\"CodeRabbit\"' '.items[] | select(.source == $s and .check == $c)' .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a03-pr-feedback.json"
    }
  ]
}

**Analyzing code injection risks**
exec
/bin/zsh -lc 'nl -ba .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a03.md' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc "git show d3e8acfe553791577576282eb0c339c018721bde:scripts/orchestrator/local-advisory.sh | nl -ba && git show d3e8acfe553791577576282eb0c339c018721bde:tests/unit/test_chain_review_scripts.py | sed -n '1,135p'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc "sed -n '157,183p' ~/.agents/skills/agmsg-orchestration/SKILL.md && rg -n '"'^##|INV-|invariant|C-50|C-51|C-58|a03'"' .orchestration/tasks/dotfiles-T128-regime-v3-a01.md" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc "python3 -B - <<'PY'
import json,subprocess
from pathlib import Path
p=Path('.ua/knowledge-graph.json')
x=json.loads(p.read_text())
for n in x.get('nodes',[]):
 if any(v in str(n.get('filePath','')) for v in ['chain','orchestrat','regime','AGENTS']):
  print(n.get('filePath'), str(n.get('summary',''))[:300])
print('FRESHNESS')
r=subprocess.check_output(['git','diff','--name-only','940a3a2b07adfd14140a0acff96784ef53a0a509..HEAD'],text=True).splitlines()
print('non-metadata changed files:',sum(not f.startswith(('.ua/','.orchestration/')) for f in r))
PY" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 103ms:
     1	---
     2	task_id: dotfiles-T128-chain-review-scripts-followup-a03
     3	seat: claude-standard-dot-a002
     4	code_commit: 9da0897a
     5	---
     6	
     7	# Validation: dotfiles-T128-chain-review-scripts-followup-a03
     8	
     9	Every command ran from the worktree `.claude/worktrees/worker-f`, inside the sandbox; `MAIN` names the main checkout and `T` the task id. `UV_OFFLINE=1` was set for every uv call. The output is verbatim, with the main checkout's path replaced by `$MAIN`, and each block ends with the exit status of the command shown (a pipeline's is its last command's). Premise 1's `grep -c` prints `0` and exits 1 when it finds nothing, which is the premise's expected output. §4's block shows the mutant script and its output, and each mutant line carries its own `rc`. Captured at `9da0897a` (the code `a311781d`, the test round `a1ddb211`, the CI ShellCheck fix `9da0897a`).
    10	
    11	## 1. Task file and task copy
    12	```console
    13	$ shasum -a 256 "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md"; cmp "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md" && echo byte-identical
    14	e328a3fb8036d4b29b1ed798f42a967d66204bde810b62b84dd7048715c79ee2  $MAIN/.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a03.md
    15	e328a3fb8036d4b29b1ed798f42a967d66204bde810b62b84dd7048715c79ee2  .orchestration/dotfiles-T128-chain-review-scripts-followup-a03/task.md
    16	byte-identical
    17	[exit 0]
    18	```
    19	```console
    20	$ uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root "$PWD" "$MAIN/.orchestration/tasks/$T.md"
    21	dotfiles-T128-chain-review-scripts-followup-a03.md: OK
    22	[exit 0]
    23	```
    24	## 2. Branch and the four premises
    25	```console
    26	$ git log --oneline origin/main..HEAD; git rev-parse origin/main
    27	9da0897a fix(orchestrator): local-advisory.sh numbers each earlier finding with an if, not A && B || C (CI ShellCheck SC2015)
    28	d2b33025 docs(orchestration): chain-review-scripts followup a03 task copy and evidence (a311781d, a1ddb211)
    29	a1ddb211 test(orchestrator): the repeat test tells a line range from a wider one; the token reads a backticked path as itself (T128 chain-review-scripts followup a03)
    30	a311781d fix(orchestrator): local-advisory.sh refuses an absent owner task, hashes the owner file as evidence, and classes a repeated finding by the earlier row (T128 chain-review-scripts followup a03)
    31	f7847616970d6bd83739a75a65ad8f7c35e91462
    32	[exit 0]
    33	```
    34	```console
    35	$ git show origin/main:scripts/orchestrator/local-advisory.sh | /usr/bin/grep -c "write the owner task"
    36	0
    37	[exit 1]
    38	```
    39	```console
    40	$ git show origin/main:scripts/orchestrator/local-advisory.sh | /usr/bin/grep -c "git show origin/main"
    41	1
    42	[exit 0]
    43	```
    44	```console
    45	$ git show origin/main:scripts/orchestrator/local-advisory.sh | /usr/bin/grep -c "advisory-p2"
    46	2
    47	[exit 0]
    48	```
    49	```console
    50	$ git show origin/main:tests/unit/test_chain_review_scripts.py | /usr/bin/grep -c "def test_"
    51	14
    52	[exit 0]
    53	```
    54	## 2a. The diff outside tests and the evidence
    55	```console
    56	$ git diff origin/main...HEAD -- scripts/
    57	diff --git a/scripts/orchestrator/local-advisory.sh b/scripts/orchestrator/local-advisory.sh
    58	index 409035cc..5e67ace7 100755
    59	--- a/scripts/orchestrator/local-advisory.sh
    60	+++ b/scripts/orchestrator/local-advisory.sh
    61	@@ -4,14 +4,19 @@
    62	 # @description
    63	 #   Plan 020 step 1.2 for the local review. Reads `.orchestration/validation/<task>-local-review-<sha7>.md`. Each
    64	 #   unique finding, numbered from 1: a P0/P1 prints STOP (the PR's one round is over: the plan's step 4.2); any
    65	-#   other appends the row `local:<sha7>:<n><TAB>advisory-p2` under the heading `## Owned by <owner>` of
    66	+#   other appends the row `local:<sha7>:<n><TAB><class>` under the heading `## Owned by <owner>` of
    67	 #   `.orchestration/acceptance/<task>.md` (created when missing) and a `local-finding: <sha7>:<n>
    68	-#   not-applicable:advisory P2 owned by <owner> (…); evidence=…` line, each only when the record lacks it.
    69	+#   not-applicable:advisory P2 owned by <owner> (…); evidence=shasum -a 256 .orchestration/tasks/<owner>.md
    70	+#   (<sha256>)` line, each only when the record lacks it. A review with findings needs the owner task file. The
    71	+#   class is `advisory-p2`, unless the finding's `path:line[-line]` token (backticks ignored) matches a finding of
    72	+#   the task's earlier local review files whose `local:` row in the record has another class: then the last such
    73	+#   row's class, and the line's parenthesis names it as `repeat of local:<sha7>:<n>` (C-50).
    74	 # @arg $1 string Task id, letters, digits, `.`, `_` and `-`.
    75	 # @arg $2 string The reviewed head, 40 hex characters.
    76	 # @arg $3 string The task id that owns the advisory findings, in the task id's form.
    77	 # @exitcode 0 No P0/P1 finding.
    78	-# @exitcode 2 No local review file, or a malformed task id, head or owner task id.
    79	+# @exitcode 2 No local review file, a malformed task id, head or owner task id, or (for a review with findings) no
    80	+#   owner task file: `write the owner task <owner> first`.
    81	 # @exitcode 3 A P0/P1 finding.
    82	 # @example
    83	 #   scripts/orchestrator/local-advisory.sh dotfiles-T128-x-a01 "$head" dotfiles-T128-x-followup-a01
    84	@@ -37,6 +42,26 @@ n=$(sed -n 's/^findings: //p' "$LR" | head -1)
    85	     echo "local review of $h7: no findings"
    86	     exit 0
    87	 }
    88	+# The rows name the owner task, so it must exist; its hash is evidence that replays before the boundary (C-51).
    89	+O=".orchestration/tasks/$owner.md"
    90	+[ -f "$O" ] || {
    91	+    echo "write the owner task $owner first"
    92	+    exit 2
    93	+}
    94	+sha=$(shasum -a 256 "$O" | cut -d' ' -f1)
    95	+# C-50: a finding repeated from an earlier head takes the class the record gave it. Each earlier review's findings,
    96	+# numbered as the loop below numbers them, as `<path:line[-line]> local:<sha7>:<n>` lines.
    97	+# The class excludes the backtick, so `a.sh:1` in backticks reads as a.sh:1.
    98	+token() { [[ $1 =~ ([A-Za-z0-9._/-]+:[0-9]+(-[0-9]+)?) ]] && printf '%s\n' "${BASH_REMATCH[1]}"; }
    99	+earlier=""
   100	+for f in .orchestration/validation/"$task"-local-review-*.md; do
   101	+    [[ -f $f && $f != "$LR" ]] || continue
   102	+    e=${f%.md} && e=${e##*-local-review-} && k=0
   103	+    while IFS= read -r l; do
   104	+        k=$((k + 1))
   105	+        if t=$(token "$l"); then earlier+="$t local:$e:$k"$'\n'; fi
   106	+    done < <(/usr/bin/grep -E '^- \[P[0-3]\]' "$f" | sort -u)
   107	+done
   108	 # A literal heading match, ended by a space or the line's end: a . in the owner is no wildcard, a longer id no match.
   109	 awk -v h="## Owned by $owner" 'substr($0, 1, length(h)) == h && substr($0, length(h) + 1, 1) ~ /^ ?$/ { f = 1 } END { exit !f }' "$A" 2> /dev/null || printf '\n## Owned by %s (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)\n\n' "$owner" >> "$A"
   110	 i=0 stop=0
   111	@@ -48,8 +73,16 @@ while IFS= read -r line; do
   112	         stop=1
   113	         ;;
   114	     *)
   115	-        /usr/bin/grep -q "^local:$h7:$i	" "$A" || printf 'local:%s:%s\tadvisory-p2\n' "$h7" "$i" >> "$A"
   116	-        /usr/bin/grep -q "^local-finding: $h7:$i " "$A" || printf 'local-finding: %s:%s not-applicable:advisory P2 owned by %s (%s); evidence=git show origin/main:.orchestration/tasks/%s.md | grep -n '"'"'item 1'"'"'\n' "$h7" "$i" "$owner" "$(printf '%s' "$line" | cut -c1-120 | tr -d '`')" "$owner" >> "$A"
   117	+        # The last row in the record of an earlier finding with this token, other than advisory-p2, wins.
   118	+        class=advisory-p2 repeat=""
   119	+        t=$(token "$line") || t=""
   120	+        ids=$(printf '%s' "$earlier" | awk -v t="$t" '$1 == t { print $2 }' | tr '\n' '|')
   121	+        if [[ -n $t && -n $ids ]]; then
   122	+            row=$(/usr/bin/grep -E "^(${ids%|})	" "$A" | /usr/bin/grep -v '	advisory-p2$' | tail -1 || true)
   123	+            [ -z "$row" ] || class=${row#*	} repeat="; repeat of ${row%%	*}"
   124	+        fi
   125	+        /usr/bin/grep -q "^local:$h7:$i	" "$A" || printf 'local:%s:%s\t%s\n' "$h7" "$i" "$class" >> "$A"
   126	+        /usr/bin/grep -q "^local-finding: $h7:$i " "$A" || printf 'local-finding: %s:%s not-applicable:advisory P2 owned by %s (%s%s); evidence=shasum -a 256 %s (%s)\n' "$h7" "$i" "$owner" "$(printf '%s' "$line" | cut -c1-120 | tr -d '`')" "$repeat" "$O" "$sha" >> "$A"
   127	         ;;
   128	     esac
   129	 done < <(/usr/bin/grep -E '^- \[P[0-3]\]' "$LR" | sort -u)
   130	[exit 0]
   131	```
   132	## 3. The Check
   133	```console
   134	$ uv run python -m unittest tests/unit/test_chain_review_scripts.py -v
   135	test_local_advisory_classes_a_repeat_by_the_earlier_row (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_advisory_classes_a_repeat_by_the_earlier_row) ... ok
   136	test_local_advisory_matches_the_owner_heading_literally (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_advisory_matches_the_owner_heading_literally) ... ok
   137	test_local_advisory_records_p2_rows_and_stops_on_p0_p1 (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_advisory_records_p2_rows_and_stops_on_p0_p1) ... ok
   138	test_local_advisory_refuses_a_malformed_owner_id (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_advisory_refuses_a_malformed_owner_id) ... ok
   139	test_local_advisory_refuses_an_absent_owner_task_and_hashes_the_file (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_advisory_refuses_an_absent_owner_task_and_hashes_the_file) ... ok
   140	test_local_review_and_local_advisory_refuse_a_task_or_head_that_leaves_their_directory (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_review_and_local_advisory_refuse_a_task_or_head_that_leaves_their_directory) ... ok
   141	test_local_review_keeps_env_S_shebang_arguments (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_review_keeps_env_S_shebang_arguments) ... ok
   142	test_local_review_pins_the_review_binary_interpreter (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_review_pins_the_review_binary_interpreter) ... ok
   143	test_local_review_refuses_a_quoted_env_S_shebang (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_review_refuses_a_quoted_env_S_shebang) ... ok
   144	test_local_review_resolves_codex_through_mise_and_refuses_a_shim (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_review_resolves_codex_through_mise_and_refuses_a_shim) ... ok
   145	test_local_review_resolves_the_review_binary_before_the_checkout (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_review_resolves_the_review_binary_before_the_checkout) ... ok
   146	test_local_review_reuses_only_a_file_that_records_this_head (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_review_reuses_only_a_file_that_records_this_head) ... ok
   147	test_local_review_runs_the_review_binary_read_only_at_the_head_and_writes_one_file (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_review_runs_the_review_binary_read_only_at_the_head_and_writes_one_file) ... ok
   148	test_local_review_strips_a_worktree_path_holding_sed_syntax_literally (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_review_strips_a_worktree_path_holding_sed_syntax_literally) ... ok
   149	test_local_review_writes_no_file_when_the_review_binary_fails (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_review_writes_no_file_when_the_review_binary_fails) ... ok
   150	test_sandbox_scan_prints_the_unsandboxed_mutation_calls (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_sandbox_scan_prints_the_unsandboxed_mutation_calls) ... ok
   151	
   152	----------------------------------------------------------------------
   153	Ran 16 tests in 7.404s
   154	
   155	OK
   156	[exit 0]
   157	```
   158	```console
   159	$ shellcheck scripts/orchestrator/local-advisory.sh && echo clean
   160	clean
   161	[exit 0]
   162	```
   163	```console
   164	$ shfmt -i 4 -sr -d scripts/orchestrator/local-advisory.sh && echo clean
   165	clean
   166	[exit 0]
   167	```
   168	```console
   169	$ ruff check --config ruff.toml tests/unit/test_chain_review_scripts.py && ruff format --config ruff.toml --check tests/unit/test_chain_review_scripts.py
   170	All checks passed!
   171	1 file already formatted
   172	[exit 0]
   173	```
   174	## 4. Mutation check (each mutant a literal string replacement applied alone, its test run, the file restored with git checkout; then a baseline run)
   175	```console
   176	$ bash "$TMPDIR/crs3/mutate.sh" (the script, then its output)
   177	S=scripts/orchestrator/local-advisory.sh T=tests/unit/test_chain_review_scripts.py
   178	lrun() { # label old new test: a literal string replacement (python's str.replace, once), the test, the restore
   179	    python3 -I -c 'import sys; p, a, b = sys.argv[1:]; t = open(p).read(); assert t.count(a) == 1, a; open(p, "w").write(t.replace(a, b))' "$S" "$2" "$3"
   180	    git diff -U0 -- "$S" | /usr/bin/grep -v -E '^(---|\+\+\+|@@|diff|index)' || echo "(nothing changed)"
   181	    UV_OFFLINE=1 uv run python -m unittest "$T" -k "$4" > "$TMPDIR/crs3/m.log" 2>&1
   182	    echo "mutant=$1 test=$4 rc=$? $(tail -1 "$TMPDIR/crs3/m.log")"
   183	    git checkout -- "$S"
   184	}
   185	A=test_local_advisory_refuses_an_absent_owner_task_and_hashes_the_file R=test_local_advisory_classes_a_repeat_by_the_earlier_row H=test_local_advisory_matches_the_owner_heading_literally
   186	lrun owner-check-off '[ -f "$O" ] ||' 'true ||' $A
   187	lrun old-evidence 'evidence=shasum -a 256 %s (%s)\n'"'"' "$h7" "$i" "$owner" "$(printf '"'"'%s'"'"' "$line" | cut -c1-120 | tr -d '"'"'`'"'"')" "$repeat" "$O" "$sha"' 'evidence=git show origin/main:%s | grep -n item\n'"'"' "$h7" "$i" "$owner" "$(printf '"'"'%s'"'"' "$line" | cut -c1-120 | tr -d '"'"'`'"'"')" "$repeat" "$O"' $A
   188	lrun repeat-off '[ -z "$row" ] || class=' 'true || class=' $R
   189	lrun first-row-wins '| tail -1 || true)' '| head -1 || true)' $R
   190	lrun range-token-off ':[0-9]+(-[0-9]+)?)' ':[0-9]+)' $R
   191	lrun heading-as-regex 'substr($0, 1, length(h)) == h && substr($0, length(h) + 1, 1) ~ /^ ?$/' '$0 ~ "^" h' $H
   192	UV_OFFLINE=1 uv run python -m unittest "$T" > "$TMPDIR/crs3/m.log" 2>&1; echo "baseline rc=$? $(tail -1 "$TMPDIR/crs3/m.log")"
   193	git status --short -- scripts/
   194	--- output
   195	-[ -f "$O" ] || {
   196	+true || {
   197	mutant=owner-check-off test=test_local_advisory_refuses_an_absent_owner_task_and_hashes_the_file rc=1 FAILED (failures=1)
   198	-        /usr/bin/grep -q "^local-finding: $h7:$i " "$A" || printf 'local-finding: %s:%s not-applicable:advisory P2 owned by %s (%s%s); evidence=shasum -a 256 %s (%s)\n' "$h7" "$i" "$owner" "$(printf '%s' "$line" | cut -c1-120 | tr -d '`')" "$repeat" "$O" "$sha" >> "$A"
   199	+        /usr/bin/grep -q "^local-finding: $h7:$i " "$A" || printf 'local-finding: %s:%s not-applicable:advisory P2 owned by %s (%s%s); evidence=git show origin/main:%s | grep -n item\n' "$h7" "$i" "$owner" "$(printf '%s' "$line" | cut -c1-120 | tr -d '`')" "$repeat" "$O" >> "$A"
   200	mutant=old-evidence test=test_local_advisory_refuses_an_absent_owner_task_and_hashes_the_file rc=1 FAILED (failures=1)
   201	-            [ -z "$row" ] || class=${row#*	} repeat="; repeat of ${row%%	*}"
   202	+            true || class=${row#*	} repeat="; repeat of ${row%%	*}"
   203	mutant=repeat-off test=test_local_advisory_classes_a_repeat_by_the_earlier_row rc=1 FAILED (failures=1)
   204	-            row=$(/usr/bin/grep -E "^(${ids%|})	" "$A" | /usr/bin/grep -v '	advisory-p2$' | tail -1 || true)
   205	+            row=$(/usr/bin/grep -E "^(${ids%|})	" "$A" | /usr/bin/grep -v '	advisory-p2$' | head -1 || true)
   206	mutant=first-row-wins test=test_local_advisory_classes_a_repeat_by_the_earlier_row rc=1 FAILED (failures=1)
   207	-token() { [[ $1 =~ ([A-Za-z0-9._/-]+:[0-9]+(-[0-9]+)?) ]] && printf '%s\n' "${BASH_REMATCH[1]}"; }
   208	+token() { [[ $1 =~ ([A-Za-z0-9._/-]+:[0-9]+) ]] && printf '%s\n' "${BASH_REMATCH[1]}"; }
   209	mutant=range-token-off test=test_local_advisory_classes_a_repeat_by_the_earlier_row rc=1 FAILED (failures=1)
   210	-awk -v h="## Owned by $owner" 'substr($0, 1, length(h)) == h && substr($0, length(h) + 1, 1) ~ /^ ?$/ { f = 1 } END { exit !f }' "$A" 2> /dev/null || printf '\n## Owned by %s (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)\n\n' "$owner" >> "$A"
   211	+awk -v h="## Owned by $owner" '$0 ~ "^" h { f = 1 } END { exit !f }' "$A" 2> /dev/null || printf '\n## Owned by %s (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)\n\n' "$owner" >> "$A"
   212	mutant=heading-as-regex test=test_local_advisory_matches_the_owner_heading_literally rc=1 FAILED (failures=1)
   213	baseline rc=0 OK
   214	[exit 0]
   215	```
   216	## 5. Caps
   217	```console
   218	$ git diff --numstat origin/main...HEAD
   219	3	0	.orchestration/dotfiles-T128-chain-review-scripts-followup-a03/autoskill.md
   220	6	0	.orchestration/dotfiles-T128-chain-review-scripts-followup-a03/learning.md
   221	72	0	.orchestration/dotfiles-T128-chain-review-scripts-followup-a03/report.md
   222	27	0	.orchestration/dotfiles-T128-chain-review-scripts-followup-a03/sandbox.md
   223	106	0	.orchestration/dotfiles-T128-chain-review-scripts-followup-a03/task.md
   224	219	0	.orchestration/dotfiles-T128-chain-review-scripts-followup-a03/validation.md
   225	38	5	scripts/orchestrator/local-advisory.sh
   226	60	2	tests/unit/test_chain_review_scripts.py
   227	[exit 0]
   228	```

 exited 1 in 210ms:
zsh:1: can't create temp file for here document: operation not permitted

 succeeded in 220ms:
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
114:## 1. Finding: the fix program tripped its own rule
116:By T126 INV-6 as written: wave 1 (PR #313) 8 amendments (limit 4) and 2 revises (limit 2); wave 3b (PR #314) Bot P1 on two post-RESULT heads. The orchestrator was drafting a waiver for #313. T120 was reset only on the operator's question. The regime is therefore reset here by its own rule; this document is the redesign, and T126 and T124 are superseded (their accepted ideas are kept where named).
131:## 2. Root causes, each with its evidence
135:## 3. Principles (each names what it reuses and what it deletes)
137:- **P1 One deterministic fact per round (INV-3).** Reuses tests/unit, CI, `pr-feedback.py`. Deletes free-form revise rounds and the audit-per-round habit.
138:- **P2 Declarative over imperative at trust boundaries (INV-1, INV-5, INV-7).** Reuses `jsonschema`, PyYAML, `codex exec --output-schema`, `claude -p --json-schema`. Deletes the bespoke YAML parser, the glob NFA, the prose verdict grammar, regex parsing of `.last.md`, and the T126 "process_tiers.json next to the module" indirection (the validator reads the manifest with PyYAML).
139:- **P3 Small one-invariant PRs enforced in CI (INV-2).** Reuses GitHub required checks and the strict up-to-date ruleset already in force. Deletes waves declared inside a task file.
140:- **P4 Main-pinned mechanical checks in CI; host gate only for history-anchored rules (INV-1, INV-2, INV-8 in CI; INV-3, INV-5 record, INV-6, INV-7 anchor, INV-11 on the host).** Reuses `pull_request_target`, the `changes` job pattern that reports success for an `.orchestration`-only diff. Deletes PR #313's `REVIEW_TREE` idea (never on `main`) and the copy step of untracked evidence into the gate's cwd. The host gate `make require-crit-review` keeps its evidence rules and changes three of them in named waves: the audit verdict and categories come from the schema JSON with the `AGMSG-AUDIT` record and the category lock (V2b), the reset backstop and the Bot-head count (V3a), the history-anchored design review (V4); it continues to run from the orchestrator's main checkout.
141:- **P5 Research before dispatch; a question ends the task, not amends it (INV-4).** Reuses history (`amendment=`, `status=question`). Deletes the amendment-per-question practice. The task file's `premises` block is the mechanical residue of "verify every CLI constraint by running the real command".
142:- **P6 Reset is mechanical, loop-time, and released only by another context or the operator (INV-6).** Reuses `scripts/require-crit-review.py` as the mandatory point, `agent-stop-gate.sh` and the Codex `[hooks].Stop` as the early signal (both soft by their documented caps: Claude's 8-continuation cap, Codex's continuation prompt), `check-regime-boundary.sh` for the re-dispatch detector. Deletes the orchestrator-written redesign (the redesign author is a `review`-profile seat or a fresh headless context; the `redesign` profile of T124 v4 is dropped: `review` is the same model and effort as `deep`, so independence of context is the whole lever, and T124 round 1 showed it works).
143:- **P7 Audit staging by tier; the auditor never serializes the pipeline (INV-5, process_tiers).** See section 4.
144:- **P8 Cost measured, budgets per tier (INV-9).** Reuses the JSON cost fields the runtimes already emit and the session transcripts. Deletes `cost: n/a`.
145:- **P9 Parallelism with disjoint files and early push (INV-10).** Reuses `herdr-agents --add-worker`, draft PRs.
148:## 4. Audit stages (process_tiers; the one table the validator reads)
152:| 0 design review | a fresh Claude context on the review profile and a Codex read-only review of the same hash, schema receipts (INV-7) | before any code | - | - | required | minutes |
153:| 1 worker checks | worker in its sandbox: invariant tests first, shellcheck, unit tests | before every push | required | required | required | none for the regime |
155:| 3 schema audit | headless read-only `codex exec --output-schema`, pooled 2, started by `make audit-head` once CI is green and the Bot reviewed or 15 min passed, once per RESULT head, reused for an evidence-only head by tree equality (INV-5) | per RESULT head | - | required | required, with invariant map and permgate window | the scarce resource, now off the critical path |
158:Tier derivation: docs = prose-only `allowed_files` outside the regime's own rule prose (`home/dot_config/claude/rules/**`, the agmsg-orchestration SKILL, `AGENTS.md`, README), which is review tier by explicit list; review = the existing review-tier paths (scripts, hooks, tests, templates); design = the explicit design-tier list from T124 INV-2 v3 (install/**, setup.sh, the gate scripts, `executable_herdr-agents`, `executable_permgate`, Codex and Claude policy, sandbox and permission settings, credential helpers). Round limits: docs 1 revise; review and design 2 revises then reset. Profiles: worker `standard` (docs `express`), review `review`, audit `audit`.
162:## 5. Enforcement map
164:| invariant | enforcement point |
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
200:## 7. Thresholds (operator confirmed 2026-10-11)
204:## 8. Disposition of the halted work
208:## 9. Residuals, stated
211:- `pull_request_target` runs with the base repository's token on a public repository: the `regime` job reads PR files as data with `contents: read` only, checks out `main`'s scripts, and never executes anything from the PR; a change to `.github/workflows/regime.yml` itself is a design-tier change under INV-1.
218:- The seven existing required checks still run on `pull_request` from the PR's own workflow files; INV-1's workflow-edit refusal in the `regime` job is what closes R8 for them.
221:## 10. Design review (round 15 requested: plan 006 A102, second pair)
223:Round 1 (`.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review.md`, `claude-review-dot-a001`, 2026-10-10T21:15Z, verdict `revise`): INV-7, INV-8, INV-11, INV-12 accepted with notes; INV-1, 2, 3, 4, 5, 6, 9, 10 rejected with corrections; findings F1-F9. v2 adopts every item: the task.md copy and `task_sha256` anchor (F1), the per-task invariant-set rule and the workflow-edit refusal (F2), the gate changes assigned to V2b/V3a/V4 with the category lock, the Bot-wait timeout and the tree-equality rule (F3), the merge backstop as the mandatory point, `original_commit_id`, the audit-JSON source, the Stop-hook budget split and the boundary detector (F4), the single amendment count over every TASK (F5), INV-9/INV-10 moved out of the Stop hook (F6), the reset records corrected to `claude-review-dot-a001` with the waiver form and the thread ids (F7), rule prose in the review tier (F8), premise 1 restated and three premises added (F9); plus the Q5 salvage list, the `make audit-head` target in place of a daemon, the `regime.yml` discipline and the hash note.
225:Round 2 (`…-design-review-round2.md`, 21:29Z, verdict `revise`): every round-1 correction confirmed applied; INV-2, INV-3, INV-6 rejected for contradictions v2 introduced, plus routing, cap and premise notes. v3 adopts all of them: `implementing_tasks` is a map of task id to invariant ids inside the hashed keys and the design-on-main precondition is stated (INV-2); `revise.yaml` is a sibling of the byte-identical task.md (INV-3, INV-8, INV-12, V3c, V2b); the question threshold is 2 and audit JSONs count only when their sha256 matches their record (INV-6); V3a is an operator PR with all hook counting, V3b has no hook source, V3c no gate source; the legacy list is excluded from the line cap as data; the `workflow_dispatch` premise is added; the stage-3 sentence names the orchestrator's `make audit-head`; INV-1 names the latest TASK's token and the recommit after each amendment. Round 3 (`…-design-review-round3.md`, 21:33Z, verdict `accept`) confirmed the five edits; its two notes are carried in the acceptance record. v4 (operator direction 2026-10-11, relayed by the review seat's PONG at 22:01Z) splits V1 by responsibility into V1 (validation only) and V1c (the CI check), adds `dotfiles-T128-v1c-regime-ci-check-a01: [INV-1]` to `implementing_tasks` (a hashed key, hence this round), reorders the waves (V1, V1c, V1b, …) and aligns section 7's cap wording with INV-2. Round 4 (`…-design-review-round4.md`, 22:06Z, verdict `accept`) confirmed the split; its note (INV-1's ruleset action is V1c's acceptance record) is carried. v5 answers the Codex Bot's finding on boundary PR #316 (thread 4239305441): INV-3's `ci:<job>` form had no enforcement, so `check=` is now a test selector or a `repro:<id>` whose command and output live in revise.yaml, each with its own regime-job verification. Round 5 (`…-design-review-round5.md`, 22:12Z, verdict `accept`) confirmed it. The Codex Bot then reviewed the second boundary head (c1e2582b) and raised six P1 and four P2 findings that three same-vendor accepts had not: the auditor read the schema and AGENTS.md from the audited head (INV-5 now runs from main as the instruction root with the worktree as data), the CI job had no previous RESULT head (INV-3 now records previous_head in the ACCEPTANCE and revise.yaml, cross-checked by the host gate), ids were compared without sentences (INV-2), `allowed_files: ['*']` derived a cheap tier and a branch copy could claim a legacy id (INV-1, INV-12), and two task records pointed at an abandoned prerequisite. v6 adopts all ten and, because a cross-vendor reviewer found what a same-vendor fresh context did not, INV-7 now requires both a Claude and a Codex review of each design hash. Round 6 (`…-design-review-round6.md`, 22:28Z, verdict `revise`) accepted INV-1, 2, 3, 5, 12 and rejected INV-7: the Bot form produced no receipt, hash or RESULT, so it would have been an orchestrator-written receipt for a review it did not perform (R5). v7 makes the Codex review a `codex exec --sandbox read-only` run under a `codex-review` identity with its own receipt and RESULT, names it in the enforcement row and V4, keeps the Bot's review as swept feedback, and adds the bare-mode skills premise (round-6 INV-5 note, acted on in V2). Round 7 (Claude, 22:31Z, `accept`) confirmed INV-7. The first Codex review (`…-design-review-round7-codex.md`, `codex-review-dot-h001`, 22:34Z, `reject`) rejected INV-1, 3, 4, 5, 6, 9, 10, 12, all on one theme: evidence the orchestrator authors. v8 answers each: the waiver becomes a command under a `permissions.ask` rule (INV-1, INV-6) with the one-account residual stated in section 9; `repro:` is dropped and `check=` is a test selector only (INV-3); premises are reviewer and auditor evidence and the counting is the mechanical part (INV-4); the audit carries an input manifest and the acceptance record has an audit-input boundary (INV-5); cost records name their raw sources and stay a warning metric (INV-9); first push is the first commit's committer date and dispatchability is defined (INV-10); the independent oracle for gate-script PRs is the trusted-root audit (INV-12). The Codex P2 on the bare-mode skills premise is not adopted: the headless page says verbatim that "A directory you name with --add-dir is a partial exception: bare mode loads skills from its .claude/skills/ folder". Codex round 8 (`…-design-review-round8-codex.md`, 22:39Z, `reject`) accepted INV-1, 6, 7, 8, 9, 11 and the one-account residual, withdrew its bare-mode P2, and rejected INV-2 (tests unbounded), INV-3 (a changed file is not a run selector), INV-4 (sampling), INV-5 (the skills refusal was a premise, not a rule), INV-10 (committer date is not a push time; dependencies), INV-12 (a model audit is not a deterministic oracle), plus two stale enforcement rows. v9 adopts all: a 1000-line cap under tests/; the exact selector run on both heads in the PR's required `revise-check` job; every premise dispositioned by each reviewer and the auditor; the `.claude/**` refusal inside INV-5; the draft PR's `created_at` and an `after` list for dispatchability; a `main-tests` required job running main's tests against the PR's scripts (V5c); the two rows fixed. Claude round 8 (`…-design-review-round8.md`, 22:41Z, `revise`) rejected INV-1 (the waive script had no owner or row), INV-5 (once-per-head versus re-audit on a stale manifest) and INV-10 (fixed in v9), and offered a stronger anchor: the waiver record in a directory outside the sandbox write roots. Codex round 9 (`…-design-review-round9-codex.md`, 22:46Z, `reject`) accepted ten, rejected INV-5 (the `.claude/**` refusal that v9 claimed was silently lost by a failed edit, confirmed by grep) and INV-12 (the oracle must precede the waves), dispositioned all twelve premises (nine hold, three unverifiable in its read-only sandbox), and raised GitHub's 2026-11-02 `pull_request_target` policy. v10: the refusal is in INV-5 and verified by grep; one valid audit per head with stale-manifest replacement; the runner computes the manifest; the waiver record lives outside the sandbox write roots and V3a owns the script (map entry `[INV-6, INV-1]`); `main-tests` is wave V0 and every code wave is contract-first (INV-12, INV-2); the policy premise and residual. Claude round 9 (`…-design-review-round9.md`, 22:46Z, `revise`) found that `main-tests` as drafted would fail every intentional change and proposed running main's modules only for scripts outside `allowed_files`; Codex round 10 (`…-design-review-round10-codex.md`, 22:50Z, `reject`) accepted INV-1..11 and found that contract-first tests cannot merge ahead of an implementation that changes an existing script, proposing dormant contracts that `main-tests` activates on the implementation PR. v11's INV-12 is the union: main's modules as they are for undeclared scripts, main's dormant contracts (`REGIME_CONTRACT=1`) for declared ones, contract PRs required for design-tier waves; INV-1 states that the record's location is the guard and the ask rule the second layer (Claude round 9). Codex round 11 (`…-design-review-round11-codex.md`, 22:52Z) accepted INV-1..12 with no findings. Claude round 11 (`…-design-review-round11.md`, 22:54Z, `revise`) accepted everything but two INV-12 clauses: contracts must not stay dormant forever (the implementation PR removes the decorator; main-tests judges it against main's dormant copy) and an empty contract must fail a design-tier implementation PR. v12 adds both sentences to INV-12 and V0. Claude round 12 (`…-design-review-round12.md`, 22:57Z) accepted v12; Codex round 12 (`…-design-review-round12-codex.md`, 22:57Z, `revise`) accepted INV-1..11 and asked for a failing check behind the decorator-removal clause. v13 adds it to INV-12 (main-tests fails an implementation PR whose declared test module still carries a contract marker) and V0 carries it with the task-file reviewer's three V0 items (main's tests overlaid on a copy of the PR tree, module selection from the task's declared tests/ entries, task.md read with PyYAML). Round 13 (Claude 23:01Z, Codex 23:01Z and the premise map 23:17Z) accepted v13. Plan 006 (approved 2026-10-11) A102 amends two hashed keys: INV-12 states the in-process oracle's authenticated completion (nonce runner) and its residual, after the Codex Bot's P1 on V0's round-1 head repeated the class of the round-0 audit's finding 3; INV-2 and the map gain the .orchestration-only CI skip (`dotfiles-T128-ci-skip-orchestration-a01`, plan A201) that plan 006 orders as Phase 2. Round 14 (Codex 02:42Z `accept`; Claude 02:43Z `revise`): INV-12's residual clause understated the gap (the nonce authenticates the writer, not the counts; in-process patching of unittest's result collection forges counts with a genuine nonce) and INV-2 should cover every required check. v15 states the residual as it is, adds the runner's pinning of unittest classes, and words INV-2 for every required workflow. Round 15 asks both reviewers at once for one verdict each on this hash. Sources are the repository paths under `.orchestration/validation/dotfiles-T128-regime-v3-a01-research/` (`baseline.md`, `practice-evidence.md`, `claude-code-factsheet.md`, `codex-factsheet.md`, `github-factsheet.md`, `method-draft.md`). Receipt: `.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round15.md` (Claude) and `…-design-review-round15-codex.md` (Codex); the whole-file sha256 of this file in both headers.
227:v18 (plan 006 B0, plan 007 T701; written by the orchestrator under the records exemption, 2026-10-12): INV-12 narrowed to the undeclared-change regression guard: `main-tests` runs main's test module of every script outside `allowed_files`; a script inside `allowed_files` is judged by the PR's tests, the diff review and the trusted-root audit; the dormant-contract clauses, `REGIME_CONTRACT` and the `<task>-contract-a01` PRs are removed (A302 withdrew V1's contract PR under the Phase A correction and no wave has used one); `main-tests` decides inside its own job as the A5 workflows do. INV-2 loses the dead `-contract-a01` comparison and names A5's in-job form. `implementing_tasks` gains the V0 successor `dotfiles-T128-v0-main-tests-a02: [INV-12]` (A301) and `dotfiles-T128-gate-evidence-a01: [INV-6]` (plan 007 T702: the gate's `evidence=` grammar and the S6 refusal at INV-6's mandatory point). The INV-12 enforcement row, the V0 wave row and the wave order follow. Round 20 asks both reviewers at once for one verdict each on this hash: receipts `.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round20.md` (Claude) and `…-design-review-round20-codex.md` (Codex); the whole-file sha256 of this file in both headers.
229:v19 (round 20's one revision, 11:43Z): INV-6 gains the clause the Claude round-20 receipt asked for (the Codex round-20 receipt accepted v18 with no rejection), so `dotfiles-T128-gate-evidence-a01: [INV-6]` maps to a sentence that states the two refusals; nothing else changes. Round 21 asks both reviewers at once for one verdict each on this hash: receipts `…-design-review-round21.md` (Claude) and `…-design-review-round21-codex.md` (Codex).
231:v20 (11:46Z): the Codex round-21 receipt found the v19 clause appended to INV-4 (a stale line number after v18's two map insertions), so v20 moves that exact clause to the end of INV-6; INV-4 returns to its v18 text; nothing else changes. Round 22 asks both reviewers at once for one verdict each on this hash (round 21 was never sent to the Claude seat): receipts `…-design-review-round22.md` (Claude) and `…-design-review-round22-codex.md` (Codex).
235:v21 (13:08Z, the orchestrator under the records exemption): `implementing_tasks` gains `dotfiles-T128-gate-evidence-a02: [INV-6]`, the INV-6 successor of `dotfiles-T128-gate-evidence-a01` (withdrawn 13:02Z under INV-6 before its second amendment; reset record `dotfiles-T128-gate-evidence-a01-design-reset.md`), beside the a01 entry that stays as parked history, as the V0 and round-18 successors did; nothing else changes. Round 24 asks both reviewers at once for one verdict each on this hash: receipts `…-design-review-round24.md` (Claude) and `…-design-review-round24-codex.md` (Codex).
237:v22 (15:28Z, the orchestrator under the records exemption): `implementing_tasks` gains `dotfiles-T128-gate-evidence-a03: [INV-6]`, the INV-6 successor of a02 (withdrawn 15:25Z after its second S1 cycle; plan 011 option F: the acceptance record's machine-read parts as YAML front matter), beside the a01 and a02 entries kept as parked history; nothing else changes. Round 25 asks both reviewers at once for one verdict each on this hash: receipts `…-design-review-round25.md` (Claude) and `…-design-review-round25-codex.md` (Codex).
239:v23 (2026-10-13 02:55Z, the orchestrator under the records exemption): `implementing_tasks` gains `dotfiles-T128-gate-evidence-a04: [INV-6]`, the INV-6 successor of a03 (withdrawn 02:3xZ after the fourth binding row; plan 014 option A: the acceptance record's `ledger` must cover every swept Codex finding id and every audit finding `audit:<sha7>:<n>`, a set difference the gate computes; the a04 file's hash is in the reset record `dotfiles-T128-gate-evidence-a03-design-reset.md`, not here), beside the a01 to a03 entries kept as parked history; nothing else changes. Round 26 asks both reviewers at once for one verdict each on this hash: receipts `…-design-review-round26.md` (Claude) and `…-design-review-round26-codex.md` (Codex).
241:v24 (2026-10-13 03:05Z, the orchestrator under the records exemption): the v23 line named the a04 file's hash, which moved when round 26's Codex half found the coverage sentence omitted badged Codex review bodies (a04 round 4 after round 3; no a04 hash appears in this design, the reset record `dotfiles-T128-gate-evidence-a03-design-reset.md` is the sole anchor, so later a04 rounds do not move the design); the map entry `dotfiles-T128-gate-evidence-a04: [INV-6]` is unchanged; nothing else changes. Rounds 27 and 28 ask both reviewers at once for one verdict each on this hash: receipts `…-design-review-round28.md` (Claude) and `…-design-review-round28-codex.md` (Codex); round 27's Codex half found the two hash mentions this text removed.

 succeeded in 238ms:
     1	#!/usr/bin/env bash
     2	# @file local-advisory.sh
     3	# @brief Record a local review's P2/P3 findings as advisory rows of the acceptance record; stop on a P0/P1.
     4	# @description
     5	#   Plan 020 step 1.2 for the local review. Reads `.orchestration/validation/<task>-local-review-<sha7>.md`. Each
     6	#   unique finding, numbered from 1: a P0/P1 prints STOP (the PR's one round is over: the plan's step 4.2); any
     7	#   other appends the row `local:<sha7>:<n><TAB><class>` under the heading `## Owned by <owner>` of
     8	#   `.orchestration/acceptance/<task>.md` (created when missing) and a `local-finding: <sha7>:<n>
     9	#   not-applicable:advisory P2 owned by <owner> (…); evidence=shasum -a 256 .orchestration/tasks/<owner>.md
    10	#   (<sha256>)` line, each only when the record lacks it. A review with findings needs the owner task file. The
    11	#   class is `advisory-p2`, unless the finding's `path:line[-line]` token (backticks ignored) matches a finding of
    12	#   the task's earlier local review files whose `local:` row in the record has another class: then the last such
    13	#   row's class, and the line's parenthesis names it as `repeat of local:<sha7>:<n>` (C-50).
    14	# @arg $1 string Task id, letters, digits, `.`, `_` and `-`.
    15	# @arg $2 string The reviewed head, 40 hex characters.
    16	# @arg $3 string The task id that owns the advisory findings, in the task id's form.
    17	# @exitcode 0 No P0/P1 finding.
    18	# @exitcode 2 No local review file, a malformed task id, head or owner task id, or (for a review with findings) no
    19	#   owner task file: `write the owner task <owner> first`.
    20	# @exitcode 3 A P0/P1 finding.
    21	# @example
    22	#   scripts/orchestrator/local-advisory.sh dotfiles-T128-x-a01 "$head" dotfiles-T128-x-followup-a01
    23	set -euo pipefail
    24	task=$1 head=$2 owner=$3
    25	# Both name the files read and appended, so a / in either would reach outside .orchestration (the audit of b6ce4ff).
    26	# The owner is written into the record verbatim, so it takes the task id's form too.
    27	id='^[A-Za-z0-9][A-Za-z0-9._-]*$'
    28	[[ $task =~ $id && $head =~ ^[0-9a-f]{40}$ && $owner =~ $id ]] || {
    29	    echo "usage: local-advisory.sh <task> <40-hex head> <owner task>"
    30	    exit 2
    31	}
    32	cd "$(git rev-parse --show-toplevel)"
    33	h7=${head:0:7}
    34	LR=".orchestration/validation/$task-local-review-$h7.md"
    35	A=".orchestration/acceptance/$task.md"
    36	[ -s "$LR" ] || {
    37	    echo "no local review file $LR"
    38	    exit 2
    39	}
    40	n=$(sed -n 's/^findings: //p' "$LR" | head -1)
    41	[ "${n:-0}" != "0" ] || {
    42	    echo "local review of $h7: no findings"
    43	    exit 0
    44	}
    45	# The rows name the owner task, so it must exist; its hash is evidence that replays before the boundary (C-51).
    46	O=".orchestration/tasks/$owner.md"
    47	[ -f "$O" ] || {
    48	    echo "write the owner task $owner first"
    49	    exit 2
    50	}
    51	sha=$(shasum -a 256 "$O" | cut -d' ' -f1)
    52	# C-50: a finding repeated from an earlier head takes the class the record gave it. Each earlier review's findings,
    53	# numbered as the loop below numbers them, as `<path:line[-line]> local:<sha7>:<n>` lines.
    54	# The class excludes the backtick, so `a.sh:1` in backticks reads as a.sh:1.
    55	token() { [[ $1 =~ ([A-Za-z0-9._/-]+:[0-9]+(-[0-9]+)?) ]] && printf '%s\n' "${BASH_REMATCH[1]}"; }
    56	earlier=""
    57	for f in .orchestration/validation/"$task"-local-review-*.md; do
    58	    [[ -f $f && $f != "$LR" ]] || continue
    59	    e=${f%.md} && e=${e##*-local-review-} && k=0
    60	    while IFS= read -r l; do
    61	        k=$((k + 1))
    62	        if t=$(token "$l"); then earlier+="$t local:$e:$k"$'\n'; fi
    63	    done < <(/usr/bin/grep -E '^- \[P[0-3]\]' "$f" | sort -u)
    64	done
    65	# A literal heading match, ended by a space or the line's end: a . in the owner is no wildcard, a longer id no match.
    66	awk -v h="## Owned by $owner" 'substr($0, 1, length(h)) == h && substr($0, length(h) + 1, 1) ~ /^ ?$/ { f = 1 } END { exit !f }' "$A" 2> /dev/null || printf '\n## Owned by %s (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)\n\n' "$owner" >> "$A"
    67	i=0 stop=0
    68	while IFS= read -r line; do
    69	    i=$((i + 1))
    70	    case "$line" in
    71	    *"[P0]"* | *"[P1]"*)
    72	        echo "STOP: local finding $i of $h7 is P0/P1: $line"
    73	        stop=1
    74	        ;;
    75	    *)
    76	        # The last row in the record of an earlier finding with this token, other than advisory-p2, wins.
    77	        class=advisory-p2 repeat=""
    78	        t=$(token "$line") || t=""
    79	        ids=$(printf '%s' "$earlier" | awk -v t="$t" '$1 == t { print $2 }' | tr '\n' '|')
    80	        if [[ -n $t && -n $ids ]]; then
    81	            row=$(/usr/bin/grep -E "^(${ids%|})	" "$A" | /usr/bin/grep -v '	advisory-p2$' | tail -1 || true)
    82	            [ -z "$row" ] || class=${row#*	} repeat="; repeat of ${row%%	*}"
    83	        fi
    84	        /usr/bin/grep -q "^local:$h7:$i	" "$A" || printf 'local:%s:%s\t%s\n' "$h7" "$i" "$class" >> "$A"
    85	        /usr/bin/grep -q "^local-finding: $h7:$i " "$A" || printf 'local-finding: %s:%s not-applicable:advisory P2 owned by %s (%s%s); evidence=shasum -a 256 %s (%s)\n' "$h7" "$i" "$owner" "$(printf '%s' "$line" | cut -c1-120 | tr -d '`')" "$repeat" "$O" "$sha" >> "$A"
    86	        ;;
    87	    esac
    88	done < <(/usr/bin/grep -E '^- \[P[0-3]\]' "$LR" | sort -u)
    89	echo "local review of $h7: $i finding(s) recorded as advisory under 'Owned by $owner' in $A"
    90	[ "$stop" = 0 ] || exit 3
"""Exercise the review-side chain scripts (plan 021 step 6.3) in a temporary git repository.

Each script runs as a subprocess from this checkout with the temporary repository as its working directory, so the
repository root it resolves is the temporary one. git is the real one. A stub review binary appends its argv, its
working directory, the HEAD there, PATH and its stdin to `<calls>/<name>.log`, prints `<calls>/transcript` and exits with
`<calls>/status` (0 when absent).
"""

import hashlib
import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[2] / "scripts/orchestrator"
GIT_ENV = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
STUB = (
    "#!/usr/bin/env bash\n"
    '{{ printf "argv:"; printf " %s" "$@"; printf "\\ncwd: %s\\nhead: %s\\npath: %s\\nstdin: %s\\n" '
    '"$(pwd -P)" "$(git rev-parse HEAD)" "$PATH" "$(cat)"; }} >> "$CALLS/{name}.log"\n'
    'cat "$CALLS/transcript"\nexit "$(cat "$CALLS/status" 2> /dev/null || echo 0)"\n'
)
ARGV = "argv: --profile review -s read-only review --base main"
SCAN_HIT = "sandbox scan: unsandboxed mutation calls above (C-29); judge before the audit"


class ChainReviewScriptsTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.temp = Path(temp.name).resolve()
        self.repo = self.temp / "repo"
        self.calls = self.temp / "calls"
        self.calls.mkdir()
        self.git("init", "-q", "-b", "main", str(self.repo), cwd=self.temp)
        self.write("a.txt", "a\n")
        self.git("add", "a.txt")
        self.git("commit", "-q", "-m", "main")
        self.env = {**os.environ, **GIT_ENV, "CALLS": str(self.calls), "TMPDIR": str(self.temp)}
        for name in ("CODEX_BIN", "ORCH_REVIEW_WORKTREE"):
            self.env.pop(name, None)

    def git(self, *args, cwd=None):
        return subprocess.run(
            ["git", "-c", "commit.gpgsign=false", *args],
            cwd=cwd or self.repo,
            env={**os.environ, **GIT_ENV},
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()

    def write(self, rel, text, root=None):
        path = (root or self.repo) / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def stub(self, path, name):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(STUB.format(name=name))
        path.chmod(0o755)

    def mise(self, body):
        """A mise stub first on PATH; it runs under env -i, so it carries the calls directory itself."""
        path = self.temp / "bin/mise"
        path.parent.mkdir(parents=True, exist_ok=True)
        log = f'echo "argv: $* MISE_CONFIG_FILE=${{MISE_CONFIG_FILE:-unset}}" >> "{self.calls}/mise.log"\n'
        path.write_text("#!/bin/bash\n" + log + body)
        path.chmod(0o755)

    def review_head(self, name="review"):
        """A clean review worktree at main, a head commit made in it, codex stubbed and mise failing on PATH."""
        review = self.temp / name
        self.git("worktree", "add", "-q", "--detach", str(review), "main")
        self.write("b.txt", "b\n", root=review)
        self.git("add", "b.txt", cwd=review)
        self.git("commit", "-q", "-m", "head", cwd=review)
        head = self.git("rev-parse", "HEAD", cwd=review)
        self.git("checkout", "-q", "--detach", "main", cwd=review)
        self.stub(self.temp / "bin/codex", "codex")
        self.mise("exit 1\n")
        (self.repo / ".orchestration/validation").mkdir(parents=True, exist_ok=True)
        path = f"{self.temp / 'bin'}{os.pathsep}{os.environ['PATH']}"
        return review, head, {"ORCH_REVIEW_WORKTREE": str(review), "PATH": path}

    def log(self, name):
        path = self.calls / f"{name}.log"
        return path.read_text() if path.exists() else ""

    def run_tool(self, name, *args, code=0, env=None, cwd=None):
        # The review binary must not read what the caller's stdin holds.
        result = subprocess.run(
            ["bash", str(TOOLS / name), *map(str, args)],
            capture_output=True,
            text=True,
            input="caller stdin\n",
            cwd=cwd or self.repo,
            env={**self.env, **(env or {})},
            timeout=30,
            check=False,
        )
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        return result.stdout

    def test_local_review_runs_the_review_binary_read_only_at_the_head_and_writes_one_file(self):
        review = self.temp / "review"
        self.git("worktree", "add", "-q", "--detach", str(review), "main")
        # The head commit, made in the review worktree, carries a decoy bin/codex; the main working tree never does.
        self.stub(review / "bin/codex", "decoy")
        self.write("b.txt", "b\n", root=review)
        self.git("add", "bin/codex", "b.txt", cwd=review)
        self.git("commit", "-q", "-m", "head", cwd=review)
        head, base = self.git("rev-parse", "HEAD", cwd=review), self.git("rev-parse", "main")
        self.git("checkout", "-q", "--detach", "main", cwd=review)
        self.stub(self.temp / "bin/codex", "codex")
        self.mise("exit 1\n")
        (self.repo / ".orchestration/validation").mkdir(parents=True)
        path = f"./bin{os.pathsep}{self.temp / 'bin'}{os.pathsep}{os.environ['PATH']}"
        env = {"ORCH_REVIEW_WORKTREE": str(review), "PATH": path}
        # An earlier marker's message is not the final one; the worktree prefix is stripped; a repeated line counts once.
        final = f"One finding.\n- [P2] {review}/b.txt:1 b is new\n- [P2] {review}/b.txt:1 b is new\n"
        (self.calls / "transcript").write_text(f"codex\n- [P1] {review}/a.txt:1 superseded\ncodex\n{final}")
        finding = "- [P2] b.txt:1 b is new"
        call = f"{ARGV}\ncwd: {review}\nhead: {head}\npath: {path}\nstdin: \n"

        def out(task):
            return self.repo / f".orchestration/validation/{task}-local-review-{head[:7]}.md"

        with self.subTest("a review worktree path without its own .git entry exits 2"):
            # First, while the main working tree is clean: the dirty check alone would pass it.
            (self.repo / "plain").mkdir()
            plain = {**env, "ORCH_REVIEW_WORKTREE": str(self.repo / "plain")}

**Limiting output length**
codex
実装には、owner ファイル不在時に書き込まない処理と、過去の行から class を引き継ぐ処理があります。保存済みの最終 head の CI 証跡は12件成功ですが、GitHub API には接続できないため、ライブ再確認はできていません。続けて、反復判定の境界条件と記録の整合性を確認します。
exec
/bin/zsh -lc "nl -ba .orchestration/tasks/dotfiles-T128-regime-v3-a01.md | sed -n '1,155p'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 0ms:
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

**Analyzing missing invariants in task schemas**
exec
/bin/zsh -lc "python3 -B - <<'PY'
import json,subprocess
from pathlib import Path
x=json.loads(Path('.ua/knowledge-graph.json').read_text())
for n in x.get('nodes',[]):
 if any(v in str(n.get('filePath','')) for v in ['local-advisory','chain-review','regime','task-consistency']):
  print(n.get('filePath'),str(n.get('summary',''))[:250])
r=subprocess.check_output(['git','diff','--name-only','940a3a2b07adfd14140a0acff96784ef53a0a509..HEAD'],text=True).splitlines()
print('graph stale; non-metadata changed files:',sum(not f.startswith(('.ua/','.orchestration/')) for f in r))
PY" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc 'git show d3e8acfe553791577576282eb0c339c018721bde:scripts/orchestrator/local-advisory.sh | nl -ba' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc "git ls-tree --name-only d3e8acfe553791577576282eb0c339c018721bde schemas/ && rg -n 'local-advisory|INV-2|invariants' scripts/orchestrator/chain-integrate.sh scripts/orchestrator/task-consistency-check.py home/dot_config/claude/rules/agmsg-orchestration.md schemas/task.json" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc "git diff --name-status b167fe0a76a2e77d262f9f556c69ba6b9f118bbe d3e8acfe553791577576282eb0c339c018721bde && git log --format='%h %p %s' b167fe0a76a2e77d262f9f556c69ba6b9f118bbe..d3e8acfe553791577576282eb0c339c018721bde && git show d3e8acfe553791577576282eb0c339c018721bde:.orchestration/dotfiles-T128-chain-review-scripts-followup-a03/learning.md && git show d3e8acfe553791577576282eb0c339c018721bde:.orchestration/dotfiles-T128-chain-review-scripts-followup-a03/autoskill.md" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 108ms:
     1	#!/usr/bin/env bash
     2	# @file local-advisory.sh
     3	# @brief Record a local review's P2/P3 findings as advisory rows of the acceptance record; stop on a P0/P1.
     4	# @description
     5	#   Plan 020 step 1.2 for the local review. Reads `.orchestration/validation/<task>-local-review-<sha7>.md`. Each
     6	#   unique finding, numbered from 1: a P0/P1 prints STOP (the PR's one round is over: the plan's step 4.2); any
     7	#   other appends the row `local:<sha7>:<n><TAB><class>` under the heading `## Owned by <owner>` of
     8	#   `.orchestration/acceptance/<task>.md` (created when missing) and a `local-finding: <sha7>:<n>
     9	#   not-applicable:advisory P2 owned by <owner> (…); evidence=shasum -a 256 .orchestration/tasks/<owner>.md
    10	#   (<sha256>)` line, each only when the record lacks it. A review with findings needs the owner task file. The
    11	#   class is `advisory-p2`, unless the finding's `path:line[-line]` token (backticks ignored) matches a finding of
    12	#   the task's earlier local review files whose `local:` row in the record has another class: then the last such
    13	#   row's class, and the line's parenthesis names it as `repeat of local:<sha7>:<n>` (C-50).
    14	# @arg $1 string Task id, letters, digits, `.`, `_` and `-`.
    15	# @arg $2 string The reviewed head, 40 hex characters.
    16	# @arg $3 string The task id that owns the advisory findings, in the task id's form.
    17	# @exitcode 0 No P0/P1 finding.
    18	# @exitcode 2 No local review file, a malformed task id, head or owner task id, or (for a review with findings) no
    19	#   owner task file: `write the owner task <owner> first`.
    20	# @exitcode 3 A P0/P1 finding.
    21	# @example
    22	#   scripts/orchestrator/local-advisory.sh dotfiles-T128-x-a01 "$head" dotfiles-T128-x-followup-a01
    23	set -euo pipefail
    24	task=$1 head=$2 owner=$3
    25	# Both name the files read and appended, so a / in either would reach outside .orchestration (the audit of b6ce4ff).
    26	# The owner is written into the record verbatim, so it takes the task id's form too.
    27	id='^[A-Za-z0-9][A-Za-z0-9._-]*$'
    28	[[ $task =~ $id && $head =~ ^[0-9a-f]{40}$ && $owner =~ $id ]] || {
    29	    echo "usage: local-advisory.sh <task> <40-hex head> <owner task>"
    30	    exit 2
    31	}
    32	cd "$(git rev-parse --show-toplevel)"
    33	h7=${head:0:7}
    34	LR=".orchestration/validation/$task-local-review-$h7.md"
    35	A=".orchestration/acceptance/$task.md"
    36	[ -s "$LR" ] || {
    37	    echo "no local review file $LR"
    38	    exit 2
    39	}
    40	n=$(sed -n 's/^findings: //p' "$LR" | head -1)
    41	[ "${n:-0}" != "0" ] || {
    42	    echo "local review of $h7: no findings"
    43	    exit 0
    44	}
    45	# The rows name the owner task, so it must exist; its hash is evidence that replays before the boundary (C-51).
    46	O=".orchestration/tasks/$owner.md"
    47	[ -f "$O" ] || {
    48	    echo "write the owner task $owner first"
    49	    exit 2
    50	}
    51	sha=$(shasum -a 256 "$O" | cut -d' ' -f1)
    52	# C-50: a finding repeated from an earlier head takes the class the record gave it. Each earlier review's findings,
    53	# numbered as the loop below numbers them, as `<path:line[-line]> local:<sha7>:<n>` lines.
    54	# The class excludes the backtick, so `a.sh:1` in backticks reads as a.sh:1.
    55	token() { [[ $1 =~ ([A-Za-z0-9._/-]+:[0-9]+(-[0-9]+)?) ]] && printf '%s\n' "${BASH_REMATCH[1]}"; }
    56	earlier=""
    57	for f in .orchestration/validation/"$task"-local-review-*.md; do
    58	    [[ -f $f && $f != "$LR" ]] || continue
    59	    e=${f%.md} && e=${e##*-local-review-} && k=0
    60	    while IFS= read -r l; do
    61	        k=$((k + 1))
    62	        if t=$(token "$l"); then earlier+="$t local:$e:$k"$'\n'; fi
    63	    done < <(/usr/bin/grep -E '^- \[P[0-3]\]' "$f" | sort -u)
    64	done
    65	# A literal heading match, ended by a space or the line's end: a . in the owner is no wildcard, a longer id no match.
    66	awk -v h="## Owned by $owner" 'substr($0, 1, length(h)) == h && substr($0, length(h) + 1, 1) ~ /^ ?$/ { f = 1 } END { exit !f }' "$A" 2> /dev/null || printf '\n## Owned by %s (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)\n\n' "$owner" >> "$A"
    67	i=0 stop=0
    68	while IFS= read -r line; do
    69	    i=$((i + 1))
    70	    case "$line" in
    71	    *"[P0]"* | *"[P1]"*)
    72	        echo "STOP: local finding $i of $h7 is P0/P1: $line"
    73	        stop=1
    74	        ;;
    75	    *)
    76	        # The last row in the record of an earlier finding with this token, other than advisory-p2, wins.
    77	        class=advisory-p2 repeat=""
    78	        t=$(token "$line") || t=""
    79	        ids=$(printf '%s' "$earlier" | awk -v t="$t" '$1 == t { print $2 }' | tr '\n' '|')
    80	        if [[ -n $t && -n $ids ]]; then
    81	            row=$(/usr/bin/grep -E "^(${ids%|})	" "$A" | /usr/bin/grep -v '	advisory-p2$' | tail -1 || true)
    82	            [ -z "$row" ] || class=${row#*	} repeat="; repeat of ${row%%	*}"
    83	        fi
    84	        /usr/bin/grep -q "^local:$h7:$i	" "$A" || printf 'local:%s:%s\t%s\n' "$h7" "$i" "$class" >> "$A"
    85	        /usr/bin/grep -q "^local-finding: $h7:$i " "$A" || printf 'local-finding: %s:%s not-applicable:advisory P2 owned by %s (%s%s); evidence=shasum -a 256 %s (%s)\n' "$h7" "$i" "$owner" "$(printf '%s' "$line" | cut -c1-120 | tr -d '`')" "$repeat" "$O" "$sha" >> "$A"
    86	        ;;
    87	    esac
    88	done < <(/usr/bin/grep -E '^- \[P[0-3]\]' "$LR" | sort -u)
    89	echo "local review of $h7: $i finding(s) recorded as advisory under 'Owned by $owner' in $A"
    90	[ "$stop" = 0 ] || exit 3

 exited 1 in 168ms:
zsh:1: can't create temp file for here document: operation not permitted

 exited 2 in 228ms:
rg: schemas/task.json: No such file or directory (os error 2)
scripts/orchestrator/chain-integrate.sh:73:for s in scripts/orchestrator/{sandbox-scan.sh,local-review.sh,local-advisory.sh,fill_sweep.py,acceptance-front-matter.py,orch-audit.sh} scripts/pr-feedback.py; do
scripts/orchestrator/chain-integrate.sh:146:    step local-advisory 0,3 "${main}/scripts/orchestrator/local-advisory.sh" "${task}" "${head}" "${owner}"
home/dot_config/claude/rules/agmsg-orchestration.md:13:- **Boundaries.** At every regime or session boundary, run the Stop checklist ("Review and integration invariants"), which `make check-regime-boundary` checks; records reach `main` only between integrations (plan 020 step 3). Codify session lessons through a task, never auto-memory.

 succeeded in 238ms:
A	.orchestration/dotfiles-T128-chain-review-scripts-followup-a03/autoskill.md
A	.orchestration/dotfiles-T128-chain-review-scripts-followup-a03/learning.md
A	.orchestration/dotfiles-T128-chain-review-scripts-followup-a03/report.md
A	.orchestration/dotfiles-T128-chain-review-scripts-followup-a03/sandbox.md
A	.orchestration/dotfiles-T128-chain-review-scripts-followup-a03/task.md
A	.orchestration/dotfiles-T128-chain-review-scripts-followup-a03/validation.md
M	scripts/orchestrator/local-advisory.sh
M	tests/unit/test_chain_review_scripts.py
d3e8acfe 1e0c2e92 b167fe0a Merge branch 'main' into tools/chain-review-scripts-followup-a03
1e0c2e92 9da0897a docs(orchestration): chain-review-scripts followup a03 evidence update (the Bot's clean review, CI's ShellCheck fix 9da0897a)
9da0897a d2b33025 fix(orchestrator): local-advisory.sh numbers each earlier finding with an if, not A && B || C (CI ShellCheck SC2015)
d2b33025 a1ddb211 docs(orchestration): chain-review-scripts followup a03 task copy and evidence (a311781d, a1ddb211)
a1ddb211 a311781d test(orchestrator): the repeat test tells a line range from a wider one; the token reads a backticked path as itself (T128 chain-review-scripts followup a03)
a311781d f7847616 fix(orchestrator): local-advisory.sh refuses an absent owner task, hashes the owner file as evidence, and classes a repeated finding by the earlier row (T128 chain-review-scripts followup a03)
# Learning triage: dotfiles-T128-chain-review-scripts-followup-a03

These are candidates only; nothing is promoted.

1. [memory:decision] A mutant that survives is either a test gap or code with no effect. This run had one of each: the line-range token was untested (a `y.sh:3-9` case now tells it from `y.sh:3-5`), and a backtick strip did nothing because the token's character class already excludes the backtick, so the strip was deleted rather than tested.
2. [memory:decision] Mutants written as literal string replacements (Python's `str.replace`, asserted to match once) avoid both sed's regex escaping and perl's variable interpolation inside `\Q…\E`, which made an earlier task's perl mutants change nothing.
3. [memory:decision] CI's ShellCheck can report what the local 0.11.0 does not (SC2015 on `A && B || C`, PR #381), so a chained `&& … || true` in a new script is written as an `if` from the start.
# AutoSkill run: dotfiles-T128-chain-review-scripts-followup-a03

- Status: not used. The task names no AutoSkill run.

**Analyzing command and file handling nuances**
**Assessing security and filtering issues**
exec
/bin/zsh -lc "git show d3e8acfe553791577576282eb0c339c018721bde:tests/unit/test_chain_review_scripts.py | sed -n '1,125p;350,505p'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc "python3 -B -c 'import json,subprocess; from pathlib import Path; x=json.loads(Path(\".ua/knowledge-graph.json\").read_text()); print([(n.get(\"filePath\"),str(n.get(\"summary\",\"\"))[:200]) for n in x.get(\"nodes\",[]) if any(v in str(n.get(\"filePath\",\"\")) for v in [\"local-advisory\",\"chain-review\",\"regime\",\"task-consistency\"])]); r=subprocess.check_output([\"git\",\"diff\",\"--name-only\",\"940a3a2b07adfd14140a0acff96784ef53a0a509..HEAD\"],text=True).splitlines(); print(\"graph stale; non-metadata changed files:\",sum(not f.startswith((\".ua/\",\".orchestration/\")) for f in r))'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc "git show d3e8acfe553791577576282eb0c339c018721bde:scripts/orchestrator/chain-integrate.sh | nl -ba | sed -n '100,176p' && git show d3e8acfe553791577576282eb0c339c018721bde:scripts/orchestrator/task-consistency-check.py | sed -n '1,150p'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 105ms:
"""Exercise the review-side chain scripts (plan 021 step 6.3) in a temporary git repository.

Each script runs as a subprocess from this checkout with the temporary repository as its working directory, so the
repository root it resolves is the temporary one. git is the real one. A stub review binary appends its argv, its
working directory, the HEAD there, PATH and its stdin to `<calls>/<name>.log`, prints `<calls>/transcript` and exits with
`<calls>/status` (0 when absent).
"""

import hashlib
import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[2] / "scripts/orchestrator"
GIT_ENV = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
STUB = (
    "#!/usr/bin/env bash\n"
    '{{ printf "argv:"; printf " %s" "$@"; printf "\\ncwd: %s\\nhead: %s\\npath: %s\\nstdin: %s\\n" '
    '"$(pwd -P)" "$(git rev-parse HEAD)" "$PATH" "$(cat)"; }} >> "$CALLS/{name}.log"\n'
    'cat "$CALLS/transcript"\nexit "$(cat "$CALLS/status" 2> /dev/null || echo 0)"\n'
)
ARGV = "argv: --profile review -s read-only review --base main"
SCAN_HIT = "sandbox scan: unsandboxed mutation calls above (C-29); judge before the audit"


class ChainReviewScriptsTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.temp = Path(temp.name).resolve()
        self.repo = self.temp / "repo"
        self.calls = self.temp / "calls"
        self.calls.mkdir()
        self.git("init", "-q", "-b", "main", str(self.repo), cwd=self.temp)
        self.write("a.txt", "a\n")
        self.git("add", "a.txt")
        self.git("commit", "-q", "-m", "main")
        self.env = {**os.environ, **GIT_ENV, "CALLS": str(self.calls), "TMPDIR": str(self.temp)}
        for name in ("CODEX_BIN", "ORCH_REVIEW_WORKTREE"):
            self.env.pop(name, None)

    def git(self, *args, cwd=None):
        return subprocess.run(
            ["git", "-c", "commit.gpgsign=false", *args],
            cwd=cwd or self.repo,
            env={**os.environ, **GIT_ENV},
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()

    def write(self, rel, text, root=None):
        path = (root or self.repo) / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def stub(self, path, name):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(STUB.format(name=name))
        path.chmod(0o755)

    def mise(self, body):
        """A mise stub first on PATH; it runs under env -i, so it carries the calls directory itself."""
        path = self.temp / "bin/mise"
        path.parent.mkdir(parents=True, exist_ok=True)
        log = f'echo "argv: $* MISE_CONFIG_FILE=${{MISE_CONFIG_FILE:-unset}}" >> "{self.calls}/mise.log"\n'
        path.write_text("#!/bin/bash\n" + log + body)
        path.chmod(0o755)

    def review_head(self, name="review"):
        """A clean review worktree at main, a head commit made in it, codex stubbed and mise failing on PATH."""
        review = self.temp / name
        self.git("worktree", "add", "-q", "--detach", str(review), "main")
        self.write("b.txt", "b\n", root=review)
        self.git("add", "b.txt", cwd=review)
        self.git("commit", "-q", "-m", "head", cwd=review)
        head = self.git("rev-parse", "HEAD", cwd=review)
        self.git("checkout", "-q", "--detach", "main", cwd=review)
        self.stub(self.temp / "bin/codex", "codex")
        self.mise("exit 1\n")
        (self.repo / ".orchestration/validation").mkdir(parents=True, exist_ok=True)
        path = f"{self.temp / 'bin'}{os.pathsep}{os.environ['PATH']}"
        return review, head, {"ORCH_REVIEW_WORKTREE": str(review), "PATH": path}

    def log(self, name):
        path = self.calls / f"{name}.log"
        return path.read_text() if path.exists() else ""

    def run_tool(self, name, *args, code=0, env=None, cwd=None):
        # The review binary must not read what the caller's stdin holds.
        result = subprocess.run(
            ["bash", str(TOOLS / name), *map(str, args)],
            capture_output=True,
            text=True,
            input="caller stdin\n",
            cwd=cwd or self.repo,
            env={**self.env, **(env or {})},
            timeout=30,
            check=False,
        )
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        return result.stdout

    def test_local_review_runs_the_review_binary_read_only_at_the_head_and_writes_one_file(self):
        review = self.temp / "review"
        self.git("worktree", "add", "-q", "--detach", str(review), "main")
        # The head commit, made in the review worktree, carries a decoy bin/codex; the main working tree never does.
        self.stub(review / "bin/codex", "decoy")
        self.write("b.txt", "b\n", root=review)
        self.git("add", "bin/codex", "b.txt", cwd=review)
        self.git("commit", "-q", "-m", "head", cwd=review)
        head, base = self.git("rev-parse", "HEAD", cwd=review), self.git("rev-parse", "main")
        self.git("checkout", "-q", "--detach", "main", cwd=review)
        self.stub(self.temp / "bin/codex", "codex")
        self.mise("exit 1\n")
        (self.repo / ".orchestration/validation").mkdir(parents=True)
        path = f"./bin{os.pathsep}{self.temp / 'bin'}{os.pathsep}{os.environ['PATH']}"
        env = {"ORCH_REVIEW_WORKTREE": str(review), "PATH": path}
        # An earlier marker's message is not the final one; the worktree prefix is stripped; a repeated line counts once.
        final = f"One finding.\n- [P2] {review}/b.txt:1 b is new\n- [P2] {review}/b.txt:1 b is new\n"
        (self.calls / "transcript").write_text(f"codex\n- [P1] {review}/a.txt:1 superseded\ncodex\n{final}")
                self.assertEqual("", self.log("codex"))

    def test_local_advisory_records_p2_rows_and_stops_on_p0_p1(self):
        head, owner = "abcdef0" + "1" * 33, "t-followup-a01"
        record = self.write(".orchestration/acceptance/t-a01.md", "# record\n")
        sha = hashlib.sha256(self.write(f".orchestration/tasks/{owner}.md", "owner\n").read_bytes()).hexdigest()
        heading = f"## Owned by {owner} (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)\n"
        # Numbered in sort order; the second is cut to 120 characters, then loses its backticks.
        first, long = "- [P2] `a.sh:1` first", "- [P2] `b.sh:3` " + "y" * 130

        def review(*findings):
            front = f"---\ntask: t-a01\nfindings: {len(findings)}\n---\n\n"
            # Each finding appears twice, in the list and in the transcript, as the local review writes it.
            text = "\n".join(findings)
            self.write(f".orchestration/validation/t-a01-local-review-{head[:7]}.md", f"{front}{text}\n\n{text}\n")

        def line(n, finding):
            text = finding[:120].replace("`", "")
            return (
                f"local-finding: abcdef0:{n} not-applicable:advisory P2 owned by {owner} ({text}); "
                f"evidence=shasum -a 256 .orchestration/tasks/{owner}.md ({sha})\n"
            )

        review(long, first)
        for _ in range(2):
            stdout = self.run_tool("local-advisory.sh", "t-a01", head, owner)
        self.assertEqual(
            f"local review of abcdef0: 2 finding(s) recorded as advisory under 'Owned by {owner}' in .orchestration/acceptance/t-a01.md\n",
            stdout,
        )
        rows = "local:abcdef0:1\tadvisory-p2\n" + line(1, first)
        rows += "local:abcdef0:2\tadvisory-p2\n" + line(2, long)
        self.assertEqual(f"# record\n\n{heading}\n{rows}", record.read_text())
        record.write_text("# record\n")
        review("- [P1] a.sh:1 blocks", "- [P2] b.sh:2 second")
        stdout = self.run_tool("local-advisory.sh", "t-a01", head, owner, code=3)
        self.assertIn("STOP: local finding 1 of abcdef0 is P0/P1: - [P1] a.sh:1 blocks\n", stdout)
        rows = "local:abcdef0:2\tadvisory-p2\n" + line(2, "- [P2] b.sh:2 second")
        self.assertEqual(f"# record\n\n{heading}\n{rows}", record.read_text())
        record.write_text("# record\n")
        review("- [P0] c.sh:1 breaks")
        stdout = self.run_tool("local-advisory.sh", "t-a01", head, owner, code=3)
        self.assertIn("STOP: local finding 1 of abcdef0 is P0/P1: - [P0] c.sh:1 breaks\n", stdout)
        self.assertEqual(f"# record\n\n{heading}\n", record.read_text())
        record.write_text("# record\n")
        review()
        self.assertEqual(
            "local review of abcdef0: no findings\n", self.run_tool("local-advisory.sh", "t-a01", head, owner)
        )
        self.assertEqual("# record\n", record.read_text())
        self.assertIn("no local review file", self.run_tool("local-advisory.sh", "t-b01", head, owner, code=2))

    def test_local_advisory_refuses_a_malformed_owner_id(self):
        # The owner is a grep pattern and verbatim record text; a malformed one changes nothing.
        head = "abcdef0" + "1" * 33
        self.write(f".orchestration/validation/t-a01-local-review-{head[:7]}.md", "---\nfindings: 1\n---\n\n- [P2] x\n")
        for owner in ("", "../x", "a b", "a\nb", ".*", "-a"):
            with self.subTest(owner=owner):
                self.assertIn("usage:", self.run_tool("local-advisory.sh", "t-a01", head, owner, code=2))
        self.assertFalse((self.repo / ".orchestration/acceptance").exists())

    def test_local_advisory_matches_the_owner_heading_literally(self):
        # A dotted owner is no wildcard, and a longer id that starts with the owner is another owner.
        head = "abcdef0" + "1" * 33
        self.write(f".orchestration/validation/t-a01-local-review-{head[:7]}.md", "---\nfindings: 1\n---\n\n- [P2] x\n")
        # tXfollowup-a01 matches t.followup-a01 as a regex, anchored or not (the audit of 40f3be4, finding 2).
        near = "# record\n## Owned by t-followupXa01 (x)\n## Owned by t.followup-a01b (x)\n## Owned by tXfollowup-a01 (x)\n"
        record = self.write(".orchestration/acceptance/t-a01.md", near)
        self.write(".orchestration/tasks/t.followup-a01.md", "owner\n")
        self.run_tool("local-advisory.sh", "t-a01", head, "t.followup-a01")
        self.assertEqual(1, record.read_text().count("\n## Owned by t.followup-a01 (advisory P2"))
        self.run_tool("local-advisory.sh", "t-a01", head, "t.followup-a01")
        self.assertEqual(1, record.read_text().count("\n## Owned by t.followup-a01 (advisory P2"))
        self.assertTrue(record.read_text().startswith(near))

    def test_local_advisory_refuses_an_absent_owner_task_and_hashes_the_file(self):
        # C-51: no row names an owner task that does not exist, and the evidence replays before the boundary.
        head, owner = "abcdef0" + "1" * 33, "t-followup-a01"
        self.write(f".orchestration/validation/t-a01-local-review-{head[:7]}.md", "---\nfindings: 1\n---\n\n- [P2] x\n")
        record = self.write(".orchestration/acceptance/t-a01.md", "# record\n")
        self.assertIn(
            f"write the owner task {owner} first", self.run_tool("local-advisory.sh", "t-a01", head, owner, code=2)
        )
        self.assertEqual("# record\n", record.read_text())
        owner_file = self.write(f".orchestration/tasks/{owner}.md", "# the owner task\n")
        self.run_tool("local-advisory.sh", "t-a01", head, owner)
        sha = hashlib.sha256(owner_file.read_bytes()).hexdigest()
        [line] = [line for line in record.read_text().splitlines() if line.startswith("local-finding:")]
        self.assertTrue(line.endswith(f"; evidence=shasum -a 256 .orchestration/tasks/{owner}.md ({sha})"), line)

    def test_local_advisory_classes_a_repeat_by_the_earlier_row(self):
        # C-50: a finding found again on a later head takes the class the record gave the earlier finding, so the
        # three-rows rule can count it; the later head's row wins, and a line range is a token.
        owner, v = "t-followup-a01", ".orchestration/validation"
        self.write(f".orchestration/tasks/{owner}.md", "owner\n")
        self.write(
            f"{v}/t-a01-local-review-aaaaaa1.md",
            "---\nfindings: 2\n---\n\n- [P2] scripts/x.sh:12 quoting\n- [P2] scripts/y.sh:3-5 range\n",
        )
        self.write(f"{v}/t-a01-local-review-bbbbbb2.md", "---\nfindings: 1\n---\n\n- [P3] scripts/x.sh:12 again\n")
        rows = "local:aaaaaa1:1\tquoting\nlocal:aaaaaa1:2\trange-case\nlocal:bbbbbb2:1\tenv-s-quoting\n"
        record = self.write(".orchestration/acceptance/t-a01.md", f"# record\n{rows}")
        head = "cccccc3" + "1" * 33
        current = "- [P2] `scripts/x.sh:12` once more\n- [P2] scripts/y.sh:3-5 again\n- [P2] scripts/y.sh:3-9 wider\n- [P2] scripts/z.sh:7 new\n"
        self.write(f"{v}/t-a01-local-review-cccccc3.md", f"---\nfindings: 4\n---\n\n{current}")
        self.run_tool("local-advisory.sh", "t-a01", head, owner)
        text = record.read_text()
        self.assertEqual(
            [
                "local:cccccc3:1\tenv-s-quoting",
                "local:cccccc3:2\trange-case",
                "local:cccccc3:3\tadvisory-p2",  # y.sh:3-9 is another token than y.sh:3-5
                "local:cccccc3:4\tadvisory-p2",
            ],
            re.findall(r"^local:cccccc3:\d\t.*$", text, re.MULTILINE),
        )
        findings = re.findall(r"^local-finding: cccccc3:(\d) .*$", text, re.MULTILINE)
        self.assertEqual(["1", "2", "3", "4"], findings)
        lines = [line for line in text.splitlines() if line.startswith("local-finding: cccccc3:")]
        self.assertIn("(- [P2] scripts/x.sh:12 once more; repeat of local:bbbbbb2:1)", lines[0])
        self.assertIn("(- [P2] scripts/y.sh:3-5 again; repeat of local:aaaaaa1:2)", lines[1])
        self.assertNotIn("repeat of", lines[2] + lines[3])
        # A review without findings needs no owner file and writes no heading.
        empty = "dddddd4" + "1" * 33
        self.write(f"{v}/t-b01-local-review-dddddd4.md", "---\nfindings: 0\n---\n")
        b = self.write(".orchestration/acceptance/t-b01.md", "# record\n")
        self.run_tool("local-advisory.sh", "t-b01", empty, "t-nobody-a01")
        self.assertEqual("# record\n", b.read_text())

    def test_sandbox_scan_prints_the_unsandboxed_mutation_calls(self):
        sandboxes = ".orchestration/sandboxes"
        hit = "| 2 | dangerouslyDisableSandbox: git commit -m wip |"
        self.write(
            f"{sandboxes}/t-a01.md", f"# sandbox\n{hit}\n- The unsandboxed table Counts every git commit > log.\n"
        )
        self.assertEqual(f"2:{hit}\n{SCAN_HIT}\n", self.run_tool("sandbox-scan.sh", "t-a01"))
        # A trailing -fixtures is stripped, and the match ignores case.
        self.write(f"{sandboxes}/t-b01.md", "Outside The Sandbox: GIT ADD x\n")
        self.assertEqual(
            f"1:Outside The Sandbox: GIT ADD x\n{SCAN_HIT}\n", self.run_tool("sandbox-scan.sh", "t-b01-fixtures")
        )
        reads = (
            "| 1 | gh pr view 9 > pr.json (outside the sandbox; reads) |\n| 2 | unsandboxed tee log, lists the PRs |\n"
        )
        self.write(f"{sandboxes}/t-c01.md", reads)
        none = f"sandbox scan: no unsandboxed mutation call in {sandboxes}/t-c01.md\n"
        self.assertEqual(none, self.run_tool("sandbox-scan.sh", "t-c01"))
        self.assertEqual("", self.run_tool("sandbox-scan.sh", "t-d01"))


if __name__ == "__main__":
    unittest.main()

 succeeded in 172ms:
   100	    step fetch 0 "${gh}" pr view "${pr}" --json headRefOid --jq .headRefOid
   101	    [ "${out}" = "${head}" ] || refuse 10 "head mismatch: re-run"
   102	    sha7=${head:0:7}
   103	    # The log is named by the head, so the lines before it are written once it is known; a new head's log holds them all.
   104	    [ "${log}" = "${v}/${task}-chain-${sha7}.log" ] || { log=${v}/${task}-chain-${sha7}.log && printf '%s\n' "${lines[@]}" >> "${log}"; }
   105	    [ ! -e "${v}/${task}-audit-${sha7}.md.last.md" ] || refuse 10 "head already audited: one chain per head"
   106	    step base 0,1 "${git}" -C "${review}" merge-base --is-ancestor origin/main HEAD
   107	    if ((rc == 0)); then
   108	        step checks any "${gh}" pr checks "${pr}" --required --watch
   109	        ((rc == 0)) || refuse 12 "required checks failed"
   110	        # Plan 020 step 4: the Bot wait is never gated, so it ends present or absent and the chain goes on.
   111	        q="[.[] | select(.user.login == \"chatgpt-codex-connector[bot]\" and .commit_id == \"${head}\")] | length"
   112	        t0=$("${date}" +%s)
   113	        while step bot 0 "${gh}" api "repos/{owner}/{repo}/pulls/${pr}/reviews" --paginate --jq "${q}"; do
   114	            n=$((${out//$'\n'/+})) # one count per page
   115	            ((n == 0 && $("${date}" +%s) - t0 < ${CHAIN_BOT_WAIT:-900})) || break
   116	            sleep 30
   117	        done
   118	        say "bot review: $( ((n > 0)) && echo present || echo absent)"
   119	        # origin/main can move during the waits (PR #372 thread 4291474885): a moved base is updated, then the fetch.
   120	        step base 0 "${git}" -C "${review}" fetch -q origin main
   121	        step base 0,1 "${git}" -C "${review}" merge-base --is-ancestor origin/main HEAD
   122	        ((rc == 1)) || break
   123	    fi
   124	    ((attempt < 3)) || refuse 13 "base moved three times"
   125	    step base 0 "${gh}" pr update-branch "${pr}"
   126	    t0=$("${date}" +%s) # GitHub builds the merge commit asynchronously: poll the head check's query until it moves.
   127	    while step base 0 "${gh}" pr view "${pr}" --json headRefOid --jq .headRefOid && [ "${out}" = "${head}" ]; do
   128	        (($("${date}" +%s) - t0 < ${CHAIN_POLL_MAX:-120})) || refuse 10 "update-branch head not visible"
   129	        sleep "${CHAIN_POLL_SECONDS:-5}"
   130	    done
   131	    fresh  # a moved base may have left the main checkout's main behind, which local-review.sh diffs against
   132	    log='' # the next head's log takes every line; this one ends here
   133	done
   134	# C-29: the scan reports and exits 0, so the chain is the stop its reader used to be.
   135	step sandbox-scan 0 "${main}/scripts/orchestrator/sandbox-scan.sh" "${task}"
   136	[ -z "${out}" ] || say "${out}"
   137	if [[ ${out} == *"sandbox scan: unsandboxed mutation calls above (C-29); judge before the audit"* ]]; then
   138	    [ "${CHAIN_SCAN_JUDGED:-}" = "${sha7}" ] || refuse 16 "sandbox scan hit: judge it, then re-run with CHAIN_SCAN_JUDGED=${sha7}"
   139	    say "sandbox scan: judged by the orchestrator"
   140	fi
   141	step local-review 0,3 "${main}/scripts/orchestrator/local-review.sh" "${task}" "${head}" "${pr}"
   142	findings=0
   143	[[ ! ${out} =~ local-review:\ ([0-9]+)\ findings ]] || findings=${BASH_REMATCH[1]}
   144	if ((rc == 3)); then
   145	    [ -f "${main}/.orchestration/tasks/${owner}.md" ] || refuse 15 "write the owner task ${owner} first"
   146	    step local-advisory 0,3 "${main}/scripts/orchestrator/local-advisory.sh" "${task}" "${head}" "${owner}"
   147	    ((rc == 0)) || refuse 11 "a P0/P1 local finding: the one round or the operator"
   148	fi
   149	sweep=${v}/${task}-pr-feedback.json comments=${v}/${task}-pr-comments.json
   150	step pr-feedback 0 "${uv}" run --no-project python -I "${main}/scripts/pr-feedback.py" "${pr}" --json "${sweep}"
   151	step fill-sweep 0 "${gh}" api user --jq .login
   152	login=${out}
   153	# One compact object per line, joined into one array, so a second page does not end the JSON after the first.
   154	step fill-sweep 0 "${gh}" api "repos/{owner}/{repo}/pulls/${pr}/comments" --paginate --jq '.[]'
   155	printf '[%s]\n' "${out//$'\n'/,}" > "${comments}"
   156	step fill-sweep 0,1 "${uv}" run --no-project python -I "${main}/scripts/orchestrator/fill_sweep.py" "${sweep}" "${comments}" ${extra:+"${extra}"} --orchestrator-login "${login}"
   157	rm -f -- "${comments}"
   158	gaps=unknown
   159	[[ ! ${out} =~ gaps\ ([0-9]+) ]] || gaps=${BASH_REMATCH[1]}
   160	((rc == 0)) || refuse 14 "sweep gaps: ${gaps}"
   161	now=$("${date}" -u +%FT%TZ)
   162	body="orchestrator integration review of PR #${pr} at ${head}: local review ${findings} finding(s), each with its line in the acceptance record; sweep complete"
   163	printf '[{"id": "%s", "scope": "review", "resolved": true, "author": "claude-code", "head": "%s", "pr": "%s", "reviewed_at": "%s", "body": "%s"}]\n' \
   164	    "${task}-pr${pr}-review-1" "${head}" "${pr}" "${now}" "${body}" > "${v}/${task}-crit.json"
   165	say "${now} receipt rc=0: printf > .orchestration/validation/${task}-crit.json"
   166	printf 'review_surface: crit-data\nreviewer: claude-code\nreview_source: %s\nreview_outcome: approved\nhead: %s\npr: %s\nreviewed_at: %s\nnote: %s\n' \
   167	    ".orchestration/validation/${task}-crit.json" "${head}" "${pr}" "${now}" \
   168	    "${body} (chain-integrate.sh; the task-level audit of this head is recorded separately in .orchestration/validation/${task}-audit-${sha7}.md)" \
   169	    > "${v}/${task}-review-receipt.md"
   170	say "${now} receipt rc=0: printf > .orchestration/validation/${task}-review-receipt.md"
   171	# The gate's LEDGER_ID: a thread id of ten or more digits or audit:<sha7>:<n>; local: rows stay in the prose.
   172	tsv=${v}/${task}-ledger-${sha7}.tsv
   173	step record 0,1 /usr/bin/grep -o -E $'^([0-9]{10,}|audit:[0-9a-f]{7}:[0-9]+)\t[a-z0-9-]+' "${record}"
   174	printf '%s\n' "${out}" > "${tsv}"
   175	step record 0 "${uv}" run --no-project python -I "${main}/scripts/orchestrator/acceptance-front-matter.py" "${task}" "${sweep}" "${review}" --ledger "${tsv}"
   176	rm -f -- "${tsv}"
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

 succeeded in 697ms:
[('scripts/check-regime-boundary.sh', 'Read-only regime boundary checker that reports untracked .orchestration files across worktrees, agmsg identity seat anomalies, lingering crit review servers, leftover Herdr worker workspaces, and bare'), ('scripts/check-regime-boundary.sh', 'Counts distinct agmsg identity names registered at a checkout path for one agent type via identities.sh.')]
graph stale; non-metadata changed files: 472

**Analyzing regex validation in file review**
**Reviewing duplicate records and symlink handling**
exec
/bin/zsh -lc "python3 -B -c 'import subprocess,hashlib,pathlib,json; h=\"d3e8acfe553791577576282eb0c339c018721bde\"; t=\"dotfiles-T128-chain-review-scripts-followup-a03\"; files={\"task\":\"tasks\",\"report\":\"reports\",\"validation\":\"validation\",\"sandbox\":\"sandboxes\"}; 
for stem,folder in files.items():
 b=subprocess.check_output([\"git\",\"show\",f\"{h}:.orchestration/{t}/{stem}.md\"]); l=pathlib.Path(f\".orchestration/{folder}/{t}.md\").read_bytes(); print(stem,\"copy-identical\",b==l,\"sha256\",hashlib.sha256(b).hexdigest())
print(\"CAPS\"); print(subprocess.check_output([\"git\",\"diff\",\"--numstat\",\"b167fe0a76a2e77d262f9f556c69ba6b9f118bbe\",h],text=True))
for rev in [\"f7847616\",\"b167fe0a76a2e77d262f9f556c69ba6b9f118bbe\"]:
 s=subprocess.check_output([\"git\",\"show\",f\"{rev}:scripts/orchestrator/local-advisory.sh\"],text=True); ts=subprocess.check_output([\"git\",\"show\",f\"{rev}:tests/unit/test_chain_review_scripts.py\"],text=True); print(\"premises\",rev,[sum(k in x for x in s.splitlines()) for k in [\"write the owner task\",\"git show origin/main\",\"advisory-p2\"]]+[sum(\"def test_\" in x for x in ts.splitlines())])
f=json.loads(pathlib.Path(f\".orchestration/validation/{t}-pr-feedback.json\").read_text()); print(\"feedback\",f[\"head_sha\"],len(f[\"checks\"]),len(f[\"items\"])); print(\"all checks success\",all(c[\"conclusion\"]==\"success\" for c in f[\"checks\"])); print(\"dispositions\",[(x[\"source\"],x.get(\"line\"),x[\"disposition\"]) for x in f[\"items\"]])'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc 'git show d3e8acfe553791577576282eb0c339c018721bde:scripts/orchestrator/local-advisory.sh | bash -n && git show d3e8acfe553791577576282eb0c339c018721bde:scripts/orchestrator/local-advisory.sh | shellcheck - && git diff --check b167fe0a76a2e77d262f9f556c69ba6b9f118bbe d3e8acfe553791577576282eb0c339c018721bde' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc "rg -n 'local-advisory\\.sh|local:.*advisory-p2|local:.*quoting|INV-2|INV-6' .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a03.md scripts/orchestrator/acceptance-front-matter.py scripts/require-crit-review.py && git show --format=fuller --no-patch 1e0c2e92 && git show --format=fuller --no-patch 9da0897a && rg -n 'task-level audit.*headless|task-level audit is|Audit' ~/.agents/skills/agmsg-orchestration/SKILL.md" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 202ms:
.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a03.md:10:  - scripts/orchestrator/local-advisory.sh
.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a03.md:15:  - control: the PR edits scripts/orchestrator/local-advisory.sh in two places, the refusal of an absent owner task file with the evidence that hashes the file (item 1a) and the class of a repeated finding (item 1b)
.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a03.md:42:    disposition: "residual: no workflow or interpreter file is in allowed_files; local-advisory.sh runs git rev-parse, grep, sed, cut, tr, head, sort and now shasum from PATH, as the lineage's scripts do; the tests' seam is the temporary repository as cwd; a PR checkout as cwd chooses nothing new, since the script already resolves the record and the review file from the repository root it runs in"
.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a03.md:44:  - claim: 'local-advisory.sh on origin/main writes an advisory row without checking that the owner task file exists'
.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a03.md:45:    command: 'git show origin/main:scripts/orchestrator/local-advisory.sh | /usr/bin/grep -c "write the owner task"'
.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a03.md:48:  - claim: 'local-advisory.sh on origin/main names git show origin/main as the row evidence, replayable only after the boundary'
.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a03.md:49:    command: 'git show origin/main:scripts/orchestrator/local-advisory.sh | /usr/bin/grep -c "git show origin/main"'
.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a03.md:52:  - claim: 'local-advisory.sh on origin/main gives every row the class advisory-p2'
.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a03.md:53:    command: 'git show origin/main:scripts/orchestrator/local-advisory.sh | /usr/bin/grep -c "advisory-p2"'
.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a03.md:62:# AGMSG-TASK dotfiles-T128-chain-review-scripts-followup-a03 — local-advisory.sh refuses an absent owner task, hashes the owner file as evidence, and classes a repeated finding by the record's earlier row (corrections C-51 (2) and C-50 (3); the chain-review-scripts lineage's next owner task; a Claude seat)
.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a03.md:76:After the merge, `local-advisory.sh` writes no row whose owner task file is absent, its evidence command hashes that file in the checkout it runs from, and a finding repeated from an earlier head of the task takes the class the record gave the earlier finding.
.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a03.md:80:1. `scripts/orchestrator/local-advisory.sh`: (a) after the script's existing exit 0 for a review without findings and before it writes the `## Owned by <owner>` heading, `.orchestration/tasks/<owner>.md` must exist in the repository root the script runs from, else it prints `write the owner task <owner> first` and exits 2 as well (the missing review file keeps its exit 2; the two messages tell them apart and the `@exitcode 2` line names both), so a refused run leaves the record untouched and a review without findings needs no owner file; the `evidence=` tail of each `local-finding:` line becomes `shasum -a 256 .orchestration/tasks/<owner>.md` with the file's sha256 at the time of writing appended as `(<sha256>)`, so the line replays in the orchestrator's checkout before the boundary; (b) each finding's token, the first run of path characters, `:` and digits with an optional `-<digits>` range in the finding's line (backticks around it ignored, so `` `a.sh:1` `` and `resolve-threads.sh:48-52` both count), is compared with the findings of the task's earlier local review files (`.orchestration/validation/<task>-local-review-*.md` other than the current head's), each numbered as this script's own loop numbers them (`sort -u` order, P0 and P1 lines included); when an earlier finding has the same token and the record holds a row `local:<sha7'>:<n'><TAB><class>` for it with a class other than `advisory-p2`, the new row takes that class, the latest matching head's row winning when two earlier files match with different classes, and its `local-finding:` line's parenthesis gains `repeat of local:<sha7'>:<n'>` so the provenance is on the line; otherwise `advisory-p2`, as today. The scope is the local review files and the `local:` rows only: a repeat first classed by a Bot thread's row or an `audit:` row keeps `advisory-p2`, since those rows carry no `path:line` token (C-50's wider sentence is applied here to the one source that has tokens). Nothing else changes (the P0/P1 stop, the heading, the once-only writes).
.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a03.md:89:`uv run python -m unittest tests/unit/test_chain_review_scripts.py -v` green (the module's tests and the two new ones), pasted in the validation file with `shellcheck scripts/orchestrator/local-advisory.sh` and `git diff --numstat origin/main...HEAD`: at most 200 changed lines (added plus deleted) outside `tests/` and outside `.orchestration/` (plan 021 step 7.2) and 1000 added lines under `tests/` (INV-2).
.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a03.md:93:One PR from a fresh branch off `origin/main` (after PR #376, the a02 owner task's PR, merged as f7847616 on 2026-10-17). The PR is ready for the orchestrator's integration when the ruleset's required checks are green, the Bot's review of the final head is in (at PR open, and once more on `@codex review` after a P0/P1 fix round: plan 020 step 2), every Bot thread is replied to and resolved by the orchestrator with its disposition, the validation file carries the outputs above, and the RESULT names every P0/P1 thread with `fixed:<sha>` and every P2 thread with the disposition the worker proposes; the orchestrator's audit of the final head is dispositioned finding by finding before the gate, and a P0/P1 it leaves is the operator's decision. The Bot's P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P0 or P1 that survives the round is listed as `open:<thread id>` with `bot_rounds=2` (the Bot's review at PR open and its re-review after the fix round), stops the PR and goes to the operator as a decision; a P2 on this PR's own change whose fix stays within `allowed_files` and is small (one flag or a few lines plus one test) is fixed in a revise round the orchestrator sends with a `check=` while INV-6's counts allow it (C-50); any other P2 is advisory, owned by `dotfiles-T128-chain-review-scripts-followup-a04`, which the orchestrator writes when the first advisory P2 appears, before the PR's dispositions (C-51), and recorded under `## Owned by dotfiles-T128-chain-review-scripts-followup-a04` in this task's acceptance record. The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`. The RESULT names head, base, branch, files, every Bot thread with its disposition, the test names per row, the caps, `task_copy=<sha256 of .orchestration/dotfiles-T128-chain-review-scripts-followup-a03/task.md>` and the evidence paths.
commit 1e0c2e9291ce75ae11156a916cc872f0b6db0e7a
Author:     Fumio Moriya <moriya.fumio@technopro.com>
AuthorDate: Sat Oct 17 10:02:15 2026 +0900
Commit:     Fumio Moriya <moriya.fumio@technopro.com>
CommitDate: Sat Oct 17 10:02:15 2026 +0900

    docs(orchestration): chain-review-scripts followup a03 evidence update (the Bot's clean review, CI's ShellCheck fix 9da0897a)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
commit 9da0897a6d8571c383a32e7bd1278103450d9a4f
Author:     Fumio Moriya <moriya.fumio@technopro.com>
AuthorDate: Sat Oct 17 10:01:41 2026 +0900
Commit:     Fumio Moriya <moriya.fumio@technopro.com>
CommitDate: Sat Oct 17 10:01:41 2026 +0900

    fix(orchestrator): local-advisory.sh numbers each earlier finding with an if, not A && B || C (CI ShellCheck SC2015)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
92:  - Audit findings are input, never approval; acceptance authority stays with the orchestrator, and each RESULT gets its own acceptance record.
170:       - A P2 finding of the Codex Bot, local review or task-level audit is advisory: disposition it `not-applicable:advisory P2 owned by <lineage>-followup-a0<n>` and record an `<id><TAB><class>` row under `## Owned by <owner>` in the lineage's acceptance record, with the orchestrator writing the owner task file before the row.
173:    2. Run the task-level audit of that head in the pair or headless form of the task-level audit bullet. It exits nonzero for every verdict other than `correct`. An exit with `Audit verdict: incorrect` is not a failed step: continue to step 3 and disposition its findings. A `blocked` or missing verdict means re-running the audit.

 exited 2 in 216ms:
.orchestration/dotfiles-T128-chain-review-scripts-followup-a03/task.md:106: new blank line at EOF.

 succeeded in 363ms:
task copy-identical True sha256 e328a3fb8036d4b29b1ed798f42a967d66204bde810b62b84dd7048715c79ee2
report copy-identical True sha256 dc6b79661201fdb983b05c8a757391d5869610f9f3f4c04dece2faaab142dfd8
validation copy-identical True sha256 dcb312933c7e19df2ef20a522050f0216eaa7022ef479371360b02cd2cff8e9f
sandbox copy-identical True sha256 6fcb6f2994874a2faa9450172ee815edb032ed7fae90c30ba30ecfd07fc45180
CAPS
3	0	.orchestration/dotfiles-T128-chain-review-scripts-followup-a03/autoskill.md
7	0	.orchestration/dotfiles-T128-chain-review-scripts-followup-a03/learning.md
75	0	.orchestration/dotfiles-T128-chain-review-scripts-followup-a03/report.md
27	0	.orchestration/dotfiles-T128-chain-review-scripts-followup-a03/sandbox.md
106	0	.orchestration/dotfiles-T128-chain-review-scripts-followup-a03/task.md
228	0	.orchestration/dotfiles-T128-chain-review-scripts-followup-a03/validation.md
38	5	scripts/orchestrator/local-advisory.sh
60	2	tests/unit/test_chain_review_scripts.py

premises f7847616 [0, 1, 2, 14]
premises b167fe0a76a2e77d262f9f556c69ba6b9f118bbe [0, 1, 2, 14]
feedback d3e8acfe553791577576282eb0c339c018721bde 12 8
all checks success True
dispositions [('issue_comment', None, 'not-applicable:bot summary or onboarding comment, no finding; evidence=jq --argjson u \'"https://github.com/mryfmo/dotfiles/pull/381#issuecomment-6227560372"\' \'.items[] | select(.url == $u)\' .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a03-pr-feedback.json'), ('issue_comment', None, 'not-applicable:bot summary or onboarding comment, no finding; evidence=jq --argjson u \'"https://github.com/mryfmo/dotfiles/pull/381#issuecomment-6227560380"\' \'.items[] | select(.url == $u)\' .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a03-pr-feedback.json'), ('issue_comment', None, 'not-applicable:bot summary or onboarding comment, no finding; evidence=jq --argjson u \'"https://github.com/mryfmo/dotfiles/pull/381#issuecomment-6227663819"\' \'.items[] | select(.url == $u)\' .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a03-pr-feedback.json'), ('issue_comment', None, 'not-applicable:bot summary or onboarding comment, no finding; evidence=jq --argjson u \'"https://github.com/mryfmo/dotfiles/pull/381#issuecomment-6227679116"\' \'.items[] | select(.url == $u)\' .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a03-pr-feedback.json'), ('annotation', 1, 'not-applicable:runner capacity notice, no finding; evidence=jq --argjson u \'"https://github.com/mryfmo/dotfiles/actions/runs/38998621128/job/117296597380"\' \'.items[] | select(.url == $u)\' .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a03-pr-feedback.json'), ('annotation', 1, 'not-applicable:runner capacity notice, no finding; evidence=jq --argjson u \'"https://github.com/mryfmo/dotfiles/actions/runs/38998621146/job/117296597250"\' \'.items[] | select(.url == $u)\' .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a03-pr-feedback.json'), ('annotation', 1, 'not-applicable:runner capacity notice, no finding; evidence=jq --argjson u \'"https://github.com/mryfmo/dotfiles/actions/runs/38998621128/job/117296597094"\' \'.items[] | select(.url == $u)\' .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a03-pr-feedback.json'), ('status', None, 'not-applicable:CI status, no finding; evidence=jq --argjson s \'"status"\' --argjson c \'"CodeRabbit"\' \'.items[] | select(.source == $s and .check == $c)\' .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a03-pr-feedback.json')]

**Reviewing skill task bullets**
exec
/bin/zsh -lc "sed -n '62,112p' ~/.agents/skills/agmsg-orchestration/SKILL.md" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc "git grep -n -E 'local-advisory\\.sh|local-review-\\*' d3e8acfe553791577576282eb0c339c018721bde -- scripts tests home/dot_config/claude/rules && git show d3e8acfe553791577576282eb0c339c018721bde:scripts/orchestrator/acceptance-front-matter.py | sed -n '1,160p'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 11ms:
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

 succeeded in 70ms:
d3e8acfe553791577576282eb0c339c018721bde:scripts/orchestrator/chain-integrate.sh:73:for s in scripts/orchestrator/{sandbox-scan.sh,local-review.sh,local-advisory.sh,fill_sweep.py,acceptance-front-matter.py,orch-audit.sh} scripts/pr-feedback.py; do
d3e8acfe553791577576282eb0c339c018721bde:scripts/orchestrator/chain-integrate.sh:146:    step local-advisory 0,3 "${main}/scripts/orchestrator/local-advisory.sh" "${task}" "${head}" "${owner}"
d3e8acfe553791577576282eb0c339c018721bde:scripts/orchestrator/local-advisory.sh:2:# @file local-advisory.sh
d3e8acfe553791577576282eb0c339c018721bde:scripts/orchestrator/local-advisory.sh:22:#   scripts/orchestrator/local-advisory.sh dotfiles-T128-x-a01 "$head" dotfiles-T128-x-followup-a01
d3e8acfe553791577576282eb0c339c018721bde:scripts/orchestrator/local-advisory.sh:29:    echo "usage: local-advisory.sh <task> <40-hex head> <owner task>"
d3e8acfe553791577576282eb0c339c018721bde:scripts/orchestrator/local-advisory.sh:57:for f in .orchestration/validation/"$task"-local-review-*.md; do
d3e8acfe553791577576282eb0c339c018721bde:scripts/orchestrator/pr-cost.sh:49:local_n=$({ /usr/bin/grep -l -E "^pr: ${pr}\$" .orchestration/validation/*local-review-*.md 2> /dev/null || true; } |
d3e8acfe553791577576282eb0c339c018721bde:tests/fixtures/regime/invariants.md:9:- Before every acceptance action (revise, accept, merge) the orchestrator runs `scripts/regime-counters.sh <task id>` and pastes its output into the acceptance record. S2 is decided from INV-6's counts: each component the script prints is read from its output, and for each component it prints as `unknown` the record pastes the command and output that read the source INV-6 names for that component, or, while that source has no entry for the task, says so and pastes the reading of the interim record the orchestrator used in its place. S1 (plan 006: the same finding class three times on one artifact, from any reviewer) is decided from the record's finding-class table, which gives a class to every finding the PR-feedback sweep lists, whatever its disposition, and to every task-level audit finding; three rows of one class stop the artifact. Read that table over non-advisory rows only: list advisory P2 rows with their classes (`advisory-p2` and the `local:<sha7>:<n>` rows `local-advisory.sh` writes), exclude them from S1's three-rows count, and name the excluded rows in the record. The gate's S6 check still sees every ledger row, so an advisory class at three rows gets its `searches` entry from `acceptance-front-matter.py` like any other. INV-6's message and head counts and the S2 lines (`revises`, `amendments`, `questions`, `bot_p1_heads`) take no ledger rows; `scripts/regime-counters.sh` prints them unchanged.
d3e8acfe553791577576282eb0c339c018721bde:tests/unit/test_chain_glue.py:62:    "orchestrator/local-advisory.sh": "local-advisory",
d3e8acfe553791577576282eb0c339c018721bde:tests/unit/test_chain_review_scripts.py:257:                self.assertIn("usage:", self.run_tool("local-advisory.sh", task, commit, "t-followup-a01", code=2))
d3e8acfe553791577576282eb0c339c018721bde:tests/unit/test_chain_review_scripts.py:375:            stdout = self.run_tool("local-advisory.sh", "t-a01", head, owner)
d3e8acfe553791577576282eb0c339c018721bde:tests/unit/test_chain_review_scripts.py:385:        stdout = self.run_tool("local-advisory.sh", "t-a01", head, owner, code=3)
d3e8acfe553791577576282eb0c339c018721bde:tests/unit/test_chain_review_scripts.py:391:        stdout = self.run_tool("local-advisory.sh", "t-a01", head, owner, code=3)
d3e8acfe553791577576282eb0c339c018721bde:tests/unit/test_chain_review_scripts.py:397:            "local review of abcdef0: no findings\n", self.run_tool("local-advisory.sh", "t-a01", head, owner)
d3e8acfe553791577576282eb0c339c018721bde:tests/unit/test_chain_review_scripts.py:400:        self.assertIn("no local review file", self.run_tool("local-advisory.sh", "t-b01", head, owner, code=2))
d3e8acfe553791577576282eb0c339c018721bde:tests/unit/test_chain_review_scripts.py:408:                self.assertIn("usage:", self.run_tool("local-advisory.sh", "t-a01", head, owner, code=2))
d3e8acfe553791577576282eb0c339c018721bde:tests/unit/test_chain_review_scripts.py:419:        self.run_tool("local-advisory.sh", "t-a01", head, "t.followup-a01")
d3e8acfe553791577576282eb0c339c018721bde:tests/unit/test_chain_review_scripts.py:421:        self.run_tool("local-advisory.sh", "t-a01", head, "t.followup-a01")
d3e8acfe553791577576282eb0c339c018721bde:tests/unit/test_chain_review_scripts.py:431:            f"write the owner task {owner} first", self.run_tool("local-advisory.sh", "t-a01", head, owner, code=2)
d3e8acfe553791577576282eb0c339c018721bde:tests/unit/test_chain_review_scripts.py:435:        self.run_tool("local-advisory.sh", "t-a01", head, owner)
d3e8acfe553791577576282eb0c339c018721bde:tests/unit/test_chain_review_scripts.py:455:        self.run_tool("local-advisory.sh", "t-a01", head, owner)
d3e8acfe553791577576282eb0c339c018721bde:tests/unit/test_chain_review_scripts.py:476:        self.run_tool("local-advisory.sh", "t-b01", empty, "t-nobody-a01")
"""acceptance-front-matter.py <task> <sweep-json> <pr-worktree> [--ledger <tsv>] [--audit-dispositions <tsv>]

Write or update the JSON block of `.orchestration/acceptance/<task>.md` in this checkout (plan 007 T718, a05 item 1;
plan 013 A′, C-24, C-26): the object between the record's first two `---` lines that the gate reads. `head` is
`git -C <pr-worktree> rev-parse HEAD` and must equal the sweep JSON's `head_sha`; `pr` is the sweep JSON's own `pr`.
`ledger` keeps every row the record has and adds each `--ledger` row (`id<TAB>class`) whose id is new; a row whose
id is present is printed as kept-ledger-row. `searches` is recomputed by the gate's rule: each class with three or
more rows, with the sorted basenames of the mistake records naming it. `audit_findings` come from
`--audit-dispositions` (`n<TAB>reason<TAB>evidence`), required when the audit summary orch-audit.sh writes beside
its receipt (`.orchestration/validation/<task>-audit-<sha7>.md.last.md`) ends in `Verdict: incorrect`, refused
otherwise; the record is written before the audit (the audit reads it) and again after an incorrect one. A record
that starts with a `---` block is read with the gate module's reader (duplicate keys refused) and keeps its text
after the block and its `dispatch` list; a prose record gets the block prepended. The gate module's field checks
run on the new block, and any refusal exits 1 before anything is written.
"""

import argparse
import collections
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path


def refuse(message):
    sys.exit(f"acceptance-front-matter: {message}; nothing written")


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout.strip()


def rows(path, width):
    """The `width`-field rows of a TSV file, blank and `#` lines skipped."""
    lines = Path(path).read_text().splitlines() if path else []
    found = [line.split("\t") for line in lines if line.strip() and not line.startswith("#")]
    for fields in found:
        if len(fields) != width:
            refuse(f"{path}: a row needs {width} tab-separated fields: {fields!r}")
    return found


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


if __name__ == "__main__":
    main()

**Analyzing design limitations and task scope**
**Reviewing ledger ownership and task boundaries**
web search: 
exec
/bin/zsh -lc "rg -n 'C-50|M-20261015-02|local:|LEDGER_ID|three.rows|S6' .orchestration/learning/mistakes scripts/require-crit-review.py .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a04.md" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc "git show d3e8acfe553791577576282eb0c339c018721bde:scripts/orchestrator/local-review.sh | nl -ba | sed -n '1,85p;150,215p' && git show d3e8acfe553791577576282eb0c339c018721bde:.github/workflows/test.yaml | rg -n -C 3 'unit|ShellCheck|unittest'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 exited 2 in 25ms:
rg: .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a04.md: No such file or directory (os error 2)
scripts/require-crit-review.py:36:LEDGER_ID = re.compile(r"\d{10,}|audit:[0-9a-f]{7}:\d+")
scripts/require-crit-review.py:45:S6_CLASS_LIMIT = 3
scripts/require-crit-review.py:803:                or not LEDGER_ID.fullmatch(str(row["id"]))
scripts/require-crit-review.py:921:        errors.append(f"S6: ledger lacks {', '.join(sorted(missing))}")
scripts/require-crit-review.py:925:        if count < S6_CLASS_LIMIT:
scripts/require-crit-review.py:929:            errors.append(f"S6: class {cls} at {count}: {found}")
scripts/require-crit-review.py:931:            errors.append(f"S6: class {cls} at {count} without a matching records search")
scripts/require-crit-review.py:936:    """Recompute S6's records search with pathlib: the files with a `classes:` line naming the class.
.orchestration/learning/mistakes/M-20261012-1.md:17:- **Should have been:** a class row per finding at disposition in the current acceptance record; three rows of one class stop the artifact; the worker's early stop over the Codex Bot's badged findings
.orchestration/learning/mistakes/M-20261012-33.md:16:- **Detection and why not earlier:** (1) nothing adversarial reads the code before the push: the pair reviews the task text, the worker's tests pin the behaviours the text names, the audit comes after the Bot; the GitHub Bot is the first reviewer of the code and it runs on every head, update-branch merges included, sampling new findings each time; (2) the S6 search keys on `classes:` slugs and M-21's defect lived in its prose; (3) the worker applied the capped-read lesson to the input the task text named (`history.sh`: bus-read.sh refuses a read at its limit) and not to the second default-limited input the script reads (`memory search`); (4) bus-read.sh re-derived the task-closing rule the stop gate owns, with a smaller status set and without the peer binding; both bus-read threads say the threat row was closed by a happy-path test.
.orchestration/learning/mistakes/M-20261012-33.md:18:- **Should have been:** (a) a head is reviewed locally with the Bot's engine (`codex review --base main`, review profile, read-only) before the audit, and moves on only when a local round adds nothing; (b) one definition of "task closed" (the stop gate's), consumed by bus-read.sh and never re-derived; (c) the S6 search reads the record bodies as well as `classes:`, and three-repeat.sh does the same; a count printed from a default-limited read states the cap or raises it; (d) no boundary while an open PR is between its final update-branch and its merge.
.orchestration/learning/mistakes/M-20261015-02.md:2:id: M-20261015-02
.orchestration/learning/mistakes/M-20261015-02.md:3:artifact: "PR #365 (dotfiles-T128-task-checkers-followup-a01): one P2 defect (orch-audit.sh runs the ledger check as python without -I, so an untracked module beside it would be imported before the read-only audit) raised by the Bot (thread 4279174373 on 4cc9d206), the local review (local:b84e81f:1) and the task-level audit (audit:b84e81f:1), the policy reading of its disposition raised by the audits of PR #364 (c45f9b5:2) and PR #365 (b84e81f:2)"
.orchestration/learning/mistakes/M-20261015-02.md:8:corrections: [C-50]
.orchestration/learning/mistakes/M-20261015-02.md:13:# M-20261015-02
.orchestration/learning/mistakes/M-20261015-02.md:19:- **Corrections:** C-50.
.orchestration/learning/mistakes/M-20261015-06.md:15:- **Evidence:** the record's round lines: round 1 revise (two P1, one P2, three P3; Codex P1, P2), round 2 revise (the orchestrator's own C2 failure, M-20261015-04; a P2 on the gate's S6 check), Codex round 3 revise (the advisory-row exclusion missing; one closing test for six items), Codex round 4 revise (a count of new tests left at two), round 5 confirm with two P3 taken as fixes, Codex round 6 revise (the one-selector shape), round 7 confirm, Codex round 7 revise (a sentence claiming every sentence pinned), Codex round 8 confirm; each round a distinct defect of the text, none a repeat of a class, so the three-repeat rule never fired.
.orchestration/learning/mistakes/M-20261012-28.md:15:- **Evidence:** thread 4254092805: "The S6 check counts only rows supplied by the acceptance record and never verifies that the ledger includes every item from `PR_FEEDBACK_EVIDENCE` or every audit finding. An acceptance record with `ledger: []`, or one that omits enough occurrences of a repeated class to keep its count below three, therefore passes". The a03 contract (amended) defines `ledger` rows as `{id, class}` with the id's shape, and `searches` for classes at three, and says nothing about which ids must be present. Counters at 02:32Z: `tasks=2 amendments=1 questions=1 results=1 revises=0`: a second amendment is INV-6's reset.
.orchestration/learning/mistakes/M-20261012-19.md:7:count_at_detection: "3 on the T703 lineage (4248319926 on 375bae0f: the classes: data absent from the PR tree; 4248711363: the gate's S6 refusal not in the tree; 4248711371: task-consistency-check C4 not in the tree); item 6's ACCEPTANCE_EVIDENCE sentence is a fourth candidate"
.orchestration/learning/mistakes/M-20261016-01.md:7:count_at_detection: "predicate-shape-overmatch: four findings on one artifact (any-part basename, first-part basename with a chained command, basename of a single token under another path, any prefix before .claude/hooks; the peer's interpreter-basename token); the record's rows carried three different class slugs, so S6 saw none"
.orchestration/learning/mistakes/M-20261016-01.md:16:- **Detection and why not earlier:** each finding was dispositioned with its own slug (`chain-after-managed-program`, `basename-collision`, `prefix-over-match`), so the ledger never reached three rows of one class and S6's search never ran; each amendment answered the finding's example with a narrower shape (exact cardinality, then a path pattern) and the next review found the next shape.
.orchestration/learning/mistakes/M-20261016-01.md:18:- **Should have been:** at the first over-match finding, replace the shape with the identity (string equality with the rendered managed values) instead of narrowing the shape; class every over-match finding with one slug so the third triggers S6; and, since the managed template never rendered an interpreter form, admit no form the template never produced.
.orchestration/learning/mistakes/M-20261012-26.md:20:- **Third instance, 01:3xZ:** the round-3 Codex prompt was derived with `sed` from the round-2 prompt file, itself rendered while the hash file was missing, so it carried `sha256 ; verify`; the hash pattern matched nothing, `grep -c` printed 0, and the chain stopped (no run). Plan 007 S6 at three: the records search (`/usr/bin/grep -rl 'classes:.*hand-typed-chain' .orchestration/learning/mistakes/` → M-20261012-11, -18, -25, -26) names C-13 and C-14, whose mechanism is `codex-review.sh`; written in the scratchpad before the next run (`codex-review.sh <profile> <reviewed-file> <template> <receipt> <transcript>`: computes the hash, renders `@@SHA@@`, refuses a prompt without it, closes stdin) and used from then on until T718 a02 lands it.
.orchestration/learning/mistakes/M-20261014-07.md:15:- **Evidence:** the record line says "the owned rows under `## Owned by dotfiles-T128-playbook-rules-followup-a01` in the a04 record on `origin/main`: 9 (local 9)"; the section holds four `<id>\t<class>` rows (`local:65a3d71:1`, `audit:71eb920:1`, `audit:65a3d71:1`, `audit:65a3d71:2`) and five prose lines (a `local-finding:` line, an audit summary line, two `audit-finding:` lines, the heading's own subtitle). The figure was pasted command output, as run-not-recall requires, but the command (`awk '/^## Owned by/{p=1;next} p&&/^## /{exit} p&&NF'`) counted every non-empty line of the section, not rows.
.orchestration/learning/mistakes/M-20261012-20.md:16:- **Root cause:** the task specified the S6 check as a scan of pasted free text ("names the class slug and both commands"), so the worker built a hand-written parser at a trust boundary and each round tightened it against the previous bypass; the design calls that a conformance finding (INV-12 enforcement row: no new hand-written parser at a trust boundary). The pasted command text was never the evidence; the record set the search found is.

 succeeded in 81ms:
     1	#!/usr/bin/env bash
     2	# @file local-review.sh
     3	# @brief Review a PR head's diff against main locally with the Bot's engine, once per head, before the audit (C-32).
     4	# @description
     5	#   Run outside the Bash sandbox: inside it codex exits 1 ("failed to initialize in-process app-server client:
     6	#   Operation not permitted"). An existing `.orchestration/validation/<task>-local-review-<sha7>.md` whose `head:` is
     7	#   this head is reused and re-reported; one that records another head is refused. Otherwise the clean review
     8	#   worktree (`$ORCH_REVIEW_WORKTREE`, else `.claude/worktrees/orchestrator-review`), a path with its own `.git`
     9	#   entry, is checked out detached at the head and left there, and the review binary runs in it as `--profile review
    10	#   -s read-only review --base main`. The binary is `$CODEX_BIN`, else codex as `mise which` answers it under `env
    11	#   -i` in the root, else `command -v`; it is resolved before the checkout, and a path under a `shims` directory is
    12	#   refused. When its first line is an env shebang (`#!/usr/bin/env NAME` or `env -S NAME ARG…`), NAME is resolved the
    13	#   same way and runs with the `-S` form's ARG words, then the binary, so no interpreter comes from PATH in the PR
    14	#   worktree. A `-S` string holding a quote, a backslash, a `$` or a word starting with `#` is refused, since env -S
    15	#   splits those differently. When the
    16	#   binary fails, no file is written. Otherwise the file gets the front matter, the unique `-
    17	#   [P0-3]` findings of the transcript's final message, and that message with the worktree prefix stripped; the
    18	#   findings are printed, then `local-review: <n> findings (<file>)`.
    19	# @arg $1 string Task id, letters, digits, `.`, `_` and `-`.
    20	# @arg $2 string The PR head commit, a local one, 40 hex characters.
    21	# @arg $3 int PR number.
    22	# @exitcode 0 No finding.
    23	# @exitcode 2 A precondition failed: a malformed task id or head, a review file of another head, the head is not a
    24	#   local commit, the review worktree is not a worktree root or not clean, no review binary outside a shims
    25	#   directory, or an env -S shebang the script does not split.
    26	# @exitcode 3 One or more findings.
    27	# @exitcode 4 The review binary failed; no file is written, and its transcript stays in `$TMPDIR`.
    28	# @example
    29	#   scripts/orchestrator/local-review.sh dotfiles-T128-x-a01 "$(git rev-parse FETCH_HEAD)" 356
    30	set -euo pipefail
    31	task=$1 head=$2 pr=$3
    32	# Both name the review file, so a / in either would write outside the validation directory (the audit of b6ce4ff).
    33	[[ $task =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ && $head =~ ^[0-9a-f]{40}$ ]] || {
    34	    echo "local-review: usage: local-review.sh <task> <40-hex head> <pr>"
    35	    exit 2
    36	}
    37	R="$(git rev-parse --show-toplevel)"
    38	cd -- "$R"
    39	W=${ORCH_REVIEW_WORKTREE:-$R/.claude/worktrees/orchestrator-review}
    40	out=$R/.orchestration/validation/$task-local-review-${head:0:7}.md
    41	if [ -s "$out" ]; then
    42	    # one sample per head (C-32): a review of this head exists; reuse it instead of sampling again. The name keeps
    43	    # seven characters of the head, so the recorded head must be this one (PR #357 thread 4270918140).
    44	    [ "$(sed -n 's/^head: //p' "$out" | head -1)" = "$head" ] || {
    45	        echo "local-review: $out records another head; not reused"
    46	        exit 2
    47	    }
    48	    findings=$(/usr/bin/grep -E '^- \[P[0-3]\]' "$out" | sort -u || true)
    49	    n=$(sed -n 's/^findings: //p' "$out" | head -1)
    50	    printf '%s\n' "$findings"
    51	    echo "local-review: $n findings (existing $out)"
    52	    [ "${n:-0}" = 0 ] || exit 3
    53	    exit 0
    54	fi
    55	git -C "$R" cat-file -e "$head^{commit}" 2> /dev/null || {
    56	    echo "local-review: $head is not a local commit (fetch pull/$pr/head first)"
    57	    exit 2
    58	}
    59	# Without its own .git entry, git -C would act on an enclosing checkout and move that one to the head.
    60	[ -e "$W/.git" ] || {
    61	    echo "local-review: $W is not a worktree root"
    62	    exit 2
    63	}
    64	[ -z "$(git -C "$W" status --porcelain)" ] || {
    65	    echo "local-review: $W is not clean"
    66	    exit 2
    67	}
    68	# Resolved in the root before the checkout and run by its absolute path, so no relative PATH entry (./bin) picks a
    69	# binary from the PR head. A mise shim would pick its binary from the PR worktree it runs in, so a name comes from
    70	# mise which under env -i, as orch-gate.sh resolves gh, and a shims path is refused (the audit of b6ce4ff). Sets
    71	# found; a refusal exits here, before the checkout.
    72	resolve() { # <name> <what> [<found by command -v alone>]
    73	    if [ -n "${3:-}" ]; then
    74	        found=$(command -v "$1") || found=
    75	    else
    76	        found=$(env -i PATH="$PATH" HOME="$HOME" mise which "$1" 2> /dev/null || command -v "$1") || found=
    77	    fi
    78	    [ -n "$found" ] || {
    79	        echo "local-review: no $2 $1"
    80	        exit 2
    81	    }
    82	    [[ $found == /* ]] || found=$R/$found
    83	    [[ $found != */shims/* ]] || {
    84	        echo "local-review: the $2 $found is under a shims directory; refused"
    85	        exit 2
55-          fetch-depth: 0
56-          persist-credentials: false
57-
58:      - name: Decide whether the diff needs the unit tests
59-        id: decide
60-        env:
61-          EVENT_NAME: ${{ github.event_name }}
--
85-          # `.github/workflows/`, `home/`, `install/`, and `tests/` in an env-
86-          # var-like form to make the rule reusable. For this workflow, keeping
87-          # the pattern inline is still easier to read because the rule is only
88:          # used once and only decides whether the expensive unit-test steps
89-          # should run. It does not decide whether the required workflow itself
90-          # reports a status. If more workflows need the same rule later,
91-          # extract a shared script instead of hiding the pattern in env.
--
105-            echo "should_test=false" >> "${GITHUB_OUTPUT}"
106-          fi
107-
108:      - name: Skip full unit test run for unrelated changes
109-        if: ${{ steps.decide.outputs.should_test != 'true' }}
110-        run: |
111:          echo "No unit-test-relevant files changed."
112-          echo "Compared diff range: ${{ steps.decide.outputs.diff_range }}"
113-
114-      - name: Install tools
--
304-          mise -C "${RUNNER_TEMP}/statusline-mise" x node npm:prettier -- \
305-            sh -c 'cd "${GITHUB_WORKSPACE}" && git ls-files -z "*.md" | xargs -0 prettier --check'
306-
307:      - name: Run `ShellCheck`
308-        if: ${{ steps.decide.outputs.should_test == 'true' }}
309-        run: |
310-          git ls-files -z 'setup.sh' 'install/*.sh' 'install/**/*.sh' 'scripts/*.sh' | xargs -0 shellcheck -x
--
315-        with:
316-          enable-cache: false
317-
318:      - name: Run Python unit tests
319-        if: ${{ steps.decide.outputs.should_test == 'true' }}
320-        run: |
321-          if [[ "${OS}" == ubuntu-* ]]; then
--
325-            command -v zsh > /dev/null 2>&1 || brew install zsh
326-          fi
327-
328:          make unit-test
329-
330-      - name: Prepare public dotfiles fixture
331-        if: ${{ steps.decide.outputs.should_test == 'true' }}
--
367-            printf 'FILES_TEST_CONFIG=%s\n' "${files_test_config}"
368-          } >> "${GITHUB_ENV}"
369-
370:      - name: Run unit test
371-        if: ${{ steps.decide.outputs.should_test == 'true' }}
372-        run: |
373-          if [ "${OS}" == "macos-14" ]; then
--
376-            # the test matrix for platform validation, but collect Codecov
377-            # reports from the Ubuntu jobs where bashcov parses Bats output
378-            # reliably.
379:            ./scripts/run_unit_test.sh
380-            exit 0
381-          fi
382-
--
387-
388-          # Use a unique command name per matrix job so SimpleCov keeps each
389-          # session separated before Codecov merges by flag/name.
390:          BASHCOV_COMMAND_NAME="unit-test-${OS}-${SYSTEM}" \
391:            ruby ./scripts/run_bashcov_unit_test.rb "${bashcov_args[@]}" -- ./scripts/run_unit_test.sh
392-
393-      - name: Setup for Codecov
394-        if: ${{ steps.decide.outputs.should_test == 'true' && matrix.os == 'ubuntu-24.04' && !endsWith(github.actor, '[bot]') }}

web search: https://github.com/mryfmo/dotfiles/pull/381
**Reviewing task invariant and acceptance findings**
**Analyzing orchestration audit and bot activity**
codex
反復 class の引き継ぎ先に問題を見つけました。`local:` 行は統合スクリプトで ledger から除外され、gate もその ID を受け付けないため、class を揃えても S6 の「同じ class が3件」の検査には届きません。過去のレビュー名を正規表現に渡す処理も、読み取り専用の再現で確認します。
exec
/bin/zsh -lc "python3 -B -c 'import subprocess; h=\"d3e8acfe553791577576282eb0c339c018721bde\"; s=subprocess.check_output([\"git\",\"show\",f\"{h}:scripts/orchestrator/local-advisory.sh\"],text=True).splitlines(); token=s[54]; loop=\"\\n\".join(s[75:83]); q=lambda x: chr(39)+x.replace(chr(39),chr(39)+chr(34)+chr(39)+chr(34)+chr(39))+chr(39); 
for label,earlier,record in [(\"valid\", \"scripts/x.sh:12 local:aaaaaa1:1\\nscripts/x.sh:12 local:bbbbbb2:1\\n\", \"local:aaaaaa1:1\\tquoting\\nlocal:bbbbbb2:1\\tenv-s-quoting\\n\"),(\"invalid review suffix .* matches an unrelated class row\", \"scripts/x.sh:12 local:.*:1\\n\", \"local:aaaaaa1:1\\tquoting\\nlocal:bbbbbb2:1\\tunrelated-class\\n\"),(\"advisory-p2 does not override class\", \"scripts/x.sh:12 local:aaaaaa1:1\\nscripts/x.sh:12 local:bbbbbb2:1\\n\", \"local:aaaaaa1:1\\tquoting\\nlocal:bbbbbb2:1\\tadvisory-p2\\n\")]:
 code=\"set -euo pipefail\\n\"+token+\"\\nline=\"+q(\"- [P2] scripts/x.sh:12 current\")+\"\\nearlier=\"+q(earlier)+\"\\nA=/dev/stdin\\n\"+loop+\"\\nprintf \\\"class=%s%s\\\\n\\\" \\\""'$class'"\\\" \\\""'$repeat'"\\\"\\n\"; r=subprocess.run([\"bash\",\"-c\",code],input=record,text=True,capture_output=True); print(label, \"rc\",r.returncode,r.stdout.strip(),r.stderr.strip())
rows=\"local:aaaaaa1:1\\tquoting\\nlocal:bbbbbb2:1\\tquoting\\nlocal:cccccc3:1\\tquoting\\n\"; r=subprocess.run([\"/usr/bin/grep\",\"-o\",\"-E\",\""'^([0-9]{10,}|audit:[0-9a-f]{7}:[0-9]+)'"\\t[a-z0-9-]+\"],input=rows,text=True,capture_output=True); print(\"chain ledger extraction of three local quoting rows:\",repr(r.stdout),\"rc\",r.returncode)'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc "git show d3e8acfe553791577576282eb0c339c018721bde:tests/unit/test_chain_review_scripts.py | python3 -B -c 'import ast,sys; t=ast.parse(sys.stdin.read()); print(\"Python syntax OK; test methods:\",sum(isinstance(n,ast.FunctionDef) and n.name.startswith(\"test_\") for n in ast.walk(t)))' && git status --short" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc "nl -ba .orchestration/learning/mistakes/M-20261015-02.md && rg -n 'C-50' .orchestration/corrections* .orchestration/learning && git show d3e8acfe553791577576282eb0c339c018721bde:scripts/require-crit-review.py | nl -ba | sed -n '28,48p;790,810p;900,935p'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 exited 1 in 106ms:
     1	---
     2	id: M-20261015-02
     3	artifact: "PR #365 (dotfiles-T128-task-checkers-followup-a01): one P2 defect (orch-audit.sh runs the ledger check as python without -I, so an untracked module beside it would be imported before the read-only audit) raised by the Bot (thread 4279174373 on 4cc9d206), the local review (local:b84e81f:1) and the task-level audit (audit:b84e81f:1), the policy reading of its disposition raised by the audits of PR #364 (c45f9b5:2) and PR #365 (b84e81f:2)"
     4	classes: [sys-path-shadowing, advisory-policy-reading]
     5	found_at: "2026-10-15T05:54:07Z (the audit of b84e81f0, the third row of the class on the artifact; three-repeat.sh: search none, compactiondb 0)"
     6	detector: "the task-level audit; S1 read from the record's class table"
     7	count_at_detection: "sys-path-shadowing: three on PR #365 (the first artifact); advisory-policy-reading: two on the regime today (PR #364 and PR #365), first per artifact"
     8	corrections: [C-50]
     9	status: open
    10	recorded_at: "2026-10-15T05:54:07Z"
    11	---
    12	
    13	# M-20261015-02
    14	
    15	- **Evidence:** the Bot's thread 4279174373 (orch-audit.sh:55, 05:00:08Z), the chain's local review of b84e81f0 (`- [P2] Isolate imports when running the trusted checker — scripts/orchestrator/orch-audit.sh:55-57`), and the audit of b84e81f0 (`[P2] high implementation scripts/orchestrator/orch-audit.sh:57 — … Run the checker with -I and test sibling-module shadowing`) name one defect; the record carried it as `not-applicable:advisory P2 owned by dotfiles-T128-task-checkers-followup-a02` after the Bot, the chain added a second advisory row after the local review, and the audit rejected the disposition as a deferral (`[P2] high orchestration …pr-feedback.json:116 — … AGENTS.md explicitly rejects deferred work as a disposition`), as the audit of PR #364's c45f9b5 had rejected the same policy the hour before.
    16	- **Detection and why not earlier:** the plan 020 step 4 policy makes every P2 advisory, whatever its size, so the orchestrator applied it after the Bot and again after the local review without weighing the fix (one flag, one test, within the task's allowed files); the class reached three only when the audit repeated it, and the three-repeat search found no record because the class was new.
    17	- **Root cause:** plan 020 step 4 and the task template's Completion clause bind every P2 to the lineage's next owner task and give the orchestrator no rule for a small P2 that several reviewers repeat; the owner-task mechanism was designed for findings outside the task's scope or beyond one round, not for a one-line fix inside the PR's own change, and each reviewer that reads AGENTS.md's prohibition of deferral then re-raises the disposition rather than the defect.
    18	- **Should have been:** after the Bot's P2 on the PR's own new code, a revise round with a `check=` (one flag, one test) before the RESULT's integration, the owner-task row reserved for findings outside the task's files or needing a design; the class table read after each reviewer, so the second row of one class already triggers the weighing, not the third.
    19	- **Corrections:** C-50.
zsh:1: no matches found: .orchestration/corrections*

 succeeded in 225ms:
Python syntax OK; test methods: 16
 M .orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a02.md
 M .orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a03.md
 M .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a03.md
?? .orchestration/reports/dotfiles-T128-chain-review-scripts-followup-a03.md
?? .orchestration/sandboxes/dotfiles-T128-chain-review-scripts-followup-a03.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a02-audit-8afc458.md.last.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a03-audit-d3e8acf.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a03-pr-feedback.json
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a03.md

 succeeded in 255ms:
valid rc 0 class=env-s-quoting; repeat of local:bbbbbb2:1 
invalid review suffix .* matches an unrelated class row rc 0 class=unrelated-class; repeat of local:bbbbbb2:1 
advisory-p2 does not override class rc 0 class=quoting; repeat of local:aaaaaa1:1 
chain ledger extraction of three local quoting rows: '' rc 1

**Analyzing security validation nuances**
**Distinguishing specification and orchestration issues**
exec
/bin/zsh -lc "python3 -B -c 'import json,pathlib; p=pathlib.Path(\".orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a03-pr-feedback.json\"); x=json.loads(p.read_text()); print(\"feedback item bodies:\");
for n,i in enumerate(x[\"items\"],1): print(n,i[\"source\"],i[\"level\"],i[\"body\"] if i[\"source\"] not in [\"issue_comment\"] or len(i[\"body\"])<100 else i[\"body\"][:180])'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc "git show d3e8acfe553791577576282eb0c339c018721bde:.orchestration/dotfiles-T128-chain-review-scripts-followup-a03/task.md | nl -ba | sed -n '60,95p' && git diff --quiet 9da0897a d3e8acfe553791577576282eb0c339c018721bde -- scripts/orchestrator/local-advisory.sh tests/unit/test_chain_review_scripts.py" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc "rg -n 'C-50' .orchestration/learning/corrections && git show d3e8acfe553791577576282eb0c339c018721bde:scripts/require-crit-review.py | nl -ba | sed -n '28,48p;790,810p;900,935p'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 117ms:
.orchestration/learning/corrections/C-50.md:2:id: C-50
    28	# A not-applicable reason names the command whose pasted output supports it (plan 007 Phase 0); it is split once
    29	# on its first delimiter, and a second delimiter is refused.
    30	FIXED_DISPOSITION = re.compile(r"fixed:(?P<commit>[0-9a-f]{7,40})")
    31	EVIDENCE_DELIMITER = "; evidence="
    32	DISPOSITION_GRAMMAR = "fixed:<commit> or not-applicable:<reason>; evidence=<command>"
    33	FAILURE_REASON_MIN_CHARS = 20
    34	# The acceptance record's JSON block between its first two --- lines (the prose after it is not read).
    35	RECORD_FORMAT = 1
    36	LEDGER_ID = re.compile(r"\d{10,}|audit:[0-9a-f]{7}:\d+")
    37	CLASS_SLUG = re.compile(r"[a-z0-9-]+")
    38	AUDIT_FINDING_KEYS = {"n", "reason", "evidence"}
    39	# Every audit_findings field is a non-empty string; n holds the finding number in ASCII digits.
    40	FINDING_NUMBER = re.compile(r"[1-9][0-9]*")
    41	RECORD_KEYS = {"format", "task", "head", "pr", "ledger", "searches", "audit_findings", "dispatch"}
    42	# The swept finding ids the ledger must cover: Codex review comments, and Codex review bodies carrying a badge.
    43	CODEX_BOT = "chatgpt-codex-connector[bot]"
    44	BADGE_TOKENS = ("![P0 Badge]", "![P1 Badge]", "![P2 Badge]", "![P3 Badge]")
    45	S6_CLASS_LIMIT = 3
    46	MISTAKE_RECORDS = ".orchestration/learning/mistakes/"
    47	# herdr-agents --audit names and concludes the task-level audit this way.
    48	AUDIT_NAME = re.compile(r"(?P<task>.+)-audit-(?P<sha>[0-9a-f]{7,40})\.md")
   790	    if not is_int(record.get("format")) or record["format"] != RECORD_FORMAT:
   791	        errors.append(f"format must be {RECORD_FORMAT}")
   792	    ledger = record.get("ledger")
   793	    if not isinstance(ledger, list):
   794	        errors.append("ledger must be a list of {id, class} rows")
   795	    else:
   796	        for index, row in enumerate(ledger):
   797	            # A thread id may be a JSON number or a string; the id is its text either way.
   798	            if (
   799	                not isinstance(row, dict)
   800	                or set(row) != {"id", "class"}
   801	                or not isinstance(row["id"], (int, str))
   802	                or isinstance(row["id"], bool)
   803	                or not LEDGER_ID.fullmatch(str(row["id"]))
   804	                or not isinstance(row["class"], str)
   805	                or not CLASS_SLUG.fullmatch(row["class"])
   806	            ):
   807	                errors.append(
   808	                    f"ledger row {index} must be {{id: <thread id or audit:<sha7>:<n>>, class: <[a-z0-9-] slug>}}: {row!r}"
   809	                )
   810	    searches = record.get("searches")
   900	        return [path_error], None
   901	    # Bound like the audit: another task's record must not stand in for this one's.
   902	    if task is not None:
   903	        for name in (path.name, path.resolve().name):
   904	            if name != f"{task}.md":
   905	                return [
   906	                    f"{ACCEPTANCE_ENV} must be {task}.md, the record of the task named by {PR_FEEDBACK_ENV}, not {name}"
   907	                ], None
   908	    if not path.is_file():
   909	        return [f"{ACCEPTANCE_ENV} file does not exist: {path}"], None
   910	    record, error = read_acceptance_record(path)
   911	    if record is None:
   912	        return [f"{ACCEPTANCE_ENV} {error}"], None
   913	    errors = record_field_errors(record, path.name.removesuffix(".md"), head, pr)
   914	    if errors:
   915	        return errors, record
   916	    summary, summary_error = audit_summary(root)
   917	    if summary_error is not None:
   918	        return [summary_error], record
   919	    missing = swept_finding_ids(items, summary, head) - {str(row["id"]) for row in record["ledger"]}
   920	    if missing:
   921	        errors.append(f"S6: ledger lacks {', '.join(sorted(missing))}")
   922	    classes = Counter(row["class"] for row in record["ledger"])
   923	    stated = {entry["class"]: set(entry["records"]) for entry in record["searches"]}
   924	    for cls, count in classes.items():
   925	        if count < S6_CLASS_LIMIT:
   926	            continue
   927	        found = mistake_records(root, cls)
   928	        if isinstance(found, str):
   929	            errors.append(f"S6: class {cls} at {count}: {found}")
   930	        elif stated.get(cls) != found:
   931	            errors.append(f"S6: class {cls} at {count} without a matching records search")
   932	    return errors, record
   933	
   934	
   935	def mistake_records(root: Path, slug: str) -> set[str] | str:

 succeeded in 172ms:
    60	---
    61	
    62	# AGMSG-TASK dotfiles-T128-chain-review-scripts-followup-a03 — local-advisory.sh refuses an absent owner task, hashes the owner file as evidence, and classes a repeated finding by the record's earlier row (corrections C-51 (2) and C-50 (3); the chain-review-scripts lineage's next owner task; a Claude seat)
    63	
    64	Written 2026-10-15 by the orchestrator seat (the bus time of its TASK line is the dispatch time), pair-reviewed before dispatch. Two corrections name this task as the landing of their tool half. C-51 (M-20261015-03): the chain wrote advisory rows whose owner task existed only as a name, with an evidence command (`git show origin/main:.orchestration/tasks/<owner>.md …`) that replays only after a boundary, and two audits raised it. C-50 (M-20261015-02): the class table gives every local advisory row the generic class `advisory-p2`, so a defect found again on a later head is never counted as a repeat of the same class and the three-rows rule cannot fire on it.
    65	
    66	## Change (round 2, 2026-10-15T22:08:38Z)
    67	
    68	The review seat's round 1 (confirm on `0d82d7c4`, five P3 taken as text fixes since the task waits for the a02 owner task): the owner check sits after the no-findings exit and before the heading; both refusals exit 2 with distinct messages; the token grammar ignores backticks and allows a line range, and the earlier number is the loop's; the scope (local review files and `local:` rows only) is stated against C-50's wider sentence; a repeat row's line names its provenance.
    69	
    70	## Change (round 3, 2026-10-15T22:11:13Z)
    71	
    72	The Codex half's round 2 (on `5bd7e601`): P3 the absent-owner case now asserts the record byte-identical to its pre-run content; P3 the repeat test adds a line-range token and two matching earlier heads with different classes, the later head's class winning.
    73	
    74	## Goal
    75	
    76	After the merge, `local-advisory.sh` writes no row whose owner task file is absent, its evidence command hashes that file in the checkout it runs from, and a finding repeated from an earlier head of the task takes the class the record gave the earlier finding.
    77	
    78	## Files
    79	
    80	1. `scripts/orchestrator/local-advisory.sh`: (a) after the script's existing exit 0 for a review without findings and before it writes the `## Owned by <owner>` heading, `.orchestration/tasks/<owner>.md` must exist in the repository root the script runs from, else it prints `write the owner task <owner> first` and exits 2 as well (the missing review file keeps its exit 2; the two messages tell them apart and the `@exitcode 2` line names both), so a refused run leaves the record untouched and a review without findings needs no owner file; the `evidence=` tail of each `local-finding:` line becomes `shasum -a 256 .orchestration/tasks/<owner>.md` with the file's sha256 at the time of writing appended as `(<sha256>)`, so the line replays in the orchestrator's checkout before the boundary; (b) each finding's token, the first run of path characters, `:` and digits with an optional `-<digits>` range in the finding's line (backticks around it ignored, so `` `a.sh:1` `` and `resolve-threads.sh:48-52` both count), is compared with the findings of the task's earlier local review files (`.orchestration/validation/<task>-local-review-*.md` other than the current head's), each numbered as this script's own loop numbers them (`sort -u` order, P0 and P1 lines included); when an earlier finding has the same token and the record holds a row `local:<sha7'>:<n'><TAB><class>` for it with a class other than `advisory-p2`, the new row takes that class, the latest matching head's row winning when two earlier files match with different classes, and its `local-finding:` line's parenthesis gains `repeat of local:<sha7'>:<n'>` so the provenance is on the line; otherwise `advisory-p2`, as today. The scope is the local review files and the `local:` rows only: a repeat first classed by a Bot thread's row or an `audit:` row keeps `advisory-p2`, since those rows carry no `path:line` token (C-50's wider sentence is applied here to the one source that has tokens). Nothing else changes (the P0/P1 stop, the heading, the once-only writes).
    81	2. `tests/unit/test_chain_review_scripts.py`: two new tests in the module's style (the temporary repository, the script as a subprocess): `test_local_advisory_refuses_an_absent_owner_task_and_hashes_the_file` (no owner file: exit 2, `write the owner task` on stdout or stderr, and the record byte-identical to what the case wrote before the run, so no heading and no row appeared; with the owner file: exit 0, the `local-finding:` line's evidence names `shasum -a 256 .orchestration/tasks/<owner>.md` and the file's actual sha256) and `test_local_advisory_classes_a_repeat_by_the_earlier_row` (two earlier review files: the older with a finding at `scripts/x.sh:12` whose record row carries the class `quoting`, the newer with the same token whose row carries `env-s-quoting`, and the older also with a finding at `scripts/y.sh:3-5` whose row carries `range-case`; a current review file with a P2 at `` `scripts/x.sh:12` `` in backticks, one at `scripts/y.sh:3-5` and one at another token: the new rows are `env-s-quoting` (the later head's class wins), `range-case` (the line-range token matches) and `advisory-p2` respectively, and the first two rows' `local-finding:` lines hold `repeat of local:<sha7'>:<n'>` naming the matched head and number; a review without findings and no owner file: exit 0 and no heading written).
    82	
    83	## Out of scope
    84	
    85	`local-review.sh` and `sandbox-scan.sh` (the a02 owner task's and the lineage's); the chain scripts that call this one (T7's `chain-integrate.sh`); the record's class table beyond the rows this script writes.
    86	
    87	## Check
    88	
    89	`uv run python -m unittest tests/unit/test_chain_review_scripts.py -v` green (the module's tests and the two new ones), pasted in the validation file with `shellcheck scripts/orchestrator/local-advisory.sh` and `git diff --numstat origin/main...HEAD`: at most 200 changed lines (added plus deleted) outside `tests/` and outside `.orchestration/` (plan 021 step 7.2) and 1000 added lines under `tests/` (INV-2).
    90	
    91	## Completion
    92	
    93	One PR from a fresh branch off `origin/main` (after PR #376, the a02 owner task's PR, merged as f7847616 on 2026-10-17). The PR is ready for the orchestrator's integration when the ruleset's required checks are green, the Bot's review of the final head is in (at PR open, and once more on `@codex review` after a P0/P1 fix round: plan 020 step 2), every Bot thread is replied to and resolved by the orchestrator with its disposition, the validation file carries the outputs above, and the RESULT names every P0/P1 thread with `fixed:<sha>` and every P2 thread with the disposition the worker proposes; the orchestrator's audit of the final head is dispositioned finding by finding before the gate, and a P0/P1 it leaves is the operator's decision. The Bot's P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P0 or P1 that survives the round is listed as `open:<thread id>` with `bot_rounds=2` (the Bot's review at PR open and its re-review after the fix round), stops the PR and goes to the operator as a decision; a P2 on this PR's own change whose fix stays within `allowed_files` and is small (one flag or a few lines plus one test) is fixed in a revise round the orchestrator sends with a `check=` while INV-6's counts allow it (C-50); any other P2 is advisory, owned by `dotfiles-T128-chain-review-scripts-followup-a04`, which the orchestrator writes when the first advisory P2 appears, before the PR's dispositions (C-51), and recorded under `## Owned by dotfiles-T128-chain-review-scripts-followup-a04` in this task's acceptance record. The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`. The RESULT names head, base, branch, files, every Bot thread with its disposition, the test names per row, the caps, `task_copy=<sha256 of .orchestration/dotfiles-T128-chain-review-scripts-followup-a03/task.md>` and the evidence paths.
    94	
    95	## Owned row (2026-10-16T05:53:07Z)

 succeeded in 176ms:
feedback item bodies:
1 issue_comment comment <!-- codex-pull-request-review-summary -->
<!-- codex-review-state:v1 {"code_review":{"commit_sha":"d2b33025d05f00b8dca947b54f9bbe0d16f1991b","has_any_findings":false,"has_unresolv
2 issue_comment comment <!-- This is an auto-generated comment: summarize by coderabbit.ai -->
<!-- This is an auto-generated comment: skip review by coderabbit.ai -->

> [!IMPORTANT]
> ## Review skipped

3 issue_comment comment @codex review
4 issue_comment comment <!-- codex-review-receipt:v1 -->

Codex Review: Didn't find any major issues. What shall we delve into next?

**Reviewed commit:** `d2b33025d0`

<details> <summary>ℹ️ About Codex i
5 annotation notice Due to capacity constraints, jobs targeting macOS arm64 runners may experience longer queue times.
6 annotation notice Due to capacity constraints, jobs targeting macOS arm64 runners may experience longer queue times.
7 annotation notice Due to capacity constraints, jobs targeting macOS arm64 runners may experience longer queue times.
8 status success CodeRabbit: Review skipped: automatic reviews are disabled

**Verifying data consistency**
exec
/bin/zsh -lc "nl -ba .orchestration/learning/corrections/C-50.md && git show d3e8acfe553791577576282eb0c339c018721bde:scripts/orchestrator/chain-integrate.sh | nl -ba | sed -n '170,195p' && git status --short -- scripts tests" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 24ms:
     1	---
     2	id: C-50
     3	closes: [M-20261015-02]
     4	means: "A P2 on a PR's own change whose fix stays within the task's allowed_files and is small (one flag or a few lines plus one test) is fixed in a revise round with a check= before integration, never dispositioned as advisory to the owner task; the owner-task row is for a P2 outside the task's files, needing a design, or beyond one round. The class table is read after every reviewer, and two rows of one class on an artifact already trigger the weighing."
     5	method: "(1) done 2026-10-15T05:54:07Z: PR #365's defect sent to a002 as a revise round (check=tests/unit/test_orchestrator_tools.py::test_orch_audit_runs_the_ledger_check_isolated_from_sibling_modules, previous_head=b84e81f0), the record's class table corrected (the chain's generic advisory-p2 class replaced by the defect's class), the three-repeat search pasted; (2) done 2026-10-15 for plan 020 step 4's Completion clause and 2026-10-15T10:57:56Z for the task template .orchestration/templates/task-short.md (both the orchestrator's boundary edits: the template is an .orchestration file that task-consistency-check.py's C2 keeps out of a worker task's allowed_files, so it never travels through a worker PR); pending for the SKILL and rule sentences through the standing-rules task dotfiles-T128-rules-step8-a01 (plan 022 T13), and the chain's local-advisory step classes a repeated finding by the record's existing row for the same file:line instead of the generic class (orchestrator-tools lineage, next owner task)."
     6	sources:
     7	  - url: ".orchestration/plans/020-certain-order.md step 4 (the advisory-P2 policy)"
     8	    fetched_at: "2026-10-15"
     9	    quote: "a P2 on this PR is advisory, owned by <lineage>-followup-a0<n>, which the orchestrator writes when the first advisory P2 appears"
    10	    verified_by: "the Completion clauses of the T128 short-form tasks of 2026-10-14 and 2026-10-15"
    11	  - url: "AGENTS.md, Audit section and the task-level audit bullet of the agmsg-orchestration SKILL"
    12	    fetched_at: "2026-10-15"
    13	    quote: "Deferral (\"later\", a follow-up task, a stopgap or a suppression) is not a disposition."
    14	    verified_by: "the audits of c45f9b5 (PR #364) and b84e81f (PR #365), both raising the policy as an orchestration finding"
    15	mechanism: ['procedure:revise round with check= for a small in-scope P2 (standing from 2026-10-15T05:54:07Z)', 'rule:plan 020 step 4 Completion clause (done 2026-10-15) and task-short.md template (done 2026-10-15T10:57:56Z, orchestrator boundary edit)', 'rule:SKILL step 15, Message Contract and pr-integration.md sentences (pending, plan 022 T13 dotfiles-T128-rules-step8-a01)', 'tool:local-advisory.sh classes a repeat by the existing row of the same file:line (pending, dotfiles-T128-chain-review-scripts-followup-a03: the script belongs to the chain-review lineage)']
    16	verification: "pending: the next small P2 on a PR's own change is fixed in a revise round and its class never reaches three; the audit after the fix raises no orchestration finding on the disposition."
    17	status: pending
    18	---
   170	say "${now} receipt rc=0: printf > .orchestration/validation/${task}-review-receipt.md"
   171	# The gate's LEDGER_ID: a thread id of ten or more digits or audit:<sha7>:<n>; local: rows stay in the prose.
   172	tsv=${v}/${task}-ledger-${sha7}.tsv
   173	step record 0,1 /usr/bin/grep -o -E $'^([0-9]{10,}|audit:[0-9a-f]{7}:[0-9]+)\t[a-z0-9-]+' "${record}"
   174	printf '%s\n' "${out}" > "${tsv}"
   175	step record 0 "${uv}" run --no-project python -I "${main}/scripts/orchestrator/acceptance-front-matter.py" "${task}" "${sweep}" "${review}" --ledger "${tsv}"
   176	rm -f -- "${tsv}"
   177	step audit 0 "${main}/scripts/orchestrator/orch-audit.sh" "${task}" "${review}" "${pr}"
   178	verdict="chain-integrate: ${task} ${head} ${out##*$'\n'}"
   179	step audit 0 "${git}" -C "${review}" checkout -q --detach "${head}" # orch-audit.sh leaves it at origin/main; the gate reads it
   180	say "${verdict}" && echo "${verdict}"

**Refining task scope and evaluation**
**Assessing invariant reporting and findings**
**Assessing report completeness and bot review**
**Summarizing reproducible findings with precise formatting**

I’m preparing a clear explanation of two reproducible cases without broad invariant issues, aiming for about 300–400 words in English with a brief Japanese summary preamble. I’ll format findings in concise paragraphs with specific P2 labels, note invariant assessments with references to INV2 and INV6 limitations, and respect the user’s preference for exact, code-linked citations without headings or final approval statements.
**Verifying PR diff consistency**
**Summarizing orchestration validation results**

I’m reviewing evidence for local row assertions, confirming patterns and orchestration findings showing some repeated local rows bypass enforcement. No tests are rerun, but existing shellcheck results and code validation support the conclusion. I’ll prepare a concise final summary with key evidence and remarks within 350 words.
codex
[P2] high implementation scripts/orchestrator/local-advisory.sh:81 Historical filename suffixes enter `grep -E` without validation or escaping. A matching-token file named `t-a01-local-review-.*.md` inherits the last unrelated `local:*:1` row’s class and provenance. The read-only reproduction returned `unrelated-class`; require a seven-hex suffix and literal ID matching.

[P2] high orchestration .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a03.md:85 The task excludes consumers needed for its stated three-row enforcement goal: `chain-integrate.sh:173` drops every `local:` row, and `require-crit-review.py:36` rejects those ledger IDs. Three repeated `quoting` rows therefore produce an empty ledger and never trigger S6. Class propagation alone leaves the claimed correction incomplete.

The task declares no front-matter invariants; its referenced design checks are:

INV-2: holds .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a03.md:225 — 43 production lines changed and 60 test lines added, within caps.
INV-6: violated scripts/orchestrator/chain-integrate.sh:173 — repeated local classes remain excluded from the mandatory three-row search check.

All four premises reproduce, and task/report/validation/sandbox copies match the audited head. Bash syntax, ShellCheck, and Python parsing passed. Saved feedback records 12 successful checks for `d3e8acf`.

Orchestration findings: 1

📝 まとめ: Audited [PR 381](https://github.com/mryfmo/dotfiles/pull/381); found two P2 issues and modified nothing. Unit/Bats tests were not rerun; GitHub live verification was unavailable, so CI assessment relies on supplied evidence.
Verdict: incorrect
hook: Stop
hook: Stop Completed
tokens used
121,863
[P2] high implementation scripts/orchestrator/local-advisory.sh:81 Historical filename suffixes enter `grep -E` without validation or escaping. A matching-token file named `t-a01-local-review-.*.md` inherits the last unrelated `local:*:1` row’s class and provenance. The read-only reproduction returned `unrelated-class`; require a seven-hex suffix and literal ID matching.

[P2] high orchestration .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a03.md:85 The task excludes consumers needed for its stated three-row enforcement goal: `chain-integrate.sh:173` drops every `local:` row, and `require-crit-review.py:36` rejects those ledger IDs. Three repeated `quoting` rows therefore produce an empty ledger and never trigger S6. Class propagation alone leaves the claimed correction incomplete.

The task declares no front-matter invariants; its referenced design checks are:

INV-2: holds .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a03.md:225 — 43 production lines changed and 60 test lines added, within caps.
INV-6: violated scripts/orchestrator/chain-integrate.sh:173 — repeated local classes remain excluded from the mandatory three-row search check.

All four premises reproduce, and task/report/validation/sandbox copies match the audited head. Bash syntax, ShellCheck, and Python parsing passed. Saved feedback records 12 successful checks for `d3e8acf`.

Orchestration findings: 1

📝 まとめ: Audited [PR 381](https://github.com/mryfmo/dotfiles/pull/381); found two P2 issues and modified nothing. Unit/Bats tests were not rerun; GitHub live verification was unavailable, so CI assessment relies on supplied evidence.
Verdict: incorrect
