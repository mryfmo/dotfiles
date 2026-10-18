---
task_id: dotfiles-T133-regime-ci-a02
seat: claude-standard-dot-a008
head: 1ee15af1
---

# Validation: dotfiles-T133-regime-ci-a02

Every command ran from the worktree `.claude/worktrees/worker-f` on the branch `tools/regime-ci-a01` (PR #418) at `1ee15af1` (the code head after amendment 1), inside the sandbox, through a generator that prints each command, its verbatim output and its exit status (a block's status is its last command's), except §11 (premise 5, through gh outside the sandbox). `MAIN` names the main checkout and `T` the task id. The scratch worktrees (`$R`, `$Q`, `$M`, and the bootstrap's isolated base checkout under `$TMPDIR`) are removed after their block with `git worktree remove --force`. §0's exit 128 is premise 6 holding (the base has no regime.yml). §6 is item 8's local bootstrap: this first PR cannot run its own `pull_request_target` job, so the job's command line runs in an isolated checkout of the base sha with the candidate verifier installed for that run only and the base's checker; the head is data (its sha). The a01 records under `.orchestration/dotfiles-T133-regime-ci-a01/` (blocks there and their `regime` runs on this PR) are historical evidence of the withdrawn design.

## 0. Premise 6: the base has no regime.yml, so this first PR cannot run its own pull_request_target job
```console
$ git rev-parse origin/main; git cat-file -e origin/main:.github/workflows/regime.yml
3e41e36abc949acd7e6b4859c1a22df9e665c8d4
fatal: path '.github/workflows/regime.yml' exists on disk, but not in 'origin/main'
[exit 128]
```
## 1. Task file (amendment 1, sha256 807c6b74…) and task copy; the a01 copy is deleted and a01's other evidence unchanged since 4a921414
```console
$ shasum -a 256 "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md"; cmp "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md" && echo byte-identical; git diff --name-status 4a921414 HEAD -- .orchestration/dotfiles-T133-regime-ci-a01
807c6b7446b7bbf795aa2b6aa6db1c46b9543b8ac953e40b4309dfd735322219  ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-regime-ci-a02.md
807c6b7446b7bbf795aa2b6aa6db1c46b9543b8ac953e40b4309dfd735322219  .orchestration/dotfiles-T133-regime-ci-a02/task.md
byte-identical
D	.orchestration/dotfiles-T133-regime-ci-a01/task.md
[exit 0]
```
## 1a. The task-consistency check on the dispatched file
```console
$ uv run --offline --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root "$PWD" "$MAIN/.orchestration/tasks/$T.md"
dotfiles-T133-regime-ci-a02.md: OK
[exit 0]
```
## 2. Premises 1 to 4, replayed on origin/main (premise 5 needs gh: §11)
```console
$ B=$(git rev-parse origin/main); echo "origin/main=$B"; git ls-tree -r --name-only "$B" -- .github/workflows/regime.yml scripts/orchestrator/regime-ci.py tests/unit/test_regime_ci.py | wc -l; for f in $(git ls-tree --name-only "$B" .github/workflows/ | /usr/bin/grep "\.yaml$"); do git show "$B:$f"; done | /usr/bin/grep -h "uses: actions/checkout@\|uses: astral-sh/setup-uv@" | sed "s/^[- ]*//" | sort -u; git show "$B:scripts/orchestrator/task-consistency-check.py" | /usr/bin/grep -c "^C[0-9]*b\? "; git show "$B:scripts/orchestrator/result-precheck.sh" > /dev/null 2>&1 && echo present-on-main || echo absent-on-main
origin/main=3e41e36abc949acd7e6b4859c1a22df9e665c8d4
       0
uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7
uses: astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7 # v10.2.0
11
absent-on-main
[exit 0]
```
## 3. Branch, base and the commits since 4a921414
```console
$ git branch --show-current; git rev-parse HEAD origin/main; git log --oneline 4a921414..HEAD
tools/regime-ci-a01
1ee15af1a159b45baefcd5505f816f9bbcccef98
3e41e36abc949acd7e6b4859c1a22df9e665c8d4
1ee15af1 fix(orchestrator): the base checker reads only the base's dispatched bytes (T133 regime-ci a02 amendment 1; worker review P0 of bcbd6949)
357ff237 test(orchestrator): the checker-skipped warning, the unverifiable report of a hostile copy, and a chain that counts only when both copies verify (T133 regime-ci a02 amendment 1)
3636fc05 docs(orchestration): T133 regime-ci a02: the task copy at amendment 1 (807c6b74)
56ccbee1 test(orchestrator): a pull request's text never reaches the base checker; an authenticated predecessor stays checked; a rename into the evidence directory is drift (T133 regime-ci a02, worker review P0 and P3s)
bcbd6949 fix(orchestrator): regime runs the base's workflow, verifier and checker and reads the head as data (T133 regime-ci a02; Bot P1 4308651010, 4308651011, 4308651013)
6a423f4c test(orchestrator): the retained regime-ci tests on the a02 base-checkout model (T133 regime-ci a02)
d16bfc6e test(orchestrator): the a02 redesign's four tests, red against 4a921414 (T133 regime-ci a02)
64be693c docs(orchestration): T133 regime-ci a02: the reset copy replaces a01's (reset_of dotfiles-T133-regime-ci-a01)
[exit 0]
```
## 4. RED: the four redesign tests at d16bfc6e, whose regime.yml and regime-ci.py are 4a921414's, in a scratch worktree
```console
$ git -C "$R" diff --quiet 4a921414 -- .github/workflows/regime.yml scripts/orchestrator/regime-ci.py && echo "workflow and verifier identical to 4a921414"; cd "$R" && uv run python -m unittest tests.unit.test_regime_ci.RegimeCiTest.test_the_regime_workflow_runs_base_code_only tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_reads_the_head_as_data_and_runs_the_base_verifier tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_exempts_records_only_heads_by_content_not_branch_name tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_unverifiable_copy_is_a_warning_until_the_flag 2>&1 | /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^(OK|FAILED)" | sed -E "s/ \\(tests\\.unit\\.test_regime_ci\\.RegimeCiTest\\.[a-z_]+\\)//" | cut -c1-200
workflow and verifier identical to 4a921414
FAIL: test_the_regime_workflow_runs_base_code_only
FAIL: test_regime_ci_reads_the_head_as_data_and_runs_the_base_verifier (expected=0, phrase=None)
FAIL: test_regime_ci_reads_the_head_as_data_and_runs_the_base_verifier (expected=1, phrase='allowed-files: stray.sh is outside allowed_files')
FAIL: test_regime_ci_reads_the_head_as_data_and_runs_the_base_verifier (expected=1, phrase='task-copy: ')
FAIL: test_regime_ci_exempts_records_only_heads_by_content_not_branch_name
FAIL: test_regime_ci_unverifiable_copy_is_a_warning_until_the_flag (head_dispatched=False)
FAIL: test_regime_ci_unverifiable_copy_is_a_warning_until_the_flag (head_dispatched=True)
Ran 4 tests in 4.726s
FAILED (failures=7)
[exit 0]
```
## 4a. RED for the worker review: the P0 and P3 regressions at 56ccbee1, whose regime-ci.py is bcbd6949's (the marker command ran), in a scratch worktree
```console
$ git -C "$Q" diff --quiet bcbd6949 -- scripts/orchestrator/regime-ci.py && echo "regime-ci.py identical to bcbd6949"; cd "$Q" && uv run python -m unittest tests.unit.test_regime_ci 2>&1 | /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^(OK|FAILED)" | sed -E "s/ \\(tests\\.unit\\.test_regime_ci\\.RegimeCiTest\\.[a-z_]+\\)//" | cut -c1-200
regime-ci.py identical to bcbd6949
FAIL: test_regime_ci_keeps_an_authenticated_predecessor_a_head_only_successor_names
FAIL: test_regime_ci_never_feeds_a_pull_request_s_text_to_the_base_checker (dispatched=False)
FAIL: test_regime_ci_never_feeds_a_pull_request_s_text_to_the_base_checker (dispatched=True)
FAIL: test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr (case='precheck renamed')
Ran 14 tests in 32.486s
FAILED (failures=4)
[exit 0]
```
## 5. GREEN: the Check's unit-test commands on HEAD
```console
$ git rev-parse --short=8 HEAD; uv run python -m unittest tests.unit.test_regime_ci -v 2>&1 | /usr/bin/grep -E "\.\.\. |^Ran|^(OK|FAILED)"; uv run python -m unittest tests.unit.test_workflow_security -v 2>&1 | /usr/bin/grep -E "\.\.\. |^Ran|^(OK|FAILED)"
1ee15af1
test_regime_ci_checks_only_the_latest_copy_of_a_reset_of_lineage (tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_checks_only_the_latest_copy_of_a_reset_of_lineage) ... ok
test_regime_ci_checks_the_copy_against_result_txt_without_dispatched_text (tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_checks_the_copy_against_result_txt_without_dispatched_text) ... ok
test_regime_ci_exempts_records_only_heads_by_content_not_branch_name (tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_exempts_records_only_heads_by_content_not_branch_name) ... ok
test_regime_ci_keeps_an_authenticated_predecessor_a_head_only_successor_names (tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_keeps_an_authenticated_predecessor_a_head_only_successor_names) ... ok
test_regime_ci_never_feeds_a_pull_request_s_text_to_the_base_checker (tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_never_feeds_a_pull_request_s_text_to_the_base_checker) ... ok
test_regime_ci_passes_a_records_only_pr_with_no_target (tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_passes_a_records_only_pr_with_no_target) ... ok
test_regime_ci_reads_the_head_as_data_and_runs_the_base_verifier (tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_reads_the_head_as_data_and_runs_the_base_verifier) ... ok
test_regime_ci_refuses_a_checkout_not_at_the_base_and_a_diff_git_cannot_list (tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_refuses_a_checkout_not_at_the_base_and_a_diff_git_cannot_list) ... ok
test_regime_ci_reports_a_copy_whose_task_id_is_not_its_directory (tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_reports_a_copy_whose_task_id_is_not_its_directory) ... ok
test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr (tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr) ... ok
test_regime_ci_runs_the_checker_without_the_checkout_s_uv_config (tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_runs_the_checker_without_the_checkout_s_uv_config) ... ok
test_regime_ci_unverifiable_copy_is_a_warning_until_the_flag (tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_unverifiable_copy_is_a_warning_until_the_flag) ... ok
test_regime_ci_warns_without_precheck_and_without_dispatched_text (tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_warns_without_precheck_and_without_dispatched_text) ... ok
test_the_regime_workflow_runs_base_code_only (tests.unit.test_regime_ci.RegimeCiTest.test_the_regime_workflow_runs_base_code_only) ... ok
Ran 14 tests in 32.018s
OK
test_checkout_does_not_persist_credentials_without_explicit_exemption (tests.unit.test_workflow_security.WorkflowSecurityTest.test_checkout_does_not_persist_credentials_without_explicit_exemption) ... ok
test_checkout_rejects_duplicate_or_non_false_credential_settings (tests.unit.test_workflow_security.WorkflowSecurityTest.test_checkout_rejects_duplicate_or_non_false_credential_settings) ... ok
test_checkout_setting_does_not_leak_from_the_next_step (tests.unit.test_workflow_security.WorkflowSecurityTest.test_checkout_setting_does_not_leak_from_the_next_step) ... ok
test_external_actions_use_full_commit_shas (tests.unit.test_workflow_security.WorkflowSecurityTest.test_external_actions_use_full_commit_shas) ... ok
test_quoted_unnamed_checkout_is_detected (tests.unit.test_workflow_security.WorkflowSecurityTest.test_quoted_unnamed_checkout_is_detected) ... ok
test_unnamed_checkout_setting_does_not_leak_from_the_next_step (tests.unit.test_workflow_security.WorkflowSecurityTest.test_unnamed_checkout_setting_does_not_leak_from_the_next_step) ... ok
test_workflows_have_exact_top_level_permissions (tests.unit.test_workflow_security.WorkflowSecurityTest.test_workflows_have_exact_top_level_permissions) ... ok
test_workflows_have_no_job_level_permission_overrides (tests.unit.test_workflow_security.WorkflowSecurityTest.test_workflows_have_no_job_level_permission_overrides) ... ok
Ran 8 tests in 0.003s
OK
[exit 0]
```
## 5a. Each rule of the redesigned verifier disabled in turn in a scratch worktree at HEAD: the test module fails for every mutant (the helper, then its run)
```console
$ cat "$TMPDIR/mut-regime.py"; echo "--- run"; uv run python "$TMPDIR/mut-regime.py" "$M"
"""Each mutant disables one rule of regime-ci.py in a scratch copy; the test module must fail for every one."""
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
script = root / "scripts/orchestrator/regime-ci.py"
original = script.read_text()
MUTANTS = [
    ("task-copy (base dispatched)", "if data != copy:", "if False:"),
    ("task-copy (result.txt)", 'if result is not None and token(result_text, "task_copy") != sha256(copy):', "if False:"),
    ("dispatched read at the base", 'dispatched = show(root, base, f".orchestration/tasks/{t}.md")', 'dispatched = show(root, head, f".orchestration/tasks/{t}.md")'),
    ("REGIME_REQUIRE_DISPATCHED", 'found += [("task-copy", unverifiable)] if os.environ.get("REGIME_REQUIRE_DISPATCHED") == "1" else []', "found += []"),
    ("policy allowed_files", 'entries = [a for a in rules.get("allowed_files") or [] if isinstance(a, str)]', 'entries = [a for a in fm.get("allowed_files") or [] if isinstance(a, str)]'),
    ("policy reset_of exempt", 'exempt = tuple(f".orchestration/{p}/" for p in rules.get("reset_of") or [] if isinstance(p, str))', "exempt = ()"),
    ("checkout at the base", "if at != base:", "if False:"),
    ("records-only by content", "if not stray:", "if True:"),
    ("precheck sha", 'if token(result_text, "precheck") != sha256(data):', "if False:"),
    ("precheck 40-hex", 'if not isinstance(bound, str) or not re.fullmatch(r"[0-9a-f]{40}", bound):', "if not bound:"),
    ("precheck non-ancestor", 'if git(root, "merge-base", "--is-ancestor", bound, head).returncode:', "if False:"),
    ("precheck evidence-only", 'if not p.startswith((f".orchestration/{t}/", *exempt))', "if False"),
    ("allowed-files", "return re.fullmatch(rx, path) is not None", "return True"),
    ("caps outside", "if outside and out_lines > int(outside.group(1)):", "if False:"),
    ("caps tests", "if tests and test_lines > int(tests.group(1)):", "if False:"),
    ("caps wording", r"(?: \([^)]*\))?", ""),
    ("checker lines", 'return [("checker", ln) for ln in lines if not re.fullmatch(r"C1 task_id .* != file task", ln)]', "return []"),
    ("checker verdict", 'if (out[:1], run.returncode) not in ((["task.md: OK"], 0), (["task.md: FAIL"], 1)):', "if False:"),
    ("task-id", 'if fm.get("task_id") != t:', "if False:"),
    ("git listing", "    if out.returncode:", "    if False:"),
    ("C1 filter", r' if not re.fullmatch(r"C1 task_id .* != file task", ln)', ""),
    ("checker fed the head copy", "found += checker(root, data) if dispatched else []", "found += checker(root, copy)"),
    ("chain counts with the successor alone", "if p in policies and p != t and authentic and policies[p][2]", "if p in policies and p != t and authentic"),
    ("precheck with renames", '"--name-only", "--no-renames", bound, head', '"--name-only", bound, head'),
    ("self-touch warning", "for path in sorted(set(changed) & set(RUNS)):", "for path in []:"),
    ("reset_of lineage", "    targets = [t for t in targets if t not in later]\n", ""),
    ("lineage exempt", "not p.startswith(exempt) and ", ""),
]
for name, old, new in MUTANTS:
    assert original.count(old) == 1, name
    script.write_text(original.replace(old, new))
    run = subprocess.run([sys.executable, "-m", "unittest", "tests.unit.test_regime_ci"], cwd=root, capture_output=True, text=True)
    print(f"{name}: {run.stderr.strip().splitlines()[-1]}")
script.write_text(original)
--- run
task-copy (base dispatched): FAILED (failures=3)
task-copy (result.txt): FAILED (failures=1)
dispatched read at the base: FAILED (failures=2)
REGIME_REQUIRE_DISPATCHED: FAILED (failures=2)
policy allowed_files: FAILED (failures=1)
policy reset_of exempt: FAILED (failures=2)
checkout at the base: FAILED (failures=1)
records-only by content: FAILED (failures=2)
precheck sha: FAILED (failures=1)
precheck 40-hex: FAILED (failures=1)
precheck non-ancestor: FAILED (failures=2)
precheck evidence-only: FAILED (failures=3)
allowed-files: FAILED (failures=5)
caps outside: FAILED (failures=2)
caps tests: FAILED (failures=1)
caps wording: FAILED (failures=1)
checker lines: FAILED (failures=1)
checker verdict: FAILED (failures=2)
task-id: FAILED (failures=1)
git listing: FAILED (failures=1)
C1 filter: FAILED (failures=6)
checker fed the head copy: FAILED (failures=2)
chain counts with the successor alone: FAILED (failures=1)
precheck with renames: FAILED (failures=1)
self-touch warning: FAILED (failures=1)
reset_of lineage: FAILED (failures=1)
lineage exempt: FAILED (failures=2)
[exit 0]
```
## 6. Item 8: the job's command line in an isolated checkout of the base sha, with the candidate verifier installed for the run and the base's checker; the head is data (the helper, then its run)
```console
$ cat "$TMPDIR/regime-bootstrap.sh"; echo "--- run"; bash "$TMPDIR/regime-bootstrap.sh" 2>&1 | sed "s|$TMPDIR|\$TMPDIR|g"
#!/bin/bash
# a02 item 8: the job's command line in an isolated checkout of the PR's base, with the reviewed candidate verifier
# installed for this run (the base has none yet), the base's checker, and the head as data (its commit sha only).
set -u
BASE_SHA=$(git rev-parse origin/main)
HEAD_SHA=${1:-$(git rev-parse HEAD)}
W="$TMPDIR/regime-bootstrap"
echo "premise 6: git cat-file -e origin/main:.github/workflows/regime.yml"
git cat-file -e origin/main:.github/workflows/regime.yml; echo "exit $?"
git worktree add -q --detach "$W" "$BASE_SHA"
cp scripts/orchestrator/regime-ci.py "$W/scripts/orchestrator/regime-ci.py"
echo "base checkout $(git -C "$W" rev-parse HEAD) (BASE_SHA=$BASE_SHA); head HEAD_SHA=$HEAD_SHA"
echo "candidate verifier: scripts/orchestrator/regime-ci.py at $(git rev-parse --short=12 HEAD) sha256 $(shasum -a 256 scripts/orchestrator/regime-ci.py | cut -d' ' -f1)"
echo "base checker: $(git -C "$W" rev-parse --short=12 HEAD):scripts/orchestrator/task-consistency-check.py sha256 $(shasum -a 256 "$W/scripts/orchestrator/task-consistency-check.py" | cut -d' ' -f1)"
echo "\$ uv run --no-config --no-project --with pyyaml python -I scripts/orchestrator/regime-ci.py --base \"\${BASE_SHA}\" --head \"\${HEAD_SHA}\""
(cd "$W" && uv run --no-config --no-project --with pyyaml python -I scripts/orchestrator/regime-ci.py --base "${BASE_SHA}" --head "${HEAD_SHA}"); rc=$?
echo "exit $rc"
git worktree remove --force "$W"
exit $rc
--- run
premise 6: git cat-file -e origin/main:.github/workflows/regime.yml
fatal: path '.github/workflows/regime.yml' exists on disk, but not in 'origin/main'
exit 128
base checkout 3e41e36abc949acd7e6b4859c1a22df9e665c8d4 (BASE_SHA=3e41e36abc949acd7e6b4859c1a22df9e665c8d4); head HEAD_SHA=1ee15af1a159b45baefcd5505f816f9bbcccef98
candidate verifier: scripts/orchestrator/regime-ci.py at 1ee15af1a159 sha256 1ea737bab4ca1d17f51683b3c758a26f1af7caf8597171f9c1062c63f31861cd
base checker: 3e41e36abc94:scripts/orchestrator/task-consistency-check.py sha256 0f84a229bced899c51bfcb7b627aea8c98879b72fd14d7f2556f1e96f7d63234
$ uv run --no-config --no-project --with pyyaml python -I scripts/orchestrator/regime-ci.py --base "${BASE_SHA}" --head "${HEAD_SHA}"
regime-ci: warning: the diff changes .github/workflows/regime.yml; this run executed the base's version, the audit reads the change
regime-ci: warning: the diff changes scripts/orchestrator/regime-ci.py; this run executed the base's version, the audit reads the change
regime-ci: warning: dotfiles-T133-regime-ci-a02: task copy unverifiable (no dispatched text at base)
regime-ci: warning: dotfiles-T133-regime-ci-a02: checker skipped: the copy is unverifiable, and the base's checker reads only the base's text
regime-ci: warning: dotfiles-T133-regime-ci-a02: precheck absent
regime-ci: ok 1 task(s)
exit 0
[exit 0]
```
## 7. make format: the shfmt step fails on 12 tracked files, the same on origin/main; the steps after it pass on this branch's files
```console
$ make format > "$TMPDIR/fmt.txt" 2>&1; echo "make format exit $?"; /usr/bin/grep -E "^diff " "$TMPDIR/fmt.txt" | awk "{print \$3}" | sort -u > "$TMPDIR/fmt-files.txt"; cat "$TMPDIR/fmt-files.txt"; git diff --name-only origin/main...HEAD | /usr/bin/grep -c -x -F -f "$TMPDIR/fmt-files.txt" || echo "none of them is this branch's"; for f in $(cat "$TMPDIR/fmt-files.txt"); do git show "origin/main:$f" > "$TMPDIR/m.sh" 2>/dev/null && shfmt --indent 4 --space-redirects -d "$TMPDIR/m.sh" > /dev/null; echo "$f origin/main shfmt exit $?"; done; ruff format --config ruff.toml --check scripts/orchestrator/regime-ci.py tests/unit/test_regime_ci.py tests/unit/test_workflow_security.py; prettier --check .github/workflows/regime.yml .orchestration/$T/*.md 2>&1 | tail -n 1
make format exit 2
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
0
none of them is this branch's
.orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/pr-cost.sh origin/main shfmt exit 1
.orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/resolve-threads.sh origin/main shfmt exit 1
.orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-advisory.sh origin/main shfmt exit 1
.orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-review.sh origin/main shfmt exit 1
.orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/sandbox-scan.sh origin/main shfmt exit 1
.orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/boundary.sh origin/main shfmt exit 1
.orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/ff-main.sh origin/main shfmt exit 1
.orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-audit.sh origin/main shfmt exit 1
.orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-gate.sh origin/main shfmt exit 1
.orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/t717-prep.sh origin/main shfmt exit 1
home/dot_claude/hooks/executable_project-map-reload.sh origin/main shfmt exit 1
tests/install/macos/common/brew.bats origin/main shfmt exit 1
3 files already formatted
All matched files use Prettier code style!
[exit 0]
```
## 8. ruff check; and test_workflow_security.py against origin/main: exactly the one EXPECTED_PERMISSIONS entry
```console
$ ruff check --config ruff.toml scripts/orchestrator/regime-ci.py tests/unit/test_regime_ci.py; git diff origin/main...HEAD -- tests/unit/test_workflow_security.py | /usr/bin/grep "^[+-][^+-]"
All checks passed!
+    "regime.yml": {"contents": "read"},
[exit 0]
```
## 9. Caps: git diff --numstat origin/main...HEAD, summed, and the changed-file inventory
```console
$ git diff --numstat origin/main...HEAD; git diff --numstat origin/main...HEAD | awk -F "\t" "\$3 ~ /^\\.orchestration\\// {next} \$3 ~ /^tests\\// {t += \$1 + \$2; next} {o += \$1 + \$2} END {printf \"outside tests/ and .orchestration/: %d of 330\nunder tests/: %d of 480\n\", o, t}"
42	0	.github/workflows/regime.yml
107	0	.orchestration/dotfiles-T133-regime-ci-a01/dotfiles-T133-regime-ci-a01-worker-crit.json
16	0	.orchestration/dotfiles-T133-regime-ci-a01/dotfiles-T133-regime-ci-a01-worker-review-receipt.md
16	0	.orchestration/dotfiles-T133-regime-ci-a01/learning.md
38	0	.orchestration/dotfiles-T133-regime-ci-a01/pr-body.md
134	0	.orchestration/dotfiles-T133-regime-ci-a01/report.md
35	0	.orchestration/dotfiles-T133-regime-ci-a01/sandbox.md
250	0	.orchestration/dotfiles-T133-regime-ci-a01/validation.md
193	0	.orchestration/dotfiles-T133-regime-ci-a02/task.md
282	0	scripts/orchestrator/regime-ci.py
404	0	tests/unit/test_regime_ci.py
1	0	tests/unit/test_workflow_security.py
outside tests/ and .orchestration/: 324 of 330
under tests/: 405 of 480
[exit 0]
```
## 11. Premise 5, replayed through gh (outside the sandbox): the ruleset's required contexts do not include regime
```console
$ gh api repos/mryfmo/dotfiles/rulesets/24397953 --jq '[.rules[]|select(.type=="required_status_checks")|.parameters.required_status_checks[].context]|map(select(.=="regime"))|length'; gh api repos/mryfmo/dotfiles/rulesets/24397953 --jq '[.rules[]|select(.type=="required_status_checks")|.parameters.required_status_checks[].context]'
0
["test (ubuntu-24.04, server)","test (ubuntu-24.04, client)","test (macos-14, client)","public-bootstrap (ubuntu-24.04, server)","public-bootstrap (ubuntu-24.04, client)","validate","public-bootstrap (macos-14, client)"]
[exit 0]
```
