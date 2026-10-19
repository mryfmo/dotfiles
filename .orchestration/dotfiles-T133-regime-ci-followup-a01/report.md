---
task_id: dotfiles-T133-regime-ci-followup-a01
seat: claude-standard-dot-a011
branch: tools/regime-ci-followup-a01
base: 0e496ce7 (origin/main at the branch point; origin/main has since moved to 86ea9884, PR #422, which changes no regime file)
code_head: b65dd4c2 (e0565b47 the task copy and pr-body.md; 6c96e10a red, e6ea7c8d fix and b65dd4c2 review fixes for row ci:39185982423:1)
task_sha256: 65d4b24a390674b303e7dcad6a305be7584ebf49e5f3776f2560dd9ffc14a0a1
---

# Report: dotfiles-T133-regime-ci-followup-a01

- Seat: `claude-standard-dot-a011` in `.claude/worktrees/worker-d`. The branch `tools/regime-ci-followup-a01` was created with `--no-track` from `origin/main` `0e496ce7` (PR #418's merge), after a single-command `git fetch origin main`. The branches of PRs #424, #421 and #410 were left untouched.
- Task file: `65d4b24a…`, copied byte-identical to `.orchestration/dotfiles-T133-regime-ci-followup-a01/task.md`; the task-consistency check passes (validation §1).
- The owned rows are the four under `## Owned by dotfiles-T133-regime-ci-followup-a01` in `.orchestration/acceptance/dotfiles-T133-regime-ci-a02.md`.
  - The first three are text rows, read at dispatch.
  - The fourth, `ci:39185982423:1`, was added at 01:4xZ. The orchestrator's PING (01:45:36Z) asked for it before the first push, and I answered alive before writing it.
  - Only the fourth row changes code: `regime.yml` and the two test modules.
- As the dispatch note asks, the two text rows are realized in this task's own records and Check evidence, never by editing the a02 copy. The PR description is a file the orchestrator applies; the seat ran no `gh pr edit`.

## Row audit:f7d2c48:3 (stale-pr-description)

PR #418 merged as `0e496ce7`, but its title and description still describe the withdrawn a01 design (`pull_request`, a checkout of the head, the head's checker). `.orchestration/dotfiles-T133-regime-ci-followup-a01/pr-body.md` holds the correction for the orchestrator to apply. Its first line, `title: …`, is the `--title`. The body starts at the `## Summary` line.

Both describe only what merged:

- `pull_request_target` runs the base's workflow, checking out the event's base sha (as merged, before row 4) with full history and no persisted credentials. The head is fetched as `refs/pull/<n>/head`, its sha is checked against the event's, and it is never checked out or run.
- The base's verifier and checker run against head content that only git reads.
- The policy is the base's dispatched text when there is one. Otherwise the PR's own copy is a provisional policy, with a warning until `REGIME_REQUIRE_DISPATCHED=1`.
- Every rule, warning and exit code of `regime-ci.py` as merged, the tests as merged, and the one `EXPECTED_PERMISSIONS` entry.

Every claim was checked against `0e496ce7`. The first independent review found several inaccuracies in my draft, and each was corrected:

- an overstated trust boundary (no dispatched text means the PR's own policy);
- missing rules (the `task_copy=` token, the checker-skipped and predecessor warnings, all exit-code causes, caps from the policy text, the reset_of exemption);
- the a01 directory's task copy, which a02's reset removed;
- the `title:` line convention.

This row's test is that comparison of the body with the merged files.

## Row audit:7fad835:1 (threat-row-selector)

The a02 task's `regime-ci.py` row claims head data read through `git show`, the base's checker on a temporary task copy, dispatched-text authentication, precheck binding, allowed files, caps and content-based exemption. Its `closed` selector named only `test_regime_ci_reads_the_head_as_data_and_runs_the_base_verifier`.

The row in the record names three tests, but five close the control. The worker review found three single-line mutants that survive those three tests: the PR's text fed to the checker, the checker run on an unverifiable copy, and the checkout-at-base refusal turned off. Only the last two tests below catch them. The five tests are:

- `tests/unit/test_regime_ci.py::RegimeCiTest::test_regime_ci_reads_the_head_as_data_and_runs_the_base_verifier`: the base verifier and checker run, the head's own programs never do; dispatched-text authentication against a forged dispatched copy; allowed files.
- `…::test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr`: the violation table, one violation per case for task-copy, every precheck form, allowed files, both caps and the checker.
- `…::test_regime_ci_passes_a_records_only_pr_with_no_target`: the content-based no-target exemption.
- `…::test_regime_ci_never_feeds_a_pull_request_s_text_to_the_base_checker`: the checker reads only the base's text, never the PR's copy.
- `…::test_regime_ci_refuses_a_checkout_not_at_the_base_and_a_diff_git_cannot_list`: the verifier and checker that run must be the base's.

Red then green (validation §5): in a scratch copy of the head, one line of `regime-ci.py` is replaced so that a claimed check stops reporting, and the five tests run. The unmutated baseline passes. Each of the nine mutations fails a named test:

| Mutation | What goes red |
| --- | --- |
| base checker | the table's three `checker` cases |
| dispatched-text authentication | the no-PR-text test, the base-verifier test's forged case and the table's `task-copy` case |
| precheck binding | the table's eight `precheck` cases |
| allowed files | the base-verifier test's two violation cases and the table's `allowed-files` case |
| caps | the table's three `caps` cases |
| content-based exemption | the no-target test |
| the PR's text to the checker | the no-PR-text test (dispatched case) |
| the checker on an unverifiable copy | the no-PR-text test (both cases) |
| the checkout-at-base refusal off | the checkout test |

## Row audit:7fad835:2 (evidence-head-mismatch)

The rule now reads: "bootstrap on the code head, with the evidence commit touching only `.orchestration/<task>/`", the rule `regime-ci.py` already applies to precheck.json.

- **The bootstrap.** The local bootstrap (§4) runs the fixed job's command, `uv run --no-config --no-project --with pyyaml python -I scripts/orchestrator/regime-ci.py --base "$(git rev-parse HEAD)" --head "${HEAD_SHA}"`. It runs from an isolated scratch checkout of the base branch's tip `86ea9884` (current `origin/main`), against the code head `b65dd4c2`, whose full sha the block prints.
- **Its result.** It exits 0 with `regime-ci: ok 1 task(s)`. Its six warnings are documented:
  - the diff changes `regime.yml`, so this run executed the base's version;
  - the copy is unverifiable, with no dispatched text at the base;
  - the checker is skipped for that reason;
  - precheck is absent;
  - this follow-up task's `## Check` names no caps of its own (two warnings).
- **Both identities.** The code head is `b65dd4c2`. The final head is the next commit, which adds only `.orchestration/dotfiles-T133-regime-ci-followup-a01/` files and none of the three that regime-ci.py reads there (`task.md`, `precheck.json`, `result.txt`), so the verdict carries over. The RESULT carries `git diff --name-only b65dd4c2 <final head>` and the regime job's own conclusion on the final head (`gh run view`). On this PR that run executes main's workflow as it is now, with the event's base sha, because `pull_request_target` takes the workflow from the base.

## Row ci:39185982423:1 (stale-base-sha)

- **The defect** (PR #420, run 39185982423). `regime.yml` checked out and passed `github.event.pull_request.base.sha`. That recorded value can lag the base branch. On PR #420 it was `740772ef`, the head's fork point, although `main` had been `0e496ce7` for 24 minutes before the run. So it predated the verifier, and the job found no `regime-ci.py`. The worker review read the run: the event was almost certainly a synchronize, so the value does not simply refresh on a push. It also follows the head's fork point, so a PR author could pick an older verifier or policy by basing the head on an old commit of `main`. The run-time tip removes that lever.
- **The fix (`e6ea7c8d`, `regime.yml` only; `b65dd4c2` corrects its comment to the observed lag).**
  - `actions/checkout` takes `ref: refs/heads/${{ github.base_ref }}`, the base branch's tip at run time, which the pull request cannot move. It is an action input, not shell.
  - The verifier gets `--base "$(git rev-parse HEAD)"`, exactly the commit just checked out. The old `BASE_SHA` environment entry is gone.
  - `regime-ci.py` is unchanged. It already diffs `base...head` through the merge base, so a base that moved past the PR's merge base counts only the PR's own changes. It already requires the checkout to be at `--base`.
- **Tests** (red `6c96e10a`, green at the head; validation §3).
  - `tests/unit/test_workflow_security.py::WorkflowSecurityTest::test_the_regime_workflow_takes_its_base_from_the_base_branch_tip_at_run_time` is the red-then-green workflow-shape test. It requires no `pull_request.base.sha`, the `refs/heads/${{ github.base_ref }}` ref and the `--base "$(git rev-parse HEAD)"` form.
  - `tests/unit/test_regime_ci.py::RegimeCiTest::test_regime_ci_accepts_a_base_that_moved_past_the_merge_base` is the regime-ci test. Since `b65dd4c2` it models PR #420. The PR branches from a base with no dispatched text. Then the base branch gains a commit that adds the dispatched text and two unrelated files. The verifier, run against that tip, reports exactly `ok 1 task(s)`, with no warning. That shows the policy is read at `--base`, and that only the PR's own changes count (`base...head`).
    - It passes on the unchanged verifier, so it cannot be red on `6c96e10a`. It is proved by mutation instead (validation §3): reading the dispatched text at the merge base turns it red.
    - The workflow review also turned it red by changing `base...head` to `base..head`.
  - `test_the_regime_workflow_runs_base_code_only` now expects the new ref and command. The original guard rejected the bare word `head` in any step's `with:`, which `refs/heads/` contains. Since `b65dd4c2` the guard strips only `refs/heads/` and then rejects `head`, `merge_commit_sha`, `event.after` and `pull/`. That keeps the old guard's strength, which the narrowed form of `6c96e10a` had lost, for example against `head.ref` and `head.repo.full_name`.

## The Check

The a02 Check, as written and as reworded by row 3:

- `uv run python -m unittest tests.unit.test_regime_ci -v`: 16 tests OK. `uv run python -m unittest tests.unit.test_workflow_security -v`: 9 tests OK (§3). On `6c96e10a` the two workflow-shape tests are red, and the merge-base mutation turns the moved-base test red (§3).
- The local bootstrap (§4), as above.
- `make format`: exit 2 (§7). Its whole-tree shfmt step flags 12 files, all unchanged from `0e496ce7`. ruff (65 files) and prettier are clean.
- Caps (§6): 7 changed lines outside `tests/` and `.orchestration/` (cap 330); 28 under `tests/` (cap 480).
- No local Bats ran.

## Changed files

- `.github/workflows/regime.yml`, `tests/unit/test_regime_ci.py` and `tests/unit/test_workflow_security.py` (row `ci:39185982423:1`).
- `.orchestration/dotfiles-T133-regime-ci-followup-a01/**`: `task.md` and `pr-body.md` at the code head, then the evidence (this report, `validation.md`, `sandbox.md`, `learning.md`, the worker review files) and the corrected `pr-body.md`.
- `scripts/orchestrator/regime-ci.py` is unchanged.

## Evidence, review, cost

- Evidence in `.orchestration/dotfiles-T133-regime-ci-followup-a01/`.
- Worker review: `dotfiles-T133-regime-ci-followup-a01-worker-crit.json` and `dotfiles-T133-regime-ci-followup-a01-worker-review-receipt.md`. There were two read-only rounds by fresh subagents. Both worker-side fix rounds this task allows under C-61 are used.
  - **Round 1**, on `pr-body.md` at `e0565b47` and the draft validation: `Verdict: incorrect`. It found four P2 and eleven P3, all fixed in the records: the corrected PR body, the five-test selector with nine mutations, the printed head sha, and the two identities.
  - **Round 2**, on `e0565b47..e6ea7c8d`: `Verdict: correct`. Its three P3 are fixed in `b65dd4c2`.
  - Round 2's P2 outside the changeset is not applicable. It said a closing test did not exist, but `test_regime_ci_passes_a_records_only_pr_with_no_target` is at `tests/unit/test_regime_ci.py:396` at `e6ea7c8d`, and §5 runs it.
- precheck: pending-411 (`scripts/orchestrator/result-precheck.sh` is not on main).
- No Understand-Anything hook prompt fired, and no Plan Mode was used.
- cost: n/a (the runtime exposes no token or cost figure to the seat).
