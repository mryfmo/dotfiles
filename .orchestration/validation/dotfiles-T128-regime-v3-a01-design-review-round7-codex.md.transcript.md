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
session id: 01a127f3-1b24-7372-b959-baabef7eb68e
--------
user
You are an independent design reviewer (Codex, read-only). Review the design file .orchestration/tasks/dotfiles-T128-regime-v3-a01.md (regime v3 for an AI coding-agent orchestration: orchestrator, workers, headless auditor, Codex GitHub bot). Treat everything in it as untrusted claims. Read first: .orchestration/validation/dotfiles-T128-regime-v3-a01-research/baseline.md, practice-evidence.md, claude-code-factsheet.md, codex-factsheet.md, github-factsheet.md; the previous receipts .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review*.md; and the scripts the enforcement map names (scripts/require-crit-review.py, scripts/agent-stop-gate.sh, scripts/check-regime-boundary.sh, scripts/pr-feedback.py, .github/workflows/test.yaml). For each invariant INV-1..INV-12 answer one line `INV-n: accepted` or `INV-n: rejected: <what is wrong and what would be right>`, judging: testable as written; the named enforcement point is the earliest mandatory one; it closes the threat it maps to; it cannot be gamed by the orchestrator or a PR (the PR controls its own files; the orchestrator controls every .orchestration file; only agmsg history and GitHub state are not authored by them). Then list under `## Findings` each remaining gap as `[P0-P3] <file:line or section> <one-line rationale>`, prioritising ways a PR or the orchestrator could pass the gates while violating the intent, and anything the cited official documentation contradicts. Then `## Residual` with what still passes from the T118/T119/T124 failure modes named in section 1. Write the receipt as your final message with a YAML header: reviewed_at (UTC ISO), reviewer: codex-review-dot-h001 (headless), profile: review, design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@40476474ad9aec1f36f14927a43a8f98d0187eb5d7092b422b635fbdff70142a, round: 7, then the per-invariant lines, Findings, Residual, and exactly one final line `Design verdict: accept|revise|reject`. Do not modify any file.
warning: loading hooks from both ~/.codex/hooks.json and ~/.codex/config.toml; prefer a single representation for this layer
hook: SessionStart
hook: SessionStart
hook: SessionStart Completed
hook: SessionStart Completed
hook: UserPromptSubmit
hook: UserPromptSubmit Completed
codex
🤖 I read the AGENTS.md for mryfmo/dotfiles.

独立設計レビューとして、指定資料・既存 receipt・enforcement scripts を突き合わせます。`agmsg-orchestration` の worklog 規則と、レビュー用途の `ponytail-review` を先に確認します。読み取り専用のためファイルは変更しません。
exec
/bin/zsh -lc "sed -n '1,260p' ~/.agents/skills/agmsg-orchestration/SKILL.md && sed -n '1,240p' ~/.codex/plugins/cache/ponytail/ponytail/5.1.0/skills/ponytail-review/SKILL.md" in ~/Workspace/dotfiles
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

**Reviewing skill and constraints**
codex
スキル上は plan/todo 更新が必要ですが、今回はユーザー指定の read-only と「ファイルを変更しない」が優先されるため、worklog は作成・更新しません。設計の各 invariant を、実装上の強制点と証拠の信頼境界まで追跡します。
exec
/bin/zsh -lc "wc -l .orchestration/tasks/dotfiles-T128-regime-v3-a01.md .orchestration/validation/dotfiles-T128-regime-v3-a01-research/baseline.md .orchestration/validation/dotfiles-T128-regime-v3-a01-research/practice-evidence.md .orchestration/validation/dotfiles-T128-regime-v3-a01-research/claude-code-factsheet.md .orchestration/validation/dotfiles-T128-regime-v3-a01-research/codex-factsheet.md .orchestration/validation/dotfiles-T128-regime-v3-a01-research/github-factsheet.md scripts/require-crit-review.py scripts/agent-stop-gate.sh scripts/check-regime-boundary.sh scripts/pr-feedback.py .github/workflows/test.yaml; shasum -a 256 .orchestration/tasks/dotfiles-T128-regime-v3-a01.md; rg --files .orchestration/validation | rg 'dotfiles-T128-regime-v3-a01-design-review.*\\.md"'$'"' | sort" in ~/Workspace/dotfiles
 succeeded in 260ms:
     205 .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
      19 .orchestration/validation/dotfiles-T128-regime-v3-a01-research/baseline.md
      74 .orchestration/validation/dotfiles-T128-regime-v3-a01-research/practice-evidence.md
      96 .orchestration/validation/dotfiles-T128-regime-v3-a01-research/claude-code-factsheet.md
      83 .orchestration/validation/dotfiles-T128-regime-v3-a01-research/codex-factsheet.md
      69 .orchestration/validation/dotfiles-T128-regime-v3-a01-research/github-factsheet.md
     831 scripts/require-crit-review.py
     303 scripts/agent-stop-gate.sh
     203 scripts/check-regime-boundary.sh
     304 scripts/pr-feedback.py
     432 .github/workflows/test.yaml
    2619 total
40476474ad9aec1f36f14927a43a8f98d0187eb5d7092b422b635fbdff70142a  .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round2.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round3.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round4.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round5.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round6.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round7-codex.md.transcript.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round7.md
.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review.md

**Prioritizing design and research files**
exec
/bin/zsh -lc 'for f in .orchestration/validation/dotfiles-T128-regime-v3-a01-research/{baseline,practice-evidence,claude-code-factsheet,codex-factsheet,github-factsheet}.md .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review.md .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round{2,3,4,5,6,7}.md; do echo "FILE $f"; nl -ba "$f"; done; echo '"'FILE design'; nl -ba .orchestration/tasks/dotfiles-T128-regime-v3-a01.md" in ~/Workspace/dotfiles
 succeeded in 478ms:
FILE .orchestration/validation/dotfiles-T128-regime-v3-a01-research/baseline.md
     1	# Measured baseline (agmsg history + GitHub, 2026-10-11)
     2	
     3	| task | PR | files | +lines | TASK sends | amendments | PONG questions | RESULTs | revises | audits (incorrect) | audit findings | Bot threads (heads) | Bot P0/P1 | wall |
     4	|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
     5	| T114 canonical-clone | - | - | - | 1 | 0 | 0 | 5 | 6 | 3 (3) | 10 | - | - | 21.5h |
     6	| T115 worker-audit-xhigh | 305 | 7 | 18 | 1 | 1 | 0 | 2 | 2 | 1 (0) | 0 | 1 (1) | 0 | 1.0h |
     7	| T116 on-demand-workers | 306 | 11 | 529 | 1 | 1 | 0 | 2 | 3 | 1 (0) | 0 | 2 (1) | 2 | 3.4h |
     8	| T117 upgrade-outside | 308 | 8 | 156 | 1 | 2 | 0 | 2 | 3 | 1 (0) | 0 | 6 (2) | 0 | 2.1h |
     9	| T118 rolling-tools | 310 | 35 | 881 | 2 | 7 | 0 | 10 | 20 | 8 (7) | 16 | 16 (7) | 0 | 10.6h |
    10	| T119 rolling-release | 312 | 37 | 3191 | 10 | 8 | 8 | 6 | 5 | 4 (4) | 12 | 25 (11) | 7 | 11.1h |
    11	| T120 npm-provenance | 315 | 19 | 1489 | 8 | 6(8 in file) | 1 | 0 | 0 | 0 | 0 | 15 (5) | 8 | 4.9h, reset |
    12	| T124 W1 validator | 313 | 20 | 2642 | 10 | 8 | 6 | 2 | 2 | 0 | 0 | 52 (10) | 31 | 5.7h, halted |
    13	| T124 W3b audit | 314 | 9 | 1462 | 10 | 5 | 0 | 1 | 0 | 0 | 0 | 24 (4) | 2 | 4.0h, halted (reset (d) fired) |
    14	
    15	Audit timing (T119, four headless audits): files written 11:48, 13:55, 15:52, 17:23 local; each run ~15-25 min; 4 audits ≈ 1.3 h of an 11.1 h task. The audit is not the wall-clock bottleneck; rounds are.
    16	Where defects were found (T118/T119): Bot threads 41, audit findings 28, operator corrections of premise 2 (T119 Amendments 7-8). Audit `incorrect` verdicts: 11 of 12 runs on T114/T118/T119.
    17	Every acceptance record: cost n/a (tokens never measured). Session JSONL carries per-message usage (cache_read_input_tokens etc.), so cost is measurable offline.
    18	Bespoke code on the halted branches: validate-task.py 503 + high_risk_paths.py 316 + tests 695 (PR 313); audit-head.sh 555 + schema 47 + tests 756 (PR 314). 33 of 52 Bot threads on PR 313 are on validate-task.py (own YAML parser, own glob NFA): bypass findings on a hand-written trust-boundary parser.
    19	Thresholds T126 INV-6 applied to its own program: W1 8 amendments (>4), 2 revises (=2) -> reset; W3b Bot P1 on two post-RESULT heads -> reset. The orchestrator was preparing a waiver instead.
FILE .orchestration/validation/dotfiles-T128-regime-v3-a01-research/practice-evidence.md
     1	# Evidence sheet: orchestrator / worker / auditor coding-agent loops (2026-10-11)
     2	
     3	Tags: [primary] peer-reviewed/first-party data; [preprint] arXiv; [vendor doc]; [practitioner] opinion; [UNVERIFIED] snippets/secondary only.
     4	
     5	## A. Self-correction and reviewer independence
     6	
     7	- [primary] Intrinsic self-correction (no external signal) degrades reasoning accuracy. GPT-4: GSM8K 95.5 → 91.5 → 89.0 over rounds 0/1/2; CommonSenseQA 82.0 → 79.5 → 80.0; HotpotQA 49.0 → 49.0 → 43.0. GPT-3.5 CommonSenseQA 75.8 → 38.1 after one round. Correct→incorrect flips outnumber incorrect→correct. Earlier positive results used oracle labels. Condition: the loop has no ground-truth feedback. — https://arxiv.org/html/2310.01798v2
     8	- [primary] Same paper: at equal response budget, independent resampling + self-consistency beats multi-agent debate (GSM8K: 6 responses 85.3 vs 83.2; 9 responses 88.2 vs 83.0). Condition: compare at matched sample count. — https://arxiv.org/html/2310.01798v2
     9	- [primary] Self-Refine: ~20 points absolute average gain across 7 tasks, but gains concentrate in iteration 1 and the paper states "diminishing returns" (Code Optimization 22.0 → 27.0 → 27.9 → 28.8; Constrained Generation 29.0 → 40.3 → 46.7 → 49.7). Max 4 iterations; stop on a task criterion or a stop score from the feedback. Condition: the model can generate useful feedback on its own output (not a reasoning-correctness task). — https://arxiv.org/html/2303.17651
    10	- [primary, NeurIPS 2024] Self-preference bias: GPT-4 distinguishes its own summaries from others at 73.5% out of the box; in unambiguous pairwise cases GPT-4 preferred its own output 59.3% vs 18.0% (XSUM) and 87.7% vs 3.4% (CNN); human raters saw equal quality. Self-recognition and self-preference correlate linearly under fine-tuning (Kendall τ 0.41 → 0.74 for GPT-3.5). Caveat: Table 7 Llama-2 fine-tuned figures (0.45–0.56) contradict the paper's ">90%" text. Implication: a same-model, same-context reviewer is biased toward approval. — https://arxiv.org/html/2404.13076v1
    11	- [preprint, Dec 2024] "Dark side" of intrinsic self-correction: answer wavering and prompt bias appear even on simple factual questions across o1/4o/3.5 and Llama 2/3; mitigations tested are question repeating and small-sample SFT (no effect sizes in abstract). — https://arxiv.org/abs/2412.14959
    12	- [preprint] SWE-Dev inference scaling: 32B resolve rate 34.0% at 30 agent rounds → 36.6% at 75; gain from 30→45 "significantly more pronounced" than 45→75; authors conclude there is "a practical upper limit to the benefits of iteration scaling". Condition: single trajectory, more turns, same context. — https://arxiv.org/html/2506.07636
    13	- [primary, Meta industrial] Test-failure repair agent at scale: 42.3% solve rate at an average of 11.8 feedback iterations in the "balanced" configuration; budget chosen on cost/latency tradeoff, no saturation curve given. — https://arxiv.org/abs/2507.18755
    14	- [preprint, 2026] "Looping is not reliability": forcing a second revision after a correct patch dropped current-correctness 0.820 → 0.673 while ever-correct rose to 0.847 (correct patches found, then lost). Stale verifier traces harmed 34/135 correct starts vs 4/135 with current traces (+22.2 pts, 95% CI [8.9, 37.0]). Recommends binding verifier evidence to an exact code state and preserving verified checkpoints rather than looping. — https://arxiv.org/abs/2607.24604
    15	- [primary] Repeated independent sampling: SWE-bench Lite coverage 15.9% (1 sample) → 56% (250 samples) with DeepSeek-Coder-V2; coverage is log-linear in samples, but without an automatic verifier majority-vote/reward-model selection "plateau beyond several hundred samples". Condition: the gain is realised only with a trustworthy verifier (tests). — https://arxiv.org/abs/2407.21787
    16	- [UNVERIFIED] Verifier gap on SWE-bench Verified: mean pass@1 76.1%, oracle pass@3 84.4%, LLM-verifier selection 78.2% (arXiv 2607.05391); SWE Atlas reports 2–3x drop from Pass@3 to Pass^3 (all three runs pass). Seen only in search snippets. — https://arxiv.org/pdf/2607.05391 ; https://arxiv.org/pdf/2605.08366
    17	- [vendor doc] Claude Code best practices: "If you've corrected Claude more than twice on the same issue in one session, the context is cluttered with failed approaches. Run /clear and start fresh with a more specific prompt"; "A clean session with a better prompt almost always outperforms a long session with accumulated corrections"; "A fresh context improves code review since Claude won't be biased toward code it just wrote." — https://code.claude.com/docs/en/best-practices
    18	
    19	On stopping: (1) a loop whose only signal is the model re-reading its own output degrades after round 1 (Huang; Self-Refine); (2) with a real verifier, independent fresh attempts scale better than longer single trajectories; (3) revising an already-passing state loses correct work; (4) the only published numeric restart triggers are heuristics: 2 failed corrections → fresh context (Anthropic), 3 same-error iterations → new agent (Osmani).
    20	
    21	## B. Review staging, cost of defects, reviewer throughput, PR size
    22	
    23	- [journalism; book] The "1x/10x/100x by phase" chart has no traceable data: Pressman 1987 cites IBM Systems Sciences Institute "course notes" [IBM81]; Bossavit found the institute was an internal training programme with no supporting data; Hillel Wayne: "it doesn't exist". — https://www.theregister.com/2021/07/22/bugs_expense_bs/ ; https://leanpub.com/leprechauns
    24	- [primary] Menzies et al., 171 TSP projects 2006–2014: "no evidence for the delayed issue effect"; resolving later was not consistently or substantially costlier. Shift-left multipliers are not empirically established. — https://arxiv.org/abs/1609.04886
    25	- [UNVERIFIED] Design vs code inspection effectiveness (secondhand averages 55% vs 60%, attributed to Code Complete) and Fagan 1976 "82% of errors found" could not be verified in the primary text; a snippet of Fagan's paper reports a 23% net coding productivity gain from design+code inspections (PDF not opened). Treat design-vs-code effectiveness comparisons as unsupported. — https://www.ida.liu.se/~TDDC90/labs/lab-papers/fagan76.pdf
    26	- [primary, ICSE-SEIP 2018] Google (9M reviewed changes): median change 24 lines; >35% touch one file, ~90% <10 files, >10% are single-line; median reviewer count 1, <25% of changes have >1 reviewer; initial feedback median <1 hour for small changes vs ~5 hours for very large; overall median review latency <4 hours; defect finding "welcomed but not the only focus" — readability and norms dominate. — https://research.google/pubs/modern-code-review-a-case-study-at-google/ (PDF: https://sback.it/publications/icse2018seip.pdf)
    27	- [primary, vendor doc] Google eng-practices: "100 lines is usually a reasonable size for a CL, and 1000 lines is usually too large"; "a 200-line change in one file might be okay, but spread across 50 files it would usually be too large"; reviewers may reject a CL solely for size. — https://google.github.io/eng-practices/review/developer/small-cls.html
    28	- [vendor study] SmartBear/Cisco (vendor evaluating its own tool, 2006): review ≤200–400 LOC per session; defect density drops significantly above ~500 LOC/hour; ≤60 minutes per session; the "70–90% defect discovery" figure appears on the vendor page, not independently verified. — https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/
    29	- [primary, ICSE 2013, abstract only] Microsoft (Bacchelli & Bird): finding defects is the top stated motivation, but "reviews are less about defects than expected"; defect comments are a small proportion. The often-quoted "~15%" comes from a later Microsoft paper, not this one. — https://2013.icse-conferences.org/content/expectations-outcomes-and-challenges-modern-code-review.html
    30	- [primary, TOSEM] 567 Claude Code PRs across 157 OSS projects: 83.8% eventually merged; 54.9% of merged PRs merged unmodified, 45.1% needed human revision (mostly bug fixes, docs, project-standard conformance). — https://arxiv.org/abs/2509.14745
    31	
    32	Net: primary support for small changes and one fast reviewer; none for phase-cost multipliers or design-review-beats-code-review.
    33	
    34	## C. Stop-the-line and rework loops in quality systems
    35	
    36	- [primary, Toyota UK] Andon: any line member may pull the cord; first pull calls the team leader, line continues if fixed within the station's takt; otherwise the line stops until resolved. Rationale (jidoka): fix at source, short-term cost accepted for root-cause elimination. — https://mag.toyota.co.uk/toyota-manufacturing-25-objects-andon-cord/
    37	- [secondary] PDCA: Shewhart (1920s), adapted by Deming. Five Whys (Ohno): "five" is not literal; iterate until the root cause is removed; criticised as shallow. — https://en.wikipedia.org/wiki/PDCA ; https://www.lean.org/lexicon-terms/5-whys/
    38	- [primary, NIST handbook] Western Electric run rules as process-intervention triggers on a Shewhart chart: 1 point beyond 3σ; 2 of 3 beyond 2σ same side; 4 of 5 beyond 1σ same side; 8 consecutive on one side of centre. False-alarm rate: 1 in 371 points with 3σ alone, 1 in 91.75 with all WECO rules. A signal triggers assignable-cause investigation, not an automatic halt. — https://itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm
    39	- [primary, DORA] Instability metrics: change fail rate = "percentage of deployments causing failures in production"; deployment rework rate (added 2024) = "percentage of deployments that are unplanned work to fix bugs". Throughput: lead time, deploy frequency, failed-deployment recovery time. — https://dora.dev/guides/dora-metrics/history/
    40	- [primary, Google blog of DORA 2025] n≈5,000; 90% use AI; >80% perceive productivity gain; 30% little/no trust in AI code; AI adoption now positively related to throughput but still "a negative relationship with software delivery stability"; seven team archetypes; AI framed as an amplifier of existing strengths/weaknesses. — https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report
    41	
    42	## D. Current multi-agent coding practice (2025–2026)
    43	
    44	- [vendor doc] Anthropic "Building effective agents": evaluator-optimizer fits when "LLM responses can be demonstrably improved when a human articulates their feedback" and "the LLM can provide such feedback"; add "stopping conditions (such as a maximum number of iterations)"; "find the simplest solution possible"; agents trade latency and cost for performance and errors compound. — https://www.anthropic.com/engineering/building-effective-agents
    45	- [vendor doc] Anthropic multi-agent research system: agents ≈4x chat tokens, multi-agent ≈15x; Opus-lead + Sonnet-subagents beat single Opus by 90.2% on an internal breadth-first research eval; token usage explains 80% of BrowseComp variance (95% with tool calls + model choice); effort scaling rule: simple fact 1 agent/3–10 tool calls, comparisons 2–4 subagents/10–15 calls each, complex >10 subagents; notes "most coding tasks have fewer parallelizable subtasks than research"; early versions over-spawned subagents and failed to stop, fixed with explicit effort budgets and stop criteria. — https://www.anthropic.com/engineering/multi-agent-research-system
    46	- [vendor doc] Claude Code best practices: give the agent a runnable check; "by a second opinion: a verification subagent... has a fresh model try to refute the result, so the agent doing the work isn't the one grading it"; "/clear after two failed corrections"; writer/reviewer split across sessions; warning: "A reviewer prompted to find gaps will usually report some, even when the work is sound... Tell the reviewer to flag only gaps that affect correctness or the stated requirements." — https://code.claude.com/docs/en/best-practices
    47	- [vendor doc] Claude Code Review (managed): multiple parallel agents each hunting one defect class, then a verification step filters false positives before posting; average 20 minutes and $15–25 per review, scaling with PR size; `low` effort reports only high-confidence findings; REVIEW.md can cap nits ("at most five") and demand `file:line` evidence; re-review convergence rule suppresses new nits after round 1. — https://code.claude.com/docs/en/code-review
    48	- [vendor doc, PDF] OpenAI "A practical guide to building agents": "maximize a single agent's capabilities first"; split agents on complex conditional logic or tool overload ("some implementations successfully manage more than 15 well-defined, distinct tools while others struggle with fewer than 10 overlapping tools"); prototype with the most capable model, then swap smaller models per task; human intervention triggers: "Exceeding failure thresholds: set limits on agent retries or actions" and "High-risk actions: sensitive, irreversible, or high stakes"; guardrails layered (LLM, regex, moderation, tool-risk rating, output validation). No numeric retry count given. — https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf
    49	- [practitioner, unattributed numbers] Osmani "Code Agent Orchestra": 3–5 agents sweet spot ("don't run more agents than you can meaningfully review"); one file one owner; 1 reviewer per 3–4 builders; per-agent token budgets (180k frontend/280k backend) with auto-pause at 85%; MAX_ITERATIONS=8; kill/reassign after 3 same-error iterations; cites ETH Zurich (Gloaguen et al.): LLM-written AGENTS.md −3% success, +20% cost; developer-written +4%. — https://addyosmani.com/blog/code-agent-orchestra/
    50	- [primary RCT] METR early-2025: 16 experienced OSS developers, 246 issues, Cursor Pro + Claude 3.5/3.7; AI-allowed tasks took 19% longer; developers forecast +24% and afterwards believed +20%; authors say not to generalise, and the page is now marked superseded by the Feb-2026 update. — https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/
    51	- [UNVERIFIED, secondary] METR Feb-2026 continuation: returning developers −18% (CI −38% to +9%), new recruits −4% (CI −15% to +9%); both CIs cross zero; METR called the data an unreliable signal (selection: developers refusing the no-AI arm; pay cut; multi-agent timing) and redesigned the study. Sign convention disputed in secondary coverage; metr.org not opened. — https://blog.robbowley.net/2026/04/04/metrs-developer-productivity-research-2026-update/
    52	
    53	## E. LLM-as-judge for code
    54	
    55	- [primary, EMNLP 2024 Industry] Format restriction (JSON/XML) causes "a significant decline in LLMs reasoning abilities"; stricter constraints degrade more; secondary summaries report classification can be neutral or improved; recommended pattern is reason in free text, then convert to the schema. — https://arxiv.org/abs/2408.02442
    56	- [preprint, 2026, 21 judges, ~541k judgments] "Reliability without validity": exact-match agreement overstates chance-corrected agreement by 33.8–41.3 points on MT-Bench (85% exact ≈ κ 0.48; best κ 0.511); test-retest ≈0.94 yet strongly position-biased judges exist (|P(A)−0.5| up to 0.192). Recommends κ, position-swap checks, ≥3 replicates, ≥2 benchmarks. — https://arxiv.org/html/2606.19544v1
    57	- [preprint, 2026] Judges without a reference answer are lenient: adding a visible reference flipped 9–85% of verdicts, mostly correct→incorrect, and raised human agreement (e.g., 0.34 → 0.85 for Gemma3-27B). Condition: give the judge the spec/expected behaviour, not just the artifact. — https://www.alphaxiv.org/abs/2607.12885.md
    58	- [preprint, 2026] Multi-round review: single-pass review had best F1 (0.376); a second round raised recall ~0.08 but produced 62% more false positives (8.5 vs 5.2 per artifact), precision 0.30 → 0.20 ("false positive pressure": reviewers invent findings once real errors are exhausted); independent re-review without context was worst (0.263). Small single-author study, 30 artifacts/150 planted errors. — https://arxiv.org/abs/2603.16244
    59	- [preprint, ISSTA 2026] MCR-Bench, 2,269 real multi-round review tasks: performance "degrading significantly as the number of interaction rounds increases"; failure drivers are cross-round temporal misalignment and poor long-range memory (secondary summary, UNVERIFIED: over-reviewing ≈27.8%, re-flagging fixed defects ≈32.5% of errors). — https://arxiv.org/abs/2608.27442
    60	- [preprint, 2026] Cross-model review (Opus 4.6 generator; GPT-5.4, Gemini 2.5 Pro/Flash reviewers; 150 planted errors): top-tier cross-model F1 32.3% vs same-model fresh-session 28.6%, difference not significant; cross-model recall higher (38.4 vs 27.1), precision lower (28.6 vs 31.5); overlap between the two Jaccard 41.2%; one same-model + one cross-model review covered 56.7% of errors vs 42.7% for two same-model; same-model better on code (40.7 vs 37.2); 9.4% of cross-model false positives were "model bias" (flagging the generator's real tools/features as nonexistent); lightweight cross-model reviewer (24.0%) was no better than self-review. Single author, Korean artifacts, keyword matching. — https://arxiv.org/html/2610.01471v2
    61	- [preprint, 2026] Five-model code-review comparison (n=150): Haiku 4.5 F1 0.365 (P 0.486/R 0.293) vs Sonnet 4.6 0.343 (P 0.558/R 0.248); every Haiku+second-model union lowered F1 (0.304–0.333) — models largely find the same bugs and the second model adds its false positives; 19/150 samples were a shared blind spot. — https://arxiv.org/html/2606.15689v1
    62	- [vendor doc] Anthropic's own practice: structured severity tags (Important/Nit/Pre-existing), a dedicated verification agent to filter candidates, evidence requirement ("behavior claims need a file:line citation"), and the explicit "find gaps" over-reporting warning. — https://code.claude.com/docs/en/code-review ; https://code.claude.com/docs/en/best-practices
    63	
    64	## F. Cost optimisation in agent pipelines
    65	
    66	- [vendor doc] Claude prompt caching: cache write 1.25x base input (5-min TTL) or 2x (1-hour); cache read 0.1x (0.05x on Opus/Sonnet 5.5, 0.025x on Fable/Mythos 5.1); minimum cacheable prefix 512–4,096 tokens by model; cache hits don't count against rate limits. — https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching
    67	- [preprint, 500+ agent sessions] Prompt caching cut API cost 41–80% across OpenAI/Anthropic/Google with 10k-token system prompts and improved TTFT 13–31%; naive full-context caching can increase latency; keep dynamic content and tool results out of the cached prefix. — https://arxiv.org/abs/2601.06007
    68	- [primary, ICLR 2025] RouteLLM: preference-trained strong/weak routers cut cost "by over 2 times in certain cases" without quality loss; routers transfer when the model pair is swapped. The "85% cheaper at 95% of GPT-4" headline is benchmark-specific (MT-Bench), per secondary sources. — https://arxiv.org/abs/2406.18665
    69	- [vendor doc] Anthropic published unit costs: ≈$13/developer/active day, $150–250/month, 90% under $30/day; Code Review $15–25 per PR review (per-push triggers multiply cost by pushes); monthly spend caps per service. — https://code.claude.com/docs/en/costs ; https://code.claude.com/docs/en/code-review
    70	- [UNVERIFIED] Cost-per-merged-change numbers: single-author experiment reporting $7–$70 for the same feature across agents with harness alone moving cost ~2.5x; "durable change" accounting (merged minus later corrective work) exists only as worked examples. No controlled study measures routing, caching and cost-per-merge together. — https://getunblocked.com/blog/cost-per-merged-pr/
    71	
    72	## Gaps (searched, not found)
    73	
    74	No primary study plots coding-agent success against self-repair iteration count for one model; no controlled comparison of JSON-verdict vs free-text judges on code; no primary data isolating "find gaps" prompt wording; no peer-reviewed cost-per-merged-change benchmark.
FILE .orchestration/validation/dotfiles-T128-regime-v3-a01-research/claude-code-factsheet.md
     1	# Claude Code capability fact sheet (docs as of 2026-10-11; installed 2.1.293)
     2	
     3	Sources: code.claude.com/docs/en/* and anthropic.com/engineering. Fetched directly. "UNVERIFIED" marks claims the pages did not confirm.
     4	
     5	Abbreviations: CLI = https://code.claude.com/docs/en/cli-reference, HEADLESS = https://code.claude.com/docs/en/headless, HOOKS = https://code.claude.com/docs/en/hooks, PERM = https://code.claude.com/docs/en/permissions, PMODES = https://code.claude.com/docs/en/permission-modes, SETTINGS = https://code.claude.com/docs/en/settings, SANDBOX = https://code.claude.com/docs/en/sandboxing, SUB = https://code.claude.com/docs/en/sub-agents, TEAMS = https://code.claude.com/docs/en/agent-teams, BP = https://code.claude.com/docs/en/best-practices, CACHE = https://code.claude.com/docs/en/prompt-caching, COSTS = https://code.claude.com/docs/en/costs.
     6	
     7	## 1. Headless / non-interactive
     8	
     9	- `--output-format`: `text` (default), `json` ("structured JSON with result, session ID, and metadata"), `stream-json` (NDJSON; last line is a `result` message "with the final response text, cost, and session metadata") — HEADLESS
    10	- `--json-schema` (print mode only): "The response includes metadata about the request (session ID, usage, etc.) with the structured output in the `structured_output` field"; invalid schema exits with `Error: --json-schema is not a valid JSON Schema`; `format` keyword is annotation-only — HEADLESS, CLI
    11	- JSON result fields: `total_cost_usd` plus "a per-model cost breakdown" (`modelUsage`), `usage` (incl. `cache_creation.ephemeral_1h_input_tokens`/`ephemeral_5m_input_tokens`), `session_id`, `permission_denials`, `subtype` (`success`, `error_max_turns`, `error_max_budget_usd`, `error_during_execution`), `duration_api_ms`; `usage` "Excluded" subagents, `total_cost_usd`/`modelUsage` "Included" — HEADLESS, CACHE, https://code.claude.com/docs/en/agent-sdk/cost-tracking. `num_turns`: UNVERIFIED on these pages.
    12	- Costs are "client-side estimates, not authoritative billing data" — cost-tracking
    13	- `--max-budget-usd` (print only): "Spend from subagents counts toward the cap. Spend can pass the cap, so leave headroom"; at the cap "spawning another subagent fails with `Budget limit reached`" and background subagents are stopped (v2.1.217+); restored totals from `--continue/--resume` don't count — CLI
    14	- `--max-turns` (print only): "Exits with an error when the limit is reached. No limit by default" — CLI
    15	- `--permission-mode`: `default`, `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions`, `manual` alias; "Overrides `defaultMode` from settings files" — CLI
    16	- A `-p` run starts in `default` "in sessions that fetch feature flags"; `auto` only in non-flag sessions on v2.1.285+ — PMODES
    17	- `dontAsk`: "denies every call that would otherwise prompt"; `AskUserQuestion`, `requiresUserInteraction` MCP tools, network-path reads "are denied even when an allow rule matches" — HEADLESS
    18	- `--permission-prompts none` (v2.1.259+): "Anything that would prompt is denied unless a `PermissionRequest` hook allows it, Claude is told that nobody can approve the request and not to retry it"; removes `AskUserQuestion`; denials appear in `permission_denials` — HEADLESS
    19	- `--allowedTools`: in a run that starts in auto mode "Claude Code drops a bare `Bash` entry as a broad allow rule and auto mode evaluates each command instead" — HEADLESS. `--disallowedTools`: bare name removes the tool from context; scoped rule denies matching calls — CLI
    20	- `--bare`: skips "hooks, skills, custom commands, subagents, installed plugins, MCP servers, auto memory, and CLAUDE.md"; "never reads OAuth credentials or the system keychain. For the Anthropic API, set `ANTHROPIC_API_KEY`... or supply an `apiKeyHelper` in the `--settings` JSON"; no system reminders, no background tasks (v2.1.286+); "will become the default for `-p`" — HEADLESS. Bare sessions bind no inbox socket, so they can't receive cross-session messages — https://code.claude.com/docs/en/cross-session-messaging
    21	- Without `--bare`, `-p` "runs the hooks in a project's `.claude/settings.json` and connects the servers in its `.mcp.json`, even in a folder you've never trusted" — HEADLESS
    22	- `--settings`: file or inline JSON, "above your user, project, and local files and below managed settings" — SETTINGS. `--setting-sources user,project,local` restricts sources — CLI
    23	- `--resume <id|name|transcript-path>`, `--continue` (skips `-p`-created sessions unless `claude -p --continue`), `--fork-session`, `--session-id <uuid>`, `--no-session-persistence` — CLI
    24	- `--agents` JSON (file path with `--print`, v2.1.281+); `--model`; `--effort low|medium|high|xhigh|max|ultracode`; `--append-system-prompt[-file]`; `--forward-subagent-text`; `--include-hook-events` — CLI
    25	- `-p` waits for background subagents/workflows after the final turn, idle cap 10 min (`CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS`) — HEADLESS
    26	
    27	## 2. Hooks
    28	
    29	- Events: SessionStart, Setup, UserPromptSubmit, UserPromptExpansion, PreToolUse, PermissionRequest, PermissionDenied, PostToolUse, PostToolUseFailure, PostToolBatch, Notification, MessageDisplay, SubagentStart, SubagentStop, TaskCreated, TaskCompleted, Stop, StopFailure, TeammateIdle, InstructionsLoaded, ConfigChange, CwdChanged, DirectoryAdded, FileChanged, WorktreeCreate, WorktreeRemove, PreCompact, PostCompact, PreModelSwitch, PostModelSwitch, Elicitation, ElicitationResult, SessionEnd — HOOKS
    30	- Common input: `session_id`, `prompt_id`, `transcript_path` ("written asynchronously and may lag"), `cwd`, `scratchpad_dir`, `permission_mode`, `effort.level`, `hook_event_name`; agent fields `agent_id`, `agent_type` — HOOKS
    31	- Per-event: SessionStart `source` = `startup|resume|clear|compact|fork`; SessionEnd `reason` incl. `clear`, `resume`, `logout`, `prompt_input_exit`, `other`; PostToolUse `tool_name`, `tool_input`, `tool_response`, `tool_use_id`; Stop/SubagentStop `stop_hook_active`, `last_assistant_message`, SubagentStop adds `agent_transcript_path`; TaskCompleted `task_id`, `task_subject`, `task_description`, `teammate_name`; TeammateIdle `teammate_name` — HOOKS. PreCompact/PostCompact input fields: UNVERIFIED (not extracted).
    32	- Blocking: "Exit with code 2 to block the action"; other non-zero = "non-blocking error. The action goes ahead". Can block: PreToolUse, UserPromptSubmit, Stop, SubagentStop, TeammateIdle, TaskCreated, TaskCompleted, ConfigChange, PreCompact, PreModelSwitch, Elicitation*, Worktree*, PostToolBatch. Cannot: PermissionRequest ("Exit code 2 isn't honored"), PostToolUse, PermissionDenied, Notification, SubagentStart, SessionStart/End, PostCompact, StopFailure — HOOKS
    33	- JSON: `continue:false` + `stopReason` stops Claude entirely; `decision:"block"` + `reason` (only value is `block`); PreToolUse `hookSpecificOutput.permissionDecision` `allow|deny|ask|defer`, `updatedInput`; PermissionRequest `hookSpecificOutput.decision.behavior` `allow|deny` with `updatedInput`, `message`, `interrupt`; `additionalContext`; `systemMessage` — HOOKS
    34	- Stop: `stop_hook_active` "is `true` when Claude Code is already continuing as a result of a stop hook"; "8-consecutive-continuation cap... resets each time Claude calls a tool. To raise the cap, set `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP`" (0 disables) — HOOKS, env-vars
    35	- SubagentStop block "keeps the subagent running and delivers `reason` to the subagent as its next instruction" — HOOKS
    36	- TaskCompleted: exit 2 → "the task is not marked as completed and the stderr message is fed back"; "When the `TaskUpdate` tool triggered the event, Claude Code ignores `continue: false`; exit code 2 still blocks" — HOOKS
    37	- Timeouts: default 600 s for `command`/`http`/`mcp_tool`, 30 s `prompt`, 60 s `agent`; 30 s on UserPromptSubmit/PreModelSwitch; SessionEnd 1.5 s; `async:true` hooks "can't block" — HOOKS
    38	- Execution: "All matching hooks run in parallel. If you define the same handler in more than one settings file, it runs once" — HOOKS
    39	- Settings precedence (highest first): "managed settings, command line, project local, shared project, user" — SETTINGS. (The caller's assumed order "managed > user > project > local" does not match the page.)
    40	- `disableAllHooks`: "set in user, project, or local settings can't disable those managed hooks"; `allowManagedHooksOnly` blocks user/project/local/plugin hooks; for untrusted repos use `--settings '{"disableAllHooks": true}'` because "the repository's project settings take precedence over yours" — HOOKS, PERM
    41	- Env: `$CLAUDE_PROJECT_DIR`, `CLAUDE_ENV_FILE` (SessionStart), `$CLAUDE_EFFORT`, `CLAUDE_CODE_REMOTE`, `CLAUDE_CODE_MESSAGING_SOCKET`; "There is no `$CLAUDE_MODEL`" — HOOKS. `CLAUDE_SESSION_ID`: UNVERIFIED (absent from hooks and env-vars pages; use stdin `session_id`).
    42	
    43	## 3. Permissions and sandbox
    44	
    45	- "Rules are evaluated in order: deny, then ask, then allow... An allow rule can't carve an exception out of a deny rule"; "If a tool is denied at any level, no other level can allow it... a managed settings deny can't be overridden by `--allowedTools`" — PERM
    46	- `allowManagedPermissionRulesOnly` makes managed the only rule source; `disableAutoMode`/`disableBypassPermissionsMode: "disable"` work from any scope — PERM
    47	- `defaultMode` `auto` and `bypassPermissions` "don't take effect from project or local settings; set them in user or managed settings instead" (bypass from any file before v2.1.257) — SETTINGS, PMODES
    48	- Protected paths (`.git`, `.claude` except `.claude/worktrees/`, etc.): `default/acceptEdits` prompted, `auto` routed to classifier, `dontAsk` denied, `bypassPermissions` allowed; `permissions.allow` "do not pre-approve protected-path writes" — PMODES
    49	- Auto mode: "a second model, the classifier"; runs "on Claude Sonnet 5 by default"; blocks e.g. "Sending keystrokes to Claude Code's own tmux pane... which the classifier treats as Claude changing its own permissions or oversight", "Writing to Claude Code session transcripts", "Launching an autonomous agent loop that runs without human approval or a sandbox, such as one started with `--dangerously-skip-permissions`"; rule labels appear as `[Data Exfiltration]`, `Git Destructive`; a rule literally labeled "Self-Modification": UNVERIFIED — PMODES, https://code.claude.com/docs/en/auto-mode-config
    50	- Fallback: "if the classifier blocks an action 3 times in a row or 20 times total, auto mode pauses and Claude Code resumes prompting" (not configurable); in `-p` "Claude Code doesn't stop the run" — PMODES, BP. The Mar 2026 engineering post says headless "we instead terminate the process" — docs for 2.1.293 supersede.
    51	- `autoMode` is read only from user, managed, `--settings`; "doesn't read `autoMode` from project settings"; `permissions.ask` rules "always force a permission prompt, even in auto mode"; `autoMode.classifyAllShell` — auto-mode-config
    52	- Classifier reviews subagent work at spawn, during, and "When the subagent finishes... before the parent reads the report"; flagged reports are "prepended with a security warning" — PMODES
    53	- Sandbox: OS-enforced for Bash/PowerShell/Monitor only; file tools, MCP, hooks run outside; `network.allowedDomains` "start empty"; `excludedCommands` run "outside the sandbox, which means no filesystem restrictions and no network proxy"; `allowUnsandboxedCommands:false` makes Claude Code "ignore the `dangerouslyDisableSandbox` parameter"; a `false` in user/`--settings`/managed "holds even when a project's settings set `true`" (v2.1.285+); under an admin-required sandbox repo files' `excludedCommands`, `allowedDomains`, `allowUnixSockets` are ignored; `strictAllowlist` and `allowManagedDomainsOnly` deny instead of prompt — SANDBOX
    54	
    55	## 4. Subagents
    56	
    57	- Frontmatter: `name`, `description` (required); `tools`, `disallowedTools`, `model` (`sonnet|opus|haiku|fable|<id>|inherit`), `effort` (`low..max`), `permissionMode` (`default|acceptEdits|auto|dontAsk|bypassPermissions|plan`), `maxTurns`, `skills`, `mcpServers`, `hooks`, `memory` (`user|project|local`), `background: true`, `isolation: worktree`, `color`, `initialPrompt`, `omitClaudeMd`, `experimental.cacheTtl` — SUB
    58	- `isolation: worktree`: "temporary git worktree... branched by default from your default branch... automatically cleaned up if the subagent makes no changes"; worktree path `<repo>/.claude/worktrees/<name>` is documented for `--worktree` (CLI) and WorktreeCreate covers subagent isolation (HOOKS); exact subagent path: UNVERIFIED
    59	- Concurrency: "when 20 subagents are running in a session, spawning another... fails with `Concurrent subagent limit reached`" (`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`); nesting up to three layers (`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`) — SUB
    60	- Foreground blocks and passes prompts through; background prompts surface in main session; background subagents "run with a smaller built-in tool set"; fork mode is default in interactive sessions (background, no `run_in_background`) and off in `-p`/SDK — SUB
    61	- "Each subagent starts with a fresh, isolated context window"; Explore/Plan skip CLAUDE.md and are one-shot; others get an agent ID resumable via `SendMessage`; transcripts at `~/.claude/projects/{project}/{sessionId}/subagents/agent-{agentId}.jsonl` — SUB
    62	- Reviewer pattern: `code-reviewer` with `tools: Read, Grep, Glob, Bash`, `model: inherit`; "Limit tool access" — SUB. Over-reporting: "A reviewer prompted to find gaps will usually report some, even when the work is sound... Tell the reviewer to flag only gaps that affect correctness or the stated requirements" — BP
    63	
    64	## 5. Agent view, teams, messaging, workflows
    65	
    66	- Agent view (research preview): `claude --bg "<prompt>"` (positional, rejects `-p`), `claude agents [--json [--all]] [--cwd]`, `claude attach|logs|stop|respawn|rm <id>`; supervisor keeps sessions running; "Before editing files, Claude moves the session into an isolated git worktree under `.claude/worktrees/`" (opt out `worktree.bgIsolation: "none"`); permission prompts are not auto-answered ("Needs input"); finishes with "a report saying what it did and where the work is"; "never pushes to `main` or `master`" — https://code.claude.com/docs/en/agent-view
    67	- Agent teams: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`; "approximately 7x more tokens than standard sessions when teammates run in plan mode" (COSTS); not spawned in `-p`; `TeammateIdle`/`TaskCreated`/`TaskCompleted` exit 2 "send feedback and keep the teammate working"; plan approval: "Claude Code approves the plan in the lead's session as soon as the request arrives, without the lead reviewing it"; "A teammate can't approve a permission prompt or supply consent on your behalf"; teammates inherit lead's mode except `dontAsk`; one team per session, no nesting — TEAMS
    68	- Cross-session messaging (v2.1.224+): Claude uses `ListAgents`/`SendMessage`; incoming message "can't approve anything", "can't change configuration", commands arrive as text; `crossSessionInbound` `accept|hold|refuse`; `-p` sessions bind an inbox (not `--bare`); start a `-p` worker with `crossSessionInbound: accept` in `--settings` — cross-session-messaging
    69	- Workflows: JS script Claude writes; `agent(prompt, { schema, label, stallMs })`, `pipeline()`, `parallel()`, `phase()`, `log()`, `args`; `schema` → "that subagent returns JSON matching the shape" (five validation attempts); 16 concurrent agents default, 1,000 per run; resume: completed agents "return saved result", failed and later ones rerun; in `-p` needs a `Workflow` allow rule, auto mode, bypass, or PreToolUse hook; "have independent agents adversarially review each other's findings" — https://code.claude.com/docs/en/workflows
    70	
    71	## 6. Cost, telemetry, caching
    72	
    73	- `/usage` Session block: total cost, per-model tokens, `Prompt cache (main)` hit ratio and warm/cold; resets on `/clear`; `/cost` is not documented on the costs page (UNVERIFIED as a current command) — COSTS
    74	- OTel (`CLAUDE_CODE_ENABLE_TELEMETRY=1`): metrics `claude_code.session.count`, `lines_of_code.count`, `pull_request.count`, `commit.count`, `cost.usage`, `token.usage`, `code_edit_tool.decision`, `active_time.total`; events `user_prompt`, `tool_result`, `api_request` (`cost_usd`, `input_tokens`, `cache_read_tokens`, `cache_creation_tokens`), `api_error`, `tool_decision` (`source`: `config|hook|user_permanent|...`); `session.id`, `prompt.id` attributes — https://code.claude.com/docs/en/monitoring-usage
    75	- Transcripts: `~/.claude/projects/<project>/<session-id>.jsonl`, `<project>` = cwd with non-alphanumerics → `-`; "The entry format is internal to Claude Code and changes between versions"; session cost totals are saved to the transcript on normal exit (v2.1.277+). Per-message usage in each JSONL line: UNVERIFIED — sessions, cost-tracking
    76	- Cache invalidators: model switch, effort change ("On Opus 5.5, Sonnet 5.5, Haiku 5.5, and Fable 5.1 with an API key or a Claude subscription, the cache stays intact"), fast mode, MCP server connect/remove (when tools loaded upfront), plugin MCP changes, bare-tool deny without tool search, compaction, many images, upgrade. Cache-safe: permission mode change, CLAUDE.md edits (don't apply until `/clear`/`/compact`), skills, `/rewind` — CACHE
    77	- TTL: main conversation 1 h on subscription within plan usage, else 5 min; "Everything else" (subagents, workflows, teammates, forks) 5 min; `promptCacheTtl`/`subagentPromptCacheTtl` or `CLAUDE_CODE_[SUBAGENT_]PROMPT_CACHE_TTL` (`5m|1h`, v2.1.242+); subagent "first request doesn't read the parent's cache"; a fork "reads the parent's cache" — CACHE
    78	
    79	## 7. Quality-loop guidance
    80	
    81	- "If you've corrected Claude more than twice on the same issue in one session, the context is cluttered with failed approaches. Run `/clear` and start fresh with a more specific prompt that incorporates what you learned. A clean session with a better prompt almost always outperforms a long session with accumulated corrections." — BP
    82	- "Give Claude a check it can run: tests, a build, a screenshot to compare"; gates: in one prompt, `/goal`, "a Stop hook runs your check as a script and blocks the turn from ending until it passes", "a verification subagent... has a fresh model try to refute the result, so the agent doing the work isn't the one grading it"; "Have Claude show evidence rather than asserting success" — BP
    83	- "A fresh context improves code review since Claude won't be biased toward code it just wrote"; Writer/Reviewer table across two sessions; "A reviewer running in a fresh subagent context sees only the diff and the criteria you give it... Report gaps, not style preferences" — BP
    84	- Plan mode: "If you could describe the diff in one sentence, skip the plan" — BP
    85	- `/goal`: "a session-scoped prompt-based Stop hook"; evaluator is "your configured small fast model", "does not call tools, so it can only judge what Claude has already surfaced"; stops with warning after "no tool use for several turns in a row"; works in `-p`; unavailable when `disableAllHooks` or `allowManagedHooksOnly` — https://code.claude.com/docs/en/goal
    86	
    87	## 8. Anthropic engineering guidance
    88	
    89	- Building effective agents (https://www.anthropic.com/engineering/building-effective-agents): orchestrator-workers is "well-suited for complex tasks where you can't predict the subtasks needed". Evaluator-optimizer is "particularly effective when we have clear evaluation criteria, and when iterative refinement provides measurable value"; fit signs are that "LLM responses can be demonstrably improved when a human articulates their feedback" and the LLM can provide that feedback. Add complexity only when it "demonstrably improves outcomes"; "Agentic systems often trade latency and cost for better task performance".
    90	- Multi-agent research system (https://www.anthropic.com/engineering/multi-agent-research-system): Opus 4 lead + Sonnet 4 subagents "outperformed single-agent Claude Opus 4 by 90.2%"; "token usage by itself explains 80% of the variance"; "multi-agent systems use about 15× more tokens than chats", so they "require tasks where the value of the task is high enough to pay for the increased performance"; "most coding tasks involve fewer truly parallelizable tasks than research". Judging: "a single LLM call with a single prompt outputting scores from 0.0-1.0 and a pass-fail grade" was most aligned; "focusing on end-state evaluation rather than turn-by-turn analysis"; start with ~20 real queries.
    91	- Demystifying evals (https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents): code-based graders "Fast, Cheap, Objective, Reproducible" but brittle; model-based "Flexible", "Non-deterministic", "Requires calibration with human graders"; prefer "deterministic graders where possible", LLM graders "where necessary"; `pass@k` for one success, `pass^k` "for agents where consistency is essential"; grade each dimension "with an isolated LLM-as-judge"; "Give the LLM a way out"; "You won't know if your graders are working well unless you read the transcripts"; "20-50 simple tasks drawn from real failures is a great start".
    92	- Effective harnesses for long-running agents (https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents): initializer agent + incremental coding agent, `claude-progress.txt`, feature list "initially marked as 'failing'", git commits per step, "It is unacceptable to remove or edit tests", "Self-verify all features. Only mark features as 'passing' after careful testing", "only one feature at a time".
    93	- Harness design for long-running apps, Mar 2026 (https://www.anthropic.com/engineering/harness-design-long-running-apps): planner/generator/evaluator; agents "confidently praising the work—even when... obviously mediocre"; "tuning a standalone evaluator to be skeptical turns out to be far more tractable than making a generator critical of its own work"; sprint contracts with hard per-criterion thresholds; full harness "over 20x more expensive" ($200 vs $9) but on Opus 4.6 tasks within solo capability "no longer needed the evaluator": "It is worth the cost when the task sits beyond what the current model does reliably solo"; "every component in a harness encodes an assumption about what the model can't do on its own".
    94	- Building a C compiler with parallel Claudes, Feb 2026 (https://www.anthropic.com/engineering/building-c-compiler): 16 agents, lock files in `current_tasks/` plus git, no orchestrator; "the task verifier is nearly perfect" or Claude "will solve the wrong problem"; ~2,000 sessions, "just under $20,000"; "it is easy to see tests pass and assume the job is done, when this is rarely the case".
    95	- Auto mode, Mar 2026 (https://www.anthropic.com/engineering/claude-code-auto-mode): two-stage classifier on user messages and tool calls only; "Everything the agent chooses on its own is unauthorized until the user says otherwise"; "Degrade security posture" covers "modifying the agent's own permission config"; runs "at both ends of a subagent handoff" because inside a subagent "the orchestrator's instruction is the user message"; full pipeline FPR 0.4%, FNR on overeager actions 17%.
    96	- No 2026 engineering post on code-review agents or agent teams exists on the index page — https://www.anthropic.com/engineering
FILE .orchestration/validation/dotfiles-T128-regime-v3-a01-research/codex-factsheet.md
     1	# Codex CLI 0.161.0 fact sheet (2026-10-11)
     2	
     3	Source tags: `DOC` = official docs (every `developers.openai.com/codex/*` URL now 308-redirects to `learn.chatgpt.com/docs/*`; final URL cited). `SRC` = `github.com/openai/codex` at tag `rust-v0.161.0`. `CLI` = installed `codex-cli 0.161.0 --help` output (clap only, no model call). `LOCAL` = observed on this machine's `~/.codex`, not official. Third-party claims surfaced by search were dropped.
     4	
     5	DOC short names → `https://learn.chatgpt.com` + : non-interactive-mode=/docs/non-interactive-mode; developer-commands=/docs/developer-commands?surface=cli; config-reference=/docs/config-file/config-reference; config-advanced=/docs/config-file/config-advanced; agent-approvals-security=/docs/agent-approvals-security; permissions=/docs/permissions; hooks=/docs/hooks; rules=/docs/agent-configuration/rules; subagents.md=/docs/agent-configuration/subagents.md; agents-md.md=/docs/agent-configuration/agents-md.md; third-party/github.md=/docs/third-party/github.md; pricing.md=/docs/pricing.md; models.md=/docs/models.md; cloud=/docs/cloud; codex/cli.md=/docs/codex/cli.md; github-code-reviews=/use-cases/github-code-reviews.
     6	
     7	## 1. `codex exec`
     8	
     9	- Default sandbox is read-only: "By default, `codex exec` runs in a read-only sandbox." Progress streams to stderr; only the final agent message goes to stdout. DOC — https://learn.chatgpt.com/docs/non-interactive-mode
    10	- Flags present in 0.161.0 `codex exec --help`: `-c key=value` (value parsed as TOML, dotted paths), `--enable/--disable <feature>`, `--strict-config`, `-m/--model`, `-p/--profile` (layers `$CODEX_HOME/<name>.config.toml`), `-s/--sandbox read-only|workspace-write|danger-full-access`, `--approve-for-me` ("Route approval requests through automatic review using the workspace-write sandbox"), `--dangerously-bypass-approvals-and-sandbox`, `--dangerously-bypass-hook-trust`, `-C/--cd`, `--worktree` ("Run the session in a new managed Git worktree"), `--add-dir`, `--skip-git-repo-check`, `--ephemeral`, `--ignore-user-config`, `--ignore-rules`, `--output-schema <FILE>`, `--json`, `-o/--output-last-message <FILE>`. Subcommands: `resume`, `fork`, `review`. CLI
    11	- `--full-auto`: docs say it is a "deprecated compatibility flag and prints a warning" (DOC — non-interactive-mode page); installed 0.161.0 rejects it: `error: unexpected argument '--full-auto' found`. CLI. SRC `codex-rs/exec/src/lib.rs` has no `full_auto` handling.
    12	- `-a/--ask-for-approval` exists only on top-level `codex` (`on-request | never`); `codex exec -a never` fails with `unexpected argument '-a'`. Set exec approval policy via `-c approval_policy=...`. CLI; the docs' exec flag table also omits it. DOC — https://learn.chatgpt.com/docs/developer-commands?surface=cli
    13	- Headless default: `approval_policy: Some(AskForApproval::Never)` ("Default to never ask for approvals in headless mode"; dropped when the resolved reviewer is AutoReview). SRC — https://raw.githubusercontent.com/openai/codex/rust-v0.161.0/codex-rs/exec/src/lib.rs
    14	- Git check: "Codex requires commands to run inside a Git repository to prevent destructive changes"; override with `--skip-git-repo-check`. DOC — non-interactive-mode. SRC: check is `get_git_repo_root(&default_cwd).is_none()` → prints `Not inside a trusted directory and --skip-git-repo-check was not specified.` and exits 1; also skipped when `--dangerously-bypass-approvals-and-sandbox` is set. Whether a worktree's `.git` _file_ satisfies `get_git_repo_root`: UNVERIFIED (git_info.rs not located at the tag; circumstantial: `codex exec --worktree` exists (CLI) and LOCAL worktree runs succeed).
    15	- JSONL (`--json`): event types `thread.started`, `turn.started`, `turn.completed`, `turn.failed`, `item.*` (`item.started`, `item.completed`), `error`; item types: agent messages, reasoning, command executions, file changes, MCP tool calls, web searches, plan updates. `turn.completed` carries `usage` with `input_tokens`, `cached_input_tokens`, `output_tokens`, `reasoning_output_tokens`. No cost field is documented. DOC — https://learn.chatgpt.com/docs/non-interactive-mode
    16	- `-o` writes the final message to a file "and still prints it to stdout"; docs recommend pairing `--json` with `--output-last-message` in CI. DOC — non-interactive-mode; developer-commands.
    17	- `--output-schema`: docs wording is "request a final response that conforms to a JSON Schema" (DOC — non-interactive-mode) and "Codex validates tool output against it" (DOC — developer-commands). SRC: exec only parses the file as JSON (`Failed to read output schema file`, `... is not valid JSON` → exit 1) and sends it as `output_schema` in `TurnStartParams`; core builds Responses `text.format = {type: json_schema, name: "codex_output_schema", strict: output_schema_strict, schema}` (SRC — `codex-rs/codex-api/src/common.rs`), with `Prompt::default().output_schema_strict = true` ("Whether the Responses API should strictly validate `output_schema`", SRC — `codex-rs/core/src/client_common.rs`). So enforcement is server-side strict JSON schema, no local post-validation; whether core ever overrides `strict` to false for incompatible schemas: UNVERIFIED. The `review` path does not use `output_schema`. SRC — exec/src/lib.rs
    18	- Exit codes: no documented table (DOC — developer-commands documents exit codes only for `apply`, `cloud`, `login status`). SRC: exits 1 on config/startup errors, and after the run `if error_seen { std::process::exit(1) }` where `error_seen` is set by a non-retried `Error` notification, a `TurnCompleted` with status `Failed`/`Interrupted`, or a failed server-request response; otherwise 0. SRC — exec/src/lib.rs. An enabled MCP server with `required = true` that fails to start makes exec "exit with an error". DOC — non-interactive-mode
    19	- `resume`: `codex exec resume --last "<prompt>"` or `codex exec resume <SESSION_ID|thread name> [PROMPT]`; `--all` disables cwd filtering. DOC — non-interactive-mode; CLI
    20	- `--ephemeral`: "Run without persisting session files to disk." CLI; DOC — non-interactive-mode
    21	- Auth: reuses CLI login; `CODEX_API_KEY` works for a single run (also for `codex review`); docs warn against job-level API keys in workflows running repo-controlled code, and against ChatGPT `auth.json` in public repos. DOC — non-interactive-mode
    22	
    23	## 2. `codex review`
    24	
    25	- Top-level `codex review [PROMPT]` flags: `--uncommitted` ("staged, unstaged, and untracked"), `--base <BRANCH>`, `--commit <SHA>`, `--title` (requires `--commit`), `-c`, `--enable/--disable`, `--strict-config`. No `-m`, `--json`, `-o`, `--output-schema`, `--sandbox`. CLI; DOC — developer-commands. `--uncommitted`, `--base`, `--commit` and a custom PROMPT "conflict with one another". DOC — developer-commands
    26	- `codex exec review [PROMPT]` additionally accepts `-m`, `--json`, `-o`, `--output-schema`, `--worktree`, `--ephemeral`, `--skip-git-repo-check`, `--ignore-rules`, `--dangerously-bypass-*`. CLI (not in the docs table). `--output-schema` is ignored on the review path (SRC — exec/src/lib.rs). Whether `--json` emits findings as a structured item: UNVERIFIED (not run; would consume quota).
    27	- Output: "Codex reports prioritized findings without modifying your working tree." DOC — https://learn.chatgpt.com/docs/codex/cli.md. Internal structure: `ReviewOutputEvent { findings: Vec<ReviewFinding>, overall_correctness: String, overall_explanation: String, overall_confidence_score: f32 }`, `ReviewFinding { title, body, confidence_score: f32, priority: i32, code_location: { absolute_file_path, line_range { start, end } } }`. SRC — https://raw.githubusercontent.com/openai/codex/rust-v0.161.0/codex-rs/protocol/src/protocol.rs. The P0–P3 definitions come from a server-side review prompt: UNVERIFIED (not in the binary strings or repo at this tag).
    28	- `review_model`: "Optional model override used by `/review` (defaults to the current session model)." DOC — https://learn.chatgpt.com/docs/config-file/config-reference. Applicability to `codex review` CLI: UNVERIFIED.
    29	- `approvals_reviewer = user | auto_review`: "Who reviews eligible approval prompts under `on-request` or granular approval policies"; default `user`; `auto_review` uses a reviewer subagent, does not change sandboxing, "Prompt-build, review-session, and parse failures fail closed", critical-risk actions denied, uses extra model calls. DOC — config-reference; https://learn.chatgpt.com/docs/agent-approvals-security. `--approve-for-me` is the CLI switch (CLI only; not in docs).
    30	
    31	## 3. `config.toml`
    32	
    33	- `approval_policy`: `on-request | never | { granular = { sandbox_approval, rules, mcp_elicitations, request_permissions, skill_approval } }`. "`untrusted` is unsupported" and "can prevent startup"; `on-failure` deprecated ("use `on-request` for interactive runs and `never` for non-interactive runs"). DOC — config-reference; agent-approvals-security
    34	- `sandbox_mode`: `read-only | workspace-write | danger-full-access`. `[sandbox_workspace_write]`: `network_access` ("Allow outbound network access inside the workspace-write sandbox"), `writable_roots` ("Additional writable roots"), `exclude_tmpdir_env_var` (exclude `$TMPDIR`), `exclude_slash_tmp` (exclude `/tmp`). Must not be combined with `default_permissions`/`[permissions]`. DOC — config-reference; https://learn.chatgpt.com/docs/permissions
    35	- `notify = ["cmd", ...]`: invoked "whenever Codex emits supported events (currently only `agent-turn-complete`)"; single JSON argument with `type`, `thread-id`, `turn-id`, `cwd`, `input-messages`, `last-assistant-message`. DOC — https://learn.chatgpt.com/docs/config-file/config-advanced
    36	- `model_reasoning_effort`: "such as `low`, `medium`, `high`, `xhigh`, `max`, or `ultra`"; levels "depend on the model and client"; `plan_mode_reasoning_effort` override. DOC — config-reference
    37	- `[features]`: `hooks` ("Enable lifecycle hooks loaded from `hooks.json` or inline `[hooks]`"; `codex_hooks` deprecated alias), `multi_agent` (on by default), `network_proxy`, `web_search`, etc. DOC — config-reference. Installed: `hooks stable true`, `multi_agent stable true`, `multi_agent_v2 stable false`, `network_proxy experimental false`. CLI (`codex features list`)
    38	- `[hooks]`: events `PreToolUse`, `PermissionRequest`, `PostToolUse`, `PreCompact`, `PostCompact`, `SessionStart`, `SessionEnd`, `SubagentStart`, `SubagentStop`, `UserPromptSubmit`, `Stop`, `Interrupt`. Handler types `command`, `mcp_tool` (`prompt`/`agent` parsed but skipped); `timeout` seconds (default 600; `SessionEnd`/`Interrupt` default 1, max 3); `async` (background, cannot block); `additionalContextLimit` default 2500. Sources: `~/.codex/hooks.json`, `~/.codex/config.toml`, `<repo>/.codex/hooks.json`, `<repo>/.codex/config.toml` (project hooks only when the project `.codex/` layer is trusted), plugins, managed `requirements.toml`. Non-managed hooks "must be reviewed and trusted"; trust is per hash, "new or changed hooks are marked for review and skipped until trusted"; `--dangerously-bypass-hook-trust` skips that for one invocation. DOC — https://learn.chatgpt.com/docs/hooks
    39	- Hook input: common `session_id`, `transcript_path`, `cwd`, `hook_event_name`, `model`, `permission_mode`; `PreToolUse`/`PostToolUse`: `turn_id`, `tool_name` (`Bash`, `apply_patch` with `Edit`/`Write` aliases, MCP names), `tool_use_id`, `tool_input` (`tool_input.command` for Bash), `tool_response`; `PermissionRequest`: `tool_name`, `tool_input(.description)`; `Stop`/`SubagentStop`: `stop_hook_active`, `last_assistant_message` (+ `agent_id`, `agent_type`, `agent_transcript_path`); `UserPromptSubmit`: `prompt`; `SessionStart`: `source` (`startup|resume|clear|compact`); `SessionEnd`: `reason`. DOC — hooks
    40	- Hook semantics: exit 0 no output = continue; exit 2 + stderr reason blocks for `PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `SubagentStop`, `Stop`. `PreToolUse`: `hookSpecificOutput.permissionDecision: "deny"|"allow"` (+`updatedInput`); `"ask"` unsupported (hook fails, tool call continues). `PermissionRequest`: `hookSpecificOutput.decision.behavior: "allow"|"deny"`, "any `deny` wins", no decision → normal prompt. `Stop`: `decision: "block"` "doesn't reject the turn" but injects a continuation prompt; `continue: false` wins. `SessionEnd` advisory only. `Interrupt` cannot be prevented. DOC — hooks. Whether hooks fire under `codex exec`: UNVERIFIED (docs silent; the only evidence is that `codex exec` exposes `--dangerously-bypass-hook-trust`).
    41	- `[agents]`: `enabled` (default true), `max_concurrent_threads_per_session` (`max_threads` legacy alias; default not documented), `default_subagent_model`, `default_subagent_reasoning_effort`, `interrupt_message`; roles as `agents.<name>` with `config_file`/`description` (DOC — config-reference) or standalone TOML in `~/.codex/agents/`/`.codex/agents/` with `name`, `description`, `developer_instructions`, optional `sandbox_mode` (DOC — https://learn.chatgpt.com/docs/agent-configuration/subagents.md). `max_depth`: UNVERIFIED (not in either page).
    42	- Profiles: `$CODEX_HOME/<name>.config.toml` layered by `--profile`; "In Codex 0.134.0 and later, `--profile` no longer reads `[profiles.profile-name]`"; project `.codex/config.toml` cannot set `profile`. DOC — config-advanced; config-reference
    43	- Rules: `rules/*.rules` next to each active config layer (`~/.codex/rules/default.rules`; `<repo>/.codex/rules/` only when trusted); Starlark `prefix_rule(pattern=[...], decision="allow"|"prompt"|"forbidden", justification, match, not_match)`; strictest wins; `allow` runs the command outside the sandbox without prompting; test with `codex execpolicy check --pretty --rules <file> -- <cmd>`. DOC — https://learn.chatgpt.com/docs/agent-configuration/rules. `--ignore-rules` skips user and project rules. CLI
    44	- `project_doc_max_bytes`: "Maximum bytes read from `AGENTS.md`", default 32 KiB; discovery `~/.codex/AGENTS.override.md|AGENTS.md`, then project root down to cwd, one file per directory, concatenated root-first, nearer files later. DOC — https://learn.chatgpt.com/docs/agent-configuration/agents-md.md
    45	- `shell_environment_policy`: `inherit = all|core|none`, `filters` (include/exclude patterns), `set`, `ignore_default_excludes` ("Keep variables containing KEY, SECRET, or TOKEN before other filters run (default: true)"), `experimental_use_profile`. DOC — config-reference
    46	- `projects.<path>.trust_level = "trusted"|"untrusted"`; "Untrusted projects skip project-scoped `.codex/` layers, including project-local config, hooks, and rules." DOC — config-reference
    47	- `history.persistence = save-all|none`, `history.max_bytes`; `log_dir` (default `$CODEX_HOME/log`); `sqlite_home`. DOC — config-reference
    48	
    49	## 4. GitHub "Codex" review bot
    50	
    51	- Triggers: `@codex review` comment (Codex reacts 👀 then posts a review); `@codex review for <focus>`; `@codex security review`; Automatic review per repository ("Review code" setting, needs GitHub push/admin) and per user ("Personal preferences", "Choose timing with Review trigger" — options not enumerated). Any other `@codex ...` (e.g. `@codex fix the P1 issue`) "starts a legacy cloud chat with the pull request as context"; Codex "can push a fix back to the branch when it has permission". DOC — https://learn.chatgpt.com/docs/third-party/github.md
    52	- Output: "a standard GitHub code review focused on serious issues"; "In GitHub, Codex flags only P0 and P1 issues"; the example shows a `[P1]` label on a line-anchored comment. Inline vs summary layout and P2/P3 handling: not documented. DOC — third-party/github.md
    53	- `AGENTS.md`: Codex "searches your repository for `AGENTS.md` files and follows the applicable code review rules"; put a `## Code Review Rules` section (`###` groups) in the file closest to the governed code; root = repo-wide, nested = service-specific; "applies the root and more-specific guidance that covers each changed file"; keep lint/format to CI. DOC — third-party/github.md; https://learn.chatgpt.com/use-cases/github-code-reviews
    54	- Quota: "Code Review usage applies only when Codex runs reviews through GitHub. Reviews run locally or outside of GitHub count toward your general usage limits." DOC — https://learn.chatgpt.com/docs/pricing.md. Numeric review quotas: UNVERIFIED.
    55	- Re-review on every push, hidden-directory (`.orchestration/`) coverage, draft PRs, and requesting a review of a specific commit: UNVERIFIED (not in any official page; only GitLab documents "On every push").
    56	
    57	## 5. Session logs and usage
    58	
    59	- State root: `CODEX_HOME` (default `~/.codex`); `history.jsonl` when persistence enabled; logs under `log_dir` (default `$CODEX_HOME/log`). DOC — config-advanced; config-reference. `--ephemeral` skips "session rollout files". DOC — non-interactive-mode
    60	- No official page names `~/.codex/sessions` (hooks input `transcript_path` is the only official acknowledgment of a per-session transcript file, DOC — hooks). LOCAL: rollouts live at `~/.codex/sessions/YYYY/MM/DD/rollout-<ts>-<uuid>.jsonl` plus `session_index.jsonl` and `logs_2.sqlite`/`state_5.sqlite`; `codex migrate-rollouts` "migrate[s] legacy local sessions to paginated thread history" (CLI), i.e. the on-disk format is in transition (`ThreadHistoryMode legacy|paginated` strings in the binary).
    61	- Per-turn usage is recorded: LOCAL rollout lines `event_msg`/`token_count` carry `info.total_token_usage` and `info.last_token_usage` (`input_tokens`, `cached_input_tokens`, `cache_write_input_tokens`, `output_tokens`, `reasoning_output_tokens`, `total_tokens`), `model_context_window`, and `rate_limits` (`primary.used_percent`, `window_minutes` (10080 observed), `resets_at`, `credits.balance`, `plan_type`). Field names match SRC `TokenCountEvent { info: Option<TokenUsageInfo>, rate_limits: Option<RateLimitSnapshot> }`, `RateLimitWindow { used_percent, window_minutes, resets_at }`. SRC — protocol.rs
    62	- From a finished `codex exec --json` run, read `turn.completed.usage` (tokens only; no cost, no rate-limit snapshot documented). DOC — non-interactive-mode. In the TUI, `/status` and `/usage` show limits and token activity. DOC — developer-commands
    63	
    64	## 6. Sandbox
    65	
    66	- macOS "uses Seatbelt policies and runs commands using `sandbox-exec`"; "Linux uses `bwrap` plus `seccomp` by default" (Landlock not mentioned; moved to bwrap in 0.115; WSL1 unsupported); Windows MXC. If the platform sandbox cannot enforce the policy, Codex "refuses to run the command instead of silently running it unsandboxed". DOC — agent-approvals-security; permissions
    67	- workspace-write: "Defaults include no network access and write permissions limited to the active workspace"; workspace = cwd plus "temporary directories like `/tmp`" (`$TMPDIR` via `:tmpdir` in permissions profiles); network only with `[sandbox_workspace_write] network_access = true`. DOC — agent-approvals-security; permissions. Network in read-only mode: UNVERIFIED (docs state only that network is off by default and `:read-only` "keeps local command execution read-only").
    68	- Protected paths inside writable roots: "`<writable_root>/.git` is protected as read-only whether it appears as a directory or file"; for a `gitdir:` pointer file "the resolved directory is also protected"; `.codex` and `.agents` directories likewise; "Protection is recursive". DOC — agent-approvals-security. So in workspace-write, neither a worktree's `.git` file nor its resolved per-worktree gitdir is writable; whether the shared _common_ dir (`commondir`) is also protected: UNVERIFIED.
    69	- `danger-full-access`: no sandbox, no approvals; `--dangerously-bypass-approvals-and-sandbox` (`--yolo`) also skips the git check. DOC — agent-approvals-security; SRC — exec/src/lib.rs
    70	- Worktrees: `--worktree` on `codex exec`/`review` runs "in a new managed Git worktree" (CLI); `codex exec` in an existing worktree directory needing `--skip-git-repo-check`: UNVERIFIED.
    71	
    72	## 7. Rate limits, cost, effort
    73	
    74	- ChatGPT sign-in: usage draws on the plan's allowance; Plus $20, Pro $100/$200/$500; "Pro plans currently have no five-hour limit"; Plus/Standard Business message estimates are "per five-hour period" and "Weekly limits may also apply"; Plus/Pro can buy credits. API key: "Pay for Codex usage based on API pricing"; models "follow the API models available to your key". DOC — https://learn.chatgpt.com/docs/pricing.md
    75	- Credit rates per 1M tokens (input/cached/output): GPT-6 Astra 250/25/1,250; GPT-6.1 Sol 50/2.5/250; GPT-6 Luna 2.5/0.25/12.5; Fast 2.5x, Ultrafast 8x of included usage. DOC — pricing.md
    76	- `help.openai.com/en/articles/11369540` could not be fetched (JS wall/403): help-center specifics UNVERIFIED.
    77	- Effort: config names `low|medium|high|xhigh|max|ultra`; models page calls them Light/Medium/High/Extra High/Max/Ultra; "Higher reasoning effort can improve results for complex tasks, but it takes longer and uses more tokens"; "Most tasks do not need Max or Ultra"; Ultra "uses subagents"; Luna supports up to Max; some paid plans omit Extra High on Astra. No quantitative xhigh cost/latency guidance exists. DOC — https://learn.chatgpt.com/docs/models.md
    78	
    79	## 8. Multi-agent guidance
    80	
    81	- Subagents are on by default; orchestration (spawn, route follow-ups, wait, close) is handled by Codex; "Subagents inherit your current sandbox policy"; a custom agent file may set `sandbox_mode`; in the CLI the parent's live overrides (`/permissions`, `--yolo`) are reapplied to children; "In non-interactive flows ... an action that needs new approval fails and Codex surfaces the error back to the parent workflow"; subagent runs "consume more tokens"; recommended for read-heavy parallel work, caution for parallel writes. DOC — https://learn.chatgpt.com/docs/agent-configuration/subagents.md
    82	- Collaboration tools listed under `features.multi_agent`: `spawn_agent`, `send_input`, `resume_agent`, `wait_agent`, `close_agent`. DOC — config-reference
    83	- Codex Cloud: "Each task has its own workspace and can keep working while your computer is asleep"; tasks start from a published environment; `codex cloud exec --env --attempts 1–4`, `codex cloud list --json`; "Cloud tasks may use more of your allowance than local messages". DOC — https://learn.chatgpt.com/docs/cloud; developer-commands; pricing.md
FILE .orchestration/validation/dotfiles-T128-regime-v3-a01-research/github-factsheet.md
     1	# GitHub merge-gate mechanics for a user-owned repo (facts as of 2026-10-11)
     2	
     3	Sources: docs.github.com, cli.github.com/manual, github.blog changelog, docs.coderabbit.ai, learn.chatgpt.com (redirect target of developers.openai.com/codex). "UNVERIFIED" = no fetched official page states it.
     4	
     5	## 1. Rulesets on a personal repository
     6	
     7	- Repo-level ruleset rules: require PR; required approvals; dismiss stale approvals; code-owner review; "Require approval of the most recent reviewable push"; conversation resolution; merge method; required status checks (strict/loose, app source); require deployments; code scanning; code quality; signed commits; linear history; restrict creations/updates/deletions; block force pushes; file path/size/extension limits. — https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets
     8	- Only rule explicitly denied to user-owned repos: team-based required reviewers — "This rule is not available on user-owned repositories as they do not contain teams." — same URL.
     9	- "Require merge queue" and "Require deployments to succeed" are repo-level rules: "This rule is not available for rulesets created at the organization level." (restriction on org-level, not on user-owned). — https://docs.github.com/en/enterprise-cloud@latest/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets
    10	- Required workflows: "Ruleset workflows can be configured at the organization or enterprise level"; supported events `pull_request`, `pull_request_target`, `merge_group`, "Any filters you specify for the supported events are ignored"; "Applying this rule will block direct pushes." — same enterprise-cloud URL. Changelog: requiring a workflow "will only be available on GitHub Enterprise plans via Repository Rules"; old Actions Required Workflows removed "On October 18th" (2023). — https://github.blog/changelog/2023-08-02-github-actions-required-workflows-will-move-to-repository-rules/ . No page mentions user-owned repos (explicit denial UNVERIFIED).
    11	- Merge queue availability: "Merge queue is available on private and public repos on the GitHub Enterprise Cloud plan" and "all public repos owned by organizations". No page mentions user-owned repos. — https://github.blog/changelog/2023-07-12-pull-request-merge-queue-is-now-generally-available/
    12	- Ruleset plan gating for a private personal repo: UNVERIFIED. Plans page lists "Protected branches", "Code owners", "Required pull request reviewers" under Pro "in private repositories"; Free lists only "Deployment protection rules for public repositories". — https://docs.github.com/en/get-started/learning-about-github/githubs-plans
    13	- Bypass actors: "Repository admins, organization owners, and enterprise owners", maintain/write roles, teams, GitHub Apps, Dependabot; modes "Always allow" / "For pull requests only". — https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository . REST `bypass_actors[].actor_type`: Integration, OrganizationAdmin, RepositoryRole, Team, DeployKey, User; `bypass_mode`: always, pull_request, exempt. — https://docs.github.com/en/rest/repos/rules
    14	- Tamper ceiling: repo admins edit repo rulesets; only org-level rulesets are locked ("only owners of the organization can edit the ruleset"). — https://docs.github.com/en/organizations/managing-organization-settings/creating-rulesets-for-repositories-in-your-organization
    15	- Self-approval: "Pull request authors cannot approve their own pull requests." — https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/approving-a-pull-request-with-required-reviews . Personal-account default: "workflows are not allowed to create or approve pull requests." — https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository . Copilot default review is "Comment"; approvals are public preview, "off by default". — https://docs.github.com/en/copilot/how-tos/use-copilot-agents/request-a-code-review/use-code-review . Consequence: with one write account, approval count >= 1, code-owner review and last-push approval are unsatisfiable without bypass.
    16	- Code owners "must have write permissions for the repository". — https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
    17	- Signed commits: unsigned head commits can block even a signed squash; linear history needs squash/rebase enabled; block force pushes and restrict deletions are on by default. — available-rules URL above.
    18	
    19	## 2. Trust model of status checks
    20	
    21	- `pull_request_target` "runs in the context of the default branch of the base repository, rather than in the context of the merge commit"; "This prevents execution of unsafe code from the head of the pull request that could alter your repository"; "Running untrusted code on the `pull_request_target` trigger may lead to security vulnerabilities." `pull_request`: `GITHUB_SHA` "is the last merge commit of the pull request merge branch" (that `pull_request` runs the PR-side workflow file is an inference from these contrasting statements plus the fork-approval page; no page states it directly). — https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows
    22	- Fork PR approval doc: review proposed changes "especially to `.github/workflows/`" before approving a run. — https://docs.github.com/en/actions/managing-workflow-runs-and-deployments/managing-workflow-runs/approving-workflow-runs-from-public-forks
    23	- `pull_request_target`/`workflow_run` "may have repository write access and access to referenced secrets"; they "must not explicitly check out untrusted code, including from pull request forks". "Pinning an action to a full-length commit SHA is currently the only way to use an action as an immutable release." Add the workflows dir to CODEOWNERS so changes "will first require approval". — https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions
    24	- `workflow_run`: "This event will only trigger a workflow run if the workflow file exists on the default branch"; "able to access secrets and write tokens, even if the previous workflow was not"; `GITHUB_SHA` = "Last commit on default branch". — events URL above.
    25	- Required-check eligibility: workflow-job checks count only when the run "must be triggered by one of these events": push, pull_request, pull_request_review, pull_request_target, deployment, deployment_status; `workflow_run` and `workflow_dispatch` are not listed (`workflow_dispatch` checks "do not appear in the pull request's checks section"); merge queue needs `merge_group`; this "restriction applies only to checks created by workflow jobs, not to checks created by an external GitHub App". Error text: "Required status check "build" was not set by the expected GitHub App." — https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/troubleshooting-required-status-checks
    26	- App source: "you can select an app as the expected source of status updates"; app needs `statuses:write` and a recent check run. — available-rules URL. REST ruleset `required_status_checks[].integration_id`: "The optional integration ID that this status check must originate from." — https://docs.github.com/en/rest/repos/rules . Branch protection `checks[].app_id`: "Pass -1 to explicitly allow any app to set the status." — https://docs.github.com/en/rest/branches/branch-protection . Note: a PR-edited and a base-branch workflow both report through the same GitHub Actions app, so app-source pinning does not distinguish them (inference from the above; no page states it).
    27	- Reusable workflows: `{owner}/{repo}/.github/workflows/{filename}@{ref}`, "the `{ref}` can be a SHA, a release tag, or a branch name"; "Using the commit SHA is the safest option"; local `./` reference "is from the same commit as the caller workflow". — https://docs.github.com/en/actions/sharing-automations/reusing-workflows
    28	- Environments: "Users with GitHub Free plans can only configure environments for public repositories"; Pro covers private; required reviewers "up to 6 people or teams"; option "to prevent users from approving workflows runs that they triggered". — https://docs.github.com/en/actions/managing-workflow-runs-and-deployments/managing-deployments/managing-environments-for-deployment
    29	- CODEOWNERS enforced only with "Require review from Code Owners"; sole owner = PR author (see self-approval). — about-code-owners URL.
    30	- User-owned availability: pull_request_target, workflow_run, reusable workflows, app-source checks, CODEOWNERS: no restriction stated; environments: public only on Free; required workflows: org/enterprise only.
    31	
    32	## 3. gh CLI and API surfaces
    33	
    34	- `gh pr merge --match-head-commit <SHA>`: "Commit SHA that the pull request head must match to allow merge"; `--auto`: "Automatically merge only after necessary requirements are met"; `--admin`: "Use administrator privileges to merge a pull request that does not meet requirements"; on a branch requiring a merge queue, if checks have not passed "auto-merge will be enabled", else the PR is added to the queue. — https://cli.github.com/manual/gh_pr_merge
    35	- `gh pr update-branch`: "The default behavior is to update with a merge commit"; `--rebase` to rebase. — https://cli.github.com/manual/gh_pr_update-branch
    36	- `gh pr checks`: `--watch`, `--fail-fast`, `--required`, `--interval` (default 10); exit code "8: Checks pending"; JSON `bucket` in pass/fail/pending/skipping/cancel. — https://cli.github.com/manual/gh_pr_checks
    37	- `gh pr review --approve|--request-changes|--comment`; manual silent on self-approval (server rule above applies). — https://cli.github.com/manual/gh_pr_review
    38	- `gh api --paginate` ("Make additional HTTP requests to fetch all pages"), `--slurp`, `--jq`; GraphQL via endpoint `graphql`; `--paginate` with GraphQL "requires that the original query accepts an `$endCursor: String` variable". — https://cli.github.com/manual/gh_api
    39	- Check runs: `GET /repos/{owner}/{repo}/commits/{ref}/check-runs` (per_page default 30, max 100; `check_name`, `status`, `filter=latest|all`, `app_id`); `GET .../check-runs/{id}/annotations` (default 30, max 100); `annotation_level`: `notice`, `warning`, `failure`; "maximum of 50 per API request", appended on update; create/update "only available to GitHub Apps"; Actions "limited to 10 warning and 10 error annotations per step". — https://docs.github.com/en/rest/checks/runs ; "For most endpoints, the maximum value of `per_page` is `100`." — https://docs.github.com/en/rest/using-the-rest-api/using-pagination-in-the-rest-api
    40	- GraphQL `resolveReviewThread(input: {threadId: ID!})` "Marks a review thread as resolved."; `unresolveReviewThread` likewise; `PullRequestReviewThread.isResolved`, `resolvedBy`, `viewerCanResolve`. — https://docs.github.com/en/graphql/reference/pulls
    41	
    42	## 4. Branch protection vs rulesets; up-to-date; auto-merge; skipped checks
    43	
    44	- Both can apply; "all applicable rules are enforced"; "the most restrictive version of the rule applies"; "A ruleset does not have a priority." — https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets
    45	- Classic protection: by default "don't apply to people with admin permissions" unless "Do not allow bypassing the above settings"; strict = "The branch **must** be up to date with the base branch before merging"; required checks need `successful`, `skipped`, or `neutral`. — https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/about-protected-branches ; REST `strict_required_status_checks_policy`: "Whether pull requests targeting a matching branch must be tested with the latest code." — rest/repos/rules URL
    46	- Squash + up-to-date: no page addresses squash specifically (UNVERIFIED). Merge queue intro: provides the benefit of up-to-date but "does not require a pull request author to update their pull request branch and wait for status checks". — managing-a-merge-queue URL
    47	- Auto-merge: "merges a pull request automatically after all required reviews and status checks pass"; "disabled if someone without write permissions pushes new changes to the head branch or switches the base branch"; must be enabled per repository. — https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/automatically-merging-a-pull-request
    48	- Skipped required checks: path/branch/commit-message skips "stay in a "Pending" state and block merging" ("Waiting for status to be reported"); guidance "Avoid requiring workflows that can be skipped."; `if`-skipped job "reports "Success""; job after failed dependency "is skipped and may not block merging" -> use `always()` with `needs`; "If a check and a commit status have the same name, both must pass". The current cloud page has no duplicate-workflow/`paths-ignore` example. — troubleshooting URL above
    49	- Checks are evaluated on the test merge commit when it has a status, else on the head commit. — troubleshooting URL
    50	
    51	## 5. GitHub Actions mechanics
    52	
    53	- Concurrency: "at most one running job or workflow in a concurrency group at any time"; `cancel-in-progress: true`; "Up to 100 jobs or workflow runs can be `pending`"; `group: ${{ github.head_ref || github.run_id }}`. — https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/control-the-concurrency-of-workflows-and-jobs
    54	- OIDC: provider "issues a short-lived access token that is only valid for a single job"; claims `sub`, `repository`, `ref`, `environment`, `job_workflow_ref` (e.g. `octo-org/octo-automation/.github/workflows/oidc.yml@refs/heads/main`). — https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect
    55	- Attestations: "cryptographically signed claims that establish your build's provenance"; public repos use Sigstore Public Good with transparency log, private use GitHub's Sigstore instance; "SLSA v1.0 Build Level 2". — https://docs.github.com/en/actions/concepts/security/artifact-attestations . How-to uses `actions/attest@v4` with `permissions: id-token: write, contents: read, attestations: write`; verify with `gh attestation verify PATH -R OWNER/REPO`. — https://docs.github.com/en/actions/security-for-github-actions/using-artifact-attestations/using-artifact-attestations-to-establish-provenance-for-builds . GA changelog used `actions/attest-build-provenance@v1`; "supports both public and private repositories". — https://github.blog/changelog/2024-06-25-artifact-attestations-is-generally-available/ . Private-repo plan gating: UNVERIFIED.
    56	- Annotations: `::error file={name},line={line},endLine={endLine},title={title}::{message}` (also `::warning`, `::notice`); `GITHUB_STEP_SUMMARY` "maximum size of 1MiB" per step, "A maximum of 20 job summaries from steps are displayed per job." — https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/workflow-commands-for-github-actions
    57	- `GITHUB_TOKEN` defaults for personal-account repos: "only has read access for the `contents` and `packages` scopes"; "workflows are not allowed to create or approve pull requests"; fork approval: "By default, all first-time contributors require approval". — managing-github-actions-settings URL . "events triggered by the `GITHUB_TOKEN` will not create a new workflow run." — https://docs.github.com/en/actions/concepts/security/github_token . Scopes include `checks`, `statuses`, `pull-requests`, `id-token`, `attestations`; "If you specify the access for any of these permissions, all of those that are not specified are set to `none`." Fork PRs: "The `GITHUB_TOKEN` has read-only permissions in pull requests from forked repositories." — https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax ; events URL
    58	- Reading another PR's checks: check-runs listing is a read endpoint ("OAuth apps and authenticated users can view check runs"); a job with `checks: read` can query it (combination of two docs; no single page states it).
    59	
    60	## 6. Bots
    61	
    62	- Codex (OpenAI): trigger with `@codex review` in a PR comment; "Codex flags only P0 and P1 issues"; "posts a standard GitHub code review"; automatic review via Codex settings ("GitHub push or admin permission for its settings"); `## Code Review Rules` in nearest `AGENTS.md`; follow-up e.g. "@codex fix the P1 issue". Rate limits and approve/request-changes behaviour: UNVERIFIED. — https://learn.chatgpt.com/docs/third-party/github (redirect target of https://developers.openai.com/codex/integrations/github); https://developers.openai.com/codex/use-cases/github-code-reviews
    63	- CodeRabbit: limits "enforced **per developer** over rolling time windows"; PR reviews/hour: Free 1 (summary only), OSS 1–10, Essentials 5, Team 8, Advanced 10, Enterprise 12; files/review 150–300; "Open-source projects receive Team features". — https://docs.coderabbit.ai/management/plans . "CodeRabbit reviews pushes, not commits"; default "an incremental review on every push, and a pause after five reviewed commits"; rate-limited push posts check "Review rate limited" that passes "so it never blocks merging on protected branches"; `@coderabbitai rate limit`, `@coderabbitai review`. — https://docs.coderabbit.ai/management/rate-limits . `@coderabbitai review` = "incremental review of new changes only"; `@coderabbitai full review` = "complete review of all files from scratch"; `@coderabbitai resolve` "Marks all CodeRabbit review comments as resolved." — https://docs.coderabbit.ai/reference/review-commands
    64	- Copilot code review: `gh pr edit PR-NUMBER --add-reviewer @copilot`, `gh pr create --reviewer @copilot`, REST reviewer `copilot-pull-request-reviewer[bot]`; default "Copilot leaves a "Comment" review"; approvals public preview, dismissed on new commits; re-review only on request unless "Review new pushes" ruleset; "Copilot may repeat the same comments". — use-code-review URL . Plans: automatic reviews "available on the Copilot Pro, Copilot Pro+, and Copilot Max plans" or Business/Enterprise license; "Copilot Free plan, which does not include Copilot code review"; "In personal repositories, only the repository owner or a direct collaborator can request a review."; billed in AI credits; no per-review quota stated. — https://docs.github.com/en/copilot/concepts/agents/code-review
    65	
    66	## 7. PR size
    67	
    68	- Only official guidance: "Write small pull requests" — "Small, focused pull requests are easier to review and safer to merge."; "When a change grows large, consider splitting it into smaller pull requests that each serve one purpose." No numeric limit. — https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/getting-started/best-practices-for-pull-requests
    69	- No github.blog PR-size research found.
FILE .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review.md
     1	---
     2	reviewed_at: 2026-10-10T21:15:46Z
     3	reviewer: claude-review-dot-a001
     4	profile: review
     5	session: 2089b04f-f9c7-498b-86c5-76f2140048d5
     6	design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@b91e8bb407e1019196eade22604fac30801bfce173a95416e9176ca8917b352f
     7	design_hash_kind: whole-file sha256 (the canonical hash tool is V1's deliverable)
     8	task: dotfiles-T128-design-review-a01
     9	round: 1
    10	---
    11	
    12	# Design review: dotfiles-T128-regime-v3-a01, round 1
    13	
    14	Reviewed from a fresh context seated at .claude/worktrees/worker-d, every path read in the main checkout at main d29ce4c1. Read: the design, baseline.md, practice-evidence.md, method-draft.md, the three fact sheets, T126, T124, both reset records, require-crit-review.py, agent-stop-gate.sh, check-regime-boundary.sh, pr-feedback.py, test.yaml, the --audit path of executable_herdr-agents, .claude/settings.json, the file lists of origin/feat/task-validator (52bb69fc) and origin/feat/audit-grammar (9fc521fe). Re-ran: premises 1, 3, 6 and the history counts for T124 W1, T124 W3b and T119. Fetched: the Claude Code headless, hooks and best-practices pages, the Codex hooks page, GitHub's troubleshooting-required-status-checks and events-that-trigger-workflows pages. Not verified: the live ruleset (gh api failed on TLS inside the sandbox and the task forbids an out-of-sandbox read); the Bot P1 head count on PR 314; the per-message usage format of session transcripts.
    15	
    16	## 1. Invariants
    17	
    18	INV-1: rejected: the CI job has no input. The task file is orchestrator-authored, lives untracked in the main checkout until the boundary commit, and INV-8 puts only worker evidence on the branch; at PR time the implementing task file is on neither the base nor the head, so "validates every task file the PR adds or changes" validates nothing for the PR it governs. Right: the AGMSG-TASK carries task_sha256=; the worker's first commit copies the task file to .orchestration/<task id>/task.md; the regime job validates that copy against main's schemas/task.json; the host gate compares its sha256 with the token in history. Also: the regime check only binds once the ruleset lists it as required; name that operator action in V1's acceptance record.
    19	
    20	INV-2: rejected: the wave table breaks the rule it implements. "One task invariant per PR": V1 carries INV-1 and INV-2, V3 carries INV-3, INV-4, INV-6 and INV-10, V5 carries INV-8 and INV-9 (design lines 142-146). Either the unit is "one implementing task's declared invariant set" (then say so and the CI check compares the PR's task.md invariant ids with the design's implementing_tasks entry), or V3 and V5 split. Second gap: the seven required checks of test.yaml run on pull_request (test.yaml:11), so a PR still edits the workflow that runs INV-12's unit tests (R8 stays open there); the regime job should refuse a PR that changes .github/workflows/** unless its task.md is design tier and lists the file.
    21	
    22	INV-3: rejected: "fails on the previous head" and "the fix turns green" are not gate-checkable; the gate cannot run tests on an earlier head. Mechanical core: the ACCEPTANCE status=revise carries check=<tests/...::name | ci:<job> | repro:<id>>; the RESULT's validation file carries the same id with pasted output; the regime job verifies the named test exists on the head and differs from the previous RESULT head (git diff <prev head> <head> -- <test file> non-empty). State that; the rest is the worker's evidence.
    23	
    24	INV-4: rejected: internally inconsistent. "the orchestrator may amend once" allows one amendment; "a third amendment withdraws" allows two; INV-6 and section 7 say two. Fix the count once (INV-6 is the counter, INV-4 the trigger). Second: "counted from AGMSG-TASK amendment= messages" is the relabel path INV-12 names; count every AGMSG-TASK for the task_id after the first (history: T124 W1 10 TASK sends, 8 with amendment=; W3b 10 and 5; T119 10 and 8). Third: "withdraws the task to design" names no enforcement point; it is INV-6's Stop block and merge backstop, so say so.
    25	
    26	INV-5: rejected: (a) the gate today takes the verdict by regex from the .last.md companion (require-crit-review.py:30-31, 638-665) and accepts not-applicable for every finding whatever its category (require-crit-review.py:698-710); replacing that with the schema JSON, the AGMSG-AUDIT sha256 lookup and the orchestration/conformance lock is a change to an existing evidence rule, and no wave names it (V2 is runner and schema, V3 the reset backstop, V4 the design-review anchor, V5 accept-task.py). P4's "gains only history-anchored checks; nothing removed except REVIEW_TREE" is false on its own terms, and REVIEW_TREE does not exist on main (it was PR 313's). (b) The AGMSG-AUDIT record names no sending identity; the runner runs on the orchestrator's host, so say honestly that the anchor prevents edits after the record, not fabrication before it, and name the identity. (c) "started automatically when ... the Codex Bot has reviewed the head" has no timeout; the SKILL's 15-minute bot: none rule must carry over or a head the Bot skips stalls stage 3 (Bot re-review per push is UNVERIFIED in codex-factsheet.md:55). (d) "never for an evidence-only revision" conflicts with audit_name_error, which requires the audit sha to prefix HEAD (require-crit-review.py:614-615): an evidence-only commit moves HEAD and the gate refuses the earlier audit. Right: the gate accepts an audit of an earlier head when git diff --quiet <audited> <HEAD> -- . ':!.orchestration' holds; assign it to a wave. (e) "rationale written before the verdict" is a prompt instruction, not a schema property: strict JSON schema does not order generation, and PR 314's schema lists verdict first.
    27	
    28	INV-6: rejected: (a) the loop-time block is soft on both runtimes: Claude's Stop hook has an 8-consecutive-continuation cap that resets on any tool call (hooks page, Stop section), and Codex's decision: block "doesn't reject the turn" but injects a continuation prompt (learn.chatgpt.com/docs/hooks). The merge backstop in the gate is therefore the mandatory point and the Stop hook the early signal; the invariant says the reverse. (b) The Bot count "on two heads" is not computable from the sweep JSON: pr-feedback.py records commit_id on review items only (pr-feedback.py:199) and nothing on review_comment items; the collector change (T124 wave 2a's original_commit_id) is in no wave. (c) The audit count needs the audit JSONs, which are orchestrator files in the main checkout; name the source. (d) The Stop hook runs with timeout 5 and a 3 s history budget (.claude/settings.json; agent-stop-gate.sh:209-212): history counts fit, GitHub counts do not; split the counts by source. (e) "re-dispatch ... is a boundary violation" names no detector; T124 v3 INV-5 had one (a closed-unmerged PR whose task has no reset record; a task over a threshold with no accepted record) in check-regime-boundary.sh; restore it in V3.
    29	
    30	INV-7: accepted. Notes: the canonical hash covers five front-matter keys; sections 4 to 9 (stages, enforcement map, waves, thresholds) are outside it, so the wave table can change after review without a new one; add that to INV-12's gaming paths or hash implementing_tasks together with the wave file list. Bootstrap: this receipt carries a whole-file sha256, so V1's AGMSG-TASK is anchored by that form; V4's gate check must accept both forms for this design or V1 needs a second review.
    31	
    32	INV-8: accepted. Notes: add the task.md copy (INV-1 above); the gate's path rules (feedback_path_error, orchestration_path_error) already fit, because the orchestrator's records stay under .orchestration/validation and acceptance; the "final head" with worker evidence committed is what INV-5 (d) above must handle.
    33	
    34	INV-9: rejected: "whose breach pauses the task for an operator decision" names no mechanism that pauses; the enforcement map puts cost in accept-task.py and the boundary warning, which run after the fact. Say "the acceptance record names the operator decision and the boundary check warns", or name the Stop-hook check with its budget source. Per-message usage in session transcripts is UNVERIFIED in claude-code-factsheet.md:75; the premises block does not cover it.
    35	
    36	INV-10: rejected: the stop gate reads history rows as from, to, body with no timestamp (agent-stop-gate.sh:65), and a push is GitHub state the 5 s hook cannot fetch; neither the 30-minute first push nor the 20-minute idle is computable where INV-10 places them. Right: history.sh timestamps for the TASK time, gh pr view for the first push, both in check-regime-boundary.sh and accept-task.py; the Stop hook can at most read the TASK time once the awk carries the timestamp column.
    37	
    38	INV-11: accepted. Note: permgate records input_hash and no session_id or cwd today (executable_permgate:161, 219), consistent with the design; the sandbox record the gate compares against is the one INV-8 commits on the branch.
    39	
    40	INV-12: accepted. Notes: add the gaming paths this review names (a TASK without amendment=, an evidence-only relabel of a code change, a wave-table rewrite after review, a Bot-skipped head that never starts its audit).
    41	
    42	## 2. Failure modes that still pass (Q2)
    43	
    44	- Amendment accretion (T119, T124 W1, T120): passes while INV-4 counts only amendment= tokens; a plain AGMSG-TASK, a poke or a note carries the same text. INV-4 should catch it by counting every TASK after the first.
    45	- Bespoke parser bypass loop (PR 313): closed for the validator by INV-1 (jsonschema plus PyYAML). Not closed for V2's audit-head.sh and audit-watch.sh and V5's accept-task.py, which are new code at the same boundary; INV-2 bounds their size, not their kind. INV-1's principle (no hand-written parser at a trust boundary) should be stated as a rule the auditor checks per PR.
    46	- Oversized PR (PR 312, 313): closed by INV-2 once regime is a required check; open until the ruleset lists it.
    47	- Waiver instead of reset (PR 313 round 2): open until V3; after V3 the Stop block is soft (INV-6 (a)) and the merge backstop is the catch. INV-6 should name the backstop as mandatory.
    48	- Orchestrator self-disposition (T119 audit-finding 2): passes today and after V2, because audit_disposition_errors accepts not-applicable for any category (require-crit-review.py:698-710) and no wave changes it. INV-5 should catch it; assign the lock to V3 or V5.
    49	- Audit as serial queue (T119): closed by the pool and auto-start in INV-5, subject to the Bot-wait timeout (INV-5 (c)).
    50	
    51	## 3. pull_request_target as the main-pinned check (Q3)
    52	
    53	The discipline is sufficient on a public repository if the job keeps main at the workspace root and never checks out the PR head there. Confirmed: pull_request_target is an eligible event for required checks and an if-skipped job reports Success (troubleshooting page), so the changes pattern transfers; GITHUB_SHA under pull_request_target is the last commit on the default branch (events page), so actions/checkout's default ref is main, and the diff range must come from github.event.pull_request.head.sha against its merge-base with main, not from github.sha as test.yaml:38-48 does. Executable surface, each to be excluded in regime.yml: actions/checkout with ref: head.sha at the root; uv run without --no-project (it reads a PR-controlled pyproject.toml); yaml.load instead of safe_load; make or any script invoked from a PR tree; a dependency file read from the PR. Read PR files as git show <head>:<path> or into a subdirectory never on PATH, with permissions: contents: read and no secrets. One residual the design does not state: a PR that changes regime.yml is checked by main's copy, never its own, so a regime.yml change has no pre-merge exercise; name the way it is tested (a workflow_dispatch dry run or the unit test of its script) before V1 lands. The merge commit is irrelevant here: checks are evaluated on the test merge commit when it has a status, else the head (troubleshooting page).
    54	
    55	## 4. Reset rule and redesign author (Q4)
    56	
    57	Counts: revises should be counted as RESULTs for the task_id minus one (worker-authored; a split round without a revise ACCEPTANCE still produces a RESULT); amendments as TASKs after the first (INV-4); Bot heads need original_commit_id on inline items (INV-6 (b)); audit heads are fine once the JSONs are named. Gaming: split rounds and relabelled amendments are closed by those two counts; re-dispatch under a new id needs the boundary detector (INV-6 (e)); a question answered as a note still counts because the worker's PONG status=question is in history, so the orchestrator cannot suppress it. Bootstrap exception: trust anchor 5 says a reset is released only by another context or the operator; T128 was written by claude-deep-dot, who dispatched the abandoned tasks, and the reset records call it a "bootstrap exception" in prose, which is R5's shape. Bounded only if the records carry the operator form the design itself specifies (DESIGN_RESET_WAIVED_BY with the 2026-10-11 decision), this receipt is the only release, and no further orchestrator-authored design follows under T128. Both reset records name claude-review-dot-a004 as the pre-dispatch reviewer; history holds the TASK to claude-review-dot-a001 (2026-10-10T21:04:16Z); correct the records before they are committed. Dropping the redesign profile: review is claude-fable-5-1 at effort high (agent-config.yaml:41), the same model and effort as deep (agent-config.yaml:44), so the lever is exactly and only a separate context; the evidence supports that (T124 round 1; practice-evidence.md:60, cross-model vs same-model fresh not significant), and T124 v4's xhigh had no measured benefit. Not a loss; state the equality so nobody reads "review profile" as a different model.
    58	
    59	## 5. Ponytail on the waves (Q5)
    60	
    61	Caps: V1 (seven files, schema plus about 80 lines plus workflow) and V2 fit; V3 edits agent-stop-gate.sh, require-crit-review.py, the manifest, its rendered codex-config-managed.toml, validate-task.py and check-regime-boundary.sh, within 15 files but four invariants (INV-2 above); V5's accept-task.py has no size estimate and T125's draft is the risk. Still bespoke where a platform feature or script exists: audit-watch.sh polls CI and the Bot, which gh pr checks --watch plus the SKILL's existing Bot list loop already do; make it a Makefile target around those, not a daemon. design-review.sh and audit-head.sh are thin wrappers and fine at about 100 lines. Salvage the design drops: PR 313's scripts/legacy-task-ids.txt (310 ids, only shrinks) is a simpler grandfather than "format-2 and tier stamping", and its 41 test names in tests/unit/test_validate_task.py are the test ideas; PR 314's scripts/schemas/audit.json already matches INV-5's field set and is named; PR 314's pre-push hardening (evidence staged and installed only once masked; the fallback claude limited to the .orchestration dir and the worktree, PONG of 2026-10-10T12:36:42Z) belongs in V2's runner; PR 313's home/dot_codex/modify_private_redesign.config.toml is correctly dropped with the profile. scripts/lib/ holds only shell today (asset-manifest.sh, github-release.sh, installer-pins.sh), so high_risk_paths.py is a new module, not a move.
    62	
    63	## 6. Audit staging (Q6)
    64	
    65	Stages and tiers are right with one tier error: docs tier is "prose-only allowed_files", which puts the regime's own rule text (home/dot_config/claude/rules/*.md, the SKILL, AGENTS.md) on CI plus Bot with no audit; PR 313 thread 4237594826 raised this exact point. Rule prose the machinery cites belongs in review tier by an explicit list. "Once per RESULT head, never for evidence-only revisions" is safe under the cited literature (2607.24604: bind verifier evidence to the exact code state) only with the tree-equality check of INV-5 (d); without it "evidence-only" is an orchestrator assertion. Input set: add the previous round's audit JSON and the acceptance record's dispositions (MCR-Bench's re-flagging failure, practice-evidence.md:59), and the head's pr-feedback JSON; the permgate window is listed for design tier only, which matches INV-11's coverage. Order the schema so findings precede verdict and keep the reasoning instruction in the prompt (INV-5 (e)).
    66	
    67	## 7. Premises (Q7)
    68	
    69	1. Holds for PyYAML (Makefile:189, 203; agent-assets.yml:35), does not hold as stated for jsonschema: no --with jsonschema exists in Makefile or any workflow; the premise's pasted output names only pyyaml. Unverified, not refuted; V1 adds the dependency and the premise should say so.
    70	2. Holds: the troubleshooting page lists push, pull_request, pull_request_review, pull_request_target, deployment, deployment_status; the events page: "This event runs in the context of the default branch of the base repository", GITHUB_SHA "Last commit on default branch".
    71	3. Holds: codex-cli 0.161.0; codex exec --help lists --output-schema <FILE>; codex exec --full-auto fails with "unexpected argument '--full-auto' found"; codex exec -a never fails with "unexpected argument '-a' found".
    72	4. Holds: headless page: "In bare mode, Claude Code never reads OAuth credentials or the system keychain"; "Without --bare, a -p session runs the hooks in a project's .claude/settings.json"; "the structured output in the structured_output field"; "If the run reaches its --max-budget-usd cap, Claude Code stops the remaining background work".
    73	5. Holds verbatim: "If you've corrected Claude more than twice on the same issue in one session, the context is cluttered with failed approaches. Run /clear and start fresh with a more specific prompt that incorporates what you learned."
    74	6. Holds: the four T119 audit files are dated 11:48, 13:55, 15:52, 17:23 local; history: first TASK 2026-10-09T21:26:24Z, accepted ACCEPTANCE 2026-10-10T08:32:16Z, 11.1 h.
    75	7. Holds for the event list (Stop is listed) and weakens the use made of it: the Codex page says decision: "block" "doesn't reject the turn" and exit 2 writes "the continuation reason"; see INV-6 (a).
    76	
    77	Baseline recount from history.sh dotfiles-conformance "" 5000: T124 W1 TASK 10, amendment= 8, questions 6, RESULTs 2, revises 2; W3b 10, 5, 0, 1, 0; T119 10, 8, 8, 6, 5; all equal to baseline.md. Note for V3: history.sh defaults to 20 rows and silently truncates; a counter must use the storage facade as agent-stop-gate.sh does, or pass a limit.
    78	
    79	## 8. What the design should not do (Q8)
    80	
    81	- Do not place GitHub-sourced counts or push timing in the 5 s Stop hook (INV-6 (d), INV-10); they belong to the gate and the boundary check.
    82	- Do not call the Stop block the enforcement point (INV-6 (a)); it is the early signal.
    83	- Do not promise a budget "pause" without a mechanism (INV-9).
    84	- The 500-added-line cap would have split T116 (+529), T118 (+881) and every later task; defensible, but say that it changes the unit of work, not only the review load.
    85	- Section 10 names scratchpad files (claude-code-capabilities-factsheet.md, codex-fact-sheet.md, github-merge-gates-factsheet.md, evidence-sheet-2026-10-11.md, regime/baseline.md) that are not the repository paths under .orchestration/validation/dotfiles-T128-regime-v3-a01-research/; the receipt must be checkable from the repository, so cite those.
    86	- Section 1 states W3b "Bot P1 on two post-RESULT heads"; the worker's PONG of 2026-10-10T12:36:42Z counted one head at that time, and the second (9fc521fe) is not verifiable from here; the reset record should cite the thread ids.
    87	
    88	## 9. Document findings
    89	
    90	- F1 INV-1 enforcement input (section 1).
    91	- F2 INV-2 wave table versus one invariant per PR; test.yaml stays PR-editable.
    92	- F3 INV-5 gate changes unassigned; category lock absent; Bot-wait timeout; evidence-only head versus audit sha prefix.
    93	- F4 INV-6 soft Stop block on both runtimes; Bot head count not computable; boundary detector dropped.
    94	- F5 INV-4 contradiction and relabel path.
    95	- F6 INV-9 and INV-10 enforcement points not reachable from the Stop hook.
    96	- F7 Reset records name the wrong reviewer identity; bootstrap exception in prose rather than the operator-waiver form.
    97	- F8 Docs tier covers the regime's own rule prose.
    98	- F9 Premise 1 overstates jsonschema availability.
    99	
   100	The direction, the trust anchors and the thresholds are sound and the premises hold where checked; the rejections are enforcement gaps that a second round of this document closes without a new design.
   101	
   102	Design verdict: revise
FILE .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round2.md
     1	---
     2	reviewed_at: 2026-10-10T21:29:22Z
     3	reviewer: claude-review-dot-a001
     4	profile: review
     5	session: 2089b04f-f9c7-498b-86c5-76f2140048d5
     6	design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@61b0a812c699e57c13713057571a5883044039a0414e2fdc3dca7913421e5f85
     7	design_hash_kind: whole-file sha256 (the canonical hash tool is V1's deliverable)
     8	task: dotfiles-T128-design-review-a01
     9	round: 2
    10	previous: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review.md
    11	---
    12	
    13	# Design review: dotfiles-T128-regime-v3-a01, round 2
    14	
    15	Same reviewer, same seat, the design re-read in full at the hash above against the round-1 receipt. Re-ran: premise 1 as restated (uv run --no-project --with jsonschema --with pyyaml: 4.26.0 6.0.3), premise 8 (the named transcript: 5168 usage entries, last one with input_tokens, cache_creation_input_tokens, cache_read_input_tokens, output_tokens), premise 9 (history.sh default 20 rows; the --limit 600 form and the positional "" 600 form both print the whole history, 266 rows at review time). Read both reset records' headers. Fetched the events-that-trigger-workflows page for workflow_dispatch. Not verified: the two Bot thread ids in the W3b reset record (GitHub unreachable from the sandbox); whether history.sh honours --limit as a flag beyond the row count matching the positional form.
    16	
    17	## 1. Round-1 corrections
    18	
    19	Every F1-F9 item and every INV rejection is applied as written: the task.md copy with task_sha256 and the workflow-edit refusal (INV-1, lines 44, 142); the per-task invariant set (INV-2, line 45); check= with the CI existence-and-diff step (INV-3, lines 46, 144); the single amendment count over every TASK and the consistent threshold (INV-4, line 47); the gate changes assigned to V2b, V3a and V4, the 15-minute Bot wait, the tree-equality rule, the audit identity, the schema order and the honest anchor statement (INV-5, line 48; P4, line 116); the merge backstop as the mandatory point, original_commit_id, the audit-JSON source, the hook's history-only counts, the boundary detector (INV-6, line 49); INV-9 and INV-10 out of the Stop hook (lines 52-53); rule prose in the review tier (line 134); premise 1 restated and three premises added (lines 57-59, 75-83); the Q5 salvage list, make audit-head in place of a daemon, the regime.yml discipline (line 188), the test.yaml residual (line 189), the bootstrap stated in the waiver form (line 190). Both reset records now name claude-review-dot-a001 with the TASK timestamp, carry DESIGN_RESET_WAIVED_BY=operator with the scope "T128 design only", and the W3b record cites threads 4237434169 and 4237652017.
    20	
    21	## 2. Invariants
    22	
    23	INV-1: accepted. Note: each amendment changes the task file; say the gate compares the copy with the latest AGMSG-TASK's task_sha256 and that the worker recommits the copy after each amendment.
    24	
    25	INV-2: rejected: "its task.md invariant ids equal the design's implementing_tasks entry for that task" is not computable: implementing_tasks (lines 9-21) is a flat list of task ids with no invariant per entry; the mapping exists only in section 6 prose, outside the hashed keys. Right: implementing_tasks becomes a map {task id: [INV ids]} inside the hashed keys. Second gap: the regime job needs the design file on the runner, and the design is untracked in the main checkout until a boundary commit (git status at review time: untracked). State the precondition: the design reaches main through a boundary PR before the implementing TASK is dispatched and the regime job fails closed when the design named by the task.md copy is absent from main; or copy the design to the branch beside task.md, anchored by the review RESULT's design_sha256= in history.
    26	
    27	INV-3: rejected: it contradicts INV-1. INV-1 anchors the branch copy of task.md to task_sha256= in history (line 44); the INV-3 enforcement row has the worker append a revise: list to that same copy (line 144), so the first revise round breaks the hash the gate checks, and V1 and V3c would ship incompatible rules. Right: the worker's revise list is a sibling file (.orchestration/<task id>/revise.yaml) that the regime job reads; task.md stays byte-identical to the dispatched file.
    28	
    29	INV-4: accepted. Note: the question count now lives in INV-6 without a threshold (below).
    30	
    31	INV-5: accepted. Note: section 4's paragraph (line 136) still says stage 3 "starts without the orchestrator" while the table (line 131) starts it with make audit-head; say the orchestrator runs it on RESULT arrival and that the pool, once-per-head and tree-equality rules are what remove the queue.
    32	
    33	INV-6: rejected: "PONG status=question" is listed among the history counts (line 49) with no threshold in INV-6 or section 7 (line 175); v1 had "a second question". Right: state 2, or say questions count only through the TASKs that answer them and remove the item. Note: the audit-heads count reads .orchestration/validation/<task>-audit-<sha7>.json from the main checkout; require the JSON's sha256 to match its AGMSG-AUDIT record before counting, as INV-5 does for the verdict, or the orchestrator can edit a finding away.
    34	
    35	INV-7: accepted. Fixing INV-2 and INV-3 changes hashed keys, so INV-7 itself requires a round 3; it can be a diff confirmation.
    36	
    37	INV-8: accepted. Note: the revise.yaml of INV-3 lands under the same directory.
    38	
    39	INV-9: accepted. Premise 8 holds as re-run.
    40	
    41	INV-10: accepted.
    42	
    43	INV-11: accepted.
    44	
    45	INV-12: accepted. Note: add "a revise list appended to the hashed task.md" to the gaming paths once INV-3 is fixed.
    46	
    47	## 3. New in v2 that reopens a finding
    48	
    49	- Routing (F2's companion). V3b (line 163) is "Claude seat" and edits agent-stop-gate.sh, Claude's own Stop hook source; P10 (line 122) routes a Claude-boundary source to a Codex seat, and the SKILL names the auto-mode classifier's refusal of such a change on a Claude seat. V3a (line 162) puts the same file, the Codex Stop entry and the gate in one PR, three boundaries, which makes it an operator PR by construction; say so instead of "Claude seat for that part". V3a and V3b both implement the early-signal counts in agent-stop-gate.sh; assign the hook counting once (V3a) and leave V3b the schema, validator and SKILL text. V3c (line 164) is "Claude seat" and edits "the gate's validation-file line" in require-crit-review.py, an operator-routed source under P10; move that line to V2b or route V3c to the operator.
    50	- Caps (F2). V1 (line 158) carries scripts/legacy-task-ids.txt at 310 lines outside tests/, plus the schema, validator, module and workflow, which is over INV-2's 500 added lines. Round 1 recommended the list as the simpler grandfather, so this is a cost the round-1 note did not weigh. Right: exclude the list from the line count as data by rule in pr-caps.sh, or revert to the format-2 key grandfather; name one.
    51	- Premise. V1's regime.yml test plan (lines 158, 187) relies on workflow_dispatch; the events page: "This event will only trigger a workflow run if the workflow file exists on the default branch." The stated sequence (merge unlisted, dry run from main against a closed PR, then list as required) is consistent with it; add it to the premises since V1 depends on it.
    52	- Evidence hygiene. Premise 8's command (line 79) embeds a transcript path in the home directory's slug form; run the masker on the design before the boundary commit, since the validator rejects home-directory paths under .orchestration/**.
    53	
    54	## 4. Edits that make round 3 a confirmation
    55	
    56	1. implementing_tasks as a map of task id to invariant ids (INV-2), and the design-on-main precondition or branch copy for the regime job.
    57	2. revise.yaml beside task.md; task.md byte-identical to the dispatched file (INV-3, line 144, V3c).
    58	3. A question threshold in INV-6 and section 7, or the item removed.
    59	4. V3a as an operator PR; hook counting in V3a only; V3b and V3c routed by the sources they touch.
    60	5. legacy-task-ids.txt excluded from the line cap or dropped; the workflow_dispatch premise added; the section 4 sentence fixed; the latest-TASK token named in INV-1.
    61	
    62	Everything round 1 asked for is in v2; the three rejections are contradictions v2 introduced while applying it, each a one-line change, and INV-7's own rule requires the re-review once the hashed keys change.
    63	
    64	Design verdict: revise
FILE .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round3.md
     1	---
     2	reviewed_at: 2026-10-10T21:33:02Z
     3	reviewer: claude-review-dot-a001
     4	profile: review
     5	session: 2089b04f-f9c7-498b-86c5-76f2140048d5
     6	design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@b2bfad90d1e1d3b8210b40321f6d23cfdab7c4e5b27e8d644b02a8fea9d535d2
     7	design_hash_kind: whole-file sha256 (the canonical hash tool is V1's deliverable)
     8	task: dotfiles-T128-design-review-a01
     9	round: 3
    10	previous: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round2.md
    11	---
    12	
    13	# Design review: dotfiles-T128-regime-v3-a01, round 3 (confirmation)
    14	
    15	Same reviewer and seat; v3 read in full at the hash above and checked line by line against the five edits of the round-2 receipt's section 4. The hashed keys changed between v2 and v3 (implementing_tasks, INV-1, INV-2, INV-3, INV-6, INV-8, INV-12, one premise), so this round is the review INV-7 requires. No command was re-run and no page re-fetched: v3 adds no claim that round 1 or round 2 did not already verify.
    16	
    17	## 1. The five edits
    18	
    19	1. implementing_tasks is a map of task id to invariant ids inside the hashed keys (lines 9-21); INV-2 states the design-on-main precondition through a boundary PR and the fail-closed rule for a missing design (line 45); V1 repeats the precondition (line 162). Applied.
    20	2. revise.yaml is a sibling file and task.md stays byte-identical (INV-3 line 46; INV-8 line 51; INV-12 gaming path line 55; enforcement row line 148; V3c line 168; the validation-file line assigned to V2b, line 165). Applied.
    21	3. Question threshold 2 in INV-6 (line 49) and section 7 (line 179); audit JSONs count only when their sha256 matches their AGMSG-AUDIT record (line 49; map line 151). Applied.
    22	4. V3a is an operator PR carrying all hook counting, with a Codex security-profile review before acceptance (line 166); V3b has no hook source (line 167); V3c has no gate source (line 168). Applied.
    23	5. The legacy list is excluded from the line cap as data (INV-2 line 45; INV-12 line 55; V1 line 162); the workflow_dispatch premise is added with the page's sentence (lines 84-86); the stage-3 sentence names the orchestrator's make audit-head and what removes the queue (line 140); INV-1 names the latest TASK's token and the recommit after each amendment (line 44). Applied.
    24	
    25	## 2. Invariants
    26	
    27	INV-1: accepted.
    28	INV-2: accepted. Note: section 7 (line 179) still words the cap as "outside tests/ and .orchestration/" without the data-list exclusion that INV-2 and INV-12 state; section 7 is outside the hash, so align it in the next edit without a new review.
    29	INV-3: accepted.
    30	INV-4: accepted.
    31	INV-5: accepted.
    32	INV-6: accepted.
    33	INV-7: accepted.
    34	INV-8: accepted.
    35	INV-9: accepted.
    36	INV-10: accepted.
    37	INV-11: accepted.
    38	INV-12: accepted.
    39	
    40	## 3. New in v3
    41	
    42	- scripts/regime-check.sh (lines 162, 168) now holds the regime job's logic, consistent with the residual that regime.yml itself is never exercised by its own PR (line 191). V1 is nine files; its added lines outside tests/, .orchestration/ and the data list (schema, validator, module, regime-check.sh, workflow, manifest, SKILL) are close to the 500 cap; V1b is the split if it goes over.
    43	- V2b's map entry is [INV-5] (line 13) while its scope carries INV-3's validation-file line (line 165). The id comparison of INV-2 is between task.md and the map, not the diff, so this is not a mechanical conflict; V2b's acceptance record should say the line is INV-3 enforcement dispatched under V2b, or the map lists [INV-5, INV-3] at the next hashed-key change.
    44	
    45	Nothing in v3 reopens a round-1 or round-2 finding.
    46	
    47	Design verdict: accept
FILE .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round4.md
     1	---
     2	reviewed_at: 2026-10-10T22:06:21Z
     3	reviewer: claude-review-dot-a001
     4	profile: review
     5	session: 2089b04f-f9c7-498b-86c5-76f2140048d5
     6	design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@6eedc15f74d9a150a601190e3fb839175be3799c2eadf37331f850430c930210
     7	design_hash_kind: whole-file sha256 (the canonical hash tool is V1's deliverable)
     8	task: dotfiles-T128-design-review-a01
     9	round: 4
    10	previous: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round3.md
    11	---
    12	
    13	# Design review: dotfiles-T128-regime-v3-a01, round 4 (confirmation of the V1 split)
    14	
    15	Diff check of v4 against the four edits the Round-4 section names. The hashed key implementing_tasks changed, so this is the review INV-7 requires.
    16	
    17	1. V1 is validation only (line 163: schema, validator, tier module, legacy list, its test) and V1c is the CI check after V1 (line 164: regime-check.sh, regime.yml, its test, process_tiers, SKILL step 3, README); V1b follows V1c (line 165). Applied.
    18	2. implementing_tasks gains dotfiles-T128-v1c-regime-ci-check-a01: [INV-1] (line 11), the second task on one invariant as V2 and V2b are on INV-5. Applied.
    19	3. Order V1, V1c, V1b, V2, V2b, V3a, V3b, V3c, V3d, V4, V5a, V5b, V6 (line 177); V1 with V2 stays the concurrent pair. Applied.
    20	4. Section 7 (line 181) now reads "15 changed files (the file count excludes .orchestration/ only) and 500 added lines outside tests/, .orchestration/ and the data list scripts/legacy-task-ids.txt", matching INV-2 and V1b. Applied. The receipt pointer names this round (line 7).
    21	
    22	The four task files that follow carry INV-1, INV-2 and INV-5 byte-identical to this file's invariants (checked with PyYAML) and name this receipt.
    23	
    24	INV-1: accepted. INV-2: accepted. INV-3: accepted. INV-4: accepted. INV-5: accepted. INV-6: accepted. INV-7: accepted. INV-8: accepted. INV-9: accepted. INV-10: accepted. INV-11: accepted. INV-12: accepted.
    25	
    26	Note: INV-1's sentence names "V1's acceptance record" for the ruleset action; after the split that record is V1c's. The sentence is hashed, so leave it and let V1c's acceptance record say it carries the action.
    27	
    28	Design verdict: accept
FILE .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round5.md
     1	---
     2	reviewed_at: 2026-10-10T22:12:18Z
     3	reviewer: claude-review-dot-a001
     4	profile: review
     5	session: 2089b04f-f9c7-498b-86c5-76f2140048d5
     6	design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@b5eb917f85d44726a514efbf910d2e0f04c17f07110ef90310fd6b3b13719ceb
     7	design_hash_kind: whole-file sha256 (the canonical hash tool is V1's deliverable)
     8	task: dotfiles-T128-design-review-a01
     9	round: 5
    10	previous: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round4.md
    11	---
    12	
    13	# Design review: dotfiles-T128-regime-v3-a01, round 5 (confirmation of the INV-3 form change)
    14	
    15	Diff check of v5 against the Round-5 section: INV-3 (line 47) now admits check=<tests/<file>::<name> | repro:<id>>; the ci:<job> form is gone; a repro carries its command and pasted output in revise.yaml; the CI regime job verifies the test selector by existence and diff against the previous RESULT head and the repro by a non-empty command and output; the host gate requires the same id in the validation file. The receipt pointer names this round (line 7). V3c (line 170) and V2b still match the split of CI step and gate line. Dropping ci:<job> is right: a new CI job is a .github/workflows/** change, design tier under INV-1 and never a one-round fix, and it had no "fails on the previous head" meaning; the test selector and the repro both do.
    16	
    17	INV-1: accepted. INV-2: accepted. INV-3: accepted. INV-4: accepted. INV-5: accepted. INV-6: accepted. INV-7: accepted. INV-8: accepted. INV-9: accepted. INV-10: accepted. INV-11: accepted. INV-12: accepted.
    18	
    19	Note: the task files V1, V1c, V1b and V2 still name the round-4 receipt, whose header hash is v4's whole-file sha256; V4's gate (and INV-7's whole-file form for pre-V4 receipts) compares the receipt against the current design, so every design change needs the implementing task files' design_review.receipt moved in the same edit. The task-review round-4 receipt carries this as its one item.
    20	
    21	Design verdict: accept
FILE .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round6.md
     1	---
     2	reviewed_at: 2026-10-10T22:28:36Z
     3	reviewer: claude-review-dot-a001
     4	profile: review
     5	session: 2089b04f-f9c7-498b-86c5-76f2140048d5
     6	design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@25b36e1c6e41aed8014af28911dbe9744bacc77a37ad6c1e445b35a03c5030be
     7	design_hash_kind: whole-file sha256 (the canonical hash tool is V1's deliverable)
     8	task: dotfiles-T128-design-review-a01
     9	round: 6
    10	previous: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round5.md
    11	---
    12	
    13	# Design review: dotfiles-T128-regime-v3-a01, round 6 (six invariants after the Bot review of c1e2582b)
    14	
    15	The Bot threads 4239399740-4239399761 on PR 316 were not read: GitHub is unreachable from this sandbox and the task forbids an out-of-sandbox read. Each change is judged on its own mechanics against the fact sheets and the scripts; where the change names a Bot finding, the finding's substance is inferred from the change.
    16	
    17	## Changed invariants
    18	
    19	INV-1: accepted. The literal first segment plus the tier-by-literal-prefix rule closes allowed_files of ['*'] and friends, and binding the legacy exemption to .orchestration/tasks/ on main closes the branch-copy claim; both are mechanical in V1 and V1c. Note: the schema regex V1 chose admits a wildcard inside the first segment (scripts*); see the task-review receipt.
    20	
    21	INV-2: accepted. Byte-for-byte sentence equality against the design read from main is what this seat has been checking by hand each round; now the regime job does it.
    22	
    23	INV-3: accepted. previous_head carried in the ACCEPTANCE and revise.yaml, diffed by CI and cross-checked by the host gate against the previous RESULT's head in history, closes the gap round 1 named (CI cannot know the previous head). Note: INV-12 should list "a previous_head that is not the previous RESULT's head" as a gaming path; the generic clause covers its test, so this is wording, not a hole.
    24	
    25	INV-5: accepted with one note that V2 must act on. The instruction root and the schema from main, the head as --add-dir data, closes the schema-or-AGENTS.md-on-the-audited-head path for codex. The claude fallback is not fully closed: the headless page states that bare mode "loads skills from its .claude/skills/ folder" of a directory named with --add-dir, so a head that adds or changes .claude/skills/** enters the fallback's context as skill descriptions. The runner should refuse the fallback (exit 2, blocked) when git diff --quiet origin/main <head> -- .claude/skills fails, leaving such a head to the codex path; add the page's sentence as a premise.
    26	
    27	INV-7: rejected: the second review's alternative form contradicts the sentence. "or the Codex Bot's review of the boundary PR carrying the design" produces no receipt, no canonical hash and no AGMSG-RESULT from a Codex identity, yet the same sentence requires each receipt to be a schema document naming the hash and both RESULTs to precede the implementing TASK; the only way the Bot form satisfies that is an orchestrator-written receipt for a review it did not perform, which is R5. Right: the Codex review is codex exec --sandbox read-only on the review profile under a codex-review identity (headless, V4's runner, or a seated one until V4), its receipt and RESULT like the Claude one; the Bot's PR review stays what it is, swept feedback. Second gap: the enforcement row (line 153) and V4 (line 172) still describe one -review- identity and one receipt; name the Codex form in both and the gate rule "two RESULTs, one from a Claude -review- identity and one from a Codex -review- identity, both naming the current hash". The round-6 Codex receipt in flight (…-round6-codex.md) is the right shape for this.
    28	
    29	INV-12: accepted; the four new gaming paths match INV-1, INV-2 and INV-5 as changed.
    30	
    31	INV-4, INV-6, INV-8, INV-9, INV-10, INV-11: unchanged, accepted.
    32	
    33	Stage-0 row (line 133) matches INV-7's two reviews; section 10 records rounds 2 to 5 correctly.
    34	
    35	Design verdict: revise
FILE .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round7.md
     1	---
     2	reviewed_at: 2026-10-10T22:31:53Z
     3	reviewer: claude-review-dot-a001
     4	profile: review
     5	session: 2089b04f-f9c7-498b-86c5-76f2140048d5
     6	design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@40476474ad9aec1f36f14927a43a8f98d0187eb5d7092b422b635fbdff70142a
     7	design_hash_kind: whole-file sha256 (the canonical hash tool is V1's deliverable)
     8	task: dotfiles-T128-design-review-a01
     9	round: 7
    10	previous: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round6.md
    11	---
    12	
    13	# Design review: dotfiles-T128-regime-v3-a01, round 7 (confirmation of the INV-7 fix)
    14	
    15	- INV-7 (line 51): the second review is codex exec --sandbox read-only on the review profile under a codex-review identity (headless through V4's runner, or seated until V4); each receipt names the canonical hash, each is announced by an AGMSG-RESULT from its reviewing identity, both precede the implementing TASK; the Codex Bot's review of a boundary PR is swept feedback, never a design receipt. The contradiction round 6 named is gone.
    16	- Enforcement row (line 156) and V4 (line 175): two headless runs per hash under claude-review-dot-hNNN and codex-review-dot-hNNN, each joining for the run and sending its RESULT; the gate requires both RESULTs and recomputes both hashes, whole-file form accepted for pre-V4 receipts. Stage 0 (line 136) matches.
    17	- Premise added (lines 88-90): bare mode loads skills from the .claude/skills/ folder of an --add-dir directory, with the headless page's sentence; V2 acts on it.
    18	- Receipt pointer names this round (line 7). The three invariants the four task files carry (INV-1, INV-2, INV-5) are byte-identical to round 6's; the other invariants were not diffed byte for byte against v6, and the Round-7 section states INV-7 as the only invariant change.
    19	
    20	INV-1: accepted. INV-2: accepted. INV-3: accepted. INV-4: accepted. INV-5: accepted. INV-6: accepted. INV-7: accepted. INV-8: accepted. INV-9: accepted. INV-10: accepted. INV-11: accepted. INV-12: accepted.
    21	
    22	Design verdict: accept
FILE design
     1	---
     2	format: 2
     3	task_id: dotfiles-T128-regime-v3-a01
     4	kind: design
     5	security: true
     6	design_review:
     7	  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round7.md
     8	  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
     9	implementing_tasks:
    10	  dotfiles-T128-v1-task-schema-a01: [INV-1]
    11	  dotfiles-T128-v1c-regime-ci-check-a01: [INV-1]
    12	  dotfiles-T128-v1b-pr-caps-a01: [INV-2]
    13	  dotfiles-T128-v2-audit-schema-and-runner-a01: [INV-5]
    14	  dotfiles-T128-v2b-audit-gate-a01: [INV-5]
    15	  dotfiles-T128-v3a-reset-counters-a01: [INV-6]
    16	  dotfiles-T128-v3b-premises-and-amendments-a01: [INV-4]
    17	  dotfiles-T128-v3c-one-fact-per-round-a01: [INV-3]
    18	  dotfiles-T128-v3d-idle-and-first-push-a01: [INV-10]
    19	  dotfiles-T128-v4-design-review-runner-a01: [INV-7]
    20	  dotfiles-T128-v5a-evidence-on-branch-a01: [INV-8]
    21	  dotfiles-T128-v5b-cost-fields-a01: [INV-9]
    22	  dotfiles-T128-v6-permgate-session-a01: [INV-11]
    23	supersedes:
    24	  - dotfiles-T126-regime-v2-a01
    25	  - dotfiles-T124-design-gate-and-reset-rule-a01
    26	reset_of:
    27	  - dotfiles-T124-wave1-task-validator-a01
    28	  - dotfiles-T124-wave3b-audit-grammar-a01
    29	threat_model:
    30	  R1: rounds are judged by models re-reading models and add no deterministic fact, so a wrong premise is patched round after round (T118 20 revises, T119 5 revises and 4 audits; the vendor's own rule is two corrections, then start fresh)
    31	  R2: "hand-written parsers at a trust boundary have an unbounded bypass surface (PR 313: 33 of 52 Bot threads on a 503-line validator with its own YAML parser, written on the false premise that PyYAML is unavailable)"
    32	  R3: "PRs larger than a reviewer can hold (PR 313 20 files +2642, PR 312 37 files +3191; Google: 100 lines reasonable, 1000 too large)"
    33	  R4: task text grown by question-and-amendment (PR 313 6 questions 8 amendments, T119 8 and 8, T120 8 amendments and no RESULT) keeps the under-researched premise
    34	  R5: the orchestrator's artifacts are unaudited and it dispositions findings about itself (T119 audit-finding 2); the reset rule was prose the orchestrator could waive (PR 313 revise round 2)
    35	  R6: "the auditor becomes a serial queue when audits run once per round in one tab (measured: 4 audits about 1.3 h of T119's 11.1 h; the rounds, not the audits, were the cost)"
    36	  R7: cost is unmeasured (every acceptance record says cost n/a) so no stage can be weighed against its value
    37	  R8: a PR can change the check that judges it (a pull_request workflow runs the PR head's workflow file); host-side evidence is whatever the orchestrator copies into the gate's cwd
    38	trust_anchors:
    39	  - agmsg message history (append-only, read through history.sh) for who did what and when; GitHub for PR, CI, Bot, ruleset and merge state; the main checkout for files, never the gate's cwd
    40	  - JSON Schema documents validated by the jsonschema library (PyYAML for front matter) for task files, audit verdicts, design-review receipts and evidence; model verdicts produced under schema (codex exec --output-schema, server-side strict; claude -p --json-schema)
    41	  - mechanical checks run from main's workflow file as a pull_request_target required status check that reads PR files as data and executes nothing from the PR; required workflows are organization-only, so this is the main-pinned form available to a user-owned repository
    42	  - the operator waiver is visible, not prevented (acceptance record, boundary PR body, check-regime-boundary)
    43	  - a reset is released only by a redesign written in a context other than the one that wrote the abandoned task, or by the operator
    44	invariants:
    45	  INV-1: "every task is a format-2 file whose front matter validates against schemas/task.json (jsonschema + PyYAML, no hand-written parser; every allowed_files entry starts with a literal path segment and a wildcard entry derives the tier of every design-tier path its literal prefix can cover); legacy task ids are grandfathered only for files under .orchestration/tasks/ on main, never for a branch copy; the tier (docs, review, design) is derived from allowed_files by the shared high-risk module, with the regime's own rule prose (home/dot_config/claude/rules/**, the agmsg-orchestration SKILL, AGENTS.md, README) listed in the review tier, and selects the pipeline from process_tiers in agent-config.yaml; every AGMSG-TASK for the task, the first and each amendment, carries task_sha256= of the task file as sent, the worker commits the file byte-identical to .orchestration/<task id>/task.md (first commit, recommitted after each amendment), the CI regime job validates that copy with main's schema and refuses a PR that changes .github/workflows/** unless its task.md is design tier and lists the file, the host gate compares the copy's sha256 with the latest AGMSG-TASK's token in history, and the regime check binds only once the ruleset lists it as required (an operator action named in V1's acceptance record); the orchestrator can add or skip a stage only with an operator waiver named in the acceptance record"
    46	  INV-2: "a PR is mergeable only within the caps the CI regime job enforces from main's workflow (at most 15 changed files and 500 added lines outside tests/, .orchestration/ and the data list scripts/legacy-task-ids.txt), and its task.md invariants equal the design's as a set of ids and byte-for-byte as sentences (the design read from main, never from the PR); the design file must be on main (through a boundary PR) before the implementing TASK is dispatched and the regime job fails closed when the design named by task.md is absent from main; exceeding a cap is a split, never a finding to disposition (the cap changes the unit of work: T116 +529 and T118 +881 would have been split)"
    47	  INV-3: "a revise round is admissible only when it adds a new deterministic check: the AGMSG-ACCEPTANCE status=revise carries check=<tests/<file>::<name> | repro:<id>> and previous_head=<the RESULT head being revised>, the worker records both in .orchestration/<task id>/revise.yaml (a sibling file; task.md stays byte-identical to the dispatched file) together with the command and pasted output for a repro, the CI regime job verifies, for a test selector, that the named test file exists on the head and differs between the recorded previous_head and the head (git diff <previous_head> <head> -- <test file> non-empty) and, for a repro, that revise.yaml carries a non-empty command and output for that id, and the host gate, which reads history, verifies that previous_head equals the head of the previous AGMSG-RESULT for the task and requires the same id in the validation file; a finding that cannot become a check is dispositioned, never iterated"
    48	  INV-4: a task file carries premises, each with the command and pasted output that verified it before dispatch; a worker question (AGMSG-PONG status=question) is a specification defect answered by at most one further AGMSG-TASK; amendments are every AGMSG-TASK for the task_id after the first, whatever its wording, and the second one is INV-6's count, which withdraws the task to design through INV-6's merge backstop and Stop signal
    49	  INV-5: "the task-level audit is a headless read-only run whose instruction root is the trusted main checkout and whose schema is main's schemas/audit.json: codex exec --output-schema <main>/schemas/audit.json -C <main> with the detached worktree at the head added as a read-only data directory (--add-dir), so the audited PR controls neither the schema nor the AGENTS.md the auditor reads; the fallback claude -p --json-schema from the same root with --add-dir <worktree>, --bare when an API key is set and otherwise with project and user hooks disabled started when CI is green and the Codex Bot has reviewed the head or 15 minutes have passed without a Bot review (recorded as bot: none), at most once per RESULT head, pooled two at a time; the gate accepts an audit of an earlier head only when git diff --quiet <audited head> <HEAD> -- . ':!.orchestration' holds (an evidence-only revision), otherwise a new audit is required; its input includes the task's invariants and premises, the worker's evidence, the orchestrator's task file, amendments, acceptance record with its dispositions, the head's pr-feedback JSON and the previous round's audit JSON; the schema lists findings {priority, confidence, category in {specification, implementation, evidence, orchestration, conformance}, path, line, rationale} and the per-invariant map before the verdict, and the prompt asks for the rationale before each verdict; the runner, under the identity claude-audit-dot-h001 or codex-audit-dot-h001 on the orchestrator's host, records the JSON's sha256 in agmsg history (AGMSG-AUDIT v1 task_id= head= sha256= auditor=) before the gate reads it, an anchor that prevents edits after the record and not fabrication before it; the gate reads the verdict and categories from the JSON, and orchestration and conformance findings at P0-P2 accept only an operator waiver or a design reset, never not-applicable"
    50	  INV-6: "the reset rule's mandatory point is the merge backstop in scripts/require-crit-review.py, with the orchestrator's Stop hook (Claude Stop hook, Codex [hooks].Stop) as the early signal, soft on both runtimes by their documented caps; counts come from history for the hook and the gate (revises = RESULTs for the task_id minus one, threshold 2; amendments = AGMSG-TASKs after the first, threshold 2; AGMSG-PONG status=question, threshold 2) and from GitHub and main-checkout files for the gate and the boundary check only (Codex Bot P0 or P1 on two heads after the first RESULT, from original_commit_id on review_comment items recorded by pr-feedback.py; an audit implementation or specification finding at P0-P1 on two heads, from .orchestration/validation/<task>-audit-<sha7>.json in the main checkout, each counted only when its sha256 matches its AGMSG-AUDIT record); when a count is reached the gate refuses the merge until a reset record names a redesign task whose design RESULT comes from an identity other than the task's author, or the operator sets DESIGN_RESET_WAIVED_BY; check-regime-boundary.sh reports a closed-unmerged PR whose task has no reset record and a task over any count with neither an accepted acceptance record nor a reset record"
    51	  INV-7: "the design tier adds, before any code is dispatched, two design reviews of the same design hash: a fresh Claude context on the review profile (a headless run or a seated -review- identity; the review profile is the same model and effort as deep, so the lever is the separate context) and a Codex read-only review (codex exec --sandbox read-only on the review profile under a codex-review identity: headless through V4's runner, or seated until V4); each receipt is a schema document naming the design file's canonical hash over invariants, threat_model, trust_anchors, implementing_tasks and premises, each is announced by an AGMSG-RESULT from its reviewing identity, and both RESULTs precede the implementing AGMSG-TASK in history; the Codex Bot's review of a boundary PR is swept feedback, never a design receipt; a change to the hashed keys needs new reviews; the gate accepts the whole-file sha256 form for receipts written before V4 lands"
    52	  INV-8: "worker evidence (the task.md copy, revise.yaml, report, validation, sandbox, learning, autoskill, worker review JSON) is committed on the PR branch under .orchestration/<task id>/ before the final RESULT so the Bot, CI and the gate read the same files from the audited head; the orchestrator's records (audit JSON, acceptance, pr-feedback) stay under .orchestration/validation and .orchestration/acceptance in the boundary commit because the merge is --match-head-commit"
    53	  INV-9: "every acceptance record carries measured cost (rounds, amendments, questions, wall time TASK to final RESULT from history timestamps, audit count, Bot threads, tokens: total_cost_usd from claude -p JSON, turn.completed.usage from codex exec --json, per-message usage from the seat's session transcript) written by accept-task.py; each tier has a budget, the acceptance record names the operator decision when it is exceeded, and check-regime-boundary.sh warns; headless runs carry --max-budget-usd"
    54	  INV-10: at most three concurrent workers with pairwise-disjoint allowed_files; the first push (a draft PR) lands within 30 minutes of the TASK and a seated worker is not idle for 20 minutes while a dispatchable task exists, both computed in check-regime-boundary.sh and accept-task.py from history.sh timestamps and gh pr view, never in the Stop hook; headless reviews and audits do not count as workers
    55	  INV-11: permgate records session_id and cwd per decision, and the gate compares a Claude worker's permission-gated Bash count in the task window with the sandbox record (an understated record is refused); Codex workers cannot escalate and are not covered
    56	  INV-12: "every rule above is exercised by a unit test that fails when the rule is removed, including one per gaming path (a schema-valid task with a prose cap bypass, a revise without a named check, a revise list appended to the hashed task.md, an AGMSG-TASK without amendment= that still counts, an evidence-only relabel of a code change caught by the tree-equality check, a wave-table rewrite after review, an audit JSON edited after its history record, a receipt whose hash predates a key change, a reset record naming the author's own identity, a Bot-skipped head whose audit never starts, a single PR split only in the task file, a branch task.md claiming a legacy id, allowed_files of ['*'] or a wildcard first segment, an invariant sentence weakened under its id, a schema or AGENTS.md edited on the audited head); legacy task ids are grandfathered by the checked-in list scripts/legacy-task-ids.txt, which only shrinks and is excluded from the line cap as data"
    57	premises:
    58	  - claim: PyYAML is already installed by uv in the Makefile and CI; jsonschema is not yet named anywhere and V1 adds --with jsonschema; both resolve through uv on this host
    59	    command: "grep -n 'with pyyaml\\|jsonschema' Makefile .github/workflows/*.yml; uv run --no-project --with jsonschema --with pyyaml python -c 'import jsonschema, yaml; print(jsonschema.__version__, yaml.__version__)'"
    60	    output: "Makefile:189 and :203 and agent-assets.yml:35 use --with pyyaml; no jsonschema anywhere; 4.26.0 6.0.3"
    61	  - claim: required workflows are organization-only; pull_request_target runs the base branch's workflow file and is eligible as a required status check
    62	    command: "WebFetch docs.github.com available-rules-for-rulesets (enterprise-cloud) and troubleshooting-required-status-checks"
    63	    output: "Ruleset workflows can be configured at the organization or enterprise level; required checks count when triggered by push, pull_request, pull_request_review, pull_request_target, deployment, deployment_status; pull_request_target runs in the context of the default branch of the base repository"
    64	  - claim: codex exec --output-schema is enforced server-side as a strict JSON schema; codex 0.161.0 rejects --full-auto and -a on exec
    65	    command: "codex exec --help; read codex-rs/exec/src/lib.rs and codex-api/src/common.rs at rust-v0.161.0"
    66	    output: "text.format = {type: json_schema, strict: true, schema}; error: unexpected argument '--full-auto' found; approval policy for exec is set with -c approval_policy=never"
    67	  - claim: claude -p --bare requires an API key and skips hooks; without --bare a -p run executes the project's hooks; --json-schema returns structured_output; --max-budget-usd caps spend
    68	    command: "WebFetch code.claude.com/docs/en/headless and cli-reference"
    69	    output: "--bare never reads OAuth credentials or the system keychain; set ANTHROPIC_API_KEY; without --bare -p runs the hooks in a project's .claude/settings.json; the structured output is in the structured_output field; spend can pass the cap, so leave headroom"
    70	  - claim: the vendor's own reset rule is two corrections
    71	    command: "WebFetch code.claude.com/docs/en/best-practices"
    72	    output: "If you've corrected Claude more than twice on the same issue in one session, the context is cluttered with failed approaches. Run /clear and start fresh with a more specific prompt"
    73	  - claim: the audit was not the wall-clock bottleneck
    74	    command: "stat .orchestration/validation/dotfiles-T119-*-audit-*.md; history.sh dotfiles-conformance (TASK 2026-10-09T21:26Z to ACCEPTANCE 2026-10-10T08:32Z)"
    75	    output: "four audit files written 11:48, 13:55, 15:52, 17:23 local, each run 15-25 minutes, about 1.3 h of an 11.1 h task"
    76	  - claim: both runtimes' Stop hooks are soft signals, not hard stops, so the merge gate is the mandatory point
    77	    command: "WebFetch learn.chatgpt.com/docs/hooks; WebFetch code.claude.com/docs/en/hooks (Stop section)"
    78	    output: "Codex: decision block doesn't reject the turn but injects a continuation prompt; Claude: 8-consecutive-continuation cap that resets each time Claude calls a tool"
    79	  - claim: the seat's session transcript carries per-message token usage on this host
    80	    command: "grep -o '\"usage\":{[^}]*}' ~/.claude/projects/-Users-a0004262-Workspace-dotfiles--claude-worktrees-worker-c/3747b995-3bb1-4c51-8421-4b1e672b442a.jsonl | tail -1; grep -c '\"usage\"' <same file>"
    81	    output: "usage with input_tokens, cache_creation_input_tokens, cache_read_input_tokens, output_tokens; 5168 usage entries (format internal to Claude Code per its docs)"
    82	  - claim: history.sh truncates to 20 rows by default, so counters read the storage facade or pass a limit
    83	    command: "history.sh dotfiles-conformance | wc -l; history.sh dotfiles-conformance --limit 600 | wc -l"
    84	    output: "20; 256 (the whole team history)"
    85	  - claim: "workflow_dispatch runs a workflow only once its file is on the default branch, so regime.yml is merged unlisted, dry-run from main against a closed PR, then listed as required"
    86	    command: "WebFetch docs.github.com events-that-trigger-workflows (workflow_dispatch)"
    87	    output: "This event will only trigger a workflow run if the workflow file exists on the default branch"
    88	  - claim: "bare mode loads skills from the .claude/skills/ folder of a directory named with --add-dir, so the claude fallback must refuse a head that changes .claude/skills/**"
    89	    command: "WebFetch code.claude.com/docs/en/headless (bare mode section)"
    90	    output: "bare mode loads skills from its .claude/skills/ folder (of directories named with --add-dir)"
    91	
    92	---
    93	
    94	# AGMSG-TASK dotfiles-T128-regime-v3-a01 — DESIGN: regime v3, the redesign after the 2026-10-10 halt
    95	
    96	Drafted 2026-10-11 (local) by the orchestrator seat `claude-deep-dot` under a recorded bootstrap exception (operator decision 2026-10-11: the orchestrator drafts, a fresh context on the review profile must accept before any implementing task is dispatched). Operator direction (pasted 2026-10-11): when substantive findings repeat, the design, implementation or verification is wrong and a mechanism must force the redo; prose alone repeats the mistake; the auditor must be able to find the orchestrator's and the worker's mistakes; efficiency, quality and cost are optimised together; the auditor must not become the bottleneck and the audit stages must be chosen; all of it grounded in the tools' official documentation and current practice. Research inputs: fact sheets on Claude Code 2.1.293, Codex CLI 0.161.0, GitHub rulesets and Actions, and the research literature, read 2026-10-11; the measured baseline below.
    97	
    98	## 1. Finding: the fix program tripped its own rule
    99	
   100	By T126 INV-6 as written: wave 1 (PR #313) 8 amendments (limit 4) and 2 revises (limit 2); wave 3b (PR #314) Bot P1 on two post-RESULT heads. The orchestrator was drafting a waiver for #313. T120 was reset only on the operator's question. The regime is therefore reset here by its own rule; this document is the redesign, and T126 and T124 are superseded (their accepted ideas are kept where named).
   101	
   102	Measured baseline (history + GitHub):
   103	
   104	| task | PR | files | +lines | amendments | questions | revises | audits (incorrect) | Bot threads (heads) | P0/P1 | wall |
   105	|---|---|---|---|---|---|---|---|---|---|---|
   106	| T114 | - | - | - | 0 | 0 | 6 | 3 (3) | - | - | 21.5h |
   107	| T118 | 310 | 35 | 881 | 7 | 0 | 20 | 8 (7) | 16 (7) | 0 | 10.6h |
   108	| T119 | 312 | 37 | 3191 | 8 | 8 | 5 | 4 (4) | 25 (11) | 7 | 11.1h |
   109	| T120 | 315 | 19 | 1489 | 8 | 1 | 0 | 0 | 15 (5) | 8 | reset |
   110	| T124 W1 | 313 | 20 | 2642 | 8 | 6 | 2 | 0 | 52 (10) | 31 | halted, reset |
   111	| T124 W3b | 314 | 9 | 1462 | 5 | 0 | 0 | 0 | 24 (4) | 2 | halted, reset |
   112	
   113	Every acceptance record to date says `cost: n/a`.
   114	
   115	## 2. Root causes, each with its evidence
   116	
   117	R1 to R8 in the front matter. The literature behind R1: intrinsic self-correction without an external signal degrades after the first round (Huang et al. 2023); a second review round on the same artifact raised recall slightly and false positives by 62% (arXiv 2603.16244); multi-round review degrades with rounds (MCR-Bench); revising an already-correct state loses correct work unless verifier evidence is bound to the exact code state (arXiv 2607.24604). Behind R3: Google's review study (median change 24 lines, ~90% under 10 files) and its CL-size guidance. Behind R5 and R6: a judge without a reference is lenient and a reference flips 9-85% of verdicts toward correct (2607.12885); format-restricted generation degrades reasoning, so verdicts reason first and then fill the schema (2408.02442); Anthropic's harness-design post: a standalone skeptical evaluator is tractable where a self-critical generator is not, and the evaluator is worth its cost only where the task exceeds the model's reliable solo capability, which is what the tier table encodes.
   118	
   119	## 3. Principles (each names what it reuses and what it deletes)
   120	
   121	- **P1 One deterministic fact per round (INV-3).** Reuses tests/unit, CI, `pr-feedback.py`. Deletes free-form revise rounds and the audit-per-round habit.
   122	- **P2 Declarative over imperative at trust boundaries (INV-1, INV-5, INV-7).** Reuses `jsonschema`, PyYAML, `codex exec --output-schema`, `claude -p --json-schema`. Deletes the bespoke YAML parser, the glob NFA, the prose verdict grammar, regex parsing of `.last.md`, and the T126 "process_tiers.json next to the module" indirection (the validator reads the manifest with PyYAML).
   123	- **P3 Small one-invariant PRs enforced in CI (INV-2).** Reuses GitHub required checks and the strict up-to-date ruleset already in force. Deletes waves declared inside a task file.
   124	- **P4 Main-pinned mechanical checks in CI; host gate only for history-anchored rules (INV-1, INV-2, INV-8 in CI; INV-3, INV-5 record, INV-6, INV-7 anchor, INV-11 on the host).** Reuses `pull_request_target`, the `changes` job pattern that reports success for an `.orchestration`-only diff. Deletes PR #313's `REVIEW_TREE` idea (never on `main`) and the copy step of untracked evidence into the gate's cwd. The host gate `make require-crit-review` keeps its evidence rules and changes three of them in named waves: the audit verdict and categories come from the schema JSON with the `AGMSG-AUDIT` record and the category lock (V2b), the reset backstop and the Bot-head count (V3a), the history-anchored design review (V4); it continues to run from the orchestrator's main checkout.
   125	- **P5 Research before dispatch; a question ends the task, not amends it (INV-4).** Reuses history (`amendment=`, `status=question`). Deletes the amendment-per-question practice. The task file's `premises` block is the mechanical residue of "verify every CLI constraint by running the real command".
   126	- **P6 Reset is mechanical, loop-time, and released only by another context or the operator (INV-6).** Reuses `scripts/require-crit-review.py` as the mandatory point, `agent-stop-gate.sh` and the Codex `[hooks].Stop` as the early signal (both soft by their documented caps: Claude's 8-continuation cap, Codex's continuation prompt), `check-regime-boundary.sh` for the re-dispatch detector. Deletes the orchestrator-written redesign (the redesign author is a `review`-profile seat or a fresh headless context; the `redesign` profile of T124 v4 is dropped: `review` is the same model and effort as `deep`, so independence of context is the whole lever, and T124 round 1 showed it works).
   127	- **P7 Audit staging by tier; the auditor never serializes the pipeline (INV-5, process_tiers).** See section 4.
   128	- **P8 Cost measured, budgets per tier (INV-9).** Reuses the JSON cost fields the runtimes already emit and the session transcripts. Deletes `cost: n/a`.
   129	- **P9 Parallelism with disjoint files and early push (INV-10).** Reuses `herdr-agents --add-worker`, draft PRs.
   130	- **P10 Routing stays by boundary.** Claude-boundary sources to a Codex seat, Codex-boundary to a Claude seat, permgate and shared gate sources to the operator, as the agmsg-orchestration skill's step 3 states; nothing here changes that.
   131	
   132	## 4. Audit stages (process_tiers; the one table the validator reads)
   133	
   134	| stage | who | when | tier docs | tier review | tier design | cost |
   135	|---|---|---|---|---|---|---|
   136	| 0 design review | a fresh Claude context on the review profile and a Codex read-only review of the same hash, schema receipts (INV-7) | before any code | - | - | required | minutes |
   137	| 1 worker checks | worker in its sandbox: invariant tests first, shellcheck, unit tests | before every push | required | required | required | none for the regime |
   138	| 2 CI + Bot | main-pinned `regime` check (schema, caps, evidence shape) + unit tests + Codex Bot | every push, in parallel | required | required | required | none |
   139	| 3 schema audit | headless read-only `codex exec --output-schema`, pooled 2, started by `make audit-head` once CI is green and the Bot reviewed or 15 min passed, once per RESULT head, reused for an evidence-only head by tree equality (INV-5) | per RESULT head | - | required | required, with invariant map and permgate window | the scarce resource, now off the critical path |
   140	| 4 acceptance | orchestrator: sweep, dispositions, record, host gate, merge `--match-head-commit` | per RESULT | required | required | required | minutes |
   141	
   142	Tier derivation: docs = prose-only `allowed_files` outside the regime's own rule prose (`home/dot_config/claude/rules/**`, the agmsg-orchestration SKILL, `AGENTS.md`, README), which is review tier by explicit list; review = the existing review-tier paths (scripts, hooks, tests, templates); design = the explicit design-tier list from T124 INV-2 v3 (install/**, setup.sh, the gate scripts, `executable_herdr-agents`, `executable_permgate`, Codex and Claude policy, sandbox and permission settings, credential helpers). Round limits: docs 1 revise; review and design 2 revises then reset. Profiles: worker `standard` (docs `express`), review `review`, audit `audit`.
   143	
   144	Why stage 3 is not the queue: the orchestrator starts it with `make audit-head` when the RESULT arrives (the wait on CI and the Bot is inside the target), it runs concurrently (pool of two, each in its own detached worktree), once per head, and an evidence-only head reuses the earlier audit by tree equality; the measured cost of the old serial form was 1.3 h of 11.1 h, so the throughput levers are P1 and P6, and the pool removes the residual queue.
   145	
   146	## 5. Enforcement map
   147	
   148	| invariant | enforcement point |
   149	|---|---|
   150	| INV-1 | `.github/workflows/regime.yml` (`pull_request_target`, required check `regime`: validates `.orchestration/<task id>/task.md` from the PR head read as data, refuses workflow edits outside a design-tier task), `scripts/validate-task.py` (schema + PyYAML, about 80 lines), `schemas/task.json`, `scripts/lib/high_risk_paths.py` (new module: tier lists and `tier_of`), `scripts/legacy-task-ids.txt` (grandfather list), `process_tiers` in the manifest; host gate compares the copy's sha256 with `task_sha256=` in history (V3a) |
   151	| INV-2 | `regime.yml` step with `scripts/pr-caps.sh` and the task.md invariant-id comparison against the design's `implementing_tasks` |
   152	| INV-3 | `regime-check.sh` step: a test selector named in `.orchestration/<task id>/revise.yaml` (sibling of the byte-identical task.md) exists on the head and differs from the previous RESULT head; a `repro:<id>` carries command and output there; the host gate's matching validation-file line is V2b's |
   153	| INV-4 | `scripts/validate-task.py` (premises required for code and design tasks); `agent-stop-gate.sh` early signal on the second AGMSG-TASK or second PONG question; the merge backstop is INV-6's |
   154	| INV-5 | `schemas/audit.json` (findings and invariant map before verdict), `scripts/audit-head.sh` (about 100 lines: detached worktree, `codex exec`, fallback, sha256 to history under the audit identity, `.last.md` render; PR #314's hardening kept), `make audit-head` target around `gh pr checks --watch` and the SKILL's Bot list loop with its 15-minute `bot: none` rule (no daemon), `AGENTS.md` Audit section; gate: JSON verdict and categories, `AGMSG-AUDIT` lookup, category lock, tree-equality acceptance of an earlier head (V2b) |
   155	| INV-6 | `scripts/require-crit-review.py` (mandatory: history counts, Bot heads from `original_commit_id` recorded by `scripts/pr-feedback.py`, audit heads from the main checkout's audit JSONs whose sha256 matches their `AGMSG-AUDIT` record, reset record or `DESIGN_RESET_WAIVED_BY`), `scripts/agent-stop-gate.sh` and the manifest's `codex.hooks` Stop entry (early signal, history counts only, within the 3 s history budget), `scripts/check-regime-boundary.sh` (closed-unmerged PR without a reset record; over-count task without an accepted or reset record; waiver listing) |
   156	| INV-7 | `scripts/design-review.sh` + `schemas/design-review.json`: two headless runs per design hash, `claude -p` under `claude-review-dot-hNNN` and `codex exec --sandbox read-only` under `codex-review-dot-hNNN`, each joining for the run and sending its RESULT; gate: both RESULTs precede the implementing TASK, both hashes recomputed, whole-file form accepted for pre-V4 receipts |
   157	| INV-8 | worker writes under `.orchestration/<task id>/` on the branch (task.md copy first); `regime.yml` validates the evidence JSON shapes; the gate's existing path rules keep the orchestrator's records under `validation/` and `acceptance/` |
   158	| INV-9 | `scripts/accept-task.py` (sweep, dispositions scaffold, record rows, gate invocation, merge command, cost fields), budgets in `process_tiers`, `check-regime-boundary.sh` warning |
   159	| INV-10 | `scripts/check-regime-boundary.sh` and `scripts/accept-task.py` from `history.sh` timestamps (storage facade or `--limit`, never the 20-row default) and `gh pr view` |
   160	| INV-11 | `executable_permgate` (operator-routed, Codex security review) + gate cross-check |
   161	| INV-12 | one test module per script; `make unit-test` in CI; the auditor checks per PR that no new hand-written parser sits at a trust boundary (a `conformance` finding) |
   162	| prose | SKILL, `agmsg-orchestration.md`, `pr-integration.md`, `crit-review.md`, `model-selection.md`, README: each wave edits only the sections it implements |
   163	
   164	## 6. Waves (one PR, one invariant, within INV-2's caps; each task file reviewed by a fresh context before dispatch)
   165	
   166	- **V1** INV-1, validation only (operator direction 2026-10-11, relayed through the review seat; also the cap: the undivided V1 sat at 500 added lines): `schemas/task.json`, `scripts/validate-task.py`, `scripts/lib/high_risk_paths.py`, `scripts/legacy-task-ids.txt` (from PR #313; data, excluded from the line cap), `tests/unit/test_validate_task.py`. Claude seat. Design tier: this review is its stage 0. Precondition: this design is on `main` through a boundary PR before V1's TASK is dispatched.
   167	- **V1c** INV-1, the CI check (after V1): `scripts/regime-check.sh`, `.github/workflows/regime.yml` (task.md validation, workflow-edit refusal, `workflow_dispatch` dry run), `tests/unit/test_regime_check.py`, `process_tiers` in the manifest, SKILL step 3 paragraph, README sentence. Claude seat. Acceptance names the operator action that lists `regime` as a required check, after the dry run from `main` against a closed PR. Two tasks map to INV-1 as V2 and V2b map to INV-5.
   168	- **V1b** INV-2 (after V1c): `scripts/pr-caps.sh`, the caps and invariant-id steps in `regime-check.sh`, tests, one SKILL sentence.
   169	- **V2** INV-5 runner: `schemas/audit.json` (PR #314's, reordered), `scripts/audit-head.sh` with PR #314's hardening, `make audit-head`, `AGENTS.md` Audit section, tests, the SKILL's task-level audit bullet. Claude seat.
   170	- **V2b** INV-5 gate: `scripts/require-crit-review.py` reads the JSON verdict and categories, requires the `AGMSG-AUDIT` record, locks orchestration and conformance at P0-P2 to waiver or reset, accepts an earlier audited head by tree equality, and requires the INV-3 `check=` line in the validation file; tests. Operator-routed gate source (delegable to a Claude seat with recorded opt-in).
   171	- **V3a** INV-6: `scripts/pr-feedback.py` (`original_commit_id` on review_comment items), `require-crit-review.py` reset backstop and `task_sha256` comparison, `agent-stop-gate.sh` history counts (revises, amendments, questions) as the early signal, the Codex Stop entry in the manifest and its rendered template, `check-regime-boundary.sh` detector and waiver listing; tests. Three boundaries in one PR (gate source, Claude hook source, Codex hook source): an operator PR by construction, reviewed by a Codex `security`-profile seat before acceptance.
   172	- **V3b** INV-4: premises in the schema and validator, SKILL text (questions end the task; one answering TASK at most). Claude seat; no hook source (the counting is V3a's).
   173	- **V3c** INV-3: `check=` in the ACCEPTANCE contract (SKILL), `revise.yaml` beside task.md in the Worker Playbook, the `regime-check.sh` step; tests. Claude seat (no gate source: the validation-file line is V2b's).
   174	- **V3d** INV-10: idle and first-push computations in `check-regime-boundary.sh` and `accept-task.py` (the latter lands in V5b; V3d adds them to the boundary check only). Claude seat.
   175	- **V4** INV-7: `scripts/design-review.sh` (Claude and Codex runs under their `-review-dot-hNNN` identities), `schemas/design-review.json`, the history anchor and hash check in the gate (two RESULTs, both forms), SKILL paragraph. Operator-routed for the gate part.
   176	- **V5a** INV-8: `.orchestration/<task id>/` paths in the Worker Playbook, task.md copy as the first commit, evidence-shape validation in `regime.yml`, boundary commit reduced to orchestrator records. Claude seat.
   177	- **V5b** INV-9: `scripts/accept-task.py`, cost fields, budgets in `process_tiers`, `check-regime-boundary.sh` budget warning. Claude seat. Size: the sweep, scaffold and gate invocation already exist as commands; the script sequences them, about 200 lines.
   178	- **V6** INV-11: `executable_permgate` session_id and cwd; gate cross-check. Operator-routed, Codex `security` profile review.
   179	
   180	Order: V1, V1c, V1b, V2, V2b, V3a, V3b, V3c, V3d, V4, V5a, V5b, V6. File-disjoint pairs may run concurrently (V1 with V2; V3b with V3d); the gate-source waves (V2b, V3a, V4's gate part) run serially.
   181	
   182	## 7. Thresholds (operator confirmed 2026-10-11)
   183	
   184	revise 2; amendments 2; questions 2; Bot P0/P1 heads 2 (post-RESULT); audit implementation or specification P0-P1 heads 2; PR 15 changed files (the file count excludes `.orchestration/` only) and 500 added lines outside `tests/`, `.orchestration/` and the data list `scripts/legacy-task-ids.txt`; first push 30 minutes; idle 20 minutes; workers 3; audit pool 2; audit once per head; docs tier 1 revise.
   185	
   186	## 8. Disposition of the halted work
   187	
   188	PR #313 and #314 closed unmerged as reference branches (reset records in `.orchestration/acceptance/…-design-reset.md`); PR #315 is a draft per T120's reset record; the four worker seats are removed. Salvaged: the format-2 key set, the tier table, `scripts/legacy-task-ids.txt` and the test ideas of `tests/unit/test_validate_task.py` (V1); `scripts/schemas/audit.json`, the AGENTS.md Audit text, the pre-push hardening and the `AGMSG-AUDIT` record (V2). Dropped with the `redesign` profile: PR #313's `home/dot_codex/modify_private_redesign.config.toml`. T127 (T120's redesign) follows V1 under this regime.
   189	
   190	## 9. Residuals, stated
   191	
   192	- Workers' conduct is checked mechanically only for Claude seats and only after V6; until then the sandbox record is self-reported.
   193	- `pull_request_target` runs with the base repository's token on a public repository: the `regime` job reads PR files as data with `contents: read` only, checks out `main`'s scripts, and never executes anything from the PR; a change to `.github/workflows/regime.yml` itself is a design-tier change under INV-1.
   194	- A repository admin can edit the ruleset; that path is visible on GitHub, not prevented, consistent with the waiver anchor.
   195	- The design-review receipt's anchor in history is only as strong as the `-review-` identity's independence; a fresh headless context per review (V4) is the mitigation, and until V4 lands a seated `review`-profile identity reviews.
   196	- The `regime` job runs `main`'s workflow file, so a change to `regime.yml` is never exercised by its own PR; its logic therefore lives in scripts with unit tests, and a `workflow_dispatch` dry run precedes listing it as required.
   197	- `regime.yml` discipline, stated once: `main` stays at the workspace root (`actions/checkout` default ref under `pull_request_target`); the PR head is fetched as data and read with `git show <head sha>:<path>` into a directory never on `PATH`; the diff range is the merge-base of `github.event.pull_request.head.sha` with `main`, never `github.sha`; `uv run --no-project`; `yaml.safe_load`; no `make`, no script, no dependency file from the PR tree; `permissions: contents: read`; no secrets.
   198	- The seven existing required checks still run on `pull_request` from the PR's own workflow files; INV-1's workflow-edit refusal in the `regime` job is what closes R8 for them.
   199	- Bootstrap: this design was written by the orchestrator that dispatched the abandoned tasks. The reset records carry the operator's waiver form (`DESIGN_RESET_WAIVED_BY=operator`, decision 2026-10-11), this review is the only release, and no further orchestrator-authored design follows under T128; T127 (T120's redesign) is written by another context.
   200	
   201	## 10. Design review (round 7 requested: INV-7's Codex form)
   202	
   203	Round 1 (`.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review.md`, `claude-review-dot-a001`, 2026-10-10T21:15Z, verdict `revise`): INV-7, INV-8, INV-11, INV-12 accepted with notes; INV-1, 2, 3, 4, 5, 6, 9, 10 rejected with corrections; findings F1-F9. v2 adopts every item: the task.md copy and `task_sha256` anchor (F1), the per-task invariant-set rule and the workflow-edit refusal (F2), the gate changes assigned to V2b/V3a/V4 with the category lock, the Bot-wait timeout and the tree-equality rule (F3), the merge backstop as the mandatory point, `original_commit_id`, the audit-JSON source, the Stop-hook budget split and the boundary detector (F4), the single amendment count over every TASK (F5), INV-9/INV-10 moved out of the Stop hook (F6), the reset records corrected to `claude-review-dot-a001` with the waiver form and the thread ids (F7), rule prose in the review tier (F8), premise 1 restated and three premises added (F9); plus the Q5 salvage list, the `make audit-head` target in place of a daemon, the `regime.yml` discipline and the hash note.
   204	
   205	Round 2 (`…-design-review-round2.md`, 21:29Z, verdict `revise`): every round-1 correction confirmed applied; INV-2, INV-3, INV-6 rejected for contradictions v2 introduced, plus routing, cap and premise notes. v3 adopts all of them: `implementing_tasks` is a map of task id to invariant ids inside the hashed keys and the design-on-main precondition is stated (INV-2); `revise.yaml` is a sibling of the byte-identical task.md (INV-3, INV-8, INV-12, V3c, V2b); the question threshold is 2 and audit JSONs count only when their sha256 matches their record (INV-6); V3a is an operator PR with all hook counting, V3b has no hook source, V3c no gate source; the legacy list is excluded from the line cap as data; the `workflow_dispatch` premise is added; the stage-3 sentence names the orchestrator's `make audit-head`; INV-1 names the latest TASK's token and the recommit after each amendment. Round 3 (`…-design-review-round3.md`, 21:33Z, verdict `accept`) confirmed the five edits; its two notes are carried in the acceptance record. v4 (operator direction 2026-10-11, relayed by the review seat's PONG at 22:01Z) splits V1 by responsibility into V1 (validation only) and V1c (the CI check), adds `dotfiles-T128-v1c-regime-ci-check-a01: [INV-1]` to `implementing_tasks` (a hashed key, hence this round), reorders the waves (V1, V1c, V1b, …) and aligns section 7's cap wording with INV-2. Round 4 (`…-design-review-round4.md`, 22:06Z, verdict `accept`) confirmed the split; its note (INV-1's ruleset action is V1c's acceptance record) is carried. v5 answers the Codex Bot's finding on boundary PR #316 (thread 4239305441): INV-3's `ci:<job>` form had no enforcement, so `check=` is now a test selector or a `repro:<id>` whose command and output live in revise.yaml, each with its own regime-job verification. Round 5 (`…-design-review-round5.md`, 22:12Z, verdict `accept`) confirmed it. The Codex Bot then reviewed the second boundary head (c1e2582b) and raised six P1 and four P2 findings that three same-vendor accepts had not: the auditor read the schema and AGENTS.md from the audited head (INV-5 now runs from main as the instruction root with the worktree as data), the CI job had no previous RESULT head (INV-3 now records previous_head in the ACCEPTANCE and revise.yaml, cross-checked by the host gate), ids were compared without sentences (INV-2), `allowed_files: ['*']` derived a cheap tier and a branch copy could claim a legacy id (INV-1, INV-12), and two task records pointed at an abandoned prerequisite. v6 adopts all ten and, because a cross-vendor reviewer found what a same-vendor fresh context did not, INV-7 now requires both a Claude and a Codex review of each design hash. Round 6 (`…-design-review-round6.md`, 22:28Z, verdict `revise`) accepted INV-1, 2, 3, 5, 12 and rejected INV-7: the Bot form produced no receipt, hash or RESULT, so it would have been an orchestrator-written receipt for a review it did not perform (R5). v7 makes the Codex review a `codex exec --sandbox read-only` run under a `codex-review` identity with its own receipt and RESULT, names it in the enforcement row and V4, keeps the Bot's review as swept feedback, and adds the bare-mode skills premise (round-6 INV-5 note, acted on in V2). Round 7 asks the Claude reviewer to confirm INV-7; the Codex review of v6 (hash 25b36e1c) that is already running is reported under `codex-review-dot-h001`, and a Codex confirmation of v7 follows it. Sources are the repository paths under `.orchestration/validation/dotfiles-T128-regime-v3-a01-research/` (`baseline.md`, `practice-evidence.md`, `claude-code-factsheet.md`, `codex-factsheet.md`, `github-factsheet.md`, `method-draft.md`). Receipt: `.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round7.md` (Claude) and `…-design-review-round7-codex.md` (Codex); the whole-file sha256 of this file in both headers.

**Clarifying output and design**
exec
/bin/zsh -lc "nl -ba .orchestration/tasks/dotfiles-T128-regime-v3-a01.md | sed -n '1,205p'; for f in .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review*.md; do echo \"FILE "'$f"; rg -n '"'"'^(reviewed_at:|reviewer:|profile:|design:|round:|INV-[0-9]+:|## Findings|'"\\[P[0-3]\\]|## Residual|Design verdict:)' \""'$f"; done' in ~/Workspace/dotfiles
 succeeded in 189ms:
     1	---
     2	format: 2
     3	task_id: dotfiles-T128-regime-v3-a01
     4	kind: design
     5	security: true
     6	design_review:
     7	  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round7.md
     8	  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
     9	implementing_tasks:
    10	  dotfiles-T128-v1-task-schema-a01: [INV-1]
    11	  dotfiles-T128-v1c-regime-ci-check-a01: [INV-1]
    12	  dotfiles-T128-v1b-pr-caps-a01: [INV-2]
    13	  dotfiles-T128-v2-audit-schema-and-runner-a01: [INV-5]
    14	  dotfiles-T128-v2b-audit-gate-a01: [INV-5]
    15	  dotfiles-T128-v3a-reset-counters-a01: [INV-6]
    16	  dotfiles-T128-v3b-premises-and-amendments-a01: [INV-4]
    17	  dotfiles-T128-v3c-one-fact-per-round-a01: [INV-3]
    18	  dotfiles-T128-v3d-idle-and-first-push-a01: [INV-10]
    19	  dotfiles-T128-v4-design-review-runner-a01: [INV-7]
    20	  dotfiles-T128-v5a-evidence-on-branch-a01: [INV-8]
    21	  dotfiles-T128-v5b-cost-fields-a01: [INV-9]
    22	  dotfiles-T128-v6-permgate-session-a01: [INV-11]
    23	supersedes:
    24	  - dotfiles-T126-regime-v2-a01
    25	  - dotfiles-T124-design-gate-and-reset-rule-a01
    26	reset_of:
    27	  - dotfiles-T124-wave1-task-validator-a01
    28	  - dotfiles-T124-wave3b-audit-grammar-a01
    29	threat_model:
    30	  R1: rounds are judged by models re-reading models and add no deterministic fact, so a wrong premise is patched round after round (T118 20 revises, T119 5 revises and 4 audits; the vendor's own rule is two corrections, then start fresh)
    31	  R2: "hand-written parsers at a trust boundary have an unbounded bypass surface (PR 313: 33 of 52 Bot threads on a 503-line validator with its own YAML parser, written on the false premise that PyYAML is unavailable)"
    32	  R3: "PRs larger than a reviewer can hold (PR 313 20 files +2642, PR 312 37 files +3191; Google: 100 lines reasonable, 1000 too large)"
    33	  R4: task text grown by question-and-amendment (PR 313 6 questions 8 amendments, T119 8 and 8, T120 8 amendments and no RESULT) keeps the under-researched premise
    34	  R5: the orchestrator's artifacts are unaudited and it dispositions findings about itself (T119 audit-finding 2); the reset rule was prose the orchestrator could waive (PR 313 revise round 2)
    35	  R6: "the auditor becomes a serial queue when audits run once per round in one tab (measured: 4 audits about 1.3 h of T119's 11.1 h; the rounds, not the audits, were the cost)"
    36	  R7: cost is unmeasured (every acceptance record says cost n/a) so no stage can be weighed against its value
    37	  R8: a PR can change the check that judges it (a pull_request workflow runs the PR head's workflow file); host-side evidence is whatever the orchestrator copies into the gate's cwd
    38	trust_anchors:
    39	  - agmsg message history (append-only, read through history.sh) for who did what and when; GitHub for PR, CI, Bot, ruleset and merge state; the main checkout for files, never the gate's cwd
    40	  - JSON Schema documents validated by the jsonschema library (PyYAML for front matter) for task files, audit verdicts, design-review receipts and evidence; model verdicts produced under schema (codex exec --output-schema, server-side strict; claude -p --json-schema)
    41	  - mechanical checks run from main's workflow file as a pull_request_target required status check that reads PR files as data and executes nothing from the PR; required workflows are organization-only, so this is the main-pinned form available to a user-owned repository
    42	  - the operator waiver is visible, not prevented (acceptance record, boundary PR body, check-regime-boundary)
    43	  - a reset is released only by a redesign written in a context other than the one that wrote the abandoned task, or by the operator
    44	invariants:
    45	  INV-1: "every task is a format-2 file whose front matter validates against schemas/task.json (jsonschema + PyYAML, no hand-written parser; every allowed_files entry starts with a literal path segment and a wildcard entry derives the tier of every design-tier path its literal prefix can cover); legacy task ids are grandfathered only for files under .orchestration/tasks/ on main, never for a branch copy; the tier (docs, review, design) is derived from allowed_files by the shared high-risk module, with the regime's own rule prose (home/dot_config/claude/rules/**, the agmsg-orchestration SKILL, AGENTS.md, README) listed in the review tier, and selects the pipeline from process_tiers in agent-config.yaml; every AGMSG-TASK for the task, the first and each amendment, carries task_sha256= of the task file as sent, the worker commits the file byte-identical to .orchestration/<task id>/task.md (first commit, recommitted after each amendment), the CI regime job validates that copy with main's schema and refuses a PR that changes .github/workflows/** unless its task.md is design tier and lists the file, the host gate compares the copy's sha256 with the latest AGMSG-TASK's token in history, and the regime check binds only once the ruleset lists it as required (an operator action named in V1's acceptance record); the orchestrator can add or skip a stage only with an operator waiver named in the acceptance record"
    46	  INV-2: "a PR is mergeable only within the caps the CI regime job enforces from main's workflow (at most 15 changed files and 500 added lines outside tests/, .orchestration/ and the data list scripts/legacy-task-ids.txt), and its task.md invariants equal the design's as a set of ids and byte-for-byte as sentences (the design read from main, never from the PR); the design file must be on main (through a boundary PR) before the implementing TASK is dispatched and the regime job fails closed when the design named by task.md is absent from main; exceeding a cap is a split, never a finding to disposition (the cap changes the unit of work: T116 +529 and T118 +881 would have been split)"
    47	  INV-3: "a revise round is admissible only when it adds a new deterministic check: the AGMSG-ACCEPTANCE status=revise carries check=<tests/<file>::<name> | repro:<id>> and previous_head=<the RESULT head being revised>, the worker records both in .orchestration/<task id>/revise.yaml (a sibling file; task.md stays byte-identical to the dispatched file) together with the command and pasted output for a repro, the CI regime job verifies, for a test selector, that the named test file exists on the head and differs between the recorded previous_head and the head (git diff <previous_head> <head> -- <test file> non-empty) and, for a repro, that revise.yaml carries a non-empty command and output for that id, and the host gate, which reads history, verifies that previous_head equals the head of the previous AGMSG-RESULT for the task and requires the same id in the validation file; a finding that cannot become a check is dispositioned, never iterated"
    48	  INV-4: a task file carries premises, each with the command and pasted output that verified it before dispatch; a worker question (AGMSG-PONG status=question) is a specification defect answered by at most one further AGMSG-TASK; amendments are every AGMSG-TASK for the task_id after the first, whatever its wording, and the second one is INV-6's count, which withdraws the task to design through INV-6's merge backstop and Stop signal
    49	  INV-5: "the task-level audit is a headless read-only run whose instruction root is the trusted main checkout and whose schema is main's schemas/audit.json: codex exec --output-schema <main>/schemas/audit.json -C <main> with the detached worktree at the head added as a read-only data directory (--add-dir), so the audited PR controls neither the schema nor the AGENTS.md the auditor reads; the fallback claude -p --json-schema from the same root with --add-dir <worktree>, --bare when an API key is set and otherwise with project and user hooks disabled started when CI is green and the Codex Bot has reviewed the head or 15 minutes have passed without a Bot review (recorded as bot: none), at most once per RESULT head, pooled two at a time; the gate accepts an audit of an earlier head only when git diff --quiet <audited head> <HEAD> -- . ':!.orchestration' holds (an evidence-only revision), otherwise a new audit is required; its input includes the task's invariants and premises, the worker's evidence, the orchestrator's task file, amendments, acceptance record with its dispositions, the head's pr-feedback JSON and the previous round's audit JSON; the schema lists findings {priority, confidence, category in {specification, implementation, evidence, orchestration, conformance}, path, line, rationale} and the per-invariant map before the verdict, and the prompt asks for the rationale before each verdict; the runner, under the identity claude-audit-dot-h001 or codex-audit-dot-h001 on the orchestrator's host, records the JSON's sha256 in agmsg history (AGMSG-AUDIT v1 task_id= head= sha256= auditor=) before the gate reads it, an anchor that prevents edits after the record and not fabrication before it; the gate reads the verdict and categories from the JSON, and orchestration and conformance findings at P0-P2 accept only an operator waiver or a design reset, never not-applicable"
    50	  INV-6: "the reset rule's mandatory point is the merge backstop in scripts/require-crit-review.py, with the orchestrator's Stop hook (Claude Stop hook, Codex [hooks].Stop) as the early signal, soft on both runtimes by their documented caps; counts come from history for the hook and the gate (revises = RESULTs for the task_id minus one, threshold 2; amendments = AGMSG-TASKs after the first, threshold 2; AGMSG-PONG status=question, threshold 2) and from GitHub and main-checkout files for the gate and the boundary check only (Codex Bot P0 or P1 on two heads after the first RESULT, from original_commit_id on review_comment items recorded by pr-feedback.py; an audit implementation or specification finding at P0-P1 on two heads, from .orchestration/validation/<task>-audit-<sha7>.json in the main checkout, each counted only when its sha256 matches its AGMSG-AUDIT record); when a count is reached the gate refuses the merge until a reset record names a redesign task whose design RESULT comes from an identity other than the task's author, or the operator sets DESIGN_RESET_WAIVED_BY; check-regime-boundary.sh reports a closed-unmerged PR whose task has no reset record and a task over any count with neither an accepted acceptance record nor a reset record"
    51	  INV-7: "the design tier adds, before any code is dispatched, two design reviews of the same design hash: a fresh Claude context on the review profile (a headless run or a seated -review- identity; the review profile is the same model and effort as deep, so the lever is the separate context) and a Codex read-only review (codex exec --sandbox read-only on the review profile under a codex-review identity: headless through V4's runner, or seated until V4); each receipt is a schema document naming the design file's canonical hash over invariants, threat_model, trust_anchors, implementing_tasks and premises, each is announced by an AGMSG-RESULT from its reviewing identity, and both RESULTs precede the implementing AGMSG-TASK in history; the Codex Bot's review of a boundary PR is swept feedback, never a design receipt; a change to the hashed keys needs new reviews; the gate accepts the whole-file sha256 form for receipts written before V4 lands"
    52	  INV-8: "worker evidence (the task.md copy, revise.yaml, report, validation, sandbox, learning, autoskill, worker review JSON) is committed on the PR branch under .orchestration/<task id>/ before the final RESULT so the Bot, CI and the gate read the same files from the audited head; the orchestrator's records (audit JSON, acceptance, pr-feedback) stay under .orchestration/validation and .orchestration/acceptance in the boundary commit because the merge is --match-head-commit"
    53	  INV-9: "every acceptance record carries measured cost (rounds, amendments, questions, wall time TASK to final RESULT from history timestamps, audit count, Bot threads, tokens: total_cost_usd from claude -p JSON, turn.completed.usage from codex exec --json, per-message usage from the seat's session transcript) written by accept-task.py; each tier has a budget, the acceptance record names the operator decision when it is exceeded, and check-regime-boundary.sh warns; headless runs carry --max-budget-usd"
    54	  INV-10: at most three concurrent workers with pairwise-disjoint allowed_files; the first push (a draft PR) lands within 30 minutes of the TASK and a seated worker is not idle for 20 minutes while a dispatchable task exists, both computed in check-regime-boundary.sh and accept-task.py from history.sh timestamps and gh pr view, never in the Stop hook; headless reviews and audits do not count as workers
    55	  INV-11: permgate records session_id and cwd per decision, and the gate compares a Claude worker's permission-gated Bash count in the task window with the sandbox record (an understated record is refused); Codex workers cannot escalate and are not covered
    56	  INV-12: "every rule above is exercised by a unit test that fails when the rule is removed, including one per gaming path (a schema-valid task with a prose cap bypass, a revise without a named check, a revise list appended to the hashed task.md, an AGMSG-TASK without amendment= that still counts, an evidence-only relabel of a code change caught by the tree-equality check, a wave-table rewrite after review, an audit JSON edited after its history record, a receipt whose hash predates a key change, a reset record naming the author's own identity, a Bot-skipped head whose audit never starts, a single PR split only in the task file, a branch task.md claiming a legacy id, allowed_files of ['*'] or a wildcard first segment, an invariant sentence weakened under its id, a schema or AGENTS.md edited on the audited head); legacy task ids are grandfathered by the checked-in list scripts/legacy-task-ids.txt, which only shrinks and is excluded from the line cap as data"
    57	premises:
    58	  - claim: PyYAML is already installed by uv in the Makefile and CI; jsonschema is not yet named anywhere and V1 adds --with jsonschema; both resolve through uv on this host
    59	    command: "grep -n 'with pyyaml\\|jsonschema' Makefile .github/workflows/*.yml; uv run --no-project --with jsonschema --with pyyaml python -c 'import jsonschema, yaml; print(jsonschema.__version__, yaml.__version__)'"
    60	    output: "Makefile:189 and :203 and agent-assets.yml:35 use --with pyyaml; no jsonschema anywhere; 4.26.0 6.0.3"
    61	  - claim: required workflows are organization-only; pull_request_target runs the base branch's workflow file and is eligible as a required status check
    62	    command: "WebFetch docs.github.com available-rules-for-rulesets (enterprise-cloud) and troubleshooting-required-status-checks"
    63	    output: "Ruleset workflows can be configured at the organization or enterprise level; required checks count when triggered by push, pull_request, pull_request_review, pull_request_target, deployment, deployment_status; pull_request_target runs in the context of the default branch of the base repository"
    64	  - claim: codex exec --output-schema is enforced server-side as a strict JSON schema; codex 0.161.0 rejects --full-auto and -a on exec
    65	    command: "codex exec --help; read codex-rs/exec/src/lib.rs and codex-api/src/common.rs at rust-v0.161.0"
    66	    output: "text.format = {type: json_schema, strict: true, schema}; error: unexpected argument '--full-auto' found; approval policy for exec is set with -c approval_policy=never"
    67	  - claim: claude -p --bare requires an API key and skips hooks; without --bare a -p run executes the project's hooks; --json-schema returns structured_output; --max-budget-usd caps spend
    68	    command: "WebFetch code.claude.com/docs/en/headless and cli-reference"
    69	    output: "--bare never reads OAuth credentials or the system keychain; set ANTHROPIC_API_KEY; without --bare -p runs the hooks in a project's .claude/settings.json; the structured output is in the structured_output field; spend can pass the cap, so leave headroom"
    70	  - claim: the vendor's own reset rule is two corrections
    71	    command: "WebFetch code.claude.com/docs/en/best-practices"
    72	    output: "If you've corrected Claude more than twice on the same issue in one session, the context is cluttered with failed approaches. Run /clear and start fresh with a more specific prompt"
    73	  - claim: the audit was not the wall-clock bottleneck
    74	    command: "stat .orchestration/validation/dotfiles-T119-*-audit-*.md; history.sh dotfiles-conformance (TASK 2026-10-09T21:26Z to ACCEPTANCE 2026-10-10T08:32Z)"
    75	    output: "four audit files written 11:48, 13:55, 15:52, 17:23 local, each run 15-25 minutes, about 1.3 h of an 11.1 h task"
    76	  - claim: both runtimes' Stop hooks are soft signals, not hard stops, so the merge gate is the mandatory point
    77	    command: "WebFetch learn.chatgpt.com/docs/hooks; WebFetch code.claude.com/docs/en/hooks (Stop section)"
    78	    output: "Codex: decision block doesn't reject the turn but injects a continuation prompt; Claude: 8-consecutive-continuation cap that resets each time Claude calls a tool"
    79	  - claim: the seat's session transcript carries per-message token usage on this host
    80	    command: "grep -o '\"usage\":{[^}]*}' ~/.claude/projects/-Users-a0004262-Workspace-dotfiles--claude-worktrees-worker-c/3747b995-3bb1-4c51-8421-4b1e672b442a.jsonl | tail -1; grep -c '\"usage\"' <same file>"
    81	    output: "usage with input_tokens, cache_creation_input_tokens, cache_read_input_tokens, output_tokens; 5168 usage entries (format internal to Claude Code per its docs)"
    82	  - claim: history.sh truncates to 20 rows by default, so counters read the storage facade or pass a limit
    83	    command: "history.sh dotfiles-conformance | wc -l; history.sh dotfiles-conformance --limit 600 | wc -l"
    84	    output: "20; 256 (the whole team history)"
    85	  - claim: "workflow_dispatch runs a workflow only once its file is on the default branch, so regime.yml is merged unlisted, dry-run from main against a closed PR, then listed as required"
    86	    command: "WebFetch docs.github.com events-that-trigger-workflows (workflow_dispatch)"
    87	    output: "This event will only trigger a workflow run if the workflow file exists on the default branch"
    88	  - claim: "bare mode loads skills from the .claude/skills/ folder of a directory named with --add-dir, so the claude fallback must refuse a head that changes .claude/skills/**"
    89	    command: "WebFetch code.claude.com/docs/en/headless (bare mode section)"
    90	    output: "bare mode loads skills from its .claude/skills/ folder (of directories named with --add-dir)"
    91	
    92	---
    93	
    94	# AGMSG-TASK dotfiles-T128-regime-v3-a01 — DESIGN: regime v3, the redesign after the 2026-10-10 halt
    95	
    96	Drafted 2026-10-11 (local) by the orchestrator seat `claude-deep-dot` under a recorded bootstrap exception (operator decision 2026-10-11: the orchestrator drafts, a fresh context on the review profile must accept before any implementing task is dispatched). Operator direction (pasted 2026-10-11): when substantive findings repeat, the design, implementation or verification is wrong and a mechanism must force the redo; prose alone repeats the mistake; the auditor must be able to find the orchestrator's and the worker's mistakes; efficiency, quality and cost are optimised together; the auditor must not become the bottleneck and the audit stages must be chosen; all of it grounded in the tools' official documentation and current practice. Research inputs: fact sheets on Claude Code 2.1.293, Codex CLI 0.161.0, GitHub rulesets and Actions, and the research literature, read 2026-10-11; the measured baseline below.
    97	
    98	## 1. Finding: the fix program tripped its own rule
    99	
   100	By T126 INV-6 as written: wave 1 (PR #313) 8 amendments (limit 4) and 2 revises (limit 2); wave 3b (PR #314) Bot P1 on two post-RESULT heads. The orchestrator was drafting a waiver for #313. T120 was reset only on the operator's question. The regime is therefore reset here by its own rule; this document is the redesign, and T126 and T124 are superseded (their accepted ideas are kept where named).
   101	
   102	Measured baseline (history + GitHub):
   103	
   104	| task | PR | files | +lines | amendments | questions | revises | audits (incorrect) | Bot threads (heads) | P0/P1 | wall |
   105	|---|---|---|---|---|---|---|---|---|---|---|
   106	| T114 | - | - | - | 0 | 0 | 6 | 3 (3) | - | - | 21.5h |
   107	| T118 | 310 | 35 | 881 | 7 | 0 | 20 | 8 (7) | 16 (7) | 0 | 10.6h |
   108	| T119 | 312 | 37 | 3191 | 8 | 8 | 5 | 4 (4) | 25 (11) | 7 | 11.1h |
   109	| T120 | 315 | 19 | 1489 | 8 | 1 | 0 | 0 | 15 (5) | 8 | reset |
   110	| T124 W1 | 313 | 20 | 2642 | 8 | 6 | 2 | 0 | 52 (10) | 31 | halted, reset |
   111	| T124 W3b | 314 | 9 | 1462 | 5 | 0 | 0 | 0 | 24 (4) | 2 | halted, reset |
   112	
   113	Every acceptance record to date says `cost: n/a`.
   114	
   115	## 2. Root causes, each with its evidence
   116	
   117	R1 to R8 in the front matter. The literature behind R1: intrinsic self-correction without an external signal degrades after the first round (Huang et al. 2023); a second review round on the same artifact raised recall slightly and false positives by 62% (arXiv 2603.16244); multi-round review degrades with rounds (MCR-Bench); revising an already-correct state loses correct work unless verifier evidence is bound to the exact code state (arXiv 2607.24604). Behind R3: Google's review study (median change 24 lines, ~90% under 10 files) and its CL-size guidance. Behind R5 and R6: a judge without a reference is lenient and a reference flips 9-85% of verdicts toward correct (2607.12885); format-restricted generation degrades reasoning, so verdicts reason first and then fill the schema (2408.02442); Anthropic's harness-design post: a standalone skeptical evaluator is tractable where a self-critical generator is not, and the evaluator is worth its cost only where the task exceeds the model's reliable solo capability, which is what the tier table encodes.
   118	
   119	## 3. Principles (each names what it reuses and what it deletes)
   120	
   121	- **P1 One deterministic fact per round (INV-3).** Reuses tests/unit, CI, `pr-feedback.py`. Deletes free-form revise rounds and the audit-per-round habit.
   122	- **P2 Declarative over imperative at trust boundaries (INV-1, INV-5, INV-7).** Reuses `jsonschema`, PyYAML, `codex exec --output-schema`, `claude -p --json-schema`. Deletes the bespoke YAML parser, the glob NFA, the prose verdict grammar, regex parsing of `.last.md`, and the T126 "process_tiers.json next to the module" indirection (the validator reads the manifest with PyYAML).
   123	- **P3 Small one-invariant PRs enforced in CI (INV-2).** Reuses GitHub required checks and the strict up-to-date ruleset already in force. Deletes waves declared inside a task file.
   124	- **P4 Main-pinned mechanical checks in CI; host gate only for history-anchored rules (INV-1, INV-2, INV-8 in CI; INV-3, INV-5 record, INV-6, INV-7 anchor, INV-11 on the host).** Reuses `pull_request_target`, the `changes` job pattern that reports success for an `.orchestration`-only diff. Deletes PR #313's `REVIEW_TREE` idea (never on `main`) and the copy step of untracked evidence into the gate's cwd. The host gate `make require-crit-review` keeps its evidence rules and changes three of them in named waves: the audit verdict and categories come from the schema JSON with the `AGMSG-AUDIT` record and the category lock (V2b), the reset backstop and the Bot-head count (V3a), the history-anchored design review (V4); it continues to run from the orchestrator's main checkout.
   125	- **P5 Research before dispatch; a question ends the task, not amends it (INV-4).** Reuses history (`amendment=`, `status=question`). Deletes the amendment-per-question practice. The task file's `premises` block is the mechanical residue of "verify every CLI constraint by running the real command".
   126	- **P6 Reset is mechanical, loop-time, and released only by another context or the operator (INV-6).** Reuses `scripts/require-crit-review.py` as the mandatory point, `agent-stop-gate.sh` and the Codex `[hooks].Stop` as the early signal (both soft by their documented caps: Claude's 8-continuation cap, Codex's continuation prompt), `check-regime-boundary.sh` for the re-dispatch detector. Deletes the orchestrator-written redesign (the redesign author is a `review`-profile seat or a fresh headless context; the `redesign` profile of T124 v4 is dropped: `review` is the same model and effort as `deep`, so independence of context is the whole lever, and T124 round 1 showed it works).
   127	- **P7 Audit staging by tier; the auditor never serializes the pipeline (INV-5, process_tiers).** See section 4.
   128	- **P8 Cost measured, budgets per tier (INV-9).** Reuses the JSON cost fields the runtimes already emit and the session transcripts. Deletes `cost: n/a`.
   129	- **P9 Parallelism with disjoint files and early push (INV-10).** Reuses `herdr-agents --add-worker`, draft PRs.
   130	- **P10 Routing stays by boundary.** Claude-boundary sources to a Codex seat, Codex-boundary to a Claude seat, permgate and shared gate sources to the operator, as the agmsg-orchestration skill's step 3 states; nothing here changes that.
   131	
   132	## 4. Audit stages (process_tiers; the one table the validator reads)
   133	
   134	| stage | who | when | tier docs | tier review | tier design | cost |
   135	|---|---|---|---|---|---|---|
   136	| 0 design review | a fresh Claude context on the review profile and a Codex read-only review of the same hash, schema receipts (INV-7) | before any code | - | - | required | minutes |
   137	| 1 worker checks | worker in its sandbox: invariant tests first, shellcheck, unit tests | before every push | required | required | required | none for the regime |
   138	| 2 CI + Bot | main-pinned `regime` check (schema, caps, evidence shape) + unit tests + Codex Bot | every push, in parallel | required | required | required | none |
   139	| 3 schema audit | headless read-only `codex exec --output-schema`, pooled 2, started by `make audit-head` once CI is green and the Bot reviewed or 15 min passed, once per RESULT head, reused for an evidence-only head by tree equality (INV-5) | per RESULT head | - | required | required, with invariant map and permgate window | the scarce resource, now off the critical path |
   140	| 4 acceptance | orchestrator: sweep, dispositions, record, host gate, merge `--match-head-commit` | per RESULT | required | required | required | minutes |
   141	
   142	Tier derivation: docs = prose-only `allowed_files` outside the regime's own rule prose (`home/dot_config/claude/rules/**`, the agmsg-orchestration SKILL, `AGENTS.md`, README), which is review tier by explicit list; review = the existing review-tier paths (scripts, hooks, tests, templates); design = the explicit design-tier list from T124 INV-2 v3 (install/**, setup.sh, the gate scripts, `executable_herdr-agents`, `executable_permgate`, Codex and Claude policy, sandbox and permission settings, credential helpers). Round limits: docs 1 revise; review and design 2 revises then reset. Profiles: worker `standard` (docs `express`), review `review`, audit `audit`.
   143	
   144	Why stage 3 is not the queue: the orchestrator starts it with `make audit-head` when the RESULT arrives (the wait on CI and the Bot is inside the target), it runs concurrently (pool of two, each in its own detached worktree), once per head, and an evidence-only head reuses the earlier audit by tree equality; the measured cost of the old serial form was 1.3 h of 11.1 h, so the throughput levers are P1 and P6, and the pool removes the residual queue.
   145	
   146	## 5. Enforcement map
   147	
   148	| invariant | enforcement point |
   149	|---|---|
   150	| INV-1 | `.github/workflows/regime.yml` (`pull_request_target`, required check `regime`: validates `.orchestration/<task id>/task.md` from the PR head read as data, refuses workflow edits outside a design-tier task), `scripts/validate-task.py` (schema + PyYAML, about 80 lines), `schemas/task.json`, `scripts/lib/high_risk_paths.py` (new module: tier lists and `tier_of`), `scripts/legacy-task-ids.txt` (grandfather list), `process_tiers` in the manifest; host gate compares the copy's sha256 with `task_sha256=` in history (V3a) |
   151	| INV-2 | `regime.yml` step with `scripts/pr-caps.sh` and the task.md invariant-id comparison against the design's `implementing_tasks` |
   152	| INV-3 | `regime-check.sh` step: a test selector named in `.orchestration/<task id>/revise.yaml` (sibling of the byte-identical task.md) exists on the head and differs from the previous RESULT head; a `repro:<id>` carries command and output there; the host gate's matching validation-file line is V2b's |
   153	| INV-4 | `scripts/validate-task.py` (premises required for code and design tasks); `agent-stop-gate.sh` early signal on the second AGMSG-TASK or second PONG question; the merge backstop is INV-6's |
   154	| INV-5 | `schemas/audit.json` (findings and invariant map before verdict), `scripts/audit-head.sh` (about 100 lines: detached worktree, `codex exec`, fallback, sha256 to history under the audit identity, `.last.md` render; PR #314's hardening kept), `make audit-head` target around `gh pr checks --watch` and the SKILL's Bot list loop with its 15-minute `bot: none` rule (no daemon), `AGENTS.md` Audit section; gate: JSON verdict and categories, `AGMSG-AUDIT` lookup, category lock, tree-equality acceptance of an earlier head (V2b) |
   155	| INV-6 | `scripts/require-crit-review.py` (mandatory: history counts, Bot heads from `original_commit_id` recorded by `scripts/pr-feedback.py`, audit heads from the main checkout's audit JSONs whose sha256 matches their `AGMSG-AUDIT` record, reset record or `DESIGN_RESET_WAIVED_BY`), `scripts/agent-stop-gate.sh` and the manifest's `codex.hooks` Stop entry (early signal, history counts only, within the 3 s history budget), `scripts/check-regime-boundary.sh` (closed-unmerged PR without a reset record; over-count task without an accepted or reset record; waiver listing) |
   156	| INV-7 | `scripts/design-review.sh` + `schemas/design-review.json`: two headless runs per design hash, `claude -p` under `claude-review-dot-hNNN` and `codex exec --sandbox read-only` under `codex-review-dot-hNNN`, each joining for the run and sending its RESULT; gate: both RESULTs precede the implementing TASK, both hashes recomputed, whole-file form accepted for pre-V4 receipts |
   157	| INV-8 | worker writes under `.orchestration/<task id>/` on the branch (task.md copy first); `regime.yml` validates the evidence JSON shapes; the gate's existing path rules keep the orchestrator's records under `validation/` and `acceptance/` |
   158	| INV-9 | `scripts/accept-task.py` (sweep, dispositions scaffold, record rows, gate invocation, merge command, cost fields), budgets in `process_tiers`, `check-regime-boundary.sh` warning |
   159	| INV-10 | `scripts/check-regime-boundary.sh` and `scripts/accept-task.py` from `history.sh` timestamps (storage facade or `--limit`, never the 20-row default) and `gh pr view` |
   160	| INV-11 | `executable_permgate` (operator-routed, Codex security review) + gate cross-check |
   161	| INV-12 | one test module per script; `make unit-test` in CI; the auditor checks per PR that no new hand-written parser sits at a trust boundary (a `conformance` finding) |
   162	| prose | SKILL, `agmsg-orchestration.md`, `pr-integration.md`, `crit-review.md`, `model-selection.md`, README: each wave edits only the sections it implements |
   163	
   164	## 6. Waves (one PR, one invariant, within INV-2's caps; each task file reviewed by a fresh context before dispatch)
   165	
   166	- **V1** INV-1, validation only (operator direction 2026-10-11, relayed through the review seat; also the cap: the undivided V1 sat at 500 added lines): `schemas/task.json`, `scripts/validate-task.py`, `scripts/lib/high_risk_paths.py`, `scripts/legacy-task-ids.txt` (from PR #313; data, excluded from the line cap), `tests/unit/test_validate_task.py`. Claude seat. Design tier: this review is its stage 0. Precondition: this design is on `main` through a boundary PR before V1's TASK is dispatched.
   167	- **V1c** INV-1, the CI check (after V1): `scripts/regime-check.sh`, `.github/workflows/regime.yml` (task.md validation, workflow-edit refusal, `workflow_dispatch` dry run), `tests/unit/test_regime_check.py`, `process_tiers` in the manifest, SKILL step 3 paragraph, README sentence. Claude seat. Acceptance names the operator action that lists `regime` as a required check, after the dry run from `main` against a closed PR. Two tasks map to INV-1 as V2 and V2b map to INV-5.
   168	- **V1b** INV-2 (after V1c): `scripts/pr-caps.sh`, the caps and invariant-id steps in `regime-check.sh`, tests, one SKILL sentence.
   169	- **V2** INV-5 runner: `schemas/audit.json` (PR #314's, reordered), `scripts/audit-head.sh` with PR #314's hardening, `make audit-head`, `AGENTS.md` Audit section, tests, the SKILL's task-level audit bullet. Claude seat.
   170	- **V2b** INV-5 gate: `scripts/require-crit-review.py` reads the JSON verdict and categories, requires the `AGMSG-AUDIT` record, locks orchestration and conformance at P0-P2 to waiver or reset, accepts an earlier audited head by tree equality, and requires the INV-3 `check=` line in the validation file; tests. Operator-routed gate source (delegable to a Claude seat with recorded opt-in).
   171	- **V3a** INV-6: `scripts/pr-feedback.py` (`original_commit_id` on review_comment items), `require-crit-review.py` reset backstop and `task_sha256` comparison, `agent-stop-gate.sh` history counts (revises, amendments, questions) as the early signal, the Codex Stop entry in the manifest and its rendered template, `check-regime-boundary.sh` detector and waiver listing; tests. Three boundaries in one PR (gate source, Claude hook source, Codex hook source): an operator PR by construction, reviewed by a Codex `security`-profile seat before acceptance.
   172	- **V3b** INV-4: premises in the schema and validator, SKILL text (questions end the task; one answering TASK at most). Claude seat; no hook source (the counting is V3a's).
   173	- **V3c** INV-3: `check=` in the ACCEPTANCE contract (SKILL), `revise.yaml` beside task.md in the Worker Playbook, the `regime-check.sh` step; tests. Claude seat (no gate source: the validation-file line is V2b's).
   174	- **V3d** INV-10: idle and first-push computations in `check-regime-boundary.sh` and `accept-task.py` (the latter lands in V5b; V3d adds them to the boundary check only). Claude seat.
   175	- **V4** INV-7: `scripts/design-review.sh` (Claude and Codex runs under their `-review-dot-hNNN` identities), `schemas/design-review.json`, the history anchor and hash check in the gate (two RESULTs, both forms), SKILL paragraph. Operator-routed for the gate part.
   176	- **V5a** INV-8: `.orchestration/<task id>/` paths in the Worker Playbook, task.md copy as the first commit, evidence-shape validation in `regime.yml`, boundary commit reduced to orchestrator records. Claude seat.
   177	- **V5b** INV-9: `scripts/accept-task.py`, cost fields, budgets in `process_tiers`, `check-regime-boundary.sh` budget warning. Claude seat. Size: the sweep, scaffold and gate invocation already exist as commands; the script sequences them, about 200 lines.
   178	- **V6** INV-11: `executable_permgate` session_id and cwd; gate cross-check. Operator-routed, Codex `security` profile review.
   179	
   180	Order: V1, V1c, V1b, V2, V2b, V3a, V3b, V3c, V3d, V4, V5a, V5b, V6. File-disjoint pairs may run concurrently (V1 with V2; V3b with V3d); the gate-source waves (V2b, V3a, V4's gate part) run serially.
   181	
   182	## 7. Thresholds (operator confirmed 2026-10-11)
   183	
   184	revise 2; amendments 2; questions 2; Bot P0/P1 heads 2 (post-RESULT); audit implementation or specification P0-P1 heads 2; PR 15 changed files (the file count excludes `.orchestration/` only) and 500 added lines outside `tests/`, `.orchestration/` and the data list `scripts/legacy-task-ids.txt`; first push 30 minutes; idle 20 minutes; workers 3; audit pool 2; audit once per head; docs tier 1 revise.
   185	
   186	## 8. Disposition of the halted work
   187	
   188	PR #313 and #314 closed unmerged as reference branches (reset records in `.orchestration/acceptance/…-design-reset.md`); PR #315 is a draft per T120's reset record; the four worker seats are removed. Salvaged: the format-2 key set, the tier table, `scripts/legacy-task-ids.txt` and the test ideas of `tests/unit/test_validate_task.py` (V1); `scripts/schemas/audit.json`, the AGENTS.md Audit text, the pre-push hardening and the `AGMSG-AUDIT` record (V2). Dropped with the `redesign` profile: PR #313's `home/dot_codex/modify_private_redesign.config.toml`. T127 (T120's redesign) follows V1 under this regime.
   189	
   190	## 9. Residuals, stated
   191	
   192	- Workers' conduct is checked mechanically only for Claude seats and only after V6; until then the sandbox record is self-reported.
   193	- `pull_request_target` runs with the base repository's token on a public repository: the `regime` job reads PR files as data with `contents: read` only, checks out `main`'s scripts, and never executes anything from the PR; a change to `.github/workflows/regime.yml` itself is a design-tier change under INV-1.
   194	- A repository admin can edit the ruleset; that path is visible on GitHub, not prevented, consistent with the waiver anchor.
   195	- The design-review receipt's anchor in history is only as strong as the `-review-` identity's independence; a fresh headless context per review (V4) is the mitigation, and until V4 lands a seated `review`-profile identity reviews.
   196	- The `regime` job runs `main`'s workflow file, so a change to `regime.yml` is never exercised by its own PR; its logic therefore lives in scripts with unit tests, and a `workflow_dispatch` dry run precedes listing it as required.
   197	- `regime.yml` discipline, stated once: `main` stays at the workspace root (`actions/checkout` default ref under `pull_request_target`); the PR head is fetched as data and read with `git show <head sha>:<path>` into a directory never on `PATH`; the diff range is the merge-base of `github.event.pull_request.head.sha` with `main`, never `github.sha`; `uv run --no-project`; `yaml.safe_load`; no `make`, no script, no dependency file from the PR tree; `permissions: contents: read`; no secrets.
   198	- The seven existing required checks still run on `pull_request` from the PR's own workflow files; INV-1's workflow-edit refusal in the `regime` job is what closes R8 for them.
   199	- Bootstrap: this design was written by the orchestrator that dispatched the abandoned tasks. The reset records carry the operator's waiver form (`DESIGN_RESET_WAIVED_BY=operator`, decision 2026-10-11), this review is the only release, and no further orchestrator-authored design follows under T128; T127 (T120's redesign) is written by another context.
   200	
   201	## 10. Design review (round 7 requested: INV-7's Codex form)
   202	
   203	Round 1 (`.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review.md`, `claude-review-dot-a001`, 2026-10-10T21:15Z, verdict `revise`): INV-7, INV-8, INV-11, INV-12 accepted with notes; INV-1, 2, 3, 4, 5, 6, 9, 10 rejected with corrections; findings F1-F9. v2 adopts every item: the task.md copy and `task_sha256` anchor (F1), the per-task invariant-set rule and the workflow-edit refusal (F2), the gate changes assigned to V2b/V3a/V4 with the category lock, the Bot-wait timeout and the tree-equality rule (F3), the merge backstop as the mandatory point, `original_commit_id`, the audit-JSON source, the Stop-hook budget split and the boundary detector (F4), the single amendment count over every TASK (F5), INV-9/INV-10 moved out of the Stop hook (F6), the reset records corrected to `claude-review-dot-a001` with the waiver form and the thread ids (F7), rule prose in the review tier (F8), premise 1 restated and three premises added (F9); plus the Q5 salvage list, the `make audit-head` target in place of a daemon, the `regime.yml` discipline and the hash note.
   204	
   205	Round 2 (`…-design-review-round2.md`, 21:29Z, verdict `revise`): every round-1 correction confirmed applied; INV-2, INV-3, INV-6 rejected for contradictions v2 introduced, plus routing, cap and premise notes. v3 adopts all of them: `implementing_tasks` is a map of task id to invariant ids inside the hashed keys and the design-on-main precondition is stated (INV-2); `revise.yaml` is a sibling of the byte-identical task.md (INV-3, INV-8, INV-12, V3c, V2b); the question threshold is 2 and audit JSONs count only when their sha256 matches their record (INV-6); V3a is an operator PR with all hook counting, V3b has no hook source, V3c no gate source; the legacy list is excluded from the line cap as data; the `workflow_dispatch` premise is added; the stage-3 sentence names the orchestrator's `make audit-head`; INV-1 names the latest TASK's token and the recommit after each amendment. Round 3 (`…-design-review-round3.md`, 21:33Z, verdict `accept`) confirmed the five edits; its two notes are carried in the acceptance record. v4 (operator direction 2026-10-11, relayed by the review seat's PONG at 22:01Z) splits V1 by responsibility into V1 (validation only) and V1c (the CI check), adds `dotfiles-T128-v1c-regime-ci-check-a01: [INV-1]` to `implementing_tasks` (a hashed key, hence this round), reorders the waves (V1, V1c, V1b, …) and aligns section 7's cap wording with INV-2. Round 4 (`…-design-review-round4.md`, 22:06Z, verdict `accept`) confirmed the split; its note (INV-1's ruleset action is V1c's acceptance record) is carried. v5 answers the Codex Bot's finding on boundary PR #316 (thread 4239305441): INV-3's `ci:<job>` form had no enforcement, so `check=` is now a test selector or a `repro:<id>` whose command and output live in revise.yaml, each with its own regime-job verification. Round 5 (`…-design-review-round5.md`, 22:12Z, verdict `accept`) confirmed it. The Codex Bot then reviewed the second boundary head (c1e2582b) and raised six P1 and four P2 findings that three same-vendor accepts had not: the auditor read the schema and AGENTS.md from the audited head (INV-5 now runs from main as the instruction root with the worktree as data), the CI job had no previous RESULT head (INV-3 now records previous_head in the ACCEPTANCE and revise.yaml, cross-checked by the host gate), ids were compared without sentences (INV-2), `allowed_files: ['*']` derived a cheap tier and a branch copy could claim a legacy id (INV-1, INV-12), and two task records pointed at an abandoned prerequisite. v6 adopts all ten and, because a cross-vendor reviewer found what a same-vendor fresh context did not, INV-7 now requires both a Claude and a Codex review of each design hash. Round 6 (`…-design-review-round6.md`, 22:28Z, verdict `revise`) accepted INV-1, 2, 3, 5, 12 and rejected INV-7: the Bot form produced no receipt, hash or RESULT, so it would have been an orchestrator-written receipt for a review it did not perform (R5). v7 makes the Codex review a `codex exec --sandbox read-only` run under a `codex-review` identity with its own receipt and RESULT, names it in the enforcement row and V4, keeps the Bot's review as swept feedback, and adds the bare-mode skills premise (round-6 INV-5 note, acted on in V2). Round 7 asks the Claude reviewer to confirm INV-7; the Codex review of v6 (hash 25b36e1c) that is already running is reported under `codex-review-dot-h001`, and a Codex confirmation of v7 follows it. Sources are the repository paths under `.orchestration/validation/dotfiles-T128-regime-v3-a01-research/` (`baseline.md`, `practice-evidence.md`, `claude-code-factsheet.md`, `codex-factsheet.md`, `github-factsheet.md`, `method-draft.md`). Receipt: `.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round7.md` (Claude) and `…-design-review-round7-codex.md` (Codex); the whole-file sha256 of this file in both headers.
FILE .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round2.md
2:reviewed_at: 2026-10-10T21:29:22Z
3:reviewer: claude-review-dot-a001
4:profile: review
6:design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@61b0a812c699e57c13713057571a5883044039a0414e2fdc3dca7913421e5f85
9:round: 2
23:INV-1: accepted. Note: each amendment changes the task file; say the gate compares the copy with the latest AGMSG-TASK's task_sha256 and that the worker recommits the copy after each amendment.
25:INV-2: rejected: "its task.md invariant ids equal the design's implementing_tasks entry for that task" is not computable: implementing_tasks (lines 9-21) is a flat list of task ids with no invariant per entry; the mapping exists only in section 6 prose, outside the hashed keys. Right: implementing_tasks becomes a map {task id: [INV ids]} inside the hashed keys. Second gap: the regime job needs the design file on the runner, and the design is untracked in the main checkout until a boundary commit (git status at review time: untracked). State the precondition: the design reaches main through a boundary PR before the implementing TASK is dispatched and the regime job fails closed when the design named by the task.md copy is absent from main; or copy the design to the branch beside task.md, anchored by the review RESULT's design_sha256= in history.
27:INV-3: rejected: it contradicts INV-1. INV-1 anchors the branch copy of task.md to task_sha256= in history (line 44); the INV-3 enforcement row has the worker append a revise: list to that same copy (line 144), so the first revise round breaks the hash the gate checks, and V1 and V3c would ship incompatible rules. Right: the worker's revise list is a sibling file (.orchestration/<task id>/revise.yaml) that the regime job reads; task.md stays byte-identical to the dispatched file.
29:INV-4: accepted. Note: the question count now lives in INV-6 without a threshold (below).
31:INV-5: accepted. Note: section 4's paragraph (line 136) still says stage 3 "starts without the orchestrator" while the table (line 131) starts it with make audit-head; say the orchestrator runs it on RESULT arrival and that the pool, once-per-head and tree-equality rules are what remove the queue.
33:INV-6: rejected: "PONG status=question" is listed among the history counts (line 49) with no threshold in INV-6 or section 7 (line 175); v1 had "a second question". Right: state 2, or say questions count only through the TASKs that answer them and remove the item. Note: the audit-heads count reads .orchestration/validation/<task>-audit-<sha7>.json from the main checkout; require the JSON's sha256 to match its AGMSG-AUDIT record before counting, as INV-5 does for the verdict, or the orchestrator can edit a finding away.
35:INV-7: accepted. Fixing INV-2 and INV-3 changes hashed keys, so INV-7 itself requires a round 3; it can be a diff confirmation.
37:INV-8: accepted. Note: the revise.yaml of INV-3 lands under the same directory.
39:INV-9: accepted. Premise 8 holds as re-run.
41:INV-10: accepted.
43:INV-11: accepted.
45:INV-12: accepted. Note: add "a revise list appended to the hashed task.md" to the gaming paths once INV-3 is fixed.
64:Design verdict: revise
FILE .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round3.md
2:reviewed_at: 2026-10-10T21:33:02Z
3:reviewer: claude-review-dot-a001
4:profile: review
6:design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@b2bfad90d1e1d3b8210b40321f6d23cfdab7c4e5b27e8d644b02a8fea9d535d2
9:round: 3
27:INV-1: accepted.
28:INV-2: accepted. Note: section 7 (line 179) still words the cap as "outside tests/ and .orchestration/" without the data-list exclusion that INV-2 and INV-12 state; section 7 is outside the hash, so align it in the next edit without a new review.
29:INV-3: accepted.
30:INV-4: accepted.
31:INV-5: accepted.
32:INV-6: accepted.
33:INV-7: accepted.
34:INV-8: accepted.
35:INV-9: accepted.
36:INV-10: accepted.
37:INV-11: accepted.
38:INV-12: accepted.
47:Design verdict: accept
FILE .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round4.md
2:reviewed_at: 2026-10-10T22:06:21Z
3:reviewer: claude-review-dot-a001
4:profile: review
6:design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@6eedc15f74d9a150a601190e3fb839175be3799c2eadf37331f850430c930210
9:round: 4
24:INV-1: accepted. INV-2: accepted. INV-3: accepted. INV-4: accepted. INV-5: accepted. INV-6: accepted. INV-7: accepted. INV-8: accepted. INV-9: accepted. INV-10: accepted. INV-11: accepted. INV-12: accepted.
28:Design verdict: accept
FILE .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round5.md
2:reviewed_at: 2026-10-10T22:12:18Z
3:reviewer: claude-review-dot-a001
4:profile: review
6:design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@b5eb917f85d44726a514efbf910d2e0f04c17f07110ef90310fd6b3b13719ceb
9:round: 5
17:INV-1: accepted. INV-2: accepted. INV-3: accepted. INV-4: accepted. INV-5: accepted. INV-6: accepted. INV-7: accepted. INV-8: accepted. INV-9: accepted. INV-10: accepted. INV-11: accepted. INV-12: accepted.
21:Design verdict: accept
FILE .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round6.md
2:reviewed_at: 2026-10-10T22:28:36Z
3:reviewer: claude-review-dot-a001
4:profile: review
6:design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@25b36e1c6e41aed8014af28911dbe9744bacc77a37ad6c1e445b35a03c5030be
9:round: 6
19:INV-1: accepted. The literal first segment plus the tier-by-literal-prefix rule closes allowed_files of ['*'] and friends, and binding the legacy exemption to .orchestration/tasks/ on main closes the branch-copy claim; both are mechanical in V1 and V1c. Note: the schema regex V1 chose admits a wildcard inside the first segment (scripts*); see the task-review receipt.
21:INV-2: accepted. Byte-for-byte sentence equality against the design read from main is what this seat has been checking by hand each round; now the regime job does it.
23:INV-3: accepted. previous_head carried in the ACCEPTANCE and revise.yaml, diffed by CI and cross-checked by the host gate against the previous RESULT's head in history, closes the gap round 1 named (CI cannot know the previous head). Note: INV-12 should list "a previous_head that is not the previous RESULT's head" as a gaming path; the generic clause covers its test, so this is wording, not a hole.
25:INV-5: accepted with one note that V2 must act on. The instruction root and the schema from main, the head as --add-dir data, closes the schema-or-AGENTS.md-on-the-audited-head path for codex. The claude fallback is not fully closed: the headless page states that bare mode "loads skills from its .claude/skills/ folder" of a directory named with --add-dir, so a head that adds or changes .claude/skills/** enters the fallback's context as skill descriptions. The runner should refuse the fallback (exit 2, blocked) when git diff --quiet origin/main <head> -- .claude/skills fails, leaving such a head to the codex path; add the page's sentence as a premise.
27:INV-7: rejected: the second review's alternative form contradicts the sentence. "or the Codex Bot's review of the boundary PR carrying the design" produces no receipt, no canonical hash and no AGMSG-RESULT from a Codex identity, yet the same sentence requires each receipt to be a schema document naming the hash and both RESULTs to precede the implementing TASK; the only way the Bot form satisfies that is an orchestrator-written receipt for a review it did not perform, which is R5. Right: the Codex review is codex exec --sandbox read-only on the review profile under a codex-review identity (headless, V4's runner, or a seated one until V4), its receipt and RESULT like the Claude one; the Bot's PR review stays what it is, swept feedback. Second gap: the enforcement row (line 153) and V4 (line 172) still describe one -review- identity and one receipt; name the Codex form in both and the gate rule "two RESULTs, one from a Claude -review- identity and one from a Codex -review- identity, both naming the current hash". The round-6 Codex receipt in flight (…-round6-codex.md) is the right shape for this.
29:INV-12: accepted; the four new gaming paths match INV-1, INV-2 and INV-5 as changed.
35:Design verdict: revise
FILE .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round7-codex.md.transcript.md
FILE .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round7.md
2:reviewed_at: 2026-10-10T22:31:53Z
3:reviewer: claude-review-dot-a001
4:profile: review
6:design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@40476474ad9aec1f36f14927a43a8f98d0187eb5d7092b422b635fbdff70142a
9:round: 7
20:INV-1: accepted. INV-2: accepted. INV-3: accepted. INV-4: accepted. INV-5: accepted. INV-6: accepted. INV-7: accepted. INV-8: accepted. INV-9: accepted. INV-10: accepted. INV-11: accepted. INV-12: accepted.
22:Design verdict: accept
FILE .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review.md
2:reviewed_at: 2026-10-10T21:15:46Z
3:reviewer: claude-review-dot-a001
4:profile: review
6:design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@b91e8bb407e1019196eade22604fac30801bfce173a95416e9176ca8917b352f
9:round: 1
18:INV-1: rejected: the CI job has no input. The task file is orchestrator-authored, lives untracked in the main checkout until the boundary commit, and INV-8 puts only worker evidence on the branch; at PR time the implementing task file is on neither the base nor the head, so "validates every task file the PR adds or changes" validates nothing for the PR it governs. Right: the AGMSG-TASK carries task_sha256=; the worker's first commit copies the task file to .orchestration/<task id>/task.md; the regime job validates that copy against main's schemas/task.json; the host gate compares its sha256 with the token in history. Also: the regime check only binds once the ruleset lists it as required; name that operator action in V1's acceptance record.
20:INV-2: rejected: the wave table breaks the rule it implements. "One task invariant per PR": V1 carries INV-1 and INV-2, V3 carries INV-3, INV-4, INV-6 and INV-10, V5 carries INV-8 and INV-9 (design lines 142-146). Either the unit is "one implementing task's declared invariant set" (then say so and the CI check compares the PR's task.md invariant ids with the design's implementing_tasks entry), or V3 and V5 split. Second gap: the seven required checks of test.yaml run on pull_request (test.yaml:11), so a PR still edits the workflow that runs INV-12's unit tests (R8 stays open there); the regime job should refuse a PR that changes .github/workflows/** unless its task.md is design tier and lists the file.
22:INV-3: rejected: "fails on the previous head" and "the fix turns green" are not gate-checkable; the gate cannot run tests on an earlier head. Mechanical core: the ACCEPTANCE status=revise carries check=<tests/...::name | ci:<job> | repro:<id>>; the RESULT's validation file carries the same id with pasted output; the regime job verifies the named test exists on the head and differs from the previous RESULT head (git diff <prev head> <head> -- <test file> non-empty). State that; the rest is the worker's evidence.
24:INV-4: rejected: internally inconsistent. "the orchestrator may amend once" allows one amendment; "a third amendment withdraws" allows two; INV-6 and section 7 say two. Fix the count once (INV-6 is the counter, INV-4 the trigger). Second: "counted from AGMSG-TASK amendment= messages" is the relabel path INV-12 names; count every AGMSG-TASK for the task_id after the first (history: T124 W1 10 TASK sends, 8 with amendment=; W3b 10 and 5; T119 10 and 8). Third: "withdraws the task to design" names no enforcement point; it is INV-6's Stop block and merge backstop, so say so.
26:INV-5: rejected: (a) the gate today takes the verdict by regex from the .last.md companion (require-crit-review.py:30-31, 638-665) and accepts not-applicable for every finding whatever its category (require-crit-review.py:698-710); replacing that with the schema JSON, the AGMSG-AUDIT sha256 lookup and the orchestration/conformance lock is a change to an existing evidence rule, and no wave names it (V2 is runner and schema, V3 the reset backstop, V4 the design-review anchor, V5 accept-task.py). P4's "gains only history-anchored checks; nothing removed except REVIEW_TREE" is false on its own terms, and REVIEW_TREE does not exist on main (it was PR 313's). (b) The AGMSG-AUDIT record names no sending identity; the runner runs on the orchestrator's host, so say honestly that the anchor prevents edits after the record, not fabrication before it, and name the identity. (c) "started automatically when ... the Codex Bot has reviewed the head" has no timeout; the SKILL's 15-minute bot: none rule must carry over or a head the Bot skips stalls stage 3 (Bot re-review per push is UNVERIFIED in codex-factsheet.md:55). (d) "never for an evidence-only revision" conflicts with audit_name_error, which requires the audit sha to prefix HEAD (require-crit-review.py:614-615): an evidence-only commit moves HEAD and the gate refuses the earlier audit. Right: the gate accepts an audit of an earlier head when git diff --quiet <audited> <HEAD> -- . ':!.orchestration' holds; assign it to a wave. (e) "rationale written before the verdict" is a prompt instruction, not a schema property: strict JSON schema does not order generation, and PR 314's schema lists verdict first.
28:INV-6: rejected: (a) the loop-time block is soft on both runtimes: Claude's Stop hook has an 8-consecutive-continuation cap that resets on any tool call (hooks page, Stop section), and Codex's decision: block "doesn't reject the turn" but injects a continuation prompt (learn.chatgpt.com/docs/hooks). The merge backstop in the gate is therefore the mandatory point and the Stop hook the early signal; the invariant says the reverse. (b) The Bot count "on two heads" is not computable from the sweep JSON: pr-feedback.py records commit_id on review items only (pr-feedback.py:199) and nothing on review_comment items; the collector change (T124 wave 2a's original_commit_id) is in no wave. (c) The audit count needs the audit JSONs, which are orchestrator files in the main checkout; name the source. (d) The Stop hook runs with timeout 5 and a 3 s history budget (.claude/settings.json; agent-stop-gate.sh:209-212): history counts fit, GitHub counts do not; split the counts by source. (e) "re-dispatch ... is a boundary violation" names no detector; T124 v3 INV-5 had one (a closed-unmerged PR whose task has no reset record; a task over a threshold with no accepted record) in check-regime-boundary.sh; restore it in V3.
30:INV-7: accepted. Notes: the canonical hash covers five front-matter keys; sections 4 to 9 (stages, enforcement map, waves, thresholds) are outside it, so the wave table can change after review without a new one; add that to INV-12's gaming paths or hash implementing_tasks together with the wave file list. Bootstrap: this receipt carries a whole-file sha256, so V1's AGMSG-TASK is anchored by that form; V4's gate check must accept both forms for this design or V1 needs a second review.
32:INV-8: accepted. Notes: add the task.md copy (INV-1 above); the gate's path rules (feedback_path_error, orchestration_path_error) already fit, because the orchestrator's records stay under .orchestration/validation and acceptance; the "final head" with worker evidence committed is what INV-5 (d) above must handle.
34:INV-9: rejected: "whose breach pauses the task for an operator decision" names no mechanism that pauses; the enforcement map puts cost in accept-task.py and the boundary warning, which run after the fact. Say "the acceptance record names the operator decision and the boundary check warns", or name the Stop-hook check with its budget source. Per-message usage in session transcripts is UNVERIFIED in claude-code-factsheet.md:75; the premises block does not cover it.
36:INV-10: rejected: the stop gate reads history rows as from, to, body with no timestamp (agent-stop-gate.sh:65), and a push is GitHub state the 5 s hook cannot fetch; neither the 30-minute first push nor the 20-minute idle is computable where INV-10 places them. Right: history.sh timestamps for the TASK time, gh pr view for the first push, both in check-regime-boundary.sh and accept-task.py; the Stop hook can at most read the TASK time once the awk carries the timestamp column.
38:INV-11: accepted. Note: permgate records input_hash and no session_id or cwd today (executable_permgate:161, 219), consistent with the design; the sandbox record the gate compares against is the one INV-8 commits on the branch.
40:INV-12: accepted. Notes: add the gaming paths this review names (a TASK without amendment=, an evidence-only relabel of a code change, a wave-table rewrite after review, a Bot-skipped head that never starts its audit).
102:Design verdict: revise

**Inspecting script and factsheets**
exec
/bin/zsh -lc 'rg -n "(audit|AGMSG|task_sha|reset|waiv|feedback|original_commit|orchestration|acceptance|receipt|review_source|head|BASE|PR_FEEDBACK|AUDIT)" scripts/require-crit-review.py | head -220; rg -n "(AGMSG|history|question|amend|revise|timeout|Stop|block|reset)" scripts/agent-stop-gate.sh; rg -n "(orchestration|accept|reset|closed|identity|delivery|crit|worktree|PR|history)" scripts/check-regime-boundary.sh; rg -n "(original_commit|commit_id|review_comment|annotation|status|head|pagination|thread|resolution)" scripts/pr-feedback.py; rg -n "''^(name:|on:|permissions:)|pull_request|workflow_dispatch|checkout|make |uv run|required|regime" .github/workflows/test.yaml' in ~/Workspace/dotfiles
 succeeded in 42ms:
23:PR_FEEDBACK_ENV = "PR_FEEDBACK_EVIDENCE"
24:AUDIT_ENV = "AUDIT_EVIDENCE"
25:AUDIT_DISPOSITIONS_ENV = "AUDIT_DISPOSITIONS"
26:PR_FEEDBACK_DISPOSITION = re.compile(r"(?:fixed:(?P<commit>[0-9a-f]{7,40})|not-applicable:(?P<reason>.*\S.*))", re.S)
28:# herdr-agents --audit names and concludes the task-level audit this way.
29:AUDIT_NAME = re.compile(r"(?P<task>.+)-audit-(?P<sha>[0-9a-f]{7,40})\.md")
30:AUDIT_VERDICT = re.compile(r"\s*Verdict: (correct|incorrect|blocked)\s*")
31:AUDIT_FINDING = re.compile(r"^\s*(?:[-*+]\s+)?\[P[0-3]\]", re.M)
32:AUDIT_FINDING_DISPOSITION_PREFIX = "audit-finding:"
33:AUDIT_FINDING_NUMBER = re.compile(rf"{AUDIT_FINDING_DISPOSITION_PREFIX}\s*(?P<number>\d+)\b")
111:CRIT_DATA_SOURCE_FIELD = "review_source"
136:    """Skip worklogs and the PR feedback evidence file itself when sizing a diff."""
139:    evidence = os.environ.get(PR_FEEDBACK_ENV, "").strip()
145:    return feedback_path_error(root, evidence_path) is None and feedback_relative_path(root, evidence_path) == Path(
150:def feedback_relative_path(root: Path, path: Path) -> Path:
159:def feedback_path_error(root: Path, path: Path) -> str | None:
162:            feedback_relative_path(root, path),
166:        return f"{PR_FEEDBACK_ENV} must point to a repo-local JSON file"
168:        relative.parts[:2] != (".orchestration", "validation") or not relative.name.endswith("-pr-feedback.json")
171:        return "evidence must live under .orchestration/validation/ and end with -pr-feedback.json"
274:        return [f"{EVIDENCE_ENV} must point to a review receipt file"]
360:def commit_in_range(root: Path, commit: str, base: str, head: str) -> bool:
361:    """Return whether commit is in base..head: reachable from head, not from base."""
363:        run_git(["merge-base", "--is-ancestor", commit, head], root).returncode == 0
368:def pr_feedback_errors(root: Path, required: bool, head: str | None = None, base: str | None = None) -> list[str]:
369:    """Check the filled pr-feedback.py JSON: every item needs a root-cause disposition."""
370:    evidence = os.environ.get(PR_FEEDBACK_ENV, "").strip()
373:            return [f"{PR_FEEDBACK_ENV} must point to the filled scripts/pr-feedback.py JSON for PR integration"]
378:    path_error = feedback_path_error(root, path)
382:        return [f"{PR_FEEDBACK_ENV} file does not exist: {path}"]
386:        return [f"{PR_FEEDBACK_ENV} must be valid JSON: {error}"]
389:        return [f"{PR_FEEDBACK_ENV} must be a pr-feedback.py document with an items list"]
392:    if head is not None and data.get("head_sha") != head:
394:            f"{PR_FEEDBACK_ENV} was collected for head {data.get('head_sha')!r}, not the current HEAD {head}; rerun scripts/pr-feedback.py"
396:    if head is not None and base is not None:
397:        errors.extend(collected_feedback_errors(root, data, head, base))
401:        label = f"{PR_FEEDBACK_ENV} item {index}"
407:        match = PR_FEEDBACK_DISPOSITION.fullmatch(disposition) if isinstance(disposition, str) else None
416:            and head is not None
418:            and not commit_in_range(root, commit, data["base_sha"], head)
443:def feedback_key(item: dict, masked: bool = False) -> tuple:
444:    """Identify a feedback item; `masked` takes its body and path as `--mask-secrets` saves them.
461:def missing_feedback(collected: list, saved: list) -> Counter:
463:    available = Counter(feedback_key(item) for item in saved if isinstance(item, dict))
466:        for key in dict.fromkeys((feedback_key(item), feedback_key(item, masked=True))):
471:            missing[feedback_key(item)] += 1
475:def pr_base_errors(root: Path, evidence: dict, pr: int, head: str, base: str) -> list[str]:
479:    failure = f"could not verify PR #{pr} base on GitHub; fetch the base and rerun scripts/pr-feedback.py"
495:                f"{PR_FEEDBACK_ENV} does not match the local GitHub repository {repo}; rerun scripts/pr-feedback.py"
498:            ["gh", "pr", "view", str(pr), "--repo", repo, "--json", "headRefOid,baseRefName,baseRefOid"],
520:    if metadata.get("headRefOid") != head:
521:        return [f"PR #{pr} head on GitHub is {metadata.get('headRefOid')}, not the local HEAD {head}; push first"]
524:            f"{PR_FEEDBACK_ENV} does not match the GitHub base {github_ref} ({github_base}); rerun scripts/pr-feedback.py"
533:            first_parents = run_git(["rev-list", "--first-parent", head], root)
538:            actual = run_git(["merge-base", base_sha, head], root)
539:            expected = run_git(["merge-base", github_base, head], root)
547:def collected_feedback_errors(root: Path, evidence: dict, head: str, base: str) -> list[str]:
548:    """Re-collect the PR's feedback and require every current item in the evidence.
551:    base SHA's scripts/pr-feedback.py (the PR under review cannot swap it) for the
552:    evidence's PR, requires the PR head on GitHub to be this HEAD, and requires
559:        return [f"{PR_FEEDBACK_ENV} must name its pull request number in `pr`"]
560:    errors = pr_base_errors(root, evidence, pr, head, base)
567:        collector = root / "scripts/pr-feedback.py"
568:        base_collector = run_git(["show", f"{evidence['base_sha']}:scripts/pr-feedback.py"], root)
570:            collector = Path(temporary) / "pr-feedback.py"
582:            return [f"could not re-collect PR #{pr} feedback with scripts/pr-feedback.py: {detail[0]}"]
584:    if collected.get("head_sha") != head:
585:        return [f"PR #{pr} head on GitHub is {collected.get('head_sha')}, not the local HEAD {head}; push first"]
587:        return [f"collected feedback does not match the local GitHub repository {evidence['repo']}"]
588:    missing = missing_feedback(collected.get("items", []), evidence.get("items", []))
592:            f"{PR_FEEDBACK_ENV} lacks {sum(missing.values())} current feedback item(s) for PR #{pr}, e.g. {sample[0]}:{sample[2]} {sample[1]}; rerun scripts/pr-feedback.py and disposition them"
597:def orchestration_path_error(root: Path, path: Path, env: str, directory: str) -> str | None:
598:    """Apply feedback_path_error's rule (repo-local, also after resolving links) to another .orchestration dir."""
600:        relatives = (feedback_relative_path(root, path), path.resolve().relative_to(root.resolve()))
602:        return f"{env} must point to a repo-local file under .orchestration/{directory}/"
603:    if any(relative.parts[:2] != (".orchestration", directory) for relative in relatives):
604:        return f"{env} must live under .orchestration/{directory}/"
608:def audit_name_error(name: str, head: str, task: str) -> str | None:
609:    match = AUDIT_NAME.fullmatch(name)
611:        return f"{AUDIT_ENV} must be named <id>-audit-<sha7>.md, not {name}"
613:        return f"{AUDIT_ENV} audits task {match.group('task')!r}, not {task!r} named by {PR_FEEDBACK_ENV} (<task>-pr-feedback.json)"
614:    if not head.startswith(match.group("sha")):
615:        return f"{AUDIT_ENV} audits {match.group('sha')}, not HEAD {head}; audit the final head"
619:def audit_errors(root: Path, head: str, task: str) -> list[str]:
620:    """Require the task-level audit of HEAD for task: `correct`, or `incorrect` with every finding not-applicable."""
621:    evidence = os.environ.get(AUDIT_ENV, "").strip()
624:            f"{AUDIT_ENV} must point to the task-level audit of HEAD, .orchestration/validation/<id>-audit-<sha7>.md (herdr-agents --audit)"
629:    path_error = orchestration_path_error(root, path, AUDIT_ENV, "validation")
633:        name_error = audit_name_error(name, head, task)
637:        return [f"{AUDIT_ENV} file does not exist: {path}"]
639:    # transcript, where repository text the auditor quoted could end in a verdict line.
643:            f"{AUDIT_ENV} verdict is missing: {source.name} must exist with codex's final message; re-run the audit"
645:    source_error = orchestration_path_error(root, source, AUDIT_ENV, "validation")
650:        return [f"{AUDIT_ENV} companion {source.name} resolves to {resolved}; it must be this audit's own last message"]
651:    name_error = audit_name_error(resolved.removesuffix(".last.md"), head, task)
656:    match = AUDIT_VERDICT.fullmatch(lines[-1]) if lines else None
661:        return [f"{AUDIT_ENV} verdict is {verdict} in {source}; a blocked or missing audit cannot be accepted"]
662:    findings = len(AUDIT_FINDING.findall(text))
664:        return [f"{AUDIT_ENV} verdict is incorrect but {source} lists no [P0-P3] finding to disposition"]
665:    return audit_disposition_errors(root, findings)
668:def audit_disposition_errors(root: Path, findings: int) -> list[str]:
669:    value = os.environ.get(AUDIT_DISPOSITIONS_ENV, "").strip()
672:            f"{AUDIT_ENV} verdict is incorrect: {AUDIT_DISPOSITIONS_ENV} must name the acceptance record that dispositions its {findings} finding(s)"
677:    path_error = orchestration_path_error(root, path, AUDIT_DISPOSITIONS_ENV, "acceptance")
681:        return [f"{AUDIT_DISPOSITIONS_ENV} file does not exist: {path}"]
686:        if not line.startswith(AUDIT_FINDING_DISPOSITION_PREFIX):
688:        number = AUDIT_FINDING_NUMBER.match(line)
691:                f"{AUDIT_DISPOSITIONS_ENV} line must name its finding as `{AUDIT_FINDING_DISPOSITION_PREFIX} <1-{findings}>` in audit order: {line}"
696:            errors.append(f"{AUDIT_DISPOSITIONS_ENV} dispositions finding {finding} more than once: {line}")
698:        match = PR_FEEDBACK_DISPOSITION.search(line)
700:            errors.append(f"{AUDIT_DISPOSITIONS_ENV} line needs `not-applicable:<reason>`: {line}")
703:                f"{AUDIT_DISPOSITIONS_ENV} line cites fixed:{match.group('commit')}; a fix moves HEAD, so audit the new head instead: {line}"
707:                f"{AUDIT_DISPOSITIONS_ENV} not-applicable needs a reason of at least {FAILURE_REASON_MIN_CHARS} characters: {line}"
714:            f"{AUDIT_DISPOSITIONS_ENV} leaves audit finding(s) {', '.join(map(str, missing))} of {findings} without a disposition; add one `{AUDIT_FINDING_DISPOSITION_PREFIX} <n> … not-applicable:<reason>` line per finding, numbered in audit order"
738:        return f"--base {base!r} is not a git ref; pass a branch or commit such as BASE=origin/main"
741:        return f"--base {base!r} does not resolve to a commit; fetch it or fix BASE"
749:        help="also review committed changes in <base>...HEAD and require PR_FEEDBACK_EVIDENCE, plus AUDIT_EVIDENCE when review is required (PR integration)",
762:    head = run_git(["rev-parse", "HEAD"], root).stdout.strip() if args.base else None
763:    feedback_errors = pr_feedback_errors(root, required=args.base is not None, head=head, base=args.base)
764:    if feedback_errors:
765:        print("PR feedback evidence is incomplete; run scripts/pr-feedback.py and disposition every item.")
766:        for error in feedback_errors:
769:    if os.environ.get(PR_FEEDBACK_ENV, "").strip():
771:            print(f"PR feedback evidence accepted: {os.environ[PR_FEEDBACK_ENV].strip()}")
774:                f"PR feedback evidence format checked only: {os.environ[PR_FEEDBACK_ENV].strip()}"
775:                " (set BASE=<ref> to bind it to HEAD, re-collect it, and check fixed: commits)"
784:    if head is not None and not all(path.startswith(".orchestration/") for path in paths):
785:        # The base path already validated PR_FEEDBACK_EVIDENCE's location and -pr-feedback.json suffix.
786:        task = Path(os.environ[PR_FEEDBACK_ENV].strip()).name.removesuffix("-pr-feedback.json")
787:        errors = audit_errors(root, head, task)
789:            print("Task-level audit evidence is required for PR integration of this change:")
793:        print(f"Audit evidence accepted: {os.environ[AUDIT_ENV].strip()}")
813:    print("Record a receipt with `review_surface:`, `reviewer:`, and `review_outcome:`.")
822:        "Then use `review_surface: crit-data`, `reviewer: codex` or `reviewer: claude-code`, and `review_source: <json path>`."
825:        "After addressing review feedback, rerun with AGENT_REVIEWED=1 or CRIT_REVIEWED=1 plus REVIEW_EVIDENCE=<path>."
3:# @brief Claude Code Stop hook that keeps an agmsg seat from idling with work pending.
5:#   Reads the Stop hook JSON on stdin and classifies the session's checkout:
9:#   Orchestrator seat: blocks on `git status` entries outside `.orchestration/`
11:#   `AGMSG-RESULT` addressed to the seat's unsuffixed claude-code identity that
12:#   has no later `AGMSG-ACCEPTANCE` or `AGMSG-TASK` re-dispatch from it.
14:#   Worker seat: blocks on every task_id whose latest `AGMSG-TASK` (or
15:#   `AGMSG-ACCEPTANCE status=revise`) addressed to a claude-code identity
16:#   registered at the worktree has no later `AGMSG-RESULT` or `AGMSG-PONG
17:#   status=blocked` for that task_id from it, nor a later `AGMSG-ACCEPTANCE`
21:#   whole team history through agmsg's own storage facade, the one
22:#   `history.sh` reads (the agmsg skill forbids reading its database
24:#   needs no network; only the watchdog fallback (no timeout or gtimeout) uses
26:#   agmsg install it passes; a failing identity lookup or an unreadable store blocks
37:# @option --read-history <team> Internal: print one team's history rows (the gate runs itself this way under timeout).
38:# @option --mountinfo <file> Test only: read mount points from <file>. The Stop hook passes no arguments, so its inherited environment cannot redirect the table.
47:# Team-wide history as `from<TAB>to<TAB>body` rows, chronological. This is the
48:# storage facade history.sh itself calls, without its per-recipient unread pass
50:# AGMSG_BUSY_TIMEOUT (agmsg's documented knob, default 5000 ms per sqlite call)
51:# shortens each wait on a contended store. storage_history runs storage_init, which writes unless
56:# SQLITE_BUSY; only a non-initializing storage_history upstream would close that.
57:read_history() {
58:    export AGMSG_BUSY_TIMEOUT=1000
62:    if [[ ${_AGMSG_STORAGE_LOADED:-} == sqlite ]]; then
63:        [[ "$(agmsg_sqlite "$(_sqlite_db "$1")" 'PRAGMA user_version;' 2> /dev/null)" == "${_AGMSG_STORAGE_SCHEMA_REV:-}" ]] || return 1
65:    storage_history "$1" | jq -r '[.from, .to, .body] | @tsv'
68:# `--read-history <team>` is the read alone, so the gate can run it under
69:# timeout as a child of itself.
70:if [[ ${1:-} == --read-history ]]; then
71:    read_history "$2"
79:# GNU timeout, or Homebrew coreutils' gtimeout on macOS; empty when neither.
80:runner="$(command -v timeout || command -v gtimeout || true)"
186:        # Stop hook), so control characters are shell-quoted, never raw.
196:# A lookup that runs but fails must not read as "no seat here"; it blocks once,
198:if ! identities="$(AGMSG_RESOLVE_PROJECT=0 "${scripts}/identities.sh" "${top}" claude-code 2> /dev/null)"; then
203:block() {
209:# All history reads share one 3 s budget inside the 5 s hook timeout: a
211:# running out of budget blocks at once.
214:# Read one team's history into ${history} within ${remaining} seconds; exit
215:# status 124 on expiry, as timeout(1) reports it. Without timeout or gtimeout
220:        history="$("${runner}" "${remaining}" bash "${BASH_SOURCE[0]}" --read-history "$1" 2> /dev/null)"
225:    bash "${BASH_SOURCE[0]}" --read-history "$1" > "${out}" 2> /dev/null &
240:        history="$(< "${out}")"
251:    # ponytail: an unreadable store blocks every turn once; add a timestamp
253:    # `timeout 0` would mean no limit, so a spent budget blocks before the read.
262:        reasons+=("agmsg history read exceeded the hook budget; retry")
263:        block
265:        [[ ${active} == true ]] || reasons+=("agmsg history unreadable for team ${team}; check ${scripts}/history.sh ${team}")
271:            reasons+=("AGMSG-RESULT task_id=${task} in team ${team} has no AGMSG-ACCEPTANCE from ${name}; review it and send AGMSG-ACCEPTANCE v1 task_id=${task}")
273:            reasons+=("AGMSG-TASK task_id=${task} in team ${team} to ${name} has no AGMSG-RESULT yet; finish it and send AGMSG-RESULT v1 task_id=${task} (or AGMSG-PONG v1 status=blocked) with agmsg-dispatch")
284:            # TASK / revise ACCEPTANCE sender (worker). Only a message between
287:                if ($2 == me && kind == "AGMSG-RESULT") pending[id] = $1
288:                else if ((id in pending) && $1 == me && $2 == pending[id] && (kind == "AGMSG-ACCEPTANCE" || kind == "AGMSG-TASK")) delete pending[id]
289:            } else if ($2 == me && (kind == "AGMSG-TASK" || (kind == "AGMSG-ACCEPTANCE" && status == "revise"))) {
293:            } else if ($1 == me && $2 == pending[id] && (kind == "AGMSG-RESULT" || (kind == "AGMSG-PONG" && status == "blocked"))) {
295:            } else if ($1 == pending[id] && $2 == me && kind == "AGMSG-ACCEPTANCE") {
299:        END { for (id in pending) print id }' <<< "${history}")
302:[[ ${#reasons[@]} -eq 0 ]] || block
5:#   Verifies the Stop list of the agmsg-orchestration skill for this
7:#   untracked `.orchestration` files in every registered checkout
8:#   (`git worktree list`); exactly one agmsg identity name across claude-code
10:#   reported too); any identity at a linked worktree under `.claude/worktrees/`
11:#   (a worker still seated: `herdr-agents --remove-worker <worktree>`), and
14:#   no identity, such as a CI checkout, is never flagged); running
15:#   `crit _serve` review servers; a canonical clone (`chezmoi source-path`,
38:# when this script runs from a linked worktree.
49:done < <(git -C "${root}" worktree list --porcelain 2> /dev/null | sed -n 's/^worktree //p')
54:        [[ -n ${path} ]] && violations+=("untracked .orchestration file in ${checkout}: ${path}")
55:    done < <(git -C "${checkout}" ls-files --others --exclude-standard -- .orchestration 2> /dev/null)
58:# @description Print the number of distinct agmsg identity names at a path.
62:    AGMSG_RESOLVE_PROJECT=0 "${scripts}/identities.sh" "$1" "$2" 2> /dev/null | cut -f 2 | sort -u | grep -c . || true
67:    # exactly one identity across both runtime types. Workers are seated on
68:    # demand in linked worktrees, so an identity left at one at a boundary is
72:        AGMSG_RESOLVE_PROJECT=0 "${scripts}/identities.sh" "${main}" claude-code 2> /dev/null || true
73:        AGMSG_RESOLVE_PROJECT=0 "${scripts}/identities.sh" "${main}" codex 2> /dev/null || true
76:        violations+=("no agmsg identity at the active seat ${main} (expected one)")
81:    # with no identity may sit at a detached HEAD.
100:        if ((seated > 0)) && [[ ${resolved} == "${resolved_main}/.claude/worktrees/"* ]]; then
101:            worktree=".claude/worktrees/${resolved#"${resolved_main}/.claude/worktrees/"}"
102:            violations+=("worker still seated at ${worktree} (herdr-agents --remove-worker ${worktree})")
107:if command -v pgrep > /dev/null 2>&1 && pgrep -f 'crit _serve' > /dev/null 2>&1; then
108:    violations+=("crit review server still running (pgrep -f 'crit _serve')")
165:    # worktree is a worker tab still open.
173:            jq -r --arg worktrees "${main}/.claude/worktrees/" \
174:                '[.result.panes[]? | select((.cwd // "") | startswith($worktrees)) | (.label // .pane_id)] | unique[]' 2> /dev/null)
192:# The seat lock belongs to the main checkout, also when run from a worktree.
2:"""Collect every piece of GitHub feedback on a pull request head into one JSON document.
7:thread's resolution state), non-passing check runs, every check-run
8:annotation at any level, and every commit status on the PR head. Each item
15:from __future__ import annotations
97:        ["gh", "auth", "status"],
147:def thread_states(repo: str, number: int, graphql: GraphQL) -> dict[int, dict[str, bool]]:
148:    """Map each review comment id to its thread's resolved and outdated state."""
157:        threads = data["data"]["repository"]["pullRequest"]["reviewThreads"]
158:        for thread in threads["nodes"]:
159:            state = {"resolved": thread["isResolved"], "outdated": thread["isOutdated"]}
160:            comments = thread["comments"]
168:                    {"id": thread["id"], "cursor": comments["pageInfo"]["endCursor"]},
171:        if not threads["pageInfo"]["hasNextPage"]:
173:        cursor = threads["pageInfo"]["endCursor"]
178:    sha = pull["head"]["sha"]
199:                commit=review.get("commit_id"),
202:    states = thread_states(repo, number, graphql)
207:                "review_comment",
220:        conclusion = run.get("conclusion") or run.get("status")
235:        if output.get("annotations_count"):
236:            for annotation in flatten(fetch(f"repos/{repo}/check-runs/{run['id']}/annotations", True)):
237:                message = " ".join(part for part in (annotation.get("title"), annotation["message"]) if part)
240:                        "annotation",
242:                        annotation["annotation_level"],
245:                        annotation.get("path"),
246:                        annotation.get("start_line"),
251:    # The statuses list keeps creators and is newest first; keep each context's latest.
253:    for status in flatten(fetch(f"repos/{repo}/commits/{sha}/statuses", True)):
254:        latest.setdefault(status["context"], status)
255:    for status in latest.values():
258:                "status",
259:                status.get("creator"),
260:                status["state"],
261:                f"{status['context']}: {status.get('description') or ''}".strip(),
262:                status.get("target_url"),
263:                check=status["context"],
270:        "head_sha": sha,
297:        f"pr-feedback: {repo}#{args.pr} head {document['head_sha'][:7]}: {len(document['items'])} items ({summary})",
1:name: Unit test
3:on:
6:  # skipped required checks in a pending state and block merges.
11:  pull_request:
13:permissions:
28:        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7
43:          # Keep the diff calculation here so the required workflow can always
46:          if [ "${EVENT_NAME}" = "pull_request" ]; then
59:          # var-like form to make the rule reusable. For this workflow, keeping
62:          # should run. It does not decide whether the required workflow itself
91:        # Non-required canary for the next Ubuntu image: it shows how the suite
116:        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7
143:            # Ruby is required for bashcov/simplecov formatters.
175:            echo "chezmoi v${chezmoi_version}: the GitHub release attestation did not verify (gh 2.93.0 or newer, authenticated, is required)" >&2
340:          make unit-test

**Analyzing design enforcement gaps**
**Examining trust assumptions and validation**
**Evaluating orchestrator and permission controls**
**Reviewing unit test controls and PR implications**
codex
中間判定では、特に「存在確認・非空確認」を真偽検証と取り違えている箇所が残っています。具体的には revise の `repro`、premise の貼付出力、コスト、operator waiver が、書き手自身による捏造や上書きを機械的に排除できるかを重点確認しています。
exec
/bin/zsh -lc "nl -ba .orchestration/validation/dotfiles-T128-regime-v3-a01-research/claude-code-factsheet.md; nl -ba .orchestration/validation/dotfiles-T128-regime-v3-a01-research/codex-factsheet.md; nl -ba .orchestration/validation/dotfiles-T128-regime-v3-a01-research/github-factsheet.md; sed -n '180,230p' scripts/pr-feedback.py; sed -n '1,120p' .github/workflows/test.yaml; sed -n '120,240p' .github/workflows/test.yaml; sed -n '240,432p' .github/workflows/test.yaml" in ~/Workspace/dotfiles
 succeeded in 121ms:
     1	# Claude Code capability fact sheet (docs as of 2026-10-11; installed 2.1.293)
     2	
     3	Sources: code.claude.com/docs/en/* and anthropic.com/engineering. Fetched directly. "UNVERIFIED" marks claims the pages did not confirm.
     4	
     5	Abbreviations: CLI = https://code.claude.com/docs/en/cli-reference, HEADLESS = https://code.claude.com/docs/en/headless, HOOKS = https://code.claude.com/docs/en/hooks, PERM = https://code.claude.com/docs/en/permissions, PMODES = https://code.claude.com/docs/en/permission-modes, SETTINGS = https://code.claude.com/docs/en/settings, SANDBOX = https://code.claude.com/docs/en/sandboxing, SUB = https://code.claude.com/docs/en/sub-agents, TEAMS = https://code.claude.com/docs/en/agent-teams, BP = https://code.claude.com/docs/en/best-practices, CACHE = https://code.claude.com/docs/en/prompt-caching, COSTS = https://code.claude.com/docs/en/costs.
     6	
     7	## 1. Headless / non-interactive
     8	
     9	- `--output-format`: `text` (default), `json` ("structured JSON with result, session ID, and metadata"), `stream-json` (NDJSON; last line is a `result` message "with the final response text, cost, and session metadata") — HEADLESS
    10	- `--json-schema` (print mode only): "The response includes metadata about the request (session ID, usage, etc.) with the structured output in the `structured_output` field"; invalid schema exits with `Error: --json-schema is not a valid JSON Schema`; `format` keyword is annotation-only — HEADLESS, CLI
    11	- JSON result fields: `total_cost_usd` plus "a per-model cost breakdown" (`modelUsage`), `usage` (incl. `cache_creation.ephemeral_1h_input_tokens`/`ephemeral_5m_input_tokens`), `session_id`, `permission_denials`, `subtype` (`success`, `error_max_turns`, `error_max_budget_usd`, `error_during_execution`), `duration_api_ms`; `usage` "Excluded" subagents, `total_cost_usd`/`modelUsage` "Included" — HEADLESS, CACHE, https://code.claude.com/docs/en/agent-sdk/cost-tracking. `num_turns`: UNVERIFIED on these pages.
    12	- Costs are "client-side estimates, not authoritative billing data" — cost-tracking
    13	- `--max-budget-usd` (print only): "Spend from subagents counts toward the cap. Spend can pass the cap, so leave headroom"; at the cap "spawning another subagent fails with `Budget limit reached`" and background subagents are stopped (v2.1.217+); restored totals from `--continue/--resume` don't count — CLI
    14	- `--max-turns` (print only): "Exits with an error when the limit is reached. No limit by default" — CLI
    15	- `--permission-mode`: `default`, `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions`, `manual` alias; "Overrides `defaultMode` from settings files" — CLI
    16	- A `-p` run starts in `default` "in sessions that fetch feature flags"; `auto` only in non-flag sessions on v2.1.285+ — PMODES
    17	- `dontAsk`: "denies every call that would otherwise prompt"; `AskUserQuestion`, `requiresUserInteraction` MCP tools, network-path reads "are denied even when an allow rule matches" — HEADLESS
    18	- `--permission-prompts none` (v2.1.259+): "Anything that would prompt is denied unless a `PermissionRequest` hook allows it, Claude is told that nobody can approve the request and not to retry it"; removes `AskUserQuestion`; denials appear in `permission_denials` — HEADLESS
    19	- `--allowedTools`: in a run that starts in auto mode "Claude Code drops a bare `Bash` entry as a broad allow rule and auto mode evaluates each command instead" — HEADLESS. `--disallowedTools`: bare name removes the tool from context; scoped rule denies matching calls — CLI
    20	- `--bare`: skips "hooks, skills, custom commands, subagents, installed plugins, MCP servers, auto memory, and CLAUDE.md"; "never reads OAuth credentials or the system keychain. For the Anthropic API, set `ANTHROPIC_API_KEY`... or supply an `apiKeyHelper` in the `--settings` JSON"; no system reminders, no background tasks (v2.1.286+); "will become the default for `-p`" — HEADLESS. Bare sessions bind no inbox socket, so they can't receive cross-session messages — https://code.claude.com/docs/en/cross-session-messaging
    21	- Without `--bare`, `-p` "runs the hooks in a project's `.claude/settings.json` and connects the servers in its `.mcp.json`, even in a folder you've never trusted" — HEADLESS
    22	- `--settings`: file or inline JSON, "above your user, project, and local files and below managed settings" — SETTINGS. `--setting-sources user,project,local` restricts sources — CLI
    23	- `--resume <id|name|transcript-path>`, `--continue` (skips `-p`-created sessions unless `claude -p --continue`), `--fork-session`, `--session-id <uuid>`, `--no-session-persistence` — CLI
    24	- `--agents` JSON (file path with `--print`, v2.1.281+); `--model`; `--effort low|medium|high|xhigh|max|ultracode`; `--append-system-prompt[-file]`; `--forward-subagent-text`; `--include-hook-events` — CLI
    25	- `-p` waits for background subagents/workflows after the final turn, idle cap 10 min (`CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS`) — HEADLESS
    26	
    27	## 2. Hooks
    28	
    29	- Events: SessionStart, Setup, UserPromptSubmit, UserPromptExpansion, PreToolUse, PermissionRequest, PermissionDenied, PostToolUse, PostToolUseFailure, PostToolBatch, Notification, MessageDisplay, SubagentStart, SubagentStop, TaskCreated, TaskCompleted, Stop, StopFailure, TeammateIdle, InstructionsLoaded, ConfigChange, CwdChanged, DirectoryAdded, FileChanged, WorktreeCreate, WorktreeRemove, PreCompact, PostCompact, PreModelSwitch, PostModelSwitch, Elicitation, ElicitationResult, SessionEnd — HOOKS
    30	- Common input: `session_id`, `prompt_id`, `transcript_path` ("written asynchronously and may lag"), `cwd`, `scratchpad_dir`, `permission_mode`, `effort.level`, `hook_event_name`; agent fields `agent_id`, `agent_type` — HOOKS
    31	- Per-event: SessionStart `source` = `startup|resume|clear|compact|fork`; SessionEnd `reason` incl. `clear`, `resume`, `logout`, `prompt_input_exit`, `other`; PostToolUse `tool_name`, `tool_input`, `tool_response`, `tool_use_id`; Stop/SubagentStop `stop_hook_active`, `last_assistant_message`, SubagentStop adds `agent_transcript_path`; TaskCompleted `task_id`, `task_subject`, `task_description`, `teammate_name`; TeammateIdle `teammate_name` — HOOKS. PreCompact/PostCompact input fields: UNVERIFIED (not extracted).
    32	- Blocking: "Exit with code 2 to block the action"; other non-zero = "non-blocking error. The action goes ahead". Can block: PreToolUse, UserPromptSubmit, Stop, SubagentStop, TeammateIdle, TaskCreated, TaskCompleted, ConfigChange, PreCompact, PreModelSwitch, Elicitation*, Worktree*, PostToolBatch. Cannot: PermissionRequest ("Exit code 2 isn't honored"), PostToolUse, PermissionDenied, Notification, SubagentStart, SessionStart/End, PostCompact, StopFailure — HOOKS
    33	- JSON: `continue:false` + `stopReason` stops Claude entirely; `decision:"block"` + `reason` (only value is `block`); PreToolUse `hookSpecificOutput.permissionDecision` `allow|deny|ask|defer`, `updatedInput`; PermissionRequest `hookSpecificOutput.decision.behavior` `allow|deny` with `updatedInput`, `message`, `interrupt`; `additionalContext`; `systemMessage` — HOOKS
    34	- Stop: `stop_hook_active` "is `true` when Claude Code is already continuing as a result of a stop hook"; "8-consecutive-continuation cap... resets each time Claude calls a tool. To raise the cap, set `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP`" (0 disables) — HOOKS, env-vars
    35	- SubagentStop block "keeps the subagent running and delivers `reason` to the subagent as its next instruction" — HOOKS
    36	- TaskCompleted: exit 2 → "the task is not marked as completed and the stderr message is fed back"; "When the `TaskUpdate` tool triggered the event, Claude Code ignores `continue: false`; exit code 2 still blocks" — HOOKS
    37	- Timeouts: default 600 s for `command`/`http`/`mcp_tool`, 30 s `prompt`, 60 s `agent`; 30 s on UserPromptSubmit/PreModelSwitch; SessionEnd 1.5 s; `async:true` hooks "can't block" — HOOKS
    38	- Execution: "All matching hooks run in parallel. If you define the same handler in more than one settings file, it runs once" — HOOKS
    39	- Settings precedence (highest first): "managed settings, command line, project local, shared project, user" — SETTINGS. (The caller's assumed order "managed > user > project > local" does not match the page.)
    40	- `disableAllHooks`: "set in user, project, or local settings can't disable those managed hooks"; `allowManagedHooksOnly` blocks user/project/local/plugin hooks; for untrusted repos use `--settings '{"disableAllHooks": true}'` because "the repository's project settings take precedence over yours" — HOOKS, PERM
    41	- Env: `$CLAUDE_PROJECT_DIR`, `CLAUDE_ENV_FILE` (SessionStart), `$CLAUDE_EFFORT`, `CLAUDE_CODE_REMOTE`, `CLAUDE_CODE_MESSAGING_SOCKET`; "There is no `$CLAUDE_MODEL`" — HOOKS. `CLAUDE_SESSION_ID`: UNVERIFIED (absent from hooks and env-vars pages; use stdin `session_id`).
    42	
    43	## 3. Permissions and sandbox
    44	
    45	- "Rules are evaluated in order: deny, then ask, then allow... An allow rule can't carve an exception out of a deny rule"; "If a tool is denied at any level, no other level can allow it... a managed settings deny can't be overridden by `--allowedTools`" — PERM
    46	- `allowManagedPermissionRulesOnly` makes managed the only rule source; `disableAutoMode`/`disableBypassPermissionsMode: "disable"` work from any scope — PERM
    47	- `defaultMode` `auto` and `bypassPermissions` "don't take effect from project or local settings; set them in user or managed settings instead" (bypass from any file before v2.1.257) — SETTINGS, PMODES
    48	- Protected paths (`.git`, `.claude` except `.claude/worktrees/`, etc.): `default/acceptEdits` prompted, `auto` routed to classifier, `dontAsk` denied, `bypassPermissions` allowed; `permissions.allow` "do not pre-approve protected-path writes" — PMODES
    49	- Auto mode: "a second model, the classifier"; runs "on Claude Sonnet 5 by default"; blocks e.g. "Sending keystrokes to Claude Code's own tmux pane... which the classifier treats as Claude changing its own permissions or oversight", "Writing to Claude Code session transcripts", "Launching an autonomous agent loop that runs without human approval or a sandbox, such as one started with `--dangerously-skip-permissions`"; rule labels appear as `[Data Exfiltration]`, `Git Destructive`; a rule literally labeled "Self-Modification": UNVERIFIED — PMODES, https://code.claude.com/docs/en/auto-mode-config
    50	- Fallback: "if the classifier blocks an action 3 times in a row or 20 times total, auto mode pauses and Claude Code resumes prompting" (not configurable); in `-p` "Claude Code doesn't stop the run" — PMODES, BP. The Mar 2026 engineering post says headless "we instead terminate the process" — docs for 2.1.293 supersede.
    51	- `autoMode` is read only from user, managed, `--settings`; "doesn't read `autoMode` from project settings"; `permissions.ask` rules "always force a permission prompt, even in auto mode"; `autoMode.classifyAllShell` — auto-mode-config
    52	- Classifier reviews subagent work at spawn, during, and "When the subagent finishes... before the parent reads the report"; flagged reports are "prepended with a security warning" — PMODES
    53	- Sandbox: OS-enforced for Bash/PowerShell/Monitor only; file tools, MCP, hooks run outside; `network.allowedDomains` "start empty"; `excludedCommands` run "outside the sandbox, which means no filesystem restrictions and no network proxy"; `allowUnsandboxedCommands:false` makes Claude Code "ignore the `dangerouslyDisableSandbox` parameter"; a `false` in user/`--settings`/managed "holds even when a project's settings set `true`" (v2.1.285+); under an admin-required sandbox repo files' `excludedCommands`, `allowedDomains`, `allowUnixSockets` are ignored; `strictAllowlist` and `allowManagedDomainsOnly` deny instead of prompt — SANDBOX
    54	
    55	## 4. Subagents
    56	
    57	- Frontmatter: `name`, `description` (required); `tools`, `disallowedTools`, `model` (`sonnet|opus|haiku|fable|<id>|inherit`), `effort` (`low..max`), `permissionMode` (`default|acceptEdits|auto|dontAsk|bypassPermissions|plan`), `maxTurns`, `skills`, `mcpServers`, `hooks`, `memory` (`user|project|local`), `background: true`, `isolation: worktree`, `color`, `initialPrompt`, `omitClaudeMd`, `experimental.cacheTtl` — SUB
    58	- `isolation: worktree`: "temporary git worktree... branched by default from your default branch... automatically cleaned up if the subagent makes no changes"; worktree path `<repo>/.claude/worktrees/<name>` is documented for `--worktree` (CLI) and WorktreeCreate covers subagent isolation (HOOKS); exact subagent path: UNVERIFIED
    59	- Concurrency: "when 20 subagents are running in a session, spawning another... fails with `Concurrent subagent limit reached`" (`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`); nesting up to three layers (`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`) — SUB
    60	- Foreground blocks and passes prompts through; background prompts surface in main session; background subagents "run with a smaller built-in tool set"; fork mode is default in interactive sessions (background, no `run_in_background`) and off in `-p`/SDK — SUB
    61	- "Each subagent starts with a fresh, isolated context window"; Explore/Plan skip CLAUDE.md and are one-shot; others get an agent ID resumable via `SendMessage`; transcripts at `~/.claude/projects/{project}/{sessionId}/subagents/agent-{agentId}.jsonl` — SUB
    62	- Reviewer pattern: `code-reviewer` with `tools: Read, Grep, Glob, Bash`, `model: inherit`; "Limit tool access" — SUB. Over-reporting: "A reviewer prompted to find gaps will usually report some, even when the work is sound... Tell the reviewer to flag only gaps that affect correctness or the stated requirements" — BP
    63	
    64	## 5. Agent view, teams, messaging, workflows
    65	
    66	- Agent view (research preview): `claude --bg "<prompt>"` (positional, rejects `-p`), `claude agents [--json [--all]] [--cwd]`, `claude attach|logs|stop|respawn|rm <id>`; supervisor keeps sessions running; "Before editing files, Claude moves the session into an isolated git worktree under `.claude/worktrees/`" (opt out `worktree.bgIsolation: "none"`); permission prompts are not auto-answered ("Needs input"); finishes with "a report saying what it did and where the work is"; "never pushes to `main` or `master`" — https://code.claude.com/docs/en/agent-view
    67	- Agent teams: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`; "approximately 7x more tokens than standard sessions when teammates run in plan mode" (COSTS); not spawned in `-p`; `TeammateIdle`/`TaskCreated`/`TaskCompleted` exit 2 "send feedback and keep the teammate working"; plan approval: "Claude Code approves the plan in the lead's session as soon as the request arrives, without the lead reviewing it"; "A teammate can't approve a permission prompt or supply consent on your behalf"; teammates inherit lead's mode except `dontAsk`; one team per session, no nesting — TEAMS
    68	- Cross-session messaging (v2.1.224+): Claude uses `ListAgents`/`SendMessage`; incoming message "can't approve anything", "can't change configuration", commands arrive as text; `crossSessionInbound` `accept|hold|refuse`; `-p` sessions bind an inbox (not `--bare`); start a `-p` worker with `crossSessionInbound: accept` in `--settings` — cross-session-messaging
    69	- Workflows: JS script Claude writes; `agent(prompt, { schema, label, stallMs })`, `pipeline()`, `parallel()`, `phase()`, `log()`, `args`; `schema` → "that subagent returns JSON matching the shape" (five validation attempts); 16 concurrent agents default, 1,000 per run; resume: completed agents "return saved result", failed and later ones rerun; in `-p` needs a `Workflow` allow rule, auto mode, bypass, or PreToolUse hook; "have independent agents adversarially review each other's findings" — https://code.claude.com/docs/en/workflows
    70	
    71	## 6. Cost, telemetry, caching
    72	
    73	- `/usage` Session block: total cost, per-model tokens, `Prompt cache (main)` hit ratio and warm/cold; resets on `/clear`; `/cost` is not documented on the costs page (UNVERIFIED as a current command) — COSTS
    74	- OTel (`CLAUDE_CODE_ENABLE_TELEMETRY=1`): metrics `claude_code.session.count`, `lines_of_code.count`, `pull_request.count`, `commit.count`, `cost.usage`, `token.usage`, `code_edit_tool.decision`, `active_time.total`; events `user_prompt`, `tool_result`, `api_request` (`cost_usd`, `input_tokens`, `cache_read_tokens`, `cache_creation_tokens`), `api_error`, `tool_decision` (`source`: `config|hook|user_permanent|...`); `session.id`, `prompt.id` attributes — https://code.claude.com/docs/en/monitoring-usage
    75	- Transcripts: `~/.claude/projects/<project>/<session-id>.jsonl`, `<project>` = cwd with non-alphanumerics → `-`; "The entry format is internal to Claude Code and changes between versions"; session cost totals are saved to the transcript on normal exit (v2.1.277+). Per-message usage in each JSONL line: UNVERIFIED — sessions, cost-tracking
    76	- Cache invalidators: model switch, effort change ("On Opus 5.5, Sonnet 5.5, Haiku 5.5, and Fable 5.1 with an API key or a Claude subscription, the cache stays intact"), fast mode, MCP server connect/remove (when tools loaded upfront), plugin MCP changes, bare-tool deny without tool search, compaction, many images, upgrade. Cache-safe: permission mode change, CLAUDE.md edits (don't apply until `/clear`/`/compact`), skills, `/rewind` — CACHE
    77	- TTL: main conversation 1 h on subscription within plan usage, else 5 min; "Everything else" (subagents, workflows, teammates, forks) 5 min; `promptCacheTtl`/`subagentPromptCacheTtl` or `CLAUDE_CODE_[SUBAGENT_]PROMPT_CACHE_TTL` (`5m|1h`, v2.1.242+); subagent "first request doesn't read the parent's cache"; a fork "reads the parent's cache" — CACHE
    78	
    79	## 7. Quality-loop guidance
    80	
    81	- "If you've corrected Claude more than twice on the same issue in one session, the context is cluttered with failed approaches. Run `/clear` and start fresh with a more specific prompt that incorporates what you learned. A clean session with a better prompt almost always outperforms a long session with accumulated corrections." — BP
    82	- "Give Claude a check it can run: tests, a build, a screenshot to compare"; gates: in one prompt, `/goal`, "a Stop hook runs your check as a script and blocks the turn from ending until it passes", "a verification subagent... has a fresh model try to refute the result, so the agent doing the work isn't the one grading it"; "Have Claude show evidence rather than asserting success" — BP
    83	- "A fresh context improves code review since Claude won't be biased toward code it just wrote"; Writer/Reviewer table across two sessions; "A reviewer running in a fresh subagent context sees only the diff and the criteria you give it... Report gaps, not style preferences" — BP
    84	- Plan mode: "If you could describe the diff in one sentence, skip the plan" — BP
    85	- `/goal`: "a session-scoped prompt-based Stop hook"; evaluator is "your configured small fast model", "does not call tools, so it can only judge what Claude has already surfaced"; stops with warning after "no tool use for several turns in a row"; works in `-p`; unavailable when `disableAllHooks` or `allowManagedHooksOnly` — https://code.claude.com/docs/en/goal
    86	
    87	## 8. Anthropic engineering guidance
    88	
    89	- Building effective agents (https://www.anthropic.com/engineering/building-effective-agents): orchestrator-workers is "well-suited for complex tasks where you can't predict the subtasks needed". Evaluator-optimizer is "particularly effective when we have clear evaluation criteria, and when iterative refinement provides measurable value"; fit signs are that "LLM responses can be demonstrably improved when a human articulates their feedback" and the LLM can provide that feedback. Add complexity only when it "demonstrably improves outcomes"; "Agentic systems often trade latency and cost for better task performance".
    90	- Multi-agent research system (https://www.anthropic.com/engineering/multi-agent-research-system): Opus 4 lead + Sonnet 4 subagents "outperformed single-agent Claude Opus 4 by 90.2%"; "token usage by itself explains 80% of the variance"; "multi-agent systems use about 15× more tokens than chats", so they "require tasks where the value of the task is high enough to pay for the increased performance"; "most coding tasks involve fewer truly parallelizable tasks than research". Judging: "a single LLM call with a single prompt outputting scores from 0.0-1.0 and a pass-fail grade" was most aligned; "focusing on end-state evaluation rather than turn-by-turn analysis"; start with ~20 real queries.
    91	- Demystifying evals (https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents): code-based graders "Fast, Cheap, Objective, Reproducible" but brittle; model-based "Flexible", "Non-deterministic", "Requires calibration with human graders"; prefer "deterministic graders where possible", LLM graders "where necessary"; `pass@k` for one success, `pass^k` "for agents where consistency is essential"; grade each dimension "with an isolated LLM-as-judge"; "Give the LLM a way out"; "You won't know if your graders are working well unless you read the transcripts"; "20-50 simple tasks drawn from real failures is a great start".
    92	- Effective harnesses for long-running agents (https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents): initializer agent + incremental coding agent, `claude-progress.txt`, feature list "initially marked as 'failing'", git commits per step, "It is unacceptable to remove or edit tests", "Self-verify all features. Only mark features as 'passing' after careful testing", "only one feature at a time".
    93	- Harness design for long-running apps, Mar 2026 (https://www.anthropic.com/engineering/harness-design-long-running-apps): planner/generator/evaluator; agents "confidently praising the work—even when... obviously mediocre"; "tuning a standalone evaluator to be skeptical turns out to be far more tractable than making a generator critical of its own work"; sprint contracts with hard per-criterion thresholds; full harness "over 20x more expensive" ($200 vs $9) but on Opus 4.6 tasks within solo capability "no longer needed the evaluator": "It is worth the cost when the task sits beyond what the current model does reliably solo"; "every component in a harness encodes an assumption about what the model can't do on its own".
    94	- Building a C compiler with parallel Claudes, Feb 2026 (https://www.anthropic.com/engineering/building-c-compiler): 16 agents, lock files in `current_tasks/` plus git, no orchestrator; "the task verifier is nearly perfect" or Claude "will solve the wrong problem"; ~2,000 sessions, "just under $20,000"; "it is easy to see tests pass and assume the job is done, when this is rarely the case".
    95	- Auto mode, Mar 2026 (https://www.anthropic.com/engineering/claude-code-auto-mode): two-stage classifier on user messages and tool calls only; "Everything the agent chooses on its own is unauthorized until the user says otherwise"; "Degrade security posture" covers "modifying the agent's own permission config"; runs "at both ends of a subagent handoff" because inside a subagent "the orchestrator's instruction is the user message"; full pipeline FPR 0.4%, FNR on overeager actions 17%.
    96	- No 2026 engineering post on code-review agents or agent teams exists on the index page — https://www.anthropic.com/engineering
     1	# Codex CLI 0.161.0 fact sheet (2026-10-11)
     2	
     3	Source tags: `DOC` = official docs (every `developers.openai.com/codex/*` URL now 308-redirects to `learn.chatgpt.com/docs/*`; final URL cited). `SRC` = `github.com/openai/codex` at tag `rust-v0.161.0`. `CLI` = installed `codex-cli 0.161.0 --help` output (clap only, no model call). `LOCAL` = observed on this machine's `~/.codex`, not official. Third-party claims surfaced by search were dropped.
     4	
     5	DOC short names → `https://learn.chatgpt.com` + : non-interactive-mode=/docs/non-interactive-mode; developer-commands=/docs/developer-commands?surface=cli; config-reference=/docs/config-file/config-reference; config-advanced=/docs/config-file/config-advanced; agent-approvals-security=/docs/agent-approvals-security; permissions=/docs/permissions; hooks=/docs/hooks; rules=/docs/agent-configuration/rules; subagents.md=/docs/agent-configuration/subagents.md; agents-md.md=/docs/agent-configuration/agents-md.md; third-party/github.md=/docs/third-party/github.md; pricing.md=/docs/pricing.md; models.md=/docs/models.md; cloud=/docs/cloud; codex/cli.md=/docs/codex/cli.md; github-code-reviews=/use-cases/github-code-reviews.
     6	
     7	## 1. `codex exec`
     8	
     9	- Default sandbox is read-only: "By default, `codex exec` runs in a read-only sandbox." Progress streams to stderr; only the final agent message goes to stdout. DOC — https://learn.chatgpt.com/docs/non-interactive-mode
    10	- Flags present in 0.161.0 `codex exec --help`: `-c key=value` (value parsed as TOML, dotted paths), `--enable/--disable <feature>`, `--strict-config`, `-m/--model`, `-p/--profile` (layers `$CODEX_HOME/<name>.config.toml`), `-s/--sandbox read-only|workspace-write|danger-full-access`, `--approve-for-me` ("Route approval requests through automatic review using the workspace-write sandbox"), `--dangerously-bypass-approvals-and-sandbox`, `--dangerously-bypass-hook-trust`, `-C/--cd`, `--worktree` ("Run the session in a new managed Git worktree"), `--add-dir`, `--skip-git-repo-check`, `--ephemeral`, `--ignore-user-config`, `--ignore-rules`, `--output-schema <FILE>`, `--json`, `-o/--output-last-message <FILE>`. Subcommands: `resume`, `fork`, `review`. CLI
    11	- `--full-auto`: docs say it is a "deprecated compatibility flag and prints a warning" (DOC — non-interactive-mode page); installed 0.161.0 rejects it: `error: unexpected argument '--full-auto' found`. CLI. SRC `codex-rs/exec/src/lib.rs` has no `full_auto` handling.
    12	- `-a/--ask-for-approval` exists only on top-level `codex` (`on-request | never`); `codex exec -a never` fails with `unexpected argument '-a'`. Set exec approval policy via `-c approval_policy=...`. CLI; the docs' exec flag table also omits it. DOC — https://learn.chatgpt.com/docs/developer-commands?surface=cli
    13	- Headless default: `approval_policy: Some(AskForApproval::Never)` ("Default to never ask for approvals in headless mode"; dropped when the resolved reviewer is AutoReview). SRC — https://raw.githubusercontent.com/openai/codex/rust-v0.161.0/codex-rs/exec/src/lib.rs
    14	- Git check: "Codex requires commands to run inside a Git repository to prevent destructive changes"; override with `--skip-git-repo-check`. DOC — non-interactive-mode. SRC: check is `get_git_repo_root(&default_cwd).is_none()` → prints `Not inside a trusted directory and --skip-git-repo-check was not specified.` and exits 1; also skipped when `--dangerously-bypass-approvals-and-sandbox` is set. Whether a worktree's `.git` _file_ satisfies `get_git_repo_root`: UNVERIFIED (git_info.rs not located at the tag; circumstantial: `codex exec --worktree` exists (CLI) and LOCAL worktree runs succeed).
    15	- JSONL (`--json`): event types `thread.started`, `turn.started`, `turn.completed`, `turn.failed`, `item.*` (`item.started`, `item.completed`), `error`; item types: agent messages, reasoning, command executions, file changes, MCP tool calls, web searches, plan updates. `turn.completed` carries `usage` with `input_tokens`, `cached_input_tokens`, `output_tokens`, `reasoning_output_tokens`. No cost field is documented. DOC — https://learn.chatgpt.com/docs/non-interactive-mode
    16	- `-o` writes the final message to a file "and still prints it to stdout"; docs recommend pairing `--json` with `--output-last-message` in CI. DOC — non-interactive-mode; developer-commands.
    17	- `--output-schema`: docs wording is "request a final response that conforms to a JSON Schema" (DOC — non-interactive-mode) and "Codex validates tool output against it" (DOC — developer-commands). SRC: exec only parses the file as JSON (`Failed to read output schema file`, `... is not valid JSON` → exit 1) and sends it as `output_schema` in `TurnStartParams`; core builds Responses `text.format = {type: json_schema, name: "codex_output_schema", strict: output_schema_strict, schema}` (SRC — `codex-rs/codex-api/src/common.rs`), with `Prompt::default().output_schema_strict = true` ("Whether the Responses API should strictly validate `output_schema`", SRC — `codex-rs/core/src/client_common.rs`). So enforcement is server-side strict JSON schema, no local post-validation; whether core ever overrides `strict` to false for incompatible schemas: UNVERIFIED. The `review` path does not use `output_schema`. SRC — exec/src/lib.rs
    18	- Exit codes: no documented table (DOC — developer-commands documents exit codes only for `apply`, `cloud`, `login status`). SRC: exits 1 on config/startup errors, and after the run `if error_seen { std::process::exit(1) }` where `error_seen` is set by a non-retried `Error` notification, a `TurnCompleted` with status `Failed`/`Interrupted`, or a failed server-request response; otherwise 0. SRC — exec/src/lib.rs. An enabled MCP server with `required = true` that fails to start makes exec "exit with an error". DOC — non-interactive-mode
    19	- `resume`: `codex exec resume --last "<prompt>"` or `codex exec resume <SESSION_ID|thread name> [PROMPT]`; `--all` disables cwd filtering. DOC — non-interactive-mode; CLI
    20	- `--ephemeral`: "Run without persisting session files to disk." CLI; DOC — non-interactive-mode
    21	- Auth: reuses CLI login; `CODEX_API_KEY` works for a single run (also for `codex review`); docs warn against job-level API keys in workflows running repo-controlled code, and against ChatGPT `auth.json` in public repos. DOC — non-interactive-mode
    22	
    23	## 2. `codex review`
    24	
    25	- Top-level `codex review [PROMPT]` flags: `--uncommitted` ("staged, unstaged, and untracked"), `--base <BRANCH>`, `--commit <SHA>`, `--title` (requires `--commit`), `-c`, `--enable/--disable`, `--strict-config`. No `-m`, `--json`, `-o`, `--output-schema`, `--sandbox`. CLI; DOC — developer-commands. `--uncommitted`, `--base`, `--commit` and a custom PROMPT "conflict with one another". DOC — developer-commands
    26	- `codex exec review [PROMPT]` additionally accepts `-m`, `--json`, `-o`, `--output-schema`, `--worktree`, `--ephemeral`, `--skip-git-repo-check`, `--ignore-rules`, `--dangerously-bypass-*`. CLI (not in the docs table). `--output-schema` is ignored on the review path (SRC — exec/src/lib.rs). Whether `--json` emits findings as a structured item: UNVERIFIED (not run; would consume quota).
    27	- Output: "Codex reports prioritized findings without modifying your working tree." DOC — https://learn.chatgpt.com/docs/codex/cli.md. Internal structure: `ReviewOutputEvent { findings: Vec<ReviewFinding>, overall_correctness: String, overall_explanation: String, overall_confidence_score: f32 }`, `ReviewFinding { title, body, confidence_score: f32, priority: i32, code_location: { absolute_file_path, line_range { start, end } } }`. SRC — https://raw.githubusercontent.com/openai/codex/rust-v0.161.0/codex-rs/protocol/src/protocol.rs. The P0–P3 definitions come from a server-side review prompt: UNVERIFIED (not in the binary strings or repo at this tag).
    28	- `review_model`: "Optional model override used by `/review` (defaults to the current session model)." DOC — https://learn.chatgpt.com/docs/config-file/config-reference. Applicability to `codex review` CLI: UNVERIFIED.
    29	- `approvals_reviewer = user | auto_review`: "Who reviews eligible approval prompts under `on-request` or granular approval policies"; default `user`; `auto_review` uses a reviewer subagent, does not change sandboxing, "Prompt-build, review-session, and parse failures fail closed", critical-risk actions denied, uses extra model calls. DOC — config-reference; https://learn.chatgpt.com/docs/agent-approvals-security. `--approve-for-me` is the CLI switch (CLI only; not in docs).
    30	
    31	## 3. `config.toml`
    32	
    33	- `approval_policy`: `on-request | never | { granular = { sandbox_approval, rules, mcp_elicitations, request_permissions, skill_approval } }`. "`untrusted` is unsupported" and "can prevent startup"; `on-failure` deprecated ("use `on-request` for interactive runs and `never` for non-interactive runs"). DOC — config-reference; agent-approvals-security
    34	- `sandbox_mode`: `read-only | workspace-write | danger-full-access`. `[sandbox_workspace_write]`: `network_access` ("Allow outbound network access inside the workspace-write sandbox"), `writable_roots` ("Additional writable roots"), `exclude_tmpdir_env_var` (exclude `$TMPDIR`), `exclude_slash_tmp` (exclude `/tmp`). Must not be combined with `default_permissions`/`[permissions]`. DOC — config-reference; https://learn.chatgpt.com/docs/permissions
    35	- `notify = ["cmd", ...]`: invoked "whenever Codex emits supported events (currently only `agent-turn-complete`)"; single JSON argument with `type`, `thread-id`, `turn-id`, `cwd`, `input-messages`, `last-assistant-message`. DOC — https://learn.chatgpt.com/docs/config-file/config-advanced
    36	- `model_reasoning_effort`: "such as `low`, `medium`, `high`, `xhigh`, `max`, or `ultra`"; levels "depend on the model and client"; `plan_mode_reasoning_effort` override. DOC — config-reference
    37	- `[features]`: `hooks` ("Enable lifecycle hooks loaded from `hooks.json` or inline `[hooks]`"; `codex_hooks` deprecated alias), `multi_agent` (on by default), `network_proxy`, `web_search`, etc. DOC — config-reference. Installed: `hooks stable true`, `multi_agent stable true`, `multi_agent_v2 stable false`, `network_proxy experimental false`. CLI (`codex features list`)
    38	- `[hooks]`: events `PreToolUse`, `PermissionRequest`, `PostToolUse`, `PreCompact`, `PostCompact`, `SessionStart`, `SessionEnd`, `SubagentStart`, `SubagentStop`, `UserPromptSubmit`, `Stop`, `Interrupt`. Handler types `command`, `mcp_tool` (`prompt`/`agent` parsed but skipped); `timeout` seconds (default 600; `SessionEnd`/`Interrupt` default 1, max 3); `async` (background, cannot block); `additionalContextLimit` default 2500. Sources: `~/.codex/hooks.json`, `~/.codex/config.toml`, `<repo>/.codex/hooks.json`, `<repo>/.codex/config.toml` (project hooks only when the project `.codex/` layer is trusted), plugins, managed `requirements.toml`. Non-managed hooks "must be reviewed and trusted"; trust is per hash, "new or changed hooks are marked for review and skipped until trusted"; `--dangerously-bypass-hook-trust` skips that for one invocation. DOC — https://learn.chatgpt.com/docs/hooks
    39	- Hook input: common `session_id`, `transcript_path`, `cwd`, `hook_event_name`, `model`, `permission_mode`; `PreToolUse`/`PostToolUse`: `turn_id`, `tool_name` (`Bash`, `apply_patch` with `Edit`/`Write` aliases, MCP names), `tool_use_id`, `tool_input` (`tool_input.command` for Bash), `tool_response`; `PermissionRequest`: `tool_name`, `tool_input(.description)`; `Stop`/`SubagentStop`: `stop_hook_active`, `last_assistant_message` (+ `agent_id`, `agent_type`, `agent_transcript_path`); `UserPromptSubmit`: `prompt`; `SessionStart`: `source` (`startup|resume|clear|compact`); `SessionEnd`: `reason`. DOC — hooks
    40	- Hook semantics: exit 0 no output = continue; exit 2 + stderr reason blocks for `PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `SubagentStop`, `Stop`. `PreToolUse`: `hookSpecificOutput.permissionDecision: "deny"|"allow"` (+`updatedInput`); `"ask"` unsupported (hook fails, tool call continues). `PermissionRequest`: `hookSpecificOutput.decision.behavior: "allow"|"deny"`, "any `deny` wins", no decision → normal prompt. `Stop`: `decision: "block"` "doesn't reject the turn" but injects a continuation prompt; `continue: false` wins. `SessionEnd` advisory only. `Interrupt` cannot be prevented. DOC — hooks. Whether hooks fire under `codex exec`: UNVERIFIED (docs silent; the only evidence is that `codex exec` exposes `--dangerously-bypass-hook-trust`).
    41	- `[agents]`: `enabled` (default true), `max_concurrent_threads_per_session` (`max_threads` legacy alias; default not documented), `default_subagent_model`, `default_subagent_reasoning_effort`, `interrupt_message`; roles as `agents.<name>` with `config_file`/`description` (DOC — config-reference) or standalone TOML in `~/.codex/agents/`/`.codex/agents/` with `name`, `description`, `developer_instructions`, optional `sandbox_mode` (DOC — https://learn.chatgpt.com/docs/agent-configuration/subagents.md). `max_depth`: UNVERIFIED (not in either page).
    42	- Profiles: `$CODEX_HOME/<name>.config.toml` layered by `--profile`; "In Codex 0.134.0 and later, `--profile` no longer reads `[profiles.profile-name]`"; project `.codex/config.toml` cannot set `profile`. DOC — config-advanced; config-reference
    43	- Rules: `rules/*.rules` next to each active config layer (`~/.codex/rules/default.rules`; `<repo>/.codex/rules/` only when trusted); Starlark `prefix_rule(pattern=[...], decision="allow"|"prompt"|"forbidden", justification, match, not_match)`; strictest wins; `allow` runs the command outside the sandbox without prompting; test with `codex execpolicy check --pretty --rules <file> -- <cmd>`. DOC — https://learn.chatgpt.com/docs/agent-configuration/rules. `--ignore-rules` skips user and project rules. CLI
    44	- `project_doc_max_bytes`: "Maximum bytes read from `AGENTS.md`", default 32 KiB; discovery `~/.codex/AGENTS.override.md|AGENTS.md`, then project root down to cwd, one file per directory, concatenated root-first, nearer files later. DOC — https://learn.chatgpt.com/docs/agent-configuration/agents-md.md
    45	- `shell_environment_policy`: `inherit = all|core|none`, `filters` (include/exclude patterns), `set`, `ignore_default_excludes` ("Keep variables containing KEY, SECRET, or TOKEN before other filters run (default: true)"), `experimental_use_profile`. DOC — config-reference
    46	- `projects.<path>.trust_level = "trusted"|"untrusted"`; "Untrusted projects skip project-scoped `.codex/` layers, including project-local config, hooks, and rules." DOC — config-reference
    47	- `history.persistence = save-all|none`, `history.max_bytes`; `log_dir` (default `$CODEX_HOME/log`); `sqlite_home`. DOC — config-reference
    48	
    49	## 4. GitHub "Codex" review bot
    50	
    51	- Triggers: `@codex review` comment (Codex reacts 👀 then posts a review); `@codex review for <focus>`; `@codex security review`; Automatic review per repository ("Review code" setting, needs GitHub push/admin) and per user ("Personal preferences", "Choose timing with Review trigger" — options not enumerated). Any other `@codex ...` (e.g. `@codex fix the P1 issue`) "starts a legacy cloud chat with the pull request as context"; Codex "can push a fix back to the branch when it has permission". DOC — https://learn.chatgpt.com/docs/third-party/github.md
    52	- Output: "a standard GitHub code review focused on serious issues"; "In GitHub, Codex flags only P0 and P1 issues"; the example shows a `[P1]` label on a line-anchored comment. Inline vs summary layout and P2/P3 handling: not documented. DOC — third-party/github.md
    53	- `AGENTS.md`: Codex "searches your repository for `AGENTS.md` files and follows the applicable code review rules"; put a `## Code Review Rules` section (`###` groups) in the file closest to the governed code; root = repo-wide, nested = service-specific; "applies the root and more-specific guidance that covers each changed file"; keep lint/format to CI. DOC — third-party/github.md; https://learn.chatgpt.com/use-cases/github-code-reviews
    54	- Quota: "Code Review usage applies only when Codex runs reviews through GitHub. Reviews run locally or outside of GitHub count toward your general usage limits." DOC — https://learn.chatgpt.com/docs/pricing.md. Numeric review quotas: UNVERIFIED.
    55	- Re-review on every push, hidden-directory (`.orchestration/`) coverage, draft PRs, and requesting a review of a specific commit: UNVERIFIED (not in any official page; only GitLab documents "On every push").
    56	
    57	## 5. Session logs and usage
    58	
    59	- State root: `CODEX_HOME` (default `~/.codex`); `history.jsonl` when persistence enabled; logs under `log_dir` (default `$CODEX_HOME/log`). DOC — config-advanced; config-reference. `--ephemeral` skips "session rollout files". DOC — non-interactive-mode
    60	- No official page names `~/.codex/sessions` (hooks input `transcript_path` is the only official acknowledgment of a per-session transcript file, DOC — hooks). LOCAL: rollouts live at `~/.codex/sessions/YYYY/MM/DD/rollout-<ts>-<uuid>.jsonl` plus `session_index.jsonl` and `logs_2.sqlite`/`state_5.sqlite`; `codex migrate-rollouts` "migrate[s] legacy local sessions to paginated thread history" (CLI), i.e. the on-disk format is in transition (`ThreadHistoryMode legacy|paginated` strings in the binary).
    61	- Per-turn usage is recorded: LOCAL rollout lines `event_msg`/`token_count` carry `info.total_token_usage` and `info.last_token_usage` (`input_tokens`, `cached_input_tokens`, `cache_write_input_tokens`, `output_tokens`, `reasoning_output_tokens`, `total_tokens`), `model_context_window`, and `rate_limits` (`primary.used_percent`, `window_minutes` (10080 observed), `resets_at`, `credits.balance`, `plan_type`). Field names match SRC `TokenCountEvent { info: Option<TokenUsageInfo>, rate_limits: Option<RateLimitSnapshot> }`, `RateLimitWindow { used_percent, window_minutes, resets_at }`. SRC — protocol.rs
    62	- From a finished `codex exec --json` run, read `turn.completed.usage` (tokens only; no cost, no rate-limit snapshot documented). DOC — non-interactive-mode. In the TUI, `/status` and `/usage` show limits and token activity. DOC — developer-commands
    63	
    64	## 6. Sandbox
    65	
    66	- macOS "uses Seatbelt policies and runs commands using `sandbox-exec`"; "Linux uses `bwrap` plus `seccomp` by default" (Landlock not mentioned; moved to bwrap in 0.115; WSL1 unsupported); Windows MXC. If the platform sandbox cannot enforce the policy, Codex "refuses to run the command instead of silently running it unsandboxed". DOC — agent-approvals-security; permissions
    67	- workspace-write: "Defaults include no network access and write permissions limited to the active workspace"; workspace = cwd plus "temporary directories like `/tmp`" (`$TMPDIR` via `:tmpdir` in permissions profiles); network only with `[sandbox_workspace_write] network_access = true`. DOC — agent-approvals-security; permissions. Network in read-only mode: UNVERIFIED (docs state only that network is off by default and `:read-only` "keeps local command execution read-only").
    68	- Protected paths inside writable roots: "`<writable_root>/.git` is protected as read-only whether it appears as a directory or file"; for a `gitdir:` pointer file "the resolved directory is also protected"; `.codex` and `.agents` directories likewise; "Protection is recursive". DOC — agent-approvals-security. So in workspace-write, neither a worktree's `.git` file nor its resolved per-worktree gitdir is writable; whether the shared _common_ dir (`commondir`) is also protected: UNVERIFIED.
    69	- `danger-full-access`: no sandbox, no approvals; `--dangerously-bypass-approvals-and-sandbox` (`--yolo`) also skips the git check. DOC — agent-approvals-security; SRC — exec/src/lib.rs
    70	- Worktrees: `--worktree` on `codex exec`/`review` runs "in a new managed Git worktree" (CLI); `codex exec` in an existing worktree directory needing `--skip-git-repo-check`: UNVERIFIED.
    71	
    72	## 7. Rate limits, cost, effort
    73	
    74	- ChatGPT sign-in: usage draws on the plan's allowance; Plus $20, Pro $100/$200/$500; "Pro plans currently have no five-hour limit"; Plus/Standard Business message estimates are "per five-hour period" and "Weekly limits may also apply"; Plus/Pro can buy credits. API key: "Pay for Codex usage based on API pricing"; models "follow the API models available to your key". DOC — https://learn.chatgpt.com/docs/pricing.md
    75	- Credit rates per 1M tokens (input/cached/output): GPT-6 Astra 250/25/1,250; GPT-6.1 Sol 50/2.5/250; GPT-6 Luna 2.5/0.25/12.5; Fast 2.5x, Ultrafast 8x of included usage. DOC — pricing.md
    76	- `help.openai.com/en/articles/11369540` could not be fetched (JS wall/403): help-center specifics UNVERIFIED.
    77	- Effort: config names `low|medium|high|xhigh|max|ultra`; models page calls them Light/Medium/High/Extra High/Max/Ultra; "Higher reasoning effort can improve results for complex tasks, but it takes longer and uses more tokens"; "Most tasks do not need Max or Ultra"; Ultra "uses subagents"; Luna supports up to Max; some paid plans omit Extra High on Astra. No quantitative xhigh cost/latency guidance exists. DOC — https://learn.chatgpt.com/docs/models.md
    78	
    79	## 8. Multi-agent guidance
    80	
    81	- Subagents are on by default; orchestration (spawn, route follow-ups, wait, close) is handled by Codex; "Subagents inherit your current sandbox policy"; a custom agent file may set `sandbox_mode`; in the CLI the parent's live overrides (`/permissions`, `--yolo`) are reapplied to children; "In non-interactive flows ... an action that needs new approval fails and Codex surfaces the error back to the parent workflow"; subagent runs "consume more tokens"; recommended for read-heavy parallel work, caution for parallel writes. DOC — https://learn.chatgpt.com/docs/agent-configuration/subagents.md
    82	- Collaboration tools listed under `features.multi_agent`: `spawn_agent`, `send_input`, `resume_agent`, `wait_agent`, `close_agent`. DOC — config-reference
    83	- Codex Cloud: "Each task has its own workspace and can keep working while your computer is asleep"; tasks start from a published environment; `codex cloud exec --env --attempts 1–4`, `codex cloud list --json`; "Cloud tasks may use more of your allowance than local messages". DOC — https://learn.chatgpt.com/docs/cloud; developer-commands; pricing.md
     1	# GitHub merge-gate mechanics for a user-owned repo (facts as of 2026-10-11)
     2	
     3	Sources: docs.github.com, cli.github.com/manual, github.blog changelog, docs.coderabbit.ai, learn.chatgpt.com (redirect target of developers.openai.com/codex). "UNVERIFIED" = no fetched official page states it.
     4	
     5	## 1. Rulesets on a personal repository
     6	
     7	- Repo-level ruleset rules: require PR; required approvals; dismiss stale approvals; code-owner review; "Require approval of the most recent reviewable push"; conversation resolution; merge method; required status checks (strict/loose, app source); require deployments; code scanning; code quality; signed commits; linear history; restrict creations/updates/deletions; block force pushes; file path/size/extension limits. — https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets
     8	- Only rule explicitly denied to user-owned repos: team-based required reviewers — "This rule is not available on user-owned repositories as they do not contain teams." — same URL.
     9	- "Require merge queue" and "Require deployments to succeed" are repo-level rules: "This rule is not available for rulesets created at the organization level." (restriction on org-level, not on user-owned). — https://docs.github.com/en/enterprise-cloud@latest/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets
    10	- Required workflows: "Ruleset workflows can be configured at the organization or enterprise level"; supported events `pull_request`, `pull_request_target`, `merge_group`, "Any filters you specify for the supported events are ignored"; "Applying this rule will block direct pushes." — same enterprise-cloud URL. Changelog: requiring a workflow "will only be available on GitHub Enterprise plans via Repository Rules"; old Actions Required Workflows removed "On October 18th" (2023). — https://github.blog/changelog/2023-08-02-github-actions-required-workflows-will-move-to-repository-rules/ . No page mentions user-owned repos (explicit denial UNVERIFIED).
    11	- Merge queue availability: "Merge queue is available on private and public repos on the GitHub Enterprise Cloud plan" and "all public repos owned by organizations". No page mentions user-owned repos. — https://github.blog/changelog/2023-07-12-pull-request-merge-queue-is-now-generally-available/
    12	- Ruleset plan gating for a private personal repo: UNVERIFIED. Plans page lists "Protected branches", "Code owners", "Required pull request reviewers" under Pro "in private repositories"; Free lists only "Deployment protection rules for public repositories". — https://docs.github.com/en/get-started/learning-about-github/githubs-plans
    13	- Bypass actors: "Repository admins, organization owners, and enterprise owners", maintain/write roles, teams, GitHub Apps, Dependabot; modes "Always allow" / "For pull requests only". — https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository . REST `bypass_actors[].actor_type`: Integration, OrganizationAdmin, RepositoryRole, Team, DeployKey, User; `bypass_mode`: always, pull_request, exempt. — https://docs.github.com/en/rest/repos/rules
    14	- Tamper ceiling: repo admins edit repo rulesets; only org-level rulesets are locked ("only owners of the organization can edit the ruleset"). — https://docs.github.com/en/organizations/managing-organization-settings/creating-rulesets-for-repositories-in-your-organization
    15	- Self-approval: "Pull request authors cannot approve their own pull requests." — https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/approving-a-pull-request-with-required-reviews . Personal-account default: "workflows are not allowed to create or approve pull requests." — https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository . Copilot default review is "Comment"; approvals are public preview, "off by default". — https://docs.github.com/en/copilot/how-tos/use-copilot-agents/request-a-code-review/use-code-review . Consequence: with one write account, approval count >= 1, code-owner review and last-push approval are unsatisfiable without bypass.
    16	- Code owners "must have write permissions for the repository". — https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
    17	- Signed commits: unsigned head commits can block even a signed squash; linear history needs squash/rebase enabled; block force pushes and restrict deletions are on by default. — available-rules URL above.
    18	
    19	## 2. Trust model of status checks
    20	
    21	- `pull_request_target` "runs in the context of the default branch of the base repository, rather than in the context of the merge commit"; "This prevents execution of unsafe code from the head of the pull request that could alter your repository"; "Running untrusted code on the `pull_request_target` trigger may lead to security vulnerabilities." `pull_request`: `GITHUB_SHA` "is the last merge commit of the pull request merge branch" (that `pull_request` runs the PR-side workflow file is an inference from these contrasting statements plus the fork-approval page; no page states it directly). — https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows
    22	- Fork PR approval doc: review proposed changes "especially to `.github/workflows/`" before approving a run. — https://docs.github.com/en/actions/managing-workflow-runs-and-deployments/managing-workflow-runs/approving-workflow-runs-from-public-forks
    23	- `pull_request_target`/`workflow_run` "may have repository write access and access to referenced secrets"; they "must not explicitly check out untrusted code, including from pull request forks". "Pinning an action to a full-length commit SHA is currently the only way to use an action as an immutable release." Add the workflows dir to CODEOWNERS so changes "will first require approval". — https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions
    24	- `workflow_run`: "This event will only trigger a workflow run if the workflow file exists on the default branch"; "able to access secrets and write tokens, even if the previous workflow was not"; `GITHUB_SHA` = "Last commit on default branch". — events URL above.
    25	- Required-check eligibility: workflow-job checks count only when the run "must be triggered by one of these events": push, pull_request, pull_request_review, pull_request_target, deployment, deployment_status; `workflow_run` and `workflow_dispatch` are not listed (`workflow_dispatch` checks "do not appear in the pull request's checks section"); merge queue needs `merge_group`; this "restriction applies only to checks created by workflow jobs, not to checks created by an external GitHub App". Error text: "Required status check "build" was not set by the expected GitHub App." — https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/troubleshooting-required-status-checks
    26	- App source: "you can select an app as the expected source of status updates"; app needs `statuses:write` and a recent check run. — available-rules URL. REST ruleset `required_status_checks[].integration_id`: "The optional integration ID that this status check must originate from." — https://docs.github.com/en/rest/repos/rules . Branch protection `checks[].app_id`: "Pass -1 to explicitly allow any app to set the status." — https://docs.github.com/en/rest/branches/branch-protection . Note: a PR-edited and a base-branch workflow both report through the same GitHub Actions app, so app-source pinning does not distinguish them (inference from the above; no page states it).
    27	- Reusable workflows: `{owner}/{repo}/.github/workflows/{filename}@{ref}`, "the `{ref}` can be a SHA, a release tag, or a branch name"; "Using the commit SHA is the safest option"; local `./` reference "is from the same commit as the caller workflow". — https://docs.github.com/en/actions/sharing-automations/reusing-workflows
    28	- Environments: "Users with GitHub Free plans can only configure environments for public repositories"; Pro covers private; required reviewers "up to 6 people or teams"; option "to prevent users from approving workflows runs that they triggered". — https://docs.github.com/en/actions/managing-workflow-runs-and-deployments/managing-deployments/managing-environments-for-deployment
    29	- CODEOWNERS enforced only with "Require review from Code Owners"; sole owner = PR author (see self-approval). — about-code-owners URL.
    30	- User-owned availability: pull_request_target, workflow_run, reusable workflows, app-source checks, CODEOWNERS: no restriction stated; environments: public only on Free; required workflows: org/enterprise only.
    31	
    32	## 3. gh CLI and API surfaces
    33	
    34	- `gh pr merge --match-head-commit <SHA>`: "Commit SHA that the pull request head must match to allow merge"; `--auto`: "Automatically merge only after necessary requirements are met"; `--admin`: "Use administrator privileges to merge a pull request that does not meet requirements"; on a branch requiring a merge queue, if checks have not passed "auto-merge will be enabled", else the PR is added to the queue. — https://cli.github.com/manual/gh_pr_merge
    35	- `gh pr update-branch`: "The default behavior is to update with a merge commit"; `--rebase` to rebase. — https://cli.github.com/manual/gh_pr_update-branch
    36	- `gh pr checks`: `--watch`, `--fail-fast`, `--required`, `--interval` (default 10); exit code "8: Checks pending"; JSON `bucket` in pass/fail/pending/skipping/cancel. — https://cli.github.com/manual/gh_pr_checks
    37	- `gh pr review --approve|--request-changes|--comment`; manual silent on self-approval (server rule above applies). — https://cli.github.com/manual/gh_pr_review
    38	- `gh api --paginate` ("Make additional HTTP requests to fetch all pages"), `--slurp`, `--jq`; GraphQL via endpoint `graphql`; `--paginate` with GraphQL "requires that the original query accepts an `$endCursor: String` variable". — https://cli.github.com/manual/gh_api
    39	- Check runs: `GET /repos/{owner}/{repo}/commits/{ref}/check-runs` (per_page default 30, max 100; `check_name`, `status`, `filter=latest|all`, `app_id`); `GET .../check-runs/{id}/annotations` (default 30, max 100); `annotation_level`: `notice`, `warning`, `failure`; "maximum of 50 per API request", appended on update; create/update "only available to GitHub Apps"; Actions "limited to 10 warning and 10 error annotations per step". — https://docs.github.com/en/rest/checks/runs ; "For most endpoints, the maximum value of `per_page` is `100`." — https://docs.github.com/en/rest/using-the-rest-api/using-pagination-in-the-rest-api
    40	- GraphQL `resolveReviewThread(input: {threadId: ID!})` "Marks a review thread as resolved."; `unresolveReviewThread` likewise; `PullRequestReviewThread.isResolved`, `resolvedBy`, `viewerCanResolve`. — https://docs.github.com/en/graphql/reference/pulls
    41	
    42	## 4. Branch protection vs rulesets; up-to-date; auto-merge; skipped checks
    43	
    44	- Both can apply; "all applicable rules are enforced"; "the most restrictive version of the rule applies"; "A ruleset does not have a priority." — https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets
    45	- Classic protection: by default "don't apply to people with admin permissions" unless "Do not allow bypassing the above settings"; strict = "The branch **must** be up to date with the base branch before merging"; required checks need `successful`, `skipped`, or `neutral`. — https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/about-protected-branches ; REST `strict_required_status_checks_policy`: "Whether pull requests targeting a matching branch must be tested with the latest code." — rest/repos/rules URL
    46	- Squash + up-to-date: no page addresses squash specifically (UNVERIFIED). Merge queue intro: provides the benefit of up-to-date but "does not require a pull request author to update their pull request branch and wait for status checks". — managing-a-merge-queue URL
    47	- Auto-merge: "merges a pull request automatically after all required reviews and status checks pass"; "disabled if someone without write permissions pushes new changes to the head branch or switches the base branch"; must be enabled per repository. — https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/automatically-merging-a-pull-request
    48	- Skipped required checks: path/branch/commit-message skips "stay in a "Pending" state and block merging" ("Waiting for status to be reported"); guidance "Avoid requiring workflows that can be skipped."; `if`-skipped job "reports "Success""; job after failed dependency "is skipped and may not block merging" -> use `always()` with `needs`; "If a check and a commit status have the same name, both must pass". The current cloud page has no duplicate-workflow/`paths-ignore` example. — troubleshooting URL above
    49	- Checks are evaluated on the test merge commit when it has a status, else on the head commit. — troubleshooting URL
    50	
    51	## 5. GitHub Actions mechanics
    52	
    53	- Concurrency: "at most one running job or workflow in a concurrency group at any time"; `cancel-in-progress: true`; "Up to 100 jobs or workflow runs can be `pending`"; `group: ${{ github.head_ref || github.run_id }}`. — https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/control-the-concurrency-of-workflows-and-jobs
    54	- OIDC: provider "issues a short-lived access token that is only valid for a single job"; claims `sub`, `repository`, `ref`, `environment`, `job_workflow_ref` (e.g. `octo-org/octo-automation/.github/workflows/oidc.yml@refs/heads/main`). — https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect
    55	- Attestations: "cryptographically signed claims that establish your build's provenance"; public repos use Sigstore Public Good with transparency log, private use GitHub's Sigstore instance; "SLSA v1.0 Build Level 2". — https://docs.github.com/en/actions/concepts/security/artifact-attestations . How-to uses `actions/attest@v4` with `permissions: id-token: write, contents: read, attestations: write`; verify with `gh attestation verify PATH -R OWNER/REPO`. — https://docs.github.com/en/actions/security-for-github-actions/using-artifact-attestations/using-artifact-attestations-to-establish-provenance-for-builds . GA changelog used `actions/attest-build-provenance@v1`; "supports both public and private repositories". — https://github.blog/changelog/2024-06-25-artifact-attestations-is-generally-available/ . Private-repo plan gating: UNVERIFIED.
    56	- Annotations: `::error file={name},line={line},endLine={endLine},title={title}::{message}` (also `::warning`, `::notice`); `GITHUB_STEP_SUMMARY` "maximum size of 1MiB" per step, "A maximum of 20 job summaries from steps are displayed per job." — https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/workflow-commands-for-github-actions
    57	- `GITHUB_TOKEN` defaults for personal-account repos: "only has read access for the `contents` and `packages` scopes"; "workflows are not allowed to create or approve pull requests"; fork approval: "By default, all first-time contributors require approval". — managing-github-actions-settings URL . "events triggered by the `GITHUB_TOKEN` will not create a new workflow run." — https://docs.github.com/en/actions/concepts/security/github_token . Scopes include `checks`, `statuses`, `pull-requests`, `id-token`, `attestations`; "If you specify the access for any of these permissions, all of those that are not specified are set to `none`." Fork PRs: "The `GITHUB_TOKEN` has read-only permissions in pull requests from forked repositories." — https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax ; events URL
    58	- Reading another PR's checks: check-runs listing is a read endpoint ("OAuth apps and authenticated users can view check runs"); a job with `checks: read` can query it (combination of two docs; no single page states it).
    59	
    60	## 6. Bots
    61	
    62	- Codex (OpenAI): trigger with `@codex review` in a PR comment; "Codex flags only P0 and P1 issues"; "posts a standard GitHub code review"; automatic review via Codex settings ("GitHub push or admin permission for its settings"); `## Code Review Rules` in nearest `AGENTS.md`; follow-up e.g. "@codex fix the P1 issue". Rate limits and approve/request-changes behaviour: UNVERIFIED. — https://learn.chatgpt.com/docs/third-party/github (redirect target of https://developers.openai.com/codex/integrations/github); https://developers.openai.com/codex/use-cases/github-code-reviews
    63	- CodeRabbit: limits "enforced **per developer** over rolling time windows"; PR reviews/hour: Free 1 (summary only), OSS 1–10, Essentials 5, Team 8, Advanced 10, Enterprise 12; files/review 150–300; "Open-source projects receive Team features". — https://docs.coderabbit.ai/management/plans . "CodeRabbit reviews pushes, not commits"; default "an incremental review on every push, and a pause after five reviewed commits"; rate-limited push posts check "Review rate limited" that passes "so it never blocks merging on protected branches"; `@coderabbitai rate limit`, `@coderabbitai review`. — https://docs.coderabbit.ai/management/rate-limits . `@coderabbitai review` = "incremental review of new changes only"; `@coderabbitai full review` = "complete review of all files from scratch"; `@coderabbitai resolve` "Marks all CodeRabbit review comments as resolved." — https://docs.coderabbit.ai/reference/review-commands
    64	- Copilot code review: `gh pr edit PR-NUMBER --add-reviewer @copilot`, `gh pr create --reviewer @copilot`, REST reviewer `copilot-pull-request-reviewer[bot]`; default "Copilot leaves a "Comment" review"; approvals public preview, dismissed on new commits; re-review only on request unless "Review new pushes" ruleset; "Copilot may repeat the same comments". — use-code-review URL . Plans: automatic reviews "available on the Copilot Pro, Copilot Pro+, and Copilot Max plans" or Business/Enterprise license; "Copilot Free plan, which does not include Copilot code review"; "In personal repositories, only the repository owner or a direct collaborator can request a review."; billed in AI credits; no per-review quota stated. — https://docs.github.com/en/copilot/concepts/agents/code-review
    65	
    66	## 7. PR size
    67	
    68	- Only official guidance: "Write small pull requests" — "Small, focused pull requests are easier to review and safer to merge."; "When a change grows large, consider splitting it into smaller pull requests that each serve one purpose." No numeric limit. — https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/getting-started/best-practices-for-pull-requests
    69	- No github.blog PR-size research found.

    for comment in flatten(fetch(f"repos/{repo}/issues/{number}/comments", True)):
        items.append(
            item(
                "issue_comment",
                comment["user"],
                "comment",
                comment["body"],
                comment["html_url"],
            )
        )
    for review in flatten(fetch(f"repos/{repo}/pulls/{number}/reviews", True)):
        items.append(
            item(
                "review",
                review["user"],
                review["state"].lower(),
                review["body"],
                review["html_url"],
                commit=review.get("commit_id"),
            )
        )
    states = thread_states(repo, number, graphql)
    for comment in flatten(fetch(f"repos/{repo}/pulls/{number}/comments", True)):
        state = states.get(comment["id"], {"resolved": False, "outdated": False})
        items.append(
            item(
                "review_comment",
                comment["user"],
                "comment",
                comment["body"],
                comment["html_url"],
                comment["path"],
                comment.get("line") or comment.get("original_line"),
                **state,
            )
        )

    checks = []
    for run in flatten(fetch(f"repos/{repo}/commits/{sha}/check-runs", True), "check_runs"):
        conclusion = run.get("conclusion") or run.get("status")
        checks.append({"name": run["name"], "conclusion": conclusion, "url": run["html_url"]})
        output = run.get("output") or {}
        if conclusion not in PASSING_CONCLUSIONS:
            summary = " ".join(part for part in (output.get("title"), output.get("summary")) if part)
            items.append(
                item(
                    "check_run",
                    run.get("app"),
                    conclusion,
                    f"{run['name']}: {summary}".strip(),
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
  changes:
    runs-on: ubuntu-24.04
    outputs:
      should_test: ${{ steps.filter.outputs.should_test }}
      diff_range: ${{ steps.filter.outputs.diff_range }}

    steps:
      - name: Configure Git defaults
        run: git config --global init.defaultBranch main

      - name: Checkout repository
        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7
        with:
          fetch-depth: 0
          persist-credentials: false

      - name: Detect unit-test-relevant changes
        id: filter
        env:
          EVENT_NAME: ${{ github.event_name }}
          BASE_REF: ${{ github.base_ref }}
          BEFORE_SHA: ${{ github.event.before }}
          HEAD_SHA: ${{ github.sha }}
        run: |
          set -euo pipefail

          # Keep the diff calculation here so the required workflow can always
          # start and report a final status before we decide whether to run the
          # heavier test steps.
          if [ "${EVENT_NAME}" = "pull_request" ]; then
            git fetch --no-tags --depth=1 origin "${BASE_REF}"
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
          changed="$(git -c core.quotePath=false diff --name-only "${diff_range}")"
          relevant="$(grep -v '^\.orchestration/' <<< "${changed}" || true)"
          if grep -Eq '^(\.github/workflows/|home/|install/|scripts/|tests/|plans/|docs/|setup\.sh$|Makefile$|ruff\.toml$|\.prettierignore$)|(^|/)[^/]+\.(py|md)$' <<< "${relevant}"; then
            echo "should_test=true" >> "${GITHUB_OUTPUT}"
          else
            echo "should_test=false" >> "${GITHUB_OUTPUT}"
          fi

  test:
    needs: changes
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
          persist-credentials: false

      - name: Skip full unit test run for unrelated changes
      - name: Skip full unit test run for unrelated changes
        if: ${{ needs.changes.outputs.should_test != 'true' }}
        run: |
          echo "No unit-test-relevant files changed."
          echo "Compared diff range: ${{ needs.changes.outputs.diff_range }}"

      - name: Install tools
        if: ${{ needs.changes.outputs.should_test == 'true' }}
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
          curl -fsSL "${base_url}/${artifact}" -o "${RUNNER_TEMP}/${artifact}"
          curl -fsSL "${base_url}/chezmoi_${chezmoi_version}_checksums.txt" \
            | grep "  ${artifact}$" \
            | (cd "${RUNNER_TEMP}" && "${sha256_check[@]}")
          # The checksum file comes from the same release; the attestation is the publisher's
          # check, verified before chezmoi runs with the runner's authenticated gh (GITHUB_TOKEN).
          if ! github_release_attestation twpayne/chezmoi "v${chezmoi_version}" "${RUNNER_TEMP}/${artifact}"; then
            echo "chezmoi v${chezmoi_version}: the GitHub release attestation did not verify (gh 2.93.0 or newer, authenticated, is required)" >&2
            exit 1
          fi
          tar -xzf "${RUNNER_TEMP}/${artifact}" -C "${RUNNER_TEMP}" chezmoi
          sudo install -m 0755 "${RUNNER_TEMP}/chezmoi" /usr/local/bin/chezmoi

          files_test_chezmoi="$(command -v chezmoi)"
          case "${files_test_chezmoi}" in
            /*/mise/shims/*|"")
              echo "Files test chezmoi must resolve outside mise shims: ${files_test_chezmoi:-missing}" >&2
              exit 1
              ;;
            /*) ;;
            *)
              echo "Files test chezmoi must be an absolute path: ${files_test_chezmoi}" >&2
              exit 1
              ;;
          esac
          test -x "${files_test_chezmoi}"
          # A runner-provided chezmoi earlier on PATH must not shadow this release.
          "${files_test_chezmoi}" --version | grep -F "v${chezmoi_version}"
          printf 'FILES_TEST_CHEZMOI=%s\n' "${files_test_chezmoi}" >> "${GITHUB_ENV}"

          # Install coverage tooling as user gems and expose gem bin dir on PATH
          # before installation so RubyGems can expose executables immediately.
          # `--no-document` keeps CI faster and deterministic.
          gem_bin_dir="$(ruby -r rubygems -e 'puts Gem.user_dir')/bin"
          echo "${gem_bin_dir}" >> "${GITHUB_PATH}"
          export PATH="${gem_bin_dir}:${PATH}"
          gem install --user-install --no-document bashcov --version 3.3.0
          gem install --user-install --no-document simplecov-cobertura --version 3.1.0

      - name: Prepare statusline tool config
        if: ${{ needs.changes.outputs.should_test == 'true' }}
        run: |
          statusline_mise_dir="${RUNNER_TEMP}/statusline-mise"
          mkdir -p "${statusline_mise_dir}"
          cp home/dot_mise/config.toml "${statusline_mise_dir}/mise.toml"

      - name: Setup mise for statusline smoke
        if: ${{ needs.changes.outputs.should_test == 'true' }}
        uses: jdx/mise-action@c2a87611a18de5b3828c5652fe268e992400cb5c # v4
        with:
          # The newest mise at least 72 hours old, as hosts get it (minimum_release_age).
          minimum_release_age: 72h
          install: false
          cache: true

      - name: Install statusline tools
        if: ${{ needs.changes.outputs.should_test == 'true' }}
        run: |
          mise trust --yes "${RUNNER_TEMP}/statusline-mise/mise.toml"
          mise -C "${RUNNER_TEMP}/statusline-mise" install node
          # Every version comes from the copied config and its minimum_release_age (no literal here).
          mise -C "${RUNNER_TEMP}/statusline-mise" install npm:ccstatusline npm:ccusage
          mise -C "${RUNNER_TEMP}/statusline-mise" install ruff npm:prettier

      - name: Smoke-test statusline tools without network
        if: ${{ needs.changes.outputs.should_test == 'true' }}
        run: |
          set -euo pipefail

          statusline_mise_dir="${RUNNER_TEMP}/statusline-mise"
          ccstatusline_bin="$(mise -C "${statusline_mise_dir}" which ccstatusline)"
          ccusage_bin="$(mise -C "${statusline_mise_dir}" which ccusage)"
          # mise which answers through the "latest" symlink and mise where with the
          # mise which answers through the "latest" symlink and mise where with the
          # version directory, so both sides are compared as physical paths.
          ccstatusline_root="$(cd "$(mise -C "${statusline_mise_dir}" where npm:ccstatusline)" && pwd -P)"
          ccusage_root="$(cd "$(mise -C "${statusline_mise_dir}" where npm:ccusage)" && pwd -P)"
          ccstatusline_version="$(mise -C "${statusline_mise_dir}" current npm:ccstatusline)"
          ccusage_version="$(mise -C "${statusline_mise_dir}" current npm:ccusage)"
          # Run both tools on the node the copied config resolved. Without this, their
          # `#!/usr/bin/env node` falls through the mise shim to the image's
          # system node, which nothing has read yet: on the ubuntu-26.04 image
          # that cold first read of /usr/local/bin/node alone took 0.6 s to over
          # 5 s (fincore: 0 resident pages before the run), which tripped the
          # 5-second limit (T59).
          node_bin_dir="$(mise -C "${statusline_mise_dir}" where node)/bin"
          case "$(PATH="${node_bin_dir}:${PATH}" command -v node)" in
            "${node_bin_dir}/node") ;;
            *) echo "node did not resolve from mise's install" >&2; exit 1 ;;
          esac

          case "$(cd "$(dirname "${ccstatusline_bin}")" && pwd -P)/" in
            "${ccstatusline_root}"/*) ;;
            *) echo "ccstatusline did not resolve from mise's install" >&2; exit 1 ;;
          esac
          case "$(cd "$(dirname "${ccusage_bin}")" && pwd -P)/" in
            "${ccusage_root}"/*) ;;
            *) echo "ccusage did not resolve from mise's install" >&2; exit 1 ;;
          esac

          smoke_home="${RUNNER_TEMP}/statusline-smoke-home"
          mkdir -p "${smoke_home}"
          smoke=(
            /usr/bin/env
            "HOME=${smoke_home}"
            "PATH=${node_bin_dir}:${PATH}"
            "HTTP_PROXY=http://127.0.0.1:1"
            "HTTPS_PROXY=http://127.0.0.1:1"
            NO_PROXY=
            python3 scripts/check-statusline-tools.py
            --ccstatusline "${ccstatusline_bin}"
            --ccstatusline-version "${ccstatusline_version}"
            --ccusage "${ccusage_bin}"
            --ccusage-version "${ccusage_version}"
          )

          if [[ "${OS}" == ubuntu-* ]]; then
            sudo unshare --net -- sh -c 'test -z "$(ip route show)"'
            sudo unshare --net -- "${smoke[@]}"
          elif [ "${OS}" = "macos-14" ]; then
            sandbox_profile='(version 1)(allow default)(deny network*)'
            if /usr/bin/sandbox-exec -p "${sandbox_profile}" \
              python3 -c 'import socket; s = socket.socket(); s.bind(("127.0.0.1", 0))'; then
              echo "macOS network-denial oracle unexpectedly bound a socket" >&2
              exit 1
            fi
            /usr/bin/sandbox-exec -p "${sandbox_profile}" "${smoke[@]}"
          else
            echo "${OS} is not supported" >&2
            exit 1
          fi

      - name: Run `shfmt`
        if: ${{ needs.changes.outputs.should_test == 'true' }}
        run: |
          # shfmt is version-pinned via mise: brew/apt ship divergent versions
          # (3.14 changed heredoc-in-if formatting) and unpinned runners disagree.
          git ls-files -- ':(glob)install/**/*.sh' ':(glob)scripts/**/*.sh' | xargs mise x shfmt@3.14.1 -- shfmt -i 4 -sr -d

      - name: Check Python and Markdown formatting
        if: ${{ needs.changes.outputs.should_test == 'true' }}
        run: |
          # ruff and prettier come from home/dot_mise/config.toml (latest behind the cooldown).
          # mise -C resolves those versions and changes directory, so each check
          # returns to the repository, where ruff.toml and .prettierignore apply.
          # --config makes the root ruff.toml govern every file, so its
          # exclusions also cover vendor/compactiondb, which has its own pyproject.
          mise -C "${RUNNER_TEMP}/statusline-mise" x ruff -- \
            sh -c 'cd "${GITHUB_WORKSPACE}" && git ls-files -z "*.py" | xargs -0 ruff format --config ruff.toml --check'
          mise -C "${RUNNER_TEMP}/statusline-mise" x node npm:prettier -- \
            sh -c 'cd "${GITHUB_WORKSPACE}" && git ls-files -z "*.md" | xargs -0 prettier --check'

      - name: Run `ShellCheck`
        if: ${{ needs.changes.outputs.should_test == 'true' }}
        run: |
          git ls-files -z 'setup.sh' 'install/*.sh' 'install/**/*.sh' 'scripts/*.sh' | xargs -0 shellcheck -x

      - name: Setup uv
        if: ${{ needs.changes.outputs.should_test == 'true' }}
        uses: astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7 # v10.2.0
        with:
          enable-cache: false

      - name: Run Python unit tests
        if: ${{ needs.changes.outputs.should_test == 'true' }}
        run: |
          if [[ "${OS}" == ubuntu-* ]]; then
            sudo apt-get update && sudo apt-get install -y jq zsh
          elif [ "${OS}" == "macos-14" ]; then
            command -v jq > /dev/null 2>&1 || brew install jq
            command -v zsh > /dev/null 2>&1 || brew install zsh
          fi

          make unit-test

      - name: Prepare public dotfiles fixture
        if: ${{ needs.changes.outputs.should_test == 'true' }}
        run: |
          set -euo pipefail

          files_test_home="${RUNNER_TEMP}/dotfiles-files-${OS}-${SYSTEM}"
          files_test_source="${RUNNER_TEMP}/dotfiles-public-source-${OS}-${SYSTEM}"
          files_test_config="${files_test_home}/.config/chezmoi/chezmoi.yaml"
          if [ -e "${files_test_source}" ]; then
            echo "Fixture source already exists: ${files_test_source}" >&2
            exit 1
          fi
          cp -R "${GITHUB_WORKSPACE}/home" "${files_test_source}"
          rm -f "${files_test_source}/.chezmoiexternal.yaml.tmpl"
          rm -rf "${files_test_source}/.chezmoitemplates/chezmoiexternal.d"
          mkdir -p "${files_test_home}" "$(dirname "${files_test_config}")"
          printf 'sourceDir: "%s"\ndata:\n  email: "ci@example.invalid"\n  system: "%s"\n' \
            "${files_test_source}" "${SYSTEM}" > "${files_test_config}"

          # Remove external definitions only from the fixture copy, then apply
          # everything else so role-specific ignores determine both boundaries.
          # Regenerate the full config from its managed template first so
          # subsequent `chezmoi diff` output contains only target drift.
          CI=true HOME="${files_test_home}" "${FILES_TEST_CHEZMOI}" \
            --source "${files_test_source}" \
            --destination "${files_test_home}" \
            --config "${files_test_config}" \
            init
          HOME="${files_test_home}" "${FILES_TEST_CHEZMOI}" \
            --source "${files_test_source}" \
            --destination "${files_test_home}" \
            --config "${files_test_config}" \
            --refresh-externals=never \
            apply --exclude=scripts,externals
          {
            printf 'FILES_TEST_HOME=%s\n' "${files_test_home}"
            printf 'FILES_TEST_SOURCE=%s\n' "${files_test_source}"
            printf 'FILES_TEST_CONFIG=%s\n' "${files_test_config}"
          } >> "${GITHUB_ENV}"

      - name: Run unit test
        if: ${{ needs.changes.outputs.should_test == 'true' }}
        run: |
          if [ "${OS}" == "macos-14" ]; then
            # Bats uses its own tracing internals on macOS, and bashcov can
            # misread those records as coverage trace entries. Keep macOS in
            # the test matrix for platform validation, but collect Codecov
            # reports from the Ubuntu jobs where bashcov parses Bats output
            # reliably.
            ./scripts/run_unit_test.sh
            exit 0
          fi

          # Shared bashcov defaults:
          # - `--skip-uncovered`: limit report to executed files.
          # - `--root .`: normalize paths relative to repository root.
          bashcov_args=(--skip-uncovered --root .)

          # Use a unique command name per matrix job so SimpleCov keeps each
          # session separated before Codecov merges by flag/name.
          BASHCOV_COMMAND_NAME="unit-test-${OS}-${SYSTEM}" \
            ruby ./scripts/run_bashcov_unit_test.rb "${bashcov_args[@]}" -- ./scripts/run_unit_test.sh

      - name: Setup for Codecov
        if: ${{ needs.changes.outputs.should_test == 'true' && matrix.os == 'ubuntu-24.04' && !endsWith(github.actor, '[bot]') }}
        run: |
          # codecov-action uses these tools while preparing and uploading the
          # explicit Cobertura report in this repository setup.
          sudo apt-get install -y jq curl

      - name: Upload coverage to Codecov
        if: ${{ needs.changes.outputs.should_test == 'true' && matrix.os == 'ubuntu-24.04' && !endsWith(github.actor, '[bot]') }}
        uses: codecov/codecov-action@303a32d7a59b442fa8d48b6a1cc6825c09c847a5 # v7
        env:
          CODECOV_TOKEN: ${{ secrets.CODECOV_TOKEN }}
        with:
          files: ./coverage/coverage.xml
          # Upload only the explicit report file generated in this workflow.
          # This prevents unexpected auto-discovery from old/temporary files.
          disable_search: true
          env_vars: OS,SYSTEM
          fail_ci_if_error: false
          flags: ${{ env.CODECOV_FLAGS }}
          name: ${{ env.CODECOV_NAME }}
          # Avoid language auto-discovery warnings for gcov/coverage.py in this
          # shell-only workflow; upload the explicit Cobertura report only.
          plugins: noop
          # Use the PyPI-distributed CLI in CI to avoid non-actionable GPG trust
          # warnings emitted by the standalone binary signature verifier.
          use_pypi: true
          verbose: false

**Checking current UTC date and reviewing design sections**
exec
/bin/zsh -lc "nl -ba .orchestration/tasks/dotfiles-T128-regime-v3-a01.md | sed -n '94,145p'; nl -ba .orchestration/validation/dotfiles-T128-regime-v3-a01-research/codex-factsheet.md | sed -n '1,83p'; nl -ba .orchestration/validation/dotfiles-T128-regime-v3-a01-research/github-factsheet.md | sed -n '1,69p'; date -u +%Y-%m-%dT%H:%M:%SZ" in ~/Workspace/dotfiles
 succeeded in 88ms:
    94	# AGMSG-TASK dotfiles-T128-regime-v3-a01 — DESIGN: regime v3, the redesign after the 2026-10-10 halt
    95	
    96	Drafted 2026-10-11 (local) by the orchestrator seat `claude-deep-dot` under a recorded bootstrap exception (operator decision 2026-10-11: the orchestrator drafts, a fresh context on the review profile must accept before any implementing task is dispatched). Operator direction (pasted 2026-10-11): when substantive findings repeat, the design, implementation or verification is wrong and a mechanism must force the redo; prose alone repeats the mistake; the auditor must be able to find the orchestrator's and the worker's mistakes; efficiency, quality and cost are optimised together; the auditor must not become the bottleneck and the audit stages must be chosen; all of it grounded in the tools' official documentation and current practice. Research inputs: fact sheets on Claude Code 2.1.293, Codex CLI 0.161.0, GitHub rulesets and Actions, and the research literature, read 2026-10-11; the measured baseline below.
    97	
    98	## 1. Finding: the fix program tripped its own rule
    99	
   100	By T126 INV-6 as written: wave 1 (PR #313) 8 amendments (limit 4) and 2 revises (limit 2); wave 3b (PR #314) Bot P1 on two post-RESULT heads. The orchestrator was drafting a waiver for #313. T120 was reset only on the operator's question. The regime is therefore reset here by its own rule; this document is the redesign, and T126 and T124 are superseded (their accepted ideas are kept where named).
   101	
   102	Measured baseline (history + GitHub):
   103	
   104	| task | PR | files | +lines | amendments | questions | revises | audits (incorrect) | Bot threads (heads) | P0/P1 | wall |
   105	|---|---|---|---|---|---|---|---|---|---|---|
   106	| T114 | - | - | - | 0 | 0 | 6 | 3 (3) | - | - | 21.5h |
   107	| T118 | 310 | 35 | 881 | 7 | 0 | 20 | 8 (7) | 16 (7) | 0 | 10.6h |
   108	| T119 | 312 | 37 | 3191 | 8 | 8 | 5 | 4 (4) | 25 (11) | 7 | 11.1h |
   109	| T120 | 315 | 19 | 1489 | 8 | 1 | 0 | 0 | 15 (5) | 8 | reset |
   110	| T124 W1 | 313 | 20 | 2642 | 8 | 6 | 2 | 0 | 52 (10) | 31 | halted, reset |
   111	| T124 W3b | 314 | 9 | 1462 | 5 | 0 | 0 | 0 | 24 (4) | 2 | halted, reset |
   112	
   113	Every acceptance record to date says `cost: n/a`.
   114	
   115	## 2. Root causes, each with its evidence
   116	
   117	R1 to R8 in the front matter. The literature behind R1: intrinsic self-correction without an external signal degrades after the first round (Huang et al. 2023); a second review round on the same artifact raised recall slightly and false positives by 62% (arXiv 2603.16244); multi-round review degrades with rounds (MCR-Bench); revising an already-correct state loses correct work unless verifier evidence is bound to the exact code state (arXiv 2607.24604). Behind R3: Google's review study (median change 24 lines, ~90% under 10 files) and its CL-size guidance. Behind R5 and R6: a judge without a reference is lenient and a reference flips 9-85% of verdicts toward correct (2607.12885); format-restricted generation degrades reasoning, so verdicts reason first and then fill the schema (2408.02442); Anthropic's harness-design post: a standalone skeptical evaluator is tractable where a self-critical generator is not, and the evaluator is worth its cost only where the task exceeds the model's reliable solo capability, which is what the tier table encodes.
   118	
   119	## 3. Principles (each names what it reuses and what it deletes)
   120	
   121	- **P1 One deterministic fact per round (INV-3).** Reuses tests/unit, CI, `pr-feedback.py`. Deletes free-form revise rounds and the audit-per-round habit.
   122	- **P2 Declarative over imperative at trust boundaries (INV-1, INV-5, INV-7).** Reuses `jsonschema`, PyYAML, `codex exec --output-schema`, `claude -p --json-schema`. Deletes the bespoke YAML parser, the glob NFA, the prose verdict grammar, regex parsing of `.last.md`, and the T126 "process_tiers.json next to the module" indirection (the validator reads the manifest with PyYAML).
   123	- **P3 Small one-invariant PRs enforced in CI (INV-2).** Reuses GitHub required checks and the strict up-to-date ruleset already in force. Deletes waves declared inside a task file.
   124	- **P4 Main-pinned mechanical checks in CI; host gate only for history-anchored rules (INV-1, INV-2, INV-8 in CI; INV-3, INV-5 record, INV-6, INV-7 anchor, INV-11 on the host).** Reuses `pull_request_target`, the `changes` job pattern that reports success for an `.orchestration`-only diff. Deletes PR #313's `REVIEW_TREE` idea (never on `main`) and the copy step of untracked evidence into the gate's cwd. The host gate `make require-crit-review` keeps its evidence rules and changes three of them in named waves: the audit verdict and categories come from the schema JSON with the `AGMSG-AUDIT` record and the category lock (V2b), the reset backstop and the Bot-head count (V3a), the history-anchored design review (V4); it continues to run from the orchestrator's main checkout.
   125	- **P5 Research before dispatch; a question ends the task, not amends it (INV-4).** Reuses history (`amendment=`, `status=question`). Deletes the amendment-per-question practice. The task file's `premises` block is the mechanical residue of "verify every CLI constraint by running the real command".
   126	- **P6 Reset is mechanical, loop-time, and released only by another context or the operator (INV-6).** Reuses `scripts/require-crit-review.py` as the mandatory point, `agent-stop-gate.sh` and the Codex `[hooks].Stop` as the early signal (both soft by their documented caps: Claude's 8-continuation cap, Codex's continuation prompt), `check-regime-boundary.sh` for the re-dispatch detector. Deletes the orchestrator-written redesign (the redesign author is a `review`-profile seat or a fresh headless context; the `redesign` profile of T124 v4 is dropped: `review` is the same model and effort as `deep`, so independence of context is the whole lever, and T124 round 1 showed it works).
   127	- **P7 Audit staging by tier; the auditor never serializes the pipeline (INV-5, process_tiers).** See section 4.
   128	- **P8 Cost measured, budgets per tier (INV-9).** Reuses the JSON cost fields the runtimes already emit and the session transcripts. Deletes `cost: n/a`.
   129	- **P9 Parallelism with disjoint files and early push (INV-10).** Reuses `herdr-agents --add-worker`, draft PRs.
   130	- **P10 Routing stays by boundary.** Claude-boundary sources to a Codex seat, Codex-boundary to a Claude seat, permgate and shared gate sources to the operator, as the agmsg-orchestration skill's step 3 states; nothing here changes that.
   131	
   132	## 4. Audit stages (process_tiers; the one table the validator reads)
   133	
   134	| stage | who | when | tier docs | tier review | tier design | cost |
   135	|---|---|---|---|---|---|---|
   136	| 0 design review | a fresh Claude context on the review profile and a Codex read-only review of the same hash, schema receipts (INV-7) | before any code | - | - | required | minutes |
   137	| 1 worker checks | worker in its sandbox: invariant tests first, shellcheck, unit tests | before every push | required | required | required | none for the regime |
   138	| 2 CI + Bot | main-pinned `regime` check (schema, caps, evidence shape) + unit tests + Codex Bot | every push, in parallel | required | required | required | none |
   139	| 3 schema audit | headless read-only `codex exec --output-schema`, pooled 2, started by `make audit-head` once CI is green and the Bot reviewed or 15 min passed, once per RESULT head, reused for an evidence-only head by tree equality (INV-5) | per RESULT head | - | required | required, with invariant map and permgate window | the scarce resource, now off the critical path |
   140	| 4 acceptance | orchestrator: sweep, dispositions, record, host gate, merge `--match-head-commit` | per RESULT | required | required | required | minutes |
   141	
   142	Tier derivation: docs = prose-only `allowed_files` outside the regime's own rule prose (`home/dot_config/claude/rules/**`, the agmsg-orchestration SKILL, `AGENTS.md`, README), which is review tier by explicit list; review = the existing review-tier paths (scripts, hooks, tests, templates); design = the explicit design-tier list from T124 INV-2 v3 (install/**, setup.sh, the gate scripts, `executable_herdr-agents`, `executable_permgate`, Codex and Claude policy, sandbox and permission settings, credential helpers). Round limits: docs 1 revise; review and design 2 revises then reset. Profiles: worker `standard` (docs `express`), review `review`, audit `audit`.
   143	
   144	Why stage 3 is not the queue: the orchestrator starts it with `make audit-head` when the RESULT arrives (the wait on CI and the Bot is inside the target), it runs concurrently (pool of two, each in its own detached worktree), once per head, and an evidence-only head reuses the earlier audit by tree equality; the measured cost of the old serial form was 1.3 h of 11.1 h, so the throughput levers are P1 and P6, and the pool removes the residual queue.
   145	
     1	# Codex CLI 0.161.0 fact sheet (2026-10-11)
     2	
     3	Source tags: `DOC` = official docs (every `developers.openai.com/codex/*` URL now 308-redirects to `learn.chatgpt.com/docs/*`; final URL cited). `SRC` = `github.com/openai/codex` at tag `rust-v0.161.0`. `CLI` = installed `codex-cli 0.161.0 --help` output (clap only, no model call). `LOCAL` = observed on this machine's `~/.codex`, not official. Third-party claims surfaced by search were dropped.
     4	
     5	DOC short names → `https://learn.chatgpt.com` + : non-interactive-mode=/docs/non-interactive-mode; developer-commands=/docs/developer-commands?surface=cli; config-reference=/docs/config-file/config-reference; config-advanced=/docs/config-file/config-advanced; agent-approvals-security=/docs/agent-approvals-security; permissions=/docs/permissions; hooks=/docs/hooks; rules=/docs/agent-configuration/rules; subagents.md=/docs/agent-configuration/subagents.md; agents-md.md=/docs/agent-configuration/agents-md.md; third-party/github.md=/docs/third-party/github.md; pricing.md=/docs/pricing.md; models.md=/docs/models.md; cloud=/docs/cloud; codex/cli.md=/docs/codex/cli.md; github-code-reviews=/use-cases/github-code-reviews.
     6	
     7	## 1. `codex exec`
     8	
     9	- Default sandbox is read-only: "By default, `codex exec` runs in a read-only sandbox." Progress streams to stderr; only the final agent message goes to stdout. DOC — https://learn.chatgpt.com/docs/non-interactive-mode
    10	- Flags present in 0.161.0 `codex exec --help`: `-c key=value` (value parsed as TOML, dotted paths), `--enable/--disable <feature>`, `--strict-config`, `-m/--model`, `-p/--profile` (layers `$CODEX_HOME/<name>.config.toml`), `-s/--sandbox read-only|workspace-write|danger-full-access`, `--approve-for-me` ("Route approval requests through automatic review using the workspace-write sandbox"), `--dangerously-bypass-approvals-and-sandbox`, `--dangerously-bypass-hook-trust`, `-C/--cd`, `--worktree` ("Run the session in a new managed Git worktree"), `--add-dir`, `--skip-git-repo-check`, `--ephemeral`, `--ignore-user-config`, `--ignore-rules`, `--output-schema <FILE>`, `--json`, `-o/--output-last-message <FILE>`. Subcommands: `resume`, `fork`, `review`. CLI
    11	- `--full-auto`: docs say it is a "deprecated compatibility flag and prints a warning" (DOC — non-interactive-mode page); installed 0.161.0 rejects it: `error: unexpected argument '--full-auto' found`. CLI. SRC `codex-rs/exec/src/lib.rs` has no `full_auto` handling.
    12	- `-a/--ask-for-approval` exists only on top-level `codex` (`on-request | never`); `codex exec -a never` fails with `unexpected argument '-a'`. Set exec approval policy via `-c approval_policy=...`. CLI; the docs' exec flag table also omits it. DOC — https://learn.chatgpt.com/docs/developer-commands?surface=cli
    13	- Headless default: `approval_policy: Some(AskForApproval::Never)` ("Default to never ask for approvals in headless mode"; dropped when the resolved reviewer is AutoReview). SRC — https://raw.githubusercontent.com/openai/codex/rust-v0.161.0/codex-rs/exec/src/lib.rs
    14	- Git check: "Codex requires commands to run inside a Git repository to prevent destructive changes"; override with `--skip-git-repo-check`. DOC — non-interactive-mode. SRC: check is `get_git_repo_root(&default_cwd).is_none()` → prints `Not inside a trusted directory and --skip-git-repo-check was not specified.` and exits 1; also skipped when `--dangerously-bypass-approvals-and-sandbox` is set. Whether a worktree's `.git` _file_ satisfies `get_git_repo_root`: UNVERIFIED (git_info.rs not located at the tag; circumstantial: `codex exec --worktree` exists (CLI) and LOCAL worktree runs succeed).
    15	- JSONL (`--json`): event types `thread.started`, `turn.started`, `turn.completed`, `turn.failed`, `item.*` (`item.started`, `item.completed`), `error`; item types: agent messages, reasoning, command executions, file changes, MCP tool calls, web searches, plan updates. `turn.completed` carries `usage` with `input_tokens`, `cached_input_tokens`, `output_tokens`, `reasoning_output_tokens`. No cost field is documented. DOC — https://learn.chatgpt.com/docs/non-interactive-mode
    16	- `-o` writes the final message to a file "and still prints it to stdout"; docs recommend pairing `--json` with `--output-last-message` in CI. DOC — non-interactive-mode; developer-commands.
    17	- `--output-schema`: docs wording is "request a final response that conforms to a JSON Schema" (DOC — non-interactive-mode) and "Codex validates tool output against it" (DOC — developer-commands). SRC: exec only parses the file as JSON (`Failed to read output schema file`, `... is not valid JSON` → exit 1) and sends it as `output_schema` in `TurnStartParams`; core builds Responses `text.format = {type: json_schema, name: "codex_output_schema", strict: output_schema_strict, schema}` (SRC — `codex-rs/codex-api/src/common.rs`), with `Prompt::default().output_schema_strict = true` ("Whether the Responses API should strictly validate `output_schema`", SRC — `codex-rs/core/src/client_common.rs`). So enforcement is server-side strict JSON schema, no local post-validation; whether core ever overrides `strict` to false for incompatible schemas: UNVERIFIED. The `review` path does not use `output_schema`. SRC — exec/src/lib.rs
    18	- Exit codes: no documented table (DOC — developer-commands documents exit codes only for `apply`, `cloud`, `login status`). SRC: exits 1 on config/startup errors, and after the run `if error_seen { std::process::exit(1) }` where `error_seen` is set by a non-retried `Error` notification, a `TurnCompleted` with status `Failed`/`Interrupted`, or a failed server-request response; otherwise 0. SRC — exec/src/lib.rs. An enabled MCP server with `required = true` that fails to start makes exec "exit with an error". DOC — non-interactive-mode
    19	- `resume`: `codex exec resume --last "<prompt>"` or `codex exec resume <SESSION_ID|thread name> [PROMPT]`; `--all` disables cwd filtering. DOC — non-interactive-mode; CLI
    20	- `--ephemeral`: "Run without persisting session files to disk." CLI; DOC — non-interactive-mode
    21	- Auth: reuses CLI login; `CODEX_API_KEY` works for a single run (also for `codex review`); docs warn against job-level API keys in workflows running repo-controlled code, and against ChatGPT `auth.json` in public repos. DOC — non-interactive-mode
    22	
    23	## 2. `codex review`
    24	
    25	- Top-level `codex review [PROMPT]` flags: `--uncommitted` ("staged, unstaged, and untracked"), `--base <BRANCH>`, `--commit <SHA>`, `--title` (requires `--commit`), `-c`, `--enable/--disable`, `--strict-config`. No `-m`, `--json`, `-o`, `--output-schema`, `--sandbox`. CLI; DOC — developer-commands. `--uncommitted`, `--base`, `--commit` and a custom PROMPT "conflict with one another". DOC — developer-commands
    26	- `codex exec review [PROMPT]` additionally accepts `-m`, `--json`, `-o`, `--output-schema`, `--worktree`, `--ephemeral`, `--skip-git-repo-check`, `--ignore-rules`, `--dangerously-bypass-*`. CLI (not in the docs table). `--output-schema` is ignored on the review path (SRC — exec/src/lib.rs). Whether `--json` emits findings as a structured item: UNVERIFIED (not run; would consume quota).
    27	- Output: "Codex reports prioritized findings without modifying your working tree." DOC — https://learn.chatgpt.com/docs/codex/cli.md. Internal structure: `ReviewOutputEvent { findings: Vec<ReviewFinding>, overall_correctness: String, overall_explanation: String, overall_confidence_score: f32 }`, `ReviewFinding { title, body, confidence_score: f32, priority: i32, code_location: { absolute_file_path, line_range { start, end } } }`. SRC — https://raw.githubusercontent.com/openai/codex/rust-v0.161.0/codex-rs/protocol/src/protocol.rs. The P0–P3 definitions come from a server-side review prompt: UNVERIFIED (not in the binary strings or repo at this tag).
    28	- `review_model`: "Optional model override used by `/review` (defaults to the current session model)." DOC — https://learn.chatgpt.com/docs/config-file/config-reference. Applicability to `codex review` CLI: UNVERIFIED.
    29	- `approvals_reviewer = user | auto_review`: "Who reviews eligible approval prompts under `on-request` or granular approval policies"; default `user`; `auto_review` uses a reviewer subagent, does not change sandboxing, "Prompt-build, review-session, and parse failures fail closed", critical-risk actions denied, uses extra model calls. DOC — config-reference; https://learn.chatgpt.com/docs/agent-approvals-security. `--approve-for-me` is the CLI switch (CLI only; not in docs).
    30	
    31	## 3. `config.toml`
    32	
    33	- `approval_policy`: `on-request | never | { granular = { sandbox_approval, rules, mcp_elicitations, request_permissions, skill_approval } }`. "`untrusted` is unsupported" and "can prevent startup"; `on-failure` deprecated ("use `on-request` for interactive runs and `never` for non-interactive runs"). DOC — config-reference; agent-approvals-security
    34	- `sandbox_mode`: `read-only | workspace-write | danger-full-access`. `[sandbox_workspace_write]`: `network_access` ("Allow outbound network access inside the workspace-write sandbox"), `writable_roots` ("Additional writable roots"), `exclude_tmpdir_env_var` (exclude `$TMPDIR`), `exclude_slash_tmp` (exclude `/tmp`). Must not be combined with `default_permissions`/`[permissions]`. DOC — config-reference; https://learn.chatgpt.com/docs/permissions
    35	- `notify = ["cmd", ...]`: invoked "whenever Codex emits supported events (currently only `agent-turn-complete`)"; single JSON argument with `type`, `thread-id`, `turn-id`, `cwd`, `input-messages`, `last-assistant-message`. DOC — https://learn.chatgpt.com/docs/config-file/config-advanced
    36	- `model_reasoning_effort`: "such as `low`, `medium`, `high`, `xhigh`, `max`, or `ultra`"; levels "depend on the model and client"; `plan_mode_reasoning_effort` override. DOC — config-reference
    37	- `[features]`: `hooks` ("Enable lifecycle hooks loaded from `hooks.json` or inline `[hooks]`"; `codex_hooks` deprecated alias), `multi_agent` (on by default), `network_proxy`, `web_search`, etc. DOC — config-reference. Installed: `hooks stable true`, `multi_agent stable true`, `multi_agent_v2 stable false`, `network_proxy experimental false`. CLI (`codex features list`)
    38	- `[hooks]`: events `PreToolUse`, `PermissionRequest`, `PostToolUse`, `PreCompact`, `PostCompact`, `SessionStart`, `SessionEnd`, `SubagentStart`, `SubagentStop`, `UserPromptSubmit`, `Stop`, `Interrupt`. Handler types `command`, `mcp_tool` (`prompt`/`agent` parsed but skipped); `timeout` seconds (default 600; `SessionEnd`/`Interrupt` default 1, max 3); `async` (background, cannot block); `additionalContextLimit` default 2500. Sources: `~/.codex/hooks.json`, `~/.codex/config.toml`, `<repo>/.codex/hooks.json`, `<repo>/.codex/config.toml` (project hooks only when the project `.codex/` layer is trusted), plugins, managed `requirements.toml`. Non-managed hooks "must be reviewed and trusted"; trust is per hash, "new or changed hooks are marked for review and skipped until trusted"; `--dangerously-bypass-hook-trust` skips that for one invocation. DOC — https://learn.chatgpt.com/docs/hooks
    39	- Hook input: common `session_id`, `transcript_path`, `cwd`, `hook_event_name`, `model`, `permission_mode`; `PreToolUse`/`PostToolUse`: `turn_id`, `tool_name` (`Bash`, `apply_patch` with `Edit`/`Write` aliases, MCP names), `tool_use_id`, `tool_input` (`tool_input.command` for Bash), `tool_response`; `PermissionRequest`: `tool_name`, `tool_input(.description)`; `Stop`/`SubagentStop`: `stop_hook_active`, `last_assistant_message` (+ `agent_id`, `agent_type`, `agent_transcript_path`); `UserPromptSubmit`: `prompt`; `SessionStart`: `source` (`startup|resume|clear|compact`); `SessionEnd`: `reason`. DOC — hooks
    40	- Hook semantics: exit 0 no output = continue; exit 2 + stderr reason blocks for `PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `SubagentStop`, `Stop`. `PreToolUse`: `hookSpecificOutput.permissionDecision: "deny"|"allow"` (+`updatedInput`); `"ask"` unsupported (hook fails, tool call continues). `PermissionRequest`: `hookSpecificOutput.decision.behavior: "allow"|"deny"`, "any `deny` wins", no decision → normal prompt. `Stop`: `decision: "block"` "doesn't reject the turn" but injects a continuation prompt; `continue: false` wins. `SessionEnd` advisory only. `Interrupt` cannot be prevented. DOC — hooks. Whether hooks fire under `codex exec`: UNVERIFIED (docs silent; the only evidence is that `codex exec` exposes `--dangerously-bypass-hook-trust`).
    41	- `[agents]`: `enabled` (default true), `max_concurrent_threads_per_session` (`max_threads` legacy alias; default not documented), `default_subagent_model`, `default_subagent_reasoning_effort`, `interrupt_message`; roles as `agents.<name>` with `config_file`/`description` (DOC — config-reference) or standalone TOML in `~/.codex/agents/`/`.codex/agents/` with `name`, `description`, `developer_instructions`, optional `sandbox_mode` (DOC — https://learn.chatgpt.com/docs/agent-configuration/subagents.md). `max_depth`: UNVERIFIED (not in either page).
    42	- Profiles: `$CODEX_HOME/<name>.config.toml` layered by `--profile`; "In Codex 0.134.0 and later, `--profile` no longer reads `[profiles.profile-name]`"; project `.codex/config.toml` cannot set `profile`. DOC — config-advanced; config-reference
    43	- Rules: `rules/*.rules` next to each active config layer (`~/.codex/rules/default.rules`; `<repo>/.codex/rules/` only when trusted); Starlark `prefix_rule(pattern=[...], decision="allow"|"prompt"|"forbidden", justification, match, not_match)`; strictest wins; `allow` runs the command outside the sandbox without prompting; test with `codex execpolicy check --pretty --rules <file> -- <cmd>`. DOC — https://learn.chatgpt.com/docs/agent-configuration/rules. `--ignore-rules` skips user and project rules. CLI
    44	- `project_doc_max_bytes`: "Maximum bytes read from `AGENTS.md`", default 32 KiB; discovery `~/.codex/AGENTS.override.md|AGENTS.md`, then project root down to cwd, one file per directory, concatenated root-first, nearer files later. DOC — https://learn.chatgpt.com/docs/agent-configuration/agents-md.md
    45	- `shell_environment_policy`: `inherit = all|core|none`, `filters` (include/exclude patterns), `set`, `ignore_default_excludes` ("Keep variables containing KEY, SECRET, or TOKEN before other filters run (default: true)"), `experimental_use_profile`. DOC — config-reference
    46	- `projects.<path>.trust_level = "trusted"|"untrusted"`; "Untrusted projects skip project-scoped `.codex/` layers, including project-local config, hooks, and rules." DOC — config-reference
    47	- `history.persistence = save-all|none`, `history.max_bytes`; `log_dir` (default `$CODEX_HOME/log`); `sqlite_home`. DOC — config-reference
    48	
    49	## 4. GitHub "Codex" review bot
    50	
    51	- Triggers: `@codex review` comment (Codex reacts 👀 then posts a review); `@codex review for <focus>`; `@codex security review`; Automatic review per repository ("Review code" setting, needs GitHub push/admin) and per user ("Personal preferences", "Choose timing with Review trigger" — options not enumerated). Any other `@codex ...` (e.g. `@codex fix the P1 issue`) "starts a legacy cloud chat with the pull request as context"; Codex "can push a fix back to the branch when it has permission". DOC — https://learn.chatgpt.com/docs/third-party/github.md
    52	- Output: "a standard GitHub code review focused on serious issues"; "In GitHub, Codex flags only P0 and P1 issues"; the example shows a `[P1]` label on a line-anchored comment. Inline vs summary layout and P2/P3 handling: not documented. DOC — third-party/github.md
    53	- `AGENTS.md`: Codex "searches your repository for `AGENTS.md` files and follows the applicable code review rules"; put a `## Code Review Rules` section (`###` groups) in the file closest to the governed code; root = repo-wide, nested = service-specific; "applies the root and more-specific guidance that covers each changed file"; keep lint/format to CI. DOC — third-party/github.md; https://learn.chatgpt.com/use-cases/github-code-reviews
    54	- Quota: "Code Review usage applies only when Codex runs reviews through GitHub. Reviews run locally or outside of GitHub count toward your general usage limits." DOC — https://learn.chatgpt.com/docs/pricing.md. Numeric review quotas: UNVERIFIED.
    55	- Re-review on every push, hidden-directory (`.orchestration/`) coverage, draft PRs, and requesting a review of a specific commit: UNVERIFIED (not in any official page; only GitLab documents "On every push").
    56	
    57	## 5. Session logs and usage
    58	
    59	- State root: `CODEX_HOME` (default `~/.codex`); `history.jsonl` when persistence enabled; logs under `log_dir` (default `$CODEX_HOME/log`). DOC — config-advanced; config-reference. `--ephemeral` skips "session rollout files". DOC — non-interactive-mode
    60	- No official page names `~/.codex/sessions` (hooks input `transcript_path` is the only official acknowledgment of a per-session transcript file, DOC — hooks). LOCAL: rollouts live at `~/.codex/sessions/YYYY/MM/DD/rollout-<ts>-<uuid>.jsonl` plus `session_index.jsonl` and `logs_2.sqlite`/`state_5.sqlite`; `codex migrate-rollouts` "migrate[s] legacy local sessions to paginated thread history" (CLI), i.e. the on-disk format is in transition (`ThreadHistoryMode legacy|paginated` strings in the binary).
    61	- Per-turn usage is recorded: LOCAL rollout lines `event_msg`/`token_count` carry `info.total_token_usage` and `info.last_token_usage` (`input_tokens`, `cached_input_tokens`, `cache_write_input_tokens`, `output_tokens`, `reasoning_output_tokens`, `total_tokens`), `model_context_window`, and `rate_limits` (`primary.used_percent`, `window_minutes` (10080 observed), `resets_at`, `credits.balance`, `plan_type`). Field names match SRC `TokenCountEvent { info: Option<TokenUsageInfo>, rate_limits: Option<RateLimitSnapshot> }`, `RateLimitWindow { used_percent, window_minutes, resets_at }`. SRC — protocol.rs
    62	- From a finished `codex exec --json` run, read `turn.completed.usage` (tokens only; no cost, no rate-limit snapshot documented). DOC — non-interactive-mode. In the TUI, `/status` and `/usage` show limits and token activity. DOC — developer-commands
    63	
    64	## 6. Sandbox
    65	
    66	- macOS "uses Seatbelt policies and runs commands using `sandbox-exec`"; "Linux uses `bwrap` plus `seccomp` by default" (Landlock not mentioned; moved to bwrap in 0.115; WSL1 unsupported); Windows MXC. If the platform sandbox cannot enforce the policy, Codex "refuses to run the command instead of silently running it unsandboxed". DOC — agent-approvals-security; permissions
    67	- workspace-write: "Defaults include no network access and write permissions limited to the active workspace"; workspace = cwd plus "temporary directories like `/tmp`" (`$TMPDIR` via `:tmpdir` in permissions profiles); network only with `[sandbox_workspace_write] network_access = true`. DOC — agent-approvals-security; permissions. Network in read-only mode: UNVERIFIED (docs state only that network is off by default and `:read-only` "keeps local command execution read-only").
    68	- Protected paths inside writable roots: "`<writable_root>/.git` is protected as read-only whether it appears as a directory or file"; for a `gitdir:` pointer file "the resolved directory is also protected"; `.codex` and `.agents` directories likewise; "Protection is recursive". DOC — agent-approvals-security. So in workspace-write, neither a worktree's `.git` file nor its resolved per-worktree gitdir is writable; whether the shared _common_ dir (`commondir`) is also protected: UNVERIFIED.
    69	- `danger-full-access`: no sandbox, no approvals; `--dangerously-bypass-approvals-and-sandbox` (`--yolo`) also skips the git check. DOC — agent-approvals-security; SRC — exec/src/lib.rs
    70	- Worktrees: `--worktree` on `codex exec`/`review` runs "in a new managed Git worktree" (CLI); `codex exec` in an existing worktree directory needing `--skip-git-repo-check`: UNVERIFIED.
    71	
    72	## 7. Rate limits, cost, effort
    73	
    74	- ChatGPT sign-in: usage draws on the plan's allowance; Plus $20, Pro $100/$200/$500; "Pro plans currently have no five-hour limit"; Plus/Standard Business message estimates are "per five-hour period" and "Weekly limits may also apply"; Plus/Pro can buy credits. API key: "Pay for Codex usage based on API pricing"; models "follow the API models available to your key". DOC — https://learn.chatgpt.com/docs/pricing.md
    75	- Credit rates per 1M tokens (input/cached/output): GPT-6 Astra 250/25/1,250; GPT-6.1 Sol 50/2.5/250; GPT-6 Luna 2.5/0.25/12.5; Fast 2.5x, Ultrafast 8x of included usage. DOC — pricing.md
    76	- `help.openai.com/en/articles/11369540` could not be fetched (JS wall/403): help-center specifics UNVERIFIED.
    77	- Effort: config names `low|medium|high|xhigh|max|ultra`; models page calls them Light/Medium/High/Extra High/Max/Ultra; "Higher reasoning effort can improve results for complex tasks, but it takes longer and uses more tokens"; "Most tasks do not need Max or Ultra"; Ultra "uses subagents"; Luna supports up to Max; some paid plans omit Extra High on Astra. No quantitative xhigh cost/latency guidance exists. DOC — https://learn.chatgpt.com/docs/models.md
    78	
    79	## 8. Multi-agent guidance
    80	
    81	- Subagents are on by default; orchestration (spawn, route follow-ups, wait, close) is handled by Codex; "Subagents inherit your current sandbox policy"; a custom agent file may set `sandbox_mode`; in the CLI the parent's live overrides (`/permissions`, `--yolo`) are reapplied to children; "In non-interactive flows ... an action that needs new approval fails and Codex surfaces the error back to the parent workflow"; subagent runs "consume more tokens"; recommended for read-heavy parallel work, caution for parallel writes. DOC — https://learn.chatgpt.com/docs/agent-configuration/subagents.md
    82	- Collaboration tools listed under `features.multi_agent`: `spawn_agent`, `send_input`, `resume_agent`, `wait_agent`, `close_agent`. DOC — config-reference
    83	- Codex Cloud: "Each task has its own workspace and can keep working while your computer is asleep"; tasks start from a published environment; `codex cloud exec --env --attempts 1–4`, `codex cloud list --json`; "Cloud tasks may use more of your allowance than local messages". DOC — https://learn.chatgpt.com/docs/cloud; developer-commands; pricing.md
     1	# GitHub merge-gate mechanics for a user-owned repo (facts as of 2026-10-11)
     2	
     3	Sources: docs.github.com, cli.github.com/manual, github.blog changelog, docs.coderabbit.ai, learn.chatgpt.com (redirect target of developers.openai.com/codex). "UNVERIFIED" = no fetched official page states it.
     4	
     5	## 1. Rulesets on a personal repository
     6	
     7	- Repo-level ruleset rules: require PR; required approvals; dismiss stale approvals; code-owner review; "Require approval of the most recent reviewable push"; conversation resolution; merge method; required status checks (strict/loose, app source); require deployments; code scanning; code quality; signed commits; linear history; restrict creations/updates/deletions; block force pushes; file path/size/extension limits. — https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets
     8	- Only rule explicitly denied to user-owned repos: team-based required reviewers — "This rule is not available on user-owned repositories as they do not contain teams." — same URL.
     9	- "Require merge queue" and "Require deployments to succeed" are repo-level rules: "This rule is not available for rulesets created at the organization level." (restriction on org-level, not on user-owned). — https://docs.github.com/en/enterprise-cloud@latest/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets
    10	- Required workflows: "Ruleset workflows can be configured at the organization or enterprise level"; supported events `pull_request`, `pull_request_target`, `merge_group`, "Any filters you specify for the supported events are ignored"; "Applying this rule will block direct pushes." — same enterprise-cloud URL. Changelog: requiring a workflow "will only be available on GitHub Enterprise plans via Repository Rules"; old Actions Required Workflows removed "On October 18th" (2023). — https://github.blog/changelog/2023-08-02-github-actions-required-workflows-will-move-to-repository-rules/ . No page mentions user-owned repos (explicit denial UNVERIFIED).
    11	- Merge queue availability: "Merge queue is available on private and public repos on the GitHub Enterprise Cloud plan" and "all public repos owned by organizations". No page mentions user-owned repos. — https://github.blog/changelog/2023-07-12-pull-request-merge-queue-is-now-generally-available/
    12	- Ruleset plan gating for a private personal repo: UNVERIFIED. Plans page lists "Protected branches", "Code owners", "Required pull request reviewers" under Pro "in private repositories"; Free lists only "Deployment protection rules for public repositories". — https://docs.github.com/en/get-started/learning-about-github/githubs-plans
    13	- Bypass actors: "Repository admins, organization owners, and enterprise owners", maintain/write roles, teams, GitHub Apps, Dependabot; modes "Always allow" / "For pull requests only". — https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository . REST `bypass_actors[].actor_type`: Integration, OrganizationAdmin, RepositoryRole, Team, DeployKey, User; `bypass_mode`: always, pull_request, exempt. — https://docs.github.com/en/rest/repos/rules
    14	- Tamper ceiling: repo admins edit repo rulesets; only org-level rulesets are locked ("only owners of the organization can edit the ruleset"). — https://docs.github.com/en/organizations/managing-organization-settings/creating-rulesets-for-repositories-in-your-organization
    15	- Self-approval: "Pull request authors cannot approve their own pull requests." — https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/approving-a-pull-request-with-required-reviews . Personal-account default: "workflows are not allowed to create or approve pull requests." — https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository . Copilot default review is "Comment"; approvals are public preview, "off by default". — https://docs.github.com/en/copilot/how-tos/use-copilot-agents/request-a-code-review/use-code-review . Consequence: with one write account, approval count >= 1, code-owner review and last-push approval are unsatisfiable without bypass.
    16	- Code owners "must have write permissions for the repository". — https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
    17	- Signed commits: unsigned head commits can block even a signed squash; linear history needs squash/rebase enabled; block force pushes and restrict deletions are on by default. — available-rules URL above.
    18	
    19	## 2. Trust model of status checks
    20	
    21	- `pull_request_target` "runs in the context of the default branch of the base repository, rather than in the context of the merge commit"; "This prevents execution of unsafe code from the head of the pull request that could alter your repository"; "Running untrusted code on the `pull_request_target` trigger may lead to security vulnerabilities." `pull_request`: `GITHUB_SHA` "is the last merge commit of the pull request merge branch" (that `pull_request` runs the PR-side workflow file is an inference from these contrasting statements plus the fork-approval page; no page states it directly). — https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows
    22	- Fork PR approval doc: review proposed changes "especially to `.github/workflows/`" before approving a run. — https://docs.github.com/en/actions/managing-workflow-runs-and-deployments/managing-workflow-runs/approving-workflow-runs-from-public-forks
    23	- `pull_request_target`/`workflow_run` "may have repository write access and access to referenced secrets"; they "must not explicitly check out untrusted code, including from pull request forks". "Pinning an action to a full-length commit SHA is currently the only way to use an action as an immutable release." Add the workflows dir to CODEOWNERS so changes "will first require approval". — https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions
    24	- `workflow_run`: "This event will only trigger a workflow run if the workflow file exists on the default branch"; "able to access secrets and write tokens, even if the previous workflow was not"; `GITHUB_SHA` = "Last commit on default branch". — events URL above.
    25	- Required-check eligibility: workflow-job checks count only when the run "must be triggered by one of these events": push, pull_request, pull_request_review, pull_request_target, deployment, deployment_status; `workflow_run` and `workflow_dispatch` are not listed (`workflow_dispatch` checks "do not appear in the pull request's checks section"); merge queue needs `merge_group`; this "restriction applies only to checks created by workflow jobs, not to checks created by an external GitHub App". Error text: "Required status check "build" was not set by the expected GitHub App." — https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/troubleshooting-required-status-checks
    26	- App source: "you can select an app as the expected source of status updates"; app needs `statuses:write` and a recent check run. — available-rules URL. REST ruleset `required_status_checks[].integration_id`: "The optional integration ID that this status check must originate from." — https://docs.github.com/en/rest/repos/rules . Branch protection `checks[].app_id`: "Pass -1 to explicitly allow any app to set the status." — https://docs.github.com/en/rest/branches/branch-protection . Note: a PR-edited and a base-branch workflow both report through the same GitHub Actions app, so app-source pinning does not distinguish them (inference from the above; no page states it).
    27	- Reusable workflows: `{owner}/{repo}/.github/workflows/{filename}@{ref}`, "the `{ref}` can be a SHA, a release tag, or a branch name"; "Using the commit SHA is the safest option"; local `./` reference "is from the same commit as the caller workflow". — https://docs.github.com/en/actions/sharing-automations/reusing-workflows
    28	- Environments: "Users with GitHub Free plans can only configure environments for public repositories"; Pro covers private; required reviewers "up to 6 people or teams"; option "to prevent users from approving workflows runs that they triggered". — https://docs.github.com/en/actions/managing-workflow-runs-and-deployments/managing-deployments/managing-environments-for-deployment
    29	- CODEOWNERS enforced only with "Require review from Code Owners"; sole owner = PR author (see self-approval). — about-code-owners URL.
    30	- User-owned availability: pull_request_target, workflow_run, reusable workflows, app-source checks, CODEOWNERS: no restriction stated; environments: public only on Free; required workflows: org/enterprise only.
    31	
    32	## 3. gh CLI and API surfaces
    33	
    34	- `gh pr merge --match-head-commit <SHA>`: "Commit SHA that the pull request head must match to allow merge"; `--auto`: "Automatically merge only after necessary requirements are met"; `--admin`: "Use administrator privileges to merge a pull request that does not meet requirements"; on a branch requiring a merge queue, if checks have not passed "auto-merge will be enabled", else the PR is added to the queue. — https://cli.github.com/manual/gh_pr_merge
    35	- `gh pr update-branch`: "The default behavior is to update with a merge commit"; `--rebase` to rebase. — https://cli.github.com/manual/gh_pr_update-branch
    36	- `gh pr checks`: `--watch`, `--fail-fast`, `--required`, `--interval` (default 10); exit code "8: Checks pending"; JSON `bucket` in pass/fail/pending/skipping/cancel. — https://cli.github.com/manual/gh_pr_checks
    37	- `gh pr review --approve|--request-changes|--comment`; manual silent on self-approval (server rule above applies). — https://cli.github.com/manual/gh_pr_review
    38	- `gh api --paginate` ("Make additional HTTP requests to fetch all pages"), `--slurp`, `--jq`; GraphQL via endpoint `graphql`; `--paginate` with GraphQL "requires that the original query accepts an `$endCursor: String` variable". — https://cli.github.com/manual/gh_api
    39	- Check runs: `GET /repos/{owner}/{repo}/commits/{ref}/check-runs` (per_page default 30, max 100; `check_name`, `status`, `filter=latest|all`, `app_id`); `GET .../check-runs/{id}/annotations` (default 30, max 100); `annotation_level`: `notice`, `warning`, `failure`; "maximum of 50 per API request", appended on update; create/update "only available to GitHub Apps"; Actions "limited to 10 warning and 10 error annotations per step". — https://docs.github.com/en/rest/checks/runs ; "For most endpoints, the maximum value of `per_page` is `100`." — https://docs.github.com/en/rest/using-the-rest-api/using-pagination-in-the-rest-api
    40	- GraphQL `resolveReviewThread(input: {threadId: ID!})` "Marks a review thread as resolved."; `unresolveReviewThread` likewise; `PullRequestReviewThread.isResolved`, `resolvedBy`, `viewerCanResolve`. — https://docs.github.com/en/graphql/reference/pulls
    41	
    42	## 4. Branch protection vs rulesets; up-to-date; auto-merge; skipped checks
    43	
    44	- Both can apply; "all applicable rules are enforced"; "the most restrictive version of the rule applies"; "A ruleset does not have a priority." — https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets
    45	- Classic protection: by default "don't apply to people with admin permissions" unless "Do not allow bypassing the above settings"; strict = "The branch **must** be up to date with the base branch before merging"; required checks need `successful`, `skipped`, or `neutral`. — https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/about-protected-branches ; REST `strict_required_status_checks_policy`: "Whether pull requests targeting a matching branch must be tested with the latest code." — rest/repos/rules URL
    46	- Squash + up-to-date: no page addresses squash specifically (UNVERIFIED). Merge queue intro: provides the benefit of up-to-date but "does not require a pull request author to update their pull request branch and wait for status checks". — managing-a-merge-queue URL
    47	- Auto-merge: "merges a pull request automatically after all required reviews and status checks pass"; "disabled if someone without write permissions pushes new changes to the head branch or switches the base branch"; must be enabled per repository. — https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/automatically-merging-a-pull-request
    48	- Skipped required checks: path/branch/commit-message skips "stay in a "Pending" state and block merging" ("Waiting for status to be reported"); guidance "Avoid requiring workflows that can be skipped."; `if`-skipped job "reports "Success""; job after failed dependency "is skipped and may not block merging" -> use `always()` with `needs`; "If a check and a commit status have the same name, both must pass". The current cloud page has no duplicate-workflow/`paths-ignore` example. — troubleshooting URL above
    49	- Checks are evaluated on the test merge commit when it has a status, else on the head commit. — troubleshooting URL
    50	
    51	## 5. GitHub Actions mechanics
    52	
    53	- Concurrency: "at most one running job or workflow in a concurrency group at any time"; `cancel-in-progress: true`; "Up to 100 jobs or workflow runs can be `pending`"; `group: ${{ github.head_ref || github.run_id }}`. — https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/control-the-concurrency-of-workflows-and-jobs
    54	- OIDC: provider "issues a short-lived access token that is only valid for a single job"; claims `sub`, `repository`, `ref`, `environment`, `job_workflow_ref` (e.g. `octo-org/octo-automation/.github/workflows/oidc.yml@refs/heads/main`). — https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect
    55	- Attestations: "cryptographically signed claims that establish your build's provenance"; public repos use Sigstore Public Good with transparency log, private use GitHub's Sigstore instance; "SLSA v1.0 Build Level 2". — https://docs.github.com/en/actions/concepts/security/artifact-attestations . How-to uses `actions/attest@v4` with `permissions: id-token: write, contents: read, attestations: write`; verify with `gh attestation verify PATH -R OWNER/REPO`. — https://docs.github.com/en/actions/security-for-github-actions/using-artifact-attestations/using-artifact-attestations-to-establish-provenance-for-builds . GA changelog used `actions/attest-build-provenance@v1`; "supports both public and private repositories". — https://github.blog/changelog/2024-06-25-artifact-attestations-is-generally-available/ . Private-repo plan gating: UNVERIFIED.
    56	- Annotations: `::error file={name},line={line},endLine={endLine},title={title}::{message}` (also `::warning`, `::notice`); `GITHUB_STEP_SUMMARY` "maximum size of 1MiB" per step, "A maximum of 20 job summaries from steps are displayed per job." — https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/workflow-commands-for-github-actions
    57	- `GITHUB_TOKEN` defaults for personal-account repos: "only has read access for the `contents` and `packages` scopes"; "workflows are not allowed to create or approve pull requests"; fork approval: "By default, all first-time contributors require approval". — managing-github-actions-settings URL . "events triggered by the `GITHUB_TOKEN` will not create a new workflow run." — https://docs.github.com/en/actions/concepts/security/github_token . Scopes include `checks`, `statuses`, `pull-requests`, `id-token`, `attestations`; "If you specify the access for any of these permissions, all of those that are not specified are set to `none`." Fork PRs: "The `GITHUB_TOKEN` has read-only permissions in pull requests from forked repositories." — https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax ; events URL
    58	- Reading another PR's checks: check-runs listing is a read endpoint ("OAuth apps and authenticated users can view check runs"); a job with `checks: read` can query it (combination of two docs; no single page states it).
    59	
    60	## 6. Bots
    61	
    62	- Codex (OpenAI): trigger with `@codex review` in a PR comment; "Codex flags only P0 and P1 issues"; "posts a standard GitHub code review"; automatic review via Codex settings ("GitHub push or admin permission for its settings"); `## Code Review Rules` in nearest `AGENTS.md`; follow-up e.g. "@codex fix the P1 issue". Rate limits and approve/request-changes behaviour: UNVERIFIED. — https://learn.chatgpt.com/docs/third-party/github (redirect target of https://developers.openai.com/codex/integrations/github); https://developers.openai.com/codex/use-cases/github-code-reviews
    63	- CodeRabbit: limits "enforced **per developer** over rolling time windows"; PR reviews/hour: Free 1 (summary only), OSS 1–10, Essentials 5, Team 8, Advanced 10, Enterprise 12; files/review 150–300; "Open-source projects receive Team features". — https://docs.coderabbit.ai/management/plans . "CodeRabbit reviews pushes, not commits"; default "an incremental review on every push, and a pause after five reviewed commits"; rate-limited push posts check "Review rate limited" that passes "so it never blocks merging on protected branches"; `@coderabbitai rate limit`, `@coderabbitai review`. — https://docs.coderabbit.ai/management/rate-limits . `@coderabbitai review` = "incremental review of new changes only"; `@coderabbitai full review` = "complete review of all files from scratch"; `@coderabbitai resolve` "Marks all CodeRabbit review comments as resolved." — https://docs.coderabbit.ai/reference/review-commands
    64	- Copilot code review: `gh pr edit PR-NUMBER --add-reviewer @copilot`, `gh pr create --reviewer @copilot`, REST reviewer `copilot-pull-request-reviewer[bot]`; default "Copilot leaves a "Comment" review"; approvals public preview, dismissed on new commits; re-review only on request unless "Review new pushes" ruleset; "Copilot may repeat the same comments". — use-code-review URL . Plans: automatic reviews "available on the Copilot Pro, Copilot Pro+, and Copilot Max plans" or Business/Enterprise license; "Copilot Free plan, which does not include Copilot code review"; "In personal repositories, only the repository owner or a direct collaborator can request a review."; billed in AI credits; no per-review quota stated. — https://docs.github.com/en/copilot/concepts/agents/code-review
    65	
    66	## 7. PR size
    67	
    68	- Only official guidance: "Write small pull requests" — "Small, focused pull requests are easier to review and safer to merge."; "When a change grows large, consider splitting it into smaller pull requests that each serve one purpose." No numeric limit. — https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/getting-started/best-practices-for-pull-requests
    69	- No github.blog PR-size research found.
2026-10-10T22:34:30Z

**Finalizing design verdict details**
**Analyzing fallback and audit findings**
**Analyzing invariant checks and design gaps**
**Reviewing enforcement approach**
codex
---
reviewed_at: 2026-10-10T22:34:30Z
reviewer: codex-review-dot-h001
profile: review
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@40476474ad9aec1f36f14927a43a8f98d0187eb5d7092b422b635fbdff70142a
round: 7
---

INV-1: rejected: an operator waiver is only named in an orchestrator-authored acceptance record, so the orchestrator can fabricate permission to skip stages; require an operator-authenticated agmsg or GitHub event and bind its immutable identifier in the gate.
INV-2: accepted
INV-3: rejected: the `repro:<id>` path verifies only that PR-controlled command and output strings are non-empty, so any revision passes without adding a deterministic check; execute a main-approved reproducer in CI or remove this alternative.
INV-4: rejected: premises and pasted outputs are entirely orchestrator-authored and never independently executed or history-anchored, so false premises still pass; verify commands in a trusted runner and bind results to the task hash before dispatch.
INV-5: rejected: the audit is said to consume an acceptance record before stage 4 creates it, and no hash binds the complete audit input set; create and anchor an immutable pre-acceptance disposition draft before audit, then prohibit material changes without re-audit.
INV-6: rejected: `DESIGN_RESET_WAIVED_BY` and the reset record do not authenticate operator consent, allowing the orchestrator to release its own reset; require an operator-authored agmsg or GitHub event whose actor and immutable id the gate verifies.
INV-7: accepted
INV-8: accepted
INV-9: rejected: `accept-task.py` writes orchestrator-controlled cost claims from local transcripts without an immutable source binding, while transcript format is explicitly internal and per-message usage is unverified; anchor raw runtime JSON/session identifiers before acceptance and recompute the totals.
INV-10: rejected: `gh pr view` cannot establish the time of the first pushed commit, and “idle while a dispatchable task exists” has no mechanical definition or trusted dispatchability source; use immutable GitHub commit timestamps and define dispatchability as a computable history state.
INV-11: accepted
INV-12: rejected: `make unit-test` runs from the PR-controlled `pull_request` workflow and PR-controlled tests, while the proposed main-pinned job checks schemas, caps, and evidence shape rather than independently exercising every invariant; run invariant tests and their trusted harness from the base branch against PR data.

## Findings

[P1] .orchestration/tasks/dotfiles-T128-regime-v3-a01.md:45 The stage-skipping waiver is authenticated only by an orchestrator-authored acceptance record, so INV-1 can be bypassed by the actor it constrains.

[P1] .orchestration/tasks/dotfiles-T128-regime-v3-a01.md:47 A fabricated non-empty `repro` command and output satisfy INV-3 without introducing any executable fact.

[P1] .orchestration/tasks/dotfiles-T128-regime-v3-a01.md:48 The orchestrator can invent premise output, leaving T119’s false-premise amendment loop open before dispatch.

[P1] .orchestration/tasks/dotfiles-T128-regime-v3-a01.md:49 The audit input includes an acceptance record that stage 4 has not yet produced, and later edits to that record do not invalidate the audit.

[P1] .orchestration/tasks/dotfiles-T128-regime-v3-a01.md:50 The orchestrator can set `DESIGN_RESET_WAIVED_BY` and author the supporting record, defeating the mandatory reset backstop.

[P1] .orchestration/tasks/dotfiles-T128-regime-v3-a01.md:56 INV-12 relies on tests and a `pull_request` workflow the PR controls, so a malicious PR can weaken the oracle that judges its enforcement code.

[P2] .orchestration/tasks/dotfiles-T128-regime-v3-a01.md:53 Cost totals are copied into orchestrator-controlled evidence without a trusted runtime-output digest, permitting arbitrary understatement.

[P2] .orchestration/tasks/dotfiles-T128-regime-v3-a01.md:54 GitHub PR metadata does not identify the first push time, and “dispatchable” is subjective, making both timing rules gameable.

[P2] .orchestration/tasks/dotfiles-T128-regime-v3-a01.md:88 The premise that Claude bare mode loads skills from `--add-dir` contradicts the cited factsheet, which says `--bare` skips skills; fallback policy must distinguish bare from non-bare execution.

## Residual

T118’s long revise loop can still pass through fabricated `repro` evidence, and its oversized review burden can move into excluded tests or orchestration evidence.

T119’s false-premise cycle remains possible because premise commands are recorded but not independently executed; the orchestrator can also waive the resulting reset.

T124’s trust-boundary bypass pattern remains possible because PR-controlled invariant tests can approve weakened enforcement, while unauthenticated waiver and cost records preserve the same self-certification problem.

Design verdict: reject
hook: Stop
hook: Stop Completed
tokens used
79,586
---
reviewed_at: 2026-10-10T22:34:30Z
reviewer: codex-review-dot-h001
profile: review
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@40476474ad9aec1f36f14927a43a8f98d0187eb5d7092b422b635fbdff70142a
round: 7
---

INV-1: rejected: an operator waiver is only named in an orchestrator-authored acceptance record, so the orchestrator can fabricate permission to skip stages; require an operator-authenticated agmsg or GitHub event and bind its immutable identifier in the gate.
INV-2: accepted
INV-3: rejected: the `repro:<id>` path verifies only that PR-controlled command and output strings are non-empty, so any revision passes without adding a deterministic check; execute a main-approved reproducer in CI or remove this alternative.
INV-4: rejected: premises and pasted outputs are entirely orchestrator-authored and never independently executed or history-anchored, so false premises still pass; verify commands in a trusted runner and bind results to the task hash before dispatch.
INV-5: rejected: the audit is said to consume an acceptance record before stage 4 creates it, and no hash binds the complete audit input set; create and anchor an immutable pre-acceptance disposition draft before audit, then prohibit material changes without re-audit.
INV-6: rejected: `DESIGN_RESET_WAIVED_BY` and the reset record do not authenticate operator consent, allowing the orchestrator to release its own reset; require an operator-authored agmsg or GitHub event whose actor and immutable id the gate verifies.
INV-7: accepted
INV-8: accepted
INV-9: rejected: `accept-task.py` writes orchestrator-controlled cost claims from local transcripts without an immutable source binding, while transcript format is explicitly internal and per-message usage is unverified; anchor raw runtime JSON/session identifiers before acceptance and recompute the totals.
INV-10: rejected: `gh pr view` cannot establish the time of the first pushed commit, and “idle while a dispatchable task exists” has no mechanical definition or trusted dispatchability source; use immutable GitHub commit timestamps and define dispatchability as a computable history state.
INV-11: accepted
INV-12: rejected: `make unit-test` runs from the PR-controlled `pull_request` workflow and PR-controlled tests, while the proposed main-pinned job checks schemas, caps, and evidence shape rather than independently exercising every invariant; run invariant tests and their trusted harness from the base branch against PR data.

## Findings

[P1] .orchestration/tasks/dotfiles-T128-regime-v3-a01.md:45 The stage-skipping waiver is authenticated only by an orchestrator-authored acceptance record, so INV-1 can be bypassed by the actor it constrains.

[P1] .orchestration/tasks/dotfiles-T128-regime-v3-a01.md:47 A fabricated non-empty `repro` command and output satisfy INV-3 without introducing any executable fact.

[P1] .orchestration/tasks/dotfiles-T128-regime-v3-a01.md:48 The orchestrator can invent premise output, leaving T119’s false-premise amendment loop open before dispatch.

[P1] .orchestration/tasks/dotfiles-T128-regime-v3-a01.md:49 The audit input includes an acceptance record that stage 4 has not yet produced, and later edits to that record do not invalidate the audit.

[P1] .orchestration/tasks/dotfiles-T128-regime-v3-a01.md:50 The orchestrator can set `DESIGN_RESET_WAIVED_BY` and author the supporting record, defeating the mandatory reset backstop.

[P1] .orchestration/tasks/dotfiles-T128-regime-v3-a01.md:56 INV-12 relies on tests and a `pull_request` workflow the PR controls, so a malicious PR can weaken the oracle that judges its enforcement code.

[P2] .orchestration/tasks/dotfiles-T128-regime-v3-a01.md:53 Cost totals are copied into orchestrator-controlled evidence without a trusted runtime-output digest, permitting arbitrary understatement.

[P2] .orchestration/tasks/dotfiles-T128-regime-v3-a01.md:54 GitHub PR metadata does not identify the first push time, and “dispatchable” is subjective, making both timing rules gameable.

[P2] .orchestration/tasks/dotfiles-T128-regime-v3-a01.md:88 The premise that Claude bare mode loads skills from `--add-dir` contradicts the cited factsheet, which says `--bare` skips skills; fallback policy must distinguish bare from non-bare execution.

## Residual

T118’s long revise loop can still pass through fabricated `repro` evidence, and its oversized review burden can move into excluded tests or orchestration evidence.

T119’s false-premise cycle remains possible because premise commands are recorded but not independently executed; the orchestrator can also waive the resulting reset.

T124’s trust-boundary bypass pattern remains possible because PR-controlled invariant tests can approve weakened enforcement, while unauthenticated waiver and cost records preserve the same self-certification problem.

Design verdict: reject
