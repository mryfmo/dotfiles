# Acceptance: dotfiles-T101-codex-worker-profile-default-a01

- **Decision:** ACCEPTED. PR #283 squash-merged to `main` as `aeb025e8`; head `462bbb1d`. Gate passed at the head in the orchestrator-review worktree with the PR-feedback, audit (`incorrect`, one evidence-only disposition below) and crit evidence (`BASE=origin/main … AUDIT_DISPOSITIONS=… make require-crit-review` rc=0, 2026-10-05 12:05Z).
- **Worker:** `codex-standard-dot-a006` (worker-e, wT:pC, `standard` profile). task_rev verified at dispatch (11:40Z, after a re-seat: the first seat answered the linkage PING but accepted no later wake).
- **Exemption declared:** acceptance and final integration; evidence-sync bookkeeping. **Deviation:** the orchestrator opened PR #283 on the worker's pushed branch because the post-T90 seat has no provisioned worker gh credential (`GH_CONFIG_DIR=~/.config/gh-worker`, `hosts.yml` missing); the worker pushed over SSH and ran every local check; the orchestrator ran `gh pr checks --watch`, the Bot wait and the sweep for it. The gate's author-vs-merger role check is inactive until provisioning, so the orchestrator-authored PR is accepted this once; after provisioning, workers open their own PRs again.
- **Plan reference:** lesson of the 2026-10-05 usage review (worker tokens on the `security` profile).

## What is under acceptance (PR #283, head `462bbb1d`, one commit on main b277a45c; 3 files, +17/−2)

- SKILL "Parallel workers": Codex ordinary tasks `--profile standard`; `--profile security` only for trust-boundary tasks with a `codex-security-dot-aNNN` identity. Orchestrator Playbook step 3: the task file records kind and chosen worker profile.
- README: one sentence with the same default.
- `tests/unit/test_agmsg_orchestration_docs.py`: `test_codex_worker_profile_defaults_to_standard`.

## Audit / sweep / gate

| scope | verdict |
|---|---|
| task-level, head 462bbb1d | incorrect (1 evidence-reality finding; no implementation, security or regression defect; the auditor ran the 16 documentation tests and confirmed the new test fails five ways against the base prose) → disposition below |

audit-finding: 1 the validation file named commit 462bbb1d only in prose, with no pasted command output containing it → not-applicable:evidence-only; the worker appended the verbatim `git log -1` and `git rev-parse HEAD` output showing 462bbb1d641b641c7e522de16aa0e239e296606e to its validation file in worker-e (PONG decision 3, confirmed by its corrected PONG at 12:02Z) and the orchestrator re-copied and re-read it; the validation file is an untracked artifact outside the PR diff, so the head does not move

- Sweep (head 462bbb1d): `.orchestration/validation/dotfiles-T101-codex-worker-profile-default-a01-pr-feedback.json`, 6 items, all `not-applicable` (Codex quota notice, CodeRabbit summary and status, 3 macOS capacity notices). Bot coverage: none (quota). Crit evidence `…-crit.json` and receipt `…-review-receipt.md`; worker-side `…-worker-crit.json` / `…-worker-review-receipt.md` copied from worker-e.

## CompactionDB

- Worker decision: none (Codex seat). Orchestrator consolidation `0a886102-61db-4391-9ef5-0bdaf7e725a1`.
