# Report: dotfiles-T128-ci-skip-orchestration-a01

- Seat: `claude-standard-dot-a003` in `.claude/worktrees/worker-f`, branch `feat/ci-skip-orchestration` from `origin/main` `b896d9bc`, PR #320. Plan 006 Phase A5 (INV-2's CI clause), with Amendment 1.
- Task file sha256 `6dd3d682…` checked against the TASK and copied byte-identical in `be935742`; Amendment 1's sha256 `8e9c23da…` checked and re-copied byte-identical in `f7393ee1`. Content commit `9fcd2b04`.

## What changed (`9fcd2b04`)

1. `.github/workflows/remote.yaml`: `public-bootstrap` and `private-bootstrap` each decide `should_run` in their own step `decide`, right after the checkout (now `fetch-depth: 0`, still `persist-credentials: false`). On `pull_request` the step diffs `origin/<base>...<head>` with `--no-renames` (both sides of a rename are listed) and writes `false` only when no path is outside `.orchestration/`; an empty diff runs the bootstrap. Every other event writes `true` before any git call. The bootstrap step (public) and the deploy-key and bootstrap steps (private, prefixed to their existing secret gates) carry `steps.decide.outputs.should_run == 'true'`; a notice step reports the skip. Job names and matrices are unchanged; no `needs`, no job-level `if`.
2. `.github/workflows/test.yaml`: the `changes` job is gone and `test` no longer `needs` it. Its filter script moved, unchanged but for its comment, into the `test` job's own step `decide` after the checkout (now `fetch-depth: 0`); every `needs.changes.outputs.*` read became `steps.decide.outputs.*`. Lines 1–12 and the ubuntu-26.04 canary's job-level `continue-on-error` are unchanged.
3. `tests/unit/test_workflow_orchestration_skip.py` (stdlib only; PyYAML is not in the unit-test environment): the context names equal `REQUIRED_CONTEXTS` (premise 1's seven); no required context's job has a job-level `if` or `needs`, and no `changes` job is left; each deciding job's step `decide` follows a full-history, credential-free checkout and has no `continue-on-error` and no `if`; every heavy step carries its job's gate; both bootstrap jobs run the same script; a `main-tests` job, when present, decides in itself. The decision scripts are extracted from the workflows and run against a scratch repository: `push`, `schedule`, `workflow_dispatch` → `true`; `pull_request` with an `.orchestration`-only diff → `false`, a mixed diff, a rename out of `home/`, a deletion outside `.orchestration/`, an empty diff → `true`, a deletion inside → `false`; test.yaml's decision → `should_test=false` for `.orchestration` only, `true` for `home/`.

## Threat table (the completion condition)

| Row | Disposition | Where |
|---|---|---|
| The PR edits the workflow files themselves | residual, as the task states | `tests/unit/test_workflow_security.py` passes unchanged (validation §1) |
| The decision step misclassifies a diff | closed | `DecisionTest.test_a_pull_request_skips_the_bootstrap_only_for_an_orchestration_only_diff` (mixed, pure, renamed, deleted in and out, empty), `DecisionTest.test_the_unit_test_decision_skips_an_orchestration_only_diff` |
| A required job is skipped (job-level `if`, or `needs`) | closed | `RequiredContextsTest.test_no_required_contexts_job_has_a_job_level_if_or_needs`, `…test_no_job_is_left_for_a_required_job_to_need`, `…test_the_required_contexts_are_the_workflows_jobs` |
| The decision step itself fails | closed | `DecisionStepTest.test_each_deciding_job_decides_after_its_checkout_and_fails_closed`, `…test_every_heavy_step_carries_its_jobs_decision` |
| Push and schedule have no PR range | closed | `DecisionTest.test_every_event_but_pull_request_bootstraps` |

Each closing test fails when its rule is broken: 14 of 14 mutations in a `git archive HEAD` copy (validation §3).

## CI and Bot (head `9fcd2b04`)

- CI: 13 of 13 pass, the seven required contexts among them; on this mixed diff the decision steps succeeded and the bootstrap and unit-test steps ran (validation §5). `private-bootstrap`'s deploy-key and bootstrap steps were skipped by their existing secret gate, as on PR 316 (≈12 s per leg there too).
- Bot round 1: the connector summary shows Code Review ✅ Completed at 05:52:35Z and Security Review ✅ Completed at 05:55:43Z on `9fcd2b0`, with 👍 at 05:55Z; no review object and no review comment. No fix round.
- The evidence head's CI and Bot wait are in the RESULT and the main-checkout copy of this report.

## Notes for the orchestrator

- Outside `allowed_files`, stale after this PR: SKILL.md line 71 says "the `changes` job skips the test matrix for an `.orchestration`-only diff, and the ruleset accepts the resulting `skipped` required checks". That is the fail-open mechanism this PR removes; the checks now report success from a completed job.
- The step `decide` now runs on every matrix leg, macOS included, so the remote.yaml script avoids `mapfile` and empty-array expansion (bash 3.2).
- A201's completion condition (≤ 10 minutes on the next `.orchestration`-only PR) is the orchestrator's post-merge check; this PR's own diff is mixed and ran the full matrix.
- Understand-Anything hook: did not fire. plan-mode-used: no.

## CompactionDB

`memory add` printed `a48481dc-7c94-40a9-9300-b01cafb77a48` (validation §6).

cost: n/a
