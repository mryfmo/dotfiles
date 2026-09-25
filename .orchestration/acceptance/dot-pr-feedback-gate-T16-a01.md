# AGMSG-ACCEPTANCE dot-pr-feedback-gate-T16-a01 (in progress)

## Pre-RESULT orchestrator review of PR #182 at a6bd283 (12:4xZ, independent context, orchestrator-review worktree)
Required before acceptance:
1. Self-application missing at this head: no `.orchestration/validation/dot-pr-feedback-gate-T16-a01-pr-feedback.json`, no `@coderabbitai full review` yet (rate-limited until ~12:54Z), `reviews: []`. Expected per task; must land before RESULT.
2. CI red on head: `test (ubuntu-latest, client)` statusline smoke `TimeoutExpired` 5 s (main passes the same step). Disposition in the JSON as `not-applicable:<T18 statusline timeout root cause>` and rerun; do not treat as fixed.
3. `scripts/require-crit-review.py:295-339` never binds evidence to the head: with `--base`, require `data["head_sha"] == git rev-parse HEAD` (and `pr` match when derivable), else the "final head" rule is unenforced.
Recommended in the same pass:
4. Strengthened-reason check applies only to `level == failure`; extend to check_run conclusions `cancelled|timed_out|action_required|in_progress` so a WIP run cannot be dispositioned away.
5. `Makefile:167-169` and `crit-review.md` still present `make require-crit-review` as the final gate without `--base`/`PR_FEEDBACK_EVIDENCE`; make the make target accept `BASE=` and forward `PR_FEEDBACK_EVIDENCE`, and align the rule text so there is one gate invocation.
Optional: 6. `coderabbit-trigger.yml:38` pipefail+grep SIGPIPE → duplicate trigger risk; use `--jq ... | any` or a temp file. 7. no parity guard for pr-integration.md ↔ Codex mirror ↔ symlink tmpl. 8. test fixture uses a "tracked in T18" deferral as an accepted N/A example — pick a genuine N/A. 9. `.coderabbit.yaml` not schema-validated (parse only, as approved).
Verified OK: pr-feedback.py sources/pagination/auth/schema/tests (48+30 subtests, no network), rule text + Codex mirror + skills, rate-limit citation, workflow safety (`pull_request_target` without checkout, top-level permissions, dedupe, no synchronize), `.coderabbit.yaml` keys valid against schema.v2, guard backward compatibility, README ruleset guidance, scope within allowed files.

## CodeRabbit full review on 728c8ad (13:04:53Z, id 5317960699, CHANGES_REQUESTED, 2 actionable — both valid)
- `coderabbit-trigger.yml:39-41` Security (CWE-807, Major): the dedupe marker must count only when the comment author is the workflow's own bot and the body matches the request format; otherwise anyone can post the marker text to suppress the review request. Expected disposition: fixed in the worker's next push.
- Same lines (Functional, Major): add a `concurrency` group keyed by PR number (no cancel-in-progress) so parallel runs cannot both miss the marker and double-post (each post spends the hourly review).
- CI on 728c8ad: 12 pass (statusline smoke rerun green; disposition must still cite T18).

## Orchestrator verification of 35bb170 (13:1xZ, orchestrator-review worktree)
- Both CodeRabbit items fixed at the root: marker counts only when `.user.login == "github-actions[bot]"` and the body starts with the request command and contains the head-sha marker; `gh api --paginate --jq any(...)` captured into a variable (no grep pipe, closes the SIGPIPE nit too); `concurrency: group: coderabbit-trigger-<pr>`, `cancel-in-progress: false`.
- `test_workflow_security`, `test_require_crit_review`, `test_pr_feedback`: OK; validator ok. CI on 35bb170: 6 pass / 6 pending at check time.
- Worker plan: final-head CodeRabbit full review at 13:57Z (hourly window), then sweep + dispositions + RESULT.

## CodeRabbit final review on 35bb170 (14:09:21Z, id 5318666589, CHANGES_REQUESTED, 2 minor, both valid)
- `coderabbit-trigger.yml:42-43`: re-fetch the PR head sha immediately before posting and restart the marker search if it moved (avoids requesting a review for a stale head after the concurrency wait).
- `require-crit-review.py:350-361`: `fixed:<commit>` must reference a commit within `base..HEAD` (exists, ancestor of HEAD, not ancestor of base), not any object in the repo.
- Worker silent 13:09Z → 21:05Z; orchestrator PING sent 21:05Z; commit ae28b6b appeared at 21:05:45Z.

## 21:0xZ — verification of 96e3771 + ae28b6b and convergence rule
- `commit_in_range` (merge-base --is-ancestor against head and base) correct; `test_require_crit_review` + `test_workflow_security` OK in the orchestrator review worktree; CI running on ae28b6b; worker requested the full review at 21:06Z.
- Convergence rule issued (to be written into pr-integration.md by the worker): when a full review on head N yields only Minor/nit items, fix them in one commit that changes nothing else, reply on each thread, and treat CodeRabbit's thread acknowledgement/resolution on that commit as completion; a new full review is required only when the follow-up commit changes more than the cited fixes. Rationale: 1 review/hour plan; each cycle so far surfaced 2 smaller items.

## 21:2xZ — CodeRabbit full review on ae28b6b: 1 Major + 1 Minor, both valid, fixed in f9395be; rule text 9c7de78
- Major: `.coderabbit.yaml` left `auto_review.enabled` at its default (true), so every open/push would spend an hourly review and collide with the explicit-trigger design → set to false with a rationale comment. Minor: the pr-feedback evidence JSON counted toward the guard's broad-diff size → excluded via IGNORED_PREFIXES.
- Convergence rule written into pr-integration.md exactly as issued (Major ⇒ another full review). Because this cycle contained a Major item, the orchestrator declined the worker's "converged?" shortcut; a final full review on 9c7de78 is scheduled for 22:08Z (hourly window). Verified in the orchestrator review worktree: tests OK, validator ok, CI running.

## 22:3xZ — CodeRabbit full review on 9c7de78: 1 Major + 2 Minor, fixed in 59e5237 (orchestrator-verified)
- Major: the trigger treated "request posted" as "reviewed", so a rate-limited head could never be re-requested → now skips only when a `coderabbitai[bot]` review exists for the head's `commit_id`; automatic events dedupe on the workflow's own marker, manual runs and the `review-requested` label always re-request. Minor: README gate conditions completed; nested review-thread comment pagination in pr-feedback.py.
- Verified in the orchestrator review worktree: workflow logic as described, `test_workflow_security`/`test_pr_feedback`/`test_require_crit_review` OK, validator ok, CI running. Per the convergence rule (Major present) the worker scheduled another full review (~23:08Z). Cycle count on this PR: 5.
