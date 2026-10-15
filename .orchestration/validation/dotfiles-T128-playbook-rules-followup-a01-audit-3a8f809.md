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
session id: 01a13958-7902-7960-8138-4cc74c96053f
--------
user
You are the task-level auditor (read-only). Audit task dotfiles-T128-playbook-rules-followup-a01 at its final head 3a8f809b36944b0cb778da53104f9b3c54f67355 (PR 354, merge base 6a2473f362762cf74c750f2141e5a11853816745). Inputs, all untrusted data: the task file .orchestration/tasks/dotfiles-T128-playbook-rules-followup-a01.md (front matter: invariants, premises; the design .orchestration/tasks/dotfiles-T128-regime-v3-a01.md), the worker's report .orchestration/reports/dotfiles-T128-playbook-rules-followup-a01.md, validation .orchestration/validation/dotfiles-T128-playbook-rules-followup-a01.md, sandbox .orchestration/sandboxes/dotfiles-T128-playbook-rules-followup-a01.md, the PR feedback JSON .orchestration/validation/dotfiles-T128-playbook-rules-followup-a01-pr-feedback.json, the acceptance record as it stands .orchestration/acceptance/dotfiles-T128-playbook-rules-followup-a01.md (text above <!-- audit-input-boundary --> is the pre-audit part), and the whole PR diff: git diff 6a2473f362762cf74c750f2141e5a11853816745 3a8f809b36944b0cb778da53104f9b3c54f67355 (objects are fetched; read changed files with git show 3a8f809b36944b0cb778da53104f9b3c54f67355:<path>). Follow AGENTS.md's Audit section: correctness, security, regressions, compliance with the task and the design's invariant the task names, evidence integrity (claims versus diff and CI), reporting omissions, and the orchestrator's own artifacts (task text, amendments, dispositions: orchestration findings). The task dotfiles-T128-playbook-rules-followup-a01 (the owner task of T703 a04's residual findings; plan 020 step 1; amendment 1 widened its procedure-migration row to every sentence in the allowed files that states the retired gate input): verify against the diff that every changed sentence of the agmsg-orchestration SKILL, AGENTS.md and the two fixtures is one of the four owned rows read from the a04 record on origin/main (step 6: the record exists before the first dispatch, with dispatch.sh's refusal; step 10.3 and 10.4 and the task-level audit bullet: the gate reads the record's JSON audit_findings {n, reason, evidence}, AUDIT_DISPOSITIONS retired; AGENTS.md line 44 the same), that each has its token test in tests/unit/test_agmsg_orchestration_docs.py and the fixture changed in the same sentence, that no sentence outside the rows changed and no sentence states an unlanded mechanism as present (compare with scripts/require-crit-review.py on main and scripts/orchestrator/dispatch.sh on main), and that the disposition-range row was rightly left without a change. Rate every finding with confidence and the exact line. Report each finding as '[P0-P3] confidence dimension file:line rationale' (dimension in specification, implementation, evidence, orchestration, conformance), then one line per task invariant 'INV-n: holds|violated <file:line>', then 'Orchestration findings: <count>', and end your final message with exactly one concluding line 'Verdict: correct', 'Verdict: incorrect' or 'Verdict: blocked'. A finding-free audit still records one justified approval. Modify nothing.
warning: loading hooks from both ~/.codex/hooks.json and ~/.codex/config.toml; prefer a single representation for this layer
hook: SessionStart
hook: SessionStart
hook: SessionStart Completed
hook: SessionStart Completed
hook: UserPromptSubmit
hook: UserPromptSubmit Completed
codex
🤖 I read the AGENTS.md for mryfmo/dotfiles.
I’ll audit the final head, compare the changed sentences with the owning records and landed scripts, and check the reported tests and PR feedback. I’m using the agmsg-orchestration, GitHub workflow, and Ponytail review skills; all work will remain read-only.
exec
/bin/zsh -lc 'cat ~/.agents/skills/agmsg-orchestration/SKILL.md' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc 'cat ~/.agents/skills/gh-first-workflow/SKILL.md && cat ~/.codex/plugins/cache/ponytail/ponytail/5.2.0/skills/ponytail/SKILL.md && cat ~/.codex/plugins/cache/ponytail/ponytail/5.2.0/skills/ponytail-review/SKILL.md' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc 'pwd && git status --short && git rev-parse HEAD && git rev-parse origin/main' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 104ms:
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

 succeeded in 124ms:
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

 succeeded in 163ms:
~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 M .orchestration/tasks/dotfiles-T128-playbook-rules-followup-a01.md
?? .orchestration/acceptance/dotfiles-T128-playbook-rules-followup-a01.md
?? .orchestration/reports/dotfiles-T128-playbook-rules-followup-a01.md
?? .orchestration/sandboxes/dotfiles-T128-playbook-rules-followup-a01.md
?? .orchestration/validation/dotfiles-T128-playbook-rules-followup-a01-audit-3a8f809.md
?? .orchestration/validation/dotfiles-T128-playbook-rules-followup-a01-pr-feedback.json
?? .orchestration/validation/dotfiles-T128-playbook-rules-followup-a01.md
6a2473f362762cf74c750f2141e5a11853816745
6a2473f362762cf74c750f2141e5a11853816745

**Maintaining read-only access**
codex
🐙 私は gh-first-workflow を読みました。
The checkout has local audit inputs, so I’ll read the reviewed files directly from the specified Git commits and keep those inputs separate. Your read-only instruction also means I won’t write worklogs or review receipts.
exec
/bin/zsh -lc "rg -n 'Orchestrator Playbook|task-level audit|"'^6'"\\.|"'^10'"\\.|"'^11'"\\.|Codex seat worklogs' ~/.agents/skills/agmsg-orchestration/SKILL.md && if test -f .ua/meta.json; then cat .ua/meta.json; fi && if test -f .ua/knowledge-graph.json; then python3 -B -c 'import json; d=json.load(open(\".ua/knowledge-graph.json\")); print(type(d).__name__); print(list(d)[:15]); nodes=d.get(\"nodes\",[]); print(\"nodes\",len(nodes)); print(json.dumps([{\"summary\":n.get(\"summary\"), \"filePath\":n.get(\"filePath\")} for n in nodes if any(s in str(n.get(\"filePath\", \"\")) for s in [\"require-crit\", \"orchestrator/dispatch\", \"test_agmsg_orchestration_docs\", \"regime-v3\", \"playbook\"])],indent=2))'; fi" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc 'git diff --stat 6a2473f362762cf74c750f2141e5a11853816745 3a8f809b36944b0cb778da53104f9b3c54f67355 && git diff --no-ext-diff 6a2473f362762cf74c750f2141e5a11853816745 3a8f809b36944b0cb778da53104f9b3c54f67355' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc 'gh pr view 354 --json url,state,baseRefName,baseRefOid,headRefName,headRefOid,statusCheckRollup,reviews,commits' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc 'nl -ba .orchestration/tasks/dotfiles-T128-playbook-rules-followup-a01.md && nl -ba .orchestration/reports/dotfiles-T128-playbook-rules-followup-a01.md && nl -ba .orchestration/validation/dotfiles-T128-playbook-rules-followup-a01.md && nl -ba .orchestration/sandboxes/dotfiles-T128-playbook-rules-followup-a01.md && nl -ba .orchestration/acceptance/dotfiles-T128-playbook-rules-followup-a01.md' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 305ms:
 .../autoskill.md                                   |   3 +
 .../learning.md                                    |   6 +
 .../report.md                                      |  58 +++++++
 .../sandbox.md                                     |  26 ++++
 .../task.md                                        |  87 +++++++++++
 .../validation.md                                  | 171 +++++++++++++++++++++
 AGENTS.md                                          |   2 +-
 .../dot_agents/skills/agmsg-orchestration/SKILL.md |  10 +-
 tests/fixtures/regime/invariants.md                |   2 +-
 tests/fixtures/regime/orchestrator-step-6.md       |   2 +-
 tests/unit/test_agmsg_orchestration_docs.py        |  52 ++++++-
 11 files changed, 407 insertions(+), 12 deletions(-)
diff --git a/.orchestration/dotfiles-T128-playbook-rules-followup-a01/autoskill.md b/.orchestration/dotfiles-T128-playbook-rules-followup-a01/autoskill.md
new file mode 100644
index 00000000..c20887fa
--- /dev/null
+++ b/.orchestration/dotfiles-T128-playbook-rules-followup-a01/autoskill.md
@@ -0,0 +1,3 @@
+# AutoSkill run: dotfiles-T128-playbook-rules-followup-a01
+
+- Status: not used. The task names no AutoSkill run.
diff --git a/.orchestration/dotfiles-T128-playbook-rules-followup-a01/learning.md b/.orchestration/dotfiles-T128-playbook-rules-followup-a01/learning.md
new file mode 100644
index 00000000..4e434c60
--- /dev/null
+++ b/.orchestration/dotfiles-T128-playbook-rules-followup-a01/learning.md
@@ -0,0 +1,6 @@
+# Learning triage: dotfiles-T128-playbook-rules-followup-a01
+
+These are candidates only; nothing is promoted.
+
+1. [memory:decision] An owner section can hold rows that name no rule sentence. `audit:65a3d71:1` (disposition-range) was a sweep-table correction, already made. Report such a row as no change with its reason, rather than inventing a sentence to edit.
+2. [memory:failure] A retired gate input survives in every artifact that restated it. The audit named SKILL lines 171 to 178, but the task-level audit bullet and AGENTS.md:44 stated the same retired mechanism, so a migration fixed by line numbers stays half done. Before editing, grep the allowed files for the retired names (`AUDIT_DISPOSITIONS`, `audit-finding`) and ask once for the scope, with the hits pasted. Amendment 1 then named every sentence.
diff --git a/.orchestration/dotfiles-T128-playbook-rules-followup-a01/report.md b/.orchestration/dotfiles-T128-playbook-rules-followup-a01/report.md
new file mode 100644
index 00000000..0f2fbe1f
--- /dev/null
+++ b/.orchestration/dotfiles-T128-playbook-rules-followup-a01/report.md
@@ -0,0 +1,58 @@
+---
+task_id: dotfiles-T128-playbook-rules-followup-a01
+seat: claude-standard-dot-a002
+branch: regime/playbook-rules-followup
+base: c15ba668da20dc2956220077cb0f20054ab352c7
+rule_commit: 7a282f3b
+task_sha256: ec415eaf526937fd43907a59fccfc455de117850003ba3d48cd20b065fc5564b
+---
+
+# Report: dotfiles-T128-playbook-rules-followup-a01
+
+- Seat: `claude-standard-dot-a002` in `.claude/worktrees/worker-f`, on a fresh branch `regime/playbook-rules-followup` from `origin/main` `c15ba668`. The task-checkers branch stays as it is.
+- Task file: amendment 1, sha256 `ec415eaf…`, copied byte-identical to `.orchestration/dotfiles-T128-playbook-rules-followup-a01/task.md` (validation §1).
+- Round 1 was dispatched at 06:47:41Z. At 06:50Z I asked whether two more sentences belonged to the `procedure-migration` row: the task-level audit bullet and AGENTS.md:44, which both state the retired gate input outside SKILL lines 171 to 178. Amendment 1 (07:03:44Z) put them in the row. Nothing was pushed before it.
+
+## The owned rows
+
+The `## Owned by dotfiles-T128-playbook-rules-followup-a01` section of `.orchestration/acceptance/dotfiles-T128-playbook-rules-a04.md` on `origin/main` (sha256 `3bfd13d7…`) holds four rows (validation §2):
+
+| Row | Class | What changed (`7a282f3b`) |
+|---|---|---|
+| `local:65a3d71:1` | rule-gap | Orchestrator Playbook step 6: "so the orchestrator creates that record, `.orchestration/acceptance/<task>.md`, before the task's first dispatch (`scripts/orchestrator/dispatch.sh` refuses a record that does not exist or that names another task)". `dispatch.sh` refuses a record that is not an existing regular file or whose `task` is another task (its header, validation §3). The pinned fixture `orchestrator-step-6.md` changes with it. |
+| `audit:65a3d71:2` | rule-gap | The same finding as `local:65a3d71:1`, as the audit of `65a3d71b` raised it, so it is fixed by the same sentence. |
+| `audit:71eb920:1` | procedure-migration | Every sentence in the allowed files that still stated the retired gate input (amendment 1); the gate on `main` reads the record's JSON `audit_findings` and only reports `AUDIT_DISPOSITIONS` as retired (validation §3). The changed sentences are listed below the table. |
+| `audit:65a3d71:1` | disposition-range | No rule sentence: the finding was a sweep-table disposition (`fixed:a03c1daa` outside base..head), corrected in a04's sweep at 14:41Z. Nothing changes for it. |
+
+The `procedure-migration` row changed these sentences:
+
+- **The task-level audit bullet (invariants section):**
+  - An `incorrect` verdict is dispositioned in `audit_findings`, the only form the gate reads: one `{n, reason, evidence}` entry per finding, `n` a string, `reason` at least 20 characters. The entries are written with `acceptance-front-matter.py --audit-dispositions`, and an entry never cites a fix.
+  - A `Verdict: correct` finding keeps its `audit-finding: <n> …` prose line.
+  - The pinned fixture `invariants.md` changes with it.
+- **Step 10.3:** it now points to that bullet.
+- **Step 10.4:** the gate command drops `[AUDIT_DISPOSITIONS=<acceptance record>]`, and the `AUDIT_EVIDENCE` bullet now asks for an `audit_findings` entry per finding.
+- **AGENTS.md:44:** the gate takes `PR_FEEDBACK_EVIDENCE`, `AUDIT_EVIDENCE` and `ACCEPTANCE_EVIDENCE`.
+
+Each changed sentence has a token test, and the superseded forms are asserted absent:
+
+- `test_dispatches_are_recorded_from_the_bus`;
+- `test_the_gate_reads_the_acceptance_record`;
+- `test_an_incorrect_audit_is_dispositioned_in_audit_findings` (new).
+
+The documentation module runs 48 tests OK (validation §4).
+
+## Caps and checks
+
+- **INV-2** (validation §7): 5 files outside `.orchestration/`, 6 added lines outside `tests/` and 50 added lines under `tests/`.
+- **Formatting:** prettier and `ruff format --check` are clean.
+- **`ruff check`:** reports the module's implicit-concatenation style (ISC004) on the new tuples as on its existing ones, 12 against 7 on `origin/main`. CI runs only the format check.
+
+## CI and the Bot
+
+In the RESULT. The Bot reviews once, at PR open.
+
+## Not done, or outside scope
+
+- Understand-Anything hook: did not fire. plan-mode-used: no.
+- cost: n/a (the runtime exposes no session figures to the seat).
diff --git a/.orchestration/dotfiles-T128-playbook-rules-followup-a01/sandbox.md b/.orchestration/dotfiles-T128-playbook-rules-followup-a01/sandbox.md
new file mode 100644
index 00000000..51dc4e2c
--- /dev/null
+++ b/.orchestration/dotfiles-T128-playbook-rules-followup-a01/sandbox.md
@@ -0,0 +1,26 @@
+---
+task_id: dotfiles-T128-playbook-rules-followup-a01
+seat: claude-standard-dot-a002
+permission_gated_commands: see the table
+---
+
+# Sandbox record: dotfiles-T128-playbook-rules-followup-a01
+
+- Period: from the AGMSG-TASK (2026-10-14T06:47:41Z) to the RESULT.
+- These ran inside the sandbox:
+  - the HTTPS `git fetch` and `git push`;
+  - the branch, the edits, the task copy and the commits;
+  - every test and format run, with `UV_OFFLINE=1`, since uv cannot reach pypi from the sandbox.
+- No local mutation was chained onto a call that ran outside the sandbox.
+
+Calls outside the sandbox: `gh` through the permission gate (`dangerouslyDisableSandbox`; `gh` fails TLS inside the sandbox) and `agmsg-dispatch` through `excludedCommands`.
+
+| # | Command | Step 4 case |
+|--:|---|---|
+| 1 | `agmsg-dispatch … AGMSG-PONG v1 task_id=dotfiles-T128-playbook-rules-followup-a01 status=question …` (06:50Z, the scope of the procedure-migration row) | `agmsg-dispatch` |
+| 2 | `agmsg-dispatch … AGMSG-PONG v1 … status=alive note=working…` (06:53Z) | `agmsg-dispatch` |
+| 3 | `gh pr create --draft …` | `gh` |
+| 4 | `gh pr ready <n>` | `gh` |
+| 5 | Bot wait from the ready (background; `gh api` reads every 30 seconds) | `gh` |
+| 6 | `gh pr checks <n> --watch` (exit status joined) | `gh` |
+| 7 | `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T128-playbook-rules-followup-a01 …` | `agmsg-dispatch` |
diff --git a/.orchestration/dotfiles-T128-playbook-rules-followup-a01/task.md b/.orchestration/dotfiles-T128-playbook-rules-followup-a01/task.md
new file mode 100644
index 00000000..25d35372
--- /dev/null
+++ b/.orchestration/dotfiles-T128-playbook-rules-followup-a01/task.md
@@ -0,0 +1,87 @@
+---
+format: 2
+task_id: dotfiles-T128-playbook-rules-followup-a01
+kind: docs
+security: false
+design_review:
+  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
+  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
+allowed_files:
+  - home/dot_agents/skills/agmsg-orchestration/SKILL.md
+  - AGENTS.md
+  - tests/unit/test_agmsg_orchestration_docs.py
+  - tests/fixtures/regime/*.md
+  - .orchestration/dotfiles-T128-playbook-rules-followup-a01/**
+after: [dotfiles-T128-playbook-rules-a04]
+threat_table:
+  - control: the PR edits home/dot_agents/skills/agmsg-orchestration/SKILL.md, the rules Claude seats follow once it is applied
+    disposition: "residual: the applied copy changes only after the merge and the operator's make update; before the merge the orchestrator's diff review and the audit from main judge every sentence, and tests/unit/test_agmsg_orchestration_docs.py pins each new sentence with a token and each changed section whole"
+  - control: the PR edits AGENTS.md "Code Review Rules", which the Codex Bot reads from the PR tree, so a PR can rewrite the Bot's rules for its own review
+    disposition: "residual: the Bot's review of a PR that edits its own rules is swept feedback with no gate authority (INV-7); the task-level audit runs with main's AGENTS.md as its instruction root (INV-5) and the orchestrator's review reads the diff; a change to Code Review Rules is review tier with one schema audit (INV-1)"
+  - control: the PR edits tests/unit/test_agmsg_orchestration_docs.py, the module that pins its own rule sentences, so it controls the oracle as well as the text
+    disposition: "residual: the orchestrator's diff review and the task-level audit from main read the test diff beside the prose diff"
+  - control: the PR edits tests/fixtures/regime/*.md, the expected values of test_regime_rule_sections_are_pinned_whole, so a rule and its fixture can change together
+    disposition: "residual: a fixture diff is the declared change itself (the test's message requires listing it in the RESULT, INV-12); the orchestrator's diff review and the task-level audit from main read each fixture diff beside the prose diff, and main keeps the previous fixture to compare against"
+  - control: the task-file copy on the branch (.orchestration/dotfiles-T128-playbook-rules-followup-a01/task.md)
+    disposition: "residual: the copy is byte-identical to the dispatched task file (sha256 in the worker's validation file, compared by the orchestrator at acceptance); the pair's receipts name this file's hash"
+  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
+    disposition: "residual: read with PyYAML by task-consistency-check C1 to C6 before dispatch and by the orchestrator at acceptance, never by a hand-written parser; a changed field fails the byte comparison above"
+  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
+    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file, so a second front matter or a moved separator fails acceptance"
+  - control: the branch evidence records under .orchestration/dotfiles-T128-playbook-rules-followup-a01/ (report.md, validation.md, sandbox.md, learning.md, autoskill.md)
+    disposition: "residual: they are the worker's untrusted claims; acceptance re-checks each claim against the diff, CI and the test output, and the audit reads those sources itself"
+  - control: in-process effects
+    disposition: "residual: none; the declared test module reads prose and fixtures and imports no changed script"
+  - control: workflow and interpreter or environment inputs
+    disposition: "residual: none in allowed_files; an undeclared change to such a file is outside the task and fails at the audit (INV-12)"
+  - control: new or renamed scripts
+    disposition: "residual: none; allowed_files names no script path, so a new or renamed script is an undeclared change the audit fails"
+  - control: orchestrator effect merge
+    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
+  - control: orchestrator effect update-branch
+    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
+  - control: orchestrator effect forced worker removal
+    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
+premises:
+  - claim: "the a04 task names this task as the owner of the residual findings of PR #328's final head"
+    command: "grep -c 'owned by dotfiles-T128-playbook-rules-followup-a01' .orchestration/tasks/dotfiles-T128-playbook-rules-a04.md"
+    output: "1"
+  - claim: "the a04 acceptance record is on origin/main (the owned section is appended to it by the boundary after a04's merge, before this task dispatches)"
+    command: "git cat-file -e origin/main:.orchestration/acceptance/dotfiles-T128-playbook-rules-a04.md && echo present"
+    output: "present"
+
+---
+
+# AGMSG-TASK dotfiles-T128-playbook-rules-followup-a01 — the residual findings of PR #328's final head (the owner task of T703 a04's Completion clause, plan 017; C-32's owner-first pattern)
+
+Written 2026-10-13 10:19Z by the orchestrator seat, pair-reviewed before dispatch. T703's a04 (PR #328) gets one revise round for the findings of its amendment-1 head (the Bot's and the C-32 local review's); a P2 finding on the final head that round did not fix is dispositioned on PR #328 as `not-applicable:advisory P2 owned by dotfiles-T128-playbook-rules-followup-a01; evidence=git show origin/main:.orchestration/tasks/dotfiles-T128-playbook-rules-followup-a01.md | grep -n 'item 1'` (the gate's full form once PR #329 lands) and recorded as a row of `.orchestration/acceptance/dotfiles-T128-playbook-rules-a04.md`'s ledger. This task fixes exactly those rows in the rule text after a04 merges; it exists on `main` before the findings do, so no boundary commit is needed between a04's final head and its merge. Review tier by INV-1 (`kind: docs`; the same files as a04). The threat table names every `allowed_files` entry plus the non-path controls; `task-consistency-check.py` C1 to C10 and C7b pass on this file.
+
+## What to do
+
+1. The owned rows: the `<id>\t<class>` rows under the heading `## Owned by dotfiles-T128-playbook-rules-followup-a01` in `.orchestration/acceptance/dotfiles-T128-playbook-rules-a04.md` as read from `origin/main` (Codex Bot P2 threads and local-review findings on a04's final head after its one revise round, each dispositioned on PR #328 as `not-applicable:advisory P2 owned by dotfiles-T128-playbook-rules-followup-a01; evidence=git show origin/main:.orchestration/tasks/dotfiles-T128-playbook-rules-followup-a01.md | grep -n 'item 1'` (the gate's full form once PR #329 lands)). That section is this item's whole definition, closed at a04's acceptance and landed by the boundary after a04's merge; this task dispatches only after that boundary (the dispatch line names the record's hash); a finding outside the section is not owned here, and a missing or empty section at dispatch makes this task a no-op that report.md states (the section is created at the lineage's acceptance, so it does not exist before that). For each row: the rule sentence it names is corrected against the design on `main` (`.orchestration/tasks/dotfiles-T128-regime-v3-a01.md`, read from main) and the thread's text, with one token test per changed sentence in `tests/unit/test_agmsg_orchestration_docs.py` (and the fixture under `tests/fixtures/regime/` when the pinned section changes), in the style of a04's item 7; the RESULT lists each row with `fixed:<sha>`. The `procedure-migration` row (`audit:71eb920:1`) covers every sentence in this task's allowed files that still states the retired gate input (`AUDIT_DISPOSITIONS`, or the `audit-finding:` prose as what the gate reads), since the gate on main reads the acceptance record's JSON `audit_findings` (`{n, reason, evidence}`, PR #329): the step 10 lines the audit named, the task-level audit bullet of the SKILL, the AGENTS.md gate sentence, and the pinned fixture `tests/fixtures/regime/invariants.md` where `tests/unit/test_agmsg_orchestration_docs.py` holds them (the lines on `origin/main` at 26909ee4 and after are pasted in the Change section below); each changed sentence gets its token test as above (amendment 1, the worker's question of 06:50Z).
+2. Nothing else changes: not the Worker Playbook, not the message contract, not any sentence outside the owned rows.
+
+## Validation
+
+- `uv run --no-project python -m unittest tests/unit/test_agmsg_orchestration_docs.py -v` output in the validation file, with the changed tests named and the fixture list.
+- `git diff --numstat origin/main...HEAD` in the validation file (INV-2 caps: at most 15 changed files outside `.orchestration/`, 500 added lines outside `tests/`, 1000 under `tests/`).
+
+## Completion
+
+The PR is ready for the orchestrator's integration when CI is green, the Bot wait of Worker Playbook step 15 is done, the validation file carries the outputs above, and the RESULT names every unresolved Bot thread with `fixed:<sha>` or a proposed `not-applicable:<reason>; evidence=<command>`. A fresh branch `regime/playbook-rules-followup` from `origin/main` after a04 merges, a new PR, `kind: docs`; the orchestrator runs the local review (C-32) on the pushed head and returns its findings with the Bot's in one revise round at most.
+
+## Change (amendment 1, 2026-10-14)
+
+Why: the worker's question (bus 1108, 06:50:50Z): two sentences outside SKILL lines 171 to 178 state the retired gate mechanism (`AUDIT_DISPOSITIONS`, the `audit-finding:` prose as the gate's input), the task-level audit bullet and AGENTS.md's gate sentence, and item 2 forbids sentences outside the owned rows. What changed: item 1 gained one sentence defining the `procedure-migration` row's scope as every such sentence in the allowed files, with the fixture, each with its token test; nothing else. The lines on `origin/main` (c15ba668) that the row now covers, pasted:
+
+```text
+$ git show origin/main:home/dot_agents/skills/agmsg-orchestration/SKILL.md | grep -n 'AUDIT_DISPOSITIONS\|audit-finding'
+90:  - The orchestrator dispositions every `[P0-P3]` finding in the acceptance record, whatever the verdict: exactly one `audit-finding: <n> …` line per finding
+171:    3. Write the acceptance record, summarising the dispositions, with an `audit-finding:` line for every audit finding whatever the verdict (the gate needs
+172:    4. Run the gate: `AUDIT_EVIDENCE=<audit> [AUDIT_DISPOSITIONS=<acceptance record>] AGENT_REVIEWED=1 REVIEW_EVIDENCE=<receipt> ACCEPTANCE_EVIDENCE=<accept
+178:       - `AUDIT_EVIDENCE` must be the task-level file `.orchestration/validation/<task>-audit-<sha7>.md` (the same `<task>` as the feedback JSON); a per-com
+$ git show origin/main:AGENTS.md | grep -n 'AUDIT_DISPOSITIONS'
+44:- Before merging a pull request, follow the integration order in the agmsg-orchestration SKILL's Orchestrator Playbook step 10 and `home/dot_config/claude/ru
+$ git show origin/main:tests/fixtures/regime/invariants.md | grep -n 'AUDIT_DISPOSITIONS\|audit-finding'
+27:  - The orchestrator dispositions every `[P0-P3]` finding in the acceptance record, whatever the verdict: exactly one `audit-finding: <n> …` line per finding
+```
diff --git a/.orchestration/dotfiles-T128-playbook-rules-followup-a01/validation.md b/.orchestration/dotfiles-T128-playbook-rules-followup-a01/validation.md
new file mode 100644
index 00000000..ab4dc2e1
--- /dev/null
+++ b/.orchestration/dotfiles-T128-playbook-rules-followup-a01/validation.md
@@ -0,0 +1,171 @@
+---
+task_id: dotfiles-T128-playbook-rules-followup-a01
+seat: claude-standard-dot-a002
+rule_commit: 7a282f3b
+---
+
+# Validation: dotfiles-T128-playbook-rules-followup-a01
+
+Every command ran from the worktree `.claude/worktrees/worker-f` inside the sandbox, with `MAIN` naming the main checkout and `UV_OFFLINE=1` set (uv cannot reach pypi from the sandbox). The output is verbatim; each block ends with the command's exit status. Captured at `7a282f3b`, before the PR was opened.
+
+Changed tests: `test_dispatches_are_recorded_from_the_bus` (step 6's sentence), `test_the_gate_reads_the_acceptance_record` (step 10.3 and 10.4) and `test_an_incorrect_audit_is_dispositioned_in_audit_findings` (new: the task-level audit bullet and AGENTS.md's gate sentence). Changed fixtures (`test_regime_rule_sections_are_pinned_whole`): `tests/fixtures/regime/orchestrator-step-6.md` and `tests/fixtures/regime/invariants.md`, each in the one changed sentence.
+
+## 1. Task file and task copy
+
+```console
+$ shasum -a 256 "$MAIN/.orchestration/tasks/dotfiles-T128-playbook-rules-followup-a01.md" .orchestration/dotfiles-T128-playbook-rules-followup-a01/task.md | sed "s#$MAIN/##"; cmp "$MAIN/.orchestration/tasks/dotfiles-T128-playbook-rules-followup-a01.md" .orchestration/dotfiles-T128-playbook-rules-followup-a01/task.md && echo byte-identical
+ec415eaf526937fd43907a59fccfc455de117850003ba3d48cd20b065fc5564b  .orchestration/tasks/dotfiles-T128-playbook-rules-followup-a01.md
+ec415eaf526937fd43907a59fccfc455de117850003ba3d48cd20b065fc5564b  .orchestration/dotfiles-T128-playbook-rules-followup-a01/task.md
+byte-identical
+[exit 0]
+```
+
+## 2. Branch and the owned section (item 1's definition)
+
+```console
+$ git log --oneline origin/main..HEAD; git rev-parse origin/main
+7a282f3b docs(agmsg-orchestration): the record before the first dispatch; audit_findings replaces AUDIT_DISPOSITIONS (T703 a04 owner rows)
+c15ba668da20dc2956220077cb0f20054ab352c7
+[exit 0]
+```
+```console
+$ git show origin/main:.orchestration/acceptance/dotfiles-T128-playbook-rules-a04.md | shasum -a 256; git show origin/main:.orchestration/acceptance/dotfiles-T128-playbook-rules-a04.md | awk '/^## Owned by dotfiles-T128-playbook-rules-followup-a01/ {p = 1} p && /^(local|audit):[0-9a-f]{7}:[0-9]+\t/'
+3bfd13d7c9e2b381e3de118b6f717d9025ce2b67f5b2bc08b844d0486613e5ec  -
+local:65a3d71:1	rule-gap
+audit:71eb920:1	procedure-migration (the SKILL step 10.4 gate command still names AUDIT_DISPOSITIONS; from the audit of PR #329's head)
+audit:65a3d71:1	disposition-range
+audit:65a3d71:2	rule-gap
+[exit 0]
+```
+
+## 3. The retired gate input before and after
+
+```console
+$ for f in home/dot_agents/skills/agmsg-orchestration/SKILL.md AGENTS.md tests/fixtures/regime/invariants.md; do echo "== origin/main:$f"; git show "origin/main:$f" | /usr/bin/grep -n "AUDIT_DISPOSITIONS\|audit-finding" | cut -c1-140; echo "== HEAD:$f"; /usr/bin/grep -n "AUDIT_DISPOSITIONS\|audit-finding" "$f" | cut -c1-140; done
+== origin/main:home/dot_agents/skills/agmsg-orchestration/SKILL.md
+90:  - The orchestrator dispositions every `[P0-P3]` finding in the acceptance record, whatever the verdict: exactly one `audit-finding: <n>
+171:    3. Write the acceptance record, summarising the dispositions, with an `audit-finding:` line for every audit finding whatever the ver
+172:    4. Run the gate: `AUDIT_EVIDENCE=<audit> [AUDIT_DISPOSITIONS=<acceptance record>] AGENT_REVIEWED=1 REVIEW_EVIDENCE=<receipt> ACCEPTA
+178:       - `AUDIT_EVIDENCE` must be the task-level file `.orchestration/validation/<task>-audit-<sha7>.md` (the same `<task>` as the feedb
+== HEAD:home/dot_agents/skills/agmsg-orchestration/SKILL.md
+90:  - The orchestrator dispositions every `[P0-P3]` finding in the acceptance record, whatever the verdict, numbered 1..N in the audit's or
+171:    3. Write the acceptance record, summarising the dispositions, with every audit finding dispositioned as the task-level audit bullet 
+== origin/main:AGENTS.md
+44:- Before merging a pull request, follow the integration order in the agmsg-orchestration SKILL's Orchestrator Playbook step 10 and `home/
+== HEAD:AGENTS.md
+== origin/main:tests/fixtures/regime/invariants.md
+27:  - The orchestrator dispositions every `[P0-P3]` finding in the acceptance record, whatever the verdict: exactly one `audit-finding: <n>
+== HEAD:tests/fixtures/regime/invariants.md
+27:  - The orchestrator dispositions every `[P0-P3]` finding in the acceptance record, whatever the verdict, numbered 1..N in the audit's or
+[exit 0]
+```
+```console
+$ git grep -n "RETIRED_AUDIT_DISPOSITIONS_ENV =\|^FAILURE_REASON_MIN_CHARS\|def audit_findings_errors" -- scripts/require-crit-review.py; /usr/bin/grep -n "audit-dispositions" scripts/orchestrator/acceptance-front-matter.py | head -3; /usr/bin/grep -n "is not an existing regular file\|whose .task. is not" scripts/orchestrator/dispatch.sh
+scripts/require-crit-review.py:26:RETIRED_AUDIT_DISPOSITIONS_ENV = "AUDIT_DISPOSITIONS"
+scripts/require-crit-review.py:33:FAILURE_REASON_MIN_CHARS = 20
+scripts/require-crit-review.py:705:def audit_findings_errors(record: dict | None, findings: int) -> list[str]:
+1:"""acceptance-front-matter.py <task> <sweep-json> <pr-worktree> [--ledger <tsv>] [--audit-dispositions <tsv>]
+9:`--audit-dispositions` (`n<TAB>reason<TAB>evidence`), required when the audit summary orch-audit.sh writes beside
+51:    parser.add_argument("--audit-dispositions")
+34:#   (thread 4255272797). A record that is not an existing regular file writable in a
+35:#   writable directory, or whose `task` is not the line's `task_id`, is refused
+[exit 0]
+```
+
+## 4. The Validation command
+
+```console
+$ uv run --no-project python -m unittest tests/unit/test_agmsg_orchestration_docs.py -v
+test_docs_no_longer_name_codex_review_commit (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationForbiddenPhrasesTest.test_docs_no_longer_name_codex_review_commit) ... ok
+test_rule_and_skill_name_worker_seats_not_codex_workers (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationForbiddenPhrasesTest.test_rule_and_skill_name_worker_seats_not_codex_workers) ... ok
+test_rule_drops_the_worker_network_escalation (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationForbiddenPhrasesTest.test_rule_drops_the_worker_network_escalation) ... ok
+test_skill_drops_the_pane_status_gate_and_raw_pane_wakes (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationForbiddenPhrasesTest.test_skill_drops_the_pane_status_gate_and_raw_pane_wakes) ... ok
+test_rule_pointers_name_real_skill_sections (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationRuleTest.test_rule_pointers_name_real_skill_sections) ... ok
+test_rule_states_the_invariants (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationRuleTest.test_rule_states_the_invariants) ... ok
+test_word_budgets (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationRuleTest.test_word_budgets) ... ok
+test_audit_command_lives_only_in_the_task_level_audit_bullet (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationSingleSourceTest.test_audit_command_lives_only_in_the_task_level_audit_bullet) ... ok
+test_codex_agents_points_at_the_worklog_section (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationSingleSourceTest.test_codex_agents_points_at_the_worklog_section) ... ok
+test_contextdb_cli_is_invoked_with_uv_run (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationSingleSourceTest.test_contextdb_cli_is_invoked_with_uv_run) ... ok
+test_skill_masks_evidence_with_a_runnable_command (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationSingleSourceTest.test_skill_masks_evidence_with_a_runnable_command) ... ok
+test_claude_worker_merge_denials_and_prefix_limits_are_documented (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationSkillTest.test_claude_worker_merge_denials_and_prefix_limits_are_documented) ... ok
+test_codex_worker_profile_defaults_to_standard (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationSkillTest.test_codex_worker_profile_defaults_to_standard) ... ok
+test_skill_carries_the_audit_gate_and_bot_wait_mechanics (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationSkillTest.test_skill_carries_the_audit_gate_and_bot_wait_mechanics) ... ok
+test_skill_carries_the_parallel_execution_and_routing_mechanics (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationSkillTest.test_skill_carries_the_parallel_execution_and_routing_mechanics) ... ok
+test_skill_carries_the_registration_and_delivery_mechanics (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationSkillTest.test_skill_carries_the_registration_and_delivery_mechanics) ... ok
+test_skill_carries_the_session_lessons (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationSkillTest.test_skill_carries_the_session_lessons) ... ok
+test_a_design_lands_on_main_before_its_task (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_a_design_lands_on_main_before_its_task) ... ok
+test_a_revise_acceptance_names_the_previous_head_and_a_check (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_a_revise_acceptance_names_the_previous_head_and_a_check) ... ok
+test_a_trust_boundary_task_carries_a_threat_table (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_a_trust_boundary_task_carries_a_threat_table) ... ok
+test_an_incorrect_audit_is_dispositioned_in_audit_findings (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_an_incorrect_audit_is_dispositioned_in_audit_findings) ... ok
+test_bot_fix_rounds_are_capped_and_the_pr_is_ready_first (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_bot_fix_rounds_are_capped_and_the_pr_is_ready_first) ... ok
+test_boundary_merge_sentence_names_the_in_job_decision (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_boundary_merge_sentence_names_the_in_job_decision) ... ok
+test_closed_selector_existence_is_checked_at_acceptance (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_closed_selector_existence_is_checked_at_acceptance) ... ok
+test_code_review_rules_cover_orchestration_records_and_threat_tables (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_code_review_rules_cover_orchestration_records_and_threat_tables) ... ok
+test_counters_bullet_names_owners_not_sources (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_counters_bullet_names_owners_not_sources) ... ok
+test_counters_run_before_every_acceptance_action (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_counters_run_before_every_acceptance_action) ... ok
+test_design_review_runs_in_paired_rounds_with_a_cap (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_design_review_runs_in_paired_rounds_with_a_cap) ... ok
+test_dispatches_are_recorded_from_the_bus (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_dispatches_are_recorded_from_the_bus) ... ok
+test_open_review_body_findings_have_an_identifier (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_open_review_body_findings_have_an_identifier) ... ok
+test_open_third_round_threads_have_an_integration_outcome (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_open_third_round_threads_have_an_integration_outcome) ... ok
+test_orchestration_records_rule_binds_the_bot_review_only (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_orchestration_records_rule_binds_the_bot_review_only) ... ok
+test_pattern_rules_pin_their_safeguards (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_pattern_rules_pin_their_safeguards) ... ok
+test_question_pongs_are_in_the_contract (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_question_pongs_are_in_the_contract) ... ok
+test_regime_rule_sections_are_pinned_whole (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_regime_rule_sections_are_pinned_whole) ... ok
+test_rule_changes_travel_as_task_amendments (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_rule_changes_travel_as_task_amendments) ... ok
+test_shape_is_checked_by_hand_until_the_schema_lands (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_shape_is_checked_by_hand_until_the_schema_lands) ... ok
+test_shape_rules_and_the_decision_sentence_are_pinned (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_shape_rules_and_the_decision_sentence_are_pinned) ... ok
+test_task_file_review_is_one_round_with_a_fixed_stop_condition (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_task_file_review_is_one_round_with_a_fixed_stop_condition) ... ok
+test_the_bot_wait_filters_the_codex_bot (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_the_bot_wait_filters_the_codex_bot) ... ok
+test_the_ci_watch_is_joined_before_the_result (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_the_ci_watch_is_joined_before_the_result) ... ok
+test_the_ci_watcher_survives_the_no_checks_race (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_the_ci_watcher_survives_the_no_checks_race) ... ok
+test_the_gate_reads_the_acceptance_record (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_the_gate_reads_the_acceptance_record) ... ok
+test_threat_table_rows_have_a_fixed_unit (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_threat_table_rows_have_a_fixed_unit) ... ok
+test_threat_table_rule_carries_no_grammar (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_threat_table_rule_carries_no_grammar) ... ok
+test_three_repeats_start_with_a_pasted_correction_search (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_three_repeats_start_with_a_pasted_correction_search) ... ok
+test_workers_commit_inside_the_sandbox (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_workers_commit_inside_the_sandbox) ... ok
+test_workers_open_the_pr_as_a_draft (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_workers_open_the_pr_as_a_draft) ... ok
+
+----------------------------------------------------------------------
+Ran 48 tests in 0.012s
+
+OK
+[exit 0]
+```
+
+## 5. Formatting
+
+```console
+$ prettier --check home/dot_agents/skills/agmsg-orchestration/SKILL.md AGENTS.md tests/fixtures/regime/*.md; ruff format --config ruff.toml --check tests/unit/test_agmsg_orchestration_docs.py
+Checking formatting...
+All matched files use Prettier code style!
+1 file already formatted
+[exit 0]
+```
+
+## 6. The changed tests and fixtures
+
+```console
+$ git diff origin/main...HEAD --stat -- tests; git diff origin/main...HEAD -- tests/unit/test_agmsg_orchestration_docs.py | /usr/bin/grep "^@@\|^+    def \|^ *def test" | cut -c1-140
+ tests/fixtures/regime/invariants.md          |  2 +-
+ tests/fixtures/regime/orchestrator-step-6.md |  2 +-
+ tests/unit/test_agmsg_orchestration_docs.py  | 52 +++++++++++++++++++++++++---
+ 3 files changed, 50 insertions(+), 6 deletions(-)
+@@ -522,7 +522,12 @@ class AgmsgRegimePatternTest(unittest.TestCase):
+@@ -629,11 +634,50 @@ class AgmsgRegimePatternTest(unittest.TestCase):
+     def test_the_gate_reads_the_acceptance_record(self) -> None:
++    def test_an_incorrect_audit_is_dispositioned_in_audit_findings(self) -> None:
+[exit 0]
+```
+
+## 7. Caps (INV-2)
+
+```console
+$ git diff --numstat origin/main...HEAD -- . ':!.orchestration' | awk '{print; f++; if ($3 ~ /^tests\//) t += $1; else x += $1} END {printf "files outside .orchestration: %d (cap 15); added outside tests: %d (cap 500); added under tests: %d (cap 1000)\n", f, x, t}'
+1	1	AGENTS.md
+5	5	home/dot_agents/skills/agmsg-orchestration/SKILL.md
+1	1	tests/fixtures/regime/invariants.md
+1	1	tests/fixtures/regime/orchestrator-step-6.md
+48	4	tests/unit/test_agmsg_orchestration_docs.py
+files outside .orchestration: 5 (cap 15); added outside tests: 6 (cap 500); added under tests: 50 (cap 1000)
+[exit 0]
+```
diff --git a/AGENTS.md b/AGENTS.md
index a0b54678..1a825101 100644
--- a/AGENTS.md
+++ b/AGENTS.md
@@ -41,7 +41,7 @@
 - Agent evidence must contain at least one resolved record. For a finding-free review, add and resolve one review-scope approval record.
 - When the crit CLI or its data is unavailable, save the independent agent review in that same JSON shape (hand-written records are acceptable), mark each record `resolved: true` after addressing it, and reference it from the receipt exactly as crit-exported evidence; the guard validates shape, not provenance.
 - This local evidence is process evidence, not reviewer authentication. Human `CRIT_REVIEWED=1` receipts remain supported.
-- Before merging a pull request, follow the integration order in the agmsg-orchestration SKILL's Orchestrator Playbook step 10 and `home/dot_config/claude/rules/pr-integration.md`: the `scripts/pr-feedback.py` sweep, the task-level audit, the acceptance record, then the gate with `PR_FEEDBACK_EVIDENCE` and `AUDIT_EVIDENCE` (`AUDIT_DISPOSITIONS` for an `incorrect` verdict).
+- Before merging a pull request, follow the integration order in the agmsg-orchestration SKILL's Orchestrator Playbook step 10 and `home/dot_config/claude/rules/pr-integration.md`: the `scripts/pr-feedback.py` sweep, the task-level audit, the acceptance record, then the gate with `PR_FEEDBACK_EVIDENCE`, `AUDIT_EVIDENCE` and `ACCEPTANCE_EVIDENCE` (the record's `audit_findings` disposition an `incorrect` verdict).
 
 ## Audit
 
diff --git a/home/dot_agents/skills/agmsg-orchestration/SKILL.md b/home/dot_agents/skills/agmsg-orchestration/SKILL.md
index 62fc1923..2e706a28 100644
--- a/home/dot_agents/skills/agmsg-orchestration/SKILL.md
+++ b/home/dot_agents/skills/agmsg-orchestration/SKILL.md
@@ -87,7 +87,7 @@ Use this skill for structured multi-agent work where an orchestrator seat assign
     - The gate needs both the transcript file and its non-empty `.last.md` companion.
   - Run either form from a clean tree: the only untracked content in the audited checkout is this task's `.orchestration` evidence that the audit prompt names (task file, report, validation, sandbox file, feedback JSON). Otherwise run it from a dedicated clean checkout, so no other edit can reach the auditor.
   - A new push, including a `gh pr update-branch` merge, needs a new audit of the new head.
-  - The orchestrator dispositions every `[P0-P3]` finding in the acceptance record, whatever the verdict: exactly one `audit-finding: <n> …` line per finding, numbered 1..N in the audit's order of `[P0-P3]` lines. The audit's finding lines may be bulleted; a disposition line may be indented but never starts with a list marker, or the gate skips it. `fixed:<sha>` needs a fresh audit of that sha; otherwise `not-applicable:<reason of at least 20 characters>`. Deferral ("later", a follow-up task, a stopgap or a suppression) is not a disposition. The gate enforces these lines only for an `incorrect` verdict (T68), but a finding under `Verdict: correct` is dispositioned all the same.
+  - The orchestrator dispositions every `[P0-P3]` finding in the acceptance record, whatever the verdict, numbered 1..N in the audit's order of `[P0-P3]` lines (the audit's finding lines may be bulleted). For an `incorrect` verdict the dispositions are the record's JSON `audit_findings`, the only form the gate reads: one `{n, reason, evidence}` entry per finding, `n` the number as a string and `reason` at least 20 characters, written with `scripts/orchestrator/acceptance-front-matter.py --audit-dispositions <tsv>`; an entry never cites a fix, since a fix moves the head and needs its own audit. A finding under `Verdict: correct` is dispositioned all the same, as an `audit-finding: <n> …` line in the record's prose: `fixed:<sha>` with a fresh audit of that sha, otherwise `not-applicable:<reason of at least 20 characters>`. Deferral ("later", a follow-up task, a stopgap or a suppression) is not a disposition.
   - The audit evidence and the PR-feedback JSON quote reviewed content, so mask them with `uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets <files>` before they are committed. The gate compares PR-feedback bodies after the same masking, so masked feedback evidence still matches the live collection (T93, #251).
   - Audit findings are input, never approval; acceptance authority stays with the orchestrator, and each RESULT gets its own acceptance record.
 - Crit is agent-side only for Claude Code and Codex alike, as in `home/dot_config/claude/rules/crit-review.md`: record crit-data evidence (`crit status --json`, `crit comments --all --json <review.json>`) and never open a browser review to ask the user. When Crit data is unavailable, save the independent agent review as the same repo-local JSON list (objects with non-empty string `id`, `body`, `scope` and `resolved: true`, at least one `scope: "review"` or path-bound `line`/`file` record; hand-written records are acceptable because the guard validates shape, not provenance) and reference it from a `review_surface: crit-data` receipt with `reviewer: claude-code`, `claude`, or `codex`, `review_source: <that JSON>`, and `review_outcome: approved` or `addressed`. Run `crit share` or any other publish step only when the user explicitly asks for it. Close a Crit session opened by the Plan Mode hook once its review is done, so no local Crit web server stays resident.
@@ -161,21 +161,21 @@ AGMSG-PONG v1 task_id=<id> status=alive|blocked|question note=<short-note>
 3. Write a task file that includes objective, scope, allowed files, forbidden actions, expected artifacts, validation commands, and max turns. Name the render check as `make render-check`, never the bare `python3 scripts/generate-agent-configs.py --check`, which fails without PyYAML. Ground `allowed_files` by grepping the repository for every touch point the task names (tests that pin call sequences, mirrors, fixtures) before dispatch. Verify every CLI constraint the task asserts by running the real command in a safe form, not by reading `--help`. Presume an auditor finding that contradicts your own review is right until you refute it with evidence. Decide the worker kind from the allowed files before dispatch: a seat never edits the source of its own execution boundary, so a change is routed by the boundary it touches. A change that touches only Claude's boundary goes to a Codex seat: the `claude.permissions`, `claude.sandbox` and `claude.hooks` blocks of `home/dot_agents/agent-config.yaml` (including excludedCommands, allowUnsandboxedCommands, writable roots, network and the PermissionRequest hook), the Claude-rendering parts of `scripts/generate-agent-configs.py`, the rendered `home/.chezmoitemplates/claude-settings-managed.json`, and `home/dot_claude/modify_private_settings.json`. A change that touches only Codex's boundary goes to a Claude seat: `codex.sandbox_workspace_write`, `codex.approval_policy`, the Codex-rendering parts of the renderer, and `home/.chezmoitemplates/codex-config-managed.toml`. A change that touches both, or a shared source the orchestrator cannot split (such as `codex.sandbox_workspace_write.writable_roots`, which also renders into Claude's `allowWrite`), goes to the operator. The orchestrator decides the kind from the diff the task will produce and records it and the chosen worker profile in the task file. The Claude Code auto-mode classifier also refuses a Claude-boundary task on a Claude seat as Self-Modification. A task that edits permgate (`home/dot_agents/permgate-policy.yaml`, `home/dot_local/bin/common/executable_permgate`), the PermissionRequest hook of both seats, goes to the operator; a Codex `security`-profile worker reviews the change before the orchestrator accepts it, per the model-selection rule. `auto` is Claude Code's built-in starting permission mode since 2.1.283. A project-level `defaultMode: auto` (`.claude/settings.json` or `.claude/settings.local.json`) does not take effect, and the session then also ignores the user-level `defaultMode`, so `auto` belongs only in user or managed settings. Before dispatch, read the task's verbatim blocks against each other for contradictions, and state each rule once; a second artifact references the first instead of restating it.
 4. Start or relaunch worker panes only through `herdr-agents` modes. Deliver messages and wakes as in step 6; never use `pane send-text` followed by `send-keys Enter`, because the separate Enter races the TUI composer and fails nondeterministically.
 5. Configure delivery deliberately. `delivery.sh set turn` is useful for turn-end inbox checks; changing delivery mode can kill project watcher processes, so do it before starting long-running project watchers.
-6. Send `AGMSG-TASK v1` with the exact artifact paths and `done_signal=AGMSG-RESULT`. Pass every `send.sh`/`poke.sh` body with `--body-file <path>` (both take it in agmsg v1.5.0), never as a positional argument: a positional `<text>` passes through the caller's own shell first, where a backtick or `$( )` in the body silently executes and vanishes from what arrives (upstream #378). `agmsg-dispatch` is the one exception and takes a single-line, shell-safe positional message. Pick the path by how the recipient is seated, never by inferring pane or agent status: a worker in a `herdr-agents` pane gets `agmsg-dispatch <team> <from> <to> <pane_id> "<message>"` (send, generic wake, `read_at` wait; single-line shell-safe text only), the sanctioned wake path until worker seating writes placement records at launch, because `poke.sh` exits 1 with "no placement record" for a hand-joined member, and a herdr-agents worker gets a record only once it acts from its own pane (upstream `send.sh`/`inbox.sh` record the acting pane, #1109); a spawn-seated member (placement record `run/spawn.*`; `team.sh <team> --json` shows its pane) gets `poke.sh <team> <name> --body-file <path> [--retries N --retry-delay SECONDS --backoff fixed|exponential]`, which types and submits in one call and refuses to type over an in-progress draft (#1321/#1322); a pane-less member gets `send.sh <team> <from> <to> --body-file <path>` and its own delivery mode. Verify delivery via the messages.db `read_at` column. `poke.sh` exit codes: 10 = terminal unreachable, 12 = pane gone or no live agent, 14/15 = refused to type over a changing or unlocatable input box, 13 = the driver has no poke path for this pane (for example a `plain` terminal); where poke.sh's narrow agmsg-message fallback succeeds it exits 0, so 13 means nothing was delivered, and the printed reason names the native channel, asks the caller to claim its own identity first, or reports that the fallback failed. Never retry a 13 as `send.sh` yourself: that overrides the driver's considered refusal and can double-deliver. Seating case: a worker in an unviewed or headless Herdr workspace (no client attached, a small pane rect such as 18x41) makes `poke.sh` exit 14/15 from its TUI input locator; that is a locator refusal, not evidence about the worker's state, so wake it with `agmsg-dispatch` and verify `read_at`. Every dispatch (TASK, ACCEPTANCE, PING) is recorded in the current acceptance record under a `dispatch:` key as the bus line with its read marker; a seat is reported as working only from such a line, and after a context compaction the open TASK list is re-derived from a bus read that is refused when it reaches its limit (`bus-read.sh` exits when the history reaches `BUS_READ_LIMIT`; the orchestrator raises the limit and reads again), never from a default-limited one and never from a read whose truncation went unnoticed. A seated worker idle for 20 minutes since its latest bus event for the task while a dispatchable task exists (INV-10's idle figure; its 30 minutes is the first-push deadline) gets a bus read, then a PING; a longer silent wait is never the answer. `scripts/orchestrator/dispatch.sh` writes the line and `scripts/orchestrator/bus-read.sh` performs the read and prints the minutes since each open task's latest event (both on main since a03c1daa, plan 007 T718); the orchestrator applies the 20-minute figure to the minutes the script prints (the script's own silence flag still uses 30 minutes, a recorded residual of the tools lineage).
+6. Send `AGMSG-TASK v1` with the exact artifact paths and `done_signal=AGMSG-RESULT`. Pass every `send.sh`/`poke.sh` body with `--body-file <path>` (both take it in agmsg v1.5.0), never as a positional argument: a positional `<text>` passes through the caller's own shell first, where a backtick or `$( )` in the body silently executes and vanishes from what arrives (upstream #378). `agmsg-dispatch` is the one exception and takes a single-line, shell-safe positional message. Pick the path by how the recipient is seated, never by inferring pane or agent status: a worker in a `herdr-agents` pane gets `agmsg-dispatch <team> <from> <to> <pane_id> "<message>"` (send, generic wake, `read_at` wait; single-line shell-safe text only), the sanctioned wake path until worker seating writes placement records at launch, because `poke.sh` exits 1 with "no placement record" for a hand-joined member, and a herdr-agents worker gets a record only once it acts from its own pane (upstream `send.sh`/`inbox.sh` record the acting pane, #1109); a spawn-seated member (placement record `run/spawn.*`; `team.sh <team> --json` shows its pane) gets `poke.sh <team> <name> --body-file <path> [--retries N --retry-delay SECONDS --backoff fixed|exponential]`, which types and submits in one call and refuses to type over an in-progress draft (#1321/#1322); a pane-less member gets `send.sh <team> <from> <to> --body-file <path>` and its own delivery mode. Verify delivery via the messages.db `read_at` column. `poke.sh` exit codes: 10 = terminal unreachable, 12 = pane gone or no live agent, 14/15 = refused to type over a changing or unlocatable input box, 13 = the driver has no poke path for this pane (for example a `plain` terminal); where poke.sh's narrow agmsg-message fallback succeeds it exits 0, so 13 means nothing was delivered, and the printed reason names the native channel, asks the caller to claim its own identity first, or reports that the fallback failed. Never retry a 13 as `send.sh` yourself: that overrides the driver's considered refusal and can double-deliver. Seating case: a worker in an unviewed or headless Herdr workspace (no client attached, a small pane rect such as 18x41) makes `poke.sh` exit 14/15 from its TUI input locator; that is a locator refusal, not evidence about the worker's state, so wake it with `agmsg-dispatch` and verify `read_at`. Every dispatch (TASK, ACCEPTANCE, PING) is recorded in the current acceptance record under a `dispatch:` key as the bus line with its read marker, so the orchestrator creates that record, `.orchestration/acceptance/<task>.md`, before the task's first dispatch (`scripts/orchestrator/dispatch.sh` refuses a record that does not exist or that names another task); a seat is reported as working only from such a line, and after a context compaction the open TASK list is re-derived from a bus read that is refused when it reaches its limit (`bus-read.sh` exits when the history reaches `BUS_READ_LIMIT`; the orchestrator raises the limit and reads again), never from a default-limited one and never from a read whose truncation went unnoticed. A seated worker idle for 20 minutes since its latest bus event for the task while a dispatchable task exists (INV-10's idle figure; its 30 minutes is the first-push deadline) gets a bus read, then a PING; a longer silent wait is never the answer. `scripts/orchestrator/dispatch.sh` writes the line and `scripts/orchestrator/bus-read.sh` performs the read and prints the minutes since each open task's latest event (both on main since a03c1daa, plan 007 T718); the orchestrator applies the 20-minute figure to the minutes the script prints (the script's own silence flag still uses 30 minutes, a recorded residual of the tools lineage).
 7. Track `max_turns`. Use `AGMSG-PING` for liveness if a worker stalls.
 8. On `AGMSG-RESULT`, read the task file and every referenced artifact before deciding.
 9. For a RESULT carrying `effects`, verify that every declared effect has the report's stated reverse mapping before acceptance; record any irreversible effect in the acceptance note.
 10. For a RESULT that carries a pull request, integrate in this order. This is the single procedure that the PR integration rule, `AGENTS.md`, the README and the gh-first-workflow skill cite. A `gh pr update-branch` moves the head, so steps 1 to 4 run again on the new head. After an update-branch the orchestrator runs it, the order is CI on the new head, then the sweep, then the audit; an audit started before CI finishes sees incomplete evidence and returns an evidence-only `incorrect`. Select a checkout with git -C <absolute path>, never with cd, which the sandboxed Bash may not honour. After moving the review worktree to the audited head, verify git -C <review> rev-parse HEAD equals that head and git -C <main> symbolic-ref --short HEAD prints main before the audit and the gate.
     1. Sweep the final head's feedback with `scripts/pr-feedback.py <pr> --json .orchestration/validation/<task>-pr-feedback.json` and give every item a `fixed:<commit>` or `not-applicable:<reason>` disposition, leaving none on `failure` or `warning` annotations. Optionally request `@coderabbitai full review` on the final head first; when a CodeRabbit review exists it is swept like any other item, and the gate does not require a bot review. An `open:<thread id>` item from a worker's third Bot round is a sweep item like any other: it becomes `fixed:<sha>` through a revise round that carries its `check=` (a round that counts toward INV-6 like any other), or `not-applicable:<reason>` with a pasted refutation; until one of those exists the PR is not merged, never with the thread open.
     2. Run the task-level audit of that head in the pair or headless form of the task-level audit bullet. It exits nonzero for every verdict other than `correct`. An exit with `Audit verdict: incorrect` is not a failed step: continue to step 3 and disposition its findings. A `blocked` or missing verdict means re-running the audit.
-    3. Write the acceptance record, summarising the dispositions, with an `audit-finding:` line for every audit finding whatever the verdict (the gate needs them, through `AUDIT_DISPOSITIONS`, when it is `incorrect`).
-    4. Run the gate: `AUDIT_EVIDENCE=<audit> [AUDIT_DISPOSITIONS=<acceptance record>] AGENT_REVIEWED=1 REVIEW_EVIDENCE=<receipt> ACCEPTANCE_EVIDENCE=<acceptance record> BASE=origin/main PR_FEEDBACK_EVIDENCE=<json> make require-crit-review`.
+    3. Write the acceptance record, summarising the dispositions, with every audit finding dispositioned as the task-level audit bullet says: for an `incorrect` verdict the record's JSON `audit_findings`, which the gate reads through `ACCEPTANCE_EVIDENCE` (it never reads `AUDIT_DISPOSITIONS`, which is retired).
+    4. Run the gate: `AUDIT_EVIDENCE=<audit> AGENT_REVIEWED=1 REVIEW_EVIDENCE=<receipt> ACCEPTANCE_EVIDENCE=<acceptance record> BASE=origin/main PR_FEEDBACK_EVIDENCE=<json> make require-crit-review`.
        - A `review` sweep item whose body carries a `P0`–`P3` badge is a finding with its own `fixed:<commit>` or `not-applicable:<reason>` disposition, never a container for its inline threads.
        - The sweep covers issue comments, reviews, inline review comments with thread resolution, non-passing check runs, check-run annotations at every level (`notice`, `warning`, `failure`), and commit statuses. A `failure` marked `not-applicable` needs a concrete reason of at least 20 characters.
        - A CodeRabbit full review is optional, at most once on the final head: the plan allows one review per hour and every review event spends one (docs.coderabbit.ai/management/rate-limits).
        - The feedback JSON may be masked with `uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets`, which masks its keys and string values; the gate identifies an item by its source, url, level, path, line and body, and accepts a body or path that is verbatim or exactly that masked form.
        - The gate rejects evidence outside `.orchestration/validation/` or without the `-pr-feedback.json` suffix. It binds `BASE` to the PR's GitHub base before running the collector from that authenticated SHA: an older base must be outside HEAD's first-parent chain, an advanced base must preserve the merge-base with the PR head, and PR branch commits (including `HEAD`) cannot substitute for the base. Evidence must match the local GitHub repository independently of `GH_REPO`, and `fixed:` commits must be in the authenticated GitHub base-to-head range whatever `BASE` is selected.
-       - `AUDIT_EVIDENCE` must be the task-level file `.orchestration/validation/<task>-audit-<sha7>.md` (the same `<task>` as the feedback JSON); a per-commit `audit-<sha>.md` is rejected. Its verdict comes only from the non-empty `<file>.last.md` and must be `correct`, or `incorrect` with `AUDIT_DISPOSITIONS`. PRs that change only `.orchestration/` files need no audit.
+       - `AUDIT_EVIDENCE` must be the task-level file `.orchestration/validation/<task>-audit-<sha7>.md` (the same `<task>` as the feedback JSON); a per-commit `audit-<sha>.md` is rejected. Its verdict comes only from the non-empty `<file>.last.md` and must be `correct`, or `incorrect` with an `audit_findings` entry in the acceptance record for each of its findings. PRs that change only `.orchestration/` files need no audit.
        - A boundary PR (`orchestration/boundary-<date>[-n]`, `.orchestration` files only) skips the gate, the sweep JSON and the audit (with `BASE` set the gate would demand `PR_FEEDBACK_EVIDENCE`); each Bot thread on it still gets a disposition reply and is resolved, and the next boundary commit message names the PR.
     5. After the required checks pass and the threads are resolved, merge with `gh pr merge <pr> --squash --match-head-commit <audited head sha>`, so a newer head can never be merged on the evidence of the audited one. Every seat acts as the machine's one GitHub account, so no approval is required or possible. Who merges is decided by the integration gate and by native denial of merge commands in Codex seats; `herdr-agents` writes the Claude worker deny rules (`Bash(gh pr merge:*)`, `Bash(gh api -X PUT:*)`, `Bash(gh api --method PUT:*)`, `Bash(gh api graphql:*)`) into the worker worktree's `.claude/settings.local.json`, where [deny rules take precedence over allow rules and cover nested subcommands in every permission mode](https://code.claude.com/docs/en/permissions), but a method flag after the path escapes these prefix rules, so the integration gate remains the authority.
     6. Send `AGMSG-ACCEPTANCE` (step 11).
diff --git a/tests/fixtures/regime/invariants.md b/tests/fixtures/regime/invariants.md
index a1360120..5695c3b1 100644
--- a/tests/fixtures/regime/invariants.md
+++ b/tests/fixtures/regime/invariants.md
@@ -24,7 +24,7 @@
     - The gate needs both the transcript file and its non-empty `.last.md` companion.
   - Run either form from a clean tree: the only untracked content in the audited checkout is this task's `.orchestration` evidence that the audit prompt names (task file, report, validation, sandbox file, feedback JSON). Otherwise run it from a dedicated clean checkout, so no other edit can reach the auditor.
   - A new push, including a `gh pr update-branch` merge, needs a new audit of the new head.
-  - The orchestrator dispositions every `[P0-P3]` finding in the acceptance record, whatever the verdict: exactly one `audit-finding: <n> …` line per finding, numbered 1..N in the audit's order of `[P0-P3]` lines. The audit's finding lines may be bulleted; a disposition line may be indented but never starts with a list marker, or the gate skips it. `fixed:<sha>` needs a fresh audit of that sha; otherwise `not-applicable:<reason of at least 20 characters>`. Deferral ("later", a follow-up task, a stopgap or a suppression) is not a disposition. The gate enforces these lines only for an `incorrect` verdict (T68), but a finding under `Verdict: correct` is dispositioned all the same.
+  - The orchestrator dispositions every `[P0-P3]` finding in the acceptance record, whatever the verdict, numbered 1..N in the audit's order of `[P0-P3]` lines (the audit's finding lines may be bulleted). For an `incorrect` verdict the dispositions are the record's JSON `audit_findings`, the only form the gate reads: one `{n, reason, evidence}` entry per finding, `n` the number as a string and `reason` at least 20 characters, written with `scripts/orchestrator/acceptance-front-matter.py --audit-dispositions <tsv>`; an entry never cites a fix, since a fix moves the head and needs its own audit. A finding under `Verdict: correct` is dispositioned all the same, as an `audit-finding: <n> …` line in the record's prose: `fixed:<sha>` with a fresh audit of that sha, otherwise `not-applicable:<reason of at least 20 characters>`. Deferral ("later", a follow-up task, a stopgap or a suppression) is not a disposition.
   - The audit evidence and the PR-feedback JSON quote reviewed content, so mask them with `uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets <files>` before they are committed. The gate compares PR-feedback bodies after the same masking, so masked feedback evidence still matches the live collection (T93, #251).
   - Audit findings are input, never approval; acceptance authority stays with the orchestrator, and each RESULT gets its own acceptance record.
 - Crit is agent-side only for Claude Code and Codex alike, as in `home/dot_config/claude/rules/crit-review.md`: record crit-data evidence (`crit status --json`, `crit comments --all --json <review.json>`) and never open a browser review to ask the user. When Crit data is unavailable, save the independent agent review as the same repo-local JSON list (objects with non-empty string `id`, `body`, `scope` and `resolved: true`, at least one `scope: "review"` or path-bound `line`/`file` record; hand-written records are acceptable because the guard validates shape, not provenance) and reference it from a `review_surface: crit-data` receipt with `reviewer: claude-code`, `claude`, or `codex`, `review_source: <that JSON>`, and `review_outcome: approved` or `addressed`. Run `crit share` or any other publish step only when the user explicitly asks for it. Close a Crit session opened by the Plan Mode hook once its review is done, so no local Crit web server stays resident.
diff --git a/tests/fixtures/regime/orchestrator-step-6.md b/tests/fixtures/regime/orchestrator-step-6.md
index dd36748b..86762df5 100644
--- a/tests/fixtures/regime/orchestrator-step-6.md
+++ b/tests/fixtures/regime/orchestrator-step-6.md
@@ -1 +1 @@
-6. Send `AGMSG-TASK v1` with the exact artifact paths and `done_signal=AGMSG-RESULT`. Pass every `send.sh`/`poke.sh` body with `--body-file <path>` (both take it in agmsg v1.5.0), never as a positional argument: a positional `<text>` passes through the caller's own shell first, where a backtick or `$( )` in the body silently executes and vanishes from what arrives (upstream #378). `agmsg-dispatch` is the one exception and takes a single-line, shell-safe positional message. Pick the path by how the recipient is seated, never by inferring pane or agent status: a worker in a `herdr-agents` pane gets `agmsg-dispatch <team> <from> <to> <pane_id> "<message>"` (send, generic wake, `read_at` wait; single-line shell-safe text only), the sanctioned wake path until worker seating writes placement records at launch, because `poke.sh` exits 1 with "no placement record" for a hand-joined member, and a herdr-agents worker gets a record only once it acts from its own pane (upstream `send.sh`/`inbox.sh` record the acting pane, #1109); a spawn-seated member (placement record `run/spawn.*`; `team.sh <team> --json` shows its pane) gets `poke.sh <team> <name> --body-file <path> [--retries N --retry-delay SECONDS --backoff fixed|exponential]`, which types and submits in one call and refuses to type over an in-progress draft (#1321/#1322); a pane-less member gets `send.sh <team> <from> <to> --body-file <path>` and its own delivery mode. Verify delivery via the messages.db `read_at` column. `poke.sh` exit codes: 10 = terminal unreachable, 12 = pane gone or no live agent, 14/15 = refused to type over a changing or unlocatable input box, 13 = the driver has no poke path for this pane (for example a `plain` terminal); where poke.sh's narrow agmsg-message fallback succeeds it exits 0, so 13 means nothing was delivered, and the printed reason names the native channel, asks the caller to claim its own identity first, or reports that the fallback failed. Never retry a 13 as `send.sh` yourself: that overrides the driver's considered refusal and can double-deliver. Seating case: a worker in an unviewed or headless Herdr workspace (no client attached, a small pane rect such as 18x41) makes `poke.sh` exit 14/15 from its TUI input locator; that is a locator refusal, not evidence about the worker's state, so wake it with `agmsg-dispatch` and verify `read_at`. Every dispatch (TASK, ACCEPTANCE, PING) is recorded in the current acceptance record under a `dispatch:` key as the bus line with its read marker; a seat is reported as working only from such a line, and after a context compaction the open TASK list is re-derived from a bus read that is refused when it reaches its limit (`bus-read.sh` exits when the history reaches `BUS_READ_LIMIT`; the orchestrator raises the limit and reads again), never from a default-limited one and never from a read whose truncation went unnoticed. A seated worker idle for 20 minutes since its latest bus event for the task while a dispatchable task exists (INV-10's idle figure; its 30 minutes is the first-push deadline) gets a bus read, then a PING; a longer silent wait is never the answer. `scripts/orchestrator/dispatch.sh` writes the line and `scripts/orchestrator/bus-read.sh` performs the read and prints the minutes since each open task's latest event (both on main since a03c1daa, plan 007 T718); the orchestrator applies the 20-minute figure to the minutes the script prints (the script's own silence flag still uses 30 minutes, a recorded residual of the tools lineage).
+6. Send `AGMSG-TASK v1` with the exact artifact paths and `done_signal=AGMSG-RESULT`. Pass every `send.sh`/`poke.sh` body with `--body-file <path>` (both take it in agmsg v1.5.0), never as a positional argument: a positional `<text>` passes through the caller's own shell first, where a backtick or `$( )` in the body silently executes and vanishes from what arrives (upstream #378). `agmsg-dispatch` is the one exception and takes a single-line, shell-safe positional message. Pick the path by how the recipient is seated, never by inferring pane or agent status: a worker in a `herdr-agents` pane gets `agmsg-dispatch <team> <from> <to> <pane_id> "<message>"` (send, generic wake, `read_at` wait; single-line shell-safe text only), the sanctioned wake path until worker seating writes placement records at launch, because `poke.sh` exits 1 with "no placement record" for a hand-joined member, and a herdr-agents worker gets a record only once it acts from its own pane (upstream `send.sh`/`inbox.sh` record the acting pane, #1109); a spawn-seated member (placement record `run/spawn.*`; `team.sh <team> --json` shows its pane) gets `poke.sh <team> <name> --body-file <path> [--retries N --retry-delay SECONDS --backoff fixed|exponential]`, which types and submits in one call and refuses to type over an in-progress draft (#1321/#1322); a pane-less member gets `send.sh <team> <from> <to> --body-file <path>` and its own delivery mode. Verify delivery via the messages.db `read_at` column. `poke.sh` exit codes: 10 = terminal unreachable, 12 = pane gone or no live agent, 14/15 = refused to type over a changing or unlocatable input box, 13 = the driver has no poke path for this pane (for example a `plain` terminal); where poke.sh's narrow agmsg-message fallback succeeds it exits 0, so 13 means nothing was delivered, and the printed reason names the native channel, asks the caller to claim its own identity first, or reports that the fallback failed. Never retry a 13 as `send.sh` yourself: that overrides the driver's considered refusal and can double-deliver. Seating case: a worker in an unviewed or headless Herdr workspace (no client attached, a small pane rect such as 18x41) makes `poke.sh` exit 14/15 from its TUI input locator; that is a locator refusal, not evidence about the worker's state, so wake it with `agmsg-dispatch` and verify `read_at`. Every dispatch (TASK, ACCEPTANCE, PING) is recorded in the current acceptance record under a `dispatch:` key as the bus line with its read marker, so the orchestrator creates that record, `.orchestration/acceptance/<task>.md`, before the task's first dispatch (`scripts/orchestrator/dispatch.sh` refuses a record that does not exist or that names another task); a seat is reported as working only from such a line, and after a context compaction the open TASK list is re-derived from a bus read that is refused when it reaches its limit (`bus-read.sh` exits when the history reaches `BUS_READ_LIMIT`; the orchestrator raises the limit and reads again), never from a default-limited one and never from a read whose truncation went unnoticed. A seated worker idle for 20 minutes since its latest bus event for the task while a dispatchable task exists (INV-10's idle figure; its 30 minutes is the first-push deadline) gets a bus read, then a PING; a longer silent wait is never the answer. `scripts/orchestrator/dispatch.sh` writes the line and `scripts/orchestrator/bus-read.sh` performs the read and prints the minutes since each open task's latest event (both on main since a03c1daa, plan 007 T718); the orchestrator applies the 20-minute figure to the minutes the script prints (the script's own silence flag still uses 30 minutes, a recorded residual of the tools lineage).
diff --git a/tests/unit/test_agmsg_orchestration_docs.py b/tests/unit/test_agmsg_orchestration_docs.py
index 656c7f92..b50b9973 100644
--- a/tests/unit/test_agmsg_orchestration_docs.py
+++ b/tests/unit/test_agmsg_orchestration_docs.py
@@ -522,7 +522,12 @@ class AgmsgRegimePatternTest(unittest.TestCase):
         step = self.section(self.section(SKILL.read_text(), "## Orchestrator Playbook"), "\n6. ", "\n7. ")
         for token in (
             "Every dispatch (TASK, ACCEPTANCE, PING) is recorded in the current acceptance record under a "
-            "`dispatch:` key as the bus line with its read marker; a seat is reported as working only from such a "
+            "`dispatch:` key as the bus line with its read marker, "
+            # Row local:65a3d71:1 (the a04 record's owned section): dispatch.sh refuses a missing record, so the rule
+            # says who creates it and when.
+            "so the orchestrator creates that record, `.orchestration/acceptance/<task>.md`, before the task's first "
+            "dispatch (`scripts/orchestrator/dispatch.sh` refuses a record that does not exist or that names another "
+            "task); a seat is reported as working only from such a "
             # The local review of 7771082f: the merged bus-read.sh refuses a read at its limit; nothing reads all.
             "line, and after a context compaction the open TASK list is re-derived from a bus read that is refused "
             "when it reaches its limit (`bus-read.sh` exits when the history reaches `BUS_READ_LIMIT`; the "
@@ -629,11 +634,50 @@ class AgmsgRegimePatternTest(unittest.TestCase):
     def test_the_gate_reads_the_acceptance_record(self) -> None:
         # Plan 007 T703 item 6: the gate reads the record's ledger and `search:` line once gate-evidence-a02 lands.
         step = self.section(self.section(SKILL.read_text(), "## Orchestrator Playbook"), "\n10. ", "\n11. ")
+        # Row audit:71eb920:1 (the a04 record's owned section): the gate retired AUDIT_DISPOSITIONS and reads an
+        # incorrect audit's dispositions from the record's audit_findings, so step 10 no longer names the variable.
+        for token in (
+            "`AUDIT_EVIDENCE=<audit> AGENT_REVIEWED=1 REVIEW_EVIDENCE=<receipt> ACCEPTANCE_EVIDENCE=<acceptance record> "
+            "BASE=origin/main PR_FEEDBACK_EVIDENCE=<json> make require-crit-review`",
+            "with every audit finding dispositioned as the task-level audit bullet says: for an `incorrect` verdict "
+            "the record's JSON `audit_findings`, which the gate reads through `ACCEPTANCE_EVIDENCE` (it never reads "
+            "`AUDIT_DISPOSITIONS`, which is retired).",
+            "must be `correct`, or `incorrect` with an `audit_findings` entry in the acceptance record for each of its "
+            "findings.",
+        ):
+            with self.subTest(token=token[:40]):
+                self.assertIn(token, step)
+        for stale in ("[AUDIT_DISPOSITIONS=", "through `AUDIT_DISPOSITIONS`", "`incorrect` with `AUDIT_DISPOSITIONS`"):
+            with self.subTest(stale=stale):
+                self.assertNotIn(stale, step)
+
+    def test_an_incorrect_audit_is_dispositioned_in_audit_findings(self) -> None:
+        # Row audit:71eb920:1, amendment 1: the task-level audit bullet and AGENTS.md's gate sentence named the retired
+        # gate input (the audit-finding: prose the gate read through AUDIT_DISPOSITIONS); the gate reads audit_findings.
+        bullet = self.section(
+            self.invariants(), "\n  - The orchestrator dispositions every `[P0-P3]` finding", "\n  - "
+        )
+        for token in (
+            "For an `incorrect` verdict the dispositions are the record's JSON `audit_findings`, the only form the gate "
+            "reads: one `{n, reason, evidence}` entry per finding, `n` the number as a string and `reason` at least 20 "
+            "characters, written with `scripts/orchestrator/acceptance-front-matter.py --audit-dispositions <tsv>`; an "
+            "entry never cites a fix, since a fix moves the head and needs its own audit.",
+            "A finding under `Verdict: correct` is dispositioned all the same, as an `audit-finding: <n> …` line in the "
+            "record's prose: `fixed:<sha>` with a fresh audit of that sha, otherwise `not-applicable:<reason of at "
+            "least 20 characters>`.",
+        ):
+            with self.subTest(token=token[:40]):
+                self.assertIn(token, bullet)
+        for stale in ("The gate enforces these lines only for an `incorrect` verdict", "or the gate skips it"):
+            with self.subTest(stale=stale):
+                self.assertNotIn(stale, bullet)
+        agents = (ROOT / "AGENTS.md").read_text()
         self.assertIn(
-            "REVIEW_EVIDENCE=<receipt> ACCEPTANCE_EVIDENCE=<acceptance record> BASE=origin/main "
-            "PR_FEEDBACK_EVIDENCE=<json> make require-crit-review",
-            step,
+            "then the gate with `PR_FEEDBACK_EVIDENCE`, `AUDIT_EVIDENCE` and `ACCEPTANCE_EVIDENCE` (the record's "
+            "`audit_findings` disposition an `incorrect` verdict).",
+            agents,
         )
+        self.assertNotIn("`AUDIT_DISPOSITIONS` for an `incorrect` verdict", agents)
 
 
 class AgmsgOrchestrationSingleSourceTest(unittest.TestCase):

 succeeded in 410ms:
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
    61	1. The owned rows: the `<id>\t<class>` rows under the heading `## Owned by dotfiles-T128-playbook-rules-followup-a01` in `.orchestration/acceptance/dotfiles-T128-playbook-rules-a04.md` as read from `origin/main` (Codex Bot P2 threads and local-review findings on a04's final head after its one revise round, each dispositioned on PR #328 as `not-applicable:advisory P2 owned by dotfiles-T128-playbook-rules-followup-a01; evidence=git show origin/main:.orchestration/tasks/dotfiles-T128-playbook-rules-followup-a01.md | grep -n 'item 1'` (the gate's full form once PR #329 lands)). That section is this item's whole definition, closed at a04's acceptance and landed by the boundary after a04's merge; this task dispatches only after that boundary (the dispatch line names the record's hash); a finding outside the section is not owned here, and a missing or empty section at dispatch makes this task a no-op that report.md states (the section is created at the lineage's acceptance, so it does not exist before that). For each row: the rule sentence it names is corrected against the design on `main` (`.orchestration/tasks/dotfiles-T128-regime-v3-a01.md`, read from main) and the thread's text, with one token test per changed sentence in `tests/unit/test_agmsg_orchestration_docs.py` (and the fixture under `tests/fixtures/regime/` when the pinned section changes), in the style of a04's item 7; the RESULT lists each row with `fixed:<sha>`. The `procedure-migration` row (`audit:71eb920:1`) covers every sentence in this task's allowed files that still states the retired gate input (`AUDIT_DISPOSITIONS`, or the `audit-finding:` prose as what the gate reads), since the gate on main reads the acceptance record's JSON `audit_findings` (`{n, reason, evidence}`, PR #329): the step 10 lines the audit named, the task-level audit bullet of the SKILL, the AGENTS.md gate sentence, and the pinned fixture `tests/fixtures/regime/invariants.md` where `tests/unit/test_agmsg_orchestration_docs.py` holds them (the lines on `origin/main` at 26909ee4 and after are pasted in the Change section below); each changed sentence gets its token test as above (amendment 1, the worker's question of 06:50Z).
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
    72	
    73	## Change (amendment 1, 2026-10-14)
    74	
    75	Why: the worker's question (bus 1108, 06:50:50Z): two sentences outside SKILL lines 171 to 178 state the retired gate mechanism (`AUDIT_DISPOSITIONS`, the `audit-finding:` prose as the gate's input), the task-level audit bullet and AGENTS.md's gate sentence, and item 2 forbids sentences outside the owned rows. What changed: item 1 gained one sentence defining the `procedure-migration` row's scope as every such sentence in the allowed files, with the fixture, each with its token test; nothing else. The lines on `origin/main` (c15ba668) that the row now covers, pasted:
    76	
    77	```text
    78	$ git show origin/main:home/dot_agents/skills/agmsg-orchestration/SKILL.md | grep -n 'AUDIT_DISPOSITIONS\|audit-finding'
    79	90:  - The orchestrator dispositions every `[P0-P3]` finding in the acceptance record, whatever the verdict: exactly one `audit-finding: <n> …` line per finding
    80	171:    3. Write the acceptance record, summarising the dispositions, with an `audit-finding:` line for every audit finding whatever the verdict (the gate needs
    81	172:    4. Run the gate: `AUDIT_EVIDENCE=<audit> [AUDIT_DISPOSITIONS=<acceptance record>] AGENT_REVIEWED=1 REVIEW_EVIDENCE=<receipt> ACCEPTANCE_EVIDENCE=<accept
    82	178:       - `AUDIT_EVIDENCE` must be the task-level file `.orchestration/validation/<task>-audit-<sha7>.md` (the same `<task>` as the feedback JSON); a per-com
    83	$ git show origin/main:AGENTS.md | grep -n 'AUDIT_DISPOSITIONS'
    84	44:- Before merging a pull request, follow the integration order in the agmsg-orchestration SKILL's Orchestrator Playbook step 10 and `home/dot_config/claude/ru
    85	$ git show origin/main:tests/fixtures/regime/invariants.md | grep -n 'AUDIT_DISPOSITIONS\|audit-finding'
    86	27:  - The orchestrator dispositions every `[P0-P3]` finding in the acceptance record, whatever the verdict: exactly one `audit-finding: <n> …` line per finding
    87	```
     1	---
     2	task_id: dotfiles-T128-playbook-rules-followup-a01
     3	seat: claude-standard-dot-a002
     4	branch: regime/playbook-rules-followup
     5	base: c15ba668da20dc2956220077cb0f20054ab352c7
     6	rule_commit: 7a282f3b
     7	task_sha256: ec415eaf526937fd43907a59fccfc455de117850003ba3d48cd20b065fc5564b
     8	---
     9	
    10	# Report: dotfiles-T128-playbook-rules-followup-a01
    11	
    12	- Seat: `claude-standard-dot-a002` in `.claude/worktrees/worker-f`, on a fresh branch `regime/playbook-rules-followup` from `origin/main` `c15ba668`. The task-checkers branch stays as it is.
    13	- Task file: amendment 1, sha256 `ec415eaf…`, copied byte-identical to `.orchestration/dotfiles-T128-playbook-rules-followup-a01/task.md` (validation §1).
    14	- Round 1 was dispatched at 06:47:41Z. At 06:50Z I asked whether two more sentences belonged to the `procedure-migration` row: the task-level audit bullet and AGENTS.md:44, which both state the retired gate input outside SKILL lines 171 to 178. Amendment 1 (07:03:44Z) put them in the row. Nothing was pushed before it.
    15	
    16	## The owned rows
    17	
    18	The `## Owned by dotfiles-T128-playbook-rules-followup-a01` section of `.orchestration/acceptance/dotfiles-T128-playbook-rules-a04.md` on `origin/main` (sha256 `3bfd13d7…`) holds four rows (validation §2):
    19	
    20	| Row | Class | What changed (`7a282f3b`) |
    21	|---|---|---|
    22	| `local:65a3d71:1` | rule-gap | Orchestrator Playbook step 6: "so the orchestrator creates that record, `.orchestration/acceptance/<task>.md`, before the task's first dispatch (`scripts/orchestrator/dispatch.sh` refuses a record that does not exist or that names another task)". `dispatch.sh` refuses a record that is not an existing regular file or whose `task` is another task (its header, validation §3). The pinned fixture `orchestrator-step-6.md` changes with it. |
    23	| `audit:65a3d71:2` | rule-gap | The same finding as `local:65a3d71:1`, as the audit of `65a3d71b` raised it, so it is fixed by the same sentence. |
    24	| `audit:71eb920:1` | procedure-migration | Every sentence in the allowed files that still stated the retired gate input (amendment 1); the gate on `main` reads the record's JSON `audit_findings` and only reports `AUDIT_DISPOSITIONS` as retired (validation §3). The changed sentences are listed below the table. |
    25	| `audit:65a3d71:1` | disposition-range | No rule sentence: the finding was a sweep-table disposition (`fixed:a03c1daa` outside base..head), corrected in a04's sweep at 14:41Z. Nothing changes for it. |
    26	
    27	The `procedure-migration` row changed these sentences:
    28	
    29	- **The task-level audit bullet (invariants section):**
    30	  - An `incorrect` verdict is dispositioned in `audit_findings`, the only form the gate reads: one `{n, reason, evidence}` entry per finding, `n` a string, `reason` at least 20 characters. The entries are written with `acceptance-front-matter.py --audit-dispositions`, and an entry never cites a fix.
    31	  - A `Verdict: correct` finding keeps its `audit-finding: <n> …` prose line.
    32	  - The pinned fixture `invariants.md` changes with it.
    33	- **Step 10.3:** it now points to that bullet.
    34	- **Step 10.4:** the gate command drops `[AUDIT_DISPOSITIONS=<acceptance record>]`, and the `AUDIT_EVIDENCE` bullet now asks for an `audit_findings` entry per finding.
    35	- **AGENTS.md:44:** the gate takes `PR_FEEDBACK_EVIDENCE`, `AUDIT_EVIDENCE` and `ACCEPTANCE_EVIDENCE`.
    36	
    37	Each changed sentence has a token test, and the superseded forms are asserted absent:
    38	
    39	- `test_dispatches_are_recorded_from_the_bus`;
    40	- `test_the_gate_reads_the_acceptance_record`;
    41	- `test_an_incorrect_audit_is_dispositioned_in_audit_findings` (new).
    42	
    43	The documentation module runs 48 tests OK (validation §4).
    44	
    45	## Caps and checks
    46	
    47	- **INV-2** (validation §7): 5 files outside `.orchestration/`, 6 added lines outside `tests/` and 50 added lines under `tests/`.
    48	- **Formatting:** prettier and `ruff format --check` are clean.
    49	- **`ruff check`:** reports the module's implicit-concatenation style (ISC004) on the new tuples as on its existing ones, 12 against 7 on `origin/main`. CI runs only the format check.
    50	
    51	## CI and the Bot
    52	
    53	In the RESULT. The Bot reviews once, at PR open.
    54	
    55	## Not done, or outside scope
    56	
    57	- Understand-Anything hook: did not fire. plan-mode-used: no.
    58	- cost: n/a (the runtime exposes no session figures to the seat).
     1	---
     2	task_id: dotfiles-T128-playbook-rules-followup-a01
     3	seat: claude-standard-dot-a002
     4	rule_commit: 7a282f3b
     5	---
     6	
     7	# Validation: dotfiles-T128-playbook-rules-followup-a01
     8	
     9	Every command ran from the worktree `.claude/worktrees/worker-f` inside the sandbox, with `MAIN` naming the main checkout and `UV_OFFLINE=1` set (uv cannot reach pypi from the sandbox). The output is verbatim; each block ends with the command's exit status. Captured at `7a282f3b`, before the PR was opened.
    10	
    11	Changed tests: `test_dispatches_are_recorded_from_the_bus` (step 6's sentence), `test_the_gate_reads_the_acceptance_record` (step 10.3 and 10.4) and `test_an_incorrect_audit_is_dispositioned_in_audit_findings` (new: the task-level audit bullet and AGENTS.md's gate sentence). Changed fixtures (`test_regime_rule_sections_are_pinned_whole`): `tests/fixtures/regime/orchestrator-step-6.md` and `tests/fixtures/regime/invariants.md`, each in the one changed sentence.
    12	
    13	## 1. Task file and task copy
    14	
    15	```console
    16	$ shasum -a 256 "$MAIN/.orchestration/tasks/dotfiles-T128-playbook-rules-followup-a01.md" .orchestration/dotfiles-T128-playbook-rules-followup-a01/task.md | sed "s#$MAIN/##"; cmp "$MAIN/.orchestration/tasks/dotfiles-T128-playbook-rules-followup-a01.md" .orchestration/dotfiles-T128-playbook-rules-followup-a01/task.md && echo byte-identical
    17	ec415eaf526937fd43907a59fccfc455de117850003ba3d48cd20b065fc5564b  .orchestration/tasks/dotfiles-T128-playbook-rules-followup-a01.md
    18	ec415eaf526937fd43907a59fccfc455de117850003ba3d48cd20b065fc5564b  .orchestration/dotfiles-T128-playbook-rules-followup-a01/task.md
    19	byte-identical
    20	[exit 0]
    21	```
    22	
    23	## 2. Branch and the owned section (item 1's definition)
    24	
    25	```console
    26	$ git log --oneline origin/main..HEAD; git rev-parse origin/main
    27	7a282f3b docs(agmsg-orchestration): the record before the first dispatch; audit_findings replaces AUDIT_DISPOSITIONS (T703 a04 owner rows)
    28	c15ba668da20dc2956220077cb0f20054ab352c7
    29	[exit 0]
    30	```
    31	```console
    32	$ git show origin/main:.orchestration/acceptance/dotfiles-T128-playbook-rules-a04.md | shasum -a 256; git show origin/main:.orchestration/acceptance/dotfiles-T128-playbook-rules-a04.md | awk '/^## Owned by dotfiles-T128-playbook-rules-followup-a01/ {p = 1} p && /^(local|audit):[0-9a-f]{7}:[0-9]+\t/'
    33	3bfd13d7c9e2b381e3de118b6f717d9025ce2b67f5b2bc08b844d0486613e5ec  -
    34	local:65a3d71:1	rule-gap
    35	audit:71eb920:1	procedure-migration (the SKILL step 10.4 gate command still names AUDIT_DISPOSITIONS; from the audit of PR #329's head)
    36	audit:65a3d71:1	disposition-range
    37	audit:65a3d71:2	rule-gap
    38	[exit 0]
    39	```
    40	
    41	## 3. The retired gate input before and after
    42	
    43	```console
    44	$ for f in home/dot_agents/skills/agmsg-orchestration/SKILL.md AGENTS.md tests/fixtures/regime/invariants.md; do echo "== origin/main:$f"; git show "origin/main:$f" | /usr/bin/grep -n "AUDIT_DISPOSITIONS\|audit-finding" | cut -c1-140; echo "== HEAD:$f"; /usr/bin/grep -n "AUDIT_DISPOSITIONS\|audit-finding" "$f" | cut -c1-140; done
    45	== origin/main:home/dot_agents/skills/agmsg-orchestration/SKILL.md
    46	90:  - The orchestrator dispositions every `[P0-P3]` finding in the acceptance record, whatever the verdict: exactly one `audit-finding: <n>
    47	171:    3. Write the acceptance record, summarising the dispositions, with an `audit-finding:` line for every audit finding whatever the ver
    48	172:    4. Run the gate: `AUDIT_EVIDENCE=<audit> [AUDIT_DISPOSITIONS=<acceptance record>] AGENT_REVIEWED=1 REVIEW_EVIDENCE=<receipt> ACCEPTA
    49	178:       - `AUDIT_EVIDENCE` must be the task-level file `.orchestration/validation/<task>-audit-<sha7>.md` (the same `<task>` as the feedb
    50	== HEAD:home/dot_agents/skills/agmsg-orchestration/SKILL.md
    51	90:  - The orchestrator dispositions every `[P0-P3]` finding in the acceptance record, whatever the verdict, numbered 1..N in the audit's or
    52	171:    3. Write the acceptance record, summarising the dispositions, with every audit finding dispositioned as the task-level audit bullet 
    53	== origin/main:AGENTS.md
    54	44:- Before merging a pull request, follow the integration order in the agmsg-orchestration SKILL's Orchestrator Playbook step 10 and `home/
    55	== HEAD:AGENTS.md
    56	== origin/main:tests/fixtures/regime/invariants.md
    57	27:  - The orchestrator dispositions every `[P0-P3]` finding in the acceptance record, whatever the verdict: exactly one `audit-finding: <n>
    58	== HEAD:tests/fixtures/regime/invariants.md
    59	27:  - The orchestrator dispositions every `[P0-P3]` finding in the acceptance record, whatever the verdict, numbered 1..N in the audit's or
    60	[exit 0]
    61	```
    62	```console
    63	$ git grep -n "RETIRED_AUDIT_DISPOSITIONS_ENV =\|^FAILURE_REASON_MIN_CHARS\|def audit_findings_errors" -- scripts/require-crit-review.py; /usr/bin/grep -n "audit-dispositions" scripts/orchestrator/acceptance-front-matter.py | head -3; /usr/bin/grep -n "is not an existing regular file\|whose .task. is not" scripts/orchestrator/dispatch.sh
    64	scripts/require-crit-review.py:26:RETIRED_AUDIT_DISPOSITIONS_ENV = "AUDIT_DISPOSITIONS"
    65	scripts/require-crit-review.py:33:FAILURE_REASON_MIN_CHARS = 20
    66	scripts/require-crit-review.py:705:def audit_findings_errors(record: dict | None, findings: int) -> list[str]:
    67	1:"""acceptance-front-matter.py <task> <sweep-json> <pr-worktree> [--ledger <tsv>] [--audit-dispositions <tsv>]
    68	9:`--audit-dispositions` (`n<TAB>reason<TAB>evidence`), required when the audit summary orch-audit.sh writes beside
    69	51:    parser.add_argument("--audit-dispositions")
    70	34:#   (thread 4255272797). A record that is not an existing regular file writable in a
    71	35:#   writable directory, or whose `task` is not the line's `task_id`, is refused
    72	[exit 0]
    73	```
    74	
    75	## 4. The Validation command
    76	
    77	```console
    78	$ uv run --no-project python -m unittest tests/unit/test_agmsg_orchestration_docs.py -v
    79	test_docs_no_longer_name_codex_review_commit (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationForbiddenPhrasesTest.test_docs_no_longer_name_codex_review_commit) ... ok
    80	test_rule_and_skill_name_worker_seats_not_codex_workers (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationForbiddenPhrasesTest.test_rule_and_skill_name_worker_seats_not_codex_workers) ... ok
    81	test_rule_drops_the_worker_network_escalation (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationForbiddenPhrasesTest.test_rule_drops_the_worker_network_escalation) ... ok
    82	test_skill_drops_the_pane_status_gate_and_raw_pane_wakes (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationForbiddenPhrasesTest.test_skill_drops_the_pane_status_gate_and_raw_pane_wakes) ... ok
    83	test_rule_pointers_name_real_skill_sections (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationRuleTest.test_rule_pointers_name_real_skill_sections) ... ok
    84	test_rule_states_the_invariants (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationRuleTest.test_rule_states_the_invariants) ... ok
    85	test_word_budgets (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationRuleTest.test_word_budgets) ... ok
    86	test_audit_command_lives_only_in_the_task_level_audit_bullet (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationSingleSourceTest.test_audit_command_lives_only_in_the_task_level_audit_bullet) ... ok
    87	test_codex_agents_points_at_the_worklog_section (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationSingleSourceTest.test_codex_agents_points_at_the_worklog_section) ... ok
    88	test_contextdb_cli_is_invoked_with_uv_run (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationSingleSourceTest.test_contextdb_cli_is_invoked_with_uv_run) ... ok
    89	test_skill_masks_evidence_with_a_runnable_command (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationSingleSourceTest.test_skill_masks_evidence_with_a_runnable_command) ... ok
    90	test_claude_worker_merge_denials_and_prefix_limits_are_documented (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationSkillTest.test_claude_worker_merge_denials_and_prefix_limits_are_documented) ... ok
    91	test_codex_worker_profile_defaults_to_standard (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationSkillTest.test_codex_worker_profile_defaults_to_standard) ... ok
    92	test_skill_carries_the_audit_gate_and_bot_wait_mechanics (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationSkillTest.test_skill_carries_the_audit_gate_and_bot_wait_mechanics) ... ok
    93	test_skill_carries_the_parallel_execution_and_routing_mechanics (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationSkillTest.test_skill_carries_the_parallel_execution_and_routing_mechanics) ... ok
    94	test_skill_carries_the_registration_and_delivery_mechanics (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationSkillTest.test_skill_carries_the_registration_and_delivery_mechanics) ... ok
    95	test_skill_carries_the_session_lessons (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationSkillTest.test_skill_carries_the_session_lessons) ... ok
    96	test_a_design_lands_on_main_before_its_task (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_a_design_lands_on_main_before_its_task) ... ok
    97	test_a_revise_acceptance_names_the_previous_head_and_a_check (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_a_revise_acceptance_names_the_previous_head_and_a_check) ... ok
    98	test_a_trust_boundary_task_carries_a_threat_table (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_a_trust_boundary_task_carries_a_threat_table) ... ok
    99	test_an_incorrect_audit_is_dispositioned_in_audit_findings (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_an_incorrect_audit_is_dispositioned_in_audit_findings) ... ok
   100	test_bot_fix_rounds_are_capped_and_the_pr_is_ready_first (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_bot_fix_rounds_are_capped_and_the_pr_is_ready_first) ... ok
   101	test_boundary_merge_sentence_names_the_in_job_decision (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_boundary_merge_sentence_names_the_in_job_decision) ... ok
   102	test_closed_selector_existence_is_checked_at_acceptance (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_closed_selector_existence_is_checked_at_acceptance) ... ok
   103	test_code_review_rules_cover_orchestration_records_and_threat_tables (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_code_review_rules_cover_orchestration_records_and_threat_tables) ... ok
   104	test_counters_bullet_names_owners_not_sources (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_counters_bullet_names_owners_not_sources) ... ok
   105	test_counters_run_before_every_acceptance_action (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_counters_run_before_every_acceptance_action) ... ok
   106	test_design_review_runs_in_paired_rounds_with_a_cap (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_design_review_runs_in_paired_rounds_with_a_cap) ... ok
   107	test_dispatches_are_recorded_from_the_bus (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_dispatches_are_recorded_from_the_bus) ... ok
   108	test_open_review_body_findings_have_an_identifier (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_open_review_body_findings_have_an_identifier) ... ok
   109	test_open_third_round_threads_have_an_integration_outcome (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_open_third_round_threads_have_an_integration_outcome) ... ok
   110	test_orchestration_records_rule_binds_the_bot_review_only (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_orchestration_records_rule_binds_the_bot_review_only) ... ok
   111	test_pattern_rules_pin_their_safeguards (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_pattern_rules_pin_their_safeguards) ... ok
   112	test_question_pongs_are_in_the_contract (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_question_pongs_are_in_the_contract) ... ok
   113	test_regime_rule_sections_are_pinned_whole (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_regime_rule_sections_are_pinned_whole) ... ok
   114	test_rule_changes_travel_as_task_amendments (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_rule_changes_travel_as_task_amendments) ... ok
   115	test_shape_is_checked_by_hand_until_the_schema_lands (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_shape_is_checked_by_hand_until_the_schema_lands) ... ok
   116	test_shape_rules_and_the_decision_sentence_are_pinned (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_shape_rules_and_the_decision_sentence_are_pinned) ... ok
   117	test_task_file_review_is_one_round_with_a_fixed_stop_condition (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_task_file_review_is_one_round_with_a_fixed_stop_condition) ... ok
   118	test_the_bot_wait_filters_the_codex_bot (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_the_bot_wait_filters_the_codex_bot) ... ok
   119	test_the_ci_watch_is_joined_before_the_result (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_the_ci_watch_is_joined_before_the_result) ... ok
   120	test_the_ci_watcher_survives_the_no_checks_race (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_the_ci_watcher_survives_the_no_checks_race) ... ok
   121	test_the_gate_reads_the_acceptance_record (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_the_gate_reads_the_acceptance_record) ... ok
   122	test_threat_table_rows_have_a_fixed_unit (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_threat_table_rows_have_a_fixed_unit) ... ok
   123	test_threat_table_rule_carries_no_grammar (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_threat_table_rule_carries_no_grammar) ... ok
   124	test_three_repeats_start_with_a_pasted_correction_search (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_three_repeats_start_with_a_pasted_correction_search) ... ok
   125	test_workers_commit_inside_the_sandbox (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_workers_commit_inside_the_sandbox) ... ok
   126	test_workers_open_the_pr_as_a_draft (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_workers_open_the_pr_as_a_draft) ... ok
   127	
   128	----------------------------------------------------------------------
   129	Ran 48 tests in 0.012s
   130	
   131	OK
   132	[exit 0]
   133	```
   134	
   135	## 5. Formatting
   136	
   137	```console
   138	$ prettier --check home/dot_agents/skills/agmsg-orchestration/SKILL.md AGENTS.md tests/fixtures/regime/*.md; ruff format --config ruff.toml --check tests/unit/test_agmsg_orchestration_docs.py
   139	Checking formatting...
   140	All matched files use Prettier code style!
   141	1 file already formatted
   142	[exit 0]
   143	```
   144	
   145	## 6. The changed tests and fixtures
   146	
   147	```console
   148	$ git diff origin/main...HEAD --stat -- tests; git diff origin/main...HEAD -- tests/unit/test_agmsg_orchestration_docs.py | /usr/bin/grep "^@@\|^+    def \|^ *def test" | cut -c1-140
   149	 tests/fixtures/regime/invariants.md          |  2 +-
   150	 tests/fixtures/regime/orchestrator-step-6.md |  2 +-
   151	 tests/unit/test_agmsg_orchestration_docs.py  | 52 +++++++++++++++++++++++++---
   152	 3 files changed, 50 insertions(+), 6 deletions(-)
   153	@@ -522,7 +522,12 @@ class AgmsgRegimePatternTest(unittest.TestCase):
   154	@@ -629,11 +634,50 @@ class AgmsgRegimePatternTest(unittest.TestCase):
   155	     def test_the_gate_reads_the_acceptance_record(self) -> None:
   156	+    def test_an_incorrect_audit_is_dispositioned_in_audit_findings(self) -> None:
   157	[exit 0]
   158	```
   159	
   160	## 7. Caps (INV-2)
   161	
   162	```console
   163	$ git diff --numstat origin/main...HEAD -- . ':!.orchestration' | awk '{print; f++; if ($3 ~ /^tests\//) t += $1; else x += $1} END {printf "files outside .orchestration: %d (cap 15); added outside tests: %d (cap 500); added under tests: %d (cap 1000)\n", f, x, t}'
   164	1	1	AGENTS.md
   165	5	5	home/dot_agents/skills/agmsg-orchestration/SKILL.md
   166	1	1	tests/fixtures/regime/invariants.md
   167	1	1	tests/fixtures/regime/orchestrator-step-6.md
   168	48	4	tests/unit/test_agmsg_orchestration_docs.py
   169	files outside .orchestration: 5 (cap 15); added outside tests: 6 (cap 500); added under tests: 50 (cap 1000)
   170	[exit 0]
   171	```
     1	---
     2	task_id: dotfiles-T128-playbook-rules-followup-a01
     3	seat: claude-standard-dot-a002
     4	permission_gated_commands: see the table
     5	---
     6	
     7	# Sandbox record: dotfiles-T128-playbook-rules-followup-a01
     8	
     9	- Period: from the AGMSG-TASK (2026-10-14T06:47:41Z) to the RESULT.
    10	- These ran inside the sandbox:
    11	  - the HTTPS `git fetch` and `git push`;
    12	  - the branch, the edits, the task copy and the commits;
    13	  - every test and format run, with `UV_OFFLINE=1`, since uv cannot reach pypi from the sandbox.
    14	- No local mutation was chained onto a call that ran outside the sandbox.
    15	
    16	Calls outside the sandbox: `gh` through the permission gate (`dangerouslyDisableSandbox`; `gh` fails TLS inside the sandbox) and `agmsg-dispatch` through `excludedCommands`.
    17	
    18	| # | Command | Step 4 case |
    19	|--:|---|---|
    20	| 1 | `agmsg-dispatch … AGMSG-PONG v1 task_id=dotfiles-T128-playbook-rules-followup-a01 status=question …` (06:50Z, the scope of the procedure-migration row) | `agmsg-dispatch` |
    21	| 2 | `agmsg-dispatch … AGMSG-PONG v1 … status=alive note=working…` (06:53Z) | `agmsg-dispatch` |
    22	| 3 | `gh pr create --draft …` | `gh` |
    23	| 4 | `gh pr ready <n>` | `gh` |
    24	| 5 | Bot wait from the ready (background; `gh api` reads every 30 seconds) | `gh` |
    25	| 6 | `gh pr checks <n> --watch` (exit status joined) | `gh` |
    26	| 7 | `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T128-playbook-rules-followup-a01 …` | `agmsg-dispatch` |
     1	---
     2	{
     3	  "format": 1,
     4	  "task": "dotfiles-T128-playbook-rules-followup-a01",
     5	  "head": "3a8f809b36944b0cb778da53104f9b3c54f67355",
     6	  "pr": 354,
     7	  "ledger": [],
     8	  "searches": [],
     9	  "audit_findings": []
    10	}
    11	---
    12	
    13	# Acceptance record: dotfiles-T128-playbook-rules-followup-a01 (the owner task of T703 a04's residual rows in the agmsg-orchestration SKILL; plan 017; Claude seat a002 in worker-f)
    14	
    15	- 2026-10-13 10:19Z task text written by the orchestrator seat; pair-confirmed by the owners review (`dotfiles-T128-followup-owners-review-a01`, round 2, bus 943, 2026-10-13 13:50:27Z, `rules_sha256=e22e0cc4…`); landed by boundary (12).
    16	- 2026-10-14 06:44Z pre-dispatch: `after: [dotfiles-T128-playbook-rules-a04]` met (PR #328 merged 2026-10-13 14:43:36Z as 26909ee4); file hash `e22e0cc45de6fe70ac9be9b3e7b710055b7cd8b8c50767d7a832a9335f392c51` equals the confirmed hash; checker: `dotfiles-T128-playbook-rules-followup-a01.md: OK`; the owned rows under `## Owned by dotfiles-T128-playbook-rules-followup-a01` in the a04 record on `origin/main`: 9 (local 9); premises 1 and 2 re-run equal (`premise-run.py`); no in-flight task holds its files (the hook task edits the project-map rule and SKILL, the PATH task `scripts/orchestrator/orch-gate.sh` and two test modules). Seat: `claude-standard-dot-a002` (worker-f, w5:p9), free since PR #352 merged 06:32:35Z.
    17	- **Dispatched 06:47:41Z to `claude-standard-dot-a002` (worker-f, w5:p9), bus 1106, read** (the line in the dispatch list above).
    18	- 06:50:50Z a002 PONG `status=question` (bus 1108): the owned section on `origin/main` (c15ba668, a04 record lines 69 to 82) holds four rows (`local:65a3d71:1 rule-gap`, `audit:65a3d71:2 rule-gap`, `audit:65a3d71:1 disposition-range`, which names no rule sentence, and `audit:71eb920:1 procedure-migration`, SKILL lines 171 to 178 naming `AUDIT_DISPOSITIONS` where the gate on main reads the record's JSON `audit_findings`); it fixes those; question: two more sentences state the same retired mechanism outside 171 to 178 (the task-level audit bullet, SKILL line 90; AGENTS.md line 44) while item 2 forbids sentences outside the owned rows: inside the `procedure-migration` row or another owner's? Nothing pushed. The orchestrator's count of "9 rows" at 06:44Z counted the section's prose lines too; the four rows are the section's `<id>\t<class>` lines.
    19	- 06:52:29Z PING (bus 1110, read): the answer is a scope change of item 1's row, so it travels as amendment 1 (pair-confirmed, hashed), not as a PONG; hold the push; the four rows proceed in the working tree. Amendment 1 written 06:5xZ (item 1: the `procedure-migration` row covers every sentence in the allowed files that states the retired gate input, the fixture included, each with its token test; the `origin/main` lines pasted in its Change section; the pre-amendment copy at `validation/dotfiles-T128-playbook-rules-followup-a01-pre-amend1.md`, hash e22e0cc4); its paired review dispatched to the review seat and the Codex half. INV-6 for this task so far: questions=1, amendments=1 (pending confirm), revises=0.
    20	- 06:57:38Z the Codex half: `confirm` on ec415eaf (receipt `validation/dotfiles-T128-playbook-rules-followup-a01-amend-review-a01-codex-r1.md`, 55 s); 07:00:33Z the seat: `confirm` on the same hash. **Amendment 1 pair-confirmed on `ec415eaf526937fd43907a59fccfc455de117850003ba3d48cd20b065fc5564b`**; ACCEPTANCE accepted to the seat; the amended TASK line (`amendment=1`, `previous_task_sha256` e22e0cc4 computed from `origin/main` at send) to a002 (the line in the dispatch list above). Owner rows on `origin/main` by the row grammar (`owner-rows.sh`, C-41): `local:65a3d71:1 rule-gap`, `audit:71eb920:1 procedure-migration`, `audit:65a3d71:1 disposition-range`, `audit:65a3d71:2 rule-gap`, `rows=4`; the 06:44Z figure of 9 counted the section's prose lines (M-20261014-07).
    21	- 07:02:59Z ACCEPTANCE accepted for the amend review to the seat (bus 1120, read), sent ahead of the queued copy in the dispatch command (the amended TASK line to a002 waits for its read; a second identical ACCEPTANCE may follow from that command and is a duplicate, not a new decision).
    22	- 07:20:57Z RESULT (bus 1123): `status=ready_for_review revises=0 questions=1 amendments=1`, PR #354 head `bd9e8a69606b03a54973bd631baa25ed07b6d247` on base c15ba668 (branch `regime/playbook-rules-followup`; 7a282f3b the owned rows, bd9e8a69 the task copy and evidence); `task_copy` ec415eaf equals amendment 1; rows: `local:65a3d71:1` and `audit:65a3d71:2` `fixed:7a282f3b` (step 6: the orchestrator creates the acceptance record before the task's first dispatch; dispatch.sh refuses a missing or another task's record), `audit:71eb920:1` `fixed:7a282f3b` (amendment 1's scope: the task-level audit bullet now says an incorrect verdict is dispositioned in the record's JSON `audit_findings` {n, reason, evidence} written by `acceptance-front-matter.py --audit-dispositions`, correct-verdict findings keep the `audit-finding:` prose; step 10.3 points to it; the 10.4 command without `AUDIT_DISPOSITIONS`; the `AUDIT_EVIDENCE` bullet; AGENTS.md's gate sentence), `audit:65a3d71:1` (disposition-range) names no sentence, no change; files AGENTS.md, the SKILL, `tests/unit/test_agmsg_orchestration_docs.py`, `tests/fixtures/regime/orchestrator-step-6.md`, `tests/fixtures/regime/invariants.md` (each fixture in its one changed sentence) plus the task evidence directory; tests 48 OK (two changed, one new `test_an_incorrect_audit_is_dispositioned_in_audit_findings`, the stale forms asserted absent); no threads; the Bot's single review clean (issue comment 6163090018 "Did not find any major issues", reviewed bd9e8a69; posted 613 s after `gh pr ready` 07:07:25Z); CI 13 of 13; caps 5 files outside `.orchestration/`, 6 added outside tests, 50 under tests. ACCEPTANCE `pending-integration head=bd9e8a69` 07:21:37Z (bus 1124, read); the chain runs after PR #353 merges (its merge moves main, one `update-branch` for this PR then).

 exited 1 in 463ms:
error connecting to api.github.com
check your internet connection or https://githubstatus.com

 succeeded in 466ms:
21:- A Claude session started in the repository root outside Herdr (a plain shell, mosh/ssh, or `claude -p`) is a pane-less orchestrator: nothing seats a worker automatically, and the SessionStart `herdr-agents --attach` hook prints a summary line naming that state, the on-demand commands, and any seated worker, followed in a regime repository by the `agmsg-orchestration:` directive line. Bring the regime up on demand: claim the seat outside the sandbox with the composite instance id, `actas-claim.sh <repo> claude-code <name> <session_id>.<claude pid>` (a claim from sandboxed Bash writes the bare session id and turn delivery then skips silently; see the seat-lock bullet below); seat the worker with `herdr-agents --add-worker <worktree>` (it derives `HERDR_SOCKET_PATH` from the default Herdr server socket `~/.config/herdr/herdr.sock`, the path the Claude sandbox allowlists, before creating anything, accepts a claude worker's workspace-trust dialog during spawn's readiness wait, and takes `--ready-timeout <seconds>`); confirm the worker's placement from its `run/spawn.*` placement record itself (the `herdr:<socket>:<pane>` row that upstream `agmsg_spawn_path` resolves) and the `linkage=` line `--add-worker` prints, never from `team.sh <team> --json`, which observes Codex members by reading their pane; treat the `linkage=` line `--add-worker` prints as the `AGMSG-PING` evidence, and on `pong=no` or `linkage=unreached` wake again with `agmsg-dispatch <team> <orchestrator> <worker> <pane> 'AGMSG-PING v1 task_id=<id> reason=<reason>'` and verify the PING's `read_at` (`poke.sh` only for a viewed workspace); and dispatch no AGMSG-TASK before its `AGMSG-PONG` arrives. Without a managed workspace the auditor runs headless, in the form the task-level audit bullet below names. A sandboxed pane-less session cannot keep a Monitor watch (the sandbox's pid namespace), so RESULTs arrive by turn delivery.
33:- Delegate all repository-mutating work — file edits, builds, test runs, and git state changes — to seated workers, with at most one seated worker per git worktree and sequential assignments within one worktree. Add worktrees for parallelism; never use parallel `codex exec` or per-task Codex spawning, except that the read-only, non-interactive task-level audit the orchestrator runs during acceptance (the task-level audit bullet below) is not worker spawning and is permitted; it is identity-less. agmsg/herdr control-plane commands (`delivery.sh`, `watch.sh`, `actas-claim.sh`, `send.sh`, `join.sh`, and herdr agent/pane commands) are orchestrator-side exemptions.
43:  - Some steps stay sequential. The single audit tab serializes audits; the task-level audit of T67 reduces them to one per task. The orchestrator-side gate (`make require-crit-review`) and merges also run one at a time.
72:- Before every acceptance action (revise, accept, merge) the orchestrator runs `scripts/regime-counters.sh <task id>` and pastes its output into the acceptance record. S2 is decided from INV-6's counts: each component the script prints is read from its output, and for each component it prints as `unknown` the record pastes the command and output that read the source INV-6 names for that component, or, while that source has no entry for the task, says so and pastes the reading of the interim record the orchestrator used in its place. S1 (plan 006: the same finding class three times on one artifact, from any reviewer) is decided from the record's finding-class table, which gives a class to every finding the PR-feedback sweep lists, whatever its disposition, and to every task-level audit finding; three rows of one class stop the artifact.
157:## Orchestrator Playbook
164:6. Send `AGMSG-TASK v1` with the exact artifact paths and `done_signal=AGMSG-RESULT`. Pass every `send.sh`/`poke.sh` body with `--body-file <path>` (both take it in agmsg v1.5.0), never as a positional argument: a positional `<text>` passes through the caller's own shell first, where a backtick or `$( )` in the body silently executes and vanishes from what arrives (upstream #378). `agmsg-dispatch` is the one exception and takes a single-line, shell-safe positional message. Pick the path by how the recipient is seated, never by inferring pane or agent status: a worker in a `herdr-agents` pane gets `agmsg-dispatch <team> <from> <to> <pane_id> "<message>"` (send, generic wake, `read_at` wait; single-line shell-safe text only), the sanctioned wake path until worker seating writes placement records at launch, because `poke.sh` exits 1 with "no placement record" for a hand-joined member, and a herdr-agents worker gets a record only once it acts from its own pane (upstream `send.sh`/`inbox.sh` record the acting pane, #1109); a spawn-seated member (placement record `run/spawn.*`; `team.sh <team> --json` shows its pane) gets `poke.sh <team> <name> --body-file <path> [--retries N --retry-delay SECONDS --backoff fixed|exponential]`, which types and submits in one call and refuses to type over an in-progress draft (#1321/#1322); a pane-less member gets `send.sh <team> <from> <to> --body-file <path>` and its own delivery mode. Verify delivery via the messages.db `read_at` column. `poke.sh` exit codes: 10 = terminal unreachable, 12 = pane gone or no live agent, 14/15 = refused to type over a changing or unlocatable input box, 13 = the driver has no poke path for this pane (for example a `plain` terminal); where poke.sh's narrow agmsg-message fallback succeeds it exits 0, so 13 means nothing was delivered, and the printed reason names the native channel, asks the caller to claim its own identity first, or reports that the fallback failed. Never retry a 13 as `send.sh` yourself: that overrides the driver's considered refusal and can double-deliver. Seating case: a worker in an unviewed or headless Herdr workspace (no client attached, a small pane rect such as 18x41) makes `poke.sh` exit 14/15 from its TUI input locator; that is a locator refusal, not evidence about the worker's state, so wake it with `agmsg-dispatch` and verify `read_at`. Every dispatch (TASK, ACCEPTANCE, PING) is recorded in the current acceptance record under a `dispatch:` key as the bus line with its read marker; a seat is reported as working only from such a line, and after a context compaction the open TASK list is re-derived from a bus read that is refused when it reaches its limit (`bus-read.sh` exits when the history reaches `BUS_READ_LIMIT`; the orchestrator raises the limit and reads again), never from a default-limited one and never from a read whose truncation went unnoticed. A seated worker idle for 20 minutes since its latest bus event for the task while a dispatchable task exists (INV-10's idle figure; its 30 minutes is the first-push deadline) gets a bus read, then a PING; a longer silent wait is never the answer. `scripts/orchestrator/dispatch.sh` writes the line and `scripts/orchestrator/bus-read.sh` performs the read and prints the minutes since each open task's latest event (both on main since a03c1daa, plan 007 T718); the orchestrator applies the 20-minute figure to the minutes the script prints (the script's own silence flag still uses 30 minutes, a recorded residual of the tools lineage).
168:10. For a RESULT that carries a pull request, integrate in this order. This is the single procedure that the PR integration rule, `AGENTS.md`, the README and the gh-first-workflow skill cite. A `gh pr update-branch` moves the head, so steps 1 to 4 run again on the new head. After an update-branch the orchestrator runs it, the order is CI on the new head, then the sweep, then the audit; an audit started before CI finishes sees incomplete evidence and returns an evidence-only `incorrect`. Select a checkout with git -C <absolute path>, never with cd, which the sandboxed Bash may not honour. After moving the review worktree to the audited head, verify git -C <review> rev-parse HEAD equals that head and git -C <main> symbolic-ref --short HEAD prints main before the audit and the gate.
170:    2. Run the task-level audit of that head in the pair or headless form of the task-level audit bullet. It exits nonzero for every verdict other than `correct`. An exit with `Audit verdict: incorrect` is not a failed step: continue to step 3 and disposition its findings. A `blocked` or missing verdict means re-running the audit.
182:11. Send `AGMSG-ACCEPTANCE v1 status=accepted` when done, or `status=revise` with a narrow `reason` and `next_action` when more work is required.
191:6. Put the verbatim output of every validation command in `expected_validation_file`; every identifier your report claims to have created must appear in that output.
195:10. If blocked, still write the report and evidence paths that explain the blocker.
196:11. Reply with the requested `done_signal`, normally `AGMSG-RESULT v1`, and include all artifact paths. To a herdr-paned orchestrator, send RESULT and PONG with `agmsg-dispatch <team> <worker> <orchestrator> <pane_id>` (for example `wN:p1`; single-line, shell-safe text) rather than bare `send.sh`, so the wake starts the idle orchestrator's turn and its Stop hook delivers the message. The Claude sandbox manifest lists `agmsg-dispatch` in `claude.sandbox.excludedCommands`, so a Claude worker runs it outside the sandbox from the first attempt: no failed sandboxed run, no unsandboxed retry, and no escalation. Claude Code still applies its permission rules to excluded commands, so the managed settings allow `Bash(agmsg-dispatch:*)` (the only managed `permissions.allow` entry) and the dispatch runs without a prompt. A Codex seat runs under Codex's own sandbox, which this setting does not cover.
214:## Codex seat worklogs
{
  "lastAnalyzedAt": "2026-10-02T14:12:51Z",
  "gitCommitHash": "940a3a2b07adfd14140a0acff96784ef53a0a509",
  "version": "1.0.0",
  "analyzedFiles": 368
}
dict
['version', 'project', 'nodes', 'edges', 'layers', 'tour']
nodes 984
[
  {
    "summary": "Integration guard that requires native agent or Crit review evidence for meaningful diffs and, for PR integration, re-collects GitHub feedback from the authenticated base's pr-feedback.py and requires a root-cause disposition for every item.",
    "filePath": "scripts/require-crit-review.py"
  },
  {
    "summary": "Skips worklogs and the PR feedback evidence file itself when sizing a diff.",
    "filePath": "scripts/require-crit-review.py"
  },
  {
    "summary": "Rejects PR feedback evidence outside .orchestration/validation/ or without the -pr-feedback.json suffix.",
    "filePath": "scripts/require-crit-review.py"
  },
  {
    "summary": "Lists unstaged, staged, untracked, and optionally base...HEAD changed paths, excluding ignored files.",
    "filePath": "scripts/require-crit-review.py"
  },
  {
    "summary": "Sums added and removed line counts across working, staged, and base...HEAD diffs via git numstat.",
    "filePath": "scripts/require-crit-review.py"
  },
  {
    "summary": "Classifies a path as high risk (policy/config file, agent lifecycle prefix, or risky token) and returns the reason.",
    "filePath": "scripts/require-crit-review.py"
  },
  {
    "summary": "Aggregates reasons that make review mandatory: high-risk paths, many files, or large line counts.",
    "filePath": "scripts/require-crit-review.py"
  },
  {
    "summary": "Validates the review receipt file and its required fields, dispatching to agent or Crit evidence checks.",
    "filePath": "scripts/require-crit-review.py"
  },
  {
    "summary": "Checks agent reviewer receipts require the crit-data surface, an allowed outcome, and valid Crit JSON evidence.",
    "filePath": "scripts/require-crit-review.py"
  },
  {
    "summary": "Validates repo-local Crit JSON evidence: inside the repo, a list of well-formed resolved records with at least one review/line/file scope.",
    "filePath": "scripts/require-crit-review.py"
  },
  {
    "summary": "Checks the filled pr-feedback JSON: correct head, valid fixed:<commit> or not-applicable:<reason> dispositions, failure reasons long enough, and fixed commits in range.",
    "filePath": "scripts/require-crit-review.py"
  },
  {
    "summary": "Binds the evidence's base to the PR's GitHub base and local repository before running any collector, rejecting stale or rewritten bases.",
    "filePath": "scripts/require-crit-review.py"
  },
  {
    "summary": "Re-runs the GitHub base's pr-feedback.py and requires every currently collected item to be present in the evidence.",
    "filePath": "scripts/require-crit-review.py"
  },
  {
    "summary": "CLI entry that decides whether review is required, validates base, review receipts, and PR feedback evidence, and exits non-zero on any error.",
    "filePath": "scripts/require-crit-review.py"
  },
  {
    "summary": "Documentation parity test asserting the agmsg-orchestration rule and SKILL teach the same registration and delivery invariants and that the SKILL drops pane-status gating and raw pane wakes.",
    "filePath": "tests/unit/test_agmsg_orchestration_docs.py"
  },
  {
    "summary": "Test case asserting the agmsg-orchestration rule and SKILL share registration and delivery invariants.",
    "filePath": "tests/unit/test_agmsg_orchestration_docs.py"
  }
]

**Managing output truncation**
exec
/bin/zsh -lc 'git diff --no-ext-diff 6a2473f362762cf74c750f2141e5a11853816745 3a8f809b36944b0cb778da53104f9b3c54f67355 -- AGENTS.md home/dot_agents/skills/agmsg-orchestration/SKILL.md tests' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 75ms:
diff --git a/AGENTS.md b/AGENTS.md
index a0b54678..1a825101 100644
--- a/AGENTS.md
+++ b/AGENTS.md
@@ -41,7 +41,7 @@
 - Agent evidence must contain at least one resolved record. For a finding-free review, add and resolve one review-scope approval record.
 - When the crit CLI or its data is unavailable, save the independent agent review in that same JSON shape (hand-written records are acceptable), mark each record `resolved: true` after addressing it, and reference it from the receipt exactly as crit-exported evidence; the guard validates shape, not provenance.
 - This local evidence is process evidence, not reviewer authentication. Human `CRIT_REVIEWED=1` receipts remain supported.
-- Before merging a pull request, follow the integration order in the agmsg-orchestration SKILL's Orchestrator Playbook step 10 and `home/dot_config/claude/rules/pr-integration.md`: the `scripts/pr-feedback.py` sweep, the task-level audit, the acceptance record, then the gate with `PR_FEEDBACK_EVIDENCE` and `AUDIT_EVIDENCE` (`AUDIT_DISPOSITIONS` for an `incorrect` verdict).
+- Before merging a pull request, follow the integration order in the agmsg-orchestration SKILL's Orchestrator Playbook step 10 and `home/dot_config/claude/rules/pr-integration.md`: the `scripts/pr-feedback.py` sweep, the task-level audit, the acceptance record, then the gate with `PR_FEEDBACK_EVIDENCE`, `AUDIT_EVIDENCE` and `ACCEPTANCE_EVIDENCE` (the record's `audit_findings` disposition an `incorrect` verdict).
 
 ## Audit
 
diff --git a/home/dot_agents/skills/agmsg-orchestration/SKILL.md b/home/dot_agents/skills/agmsg-orchestration/SKILL.md
index 62fc1923..2e706a28 100644
--- a/home/dot_agents/skills/agmsg-orchestration/SKILL.md
+++ b/home/dot_agents/skills/agmsg-orchestration/SKILL.md
@@ -87,7 +87,7 @@ Use this skill for structured multi-agent work where an orchestrator seat assign
     - The gate needs both the transcript file and its non-empty `.last.md` companion.
   - Run either form from a clean tree: the only untracked content in the audited checkout is this task's `.orchestration` evidence that the audit prompt names (task file, report, validation, sandbox file, feedback JSON). Otherwise run it from a dedicated clean checkout, so no other edit can reach the auditor.
   - A new push, including a `gh pr update-branch` merge, needs a new audit of the new head.
-  - The orchestrator dispositions every `[P0-P3]` finding in the acceptance record, whatever the verdict: exactly one `audit-finding: <n> …` line per finding, numbered 1..N in the audit's order of `[P0-P3]` lines. The audit's finding lines may be bulleted; a disposition line may be indented but never starts with a list marker, or the gate skips it. `fixed:<sha>` needs a fresh audit of that sha; otherwise `not-applicable:<reason of at least 20 characters>`. Deferral ("later", a follow-up task, a stopgap or a suppression) is not a disposition. The gate enforces these lines only for an `incorrect` verdict (T68), but a finding under `Verdict: correct` is dispositioned all the same.
+  - The orchestrator dispositions every `[P0-P3]` finding in the acceptance record, whatever the verdict, numbered 1..N in the audit's order of `[P0-P3]` lines (the audit's finding lines may be bulleted). For an `incorrect` verdict the dispositions are the record's JSON `audit_findings`, the only form the gate reads: one `{n, reason, evidence}` entry per finding, `n` the number as a string and `reason` at least 20 characters, written with `scripts/orchestrator/acceptance-front-matter.py --audit-dispositions <tsv>`; an entry never cites a fix, since a fix moves the head and needs its own audit. A finding under `Verdict: correct` is dispositioned all the same, as an `audit-finding: <n> …` line in the record's prose: `fixed:<sha>` with a fresh audit of that sha, otherwise `not-applicable:<reason of at least 20 characters>`. Deferral ("later", a follow-up task, a stopgap or a suppression) is not a disposition.
   - The audit evidence and the PR-feedback JSON quote reviewed content, so mask them with `uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets <files>` before they are committed. The gate compares PR-feedback bodies after the same masking, so masked feedback evidence still matches the live collection (T93, #251).
   - Audit findings are input, never approval; acceptance authority stays with the orchestrator, and each RESULT gets its own acceptance record.
 - Crit is agent-side only for Claude Code and Codex alike, as in `home/dot_config/claude/rules/crit-review.md`: record crit-data evidence (`crit status --json`, `crit comments --all --json <review.json>`) and never open a browser review to ask the user. When Crit data is unavailable, save the independent agent review as the same repo-local JSON list (objects with non-empty string `id`, `body`, `scope` and `resolved: true`, at least one `scope: "review"` or path-bound `line`/`file` record; hand-written records are acceptable because the guard validates shape, not provenance) and reference it from a `review_surface: crit-data` receipt with `reviewer: claude-code`, `claude`, or `codex`, `review_source: <that JSON>`, and `review_outcome: approved` or `addressed`. Run `crit share` or any other publish step only when the user explicitly asks for it. Close a Crit session opened by the Plan Mode hook once its review is done, so no local Crit web server stays resident.
@@ -161,21 +161,21 @@ AGMSG-PONG v1 task_id=<id> status=alive|blocked|question note=<short-note>
 3. Write a task file that includes objective, scope, allowed files, forbidden actions, expected artifacts, validation commands, and max turns. Name the render check as `make render-check`, never the bare `python3 scripts/generate-agent-configs.py --check`, which fails without PyYAML. Ground `allowed_files` by grepping the repository for every touch point the task names (tests that pin call sequences, mirrors, fixtures) before dispatch. Verify every CLI constraint the task asserts by running the real command in a safe form, not by reading `--help`. Presume an auditor finding that contradicts your own review is right until you refute it with evidence. Decide the worker kind from the allowed files before dispatch: a seat never edits the source of its own execution boundary, so a change is routed by the boundary it touches. A change that touches only Claude's boundary goes to a Codex seat: the `claude.permissions`, `claude.sandbox` and `claude.hooks` blocks of `home/dot_agents/agent-config.yaml` (including excludedCommands, allowUnsandboxedCommands, writable roots, network and the PermissionRequest hook), the Claude-rendering parts of `scripts/generate-agent-configs.py`, the rendered `home/.chezmoitemplates/claude-settings-managed.json`, and `home/dot_claude/modify_private_settings.json`. A change that touches only Codex's boundary goes to a Claude seat: `codex.sandbox_workspace_write`, `codex.approval_policy`, the Codex-rendering parts of the renderer, and `home/.chezmoitemplates/codex-config-managed.toml`. A change that touches both, or a shared source the orchestrator cannot split (such as `codex.sandbox_workspace_write.writable_roots`, which also renders into Claude's `allowWrite`), goes to the operator. The orchestrator decides the kind from the diff the task will produce and records it and the chosen worker profile in the task file. The Claude Code auto-mode classifier also refuses a Claude-boundary task on a Claude seat as Self-Modification. A task that edits permgate (`home/dot_agents/permgate-policy.yaml`, `home/dot_local/bin/common/executable_permgate`), the PermissionRequest hook of both seats, goes to the operator; a Codex `security`-profile worker reviews the change before the orchestrator accepts it, per the model-selection rule. `auto` is Claude Code's built-in starting permission mode since 2.1.283. A project-level `defaultMode: auto` (`.claude/settings.json` or `.claude/settings.local.json`) does not take effect, and the session then also ignores the user-level `defaultMode`, so `auto` belongs only in user or managed settings. Before dispatch, read the task's verbatim blocks against each other for contradictions, and state each rule once; a second artifact references the first instead of restating it.
 4. Start or relaunch worker panes only through `herdr-agents` modes. Deliver messages and wakes as in step 6; never use `pane send-text` followed by `send-keys Enter`, because the separate Enter races the TUI composer and fails nondeterministically.
 5. Configure delivery deliberately. `delivery.sh set turn` is useful for turn-end inbox checks; changing delivery mode can kill project watcher processes, so do it before starting long-running project watchers.
-6. Send `AGMSG-TASK v1` with the exact artifact paths and `done_signal=AGMSG-RESULT`. Pass every `send.sh`/`poke.sh` body with `--body-file <path>` (both take it in agmsg v1.5.0), never as a positional argument: a positional `<text>` passes through the caller's own shell first, where a backtick or `$( )` in the body silently executes and vanishes from what arrives (upstream #378). `agmsg-dispatch` is the one exception and takes a single-line, shell-safe positional message. Pick the path by how the recipient is seated, never by inferring pane or agent status: a worker in a `herdr-agents` pane gets `agmsg-dispatch <team> <from> <to> <pane_id> "<message>"` (send, generic wake, `read_at` wait; single-line shell-safe text only), the sanctioned wake path until worker seating writes placement records at launch, because `poke.sh` exits 1 with "no placement record" for a hand-joined member, and a herdr-agents worker gets a record only once it acts from its own pane (upstream `send.sh`/`inbox.sh` record the acting pane, #1109); a spawn-seated member (placement record `run/spawn.*`; `team.sh <team> --json` shows its pane) gets `poke.sh <team> <name> --body-file <path> [--retries N --retry-delay SECONDS --backoff fixed|exponential]`, which types and submits in one call and refuses to type over an in-progress draft (#1321/#1322); a pane-less member gets `send.sh <team> <from> <to> --body-file <path>` and its own delivery mode. Verify delivery via the messages.db `read_at` column. `poke.sh` exit codes: 10 = terminal unreachable, 12 = pane gone or no live agent, 14/15 = refused to type over a changing or unlocatable input box, 13 = the driver has no poke path for this pane (for example a `plain` terminal); where poke.sh's narrow agmsg-message fallback succeeds it exits 0, so 13 means nothing was delivered, and the printed reason names the native channel, asks the caller to claim its own identity first, or reports that the fallback failed. Never retry a 13 as `send.sh` yourself: that overrides the driver's considered refusal and can double-deliver. Seating case: a worker in an unviewed or headless Herdr workspace (no client attached, a small pane rect such as 18x41) makes `poke.sh` exit 14/15 from its TUI input locator; that is a locator refusal, not evidence about the worker's state, so wake it with `agmsg-dispatch` and verify `read_at`. Every dispatch (TASK, ACCEPTANCE, PING) is recorded in the current acceptance record under a `dispatch:` key as the bus line with its read marker; a seat is reported as working only from such a line, and after a context compaction the open TASK list is re-derived from a bus read that is refused when it reaches its limit (`bus-read.sh` exits when the history reaches `BUS_READ_LIMIT`; the orchestrator raises the limit and reads again), never from a default-limited one and never from a read whose truncation went unnoticed. A seated worker idle for 20 minutes since its latest bus event for the task while a dispatchable task exists (INV-10's idle figure; its 30 minutes is the first-push deadline) gets a bus read, then a PING; a longer silent wait is never the answer. `scripts/orchestrator/dispatch.sh` writes the line and `scripts/orchestrator/bus-read.sh` performs the read and prints the minutes since each open task's latest event (both on main since a03c1daa, plan 007 T718); the orchestrator applies the 20-minute figure to the minutes the script prints (the script's own silence flag still uses 30 minutes, a recorded residual of the tools lineage).
+6. Send `AGMSG-TASK v1` with the exact artifact paths and `done_signal=AGMSG-RESULT`. Pass every `send.sh`/`poke.sh` body with `--body-file <path>` (both take it in agmsg v1.5.0), never as a positional argument: a positional `<text>` passes through the caller's own shell first, where a backtick or `$( )` in the body silently executes and vanishes from what arrives (upstream #378). `agmsg-dispatch` is the one exception and takes a single-line, shell-safe positional message. Pick the path by how the recipient is seated, never by inferring pane or agent status: a worker in a `herdr-agents` pane gets `agmsg-dispatch <team> <from> <to> <pane_id> "<message>"` (send, generic wake, `read_at` wait; single-line shell-safe text only), the sanctioned wake path until worker seating writes placement records at launch, because `poke.sh` exits 1 with "no placement record" for a hand-joined member, and a herdr-agents worker gets a record only once it acts from its own pane (upstream `send.sh`/`inbox.sh` record the acting pane, #1109); a spawn-seated member (placement record `run/spawn.*`; `team.sh <team> --json` shows its pane) gets `poke.sh <team> <name> --body-file <path> [--retries N --retry-delay SECONDS --backoff fixed|exponential]`, which types and submits in one call and refuses to type over an in-progress draft (#1321/#1322); a pane-less member gets `send.sh <team> <from> <to> --body-file <path>` and its own delivery mode. Verify delivery via the messages.db `read_at` column. `poke.sh` exit codes: 10 = terminal unreachable, 12 = pane gone or no live agent, 14/15 = refused to type over a changing or unlocatable input box, 13 = the driver has no poke path for this pane (for example a `plain` terminal); where poke.sh's narrow agmsg-message fallback succeeds it exits 0, so 13 means nothing was delivered, and the printed reason names the native channel, asks the caller to claim its own identity first, or reports that the fallback failed. Never retry a 13 as `send.sh` yourself: that overrides the driver's considered refusal and can double-deliver. Seating case: a worker in an unviewed or headless Herdr workspace (no client attached, a small pane rect such as 18x41) makes `poke.sh` exit 14/15 from its TUI input locator; that is a locator refusal, not evidence about the worker's state, so wake it with `agmsg-dispatch` and verify `read_at`. Every dispatch (TASK, ACCEPTANCE, PING) is recorded in the current acceptance record under a `dispatch:` key as the bus line with its read marker, so the orchestrator creates that record, `.orchestration/acceptance/<task>.md`, before the task's first dispatch (`scripts/orchestrator/dispatch.sh` refuses a record that does not exist or that names another task); a seat is reported as working only from such a line, and after a context compaction the open TASK list is re-derived from a bus read that is refused when it reaches its limit (`bus-read.sh` exits when the history reaches `BUS_READ_LIMIT`; the orchestrator raises the limit and reads again), never from a default-limited one and never from a read whose truncation went unnoticed. A seated worker idle for 20 minutes since its latest bus event for the task while a dispatchable task exists (INV-10's idle figure; its 30 minutes is the first-push deadline) gets a bus read, then a PING; a longer silent wait is never the answer. `scripts/orchestrator/dispatch.sh` writes the line and `scripts/orchestrator/bus-read.sh` performs the read and prints the minutes since each open task's latest event (both on main since a03c1daa, plan 007 T718); the orchestrator applies the 20-minute figure to the minutes the script prints (the script's own silence flag still uses 30 minutes, a recorded residual of the tools lineage).
 7. Track `max_turns`. Use `AGMSG-PING` for liveness if a worker stalls.
 8. On `AGMSG-RESULT`, read the task file and every referenced artifact before deciding.
 9. For a RESULT carrying `effects`, verify that every declared effect has the report's stated reverse mapping before acceptance; record any irreversible effect in the acceptance note.
 10. For a RESULT that carries a pull request, integrate in this order. This is the single procedure that the PR integration rule, `AGENTS.md`, the README and the gh-first-workflow skill cite. A `gh pr update-branch` moves the head, so steps 1 to 4 run again on the new head. After an update-branch the orchestrator runs it, the order is CI on the new head, then the sweep, then the audit; an audit started before CI finishes sees incomplete evidence and returns an evidence-only `incorrect`. Select a checkout with git -C <absolute path>, never with cd, which the sandboxed Bash may not honour. After moving the review worktree to the audited head, verify git -C <review> rev-parse HEAD equals that head and git -C <main> symbolic-ref --short HEAD prints main before the audit and the gate.
     1. Sweep the final head's feedback with `scripts/pr-feedback.py <pr> --json .orchestration/validation/<task>-pr-feedback.json` and give every item a `fixed:<commit>` or `not-applicable:<reason>` disposition, leaving none on `failure` or `warning` annotations. Optionally request `@coderabbitai full review` on the final head first; when a CodeRabbit review exists it is swept like any other item, and the gate does not require a bot review. An `open:<thread id>` item from a worker's third Bot round is a sweep item like any other: it becomes `fixed:<sha>` through a revise round that carries its `check=` (a round that counts toward INV-6 like any other), or `not-applicable:<reason>` with a pasted refutation; until one of those exists the PR is not merged, never with the thread open.
     2. Run the task-level audit of that head in the pair or headless form of the task-level audit bullet. It exits nonzero for every verdict other than `correct`. An exit with `Audit verdict: incorrect` is not a failed step: continue to step 3 and disposition its findings. A `blocked` or missing verdict means re-running the audit.
-    3. Write the acceptance record, summarising the dispositions, with an `audit-finding:` line for every audit finding whatever the verdict (the gate needs them, through `AUDIT_DISPOSITIONS`, when it is `incorrect`).
-    4. Run the gate: `AUDIT_EVIDENCE=<audit> [AUDIT_DISPOSITIONS=<acceptance record>] AGENT_REVIEWED=1 REVIEW_EVIDENCE=<receipt> ACCEPTANCE_EVIDENCE=<acceptance record> BASE=origin/main PR_FEEDBACK_EVIDENCE=<json> make require-crit-review`.
+    3. Write the acceptance record, summarising the dispositions, with every audit finding dispositioned as the task-level audit bullet says: for an `incorrect` verdict the record's JSON `audit_findings`, which the gate reads through `ACCEPTANCE_EVIDENCE` (it never reads `AUDIT_DISPOSITIONS`, which is retired).
+    4. Run the gate: `AUDIT_EVIDENCE=<audit> AGENT_REVIEWED=1 REVIEW_EVIDENCE=<receipt> ACCEPTANCE_EVIDENCE=<acceptance record> BASE=origin/main PR_FEEDBACK_EVIDENCE=<json> make require-crit-review`.
        - A `review` sweep item whose body carries a `P0`–`P3` badge is a finding with its own `fixed:<commit>` or `not-applicable:<reason>` disposition, never a container for its inline threads.
        - The sweep covers issue comments, reviews, inline review comments with thread resolution, non-passing check runs, check-run annotations at every level (`notice`, `warning`, `failure`), and commit statuses. A `failure` marked `not-applicable` needs a concrete reason of at least 20 characters.
        - A CodeRabbit full review is optional, at most once on the final head: the plan allows one review per hour and every review event spends one (docs.coderabbit.ai/management/rate-limits).
        - The feedback JSON may be masked with `uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets`, which masks its keys and string values; the gate identifies an item by its source, url, level, path, line and body, and accepts a body or path that is verbatim or exactly that masked form.
        - The gate rejects evidence outside `.orchestration/validation/` or without the `-pr-feedback.json` suffix. It binds `BASE` to the PR's GitHub base before running the collector from that authenticated SHA: an older base must be outside HEAD's first-parent chain, an advanced base must preserve the merge-base with the PR head, and PR branch commits (including `HEAD`) cannot substitute for the base. Evidence must match the local GitHub repository independently of `GH_REPO`, and `fixed:` commits must be in the authenticated GitHub base-to-head range whatever `BASE` is selected.
-       - `AUDIT_EVIDENCE` must be the task-level file `.orchestration/validation/<task>-audit-<sha7>.md` (the same `<task>` as the feedback JSON); a per-commit `audit-<sha>.md` is rejected. Its verdict comes only from the non-empty `<file>.last.md` and must be `correct`, or `incorrect` with `AUDIT_DISPOSITIONS`. PRs that change only `.orchestration/` files need no audit.
+       - `AUDIT_EVIDENCE` must be the task-level file `.orchestration/validation/<task>-audit-<sha7>.md` (the same `<task>` as the feedback JSON); a per-commit `audit-<sha>.md` is rejected. Its verdict comes only from the non-empty `<file>.last.md` and must be `correct`, or `incorrect` with an `audit_findings` entry in the acceptance record for each of its findings. PRs that change only `.orchestration/` files need no audit.
        - A boundary PR (`orchestration/boundary-<date>[-n]`, `.orchestration` files only) skips the gate, the sweep JSON and the audit (with `BASE` set the gate would demand `PR_FEEDBACK_EVIDENCE`); each Bot thread on it still gets a disposition reply and is resolved, and the next boundary commit message names the PR.
     5. After the required checks pass and the threads are resolved, merge with `gh pr merge <pr> --squash --match-head-commit <audited head sha>`, so a newer head can never be merged on the evidence of the audited one. Every seat acts as the machine's one GitHub account, so no approval is required or possible. Who merges is decided by the integration gate and by native denial of merge commands in Codex seats; `herdr-agents` writes the Claude worker deny rules (`Bash(gh pr merge:*)`, `Bash(gh api -X PUT:*)`, `Bash(gh api --method PUT:*)`, `Bash(gh api graphql:*)`) into the worker worktree's `.claude/settings.local.json`, where [deny rules take precedence over allow rules and cover nested subcommands in every permission mode](https://code.claude.com/docs/en/permissions), but a method flag after the path escapes these prefix rules, so the integration gate remains the authority.
     6. Send `AGMSG-ACCEPTANCE` (step 11).
diff --git a/tests/fixtures/regime/invariants.md b/tests/fixtures/regime/invariants.md
index a1360120..5695c3b1 100644
--- a/tests/fixtures/regime/invariants.md
+++ b/tests/fixtures/regime/invariants.md
@@ -24,7 +24,7 @@
     - The gate needs both the transcript file and its non-empty `.last.md` companion.
   - Run either form from a clean tree: the only untracked content in the audited checkout is this task's `.orchestration` evidence that the audit prompt names (task file, report, validation, sandbox file, feedback JSON). Otherwise run it from a dedicated clean checkout, so no other edit can reach the auditor.
   - A new push, including a `gh pr update-branch` merge, needs a new audit of the new head.
-  - The orchestrator dispositions every `[P0-P3]` finding in the acceptance record, whatever the verdict: exactly one `audit-finding: <n> …` line per finding, numbered 1..N in the audit's order of `[P0-P3]` lines. The audit's finding lines may be bulleted; a disposition line may be indented but never starts with a list marker, or the gate skips it. `fixed:<sha>` needs a fresh audit of that sha; otherwise `not-applicable:<reason of at least 20 characters>`. Deferral ("later", a follow-up task, a stopgap or a suppression) is not a disposition. The gate enforces these lines only for an `incorrect` verdict (T68), but a finding under `Verdict: correct` is dispositioned all the same.
+  - The orchestrator dispositions every `[P0-P3]` finding in the acceptance record, whatever the verdict, numbered 1..N in the audit's order of `[P0-P3]` lines (the audit's finding lines may be bulleted). For an `incorrect` verdict the dispositions are the record's JSON `audit_findings`, the only form the gate reads: one `{n, reason, evidence}` entry per finding, `n` the number as a string and `reason` at least 20 characters, written with `scripts/orchestrator/acceptance-front-matter.py --audit-dispositions <tsv>`; an entry never cites a fix, since a fix moves the head and needs its own audit. A finding under `Verdict: correct` is dispositioned all the same, as an `audit-finding: <n> …` line in the record's prose: `fixed:<sha>` with a fresh audit of that sha, otherwise `not-applicable:<reason of at least 20 characters>`. Deferral ("later", a follow-up task, a stopgap or a suppression) is not a disposition.
   - The audit evidence and the PR-feedback JSON quote reviewed content, so mask them with `uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets <files>` before they are committed. The gate compares PR-feedback bodies after the same masking, so masked feedback evidence still matches the live collection (T93, #251).
   - Audit findings are input, never approval; acceptance authority stays with the orchestrator, and each RESULT gets its own acceptance record.
 - Crit is agent-side only for Claude Code and Codex alike, as in `home/dot_config/claude/rules/crit-review.md`: record crit-data evidence (`crit status --json`, `crit comments --all --json <review.json>`) and never open a browser review to ask the user. When Crit data is unavailable, save the independent agent review as the same repo-local JSON list (objects with non-empty string `id`, `body`, `scope` and `resolved: true`, at least one `scope: "review"` or path-bound `line`/`file` record; hand-written records are acceptable because the guard validates shape, not provenance) and reference it from a `review_surface: crit-data` receipt with `reviewer: claude-code`, `claude`, or `codex`, `review_source: <that JSON>`, and `review_outcome: approved` or `addressed`. Run `crit share` or any other publish step only when the user explicitly asks for it. Close a Crit session opened by the Plan Mode hook once its review is done, so no local Crit web server stays resident.
diff --git a/tests/fixtures/regime/orchestrator-step-6.md b/tests/fixtures/regime/orchestrator-step-6.md
index dd36748b..86762df5 100644
--- a/tests/fixtures/regime/orchestrator-step-6.md
+++ b/tests/fixtures/regime/orchestrator-step-6.md
@@ -1 +1 @@
-6. Send `AGMSG-TASK v1` with the exact artifact paths and `done_signal=AGMSG-RESULT`. Pass every `send.sh`/`poke.sh` body with `--body-file <path>` (both take it in agmsg v1.5.0), never as a positional argument: a positional `<text>` passes through the caller's own shell first, where a backtick or `$( )` in the body silently executes and vanishes from what arrives (upstream #378). `agmsg-dispatch` is the one exception and takes a single-line, shell-safe positional message. Pick the path by how the recipient is seated, never by inferring pane or agent status: a worker in a `herdr-agents` pane gets `agmsg-dispatch <team> <from> <to> <pane_id> "<message>"` (send, generic wake, `read_at` wait; single-line shell-safe text only), the sanctioned wake path until worker seating writes placement records at launch, because `poke.sh` exits 1 with "no placement record" for a hand-joined member, and a herdr-agents worker gets a record only once it acts from its own pane (upstream `send.sh`/`inbox.sh` record the acting pane, #1109); a spawn-seated member (placement record `run/spawn.*`; `team.sh <team> --json` shows its pane) gets `poke.sh <team> <name> --body-file <path> [--retries N --retry-delay SECONDS --backoff fixed|exponential]`, which types and submits in one call and refuses to type over an in-progress draft (#1321/#1322); a pane-less member gets `send.sh <team> <from> <to> --body-file <path>` and its own delivery mode. Verify delivery via the messages.db `read_at` column. `poke.sh` exit codes: 10 = terminal unreachable, 12 = pane gone or no live agent, 14/15 = refused to type over a changing or unlocatable input box, 13 = the driver has no poke path for this pane (for example a `plain` terminal); where poke.sh's narrow agmsg-message fallback succeeds it exits 0, so 13 means nothing was delivered, and the printed reason names the native channel, asks the caller to claim its own identity first, or reports that the fallback failed. Never retry a 13 as `send.sh` yourself: that overrides the driver's considered refusal and can double-deliver. Seating case: a worker in an unviewed or headless Herdr workspace (no client attached, a small pane rect such as 18x41) makes `poke.sh` exit 14/15 from its TUI input locator; that is a locator refusal, not evidence about the worker's state, so wake it with `agmsg-dispatch` and verify `read_at`. Every dispatch (TASK, ACCEPTANCE, PING) is recorded in the current acceptance record under a `dispatch:` key as the bus line with its read marker; a seat is reported as working only from such a line, and after a context compaction the open TASK list is re-derived from a bus read that is refused when it reaches its limit (`bus-read.sh` exits when the history reaches `BUS_READ_LIMIT`; the orchestrator raises the limit and reads again), never from a default-limited one and never from a read whose truncation went unnoticed. A seated worker idle for 20 minutes since its latest bus event for the task while a dispatchable task exists (INV-10's idle figure; its 30 minutes is the first-push deadline) gets a bus read, then a PING; a longer silent wait is never the answer. `scripts/orchestrator/dispatch.sh` writes the line and `scripts/orchestrator/bus-read.sh` performs the read and prints the minutes since each open task's latest event (both on main since a03c1daa, plan 007 T718); the orchestrator applies the 20-minute figure to the minutes the script prints (the script's own silence flag still uses 30 minutes, a recorded residual of the tools lineage).
+6. Send `AGMSG-TASK v1` with the exact artifact paths and `done_signal=AGMSG-RESULT`. Pass every `send.sh`/`poke.sh` body with `--body-file <path>` (both take it in agmsg v1.5.0), never as a positional argument: a positional `<text>` passes through the caller's own shell first, where a backtick or `$( )` in the body silently executes and vanishes from what arrives (upstream #378). `agmsg-dispatch` is the one exception and takes a single-line, shell-safe positional message. Pick the path by how the recipient is seated, never by inferring pane or agent status: a worker in a `herdr-agents` pane gets `agmsg-dispatch <team> <from> <to> <pane_id> "<message>"` (send, generic wake, `read_at` wait; single-line shell-safe text only), the sanctioned wake path until worker seating writes placement records at launch, because `poke.sh` exits 1 with "no placement record" for a hand-joined member, and a herdr-agents worker gets a record only once it acts from its own pane (upstream `send.sh`/`inbox.sh` record the acting pane, #1109); a spawn-seated member (placement record `run/spawn.*`; `team.sh <team> --json` shows its pane) gets `poke.sh <team> <name> --body-file <path> [--retries N --retry-delay SECONDS --backoff fixed|exponential]`, which types and submits in one call and refuses to type over an in-progress draft (#1321/#1322); a pane-less member gets `send.sh <team> <from> <to> --body-file <path>` and its own delivery mode. Verify delivery via the messages.db `read_at` column. `poke.sh` exit codes: 10 = terminal unreachable, 12 = pane gone or no live agent, 14/15 = refused to type over a changing or unlocatable input box, 13 = the driver has no poke path for this pane (for example a `plain` terminal); where poke.sh's narrow agmsg-message fallback succeeds it exits 0, so 13 means nothing was delivered, and the printed reason names the native channel, asks the caller to claim its own identity first, or reports that the fallback failed. Never retry a 13 as `send.sh` yourself: that overrides the driver's considered refusal and can double-deliver. Seating case: a worker in an unviewed or headless Herdr workspace (no client attached, a small pane rect such as 18x41) makes `poke.sh` exit 14/15 from its TUI input locator; that is a locator refusal, not evidence about the worker's state, so wake it with `agmsg-dispatch` and verify `read_at`. Every dispatch (TASK, ACCEPTANCE, PING) is recorded in the current acceptance record under a `dispatch:` key as the bus line with its read marker, so the orchestrator creates that record, `.orchestration/acceptance/<task>.md`, before the task's first dispatch (`scripts/orchestrator/dispatch.sh` refuses a record that does not exist or that names another task); a seat is reported as working only from such a line, and after a context compaction the open TASK list is re-derived from a bus read that is refused when it reaches its limit (`bus-read.sh` exits when the history reaches `BUS_READ_LIMIT`; the orchestrator raises the limit and reads again), never from a default-limited one and never from a read whose truncation went unnoticed. A seated worker idle for 20 minutes since its latest bus event for the task while a dispatchable task exists (INV-10's idle figure; its 30 minutes is the first-push deadline) gets a bus read, then a PING; a longer silent wait is never the answer. `scripts/orchestrator/dispatch.sh` writes the line and `scripts/orchestrator/bus-read.sh` performs the read and prints the minutes since each open task's latest event (both on main since a03c1daa, plan 007 T718); the orchestrator applies the 20-minute figure to the minutes the script prints (the script's own silence flag still uses 30 minutes, a recorded residual of the tools lineage).
diff --git a/tests/unit/test_agmsg_orchestration_docs.py b/tests/unit/test_agmsg_orchestration_docs.py
index 656c7f92..b50b9973 100644
--- a/tests/unit/test_agmsg_orchestration_docs.py
+++ b/tests/unit/test_agmsg_orchestration_docs.py
@@ -522,7 +522,12 @@ class AgmsgRegimePatternTest(unittest.TestCase):
         step = self.section(self.section(SKILL.read_text(), "## Orchestrator Playbook"), "\n6. ", "\n7. ")
         for token in (
             "Every dispatch (TASK, ACCEPTANCE, PING) is recorded in the current acceptance record under a "
-            "`dispatch:` key as the bus line with its read marker; a seat is reported as working only from such a "
+            "`dispatch:` key as the bus line with its read marker, "
+            # Row local:65a3d71:1 (the a04 record's owned section): dispatch.sh refuses a missing record, so the rule
+            # says who creates it and when.
+            "so the orchestrator creates that record, `.orchestration/acceptance/<task>.md`, before the task's first "
+            "dispatch (`scripts/orchestrator/dispatch.sh` refuses a record that does not exist or that names another "
+            "task); a seat is reported as working only from such a "
             # The local review of 7771082f: the merged bus-read.sh refuses a read at its limit; nothing reads all.
             "line, and after a context compaction the open TASK list is re-derived from a bus read that is refused "
             "when it reaches its limit (`bus-read.sh` exits when the history reaches `BUS_READ_LIMIT`; the "
@@ -629,11 +634,50 @@ class AgmsgRegimePatternTest(unittest.TestCase):
     def test_the_gate_reads_the_acceptance_record(self) -> None:
         # Plan 007 T703 item 6: the gate reads the record's ledger and `search:` line once gate-evidence-a02 lands.
         step = self.section(self.section(SKILL.read_text(), "## Orchestrator Playbook"), "\n10. ", "\n11. ")
+        # Row audit:71eb920:1 (the a04 record's owned section): the gate retired AUDIT_DISPOSITIONS and reads an
+        # incorrect audit's dispositions from the record's audit_findings, so step 10 no longer names the variable.
+        for token in (
+            "`AUDIT_EVIDENCE=<audit> AGENT_REVIEWED=1 REVIEW_EVIDENCE=<receipt> ACCEPTANCE_EVIDENCE=<acceptance record> "
+            "BASE=origin/main PR_FEEDBACK_EVIDENCE=<json> make require-crit-review`",
+            "with every audit finding dispositioned as the task-level audit bullet says: for an `incorrect` verdict "
+            "the record's JSON `audit_findings`, which the gate reads through `ACCEPTANCE_EVIDENCE` (it never reads "
+            "`AUDIT_DISPOSITIONS`, which is retired).",
+            "must be `correct`, or `incorrect` with an `audit_findings` entry in the acceptance record for each of its "
+            "findings.",
+        ):
+            with self.subTest(token=token[:40]):
+                self.assertIn(token, step)
+        for stale in ("[AUDIT_DISPOSITIONS=", "through `AUDIT_DISPOSITIONS`", "`incorrect` with `AUDIT_DISPOSITIONS`"):
+            with self.subTest(stale=stale):
+                self.assertNotIn(stale, step)
+
+    def test_an_incorrect_audit_is_dispositioned_in_audit_findings(self) -> None:
+        # Row audit:71eb920:1, amendment 1: the task-level audit bullet and AGENTS.md's gate sentence named the retired
+        # gate input (the audit-finding: prose the gate read through AUDIT_DISPOSITIONS); the gate reads audit_findings.
+        bullet = self.section(
+            self.invariants(), "\n  - The orchestrator dispositions every `[P0-P3]` finding", "\n  - "
+        )
+        for token in (
+            "For an `incorrect` verdict the dispositions are the record's JSON `audit_findings`, the only form the gate "
+            "reads: one `{n, reason, evidence}` entry per finding, `n` the number as a string and `reason` at least 20 "
+            "characters, written with `scripts/orchestrator/acceptance-front-matter.py --audit-dispositions <tsv>`; an "
+            "entry never cites a fix, since a fix moves the head and needs its own audit.",
+            "A finding under `Verdict: correct` is dispositioned all the same, as an `audit-finding: <n> …` line in the "
+            "record's prose: `fixed:<sha>` with a fresh audit of that sha, otherwise `not-applicable:<reason of at "
+            "least 20 characters>`.",
+        ):
+            with self.subTest(token=token[:40]):
+                self.assertIn(token, bullet)
+        for stale in ("The gate enforces these lines only for an `incorrect` verdict", "or the gate skips it"):
+            with self.subTest(stale=stale):
+                self.assertNotIn(stale, bullet)
+        agents = (ROOT / "AGENTS.md").read_text()
         self.assertIn(
-            "REVIEW_EVIDENCE=<receipt> ACCEPTANCE_EVIDENCE=<acceptance record> BASE=origin/main "
-            "PR_FEEDBACK_EVIDENCE=<json> make require-crit-review",
-            step,
+            "then the gate with `PR_FEEDBACK_EVIDENCE`, `AUDIT_EVIDENCE` and `ACCEPTANCE_EVIDENCE` (the record's "
+            "`audit_findings` disposition an `incorrect` verdict).",
+            agents,
         )
+        self.assertNotIn("`AUDIT_DISPOSITIONS` for an `incorrect` verdict", agents)
 
 
 class AgmsgOrchestrationSingleSourceTest(unittest.TestCase):

**Assessing changed sentences and tokens**
exec
/bin/zsh -lc 'nl -ba .orchestration/tasks/dotfiles-T128-playbook-rules-followup-a01.md && git show origin/main:.orchestration/acceptance/dotfiles-T128-playbook-rules-a04.md | nl -ba && git diff --name-only 940a3a2b07adfd14140a0acff96784ef53a0a509..HEAD | head -25' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 430ms:
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
    61	1. The owned rows: the `<id>\t<class>` rows under the heading `## Owned by dotfiles-T128-playbook-rules-followup-a01` in `.orchestration/acceptance/dotfiles-T128-playbook-rules-a04.md` as read from `origin/main` (Codex Bot P2 threads and local-review findings on a04's final head after its one revise round, each dispositioned on PR #328 as `not-applicable:advisory P2 owned by dotfiles-T128-playbook-rules-followup-a01; evidence=git show origin/main:.orchestration/tasks/dotfiles-T128-playbook-rules-followup-a01.md | grep -n 'item 1'` (the gate's full form once PR #329 lands)). That section is this item's whole definition, closed at a04's acceptance and landed by the boundary after a04's merge; this task dispatches only after that boundary (the dispatch line names the record's hash); a finding outside the section is not owned here, and a missing or empty section at dispatch makes this task a no-op that report.md states (the section is created at the lineage's acceptance, so it does not exist before that). For each row: the rule sentence it names is corrected against the design on `main` (`.orchestration/tasks/dotfiles-T128-regime-v3-a01.md`, read from main) and the thread's text, with one token test per changed sentence in `tests/unit/test_agmsg_orchestration_docs.py` (and the fixture under `tests/fixtures/regime/` when the pinned section changes), in the style of a04's item 7; the RESULT lists each row with `fixed:<sha>`. The `procedure-migration` row (`audit:71eb920:1`) covers every sentence in this task's allowed files that still states the retired gate input (`AUDIT_DISPOSITIONS`, or the `audit-finding:` prose as what the gate reads), since the gate on main reads the acceptance record's JSON `audit_findings` (`{n, reason, evidence}`, PR #329): the step 10 lines the audit named, the task-level audit bullet of the SKILL, the AGENTS.md gate sentence, and the pinned fixture `tests/fixtures/regime/invariants.md` where `tests/unit/test_agmsg_orchestration_docs.py` holds them (the lines on `origin/main` at 26909ee4 and after are pasted in the Change section below); each changed sentence gets its token test as above (amendment 1, the worker's question of 06:50Z).
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
    72	
    73	## Change (amendment 1, 2026-10-14)
    74	
    75	Why: the worker's question (bus 1108, 06:50:50Z): two sentences outside SKILL lines 171 to 178 state the retired gate mechanism (`AUDIT_DISPOSITIONS`, the `audit-finding:` prose as the gate's input), the task-level audit bullet and AGENTS.md's gate sentence, and item 2 forbids sentences outside the owned rows. What changed: item 1 gained one sentence defining the `procedure-migration` row's scope as every such sentence in the allowed files, with the fixture, each with its token test; nothing else. The lines on `origin/main` (c15ba668) that the row now covers, pasted:
    76	
    77	```text
    78	$ git show origin/main:home/dot_agents/skills/agmsg-orchestration/SKILL.md | grep -n 'AUDIT_DISPOSITIONS\|audit-finding'
    79	90:  - The orchestrator dispositions every `[P0-P3]` finding in the acceptance record, whatever the verdict: exactly one `audit-finding: <n> …` line per finding
    80	171:    3. Write the acceptance record, summarising the dispositions, with an `audit-finding:` line for every audit finding whatever the verdict (the gate needs
    81	172:    4. Run the gate: `AUDIT_EVIDENCE=<audit> [AUDIT_DISPOSITIONS=<acceptance record>] AGENT_REVIEWED=1 REVIEW_EVIDENCE=<receipt> ACCEPTANCE_EVIDENCE=<accept
    82	178:       - `AUDIT_EVIDENCE` must be the task-level file `.orchestration/validation/<task>-audit-<sha7>.md` (the same `<task>` as the feedback JSON); a per-com
    83	$ git show origin/main:AGENTS.md | grep -n 'AUDIT_DISPOSITIONS'
    84	44:- Before merging a pull request, follow the integration order in the agmsg-orchestration SKILL's Orchestrator Playbook step 10 and `home/dot_config/claude/ru
    85	$ git show origin/main:tests/fixtures/regime/invariants.md | grep -n 'AUDIT_DISPOSITIONS\|audit-finding'
    86	27:  - The orchestrator dispositions every `[P0-P3]` finding in the acceptance record, whatever the verdict: exactly one `audit-finding: <n> …` line per finding
    87	```
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
    71	local:65a3d71:1	rule-gap
    72	audit:71eb920:1	procedure-migration (the SKILL step 10.4 gate command still names AUDIT_DISPOSITIONS; from the audit of PR #329's head)
    73	
    74	local-finding: 65a3d71:1 not-applicable:P1 by the post-round local review (SKILL.md:164: the rule requires dispatch logging into the current acceptance record and the tools refuse a missing record, but no sentence says the orchestrator creates the record before the first dispatch); plan 021 S21: the local review is a sampler and not the acceptance authority, so this finding is referred as input to the audit of this head, which decides; if the audit raises it as P0/P1 the PR stops (plan 020 step 4.2), otherwise it is advisory and owned by dotfiles-T128-playbook-rules-followup-a01; evidence=sed -n 1,20p .orchestration/validation/dotfiles-T128-playbook-rules-a04-local-review-65a3d71.md
    75	
    76	- 14:41Z audit of 65a3d71b (`dotfiles-T128-playbook-rules-a04-audit-65a3d71.md`): `Verdict: incorrect`, two P2, no P0/P1: (1) orchestration: thread 4250028600's `fixed:a03c1daa` cites a commit outside base..head (the gate rejects it); corrected to a `not-applicable` with evidence that the base contains the fix; (2) specification: the post-round local P1 (SKILL.md:164, the acceptance record's creation before the first dispatch is implicit) is judged advisory, owned by `dotfiles-T128-playbook-rules-followup-a01`, not merge-blocking; INV-2, INV-10, INV-12 hold on the head; all 47 documentation tests pass; CI 12 checks plus the CodeRabbit skip. Both dispositioned below; the chain continues to the gate and the merge.
    77	
    78	audit:65a3d71:1	disposition-range
    79	audit:65a3d71:2	rule-gap
    80	
    81	audit-finding: 1 not-applicable:corrected in the sweep table at 14:41Z: thread 4250028600 now reads not-applicable with the evidence that T718's squash a03c1daa is an ancestor of this PR's base 4e7a9b3a (the gate accepts fixed:<sha> only inside base..head); the re-run sweep carries the corrected row; evidence=grep -n 4250028600 .orchestration/validation/dotfiles-T128-playbook-rules-a04-pr-feedback.json
    82	audit-finding: 2 not-applicable:advisory per the audit itself (no P0/P1): the rule gap "the orchestrator creates the lineage's acceptance record before its first dispatch" is owned by dotfiles-T128-playbook-rules-followup-a01 (row local:65a3d71:1 under the owner heading of this record); evidence=git show origin/main:.orchestration/tasks/dotfiles-T128-playbook-rules-followup-a01.md | grep -n 'item 1'
    83	- 14:43:36Z **merged as `26909ee4`** (`gh pr merge --squash --match-head-commit 65a3d71b`) after the gate (rc=0; the sweep re-run after the 16 thread replies: 65 items, 0 gaps). ACCEPTANCE `accepted` sent to a003 (14:44Z). Cost line appended to `.orchestration/metrics/pr-cost.tsv`. The owner section carries one advisory row (local:65a3d71:1, the record-creation sentence) for `dotfiles-T128-playbook-rules-followup-a01`..claude/contextdb/contextdb/cli.py
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

**Ensuring controlled output**
codex
The diff’s rule edits stay within the dispatch and audit-disposition topics owned by this task. I’m checking the token tests and matching fixtures next. The GitHub CLI cannot connect from this sandbox, so I’m trying the read-only GitHub connector to verify final-head CI.
exec
/bin/zsh -lc "git show origin/main:.orchestration/acceptance/dotfiles-T128-playbook-rules-a04.md | nl -ba | sed -n '61,105p' && git show origin/main:.orchestration/tasks/dotfiles-T128-regime-v3-a01.md | nl -ba | sed -n '1,135p'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 20ms:
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
    71	local:65a3d71:1	rule-gap
    72	audit:71eb920:1	procedure-migration (the SKILL step 10.4 gate command still names AUDIT_DISPOSITIONS; from the audit of PR #329's head)
    73	
    74	local-finding: 65a3d71:1 not-applicable:P1 by the post-round local review (SKILL.md:164: the rule requires dispatch logging into the current acceptance record and the tools refuse a missing record, but no sentence says the orchestrator creates the record before the first dispatch); plan 021 S21: the local review is a sampler and not the acceptance authority, so this finding is referred as input to the audit of this head, which decides; if the audit raises it as P0/P1 the PR stops (plan 020 step 4.2), otherwise it is advisory and owned by dotfiles-T128-playbook-rules-followup-a01; evidence=sed -n 1,20p .orchestration/validation/dotfiles-T128-playbook-rules-a04-local-review-65a3d71.md
    75	
    76	- 14:41Z audit of 65a3d71b (`dotfiles-T128-playbook-rules-a04-audit-65a3d71.md`): `Verdict: incorrect`, two P2, no P0/P1: (1) orchestration: thread 4250028600's `fixed:a03c1daa` cites a commit outside base..head (the gate rejects it); corrected to a `not-applicable` with evidence that the base contains the fix; (2) specification: the post-round local P1 (SKILL.md:164, the acceptance record's creation before the first dispatch is implicit) is judged advisory, owned by `dotfiles-T128-playbook-rules-followup-a01`, not merge-blocking; INV-2, INV-10, INV-12 hold on the head; all 47 documentation tests pass; CI 12 checks plus the CodeRabbit skip. Both dispositioned below; the chain continues to the gate and the merge.
    77	
    78	audit:65a3d71:1	disposition-range
    79	audit:65a3d71:2	rule-gap
    80	
    81	audit-finding: 1 not-applicable:corrected in the sweep table at 14:41Z: thread 4250028600 now reads not-applicable with the evidence that T718's squash a03c1daa is an ancestor of this PR's base 4e7a9b3a (the gate accepts fixed:<sha> only inside base..head); the re-run sweep carries the corrected row; evidence=grep -n 4250028600 .orchestration/validation/dotfiles-T128-playbook-rules-a04-pr-feedback.json
    82	audit-finding: 2 not-applicable:advisory per the audit itself (no P0/P1): the rule gap "the orchestrator creates the lineage's acceptance record before its first dispatch" is owned by dotfiles-T128-playbook-rules-followup-a01 (row local:65a3d71:1 under the owner heading of this record); evidence=git show origin/main:.orchestration/tasks/dotfiles-T128-playbook-rules-followup-a01.md | grep -n 'item 1'
    83	- 14:43:36Z **merged as `26909ee4`** (`gh pr merge --squash --match-head-commit 65a3d71b`) after the gate (rc=0; the sweep re-run after the 16 thread replies: 65 items, 0 gaps). ACCEPTANCE `accepted` sent to a003 (14:44Z). Cost line appended to `.orchestration/metrics/pr-cost.tsv`. The owner section carries one advisory row (local:65a3d71:1, the record-creation sentence) for `dotfiles-T128-playbook-rules-followup-a01`.     1	---
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

**Checking token budget**
mcp: codex_apps/github.get_pr_info started
mcp: codex_apps/github.fetch_commit_workflow_runs started
mcp: codex_apps/github.get_commit_combined_status started
mcp: codex_apps/github.get_commit_combined_status (completed)
mcp: codex_apps/github.fetch_commit_workflow_runs (completed)
mcp: codex_apps/github.get_pr_info (completed)
exec
/bin/zsh -lc 'nl -ba .orchestration/validation/dotfiles-T128-playbook-rules-followup-a01-pr-feedback.json' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 0ms:
     1	{
     2	  "repo": "mryfmo/dotfiles",
     3	  "pr": 354,
     4	  "head_sha": "3a8f809b36944b0cb778da53104f9b3c54f67355",
     5	  "base_ref": "main",
     6	  "base_sha": "6a2473f362762cf74c750f2141e5a11853816745",
     7	  "generated_at": "2026-10-14T07:37:38+00:00",
     8	  "checks": [
     9	    {
    10	      "name": "public-bootstrap (ubuntu-24.04, server)",
    11	      "conclusion": "success",
    12	      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38528170006/job/115733387767"
    13	    },
    14	    {
    15	      "name": "private-bootstrap (macos-14, client)",
    16	      "conclusion": "success",
    17	      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38528170006/job/115733387697"
    18	    },
    19	    {
    20	      "name": "public-bootstrap (macos-14, client)",
    21	      "conclusion": "success",
    22	      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38528170006/job/115733387670"
    23	    },
    24	    {
    25	      "name": "private-bootstrap (ubuntu-24.04, client)",
    26	      "conclusion": "success",
    27	      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38528170006/job/115733387645"
    28	    },
    29	    {
    30	      "name": "private-bootstrap (ubuntu-24.04, server)",
    31	      "conclusion": "success",
    32	      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38528170006/job/115733387462"
    33	    },
    34	    {
    35	      "name": "test (macos-14, client)",
    36	      "conclusion": "success",
    37	      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38528169882/job/115733387456"
    38	    },
    39	    {
    40	      "name": "validate",
    41	      "conclusion": "success",
    42	      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38528170041/job/115733387255"
    43	    },
    44	    {
    45	      "name": "public-bootstrap (ubuntu-24.04, client)",
    46	      "conclusion": "success",
    47	      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38528170006/job/115733387212"
    48	    },
    49	    {
    50	      "name": "test (ubuntu-24.04, client)",
    51	      "conclusion": "success",
    52	      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38528169882/job/115733387173"
    53	    },
    54	    {
    55	      "name": "test (ubuntu-26.04, client)",
    56	      "conclusion": "success",
    57	      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38528169882/job/115733387107"
    58	    },
    59	    {
    60	      "name": "test (ubuntu-24.04, server)",
    61	      "conclusion": "success",
    62	      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38528169882/job/115733386989"
    63	    },
    64	    {
    65	      "name": "GitGuardian Security Checks",
    66	      "conclusion": "success",
    67	      "url": "https://github.com/mryfmo/dotfiles/runs/115733372329"
    68	    }
    69	  ],
    70	  "items": [
    71	    {
    72	      "source": "issue_comment",
    73	      "author": "coderabbitai[bot]",
    74	      "bot": true,
    75	      "level": "comment",
    76	      "path": null,
    77	      "line": null,
    78	      "body": "<!-- This is an auto-generated comment: summarize by coderabbit.ai -->\n<!-- This is an auto-generated comment: skip review by coderabbit.ai -->\n\n> [!IMPORTANT]\n> ## Review skipped\n> \n> Auto reviews are disabled on this repository. Please check the settings in the CodeRabbit UI or the `.coderabbit.yaml` file in this repository. To trigger a single review, invoke the `@coderabbitai review` command.\n> \n> <details>\n> <summary><strong>⚙️ Run configuration</strong></summary>\n> <dl>\n> <dd>\n> \n> - **Configuration used**: Repository: mryfmo/dotfiles/.coderabbit.yaml\n> - **Review profile**: CHILL\n> - **Plan**: Advanced\n> - **Run ID**: `2695824c-c80c-4865-8938-f09bb9a47197`\n> \n> </dd>\n> </dl>\n> </details>\n> \n> You can disable this status message by setting the `reviews.review_status` to `false` in the CodeRabbit configuration file.\n> \n> Use the checkbox below for a quick retry:\n> - [ ] <!-- {\"checkboxId\":\"e9bb8d72-00e8-4f67-9cb2-caf3b22574fe\"} --> 🔍 Trigger review\n\n<!-- end of auto-generated comment: skip review by coderabbit.ai -->\n\n<!-- autopilot:start -->\n- [ ] <!-- {\"checkboxId\":\"2708ad07-9f24-4260-9c11-7dc76a49f2e3\"} --> <strong title=\"Keep fixing CodeRabbit findings and required CI, and resolving merge conflicts\">Autofix</strong> · Keep fixing CodeRabbit findings and required CI, and resolving merge conflicts\n<!-- autopilot:end -->\n<!-- tips_start -->\n\n\n\nThanks for using [CodeRabbit](https://coderabbit.ai?utm_source=oss&utm_medium=github&utm_campaign=mryfmo/dotfiles&utm_content=354)! It's free for OSS, and your support helps us grow. If you like it, consider giving us a shout-out.\n\n<details>\n<summary><strong>❤️ Share</strong></summary>\n<dl>\n<dd>\n\n- [X](https://twitter.com/intent/tweet?text=I%20just%20used%20%40coderabbitai%20for%20my%20code%20review%2C%20and%20it%27s%20fantastic%21%20It%27s%20free%20for%20OSS%20and%20offers%20a%20free%20trial%20for%20the%20proprietary%20code.%20Check%20it%20out%3A&url=https%3A//coderabbit.ai)\n- [Mastodon](https://mastodon.social/share?text=I%20just%20used%20%40coderabbitai%20for%20my%20code%20review%2C%20and%20it%27s%20fantastic%21%20It%27s%20free%20for%20OSS%20and%20offers%20a%20free%20trial%20for%20the%20proprietary%20code.%20Check%20it%20out%3A%20https%3A%2F%2Fcoderabbit.ai)\n- [Reddit](https://www.reddit.com/submit?title=Great%20tool%20for%20code%20review%20-%20CodeRabbit&text=I%20just%20used%20CodeRabbit%20for%20my%20code%20review%2C%20and%20it%27s%20fantastic%21%20It%27s%20free%20for%20OSS%20and%20offers%20a%20free%20trial%20for%20proprietary%20code.%20Check%20it%20out%3A%20https%3A//coderabbit.ai)\n- [LinkedIn](https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Fcoderabbit.ai&mini=true&title=Great%20tool%20for%20code%20review%20-%20CodeRabbit&summary=I%20just%20used%20CodeRabbit%20for%20my%20code%20review%2C%20and%20it%27s%20fantastic%21%20It%27s%20free%20for%20OSS%20and%20offers%20a%20free%20trial%20for%20proprietary%20code)\n\n</dd>\n</dl>\n</details>\n\n\n<sub>Comment `@coderabbitai help` to get the list of available commands.</sub>\n\n<!-- tips_end -->",
    79	      "url": "https://github.com/mryfmo/dotfiles/pull/354#issuecomment-6162903249",
    80	      "disposition": "not-applicable:bot summary or onboarding comment, no finding; evidence=gh api repos/mryfmo/dotfiles/issues/comments/6162903249 --jq '.user.login,.body'"
    81	    },
    82	    {
    83	      "source": "issue_comment",
    84	      "author": "chatgpt-codex-connector[bot]",
    85	      "bot": true,
    86	      "level": "comment",
    87	      "path": null,
    88	      "line": null,
    89	      "body": "<!-- codex-pull-request-review-summary -->\n<!-- codex-security-review:v1 {\"blockingSeverityThreshold\":\"P0\",\"headSha\":\"bd9e8a69606b03a54973bd631baa25ed07b6d247\",\"mergeGateEnabled\":false,\"pullRequestNumber\":354,\"repository\":\"mryfmo/dotfiles\",\"status\":\"completed\"} -->\n## Codex Review Summary\n\nThis comment shows the latest Codex review activity on this pull request.\n\n| Review | Status | Commit | Review trigger |\n| --- | --- | --- | --- |\n| 📝 **Code Review** | ✅ **Completed** <relative-time datetime=\"2026-10-14T07:19:54.469954Z\">2026-10-14T07:19:54.469954Z</relative-time> | `bd9e8a6` | Manual request |\n| 🔒 **Security Review** | ✅ **Completed** <relative-time datetime=\"2026-10-14T07:12:53.951588Z\">2026-10-14T07:12:53.951588Z</relative-time> | `bd9e8a6` | Draft marked ready |\n\n\n\n<details> <summary>ℹ️ About Codex in GitHub</summary>\n<br/>\n\n[Your team has set up Codex to review pull requests in this repo](https://chatgpt.com/codex/cloud/settings/general). Reviews are triggered when you\n- Open a pull request for review\n- Mark a draft as ready\n- Comment \"@codex review\" or \"@codex security review\".\n\nCodex reacts with 👀 while any review is running, comments if it has suggestions, and reacts with 👍 once all reviews finish with no findings.\n\n</details>",
    90	      "url": "https://github.com/mryfmo/dotfiles/pull/354#issuecomment-6162906130",
    91	      "disposition": "not-applicable:bot summary or onboarding comment, no finding; evidence=gh api repos/mryfmo/dotfiles/issues/comments/6162906130 --jq '.user.login,.body'"
    92	    },
    93	    {
    94	      "source": "issue_comment",
    95	      "author": "moriya-fumio-thd",
    96	      "bot": false,
    97	      "level": "comment",
    98	      "path": null,
    99	      "line": null,
   100	      "body": "@codex review",
   101	      "url": "https://github.com/mryfmo/dotfiles/pull/354#issuecomment-6163057197",
   102	      "disposition": "not-applicable:bot summary or onboarding comment, no finding; evidence=gh api repos/mryfmo/dotfiles/issues/comments/6163057197 --jq '.user.login,.body'"
   103	    },
   104	    {
   105	      "source": "issue_comment",
   106	      "author": "chatgpt-codex-connector[bot]",
   107	      "bot": true,
   108	      "level": "comment",
   109	      "path": null,
   110	      "line": null,
   111	      "body": "Codex Review: Didn't find any major issues. What shall we delve into next?\n\n**Reviewed commit:** `bd9e8a6960`\n\n<details> <summary>ℹ️ About Codex in GitHub</summary>\n<br/>\n\nCodex has been enabled to automatically review pull requests in this repo. Reviews are triggered when you\n- Open a pull request for review\n- Mark a draft as ready\n- Comment \"@codex review\".\n\nIf Codex has suggestions, it will comment; otherwise it will react with 👍.\n\n\n\n\nWhen you [sign up for Codex through ChatGPT](https://openai.com/codex), Codex can also answer questions or update the PR, like \"@codex address that feedback\".\n            \n</details>",
   112	      "url": "https://github.com/mryfmo/dotfiles/pull/354#issuecomment-6163090018",
   113	      "disposition": "not-applicable:bot summary or onboarding comment, no finding; evidence=gh api repos/mryfmo/dotfiles/issues/comments/6163090018 --jq '.user.login,.body'"
   114	    },
   115	    {
   116	      "source": "annotation",
   117	      "author": "github-actions",
   118	      "bot": true,
   119	      "level": "notice",
   120	      "path": ".github",
   121	      "line": 1,
   122	      "body": "Due to capacity constraints, jobs targeting macOS arm64 runners may experience longer queue times.",
   123	      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38528170006/job/115733387697",
   124	      "check": "private-bootstrap (macos-14, client)",
   125	      "disposition": "not-applicable:runner capacity notice, no finding; evidence=gh run view 38528170006 --repo mryfmo/dotfiles --job 115733387697"
   126	    },
   127	    {
   128	      "source": "annotation",
   129	      "author": "github-actions",
   130	      "bot": true,
   131	      "level": "notice",
   132	      "path": ".github",
   133	      "line": 1,
   134	      "body": "Due to capacity constraints, jobs targeting macOS arm64 runners may experience longer queue times.",
   135	      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38528170006/job/115733387670",
   136	      "check": "public-bootstrap (macos-14, client)",
   137	      "disposition": "not-applicable:runner capacity notice, no finding; evidence=gh run view 38528170006 --repo mryfmo/dotfiles --job 115733387670"
   138	    },
   139	    {
   140	      "source": "annotation",
   141	      "author": "github-actions",
   142	      "bot": true,
   143	      "level": "notice",
   144	      "path": ".github",
   145	      "line": 1,
   146	      "body": "Due to capacity constraints, jobs targeting macOS arm64 runners may experience longer queue times.",
   147	      "url": "https://github.com/mryfmo/dotfiles/actions/runs/38528169882/job/115733387456",
   148	      "check": "test (macos-14, client)",
   149	      "disposition": "not-applicable:runner capacity notice, no finding; evidence=gh run view 38528169882 --repo mryfmo/dotfiles --job 115733387456"
   150	    },
   151	    {
   152	      "source": "status",
   153	      "author": "coderabbitai[bot]",
   154	      "bot": true,
   155	      "level": "success",
   156	      "path": null,
   157	      "line": null,
   158	      "body": "CodeRabbit: Review skipped: automatic reviews are disabled",
   159	      "url": null,
   160	      "check": "CodeRabbit",
   161	      "disposition": "not-applicable:CI status, no finding; evidence=gh pr checks 354 --repo mryfmo/dotfiles"
   162	    }
   163	  ]
   164	}

**Reviewing task invariants and audit checks**
exec
/bin/zsh -lc "git show origin/main:scripts/require-crit-review.py | rg -n 'audit_findings|AUDIT_DISPOSITIONS|ACCEPTANCE_EVIDENCE|audit.disposition|incorrect|evidence|len\\(reason'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc 'nl -ba .orchestration/reports/dotfiles-T128-playbook-rules-followup-a01.md && nl -ba .orchestration/validation/dotfiles-T128-playbook-rules-followup-a01.md' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
exec
/bin/zsh -lc 'git show origin/main:scripts/orchestrator/dispatch.sh | nl -ba && git show origin/main:scripts/orchestrator/acceptance-front-matter.py | nl -ba' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 107ms:
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
    37	#   Only a bus row this send created is recorded: the rows matching the line,
    38	#   sender and recipient are counted before and after the send, and a send that
    39	#   added none leaves the record unchanged and exits 1. The read state is the
    40	#   marker the team-wide `history.sh <team> "" <BUS_READ_LIMIT>` prints for the new row
    41	#   (`●` unread, `○` read): agmsg's scripts expose no read_at time, this script
    42	#   never reads the message database, and it never passes an agent to
    43	#   history.sh, whose agent argument renames the caller's pane after it. A read
    44	#   whose non-empty lines reach the limit may have lost its oldest rows, so it
    45	#   is refused before the send (thread 4255272803).
    46	# @arg $1 string agmsg team.
    47	# @arg $2 string Sender identity.
    48	# @arg $3 string Recipient identity.
    49	# @arg $4 string Recipient pane id (for example `w5:pA`).
    50	# @arg $5 path File holding the line.
    51	# @arg $6 path Optional acceptance record (`.orchestration/acceptance/<task>.md`), relative to the current directory.
    52	# @env AGMSG_SCRIPTS The agmsg scripts directory (default `$HOME/.agents/skills/agmsg/scripts`).
    53	# @env BUS_READ_LIMIT The row limit of the history read (default 100000).
    54	# @exitcode 0 Sent, and recorded when a record was given (agmsg-dispatch's own status otherwise).
    55	# @exitcode 1 A field check failed, the record is malformed, or the sent line was not recorded.
    56	# @exitcode 2 Usage error, or the file is not one AGMSG-TASK, AGMSG-ACCEPTANCE or AGMSG-PING v1 line.
    57	# @example
    58	#   scripts/orchestrator/dispatch.sh dotfiles-conformance claude-deep-dot claude-standard-dot-a003 w5:pA \
    59	#     "$TMPDIR/task-line.txt" .orchestration/acceptance/dotfiles-T128-orchestrator-tools-a01.md
    60	set -euo pipefail
    61	
    62	usage() {
    63	    echo "usage: dispatch.sh <team> <from> <to> <pane> <line-file> [<acceptance-record>]" >&2
    64	    exit 2
    65	}
    66	(($# == 5 || $# == 6)) || usage
    67	team=$1 from=$2 to=$3 pane=$4 file=$5 record=${6:-}
    68	[[ -f ${file} ]] || usage
    69	# Thread 4256541716: command substitution drops a NUL byte, so the line sent would not be the file's.
    70	if (($(tr -d '\0' < "${file}" | wc -c) != $(wc -c < "${file}"))); then
    71	    echo "dispatch: ${file} holds a NUL byte" >&2
    72	    exit 2
    73	fi
    74	# The sentinel keeps every trailing newline, which $( ) alone would drop (thread 4254107304).
    75	line="$(cat -- "${file}" && printf x)" && line=${line%x} && line=${line%$'\n'}
    76	[[ ${line} != *$'\n'* ]] || {
    77	    echo "dispatch: ${file} holds more than one line" >&2
    78	    exit 2
    79	}
    80	[[ ${line} =~ ^AGMSG-(TASK|ACCEPTANCE|PING)[[:blank:]]+v1[[:blank:]] ]] || {
    81	    echo "dispatch: not an AGMSG-TASK, AGMSG-ACCEPTANCE or AGMSG-PING v1 line" >&2
    82	    exit 2
    83	}
    84	root="$(git -C "$(dirname -- "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
    85	
    86	read -ra tokens <<< "${line}"
    87	for t in "${tokens[@]:2}"; do
    88	    [[ ${t} == *=* ]] || {
    89	        echo "dispatch: ${t} is not a <key>=<value> token" >&2
    90	        exit 2
    91	    }
    92	done
    93	# @description Print the value of the first `<key>=` token, or fail.
    94	# @arg $1 string Key.
    95	value_of() {
    96	    local t
    97	    for t in "${tokens[@]}"; do
    98	        [[ ${t} == "$1="* ]] && printf '%s' "${t#*=}" && return 0
    99	    done
   100	    return 1
   101	}
   102	# @description Print how many tokens carry `<key>=`.
   103	# @arg $1 string Key.
   104	count_of() {
   105	    local t n=0
   106	    for t in "${tokens[@]}"; do
   107	        [[ ${t} == "$1="* ]] && n=$((n + 1))
   108	    done
   109	    printf '%s' "${n}"
   110	}
   111	# Thread 4254893065: every message names exactly one task, before any hash or record work.
   112	if (($(count_of task_id) != 1)) || [[ -z "$(value_of task_id)" ]]; then
   113	    echo "dispatch: the line needs exactly one non-empty task_id=" >&2
   114	    exit 1
   115	fi
   116	# Thread 4254163604: a TASK whose file is not hash-bound is never sent. The kind is the parsed
   117	# first token, so a tab after it does not skip this check (thread 4260535901).
   118	if [[ ${tokens[0]} == AGMSG-TASK ]]; then
   119	    for field in task_file task_sha256; do
   120	        value_of "${field}" > /dev/null || {
   121	            echo "dispatch: an AGMSG-TASK line needs ${field}=" >&2
   122	            exit 1
   123	        }
   124	    done
   125	fi
   126	for t in "${tokens[@]}"; do
   127	    # Thread 4254771302: any name before _sha256=, digits included (a02_expected_sha256=).
   128	    [[ ${t} =~ ^([^=]+)_sha256=(.*)$ ]] || continue
   129	    name=${BASH_REMATCH[1]} want=${BASH_REMATCH[2]}
   130	    field="${name}_sha256"
   131	    [[ ${want} =~ ^[0-9a-f]{64}$ ]] || {
   132	        echo "dispatch: ${field} is not 64 lowercase hex digits" >&2
   133	        exit 1
   134	    }
   135	    # Thread 4256541725: a previous_<name>_sha256= reference names no file here (a02 item 4's grammar row).
   136	    if [[ ${name} == previous_* ]]; then
   137	        continue
   138	    fi
   139	    # Thread 4254494989: a repeated key leaves a second, unhashed value in the line.
   140	    for key in "${field}" "${name}_file" "${name}"; do
   141	        (($(count_of "${key}") <= 1)) || {
   142	            echo "dispatch: ${field}: ${key}= appears more than once" >&2
   143	            exit 1
   144	        }
   145	    done
   146	    if value_of "${name}_file" > /dev/null && value_of "${name}" > /dev/null; then
   147	        echo "dispatch: ${field}: both ${name}_file= and ${name}= name a file" >&2
   148	        exit 1
   149	    fi
   150	    path="$(value_of "${name}_file" || value_of "${name}")" || {
   151	        echo "dispatch: ${field} has no ${name}_file= or ${name}= field naming its file" >&2
   152	        exit 1
   153	    }
   154	    [[ ${path} == /* ]] || path="${root}/${path}"
   155	    [[ -f ${path} ]] || {
   156	        echo "dispatch: ${field}: ${path} does not exist" >&2
   157	        exit 1
   158	    }
   159	    got="$(shasum -a 256 "${path}")" && got=${got%% *}
   160	    [[ ${got} == "${want}" ]] || {
   161	        echo "dispatch: ${field} mismatch: the line has ${want}, ${path} hashes to ${got}" >&2
   162	        exit 1
   163	    }
   164	done
   165	[[ -n ${record} ]] || exec agmsg-dispatch "${team}" "${from}" "${to}" "${pane}" "${line}"
   166	
   167	# Modes: `check` parses the record; `append` finds the sent line in history.sh's
   168	# output on stdin, takes its read marker (● unread, ○ read) and appends it.
   169	read -r -d '' recorder << 'PY' || true
   170	import fcntl, json, os, re, shutil, sys, tempfile
   171	from pathlib import Path
   172	
   173	mode, path, line, sender, to, before, task, limit = sys.argv[1:9]
   174	record = Path(path)
   175	rows = [r for r in sys.stdin.read().splitlines() if r]
   176	
   177	def refuse(pairs):
   178	    keys = [k for k, _ in pairs]
   179	    dup = next((k for k in keys if keys.count(k) > 1), None)
   180	    if dup is not None:
   181	        sys.exit(f"dispatch: {path}: duplicate key {dup}")
   182	    return dict(pairs)
   183	
   184	def constant(name):
   185	    sys.exit(f"dispatch: {path}: non-finite number {name}")
   186	
   187	def load():
   188	    # newline="": a CRLF record keeps its line endings (thread 4256987087).
   189	    with open(record, newline="") as f:
   190	        text = f.read()
   191	    block, rest = {}, text
   192	    if re.match(r"---\r?\n", text):
   193	        m = re.match(r"---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
   194	        if not m:
   195	            sys.exit(f"dispatch: {path}: the block between the first two --- lines is not closed")
   196	        try:
   197	            block = json.loads(m.group(1), object_pairs_hook=refuse, parse_constant=constant)
   198	        except json.JSONDecodeError as e:
   199	            sys.exit(f"dispatch: {path}: the block is not valid JSON: {e}")
   200	        rest = text[m.end():]
   201	        if not isinstance(block, dict):
   202	            sys.exit(f"dispatch: {path}: the block is not a JSON object")
   203	    if not isinstance(block.setdefault("dispatch", []), list):
   204	        sys.exit(f"dispatch: {path}: dispatch is not a list")
   205	    # Thread 4254844587: another task's record never takes this task's dispatch.
   206	    if "task" in block and block["task"] != task:
   207	        sys.exit(f"dispatch: {path} is the record of task {block['task']}, the line is task {task}")
   208	    return block, rest
   209	
   210	row = re.compile(r"^\s*(\S+)\s+\[[^\]]+\]\s+(\S+)\s+→\s+(\S+):\s(.*)$")
   211	marks = [m.group(1) for m in map(row.match, rows) if m and (m.group(2), m.group(3), m.group(4)) == (sender, to, line)]
   212	if mode == "check":
   213	    load()
   214	    if len(rows) >= int(limit):
   215	        sys.exit(f"dispatch: the history read is capped at {limit} rows; raise BUS_READ_LIMIT")
   216	    print(len(marks))
   217	    sys.exit(0)
   218	# Thread 4255272797: the read-modify-write holds the record directory's lock, so a second dispatch waits.
   219	lock = os.open(record.parent, os.O_RDONLY)
   220	fcntl.flock(lock, fcntl.LOCK_EX)
   221	block, rest = load()
   222	# Thread 4254399807: an older identical row is not this send.
   223	if len(marks) <= int(before):
   224	    sys.exit(f"dispatch: this send added no bus row; {path} is unchanged")
   225	block["dispatch"].append(f"{line} read_at={'read' if marks[-1] == '○' else 'unread'}")
   226	body = json.dumps(block, sort_keys=True, indent=2, ensure_ascii=False)
   227	# Thread 4254844595: the line is already sent, so the record is replaced whole or not at all.
   228	fd, tmp = tempfile.mkstemp(dir=record.parent, prefix=f".{record.name}.")
   229	try:
   230	    with os.fdopen(fd, "w", newline="") as f:
   231	        f.write(f"---\n{body}\n---\n{rest}")
   232	        f.flush()
   233	        os.fsync(f.fileno())
   234	    shutil.copymode(record, tmp)
   235	    os.replace(tmp, record)
   236	except BaseException:
   237	    Path(tmp).unlink(missing_ok=True)
   238	    raise
   239	PY
   240	[[ ${record} == /* ]] || record="${PWD}/${record}"
   241	# The local review of 0d199475 (C-32): a record mkstemp cannot replace would fail only after the send.
   242	if [[ ! -f ${record} || ! -w ${record} || ! -w "$(dirname -- "${record}")" ]]; then
   243	    echo "dispatch: the record ${record} cannot be written" >&2
   244	    exit 1
   245	fi
   246	limit=${BUS_READ_LIMIT:-100000}
   247	[[ ${limit} =~ ^[1-9][0-9]*$ ]] || usage
   248	task="$(value_of task_id)"
   249	# Team-wide: history.sh renames the calling pane after an agent argument (thread 4254399805).
   250	bus() { "${AGMSG_SCRIPTS:-${HOME}/.agents/skills/agmsg/scripts}/history.sh" "${team}" "" "${limit}"; }
   251	before="$(bus | python3 -I -c "${recorder}" check "${record}" "${line}" "${from}" "${to}" 0 "${task}" "${limit}")"
   252	rc=0
   253	agmsg-dispatch "${team}" "${from}" "${to}" "${pane}" "${line}" || rc=$?
   254	bus | python3 -I -c "${recorder}" append "${record}" "${line}" "${from}" "${to}" "${before}" "${task}" "${limit}"
   255	exit "${rc}"
     1	"""acceptance-front-matter.py <task> <sweep-json> <pr-worktree> [--ledger <tsv>] [--audit-dispositions <tsv>]
     2	
     3	Write or update the JSON block of `.orchestration/acceptance/<task>.md` in this checkout (plan 007 T718, a05 item 1;
     4	plan 013 A′, C-24, C-26): the object between the record's first two `---` lines that the gate reads. `head` is
     5	`git -C <pr-worktree> rev-parse HEAD` and must equal the sweep JSON's `head_sha`; `pr` is the sweep JSON's own `pr`.
     6	`ledger` keeps every row the record has and adds each `--ledger` row (`id<TAB>class`) whose id is new; a row whose
     7	id is present is printed as kept-ledger-row. `searches` is recomputed by the gate's rule: each class with three or
     8	more rows, with the sorted basenames of the mistake records naming it. `audit_findings` come from
     9	`--audit-dispositions` (`n<TAB>reason<TAB>evidence`), required when the audit summary orch-audit.sh writes beside
    10	its receipt (`.orchestration/validation/<task>-audit-<sha7>.md.last.md`) ends in `Verdict: incorrect`, refused
    11	otherwise; the record is written before the audit (the audit reads it) and again after an incorrect one. A record
    12	that starts with a `---` block is read with the gate module's reader (duplicate keys refused) and keeps its text
    13	after the block and its `dispatch` list; a prose record gets the block prepended. The gate module's field checks
    14	run on the new block, and any refusal exits 1 before anything is written.
    15	"""
    16	
    17	import argparse
    18	import collections
    19	import importlib.util
    20	import json
    21	import re
    22	import subprocess
    23	import sys
    24	from pathlib import Path
    25	
    26	
    27	def refuse(message):
    28	    sys.exit(f"acceptance-front-matter: {message}; nothing written")
    29	
    30	
    31	def git(*args):
    32	    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout.strip()
    33	
    34	
    35	def rows(path, width):
    36	    """The `width`-field rows of a TSV file, blank and `#` lines skipped."""
    37	    lines = Path(path).read_text().splitlines() if path else []
    38	    found = [line.split("\t") for line in lines if line.strip() and not line.startswith("#")]
    39	    for fields in found:
    40	        if len(fields) != width:
    41	            refuse(f"{path}: a row needs {width} tab-separated fields: {fields!r}")
    42	    return found
    43	
    44	
    45	def main():
    46	    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    47	    parser.add_argument("task")
    48	    parser.add_argument("sweep")
    49	    parser.add_argument("pr_worktree")
    50	    parser.add_argument("--ledger")
    51	    parser.add_argument("--audit-dispositions")
    52	    args = parser.parse_args()
    53	    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", args.task):
    54	        parser.error(f"not a task id: {args.task!r}")
    55	    root = Path(git("-C", str(Path(__file__).resolve().parent), "rev-parse", "--show-toplevel"))
    56	    spec = importlib.util.spec_from_file_location("require_crit_review", root / "scripts/require-crit-review.py")
    57	    gate = importlib.util.module_from_spec(spec)
    58	    spec.loader.exec_module(gate)
    59	
    60	    try:
    61	        sweep = json.loads(Path(args.sweep).read_text(), object_pairs_hook=gate.refuse_duplicate_keys)
    62	    except ValueError as error:
    63	        refuse(f"{args.sweep}: {error}")
    64	    head = git("-C", args.pr_worktree, "rev-parse", "HEAD")
    65	    if sweep.get("head_sha") != head:
    66	        refuse(f"the sweep was collected for head {sweep.get('head_sha')!r}, not {args.pr_worktree}'s HEAD {head}")
    67	
    68	    path = root / ".orchestration/acceptance" / f"{args.task}.md"
    69	    text = path.read_text() if path.is_file() else ""
    70	    record, rest = {}, text
    71	    if text.split("\n")[0] == "---":
    72	        record, error = gate.read_acceptance_record(path)
    73	        if error:
    74	            refuse(error)
    75	        lines = text.split("\n")
    76	        rest = "\n".join(lines[lines.index("---", 1) + 1 :])
    77	
    78	    ledger = list(record.get("ledger", []))
    79	    present = {str(row.get("id")) for row in ledger if isinstance(row, dict)}
    80	    for row_id, cls in rows(args.ledger, 2):
    81	        if row_id in present:
    82	            print("kept-ledger-row", row_id)
    83	        else:
    84	            ledger.append({"id": row_id, "class": cls})
    85	            present.add(row_id)
    86	
    87	    summary = root / f".orchestration/validation/{args.task}-audit-{head[:7]}.md.last.md"
    88	    audit = summary.read_text() if summary.is_file() else ""
    89	    # The gate's verdict rule: the summary's last non-blank line.
    90	    last = [line for line in audit.splitlines() if line.strip()][-1:]
    91	    verdict = (match := gate.AUDIT_VERDICT.fullmatch(last[0]) if last else None) and match.group(1)
    92	    incorrect = verdict == "incorrect"
    93	    if incorrect != (args.audit_dispositions is not None):
    94	        refuse(
    95	            f"--audit-dispositions is {'required' if incorrect else 'refused'}: {summary.name} {verdict or 'missing'}"
    96	        )
    97	    findings = [
    98	        {"n": n, "reason": reason, "evidence": evidence} for n, reason, evidence in rows(args.audit_dispositions, 3)
    99	    ]
   100	
   101	    classes = collections.Counter(
   102	        row["class"] for row in ledger if isinstance(row, dict) and isinstance(row.get("class"), str)
   103	    )
   104	    searches = []
   105	    for cls in sorted(c for c, count in classes.items() if count >= gate.S6_CLASS_LIMIT):
   106	        found = gate.mistake_records(root, cls)
   107	        if isinstance(found, str):
   108	            refuse(found)
   109	        searches.append({"class": cls, "records": sorted(found)})
   110	
   111	    block = {**record, "format": gate.RECORD_FORMAT, "task": args.task, "head": head, "pr": sweep.get("pr")}
   112	    block.update(ledger=ledger, searches=searches, audit_findings=findings)
   113	    errors = gate.record_field_errors(block, args.task, head, sweep.get("pr"))
   114	    if not errors and incorrect:
   115	        errors = gate.audit_findings_errors(block, len(gate.AUDIT_FINDING.findall(audit)))
   116	    if errors:
   117	        refuse("; ".join(errors))
   118	    path.parent.mkdir(parents=True, exist_ok=True)
   119	    path.write_text("---\n" + json.dumps(block, indent=2, sort_keys=True, ensure_ascii=False) + "\n---\n" + rest)
   120	    print("written", path.relative_to(root), "head", head[:7], "pr", block["pr"], "ledger", len(ledger))
   121	
   122	
   123	if __name__ == "__main__":
   124	    main()

 succeeded in 141ms:
25:# Retired: an incorrect audit's findings are dispositioned in the acceptance record's `audit_findings`.
26:RETIRED_AUDIT_DISPOSITIONS_ENV = "AUDIT_DISPOSITIONS"
27:ACCEPTANCE_ENV = "ACCEPTANCE_EVIDENCE"
31:EVIDENCE_DELIMITER = "; evidence="
32:DISPOSITION_GRAMMAR = "fixed:<commit> or not-applicable:<reason>; evidence=<command>"
38:AUDIT_FINDING_KEYS = {"n", "reason", "evidence"}
39:# Every audit_findings field is a non-empty string; n holds the finding number in ASCII digits.
41:RECORD_KEYS = {"format", "task", "head", "pr", "ledger", "searches", "audit_findings", "dispatch"}
49:AUDIT_VERDICT = re.compile(r"\s*Verdict: (correct|incorrect|blocked)\s*")
153:    """Skip worklogs and the PR feedback and acceptance evidence files themselves when sizing a diff."""
157:        (PR_FEEDBACK_ENV, lambda evidence_path: feedback_path_error(root, evidence_path)),
160:            lambda evidence_path: orchestration_path_error(root, evidence_path, ACCEPTANCE_ENV, "acceptance"),
163:        evidence = os.environ.get(env, "").strip()
164:        if not evidence:
166:        evidence_path = Path(evidence)
167:        if not evidence_path.is_absolute():
168:            evidence_path = root / evidence_path
169:        if path_error(evidence_path) is None and feedback_relative_path(root, evidence_path) == Path(path):
180:    raise ValueError("evidence is outside the repository")
195:        return "evidence must live under .orchestration/validation/ and end with -pr-feedback.json"
285:def resolve_evidence_path(root: Path) -> Path | None:
286:    evidence = os.environ.get(EVIDENCE_ENV, "").strip()
287:    if not evidence:
289:    path = Path(evidence)
295:def evidence_errors(root: Path, marker: str) -> list[str]:
296:    path = resolve_evidence_path(root)
302:    parsed_fields = {field: evidence_field(text, field) for field in REQUIRED_EVIDENCE_FIELDS}
335:    source = evidence_field(text, CRIT_DATA_SOURCE_FIELD)
351:        return [f"{CRIT_DATA_SOURCE_FIELD} must point to a repo-local JSON evidence file"]
354:        return [f"{CRIT_DATA_SOURCE_FIELD} JSON evidence file does not exist: {path}"]
393:    """Read `fixed:<commit>` as (commit, "") or `not-applicable:<reason>; evidence=<command>` as (None, reason)."""
408:    evidence = os.environ.get(PR_FEEDBACK_ENV, "").strip()
409:    if not evidence:
413:    path = Path(evidence)
460:        if item.get("level") in STRICT_REASON_LEVELS and not commit and len(reason) < FAILURE_REASON_MIN_CHARS:
484:    values of a JSON file) is the repository's documented way to keep evidence
512:def pr_base_errors(root: Path, evidence: dict, pr: int, head: str, base: str) -> list[str]:
530:        if evidence.get("repo") != repo:
559:    if evidence.get("base_sha") != github_base or evidence.get("base_ref") != github_ref:
584:def collected_feedback_errors(root: Path, evidence: dict, head: str, base: str) -> list[str]:
585:    """Re-collect the PR's feedback and require every current item in the evidence.
589:    evidence's PR, requires the PR head on GitHub to be this HEAD, and requires
594:    pr = evidence.get("pr")
597:    errors = pr_base_errors(root, evidence, pr, head, base)
605:        base_collector = run_git(["show", f"{evidence['base_sha']}:scripts/pr-feedback.py"], root)
610:            [sys.executable, str(collector), str(pr), "--repo", evidence["repo"], "--json", str(collected_path)],
623:    if collected.get("repo") != evidence["repo"]:
624:        return [f"collected feedback does not match the local GitHub repository {evidence['repo']}"]
625:    missing = missing_feedback(collected.get("items", []), evidence.get("items", []))
657:    """Require the task-level audit of HEAD for task: `correct`, or `incorrect` with every finding in audit_findings."""
658:    evidence = os.environ.get(AUDIT_ENV, "").strip()
659:    if not evidence:
663:    path = Path(evidence)
697:    if verdict != "incorrect":
701:        return [f"{AUDIT_ENV} verdict is incorrect but {source} lists no [P0-P3] finding to disposition"]
702:    return audit_findings_errors(record, findings)
705:def audit_findings_errors(record: dict | None, findings: int) -> list[str]:
706:    """An incorrect audit needs one `audit_findings` entry per finding 1..N (each entry's shape is checked on load)."""
707:    entries = (record or {}).get("audit_findings")
710:            f"{AUDIT_ENV} verdict is incorrect: the acceptance record's audit_findings must disposition its {findings} finding(s)"
714:        f"audit_findings dispositions finding {n} more than once" for n in sorted(set(numbers)) if numbers.count(n) > 1
717:        f"audit_findings names finding {n}, but the audit lists {findings}"
724:            f"audit_findings leaves audit finding(s) {', '.join(map(str, missing))} of {findings} without a disposition; add one {{n, reason, evidence}} entry per finding"
771:    """Check the identity triple (task, head, pr) first, then format, ledger, searches and audit_findings."""
831:    findings = record.get("audit_findings")
833:        errors.append("audit_findings must be a list of {n, reason, evidence} entries")
836:            errors.append(f"audit_findings entry {index} cites a fix; a fix moves HEAD, so audit the new head instead")
842:            or not is_text(entry["evidence"])
845:                f"audit_findings entry {index} must be {{n: <finding number>, reason: <text>, evidence: <command>}}, each a non-empty string"
849:                f"audit_findings entry {index} needs a reason of at least {FAILURE_REASON_MIN_CHARS} characters"
953:def evidence_field(text: str, field: str) -> str | None:
983:        help="also review committed changes in <base>...HEAD and require PR_FEEDBACK_EVIDENCE and ACCEPTANCE_EVIDENCE, plus AUDIT_EVIDENCE when review is required (PR integration)",
999:        print("PR feedback evidence is incomplete; run scripts/pr-feedback.py and disposition every item.")
1005:            print(f"PR feedback evidence accepted: {os.environ[PR_FEEDBACK_ENV].strip()}")
1008:                f"PR feedback evidence format checked only: {os.environ[PR_FEEDBACK_ENV].strip()}"
1027:        print("Acceptance record evidence is incomplete:")
1032:        print(f"Acceptance evidence accepted: {os.environ[ACCEPTANCE_ENV].strip()}")
1033:    if os.environ.get(RETIRED_AUDIT_DISPOSITIONS_ENV, "").strip():
1035:            f"{RETIRED_AUDIT_DISPOSITIONS_ENV} is retired and not read: the acceptance record's audit_findings disposition an incorrect audit."
1047:            print("Task-level audit evidence is required for PR integration of this change:")
1051:        print(f"Audit evidence accepted: {os.environ[AUDIT_ENV].strip()}")
1055:        errors = evidence_errors(root, marker)
1059:        print(f"{marker} requires review evidence before completion.")
1078:    print("This local evidence is process evidence, not reviewer authentication.")

 succeeded in 153ms:
     1	---
     2	task_id: dotfiles-T128-playbook-rules-followup-a01
     3	seat: claude-standard-dot-a002
     4	branch: regime/playbook-rules-followup
     5	base: c15ba668da20dc2956220077cb0f20054ab352c7
     6	rule_commit: 7a282f3b
     7	task_sha256: ec415eaf526937fd43907a59fccfc455de117850003ba3d48cd20b065fc5564b
     8	---
     9	
    10	# Report: dotfiles-T128-playbook-rules-followup-a01
    11	
    12	- Seat: `claude-standard-dot-a002` in `.claude/worktrees/worker-f`, on a fresh branch `regime/playbook-rules-followup` from `origin/main` `c15ba668`. The task-checkers branch stays as it is.
    13	- Task file: amendment 1, sha256 `ec415eaf…`, copied byte-identical to `.orchestration/dotfiles-T128-playbook-rules-followup-a01/task.md` (validation §1).
    14	- Round 1 was dispatched at 06:47:41Z. At 06:50Z I asked whether two more sentences belonged to the `procedure-migration` row: the task-level audit bullet and AGENTS.md:44, which both state the retired gate input outside SKILL lines 171 to 178. Amendment 1 (07:03:44Z) put them in the row. Nothing was pushed before it.
    15	
    16	## The owned rows
    17	
    18	The `## Owned by dotfiles-T128-playbook-rules-followup-a01` section of `.orchestration/acceptance/dotfiles-T128-playbook-rules-a04.md` on `origin/main` (sha256 `3bfd13d7…`) holds four rows (validation §2):
    19	
    20	| Row | Class | What changed (`7a282f3b`) |
    21	|---|---|---|
    22	| `local:65a3d71:1` | rule-gap | Orchestrator Playbook step 6: "so the orchestrator creates that record, `.orchestration/acceptance/<task>.md`, before the task's first dispatch (`scripts/orchestrator/dispatch.sh` refuses a record that does not exist or that names another task)". `dispatch.sh` refuses a record that is not an existing regular file or whose `task` is another task (its header, validation §3). The pinned fixture `orchestrator-step-6.md` changes with it. |
    23	| `audit:65a3d71:2` | rule-gap | The same finding as `local:65a3d71:1`, as the audit of `65a3d71b` raised it, so it is fixed by the same sentence. |
    24	| `audit:71eb920:1` | procedure-migration | Every sentence in the allowed files that still stated the retired gate input (amendment 1); the gate on `main` reads the record's JSON `audit_findings` and only reports `AUDIT_DISPOSITIONS` as retired (validation §3). The changed sentences are listed below the table. |
    25	| `audit:65a3d71:1` | disposition-range | No rule sentence: the finding was a sweep-table disposition (`fixed:a03c1daa` outside base..head), corrected in a04's sweep at 14:41Z. Nothing changes for it. |
    26	
    27	The `procedure-migration` row changed these sentences:
    28	
    29	- **The task-level audit bullet (invariants section):**
    30	  - An `incorrect` verdict is dispositioned in `audit_findings`, the only form the gate reads: one `{n, reason, evidence}` entry per finding, `n` a string, `reason` at least 20 characters. The entries are written with `acceptance-front-matter.py --audit-dispositions`, and an entry never cites a fix.
    31	  - A `Verdict: correct` finding keeps its `audit-finding: <n> …` prose line.
    32	  - The pinned fixture `invariants.md` changes with it.
    33	- **Step 10.3:** it now points to that bullet.
    34	- **Step 10.4:** the gate command drops `[AUDIT_DISPOSITIONS=<acceptance record>]`, and the `AUDIT_EVIDENCE` bullet now asks for an `audit_findings` entry per finding.
    35	- **AGENTS.md:44:** the gate takes `PR_FEEDBACK_EVIDENCE`, `AUDIT_EVIDENCE` and `ACCEPTANCE_EVIDENCE`.
    36	
    37	Each changed sentence has a token test, and the superseded forms are asserted absent:
    38	
    39	- `test_dispatches_are_recorded_from_the_bus`;
    40	- `test_the_gate_reads_the_acceptance_record`;
    41	- `test_an_incorrect_audit_is_dispositioned_in_audit_findings` (new).
    42	
    43	The documentation module runs 48 tests OK (validation §4).
    44	
    45	## Caps and checks
    46	
    47	- **INV-2** (validation §7): 5 files outside `.orchestration/`, 6 added lines outside `tests/` and 50 added lines under `tests/`.
    48	- **Formatting:** prettier and `ruff format --check` are clean.
    49	- **`ruff check`:** reports the module's implicit-concatenation style (ISC004) on the new tuples as on its existing ones, 12 against 7 on `origin/main`. CI runs only the format check.
    50	
    51	## CI and the Bot
    52	
    53	In the RESULT. The Bot reviews once, at PR open.
    54	
    55	## Not done, or outside scope
    56	
    57	- Understand-Anything hook: did not fire. plan-mode-used: no.
    58	- cost: n/a (the runtime exposes no session figures to the seat).
     1	---
     2	task_id: dotfiles-T128-playbook-rules-followup-a01
     3	seat: claude-standard-dot-a002
     4	rule_commit: 7a282f3b
     5	---
     6	
     7	# Validation: dotfiles-T128-playbook-rules-followup-a01
     8	
     9	Every command ran from the worktree `.claude/worktrees/worker-f` inside the sandbox, with `MAIN` naming the main checkout and `UV_OFFLINE=1` set (uv cannot reach pypi from the sandbox). The output is verbatim; each block ends with the command's exit status. Captured at `7a282f3b`, before the PR was opened.
    10	
    11	Changed tests: `test_dispatches_are_recorded_from_the_bus` (step 6's sentence), `test_the_gate_reads_the_acceptance_record` (step 10.3 and 10.4) and `test_an_incorrect_audit_is_dispositioned_in_audit_findings` (new: the task-level audit bullet and AGENTS.md's gate sentence). Changed fixtures (`test_regime_rule_sections_are_pinned_whole`): `tests/fixtures/regime/orchestrator-step-6.md` and `tests/fixtures/regime/invariants.md`, each in the one changed sentence.
    12	
    13	## 1. Task file and task copy
    14	
    15	```console
    16	$ shasum -a 256 "$MAIN/.orchestration/tasks/dotfiles-T128-playbook-rules-followup-a01.md" .orchestration/dotfiles-T128-playbook-rules-followup-a01/task.md | sed "s#$MAIN/##"; cmp "$MAIN/.orchestration/tasks/dotfiles-T128-playbook-rules-followup-a01.md" .orchestration/dotfiles-T128-playbook-rules-followup-a01/task.md && echo byte-identical
    17	ec415eaf526937fd43907a59fccfc455de117850003ba3d48cd20b065fc5564b  .orchestration/tasks/dotfiles-T128-playbook-rules-followup-a01.md
    18	ec415eaf526937fd43907a59fccfc455de117850003ba3d48cd20b065fc5564b  .orchestration/dotfiles-T128-playbook-rules-followup-a01/task.md
    19	byte-identical
    20	[exit 0]
    21	```
    22	
    23	## 2. Branch and the owned section (item 1's definition)
    24	
    25	```console
    26	$ git log --oneline origin/main..HEAD; git rev-parse origin/main
    27	7a282f3b docs(agmsg-orchestration): the record before the first dispatch; audit_findings replaces AUDIT_DISPOSITIONS (T703 a04 owner rows)
    28	c15ba668da20dc2956220077cb0f20054ab352c7
    29	[exit 0]
    30	```
    31	```console
    32	$ git show origin/main:.orchestration/acceptance/dotfiles-T128-playbook-rules-a04.md | shasum -a 256; git show origin/main:.orchestration/acceptance/dotfiles-T128-playbook-rules-a04.md | awk '/^## Owned by dotfiles-T128-playbook-rules-followup-a01/ {p = 1} p && /^(local|audit):[0-9a-f]{7}:[0-9]+\t/'
    33	3bfd13d7c9e2b381e3de118b6f717d9025ce2b67f5b2bc08b844d0486613e5ec  -
    34	local:65a3d71:1	rule-gap
    35	audit:71eb920:1	procedure-migration (the SKILL step 10.4 gate command still names AUDIT_DISPOSITIONS; from the audit of PR #329's head)
    36	audit:65a3d71:1	disposition-range
    37	audit:65a3d71:2	rule-gap
    38	[exit 0]
    39	```
    40	
    41	## 3. The retired gate input before and after
    42	
    43	```console
    44	$ for f in home/dot_agents/skills/agmsg-orchestration/SKILL.md AGENTS.md tests/fixtures/regime/invariants.md; do echo "== origin/main:$f"; git show "origin/main:$f" | /usr/bin/grep -n "AUDIT_DISPOSITIONS\|audit-finding" | cut -c1-140; echo "== HEAD:$f"; /usr/bin/grep -n "AUDIT_DISPOSITIONS\|audit-finding" "$f" | cut -c1-140; done
    45	== origin/main:home/dot_agents/skills/agmsg-orchestration/SKILL.md
    46	90:  - The orchestrator dispositions every `[P0-P3]` finding in the acceptance record, whatever the verdict: exactly one `audit-finding: <n>
    47	171:    3. Write the acceptance record, summarising the dispositions, with an `audit-finding:` line for every audit finding whatever the ver
    48	172:    4. Run the gate: `AUDIT_EVIDENCE=<audit> [AUDIT_DISPOSITIONS=<acceptance record>] AGENT_REVIEWED=1 REVIEW_EVIDENCE=<receipt> ACCEPTA
    49	178:       - `AUDIT_EVIDENCE` must be the task-level file `.orchestration/validation/<task>-audit-<sha7>.md` (the same `<task>` as the feedb
    50	== HEAD:home/dot_agents/skills/agmsg-orchestration/SKILL.md
    51	90:  - The orchestrator dispositions every `[P0-P3]` finding in the acceptance record, whatever the verdict, numbered 1..N in the audit's or
    52	171:    3. Write the acceptance record, summarising the dispositions, with every audit finding dispositioned as the task-level audit bullet 
    53	== origin/main:AGENTS.md
    54	44:- Before merging a pull request, follow the integration order in the agmsg-orchestration SKILL's Orchestrator Playbook step 10 and `home/
    55	== HEAD:AGENTS.md
    56	== origin/main:tests/fixtures/regime/invariants.md
    57	27:  - The orchestrator dispositions every `[P0-P3]` finding in the acceptance record, whatever the verdict: exactly one `audit-finding: <n>
    58	== HEAD:tests/fixtures/regime/invariants.md
    59	27:  - The orchestrator dispositions every `[P0-P3]` finding in the acceptance record, whatever the verdict, numbered 1..N in the audit's or
    60	[exit 0]
    61	```
    62	```console
    63	$ git grep -n "RETIRED_AUDIT_DISPOSITIONS_ENV =\|^FAILURE_REASON_MIN_CHARS\|def audit_findings_errors" -- scripts/require-crit-review.py; /usr/bin/grep -n "audit-dispositions" scripts/orchestrator/acceptance-front-matter.py | head -3; /usr/bin/grep -n "is not an existing regular file\|whose .task. is not" scripts/orchestrator/dispatch.sh
    64	scripts/require-crit-review.py:26:RETIRED_AUDIT_DISPOSITIONS_ENV = "AUDIT_DISPOSITIONS"
    65	scripts/require-crit-review.py:33:FAILURE_REASON_MIN_CHARS = 20
    66	scripts/require-crit-review.py:705:def audit_findings_errors(record: dict | None, findings: int) -> list[str]:
    67	1:"""acceptance-front-matter.py <task> <sweep-json> <pr-worktree> [--ledger <tsv>] [--audit-dispositions <tsv>]
    68	9:`--audit-dispositions` (`n<TAB>reason<TAB>evidence`), required when the audit summary orch-audit.sh writes beside
    69	51:    parser.add_argument("--audit-dispositions")
    70	34:#   (thread 4255272797). A record that is not an existing regular file writable in a
    71	35:#   writable directory, or whose `task` is not the line's `task_id`, is refused
    72	[exit 0]
    73	```
    74	
    75	## 4. The Validation command
    76	
    77	```console
    78	$ uv run --no-project python -m unittest tests/unit/test_agmsg_orchestration_docs.py -v
    79	test_docs_no_longer_name_codex_review_commit (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationForbiddenPhrasesTest.test_docs_no_longer_name_codex_review_commit) ... ok
    80	test_rule_and_skill_name_worker_seats_not_codex_workers (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationForbiddenPhrasesTest.test_rule_and_skill_name_worker_seats_not_codex_workers) ... ok
    81	test_rule_drops_the_worker_network_escalation (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationForbiddenPhrasesTest.test_rule_drops_the_worker_network_escalation) ... ok
    82	test_skill_drops_the_pane_status_gate_and_raw_pane_wakes (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationForbiddenPhrasesTest.test_skill_drops_the_pane_status_gate_and_raw_pane_wakes) ... ok
    83	test_rule_pointers_name_real_skill_sections (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationRuleTest.test_rule_pointers_name_real_skill_sections) ... ok
    84	test_rule_states_the_invariants (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationRuleTest.test_rule_states_the_invariants) ... ok
    85	test_word_budgets (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationRuleTest.test_word_budgets) ... ok
    86	test_audit_command_lives_only_in_the_task_level_audit_bullet (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationSingleSourceTest.test_audit_command_lives_only_in_the_task_level_audit_bullet) ... ok
    87	test_codex_agents_points_at_the_worklog_section (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationSingleSourceTest.test_codex_agents_points_at_the_worklog_section) ... ok
    88	test_contextdb_cli_is_invoked_with_uv_run (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationSingleSourceTest.test_contextdb_cli_is_invoked_with_uv_run) ... ok
    89	test_skill_masks_evidence_with_a_runnable_command (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationSingleSourceTest.test_skill_masks_evidence_with_a_runnable_command) ... ok
    90	test_claude_worker_merge_denials_and_prefix_limits_are_documented (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationSkillTest.test_claude_worker_merge_denials_and_prefix_limits_are_documented) ... ok
    91	test_codex_worker_profile_defaults_to_standard (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationSkillTest.test_codex_worker_profile_defaults_to_standard) ... ok
    92	test_skill_carries_the_audit_gate_and_bot_wait_mechanics (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationSkillTest.test_skill_carries_the_audit_gate_and_bot_wait_mechanics) ... ok
    93	test_skill_carries_the_parallel_execution_and_routing_mechanics (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationSkillTest.test_skill_carries_the_parallel_execution_and_routing_mechanics) ... ok
    94	test_skill_carries_the_registration_and_delivery_mechanics (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationSkillTest.test_skill_carries_the_registration_and_delivery_mechanics) ... ok
    95	test_skill_carries_the_session_lessons (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationSkillTest.test_skill_carries_the_session_lessons) ... ok
    96	test_a_design_lands_on_main_before_its_task (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_a_design_lands_on_main_before_its_task) ... ok
    97	test_a_revise_acceptance_names_the_previous_head_and_a_check (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_a_revise_acceptance_names_the_previous_head_and_a_check) ... ok
    98	test_a_trust_boundary_task_carries_a_threat_table (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_a_trust_boundary_task_carries_a_threat_table) ... ok
    99	test_an_incorrect_audit_is_dispositioned_in_audit_findings (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_an_incorrect_audit_is_dispositioned_in_audit_findings) ... ok
   100	test_bot_fix_rounds_are_capped_and_the_pr_is_ready_first (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_bot_fix_rounds_are_capped_and_the_pr_is_ready_first) ... ok
   101	test_boundary_merge_sentence_names_the_in_job_decision (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_boundary_merge_sentence_names_the_in_job_decision) ... ok
   102	test_closed_selector_existence_is_checked_at_acceptance (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_closed_selector_existence_is_checked_at_acceptance) ... ok
   103	test_code_review_rules_cover_orchestration_records_and_threat_tables (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_code_review_rules_cover_orchestration_records_and_threat_tables) ... ok
   104	test_counters_bullet_names_owners_not_sources (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_counters_bullet_names_owners_not_sources) ... ok
   105	test_counters_run_before_every_acceptance_action (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_counters_run_before_every_acceptance_action) ... ok
   106	test_design_review_runs_in_paired_rounds_with_a_cap (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_design_review_runs_in_paired_rounds_with_a_cap) ... ok
   107	test_dispatches_are_recorded_from_the_bus (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_dispatches_are_recorded_from_the_bus) ... ok
   108	test_open_review_body_findings_have_an_identifier (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_open_review_body_findings_have_an_identifier) ... ok
   109	test_open_third_round_threads_have_an_integration_outcome (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_open_third_round_threads_have_an_integration_outcome) ... ok
   110	test_orchestration_records_rule_binds_the_bot_review_only (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_orchestration_records_rule_binds_the_bot_review_only) ... ok
   111	test_pattern_rules_pin_their_safeguards (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_pattern_rules_pin_their_safeguards) ... ok
   112	test_question_pongs_are_in_the_contract (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_question_pongs_are_in_the_contract) ... ok
   113	test_regime_rule_sections_are_pinned_whole (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_regime_rule_sections_are_pinned_whole) ... ok
   114	test_rule_changes_travel_as_task_amendments (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_rule_changes_travel_as_task_amendments) ... ok
   115	test_shape_is_checked_by_hand_until_the_schema_lands (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_shape_is_checked_by_hand_until_the_schema_lands) ... ok
   116	test_shape_rules_and_the_decision_sentence_are_pinned (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_shape_rules_and_the_decision_sentence_are_pinned) ... ok
   117	test_task_file_review_is_one_round_with_a_fixed_stop_condition (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_task_file_review_is_one_round_with_a_fixed_stop_condition) ... ok
   118	test_the_bot_wait_filters_the_codex_bot (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_the_bot_wait_filters_the_codex_bot) ... ok
   119	test_the_ci_watch_is_joined_before_the_result (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_the_ci_watch_is_joined_before_the_result) ... ok
   120	test_the_ci_watcher_survives_the_no_checks_race (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_the_ci_watcher_survives_the_no_checks_race) ... ok
   121	test_the_gate_reads_the_acceptance_record (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_the_gate_reads_the_acceptance_record) ... ok
   122	test_threat_table_rows_have_a_fixed_unit (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_threat_table_rows_have_a_fixed_unit) ... ok
   123	test_threat_table_rule_carries_no_grammar (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_threat_table_rule_carries_no_grammar) ... ok
   124	test_three_repeats_start_with_a_pasted_correction_search (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_three_repeats_start_with_a_pasted_correction_search) ... ok
   125	test_workers_commit_inside_the_sandbox (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_workers_commit_inside_the_sandbox) ... ok
   126	test_workers_open_the_pr_as_a_draft (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_workers_open_the_pr_as_a_draft) ... ok
   127	
   128	----------------------------------------------------------------------
   129	Ran 48 tests in 0.012s
   130	
   131	OK
   132	[exit 0]
   133	```
   134	
   135	## 5. Formatting
   136	
   137	```console
   138	$ prettier --check home/dot_agents/skills/agmsg-orchestration/SKILL.md AGENTS.md tests/fixtures/regime/*.md; ruff format --config ruff.toml --check tests/unit/test_agmsg_orchestration_docs.py
   139	Checking formatting...
   140	All matched files use Prettier code style!
   141	1 file already formatted
   142	[exit 0]
   143	```
   144	
   145	## 6. The changed tests and fixtures
   146	
   147	```console
   148	$ git diff origin/main...HEAD --stat -- tests; git diff origin/main...HEAD -- tests/unit/test_agmsg_orchestration_docs.py | /usr/bin/grep "^@@\|^+    def \|^ *def test" | cut -c1-140
   149	 tests/fixtures/regime/invariants.md          |  2 +-
   150	 tests/fixtures/regime/orchestrator-step-6.md |  2 +-
   151	 tests/unit/test_agmsg_orchestration_docs.py  | 52 +++++++++++++++++++++++++---
   152	 3 files changed, 50 insertions(+), 6 deletions(-)
   153	@@ -522,7 +522,12 @@ class AgmsgRegimePatternTest(unittest.TestCase):
   154	@@ -629,11 +634,50 @@ class AgmsgRegimePatternTest(unittest.TestCase):
   155	     def test_the_gate_reads_the_acceptance_record(self) -> None:
   156	+    def test_an_incorrect_audit_is_dispositioned_in_audit_findings(self) -> None:
   157	[exit 0]
   158	```
   159	
   160	## 7. Caps (INV-2)
   161	
   162	```console
   163	$ git diff --numstat origin/main...HEAD -- . ':!.orchestration' | awk '{print; f++; if ($3 ~ /^tests\//) t += $1; else x += $1} END {printf "files outside .orchestration: %d (cap 15); added outside tests: %d (cap 500); added under tests: %d (cap 1000)\n", f, x, t}'
   164	1	1	AGENTS.md
   165	5	5	home/dot_agents/skills/agmsg-orchestration/SKILL.md
   166	1	1	tests/fixtures/regime/invariants.md
   167	1	1	tests/fixtures/regime/orchestrator-step-6.md
   168	48	4	tests/unit/test_agmsg_orchestration_docs.py
   169	files outside .orchestration: 5 (cap 15); added outside tests: 6 (cap 500); added under tests: 50 (cap 1000)
   170	[exit 0]
   171	```

**Adjusting output budget**
exec
/bin/zsh -lc "git show origin/main:scripts/require-crit-review.py | nl -ba | sed -n '520,850p'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 10ms:
   520	            cwd=root,
   521	            env=env,
   522	            capture_output=True,
   523	            text=True,
   524	            check=False,
   525	        )
   526	        repo_data = json.loads(repository.stdout) if repository.returncode == 0 else None
   527	        repo = repo_data.get("nameWithOwner") if isinstance(repo_data, dict) else None
   528	        if not isinstance(repo, str) or not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo):
   529	            return [failure]
   530	        if evidence.get("repo") != repo:
   531	            return [
   532	                f"{PR_FEEDBACK_ENV} does not match the local GitHub repository {repo}; rerun scripts/pr-feedback.py"
   533	            ]
   534	        result = subprocess.run(
   535	            ["gh", "pr", "view", str(pr), "--repo", repo, "--json", "headRefOid,baseRefName,baseRefOid"],
   536	            cwd=root,
   537	            env=env,
   538	            capture_output=True,
   539	            text=True,
   540	            check=False,
   541	        )
   542	        metadata = json.loads(result.stdout) if result.returncode == 0 else None
   543	    except (OSError, json.JSONDecodeError):
   544	        return [failure]
   545	    if not isinstance(metadata, dict):
   546	        return [failure]
   547	    github_base = metadata.get("baseRefOid")
   548	    github_ref = metadata.get("baseRefName")
   549	    if (
   550	        not isinstance(github_base, str)
   551	        or not re.fullmatch(r"[0-9a-f]{40}", github_base)
   552	        or not isinstance(github_ref, str)
   553	        or not github_ref.strip()
   554	        or run_git(["cat-file", "-e", f"{github_base}^{{commit}}"], root).returncode != 0
   555	    ):
   556	        return [failure]
   557	    if metadata.get("headRefOid") != head:
   558	        return [f"PR #{pr} head on GitHub is {metadata.get('headRefOid')}, not the local HEAD {head}; push first"]
   559	    if evidence.get("base_sha") != github_base or evidence.get("base_ref") != github_ref:
   560	        return [
   561	            f"{PR_FEEDBACK_ENV} does not match the GitHub base {github_ref} ({github_base}); rerun scripts/pr-feedback.py"
   562	        ]
   563	
   564	    resolved = run_git(["rev-parse", "--verify", "--end-of-options", f"{base}^{{commit}}"], root)
   565	    base_sha = resolved.stdout.strip()
   566	    if resolved.returncode == 0:
   567	        if base_sha == github_base:
   568	            return []
   569	        if run_git(["merge-base", "--is-ancestor", base_sha, github_base], root).returncode == 0:
   570	            first_parents = run_git(["rev-list", "--first-parent", head], root)
   571	            if first_parents.returncode == 0 and base_sha not in first_parents.stdout.splitlines():
   572	                return []
   573	        # An advanced base must stay on the base side of the fork, not absorb PR commits.
   574	        if run_git(["merge-base", "--is-ancestor", github_base, base_sha], root).returncode == 0:
   575	            actual = run_git(["merge-base", base_sha, head], root)
   576	            expected = run_git(["merge-base", github_base, head], root)
   577	            if actual.returncode == expected.returncode == 0 and actual.stdout == expected.stdout:
   578	                return []
   579	    return [
   580	        f"--base {base!r} is not bound to PR #{pr} base {github_ref} ({github_base}); use the PR base, not its branch or HEAD"
   581	    ]
   582	
   583	
   584	def collected_feedback_errors(root: Path, evidence: dict, head: str, base: str) -> list[str]:
   585	    """Re-collect the PR's feedback and require every current item in the evidence.
   586	
   587	    A hand-written or stale document cannot pass: the guard runs the GitHub
   588	    base SHA's scripts/pr-feedback.py (the PR under review cannot swap it) for the
   589	    evidence's PR, requires the PR head on GitHub to be this HEAD, and requires
   590	    each collected item (as a multiset) to be present. A bot review is not
   591	    required; when one exists it is collected and must be dispositioned like any
   592	    other item.
   593	    """
   594	    pr = evidence.get("pr")
   595	    if not isinstance(pr, int) or isinstance(pr, bool) or pr <= 0:
   596	        return [f"{PR_FEEDBACK_ENV} must name its pull request number in `pr`"]
   597	    errors = pr_base_errors(root, evidence, pr, head, base)
   598	    if errors:
   599	        return errors
   600	    with tempfile.TemporaryDirectory() as temporary:
   601	        collected_path = Path(temporary) / "collected.json"
   602	        # An advanced local base may contain untrusted code despite a safe merge-base.
   603	        # Execute only the GitHub-authenticated base's collector, including bootstrap.
   604	        collector = root / "scripts/pr-feedback.py"
   605	        base_collector = run_git(["show", f"{evidence['base_sha']}:scripts/pr-feedback.py"], root)
   606	        if base_collector.returncode == 0:
   607	            collector = Path(temporary) / "pr-feedback.py"
   608	            collector.write_text(base_collector.stdout)
   609	        result = subprocess.run(
   610	            [sys.executable, str(collector), str(pr), "--repo", evidence["repo"], "--json", str(collected_path)],
   611	            cwd=root,
   612	            check=False,
   613	            text=True,
   614	            stdout=subprocess.PIPE,
   615	            stderr=subprocess.PIPE,
   616	        )
   617	        if result.returncode != 0 or not collected_path.is_file():
   618	            detail = (result.stderr or result.stdout).strip().splitlines()[-1:] or ["no output"]
   619	            return [f"could not re-collect PR #{pr} feedback with scripts/pr-feedback.py: {detail[0]}"]
   620	        collected = json.loads(collected_path.read_text())
   621	    if collected.get("head_sha") != head:
   622	        return [f"PR #{pr} head on GitHub is {collected.get('head_sha')}, not the local HEAD {head}; push first"]
   623	    if collected.get("repo") != evidence["repo"]:
   624	        return [f"collected feedback does not match the local GitHub repository {evidence['repo']}"]
   625	    missing = missing_feedback(collected.get("items", []), evidence.get("items", []))
   626	    if missing:
   627	        sample = next(iter(missing))
   628	        return [
   629	            f"{PR_FEEDBACK_ENV} lacks {sum(missing.values())} current feedback item(s) for PR #{pr}, e.g. {sample[0]}:{sample[2]} {sample[1]}; rerun scripts/pr-feedback.py and disposition them"
   630	        ]
   631	    return []
   632	
   633	
   634	def orchestration_path_error(root: Path, path: Path, env: str, directory: str) -> str | None:
   635	    """Apply feedback_path_error's rule (repo-local, also after resolving links) to another .orchestration dir."""
   636	    try:
   637	        relatives = (feedback_relative_path(root, path), path.resolve().relative_to(root.resolve()))
   638	    except ValueError:
   639	        return f"{env} must point to a repo-local file under .orchestration/{directory}/"
   640	    if any(relative.parts[:2] != (".orchestration", directory) for relative in relatives):
   641	        return f"{env} must live under .orchestration/{directory}/"
   642	    return None
   643	
   644	
   645	def audit_name_error(name: str, head: str, task: str) -> str | None:
   646	    match = AUDIT_NAME.fullmatch(name)
   647	    if not match:
   648	        return f"{AUDIT_ENV} must be named <id>-audit-<sha7>.md, not {name}"
   649	    if match.group("task") != task:
   650	        return f"{AUDIT_ENV} audits task {match.group('task')!r}, not {task!r} named by {PR_FEEDBACK_ENV} (<task>-pr-feedback.json)"
   651	    if not head.startswith(match.group("sha")):
   652	        return f"{AUDIT_ENV} audits {match.group('sha')}, not HEAD {head}; audit the final head"
   653	    return None
   654	
   655	
   656	def audit_errors(root: Path, head: str, task: str, record: dict | None) -> list[str]:
   657	    """Require the task-level audit of HEAD for task: `correct`, or `incorrect` with every finding in audit_findings."""
   658	    evidence = os.environ.get(AUDIT_ENV, "").strip()
   659	    if not evidence:
   660	        return [
   661	            f"{AUDIT_ENV} must point to the task-level audit of HEAD, .orchestration/validation/<id>-audit-<sha7>.md (herdr-agents --audit)"
   662	        ]
   663	    path = Path(evidence)
   664	    if not path.is_absolute():
   665	        path = root / path
   666	    path_error = orchestration_path_error(root, path, AUDIT_ENV, "validation")
   667	    if path_error:
   668	        return [path_error]
   669	    for name in (path.name, path.resolve().name):
   670	        name_error = audit_name_error(name, head, task)
   671	        if name_error:
   672	            return [name_error]
   673	    if not path.is_file():
   674	        return [f"{AUDIT_ENV} file does not exist: {path}"]
   675	    # The verdict comes only from codex's final message (`codex exec -o`), never from the
   676	    # transcript, where repository text the auditor quoted could end in a verdict line.
   677	    source = path.with_name(f"{path.name}.last.md")
   678	    if not source.is_file() or not source.read_text().strip():
   679	        return [
   680	            f"{AUDIT_ENV} verdict is missing: {source.name} must exist with codex's final message; re-run the audit"
   681	        ]
   682	    source_error = orchestration_path_error(root, source, AUDIT_ENV, "validation")
   683	    if source_error:
   684	        return [f"{source_error} (its companion {source.name})"]
   685	    resolved = source.resolve().name
   686	    if resolved != source.name:
   687	        return [f"{AUDIT_ENV} companion {source.name} resolves to {resolved}; it must be this audit's own last message"]
   688	    name_error = audit_name_error(resolved.removesuffix(".last.md"), head, task)
   689	    if name_error:
   690	        return [f"{name_error} (its companion {source.name})"]
   691	    text = source.read_text()
   692	    lines = [line for line in text.splitlines() if line.strip()]
   693	    match = AUDIT_VERDICT.fullmatch(lines[-1]) if lines else None
   694	    verdict = match.group(1) if match else "missing"
   695	    if verdict == "correct":
   696	        return []
   697	    if verdict != "incorrect":
   698	        return [f"{AUDIT_ENV} verdict is {verdict} in {source}; a blocked or missing audit cannot be accepted"]
   699	    findings = len(AUDIT_FINDING.findall(text))
   700	    if not findings:
   701	        return [f"{AUDIT_ENV} verdict is incorrect but {source} lists no [P0-P3] finding to disposition"]
   702	    return audit_findings_errors(record, findings)
   703	
   704	
   705	def audit_findings_errors(record: dict | None, findings: int) -> list[str]:
   706	    """An incorrect audit needs one `audit_findings` entry per finding 1..N (each entry's shape is checked on load)."""
   707	    entries = (record or {}).get("audit_findings")
   708	    if not entries:
   709	        return [
   710	            f"{AUDIT_ENV} verdict is incorrect: the acceptance record's audit_findings must disposition its {findings} finding(s)"
   711	        ]
   712	    numbers = [int(entry["n"]) for entry in entries]
   713	    errors = [
   714	        f"audit_findings dispositions finding {n} more than once" for n in sorted(set(numbers)) if numbers.count(n) > 1
   715	    ]
   716	    errors += [
   717	        f"audit_findings names finding {n}, but the audit lists {findings}"
   718	        for n in sorted(set(numbers))
   719	        if n > findings
   720	    ]
   721	    missing = sorted(set(range(1, findings + 1)) - set(numbers))
   722	    if missing:
   723	        errors.append(
   724	            f"audit_findings leaves audit finding(s) {', '.join(map(str, missing))} of {findings} without a disposition; add one {{n, reason, evidence}} entry per finding"
   725	        )
   726	    return errors
   727	
   728	
   729	def refuse_duplicate_keys(pairs: list[tuple[str, object]]) -> dict:
   730	    """json.loads keeps the last of two equal keys; the record's reader refuses them instead."""
   731	    seen: set[str] = set()
   732	    for key, _ in pairs:
   733	        if key in seen:
   734	            raise ValueError(f"acceptance record: duplicate key {key}")
   735	        seen.add(key)
   736	    return dict(pairs)
   737	
   738	
   739	def refuse_non_finite(name: str) -> object:
   740	    """json.loads accepts NaN and Infinity by default; a record field never needs one."""
   741	    raise ValueError("acceptance record: non-finite number")
   742	
   743	
   744	def read_acceptance_record(path: Path) -> tuple[dict | None, str | None]:
   745	    """Load the record's JSON block between its first two --- lines with the standard library only."""
   746	    # Both delimiters are whole lines that are exactly `---`: `---junk` closes nothing.
   747	    lines = path.read_text().split("\n")
   748	    if lines[0] != "---" or "---" not in lines[1:]:
   749	        return None, "acceptance record must start with a JSON block between two lines that are exactly ---"
   750	    block = "\n".join(lines[1 : lines.index("---", 1)])
   751	    try:
   752	        data = json.loads(block, object_pairs_hook=refuse_duplicate_keys, parse_constant=refuse_non_finite)
   753	    except json.JSONDecodeError as error:
   754	        return None, f"acceptance record: the block between the first two --- lines is not JSON: {error}"
   755	    except ValueError as error:
   756	        return None, str(error)
   757	    if not isinstance(data, dict):
   758	        return None, "acceptance record: the block must be one JSON object"
   759	    return data, None
   760	
   761	
   762	def is_int(value: object) -> bool:
   763	    return isinstance(value, int) and not isinstance(value, bool)
   764	
   765	
   766	def is_text(value: object) -> bool:
   767	    return isinstance(value, str) and bool(value.strip())
   768	
   769	
   770	def record_field_errors(record: dict, task: str, head: str, pr: object) -> list[str]:
   771	    """Check the identity triple (task, head, pr) first, then format, ledger, searches and audit_findings."""
   772	    errors: list[str] = []
   773	    if record.get("task") != task:
   774	        errors.append(f"task must be {task!r}, the task id the file name carries")
   775	    if record.get("head") != head:
   776	        errors.append(f"acceptance record head {record.get('head')} is not HEAD {head}")
   777	    if not is_int(record.get("pr")) or record["pr"] <= 0 or (pr is not None and record["pr"] != pr):
   778	        errors.append(
   779	            f"acceptance record pr {record.get('pr')} is not the swept pr {pr}"
   780	            if pr is not None
   781	            else "acceptance record pr must be the pull request number"
   782	        )
   783	    if errors:
   784	        return errors
   785	    errors += [f"acceptance record: unknown key {key}" for key in sorted(set(record) - RECORD_KEYS)]
   786	    if "dispatch" in record and (
   787	        not isinstance(record["dispatch"], list) or not all(isinstance(line, str) for line in record["dispatch"])
   788	    ):
   789	        errors.append("dispatch must be a list of strings")
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
   811	    if not isinstance(searches, list):
   812	        errors.append("searches must be a list of {class, records} entries")
   813	    else:
   814	        seen: set[str] = set()
   815	        for index, entry in enumerate(searches):
   816	            if (
   817	                not isinstance(entry, dict)
   818	                or set(entry) != {"class", "records"}
   819	                or not isinstance(entry["class"], str)
   820	                or not CLASS_SLUG.fullmatch(entry["class"])
   821	                or not isinstance(entry["records"], list)
   822	                or not all(isinstance(name, str) for name in entry["records"])
   823	            ):
   824	                errors.append(
   825	                    f"searches entry {index} must be {{class: <slug>, records: [<file basename>, …]}}: {entry!r}"
   826	                )
   827	            elif entry["class"] in seen:
   828	                errors.append(f"searches names class {entry['class']} more than once")
   829	            else:
   830	                seen.add(entry["class"])
   831	    findings = record.get("audit_findings")
   832	    if findings is not None and not isinstance(findings, list):
   833	        errors.append("audit_findings must be a list of {n, reason, evidence} entries")
   834	    for index, entry in enumerate(findings if isinstance(findings, list) else []):
   835	        if isinstance(entry, dict) and "fixed" in entry:
   836	            errors.append(f"audit_findings entry {index} cites a fix; a fix moves HEAD, so audit the new head instead")
   837	        elif (
   838	            not isinstance(entry, dict)
   839	            or set(entry) != AUDIT_FINDING_KEYS
   840	            or not (isinstance(entry["n"], str) and FINDING_NUMBER.fullmatch(entry["n"]))
   841	            or not is_text(entry["reason"])
   842	            or not is_text(entry["evidence"])
   843	        ):
   844	            errors.append(
   845	                f"audit_findings entry {index} must be {{n: <finding number>, reason: <text>, evidence: <command>}}, each a non-empty string"
   846	            )
   847	        elif len(entry["reason"].strip()) < FAILURE_REASON_MIN_CHARS:
   848	            errors.append(
   849	                f"audit_findings entry {index} needs a reason of at least {FAILURE_REASON_MIN_CHARS} characters"
   850	            )

**Reviewing test approach for evidence command**
exec
/bin/zsh -lc "git show 3a8f809b36944b0cb778da53104f9b3c54f67355:tests/unit/test_agmsg_orchestration_docs.py | nl -ba | sed -n '1,240p'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 27ms:
     1	import re
     2	import unittest
     3	from pathlib import Path
     4	
     5	ROOT = Path(__file__).resolve().parents[2]
     6	RULES = ROOT / "home/dot_config/claude/rules"
     7	RULE = RULES / "agmsg-orchestration.md"
     8	SKILL = ROOT / "home/dot_agents/skills/agmsg-orchestration/SKILL.md"
     9	# The always-loaded Claude rules; gpu.md, latex.md and python.md load only for matching paths.
    10	ALWAYS_LOADED_RULES = (
    11	    "agmsg-orchestration.md",
    12	    "ask-user-question.md",
    13	    "compactiondb.md",
    14	    "crit-review.md",
    15	    "model-selection.md",
    16	    "ponytail.md",
    17	    "pr-integration.md",
    18	    "understand-anything.md",
    19	)
    20	PAIR_AUDIT = "herdr-agents --audit <head-sha> --task <id>"
    21	HEADLESS_AUDIT = "codex <MODEL_PROFILE_AUDIT_CODEX_ARGS> exec --sandbox read-only -C <repo> -o <out>.last.md"
    22	
    23	
    24	def words(path: Path) -> int:
    25	    return len(path.read_text().split())
    26	
    27	
    28	class AgmsgOrchestrationRuleTest(unittest.TestCase):
    29	    """The rule carries the regime's invariants within its word budget; the SKILL carries the procedure."""
    30	
    31	    def test_rule_states_the_invariants(self) -> None:
    32	        text = RULE.read_text()
    33	        for invariant in (
    34	            "invoke the `agmsg-orchestration` skill",
    35	            "Only the operator opts out",
    36	            "is never an implicit opt-out",
    37	            "Every repository mutation goes to a seated worker of the manifest's `worker_kind`",
    38	            "or after the operator's explicit opt-out for the current task",
    39	            "`make require-crit-review` stay with the orchestrator and are never delegated",
    40	            "one task-level audit of its final head",
    41	            "AGMSG-PONG v1 status=blocked",
    42	            "except the few commands Worker Playbook step 4 sends through the permission gate",
    43	            "Agent-to-agent permission approval is forbidden",
    44	            "never pushes a repository change to `main` directly",
    45	            "gh pr merge --squash",
    46	            "--match-head-commit <audited head sha>",
    47	            "AGMSG_RESOLVE_PROJECT=0 join.sh <team> <name> <type> <worktree>",
    48	            "pairwise-disjoint",
    49	            "disjoint code tasks run concurrently while overlapping code files run serially",
    50	            "gh pr update-branch",
    51	            "never edits the source of its own execution boundary",
    52	            "make check-regime-boundary",
    53	            # Pinned registration and wake tokens; their procedure is in the SKILL.
    54	            "agmsg-dispatch",
    55	            "poke.sh",
    56	            "send.sh",
    57	            "--body-file",
    58	            "inbox.sh",
    59	            "exit 13",
    60	        ):
    61	            with self.subTest(invariant=invariant):
    62	                self.assertIn(invariant, text)
    63	
    64	    def test_rule_pointers_name_real_skill_sections(self) -> None:
    65	        rule = RULE.read_text()
    66	        skill = SKILL.read_text()
    67	        # Quoted capitalised names are SKILL headings, except the task-level audit bullet checked below.
    68	        for heading in set(re.findall(r'"([A-Z][^"]+)"', rule)) - {"Task-level audit"}:
    69	            with self.subTest(heading=heading):
    70	                self.assertIn(f"\n## {heading}\n", skill)
    71	        playbooks = {
    72	            "Orchestrator": skill.split("## Orchestrator Playbook", 1)[1].split("\n## ", 1)[0],
    73	            "Worker": skill.split("## Worker Playbook", 1)[1].split("\n## ", 1)[0],
    74	        }
    75	        for playbook, step in re.findall(r"(Orchestrator|Worker) Playbook step (\d+)", rule):
    76	            with self.subTest(playbook=playbook, step=step):
    77	                self.assertRegex(playbooks[playbook], rf"(?m)^{step}\. ")
    78	        self.assertIn('the "Task-level audit" bullet', rule)
    79	        self.assertIn("\n- Task-level audit:", skill)
    80	
    81	    def test_word_budgets(self) -> None:
    82	        self.assertLessEqual(words(RULE), 450)
    83	        self.assertLessEqual(sum(words(RULES / name) for name in ALWAYS_LOADED_RULES), 1800)
    84	
    85	
    86	class AgmsgOrchestrationSkillTest(unittest.TestCase):
    87	    """The SKILL holds the mechanics the rule points at."""
    88	
    89	    def test_claude_worker_merge_denials_and_prefix_limits_are_documented(self) -> None:
    90	        for path in (ROOT / "README.md", SKILL):
    91	            text = " ".join(path.read_text().split())
    92	            with self.subTest(path=path.name):
    93	                for token in (
    94	                    "Bash(gh pr merge:*)",
    95	                    "Bash(gh api -X PUT:*)",
    96	                    "Bash(gh api --method PUT:*)",
    97	                    "Bash(gh api graphql:*)",
    98	                    "herdr-agents",
    99	                    ".claude/settings.local.json",
   100	                    "deny rules",
   101	                    "nested subcommands",
   102	                    "permission mode",
   103	                    "flag after the path",
   104	                    "integration gate",
   105	                    "https://code.claude.com/docs/en/permissions",
   106	                ):
   107	                    self.assertIn(token, text)
   108	                self.assertNotIn("Claude worker seats have no such denial yet", text)
   109	                self.assertNotIn("Claude seats get their deny rules in a separate task", text)
   110	
   111	    def test_skill_carries_the_registration_and_delivery_mechanics(self) -> None:
   112	        text = SKILL.read_text()
   113	        for token in (
   114	            "AGMSG_RESOLVE_PROJECT=0 join.sh <team> <name> <type> <worktree>",
   115	            "poke.sh",
   116	            "send.sh",
   117	            "--body-file",
   118	            "agmsg-dispatch",
   119	            "13 =",
   120	            "inbox.sh",
   121	            "gh pr merge --squash",
   122	            "--match-head-commit <audited head sha>",
   123	            "never pushes a repository change to `main` directly",
   124	            "is never an implicit opt-out",
   125	            "actas.<team>__<name>.session",
   126	            "`<common>/objects`",
   127	            "messages.db `read_at`/PONG query",
   128	            "Never run full mode from inside an existing managed workspace",
   129	            "`--restart-worker` is retired and exits 2",
   130	            "herdr-agents --add-worker [<worktree>]",
   131	            "remove every worker with `herdr-agents --remove-worker <worktree>`",
   132	            "machine-state hygiene that touches no repository",
   133	        ):
   134	            with self.subTest(token=token):
   135	                self.assertIn(token, text)
   136	
   137	    def test_skill_carries_the_parallel_execution_and_routing_mechanics(self) -> None:
   138	        text = SKILL.read_text()
   139	        for token in (
   140	            "pairwise-disjoint",
   141	            "--add-worker",
   142	            "re-tasked immediately",
   143	            "acceptance follows RESULT arrival order",
   144	            "gh pr update-branch",
   145	            "Self-Modification",
   146	            "home/dot_claude/modify_private_settings.json",
   147	            "`claude.sandbox`",
   148	            "home/dot_agents/permgate-policy.yaml",
   149	            "PermissionRequest hook of both seats, goes to the operator",
   150	            "AGMSG-PONG v1 status=blocked",
   151	            "--ask-for-approval never",
   152	        ):
   153	            with self.subTest(token=token):
   154	                self.assertIn(token, text)
   155	
   156	    def test_codex_worker_profile_defaults_to_standard(self) -> None:
   157	        text = SKILL.read_text()
   158	        parallel = text.split("## Parallel workers", 1)[1].split("\n## ", 1)[0]
   159	        for token in (
   160	            "For Codex, seat ordinary tasks with `--profile standard`",
   161	            "use `--profile security` only for trust-boundary tasks",
   162	            "permgate, redaction or secret handling, sandbox or permission policy",
   163	            "`codex-security-dot-aNNN`",
   164	        ):
   165	            with self.subTest(token=token):
   166	                self.assertIn(token, parallel)
   167	        routing = text.split("## Orchestrator Playbook", 1)[1].split("\n4. ", 1)[0]
   168	        self.assertIn("records it and the chosen worker profile in the task file", routing)
   169	
   170	    def test_skill_carries_the_audit_gate_and_bot_wait_mechanics(self) -> None:
   171	        text = SKILL.read_text()
   172	        for token in (
   173	            "--audit",
   174	            "--task",
   175	            "-audit-<sha7>.md",
   176	            "AUDIT_EVIDENCE",
   177	            "in_reply_to_id",
   178	            "until a review of the final head appears or 15 minutes pass",
   179	            "needs green CI but no new Bot wait",
   180	            "CI on the new head, then the sweep, then the audit",
   181	            "audit-finding: <n>",
   182	            "Such a review-body finding is listed alongside the top-level inline comments and fixed or dispositioned the same way.",
   183	            "A `review` sweep item whose body carries a `P0`–`P3` badge is a finding with its own `fixed:<commit>` or `not-applicable:<reason>` disposition, never a container for its inline threads.",
   184	            "Deferral",
   185	            "is not a disposition",
   186	        ):
   187	            with self.subTest(token=token):
   188	                self.assertIn(token, text)
   189	
   190	    def test_skill_carries_the_session_lessons(self) -> None:
   191	        text = SKILL.read_text()
   192	        for token in (
   193	            "WebFetch tool, not Bash `curl`",
   194	            "Fetch and fast-forward inside the sandbox",
   195	            "So a Claude seat runs three commands outside the sandbox through the permission gate:",
   196	            "`gh`, `git push`, and an authenticated `git fetch`",
   197	            "-worker-crit.json",
   198	            "writing the task's artifacts at their expected main-checkout paths and masking them with the repository masker, through the permission gate because the main checkout is not writable from a worktree sandbox",
   199	            "(a Claude seat writes them through the permission gate, step 4)",
   200	            "never run `git worktree prune` from a sandboxed seat",
   201	            "`git worktree remove <path>` only",
   202	            "the orchestrator moves them into the main checkout",
   203	            "uv run --no-project .claude/hooks/contextdb_cli.py memory candidates --limit 20",
   204	            "uv run --no-project .claude/hooks/contextdb_cli.py memory promote <id> --scope project",
   205	        ):
   206	            with self.subTest(token=token):
   207	                self.assertIn(token, text)
   208	
   209	
   210	class AgmsgRegimePatternTest(unittest.TestCase):
   211	    """Plan 006 Phase A: the review and fix pattern, each rule in the section that owns it."""
   212	
   213	    @staticmethod
   214	    def section(text: str, start: str, end: str = "\n## ") -> str:
   215	        return text.split(start, 1)[1].split(end, 1)[0]
   216	
   217	    def invariants(self) -> str:
   218	        return self.section(SKILL.read_text(), "## Review and integration invariants")
   219	
   220	    # Plan 006 S1 on the docs tests (class unpinned): token tests pin only the clauses their author chose, so
   221	    # each regime rule section is also pinned whole; a rule changes only together with its fixture (INV-12).
   222	    PINNED_SECTIONS = (
   223	        # name, file, outer slice or None, (start, end): the start marker is part of the pinned text.
   224	        ("invariants", SKILL, None, ("## Review and integration invariants", "\n## ")),
   225	        ("worker-step-15", SKILL, None, ("\n15. After the final push", "\n## ")),
   226	        ("orchestrator-step-6", SKILL, ("## Orchestrator Playbook", "\n## "), ("\n6. ", "\n7. ")),
   227	        ("orchestrator-step-7", SKILL, ("## Orchestrator Playbook", "\n## "), ("\n7. ", "\n8. ")),
   228	        ("message-contract", SKILL, None, ("## Message Contract v1", "\n## ")),
   229	        (
   230	            "code-review-orchestration",
   231	            ROOT / "AGENTS.md",
   232	            None,
   233	            ("### Orchestration records and trust-boundary code", "\n## "),
   234	        ),
   235	    )
   236	
   237	    @staticmethod
   238	    def normalized(text: str) -> str:
   239	        return "\n".join(line.rstrip() for line in text.split("\n")).strip()
   240	

exec
/bin/zsh -lc "git show 3a8f809b36944b0cb778da53104f9b3c54f67355:tests/unit/test_agmsg_orchestration_docs.py | nl -ba | sed -n '241,525p'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 53ms:
   241	    def test_regime_rule_sections_are_pinned_whole(self) -> None:
   242	        for name, path, outer, (start, end) in self.PINNED_SECTIONS:
   243	            with self.subTest(section=name):
   244	                text = path.read_text()
   245	                if outer:
   246	                    text = self.section(text, *outer)
   247	                fixture = ROOT / "tests/fixtures/regime" / f"{name}.md"
   248	                self.assertEqual(
   249	                    self.normalized(start + self.section(text, start, end)),
   250	                    self.normalized(fixture.read_text()),
   251	                    f"regime rule section {name} changed: declare the change by updating "
   252	                    f"tests/fixtures/regime/{name}.md in the same commit and listing it in the RESULT",
   253	                )
   254	
   255	    def test_design_review_runs_in_paired_rounds_with_a_cap(self) -> None:
   256	        text = self.invariants()
   257	        for token in (
   258	            "get the same design hash at the same time",
   259	            "The orchestrator revises once per pair of results",
   260	            "opens no round while one is still open",
   261	            "frozen at the hash the pair last accepted",
   262	            # Thread 4243537279: a revision after the third pair would freeze an unreviewed hash.
   263	            "any later change to a hashed key is a new pair (INV-7)",
   264	            # Thread 4243732324: a third pair that returns revise or reject has no accepted hash to freeze.
   265	            "on its revise or reject nothing is frozen",
   266	            "becomes a residual list that is worker input",
   267	            "never implementation detail",
   268	        ):
   269	            with self.subTest(token=token):
   270	                self.assertIn(token, text)
   271	
   272	    def test_task_file_review_is_one_round_with_a_fixed_stop_condition(self) -> None:
   273	        text = self.invariants()
   274	        for token in (
   275	            "A task-file review is one round with a fixed stop condition",
   276	            "no contradiction with the design",
   277	            "the premises hold",
   278	            "`allowed_files` covers every touch point that grep finds",
   279	            # Plan 006 B0: design v20 removed contract PRs, so the check names the implementing_tasks entry;
   280	            # thread 4247933561: a task without an `invariants` key (a docs or review task) needs no entry;
   281	            # thread 4257278283: matching ids is not enough, so each sentence is compared with the design's.
   282	            "one invariant check (for a task that carries an `invariants` key: the task id maps to its "
   283	            "`implementing_tasks` entry, the invariant ids match, and each invariant's sentence equals the design's "
   284	            "byte-for-byte, the design read from main (INV-2), checked by hand in the review until a checker lands; "
   285	            "a task without the key needs no entry)",
   286	        ):
   287	            with self.subTest(token=token):
   288	                self.assertIn(token, text)
   289	        self.assertNotIn("-contract-a01", text)
   290	
   291	    def test_a_design_lands_on_main_before_its_task(self) -> None:
   292	        # Thread 4243537281: a boundary PR carrying the design is INV-2's dispatch prerequisite.
   293	        text = self.invariants()
   294	        for token in ("carries no task draft under review", "before its implementing TASK is dispatched (INV-2)"):
   295	            with self.subTest(token=token):
   296	                self.assertIn(token, text)
   297	        self.assertNotIn("is never a prerequisite of a dispatch", text)
   298	
   299	    def test_boundary_merge_sentence_names_the_in_job_decision(self) -> None:
   300	        # PR 320 removes the changes job: a skipped required job reports Success, so each job decides itself.
   301	        text = self.invariants()
   302	        self.assertIn(
   303	            "each required job decides inside itself and reports success on an `.orchestration`-only diff; "
   304	            "a skipped required job would report Success (fail-open), so no required job carries a job-level "
   305	            "`if` or a `needs`.",
   306	            text,
   307	        )
   308	        self.assertNotIn("the ruleset accepts the resulting `skipped` required checks", text)
   309	
   310	    def test_a_trust_boundary_task_carries_a_threat_table(self) -> None:
   311	        text = self.invariants()
   312	        for token in (
   313	            "carries a `threat_table` in its front matter",
   314	            "`closed: tests/<file>::<name>`",
   315	            "`residual: <sentence>`",
   316	            "`out-of-scope: <task id>`",
   317	            "Shape is `schemas/task.json`'s",
   318	            "Substance is the reviewers'",
   319	            "The table is the task's completion condition",
   320	            "a missing row is added once, counted as an amendment",
   321	        ):
   322	            with self.subTest(token=token):
   323	                self.assertIn(token, text)
   324	
   325	    def test_threat_table_rule_carries_no_grammar(self) -> None:
   326	        # The reset of PR 318: shape lives in schemas/task.json, never as a pattern in prose.
   327	        text = self.invariants()
   328	        self.assertNotIn("^(closed|residual|out-of-scope)", text)
   329	        self.assertNotIn("`none`", text)
   330	
   331	    # Thread 4240348412 is closed by a05's counters bullet: the script reads the whole history (scripts/regime-counters.sh:85), no by-hand read remains.
   332	    def test_open_third_round_threads_have_an_integration_outcome(self) -> None:
   333	        # Thread 4240348414: an open: item needs a path through steps 10.1 and 10.5.
   334	        playbook = self.section(SKILL.read_text(), "## Orchestrator Playbook")
   335	        for token in ("is a sweep item like any other", "the PR is not merged, never with the thread open"):
   336	            with self.subTest(token=token):
   337	                self.assertIn(token, playbook)
   338	
   339	    def test_counters_run_before_every_acceptance_action(self) -> None:
   340	        text = self.invariants()
   341	        self.assertIn(
   342	            "Before every acceptance action (revise, accept, merge) the orchestrator runs "
   343	            "`scripts/regime-counters.sh <task id>`",
   344	            text,
   345	        )
   346	        # Thread 4240566268: the counts are evidence for the S1/S2 decision.
   347	        self.assertIn("and pastes its output into the acceptance record", text)
   348	
   349	    def test_bot_fix_rounds_are_capped_and_the_pr_is_ready_first(self) -> None:
   350	        step = self.section(SKILL.read_text(), "\n15. After the final push", "\n## ")
   351	        for token in (
   352	            # Thread 4240646079: after a fix push the PR is already ready, and `gh pr ready` fails there.
   353	            "Mark the PR ready for review with `gh pr ready <n>` before the first wait, while it is still a draft",
   354	            "within 10 minutes, post `@codex review`",
   355	            "at most twice. The third Bot round is not fixed",
   356	            "`AGMSG-RESULT … bot_rounds=3`",
   357	            "in the background and the Bot wait below at the same time",
   358	            "listed as `open:<thread id>`",
   359	            "an escalated label that the next bullet's",
   360	            "never from the end of CI",
   361	        ):
   362	            with self.subTest(token=token):
   363	                self.assertIn(token, step)
   364	
   365	    def test_open_review_body_findings_have_an_identifier(self) -> None:
   366	        # Thread 4240290382: a review-body finding has no thread id.
   367	        step = self.section(SKILL.read_text(), "\n15. After the final push", "\n## ")
   368	        self.assertIn("(`open:review-<review id>` for a review-body finding)", step)
   369	
   370	    def test_the_ci_watch_is_joined_before_the_result(self) -> None:
   371	        # Thread 4240290391: the background CI watcher's exit status gates the RESULT.
   372	        step = self.section(SKILL.read_text(), "\n15. After the final push", "\n## ")
   373	        self.assertIn(
   374	            "Wait for that watcher's exit status before the RESULT: a non-zero exit means no RESULT until CI passes.",
   375	            step,
   376	        )
   377	
   378	    def test_question_pongs_are_in_the_contract(self) -> None:
   379	        # Thread 4243732330: INV-6 counts AGMSG-PONG status=question, so the contract must allow it.
   380	        contract = self.section(SKILL.read_text(), "## Message Contract v1")
   381	        for token in ("status=alive|blocked|question", "`question`: the worker holds and asks; INV-6 counts it."):
   382	            with self.subTest(token=token):
   383	                self.assertIn(token, contract)
   384	
   385	    def test_a_revise_acceptance_names_the_previous_head_and_a_check(self) -> None:
   386	        contract = self.section(SKILL.read_text(), "## Message Contract v1")
   387	        self.assertIn("carries `previous_head=<the RESULT head being revised>`", contract)
   388	        self.assertIn("one failing-test selector per finding (`check=tests/<file>::<name>`)", contract)
   389	        self.assertIn("`.orchestration/<task id>/revise.yaml`", contract)
   390	
   391	    def test_code_review_rules_cover_orchestration_records_and_threat_tables(self) -> None:
   392	        rules = self.section((ROOT / "AGENTS.md").read_text(), "## Code Review Rules")
   393	        subsection = self.section(rules, "### Orchestration records and trust-boundary code", "\n### ")
   394	        for token in (
   395	            "review them for secrets and home-directory paths only",
   396	            "Judge from the diff, whatever the task's metadata says, whether a change touches a trust boundary",
   397	            "report a missing table or a missing row",
   398	            "a `residual` row whose control does not mitigate the risk",
   399	            "an `out-of-scope` row whose owner does not own it",
   400	            "Do not re-raise a `residual` row whose control mitigates the risk",
   401	            "Shape (the test selector, the sentence, the owning task id) is the schema's to check, not the review's",
   402	        ):
   403	            with self.subTest(token=token):
   404	                self.assertIn(token, subsection)
   405	
   406	    def test_orchestration_records_rule_binds_the_bot_review_only(self) -> None:
   407	        # Audit of 27ea99b2: the secrets-only scope is plan 006 A4's for the Bot, never the auditor's.
   408	        rules = self.section((ROOT / "AGENTS.md").read_text(), "## Code Review Rules")
   409	        bullet = self.section(rules, "### Orchestration records and trust-boundary code", "\n### ").split("\n- ")[1]
   410	        for token in (
   411	            "in the pull-request review by the Codex Bot, review them for secrets and home-directory paths only",
   412	            "The task-level audit keeps the full scope of the Audit section.",
   413	            # Thread 4243732326: the next bullet reviews the threat table inside task.md.
   414	            "except a trust-boundary task's `threat_table`",
   415	        ):
   416	            with self.subTest(token=token):
   417	                self.assertIn(token, bullet)
   418	
   419	    def test_shape_is_checked_by_hand_until_the_schema_lands(self) -> None:
   420	        # Audit of 27ea99b2: neither schemas/task.json nor its validator exists yet.
   421	        sentence = (
   422	            "Until `schemas/task.json` lands in wave V1, the task-file review checks the three shape rules by hand."
   423	        )
   424	        rules = self.section((ROOT / "AGENTS.md").read_text(), "## Code Review Rules")
   425	        for name, text in (
   426	            ("SKILL invariants", self.invariants()),
   427	            ("AGENTS.md", self.section(rules, "### Orchestration records and trust-boundary code", "\n### ")),
   428	        ):
   429	            with self.subTest(section=name):
   430	                self.assertIn(sentence, text)
   431	
   432	    def test_pattern_rules_pin_their_safeguards(self) -> None:
   433	        # Audit of 27ea99b2: each safeguard could be removed with every other test still passing.
   434	        rules = self.section((ROOT / "AGENTS.md").read_text(), "## Code Review Rules")
   435	        subsection = self.section(rules, "### Orchestration records and trust-boundary code", "\n### ")
   436	        self.assertIn("report a `closed` row whose test does not close it", subsection)
   437	        text = self.invariants()
   438	        for token in (
   439	            "(the tree and its tests, task.md, workflow files,",
   440	            "a fresh Claude context on the `review` profile and a Codex read-only run",
   441	            # Item 7 of a04 reworded the clause; the safeguard is the same sentence.
   442	            "any merged boundary that carries the design meets that precondition",
   443	        ):
   444	            with self.subTest(token=token):
   445	                self.assertIn(token, text)
   446	
   447	    def test_closed_selector_existence_is_checked_at_acceptance(self) -> None:
   448	        # Audit of b7ae2d54 and thread 4240646082: a closed row's test does not exist before implementation.
   449	        text = self.invariants()
   450	        for token in (
   451	            "a `closed` selector names a test present in the PR tree at acceptance and in the schema's validation of the PR",
   452	            "For a `closed` row it checks the selector's form only, since the test does not exist before implementation.",
   453	        ):
   454	            with self.subTest(token=token):
   455	                self.assertIn(token, text)
   456	
   457	    def test_the_bot_wait_filters_the_codex_bot(self) -> None:
   458	        # Audit of b7ae2d54 and thread 4243369347: a CodeRabbit review matched `.user.type=="Bot"` and ended the wait.
   459	        step = self.section(SKILL.read_text(), "\n15. After the final push", "\n## ")
   460	        for token in (
   461	            '.[]|select(.user.login=="chatgpt-codex-connector[bot]" and .commit_id=="<head-sha>")',
   462	            '.[]|select(.in_reply_to_id == null and .user.login=="chatgpt-codex-connector[bot]" and .original_commit_id=="<head-sha>")',
   463	            "A human comment, a CodeRabbit review or an earlier head's review never ends the wait.",
   464	        ):
   465	            with self.subTest(token=token):
   466	                self.assertIn(token, step)
   467	        self.assertNotIn('.user.type=="Bot"', step)
   468	
   469	    def test_shape_rules_and_the_decision_sentence_are_pinned(self) -> None:
   470	        # Audit of b7ae2d54: the S1/S2 decision and the three shape rules could each be removed unnoticed.
   471	        text = self.invariants()
   472	        for token in (
   473	            "S2 is decided from INV-6's counts",
   474	            "a `closed` selector names a test present in the PR tree",
   475	            "an `out-of-scope` owner is a task id in the design's `implementing_tasks`",
   476	            "a `residual` payload is a sentence of at least 20 characters",
   477	        ):
   478	            with self.subTest(token=token):
   479	                self.assertIn(token, text)
   480	
   481	    def test_counters_bullet_names_owners_not_sources(self) -> None:
   482	        # Plan 006 S1 on the counters bullet: it states its obligations by reference and names no source.
   483	        bullet = self.section(self.invariants(), "\n- Before every acceptance action", "\n- ")
   484	        for token in (
   485	            "for each component it prints as `unknown` the record pastes the command and output that read the source INV-6 names for that component",
   486	            "gives a class to every finding the PR-feedback sweep lists, whatever its disposition, and to every task-level audit finding",
   487	        ):
   488	            with self.subTest(token=token):
   489	                self.assertIn(token, bullet)
   490	        for phrase in ("review bodies", "by hand", "gh api --paginate", "until it is on `main`"):
   491	            with self.subTest(phrase=phrase):
   492	                self.assertNotIn(phrase, bullet)
   493	
   494	    def test_the_ci_watcher_survives_the_no_checks_race(self) -> None:
   495	        # Thread 4243516880: `gh pr checks --watch` exits 1 with "no checks reported" before the first check appears.
   496	        step = self.section(SKILL.read_text(), "\n15. After the final push", "\n## ")
   497	        self.assertIn(
   498	            "Right after a push GitHub can report no checks yet, and the watcher then exits 1 with `no checks reported`: start it once a check is listed, and restart it on that message instead of reading it as a CI failure.",
   499	            step,
   500	        )
   501	
   502	    def test_workers_open_the_pr_as_a_draft(self) -> None:
   503	        # Thread 4240566266: step 15's `gh pr ready` starts the Bot timer only on a draft PR.
   504	        step = self.section(SKILL.read_text(), "\n2. Switch to the `repo`", "\n3. ")
   505	        self.assertIn("`gh pr create --draft --head <branch>`", step)
   506	
   507	    def test_workers_commit_inside_the_sandbox(self) -> None:
   508	        # Audit of 27ea99b2: only the push is a step 4 exemption, so the commit stays inside.
   509	        step = self.section(SKILL.read_text(), "\n2. Switch to the `repo`", "\n3. ")
   510	        for token in (
   511	            "Commit inside the sandbox, with `git -c commit.gpgsign=false` when the signing key is unreadable there",
   512	            "only the push leaves the sandbox",
   513	            # Thread 4240598179: a Codex seat never leaves its sandbox, push included.
   514	            "a Codex seat pushes from inside it (step 4)",
   515	        ):
   516	            with self.subTest(token=token):
   517	                self.assertIn(token, step)
   518	
   519	    def test_dispatches_are_recorded_from_the_bus(self) -> None:
   520	        # Plan 007 T703 item 1 (C-12): a seat's status comes from a bus line, never from memory; plan 010 option D:
   521	        # the obligation stays here, and the commands move to plan 007 T718's scripts.
   522	        step = self.section(self.section(SKILL.read_text(), "## Orchestrator Playbook"), "\n6. ", "\n7. ")
   523	        for token in (
   524	            "Every dispatch (TASK, ACCEPTANCE, PING) is recorded in the current acceptance record under a "
   525	            "`dispatch:` key as the bus line with its read marker, "

**Reviewing orchestration and acceptance records**
**Analyzing missing dispatch in acceptance data**
codex
The documented JSON format and dispatch refusal both match code already on `origin/main`. The GitHub connector also confirms successful final-head Actions runs. I’m checking two remaining points: whether the tests cover every changed sentence, and whether the acceptance record contains the dispatch evidence it cites.
mcp: codex_apps/github.fetch_workflow_run_jobs started
mcp: codex_apps/github.fetch_workflow_run_jobs started
mcp: codex_apps/github.fetch_workflow_run_jobs started
mcp: codex_apps/github.list_pull_request_reviews started
mcp: codex_apps/github.list_pull_request_review_threads started
mcp: codex_apps/github.fetch_issue_comments started
mcp: codex_apps/github.list_pull_request_reviews (completed)
mcp: codex_apps/github.fetch_workflow_run_jobs (completed)
mcp: codex_apps/github.fetch_workflow_run_jobs (completed)
mcp: codex_apps/github.fetch_workflow_run_jobs (completed)
mcp: codex_apps/github.fetch_issue_comments (completed)
mcp: codex_apps/github.list_pull_request_review_threads (completed)
**Ensuring careful tool output**
exec
/bin/zsh -lc "git show 3a8f809b36944b0cb778da53104f9b3c54f67355:tests/unit/test_agmsg_orchestration_docs.py | nl -ba | sed -n '525,800p' && git show origin/main:scripts/orchestrator/acceptance-front-matter.py | nl -ba | sed -n '85,135p' && git show origin/main:scripts/require-crit-review.py | rg -n 'RETIRED_AUDIT_DISPOSITIONS|numbered|AUDIT_FINDING ='" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 50ms:
   525	            "`dispatch:` key as the bus line with its read marker, "
   526	            # Row local:65a3d71:1 (the a04 record's owned section): dispatch.sh refuses a missing record, so the rule
   527	            # says who creates it and when.
   528	            "so the orchestrator creates that record, `.orchestration/acceptance/<task>.md`, before the task's first "
   529	            "dispatch (`scripts/orchestrator/dispatch.sh` refuses a record that does not exist or that names another "
   530	            "task); a seat is reported as working only from such a "
   531	            # The local review of 7771082f: the merged bus-read.sh refuses a read at its limit; nothing reads all.
   532	            "line, and after a context compaction the open TASK list is re-derived from a bus read that is refused "
   533	            "when it reaches its limit (`bus-read.sh` exits when the history reaches `BUS_READ_LIMIT`; the "
   534	            "orchestrator raises the limit and reads again), never from a default-limited one and never from a read "
   535	            "whose truncation went unnoticed.",
   536	            # Threads 4248319936 and 4249303426: the clock runs from the seat's latest event for the task;
   537	            # thread 4257278271: INV-10's idle figure is 20 minutes, its 30 minutes the first-push deadline.
   538	            "A seated worker idle for 20 minutes since its latest bus event for the task while a dispatchable task "
   539	            "exists (INV-10's idle figure; its 30 minutes is the first-push deadline) gets a bus read, then a PING; "
   540	            "a longer silent wait is never the answer.",
   541	            # Thread 4249303413: history.sh shows the latest 20 rows unless given a limit.
   542	            "`scripts/orchestrator/dispatch.sh` writes the line and `scripts/orchestrator/bus-read.sh` performs the "
   543	            "read and prints the minutes since each open task's latest event (both on main since a03c1daa, plan 007 "
   544	            "T718); the orchestrator applies the 20-minute figure to the minutes the script prints (the script's own "
   545	            "silence flag still uses 30 minutes, a recorded residual of the tools lineage).",
   546	        ):
   547	            with self.subTest(token=token[:40]):
   548	                self.assertIn(token, step)
   549	        for stale in (
   550	            "expected duration",
   551	            "the bus line `history.sh <team>` prints",
   552	            "no bus event from its seat since",
   553	            "complete bus read",
   554	            "silent for thirty minutes",
   555	        ):
   556	            with self.subTest(stale=stale):
   557	                self.assertNotIn(stale, step)
   558	
   559	    def test_rule_changes_travel_as_task_amendments(self) -> None:
   560	        # Plan 007 Phase 0: a rule sentence changed through a PONG answer bypasses the hash and C1 to C6;
   561	        # plan 007 T704: the checker has landed, so the sentence names it instead of its landing condition.
   562	        self.assertIn(
   563	            "A change to a rule sentence requested of a worker travels as a task amendment (hashed, checked by "
   564	            "`scripts/orchestrator/task-consistency-check.py` (C1 to C10 and C7b) before dispatch and at acceptance, "
   565	            "confirmed by the review seat), never as a PONG answer.",
   566	            self.invariants(),
   567	        )
   568	        self.assertNotIn("C1 to C6 once plan 007 T704 lands it and by hand until then", self.invariants())
   569	
   570	    def test_three_repeats_start_with_a_pasted_correction_search(self) -> None:
   571	        # Plan 007 S6: the third repeat of a class is answered by a recorded correction, never by another fix round;
   572	        # plan 010 option D: the obligation stays here, and the commands move to plan 007 T718's three-repeat.sh.
   573	        bullet = self.section(self.invariants(), "\n- When a finding class reaches three on one artifact", "\n- ")
   574	        for token in (
   575	            # Threads 4247933574 and 4249303398: the records search, and a correction applied mechanism by mechanism.
   576	            " (the record's ledger) or `scripts/regime-counters.sh` prints an S1 candidate, the next acceptance "
   577	            "action is the records search for that class, pasted into the record as the line "
   578	            "`search: <class> -> <the matching mistake records or none>`, and the matching correction is applied "
   579	            "when its mechanism is landed, or landed first when it is pending, mechanism by mechanism, before any "
   580	            "dispatch; a class is a slug of `[a-z0-9-]` assigned at disposition time, never text taken from a review "
   581	            "title.",
   582	            # Thread 4249303433: review-derived text never reaches a shell.
   583	            "Once plan 007 T718 lands, `scripts/orchestrator/three-repeat.sh <class>` validates the slug, runs the "
   584	            "records search and the CompactionDB search without a shell and prints the line; until then the "
   585	            "orchestrator runs them by hand with a validated slug.",
   586	            # Thread 4248711363: the gate does not read the line yet, so the sentence names its landing condition.
   587	            "Once `dotfiles-T128-gate-evidence-a02` lands, the gate refuses the action without the line; until then "
   588	            "the orchestrator refuses it by rule.",
   589	            "Every `not-applicable` disposition carries `; evidence=<command>` with the output pasted in the record.",
   590	        ):
   591	            with self.subTest(token=token[:40]):
   592	                self.assertIn(token, bullet)
   593	        for stale in (
   594	            "`grep -rl <class slug> .orchestration/learning/corrections/`",
   595	            "`grep -l 'classes:",
   596	            "gate-evidence-a01",
   597	            "memory search <class slug>",
   598	        ):
   599	            with self.subTest(stale=stale):
   600	                self.assertNotIn(stale, bullet)
   601	
   602	    def test_threat_table_rows_have_a_fixed_unit(self) -> None:
   603	        # Plan 007 T703 item 4: without a unit, a missing row is a judgment call for each reviewer.
   604	        bullet = self.section(self.invariants(), "\n- A task that touches a trust boundary", "\n- ")
   605	        self.assertIn(
   606	            "metadata separators). The row unit is one row per `allowed_files` entry, one row per listed control "
   607	            "that is not a path (task metadata, workflow and interpreter or environment inputs, in-process effects, "
   608	            "new or renamed scripts, metadata separators), carried by the declared test module's row where that is "
   609	            "where the control acts, and one row per orchestrator effect from the fixed list (forced removal, merge, "
   610	            # Thread 4257278276: an executed wildcard entry gets a row per changed file; a data wildcard keeps one.
   611	            # Plan 007 T704: C4 and C7b have landed, so the clause names the script instead of its landing condition.
   612	            "update-branch); under a wildcard `allowed_files` entry whose files are executed or applied (scripts, "
   613	            "workflows, hooks, settings, the rules seats follow), one row per concrete file the PR changes; a "
   614	            "wildcard over test fixtures or other data files keeps one row; C4 and C7b of "
   615	            "`scripts/orchestrator/task-consistency-check.py` verify the path half before dispatch, and the task-file "
   616	            "review checks the rest.",
   617	            bullet,
   618	        )
   619	        for stale in (
   620	            "C4 verifies the path half before dispatch",
   621	            "C4 of the task-consistency check (plan 007 T704) verifies the path half once it lands",
   622	        ):
   623	            with self.subTest(stale=stale):
   624	                self.assertNotIn(stale, bullet)
   625	        rules = self.section((ROOT / "AGENTS.md").read_text(), "## Code Review Rules")
   626	        subsection = self.section(rules, "### Orchestration records and trust-boundary code", "\n### ")
   627	        self.assertIn(
   628	            "report a missing table or a missing row; a row's unit is the SKILL threat-table bullet's (one per "
   629	            "`allowed_files` entry, one per non-path control, one per orchestrator effect), so review a missing "
   630	            "row at that unit; report a `closed` row",
   631	            subsection,
   632	        )
   633	
   634	    def test_the_gate_reads_the_acceptance_record(self) -> None:
   635	        # Plan 007 T703 item 6: the gate reads the record's ledger and `search:` line once gate-evidence-a02 lands.
   636	        step = self.section(self.section(SKILL.read_text(), "## Orchestrator Playbook"), "\n10. ", "\n11. ")
   637	        # Row audit:71eb920:1 (the a04 record's owned section): the gate retired AUDIT_DISPOSITIONS and reads an
   638	        # incorrect audit's dispositions from the record's audit_findings, so step 10 no longer names the variable.
   639	        for token in (
   640	            "`AUDIT_EVIDENCE=<audit> AGENT_REVIEWED=1 REVIEW_EVIDENCE=<receipt> ACCEPTANCE_EVIDENCE=<acceptance record> "
   641	            "BASE=origin/main PR_FEEDBACK_EVIDENCE=<json> make require-crit-review`",
   642	            "with every audit finding dispositioned as the task-level audit bullet says: for an `incorrect` verdict "
   643	            "the record's JSON `audit_findings`, which the gate reads through `ACCEPTANCE_EVIDENCE` (it never reads "
   644	            "`AUDIT_DISPOSITIONS`, which is retired).",
   645	            "must be `correct`, or `incorrect` with an `audit_findings` entry in the acceptance record for each of its "
   646	            "findings.",
   647	        ):
   648	            with self.subTest(token=token[:40]):
   649	                self.assertIn(token, step)
   650	        for stale in ("[AUDIT_DISPOSITIONS=", "through `AUDIT_DISPOSITIONS`", "`incorrect` with `AUDIT_DISPOSITIONS`"):
   651	            with self.subTest(stale=stale):
   652	                self.assertNotIn(stale, step)
   653	
   654	    def test_an_incorrect_audit_is_dispositioned_in_audit_findings(self) -> None:
   655	        # Row audit:71eb920:1, amendment 1: the task-level audit bullet and AGENTS.md's gate sentence named the retired
   656	        # gate input (the audit-finding: prose the gate read through AUDIT_DISPOSITIONS); the gate reads audit_findings.
   657	        bullet = self.section(
   658	            self.invariants(), "\n  - The orchestrator dispositions every `[P0-P3]` finding", "\n  - "
   659	        )
   660	        for token in (
   661	            "For an `incorrect` verdict the dispositions are the record's JSON `audit_findings`, the only form the gate "
   662	            "reads: one `{n, reason, evidence}` entry per finding, `n` the number as a string and `reason` at least 20 "
   663	            "characters, written with `scripts/orchestrator/acceptance-front-matter.py --audit-dispositions <tsv>`; an "
   664	            "entry never cites a fix, since a fix moves the head and needs its own audit.",
   665	            "A finding under `Verdict: correct` is dispositioned all the same, as an `audit-finding: <n> …` line in the "
   666	            "record's prose: `fixed:<sha>` with a fresh audit of that sha, otherwise `not-applicable:<reason of at "
   667	            "least 20 characters>`.",
   668	        ):
   669	            with self.subTest(token=token[:40]):
   670	                self.assertIn(token, bullet)
   671	        for stale in ("The gate enforces these lines only for an `incorrect` verdict", "or the gate skips it"):
   672	            with self.subTest(stale=stale):
   673	                self.assertNotIn(stale, bullet)
   674	        agents = (ROOT / "AGENTS.md").read_text()
   675	        self.assertIn(
   676	            "then the gate with `PR_FEEDBACK_EVIDENCE`, `AUDIT_EVIDENCE` and `ACCEPTANCE_EVIDENCE` (the record's "
   677	            "`audit_findings` disposition an `incorrect` verdict).",
   678	            agents,
   679	        )
   680	        self.assertNotIn("`AUDIT_DISPOSITIONS` for an `incorrect` verdict", agents)
   681	
   682	
   683	class AgmsgOrchestrationSingleSourceTest(unittest.TestCase):
   684	    """The audit command appears once, in the SKILL's task-level audit bullet; everything else points there."""
   685	
   686	    POINTERS = (
   687	        ROOT / "AGENTS.md",
   688	        ROOT / "README.md",
   689	        RULE,
   690	        RULES / "model-selection.md",
   691	        RULES / "pr-integration.md",
   692	        ROOT / "home/dot_config/codex/AGENTS.md",
   693	        ROOT / "home/dot_agents/skills/gh-first-workflow/SKILL.md",
   694	    )
   695	
   696	    def test_audit_command_lives_only_in_the_task_level_audit_bullet(self) -> None:
   697	        skill = SKILL.read_text()
   698	        bullet = skill.split("\n- Task-level audit:", 1)[1].split("\n- ", 1)[0]
   699	        for command in (PAIR_AUDIT, HEADLESS_AUDIT):
   700	            with self.subTest(command=command):
   701	                self.assertEqual(skill.count(command), 1)
   702	                self.assertIn(command, bullet)
   703	                for path in self.POINTERS:
   704	                    with self.subTest(path=path.name):
   705	                        self.assertNotIn(command, path.read_text())
   706	        for path in self.POINTERS:
   707	            with self.subTest(path=path.name):
   708	                self.assertNotIn("exec --sandbox read-only", path.read_text())
   709	
   710	    def test_codex_agents_points_at_the_worklog_section(self) -> None:
   711	        codex = (ROOT / "home/dot_config/codex/AGENTS.md").read_text()
   712	        self.assertIn("「Codex seat worklogs」", codex)
   713	        self.assertIn("\n## Codex seat worklogs\n", SKILL.read_text())
   714	
   715	    def test_skill_masks_evidence_with_a_runnable_command(self) -> None:
   716	        # The validator is not executable (mode 100644), so the SKILL names it only through uv run.
   717	        text = SKILL.read_text()
   718	        runnable = "`uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets"
   719	        self.assertGreaterEqual(text.count(runnable), 3)
   720	        self.assertEqual(text.count("scripts/validate-agent-assets.py --mask-secrets"), text.count(runnable))
   721	
   722	    def test_contextdb_cli_is_invoked_with_uv_run(self) -> None:
   723	        paths = [
   724	            ROOT / "CLAUDE.md",
   725	            ROOT / "AGENTS.md",
   726	            SKILL,
   727	            ROOT / "home/dot_config/codex/AGENTS.md",
   728	            *sorted(RULES.glob("*.md")),
   729	        ]
   730	        for path in paths:
   731	            text = path.read_text()
   732	            with self.subTest(path=path.name):
   733	                self.assertNotIn("python3 .claude/hooks/contextdb_cli.py", text)
   734	                # Without --no-project, uv would create or sync the target project's environment first.
   735	                self.assertNotIn("uv run .claude/hooks/contextdb_cli.py", text)
   736	        for path in (ROOT / "CLAUDE.md", SKILL, RULES / "compactiondb.md", ROOT / "home/dot_config/codex/AGENTS.md"):
   737	            with self.subTest(path=path.name):
   738	                self.assertIn("uv run --no-project .claude/hooks/contextdb_cli.py", path.read_text())
   739	
   740	
   741	class AgmsgOrchestrationForbiddenPhrasesTest(unittest.TestCase):
   742	    def test_docs_no_longer_name_codex_review_commit(self) -> None:
   743	        for path in (
   744	            ROOT / "AGENTS.md",
   745	            ROOT / "README.md",
   746	            RULE,
   747	            SKILL,
   748	            RULES / "model-selection.md",
   749	        ):
   750	            text = path.read_text()
   751	            lines = [line for line in text.splitlines() if "review --commit" in line]
   752	            with self.subTest(path=path.name):
   753	                self.assertNotIn("audit review --commit", text)
   754	                # README keeps one sentence explaining why `codex review --commit` is not used.
   755	                self.assertEqual(
   756	                    [line for line in lines if not line.startswith("`codex review --commit` is not used")], []
   757	                )
   758	
   759	    def test_rule_and_skill_name_worker_seats_not_codex_workers(self) -> None:
   760	        # The worker kind comes from the manifest; model-selection.md's security-profile sentence is exempt.
   761	        for path in (RULE, SKILL):
   762	            with self.subTest(path=path.name):
   763	                self.assertNotIn("Codex worker", path.read_text())
   764	
   765	    def test_rule_drops_the_worker_network_escalation(self) -> None:
   766	        self.assertNotIn("network access stays off", RULE.read_text())
   767	
   768	    def test_skill_drops_the_pane_status_gate_and_raw_pane_wakes(self) -> None:
   769	        text = SKILL.read_text()
   770	        for stale in (
   771	            "isn't already `working`",
   772	            "wake or prompt a worker with `herdr pane run",
   773	            "upstream's own default) and Claude Code",
   774	        ):
   775	            with self.subTest(stale=stale):
   776	                self.assertNotIn(stale, text)
   777	
   778	
   779	if __name__ == "__main__":
   780	    unittest.main()
    85	            present.add(row_id)
    86	
    87	    summary = root / f".orchestration/validation/{args.task}-audit-{head[:7]}.md.last.md"
    88	    audit = summary.read_text() if summary.is_file() else ""
    89	    # The gate's verdict rule: the summary's last non-blank line.
    90	    last = [line for line in audit.splitlines() if line.strip()][-1:]
    91	    verdict = (match := gate.AUDIT_VERDICT.fullmatch(last[0]) if last else None) and match.group(1)
    92	    incorrect = verdict == "incorrect"
    93	    if incorrect != (args.audit_dispositions is not None):
    94	        refuse(
    95	            f"--audit-dispositions is {'required' if incorrect else 'refused'}: {summary.name} {verdict or 'missing'}"
    96	        )
    97	    findings = [
    98	        {"n": n, "reason": reason, "evidence": evidence} for n, reason, evidence in rows(args.audit_dispositions, 3)
    99	    ]
   100	
   101	    classes = collections.Counter(
   102	        row["class"] for row in ledger if isinstance(row, dict) and isinstance(row.get("class"), str)
   103	    )
   104	    searches = []
   105	    for cls in sorted(c for c, count in classes.items() if count >= gate.S6_CLASS_LIMIT):
   106	        found = gate.mistake_records(root, cls)
   107	        if isinstance(found, str):
   108	            refuse(found)
   109	        searches.append({"class": cls, "records": sorted(found)})
   110	
   111	    block = {**record, "format": gate.RECORD_FORMAT, "task": args.task, "head": head, "pr": sweep.get("pr")}
   112	    block.update(ledger=ledger, searches=searches, audit_findings=findings)
   113	    errors = gate.record_field_errors(block, args.task, head, sweep.get("pr"))
   114	    if not errors and incorrect:
   115	        errors = gate.audit_findings_errors(block, len(gate.AUDIT_FINDING.findall(audit)))
   116	    if errors:
   117	        refuse("; ".join(errors))
   118	    path.parent.mkdir(parents=True, exist_ok=True)
   119	    path.write_text("---\n" + json.dumps(block, indent=2, sort_keys=True, ensure_ascii=False) + "\n---\n" + rest)
   120	    print("written", path.relative_to(root), "head", head[:7], "pr", block["pr"], "ledger", len(ledger))
   121	
   122	
   123	if __name__ == "__main__":
   124	    main()
26:RETIRED_AUDIT_DISPOSITIONS_ENV = "AUDIT_DISPOSITIONS"
50:AUDIT_FINDING = re.compile(r"^\s*(?:[-*+]\s+)?\[P[0-3]\]", re.M)
855:    """The ids a ledger must cover: the sweep's Codex findings and the audit's numbered findings (a set, no regex)."""
1033:    if os.environ.get(RETIRED_AUDIT_DISPOSITIONS_ENV, "").strip():
1035:            f"{RETIRED_AUDIT_DISPOSITIONS_ENV} is retired and not read: the acceptance record's audit_findings disposition an incorrect audit."

**Designing test strategy**
**Outlining detailed mutation tests**
**Handling heredoc and quoting in code execution**
exec
/bin/zsh -lc "python3 -B -c '
import hashlib, json, subprocess
from pathlib import Path
head='\\''3a8f809b36944b0cb778da53104f9b3c54f67355'\\''
base='\\''6a2473f362762cf74c750f2141e5a11853816745'\\''
task='\\''dotfiles-T128-playbook-rules-followup-a01'\\''
def blob(ref,path):
    return subprocess.check_output(['\\''git'\\'','\\''show'\\'',f'\\''{ref}:{path}'\\''])
for name,local in [('\\''task'\\'',f'\\''.orchestration/tasks/{task}.md'\\''),('\\''report'\\'',f'\\''.orchestration/reports/{task}.md'\\''),('\\''validation'\\'',f'\\''.orchestration/validation/{task}.md'\\''),('\\''sandbox'\\'',f'\\''.orchestration/sandboxes/{task}.md'\\'')]:
    data=blob(head,f'\\''.orchestration/{task}/{name}.md'\\'')
    print(name, '\\''sha256='\\''+hashlib.sha256(data).hexdigest(), '\\''local_copy_equal='\\''+str(data==Path(local).read_bytes()))
owner=blob('\\''origin/main'\\'','\\''.orchestration/acceptance/dotfiles-T128-playbook-rules-a04.md'\\'')
print('\\''owner_record_sha256='\\''+hashlib.sha256(owner).hexdigest())
print('\\''premise_1_count='\\''+str(blob('\\''origin/main'\\'','\\''.orchestration/tasks/dotfiles-T128-playbook-rules-a04.md'\\'').decode().count('\\''owned by '\\''+task)))
print('\\''main_to_head_numstat:'\\'')
print(subprocess.check_output(['\\''git'\\'','\\''diff'\\'','\\''--numstat'\\'',base,head],text=True))
print('\\''head_commit:'\\'')
print(subprocess.check_output(['\\''git'\\'','\\''show'\\'','\\''-s'\\'','\\''--format=%H%n%P%n%s'\\'',head],text=True))
print('\\''base_update_changed_owned_files:'\\'')
owned=['\\''AGENTS.md'\\'','\\''home/dot_agents/skills/agmsg-orchestration/SKILL.md'\\'','\\''tests/unit/test_agmsg_orchestration_docs.py'\\'','\\''tests/fixtures/regime'\\'']
print(subprocess.check_output(['\\''git'\\'','\\''diff'\\'','\\''--name-only'\\'','\\''bd9e8a69606b03a54973bd631baa25ed07b6d247'\\'',head,'\\''--'\\'',*owned],text=True))
print('\\''acceptance_record:'\\'')
acc=Path(f'\\''.orchestration/acceptance/{task}.md'\\'').read_text().split('\\''<"'!-- audit-input-boundary -->'"'\\'')[0]
print('\\''sha256='\\''+hashlib.sha256(acc.encode()).hexdigest())
front=json.loads(acc.split('\\''---'\\'',2)[1]); print('\\''front_keys='\\''+'\\'','\\''.join(front)); print('\\''dispatch_list='\\''+str(front.get('\\''dispatch'\\'')))
for n,line in enumerate(acc.splitlines(),1):
    if '\\''dispatch'\\'' in line.lower() or '\\''counter'\\'' in line.lower(): print(f'\\''{n}: {line}'\\'')
print('\\''graph_stale_changed_nonrecords='\\''+str(any(not p.startswith(('\\''.ua/'\\'','\\''.orchestration/'\\'')) for p in subprocess.check_output(['\\''git'\\'','\\''diff'\\'','\\''--name-only'\\'','\\''940a3a2b07adfd14140a0acff96784ef53a0a509..HEAD'\\''],text=True).splitlines())))
'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 655ms:
task sha256=ec415eaf526937fd43907a59fccfc455de117850003ba3d48cd20b065fc5564b local_copy_equal=True
report sha256=cc1ef10a3b5305d6811a1bb5bec00eefeb73c0cc55f4efcea0b4653deae0e77d local_copy_equal=True
validation sha256=31c0fb9414feffbe66904da51aa65df992a874e49312060e84d86706264209f3 local_copy_equal=True
sandbox sha256=a7262936991cffde9428b4e5f90bd6f855938b7e9fdcf2c13b7c06c4fadc1aed local_copy_equal=True
owner_record_sha256=3bfd13d7c9e2b381e3de118b6f717d9025ce2b67f5b2bc08b844d0486613e5ec
premise_1_count=1
main_to_head_numstat:
3	0	.orchestration/dotfiles-T128-playbook-rules-followup-a01/autoskill.md
6	0	.orchestration/dotfiles-T128-playbook-rules-followup-a01/learning.md
58	0	.orchestration/dotfiles-T128-playbook-rules-followup-a01/report.md
26	0	.orchestration/dotfiles-T128-playbook-rules-followup-a01/sandbox.md
87	0	.orchestration/dotfiles-T128-playbook-rules-followup-a01/task.md
171	0	.orchestration/dotfiles-T128-playbook-rules-followup-a01/validation.md
1	1	AGENTS.md
5	5	home/dot_agents/skills/agmsg-orchestration/SKILL.md
1	1	tests/fixtures/regime/invariants.md
1	1	tests/fixtures/regime/orchestrator-step-6.md
48	4	tests/unit/test_agmsg_orchestration_docs.py

head_commit:
3a8f809b36944b0cb778da53104f9b3c54f67355
bd9e8a69606b03a54973bd631baa25ed07b6d247 6a2473f362762cf74c750f2141e5a11853816745
Merge branch 'main' into regime/playbook-rules-followup

base_update_changed_owned_files:

acceptance_record:
sha256=6f179f62cb0b490278c1ba4a4c68bfc283b61b1aae962fb1b5275feaaeb72d13
front_keys=format,task,head,pr,ledger,searches,audit_findings
dispatch_list=None
16: - 2026-10-14 06:44Z pre-dispatch: `after: [dotfiles-T128-playbook-rules-a04]` met (PR #328 merged 2026-10-13 14:43:36Z as 26909ee4); file hash `e22e0cc45de6fe70ac9be9b3e7b710055b7cd8b8c50767d7a832a9335f392c51` equals the confirmed hash; checker: `dotfiles-T128-playbook-rules-followup-a01.md: OK`; the owned rows under `## Owned by dotfiles-T128-playbook-rules-followup-a01` in the a04 record on `origin/main`: 9 (local 9); premises 1 and 2 re-run equal (`premise-run.py`); no in-flight task holds its files (the hook task edits the project-map rule and SKILL, the PATH task `scripts/orchestrator/orch-gate.sh` and two test modules). Seat: `claude-standard-dot-a002` (worker-f, w5:p9), free since PR #352 merged 06:32:35Z.
17: - **Dispatched 06:47:41Z to `claude-standard-dot-a002` (worker-f, w5:p9), bus 1106, read** (the line in the dispatch list above).
19: - 06:52:29Z PING (bus 1110, read): the answer is a scope change of item 1's row, so it travels as amendment 1 (pair-confirmed, hashed), not as a PONG; hold the push; the four rows proceed in the working tree. Amendment 1 written 06:5xZ (item 1: the `procedure-migration` row covers every sentence in the allowed files that states the retired gate input, the fixture included, each with its token test; the `origin/main` lines pasted in its Change section; the pre-amendment copy at `validation/dotfiles-T128-playbook-rules-followup-a01-pre-amend1.md`, hash e22e0cc4); its paired review dispatched to the review seat and the Codex half. INV-6 for this task so far: questions=1, amendments=1 (pending confirm), revises=0.
20: - 06:57:38Z the Codex half: `confirm` on ec415eaf (receipt `validation/dotfiles-T128-playbook-rules-followup-a01-amend-review-a01-codex-r1.md`, 55 s); 07:00:33Z the seat: `confirm` on the same hash. **Amendment 1 pair-confirmed on `ec415eaf526937fd43907a59fccfc455de117850003ba3d48cd20b065fc5564b`**; ACCEPTANCE accepted to the seat; the amended TASK line (`amendment=1`, `previous_task_sha256` e22e0cc4 computed from `origin/main` at send) to a002 (the line in the dispatch list above). Owner rows on `origin/main` by the row grammar (`owner-rows.sh`, C-41): `local:65a3d71:1 rule-gap`, `audit:71eb920:1 procedure-migration`, `audit:65a3d71:1 disposition-range`, `audit:65a3d71:2 rule-gap`, `rows=4`; the 06:44Z figure of 9 counted the section's prose lines (M-20261014-07).
21: - 07:02:59Z ACCEPTANCE accepted for the amend review to the seat (bus 1120, read), sent ahead of the queued copy in the dispatch command (the amended TASK line to a002 waits for its read; a second identical ACCEPTANCE may follow from that command and is a duplicate, not a new decision).
22: - 07:20:57Z RESULT (bus 1123): `status=ready_for_review revises=0 questions=1 amendments=1`, PR #354 head `bd9e8a69606b03a54973bd631baa25ed07b6d247` on base c15ba668 (branch `regime/playbook-rules-followup`; 7a282f3b the owned rows, bd9e8a69 the task copy and evidence); `task_copy` ec415eaf equals amendment 1; rows: `local:65a3d71:1` and `audit:65a3d71:2` `fixed:7a282f3b` (step 6: the orchestrator creates the acceptance record before the task's first dispatch; dispatch.sh refuses a missing or another task's record), `audit:71eb920:1` `fixed:7a282f3b` (amendment 1's scope: the task-level audit bullet now says an incorrect verdict is dispositioned in the record's JSON `audit_findings` {n, reason, evidence} written by `acceptance-front-matter.py --audit-dispositions`, correct-verdict findings keep the `audit-finding:` prose; step 10.3 points to it; the 10.4 command without `AUDIT_DISPOSITIONS`; the `AUDIT_EVIDENCE` bullet; AGENTS.md's gate sentence), `audit:65a3d71:1` (disposition-range) names no sentence, no change; files AGENTS.md, the SKILL, `tests/unit/test_agmsg_orchestration_docs.py`, `tests/fixtures/regime/orchestrator-step-6.md`, `tests/fixtures/regime/invariants.md` (each fixture in its one changed sentence) plus the task evidence directory; tests 48 OK (two changed, one new `test_an_incorrect_audit_is_dispositioned_in_audit_findings`, the stale forms asserted absent); no threads; the Bot's single review clean (issue comment 6163090018 "Did not find any major issues", reviewed bd9e8a69; posted 613 s after `gh pr ready` 07:07:25Z); CI 13 of 13; caps 5 files outside `.orchestration/`, 6 added outside tests, 50 under tests. ACCEPTANCE `pending-integration head=bd9e8a69` 07:21:37Z (bus 1124, read); the chain runs after PR #353 merges (its merge moves main, one `update-branch` for this PR then).
graph_stale_changed_nonrecords=True

**Reviewing commit invariant compliance**
**Clarifying invariant mappings and evidence**

I’m outlining which task invariants apply and noting missing dispatch evidence, aiming to explain partial compliance without overstating results. I’ll keep the scope focused on confirmed holds like INV2 and INV12 while clarifying test gaps.
exec
/bin/zsh -lc "python3 -B -c '
import io, subprocess, types, unittest
from pathlib import Path
from unittest.mock import patch
root=Path.cwd()
head='\\''3a8f809b36944b0cb778da53104f9b3c54f67355'\\''
path='\\''tests/unit/test_agmsg_orchestration_docs.py'\\''
cache={}
def blob(rel):
    if rel not in cache:
        cache[rel]=subprocess.check_output(['\\''git'\\'','\\''show'\\'',f'\\''{head}:{rel}'\\''],text=True)
    return cache[rel]
module=types.ModuleType('\\''audited_docs_tests'\\'')
module.__file__=str(root/path)
exec(compile(blob(path),module.__file__,'\\''exec'\\''),module.__dict__)
tree=subprocess.check_output(['\\''git'\\'','\\''ls-tree'\\'','\\''-r'\\'','\\''--name-only'\\'',head,'\\''--'\\'','\\''home/dot_config/claude/rules'\\''],text=True).splitlines()
def read_text(p,*args,**kwargs):
    return blob(p.relative_to(root).as_posix())
def glob(p,pattern):
    rel=p.relative_to(root).as_posix()
    return iter(root/item for item in tree if str(Path(item).parent)==rel and Path(item).match(pattern))
out=io.StringIO()
with patch.object(Path,'\\''read_text'\\'',read_text),patch.object(Path,'\\''glob'\\'',glob):
    result=unittest.TextTestRunner(stream=out,verbosity=1).run(unittest.defaultTestLoader.loadTestsFromModule(module))
print('\\''Executed reviewed module with every repository read supplied by git show at '\\''+head+'\\''; no files written.'\\'')
print(out.getvalue())
print('\\''git_blob_inputs='\\''+str(len(cache)))
for rel in sorted(cache): print(rel)
raise SystemExit(not result.wasSuccessful())
'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 617ms:
Executed reviewed module with every repository read supplied by git show at 3a8f809b36944b0cb778da53104f9b3c54f67355; no files written.
................................................
----------------------------------------------------------------------
Ran 48 tests in 0.483s

OK

git_blob_inputs=25
AGENTS.md
CLAUDE.md
README.md
home/dot_agents/skills/agmsg-orchestration/SKILL.md
home/dot_agents/skills/gh-first-workflow/SKILL.md
home/dot_config/claude/rules/agmsg-orchestration.md
home/dot_config/claude/rules/ask-user-question.md
home/dot_config/claude/rules/compactiondb.md
home/dot_config/claude/rules/crit-review.md
home/dot_config/claude/rules/gpu.md
home/dot_config/claude/rules/latex.md
home/dot_config/claude/rules/model-selection.md
home/dot_config/claude/rules/ponytail.md
home/dot_config/claude/rules/pr-integration.md
home/dot_config/claude/rules/project-map.md
home/dot_config/claude/rules/python.md
home/dot_config/claude/rules/understand-anything.md
home/dot_config/codex/AGENTS.md
tests/fixtures/regime/code-review-orchestration.md
tests/fixtures/regime/invariants.md
tests/fixtures/regime/message-contract.md
tests/fixtures/regime/orchestrator-step-6.md
tests/fixtures/regime/orchestrator-step-7.md
tests/fixtures/regime/worker-step-15.md
tests/unit/test_agmsg_orchestration_docs.py

**Testing mutation on changed sentences**
**Verifying orchestration and token handling**
exec
/bin/zsh -lc 'crit status --json' in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 139ms:
{
  "branch": "HEAD",
  "daemon": {
    "running": false
  },
  "review_file": "~/.crit/reviews/c0209481ed61/review.json",
  "review_file_exists": false,
  "sessions": [],
  "vcs": "git"
}

exec
/bin/zsh -lc "git show 3a8f809b36944b0cb778da53104f9b3c54f67355:.orchestration/dotfiles-T128-playbook-rules-followup-a01/autoskill.md && git show 3a8f809b36944b0cb778da53104f9b3c54f67355:.orchestration/dotfiles-T128-playbook-rules-followup-a01/learning.md && git show 3a8f809b36944b0cb778da53104f9b3c54f67355:.orchestration/dotfiles-T128-playbook-rules-followup-a01/sandbox.md && git show origin/main:scripts/require-crit-review.py | nl -ba | sed -n '1015,1045p'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 42ms:
# AutoSkill run: dotfiles-T128-playbook-rules-followup-a01

- Status: not used. The task names no AutoSkill run.
# Learning triage: dotfiles-T128-playbook-rules-followup-a01

These are candidates only; nothing is promoted.

1. [memory:decision] An owner section can hold rows that name no rule sentence. `audit:65a3d71:1` (disposition-range) was a sweep-table correction, already made. Report such a row as no change with its reason, rather than inventing a sentence to edit.
2. [memory:failure] A retired gate input survives in every artifact that restated it. The audit named SKILL lines 171 to 178, but the task-level audit bullet and AGENTS.md:44 stated the same retired mechanism, so a migration fixed by line numbers stays half done. Before editing, grep the allowed files for the retired names (`AUDIT_DISPOSITIONS`, `audit-finding`) and ask once for the scope, with the hits pasted. Amendment 1 then named every sentence.
---
task_id: dotfiles-T128-playbook-rules-followup-a01
seat: claude-standard-dot-a002
permission_gated_commands: see the table
---

# Sandbox record: dotfiles-T128-playbook-rules-followup-a01

- Period: from the AGMSG-TASK (2026-10-14T06:47:41Z) to the RESULT.
- These ran inside the sandbox:
  - the HTTPS `git fetch` and `git push`;
  - the branch, the edits, the task copy and the commits;
  - every test and format run, with `UV_OFFLINE=1`, since uv cannot reach pypi from the sandbox.
- No local mutation was chained onto a call that ran outside the sandbox.

Calls outside the sandbox: `gh` through the permission gate (`dangerouslyDisableSandbox`; `gh` fails TLS inside the sandbox) and `agmsg-dispatch` through `excludedCommands`.

| # | Command | Step 4 case |
|--:|---|---|
| 1 | `agmsg-dispatch … AGMSG-PONG v1 task_id=dotfiles-T128-playbook-rules-followup-a01 status=question …` (06:50Z, the scope of the procedure-migration row) | `agmsg-dispatch` |
| 2 | `agmsg-dispatch … AGMSG-PONG v1 … status=alive note=working…` (06:53Z) | `agmsg-dispatch` |
| 3 | `gh pr create --draft …` | `gh` |
| 4 | `gh pr ready <n>` | `gh` |
| 5 | Bot wait from the ready (background; `gh api` reads every 30 seconds) | `gh` |
| 6 | `gh pr checks <n> --watch` (exit status joined) | `gh` |
| 7 | `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T128-playbook-rules-followup-a01 …` | `agmsg-dispatch` |
  1015	    feedback_document = json.loads((root / feedback).read_text()) if feedback else {}
  1016	    feedback_pr = feedback_document.get("pr") if feedback else None
  1017	    current_head = head or run_git(["rev-parse", "HEAD"], root).stdout.strip()
  1018	    acceptance, record = acceptance_errors(
  1019	        root,
  1020	        required=args.base is not None,
  1021	        task=task,
  1022	        head=current_head,
  1023	        pr=feedback_pr,
  1024	        items=feedback_document.get("items"),
  1025	    )
  1026	    if acceptance:
  1027	        print("Acceptance record evidence is incomplete:")
  1028	        for error in acceptance:
  1029	            print(f"- {error}")
  1030	        raise SystemExit(1)
  1031	    if os.environ.get(ACCEPTANCE_ENV, "").strip():
  1032	        print(f"Acceptance evidence accepted: {os.environ[ACCEPTANCE_ENV].strip()}")
  1033	    if os.environ.get(RETIRED_AUDIT_DISPOSITIONS_ENV, "").strip():
  1034	        print(
  1035	            f"{RETIRED_AUDIT_DISPOSITIONS_ENV} is retired and not read: the acceptance record's audit_findings disposition an incorrect audit."
  1036	        )
  1037	
  1038	    paths = changed_paths(root, args.base)
  1039	    reasons = review_reasons(root, paths, args.base)
  1040	    if not reasons:
  1041	        print("Review not required: no meaningful review trigger found.")
  1042	        return
  1043	
  1044	    if head is not None and not all(path.startswith(".orchestration/") for path in paths):
  1045	        errors = audit_errors(root, head, task, record)

**Clarifying test gate requirements**
**Finalizing audit summary format**

I’m making sure to follow the user’s requested summary structure: listing findings clearly, including orchestration counts and verdicts without extra lines, and covering all relevant test baselines, mutation checks, and task invariant mentions properly.
exec
/bin/zsh -lc "python3 -B -c '
import io, subprocess, types, unittest
from pathlib import Path
from unittest.mock import patch
root=Path.cwd()
head='\\''3a8f809b36944b0cb778da53104f9b3c54f67355'\\''
base='\\''6a2473f362762cf74c750f2141e5a11853816745'\\''
module_path='\\''tests/unit/test_agmsg_orchestration_docs.py'\\''
skill='\\''home/dot_agents/skills/agmsg-orchestration/SKILL.md'\\''
cache={}
def blob(ref,rel):
    key=(ref,rel)
    if key not in cache: cache[key]=subprocess.check_output(['\\''git'\\'','\\''show'\\'',f'\\''{ref}:{rel}'\\''],text=True)
    return cache[key]
module=types.ModuleType('\\''audited_docs_tests'\\'')
module.__file__=str(root/module_path)
exec(compile(blob(head,module_path),module.__file__,'\\''exec'\\''),module.__dict__)
cases=[
('\\''step 6'\\'',skill,164,'\\''test_dispatches_are_recorded_from_the_bus'\\''),
('\\''audit dispositions'\\'',skill,90,'\\''test_an_incorrect_audit_is_dispositioned_in_audit_findings'\\''),
('\\''step 10.3'\\'',skill,171,'\\''test_the_gate_reads_the_acceptance_record'\\''),
('\\''step 10.4 command'\\'',skill,172,'\\''test_the_gate_reads_the_acceptance_record'\\''),
('\\''step 10.4 audit evidence'\\'',skill,178,'\\''test_the_gate_reads_the_acceptance_record'\\''),
('\\''AGENTS gate sentence'\\'','\\''AGENTS.md'\\'',44,'\\''test_an_incorrect_audit_is_dispositioned_in_audit_findings'\\''),
]
for label,path,line,test in cases:
    new=blob(head,path).splitlines(keepends=True)
    old=blob(base,path).splitlines(keepends=True)
    assert new[line-1]"'!=old[line-1]
    new[line-1]=old[line-1]
    changed='"'\\'''\\''.join(new)
    def read_text(p,*args,**kwargs):
        rel=p.relative_to(root).as_posix()
        return changed if rel==path else blob(head,rel)
    with patch.object(Path,'\\''read_text'\\'',read_text):
        result=unittest.TextTestRunner(stream=io.StringIO()).run(unittest.TestSuite([module.AgmsgRegimePatternTest(test)]))
    print(label+'\\'': reverting documented change is detected by '\\''+test+'\\'' = '\\''+str(not result.wasSuccessful()))
    assert not result.wasSuccessful()
print('\\''Six independent regression checks completed in memory; no files written.'\\'')
'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 succeeded in 189ms:
step 6: reverting documented change is detected by test_dispatches_are_recorded_from_the_bus = True
audit dispositions: reverting documented change is detected by test_an_incorrect_audit_is_dispositioned_in_audit_findings = True
step 10.3: reverting documented change is detected by test_the_gate_reads_the_acceptance_record = True
step 10.4 command: reverting documented change is detected by test_the_gate_reads_the_acceptance_record = True
step 10.4 audit evidence: reverting documented change is detected by test_the_gate_reads_the_acceptance_record = True
AGENTS gate sentence: reverting documented change is detected by test_an_incorrect_audit_is_dispositioned_in_audit_findings = True
Six independent regression checks completed in memory; no files written.

**Confirming final verification steps**
**Assessing audit source and invariant findings**

I’m verifying that missing outputs in the audit are benign and supported by saved data, while checking dispatch records against acceptance snapshots for accuracy. I’m also considering task invariants and clarifying the absence of declared invariants to align with the user’s request and avoid false assumptions.
codex
All 48 documentation tests pass against the final-head Git blobs. Reverting each of the six rule edits in memory makes its token test fail, and both fixtures match their sections.

I found one orchestration evidence issue: the acceptance record refers to a “dispatch list above,” but it has no `dispatch` field or bus lines. Its summaries therefore don’t preserve the task payload hashes and delivery markers required by step 6.
exec
/bin/zsh -lc "git status --short && git diff --check 6a2473f362762cf74c750f2141e5a11853816745 3a8f809b36944b0cb778da53104f9b3c54f67355 && git show 3a8f809b36944b0cb778da53104f9b3c54f67355:AGENTS.md | nl -ba | sed -n '39,46p' && nl -ba .orchestration/acceptance/dotfiles-T128-playbook-rules-followup-a01.md | sed -n '1,22p'" in ~/Workspace/dotfiles/.claude/worktrees/orchestrator-review
 exited 2 in 67ms:
 M .orchestration/tasks/dotfiles-T128-playbook-rules-followup-a01.md
?? .orchestration/acceptance/dotfiles-T128-playbook-rules-followup-a01.md
?? .orchestration/reports/dotfiles-T128-playbook-rules-followup-a01.md
?? .orchestration/sandboxes/dotfiles-T128-playbook-rules-followup-a01.md
?? .orchestration/validation/dotfiles-T128-playbook-rules-followup-a01-audit-3a8f809.md
?? .orchestration/validation/dotfiles-T128-playbook-rules-followup-a01-pr-feedback.json
?? .orchestration/validation/dotfiles-T128-playbook-rules-followup-a01.md
.orchestration/dotfiles-T128-playbook-rules-followup-a01/validation.md:52: trailing whitespace.
+171:    3. Write the acceptance record, summarising the dispositions, with every audit finding dispositioned as the task-level audit bullet 

**Finalizing CI instruction format**
**Structuring final verdict and summary**
codex
[P2] high confidence orchestration .orchestration/acceptance/dotfiles-T128-playbook-rules-followup-a01.md:17 The referenced “dispatch list above” is absent: neither the JSON nor the prose contains the required bus lines. The initial and amended TASK payloads, hashes and read markers therefore cannot be checked against this record. Restore the bus-derived `dispatch` entries required by step 6 and task item 1.

The implementation matches the four owned rows. Both rule-gap rows share the step-6 fix; the migration covers all specified locations; disposition-range correctly requires no edit. No unrelated rule sentences changed, and the documented mechanisms exist on main. Both fixtures match. All 48 tests pass; reverting each of the six rule edits makes its token test fail. Final-head Actions succeeded for [PR #354](https://github.com/mryfmo/dotfiles/pull/354).

The task declares no `invariants` map; its directly applicable caps and test requirements were checked:

INV-2: holds .orchestration/dotfiles-T128-playbook-rules-followup-a01/validation.md:164 — verified 5 files, 6 added non-test lines and 50 added test lines.
INV-12: holds tests/unit/test_agmsg_orchestration_docs.py:519 — token regression checks and matching whole-section fixtures pass.

📝 まとめ: Read-only audit completed; the implementation passes, but the acceptance record lacks its cited dispatch evidence.

Orchestration findings: 1
Not checked: local Bats and the merge gate; dispatch evidence remains incomplete.
Verdict: incorrect
hook: Stop
hook: Stop Completed
tokens used
258,899
[P2] high confidence orchestration .orchestration/acceptance/dotfiles-T128-playbook-rules-followup-a01.md:17 The referenced “dispatch list above” is absent: neither the JSON nor the prose contains the required bus lines. The initial and amended TASK payloads, hashes and read markers therefore cannot be checked against this record. Restore the bus-derived `dispatch` entries required by step 6 and task item 1.

The implementation matches the four owned rows. Both rule-gap rows share the step-6 fix; the migration covers all specified locations; disposition-range correctly requires no edit. No unrelated rule sentences changed, and the documented mechanisms exist on main. Both fixtures match. All 48 tests pass; reverting each of the six rule edits makes its token test fail. Final-head Actions succeeded for [PR #354](https://github.com/mryfmo/dotfiles/pull/354).

The task declares no `invariants` map; its directly applicable caps and test requirements were checked:

INV-2: holds .orchestration/dotfiles-T128-playbook-rules-followup-a01/validation.md:164 — verified 5 files, 6 added non-test lines and 50 added test lines.
INV-12: holds tests/unit/test_agmsg_orchestration_docs.py:519 — token regression checks and matching whole-section fixtures pass.

📝 まとめ: Read-only audit completed; the implementation passes, but the acceptance record lacks its cited dispatch evidence.

Orchestration findings: 1
Not checked: local Bats and the merge gate; dispatch evidence remains incomplete.
Verdict: incorrect
