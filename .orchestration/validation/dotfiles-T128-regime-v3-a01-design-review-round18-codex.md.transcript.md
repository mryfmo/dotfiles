Reading additional input from stdin...
OpenAI Codex v0.161.0
--------
workdir: ~/Workspace/dotfiles
model: gpt-5.6-sol
provider: openai
approval: never
sandbox: read-only
reasoning effort: low
reasoning summaries: concise
session id: 01a129e3-708b-7783-bb1e-9c167afbf609
--------
user
You are the Codex design reviewer (read-only), round 18 (one pair with the Claude reviewer on the same hash). Your round-17 receipt (.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round17-codex.md) accepted the design at whole-file sha256 15957fbc6b47ff8f2424072ca5b5849911b7be90582e1d850f5d315563494cd4 (v16). The design .orchestration/tasks/dotfiles-T128-regime-v3-a01.md is now v17 (whole-file sha256 1d5f4c07e8a23d0bc5185931fe1037c16b76ae48441b62ffb05bd3ffde2ac0a5). The delta is exactly two hashed map lines in implementing_tasks: `dotfiles-T128-ci-skip-orchestration-a02: [INV-2]` inserted after the ci-skip a01 entry and `dotfiles-T128-regime-counters-a02: [INV-6]` inserted after the regime-counters a01 entry. The a02 tasks are the INV-6 reset continuations of their a01 tasks (reset records .orchestration/acceptance/dotfiles-T128-ci-skip-orchestration-a01-design-reset.md and dotfiles-T128-regime-counters-a01-design-reset.md; task files .orchestration/tasks/dotfiles-T128-ci-skip-orchestration-a02.md and dotfiles-T128-regime-counters-a02.md, each with reset_of). INV-2 compares a task's invariant ids with the map by task id and remaps only -contract-a01 ids, so without these entries a reset successor cannot satisfy INV-2 on main. Judge only the delta: do the entries name the same invariants as the tasks they succeed, and does a reset successor under INV-2 or INV-6 need anything else in the hashed keys (for example a general rule mapping a reset_of successor to its predecessor's entry instead of per-task lines). Confirm INV-1..INV-12 and the premises unchanged against your round-17 receipt (the removal of the two lines reproduces 15957fbc). Write 'INV-n: accepted' or 'INV-n: rejected: <wrong and right, achievable here>' for each, then '## Findings' (delta only), '## Residual', and exactly one final line 'Design verdict: accept|revise|reject'. Header lines first: reviewed_at (UTC ISO), reviewer: codex-review-dot-h001 (headless), profile: review, design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@1d5f4c07e8a23d0bc5185931fe1037c16b76ae48441b62ffb05bd3ffde2ac0a5, round: 18, previous: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round17-codex.md. Do not edit any file; your final message is the receipt.
warning: loading hooks from both ~/.codex/hooks.json and ~/.codex/config.toml; prefer a single representation for this layer
hook: SessionStart
hook: SessionStart
hook: SessionStart Completed
hook: SessionStart Completed
hook: UserPromptSubmit
hook: UserPromptSubmit Completed
**Reviewing relevant files**
codex
🤖 I read the AGENTS.md for mryfmo/dotfiles.

`agmsg-orchestration` の Codex seat worklog と Ponytail のレビュー方針を確認し、指定された v16→v17 の2行だけを読み取り専用で検証します。ファイルは編集しません。
exec
/bin/zsh -lc "sed -n '1,240p' ~/.agents/skills/agmsg-orchestration/SKILL.md && sed -n '1,220p' ~/.codex/plugins/cache/ponytail/ponytail/5.1.0/skills/ponytail-review/SKILL.md" in ~/Workspace/dotfiles
 succeeded in 24ms:
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

**Reviewing worklogs and files**
codex
スキル上は通常 plan/todo 更新が必要ですが、この依頼は明示的な read-only かつ「編集禁止」なので、worklog は作成・更新せず、レビュー証跡そのものを最終回答として返します。次にハッシュ、round 17、reset 記録、a02 task の invariant 宣言を突合します。
exec
/bin/zsh -lc "sha256sum .orchestration/tasks/dotfiles-T128-regime-v3-a01.md .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round17-codex.md 2>/dev/null || shasum -a 256 .orchestration/tasks/dotfiles-T128-regime-v3-a01.md .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round17-codex.md
sed -n '1,260p' .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round17-codex.md
rg -n -C 3 'implementing_tasks|ci-skip-orchestration|regime-counters|INV-[0-9]+|premise|Premise' .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
for f in .orchestration/acceptance/dotfiles-T128-ci-skip-orchestration-a01-design-reset.md .orchestration/acceptance/dotfiles-T128-regime-counters-a01-design-reset.md .orchestration/tasks/dotfiles-T128-ci-skip-orchestration-a02.md .orchestration/tasks/dotfiles-T128-regime-counters-a02.md; do echo \"FILE "'$f"; sed -n '"'1,260p' \""'$f"; done' in ~/Workspace/dotfiles
 succeeded in 104ms:
1d5f4c07e8a23d0bc5185931fe1037c16b76ae48441b62ffb05bd3ffde2ac0a5  .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
9625f83e73c79a0c347293b03f9ce7e1866be1ca43a094cb9b52207d3db978f6  .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round17-codex.md
reviewed_at: 2026-10-11T04:16:15Z  
reviewer: codex-review-dot-h001 (headless)  
profile: review  
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@15957fbc6b47ff8f2424072ca5b5849911b7be90582e1d850f5d315563494cd4  
round: 17  
previous: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round16-codex.md

INV-1: accepted

INV-2: accepted

INV-3: accepted

INV-4: accepted

INV-5: accepted

INV-6: accepted

INV-7: accepted

INV-8: accepted

INV-9: accepted

INV-10: accepted

INV-11: accepted

INV-12: accepted

## Findings

The silencing-record row closes the first gap. Acceptance is anchored to GitHub merge state, reset to an independently authored design RESULT in agmsg history, and waiver handling to INV-1’s protected state-directory path; its three negative tests cover the forged forms identified in round 16.

The PR-control row honestly states the second gap as residual rather than closed. Its trusted-root design audit, live acceptance replay against independently computed premises, later main-tests guard, and explicit withdrawal of dormant contracts are appropriate compensating controls under INV-6 and trust anchors 1, 4, and 5.

## Residual

The PR still authors the counter implementation, tests, fixtures, and `source=` label. Acceptance therefore depends on the named trusted-root audit and live replay until V0’s main-tests protection lands. V3a remains responsible for the mandatory merge backstop and protected waiver path. Implementation and tests were not executed; no files were modified.

Design verdict: accept6-design_review:
7-  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round15.md
8-  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
9:implementing_tasks:
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
28-supersedes:
29-  - dotfiles-T126-regime-v2-a01
30-  - dotfiles-T124-design-gate-and-reset-rule-a01
--
32-  - dotfiles-T124-wave1-task-validator-a01
33-  - dotfiles-T124-wave3b-audit-grammar-a01
34-threat_model:
35:  R1: rounds are judged by models re-reading models and add no deterministic fact, so a wrong premise is patched round after round (T118 20 revises, T119 5 revises and 4 audits; the vendor's own rule is two corrections, then start fresh)
36:  R2: "hand-written parsers at a trust boundary have an unbounded bypass surface (PR 313: 33 of 52 Bot threads on a 503-line validator with its own YAML parser, written on the false premise that PyYAML is unavailable)"
37-  R3: "PRs larger than a reviewer can hold (PR 313 20 files +2642, PR 312 37 files +3191; Google: 100 lines reasonable, 1000 too large)"
38:  R4: task text grown by question-and-amendment (PR 313 6 questions 8 amendments, T119 8 and 8, T120 8 amendments and no RESULT) keeps the under-researched premise
39-  R5: the orchestrator's artifacts are unaudited and it dispositions findings about itself (T119 audit-finding 2); the reset rule was prose the orchestrator could waive (PR 313 revise round 2)
40-  R6: "the auditor becomes a serial queue when audits run once per round in one tab (measured: 4 audits about 1.3 h of T119's 11.1 h; the rounds, not the audits, were the cost)"
41-  R7: cost is unmeasured (every acceptance record says cost n/a) so no stage can be weighed against its value
--
47-  - the operator waiver is visible, not prevented (acceptance record, boundary PR body, check-regime-boundary)
48-  - a reset is released only by a redesign written in a context other than the one that wrote the abandoned task, or by the operator
49-invariants:
50:  INV-1: "every task is a format-2 file whose front matter validates against schemas/task.json (jsonschema + PyYAML, no hand-written parser; every allowed_files entry starts with a literal path segment and a wildcard entry derives the tier of every design-tier path its literal prefix can cover); legacy task ids are grandfathered only for files under .orchestration/tasks/ on main, never for a branch copy; the tier (docs, review, design) is derived from allowed_files by the shared high-risk module, with the regime's own rule prose (home/dot_config/claude/rules/**, the agmsg-orchestration SKILL, AGENTS.md, README) listed in the review tier, and selects the pipeline from process_tiers in agent-config.yaml; every AGMSG-TASK for the task, the first and each amendment, carries task_sha256= of the task file as sent, the worker commits the file byte-identical to .orchestration/<task id>/task.md (first commit, recommitted after each amendment), the CI regime job validates that copy with main's schema and refuses a PR that changes .github/workflows/** unless its task.md is design tier and lists the file, the host gate compares the copy's sha256 with the latest AGMSG-TASK's token in history, and the regime check binds only once the ruleset lists it as required (an operator action named in V1's acceptance record); the orchestrator can add or skip a stage only with an operator waiver written by scripts/regime-waive.sh, a command under a permissions.ask rule in the managed settings with no permgate policy entry, so that only the human's answer to the native prompt runs it (an ask rule prompts even in auto mode; agent-to-agent approval is forbidden); the waiver names the task, the stage and a reason and is written under $XDG_STATE_HOME/regime/waivers/, a directory outside every seat's sandbox write roots, so no sandboxed seat can write it and only a command run outside the sandbox on the human's answer to the native prompt can (the directory is the guard; the ask rule on the named command is the second layer, since a reworded command would still meet the prompt at the sandbox boundary); it is listed by check-regime-boundary.sh and the boundary PR body (V3a owns the script and its ask rule), and is the strongest friction available on a machine where every seat and GitHub action is the operator's own account (operator authentication is a stated residual, not a claim)"
51:  INV-2: "a PR is mergeable only within the caps the CI regime job enforces from main's workflow (at most 15 changed files outside .orchestration/, 500 added lines outside tests/, .orchestration/ and the data list scripts/legacy-task-ids.txt, and 1000 added lines under tests/), and its task.md invariants equal the design's as a set of ids and byte-for-byte as sentences (the design read from main, never from the PR; a task id ending in -contract-a01 is compared with its implementing task's entry); the design file must be on main (through a boundary PR) before the implementing TASK is dispatched and the regime job fails closed when the design named by task.md is absent from main; an .orchestration-only PR runs no bootstrap or test matrix and every required check context still reports success (each required workflow decides inside its jobs, as test.yaml's changes job does), so a boundary PR merges in minutes; exceeding a cap is a split, never a finding to disposition (the cap changes the unit of work: T116 +529 and T118 +881 would have been split)"
52:  INV-3: "a revise round is admissible only when it adds a new deterministic check: the AGMSG-ACCEPTANCE status=revise carries check=tests/<file>::<name> and previous_head=<the RESULT head being revised>, the worker records both in .orchestration/<task id>/revise.yaml (a sibling file; task.md stays byte-identical to the dispatched file), the main-pinned regime job verifies that the named test file exists on the head and differs between previous_head and the head, the PR's own unit-test workflow (a required check, run in the PR's context) collects and runs exactly that selector on the head (it must pass) and on previous_head (it must fail or be absent), and the host gate, which reads history, verifies that previous_head equals the head of the previous AGMSG-RESULT for the task and requires the same selector in the validation file; a finding that cannot become a test is dispositioned, never iterated"
53:  INV-4: "a task file carries premises, each with the command and pasted output that verified it before dispatch; premises are evidence for the design reviewers and the auditor, each of whom dispositions every premise in the receipt or audit JSON as holds, fails or unverifiable (a local command re-run, an external claim re-fetched; a fails is a specification finding and a rejection), a complete disposition the schema requires rather than a sample, and the mechanical part of this invariant is the counting: a worker question (AGMSG-PONG status=question) is a specification defect answered by at most one further AGMSG-TASK, amendments are every AGMSG-TASK for the task_id after the first, whatever its wording, and the second amendment or the second question is INV-6's count, which withdraws the task to design through INV-6's merge backstop and Stop signal"
54:  INV-5: "the task-level audit is a headless read-only run whose instruction root is the trusted main checkout and whose schema is main's schemas/audit.json: codex exec --output-schema <main>/schemas/audit.json -C <main> with the detached worktree at the head added as a read-only data directory (--add-dir), so the audited PR controls neither the schema nor the AGENTS.md the auditor reads; the fallback claude -p --json-schema from the same root with --add-dir <worktree>, --bare when an API key is set and otherwise with project and user hooks disabled, and refused with exit 2 blocked when the head changes any file under .claude/ (bare mode loads skills from an --add-dir directory's .claude/skills/), leaving such a head to the codex path), with at most one valid audit per head (a stale input manifest invalidates an audit and a new audit of the same head replaces it), pooled two at a time; the gate accepts an audit of an earlier head only when git diff --quiet <audited head> <HEAD> -- . ':!.orchestration' holds (an evidence-only revision), otherwise a new audit is required; its input includes the task's invariants and premises, the worker's evidence, the orchestrator's task file and amendments, the acceptance record as it stands when present (its text above the line <!-- audit-input-boundary --> is the pre-audit part; dispositions of this audit's findings are appended below it), the head's pr-feedback JSON and the previous round's audit JSON; the audit JSON carries an input manifest (path to sha256 of every input as read, computed by the runner, which overwrites any model-supplied value) and the gate recomputes the manifest at gate time, so a pre-audit input edited after the audit makes the audit stale and a new audit is required; the schema lists findings {priority, confidence, category in {specification, implementation, evidence, orchestration, conformance}, path, line, rationale} and the per-invariant map before the verdict, and the prompt asks for the rationale before each verdict; the runner, under the identity claude-audit-dot-h001 or codex-audit-dot-h001 on the orchestrator's host, records the JSON's sha256 in agmsg history (AGMSG-AUDIT v1 task_id= head= sha256= auditor=) before the gate reads it, an anchor that prevents edits after the record and not fabrication before it; the gate reads the verdict and categories from the JSON, and orchestration and conformance findings at P0-P2 accept only an operator waiver or a design reset, never not-applicable"
55:  INV-6: "the reset rule's mandatory point is the merge backstop in scripts/require-crit-review.py, with the orchestrator's Stop hook (Claude Stop hook, Codex [hooks].Stop) as the early signal, soft on both runtimes by their documented caps; counts come from history for the hook and the gate (revises = RESULTs for the task_id minus one, threshold 2; amendments = AGMSG-TASKs after the first, threshold 2; AGMSG-PONG status=question, threshold 2) and from GitHub and main-checkout files for the gate and the boundary check only (Codex Bot P0 or P1 on two heads after the first RESULT, from original_commit_id on review_comment items recorded by pr-feedback.py; an audit implementation or specification finding at P0-P1 on two heads, from .orchestration/validation/<task>-audit-<sha7>.json in the main checkout, each counted only when its sha256 matches its AGMSG-AUDIT record); when a count is reached the gate refuses the merge until a reset record names a redesign task whose design RESULT comes from an identity other than the task's author, or a waiver written by scripts/regime-waive.sh under the INV-1 ask-rule discipline into the state directory outside the sandbox write roots (the only release path besides a redesign; the one-account residual of INV-1 applies); check-regime-boundary.sh reports a closed-unmerged PR whose task has no reset record and a task over any count with neither an accepted acceptance record nor a reset record"
56:  INV-7: "the design tier adds, before any code is dispatched, two design reviews of the same design hash: a fresh Claude context on the review profile (a headless run or a seated -review- identity; the review profile is the same model and effort as deep, so the lever is the separate context) and a Codex read-only review (codex exec --sandbox read-only on the review profile under a codex-review identity: headless through V4's runner, or seated until V4); each receipt is a schema document naming the design file's canonical hash over invariants, threat_model, trust_anchors, implementing_tasks and premises, each is announced by an AGMSG-RESULT from its reviewing identity, and both RESULTs precede the implementing AGMSG-TASK in history; the Codex Bot's review of a boundary PR is swept feedback, never a design receipt; a change to the hashed keys needs new reviews; the gate accepts the whole-file sha256 form for receipts written before V4 lands"
57:  INV-8: "worker evidence (the task.md copy, revise.yaml, report, validation, sandbox, learning, autoskill, worker review JSON) is committed on the PR branch under .orchestration/<task id>/ before the final RESULT so the Bot, CI and the gate read the same files from the audited head; the orchestrator's records (audit JSON, acceptance, pr-feedback) stay under .orchestration/validation and .orchestration/acceptance in the boundary commit because the merge is --match-head-commit"
58:  INV-9: "every acceptance record carries measured cost (rounds, amendments, questions, wall time TASK to final RESULT from history timestamps, audit count, Bot threads, tokens: total_cost_usd from claude -p JSON, turn.completed.usage from codex exec --json, per-message usage from the seat's session transcript) written by accept-task.py, which also records the path and sha256 of every raw source it read (the headless runs' JSON, the transcript files at acceptance time) so a total can be recomputed; cost is a warning metric, never a gate: each tier has a budget, the acceptance record names the operator decision when it is exceeded, and check-regime-boundary.sh warns; headless runs carry --max-budget-usd"
59:  INV-10: "at most three concurrent workers with pairwise-disjoint allowed_files; the first push is the draft PR's server-side created_at (gh api pulls/<n>), which must fall within 30 minutes of the TASK's history timestamp, and a seated worker is not idle for 20 minutes while a dispatchable task exists, a dispatchable task being a format-2 file under .orchestration/tasks/ with no AGMSG-TASK for its id in history, no superseded_by or reset record, and every task id in its after list accepted (an acceptance record with Decision accepted in the main checkout); both computed in check-regime-boundary.sh and accept-task.py, never in the Stop hook; headless reviews and audits do not count as workers"
60:  INV-11: permgate records session_id and cwd per decision, and the gate compares a Claude worker's permission-gated Bash count in the task window with the sandbox record (an understated record is refused); Codex workers cannot escalate and are not covered
61:  INV-12: "every rule above is exercised by a unit test that fails when the rule is removed; the PR's own workflow runs the PR's tests, and a required check main-tests (wave V0, before every other wave) fetches main's tests/unit and runs them in the PR's context in two modes: for a script outside the task.md's allowed_files it runs main's module as it is, so an undeclared change to any script fails; for a script inside allowed_files it runs only main's dormant contract tests for that module (tests marked with the regime's contract decorator, which skip in ordinary CI and run when REGIME_CONTRACT=1), so an intentional change is judged by the contract that was reviewed and merged on main before the implementation; the implementation PR promotes those contracts by removing the decorator in its own tree (main-tests judges it against main's dormant copy, so nothing stays dormant after the wave lands), main-tests fails an implementation PR (any task id not ending in -contract-a01) whose declared test module in the PR tree still carries a contract marker, and main-tests fails a design-tier implementation PR whose declared script has no dormant contract on main (an empty contract is not a pass); a design-tier code wave lands its contract tests first in a <task>-contract-a01 PR (dormant, hence mergeable), a review-tier wave may; the design-tier audit from the trusted root reads the diff; a deleted or weakened fails-when-removed test is a conformance finding; main-tests is an in-process oracle: code that main's tests import from the PR runs inside the test process, so the harness authenticates that main's runner reached its end with a per-run nonce that only the runner sees (read from a pipe and closed before any test loads, written back with the counts), and the runner pins unittest's result and runner classes before importing any test; the nonce authenticates the writer, not the counts: adversarial PR code running in the same process can still patch result collection or read the nonce from a frame, so in-process forgery remains a stated residual that the trusted-root audit catches, named in every acceptance record of a design-tier PR; including one test per gaming path (a schema-valid task with a prose cap bypass, a revise without a named check, a revise list appended to the hashed task.md, an AGMSG-TASK without amendment= that still counts, an evidence-only relabel of a code change caught by the tree-equality check, a wave-table rewrite after review, an audit JSON edited after its history record, a receipt whose hash predates a key change, a reset record naming the author's own identity, a Bot-skipped head whose audit never starts, a single PR split only in the task file, a branch task.md claiming a legacy id, allowed_files of ['*'] or a wildcard first segment, an invariant sentence weakened under its id, a schema or AGENTS.md edited on the audited head, an undeclared script change that main-tests must fail); legacy task ids are grandfathered by the checked-in list scripts/legacy-task-ids.txt, which only shrinks and is excluded from the line cap as data"
62:premises:
63-  - claim: PyYAML is already installed by uv in the Makefile and CI; jsonschema is not yet named anywhere and V1 adds --with jsonschema; both resolve through uv on this host
64-    command: "grep -n 'with pyyaml\\|jsonschema' Makefile .github/workflows/*.yml; uv run --no-project --with jsonschema --with pyyaml python -c 'import jsonschema, yaml; print(jsonschema.__version__, yaml.__version__)'"
65-    output: "Makefile:189 and :203 and agent-assets.yml:35 use --with pyyaml; no jsonschema anywhere; 4.26.0 6.0.3"
--
108-
109-## 1. Finding: the fix program tripped its own rule
110-
111:By T126 INV-6 as written: wave 1 (PR #313) 8 amendments (limit 4) and 2 revises (limit 2); wave 3b (PR #314) Bot P1 on two post-RESULT heads. The orchestrator was drafting a waiver for #313. T120 was reset only on the operator's question. The regime is therefore reset here by its own rule; this document is the redesign, and T126 and T124 are superseded (their accepted ideas are kept where named).
112-
113-Measured baseline (history + GitHub):
114-
--
129-
130-## 3. Principles (each names what it reuses and what it deletes)
131-
132:- **P1 One deterministic fact per round (INV-3).** Reuses tests/unit, CI, `pr-feedback.py`. Deletes free-form revise rounds and the audit-per-round habit.
133:- **P2 Declarative over imperative at trust boundaries (INV-1, INV-5, INV-7).** Reuses `jsonschema`, PyYAML, `codex exec --output-schema`, `claude -p --json-schema`. Deletes the bespoke YAML parser, the glob NFA, the prose verdict grammar, regex parsing of `.last.md`, and the T126 "process_tiers.json next to the module" indirection (the validator reads the manifest with PyYAML).
134:- **P3 Small one-invariant PRs enforced in CI (INV-2).** Reuses GitHub required checks and the strict up-to-date ruleset already in force. Deletes waves declared inside a task file.
135:- **P4 Main-pinned mechanical checks in CI; host gate only for history-anchored rules (INV-1, INV-2, INV-8 in CI; INV-3, INV-5 record, INV-6, INV-7 anchor, INV-11 on the host).** Reuses `pull_request_target`, the `changes` job pattern that reports success for an `.orchestration`-only diff. Deletes PR #313's `REVIEW_TREE` idea (never on `main`) and the copy step of untracked evidence into the gate's cwd. The host gate `make require-crit-review` keeps its evidence rules and changes three of them in named waves: the audit verdict and categories come from the schema JSON with the `AGMSG-AUDIT` record and the category lock (V2b), the reset backstop and the Bot-head count (V3a), the history-anchored design review (V4); it continues to run from the orchestrator's main checkout.
136:- **P5 Research before dispatch; a question ends the task, not amends it (INV-4).** Reuses history (`amendment=`, `status=question`). Deletes the amendment-per-question practice. The task file's `premises` block is the mechanical residue of "verify every CLI constraint by running the real command".
137:- **P6 Reset is mechanical, loop-time, and released only by another context or the operator (INV-6).** Reuses `scripts/require-crit-review.py` as the mandatory point, `agent-stop-gate.sh` and the Codex `[hooks].Stop` as the early signal (both soft by their documented caps: Claude's 8-continuation cap, Codex's continuation prompt), `check-regime-boundary.sh` for the re-dispatch detector. Deletes the orchestrator-written redesign (the redesign author is a `review`-profile seat or a fresh headless context; the `redesign` profile of T124 v4 is dropped: `review` is the same model and effort as `deep`, so independence of context is the whole lever, and T124 round 1 showed it works).
138:- **P7 Audit staging by tier; the auditor never serializes the pipeline (INV-5, process_tiers).** See section 4.
139:- **P8 Cost measured, budgets per tier (INV-9).** Reuses the JSON cost fields the runtimes already emit and the session transcripts. Deletes `cost: n/a`.
140:- **P9 Parallelism with disjoint files and early push (INV-10).** Reuses `herdr-agents --add-worker`, draft PRs.
141-- **P10 Routing stays by boundary.** Claude-boundary sources to a Codex seat, Codex-boundary to a Claude seat, permgate and shared gate sources to the operator, as the agmsg-orchestration skill's step 3 states; nothing here changes that.
142-
143-## 4. Audit stages (process_tiers; the one table the validator reads)
144-
145-| stage | who | when | tier docs | tier review | tier design | cost |
146-|---|---|---|---|---|---|---|
147:| 0 design review | a fresh Claude context on the review profile and a Codex read-only review of the same hash, schema receipts (INV-7) | before any code | - | - | required | minutes |
148-| 1 worker checks | worker in its sandbox: invariant tests first, shellcheck, unit tests | before every push | required | required | required | none for the regime |
149-| 2 CI + Bot | main-pinned `regime` check (schema, caps, evidence shape) + unit tests + Codex Bot | every push, in parallel | required | required | required | none |
150:| 3 schema audit | headless read-only `codex exec --output-schema`, pooled 2, started by `make audit-head` once CI is green and the Bot reviewed or 15 min passed, once per RESULT head, reused for an evidence-only head by tree equality (INV-5) | per RESULT head | - | required | required, with invariant map and permgate window | the scarce resource, now off the critical path |
151-| 4 acceptance | orchestrator: sweep, dispositions, record, host gate, merge `--match-head-commit` | per RESULT | required | required | required | minutes |
152-
153:Tier derivation: docs = prose-only `allowed_files` outside the regime's own rule prose (`home/dot_config/claude/rules/**`, the agmsg-orchestration SKILL, `AGENTS.md`, README), which is review tier by explicit list; review = the existing review-tier paths (scripts, hooks, tests, templates); design = the explicit design-tier list from T124 INV-2 v3 (install/**, setup.sh, the gate scripts, `executable_herdr-agents`, `executable_permgate`, Codex and Claude policy, sandbox and permission settings, credential helpers). Round limits: docs 1 revise; review and design 2 revises then reset. Profiles: worker `standard` (docs `express`), review `review`, audit `audit`.
154-
155-Why stage 3 is not the queue: the orchestrator starts it with `make audit-head` when the RESULT arrives (the wait on CI and the Bot is inside the target), it runs concurrently (pool of two, each in its own detached worktree), once per head, and an evidence-only head reuses the earlier audit by tree equality; the measured cost of the old serial form was 1.3 h of 11.1 h, so the throughput levers are P1 and P6, and the pool removes the residual queue.
156-
--
158-
159-| invariant | enforcement point |
160-|---|---|
161:| INV-1 | `.github/workflows/regime.yml` (`pull_request_target`, required check `regime`: validates `.orchestration/<task id>/task.md` from the PR head read as data, refuses workflow edits outside a design-tier task; an explicit Actions event policy allowing `pull_request_target` is set by the operator before 2026-11-02, named in V1c's acceptance record), `scripts/validate-task.py` (schema + PyYAML, about 80 lines), `schemas/task.json`, `scripts/lib/high_risk_paths.py` (new module: tier lists and `tier_of`), `scripts/legacy-task-ids.txt` (grandfather list), `process_tiers` in the manifest; host gate compares the copy's sha256 with `task_sha256=` in history (V3a); stage waivers by `scripts/regime-waive.sh` under its `permissions.ask` rule, written outside the sandbox write roots (V3a) |
162:| INV-2 | `regime.yml` step with `scripts/pr-caps.sh` and the task.md invariant-id comparison against the design's `implementing_tasks` |
163:| INV-3 | `regime-check.sh` step: the test selector named in `.orchestration/<task id>/revise.yaml` (sibling of the byte-identical task.md) exists on the head and its file differs between `previous_head` and the head; a `revise-check` job in `test.yaml` (PR context, required) runs exactly that selector on both heads; the host gate's `previous_head` history check and validation-file line are V2b's |
164:| INV-4 | `scripts/validate-task.py` (premises required for code and design tasks); `agent-stop-gate.sh` early signal on the second AGMSG-TASK or second PONG question; the merge backstop is INV-6's |
165:| INV-5 | `schemas/audit.json` (findings and invariant map before verdict), `scripts/audit-head.sh` (about 100 lines: detached worktree, `codex exec`, fallback, sha256 to history under the audit identity, `.last.md` render; PR #314's hardening kept), `make audit-head` target around `gh pr checks --watch` and the SKILL's Bot list loop with its 15-minute `bot: none` rule (no daemon), `AGENTS.md` Audit section; gate: JSON verdict and categories, `AGMSG-AUDIT` lookup, category lock, tree-equality acceptance of an earlier head (V2b) |
166:| INV-6 | `scripts/require-crit-review.py` (mandatory: history counts, Bot heads from `original_commit_id` recorded by `scripts/pr-feedback.py`, audit heads from the main checkout's audit JSONs whose sha256 matches their `AGMSG-AUDIT` record, reset record or a `scripts/regime-waive.sh` waiver), `scripts/agent-stop-gate.sh` and the manifest's `codex.hooks` Stop entry (early signal, history counts only, within the 3 s history budget), `scripts/check-regime-boundary.sh` (closed-unmerged PR without a reset record; over-count task without an accepted or reset record; waiver listing) |
167:| INV-7 | `scripts/design-review.sh` + `schemas/design-review.json`: two headless runs per design hash, `claude -p` under `claude-review-dot-hNNN` and `codex exec --sandbox read-only` under `codex-review-dot-hNNN`, each joining for the run and sending its RESULT; gate: both RESULTs precede the implementing TASK, both hashes recomputed, whole-file form accepted for pre-V4 receipts |
168:| INV-8 | worker writes under `.orchestration/<task id>/` on the branch (task.md copy first); `regime.yml` validates the evidence JSON shapes; the gate's existing path rules keep the orchestrator's records under `validation/` and `acceptance/` |
169:| INV-9 | `scripts/accept-task.py` (sweep, dispositions scaffold, record rows, gate invocation, merge command, cost fields), budgets in `process_tiers`, `check-regime-boundary.sh` warning |
170:| INV-10 | `scripts/check-regime-boundary.sh` and `scripts/accept-task.py` from `history.sh` timestamps (storage facade or `--limit`, never the 20-row default), the draft PR's `created_at` from `gh api pulls/<n>`, and the task's `after` list against acceptance records |
171:| INV-11 | `executable_permgate` (operator-routed, Codex security review) + gate cross-check |
172:| INV-12 | one test module per script; `make unit-test` in CI; the `main-tests` required job (V0): main's modules for scripts outside the PR's `allowed_files`, main's dormant contracts (`REGIME_CONTRACT=1`) for scripts inside it; contract PRs (`<task>-contract-a01`, dormant tests, merged before a design-tier implementation); the auditor checks per PR that no new hand-written parser sits at a trust boundary (a `conformance` finding) |
173-| prose | SKILL, `agmsg-orchestration.md`, `pr-integration.md`, `crit-review.md`, `model-selection.md`, README: each wave edits only the sections it implements |
174-
175:## 6. Waves (one PR, one invariant, within INV-2's caps; each task file reviewed by a fresh context before dispatch)
176-
177:- **V0** INV-12: the `main-tests` required job in `test.yaml` (main's `tests/unit` in the PR's context: modules of scripts outside the PR's `allowed_files` as they are, dormant contract tests of scripts inside it with `REGIME_CONTRACT=1`), the contract decorator in `tests/unit/regime_contract.py`, and the two-mode protocol in the Worker Playbook; lands before every other wave. Claude seat; design tier (workflow); the operator lists the check at its acceptance.
178:- **V1** INV-1, validation only (operator direction 2026-10-11, relayed through the review seat; also the cap: the undivided V1 sat at 500 added lines): `schemas/task.json`, `scripts/validate-task.py`, `scripts/lib/high_risk_paths.py`, `scripts/legacy-task-ids.txt` (from PR #313; data, excluded from the line cap), `tests/unit/test_validate_task.py`. Claude seat. Design tier: this review is its stage 0. Precondition: this design is on `main` through a boundary PR before V1's TASK is dispatched.
179:- **V1c** INV-1, the CI check (after V1): `scripts/regime-check.sh`, `.github/workflows/regime.yml` (task.md validation, workflow-edit refusal, `workflow_dispatch` dry run), `tests/unit/test_regime_check.py`, `process_tiers` in the manifest, SKILL step 3 paragraph, README sentence. Claude seat. Acceptance names the operator action that lists `regime` as a required check, after the dry run from `main` against a closed PR. Two tasks map to INV-1 as V2 and V2b map to INV-5.
180:- **V1b** INV-2 (after V1c): `scripts/pr-caps.sh`, the caps and invariant-id steps in `regime-check.sh`, tests, one SKILL sentence.
181:- **V2** INV-5 runner: `schemas/audit.json` (PR #314's, reordered), `scripts/audit-head.sh` with PR #314's hardening, `make audit-head`, `AGENTS.md` Audit section, tests, the SKILL's task-level audit bullet. Claude seat.
182:- **V2b** INV-5 gate: `scripts/require-crit-review.py` reads the JSON verdict and categories, requires the `AGMSG-AUDIT` record, locks orchestration and conformance at P0-P2 to waiver or reset, accepts an earlier audited head by tree equality, and requires the INV-3 `check=` line in the validation file; tests. Operator-routed gate source (delegable to a Claude seat with recorded opt-in).
183:- **A3** INV-6 (plan 006 Phase A, `dotfiles-T128-regime-counters-a01`): `scripts/regime-counters.sh` computes every INV-6 count from history and GitHub and prints the thresholds reached; `check-regime-boundary.sh` reports a reached threshold without a reset record or waiver; the orchestrator runs it before every acceptance action. V3a wires that script into the hook and the gate.
184:- **V3a** INV-6: `scripts/pr-feedback.py` (`original_commit_id` on review_comment items), `require-crit-review.py` reset backstop and `task_sha256` comparison, `agent-stop-gate.sh` history counts (revises, amendments, questions) as the early signal, the Codex Stop entry in the manifest and its rendered template, `scripts/regime-waive.sh` with its `permissions.ask` rule in the manifest's Claude permissions block (no permgate policy entry), `check-regime-boundary.sh` detector and waiver listing; tests. Four boundaries in one PR (gate source, Claude hook and permission source, Codex hook source): an operator PR by construction, reviewed by a Codex `security`-profile seat before acceptance.
185:- **V3b** INV-4: premises in the schema and validator, SKILL text (questions end the task; one answering TASK at most). Claude seat; no hook source (the counting is V3a's).
186:- **V3c** INV-3: `check=` and `previous_head=` in the ACCEPTANCE contract (SKILL), `revise.yaml` beside task.md in the Worker Playbook, the `regime-check.sh` step, the `revise-check` job in `test.yaml`; tests. Claude seat (no gate source: the history check and validation-file line are V2b's).
187:- **V3d** INV-10: idle and first-push computations in `check-regime-boundary.sh` and `accept-task.py` (the latter lands in V5b; V3d adds them to the boundary check only). Claude seat.
188:- **V4** INV-7: `scripts/design-review.sh` (Claude and Codex runs under their `-review-dot-hNNN` identities), `schemas/design-review.json`, the history anchor and hash check in the gate (two RESULTs, both forms), SKILL paragraph. Operator-routed for the gate part.
189:- **V5a** INV-8: `.orchestration/<task id>/` paths in the Worker Playbook, task.md copy as the first commit, evidence-shape validation in `regime.yml`, boundary commit reduced to orchestrator records. Claude seat.
190:- **V5b** INV-9: `scripts/accept-task.py`, cost fields with source digests, budgets in `process_tiers`, `check-regime-boundary.sh` budget warning. Claude seat. Size: the sweep, scaffold and gate invocation already exist as commands; the script sequences them, about 200 lines.
191:- **V6** INV-11: `executable_permgate` session_id and cwd; gate cross-check. Operator-routed, Codex `security` profile review.
192-
193-Order: V0, then each design-tier code wave as `<task>-contract-a01` (dormant contract tests) followed by its implementation: V1, V1c, V1b, V2, V2b, V3a, V3b, V3c, V3d, V4, V5a, V5b, V6. File-disjoint pairs may run concurrently (V1 with V2; V3b with V3d); the gate-source waves (V2b, V3a, V4's gate part) run serially.
194-
--
203-## 9. Residuals, stated
204-
205-- Workers' conduct is checked mechanically only for Claude seats and only after V6; until then the sandbox record is self-reported.
206:- `pull_request_target` runs with the base repository's token on a public repository: the `regime` job reads PR files as data with `contents: read` only, checks out `main`'s scripts, and never executes anything from the PR; a change to `.github/workflows/regime.yml` itself is a design-tier change under INV-1.
207-- A repository admin can edit the ruleset; that path is visible on GitHub, not prevented, consistent with the waiver anchor.
208-- Operator authentication does not exist on this machine: every seat runs as the one user and every GitHub action as the one account, so no record can prove that the operator rather than the orchestrator wrote it. The regime therefore makes every waiver pass through a native permission prompt (`permissions.ask`, which no classifier, hook or agent may answer) and makes every waiver visible in three places; it does not claim more. The Codex design review of round 7 asked for authenticated operator events; this is the honest limit of what the machine offers.
209-- The design-review receipt's anchor in history is only as strong as the `-review-` identity's independence; a fresh headless context per review (V4) is the mitigation, and until V4 lands a seated `review`-profile identity reviews.
210-- GitHub's default Actions policy blocks `pull_request_target` on public repositories from 2026-11-02 (evaluate mode today); the operator sets an explicit event policy allowing it before then, or the `regime` job loses its main-pinned form and the host gate becomes the only gate again. Named in V1c's acceptance record.
211-- The `regime` job runs `main`'s workflow file, so a change to `regime.yml` is never exercised by its own PR; its logic therefore lives in scripts with unit tests, and a `workflow_dispatch` dry run precedes listing it as required.
212-- `regime.yml` discipline, stated once: `main` stays at the workspace root (`actions/checkout` default ref under `pull_request_target`); the PR head is fetched as data and read with `git show <head sha>:<path>` into a directory never on `PATH`; the diff range is the merge-base of `github.event.pull_request.head.sha` with `main`, never `github.sha`; `uv run --no-project`; `yaml.safe_load`; no `make`, no script, no dependency file from the PR tree; `permissions: contents: read`; no secrets.
213:- The seven existing required checks still run on `pull_request` from the PR's own workflow files; INV-1's workflow-edit refusal in the `regime` job is what closes R8 for them.
214-- Bootstrap: this design was written by the orchestrator that dispatched the abandoned tasks. The reset records carry the operator's waiver form (`DESIGN_RESET_WAIVED_BY=operator`, decision 2026-10-11), this review is the only release, and no further orchestrator-authored design follows under T128; T127 (T120's redesign) is written by another context.
215-
216-## 10. Design review (round 15 requested: plan 006 A102, second pair)
217-
218:Round 1 (`.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review.md`, `claude-review-dot-a001`, 2026-10-10T21:15Z, verdict `revise`): INV-7, INV-8, INV-11, INV-12 accepted with notes; INV-1, 2, 3, 4, 5, 6, 9, 10 rejected with corrections; findings F1-F9. v2 adopts every item: the task.md copy and `task_sha256` anchor (F1), the per-task invariant-set rule and the workflow-edit refusal (F2), the gate changes assigned to V2b/V3a/V4 with the category lock, the Bot-wait timeout and the tree-equality rule (F3), the merge backstop as the mandatory point, `original_commit_id`, the audit-JSON source, the Stop-hook budget split and the boundary detector (F4), the single amendment count over every TASK (F5), INV-9/INV-10 moved out of the Stop hook (F6), the reset records corrected to `claude-review-dot-a001` with the waiver form and the thread ids (F7), rule prose in the review tier (F8), premise 1 restated and three premises added (F9); plus the Q5 salvage list, the `make audit-head` target in place of a daemon, the `regime.yml` discipline and the hash note.
219-
220:Round 2 (`…-design-review-round2.md`, 21:29Z, verdict `revise`): every round-1 correction confirmed applied; INV-2, INV-3, INV-6 rejected for contradictions v2 introduced, plus routing, cap and premise notes. v3 adopts all of them: `implementing_tasks` is a map of task id to invariant ids inside the hashed keys and the design-on-main precondition is stated (INV-2); `revise.yaml` is a sibling of the byte-identical task.md (INV-3, INV-8, INV-12, V3c, V2b); the question threshold is 2 and audit JSONs count only when their sha256 matches their record (INV-6); V3a is an operator PR with all hook counting, V3b has no hook source, V3c no gate source; the legacy list is excluded from the line cap as data; the `workflow_dispatch` premise is added; the stage-3 sentence names the orchestrator's `make audit-head`; INV-1 names the latest TASK's token and the recommit after each amendment. Round 3 (`…-design-review-round3.md`, 21:33Z, verdict `accept`) confirmed the five edits; its two notes are carried in the acceptance record. v4 (operator direction 2026-10-11, relayed by the review seat's PONG at 22:01Z) splits V1 by responsibility into V1 (validation only) and V1c (the CI check), adds `dotfiles-T128-v1c-regime-ci-check-a01: [INV-1]` to `implementing_tasks` (a hashed key, hence this round), reorders the waves (V1, V1c, V1b, …) and aligns section 7's cap wording with INV-2. Round 4 (`…-design-review-round4.md`, 22:06Z, verdict `accept`) confirmed the split; its note (INV-1's ruleset action is V1c's acceptance record) is carried. v5 answers the Codex Bot's finding on boundary PR #316 (thread 4239305441): INV-3's `ci:<job>` form had no enforcement, so `check=` is now a test selector or a `repro:<id>` whose command and output live in revise.yaml, each with its own regime-job verification. Round 5 (`…-design-review-round5.md`, 22:12Z, verdict `accept`) confirmed it. The Codex Bot then reviewed the second boundary head (c1e2582b) and raised six P1 and four P2 findings that three same-vendor accepts had not: the auditor read the schema and AGENTS.md from the audited head (INV-5 now runs from main as the instruction root with the worktree as data), the CI job had no previous RESULT head (INV-3 now records previous_head in the ACCEPTANCE and revise.yaml, cross-checked by the host gate), ids were compared without sentences (INV-2), `allowed_files: ['*']` derived a cheap tier and a branch copy could claim a legacy id (INV-1, INV-12), and two task records pointed at an abandoned prerequisite. v6 adopts all ten and, because a cross-vendor reviewer found what a same-vendor fresh context did not, INV-7 now requires both a Claude and a Codex review of each design hash. Round 6 (`…-design-review-round6.md`, 22:28Z, verdict `revise`) accepted INV-1, 2, 3, 5, 12 and rejected INV-7: the Bot form produced no receipt, hash or RESULT, so it would have been an orchestrator-written receipt for a review it did not perform (R5). v7 makes the Codex review a `codex exec --sandbox read-only` run under a `codex-review` identity with its own receipt and RESULT, names it in the enforcement row and V4, keeps the Bot's review as swept feedback, and adds the bare-mode skills premise (round-6 INV-5 note, acted on in V2). Round 7 (Claude, 22:31Z, `accept`) confirmed INV-7. The first Codex review (`…-design-review-round7-codex.md`, `codex-review-dot-h001`, 22:34Z, `reject`) rejected INV-1, 3, 4, 5, 6, 9, 10, 12, all on one theme: evidence the orchestrator authors. v8 answers each: the waiver becomes a command under a `permissions.ask` rule (INV-1, INV-6) with the one-account residual stated in section 9; `repro:` is dropped and `check=` is a test selector only (INV-3); premises are reviewer and auditor evidence and the counting is the mechanical part (INV-4); the audit carries an input manifest and the acceptance record has an audit-input boundary (INV-5); cost records name their raw sources and stay a warning metric (INV-9); first push is the first commit's committer date and dispatchability is defined (INV-10); the independent oracle for gate-script PRs is the trusted-root audit (INV-12). The Codex P2 on the bare-mode skills premise is not adopted: the headless page says verbatim that "A directory you name with --add-dir is a partial exception: bare mode loads skills from its .claude/skills/ folder". Codex round 8 (`…-design-review-round8-codex.md`, 22:39Z, `reject`) accepted INV-1, 6, 7, 8, 9, 11 and the one-account residual, withdrew its bare-mode P2, and rejected INV-2 (tests unbounded), INV-3 (a changed file is not a run selector), INV-4 (sampling), INV-5 (the skills refusal was a premise, not a rule), INV-10 (committer date is not a push time; dependencies), INV-12 (a model audit is not a deterministic oracle), plus two stale enforcement rows. v9 adopts all: a 1000-line cap under tests/; the exact selector run on both heads in the PR's required `revise-check` job; every premise dispositioned by each reviewer and the auditor; the `.claude/**` refusal inside INV-5; the draft PR's `created_at` and an `after` list for dispatchability; a `main-tests` required job running main's tests against the PR's scripts (V5c); the two rows fixed. Claude round 8 (`…-design-review-round8.md`, 22:41Z, `revise`) rejected INV-1 (the waive script had no owner or row), INV-5 (once-per-head versus re-audit on a stale manifest) and INV-10 (fixed in v9), and offered a stronger anchor: the waiver record in a directory outside the sandbox write roots. Codex round 9 (`…-design-review-round9-codex.md`, 22:46Z, `reject`) accepted ten, rejected INV-5 (the `.claude/**` refusal that v9 claimed was silently lost by a failed edit, confirmed by grep) and INV-12 (the oracle must precede the waves), dispositioned all twelve premises (nine hold, three unverifiable in its read-only sandbox), and raised GitHub's 2026-11-02 `pull_request_target` policy. v10: the refusal is in INV-5 and verified by grep; one valid audit per head with stale-manifest replacement; the runner computes the manifest; the waiver record lives outside the sandbox write roots and V3a owns the script (map entry `[INV-6, INV-1]`); `main-tests` is wave V0 and every code wave is contract-first (INV-12, INV-2); the policy premise and residual. Claude round 9 (`…-design-review-round9.md`, 22:46Z, `revise`) found that `main-tests` as drafted would fail every intentional change and proposed running main's modules only for scripts outside `allowed_files`; Codex round 10 (`…-design-review-round10-codex.md`, 22:50Z, `reject`) accepted INV-1..11 and found that contract-first tests cannot merge ahead of an implementation that changes an existing script, proposing dormant contracts that `main-tests` activates on the implementation PR. v11's INV-12 is the union: main's modules as they are for undeclared scripts, main's dormant contracts (`REGIME_CONTRACT=1`) for declared ones, contract PRs required for design-tier waves; INV-1 states that the record's location is the guard and the ask rule the second layer (Claude round 9). Codex round 11 (`…-design-review-round11-codex.md`, 22:52Z) accepted INV-1..12 with no findings. Claude round 11 (`…-design-review-round11.md`, 22:54Z, `revise`) accepted everything but two INV-12 clauses: contracts must not stay dormant forever (the implementation PR removes the decorator; main-tests judges it against main's dormant copy) and an empty contract must fail a design-tier implementation PR. v12 adds both sentences to INV-12 and V0. Claude round 12 (`…-design-review-round12.md`, 22:57Z) accepted v12; Codex round 12 (`…-design-review-round12-codex.md`, 22:57Z, `revise`) accepted INV-1..11 and asked for a failing check behind the decorator-removal clause. v13 adds it to INV-12 (main-tests fails an implementation PR whose declared test module still carries a contract marker) and V0 carries it with the task-file reviewer's three V0 items (main's tests overlaid on a copy of the PR tree, module selection from the task's declared tests/ entries, task.md read with PyYAML). Round 13 (Claude 23:01Z, Codex 23:01Z and the premise map 23:17Z) accepted v13. Plan 006 (approved 2026-10-11) A102 amends two hashed keys: INV-12 states the in-process oracle's authenticated completion (nonce runner) and its residual, after the Codex Bot's P1 on V0's round-1 head repeated the class of the round-0 audit's finding 3; INV-2 and the map gain the .orchestration-only CI skip (`dotfiles-T128-ci-skip-orchestration-a01`, plan A201) that plan 006 orders as Phase 2. Round 14 (Codex 02:42Z `accept`; Claude 02:43Z `revise`): INV-12's residual clause understated the gap (the nonce authenticates the writer, not the counts; in-process patching of unittest's result collection forges counts with a genuine nonce) and INV-2 should cover every required check. v15 states the residual as it is, adds the runner's pinning of unittest classes, and words INV-2 for every required workflow. Round 15 asks both reviewers at once for one verdict each on this hash. Sources are the repository paths under `.orchestration/validation/dotfiles-T128-regime-v3-a01-research/` (`baseline.md`, `practice-evidence.md`, `claude-code-factsheet.md`, `codex-factsheet.md`, `github-factsheet.md`, `method-draft.md`). Receipt: `.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round15.md` (Claude) and `…-design-review-round15-codex.md` (Codex); the whole-file sha256 of this file in both headers.
FILE .orchestration/acceptance/dotfiles-T128-ci-skip-orchestration-a01-design-reset.md
---
format: 2
reset_of: dotfiles-T128-ci-skip-orchestration-a01
redesign_task: dotfiles-T128-ci-skip-orchestration-a02
design_sha256: 2c3a5ee2439a4c8e0aa16e0013e9b8acfcbb82fc330b259f7748f34938d5d9bc
redesign_source: dotfiles-T128-ci-skip-redesign-a01
redesign_seat: claude-review-dot-a001 (review profile, a context other than the task's author)
reason: "design INV-6 on PR 320: two RESULTs (456, 485: revises=1) and one amendment; the second audit (dc4e6c37) found the hand-written workflow reader's class a second time (spaced, escaped and flow-mapping keys after the first audit's quoted keys) and re-raised the design-on-main prerequisite (main at b896d9bc holds neither the task's implementing_tasks entry nor its INV-2 sentence); a further round reaches a threshold, so the rule's path is a reset with a redesign by another context"
---

# Design reset: dotfiles-T128-ci-skip-orchestration-a01 (PR #320), 2026-10-11

- **What stops:** task id a01's specification. The branch, PR #320, the worker `claude-standard-dot-a003` and the implementation (in-job fail-closed decision, no `needs`, no job-level `if`, `--no-renames`, the required-context constant) continue under `dotfiles-T128-ci-skip-orchestration-a02`.
- **Why a reset:** the reader finding recurred as a class (quoted keys, then spaced and escaped keys and flow mappings); fixing it form by form is the pattern the operator's rule forbids, and the specification said nothing about unsupported syntax. The design-on-main finding is the orchestrator's: the task was dispatched under plan 006 Phase 0's rule that a boundary is never a dispatch prerequisite, which contradicts INV-2's hashed sentence ("the design file must be on main (through a boundary PR) before the implementing TASK is dispatched"); the auditor is right. The remedy is mechanical: design v16 goes to `main` by the boundary PR `orchestration/boundary-2026-10-11-2` before this PR's final audit, and the plan's Phase 0 rule is corrected to INV-2's text (recorded in plan 006).
- **Redesign:** `dotfiles-T128-ci-skip-redesign-a01` on the review seat produces the whole a02 task file (fail-closed reader row with four mutation tests; the design-on-main row with the boundary PR in `after:`); the orchestrator writes it byte-identical from the receipt and the review seat confirms its hash (`verdict=accept design_sha256=<hash>`), the anchor.
- **Counts carried:** A5 at the reset: tasks 2, amendments 1, questions 0, results 2, revises 1, Bot P0/P1 heads after the first RESULT 0, wall 05:42Z to 07:13Z (1 h 31 min).
- **Waiver:** none.
- **Anchor:** redesign RESULT 496 (`claude-review-dot-a001`, 07:33:43Z, receipt `c55e1585…`, `a02_expected_sha256=2c3a5ee2…`, matched on disk); the review seat's `verdict=accept design_sha256=2c3a5ee2…` is the anchor (requested 07:36Z). `after:` stays `[]` (V1 types it as task ids); the boundary dependency is the design-on-main row. The successor ids need `implementing_tasks` entries (v16 maps the a01 ids only): design v17 adds `dotfiles-T128-ci-skip-orchestration-a02: [INV-2]` and `dotfiles-T128-regime-counters-a02: [INV-6]`, reviewed as a pair (round 18) and carried by the next boundary PR.
FILE .orchestration/acceptance/dotfiles-T128-regime-counters-a01-design-reset.md
---
format: 2
reset_of: dotfiles-T128-regime-counters-a01
redesign_task: dotfiles-T128-regime-counters-a02
design_sha256: afc46c3b7e7fb91bdc61196921e897327061f189da540b27408e66d122f1b8b7
redesign_source: dotfiles-T128-regime-counters-redesign-a01
redesign_seat: claude-review-dot-a001 (review profile, a context other than the task's author)
reason: "design INV-6 on PR 319: after amendment 1 the task has two RESULTs (revises=1) and one amendment, and the audit of 72764f05 found two P1s (status and verdict tokens matched anywhere in a message body; a reset record may name an unrelated, already accepted design) and one P2 (the fixtures put 1735 added lines under tests/ against INV-2's cap of 1000); any further round reaches a threshold, so the rule's path is a reset with a redesign by another context"
---

# Design reset: dotfiles-T128-regime-counters-a01 (PR #319), 2026-10-11

- **What stops:** task id a01's specification. The branch, PR #319, the worker `claude-standard-dot-a004` and the implementation continue under `dotfiles-T128-regime-counters-a02`, which carries the two missing threat rows (first-token reads of `status=`/`verdict=`; the redesign task's `reset_of` must name the task being reset) and the fixture budget, and is otherwise the a01 file at `d9a44b7e…`.
- **Why a reset:** two of the three audit findings are specification gaps of the orchestrator's (the anchor rule did not bind the redesign to the task; the fixture budget was not stated and the acceptance record's cap claim was wrong) and the third is an implementation defect the specification's wording ("counts follow INV-6's sentence") did not pin to first-token reads. The counts leave no second round under the rule.
- **Redesign:** `dotfiles-T128-regime-counters-redesign-a01` on the review seat produces the whole a02 task file; the orchestrator writes it byte-identical from the receipt's block and the review seat confirms its hash (`verdict=accept design_sha256=<hash>`), the anchor the boundary probe reads. The T128 design's own `reset_of` names the T124 waves, so the binding rule holds for the existing resets.
- **Counts carried:** A3 at the reset: tasks 2, amendments 1, questions 0, results 2, revises 1, Bot P0/P1 heads after the first RESULT 0, wall 2 h 23 min to the second RESULT.
- **Waiver:** none.
- **Anchor:** redesign RESULT 479 (`claude-review-dot-a001`, 06:58:42Z, receipt `b4864193…`, `a02_expected_sha256=0cfd6689…`); the file written from the block needed one mechanical fix (the twelfth row's `control:` value held a colon-space and PyYAML rejected the front matter; the orchestrator wrapped that one value in double quotes, nothing else), so the on-disk hash is `afc46c3b…`; the review seat's `verdict=accept design_sha256=afc46c3b…` on the on-disk file is the anchor (confirmed: RESULT 483, 07:01:02Z). Dispatched to `claude-standard-dot-a004` at 07:03Z.
FILE .orchestration/tasks/dotfiles-T128-ci-skip-orchestration-a02.md
---
format: 2
task_id: dotfiles-T128-ci-skip-orchestration-a02
kind: code
security: true
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round16.md
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
    disposition: "closed: the design that names this task id in implementing_tasks (dotfiles-T128-ci-skip-orchestration-a02: [INV-2] beside a01's entry; a hashed-key change with its pair of design reviews, the INV-2 sentence unchanged) lands on main through the boundary PR orchestration/boundary-2026-10-11-2 before this PR's final audit; this PR takes that main with gh pr update-branch and merges only from a head audited on it; test: none (the acceptance record pastes git show origin/main:.orchestration/tasks/dotfiles-T128-regime-v3-a01.md | sha256sum and the map line)"
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
FILE .orchestration/tasks/dotfiles-T128-regime-counters-a02.md
---
format: 2
task_id: dotfiles-T128-regime-counters-a02
kind: code
security: true
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round16.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - scripts/regime-counters.sh
  - scripts/check-regime-boundary.sh
  - tests/unit/test_regime_counters.py
  - tests/unit/test_check_regime_boundary.py
  - tests/fixtures/regime-counters/**
after: []
reset_of: [dotfiles-T128-regime-counters-a01]
invariants:
  INV-6: "the reset rule's mandatory point is the merge backstop in scripts/require-crit-review.py, with the orchestrator's Stop hook (Claude Stop hook, Codex [hooks].Stop) as the early signal, soft on both runtimes by their documented caps; counts come from history for the hook and the gate (revises = RESULTs for the task_id minus one, threshold 2; amendments = AGMSG-TASKs after the first, threshold 2; AGMSG-PONG status=question, threshold 2) and from GitHub and main-checkout files for the gate and the boundary check only (Codex Bot P0 or P1 on two heads after the first RESULT, from original_commit_id on review_comment items recorded by pr-feedback.py; an audit implementation or specification finding at P0-P1 on two heads, from .orchestration/validation/<task>-audit-<sha7>.json in the main checkout, each counted only when its sha256 matches its AGMSG-AUDIT record); when a count is reached the gate refuses the merge until a reset record names a redesign task whose design RESULT comes from an identity other than the task's author, or a waiver written by scripts/regime-waive.sh under the INV-1 ask-rule discipline into the state directory outside the sandbox write roots (the only release path besides a redesign; the one-account residual of INV-1 applies); check-regime-boundary.sh reports a closed-unmerged PR whose task has no reset record and a task over any count with neither an accepted acceptance record nor a reset record"
threat_table:
  - control: the orchestrator edits .orchestration files
    disposition: "closed: every count comes from agmsg history or GitHub only; .orchestration files select which task ids the boundary check reports and can never raise or lower a count; test: a forged acceptance record changes no count"
  - control: the orchestrator writes the acceptance, reset or waiver record that would silence a boundary report
    disposition: "closed: a record silences the report only through INV-6's anchor for it: an accepted acceptance record only when GitHub shows the task's PR merged (gh api pulls/<n>, merged_at non-null; the PR number comes from the record's pr= line); a reset record only when history holds an AGMSG-RESULT verdict=accept naming the redesign design hash the record names, sent by an identity other than the abandoned task's author (the TASK sender); a waiver only from the state directory outside the sandbox write roots that scripts/regime-waive.sh (V3a) writes, so before V3a no waiver silences anything and a DESIGN_RESET_WAIVED_BY= line is printed as regime-boundary: <id> waiver-unanchored (visible, not prevented: trust anchor 4); tests: a forged accepted record with an unmerged PR, a reset record whose hash has no foreign RESULT, and a waiver line in an acceptance record each leave the report in place"
  - control: a reset record names an unrelated, already accepted design and its genuine hash (the audit of 72764f05, P1)
    disposition: "closed: a reset record anchors only when the redesign task file it names carries a reset_of list that names the task being reset, and history holds the foreign verdict=accept on that file's hash; a record naming any other accepted design anchors nothing; test: a reset record naming an unrelated accepted design leaves the report in place"
  - control: the PR authors scripts/regime-counters.sh, its tests and its fixtures (R8)
    disposition: "residual: a PR-authored test cannot close its own author's undercount or a forged source= label; compensating controls: the design-tier audit of the final head from main as instruction root (INV-5 form, headless now), and the orchestrator's acceptance replay, which runs the branch's script live without any fixture flag on dotfiles-T119-rolling-release-assets-a01 and on dotfiles-T128-v0-main-tests-a01 --pr 317 and compares the output with the figures INV-6's sentence gives for this task's premises (T119: 10 TASKs, 9 amendments because the ninth TASK after the first carries no amendment= token, 8 questions; PR 317: the first RESULT head is adcf783b, 01:42Z, and six P0/P1 heads follow it) in the acceptance record; main-tests' undeclared-change guard applies after V0 lands; dormant contracts are withdrawn by plan 006"
  - control: history.sh truncates to 20 rows by default
    disposition: "closed: the script reads the whole team history through lib/storage.sh's storage_history, as scripts/agent-stop-gate.sh read_history does; test: a 600-row fixture counts fully"
  - control: a worker sends extra RESULTs or PONGs
    disposition: "closed: revises = RESULTs for the task_id minus one, exactly INV-6's sentence (the message contract has no withdrawn or superseded status; an ACCEPTANCE status=parked changes no count), every counted message id printed; questions = PONG status=question; a status or a verdict is read from the first status= or verdict= token of the body, the way tok() reads task_id, never from free text (the audit of 72764f05, P1: has() anywhere in the body); tests per status the contract has (ready_for_review, blocked), plus a PONG status=blocked whose note mentions status=question that counts no question and a RESULT verdict=revise whose note mentions verdict=accept that anchors no reset"
  - control: the Bot head count depends on live GitHub state
    disposition: "closed: review_comment items carrying a P0 or P1 badge, grouped by original_commit_id (the field pr-feedback.py records, read live with gh api because the feedback JSON exists only at acceptance), counted only for heads after the first RESULT's head= taken from history; a gh failure, a first RESULT without a head= token, or review_comment items without original_commit_id print unknown, never 0; test with a recorded API fixture and one negative case each"
  - control: a task without a pull request (review, design and redesign tasks) can never anchor an accepted record on a merge, so the probe would report it forever and the report would become noise
    disposition: "closed: an accepted acceptance record silences a PR-less task only when none of the task's RESULTs carries a pr= token and the record carries a pr=none line; a RESULT with pr= makes pr=none a forgery that silences nothing; every accepted record carries pr=<n> or pr=none (the orchestrator adds the line to existing records in the boundary commit); tests: a PR-less review task with pr=none is silenced, the same record on a task whose RESULT names a PR is not"
  - control: the test seams --history-file and --github-file could feed forged inputs
    disposition: "closed: the seams are flags, scripts/check-regime-boundary.sh never passes them, and every output line ends in source=live or source=fixture so a pasted output shows which was used; test asserts the marker"
  - control: audit findings per head
    disposition: "out-of-scope: V2 (INV-6 counts audit findings from .orchestration/validation/<task>-audit-<sha7>.json whose sha256 matches an AGMSG-AUDIT record; neither exists before V2); until then the script prints audits=unknown and the orchestrator counts audit classes by hand in the acceptance record"
  - control: the thresholds could be edited in the script
    disposition: "residual: the thresholds are INV-6's constants (revises 2, amendments 2, questions 2, Bot P0/P1 heads 2); changing them is a hashed design change under INV-7; compensating control: the design review, and V3a's gate reads the same constants"
  - control: "the PR's fixtures count against INV-2's 1000-line cap under tests/ (the audit of 72764f05, P2: 697 unit-test lines plus 1038 fixture lines on the a01 head)"
    disposition: "closed: tests/fixtures/regime-counters/* hold only the rows and fields the tests read (PR 313: the P0/P1 top-level comments and the commits; message TSVs cut to the task's rows), so git diff --numstat origin/main -- tests/ adds at most 1000 lines; test: none, the acceptance measures it from the pasted numstat"
premises:
  - claim: "the counts the plan needs are derivable from history (TASK, amendment=, PONG status=question, RESULT, ACCEPTANCE status=revise, timestamps) and GitHub (review_comment original_commit_id, P badge); T119 has 10 TASKs, 8 of them tagged amendment=, and INV-6 counts the nine after the first; the PR 313 figure is the Bot thread count, not INV-6's head count"
    command: "~/.agents/skills/agmsg/scripts/history.sh dotfiles-conformance --limit 1000 | grep -c 'AGMSG-TASK v1 task_id=dotfiles-T119-rolling-release-assets-a01'; gh api --paginate repos/mryfmo/dotfiles/pulls/313/comments --jq '[.[]|select(.in_reply_to_id==null)]|length'"
    output: |-
      10
      52
  - claim: "scripts/agent-stop-gate.sh already reads the whole team history through the storage facade; the counters reuse that read, not history.sh's 20-row default"
    command: "grep -n 'storage_history\\|read_history\\|lib/storage' scripts/agent-stop-gate.sh | head -6"
    output: |-
      51:# shortens each wait on a contended store. storage_history runs storage_init, which writes unless
      56:# SQLITE_BUSY; only a non-initializing storage_history upstream would close that.
      57:read_history() {
      60:    source "${scripts}/lib/storage.sh" && agmsg_storage_load || return 1
      65:    storage_history "$1" | jq -r '[.from, .to, .body] | @tsv'
      71:    read_history "$2"
  - claim: "PR 317's Bot-reviewed heads, one per fix round, are the V0 fixture's expected Bot heads; V0's first RESULT is the 01:42Z one at head adcf783b (the 02:19Z RESULT at 32fe9a36 is its second), so the six P0/P1 heads after adcf783b count under INV-6"
    command: "gh api --paginate repos/mryfmo/dotfiles/pulls/317/reviews --jq '.[]|select(.user.type==\"Bot\")|[.commit_id[0:8],.submitted_at]|@tsv'"
    output: |-
      32fe9a36	2026-10-11T02:37:13Z
      56ca6c69	2026-10-11T02:52:38Z
      de138f65	2026-10-11T03:03:00Z
      f6528bba	2026-10-11T03:10:28Z
      98f1d250	2026-10-11T03:24:14Z
      2602f575	2026-10-11T03:43:58Z
      e314c502	2026-10-11T04:04:13Z
---

# AGMSG-TASK dotfiles-T128-regime-counters-a02 — Phase A3, reset continuation: the counters S1 and S2 are decided from

Plan 006 Phase A. Written by the review seat as the reset redesign of `dotfiles-T128-regime-counters-a01` (`dotfiles-T128-regime-counters-redesign-a01`), under the reset record `.orchestration/acceptance/dotfiles-T128-regime-counters-a01-design-reset.md`. Same worker (`claude-standard-dot-a004`), same worktree (`.claude/worktrees/worker-c`), same branch and PR (`feat/regime-counters`, #319), continuing from head `72764f05`. Review tier by path, treated as design tier because its output decides stops: the threat table above is the completion condition, and a missing row is added once as an amendment, never fixed finding by finding. Implements the counting half of INV-6 (design wave A3); the hook and gate wiring stay in V3a.

## What to build

1. `scripts/regime-counters.sh <task id> [--team dotfiles-conformance] [--pr <n>] [--history-only] [--history-file <tsv>] [--github-file <json>]`. `--history-only` skips GitHub (prints `bot_p1_heads_after_result=skipped`) and returns within 3 seconds on the live store, for the Stop hook V3a wires it into (INV-6's budget); the gate and the boundary check always run the full form. Output, one line: `task=<id> tasks=<n> amendments=<n> questions=<n> results=<n> withdrawn=<n> revises=<n> first_result_head=<sha|none> bot_p1_heads_after_result=<n|unknown> audits=unknown wall=<first TASK ts>..<last RESULT ts> (<h:mm>) source=<live|fixture>`; then one line per threshold reached, `S2: revises <n> >= 2`, `S2: amendments <n> >= 2`, `S2: questions <n> >= 2`, `S2: bot_p1_heads <n> >= 2`; then `S1: candidate class=<first three words, lower-cased> count=<n>` for every Bot thread title class (the first line of a top-level review_comment, badge stripped) that appears three or more times on the PR. History comes from `lib/storage.sh` `storage_history` (the way `agent-stop-gate.sh` `read_history` sources it), GitHub from `gh api --paginate`, fixtures only through the two flags. Counts follow INV-6's sentence and nothing else: revises = RESULTs for the task_id minus one (no status is excluded; the contract has no withdrawn status); amendments = TASKs after the first; questions = `PONG status=question`; Bot heads = `original_commit_id` of P0/P1 review_comment items after the first RESULT's `head=`; `unknown` when the first RESULT has no `head=` or the items carry no `original_commit_id`. A status or a verdict is the first `status=` or `verdict=` token of the body, read the way `tok()` reads `task_id`; a token that appears later in free text counts nothing (`has()` over the whole body is gone). shdoc header; under 150 lines; `shellcheck` clean.
2. `scripts/check-regime-boundary.sh`: for every `.orchestration/tasks/<id>.md` whose id has a TASK in history, run the counters (live, never a fixture) and print `regime-boundary: <id> <S2 line>` when a threshold is reached, unless an anchored record silences it as the threat table states (merged PR named by the record's `pr=<n>` line for an accepted acceptance record; `pr=none` only for a task none of whose RESULTs names a PR; foreign design RESULT for a reset record, and only when the redesign task file the record names carries a `reset_of` list naming this task, so an unrelated accepted design anchors nothing; no waiver before V3a, a `DESIGN_RESET_WAIVED_BY=` line printed as `waiver-unanchored`). The probe skips, as the other probes skip on a missing tool, when `scripts/regime-counters.sh` is not beside the script or no agmsg store is readable, so `tests/unit/test_herdr_agents.py`'s scratch-worktree run (lines 2809-2815 copy the boundary script alone and run `--report`) stays green. Keep the existing probes untouched. `after: []`: A3 precedes V0; V0's Phase B re-specification takes A3's modules as given.
3. `tests/unit/test_regime_counters.py`, with fixtures under `tests/fixtures/regime-counters/` exported from the real store (`history.sh dotfiles-conformance --limit 2000` filtered by task id, as TSV) and from `gh api` (JSON): T118 (`dotfiles-T118-*`, the 20-revise task), T119 (`dotfiles-T119-rolling-release-assets-a01`: 10 TASKs, 8 amendments), T124 W1 (PR 313: Bot P1 heads), V0 (`dotfiles-T128-v0-main-tests-a01`, PR 317: the Bot P1 heads after the RESULT head 32fe9a36; premise 3 lists the Bot-reviewed heads). Expected values come from the fixture; where the fixture disagrees with `baseline.md`, the report says so and the test follows the fixture. One test per threat-table `closed` row (the anchor row needs its three negative cases), each failing when its rule is removed; the boundary probe (violation, the three silenced-record negatives, the skip) is tested in `tests/unit/test_check_regime_boundary.py`, the declared module of `scripts/check-regime-boundary.sh` (the existing boundary tests in `tests/unit/test_herdr_agents.py` stay untouched). The fixtures carry message bodies: run `uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets tests/fixtures/regime-counters/*` before committing them, and cut them to the rows and fields the tests read so `tests/` stays within INV-2's 1000 added lines (the a01 head carried 697 + 1038). Two tests join the module for the reset's rows: `test_a_status_in_free_text_counts_nothing` (a PONG `status=blocked` noting `status=question`; a RESULT `verdict=revise` noting `verdict=accept`) and, in `tests/unit/test_check_regime_boundary.py`, `test_a_reset_record_naming_an_unrelated_accepted_design_anchors_nothing`.

## History

a01's amendment 1 (06:05Z) added the PR-less anchor row (an accepted record silences a review, design or redesign task only with `pr=none` when no RESULT names a PR) and corrected the premises to the fixtures' figures (T119 amendments 9; V0 first RESULT head `adcf783b`, six heads after it). The audit of `72764f05` then found two P1s and one P2: `has()` matched `status=`/`verdict=` tokens anywhere in a body, a reset record could name an unrelated accepted design and its genuine hash, and the tests plus fixtures added 1735 lines under `tests/` against INV-2's 1000. With two RESULTs already (revises 1, amendments 1) any further round reaches INV-6's threshold, so this file is the reset redesign, written by the review seat: the two rows, the first-token rule, the `reset_of` binding and the fixture budget above, nothing else changed.

## Validation

`shellcheck scripts/regime-counters.sh scripts/check-regime-boundary.sh`; `make unit-test` (or the module runs the Makefile uses) with `tests/unit/test_regime_counters.py`, `tests/unit/test_check_regime_boundary.py` and `tests/unit/test_herdr_agents.py` green; `scripts/regime-counters.sh dotfiles-T128-v0-main-tests-a01 --pr 317` and `scripts/regime-counters.sh dotfiles-T119-rolling-release-assets-a01` pasted live; `make check-regime-boundary` pasted; `git diff --numstat origin/main -- tests/ | awk '{a+=$1} END {print a}'` pasted, at most 1000; `invariant: INV-6 → <file:line>` lines; every threat-table `closed` row names its test by `tests/unit/test_regime_counters.py::<name>`; the premises re-run and pasted.

## First commit

Copy this task file byte-identical to `.orchestration/dotfiles-T128-regime-counters-a02/task.md` (the `…-a01/` directory stays as history); evidence for this task beside it.

## Completion

The PR is open and ready; continue from `72764f05` with one content commit after the task copy; CI; Bot wait with at most two P0/P1 fix rounds (a third round is reported in the RESULT as `bot_rounds=3` with the open threads, not fixed); artifacts; `memory add`; `AGMSG-RESULT v1 task_id=dotfiles-T128-regime-counters-a02 … reset_of=dotfiles-T128-regime-counters-a01 bot_rounds=<n>` via `agmsg-dispatch dotfiles-conformance <you> claude-deep-dot w5:p1`. max_turns=8. Forbidden: `scripts/require-crit-review.py`, `scripts/agent-stop-gate.sh`, anything outside `allowed_files`; `make update`; resolving threads.

**Verifying removal hash and mappings**
exec
/bin/zsh -lc "sed '/"'^  dotfiles-T128-ci-skip-orchestration-a02: '"\\[INV-2\\]"'$/d; /''^  dotfiles-T128-regime-counters-a02: '"\\[INV-6\\]"'$/d'"' .orchestration/tasks/dotfiles-T128-regime-v3-a01.md | shasum -a 256
for f in .orchestration/tasks/dotfiles-T128-ci-skip-orchestration-a02.md .orchestration/tasks/dotfiles-T128-regime-counters-a02.md; do echo \"--- "'$f"; sed -n '"'1,42p' \""'$f"; done
for f in .orchestration/acceptance/dotfiles-T128-ci-skip-orchestration-a01-design-reset.md .orchestration/acceptance/dotfiles-T128-regime-counters-a01-design-reset.md; do echo "--- $f"; rg -n '"'"'^(task|reset|redesign|design|Decision|decision|sha|review|author|worker)|reset_of|INV-[26]|AGMSG-RESULT'"' \""'$f"; done
git diff --no-index -- /dev/null /dev/null >/dev/null; date -u +%Y-%m-%dT%H:%M:%SZ' in ~/Workspace/dotfiles
 succeeded in 80ms:
15957fbc6b47ff8f2424072ca5b5849911b7be90582e1d850f5d315563494cd4  -
--- .orchestration/tasks/dotfiles-T128-ci-skip-orchestration-a02.md
---
format: 2
task_id: dotfiles-T128-ci-skip-orchestration-a02
kind: code
security: true
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round16.md
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
    disposition: "closed: the design that names this task id in implementing_tasks (dotfiles-T128-ci-skip-orchestration-a02: [INV-2] beside a01's entry; a hashed-key change with its pair of design reviews, the INV-2 sentence unchanged) lands on main through the boundary PR orchestration/boundary-2026-10-11-2 before this PR's final audit; this PR takes that main with gh pr update-branch and merges only from a head audited on it; test: none (the acceptance record pastes git show origin/main:.orchestration/tasks/dotfiles-T128-regime-v3-a01.md | sha256sum and the map line)"
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
--- .orchestration/tasks/dotfiles-T128-regime-counters-a02.md
---
format: 2
task_id: dotfiles-T128-regime-counters-a02
kind: code
security: true
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round16.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - scripts/regime-counters.sh
  - scripts/check-regime-boundary.sh
  - tests/unit/test_regime_counters.py
  - tests/unit/test_check_regime_boundary.py
  - tests/fixtures/regime-counters/**
after: []
reset_of: [dotfiles-T128-regime-counters-a01]
invariants:
  INV-6: "the reset rule's mandatory point is the merge backstop in scripts/require-crit-review.py, with the orchestrator's Stop hook (Claude Stop hook, Codex [hooks].Stop) as the early signal, soft on both runtimes by their documented caps; counts come from history for the hook and the gate (revises = RESULTs for the task_id minus one, threshold 2; amendments = AGMSG-TASKs after the first, threshold 2; AGMSG-PONG status=question, threshold 2) and from GitHub and main-checkout files for the gate and the boundary check only (Codex Bot P0 or P1 on two heads after the first RESULT, from original_commit_id on review_comment items recorded by pr-feedback.py; an audit implementation or specification finding at P0-P1 on two heads, from .orchestration/validation/<task>-audit-<sha7>.json in the main checkout, each counted only when its sha256 matches its AGMSG-AUDIT record); when a count is reached the gate refuses the merge until a reset record names a redesign task whose design RESULT comes from an identity other than the task's author, or a waiver written by scripts/regime-waive.sh under the INV-1 ask-rule discipline into the state directory outside the sandbox write roots (the only release path besides a redesign; the one-account residual of INV-1 applies); check-regime-boundary.sh reports a closed-unmerged PR whose task has no reset record and a task over any count with neither an accepted acceptance record nor a reset record"
threat_table:
  - control: the orchestrator edits .orchestration files
    disposition: "closed: every count comes from agmsg history or GitHub only; .orchestration files select which task ids the boundary check reports and can never raise or lower a count; test: a forged acceptance record changes no count"
  - control: the orchestrator writes the acceptance, reset or waiver record that would silence a boundary report
    disposition: "closed: a record silences the report only through INV-6's anchor for it: an accepted acceptance record only when GitHub shows the task's PR merged (gh api pulls/<n>, merged_at non-null; the PR number comes from the record's pr= line); a reset record only when history holds an AGMSG-RESULT verdict=accept naming the redesign design hash the record names, sent by an identity other than the abandoned task's author (the TASK sender); a waiver only from the state directory outside the sandbox write roots that scripts/regime-waive.sh (V3a) writes, so before V3a no waiver silences anything and a DESIGN_RESET_WAIVED_BY= line is printed as regime-boundary: <id> waiver-unanchored (visible, not prevented: trust anchor 4); tests: a forged accepted record with an unmerged PR, a reset record whose hash has no foreign RESULT, and a waiver line in an acceptance record each leave the report in place"
  - control: a reset record names an unrelated, already accepted design and its genuine hash (the audit of 72764f05, P1)
    disposition: "closed: a reset record anchors only when the redesign task file it names carries a reset_of list that names the task being reset, and history holds the foreign verdict=accept on that file's hash; a record naming any other accepted design anchors nothing; test: a reset record naming an unrelated accepted design leaves the report in place"
  - control: the PR authors scripts/regime-counters.sh, its tests and its fixtures (R8)
    disposition: "residual: a PR-authored test cannot close its own author's undercount or a forged source= label; compensating controls: the design-tier audit of the final head from main as instruction root (INV-5 form, headless now), and the orchestrator's acceptance replay, which runs the branch's script live without any fixture flag on dotfiles-T119-rolling-release-assets-a01 and on dotfiles-T128-v0-main-tests-a01 --pr 317 and compares the output with the figures INV-6's sentence gives for this task's premises (T119: 10 TASKs, 9 amendments because the ninth TASK after the first carries no amendment= token, 8 questions; PR 317: the first RESULT head is adcf783b, 01:42Z, and six P0/P1 heads follow it) in the acceptance record; main-tests' undeclared-change guard applies after V0 lands; dormant contracts are withdrawn by plan 006"
  - control: history.sh truncates to 20 rows by default
    disposition: "closed: the script reads the whole team history through lib/storage.sh's storage_history, as scripts/agent-stop-gate.sh read_history does; test: a 600-row fixture counts fully"
  - control: a worker sends extra RESULTs or PONGs
    disposition: "closed: revises = RESULTs for the task_id minus one, exactly INV-6's sentence (the message contract has no withdrawn or superseded status; an ACCEPTANCE status=parked changes no count), every counted message id printed; questions = PONG status=question; a status or a verdict is read from the first status= or verdict= token of the body, the way tok() reads task_id, never from free text (the audit of 72764f05, P1: has() anywhere in the body); tests per status the contract has (ready_for_review, blocked), plus a PONG status=blocked whose note mentions status=question that counts no question and a RESULT verdict=revise whose note mentions verdict=accept that anchors no reset"
  - control: the Bot head count depends on live GitHub state
    disposition: "closed: review_comment items carrying a P0 or P1 badge, grouped by original_commit_id (the field pr-feedback.py records, read live with gh api because the feedback JSON exists only at acceptance), counted only for heads after the first RESULT's head= taken from history; a gh failure, a first RESULT without a head= token, or review_comment items without original_commit_id print unknown, never 0; test with a recorded API fixture and one negative case each"
  - control: a task without a pull request (review, design and redesign tasks) can never anchor an accepted record on a merge, so the probe would report it forever and the report would become noise
    disposition: "closed: an accepted acceptance record silences a PR-less task only when none of the task's RESULTs carries a pr= token and the record carries a pr=none line; a RESULT with pr= makes pr=none a forgery that silences nothing; every accepted record carries pr=<n> or pr=none (the orchestrator adds the line to existing records in the boundary commit); tests: a PR-less review task with pr=none is silenced, the same record on a task whose RESULT names a PR is not"
  - control: the test seams --history-file and --github-file could feed forged inputs
    disposition: "closed: the seams are flags, scripts/check-regime-boundary.sh never passes them, and every output line ends in source=live or source=fixture so a pasted output shows which was used; test asserts the marker"
  - control: audit findings per head
    disposition: "out-of-scope: V2 (INV-6 counts audit findings from .orchestration/validation/<task>-audit-<sha7>.json whose sha256 matches an AGMSG-AUDIT record; neither exists before V2); until then the script prints audits=unknown and the orchestrator counts audit classes by hand in the acceptance record"
  - control: the thresholds could be edited in the script
    disposition: "residual: the thresholds are INV-6's constants (revises 2, amendments 2, questions 2, Bot P0/P1 heads 2); changing them is a hashed design change under INV-7; compensating control: the design review, and V3a's gate reads the same constants"
  - control: "the PR's fixtures count against INV-2's 1000-line cap under tests/ (the audit of 72764f05, P2: 697 unit-test lines plus 1038 fixture lines on the a01 head)"
--- .orchestration/acceptance/dotfiles-T128-ci-skip-orchestration-a01-design-reset.md
3:reset_of: dotfiles-T128-ci-skip-orchestration-a01
4:redesign_task: dotfiles-T128-ci-skip-orchestration-a02
5:design_sha256: 2c3a5ee2439a4c8e0aa16e0013e9b8acfcbb82fc330b259f7748f34938d5d9bc
6:redesign_source: dotfiles-T128-ci-skip-redesign-a01
7:redesign_seat: claude-review-dot-a001 (review profile, a context other than the task's author)
8:reason: "design INV-6 on PR 320: two RESULTs (456, 485: revises=1) and one amendment; the second audit (dc4e6c37) found the hand-written workflow reader's class a second time (spaced, escaped and flow-mapping keys after the first audit's quoted keys) and re-raised the design-on-main prerequisite (main at b896d9bc holds neither the task's implementing_tasks entry nor its INV-2 sentence); a further round reaches a threshold, so the rule's path is a reset with a redesign by another context"
14:- **Why a reset:** the reader finding recurred as a class (quoted keys, then spaced and escaped keys and flow mappings); fixing it form by form is the pattern the operator's rule forbids, and the specification said nothing about unsupported syntax. The design-on-main finding is the orchestrator's: the task was dispatched under plan 006 Phase 0's rule that a boundary is never a dispatch prerequisite, which contradicts INV-2's hashed sentence ("the design file must be on main (through a boundary PR) before the implementing TASK is dispatched"); the auditor is right. The remedy is mechanical: design v16 goes to `main` by the boundary PR `orchestration/boundary-2026-10-11-2` before this PR's final audit, and the plan's Phase 0 rule is corrected to INV-2's text (recorded in plan 006).
18:- **Anchor:** redesign RESULT 496 (`claude-review-dot-a001`, 07:33:43Z, receipt `c55e1585…`, `a02_expected_sha256=2c3a5ee2…`, matched on disk); the review seat's `verdict=accept design_sha256=2c3a5ee2…` is the anchor (requested 07:36Z). `after:` stays `[]` (V1 types it as task ids); the boundary dependency is the design-on-main row. The successor ids need `implementing_tasks` entries (v16 maps the a01 ids only): design v17 adds `dotfiles-T128-ci-skip-orchestration-a02: [INV-2]` and `dotfiles-T128-regime-counters-a02: [INV-6]`, reviewed as a pair (round 18) and carried by the next boundary PR.
--- .orchestration/acceptance/dotfiles-T128-regime-counters-a01-design-reset.md
3:reset_of: dotfiles-T128-regime-counters-a01
4:redesign_task: dotfiles-T128-regime-counters-a02
5:design_sha256: afc46c3b7e7fb91bdc61196921e897327061f189da540b27408e66d122f1b8b7
6:redesign_source: dotfiles-T128-regime-counters-redesign-a01
7:redesign_seat: claude-review-dot-a001 (review profile, a context other than the task's author)
8:reason: "design INV-6 on PR 319: after amendment 1 the task has two RESULTs (revises=1) and one amendment, and the audit of 72764f05 found two P1s (status and verdict tokens matched anywhere in a message body; a reset record may name an unrelated, already accepted design) and one P2 (the fixtures put 1735 added lines under tests/ against INV-2's cap of 1000); any further round reaches a threshold, so the rule's path is a reset with a redesign by another context"
13:- **What stops:** task id a01's specification. The branch, PR #319, the worker `claude-standard-dot-a004` and the implementation continue under `dotfiles-T128-regime-counters-a02`, which carries the two missing threat rows (first-token reads of `status=`/`verdict=`; the redesign task's `reset_of` must name the task being reset) and the fixture budget, and is otherwise the a01 file at `d9a44b7e…`.
14:- **Why a reset:** two of the three audit findings are specification gaps of the orchestrator's (the anchor rule did not bind the redesign to the task; the fixture budget was not stated and the acceptance record's cap claim was wrong) and the third is an implementation defect the specification's wording ("counts follow INV-6's sentence") did not pin to first-token reads. The counts leave no second round under the rule.
15:- **Redesign:** `dotfiles-T128-regime-counters-redesign-a01` on the review seat produces the whole a02 task file; the orchestrator writes it byte-identical from the receipt's block and the review seat confirms its hash (`verdict=accept design_sha256=<hash>`), the anchor the boundary probe reads. The T128 design's own `reset_of` names the T124 waves, so the binding rule holds for the existing resets.
2026-10-11T07:35:58Z

**Ensuring exact final output**
**Respecting exact format constraints**
codex
reviewed_at: 2026-10-11T07:35:58Z  
reviewer: codex-review-dot-h001 (headless)  
profile: review  
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@1d5f4c07e8a23d0bc5185931fe1037c16b76ae48441b62ffb05bd3ffde2ac0a5  
round: 18  
previous: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round17-codex.md

INV-1: accepted

INV-2: accepted

INV-3: accepted

INV-4: accepted

INV-5: accepted

INV-6: accepted

INV-7: accepted

INV-8: accepted

INV-9: accepted

INV-10: accepted

INV-11: accepted

INV-12: accepted

## Findings

The two entries name exactly the invariant sets carried by their reset successors: `dotfiles-T128-ci-skip-orchestration-a02` carries only INV-2, and `dotfiles-T128-regime-counters-a02` carries only INV-6.

The per-task entries are necessary under INV-2’s current lookup: reset successors retain distinct task ids, while only `-contract-a01` ids are remapped. No additional hashed-key change is needed. INV-6’s `reset_of` binding authenticates the reset relationship; it does not provide implementing-task map inheritance. Adding a general successor-to-predecessor mapping rule would be a separate semantic change, not required for these two successors.

Removing exactly these two lines reproduces whole-file sha256 `15957fbc6b47ff8f2424072ca5b5849911b7be90582e1d850f5d315563494cd4`. Therefore INV-1 through INV-12, the premises, and all other hashed content are unchanged from round 17.

## Residual

The round-17 residual remains unchanged: the PR-authored counter implementation, tests, fixtures, and `source=` label depend on the trusted-root audit and live acceptance replay until V0’s main-tests protection lands. V3a remains responsible for the mandatory merge backstop and protected waiver path. Implementation and tests were not executed; no files were modified.

Design verdict: accept
hook: Stop
hook: Stop Completed
tokens used
40,787
reviewed_at: 2026-10-11T07:35:58Z  
reviewer: codex-review-dot-h001 (headless)  
profile: review  
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@1d5f4c07e8a23d0bc5185931fe1037c16b76ae48441b62ffb05bd3ffde2ac0a5  
round: 18  
previous: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round17-codex.md

INV-1: accepted

INV-2: accepted

INV-3: accepted

INV-4: accepted

INV-5: accepted

INV-6: accepted

INV-7: accepted

INV-8: accepted

INV-9: accepted

INV-10: accepted

INV-11: accepted

INV-12: accepted

## Findings

The two entries name exactly the invariant sets carried by their reset successors: `dotfiles-T128-ci-skip-orchestration-a02` carries only INV-2, and `dotfiles-T128-regime-counters-a02` carries only INV-6.

The per-task entries are necessary under INV-2’s current lookup: reset successors retain distinct task ids, while only `-contract-a01` ids are remapped. No additional hashed-key change is needed. INV-6’s `reset_of` binding authenticates the reset relationship; it does not provide implementing-task map inheritance. Adding a general successor-to-predecessor mapping rule would be a separate semantic change, not required for these two successors.

Removing exactly these two lines reproduces whole-file sha256 `15957fbc6b47ff8f2424072ca5b5849911b7be90582e1d850f5d315563494cd4`. Therefore INV-1 through INV-12, the premises, and all other hashed content are unchanged from round 17.

## Residual

The round-17 residual remains unchanged: the PR-authored counter implementation, tests, fixtures, and `source=` label depend on the trusted-root audit and live acceptance replay until V0’s main-tests protection lands. V3a remains responsible for the mandatory merge backstop and protected waiver path. Implementation and tests were not executed; no files were modified.

Design verdict: accept
