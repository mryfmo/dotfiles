# Validation: dotfiles-T103-gh-auth-stores-a01

- **PR:** #288, branch `feat/gh-auth-stores` on base `origin/main` `2d0ef943`. `main` has not moved, so the branch is up to date.
- **Final head:** `0a28eb74c3f921b254011f1d4cde667ada2e30a3`.
- **task_rev:** dispatch `sha256:81602cc11cfe4acc76436b0b9389f57056007012eb2a1f5aebe959dc1bcbd299`; PONG decision 1 `sha256:3f7c52c2f697c706b0eb30a71d2357d4f47767af139f9a68ca976d1a80c7ba86`; PONG decision 2 `sha256:e1045624ccf3d4645255dfcb056b7d71b276433be41e500576aac6e16543ad95`.

## Task validation commands on the final head 0a28eb74 (verbatim)

```
$ git rev-parse HEAD
0a28eb74c3f921b254011f1d4cde667ada2e30a3
exit=0
```

```
$ bash -n setup.sh scripts/gh-auth-stores.sh; echo "rc=$?"
rc=0
exit=0
```

```
$ shellcheck setup.sh scripts/gh-auth-stores.sh; echo "rc=$?"
rc=0
exit=0
```

```
$ make render-check
uv run --with pyyaml scripts/generate-agent-configs.py --check
generated agent configs are up to date
exit=0
```

```
$ make unit-test 2>&1 | tail -3
Ran 915 tests in 221.097s

OK (skipped=1)
exit=0
```

```
$ uv run --no-project --with pyyaml scripts/validate-agent-assets.py; echo "rc=$?"
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/autoskill/runs/dotfiles-T103-gh-auth-stores-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/learning/dotfiles-T103-gh-auth-stores-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/sandboxes/dotfiles-T103-gh-auth-stores-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/tasks/dotfiles-T103-gh-auth-stores-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/github-auth-design-2026-10-05.md
agent asset validation ok
rc=0
exit=0
```

```
$ grep -n 'gh auth login' Makefile scripts/update-agent-assets.sh home/.chezmoiscripts 2>/dev/null; echo "rc=$? (expect no match outside the gh-auth target)"
rc=2 (expect no match outside the gh-auth target)
exit=0
```

```
$ grep -rn 'gh auth login' Makefile scripts/update-agent-assets.sh home/.chezmoiscripts; echo "rc=$?   # recursive form: home/.chezmoiscripts is a directory, which plain grep -n reports as an error (rc=2 above)"
rc=1   # recursive form: home/.chezmoiscripts is a directory, which plain grep -n reports as an error (rc=2 above)
exit=0
```

```
$ grep -rn 'gh auth setup-git' setup.sh scripts/ Makefile; echo "rc=$?   # only the explanatory comment remains (PONG decision 1)"
scripts/gh-auth-stores.sh:14:#   `gh auth setup-git` would rewrite that chezmoi-managed file. No credential
rc=0   # only the explanatory comment remains (PONG decision 1)
exit=0
```

```
$ bash -n scripts/check-tools.sh && shellcheck scripts/check-tools.sh; echo "rc=$?"
rc=0
exit=0
```

```
$ git ls-files -z "*.py" | xargs -0 ruff format --config ruff.toml --check
44 files already formatted
exit=0
```

```
$ mise x node npm:prettier -- prettier --check README.md
Checking formatting...
All matched files use Prettier code style!
exit=0
```

```
$ git diff origin/main --stat
 Makefile                                  |   5 ++
 README.md                                 |  52 ++++++++++---
 home/dot_agents/agent-config.yaml         |   9 ++-
 home/dot_agents/model-profiles.env        |   2 +
 scripts/check-agent-runtime.py            |  76 ++++++++++++++++++-
 scripts/check-tools.sh                    |   2 +-
 scripts/generate-agent-configs.py         |  29 +++++++-
 scripts/gh-auth-stores.sh                 |  83 +++++++++++++++++++++
 setup.sh                                  |  15 ++++
 tests/unit/test_check_agent_runtime.py    |  84 +++++++++++++++++++++
 tests/unit/test_generate_agent_configs.py |  31 ++++++++
 tests/unit/test_gh_auth_stores.py         | 120 ++++++++++++++++++++++++++++++
 tests/unit/test_runtime_health.py         |   2 +-
 13 files changed, 488 insertions(+), 22 deletions(-)
exit=0
```

## The new tests on origin/main (2d0ef943)

```
$ (scratch worktree at origin/main 2d0ef943, with the T103 test files copied in) uv run --no-project python -m unittest <the new T103 tests>
EEEEF
======================================================================
ERROR: test_on_a_terminal_it_logs_in_only_the_empty_stores (tests.unit.test_gh_auth_stores.GhAuthStoresTest.test_on_a_terminal_it_logs_in_only_the_empty_stores)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tmp/claude-1000/-home-moriya-Workspace-dotfiles--claude-worktrees-worker-c/79f0f3c0-a708-4c6f-affe-0d87fcc6ba5a/scratchpad/t103-base/tests/unit/test_gh_auth_stores.py", line 77, in test_on_a_terminal_it_logs_in_only_the_empty_stores
    result = self.run_script(secondary)
  File "/tmp/claude-1000/-home-moriya-Workspace-dotfiles--claude-worktrees-worker-c/79f0f3c0-a708-4c6f-affe-0d87fcc6ba5a/scratchpad/t103-base/tests/unit/test_gh_auth_stores.py", line 59, in run_script
    return subprocess.run(
           ~~~~~~~~~~~~~~^
        [str(SCRIPT)], stdin=stdin, env=self.env, capture_output=True, text=True, check=False, timeout=30
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "~/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/subprocess.py", line 554, in run
    with Popen(*popenargs, **kwargs) as process:
         ~~~~~^^^^^^^^^^^^^^^^^^^^^^
  File "~/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/subprocess.py", line 1039, in __init__
    self._execute_child(args, executable, preexec_fn, close_fds,
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                        pass_fds, cwd, env,
                        ^^^^^^^^^^^^^^^^^^^
    ...<5 lines>...
                        gid, gids, uid, umask,
                        ^^^^^^^^^^^^^^^^^^^^^^
                        start_new_session, process_group)
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "~/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/subprocess.py", line 1991, in _execute_child
    raise child_exception_type(errno_num, err_msg, err_filename)
FileNotFoundError: [Errno 2] No such file or directory: '/tmp/claude-1000/-home-moriya-Workspace-dotfiles--claude-worktrees-worker-c/79f0f3c0-a708-4c6f-affe-0d87fcc6ba5a/scratchpad/t103-base/scripts/gh-auth-stores.sh'

======================================================================
ERROR: test_without_a_terminal_it_never_prompts (tests.unit.test_gh_auth_stores.GhAuthStoresTest.test_without_a_terminal_it_never_prompts)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tmp/claude-1000/-home-moriya-Workspace-dotfiles--claude-worktrees-worker-c/79f0f3c0-a708-4c6f-affe-0d87fcc6ba5a/scratchpad/t103-base/tests/unit/test_gh_auth_stores.py", line 67, in test_without_a_terminal_it_never_prompts
    result = self.run_script(subprocess.DEVNULL)
  File "/tmp/claude-1000/-home-moriya-Workspace-dotfiles--claude-worktrees-worker-c/79f0f3c0-a708-4c6f-affe-0d87fcc6ba5a/scratchpad/t103-base/tests/unit/test_gh_auth_stores.py", line 59, in run_script
    return subprocess.run(
           ~~~~~~~~~~~~~~^
        [str(SCRIPT)], stdin=stdin, env=self.env, capture_output=True, text=True, check=False, timeout=30
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "~/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/subprocess.py", line 554, in run
    with Popen(*popenargs, **kwargs) as process:
         ~~~~~^^^^^^^^^^^^^^^^^^^^^^
  File "~/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/subprocess.py", line 1039, in __init__
    self._execute_child(args, executable, preexec_fn, close_fds,
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                        pass_fds, cwd, env,
                        ^^^^^^^^^^^^^^^^^^^
    ...<5 lines>...
                        gid, gids, uid, umask,
                        ^^^^^^^^^^^^^^^^^^^^^^
                        start_new_session, process_group)
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "~/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/subprocess.py", line 1991, in _execute_child
    raise child_exception_type(errno_num, err_msg, err_filename)
FileNotFoundError: [Errno 2] No such file or directory: '/tmp/claude-1000/-home-moriya-Workspace-dotfiles--claude-worktrees-worker-c/79f0f3c0-a708-4c6f-affe-0d87fcc6ba5a/scratchpad/t103-base/scripts/gh-auth-stores.sh'

======================================================================
ERROR: test_gh_credential_stores_report_present_missing_and_bad_mode (tests.unit.test_check_agent_runtime.CheckAgentRuntimeTest.test_gh_credential_stores_report_present_missing_and_bad_mode)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tmp/claude-1000/-home-moriya-Workspace-dotfiles--claude-worktrees-worker-c/79f0f3c0-a708-4c6f-affe-0d87fcc6ba5a/scratchpad/t103-base/tests/unit/test_check_agent_runtime.py", line 984, in test_gh_credential_stores_report_present_missing_and_bad_mode
    findings = self.module.gh_credential_store_findings(home=home, env_path=env_path, gh=gh)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: module 'check_agent_runtime' has no attribute 'gh_credential_store_findings'

======================================================================
ERROR: test_gh_credential_stores_warn_on_two_logins_a_failed_status_or_no_gh (tests.unit.test_check_agent_runtime.CheckAgentRuntimeTest.test_gh_credential_stores_warn_on_two_logins_a_failed_status_or_no_gh)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tmp/claude-1000/-home-moriya-Workspace-dotfiles--claude-worktrees-worker-c/79f0f3c0-a708-4c6f-affe-0d87fcc6ba5a/scratchpad/t103-base/tests/unit/test_check_agent_runtime.py", line 1007, in test_gh_credential_stores_warn_on_two_logins_a_failed_status_or_no_gh
    findings = self.module.gh_credential_store_findings(home=home, env_path=env_path, gh=gh)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: module 'check_agent_runtime' has no attribute 'gh_credential_store_findings'

======================================================================
FAIL: test_gh_credential_stores_render_one_directory_per_account (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_gh_credential_stores_render_one_directory_per_account)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tmp/claude-1000/-home-moriya-Workspace-dotfiles--claude-worktrees-worker-c/79f0f3c0-a708-4c6f-affe-0d87fcc6ba5a/scratchpad/t103-base/tests/unit/test_generate_agent_configs.py", line 1346, in test_gh_credential_stores_render_one_directory_per_account
    self.assertEqual(rendered_stores(), list(defaults.values()))
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: Lists differ: ['', '', '~/.config/gh-worker'] != ['~/.config/gh', '~/.config/gh-work', '~/.config/gh-worker']

First differing element 0:
''
'~/.config/gh'

- ['', '', '~/.config/gh-worker']
+ ['~/.config/gh', '~/.config/gh-work', '~/.config/gh-worker']

----------------------------------------------------------------------
Ran 5 tests in 0.016s

FAILED (failures=1, errors=4)
exit=1
```

## crit status (no review file on this branch, hence the subagent review evidence)

```
$ crit status --json
{
  "branch": "feat/gh-auth-stores",
  "daemon": {
    "running": false
  },
  "review_file": "~/.crit/reviews/88fb2027d272/review.json",
  "review_file_exists": false,
  "sessions": [],
  "vcs": "git"
}

exit=0
```

## CompactionDB (main checkout; command exactly as executed, the returned id and a readback)

```
$ cd <main checkout> && uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dotfiles-T103 (operator 2026-10-05): GitHub credentials are one store per account, prompted for only in the interactive operator phase (`setup.sh`, `make gh-auth`); `make update` never prompts; chezmoi-private encrypted `hosts.yml` files make the prompt a no-op.'
ba9aa377-1bb6-4a41-898a-5fe622684558
exit=0
$ uv run --no-project .claude/hooks/contextdb_cli.py memory search dotfiles-T103
ba9aa377-1bb6-4a41-898a-5fe622684558 [project/decision] dotfiles-T103 (operator 2026-10-05): GitHub credentials are one store per account, prompted for only in the interactive operator phase (`setup.sh`, `make gh-auth`); `make update` never prompts; chezmoi-private encrypted `hosts.yml` files make the prompt a no-op.
exit=0
```

## CI on the first head bb9e92ed

```
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37380616474/job/112001338537	
build (client)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37380616473/job/112001338529	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415730	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001338758	
private-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339065	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339173	
private-bootstrap (ubuntu-24.04, server)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339037	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415737	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339210	
changes	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001339117	
private-bootstrap (ubuntu-24.04, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339211	
build (server)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37380616473/job/112001339001	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415651	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415613	
validate	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616478/job/112001337949	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37380616474/job/112001338537	
build (client)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37380616473/job/112001338529	
build (server)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37380616473/job/112001339001	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001338758	
private-bootstrap (macos-14, client)	pass	14s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339065	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415730	
changes	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001339117	
private-bootstrap (ubuntu-24.04, server)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339037	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339210	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415651	
private-bootstrap (ubuntu-24.04, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339211	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339173	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415737	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415613	
validate	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616478/job/112001337949	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37380616474/job/112001338537	
build (client)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37380616473/job/112001338529	
build (server)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37380616473/job/112001339001	
changes	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001339117	
private-bootstrap (macos-14, client)	pass	14s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339065	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001338758	
private-bootstrap (ubuntu-24.04, server)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339037	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339173	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339210	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415730	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415613	
private-bootstrap (ubuntu-24.04, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339211	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415651	
validate	pass	1m21s	https://github.com/mryfmo/dotfiles/actions/runs/37380616478/job/112001337949	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415737	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37380616474/job/112001338537	
build (client)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37380616473/job/112001338529	
build (server)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37380616473/job/112001339001	
changes	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001339117	
private-bootstrap (macos-14, client)	pass	14s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339065	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001338758	
private-bootstrap (ubuntu-24.04, server)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339037	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339173	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339210	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415730	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415613	
private-bootstrap (ubuntu-24.04, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339211	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415651	
validate	pass	1m21s	https://github.com/mryfmo/dotfiles/actions/runs/37380616478/job/112001337949	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415737	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37380616474/job/112001338537	
build (client)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37380616473/job/112001338529	
build (server)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37380616473/job/112001339001	
changes	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001339117	
private-bootstrap (macos-14, client)	pass	14s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339065	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001338758	
private-bootstrap (ubuntu-24.04, server)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339037	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339173	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339210	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415730	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415613	
private-bootstrap (ubuntu-24.04, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339211	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415651	
validate	pass	1m21s	https://github.com/mryfmo/dotfiles/actions/runs/37380616478/job/112001337949	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415737	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37380616474/job/112001338537	
build (client)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37380616473/job/112001338529	
build (server)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37380616473/job/112001339001	
changes	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001339117	
private-bootstrap (macos-14, client)	pass	14s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339065	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001338758	
private-bootstrap (ubuntu-24.04, server)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339037	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339173	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339210	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415730	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415613	
private-bootstrap (ubuntu-24.04, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339211	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415651	
validate	pass	1m21s	https://github.com/mryfmo/dotfiles/actions/runs/37380616478/job/112001337949	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415737	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37380616474/job/112001338537	
build (client)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37380616473/job/112001338529	
build (server)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37380616473/job/112001339001	
changes	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001339117	
private-bootstrap (macos-14, client)	pass	14s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339065	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001338758	
private-bootstrap (ubuntu-24.04, server)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339037	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339173	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339210	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415730	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415613	
private-bootstrap (ubuntu-24.04, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339211	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415651	
validate	pass	1m21s	https://github.com/mryfmo/dotfiles/actions/runs/37380616478/job/112001337949	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415737	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37380616474/job/112001338537	
build (client)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37380616473/job/112001338529	
build (server)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37380616473/job/112001339001	
changes	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001339117	
private-bootstrap (macos-14, client)	pass	14s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339065	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001338758	
private-bootstrap (ubuntu-24.04, server)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339037	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339173	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339210	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415730	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415613	
private-bootstrap (ubuntu-24.04, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339211	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415651	
validate	pass	1m21s	https://github.com/mryfmo/dotfiles/actions/runs/37380616478/job/112001337949	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415737	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37380616474/job/112001338537	
build (client)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37380616473/job/112001338529	
build (server)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37380616473/job/112001339001	
changes	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001339117	
private-bootstrap (macos-14, client)	pass	14s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339065	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001338758	
private-bootstrap (ubuntu-24.04, server)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339037	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339173	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339210	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415730	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415613	
private-bootstrap (ubuntu-24.04, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339211	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415651	
validate	pass	1m21s	https://github.com/mryfmo/dotfiles/actions/runs/37380616478/job/112001337949	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415737	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37380616474/job/112001338537	
build (client)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37380616473/job/112001338529	
build (server)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37380616473/job/112001339001	
changes	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001339117	
private-bootstrap (macos-14, client)	pass	14s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339065	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001338758	
private-bootstrap (ubuntu-24.04, server)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339037	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339173	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339210	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415730	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415613	
private-bootstrap (ubuntu-24.04, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339211	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415651	
validate	pass	1m21s	https://github.com/mryfmo/dotfiles/actions/runs/37380616478/job/112001337949	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415737	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37380616474/job/112001338537	
build (client)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37380616473/job/112001338529	
build (server)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37380616473/job/112001339001	
changes	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001339117	
private-bootstrap (macos-14, client)	pass	14s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339065	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001338758	
private-bootstrap (ubuntu-24.04, server)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339037	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339173	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339210	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415730	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415613	
private-bootstrap (ubuntu-24.04, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339211	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415651	
validate	pass	1m21s	https://github.com/mryfmo/dotfiles/actions/runs/37380616478/job/112001337949	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415737	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37380616474/job/112001338537	
build (client)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37380616473/job/112001338529	
build (server)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37380616473/job/112001339001	
changes	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001339117	
private-bootstrap (macos-14, client)	pass	14s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339065	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001338758	
private-bootstrap (ubuntu-24.04, server)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339037	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339173	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339210	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415730	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415613	
private-bootstrap (ubuntu-24.04, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339211	
test (ubuntu-24.04, server)	pass	5m35s	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415651	
validate	pass	1m21s	https://github.com/mryfmo/dotfiles/actions/runs/37380616478/job/112001337949	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415737	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37380616474/job/112001338537	
build (client)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37380616473/job/112001338529	
build (server)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37380616473/job/112001339001	
changes	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001339117	
private-bootstrap (macos-14, client)	pass	14s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339065	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001338758	
private-bootstrap (ubuntu-24.04, server)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339037	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415613	
public-bootstrap (ubuntu-24.04, server)	pass	6m2s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339210	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339173	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415730	
private-bootstrap (ubuntu-24.04, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339211	
test (ubuntu-24.04, server)	pass	5m35s	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415651	
validate	pass	1m21s	https://github.com/mryfmo/dotfiles/actions/runs/37380616478/job/112001337949	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415737	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37380616474/job/112001338537	
build (client)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37380616473/job/112001338529	
build (server)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37380616473/job/112001339001	
changes	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001339117	
private-bootstrap (macos-14, client)	pass	14s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339065	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001338758	
private-bootstrap (ubuntu-24.04, server)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339037	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415613	
public-bootstrap (ubuntu-24.04, server)	pass	6m2s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339210	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339173	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415730	
private-bootstrap (ubuntu-24.04, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339211	
test (ubuntu-24.04, server)	pass	5m35s	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415651	
validate	pass	1m21s	https://github.com/mryfmo/dotfiles/actions/runs/37380616478/job/112001337949	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415737	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37380616474/job/112001338537	
build (client)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37380616473/job/112001338529	
build (server)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37380616473/job/112001339001	
changes	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001339117	
private-bootstrap (macos-14, client)	pass	14s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339065	
private-bootstrap (ubuntu-24.04, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339211	
private-bootstrap (ubuntu-24.04, server)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339037	
public-bootstrap (ubuntu-24.04, server)	pass	6m2s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339210	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415730	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415613	
test (ubuntu-24.04, server)	pass	5m35s	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415651	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001338758	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339173	
test (macos-14, client)	pass	6m58s	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415737	
validate	pass	1m21s	https://github.com/mryfmo/dotfiles/actions/runs/37380616478/job/112001337949	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37380616474/job/112001338537	
build (client)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37380616473/job/112001338529	
build (server)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37380616473/job/112001339001	
changes	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001339117	
private-bootstrap (macos-14, client)	pass	14s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339065	
private-bootstrap (ubuntu-24.04, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339211	
private-bootstrap (ubuntu-24.04, server)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339037	
public-bootstrap (ubuntu-24.04, server)	pass	6m2s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339210	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415730	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415613	
test (ubuntu-24.04, server)	pass	5m35s	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415651	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001338758	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339173	
test (macos-14, client)	pass	6m58s	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415737	
validate	pass	1m21s	https://github.com/mryfmo/dotfiles/actions/runs/37380616478/job/112001337949	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37380616474/job/112001338537	
build (client)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37380616473/job/112001338529	
build (server)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37380616473/job/112001339001	
changes	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001339117	
private-bootstrap (macos-14, client)	pass	14s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339065	
private-bootstrap (ubuntu-24.04, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339211	
private-bootstrap (ubuntu-24.04, server)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339037	
public-bootstrap (ubuntu-24.04, server)	pass	6m2s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339210	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415730	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415613	
test (ubuntu-24.04, server)	pass	5m35s	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415651	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001338758	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339173	
test (macos-14, client)	pass	6m58s	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415737	
validate	pass	1m21s	https://github.com/mryfmo/dotfiles/actions/runs/37380616478/job/112001337949	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37380616474/job/112001338537	
build (client)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37380616473/job/112001338529	
build (server)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37380616473/job/112001339001	
changes	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001339117	
private-bootstrap (macos-14, client)	pass	14s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339065	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001338758	
private-bootstrap (ubuntu-24.04, server)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339037	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415613	
private-bootstrap (ubuntu-24.04, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339211	
public-bootstrap (ubuntu-24.04, server)	pass	6m2s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339210	
test (ubuntu-24.04, client)	pass	8m39s	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415730	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339173	
test (macos-14, client)	pass	6m58s	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415737	
test (ubuntu-24.04, server)	pass	5m35s	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415651	
validate	pass	1m21s	https://github.com/mryfmo/dotfiles/actions/runs/37380616478/job/112001337949	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37380616474/job/112001338537	
build (client)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37380616473/job/112001338529	
build (server)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37380616473/job/112001339001	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001338758	
changes	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001339117	
private-bootstrap (macos-14, client)	pass	14s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339065	
private-bootstrap (ubuntu-24.04, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339211	
private-bootstrap (ubuntu-24.04, server)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339037	
public-bootstrap (ubuntu-24.04, client)	pass	9m3s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339173	
public-bootstrap (ubuntu-24.04, server)	pass	6m2s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339210	
test (macos-14, client)	pass	6m58s	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415737	
test (ubuntu-24.04, client)	pass	8m39s	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415730	
test (ubuntu-24.04, server)	pass	5m35s	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415651	
test (ubuntu-26.04, client)	pass	8m59s	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415613	
validate	pass	1m21s	https://github.com/mryfmo/dotfiles/actions/runs/37380616478/job/112001337949	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37380616474/job/112001338537	
build (client)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37380616473/job/112001338529	
build (server)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37380616473/job/112001339001	
changes	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001339117	
private-bootstrap (macos-14, client)	pass	14s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339065	
private-bootstrap (ubuntu-24.04, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339211	
private-bootstrap (ubuntu-24.04, server)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339037	
public-bootstrap (macos-14, client)	pass	9m44s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001338758	
public-bootstrap (ubuntu-24.04, client)	pass	9m3s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339173	
public-bootstrap (ubuntu-24.04, server)	pass	6m2s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339210	
test (macos-14, client)	pass	6m58s	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415737	
test (ubuntu-24.04, client)	pass	8m39s	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415730	
test (ubuntu-24.04, server)	pass	5m35s	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415651	
test (ubuntu-26.04, client)	pass	8m59s	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415613	
validate	pass	1m21s	https://github.com/mryfmo/dotfiles/actions/runs/37380616478/job/112001337949	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37380616474/job/112001338537	
build (client)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37380616473/job/112001338529	
build (server)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37380616473/job/112001339001	
changes	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001339117	
private-bootstrap (macos-14, client)	pass	14s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339065	
private-bootstrap (ubuntu-24.04, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339211	
private-bootstrap (ubuntu-24.04, server)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339037	
public-bootstrap (macos-14, client)	pass	9m44s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001338758	
public-bootstrap (ubuntu-24.04, client)	pass	9m3s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339173	
public-bootstrap (ubuntu-24.04, server)	pass	6m2s	https://github.com/mryfmo/dotfiles/actions/runs/37380616538/job/112001339210	
test (macos-14, client)	pass	6m58s	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415737	
test (ubuntu-24.04, client)	pass	8m39s	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415730	
test (ubuntu-24.04, server)	pass	5m35s	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415651	
test (ubuntu-26.04, client)	pass	8m59s	https://github.com/mryfmo/dotfiles/actions/runs/37380616658/job/112001415613	
validate	pass	1m21s	https://github.com/mryfmo/dotfiles/actions/runs/37380616478/job/112001337949	
watch exit=0
```

## CI, mergeable state and Bot wait on the final head 0a28eb74 (cutoff `2026-10-05T22:34:07Z`, set before the push)

```
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37383310726/job/112010405665	
build (client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37383310943/job/112010407120	
build (server)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37383310943/job/112010406731	
private-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406100	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406290	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491861	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406374	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406249	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010492025	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491997	
private-bootstrap (ubuntu-24.04, server)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406259	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406339	
validate	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310737/job/112010405709	
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010406507	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491907	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37383310726/job/112010405665	
build (client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37383310943/job/112010407120	
build (server)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37383310943/job/112010406731	
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010406507	
private-bootstrap (macos-14, client)	pass	14s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406100	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406374	
private-bootstrap (ubuntu-24.04, server)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406259	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406290	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406249	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406339	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491861	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010492025	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491907	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491997	
validate	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310737/job/112010405709	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37383310726/job/112010405665	
build (client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37383310943/job/112010407120	
build (server)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37383310943/job/112010406731	
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010406507	
private-bootstrap (macos-14, client)	pass	14s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406100	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406374	
private-bootstrap (ubuntu-24.04, server)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406259	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406290	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406249	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406339	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491861	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010492025	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491907	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491997	
validate	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310737/job/112010405709	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37383310726/job/112010405665	
build (client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37383310943/job/112010407120	
build (server)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37383310943/job/112010406731	
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010406507	
private-bootstrap (macos-14, client)	pass	14s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406100	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406374	
private-bootstrap (ubuntu-24.04, server)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406259	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406290	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406249	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406339	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491861	
validate	pass	1m21s	https://github.com/mryfmo/dotfiles/actions/runs/37383310737/job/112010405709	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010492025	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491907	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491997	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37383310726/job/112010405665	
build (client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37383310943/job/112010407120	
build (server)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37383310943/job/112010406731	
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010406507	
private-bootstrap (macos-14, client)	pass	14s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406100	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406374	
private-bootstrap (ubuntu-24.04, server)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406259	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406290	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406249	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406339	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491861	
validate	pass	1m21s	https://github.com/mryfmo/dotfiles/actions/runs/37383310737/job/112010405709	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010492025	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491907	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491997	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37383310726/job/112010405665	
build (client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37383310943/job/112010407120	
build (server)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37383310943/job/112010406731	
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010406507	
private-bootstrap (macos-14, client)	pass	14s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406100	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406374	
private-bootstrap (ubuntu-24.04, server)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406259	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406290	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406249	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406339	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491861	
validate	pass	1m21s	https://github.com/mryfmo/dotfiles/actions/runs/37383310737/job/112010405709	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010492025	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491907	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491997	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37383310726/job/112010405665	
build (client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37383310943/job/112010407120	
build (server)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37383310943/job/112010406731	
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010406507	
private-bootstrap (macos-14, client)	pass	14s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406100	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406374	
private-bootstrap (ubuntu-24.04, server)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406259	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406290	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406249	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406339	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491861	
validate	pass	1m21s	https://github.com/mryfmo/dotfiles/actions/runs/37383310737/job/112010405709	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010492025	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491907	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491997	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37383310726/job/112010405665	
build (client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37383310943/job/112010407120	
build (server)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37383310943/job/112010406731	
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010406507	
private-bootstrap (macos-14, client)	pass	14s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406100	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406374	
private-bootstrap (ubuntu-24.04, server)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406259	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406290	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406249	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406339	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491861	
validate	pass	1m21s	https://github.com/mryfmo/dotfiles/actions/runs/37383310737/job/112010405709	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010492025	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491907	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491997	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37383310726/job/112010405665	
build (client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37383310943/job/112010407120	
build (server)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37383310943/job/112010406731	
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010406507	
private-bootstrap (macos-14, client)	pass	14s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406100	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406374	
private-bootstrap (ubuntu-24.04, server)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406259	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406290	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406249	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406339	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491861	
validate	pass	1m21s	https://github.com/mryfmo/dotfiles/actions/runs/37383310737/job/112010405709	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010492025	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491907	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491997	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37383310726/job/112010405665	
build (client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37383310943/job/112010407120	
build (server)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37383310943/job/112010406731	
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010406507	
private-bootstrap (macos-14, client)	pass	14s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406100	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406374	
private-bootstrap (ubuntu-24.04, server)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406259	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406290	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406249	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406339	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491861	
validate	pass	1m21s	https://github.com/mryfmo/dotfiles/actions/runs/37383310737/job/112010405709	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010492025	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491907	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491997	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37383310726/job/112010405665	
build (client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37383310943/job/112010407120	
build (server)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37383310943/job/112010406731	
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010406507	
private-bootstrap (macos-14, client)	pass	14s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406100	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406290	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406339	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491861	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406374	
private-bootstrap (ubuntu-24.04, server)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406259	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406249	
test (ubuntu-24.04, server)	pass	4m51s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491907	
validate	pass	1m21s	https://github.com/mryfmo/dotfiles/actions/runs/37383310737/job/112010405709	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010492025	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491997	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37383310726/job/112010405665	
build (client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37383310943/job/112010407120	
build (server)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37383310943/job/112010406731	
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010406507	
private-bootstrap (macos-14, client)	pass	14s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406100	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406290	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406339	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491861	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406374	
private-bootstrap (ubuntu-24.04, server)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406259	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406249	
test (ubuntu-24.04, server)	pass	4m51s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491907	
validate	pass	1m21s	https://github.com/mryfmo/dotfiles/actions/runs/37383310737/job/112010405709	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010492025	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491997	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37383310726/job/112010405665	
build (client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37383310943/job/112010407120	
build (server)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37383310943/job/112010406731	
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010406507	
private-bootstrap (macos-14, client)	pass	14s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406100	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406290	
public-bootstrap (ubuntu-24.04, server)	pass	6m21s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406339	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491861	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406374	
private-bootstrap (ubuntu-24.04, server)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406259	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406249	
test (ubuntu-24.04, server)	pass	4m51s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491907	
validate	pass	1m21s	https://github.com/mryfmo/dotfiles/actions/runs/37383310737/job/112010405709	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010492025	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491997	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37383310726/job/112010405665	
build (client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37383310943/job/112010407120	
build (server)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37383310943/job/112010406731	
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010406507	
private-bootstrap (macos-14, client)	pass	14s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406100	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406290	
public-bootstrap (ubuntu-24.04, server)	pass	6m21s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406339	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491861	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406374	
private-bootstrap (ubuntu-24.04, server)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406259	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406249	
test (ubuntu-24.04, server)	pass	4m51s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491907	
validate	pass	1m21s	https://github.com/mryfmo/dotfiles/actions/runs/37383310737/job/112010405709	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010492025	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491997	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37383310726/job/112010405665	
build (client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37383310943/job/112010407120	
build (server)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37383310943/job/112010406731	
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010406507	
private-bootstrap (macos-14, client)	pass	14s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406100	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406290	
public-bootstrap (ubuntu-24.04, server)	pass	6m21s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406339	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491861	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406374	
private-bootstrap (ubuntu-24.04, server)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406259	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406249	
test (ubuntu-24.04, server)	pass	4m51s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491907	
validate	pass	1m21s	https://github.com/mryfmo/dotfiles/actions/runs/37383310737/job/112010405709	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010492025	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491997	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37383310726/job/112010405665	
build (client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37383310943/job/112010407120	
build (server)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37383310943/job/112010406731	
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010406507	
private-bootstrap (macos-14, client)	pass	14s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406100	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406290	
public-bootstrap (ubuntu-24.04, server)	pass	6m21s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406339	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491861	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406374	
private-bootstrap (ubuntu-24.04, server)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406259	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406249	
test (ubuntu-24.04, server)	pass	4m51s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491907	
validate	pass	1m21s	https://github.com/mryfmo/dotfiles/actions/runs/37383310737/job/112010405709	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010492025	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491997	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37383310726/job/112010405665	
build (client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37383310943/job/112010407120	
build (server)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37383310943/job/112010406731	
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010406507	
private-bootstrap (macos-14, client)	pass	14s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406100	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406374	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406290	
private-bootstrap (ubuntu-24.04, server)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406259	
public-bootstrap (ubuntu-24.04, server)	pass	6m21s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406339	
test (macos-14, client)	pass	7m53s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491861	
test (ubuntu-24.04, client)	pass	7m59s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010492025	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406249	
test (ubuntu-24.04, server)	pass	4m51s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491907	
validate	pass	1m21s	https://github.com/mryfmo/dotfiles/actions/runs/37383310737/job/112010405709	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491997	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37383310726/job/112010405665	
build (client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37383310943/job/112010407120	
build (server)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37383310943/job/112010406731	
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010406507	
private-bootstrap (macos-14, client)	pass	14s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406100	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406374	
private-bootstrap (ubuntu-24.04, server)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406259	
public-bootstrap (macos-14, client)	pass	8m36s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406290	
public-bootstrap (ubuntu-24.04, server)	pass	6m21s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406339	
test (macos-14, client)	pass	7m53s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491861	
test (ubuntu-24.04, client)	pass	7m59s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010492025	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406249	
test (ubuntu-24.04, server)	pass	4m51s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491907	
validate	pass	1m21s	https://github.com/mryfmo/dotfiles/actions/runs/37383310737/job/112010405709	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491997	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37383310726/job/112010405665	
build (client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37383310943/job/112010407120	
build (server)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37383310943/job/112010406731	
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010406507	
private-bootstrap (macos-14, client)	pass	14s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406100	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406374	
private-bootstrap (ubuntu-24.04, server)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406259	
public-bootstrap (macos-14, client)	pass	8m36s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406290	
public-bootstrap (ubuntu-24.04, client)	pass	9m24s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406249	
public-bootstrap (ubuntu-24.04, server)	pass	6m21s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406339	
test (macos-14, client)	pass	7m53s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491861	
test (ubuntu-24.04, client)	pass	7m59s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010492025	
test (ubuntu-24.04, server)	pass	4m51s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491907	
validate	pass	1m21s	https://github.com/mryfmo/dotfiles/actions/runs/37383310737/job/112010405709	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491997	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37383310726/job/112010405665	
build (client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37383310943/job/112010407120	
build (server)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37383310943/job/112010406731	
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010406507	
private-bootstrap (macos-14, client)	pass	14s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406100	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406374	
private-bootstrap (ubuntu-24.04, server)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406259	
public-bootstrap (macos-14, client)	pass	8m36s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406290	
public-bootstrap (ubuntu-24.04, client)	pass	9m24s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406249	
public-bootstrap (ubuntu-24.04, server)	pass	6m21s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406339	
test (macos-14, client)	pass	7m53s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491861	
test (ubuntu-24.04, client)	pass	7m59s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010492025	
test (ubuntu-24.04, server)	pass	4m51s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491907	
test (ubuntu-26.04, client)	pass	9m26s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491997	
validate	pass	1m21s	https://github.com/mryfmo/dotfiles/actions/runs/37383310737/job/112010405709	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37383310726/job/112010405665	
build (client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37383310943/job/112010407120	
build (server)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37383310943/job/112010406731	
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010406507	
private-bootstrap (macos-14, client)	pass	14s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406100	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406374	
private-bootstrap (ubuntu-24.04, server)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406259	
public-bootstrap (macos-14, client)	pass	8m36s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406290	
public-bootstrap (ubuntu-24.04, client)	pass	9m24s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406249	
public-bootstrap (ubuntu-24.04, server)	pass	6m21s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406339	
test (macos-14, client)	pass	7m53s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491861	
test (ubuntu-24.04, client)	pass	7m59s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010492025	
test (ubuntu-24.04, server)	pass	4m51s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491907	
test (ubuntu-26.04, client)	pass	9m26s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491997	
validate	pass	1m21s	https://github.com/mryfmo/dotfiles/actions/runs/37383310737/job/112010405709	
watch exit=0
```

```
$ gh pr checks 288
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37383310726/job/112010405665	
build (client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37383310943/job/112010407120	
build (server)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37383310943/job/112010406731	
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010406507	
private-bootstrap (macos-14, client)	pass	14s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406100	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406374	
private-bootstrap (ubuntu-24.04, server)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406259	
public-bootstrap (macos-14, client)	pass	8m36s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406290	
public-bootstrap (ubuntu-24.04, client)	pass	9m24s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406249	
public-bootstrap (ubuntu-24.04, server)	pass	6m21s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406339	
test (macos-14, client)	pass	7m53s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491861	
test (ubuntu-24.04, client)	pass	7m59s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010492025	
test (ubuntu-24.04, server)	pass	4m51s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491907	
test (ubuntu-26.04, client)	pass	9m26s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491997	
validate	pass	1m21s	https://github.com/mryfmo/dotfiles/actions/runs/37383310737/job/112010405709	
exit=0
```

```
$ gh api repos/mryfmo/dotfiles/pulls/288 --jq '.mergeable_state'
blocked
exit=0
```

The PR is `blocked` because one review thread is unresolved: the Bot security review below. The approval count is 0, and all checks pass.

```
start 2026-10-05T22:44:18Z head=0a28eb74c3f921b254011f1d4cde667ada2e30a3 quota_cutoff=2026-10-05T22:34:07Z
poll 1 2026-10-05T22:44:20Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 2 2026-10-05T22:44:51Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 3 2026-10-05T22:45:23Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 4 2026-10-05T22:45:54Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 5 2026-10-05T22:46:25Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 6 2026-10-05T22:46:57Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 7 2026-10-05T22:47:28Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 8 2026-10-05T22:48:00Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 9 2026-10-05T22:48:31Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 10 2026-10-05T22:49:02Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 11 2026-10-05T22:49:34Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 12 2026-10-05T22:50:05Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 13 2026-10-05T22:50:37Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 14 2026-10-05T22:51:08Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 15 2026-10-05T22:51:40Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 16 2026-10-05T22:52:11Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 17 2026-10-05T22:52:42Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 18 2026-10-05T22:53:14Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 19 2026-10-05T22:53:45Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 20 2026-10-05T22:54:17Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 21 2026-10-05T22:54:48Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 22 2026-10-05T22:55:19Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 23 2026-10-05T22:55:51Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 24 2026-10-05T22:56:22Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 25 2026-10-05T22:56:54Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 26 2026-10-05T22:57:25Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 27 2026-10-05T22:57:56Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 28 2026-10-05T22:58:28Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 29 2026-10-05T22:58:59Z bot_reviews=0 bot_comments=0 quota_notices=0
end 2026-10-05T22:59:29Z
```

## Bot items on PR 288 (all heads), swept after the wait

```
$ gh api --paginate repos/mryfmo/dotfiles/pulls/288/reviews --jq '[.[]|select(.user.type=="Bot")|{id,commit_id,submitted_at}]'
[
{
"commit_id": "bb9e92ed17f7f8966a43ed5c60982dc97da58c19",
"id": 5421306432,
"submitted_at": "2026-10-05T22:19:35Z"
}
]
$ gh api --paginate repos/mryfmo/dotfiles/pulls/288/comments --jq '[.[]|select(.user.type=="Bot" and .in_reply_to_id==null)|{id,original_commit_id,path,line,created_at}]'
[
{
"created_at": "2026-10-05T22:19:35Z",
"id": 4189443339,
"line": 45,
"original_commit_id": "bb9e92ed17f7f8966a43ed5c60982dc97da58c19",
"path": "scripts/gh-auth-stores.sh"
}
]
$ gh api --paginate repos/mryfmo/dotfiles/issues/288/comments --jq '.[]|select(.user.type=="Bot")|"\(.id) \(.created_at) \(.body[0:100]|gsub("\n";" "))"'
6004109337 2026-10-05T22:09:21Z Codex usage limits have been reached for code reviews. Please check with the admins of this repo to 
6004110958 2026-10-05T22:09:27Z <!-- This is an auto-generated comment: summarize by coderabbit.ai --> <!-- This is an auto-generate
$ gh pr checks 288
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37383310726/job/112010405665	
build (client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37383310943/job/112010407120	
build (server)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37383310943/job/112010406731	
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010406507	
private-bootstrap (macos-14, client)	pass	14s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406100	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406374	
private-bootstrap (ubuntu-24.04, server)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406259	
public-bootstrap (macos-14, client)	pass	8m36s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406290	
public-bootstrap (ubuntu-24.04, client)	pass	9m24s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406249	
public-bootstrap (ubuntu-24.04, server)	pass	6m21s	https://github.com/mryfmo/dotfiles/actions/runs/37383310730/job/112010406339	
test (macos-14, client)	pass	7m53s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491861	
test (ubuntu-24.04, client)	pass	7m59s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010492025	
test (ubuntu-24.04, server)	pass	4m51s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491907	
test (ubuntu-26.04, client)	pass	9m26s	https://github.com/mryfmo/dotfiles/actions/runs/37383310782/job/112010491997	
validate	pass	1m21s	https://github.com/mryfmo/dotfiles/actions/runs/37383310737/job/112010405709	
exit=0
```

- **The Bot security review:** review 5421306432 at 22:19:35Z, with its inline P1 thread 4189443339 on `scripts/gh-auth-stores.sh:45`. It was posted on the first head `bb9e92ed`. The final-head loop counted only items on `0a28eb74`, so it found it through `mergeable_state` and this sweep.
- **Its disposition:** reported by PONG (message after 22:59Z). Per PONG decision 2, file storage for every store is the operator's decision. The orchestrator replies `not-applicable` and resolves the thread; this seat does not touch it.
- **Quota notice:** the Codex quota notice at 22:09:21Z came when the PR opened, on `bb9e92ed`.
- **Final head:** no Bot review, inline comment or quota notice exists for `0a28eb74`.

## Revise round 1 (task_rev `sha256:a7f207f019ec83995c4e49b649448926937346928c44338606d046501c03fa70`)

Final head `a41a56bd2b3b93c3432db647df1af39196762211`. Pushed after the quota cutoff `2026-10-05T23:28:27Z`. `main` is unchanged at `2d0ef943`.

### The round-1 tests on the previous head (0a28eb74)

The transcript first pasted here ended `FAILED (failures=4)` followed by `exit=0`. That `exit=0` was the status of a `grep` that filtered the test output, not of the tests. The wrapper that was actually run, verbatim:

```bash
{ echo '$ (scratch worktree at the previous head 0a28eb74, with the round-1 test files copied in) uv run --no-project python -m unittest <the four round-1 tests>'; (cd $W && uv run --no-project python -m unittest <the four round-1 tests> 2>&1 | grep -vE '^ERROR: (owner_|work_|worker_)'); echo "exit=$?"; } > $O 2>&1
```

Re-run in revise round 2 without the filter, so the pasted status is the test process's own. The test files are taken from `a41a56bd` with `git show`, the same content that was copied the first time:

```
$ git worktree add --detach <scratch> 0a28eb74
$ for f in test_gh_auth_stores.py test_check_agent_runtime.py test_generate_agent_configs.py; do git show "a41a56bd:tests/unit/$f" > "<scratch>/tests/unit/$f"; done
$ (cd <scratch> && timeout 120 uv run --no-project python -m unittest tests.unit.test_gh_auth_stores.GhAuthStoresTest.test_setup_finds_a_mise_installed_gh_on_a_fresh_path tests.unit.test_gh_auth_stores.GhAuthStoresTest.test_without_a_terminal_it_never_prompts tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_gh_credential_stores_render_one_directory_per_account tests.unit.test_check_agent_runtime.CheckAgentRuntimeTest.test_gh_credential_stores_report_present_missing_and_bad_mode 2>&1); echo "test exit=$?"
FFERROR: owner_gh_config_dir must be an absolute or ~/ path without control characters
ERROR: owner_gh_config_dir must be an absolute or ~/ path without control characters
ERROR: owner_gh_config_dir must be an absolute or ~/ path without control characters
ERROR: owner_gh_config_dir must be an absolute or ~/ path without control characters
ERROR: work_gh_config_dir must be an absolute or ~/ path without control characters
ERROR: work_gh_config_dir must be an absolute or ~/ path without control characters
ERROR: work_gh_config_dir must be an absolute or ~/ path without control characters
ERROR: work_gh_config_dir must be an absolute or ~/ path without control characters
ERROR: owner_gh_config_dir, work_gh_config_dir and worker_gh_config_dir must name different directories
FF
======================================================================
FAIL: test_setup_finds_a_mise_installed_gh_on_a_fresh_path (tests.unit.test_gh_auth_stores.GhAuthStoresTest.test_setup_finds_a_mise_installed_gh_on_a_fresh_path)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tmp/claude-1000/-home-moriya-Workspace-dotfiles--claude-worktrees-worker-c/79f0f3c0-a708-4c6f-affe-0d87fcc6ba5a/scratchpad/t103-r1-rerun/tests/unit/test_gh_auth_stores.py", line 122, in test_setup_finds_a_mise_installed_gh_on_a_fresh_path
    self.assertNotIn("Skipping the GitHub logins", result.stdout)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'Skipping the GitHub logins' unexpectedly found in 'Skipping the GitHub logins; run `make gh-auth` in the dotfiles checkout once gh is installed.\n'

======================================================================
FAIL: test_without_a_terminal_it_never_prompts (tests.unit.test_gh_auth_stores.GhAuthStoresTest.test_without_a_terminal_it_never_prompts)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tmp/claude-1000/-home-moriya-Workspace-dotfiles--claude-worktrees-worker-c/79f0f3c0-a708-4c6f-affe-0d87fcc6ba5a/scratchpad/t103-r1-rerun/tests/unit/test_gh_auth_stores.py", line 77, in test_without_a_terminal_it_never_prompts
    self.assertEqual(stat.S_IMODE(owner_hosts.stat().st_mode), 0o600)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 420 != 384

======================================================================
FAIL: test_gh_credential_stores_render_one_directory_per_account (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_gh_credential_stores_render_one_directory_per_account)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tmp/claude-1000/-home-moriya-Workspace-dotfiles--claude-worktrees-worker-c/79f0f3c0-a708-4c6f-affe-0d87fcc6ba5a/scratchpad/t103-r1-rerun/tests/unit/test_generate_agent_configs.py", line 1364, in test_gh_credential_stores_render_one_directory_per_account
    with mock.patch.dict(os.environ, {"HOME": "~"}), self.assertRaises(SystemExit):
                                                                 ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
AssertionError: SystemExit not raised

======================================================================
FAIL: test_gh_credential_stores_report_present_missing_and_bad_mode (tests.unit.test_check_agent_runtime.CheckAgentRuntimeTest.test_gh_credential_stores_report_present_missing_and_bad_mode)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tmp/claude-1000/-home-moriya-Workspace-dotfiles--claude-worktrees-worker-c/79f0f3c0-a708-4c6f-affe-0d87fcc6ba5a/scratchpad/t103-r1-rerun/tests/unit/test_check_agent_runtime.py", line 986, in test_gh_credential_stores_report_present_missing_and_bad_mode
    self.assertEqual(
    ~~~~~~~~~~~~~~~~^
        findings,
        ^^^^^^^^^
    ...<7 lines>...
        ],
        ^^
    )
    ^
AssertionError: Lists differ: ['fou[305 chars] 0600', 'WARN: GitHub worker credential store [42 chars]uth'] != ['fou[305 chars] 0600; run make gh-auth', 'WARN: GitHub worker[60 chars]uth']

First differing element 1:
'WARN[118 chars] be a user-owned regular file with mode 0600'
'WARN[118 chars] be a user-owned regular file with mode 0600; run make gh-auth'

  ['found: GitHub owner credential store '
   '/tmp/claude-1000/check-agent-runtime-test-oz_i9ab9/home/.config/gh '
   '(hosts.yml 0600, one user: owner-login)',
   'WARN: GitHub work credential store '
   '/tmp/claude-1000/check-agent-runtime-test-oz_i9ab9/home/.config/gh-work: '
-  'hosts.yml must be a user-owned regular file with mode 0600',
+  'hosts.yml must be a user-owned regular file with mode 0600; run make gh-auth',
?                                                             ++++++++++++++++++

   'WARN: GitHub worker credential store /abs/never has no hosts.yml; run make '
   'gh-auth']

----------------------------------------------------------------------
Ran 4 tests in 0.026s

FAILED (failures=4)
test exit=1
```

### Task validation commands on a41a56bd

```
$ git rev-parse HEAD
a41a56bd2b3b93c3432db647df1af39196762211
exit=0
```

```
$ bash -n setup.sh scripts/gh-auth-stores.sh; echo "rc=$?"
rc=0
exit=0
```

```
$ shellcheck setup.sh scripts/gh-auth-stores.sh; echo "rc=$?"
rc=0
exit=0
```

```
$ make render-check
uv run --with pyyaml scripts/generate-agent-configs.py --check
generated agent configs are up to date
exit=0
```

```
$ make unit-test 2>&1 | tail -3
Ran 916 tests in 224.155s

OK (skipped=1)
exit=0
```

```
$ uv run --no-project --with pyyaml scripts/validate-agent-assets.py; echo "rc=$?"
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/acceptance/dotfiles-T103-gh-auth-stores-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/autoskill/runs/dotfiles-T103-gh-auth-stores-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/learning/dotfiles-T103-gh-auth-stores-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/reports/dotfiles-T103-gh-auth-stores-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/sandboxes/dotfiles-T103-gh-auth-stores-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/tasks/dotfiles-T103-gh-auth-stores-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T103-gh-auth-stores-a01-audit-0a28eb7.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T103-gh-auth-stores-a01-audit-0a28eb7.md.last.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T103-gh-auth-stores-a01-crit.json
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T103-gh-auth-stores-a01-pr-feedback.json
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T103-gh-auth-stores-a01-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T103-gh-auth-stores-a01-worker-crit.json
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T103-gh-auth-stores-a01-worker-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T103-gh-auth-stores-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/github-auth-design-2026-10-05.md
agent asset validation ok
rc=0
exit=0
```

```
$ grep -n 'gh auth login' Makefile scripts/update-agent-assets.sh home/.chezmoiscripts 2>/dev/null; echo "rc=$? (expect no match outside the gh-auth target)"
rc=2 (expect no match outside the gh-auth target)
exit=0
```

```
$ grep -rn 'gh auth login' Makefile scripts/update-agent-assets.sh home/.chezmoiscripts; echo "rc=$?   # recursive form: home/.chezmoiscripts is a directory, which plain grep -n reports as an error (rc=2 above)"
rc=1   # recursive form: home/.chezmoiscripts is a directory, which plain grep -n reports as an error (rc=2 above)
exit=0
```

```
$ bash -n scripts/check-tools.sh && shellcheck scripts/check-tools.sh; echo "rc=$?"
rc=0
exit=0
```

```
$ git ls-files -z "*.py" | xargs -0 ruff format --config ruff.toml --check
44 files already formatted
exit=0
```

```
$ mise x node npm:prettier -- prettier --check README.md
[33mmise[0m [33mWARN[0m  tool purgatory cleanup failed: Read-only file system (os error 30)
Checking formatting...
All matched files use Prettier code style!
exit=0
```

```
$ bash /tmp/claude-1000/t103/ruff-scan.sh   # the script is pasted in the validation file
scripts/check-agent-runtime.py: 3 findings in the file, 0 on added lines
scripts/generate-agent-configs.py: 4 findings in the file, 0 on added lines
tests/unit/test_generate_agent_configs.py: 11 findings in the file, 0 on added lines
tests/unit/test_runtime_health.py: 19 findings in the file, 0 on added lines
tests/unit/test_gh_auth_stores.py: 0 findings in the file, 0 on added lines
tests/unit/test_check_agent_runtime.py: 7 findings in the file, 0 on added lines
exit=0
```

The ruff added-line scan script that the last block ran:

```bash
# ruff check findings on lines this branch adds (git diff -U0 origin/main hunks), per changed Python file
for f in scripts/check-agent-runtime.py scripts/generate-agent-configs.py tests/unit/test_generate_agent_configs.py tests/unit/test_runtime_health.py tests/unit/test_gh_auth_stores.py tests/unit/test_check_agent_runtime.py; do
  added=$(git diff -U0 origin/main -- "$f" | grep -o "^@@ [^@]*+[0-9,]*" | sed "s/.*+//")
  total=$(ruff check --config ruff.toml --output-format concise "$f" 2>/dev/null | sed -E "s/\x1b\[[0-9;]*m//g" | grep -cE "^[^ ]+:[0-9]+:")
  hits=$(ruff check --config ruff.toml --output-format concise "$f" 2>/dev/null | sed -E "s/\x1b\[[0-9;]*m//g" | grep -E "^[^ ]+:[0-9]+:" | while IFS=: read -r fp ln col rest; do for r in $added; do s=${r%,*}; c=${r#*,}; [ "$c" = "$r" ] && c=1; if [ "$ln" -ge "$s" ] && [ "$ln" -lt $((s + c)) ]; then echo "$fp:$ln:$col:$rest"; fi; done; done)
  printf '%s: %s findings in the file, %s on added lines\n' "$f" "$total" "$(printf '%s' "$hits" | grep -c .)"
  [ -z "$hits" ] || printf '%s\n' "$hits"
done
```

### CI, mergeable state and Bot wait on a41a56bd (`bot: none`; no quota notice after the cutoff)

```
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325241	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325519	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325433	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028373048	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028372954	
build	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37388694768/job/112028325708	
private-bootstrap (macos-14, client)	pass	13s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325492	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028373058	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build (server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37388694985/job/112028326566	
build (client)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37388694985/job/112028326365	
validate	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694611/job/112028325105	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028372967	
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028326415	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325564	
private-bootstrap (ubuntu-24.04, server)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325595	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325241	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325519	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325433	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028373048	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028372954	
build	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37388694768/job/112028325708	
private-bootstrap (macos-14, client)	pass	13s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325492	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028373058	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build (server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37388694985/job/112028326566	
build (client)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37388694985/job/112028326365	
validate	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694611/job/112028325105	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028372967	
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028326415	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325564	
private-bootstrap (ubuntu-24.04, server)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325595	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325241	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325519	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325433	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028373048	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028372954	
build	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37388694768/job/112028325708	
private-bootstrap (macos-14, client)	pass	13s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325492	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028373058	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build (server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37388694985/job/112028326566	
build (client)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37388694985/job/112028326365	
validate	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694611/job/112028325105	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028372967	
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028326415	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325564	
private-bootstrap (ubuntu-24.04, server)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325595	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325241	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325519	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325433	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028373048	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028372954	
build	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37388694768/job/112028325708	
private-bootstrap (macos-14, client)	pass	13s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325492	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028373058	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build (server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37388694985/job/112028326566	
build (client)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37388694985/job/112028326365	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028372967	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325564	
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028326415	
private-bootstrap (ubuntu-24.04, server)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325595	
validate	pass	1m22s	https://github.com/mryfmo/dotfiles/actions/runs/37388694611/job/112028325105	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325241	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325519	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325433	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028373048	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028372954	
build	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37388694768/job/112028325708	
private-bootstrap (macos-14, client)	pass	13s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325492	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028373058	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build (server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37388694985/job/112028326566	
build (client)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37388694985/job/112028326365	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028372967	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325564	
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028326415	
private-bootstrap (ubuntu-24.04, server)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325595	
validate	pass	1m22s	https://github.com/mryfmo/dotfiles/actions/runs/37388694611/job/112028325105	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325241	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325519	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325433	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028373048	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028372954	
build	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37388694768/job/112028325708	
private-bootstrap (macos-14, client)	pass	13s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325492	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028373058	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build (server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37388694985/job/112028326566	
build (client)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37388694985/job/112028326365	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028372967	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325564	
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028326415	
private-bootstrap (ubuntu-24.04, server)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325595	
validate	pass	1m22s	https://github.com/mryfmo/dotfiles/actions/runs/37388694611/job/112028325105	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325241	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325519	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325433	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028373048	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028372954	
build	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37388694768/job/112028325708	
private-bootstrap (macos-14, client)	pass	13s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325492	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028373058	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build (server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37388694985/job/112028326566	
build (client)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37388694985/job/112028326365	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028372967	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325564	
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028326415	
private-bootstrap (ubuntu-24.04, server)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325595	
validate	pass	1m22s	https://github.com/mryfmo/dotfiles/actions/runs/37388694611/job/112028325105	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325241	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325519	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325433	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028373048	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028372954	
build	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37388694768/job/112028325708	
private-bootstrap (macos-14, client)	pass	13s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325492	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028373058	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build (server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37388694985/job/112028326566	
build (client)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37388694985/job/112028326365	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028372967	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325564	
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028326415	
private-bootstrap (ubuntu-24.04, server)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325595	
validate	pass	1m22s	https://github.com/mryfmo/dotfiles/actions/runs/37388694611/job/112028325105	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325241	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325519	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325433	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028373048	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028372954	
build	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37388694768/job/112028325708	
private-bootstrap (macos-14, client)	pass	13s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325492	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028373058	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build (server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37388694985/job/112028326566	
build (client)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37388694985/job/112028326365	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028372967	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325564	
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028326415	
private-bootstrap (ubuntu-24.04, server)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325595	
validate	pass	1m22s	https://github.com/mryfmo/dotfiles/actions/runs/37388694611/job/112028325105	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325241	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325519	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325433	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028373048	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028372954	
build	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37388694768/job/112028325708	
private-bootstrap (macos-14, client)	pass	13s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325492	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028373058	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build (server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37388694985/job/112028326566	
build (client)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37388694985/job/112028326365	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028372967	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325564	
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028326415	
private-bootstrap (ubuntu-24.04, server)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325595	
validate	pass	1m22s	https://github.com/mryfmo/dotfiles/actions/runs/37388694611/job/112028325105	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325241	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325519	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325433	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028373058	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028372954	
build	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37388694768/job/112028325708	
private-bootstrap (macos-14, client)	pass	13s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325492	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build (client)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37388694985/job/112028326365	
build (server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37388694985/job/112028326566	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325564	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028372967	
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028326415	
private-bootstrap (ubuntu-24.04, server)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325595	
test (ubuntu-24.04, server)	pass	4m48s	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028373048	
validate	pass	1m22s	https://github.com/mryfmo/dotfiles/actions/runs/37388694611/job/112028325105	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325241	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325519	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325433	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028373058	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028372954	
build	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37388694768/job/112028325708	
private-bootstrap (macos-14, client)	pass	13s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325492	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build (client)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37388694985/job/112028326365	
build (server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37388694985/job/112028326566	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325564	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028372967	
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028326415	
private-bootstrap (ubuntu-24.04, server)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325595	
test (ubuntu-24.04, server)	pass	4m48s	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028373048	
validate	pass	1m22s	https://github.com/mryfmo/dotfiles/actions/runs/37388694611/job/112028325105	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325241	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325519	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325433	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028373058	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028372954	
build	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37388694768/job/112028325708	
private-bootstrap (macos-14, client)	pass	13s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325492	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build (client)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37388694985/job/112028326365	
build (server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37388694985/job/112028326566	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325564	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028372967	
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028326415	
private-bootstrap (ubuntu-24.04, server)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325595	
test (ubuntu-24.04, server)	pass	4m48s	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028373048	
validate	pass	1m22s	https://github.com/mryfmo/dotfiles/actions/runs/37388694611/job/112028325105	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325241	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325519	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325433	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028373058	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028372954	
build	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37388694768/job/112028325708	
private-bootstrap (macos-14, client)	pass	13s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325492	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build (client)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37388694985/job/112028326365	
build (server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37388694985/job/112028326566	
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028326415	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028372967	
private-bootstrap (ubuntu-24.04, server)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325595	
public-bootstrap (ubuntu-24.04, server)	pass	6m48s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325564	
test (ubuntu-24.04, server)	pass	4m48s	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028373048	
validate	pass	1m22s	https://github.com/mryfmo/dotfiles/actions/runs/37388694611/job/112028325105	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37388694768/job/112028325708	
build (client)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37388694985/job/112028326365	
build (server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37388694985/job/112028326566	
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028326415	
private-bootstrap (macos-14, client)	pass	13s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325492	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325433	
private-bootstrap (ubuntu-24.04, server)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325595	
public-bootstrap (ubuntu-24.04, client)	pass	7m14s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325519	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028373058	
validate	pass	1m22s	https://github.com/mryfmo/dotfiles/actions/runs/37388694611/job/112028325105	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325241	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028372967	
public-bootstrap (ubuntu-24.04, server)	pass	6m48s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325564	
test (ubuntu-24.04, server)	pass	4m48s	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028373048	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028372954	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37388694768/job/112028325708	
build (client)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37388694985/job/112028326365	
build (server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37388694985/job/112028326566	
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028326415	
private-bootstrap (macos-14, client)	pass	13s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325492	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325433	
test (macos-14, client)	pass	7m28s	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028372967	
test (ubuntu-24.04, server)	pass	4m48s	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028373048	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028372954	
private-bootstrap (ubuntu-24.04, server)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325595	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325241	
public-bootstrap (ubuntu-24.04, client)	pass	7m14s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325519	
public-bootstrap (ubuntu-24.04, server)	pass	6m48s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325564	
validate	pass	1m22s	https://github.com/mryfmo/dotfiles/actions/runs/37388694611/job/112028325105	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028373058	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37388694768/job/112028325708	
build (client)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37388694985/job/112028326365	
build (server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37388694985/job/112028326566	
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028326415	
private-bootstrap (macos-14, client)	pass	13s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325492	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325433	
test (macos-14, client)	pass	7m28s	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028372967	
test (ubuntu-24.04, server)	pass	4m48s	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028373048	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028372954	
private-bootstrap (ubuntu-24.04, server)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325595	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325241	
public-bootstrap (ubuntu-24.04, client)	pass	7m14s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325519	
public-bootstrap (ubuntu-24.04, server)	pass	6m48s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325564	
validate	pass	1m22s	https://github.com/mryfmo/dotfiles/actions/runs/37388694611/job/112028325105	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028373058	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37388694768/job/112028325708	
build (client)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37388694985/job/112028326365	
build (server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37388694985/job/112028326566	
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028326415	
private-bootstrap (macos-14, client)	pass	13s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325492	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325433	
private-bootstrap (ubuntu-24.04, server)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325595	
public-bootstrap (macos-14, client)	pass	8m30s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325241	
test (macos-14, client)	pass	7m28s	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028372967	
test (ubuntu-24.04, server)	pass	4m48s	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028373048	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028373058	
public-bootstrap (ubuntu-24.04, client)	pass	7m14s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325519	
public-bootstrap (ubuntu-24.04, server)	pass	6m48s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325564	
test (ubuntu-24.04, client)	pass	8m39s	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028372954	
validate	pass	1m22s	https://github.com/mryfmo/dotfiles/actions/runs/37388694611/job/112028325105	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37388694768/job/112028325708	
build (client)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37388694985/job/112028326365	
build (server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37388694985/job/112028326566	
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028326415	
private-bootstrap (macos-14, client)	pass	13s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325492	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325433	
private-bootstrap (ubuntu-24.04, server)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325595	
public-bootstrap (macos-14, client)	pass	8m30s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325241	
public-bootstrap (ubuntu-24.04, client)	pass	7m14s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325519	
public-bootstrap (ubuntu-24.04, server)	pass	6m48s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325564	
test (macos-14, client)	pass	7m28s	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028372967	
test (ubuntu-24.04, client)	pass	8m39s	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028372954	
test (ubuntu-24.04, server)	pass	4m48s	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028373048	
test (ubuntu-26.04, client)	pass	8m59s	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028373058	
validate	pass	1m22s	https://github.com/mryfmo/dotfiles/actions/runs/37388694611/job/112028325105	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37388694768/job/112028325708	
build (client)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37388694985/job/112028326365	
build (server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37388694985/job/112028326566	
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028326415	
private-bootstrap (macos-14, client)	pass	13s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325492	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325433	
private-bootstrap (ubuntu-24.04, server)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325595	
public-bootstrap (macos-14, client)	pass	8m30s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325241	
public-bootstrap (ubuntu-24.04, client)	pass	7m14s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325519	
public-bootstrap (ubuntu-24.04, server)	pass	6m48s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325564	
test (macos-14, client)	pass	7m28s	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028372967	
test (ubuntu-24.04, client)	pass	8m39s	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028372954	
test (ubuntu-24.04, server)	pass	4m48s	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028373048	
test (ubuntu-26.04, client)	pass	8m59s	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028373058	
validate	pass	1m22s	https://github.com/mryfmo/dotfiles/actions/runs/37388694611/job/112028325105	
watch exit=0
```

```
$ gh pr checks 288
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37388694768/job/112028325708	
build (client)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37388694985/job/112028326365	
build (server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37388694985/job/112028326566	
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028326415	
private-bootstrap (macos-14, client)	pass	13s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325492	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325433	
private-bootstrap (ubuntu-24.04, server)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325595	
public-bootstrap (macos-14, client)	pass	8m30s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325241	
public-bootstrap (ubuntu-24.04, client)	pass	7m14s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325519	
public-bootstrap (ubuntu-24.04, server)	pass	6m48s	https://github.com/mryfmo/dotfiles/actions/runs/37388694599/job/112028325564	
test (macos-14, client)	pass	7m28s	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028372967	
test (ubuntu-24.04, client)	pass	8m39s	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028372954	
test (ubuntu-24.04, server)	pass	4m48s	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028373048	
test (ubuntu-26.04, client)	pass	8m59s	https://github.com/mryfmo/dotfiles/actions/runs/37388694695/job/112028373058	
validate	pass	1m22s	https://github.com/mryfmo/dotfiles/actions/runs/37388694611/job/112028325105	
exit=0
```

```
$ gh api repos/mryfmo/dotfiles/pulls/288 --jq '.mergeable_state'
clean
exit=0
```

```
start 2026-10-05T23:38:08Z head=a41a56bd2b3b93c3432db647df1af39196762211 quota_cutoff=2026-10-05T23:28:27Z
poll 1 2026-10-05T23:38:09Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 2 2026-10-05T23:38:41Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 3 2026-10-05T23:39:12Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 4 2026-10-05T23:39:44Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 5 2026-10-05T23:40:15Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 6 2026-10-05T23:40:47Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 7 2026-10-05T23:41:18Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 8 2026-10-05T23:41:50Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 9 2026-10-05T23:42:21Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 10 2026-10-05T23:42:52Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 11 2026-10-05T23:43:24Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 12 2026-10-05T23:43:55Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 13 2026-10-05T23:44:27Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 14 2026-10-05T23:44:58Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 15 2026-10-05T23:45:29Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 16 2026-10-05T23:46:01Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 17 2026-10-05T23:46:33Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 18 2026-10-05T23:47:04Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 19 2026-10-05T23:47:35Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 20 2026-10-05T23:48:07Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 21 2026-10-05T23:48:38Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 22 2026-10-05T23:49:10Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 23 2026-10-05T23:49:41Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 24 2026-10-05T23:50:12Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 25 2026-10-05T23:50:44Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 26 2026-10-05T23:51:15Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 27 2026-10-05T23:51:47Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 28 2026-10-05T23:52:18Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 29 2026-10-05T23:52:50Z bot_reviews=0 bot_comments=0 quota_notices=0
end 2026-10-05T23:53:20Z
```

Every Bot item on PR 288 (all heads) and every review thread, swept after the wait:

```
$ gh api --paginate repos/mryfmo/dotfiles/pulls/288/reviews --jq '[.[]|select(.user.type=="Bot")|{id,commit_id,submitted_at}]'
[
{
"commit_id": "bb9e92ed17f7f8966a43ed5c60982dc97da58c19",
"id": 5421306432,
"submitted_at": "2026-10-05T22:19:35Z"
}
]
$ gh api --paginate repos/mryfmo/dotfiles/pulls/288/comments --jq '[.[]|select(.user.type=="Bot" and .in_reply_to_id==null)|{id,original_commit_id,path,line,created_at}]'
[
{
"created_at": "2026-10-05T22:19:35Z",
"id": 4189443339,
"line": 48,
"original_commit_id": "bb9e92ed17f7f8966a43ed5c60982dc97da58c19",
"path": "scripts/gh-auth-stores.sh"
}
]
$ gh api --paginate repos/mryfmo/dotfiles/issues/288/comments --jq '.[]|select(.user.type=="Bot")|"\(.id) \(.created_at) \(.body[0:100]|gsub("\n";" "))"'
6004109337 2026-10-05T22:09:21Z Codex usage limits have been reached for code reviews. Please check with the admins of this repo to 
6004110958 2026-10-05T22:09:27Z <!-- This is an auto-generated comment: summarize by coderabbit.ai --> <!-- This is an auto-generate
$ gh api graphql -f query=<reviewThreads of PR 288> --jq '.data.repository.pullRequest.reviewThreads.nodes[]|{isResolved,path,line}'
{
"isResolved": true,
"line": 48,
"path": "scripts/gh-auth-stores.sh"
}
```

- **The one Bot review:** the security review on `bb9e92ed`. Its thread is resolved: the orchestrator recorded `not-applicable` per PONG decision 2, and this seat did not touch it.
- **Final head:** no Bot review, inline comment or quota notice exists for `a41a56bd`.

## Revise round 2 (task_rev `sha256:2043ad50477829ad25979a12ecc420e2d4ac69e2c5dc285a454c6b9db7310816`)

Final head `c4fa1c14d447d99ca3de999bd4c47df3407ecc2b`. Pushed after the quota cutoff `2026-10-06T00:03:37Z`. `main` is unchanged at `2d0ef943`.

### The round-2 test on the previous head (a41a56bd); the test process's own exit status

```
$ git worktree add --detach <scratch> a41a56bd && cp tests/unit/test_gh_auth_stores.py <scratch>/tests/unit/
$ (cd <scratch> && uv run --no-project python -m unittest tests.unit.test_gh_auth_stores.GhAuthStoresTest.test_a_hosts_file_it_cannot_secure_fails_the_store 2>&1); echo "test exit=$?"
FFF
======================================================================
FAIL: test_a_hosts_file_it_cannot_secure_fails_the_store (tests.unit.test_gh_auth_stores.GhAuthStoresTest.test_a_hosts_file_it_cannot_secure_fails_the_store) (store='owner')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tmp/claude-1000/-home-moriya-Workspace-dotfiles--claude-worktrees-worker-c/79f0f3c0-a708-4c6f-affe-0d87fcc6ba5a/scratchpad/t103-r2-prev/tests/unit/test_gh_auth_stores.py", line 144, in test_a_hosts_file_it_cannot_secure_fails_the_store
    self.assertIn(
    ~~~~~~~~~~~~~^
        f"gh-auth: {label} store {store}: cannot set hosts.yml to mode 0600; "
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        'make it yours, then run "make gh-auth"',
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        result.stderr,
        ^^^^^^^^^^^^^^
    )
    ^
AssertionError: 'gh-auth: owner store /tmp/claude-1000/gh-auth-stores-test-zbg20y3v/home/.config/gh: cannot set hosts.yml to mode 0600; make it yours, then run "make gh-auth"' not found in 'chmod: Operation not permitted\nchmod: Operation not permitted\nchmod: Operation not permitted\n'

======================================================================
FAIL: test_a_hosts_file_it_cannot_secure_fails_the_store (tests.unit.test_gh_auth_stores.GhAuthStoresTest.test_a_hosts_file_it_cannot_secure_fails_the_store) (store='work')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tmp/claude-1000/-home-moriya-Workspace-dotfiles--claude-worktrees-worker-c/79f0f3c0-a708-4c6f-affe-0d87fcc6ba5a/scratchpad/t103-r2-prev/tests/unit/test_gh_auth_stores.py", line 144, in test_a_hosts_file_it_cannot_secure_fails_the_store
    self.assertIn(
    ~~~~~~~~~~~~~^
        f"gh-auth: {label} store {store}: cannot set hosts.yml to mode 0600; "
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        'make it yours, then run "make gh-auth"',
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        result.stderr,
        ^^^^^^^^^^^^^^
    )
    ^
AssertionError: 'gh-auth: work store /tmp/claude-1000/gh-auth-stores-test-zbg20y3v/home/.config/gh-work: cannot set hosts.yml to mode 0600; make it yours, then run "make gh-auth"' not found in 'chmod: Operation not permitted\nchmod: Operation not permitted\nchmod: Operation not permitted\n'

======================================================================
FAIL: test_a_hosts_file_it_cannot_secure_fails_the_store (tests.unit.test_gh_auth_stores.GhAuthStoresTest.test_a_hosts_file_it_cannot_secure_fails_the_store)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tmp/claude-1000/-home-moriya-Workspace-dotfiles--claude-worktrees-worker-c/79f0f3c0-a708-4c6f-affe-0d87fcc6ba5a/scratchpad/t103-r2-prev/tests/unit/test_gh_auth_stores.py", line 150, in test_a_hosts_file_it_cannot_secure_fails_the_store
    self.assertNotIn("owner store", result.stdout)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'owner store' unexpectedly found in 'gh-auth: owner store /tmp/claude-1000/gh-auth-stores-test-zbg20y3v/home/.config/gh already holds a token; skipped\ngh-auth: work store /tmp/claude-1000/gh-auth-stores-test-zbg20y3v/home/.config/gh-work has no token; log in as the work account\ngh-auth: worker store /tmp/claude-1000/gh-auth-stores-test-zbg20y3v/worker store has no token; log in as the worker account\n'

----------------------------------------------------------------------
Ran 1 test in 0.016s

FAILED (failures=3)
test exit=1
```

### Task validation commands on c4fa1c14

```
$ git rev-parse HEAD
c4fa1c14d447d99ca3de999bd4c47df3407ecc2b
exit=0
```

```
$ bash -n setup.sh scripts/gh-auth-stores.sh; echo "rc=$?"
rc=0
exit=0
```

```
$ shellcheck setup.sh scripts/gh-auth-stores.sh; echo "rc=$?"
rc=0
exit=0
```

```
$ make render-check
uv run --with pyyaml scripts/generate-agent-configs.py --check
generated agent configs are up to date
exit=0
```

```
$ make unit-test 2>&1 | tail -3
Ran 917 tests in 222.928s

OK (skipped=1)
exit=0
```

```
$ uv run --no-project --with pyyaml scripts/validate-agent-assets.py; echo "rc=$?"
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/acceptance/dotfiles-T103-gh-auth-stores-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/autoskill/runs/dotfiles-T103-gh-auth-stores-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/learning/dotfiles-T103-gh-auth-stores-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/reports/dotfiles-T103-gh-auth-stores-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/sandboxes/dotfiles-T103-gh-auth-stores-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/tasks/dotfiles-T103-gh-auth-stores-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T103-gh-auth-stores-a01-audit-0a28eb7.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T103-gh-auth-stores-a01-audit-0a28eb7.md.last.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T103-gh-auth-stores-a01-audit-a41a56b.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T103-gh-auth-stores-a01-audit-a41a56b.md.last.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T103-gh-auth-stores-a01-crit.json
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T103-gh-auth-stores-a01-pr-feedback.json
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T103-gh-auth-stores-a01-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T103-gh-auth-stores-a01-worker-crit.json
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T103-gh-auth-stores-a01-worker-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T103-gh-auth-stores-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/github-auth-design-2026-10-05.md
agent asset validation ok
rc=0
exit=0
```

```
$ grep -n 'gh auth login' Makefile scripts/update-agent-assets.sh home/.chezmoiscripts 2>/dev/null; echo "rc=$? (expect no match outside the gh-auth target)"
rc=2 (expect no match outside the gh-auth target)
exit=0
```

```
$ grep -rn 'gh auth login' Makefile scripts/update-agent-assets.sh home/.chezmoiscripts; echo "rc=$?   # recursive form: home/.chezmoiscripts is a directory, which plain grep -n reports as an error (rc=2 above)"
rc=1   # recursive form: home/.chezmoiscripts is a directory, which plain grep -n reports as an error (rc=2 above)
exit=0
```

```
$ bash -n scripts/check-tools.sh && shellcheck scripts/check-tools.sh; echo "rc=$?"
rc=0
exit=0
```

```
$ git ls-files -z "*.py" | xargs -0 ruff format --config ruff.toml --check
44 files already formatted
exit=0
```

```
$ mise x node npm:prettier -- prettier --check README.md
[33mmise[0m [33mWARN[0m  tool purgatory cleanup failed: Read-only file system (os error 30)
Checking formatting...
All matched files use Prettier code style!
exit=0
```

```
$ bash /tmp/claude-1000/t103/ruff-scan.sh   # the script is pasted in the round-1 section
scripts/check-agent-runtime.py: 3 findings in the file, 0 on added lines
scripts/generate-agent-configs.py: 4 findings in the file, 0 on added lines
tests/unit/test_generate_agent_configs.py: 11 findings in the file, 0 on added lines
tests/unit/test_runtime_health.py: 19 findings in the file, 0 on added lines
tests/unit/test_gh_auth_stores.py: 0 findings in the file, 0 on added lines
tests/unit/test_check_agent_runtime.py: 7 findings in the file, 0 on added lines
exit=0
```

### CI, mergeable state and Bot wait on c4fa1c14 (`bot: none`; no quota notice after the cutoff)

```
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37391960502/job/112038882765	
build (client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37391960461/job/112038882900	
build (server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37391960461/job/112038882645	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882805	
private-bootstrap (macos-14, client)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882860	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882463	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925858	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925897	
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038884160	
private-bootstrap (ubuntu-24.04, server)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882840	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882789	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925889	
validate	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960460/job/112038882602	
private-bootstrap (ubuntu-24.04, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882845	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038926084	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37391960502/job/112038882765	
build (client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37391960461/job/112038882900	
build (server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37391960461/job/112038882645	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882805	
private-bootstrap (macos-14, client)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882860	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882463	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925858	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925897	
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038884160	
private-bootstrap (ubuntu-24.04, server)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882840	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882789	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925889	
validate	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960460/job/112038882602	
private-bootstrap (ubuntu-24.04, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882845	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038926084	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37391960502/job/112038882765	
build (client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37391960461/job/112038882900	
build (server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37391960461/job/112038882645	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882805	
private-bootstrap (macos-14, client)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882860	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882463	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925858	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925897	
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038884160	
private-bootstrap (ubuntu-24.04, server)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882840	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882789	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925889	
validate	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960460/job/112038882602	
private-bootstrap (ubuntu-24.04, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882845	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038926084	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37391960502/job/112038882765	
build (client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37391960461/job/112038882900	
build (server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37391960461/job/112038882645	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882805	
private-bootstrap (macos-14, client)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882860	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882463	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925858	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925897	
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038884160	
private-bootstrap (ubuntu-24.04, server)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882840	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882789	
validate	pass	1m22s	https://github.com/mryfmo/dotfiles/actions/runs/37391960460/job/112038882602	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925889	
private-bootstrap (ubuntu-24.04, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882845	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038926084	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37391960502/job/112038882765	
build (client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37391960461/job/112038882900	
build (server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37391960461/job/112038882645	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882805	
private-bootstrap (macos-14, client)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882860	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882463	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925858	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925897	
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038884160	
private-bootstrap (ubuntu-24.04, server)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882840	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882789	
validate	pass	1m22s	https://github.com/mryfmo/dotfiles/actions/runs/37391960460/job/112038882602	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925889	
private-bootstrap (ubuntu-24.04, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882845	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038926084	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37391960502/job/112038882765	
build (client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37391960461/job/112038882900	
build (server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37391960461/job/112038882645	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882805	
private-bootstrap (macos-14, client)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882860	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882463	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925858	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925897	
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038884160	
private-bootstrap (ubuntu-24.04, server)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882840	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882789	
validate	pass	1m22s	https://github.com/mryfmo/dotfiles/actions/runs/37391960460/job/112038882602	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925889	
private-bootstrap (ubuntu-24.04, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882845	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038926084	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37391960502/job/112038882765	
build (client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37391960461/job/112038882900	
build (server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37391960461/job/112038882645	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882805	
private-bootstrap (macos-14, client)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882860	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882463	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925858	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925897	
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038884160	
private-bootstrap (ubuntu-24.04, server)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882840	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882789	
validate	pass	1m22s	https://github.com/mryfmo/dotfiles/actions/runs/37391960460/job/112038882602	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925889	
private-bootstrap (ubuntu-24.04, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882845	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038926084	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37391960502/job/112038882765	
build (client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37391960461/job/112038882900	
build (server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37391960461/job/112038882645	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882805	
private-bootstrap (macos-14, client)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882860	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882463	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925858	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925897	
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038884160	
private-bootstrap (ubuntu-24.04, server)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882840	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882789	
validate	pass	1m22s	https://github.com/mryfmo/dotfiles/actions/runs/37391960460/job/112038882602	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925889	
private-bootstrap (ubuntu-24.04, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882845	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038926084	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37391960502/job/112038882765	
build (client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37391960461/job/112038882900	
build (server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37391960461/job/112038882645	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882805	
private-bootstrap (macos-14, client)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882860	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882463	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925858	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925897	
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038884160	
private-bootstrap (ubuntu-24.04, server)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882840	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882789	
validate	pass	1m22s	https://github.com/mryfmo/dotfiles/actions/runs/37391960460/job/112038882602	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925889	
private-bootstrap (ubuntu-24.04, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882845	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038926084	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37391960502/job/112038882765	
build (client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37391960461/job/112038882900	
build (server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37391960461/job/112038882645	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882805	
private-bootstrap (macos-14, client)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882860	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882463	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925858	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925897	
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038884160	
private-bootstrap (ubuntu-24.04, server)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882840	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882789	
validate	pass	1m22s	https://github.com/mryfmo/dotfiles/actions/runs/37391960460/job/112038882602	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925889	
private-bootstrap (ubuntu-24.04, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882845	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038926084	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37391960502/job/112038882765	
build (client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37391960461/job/112038882900	
build (server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37391960461/job/112038882645	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882805	
private-bootstrap (macos-14, client)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882860	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882463	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925858	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925897	
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038884160	
private-bootstrap (ubuntu-24.04, server)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882840	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882789	
validate	pass	1m22s	https://github.com/mryfmo/dotfiles/actions/runs/37391960460/job/112038882602	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925889	
private-bootstrap (ubuntu-24.04, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882845	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038926084	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37391960502/job/112038882765	
build (client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37391960461/job/112038882900	
build (server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37391960461/job/112038882645	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882805	
private-bootstrap (macos-14, client)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882860	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882463	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925858	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925897	
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038884160	
private-bootstrap (ubuntu-24.04, server)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882840	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882789	
validate	pass	1m22s	https://github.com/mryfmo/dotfiles/actions/runs/37391960460/job/112038882602	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925889	
private-bootstrap (ubuntu-24.04, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882845	
test (ubuntu-24.04, server)	pass	5m42s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038926084	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37391960502/job/112038882765	
build (client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37391960461/job/112038882900	
build (server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37391960461/job/112038882645	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882805	
private-bootstrap (macos-14, client)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882860	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882463	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925858	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925897	
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038884160	
private-bootstrap (ubuntu-24.04, server)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882840	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882789	
validate	pass	1m22s	https://github.com/mryfmo/dotfiles/actions/runs/37391960460/job/112038882602	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925889	
private-bootstrap (ubuntu-24.04, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882845	
test (ubuntu-24.04, server)	pass	5m42s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038926084	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37391960502/job/112038882765	
build (client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37391960461/job/112038882900	
build (server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37391960461/job/112038882645	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882805	
private-bootstrap (macos-14, client)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882860	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882463	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925858	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925897	
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038884160	
private-bootstrap (ubuntu-24.04, server)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882840	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882789	
validate	pass	1m22s	https://github.com/mryfmo/dotfiles/actions/runs/37391960460/job/112038882602	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925889	
private-bootstrap (ubuntu-24.04, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882845	
test (ubuntu-24.04, server)	pass	5m42s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038926084	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37391960502/job/112038882765	
build (client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37391960461/job/112038882900	
build (server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37391960461/job/112038882645	
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038884160	
private-bootstrap (macos-14, client)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882860	
private-bootstrap (ubuntu-24.04, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882845	
private-bootstrap (ubuntu-24.04, server)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882840	
test (macos-14, client)	pass	6m57s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925858	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882805	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882789	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882463	
validate	pass	1m22s	https://github.com/mryfmo/dotfiles/actions/runs/37391960460/job/112038882602	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925889	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925897	
test (ubuntu-24.04, server)	pass	5m42s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038926084	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37391960502/job/112038882765	
build (client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37391960461/job/112038882900	
build (server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37391960461/job/112038882645	
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038884160	
private-bootstrap (macos-14, client)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882860	
private-bootstrap (ubuntu-24.04, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882845	
private-bootstrap (ubuntu-24.04, server)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882840	
public-bootstrap (ubuntu-24.04, server)	pass	7m41s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882463	
test (macos-14, client)	pass	6m57s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925858	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882805	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882789	
validate	pass	1m22s	https://github.com/mryfmo/dotfiles/actions/runs/37391960460/job/112038882602	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925889	
test (ubuntu-24.04, server)	pass	5m42s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038926084	
test (ubuntu-26.04, client)	pass	7m46s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925897	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37391960502/job/112038882765	
build (client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37391960461/job/112038882900	
build (server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37391960461/job/112038882645	
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038884160	
private-bootstrap (macos-14, client)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882860	
private-bootstrap (ubuntu-24.04, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882845	
private-bootstrap (ubuntu-24.04, server)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882840	
public-bootstrap (ubuntu-24.04, server)	pass	7m41s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882463	
test (macos-14, client)	pass	6m57s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925858	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882805	
public-bootstrap (ubuntu-24.04, client)	pass	8m6s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882789	
test (ubuntu-24.04, client)	pass	8m8s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925889	
test (ubuntu-24.04, server)	pass	5m42s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038926084	
test (ubuntu-26.04, client)	pass	7m46s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925897	
validate	pass	1m22s	https://github.com/mryfmo/dotfiles/actions/runs/37391960460/job/112038882602	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37391960502/job/112038882765	
build (client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37391960461/job/112038882900	
build (server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37391960461/job/112038882645	
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038884160	
private-bootstrap (macos-14, client)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882860	
private-bootstrap (ubuntu-24.04, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882845	
private-bootstrap (ubuntu-24.04, server)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882840	
public-bootstrap (ubuntu-24.04, server)	pass	7m41s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882463	
test (macos-14, client)	pass	6m57s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925858	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882805	
public-bootstrap (ubuntu-24.04, client)	pass	8m6s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882789	
test (ubuntu-24.04, client)	pass	8m8s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925889	
test (ubuntu-24.04, server)	pass	5m42s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038926084	
test (ubuntu-26.04, client)	pass	7m46s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925897	
validate	pass	1m22s	https://github.com/mryfmo/dotfiles/actions/runs/37391960460/job/112038882602	
[0;1;39mRefreshing checks status every 30 seconds. Press Ctrl+C to quit.
[0m
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37391960502/job/112038882765	
build (client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37391960461/job/112038882900	
build (server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37391960461/job/112038882645	
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038884160	
private-bootstrap (macos-14, client)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882860	
private-bootstrap (ubuntu-24.04, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882845	
private-bootstrap (ubuntu-24.04, server)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882840	
public-bootstrap (ubuntu-24.04, server)	pass	7m41s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882463	
test (macos-14, client)	pass	6m57s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925858	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882805	
public-bootstrap (ubuntu-24.04, client)	pass	8m6s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882789	
test (ubuntu-24.04, client)	pass	8m8s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925889	
test (ubuntu-24.04, server)	pass	5m42s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038926084	
test (ubuntu-26.04, client)	pass	7m46s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925897	
validate	pass	1m22s	https://github.com/mryfmo/dotfiles/actions/runs/37391960460/job/112038882602	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37391960502/job/112038882765	
build (client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37391960461/job/112038882900	
build (server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37391960461/job/112038882645	
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038884160	
private-bootstrap (macos-14, client)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882860	
private-bootstrap (ubuntu-24.04, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882845	
private-bootstrap (ubuntu-24.04, server)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882840	
public-bootstrap (macos-14, client)	pass	9m45s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882805	
public-bootstrap (ubuntu-24.04, client)	pass	8m6s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882789	
public-bootstrap (ubuntu-24.04, server)	pass	7m41s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882463	
test (macos-14, client)	pass	6m57s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925858	
test (ubuntu-24.04, client)	pass	8m8s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925889	
test (ubuntu-24.04, server)	pass	5m42s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038926084	
test (ubuntu-26.04, client)	pass	7m46s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925897	
validate	pass	1m22s	https://github.com/mryfmo/dotfiles/actions/runs/37391960460/job/112038882602	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37391960502/job/112038882765	
build (client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37391960461/job/112038882900	
build (server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37391960461/job/112038882645	
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038884160	
private-bootstrap (macos-14, client)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882860	
private-bootstrap (ubuntu-24.04, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882845	
private-bootstrap (ubuntu-24.04, server)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882840	
public-bootstrap (macos-14, client)	pass	9m45s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882805	
public-bootstrap (ubuntu-24.04, client)	pass	8m6s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882789	
public-bootstrap (ubuntu-24.04, server)	pass	7m41s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882463	
test (macos-14, client)	pass	6m57s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925858	
test (ubuntu-24.04, client)	pass	8m8s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925889	
test (ubuntu-24.04, server)	pass	5m42s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038926084	
test (ubuntu-26.04, client)	pass	7m46s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925897	
validate	pass	1m22s	https://github.com/mryfmo/dotfiles/actions/runs/37391960460/job/112038882602	
watch exit=0
```

```
$ gh pr checks 288
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37391960502/job/112038882765	
build (client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37391960461/job/112038882900	
build (server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37391960461/job/112038882645	
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038884160	
private-bootstrap (macos-14, client)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882860	
private-bootstrap (ubuntu-24.04, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882845	
private-bootstrap (ubuntu-24.04, server)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882840	
public-bootstrap (macos-14, client)	pass	9m45s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882805	
public-bootstrap (ubuntu-24.04, client)	pass	8m6s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882789	
public-bootstrap (ubuntu-24.04, server)	pass	7m41s	https://github.com/mryfmo/dotfiles/actions/runs/37391960457/job/112038882463	
test (macos-14, client)	pass	6m57s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925858	
test (ubuntu-24.04, client)	pass	8m8s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925889	
test (ubuntu-24.04, server)	pass	5m42s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038926084	
test (ubuntu-26.04, client)	pass	7m46s	https://github.com/mryfmo/dotfiles/actions/runs/37391960980/job/112038925897	
validate	pass	1m22s	https://github.com/mryfmo/dotfiles/actions/runs/37391960460/job/112038882602	
exit=0
```

```
$ gh api repos/mryfmo/dotfiles/pulls/288 --jq '.mergeable_state'
clean
exit=0
```

```
start 2026-10-06T00:13:51Z head=c4fa1c14d447d99ca3de999bd4c47df3407ecc2b quota_cutoff=2026-10-06T00:03:37Z
poll 1 2026-10-06T00:13:53Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 2 2026-10-06T00:14:24Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 3 2026-10-06T00:14:55Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 4 2026-10-06T00:15:27Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 5 2026-10-06T00:15:59Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 6 2026-10-06T00:16:31Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 7 2026-10-06T00:17:02Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 8 2026-10-06T00:17:34Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 9 2026-10-06T00:18:05Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 10 2026-10-06T00:18:37Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 11 2026-10-06T00:19:08Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 12 2026-10-06T00:19:39Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 13 2026-10-06T00:20:11Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 14 2026-10-06T00:20:42Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 15 2026-10-06T00:21:14Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 16 2026-10-06T00:21:45Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 17 2026-10-06T00:22:16Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 18 2026-10-06T00:22:48Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 19 2026-10-06T00:23:19Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 20 2026-10-06T00:23:51Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 21 2026-10-06T00:24:22Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 22 2026-10-06T00:24:54Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 23 2026-10-06T00:25:25Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 24 2026-10-06T00:25:56Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 25 2026-10-06T00:26:28Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 26 2026-10-06T00:26:59Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 27 2026-10-06T00:27:31Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 28 2026-10-06T00:28:02Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 29 2026-10-06T00:28:34Z bot_reviews=0 bot_comments=0 quota_notices=0
end 2026-10-06T00:29:04Z
```

Every Bot item on PR 288 (all heads) and every review thread, swept after the wait:

```
$ gh api --paginate repos/mryfmo/dotfiles/pulls/288/reviews --jq '[.[]|select(.user.type=="Bot")|{id,commit_id,submitted_at}]'
[
{
"commit_id": "bb9e92ed17f7f8966a43ed5c60982dc97da58c19",
"id": 5421306432,
"submitted_at": "2026-10-05T22:19:35Z"
}
]
$ gh api --paginate repos/mryfmo/dotfiles/pulls/288/comments --jq '[.[]|select(.user.type=="Bot" and .in_reply_to_id==null)|{id,original_commit_id,path,line,created_at}]'
[
{
"created_at": "2026-10-05T22:19:35Z",
"id": 4189443339,
"line": 62,
"original_commit_id": "bb9e92ed17f7f8966a43ed5c60982dc97da58c19",
"path": "scripts/gh-auth-stores.sh"
}
]
$ gh api --paginate repos/mryfmo/dotfiles/issues/288/comments --jq '.[]|select(.user.type=="Bot")|"\(.id) \(.created_at) \(.body[0:100]|gsub("\n";" "))"'
6004109337 2026-10-05T22:09:21Z Codex usage limits have been reached for code reviews. Please check with the admins of this repo to 
6004110958 2026-10-05T22:09:27Z <!-- This is an auto-generated comment: summarize by coderabbit.ai --> <!-- This is an auto-generate
$ gh api graphql -f query=<reviewThreads of PR 288> --jq '.data.repository.pullRequest.reviewThreads.nodes[]|{isResolved,path,line}'
{
"isResolved": true,
"line": 62,
"path": "scripts/gh-auth-stores.sh"
}
```

- **Bot items:** none were posted for `a41a56bd` or `c4fa1c14`.
- **Review threads:** the only one is the `bb9e92ed` security thread, which the orchestrator resolved.
