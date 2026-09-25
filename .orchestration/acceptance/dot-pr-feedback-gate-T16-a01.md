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
