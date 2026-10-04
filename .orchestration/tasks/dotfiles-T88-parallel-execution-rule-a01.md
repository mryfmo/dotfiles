# AGMSG-TASK dotfiles-T88-parallel-execution-rule-a01

Drafted 2026-10-04 by the orchestrator seat from the operator instruction 「並列化できる箇所は並行して作業を実施するように規定し、効率よく作業を実施」 (codify, not only apply). Numbered after the plan's T62–T87 block. Worker: the identity named in the dispatch. Dispatch condition: dotfiles-T64 merged (it edits `SKILL.md:46`; this task edits the same file, so they are sequential).

## Objective

Write the parallel-execution regime into the orchestration documents so it is a rule, not a session habit:

1. `home/dot_config/claude/rules/agmsg-orchestration.md`: one invariant bullet — independent tasks (no dependency, pairwise-disjoint `allowed_files`) are dispatched concurrently to worker worktrees seated with `herdr-agents --add-worker`, up to three workers; tasks whose code files overlap run sequentially, while shared prose files (README, SKILL) may be edited concurrently in non-overlapping sections (the later PR rebases with `gh pr update-branch`, and a real conflict blocks only the later one); a freed worker is re-tasked immediately; acceptance follows RESULT arrival order; audits queue on the single audit tab. Keep it to one bullet (the rule file is being shrunk by T83).
2. `home/dot_agents/skills/agmsg-orchestration/SKILL.md`, section "Parallel workers": the procedure — at plan approval, partition the approved tasks into waves by dependency and file overlap (code files: disjoint; shared prose files: disjoint sections) (write the wave table into the plan file); seat `min(3, |wave|)` workers; dispatch every task of the current wave at once with a distinct `-aNNN` identity and its own worktree; when a RESULT arrives, run acceptance for that task while the others continue; when a worker frees, dispatch the next dependency-free task whose files do not overlap any in-flight task; never leave a seated worker idle while a dispatchable task exists; record the wave table and the per-task worker in the acceptance records. Note the single-audit-tab constraint (audits serialize; the task-level audit of T67 reduces their count to one per task) and the orchestrator-side steps that stay sequential (gate, merge).
3. `tests/unit/test_agmsg_orchestration_docs.py`: add shared tokens so rule and SKILL stay in parity (for example `pairwise-disjoint`, `--add-worker`, `re-tasked immediately`), following the existing test style.
4. **Task routing by seat capability (operator 2026-10-04, from the T62 incident):** the Claude Code auto-mode classifier refuses a Claude agent that edits the source of Claude's own permission policy (reason "Self-Modification": the manifest `claude.permissions` block in `home/dot_agents/agent-config.yaml`, the rendered `home/.chezmoitemplates/claude-settings-managed.json`, the merge script `home/dot_claude/modify_private_settings.json`) and forbids reaching the same outcome through another tool. Rule bullet: such tasks are dispatched to a Codex worker or performed by the operator, never to a Claude seat; a Claude worker that hits the classifier stops without a diff and sends `AGMSG-PONG v1 status=blocked` naming the classifier reason (it never works around it). SKILL: add this to the task-authoring checklist (orchestrator decides the worker kind from the allowed files before dispatch) and to the worker playbook (classifier denial = blocked PONG). Also record there that `auto` is Claude Code's built-in starting mode since 2.1.283 and that a project-level `auto` disables the user-level value.
5. **Contradiction left by T64 (outside its allowed files):** `home/dot_config/claude/rules/agmsg-orchestration.md:17` still says "network access stays off, so a GitHub fetch or push remains a boundary action whose escalation prompt only the human operator answers". Align it with SKILL.md:46 (the worker seat runs with `--ask-for-approval never` and in-sandbox network; no escalation exists for a worker; out-of-sandbox or forbidden actions fail and are reported as blocked PONGs).
6. **Worker playbook hygiene (from the T64 report):** a worker that used Plan Mode closes its crit review server (`crit stop`) before sending RESULT; the regime-boundary check and `make check-regime-boundary` treat a running `crit _serve` as a violation, and unit tests that read the host `pgrep` fail while one runs.
7. `AGENTS.md`: no change unless a sentence there contradicts these rules (report if so).

[memory:decision] dotfiles-T88 (operator 2026-10-04): tasks that edit Claude's permission-policy source go to a Codex worker or the operator (the auto-mode classifier refuses a Claude seat as self-modification; the worker reports a blocked PONG, never evades); independent tasks run in parallel on up to three herdr-agents worker worktrees with pairwise-disjoint allowed_files; same-file tasks run sequentially; freed workers are re-tasked at once; acceptance follows RESULT order and audits queue on the single audit tab. Written into the agmsg-orchestration rule and SKILL.

## Repo / branch

- Work ONLY in your own worktree (worker-d for a006). `git fetch origin`; `git switch -c docs/parallel-execution-rule origin/main` (3a0816e6 or later: T64 and T89 are merged). T67 (a005) edits README's audit section and herdr-agents concurrently; T65 (a007) edits scripts/agent-stop-gate.sh; neither touches the rule, SKILL or the docs test. Verify the dispatched task_rev; else stop and PONG blocked.
- Strict status checks: if `main` moves, `gh pr update-branch <pr>` and wait for CI again before RESULT.

## Allowed files

- `home/dot_config/claude/rules/agmsg-orchestration.md`, `home/dot_agents/skills/agmsg-orchestration/SKILL.md`, `tests/unit/test_agmsg_orchestration_docs.py`
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dotfiles-T88-parallel-execution-rule-a01.md` (main checkout)

## Forbidden actions

- Any code change; `README.md`; `AGENTS.md` (report only); `make update`/`make apply`; local bats; merging; force push; pushing `main`.

## Validation commands (paste verbatim output)

```
git diff origin/main --stat
uv run python -m unittest tests.unit.test_agmsg_orchestration_docs 2>&1 | tail -3
grep -n 'pairwise-disjoint\|re-tasked\|Self-Modification' home/dot_config/claude/rules/agmsg-orchestration.md home/dot_agents/skills/agmsg-orchestration/SKILL.md
wc -w home/dot_config/claude/rules/agmsg-orchestration.md
make unit-test
make validate-agent-assets
mise x node npm:prettier -- prettier --check home/dot_config/claude/rules/agmsg-orchestration.md home/dot_agents/skills/agmsg-orchestration/SKILL.md
gh pr checks <pr-number>
gh api repos/mryfmo/dotfiles/pulls/<pr-number> --jq '.mergeable_state'
```

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green on the final head, branch up to date.
2. After the final push: `gh pr checks <pr> --watch`; wait (≤15 min) for the Codex Bot review of that head; fix P0/P1 inline findings and repeat; do not resolve threads.
3. Artifacts at the exact expected paths; validation with verbatim outputs, PR number, head SHA.
4. CompactionDB `memory add --kind decision --scope project` with the `[memory:decision]` text from the main checkout; paste command and output.
5. `AGMSG-RESULT v1` via `agmsg-dispatch dotfiles <your identity> claude-remediation-dot wT:p1 "<single line>"` (outside the sandbox). `cost:` line. max_turns=25.

## Revise round 1 (orchestrator, 2026-10-04 02:58Z) — audit findings on e50150df

The task-level audit of e50150df returned `incorrect` with four P2/P3 findings. Two (seat cap counting the pair worker; `gh pr update-branch` merges) are already fixed in e68eb6a7, whose own audit is `correct`. The other two concern the new Worker Playbook step 14 and are still in the head c8d31501. Fix both in one commit on `docs/parallel-execution-rule`, before continuing T68.

1. **`crit stop` misses a daemon started on another branch.** `crit stop` (v0.21.x, `internal/session/stop_cli.go`) stops only the daemon of the current session, resolved from the current branch; a Plan Mode server started before `git switch -c <task-branch>` is left running, which is the common worker case. Step 14 must give the leftover path: when the unsandboxed `pgrep -af '[c]rit _serve'` still lists a server, check that its cwd is your own worktree (`readlink /proc/<pid>/cwd`) and stop that one with `kill <pid>`; never touch a server whose cwd is another seat's checkout; `--all` stays forbidden.
2. **Scope and the sandbox.** Say explicitly that step 14 applies to a Claude worker (Plan Mode and Crit are Claude Code features; a Codex seat under `--ask-for-approval never` never has a plan server), and that the unsandboxed `pgrep`/`readlink`/`kill` are read-only or self-owned-process commands the Claude permission gate allows, so they are not the step-4 boundary.

Allowed files for this round: `home/dot_agents/skills/agmsg-orchestration/SKILL.md` (step 14 only) and `tests/unit/test_agmsg_orchestration_docs.py` only if an existing assertion pins the step-14 text. Keep the rule file unchanged. Then `gh pr update-branch 243` (main is 138e6a72 after #244), wait for CI and the Codex Bot on the final head, do not resolve threads, and send a RESULT line naming the fix commit, the final head and the thread dispositions. Resume T68 afterwards.

### Revise round 1 addendum (orchestrator, 2026-10-04 03:40Z) — portability and the precise stop

The SKILL is the procedure for every worker seat, macOS included, so step 14 must not bake in Linux-only commands.

- `readlink /proc/<pid>/cwd` has no macOS equivalent; use `lsof -a -d cwd -p <pid> -Fn` (both platforms) or state the two forms. BSD `pgrep` has no `-a`; write the check as `pgrep -fl 'crit _serve'` (the `-l` list form) or note both.
- The Plan Mode server is started by the plugin's `crit plan-hook` (PermissionRequest hook on ExitPlanMode). `crit stop [file...]` says files target an exact file-mode session. Verify on a scratch plan file in your worktree whether `crit stop <plan-file>` (or `crit status --json` plus the session's own stop path) stops that server regardless of the current branch; if it does, step 14 names that as the stop command and the `kill <pid>` path is only the last resort after `pgrep` still shows a server whose cwd is your worktree. Paste the scratch run in validation.

### PONG decision 2 (orchestrator, 2026-10-04 04:10Z)

- 4175958710 (step 14 host cleanup needs commands the managed permissions do not allow): agreed. Step 14 keeps only the `pgrep -fl` check inside the worker's allowance; a server that survives `crit stop` is reported in the RESULT as `crit-cleanup-pending=<pid>` and the orchestrator stops it (the worker never escalates). Disposition `fixed:<your commit>`.
- 4175958708 (re-tasking a freed worker can stack the next task on the unaccepted branch): allowed, one sentence in the parallel procedure: the next task starts on a fresh branch from `origin/main`; the previous task's branch stays in the worktree, untouched, for its revise rounds and until its acceptance. Same commit. Then update-branch if `main` moved, CI, Bot, RESULT.

### PONG decision 3 (orchestrator, 2026-10-04 05:00Z)

- 4176005504 (a sandboxed `pgrep` sees only the sandbox pid namespace): agreed; move the host inspection to the orchestrator. The worker reports `plan-mode-used=<worktree>` in its RESULT and runs no `pgrep`; the orchestrator checks and stops a leftover `crit _serve` at acceptance (`make check-regime-boundary` already reports it).
- 4176005501 (SKILL:40 says `gh pr update-branch` only for prose PRs): allowed; reword to every in-flight PR whose base moved, prose or code, before CI, the Bot wait and the gate, because the ruleset's strict up-to-date policy refuses the merge otherwise.
- 4176005508 (routing list omits `home/dot_agents/permgate-policy.yaml` and `executable_permgate`): add both, but cite the model-selection rule rather than the classifier: permgate policy, redaction/secret handling and trust-boundary work run on a Codex `security`-profile worker by that rule, independent of whether the auto-mode classifier happens to allow a Claude seat (it allowed T66). One commit for all three; then update-branch (main is 8922f13b), CI, Bot, RESULT.

## Revise round 2 (orchestrator, 2026-10-04 06:50Z) — task-level audit of 04fd9425 is `incorrect`

Findings (`.orchestration/validation/dotfiles-T88-parallel-execution-rule-a01-audit-04fd942.md.last.md`) and what to do, after the T68 round:

1. **P2, Codex is wrongly excluded from plan-server cleanup.** The managed Codex config enables the Crit plugin's Stop hook (`crit plan-hook --mode codex`, `codex-config-managed.toml:114`), which starts a plan review regardless of the approval policy. Step 14: any worker whose session started a Crit plan review (a Claude seat through Plan Mode's ExitPlanMode hook, a Codex seat through the plugin's Stop hook) reports `plan-mode-used=<worktree>`; delete the sentence that a Codex seat never has a plan server, and keep "Plan Mode" only where it names the Claude feature.
2. **P2, stale session record and pid reuse.** The orchestrator confirms live identity before `kill`: `ps -o args= -p <pid>` must show `crit _serve` and the cwd must match the record; a record whose pid is gone or runs another command is stale and is removed, never killed.
3. **P2, sandbox artifact.** `.orchestration/sandboxes/dotfiles-T88-parallel-execution-rule-a01.md:9` says "No new Crit server", while the validation records the scratch `crit plan` server and the report a stray `crit version` daemon. Record both host operations and their cleanup in the sandbox file.
4. **P3, evidence.** Paste the CompactionDB command as actually run, with the verbatim `--content`, and its UUID in the validation file.

Allowed files: `SKILL.md` step 14 and the T88 artifacts. One commit; `gh pr update-branch 243` if `main` moved; CI; Bot (paginated listing); RESULT naming every thread.

### PONG decision 4 (orchestrator, 2026-10-04 07:00Z) — Codex findings on adfd1fa7, scope extended

- 4176301037 (P1, routing checks only `claude.permissions`): agreed. The routing invariant covers the whole `claude.permissions` and `claude.sandbox` blocks of `agent-config.yaml` (excludedCommands, allowUnsandboxedCommands, writable roots, network), the rendered `claude-settings-managed.json`, `modify_private_settings.json`, and permgate (already listed): a seat never edits the source of its own execution boundary. Allowed files for this round now include `home/dot_config/claude/rules/agmsg-orchestration.md` (that bullet) and the SKILL step 3 sentence; keep the docs test's shared tokens in sync if it pins the sentence.
- 4176301038 (P2, orchestrator cleanup commands would also run sandboxed): agreed; state that the orchestrator runs `pgrep`/`ps`/`kill` outside its sandbox through the permission gate (`dangerouslyDisableSandbox`, answered by the operator or the auto-mode classifier) under its control-plane exemption, as it already does for `agmsg-dispatch` and `herdr-agents --audit`.
- 4176301040 (P2, `--add-worker` seats the manifest kind, not Codex): `not-applicable`. The worker kind is a manifest decision (`worker_kind`), and the current regime seats Claude workers by that manifest; the "resident Codex workers" wording is the legacy phrasing that T83 removes ("kind is the manifest's"). The orchestrator replies on the thread; do not change the procedure.

One commit; `gh pr update-branch 243` (main is f32f33a0 after #246) if the Bot or CI need it; CI; Bot; RESULT naming every thread.

## Revise round 3 (orchestrator, 2026-10-04 09:35Z) — task-level audit of 19becfc5 is `incorrect`

1. **P2, step 14 live-identity check.** Before `kill`, the orchestrator must also confirm the live process's cwd, not only the stored one: `readlink /proc/<pid>/cwd` on Linux (`lsof -a -d cwd -p <pid> -Fn` on macOS) must equal the record's `cwd` and lie under that worker's worktree; a mismatch means the pid was reused and the record is stale (removed, never killed). One or two sentences in step 14's orchestrator bullet.
2. **P3, evidence.** Paste the commands and verbatim output of the stale-record check and removal you performed (`~/.crit/sessions/b8359df9be5d.json`: the `ps -o args= -p <pid>` result, the `readlink` or equivalent, and the `rm`).

One commit for item 1, artifact edit for item 2, `gh pr update-branch 243` if `main` moved, CI, Bot (paginated listing), RESULT. Standing directive applies.

## Revise round 4 (orchestrator, 2026-10-04 10:55Z) — two Codex P2s on 5bef5588, scope extended

- 4176692309 (rule bullet omits permgate): valid; add the one phrase to the rule's routing bullet so the rule and the SKILL list the same sources (`home/dot_agents/permgate-policy.yaml`, `executable_permgate` → Codex `security`-profile worker, per the model-selection rule). Allowed: `home/dot_config/claude/rules/agmsg-orchestration.md` (that bullet) and the docs test token if it pins the list.
- 4176692312 (reusing the worker worktree before acceptance): add one sentence to the parallel procedure: the worker commits and pushes everything before RESULT, so when a `status=revise` arrives it checks the earlier branch out again, does the round, and returns to the newer task's branch; the worktree is reused sequentially and nothing uncommitted is ever left behind. `fixed:<sha>` for both.

One commit; `gh pr update-branch 243` if `main` moved (65915b93 now); CI; Bot (paginated listing); RESULT. The audit of 5bef5588 is running and its findings, if any, follow as an addendum.

### Round 4 addendum (orchestrator, 2026-10-04 11:20Z) — audit of 5bef5588

The task-level audit of 5bef5588 confirms both round-4 items and adds: the validation's "verbatim" transcript replaces the PID lookup command with an ellipsis, and the scratch cleanup and the CI rerun have no pasted command output (`.orchestration/validation/dotfiles-T88-parallel-execution-rule-a01.md:705`). Paste the actual commands and outputs in the same commit's artifact edits. The orchestrator re-collects the PR feedback at the round-4 head.

## Revise round 5 (orchestrator, 2026-10-04 12:00Z) — task-level audit of 0189cfb3 is `incorrect`

1. **P2, shared boundary sources.** Routing the renderer and `codex.sandbox_workspace_write.writable_roots` to "a Codex worker" lets a Codex seat edit sources of its own sandbox. Refine the invariant in both files: a change is routed by the boundary it touches. A change that touches only Claude's boundary (the `claude.*` blocks, `claude-settings-managed.json`, `modify_private_settings.json`, the Claude-rendering parts of the renderer) goes to a Codex seat; one that touches only Codex's boundary (`codex.sandbox_workspace_write`, `codex.approval_policy`, the Codex-rendering parts of the renderer, `codex-config-managed.toml`) goes to a Claude seat; one that touches both, or a shared source the orchestrator cannot split, goes to the operator. The orchestrator decides the kind from the diff the task will produce and records it in the task file.
2. **P2, clean checkpoint before every switch.** The parallel procedure: before switching branches for a revise, the worker commits (or stashes with a named tag it restores afterwards) the newer task's work so the switch never carries edits across; state it in the same sentence as the commit-and-push-before-RESULT rule.
3. **P3, evidence.** Paste the Prettier run on the final head (command and output) in the validation file.

One commit; `gh pr update-branch 243` (main is f2b5c115 now); CI; Bot (paginated listing); RESULT. Standing directive applies.

## Revise round 6 (orchestrator, 2026-10-04 13:10Z) — task-level audit of fb4c9a9a is `incorrect`

1. **P2, permgate routing contradicts the round-5 invariant.** permgate (`home/dot_agents/permgate-policy.yaml`, `executable_permgate`) is the PermissionRequest hook of both seats, so by the boundary rule an edit to it goes to the operator. The model-selection rule assigns the Codex `security`-profile worker to *security audits of pending changes* (`/security-review`, permgate policy, redaction, trust-boundary work), not to editing permgate itself. Correct the sentence in the rule bullet and SKILL step 3: permgate edits → operator; the security-profile Codex worker reviews such a change before the orchestrator accepts it. Keep the docs test token in sync.
2. **P3, evidence.** Paste the paginated Bot poll on the final head (the reviews listing with its head filter, the top-level comments listing, and the reactions query) with their output and the observation window.

One commit; `gh pr update-branch 243` if `main` moved; CI; Bot (paginated listing); RESULT. Standing directive applies.
