---
task_id: dotfiles-T129-normalised-comparison-lint-followup-a01
seat: claude-standard-dot-a008
head: 1b56dc2b
---

# Validation: dotfiles-T129-normalised-comparison-lint-followup-a01

Every command ran from the worktree `.claude/worktrees/worker-f` on the branch `lint/normalised-comparisons-followup-a01` at `1b56dc2b`, inside the sandbox, through `$TMPDIR/val.sh` (a generator that prints each command, its verbatim output and its exit status); `MAIN` names the main checkout, `T` the task id, `BASE` PR #387's head `7c8e7484`. The scratch worktrees (`$R`, `$V`, `$X`, `$B`, `$S`) live under `$TMPDIR` and are removed after their block with `git worktree remove --force`. A block's status is its last command's. The red tracked-tree test of §3 to §5 is the same with the base script and baseline (§5a); see the report.

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
1b56dc2b fix(lint): the jq program is the base scan's first single-quoted string that is no option's argument (T129 followup a01 review)
be2958cf test(lint): the forms the base jq scan read stay read; map(re.escape) and a jq comment (T129 followup a01 review)
37bf6a51 fix(lint): follow jq named through a variable or a substitution to its program (T129 followup a01)
979c0429 fix(lint): locate the jq program after its options, require a normaliser application per side, escape every interpolation (T129 followup a01)
a6518485 test(lint): one refusal fixture per owned row of the lint lineage's follow-up (T129 followup a01)
1b56dc2b8e0c36282bdae426e2846464a54bba46
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
Ran 9 tests in 3.561s

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
Ran 9 tests in 3.862s
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
Ran 9 tests in 4.262s
FAILED (failures=8)
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
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_lint_comparisons.py", line 264, in test_the_tracked_tree_is_clean_against_the_baseline
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
Ran 9 tests in 4.260s

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
1	0	scripts/lint-comparisons-baseline.tsv
13	12	scripts/lint-comparisons.py
64	0	tests/unit/test_lint_comparisons.py
--- origin/main...HEAD
86	0	scripts/lint-comparisons-baseline.tsv
200	0	scripts/lint-comparisons.py
268	0	tests/unit/test_lint_comparisons.py
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
