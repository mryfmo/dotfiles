---
task_id: dotfiles-T130-sandbox-portability-followup-a01
seat: claude-review-dot-a005
code_commit: 0b72f4c8
---

# Validation: dotfiles-T130-sandbox-portability-followup-a01

Every command ran from the worktree `.claude/worktrees/worker-d` on the branch `portability/followup-a01` (stacked on PR #395's head `5992fac5` as the dispatch note says; it is rebased onto `origin/main` after #395 merges) at `0b72f4c8` (the test commit `3887df89`, the fix `a666ac42`, the docstring commit `0b72f4c8`; §4 to §6 were re-run on `0b72f4c8`), inside the sandbox; `MAIN` names the main checkout and `T` the task id. uv ran offline. The output is verbatim, with the main checkout's and the home directory's paths replaced by `$MAIN` and `$HOME`, and each block ends with the exit status of the command shown.

## 1. Task file (sha256 5141e931…) and task copy
```console
$ shasum -a 256 "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md"; cmp "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md" && echo byte-identical
5141e9313d66a6fc414ef204a9afb38178aaeeef85c07bc76a2b5c1272758511  $MAIN/.orchestration/tasks/dotfiles-T130-sandbox-portability-followup-a01.md
5141e9313d66a6fc414ef204a9afb38178aaeeef85c07bc76a2b5c1272758511  .orchestration/dotfiles-T130-sandbox-portability-followup-a01/task.md
byte-identical
[exit 0]
```
## 1a. The task-consistency check on the dispatched file
```console
$ uv run --offline --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root "$PWD" "$MAIN/.orchestration/tasks/$T.md"
dotfiles-T130-sandbox-portability-followup-a01.md: OK
[exit 0]
```
## 1b. The owned rows at dispatch, read from the lineage's acceptance record in the main checkout (the record is the source; one row)
```console
$ awk '/^## Owned by dotfiles-T130-sandbox-portability-followup-a01/{p=1} p' "$MAIN/.orchestration/acceptance/dotfiles-T130-sandbox-portability-a01.md"
## Owned by dotfiles-T130-sandbox-portability-followup-a01 (advisory P2 of the re-review on 5992fac5 and the round-1 P3; plan 020 step 1.2; rows id<TAB>class)

4303340052	quoting-in-regex-predicates
[exit 0]
```
## 2. Branch: three commits stacked on 5992fac5
```console
$ git log --oneline 5992fac5..HEAD; git log --oneline -1 5992fac5
0b72f4c8 fix(portability): the scanner's docstring says the continuation is read from the code view (T130 sandbox-portability followup a01, worker review P3)
a666ac42 fix(portability): one scan blanks every quoted span and escaped character before the guards read shell syntax (T130 sandbox-portability followup a01, row 4303340052, D-S1-395)
3887df89 test(portability): a quoted pipe, semicolon, ampersand, escaped quote or hash inside an argument is never read as shell syntax by the guards (T130 sandbox-portability followup a01, row 4303340052, red)
--- stacked on:
5992fac5 chore(orchestration): T130 sandbox-portability a01 revise-round records (revise.yaml, the round's validation, report, sandbox, learning, worker review evidence)
[exit 0]
```
## 3. The row's check red on the test commit 3887df89 (the predicates moved to module level unchanged; the four earlier tests OK; the new test fails because the old predicate accepts lines 2 to 5 and refuses the quoted lines 6 and 7)
```console
$ UV_OFFLINE=1 uv run --no-project python -m unittest tests/unit/test_sandbox_portability.py -v
test_a_continued_diff_command_is_refused (tests.unit.test_sandbox_portability.SandboxPortabilityTest.test_a_continued_diff_command_is_refused) ... ok
test_a_quoted_hash_is_not_a_comment (tests.unit.test_sandbox_portability.SandboxPortabilityTest.test_a_quoted_hash_is_not_a_comment) ... ok
test_a_quoted_span_is_never_shell_syntax (tests.unit.test_sandbox_portability.SandboxPortabilityTest.test_a_quoted_span_is_never_shell_syntax) ... FAIL
test_no_hard_coded_tmp_in_tracked_scripts (tests.unit.test_sandbox_portability.SandboxPortabilityTest.test_no_hard_coded_tmp_in_tracked_scripts) ... ok
test_no_process_substitution_in_tracked_scripts (tests.unit.test_sandbox_portability.SandboxPortabilityTest.test_no_process_substitution_in_tracked_scripts) ... ok

======================================================================
FAIL: test_a_quoted_span_is_never_shell_syntax (tests.unit.test_sandbox_portability.SandboxPortabilityTest.test_a_quoted_span_is_never_shell_syntax)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "$MAIN/.claude/worktrees/worker-d/tests/unit/test_sandbox_portability.py", line 162, in test_a_quoted_span_is_never_shell_syntax
    self.assertEqual(
    ~~~~~~~~~~~~~~~~^
        [f"scripts/bad.sh:{n}: {text}" for n, text in enumerate(quoted.split("\n")[1:5], 2)],
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        hits(repo, {"shell"}, diff_refused),
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
AssertionError: Lists differ: ["scripts/bad.sh:2: diff --label 'old|new' <(sort a) <(sor[187 chars] b)'] != ["scripts/bad.sh:6: echo 'diff <(a) <(b)'", 'scripts/bad.s[15 chars]" b']

First differing element 0:
"scripts/bad.sh:2: diff --label 'old|new' <(sort a) <(sort b)"
"scripts/bad.sh:6: echo 'diff <(a) <(b)'"

First list contains 2 additional elements.
First extra element 2:
'scripts/bad.sh:4: diff --label "a&b" <(sort a) <(sort b)'

+ ["scripts/bad.sh:6: echo 'diff <(a) <(b)'", 'scripts/bad.sh:7: diff "<(a)" b']
- ["scripts/bad.sh:2: diff --label 'old|new' <(sort a) <(sort b)",
-  'scripts/bad.sh:3: diff --label "a;b" <(sort a) <(sort b)',
-  'scripts/bad.sh:4: diff --label "a&b" <(sort a) <(sort b)',
-  'scripts/bad.sh:5: diff --label "a\\"b # c" <(sort a) <(sort b)']

----------------------------------------------------------------------
Ran 5 tests in 1.748s

FAILED (failures=1)
[exit 1]
```
## 4. The Check: the five tests green on 0b72f4c8 (the checkout still accepted by both guards)
```console
$ UV_OFFLINE=1 uv run --no-project python -m unittest tests/unit/test_sandbox_portability.py -v
test_a_continued_diff_command_is_refused (tests.unit.test_sandbox_portability.SandboxPortabilityTest.test_a_continued_diff_command_is_refused) ... ok
test_a_quoted_hash_is_not_a_comment (tests.unit.test_sandbox_portability.SandboxPortabilityTest.test_a_quoted_hash_is_not_a_comment) ... ok
test_a_quoted_span_is_never_shell_syntax (tests.unit.test_sandbox_portability.SandboxPortabilityTest.test_a_quoted_span_is_never_shell_syntax) ... ok
test_no_hard_coded_tmp_in_tracked_scripts (tests.unit.test_sandbox_portability.SandboxPortabilityTest.test_no_hard_coded_tmp_in_tracked_scripts) ... ok
test_no_process_substitution_in_tracked_scripts (tests.unit.test_sandbox_portability.SandboxPortabilityTest.test_no_process_substitution_in_tracked_scripts) ... ok

----------------------------------------------------------------------
Ran 5 tests in 1.415s

OK
[exit 0]
```
## 5. The Check: git diff --numstat, against the stack base and against origin/main
```console
$ git diff --numstat 5992fac5...HEAD; git diff --numstat origin/main...HEAD
--- the task's own diff (5992fac5...HEAD):
63	32	tests/unit/test_sandbox_portability.py
--- against origin/main (includes PR #395's unmerged diff until the rebase):
3	0	.orchestration/dotfiles-T130-sandbox-portability-a01/autoskill.md
26	0	.orchestration/dotfiles-T130-sandbox-portability-a01/dotfiles-T130-sandbox-portability-a01-worker-crit.json
12	0	.orchestration/dotfiles-T130-sandbox-portability-a01/dotfiles-T130-sandbox-portability-a01-worker-review-receipt.md
8	0	.orchestration/dotfiles-T130-sandbox-portability-a01/learning.md
54	0	.orchestration/dotfiles-T130-sandbox-portability-a01/report.md
11	0	.orchestration/dotfiles-T130-sandbox-portability-a01/revise.yaml
23	0	.orchestration/dotfiles-T130-sandbox-portability-a01/sandbox.md
93	0	.orchestration/dotfiles-T130-sandbox-portability-a01/task.md
283	0	.orchestration/dotfiles-T130-sandbox-portability-a01/validation.md
2	2	scripts/check-statusline-tools.py
190	0	tests/unit/test_sandbox_portability.py
[exit 0]
```
## 5a. Caps summed for both bases (the Check reads origin/main...HEAD; until #395 merges that range carries #395's 159 test lines and its two literals; after the rebase only the first line applies)
```console
$ git diff --numstat <base>...HEAD | awk '…'
5992fac5: outside tests/ and .orchestration/: 0 changed lines (cap 40); under tests/: 63 added lines (cap 200)
origin/main: outside tests/ and .orchestration/: 4 changed lines (cap 40); under tests/: 190 added lines (cap 200)
[exit 0]
```
## 6. ruff on the test file
```console
$ ruff format --check tests/unit/test_sandbox_portability.py; ruff check tests/unit/test_sandbox_portability.py
1 file already formatted
[exit 0]
All checks passed!
[exit 0]
```
## 7. The round-1 P3 candidates of PR #395's worker review, measured on the checkout with the new scanner (information for the orchestrator; nothing changed, no row owns them yet)
```console
$ UV_OFFLINE=1 uv run --no-project python - <<PY … PY   # imports the test module and runs each candidate widening over the tracked files
(1) .sh/.bash/.zsh.tmpl tracked: 32; diff-guard hits if included: 0 []; /tmp-guard hits if included: 0 []
(2) lines exempt only because a comment or quoted text names TMPDIR: 0 []
(4) colordiff/sdiff/diff3/git diff/$DIFF with <( or >( in tracked shell files: 0 []
(5) shell files classified by shebang only: 28 (the refused fixture is named .sh)
(6) GIT_DIR/GIT_WORK_TREE set in this environment: ['GIT_CONFIG_COUNT', 'GIT_CONFIG_KEY_0', 'GIT_CONFIG_KEY_1', 'GIT_CONFIG_KEY_2', 'GIT_CONFIG_KEY_3', 'GIT_CONFIG_PARAMETERS', 'GIT_CONFIG_VALUE_0', 'GIT_CONFIG_VALUE_1', 'GIT_CONFIG_VALUE_2', 'GIT_CONFIG_VALUE_3', 'GIT_EDITOR', 'GIT_SSH_COMMAND']
[exit 0]
```
## 8. CompactionDB memory add (Message Contract: before completion)
```console
$ UV_OFFLINE=1 uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "[memory:decision] T130 sandbox-portability followup a01 (D-S1-395): …"
622d4f93-f1c1-4b9e-90db-2a85802337bb
[exit 0]
```
