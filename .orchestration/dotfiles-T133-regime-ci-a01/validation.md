---
task_id: dotfiles-T133-regime-ci-a01
seat: claude-standard-dot-a008
head: afd044f5
---

# Validation: dotfiles-T133-regime-ci-a01

Every command ran from the worktree `.claude/worktrees/worker-f` on the branch `tools/regime-ci-a01` at `afd044f5` (the merge of `origin/main` 3e41e36a after amendment 1), inside the sandbox, through a generator that prints each command, its verbatim output and its exit status (a block's status is its last command's), except §11 (premise 5, through gh outside the sandbox, pasted from its saved output) and §10 (the PR's own `regime` job, from `gh run view`). `MAIN` names the main checkout and `T` the task id. The scratch worktrees (`$R`, `$Q`, `$P`, `$M` under `$TMPDIR`) are removed after their block with `git worktree remove --force`. §6 runs the Check's command as the task states it (without `--no-config`, which only the workflow and the checker's run need).

## 1. Task file (amendment 1, sha256 0bca9954…) and task copy
```console
$ shasum -a 256 "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md"; cmp "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md" && echo byte-identical
0bca9954f0cefdc21c289249b9130d41d566c4eaadaf495565874868f04a402d  ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-regime-ci-a01.md
0bca9954f0cefdc21c289249b9130d41d566c4eaadaf495565874868f04a402d  .orchestration/dotfiles-T133-regime-ci-a01/task.md
byte-identical
[exit 0]
```
## 1a. The task-consistency check on the dispatched file
```console
$ uv run --offline --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root "$PWD" "$MAIN/.orchestration/tasks/$T.md"
dotfiles-T133-regime-ci-a01.md: OK
[exit 0]
```
## 2. Premises 1 to 4, replayed on origin/main (premise 5 needs gh: §11)
```console
$ B=$(git rev-parse origin/main); echo "origin/main=$B"; git ls-tree -r --name-only "$B" -- .github/workflows/regime.yml scripts/orchestrator/regime-ci.py tests/unit/test_regime_ci.py | wc -l; git show "$B:.github/workflows" > /dev/null; for f in $(git ls-tree --name-only "$B" .github/workflows/ | /usr/bin/grep "\.yaml$"); do git show "$B:$f"; done | /usr/bin/grep -h "uses: actions/checkout@\|uses: astral-sh/setup-uv@" | sed "s/^[- ]*//" | sort -u; git show "$B:scripts/orchestrator/task-consistency-check.py" | /usr/bin/grep -c "^C[0-9]*b\? "; git show "$B:scripts/orchestrator/result-precheck.sh" > /dev/null 2>&1 && echo present-on-main || echo absent-on-main
origin/main=3e41e36abc949acd7e6b4859c1a22df9e665c8d4
       0
uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7
uses: astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7 # v10.2.0
11
absent-on-main
[exit 0]
```
## 3. Branch, base and commits
```console
$ git branch --show-current; git rev-parse HEAD origin/main; git log --oneline origin/main..HEAD
tools/regime-ci-a01
afd044f5de3f2400e9ef20188ad66987fc53c168
3e41e36abc949acd7e6b4859c1a22df9e665c8d4
afd044f5 Merge branch 'main' of https://github.com/mryfmo/dotfiles into tools/regime-ci-a01
a060b4a2 docs(orchestration): T133 regime-ci a01: the task copy at amendment 1 (0bca9954)
26c50932 feat(orchestrator): regime-ci checks only the latest copy of a reset_of lineage (T133 regime-ci a01 amendment 1)
521516f4 test(ci): the workflow-security allowlist names regime.yml with contents: read (T133 regime-ci a01 amendment 1)
e88480c2 test(orchestrator): regime-ci checks only the latest copy of a reset_of lineage (T133 regime-ci a01 amendment 1)
a8eccfc7 docs(orchestration): T133 regime-ci a01: the worker evidence at 7e8851f0
7e8851f0 docs(orchestrator): regime-ci's usage line names --no-config (T133 regime-ci a01, worker re-review P3)
9a787b13 test(orchestrator): regime-ci's round-2 review cases: a reverted prechecked change, a verdict line with the wrong exit code, the checkout's uv config (T133 regime-ci a01)
a1c90c78 fix(orchestrator): regime-ci fails closed on every input it cannot validate (T133 regime-ci a01, worker review)
7311f004 test(orchestrator): regime-ci's fail-closed cases from the worker review (T133 regime-ci a01)
c6cc8f20 docs(orchestration): T133 regime-ci a01: the PR body
69a3128f fix(orchestrator): regime-ci drops the checker's C1 file-name line for any task_id, since task-id checks the directory (T133 regime-ci a01)
467004a2 test(orchestrator): regime-ci reports a copy whose task_id is not its directory (T133 regime-ci a01)
8e326842 docs(orchestration): T133 regime-ci a01: the task copy
811dd3ce feat(orchestrator): the regime CI job checks a PR against its task copy (T133 regime-ci a01, plan 024 P1-11)
159af0ca test(orchestrator): the regime CI job's tests (T133 regime-ci a01, plan 024 P1-11)
[exit 0]
```
## 4. RED: the tests commit 159af0ca (no regime-ci.py, no regime.yml), in a scratch worktree
```console
$ git -C "$R" log --oneline -1; ls "$R/scripts/orchestrator/regime-ci.py" "$R/.github/workflows/regime.yml" 2>&1 | sed "s|$R/||"; cd "$R" && uv run python -m unittest tests.unit.test_regime_ci 2>&1 | /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^(OK|FAILED)" | cut -c1-200
159af0ca test(orchestrator): the regime CI job's tests (T133 regime-ci a01, plan 024 P1-11)
ls: .github/workflows/regime.yml: No such file or directory
ls: scripts/orchestrator/regime-ci.py: No such file or directory
ERROR: test_the_regime_workflow_pins_its_actions_runs_on_the_pr_head_and_cancels_superseded_runs (tests.unit.test_regime_ci.RegimeCiTest.test_the_regime_workflow_pins_its_actions_runs_on_the_pr_head_a
FAIL: test_regime_ci_passes_a_records_only_pr_with_no_target (tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_passes_a_records_only_pr_with_no_target)
FAIL: test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr (tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr)
FAIL: test_regime_ci_warns_without_precheck_and_without_dispatched_text (tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_warns_without_precheck_and_without_dispatched_text)
Ran 4 tests in 0.900s
FAILED (failures=3, errors=1)
[exit 0]
```
## 4a. RED for the worker review: the tests at 7311f004 against 69a3128f's regime-ci.py (before the fail-closed re-plan), in a scratch worktree
```console
$ git -C "$Q" diff --quiet 69a3128f -- scripts/orchestrator/regime-ci.py && echo "regime-ci.py identical to 69a3128f"; cd "$Q" && uv run python -m unittest tests.unit.test_regime_ci -v 2>&1 | /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^(OK|FAILED)" | sed -E "s/ \\(tests\\.unit\\.test_regime_ci\\.RegimeCiTest\\.[a-z_]+\\)//" | cut -c1-200
regime-ci.py identical to 69a3128f
FAIL: test_regime_ci_refuses_a_checkout_not_at_the_head_and_a_diff_git_cannot_list
FAIL: test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr (case='precheck late')
FAIL: test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr (case='precheck symbolic')
FAIL: test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr (case='precheck none')
FAIL: test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr (case='caps worded')
FAIL: test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr (case='checker crash')
FAIL: test_regime_ci_warns_without_precheck_and_without_dispatched_text
Ran 7 tests in 15.391s
FAILED (failures=7)
[exit 0]
```
## 4b. RED for amendment 1: the lineage test at e88480c2 against 7e8851f0's regime-ci.py (before the reset_of rule), in a scratch worktree
```console
$ git -C "$P" diff --quiet 7e8851f0 -- scripts/orchestrator/regime-ci.py && echo "regime-ci.py identical to 7e8851f0"; cd "$P" && uv run python -m unittest tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_checks_only_the_latest_copy_of_a_reset_of_lineage 2>&1 | /usr/bin/grep -E "^(FAIL|ERROR):|^AssertionError|^Ran|^(OK|FAILED)" | cut -c1-220
regime-ci.py identical to 7e8851f0
FAIL: test_regime_ci_checks_only_the_latest_copy_of_a_reset_of_lineage (tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_checks_only_the_latest_copy_of_a_reset_of_lineage) (reset_of=True)
AssertionError: 0 != 1 : regime-ci: warning: t1-a01: precheck absent
Ran 1 test in 2.040s
FAILED (failures=1)
[exit 0]
```
## 4c. Amendment 1: tests/unit/test_workflow_security.py differs from origin/main by exactly the one EXPECTED_PERMISSIONS entry, and its tests pass with regime.yml
```console
$ git diff origin/main...HEAD -- tests/unit/test_workflow_security.py | /usr/bin/grep "^[+-][^+-]"; uv run python -m unittest tests.unit.test_workflow_security 2>&1 | tail -n 1
+    "regime.yml": {"contents": "read"},
OK
[exit 0]
```
## 5. GREEN: the Check's unit-test command on HEAD
```console
$ git rev-parse --short=8 HEAD; uv run python -m unittest tests.unit.test_regime_ci -v 2>&1 | /usr/bin/grep -E "\.\.\. |^Ran|^(OK|FAILED)"
afd044f5
test_regime_ci_checks_only_the_latest_copy_of_a_reset_of_lineage (tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_checks_only_the_latest_copy_of_a_reset_of_lineage) ... ok
test_regime_ci_checks_the_copy_against_result_txt_without_dispatched_text (tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_checks_the_copy_against_result_txt_without_dispatched_text) ... ok
test_regime_ci_passes_a_records_only_pr_with_no_target (tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_passes_a_records_only_pr_with_no_target) ... ok
test_regime_ci_refuses_a_checkout_not_at_the_head_and_a_diff_git_cannot_list (tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_refuses_a_checkout_not_at_the_head_and_a_diff_git_cannot_list) ... ok
test_regime_ci_reports_a_copy_whose_task_id_is_not_its_directory (tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_reports_a_copy_whose_task_id_is_not_its_directory) ... ok
test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr (tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr) ... ok
test_regime_ci_runs_the_checker_without_the_checkout_s_uv_config (tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_runs_the_checker_without_the_checkout_s_uv_config) ... ok
test_regime_ci_warns_without_precheck_and_without_dispatched_text (tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_warns_without_precheck_and_without_dispatched_text) ... ok
test_the_regime_workflow_pins_its_actions_runs_on_the_pr_head_and_cancels_superseded_runs (tests.unit.test_regime_ci.RegimeCiTest.test_the_regime_workflow_pins_its_actions_runs_on_the_pr_head_and_cancels_superseded_runs) ... ok
Ran 9 tests in 21.594s
OK
[exit 0]
```
## 5a. Each rule disabled in turn in a scratch worktree at HEAD: the test module fails for every mutant (the helper, then its run)
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
    ("task-copy (dispatched)", "if dispatched != copy:", "if False:"),
    ("task-copy (result.txt)", 'if token(result_text, "task_copy") != sha256(copy):', "if False:"),
    ("precheck sha", 'if token(result_text, "precheck") != sha256(data):', "if False:"),
    ("precheck 40-hex", 'if not isinstance(bound, str) or not re.fullmatch(r"[0-9a-f]{40}", bound):', "if not bound:"),
    ("precheck non-ancestor", 'if git(root, "merge-base", "--is-ancestor", bound, head).returncode:', "if False:"),
    ("precheck evidence-only", 'if not p.startswith((f".orchestration/{t}/", *exempt))', "if False"),
    ("allowed-files", "return re.fullmatch(rx, path) is not None", "return True"),
    ("caps outside", "if outside and out_lines > int(outside.group(1)):", "if False:"),
    ("caps tests", "if tests and test_lines > int(tests.group(1)):", "if False:"),
    ("caps wording", r"(?: \([^)]*\))?", ""),
    ("checker lines", 'found += [("checker", ln) for ln in lines]', "pass"),
    ("checker verdict", 'if (out[:1], run.returncode) not in ((["task.md: OK"], 0), (["task.md: FAIL"], 1)):', "if False:"),
    ("task-id", 'if fm.get("task_id") != t:', "if False:"),
    ("records-only", "if not stray or ", "if True or "),
    ("orchestration/ head", 'or os.environ.get("GITHUB_HEAD_REF", "").startswith("orchestration/")', ""),
    ("checkout", "if at != head:", "if False:"),
    ("git listing", "    if out.returncode:", "    if False:"),
    ("C1 filter", r'and not re.fullmatch(r"C1 task_id .* != file task", ln.strip())', ""),
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
task-copy (dispatched): FAILED (failures=1)
task-copy (result.txt): FAILED (failures=1)
precheck sha: FAILED (failures=1)
precheck 40-hex: FAILED (failures=1)
precheck non-ancestor: FAILED (failures=2)
precheck evidence-only: FAILED (failures=2)
allowed-files: FAILED (failures=2)
caps outside: FAILED (failures=2)
caps tests: FAILED (failures=1)
caps wording: FAILED (failures=1)
checker lines: FAILED (failures=1)
checker verdict: FAILED (failures=2)
task-id: FAILED (failures=1)
records-only: FAILED (failures=1)
orchestration/ head: FAILED (failures=1)
checkout: FAILED (failures=1)
git listing: FAILED (failures=1)
C1 filter: FAILED (failures=6)
self-touch warning: FAILED (failures=1)
reset_of lineage: FAILED (failures=1)
lineage exempt: FAILED (failures=1)
[exit 0]
```
## 6. The Check: regime-ci on this branch (its own task copy is the target; the precheck warning is expected until PR #411 merges)
```console
$ GITHUB_HEAD_REF=tools/regime-ci-a01 uv run --no-project --with pyyaml python -I scripts/orchestrator/regime-ci.py --base origin/main --head HEAD
regime-ci: warning: the diff changes .github/workflows/regime.yml, which this job runs; the audit reads that change
regime-ci: warning: the diff changes scripts/orchestrator/regime-ci.py, which this job runs; the audit reads that change
regime-ci: warning: dotfiles-T133-regime-ci-a01: task copy unverifiable (no dispatched text at head, no result.txt)
regime-ci: warning: dotfiles-T133-regime-ci-a01: precheck absent
regime-ci: ok 1 task(s)
[exit 0]
```
## 7. make format: the shfmt step fails on 12 tracked files, the same on origin/main (validation of T133 a01, §9); the steps after it pass on this branch's files
```console
$ make format > "$TMPDIR/fmt.txt" 2>&1; echo "make format exit $?"; /usr/bin/grep -E "^diff " "$TMPDIR/fmt.txt" | awk "{print \$3}" | sort -u; /usr/bin/grep -E "^diff " "$TMPDIR/fmt.txt" | awk "{print \$3}" | sort -u > "$TMPDIR/fmt-files.txt"; git diff --name-only origin/main...HEAD | /usr/bin/grep -c -x -F -f "$TMPDIR/fmt-files.txt" || echo "none of them is this branch's"; ruff format --config ruff.toml --check scripts/orchestrator/regime-ci.py tests/unit/test_regime_ci.py; prettier --check .github/workflows/regime.yml .orchestration/$T/*.md 2>&1 | tail -n 1
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
2 files already formatted
All matched files use Prettier code style!
[exit 0]
```
## 8. ruff check on the script and the tests
```console
$ ruff check --config ruff.toml scripts/orchestrator/regime-ci.py tests/unit/test_regime_ci.py
All checks passed!
[exit 0]
```
## 9. Caps: git diff --numstat origin/main...HEAD, summed
```console
$ git diff --numstat origin/main...HEAD; git diff --numstat origin/main...HEAD | awk -F "\t" "\$3 ~ /^\\.orchestration\\// {next} \$3 ~ /^tests\\// {t += \$1 + \$2; next} {o += \$1 + \$2} END {printf \"outside tests/ and .orchestration/: %d of 300\nunder tests/: %d of 450\n\", o, t}"
36	0	.github/workflows/regime.yml
107	0	.orchestration/dotfiles-T133-regime-ci-a01/dotfiles-T133-regime-ci-a01-worker-crit.json
16	0	.orchestration/dotfiles-T133-regime-ci-a01/dotfiles-T133-regime-ci-a01-worker-review-receipt.md
16	0	.orchestration/dotfiles-T133-regime-ci-a01/learning.md
38	0	.orchestration/dotfiles-T133-regime-ci-a01/pr-body.md
128	0	.orchestration/dotfiles-T133-regime-ci-a01/report.md
34	0	.orchestration/dotfiles-T133-regime-ci-a01/sandbox.md
103	0	.orchestration/dotfiles-T133-regime-ci-a01/task.md
215	0	.orchestration/dotfiles-T133-regime-ci-a01/validation.md
259	0	scripts/orchestrator/regime-ci.py
274	0	tests/unit/test_regime_ci.py
1	0	tests/unit/test_workflow_security.py
outside tests/ and .orchestration/: 295 of 300
under tests/: 275 of 450
[exit 0]
```
## 11. Premise 5, replayed through gh (outside the sandbox): the ruleset's required contexts do not include regime
```console
$ gh api repos/mryfmo/dotfiles/rulesets/24397953 --jq '[.rules[]|select(.type=="required_status_checks")|.parameters.required_status_checks[].context]|map(select(.=="regime"))|length'; gh api repos/mryfmo/dotfiles/rulesets/24397953 --jq '[.rules[]|select(.type=="required_status_checks")|.parameters.required_status_checks[].context]'
0
["test (ubuntu-24.04, server)","test (ubuntu-24.04, client)","test (macos-14, client)","public-bootstrap (ubuntu-24.04, server)","public-bootstrap (ubuntu-24.04, client)","validate","public-bootstrap (macos-14, client)"]
[exit 0]
```
