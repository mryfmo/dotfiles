---
task_id: dotfiles-T133-regime-ci-a01
seat: claude-standard-dot-a008
branch: tools/regime-ci-a01
base: de3b73cc
pr: 418
test_commit: 159af0ca
feature_commit: 811dd3ce
review_test_commit: 7311f004
review_fix_commit: a1c90c78
rereview_test_commit: 9a787b13
task_sha256: da3965e6b10fd3fe743f2aee8849ee67b1cc1d55924357407485f7ca41610fbf
precheck: pending-411
---

# Report: dotfiles-T133-regime-ci-a01

- Seat: `claude-standard-dot-a008` in `.claude/worktrees/worker-f`. AGMSG-TASK arrived at 2026-10-18T13:15:33Z with `task_sha256=da3965e6…`.
  - The dispatched file and the branch copy `task.md` match it byte for byte (validation §1), and the task-consistency check passes on it (§1a).
  - Premises 1 to 4 replay on `origin/main` (§2), and premise 5 through gh (§11).
- Branch: a fresh `tools/regime-ci-a01` (`git switch -c … --no-track origin/main` at `de3b73cc`). PR #416's branch is untouched.

## What changed

1. `.github/workflows/regime.yml` (Files item 1):
   - Trigger and concurrency: `on: pull_request` (opened, synchronize, reopened, ready_for_review), and `concurrency: regime-pr-<number>` with `cancel-in-progress: true`.
   - One job `regime` on `ubuntu-24.04`:
     - `actions/checkout@3d3c42e5…` with `fetch-depth: 0`, `ref: <PR head sha>` and `persist-credentials: false`;
     - `astral-sh/setup-uv@c18668ad…` with `enable-cache: false`, as test.yaml does;
     - then `uv run --no-config --no-project --with pyyaml python -I scripts/orchestrator/regime-ci.py --base "origin/${BASE_REF}" --head "${HEAD_SHA}"`.
   - Additions beyond item 1, each a hardening:
     - `permissions: contents: read` and `persist-credentials: false`, in the other workflows' form;
     - the base ref and head sha passed through `env`, so no expression is spliced into the shell line;
     - `--no-config`, so a `uv.toml`, `pyproject.toml` or `.python-version` in the checkout cannot steer uv;
     - `timeout-minutes: 10`.
2. `scripts/orchestrator/regime-ci.py` (Files item 2) takes the tasks whose `.orchestration/<t>/` the diff `<base>...<head>` touches and that carry `task.md` at `<head>`.
   - Output, per task: one `regime-ci: <t>: <rule>: <detail>` line per violation, and `regime-ci: warning: <t>: <detail>` lines.
     - The rules are `task-id`, `checker`, `task-copy`, `precheck`, `allowed-files` and `caps`, plus `front-matter` for an unreadable copy and `git` for a failed git read.
   - Exit: 1 on any violation, 2 when a git listing fails, else `regime-ci: ok <n> task(s)`.
   - What it reads and runs:
     - Data is read with `git show <head>:<path>`, `yaml.safe_load` and `json`.
     - The only program run from the checkout is the tracked checker, with `--no-config`.
     - The checkout must be at `<head>` (a `checkout` refusal otherwise), so the checker reads only the head's files.
   - A diff that changes the checker, regime-ci.py or regime.yml prints a warning.
3. `tests/unit/test_regime_ci.py` (Files item 3): the four named tests and four more (below). The fixtures are temporary repositories with a base holding the dispatched text and the tracked checker, a code commit, and an evidence commit.
   - `test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr` runs one subtest per rule branch, each giving exactly one violation line with its phrase.
   - The four more tests:
     - `…_reports_a_copy_whose_task_id_is_not_its_directory`
     - `…_runs_the_checker_without_the_checkout_s_uv_config`
     - `…_checks_the_copy_against_result_txt_without_dispatched_text`
     - `…_refuses_a_checkout_not_at_the_head_and_a_diff_git_cannot_list`

## Design corrections and readings (each stated for the orchestrator)

- **The head sha, not `github.sha`** (as the task states). `github.sha` is the merge commit on `pull_request` events, so the checkout and `--head` take `github.event.pull_request.head.sha`.
- **The precheck binding, rule (c).**
  - A committed `precheck.json` cannot name the commit that adds it. "Its `head` equals `<head>`" would therefore fail every PR that carries one: PR #411's records name the code commit `56a734cd`, and its head `4ed1b27a` adds only evidence on top.
  - The rule is the evidence-only ancestor rule of verdict.sh condition 1. The head is a 40-hex id equal to `<head>`, or an ancestor of `<head>` such that every path in `git diff --name-only <precheck head> <head>` is under `.orchestration/<t>/`.
  - The sha256 check against result.txt's `precheck=` is unchanged.
  - Consequence: a `gh pr update-branch` turns `regime` red until a new precheck.json names a head the merge descends from. That matches the design's precheck-head-equals-head intent, and the orchestrator's step 10 reruns the precheck after update-branch anyway.
- **C1 on copies.** The checker's C1 compares `task_id` with the file name, which is `task` for every copy. regime-ci drops the checker's `C1 task_id … != file task` line and checks instead that the copy's `task_id` equals its directory (`task-id`). Every other checker line is reported verbatim.
- **The checker's result counts only with its verdict line** (`task.md: OK` with exit 0, `task.md: FAIL` with exit 1). A crash, which also exits 1, is a violation with its output.
- **No task copy.** A diff with no task copy and with a path outside `.orchestration/` is a violation (`no target: …`, exit 1). Files item 2 names only the records-only pass, and a code change without a task is the regime's own failure. A head branch under `orchestration/` passes as records-only whatever it changes (`GITHUB_HEAD_REF`, as item 2 asks).
- **Target detection.** Item 2's "the task directories whose task.md is in that list or exists at <head>" is read as the directories of the changed `.orchestration/<t>/` paths that carry `task.md` at `<head>`. Otherwise every old task directory with a copy would be a target of every PR.

## re-plan

`re-plan: fail-open-on-unvalidated-input -> after the worker review of 811dd3ce (a crashing checker passed as clean because a crash also exits 1, an unparsed cap sentence and an empty git listing passed silently, a symbolic precheck head resolved to the head: four findings of one class) every rule was re-read against one rule, that it is ok only on a positive check of parsed, validated input, the lesson of T133 verdict-audit-pool a01's re-plan; the specification reading changed where a missing or unparseable input had passed (the checker's verdict line with its exit code, a warning per missing cap, a 40-hex precheck head), the design moved every git listing behind one helper that raises on a nonzero exit (exit 2) and replaced the PR-path pathspec with an unrestricted diff, the implementation added one subtest per rule branch with its phrase, and the verification ran each new case against the scripts before the fix (validation §4a) and nineteen single-rule mutants (§5a).`

## Worker review (three rounds; the record and the receipt name every finding)

An independent read-only reviewer did the review: a fresh general-purpose subagent of this seat, given the task file, the threat table and the commit range, not my conclusions.

1. Round 1 on `de3b73cc..811dd3ce` returned `Verdict: incorrect`: one P1, four P2 and seven P3.
   - The P1: a checker crash passed as clean.
   - Most P2 and P3 were fixed in a1c90c78 after the re-plan above, with tests in 7311f004 that are red at 69a3128f (§4a).
   - P2-2, a PR with two task directories, is the spec gap below.
   - P3-6 (the `orchestration/` head) is what the spec requires.
   - P3-5 was fixed earlier, in 69a3128f.
2. Round 2 on `811dd3ce..a1c90c78`, the same reviewer with its context kept, returned `Verdict: correct`. Every fix claim held, and it found no new fail-open path. Its three surviving mutants are closed in 9a787b13: a prechecked change reverted to base, a verdict line with the wrong exit code, and the checkout's uv config. Its stale PR body (P3-d) is refreshed in `pr-body.md`.
3. Round 3 is not run. The delta after round 2 is three test cases and one docstring line, and its 19 mutants (§5a) are each killed.

## The two warnings, and when each becomes a failure

- `task copy unverifiable (no dispatched text at head, no result.txt)`:
  - The dispatched `.orchestration/tasks/<t>.md` reaches `main` at a regime boundary, after the PR.
  - Once a PR carries result.txt (PR #411's convention), the copy is checked against its `task_copy=` and the warning disappears.
  - This branch shows it (§6).
- `precheck absent`:
  - It stays a warning until `PRECHECK_REQUIRED` flips (after the four merge-base confirmations of plan 024), which a later task turns into a failure.
  - This branch shows it (§6), and the RESULT carries `precheck=pending-411`.

## The operator's promotion step

`regime` starts optional: the ruleset's seven required contexts do not include it (premise 5, §11). Making it required is the operator's ruleset step, through `ruleset-request.sh` once P1-14 lands. P2-2 (below) should be fixed before that step.

## Proposed advisory (P2), for `dotfiles-T133-regime-ci-followup-a01`

- P2-2: a PR that carries two task directories (a `reset_of` lineage such as #408, or a follow-up carrying a predecessor's records such as #413) fails each copy.
  - Each copy's `allowed_files` and precheck are checked against the other task's paths.
  - The reviewer's runs against #408 and #413 exit 1.
  - Proposed: skip a target that another target names in `reset_of`, and allow every target's own `.orchestration/<t>/` paths for the others.
  - It is outside Files item 2's per-copy rules. Its owner task file is the orchestrator's to write, under the Completion clause.

## Residuals

- regime-ci.py and the checker run from the PR's own checkout on a `pull_request` event, with no secrets and a read-only token.
  - A PR that edits either can change what the job reports. regime-ci prints a warning for that, and the edit is in its own diff, which the task-level audit and the security review read (the threat table's workflow row).
  - The task's Goal sentence "executes nothing the pull request controls" holds for the copy, precheck.json and result.txt (data only), not for those two programs.
- The caps count additions plus deletions; a binary file counts 0 lines.
- `allowed_files` globs: `/**` takes its prefix, and `*` and `?` stay within one segment. A `[...]` class is taken literally; none appears in the tree's task files.

## Blocked: the workflow-security allowlist (an amendment requested)

PR #418's CI `test` jobs fail on `tests/unit/test_workflow_security.py::test_workflows_have_exact_top_level_permissions`. Its `EXPECTED_PERMISSIONS` allowlist names every workflow file, by design, and lacks `regime.yml`. The fix is one line, `"regime.yml": {"contents": "read"}`, in a file outside `allowed_files`. `AGMSG-PONG v1 … status=blocked` (message 2235, 13:36:50Z) asks for the amendment. The job `regime` itself passes on the PR (§10).

## Caps (§9)

- Outside `tests/` and `.orchestration/`: regime.yml and regime-ci.py against the cap of 300 (the counts are in §9).
- `tests/`: test_regime_ci.py against the cap of 450.

## PR

- PR #418 was opened as a draft from this worktree with the plain create command and `--body-file .orchestration/dotfiles-T133-regime-ci-a01/pr-body.md` at c6cc8f20.
- The body on GitHub is the one opened then. `pr-body.md` is refreshed for the re-plan, but editing the GitHub body needs `gh pr edit`, which matches a live ask rule, so this report carries the change.
- Its own `regime` job is pasted from `gh run view` on the final head (§10).

cost: n/a
