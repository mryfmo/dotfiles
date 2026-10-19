---
task_id: dotfiles-T129-normalised-comparison-lint-followup-a03
seat: claude-standard-dot-a008
code_head: 77bb5753
previous_head: c0eb536cd33b53084ae86d17ec66e82b476f3092
---

# Validation: dotfiles-T129-normalised-comparison-lint-followup-a03

- Every block ran inside the sandbox from this worktree on `lint/normalised-comparisons-followup-a01` at the code head `77bb5753`. Each block prints its commands, their verbatim output and the block's last exit status. The only later commit adds this directory's records.
- `MAIN` names the main checkout, `T` the task id, and `OLD` the chain's head `c0eb536c`. The scratch worktrees under `$TMPDIR` are removed after their block with `git worktree remove --force`.
- **Red, then green:**
  - §5 is red at `c0eb536c`: the checkout lint fails on the unchanged `regime-ci.py`, and the five named tests fail.
  - §6 and §6a are green at the code head.
- **`make format` exits 2, an inherited failure.** It flags the same files at the merge-base `b22a5580` (§10a) and is reported as a failure, not as passing.

## 1. Task file (sha256 8356dfb5…) and the branch copy
```console
$ shasum -a 256 "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md"; cmp "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md" && echo byte-identical
8356dfb5cd99223b1bbdda0eb3cc4fe5ba485f69006b81ebc2446ec034a4e5ce  ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-followup-a03.md
8356dfb5cd99223b1bbdda0eb3cc4fe5ba485f69006b81ebc2446ec034a4e5ce  .orchestration/dotfiles-T129-normalised-comparison-lint-followup-a03/task.md
byte-identical
[exit 0]
```
## 1a. The task-consistency check on the dispatched file
```console
$ uv run --offline --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root "$PWD" "$MAIN/.orchestration/tasks/$T.md"
dotfiles-T129-normalised-comparison-lint-followup-a03.md: OK
[exit 0]
```
## 2. Branch, origin/main, merge-base and this task's commits on the chain head c0eb536c
```console
$ git branch --show-current; git rev-parse HEAD origin/main; git merge-base origin/main HEAD; git log --oneline $OLD..HEAD
lint/normalised-comparisons-followup-a01
77bb5753436d1884ec32540fa72c3ca4faeec4e1
b22a5580d0778e57a66d3f75c76e3c55b88701e1
b22a5580d0778e57a66d3f75c76e3c55b88701e1
77bb5753 test(lint): the no-flag changed set is origin/main...HEAD in a real repository after update-branch, a rename changes both paths, a missing base fails closed; the checkout test matches warned paths exactly (T129 normalised-comparison-lint followup a03, worker review)
4bb6092d feat(lint): the comparison lint guards the files a change touches: --changed (default origin/main...HEAD through an isolated system git) fails a changed file's unbaselined hit or stale row and warns for unchanged files; --all reports everything (T129 normalised-comparison-lint followup a03)
6db2187c test(lint): the changed files are clean against the baseline; drift in an unchanged file warns; a changed file's hit or stale row fails; --all reports everything (T129 normalised-comparison-lint followup a03)
088f377e chore(orchestration): the C3 reset copy: the a03 task copy replaces a01's (T129 normalised-comparison-lint followup a03)
[exit 0]
```
## 3. The C3 reset copy (first push): the a01 copy leaves, the a03 copy is added
```console
$ for f in .orchestration/dotfiles-T129-normalised-comparison-lint-followup-a01/task.md .orchestration/$T/task.md; do git cat-file -e "HEAD:$f" 2> /dev/null && echo "present at HEAD: $f" || echo "absent at HEAD: $f"; done; git show --stat --format="%h %s" 088f377e | cut -c1-150
absent at HEAD: .orchestration/dotfiles-T129-normalised-comparison-lint-followup-a01/task.md
present at HEAD: .orchestration/dotfiles-T129-normalised-comparison-lint-followup-a03/task.md
088f377e chore(orchestration): the C3 reset copy: the a03 task copy replaces a01's (T129 normalised-comparison-lint followup a03)

 .../task.md                                        |  83 ------------
 .../task.md                                        | 139 +++++++++++++++++++++
 2 files changed, 139 insertions(+), 83 deletions(-)
[exit 0]
```
## 4. The Check's measurement at c0eb536c (git diff --numstat b22a5580...c0eb536c, outside tests/ and .orchestration/ with the baseline, and under tests/)
```console
$ git diff --numstat b22a5580...$OLD -- . ":!.orchestration"; git diff --numstat b22a5580...$OLD | awk -F "\t" "\$3 ~ /^\\.orchestration\\// {next} \$3 ~ /^tests\\// {t += \$1 + \$2; next} {o += \$1 + \$2} END {printf \"outside: %d, under tests/: %d\n\", o, t}"
93	0	scripts/lint-comparisons-baseline.tsv
200	0	scripts/lint-comparisons.py
271	0	tests/unit/test_lint_comparisons.py
outside: 293, under tests/: 271
[exit 0]
```
## 5. RED at c0eb536c, in a scratch worktree: the checkout lint fails on the unchanged scripts/orchestrator/regime-ci.py, then the five named tests (this head's test file, c0eb536c's script)
```console
$ cd "$R" && git rev-parse --short=8 HEAD && uv run --no-project python -I scripts/lint-comparisons.py; echo "lint exit $?"; git -C "$R" diff --quiet origin/main...$OLD -- scripts/orchestrator/regime-ci.py && echo "regime-ci.py is unchanged by PR #415"; git -C "$OLDPWD" show HEAD:tests/unit/test_lint_comparisons.py > tests/unit/test_lint_comparisons.py; uv run python -m unittest $NEW5 2>&1 | /usr/bin/grep -E "^(FAIL|ERROR):|^AssertionError|^Ran|^(OK|FAILED)|^usage|error: unrecognized" | sed -E "s/ \(tests\.unit\.test_lint_comparisons\.LintComparisonsTest\.[a-z_]+\)//" | cut -c1-200
c0eb536c
scripts/orchestrator/regime-ci.py:65: R6 an identifier is interpolated into a regex (grep -E on $name; re.* on an f-string)
scripts/orchestrator/regime-ci.py:71: R4 Python compares a path or URL by its string form
scripts/orchestrator/regime-ci.py:72: R4 Python compares a path or URL by its string form
scripts/orchestrator/regime-ci.py:90: R4 Python compares a path or URL by its string form
scripts/orchestrator/regime-ci.py:246: R4 Python compares a path or URL by its string form
lint exit 1
regime-ci.py is unchanged by PR #415
FAIL: test_the_changed_files_are_clean_against_the_baseline
AssertionError: Tuples differ: (0, '') != (1, '')
FAIL: test_a_hit_main_introduced_in_an_unchanged_file_passes_with_a_warning
AssertionError: 0 != 2 : usage: lint-comparisons.py [-h] [--list-rules] [--baseline BASELINE]
lint-comparisons.py: error: unrecognized arguments: --changed other.sh
FAIL: test_a_hit_in_a_changed_file_fails
AssertionError: 1 != 2 : usage: lint-comparisons.py [-h] [--list-rules] [--baseline BASELINE]
lint-comparisons.py: error: unrecognized arguments: --changed r1.sh other.sh
FAIL: test_a_stale_row_for_a_changed_file_fails
AssertionError: Tuples differ: (1, 'stale baseline row r1.sh R1\n') != (2, '')
lint-comparisons.py: error: unrecognized arguments: --changed r1.sh
FAIL: test_a_stale_row_for_an_unchanged_file_warns
AssertionError: 0 != 2 : usage: lint-comparisons.py [-h] [--list-rules] [--baseline BASELINE]
lint-comparisons.py: error: unrecognized arguments: --changed other.sh
Ran 5 tests in 0.554s
FAILED (failures=5)
[exit 0]
```
## 6. GREEN: the Check's unit command at HEAD, verbose
```console
$ git rev-parse --short=8 HEAD; uv run python -m unittest tests/unit/test_lint_comparisons.py -v 2>&1 | /usr/bin/grep -E "\.\.\. |^Ran|^(OK|FAILED)"
77bb5753
test_a_baseline_row_is_consumed_once_so_a_duplicate_hit_fails (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_baseline_row_is_consumed_once_so_a_duplicate_hit_fails) ... ok
test_a_baseline_row_matching_no_hit_fails_as_stale (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_baseline_row_matching_no_hit_fails_as_stale) ... ok
test_a_hit_in_a_changed_file_fails (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_hit_in_a_changed_file_fails) ... ok
test_a_hit_main_introduced_in_an_unchanged_file_passes_with_a_warning (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_hit_main_introduced_in_an_unchanged_file_passes_with_a_warning) ... ok
test_a_jq_normaliser_name_inside_a_string_literal_is_no_application (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_jq_normaliser_name_inside_a_string_literal_is_no_application) ... ok
test_a_normaliser_is_matched_by_its_qualified_name_so_a_foreign_receiver_fails (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_normaliser_is_matched_by_its_qualified_name_so_a_foreign_receiver_fails) ... ok
test_a_single_quoted_jq_option_value_is_not_read_as_the_program (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_single_quoted_jq_option_value_is_not_read_as_the_program) ... ok
test_a_stale_row_for_a_changed_file_fails (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_stale_row_for_a_changed_file_fails) ... ok
test_a_stale_row_for_an_unchanged_file_warns (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_stale_row_for_an_unchanged_file_warns) ... ok
test_each_rule_refuses_its_fixture_and_each_normaliser_and_the_marker_are_accepted (tests.unit.test_lint_comparisons.LintComparisonsTest.test_each_rule_refuses_its_fixture_and_each_normaliser_and_the_marker_are_accepted) ... ok
test_every_f_string_interpolation_in_a_regex_is_escaped (tests.unit.test_lint_comparisons.LintComparisonsTest.test_every_f_string_interpolation_in_a_regex_is_escaped) ... ok
test_the_changed_files_are_clean_against_the_baseline (tests.unit.test_lint_comparisons.LintComparisonsTest.test_the_changed_files_are_clean_against_the_baseline) ... ok
test_the_jq_normaliser_is_required_on_each_operand_side (tests.unit.test_lint_comparisons.LintComparisonsTest.test_the_jq_normaliser_is_required_on_each_operand_side) ... ok
test_with_no_mode_flag_the_change_is_origin_main_to_head_and_a_missing_base_fails (tests.unit.test_lint_comparisons.LintComparisonsTest.test_with_no_mode_flag_the_change_is_origin_main_to_head_and_a_missing_base_fails) ... ok
Ran 14 tests in 5.177s
OK
[exit 0]
```
## 6a. The worker review P2: each mutant of the no-flag changed-set lookup fails test_with_no_mode_flag_the_change_is_origin_main_to_head_and_a_missing_base_fails, in a scratch worktree at HEAD (the mutant script, then its run)
```console
$ cat "$TMPDIR/mut-l03.py"; uv run --no-project python -I "$TMPDIR/mut-l03.py" "$Q"
# Each mutant breaks the no-flag changed-set lookup; the review round's test must fail on every one.
import subprocess, sys
from pathlib import Path
root = Path(sys.argv[1]); f = root / "scripts/lint-comparisons.py"; src = f.read_text()
M = {
    "the lookup returns an empty set": ('set(git(*diff) if args.changed is None', 'set(() if args.changed is None'),
    "no -z": ('"--no-renames", "-z", ', '"--no-renames", '),
    "the range reversed": ('"origin/main...HEAD")', '"HEAD...origin/main")'),
    "check=False": ('text=True, check=True)', 'text=True, check=False)'),
    "rename detection kept": ('"--name-only", "--no-renames", ', '"--name-only", '),
}
test = "tests.unit.test_lint_comparisons.LintComparisonsTest.test_with_no_mode_flag_the_change_is_origin_main_to_head_and_a_missing_base_fails"
for name, (a, b) in M.items():
    assert src.count(a) == 1, name
    f.write_text(src.replace(a, b))
    r = subprocess.run(["uv", "run", "python", "-m", "unittest", test], cwd=root, capture_output=True, text=True)
    print(f"{name}: {'killed' if r.returncode else 'SURVIVED'}")
f.write_text(src)
the lookup returns an empty set: killed
no -z: killed
the range reversed: killed
check=False: killed
rename detection kept: killed
[exit 0]
```
## 7. The Check's lint at HEAD, no mode flag: exit 0, the unchanged-file drift as warnings
```console
$ uv run --no-project python -I scripts/lint-comparisons.py; echo "lint exit $?"
warning: scripts/orchestrator/regime-ci.py:65: R6 an identifier is interpolated into a regex (grep -E on $name; re.* on an f-string)
warning: scripts/orchestrator/regime-ci.py:71: R4 Python compares a path or URL by its string form
warning: scripts/orchestrator/regime-ci.py:72: R4 Python compares a path or URL by its string form
warning: scripts/orchestrator/regime-ci.py:90: R4 Python compares a path or URL by its string form
warning: scripts/orchestrator/regime-ci.py:246: R4 Python compares a path or URL by its string form
warning: 5 unbaselined hit(s) and 0 stale row(s) in unchanged files
lint exit 0
[exit 0]
```
## 8. The Check's --all report at HEAD: every hit, baseline-matched ones marked, and every stale row; exit 0
```console
$ uv run --no-project python -I scripts/lint-comparisons.py --all; echo "lint --all exit $?"
home/dot_agents/skills/gh-comment-attach-files/scripts/attach_comment_files.py:559: R4 Python compares a path or URL by its string form (baseline)
home/dot_agents/skills/gh-comment-attach-files/scripts/attach_comment_files.py:575: R4 Python compares a path or URL by its string form (baseline)
home/dot_claude/hooks/executable_project-map-reload.sh:40: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
home/dot_claude/hooks/executable_project-map-reload.sh:48: R3 jq compares a URL or path by its string form (baseline)
home/dot_claude/hooks/executable_project-map-reload.sh:56: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
home/dot_local/bin/common/executable_agent-session-staleness:71: R4 Python compares a path or URL by its string form (baseline)
home/dot_local/bin/common/executable_herdr-agents:416: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
home/dot_local/bin/common/executable_herdr-agents:539: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
home/dot_local/bin/common/executable_herdr-agents:758: R3 jq compares a URL or path by its string form (baseline)
home/dot_local/bin/common/executable_herdr-agents:760: R3 jq compares a URL or path by its string form (baseline)
home/dot_local/bin/common/executable_herdr-agents:992: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
home/dot_local/bin/common/executable_herdr-agents:1186: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
home/dot_local/bin/common/executable_herdr-agents:1233: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
home/dot_local/bin/common/executable_herdr-agents:1309: R3 jq compares a URL or path by its string form (baseline)
home/dot_local/bin/common/executable_herdr-agents:1395: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
home/dot_local/bin/common/executable_herdr-agents:1717: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
home/dot_local/bin/common/executable_herdr-agents:1843: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
home/dot_local/bin/common/executable_herdr-agents:1846: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
home/dot_local/bin/common/executable_herdr-agents:2050: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
home/dot_local/bin/common/executable_herdr-agents:2117: R6 an identifier is interpolated into a regex (grep -E on $name; re.* on an f-string) (baseline)
home/dot_local/bin/common/executable_remove-agent-asset:82: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
home/dot_local/bin/common/executable_remove-agent-asset:101: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
home/dot_local/bin/common/executable_remove-agent-asset:211: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
home/dot_local/bin/common/executable_ua-symbol-coverage:90: R4 Python compares a path or URL by its string form (baseline)
home/dot_local/bin/common/executable_ua-symbol-coverage:92: R4 Python compares a path or URL by its string form (baseline)
home/dot_local/bin/common/executable_ua-symbol-coverage:94: R4 Python compares a path or URL by its string form (baseline)
home/dot_local/bin/common/executable_ua-symbol-coverage:170: R4 Python compares a path or URL by its string form (baseline)
home/dot_local/bin/common/executable_ua-symbol-coverage:172: R4 Python compares a path or URL by its string form (baseline)
home/dot_local/bin/common/executable_ua-symbol-coverage:218: R4 Python compares a path or URL by its string form (baseline)
home/dot_local/bin/common/executable_ua-symbol-coverage:230: R4 Python compares a path or URL by its string form (baseline)
home/dot_local/bin/common/executable_ua-symbol-coverage:236: R4 Python compares a path or URL by its string form (baseline)
home/dot_local/bin/common/executable_ua-symbol-coverage:239: R4 Python compares a path or URL by its string form (baseline)
home/dot_local/bin/common/executable_ua-symbol-coverage:241: R4 Python compares a path or URL by its string form (baseline)
install/ubuntu/client/default_shell.sh:17: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
install/ubuntu/common/aws_cli.sh:66: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
install/ubuntu/common/aws_cli.sh:81: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
install/ubuntu/common/aws_cli.sh:161: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
scripts/agent-stop-gate.sh:114: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
scripts/agent-stop-gate.sh:126: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
scripts/check-agent-runtime.py:133: R4 Python compares a path or URL by its string form (baseline)
scripts/check-agent-runtime.py:134: R4 Python compares a path or URL by its string form (baseline)
scripts/check-agent-runtime.py:677: R4 Python compares a path or URL by its string form (baseline)
scripts/check-agent-runtime.py:679: R4 Python compares a path or URL by its string form (baseline)
scripts/check-regime-boundary.sh:191: R3 jq compares a URL or path by its string form (baseline)
scripts/generate-agent-configs.py:1378: R4 Python compares a path or URL by its string form (baseline)
scripts/generate-docs.sh:129: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
scripts/generate-docs.sh:145: R2 shell case matches a path or URL operand by its string form (baseline)
scripts/generate-docs.sh:518: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
scripts/gh-auth.sh:50: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
scripts/lib/asset-manifest.sh:75: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
scripts/lib/github-release.sh:28: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
scripts/orchestrator/chain-integrate.sh:69: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
scripts/orchestrator/ci-rerun.sh:117: R6 an identifier is interpolated into a regex (grep -E on $name; re.* on an f-string) (baseline)
scripts/orchestrator/dispatch.sh:109: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
scripts/orchestrator/dispatch.sh:190: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
scripts/orchestrator/dispatch.sh:202: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
scripts/orchestrator/dispatch.sh:209: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
scripts/orchestrator/dispatch.sh:334: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
scripts/orchestrator/ledger-check.py:25: R4 Python compares a path or URL by its string form (baseline)
scripts/orchestrator/local-review.sh:82: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
scripts/orchestrator/local-review.sh:83: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
scripts/orchestrator/orch-gate.sh:72: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
scripts/orchestrator/pr-cost.sh:49: R6 an identifier is interpolated into a regex (grep -E on $name; re.* on an f-string) (baseline)
scripts/orchestrator/regime-ci.py:65: R6 an identifier is interpolated into a regex (grep -E on $name; re.* on an f-string)
scripts/orchestrator/regime-ci.py:71: R4 Python compares a path or URL by its string form
scripts/orchestrator/regime-ci.py:72: R4 Python compares a path or URL by its string form
scripts/orchestrator/regime-ci.py:90: R4 Python compares a path or URL by its string form
scripts/orchestrator/regime-ci.py:246: R4 Python compares a path or URL by its string form
scripts/orchestrator/resolve-threads.sh:45: R3 jq compares a URL or path by its string form (baseline)
scripts/orchestrator/task-consistency-check.py:56: R4 Python compares a path or URL by its string form (baseline)
scripts/orchestrator/task-consistency-check.py:66: R6 an identifier is interpolated into a regex (grep -E on $name; re.* on an f-string) (baseline)
scripts/orchestrator/task-consistency-check.py:118: R4 Python compares a path or URL by its string form (baseline)
scripts/require-crit-review.py:159: R4 Python compares a path or URL by its string form (baseline)
scripts/require-crit-review.py:251: R4 Python compares a path or URL by its string form (baseline)
scripts/require-crit-review.py:258: R4 Python compares a path or URL by its string form (baseline)
scripts/require-crit-review.py:260: R4 Python compares a path or URL by its string form (baseline)
scripts/require-crit-review.py:1066: R4 Python compares a path or URL by its string form (baseline)
scripts/update-agent-assets.sh:274: R2 shell case matches a path or URL operand by its string form (baseline)
scripts/update-agent-assets.sh:950: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
scripts/update-agent-assets.sh:959: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
scripts/update-agent-assets.sh:982: R2 shell case matches a path or URL operand by its string form (baseline)
scripts/upgrade-tools.sh:283: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
scripts/validate-agent-assets.py:115: R4 Python compares a path or URL by its string form (baseline)
scripts/validate-agent-assets.py:268: R4 Python compares a path or URL by its string form (baseline)
scripts/validate-agent-assets.py:317: R4 Python compares a path or URL by its string form (baseline)
scripts/validate-agent-assets.py:321: R4 Python compares a path or URL by its string form (baseline)
scripts/validate-agent-assets.py:377: R4 Python compares a path or URL by its string form (baseline)
scripts/validate-agent-assets.py:403: R4 Python compares a path or URL by its string form (baseline)
scripts/validate-agent-assets.py:475: R4 Python compares a path or URL by its string form (baseline)
scripts/validate-agent-assets.py:504: R4 Python compares a path or URL by its string form (baseline)
scripts/validate-agent-assets.py:506: R4 Python compares a path or URL by its string form (baseline)
scripts/validate-agent-assets.py:509: R4 Python compares a path or URL by its string form (baseline)
scripts/validate-agent-assets.py:511: R4 Python compares a path or URL by its string form (baseline)
scripts/validate-agent-assets.py:823: R4 Python compares a path or URL by its string form (baseline)
scripts/validate-agent-assets.py:1059: R4 Python compares a path or URL by its string form (baseline)
scripts/validate-agent-assets.py:1330: R4 Python compares a path or URL by its string form (baseline)
scripts/validate-agent-assets.py:1405: R4 Python compares a path or URL by its string form (baseline)
scripts/validate-agent-assets.py:1408: R6 an identifier is interpolated into a regex (grep -E on $name; re.* on an f-string) (baseline)
lint --all exit 0
[exit 0]
```
## 9. The baseline is unchanged since c0eb536c and holds no regime-ci.py row; the rule table and LIMIT line are unchanged
```console
$ git diff --quiet $OLD HEAD -- scripts/lint-comparisons-baseline.tsv && echo "baseline unchanged since c0eb536c"; echo "regime-ci.py rows: $(/usr/bin/grep -c regime-ci scripts/lint-comparisons-baseline.tsv)"; git show $OLD:scripts/lint-comparisons.py > "$TMPDIR/lint-old.py"; uv run --no-project python -I "$TMPDIR/lint-old.py" --list-rules > "$TMPDIR/rules-old.txt"; uv run --no-project python -I scripts/lint-comparisons.py --list-rules > "$TMPDIR/rules-new.txt"; cmp "$TMPDIR/rules-old.txt" "$TMPDIR/rules-new.txt" && echo "--list-rules identical"; git diff $OLD HEAD -- scripts/lint-comparisons.py | /usr/bin/grep -E "^[-+](RULES|LIMIT|TOKEN|LITERAL|MARKER|SH_NORM|JQ_|PS|PGREP|GREP|PY_NORM|OPS) " || echo "no rule constant changed"
baseline unchanged since c0eb536c
regime-ci.py rows: 0
--list-rules identical
no rule constant changed
[exit 0]
```
## 10. ruff check on the script (the Check), ruff format --check on both files
```console
$ ruff check scripts/lint-comparisons.py; ruff format --config ruff.toml --check scripts/lint-comparisons.py tests/unit/test_lint_comparisons.py
All checks passed!
2 files already formatted
[exit 0]
```
## 10a. make format flags the same files at the merge-base b22a5580 (scratch worktree) as at HEAD, and none of this PR's; shfmt v3.14.1
```console
$ for each checkout: make format; echo exit; the files its diff names
77bb5753: make format exit 2; flagged: .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/pr-cost.sh .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/resolve-threads.sh .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-advisory.sh .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-review.sh .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/sandbox-scan.sh .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/boundary.sh .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/ff-main.sh .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-audit.sh .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-gate.sh .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/t717-prep.sh home/dot_claude/hooks/executable_project-map-reload.sh tests/install/macos/common/brew.bats 
b22a5580: make format exit 2; flagged: .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/pr-cost.sh .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/resolve-threads.sh .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-advisory.sh .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-review.sh .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/sandbox-scan.sh .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/boundary.sh .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/ff-main.sh .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-audit.sh .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-gate.sh .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/t717-prep.sh home/dot_claude/hooks/executable_project-map-reload.sh tests/install/macos/common/brew.bats 
[exit 0]
```
## 11. Caps over origin/main...HEAD (additions plus deletions; the baseline counts outside) and the changed-file inventory
```console
$ B=$(git merge-base origin/main HEAD); echo "merge-base ${B:0:8}"; git diff --numstat "$B...HEAD" -- . ":!.orchestration"; git diff --numstat "$B...HEAD" | awk -F "\t" "\$3 ~ /^\\.orchestration\\// {next} \$3 ~ /^tests\\// {t += \$1 + \$2; next} {o += \$1 + \$2} END {printf \"outside tests/ and .orchestration/: %d of 400\nunder tests/: %d of 450\n\", o, t}"; git diff --name-only "$B...HEAD" -- .orchestration | cut -d/ -f2 | sort | uniq -c
merge-base b22a5580
93	0	scripts/lint-comparisons-baseline.tsv
227	0	scripts/lint-comparisons.py
390	0	tests/unit/test_lint_comparisons.py
outside tests/ and .orchestration/: 320 of 400
under tests/: 390 of 450
  11 dotfiles-T129-normalised-comparison-lint-a01
   8 dotfiles-T129-normalised-comparison-lint-followup-a01
   1 dotfiles-T129-normalised-comparison-lint-followup-a03
[exit 0]
```
