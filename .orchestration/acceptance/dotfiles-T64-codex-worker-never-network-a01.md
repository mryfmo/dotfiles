# Acceptance: dotfiles-T64-codex-worker-never-network-a01

- **Decision:** ACCEPTED. PR #236 squash-merged to `main` as `a575b3cc` (final head `d950ac69ac77b7478dc506272889800695390eff`, base `c6de5156`). Merged without `--delete-branch` while worker-c holds `chore/codex-worker-never-network`.
- **Worker:** `claude-standard-dot-a005` (worker-c). task_rev `41d4fdf3…` matched. Parallel wave 1 with T65 (a007) and T70 (a006).
- **Exemption declared:** acceptance and final integration; the orchestrator mutated no repository code.
- **Plan reference:** Phase 1, dotfiles-T64 (principle 1, Codex worker seat: never + in-sandbox network).

## What was accepted (4 files, +75/−33; 2 commits)

- `herdr-agents`: both codex worker launch paths (`write_spawn_options`, `start_worker_agent`) add `--ask-for-approval never` and `-c sandbox_workspace_write.network_access=true`; header/usage/comments and the shallow-clone stderr describe failure instead of escalation. 11 argv pins + 2 spawn-options pins updated, one explicit spawn-options assertion added.
- README (Codex worker paragraph) and SKILL.md:46: no escalation prompt for a worker; out-of-sandbox or execpolicy-forbidden actions fail and are reported as blocked PONGs; network switch is boolean with no domain allowlist configured here (Codex's network proxy domain policy exists but is unused); permgate PermissionRequest dead for the worker seat, live interactively; interactive sessions keep the base config.

## Orchestrator review

- Diff read in full; VERIFY (a)–(d) accepted from the rollouts and deterministic `codex sandbox` probes; caveat recorded: `codex exec` forces `never`, so the flag's effect was shown via `codex debug prompt-input` on the interactive config path.
- Deviations accepted: `grep -c 'ask-for-approval never'` = 6 (4 doc lines, not reworded to fit); the "no domain allowlist" wording narrowed in d950ac69.

## Audit

| commit | verdict | findings → disposition |
|---|---|---|
| b9c1aefa | incorrect | P1: a networked worker can merge via `gh api … /merge` with the shared credentials → **not-applicable to this task**: the root cause is the shared GitHub identity (the gap already existed for Claude workers), fixed by role-separated identities + `required_approving_review_count: 1` (operator decision 2026-10-04; dotfiles-T90, security-profile Codex worker). P2: rule agmsg-orchestration.md:17 still describes the escalation → routed to dotfiles-T88. P3: domain-allowlist claim inaccurate → fixed:d950ac69 |
| d950ac69 | correct | — |

## Codex Bot / sweep

- No inline thread; thumbs-up on the final head. Sweep (head d950ac69): 5 items, 0 failure/warning, all dispositioned.

## Gate

- `.claude/worktrees/orchestrator-review` at d950ac69 with evidence copies: `BASE=origin/main PR_FEEDBACK_EVIDENCE=… AGENT_REVIEWED=1 REVIEW_EVIDENCE=… make require-crit-review` exit 0; copies removed.

## CompactionDB

- Worker decision `cd40adce-50c0-49f2-8016-6ca52883df0a`; cited.

## Follow-ups routed

- dotfiles-T90 (identity separation), dotfiles-T88 (rule:17, worker closes crit servers), regime-boundary tests reading the host `pgrep` (test isolation; fold into T77), evaluate the Codex network proxy for a GitHub-only allowlist on the worker seat (plan follow-up).

## Operator follow-up

- `make update` on each clone deploys T60–T64 (stub removal, formatters and hook, execpolicy rules, the new launcher). Then `herdr-agents --restart-worker` at a task boundary so the pair worker picks up the new launch arguments, and `codex execpolicy check --rules ~/.codex/rules/default.rules -- gh pr merge 1` → `forbidden`. Until T90 lands, Codex workers are used only for T62.
