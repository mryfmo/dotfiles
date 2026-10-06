# Acceptance: dotfiles-T109-claude-worker-merge-deny-a01

- **Decision:** ACCEPTED. PR #295 squash-merged to `main` as `05ff683b` (2026-10-06 06:37Z) with `gh pr merge --squash --match-head-commit c856e512…`; head `c856e512`. Gate passed at the head in the orchestrator-review worktree with the PR-feedback, audit (`correct`) and crit evidence (`BASE=origin/main … make require-crit-review` rc=0, 06:36Z). RESULT received 06:31Z.
- **Worker:** `codex-standard-dot-a006` (worker-e, wT:pE, `standard` profile; seated after the T108 deploy, so it carries this machine's gh login). task_rev verified at dispatch (05:44Z) and at PONG decision 1 (worklog write waived).
- **Exemption declared:** acceptance and final integration; evidence-sync bookkeeping (artifact copies from worker-e).
- **Design source:** `.orchestration/validation/github-auth-design-2026-10-05.md` §16, step 2 of decision A. Routed to a Codex seat because the change writes Claude's permission policy for worker seats.

## What is under acceptance (PR #295, head `c856e512`; 5 files, +106/−9)

- `herdr-agents` `ensure_worker_merge_denials()`: for a Claude worker seated in a worktree (pair seat, `--restart-worker`, `--add-worker`), merges the four deny rules (`Bash(gh pr merge:*)`, `Bash(gh api -X PUT:*)`, `Bash(gh api --method PUT:*)`, `Bash(gh api graphql:*)`) into `<worktree>/.claude/settings.local.json`, idempotently, keeping hooks and other permissions; never for Codex seats or a main checkout, so the orchestrator's user-level settings are untouched.
- README and SKILL step 10.5: the mechanism, deny-rule precedence, and the flag-after-path limit that leaves the integration gate authoritative; docs test tokens.
- Tests: first seat adds the rules, second seat byte-identical, unrelated keys kept, Codex seat untouched; 913 unit tests OK; CI 13 checks.

## Audit / sweep / gate

| scope | verdict |
|---|---|
| task-level, head c856e512 | correct (no findings; the auditor confirmed the allowed files, the seven artifacts, the seat paths, idempotence and preservation of unrelated settings, the exclusion of Codex seats and main checkouts, the documentation against the Claude permission docs, and the 12 successful checks; it ran syntax, ShellCheck, 17 documentation tests and in-memory checks of the jq expression) |

- Sweep (head c856e512): `.orchestration/validation/dotfiles-T109-claude-worker-merge-deny-a01-pr-feedback.json`, 7 items, all `not-applicable` (Codex quota notice; Codex review summary, security review completed with no findings; CodeRabbit summary comment and status; macOS capacity notices). Bot coverage: Codex security review, no findings; no review threads. Crit evidence `…-crit.json` / `…-review-receipt.md`; worker-side `…-worker-crit.json` / `…-worker-review-receipt.md` copied from worker-e.

## Deploy

- `make update` in the canonical clone at 05ff683b (06:37Z): rc=0; the deployed `herdr-agents` carries `ensure_worker_merge_denials`.
- Live verification: worker-c's `.claude/settings.local.json` had no `permissions` key; `herdr-agents --restart-worker` re-seated the pair worker (a005, pane wT:p2) and the file now holds `permissions.deny = [Bash(gh pr merge:*), Bash(gh api -X PUT:*), Bash(gh api --method PUT:*), Bash(gh api graphql:*)]` next to the agmsg `hooks`; the main checkout's and the user-level settings are unchanged.

## CompactionDB

- Worker decision: none (Codex seat). Orchestrator consolidation `283e3ea5-25ae-4c43-b63d-458c6f95dd67`.
