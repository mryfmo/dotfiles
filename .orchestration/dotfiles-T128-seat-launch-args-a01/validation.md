# Seat launch-argument validation

All execution was inside the managed sandbox. Unit tests use temporary HOME/profile, ps/lsof stubs and fake agmsg/GitHub data. No real ps/lsof, re-seat or runtime/model change. Home-directory prefixes in pasted output are replaced by <HOME>; temporary fixture roots are replaced by <TMP>. The commit SHA that publishes this source/evidence is reported by RESULT after creation; no future commit/CI/Bot result is claimed here.

## Command

```text
git rev-parse HEAD
b167fe0a76a2e77d262f9f556c69ba6b9f118bbe
exit=0
```

## Command

```text
git rev-parse origin/main
58303c37a2ac7854ba7f8d4032b5ee2b9c28776e
exit=0
```

## Command

```text
git diff --cached --numstat
17	1	scripts/check-regime-boundary.sh
102	0	scripts/orchestrator/seat-args.sh
56	0	tests/unit/test_check_regime_boundary.py
175	0	tests/unit/test_seat_args.py
exit=0
```

## Command

```text
git diff --cached --name-only
scripts/check-regime-boundary.sh
scripts/orchestrator/seat-args.sh
tests/unit/test_check_regime_boundary.py
tests/unit/test_seat_args.py
exit=0
```

## Command

```text
shasum -a 256 .orchestration/dotfiles-T128-seat-launch-args-a01/task.md
148f5dde8795da8a8eeb265fcbbd40be11cb27e2407c979b772dcbcba772bd8f  .orchestration/dotfiles-T128-seat-launch-args-a01/task.md
exit=0
```

## Command

```text
shellcheck scripts/orchestrator/seat-args.sh scripts/check-regime-boundary.sh
exit=0
```

## Command

```text
shfmt --indent 4 --space-redirects --diff scripts/orchestrator/seat-args.sh scripts/check-regime-boundary.sh
exit=0
```

## Command

```text
uv run --no-project ruff format --check tests/unit/test_seat_args.py tests/unit/test_check_regime_boundary.py
2 files already formatted
exit=0
```

## Command

```text
git diff --cached --check
exit=0
```

## red-seat.log

```text
UV_CACHE_DIR=/tmp/codex-worker-e-uv-cache uv run --no-project python -m unittest tests/unit/test_seat_args.py -v
test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) ... 
  test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (label='claude match') ... FAIL
  test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (label='second team') ... FAIL
  test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (label='wrong team') ... FAIL
  test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (label='resumed') ... FAIL
  test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (label='different effort') ... FAIL
  test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (label='pid order') ... FAIL
  test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (label='absolute claude') ... FAIL
  test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (label='codex cwd') ... FAIL
  test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (label='codex differs') ... FAIL
  test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (label='codex resume') ... FAIL
  test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (label='npm wrapper') ... FAIL
  test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (label='absolute codex') ... FAIL
  test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (label='codex absent') ... FAIL
  test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (label='missing key') ... FAIL
  test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (label='literal substitution') ... FAIL
  test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (label='unknown identity') ... FAIL
  test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (label='kind mismatch') ... FAIL
  test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (label='missing ps') ... FAIL
  test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (label='missing lsof') ... FAIL
test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) ... ERROR

======================================================================
ERROR: test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_seat_args.py", line 87, in test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one
    calls = (self.home / "lsof-calls").read_text().splitlines()
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "<HOME>/.local/share/mise/installs/python/latest/lib/python3.15/pathlib/__init__.py", line 986, in read_text
    with self.open(mode='r', encoding=encoding, errors=errors, newline=newline) as f:
         ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<HOME>/.local/share/mise/installs/python/latest/lib/python3.15/pathlib/__init__.py", line 970, in open
    return io.open(self, mode, buffering, encoding, errors, newline)
           ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: '<TMP>~'

======================================================================
FAIL: test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (label='claude match')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_seat_args.py", line 66, in test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one
    self.assertEqual(code, result.returncode, result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 0 != 127 : bash: <HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/scripts/orchestrator/seat-args.sh: No such file or directory


======================================================================
FAIL: test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (label='second team')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_seat_args.py", line 66, in test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one
    self.assertEqual(code, result.returncode, result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 0 != 127 : bash: <HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/scripts/orchestrator/seat-args.sh: No such file or directory


======================================================================
FAIL: test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (label='wrong team')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_seat_args.py", line 66, in test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one
    self.assertEqual(code, result.returncode, result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 3 != 127 : bash: <HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/scripts/orchestrator/seat-args.sh: No such file or directory


======================================================================
FAIL: test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (label='resumed')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_seat_args.py", line 66, in test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one
    self.assertEqual(code, result.returncode, result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 3 != 127 : bash: <HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/scripts/orchestrator/seat-args.sh: No such file or directory


======================================================================
FAIL: test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (label='different effort')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_seat_args.py", line 66, in test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one
    self.assertEqual(code, result.returncode, result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 2 != 127 : bash: <HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/scripts/orchestrator/seat-args.sh: No such file or directory


======================================================================
FAIL: test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (label='pid order')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_seat_args.py", line 66, in test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one
    self.assertEqual(code, result.returncode, result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 0 != 127 : bash: <HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/scripts/orchestrator/seat-args.sh: No such file or directory


======================================================================
FAIL: test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (label='absolute claude')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_seat_args.py", line 66, in test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one
    self.assertEqual(code, result.returncode, result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 0 != 127 : bash: <HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/scripts/orchestrator/seat-args.sh: No such file or directory


======================================================================
FAIL: test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (label='codex cwd')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_seat_args.py", line 66, in test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one
    self.assertEqual(code, result.returncode, result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 0 != 127 : bash: <HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/scripts/orchestrator/seat-args.sh: No such file or directory


======================================================================
FAIL: test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (label='codex differs')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_seat_args.py", line 66, in test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one
    self.assertEqual(code, result.returncode, result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 2 != 127 : bash: <HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/scripts/orchestrator/seat-args.sh: No such file or directory


======================================================================
FAIL: test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (label='codex resume')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_seat_args.py", line 66, in test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one
    self.assertEqual(code, result.returncode, result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 2 != 127 : bash: <HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/scripts/orchestrator/seat-args.sh: No such file or directory


======================================================================
FAIL: test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (label='npm wrapper')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_seat_args.py", line 66, in test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one
    self.assertEqual(code, result.returncode, result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 0 != 127 : bash: <HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/scripts/orchestrator/seat-args.sh: No such file or directory


======================================================================
FAIL: test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (label='absolute codex')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_seat_args.py", line 66, in test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one
    self.assertEqual(code, result.returncode, result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 0 != 127 : bash: <HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/scripts/orchestrator/seat-args.sh: No such file or directory


======================================================================
FAIL: test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (label='codex absent')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_seat_args.py", line 66, in test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one
    self.assertEqual(code, result.returncode, result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 3 != 127 : bash: <HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/scripts/orchestrator/seat-args.sh: No such file or directory


======================================================================
FAIL: test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (label='missing key')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_seat_args.py", line 84, in test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one
    self.assertEqual(4 if seam else 2, result.returncode, result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 2 != 127 : bash: <HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/scripts/orchestrator/seat-args.sh: No such file or directory


======================================================================
FAIL: test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (label='literal substitution')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_seat_args.py", line 84, in test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one
    self.assertEqual(4 if seam else 2, result.returncode, result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 2 != 127 : bash: <HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/scripts/orchestrator/seat-args.sh: No such file or directory


======================================================================
FAIL: test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (label='unknown identity')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_seat_args.py", line 84, in test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one
    self.assertEqual(4 if seam else 2, result.returncode, result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 2 != 127 : bash: <HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/scripts/orchestrator/seat-args.sh: No such file or directory


======================================================================
FAIL: test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (label='kind mismatch')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_seat_args.py", line 84, in test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one
    self.assertEqual(4 if seam else 2, result.returncode, result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 2 != 127 : bash: <HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/scripts/orchestrator/seat-args.sh: No such file or directory


======================================================================
FAIL: test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (label='missing ps')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_seat_args.py", line 84, in test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one
    self.assertEqual(4 if seam else 2, result.returncode, result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 4 != 127 : bash: <HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/scripts/orchestrator/seat-args.sh: No such file or directory


======================================================================
FAIL: test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (label='missing lsof')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_seat_args.py", line 84, in test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one
    self.assertEqual(4 if seam else 2, result.returncode, result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 4 != 127 : bash: <HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/scripts/orchestrator/seat-args.sh: No such file or directory


----------------------------------------------------------------------
Ran 1 test in 0.259s

FAILED (failures=19, errors=1)
exit=1
```

## green-seat.log

```text
UV_CACHE_DIR=/tmp/codex-worker-e-uv-cache uv run --no-project python -m unittest tests/unit/test_seat_args.py -v
test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) ... ok

----------------------------------------------------------------------
Ran 1 test in 1.485s

OK
exit=0
```

## red-boundary.log

```text
GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false UV_CACHE_DIR=/tmp/codex-worker-e-uv-cache uv run --no-project python -m unittest tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_seated_worker_without_its_profile_arguments_is_a_violation -v
test_a_seated_worker_without_its_profile_arguments_is_a_violation (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_seated_worker_without_its_profile_arguments_is_a_violation) ... 
  test_a_seated_worker_without_its_profile_arguments_is_a_violation (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_seated_worker_without_its_profile_arguments_is_a_violation) (label='resumed') ... FAIL
  test_a_seated_worker_without_its_profile_arguments_is_a_violation (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_seated_worker_without_its_profile_arguments_is_a_violation) (label='matching second team') ... FAIL

======================================================================
FAIL: test_a_seated_worker_without_its_profile_arguments_is_a_violation (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_seated_worker_without_its_profile_arguments_is_a_violation) (label='resumed')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_check_regime_boundary.py", line 324, in test_a_seated_worker_without_its_profile_arguments_is_a_violation
    self.assertEqual(sorted(expected), sorted(lines))
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: Lists differ: ['reg[16 chars]rker claude-standard-dot-a009 at .claude/workt[209 chars]b1)'] != ['reg[16 chars]rker still seated at .claude/worktrees/b1 (her[44 chars]b1)']

First differing element 0:
'regi[15 chars]rker claude-standard-dot-a009 at .claude/workt[92 chars]ched'
'regi[15 chars]rker still seated at .claude/worktrees/b1 (her[43 chars]/b1)'

First list contains 1 additional elements.
First extra element 1:
'regime-boundary: worker still seated at .claude/worktrees/b1 (herdr-agents --remove-worker .claude/worktrees/b1)'

- ['regime-boundary: worker claude-standard-dot-a009 at .claude/worktrees/b1: '
-  'seat claude-standard-dot-a009 profile=standard kind=claude process=none '
-  'args=unlaunched',
-  'regime-boundary: worker still seated at .claude/worktrees/b1 (herdr-agents '
? ^

+ ['regime-boundary: worker still seated at .claude/worktrees/b1 (herdr-agents '
? ^

   '--remove-worker .claude/worktrees/b1)']

======================================================================
FAIL: test_a_seated_worker_without_its_profile_arguments_is_a_violation (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_seated_worker_without_its_profile_arguments_is_a_violation) (label='matching second team')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_check_regime_boundary.py", line 325, in test_a_seated_worker_without_its_profile_arguments_is_a_violation
    self.assertEqual([] if missing else ["call"], (self.home / "ps-calls").read_text().splitlines())
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: Lists differ: ['call'] != []

First list contains 1 additional elements.
First extra element 0:
'call'

- ['call']
+ []

----------------------------------------------------------------------
Ran 1 test in 1.258s

FAILED (failures=2)
exit=1
```

## green-tests.log

```text
GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false UV_CACHE_DIR=/tmp/codex-worker-e-uv-cache uv run --no-project python -m unittest tests/unit/test_seat_args.py tests/unit/test_check_regime_boundary.py -v
test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) ... ok
test_a_pr_closed_unmerged_is_reported_without_an_anchored_reset_record (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_pr_closed_unmerged_is_reported_without_an_anchored_reset_record) ... ok
test_a_pr_none_record_silences_only_a_task_whose_results_name_no_pr (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_pr_none_record_silences_only_a_task_whose_results_name_no_pr) ... ok
test_a_reset_record_naming_an_unrelated_accepted_design_anchors_nothing (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_reset_record_naming_an_unrelated_accepted_design_anchors_nothing) ... ok
test_a_reset_record_silences_only_when_another_identity_accepted_its_design (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_reset_record_silences_only_when_another_identity_accepted_its_design) ... ok
test_a_seated_worker_whose_pane_is_gone_names_the_stale_removal (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_seated_worker_whose_pane_is_gone_names_the_stale_removal) ... ok
test_a_seated_worker_without_its_profile_arguments_is_a_violation (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_seated_worker_without_its_profile_arguments_is_a_violation) ... ok
test_a_task_over_a_count_is_reported (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_task_over_a_count_is_reported) ... ok
test_a_waiver_line_silences_nothing (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_waiver_line_silences_nothing) ... ok
test_an_accepted_record_silences_only_when_the_tasks_pr_is_merged (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_an_accepted_record_silences_only_when_the_tasks_pr_is_merged) ... ok
test_each_listed_task_is_counted_and_an_unsafe_id_is_skipped (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_each_listed_task_is_counted_and_an_unsafe_id_is_skipped) ... ok
test_the_probe_skips_without_the_counters_script_or_a_readable_store (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_the_probe_skips_without_the_counters_script_or_a_readable_store) ... ok

----------------------------------------------------------------------
Ran 12 tests in 15.715s

OK
exit=0
```

The first red run predates the new executable, so all19 seat subcases fail with command-not-found and its final calls-log assertion also errors because no probe ran. After the seat script existed, the boundary test failed for the missing unlaunched line and absent ps invocation; that red test proves the boundary integration, independently of new-script availability. The final full requested suite passes12 tests in15.715s. Existing boundary tests keep their exact assertions and no rendered env. No local Bats.

## Premises on origin/main

```text
git cat-file -e origin/main:scripts/orchestrator/seat-args.sh (render absent)
absent
git show origin/main:scripts/check-regime-boundary.sh | /usr/bin/grep -c seat-args
0
git show origin/main:home/dot_agents/skills/agmsg-orchestration/SKILL.md | /usr/bin/grep -c "Activate a worker model or profile change"
1
```

## Crit lookup / initial gate

```json
{
  "branch": "feat/seat-launch-args-check",
  "daemon": {
    "running": false
  },
  "review_file": "<HOME>/.crit/reviews/cc5727b5cdda/review.json",
  "review_file_exists": false,
  "sessions": [],
  "vcs": "git"
}
```

```text
make require-crit-review
Native agent review required before completion.
- review-sensitive path changed: .orchestration/dotfiles-T128-project-map-pane-open-a01-followup-a01/crit-status.json
- broad diff touches 138 files
- broad diff changes 9517 lines
Use the active agent's review path, not a browser by default:
- Codex: retrieve Crit comments/status data, review it inside the task, then address findings.
- Claude Code: retrieve Crit comments/status data, review it inside the task, then address findings.
- Use browser Crit review only when the user explicitly asks for Crit web UI or Crit data is unavailable.
Record a receipt with `review_surface:`, `reviewer:`, and `review_outcome:`.
For agent judgment, locate the review with `crit status --json`, then save `crit comments --all --json <review.json>` to a repo-local JSON file.
Evidence must contain at least one resolved record; for a finding-free review, add and resolve one review-scope approval record.
This local evidence is process evidence, not reviewer authentication.
Then use `review_surface: crit-data`, `reviewer: codex` or `reviewer: claude-code`, and `review_source: <json path>`.
After addressing review feedback, rerun with AGENT_REVIEWED=1 or CRIT_REVIEWED=1 plus REVIEW_EVIDENCE=<path>.
make: *** [require-crit-review] Error 1
exit=2
```

# Seat arguments independent worker review evidence

This records the prior seven-case stub-only check and the exact final review reply. No checks were rerun to create this file.

## Exact executed command

~~~bash
PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/tmp/codex-worker-e-uv-cache uv run --no-project python - <<'PY'
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location('seat_review_fixture', Path('tests/unit/test_seat_args.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
case = module.SeatArgsTest()
case.setUp()
identity = 'claude-standard-dot-a001'
project = str(case.temp / 'project with spaces')
expected = module.CLAUDE_ARGS
matching = f'claude {expected} -n t-{identity}'
profiles = f'MODEL_PROFILE_STANDARD_CLAUDE_ARGS="{expected}"\nMODEL_PROFILE_STANDARD_CODEX_ARGS="--profile standard"\n'
try:
    checks = [
        ('minimum matching pid ignores other team', identity, 'claude-code', profiles,
         f'300 {matching.replace("--effort xhigh", "--effort high")}\n100 {matching.replace("t-claude", "other-claude")}\n200 {matching}\n', 0, 'process=200 args=ok'),
        ('minimum matching pid wins over later correct args', identity, 'claude-code', profiles,
         f'30 {matching}\n20 {matching.replace("--effort xhigh", "--effort high")}\n', 2, 'process=20 args=differs'),
        ('nonadjacent expected tokens refused', identity, 'claude-code', profiles,
         f'200 claude --model claude-opus-5-5 --effort high xhigh --advisor fable -n t-{identity}\n', 2, 'args=differs'),
        ('exact profile key only', identity, 'claude-code', f'MODEL_PROFILE_STANDARD_CLAUDE_ARGS_EXTRA="{expected}"\n',
         f'200 {matching}\n', 2, 'args=unknown-profile'),
        ('review profile selected', 'claude-review-dot-a005', 'claude-code',
         'MODEL_PROFILE_REVIEW_CLAUDE_ARGS="--model claude-fable-5-1 --effort xhigh"\n',
         '200 claude --model claude-fable-5-1 --effort xhigh -n t-claude-review-dot-a005\n', 0, 'profile=review kind=claude process=200 args=ok'),
        ('absolute node npm wrapper', 'codex-standard-dot-a004', 'codex', profiles,
         '20 /opt/bin/node /opt/bin/codex --profile standard\n', 0, 'process=20 args=ok'),
    ]
    for label, name, kind, profile_text, lines, code, tail in checks:
        case.profiles.write_text(profile_text)
        result = case.run_probe(name, kind, 't', project, lines)
        assert result.returncode == code and tail in result.stdout, (label, result.returncode, result.stdout, result.stderr)
        print(f'{label}: exit={result.returncode} {result.stdout.strip()} PASS')
    case.profiles.write_text(profiles)
    case.ps.chmod(0o644)
    result = case.run_probe(identity, 'claude-code', 't', project, f'200 {matching}\n')
    assert result.returncode == 4 and 'args=unknown-probe' in result.stdout, (result.returncode, result.stdout)
    print(f'non-executable probe: exit={result.returncode} {result.stdout.strip()} PASS')
    print('7 additional stub-only cases passed')
finally:
    case.doCleanups()
PY
~~~

## Verbatim displayed command output

~~~text
minimum matching pid ignores other team: exit=0 seat claude-standard-dot-a001 profile=standard kind=claude process=200 args=ok PASS
minimum matching pid wins over later correct args: exit=2 seat claude-standard-dot-a001 profile=standard kind=claude process=20 args=differs expected=--model claude-opus-5-5 --effort xhigh --advisor fable found=--model claude-opus-5-5 --effort high --advisor fable -n t-claude-standard-dot-a001 PASS
nonadjacent expected tokens refused: exit=2 seat claude-standard-dot-a001 profile=standard kind=claude process=200 args=differs expected=--model claude-opus-5-5 --effort xhigh --advisor fable found=--model claude-opus-5-5 --effort high xhigh --advisor fable -n t-claude-standard-dot-a001 PASS
exact profile key only: exit=2 seat claude-standard-dot-a001 profile=standard kind=claude args=unknown-profile PASS
review profile selected: exit=0 seat claude-review-dot-a005 profile=review kind=claude process=200 args=ok PASS
absolute node npm wrapper: exit=0 seat codex-standard-dot-a004 profile=standard kind=codex process=20 args=ok PASS
non-executable probe: exit=4 seat claude-standard-dot-a001 profile=standard kind=claude args=unknown-probe PASS
7 additional stub-only cases passed
~~~

Exit status: 0, as reported by exec_command (chunk fda11c).

Stream-capture limit: exec_command exposed one combined output string, reproduced verbatim above. All displayed lines are produced by the command's Python print calls. No separate stderr text was displayed. The seven inner probe subprocesses captured stdout and stderr; the command asserted their status and stdout as shown, but did not print or persist their stderr separately. An independent verbatim per-probe stderr transcript therefore cannot be recovered without a rerun, and none is claimed here.

## Exact final review reply

Review-scope approval, high confidence. No findings in the four staged paths against fixed base `b167fe0a`.

The implementation follows the task’s selectors, literal profile parsing, adjacent-pair comparison, exit codes and per-name/type boundary grouping. No `eval` or profile sourcing was introduced.

Seven additional stub-only cases passed: minimum matching PID, earlier mismatched arguments, nonadjacent tokens, exact profile key, review-profile selection, absolute Node wrapper and non-executable probe. Source/test caps also match the reported counts.

Not checked: live processes or CI; full suites were not repeated. No repository files or refs changed.
📝 まとめ: 指定された4ファイルを独立レビューし、追加7ケースも成功しました。追加指摘はありません。
Verdict: correct


## Reviewed source byte hashes / moving remote ref

```text
41a29fd04505735b55724a9917fdb699f9a4a8f50802a8fa02920828131a0e5d  scripts/orchestrator/seat-args.sh
eb242b6e7f3ebcdeca2946993324f4012474e30ec85fdf6b418447764123d423  scripts/check-regime-boundary.sh
59c06f64e5f424daea8ebf2745e3d980f84fb963591b44f489b38014f403c844  tests/unit/test_seat_args.py
27d86374f82d7f0d069e4896173ff311725dda83b041e4a56d6285246938dfb3  tests/unit/test_check_regime_boundary.py
git rev-parse origin/main
58303c37a2ac7854ba7f8d4032b5ee2b9c28776e
```

The remote ref is shared and advanced during review; fixed branch base remains b167fe0a. No source change after the full tests/review. Source120/test231 caps are from the four staged paths against that base; final git diff --numstat origin/main...HEAD will use its merge-base.

## Evidence masking and worker gate

```text
masked 0 match(es) in .orchestration/dotfiles-T128-seat-launch-args-a01/report.md
masked 0 match(es) in .orchestration/dotfiles-T128-seat-launch-args-a01/validation.md
masked 0 match(es) in .orchestration/dotfiles-T128-seat-launch-args-a01/sandbox.md
masked 0 match(es) in .orchestration/dotfiles-T128-seat-launch-args-a01/learning.md
masked 0 match(es) in .orchestration/dotfiles-T128-seat-launch-args-a01/autoskill.md
masked 0 match(es) in .orchestration/dotfiles-T128-seat-launch-args-a01/seat-args-worker-crit.json
masked 0 match(es) in .orchestration/dotfiles-T128-seat-launch-args-a01/seat-args-worker-review-receipt.md
exit=0
```

```text
AGENT_REVIEWED=1 REVIEW_EVIDENCE=.orchestration/dotfiles-T128-seat-launch-args-a01/seat-args-worker-review-receipt.md make require-crit-review
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.
exit=0
```

## Prepublication path assertion correction

```text
Traceback (most recent call last):
  File "<stdin>", line 14, in <module>
AssertionError: validation.md
exit=1
```

The first check matched /home/ anywhere and overmatched the temporary fixture path ending in ~ in the missing-command red log. It did not identify a real user-home path. The unpublished local commit was retained as a checkpoint; path validation now checks absolute /Users or /home roots, and temp fixture prefixes are masked. No source/test change or remote publication happened between the check and correction.

```text
git diff --numstat origin/main...HEAD
3	0	.orchestration/dotfiles-T128-seat-launch-args-a01/autoskill.md
5	0	.orchestration/dotfiles-T128-seat-launch-args-a01/learning.md
19	0	.orchestration/dotfiles-T128-seat-launch-args-a01/report.md
5	0	.orchestration/dotfiles-T128-seat-launch-args-a01/sandbox.md
8	0	.orchestration/dotfiles-T128-seat-launch-args-a01/seat-args-worker-crit.json
6	0	.orchestration/dotfiles-T128-seat-launch-args-a01/seat-args-worker-review-receipt.md
107	0	.orchestration/dotfiles-T128-seat-launch-args-a01/task.md
575	0	.orchestration/dotfiles-T128-seat-launch-args-a01/validation.md
17	1	scripts/check-regime-boundary.sh
102	0	scripts/orchestrator/seat-args.sh
56	0	tests/unit/test_check_regime_boundary.py
175	0	tests/unit/test_seat_args.py
exit=0
```

```text
git diff --check origin/main...HEAD -- scripts/orchestrator/seat-args.sh scripts/check-regime-boundary.sh tests/unit/test_seat_args.py tests/unit/test_check_regime_boundary.py
exit=0
```

```text
shasum -a 256 .orchestration/dotfiles-T128-seat-launch-args-a01/task.md
148f5dde8795da8a8eeb265fcbbd40be11cb27e2407c979b772dcbcba772bd8f  .orchestration/dotfiles-T128-seat-launch-args-a01/task.md
exit=0
```

The numstat above is the unpublished commit before this validation-output append; the only amendment is this evidence file. Source changed120 and test added231 are unchanged; artifacts are excluded from both caps.

A second generic root-path regex also matched the literal /home/ in this explanation (AssertionError: validation.md, exit1). The final check uses the actual current home prefix, already masked throughout, rather than generic path examples. It passes; independent review also found no home-directory paths.

```text
validated12 allowed paths,8 canonical evidence records,0 committed worklogs; actual user home prefix absent; task SHA256 matches; source_changed=120 test_added=231
exit=0
```

## C50 revision for Bot P2 4301264676

Authorized at2026-10-17T04:07:05Z, previous_head274257172db0915df34e9f1764c69f572346727f, profile-name-grammar occurrence1. check=tests/unit/test_seat_args.py::SeatArgsTest::test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one. The generator PROFILE_NAME_RE accepts ^[a-z][a-z0-9_]*$, and launcher embeds the chosen profile in the identity; exact profile-key parsing is unchanged. Only a one-character regex extension and a seven-line subcase were added.

### First-head PR metadata (gh pr view383 JSON)

```text
{"baseRefOid":"58303c37a2ac7854ba7f8d4032b5ee2b9c28776e","headRefName":"feat/seat-launch-args-check","headRefOid":"274257172db0915df34e9f1764c69f572346727f","number":383,"url":"https://github.com/mryfmo/dotfiles/pull/383"}

```

### First-head CI progress, pending is not success

```text
[{"completedAt":"2026-10-17T04:08:19Z","link":"https://github.com/mryfmo/dotfiles/actions/runs/39000924198/job/117303477527","name":"test (macos-14, client)","state":"SUCCESS"},{"completedAt":"0001-01-01T00:00:00Z","link":"https://github.com/mryfmo/dotfiles/actions/runs/39000924147/job/117303477368","name":"public-bootstrap (macos-14, client)","state":"IN_PROGRESS"},{"completedAt":"2026-10-17T04:00:41Z","link":"https://github.com/mryfmo/dotfiles/actions/runs/39000924147/job/117303477475","name":"private-bootstrap (macos-14, client)","state":"SUCCESS"},{"completedAt":"0001-01-01T00:00:00Z","link":"https://github.com/mryfmo/dotfiles/actions/runs/39000924198/job/117303477566","name":"test (ubuntu-26.04, client)","state":"IN_PROGRESS"},{"completedAt":"2026-10-17T04:07:01Z","link":"https://github.com/mryfmo/dotfiles/actions/runs/39000924147/job/117303477729","name":"public-bootstrap (ubuntu-24.04, server)","state":"SUCCESS"},{"completedAt":"2026-10-17T04:06:11Z","link":"https://github.com/mryfmo/dotfiles/actions/runs/39000924198/job/117303477232","name":"test (ubuntu-24.04, server)","state":"SUCCESS"},{"completedAt":"0001-01-01T00:00:00Z","link":"https://github.com/mryfmo/dotfiles/actions/runs/39000924147/job/117303477535","name":"public-bootstrap (ubuntu-24.04, client)","state":"IN_PROGRESS"},{"completedAt":"2026-10-17T04:07:58Z","link":"https://github.com/mryfmo/dotfiles/actions/runs/39000924198/job/117303477416","name":"test (ubuntu-24.04, client)","state":"SUCCESS"},{"completedAt":"2026-10-17T04:00:34Z","link":"https://github.com/mryfmo/dotfiles/actions/runs/39000924147/job/117303477663","name":"private-bootstrap (ubuntu-24.04, client)","state":"SUCCESS"},{"completedAt":"2026-10-17T04:00:34Z","link":"https://github.com/mryfmo/dotfiles/actions/runs/39000924147/job/117303477672","name":"private-bootstrap (ubuntu-24.04, server)","state":"SUCCESS"},{"completedAt":"2026-10-17T04:01:29Z","link":"https://github.com/mryfmo/dotfiles/actions/runs/39000924124/job/117303476842","name":"validate","state":"SUCCESS"},{"completedAt":"2026-10-17T04:00:31Z","link":"https://dashboard.gitguardian.com","name":"GitGuardian Security Checks","state":"SUCCESS"},{"completedAt":"0001-01-01T00:00:00Z","link":"","name":"CodeRabbit","state":"SUCCESS"}]

```

### First-head Bot review body and inline finding

```text
{
  "head": "274257172db0915df34e9f1764c69f572346727f",
  "reviews": [
    {
      "body": "<!-- codex-review-receipt:v1 -->\n\n\n### \ud83d\udca1 Codex Review\n\nHere are some automated review suggestions for this pull request.\n\n**Reviewed commit:** `274257172d`\n    \n\n<details> <summary>\u2139\ufe0f About Codex in GitHub</summary>\n<br/>\n\nCodex has been enabled to automatically review pull requests in this repo. Reviews are triggered when you\n- Open a pull request for review\n- Mark a draft as ready\n- Comment \"@codex review\".\n\nIf Codex has suggestions, it will comment; otherwise it will react with \ud83d\udc4d.\n\n\n\n\nWhen you [sign up for Codex through ChatGPT](https://openai.com/codex), Codex can also answer questions or update the PR, like \"@codex address that feedback\".\n            \n</details>",
      "commit_id": "274257172db0915df34e9f1764c69f572346727f",
      "html_url": "https://github.com/mryfmo/dotfiles/pull/383#pullrequestreview-5556009034",
      "id": 5556009034,
      "state": "COMMENTED",
      "submitted_at": "2026-10-17T04:03:23Z"
    }
  ],
  "inline": [
    {
      "body": "**<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Accept launcher-valid underscores in profile names**\n\nWhen a model profile contains an underscore, the existing generator accepts it (`scripts/generate-agent-configs.py:77`) and `herdr-agents` accepts it and embeds it in the worker identity (`home/dot_local/bin/common/executable_herdr-agents:1818-1820,329`), but this regex rejects that identity before reading its rendered profile. Thus a valid seat such as `claude-my_profile-dot-a001` is permanently reported as `args=unknown-identity` even when its process arguments match; extend the identity parser to support the same profile-name grammar as the launcher.\n\nUseful? React with \ud83d\udc4d\u00a0/ \ud83d\udc4e.\n\n<!-- codex-code-review-finding:v1 -->",
      "html_url": "https://github.com/mryfmo/dotfiles/pull/383#discussion_r4301264676",
      "id": 4301264676,
      "line": 17,
      "original_commit_id": "274257172db0915df34e9f1764c69f572346727f",
      "path": "scripts/orchestrator/seat-args.sh"
    }
  ],
  "issue_comments": [
    {
      "body": "<!-- codex-pull-request-review-summary -->\n<!-- codex-review-state:v1 {\"code_review\":{\"commit_sha\":\"274257172db0915df34e9f1764c69f572346727f\",\"has_any_findings\":true,\"has_unresolved_findings\":true,\"status\":\"completed\"},\"security_review\":{\"commit_sha\":\"274257172db0915df34e9f1764c69f572346727f\",\"has_any_findings\":null,\"has_unresolved_findings\":null,\"status\":\"running\"}} -->\n<!-- codex-security-review:v1 {\"blockingSeverityThreshold\":\"P0\",\"headSha\":\"274257172db0915df34e9f1764c69f572346727f\",\"mergeGateEnabled\":false,\"pullRequestNumber\":383,\"repository\":\"mryfmo/dotfiles\",\"status\":\"running\"} -->\n## Codex Review Summary\n\nThis comment shows the latest Codex review activity on this pull request.\n\n| Review | Status | Commit | Review trigger |\n| --- | --- | --- | --- |\n| \ud83d\udcdd **Code Review** | \u2705 **Completed** <relative-time datetime=\"2026-10-17T04:03:25.509119Z\">2026-10-17T04:03:25.509119Z</relative-time> | `2742571` | Draft marked ready |\n| \ud83d\udd12 **Security Review** | \ud83d\udd04 **Running** since <relative-time datetime=\"2026-10-17T04:00:54.386752Z\">2026-10-17T04:00:54.386752Z</relative-time> | `2742571` | Draft marked ready |\n\n\n\n<details> <summary>\u2139\ufe0f About Codex in GitHub</summary>\n<br/>\n\n[Your team has set up Codex to review pull requests in this repo](https://chatgpt.com/codex/cloud/settings/general). Reviews are triggered when you\n- Open a pull request for review\n- Mark a draft as ready\n- Comment \"@codex review\" or \"@codex security review\".\n\nCodex reacts with \ud83d\udc40 while any review is running, comments if it has suggestions, and reacts with \ud83d\udc4d once all reviews finish with no findings.\n\n</details>",
      "created_at": "2026-10-17T04:00:57Z",
      "html_url": "https://github.com/mryfmo/dotfiles/pull/383#issuecomment-6229380503",
      "id": 6229380503,
      "updated_at": "2026-10-17T04:03:26Z"
    }
  ]
}

```

### Regression RED before regex change: unittest prescribed seat method -v; exit1 expected

```text
test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) ... 
  test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (label='underscore profile') ... FAIL

======================================================================
FAIL: test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (label='underscore profile')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_seat_args.py", line 110, in test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one
    self.assertEqual(0, result.returncode, result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 0 != 2 : 

----------------------------------------------------------------------
Ran 1 test in 1.317s

FAILED (failures=1)

```

### GREEN: UV_CACHE_DIR=/tmp/codex-worker-e-uv-cache GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false uv run --no-project python -m unittest tests/unit/test_seat_args.py tests/unit/test_check_regime_boundary.py -v; exit0

```text
test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) ... ok
test_a_pr_closed_unmerged_is_reported_without_an_anchored_reset_record (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_pr_closed_unmerged_is_reported_without_an_anchored_reset_record) ... ok
test_a_pr_none_record_silences_only_a_task_whose_results_name_no_pr (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_pr_none_record_silences_only_a_task_whose_results_name_no_pr) ... ok
test_a_reset_record_naming_an_unrelated_accepted_design_anchors_nothing (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_reset_record_naming_an_unrelated_accepted_design_anchors_nothing) ... ok
test_a_reset_record_silences_only_when_another_identity_accepted_its_design (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_reset_record_silences_only_when_another_identity_accepted_its_design) ... ok
test_a_seated_worker_whose_pane_is_gone_names_the_stale_removal (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_seated_worker_whose_pane_is_gone_names_the_stale_removal) ... ok
test_a_seated_worker_without_its_profile_arguments_is_a_violation (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_seated_worker_without_its_profile_arguments_is_a_violation) ... ok
test_a_task_over_a_count_is_reported (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_task_over_a_count_is_reported) ... ok
test_a_waiver_line_silences_nothing (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_waiver_line_silences_nothing) ... ok
test_an_accepted_record_silences_only_when_the_tasks_pr_is_merged (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_an_accepted_record_silences_only_when_the_tasks_pr_is_merged) ... ok
test_each_listed_task_is_counted_and_an_unsafe_id_is_skipped (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_each_listed_task_is_counted_and_an_unsafe_id_is_skipped) ... ok
test_the_probe_skips_without_the_counters_script_or_a_readable_store (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_the_probe_skips_without_the_counters_script_or_a_readable_store) ... ok

----------------------------------------------------------------------
Ran 12 tests in 16.860s

OK

```

An initial shfmt -d invocation omitted repository indent4/space-redirects flags and exited1 with indentation-only differences. The repeated deterministic output is captured below; no formatter write ran. ShellCheck before it exited0; the remainder of that initial && chain did not run.

```diff
diff scripts/orchestrator/seat-args.sh.orig scripts/orchestrator/seat-args.sh
--- scripts/orchestrator/seat-args.sh.orig
+++ scripts/orchestrator/seat-args.sh
@@ -16,13 +16,13 @@
 
 teams=$1 identity=$2 agent_type=$3 project=$4
 if [[ ! ${identity} =~ ^(claude|codex)-([a-z][a-z0-9_]*)-[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
-    printf 'seat %s args=unknown-identity\n' "${identity}"
-    exit 2
+	printf 'seat %s args=unknown-identity\n' "${identity}"
+	exit 2
 fi
 kind=${BASH_REMATCH[1]} profile=${BASH_REMATCH[2]}
 if [[ ${kind}:${agent_type} != claude:claude-code && ${kind}:${agent_type} != codex:codex ]]; then
-    printf 'seat %s args=unknown-identity\n' "${identity}"
-    exit 2
+	printf 'seat %s args=unknown-identity\n' "${identity}"
+	exit 2
 fi
 label="seat ${identity} profile=${profile} kind=${kind}"
 key="MODEL_PROFILE_$(tr '[:lower:]' '[:upper:]' <<< "${profile}_${kind}")_ARGS"
@@ -30,8 +30,8 @@
     print substr($0, length(key) + 3, length($0) - length(key) - 3); exit
 }' "${HOME}/.agents/model-profiles.env" 2> /dev/null)" || expected=""
 if [[ -z ${expected} ]]; then
-    printf '%s args=unknown-profile\n' "${label}"
-    exit 2
+	printf '%s args=unknown-profile\n' "${label}"
+	exit 2
 fi
 [[ ${kind} != codex ]] || expected="--profile ${profile}"
 read -r -a expected_args <<< "${expected}"
@@ -40,8 +40,8 @@
 lsof_probe=${SEAT_ARGS_LSOF:-/usr/sbin/lsof}
 [[ -n ${SEAT_ARGS_LSOF+x} || -x ${lsof_probe} ]] || lsof_probe=/usr/bin/lsof
 if [[ ! -x ${ps_probe} ]] || { [[ ${kind} == codex ]] && [[ ! -x ${lsof_probe} ]]; }; then
-    printf '%s args=unknown-probe\n' "${label}"
-    exit 4
+	printf '%s args=unknown-probe\n' "${label}"
+	exit 4
 fi
 
 # @description Find one literal adjacent pair in the current process tokens.
@@ -48,55 +48,55 @@
 # @arg $1 string Flag.
 # @arg $2 string Value.
 has_pair() {
-    local index
-    for ((index = 1; index + 1 < ${#words[@]}; index++)); do
-        [[ ${words[index]} != "$1" || ${words[index + 1]} != "$2" ]] || return 0
-    done
-    return 1
+	local index
+	for ((index = 1; index + 1 < ${#words[@]}; index++)); do
+		[[ ${words[index]} != "$1" || ${words[index + 1]} != "$2" ]] || return 0
+	done
+	return 1
 }
 
 selected_pid=""
 while read -r pid process_args; do
-    [[ ${pid} =~ ^[0-9]+$ ]] || continue
-    if [[ -n ${selected_pid} ]] && ((10#${pid} >= 10#${selected_pid})); then continue; fi
-    read -r -a words <<< "${process_args}"
-    program=${words[0]:-}
-    if [[ ${kind} == claude ]]; then
-        [[ ${program##*/} == claude ]] || continue
-        matched=false
-        for team in "${team_names[@]}"; do
-            if has_pair -n "${team}-${identity}"; then
-                matched=true
-                break
-            fi
-        done
-        [[ ${matched} == true ]] || continue
-    else
-        if [[ ${program##*/} != codex ]] &&
-            { [[ ${program##*/} != node ]] || [[ ${words[1]:-} != */codex ]]; }; then continue; fi
-        cwd="$("${lsof_probe}" -a -p "${pid}" -d cwd -Fn 2> /dev/null | sed -n 's/^n//p')" || cwd=""
-        [[ ${cwd} == "${project}" ]] || continue
-    fi
-    selected_pid=${pid}
-    selected=("${words[@]}")
+	[[ ${pid} =~ ^[0-9]+$ ]] || continue
+	if [[ -n ${selected_pid} ]] && ((10#${pid} >= 10#${selected_pid})); then continue; fi
+	read -r -a words <<< "${process_args}"
+	program=${words[0]:-}
+	if [[ ${kind} == claude ]]; then
+		[[ ${program##*/} == claude ]] || continue
+		matched=false
+		for team in "${team_names[@]}"; do
+			if has_pair -n "${team}-${identity}"; then
+				matched=true
+				break
+			fi
+		done
+		[[ ${matched} == true ]] || continue
+	else
+		if [[ ${program##*/} != codex ]] &&
+			{ [[ ${program##*/} != node ]] || [[ ${words[1]:-} != */codex ]]; }; then continue; fi
+		cwd="$("${lsof_probe}" -a -p "${pid}" -d cwd -Fn 2> /dev/null | sed -n 's/^n//p')" || cwd=""
+		[[ ${cwd} == "${project}" ]] || continue
+	fi
+	selected_pid=${pid}
+	selected=("${words[@]}")
 done < <("${ps_probe}" -axo pid=,command= 2> /dev/null)
 
 if [[ -z ${selected_pid} ]]; then
-    printf '%s process=none args=unlaunched\n' "${label}"
-    exit 3
+	printf '%s process=none args=unlaunched\n' "${label}"
+	exit 3
 fi
 words=("${selected[@]}")
 ok=true
 ((${#expected_args[@]} % 2 == 0)) || ok=false
 for ((index = 0; index + 1 < ${#expected_args[@]}; index += 2)); do
-    has_pair "${expected_args[index]}" "${expected_args[index + 1]}" || ok=false
+	has_pair "${expected_args[index]}" "${expected_args[index + 1]}" || ok=false
 done
 if [[ ${ok} == true ]]; then
-    printf '%s process=%s args=ok\n' "${label}" "${selected_pid}"
-    exit 0
+	printf '%s process=%s args=ok\n' "${label}" "${selected_pid}"
+	exit 0
 fi
 offset=1
 [[ ${words[0]##*/} != node ]] || offset=2
 printf '%s process=%s args=differs expected=%s found=%s\n' \
-    "${label}" "${selected_pid}" "${expected_args[*]}" "${words[*]:offset}"
+	"${label}" "${selected_pid}" "${expected_args[*]}" "${words[*]:offset}"
 exit 2
diff scripts/check-regime-boundary.sh.orig scripts/check-regime-boundary.sh
--- scripts/check-regime-boundary.sh.orig
+++ scripts/check-regime-boundary.sh
@@ -35,7 +35,7 @@
 
 report=false
 if [[ ${1:-} == --report ]]; then
-    report=true
+	report=true
 fi
 root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
 # Worker workspace labels are `<main checkout basename> worker <name>`, also
@@ -42,7 +42,7 @@
 # when this script runs from a linked worktree.
 main="${root}"
 if common="$(git -C "${root}" rev-parse --path-format=absolute --git-common-dir 2> /dev/null)"; then
-    main="${common%/.git}"
+	main="${common%/.git}"
 fi
 scripts="${HOME}/.agents/skills/agmsg/scripts"
 violations=()
@@ -49,14 +49,14 @@
 
 checkouts=()
 while IFS= read -r checkout; do
-    [[ -n ${checkout} ]] && checkouts+=("${checkout}")
+	[[ -n ${checkout} ]] && checkouts+=("${checkout}")
 done < <(git -C "${root}" worktree list --porcelain 2> /dev/null | sed -n 's/^worktree //p')
 [[ ${#checkouts[@]} -gt 0 ]] || checkouts=("${root}")
 
 for checkout in "${checkouts[@]}"; do
-    while IFS= read -r path; do
-        [[ -n ${path} ]] && violations+=("untracked .orchestration file in ${checkout}: ${path}")
-    done < <(git -C "${checkout}" ls-files --others --exclude-standard -- .orchestration 2> /dev/null)
+	while IFS= read -r path; do
+		[[ -n ${path} ]] && violations+=("untracked .orchestration file in ${checkout}: ${path}")
+	done < <(git -C "${checkout}" ls-files --others --exclude-standard -- .orchestration 2> /dev/null)
 done
 
 # @description Print the number of distinct agmsg identity names at a path.
@@ -63,7 +63,7 @@
 # @arg $1 path Checkout path.
 # @arg $2 string Agent type.
 count_names() {
-    AGMSG_RESOLVE_PROJECT=0 "${scripts}/identities.sh" "$1" "$2" 2> /dev/null | cut -f 2 | sort -u | grep -c . || true
+	AGMSG_RESOLVE_PROJECT=0 "${scripts}/identities.sh" "$1" "$2" 2> /dev/null | cut -f 2 | sort -u | grep -c . || true
 }
 
 # @description Print a seated member's pane state, `present`, `gone` or
@@ -74,88 +74,88 @@
 # @arg $1 string Team.
 # @arg $2 string Member identity.
 seat_pane_state() {
-    local state
-    # shellcheck disable=SC2016 # the inner script expands its own positional args
-    state="$(env SKILL_DIR="${HOME}/.agents/skills/agmsg" bash -c '
+	local state
+	# shellcheck disable=SC2016 # the inner script expands its own positional args
+	state="$(env SKILL_DIR="${HOME}/.agents/skills/agmsg" bash -c '
         source "$1/lib/actas-lock.sh" && source "$1/lib/terminal-registry.sh" || exit 1
         record="$(agmsg_spawn_path "$2" "$3")" && [[ -r ${record} ]] || exit 1
         ref="$(head -n 1 "${record}" | cut -f 1)"
         terminal="$(agmsg_terminal_ref_terminal "${ref}")" && id="$(agmsg_terminal_ref_id "${ref}")" || exit 1
         agmsg_terminal_load "${terminal}" > /dev/null && terminal_pane_state "${id}"' _ "${scripts}" "$1" "$2" 2> /dev/null)" || state=""
-    case "${state}" in
-    present | gone) printf '%s\n' "${state}" ;;
-    *) printf 'unknown\n' ;;
-    esac
+	case "${state}" in
+	present | gone) printf '%s\n' "${state}" ;;
+	*) printf 'unknown\n' ;;
+	esac
 }
 
 if [[ -x ${scripts}/identities.sh ]]; then
-    # The only active seat is the main checkout (orchestrator): it holds
-    # exactly one identity across both runtime types. Workers are seated on
-    # demand in linked worktrees, so an identity left at one at a boundary is
-    # a worker still seated; any other checkout is flagged only for a
-    # per-type surplus.
-    names="$({
-        AGMSG_RESOLVE_PROJECT=0 "${scripts}/identities.sh" "${main}" claude-code 2> /dev/null || true
-        AGMSG_RESOLVE_PROJECT=0 "${scripts}/identities.sh" "${main}" codex 2> /dev/null || true
-    } | cut -f 2 | sort -u | grep -c . || true)"
-    if ((names == 0)); then
-        violations+=("no agmsg identity at the active seat ${main} (expected one)")
-    elif ((names > 1)); then
-        violations+=("stray identities at the active seat ${main}: ${names} names across claude-code and codex (expected one)")
-    fi
-    # Only a seated orchestrator checkout must stay on main; a CI checkout
-    # with no identity may sit at a detached HEAD.
-    if ((names > 0)); then
-        branch="$(git -C "${main}" symbolic-ref -q --short HEAD 2> /dev/null || true)"
-        if [[ ${branch} != main ]]; then
-            violations+=("orchestrator seat is not on main: ${branch:-detached at $(git -C "${main}" rev-parse --short HEAD 2> /dev/null || echo unknown)}")
-        fi
-    fi
-    resolved_main="$(cd -- "${main}" && pwd -P)"
-    for checkout in "${checkouts[@]}"; do
-        resolved="$(cd -- "${checkout}" 2> /dev/null && pwd -P)" || resolved="${checkout}"
-        [[ ${resolved} != "${resolved_main}" ]] || continue
-        seated=0
-        for agent_type in claude-code codex; do
-            names="$(count_names "${checkout}" "${agent_type}")"
-            seated=$((seated + names))
-            if ((names > 1)); then
-                violations+=("stray ${agent_type} identities at ${checkout}: ${names} names (expected one)")
-            fi
-        done
-        if ((seated > 0)) && [[ ${resolved} == "${resolved_main}/.claude/worktrees/"* ]]; then
-            worktree=".claude/worktrees/${resolved#"${resolved_main}/.claude/worktrees/"}"
-            if [[ -x ${root}/scripts/orchestrator/seat-args.sh && -f ${HOME}/.agents/model-profiles.env ]]; then
-                for agent_type in claude-code codex; do
-                    while IFS=$'\t' read -r name teams; do
-                        probe_status=0
-                        launch_line="$("${root}/scripts/orchestrator/seat-args.sh" "${teams}" "${name}" "${agent_type}" "${checkout}" < /dev/null)" || probe_status=$?
-                        case ${probe_status} in
-                        2 | 3) violations+=("worker ${name} at ${worktree}: ${launch_line}") ;;
-                        esac
-                    done < <(AGMSG_RESOLVE_PROJECT=0 "${scripts}/identities.sh" "${checkout}" "${agent_type}" 2> /dev/null |
-                        awk -F '\t' 'NF >= 2 && $2 != "" {
+	# The only active seat is the main checkout (orchestrator): it holds
+	# exactly one identity across both runtime types. Workers are seated on
+	# demand in linked worktrees, so an identity left at one at a boundary is
+	# a worker still seated; any other checkout is flagged only for a
+	# per-type surplus.
+	names="$({
+		AGMSG_RESOLVE_PROJECT=0 "${scripts}/identities.sh" "${main}" claude-code 2> /dev/null || true
+		AGMSG_RESOLVE_PROJECT=0 "${scripts}/identities.sh" "${main}" codex 2> /dev/null || true
+	} | cut -f 2 | sort -u | grep -c . || true)"
+	if ((names == 0)); then
+		violations+=("no agmsg identity at the active seat ${main} (expected one)")
+	elif ((names > 1)); then
+		violations+=("stray identities at the active seat ${main}: ${names} names across claude-code and codex (expected one)")
+	fi
+	# Only a seated orchestrator checkout must stay on main; a CI checkout
+	# with no identity may sit at a detached HEAD.
+	if ((names > 0)); then
+		branch="$(git -C "${main}" symbolic-ref -q --short HEAD 2> /dev/null || true)"
+		if [[ ${branch} != main ]]; then
+			violations+=("orchestrator seat is not on main: ${branch:-detached at $(git -C "${main}" rev-parse --short HEAD 2> /dev/null || echo unknown)}")
+		fi
+	fi
+	resolved_main="$(cd -- "${main}" && pwd -P)"
+	for checkout in "${checkouts[@]}"; do
+		resolved="$(cd -- "${checkout}" 2> /dev/null && pwd -P)" || resolved="${checkout}"
+		[[ ${resolved} != "${resolved_main}" ]] || continue
+		seated=0
+		for agent_type in claude-code codex; do
+			names="$(count_names "${checkout}" "${agent_type}")"
+			seated=$((seated + names))
+			if ((names > 1)); then
+				violations+=("stray ${agent_type} identities at ${checkout}: ${names} names (expected one)")
+			fi
+		done
+		if ((seated > 0)) && [[ ${resolved} == "${resolved_main}/.claude/worktrees/"* ]]; then
+			worktree=".claude/worktrees/${resolved#"${resolved_main}/.claude/worktrees/"}"
+			if [[ -x ${root}/scripts/orchestrator/seat-args.sh && -f ${HOME}/.agents/model-profiles.env ]]; then
+				for agent_type in claude-code codex; do
+					while IFS=$'\t' read -r name teams; do
+						probe_status=0
+						launch_line="$("${root}/scripts/orchestrator/seat-args.sh" "${teams}" "${name}" "${agent_type}" "${checkout}" < /dev/null)" || probe_status=$?
+						case ${probe_status} in
+						2 | 3) violations+=("worker ${name} at ${worktree}: ${launch_line}") ;;
+						esac
+					done < <(AGMSG_RESOLVE_PROJECT=0 "${scripts}/identities.sh" "${checkout}" "${agent_type}" 2> /dev/null |
+						awk -F '\t' 'NF >= 2 && $2 != "" {
                             if (!($2 in teams)) { names[++n] = $2; teams[$2] = $1 }
                             else teams[$2] = teams[$2] "," $1
                         } END { for (i = 1; i <= n; i++) print names[i] "\t" teams[names[i]] }')
-                done
-            fi
-            # The first identity row decides whether the seat's pane is gone.
-            row="$({
-                AGMSG_RESOLVE_PROJECT=0 "${scripts}/identities.sh" "${checkout}" claude-code
-                AGMSG_RESOLVE_PROJECT=0 "${scripts}/identities.sh" "${checkout}" codex
-            } 2> /dev/null | head -n 1)" || row=""
-            if [[ -n ${row} && $(seat_pane_state "$(cut -f 1 <<< "${row}")" "$(cut -f 2 <<< "${row}")") == gone ]]; then
-                violations+=("worker seated but its pane is gone at ${worktree} (herdr-agents --remove-worker ${worktree} --stale)")
-            else
-                violations+=("worker still seated at ${worktree} (herdr-agents --remove-worker ${worktree})")
-            fi
-        fi
-    done
+				done
+			fi
+			# The first identity row decides whether the seat's pane is gone.
+			row="$({
+				AGMSG_RESOLVE_PROJECT=0 "${scripts}/identities.sh" "${checkout}" claude-code
+				AGMSG_RESOLVE_PROJECT=0 "${scripts}/identities.sh" "${checkout}" codex
+			} 2> /dev/null | head -n 1)" || row=""
+			if [[ -n ${row} && $(seat_pane_state "$(cut -f 1 <<< "${row}")" "$(cut -f 2 <<< "${row}")") == gone ]]; then
+				violations+=("worker seated but its pane is gone at ${worktree} (herdr-agents --remove-worker ${worktree} --stale)")
+			else
+				violations+=("worker still seated at ${worktree} (herdr-agents --remove-worker ${worktree})")
+			fi
+		fi
+	done
 fi
 
 if command -v pgrep > /dev/null 2>&1 && pgrep -f 'crit _serve' > /dev/null 2>&1; then
-    violations+=("crit review server still running (pgrep -f 'crit _serve')")
+	violations+=("crit review server still running (pgrep -f 'crit _serve')")
 fi
 
 # Canonical clone: the chezmoi source checkout, when it is not this working
@@ -163,73 +163,73 @@
 # means something ran where it must not, and it blocks the operator's next
 # pull and apply.
 if command -v chezmoi > /dev/null 2>&1 &&
-    src="$(chezmoi source-path 2> /dev/null)" &&
-    canon="$(git -C "${src}" rev-parse --show-toplevel 2> /dev/null)" &&
-    [[ "$(cd -- "${canon}" && pwd -P)" != "$(cd -- "${main}" && pwd -P)" ]]; then
-    ref=HEAD
-    if git -C "${canon}" rev-parse -q --verify origin/main > /dev/null 2>&1; then
-        ref=origin/main
-    fi
-    if [[ -n "$(git -C "${canon}" ls-files -u 2> /dev/null)" ]]; then
-        violations+=("canonical clone ${canon} has unmerged entries (git ls-files -u); finish or abort its pull")
-    fi
-    if [[ -n "$(git -C "${canon}" stash list 2> /dev/null)" ]]; then
-        violations+=("canonical clone ${canon} carries a stash (git stash list); drop only the autostash entry once its content is on origin/main, and leave any other stash to its owner")
-    fi
-    files="$({
-        git -C "${canon}" diff --name-only "${ref}" -- home install scripts 2> /dev/null || true
-        git -C "${canon}" diff --cached --name-only "${ref}" -- home install scripts 2> /dev/null || true
-        git -C "${canon}" ls-files --others --exclude-standard -- home install scripts 2> /dev/null || true
-    } | sort -u | paste -sd , -)"
-    if [[ -n ${files} ]]; then
-        violations+=("canonical clone ${canon} differs from ${ref} under home/, install/ or scripts/: ${files}; nothing but pull and apply runs in the canonical clone; restore a stray diff with git -C ${canon} restore -SW --source=${ref} -- <files> and drop its autostash")
-    else
-        # Bytes equal to the ref still leave a stale HEAD with a dirty tree
-        # once the same change merged upstream; only a pull makes the clone clean.
-        files="$({
-            git -C "${canon}" diff --name-only HEAD -- home install scripts 2> /dev/null || true
-            git -C "${canon}" diff --cached --name-only HEAD -- home install scripts 2> /dev/null || true
-        } | sort -u | paste -sd , -)"
-        if [[ -n ${files} ]]; then
-            violations+=("canonical clone ${canon} has uncommitted changes under home/, install/ or scripts/ that already match ${ref} while HEAD is behind it: ${files}; pull it (git -C ${canon} pull) so its autostash re-applies as a no-op")
-        fi
-    fi
+	src="$(chezmoi source-path 2> /dev/null)" &&
+	canon="$(git -C "${src}" rev-parse --show-toplevel 2> /dev/null)" &&
+	[[ "$(cd -- "${canon}" && pwd -P)" != "$(cd -- "${main}" && pwd -P)" ]]; then
+	ref=HEAD
+	if git -C "${canon}" rev-parse -q --verify origin/main > /dev/null 2>&1; then
+		ref=origin/main
+	fi
+	if [[ -n "$(git -C "${canon}" ls-files -u 2> /dev/null)" ]]; then
+		violations+=("canonical clone ${canon} has unmerged entries (git ls-files -u); finish or abort its pull")
+	fi
+	if [[ -n "$(git -C "${canon}" stash list 2> /dev/null)" ]]; then
+		violations+=("canonical clone ${canon} carries a stash (git stash list); drop only the autostash entry once its content is on origin/main, and leave any other stash to its owner")
+	fi
+	files="$({
+		git -C "${canon}" diff --name-only "${ref}" -- home install scripts 2> /dev/null || true
+		git -C "${canon}" diff --cached --name-only "${ref}" -- home install scripts 2> /dev/null || true
+		git -C "${canon}" ls-files --others --exclude-standard -- home install scripts 2> /dev/null || true
+	} | sort -u | paste -sd , -)"
+	if [[ -n ${files} ]]; then
+		violations+=("canonical clone ${canon} differs from ${ref} under home/, install/ or scripts/: ${files}; nothing but pull and apply runs in the canonical clone; restore a stray diff with git -C ${canon} restore -SW --source=${ref} -- <files> and drop its autostash")
+	else
+		# Bytes equal to the ref still leave a stale HEAD with a dirty tree
+		# once the same change merged upstream; only a pull makes the clone clean.
+		files="$({
+			git -C "${canon}" diff --name-only HEAD -- home install scripts 2> /dev/null || true
+			git -C "${canon}" diff --cached --name-only HEAD -- home install scripts 2> /dev/null || true
+		} | sort -u | paste -sd , -)"
+		if [[ -n ${files} ]]; then
+			violations+=("canonical clone ${canon} has uncommitted changes under home/, install/ or scripts/ that already match ${ref} while HEAD is behind it: ${files}; pull it (git -C ${canon} pull) so its autostash re-applies as a no-op")
+		fi
+	fi
 fi
 
 if command -v herdr > /dev/null 2>&1 && command -v jq > /dev/null 2>&1 &&
-    workspaces="$(herdr workspace list 2> /dev/null)"; then
-    # The label prefix alone also matches another clone with the same
-    # basename, so a workspace counts only when one of its panes has its cwd
-    # in this main checkout (the find_managed_workspaces rule in herdr-agents).
-    while IFS=$'\t' read -r workspace_id label; do
-        [[ -n ${workspace_id} ]] || continue
-        if herdr pane list --workspace "${workspace_id}" 2> /dev/null |
-            jq -e --arg main "${main}" '.result.panes[]? | (.cwd // "") | select(. == $main or startswith($main + "/"))' > /dev/null 2>&1; then
-            violations+=("additional worker workspace still open: ${label} (herdr-agents --remove-worker)")
-        fi
-    done < <(jq -r --arg prefix "$(basename -- "${main}") worker " \
-        '.result.workspaces[]? | select(.workspace_id and ((.label // "") | startswith($prefix))) | [.workspace_id, .label] | @tsv' <<< "${workspaces}" 2> /dev/null)
-    # herdr-agents --add-worker seats a worker in its own tab of the managed
-    # workspace (the one with a pane in the main checkout itself; attach mode
-    # keeps the workspace's own label): a pane there whose cwd is a linked
-    # worktree is a worker tab still open.
-    while IFS=$'\t' read -r workspace_id label; do
-        [[ -n ${workspace_id} ]] || continue
-        herdr pane list --workspace "${workspace_id}" 2> /dev/null |
-            jq -e --arg main "${main}" '.result.panes[]? | select(.cwd == $main)' > /dev/null 2>&1 || continue
-        while IFS= read -r pane_label; do
-            violations+=("additional worker tab still open in ${label}: ${pane_label} (herdr-agents --remove-worker)")
-        done < <(herdr pane list --workspace "${workspace_id}" 2> /dev/null |
-            jq -r --arg worktrees "${main}/.claude/worktrees/" \
-                '[.result.panes[]? | select((.cwd // "") | startswith($worktrees)) | (.label // .pane_id)] | unique[]' 2> /dev/null)
-    done < <(jq -r --arg prefix "$(basename -- "${main}") worker " \
-        '.result.workspaces[]? | select(.workspace_id and ((.label // "") | startswith($prefix) | not)) | [.workspace_id, (.label // "")] | @tsv' <<< "${workspaces}" 2> /dev/null)
+	workspaces="$(herdr workspace list 2> /dev/null)"; then
+	# The label prefix alone also matches another clone with the same
+	# basename, so a workspace counts only when one of its panes has its cwd
+	# in this main checkout (the find_managed_workspaces rule in herdr-agents).
+	while IFS=$'\t' read -r workspace_id label; do
+		[[ -n ${workspace_id} ]] || continue
+		if herdr pane list --workspace "${workspace_id}" 2> /dev/null |
+			jq -e --arg main "${main}" '.result.panes[]? | (.cwd // "") | select(. == $main or startswith($main + "/"))' > /dev/null 2>&1; then
+			violations+=("additional worker workspace still open: ${label} (herdr-agents --remove-worker)")
+		fi
+	done < <(jq -r --arg prefix "$(basename -- "${main}") worker " \
+		'.result.workspaces[]? | select(.workspace_id and ((.label // "") | startswith($prefix))) | [.workspace_id, .label] | @tsv' <<< "${workspaces}" 2> /dev/null)
+	# herdr-agents --add-worker seats a worker in its own tab of the managed
+	# workspace (the one with a pane in the main checkout itself; attach mode
+	# keeps the workspace's own label): a pane there whose cwd is a linked
+	# worktree is a worker tab still open.
+	while IFS=$'\t' read -r workspace_id label; do
+		[[ -n ${workspace_id} ]] || continue
+		herdr pane list --workspace "${workspace_id}" 2> /dev/null |
+			jq -e --arg main "${main}" '.result.panes[]? | select(.cwd == $main)' > /dev/null 2>&1 || continue
+		while IFS= read -r pane_label; do
+			violations+=("additional worker tab still open in ${label}: ${pane_label} (herdr-agents --remove-worker)")
+		done < <(herdr pane list --workspace "${workspace_id}" 2> /dev/null |
+			jq -r --arg worktrees "${main}/.claude/worktrees/" \
+				'[.result.panes[]? | select((.cwd // "") | startswith($worktrees)) | (.label // .pane_id)] | unique[]' 2> /dev/null)
+	done < <(jq -r --arg prefix "$(basename -- "${main}") worker " \
+		'.result.workspaces[]? | select(.workspace_id and ((.label // "") | startswith($prefix) | not)) | [.workspace_id, (.label // "")] | @tsv' <<< "${workspaces}" 2> /dev/null)
 fi
 
 while IFS= read -r warning; do
-    [[ -n ${warning} ]] && violations+=("${warning#WARN: }")
+	[[ -n ${warning} ]] && violations+=("${warning#WARN: }")
 done < <(
-    python3 - "${root}" "${main}" << 'PY' 2> /dev/null
+	python3 - "${root}" "${main}" << 'PY' 2> /dev/null
 import importlib.util
 import sys
 from pathlib import Path
@@ -271,7 +271,7 @@
 # @arg $2 string `reset_of` or `pr_less`.
 # @arg $3 string Task id, for `reset_of`.
 front_matter_says() {
-    local script='import sys, yaml
+	local script='import sys, yaml
 try:
     text = open(sys.argv[1], encoding="utf-8").read()
     data = yaml.safe_load(text.split("\n---\n", 1)[0][4:]) if text.startswith("---\n") else None
@@ -284,73 +284,73 @@
 else:
     yes = data.get("format") == 2 and data.get("kind") in ("review", "design")
 print("yes" if yes else "no")'
-    [[ "$(uv run --offline --no-project --quiet --with pyyaml python -c "${script}" "$@" < /dev/null 2> /dev/null ||
-        uv run --no-project --quiet --with pyyaml python -c "${script}" "$@" < /dev/null 2> /dev/null)" == yes ]]
+	[[ "$(uv run --offline --no-project --quiet --with pyyaml python -c "${script}" "$@" < /dev/null 2> /dev/null ||
+		uv run --no-project --quiet --with pyyaml python -c "${script}" "$@" < /dev/null 2> /dev/null)" == yes ]]
 }
 
 if task_ids="$("${counters}" --list-tasks 2> /dev/null)"; then
-    while read -r task _; do
-        # Ids come from agent-written history and become paths: one plain file name only.
-        [[ ${task} =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ && -f ${main}/.orchestration/tasks/${task}.md ]] || continue
-        accepted="${main}/.orchestration/acceptance/${task}.md"
-        reset="${main}/.orchestration/acceptance/${task}-design-reset.md"
-        args=("${task}")
-        if [[ -f ${reset} ]]; then
-            hash="$(sed -n 's/^design_sha256: *\([0-9a-f]\{64\}\) *$/\1/p' "${reset}" | head -n 1)"
-            redesign="$(sed -n 's/^redesign_task: *\([A-Za-z0-9][A-Za-z0-9._-]*\) *$/\1/p' "${reset}" | head -n 1)"
-            source_task="$(sed -n 's/^redesign_source: *\([A-Za-z0-9][A-Za-z0-9._-]*\) *$/\1/p' "${reset}" | head -n 1)"
-            design="${main}/.orchestration/tasks/${redesign}.md"
-            # The hash must be the named redesign task's own file, and that file must
-            # name this task in reset_of: an unrelated accepted design anchors nothing.
-            if [[ -n ${hash} && -n ${redesign} && -f ${design} ]] &&
-                [[ "$({ sha256sum "${design}" 2> /dev/null || shasum -a 256 "${design}"; } | cut -d ' ' -f 1)" == "${hash}" ]] &&
-                front_matter_says "${design}" reset_of "${task}"; then
-                args+=(--reset-hash "${hash}" --reset-source "${source_task}")
-            fi
-        fi
-        counts="$("${counters}" "${args[@]}" < /dev/null 2> /dev/null)" || continue
-        # The task's PR from its RESULTs: digits, `none` (no RESULT carries pr=) or `invalid`.
-        task_pr="$(sed -n 's/^detail: pr=\([^ ]*\) .*/\1/p' <<< "${counts}")"
-        pr=""
-        if [[ ${task_pr} =~ ^[0-9]+$ ]]; then
-            pr="${task_pr}"
-        fi
-        by="$(sed -n 's/^reset: .* accepted_by=\([^ ]*\) .*/\1/p' <<< "${counts}")"
-        state="" merged_at=""
-        if [[ -n ${pr} ]]; then
-            IFS=$'\t' read -r state merged_at < <(cd -- "${main}" && gh api "repos/{owner}/{repo}/pulls/${pr}" --jq '[.state, (.merged_at // "")] | @tsv' < /dev/null 2> /dev/null || true) || true
-        fi
-        record_pr=""
-        if [[ -f ${accepted} ]] && grep -Eiq '^(- )?\*\*decision:\*\* *accepted|^status: *accepted' "${accepted}"; then
-            record_pr="$(sed -nE 's/^(- )?pr=([0-9]+|none)([[:space:]].*)?$/\2/p' "${accepted}" | head -n 1)"
-        fi
-        reset_anchored=false silenced=false
-        if [[ -n ${by} && ${by} != none ]]; then
-            reset_anchored=true silenced=true
-        elif [[ -n ${pr} && -n ${merged_at} && ${record_pr} == "${pr}" ]]; then
-            silenced=true
-        elif [[ ${record_pr} == none && ${task_pr} == none ]] &&
-            front_matter_says "${main}/.orchestration/tasks/${task}.md" pr_less; then
-            silenced=true
-        fi
-        if [[ ${silenced} == false ]] && grep -q '^S2: ' <<< "${counts}"; then
-            while IFS= read -r line; do
-                violations+=("${task} ${line}")
-            done < <(grep '^S2: ' <<< "${counts}")
-        fi
-        if grep -qs 'DESIGN_RESET_WAIVED_BY=' "${accepted}" "${reset}"; then
-            violations+=("${task} waiver-unanchored")
-        fi
-        if [[ ${state} == closed && -z ${merged_at} && ${reset_anchored} == false ]]; then
-            violations+=("${task} PR #${pr} closed unmerged without an anchored reset record")
-        fi
-    done <<< "${task_ids}"
+	while read -r task _; do
+		# Ids come from agent-written history and become paths: one plain file name only.
+		[[ ${task} =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ && -f ${main}/.orchestration/tasks/${task}.md ]] || continue
+		accepted="${main}/.orchestration/acceptance/${task}.md"
+		reset="${main}/.orchestration/acceptance/${task}-design-reset.md"
+		args=("${task}")
+		if [[ -f ${reset} ]]; then
+			hash="$(sed -n 's/^design_sha256: *\([0-9a-f]\{64\}\) *$/\1/p' "${reset}" | head -n 1)"
+			redesign="$(sed -n 's/^redesign_task: *\([A-Za-z0-9][A-Za-z0-9._-]*\) *$/\1/p' "${reset}" | head -n 1)"
+			source_task="$(sed -n 's/^redesign_source: *\([A-Za-z0-9][A-Za-z0-9._-]*\) *$/\1/p' "${reset}" | head -n 1)"
+			design="${main}/.orchestration/tasks/${redesign}.md"
+			# The hash must be the named redesign task's own file, and that file must
+			# name this task in reset_of: an unrelated accepted design anchors nothing.
+			if [[ -n ${hash} && -n ${redesign} && -f ${design} ]] &&
+				[[ "$({ sha256sum "${design}" 2> /dev/null || shasum -a 256 "${design}"; } | cut -d ' ' -f 1)" == "${hash}" ]] &&
+				front_matter_says "${design}" reset_of "${task}"; then
+				args+=(--reset-hash "${hash}" --reset-source "${source_task}")
+			fi
+		fi
+		counts="$("${counters}" "${args[@]}" < /dev/null 2> /dev/null)" || continue
+		# The task's PR from its RESULTs: digits, `none` (no RESULT carries pr=) or `invalid`.
+		task_pr="$(sed -n 's/^detail: pr=\([^ ]*\) .*/\1/p' <<< "${counts}")"
+		pr=""
+		if [[ ${task_pr} =~ ^[0-9]+$ ]]; then
+			pr="${task_pr}"
+		fi
+		by="$(sed -n 's/^reset: .* accepted_by=\([^ ]*\) .*/\1/p' <<< "${counts}")"
+		state="" merged_at=""
+		if [[ -n ${pr} ]]; then
+			IFS=$'\t' read -r state merged_at < <(cd -- "${main}" && gh api "repos/{owner}/{repo}/pulls/${pr}" --jq '[.state, (.merged_at // "")] | @tsv' < /dev/null 2> /dev/null || true) || true
+		fi
+		record_pr=""
+		if [[ -f ${accepted} ]] && grep -Eiq '^(- )?\*\*decision:\*\* *accepted|^status: *accepted' "${accepted}"; then
+			record_pr="$(sed -nE 's/^(- )?pr=([0-9]+|none)([[:space:]].*)?$/\2/p' "${accepted}" | head -n 1)"
+		fi
+		reset_anchored=false silenced=false
+		if [[ -n ${by} && ${by} != none ]]; then
+			reset_anchored=true silenced=true
+		elif [[ -n ${pr} && -n ${merged_at} && ${record_pr} == "${pr}" ]]; then
+			silenced=true
+		elif [[ ${record_pr} == none && ${task_pr} == none ]] &&
+			front_matter_says "${main}/.orchestration/tasks/${task}.md" pr_less; then
+			silenced=true
+		fi
+		if [[ ${silenced} == false ]] && grep -q '^S2: ' <<< "${counts}"; then
+			while IFS= read -r line; do
+				violations+=("${task} ${line}")
+			done < <(grep '^S2: ' <<< "${counts}")
+		fi
+		if grep -qs 'DESIGN_RESET_WAIVED_BY=' "${accepted}" "${reset}"; then
+			violations+=("${task} waiver-unanchored")
+		fi
+		if [[ ${state} == closed && -z ${merged_at} && ${reset_anchored} == false ]]; then
+			violations+=("${task} PR #${pr} closed unmerged without an anchored reset record")
+		fi
+	done <<< "${task_ids}"
 fi
 
 for violation in ${violations[@]+"${violations[@]}"}; do
-    printf 'regime-boundary: %s\n' "${violation}"
+	printf 'regime-boundary: %s\n' "${violation}"
 done
 if [[ ${report} == false && ${#violations[@]} -gt 0 ]]; then
-    exit 1
+	exit 1
 fi
 exit 0
```

Correct configured checks:
```text
$ shellcheck scripts/orchestrator/seat-args.sh scripts/check-regime-boundary.sh
exit=0; stdout/stderr empty
$ shfmt --indent 4 --space-redirects --diff scripts/orchestrator/seat-args.sh scripts/check-regime-boundary.sh
exit=0; stdout/stderr empty
$ UV_CACHE_DIR=/tmp/codex-worker-e-uv-cache uv run --no-project ruff format --check tests/unit/test_seat_args.py tests/unit/test_check_regime_boundary.py
2 files already formatted
exit=0
$ git diff --check
exit=0; stdout/stderr empty
```

Final locally-tested source bytes:
```text
5b4b6d28a63945d101750ec8c90963f3ee534ab189bd5086b4781520e5257625  scripts/orchestrator/seat-args.sh
eb242b6e7f3ebcdeca2946993324f4012474e30ec85fdf6b418447764123d423  scripts/check-regime-boundary.sh
74ff7e8c1a969a994d181234d1edc8e94502d908a17320408c200b37ebb201a2  tests/unit/test_seat_args.py
27d86374f82d7f0d069e4896173ff311725dda83b041e4a56d6285246938dfb3  tests/unit/test_check_regime_boundary.py
148f5dde8795da8a8eeb265fcbbd40be11cb27e2407c979b772dcbcba772bd8f  .orchestration/dotfiles-T128-seat-launch-args-a01/task.md
```

## Independent C50 review transcript

Source hashes matched the locally-tested files. Transcript SHA256 d61a817387b6966b27b4a10c8f6ff10527b32227482e26c2fc3ff6443184709a. Parent read the complete transcript before resolving the JSON and receipt.

# Seat launch arguments C50 independent review

Review base: 274257172db0915df34e9f1764c69f572346727f.

Scope: the profile-character-class change in scripts/orchestrator/seat-args.sh and its added underscore-profile subtest in tests/unit/test_seat_args.py. Generator grammar and launcher identity formation were read as connected context. No repository files or refs were changed. No live ps/lsof, browser/server or full test suite was run.

## Conclusion

Review-scope approval, high confidence. Bot P2 4301264676, class profile-name-grammar, is addressed: the profile capture now uses the generator's [a-z][a-z0-9_]* grammar; the launcher preserves the profile in kind-profile-suffix-aNNN identities; the existing key normalization produces MODEL_PROFILE_MY_PROFILE_<KIND>_ARGS. The new subtest exercises the reported valid Claude identity. Additional isolated stub cases confirm both Claude and Codex accept my_profile while a leading underscore remains invalid. No additional finding.

## Reviewed source SHA256

- scripts/orchestrator/seat-args.sh: 5b4b6d28a63945d101750ec8c90963f3ee534ab189bd5086b4781520e5257625
- tests/unit/test_seat_args.py: 74ff7e8c1a969a994d181234d1edc8e94502d908a17320408c200b37ebb201a2

## Exact command/output transcript

The execution tool exposes combined stdout/stderr for each outer command. That displayed output is copied verbatim below with its recorded exit status. The additional probe explicitly captures and prints each inner subprocess's stdout, stderr and exit status as JSON; all three inner stderr strings were empty.

### Delta, caller search and source hashes

~~~bash
git diff 274257172db0915df34e9f1764c69f572346727f -- scripts/orchestrator/seat-args.sh tests/unit/test_seat_args.py && rg -n 'PROFILE_NAME_RE|worker_name=|worker_name\(|identity=|seat_name=|WORKER_PROFILE.*name|WORKER_PROFILE.*worker|kind.*profile|profile.*kind' scripts/generate-agent-configs.py home/dot_local/bin/common/executable_herdr-agents && shasum -a 256 scripts/orchestrator/seat-args.sh tests/unit/test_seat_args.py
~~~

Verbatim displayed output:

~~~text
diff --git a/scripts/orchestrator/seat-args.sh b/scripts/orchestrator/seat-args.sh
index 522edb79..7cd98297 100755
--- a/scripts/orchestrator/seat-args.sh
+++ b/scripts/orchestrator/seat-args.sh
@@ -15,7 +15,7 @@
 set -euo pipefail
 
 teams=$1 identity=$2 agent_type=$3 project=$4
-if [[ ! ${identity} =~ ^(claude|codex)-([a-z][a-z0-9]*)-[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
+if [[ ! ${identity} =~ ^(claude|codex)-([a-z][a-z0-9_]*)-[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
     printf 'seat %s args=unknown-identity\n' "${identity}"
     exit 2
 fi
diff --git a/tests/unit/test_seat_args.py b/tests/unit/test_seat_args.py
index ca613174..c799acc3 100644
--- a/tests/unit/test_seat_args.py
+++ b/tests/unit/test_seat_args.py
@@ -103,6 +103,13 @@ class SeatArgsTest(unittest.TestCase):
                 runtime = "claude" if kind == "claude-code" else "codex"
                 self.assertEqual(f"seat {identity} profile=standard kind={runtime} {tail}\n", result.stdout)
 
+        with self.subTest(label="underscore profile"):
+            identity = "claude-my_profile-dot-a001"
+            self.profiles.write_text(f'MODEL_PROFILE_MY_PROFILE_CLAUDE_ARGS="{CLAUDE_ARGS}"\n')
+            result = self.run_probe(identity, "claude-code", "t", project, f"200 {match.replace(claude, identity)}\n")
+            self.assertEqual(0, result.returncode, result.stderr)
+            self.assertEqual(f"seat {identity} profile=my_profile kind=claude process=200 args=ok\n", result.stdout)
+
         for label, identity, kind, profile_text, seam, expected in [
             (
                 "missing key",
scripts/generate-agent-configs.py:77:PROFILE_NAME_RE = re.compile(r"^[a-z][a-z0-9_]*$")
scripts/generate-agent-configs.py:101:        if not PROFILE_NAME_RE.match(str(name)):
scripts/generate-agent-configs.py:1273:        lines.append(f'HERDR_AGENTS_WORKER_PROFILE="{profile_name}"')
home/dot_local/bin/common/executable_herdr-agents:60:#   to `worker_kind` from the manifest via ~/.agents/model-profiles.env, then
home/dot_local/bin/common/executable_herdr-agents:62:# @arg HERDR_AGENTS_WORKER_PROFILE Environment variable naming the worker's
home/dot_local/bin/common/executable_herdr-agents:91:       herdr-agents --add-worker [<worktree>] [--kind codex|claude] [--profile NAME] [--ready-timeout SECONDS] [DIR]
home/dot_local/bin/common/executable_herdr-agents:142:worker_kind from ~/.agents/model-profiles.env, then codex) and --kind select
home/dot_local/bin/common/executable_herdr-agents:283:#   there is reused. A new one is <kind>-<profile>-<suffix>-aNNN (next free NNN)
home/dot_local/bin/common/executable_herdr-agents:463:    profile_env_key="MODEL_PROFILE_$(printf '%s' "${HERDR_AGENTS_WORKER_PROFILE}" | tr '[:lower:]' '[:upper:]')_$(printf '%s' "${kind}" | tr '[:lower:]' '[:upper:]')_ARGS"
home/dot_local/bin/common/executable_herdr-agents:473:    [[ ${kind} == claude ]] || args="--profile ${HERDR_AGENTS_WORKER_PROFILE} --sandbox workspace-write --ask-for-approval never --config sandbox_workspace_write.network_access=true"
home/dot_local/bin/common/executable_herdr-agents:613:    identity="$(AGMSG_RESOLVE_PROJECT=0 "${scripts}/identities.sh" "${workdir}" claude-code 2> /dev/null |
home/dot_local/bin/common/executable_herdr-agents:614:        awk -F '\t' '$2 !~ /-a[0-9][0-9][0-9]$/ { print $2 }' | sort -u)" || identity=""
home/dot_local/bin/common/executable_herdr-agents:694:    identity="$(AGMSG_RESOLVE_PROJECT=0 "${identities}" "${workdir}" "${type}" 2> /dev/null |
home/dot_local/bin/common/executable_herdr-agents:695:        awk -F '\t' '$2 !~ /-a[0-9][0-9][0-9]$/ { print $2 }' | sort -u)" || identity=""
home/dot_local/bin/common/executable_herdr-agents:1585:    printf 'herdr-agents: --restart-worker is retired; run herdr-agents --remove-worker <worktree> and then herdr-agents --add-worker <worktree> [--kind …] [--profile NAME]\n' >&2
home/dot_local/bin/common/executable_herdr-agents:1681:    while [[ ${1:-} == "--kind" || ${1:-} == "--profile" || ${1:-} == "--ready-timeout" || ${1:-} == "--force" || ${1:-} == "--stale" ]]; do
home/dot_local/bin/common/executable_herdr-agents:1683:        --kind | --profile | --ready-timeout)
home/dot_local/bin/common/executable_herdr-agents:1817:    HERDR_AGENTS_WORKER_PROFILE="${seat_profile:-$(resolve_worker_profile)}"
home/dot_local/bin/common/executable_herdr-agents:1833:    seat_identity="$(ensure_worker_identity "${seat_kind}" "${workdir}" "${seat_dir}" --no-join)"
home/dot_local/bin/common/executable_herdr-agents:1835:    seat_name="${seat_identity#*$'\t'}"
5b4b6d28a63945d101750ec8c90963f3ee534ab189bd5086b4781520e5257625  scripts/orchestrator/seat-args.sh
74ff7e8c1a969a994d181234d1edc8e94502d908a17320408c200b37ebb201a2  tests/unit/test_seat_args.py
~~~

Exit status: 0. Tool chunk: d4194d.

### Generator grammar, identity formation and scope

~~~bash
sed -n '72,108p' scripts/generate-agent-configs.py && sed -n '278,348p' home/dot_local/bin/common/executable_herdr-agents && sed -n '1262,1285p' scripts/generate-agent-configs.py && sed -n '17,38p' scripts/orchestrator/seat-args.sh && git diff --name-only 274257172db0915df34e9f1764c69f572346727f -- scripts tests
~~~

Verbatim displayed output:

~~~text

def enabled_for(server: dict[str, Any], agent: str) -> bool:
    return bool(server.get("agents", {}).get(agent, False))


PROFILE_NAME_RE = re.compile(r"^[a-z][a-z0-9_]*$")
PROFILE_VALUE_RE = re.compile(r"^[A-Za-z0-9._\[\]-]+$")
PROFILE_AGENT_KEYS = {
    "claude": ("model", "effort"),
    "codex": ("model", "model_reasoning_effort"),
}
PROFILE_OPTIONAL_KEYS = {"claude": ("advisor",)}
CODEX_SANDBOX_MODES = ("read-only", "workspace-write", "danger-full-access")
RUNTIME_PREFIXES = (
    "hooks.state",
    "marketplaces",
    "tui.model_availability_nux",
    "projects",
)


def model_profiles(manifest: dict[str, Any]) -> dict[str, Any]:
    profiles = manifest.get("model_profiles")
    if not isinstance(profiles, dict) or not profiles:
        fail("model_profiles must be a non-empty mapping")
    for required in ("express", "standard"):
        if required not in profiles:
            fail(f"model_profiles must define the {required} profile")
    for name, profile in profiles.items():
        if not PROFILE_NAME_RE.match(str(name)):
            fail(f"model profile name is not launcher-safe: {name}")
        if not isinstance(profile, dict):
            fail(f"model profile {name} must be a mapping")
        for agent, keys in PROFILE_AGENT_KEYS.items():
            mapping = profile.get(agent)
            if not isinstance(mapping, dict):
                fail(f"model profile {name} is missing {agent}")
    printf '%s\n' "${path}"
}

# @description Print `<team><TAB><name>` of the agmsg identity seated at a worker
#   worktree, registering one when none exists. An existing single registration
#   there is reused. A new one is <kind>-<profile>-<suffix>-aNNN (next free NNN)
#   in the orchestrator's team, where team and suffix come from the
#   orchestrator's one non-worker (no -aNNN) claude-code identity at the main
#   checkout; it is joined with AGMSG_RESOLVE_PROJECT=0 so upstream project
#   resolution (#92) cannot rewrite the worktree path to the main checkout,
#   unless $4 is `--no-join` (spawn.sh joins it itself).
# @arg $1 string Worker kind.
# @arg $2 workdir Absolute main checkout path.
# @arg $3 path Absolute worker worktree path.
# @arg $4 string Optional `--no-join` to only derive the identity.
# @exitcode 2 If the worktree or orchestrator registration is ambiguous.
function ensure_worker_identity() {
    local kind="$1"
    local workdir="$2"
    local worktree="$3"
    local join="${4:-}"
    local scripts="${HOME}/.agents/skills/agmsg/scripts"
    local agent_type seated orchestrator team suffix name next

    agent_type="$(worker_agmsg_type "${kind}")"
    if [[ ! -x ${scripts}/identities.sh || ! -x ${scripts}/join.sh ]]; then
        printf 'agmsg scripts not found; skipping worker identity registration: %s\n' "${scripts}" >&2
        return 0
    fi
    seated="$(AGMSG_RESOLVE_PROJECT=0 "${scripts}/identities.sh" "${worktree}" "${agent_type}" 2> /dev/null | sort -u)" || seated=""
    # One name in several teams is one seat (distinct names decide, as in
    # distinct_agmsg_identity_count).
    if [[ "$(cut -f 2 <<< "${seated}" | sort -u | grep -c .)" -gt 1 ]]; then
        printf 'herdr-agents: several agmsg %s identities are registered at %s (%s); refusing to pick one.\n' "${agent_type}" "${worktree}" "$(cut -f 2 <<< "${seated}" | sort -u | tr '\n' ' ' | sed 's/ $//')" >&2
        exit 2
    fi
    if [[ -n ${seated} ]]; then
        head -n 1 <<< "${seated}"
        return 0
    fi
    orchestrator="$(AGMSG_RESOLVE_PROJECT=0 "${scripts}/identities.sh" "${workdir}" "${orchestrator_agmsg_type}" 2> /dev/null |
        awk -F '\t' '$2 !~ /-a[0-9][0-9][0-9]$/' | sort -u)" || orchestrator=""
    if [[ -z ${orchestrator} || ${orchestrator} == *$'\n'* ]]; then
        printf 'herdr-agents: need exactly one orchestrator %s identity at %s to name the worker; register the worker yourself with: AGMSG_RESOLVE_PROJECT=0 %s/join.sh <team> <name> %s %q\n' \
            "${orchestrator_agmsg_type}" "${workdir}" "${scripts}" "${agent_type}" "${worktree}" >&2
        exit 2
    fi
    team="${orchestrator%%$'\t'*}"
    suffix="${orchestrator##*-}"
    next="$(AGMSG_RESOLVE_PROJECT=0 "${scripts}/team.sh" "${team}" --json 2> /dev/null |
        jq -r '.[]?.member // empty' | sed -n 's/.*-a\([0-9][0-9][0-9]\)$/\1/p' | sort -n | tail -n 1)" || next=""
    printf -v name '%s-%s-%s-a%03d' "${kind}" "${HERDR_AGENTS_WORKER_PROFILE}" "${suffix}" "$((10#${next:-0} + 1))"
    if [[ ${join} != --no-join ]]; then
        AGMSG_RESOLVE_PROJECT=0 "${scripts}/join.sh" "${team}" "${name}" "${agent_type}" "${worktree}" > /dev/null
    fi
    printf '%s\t%s\n' "${team}" "${name}"
}

# @description Point agmsg delivery at the worker worktree when its hook is
#   missing: `both` for claude-code (turn delivery; upstream session-start.sh
#   skips sessions under .claude/worktrees, #367, so no Monitor watch starts
#   there), `turn` for codex. delivery.sh bakes the path into the hook.
# @arg $1 string Worker kind.
# @arg $2 path Absolute worker worktree path.
function ensure_worker_delivery() {
    local kind="$1"
    local worktree="$2"
    local delivery="${HOME}/.agents/skills/agmsg/scripts/delivery.sh"
    local log_file="${HOME}/.config/herdr/herdr-agents.log"

    [[ -x ${delivery} ]] || return 0
def render_model_profiles_env(manifest: dict[str, Any]) -> str:
    profiles = model_profiles(manifest)
    interactive_profile(manifest)
    lines = [
        "# Shell fragment sourced by agent launchers (herdr-agents).",
        f"# {GENERATED_HEADER}",
        f'MODEL_PROFILE_INTERACTIVE="{manifest["interactive_profile"]}"',
        f'HERDR_AGENTS_WORKER_KIND="{worker_kind(manifest)}"',
        f'HERDR_AGENTS_ORCHESTRATOR_KIND="{orchestrator_kind(manifest)}"',
    ]
    if (profile_name := worker_profile(manifest)) is not None:
        lines.append(f'HERDR_AGENTS_WORKER_PROFILE="{profile_name}"')
    if (worktree := worker_worktree(manifest)) is not None:
        lines.append(f'HERDR_AGENTS_WORKER_WORKTREE="{worktree}"')
    for name, profile in sorted(profiles.items()):
        var = str(name).upper()
        claude = profile["claude"]
        claude_args = f"--model {claude['model']} --effort {claude['effort']}"
        if "advisor" in claude:
            claude_args += f" --advisor {claude['advisor']}"
        lines.append(f'MODEL_PROFILE_{var}_CLAUDE_ARGS="{claude_args}"')
        lines.append(f'MODEL_PROFILE_{var}_CODEX_ARGS="--profile {name}"')
    return "\n".join(lines) + "\n"

teams=$1 identity=$2 agent_type=$3 project=$4
if [[ ! ${identity} =~ ^(claude|codex)-([a-z][a-z0-9_]*)-[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
    printf 'seat %s args=unknown-identity\n' "${identity}"
    exit 2
fi
kind=${BASH_REMATCH[1]} profile=${BASH_REMATCH[2]}
if [[ ${kind}:${agent_type} != claude:claude-code && ${kind}:${agent_type} != codex:codex ]]; then
    printf 'seat %s args=unknown-identity\n' "${identity}"
    exit 2
fi
label="seat ${identity} profile=${profile} kind=${kind}"
key="MODEL_PROFILE_$(tr '[:lower:]' '[:upper:]' <<< "${profile}_${kind}")_ARGS"
expected="$(awk -v key="${key}" 'index($0, key "=\"") == 1 && substr($0, length($0), 1) == "\"" {
    print substr($0, length(key) + 3, length($0) - length(key) - 3); exit
}' "${HOME}/.agents/model-profiles.env" 2> /dev/null)" || expected=""
if [[ -z ${expected} ]]; then
    printf '%s args=unknown-profile\n' "${label}"
    exit 2
fi
[[ ${kind} != codex ]] || expected="--profile ${profile}"
read -r -a expected_args <<< "${expected}"
IFS=, read -r -a team_names <<< "${teams}"
scripts/orchestrator/seat-args.sh
tests/unit/test_seat_args.py
~~~

Exit status: 0. Tool chunk: cca7a4.

### Additional stub-only behavior check

~~~bash
PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/tmp/codex-worker-e-uv-cache uv run --no-project python - <<'PY'
import importlib.util
import json
from pathlib import Path

spec = importlib.util.spec_from_file_location('seat_c50_fixture', Path('tests/unit/test_seat_args.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
case = module.SeatArgsTest()
case.setUp()
project = str(case.temp / 'project with spaces')
case.profiles.write_text(
    f'MODEL_PROFILE_MY_PROFILE_CLAUDE_ARGS="{module.CLAUDE_ARGS}"\n'
    'MODEL_PROFILE_MY_PROFILE_CODEX_ARGS="--profile my_profile"\n'
)
try:
    cases = [
        ('claude underscore profile', 'claude-my_profile-dot-a001', 'claude-code',
         f'200 claude {module.CLAUDE_ARGS} -n t-claude-my_profile-dot-a001\n', 0,
         'seat claude-my_profile-dot-a001 profile=my_profile kind=claude process=200 args=ok\n'),
        ('codex underscore profile', 'codex-my_profile-dot-a004', 'codex',
         '20 codex --profile my_profile\n', 0,
         'seat codex-my_profile-dot-a004 profile=my_profile kind=codex process=20 args=ok\n'),
        ('leading underscore still rejected', 'claude-_my_profile-dot-a001', 'claude-code', '', 2,
         'seat claude-_my_profile-dot-a001 args=unknown-identity\n'),
    ]
    for label, identity, kind, lines, code, expected_stdout in cases:
        result = case.run_probe(identity, kind, 't', project, lines)
        assert (result.returncode, result.stdout, result.stderr) == (code, expected_stdout, ''), (label, result)
        print(json.dumps({'case': label, 'exit': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr}))
    print('3 C50 stub-only cases passed')
finally:
    case.doCleanups()
PY
~~~

Verbatim displayed output:

~~~text
{"case": "claude underscore profile", "exit": 0, "stdout": "seat claude-my_profile-dot-a001 profile=my_profile kind=claude process=200 args=ok\n", "stderr": ""}
{"case": "codex underscore profile", "exit": 0, "stdout": "seat codex-my_profile-dot-a004 profile=my_profile kind=codex process=20 args=ok\n", "stderr": ""}
{"case": "leading underscore still rejected", "exit": 2, "stdout": "seat claude-_my_profile-dot-a001 args=unknown-identity\n", "stderr": ""}
3 C50 stub-only cases passed
~~~

Exit status: 0. Tool chunk: 016c6b.

Not checked: live process behavior, CI and the concurrently running full two-module suite. This review covers only the authorized C50 delta.

Verdict: correct


## C50 worker gate and source/test cap snapshot

```text
$ AGENT_REVIEWED=1 REVIEW_EVIDENCE=.orchestration/dotfiles-T128-seat-launch-args-a01/seat-args-worker-review-receipt.md make require-crit-review
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.
exit=0
$ git diff --numstat b167fe0a76a2e77d262f9f556c69ba6b9f118bbe -- scripts/orchestrator/seat-args.sh scripts/check-regime-boundary.sh tests/unit/test_seat_args.py tests/unit/test_check_regime_boundary.py
17	1	scripts/check-regime-boundary.sh
102	0	scripts/orchestrator/seat-args.sh
56	0	tests/unit/test_check_regime_boundary.py
182	0	tests/unit/test_seat_args.py
exit=0
Source changed120<=200; test added238<=1000; source/test bytes remain as reviewed.
```

## C50 artifact masking

```text
$ UV_CACHE_DIR=/tmp/codex-worker-e-uv-cache uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets <eight C50 canonical files excluding immutable task.md>
masked 0 match(es) in .orchestration/dotfiles-T128-seat-launch-args-a01/report.md
masked 0 match(es) in .orchestration/dotfiles-T128-seat-launch-args-a01/validation.md
masked 0 match(es) in .orchestration/dotfiles-T128-seat-launch-args-a01/sandbox.md
masked 0 match(es) in .orchestration/dotfiles-T128-seat-launch-args-a01/learning.md
masked 0 match(es) in .orchestration/dotfiles-T128-seat-launch-args-a01/autoskill.md
masked 0 match(es) in .orchestration/dotfiles-T128-seat-launch-args-a01/seat-args-worker-crit.json
masked 0 match(es) in .orchestration/dotfiles-T128-seat-launch-args-a01/seat-args-worker-review-receipt.md
masked 0 match(es) in .orchestration/dotfiles-T128-seat-launch-args-a01/revise.yaml
exit=0
```

All-path git diff --check exits2 solely on the verbatim unittest and formatter diff whitespace copied above. The transcript is preserved; the production/test paths pass the scoped check.

```text
$ git diff --check
.orchestration/dotfiles-T128-seat-launch-args-a01/validation.md:684: trailing whitespace.
+test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) ... 
.orchestration/dotfiles-T128-seat-launch-args-a01/validation.md:694: trailing whitespace.
+AssertionError: 0 != 2 : 
.orchestration/dotfiles-T128-seat-launch-args-a01/validation.md:733: trailing whitespace.
+ 
.orchestration/dotfiles-T128-seat-launch-args-a01/validation.md:770: trailing whitespace.
+ 
.orchestration/dotfiles-T128-seat-launch-args-a01/validation.md:787: trailing whitespace.
+ 
.orchestration/dotfiles-T128-seat-launch-args-a01/validation.md:835: trailing whitespace.
+ 
.orchestration/dotfiles-T128-seat-launch-args-a01/validation.md:865: trailing whitespace.
+ 
.orchestration/dotfiles-T128-seat-launch-args-a01/validation.md:883: trailing whitespace.
+ 
.orchestration/dotfiles-T128-seat-launch-args-a01/validation.md:890: trailing whitespace.
+ 
.orchestration/dotfiles-T128-seat-launch-args-a01/validation.md:899: trailing whitespace.
+ 
.orchestration/dotfiles-T128-seat-launch-args-a01/validation.md:908: trailing whitespace.
+ 
.orchestration/dotfiles-T128-seat-launch-args-a01/validation.md:934: trailing whitespace.
+ 
.orchestration/dotfiles-T128-seat-launch-args-a01/validation.md:1060: trailing whitespace.
+ 
.orchestration/dotfiles-T128-seat-launch-args-a01/validation.md:1065: trailing whitespace.
+ 
.orchestration/dotfiles-T128-seat-launch-args-a01/validation.md:1134: trailing whitespace.
+ 
.orchestration/dotfiles-T128-seat-launch-args-a01/validation.md:1191: trailing whitespace.
+ 
.orchestration/dotfiles-T128-seat-launch-args-a01/validation.md:1219: trailing whitespace.
+ 
.orchestration/dotfiles-T128-seat-launch-args-a01/validation.md:1334: trailing whitespace.
+ 
.orchestration/dotfiles-T128-seat-launch-args-a01/validation.md:1406: trailing whitespace.
+ 
.orchestration/dotfiles-T128-seat-launch-args-a01/validation.md:1420: trailing whitespace.
+ 
exit=2
$ git diff --check -- scripts/orchestrator/seat-args.sh scripts/check-regime-boundary.sh tests/unit/test_seat_args.py tests/unit/test_check_regime_boundary.py
stdout/stderr empty; exit=0
```

## Second C50: process-visibility4301301556

Authorized ACCEPTANCE2026-10-17T04:15:41Z on previous_headbfae75c14f52ff1b8083a69179bd90e91aa99458, class process-visibility occurrence1, exact test selector unchanged. Failed ps or no numeric process line skips4; failed/empty lsof skips4. Stderr one diagnostic, no host process command. A nonempty sandbox namespace hiding the host remains indistinguishable from real absence; no host-visibility claim.

### Prior exact-head Bot review and finding

```text
{
  "head": "bfae75c14f52ff1b8083a69179bd90e91aa99458",
  "reviews": [
    {
      "body": "<!-- codex-review-receipt:v1 -->\n\n\n### \ud83d\udca1 Codex Review\n\nHere are some automated review suggestions for this pull request.\n\n**Reviewed commit:** `bfae75c14f`\n    \n\n<details> <summary>\u2139\ufe0f About Codex in GitHub</summary>\n<br/>\n\nCodex has been enabled to automatically review pull requests in this repo. Reviews are triggered when you\n- Open a pull request for review\n- Mark a draft as ready\n- Comment \"@codex review\".\n\nIf Codex has suggestions, it will comment; otherwise it will react with \ud83d\udc4d.\n\n\n\n\nWhen you [sign up for Codex through ChatGPT](https://openai.com/codex), Codex can also answer questions or update the PR, like \"@codex address that feedback\".\n            \n</details>",
      "commit_id": "bfae75c14f52ff1b8083a69179bd90e91aa99458",
      "html_url": "https://github.com/mryfmo/dotfiles/pull/383#pullrequestreview-5556073590",
      "id": 5556073590,
      "state": "COMMENTED",
      "submitted_at": "2026-10-17T04:13:09Z"
    }
  ],
  "inline": [
    {
      "body": "**<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Run the process probe outside the agent sandbox**\n\nWhen this boundary check runs from the normal Claude orchestrator context, this subprocess inherits the agent sandbox: `home/dot_agents/skills/agmsg-orchestration/SKILL.md:56` documents that macOS Seatbelt denies `ps` and Linux bubblewrap hides outside processes. Consequently, `seat-args.sh` receives no visible worker rows and reports a healthy seat as `process=none args=unlaunched`; an executable-but-denied `ps` also reproduces this because its failure is discarded by the process substitution. Invoke the probe through an established outside-sandbox mechanism or another process source visible from the sandbox. The process-input threat-table row only describes the probes as read-only/test-replaceable and therefore does not mitigate this runtime limitation.\n\nAGENTS.md reference: [AGENTS.md:L75-L78](https://github.com/mryfmo/dotfiles/blob/bfae75c14f52ff1b8083a69179bd90e91aa99458/AGENTS.md#L75-L78)\n\nUseful? React with \ud83d\udc4d\u00a0/ \ud83d\udc4e.\n\n<!-- codex-code-review-finding:v1 -->",
      "html_url": "https://github.com/mryfmo/dotfiles/pull/383#discussion_r4301301556",
      "id": 4301301556,
      "line": 132,
      "original_commit_id": "bfae75c14f52ff1b8083a69179bd90e91aa99458",
      "path": "scripts/check-regime-boundary.sh"
    }
  ],
  "issue_comments": [
    {
      "body": "<!-- codex-pull-request-review-summary -->\n<!-- codex-review-state:v1 {\"code_review\":{\"commit_sha\":\"bfae75c14f52ff1b8083a69179bd90e91aa99458\",\"has_any_findings\":true,\"has_unresolved_findings\":true,\"status\":\"completed\"},\"security_review\":{\"commit_sha\":\"274257172db0915df34e9f1764c69f572346727f\",\"has_any_findings\":false,\"has_unresolved_findings\":false,\"status\":\"completed\"}} -->\n<!-- codex-security-review:v1 {\"blockingSeverityThreshold\":\"P0\",\"headSha\":\"274257172db0915df34e9f1764c69f572346727f\",\"mergeGateEnabled\":false,\"pullRequestNumber\":383,\"repository\":\"mryfmo/dotfiles\",\"status\":\"completed\"} -->\n## Codex Review Summary\n\nThis comment shows the latest Codex review activity on this pull request.\n\n| Review | Status | Commit | Review trigger |\n| --- | --- | --- | --- |\n| \ud83d\udcdd **Code Review** | \u2705 **Completed** <relative-time datetime=\"2026-10-17T04:13:12.249447Z\">2026-10-17T04:13:12.249447Z</relative-time> | `bfae75c` | Manual request |\n| \ud83d\udd12 **Security Review** | \u2705 **Completed** <relative-time datetime=\"2026-10-17T04:05:25.814777Z\">2026-10-17T04:05:25.814777Z</relative-time> | `2742571` | Draft marked ready |\n\n\n\n<details> <summary>\u2139\ufe0f About Codex in GitHub</summary>\n<br/>\n\n[Your team has set up Codex to review pull requests in this repo](https://chatgpt.com/codex/cloud/settings/general). Reviews are triggered when you\n- Open a pull request for review\n- Mark a draft as ready\n- Comment \"@codex review\" or \"@codex security review\".\n\nCodex reacts with \ud83d\udc40 while any review is running, comments if it has suggestions, and reacts with \ud83d\udc4d once all reviews finish with no findings.\n\n</details>",
      "created_at": "2026-10-17T04:00:57Z",
      "html_url": "https://github.com/mryfmo/dotfiles/pull/383#issuecomment-6229380503",
      "id": 6229380503,
      "updated_at": "2026-10-17T04:13:13Z"
    }
  ]
}

```

### Stub reproduction on prior source

```text
{"executable_stub_ps_exit": 1, "script_exit": 3, "stdout": "seat claude-standard-dot-a001 profile=standard kind=claude process=none args=unlaunched\n", "stderr": ""}
Reproduced: executable-but-failing ps is indistinguishable from an absent process. Stub only; no live process probe.

```

### RED prescribed seat method before second C50, exit1 expected

```text
test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) ... 
  test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (probe='ps', exit=1) ... FAIL
  test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (probe='ps', exit=0) ... FAIL
  test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (probe='lsof', exit=1) ... FAIL
  test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (probe='lsof', exit=0) ... FAIL

======================================================================
FAIL: test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (probe='ps', exit=1)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_seat_args.py", line 175, in test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one
    self.assertEqual(4, result.returncode)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 4 != 3

======================================================================
FAIL: test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (probe='ps', exit=0)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_seat_args.py", line 175, in test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one
    self.assertEqual(4, result.returncode)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 4 != 3

======================================================================
FAIL: test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (probe='lsof', exit=1)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_seat_args.py", line 175, in test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one
    self.assertEqual(4, result.returncode)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 4 != 3

======================================================================
FAIL: test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (probe='lsof', exit=0)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_seat_args.py", line 175, in test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one
    self.assertEqual(4, result.returncode)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 4 != 3

----------------------------------------------------------------------
Ran 1 test in 1.448s

FAILED (failures=4)

```

### GREEN full requested two modules with process-only cache/signing overrides, exit0

```text
test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) ... ok
test_a_pr_closed_unmerged_is_reported_without_an_anchored_reset_record (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_pr_closed_unmerged_is_reported_without_an_anchored_reset_record) ... ok
test_a_pr_none_record_silences_only_a_task_whose_results_name_no_pr (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_pr_none_record_silences_only_a_task_whose_results_name_no_pr) ... ok
test_a_reset_record_naming_an_unrelated_accepted_design_anchors_nothing (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_reset_record_naming_an_unrelated_accepted_design_anchors_nothing) ... ok
test_a_reset_record_silences_only_when_another_identity_accepted_its_design (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_reset_record_silences_only_when_another_identity_accepted_its_design) ... ok
test_a_seated_worker_whose_pane_is_gone_names_the_stale_removal (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_seated_worker_whose_pane_is_gone_names_the_stale_removal) ... ok
test_a_seated_worker_without_its_profile_arguments_is_a_violation (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_seated_worker_without_its_profile_arguments_is_a_violation) ... ok
test_a_task_over_a_count_is_reported (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_task_over_a_count_is_reported) ... ok
test_a_waiver_line_silences_nothing (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_waiver_line_silences_nothing) ... ok
test_an_accepted_record_silences_only_when_the_tasks_pr_is_merged (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_an_accepted_record_silences_only_when_the_tasks_pr_is_merged) ... ok
test_each_listed_task_is_counted_and_an_unsafe_id_is_skipped (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_each_listed_task_is_counted_and_an_unsafe_id_is_skipped) ... ok
test_the_probe_skips_without_the_counters_script_or_a_readable_store (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_the_probe_skips_without_the_counters_script_or_a_readable_store) ... ok

----------------------------------------------------------------------
Ran 12 tests in 16.258s

OK

```

```text
$ shellcheck scripts/orchestrator/seat-args.sh scripts/check-regime-boundary.sh
stdout/stderr empty; exit=0
$ shfmt --indent 4 --space-redirects --diff scripts/orchestrator/seat-args.sh scripts/check-regime-boundary.sh
stdout/stderr empty; exit=0
$ UV_CACHE_DIR=/tmp/codex-worker-e-uv-cache uv run --no-project ruff format --check tests/unit/test_seat_args.py tests/unit/test_check_regime_boundary.py
2 files already formatted
exit=0
$ git diff --check -- scripts/orchestrator/seat-args.sh scripts/check-regime-boundary.sh tests/unit/test_seat_args.py tests/unit/test_check_regime_boundary.py
stdout/stderr empty; exit=0
$ git diff --numstat b167fe0a76a2e77d262f9f556c69ba6b9f118bbe -- scripts tests
17	1	scripts/check-regime-boundary.sh
119	0	scripts/orchestrator/seat-args.sh
56	0	tests/unit/test_check_regime_boundary.py
201	0	tests/unit/test_seat_args.py
exit=0; source137<=200, test additions257<=1000
$ shasum -a 256 <the four source/test files and task.md>
7abcdcdb867cd289fd26acaaa3103a4085f1b7f32ef5ad99413c55eb9a7e8a55  scripts/orchestrator/seat-args.sh
eb242b6e7f3ebcdeca2946993324f4012474e30ec85fdf6b418447764123d423  scripts/check-regime-boundary.sh
42215a55c685620b00cb53c1092c5abda30c6210d75d9f4d3e5582e78f4296d1  tests/unit/test_seat_args.py
27d86374f82d7f0d069e4896173ff311725dda83b041e4a56d6285246938dfb3  tests/unit/test_check_regime_boundary.py
148f5dde8795da8a8eeb265fcbbd40be11cb27e2407c979b772dcbcba772bd8f  .orchestration/dotfiles-T128-seat-launch-args-a01/task.md
```

## Independent second C50 transcript

Parent read full transcript; source hashes match tested bytes. SHA25654768faec91b016680275bc472010ca569c69256bb7f104c9a0a6b8346f1c23e. Approval is for the narrowed authorized failed/empty check and explicitly retains the nonempty namespace limitation.

# Seat launch arguments process-visibility C50 review

Review base: bfae75c14f52ff1b8083a69179bd90e91aa99458.

Scope: only the ps/lsof failure-and-empty-output delta in scripts/orchestrator/seat-args.sh and its four added subcases in tests/unit/test_seat_args.py. The orchestrator explicitly narrowed this C50 check to nonzero probes and empty usable output. No repository source, refs or configuration were changed by the reviewer; all exercised processes were fixture stubs.

## Conclusion

Approval for the authorized narrowed C50 delta, high confidence. The ps snapshot is captured once with its status; a nonzero status or no numeric process line returns unknown-probe/4. The lsof pipeline's nonzero status is preserved through pipefail; nonzero or empty extracted cwd returns unknown-probe/4. Diagnostics identify the failed probe and status without reproducing raw probe output. The four added subcases assert exact exit, stdout and stderr. Eight additional independent stub cases passed, including nonzero probes that still print plausible output, header-only ps, lsof without a cwd, and existing matching/unlaunched behavior. No further finding within the authorized scope.

Residual limitation: a nonempty sandbox PID namespace can hide host workers. Its visible snapshot is indistinguishable from a genuinely absent seat, and the script still returns unlaunched/3 when no matching process appears in that nonempty snapshot. This review does not claim host process visibility or closure of that residual limitation.

## Reviewed source SHA256

- scripts/orchestrator/seat-args.sh: 7abcdcdb867cd289fd26acaaa3103a4085f1b7f32ef5ad99413c55eb9a7e8a55
- tests/unit/test_seat_args.py: 42215a55c685620b00cb53c1092c5abda30c6210d75d9f4d3e5582e78f4296d1

## Exact command/output transcript

The outer execution tool exposes combined stdout/stderr, reproduced verbatim below with the recorded exit status. The behavioral check separately captures and prints every inner probe's stdout, stderr and exit status as JSON. No commands were rerun to create this transcript.

### Exact source/test delta, numbered source and source hashes

~~~bash
git diff bfae75c14f52ff1b8083a69179bd90e91aa99458 -- scripts/orchestrator/seat-args.sh tests/unit/test_seat_args.py && nl -ba scripts/orchestrator/seat-args.sh && shasum -a 256 scripts/orchestrator/seat-args.sh tests/unit/test_seat_args.py
~~~

Verbatim displayed output:

~~~text
diff --git a/scripts/orchestrator/seat-args.sh b/scripts/orchestrator/seat-args.sh
index 7cd98297..b8a9ecfd 100755
--- a/scripts/orchestrator/seat-args.sh
+++ b/scripts/orchestrator/seat-args.sh
@@ -44,6 +44,21 @@ if [[ ! -x ${ps_probe} ]] || { [[ ${kind} == codex ]] && [[ ! -x ${lsof_probe} ]
     exit 4
 fi
 
+# @description Skip a probe whose result cannot establish process visibility.
+# @arg $1 string Diagnostic without probe output.
+unknown_probe() {
+    printf '%s args=unknown-probe\n' "${label}"
+    printf 'seat-args: %s\n' "$1" >&2
+    exit 4
+}
+
+probe_status=0
+processes="$("${ps_probe}" -axo pid=,command= 2> /dev/null)" || probe_status=$?
+if ((probe_status != 0)); then unknown_probe "ps failed (exit ${probe_status})"; fi
+if ! grep -Eq '^[[:blank:]]*[0-9]+[[:blank:]]+[^[:blank:]]' <<< "${processes}"; then
+    unknown_probe 'ps listed no process'
+fi
+
 # @description Find one literal adjacent pair in the current process tokens.
 # @arg $1 string Flag.
 # @arg $2 string Value.
@@ -74,12 +89,14 @@ while read -r pid process_args; do
     else
         if [[ ${program##*/} != codex ]] &&
             { [[ ${program##*/} != node ]] || [[ ${words[1]:-} != */codex ]]; }; then continue; fi
-        cwd="$("${lsof_probe}" -a -p "${pid}" -d cwd -Fn 2> /dev/null | sed -n 's/^n//p')" || cwd=""
+        probe_status=0
+        cwd="$("${lsof_probe}" -a -p "${pid}" -d cwd -Fn 2> /dev/null | sed -n 's/^n//p')" || probe_status=$?
+        if ((probe_status != 0)) || [[ -z ${cwd} ]]; then unknown_probe "lsof failed (exit ${probe_status})"; fi
         [[ ${cwd} == "${project}" ]] || continue
     fi
     selected_pid=${pid}
     selected=("${words[@]}")
-done < <("${ps_probe}" -axo pid=,command= 2> /dev/null)
+done <<< "${processes}"
 
 if [[ -z ${selected_pid} ]]; then
     printf '%s process=none args=unlaunched\n' "${label}"
diff --git a/tests/unit/test_seat_args.py b/tests/unit/test_seat_args.py
index c799acc3..ce7521b2 100644
--- a/tests/unit/test_seat_args.py
+++ b/tests/unit/test_seat_args.py
@@ -157,6 +157,25 @@ class SeatArgsTest(unittest.TestCase):
         self.assertIn("-a -p 20 -d cwd -Fn", calls)
         self.assertEqual({"-axo pid=,command="}, set((self.home / "ps-calls").read_text().splitlines()))
 
+        original_ps, original_lsof = self.ps.read_text(), self.lsof.read_text()
+        for probe, code, kind, diagnostic in [
+            (self.ps, 1, "claude-code", "ps failed (exit 1)"),
+            (self.ps, 0, "claude-code", "ps listed no process"),
+            (self.lsof, 1, "codex", "lsof failed (exit 1)"),
+            (self.lsof, 0, "codex", "lsof failed (exit 0)"),
+        ]:
+            with self.subTest(probe=probe.name, exit=code):
+                self.ps.write_text(original_ps)
+                self.lsof.write_text(original_lsof)
+                probe.write_text(f"#!/bin/bash\nexit {code}\n")
+                self.profiles.write_text(profiles)
+                identity = claude if kind == "claude-code" else codex
+                result = self.run_probe(identity, kind, "t", project, f"200 {match}\n20 codex --profile standard\n")
+                runtime = "claude" if kind == "claude-code" else "codex"
+                self.assertEqual(4, result.returncode)
+                self.assertEqual(f"seat {identity} profile=standard kind={runtime} args=unknown-probe\n", result.stdout)
+                self.assertEqual(f"seat-args: {diagnostic}\n", result.stderr)
+
     def run_probe(self, identity, kind, teams, project, processes, **seams):
         (self.home / "ps-lines").write_text(processes)
         (self.home / "cwd-10").write_text("p10\nn/another/repository\n")
     1	#!/usr/bin/env bash
     2	# @file seat-args.sh
     3	# @brief Compare a seated worker's live arguments with its rendered profile.
     4	# @description
     5	#   Reads profile text and process probes without sourcing, writing or signalling.
     6	#   SEAT_ARGS_PS and SEAT_ARGS_LSOF replace the absolute probes in tests.
     7	# @arg $1 string Comma-separated teams of the seated identity.
     8	# @arg $2 string Identity in kind-profile-suffix form.
     9	# @arg $3 string Agent type, claude-code or codex.
    10	# @arg $4 path Project cwd used to select a Codex process.
    11	# @exitcode 0 Profile pairs match.
    12	# @exitcode 2 Arguments differ, or identity/profile is unknown.
    13	# @exitcode 3 No launched process matches.
    14	# @exitcode 4 A required probe binary is unavailable.
    15	set -euo pipefail
    16	
    17	teams=$1 identity=$2 agent_type=$3 project=$4
    18	if [[ ! ${identity} =~ ^(claude|codex)-([a-z][a-z0-9_]*)-[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
    19	    printf 'seat %s args=unknown-identity\n' "${identity}"
    20	    exit 2
    21	fi
    22	kind=${BASH_REMATCH[1]} profile=${BASH_REMATCH[2]}
    23	if [[ ${kind}:${agent_type} != claude:claude-code && ${kind}:${agent_type} != codex:codex ]]; then
    24	    printf 'seat %s args=unknown-identity\n' "${identity}"
    25	    exit 2
    26	fi
    27	label="seat ${identity} profile=${profile} kind=${kind}"
    28	key="MODEL_PROFILE_$(tr '[:lower:]' '[:upper:]' <<< "${profile}_${kind}")_ARGS"
    29	expected="$(awk -v key="${key}" 'index($0, key "=\"") == 1 && substr($0, length($0), 1) == "\"" {
    30	    print substr($0, length(key) + 3, length($0) - length(key) - 3); exit
    31	}' "${HOME}/.agents/model-profiles.env" 2> /dev/null)" || expected=""
    32	if [[ -z ${expected} ]]; then
    33	    printf '%s args=unknown-profile\n' "${label}"
    34	    exit 2
    35	fi
    36	[[ ${kind} != codex ]] || expected="--profile ${profile}"
    37	read -r -a expected_args <<< "${expected}"
    38	IFS=, read -r -a team_names <<< "${teams}"
    39	ps_probe=${SEAT_ARGS_PS:-/bin/ps}
    40	lsof_probe=${SEAT_ARGS_LSOF:-/usr/sbin/lsof}
    41	[[ -n ${SEAT_ARGS_LSOF+x} || -x ${lsof_probe} ]] || lsof_probe=/usr/bin/lsof
    42	if [[ ! -x ${ps_probe} ]] || { [[ ${kind} == codex ]] && [[ ! -x ${lsof_probe} ]]; }; then
    43	    printf '%s args=unknown-probe\n' "${label}"
    44	    exit 4
    45	fi
    46	
    47	# @description Skip a probe whose result cannot establish process visibility.
    48	# @arg $1 string Diagnostic without probe output.
    49	unknown_probe() {
    50	    printf '%s args=unknown-probe\n' "${label}"
    51	    printf 'seat-args: %s\n' "$1" >&2
    52	    exit 4
    53	}
    54	
    55	probe_status=0
    56	processes="$("${ps_probe}" -axo pid=,command= 2> /dev/null)" || probe_status=$?
    57	if ((probe_status != 0)); then unknown_probe "ps failed (exit ${probe_status})"; fi
    58	if ! grep -Eq '^[[:blank:]]*[0-9]+[[:blank:]]+[^[:blank:]]' <<< "${processes}"; then
    59	    unknown_probe 'ps listed no process'
    60	fi
    61	
    62	# @description Find one literal adjacent pair in the current process tokens.
    63	# @arg $1 string Flag.
    64	# @arg $2 string Value.
    65	has_pair() {
    66	    local index
    67	    for ((index = 1; index + 1 < ${#words[@]}; index++)); do
    68	        [[ ${words[index]} != "$1" || ${words[index + 1]} != "$2" ]] || return 0
    69	    done
    70	    return 1
    71	}
    72	
    73	selected_pid=""
    74	while read -r pid process_args; do
    75	    [[ ${pid} =~ ^[0-9]+$ ]] || continue
    76	    if [[ -n ${selected_pid} ]] && ((10#${pid} >= 10#${selected_pid})); then continue; fi
    77	    read -r -a words <<< "${process_args}"
    78	    program=${words[0]:-}
    79	    if [[ ${kind} == claude ]]; then
    80	        [[ ${program##*/} == claude ]] || continue
    81	        matched=false
    82	        for team in "${team_names[@]}"; do
    83	            if has_pair -n "${team}-${identity}"; then
    84	                matched=true
    85	                break
    86	            fi
    87	        done
    88	        [[ ${matched} == true ]] || continue
    89	    else
    90	        if [[ ${program##*/} != codex ]] &&
    91	            { [[ ${program##*/} != node ]] || [[ ${words[1]:-} != */codex ]]; }; then continue; fi
    92	        probe_status=0
    93	        cwd="$("${lsof_probe}" -a -p "${pid}" -d cwd -Fn 2> /dev/null | sed -n 's/^n//p')" || probe_status=$?
    94	        if ((probe_status != 0)) || [[ -z ${cwd} ]]; then unknown_probe "lsof failed (exit ${probe_status})"; fi
    95	        [[ ${cwd} == "${project}" ]] || continue
    96	    fi
    97	    selected_pid=${pid}
    98	    selected=("${words[@]}")
    99	done <<< "${processes}"
   100	
   101	if [[ -z ${selected_pid} ]]; then
   102	    printf '%s process=none args=unlaunched\n' "${label}"
   103	    exit 3
   104	fi
   105	words=("${selected[@]}")
   106	ok=true
   107	((${#expected_args[@]} % 2 == 0)) || ok=false
   108	for ((index = 0; index + 1 < ${#expected_args[@]}; index += 2)); do
   109	    has_pair "${expected_args[index]}" "${expected_args[index + 1]}" || ok=false
   110	done
   111	if [[ ${ok} == true ]]; then
   112	    printf '%s process=%s args=ok\n' "${label}" "${selected_pid}"
   113	    exit 0
   114	fi
   115	offset=1
   116	[[ ${words[0]##*/} != node ]] || offset=2
   117	printf '%s process=%s args=differs expected=%s found=%s\n' \
   118	    "${label}" "${selected_pid}" "${expected_args[*]}" "${words[*]:offset}"
   119	exit 2
7abcdcdb867cd289fd26acaaa3103a4085f1b7f32ef5ad99413c55eb9a7e8a55  scripts/orchestrator/seat-args.sh
42215a55c685620b00cb53c1092c5abda30c6210d75d9f4d3e5582e78f4296d1  tests/unit/test_seat_args.py
~~~

Exit status: 0. Tool chunk: 0ac17e.

### Additional stub-only process-visibility checks

~~~bash
PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/tmp/codex-worker-e-uv-cache uv run --no-project python - <<'PY'
import importlib.util
import json
from pathlib import Path

spec = importlib.util.spec_from_file_location('seat_probe_review_fixture', Path('tests/unit/test_seat_args.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
case = module.SeatArgsTest()
case.setUp()
project = str(case.temp / 'project with spaces')
claude = 'claude-standard-dot-a001'
codex = 'codex-standard-dot-a004'
matching = f'200 claude {module.CLAUDE_ARGS} -n t-{claude}\n'
case.profiles.write_text(
    f'MODEL_PROFILE_STANDARD_CLAUDE_ARGS="{module.CLAUDE_ARGS}"\n'
    'MODEL_PROFILE_STANDARD_CODEX_ARGS="--profile standard"\n'
)
original_ps, original_lsof = case.ps.read_text(), case.lsof.read_text()
cases = [
    ('ps failure despite valid stdout', claude, 'claude-code', '#!/bin/bash\ncat "$HOME/ps-lines"\nexit 7\n', None, matching, 4, 'ps failed (exit 7)'),
    ('ps empty success', claude, 'claude-code', '#!/bin/bash\nexit 0\n', None, matching, 4, 'ps listed no process'),
    ('ps header only', claude, 'claude-code', '#!/bin/bash\nprintf "PID COMMAND\\n"\n', None, matching, 4, 'ps listed no process'),
    ('lsof failure despite cwd stdout', codex, 'codex', None, '#!/bin/bash\ncat "$HOME/cwd-20"\nexit 7\n', '20 codex --profile standard\n', 4, 'lsof failed (exit 7)'),
    ('lsof empty success', codex, 'codex', None, '#!/bin/bash\nexit 0\n', '20 codex --profile standard\n', 4, 'lsof failed (exit 0)'),
    ('lsof pid only', codex, 'codex', None, '#!/bin/bash\nprintf "p20\\n"\n', '20 codex --profile standard\n', 4, 'lsof failed (exit 0)'),
    ('nonempty snapshot without target', claude, 'claude-code', None, None, '1 /sbin/init\n', 3, None),
    ('visible matching seat', claude, 'claude-code', None, None, matching, 0, None),
]
try:
    for label, identity, kind, ps_text, lsof_text, lines, code, diagnostic in cases:
        case.ps.write_text(ps_text if ps_text is not None else original_ps)
        case.lsof.write_text(lsof_text if lsof_text is not None else original_lsof)
        result = case.run_probe(identity, kind, 't', project, lines)
        runtime = 'claude' if kind == 'claude-code' else 'codex'
        prefix = f'seat {identity} profile=standard kind={runtime}'
        if code == 4:
            expected_stdout = f'{prefix} args=unknown-probe\n'
            expected_stderr = f'seat-args: {diagnostic}\n'
        else:
            tail = 'process=none args=unlaunched' if code == 3 else 'process=200 args=ok'
            expected_stdout = f'{prefix} {tail}\n'
            expected_stderr = ''
        assert (result.returncode, result.stdout, result.stderr) == (code, expected_stdout, expected_stderr), (label, result)
        print(json.dumps({'case': label, 'exit': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr}))
    print('8 additional stub-only process-visibility cases passed')
finally:
    case.doCleanups()
PY
~~~

Verbatim displayed output:

~~~text
{"case": "ps failure despite valid stdout", "exit": 4, "stdout": "seat claude-standard-dot-a001 profile=standard kind=claude args=unknown-probe\n", "stderr": "seat-args: ps failed (exit 7)\n"}
{"case": "ps empty success", "exit": 4, "stdout": "seat claude-standard-dot-a001 profile=standard kind=claude args=unknown-probe\n", "stderr": "seat-args: ps listed no process\n"}
{"case": "ps header only", "exit": 4, "stdout": "seat claude-standard-dot-a001 profile=standard kind=claude args=unknown-probe\n", "stderr": "seat-args: ps listed no process\n"}
{"case": "lsof failure despite cwd stdout", "exit": 4, "stdout": "seat codex-standard-dot-a004 profile=standard kind=codex args=unknown-probe\n", "stderr": "seat-args: lsof failed (exit 7)\n"}
{"case": "lsof empty success", "exit": 4, "stdout": "seat codex-standard-dot-a004 profile=standard kind=codex args=unknown-probe\n", "stderr": "seat-args: lsof failed (exit 0)\n"}
{"case": "lsof pid only", "exit": 4, "stdout": "seat codex-standard-dot-a004 profile=standard kind=codex args=unknown-probe\n", "stderr": "seat-args: lsof failed (exit 0)\n"}
{"case": "nonempty snapshot without target", "exit": 3, "stdout": "seat claude-standard-dot-a001 profile=standard kind=claude process=none args=unlaunched\n", "stderr": ""}
{"case": "visible matching seat", "exit": 0, "stdout": "seat claude-standard-dot-a001 profile=standard kind=claude process=200 args=ok\n", "stderr": ""}
8 additional stub-only process-visibility cases passed
~~~

Exit status: 0. Tool chunk: fccd08.

Not checked: live host/sandbox process lists, CI or the parent's concurrently running full two-module suite.

Verdict: correct


## Second C50 worker gate and masking

```text
$ AGENT_REVIEWED=1 REVIEW_EVIDENCE=.orchestration/dotfiles-T128-seat-launch-args-a01/seat-args-worker-review-receipt.md make require-crit-review
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.
exit=0
$ UV_CACHE_DIR=/tmp/codex-worker-e-uv-cache uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets <six changed canonical artifacts>
masked 0 match(es) in .orchestration/dotfiles-T128-seat-launch-args-a01/report.md
masked 0 match(es) in .orchestration/dotfiles-T128-seat-launch-args-a01/validation.md
masked 0 match(es) in .orchestration/dotfiles-T128-seat-launch-args-a01/learning.md
masked 0 match(es) in .orchestration/dotfiles-T128-seat-launch-args-a01/seat-args-worker-crit.json
masked 0 match(es) in .orchestration/dotfiles-T128-seat-launch-args-a01/seat-args-worker-review-receipt.md
masked 0 match(es) in .orchestration/dotfiles-T128-seat-launch-args-a01/revise.yaml
exit=0
```

## Third C50: continue after an uninspectable cwd

ACCEPTANCE2026-10-17T04:25:34Z, previous_heada428eb5ff31dc8452e22fbea332efa2a5ee9a5e8, Bot4301342120, process-visibility occurrence2. New regression subcases matching/differs/all-uninspectable assert both pid10 and20 were inspected; no host probe. The next same-class occurrence stops rounds pending re-plan.

### Prior exact-head Bot review body and inline finding

```text
{
  "head": "a428eb5ff31dc8452e22fbea332efa2a5ee9a5e8",
  "reviews": [
    {
      "body": "<!-- codex-review-receipt:v1 -->\n\n\n### \ud83d\udca1 Codex Review\n\nHere are some automated review suggestions for this pull request.\n\n**Reviewed commit:** `a428eb5ff3`\n    \n\n<details> <summary>\u2139\ufe0f About Codex in GitHub</summary>\n<br/>\n\nCodex has been enabled to automatically review pull requests in this repo. Reviews are triggered when you\n- Open a pull request for review\n- Mark a draft as ready\n- Comment \"@codex review\".\n\nIf Codex has suggestions, it will comment; otherwise it will react with \ud83d\udc4d.\n\n\n\n\nWhen you [sign up for Codex through ChatGPT](https://openai.com/codex), Codex can also answer questions or update the PR, like \"@codex address that feedback\".\n            \n</details>",
      "commit_id": "a428eb5ff31dc8452e22fbea332efa2a5ee9a5e8",
      "html_url": "https://github.com/mryfmo/dotfiles/pull/383#pullrequestreview-5556138510",
      "id": 5556138510,
      "state": "COMMENTED",
      "submitted_at": "2026-10-17T04:23:11Z"
    }
  ],
  "inline": [
    {
      "body": "**<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Continue past uninspectable unrelated Codex processes**\n\nWhen the global `ps` output contains any Codex-looking process whose cwd cannot be inspected\u2014for example, an unrelated process owned by another user or one that exits between `ps` and `lsof`\u2014this branch immediately returns `unknown-probe` (exit 4). `check-regime-boundary.sh` silently skips exit 4, so a later live worker process is never examined and mismatched launch arguments go unreported; continue scanning and only return unknown when no matching process can be established after accounting for failed lookups. This also leaves the process-input residual control ineffective for this availability failure mode.\n\nAGENTS.md reference: [AGENTS.md:L78-L78](https://github.com/mryfmo/dotfiles/blob/a428eb5ff31dc8452e22fbea332efa2a5ee9a5e8/AGENTS.md#L78-L78)\n\nUseful? React with \ud83d\udc4d\u00a0/ \ud83d\udc4e.\n\n<!-- codex-code-review-finding:v1 -->",
      "html_url": "https://github.com/mryfmo/dotfiles/pull/383#discussion_r4301342120",
      "id": 4301342120,
      "line": 94,
      "original_commit_id": "a428eb5ff31dc8452e22fbea332efa2a5ee9a5e8",
      "path": "scripts/orchestrator/seat-args.sh"
    }
  ],
  "issue_comments": [
    {
      "body": "<!-- codex-pull-request-review-summary -->\n<!-- codex-review-state:v1 {\"code_review\":{\"commit_sha\":\"a428eb5ff31dc8452e22fbea332efa2a5ee9a5e8\",\"has_any_findings\":true,\"has_unresolved_findings\":true,\"status\":\"completed\"},\"security_review\":{\"commit_sha\":\"274257172db0915df34e9f1764c69f572346727f\",\"has_any_findings\":false,\"has_unresolved_findings\":false,\"status\":\"completed\"}} -->\n<!-- codex-security-review:v1 {\"blockingSeverityThreshold\":\"P0\",\"headSha\":\"274257172db0915df34e9f1764c69f572346727f\",\"mergeGateEnabled\":false,\"pullRequestNumber\":383,\"repository\":\"mryfmo/dotfiles\",\"status\":\"completed\"} -->\n## Codex Review Summary\n\nThis comment shows the latest Codex review activity on this pull request.\n\n| Review | Status | Commit | Review trigger |\n| --- | --- | --- | --- |\n| \ud83d\udcdd **Code Review** | \u2705 **Completed** <relative-time datetime=\"2026-10-17T04:23:13.817632Z\">2026-10-17T04:23:13.817632Z</relative-time> | `a428eb5` | Manual request |\n| \ud83d\udd12 **Security Review** | \u2705 **Completed** <relative-time datetime=\"2026-10-17T04:05:25.814777Z\">2026-10-17T04:05:25.814777Z</relative-time> | `2742571` | Draft marked ready |\n\n\n\n<details> <summary>\u2139\ufe0f About Codex in GitHub</summary>\n<br/>\n\n[Your team has set up Codex to review pull requests in this repo](https://chatgpt.com/codex/cloud/settings/general). Reviews are triggered when you\n- Open a pull request for review\n- Mark a draft as ready\n- Comment \"@codex review\" or \"@codex security review\".\n\nCodex reacts with \ud83d\udc40 while any review is running, comments if it has suggestions, and reacts with \ud83d\udc4d once all reviews finish with no findings.\n\n</details>",
      "created_at": "2026-10-17T04:00:57Z",
      "html_url": "https://github.com/mryfmo/dotfiles/pull/383#issuecomment-6229380503",
      "id": 6229380503,
      "updated_at": "2026-10-17T04:23:14Z"
    }
  ]
}

```

### Stub reproduction before the fix

```text
{"script_exit": 4, "stdout": "seat codex-standard-dot-a004 profile=standard kind=codex args=unknown-probe\n", "stderr": "seat-args: lsof failed (exit 1)\n"}
Reproduced: uninspectable PID10 skips before visible mismatched PID20. Fixture only.

```

### RED prescribed seat method, exit1 expected

```text
test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) ... 
  test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (decoy_cwd_unavailable=True, profile='standard', all_unavailable=False) ... FAIL
  test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (decoy_cwd_unavailable=True, profile='review', all_unavailable=False) ... FAIL
  test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (decoy_cwd_unavailable=True, profile='standard', all_unavailable=True) ... FAIL

======================================================================
FAIL: test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (decoy_cwd_unavailable=True, profile='standard', all_unavailable=False)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_seat_args.py", line 172, in test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one
    self.assertEqual(code, result.returncode)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 0 != 4

======================================================================
FAIL: test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (decoy_cwd_unavailable=True, profile='review', all_unavailable=False)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_seat_args.py", line 172, in test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one
    self.assertEqual(code, result.returncode)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 2 != 4

======================================================================
FAIL: test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) (decoy_cwd_unavailable=True, profile='standard', all_unavailable=True)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_seat_args.py", line 175, in test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one
    self.assertEqual(
    ~~~~~~~~~~~~~~~~^
        ["-a -p 10 -d cwd -Fn", "-a -p 20 -d cwd -Fn"],
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        (self.home / "lsof-calls").read_text().splitlines(),
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
AssertionError: Lists differ: ['-a -p 10 -d cwd -Fn', '-a -p 20 -d cwd -Fn'] != ['-a -p 10 -d cwd -Fn']

First list contains 1 additional elements.
First extra element 1:
'-a -p 20 -d cwd -Fn'

- ['-a -p 10 -d cwd -Fn', '-a -p 20 -d cwd -Fn']
+ ['-a -p 10 -d cwd -Fn']

----------------------------------------------------------------------
Ran 1 test in 1.577s

FAILED (failures=3)

```

### GREEN full requested modules, process-only cache/signing overrides, exit0

```text
test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one (tests.unit.test_seat_args.SeatArgsTest.test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one) ... ok
test_a_pr_closed_unmerged_is_reported_without_an_anchored_reset_record (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_pr_closed_unmerged_is_reported_without_an_anchored_reset_record) ... ok
test_a_pr_none_record_silences_only_a_task_whose_results_name_no_pr (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_pr_none_record_silences_only_a_task_whose_results_name_no_pr) ... ok
test_a_reset_record_naming_an_unrelated_accepted_design_anchors_nothing (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_reset_record_naming_an_unrelated_accepted_design_anchors_nothing) ... ok
test_a_reset_record_silences_only_when_another_identity_accepted_its_design (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_reset_record_silences_only_when_another_identity_accepted_its_design) ... ok
test_a_seated_worker_whose_pane_is_gone_names_the_stale_removal (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_seated_worker_whose_pane_is_gone_names_the_stale_removal) ... ok
test_a_seated_worker_without_its_profile_arguments_is_a_violation (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_seated_worker_without_its_profile_arguments_is_a_violation) ... ok
test_a_task_over_a_count_is_reported (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_task_over_a_count_is_reported) ... ok
test_a_waiver_line_silences_nothing (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_waiver_line_silences_nothing) ... ok
test_an_accepted_record_silences_only_when_the_tasks_pr_is_merged (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_an_accepted_record_silences_only_when_the_tasks_pr_is_merged) ... ok
test_each_listed_task_is_counted_and_an_unsafe_id_is_skipped (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_each_listed_task_is_counted_and_an_unsafe_id_is_skipped) ... ok
test_the_probe_skips_without_the_counters_script_or_a_readable_store (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_the_probe_skips_without_the_counters_script_or_a_readable_store) ... ok

----------------------------------------------------------------------
Ran 12 tests in 16.254s

OK

```

```text
$ UV_CACHE_DIR=/tmp/codex-worker-e-uv-cache uv run --no-project ruff format tests/unit/test_seat_args.py
1 file reformatted
exit=0
$ shellcheck scripts/orchestrator/seat-args.sh scripts/check-regime-boundary.sh
stdout/stderr empty; exit=0
$ shfmt --indent 4 --space-redirects --diff scripts/orchestrator/seat-args.sh scripts/check-regime-boundary.sh
stdout/stderr empty; exit=0
$ UV_CACHE_DIR=/tmp/codex-worker-e-uv-cache uv run --no-project ruff format --check tests/unit/test_seat_args.py tests/unit/test_check_regime_boundary.py
2 files already formatted
exit=0
$ git diff --check -- scripts tests
stdout/stderr empty; exit=0
$ git diff --numstat b167fe0a76a2e77d262f9f556c69ba6b9f118bbe -- scripts tests
17	1	scripts/check-regime-boundary.sh
123	0	scripts/orchestrator/seat-args.sh
56	0	tests/unit/test_check_regime_boundary.py
222	0	tests/unit/test_seat_args.py
exit=0; source141<=200, test additions278<=1000
$ shasum -a 256 <four source/test files and immutable task copy>
656368a2217a223b4153fa038cbfc1401248dffc7d2a216d798691e21a7821ef  scripts/orchestrator/seat-args.sh
eb242b6e7f3ebcdeca2946993324f4012474e30ec85fdf6b418447764123d423  scripts/check-regime-boundary.sh
38e5199374fded7a6456ac4ff11799fd86690c96009cb7ec5d35239a7d4b2649  tests/unit/test_seat_args.py
27d86374f82d7f0d069e4896173ff311725dda83b041e4a56d6285246938dfb3  tests/unit/test_check_regime_boundary.py
148f5dde8795da8a8eeb265fcbbd40be11cb27e2407c979b772dcbcba772bd8f  .orchestration/dotfiles-T128-seat-launch-args-a01/task.md
```

## Independent third C50 review

Parent read the full transcript and matched the source hashes. SHA256621973453945c203a4c3d4c44d37eb87844cac94d8f637104d7e3c7510241035.

# Seat launch arguments deferred cwd diagnostic C50 review

Review base: a428eb5ff31dc8452e22fbea332efa2a5ee9a5e8.

Scope: the third authorized C50 delta for Bot P2 4301342120, class process-visibility. Only scripts/orchestrator/seat-args.sh and tests/unit/test_seat_args.py were reviewed. No repository files, refs or configuration were changed by this reviewer. All executed process probes were fixture stubs; no live host or sandbox ps/lsof was invoked.

## Conclusion

Review-scope approval, high confidence. The amended check is implemented correctly: each failed or empty cwd lookup records only the first diagnostic and continues scanning; a visible cwd match decides ok/differs; no match with a failed lookup returns unknown-probe/4 using that first diagnostic; no match after successful nonmatching lookups returns unlaunched/3. Existing minimum visible matching PID selection remains intact. The three new subcases exercise visible matching/differing workers after an uninspectable lower-PID decoy and all-uninspectable candidates, including exact lookup-call order. No additional finding.

Eight additional independent stub cases passed. These verify differing failure statuses retain the first diagnostic, an empty first lookup retains its exit-0 diagnostic, a failed lookup plus an inspected nonmatch yields unknown, all inspected nonmatches yield unlaunched, a visible match survives a later lower-PID lookup failure, and unsorted visible matching candidates preserve minimum-PID selection.

Residual limitation: a nonempty sandbox PID namespace can hide host workers. The script cannot distinguish those hidden workers from a genuinely absent seat when the visible nonempty snapshot contains no matching process. This review does not claim host visibility or closure of that limitation.

## Reviewed source SHA256

- scripts/orchestrator/seat-args.sh: 656368a2217a223b4153fa038cbfc1401248dffc7d2a216d798691e21a7821ef
- tests/unit/test_seat_args.py: 38e5199374fded7a6456ac4ff11799fd86690c96009cb7ec5d35239a7d4b2649

## Exact command/output transcript

The outer tool exposes combined stdout/stderr, reproduced verbatim with its recorded exit status. The fixture check separately captures and prints each inner probe's exit, stdout, stderr and recorded lsof calls as JSON. No commands were rerun to write this transcript.

### Exact C50 source/test delta, numbered source and hashes

~~~bash
git diff a428eb5ff31dc8452e22fbea332efa2a5ee9a5e8 -- scripts/orchestrator/seat-args.sh tests/unit/test_seat_args.py && nl -ba scripts/orchestrator/seat-args.sh | sed -n '68,130p' && shasum -a 256 scripts/orchestrator/seat-args.sh tests/unit/test_seat_args.py
~~~

Verbatim displayed output:

~~~text
diff --git a/scripts/orchestrator/seat-args.sh b/scripts/orchestrator/seat-args.sh
index b8a9ecfd..8783ab66 100755
--- a/scripts/orchestrator/seat-args.sh
+++ b/scripts/orchestrator/seat-args.sh
@@ -70,7 +70,7 @@ has_pair() {
     return 1
 }
 
-selected_pid=""
+selected_pid="" cwd_diagnostic=""
 while read -r pid process_args; do
     [[ ${pid} =~ ^[0-9]+$ ]] || continue
     if [[ -n ${selected_pid} ]] && ((10#${pid} >= 10#${selected_pid})); then continue; fi
@@ -91,7 +91,10 @@ while read -r pid process_args; do
             { [[ ${program##*/} != node ]] || [[ ${words[1]:-} != */codex ]]; }; then continue; fi
         probe_status=0
         cwd="$("${lsof_probe}" -a -p "${pid}" -d cwd -Fn 2> /dev/null | sed -n 's/^n//p')" || probe_status=$?
-        if ((probe_status != 0)) || [[ -z ${cwd} ]]; then unknown_probe "lsof failed (exit ${probe_status})"; fi
+        if ((probe_status != 0)) || [[ -z ${cwd} ]]; then
+            [[ -n ${cwd_diagnostic} ]] || cwd_diagnostic="lsof failed (exit ${probe_status})"
+            continue
+        fi
         [[ ${cwd} == "${project}" ]] || continue
     fi
     selected_pid=${pid}
@@ -99,6 +102,7 @@ while read -r pid process_args; do
 done <<< "${processes}"
 
 if [[ -z ${selected_pid} ]]; then
+    [[ -z ${cwd_diagnostic} ]] || unknown_probe "${cwd_diagnostic}"
     printf '%s process=none args=unlaunched\n' "${label}"
     exit 3
 fi
diff --git a/tests/unit/test_seat_args.py b/tests/unit/test_seat_args.py
index ce7521b2..93d928b1 100644
--- a/tests/unit/test_seat_args.py
+++ b/tests/unit/test_seat_args.py
@@ -158,6 +158,27 @@ class SeatArgsTest(unittest.TestCase):
         self.assertEqual({"-axo pid=,command="}, set((self.home / "ps-calls").read_text().splitlines()))
 
         original_ps, original_lsof = self.ps.read_text(), self.lsof.read_text()
+        for profile, all_unavailable, code, tail in [
+            ("standard", False, 0, "process=20 args=ok"),
+            ("review", False, 2, "process=20 args=differs expected=--profile standard found=--profile review"),
+            ("standard", True, 4, "args=unknown-probe"),
+        ]:
+            with self.subTest(decoy_cwd_unavailable=True, profile=profile, all_unavailable=all_unavailable):
+                lookup = "exit 1" if all_unavailable else '[[ $pid != 10 ]] || exit 1\ncat "$HOME/cwd-$pid"'
+                self.lsof.write_text(original_lsof.replace('cat "$HOME/cwd-$pid"', lookup))
+                (self.home / "lsof-calls").unlink()
+                self.profiles.write_text(profiles)
+                result = self.run_probe(
+                    codex, "codex", "t", project, f"10 codex --profile standard\n20 codex --profile {profile}\n"
+                )
+                self.assertEqual(code, result.returncode)
+                self.assertEqual(f"seat {codex} profile=standard kind=codex {tail}\n", result.stdout)
+                self.assertEqual("seat-args: lsof failed (exit 1)\n" if all_unavailable else "", result.stderr)
+                self.assertEqual(
+                    ["-a -p 10 -d cwd -Fn", "-a -p 20 -d cwd -Fn"],
+                    (self.home / "lsof-calls").read_text().splitlines(),
+                )
+
         for probe, code, kind, diagnostic in [
             (self.ps, 1, "claude-code", "ps failed (exit 1)"),
             (self.ps, 0, "claude-code", "ps listed no process"),
    68	        [[ ${words[index]} != "$1" || ${words[index + 1]} != "$2" ]] || return 0
    69	    done
    70	    return 1
    71	}
    72	
    73	selected_pid="" cwd_diagnostic=""
    74	while read -r pid process_args; do
    75	    [[ ${pid} =~ ^[0-9]+$ ]] || continue
    76	    if [[ -n ${selected_pid} ]] && ((10#${pid} >= 10#${selected_pid})); then continue; fi
    77	    read -r -a words <<< "${process_args}"
    78	    program=${words[0]:-}
    79	    if [[ ${kind} == claude ]]; then
    80	        [[ ${program##*/} == claude ]] || continue
    81	        matched=false
    82	        for team in "${team_names[@]}"; do
    83	            if has_pair -n "${team}-${identity}"; then
    84	                matched=true
    85	                break
    86	            fi
    87	        done
    88	        [[ ${matched} == true ]] || continue
    89	    else
    90	        if [[ ${program##*/} != codex ]] &&
    91	            { [[ ${program##*/} != node ]] || [[ ${words[1]:-} != */codex ]]; }; then continue; fi
    92	        probe_status=0
    93	        cwd="$("${lsof_probe}" -a -p "${pid}" -d cwd -Fn 2> /dev/null | sed -n 's/^n//p')" || probe_status=$?
    94	        if ((probe_status != 0)) || [[ -z ${cwd} ]]; then
    95	            [[ -n ${cwd_diagnostic} ]] || cwd_diagnostic="lsof failed (exit ${probe_status})"
    96	            continue
    97	        fi
    98	        [[ ${cwd} == "${project}" ]] || continue
    99	    fi
   100	    selected_pid=${pid}
   101	    selected=("${words[@]}")
   102	done <<< "${processes}"
   103	
   104	if [[ -z ${selected_pid} ]]; then
   105	    [[ -z ${cwd_diagnostic} ]] || unknown_probe "${cwd_diagnostic}"
   106	    printf '%s process=none args=unlaunched\n' "${label}"
   107	    exit 3
   108	fi
   109	words=("${selected[@]}")
   110	ok=true
   111	((${#expected_args[@]} % 2 == 0)) || ok=false
   112	for ((index = 0; index + 1 < ${#expected_args[@]}; index += 2)); do
   113	    has_pair "${expected_args[index]}" "${expected_args[index + 1]}" || ok=false
   114	done
   115	if [[ ${ok} == true ]]; then
   116	    printf '%s process=%s args=ok\n' "${label}" "${selected_pid}"
   117	    exit 0
   118	fi
   119	offset=1
   120	[[ ${words[0]##*/} != node ]] || offset=2
   121	printf '%s process=%s args=differs expected=%s found=%s\n' \
   122	    "${label}" "${selected_pid}" "${expected_args[*]}" "${words[*]:offset}"
   123	exit 2
656368a2217a223b4153fa038cbfc1401248dffc7d2a216d798691e21a7821ef  scripts/orchestrator/seat-args.sh
38e5199374fded7a6456ac4ff11799fd86690c96009cb7ec5d35239a7d4b2649  tests/unit/test_seat_args.py
~~~

Exit status: 0. Tool chunk: 96fff3.

### Additional deferred-diagnostic fixture checks

~~~bash
PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/tmp/codex-worker-e-uv-cache uv run --no-project python - <<'PY'
import importlib.util
import json
from pathlib import Path

spec = importlib.util.spec_from_file_location('seat_cwd_review_fixture', Path('tests/unit/test_seat_args.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
case = module.SeatArgsTest()
case.setUp()
identity = 'codex-standard-dot-a004'
project = str(case.temp / 'project with spaces')
case.profiles.write_text('MODEL_PROFILE_STANDARD_CODEX_ARGS="--profile standard"\n')
original_lsof = case.lsof.read_text()
assert original_lsof.count('cat "$HOME/cwd-$pid"') == 1
normal = '10 codex --profile standard\n20 codex --profile standard\n'
nonmatch = 'printf "p20\\nn/another/repository\\n"'
cases = [
    ('failure then matching worker', normal, '[[ $pid != 10 ]] || exit 7\ncat "$HOME/cwd-$pid"', 0, 'process=20 args=ok', '', ['10', '20']),
    ('failure then differing worker', normal.replace('20 codex --profile standard', '20 codex --profile review'), '[[ $pid != 10 ]] || exit 7\ncat "$HOME/cwd-$pid"', 2, 'process=20 args=differs expected=--profile standard found=--profile review', '', ['10', '20']),
    ('first failure retained across failed candidates', normal, 'if [[ $pid == 10 ]]; then exit 7; else exit 9; fi', 4, 'args=unknown-probe', 'seat-args: lsof failed (exit 7)\n', ['10', '20']),
    ('failure plus inspected nonmatch', normal, '[[ $pid != 10 ]] || exit 7\n' + nonmatch, 4, 'args=unknown-probe', 'seat-args: lsof failed (exit 7)\n', ['10', '20']),
    ('all inspected candidates nonmatching', normal, nonmatch, 3, 'process=none args=unlaunched', '', ['10', '20']),
    ('visible match survives later lower-pid failure', '20 codex --profile standard\n10 codex --profile standard\n', '[[ $pid != 10 ]] || exit 7\ncat "$HOME/cwd-$pid"', 0, 'process=20 args=ok', '', ['20', '10']),
    ('minimum visible matching pid still wins', '20 codex --profile standard\n10 codex --profile review\n', 'cat "$HOME/cwd-20"', 2, 'process=10 args=differs expected=--profile standard found=--profile review', '', ['20', '10']),
    ('first empty-lookup diagnostic retained', normal, 'if [[ $pid == 10 ]]; then exit 0; else exit 9; fi', 4, 'args=unknown-probe', 'seat-args: lsof failed (exit 0)\n', ['10', '20']),
]
try:
    for label, lines, lookup, code, tail, stderr, pids in cases:
        case.lsof.write_text(original_lsof.replace('cat "$HOME/cwd-$pid"', lookup))
        (case.home / 'lsof-calls').write_text('')
        result = case.run_probe(identity, 'codex', 't', project, lines)
        calls = (case.home / 'lsof-calls').read_text().splitlines()
        expected_stdout = f'seat {identity} profile=standard kind=codex {tail}\n'
        assert (result.returncode, result.stdout, result.stderr) == (code, expected_stdout, stderr), (label, result)
        assert calls == [f'-a -p {pid} -d cwd -Fn' for pid in pids], (label, calls)
        print(json.dumps({'case': label, 'exit': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr, 'lsof_calls': calls}))
    print('8 additional deferred-cwd-diagnostic stub cases passed')
finally:
    case.doCleanups()
PY
~~~

Verbatim displayed output:

~~~text
{"case": "failure then matching worker", "exit": 0, "stdout": "seat codex-standard-dot-a004 profile=standard kind=codex process=20 args=ok\n", "stderr": "", "lsof_calls": ["-a -p 10 -d cwd -Fn", "-a -p 20 -d cwd -Fn"]}
{"case": "failure then differing worker", "exit": 2, "stdout": "seat codex-standard-dot-a004 profile=standard kind=codex process=20 args=differs expected=--profile standard found=--profile review\n", "stderr": "", "lsof_calls": ["-a -p 10 -d cwd -Fn", "-a -p 20 -d cwd -Fn"]}
{"case": "first failure retained across failed candidates", "exit": 4, "stdout": "seat codex-standard-dot-a004 profile=standard kind=codex args=unknown-probe\n", "stderr": "seat-args: lsof failed (exit 7)\n", "lsof_calls": ["-a -p 10 -d cwd -Fn", "-a -p 20 -d cwd -Fn"]}
{"case": "failure plus inspected nonmatch", "exit": 4, "stdout": "seat codex-standard-dot-a004 profile=standard kind=codex args=unknown-probe\n", "stderr": "seat-args: lsof failed (exit 7)\n", "lsof_calls": ["-a -p 10 -d cwd -Fn", "-a -p 20 -d cwd -Fn"]}
{"case": "all inspected candidates nonmatching", "exit": 3, "stdout": "seat codex-standard-dot-a004 profile=standard kind=codex process=none args=unlaunched\n", "stderr": "", "lsof_calls": ["-a -p 10 -d cwd -Fn", "-a -p 20 -d cwd -Fn"]}
{"case": "visible match survives later lower-pid failure", "exit": 0, "stdout": "seat codex-standard-dot-a004 profile=standard kind=codex process=20 args=ok\n", "stderr": "", "lsof_calls": ["-a -p 20 -d cwd -Fn", "-a -p 10 -d cwd -Fn"]}
{"case": "minimum visible matching pid still wins", "exit": 2, "stdout": "seat codex-standard-dot-a004 profile=standard kind=codex process=10 args=differs expected=--profile standard found=--profile review\n", "stderr": "", "lsof_calls": ["-a -p 20 -d cwd -Fn", "-a -p 10 -d cwd -Fn"]}
{"case": "first empty-lookup diagnostic retained", "exit": 4, "stdout": "seat codex-standard-dot-a004 profile=standard kind=codex args=unknown-probe\n", "stderr": "seat-args: lsof failed (exit 0)\n", "lsof_calls": ["-a -p 10 -d cwd -Fn", "-a -p 20 -d cwd -Fn"]}
8 additional deferred-cwd-diagnostic stub cases passed
~~~

Exit status: 0. Tool chunk: 430677.

Not checked: live processes, CI or the parent's concurrently running full two-module suite.

Verdict: correct


## Third C50 gate and masking

```text
$ AGENT_REVIEWED=1 REVIEW_EVIDENCE=.orchestration/dotfiles-T128-seat-launch-args-a01/seat-args-worker-review-receipt.md make require-crit-review
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.
exit=0
$ UV_CACHE_DIR=/tmp/codex-worker-e-uv-cache uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets <six changed canonical artifacts>
masked 0 match(es) in .orchestration/dotfiles-T128-seat-launch-args-a01/report.md
masked 0 match(es) in .orchestration/dotfiles-T128-seat-launch-args-a01/validation.md
masked 0 match(es) in .orchestration/dotfiles-T128-seat-launch-args-a01/learning.md
masked 0 match(es) in .orchestration/dotfiles-T128-seat-launch-args-a01/seat-args-worker-crit.json
masked 0 match(es) in .orchestration/dotfiles-T128-seat-launch-args-a01/seat-args-worker-review-receipt.md
masked 0 match(es) in .orchestration/dotfiles-T128-seat-launch-args-a01/revise.yaml
exit=0
```
