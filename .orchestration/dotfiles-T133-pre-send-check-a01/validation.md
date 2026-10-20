# Validation: dotfiles-T133-pre-send-check-a01

Verbatim outputs. Home paths are written `~` and the sandbox temporary directory `$TMPDIR`. Base `60a6fb2b324d0381c4a6e539b37c650105154a7e` (origin/main at dispatch).

## 1. Red: the module before the script existed (head ff212a70, tests committed, script absent)

Each refusal assertion requires exit 1 and the named diagnostic, so the missing script (bash exit 127) fails all nine tests.

```text
$ /usr/bin/env -i PATH="$(dirname "$(command -v uv)"):/usr/bin:/bin" HOME="$HOME" TMPDIR="$TMPDIR" HTTPS_PROXY="${HTTPS_PROXY-}" HTTP_PROXY="${HTTP_PROXY-}" NO_PROXY="${NO_PROXY-}" LANG=C.UTF-8 "$HOME/.local/share/mise/installs/python/3.15.0/bin/python3" -I tests/unit/test_pre_send.py
$ ls scripts/orchestrator/pre-send.sh; git rev-parse HEAD
ls: scripts/orchestrator/pre-send.sh: No such file or directory
60a6fb2b324d0381c4a6e539b37c650105154a7e
FFFFFFFFFFFFFFFFFFFF
======================================================================
FAIL: test_all_refusals_are_reported (__main__.PreSendTest.test_all_refusals_are_reported)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 147, in test_all_refusals_are_reported
    self.refused(result, reason)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 67, in refused
    self.assertEqual(1, result.returncode, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1 != 127 : /bin/bash: $TMPDIR/tmpdobyfvb7/repo/scripts/orchestrator/pre-send.sh: No such file or directory


======================================================================
FAIL: test_consistency_refusal (__main__.PreSendTest.test_consistency_refusal)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 78, in test_consistency_refusal
    self.refused(self.run_send(self.task(name="dotfiles-T999-other-a01")), "consistency", "C1 task_id")
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 67, in refused
    self.assertEqual(1, result.returncode, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1 != 127 : /bin/bash: $TMPDIR/tmpr_f7jq62/repo/scripts/orchestrator/pre-send.sh: No such file or directory


======================================================================
FAIL: test_fenced_bash_syntax (__main__.PreSendTest.test_fenced_bash_syntax)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 111, in test_fenced_bash_syntax
    self.refused(self.run_send(path), "bash-syntax", "block(s) 2,3")
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 67, in refused
    self.assertEqual(1, result.returncode, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1 != 127 : /bin/bash: $TMPDIR/tmp9nxd6154/repo/scripts/orchestrator/pre-send.sh: No such file or directory


======================================================================
FAIL: test_input_refusal (__main__.PreSendTest.test_input_refusal) (args=())
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 160, in test_input_refusal
    self.refused(result, "input")
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 67, in refused
    self.assertEqual(1, result.returncode, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1 != 127 : /bin/bash: $TMPDIR/tmp6yjstz8w/repo/scripts/orchestrator/pre-send.sh: No such file or directory


======================================================================
FAIL: test_input_refusal (__main__.PreSendTest.test_input_refusal) (args=(PosixPath('$TMPDIR/tmp6yjstz8w/dotfiles-T999-fixture-a01.md'), PosixPath('$TMPDIR/tmp6yjstz8w/dotfiles-T999-fixture-a01.md')))
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 160, in test_input_refusal
    self.refused(result, "input")
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 67, in refused
    self.assertEqual(1, result.returncode, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1 != 127 : /bin/bash: $TMPDIR/tmp6yjstz8w/repo/scripts/orchestrator/pre-send.sh: No such file or directory


======================================================================
FAIL: test_input_refusal (__main__.PreSendTest.test_input_refusal) (args=(PosixPath('$TMPDIR/tmp6yjstz8w/absent.md'),))
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 160, in test_input_refusal
    self.refused(result, "input")
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 67, in refused
    self.assertEqual(1, result.returncode, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1 != 127 : /bin/bash: $TMPDIR/tmp6yjstz8w/repo/scripts/orchestrator/pre-send.sh: No such file or directory


======================================================================
FAIL: test_input_refusal (__main__.PreSendTest.test_input_refusal) (args=(PosixPath('$TMPDIR/tmp6yjstz8w'),))
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 160, in test_input_refusal
    self.refused(result, "input")
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 67, in refused
    self.assertEqual(1, result.returncode, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1 != 127 : /bin/bash: $TMPDIR/tmp6yjstz8w/repo/scripts/orchestrator/pre-send.sh: No such file or directory


======================================================================
FAIL: test_literal_home_refusal (__main__.PreSendTest.test_literal_home_refusal)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 90, in test_literal_home_refusal
    self.refused(self.run_send(path), "literal-home", "line(s) 14,16")
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 67, in refused
    self.assertEqual(1, result.returncode, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1 != 127 : /bin/bash: $TMPDIR/tmp82y7dbdh/repo/scripts/orchestrator/pre-send.sh: No such file or directory


======================================================================
FAIL: test_owner_section_and_rows (__main__.PreSendTest.test_owner_section_and_rows) (text=None, items=2)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 137, in test_owner_section_and_rows
    self.refused(self.run_send(path), "owner-section", refusal)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 67, in refused
    self.assertEqual(1, result.returncode, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1 != 127 : /bin/bash: $TMPDIR/tmpohykt1bm/repo/scripts/orchestrator/pre-send.sh: No such file or directory


======================================================================
FAIL: test_owner_section_and_rows (__main__.PreSendTest.test_owner_section_and_rows) (text='# r\n\n## Other\n- x\n', items=2)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 137, in test_owner_section_and_rows
    self.refused(self.run_send(path), "owner-section", refusal)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 67, in refused
    self.assertEqual(1, result.returncode, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1 != 127 : /bin/bash: $TMPDIR/tmpohykt1bm/repo/scripts/orchestrator/pre-send.sh: No such file or directory


======================================================================
FAIL: test_owner_section_and_rows (__main__.PreSendTest.test_owner_section_and_rows) (text='## Owned by dotfiles-T999-fixture-a01\n\n## Next\n', items=1)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 137, in test_owner_section_and_rows
    self.refused(self.run_send(path), "owner-section", refusal)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 67, in refused
    self.assertEqual(1, result.returncode, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1 != 127 : /bin/bash: $TMPDIR/tmpohykt1bm/repo/scripts/orchestrator/pre-send.sh: No such file or directory


======================================================================
FAIL: test_owner_section_and_rows (__main__.PreSendTest.test_owner_section_and_rows) (text='## Owned by dotfiles-T999-fixture-a01 (rows id<TAB>class)\nlocal:abc1234:1\tfix\n', items=1)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 139, in test_owner_section_and_rows
    self.passed(path)
    ~~~~~~~~~~~^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 74, in passed
    self.assertEqual(0, result.returncode, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 0 != 127 : /bin/bash: $TMPDIR/tmpohykt1bm/repo/scripts/orchestrator/pre-send.sh: No such file or directory


======================================================================
FAIL: test_owner_section_and_rows (__main__.PreSendTest.test_owner_section_and_rows) (text='# r\n\n## Owned by dotfiles-T999-fixture-a01\n- one bullet\n\n## Next\n', items=1)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 139, in test_owner_section_and_rows
    self.passed(path)
    ~~~~~~~~~~~^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 74, in passed
    self.assertEqual(0, result.returncode, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 0 != 127 : /bin/bash: $TMPDIR/tmpohykt1bm/repo/scripts/orchestrator/pre-send.sh: No such file or directory


======================================================================
FAIL: test_owner_section_and_rows (__main__.PreSendTest.test_owner_section_and_rows) (text='## Owned by dotfiles-T999-fixture-a01\n\n## Next\n- outside\nlocal:abc1234:2\tfix\n', items=1)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 137, in test_owner_section_and_rows
    self.refused(self.run_send(path), "owner-section", refusal)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 67, in refused
    self.assertEqual(1, result.returncode, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1 != 127 : /bin/bash: $TMPDIR/tmpohykt1bm/repo/scripts/orchestrator/pre-send.sh: No such file or directory


======================================================================
FAIL: test_owner_section_and_rows (__main__.PreSendTest.test_owner_section_and_rows) (text='## Owned by dotfiles-T999-fixture-a01\n\n## Next\n', items=2)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 139, in test_owner_section_and_rows
    self.passed(path)
    ~~~~~~~~~~~^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 74, in passed
    self.assertEqual(0, result.returncode, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 0 != 127 : /bin/bash: $TMPDIR/tmpohykt1bm/repo/scripts/orchestrator/pre-send.sh: No such file or directory


======================================================================
FAIL: test_passes_and_prints_final_sha256 (__main__.PreSendTest.test_passes_and_prints_final_sha256)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 153, in test_passes_and_prints_final_sha256
    self.passed(path)
    ~~~~~~~~~~~^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 74, in passed
    self.assertEqual(0, result.returncode, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 0 != 127 : /bin/bash: $TMPDIR/tmp9grk6gzf/repo/scripts/orchestrator/pre-send.sh: No such file or directory


======================================================================
FAIL: test_secret_pattern_matches_validator (__main__.PreSendTest.test_secret_pattern_matches_validator)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 85, in test_secret_pattern_matches_validator
    self.refused(result, "secret-pattern", f"2 match(es) on line(s) {lines[0]},{lines[1]}")
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 67, in refused
    self.assertEqual(1, result.returncode, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1 != 127 : /bin/bash: $TMPDIR/tmpu1en0zis/repo/scripts/orchestrator/pre-send.sh: No such file or directory


======================================================================
FAIL: test_self_cap (__main__.PreSendTest.test_self_cap) (spelling='at or under **{} lines**')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 99, in test_self_cap
    self.passed(path)  # equal to the cap
    ~~~~~~~~~~~^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 74, in passed
    self.assertEqual(0, result.returncode, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 0 != 127 : /bin/bash: $TMPDIR/tmpe2e7jseg/repo/scripts/orchestrator/pre-send.sh: No such file or directory


======================================================================
FAIL: test_self_cap (__main__.PreSendTest.test_self_cap) (spelling='at or under {} lines')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 99, in test_self_cap
    self.passed(path)  # equal to the cap
    ~~~~~~~~~~~^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 74, in passed
    self.assertEqual(0, result.returncode, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 0 != 127 : /bin/bash: $TMPDIR/tmpe2e7jseg/repo/scripts/orchestrator/pre-send.sh: No such file or directory


======================================================================
FAIL: test_self_cap (__main__.PreSendTest.test_self_cap)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 102, in test_self_cap
    self.passed(self.task("\nNo cap here.\n"))
    ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 74, in passed
    self.assertEqual(0, result.returncode, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 0 != 127 : /bin/bash: $TMPDIR/tmpe2e7jseg/repo/scripts/orchestrator/pre-send.sh: No such file or directory


----------------------------------------------------------------------
Ran 9 tests in 0.502s

FAILED (failures=20)
exit 1
```

## 2. The Bot's two P2s on 6a9edf5b, red against that script

- **4322154981:** root home literals.
- **4322154977:** longer or indented bash fences.
- **The run:** the strengthened cases ran against `6a9edf5b`'s script, swapped into the worktree and restored afterwards.

```text
$ git show 6a9edf5b:scripts/orchestrator/pre-send.sh > scripts/orchestrator/pre-send.sh; <the task's env -i module command> -k home -k fenced
FF
======================================================================
FAIL: test_fenced_bash_syntax (__main__.PreSendTest.test_fenced_bash_syntax)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 115, in test_fenced_bash_syntax
    self.refused(self.run_send(path), "bash-syntax", "block(s) 2,3,4")
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 70, in refused
    self.assertIn(detail, lines[0])
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
AssertionError: 'block(s) 2,3,4' not found in 'bash-syntax: refused (block(s) 2)'

======================================================================
FAIL: test_literal_home_refusal (__main__.PreSendTest.test_literal_home_refusal)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 93, in test_literal_home_refusal
    self.refused(self.run_send(path), "literal-home", "line(s) 14,16,17,18")
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 70, in refused
    self.assertIn(detail, lines[0])
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
AssertionError: 'line(s) 14,16,17,18' not found in 'literal-home: refused (line(s) 14,16)'

----------------------------------------------------------------------
Ran 2 tests in 0.438s

FAILED (failures=2)
exit 1
```

## 3. Green: the module at c7581cc5 (after the Bot fix 0bfa4eda and the fixture fix c7581cc5)

```text
$ <the task's env -i module command> -v
c7581cc58dfdacb003c51237afda7833e3684d38
test_all_refusals_are_reported (__main__.PreSendTest.test_all_refusals_are_reported) ... ok
test_consistency_refusal (__main__.PreSendTest.test_consistency_refusal) ... ok
test_fenced_bash_syntax (__main__.PreSendTest.test_fenced_bash_syntax) ... ok
test_input_refusal (__main__.PreSendTest.test_input_refusal) ... ok
test_literal_home_refusal (__main__.PreSendTest.test_literal_home_refusal) ... ok
test_owner_section_and_rows (__main__.PreSendTest.test_owner_section_and_rows) ... ok
test_passes_and_prints_final_sha256 (__main__.PreSendTest.test_passes_and_prints_final_sha256) ... ok
test_secret_pattern_matches_validator (__main__.PreSendTest.test_secret_pattern_matches_validator) ... ok
test_self_cap (__main__.PreSendTest.test_self_cap) ... ok

----------------------------------------------------------------------
Ran 9 tests in 4.558s

OK
exit 0
```

## 4. Static checks, the comparison lint and the preflight on its own dispatched text (0bfa4eda)

```text
$ bash -n scripts/orchestrator/pre-send.sh
exit 0
$ shellcheck -x scripts/orchestrator/pre-send.sh
exit 0
$ shfmt -i 4 -sr -d scripts/orchestrator/pre-send.sh
exit 0
$ ruff check --config ruff.toml tests/unit/test_pre_send.py
All checks passed!
exit 0
$ ruff format --config ruff.toml --check tests/unit/test_pre_send.py
1 file already formatted
exit 0
$ python3.15 -I scripts/lint-comparisons.py --baseline scripts/lint-comparisons-baseline.tsv scripts/orchestrator/pre-send.sh --changed scripts/orchestrator/pre-send.sh
exit 0
$ scripts/orchestrator/pre-send.sh ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-pre-send-check-a01.md
sha256: 907cb3d4735fa9803827aa5b358e3db98a5ee57aa622b97fe138431b4fe43f5b
exit 0
```

## 5. Caps and the crit gate

```text
$ git diff --numstat 60a6fb2b324d0381c4a6e539b37c650105154a7e...HEAD
4	0	.orchestration/dotfiles-T133-pre-send-check-a01/autoskill.md
7	0	.orchestration/dotfiles-T133-pre-send-check-a01/learning.md
77	0	.orchestration/dotfiles-T133-pre-send-check-a01/report.md
11	0	.orchestration/dotfiles-T133-pre-send-check-a01/sandbox.md
99	0	.orchestration/dotfiles-T133-pre-send-check-a01/task.md
341	0	.orchestration/dotfiles-T133-pre-send-check-a01/validation.md
89	0	scripts/orchestrator/pre-send.sh
169	0	tests/unit/test_pre_send.py
outside tests/ and .orchestration/: 89 of 90; under tests/: 169 of 220
$ make require-crit-review
Review not required: no meaningful review trigger found.
exit 0
```

## 6. CI's validate job on 1364630f, and the fixture fix c7581cc5

- **The failure:** `validate` on `1364630f` failed with `ERROR: possible committed secret in tests/unit/test_pre_send.py`. The validator scans a file's whole text, and two parts of the fixture's source matched: its `= '` fragment and its own variable name `<redacted:secret-pattern>s script

```text
$ git rev-parse HEAD
d0679105dd1c4a498b785ce11f302b1d7b5d6192
$ <the task env -i module command> -v
test_a_fence_left_open_at_the_end_is_a_bash_block (__main__.PreSendTest.test_a_fence_left_open_at_the_end_is_a_bash_block) ... FAIL
test_all_refusals_are_reported (__main__.PreSendTest.test_all_refusals_are_reported) ... ok
test_checker_diagnostics_never_echo_a_secret (__main__.PreSendTest.test_checker_diagnostics_never_echo_a_secret) ... FAIL
test_consistency_refusal (__main__.PreSendTest.test_consistency_refusal) ... ok
test_fenced_bash_syntax (__main__.PreSendTest.test_fenced_bash_syntax) ... ok
test_input_refusal (__main__.PreSendTest.test_input_refusal) ... ok
test_literal_home_refusal (__main__.PreSendTest.test_literal_home_refusal) ... ok
test_owner_section_and_rows (__main__.PreSendTest.test_owner_section_and_rows) ... ok
test_passes_and_prints_final_sha256 (__main__.PreSendTest.test_passes_and_prints_final_sha256) ... ok
test_secret_pattern_matches_validator (__main__.PreSendTest.test_secret_pattern_matches_validator) ... ok
test_self_cap (__main__.PreSendTest.test_self_cap) ... ok
test_the_owner_task_id_is_read_as_yaml (__main__.PreSendTest.test_the_owner_task_id_is_read_as_yaml) ... FAIL
test_tilde_fences_are_bash_blocks (__main__.PreSendTest.test_tilde_fences_are_bash_blocks) ... FAIL

======================================================================
FAIL: test_a_fence_left_open_at_the_end_is_a_bash_block (__main__.PreSendTest.test_a_fence_left_open_at_the_end_is_a_bash_block)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 159, in test_a_fence_left_open_at_the_end_is_a_bash_block
    self.refused(
    ~~~~~~~~~~~~^
        self.run_send(self.task("\n```bash\necho ok\n```\n\n````bash\nif then\n")), "bash-syntax", "block(s) 2"
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 67, in refused
    self.assertEqual(1, result.returncode, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1 != 0 : sha256: 4be5b78cfdf5c59181abfae7e5cb2e3473221d63178d667c541eefd553be4f8c


======================================================================
FAIL: test_checker_diagnostics_never_echo_a_secret (__main__.PreSendTest.test_checker_diagnostics_never_echo_a_secret)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 151, in test_checker_diagnostics_never_echo_a_secret
    self.assertNotIn("hunter2x", result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'hunter2x' unexpectedly found in 'consistency: refused (Traceback (most recent call last): File "$TMPDIR/tmpagg61rya/repo/scripts/orchestrator/task-consistency-check.py", line 150, in <module> sys.exit(main()) ~~~~^^ File "$TMPDIR/tmpagg61rya/repo/scripts/orchestrator/task-consistency-check.py", line 143, in main fails = check(p, args.root) File "$TMPDIR/tmpagg61rya/repo/scripts/orchestrator/task-consistency-check.py", line 48, in check fm = front(text := p.read_text()) File "$TMPDIR/tmpagg61rya/repo/scripts/orchestrator/task-consistency-check.py", line 40, in front return yaml.safe_load(text.split("\\n---\\n", 1)[0].lstrip("-\\n")) ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ File "~/.cache/uv/archive-v0/31F2mEsBsyaNJEyC/lib/python3.15/site-packages/yaml/__init__.py", line 125, in safe_load return load(stream, SafeLoader) File "~/.cache/uv/archive-v0/31F2mEsBsyaNJEyC/lib/python3.15/site-packages/yaml/__init__.py", line 81, in load return loader.get_single_data() ~~~~~~~~~~~~~~~~~~~~~~^^ File "~/.cache/uv/archive-v0/31F2mEsBsyaNJEyC/lib/python3.15/site-packages/yaml/constructor.py", line 49, in get_single_data node = self.get_single_node() File "~/.cache/uv/archive-v0/31F2mEsBsyaNJEyC/lib/python3.15/site-packages/yaml/composer.py", line 36, in get_single_node document = self.compose_document() File "~/.cache/uv/archive-v0/31F2mEsBsyaNJEyC/lib/python3.15/site-packages/yaml/composer.py", line 55, in compose_document node = self.compose_node(None, None) File "~/.cache/uv/archive-v0/31F2mEsBsyaNJEyC/lib/python3.15/site-packages/yaml/composer.py", line 84, in compose_node node = self.compose_mapping_node(anchor) File "~/.cache/uv/archive-v0/31F2mEsBsyaNJEyC/lib/python3.15/site-packages/yaml/composer.py", line 133, in compose_mapping_node item_value = self.compose_node(node, item_key) File "~/.cache/uv/archive-v0/31F2mEsBsyaNJEyC/lib/python3.15/site-packages/yaml/composer.py", line 82, in compose_node node = self.compose_sequence_node(anchor) File "~/.cache/uv/archive-v0/31F2mEsBsyaNJEyC/lib/python3.15/site-packages/yaml/composer.py", line 110, in compose_sequence_node while not self.check_event(SequenceEndEvent): ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^ File "~/.cache/uv/archive-v0/31F2mEsBsyaNJEyC/lib/python3.15/site-packages/yaml/parser.py", line 98, in check_event self.current_event = self.state() ~~~~~~~~~~^^ File "~/.cache/uv/archive-v0/31F2mEsBsyaNJEyC/lib/python3.15/site-packages/yaml/parser.py", line 483, in parse_flow_sequence_entry raise ParserError("while parsing a flow sequence", self.marks[-1], "expected \',\' or \']\', but got %r" % token.id, token.start_mark) yaml.parser.ParserError: while parsing a flow sequence in "<unicode string>", line 5, column 6: bad: [ password = \'hunter2x\' ^ expected \',\' or \']\', but got \':\' in "<unicode string>", line 6, column 14: allowed_files: ^)\nsecret-pattern: refused (1 match(es) on line(s) 6)\nsha256: 3ebe931903df368de4a3af508a4b91609d36ad754319145c74b23fbfba2feeab\n'

======================================================================
FAIL: test_the_owner_task_id_is_read_as_yaml (__main__.PreSendTest.test_the_owner_task_id_is_read_as_yaml)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 167, in test_the_owner_task_id_is_read_as_yaml
    self.refused(self.run_send(path), "owner-section", "missing")
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 67, in refused
    self.assertEqual(1, result.returncode, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1 != 0 : sha256: 44a79eb2a05a624831591a1b2fef007fca345eb3927b48be9412bd4e9e174a44


======================================================================
FAIL: test_tilde_fences_are_bash_blocks (__main__.PreSendTest.test_tilde_fences_are_bash_blocks)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 155, in test_tilde_fences_are_bash_blocks
    self.refused(self.run_send(self.task("\n~~~bash\nif then\n~~~\n")), "bash-syntax", "block(s) 1")
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 67, in refused
    self.assertEqual(1, result.returncode, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1 != 0 : sha256: 131f000be396b7b91c3fa5df2e072a6ee173a30de081c0afdf442eccb64036d4


----------------------------------------------------------------------
Ran 13 tests in 5.868s

FAILED (failures=4)
exit 1
```

## R2. Revise 1, green at c1ba793d: the module, the shell checks, ruff, the preflight on its dispatched text, caps

```text
$ git rev-parse HEAD
c1ba793de9e4e79390dcc9f9c7f6a089c65e2a09
$ <the task env -i module command> -v
test_a_fence_left_open_at_the_end_is_a_bash_block (__main__.PreSendTest.test_a_fence_left_open_at_the_end_is_a_bash_block) ... ok
test_all_refusals_are_reported (__main__.PreSendTest.test_all_refusals_are_reported) ... ok
test_checker_diagnostics_never_echo_a_secret (__main__.PreSendTest.test_checker_diagnostics_never_echo_a_secret) ... ok
test_consistency_refusal (__main__.PreSendTest.test_consistency_refusal) ... ok
test_fenced_bash_syntax (__main__.PreSendTest.test_fenced_bash_syntax) ... ok
test_input_refusal (__main__.PreSendTest.test_input_refusal) ... ok
test_literal_home_refusal (__main__.PreSendTest.test_literal_home_refusal) ... ok
test_owner_section_and_rows (__main__.PreSendTest.test_owner_section_and_rows) ... ok
test_passes_and_prints_final_sha256 (__main__.PreSendTest.test_passes_and_prints_final_sha256) ... ok
test_secret_pattern_matches_validator (__main__.PreSendTest.test_secret_pattern_matches_validator) ... ok
test_self_cap (__main__.PreSendTest.test_self_cap) ... ok
test_the_owner_task_id_is_read_as_yaml (__main__.PreSendTest.test_the_owner_task_id_is_read_as_yaml) ... ok
test_tilde_fences_are_bash_blocks (__main__.PreSendTest.test_tilde_fences_are_bash_blocks) ... ok

----------------------------------------------------------------------
Ran 13 tests in 5.320s

OK
exit 0
$ bash -n scripts/orchestrator/pre-send.sh
exit 0
$ shellcheck -x scripts/orchestrator/pre-send.sh
exit 0
$ shfmt -i 4 -sr -d scripts/orchestrator/pre-send.sh
exit 0
$ ruff check --config ruff.toml tests/unit/test_pre_send.py
All checks passed!
exit 0
$ ruff format --config ruff.toml --check tests/unit/test_pre_send.py
1 file already formatted
exit 0
$ scripts/orchestrator/pre-send.sh ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-pre-send-check-a01.md
sha256: ebe84d21dc7d36f3896b3873651aa293720b00f3c05dfc9384a899d2195d6be8
exit 0
$ git diff --numstat 230b36767eec123f90dcd79edca76993d9bb9de7 (merge-base) -- scripts tests
88	0	scripts/orchestrator/pre-send.sh
193	0	tests/unit/test_pre_send.py
```
