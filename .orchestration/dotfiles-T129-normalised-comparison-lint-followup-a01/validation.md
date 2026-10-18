---
task_id: dotfiles-T129-normalised-comparison-lint-followup-a01
seat: claude-standard-dot-a008
head: 1219ab10
pre_rebase_head: bb60ee84
---

# Validation: dotfiles-T129-normalised-comparison-lint-followup-a01

Every command ran from the worktree `.claude/worktrees/worker-f` on the branch `lint/normalised-comparisons-followup-a01` at `bb60ee84`, inside the sandbox, through `$TMPDIR/val.sh` (a generator that prints each command, its verbatim output and its exit status); `MAIN` names the main checkout, `T` the task id, `BASE` PR #387's head `7c8e7484`. The scratch worktrees (`$R`, `$V`, `$X`, `$Y`, `$B`, `$S`) live under `$TMPDIR` and are removed after their block with `git worktree remove --force`. A block's status is its last command's. The red tracked-tree test of §3 to §5 is the same with the base script and baseline (§5a); see the report.

§1 to §11 ran before Amendment 1, at the pre-rebase head `bb60ee84` on PR #387's head, and name the pre-rebase commits. §12 to §17 ran after the rebase onto `origin/main` `68f8a70a`, at `7fa5d112` (the baseline commit), from the same worktree inside the sandbox, through `$TMPDIR/val129r.sh` (the same block form; `OLD` is the pre-rebase tip `445c32dd`). §12a maps each pre-rebase commit to its rebased commit. §18 to §20 ran after `main` moved to `61231cd9` (#408): the merge 5c2ef021, the two rows it needed, and the Check again at `1219ab10`, through `$TMPDIR/val129m.sh`. §12c and §12d use scratch worktrees under `$TMPDIR`, removed after each run.

## 1. Task file (sha256 ab92d008…) and task copy
```console
$ shasum -a 256 "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md"; cmp "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md" && echo byte-identical
ab92d00811de646e00c996211970f6ec712dac711e24328510f3a43c829d7e0f  ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-followup-a01.md
ab92d00811de646e00c996211970f6ec712dac711e24328510f3a43c829d7e0f  .orchestration/dotfiles-T129-normalised-comparison-lint-followup-a01/task.md
byte-identical
[exit 0]
```
## 1a. The task-consistency check on the dispatched file
```console
$ uv run --offline --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root "$PWD" "$MAIN/.orchestration/tasks/$T.md"
dotfiles-T129-normalised-comparison-lint-followup-a01.md: OK
[exit 0]
```
## 2. Branch and base (stacked on PR #387's head 7c8e7484, as the TASK note says)
```console
$ git branch --show-current; git log --oneline "$BASE"..HEAD; git rev-parse HEAD "$BASE" origin/main; git merge-base --is-ancestor "$BASE" HEAD && echo "7c8e7484 is an ancestor of HEAD"
lint/normalised-comparisons-followup-a01
bb60ee84 fix(lint): an unbalanced double quote before the jq program is read as text, as the base read it (T129 followup a01 re-review)
a0563644 test(lint): jq named inside a double-quoted expansion with more text before its closing quote (T129 followup a01 re-review)
b6c47653 docs(orchestration): T129 normalised-comparison lint followup a01: the task copy and the worker evidence
1b56dc2b fix(lint): the jq program is the base scan's first single-quoted string that is no option's argument (T129 followup a01 review)
be2958cf test(lint): the forms the base jq scan read stay read; map(re.escape) and a jq comment (T129 followup a01 review)
37bf6a51 fix(lint): follow jq named through a variable or a substitution to its program (T129 followup a01)
979c0429 fix(lint): locate the jq program after its options, require a normaliser application per side, escape every interpolation (T129 followup a01)
a6518485 test(lint): one refusal fixture per owned row of the lint lineage's follow-up (T129 followup a01)
bb60ee84dd58527927dbe1366881e269faedf21a
7c8e748485e903ac2f4f8655c388e205c3260f22
a8a747af06b32ff1d0d1720467892f34d9465ae4
7c8e7484 is an ancestor of HEAD
[exit 0]
```
## 3. RED: the tests commit a6518485 (tests only, the base script) in a scratch worktree
```console
$ git -C "$R" log --oneline -1; git -C "$R" diff --stat "$BASE" a6518485; uv run --no-project python -I "$R/tests/unit/test_lint_comparisons.py" -v
a6518485 test(lint): one refusal fixture per owned row of the lint lineage's follow-up (T129 followup a01)
 tests/unit/test_lint_comparisons.py | 38 +++++++++++++++++++++++++++++++++++++
 1 file changed, 38 insertions(+)
test_a_baseline_row_is_consumed_once_so_a_duplicate_hit_fails (__main__.LintComparisonsTest.test_a_baseline_row_is_consumed_once_so_a_duplicate_hit_fails) ... ok
test_a_baseline_row_matching_no_hit_fails_as_stale (__main__.LintComparisonsTest.test_a_baseline_row_matching_no_hit_fails_as_stale) ... ok
test_a_jq_normaliser_name_inside_a_string_literal_is_no_application (__main__.LintComparisonsTest.test_a_jq_normaliser_name_inside_a_string_literal_is_no_application) ... FAIL
test_a_normaliser_is_matched_by_its_qualified_name_so_a_foreign_receiver_fails (__main__.LintComparisonsTest.test_a_normaliser_is_matched_by_its_qualified_name_so_a_foreign_receiver_fails) ... ok
test_a_single_quoted_jq_option_value_is_not_read_as_the_program (__main__.LintComparisonsTest.test_a_single_quoted_jq_option_value_is_not_read_as_the_program) ... FAIL
test_each_rule_refuses_its_fixture_and_each_normaliser_and_the_marker_are_accepted (__main__.LintComparisonsTest.test_each_rule_refuses_its_fixture_and_each_normaliser_and_the_marker_are_accepted) ... ok
test_every_f_string_interpolation_in_a_regex_is_escaped (__main__.LintComparisonsTest.test_every_f_string_interpolation_in_a_regex_is_escaped) ... FAIL
test_the_jq_normaliser_is_required_on_each_operand_side (__main__.LintComparisonsTest.test_the_jq_normaliser_is_required_on_each_operand_side) ... ok
test_the_tracked_tree_is_clean_against_the_baseline (__main__.LintComparisonsTest.test_the_tracked_tree_is_clean_against_the_baseline) ... FAIL

======================================================================
FAIL: test_a_jq_normaliser_name_inside_a_string_literal_is_no_application (__main__.LintComparisonsTest.test_a_jq_normaliser_name_inside_a_string_literal_is_no_application)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tmp/claude-501/red-a6518485/tests/unit/test_lint_comparisons.py", line 220, in test_a_jq_normaliser_name_inside_a_string_literal_is_no_application
    self.assert_refused_and_accepted(
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        "j.sh",
        ^^^^^^^
    ...<2 lines>...
        "jq -r 'def canonical_path: .; select((.url + \"/\" | canonical_path) == ($path | canonical_path))'\n",
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/tmp/claude-501/red-a6518485/tests/unit/test_lint_comparisons.py", line 200, in assert_refused_and_accepted
    self.assertEqual(1, result.returncode, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1 != 0 : 

======================================================================
FAIL: test_a_single_quoted_jq_option_value_is_not_read_as_the_program (__main__.LintComparisonsTest.test_a_single_quoted_jq_option_value_is_not_read_as_the_program)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tmp/claude-501/red-a6518485/tests/unit/test_lint_comparisons.py", line 207, in test_a_single_quoted_jq_option_value_is_not_read_as_the_program
    self.assert_refused_and_accepted(
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        "j.sh",
        ^^^^^^^
    ...<2 lines>...
        "jq -n --arg p '/x' 'def canonical_path: .; select((.url | canonical_path) == ($p | canonical_path))'\n",
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/tmp/claude-501/red-a6518485/tests/unit/test_lint_comparisons.py", line 200, in assert_refused_and_accepted
    self.assertEqual(1, result.returncode, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1 != 0 : 

======================================================================
FAIL: test_every_f_string_interpolation_in_a_regex_is_escaped (__main__.LintComparisonsTest.test_every_f_string_interpolation_in_a_regex_is_escaped)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tmp/claude-501/red-a6518485/tests/unit/test_lint_comparisons.py", line 229, in test_every_f_string_interpolation_in_a_regex_is_escaped
    self.assert_refused_and_accepted(
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        "r6.py",
        ^^^^^^^^
    ...<2 lines>...
        're.search(f"{re.escape(prefix)}{re.escape(name)}", text)\n',
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/tmp/claude-501/red-a6518485/tests/unit/test_lint_comparisons.py", line 200, in assert_refused_and_accepted
    self.assertEqual(1, result.returncode, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1 != 0 : 

======================================================================
FAIL: test_the_tracked_tree_is_clean_against_the_baseline (__main__.LintComparisonsTest.test_the_tracked_tree_is_clean_against_the_baseline)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tmp/claude-501/red-a6518485/tests/unit/test_lint_comparisons.py", line 238, in test_the_tracked_tree_is_clean_against_the_baseline
    self.assertEqual((0, "", ""), (result.returncode, result.stdout, result.stderr))
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: Tuples differ: (0, '', '') != (1, 'home/dot_claude/hooks/executable_proj[492 chars], '')

First differing element 0:
0
1

- (0, '', '')
+ (1,
+  'home/dot_claude/hooks/executable_project-map-reload.sh:40: R1 shell [[ ]] or '
+  '[ ] compares a path or URL operand by its string form\n'
+  'home/dot_claude/hooks/executable_project-map-reload.sh:48: R3 jq compares a '
+  'URL or path by its string form\n'
+  'home/dot_claude/hooks/executable_project-map-reload.sh:56: R1 shell [[ ]] or '
+  '[ ] compares a path or URL operand by its string form\n'
+  'stale baseline row home/dot_claude/hooks/executable_project-map-reload.sh '
+  'R1\n'
+  'stale baseline row home/dot_claude/hooks/executable_project-map-reload.sh '
+  'R3\n',
+  '')

----------------------------------------------------------------------
Ran 9 tests in 3.632s

FAILED (failures=4)
[exit 1]
```
## 3a. RED for 37bf6a51: its test file against the 979c0429 script, in a scratch worktree
```console
$ git -C "$V" log --oneline -1; git -C "$V" status --short; uv run --no-project python -I "$V/tests/unit/test_lint_comparisons.py" -v 2>&1 | grep -E "\.\.\. |^FAIL:|^Ran|^(OK|FAILED)"
979c0429 fix(lint): locate the jq program after its options, require a normaliser application per side, escape every interpolation (T129 followup a01)
 M tests/unit/test_lint_comparisons.py
test_a_baseline_row_is_consumed_once_so_a_duplicate_hit_fails (__main__.LintComparisonsTest.test_a_baseline_row_is_consumed_once_so_a_duplicate_hit_fails) ... ok
test_a_baseline_row_matching_no_hit_fails_as_stale (__main__.LintComparisonsTest.test_a_baseline_row_matching_no_hit_fails_as_stale) ... ok
test_a_jq_normaliser_name_inside_a_string_literal_is_no_application (__main__.LintComparisonsTest.test_a_jq_normaliser_name_inside_a_string_literal_is_no_application) ... ok
test_a_normaliser_is_matched_by_its_qualified_name_so_a_foreign_receiver_fails (__main__.LintComparisonsTest.test_a_normaliser_is_matched_by_its_qualified_name_so_a_foreign_receiver_fails) ... ok
test_a_single_quoted_jq_option_value_is_not_read_as_the_program (__main__.LintComparisonsTest.test_a_single_quoted_jq_option_value_is_not_read_as_the_program) ... 
  test_a_single_quoted_jq_option_value_is_not_read_as_the_program (__main__.LintComparisonsTest.test_a_single_quoted_jq_option_value_is_not_read_as_the_program) (call='"$jq"') ... FAIL
  test_a_single_quoted_jq_option_value_is_not_read_as_the_program (__main__.LintComparisonsTest.test_a_single_quoted_jq_option_value_is_not_read_as_the_program) (call='"${jq}"') ... FAIL
  test_a_single_quoted_jq_option_value_is_not_read_as_the_program (__main__.LintComparisonsTest.test_a_single_quoted_jq_option_value_is_not_read_as_the_program) (call='"$(command -v jq)"') ... FAIL
test_each_rule_refuses_its_fixture_and_each_normaliser_and_the_marker_are_accepted (__main__.LintComparisonsTest.test_each_rule_refuses_its_fixture_and_each_normaliser_and_the_marker_are_accepted) ... ok
test_every_f_string_interpolation_in_a_regex_is_escaped (__main__.LintComparisonsTest.test_every_f_string_interpolation_in_a_regex_is_escaped) ... ok
test_the_jq_normaliser_is_required_on_each_operand_side (__main__.LintComparisonsTest.test_the_jq_normaliser_is_required_on_each_operand_side) ... ok
test_the_tracked_tree_is_clean_against_the_baseline (__main__.LintComparisonsTest.test_the_tracked_tree_is_clean_against_the_baseline) ... FAIL
FAIL: test_a_single_quoted_jq_option_value_is_not_read_as_the_program (__main__.LintComparisonsTest.test_a_single_quoted_jq_option_value_is_not_read_as_the_program) (call='"$jq"')
FAIL: test_a_single_quoted_jq_option_value_is_not_read_as_the_program (__main__.LintComparisonsTest.test_a_single_quoted_jq_option_value_is_not_read_as_the_program) (call='"${jq}"')
FAIL: test_a_single_quoted_jq_option_value_is_not_read_as_the_program (__main__.LintComparisonsTest.test_a_single_quoted_jq_option_value_is_not_read_as_the_program) (call='"$(command -v jq)"')
FAIL: test_the_tracked_tree_is_clean_against_the_baseline (__main__.LintComparisonsTest.test_the_tracked_tree_is_clean_against_the_baseline)
Ran 9 tests in 3.642s
FAILED (failures=4)
[exit 0]
```
## 3b. RED for 1b56dc2b: the be2958cf test file against the 37bf6a51 script, in a scratch worktree
```console
$ git -C "$X" log --oneline -1; git -C "$X" status --short; uv run --no-project python -I "$X/tests/unit/test_lint_comparisons.py" -v 2>&1 | grep -E "\\.\\.\\. |^FAIL:|^Ran|^(OK|FAILED)"
37bf6a51 fix(lint): follow jq named through a variable or a substitution to its program (T129 followup a01)
 M tests/unit/test_lint_comparisons.py
test_a_baseline_row_is_consumed_once_so_a_duplicate_hit_fails (__main__.LintComparisonsTest.test_a_baseline_row_is_consumed_once_so_a_duplicate_hit_fails) ... ok
test_a_baseline_row_matching_no_hit_fails_as_stale (__main__.LintComparisonsTest.test_a_baseline_row_matching_no_hit_fails_as_stale) ... ok
test_a_jq_normaliser_name_inside_a_string_literal_is_no_application (__main__.LintComparisonsTest.test_a_jq_normaliser_name_inside_a_string_literal_is_no_application) ... FAIL
test_a_normaliser_is_matched_by_its_qualified_name_so_a_foreign_receiver_fails (__main__.LintComparisonsTest.test_a_normaliser_is_matched_by_its_qualified_name_so_a_foreign_receiver_fails) ... ok
test_a_single_quoted_jq_option_value_is_not_read_as_the_program (__main__.LintComparisonsTest.test_a_single_quoted_jq_option_value_is_not_read_as_the_program) ... 
  test_a_single_quoted_jq_option_value_is_not_read_as_the_program (__main__.LintComparisonsTest.test_a_single_quoted_jq_option_value_is_not_read_as_the_program) (form='jq -r "${opts[@]}" \'select(.url == $u)\' "$f"\n') ... FAIL
  test_a_single_quoted_jq_option_value_is_not_read_as_the_program (__main__.LintComparisonsTest.test_a_single_quoted_jq_option_value_is_not_read_as_the_program) (form="jq -er 2>/dev/null 'select(.path == $p)'\n") ... FAIL
  test_a_single_quoted_jq_option_value_is_not_read_as_the_program (__main__.LintComparisonsTest.test_a_single_quoted_jq_option_value_is_not_read_as_the_program) (form='jq -n --arg p "a\\"b" \'select(.url == $p)\'\n') ... FAIL
  test_a_single_quoted_jq_option_value_is_not_read_as_the_program (__main__.LintComparisonsTest.test_a_single_quoted_jq_option_value_is_not_read_as_the_program) (form='jq -n --arg root "$(cd "$(dirname "$0")/.." && pwd)" \'select(.path == $root)\'\n') ... FAIL
  test_a_single_quoted_jq_option_value_is_not_read_as_the_program (__main__.LintComparisonsTest.test_a_single_quoted_jq_option_value_is_not_read_as_the_program) (form="jq -r\\\n  'select(.url == $p)'\n") ... FAIL
test_each_rule_refuses_its_fixture_and_each_normaliser_and_the_marker_are_accepted (__main__.LintComparisonsTest.test_each_rule_refuses_its_fixture_and_each_normaliser_and_the_marker_are_accepted) ... ok
test_every_f_string_interpolation_in_a_regex_is_escaped (__main__.LintComparisonsTest.test_every_f_string_interpolation_in_a_regex_is_escaped) ... FAIL
test_the_jq_normaliser_is_required_on_each_operand_side (__main__.LintComparisonsTest.test_the_jq_normaliser_is_required_on_each_operand_side) ... ok
test_the_tracked_tree_is_clean_against_the_baseline (__main__.LintComparisonsTest.test_the_tracked_tree_is_clean_against_the_baseline) ... FAIL
FAIL: test_a_jq_normaliser_name_inside_a_string_literal_is_no_application (__main__.LintComparisonsTest.test_a_jq_normaliser_name_inside_a_string_literal_is_no_application)
FAIL: test_a_single_quoted_jq_option_value_is_not_read_as_the_program (__main__.LintComparisonsTest.test_a_single_quoted_jq_option_value_is_not_read_as_the_program) (form='jq -r "${opts[@]}" \'select(.url == $u)\' "$f"\n')
FAIL: test_a_single_quoted_jq_option_value_is_not_read_as_the_program (__main__.LintComparisonsTest.test_a_single_quoted_jq_option_value_is_not_read_as_the_program) (form="jq -er 2>/dev/null 'select(.path == $p)'\n")
FAIL: test_a_single_quoted_jq_option_value_is_not_read_as_the_program (__main__.LintComparisonsTest.test_a_single_quoted_jq_option_value_is_not_read_as_the_program) (form='jq -n --arg p "a\\"b" \'select(.url == $p)\'\n')
FAIL: test_a_single_quoted_jq_option_value_is_not_read_as_the_program (__main__.LintComparisonsTest.test_a_single_quoted_jq_option_value_is_not_read_as_the_program) (form='jq -n --arg root "$(cd "$(dirname "$0")/.." && pwd)" \'select(.path == $root)\'\n')
FAIL: test_a_single_quoted_jq_option_value_is_not_read_as_the_program (__main__.LintComparisonsTest.test_a_single_quoted_jq_option_value_is_not_read_as_the_program) (form="jq -r\\\n  'select(.url == $p)'\n")
FAIL: test_every_f_string_interpolation_in_a_regex_is_escaped (__main__.LintComparisonsTest.test_every_f_string_interpolation_in_a_regex_is_escaped)
FAIL: test_the_tracked_tree_is_clean_against_the_baseline (__main__.LintComparisonsTest.test_the_tracked_tree_is_clean_against_the_baseline)
Ran 9 tests in 4.006s
FAILED (failures=8)
[exit 0]
```
## 3c. RED for bb60ee84: the a0563644 test file against the 1b56dc2b script, in a scratch worktree
```console
$ git -C "$Y" log --oneline -1; git -C "$Y" status --short; uv run --no-project python -I "$Y/tests/unit/test_lint_comparisons.py" -v 2>&1 | grep -E "^FAIL:|^Ran|^(OK|FAILED)"
1b56dc2b fix(lint): the jq program is the base scan's first single-quoted string that is no option's argument (T129 followup a01 review)
 M tests/unit/test_lint_comparisons.py
FAIL: test_a_single_quoted_jq_option_value_is_not_read_as_the_program (__main__.LintComparisonsTest.test_a_single_quoted_jq_option_value_is_not_read_as_the_program) (form='"$(command -v jq 2>/dev/null)" -r \'select(.url == $p)\'\n')
FAIL: test_a_single_quoted_jq_option_value_is_not_read_as_the_program (__main__.LintComparisonsTest.test_a_single_quoted_jq_option_value_is_not_read_as_the_program) (form='"${tools[jq]}" -r \'select(.url == $p)\'\n')
FAIL: test_a_single_quoted_jq_option_value_is_not_read_as_the_program (__main__.LintComparisonsTest.test_a_single_quoted_jq_option_value_is_not_read_as_the_program) (form='"$bin/jq.exe" -r \'select(.url == $p)\'\n')
FAIL: test_the_tracked_tree_is_clean_against_the_baseline (__main__.LintComparisonsTest.test_the_tracked_tree_is_clean_against_the_baseline)
Ran 9 tests in 4.202s
FAILED (failures=4)
[exit 0]
```
## 4. GREEN: the Check's unit-test command on HEAD
```console
$ uv run python -m unittest tests/unit/test_lint_comparisons.py -v
test_a_baseline_row_is_consumed_once_so_a_duplicate_hit_fails (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_baseline_row_is_consumed_once_so_a_duplicate_hit_fails) ... ok
test_a_baseline_row_matching_no_hit_fails_as_stale (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_baseline_row_matching_no_hit_fails_as_stale) ... ok
test_a_jq_normaliser_name_inside_a_string_literal_is_no_application (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_jq_normaliser_name_inside_a_string_literal_is_no_application) ... ok
test_a_normaliser_is_matched_by_its_qualified_name_so_a_foreign_receiver_fails (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_normaliser_is_matched_by_its_qualified_name_so_a_foreign_receiver_fails) ... ok
test_a_single_quoted_jq_option_value_is_not_read_as_the_program (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_single_quoted_jq_option_value_is_not_read_as_the_program) ... ok
test_each_rule_refuses_its_fixture_and_each_normaliser_and_the_marker_are_accepted (tests.unit.test_lint_comparisons.LintComparisonsTest.test_each_rule_refuses_its_fixture_and_each_normaliser_and_the_marker_are_accepted) ... ok
test_every_f_string_interpolation_in_a_regex_is_escaped (tests.unit.test_lint_comparisons.LintComparisonsTest.test_every_f_string_interpolation_in_a_regex_is_escaped) ... ok
test_the_jq_normaliser_is_required_on_each_operand_side (tests.unit.test_lint_comparisons.LintComparisonsTest.test_the_jq_normaliser_is_required_on_each_operand_side) ... ok
test_the_tracked_tree_is_clean_against_the_baseline (tests.unit.test_lint_comparisons.LintComparisonsTest.test_the_tracked_tree_is_clean_against_the_baseline) ... FAIL

======================================================================
FAIL: test_the_tracked_tree_is_clean_against_the_baseline (tests.unit.test_lint_comparisons.LintComparisonsTest.test_the_tracked_tree_is_clean_against_the_baseline)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_lint_comparisons.py", line 267, in test_the_tracked_tree_is_clean_against_the_baseline
    self.assertEqual((0, "", ""), (result.returncode, result.stdout, result.stderr))
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: Tuples differ: (0, '', '') != (1, 'home/dot_claude/hooks/executable_proj[492 chars], '')

First differing element 0:
0
1

- (0, '', '')
+ (1,
+  'home/dot_claude/hooks/executable_project-map-reload.sh:40: R1 shell [[ ]] or '
+  '[ ] compares a path or URL operand by its string form\n'
+  'home/dot_claude/hooks/executable_project-map-reload.sh:48: R3 jq compares a '
+  'URL or path by its string form\n'
+  'home/dot_claude/hooks/executable_project-map-reload.sh:56: R1 shell [[ ]] or '
+  '[ ] compares a path or URL operand by its string form\n'
+  'stale baseline row home/dot_claude/hooks/executable_project-map-reload.sh '
+  'R1\n'
+  'stale baseline row home/dot_claude/hooks/executable_project-map-reload.sh '
+  'R3\n',
+  '')

----------------------------------------------------------------------
Ran 9 tests in 4.273s

FAILED (failures=1)
[exit 1]
```
## 5. The Check's lint command on HEAD
```console
$ uv run --no-project python -I scripts/lint-comparisons.py
home/dot_claude/hooks/executable_project-map-reload.sh:40: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form
home/dot_claude/hooks/executable_project-map-reload.sh:48: R3 jq compares a URL or path by its string form
home/dot_claude/hooks/executable_project-map-reload.sh:56: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form
stale baseline row home/dot_claude/hooks/executable_project-map-reload.sh R1
stale baseline row home/dot_claude/hooks/executable_project-map-reload.sh R3
[exit 1]
```
## 5a. The base script and base baseline (7c8e7484) over the same tree (a scratch worktree at HEAD with both files swapped back)
```console
$ git -C "$B" status --short; uv run --no-project python -I "$B/scripts/lint-comparisons.py"
 M scripts/lint-comparisons-baseline.tsv
 M scripts/lint-comparisons.py
home/dot_claude/hooks/executable_project-map-reload.sh:40: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form
home/dot_claude/hooks/executable_project-map-reload.sh:48: R3 jq compares a URL or path by its string form
home/dot_claude/hooks/executable_project-map-reload.sh:56: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form
stale baseline row home/dot_claude/hooks/executable_project-map-reload.sh R1
stale baseline row home/dot_claude/hooks/executable_project-map-reload.sh R3
[exit 1]
```
## 6. ruff check and ruff format
```console
$ ruff --version; ruff check scripts/lint-comparisons.py tests/unit/test_lint_comparisons.py; ruff format --config ruff.toml --check scripts/lint-comparisons.py tests/unit/test_lint_comparisons.py
ruff 0.17.0
All checks passed!
2 files already formatted
[exit 0]
```
## 7. Caps: the script alone; the numstat of this task's delta, and of origin/main...HEAD outside .orchestration (PR #387's diff is in it until the rebase)
```console
$ wc -l scripts/lint-comparisons.py; echo "--- 7c8e7484...HEAD"; git diff --numstat "$BASE"...HEAD; echo "--- origin/main...HEAD"; git diff --numstat origin/main...HEAD -- ":!.orchestration"
     200 scripts/lint-comparisons.py
--- 7c8e7484...HEAD
37	0	.orchestration/dotfiles-T129-normalised-comparison-lint-followup-a01/dotfiles-T129-normalised-comparison-lint-followup-a01-worker-crit.json
13	0	.orchestration/dotfiles-T129-normalised-comparison-lint-followup-a01/dotfiles-T129-normalised-comparison-lint-followup-a01-worker-review-receipt.md
9	0	.orchestration/dotfiles-T129-normalised-comparison-lint-followup-a01/learning.md
18	0	.orchestration/dotfiles-T129-normalised-comparison-lint-followup-a01/pr-body.md
87	0	.orchestration/dotfiles-T129-normalised-comparison-lint-followup-a01/report.md
25	0	.orchestration/dotfiles-T129-normalised-comparison-lint-followup-a01/sandbox.md
75	0	.orchestration/dotfiles-T129-normalised-comparison-lint-followup-a01/task.md
395	0	.orchestration/dotfiles-T129-normalised-comparison-lint-followup-a01/validation.md
1	0	scripts/lint-comparisons-baseline.tsv
13	12	scripts/lint-comparisons.py
67	0	tests/unit/test_lint_comparisons.py
--- origin/main...HEAD
86	0	scripts/lint-comparisons-baseline.tsv
200	0	scripts/lint-comparisons.py
271	0	tests/unit/test_lint_comparisons.py
[exit 0]
```
## 8. --list-rules is unchanged
```console
$ uv run --no-project python -I "$B/scripts/lint-comparisons.py" --list-rules > "$TMPDIR/lr-base.txt"; uv run --no-project python -I scripts/lint-comparisons.py --list-rules > "$TMPDIR/lr-head.txt"; cmp "$TMPDIR/lr-base.txt" "$TMPDIR/lr-head.txt" && echo "--list-rules byte-identical"
--list-rules byte-identical
[exit 0]
```
## 9. Every tree hit without a baseline, base script vs HEAD script (the baseline follows with one row)
```console
$ uv run --no-project python -I "$B/scripts/lint-comparisons.py" --baseline /nonexistent > "$TMPDIR/hits-base.txt"; uv run --no-project python -I scripts/lint-comparisons.py --baseline /nonexistent > "$TMPDIR/hits-head.txt"; wc -l < "$TMPDIR/hits-base.txt"; wc -l < "$TMPDIR/hits-head.txt"; diff "$TMPDIR/hits-base.txt" "$TMPDIR/hits-head.txt"; echo "--- baseline diff 7c8e7484..HEAD"; git diff "$BASE"..HEAD -- scripts/lint-comparisons-baseline.tsv | tail -n +5; echo "--- the hit line"; sed -n 66p scripts/orchestrator/task-consistency-check.py
      86
      87
62a63
> scripts/orchestrator/task-consistency-check.py:66: R6 an identifier is interpolated into a regex (grep -E on $name; re.* on an f-string)
--- baseline diff 7c8e7484..HEAD
@@ -60,6 +60,7 @@ scripts/orchestrator/pr-cost.sh	R6	f1ff986bb9600a19078ac1ead58405f0908540af85884
 scripts/orchestrator/resolve-threads.sh	R3	d642969f29e3eddf1a5b5a1227cf5d5a0797410646fcfeb3656ce9262a7a45b9
 scripts/orchestrator/task-consistency-check.py	R4	8be62cdea849cb4c813fdbab94a73396f1bcc65bd5ca86fdd8abea76aba3e602
 scripts/orchestrator/task-consistency-check.py	R4	9d437d518a52fdbd818f2ee7552e84fce6d174f54676f68dd725a0dbfcb8419f
+scripts/orchestrator/task-consistency-check.py	R6	b2513e6e90aae823c2625b0a34e8f1348f674dc60237ed42bc4d99427c3dc90b
 scripts/require-crit-review.py	R4	3bc8870a6a87dbfb811754138a767d02c5b010f4d25bd8ca0c244171b7d2435f
 scripts/require-crit-review.py	R4	4485ef36304b22adf0a481d0ab45031f304d197c997ad667a6f1661b9149d740
 scripts/require-crit-review.py	R4	5fe2a097290c874909ecd58a2bad704aa11e36fca5510619096f26e067042299
--- the hit line
        if not re.search(rf"(?:{re.escape(rid)}|-{rid.rsplit('-', 1)[-1]})/task\.md", rowtext):
[exit 0]
```
## 10. Every jq program located, base programs() vs HEAD programs(), over every tracked shell file
```console
$ cat "$TMPDIR/cmp_programs.py"; echo "--- run"; uv run --no-project python -I "$TMPDIR/cmp_programs.py" "$B/scripts/lint-comparisons.py" scripts/lint-comparisons.py
import importlib.util, sys, subprocess
from pathlib import Path
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
old, new = load(sys.argv[1], "old"), load(sys.argv[2], "new")
lost = gained = same = 0
for rel, target in new.default_files():
    text = target.read_text(errors="replace")
    lines = text.split("\n")
    if rel.removesuffix(".tmpl").endswith(".py") or lines[0].startswith("#!") and "python" in lines[0]:
        continue
    code = "\n".join("" if l.lstrip().startswith("#") else l for l in lines)
    a, b = set(old.programs(code)), set(new.programs(code))
    same += len(a & b)
    for s, p in sorted(a - b): lost += 1; print("LOST ", rel, code.count("\n", 0, s) + 1, p[:90].replace("\n", " "))
    for s, p in sorted(b - a): gained += 1; print("GAINED", rel, code.count("\n", 0, s) + 1, p[:90].replace("\n", " "))
print(f"same={same} lost={lost} gained={gained}")
--- run
LOST  home/dot_local/bin/common/executable_herdr-agents 1195 '\t'
GAINED home/dot_local/bin/common/executable_herdr-agents 1195 '.[]? | select(.member == $member) | .pane // empty'
same=86 lost=1 gained=1
[exit 0]
```
## 10a. Edge shapes (one jq call per line; the continuation form spans lines 11 to 13): the lines each script reports, base, 37bf6a51, HEAD
```console
$ cat -n "$TMPDIR/shapes/s.sh"; git show 37bf6a51:scripts/lint-comparisons.py > "$TMPDIR/lint-37bf.py"; for s in "$B/scripts/lint-comparisons.py" "$TMPDIR/lint-37bf.py" scripts/lint-comparisons.py; do printf "%s: " "$s"; uv run --no-project python -I "$s" --baseline "$TMPDIR/shapes/none.tsv" "$TMPDIR/shapes/s.sh" | cut -d: -f2 | tr "\\n" " "; echo; done
     1	jq -n "$@" 'select(.url == $u)'
     2	jq -n $flags 'select(.url == $u)'
     3	jq -n <<<"$x" 'select(.url == $u)'
     4	jq -n --arg p $(git rev-parse --show-toplevel) 'select(.path == $p)'
     5	jq -n --arg p a\ b 'select(.url == $p)'
     6	jq -n --arg p "${x//\"/}" 'select(.url == $p)'
     7	jq -n --argjson j '{"a":1}' --arg p '/x' 'select(.url == $p)'
     8	jq -n --arg 'p' '/x' 'select(.url == $p)'
     9	jq -n --indent '2' 'select(.url == $p)'
    10	jq -n --arg msg "it's" 'select(.url == $p)'
    11	jq -n --arg p \
    12	  '/x' \
    13	  'select(.url == $p)'
    14	jq -n --arg x a-L 'select(.url == $p)'
/tmp/claude-501/base-script-at-head/scripts/lint-comparisons.py: 1 2 3 4 5 6 14 
/tmp/claude-501/lint-37bf.py: 7 8 9 10 13 14 
scripts/lint-comparisons.py: 1 2 3 4 5 6 7 8 9 10 13 14 
[exit 0]
```
## 11. The rebase preview: this branch's three files on origin/main (a scratch worktree), HEAD script and base script
```console
$ git -C "$S" log --oneline -1; git -C "$S" status --short; echo "--- HEAD script"; uv run --no-project python -I "$S/scripts/lint-comparisons.py"; echo "[lint exit $?]"; echo "--- base script, same tree and baseline"; uv run --no-project python -I "$S/scripts/.lint-base-sim.py" --baseline "$S/scripts/lint-comparisons-baseline.tsv"; echo "[lint exit $?]"; echo "--- the new line"; sed -n 960p "$S/scripts/update-agent-assets.sh"; git -C "$S" log --oneline -1 -- scripts/update-agent-assets.sh
a8a747af fix(claude): render scoped sandbox access per platform (#392)
?? scripts/.lint-base-sim.py
?? scripts/lint-comparisons-baseline.tsv
?? scripts/lint-comparisons.py
?? tests/unit/test_lint_comparisons.py
--- HEAD script
home/dot_claude/hooks/executable_project-map-reload.sh:40: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form
home/dot_claude/hooks/executable_project-map-reload.sh:48: R3 jq compares a URL or path by its string form
home/dot_claude/hooks/executable_project-map-reload.sh:56: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form
scripts/update-agent-assets.sh:960: R2 shell case matches a path or URL operand by its string form
stale baseline row home/dot_claude/hooks/executable_project-map-reload.sh R1
stale baseline row home/dot_claude/hooks/executable_project-map-reload.sh R3
[lint exit 1]
--- base script, same tree and baseline
home/dot_claude/hooks/executable_project-map-reload.sh:40: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form
home/dot_claude/hooks/executable_project-map-reload.sh:48: R3 jq compares a URL or path by its string form
home/dot_claude/hooks/executable_project-map-reload.sh:56: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form
scripts/update-agent-assets.sh:960: R2 shell case matches a path or URL operand by its string form
stale baseline row home/dot_claude/hooks/executable_project-map-reload.sh R1
stale baseline row home/dot_claude/hooks/executable_project-map-reload.sh R3
stale baseline row scripts/orchestrator/task-consistency-check.py R6
[lint exit 1]
--- the new line
    case "$(uname -s)/$(uname -m)" in
f32c02b8 feat(agents): pin verified omp and hcom assets (#388)
[exit 0]
```
## 12. Amendment 1: the task file (sha256 78d582c8…) and the task copy
```console
$ shasum -a 256 "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md"; cmp "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md" && echo byte-identical; uv run --offline --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root "$PWD" "$MAIN/.orchestration/tasks/$T.md"
78d582c861315b07f98dc173db1803a20f47e708409cfa4a0f922f82742a7334  ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-followup-a01.md
78d582c861315b07f98dc173db1803a20f47e708409cfa4a0f922f82742a7334  .orchestration/dotfiles-T129-normalised-comparison-lint-followup-a01/task.md
byte-identical
dotfiles-T129-normalised-comparison-lint-followup-a01.md: OK
[exit 0]
```
## 12a. The rebase (item 1): origin/main, the branch, and each rebased commit beside the pre-rebase commit of the same subject (the merges 35eff561 and 7c8e7484 drop out)
```console
$ git log --oneline -1 origin/main; git branch --show-current; git rev-parse HEAD; git log --reverse --format="%h %s" origin/main..HEAD | while read -r new subject; do old=$(git log --no-merges --format="%h %s" origin/main.."$OLD" | awk -v s="$subject" "substr(\$0, index(\$0, \" \") + 1) == s {print \$1}"); echo "$new <- ${old:-none}  ${subject:0:90}"; done
68f8a70a fix(update): remove a dangling omp link before npm installs and skip wheel-pinned uv tools (T132 make-update-followups a01) (#405)
lint/normalised-comparisons-followup-a01
7fa5d11279916f5f7d715f8713e432fc3c85217b
aac533da <- 4663dc4d  feat(lint): refuse string-form comparisons of paths, URLs and processes (T129 normalised-c
9d1a7d14 <- 9fbd0de0  refactor(lint): bring lint-comparisons.py under the 200-line cap (T129 Amendment 2, D-cap-
f5508f92 <- 26ed34bb  fix(lint): find the test word anywhere on the line and anchor jq programs at the jq word (
bcf610b8 <- e88f8f05  fix(lint): the R2 accepted forms keep a literal tail, Python R6 needs re as the receiver, 
6cd50943 <- 4b843ce9  docs(orchestration): T129 normalised-comparison lint a01 task copy and evidence (4663dc4d,
480f48c4 <- 8d7b9831  test(lint): the three structural checks of the revise round, red on 4b843ce9 (T129 round 2
192c88d2 <- df8055ce  fix(lint): structural checks for the baseline, the Python normalisers and the jq normalise
044e5751 <- 12d5d771  fix(lint): accept the qualified pathlib.Path(...).resolve as the table's Path(...).resolve
b0baf0e2 <- d215e062  docs(orchestration): T129 lint a01 round-2 evidence (revise.yaml, the structural checks, t
9376d658 <- e8a41419  chore(lint): drop the baseline row of local-advisory.sh R6, whose hit PR #386 removed (T12
8950625c <- a08daa21  docs(orchestration): T129 lint a01 round-3 evidence (the stale row of local-advisory.sh dr
c5082855 <- a6518485  test(lint): one refusal fixture per owned row of the lint lineage's follow-up (T129 follow
c33c351f <- 979c0429  fix(lint): locate the jq program after its options, require a normaliser application per s
85100657 <- 37bf6a51  fix(lint): follow jq named through a variable or a substitution to its program (T129 follo
18536b1a <- be2958cf  test(lint): the forms the base jq scan read stay read; map(re.escape) and a jq comment (T1
514969d1 <- 1b56dc2b  fix(lint): the jq program is the base scan's first single-quoted string that is no option'
fcf9d94d <- b6c47653  docs(orchestration): T129 normalised-comparison lint followup a01: the task copy and the w
10ea506c <- a0563644  test(lint): jq named inside a double-quoted expansion with more text before its closing qu
f78e5dbf <- bb60ee84  fix(lint): an unbalanced double quote before the jq program is read as text, as the base r
b87421d2 <- 445c32dd  docs(orchestration): T129 normalised-comparison lint followup a01: the re-review round (Ve
7fa5d112 <- none  chore(lint): rehash the baseline rows of project-map-reload.sh and add the hit main gained
[exit 0]
```
## 12b. The baseline (item 2): the lint on the rebased tree with the pre-commit baseline, then the rows the baseline commit changed
```console
$ git show 7fa5d112~1:scripts/lint-comparisons-baseline.tsv > "$TMPDIR/base-pre.tsv"; uv run --no-project python -I scripts/lint-comparisons.py --baseline "$TMPDIR/base-pre.tsv"; echo "lint exit $?"; git show --format= 7fa5d112 -- scripts/lint-comparisons-baseline.tsv | /usr/bin/grep "^[-+][^-+]"; for spec in home/dot_claude/hooks/executable_project-map-reload.sh:40 home/dot_claude/hooks/executable_project-map-reload.sh:48 home/dot_claude/hooks/executable_project-map-reload.sh:56 scripts/update-agent-assets.sh:966 scripts/update-agent-assets.sh:274; do echo "$spec: $(sed -n "${spec##*:}p" "${spec%:*}" | sed "s/^ *//")"; done
home/dot_claude/hooks/executable_project-map-reload.sh:40: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form
home/dot_claude/hooks/executable_project-map-reload.sh:48: R3 jq compares a URL or path by its string form
home/dot_claude/hooks/executable_project-map-reload.sh:56: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form
scripts/update-agent-assets.sh:966: R2 shell case matches a path or URL operand by its string form
stale baseline row home/dot_claude/hooks/executable_project-map-reload.sh R1
stale baseline row home/dot_claude/hooks/executable_project-map-reload.sh R3
lint exit 1
-home/dot_claude/hooks/executable_project-map-reload.sh	R1	a45857c4797c369400f4f84156a3a92934ca4fe7f9392857147f66f9a1ad4e97
-home/dot_claude/hooks/executable_project-map-reload.sh	R3	f199a15a9fa07adaaa6e9169f70b3caec7dbabb8e214422ad1dc831913d83563
+home/dot_claude/hooks/executable_project-map-reload.sh	R1	ab243de925307b58c884435028ebbf30cfd2d4d3c7769b9ec1c277cd1607b499
+home/dot_claude/hooks/executable_project-map-reload.sh	R1	cb215215ea63c06896e19539673c3a32bc2ac653badcf41805fb5693e83cf1ab
+home/dot_claude/hooks/executable_project-map-reload.sh	R3	bf627d2c8fec1eea6f00a780e11c61f5759598466ec4324f8b5685fda986e954
+scripts/update-agent-assets.sh	R2	851db696b62d42ddfefa5fbc21df66a2bf37a6906e735a2a802cf1b1b54e878a
home/dot_claude/hooks/executable_project-map-reload.sh:40: [[ "$event_path" == */.project-map/index.html ]] || exit 0
home/dot_claude/hooks/executable_project-map-reload.sh:48: | select(.url | strings | startswith("file://"))
home/dot_claude/hooks/executable_project-map-reload.sh:56: [[ "$tab_path" == "$event_path" ]] || continue
scripts/update-agent-assets.sh:966: case "$(uname -s)/$(uname -m)" in
scripts/update-agent-assets.sh:274: case "$(uname -s)/$(uname -m)" in
[exit 0]
```
## 12c. The six Bot threads of #387 (item 3): each fixture against the lint script of its fix commit's parent and of the fix commit (the helper, then its run)
```console
$ cat "$TMPDIR/t129-threads.sh"; echo "--- run"; bash "$TMPDIR/t129-threads.sh"
#!/bin/bash
# For each #387 Bot thread: its fixture red with the lint script of the fix commit's parent, green with the fix commit's, in a scratch worktree at HEAD; then the thread's own reproducer through the lint at HEAD.
W="$TMPDIR/t129-threads-wt"
git worktree add -q --detach "$W" HEAD
while read -r thread test fix; do
    for rev in "${fix}^" "${fix}"; do
        git show "${rev}:scripts/lint-comparisons.py" > "$W/scripts/lint-comparisons.py"
        r=$(cd "$W" && uv run python -m unittest "tests.unit.test_lint_comparisons.LintComparisonsTest.${test}" 2>&1 | tail -n 1)
        echo "${thread} ${test} script@$(git rev-parse --short=8 "${rev}") -> ${r}"
    done
done << 'ROWS'
4302545078 test_a_baseline_row_is_consumed_once_so_a_duplicate_hit_fails 192c88d2
4302545082 test_a_normaliser_is_matched_by_its_qualified_name_so_a_foreign_receiver_fails 192c88d2
4302545085 test_the_jq_normaliser_is_required_on_each_operand_side 192c88d2
4302629300 test_a_single_quoted_jq_option_value_is_not_read_as_the_program c33c351f
4302629305 test_a_jq_normaliser_name_inside_a_string_literal_is_no_application c33c351f
4302629307 test_every_f_string_interpolation_in_a_regex_is_escaped c33c351f
ROWS
git worktree remove --force "$W"
echo "--- each thread's reproducer through the lint at HEAD ($(git rev-parse --short=8 HEAD)):"
R="$TMPDIR/t129-repro"; mkdir -p "$R"
printf '%s\n' 'jq -r '"'"'def canonical_path: .; select((.url | canonical_path | canonical_path) == $path)'"'" > "$R/4302545085.sh"
printf '%s\n' 'jq --arg p '"'"'/x'"'"' '"'"'select(.url == $p)'"'" > "$R/4302629300.sh"
printf '%s\n' 'jq -r '"'"'def canonical_path: .; select((.url + "canonical_path") == ($path | canonical_path))'"'" > "$R/4302629305.sh"
printf '%s\n' 'if fake.realpath(path) == "/x":' '    pass' 're.search(f"{fake.escape(name)}", text)' > "$R/4302545082.py"
printf '%s\n' 're.search(f"{re.escape(prefix)}{name}", text)' > "$R/4302629307.py"
for f in "$R"/*; do uv run --no-project python -I scripts/lint-comparisons.py --baseline /dev/null "$f" > "$R/out.txt"; rc=$?; sed "s|$R/||" "$R/out.txt"; echo "  lint exit $rc (${f##*/})"; rm -f "$R/out.txt"; done
--- run
4302545078 test_a_baseline_row_is_consumed_once_so_a_duplicate_hit_fails script@480f48c4 -> FAILED (failures=1)
4302545078 test_a_baseline_row_is_consumed_once_so_a_duplicate_hit_fails script@192c88d2 -> OK
4302545082 test_a_normaliser_is_matched_by_its_qualified_name_so_a_foreign_receiver_fails script@480f48c4 -> FAILED (failures=3)
4302545082 test_a_normaliser_is_matched_by_its_qualified_name_so_a_foreign_receiver_fails script@192c88d2 -> OK
4302545085 test_the_jq_normaliser_is_required_on_each_operand_side script@480f48c4 -> FAILED (failures=2)
4302545085 test_the_jq_normaliser_is_required_on_each_operand_side script@192c88d2 -> OK
4302629300 test_a_single_quoted_jq_option_value_is_not_read_as_the_program script@c5082855 -> FAILED (failures=1)
4302629300 test_a_single_quoted_jq_option_value_is_not_read_as_the_program script@c33c351f -> FAILED (failures=11)
4302629305 test_a_jq_normaliser_name_inside_a_string_literal_is_no_application script@c5082855 -> FAILED (failures=1)
4302629305 test_a_jq_normaliser_name_inside_a_string_literal_is_no_application script@c33c351f -> FAILED (failures=1)
4302629307 test_every_f_string_interpolation_in_a_regex_is_escaped script@c5082855 -> FAILED (failures=1)
4302629307 test_every_f_string_interpolation_in_a_regex_is_escaped script@c33c351f -> FAILED (failures=1)
--- each thread's reproducer through the lint at HEAD (7fa5d112):
4302545082.py:1: R4 Python compares a path or URL by its string form
4302545082.py:3: R6 an identifier is interpolated into a regex (grep -E on $name; re.* on an f-string)
  lint exit 1 (4302545082.py)
4302545085.sh:1: R3 jq compares a URL or path by its string form
  lint exit 1 (4302545085.sh)
4302629300.sh:1: R3 jq compares a URL or path by its string form
  lint exit 1 (4302629300.sh)
4302629305.sh:1: R3 jq compares a URL or path by its string form
  lint exit 1 (4302629305.sh)
4302629307.py:1: R6 an identifier is interpolated into a regex (grep -E on $name; re.* on an f-string)
  lint exit 1 (4302629307.py)
[exit 0]
```
## 12d. The three d215e062 threads: HEAD's fixture against each follow-up fix commit's script, and the fixture as it stood at c33c351f (the helper, then its run)
```console
$ cat "$TMPDIR/t129-threads2.sh"; echo "--- run"; bash "$TMPDIR/t129-threads2.sh"
#!/bin/bash
# The three d215e062 threads: HEAD's fixture against the lint script of each follow-up fix commit, and each fixture as it stood at c33c351f against c5082855's and c33c351f's scripts.
W="$TMPDIR/t129-threads-wt2"
git worktree add -q --detach "$W" HEAD
for test in test_a_single_quoted_jq_option_value_is_not_read_as_the_program test_a_jq_normaliser_name_inside_a_string_literal_is_no_application test_every_f_string_interpolation_in_a_regex_is_escaped; do
    for rev in c33c351f 85100657 514969d1 f78e5dbf; do
        git show "${rev}:scripts/lint-comparisons.py" > "$W/scripts/lint-comparisons.py"
        echo "HEAD fixture ${test} script@${rev} -> $(cd "$W" && uv run python -m unittest "tests.unit.test_lint_comparisons.LintComparisonsTest.${test}" 2>&1 | tail -n 1)"
    done
done
git show c33c351f:tests/unit/test_lint_comparisons.py > "$W/tests/unit/test_lint_comparisons.py"
for test in test_a_single_quoted_jq_option_value_is_not_read_as_the_program test_a_jq_normaliser_name_inside_a_string_literal_is_no_application test_every_f_string_interpolation_in_a_regex_is_escaped; do
    for rev in c5082855 c33c351f; do
        git show "${rev}:scripts/lint-comparisons.py" > "$W/scripts/lint-comparisons.py"
        echo "c33c351f fixture ${test} script@${rev} -> $(cd "$W" && uv run python -m unittest "tests.unit.test_lint_comparisons.LintComparisonsTest.${test}" 2>&1 | tail -n 1)"
    done
done
git worktree remove --force "$W"
--- run
HEAD fixture test_a_single_quoted_jq_option_value_is_not_read_as_the_program script@c33c351f -> FAILED (failures=11)
HEAD fixture test_a_single_quoted_jq_option_value_is_not_read_as_the_program script@85100657 -> FAILED (failures=8)
HEAD fixture test_a_single_quoted_jq_option_value_is_not_read_as_the_program script@514969d1 -> FAILED (failures=3)
HEAD fixture test_a_single_quoted_jq_option_value_is_not_read_as_the_program script@f78e5dbf -> OK
HEAD fixture test_a_jq_normaliser_name_inside_a_string_literal_is_no_application script@c33c351f -> FAILED (failures=1)
HEAD fixture test_a_jq_normaliser_name_inside_a_string_literal_is_no_application script@85100657 -> FAILED (failures=1)
HEAD fixture test_a_jq_normaliser_name_inside_a_string_literal_is_no_application script@514969d1 -> OK
HEAD fixture test_a_jq_normaliser_name_inside_a_string_literal_is_no_application script@f78e5dbf -> OK
HEAD fixture test_every_f_string_interpolation_in_a_regex_is_escaped script@c33c351f -> FAILED (failures=1)
HEAD fixture test_every_f_string_interpolation_in_a_regex_is_escaped script@85100657 -> FAILED (failures=1)
HEAD fixture test_every_f_string_interpolation_in_a_regex_is_escaped script@514969d1 -> OK
HEAD fixture test_every_f_string_interpolation_in_a_regex_is_escaped script@f78e5dbf -> OK
c33c351f fixture test_a_single_quoted_jq_option_value_is_not_read_as_the_program script@c5082855 -> FAILED (failures=1)
c33c351f fixture test_a_single_quoted_jq_option_value_is_not_read_as_the_program script@c33c351f -> OK
c33c351f fixture test_a_jq_normaliser_name_inside_a_string_literal_is_no_application script@c5082855 -> FAILED (failures=1)
c33c351f fixture test_a_jq_normaliser_name_inside_a_string_literal_is_no_application script@c33c351f -> OK
c33c351f fixture test_every_f_string_interpolation_in_a_regex_is_escaped script@c5082855 -> FAILED (failures=1)
c33c351f fixture test_every_f_string_interpolation_in_a_regex_is_escaped script@c33c351f -> OK
[exit 0]
```
## 13. GREEN: the Check's unit-test command on HEAD
```console
$ uv run python -m unittest tests/unit/test_lint_comparisons.py -v 2>&1 | /usr/bin/grep -E "\.\.\. |^Ran|^(OK|FAILED)"
test_a_baseline_row_is_consumed_once_so_a_duplicate_hit_fails (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_baseline_row_is_consumed_once_so_a_duplicate_hit_fails) ... ok
test_a_baseline_row_matching_no_hit_fails_as_stale (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_baseline_row_matching_no_hit_fails_as_stale) ... ok
test_a_jq_normaliser_name_inside_a_string_literal_is_no_application (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_jq_normaliser_name_inside_a_string_literal_is_no_application) ... ok
test_a_normaliser_is_matched_by_its_qualified_name_so_a_foreign_receiver_fails (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_normaliser_is_matched_by_its_qualified_name_so_a_foreign_receiver_fails) ... ok
test_a_single_quoted_jq_option_value_is_not_read_as_the_program (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_single_quoted_jq_option_value_is_not_read_as_the_program) ... ok
test_each_rule_refuses_its_fixture_and_each_normaliser_and_the_marker_are_accepted (tests.unit.test_lint_comparisons.LintComparisonsTest.test_each_rule_refuses_its_fixture_and_each_normaliser_and_the_marker_are_accepted) ... ok
test_every_f_string_interpolation_in_a_regex_is_escaped (tests.unit.test_lint_comparisons.LintComparisonsTest.test_every_f_string_interpolation_in_a_regex_is_escaped) ... ok
test_the_jq_normaliser_is_required_on_each_operand_side (tests.unit.test_lint_comparisons.LintComparisonsTest.test_the_jq_normaliser_is_required_on_each_operand_side) ... ok
test_the_tracked_tree_is_clean_against_the_baseline (tests.unit.test_lint_comparisons.LintComparisonsTest.test_the_tracked_tree_is_clean_against_the_baseline) ... ok
Ran 9 tests in 4.533s
OK
[exit 0]
```
## 14. The Check's lint command on HEAD (exit 0, no output)
```console
$ uv run --no-project python -I scripts/lint-comparisons.py
[exit 0]
```
## 15. ruff check and ruff format --check
```console
$ ruff check scripts/lint-comparisons.py tests/unit/test_lint_comparisons.py && ruff format --config ruff.toml --check scripts/lint-comparisons.py tests/unit/test_lint_comparisons.py
All checks passed!
2 files already formatted
[exit 0]
```
## 16. Caps against origin/main: the script alone, and the numstat summed as the Check reads it
```console
$ wc -l scripts/lint-comparisons.py; git diff --numstat origin/main...HEAD; git diff --numstat origin/main...HEAD | awk -F "\t" "\$3 ~ /^\\.orchestration\\// {next} \$3 ~ /^tests\\// {t += \$1; next} \$3 == \"scripts/lint-comparisons-baseline.tsv\" {b += \$1 + \$2; next} {o += \$1 + \$2} END {printf \"outside tests/ and .orchestration/, without the baseline: %d of 200\nadded under tests/: %d of 1000\nthe baseline (outside the count): %d\n\", o, t, b}"
     200 scripts/lint-comparisons.py
3	0	.orchestration/dotfiles-T129-normalised-comparison-lint-a01/autoskill.md
136	0	.orchestration/dotfiles-T129-normalised-comparison-lint-a01/baseline-rows.md
88	0	.orchestration/dotfiles-T129-normalised-comparison-lint-a01/dotfiles-T129-normalised-comparison-lint-a01-worker-crit.json
10	0	.orchestration/dotfiles-T129-normalised-comparison-lint-a01/dotfiles-T129-normalised-comparison-lint-a01-worker-review-receipt.md
11	0	.orchestration/dotfiles-T129-normalised-comparison-lint-a01/learning.md
123	0	.orchestration/dotfiles-T129-normalised-comparison-lint-a01/question-1.md
122	0	.orchestration/dotfiles-T129-normalised-comparison-lint-a01/report.md
21	0	.orchestration/dotfiles-T129-normalised-comparison-lint-a01/revise.yaml
27	0	.orchestration/dotfiles-T129-normalised-comparison-lint-a01/sandbox.md
120	0	.orchestration/dotfiles-T129-normalised-comparison-lint-a01/task.md
388	0	.orchestration/dotfiles-T129-normalised-comparison-lint-a01/validation.md
65	0	.orchestration/dotfiles-T129-normalised-comparison-lint-followup-a01/dotfiles-T129-normalised-comparison-lint-followup-a01-worker-crit.json
13	0	.orchestration/dotfiles-T129-normalised-comparison-lint-followup-a01/dotfiles-T129-normalised-comparison-lint-followup-a01-worker-review-receipt.md
9	0	.orchestration/dotfiles-T129-normalised-comparison-lint-followup-a01/learning.md
18	0	.orchestration/dotfiles-T129-normalised-comparison-lint-followup-a01/pr-body.md
91	0	.orchestration/dotfiles-T129-normalised-comparison-lint-followup-a01/report.md
25	0	.orchestration/dotfiles-T129-normalised-comparison-lint-followup-a01/sandbox.md
75	0	.orchestration/dotfiles-T129-normalised-comparison-lint-followup-a01/task.md
419	0	.orchestration/dotfiles-T129-normalised-comparison-lint-followup-a01/validation.md
88	0	scripts/lint-comparisons-baseline.tsv
200	0	scripts/lint-comparisons.py
271	0	tests/unit/test_lint_comparisons.py
outside tests/ and .orchestration/, without the baseline: 200 of 200
added under tests/: 271 of 1000
the baseline (outside the count): 88
[exit 0]
```
## 17. The rebase carried the three files unchanged, and --list-rules with them
```console
$ git diff --stat "$OLD" HEAD -- scripts/lint-comparisons.py tests/unit/test_lint_comparisons.py && echo "script and tests identical to $OLD"; uv run --no-project python -I scripts/lint-comparisons.py --list-rules
script and tests identical to 445c32dd
R0 the allow marker carries no reason
R1 shell [[ ]] or [ ] compares a path or URL operand by its string form
R2 shell case matches a path or URL operand by its string form
R3 jq compares a URL or path by its string form
R4 Python compares a path or URL by its string form
R5 a process is read as text (ps piped to grep, awk, cut or sed; pgrep -f on a variable)
R6 an identifier is interpolated into a regex (grep -E on $name; re.* on an f-string)
shortcut: the lint is statement-local, so a variable normalised on an earlier line and compared later is a hit (mark it with the marker and its reason); upgrade to a cross-line data-flow when a second such marker is needed
[exit 0]
```
## 18. main moved to 61231cd9 after the rebase (#408): PR 415's CI failed the tracked-tree test on the merge; the branch takes main by a merge, so the commits the dispositions name stay
```console
$ git log --oneline -1 origin/main; git log --format="%h parents=%p %s" -1 5c2ef021; git show 5c2ef021~1:scripts/lint-comparisons-baseline.tsv > "$TMPDIR/base-merge.tsv"; git show 5c2ef021:scripts/lint-comparisons-baseline.tsv | cmp -s - "$TMPDIR/base-merge.tsv" && echo "the merge left the baseline unchanged"; uv run --no-project python -I scripts/lint-comparisons.py --baseline "$TMPDIR/base-merge.tsv"; echo "lint exit $?"; git show --format= 1219ab10 -- scripts/lint-comparisons-baseline.tsv | /usr/bin/grep "^[-+][^-+]"; for n in 1843 1846; do echo "executable_herdr-agents:$n: $(sed -n "${n}p" home/dot_local/bin/common/executable_herdr-agents | sed "s/^ *//")"; done
61231cd9 fix(agents): enforce worker cap and worktree hooks path (#408)
5c2ef021 parents=3f58dfc5 61231cd9 Merge remote-tracking branch 'origin/main' into lint/normalised-comparisons-followup-a01
the merge left the baseline unchanged
home/dot_local/bin/common/executable_herdr-agents:1843: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form
home/dot_local/bin/common/executable_herdr-agents:1846: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form
lint exit 1
+home/dot_local/bin/common/executable_herdr-agents	R1	3a6dd8d64e8edad0d422df00c90a9ed20ea7cf7d7ed50db196d8f0cc28929b20
+home/dot_local/bin/common/executable_herdr-agents	R1	5310bef745aaa4a3a1a2ddc2790f8fb98d90f4a4db51958541a25a4e88e15c8a
executable_herdr-agents:1843: [[ ${seat_path} == "${workdir}/.claude/worktrees/"* ]] || continue
executable_herdr-agents:1846: [[ ${seat_path} != "${workdir}/${seat_worktree}" ]] || seat_seated=true
[exit 0]
```
## 19. GREEN at the head: the Check's tests, the lint (exit 0, no output), ruff
```console
$ git rev-parse HEAD; uv run python -m unittest tests/unit/test_lint_comparisons.py 2>&1 | tail -n 1; uv run --no-project python -I scripts/lint-comparisons.py; echo "lint exit $?"; ruff check scripts/lint-comparisons.py tests/unit/test_lint_comparisons.py
1219ab1087ffd310167d9676ed16eb6de84f5f4d
OK
lint exit 0
All checks passed!
[exit 0]
```
## 20. Caps against origin/main 61231cd9
```console
$ wc -l scripts/lint-comparisons.py; git diff --numstat origin/main...HEAD -- ":!.orchestration"; git diff --numstat origin/main...HEAD | awk -F "\t" "\$3 ~ /^\\.orchestration\\// {next} \$3 ~ /^tests\\// {t += \$1; next} \$3 == \"scripts/lint-comparisons-baseline.tsv\" {b += \$1 + \$2; next} {o += \$1 + \$2} END {printf \"outside tests/ and .orchestration/, without the baseline: %d of 200\nadded under tests/: %d of 1000\nthe baseline (outside the count): %d\n\", o, t, b}"
     200 scripts/lint-comparisons.py
90	0	scripts/lint-comparisons-baseline.tsv
200	0	scripts/lint-comparisons.py
271	0	tests/unit/test_lint_comparisons.py
outside tests/ and .orchestration/, without the baseline: 200 of 200
added under tests/: 271 of 1000
the baseline (outside the count): 90
[exit 0]
```
