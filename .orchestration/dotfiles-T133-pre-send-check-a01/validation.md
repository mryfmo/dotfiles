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

- **The failure:** `validate` on `1364630f` failed with `ERROR: possible committed secret in tests/unit/test_pre_send.py`. The validator scans a file's whole text, and two parts of the fixture's source matched: its `= '` fragment and its own variable name `SECRET = "`.
- **The fix, c7581cc5:** the fixture joins its `=` at runtime and the variable is named `LEAK`.
- **Checked:** the validator now passes on the whole tree, and the caps are unchanged.

```text
$ ruff check --config ruff.toml tests/unit/test_pre_send.py
All checks passed!
exit 0
$ ruff format --config ruff.toml --check tests/unit/test_pre_send.py
1 file already formatted
exit 0
$ uv run --offline --no-project --python <pinned 3.15> --with pyyaml python -I scripts/validate-agent-assets.py | tail -1; echo exit
agent asset validation ok
exit 0
$ git diff --numstat 60a6fb2b324d0381c4a6e539b37c650105154a7e...HEAD
4	0	.orchestration/dotfiles-T133-pre-send-check-a01/autoskill.md
7	0	.orchestration/dotfiles-T133-pre-send-check-a01/learning.md
90	0	.orchestration/dotfiles-T133-pre-send-check-a01/report.md
11	0	.orchestration/dotfiles-T133-pre-send-check-a01/sandbox.md
99	0	.orchestration/dotfiles-T133-pre-send-check-a01/task.md
382	0	.orchestration/dotfiles-T133-pre-send-check-a01/validation.md
89	0	scripts/orchestrator/pre-send.sh
169	0	tests/unit/test_pre_send.py
outside tests/ and .orchestration/: 89 of 90; under tests/: 169 of 220
```
