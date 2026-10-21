---
task_id: dotfiles-T133-pre-send-check-a03
seat: claude-standard-dot-a009
reset_of: dotfiles-T133-pre-send-check-a02
production_head: 1d72f16978018c3d016bbc239d79d3d7d0675105
red_fixture_commit: 96d0afefe904c5ec8b3bf13ff82a7151bb8518f1
fix_commit: 9dc5c565d6d21d4f52d5f317ca7f40d577425010
correction_commit: b8a5c394be64a666a6531435b562c5a3a9e0b878
merge_base: e00de4e0e4158de19e2c8921e572461e7e9e4ca0
---

# Validation: dotfiles-T133-pre-send-check-a03

- **Producer:** every block was run by the worker, on the Claude seat `claude-standard-dot-a009`, inside its sandbox, unless it says otherwise.
- **Placeholders:** `$HOME`, `$TMPDIR` and `$uv_path` stand for their values.
- **Branch:** the local branch is `a03/pre-send-check`. `tools/pre-send-check-a01` is checked out in a008's worktree worker-f, and git refuses a second checkout. It is pushed as `HEAD:tools/pre-send-check-a01` (sandbox record).

## 1. The task copy and uv
```console
$ shasum -a 256 "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md"
53f78f967929b80987eb515affaabde637d12c1f52edb8bce5262c95f8282f77  $HOME/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-pre-send-check-a03.md
53f78f967929b80987eb515affaabde637d12c1f52edb8bce5262c95f8282f77  .orchestration/dotfiles-T133-pre-send-check-a03/task.md
$ /usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" "$HOME/.local/bin/mise" which uv
$HOME/.local/share/mise/installs/uv/latest/uv-aarch64-apple-darwin/uv
uv_path above
[exit 0]
```

## 2. Red: the six regressions at the production head (tree 96d0afef = 1d72f169 + the red fixtures), each by exact id, with its failing assertion
```console
$ for each id: /usr/bin/env -i PATH="$(dirname "$uv_path"):/usr/bin:/bin" HOME="$HOME" TMPDIR="$TMPDIR" LANG=C.UTF-8 "$HOME/.local/share/mise/installs/python/3.15.0/bin/python3" -I tests/unit/test_pre_send.py PreSendTest.<id>
== test_multiline_task_id_has_parser_locations
FAIL: test_multiline_task_id_has_parser_locations (__main__.PreSendTest.test_multiline_task_id_has_parser_locations)
AssertionError: 'consistency: refused' not found in ['consistency: refused line(s) 1234567891', 'sha256: 00cd25e99b2930b65306286268a7bee151ca4144fb04e54f2880524039b47f43']
Ran 1 test in 0.453s
FAILED (failures=1)
== test_crlf_tilde_closer
FAIL: test_crlf_tilde_closer (__main__.PreSendTest.test_crlf_tilde_closer) (eol="'\\r\\n'")
AssertionError: 1 != 0 : sha256: 725d6f1f7f2da73ff2013a45e91cda72e3f685afe7baa03f238b28b00985ab20
FAIL: test_crlf_tilde_closer (__main__.PreSendTest.test_crlf_tilde_closer) (eol="'\\r'")
AssertionError: 1 != 0 : sha256: 02a614f390093760e0fc1efb4d8163a9c485090af8042a287560e38049047d0f
FAIL: test_crlf_tilde_closer (__main__.PreSendTest.test_crlf_tilde_closer)
AssertionError: 1 != 0 : sha256: 0b70812dcaf498aec373d9e84447ce623a6de56d67e0a2e238bf6a6c0fc90bcd
Ran 1 test in 0.494s
FAILED (failures=3)
== test_fenced_item_does_not_supply_owner_work
FAIL: test_fenced_item_does_not_supply_owner_work (__main__.PreSendTest.test_fenced_item_does_not_supply_owner_work)
AssertionError: 1 != 0 : sha256: ded23a701dd548793d4eade9515b8bcb79e99ce0603a2e7d579636293fb64084
Ran 1 test in 0.180s
FAILED (failures=1)
== test_digest_survives_replacement_and_helper_failure
FAIL: test_digest_survives_replacement_and_helper_failure (__main__.PreSendTest.test_digest_survives_replacement_and_helper_failure)
AssertionError: 'sha256: 7b4c3f32cc3b736ebb4e47dd0cc50601c0d554cfef51c76cc3a948fd71708f3c' != 'sha256: 6c1aa50442a93e42c0eb2907cf4e017cd19547891fa190f3ea473582b0479290'
Ran 1 test in 0.180s
FAILED (failures=1)
== test_entrypoint_fixed_environment
FAIL: test_entrypoint_fixed_environment (__main__.PreSendTest.test_entrypoint_fixed_environment) (path='/usr/bin:/bin')
AssertionError: Tuples differ: (0, '') != (1, '')
FAIL: test_entrypoint_fixed_environment (__main__.PreSendTest.test_entrypoint_fixed_environment) (path='$TMPDIR/tmpso3cmvom/decoy:/usr/bin:/bin')
AssertionError: Tuples differ: (0, '') != (1, '')
Ran 1 test in 0.406s
FAILED (failures=2)
== test_temp_failure_is_redacted
FAIL: test_temp_failure_is_redacted (__main__.PreSendTest.test_temp_failure_is_redacted)
AssertionError: 1 != 0 : sha256: be694e4d91f3a7bfc086c56ace0f4c583b7f7a6f3b131a8f43d9735d12198675
Ran 1 test in 0.199s
FAILED (failures=1)
```
This run was made on the working tree just before the red-fixture commit, whose content is byte-identical to 96d0afef. §3 repeats it at 96d0afef by commit.

## 3. Red at 96d0afef and green at 9dc5c565 (scratch worktree of 96d0afef, removed), by exact id and in full
```console
=== tree 96d0afefe904c5ec8b3bf13ff82a7151bb8518f1
test_multiline_task_id_has_parser_locations: FAILED (failures=1)
test_crlf_tilde_closer: FAILED (failures=3)
test_fenced_item_does_not_supply_owner_work: FAILED (failures=1)
test_digest_survives_replacement_and_helper_failure: FAILED (failures=1)
test_entrypoint_fixed_environment: FAILED (failures=2)
test_temp_failure_is_redacted: FAILED (failures=1)
full module: Ran 34 tests in 9.572s FAILED (failures=9) 
=== tree 9dc5c565d6d21d4f52d5f317ca7f40d577425010
test_multiline_task_id_has_parser_locations: OK
test_crlf_tilde_closer: OK
test_fenced_item_does_not_supply_owner_work: OK
test_digest_survives_replacement_and_helper_failure: OK
test_entrypoint_fixed_environment: OK
test_temp_failure_is_redacted: OK
full module: Ran 34 tests in 11.515s OK 
```
At 96d0afef the full module's 9 failures are exactly the six regressions' subtests (1+3+1+1+2+1). The 28 preserved tests pass both before and after the change.

## 4. The review round: the dirname decoy, red at 9dc5c565 with the tightened tests, green at b8a5c394
```console
$ for each: /usr/bin/env -i PATH="$(dirname "$uv_path"):/usr/bin:/bin" HOME="$HOME" TMPDIR="$TMPDIR" LANG=C.UTF-8 "$HOME/.local/share/mise/installs/python/3.15.0/bin/python3" -I tests/unit/test_pre_send.py PreSendTest.<id>   (tests of b8a5c394, entrypoint of 9dc5c565)
test_entrypoint_fixed_environment: AssertionError: Tuples differ: (0, '') != (1, '') FAILED (failures=1) 
test_temp_failure_is_redacted: OK 
$ /usr/bin/env -i PATH="$(dirname "$uv_path"):/usr/bin:/bin" HOME="$HOME" TMPDIR="$TMPDIR" LANG=C.UTF-8 "$HOME/.local/share/mise/installs/python/3.15.0/bin/python3" -I tests/unit/test_pre_send.py   (at b8a5c394)
Ran 34 tests in 14.867s

OK
[exit 0]
```

## 5. Static checks, caps and attribution at b8a5c394
```console
$ bash -n scripts/orchestrator/pre-send.sh
[exit 0]
$ shellcheck -x scripts/orchestrator/pre-send.sh
[exit 0]
$ shfmt -i 4 -sr -d scripts/orchestrator/pre-send.sh
[exit 0]
$ ruff check --config ruff.toml scripts/orchestrator/pre_send.py tests/unit/test_pre_send.py
All checks passed!
[exit 0]
$ ruff format --config ruff.toml --check scripts/orchestrator/pre_send.py tests/unit/test_pre_send.py
2 files already formatted
[exit 0]
$ uv run --no-project --python 3.15 python -I scripts/lint-comparisons.py --changed scripts/orchestrator/pre-send.sh scripts/orchestrator/pre_send.py tests/unit/test_pre_send.py -- scripts/orchestrator/pre-send.sh scripts/orchestrator/pre_send.py tests/unit/test_pre_send.py
[exit 0]
$ git merge-base origin/main b8a5c394be64a666a6531435b562c5a3a9e0b878; git diff --numstat e00de4e0e4158de19e2c8921e572461e7e9e4ca0 b8a5c394be64a666a6531435b562c5a3a9e0b878 -- . ':(exclude).orchestration'
e00de4e0e4158de19e2c8921e572461e7e9e4ca0
32	0	scripts/orchestrator/pre-send.sh
194	0	scripts/orchestrator/pre_send.py
359	0	tests/unit/test_pre_send.py
changed_non_tests: 226 of 360
changed_tests: 359 of 480
$ final-line attribution at b8a5c394be64a666a6531435b562c5a3a9e0b878 (git blame --line-porcelain; a03 commits 96d0afef, 9dc5c565, b8a5c394)
scripts/orchestrator/pre-send.sh: inherited a01/a02 12, a03 20
scripts/orchestrator/pre_send.py: inherited a01/a02 0, a03 194
tests/unit/test_pre_send.py: inherited a01/a02 258, a03 101
```

## 6. The crit-review gate
```console
$ AGENT_REVIEWED=1 REVIEW_EVIDENCE=.orchestration/dotfiles-T133-pre-send-check-a03/dotfiles-T133-pre-send-check-a03-worker-review-receipt.md make require-crit-review
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.
[exit 0]
```
