# Acceptance: dotfiles-T102-add-worker-credential-notice-a01

- **Decision:** ACCEPTED. PR #285 squash-merged to `main` as `0f18bce9`; head `015929c8`. Gate passed at the head in the orchestrator-review worktree with the PR-feedback, audit (`correct`) and crit evidence (`BASE=origin/main PR_FEEDBACK_EVIDENCE=… AUDIT_EVIDENCE=… AGENT_REVIEWED=1 REVIEW_EVIDENCE=… make require-crit-review` rc=0, 2026-10-05 17:29Z; `notice: GitHub role gate inactive: worker hosts.yml missing`). RESULT received 17:17Z; CI 12 successful checks, `mergeStateStatus=CLEAN`.
- **Worker:** `codex-standard-dot-a006` (worker-e, wT:pC, `standard` profile). task_rev verified at dispatch (17:04Z).
- **Exemption declared:** acceptance and final integration; evidence-sync bookkeeping. **Deviation (disclosed in the task file up front):** the orchestrator opened PR #285 on the worker's SSH-pushed branch because the post-T90 seat has no provisioned worker gh credential (the very condition this change reports); the worker ran every local check and no `gh` call; the orchestrator runs `gh pr checks --watch`, the Bot wait and the sweep. Same handling as T101 (#283); ends when the operator provisions `~/.config/gh-worker/hosts.yml`.
- **Plan reference:** follow-up noted at the a006 seating of 2026-10-05 11:25Z (first post-T90 seat learned of the missing credential only from its own `gh auth status`).

## What is under acceptance (PR #285, head `015929c8`, one commit on main aeb025e8; 3 files, +76/−1)

- `herdr-agents`: `notice_missing_worker_github_credential()` prints one stderr line when `$(worker_github_config_dir)/hosts.yml` is absent, called once in `--add-worker` before `write_spawn_options`, and once on the shared full/`--restart-worker` path after the `--attach` exit; exit status and stdout unchanged; no credential content read.
- `tests/unit/test_herdr_agents.py`: four tests (notice once in each of the three modes; silent with a configured `~/`-expanded `hosts.yml` present).
- README operator provisioning paragraph: one sentence.

## Audit / sweep / gate

| scope | verdict |
|---|---|
| task-level, head 015929c8 | correct (no findings; the auditor confirmed the allowed-file scope, both call sites before seating, presence-only check without credential reads, the digest, commit, diff stats and the 234/881 test counts; Bash syntax, ShellCheck and whitespace checks passed; Bot coverage none, quota) |

- Sweep (head 015929c8): `.orchestration/validation/dotfiles-T102-add-worker-credential-notice-a01-pr-feedback.json`, 6 items, all `not-applicable` (Codex quota notice, CodeRabbit summary comment and status, 3 macOS capacity notices). Bot coverage: none (Codex quota notice at 17:15:49Z ended the wait). Crit evidence `…-crit.json` and receipt `…-review-receipt.md` (orchestrator re-derivation incl. the mode-exit map: bootstrap/add/remove/audit/attach exit before the shared call); worker-side `…-worker-crit.json` / `…-worker-review-receipt.md` copied from worker-e.

## CompactionDB

- Worker decision: none (Codex seat). Orchestrator consolidation `89301e76-94ba-41ae-82f8-c70564a7ea71`.
