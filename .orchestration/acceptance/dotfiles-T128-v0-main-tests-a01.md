# Acceptance: dotfiles-T128-v0-main-tests-a01

- **Decision:** round-1 RESULT WITHDRAWN at 02:4xZ as premature: the Codex Bot reviews no draft PR, so the worker's step-15 Bot wait could not run on 32fe9a36 (the orchestrator's process gap, now Phase 0 of plan 006); the Bot review the orchestrator triggered (02:20Z, posted 02:37Z) raised three P1: 4240003469 completion signal forgeable in-process (the second occurrence of the class after audit round-0 finding 3; a third stops the artifact under S1), 4240003474 control characters in task metadata, 4240003472 PR-rewritable workflow (the design's residual R8, closed by V1c; dispositioned by the orchestrator as not-applicable with that reason). Items 1 and 2 go back to the worker as a resubmission of round 1 with two named selectors; the revise count stays at 1 because no second revise was requested, and the V3a counter must exclude withdrawn RESULTs (orchestration learning for V3a's task text). Design amendment A102 (INV-12 nonce runner and residual; INV-2 CI skip) is in review round 14 with both reviewers at once. Earlier: PENDING round 1 (audit of adcf783b `Verdict: incorrect`, 4 P1 and 3 P2, one `orchestration`; revise round 1 RESULT at 02:19:04Z with head `32fe9a36a6ca67670e54bbcb1c506ca391d9dd32`, 9 commits; `revise.yaml` on the branch names `previous_head` adcf783b and the six selectors; the task.md copy recommitted at `61554db0…`, equal to the revise ACCEPTANCE's `task_sha256`). Sizes at the new head: 334 added outside tests/ and .orchestration/, 438 under tests/, 7 files. Stage 2 for this head: the orchestrator marked the PR ready (02:27Z) and posted `@codex review`, because the Bot reviewed no draft; the sweep and the audit follow that review or the 15-minute cap. PR #317 `feat/main-tests`, final head `adcf783b06d9081280991a3727f8a21c3c61ac85` on main `b896d9bc`; 7 commits, 8 files (7 outside `.orchestration/`), +706/−1 (300 added outside tests/ and .orchestration/, 353 under tests/: within INV-2's caps). Worker `claude-standard-dot-a002` (worker-c, w5:p3). TASK 2026-10-11T00:02:55Z, draft PR 00:10:50Z (8 minutes), RESULT 01:42:31Z.
- **Task.md copy:** `.orchestration/dotfiles-T128-v0-main-tests-a01/task.md` on the branch hashes to `f16cbd9cecdfc3a0…`, equal to the `task_sha256=` of the AGMSG-TASK (first commit `efd8b66b`).
- **Bot wait:** no Codex Bot review within the 15-minute window (`bot: none`); CodeRabbit automatic reviews are disabled on this repository.
- **CI at the head:** 14 of 15 pass; `main-tests` fails by design (this PR adds the harness; main has no contract for the PR's two new test modules, so the design-tier no-contract rule fires on the harness's own first PR). `main-tests` is not a required check yet and is listed after this merge.
- **Exemption declared:** acceptance and final integration; evidence-sync bookkeeping; agmsg control plane.

- **Orchestrator's stated position for the auditor (round 1):** the worker's residual is accepted as the design's scope: code that main's tests import from the PR executes inside the unittest process and can forge a summary; no in-process oracle prevents it; INV-12's harness exists for undeclared regressions and declared-contract drift, and adversarial forgery in a PR is what the design-tier audit from the trusted root is for. The round-1 fixes close the environment paths (pre-harness files, interpreter selection, early exit, exemption keying, renames, empty contracts). Round-0 finding 2's suggested flag (`--isolated`) was wrong; the worker proved it and used an explicit interpreter found from `/`.

<!-- audit-input-boundary -->

## Sweep (`.orchestration/validation/dotfiles-T128-v0-main-tests-a01-pr-feedback.json`, head adcf783b, 7 items)

- `check_run` `main-tests` failure: `not-applicable:bootstrap of the harness itself; the design-tier no-contract rule fires because main holds no contract for the two new test modules; the job becomes meaningful after this merge and is listed as required then (worker report, validation §5: 925 main tests pass, two by-design lines)`.
- `annotation` failure "Process completed with exit code 1" (the same job): `not-applicable:same as the main-tests check run above, the harness's own bootstrap failure`.
- three `annotation` notices on macOS arm64 runner capacity: `not-applicable:GitHub runner capacity notice, not a finding about the change`.
- `issue_comment` CodeRabbit summary comment: `not-applicable:auto-generated summary; CodeRabbit automatic reviews are disabled and it posted no findings`.
- `status` CodeRabbit "Review skipped": `not-applicable:a success status with no content`.

## Orchestrator review

Independent read of the diff: `.orchestration/validation/dotfiles-T128-v0-main-tests-a01-crit.json` (three resolved records), receipt `…-review-receipt.md` (`review_surface: crit-data`, `review_outcome: approved`).

## Audit (`.orchestration/validation/dotfiles-T128-v0-main-tests-a01-audit-adcf783.md`, headless Codex on the audit profile from the clean review worktree at b896d9bc)

Verdict: incorrect. INV-12: violated (`scripts/main-tests.sh:97`, `:119`, `scripts/lib/contract_markers.py:88`). Orchestration findings: 1.

- audit-finding: 1 [P1 implementation test.yaml:108] PR-controlled `github-release.sh` sourced before the harness — revise round 1 item 1 (fixed in the next head).
- audit-finding: 2 [P1 implementation main-tests.sh:32] PR-planted `.venv` can select the interpreter — revise round 1 item 2.
- audit-finding: 3 [P1 implementation main-tests.sh:119] zero exit accepted without test completion — revise round 1 item 3.
- audit-finding: 4 [P1 orchestration task step 1(a)/(b)] exemption keyed on declared test paths, not scripts — the orchestrator's task text was wrong; corrected in the task file's revise section (item 4), implemented by the worker; recorded as the orchestrator's defect, not dispositioned away.
- audit-finding: 5 [P2 implementation main-tests.sh:36] rename detection hides a moved script — revise round 1 item 5.
- audit-finding: 6 [P2 implementation contract_markers.py:88] an empty `@contract` class counts as a contract — revise round 1 item 6.
- audit-finding: 7 [P2 evidence pr-feedback.json] dispositions were empty — `fixed:` by the orchestrator in the JSON before this record (all seven filled).

Revise ACCEPTANCE (INV-3 form, applied by hand until V3c): `previous_head=adcf783b…`, six `check=` selectors named, one per code finding.

cost: rounds 0; amendments 0; questions 0; wall 1 h 40 min (TASK 00:02:55Z to RESULT 01:42:31Z); audits 1; Bot threads 0; CI runs 7 heads; tokens n/a (worker report: cost n/a)
