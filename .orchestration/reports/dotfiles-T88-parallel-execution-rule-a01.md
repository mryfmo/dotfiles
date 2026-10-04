# dotfiles-T88-parallel-execution-rule-a01 — report (status: ready_for_review)

Worker: `claude-standard-dot-a006` (Claude Code, `standard`), worktree `.claude/worktrees/worker-d`.
PR: https://github.com/mryfmo/dotfiles/pull/243 — branch `docs/parallel-execution-rule`.

Commits:
- `e50150df` task commit
- `e68eb6a7` Codex review fix
- update-branch merges `240bb772` (main 57885db1) and `c8d31501` (main a5c30b6d, the T66 merge)

Final head `c8d3150159d14e45ebb067605077220c59df510b`:
- CI all pass (nix skipped);
- up to date with `origin/main` a5c30b6d;
- `mergeable_state` = `blocked` while the two Codex threads are unresolved; threads were not resolved, per the task.

Task file `41cf14c6…` verified. T88 was paused for the T66 revise round (task_rev b7fa55fe) and resumed afterwards.

## Changes (allowed files only)

1. **`home/dot_config/claude/rules/agmsg-orchestration.md`**
   - New parallel-execution bullet:
     - pairwise-disjoint `allowed_files` → concurrent dispatch to `herdr-agents --add-worker` worktrees, up to three workers in total (the resident pair worker counts), with the rest queued;
     - overlapping code files run sequentially;
     - shared prose files (README, SKILL) may be edited in non-overlapping sections, with the later PR merging the new base in via `gh pr update-branch`; a real conflict blocks only the later PR;
     - a freed worker is re-tasked immediately; acceptance follows RESULT arrival order; audits queue on the single audit tab.
   - New seat-capability routing bullet: tasks editing the source of Claude's own permission policy (the `claude.permissions` block of `agent-config.yaml`, `claude-settings-managed.json`, `modify_private_settings.json`) go to a Codex worker or the operator, never to a Claude seat. A refused Claude worker stops without a diff and sends `AGMSG-PONG v1 status=blocked` naming the Self-Modification reason.
   - The nested-worktree bullet (the one that said "network access stays off … escalation prompt") now matches SKILL bullet 46: the seat runs with `--ask-for-approval never` and in-sandbox network, there is no worker escalation, and out-of-sandbox or forbidden actions fail as blocked PONGs.
   - Word count 1269 → 1454. T83, which shrinks this file, should absorb it.
2. **`home/dot_agents/skills/agmsg-orchestration/SKILL.md`**
   - "Parallel workers": condition (4) now requires pairwise-disjoint code files and allows shared prose files in non-overlapping sections. A new "Parallel execution procedure" bullet adds:
     - the wave table in the plan file;
     - a three-worker cap counting the pair worker, with dispatch up to free seats and the rest queued;
     - accept in RESULT order;
     - re-task freed workers immediately, never leaving a seated worker idle;
     - `gh pr update-branch` described as a merge, not a rebase;
     - the wave table and per-task worker recorded in acceptance records;
     - audits serialize on the single tab (one per task via T67), and the gate and merges stay one at a time.
   - Orchestrator Playbook step 3 (task authoring) now says:
     - decide the worker kind from the allowed files;
     - Claude-permission-policy tasks go to Codex or the operator;
     - `auto` has been the built-in starting mode since 2.1.283, and a project-level `defaultMode: auto` is ignored together with the user-level value.
   - Worker Playbook step 4: a classifier denial is a boundary, so send a blocked PONG naming the reason and never evade it.
   - New step 14: before RESULT, a Plan Mode worker closes its Crit server with `crit stop` (never `--all`) and confirms with an unsandboxed `pgrep -af '[c]rit _serve'`, because `make check-regime-boundary` and host-`pgrep` unit tests fail while one runs.
3. **`tests/unit/test_agmsg_orchestration_docs.py`:** two new tests.
   - `test_rule_and_skill_share_the_parallel_execution_and_routing_invariants` checks both files for `pairwise-disjoint`, `--add-worker`, `re-tasked immediately`, `acceptance follows RESULT arrival order`, `gh pr update-branch`, `Self-Modification`, `home/dot_claude/modify_private_settings.json`, `AGMSG-PONG v1 status=blocked` and `--ask-for-approval never`.
   - `test_rule_drops_the_worker_network_escalation` checks that "network access stays off" is gone from the rule.
4. **`AGENTS.md`:** no sentence contradicts these rules (grep for network access, escalation, pairwise, parallel and Self-Modification has no hits; pasted in validation). Unchanged.

## Codex review

On e50150df there were two P2s. Both were valid, and both were fixed in `e68eb6a7`:
- `4175647852` (SKILL.md:37): a wave larger than the free seats was dispatched at once, and the pair worker was not counted against the cap. Fix: count the pair worker, dispatch up to the free seats, queue the rest; the rule says "in total (the resident pair worker counts)".
- `4175647854` (SKILL.md:40): `gh pr update-branch` merges by default rather than rebasing; verified with `gh pr update-branch --help`, pasted in validation. Fix: both files now say it merges the new base in.

After the fix:
- e68eb6a7: no Codex response before the update-branch, recorded as `bot: none`.
- 240bb772: `+1` at 02:23:21Z.
- c8d31501 (final head): `+1` at 02:32:10Z, with no new review or inline comments.

Proposed dispositions:
- 4175647852 → `fixed:e68eb6a7`
- 4175647854 → `fixed:e68eb6a7`

## Reporting notes

- **`agmsg-dispatch` and the sandbox.** Worker Playbook step 11 says `claude.sandbox.excludedCommands` runs `agmsg-dispatch` outside the sandbox from the first attempt. On this seat, every first sandboxed `agmsg-dispatch` failed with herdr socket `PermissionDenied` and needed an unsandboxed retry through the permission gate. I left it unchanged because it is out of scope; it is recorded in the learning file for a follow-up.
- **`crit stop`.** Whether a bare `crit stop` reaches a Plan Mode plan server was not verified, because this seat's server had already been stopped by pid in T66. Step 14 therefore pairs it with the `pgrep` confirmation.
- **Corrected evidence in the T66 validation file.** The round-1 sections, written earlier by this worker, had two literal `%H %s` lines and one literal `exit status: %s` line, caused by a `%%` escaping slip.
  - The two commit lines were replaced with `git show -s --format='%H %s'` output for a93fcb94 and a31dcf86.
  - The exit status was re-derived: `gh pr checks 240` on the same head a31dcf86 exits 0. The replacement line says it was re-derived.
  - The same slip was fixed in this task's own validation file before this RESULT.

[memory:decision] dotfiles-T88 (operator 2026-10-04): tasks that edit Claude's permission-policy source go to a Codex worker or the operator (the auto-mode classifier refuses a Claude seat as self-modification; the worker reports a blocked PONG, never evades); independent tasks run in parallel on up to three herdr-agents worker worktrees with pairwise-disjoint allowed_files; same-file tasks run sequentially; freed workers are re-tasked at once; acceptance follows RESULT order and audits queue on the single audit tab. Written into the agmsg-orchestration rule and SKILL.

CompactionDB, run in the main checkout outside the sandbox:

```
$ cd /home/moriya/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "dotfiles-T88 (operator 2026-10-04): tasks that edit Claude's permission-policy source go to a Codex worker or the operator (the auto-mode classifier refuses a Claude seat as self-modification; the worker reports a blocked PONG, never evades); independent tasks run in parallel on up to three herdr-agents worker worktrees with pairwise-disjoint allowed_files; same-file tasks run sequentially; freed workers are re-tasked at once; acceptance follows RESULT order and audits queue on the single audit tab. Written into the agmsg-orchestration rule and SKILL."
33356f9a-a70b-4d61-b725-dde6d67594d0
$ python3 .claude/hooks/contextdb_cli.py memory search dotfiles-T88   (the CLI truncates long entries with …)
33356f9a-a70b-4d61-b725-dde6d67594d0 [project/decision] dotfiles-T88 (operator 2026-10-04): tasks that edit Claude's permission-policy source go to a Codex worker or the operator (the auto-mode classifier refuses a Claude seat as self-modification; the worker reports a blocked PONG, never evades); independent tasks run in parallel on up to three herdr-agents worker worktrees with pairwise-disjoint allowed_files; same-file tasks run sequentially; freed workers are re-tasked at once; acceptance follows RESULT order and audits queue…
```

cost: n/a (the Claude Code runtime does not expose per-session token or cost figures to the worker)

## Revise round 1 (audit of e50150df), addendum, PONG decisions 2 and 3

The final head is `04fd942546ac3833ce5eb4f01f9f3a3f732c173c`. CI is all pass (nix skipped). `origin/main` = 8922f13b, and the branch is up to date with it. `mergeable_state` = `blocked` while threads are unresolved; threads were not resolved.

Fix commits (SKILL.md only; the rule file and the docs test are unchanged in this round):

- **`c544c79f`** (round 1, the audit's two open findings). Step 14 applies to Claude workers only: Plan Mode and Crit are Claude Code features, and a Codex seat under never-approval has no plan server. It covered the branch-orphaned plan server that `crit stop` misses.
- **`8978517d`** (PONG decision 2):
  - 4175958710: the worker does no host-side `readlink`/`kill`; a surviving server is reported, and the orchestrator cleans it up.
  - 4175958708: a re-tasked worker starts the next task on a fresh branch from `origin/main`, and the previous branch stays untouched until acceptance.
- **`c5706e2e`** (addendum). Verified on a scratch `crit plan` with crit v0.21.1, pasted in validation:
  - `crit stop <plan-file>` never matches a plan session;
  - a bare `crit stop` works only outside the sandbox and only on the branch the server was started on.
  - Step 14 records this.
- **`d609c768`** (PONG decision 3, one commit for three Codex P2s on c5706e2e):
  - 4176005504: a sandboxed `pgrep` sees only the sandbox pid namespace. The worker now adds only `plan-mode-used=<worktree>` to its RESULT, and the orchestrator lists the servers with `pgrep -fl _serve`, confirms the cwd from `~/.crit/sessions/*.json`, and runs `kill <pid>` on the host.
  - 4176005501: `gh pr update-branch` applies to every in-flight PR whose base moved, prose or code, before its CI, Bot wait and gate.
  - 4176005508: permgate edits (`permgate-policy.yaml`, `executable_permgate`) go to a Codex `security`-profile worker. The citation is the model-selection rule, not the classifier, which allowed T66.
- Update-branch merges `32225647` (main 138e6a72) and `04fd9425` (main 8922f13b).

Codex Bot:
- **32225647:** 4175958708 and 4175958710.
- **c5706e2e:** 4176005501, 4176005504 and 4176005508.
- **Final head 04fd9425:** no review and no inline comment; it reacted `+1` at 2026-10-04T04:02:29Z.

Proposed dispositions:
- 4175958708 → `fixed:8978517d`
- 4175958710 → `fixed:8978517d` (refined by `d609c768`)
- 4176005501 → `fixed:d609c768`
- 4176005504 → `fixed:d609c768`
- 4176005508 → `fixed:d609c768`
- 4175647852 and 4175647854 (round 0) stay `fixed:e68eb6a7`; the orchestrator already replied on both.

Local checks on 04fd9425: `make unit-test` 702 OK, `make validate-agent-assets` ok, the docs test OK, and prettier clean.

Housekeeping:
- The scratch plan file and `~/.crit/plans/t88-scratch-a006` were removed.
- A stray `crit version` call (crit treats `version` as a file argument) started a daemon that had already exited when checked: `pgrep` rc=1 and `ps -p` empty.
- The T88 validation file had `%%` format slips in two appended sections. They were replaced with real `git log`/`git show` output before this RESULT.

## Revise round 2 (task_rev 5bd4efd7…) and PONG decision 4 (task_rev cb40c955…)

**Round 2 (`0aed931c`, SKILL step 14).**
- Step 14 now covers any worker whose session started a Crit plan review: Claude through Plan Mode's ExitPlanMode hook, Codex through the Crit plugin's Stop hook (`crit plan-hook --mode codex`, trusted at `codex-config-managed.toml:114`; the evidence is pasted). Both report `plan-mode-used=<worktree>`. The sentence that a Codex seat never has a plan server is gone.
- Before `kill`, the orchestrator confirms live identity: `ps -o args= -p <pid>` shows `crit _serve`, and the record's cwd is the worker's worktree. A record whose pid is gone or runs another command is stale and is removed, never killed.
- The sandbox file now records the scratch `crit plan` server, the stray `crit version` daemon, and their cleanup. Applying the new step 14, I removed the stale `~/.crit/sessions/b8359df9be5d.json` (its pid was gone) rather than killing anything.
- The CompactionDB command is pasted exactly as run in the validation file and in this report, with the note that `memory search` truncates long entries.

After update-branch to `adfd1fa7` (main 06875e4e, #237), CI was green. The Codex review of adfd1fa7 then raised one P1 and two P2s outside round 2's scope, so I sent `AGMSG-PONG status=blocked`. Decision 4 extended the scope.

**Decision 4 (`0407fb07`).**
- 4176301037 (P1): the rule bullet and SKILL step 3 now state that a seat never edits the source of its own execution boundary. Both the `claude.permissions` and the `claude.sandbox` blocks (excludedCommands, allowUnsandboxedCommands, writable roots, network), the rendered `claude-settings-managed.json` and `modify_private_settings.json` go to a Codex worker or the operator. The docs parity test pins `claude.sandbox`.
- 4176301038 (P2): step 14 says the orchestrator runs its host `pgrep`/`ps`/`kill` outside its sandbox through the permission gate (`dangerouslyDisableSandbox`, answered by the operator or the auto-mode classifier) under its control-plane exemption, as for `agmsg-dispatch` and `herdr-agents --audit`.
- 4176301040 (P2): `not-applicable` per decision 4. The worker kind is the manifest's `worker_kind`, and T83 removes the legacy "resident Codex workers" wording. The orchestrator replies on the thread; the procedure is unchanged.

Update-branch onto f32f33a0 (#246, T68) gave `6d843053`, then `0407fb07` on top. Local checks: `make unit-test` 753 OK, `make validate-agent-assets` ok, the docs test OK, prettier clean. The rule file is now 1472 words.

Proposed dispositions for this round:
- 4176301037 → `fixed:0407fb07`
- 4176301038 → `fixed:0407fb07`
- 4176301040 → `not-applicable:` worker kind is the manifest's `worker_kind`; T83 drops the legacy Codex wording.

The orchestrator already replied on 4175958708, 4175958710, 4176005501, 4176005504 and 4176005508.

**Follow-up (`d0f03418`), P1 4176483554 raised on 0407fb07.** The routing list omitted the policy-emitting inputs and the renderer. The rule bullet and SKILL step 3 now name every source that renders into Claude's managed settings or permission gate:
- the `claude.permissions`, `claude.sandbox` and `claude.hooks` blocks of `agent-config.yaml`, including the PermissionRequest hook;
- `codex.sandbox_workspace_write.writable_roots`, which renders into Claude's `allowWrite`;
- `scripts/generate-agent-configs.py`;
- the rendered `claude-settings-managed.json`;
- `modify_private_settings.json`.

Proposed disposition: `fixed:d0f03418`. Local checks: `make unit-test` 753 OK, `make validate-agent-assets` ok.

Final head `d0f034182529fe9874037e0f21b7a624229ece0f`: CI is all pass (nix skipped), and the branch is up to date with `origin/main` f32f33a0. The Codex Bot gave no response on d0f03418 within ~20 minutes of the push (`bot: none`).

**Correction.** The RESULT sent at ~07:17Z said the branch was up to date with f32f33a0, but main had already moved to 0ea5948b (#250, pins only). After `gh pr update-branch`, the final head is `19becfc5d1c6e3dd30f27c897318af5ecb1cb631`. CI is all pass, `mergeable_state` = `clean`, and the Codex Bot reacted `+1` at 2026-10-04T07:20:35Z with no new findings. The orchestrator has replied on 4176301037, 4176301038 and 4176483554.

## Revise round 3 (task_rev e1ea015a…)

1. **P2, fixed in `99f84926`.** Step 14's orchestrator bullet now also requires the live process's cwd to match: `readlink /proc/<pid>/cwd` on Linux (`lsof -a -d cwd -p <pid> -Fn` on macOS) must equal the record's `cwd`. A mismatch means the pid was reused, and the record is stale (removed, never killed).
2. **P3, evidence.** The validation file now holds the verbatim stale-record check and removal from round 2: the `cat` of `~/.crit/sessions/b8359df9be5d.json`, `ps -o args= -p 3736107` with no output and rc=1, the `rm`, and the absent review directory. No `readlink` was run then because the pid was gone; a round-3 re-run of `readlink /proc/3736107/cwd` and `ps` (both rc=1) is pasted and labelled as such.

Round 3 final head `5bef5588fc118f38a3242d45acba2fd734f4e0a4` (update-branch onto main 65915b93): CI is all pass after one re-run of a transient `chezmoi: unexpected EOF` bootstrap failure.

The Codex review of 5bef5588 raised two P2s outside round 3's step-14 scope:
- **4176692309.** The rule's routing bullet omits permgate (`permgate-policy.yaml`, `executable_permgate`), which the SKILL already routes to a Codex `security` worker. Valid. The proposed fix is one phrase in the rule bullet, mirroring the SKILL; it needs the rule bullet back in the allowed files.
- **4176692312.** Re-tasking a freed worker switches its only worktree to the next task's branch before the first task is accepted, so a later revise round interrupts the second task. This is a policy call, and two options are proposed:
  - (a) `not-applicable`: in this session a revise round paused the in-flight task and switched branches in the same worktree (T88 was paused for the T66 revise round, then resumed), which worked because each task's branch stays untouched until acceptance;
  - (b) a sentence saying a revise round takes priority and the in-flight task is paused and resumed on its own branch.

## Revise round 4 (task_rev 60458ed3…)

Fix commit `0189cfb3`. The head is `0189cfb3b8480187940bd7176f5748b2ce0e15bc`; CI is all pass, and the branch is up to date with main 65915b93.
- **4176692309 → `fixed:0189cfb3`.** The rule's routing bullet now names permgate (`permgate-policy.yaml`, `executable_permgate`) for a Codex `security`-profile worker per the model-selection rule, matching the SKILL. The docs parity test pins `home/dot_agents/permgate-policy.yaml`.
- **4176692312 → `fixed:0189cfb3`.** The parallel procedure says the worker commits and pushes everything before each RESULT. A later `status=revise` checks the earlier branch out again, does the round, and returns to the newer task's branch, so the worktree is reused sequentially with nothing uncommitted left behind.
- Local checks: `make unit-test` 760 OK, `make validate-agent-assets` ok, the docs test OK, prettier clean.

The Codex review of 0189cfb3 raised P2 **4176768869**: route `home/dot_config/claude/rules/**` and the deploying `home/dot_claude/rules/**` templates away from Claude seats. Proposed disposition: `not-applicable:` the routing invariant protects a seat's execution boundary (permissions, sandbox, the permission gate and their renderers), which changes what a seat can do without review. Rule text is prose that every change already passes through PR review, the task-level audit and orchestrator acceptance. Routing all rule sources away from Claude seats would also forbid this task, a Claude worker editing rules at the orchestrator's direction. Decision left to the orchestrator.

**Round 4 addendum (task_rev 56480ce2…): evidence only, head unchanged at 0189cfb3.**

In the validation file:
- The stale-record transcript (line 705) shows the actual pid-lookup command instead of an ellipsis.
- A new section pastes the scratch-cleanup commands with their output (the `ls -la` of `~/.crit/plans/t88-scratch-a006`, then `removed`).
- The same section pastes the CI re-run: the first attempt's `chezmoi: unexpected EOF` failure lines, `gh run rerun 37186817410 --failed` (rc=0), and `gh run view … --json conclusion,attempt,jobs` showing attempt 2 success on all six bootstrap jobs. The two `gh run list` checks it relies on are re-run in full, not abbreviated.

**Correction and final head.** main moved to f2b5c115 (#248) as the round-4 RESULT was sent, so that RESULT's "up to date with 65915b93" was stale. After `gh pr update-branch`, the final head is `5fa735f5ad9f5058dce33b11d0e3aa7141e97eb8`: all 13 checks pass, `mergeable_state` = `clean`, and the Codex Bot reacted `+1` after the update. The orchestrator has replied on 4176692309, 4176692312 and 4176768869.

Learning: read `origin/main` immediately before dispatching a RESULT. Twice this task, main moved between the last update-branch and the dispatch.

## Revise round 5 (task_rev dccfdd91…)

Fix commit `fb4c9a9a`; this is the final head. CI: all 13 checks pass, `mergeable_state` = `clean`, and the branch is up to date with main f2b5c115. The Codex Bot gave no response on this head (`bot: none`).
1. **P2, route by the boundary a change touches.** The rule bullet and SKILL step 3 now route each change by the boundary it touches:
   - Claude-only sources go to a Codex seat: the `claude.*` blocks, the Claude-rendering parts of the renderer, `claude-settings-managed.json` and `modify_private_settings.json`.
   - Codex-only sources go to a Claude seat: `codex.sandbox_workspace_write`, `codex.approval_policy`, the Codex-rendering renderer parts and `codex-config-managed.toml`.
   - A change touching both, or an unsplittable shared source such as `codex.sandbox_workspace_write.writable_roots` (which also renders Claude's `allowWrite`), goes to the operator.
   - The orchestrator decides the kind from the diff the task will produce and records it in the task file.
2. **P2, clean checkpoint.** The parallel procedure says that before every branch switch the worker commits the newer task's work, or stashes it under a named tag and restores it afterwards, so a switch never carries edits across branches. This is in the same sentence as commit-and-push-before-RESULT.
3. **P3.** The Prettier run on the final head is pasted with its command, `git rev-parse HEAD` and output.

Local checks: `make unit-test` 771 OK, `make validate-agent-assets` ok, the docs test OK.

Open point: the permgate sentence (decision 3) still routes permgate to a Codex `security`-profile worker. permgate is the PermissionRequest hook for both Claude and Codex, so under the new by-boundary rule it arguably touches both boundaries, which would mean the operator. It was left as decided in decision 3; the orchestrator may want to reconcile it.

## Revise round 6 (task_rev 2e3ebc6a…)

Fix commit `62845ab9`; this is the final head. CI: all 13 checks pass, `mergeable_state` = `clean`, and the branch is up to date with main f2b5c115. The Codex Bot reacted `+1` at 2026-10-04T09:50:04Z, with no review or comment on the head.
1. **P2.** permgate is the PermissionRequest hook of both seats, so the rule bullet and SKILL step 3 now route permgate edits (`permgate-policy.yaml`, `executable_permgate`) to the operator. A Codex `security`-profile worker reviews the change before the orchestrator accepts it, per the model-selection rule, which assigns that worker to audits, not edits. The docs parity test pins the new phrase. This resolves the open point raised in round 5.
2. **P3.** The validation file pastes the paginated Bot poll on the final head: the head-filtered reviews listing, the head-filtered inline comments, the top-level issue comments and the reactions query, each with its command, output and the observation window.

Local checks: `make unit-test` 771 OK, `make validate-agent-assets` ok, the docs test OK, prettier clean.
