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
