---
task_id: dotfiles-T133-ci-efficiency-a01
seat: claude-standard-dot-a011
code_commit: 99b07d2b
---

# Validation: dotfiles-T133-ci-efficiency-a01

Every command ran from the worktree `.claude/worktrees/worker-d` on the branch `tools/ci-efficiency-a01` at `99b07d2b` (the test commit `0b7c5b4c`, the change `3affaac7`, the worker review round: the test commit `20096edf` and the fix `414e475b`, and the orchestrator's revise round 1 (amendment 2): the test commit `407a72d4` and the fix `99b07d2b`; all on `origin/main` `99a4a80f`), inside the sandbox unless a section says otherwise. `MAIN` names the main checkout, `T` the task id, `SCRATCH` the seat's scratchpad and `SHIM` the validation-only `mktemp` shim (T132 validation §5: on macOS a bare `mktemp -d` ignores `TMPDIR` and the sandbox denies the Darwin user temp directory). The output is verbatim, with the main checkout's, the home directory's and the scratchpad's paths replaced by `$MAIN`, `$HOME` and `$SCRATCH`, and each block ends with the exit status of the command shown. The item 0 measurement is its own record, `measure.md`.

## 1. Task file (amendment 2, sha256 a1c57336…) and task copy
```console
$ shasum -a 256 "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md"; cmp "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md" && echo byte-identical
a1c573367be16e604a240e610c79729a81748932e531088784295041a74f6089  $MAIN/.orchestration/tasks/dotfiles-T133-ci-efficiency-a01.md
a1c573367be16e604a240e610c79729a81748932e531088784295041a74f6089  .orchestration/dotfiles-T133-ci-efficiency-a01/task.md
byte-identical
[exit 0]
```
## 1a. The task-consistency check on the dispatched file
```console
$ uv run --offline --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root "$PWD" "$MAIN/.orchestration/tasks/$T.md"
dotfiles-T133-ci-efficiency-a01.md: OK
[exit 0]
```
## 2. Premises, re-run against origin/main (4 through the GitHub API)
```console
$ for f in test.yaml remote.yaml agent-assets.yml; do printf "%s:" ".github/workflows/$f"; git show "origin/main:.github/workflows/$f" | /usr/bin/grep -c "^concurrency:"; done
.github/workflows/test.yaml:0
.github/workflows/remote.yaml:0
.github/workflows/agent-assets.yml:0
[exit 1]
```
```console
$ git show origin/main:.github/workflows/remote.yaml | sed -n 3,9p; git show origin/main:tests/unit/test_workflow_orchestration_skip.py | /usr/bin/grep -c "def test_the_required_contexts_are_the_workflows_jobs"
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:
  schedule:
1
[exit 0]
```
```console
$ gh api repos/mryfmo/dotfiles/rulesets/24397953 --jq "[.rules[]|select(.type==\"required_status_checks\")|.parameters.required_status_checks[].context]|length"; gh api repos/mryfmo/dotfiles/rulesets/24397953 --jq "[.rules[]|select(.type==\"required_status_checks\")|.parameters.required_status_checks[].context]|sort|.[]"
7
public-bootstrap (macos-14, client)
public-bootstrap (ubuntu-24.04, client)
public-bootstrap (ubuntu-24.04, server)
test (macos-14, client)
test (ubuntu-24.04, client)
test (ubuntu-24.04, server)
validate
[exit 0]
```
## 3. Branch
```console
$ git log --oneline origin/main..HEAD; git log --oneline -1 origin/main
99b07d2b fix(ci): the bootstrap gate runs on .chezmoiroot and vendor/; ci-rerun.sh reserves the run under a lock before rerunning it (T133 ci-efficiency a01, revise round 1, Bot P2 4305896433 and 4305896435)
407a72d4 test(ci): the bootstrap gate runs on .chezmoiroot and vendor/, and ci-rerun.sh reserves a run before rerunning it (T133 ci-efficiency a01, revise round 1, Bot P2 4305896433 and 4305896435, red)
7779e78b chore(orchestration): T133 ci-efficiency a01 records (report, validation, sandbox, learning, worker review evidence)
414e475b fix(ci): ci-rerun.sh exits 1 on any failed gh or jq call; the concurrency comment says what the group does (T133 ci-efficiency a01, worker review P2 and P3)
20096edf test(ci): ci-rerun.sh reports a failing gh call as exit 1, never with its own codes (T133 ci-efficiency a01, worker review P2, red)
3affaac7 feat(ci): one run per PR head, the private bootstrap off pull requests, in-job skips and a once-only flake rerun (T133 ci-efficiency a01)
0b7c5b4c test(ci): concurrency per PR head, private bootstrap off pull requests, in-job skips and the flake rerun script (T133 ci-efficiency a01, red)
99a4a80f feat(doctor): make doctor fails on a Mac that may sleep (T129 doctor-sleep-disabled a01) (#394)
[exit 0]
```
## 4. Red on the test commits 0b7c5b4c, 20096edf and 407a72d4, green at the head: the Check's test command (scratch worktrees removed afterwards)
```console
$ git worktree add --detach -q "$SCRATCH/v133-red" 0b7c5b4c && uv run --directory "$SCRATCH/v133-red" python -m unittest tests.unit.test_workflow_orchestration_skip tests.unit.test_workflow_security tests.unit.test_ci_rerun -v 2>&1 | /usr/bin/grep -E " \.\.\. (ok|FAIL|ERROR)$|^Ran|^OK|^FAILED" | sed "s/ (tests\.unit[^)]*)//"; git worktree remove "$SCRATCH/v133-red"
test_a_main_tests_job_when_present_decides_in_itself ... ok
test_both_bootstrap_jobs_decide_with_the_same_script ... ERROR
  test_each_deciding_job_decides_after_its_checkout_and_fails_closed (job='private-bootstrap') ... ERROR
  test_every_heavy_step_carries_its_jobs_decision (job='public-bootstrap', step='Skip the bootstrap for an .orchestration-only diff') ... FAIL
test_every_heavy_step_carries_its_jobs_decision ... ERROR
test_a_pull_request_skips_the_bootstrap_only_for_an_orchestration_only_diff ... ok
  test_a_pull_request_skips_the_bootstrap_unless_a_bootstrap_path_changed (case='python-script') ... FAIL
test_every_event_but_pull_request_bootstraps ... ok
test_the_decision_survives_a_base_that_moved_after_the_checkout ... ok
test_the_unit_test_decision_ignores_renames ... ok
test_the_unit_test_decision_skips_an_orchestration_only_diff ... ok
  test_the_unit_test_decision_skips_macos_for_an_os_independent_diff_and_runs_it_otherwise (case='os-independent', event='pull_request', os='macos-14') ... FAIL
test_no_job_is_left_for_a_required_job_to_need ... ok
  test_no_required_contexts_job_has_a_job_level_if_or_needs (job='private-bootstrap', key='if') ... ERROR
  test_no_required_contexts_job_has_a_job_level_if_or_needs (job='private-bootstrap', key='needs') ... ERROR
test_the_reader_fails_closed_on_unsupported_key_forms ... ok
test_the_required_contexts_are_the_workflows_jobs ... ok
test_private_bootstrap_runs_only_on_push_schedule_and_dispatch_and_decides_with_the_bootstrap_script ... ERROR
  test_the_three_workflows_cancel_superseded_pull_request_runs_and_keep_every_main_run (workflow='test.yaml') ... FAIL
  test_the_three_workflows_cancel_superseded_pull_request_runs_and_keep_every_main_run (workflow='remote.yaml') ... FAIL
  test_the_three_workflows_cancel_superseded_pull_request_runs_and_keep_every_main_run (workflow='agent-assets.yml') ... FAIL
test_checkout_does_not_persist_credentials_without_explicit_exemption ... ok
test_checkout_rejects_duplicate_or_non_false_credential_settings ... ok
test_checkout_setting_does_not_leak_from_the_next_step ... ok
test_external_actions_use_full_commit_shas ... ok
test_quoted_unnamed_checkout_is_detected ... ok
test_unnamed_checkout_setting_does_not_leak_from_the_next_step ... ok
test_workflows_have_exact_top_level_permissions ... ok
test_workflows_have_no_job_level_permission_overrides ... ok
test_ci_rerun_reruns_once_only_when_every_failed_job_matches_a_signature ... ERROR
Ran 26 tests in 7.162s
FAILED (failures=6, errors=7)
[exit 0]
```
```console
$ git worktree add --detach -q "$SCRATCH/v133-red2" 20096edf && uv run --directory "$SCRATCH/v133-red2" python -m unittest tests.unit.test_ci_rerun -v 2>&1 | /usr/bin/grep -E " \\.\\.\\. (ok|FAIL|ERROR)$|AssertionError|^Ran|^OK|^FAILED" | sed "s/ (tests\\.unit[^)]*)//"; git worktree remove "$SCRATCH/v133-red2"
  test_a_failing_gh_exits_1_never_with_the_scripts_own_codes (gh_exit='4') ... FAIL
  test_a_failing_gh_exits_1_never_with_the_scripts_own_codes (gh_exit='2') ... FAIL
test_ci_rerun_reruns_once_only_when_every_failed_job_matches_a_signature ... ok
AssertionError: 1 != 4 : 
AssertionError: 1 != 2 : 
Ran 2 tests in 1.022s
FAILED (failures=2)
[exit 0]
```
```console
$ git worktree add --detach -q "$SCRATCH/v133-red3" 407a72d4 && uv run --directory "$SCRATCH/v133-red3" python -m unittest tests.unit.test_ci_rerun.CiRerunTest.test_ci_rerun_reserves_the_run_before_rerunning_and_never_reruns_twice tests.unit.test_workflow_orchestration_skip.DecisionTest.test_a_pull_request_skips_the_bootstrap_unless_a_bootstrap_path_changed -v 2>&1 | /usr/bin/grep -E " \\.\\.\\. (ok|FAIL|ERROR)$|Error|^Ran|^OK|^FAILED" | sed "s/ (tests\\.unit[^)]*)//"; git worktree remove "$SCRATCH/v133-red3"
test_ci_rerun_reserves_the_run_before_rerunning_and_never_reruns_twice ... ERROR
  test_a_pull_request_skips_the_bootstrap_unless_a_bootstrap_path_changed (case='chezmoiroot') ... FAIL
  test_a_pull_request_skips_the_bootstrap_unless_a_bootstrap_path_changed (case='vendor') ... FAIL
FileNotFoundError: [Errno 2] No such file or directory: '$TMPDIR/tmp01vq718q/repo/.orchestration/validation/ci-reruns.tsv'
AssertionError: 'should_run=false\n' != 'should_run=true\n'
AssertionError: 'should_run=false\n' != 'should_run=true\n'
Ran 2 tests in 2.076s
FAILED (failures=2, errors=1)
[exit 0]
```
```console
$ uv run python -m unittest tests.unit.test_workflow_orchestration_skip tests.unit.test_workflow_security tests.unit.test_ci_rerun -v
test_a_main_tests_job_when_present_decides_in_itself (tests.unit.test_workflow_orchestration_skip.DecisionStepTest.test_a_main_tests_job_when_present_decides_in_itself) ... ok
test_both_bootstrap_jobs_decide_with_the_same_script (tests.unit.test_workflow_orchestration_skip.DecisionStepTest.test_both_bootstrap_jobs_decide_with_the_same_script) ... ok
test_each_deciding_job_decides_after_its_checkout_and_fails_closed (tests.unit.test_workflow_orchestration_skip.DecisionStepTest.test_each_deciding_job_decides_after_its_checkout_and_fails_closed) ... ok
test_every_heavy_step_carries_its_jobs_decision (tests.unit.test_workflow_orchestration_skip.DecisionStepTest.test_every_heavy_step_carries_its_jobs_decision) ... ok
test_a_pull_request_skips_the_bootstrap_only_for_an_orchestration_only_diff (tests.unit.test_workflow_orchestration_skip.DecisionTest.test_a_pull_request_skips_the_bootstrap_only_for_an_orchestration_only_diff) ... ok
test_a_pull_request_skips_the_bootstrap_unless_a_bootstrap_path_changed (tests.unit.test_workflow_orchestration_skip.DecisionTest.test_a_pull_request_skips_the_bootstrap_unless_a_bootstrap_path_changed) ... ok
test_every_event_but_pull_request_bootstraps (tests.unit.test_workflow_orchestration_skip.DecisionTest.test_every_event_but_pull_request_bootstraps) ... ok
test_the_decision_survives_a_base_that_moved_after_the_checkout (tests.unit.test_workflow_orchestration_skip.DecisionTest.test_the_decision_survives_a_base_that_moved_after_the_checkout) ... ok
test_the_unit_test_decision_ignores_renames (tests.unit.test_workflow_orchestration_skip.DecisionTest.test_the_unit_test_decision_ignores_renames) ... ok
test_the_unit_test_decision_skips_an_orchestration_only_diff (tests.unit.test_workflow_orchestration_skip.DecisionTest.test_the_unit_test_decision_skips_an_orchestration_only_diff) ... ok
test_the_unit_test_decision_skips_macos_for_an_os_independent_diff_and_runs_it_otherwise (tests.unit.test_workflow_orchestration_skip.DecisionTest.test_the_unit_test_decision_skips_macos_for_an_os_independent_diff_and_runs_it_otherwise) ... ok
test_no_job_is_left_for_a_required_job_to_need (tests.unit.test_workflow_orchestration_skip.RequiredContextsTest.test_no_job_is_left_for_a_required_job_to_need) ... ok
test_no_required_contexts_job_has_a_job_level_if_or_needs (tests.unit.test_workflow_orchestration_skip.RequiredContextsTest.test_no_required_contexts_job_has_a_job_level_if_or_needs) ... ok
test_the_reader_fails_closed_on_unsupported_key_forms (tests.unit.test_workflow_orchestration_skip.RequiredContextsTest.test_the_reader_fails_closed_on_unsupported_key_forms) ... ok
test_the_required_contexts_are_the_workflows_jobs (tests.unit.test_workflow_orchestration_skip.RequiredContextsTest.test_the_required_contexts_are_the_workflows_jobs) ... ok
test_private_bootstrap_runs_only_on_push_schedule_and_dispatch_and_decides_with_the_bootstrap_script (tests.unit.test_workflow_orchestration_skip.WorkflowTriggerTest.test_private_bootstrap_runs_only_on_push_schedule_and_dispatch_and_decides_with_the_bootstrap_script) ... ok
test_the_three_workflows_cancel_superseded_pull_request_runs_and_keep_every_main_run (tests.unit.test_workflow_orchestration_skip.WorkflowTriggerTest.test_the_three_workflows_cancel_superseded_pull_request_runs_and_keep_every_main_run) ... ok
test_checkout_does_not_persist_credentials_without_explicit_exemption (tests.unit.test_workflow_security.WorkflowSecurityTest.test_checkout_does_not_persist_credentials_without_explicit_exemption) ... ok
test_checkout_rejects_duplicate_or_non_false_credential_settings (tests.unit.test_workflow_security.WorkflowSecurityTest.test_checkout_rejects_duplicate_or_non_false_credential_settings) ... ok
test_checkout_setting_does_not_leak_from_the_next_step (tests.unit.test_workflow_security.WorkflowSecurityTest.test_checkout_setting_does_not_leak_from_the_next_step) ... ok
test_external_actions_use_full_commit_shas (tests.unit.test_workflow_security.WorkflowSecurityTest.test_external_actions_use_full_commit_shas) ... ok
test_quoted_unnamed_checkout_is_detected (tests.unit.test_workflow_security.WorkflowSecurityTest.test_quoted_unnamed_checkout_is_detected) ... ok
test_unnamed_checkout_setting_does_not_leak_from_the_next_step (tests.unit.test_workflow_security.WorkflowSecurityTest.test_unnamed_checkout_setting_does_not_leak_from_the_next_step) ... ok
test_workflows_have_exact_top_level_permissions (tests.unit.test_workflow_security.WorkflowSecurityTest.test_workflows_have_exact_top_level_permissions) ... ok
test_workflows_have_no_job_level_permission_overrides (tests.unit.test_workflow_security.WorkflowSecurityTest.test_workflows_have_no_job_level_permission_overrides) ... ok
test_a_failing_gh_exits_1_never_with_the_scripts_own_codes (tests.unit.test_ci_rerun.CiRerunTest.test_a_failing_gh_exits_1_never_with_the_scripts_own_codes) ... ok
test_ci_rerun_reruns_once_only_when_every_failed_job_matches_a_signature (tests.unit.test_ci_rerun.CiRerunTest.test_ci_rerun_reruns_once_only_when_every_failed_job_matches_a_signature) ... ok
test_ci_rerun_reserves_the_run_before_rerunning_and_never_reruns_twice (tests.unit.test_ci_rerun.CiRerunTest.test_ci_rerun_reserves_the_run_before_rerunning_and_never_reruns_twice) ... ok

----------------------------------------------------------------------
Ran 28 tests in 9.357s

OK
[exit 0]
```
## 5. The moved job: origin/main remote.yaml lines 112 to 196 against private-bootstrap.yaml lines 16 to 100
```console
$ git show origin/main:.github/workflows/remote.yaml | sed -n 112,196p > "$SCRATCH/v133-old.txt"; sed -n 16,100p .github/workflows/private-bootstrap.yaml > "$SCRATCH/v133-new.txt"; diff "$SCRATCH/v133-old.txt" "$SCRATCH/v133-new.txt"
52c52,53
<           # non-ASCII paths raw. An empty diff runs the bootstrap.
---
>           # non-ASCII paths raw. An empty diff runs the bootstrap, and so does a
>           # path that can change what setup.sh installs or how this job runs it.
54c55
<           if grep -qv '^\.orchestration/' <<< "${changed}"; then
---
>           if [ -z "${changed}" ] || grep -Eq '^(setup\.sh$|\.chezmoiroot$|vendor/|install/|home/|scripts/lib/|scripts/update-agent-assets\.sh$|scripts/gh-auth\.sh$|tests/install/|\.github/workflows/remote\.yaml$|\.github/workflows/private-bootstrap\.yaml$)' <<< "${changed}"; then
60c61
<       - name: Skip the bootstrap for an .orchestration-only diff
---
>       - name: Skip the bootstrap when no bootstrap path changed
62c63
<         run: echo "Only .orchestration/ files changed; the job reports success without bootstrapping."
---
>         run: echo "No path the bootstrap reads changed; the job reports success without bootstrapping."
85d85
<             bash "${GITHUB_WORKSPACE}/setup.sh"
[exit 1]
```
## 6. Lint and format
```console
$ shellcheck scripts/orchestrator/ci-rerun.sh && echo shellcheck-clean; shfmt --version; shfmt --indent 4 --space-redirects -d scripts/orchestrator/ci-rerun.sh && echo shfmt-clean
shellcheck-clean
v3.14.1
shfmt-clean
[exit 0]
```
```console
$ git ls-files -- ":(glob)install/**/*.sh" ":(glob)scripts/**/*.sh" | xargs shfmt -i 4 -sr -d && echo "CI shfmt form: clean"
CI shfmt form: clean
[exit 0]
```
```console
$ ruff format --config ruff.toml --check tests/unit/test_workflow_orchestration_skip.py tests/unit/test_ci_rerun.py tests/unit/test_workflow_security.py; ruff check --config ruff.toml tests/unit/test_workflow_orchestration_skip.py tests/unit/test_ci_rerun.py tests/unit/test_workflow_security.py
3 files already formatted
I001 [*] Import block is un-sorted or un-formatted
 --> tests/unit/test_workflow_security.py:1:1
  |
1 | / import re
2 | | import unittest
3 | | from pathlib import Path
  | |________________________^
help: Organize imports
  |
4 |
  -
5 | ROOT = Path(__file__).resolve().parents[2]
  |

Found 1 error.
[*] 1 fixable with `--fix`.
[exit 1]
```
```console
$ make format > "$SCRATCH/v133-format.txt" 2>&1; echo "make format rc=$?"; /usr/bin/grep -E "^\+\+\+ " "$SCRATCH/v133-format.txt" | sed "s/^+++ //" | sort -u > "$SCRATCH/v133-flagged.txt"; cat "$SCRATCH/v133-flagged.txt"; git diff --quiet origin/main -- $(cat "$SCRATCH/v133-flagged.txt") && echo "every flagged file is unchanged from origin/main"; git ls-files -z "*.py" | xargs -0 ruff format --config ruff.toml --check | tail -1; git ls-files -z "*.md" | xargs -0 prettier --check | tail -1
make format rc=2
.orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/pr-cost.sh
.orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/resolve-threads.sh
.orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-advisory.sh
.orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-review.sh
.orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/sandbox-scan.sh
.orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/boundary.sh
.orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/ff-main.sh
.orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-audit.sh
.orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-gate.sh
.orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/t717-prep.sh
home/dot_claude/hooks/executable_project-map-reload.sh
tests/install/macos/common/brew.bats
every flagged file is unchanged from origin/main
62 files already formatted
All matched files use Prettier code style!
[exit 0]
```
## 7. Render check
```console
$ make render-check
uv run --offline --with pyyaml scripts/generate-agent-configs.py --check
generated agent configs are up to date
[exit 0]
```
## 8. Caps (at most 250 changed lines outside tests/, .orchestration/ and the moved job; 350 under tests/)
```console
$ git diff --numstat origin/main...HEAD
9	0	.github/flakes.yaml
7	0	.github/workflows/agent-assets.yml
101	0	.github/workflows/private-bootstrap.yaml
12	90	.github/workflows/remote.yaml
21	4	.github/workflows/test.yaml
26	0	.orchestration/dotfiles-T133-ci-efficiency-a01/dotfiles-T133-ci-efficiency-a01-worker-crit.json
13	0	.orchestration/dotfiles-T133-ci-efficiency-a01/dotfiles-T133-ci-efficiency-a01-worker-review-receipt.md
8	0	.orchestration/dotfiles-T133-ci-efficiency-a01/learning.md
326	0	.orchestration/dotfiles-T133-ci-efficiency-a01/measure.md
68	0	.orchestration/dotfiles-T133-ci-efficiency-a01/report.md
26	0	.orchestration/dotfiles-T133-ci-efficiency-a01/sandbox.md
126	0	.orchestration/dotfiles-T133-ci-efficiency-a01/task.md
396	0	.orchestration/dotfiles-T133-ci-efficiency-a01/validation.md
106	0	scripts/orchestrator/ci-rerun.sh
175	0	tests/unit/test_ci_rerun.py
76	4	tests/unit/test_workflow_orchestration_skip.py
1	0	tests/unit/test_workflow_security.py
[exit 0]
```
```console
$ git diff --numstat origin/main...HEAD | awk '$3 ~ /^tests\// { t += $1 + $2; next } $3 ~ /^\.orchestration\// { next } $3 == ".github/workflows/private-bootstrap.yaml" { moved_new = $1; next } $3 == ".github/workflows/remote.yaml" { remote = $1 + $2; next } { o += $1 + $2 } END { printf "remote.yaml changed lines %d, of which the moved job and its blank line removed: 86\noutside tests/, .orchestration/ and the moved job: %d\nprivate-bootstrap.yaml (the moved job, counted separately): %d added\ntests/: %d\n", remote, o + remote - 86, moved_new, t }'
remote.yaml changed lines 102, of which the moved job and its blank line removed: 86
outside tests/, .orchestration/ and the moved job: 163
private-bootstrap.yaml (the moved job, counted separately): 101 added
tests/: 256
[exit 0]
```
## 9. Scope: the hunks of each workflow and the files touched
```console
$ git diff --stat origin/main...HEAD; git diff -U0 origin/main...HEAD -- .github/workflows/test.yaml .github/workflows/remote.yaml .github/workflows/agent-assets.yml | /usr/bin/grep -E "^(@@|\+\+\+)"
 .github/flakes.yaml                                |   9 +
 .github/workflows/agent-assets.yml                 |   7 +
 .github/workflows/private-bootstrap.yaml           | 101 ++++++
 .github/workflows/remote.yaml                      | 102 +-----
 .github/workflows/test.yaml                        |  25 +-
 ...otfiles-T133-ci-efficiency-a01-worker-crit.json |  26 ++
 ...T133-ci-efficiency-a01-worker-review-receipt.md |  13 +
 .../dotfiles-T133-ci-efficiency-a01/learning.md    |   8 +
 .../dotfiles-T133-ci-efficiency-a01/measure.md     | 326 +++++++++++++++++
 .../dotfiles-T133-ci-efficiency-a01/report.md      |  68 ++++
 .../dotfiles-T133-ci-efficiency-a01/sandbox.md     |  26 ++
 .../dotfiles-T133-ci-efficiency-a01/task.md        | 126 +++++++
 .../dotfiles-T133-ci-efficiency-a01/validation.md  | 396 +++++++++++++++++++++
 scripts/orchestrator/ci-rerun.sh                   | 106 ++++++
 tests/unit/test_ci_rerun.py                        | 175 +++++++++
 tests/unit/test_workflow_orchestration_skip.py     |  80 ++++-
 tests/unit/test_workflow_security.py               |   1 +
 17 files changed, 1497 insertions(+), 98 deletions(-)
+++ b/.github/workflows/agent-assets.yml
@@ -12,0 +13,7 @@ on:
+++ b/.github/workflows/remote.yaml
@@ -11,0 +12,7 @@ on:
@@ -65 +72,2 @@ jobs:
@@ -67 +75 @@ jobs:
@@ -73 +81 @@ jobs:
@@ -75 +83 @@ jobs:
@@ -111,86 +118,0 @@ jobs:
+++ b/.github/workflows/test.yaml
@@ -12,0 +13,8 @@ on:
@@ -102,3 +110 @@ jobs:
@@ -105,0 +112,9 @@ jobs:
@@ -109,0 +125,2 @@ jobs:
@@ -111 +128 @@ jobs:
[exit 0]
```
## 4a. `make unit-test` with the shim at 3affaac7, and the failing modules on untouched origin/main

The full suite ran once, at `3affaac7`, as `PATH="$SHIM:$PATH" make unit-test > "$SCRATCH/t133-unit-test.txt" 2>&1` (`make unit-test rc=2`; the last lines of that run: `Ran 1181 tests in 793.390s`, `FAILED (failures=147, errors=107, skipped=2)`, `make: *** [unit-test] Error 1`). The fix round after it changes only `ci-rerun.sh`, `test_ci_rerun.py` and three comment lines, which §4 re-runs. The counts below are read from the saved outputs.
```console
$ grep -E "^Ran|^OK|^FAILED" "$SCRATCH/t133-unit-test.txt"; grep -E "^(FAIL|ERROR): " "$SCRATCH/t133-unit-test.txt" | grep -oE "test_[a-z_]+\.[A-Z][A-Za-z]+Test" | sort | uniq -c
Ran 1181 tests in 793.390s
FAILED (failures=147, errors=107, skipped=2)
   4 test_agent_stop_gate.AgentStopGateTest
   5 test_gh_auth.GhAuthTest
  82 test_herdr_agents.HerdrAgentsTest
 136 test_require_crit_review.ReviewGuardTest
   8 test_runtime_health.RuntimeHealthTest
  19 test_ua_symbol_coverage.UaSymbolCoverageTest
```
The same modules on a scratch worktree of `origin/main` `99a4a80f` (removed afterwards), with the same shim:
```console
$ git worktree add --detach -q "$SCRATCH/v-cmp" origin/main && PATH="$SHIM:$PATH" uv run --directory "$SCRATCH/v-cmp" python -m unittest tests.unit.test_gh_auth tests.unit.test_herdr_agents tests.unit.test_require_crit_review > "$SCRATCH/v-cmp.txt" 2>&1; git worktree remove --force "$SCRATCH/v-cmp"; grep -E "^Ran|^OK|^FAILED" "$SCRATCH/v-cmp.txt"; grep -E "^(FAIL|ERROR): " "$SCRATCH/v-cmp.txt" | grep -oE "test_[a-z_]+\.[A-Z][A-Za-z]+Test" | sort | uniq -c
Ran 298 tests in 350.069s
FAILED (failures=137, errors=86)
   5 test_gh_auth.GhAuthTest
  82 test_herdr_agents.HerdrAgentsTest
 136 test_require_crit_review.ReviewGuardTest
$ git worktree add --detach -q "$SCRATCH/v-cmp2" origin/main && PATH="$SHIM:$PATH" uv run --directory "$SCRATCH/v-cmp2" python -m unittest tests.unit.test_runtime_health tests.unit.test_ua_symbol_coverage > "$SCRATCH/v-cmp2.txt" 2>&1; git worktree remove --force "$SCRATCH/v-cmp2"; grep -E "^Ran|^OK|^FAILED" "$SCRATCH/v-cmp2.txt"; grep -E "^(FAIL|ERROR): " "$SCRATCH/v-cmp2.txt" | grep -oE "test_[a-z_]+\.[A-Z][A-Za-z]+Test" | sort | uniq -c; diff <the sorted runtime_health failure names of both runs> && echo "same runtime_health failures"
Ran 74 tests in 101.207s
FAILED (failures=6, errors=21)
   8 test_runtime_health.RuntimeHealthTest
  19 test_ua_symbol_coverage.UaSymbolCoverageTest
same runtime_health failures
$ git worktree add --detach -q "$SCRATCH/v-gate" origin/main && PATH="$SHIM:$PATH" uv run --directory "$SCRATCH/v-gate" python -m unittest tests.unit.test_agent_stop_gate -v > "$SCRATCH/v-gate.txt" 2>&1; git worktree remove "$SCRATCH/v-gate"; grep -E "^Ran|^OK|^FAILED" "$SCRATCH/v-gate.txt"
Ran 46 tests in 27.932s
FAILED (failures=4, skipped=1)
```
The cause of the `git commit` failures (exit 128) in those fixtures:
```console
$ git config --global --get commit.gpgsign; git config --global --get gpg.format; d="$(mktemp -d "$TMPDIR/gsign.XXXXXX")"; git -C "$d" init -q && git -C "$d" -c user.name=t -c user.email=t@t commit -q --allow-empty -m c 2>&1 | head -3; git -C "$d" -c user.name=t -c user.email=t@t -c commit.gpgsign=false commit -q --allow-empty -m c && echo "unsigned commit: ok"
true
ssh
error: Couldn't load public key $HOME/.ssh/id_ed25519.pub: No such file or directory?

fatal: failed to write commit object
unsigned commit: ok
```
## 6a. The I001 of test_workflow_security.py already exists on origin/main
```console
$ git show origin/main:tests/unit/test_workflow_security.py | ruff check --config ruff.toml --stdin-filename tests/unit/test_workflow_security.py - 2>&1 | tail -3

Found 1 error.
[*] 1 fixable with `--fix`.
```
## 11. CompactionDB: one decision in this worktree's store before completion
```console
$ uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "T133 (CI efficiency): test.yaml, remote.yaml and agent-assets.yml share one concurrency block (group <workflow>-pr-<number> or -main-<sha>, cancel-in-progress only on pull requests); private-bootstrap lives in private-bootstrap.yaml (push to main, schedule, dispatch; not required); the bootstrap and macOS unit tests skip on a PR whose diff cannot affect them; scripts/orchestrator/ci-rerun.sh reruns a run once only when every failed job matches .github/flakes.yaml and records it in .orchestration/validation/ci-reruns.tsv." 2>&1 | tail -2
a1a806d6-8f67-4f51-9bb0-261e78817bef
```
## 10. Push, the draft PR, and CI on 414e475b
```console
$ GIT_CONFIG_GLOBAL=/dev/null git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push origin tools/ci-efficiency-a01 2>&1 | tail -2
To https://github.com/mryfmo/dotfiles
 * [new branch]        tools/ci-efficiency-a01 -> tools/ci-efficiency-a01
$ gh pr create --draft --base main --head tools/ci-efficiency-a01 --title "feat(ci): one run per PR head, the private bootstrap off pull requests, in-job skips and a once-only flake rerun (T133 ci-efficiency a01)" --body-file "$SCRATCH/t133-pr-body.md"
https://github.com/mryfmo/dotfiles/pull/409
$ GIT_CONFIG_GLOBAL=/dev/null git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push origin tools/ci-efficiency-a01 2>&1 | tail -1
   3affaac7..414e475b  tools/ci-efficiency-a01 -> tools/ci-efficiency-a01
```
Seconds after the second push (05:03:03Z) and 80 seconds later: the superseded head's `Snippet install` run is cancelled, and no `Private bootstrap` run exists on the pull request:
```console
$ gh run list --branch tools/ci-efficiency-a01 --json databaseId,name,event,status,conclusion,headSha --jq '.[]|[.databaseId,.name,.event,.status,.conclusion,.headSha[0:8]]|@tsv'
39099206141	Unit test	pull_request	queued		414e475b
39099206121	Snippet install	pull_request	pending		414e475b
39099206136	Agent assets	pull_request	in_progress		414e475b
39098697844	Snippet install	pull_request	in_progress		3affaac7
39098697837	Agent assets	pull_request	completed	success	3affaac7
39098697843	Unit test	pull_request	completed	success	3affaac7
$ gh run list --branch tools/ci-efficiency-a01 --json databaseId,name,event,status,conclusion,headSha --jq '.[]|[.databaseId,.name,.event,.status,.conclusion,.headSha[0:8]]|@tsv'   # 80 s later
39099206136	Agent assets	pull_request	in_progress		414e475b
39099206141	Unit test	pull_request	in_progress		414e475b
39099206121	Snippet install	pull_request	queued		414e475b
39098697837	Agent assets	pull_request	completed	success	3affaac7
39098697843	Unit test	pull_request	completed	success	3affaac7
39098697844	Snippet install	pull_request	completed	cancelled	3affaac7
```
After CI finished on `414e475b`:
```console
$ gh run list --branch tools/ci-efficiency-a01 --json name,event,conclusion,headSha --jq '.[]|[.name,.event,.conclusion,.headSha[0:8]]|@tsv'
Agent assets	pull_request	success	414e475b
Unit test	pull_request	success	414e475b
Snippet install	pull_request	success	414e475b
Agent assets	pull_request	success	3affaac7
Unit test	pull_request	success	3affaac7
Snippet install	pull_request	cancelled	3affaac7
[exit 0]
$ gh pr checks 409 | cut -f1,2 | sort
CodeRabbit	pass
GitGuardian Security Checks	pass
public-bootstrap (macos-14, client)	pass
public-bootstrap (ubuntu-24.04, client)	pass
public-bootstrap (ubuntu-24.04, server)	pass
test (macos-14, client)	pass
test (ubuntu-24.04, client)	pass
test (ubuntu-24.04, server)	pass
test (ubuntu-26.04, client)	pass
validate	pass
$ gh api repos/mryfmo/dotfiles/commits/414e475b/check-runs --paginate --jq '.check_runs[]|[.name,.conclusion]|@tsv' | sort | grep -cE "^(validate|test \((ubuntu-24.04, (server|client)|macos-14, client)\)|public-bootstrap \((ubuntu-24.04, (server|client)|macos-14, client)\))	success$"
7
```
## 12. Revise round 1 (amendment 2; ACCEPTANCE revise of 05:47:01Z, previous_head 7779e78b)

The two `check=` tests are red on `407a72d4` and green at `99b07d2b` (§4). The Bot's two P2 threads are `fixed:99b07d2b`: 4305896433 (the path gate gains `\.chezmoiroot$|vendor/` in both bootstrap workflows) and 4305896435 (the run is reserved under `ci-reruns.lock` before `gh run rerun`). The round is pushed once, as a single command, after this record is committed. Its CI and the Bot's state on the new head are reported in the RESULT, because a record cannot hold the CI of its own commit. §10 is the CI of `414e475b`, the head before the round. The `revise.yaml` beside this file carries `previous_head` and both selectors.
