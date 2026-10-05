# T90 validation

PR: https://github.com/mryfmo/dotfiles/pull/262
Diff commit: a8151c9a65bc893aae4eed6ed0cce5c55732a51a
Previous implementation head: 507e9c159d6ce73998ca70e79ac3951c04f81ff6.
Revise round 1 documentation head: e2d5c9a3fdae30f6137c5e5fb5cae785691a66fd.
Base: 8cd66881021c4bffe28d5a3d2ba75aba76e76665.
Prior merge heads and validation history are recorded below.

## Test-first core RED (expected failure)

```text
test_worker_gh_dir_is_shell_safe_and_defaults_to_separate_config (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_worker_gh_dir_is_shell_safe_and_defaults_to_separate_config) ... FAIL
test_doctor_github_role_activation_and_file_storage (tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_github_role_activation_and_file_storage) ... FAIL
test_github_identity_gate_activation_and_current_head_approval (tests.unit.test_require_crit_review.ReviewGuardTest.test_github_identity_gate_activation_and_current_head_approval) ... FAIL

======================================================================
FAIL: test_worker_gh_dir_is_shell_safe_and_defaults_to_separate_config (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_worker_gh_dir_is_shell_safe_and_defaults_to_separate_config)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_generate_agent_configs.py", line 887, in test_worker_gh_dir_is_shell_safe_and_defaults_to_separate_config
    self.assertEqual(value, result.stdout)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^
AssertionError: '~/.config/gh-worker' != ''
- ~/.config/gh-worker


======================================================================
FAIL: test_doctor_github_role_activation_and_file_storage (tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_github_role_activation_and_file_storage)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py", line 1163, in test_doctor_github_role_activation_and_file_storage
    self.assertIn("warnings=1", missing.stdout)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'warnings=1' not found in ''

======================================================================
FAIL: test_github_identity_gate_activation_and_current_head_approval (tests.unit.test_require_crit_review.ReviewGuardTest.test_github_identity_gate_activation_and_current_head_approval)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_require_crit_review.py", line 440, in test_github_identity_gate_activation_and_current_head_approval
    self.assertIn("notice:", absent.stdout)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'notice:' not found in 'PR feedback evidence accepted: .orchestration/validation/test-pr-feedback.json\nReview not required: no meaningful review trigger found.\n'

----------------------------------------------------------------------
Ran 3 tests in 0.129s

FAILED (failures=3)
```

## Core focused tests before launcher

```text
test_worker_gh_dir_is_shell_safe_and_defaults_to_separate_config (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_worker_gh_dir_is_shell_safe_and_defaults_to_separate_config) ... ERROR: worker_gh_config_dir must be an absolute or ~/ path without control characters
ERROR: worker_gh_config_dir must be an absolute or ~/ path without control characters
ERROR: worker_gh_config_dir must be an absolute or ~/ path without control characters
ERROR: worker_gh_config_dir must be an absolute or ~/ path without control characters
ok
test_doctor_github_role_activation_and_file_storage (tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_github_role_activation_and_file_storage) ... ok
test_github_identity_gate_activation_and_current_head_approval (tests.unit.test_require_crit_review.ReviewGuardTest.test_github_identity_gate_activation_and_current_head_approval) ... ok

----------------------------------------------------------------------
Ran 3 tests in 1.224s

OK
```

## Test-first launcher RED (expected failure)

```text
FFFF
======================================================================
FAIL: test_worker_github_pair_and_restart_env (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_github_pair_and_restart_env) (kind='codex')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_herdr_agents.py", line 2612, in test_worker_github_pair_and_restart_env
    self.assertEqual(len(env_calls), 1, calls)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 0 != 1 : ['workspace list', 'workspace create --cwd /tmp/herdr-agents-test-i11elj_s/project --label project agents --env CLICOLOR_FORCE=1 --env FORCE_COLOR=1 --env HERDR_AGENTS_LAYOUT=managed --focus', 'pane list --workspace w-test', 'pane rename w-test:p1 claude-orchestrator', 'pane process-info --pane w-test:p1', 'pane read w-test:p1 --source recent-unwrapped --lines 50', 'agent start claude-orchestrator-w-test --kind claude --pane w-test:p1 --timeout 30000 --', 'pane split w-test:p1 --direction right --cwd /tmp/herdr-agents-test-i11elj_s/project --env CLICOLOR_FORCE=1 --env FORCE_COLOR=1 --env AGMSG_RESOLVE_PROJECT=0 --no-focus', 'pane process-info --pane w-test:p3', 'pane read w-test:p3 --source recent-unwrapped --lines 50', 'agent start codex-worker-w-test --kind codex --pane w-test:p3 --timeout 30000 -- --sandbox workspace-write --profile standard --ask-for-approval never -c sandbox_workspace_write.network_access=true', 'pane list --workspace w-test', 'pane rename w-test:p3 codex-worker']

======================================================================
FAIL: test_worker_github_pair_and_restart_env (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_github_pair_and_restart_env) (kind='claude')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_herdr_agents.py", line 2609, in test_worker_github_pair_and_restart_env
    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 2 != 0 : herdr-agents: worker_kind=claude would share the orchestrator's claude-code agmsg identity on /tmp/herdr-agents-test-i11elj_s/project (0 claude-code identity registered); refusing so messages do not collide silently. Registering a second identity (AGMSG_RESOLVE_PROJECT=0 /tmp/herdr-agents-test-i11elj_s/home/.agents/skills/agmsg/scripts/join.sh <team> <role> claude-code /tmp/herdr-agents-test-i11elj_s/project) lifts this guard but does not give the two sessions distinct delivery until agmsg roles land; use worker_kind=codex for separate delivery now. See the herdr-agents section of the dotfiles README.


======================================================================
FAIL: test_added_worker_github_environment_reaches_boot (tests.unit.test_herdr_agents.HerdrAgentsTest.test_added_worker_github_environment_reaches_boot) (kind='codex')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_herdr_agents.py", line 2653, in test_added_worker_github_environment_reaches_boot
    self.assertEqual(received["GH_CONFIG_DIR"], path)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'from-shell' != "/tmp/herdr-agents-test-h9lzvv42/home/worker's # $(false)"
- from-shell
+ /tmp/herdr-agents-test-h9lzvv42/home/worker's # $(false)


======================================================================
FAIL: test_added_worker_github_environment_reaches_boot (tests.unit.test_herdr_agents.HerdrAgentsTest.test_added_worker_github_environment_reaches_boot) (kind='claude')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_herdr_agents.py", line 2653, in test_added_worker_github_environment_reaches_boot
    self.assertEqual(received["GH_CONFIG_DIR"], path)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'from-shell' != "/tmp/herdr-agents-test-h9lzvv42/home/worker's # $(false)"
- from-shell
+ /tmp/herdr-agents-test-h9lzvv42/home/worker's # $(false)


----------------------------------------------------------------------
Ran 2 tests in 1.855s

FAILED (failures=4)
```

## Initial focused suite before fixture refresh; overlapped edits (superseded)

```text
..F...............F/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:597: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfdbb7d3d6200>
  is_sync, cb = self._exit_callbacks.pop()
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:597: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfdbb7d3d65c0>
  is_sync, cb = self._exit_callbacks.pop()
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:597: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfdbb7d3d6890>
  is_sync, cb = self._exit_callbacks.pop()
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:597: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfdbb7d3d66b0>
  is_sync, cb = self._exit_callbacks.pop()
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:597: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfdbb7d3d67a0>
  is_sync, cb = self._exit_callbacks.pop()
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:597: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfdbb7d3d6d40>
  is_sync, cb = self._exit_callbacks.pop()
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:597: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfdbb7d3d6e30>
  is_sync, cb = self._exit_callbacks.pop()
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:597: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfdbb7d3d6f20>
  is_sync, cb = self._exit_callbacks.pop()
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:597: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfdbb7d3d7010>
  is_sync, cb = self._exit_callbacks.pop()
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:597: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfdbb7d3d7100>
  is_sync, cb = self._exit_callbacks.pop()
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:597: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfdbb7d3d72e0>
  is_sync, cb = self._exit_callbacks.pop()
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:597: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfdbb7d3d71f0>
  is_sync, cb = self._exit_callbacks.pop()
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:597: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfdbb7d3d74c0>
  is_sync, cb = self._exit_callbacks.pop()
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:597: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfdbb7cce5e40>
  is_sync, cb = self._exit_callbacks.pop()
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:597: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfdbb7d3d4c70>
  is_sync, cb = self._exit_callbacks.pop()
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:597: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfdbb7d3d75b0>
  is_sync, cb = self._exit_callbacks.pop()
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:597: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfdbb7d3d76a0>
  is_sync, cb = self._exit_callbacks.pop()
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:597: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfdbb7d3d7790>
  is_sync, cb = self._exit_callbacks.pop()
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:597: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfdbb7d3d7880>
  is_sync, cb = self._exit_callbacks.pop()
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:597: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfdbb7d3d7970>
  is_sync, cb = self._exit_callbacks.pop()
ResourceWarning: Enable tracemalloc to get the object allocation traceback
............................................................................................F...F.....F..F...F.FF.........................................F.......................F..F.......FF.............<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfdbb7cce5e40>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfdbb7d3d7b50>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfdbb7d3d7880>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfdbb7d3d7790>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfdbb7d3d75b0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfdbb7d3d4c70>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfdbb7d3d74c0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfdbb7d3d71f0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfdbb7d3d72e0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfdbb7d3d7100>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfdbb7d3d7010>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfdbb7d3d6f20>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfdbb7d3d6d40>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfdbb7d3d67a0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfdbb7cd15d50>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfdbb7cd15f30>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfdbb7cd16020>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfdbb7cd16200>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfdbb7cd162f0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfdbb7cd164d0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfdbb7cd165c0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfdbb7cd167a0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfdbb7cd16890>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfdbb7cd16980>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
...........................ERROR: model profile standard is missing codex
ERROR: model profile standard.claude.model must be a launcher-safe string
ERROR: model_profiles must define the express profile
..ERROR: model profile standard.claude.advisor must be a launcher-safe string
................ERROR: interactive_profile must name a model profile: 'missing'
.ERROR: worker_kind must be one of ('codex', 'claude'): 'banana'
.ERROR: worker_profile must name a model profile: 'missing'
.ERROR: worker_gh_config_dir must be an absolute or ~/ path without control characters
ERROR: worker_gh_config_dir must be an absolute or ~/ path without control characters
ERROR: worker_gh_config_dir must be an absolute or ~/ path without control characters
ERROR: worker_gh_config_dir must be an absolute or ~/ path without control characters
..ERROR: worker_worktree must be a relative path under .claude/worktrees/: 'worker-c'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '/abs/.claude/worktrees/x'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/..'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/a/b'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/$(x)'
.......................................FF...........................................................................
======================================================================
FAIL: test_add_worker_emits_no_override_for_an_unparseable_codex_config (tests.unit.test_herdr_agents.HerdrAgentsTest.test_add_worker_emits_no_override_for_an_unparseable_codex_config)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_herdr_agents.py", line 2733, in test_add_worker_emits_no_override_for_an_unparseable_codex_config
    self.assertEqual(
    ~~~~~~~~~~~~~~~~^
        options,
        ^^^^^^^^
        "codex:\n  --profile: review\n  --sandbox: workspace-write\n  --ask-for-approval: never\n  --config: sandbox_workspace_write.network_access=true\n",
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
AssertionError: 'code[136 chars]rue\n  --config: shell_environment_policy.set.[68 chars]r"\n' != 'code[136 chars]rue\n'
  codex:
    --profile: review
    --sandbox: workspace-write
    --ask-for-approval: never
    --config: sandbox_workspace_write.network_access=true
-   --config: shell_environment_policy.set.GH_CONFIG_DIR="/tmp/herdr-agents-test-rxf94vsc/home/.config/gh-worker"


======================================================================
FAIL: test_add_worker_passes_codex_profile_and_sandbox_through_spawn_options (tests.unit.test_herdr_agents.HerdrAgentsTest.test_add_worker_passes_codex_profile_and_sandbox_through_spawn_options)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_herdr_agents.py", line 2777, in test_add_worker_passes_codex_profile_and_sandbox_through_spawn_options
    self.assertEqual(
    ~~~~~~~~~~~~~~~~^
        options.read_text(),
        ^^^^^^^^^^^^^^^^^^^^
        "codex:\n  --profile: review\n  --sandbox: workspace-write\n  --ask-for-approval: never\n  --config: sandbox_workspace_write.network_access=true\n"
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        f"  --config: sandbox_workspace_write.writable_roots={roots}\n",
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
AssertionError: 'code[149 chars]ig: shell_environment_policy.set.GH_CONFIG_DIR[591 chars]"]\n' != 'code[149 chars]ig: sandbox_workspace_write.writable_roots=["/[478 chars]"]\n'
Diff is 802 characters long. Set self.maxDiff to None to see it.

======================================================================
FAIL: test_claude_repair_skips_just_restarted_codex_pane_without_agent_field (tests.unit.test_herdr_agents.HerdrAgentsTest.test_claude_repair_skips_just_restarted_codex_pane_without_agent_field)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_herdr_agents.py", line 5280, in test_claude_repair_skips_just_restarted_codex_pane_without_agent_field
    self.assertIn(
    ~~~~~~~~~~~~~^
        "agent start codex-worker-w-old --kind codex --pane w-old:p2 --timeout 30000 -- --sandbox workspace-write --profile standard --ask-for-approval never -c sandbox_workspace_write.network_access=true",
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        calls,
        ^^^^^^
    )
    ^
AssertionError: 'agent start codex-worker-w-old --kind codex --pane w-old:p2 --timeout 30000 -- --sandbox workspace-write --profile standard --ask-for-approval never -c sandbox_workspace_write.network_access=true' not found in ['workspace list', 'pane list --workspace w-old', 'pane list --workspace w-old', 'agent get codex-worker-w-old', 'pane process-info --pane w-old:p2', 'pane read w-old:p2 --source recent-unwrapped --lines 50', 'pane run w-old:p2 unset GH_TOKEN GITHUB_TOKEN GH_ENTERPRISE_TOKEN GITHUB_ENTERPRISE_TOKEN; export GH_CONFIG_DIR=/tmp/herdr-agents-test-czlsefoz/home/.config/gh-worker', 'agent start codex-worker-w-old --kind codex --pane w-old:p2 --timeout 30000 -- --sandbox workspace-write --profile standard --ask-for-approval never -c sandbox_workspace_write.network_access=true -c shell_environment_policy.set.GH_CONFIG_DIR="/tmp/herdr-agents-test-czlsefoz/home/.config/gh-worker"', 'pane list --workspace w-old', 'pane rename w-old:p2 codex-worker', 'pane list --workspace w-old', 'pane run w-old:p3 export CLICOLOR_FORCE=1 FORCE_COLOR=1 HERDR_AGENTS_LAYOUT=managed', 'pane process-info --pane w-old:p3', 'pane read w-old:p3 --source recent-unwrapped --lines 50', 'pane list --workspace w-old', 'pane rename w-old:p3 claude-orchestrator', 'agent start claude-orchestrator-w-old --kind claude --pane w-old:p3 --timeout 30000 --', 'pane list --workspace w-old', 'workspace focus w-old']

======================================================================
FAIL: test_codex_profile_defaults_to_generated_interactive_profile (tests.unit.test_herdr_agents.HerdrAgentsTest.test_codex_profile_defaults_to_generated_interactive_profile)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_herdr_agents.py", line 1376, in test_codex_profile_defaults_to_generated_interactive_profile
    self.assertTrue(
    ~~~~~~~~~~~~~~~^
        any(
        ^^^^
    ...<5 lines>...
        )
        ^
    )
    ^
AssertionError: False is not true

======================================================================
FAIL: test_existing_workspace_restarts_missing_codex_agent (tests.unit.test_herdr_agents.HerdrAgentsTest.test_existing_workspace_restarts_missing_codex_agent)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_herdr_agents.py", line 5256, in test_existing_workspace_restarts_missing_codex_agent
    self.assertIn(
    ~~~~~~~~~~~~~^
        "agent start codex-worker-w-old --kind codex --pane w-old:p3 --timeout 30000 -- --sandbox workspace-write --profile standard --ask-for-approval never -c sandbox_workspace_write.network_access=true",
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        calls,
        ^^^^^^
    )
    ^
AssertionError: 'agent start codex-worker-w-old --kind codex --pane w-old:p3 --timeout 30000 -- --sandbox workspace-write --profile standard --ask-for-approval never -c sandbox_workspace_write.network_access=true' not found in ['workspace list', 'pane list --workspace w-old', 'pane list --workspace w-old', 'agent get codex-worker-w-old', 'pane split w-old:p1 --direction right --cwd /tmp/herdr-agents-test-h3k0j216/project --env CLICOLOR_FORCE=1 --env FORCE_COLOR=1 --env AGMSG_RESOLVE_PROJECT=0 --no-focus', 'pane process-info --pane w-old:p3', 'pane read w-old:p3 --source recent-unwrapped --lines 50', 'pane run w-old:p3 unset GH_TOKEN GITHUB_TOKEN GH_ENTERPRISE_TOKEN GITHUB_ENTERPRISE_TOKEN; export GH_CONFIG_DIR=/tmp/herdr-agents-test-h3k0j216/home/.config/gh-worker', 'pane process-info --pane w-old:p3', 'pane read w-old:p3 --source recent-unwrapped --lines 50', 'agent start codex-worker-w-old --kind codex --pane w-old:p3 --timeout 30000 -- --sandbox workspace-write --profile standard --ask-for-approval never -c sandbox_workspace_write.network_access=true -c shell_environment_policy.set.GH_CONFIG_DIR="/tmp/herdr-agents-test-h3k0j216/home/.config/gh-worker"', 'pane list --workspace w-old', 'pane rename w-old:p3 codex-worker', 'pane list --workspace w-old', 'pane list --workspace w-old', 'workspace focus w-old']

======================================================================
FAIL: test_explicit_worker_kind_and_profile_survive_seat_label_loading (tests.unit.test_herdr_agents.HerdrAgentsTest.test_explicit_worker_kind_and_profile_survive_seat_label_loading)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_herdr_agents.py", line 4817, in test_explicit_worker_kind_and_profile_survive_seat_label_loading
    self.assertTrue(
    ~~~~~~~~~~~~~~~^
        any(
        ^^^^
    ...<6 lines>...
        calls,
        ^^^^^^
    )
    ^
AssertionError: False is not true : ['identities /tmp/herdr-agents-test-hbo7dqqn/project claude-code', 'identities /tmp/herdr-agents-test-hbo7dqqn/project codex', 'workspace list', 'workspace create --cwd /tmp/herdr-agents-test-hbo7dqqn/project --label project agents --env CLICOLOR_FORCE=1 --env FORCE_COLOR=1 --env HERDR_AGENTS_LAYOUT=managed --focus', 'pane list --workspace w-test', 'pane rename w-test:p1 claude-orchestrator', 'pane process-info --pane w-test:p1', 'pane read w-test:p1 --source recent-unwrapped --lines 50', 'agent start claude-orchestrator-w-test --kind claude --pane w-test:p1 --timeout 30000 --', 'pane split w-test:p1 --direction right --cwd /tmp/herdr-agents-test-hbo7dqqn/project --env CLICOLOR_FORCE=1 --env FORCE_COLOR=1 --env AGMSG_RESOLVE_PROJECT=0 --no-focus', 'pane process-info --pane w-test:p3', 'pane read w-test:p3 --source recent-unwrapped --lines 50', 'pane run w-test:p3 unset GH_TOKEN GITHUB_TOKEN GH_ENTERPRISE_TOKEN GITHUB_ENTERPRISE_TOKEN; export GH_CONFIG_DIR=/tmp/herdr-agents-test-hbo7dqqn/home/.config/gh-worker', 'pane process-info --pane w-test:p3', 'pane read w-test:p3 --source recent-unwrapped --lines 50', 'agent start codex-worker-w-test --kind codex --pane w-test:p3 --timeout 30000 -- --sandbox workspace-write --profile express --ask-for-approval never -c sandbox_workspace_write.network_access=true -c shell_environment_policy.set.GH_CONFIG_DIR="/tmp/herdr-agents-test-hbo7dqqn/home/.config/gh-worker"', 'pane list --workspace w-test', 'pane rename w-test:p3 codex-worker', 'delivery set turn codex /tmp/herdr-agents-test-hbo7dqqn/project', 'delivery set both claude-code /tmp/herdr-agents-test-hbo7dqqn/project', 'doctor --project /tmp/herdr-agents-test-hbo7dqqn/project --type codex', 'identities /tmp/herdr-agents-test-hbo7dqqn/project codex', 'doctor --project /tmp/herdr-agents-test-hbo7dqqn/project --type claude-code', 'identities /tmp/herdr-agents-test-hbo7dqqn/project claude-code']

======================================================================
FAIL: test_full_mode_gives_a_codex_worker_its_worktree_git_metadata_roots (tests.unit.test_herdr_agents.HerdrAgentsTest.test_full_mode_gives_a_codex_worker_its_worktree_git_metadata_roots)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_herdr_agents.py", line 2353, in test_full_mode_gives_a_codex_worker_its_worktree_git_metadata_roots
    self.assertTrue(
    ~~~~~~~~~~~~~~~^
        starts[0].endswith(
        ^^^^^^^^^^^^^^^^^^^
    ...<2 lines>...
        starts[0],
        ^^^^^^^^^^
    )
    ^
AssertionError: False is not true : agent start codex-worker-w-test --kind codex --pane w-test:p3 --timeout 30000 -- --sandbox workspace-write --profile standard --ask-for-approval never -c sandbox_workspace_write.network_access=true -c shell_environment_policy.set.GH_CONFIG_DIR="/tmp/herdr-agents-test-ua46bhf4/home/.config/gh-worker" -c sandbox_workspace_write.writable_roots=["/tmp/herdr-agents-test-ua46bhf4/home/.agents/skills/agmsg/db","/tmp/herdr-agents-test-ua46bhf4/home/.agents/skills/agmsg/teams","/tmp/herdr-agents-test-ua46bhf4/home/.agents/skills/agmsg/run","/tmp/herdr-agents-test-ua46bhf4/home/.agents/skills/agmsg/ext-tools","/tmp/herdr-agents-test-ua46bhf4/project/.git/objects","/tmp/herdr-agents-test-ua46bhf4/project/.git/refs","/tmp/herdr-agents-test-ua46bhf4/project/.git/logs","/tmp/herdr-agents-test-ua46bhf4/project/.git/worktrees/worker-c"]

======================================================================
FAIL: test_full_mode_heal_never_starts_the_worker_in_an_exited_added_worker_pane (tests.unit.test_herdr_agents.HerdrAgentsTest.test_full_mode_heal_never_starts_the_worker_in_an_exited_added_worker_pane)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_herdr_agents.py", line 5102, in test_full_mode_heal_never_starts_the_worker_in_an_exited_added_worker_pane
    self.assertIn(
    ~~~~~~~~~~~~~^
        "agent start codex-worker-w-old --kind codex --pane w-old:p3 --timeout 30000 -- --sandbox workspace-write --profile standard --ask-for-approval never -c sandbox_workspace_write.network_access=true",
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        calls,
        ^^^^^^
    )
    ^
AssertionError: 'agent start codex-worker-w-old --kind codex --pane w-old:p3 --timeout 30000 -- --sandbox workspace-write --profile standard --ask-for-approval never -c sandbox_workspace_write.network_access=true' not found in ['workspace list', 'pane list --workspace w-old', 'pane list --workspace w-old', 'agent get codex-worker-w-old', 'pane split w-old:p1 --direction right --cwd /tmp/herdr-agents-test-uzwb5aln/project --env CLICOLOR_FORCE=1 --env FORCE_COLOR=1 --env AGMSG_RESOLVE_PROJECT=0 --no-focus', 'pane process-info --pane w-old:p3', 'pane read w-old:p3 --source recent-unwrapped --lines 50', 'pane run w-old:p3 unset GH_TOKEN GITHUB_TOKEN GH_ENTERPRISE_TOKEN GITHUB_ENTERPRISE_TOKEN; export GH_CONFIG_DIR=/tmp/herdr-agents-test-uzwb5aln/home/.config/gh-worker', 'pane process-info --pane w-old:p3', 'pane read w-old:p3 --source recent-unwrapped --lines 50', 'agent start codex-worker-w-old --kind codex --pane w-old:p3 --timeout 30000 -- --sandbox workspace-write --profile standard --ask-for-approval never -c sandbox_workspace_write.network_access=true -c shell_environment_policy.set.GH_CONFIG_DIR="/tmp/herdr-agents-test-uzwb5aln/home/.config/gh-worker"', 'pane list --workspace w-old', 'pane rename w-old:p3 codex-worker', 'pane list --workspace w-old', 'pane list --workspace w-old', 'workspace focus w-old']

======================================================================
FAIL: test_full_mode_heal_never_starts_the_worker_in_the_audit_pane (tests.unit.test_herdr_agents.HerdrAgentsTest.test_full_mode_heal_never_starts_the_worker_in_the_audit_pane)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_herdr_agents.py", line 5072, in test_full_mode_heal_never_starts_the_worker_in_the_audit_pane
    self.assertIn(
    ~~~~~~~~~~~~~^
        "agent start codex-worker-w-old --kind codex --pane w-old:p3 --timeout 30000 -- --sandbox workspace-write --profile standard --ask-for-approval never -c sandbox_workspace_write.network_access=true",
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        calls,
        ^^^^^^
    )
    ^
AssertionError: 'agent start codex-worker-w-old --kind codex --pane w-old:p3 --timeout 30000 -- --sandbox workspace-write --profile standard --ask-for-approval never -c sandbox_workspace_write.network_access=true' not found in ['workspace list', 'pane list --workspace w-old', 'pane list --workspace w-old', 'agent get codex-worker-w-old', 'pane split w-old:p1 --direction right --cwd /tmp/herdr-agents-test-f2b0zhj7/project --env CLICOLOR_FORCE=1 --env FORCE_COLOR=1 --env AGMSG_RESOLVE_PROJECT=0 --no-focus', 'pane process-info --pane w-old:p3', 'pane read w-old:p3 --source recent-unwrapped --lines 50', 'pane run w-old:p3 unset GH_TOKEN GITHUB_TOKEN GH_ENTERPRISE_TOKEN GITHUB_ENTERPRISE_TOKEN; export GH_CONFIG_DIR=/tmp/herdr-agents-test-f2b0zhj7/home/.config/gh-worker', 'pane process-info --pane w-old:p3', 'pane read w-old:p3 --source recent-unwrapped --lines 50', 'agent start codex-worker-w-old --kind codex --pane w-old:p3 --timeout 30000 -- --sandbox workspace-write --profile standard --ask-for-approval never -c sandbox_workspace_write.network_access=true -c shell_environment_policy.set.GH_CONFIG_DIR="/tmp/herdr-agents-test-f2b0zhj7/home/.config/gh-worker"', 'pane list --workspace w-old', 'pane rename w-old:p3 codex-worker', 'pane list --workspace w-old', 'pane list --workspace w-old', 'workspace focus w-old']

======================================================================
FAIL: test_restart_worker_refuses_when_the_pane_never_reaches_a_shell (tests.unit.test_herdr_agents.HerdrAgentsTest.test_restart_worker_refuses_when_the_pane_never_reaches_a_shell)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_herdr_agents.py", line 3819, in test_restart_worker_refuses_when_the_pane_never_reaches_a_shell
    self.assertIn(
    ~~~~~~~~~~~~~^
        "did not reach an interactive shell prompt; refusing agent start",
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        result.stderr,
        ^^^^^^^^^^^^^^
    )
    ^
AssertionError: 'did not reach an interactive shell prompt; refusing agent start' not found in 'Herdr worker pane w-old:p2 is not shell-ready; refusing identity setup.\n'

======================================================================
FAIL: test_uses_initial_workspace_pane_for_claude_and_splits_codex_right (tests.unit.test_herdr_agents.HerdrAgentsTest.test_uses_initial_workspace_pane_for_claude_and_splits_codex_right)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_herdr_agents.py", line 1278, in test_uses_initial_workspace_pane_for_claude_and_splits_codex_right
    self.assertIn(
    ~~~~~~~~~~~~~^
        "agent start codex-worker-w-test --kind codex --pane w-test:p3 --timeout 30000 -- --sandbox workspace-write --profile standard --ask-for-approval never -c sandbox_workspace_write.network_access=true",
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        calls,
        ^^^^^^
    )
    ^
AssertionError: 'agent start codex-worker-w-test --kind codex --pane w-test:p3 --timeout 30000 -- --sandbox workspace-write --profile standard --ask-for-approval never -c sandbox_workspace_write.network_access=true' not found in ['workspace list', 'workspace create --cwd /tmp/herdr-agents-test-h5djdmxy/project --label project agents --env CLICOLOR_FORCE=1 --env FORCE_COLOR=1 --env HERDR_AGENTS_LAYOUT=managed --focus', 'pane list --workspace w-test', 'pane rename w-test:p1 claude-orchestrator', 'pane process-info --pane w-test:p1', 'pane read w-test:p1 --source recent-unwrapped --lines 50', 'agent start claude-orchestrator-w-test --kind claude --pane w-test:p1 --timeout 30000 --', 'pane split w-test:p1 --direction right --cwd /tmp/herdr-agents-test-h5djdmxy/project --env CLICOLOR_FORCE=1 --env FORCE_COLOR=1 --env AGMSG_RESOLVE_PROJECT=0 --no-focus', 'pane process-info --pane w-test:p3', 'pane read w-test:p3 --source recent-unwrapped --lines 50', 'pane run w-test:p3 unset GH_TOKEN GITHUB_TOKEN GH_ENTERPRISE_TOKEN GITHUB_ENTERPRISE_TOKEN; export GH_CONFIG_DIR=/tmp/herdr-agents-test-h5djdmxy/home/.config/gh-worker', 'pane process-info --pane w-test:p3', 'pane read w-test:p3 --source recent-unwrapped --lines 50', 'agent start codex-worker-w-test --kind codex --pane w-test:p3 --timeout 30000 -- --sandbox workspace-write --profile standard --ask-for-approval never -c sandbox_workspace_write.network_access=true -c shell_environment_policy.set.GH_CONFIG_DIR="/tmp/herdr-agents-test-h5djdmxy/home/.config/gh-worker"', 'pane list --workspace w-test', 'pane rename w-test:p3 codex-worker']

======================================================================
FAIL: test_worker_kind_claude_appends_extra_worker_args (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_kind_claude_appends_extra_worker_args)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_herdr_agents.py", line 1990, in test_worker_kind_claude_appends_extra_worker_args
    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 2 != 0 : orchestrator_profile=none args=none
/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents: line 2582: syntax error near unexpected token `)'


======================================================================
FAIL: test_worker_profile_defaults_to_generated_worker_profile (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_profile_defaults_to_generated_worker_profile)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_herdr_agents.py", line 1394, in test_worker_profile_defaults_to_generated_worker_profile
    self.assertTrue(
    ~~~~~~~~~~~~~~~^
        any(
        ^^^^
    ...<5 lines>...
        )
        ^
    )
    ^
AssertionError: False is not true

======================================================================
FAIL: test_worker_profile_env_override_wins_over_generated_worker_profile (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_profile_env_override_wins_over_generated_worker_profile)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_herdr_agents.py", line 1414, in test_worker_profile_env_override_wins_over_generated_worker_profile
    self.assertTrue(
    ~~~~~~~~~~~~~~~^
        any(
        ^^^^
    ...<5 lines>...
        )
        ^
    )
    ^
AssertionError: False is not true

======================================================================
FAIL: test_github_identity_gate_activation_and_current_head_approval (tests.unit.test_require_crit_review.ReviewGuardTest.test_github_identity_gate_activation_and_current_head_approval) (label='active')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_require_crit_review.py", line 457, in test_github_identity_gate_activation_and_current_head_approval
    "later-submitted-change-request",
AssertionError: 0 != 1 : PR feedback evidence is incomplete; run scripts/pr-feedback.py and disposition every item.
- GitHub role gate: could not verify provisioning, effective rules or current-head approval; refusing integration


======================================================================
FAIL: test_github_identity_gate_activation_and_current_head_approval (tests.unit.test_require_crit_review.ReviewGuardTest.test_github_identity_gate_activation_and_current_head_approval) (label='comment after approval')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_require_crit_review.py", line 457, in test_github_identity_gate_activation_and_current_head_approval
    "later-submitted-change-request",
AssertionError: 0 != 1 : PR feedback evidence is incomplete; run scripts/pr-feedback.py and disposition every item.
- GitHub role gate: could not verify provisioning, effective rules or current-head approval; refusing integration


----------------------------------------------------------------------
Ran 388 tests in 170.490s

FAILED (failures=16)
```

## make unit-test; UV_CACHE_DIR=/tmp/t90-uv-cache; exit 0

```text
uv run python -m unittest discover -s tests/unit -v
test_bounded_scan_finishes_under_wall_limit (test_agent_session_staleness.AgentSessionStalenessTest.test_bounded_scan_finishes_under_wall_limit) ... ok
test_check_is_silent_when_assets_predate_session (test_agent_session_staleness.AgentSessionStalenessTest.test_check_is_silent_when_assets_predate_session) ... ok
test_check_reports_new_versions_and_mtimes_deduplicated_by_root (test_agent_session_staleness.AgentSessionStalenessTest.test_check_reports_new_versions_and_mtimes_deduplicated_by_root) ... ok
test_doctor_delegates_session_staleness_to_installed_script (test_agent_session_staleness.AgentSessionStalenessTest.test_doctor_delegates_session_staleness_to_installed_script) ... ok
test_hook_first_call_writes_private_baseline_and_is_silent (test_agent_session_staleness.AgentSessionStalenessTest.test_hook_first_call_writes_private_baseline_and_is_silent) ... ok
test_hook_missing_or_garbage_stdin_is_silent_success (test_agent_session_staleness.AgentSessionStalenessTest.test_hook_missing_or_garbage_stdin_is_silent_success) ... ok
test_hook_prunes_state_files_older_than_seven_days (test_agent_session_staleness.AgentSessionStalenessTest.test_hook_prunes_state_files_older_than_seven_days) ... ok
test_hook_second_call_detects_asset_updated_after_baseline (test_agent_session_staleness.AgentSessionStalenessTest.test_hook_second_call_detects_asset_updated_after_baseline) ... ok
test_internal_failure_is_silent_success_with_one_stderr_line (test_agent_session_staleness.AgentSessionStalenessTest.test_internal_failure_is_silent_success_with_one_stderr_line) ... ok
test_no_arguments_prints_ten_recent_updates (test_agent_session_staleness.AgentSessionStalenessTest.test_no_arguments_prints_ten_recent_updates) ... ok
test_runtime_state_and_sqlite_files_are_excluded (test_agent_session_staleness.AgentSessionStalenessTest.test_runtime_state_and_sqlite_files_are_excluded) ... ok
test_ceiling_directories_do_not_hide_the_seat (test_agent_stop_gate.AgentStopGateTest.test_ceiling_directories_do_not_hide_the_seat) ... ok
test_character_device_placeholder_is_skipped (test_agent_stop_gate.AgentStopGateTest.test_character_device_placeholder_is_skipped) ... ok
test_checkout_outside_any_seat_passes (test_agent_stop_gate.AgentStopGateTest.test_checkout_outside_any_seat_passes) ... ok
test_clean_orchestrator_passes (test_agent_stop_gate.AgentStopGateTest.test_clean_orchestrator_passes) ... ok
test_every_team_of_the_identity_is_checked (test_agent_stop_gate.AgentStopGateTest.test_every_team_of_the_identity_is_checked) ... ok
test_failing_git_status_blocks (test_agent_stop_gate.AgentStopGateTest.test_failing_git_status_blocks) ... ok
test_failing_identity_lookup_blocks_once (test_agent_stop_gate.AgentStopGateTest.test_failing_identity_lookup_blocks_once) ... ok
test_inherited_alternate_index_does_not_hide_a_staged_change (test_agent_stop_gate.AgentStopGateTest.test_inherited_alternate_index_does_not_hide_a_staged_change) ... ok
test_inherited_git_dir_does_not_hide_the_seat (test_agent_stop_gate.AgentStopGateTest.test_inherited_git_dir_does_not_hide_the_seat) ... ok
test_injected_git_config_does_not_hide_untracked_files (test_agent_stop_gate.AgentStopGateTest.test_injected_git_config_does_not_hide_untracked_files) ... ok
test_json_escaped_cwd_resolves (test_agent_stop_gate.AgentStopGateTest.test_json_escaped_cwd_resolves) ... ok
test_missing_agmsg_install_passes (test_agent_stop_gate.AgentStopGateTest.test_missing_agmsg_install_passes) ... ok
test_mountinfo_cannot_be_redirected_through_the_environment (test_agent_stop_gate.AgentStopGateTest.test_mountinfo_cannot_be_redirected_through_the_environment) ... ok
test_null_device_of_another_filesystem_is_not_a_placeholder (test_agent_stop_gate.AgentStopGateTest.test_null_device_of_another_filesystem_is_not_a_placeholder) ... ok
test_orchestrator_acceptance_to_another_member_keeps_the_result_open (test_agent_stop_gate.AgentStopGateTest.test_orchestrator_acceptance_to_another_member_keeps_the_result_open) ... ok
test_project_dir_anchors_the_seat_after_a_cd (test_agent_stop_gate.AgentStopGateTest.test_project_dir_anchors_the_seat_after_a_cd) ... ok
test_read_only_bind_of_another_empty_file_is_not_a_placeholder (test_agent_stop_gate.AgentStopGateTest.test_read_only_bind_of_another_empty_file_is_not_a_placeholder) ... ok
test_read_write_mount_is_not_a_placeholder (test_agent_stop_gate.AgentStopGateTest.test_read_write_mount_is_not_a_placeholder) ... ok
test_result_then_acceptance_passes (test_agent_stop_gate.AgentStopGateTest.test_result_then_acceptance_passes) ... ok
test_result_then_revision_task_passes (test_agent_stop_gate.AgentStopGateTest.test_result_then_revision_task_passes) ... ok
test_result_without_acceptance_blocks (test_agent_stop_gate.AgentStopGateTest.test_result_without_acceptance_blocks) ... ok
test_same_named_file_bound_from_elsewhere_is_not_a_placeholder (test_agent_stop_gate.AgentStopGateTest.test_same_named_file_bound_from_elsewhere_is_not_a_placeholder) ... ok
test_sandbox_placeholders_are_skipped (test_agent_stop_gate.AgentStopGateTest.test_sandbox_placeholders_are_skipped) ... ok
test_sandbox_placeholders_on_a_separate_filesystem_are_skipped (test_agent_stop_gate.AgentStopGateTest.test_sandbox_placeholders_on_a_separate_filesystem_are_skipped) ... ok
test_separate_git_dir_main_worktree_is_a_seat (test_agent_stop_gate.AgentStopGateTest.test_separate_git_dir_main_worktree_is_a_seat) ... ok
test_slow_store_blocks_within_the_budget (test_agent_stop_gate.AgentStopGateTest.test_slow_store_blocks_within_the_budget) ... ok
test_slow_store_blocks_within_the_budget_with_gtimeout_only (test_agent_stop_gate.AgentStopGateTest.test_slow_store_blocks_within_the_budget_with_gtimeout_only) ... ok
test_slow_store_blocks_within_the_budget_without_timeout (test_agent_stop_gate.AgentStopGateTest.test_slow_store_blocks_within_the_budget_without_timeout) ... ok
test_solo_unsuffixed_worker_is_gated (test_agent_stop_gate.AgentStopGateTest.test_solo_unsuffixed_worker_is_gated) ... ok
test_sqlite_store_off_the_current_schema_is_not_initialized (test_agent_stop_gate.AgentStopGateTest.test_sqlite_store_off_the_current_schema_is_not_initialized) ... ok
test_staged_rename_out_of_orchestration_blocks (test_agent_stop_gate.AgentStopGateTest.test_staged_rename_out_of_orchestration_blocks) ... ok
test_stop_hook_active_skips_only_the_dirty_tree_check (test_agent_stop_gate.AgentStopGateTest.test_stop_hook_active_skips_only_the_dirty_tree_check) ... ok
test_unreadable_store_blocks_once (test_agent_stop_gate.AgentStopGateTest.test_unreadable_store_blocks_once) ... ok
test_untracked_file_outside_orchestration_blocks (test_agent_stop_gate.AgentStopGateTest.test_untracked_file_outside_orchestration_blocks) ... ok
test_untracked_symlink_to_a_mount_point_is_not_a_placeholder (test_agent_stop_gate.AgentStopGateTest.test_untracked_symlink_to_a_mount_point_is_not_a_placeholder) ... ok
test_untrusted_filenames_are_quoted (test_agent_stop_gate.AgentStopGateTest.test_untrusted_filenames_are_quoted) ... ok
test_user_bind_mount_of_a_real_file_is_not_a_placeholder (test_agent_stop_gate.AgentStopGateTest.test_user_bind_mount_of_a_real_file_is_not_a_placeholder) ... ok
test_whole_filesystem_bind_is_not_a_placeholder (test_agent_stop_gate.AgentStopGateTest.test_whole_filesystem_bind_is_not_a_placeholder) ... ok
test_worker_after_result_passes (test_agent_stop_gate.AgentStopGateTest.test_worker_after_result_passes) ... ok
test_worker_alive_pong_keeps_the_task_open (test_agent_stop_gate.AgentStopGateTest.test_worker_alive_pong_keeps_the_task_open) ... ok
test_worker_blocked_pong_closes_the_task (test_agent_stop_gate.AgentStopGateTest.test_worker_blocked_pong_closes_the_task) ... ok
test_worker_result_to_another_member_keeps_the_task_open (test_agent_stop_gate.AgentStopGateTest.test_worker_result_to_another_member_keeps_the_task_open) ... ok
test_worker_revise_acceptance_reopens_the_task (test_agent_stop_gate.AgentStopGateTest.test_worker_revise_acceptance_reopens_the_task) ... ok
test_worker_task_closed_by_a_non_revise_acceptance (test_agent_stop_gate.AgentStopGateTest.test_worker_task_closed_by_a_non_revise_acceptance) ... ok
test_worker_task_newer_than_result_blocks (test_agent_stop_gate.AgentStopGateTest.test_worker_task_newer_than_result_blocks) ... ok
test_worker_tracks_each_task_id (test_agent_stop_gate.AgentStopGateTest.test_worker_tracks_each_task_id) ... ok
test_default_store_uses_shared_helper (test_agmsg_dispatch.AgmsgDispatchTest.test_default_store_uses_shared_helper) ... ok
test_idle_wakes_once_and_reads (test_agmsg_dispatch.AgmsgDispatchTest.test_idle_wakes_once_and_reads) ... ok
test_invalid_timeout_does_not_send (test_agmsg_dispatch.AgmsgDispatchTest.test_invalid_timeout_does_not_send) ... ok
test_missing_pane_inserts_nothing (test_agmsg_dispatch.AgmsgDispatchTest.test_missing_pane_inserts_nothing) ... ok
test_rejects_identifiers_outside_the_strict_grammar (test_agmsg_dispatch.AgmsgDispatchTest.test_rejects_identifiers_outside_the_strict_grammar) ... ok
test_retry_does_not_wake_newly_working_pane (test_agmsg_dispatch.AgmsgDispatchTest.test_retry_does_not_wake_newly_working_pane) ... ok
test_timeout_is_one_shared_budget (test_agmsg_dispatch.AgmsgDispatchTest.test_timeout_is_one_shared_budget) ... ok
test_unread_retries_once_then_fails (test_agmsg_dispatch.AgmsgDispatchTest.test_unread_retries_once_then_fails) ... ok
test_wake_failure_identifies_sent_message (test_agmsg_dispatch.AgmsgDispatchTest.test_wake_failure_identifies_sent_message) ... ok
test_worker_becoming_idle_after_send_is_woken (test_agmsg_dispatch.AgmsgDispatchTest.test_worker_becoming_idle_after_send_is_woken) ... ok
test_working_does_not_wake (test_agmsg_dispatch.AgmsgDispatchTest.test_working_does_not_wake) ... ok
test_working_unread_never_wakes (test_agmsg_dispatch.AgmsgDispatchTest.test_working_unread_never_wakes) ... ok
test_docs_no_longer_name_codex_review_commit (test_agmsg_orchestration_docs.AgmsgOrchestrationDocsParityTest.test_docs_no_longer_name_codex_review_commit) ... ok
test_rule_and_skill_share_the_audit_gate_and_bot_wait_invariants (test_agmsg_orchestration_docs.AgmsgOrchestrationDocsParityTest.test_rule_and_skill_share_the_audit_gate_and_bot_wait_invariants) ... ok
test_rule_and_skill_share_the_parallel_execution_and_routing_invariants (test_agmsg_orchestration_docs.AgmsgOrchestrationDocsParityTest.test_rule_and_skill_share_the_parallel_execution_and_routing_invariants) ... ok
test_rule_and_skill_share_the_registration_and_delivery_invariants (test_agmsg_orchestration_docs.AgmsgOrchestrationDocsParityTest.test_rule_and_skill_share_the_registration_and_delivery_invariants) ... ok
test_rule_drops_the_worker_network_escalation (test_agmsg_orchestration_docs.AgmsgOrchestrationDocsParityTest.test_rule_drops_the_worker_network_escalation) ... ok
test_skill_drops_the_pane_status_gate_and_raw_pane_wakes (test_agmsg_orchestration_docs.AgmsgOrchestrationDocsParityTest.test_skill_drops_the_pane_status_gate_and_raw_pane_wakes) ... ok
test_doctor_fails_when_bwrap_is_missing_with_codex (test_apparmor_userns.AppArmorUsernsTest.test_doctor_fails_when_bwrap_is_missing_with_codex) ... ok
test_doctor_fails_when_the_bwrap_probe_fails (test_apparmor_userns.AppArmorUsernsTest.test_doctor_fails_when_the_bwrap_probe_fails) ... ok
test_doctor_is_not_applicable_without_the_restriction (test_apparmor_userns.AppArmorUsernsTest.test_doctor_is_not_applicable_without_the_restriction) ... ok
test_doctor_passes_when_the_bwrap_probe_succeeds (test_apparmor_userns.AppArmorUsernsTest.test_doctor_passes_when_the_bwrap_probe_succeeds) ... ok
test_doctor_warns_optionally_when_codex_is_missing (test_apparmor_userns.AppArmorUsernsTest.test_doctor_warns_optionally_when_codex_is_missing) ... ok
test_installer_copies_and_reloads_the_profile_with_sudo (test_apparmor_userns.AppArmorUsernsTest.test_installer_copies_and_reloads_the_profile_with_sudo) ... ok
test_installer_fails_when_loading_the_profile_fails (test_apparmor_userns.AppArmorUsernsTest.test_installer_fails_when_loading_the_profile_fails) ... ok
test_installer_is_a_no_op_when_the_host_does_not_need_the_profile (test_apparmor_userns.AppArmorUsernsTest.test_installer_is_a_no_op_when_the_host_does_not_need_the_profile) ... ok
test_installer_leaves_the_profile_pending_without_cached_sudo (test_apparmor_userns.AppArmorUsernsTest.test_installer_leaves_the_profile_pending_without_cached_sudo) ... ok
test_wrapper_re_renders_when_prerequisites_change (test_apparmor_userns.AppArmorUsernsTest.test_wrapper_re_renders_when_prerequisites_change) ... ok
test_chezmoi_rendered_updater_uses_exported_source_root (test_asset_manifest.AssetManifestTest.test_chezmoi_rendered_updater_uses_exported_source_root) ... ok
test_chezmoi_rendered_updater_uses_inlined_manifest_library (test_asset_manifest.AssetManifestTest.test_chezmoi_rendered_updater_uses_inlined_manifest_library) ... ok
test_chezmoi_wrapper_renders_shebang_and_source_root (test_asset_manifest.AssetManifestTest.test_chezmoi_wrapper_renders_shebang_and_source_root) ... ok
test_failed_atomic_commit_leaves_previous_manifest_intact (test_asset_manifest.AssetManifestTest.test_failed_atomic_commit_leaves_previous_manifest_intact) ... ok
test_records_schema_two_steps_and_replaces_one_whole_entry (test_asset_manifest.AssetManifestTest.test_records_schema_two_steps_and_replaces_one_whole_entry) ... ok
test_rendered_updater_fails_when_no_source_root_is_valid (test_asset_manifest.AssetManifestTest.test_rendered_updater_fails_when_no_source_root_is_valid) ... ok
test_same_run_mise_repairs_preserve_both_identity_steps (test_asset_manifest.AssetManifestTest.test_same_run_mise_repairs_preserve_both_identity_steps) ... ok
test_two_real_install_steps_record_under_fake_home (test_asset_manifest.AssetManifestTest.test_two_real_install_steps_record_under_fake_home) ... ok
test_unwritable_destination_warns_once_without_failing (test_asset_manifest.AssetManifestTest.test_unwritable_destination_warns_once_without_failing) ... ok
test_updater_direct_source_resolves_repository_root (test_asset_manifest.AssetManifestTest.test_updater_direct_source_resolves_repository_root) ... ok
test_updater_has_one_recording_call_for_each_install_step (test_asset_manifest.AssetManifestTest.test_updater_has_one_recording_call_for_each_install_step) ... ok
test_exit_zero_install_with_expected_fake_binary_passes_postcondition (test_aws_cli_acquisition.AwsCliAcquisitionTest.test_exit_zero_install_with_expected_fake_binary_passes_postcondition) ... ok
test_exit_zero_install_with_wrong_version_fails_postcondition (test_aws_cli_acquisition.AwsCliAcquisitionTest.test_exit_zero_install_with_wrong_version_fails_postcondition) ... ok
test_exit_zero_partial_install_without_binary_fails_postcondition (test_aws_cli_acquisition.AwsCliAcquisitionTest.test_exit_zero_partial_install_without_binary_fails_postcondition) ... ok
test_gpgv_failure_preserves_existing_aws_and_skips_unzip (test_aws_cli_acquisition.AwsCliAcquisitionTest.test_gpgv_failure_preserves_existing_aws_and_skips_unzip) ... ok
test_key_metadata_failures_stop_before_dearmor_and_gpgv (test_aws_cli_acquisition.AwsCliAcquisitionTest.test_key_metadata_failures_stop_before_dearmor_and_gpgv) ... ok
test_linux_urls_are_versioned_and_unknown_architecture_fails (test_aws_cli_acquisition.AwsCliAcquisitionTest.test_linux_urls_are_versioned_and_unknown_architecture_fails) ... ok
test_platform_package_managers_and_wrapper_own_aws_cli (test_aws_cli_acquisition.AwsCliAcquisitionTest.test_platform_package_managers_and_wrapper_own_aws_cli) ... ok
test_repository_key_has_expected_current_fingerprint (test_aws_cli_acquisition.AwsCliAcquisitionTest.test_repository_key_has_expected_current_fingerprint) ... ok
test_verified_archive_runs_installer_with_user_local_update_arguments (test_aws_cli_acquisition.AwsCliAcquisitionTest.test_verified_archive_runs_installer_with_user_local_update_arguments) ... ok
test_wrong_staged_version_preserves_existing_aws_and_skips_installer (test_aws_cli_acquisition.AwsCliAcquisitionTest.test_wrong_staged_version_preserves_existing_aws_and_skips_installer) ... ok
test_agmsg_runtime_paths_are_ignored_on_both_sides (test_check_agent_runtime.CheckAgentRuntimeTest.test_agmsg_runtime_paths_are_ignored_on_both_sides) ... ok
test_agmsg_separate_store_prefix_is_ignored (test_check_agent_runtime.CheckAgentRuntimeTest.test_agmsg_separate_store_prefix_is_ignored) ... ok
test_asset_repair_invokes_only_the_detected_step (test_check_agent_runtime.CheckAgentRuntimeTest.test_asset_repair_invokes_only_the_detected_step) ... ok
test_check_includes_ua_core_warnings (test_check_agent_runtime.CheckAgentRuntimeTest.test_check_includes_ua_core_warnings) ... /home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/pathlib/_local.py:128: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f2764fc40>
  path = os.fspath(arg)
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/pathlib/_local.py:128: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f2764fb50>
  path = os.fspath(arg)
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/pathlib/_local.py:128: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f271434c0>
  path = os.fspath(arg)
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/pathlib/_local.py:128: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f271433d0>
  path = os.fspath(arg)
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/pathlib/_local.py:128: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f271432e0>
  path = os.fspath(arg)
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/pathlib/_local.py:128: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f27143100>
  path = os.fspath(arg)
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/pathlib/_local.py:128: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f27142f20>
  path = os.fspath(arg)
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/pathlib/_local.py:128: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f271436a0>
  path = os.fspath(arg)
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/pathlib/_local.py:128: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f27143970>
  path = os.fspath(arg)
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/pathlib/_local.py:128: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f27143a60>
  path = os.fspath(arg)
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/pathlib/_local.py:128: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f27143b50>
  path = os.fspath(arg)
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/pathlib/_local.py:128: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f27143c40>
  path = os.fspath(arg)
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/pathlib/_local.py:128: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f27143d30>
  path = os.fspath(arg)
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/pathlib/_local.py:128: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f27143e20>
  path = os.fspath(arg)
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/pathlib/_local.py:128: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f27143f10>
  path = os.fspath(arg)
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/pathlib/_local.py:128: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f26cfc040>
  path = os.fspath(arg)
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/pathlib/_local.py:128: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f26cfc130>
  path = os.fspath(arg)
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/pathlib/_local.py:128: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f26cfc220>
  path = os.fspath(arg)
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/pathlib/_local.py:128: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f275c7880>
  path = os.fspath(arg)
ResourceWarning: Enable tracemalloc to get the object allocation traceback
ok
test_check_uses_same_modified_for_codex_profiles (test_check_agent_runtime.CheckAgentRuntimeTest.test_check_uses_same_modified_for_codex_profiles) ... ok
test_chezmoi_drift_status_failure_is_warning (test_check_agent_runtime.CheckAgentRuntimeTest.test_chezmoi_drift_status_failure_is_warning) ... ok
test_chezmoi_drift_warnings_classify_status_and_mode_only (test_check_agent_runtime.CheckAgentRuntimeTest.test_chezmoi_drift_warnings_classify_status_and_mode_only) ... ok
test_compare_claude_skills_ignores_cowork_synced_subtree (test_check_agent_runtime.CheckAgentRuntimeTest.test_compare_claude_skills_ignores_cowork_synced_subtree) ... ok
test_content_drift_still_fails (test_check_agent_runtime.CheckAgentRuntimeTest.test_content_drift_still_fails) ... ok
test_crit_codex_skills_are_not_orphans (test_check_agent_runtime.CheckAgentRuntimeTest.test_crit_codex_skills_are_not_orphans) ... ok
test_deleted_shared_skill_file_repair_converges (test_check_agent_runtime.CheckAgentRuntimeTest.test_deleted_shared_skill_file_repair_converges) ... ok
test_every_generated_chezmoi_repair_action_is_forced (test_check_agent_runtime.CheckAgentRuntimeTest.test_every_generated_chezmoi_repair_action_is_forced) ... ok
test_executable_prefix_is_compared_against_deployed_name (test_check_agent_runtime.CheckAgentRuntimeTest.test_executable_prefix_is_compared_against_deployed_name) ... ok
test_executable_prefix_requires_deployed_execute_bit (test_check_agent_runtime.CheckAgentRuntimeTest.test_executable_prefix_requires_deployed_execute_bit) ... ok
test_execute_repair_calls_each_mapped_command_once (test_check_agent_runtime.CheckAgentRuntimeTest.test_execute_repair_calls_each_mapped_command_once) ... ok
test_ignored_paths_suppress_receipt_linked_tree_entries (test_check_agent_runtime.CheckAgentRuntimeTest.test_ignored_paths_suppress_receipt_linked_tree_entries) ... ok
test_installed_manifest_integrity_reasons (test_check_agent_runtime.CheckAgentRuntimeTest.test_installed_manifest_integrity_reasons) ... ok
test_installer_owned_agmsg_skill_and_backups_are_not_orphans (test_check_agent_runtime.CheckAgentRuntimeTest.test_installer_owned_agmsg_skill_and_backups_are_not_orphans) ... ok
test_invalid_manifest_is_one_error_and_skips_dependent_checks (test_check_agent_runtime.CheckAgentRuntimeTest.test_invalid_manifest_is_one_error_and_skips_dependent_checks) ... ok
test_json_modifier_accepts_cosmetic_reserialization (test_check_agent_runtime.CheckAgentRuntimeTest.test_json_modifier_accepts_cosmetic_reserialization) ... ok
test_json_modifier_rejects_real_value_drift (test_check_agent_runtime.CheckAgentRuntimeTest.test_json_modifier_rejects_real_value_drift) ... ok
test_managed_top_level_extra_still_fails_with_unmanaged_warning_mode (test_check_agent_runtime.CheckAgentRuntimeTest.test_managed_top_level_extra_still_fails_with_unmanaged_warning_mode) ... ok
test_manifest_drift_requires_recorded_step_with_missing_path (test_check_agent_runtime.CheckAgentRuntimeTest.test_manifest_drift_requires_recorded_step_with_missing_path) ... ok
test_missing_crit_asset_is_repairable (test_check_agent_runtime.CheckAgentRuntimeTest.test_missing_crit_asset_is_repairable) ... ok
test_missing_terminal_browser_receipt_is_harmless (test_check_agent_runtime.CheckAgentRuntimeTest.test_missing_terminal_browser_receipt_is_harmless) ... ok
test_only_exact_agmsg_root_legacy_database_names_are_ignored (test_check_agent_runtime.CheckAgentRuntimeTest.test_only_exact_agmsg_root_legacy_database_names_are_ignored) ... ok
test_orchestrator_seat_lock_is_quiet_for_a_composite_id_or_no_live_session (test_check_agent_runtime.CheckAgentRuntimeTest.test_orchestrator_seat_lock_is_quiet_for_a_composite_id_or_no_live_session) ... ok
test_orchestrator_seat_lock_warns_on_a_bare_session_id (test_check_agent_runtime.CheckAgentRuntimeTest.test_orchestrator_seat_lock_warns_on_a_bare_session_id) ... ok
test_orphan_detection_classifies_accounted_stale_and_orphan (test_check_agent_runtime.CheckAgentRuntimeTest.test_orphan_detection_classifies_accounted_stale_and_orphan) ... ok
test_parameterized_mise_step_uses_key_identity (test_check_agent_runtime.CheckAgentRuntimeTest.test_parameterized_mise_step_uses_key_identity) ... ok
test_private_prefix_is_compared_against_deployed_name (test_check_agent_runtime.CheckAgentRuntimeTest.test_private_prefix_is_compared_against_deployed_name) ... ok
test_repair_actions_map_only_detected_file_drift (test_check_agent_runtime.CheckAgentRuntimeTest.test_repair_actions_map_only_detected_file_drift) ... ok
test_repair_mode_converges_once_and_reports_each_action (test_check_agent_runtime.CheckAgentRuntimeTest.test_repair_mode_converges_once_and_reports_each_action) ... ok
test_repair_mode_fails_after_one_non_convergent_round (test_check_agent_runtime.CheckAgentRuntimeTest.test_repair_mode_fails_after_one_non_convergent_round) ... ok
test_repair_mode_never_acts_on_stale_or_orphan_warnings (test_check_agent_runtime.CheckAgentRuntimeTest.test_repair_mode_never_acts_on_stale_or_orphan_warnings) ... ok
test_repair_unset_is_byte_identical_and_never_mutates (test_check_agent_runtime.CheckAgentRuntimeTest.test_repair_unset_is_byte_identical_and_never_mutates) ... ok
test_sourced_asset_repair_runs_no_main_or_sibling_step (test_check_agent_runtime.CheckAgentRuntimeTest.test_sourced_asset_repair_runs_no_main_or_sibling_step) ... ok
test_terminal_browser_receipt_links_are_not_orphans (test_check_agent_runtime.CheckAgentRuntimeTest.test_terminal_browser_receipt_links_are_not_orphans) ... ok
test_ua_core_is_quiet_when_dist_is_fresh_or_no_clone_exists (test_check_agent_runtime.CheckAgentRuntimeTest.test_ua_core_is_quiet_when_dist_is_fresh_or_no_clone_exists) ... ok
test_ua_core_warns_when_dist_is_older_than_src (test_check_agent_runtime.CheckAgentRuntimeTest.test_ua_core_warns_when_dist_is_older_than_src) ... ok
test_ua_core_warns_when_dist_is_older_than_the_root_lockfile (test_check_agent_runtime.CheckAgentRuntimeTest.test_ua_core_warns_when_dist_is_older_than_the_root_lockfile) ... ok
test_ua_core_warns_when_the_codex_clone_has_no_built_dist (test_check_agent_runtime.CheckAgentRuntimeTest.test_ua_core_warns_when_the_codex_clone_has_no_built_dist) ... ok
test_unexpected_non_runtime_file_still_fails (test_check_agent_runtime.CheckAgentRuntimeTest.test_unexpected_non_runtime_file_still_fails) ... ok
test_unmanaged_top_level_skill_dir_warns (test_check_agent_runtime.CheckAgentRuntimeTest.test_unmanaged_top_level_skill_dir_warns) ... ok
test_apply_removes_the_symlink_farm_and_keeps_installer_owned_paths (test_chezmoiremove_agmsg.ChezmoiRemoveAgmsgTest.test_apply_removes_the_symlink_farm_and_keeps_installer_owned_paths) ... ok
test_retired_targets_are_listed_and_have_no_source (test_chezmoiremove_agmsg.ChezmoiRemoveRetiredShellFilesTest.test_retired_targets_are_listed_and_have_no_source) ... ok
test_current_only_key_is_preserved (test_claude_settings_merge.ClaudeSettingsMergeTest.test_current_only_key_is_preserved) ... ok
test_current_session_start_order_is_preserved (test_claude_settings_merge.ClaudeSettingsMergeTest.test_current_session_start_order_is_preserved)
Order is preserved; a stale bare herdr-agents command still migrates. ... ok
test_desired_current_output_is_byte_identical (test_claude_settings_merge.ClaudeSettingsMergeTest.test_desired_current_output_is_byte_identical) ... ok
test_empty_stdin_outputs_managed (test_claude_settings_merge.ClaudeSettingsMergeTest.test_empty_stdin_outputs_managed) ... ok
test_enabled_plugins_are_preserved_from_current (test_claude_settings_merge.ClaudeSettingsMergeTest.test_enabled_plugins_are_preserved_from_current) ... ok
test_invalid_json_outputs_managed (test_claude_settings_merge.ClaudeSettingsMergeTest.test_invalid_json_outputs_managed) ... ok
test_managed_hook_object_key_order_is_preserved (test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_hook_object_key_order_is_preserved) ... ok
test_managed_permgate_replaces_stale_current_ccgate_hook (test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_permgate_replaces_stale_current_ccgate_hook) ... ok
test_managed_session_start_replacement_keeps_hook_order (test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_session_start_replacement_keeps_hook_order)
Replacing a managed entry must not reorder SessionStart. ... ok
test_managed_session_start_replaces_stale_hard_coded_home_hook (test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_session_start_replaces_stale_hard_coded_home_hook)
Upgrade path: a machine that received the old hard-coded managed hook. ... ok
test_managed_wins_for_managed_key (test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_wins_for_managed_key) ... ok
test_merge_is_idempotent (test_claude_settings_merge.ClaudeSettingsMergeTest.test_merge_is_idempotent) ... ok
test_permission_merge_preserves_custom_hook_in_mixed_entry (test_claude_settings_merge.ClaudeSettingsMergeTest.test_permission_merge_preserves_custom_hook_in_mixed_entry) ... ok
test_permission_merge_preserves_unrelated_current_hooks (test_claude_settings_merge.ClaudeSettingsMergeTest.test_permission_merge_preserves_unrelated_current_hooks) ... ok
test_real_template_preserves_herdr_matcher_and_converges (test_claude_settings_merge.ClaudeSettingsMergeTest.test_real_template_preserves_herdr_matcher_and_converges) ... ok
test_real_value_change_is_redumped (test_claude_settings_merge.ClaudeSettingsMergeTest.test_real_value_change_is_redumped) ... ok
test_reordered_but_equal_current_is_byte_identical (test_claude_settings_merge.ClaudeSettingsMergeTest.test_reordered_but_equal_current_is_byte_identical) ... ok
test_runtime_enabled_plugins_survive_a_managed_file_without_the_key (test_claude_settings_merge.ClaudeSettingsMergeTest.test_runtime_enabled_plugins_survive_a_managed_file_without_the_key) ... ok
test_trailing_newline (test_claude_settings_merge.ClaudeSettingsMergeTest.test_trailing_newline) ... ok
test_current_only_runtime_tables_keep_current_group_order (test_codex_config_merge.CodexConfigMergeTest.test_current_only_runtime_tables_keep_current_group_order) ... ok
test_fresh_machine_outputs_managed_baseline (test_codex_config_merge.CodexConfigMergeTest.test_fresh_machine_outputs_managed_baseline) ... ok
test_managed_permgate_replaces_stale_private_ccgate_hook (test_codex_config_merge.CodexConfigMergeTest.test_managed_permgate_replaces_stale_private_ccgate_hook) ... ok
test_managed_templates_are_rendered_before_merge (test_codex_config_merge.CodexConfigMergeTest.test_managed_templates_are_rendered_before_merge) ... ok
test_managed_wins_for_managed_keys (test_codex_config_merge.CodexConfigMergeTest.test_managed_wins_for_managed_keys) ... ok
test_repeated_runtime_tables_are_preserved_in_order (test_codex_config_merge.CodexConfigMergeTest.test_repeated_runtime_tables_are_preserved_in_order) ... ok
test_retired_disabled_mcp_servers_are_purged_and_enabled_ones_kept (test_codex_config_merge.CodexConfigMergeTest.test_retired_disabled_mcp_servers_are_purged_and_enabled_ones_kept) ... ok
test_runtime_tables_are_preserved (test_codex_config_merge.CodexConfigMergeTest.test_runtime_tables_are_preserved) ... ok
test_runtime_tables_seed_from_managed_when_absent (test_codex_config_merge.CodexConfigMergeTest.test_runtime_tables_seed_from_managed_when_absent) ... ok
test_unknown_current_tables_are_preserved (test_codex_config_merge.CodexConfigMergeTest.test_unknown_current_tables_are_preserved) ... ok
test_working_tree_placeholder_falls_back_to_source_dir_parent (test_codex_config_merge.CodexConfigMergeTest.test_working_tree_placeholder_falls_back_to_source_dir_parent) ... ok
test_working_tree_placeholder_prefers_env_override (test_codex_config_merge.CodexConfigMergeTest.test_working_tree_placeholder_prefers_env_override) ... ok
test_rules_are_forbidden_only_and_cover_the_declared_prefixes (test_codex_execpolicy.CodexExecpolicyTest.test_rules_are_forbidden_only_and_cover_the_declared_prefixes) ... ok
test_missing_trusted_runtime_is_silent (test_contextdb_codex_notify.ContextdbCodexNotifyTest.test_missing_trusted_runtime_is_silent) ... ok
test_non_opted_project_is_silent_even_with_trusted_runtime (test_contextdb_codex_notify.ContextdbCodexNotifyTest.test_non_opted_project_is_silent_even_with_trusted_runtime) ... ok
test_project_cli_is_data_only_and_trusted_cli_gets_explicit_root (test_contextdb_codex_notify.ContextdbCodexNotifyTest.test_project_cli_is_data_only_and_trusted_cli_gets_explicit_root) ... ok
test_coverage_gems_are_compatible_and_exact (test_files_fixture.FilesFixtureTest.test_coverage_gems_are_compatible_and_exact) ... ok
test_fixture_uses_chezmoi_binary_outside_mise_shims (test_files_fixture.FilesFixtureTest.test_fixture_uses_chezmoi_binary_outside_mise_shims) ... ok
test_legacy_file_workflows_initialize_required_fixture_paths (test_files_fixture.FilesFixtureTest.test_legacy_file_workflows_initialize_required_fixture_paths) ... ok
test_a_missing_formatter_is_reported_without_a_traceback (test_format_edited_files_hook.FormatEditedFilesHookTest.test_a_missing_formatter_is_reported_without_a_traceback) ... ok
test_formatters_run_from_the_edited_files_repository_root (test_format_edited_files_hook.FormatEditedFilesHookTest.test_formatters_run_from_the_edited_files_repository_root) ... ok
test_a_declare_r_assignment_must_appear_exactly_once (test_generate_agent_configs.GenerateAgentConfigsTest.test_a_declare_r_assignment_must_appear_exactly_once) ... ok
test_a_list_render_writes_one_pin_into_several_files_and_declare_r (test_generate_agent_configs.GenerateAgentConfigsTest.test_a_list_render_writes_one_pin_into_several_files_and_declare_r) ... ok
test_absent_worker_profile_renders_no_env_line (test_generate_agent_configs.GenerateAgentConfigsTest.test_absent_worker_profile_renders_no_env_line) ... ok
test_absent_worker_worktree_renders_no_env_line (test_generate_agent_configs.GenerateAgentConfigsTest.test_absent_worker_worktree_renders_no_env_line) ... ok
test_an_empty_mcp_server_map_renders_no_tables_and_an_empty_claude_map (test_generate_agent_configs.GenerateAgentConfigsTest.test_an_empty_mcp_server_map_renders_no_tables_and_an_empty_claude_map) ... ok
test_asset_constant_must_be_assigned_exactly_once (test_generate_agent_configs.GenerateAgentConfigsTest.test_asset_constant_must_be_assigned_exactly_once) ... ok
test_asset_constants_render_into_their_files (test_generate_agent_configs.GenerateAgentConfigsTest.test_asset_constants_render_into_their_files) ... ok
test_asset_pin_must_be_a_plain_value (test_generate_agent_configs.GenerateAgentConfigsTest.test_asset_pin_must_be_a_plain_value) ... ok
test_audit_profile_renders_read_only_sandbox_override (test_generate_agent_configs.GenerateAgentConfigsTest.test_audit_profile_renders_read_only_sandbox_override) ... ok
test_bootstrap_pins_render_into_setup_and_their_installers (test_generate_agent_configs.GenerateAgentConfigsTest.test_bootstrap_pins_render_into_setup_and_their_installers) ... ok
test_check_reports_asset_render_drift (test_generate_agent_configs.GenerateAgentConfigsTest.test_check_reports_asset_render_drift) ... ok
test_claude_deny_rules_use_edit_for_file_mutations (test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_deny_rules_use_edit_for_file_mutations) ... ok
test_claude_sandbox_renders_optional_socket_and_extra_write_keys (test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_sandbox_renders_optional_socket_and_extra_write_keys) ... ok
test_claude_settings_render_interactive_advisor_only_when_set (test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_settings_render_interactive_advisor_only_when_set) ... ok
test_claude_settings_render_the_format_hook_from_its_path (test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_settings_render_the_format_hook_from_its_path) ... ok
test_claude_settings_renders_session_start_hooks (test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_settings_renders_session_start_hooks) ... ok
test_claude_settings_use_interactive_profile_with_permgate (test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_settings_use_interactive_profile_with_permgate) ... ok
test_claude_skill_symlink_outputs_strip_executable_target_prefix (test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_skill_symlink_outputs_strip_executable_target_prefix) ... ok
test_codex_config_renders_permgate_permission_request (test_generate_agent_configs.GenerateAgentConfigsTest.test_codex_config_renders_permgate_permission_request) ... ok
test_codex_config_renders_working_tree_project_key (test_generate_agent_configs.GenerateAgentConfigsTest.test_codex_config_renders_working_tree_project_key) ... ok
test_entries_reaching_one_file_through_a_symlink_edit_one_snapshot (test_generate_agent_configs.GenerateAgentConfigsTest.test_entries_reaching_one_file_through_a_symlink_edit_one_snapshot) ... ok
test_expected_outputs_uses_codex_baseline_path (test_generate_agent_configs.GenerateAgentConfigsTest.test_expected_outputs_uses_codex_baseline_path) ... ok
test_managed_claude_sandbox_excludes_agmsg_dispatch (test_generate_agent_configs.GenerateAgentConfigsTest.test_managed_claude_sandbox_excludes_agmsg_dispatch) ... ok
test_managed_codex_path_includes_installed_common_bin (test_generate_agent_configs.GenerateAgentConfigsTest.test_managed_codex_path_includes_installed_common_bin) ... ok
test_managed_hooks_use_installed_permgate_paths (test_generate_agent_configs.GenerateAgentConfigsTest.test_managed_hooks_use_installed_permgate_paths) ... ok
test_manifest_keeps_model_ids_only_in_profiles (test_generate_agent_configs.GenerateAgentConfigsTest.test_manifest_keeps_model_ids_only_in_profiles) ... ok
test_model_profiles_env_renders_claude_advisor_only_when_set (test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_renders_claude_advisor_only_when_set) ... ok
test_model_profiles_env_renders_worker_kind (test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_renders_worker_kind) ... ok
test_model_profiles_env_renders_worker_profile (test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_renders_worker_profile) ... ok
test_model_profiles_env_renders_worker_worktree (test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_renders_worker_worktree) ... ok
test_model_profiles_reject_incomplete_or_unsafe_entries (test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_reject_incomplete_or_unsafe_entries) ... ERROR: model profile standard is missing codex
ERROR: model profile standard.claude.model must be a launcher-safe string
ERROR: model_profiles must define the express profile
ok
test_model_profiles_reject_invalid_sandbox_mode (test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_reject_invalid_sandbox_mode) ... ok
test_model_profiles_reject_unsafe_advisor (test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_reject_unsafe_advisor) ... ERROR: model profile standard.claude.advisor must be a launcher-safe string
ok
test_profile_modify_scripts_are_byte_idempotent_with_runtime_state (test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_are_byte_idempotent_with_runtime_state) ... ok
test_profile_modify_scripts_are_quiet_for_matching_hook_trust (test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_are_quiet_for_matching_hook_trust) ... ok
test_profile_modify_scripts_preserve_repeated_runtime_tables (test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_preserve_repeated_runtime_tables) ... ok
test_profile_modify_scripts_preserve_runtime_state (test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_preserve_runtime_state) ... ok
test_profile_modify_scripts_seed_base_hook_trust (test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_seed_base_hook_trust) ... ok
test_profile_modify_scripts_warn_on_hook_trust_divergence (test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_warn_on_hook_trust_divergence) ... ok
test_repository_marketplace_is_a_runtime_owned_seed (test_generate_agent_configs.GenerateAgentConfigsTest.test_repository_marketplace_is_a_runtime_owned_seed) ... ok
test_security_profile_renders_launcher_and_expanded_notify (test_generate_agent_configs.GenerateAgentConfigsTest.test_security_profile_renders_launcher_and_expanded_notify) ... ok
test_set_asset_field_rejects_unknown_targets_and_unsafe_values (test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_field_rejects_unknown_targets_and_unsafe_values) ... ok
test_set_asset_field_rewrites_only_the_named_scalar (test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_field_rewrites_only_the_named_scalar) ... ok
test_set_asset_leaves_files_untouched_when_an_assignment_is_invalid (test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_leaves_files_untouched_when_an_assignment_is_invalid) ... ok
test_set_asset_refuses_fields_other_than_pins_and_checksums (test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_refuses_fields_other_than_pins_and_checksums) ... ok
test_set_asset_rejects_a_value_that_does_not_parse_back_as_a_string (test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_rejects_a_value_that_does_not_parse_back_as_a_string) ... ok
test_set_asset_reports_an_unparsable_manifest_without_a_traceback (test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_reports_an_unparsable_manifest_without_a_traceback) ... ok
test_set_asset_updates_the_manifest_and_renders_its_pins (test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_updates_the_manifest_and_renders_its_pins) ... ok
test_unknown_interactive_profile_fails (test_generate_agent_configs.GenerateAgentConfigsTest.test_unknown_interactive_profile_fails) ... ERROR: interactive_profile must name a model profile: 'missing'
ok
test_unknown_worker_kind_fails (test_generate_agent_configs.GenerateAgentConfigsTest.test_unknown_worker_kind_fails) ... ERROR: worker_kind must be one of ('codex', 'claude'): 'banana'
ok
test_unknown_worker_profile_fails (test_generate_agent_configs.GenerateAgentConfigsTest.test_unknown_worker_profile_fails) ... ERROR: worker_profile must name a model profile: 'missing'
ok
test_worker_gh_dir_is_shell_safe_and_defaults_to_separate_config (test_generate_agent_configs.GenerateAgentConfigsTest.test_worker_gh_dir_is_shell_safe_and_defaults_to_separate_config) ... ERROR: worker_gh_config_dir must be an absolute or ~/ path without control characters
ERROR: worker_gh_config_dir must be an absolute or ~/ path without control characters
ERROR: worker_gh_config_dir must be an absolute or ~/ path without control characters
ERROR: worker_gh_config_dir must be an absolute or ~/ path without control characters
ok
test_worker_kind_defaults_to_codex (test_generate_agent_configs.GenerateAgentConfigsTest.test_worker_kind_defaults_to_codex) ... ok
test_worker_worktree_outside_claude_worktrees_fails (test_generate_agent_configs.GenerateAgentConfigsTest.test_worker_worktree_outside_claude_worktrees_fails) ... ERROR: worker_worktree must be a relative path under .claude/worktrees/: 'worker-c'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '/abs/.claude/worktrees/x'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/..'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/a/b'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/$(x)'
ok
test_a_real_directory_of_that_name_stays_visible (test_gitignore_sandbox_placeholders.SandboxPlaceholderIgnoreTest.test_a_real_directory_of_that_name_stays_visible) ... ok
test_claude_settings_stay_visible (test_gitignore_sandbox_placeholders.SandboxPlaceholderIgnoreTest.test_claude_settings_stay_visible) ... ok
test_empty_placeholder_files_on_disk_leave_status_clean (test_gitignore_sandbox_placeholders.SandboxPlaceholderIgnoreTest.test_empty_placeholder_files_on_disk_leave_status_clean) ... ok
test_every_placeholder_is_ignored_at_the_root_only (test_gitignore_sandbox_placeholders.SandboxPlaceholderIgnoreTest.test_every_placeholder_is_ignored_at_the_root_only) ... ok
test_add_worker_accepts_a_claude_trust_dialog_while_spawn_waits (test_herdr_agents.HerdrAgentsTest.test_add_worker_accepts_a_claude_trust_dialog_while_spawn_waits) ... ok
test_add_worker_derives_the_default_herdr_socket_for_spawn (test_herdr_agents.HerdrAgentsTest.test_add_worker_derives_the_default_herdr_socket_for_spawn) ... ok
test_add_worker_emits_no_override_for_an_unparseable_codex_config (test_herdr_agents.HerdrAgentsTest.test_add_worker_emits_no_override_for_an_unparseable_codex_config) ... ok
test_add_worker_exits_zero_when_a_timed_out_spawn_still_links (test_herdr_agents.HerdrAgentsTest.test_add_worker_exits_zero_when_a_timed_out_spawn_still_links) ... ok
test_add_worker_keeps_the_configured_roots_from_an_indented_multi_line_array (test_herdr_agents.HerdrAgentsTest.test_add_worker_keeps_the_configured_roots_from_an_indented_multi_line_array) ... ok
test_add_worker_linkage_failure_prints_the_invocation_and_the_query (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_failure_prints_the_invocation_and_the_query) ... ok
test_add_worker_linkage_falls_back_to_the_legacy_record_without_the_resolver (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_falls_back_to_the_legacy_record_without_the_resolver) ... ok
test_add_worker_linkage_ignores_a_delayed_pong_for_another_ping (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_ignores_a_delayed_pong_for_another_ping) ... ok
test_add_worker_linkage_ignores_a_placement_record_for_a_pane_gone_from_the_workspace (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_ignores_a_placement_record_for_a_pane_gone_from_the_workspace) ... ok
test_add_worker_linkage_ignores_a_placement_record_for_a_pane_that_predates_this_spawn (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_ignores_a_placement_record_for_a_pane_that_predates_this_spawn) ... ok
test_add_worker_linkage_ignores_a_placement_record_from_another_workspace (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_ignores_a_placement_record_from_another_workspace) ... ok
test_add_worker_linkage_ignores_a_pong_older_than_this_ping (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_ignores_a_pong_older_than_this_ping) ... ok
test_add_worker_linkage_reads_a_leading_zero_wait_as_decimal (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_reads_a_leading_zero_wait_as_decimal) ... ok
test_add_worker_linkage_refuses_a_placement_conflict (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_refuses_a_placement_conflict) ... ok
test_add_worker_linkage_refuses_several_orchestrator_identities (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_refuses_several_orchestrator_identities) ... ok
test_add_worker_linkage_resolves_an_id_keyed_placement_record (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_resolves_an_id_keyed_placement_record) ... ok
test_add_worker_linkage_survives_a_non_numeric_pong_wait (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_survives_a_non_numeric_pong_wait) ... ok
test_add_worker_linkage_uses_the_spawn_placement_record_not_team_sh (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_uses_the_spawn_placement_record_not_team_sh) ... ok
test_add_worker_passes_codex_profile_and_sandbox_through_spawn_options (test_herdr_agents.HerdrAgentsTest.test_add_worker_passes_codex_profile_and_sandbox_through_spawn_options) ... ok
test_add_worker_refuses_an_undefined_profile_before_any_change (test_herdr_agents.HerdrAgentsTest.test_add_worker_refuses_an_undefined_profile_before_any_change) ... ok
test_add_worker_refuses_before_any_change_when_no_herdr_socket_is_found (test_herdr_agents.HerdrAgentsTest.test_add_worker_refuses_before_any_change_when_no_herdr_socket_is_found) ... ok
test_add_worker_rejects_a_worktree_outside_claude_worktrees (test_herdr_agents.HerdrAgentsTest.test_add_worker_rejects_a_worktree_outside_claude_worktrees) ... ok
test_add_worker_reports_a_failed_claude_spawn_without_a_trust_dialog (test_herdr_agents.HerdrAgentsTest.test_add_worker_reports_a_failed_claude_spawn_without_a_trust_dialog) ... ok
test_add_worker_reports_a_failed_spawn (test_herdr_agents.HerdrAgentsTest.test_add_worker_reports_a_failed_spawn) ... ok
test_add_worker_reports_linkage_ok_after_a_ready_spawn (test_herdr_agents.HerdrAgentsTest.test_add_worker_reports_linkage_ok_after_a_ready_spawn) ... ok
test_add_worker_reports_linkage_unreached_after_a_failed_spawn (test_herdr_agents.HerdrAgentsTest.test_add_worker_reports_linkage_unreached_after_a_failed_spawn) ... ok
test_add_worker_reports_shallow_metadata_as_not_granted (test_herdr_agents.HerdrAgentsTest.test_add_worker_reports_shallow_metadata_as_not_granted) ... ok
test_add_worker_reuses_a_seat_tab_in_the_pair_workspace (test_herdr_agents.HerdrAgentsTest.test_add_worker_reuses_a_seat_tab_in_the_pair_workspace) ... ok
test_add_worker_reuses_a_seated_workspace (test_herdr_agents.HerdrAgentsTest.test_add_worker_reuses_a_seated_workspace) ... ok
test_add_worker_seats_the_worker_in_a_tab_of_the_pair_workspace (test_herdr_agents.HerdrAgentsTest.test_add_worker_seats_the_worker_in_a_tab_of_the_pair_workspace) ... ok
test_add_worker_spawns_the_seat_in_its_own_workspace_with_profile_args (test_herdr_agents.HerdrAgentsTest.test_add_worker_spawns_the_seat_in_its_own_workspace_with_profile_args) ... ok
test_add_worker_succeeds_for_a_claude_worker_without_a_trust_dialog (test_herdr_agents.HerdrAgentsTest.test_add_worker_succeeds_for_a_claude_worker_without_a_trust_dialog) ... ok
test_added_worker_github_environment_reaches_boot (test_herdr_agents.HerdrAgentsTest.test_added_worker_github_environment_reaches_boot) ... ok
test_agent_name_taken_gives_up_after_bounded_wait (test_herdr_agents.HerdrAgentsTest.test_agent_name_taken_gives_up_after_bounded_wait) ... ok
test_another_team_members_pane_is_not_a_second_worker (test_herdr_agents.HerdrAgentsTest.test_another_team_members_pane_is_not_a_second_worker) ... ok
test_attach_bootstraps_agmsg_after_codex_reuse (test_herdr_agents.HerdrAgentsTest.test_attach_bootstraps_agmsg_after_codex_reuse) ... ok
test_attach_bootstraps_agmsg_after_codex_start (test_herdr_agents.HerdrAgentsTest.test_attach_bootstraps_agmsg_after_codex_start) ... ok
test_attach_builds_codex_right_of_current_claude_pane (test_herdr_agents.HerdrAgentsTest.test_attach_builds_codex_right_of_current_claude_pane) ... ok
test_attach_complete_workspace_is_idempotent (test_herdr_agents.HerdrAgentsTest.test_attach_complete_workspace_is_idempotent) ... ok
test_attach_completes_bootstrap_on_a_self_named_pair (test_herdr_agents.HerdrAgentsTest.test_attach_completes_bootstrap_on_a_self_named_pair) ... ok
test_attach_correct_order_does_not_swap (test_herdr_agents.HerdrAgentsTest.test_attach_correct_order_does_not_swap) ... ok
test_attach_does_not_restart_codex_agent_from_another_tab (test_herdr_agents.HerdrAgentsTest.test_attach_does_not_restart_codex_agent_from_another_tab) ... ok
test_attach_equal_halves_does_not_resize (test_herdr_agents.HerdrAgentsTest.test_attach_equal_halves_does_not_resize) ... ok
test_attach_from_the_self_named_worker_pane_exits_quietly (test_herdr_agents.HerdrAgentsTest.test_attach_from_the_self_named_worker_pane_exits_quietly) ... ok
test_attach_from_the_worker_pane_does_not_relabel_it (test_herdr_agents.HerdrAgentsTest.test_attach_from_the_worker_pane_does_not_relabel_it) ... ok
test_attach_from_the_worker_worktree_exits_quietly (test_herdr_agents.HerdrAgentsTest.test_attach_from_the_worker_worktree_exits_quietly) ... ok
test_attach_ignores_agmsg_bootstrap_failure (test_herdr_agents.HerdrAgentsTest.test_attach_ignores_agmsg_bootstrap_failure) ... ok
test_attach_ignores_extra_panes_on_other_tabs (test_herdr_agents.HerdrAgentsTest.test_attach_ignores_extra_panes_on_other_tabs) ... ok
test_attach_leaves_a_self_named_pair_alone (test_herdr_agents.HerdrAgentsTest.test_attach_leaves_a_self_named_pair_alone) ... ok
test_attach_legacy_files_pane_refuses_repair_without_layout_mutation (test_herdr_agents.HerdrAgentsTest.test_attach_legacy_files_pane_refuses_repair_without_layout_mutation) ... ok
test_attach_lowercases_and_validates_derived_agent_name (test_herdr_agents.HerdrAgentsTest.test_attach_lowercases_and_validates_derived_agent_name) ... ok
test_attach_noops_for_full_mode_managed_layout (test_herdr_agents.HerdrAgentsTest.test_attach_noops_for_full_mode_managed_layout) ... ok
test_attach_ratio_repair_skips_unsafe_layouts (test_herdr_agents.HerdrAgentsTest.test_attach_ratio_repair_skips_unsafe_layouts) ... ok
test_attach_rejects_invalid_derived_agent_name (test_herdr_agents.HerdrAgentsTest.test_attach_rejects_invalid_derived_agent_name) ... ok
test_attach_repair_splits_the_missing_worker_pane_in_its_worktree (test_herdr_agents.HerdrAgentsTest.test_attach_repair_splits_the_missing_worker_pane_in_its_worktree) ... ok
test_attach_repairs_codex_claude_order_with_one_swap (test_herdr_agents.HerdrAgentsTest.test_attach_repairs_codex_claude_order_with_one_swap) ... ok
test_attach_repairs_skewed_widths_to_equal_halves (test_herdr_agents.HerdrAgentsTest.test_attach_repairs_skewed_widths_to_equal_halves) ... ok
test_attach_reports_agmsg_skip_when_not_installed (test_herdr_agents.HerdrAgentsTest.test_attach_reports_agmsg_skip_when_not_installed) ... ok
test_attach_skips_delivery_when_turn_hook_exists (test_herdr_agents.HerdrAgentsTest.test_attach_skips_delivery_when_turn_hook_exists) ... ok
test_attach_warns_after_one_nonconverging_resize (test_herdr_agents.HerdrAgentsTest.test_attach_warns_after_one_nonconverging_resize) ... ok
test_attach_warns_when_multiple_agmsg_identities_exist (test_herdr_agents.HerdrAgentsTest.test_attach_warns_when_multiple_agmsg_identities_exist) ... ok
test_attach_without_herdr_environment_names_the_seated_worker (test_herdr_agents.HerdrAgentsTest.test_attach_without_herdr_environment_names_the_seated_worker) ... ok
test_attach_without_herdr_environment_prints_the_bring_up_summary (test_herdr_agents.HerdrAgentsTest.test_attach_without_herdr_environment_prints_the_bring_up_summary) ... ok
test_attach_without_herdr_environment_stays_quiet_in_the_worker_worktree (test_herdr_agents.HerdrAgentsTest.test_attach_without_herdr_environment_stays_quiet_in_the_worker_worktree) ... ok
test_audit_accepts_a_dir_with_an_apostrophe_quoted_intact (test_herdr_agents.HerdrAgentsTest.test_audit_accepts_a_dir_with_an_apostrophe_quoted_intact) ... ok
test_audit_creates_the_audit_tab_once_and_reuses_it (test_herdr_agents.HerdrAgentsTest.test_audit_creates_the_audit_tab_once_and_reuses_it) ... ok
test_audit_exits_2_without_a_managed_workspace (test_herdr_agents.HerdrAgentsTest.test_audit_exits_2_without_a_managed_workspace) ... ok
test_audit_fails_as_unmasked_when_masking_fails (test_herdr_agents.HerdrAgentsTest.test_audit_fails_as_unmasked_when_masking_fails) ... ok
test_audit_falls_back_to_the_recent_unwrapped_prompt_without_process_info (test_herdr_agents.HerdrAgentsTest.test_audit_falls_back_to_the_recent_unwrapped_prompt_without_process_info) ... ok
test_audit_finds_the_self_named_pair_workspace (test_herdr_agents.HerdrAgentsTest.test_audit_finds_the_self_named_pair_workspace) ... ok
test_audit_gates_on_the_concluding_line_of_the_last_message (test_herdr_agents.HerdrAgentsTest.test_audit_gates_on_the_concluding_line_of_the_last_message) ... ok
test_audit_marker_detection_reads_unwrapped_snapshots (test_herdr_agents.HerdrAgentsTest.test_audit_marker_detection_reads_unwrapped_snapshots) ... ok
test_audit_masks_evidence_before_the_verdict_gate (test_herdr_agents.HerdrAgentsTest.test_audit_masks_evidence_before_the_verdict_gate) ... ok
test_audit_masks_evidence_even_when_the_audit_exit_is_nonzero (test_herdr_agents.HerdrAgentsTest.test_audit_masks_evidence_even_when_the_audit_exit_is_nonzero) ... ok
test_audit_nonzero_exit_marker_fails_the_helper (test_herdr_agents.HerdrAgentsTest.test_audit_nonzero_exit_marker_fails_the_helper) ... ok
test_audit_pane_command_tees_evidence_and_waits_for_a_fresh_marker (test_herdr_agents.HerdrAgentsTest.test_audit_pane_command_tees_evidence_and_waits_for_a_fresh_marker) ... ok
test_audit_quotes_a_non_ascii_out_path_under_the_c_locale (test_herdr_agents.HerdrAgentsTest.test_audit_quotes_a_non_ascii_out_path_under_the_c_locale) ... ok
test_audit_quotes_the_last_message_path_for_a_non_ascii_out (test_herdr_agents.HerdrAgentsTest.test_audit_quotes_the_last_message_path_for_a_non_ascii_out) ... ok
test_audit_refuses_a_busy_audit_pane (test_herdr_agents.HerdrAgentsTest.test_audit_refuses_a_busy_audit_pane) ... ok
test_audit_refuses_a_tracked_masker_missing_from_the_tree (test_herdr_agents.HerdrAgentsTest.test_audit_refuses_a_tracked_masker_missing_from_the_tree) ... ok
test_audit_refuses_an_uncommitted_or_untracked_masker (test_herdr_agents.HerdrAgentsTest.test_audit_refuses_an_uncommitted_or_untracked_masker) ... ok
test_audit_refuses_the_masker_from_the_audited_commit (test_herdr_agents.HerdrAgentsTest.test_audit_refuses_the_masker_from_the_audited_commit) ... ok
test_audit_rejects_unsafe_arguments_before_calling_herdr (test_herdr_agents.HerdrAgentsTest.test_audit_rejects_unsafe_arguments_before_calling_herdr) ... ok
test_audit_runs_codex_exec_with_the_prompt_and_last_message_file (test_herdr_agents.HerdrAgentsTest.test_audit_runs_codex_exec_with_the_prompt_and_last_message_file) ... ok
test_audit_runs_in_dir_even_when_the_reused_pane_moved (test_herdr_agents.HerdrAgentsTest.test_audit_runs_in_dir_even_when_the_reused_pane_moved) ... ok
test_audit_skips_masking_without_a_repo_validator (test_herdr_agents.HerdrAgentsTest.test_audit_skips_masking_without_a_repo_validator) ... ok
test_audit_tab_does_not_break_attach_order_and_ratio_repair (test_herdr_agents.HerdrAgentsTest.test_audit_tab_does_not_break_attach_order_and_ratio_repair) ... ok
test_audit_tab_keeps_the_full_mode_duplicate_workspace_guard (test_herdr_agents.HerdrAgentsTest.test_audit_tab_keeps_the_full_mode_duplicate_workspace_guard) ... ok
test_audit_task_inlines_the_task_inputs_and_the_merge_base_diff (test_herdr_agents.HerdrAgentsTest.test_audit_task_inlines_the_task_inputs_and_the_merge_base_diff) ... ok
test_audit_task_names_a_txt_artifact_when_no_md_one_exists (test_herdr_agents.HerdrAgentsTest.test_audit_task_names_a_txt_artifact_when_no_md_one_exists) ... ok
test_audit_task_names_only_the_task_file_when_no_artifact_exists (test_herdr_agents.HerdrAgentsTest.test_audit_task_names_only_the_task_file_when_no_artifact_exists) ... ok
test_audit_task_refuses_a_missing_task_file_or_merge_base_before_herdr_work (test_herdr_agents.HerdrAgentsTest.test_audit_task_refuses_a_missing_task_file_or_merge_base_before_herdr_work) ... ok
test_audit_trusts_a_shell_foreground_over_a_stale_visible_snapshot (test_herdr_agents.HerdrAgentsTest.test_audit_trusts_a_shell_foreground_over_a_stale_visible_snapshot) ... ok
test_audit_uses_manifest_audit_codex_args (test_herdr_agents.HerdrAgentsTest.test_audit_uses_manifest_audit_codex_args) ... ok
test_audit_verdict_gate_reads_only_the_final_codex_block (test_herdr_agents.HerdrAgentsTest.test_audit_verdict_gate_reads_only_the_final_codex_block) ... ok
test_audit_waits_for_the_prompt_on_a_new_audit_tab (test_herdr_agents.HerdrAgentsTest.test_audit_waits_for_the_prompt_on_a_new_audit_tab) ... ok
test_bootstrap_accepts_same_identity_in_multiple_teams (test_herdr_agents.HerdrAgentsTest.test_bootstrap_accepts_same_identity_in_multiple_teams) ... ok
test_bootstrap_leaves_a_foreign_pre_push_hook_alone (test_herdr_agents.HerdrAgentsTest.test_bootstrap_leaves_a_foreign_pre_push_hook_alone) ... ok
test_bootstrap_only_creates_missing_herdr_log_directory (test_herdr_agents.HerdrAgentsTest.test_bootstrap_only_creates_missing_herdr_log_directory) ... ok
test_bootstrap_only_does_not_call_herdr_or_agents (test_herdr_agents.HerdrAgentsTest.test_bootstrap_only_does_not_call_herdr_or_agents) ... ok
test_bootstrap_only_sets_claude_delivery_once_when_hook_is_missing (test_herdr_agents.HerdrAgentsTest.test_bootstrap_only_sets_claude_delivery_once_when_hook_is_missing) ... ok
test_bootstrap_only_sets_each_missing_delivery_once (test_herdr_agents.HerdrAgentsTest.test_bootstrap_only_sets_each_missing_delivery_once) ... ok
test_bootstrap_only_skips_all_delivery_when_both_hooks_exist (test_herdr_agents.HerdrAgentsTest.test_bootstrap_only_skips_all_delivery_when_both_hooks_exist) ... ok
test_bootstrap_only_skips_home_without_agmsg_calls (test_herdr_agents.HerdrAgentsTest.test_bootstrap_only_skips_home_without_agmsg_calls) ... ok
test_bootstrap_only_warns_for_missing_claude_identity_without_joining (test_herdr_agents.HerdrAgentsTest.test_bootstrap_only_warns_for_missing_claude_identity_without_joining) ... ok
test_bootstrap_only_warns_for_multiple_claude_identities (test_herdr_agents.HerdrAgentsTest.test_bootstrap_only_warns_for_multiple_claude_identities) ... ok
test_bootstrap_removes_its_retired_pre_push_stub (test_herdr_agents.HerdrAgentsTest.test_bootstrap_removes_its_retired_pre_push_stub) ... ok
test_bootstrap_with_claude_worker_accepts_two_claude_identities (test_herdr_agents.HerdrAgentsTest.test_bootstrap_with_claude_worker_accepts_two_claude_identities) ... ok
test_bootstrap_with_claude_worker_hints_at_a_missing_worker_identity (test_herdr_agents.HerdrAgentsTest.test_bootstrap_with_claude_worker_hints_at_a_missing_worker_identity) ... ok
test_bootstrap_with_claude_worker_leaves_codex_hooks_alone (test_herdr_agents.HerdrAgentsTest.test_bootstrap_with_claude_worker_leaves_codex_hooks_alone) ... ok
test_claude_agent_accepts_manifest_profile_arguments_for_e2e (test_herdr_agents.HerdrAgentsTest.test_claude_agent_accepts_manifest_profile_arguments_for_e2e) ... ok
test_claude_repair_skips_just_restarted_codex_pane_without_agent_field (test_herdr_agents.HerdrAgentsTest.test_claude_repair_skips_just_restarted_codex_pane_without_agent_field) ... ok
test_claude_settings_add_herdr_attach_session_hook (test_herdr_agents.HerdrAgentsTest.test_claude_settings_add_herdr_attach_session_hook) ... ok
test_claude_worker_sharing_the_orchestrator_identity_is_refused (test_herdr_agents.HerdrAgentsTest.test_claude_worker_sharing_the_orchestrator_identity_is_refused) ... ok
test_claude_worker_with_a_registered_worker_identity_proceeds (test_herdr_agents.HerdrAgentsTest.test_claude_worker_with_a_registered_worker_identity_proceeds) ... ok
test_codex_profile_defaults_to_generated_interactive_profile (test_herdr_agents.HerdrAgentsTest.test_codex_profile_defaults_to_generated_interactive_profile) ... ok
test_codex_worker_is_not_subject_to_the_identity_guard (test_herdr_agents.HerdrAgentsTest.test_codex_worker_is_not_subject_to_the_identity_guard) ... ok
test_existing_legacy_files_pane_is_not_reused_for_claude_or_split_again (test_herdr_agents.HerdrAgentsTest.test_existing_legacy_files_pane_is_not_reused_for_claude_or_split_again) ... ok
test_existing_two_pane_workspace_repairs_skewed_widths (test_herdr_agents.HerdrAgentsTest.test_existing_two_pane_workspace_repairs_skewed_widths) ... ok
test_existing_workspace_matches_canonical_macos_workdir (test_herdr_agents.HerdrAgentsTest.test_existing_workspace_matches_canonical_macos_workdir) ... ok
test_existing_workspace_restarts_missing_claude_in_empty_pane (test_herdr_agents.HerdrAgentsTest.test_existing_workspace_restarts_missing_claude_in_empty_pane) ... ok
test_existing_workspace_restarts_missing_codex_agent (test_herdr_agents.HerdrAgentsTest.test_existing_workspace_restarts_missing_codex_agent) ... ok
test_existing_workspace_splits_when_missing_claude_has_no_empty_pane (test_herdr_agents.HerdrAgentsTest.test_existing_workspace_splits_when_missing_claude_has_no_empty_pane) ... ok
test_existing_workspace_with_legacy_files_pane_focuses_without_mutation (test_herdr_agents.HerdrAgentsTest.test_existing_workspace_with_legacy_files_pane_focuses_without_mutation) ... ok
test_explicit_worker_kind_and_profile_survive_seat_label_loading (test_herdr_agents.HerdrAgentsTest.test_explicit_worker_kind_and_profile_survive_seat_label_loading) ... ok
test_file_viewer_plugin_config_sets_micro_editor (test_herdr_agents.HerdrAgentsTest.test_file_viewer_plugin_config_sets_micro_editor) ... ok
test_full_and_restart_modes_refuse_duplicate_managed_workspaces (test_herdr_agents.HerdrAgentsTest.test_full_and_restart_modes_refuse_duplicate_managed_workspaces) ... ok
test_full_mode_does_not_duplicate_a_solo_codex_worker_seat (test_herdr_agents.HerdrAgentsTest.test_full_mode_does_not_duplicate_a_solo_codex_worker_seat) ... ok
test_full_mode_gives_a_codex_worker_its_worktree_git_metadata_roots (test_herdr_agents.HerdrAgentsTest.test_full_mode_gives_a_codex_worker_its_worktree_git_metadata_roots) ... ok
test_full_mode_heal_moves_a_reused_empty_pane_into_the_worktree (test_herdr_agents.HerdrAgentsTest.test_full_mode_heal_moves_a_reused_empty_pane_into_the_worktree) ... ok
test_full_mode_heal_never_starts_the_worker_in_an_exited_added_worker_pane (test_herdr_agents.HerdrAgentsTest.test_full_mode_heal_never_starts_the_worker_in_an_exited_added_worker_pane) ... ok
test_full_mode_heal_never_starts_the_worker_in_the_audit_pane (test_herdr_agents.HerdrAgentsTest.test_full_mode_heal_never_starts_the_worker_in_the_audit_pane) ... ok
test_full_mode_heals_nothing_in_a_healthy_self_named_pair (test_herdr_agents.HerdrAgentsTest.test_full_mode_heals_nothing_in_a_healthy_self_named_pair) ... ok
test_full_mode_heals_the_orchestrator_beside_a_live_added_claude_worker (test_herdr_agents.HerdrAgentsTest.test_full_mode_heals_the_orchestrator_beside_a_live_added_claude_worker) ... ok
test_full_mode_reuses_agentless_worker_pane_in_attach_labeled_workspace (test_herdr_agents.HerdrAgentsTest.test_full_mode_reuses_agentless_worker_pane_in_attach_labeled_workspace) ... ok
test_full_mode_skips_agmsg_bootstrap_for_home (test_herdr_agents.HerdrAgentsTest.test_full_mode_skips_agmsg_bootstrap_for_home) ... ok
test_full_mode_splits_the_worker_pane_in_its_worktree (test_herdr_agents.HerdrAgentsTest.test_full_mode_splits_the_worker_pane_in_its_worktree) ... ok
test_ghostty_config_does_not_auto_start_herdr_session (test_herdr_agents.HerdrAgentsTest.test_ghostty_config_does_not_auto_start_herdr_session) ... ok
test_herdr_prefix_alt_a_runs_helper_from_active_pane (test_herdr_agents.HerdrAgentsTest.test_herdr_prefix_alt_a_runs_helper_from_active_pane) ... ok
test_herdr_prefix_f_opens_file_viewer_popup (test_herdr_agents.HerdrAgentsTest.test_herdr_prefix_f_opens_file_viewer_popup) ... ok
test_make_update_and_upgrade_include_agmsg_bootstrap (test_herdr_agents.HerdrAgentsTest.test_make_update_and_upgrade_include_agmsg_bootstrap) ... ok
test_mixed_legacy_and_seat_labels_are_one_pair (test_herdr_agents.HerdrAgentsTest.test_mixed_legacy_and_seat_labels_are_one_pair) ... ok
test_new_pane_waits_for_shell_and_retries_agent_start_once_on_timeout (test_herdr_agents.HerdrAgentsTest.test_new_pane_waits_for_shell_and_retries_agent_start_once_on_timeout) ... ok
test_orchestrator_pane_appends_claude_args_after_profile_args (test_herdr_agents.HerdrAgentsTest.test_orchestrator_pane_appends_claude_args_after_profile_args) ... ok
test_orchestrator_pane_start_claims_the_seat_with_the_composite_id (test_herdr_agents.HerdrAgentsTest.test_orchestrator_pane_start_claims_the_seat_with_the_composite_id) ... ok
test_orchestrator_pane_start_without_a_session_claims_nothing (test_herdr_agents.HerdrAgentsTest.test_orchestrator_pane_start_without_a_session_claims_nothing) ... ok
test_orchestrator_pane_uses_interactive_profile_args (test_herdr_agents.HerdrAgentsTest.test_orchestrator_pane_uses_interactive_profile_args) ... ok
test_pane_creation_propagates_explicit_fpath (test_herdr_agents.HerdrAgentsTest.test_pane_creation_propagates_explicit_fpath) ... ok
test_regime_boundary_check_counts_names_across_runtime_types_at_an_active_seat (test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_counts_names_across_runtime_types_at_an_active_seat) ... ok
test_regime_boundary_check_finds_worker_workspaces_from_a_worktree (test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_finds_worker_workspaces_from_a_worktree) ... ok
test_regime_boundary_check_flags_empty_seats_only (test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_flags_empty_seats_only) ... ok
test_regime_boundary_check_gives_the_seat_lock_check_the_main_checkout (test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_gives_the_seat_lock_check_the_main_checkout) ... ok
test_regime_boundary_check_reports_an_added_worker_tab_in_the_pair_workspace (test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_reports_an_added_worker_tab_in_the_pair_workspace) ... ok
test_regime_boundary_check_scans_every_worktree_for_untracked_evidence (test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_scans_every_worktree_for_untracked_evidence) ... ok
test_registered_agent_not_ready_waits_for_idle_without_duplicate_start (test_herdr_agents.HerdrAgentsTest.test_registered_agent_not_ready_waits_for_idle_without_duplicate_start) ... ok
test_remove_worker_cleans_up_a_codex_seat_without_a_placement_record (test_herdr_agents.HerdrAgentsTest.test_remove_worker_cleans_up_a_codex_seat_without_a_placement_record) ... ok
test_remove_worker_closes_only_its_tab_in_the_pair_workspace (test_herdr_agents.HerdrAgentsTest.test_remove_worker_closes_only_its_tab_in_the_pair_workspace) ... ok
test_remove_worker_despawns_then_turns_delivery_off_leaves_and_closes (test_herdr_agents.HerdrAgentsTest.test_remove_worker_despawns_then_turns_delivery_off_leaves_and_closes) ... ok
test_remove_worker_force_retries_a_failed_graceful_despawn (test_herdr_agents.HerdrAgentsTest.test_remove_worker_force_retries_a_failed_graceful_despawn) ... ok
test_remove_worker_force_skips_the_forced_despawn_when_graceful_succeeds (test_herdr_agents.HerdrAgentsTest.test_remove_worker_force_skips_the_forced_despawn_when_graceful_succeeds) ... ok
test_remove_worker_forces_despawn_when_graceful_reports_needs_force (test_herdr_agents.HerdrAgentsTest.test_remove_worker_forces_despawn_when_graceful_reports_needs_force) ... ok
test_remove_worker_keeps_a_worker_tab_that_holds_another_running_agent (test_herdr_agents.HerdrAgentsTest.test_remove_worker_keeps_a_worker_tab_that_holds_another_running_agent) ... ok
test_remove_worker_refuses_a_dirty_worktree_without_force (test_herdr_agents.HerdrAgentsTest.test_remove_worker_refuses_a_dirty_worktree_without_force) ... ok
test_remove_worker_stops_when_a_graceful_despawn_fails (test_herdr_agents.HerdrAgentsTest.test_remove_worker_stops_when_a_graceful_despawn_fails) ... ok
test_remove_worker_stops_when_the_forced_retry_also_fails (test_herdr_agents.HerdrAgentsTest.test_remove_worker_stops_when_the_forced_retry_also_fails) ... ok
test_restart_worker_confirms_the_exit_dialog_once (test_herdr_agents.HerdrAgentsTest.test_restart_worker_confirms_the_exit_dialog_once) ... ok
test_restart_worker_exits_2_without_a_managed_workspace (test_herdr_agents.HerdrAgentsTest.test_restart_worker_exits_2_without_a_managed_workspace) ... ok
test_restart_worker_finds_a_solo_codex_worker_seat (test_herdr_agents.HerdrAgentsTest.test_restart_worker_finds_a_solo_codex_worker_seat) ... ok
test_restart_worker_finds_the_worker_by_its_seat_label (test_herdr_agents.HerdrAgentsTest.test_restart_worker_finds_the_worker_by_its_seat_label) ... ok
test_restart_worker_never_treats_the_audit_pane_as_the_worker (test_herdr_agents.HerdrAgentsTest.test_restart_worker_never_treats_the_audit_pane_as_the_worker) ... ok
test_restart_worker_passes_manifest_advisor_args_to_claude_worker (test_herdr_agents.HerdrAgentsTest.test_restart_worker_passes_manifest_advisor_args_to_claude_worker) ... ok
test_restart_worker_refuses_to_start_outside_the_seat_when_the_pane_hangs (test_herdr_agents.HerdrAgentsTest.test_restart_worker_refuses_to_start_outside_the_seat_when_the_pane_hangs) ... ok
test_restart_worker_refuses_unmanaged_extra_panes (test_herdr_agents.HerdrAgentsTest.test_restart_worker_refuses_unmanaged_extra_panes) ... ok
test_restart_worker_refuses_when_the_pane_never_reaches_a_shell (test_herdr_agents.HerdrAgentsTest.test_restart_worker_refuses_when_the_pane_never_reaches_a_shell) ... ok
test_restart_worker_relaunches_the_worker_in_its_existing_pane (test_herdr_agents.HerdrAgentsTest.test_restart_worker_relaunches_the_worker_in_its_existing_pane) ... ok
test_restart_worker_repairs_a_legacy_orchestrator_label_on_the_worker_pane (test_herdr_agents.HerdrAgentsTest.test_restart_worker_repairs_a_legacy_orchestrator_label_on_the_worker_pane) ... ok
test_restart_worker_reseats_a_main_path_worker_into_its_worktree (test_herdr_agents.HerdrAgentsTest.test_restart_worker_reseats_a_main_path_worker_into_its_worktree) ... ok
test_restart_worker_waits_for_stale_registration_then_retries_once (test_herdr_agents.HerdrAgentsTest.test_restart_worker_waits_for_stale_registration_then_retries_once) ... ok
test_seat_claim_fails_when_a_later_team_is_held_by_another_session (test_herdr_agents.HerdrAgentsTest.test_seat_claim_fails_when_a_later_team_is_held_by_another_session) ... ok
test_seat_claim_held_by_another_session_fails_without_release (test_herdr_agents.HerdrAgentsTest.test_seat_claim_held_by_another_session_fails_without_release) ... ok
test_seat_claim_keeps_a_same_session_composite_lock_of_a_live_claude (test_herdr_agents.HerdrAgentsTest.test_seat_claim_keeps_a_same_session_composite_lock_of_a_live_claude) ... ok
test_seat_claim_replaces_a_same_session_bare_lock (test_herdr_agents.HerdrAgentsTest.test_seat_claim_replaces_a_same_session_bare_lock) ... ok
test_seat_claim_replaces_a_same_session_composite_lock_of_a_dead_pid (test_herdr_agents.HerdrAgentsTest.test_seat_claim_replaces_a_same_session_composite_lock_of_a_dead_pid) ... ok
test_seat_claim_replaces_a_same_session_composite_lock_of_a_recycled_pid (test_herdr_agents.HerdrAgentsTest.test_seat_claim_replaces_a_same_session_composite_lock_of_a_recycled_pid) ... ok
test_seat_claim_replaces_same_session_bare_locks_in_every_team (test_herdr_agents.HerdrAgentsTest.test_seat_claim_replaces_same_session_bare_locks_in_every_team) ... ok
test_session_start_attach_bounds_a_trickling_hook_payload (test_herdr_agents.HerdrAgentsTest.test_session_start_attach_bounds_a_trickling_hook_payload) ... ok
test_session_start_attach_claims_the_seat_in_a_managed_pane (test_herdr_agents.HerdrAgentsTest.test_session_start_attach_claims_the_seat_in_a_managed_pane) ... ok
test_session_start_attach_claims_when_the_hook_keeps_stdin_open (test_herdr_agents.HerdrAgentsTest.test_session_start_attach_claims_when_the_hook_keeps_stdin_open) ... ok
test_session_start_attach_prints_no_directive_for_a_pane_that_is_not_the_orchestrator (test_herdr_agents.HerdrAgentsTest.test_session_start_attach_prints_no_directive_for_a_pane_that_is_not_the_orchestrator) ... ok
test_session_start_attach_prints_the_regime_directive_with_a_worker_seat (test_herdr_agents.HerdrAgentsTest.test_session_start_attach_prints_the_regime_directive_with_a_worker_seat) ... ok
test_session_start_attach_reads_the_hook_payload_and_herdr_pid (test_herdr_agents.HerdrAgentsTest.test_session_start_attach_reads_the_hook_payload_and_herdr_pid) ... ok
test_session_start_attach_skips_a_pane_that_is_not_the_orchestrator (test_herdr_agents.HerdrAgentsTest.test_session_start_attach_skips_a_pane_that_is_not_the_orchestrator) ... ok
test_start_keeps_node_global_without_mise_tool_install (test_herdr_agents.HerdrAgentsTest.test_start_keeps_node_global_without_mise_tool_install) ... ok
test_start_removes_node_global_agent_clis_shadowing_mise (test_herdr_agents.HerdrAgentsTest.test_start_removes_node_global_agent_clis_shadowing_mise) ... ok
test_start_skips_node_global_removal_without_stray (test_herdr_agents.HerdrAgentsTest.test_start_skips_node_global_removal_without_stray) ... ok
test_successful_agent_start_does_not_poll_agent_list (test_herdr_agents.HerdrAgentsTest.test_successful_agent_start_does_not_poll_agent_list) ... ok
test_two_self_named_pair_workspaces_still_refuse (test_herdr_agents.HerdrAgentsTest.test_two_self_named_pair_workspaces_still_refuse) ... ok
test_uses_initial_workspace_pane_for_claude_and_splits_codex_right (test_herdr_agents.HerdrAgentsTest.test_uses_initial_workspace_pane_for_claude_and_splits_codex_right) ... ok
test_worker_github_pair_env (test_herdr_agents.HerdrAgentsTest.test_worker_github_pair_env) ... ok
test_worker_kind_claude_accepts_a_workspace_trust_dialog (test_herdr_agents.HerdrAgentsTest.test_worker_kind_claude_accepts_a_workspace_trust_dialog) ... ok
test_worker_kind_claude_appends_extra_worker_args (test_herdr_agents.HerdrAgentsTest.test_worker_kind_claude_appends_extra_worker_args) ... ok
test_worker_kind_claude_does_not_require_codex (test_herdr_agents.HerdrAgentsTest.test_worker_kind_claude_does_not_require_codex) ... ok
test_worker_kind_claude_skips_send_keys_without_a_trust_dialog (test_herdr_agents.HerdrAgentsTest.test_worker_kind_claude_skips_send_keys_without_a_trust_dialog) ... ok
test_worker_kind_claude_starts_a_claude_worker_pane_with_profile_args (test_herdr_agents.HerdrAgentsTest.test_worker_kind_claude_starts_a_claude_worker_pane_with_profile_args) ... ok
test_worker_kind_claude_starts_with_no_resolved_args (test_herdr_agents.HerdrAgentsTest.test_worker_kind_claude_starts_with_no_resolved_args) ... ok
test_worker_kind_defaults_to_generated_env_fragment (test_herdr_agents.HerdrAgentsTest.test_worker_kind_defaults_to_generated_env_fragment) ... ok
test_worker_kind_env_override_wins_over_generated_env_fragment (test_herdr_agents.HerdrAgentsTest.test_worker_kind_env_override_wins_over_generated_env_fragment) ... ok
test_worker_kind_rejects_an_unknown_value (test_herdr_agents.HerdrAgentsTest.test_worker_kind_rejects_an_unknown_value) ... ok
test_worker_profile_defaults_to_generated_worker_profile (test_herdr_agents.HerdrAgentsTest.test_worker_profile_defaults_to_generated_worker_profile) ... ok
test_worker_profile_env_override_wins_over_generated_worker_profile (test_herdr_agents.HerdrAgentsTest.test_worker_profile_env_override_wins_over_generated_worker_profile) ... ok
test_worker_seat_ambiguity_leaves_no_worktree_behind (test_herdr_agents.HerdrAgentsTest.test_worker_seat_ambiguity_leaves_no_worktree_behind) ... ok
test_worker_seat_is_skipped_in_a_non_git_directory (test_herdr_agents.HerdrAgentsTest.test_worker_seat_is_skipped_in_a_non_git_directory) ... ok
test_worker_seat_is_skipped_in_an_unregistered_repository (test_herdr_agents.HerdrAgentsTest.test_worker_seat_is_skipped_in_an_unregistered_repository) ... ok
test_worker_seat_is_skipped_outside_a_git_main_checkout (test_herdr_agents.HerdrAgentsTest.test_worker_seat_is_skipped_outside_a_git_main_checkout) ... ok
test_worker_seat_label_comes_from_the_worker_worktree_registration (test_herdr_agents.HerdrAgentsTest.test_worker_seat_label_comes_from_the_worker_worktree_registration) ... ok
test_worker_seat_refuses_a_path_that_is_not_a_worktree (test_herdr_agents.HerdrAgentsTest.test_worker_seat_refuses_a_path_that_is_not_a_worktree) ... ok
test_worker_seat_refuses_an_ambiguous_orchestrator_identity (test_herdr_agents.HerdrAgentsTest.test_worker_seat_refuses_an_ambiguous_orchestrator_identity) ... ok
test_worker_seat_reuses_the_identity_and_hook_already_at_the_worktree (test_herdr_agents.HerdrAgentsTest.test_worker_seat_reuses_the_identity_and_hook_already_at_the_worktree) ... ok
test_yazi_edit_opener_prefers_zed_with_editor_fallback (test_herdr_agents.HerdrAgentsTest.test_yazi_edit_opener_prefers_zed_with_editor_fallback) ... ok
test_zprofile_adds_common_bin_to_login_shell_path (test_herdr_agents.HerdrAgentsTest.test_zprofile_adds_common_bin_to_login_shell_path) ... ok
test_allow_pattern_rejects_shell_chaining (test_permgate.PermgateTest.test_allow_pattern_rejects_shell_chaining) ... ok
test_apply_patch_is_never_deterministically_allowed (test_permgate.PermgateTest.test_apply_patch_is_never_deterministically_allowed) ... ok
test_bash_credentials_fall_through_without_logging_them (test_permgate.PermgateTest.test_bash_credentials_fall_through_without_logging_them) ... ok
test_claude_and_codex_hook_outputs_match_golden_bytes (test_permgate.PermgateTest.test_claude_and_codex_hook_outputs_match_golden_bytes) ... ok
test_git_diff_output_option_is_never_automatically_allowed (test_permgate.PermgateTest.test_git_diff_output_option_is_never_automatically_allowed) ... ok
test_invalid_policy_fields_fail_closed (test_permgate.PermgateTest.test_invalid_policy_fields_fail_closed) ... ok
test_invalid_policy_returns_ask_and_logs_config_error (test_permgate.PermgateTest.test_invalid_policy_returns_ask_and_logs_config_error) ... ok
test_layer_one_allows_documented_claude_and_codex_contracts (test_permgate.PermgateTest.test_layer_one_allows_documented_claude_and_codex_contracts) ... ok
test_layer_one_deny_uses_both_hook_output_schemas (test_permgate.PermgateTest.test_layer_one_deny_uses_both_hook_output_schemas) ... ok
test_log_shape_redacts_command_and_output (test_permgate.PermgateTest.test_log_shape_redacts_command_and_output) ... ok
test_mutating_or_executable_read_options_fall_through (test_permgate.PermgateTest.test_mutating_or_executable_read_options_fall_through) ... ok
test_recursion_sentinel_is_a_complete_no_op (test_permgate.PermgateTest.test_recursion_sentinel_is_a_complete_no_op) ... ok
test_repository_policy_allows_and_falls_through (test_permgate.PermgateTest.test_repository_policy_allows_and_falls_through) ... ok
test_script_named_version_is_not_a_version_check (test_permgate.PermgateTest.test_script_named_version_is_not_a_version_check) ... ok
test_structured_secret_is_redacted_from_the_summary (test_permgate.PermgateTest.test_structured_secret_is_redacted_from_the_summary) ... ok
test_unconstrained_native_reads_fall_through (test_permgate.PermgateTest.test_unconstrained_native_reads_fall_through) ... ok
test_undecided_request_falls_through_to_the_native_prompt (test_permgate.PermgateTest.test_undecided_request_falls_through_to_the_native_prompt) ... ok
test_annotations_keep_every_level_even_on_passing_checks (test_pr_feedback.PrFeedbackTest.test_annotations_keep_every_level_even_on_passing_checks) ... ok
test_bots_are_detected_from_type_login_or_app (test_pr_feedback.PrFeedbackTest.test_bots_are_detected_from_type_login_or_app) ... ok
test_collects_every_feedback_source_for_the_head (test_pr_feedback.PrFeedbackTest.test_collects_every_feedback_source_for_the_head) ... ok
test_collects_the_github_base_with_the_head (test_pr_feedback.PrFeedbackTest.test_collects_the_github_base_with_the_head) ... ok
test_commit_status_keeps_the_latest_state_per_context (test_pr_feedback.PrFeedbackTest.test_commit_status_keeps_the_latest_state_per_context) ... ok
test_every_item_carries_the_disposition_schema (test_pr_feedback.PrFeedbackTest.test_every_item_carries_the_disposition_schema) ... ok
test_gh_never_receives_forced_colour (test_pr_feedback.PrFeedbackTest.test_gh_never_receives_forced_colour) ... ok
test_graphql_strings_are_raw_and_only_integers_are_typed (test_pr_feedback.PrFeedbackTest.test_graphql_strings_are_raw_and_only_integers_are_typed) ... ok
test_main_writes_the_document_to_json (test_pr_feedback.PrFeedbackTest.test_main_writes_the_document_to_json) ... ok
test_only_non_passing_check_runs_become_items (test_pr_feedback.PrFeedbackTest.test_only_non_passing_check_runs_become_items) ... ok
test_review_comments_carry_thread_resolution_across_pages (test_pr_feedback.PrFeedbackTest.test_review_comments_carry_thread_resolution_across_pages) ... ok
test_thread_state_covers_comments_beyond_the_first_page (test_pr_feedback.PrFeedbackTest.test_thread_state_covers_comments_beyond_the_first_page) ... ok
test_unauthenticated_gh_exits_non_zero (test_pr_feedback.PrFeedbackTest.test_unauthenticated_gh_exits_non_zero) ... ok
test_rule_mirrors_and_skills_carry_the_same_requirements (test_pr_feedback.PrIntegrationRuleParityTest.test_rule_mirrors_and_skills_carry_the_same_requirements) ... ok
test_rule_symlink_points_at_the_rule (test_pr_feedback.PrIntegrationRuleParityTest.test_rule_symlink_points_at_the_rule) ... ok
test_bump_writes_only_the_five_pins_through_set_asset (test_release_asset_pins.ReleaseAssetPinsTest.test_bump_writes_only_the_five_pins_through_set_asset) ... ok
test_window_never_moves_a_pin_backwards (test_release_asset_pins.ReleaseAssetPinsTest.test_window_never_moves_a_pin_backwards) ... ok
test_window_rejects_an_unknown_current_pin (test_release_asset_pins.ReleaseAssetPinsTest.test_window_rejects_an_unknown_current_pin) ... ok
test_window_skips_a_young_release_and_takes_an_older_one (test_release_asset_pins.ReleaseAssetPinsTest.test_window_skips_a_young_release_and_takes_an_older_one) ... ok
test_all_paths_are_preflighted_before_any_deletion (test_remove_agent_asset.RemoveAgentAssetTest.test_all_paths_are_preflighted_before_any_deletion) ... ok
test_brew_refuses_ambiguous_formula (test_remove_agent_asset.RemoveAgentAssetTest.test_brew_refuses_ambiguous_formula) ... ok
test_brew_uses_uninstall_for_unambiguous_formula (test_remove_agent_asset.RemoveAgentAssetTest.test_brew_uses_uninstall_for_unambiguous_formula) ... ok
test_crit_plugin_falls_back_to_data_path_but_not_config (test_remove_agent_asset.RemoveAgentAssetTest.test_crit_plugin_falls_back_to_data_path_but_not_config) ... ok
test_default_and_explicit_dry_run_print_without_mutating (test_remove_agent_asset.RemoveAgentAssetTest.test_default_and_explicit_dry_run_print_without_mutating) ... ok
test_integration_uses_verified_herdr_uninstall (test_remove_agent_asset.RemoveAgentAssetTest.test_integration_uses_verified_herdr_uninstall) ... ok
test_invalid_manifest_is_rejected (test_remove_agent_asset.RemoveAgentAssetTest.test_invalid_manifest_is_rejected) ... ok
test_parameterized_step_removal_preserves_sibling_identity (test_remove_agent_asset.RemoveAgentAssetTest.test_parameterized_step_removal_preserves_sibling_identity) ... ok
test_plugin_uses_verified_claude_uninstall (test_remove_agent_asset.RemoveAgentAssetTest.test_plugin_uses_verified_claude_uninstall) ... ok
test_plugin_uses_verified_codex_remove (test_remove_agent_asset.RemoveAgentAssetTest.test_plugin_uses_verified_codex_remove) ... ok
test_recorded_symlink_is_removed_without_following_target (test_remove_agent_asset.RemoveAgentAssetTest.test_recorded_symlink_is_removed_without_following_target) ... ok
test_tampered_manifest_outside_safe_roots_is_refused (test_remove_agent_asset.RemoveAgentAssetTest.test_tampered_manifest_outside_safe_roots_is_refused) ... ok
test_unknown_step_lists_known_steps_without_guessing (test_remove_agent_asset.RemoveAgentAssetTest.test_unknown_step_lists_known_steps_without_guessing) ... ok
test_yes_removes_only_recorded_path_and_preserves_other_steps (test_remove_agent_asset.RemoveAgentAssetTest.test_yes_removes_only_recorded_path_and_preserves_other_steps) ... ok
test_advanced_base_cannot_delete_collector_to_trigger_head_fallback (test_require_crit_review.ReviewGuardTest.test_advanced_base_cannot_delete_collector_to_trigger_head_fallback) ... ok
test_advanced_base_cannot_supply_an_untrusted_collector (test_require_crit_review.ReviewGuardTest.test_advanced_base_cannot_supply_an_untrusted_collector) ... ok
test_agent_lifecycle_script_change_requires_review (test_require_crit_review.ReviewGuardTest.test_agent_lifecycle_script_change_requires_review) ... ok
test_agent_lifecycle_surfaces_require_review (test_require_crit_review.ReviewGuardTest.test_agent_lifecycle_surfaces_require_review) ... ok
test_agent_lifecycle_tokens_require_review (test_require_crit_review.ReviewGuardTest.test_agent_lifecycle_tokens_require_review) ... ok
test_agent_reviewer_rejects_empty_or_malformed_crit_data (test_require_crit_review.ReviewGuardTest.test_agent_reviewer_rejects_empty_or_malformed_crit_data) ... ok
test_agent_reviewer_rejects_invalid_review_outcome (test_require_crit_review.ReviewGuardTest.test_agent_reviewer_rejects_invalid_review_outcome) ... ok
test_agent_reviewer_with_command_string_source_still_requires_review (test_require_crit_review.ReviewGuardTest.test_agent_reviewer_with_command_string_source_still_requires_review) ... ok
test_agent_reviewer_with_crit_data_satisfies_required_review (test_require_crit_review.ReviewGuardTest.test_agent_reviewer_with_crit_data_satisfies_required_review) ... ok
test_agent_reviewer_with_crit_reviewed_marker_still_requires_review (test_require_crit_review.ReviewGuardTest.test_agent_reviewer_with_crit_reviewed_marker_still_requires_review) ... ok
test_agent_reviewer_with_external_crit_json_still_requires_review (test_require_crit_review.ReviewGuardTest.test_agent_reviewer_with_external_crit_json_still_requires_review) ... ok
test_agent_reviewer_with_non_review_crit_json_object_still_requires_review (test_require_crit_review.ReviewGuardTest.test_agent_reviewer_with_non_review_crit_json_object_still_requires_review) ... ok
test_agent_reviewer_with_resolved_line_comment_satisfies_required_review (test_require_crit_review.ReviewGuardTest.test_agent_reviewer_with_resolved_line_comment_satisfies_required_review) ... ok
test_agent_reviewer_with_unresolved_crit_json_still_requires_review (test_require_crit_review.ReviewGuardTest.test_agent_reviewer_with_unresolved_crit_json_still_requires_review) ... ok
test_agent_self_review_flag_evidence_still_requires_review (test_require_crit_review.ReviewGuardTest.test_agent_self_review_flag_evidence_still_requires_review) ... ok
test_agent_self_reviewer_evidence_still_requires_review (test_require_crit_review.ReviewGuardTest.test_agent_self_reviewer_evidence_still_requires_review) ... ok
test_audit_must_name_head_and_live_under_validation (test_require_crit_review.ReviewGuardTest.test_audit_must_name_head_and_live_under_validation) ... ok
test_base_accepts_a_correct_audit_of_head (test_require_crit_review.ReviewGuardTest.test_base_accepts_a_correct_audit_of_head) ... ok
test_base_accepts_exact_and_advanced_base_with_unchanged_merge_base (test_require_crit_review.ReviewGuardTest.test_base_accepts_exact_and_advanced_base_with_unchanged_merge_base) ... ok
test_base_fails_closed_when_github_metadata_is_unavailable (test_require_crit_review.ReviewGuardTest.test_base_fails_closed_when_github_metadata_is_unavailable) ... ok
test_base_fails_closed_when_unresolvable_or_option_like (test_require_crit_review.ReviewGuardTest.test_base_fails_closed_when_unresolvable_or_option_like) ... ok
test_base_rejects_forged_evidence_metadata (test_require_crit_review.ReviewGuardTest.test_base_rejects_forged_evidence_metadata) ... ok
test_base_rejects_pr_commits_before_executing_their_collector (test_require_crit_review.ReviewGuardTest.test_base_rejects_pr_commits_before_executing_their_collector) ... ok
test_base_rejects_side_branch_and_advanced_base_containing_pr_commits (test_require_crit_review.ReviewGuardTest.test_base_rejects_side_branch_and_advanced_base_containing_pr_commits) ... ok
test_base_requires_audit_evidence_for_a_reviewed_change (test_require_crit_review.ReviewGuardTest.test_base_requires_audit_evidence_for_a_reviewed_change) ... ok
test_base_requires_pr_feedback_evidence (test_require_crit_review.ReviewGuardTest.test_base_requires_pr_feedback_evidence) ... ok
test_base_reviews_committed_branch_changes (test_require_crit_review.ReviewGuardTest.test_base_reviews_committed_branch_changes) ... ok
test_blocked_or_missing_audit_verdict_fails (test_require_crit_review.ReviewGuardTest.test_blocked_or_missing_audit_verdict_fails) ... ok
test_broad_diff_requires_review (test_require_crit_review.ReviewGuardTest.test_broad_diff_requires_review) ... ok
test_broad_orchestration_only_pr_needs_no_audit (test_require_crit_review.ReviewGuardTest.test_broad_orchestration_only_pr_needs_no_audit) ... ok
test_companion_must_be_this_audits_own_last_message (test_require_crit_review.ReviewGuardTest.test_companion_must_be_this_audits_own_last_message) ... ok
test_explicit_disable_skips_guard (test_require_crit_review.ReviewGuardTest.test_explicit_disable_skips_guard) ... ok
test_feedback_accepts_absolute_path_through_a_repository_parent_alias (test_require_crit_review.ReviewGuardTest.test_feedback_accepts_absolute_path_through_a_repository_parent_alias) ... ok
test_feedback_cannot_hide_an_arbitrary_path_without_base (test_require_crit_review.ReviewGuardTest.test_feedback_cannot_hide_an_arbitrary_path_without_base) ... ok
test_feedback_does_not_exclude_symlink_aliases_outside_validation (test_require_crit_review.ReviewGuardTest.test_feedback_does_not_exclude_symlink_aliases_outside_validation) ... ok
test_feedback_path_itself_must_be_under_validation (test_require_crit_review.ReviewGuardTest.test_feedback_path_itself_must_be_under_validation) ... ok
test_feedback_symlink_cannot_hide_a_file_outside_validation (test_require_crit_review.ReviewGuardTest.test_feedback_symlink_cannot_hide_a_file_outside_validation) ... ok
test_fixed_commit_is_checked_against_github_base_not_an_older_side_parent (test_require_crit_review.ReviewGuardTest.test_fixed_commit_is_checked_against_github_base_not_an_older_side_parent) ... ok
test_github_identity_gate_activation_and_current_head_approval (test_require_crit_review.ReviewGuardTest.test_github_identity_gate_activation_and_current_head_approval) ... ok
test_github_lookup_ignores_environment_repository_override (test_require_crit_review.ReviewGuardTest.test_github_lookup_ignores_environment_repository_override) ... ok
test_github_lookup_rejects_evidence_from_another_repository (test_require_crit_review.ReviewGuardTest.test_github_lookup_rejects_evidence_from_another_repository) ... ok
test_high_risk_markdown_change_requires_review (test_require_crit_review.ReviewGuardTest.test_high_risk_markdown_change_requires_review) ... ok
test_incorrect_audit_needs_not_applicable_dispositions (test_require_crit_review.ReviewGuardTest.test_incorrect_audit_needs_not_applicable_dispositions) ... ok
test_incorrect_audit_without_findings_fails (test_require_crit_review.ReviewGuardTest.test_incorrect_audit_without_findings_fails) ... ok
test_large_untracked_file_requires_broad_diff_review (test_require_crit_review.ReviewGuardTest.test_large_untracked_file_requires_broad_diff_review) ... ok
test_missing_base_collector_falls_back_only_after_binding (test_require_crit_review.ReviewGuardTest.test_missing_base_collector_falls_back_only_after_binding) ... ok
test_native_reviewed_environment_rejects_human_reviewer (test_require_crit_review.ReviewGuardTest.test_native_reviewed_environment_rejects_human_reviewer) ... ok
test_native_reviewed_without_evidence_still_requires_review (test_require_crit_review.ReviewGuardTest.test_native_reviewed_without_evidence_still_requires_review) ... ok
test_no_diff_does_not_require_review (test_require_crit_review.ReviewGuardTest.test_no_diff_does_not_require_review) ... ok
test_older_base_must_not_be_on_the_head_first_parent_chain (test_require_crit_review.ReviewGuardTest.test_older_base_must_not_be_on_the_head_first_parent_chain) ... ok
test_orchestration_only_pr_needs_no_audit (test_require_crit_review.ReviewGuardTest.test_orchestration_only_pr_needs_no_audit) ... ok
test_pr_feedback_accepts_complete_evidence_without_a_bot_review (test_require_crit_review.ReviewGuardTest.test_pr_feedback_accepts_complete_evidence_without_a_bot_review) ... ok
test_pr_feedback_accepts_complete_root_cause_dispositions (test_require_crit_review.ReviewGuardTest.test_pr_feedback_accepts_complete_root_cause_dispositions) ... ok
test_pr_feedback_bodies_are_compared_after_secret_masking (test_require_crit_review.ReviewGuardTest.test_pr_feedback_bodies_are_compared_after_secret_masking) ... ok
test_pr_feedback_evidence_file_is_not_counted_as_a_change (test_require_crit_review.ReviewGuardTest.test_pr_feedback_evidence_file_is_not_counted_as_a_change) ... ok
test_pr_feedback_fails_when_the_collector_cannot_run (test_require_crit_review.ReviewGuardTest.test_pr_feedback_fails_when_the_collector_cannot_run) ... ok
test_pr_feedback_fixed_commit_must_be_in_the_pr_range (test_require_crit_review.ReviewGuardTest.test_pr_feedback_fixed_commit_must_be_in_the_pr_range) ... ok
test_pr_feedback_matches_a_masked_path_but_not_an_edited_one (test_require_crit_review.ReviewGuardTest.test_pr_feedback_matches_a_masked_path_but_not_an_edited_one) ... ok
test_pr_feedback_must_be_collected_for_the_current_head (test_require_crit_review.ReviewGuardTest.test_pr_feedback_must_be_collected_for_the_current_head) ... ok
test_pr_feedback_must_cover_every_currently_collected_item (test_require_crit_review.ReviewGuardTest.test_pr_feedback_must_cover_every_currently_collected_item) ... ok
test_pr_feedback_rejects_evidence_outside_the_repository (test_require_crit_review.ReviewGuardTest.test_pr_feedback_rejects_evidence_outside_the_repository) ... ok
test_pr_feedback_rejects_incomplete_or_invalid_dispositions (test_require_crit_review.ReviewGuardTest.test_pr_feedback_rejects_incomplete_or_invalid_dispositions) ... ok
test_pr_feedback_requires_the_github_head_to_match (test_require_crit_review.ReviewGuardTest.test_pr_feedback_requires_the_github_head_to_match) ... ok
test_pr_feedback_uses_the_base_collector_not_the_prs_own (test_require_crit_review.ReviewGuardTest.test_pr_feedback_uses_the_base_collector_not_the_prs_own) ... ok
test_pr_feedback_without_base_is_only_format_checked (test_require_crit_review.ReviewGuardTest.test_pr_feedback_without_base_is_only_format_checked) ... ok
test_recollection_must_match_the_authenticated_repository (test_require_crit_review.ReviewGuardTest.test_recollection_must_match_the_authenticated_repository) ... ok
test_reviewed_environment_satisfies_required_review (test_require_crit_review.ReviewGuardTest.test_reviewed_environment_satisfies_required_review) ... ok
test_reviewed_with_blank_evidence_values_still_requires_review (test_require_crit_review.ReviewGuardTest.test_reviewed_with_blank_evidence_values_still_requires_review) ... ok
test_reviewed_with_incomplete_evidence_still_requires_review (test_require_crit_review.ReviewGuardTest.test_reviewed_with_incomplete_evidence_still_requires_review) ... ok
test_small_docs_only_change_does_not_require_review (test_require_crit_review.ReviewGuardTest.test_small_docs_only_change_does_not_require_review) ... ok
test_verdict_comes_only_from_the_last_message_file (test_require_crit_review.ReviewGuardTest.test_verdict_comes_only_from_the_last_message_file) ... ok
test_agent_asset_update_removes_node_global_shadows_before_agent_commands (test_runtime_health.RuntimeHealthTest.test_agent_asset_update_removes_node_global_shadows_before_agent_commands) ... ok
test_agent_asset_update_repairs_broken_claude_with_npm_backend (test_runtime_health.RuntimeHealthTest.test_agent_asset_update_repairs_broken_claude_with_npm_backend) ... ok
test_agent_asset_update_runs_gh_extension_ensure (test_runtime_health.RuntimeHealthTest.test_agent_asset_update_runs_gh_extension_ensure) ... ok
test_agent_launchers_do_not_hardcode_model_ids (test_runtime_health.RuntimeHealthTest.test_agent_launchers_do_not_hardcode_model_ids) ... ok
test_agmsg_accepts_a_store_the_installer_creates_and_notes_run_changes (test_runtime_health.RuntimeHealthTest.test_agmsg_accepts_a_store_the_installer_creates_and_notes_run_changes) ... ok
test_agmsg_already_pinned_skips_download (test_runtime_health.RuntimeHealthTest.test_agmsg_already_pinned_skips_download) ... ok
test_agmsg_checksum_mismatch_fails_closed (test_runtime_health.RuntimeHealthTest.test_agmsg_checksum_mismatch_fails_closed) ... ok
test_agmsg_fresh_install_populates_skill_and_records_manifest (test_runtime_health.RuntimeHealthTest.test_agmsg_fresh_install_populates_skill_and_records_manifest) ... ok
test_agmsg_migrates_marker_less_legacy_dir_without_losing_live_state (test_runtime_health.RuntimeHealthTest.test_agmsg_migrates_marker_less_legacy_dir_without_losing_live_state) ... ok
test_agmsg_migration_reports_an_installer_that_mutates_live_state (test_runtime_health.RuntimeHealthTest.test_agmsg_migration_reports_an_installer_that_mutates_live_state) ... ok
test_agmsg_refuses_to_install_when_the_state_snapshot_is_empty (test_runtime_health.RuntimeHealthTest.test_agmsg_refuses_to_install_when_the_state_snapshot_is_empty) ... ok
test_agmsg_refuses_to_install_without_tar (test_runtime_health.RuntimeHealthTest.test_agmsg_refuses_to_install_without_tar) ... ok
test_agmsg_reports_an_installer_that_leaves_the_wrong_version (test_runtime_health.RuntimeHealthTest.test_agmsg_reports_an_installer_that_leaves_the_wrong_version) ... ok
test_agmsg_update_aborts_when_install_corrupts_live_state (test_runtime_health.RuntimeHealthTest.test_agmsg_update_aborts_when_install_corrupts_live_state) ... ok
test_agmsg_update_never_touches_teams_db_run (test_runtime_health.RuntimeHealthTest.test_agmsg_update_never_touches_teams_db_run) ... ok
test_client_bashrc_treats_private_sources_as_optional (test_runtime_health.RuntimeHealthTest.test_client_bashrc_treats_private_sources_as_optional) ... ok
test_codex_crit_normalizes_managed_marketplace_mode (test_runtime_health.RuntimeHealthTest.test_codex_crit_normalizes_managed_marketplace_mode) ... ok
test_codex_superpowers_reports_login_step_when_curated_catalog_is_missing (test_runtime_health.RuntimeHealthTest.test_codex_superpowers_reports_login_step_when_curated_catalog_is_missing) ... ok
test_darwin_crit_checksum_failure_preserves_existing_binary (test_runtime_health.RuntimeHealthTest.test_darwin_crit_checksum_failure_preserves_existing_binary) ... ok
test_darwin_crit_install_is_pinned_atomic_and_recorded (test_runtime_health.RuntimeHealthTest.test_darwin_crit_install_is_pinned_atomic_and_recorded) ... ok
test_doctor_github_role_activation_and_file_storage (test_runtime_health.RuntimeHealthTest.test_doctor_github_role_activation_and_file_storage) ... ok
test_doctor_reports_claude_sandbox_prerequisites (test_runtime_health.RuntimeHealthTest.test_doctor_reports_claude_sandbox_prerequisites) ... ok
test_doctor_required_optional_and_healthy_statuses (test_runtime_health.RuntimeHealthTest.test_doctor_required_optional_and_healthy_statuses) ... ok
test_linux_crit_checksum_failure_preserves_existing_binary (test_runtime_health.RuntimeHealthTest.test_linux_crit_checksum_failure_preserves_existing_binary) ... ok
test_linux_crit_correct_version_is_download_free (test_runtime_health.RuntimeHealthTest.test_linux_crit_correct_version_is_download_free) ... ok
test_linux_crit_failure_does_not_leak_cleanup_trap (test_runtime_health.RuntimeHealthTest.test_linux_crit_failure_does_not_leak_cleanup_trap) ... ok
test_linux_crit_install_is_pinned_atomic_and_recorded (test_runtime_health.RuntimeHealthTest.test_linux_crit_install_is_pinned_atomic_and_recorded) ... ok
test_linux_crit_prefers_pinned_target_over_older_path_binary (test_runtime_health.RuntimeHealthTest.test_linux_crit_prefers_pinned_target_over_older_path_binary) ... ok
test_make_doctor_does_not_skip_runtime_check_when_deployed_root_is_missing (test_runtime_health.RuntimeHealthTest.test_make_doctor_does_not_skip_runtime_check_when_deployed_root_is_missing) ... ok
test_make_doctor_passes_repair_variable_to_runtime_check (test_runtime_health.RuntimeHealthTest.test_make_doctor_passes_repair_variable_to_runtime_check) ... ok
test_make_doctor_propagates_runtime_drift_after_tool_checks (test_runtime_health.RuntimeHealthTest.test_make_doctor_propagates_runtime_drift_after_tool_checks) ... ok
test_make_update_pulls_clean_main_before_apply (test_runtime_health.RuntimeHealthTest.test_make_update_pulls_clean_main_before_apply) ... ok
test_make_update_reports_unmerged_feature_branch_before_branch_notice (test_runtime_health.RuntimeHealthTest.test_make_update_reports_unmerged_feature_branch_before_branch_notice) ... ok
test_make_update_reports_unmerged_index_before_dirty_notice (test_runtime_health.RuntimeHealthTest.test_make_update_reports_unmerged_index_before_dirty_notice) ... ok
test_make_update_skips_dirty_main_with_manual_pull_notice (test_runtime_health.RuntimeHealthTest.test_make_update_skips_dirty_main_with_manual_pull_notice) ... ok
test_upgrade_applies_mise_only_from_successful_canonical_checkout (test_runtime_health.RuntimeHealthTest.test_upgrade_applies_mise_only_from_successful_canonical_checkout) ... ok
test_upgrade_bumps_terminal_and_crit_pins_from_fetched_artifacts (test_runtime_health.RuntimeHealthTest.test_upgrade_bumps_terminal_and_crit_pins_from_fetched_artifacts) ... ok
test_upgrade_changes_checkout_not_live_mise_symlink_target (test_runtime_health.RuntimeHealthTest.test_upgrade_changes_checkout_not_live_mise_symlink_target) ... ok
test_upgrade_github_extensions_are_warning_only (test_runtime_health.RuntimeHealthTest.test_upgrade_github_extensions_are_warning_only) ... ok
test_upgrade_required_failures_are_nonzero_and_independent (test_runtime_health.RuntimeHealthTest.test_upgrade_required_failures_are_nonzero_and_independent) ... ok
test_upgrade_self_updates_mise_to_the_manifest_pin (test_runtime_health.RuntimeHealthTest.test_upgrade_self_updates_mise_to_the_manifest_pin) ... ok
test_upgrade_skips_unavailable_mise_self_update (test_runtime_health.RuntimeHealthTest.test_upgrade_skips_unavailable_mise_self_update) ... ok
test_upgrade_uses_current_mise_node_after_runtime_replacement (test_runtime_health.RuntimeHealthTest.test_upgrade_uses_current_mise_node_after_runtime_replacement)
Reject ambient npm after mise replaces the active Node runtime. ... ok
test_ci_smokes_exact_tools_with_network_denied (test_statusline_tools.StatuslineToolsTest.test_ci_smokes_exact_tools_with_network_denied) ... ok
test_direct_commands_use_offline_path_binaries (test_statusline_tools.StatuslineToolsTest.test_direct_commands_use_offline_path_binaries) ... ok
test_generated_commands_are_direct_and_static (test_statusline_tools.StatuslineToolsTest.test_generated_commands_are_direct_and_static) ... ok
test_mise_config_and_lock_pin_exact_npm_versions (test_statusline_tools.StatuslineToolsTest.test_mise_config_and_lock_pin_exact_npm_versions) ... ok
test_missing_binary_fails_immediately (test_statusline_tools.StatuslineToolsTest.test_missing_binary_fails_immediately) ... ok
test_binary_installers_replace_from_same_directory_stages (test_supply_chain_policy.SupplyChainPolicyTest.test_binary_installers_replace_from_same_directory_stages) ... ok
test_executable_downloads_are_verified_and_not_piped_to_shell (test_supply_chain_policy.SupplyChainPolicyTest.test_executable_downloads_are_verified_and_not_piped_to_shell) ... ok
test_external_checksum_failure_preserves_destination (test_supply_chain_policy.SupplyChainPolicyTest.test_external_checksum_failure_preserves_destination) ... ok
test_externals_render_without_network_discovery (test_supply_chain_policy.SupplyChainPolicyTest.test_externals_render_without_network_discovery) ... ok
test_externals_use_fixed_urls_and_checksums (test_supply_chain_policy.SupplyChainPolicyTest.test_externals_use_fixed_urls_and_checksums) ... ok
test_installer_cleanup_preserves_failure_status (test_supply_chain_policy.SupplyChainPolicyTest.test_installer_cleanup_preserves_failure_status) ... ok
test_installer_cleanup_survives_mock_function_returns (test_supply_chain_policy.SupplyChainPolicyTest.test_installer_cleanup_survives_mock_function_returns) ... ok
test_mise_apply_replaces_live_symlinks_with_independent_copies (test_supply_chain_policy.SupplyChainPolicyTest.test_mise_apply_replaces_live_symlinks_with_independent_copies) ... ok
test_mise_lock_matches_config_and_supported_platforms (test_supply_chain_policy.SupplyChainPolicyTest.test_mise_lock_matches_config_and_supported_platforms) ... ok
test_mise_lock_url_entries_have_checksums (test_supply_chain_policy.SupplyChainPolicyTest.test_mise_lock_url_entries_have_checksums) ... ok
test_mise_main_preserves_install_failure (test_supply_chain_policy.SupplyChainPolicyTest.test_mise_main_preserves_install_failure) ... ok
test_mise_npm_backend_uses_npm_and_limits_lifecycle_scripts (test_supply_chain_policy.SupplyChainPolicyTest.test_mise_npm_backend_uses_npm_and_limits_lifecycle_scripts) ... ok
test_mise_versions_are_exact_and_locking_is_enforced (test_supply_chain_policy.SupplyChainPolicyTest.test_mise_versions_are_exact_and_locking_is_enforced) ... ok
test_renovate_owns_dependency_update_notifications (test_supply_chain_policy.SupplyChainPolicyTest.test_renovate_owns_dependency_update_notifications) ... ok
test_setup_ci_rejects_and_preserves_local_drift (test_supply_chain_policy.SupplyChainPolicyTest.test_setup_ci_rejects_and_preserves_local_drift) ... ok
test_sheldon_git_sources_have_revisions (test_supply_chain_policy.SupplyChainPolicyTest.test_sheldon_git_sources_have_revisions) ... ok
test_sheldon_uses_locked_crates_io_source (test_supply_chain_policy.SupplyChainPolicyTest.test_sheldon_uses_locked_crates_io_source) ... ok
test_absent_path_without_old_ref_is_regression (test_ua_symbol_coverage.UaSymbolCoverageTest.test_absent_path_without_old_ref_is_regression) ... ok
test_chmod_only_change_keeps_the_source_unchanged_note (test_ua_symbol_coverage.UaSymbolCoverageTest.test_chmod_only_change_keeps_the_source_unchanged_note) ... ok
test_comment_lines_are_not_definitions (test_ua_symbol_coverage.UaSymbolCoverageTest.test_comment_lines_are_not_definitions) ... ok
test_def_column_reads_the_new_graph_revision (test_ua_symbol_coverage.UaSymbolCoverageTest.test_def_column_reads_the_new_graph_revision) ... ok
test_deleted_path_with_old_ref_is_explained (test_ua_symbol_coverage.UaSymbolCoverageTest.test_deleted_path_with_old_ref_is_explained) ... ok
test_flags_unexplained_symbol_loss_only (test_ua_symbol_coverage.UaSymbolCoverageTest.test_flags_unexplained_symbol_loss_only) ... ok
test_grammar_file_missing_from_graph_fails_in_covered_directories (test_ua_symbol_coverage.UaSymbolCoverageTest.test_grammar_file_missing_from_graph_fails_in_covered_directories) ... ok
test_low_similarity_move_with_no_symbols_is_regression (test_ua_symbol_coverage.UaSymbolCoverageTest.test_low_similarity_move_with_no_symbols_is_regression) ... ok
test_partial_deletion_in_changed_source_is_regression (test_ua_symbol_coverage.UaSymbolCoverageTest.test_partial_deletion_in_changed_source_is_regression) ... ok
test_partially_covered_new_file_is_not_flagged (test_ua_symbol_coverage.UaSymbolCoverageTest.test_partially_covered_new_file_is_not_flagged) ... ok
test_python_defs_inside_strings_do_not_count (test_ua_symbol_coverage.UaSymbolCoverageTest.test_python_defs_inside_strings_do_not_count) ... ok
test_rename_dropping_symbols_is_regression (test_ua_symbol_coverage.UaSymbolCoverageTest.test_rename_dropping_symbols_is_regression) ... ok
test_rename_preserving_symbols_is_ok (test_ua_symbol_coverage.UaSymbolCoverageTest.test_rename_preserving_symbols_is_ok) ... ok
test_ruby_visibility_prefixed_defs_are_counted (test_ua_symbol_coverage.UaSymbolCoverageTest.test_ruby_visibility_prefixed_defs_are_counted) ... ok
test_shell_names_with_punctuation_are_counted (test_ua_symbol_coverage.UaSymbolCoverageTest.test_shell_names_with_punctuation_are_counted) ... ok
test_unchanged_source_loss_is_noted (test_ua_symbol_coverage.UaSymbolCoverageTest.test_unchanged_source_loss_is_noted) ... ok
test_unreadable_candidate_fails_closed (test_ua_symbol_coverage.UaSymbolCoverageTest.test_unreadable_candidate_fails_closed) ... ok
test_unresolvable_ref_fails_closed (test_ua_symbol_coverage.UaSymbolCoverageTest.test_unresolvable_ref_fails_closed) ... ok
test_uv_run_script_shebang_is_python (test_ua_symbol_coverage.UaSymbolCoverageTest.test_uv_run_script_shebang_is_python) ... ok
test_builds_in_the_clone_when_no_release_artifact_exists (test_update_agent_assets_ua_core.UnderstandAnythingCoreBuildTest.test_builds_in_the_clone_when_no_release_artifact_exists) ... ok
test_builds_missing_core_in_the_release_artifact_then_copies_it (test_update_agent_assets_ua_core.UnderstandAnythingCoreBuildTest.test_builds_missing_core_in_the_release_artifact_then_copies_it) ... ok
test_doctor_stale_warning_is_cleared_by_the_update_build (test_update_agent_assets_ua_core.UnderstandAnythingCoreBuildTest.test_doctor_stale_warning_is_cleared_by_the_update_build) ... ok
test_frozen_install_failure_falls_back_to_plain_install (test_update_agent_assets_ua_core.UnderstandAnythingCoreBuildTest.test_frozen_install_failure_falls_back_to_plain_install) ... ok
test_make_update_installs_the_pinned_pnpm (test_update_agent_assets_ua_core.UnderstandAnythingCoreBuildTest.test_make_update_installs_the_pinned_pnpm) ... ok
test_prefers_mise_exec_over_an_unbacked_pnpm_shim (test_update_agent_assets_ua_core.UnderstandAnythingCoreBuildTest.test_prefers_mise_exec_over_an_unbacked_pnpm_shim) ... ok
test_rebuilds_a_release_dist_older_than_its_sources (test_update_agent_assets_ua_core.UnderstandAnythingCoreBuildTest.test_rebuilds_a_release_dist_older_than_its_sources) ... ok
test_skips_the_build_when_the_release_artifact_already_has_dist (test_update_agent_assets_ua_core.UnderstandAnythingCoreBuildTest.test_skips_the_build_when_the_release_artifact_already_has_dist) ... ok
test_uses_mise_exec_when_pnpm_is_not_on_path (test_update_agent_assets_ua_core.UnderstandAnythingCoreBuildTest.test_uses_mise_exec_when_pnpm_is_not_on_path) ... ok
test_uses_path_pnpm_only_when_mise_is_absent (test_update_agent_assets_ua_core.UnderstandAnythingCoreBuildTest.test_uses_path_pnpm_only_when_mise_is_absent) ... ok
test_warns_and_continues_when_no_pnpm_is_resolvable (test_update_agent_assets_ua_core.UnderstandAnythingCoreBuildTest.test_warns_and_continues_when_no_pnpm_is_resolvable) ... ok
test_warns_and_continues_when_the_build_fails (test_update_agent_assets_ua_core.UnderstandAnythingCoreBuildTest.test_warns_and_continues_when_the_build_fails) ... ok
test_candidate_is_no_when_another_claude_family_is_larger (test_usage_review.UsageReviewTests.test_candidate_is_no_when_another_claude_family_is_larger) ... ok
test_malformed_latest_snapshot_warns_and_never_raises (test_usage_review.UsageReviewTests.test_malformed_latest_snapshot_warns_and_never_raises) ... ok
test_report_computes_share_ratio_and_baseline_deltas (test_usage_review.UsageReviewTests.test_report_computes_share_ratio_and_baseline_deltas) ... ok
test_report_emits_due_windows_and_matching_notes_suppress_them (test_usage_review.UsageReviewTests.test_report_emits_due_windows_and_matching_notes_suppress_them) ... ok
test_snapshot_does_not_rewrite_existing_daily_file (test_usage_review.UsageReviewTests.test_snapshot_does_not_rewrite_existing_daily_file) ... ok
test_a_masked_key_collision_fails_and_leaves_the_file_unchanged (test_validate_agent_assets.MaskSecretsModeTest.test_a_masked_key_collision_fails_and_leaves_the_file_unchanged) ... ok
test_leaves_allowed_placeholders_the_scan_accepts (test_validate_agent_assets.MaskSecretsModeTest.test_leaves_allowed_placeholders_the_scan_accepts) ... ok
test_masks_an_earlier_duplicate_member_so_the_scan_passes (test_validate_agent_assets.MaskSecretsModeTest.test_masks_an_earlier_duplicate_member_so_the_scan_passes) ... ok
test_masks_every_match_in_place_and_reports_counts (test_validate_agent_assets.MaskSecretsModeTest.test_masks_every_match_in_place_and_reports_counts) ... ok
test_masks_json_string_values_and_keeps_the_document_parseable (test_validate_agent_assets.MaskSecretsModeTest.test_masks_json_string_values_and_keeps_the_document_parseable) ... ok
test_missing_file_exits_2_without_touching_others (test_validate_agent_assets.MaskSecretsModeTest.test_missing_file_exits_2_without_touching_others) ... ok
test_a_key_after_json_escaped_whitespace_is_flagged (test_validate_agent_assets.SecretPatternBoundaryTest.test_a_key_after_json_escaped_whitespace_is_flagged) ... ok
test_a_key_prefix_inside_a_hyphenated_word_is_clean (test_validate_agent_assets.SecretPatternBoundaryTest.test_a_key_prefix_inside_a_hyphenated_word_is_clean) ... ok
test_a_long_hyphenated_run_scans_in_linear_time (test_validate_agent_assets.SecretPatternBoundaryTest.test_a_long_hyphenated_run_scans_in_linear_time) ... ok
test_a_real_key_prefix_is_still_flagged (test_validate_agent_assets.SecretPatternBoundaryTest.test_a_real_key_prefix_is_still_flagged) ... ok
test_an_sk_key_body_needs_a_hyphen_free_run (test_validate_agent_assets.SecretPatternBoundaryTest.test_an_sk_key_body_needs_a_hyphen_free_run) ... <frozen importlib._bootstrap>:170: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f274dac50>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:170: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f274d98a0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:170: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f271436a0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:170: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f27143d30>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:170: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f27143970>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:170: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f27143b50>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:170: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f27143f10>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:170: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f27143e20>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:170: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f26cfc8b0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:170: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f26cfe6b0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:170: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f26cfcb80>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:170: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f274db790>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:170: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f26cfd030>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:170: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f274db880>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:170: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f26cfd120>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:170: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f26cfc7c0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:170: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f26cfc310>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:170: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f26cfc220>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:170: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f26cfcd60>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:170: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f26cfcf40>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:170: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f26cfc5e0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:170: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f26cfe980>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:170: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f26cfef20>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:170: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f26cff010>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:170: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f26cff790>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:170: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f26cfee30>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:170: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f26cff6a0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:170: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f26cffa60>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:170: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f26cffb50>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:170: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f26e5c6d0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:170: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f26e5c4f0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:170: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f26e5c040>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:170: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f26e5c220>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:170: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f26e5c130>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:170: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f26e5c9a0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:170: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f26e5cc70>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:170: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f26e5cd60>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:170: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f26e5ce50>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:170: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f26e5cf40>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:170: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f26e5d030>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:170: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f26e5d120>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:170: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f26e5d210>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:170: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f26e5d300>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:170: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfa3f26e5d3f0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
ok
test_masking_keeps_the_escape_before_the_key (test_validate_agent_assets.SecretPatternBoundaryTest.test_masking_keeps_the_escape_before_the_key) ... ok
test_agent_manifest_accepts_a_worker_worktree_under_claude_worktrees (test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_accepts_a_worker_worktree_under_claude_worktrees) ... ok
test_agent_manifest_accepts_exact_security_profile_set (test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_accepts_exact_security_profile_set) ... ok
test_agent_manifest_pins_the_audit_codex_profile (test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_pins_the_audit_codex_profile) ... ok
test_agent_manifest_rejects_a_worker_worktree_outside_claude_worktrees (test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_a_worker_worktree_outside_claude_worktrees) ... ok
test_agent_manifest_rejects_invalid_or_missing_worker_kind (test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_invalid_or_missing_worker_kind) ... ok
test_agent_manifest_rejects_missing_audit_profile (test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_missing_audit_profile) ... ok
test_agent_manifest_rejects_missing_security_profile (test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_missing_security_profile) ... ok
test_agent_manifest_rejects_unknown_worker_profile (test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_unknown_worker_profile) ... ok
test_agent_manifest_rejects_wrong_security_codex_model (test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_wrong_security_codex_model) ... ok
test_agent_manifest_requires_fable_advisor_on_the_worker_profile (test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_fable_advisor_on_the_worker_profile) ... ok
test_agent_manifest_requires_readme_to_document_restart_worker (test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_readme_to_document_restart_worker) ... ok
test_agent_manifest_requires_readme_to_state_the_worker_kind (test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_readme_to_state_the_worker_kind) ... ok
test_agmsg_installer_requires_a_release_pin_and_its_tag (test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_installer_requires_a_release_pin_and_its_tag) ... ok
test_agmsg_installer_requires_the_full_tag_commit (test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_installer_requires_the_full_tag_commit) ... ok
test_agmsg_installer_requires_the_npm_bootstrap_integrity (test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_installer_requires_the_npm_bootstrap_integrity) ... ok
test_agmsg_ownership_accepts_the_installer_layout (test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_accepts_the_installer_layout) ... ok
test_agmsg_ownership_rejects_a_managed_claude_command (test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_rejects_a_managed_claude_command) ... ok
test_agmsg_ownership_rejects_a_vendored_skill_copy (test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_rejects_a_vendored_skill_copy) ... ok
test_agmsg_ownership_rejects_removing_installer_owned_paths (test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_rejects_removing_installer_owned_paths) ... ok
test_agmsg_ownership_requires_retiring_the_symlink_farm (test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_requires_retiring_the_symlink_farm) ... ok
test_assets_accept_complete_declarations_and_rendered_versions (test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_accept_complete_declarations_and_rendered_versions) ... ok
test_assets_reject_a_malformed_render_entry (test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_a_malformed_render_entry) ... ok
test_assets_reject_each_incomplete_declaration (test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_each_incomplete_declaration) ... ok
test_assets_reject_one_assignment_rendered_from_two_fields (test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_one_assignment_rendered_from_two_fields) ... ok
test_assets_reject_one_assignment_rendered_through_a_symlink_alias (test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_one_assignment_rendered_through_a_symlink_alias) ... ok
test_assets_reject_unrendered_literal_versions_anywhere_in_install_or_scripts (test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_unrendered_literal_versions_anywhere_in_install_or_scripts) ... ok
test_assets_report_an_unrendered_declare_r_version (test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_report_an_unrendered_declare_r_version) ... ok
test_assets_scan_setup_sh_for_unrendered_versions (test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_scan_setup_sh_for_unrendered_versions) ... ok
test_claude_mcp_config_accepts_an_empty_map_and_rejects_a_non_mapping (test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_mcp_config_accepts_an_empty_map_and_rejects_a_non_mapping) ... ok
test_claude_permissions_allow_must_list_non_empty_rules (test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_permissions_allow_must_list_non_empty_rules) ... ok
test_claude_sandbox_accepts_manifest_symmetric_settings (test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_accepts_manifest_symmetric_settings) ... ok
test_claude_sandbox_extra_allow_write_must_be_absolute_or_home_paths_without_globs (test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_extra_allow_write_must_be_absolute_or_home_paths_without_globs) ... ok
test_claude_sandbox_rejects_each_broken_rule (test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_rejects_each_broken_rule) ... ok
test_claude_sandbox_requires_extra_codex_writable_roots (test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_requires_extra_codex_writable_roots) ... ok
test_claude_sandbox_unix_sockets_must_be_absolute_or_home_paths_without_globs (test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_unix_sockets_must_be_absolute_or_home_paths_without_globs) ... ok
test_codex_modify_script_requires_executable_source (test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_modify_script_requires_executable_source) ... ok
test_codex_projects_accept_working_tree_placeholder (test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_projects_accept_working_tree_placeholder) ... ok
test_codex_projects_reject_hard_coded_macos_home (test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_projects_reject_hard_coded_macos_home) ... ok
test_codex_projects_reject_missing_working_tree_placeholder (test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_projects_reject_missing_working_tree_placeholder) ... ok
test_codex_sandbox_workspace_write_accepts_matching_manifest (test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_sandbox_workspace_write_accepts_matching_manifest) ... ok
test_codex_sandbox_workspace_write_must_match_manifest (test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_sandbox_workspace_write_must_match_manifest) ... ok
test_codex_sandbox_workspace_write_requires_all_agmsg_roots (test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_sandbox_workspace_write_requires_all_agmsg_roots) ... ok
test_hook_composition_accepts_managed_source_fixture (test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_accepts_managed_source_fixture) ... ok
test_hook_composition_pins_sessionstart_order (test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_pins_sessionstart_order) ... ok
test_hook_composition_rejects_duplicate_command (test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_rejects_duplicate_command) ... ok
test_hook_composition_rejects_sync_timeout_over_budget (test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_rejects_sync_timeout_over_budget) ... ok
test_hook_composition_requires_permgate_first (test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_requires_permgate_first) ... ok
test_manifest_home_paths_allow_chezmoi_home_dir (test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_allow_chezmoi_home_dir) ... ok
test_manifest_home_paths_allow_flow_style_projects (test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_allow_flow_style_projects) ... ok
test_manifest_home_paths_exempt_runtime_owned_projects (test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_exempt_runtime_owned_projects) ... ok
test_manifest_home_paths_only_exempt_the_projects_subtree (test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_only_exempt_the_projects_subtree) ... ok
test_manifest_home_paths_reject_hard_coded_home (test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_reject_hard_coded_home) ... ok
test_manifest_home_paths_reject_hard_coded_linux_home (test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_reject_hard_coded_linux_home) ... ok
test_manifest_home_paths_reject_non_codex_projects_mapping (test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_reject_non_codex_projects_mapping) ... ok
test_permgate_policy_requires_a_schema_3_object (test_validate_agent_assets.ValidateAgentAssetsTest.test_permgate_policy_requires_a_schema_3_object) ... ok
test_recursive_scans_skip_nested_git_trees_only (test_validate_agent_assets.ValidateAgentAssetsTest.test_recursive_scans_skip_nested_git_trees_only) ... ok
test_repo_claude_settings_accept_portable_interpreter (test_validate_agent_assets.ValidateAgentAssetsTest.test_repo_claude_settings_accept_portable_interpreter) ... ok
test_repo_claude_settings_reject_machine_specific_interpreter (test_validate_agent_assets.ValidateAgentAssetsTest.test_repo_claude_settings_reject_machine_specific_interpreter) ... ERROR: /tmp/validate-agent-assets-test-c87zvtko/.claude/settings.json hook SessionEnd must not hard-code a machine-specific home path: /Users/mryfmo/.local/share/mise/installs/python/3.14.7/bin/python3.14
ok
test_secret_scan_allows_exact_placeholder_tokens (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_allows_exact_placeholder_tokens) ... ok
test_secret_scan_checks_docs_paths (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_docs_paths) ... ok
test_secret_scan_checks_extensionless_executables (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_extensionless_executables) ... ok
test_secret_scan_checks_utf16_bom_text (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_utf16_bom_text) ... ok
test_secret_scan_fails_a_nul_in_orchestration_text_and_skips_other_binaries (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_fails_a_nul_in_orchestration_text_and_skips_other_binaries) ... ok
test_secret_scan_reads_json_per_key_and_string_value (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_reads_json_per_key_and_string_value) ... ok
test_secret_scan_rejects_placeholder_with_suffix (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_rejects_placeholder_with_suffix) ... ok
test_secret_scan_rejects_utf16_orchestration_text_with_the_nul_offset (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_rejects_utf16_orchestration_text_with_the_nul_offset) ... ok
test_checkout_does_not_persist_credentials_without_explicit_exemption (test_workflow_security.WorkflowSecurityTest.test_checkout_does_not_persist_credentials_without_explicit_exemption) ... ok
test_checkout_rejects_duplicate_or_non_false_credential_settings (test_workflow_security.WorkflowSecurityTest.test_checkout_rejects_duplicate_or_non_false_credential_settings) ... ok
test_checkout_setting_does_not_leak_from_the_next_step (test_workflow_security.WorkflowSecurityTest.test_checkout_setting_does_not_leak_from_the_next_step) ... ok
test_external_actions_use_full_commit_shas (test_workflow_security.WorkflowSecurityTest.test_external_actions_use_full_commit_shas) ... ok
test_quoted_unnamed_checkout_is_detected (test_workflow_security.WorkflowSecurityTest.test_quoted_unnamed_checkout_is_detected) ... ok
test_unnamed_checkout_setting_does_not_leak_from_the_next_step (test_workflow_security.WorkflowSecurityTest.test_unnamed_checkout_setting_does_not_leak_from_the_next_step) ... ok
test_workflows_have_exact_top_level_permissions (test_workflow_security.WorkflowSecurityTest.test_workflows_have_exact_top_level_permissions) ... ok
test_workflows_have_no_job_level_permission_overrides (test_workflow_security.WorkflowSecurityTest.test_workflows_have_no_job_level_permission_overrides) ... ok

----------------------------------------------------------------------
Ran 778 tests in 195.064s

OK
```

## make render-check; UV_CACHE_DIR=/tmp/t90-uv-cache; exit 0

```text
uv run --with pyyaml scripts/generate-agent-configs.py --check
generated agent configs are up to date
```

## make validate-agent-assets; UV_CACHE_DIR=/tmp/t90-uv-cache; exit 0 (regime-boundary warnings are existing open work)

```text
uv run --with pyyaml scripts/validate-agent-assets.py
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/acceptance/dotfiles-T69-protocol-docs-unification-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/acceptance/dotfiles-T72-bootstrap-ci-pins-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/acceptance/dotfiles-T76-ineffective-settings-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/acceptance/dotfiles-T77-harness-dead-code-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/acceptance/dotfiles-T96-codex-worker-gpt61-sol-high-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/acceptance/dotfiles-T97-claude-sandbox-github-calls-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/autoskill/runs/dotfiles-T72-bootstrap-ci-pins-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/autoskill/runs/dotfiles-T76-ineffective-settings-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/autoskill/runs/dotfiles-T77-harness-dead-code-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/autoskill/runs/dotfiles-T96-codex-worker-gpt61-sol-high-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/autoskill/runs/dotfiles-T97-claude-sandbox-github-calls-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/learning/dotfiles-T72-bootstrap-ci-pins-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/learning/dotfiles-T76-ineffective-settings-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/learning/dotfiles-T77-harness-dead-code-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/learning/dotfiles-T96-codex-worker-gpt61-sol-high-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/learning/dotfiles-T97-claude-sandbox-github-calls-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/reports/dotfiles-T72-bootstrap-ci-pins-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/reports/dotfiles-T76-ineffective-settings-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/reports/dotfiles-T77-harness-dead-code-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/reports/dotfiles-T96-codex-worker-gpt61-sol-high-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/reports/dotfiles-T97-claude-sandbox-github-calls-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/sandboxes/dotfiles-T72-bootstrap-ci-pins-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/sandboxes/dotfiles-T76-ineffective-settings-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/sandboxes/dotfiles-T77-harness-dead-code-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/sandboxes/dotfiles-T96-codex-worker-gpt61-sol-high-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/sandboxes/dotfiles-T97-claude-sandbox-github-calls-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/tasks/dotfiles-T80-codex-command-hooks-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/tasks/dotfiles-T81-compactiondb-vendor-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/tasks/dotfiles-T97-claude-sandbox-github-calls-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T69-protocol-docs-unification-a01-audit-4656f19.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T69-protocol-docs-unification-a01-audit-4656f19.md.last.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T69-protocol-docs-unification-a01-audit-6b060ac.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T69-protocol-docs-unification-a01-audit-6b060ac.md.last.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T69-protocol-docs-unification-a01-audit-d9bbd80.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T69-protocol-docs-unification-a01-audit-d9bbd80.md.last.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T72-bootstrap-ci-pins-a01-audit-d5856e2.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T72-bootstrap-ci-pins-a01-audit-d5856e2.md.last.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T72-bootstrap-ci-pins-a01-crit.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T72-bootstrap-ci-pins-a01-pr-feedback.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T72-bootstrap-ci-pins-a01-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T72-bootstrap-ci-pins-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T76-ineffective-settings-a01-audit-26a882a.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T76-ineffective-settings-a01-audit-26a882a.md.last.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T76-ineffective-settings-a01-audit-f805ee3.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T76-ineffective-settings-a01-audit-f805ee3.md.last.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T76-ineffective-settings-a01-crit.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T76-ineffective-settings-a01-pr-feedback.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T76-ineffective-settings-a01-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T76-ineffective-settings-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T77-harness-dead-code-a01-audit-977bdf1.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T77-harness-dead-code-a01-audit-977bdf1.md.last.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T77-harness-dead-code-a01-crit.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T77-harness-dead-code-a01-pr-feedback.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T77-harness-dead-code-a01-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T77-harness-dead-code-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T96-codex-worker-gpt61-sol-high-a01-audit-3a06011.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T96-codex-worker-gpt61-sol-high-a01-audit-3a06011.md.last.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T96-codex-worker-gpt61-sol-high-a01-crit.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T96-codex-worker-gpt61-sol-high-a01-pr-feedback.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T96-codex-worker-gpt61-sol-high-a01-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T96-codex-worker-gpt61-sol-high-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-audit-391d2b4.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-audit-391d2b4.md.last.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-audit-5b6b0d9.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-audit-5b6b0d9.md.last.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-audit-8ffa554.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-audit-8ffa554.md.last.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-audit-efe6735.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-audit-efe6735.md.last.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-crit.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-pr-feedback.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-worker-crit.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-worker-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/autoskill/runs/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/autoskill/runs/dotfiles-T97-claude-sandbox-github-calls-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/learning/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/learning/dotfiles-T97-claude-sandbox-github-calls-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/reports/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/reports/dotfiles-T97-claude-sandbox-github-calls-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/sandboxes/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/sandboxes/dotfiles-T97-claude-sandbox-github-calls-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/validation/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-worker-crit.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-worker-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01.md
WARN: regime-boundary: additional worker workspace still open: dotfiles worker worker-d (herdr-agents --remove-worker)
WARN: regime-boundary: additional worker tab still open in dotfiles: dotfiles:codex-security-dot-a007 (herdr-agents --remove-worker)
agent asset validation ok
```

## mise x shfmt -- shfmt -i 4 -sr -d <launcher> scripts/check-tools.sh; exit 0

```text
```

## shellcheck <launcher> scripts/check-tools.sh; exit 0

```text
```

## mise x node npm:prettier -- prettier --check README.md <SKILL> <rule>; exit 0

```text
Checking formatting...
All matched files use Prettier code style!
```

## Optional ruff check with ambient config (exit 1; superseded by repository formatting-only validation, no broad lint fixes)

```text
B020 Loop control variable `index` overrides iterable it iterates
   --> scripts/generate-agent-configs.py:211:13
    |
209 |         indent = " " * (4 + 2 * depth)
210 |         key = f"{indent}{part}:"
211 |         for index in range(index + 1, len(lines)):
    |             ^^^^^
212 |             line = lines[index]
213 |             if line.strip() and len(line) - len(line.lstrip(" ")) < len(indent):
    |

FURB167 [*] Use of regular expression alias `re.M`
   --> scripts/generate-agent-configs.py:243:107
    |
241 |                 text = path.read_text()
242 |             for constant, field in entry["constants"].items():
243 |                 pattern = re.compile(rf'^((?:readonly |declare -r )?{re.escape(constant)}=)"[^"$`\\]*"$', re.M)
    |                                                                                                           ^^^^
244 |                 value = asset_field(asset, field)
245 |                 if not PLAIN_PIN_VALUE.fullmatch(value):
    |
help: Replace with `re.MULTILINE`
    |
242 |             for constant, field in entry["constants"].items():
    -                 pattern = re.compile(rf'^((?:readonly |declare -r )?{re.escape(constant)}=)"[^"$`\\]*"$', re.M)
243 +                 pattern = re.compile(rf'^((?:readonly |declare -r )?{re.escape(constant)}=)"[^"$`\\]*"$', re.MULTILINE)
244 |                 value = asset_field(asset, field)
    |

B023 Function definition does not bind loop variable `value`
   --> scripts/generate-agent-configs.py:247:78
    |
245 |                 if not PLAIN_PIN_VALUE.fullmatch(value):
246 |                     fail(f"assets.{name}.{field} is not a plain pin value: {value!r}")
247 |                 text, count = pattern.subn(lambda match: f'{match.group(1)}"{value}"', text)
    |                                                                              ^^^^^
248 |                 if count != 1:
249 |                     fail(f"{entry['file']} must assign {constant} exactly once for assets.{name}")
    |

SIM102 Use a single `if` statement instead of nested `if` statements
   --> scripts/generate-agent-configs.py:927:9
    |
925 |       stale_profiles = stale_profile_outputs(manifest)
926 |       for path, content in outputs.items():
927 | /         if args.check:
928 | |             if not path.exists() or path.read_text() != content:
    | |________________________________________________________________^
929 |                   stale.append(path.relative_to(ROOT))
930 |       if args.check:
    |
help: Combine `if` statements using `and`

I001 [*] Import block is un-sorted or un-formatted
  --> scripts/require-crit-review.py:4:1
   |
 2 |   """Require native agent review for meaningful repository changes."""
 3 |
 4 | / from __future__ import annotations
 5 | |
 6 | | import argparse
 7 | | import importlib.util
 8 | | import json
 9 | | import os
10 | | import re
11 | | import shlex
12 | | import subprocess
13 | | import tempfile
14 | | from collections import Counter
15 | | from datetime import datetime
16 | | from functools import cache
17 | | import sys
18 | | from pathlib import Path
   | |________________________^
help: Organize imports
   |
12 | import subprocess
13 + import sys
14 | import tempfile
15 | from collections import Counter
16 | from datetime import datetime
17 | from functools import cache
   - import sys
18 | from pathlib import Path
   -
19 |
   |

FURB167 [*] Use of regular expression alias `re.S`
  --> scripts/require-crit-review.py:28:113
   |
26 | AUDIT_ENV = "AUDIT_EVIDENCE"
27 | AUDIT_DISPOSITIONS_ENV = "AUDIT_DISPOSITIONS"
28 | PR_FEEDBACK_DISPOSITION = re.compile(r"(?:fixed:(?P<commit>[0-9a-f]{7,40})|not-applicable:(?P<reason>.*\S.*))", re.S)
   |                                                                                                                 ^^^^
29 | FAILURE_REASON_MIN_CHARS = 20
30 | # herdr-agents --audit names and concludes the task-level audit this way.
   |
help: Replace with `re.DOTALL`
   |
27 | AUDIT_DISPOSITIONS_ENV = "AUDIT_DISPOSITIONS"
   - PR_FEEDBACK_DISPOSITION = re.compile(r"(?:fixed:(?P<commit>[0-9a-f]{7,40})|not-applicable:(?P<reason>.*\S.*))", re.S)
28 + PR_FEEDBACK_DISPOSITION = re.compile(r"(?:fixed:(?P<commit>[0-9a-f]{7,40})|not-applicable:(?P<reason>.*\S.*))", re.DOTALL)
29 | FAILURE_REASON_MIN_CHARS = 20
   |

FURB167 [*] Use of regular expression alias `re.M`
  --> scripts/require-crit-review.py:33:60
   |
31 | AUDIT_NAME = re.compile(r"(?P<task>.+)-audit-(?P<sha>[0-9a-f]{7,40})\.md")
32 | AUDIT_VERDICT = re.compile(r"\s*Verdict: (correct|incorrect|blocked)\s*")
33 | AUDIT_FINDING = re.compile(r"^\s*(?:[-*+]\s+)?\[P[0-3]\]", re.M)
   |                                                            ^^^^
34 | AUDIT_FINDING_DISPOSITION_PREFIX = "audit-finding:"
35 | AUDIT_FINDING_NUMBER = re.compile(rf"{AUDIT_FINDING_DISPOSITION_PREFIX}\s*(?P<number>\d+)\b")
   |
help: Replace with `re.MULTILINE`
   |
32 | AUDIT_VERDICT = re.compile(r"\s*Verdict: (correct|incorrect|blocked)\s*")
   - AUDIT_FINDING = re.compile(r"^\s*(?:[-*+]\s+)?\[P[0-3]\]", re.M)
33 + AUDIT_FINDING = re.compile(r"^\s*(?:[-*+]\s+)?\[P[0-3]\]", re.MULTILINE)
34 | AUDIT_FINDING_DISPOSITION_PREFIX = "audit-finding:"
   |

UP022 Prefer `capture_output` over sending `stdout` and `stderr` to `PIPE`
   --> scripts/require-crit-review.py:119:12
    |
118 |   def run_git(args: list[str], root: Path | None = None) -> subprocess.CompletedProcess[str]:
119 |       return subprocess.run(
    |  ____________^
120 | |         ["git", *args],
121 | |         cwd=root,
122 | |         check=False,
123 | |         text=True,
124 | |         stdout=subprocess.PIPE,
125 | |         stderr=subprocess.PIPE,
126 | |     )
    | |_____^
help: Replace with `capture_output` keyword argument

PLW1510 `subprocess.run` without explicit `check` argument
   --> scripts/require-crit-review.py:570:22
    |
568 |             if paginate:
569 |                 command += ["--paginate", "--slurp"]
570 |             result = subprocess.run(command, cwd=root, env=env, capture_output=True, text=True)
    |                      ^^^^^^^^^^^^^^
571 |             if result.returncode:
572 |                 raise ValueError("GitHub API verification failed")
    |
help: Add explicit `check=False`

FURB162 Unnecessary timezone replacement with zero offset
   --> scripts/require-crit-review.py:608:48
    |
607 |         def decision_order(review):
608 |             submitted = datetime.fromisoformat(review["submitted_at"].replace("Z", "+00:00"))
    |                                                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
609 |             if submitted.tzinfo is None or type(review["id"]) is not int:
610 |                 raise ValueError("invalid review submission metadata")
    |
help: Remove `.replace()` call

UP022 Prefer `capture_output` over sending `stdout` and `stderr` to `PIPE`
   --> scripts/require-crit-review.py:652:18
    |
650 |               collector = Path(temporary) / "pr-feedback.py"
651 |               collector.write_text(base_collector.stdout)
652 |           result = subprocess.run(
    |  __________________^
653 | |             [sys.executable, str(collector), str(pr), "--repo", evidence["repo"], "--json", str(collected_path)],
654 | |             cwd=root,
655 | |             check=False,
656 | |             text=True,
657 | |             stdout=subprocess.PIPE,
658 | |             stderr=subprocess.PIPE,
659 | |         )
    | |_________^
660 |           if result.returncode != 0 or not collected_path.is_file():
661 |               detail = (result.stderr or result.stdout).strip().splitlines()[-1:] or ["no output"]
    |
help: Replace with `capture_output` keyword argument

EXE001 Shebang is present but file is not executable
 --> tests/unit/test_generate_agent_configs.py:1:1
  |
1 | #!/usr/bin/env python3
  | ^^^^^^^^^^^^^^^^^^^^^^
2 | """Exercise focused checks in generate-agent-configs.py."""
  |

SIM117 Use a single `with` statement with multiple contexts instead of nested `with` statements
   --> tests/unit/test_generate_agent_configs.py:328:13
    |
326 |           )
327 |           for name, path, value in cases:
328 | /             with self.subTest(target=f"{name}.{path}", value=value):
329 | |                 with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
    | |______________________________________________________________________________________________^
330 |                       self.module.set_asset_field(self.MANIFEST_TEXT, name, path, value)
    |
help: Combine `with` statements

UP022 Prefer `capture_output` over sending `stdout` and `stderr` to `PIPE`
   --> tests/unit/test_generate_agent_configs.py:506:18
    |
504 |           self.assertTrue(standard_profile.stat().st_mode & 0o111)
505 |
506 |           result = subprocess.run(
    |  __________________^
507 | |             [str(standard_profile)],
508 | |             input='model = "runtime"\nmodel_reasoning_effort = "high"\n\n[hooks.state]\ntrusted = true\n',
509 | |             text=True,
510 | |             stdout=subprocess.PIPE,
511 | |             stderr=subprocess.PIPE,
512 | |             env={
513 | |                 **os.environ,
514 | |                 "HOME": str(self.temp_dir / "target-home"),
515 | |                 "CHEZMOI_SOURCE_DIR": str(self.temp_dir / "home"),
516 | |                 "CHEZMOI_HOME_DIR": str(self.temp_dir / "target-home"),
517 | |             },
518 | |             check=False,
519 | |         )
    | |_________^
520 |
521 |           self.assertEqual(result.returncode, 0, result.stderr)
    |
help: Replace with `capture_output` keyword argument

UP022 Prefer `capture_output` over sending `stdout` and `stderr` to `PIPE`
   --> tests/unit/test_generate_agent_configs.py:543:18
    |
542 |           home = self.temp_dir / "target-home"
543 |           result = subprocess.run(
    |  __________________^
544 | |             [str(security_profile)],
545 | |             input="",
546 | |             text=True,
547 | |             stdout=subprocess.PIPE,
548 | |             stderr=subprocess.PIPE,
549 | |             env={**os.environ, "HOME": str(home)},
550 | |             check=False,
551 | |         )
    | |_________^
552 |
553 |           self.assertEqual(result.returncode, 0, result.stderr)
    |
help: Replace with `capture_output` keyword argument

UP022 Prefer `capture_output` over sending `stdout` and `stderr` to `PIPE`
   --> tests/unit/test_generate_agent_configs.py:604:22
    |
602 |           def render(name: str) -> dict:
603 |               path = self.temp_dir / f"home/dot_codex/modify_private_{name}.config.toml"
604 |               result = subprocess.run(
    |  ______________________^
605 | |                 [str(path)],
606 | |                 input="",
607 | |                 text=True,
608 | |                 stdout=subprocess.PIPE,
609 | |                 stderr=subprocess.PIPE,
610 | |                 check=False,
611 | |             )
    | |_____________^
612 |               self.assertEqual(result.returncode, 0, result.stderr)
613 |               return tomllib.loads(result.stdout)
    |
help: Replace with `capture_output` keyword argument

UP022 Prefer `capture_output` over sending `stdout` and `stderr` to `PIPE`
   --> tests/unit/test_generate_agent_configs.py:652:18
    |
650 |               "trusted = true\n"
651 |           )
652 |           result = subprocess.run(
    |  __________________^
653 | |             [str(standard_profile)],
654 | |             input=current,
655 | |             text=True,
656 | |             stdout=subprocess.PIPE,
657 | |             stderr=subprocess.PIPE,
658 | |             env={**os.environ, "HOME": str(self.temp_dir / "target-home")},
659 | |             check=False,
660 | |         )
    | |_________^
661 |
662 |           self.assertEqual(result.returncode, 0, result.stderr)
    |
help: Replace with `capture_output` keyword argument

UP022 Prefer `capture_output` over sending `stdout` and `stderr` to `PIPE`
   --> tests/unit/test_generate_agent_configs.py:687:18
    |
685 |               'name = "second"\n'
686 |           )
687 |           result = subprocess.run(
    |  __________________^
688 | |             [str(standard_profile)],
689 | |             input=current,
690 | |             text=True,
691 | |             stdout=subprocess.PIPE,
692 | |             stderr=subprocess.PIPE,
693 | |             env={**os.environ, "HOME": str(self.temp_dir / "target-home")},
694 | |             check=False,
695 | |         )
    | |_________^
696 |
697 |           self.assertEqual(result.returncode, 0, result.stderr)
    |
help: Replace with `capture_output` keyword argument

UP022 Prefer `capture_output` over sending `stdout` and `stderr` to `PIPE`
   --> tests/unit/test_generate_agent_configs.py:725:18
    |
723 |           )
724 |
725 |           result = subprocess.run(
    |  __________________^
726 | |             [str(standard_profile)],
727 | |             input=(
728 | |                 "[hooks.state]\n\n"
729 | |                 '[hooks.state."/home/.codex/config.toml:permission_request:0:0"]\n'
730 | |                 'trusted_hash = "sha256:profile"\n'
731 | |             ),
732 | |             text=True,
733 | |             stdout=subprocess.PIPE,
734 | |             stderr=subprocess.PIPE,
735 | |             env={**os.environ, "HOME": str(home)},
736 | |             check=False,
737 | |         )
    | |_________^
738 |
739 |           self.assertEqual(result.returncode, 0, result.stderr)
    |
help: Replace with `capture_output` keyword argument

UP022 Prefer `capture_output` over sending `stdout` and `stderr` to `PIPE`
   --> tests/unit/test_generate_agent_configs.py:754:18
    |
752 |           current = '[hooks.state."hook"]\ntrusted_hash = "sha256:profile"\n'
753 |
754 |           result = subprocess.run(
    |  __________________^
755 | |             [str(profile)],
756 | |             input=current,
757 | |             text=True,
758 | |             stdout=subprocess.PIPE,
759 | |             stderr=subprocess.PIPE,
760 | |             env={**os.environ, "HOME": str(home)},
761 | |             check=False,
762 | |         )
    | |_________^
763 |
764 |           self.assertEqual(result.returncode, 0, result.stderr)
    |
help: Replace with `capture_output` keyword argument

UP022 Prefer `capture_output` over sending `stdout` and `stderr` to `PIPE`
   --> tests/unit/test_generate_agent_configs.py:781:18
    |
779 |           current = '[hooks.state."hook"]\ntrusted_hash = "sha256:same"\n'
780 |
781 |           result = subprocess.run(
    |  __________________^
782 | |             [str(profile)],
783 | |             input=current,
784 | |             text=True,
785 | |             stdout=subprocess.PIPE,
786 | |             stderr=subprocess.PIPE,
787 | |             env={**os.environ, "HOME": str(home)},
788 | |             check=False,
789 | |         )
    | |_________^
790 |
791 |           self.assertEqual(result.returncode, 0, result.stderr)
    |
help: Replace with `capture_output` keyword argument

EXE001 Shebang is present but file is not executable
 --> tests/unit/test_herdr_agents.py:1:1
  |
1 | #!/usr/bin/env python3
  | ^^^^^^^^^^^^^^^^^^^^^^
2 | """Exercise the Herdr agent workspace helper with fake CLIs."""
  |

I001 [*] Import block is un-sorted or un-formatted
  --> tests/unit/test_herdr_agents.py:4:1
   |
 2 |   """Exercise the Herdr agent workspace helper with fake CLIs."""
 3 |
 4 | / from __future__ import annotations
 5 | |
 6 | | import json
 7 | | import os
 8 | | import re
 9 | | import shlex
10 | | import shutil
11 | | import socket
12 | | import sqlite3
13 | | import subprocess
14 | | import sys
15 | | import tempfile
16 | | import textwrap
17 | | import threading
18 | | import time
19 | | import unittest
20 | | from pathlib import Path
21 | |
22 | | import tomllib
   | |______________^
23 |
24 |   ROOT = Path(__file__).resolve().parents[2]
   |
help: Organize imports
   |
18 | import time
19 + import tomllib
20 | import unittest
21 | from pathlib import Path
   -
   - import tomllib
22 |
   |

UP022 Prefer `capture_output` over sending `stdout` and `stderr` to `PIPE`
   --> tests/unit/test_herdr_agents.py:515:16
    |
513 |           if extra_env:
514 |               env.update(extra_env)
515 |           return subprocess.run(
    |  ________________^
516 | |             ["bash", str(SCRIPT), *mode, str(self.workdir)],
517 | |             cwd=ROOT,
518 | |             env=env,
519 | |             check=False,
520 | |             text=True,
521 | |             stdout=subprocess.PIPE,
522 | |             stderr=subprocess.PIPE,
523 | |         )
    | |_________^
524 |
525 |       def run_attach_helper(
    |
help: Replace with `capture_output` keyword argument

UP022 Prefer `capture_output` over sending `stdout` and `stderr` to `PIPE`
   --> tests/unit/test_herdr_agents.py:567:16
    |
565 |               else {"stdin": stdin_fd if stdin_fd is not None else subprocess.DEVNULL}
566 |           )
567 |           return subprocess.run(
    |  ________________^
568 | |             ["bash", str(SCRIPT), "--attach"],
569 | |             cwd=cwd or self.workdir,
570 | |             env=env,
571 | |             check=False,
572 | |             **stdin_args,
573 | |             text=True,
574 | |             stdout=subprocess.PIPE,
575 | |             stderr=subprocess.PIPE,
576 | |         )
    | |_________^
577 |
578 |       def run_agmsg_bootstrap_helper(
    |
help: Replace with `capture_output` keyword argument

UP022 Prefer `capture_output` over sending `stdout` and `stderr` to `PIPE`
   --> tests/unit/test_herdr_agents.py:587:16
    |
585 |           if extra_env:
586 |               env.update(extra_env)
587 |           return subprocess.run(
    |  ________________^
588 | |             ["bash", str(SCRIPT), "--bootstrap-agmsg", str(self.workdir)],
589 | |             cwd=ROOT,
590 | |             env=env,
591 | |             check=False,
592 | |             text=True,
593 | |             stdout=subprocess.PIPE,
594 | |             stderr=subprocess.PIPE,
595 | |         )
    | |_________^
596 |
597 |       def test_attach_without_herdr_environment_prints_the_bring_up_summary(self) -> None:
    |
help: Replace with `capture_output` keyword argument

ISC004 Unparenthesized implicit string concatenation in collection
   --> tests/unit/test_herdr_agents.py:819:17
    |
817 |               ('{"result":{"layout":{"panes":[]}}}\n', 42),
818 |               (
819 | /                 '{"result":{"layout":{"panes":['
820 | |                 '{"pane_id":"w-attach:p1","rect":{"x":0,"width":"wide"}},'
821 | |                 '{"pane_id":"w-attach:p2","rect":{"x":40,"width":40}}'
822 | |                 "]}}}\n",
    | |________________________^
823 |                   0,
824 |               ),
    |
help: Did you forget a comma?
help: Wrap implicitly concatenated strings in parentheses

ISC004 Unparenthesized implicit string concatenation in collection
   --> tests/unit/test_herdr_agents.py:826:17
    |
824 |               ),
825 |               (
826 | /                 '{"result":{"layout":{"panes":['
827 | |                 '{"pane_id":"w-attach:p1","rect":{"x":0,"width":40}},'
828 | |                 '{"pane_id":"w-attach:p2","rect":{"x":40,"width":40}}'
829 | |                 '],"splits":[]}}}\n',
    | |____________________________________^
830 |                   0,
831 |               ),
    |
help: Did you forget a comma?
help: Wrap implicitly concatenated strings in parentheses

UP022 Prefer `capture_output` over sending `stdout` and `stderr` to `PIPE`
    --> tests/unit/test_herdr_agents.py:1224:26
     |
1222 |           for target in ("update", "upgrade"):
1223 |               with self.subTest(target=target):
1224 |                   result = subprocess.run(
     |  __________________________^
1225 | |                     ["make", "-n", "-f", str(MAKEFILE), target],
1226 | |                     cwd=ROOT,
1227 | |                     check=False,
1228 | |                     text=True,
1229 | |                     stdout=subprocess.PIPE,
1230 | |                     stderr=subprocess.PIPE,
1231 | |                 )
     | |_________________^
1232 |
1233 |                   self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
     |
help: Replace with `capture_output` keyword argument

UP022 Prefer `capture_output` over sending `stdout` and `stderr` to `PIPE`
    --> tests/unit/test_herdr_agents.py:1246:18
     |
1244 |           env["CHEZMOI_HOME_DIR"] = str(self.home_dir)
1245 |
1246 |           result = subprocess.run(
     |  __________________^
1247 | |             [sys.executable, str(CLAUDE_SETTINGS_MODIFIER)],
1248 | |             input="",
1249 | |             env=env,
1250 | |             check=False,
1251 | |             text=True,
1252 | |             stdout=subprocess.PIPE,
1253 | |             stderr=subprocess.PIPE,
1254 | |         )
     | |_________^
1255 |
1256 |           self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
     |
help: Replace with `capture_output` keyword argument

UP022 Prefer `capture_output` over sending `stdout` and `stderr` to `PIPE`
    --> tests/unit/test_herdr_agents.py:3338:16
     |
3336 |       def run_boundary_check(self, worktree: Path) -> subprocess.CompletedProcess[str]:
3337 |           env = {**os.environ, "HOME": str(self.home_dir), "PATH": f"{self.bin_dir}{os.pathsep}/usr/bin{os.pathsep}/bin"}
3338 |           return subprocess.run(
     |  ________________^
3339 | |             ["bash", str(worktree / "scripts/check-regime-boundary.sh"), "--report"],
3340 | |             cwd=worktree,
3341 | |             env=env,
3342 | |             check=False,
3343 | |             text=True,
3344 | |             stdout=subprocess.PIPE,
3345 | |             stderr=subprocess.PIPE,
3346 | |         )
     | |_________^
3347 |
3348 |       def test_regime_boundary_check_scans_every_worktree_for_untracked_evidence(self) -> None:
     |
help: Replace with `capture_output` keyword argument

RUF059 Unpacked variable `main` is never used
    --> tests/unit/test_herdr_agents.py:3349:9
     |
3348 |     def test_regime_boundary_check_scans_every_worktree_for_untracked_evidence(self) -> None:
3349 |         main, worktree, other = self.boundary_repo()
     |         ^^^^
3350 |         (other / ".orchestration/reports").mkdir(parents=True)
3351 |         (other / ".orchestration/reports/t.md").write_text("x\n")
     |
help: Prefix it with an underscore or any other dummy variable pattern

RUF059 Unpacked variable `other` is never used
    --> tests/unit/test_herdr_agents.py:3362:25
     |
3361 |     def test_regime_boundary_check_flags_empty_seats_only(self) -> None:
3362 |         main, worktree, other = self.boundary_repo()
     |                         ^^^^^
3363 |         scripts = self.home_dir / ".agents/skills/agmsg/scripts"
3364 |         scripts.mkdir(parents=True, exist_ok=True)
     |
help: Prefix it with an underscore or any other dummy variable pattern

RUF059 Unpacked variable `other` is never used
    --> tests/unit/test_herdr_agents.py:3379:25
     |
3378 |     def test_regime_boundary_check_counts_names_across_runtime_types_at_an_active_seat(self) -> None:
3379 |         main, worktree, other = self.boundary_repo()
     |                         ^^^^^
3380 |         profiles = self.home_dir / ".agents/model-profiles.env"
3381 |         profiles.parent.mkdir(parents=True, exist_ok=True)
     |
help: Prefix it with an underscore or any other dummy variable pattern

ISC004 Unparenthesized implicit string concatenation in collection
    --> tests/unit/test_herdr_agents.py:3491:17
     |
3489 |           self.assertEqual(
3490 |               [
3491 | /                 "regime-boundary: additional worker tab still open in dotfiles: "
3492 | |                 "dotfiles:claude-standard-dot-a007 (herdr-agents --remove-worker)"
     | |__________________________________________________________________________________^
3493 |               ],
3494 |               reported,
     |
help: Did you forget a comma?
help: Wrap implicitly concatenated strings in parentheses

PIE810 Call `startswith` once with a `tuple`
    --> tests/unit/test_herdr_agents.py:3913:17
     |
3911 |           self.assertFalse(
3912 |               any(
3913 | /                 call.startswith(("workspace create", "pane split", "agent prompt"))
3914 | |                 or call.startswith("agent start claude-orchestrator-")
     | |______________________________________________________________________^
3915 |                   for call in calls
3916 |               ),
     |
help: Merge into a single `startswith` call

ISC004 Unparenthesized implicit string concatenation in collection
    --> tests/unit/test_herdr_agents.py:4241:17
     |
4239 |               (
4240 |                   "l",
4241 | /                 "user\nReview commit\ncodex\n- [P2] Broken quoting.\nVerdict: incorrect\n"
4242 | |                 "tokens used\n12,345\n- [P2] Broken quoting.\nVerdict: incorrect\n",
     | |___________________________________________________________________________________^
4243 |                   1,
4244 |                   "incorrect",
     |
help: Did you forget a comma?
help: Wrap implicitly concatenated strings in parentheses

UP022 Prefer `capture_output` over sending `stdout` and `stderr` to `PIPE`
    --> tests/unit/test_herdr_agents.py:5398:18
     |
5396 |           self.write_executable("editor", f'#!/usr/bin/env bash\nprintf "%s\\n" "$*" > {editor_calls}\n')
5397 |           env = {"PATH": f"{self.bin_dir}:/usr/bin:/bin", "EDITOR": "editor"}
5398 |           result = subprocess.run(
     |  __________________^
5399 | |             [
5400 | |                 "bash",
5401 | |                 "-c",
5402 | |                 config["opener"]["edit"][0]["run"].replace("%s", "example.txt"),
5403 | |             ],
5404 | |             env=env,
5405 | |             check=False,
5406 | |             text=True,
5407 | |             stdout=subprocess.PIPE,
5408 | |             stderr=subprocess.PIPE,
5409 | |         )
     | |_________^
5410 |
5411 |           self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
     |
help: Replace with `capture_output` keyword argument

UP022 Prefer `capture_output` over sending `stdout` and `stderr` to `PIPE`
    --> tests/unit/test_herdr_agents.py:5417:18
     |
5415 |           self.write_executable("zed", f'#!/usr/bin/env bash\nprintf "%s\\n" "$*" > {zed_calls}\n')
5416 |           editor_calls.unlink()
5417 |           result = subprocess.run(
     |  __________________^
5418 | |             [
5419 | |                 "bash",
5420 | |                 "-c",
5421 | |                 config["opener"]["edit"][0]["run"].replace("%s", "example.txt"),
5422 | |             ],
5423 | |             env=env,
5424 | |             check=False,
5425 | |             text=True,
5426 | |             stdout=subprocess.PIPE,
5427 | |             stderr=subprocess.PIPE,
5428 | |         )
     | |_________^
5429 |
5430 |           self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
     |
help: Replace with `capture_output` keyword argument

I001 [*] Import block is un-sorted or un-formatted
  --> tests/unit/test_require_crit_review.py:4:1
   |
 2 |   """Exercise the review guard in isolated git repositories."""
 3 |
 4 | / from __future__ import annotations
 5 | |
 6 | | import json
 7 | | import os
 8 | | import shutil
 9 | | import subprocess
10 | | import sys
11 | | import tempfile
12 | | import unittest
13 | | from pathlib import Path
   | |________________________^
help: Organize imports
   |
14 |
   -
15 | ROOT = Path(__file__).resolve().parents[2]
   |

UP022 Prefer `capture_output` over sending `stdout` and `stderr` to `PIPE`
  --> tests/unit/test_require_crit_review.py:24:12
   |
22 |       if env:
23 |           merged_env.update(env)
24 |       return subprocess.run(
   |  ____________^
25 | |         command,
26 | |         cwd=cwd,
27 | |         env=merged_env,
28 | |         check=False,
29 | |         text=True,
30 | |         stdout=subprocess.PIPE,
31 | |         stderr=subprocess.PIPE,
32 | |     )
   | |_____^
help: Replace with `capture_output` keyword argument

EXE001 Shebang is present but file is not executable
 --> tests/unit/test_runtime_health.py:1:1
  |
1 | #!/usr/bin/env python3
  | ^^^^^^^^^^^^^^^^^^^^^^
2 | """Verify truthful runtime artifact, doctor, and upgrade behavior."""
  |

ISC004 Unparenthesized implicit string concatenation in collection
   --> tests/unit/test_runtime_health.py:421:17
    |
419 |                   "bash",
420 |                   "-c",
421 | /                 "source scripts/update-agent-assets.sh; "
422 | |                 "CRIT_PIN_VERSION=v9.9.9; "
423 | |                 f"CRIT_LINUX_AMD64_SHA256={checksum}; "
424 | |                 "ensure_crit_cli",
    | |_________________________________^
425 |               ],
426 |               cwd=repo,
    |
help: Did you forget a comma?
help: Wrap implicitly concatenated strings in parentheses

ISC004 Unparenthesized implicit string concatenation in collection
   --> tests/unit/test_runtime_health.py:444:17
    |
442 |                   "bash",
443 |                   "-c",
444 | /                 "source scripts/update-agent-assets.sh; "
445 | |                 "CRIT_PIN_VERSION=v9.9.9; "
446 | |                 f"CRIT_LINUX_AMD64_SHA256={checksum}; "
447 | |                 "ensure_crit_cli",
    | |_________________________________^
448 |               ],
449 |               cwd=repo,
    |
help: Did you forget a comma?
help: Wrap implicitly concatenated strings in parentheses

RUF059 Unpacked variable `home` is never used
   --> tests/unit/test_runtime_health.py:462:15
    |
461 |     def test_linux_crit_prefers_pinned_target_over_older_path_binary(self) -> None:
462 |         repo, home, env, checksum = self.crit_fixture("9.9.9")
    |               ^^^^
463 |         self.executable(
464 |             repo / "bin/crit",
    |
help: Prefix it with an underscore or any other dummy variable pattern

ISC004 Unparenthesized implicit string concatenation in collection
   --> tests/unit/test_runtime_health.py:471:17
    |
469 |                   "bash",
470 |                   "-c",
471 | /                 "source scripts/update-agent-assets.sh; "
472 | |                 "CRIT_PIN_VERSION=v9.9.9; "
473 | |                 f"CRIT_LINUX_AMD64_SHA256={checksum}; "
474 | |                 "ensure_crit_cli; crit --version",
    | |_________________________________________________^
475 |               ],
476 |               cwd=repo,
    |
help: Did you forget a comma?
help: Wrap implicitly concatenated strings in parentheses

ISC004 Unparenthesized implicit string concatenation in collection
   --> tests/unit/test_runtime_health.py:493:17
    |
491 |                   "bash",
492 |                   "-c",
493 | /                 "source scripts/update-agent-assets.sh; "
494 | |                 "CRIT_PIN_VERSION=v9.9.9; "
495 | |                 f"CRIT_LINUX_AMD64_SHA256={'0' * 64}; "
496 | |                 "ensure_crit_cli",
    | |_________________________________^
497 |               ],
498 |               cwd=repo,
    |
help: Did you forget a comma?
help: Wrap implicitly concatenated strings in parentheses

ISC004 Unparenthesized implicit string concatenation in collection
   --> tests/unit/test_runtime_health.py:511:17
    |
509 |                   "bash",
510 |                   "-c",
511 | /                 "source scripts/update-agent-assets.sh; "
512 | |                 "CRIT_PIN_VERSION=v9.9.9; "
513 | |                 f"CRIT_LINUX_AMD64_SHA256={'0' * 64}; "
514 | |                 "ensure_crit_cli || :; "
515 | |                 "later_function() { :; }; later_function",
    | |_________________________________________________________^
516 |               ],
517 |               cwd=repo,
    |
help: Did you forget a comma?
help: Wrap implicitly concatenated strings in parentheses

ISC004 Unparenthesized implicit string concatenation in collection
   --> tests/unit/test_runtime_health.py:530:17
    |
528 |                   "bash",
529 |                   "-c",
530 | /                 "source scripts/update-agent-assets.sh; "
531 | |                 "CRIT_PIN_VERSION=v9.9.9; "
532 | |                 f"CRIT_DARWIN_ARM64_SHA256={checksum}; "
533 | |                 "ensure_crit_cli",
    | |_________________________________^
534 |               ],
535 |               cwd=repo,
    |
help: Did you forget a comma?
help: Wrap implicitly concatenated strings in parentheses

ISC004 Unparenthesized implicit string concatenation in collection
   --> tests/unit/test_runtime_health.py:559:17
    |
557 |                   "bash",
558 |                   "-c",
559 | /                 "source scripts/update-agent-assets.sh; "
560 | |                 "CRIT_PIN_VERSION=v9.9.9; "
561 | |                 f"CRIT_DARWIN_ARM64_SHA256={'0' * 64}; "
562 | |                 "ensure_crit_cli",
    | |_________________________________^
563 |               ],
564 |               cwd=repo,
    |
help: Did you forget a comma?
help: Wrap implicitly concatenated strings in parentheses

ISC004 Unparenthesized implicit string concatenation in collection
   --> tests/unit/test_runtime_health.py:699:17
    |
697 |                   "bash",
698 |                   "-c",
699 | /                 "source scripts/update-agent-assets.sh; "
700 | |                 f"AGMSG_PIN_SHA256={checksum}; "
701 | |                 "AGMSG_PIN_VERSION=9.9.9; "
702 | |                 "update_agmsg",
    | |______________________________^
703 |               ],
704 |               cwd=repo,
    |
help: Did you forget a comma?
help: Wrap implicitly concatenated strings in parentheses

RUF059 Unpacked variable `home` is never used
   --> tests/unit/test_runtime_health.py:720:15
    |
719 |     def test_agmsg_already_pinned_skips_download(self) -> None:
720 |         repo, home, env, checksum = self.agmsg_fixture(preinstalled_version="1.4.2")
    |               ^^^^
721 |         result = self.run_test_command(
722 |             [
    |
help: Prefix it with an underscore or any other dummy variable pattern

ISC004 Unparenthesized implicit string concatenation in collection
   --> tests/unit/test_runtime_health.py:725:17
    |
723 |                   "bash",
724 |                   "-c",
725 | /                 "source scripts/update-agent-assets.sh; "
726 | |                 f"AGMSG_PIN_SHA256={checksum}; "
727 | |                 "AGMSG_PIN_VERSION=1.4.2; "
728 | |                 "update_agmsg",
    | |______________________________^
729 |               ],
730 |               cwd=repo,
    |
help: Did you forget a comma?
help: Wrap implicitly concatenated strings in parentheses

ISC004 Unparenthesized implicit string concatenation in collection
   --> tests/unit/test_runtime_health.py:765:17
    |
763 |                   "bash",
764 |                   "-c",
765 | /                 "source scripts/update-agent-assets.sh; "
766 | |                 f"AGMSG_PIN_SHA256={checksum}; "
767 | |                 "AGMSG_PIN_VERSION=9.9.9; "
768 | |                 "update_agmsg",
    | |______________________________^
769 |               ],
770 |               cwd=repo,
    |
help: Did you forget a comma?
help: Wrap implicitly concatenated strings in parentheses

ISC004 Unparenthesized implicit string concatenation in collection
   --> tests/unit/test_runtime_health.py:792:17
    |
790 |                   "bash",
791 |                   "-c",
792 | /                 "source scripts/update-agent-assets.sh; "
793 | |                 f"AGMSG_PIN_SHA256={checksum}; "
794 | |                 "AGMSG_PIN_VERSION=9.9.9; "
795 | |                 "update_agmsg",
    | |______________________________^
796 |               ],
797 |               cwd=repo,
    |
help: Did you forget a comma?
help: Wrap implicitly concatenated strings in parentheses

ISC004 Unparenthesized implicit string concatenation in collection
   --> tests/unit/test_runtime_health.py:825:17
    |
823 |                   "bash",
824 |                   "-c",
825 | /                 "source scripts/update-agent-assets.sh; "
826 | |                 f"AGMSG_PIN_SHA256={checksum}; "
827 | |                 "AGMSG_PIN_VERSION=9.9.9; "
828 | |                 "update_agmsg",
    | |______________________________^
829 |               ],
830 |               cwd=repo,
    |
help: Did you forget a comma?
help: Wrap implicitly concatenated strings in parentheses

ISC004 Unparenthesized implicit string concatenation in collection
   --> tests/unit/test_runtime_health.py:857:17
    |
855 |                   "bash",
856 |                   "-c",
857 | /                 "source scripts/update-agent-assets.sh; "
858 | |                 f"AGMSG_PIN_SHA256={checksum}; "
859 | |                 "AGMSG_PIN_VERSION=9.9.9; "
860 | |                 "update_agmsg",
    | |______________________________^
861 |               ],
862 |               cwd=repo,
    |
help: Did you forget a comma?
help: Wrap implicitly concatenated strings in parentheses

ISC004 Unparenthesized implicit string concatenation in collection
   --> tests/unit/test_runtime_health.py:893:17
    |
891 |                   "bash",
892 |                   "-c",
893 | /                 "source scripts/update-agent-assets.sh; "
894 | |                 f"AGMSG_PIN_SHA256={checksum}; "
895 | |                 "AGMSG_PIN_VERSION=9.9.9; "
896 | |                 "update_agmsg",
    | |______________________________^
897 |               ],
898 |               cwd=repo,
    |
help: Did you forget a comma?
help: Wrap implicitly concatenated strings in parentheses

RUF059 Unpacked variable `home` is never used
   --> tests/unit/test_runtime_health.py:909:15
    |
908 |     def test_agmsg_reports_an_installer_that_leaves_the_wrong_version(self) -> None:
909 |         repo, home, env, checksum = self.agmsg_fixture()
    |               ^^^^
910 |
911 |         result = self.run_test_command(
    |
help: Prefix it with an underscore or any other dummy variable pattern

ISC004 Unparenthesized implicit string concatenation in collection
   --> tests/unit/test_runtime_health.py:942:17
    |
940 |                   "bash",
941 |                   "-c",
942 | /                 "source scripts/update-agent-assets.sh; "
943 | |                 f"AGMSG_PIN_SHA256={checksum}; "
944 | |                 "AGMSG_PIN_VERSION=9.9.9; "
945 | |                 "update_agmsg",
    | |______________________________^
946 |               ],
947 |               cwd=repo,
    |
help: Did you forget a comma?
help: Wrap implicitly concatenated strings in parentheses

Found 60 errors.
[*] 6 fixable with the `--fix` option (47 hidden fixes can be enabled with the `--unsafe-fixes` option).
```

## python3 /tmp/t90-handoff-verify.py; exit 0

```text
PASS: installed agmsg terminal_spawn -> exported adapter -> fake Herdr -> boot process; custom path preserved and token overrides removed.
PASS: real gh auth setup-git + git credential fill select the fixture in GH_CONFIG_DIR for both roles; output captured, no real credentials or network used.
```

## make require-crit-review; expected exit 2 before receipt

```text
Native agent review required before completion.
- review-sensitive path changed: .orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-worker-crit.json
- broad diff touches 25 files
- broad diff changes 7718 lines
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
make: *** [Makefile:179: require-crit-review] Error 1
```

## AGENT_REVIEWED=1 REVIEW_EVIDENCE=<T90 receipt> make require-crit-review; exit 0

```text
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.
```

## git push origin feat/github-identity-separation; exit 0

```text
remote: 
remote: Create a pull request for 'feat/github-identity-separation' on GitHub by visiting:        
remote:      https://github.com/mryfmo/dotfiles/pull/new/feat/github-identity-separation        
remote: 
To github.com:mryfmo/dotfiles.git
 * [new branch]        feat/github-identity-separation -> feat/github-identity-separation
```

## gh pr create --base main --head feat/github-identity-separation --title <English title> --body-file /tmp/t90-pr-body.md; exit 0

```text
https://github.com/mryfmo/dotfiles/pull/262
```

## gh pr update-branch 262; exit 0

```text
✓ PR branch updated
```

## git diff origin/main --stat; exit 0

```text
 README.md                                          |  76 ++++++++++++++-
 home/dot_agents/agent-config.yaml                  |   2 +
 home/dot_agents/model-profiles.env                 |   1 +
 .../dot_agents/skills/agmsg-orchestration/SKILL.md |   2 +-
 home/dot_config/claude/rules/pr-integration.md     |   2 +
 home/dot_local/bin/common/executable_herdr-agents  |  60 +++++++++++-
 scripts/check-tools.sh                             |  65 +++++++++++++
 scripts/generate-agent-configs.py                  |   6 +-
 scripts/require-crit-review.py                     |  80 ++++++++++++++++
 tests/unit/test_generate_agent_configs.py          |  19 ++++
 tests/unit/test_herdr_agents.py                    | 103 ++++++++++++++++++---
 tests/unit/test_require_crit_review.py             |  70 ++++++++++++++
 tests/unit/test_runtime_health.py                  |  58 +++++++++++-
 13 files changed, 524 insertions(+), 20 deletions(-)
```

## Additional verbatim command outputs

`uv run python scripts/generate-agent-configs.py` initially omitted its isolated PyYAML dependency; corrected to the Makefile's --with pyyaml invocation:

```text
ERROR: PyYAML is required: uv run --with pyyaml scripts/generate-agent-configs.py
```

`mise x ruff -- ruff format --config ruff.toml --check <six changed Python files>` (exit 0):

```text
6 files already formatted
```

`git commit -m 'feat(agents): separate worker GitHub identities and gate approval'` (exit 0):

```text
[feat/github-identity-separation a8151c9a] feat(agents): separate worker GitHub identities and gate approval
 13 files changed, 524 insertions(+), 20 deletions(-)
```

`git rev-parse HEAD` after update-branch and fast-forward:

```text
3c0cc58bb32bc447c55faca0d4ac41857937bc71
```

## VERIFY sources and bounds

- gh environment precedence and GH_CONFIG_DIR: https://cli.github.com/manual/gh_help_environment
- File storage and --insecure-storage: https://cli.github.com/manual/gh_auth_login
- HTTPS credential helper: https://cli.github.com/manual/gh_auth_setup-git . Real CLI fixture verification above routes two temporary configs independently; SSH is separate.
- Required reviews and author self-approval restriction: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets and https://docs.github.com/en/pull-requests/how-tos/review-pull-requests/approving-a-pull-request-with-required-reviews
- Effective active branch rules endpoint: https://docs.github.com/en/rest/repos/rules?apiVersion=2022-11-28#get-rules-for-a-branch
- Reviews can be created pending and submitted later: https://docs.github.com/en/rest/pulls/reviews?apiVersion=2022-11-28 . Gate uses submitted_at, not ID order alone.
- Codex shell policy supported set override: https://learn.chatgpt.com/docs/config-file/config-advanced#shell-environment-policy . additional_include is not a documented key; include-only filters cannot restore variables dropped from core.
- No live second account login or ruleset PUT was performed. Scratch PR pre-approval merge refusal (expected 405) is operator follow-up, not an observed result. One required review cannot prevent an author merge after independent approval.
- Upstream driver validation sourced installed ops.sh terminal_spawn; substituted only Herdr transport and readiness/socket probes, then executed the actual boot prefix in a shell with an overriding GH_CONFIG_DIR/GH_TOKEN fixture. No real pane creation.

## uv run python -m unittest tests.unit.test_herdr_agents tests.unit.test_generate_agent_configs tests.unit.test_require_crit_review; exit 0

```text
................................................................................................................................................................................................................................<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf8d4c4c32110>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf8d4c4c32200>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf8d4c4c324d0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf8d4c4c322f0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf8d4c4c325c0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf8d4c4c323e0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf8d4c4c326b0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf8d4c4c327a0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf8d4c4c32890>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf8d4c4c32980>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf8d4c4c32b60>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf8d4c4c32a70>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf8d4c4c32d40>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf8d4c454e020>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf8d4c4c30a90>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf8d4c4c32e30>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf8d4c4c32f20>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf8d4c4c33010>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf8d4c4c33100>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf8d4c4c331f0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf8d4c4c333d0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf8d4c4c334c0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf8d4c4c336a0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf8d4c4c33790>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf8d4c4c33970>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf8d4c4c33a60>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf8d4c4c33b50>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf8d4c4c33c40>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf8d4c4c33d30>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf8d4c4c33e20>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf8d4c4c33f10>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf8d4c4b80040>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf8d4c4b80220>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf8d4c4b80310>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf8d4c4b813f0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf8d4c4b815d0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf8d4c4b816c0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf8d4c4b818a0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf8d4c4b81990>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf8d4c4b81b70>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf8d4c4b81c60>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf8d4c4b81e40>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf8d4c4b81f30>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf8d4c4b82020>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
..........................ERROR: model profile standard is missing codex
ERROR: model profile standard.claude.model must be a launcher-safe string
ERROR: model_profiles must define the express profile
..ERROR: model profile standard.claude.advisor must be a launcher-safe string
................ERROR: interactive_profile must name a model profile: 'missing'
.ERROR: worker_kind must be one of ('codex', 'claude'): 'banana'
.ERROR: worker_profile must name a model profile: 'missing'
.ERROR: worker_gh_config_dir must be an absolute or ~/ path without control characters
ERROR: worker_gh_config_dir must be an absolute or ~/ path without control characters
ERROR: worker_gh_config_dir must be an absolute or ~/ path without control characters
ERROR: worker_gh_config_dir must be an absolute or ~/ path without control characters
..ERROR: worker_worktree must be a relative path under .claude/worktrees/: 'worker-c'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '/abs/.claude/worktrees/x'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/..'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/a/b'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/$(x)'
........................................................................
----------------------------------------------------------------------
Ran 345 tests in 162.325s

OK
```

## Live effective-rule API shape verification

Initial attempt combined --slurp and --jq and was rejected before an API request (exit 1):

```text
the `--slurp` option is not supported with `--jq` or `--template`
```

Corrected `gh api --paginate --slurp repos/mryfmo/dotfiles/rules/branches/main`, parsed JSON in Python and selected approval fields (read-only, exit 0):

```text
[
  {
    "type": "pull_request",
    "required_approving_review_count": 0,
    "dismiss_stale_reviews_on_push": true,
    "require_last_push_approval": false
  }
]
```

## Base update 2 and CI retry

`gh pr update-branch 262` (exit 0):

```text
✓ PR branch updated
```

`git rev-parse HEAD`:

```text
01ce1acc44b15620879b148a714e67dceaebedfd
```

Stable patch IDs for old-base diff and new-base diff are identical:

```text
44050f6b826c141f4471ffdc17893a0cef7a18ae 0000000000000000000000000000000000000000
44050f6b826c141f4471ffdc17893a0cef7a18ae 0000000000000000000000000000000000000000
```

`XDG_CACHE_HOME=/tmp/t90-gh-cache gh run view 37219825984 --log-failed` (exit 0; default ~/.cache/gh was read-only, so redirected cache):

```text
test (ubuntu-24.04, client)	Install tools	﻿2026-10-04T17:15:50.5294105Z ##[group]Run if [ "${OS}" == "macos-14" ]; then
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5294549Z ^[[36;1mif [ "${OS}" == "macos-14" ]; then^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5294967Z ^[[36;1m  # The macos-14 runner image ships third-party taps tapped but^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5295467Z ^[[36;1m  # untrusted, and Homebrew warns on every `brew install` while one^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5295948Z ^[[36;1m  # is present. The installs below come from homebrew/core, so^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5296429Z ^[[36;1m  # resolve those taps with the brew installer's own CI handling^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5296868Z ^[[36;1m  # rather than a second hard-coded copy of the tap list.^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5297360Z ^[[36;1m  bash -c 'source install/macos/common/brew.sh; handle_ci_untrusted_taps'^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5297765Z ^[[36;1m^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5298053Z ^[[36;1m  # `bashcov` on macOS must use Homebrew Bash (>=5) to avoid the^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5298540Z ^[[36;1m  # system Bash 3.2 parser limitations that produced empty coverage.^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5299046Z ^[[36;1m  # `gawk` is available for shell tooling used by the test suite.^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5299471Z ^[[36;1m  brew install bash bats-core gawk parallel shellcheck^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5299795Z ^[[36;1m^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5300003Z ^[[36;1melif [[ "${OS}" == ubuntu-* ]]; then^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5300359Z ^[[36;1m  # Ruby is required for bashcov/simplecov formatters.^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5300890Z ^[[36;1m  sudo apt-get update && sudo apt-get install -y bats curl iproute2 parallel ruby shellcheck^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5301359Z ^[[36;1m^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5301543Z ^[[36;1melse^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5301796Z ^[[36;1m  echo "${OS} and ${SYSTEM} are not supported" >&2^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5302430Z ^[[36;1m  exit 1^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5302636Z ^[[36;1mfi^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5302824Z ^[[36;1m^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5303306Z ^[[36;1m# `chezmoi` is installed so Bats can render chezmoi templates^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5303796Z ^[[36;1m# behaviorally instead of grepping template syntax. Both platforms^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5323182Z ^[[36;1m# take the pinned release that setup.sh bootstraps; the version^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5324030Z ^[[36;1m# renders from assets.chezmoi-bootstrap in agent-config.yaml.^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5324751Z ^[[36;1msource scripts/lib/installer-pins.sh^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5325303Z ^[[36;1mcase "$(uname -s)/$(uname -m)" in^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5325898Z ^[[36;1m  Darwin/arm64) chezmoi_platform=darwin_arm64 ;;^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5326549Z ^[[36;1m  Darwin/x86_64) chezmoi_platform=darwin_amd64 ;;^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5327206Z ^[[36;1m  Linux/x86_64) chezmoi_platform=linux_amd64 ;;^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5327990Z ^[[36;1m  *) echo "no chezmoi release for $(uname -s)/$(uname -m)" >&2; exit 1 ;;^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5328676Z ^[[36;1mesac^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5329310Z ^[[36;1martifact="chezmoi_${CHEZMOI_BOOTSTRAP_PIN_VERSION}_${chezmoi_platform}.tar.gz"^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5330539Z ^[[36;1mbase_url="https://github.com/twpayne/chezmoi/releases/download/v${CHEZMOI_BOOTSTRAP_PIN_VERSION}"^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5331532Z ^[[36;1msha256_check=(sha256sum --check --strict)^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5332618Z ^[[36;1mcommand -v sha256sum >/dev/null || sha256_check=(shasum -a 256 --check --strict)^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5333591Z ^[[36;1mcurl -fsSL "${base_url}/${artifact}" -o "${RUNNER_TEMP}/${artifact}"^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5334574Z ^[[36;1mcurl -fsSL "${base_url}/chezmoi_${CHEZMOI_BOOTSTRAP_PIN_VERSION}_checksums.txt" \^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5335382Z ^[[36;1m  | grep "  ${artifact}$" \^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5335940Z ^[[36;1m  | (cd "${RUNNER_TEMP}" && "${sha256_check[@]}")^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5336650Z ^[[36;1mtar -xzf "${RUNNER_TEMP}/${artifact}" -C "${RUNNER_TEMP}" chezmoi^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5337323Z ^[[36;1msudo install -m 0755 "${RUNNER_TEMP}/chezmoi" /usr/local/bin/chezmoi^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5337775Z ^[[36;1m^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5338030Z ^[[36;1mfiles_test_chezmoi="$(command -v chezmoi)"^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5338346Z ^[[36;1mcase "${files_test_chezmoi}" in^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5338866Z ^[[36;1m  /*/mise/shims/*|"")^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5339301Z ^[[36;1m    echo "Files test chezmoi must resolve outside mise shims: ${files_test_chezmoi:-missing}" >&2^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5339771Z ^[[36;1m    exit 1^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5339974Z ^[[36;1m    ;;^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5340164Z ^[[36;1m  /*) ;;^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5340359Z ^[[36;1m  *)^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5340695Z ^[[36;1m    echo "Files test chezmoi must be an absolute path: ${files_test_chezmoi}" >&2^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5341105Z ^[[36;1m    exit 1^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5341312Z ^[[36;1m    ;;^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5341502Z ^[[36;1mesac^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5341712Z ^[[36;1mtest -x "${files_test_chezmoi}"^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5342423Z ^[[36;1m# A runner-provided chezmoi earlier on PATH must not shadow the pin.^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5343003Z ^[[36;1m"${files_test_chezmoi}" --version | grep -F "v${CHEZMOI_BOOTSTRAP_PIN_VERSION}"^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5343554Z ^[[36;1mprintf 'FILES_TEST_CHEZMOI=%s\n' "${files_test_chezmoi}" >> "${GITHUB_ENV}"^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5343947Z ^[[36;1m^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5344256Z ^[[36;1m# Install coverage tooling as user gems and expose gem bin dir on PATH^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5344766Z ^[[36;1m# before installation so RubyGems can expose executables immediately.^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5345208Z ^[[36;1m# `--no-document` keeps CI faster and deterministic.^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5345633Z ^[[36;1mgem_bin_dir="$(ruby -r rubygems -e 'puts Gem.user_dir')/bin"^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5346020Z ^[[36;1mecho "${gem_bin_dir}" >> "${GITHUB_PATH}"^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5346335Z ^[[36;1mexport PATH="${gem_bin_dir}:${PATH}"^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5346722Z ^[[36;1mgem install --user-install --no-document bashcov --version 3.3.0^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5347228Z ^[[36;1mgem install --user-install --no-document simplecov-cobertura --version 3.1.0^[[0m
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5409086Z shell: /usr/bin/bash -e {0}
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5409344Z env:
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5409552Z   OS: ubuntu-24.04
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5409765Z   SYSTEM: client
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5409981Z   CODECOV_FLAGS: ubuntu-24.04-client
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5410299Z   CODECOV_NAME: codecov-dotfiles-ubuntu-24.04-client
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5413263Z   GITHUB_TOKEN: ***
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.5413491Z ##[endgroup]
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.6235892Z Get:1 file:/etc/apt/apt-mirrors.txt Mirrorlist [144 B]
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.6471212Z Get:6 https://packages.microsoft.com/ubuntu/24.04/prod noble InRelease [3600 B]
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.6572542Z Hit:2 http://azure.archive.ubuntu.com/ubuntu noble InRelease
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.6585659Z Get:3 http://azure.archive.ubuntu.com/ubuntu noble-updates InRelease [126 kB]
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.6625067Z Get:4 http://azure.archive.ubuntu.com/ubuntu noble-backports InRelease [126 kB]
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.6650030Z Get:5 http://azure.archive.ubuntu.com/ubuntu noble-security InRelease [126 kB]
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.7283627Z Get:7 https://packages.microsoft.com/ubuntu/24.04/prod noble/main amd64 Packages [511 kB]
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.7439529Z Get:8 https://packages.microsoft.com/ubuntu/24.04/prod noble/main armhf Packages [12.6 kB]
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.7493229Z Get:9 https://packages.microsoft.com/ubuntu/24.04/prod noble/main arm64 Packages [458 kB]
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.8483533Z Get:10 http://azure.archive.ubuntu.com/ubuntu noble-updates/main amd64 Packages [1364 kB]
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.8542956Z Get:11 http://azure.archive.ubuntu.com/ubuntu noble-updates/main Translation-en [304 kB]
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.8554586Z Get:12 http://azure.archive.ubuntu.com/ubuntu noble-updates/main amd64 Components [181 kB]
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.8572833Z Get:13 http://azure.archive.ubuntu.com/ubuntu noble-updates/universe amd64 Packages [1699 kB]
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.8684805Z Get:14 http://azure.archive.ubuntu.com/ubuntu noble-updates/universe Translation-en [341 kB]
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.8708121Z Get:15 http://azure.archive.ubuntu.com/ubuntu noble-updates/universe amd64 Components [388 kB]
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.8734532Z Get:16 http://azure.archive.ubuntu.com/ubuntu noble-updates/restricted amd64 Packages [1720 kB]
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.8843075Z Get:17 http://azure.archive.ubuntu.com/ubuntu noble-updates/restricted Translation-en [394 kB]
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.8856944Z Get:18 http://azure.archive.ubuntu.com/ubuntu noble-updates/multiverse amd64 Components [940 B]
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.9163078Z Get:19 http://azure.archive.ubuntu.com/ubuntu noble-backports/main amd64 Components [5776 B]
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.9606864Z Get:20 http://azure.archive.ubuntu.com/ubuntu noble-backports/universe amd64 Components [12.6 kB]
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.9883653Z Get:21 http://azure.archive.ubuntu.com/ubuntu noble-security/main amd64 Packages [1069 kB]
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.9924097Z Get:22 http://azure.archive.ubuntu.com/ubuntu noble-security/main Translation-en [221 kB]
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.9942588Z Get:23 http://azure.archive.ubuntu.com/ubuntu noble-security/main amd64 Components [46.4 kB]
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:50.9956293Z Get:24 http://azure.archive.ubuntu.com/ubuntu noble-security/universe amd64 Packages [1216 kB]
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:51.0024556Z Get:25 http://azure.archive.ubuntu.com/ubuntu noble-security/universe Translation-en [244 kB]
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:51.0046854Z Get:26 http://azure.archive.ubuntu.com/ubuntu noble-security/universe amd64 Components [76.4 kB]
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:51.0060987Z Get:27 http://azure.archive.ubuntu.com/ubuntu noble-security/restricted amd64 Packages [1566 kB]
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:51.0154324Z Get:28 http://azure.archive.ubuntu.com/ubuntu noble-security/restricted Translation-en [361 kB]
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:55.2080480Z Fetched 12.6 MB in 1s (9233 kB/s)
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:56.0357454Z Reading package lists...
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:56.0665925Z Reading package lists...
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:56.2498870Z Building dependency tree...
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:56.2506602Z Reading state information...
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:56.4063622Z curl is already the newest version (8.5.0-2ubuntu10.15).
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:56.4065110Z iproute2 is already the newest version (6.1.0-1ubuntu6.4).
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:56.4065919Z parallel is already the newest version (20231122+ds-1).
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:56.4066763Z ruby is already the newest version (1:3.2~ubuntu1).
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:56.4067389Z ruby set to manually installed.
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:56.4067963Z shellcheck is already the newest version (0.9.0-1).
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:56.4068606Z The following NEW packages will be installed:
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:56.4070502Z   bats
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:56.4239828Z 0 upgraded, 1 newly installed, 0 to remove and 25 not upgraded.
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:56.4240536Z Need to get 45.5 kB of archives.
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:56.4241137Z After this operation, 166 kB of additional disk space will be used.
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:56.4242157Z Get:1 file:/etc/apt/apt-mirrors.txt Mirrorlist [144 B]
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:56.5462425Z Get:2 http://azure.archive.ubuntu.com/ubuntu noble/universe amd64 bats all 1.10.0-1 [45.5 kB]
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:56.8766975Z Fetched 45.5 kB in 0s (205 kB/s)
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:56.8987060Z Selecting previously unselected package bats.
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:56.9264382Z (Reading database ... 
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:56.9264872Z (Reading database ... 5%
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:56.9265227Z (Reading database ... 10%
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:56.9265511Z (Reading database ... 15%
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:56.9265789Z (Reading database ... 20%
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:56.9266057Z (Reading database ... 25%
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:56.9266330Z (Reading database ... 30%
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:56.9267187Z (Reading database ... 35%
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:56.9267476Z (Reading database ... 40%
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:56.9267871Z (Reading database ... 45%
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:56.9268238Z (Reading database ... 50%
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:56.9315229Z (Reading database ... 55%
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:57.0874618Z (Reading database ... 60%
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:57.2774494Z (Reading database ... 65%
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:57.4993738Z (Reading database ... 70%
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:57.7796926Z (Reading database ... 75%
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:57.9391723Z (Reading database ... 80%
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:58.1293179Z (Reading database ... 85%
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:58.3395330Z (Reading database ... 90%
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:58.5448830Z (Reading database ... 95%
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:58.5449367Z (Reading database ... 100%
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:58.5450707Z (Reading database ... 202296 files and directories currently installed.)
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:58.5491481Z Preparing to unpack .../archives/bats_1.10.0-1_all.deb ...
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:58.5527673Z Unpacking bats (1.10.0-1) ...
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:58.6058262Z Setting up bats (1.10.0-1) ...
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:58.6083042Z Processing triggers for man-db (2.12.0-4build2) ...
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:58.6104286Z Not building database; man-db/auto-update is not 'true'.
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:59.2281038Z 
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:59.2281680Z Running kernel seems to be up-to-date.
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:59.2282379Z 
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:59.2282527Z No services need to be restarted.
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:59.2282753Z 
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:59.2282900Z No containers need to be restarted.
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:59.2283167Z 
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:59.2283322Z No user sessions are running outdated binaries.
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:59.2283605Z 
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:15:59.2283860Z No VM guests are running outdated hypervisor (qemu) binaries on this host.
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:16:00.3136003Z curl: (22) The requested URL returned error: 500
test (ubuntu-24.04, client)	Install tools	2026-10-04T17:16:00.3169972Z ##[error]Process completed with exit code 22.
```

`gh run rerun 37219825984 --failed` exited 0 with no stdout; retry of upstream HTTP 500 during tools installation and fail-fast cancelled matrix jobs, no source change.

## Bot wait completed

```text
Diff head: a8151c9a65bc893aae4eed6ed0cce5c55732a51a
Wait started: 2026-10-04T17:05:45.131119+00:00
bot: none (15-minute bounded wait)
Wait finished: 2026-10-04T17:21:12.513475+00:00
```

Final paginated review and inline-comment endpoints (all heads):

```json
[[]]
[[]]
```

## Final local asset validation

`UV_CACHE_DIR=/tmp/t90-uv-cache make validate-agent-assets` exit 0 (captured with Python subprocess after a zsh wrapper used read-only variable `status`; wrapper corrected, no repository code impact):

```text
uv run --with pyyaml scripts/validate-agent-assets.py
agent asset validation ok
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/acceptance/dotfiles-T69-protocol-docs-unification-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/acceptance/dotfiles-T72-bootstrap-ci-pins-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/acceptance/dotfiles-T76-ineffective-settings-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/acceptance/dotfiles-T77-harness-dead-code-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/acceptance/dotfiles-T78-dead-docs-adh-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/acceptance/dotfiles-T96-codex-worker-gpt61-sol-high-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/acceptance/dotfiles-T97-claude-sandbox-github-calls-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/autoskill/runs/dotfiles-T72-bootstrap-ci-pins-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/autoskill/runs/dotfiles-T76-ineffective-settings-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/autoskill/runs/dotfiles-T77-harness-dead-code-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/autoskill/runs/dotfiles-T78-dead-docs-adh-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/autoskill/runs/dotfiles-T96-codex-worker-gpt61-sol-high-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/autoskill/runs/dotfiles-T97-claude-sandbox-github-calls-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/learning/dotfiles-T72-bootstrap-ci-pins-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/learning/dotfiles-T76-ineffective-settings-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/learning/dotfiles-T77-harness-dead-code-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/learning/dotfiles-T78-dead-docs-adh-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/learning/dotfiles-T96-codex-worker-gpt61-sol-high-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/learning/dotfiles-T97-claude-sandbox-github-calls-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/reports/dotfiles-T72-bootstrap-ci-pins-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/reports/dotfiles-T76-ineffective-settings-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/reports/dotfiles-T77-harness-dead-code-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/reports/dotfiles-T78-dead-docs-adh-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/reports/dotfiles-T96-codex-worker-gpt61-sol-high-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/reports/dotfiles-T97-claude-sandbox-github-calls-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/sandboxes/dotfiles-T72-bootstrap-ci-pins-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/sandboxes/dotfiles-T76-ineffective-settings-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/sandboxes/dotfiles-T77-harness-dead-code-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/sandboxes/dotfiles-T78-dead-docs-adh-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/sandboxes/dotfiles-T96-codex-worker-gpt61-sol-high-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/sandboxes/dotfiles-T97-claude-sandbox-github-calls-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/tasks/dotfiles-T80-codex-command-hooks-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/tasks/dotfiles-T81-compactiondb-vendor-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/tasks/dotfiles-T97-claude-sandbox-github-calls-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T69-protocol-docs-unification-a01-audit-4656f19.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T69-protocol-docs-unification-a01-audit-4656f19.md.last.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T69-protocol-docs-unification-a01-audit-6b060ac.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T69-protocol-docs-unification-a01-audit-6b060ac.md.last.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T69-protocol-docs-unification-a01-audit-d9bbd80.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T69-protocol-docs-unification-a01-audit-d9bbd80.md.last.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T72-bootstrap-ci-pins-a01-audit-d5856e2.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T72-bootstrap-ci-pins-a01-audit-d5856e2.md.last.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T72-bootstrap-ci-pins-a01-crit.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T72-bootstrap-ci-pins-a01-pr-feedback.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T72-bootstrap-ci-pins-a01-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T72-bootstrap-ci-pins-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T76-ineffective-settings-a01-audit-26a882a.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T76-ineffective-settings-a01-audit-26a882a.md.last.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T76-ineffective-settings-a01-audit-f805ee3.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T76-ineffective-settings-a01-audit-f805ee3.md.last.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T76-ineffective-settings-a01-crit.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T76-ineffective-settings-a01-pr-feedback.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T76-ineffective-settings-a01-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T76-ineffective-settings-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T77-harness-dead-code-a01-audit-977bdf1.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T77-harness-dead-code-a01-audit-977bdf1.md.last.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T77-harness-dead-code-a01-crit.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T77-harness-dead-code-a01-pr-feedback.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T77-harness-dead-code-a01-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T77-harness-dead-code-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T78-dead-docs-adh-a01-audit-8d536a3.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T78-dead-docs-adh-a01-audit-8d536a3.md.last.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T78-dead-docs-adh-a01-crit.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T78-dead-docs-adh-a01-pr-feedback.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T78-dead-docs-adh-a01-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T78-dead-docs-adh-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T96-codex-worker-gpt61-sol-high-a01-audit-3a06011.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T96-codex-worker-gpt61-sol-high-a01-audit-3a06011.md.last.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T96-codex-worker-gpt61-sol-high-a01-crit.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T96-codex-worker-gpt61-sol-high-a01-pr-feedback.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T96-codex-worker-gpt61-sol-high-a01-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T96-codex-worker-gpt61-sol-high-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-audit-391d2b4.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-audit-391d2b4.md.last.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-audit-5b6b0d9.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-audit-5b6b0d9.md.last.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-audit-8ffa554.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-audit-8ffa554.md.last.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-audit-efe6735.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-audit-efe6735.md.last.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-crit.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-pr-feedback.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-worker-crit.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-worker-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/autoskill/runs/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/autoskill/runs/dotfiles-T97-claude-sandbox-github-calls-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/learning/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/learning/dotfiles-T97-claude-sandbox-github-calls-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/reports/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/reports/dotfiles-T97-claude-sandbox-github-calls-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/sandboxes/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/sandboxes/dotfiles-T97-claude-sandbox-github-calls-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/validation/dotfiles-T90-github-identity-separation-a01-worker-crit.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/validation/dotfiles-T90-github-identity-separation-a01-worker-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/validation/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-worker-crit.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-worker-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01.md
WARN: regime-boundary: additional worker workspace still open: dotfiles worker worker-d (herdr-agents --remove-worker)
WARN: regime-boundary: additional worker tab still open in dotfiles: dotfiles:codex-security-dot-a007 (herdr-agents --remove-worker)
```

## Base update 3 (orchestration-only boundary)

Main advanced to 8cd66881021c4bffe28d5a3d2ba75aba76e76665 (#263). `gh pr update-branch 262` (exit 0):

```text
✓ PR branch updated
```

Initial local fast-forward refused to overwrite untracked prior T97 artifacts (exit 1):

```text
error: The following untracked working tree files would be overwritten by merge:
	.orchestration/autoskill/runs/dotfiles-T97-claude-sandbox-github-calls-a01.md
	.orchestration/learning/dotfiles-T97-claude-sandbox-github-calls-a01.md
	.orchestration/reports/dotfiles-T97-claude-sandbox-github-calls-a01.md
	.orchestration/sandboxes/dotfiles-T97-claude-sandbox-github-calls-a01.md
	.orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-worker-crit.json
	.orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-worker-review-receipt.md
	.orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01.md
Please move or remove them before you merge.
Aborting
Updating 01ce1acc..b99a6f95
```

The seven original artifacts were moved intact to temporary backup before retrying; preserved paths and SHA256:

```text
.orchestration/reports/dotfiles-T97-claude-sandbox-github-calls-a01.md: sha256=13119d724e52474f7acee529ebcd48bf3b59a5ede2b4bad4dd7450e2fa1b21a0 backup=/tmp/t90-prior-t97-artifacts-rl8s53uu/.orchestration/reports/dotfiles-T97-claude-sandbox-github-calls-a01.md
.orchestration/sandboxes/dotfiles-T97-claude-sandbox-github-calls-a01.md: sha256=165b55b63d9527ecf292933dc7b2452e215606d0e55aed914f1cc1776796f69f backup=/tmp/t90-prior-t97-artifacts-rl8s53uu/.orchestration/sandboxes/dotfiles-T97-claude-sandbox-github-calls-a01.md
.orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01.md: sha256=2198b768bef043fc574ec2a84e1f6dc45c544c2470fbc9017752149f674550fe backup=/tmp/t90-prior-t97-artifacts-rl8s53uu/.orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01.md
.orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-worker-crit.json: sha256=60b1a9d9e2e3410ff9c140208dd6d48a27299c5e6e2f141033b90982fa8ea78e backup=/tmp/t90-prior-t97-artifacts-rl8s53uu/.orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-worker-crit.json
.orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-worker-review-receipt.md: sha256=77d360dc74dec8b92407a55db145cddca92975421f9f48c5b6ad20b69b482f92 backup=/tmp/t90-prior-t97-artifacts-rl8s53uu/.orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-worker-review-receipt.md
.orchestration/learning/dotfiles-T97-claude-sandbox-github-calls-a01.md: sha256=e96635d26004845a77e96295bb4a6bd39ffbb37ec27b6c4b26b83c4eacdfed01 backup=/tmp/t90-prior-t97-artifacts-rl8s53uu/.orchestration/learning/dotfiles-T97-claude-sandbox-github-calls-a01.md
.orchestration/autoskill/runs/dotfiles-T97-claude-sandbox-github-calls-a01.md: sha256=ebe08f77beb6c98c65711c53aa680d12833ac43d592eca103e542d992b237e8e backup=/tmp/t90-prior-t97-artifacts-rl8s53uu/.orchestration/autoskill/runs/dotfiles-T97-claude-sandbox-github-calls-a01.md
```

`git merge --ff-only --no-stat origin/feat/github-identity-separation` (exit 0):

```text
Updating 01ce1acc..b99a6f95
Fast-forward
```

`git rev-parse HEAD`; stable patch ID unchanged:

```text
b99a6f955e3f007ec97dc65c3a018f0aa9a2bfd0
44050f6b826c141f4471ffdc17893a0cef7a18ae 0000000000000000000000000000000000000000
```

## Final task revision verification

`sha256sum /home/moriya/Workspace/dotfiles/.orchestration/tasks/dotfiles-T90-github-identity-separation-a01.md`:

```text
11c63e79d25945792e9d8ec16539d28e64e05962e392bf630ab60c53c4f65e29  /home/moriya/Workspace/dotfiles/.orchestration/tasks/dotfiles-T90-github-identity-separation-a01.md
```

## Empty-XDG regression before fix (expected failure)

```text
F
======================================================================
FAIL: test_doctor_github_role_activation_and_file_storage (tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_github_role_activation_and_file_storage) (extra={'XDG_CONFIG_HOME': ''})
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py", line 1193, in test_doctor_github_role_activation_and_file_storage
    self.assertIn(f"failures={fails}", result.stdout)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'failures=0' not found in 'failures=1,warnings=0\n'

----------------------------------------------------------------------
Ran 1 test in 0.245s

FAILED (failures=1)
```

## uv run python -m unittest tests.unit.test_runtime_health; exit0

```text
...........................................
----------------------------------------------------------------------
Ran 43 tests in 8.950s

OK
```

## Review gate with updated independent-review receipt; exit0

```text
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.
```

## git commit -m fix(doctor): use default GitHub config for empty XDG home; exit0

```text
[feat/github-identity-separation 507e9c15] fix(doctor): use default GitHub config for empty XDG home
 2 files changed, 4 insertions(+), 1 deletion(-)
```

## git push origin feat/github-identity-separation; exit0

```text
To github.com:mryfmo/dotfiles.git
   b99a6f95..507e9c15  feat/github-identity-separation -> feat/github-identity-separation
```

`git rev-parse HEAD` after doctor correction:

```text
507e9c159d6ce73998ca70e79ac3951c04f81ff6
```

Empty-XDG native fallback confirmed by upstream: https://github.com/cli/go-gh/blob/trunk/pkg/config/config.go#L234-L246 . Initial RED failed only for empty XDG; corrected fallback and custom-XDG cases pass. Independent narrow review verdict correct.

## make unit-test on final 507e9c15; UV_CACHE_DIR=/tmp/t90-uv-cache; exit0

```text
uv run python -m unittest discover -s tests/unit -v
test_bounded_scan_finishes_under_wall_limit (test_agent_session_staleness.AgentSessionStalenessTest.test_bounded_scan_finishes_under_wall_limit) ... ok
test_check_is_silent_when_assets_predate_session (test_agent_session_staleness.AgentSessionStalenessTest.test_check_is_silent_when_assets_predate_session) ... ok
test_check_reports_new_versions_and_mtimes_deduplicated_by_root (test_agent_session_staleness.AgentSessionStalenessTest.test_check_reports_new_versions_and_mtimes_deduplicated_by_root) ... ok
test_doctor_delegates_session_staleness_to_installed_script (test_agent_session_staleness.AgentSessionStalenessTest.test_doctor_delegates_session_staleness_to_installed_script) ... ok
test_hook_first_call_writes_private_baseline_and_is_silent (test_agent_session_staleness.AgentSessionStalenessTest.test_hook_first_call_writes_private_baseline_and_is_silent) ... ok
test_hook_missing_or_garbage_stdin_is_silent_success (test_agent_session_staleness.AgentSessionStalenessTest.test_hook_missing_or_garbage_stdin_is_silent_success) ... ok
test_hook_prunes_state_files_older_than_seven_days (test_agent_session_staleness.AgentSessionStalenessTest.test_hook_prunes_state_files_older_than_seven_days) ... ok
test_hook_second_call_detects_asset_updated_after_baseline (test_agent_session_staleness.AgentSessionStalenessTest.test_hook_second_call_detects_asset_updated_after_baseline) ... ok
test_internal_failure_is_silent_success_with_one_stderr_line (test_agent_session_staleness.AgentSessionStalenessTest.test_internal_failure_is_silent_success_with_one_stderr_line) ... ok
test_no_arguments_prints_ten_recent_updates (test_agent_session_staleness.AgentSessionStalenessTest.test_no_arguments_prints_ten_recent_updates) ... ok
test_runtime_state_and_sqlite_files_are_excluded (test_agent_session_staleness.AgentSessionStalenessTest.test_runtime_state_and_sqlite_files_are_excluded) ... ok
test_ceiling_directories_do_not_hide_the_seat (test_agent_stop_gate.AgentStopGateTest.test_ceiling_directories_do_not_hide_the_seat) ... ok
test_character_device_placeholder_is_skipped (test_agent_stop_gate.AgentStopGateTest.test_character_device_placeholder_is_skipped) ... ok
test_checkout_outside_any_seat_passes (test_agent_stop_gate.AgentStopGateTest.test_checkout_outside_any_seat_passes) ... ok
test_clean_orchestrator_passes (test_agent_stop_gate.AgentStopGateTest.test_clean_orchestrator_passes) ... ok
test_every_team_of_the_identity_is_checked (test_agent_stop_gate.AgentStopGateTest.test_every_team_of_the_identity_is_checked) ... ok
test_failing_git_status_blocks (test_agent_stop_gate.AgentStopGateTest.test_failing_git_status_blocks) ... ok
test_failing_identity_lookup_blocks_once (test_agent_stop_gate.AgentStopGateTest.test_failing_identity_lookup_blocks_once) ... ok
test_inherited_alternate_index_does_not_hide_a_staged_change (test_agent_stop_gate.AgentStopGateTest.test_inherited_alternate_index_does_not_hide_a_staged_change) ... ok
test_inherited_git_dir_does_not_hide_the_seat (test_agent_stop_gate.AgentStopGateTest.test_inherited_git_dir_does_not_hide_the_seat) ... ok
test_injected_git_config_does_not_hide_untracked_files (test_agent_stop_gate.AgentStopGateTest.test_injected_git_config_does_not_hide_untracked_files) ... ok
test_json_escaped_cwd_resolves (test_agent_stop_gate.AgentStopGateTest.test_json_escaped_cwd_resolves) ... ok
test_missing_agmsg_install_passes (test_agent_stop_gate.AgentStopGateTest.test_missing_agmsg_install_passes) ... ok
test_mountinfo_cannot_be_redirected_through_the_environment (test_agent_stop_gate.AgentStopGateTest.test_mountinfo_cannot_be_redirected_through_the_environment) ... ok
test_null_device_of_another_filesystem_is_not_a_placeholder (test_agent_stop_gate.AgentStopGateTest.test_null_device_of_another_filesystem_is_not_a_placeholder) ... ok
test_orchestrator_acceptance_to_another_member_keeps_the_result_open (test_agent_stop_gate.AgentStopGateTest.test_orchestrator_acceptance_to_another_member_keeps_the_result_open) ... ok
test_project_dir_anchors_the_seat_after_a_cd (test_agent_stop_gate.AgentStopGateTest.test_project_dir_anchors_the_seat_after_a_cd) ... ok
test_read_only_bind_of_another_empty_file_is_not_a_placeholder (test_agent_stop_gate.AgentStopGateTest.test_read_only_bind_of_another_empty_file_is_not_a_placeholder) ... ok
test_read_write_mount_is_not_a_placeholder (test_agent_stop_gate.AgentStopGateTest.test_read_write_mount_is_not_a_placeholder) ... ok
test_result_then_acceptance_passes (test_agent_stop_gate.AgentStopGateTest.test_result_then_acceptance_passes) ... ok
test_result_then_revision_task_passes (test_agent_stop_gate.AgentStopGateTest.test_result_then_revision_task_passes) ... ok
test_result_without_acceptance_blocks (test_agent_stop_gate.AgentStopGateTest.test_result_without_acceptance_blocks) ... ok
test_same_named_file_bound_from_elsewhere_is_not_a_placeholder (test_agent_stop_gate.AgentStopGateTest.test_same_named_file_bound_from_elsewhere_is_not_a_placeholder) ... ok
test_sandbox_placeholders_are_skipped (test_agent_stop_gate.AgentStopGateTest.test_sandbox_placeholders_are_skipped) ... ok
test_sandbox_placeholders_on_a_separate_filesystem_are_skipped (test_agent_stop_gate.AgentStopGateTest.test_sandbox_placeholders_on_a_separate_filesystem_are_skipped) ... ok
test_separate_git_dir_main_worktree_is_a_seat (test_agent_stop_gate.AgentStopGateTest.test_separate_git_dir_main_worktree_is_a_seat) ... ok
test_slow_store_blocks_within_the_budget (test_agent_stop_gate.AgentStopGateTest.test_slow_store_blocks_within_the_budget) ... ok
test_slow_store_blocks_within_the_budget_with_gtimeout_only (test_agent_stop_gate.AgentStopGateTest.test_slow_store_blocks_within_the_budget_with_gtimeout_only) ... ok
test_slow_store_blocks_within_the_budget_without_timeout (test_agent_stop_gate.AgentStopGateTest.test_slow_store_blocks_within_the_budget_without_timeout) ... ok
test_solo_unsuffixed_worker_is_gated (test_agent_stop_gate.AgentStopGateTest.test_solo_unsuffixed_worker_is_gated) ... ok
test_sqlite_store_off_the_current_schema_is_not_initialized (test_agent_stop_gate.AgentStopGateTest.test_sqlite_store_off_the_current_schema_is_not_initialized) ... ok
test_staged_rename_out_of_orchestration_blocks (test_agent_stop_gate.AgentStopGateTest.test_staged_rename_out_of_orchestration_blocks) ... ok
test_stop_hook_active_skips_only_the_dirty_tree_check (test_agent_stop_gate.AgentStopGateTest.test_stop_hook_active_skips_only_the_dirty_tree_check) ... ok
test_unreadable_store_blocks_once (test_agent_stop_gate.AgentStopGateTest.test_unreadable_store_blocks_once) ... ok
test_untracked_file_outside_orchestration_blocks (test_agent_stop_gate.AgentStopGateTest.test_untracked_file_outside_orchestration_blocks) ... ok
test_untracked_symlink_to_a_mount_point_is_not_a_placeholder (test_agent_stop_gate.AgentStopGateTest.test_untracked_symlink_to_a_mount_point_is_not_a_placeholder) ... ok
test_untrusted_filenames_are_quoted (test_agent_stop_gate.AgentStopGateTest.test_untrusted_filenames_are_quoted) ... ok
test_user_bind_mount_of_a_real_file_is_not_a_placeholder (test_agent_stop_gate.AgentStopGateTest.test_user_bind_mount_of_a_real_file_is_not_a_placeholder) ... ok
test_whole_filesystem_bind_is_not_a_placeholder (test_agent_stop_gate.AgentStopGateTest.test_whole_filesystem_bind_is_not_a_placeholder) ... ok
test_worker_after_result_passes (test_agent_stop_gate.AgentStopGateTest.test_worker_after_result_passes) ... ok
test_worker_alive_pong_keeps_the_task_open (test_agent_stop_gate.AgentStopGateTest.test_worker_alive_pong_keeps_the_task_open) ... ok
test_worker_blocked_pong_closes_the_task (test_agent_stop_gate.AgentStopGateTest.test_worker_blocked_pong_closes_the_task) ... ok
test_worker_result_to_another_member_keeps_the_task_open (test_agent_stop_gate.AgentStopGateTest.test_worker_result_to_another_member_keeps_the_task_open) ... ok
test_worker_revise_acceptance_reopens_the_task (test_agent_stop_gate.AgentStopGateTest.test_worker_revise_acceptance_reopens_the_task) ... ok
test_worker_task_closed_by_a_non_revise_acceptance (test_agent_stop_gate.AgentStopGateTest.test_worker_task_closed_by_a_non_revise_acceptance) ... ok
test_worker_task_newer_than_result_blocks (test_agent_stop_gate.AgentStopGateTest.test_worker_task_newer_than_result_blocks) ... ok
test_worker_tracks_each_task_id (test_agent_stop_gate.AgentStopGateTest.test_worker_tracks_each_task_id) ... ok
test_default_store_uses_shared_helper (test_agmsg_dispatch.AgmsgDispatchTest.test_default_store_uses_shared_helper) ... ok
test_idle_wakes_once_and_reads (test_agmsg_dispatch.AgmsgDispatchTest.test_idle_wakes_once_and_reads) ... ok
test_invalid_timeout_does_not_send (test_agmsg_dispatch.AgmsgDispatchTest.test_invalid_timeout_does_not_send) ... ok
test_missing_pane_inserts_nothing (test_agmsg_dispatch.AgmsgDispatchTest.test_missing_pane_inserts_nothing) ... ok
test_rejects_identifiers_outside_the_strict_grammar (test_agmsg_dispatch.AgmsgDispatchTest.test_rejects_identifiers_outside_the_strict_grammar) ... ok
test_retry_does_not_wake_newly_working_pane (test_agmsg_dispatch.AgmsgDispatchTest.test_retry_does_not_wake_newly_working_pane) ... ok
test_timeout_is_one_shared_budget (test_agmsg_dispatch.AgmsgDispatchTest.test_timeout_is_one_shared_budget) ... ok
test_unread_retries_once_then_fails (test_agmsg_dispatch.AgmsgDispatchTest.test_unread_retries_once_then_fails) ... /home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:552: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8f19fc40>
  def _push_exit_callback(self, callback, is_sync=True):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:552: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8f19fb50>
  def _push_exit_callback(self, callback, is_sync=True):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:552: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8ed04d60>
  def _push_exit_callback(self, callback, is_sync=True):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:552: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8ed04f40>
  def _push_exit_callback(self, callback, is_sync=True):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:552: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8ed05030>
  def _push_exit_callback(self, callback, is_sync=True):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:552: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8ed05120>
  def _push_exit_callback(self, callback, is_sync=True):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:552: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8ed05210>
  def _push_exit_callback(self, callback, is_sync=True):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:552: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8ed05300>
  def _push_exit_callback(self, callback, is_sync=True):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:552: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8ed053f0>
  def _push_exit_callback(self, callback, is_sync=True):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:552: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8ed054e0>
  def _push_exit_callback(self, callback, is_sync=True):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:552: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8ed055d0>
  def _push_exit_callback(self, callback, is_sync=True):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:552: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8ed056c0>
  def _push_exit_callback(self, callback, is_sync=True):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:552: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8ed057b0>
  def _push_exit_callback(self, callback, is_sync=True):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:552: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8ed058a0>
  def _push_exit_callback(self, callback, is_sync=True):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:552: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8ed05990>
  def _push_exit_callback(self, callback, is_sync=True):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
ok
test_wake_failure_identifies_sent_message (test_agmsg_dispatch.AgmsgDispatchTest.test_wake_failure_identifies_sent_message) ... ok
test_worker_becoming_idle_after_send_is_woken (test_agmsg_dispatch.AgmsgDispatchTest.test_worker_becoming_idle_after_send_is_woken) ... ok
test_working_does_not_wake (test_agmsg_dispatch.AgmsgDispatchTest.test_working_does_not_wake) ... ok
test_working_unread_never_wakes (test_agmsg_dispatch.AgmsgDispatchTest.test_working_unread_never_wakes) ... ok
test_docs_no_longer_name_codex_review_commit (test_agmsg_orchestration_docs.AgmsgOrchestrationDocsParityTest.test_docs_no_longer_name_codex_review_commit) ... ok
test_rule_and_skill_share_the_audit_gate_and_bot_wait_invariants (test_agmsg_orchestration_docs.AgmsgOrchestrationDocsParityTest.test_rule_and_skill_share_the_audit_gate_and_bot_wait_invariants) ... ok
test_rule_and_skill_share_the_parallel_execution_and_routing_invariants (test_agmsg_orchestration_docs.AgmsgOrchestrationDocsParityTest.test_rule_and_skill_share_the_parallel_execution_and_routing_invariants) ... ok
test_rule_and_skill_share_the_registration_and_delivery_invariants (test_agmsg_orchestration_docs.AgmsgOrchestrationDocsParityTest.test_rule_and_skill_share_the_registration_and_delivery_invariants) ... ok
test_rule_drops_the_worker_network_escalation (test_agmsg_orchestration_docs.AgmsgOrchestrationDocsParityTest.test_rule_drops_the_worker_network_escalation) ... ok
test_skill_drops_the_pane_status_gate_and_raw_pane_wakes (test_agmsg_orchestration_docs.AgmsgOrchestrationDocsParityTest.test_skill_drops_the_pane_status_gate_and_raw_pane_wakes) ... ok
test_doctor_fails_when_bwrap_is_missing_with_codex (test_apparmor_userns.AppArmorUsernsTest.test_doctor_fails_when_bwrap_is_missing_with_codex) ... ok
test_doctor_fails_when_the_bwrap_probe_fails (test_apparmor_userns.AppArmorUsernsTest.test_doctor_fails_when_the_bwrap_probe_fails) ... ok
test_doctor_is_not_applicable_without_the_restriction (test_apparmor_userns.AppArmorUsernsTest.test_doctor_is_not_applicable_without_the_restriction) ... ok
test_doctor_passes_when_the_bwrap_probe_succeeds (test_apparmor_userns.AppArmorUsernsTest.test_doctor_passes_when_the_bwrap_probe_succeeds) ... ok
test_doctor_warns_optionally_when_codex_is_missing (test_apparmor_userns.AppArmorUsernsTest.test_doctor_warns_optionally_when_codex_is_missing) ... ok
test_installer_copies_and_reloads_the_profile_with_sudo (test_apparmor_userns.AppArmorUsernsTest.test_installer_copies_and_reloads_the_profile_with_sudo) ... ok
test_installer_fails_when_loading_the_profile_fails (test_apparmor_userns.AppArmorUsernsTest.test_installer_fails_when_loading_the_profile_fails) ... ok
test_installer_is_a_no_op_when_the_host_does_not_need_the_profile (test_apparmor_userns.AppArmorUsernsTest.test_installer_is_a_no_op_when_the_host_does_not_need_the_profile) ... ok
test_installer_leaves_the_profile_pending_without_cached_sudo (test_apparmor_userns.AppArmorUsernsTest.test_installer_leaves_the_profile_pending_without_cached_sudo) ... ok
test_wrapper_re_renders_when_prerequisites_change (test_apparmor_userns.AppArmorUsernsTest.test_wrapper_re_renders_when_prerequisites_change) ... ok
test_chezmoi_rendered_updater_uses_exported_source_root (test_asset_manifest.AssetManifestTest.test_chezmoi_rendered_updater_uses_exported_source_root) ... ok
test_chezmoi_rendered_updater_uses_inlined_manifest_library (test_asset_manifest.AssetManifestTest.test_chezmoi_rendered_updater_uses_inlined_manifest_library) ... ok
test_chezmoi_wrapper_renders_shebang_and_source_root (test_asset_manifest.AssetManifestTest.test_chezmoi_wrapper_renders_shebang_and_source_root) ... ok
test_failed_atomic_commit_leaves_previous_manifest_intact (test_asset_manifest.AssetManifestTest.test_failed_atomic_commit_leaves_previous_manifest_intact) ... ok
test_records_schema_two_steps_and_replaces_one_whole_entry (test_asset_manifest.AssetManifestTest.test_records_schema_two_steps_and_replaces_one_whole_entry) ... ok
test_rendered_updater_fails_when_no_source_root_is_valid (test_asset_manifest.AssetManifestTest.test_rendered_updater_fails_when_no_source_root_is_valid) ... ok
test_same_run_mise_repairs_preserve_both_identity_steps (test_asset_manifest.AssetManifestTest.test_same_run_mise_repairs_preserve_both_identity_steps) ... ok
test_two_real_install_steps_record_under_fake_home (test_asset_manifest.AssetManifestTest.test_two_real_install_steps_record_under_fake_home) ... ok
test_unwritable_destination_warns_once_without_failing (test_asset_manifest.AssetManifestTest.test_unwritable_destination_warns_once_without_failing) ... ok
test_updater_direct_source_resolves_repository_root (test_asset_manifest.AssetManifestTest.test_updater_direct_source_resolves_repository_root) ... ok
test_updater_has_one_recording_call_for_each_install_step (test_asset_manifest.AssetManifestTest.test_updater_has_one_recording_call_for_each_install_step) ... ok
test_exit_zero_install_with_expected_fake_binary_passes_postcondition (test_aws_cli_acquisition.AwsCliAcquisitionTest.test_exit_zero_install_with_expected_fake_binary_passes_postcondition) ... ok
test_exit_zero_install_with_wrong_version_fails_postcondition (test_aws_cli_acquisition.AwsCliAcquisitionTest.test_exit_zero_install_with_wrong_version_fails_postcondition) ... ok
test_exit_zero_partial_install_without_binary_fails_postcondition (test_aws_cli_acquisition.AwsCliAcquisitionTest.test_exit_zero_partial_install_without_binary_fails_postcondition) ... ok
test_gpgv_failure_preserves_existing_aws_and_skips_unzip (test_aws_cli_acquisition.AwsCliAcquisitionTest.test_gpgv_failure_preserves_existing_aws_and_skips_unzip) ... ok
test_key_metadata_failures_stop_before_dearmor_and_gpgv (test_aws_cli_acquisition.AwsCliAcquisitionTest.test_key_metadata_failures_stop_before_dearmor_and_gpgv) ... ok
test_linux_urls_are_versioned_and_unknown_architecture_fails (test_aws_cli_acquisition.AwsCliAcquisitionTest.test_linux_urls_are_versioned_and_unknown_architecture_fails) ... ok
test_platform_package_managers_and_wrapper_own_aws_cli (test_aws_cli_acquisition.AwsCliAcquisitionTest.test_platform_package_managers_and_wrapper_own_aws_cli) ... ok
test_repository_key_has_expected_current_fingerprint (test_aws_cli_acquisition.AwsCliAcquisitionTest.test_repository_key_has_expected_current_fingerprint) ... ok
test_verified_archive_runs_installer_with_user_local_update_arguments (test_aws_cli_acquisition.AwsCliAcquisitionTest.test_verified_archive_runs_installer_with_user_local_update_arguments) ... ok
test_wrong_staged_version_preserves_existing_aws_and_skips_installer (test_aws_cli_acquisition.AwsCliAcquisitionTest.test_wrong_staged_version_preserves_existing_aws_and_skips_installer) ... ok
test_agmsg_runtime_paths_are_ignored_on_both_sides (test_check_agent_runtime.CheckAgentRuntimeTest.test_agmsg_runtime_paths_are_ignored_on_both_sides) ... ok
test_agmsg_separate_store_prefix_is_ignored (test_check_agent_runtime.CheckAgentRuntimeTest.test_agmsg_separate_store_prefix_is_ignored) ... ok
test_asset_repair_invokes_only_the_detected_step (test_check_agent_runtime.CheckAgentRuntimeTest.test_asset_repair_invokes_only_the_detected_step) ... ok
test_check_includes_ua_core_warnings (test_check_agent_runtime.CheckAgentRuntimeTest.test_check_includes_ua_core_warnings) ... /home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/glob.py:456: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8f19fb50>
  entries = list(scandir_it)
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/glob.py:456: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8f19fc40>
  entries = list(scandir_it)
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/glob.py:456: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8f4d36a0>
  entries = list(scandir_it)
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/glob.py:456: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8f11b880>
  entries = list(scandir_it)
ResourceWarning: Enable tracemalloc to get the object allocation traceback
ok
test_check_uses_same_modified_for_codex_profiles (test_check_agent_runtime.CheckAgentRuntimeTest.test_check_uses_same_modified_for_codex_profiles) ... ok
test_chezmoi_drift_status_failure_is_warning (test_check_agent_runtime.CheckAgentRuntimeTest.test_chezmoi_drift_status_failure_is_warning) ... ok
test_chezmoi_drift_warnings_classify_status_and_mode_only (test_check_agent_runtime.CheckAgentRuntimeTest.test_chezmoi_drift_warnings_classify_status_and_mode_only) ... ok
test_compare_claude_skills_ignores_cowork_synced_subtree (test_check_agent_runtime.CheckAgentRuntimeTest.test_compare_claude_skills_ignores_cowork_synced_subtree) ... ok
test_content_drift_still_fails (test_check_agent_runtime.CheckAgentRuntimeTest.test_content_drift_still_fails) ... ok
test_crit_codex_skills_are_not_orphans (test_check_agent_runtime.CheckAgentRuntimeTest.test_crit_codex_skills_are_not_orphans) ... ok
test_deleted_shared_skill_file_repair_converges (test_check_agent_runtime.CheckAgentRuntimeTest.test_deleted_shared_skill_file_repair_converges) ... ok
test_every_generated_chezmoi_repair_action_is_forced (test_check_agent_runtime.CheckAgentRuntimeTest.test_every_generated_chezmoi_repair_action_is_forced) ... ok
test_executable_prefix_is_compared_against_deployed_name (test_check_agent_runtime.CheckAgentRuntimeTest.test_executable_prefix_is_compared_against_deployed_name) ... ok
test_executable_prefix_requires_deployed_execute_bit (test_check_agent_runtime.CheckAgentRuntimeTest.test_executable_prefix_requires_deployed_execute_bit) ... ok
test_execute_repair_calls_each_mapped_command_once (test_check_agent_runtime.CheckAgentRuntimeTest.test_execute_repair_calls_each_mapped_command_once) ... ok
test_ignored_paths_suppress_receipt_linked_tree_entries (test_check_agent_runtime.CheckAgentRuntimeTest.test_ignored_paths_suppress_receipt_linked_tree_entries) ... ok
test_installed_manifest_integrity_reasons (test_check_agent_runtime.CheckAgentRuntimeTest.test_installed_manifest_integrity_reasons) ... ok
test_installer_owned_agmsg_skill_and_backups_are_not_orphans (test_check_agent_runtime.CheckAgentRuntimeTest.test_installer_owned_agmsg_skill_and_backups_are_not_orphans) ... ok
test_invalid_manifest_is_one_error_and_skips_dependent_checks (test_check_agent_runtime.CheckAgentRuntimeTest.test_invalid_manifest_is_one_error_and_skips_dependent_checks) ... ok
test_json_modifier_accepts_cosmetic_reserialization (test_check_agent_runtime.CheckAgentRuntimeTest.test_json_modifier_accepts_cosmetic_reserialization) ... ok
test_json_modifier_rejects_real_value_drift (test_check_agent_runtime.CheckAgentRuntimeTest.test_json_modifier_rejects_real_value_drift) ... ok
test_managed_top_level_extra_still_fails_with_unmanaged_warning_mode (test_check_agent_runtime.CheckAgentRuntimeTest.test_managed_top_level_extra_still_fails_with_unmanaged_warning_mode) ... ok
test_manifest_drift_requires_recorded_step_with_missing_path (test_check_agent_runtime.CheckAgentRuntimeTest.test_manifest_drift_requires_recorded_step_with_missing_path) ... ok
test_missing_crit_asset_is_repairable (test_check_agent_runtime.CheckAgentRuntimeTest.test_missing_crit_asset_is_repairable) ... ok
test_missing_terminal_browser_receipt_is_harmless (test_check_agent_runtime.CheckAgentRuntimeTest.test_missing_terminal_browser_receipt_is_harmless) ... ok
test_only_exact_agmsg_root_legacy_database_names_are_ignored (test_check_agent_runtime.CheckAgentRuntimeTest.test_only_exact_agmsg_root_legacy_database_names_are_ignored) ... ok
test_orchestrator_seat_lock_is_quiet_for_a_composite_id_or_no_live_session (test_check_agent_runtime.CheckAgentRuntimeTest.test_orchestrator_seat_lock_is_quiet_for_a_composite_id_or_no_live_session) ... ok
test_orchestrator_seat_lock_warns_on_a_bare_session_id (test_check_agent_runtime.CheckAgentRuntimeTest.test_orchestrator_seat_lock_warns_on_a_bare_session_id) ... ok
test_orphan_detection_classifies_accounted_stale_and_orphan (test_check_agent_runtime.CheckAgentRuntimeTest.test_orphan_detection_classifies_accounted_stale_and_orphan) ... ok
test_parameterized_mise_step_uses_key_identity (test_check_agent_runtime.CheckAgentRuntimeTest.test_parameterized_mise_step_uses_key_identity) ... ok
test_private_prefix_is_compared_against_deployed_name (test_check_agent_runtime.CheckAgentRuntimeTest.test_private_prefix_is_compared_against_deployed_name) ... ok
test_repair_actions_map_only_detected_file_drift (test_check_agent_runtime.CheckAgentRuntimeTest.test_repair_actions_map_only_detected_file_drift) ... ok
test_repair_mode_converges_once_and_reports_each_action (test_check_agent_runtime.CheckAgentRuntimeTest.test_repair_mode_converges_once_and_reports_each_action) ... ok
test_repair_mode_fails_after_one_non_convergent_round (test_check_agent_runtime.CheckAgentRuntimeTest.test_repair_mode_fails_after_one_non_convergent_round) ... ok
test_repair_mode_never_acts_on_stale_or_orphan_warnings (test_check_agent_runtime.CheckAgentRuntimeTest.test_repair_mode_never_acts_on_stale_or_orphan_warnings) ... ok
test_repair_unset_is_byte_identical_and_never_mutates (test_check_agent_runtime.CheckAgentRuntimeTest.test_repair_unset_is_byte_identical_and_never_mutates) ... ok
test_sourced_asset_repair_runs_no_main_or_sibling_step (test_check_agent_runtime.CheckAgentRuntimeTest.test_sourced_asset_repair_runs_no_main_or_sibling_step) ... ok
test_terminal_browser_receipt_links_are_not_orphans (test_check_agent_runtime.CheckAgentRuntimeTest.test_terminal_browser_receipt_links_are_not_orphans) ... ok
test_ua_core_is_quiet_when_dist_is_fresh_or_no_clone_exists (test_check_agent_runtime.CheckAgentRuntimeTest.test_ua_core_is_quiet_when_dist_is_fresh_or_no_clone_exists) ... ok
test_ua_core_warns_when_dist_is_older_than_src (test_check_agent_runtime.CheckAgentRuntimeTest.test_ua_core_warns_when_dist_is_older_than_src) ... ok
test_ua_core_warns_when_dist_is_older_than_the_root_lockfile (test_check_agent_runtime.CheckAgentRuntimeTest.test_ua_core_warns_when_dist_is_older_than_the_root_lockfile) ... ok
test_ua_core_warns_when_the_codex_clone_has_no_built_dist (test_check_agent_runtime.CheckAgentRuntimeTest.test_ua_core_warns_when_the_codex_clone_has_no_built_dist) ... ok
test_unexpected_non_runtime_file_still_fails (test_check_agent_runtime.CheckAgentRuntimeTest.test_unexpected_non_runtime_file_still_fails) ... ok
test_unmanaged_top_level_skill_dir_warns (test_check_agent_runtime.CheckAgentRuntimeTest.test_unmanaged_top_level_skill_dir_warns) ... ok
test_apply_removes_the_symlink_farm_and_keeps_installer_owned_paths (test_chezmoiremove_agmsg.ChezmoiRemoveAgmsgTest.test_apply_removes_the_symlink_farm_and_keeps_installer_owned_paths) ... ok
test_retired_targets_are_listed_and_have_no_source (test_chezmoiremove_agmsg.ChezmoiRemoveRetiredShellFilesTest.test_retired_targets_are_listed_and_have_no_source) ... ok
test_current_only_key_is_preserved (test_claude_settings_merge.ClaudeSettingsMergeTest.test_current_only_key_is_preserved) ... ok
test_current_session_start_order_is_preserved (test_claude_settings_merge.ClaudeSettingsMergeTest.test_current_session_start_order_is_preserved)
Order is preserved; a stale bare herdr-agents command still migrates. ... ok
test_desired_current_output_is_byte_identical (test_claude_settings_merge.ClaudeSettingsMergeTest.test_desired_current_output_is_byte_identical) ... ok
test_empty_stdin_outputs_managed (test_claude_settings_merge.ClaudeSettingsMergeTest.test_empty_stdin_outputs_managed) ... ok
test_enabled_plugins_are_preserved_from_current (test_claude_settings_merge.ClaudeSettingsMergeTest.test_enabled_plugins_are_preserved_from_current) ... ok
test_invalid_json_outputs_managed (test_claude_settings_merge.ClaudeSettingsMergeTest.test_invalid_json_outputs_managed) ... ok
test_managed_hook_object_key_order_is_preserved (test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_hook_object_key_order_is_preserved) ... ok
test_managed_permgate_replaces_stale_current_ccgate_hook (test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_permgate_replaces_stale_current_ccgate_hook) ... ok
test_managed_session_start_replacement_keeps_hook_order (test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_session_start_replacement_keeps_hook_order)
Replacing a managed entry must not reorder SessionStart. ... ok
test_managed_session_start_replaces_stale_hard_coded_home_hook (test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_session_start_replaces_stale_hard_coded_home_hook)
Upgrade path: a machine that received the old hard-coded managed hook. ... ok
test_managed_wins_for_managed_key (test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_wins_for_managed_key) ... ok
test_merge_is_idempotent (test_claude_settings_merge.ClaudeSettingsMergeTest.test_merge_is_idempotent) ... ok
test_permission_merge_preserves_custom_hook_in_mixed_entry (test_claude_settings_merge.ClaudeSettingsMergeTest.test_permission_merge_preserves_custom_hook_in_mixed_entry) ... ok
test_permission_merge_preserves_unrelated_current_hooks (test_claude_settings_merge.ClaudeSettingsMergeTest.test_permission_merge_preserves_unrelated_current_hooks) ... ok
test_real_template_preserves_herdr_matcher_and_converges (test_claude_settings_merge.ClaudeSettingsMergeTest.test_real_template_preserves_herdr_matcher_and_converges) ... ok
test_real_value_change_is_redumped (test_claude_settings_merge.ClaudeSettingsMergeTest.test_real_value_change_is_redumped) ... ok
test_reordered_but_equal_current_is_byte_identical (test_claude_settings_merge.ClaudeSettingsMergeTest.test_reordered_but_equal_current_is_byte_identical) ... ok
test_runtime_enabled_plugins_survive_a_managed_file_without_the_key (test_claude_settings_merge.ClaudeSettingsMergeTest.test_runtime_enabled_plugins_survive_a_managed_file_without_the_key) ... ok
test_trailing_newline (test_claude_settings_merge.ClaudeSettingsMergeTest.test_trailing_newline) ... ok
test_current_only_runtime_tables_keep_current_group_order (test_codex_config_merge.CodexConfigMergeTest.test_current_only_runtime_tables_keep_current_group_order) ... ok
test_fresh_machine_outputs_managed_baseline (test_codex_config_merge.CodexConfigMergeTest.test_fresh_machine_outputs_managed_baseline) ... ok
test_managed_permgate_replaces_stale_private_ccgate_hook (test_codex_config_merge.CodexConfigMergeTest.test_managed_permgate_replaces_stale_private_ccgate_hook) ... ok
test_managed_templates_are_rendered_before_merge (test_codex_config_merge.CodexConfigMergeTest.test_managed_templates_are_rendered_before_merge) ... ok
test_managed_wins_for_managed_keys (test_codex_config_merge.CodexConfigMergeTest.test_managed_wins_for_managed_keys) ... ok
test_repeated_runtime_tables_are_preserved_in_order (test_codex_config_merge.CodexConfigMergeTest.test_repeated_runtime_tables_are_preserved_in_order) ... ok
test_retired_disabled_mcp_servers_are_purged_and_enabled_ones_kept (test_codex_config_merge.CodexConfigMergeTest.test_retired_disabled_mcp_servers_are_purged_and_enabled_ones_kept) ... ok
test_runtime_tables_are_preserved (test_codex_config_merge.CodexConfigMergeTest.test_runtime_tables_are_preserved) ... ok
test_runtime_tables_seed_from_managed_when_absent (test_codex_config_merge.CodexConfigMergeTest.test_runtime_tables_seed_from_managed_when_absent) ... ok
test_unknown_current_tables_are_preserved (test_codex_config_merge.CodexConfigMergeTest.test_unknown_current_tables_are_preserved) ... ok
test_working_tree_placeholder_falls_back_to_source_dir_parent (test_codex_config_merge.CodexConfigMergeTest.test_working_tree_placeholder_falls_back_to_source_dir_parent) ... ok
test_working_tree_placeholder_prefers_env_override (test_codex_config_merge.CodexConfigMergeTest.test_working_tree_placeholder_prefers_env_override) ... ok
test_rules_are_forbidden_only_and_cover_the_declared_prefixes (test_codex_execpolicy.CodexExecpolicyTest.test_rules_are_forbidden_only_and_cover_the_declared_prefixes) ... ok
test_missing_trusted_runtime_is_silent (test_contextdb_codex_notify.ContextdbCodexNotifyTest.test_missing_trusted_runtime_is_silent) ... ok
test_non_opted_project_is_silent_even_with_trusted_runtime (test_contextdb_codex_notify.ContextdbCodexNotifyTest.test_non_opted_project_is_silent_even_with_trusted_runtime) ... ok
test_project_cli_is_data_only_and_trusted_cli_gets_explicit_root (test_contextdb_codex_notify.ContextdbCodexNotifyTest.test_project_cli_is_data_only_and_trusted_cli_gets_explicit_root) ... ok
test_coverage_gems_are_compatible_and_exact (test_files_fixture.FilesFixtureTest.test_coverage_gems_are_compatible_and_exact) ... ok
test_fixture_uses_chezmoi_binary_outside_mise_shims (test_files_fixture.FilesFixtureTest.test_fixture_uses_chezmoi_binary_outside_mise_shims) ... ok
test_legacy_file_workflows_initialize_required_fixture_paths (test_files_fixture.FilesFixtureTest.test_legacy_file_workflows_initialize_required_fixture_paths) ... ok
test_a_missing_formatter_is_reported_without_a_traceback (test_format_edited_files_hook.FormatEditedFilesHookTest.test_a_missing_formatter_is_reported_without_a_traceback) ... ok
test_formatters_run_from_the_edited_files_repository_root (test_format_edited_files_hook.FormatEditedFilesHookTest.test_formatters_run_from_the_edited_files_repository_root) ... ok
test_a_declare_r_assignment_must_appear_exactly_once (test_generate_agent_configs.GenerateAgentConfigsTest.test_a_declare_r_assignment_must_appear_exactly_once) ... ok
test_a_list_render_writes_one_pin_into_several_files_and_declare_r (test_generate_agent_configs.GenerateAgentConfigsTest.test_a_list_render_writes_one_pin_into_several_files_and_declare_r) ... ok
test_absent_worker_profile_renders_no_env_line (test_generate_agent_configs.GenerateAgentConfigsTest.test_absent_worker_profile_renders_no_env_line) ... ok
test_absent_worker_worktree_renders_no_env_line (test_generate_agent_configs.GenerateAgentConfigsTest.test_absent_worker_worktree_renders_no_env_line) ... ok
test_an_empty_mcp_server_map_renders_no_tables_and_an_empty_claude_map (test_generate_agent_configs.GenerateAgentConfigsTest.test_an_empty_mcp_server_map_renders_no_tables_and_an_empty_claude_map) ... ok
test_asset_constant_must_be_assigned_exactly_once (test_generate_agent_configs.GenerateAgentConfigsTest.test_asset_constant_must_be_assigned_exactly_once) ... ok
test_asset_constants_render_into_their_files (test_generate_agent_configs.GenerateAgentConfigsTest.test_asset_constants_render_into_their_files) ... ok
test_asset_pin_must_be_a_plain_value (test_generate_agent_configs.GenerateAgentConfigsTest.test_asset_pin_must_be_a_plain_value) ... ok
test_audit_profile_renders_read_only_sandbox_override (test_generate_agent_configs.GenerateAgentConfigsTest.test_audit_profile_renders_read_only_sandbox_override) ... ok
test_bootstrap_pins_render_into_setup_and_their_installers (test_generate_agent_configs.GenerateAgentConfigsTest.test_bootstrap_pins_render_into_setup_and_their_installers) ... ok
test_check_reports_asset_render_drift (test_generate_agent_configs.GenerateAgentConfigsTest.test_check_reports_asset_render_drift) ... ok
test_claude_deny_rules_use_edit_for_file_mutations (test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_deny_rules_use_edit_for_file_mutations) ... ok
test_claude_sandbox_renders_optional_socket_and_extra_write_keys (test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_sandbox_renders_optional_socket_and_extra_write_keys) ... ok
test_claude_settings_render_interactive_advisor_only_when_set (test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_settings_render_interactive_advisor_only_when_set) ... ok
test_claude_settings_render_the_format_hook_from_its_path (test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_settings_render_the_format_hook_from_its_path) ... ok
test_claude_settings_renders_session_start_hooks (test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_settings_renders_session_start_hooks) ... ok
test_claude_settings_use_interactive_profile_with_permgate (test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_settings_use_interactive_profile_with_permgate) ... ok
test_claude_skill_symlink_outputs_strip_executable_target_prefix (test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_skill_symlink_outputs_strip_executable_target_prefix) ... ok
test_codex_config_renders_permgate_permission_request (test_generate_agent_configs.GenerateAgentConfigsTest.test_codex_config_renders_permgate_permission_request) ... ok
test_codex_config_renders_working_tree_project_key (test_generate_agent_configs.GenerateAgentConfigsTest.test_codex_config_renders_working_tree_project_key) ... ok
test_entries_reaching_one_file_through_a_symlink_edit_one_snapshot (test_generate_agent_configs.GenerateAgentConfigsTest.test_entries_reaching_one_file_through_a_symlink_edit_one_snapshot) ... ok
test_expected_outputs_uses_codex_baseline_path (test_generate_agent_configs.GenerateAgentConfigsTest.test_expected_outputs_uses_codex_baseline_path) ... ok
test_managed_claude_sandbox_excludes_agmsg_dispatch (test_generate_agent_configs.GenerateAgentConfigsTest.test_managed_claude_sandbox_excludes_agmsg_dispatch) ... ok
test_managed_codex_path_includes_installed_common_bin (test_generate_agent_configs.GenerateAgentConfigsTest.test_managed_codex_path_includes_installed_common_bin) ... ok
test_managed_hooks_use_installed_permgate_paths (test_generate_agent_configs.GenerateAgentConfigsTest.test_managed_hooks_use_installed_permgate_paths) ... ok
test_manifest_keeps_model_ids_only_in_profiles (test_generate_agent_configs.GenerateAgentConfigsTest.test_manifest_keeps_model_ids_only_in_profiles) ... ok
test_model_profiles_env_renders_claude_advisor_only_when_set (test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_renders_claude_advisor_only_when_set) ... ok
test_model_profiles_env_renders_worker_kind (test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_renders_worker_kind) ... ok
test_model_profiles_env_renders_worker_profile (test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_renders_worker_profile) ... ok
test_model_profiles_env_renders_worker_worktree (test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_renders_worker_worktree) ... ok
test_model_profiles_reject_incomplete_or_unsafe_entries (test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_reject_incomplete_or_unsafe_entries) ... ERROR: model profile standard is missing codex
ERROR: model profile standard.claude.model must be a launcher-safe string
ERROR: model_profiles must define the express profile
ok
test_model_profiles_reject_invalid_sandbox_mode (test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_reject_invalid_sandbox_mode) ... ok
test_model_profiles_reject_unsafe_advisor (test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_reject_unsafe_advisor) ... ERROR: model profile standard.claude.advisor must be a launcher-safe string
ok
test_profile_modify_scripts_are_byte_idempotent_with_runtime_state (test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_are_byte_idempotent_with_runtime_state) ... ok
test_profile_modify_scripts_are_quiet_for_matching_hook_trust (test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_are_quiet_for_matching_hook_trust) ... ok
test_profile_modify_scripts_preserve_repeated_runtime_tables (test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_preserve_repeated_runtime_tables) ... ok
test_profile_modify_scripts_preserve_runtime_state (test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_preserve_runtime_state) ... ok
test_profile_modify_scripts_seed_base_hook_trust (test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_seed_base_hook_trust) ... ok
test_profile_modify_scripts_warn_on_hook_trust_divergence (test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_warn_on_hook_trust_divergence) ... ok
test_repository_marketplace_is_a_runtime_owned_seed (test_generate_agent_configs.GenerateAgentConfigsTest.test_repository_marketplace_is_a_runtime_owned_seed) ... ok
test_security_profile_renders_launcher_and_expanded_notify (test_generate_agent_configs.GenerateAgentConfigsTest.test_security_profile_renders_launcher_and_expanded_notify) ... ok
test_set_asset_field_rejects_unknown_targets_and_unsafe_values (test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_field_rejects_unknown_targets_and_unsafe_values) ... ok
test_set_asset_field_rewrites_only_the_named_scalar (test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_field_rewrites_only_the_named_scalar) ... ok
test_set_asset_leaves_files_untouched_when_an_assignment_is_invalid (test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_leaves_files_untouched_when_an_assignment_is_invalid) ... ok
test_set_asset_refuses_fields_other_than_pins_and_checksums (test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_refuses_fields_other_than_pins_and_checksums) ... ok
test_set_asset_rejects_a_value_that_does_not_parse_back_as_a_string (test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_rejects_a_value_that_does_not_parse_back_as_a_string) ... ok
test_set_asset_reports_an_unparsable_manifest_without_a_traceback (test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_reports_an_unparsable_manifest_without_a_traceback) ... ok
test_set_asset_updates_the_manifest_and_renders_its_pins (test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_updates_the_manifest_and_renders_its_pins) ... ok
test_unknown_interactive_profile_fails (test_generate_agent_configs.GenerateAgentConfigsTest.test_unknown_interactive_profile_fails) ... ERROR: interactive_profile must name a model profile: 'missing'
ok
test_unknown_worker_kind_fails (test_generate_agent_configs.GenerateAgentConfigsTest.test_unknown_worker_kind_fails) ... ERROR: worker_kind must be one of ('codex', 'claude'): 'banana'
ok
test_unknown_worker_profile_fails (test_generate_agent_configs.GenerateAgentConfigsTest.test_unknown_worker_profile_fails) ... ERROR: worker_profile must name a model profile: 'missing'
ok
test_worker_gh_dir_is_shell_safe_and_defaults_to_separate_config (test_generate_agent_configs.GenerateAgentConfigsTest.test_worker_gh_dir_is_shell_safe_and_defaults_to_separate_config) ... ERROR: worker_gh_config_dir must be an absolute or ~/ path without control characters
ERROR: worker_gh_config_dir must be an absolute or ~/ path without control characters
ERROR: worker_gh_config_dir must be an absolute or ~/ path without control characters
ERROR: worker_gh_config_dir must be an absolute or ~/ path without control characters
ok
test_worker_kind_defaults_to_codex (test_generate_agent_configs.GenerateAgentConfigsTest.test_worker_kind_defaults_to_codex) ... ok
test_worker_worktree_outside_claude_worktrees_fails (test_generate_agent_configs.GenerateAgentConfigsTest.test_worker_worktree_outside_claude_worktrees_fails) ... ERROR: worker_worktree must be a relative path under .claude/worktrees/: 'worker-c'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '/abs/.claude/worktrees/x'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/..'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/a/b'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/$(x)'
ok
test_a_real_directory_of_that_name_stays_visible (test_gitignore_sandbox_placeholders.SandboxPlaceholderIgnoreTest.test_a_real_directory_of_that_name_stays_visible) ... ok
test_claude_settings_stay_visible (test_gitignore_sandbox_placeholders.SandboxPlaceholderIgnoreTest.test_claude_settings_stay_visible) ... ok
test_empty_placeholder_files_on_disk_leave_status_clean (test_gitignore_sandbox_placeholders.SandboxPlaceholderIgnoreTest.test_empty_placeholder_files_on_disk_leave_status_clean) ... ok
test_every_placeholder_is_ignored_at_the_root_only (test_gitignore_sandbox_placeholders.SandboxPlaceholderIgnoreTest.test_every_placeholder_is_ignored_at_the_root_only) ... ok
test_add_worker_accepts_a_claude_trust_dialog_while_spawn_waits (test_herdr_agents.HerdrAgentsTest.test_add_worker_accepts_a_claude_trust_dialog_while_spawn_waits) ... ok
test_add_worker_derives_the_default_herdr_socket_for_spawn (test_herdr_agents.HerdrAgentsTest.test_add_worker_derives_the_default_herdr_socket_for_spawn) ... ok
test_add_worker_emits_no_override_for_an_unparseable_codex_config (test_herdr_agents.HerdrAgentsTest.test_add_worker_emits_no_override_for_an_unparseable_codex_config) ... ok
test_add_worker_exits_zero_when_a_timed_out_spawn_still_links (test_herdr_agents.HerdrAgentsTest.test_add_worker_exits_zero_when_a_timed_out_spawn_still_links) ... ok
test_add_worker_keeps_the_configured_roots_from_an_indented_multi_line_array (test_herdr_agents.HerdrAgentsTest.test_add_worker_keeps_the_configured_roots_from_an_indented_multi_line_array) ... ok
test_add_worker_linkage_failure_prints_the_invocation_and_the_query (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_failure_prints_the_invocation_and_the_query) ... ok
test_add_worker_linkage_falls_back_to_the_legacy_record_without_the_resolver (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_falls_back_to_the_legacy_record_without_the_resolver) ... ok
test_add_worker_linkage_ignores_a_delayed_pong_for_another_ping (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_ignores_a_delayed_pong_for_another_ping) ... ok
test_add_worker_linkage_ignores_a_placement_record_for_a_pane_gone_from_the_workspace (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_ignores_a_placement_record_for_a_pane_gone_from_the_workspace) ... ok
test_add_worker_linkage_ignores_a_placement_record_for_a_pane_that_predates_this_spawn (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_ignores_a_placement_record_for_a_pane_that_predates_this_spawn) ... ok
test_add_worker_linkage_ignores_a_placement_record_from_another_workspace (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_ignores_a_placement_record_from_another_workspace) ... ok
test_add_worker_linkage_ignores_a_pong_older_than_this_ping (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_ignores_a_pong_older_than_this_ping) ... ok
test_add_worker_linkage_reads_a_leading_zero_wait_as_decimal (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_reads_a_leading_zero_wait_as_decimal) ... ok
test_add_worker_linkage_refuses_a_placement_conflict (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_refuses_a_placement_conflict) ... ok
test_add_worker_linkage_refuses_several_orchestrator_identities (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_refuses_several_orchestrator_identities) ... ok
test_add_worker_linkage_resolves_an_id_keyed_placement_record (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_resolves_an_id_keyed_placement_record) ... ok
test_add_worker_linkage_survives_a_non_numeric_pong_wait (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_survives_a_non_numeric_pong_wait) ... ok
test_add_worker_linkage_uses_the_spawn_placement_record_not_team_sh (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_uses_the_spawn_placement_record_not_team_sh) ... ok
test_add_worker_passes_codex_profile_and_sandbox_through_spawn_options (test_herdr_agents.HerdrAgentsTest.test_add_worker_passes_codex_profile_and_sandbox_through_spawn_options) ... ok
test_add_worker_refuses_an_undefined_profile_before_any_change (test_herdr_agents.HerdrAgentsTest.test_add_worker_refuses_an_undefined_profile_before_any_change) ... ok
test_add_worker_refuses_before_any_change_when_no_herdr_socket_is_found (test_herdr_agents.HerdrAgentsTest.test_add_worker_refuses_before_any_change_when_no_herdr_socket_is_found) ... ok
test_add_worker_rejects_a_worktree_outside_claude_worktrees (test_herdr_agents.HerdrAgentsTest.test_add_worker_rejects_a_worktree_outside_claude_worktrees) ... ok
test_add_worker_reports_a_failed_claude_spawn_without_a_trust_dialog (test_herdr_agents.HerdrAgentsTest.test_add_worker_reports_a_failed_claude_spawn_without_a_trust_dialog) ... ok
test_add_worker_reports_a_failed_spawn (test_herdr_agents.HerdrAgentsTest.test_add_worker_reports_a_failed_spawn) ... ok
test_add_worker_reports_linkage_ok_after_a_ready_spawn (test_herdr_agents.HerdrAgentsTest.test_add_worker_reports_linkage_ok_after_a_ready_spawn) ... ok
test_add_worker_reports_linkage_unreached_after_a_failed_spawn (test_herdr_agents.HerdrAgentsTest.test_add_worker_reports_linkage_unreached_after_a_failed_spawn) ... ok
test_add_worker_reports_shallow_metadata_as_not_granted (test_herdr_agents.HerdrAgentsTest.test_add_worker_reports_shallow_metadata_as_not_granted) ... ok
test_add_worker_reuses_a_seat_tab_in_the_pair_workspace (test_herdr_agents.HerdrAgentsTest.test_add_worker_reuses_a_seat_tab_in_the_pair_workspace) ... ok
test_add_worker_reuses_a_seated_workspace (test_herdr_agents.HerdrAgentsTest.test_add_worker_reuses_a_seated_workspace) ... ok
test_add_worker_seats_the_worker_in_a_tab_of_the_pair_workspace (test_herdr_agents.HerdrAgentsTest.test_add_worker_seats_the_worker_in_a_tab_of_the_pair_workspace) ... ok
test_add_worker_spawns_the_seat_in_its_own_workspace_with_profile_args (test_herdr_agents.HerdrAgentsTest.test_add_worker_spawns_the_seat_in_its_own_workspace_with_profile_args) ... ok
test_add_worker_succeeds_for_a_claude_worker_without_a_trust_dialog (test_herdr_agents.HerdrAgentsTest.test_add_worker_succeeds_for_a_claude_worker_without_a_trust_dialog) ... ok
test_added_worker_github_environment_reaches_boot (test_herdr_agents.HerdrAgentsTest.test_added_worker_github_environment_reaches_boot) ... ok
test_agent_name_taken_gives_up_after_bounded_wait (test_herdr_agents.HerdrAgentsTest.test_agent_name_taken_gives_up_after_bounded_wait) ... ok
test_another_team_members_pane_is_not_a_second_worker (test_herdr_agents.HerdrAgentsTest.test_another_team_members_pane_is_not_a_second_worker) ... ok
test_attach_bootstraps_agmsg_after_codex_reuse (test_herdr_agents.HerdrAgentsTest.test_attach_bootstraps_agmsg_after_codex_reuse) ... ok
test_attach_bootstraps_agmsg_after_codex_start (test_herdr_agents.HerdrAgentsTest.test_attach_bootstraps_agmsg_after_codex_start) ... ok
test_attach_builds_codex_right_of_current_claude_pane (test_herdr_agents.HerdrAgentsTest.test_attach_builds_codex_right_of_current_claude_pane) ... ok
test_attach_complete_workspace_is_idempotent (test_herdr_agents.HerdrAgentsTest.test_attach_complete_workspace_is_idempotent) ... ok
test_attach_completes_bootstrap_on_a_self_named_pair (test_herdr_agents.HerdrAgentsTest.test_attach_completes_bootstrap_on_a_self_named_pair) ... ok
test_attach_correct_order_does_not_swap (test_herdr_agents.HerdrAgentsTest.test_attach_correct_order_does_not_swap) ... ok
test_attach_does_not_restart_codex_agent_from_another_tab (test_herdr_agents.HerdrAgentsTest.test_attach_does_not_restart_codex_agent_from_another_tab) ... ok
test_attach_equal_halves_does_not_resize (test_herdr_agents.HerdrAgentsTest.test_attach_equal_halves_does_not_resize) ... ok
test_attach_from_the_self_named_worker_pane_exits_quietly (test_herdr_agents.HerdrAgentsTest.test_attach_from_the_self_named_worker_pane_exits_quietly) ... ok
test_attach_from_the_worker_pane_does_not_relabel_it (test_herdr_agents.HerdrAgentsTest.test_attach_from_the_worker_pane_does_not_relabel_it) ... ok
test_attach_from_the_worker_worktree_exits_quietly (test_herdr_agents.HerdrAgentsTest.test_attach_from_the_worker_worktree_exits_quietly) ... ok
test_attach_ignores_agmsg_bootstrap_failure (test_herdr_agents.HerdrAgentsTest.test_attach_ignores_agmsg_bootstrap_failure) ... ok
test_attach_ignores_extra_panes_on_other_tabs (test_herdr_agents.HerdrAgentsTest.test_attach_ignores_extra_panes_on_other_tabs) ... ok
test_attach_leaves_a_self_named_pair_alone (test_herdr_agents.HerdrAgentsTest.test_attach_leaves_a_self_named_pair_alone) ... ok
test_attach_legacy_files_pane_refuses_repair_without_layout_mutation (test_herdr_agents.HerdrAgentsTest.test_attach_legacy_files_pane_refuses_repair_without_layout_mutation) ... ok
test_attach_lowercases_and_validates_derived_agent_name (test_herdr_agents.HerdrAgentsTest.test_attach_lowercases_and_validates_derived_agent_name) ... ok
test_attach_noops_for_full_mode_managed_layout (test_herdr_agents.HerdrAgentsTest.test_attach_noops_for_full_mode_managed_layout) ... ok
test_attach_ratio_repair_skips_unsafe_layouts (test_herdr_agents.HerdrAgentsTest.test_attach_ratio_repair_skips_unsafe_layouts) ... ok
test_attach_rejects_invalid_derived_agent_name (test_herdr_agents.HerdrAgentsTest.test_attach_rejects_invalid_derived_agent_name) ... ok
test_attach_repair_splits_the_missing_worker_pane_in_its_worktree (test_herdr_agents.HerdrAgentsTest.test_attach_repair_splits_the_missing_worker_pane_in_its_worktree) ... ok
test_attach_repairs_codex_claude_order_with_one_swap (test_herdr_agents.HerdrAgentsTest.test_attach_repairs_codex_claude_order_with_one_swap) ... ok
test_attach_repairs_skewed_widths_to_equal_halves (test_herdr_agents.HerdrAgentsTest.test_attach_repairs_skewed_widths_to_equal_halves) ... ok
test_attach_reports_agmsg_skip_when_not_installed (test_herdr_agents.HerdrAgentsTest.test_attach_reports_agmsg_skip_when_not_installed) ... ok
test_attach_skips_delivery_when_turn_hook_exists (test_herdr_agents.HerdrAgentsTest.test_attach_skips_delivery_when_turn_hook_exists) ... ok
test_attach_warns_after_one_nonconverging_resize (test_herdr_agents.HerdrAgentsTest.test_attach_warns_after_one_nonconverging_resize) ... ok
test_attach_warns_when_multiple_agmsg_identities_exist (test_herdr_agents.HerdrAgentsTest.test_attach_warns_when_multiple_agmsg_identities_exist) ... ok
test_attach_without_herdr_environment_names_the_seated_worker (test_herdr_agents.HerdrAgentsTest.test_attach_without_herdr_environment_names_the_seated_worker) ... ok
test_attach_without_herdr_environment_prints_the_bring_up_summary (test_herdr_agents.HerdrAgentsTest.test_attach_without_herdr_environment_prints_the_bring_up_summary) ... ok
test_attach_without_herdr_environment_stays_quiet_in_the_worker_worktree (test_herdr_agents.HerdrAgentsTest.test_attach_without_herdr_environment_stays_quiet_in_the_worker_worktree) ... ok
test_audit_accepts_a_dir_with_an_apostrophe_quoted_intact (test_herdr_agents.HerdrAgentsTest.test_audit_accepts_a_dir_with_an_apostrophe_quoted_intact) ... ok
test_audit_creates_the_audit_tab_once_and_reuses_it (test_herdr_agents.HerdrAgentsTest.test_audit_creates_the_audit_tab_once_and_reuses_it) ... ok
test_audit_exits_2_without_a_managed_workspace (test_herdr_agents.HerdrAgentsTest.test_audit_exits_2_without_a_managed_workspace) ... ok
test_audit_fails_as_unmasked_when_masking_fails (test_herdr_agents.HerdrAgentsTest.test_audit_fails_as_unmasked_when_masking_fails) ... ok
test_audit_falls_back_to_the_recent_unwrapped_prompt_without_process_info (test_herdr_agents.HerdrAgentsTest.test_audit_falls_back_to_the_recent_unwrapped_prompt_without_process_info) ... ok
test_audit_finds_the_self_named_pair_workspace (test_herdr_agents.HerdrAgentsTest.test_audit_finds_the_self_named_pair_workspace) ... ok
test_audit_gates_on_the_concluding_line_of_the_last_message (test_herdr_agents.HerdrAgentsTest.test_audit_gates_on_the_concluding_line_of_the_last_message) ... ok
test_audit_marker_detection_reads_unwrapped_snapshots (test_herdr_agents.HerdrAgentsTest.test_audit_marker_detection_reads_unwrapped_snapshots) ... ok
test_audit_masks_evidence_before_the_verdict_gate (test_herdr_agents.HerdrAgentsTest.test_audit_masks_evidence_before_the_verdict_gate) ... ok
test_audit_masks_evidence_even_when_the_audit_exit_is_nonzero (test_herdr_agents.HerdrAgentsTest.test_audit_masks_evidence_even_when_the_audit_exit_is_nonzero) ... ok
test_audit_nonzero_exit_marker_fails_the_helper (test_herdr_agents.HerdrAgentsTest.test_audit_nonzero_exit_marker_fails_the_helper) ... ok
test_audit_pane_command_tees_evidence_and_waits_for_a_fresh_marker (test_herdr_agents.HerdrAgentsTest.test_audit_pane_command_tees_evidence_and_waits_for_a_fresh_marker) ... ok
test_audit_quotes_a_non_ascii_out_path_under_the_c_locale (test_herdr_agents.HerdrAgentsTest.test_audit_quotes_a_non_ascii_out_path_under_the_c_locale) ... ok
test_audit_quotes_the_last_message_path_for_a_non_ascii_out (test_herdr_agents.HerdrAgentsTest.test_audit_quotes_the_last_message_path_for_a_non_ascii_out) ... ok
test_audit_refuses_a_busy_audit_pane (test_herdr_agents.HerdrAgentsTest.test_audit_refuses_a_busy_audit_pane) ... ok
test_audit_refuses_a_tracked_masker_missing_from_the_tree (test_herdr_agents.HerdrAgentsTest.test_audit_refuses_a_tracked_masker_missing_from_the_tree) ... ok
test_audit_refuses_an_uncommitted_or_untracked_masker (test_herdr_agents.HerdrAgentsTest.test_audit_refuses_an_uncommitted_or_untracked_masker) ... ok
test_audit_refuses_the_masker_from_the_audited_commit (test_herdr_agents.HerdrAgentsTest.test_audit_refuses_the_masker_from_the_audited_commit) ... ok
test_audit_rejects_unsafe_arguments_before_calling_herdr (test_herdr_agents.HerdrAgentsTest.test_audit_rejects_unsafe_arguments_before_calling_herdr) ... ok
test_audit_runs_codex_exec_with_the_prompt_and_last_message_file (test_herdr_agents.HerdrAgentsTest.test_audit_runs_codex_exec_with_the_prompt_and_last_message_file) ... ok
test_audit_runs_in_dir_even_when_the_reused_pane_moved (test_herdr_agents.HerdrAgentsTest.test_audit_runs_in_dir_even_when_the_reused_pane_moved) ... ok
test_audit_skips_masking_without_a_repo_validator (test_herdr_agents.HerdrAgentsTest.test_audit_skips_masking_without_a_repo_validator) ... ok
test_audit_tab_does_not_break_attach_order_and_ratio_repair (test_herdr_agents.HerdrAgentsTest.test_audit_tab_does_not_break_attach_order_and_ratio_repair) ... ok
test_audit_tab_keeps_the_full_mode_duplicate_workspace_guard (test_herdr_agents.HerdrAgentsTest.test_audit_tab_keeps_the_full_mode_duplicate_workspace_guard) ... ok
test_audit_task_inlines_the_task_inputs_and_the_merge_base_diff (test_herdr_agents.HerdrAgentsTest.test_audit_task_inlines_the_task_inputs_and_the_merge_base_diff) ... ok
test_audit_task_names_a_txt_artifact_when_no_md_one_exists (test_herdr_agents.HerdrAgentsTest.test_audit_task_names_a_txt_artifact_when_no_md_one_exists) ... ok
test_audit_task_names_only_the_task_file_when_no_artifact_exists (test_herdr_agents.HerdrAgentsTest.test_audit_task_names_only_the_task_file_when_no_artifact_exists) ... ok
test_audit_task_refuses_a_missing_task_file_or_merge_base_before_herdr_work (test_herdr_agents.HerdrAgentsTest.test_audit_task_refuses_a_missing_task_file_or_merge_base_before_herdr_work) ... ok
test_audit_trusts_a_shell_foreground_over_a_stale_visible_snapshot (test_herdr_agents.HerdrAgentsTest.test_audit_trusts_a_shell_foreground_over_a_stale_visible_snapshot) ... ok
test_audit_uses_manifest_audit_codex_args (test_herdr_agents.HerdrAgentsTest.test_audit_uses_manifest_audit_codex_args) ... ok
test_audit_verdict_gate_reads_only_the_final_codex_block (test_herdr_agents.HerdrAgentsTest.test_audit_verdict_gate_reads_only_the_final_codex_block) ... ok
test_audit_waits_for_the_prompt_on_a_new_audit_tab (test_herdr_agents.HerdrAgentsTest.test_audit_waits_for_the_prompt_on_a_new_audit_tab) ... ok
test_bootstrap_accepts_same_identity_in_multiple_teams (test_herdr_agents.HerdrAgentsTest.test_bootstrap_accepts_same_identity_in_multiple_teams) ... ok
test_bootstrap_leaves_a_foreign_pre_push_hook_alone (test_herdr_agents.HerdrAgentsTest.test_bootstrap_leaves_a_foreign_pre_push_hook_alone) ... ok
test_bootstrap_only_creates_missing_herdr_log_directory (test_herdr_agents.HerdrAgentsTest.test_bootstrap_only_creates_missing_herdr_log_directory) ... ok
test_bootstrap_only_does_not_call_herdr_or_agents (test_herdr_agents.HerdrAgentsTest.test_bootstrap_only_does_not_call_herdr_or_agents) ... ok
test_bootstrap_only_sets_claude_delivery_once_when_hook_is_missing (test_herdr_agents.HerdrAgentsTest.test_bootstrap_only_sets_claude_delivery_once_when_hook_is_missing) ... ok
test_bootstrap_only_sets_each_missing_delivery_once (test_herdr_agents.HerdrAgentsTest.test_bootstrap_only_sets_each_missing_delivery_once) ... ok
test_bootstrap_only_skips_all_delivery_when_both_hooks_exist (test_herdr_agents.HerdrAgentsTest.test_bootstrap_only_skips_all_delivery_when_both_hooks_exist) ... ok
test_bootstrap_only_skips_home_without_agmsg_calls (test_herdr_agents.HerdrAgentsTest.test_bootstrap_only_skips_home_without_agmsg_calls) ... ok
test_bootstrap_only_warns_for_missing_claude_identity_without_joining (test_herdr_agents.HerdrAgentsTest.test_bootstrap_only_warns_for_missing_claude_identity_without_joining) ... ok
test_bootstrap_only_warns_for_multiple_claude_identities (test_herdr_agents.HerdrAgentsTest.test_bootstrap_only_warns_for_multiple_claude_identities) ... ok
test_bootstrap_removes_its_retired_pre_push_stub (test_herdr_agents.HerdrAgentsTest.test_bootstrap_removes_its_retired_pre_push_stub) ... ok
test_bootstrap_with_claude_worker_accepts_two_claude_identities (test_herdr_agents.HerdrAgentsTest.test_bootstrap_with_claude_worker_accepts_two_claude_identities) ... ok
test_bootstrap_with_claude_worker_hints_at_a_missing_worker_identity (test_herdr_agents.HerdrAgentsTest.test_bootstrap_with_claude_worker_hints_at_a_missing_worker_identity) ... ok
test_bootstrap_with_claude_worker_leaves_codex_hooks_alone (test_herdr_agents.HerdrAgentsTest.test_bootstrap_with_claude_worker_leaves_codex_hooks_alone) ... ok
test_claude_agent_accepts_manifest_profile_arguments_for_e2e (test_herdr_agents.HerdrAgentsTest.test_claude_agent_accepts_manifest_profile_arguments_for_e2e) ... ok
test_claude_repair_skips_just_restarted_codex_pane_without_agent_field (test_herdr_agents.HerdrAgentsTest.test_claude_repair_skips_just_restarted_codex_pane_without_agent_field) ... ok
test_claude_settings_add_herdr_attach_session_hook (test_herdr_agents.HerdrAgentsTest.test_claude_settings_add_herdr_attach_session_hook) ... ok
test_claude_worker_sharing_the_orchestrator_identity_is_refused (test_herdr_agents.HerdrAgentsTest.test_claude_worker_sharing_the_orchestrator_identity_is_refused) ... ok
test_claude_worker_with_a_registered_worker_identity_proceeds (test_herdr_agents.HerdrAgentsTest.test_claude_worker_with_a_registered_worker_identity_proceeds) ... ok
test_codex_profile_defaults_to_generated_interactive_profile (test_herdr_agents.HerdrAgentsTest.test_codex_profile_defaults_to_generated_interactive_profile) ... ok
test_codex_worker_is_not_subject_to_the_identity_guard (test_herdr_agents.HerdrAgentsTest.test_codex_worker_is_not_subject_to_the_identity_guard) ... ok
test_existing_legacy_files_pane_is_not_reused_for_claude_or_split_again (test_herdr_agents.HerdrAgentsTest.test_existing_legacy_files_pane_is_not_reused_for_claude_or_split_again) ... ok
test_existing_two_pane_workspace_repairs_skewed_widths (test_herdr_agents.HerdrAgentsTest.test_existing_two_pane_workspace_repairs_skewed_widths) ... ok
test_existing_workspace_matches_canonical_macos_workdir (test_herdr_agents.HerdrAgentsTest.test_existing_workspace_matches_canonical_macos_workdir) ... ok
test_existing_workspace_restarts_missing_claude_in_empty_pane (test_herdr_agents.HerdrAgentsTest.test_existing_workspace_restarts_missing_claude_in_empty_pane) ... ok
test_existing_workspace_restarts_missing_codex_agent (test_herdr_agents.HerdrAgentsTest.test_existing_workspace_restarts_missing_codex_agent) ... ok
test_existing_workspace_splits_when_missing_claude_has_no_empty_pane (test_herdr_agents.HerdrAgentsTest.test_existing_workspace_splits_when_missing_claude_has_no_empty_pane) ... ok
test_existing_workspace_with_legacy_files_pane_focuses_without_mutation (test_herdr_agents.HerdrAgentsTest.test_existing_workspace_with_legacy_files_pane_focuses_without_mutation) ... ok
test_explicit_worker_kind_and_profile_survive_seat_label_loading (test_herdr_agents.HerdrAgentsTest.test_explicit_worker_kind_and_profile_survive_seat_label_loading) ... ok
test_file_viewer_plugin_config_sets_micro_editor (test_herdr_agents.HerdrAgentsTest.test_file_viewer_plugin_config_sets_micro_editor) ... ok
test_full_and_restart_modes_refuse_duplicate_managed_workspaces (test_herdr_agents.HerdrAgentsTest.test_full_and_restart_modes_refuse_duplicate_managed_workspaces) ... ok
test_full_mode_does_not_duplicate_a_solo_codex_worker_seat (test_herdr_agents.HerdrAgentsTest.test_full_mode_does_not_duplicate_a_solo_codex_worker_seat) ... ok
test_full_mode_gives_a_codex_worker_its_worktree_git_metadata_roots (test_herdr_agents.HerdrAgentsTest.test_full_mode_gives_a_codex_worker_its_worktree_git_metadata_roots) ... ok
test_full_mode_heal_moves_a_reused_empty_pane_into_the_worktree (test_herdr_agents.HerdrAgentsTest.test_full_mode_heal_moves_a_reused_empty_pane_into_the_worktree) ... ok
test_full_mode_heal_never_starts_the_worker_in_an_exited_added_worker_pane (test_herdr_agents.HerdrAgentsTest.test_full_mode_heal_never_starts_the_worker_in_an_exited_added_worker_pane) ... ok
test_full_mode_heal_never_starts_the_worker_in_the_audit_pane (test_herdr_agents.HerdrAgentsTest.test_full_mode_heal_never_starts_the_worker_in_the_audit_pane) ... ok
test_full_mode_heals_nothing_in_a_healthy_self_named_pair (test_herdr_agents.HerdrAgentsTest.test_full_mode_heals_nothing_in_a_healthy_self_named_pair) ... ok
test_full_mode_heals_the_orchestrator_beside_a_live_added_claude_worker (test_herdr_agents.HerdrAgentsTest.test_full_mode_heals_the_orchestrator_beside_a_live_added_claude_worker) ... ok
test_full_mode_reuses_agentless_worker_pane_in_attach_labeled_workspace (test_herdr_agents.HerdrAgentsTest.test_full_mode_reuses_agentless_worker_pane_in_attach_labeled_workspace) ... ok
test_full_mode_skips_agmsg_bootstrap_for_home (test_herdr_agents.HerdrAgentsTest.test_full_mode_skips_agmsg_bootstrap_for_home) ... ok
test_full_mode_splits_the_worker_pane_in_its_worktree (test_herdr_agents.HerdrAgentsTest.test_full_mode_splits_the_worker_pane_in_its_worktree) ... ok
test_ghostty_config_does_not_auto_start_herdr_session (test_herdr_agents.HerdrAgentsTest.test_ghostty_config_does_not_auto_start_herdr_session) ... ok
test_herdr_prefix_alt_a_runs_helper_from_active_pane (test_herdr_agents.HerdrAgentsTest.test_herdr_prefix_alt_a_runs_helper_from_active_pane) ... ok
test_herdr_prefix_f_opens_file_viewer_popup (test_herdr_agents.HerdrAgentsTest.test_herdr_prefix_f_opens_file_viewer_popup) ... ok
test_make_update_and_upgrade_include_agmsg_bootstrap (test_herdr_agents.HerdrAgentsTest.test_make_update_and_upgrade_include_agmsg_bootstrap) ... ok
test_mixed_legacy_and_seat_labels_are_one_pair (test_herdr_agents.HerdrAgentsTest.test_mixed_legacy_and_seat_labels_are_one_pair) ... ok
test_new_pane_waits_for_shell_and_retries_agent_start_once_on_timeout (test_herdr_agents.HerdrAgentsTest.test_new_pane_waits_for_shell_and_retries_agent_start_once_on_timeout) ... ok
test_orchestrator_pane_appends_claude_args_after_profile_args (test_herdr_agents.HerdrAgentsTest.test_orchestrator_pane_appends_claude_args_after_profile_args) ... ok
test_orchestrator_pane_start_claims_the_seat_with_the_composite_id (test_herdr_agents.HerdrAgentsTest.test_orchestrator_pane_start_claims_the_seat_with_the_composite_id) ... ok
test_orchestrator_pane_start_without_a_session_claims_nothing (test_herdr_agents.HerdrAgentsTest.test_orchestrator_pane_start_without_a_session_claims_nothing) ... ok
test_orchestrator_pane_uses_interactive_profile_args (test_herdr_agents.HerdrAgentsTest.test_orchestrator_pane_uses_interactive_profile_args) ... ok
test_pane_creation_propagates_explicit_fpath (test_herdr_agents.HerdrAgentsTest.test_pane_creation_propagates_explicit_fpath) ... ok
test_regime_boundary_check_counts_names_across_runtime_types_at_an_active_seat (test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_counts_names_across_runtime_types_at_an_active_seat) ... ok
test_regime_boundary_check_finds_worker_workspaces_from_a_worktree (test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_finds_worker_workspaces_from_a_worktree) ... ok
test_regime_boundary_check_flags_empty_seats_only (test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_flags_empty_seats_only) ... ok
test_regime_boundary_check_gives_the_seat_lock_check_the_main_checkout (test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_gives_the_seat_lock_check_the_main_checkout) ... ok
test_regime_boundary_check_reports_an_added_worker_tab_in_the_pair_workspace (test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_reports_an_added_worker_tab_in_the_pair_workspace) ... ok
test_regime_boundary_check_scans_every_worktree_for_untracked_evidence (test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_scans_every_worktree_for_untracked_evidence) ... ok
test_registered_agent_not_ready_waits_for_idle_without_duplicate_start (test_herdr_agents.HerdrAgentsTest.test_registered_agent_not_ready_waits_for_idle_without_duplicate_start) ... ok
test_remove_worker_cleans_up_a_codex_seat_without_a_placement_record (test_herdr_agents.HerdrAgentsTest.test_remove_worker_cleans_up_a_codex_seat_without_a_placement_record) ... ok
test_remove_worker_closes_only_its_tab_in_the_pair_workspace (test_herdr_agents.HerdrAgentsTest.test_remove_worker_closes_only_its_tab_in_the_pair_workspace) ... ok
test_remove_worker_despawns_then_turns_delivery_off_leaves_and_closes (test_herdr_agents.HerdrAgentsTest.test_remove_worker_despawns_then_turns_delivery_off_leaves_and_closes) ... ok
test_remove_worker_force_retries_a_failed_graceful_despawn (test_herdr_agents.HerdrAgentsTest.test_remove_worker_force_retries_a_failed_graceful_despawn) ... ok
test_remove_worker_force_skips_the_forced_despawn_when_graceful_succeeds (test_herdr_agents.HerdrAgentsTest.test_remove_worker_force_skips_the_forced_despawn_when_graceful_succeeds) ... ok
test_remove_worker_forces_despawn_when_graceful_reports_needs_force (test_herdr_agents.HerdrAgentsTest.test_remove_worker_forces_despawn_when_graceful_reports_needs_force) ... ok
test_remove_worker_keeps_a_worker_tab_that_holds_another_running_agent (test_herdr_agents.HerdrAgentsTest.test_remove_worker_keeps_a_worker_tab_that_holds_another_running_agent) ... ok
test_remove_worker_refuses_a_dirty_worktree_without_force (test_herdr_agents.HerdrAgentsTest.test_remove_worker_refuses_a_dirty_worktree_without_force) ... ok
test_remove_worker_stops_when_a_graceful_despawn_fails (test_herdr_agents.HerdrAgentsTest.test_remove_worker_stops_when_a_graceful_despawn_fails) ... ok
test_remove_worker_stops_when_the_forced_retry_also_fails (test_herdr_agents.HerdrAgentsTest.test_remove_worker_stops_when_the_forced_retry_also_fails) ... ok
test_restart_worker_confirms_the_exit_dialog_once (test_herdr_agents.HerdrAgentsTest.test_restart_worker_confirms_the_exit_dialog_once) ... ok
test_restart_worker_exits_2_without_a_managed_workspace (test_herdr_agents.HerdrAgentsTest.test_restart_worker_exits_2_without_a_managed_workspace) ... ok
test_restart_worker_finds_a_solo_codex_worker_seat (test_herdr_agents.HerdrAgentsTest.test_restart_worker_finds_a_solo_codex_worker_seat) ... ok
test_restart_worker_finds_the_worker_by_its_seat_label (test_herdr_agents.HerdrAgentsTest.test_restart_worker_finds_the_worker_by_its_seat_label) ... ok
test_restart_worker_never_treats_the_audit_pane_as_the_worker (test_herdr_agents.HerdrAgentsTest.test_restart_worker_never_treats_the_audit_pane_as_the_worker) ... ok
test_restart_worker_passes_manifest_advisor_args_to_claude_worker (test_herdr_agents.HerdrAgentsTest.test_restart_worker_passes_manifest_advisor_args_to_claude_worker) ... ok
test_restart_worker_refuses_to_start_outside_the_seat_when_the_pane_hangs (test_herdr_agents.HerdrAgentsTest.test_restart_worker_refuses_to_start_outside_the_seat_when_the_pane_hangs) ... ok
test_restart_worker_refuses_unmanaged_extra_panes (test_herdr_agents.HerdrAgentsTest.test_restart_worker_refuses_unmanaged_extra_panes) ... ok
test_restart_worker_refuses_when_the_pane_never_reaches_a_shell (test_herdr_agents.HerdrAgentsTest.test_restart_worker_refuses_when_the_pane_never_reaches_a_shell) ... ok
test_restart_worker_relaunches_the_worker_in_its_existing_pane (test_herdr_agents.HerdrAgentsTest.test_restart_worker_relaunches_the_worker_in_its_existing_pane) ... ok
test_restart_worker_repairs_a_legacy_orchestrator_label_on_the_worker_pane (test_herdr_agents.HerdrAgentsTest.test_restart_worker_repairs_a_legacy_orchestrator_label_on_the_worker_pane) ... ok
test_restart_worker_reseats_a_main_path_worker_into_its_worktree (test_herdr_agents.HerdrAgentsTest.test_restart_worker_reseats_a_main_path_worker_into_its_worktree) ... ok
test_restart_worker_waits_for_stale_registration_then_retries_once (test_herdr_agents.HerdrAgentsTest.test_restart_worker_waits_for_stale_registration_then_retries_once) ... ok
test_seat_claim_fails_when_a_later_team_is_held_by_another_session (test_herdr_agents.HerdrAgentsTest.test_seat_claim_fails_when_a_later_team_is_held_by_another_session) ... ok
test_seat_claim_held_by_another_session_fails_without_release (test_herdr_agents.HerdrAgentsTest.test_seat_claim_held_by_another_session_fails_without_release) ... ok
test_seat_claim_keeps_a_same_session_composite_lock_of_a_live_claude (test_herdr_agents.HerdrAgentsTest.test_seat_claim_keeps_a_same_session_composite_lock_of_a_live_claude) ... ok
test_seat_claim_replaces_a_same_session_bare_lock (test_herdr_agents.HerdrAgentsTest.test_seat_claim_replaces_a_same_session_bare_lock) ... ok
test_seat_claim_replaces_a_same_session_composite_lock_of_a_dead_pid (test_herdr_agents.HerdrAgentsTest.test_seat_claim_replaces_a_same_session_composite_lock_of_a_dead_pid) ... ok
test_seat_claim_replaces_a_same_session_composite_lock_of_a_recycled_pid (test_herdr_agents.HerdrAgentsTest.test_seat_claim_replaces_a_same_session_composite_lock_of_a_recycled_pid) ... ok
test_seat_claim_replaces_same_session_bare_locks_in_every_team (test_herdr_agents.HerdrAgentsTest.test_seat_claim_replaces_same_session_bare_locks_in_every_team) ... ok
test_session_start_attach_bounds_a_trickling_hook_payload (test_herdr_agents.HerdrAgentsTest.test_session_start_attach_bounds_a_trickling_hook_payload) ... ok
test_session_start_attach_claims_the_seat_in_a_managed_pane (test_herdr_agents.HerdrAgentsTest.test_session_start_attach_claims_the_seat_in_a_managed_pane) ... ok
test_session_start_attach_claims_when_the_hook_keeps_stdin_open (test_herdr_agents.HerdrAgentsTest.test_session_start_attach_claims_when_the_hook_keeps_stdin_open) ... ok
test_session_start_attach_prints_no_directive_for_a_pane_that_is_not_the_orchestrator (test_herdr_agents.HerdrAgentsTest.test_session_start_attach_prints_no_directive_for_a_pane_that_is_not_the_orchestrator) ... ok
test_session_start_attach_prints_the_regime_directive_with_a_worker_seat (test_herdr_agents.HerdrAgentsTest.test_session_start_attach_prints_the_regime_directive_with_a_worker_seat) ... ok
test_session_start_attach_reads_the_hook_payload_and_herdr_pid (test_herdr_agents.HerdrAgentsTest.test_session_start_attach_reads_the_hook_payload_and_herdr_pid) ... ok
test_session_start_attach_skips_a_pane_that_is_not_the_orchestrator (test_herdr_agents.HerdrAgentsTest.test_session_start_attach_skips_a_pane_that_is_not_the_orchestrator) ... ok
test_start_keeps_node_global_without_mise_tool_install (test_herdr_agents.HerdrAgentsTest.test_start_keeps_node_global_without_mise_tool_install) ... ok
test_start_removes_node_global_agent_clis_shadowing_mise (test_herdr_agents.HerdrAgentsTest.test_start_removes_node_global_agent_clis_shadowing_mise) ... ok
test_start_skips_node_global_removal_without_stray (test_herdr_agents.HerdrAgentsTest.test_start_skips_node_global_removal_without_stray) ... ok
test_successful_agent_start_does_not_poll_agent_list (test_herdr_agents.HerdrAgentsTest.test_successful_agent_start_does_not_poll_agent_list) ... ok
test_two_self_named_pair_workspaces_still_refuse (test_herdr_agents.HerdrAgentsTest.test_two_self_named_pair_workspaces_still_refuse) ... ok
test_uses_initial_workspace_pane_for_claude_and_splits_codex_right (test_herdr_agents.HerdrAgentsTest.test_uses_initial_workspace_pane_for_claude_and_splits_codex_right) ... ok
test_worker_github_pair_env (test_herdr_agents.HerdrAgentsTest.test_worker_github_pair_env) ... ok
test_worker_kind_claude_accepts_a_workspace_trust_dialog (test_herdr_agents.HerdrAgentsTest.test_worker_kind_claude_accepts_a_workspace_trust_dialog) ... ok
test_worker_kind_claude_appends_extra_worker_args (test_herdr_agents.HerdrAgentsTest.test_worker_kind_claude_appends_extra_worker_args) ... ok
test_worker_kind_claude_does_not_require_codex (test_herdr_agents.HerdrAgentsTest.test_worker_kind_claude_does_not_require_codex) ... ok
test_worker_kind_claude_skips_send_keys_without_a_trust_dialog (test_herdr_agents.HerdrAgentsTest.test_worker_kind_claude_skips_send_keys_without_a_trust_dialog) ... ok
test_worker_kind_claude_starts_a_claude_worker_pane_with_profile_args (test_herdr_agents.HerdrAgentsTest.test_worker_kind_claude_starts_a_claude_worker_pane_with_profile_args) ... ok
test_worker_kind_claude_starts_with_no_resolved_args (test_herdr_agents.HerdrAgentsTest.test_worker_kind_claude_starts_with_no_resolved_args) ... ok
test_worker_kind_defaults_to_generated_env_fragment (test_herdr_agents.HerdrAgentsTest.test_worker_kind_defaults_to_generated_env_fragment) ... ok
test_worker_kind_env_override_wins_over_generated_env_fragment (test_herdr_agents.HerdrAgentsTest.test_worker_kind_env_override_wins_over_generated_env_fragment) ... ok
test_worker_kind_rejects_an_unknown_value (test_herdr_agents.HerdrAgentsTest.test_worker_kind_rejects_an_unknown_value) ... ok
test_worker_profile_defaults_to_generated_worker_profile (test_herdr_agents.HerdrAgentsTest.test_worker_profile_defaults_to_generated_worker_profile) ... ok
test_worker_profile_env_override_wins_over_generated_worker_profile (test_herdr_agents.HerdrAgentsTest.test_worker_profile_env_override_wins_over_generated_worker_profile) ... ok
test_worker_seat_ambiguity_leaves_no_worktree_behind (test_herdr_agents.HerdrAgentsTest.test_worker_seat_ambiguity_leaves_no_worktree_behind) ... ok
test_worker_seat_is_skipped_in_a_non_git_directory (test_herdr_agents.HerdrAgentsTest.test_worker_seat_is_skipped_in_a_non_git_directory) ... ok
test_worker_seat_is_skipped_in_an_unregistered_repository (test_herdr_agents.HerdrAgentsTest.test_worker_seat_is_skipped_in_an_unregistered_repository) ... ok
test_worker_seat_is_skipped_outside_a_git_main_checkout (test_herdr_agents.HerdrAgentsTest.test_worker_seat_is_skipped_outside_a_git_main_checkout) ... ok
test_worker_seat_label_comes_from_the_worker_worktree_registration (test_herdr_agents.HerdrAgentsTest.test_worker_seat_label_comes_from_the_worker_worktree_registration) ... ok
test_worker_seat_refuses_a_path_that_is_not_a_worktree (test_herdr_agents.HerdrAgentsTest.test_worker_seat_refuses_a_path_that_is_not_a_worktree) ... ok
test_worker_seat_refuses_an_ambiguous_orchestrator_identity (test_herdr_agents.HerdrAgentsTest.test_worker_seat_refuses_an_ambiguous_orchestrator_identity) ... ok
test_worker_seat_reuses_the_identity_and_hook_already_at_the_worktree (test_herdr_agents.HerdrAgentsTest.test_worker_seat_reuses_the_identity_and_hook_already_at_the_worktree) ... ok
test_yazi_edit_opener_prefers_zed_with_editor_fallback (test_herdr_agents.HerdrAgentsTest.test_yazi_edit_opener_prefers_zed_with_editor_fallback) ... ok
test_zprofile_adds_common_bin_to_login_shell_path (test_herdr_agents.HerdrAgentsTest.test_zprofile_adds_common_bin_to_login_shell_path) ... ok
test_allow_pattern_rejects_shell_chaining (test_permgate.PermgateTest.test_allow_pattern_rejects_shell_chaining) ... ok
test_apply_patch_is_never_deterministically_allowed (test_permgate.PermgateTest.test_apply_patch_is_never_deterministically_allowed) ... ok
test_bash_credentials_fall_through_without_logging_them (test_permgate.PermgateTest.test_bash_credentials_fall_through_without_logging_them) ... ok
test_claude_and_codex_hook_outputs_match_golden_bytes (test_permgate.PermgateTest.test_claude_and_codex_hook_outputs_match_golden_bytes) ... ok
test_git_diff_output_option_is_never_automatically_allowed (test_permgate.PermgateTest.test_git_diff_output_option_is_never_automatically_allowed) ... ok
test_invalid_policy_fields_fail_closed (test_permgate.PermgateTest.test_invalid_policy_fields_fail_closed) ... ok
test_invalid_policy_returns_ask_and_logs_config_error (test_permgate.PermgateTest.test_invalid_policy_returns_ask_and_logs_config_error) ... ok
test_layer_one_allows_documented_claude_and_codex_contracts (test_permgate.PermgateTest.test_layer_one_allows_documented_claude_and_codex_contracts) ... ok
test_layer_one_deny_uses_both_hook_output_schemas (test_permgate.PermgateTest.test_layer_one_deny_uses_both_hook_output_schemas) ... ok
test_log_shape_redacts_command_and_output (test_permgate.PermgateTest.test_log_shape_redacts_command_and_output) ... ok
test_mutating_or_executable_read_options_fall_through (test_permgate.PermgateTest.test_mutating_or_executable_read_options_fall_through) ... ok
test_recursion_sentinel_is_a_complete_no_op (test_permgate.PermgateTest.test_recursion_sentinel_is_a_complete_no_op) ... ok
test_repository_policy_allows_and_falls_through (test_permgate.PermgateTest.test_repository_policy_allows_and_falls_through) ... ok
test_script_named_version_is_not_a_version_check (test_permgate.PermgateTest.test_script_named_version_is_not_a_version_check) ... ok
test_structured_secret_is_redacted_from_the_summary (test_permgate.PermgateTest.test_structured_secret_is_redacted_from_the_summary) ... ok
test_unconstrained_native_reads_fall_through (test_permgate.PermgateTest.test_unconstrained_native_reads_fall_through) ... ok
test_undecided_request_falls_through_to_the_native_prompt (test_permgate.PermgateTest.test_undecided_request_falls_through_to_the_native_prompt) ... ok
test_annotations_keep_every_level_even_on_passing_checks (test_pr_feedback.PrFeedbackTest.test_annotations_keep_every_level_even_on_passing_checks) ... ok
test_bots_are_detected_from_type_login_or_app (test_pr_feedback.PrFeedbackTest.test_bots_are_detected_from_type_login_or_app) ... ok
test_collects_every_feedback_source_for_the_head (test_pr_feedback.PrFeedbackTest.test_collects_every_feedback_source_for_the_head) ... ok
test_collects_the_github_base_with_the_head (test_pr_feedback.PrFeedbackTest.test_collects_the_github_base_with_the_head) ... ok
test_commit_status_keeps_the_latest_state_per_context (test_pr_feedback.PrFeedbackTest.test_commit_status_keeps_the_latest_state_per_context) ... ok
test_every_item_carries_the_disposition_schema (test_pr_feedback.PrFeedbackTest.test_every_item_carries_the_disposition_schema) ... ok
test_gh_never_receives_forced_colour (test_pr_feedback.PrFeedbackTest.test_gh_never_receives_forced_colour) ... ok
test_graphql_strings_are_raw_and_only_integers_are_typed (test_pr_feedback.PrFeedbackTest.test_graphql_strings_are_raw_and_only_integers_are_typed) ... ok
test_main_writes_the_document_to_json (test_pr_feedback.PrFeedbackTest.test_main_writes_the_document_to_json) ... ok
test_only_non_passing_check_runs_become_items (test_pr_feedback.PrFeedbackTest.test_only_non_passing_check_runs_become_items) ... ok
test_review_comments_carry_thread_resolution_across_pages (test_pr_feedback.PrFeedbackTest.test_review_comments_carry_thread_resolution_across_pages) ... ok
test_thread_state_covers_comments_beyond_the_first_page (test_pr_feedback.PrFeedbackTest.test_thread_state_covers_comments_beyond_the_first_page) ... ok
test_unauthenticated_gh_exits_non_zero (test_pr_feedback.PrFeedbackTest.test_unauthenticated_gh_exits_non_zero) ... ok
test_rule_mirrors_and_skills_carry_the_same_requirements (test_pr_feedback.PrIntegrationRuleParityTest.test_rule_mirrors_and_skills_carry_the_same_requirements) ... ok
test_rule_symlink_points_at_the_rule (test_pr_feedback.PrIntegrationRuleParityTest.test_rule_symlink_points_at_the_rule) ... ok
test_bump_writes_only_the_five_pins_through_set_asset (test_release_asset_pins.ReleaseAssetPinsTest.test_bump_writes_only_the_five_pins_through_set_asset) ... ok
test_window_never_moves_a_pin_backwards (test_release_asset_pins.ReleaseAssetPinsTest.test_window_never_moves_a_pin_backwards) ... ok
test_window_rejects_an_unknown_current_pin (test_release_asset_pins.ReleaseAssetPinsTest.test_window_rejects_an_unknown_current_pin) ... ok
test_window_skips_a_young_release_and_takes_an_older_one (test_release_asset_pins.ReleaseAssetPinsTest.test_window_skips_a_young_release_and_takes_an_older_one) ... ok
test_all_paths_are_preflighted_before_any_deletion (test_remove_agent_asset.RemoveAgentAssetTest.test_all_paths_are_preflighted_before_any_deletion) ... ok
test_brew_refuses_ambiguous_formula (test_remove_agent_asset.RemoveAgentAssetTest.test_brew_refuses_ambiguous_formula) ... ok
test_brew_uses_uninstall_for_unambiguous_formula (test_remove_agent_asset.RemoveAgentAssetTest.test_brew_uses_uninstall_for_unambiguous_formula) ... ok
test_crit_plugin_falls_back_to_data_path_but_not_config (test_remove_agent_asset.RemoveAgentAssetTest.test_crit_plugin_falls_back_to_data_path_but_not_config) ... ok
test_default_and_explicit_dry_run_print_without_mutating (test_remove_agent_asset.RemoveAgentAssetTest.test_default_and_explicit_dry_run_print_without_mutating) ... ok
test_integration_uses_verified_herdr_uninstall (test_remove_agent_asset.RemoveAgentAssetTest.test_integration_uses_verified_herdr_uninstall) ... ok
test_invalid_manifest_is_rejected (test_remove_agent_asset.RemoveAgentAssetTest.test_invalid_manifest_is_rejected) ... ok
test_parameterized_step_removal_preserves_sibling_identity (test_remove_agent_asset.RemoveAgentAssetTest.test_parameterized_step_removal_preserves_sibling_identity) ... ok
test_plugin_uses_verified_claude_uninstall (test_remove_agent_asset.RemoveAgentAssetTest.test_plugin_uses_verified_claude_uninstall) ... ok
test_plugin_uses_verified_codex_remove (test_remove_agent_asset.RemoveAgentAssetTest.test_plugin_uses_verified_codex_remove) ... ok
test_recorded_symlink_is_removed_without_following_target (test_remove_agent_asset.RemoveAgentAssetTest.test_recorded_symlink_is_removed_without_following_target) ... ok
test_tampered_manifest_outside_safe_roots_is_refused (test_remove_agent_asset.RemoveAgentAssetTest.test_tampered_manifest_outside_safe_roots_is_refused) ... ok
test_unknown_step_lists_known_steps_without_guessing (test_remove_agent_asset.RemoveAgentAssetTest.test_unknown_step_lists_known_steps_without_guessing) ... ok
test_yes_removes_only_recorded_path_and_preserves_other_steps (test_remove_agent_asset.RemoveAgentAssetTest.test_yes_removes_only_recorded_path_and_preserves_other_steps) ... ok
test_advanced_base_cannot_delete_collector_to_trigger_head_fallback (test_require_crit_review.ReviewGuardTest.test_advanced_base_cannot_delete_collector_to_trigger_head_fallback) ... ok
test_advanced_base_cannot_supply_an_untrusted_collector (test_require_crit_review.ReviewGuardTest.test_advanced_base_cannot_supply_an_untrusted_collector) ... ok
test_agent_lifecycle_script_change_requires_review (test_require_crit_review.ReviewGuardTest.test_agent_lifecycle_script_change_requires_review) ... ok
test_agent_lifecycle_surfaces_require_review (test_require_crit_review.ReviewGuardTest.test_agent_lifecycle_surfaces_require_review) ... ok
test_agent_lifecycle_tokens_require_review (test_require_crit_review.ReviewGuardTest.test_agent_lifecycle_tokens_require_review) ... ok
test_agent_reviewer_rejects_empty_or_malformed_crit_data (test_require_crit_review.ReviewGuardTest.test_agent_reviewer_rejects_empty_or_malformed_crit_data) ... ok
test_agent_reviewer_rejects_invalid_review_outcome (test_require_crit_review.ReviewGuardTest.test_agent_reviewer_rejects_invalid_review_outcome) ... ok
test_agent_reviewer_with_command_string_source_still_requires_review (test_require_crit_review.ReviewGuardTest.test_agent_reviewer_with_command_string_source_still_requires_review) ... ok
test_agent_reviewer_with_crit_data_satisfies_required_review (test_require_crit_review.ReviewGuardTest.test_agent_reviewer_with_crit_data_satisfies_required_review) ... ok
test_agent_reviewer_with_crit_reviewed_marker_still_requires_review (test_require_crit_review.ReviewGuardTest.test_agent_reviewer_with_crit_reviewed_marker_still_requires_review) ... ok
test_agent_reviewer_with_external_crit_json_still_requires_review (test_require_crit_review.ReviewGuardTest.test_agent_reviewer_with_external_crit_json_still_requires_review) ... ok
test_agent_reviewer_with_non_review_crit_json_object_still_requires_review (test_require_crit_review.ReviewGuardTest.test_agent_reviewer_with_non_review_crit_json_object_still_requires_review) ... ok
test_agent_reviewer_with_resolved_line_comment_satisfies_required_review (test_require_crit_review.ReviewGuardTest.test_agent_reviewer_with_resolved_line_comment_satisfies_required_review) ... ok
test_agent_reviewer_with_unresolved_crit_json_still_requires_review (test_require_crit_review.ReviewGuardTest.test_agent_reviewer_with_unresolved_crit_json_still_requires_review) ... ok
test_agent_self_review_flag_evidence_still_requires_review (test_require_crit_review.ReviewGuardTest.test_agent_self_review_flag_evidence_still_requires_review) ... ok
test_agent_self_reviewer_evidence_still_requires_review (test_require_crit_review.ReviewGuardTest.test_agent_self_reviewer_evidence_still_requires_review) ... ok
test_audit_must_name_head_and_live_under_validation (test_require_crit_review.ReviewGuardTest.test_audit_must_name_head_and_live_under_validation) ... ok
test_base_accepts_a_correct_audit_of_head (test_require_crit_review.ReviewGuardTest.test_base_accepts_a_correct_audit_of_head) ... ok
test_base_accepts_exact_and_advanced_base_with_unchanged_merge_base (test_require_crit_review.ReviewGuardTest.test_base_accepts_exact_and_advanced_base_with_unchanged_merge_base) ... ok
test_base_fails_closed_when_github_metadata_is_unavailable (test_require_crit_review.ReviewGuardTest.test_base_fails_closed_when_github_metadata_is_unavailable) ... ok
test_base_fails_closed_when_unresolvable_or_option_like (test_require_crit_review.ReviewGuardTest.test_base_fails_closed_when_unresolvable_or_option_like) ... ok
test_base_rejects_forged_evidence_metadata (test_require_crit_review.ReviewGuardTest.test_base_rejects_forged_evidence_metadata) ... ok
test_base_rejects_pr_commits_before_executing_their_collector (test_require_crit_review.ReviewGuardTest.test_base_rejects_pr_commits_before_executing_their_collector) ... ok
test_base_rejects_side_branch_and_advanced_base_containing_pr_commits (test_require_crit_review.ReviewGuardTest.test_base_rejects_side_branch_and_advanced_base_containing_pr_commits) ... ok
test_base_requires_audit_evidence_for_a_reviewed_change (test_require_crit_review.ReviewGuardTest.test_base_requires_audit_evidence_for_a_reviewed_change) ... ok
test_base_requires_pr_feedback_evidence (test_require_crit_review.ReviewGuardTest.test_base_requires_pr_feedback_evidence) ... ok
test_base_reviews_committed_branch_changes (test_require_crit_review.ReviewGuardTest.test_base_reviews_committed_branch_changes) ... ok
test_blocked_or_missing_audit_verdict_fails (test_require_crit_review.ReviewGuardTest.test_blocked_or_missing_audit_verdict_fails) ... ok
test_broad_diff_requires_review (test_require_crit_review.ReviewGuardTest.test_broad_diff_requires_review) ... ok
test_broad_orchestration_only_pr_needs_no_audit (test_require_crit_review.ReviewGuardTest.test_broad_orchestration_only_pr_needs_no_audit) ... ok
test_companion_must_be_this_audits_own_last_message (test_require_crit_review.ReviewGuardTest.test_companion_must_be_this_audits_own_last_message) ... ok
test_explicit_disable_skips_guard (test_require_crit_review.ReviewGuardTest.test_explicit_disable_skips_guard) ... ok
test_feedback_accepts_absolute_path_through_a_repository_parent_alias (test_require_crit_review.ReviewGuardTest.test_feedback_accepts_absolute_path_through_a_repository_parent_alias) ... ok
test_feedback_cannot_hide_an_arbitrary_path_without_base (test_require_crit_review.ReviewGuardTest.test_feedback_cannot_hide_an_arbitrary_path_without_base) ... ok
test_feedback_does_not_exclude_symlink_aliases_outside_validation (test_require_crit_review.ReviewGuardTest.test_feedback_does_not_exclude_symlink_aliases_outside_validation) ... ok
test_feedback_path_itself_must_be_under_validation (test_require_crit_review.ReviewGuardTest.test_feedback_path_itself_must_be_under_validation) ... ok
test_feedback_symlink_cannot_hide_a_file_outside_validation (test_require_crit_review.ReviewGuardTest.test_feedback_symlink_cannot_hide_a_file_outside_validation) ... ok
test_fixed_commit_is_checked_against_github_base_not_an_older_side_parent (test_require_crit_review.ReviewGuardTest.test_fixed_commit_is_checked_against_github_base_not_an_older_side_parent) ... ok
test_github_identity_gate_activation_and_current_head_approval (test_require_crit_review.ReviewGuardTest.test_github_identity_gate_activation_and_current_head_approval) ... ok
test_github_lookup_ignores_environment_repository_override (test_require_crit_review.ReviewGuardTest.test_github_lookup_ignores_environment_repository_override) ... ok
test_github_lookup_rejects_evidence_from_another_repository (test_require_crit_review.ReviewGuardTest.test_github_lookup_rejects_evidence_from_another_repository) ... ok
test_high_risk_markdown_change_requires_review (test_require_crit_review.ReviewGuardTest.test_high_risk_markdown_change_requires_review) ... ok
test_incorrect_audit_needs_not_applicable_dispositions (test_require_crit_review.ReviewGuardTest.test_incorrect_audit_needs_not_applicable_dispositions) ... ok
test_incorrect_audit_without_findings_fails (test_require_crit_review.ReviewGuardTest.test_incorrect_audit_without_findings_fails) ... ok
test_large_untracked_file_requires_broad_diff_review (test_require_crit_review.ReviewGuardTest.test_large_untracked_file_requires_broad_diff_review) ... ok
test_missing_base_collector_falls_back_only_after_binding (test_require_crit_review.ReviewGuardTest.test_missing_base_collector_falls_back_only_after_binding) ... ok
test_native_reviewed_environment_rejects_human_reviewer (test_require_crit_review.ReviewGuardTest.test_native_reviewed_environment_rejects_human_reviewer) ... ok
test_native_reviewed_without_evidence_still_requires_review (test_require_crit_review.ReviewGuardTest.test_native_reviewed_without_evidence_still_requires_review) ... ok
test_no_diff_does_not_require_review (test_require_crit_review.ReviewGuardTest.test_no_diff_does_not_require_review) ... ok
test_older_base_must_not_be_on_the_head_first_parent_chain (test_require_crit_review.ReviewGuardTest.test_older_base_must_not_be_on_the_head_first_parent_chain) ... ok
test_orchestration_only_pr_needs_no_audit (test_require_crit_review.ReviewGuardTest.test_orchestration_only_pr_needs_no_audit) ... ok
test_pr_feedback_accepts_complete_evidence_without_a_bot_review (test_require_crit_review.ReviewGuardTest.test_pr_feedback_accepts_complete_evidence_without_a_bot_review) ... ok
test_pr_feedback_accepts_complete_root_cause_dispositions (test_require_crit_review.ReviewGuardTest.test_pr_feedback_accepts_complete_root_cause_dispositions) ... ok
test_pr_feedback_bodies_are_compared_after_secret_masking (test_require_crit_review.ReviewGuardTest.test_pr_feedback_bodies_are_compared_after_secret_masking) ... ok
test_pr_feedback_evidence_file_is_not_counted_as_a_change (test_require_crit_review.ReviewGuardTest.test_pr_feedback_evidence_file_is_not_counted_as_a_change) ... ok
test_pr_feedback_fails_when_the_collector_cannot_run (test_require_crit_review.ReviewGuardTest.test_pr_feedback_fails_when_the_collector_cannot_run) ... ok
test_pr_feedback_fixed_commit_must_be_in_the_pr_range (test_require_crit_review.ReviewGuardTest.test_pr_feedback_fixed_commit_must_be_in_the_pr_range) ... ok
test_pr_feedback_matches_a_masked_path_but_not_an_edited_one (test_require_crit_review.ReviewGuardTest.test_pr_feedback_matches_a_masked_path_but_not_an_edited_one) ... ok
test_pr_feedback_must_be_collected_for_the_current_head (test_require_crit_review.ReviewGuardTest.test_pr_feedback_must_be_collected_for_the_current_head) ... ok
test_pr_feedback_must_cover_every_currently_collected_item (test_require_crit_review.ReviewGuardTest.test_pr_feedback_must_cover_every_currently_collected_item) ... ok
test_pr_feedback_rejects_evidence_outside_the_repository (test_require_crit_review.ReviewGuardTest.test_pr_feedback_rejects_evidence_outside_the_repository) ... ok
test_pr_feedback_rejects_incomplete_or_invalid_dispositions (test_require_crit_review.ReviewGuardTest.test_pr_feedback_rejects_incomplete_or_invalid_dispositions) ... ok
test_pr_feedback_requires_the_github_head_to_match (test_require_crit_review.ReviewGuardTest.test_pr_feedback_requires_the_github_head_to_match) ... ok
test_pr_feedback_uses_the_base_collector_not_the_prs_own (test_require_crit_review.ReviewGuardTest.test_pr_feedback_uses_the_base_collector_not_the_prs_own) ... ok
test_pr_feedback_without_base_is_only_format_checked (test_require_crit_review.ReviewGuardTest.test_pr_feedback_without_base_is_only_format_checked) ... ok
test_recollection_must_match_the_authenticated_repository (test_require_crit_review.ReviewGuardTest.test_recollection_must_match_the_authenticated_repository) ... ok
test_reviewed_environment_satisfies_required_review (test_require_crit_review.ReviewGuardTest.test_reviewed_environment_satisfies_required_review) ... ok
test_reviewed_with_blank_evidence_values_still_requires_review (test_require_crit_review.ReviewGuardTest.test_reviewed_with_blank_evidence_values_still_requires_review) ... ok
test_reviewed_with_incomplete_evidence_still_requires_review (test_require_crit_review.ReviewGuardTest.test_reviewed_with_incomplete_evidence_still_requires_review) ... ok
test_small_docs_only_change_does_not_require_review (test_require_crit_review.ReviewGuardTest.test_small_docs_only_change_does_not_require_review) ... ok
test_verdict_comes_only_from_the_last_message_file (test_require_crit_review.ReviewGuardTest.test_verdict_comes_only_from_the_last_message_file) ... ok
test_agent_asset_update_removes_node_global_shadows_before_agent_commands (test_runtime_health.RuntimeHealthTest.test_agent_asset_update_removes_node_global_shadows_before_agent_commands) ... ok
test_agent_asset_update_repairs_broken_claude_with_npm_backend (test_runtime_health.RuntimeHealthTest.test_agent_asset_update_repairs_broken_claude_with_npm_backend) ... ok
test_agent_asset_update_runs_gh_extension_ensure (test_runtime_health.RuntimeHealthTest.test_agent_asset_update_runs_gh_extension_ensure) ... ok
test_agent_launchers_do_not_hardcode_model_ids (test_runtime_health.RuntimeHealthTest.test_agent_launchers_do_not_hardcode_model_ids) ... ok
test_agmsg_accepts_a_store_the_installer_creates_and_notes_run_changes (test_runtime_health.RuntimeHealthTest.test_agmsg_accepts_a_store_the_installer_creates_and_notes_run_changes) ... ok
test_agmsg_already_pinned_skips_download (test_runtime_health.RuntimeHealthTest.test_agmsg_already_pinned_skips_download) ... ok
test_agmsg_checksum_mismatch_fails_closed (test_runtime_health.RuntimeHealthTest.test_agmsg_checksum_mismatch_fails_closed) ... ok
test_agmsg_fresh_install_populates_skill_and_records_manifest (test_runtime_health.RuntimeHealthTest.test_agmsg_fresh_install_populates_skill_and_records_manifest) ... ok
test_agmsg_migrates_marker_less_legacy_dir_without_losing_live_state (test_runtime_health.RuntimeHealthTest.test_agmsg_migrates_marker_less_legacy_dir_without_losing_live_state) ... ok
test_agmsg_migration_reports_an_installer_that_mutates_live_state (test_runtime_health.RuntimeHealthTest.test_agmsg_migration_reports_an_installer_that_mutates_live_state) ... ok
test_agmsg_refuses_to_install_when_the_state_snapshot_is_empty (test_runtime_health.RuntimeHealthTest.test_agmsg_refuses_to_install_when_the_state_snapshot_is_empty) ... ok
test_agmsg_refuses_to_install_without_tar (test_runtime_health.RuntimeHealthTest.test_agmsg_refuses_to_install_without_tar) ... ok
test_agmsg_reports_an_installer_that_leaves_the_wrong_version (test_runtime_health.RuntimeHealthTest.test_agmsg_reports_an_installer_that_leaves_the_wrong_version) ... ok
test_agmsg_update_aborts_when_install_corrupts_live_state (test_runtime_health.RuntimeHealthTest.test_agmsg_update_aborts_when_install_corrupts_live_state) ... ok
test_agmsg_update_never_touches_teams_db_run (test_runtime_health.RuntimeHealthTest.test_agmsg_update_never_touches_teams_db_run) ... ok
test_client_bashrc_treats_private_sources_as_optional (test_runtime_health.RuntimeHealthTest.test_client_bashrc_treats_private_sources_as_optional) ... ok
test_codex_crit_normalizes_managed_marketplace_mode (test_runtime_health.RuntimeHealthTest.test_codex_crit_normalizes_managed_marketplace_mode) ... ok
test_codex_superpowers_reports_login_step_when_curated_catalog_is_missing (test_runtime_health.RuntimeHealthTest.test_codex_superpowers_reports_login_step_when_curated_catalog_is_missing) ... ok
test_darwin_crit_checksum_failure_preserves_existing_binary (test_runtime_health.RuntimeHealthTest.test_darwin_crit_checksum_failure_preserves_existing_binary) ... ok
test_darwin_crit_install_is_pinned_atomic_and_recorded (test_runtime_health.RuntimeHealthTest.test_darwin_crit_install_is_pinned_atomic_and_recorded) ... ok
test_doctor_github_role_activation_and_file_storage (test_runtime_health.RuntimeHealthTest.test_doctor_github_role_activation_and_file_storage) ... ok
test_doctor_reports_claude_sandbox_prerequisites (test_runtime_health.RuntimeHealthTest.test_doctor_reports_claude_sandbox_prerequisites) ... ok
test_doctor_required_optional_and_healthy_statuses (test_runtime_health.RuntimeHealthTest.test_doctor_required_optional_and_healthy_statuses) ... ok
test_linux_crit_checksum_failure_preserves_existing_binary (test_runtime_health.RuntimeHealthTest.test_linux_crit_checksum_failure_preserves_existing_binary) ... ok
test_linux_crit_correct_version_is_download_free (test_runtime_health.RuntimeHealthTest.test_linux_crit_correct_version_is_download_free) ... ok
test_linux_crit_failure_does_not_leak_cleanup_trap (test_runtime_health.RuntimeHealthTest.test_linux_crit_failure_does_not_leak_cleanup_trap) ... ok
test_linux_crit_install_is_pinned_atomic_and_recorded (test_runtime_health.RuntimeHealthTest.test_linux_crit_install_is_pinned_atomic_and_recorded) ... ok
test_linux_crit_prefers_pinned_target_over_older_path_binary (test_runtime_health.RuntimeHealthTest.test_linux_crit_prefers_pinned_target_over_older_path_binary) ... ok
test_make_doctor_does_not_skip_runtime_check_when_deployed_root_is_missing (test_runtime_health.RuntimeHealthTest.test_make_doctor_does_not_skip_runtime_check_when_deployed_root_is_missing) ... ok
test_make_doctor_passes_repair_variable_to_runtime_check (test_runtime_health.RuntimeHealthTest.test_make_doctor_passes_repair_variable_to_runtime_check) ... ok
test_make_doctor_propagates_runtime_drift_after_tool_checks (test_runtime_health.RuntimeHealthTest.test_make_doctor_propagates_runtime_drift_after_tool_checks) ... ok
test_make_update_pulls_clean_main_before_apply (test_runtime_health.RuntimeHealthTest.test_make_update_pulls_clean_main_before_apply) ... ok
test_make_update_reports_unmerged_feature_branch_before_branch_notice (test_runtime_health.RuntimeHealthTest.test_make_update_reports_unmerged_feature_branch_before_branch_notice) ... ok
test_make_update_reports_unmerged_index_before_dirty_notice (test_runtime_health.RuntimeHealthTest.test_make_update_reports_unmerged_index_before_dirty_notice) ... ok
test_make_update_skips_dirty_main_with_manual_pull_notice (test_runtime_health.RuntimeHealthTest.test_make_update_skips_dirty_main_with_manual_pull_notice) ... ok
test_upgrade_applies_mise_only_from_successful_canonical_checkout (test_runtime_health.RuntimeHealthTest.test_upgrade_applies_mise_only_from_successful_canonical_checkout) ... ok
test_upgrade_bumps_terminal_and_crit_pins_from_fetched_artifacts (test_runtime_health.RuntimeHealthTest.test_upgrade_bumps_terminal_and_crit_pins_from_fetched_artifacts) ... ok
test_upgrade_changes_checkout_not_live_mise_symlink_target (test_runtime_health.RuntimeHealthTest.test_upgrade_changes_checkout_not_live_mise_symlink_target) ... ok
test_upgrade_github_extensions_are_warning_only (test_runtime_health.RuntimeHealthTest.test_upgrade_github_extensions_are_warning_only) ... ok
test_upgrade_required_failures_are_nonzero_and_independent (test_runtime_health.RuntimeHealthTest.test_upgrade_required_failures_are_nonzero_and_independent) ... ok
test_upgrade_self_updates_mise_to_the_manifest_pin (test_runtime_health.RuntimeHealthTest.test_upgrade_self_updates_mise_to_the_manifest_pin) ... ok
test_upgrade_skips_unavailable_mise_self_update (test_runtime_health.RuntimeHealthTest.test_upgrade_skips_unavailable_mise_self_update) ... ok
test_upgrade_uses_current_mise_node_after_runtime_replacement (test_runtime_health.RuntimeHealthTest.test_upgrade_uses_current_mise_node_after_runtime_replacement)
Reject ambient npm after mise replaces the active Node runtime. ... ok
test_ci_smokes_exact_tools_with_network_denied (test_statusline_tools.StatuslineToolsTest.test_ci_smokes_exact_tools_with_network_denied) ... ok
test_direct_commands_use_offline_path_binaries (test_statusline_tools.StatuslineToolsTest.test_direct_commands_use_offline_path_binaries) ... ok
test_generated_commands_are_direct_and_static (test_statusline_tools.StatuslineToolsTest.test_generated_commands_are_direct_and_static) ... ok
test_mise_config_and_lock_pin_exact_npm_versions (test_statusline_tools.StatuslineToolsTest.test_mise_config_and_lock_pin_exact_npm_versions) ... ok
test_missing_binary_fails_immediately (test_statusline_tools.StatuslineToolsTest.test_missing_binary_fails_immediately) ... ok
test_binary_installers_replace_from_same_directory_stages (test_supply_chain_policy.SupplyChainPolicyTest.test_binary_installers_replace_from_same_directory_stages) ... ok
test_executable_downloads_are_verified_and_not_piped_to_shell (test_supply_chain_policy.SupplyChainPolicyTest.test_executable_downloads_are_verified_and_not_piped_to_shell) ... ok
test_external_checksum_failure_preserves_destination (test_supply_chain_policy.SupplyChainPolicyTest.test_external_checksum_failure_preserves_destination) ... ok
test_externals_render_without_network_discovery (test_supply_chain_policy.SupplyChainPolicyTest.test_externals_render_without_network_discovery) ... ok
test_externals_use_fixed_urls_and_checksums (test_supply_chain_policy.SupplyChainPolicyTest.test_externals_use_fixed_urls_and_checksums) ... ok
test_installer_cleanup_preserves_failure_status (test_supply_chain_policy.SupplyChainPolicyTest.test_installer_cleanup_preserves_failure_status) ... ok
test_installer_cleanup_survives_mock_function_returns (test_supply_chain_policy.SupplyChainPolicyTest.test_installer_cleanup_survives_mock_function_returns) ... ok
test_mise_apply_replaces_live_symlinks_with_independent_copies (test_supply_chain_policy.SupplyChainPolicyTest.test_mise_apply_replaces_live_symlinks_with_independent_copies) ... ok
test_mise_lock_matches_config_and_supported_platforms (test_supply_chain_policy.SupplyChainPolicyTest.test_mise_lock_matches_config_and_supported_platforms) ... ok
test_mise_lock_url_entries_have_checksums (test_supply_chain_policy.SupplyChainPolicyTest.test_mise_lock_url_entries_have_checksums) ... ok
test_mise_main_preserves_install_failure (test_supply_chain_policy.SupplyChainPolicyTest.test_mise_main_preserves_install_failure) ... ok
test_mise_npm_backend_uses_npm_and_limits_lifecycle_scripts (test_supply_chain_policy.SupplyChainPolicyTest.test_mise_npm_backend_uses_npm_and_limits_lifecycle_scripts) ... ok
test_mise_versions_are_exact_and_locking_is_enforced (test_supply_chain_policy.SupplyChainPolicyTest.test_mise_versions_are_exact_and_locking_is_enforced) ... ok
test_renovate_owns_dependency_update_notifications (test_supply_chain_policy.SupplyChainPolicyTest.test_renovate_owns_dependency_update_notifications) ... ok
test_setup_ci_rejects_and_preserves_local_drift (test_supply_chain_policy.SupplyChainPolicyTest.test_setup_ci_rejects_and_preserves_local_drift) ... ok
test_sheldon_git_sources_have_revisions (test_supply_chain_policy.SupplyChainPolicyTest.test_sheldon_git_sources_have_revisions) ... ok
test_sheldon_uses_locked_crates_io_source (test_supply_chain_policy.SupplyChainPolicyTest.test_sheldon_uses_locked_crates_io_source) ... ok
test_absent_path_without_old_ref_is_regression (test_ua_symbol_coverage.UaSymbolCoverageTest.test_absent_path_without_old_ref_is_regression) ... ok
test_chmod_only_change_keeps_the_source_unchanged_note (test_ua_symbol_coverage.UaSymbolCoverageTest.test_chmod_only_change_keeps_the_source_unchanged_note) ... ok
test_comment_lines_are_not_definitions (test_ua_symbol_coverage.UaSymbolCoverageTest.test_comment_lines_are_not_definitions) ... ok
test_def_column_reads_the_new_graph_revision (test_ua_symbol_coverage.UaSymbolCoverageTest.test_def_column_reads_the_new_graph_revision) ... ok
test_deleted_path_with_old_ref_is_explained (test_ua_symbol_coverage.UaSymbolCoverageTest.test_deleted_path_with_old_ref_is_explained) ... ok
test_flags_unexplained_symbol_loss_only (test_ua_symbol_coverage.UaSymbolCoverageTest.test_flags_unexplained_symbol_loss_only) ... ok
test_grammar_file_missing_from_graph_fails_in_covered_directories (test_ua_symbol_coverage.UaSymbolCoverageTest.test_grammar_file_missing_from_graph_fails_in_covered_directories) ... ok
test_low_similarity_move_with_no_symbols_is_regression (test_ua_symbol_coverage.UaSymbolCoverageTest.test_low_similarity_move_with_no_symbols_is_regression) ... ok
test_partial_deletion_in_changed_source_is_regression (test_ua_symbol_coverage.UaSymbolCoverageTest.test_partial_deletion_in_changed_source_is_regression) ... ok
test_partially_covered_new_file_is_not_flagged (test_ua_symbol_coverage.UaSymbolCoverageTest.test_partially_covered_new_file_is_not_flagged) ... ok
test_python_defs_inside_strings_do_not_count (test_ua_symbol_coverage.UaSymbolCoverageTest.test_python_defs_inside_strings_do_not_count) ... ok
test_rename_dropping_symbols_is_regression (test_ua_symbol_coverage.UaSymbolCoverageTest.test_rename_dropping_symbols_is_regression) ... ok
test_rename_preserving_symbols_is_ok (test_ua_symbol_coverage.UaSymbolCoverageTest.test_rename_preserving_symbols_is_ok) ... ok
test_ruby_visibility_prefixed_defs_are_counted (test_ua_symbol_coverage.UaSymbolCoverageTest.test_ruby_visibility_prefixed_defs_are_counted) ... ok
test_shell_names_with_punctuation_are_counted (test_ua_symbol_coverage.UaSymbolCoverageTest.test_shell_names_with_punctuation_are_counted) ... ok
test_unchanged_source_loss_is_noted (test_ua_symbol_coverage.UaSymbolCoverageTest.test_unchanged_source_loss_is_noted) ... ok
test_unreadable_candidate_fails_closed (test_ua_symbol_coverage.UaSymbolCoverageTest.test_unreadable_candidate_fails_closed) ... ok
test_unresolvable_ref_fails_closed (test_ua_symbol_coverage.UaSymbolCoverageTest.test_unresolvable_ref_fails_closed) ... ok
test_uv_run_script_shebang_is_python (test_ua_symbol_coverage.UaSymbolCoverageTest.test_uv_run_script_shebang_is_python) ... ok
test_builds_in_the_clone_when_no_release_artifact_exists (test_update_agent_assets_ua_core.UnderstandAnythingCoreBuildTest.test_builds_in_the_clone_when_no_release_artifact_exists) ... ok
test_builds_missing_core_in_the_release_artifact_then_copies_it (test_update_agent_assets_ua_core.UnderstandAnythingCoreBuildTest.test_builds_missing_core_in_the_release_artifact_then_copies_it) ... ok
test_doctor_stale_warning_is_cleared_by_the_update_build (test_update_agent_assets_ua_core.UnderstandAnythingCoreBuildTest.test_doctor_stale_warning_is_cleared_by_the_update_build) ... ok
test_frozen_install_failure_falls_back_to_plain_install (test_update_agent_assets_ua_core.UnderstandAnythingCoreBuildTest.test_frozen_install_failure_falls_back_to_plain_install) ... ok
test_make_update_installs_the_pinned_pnpm (test_update_agent_assets_ua_core.UnderstandAnythingCoreBuildTest.test_make_update_installs_the_pinned_pnpm) ... ok
test_prefers_mise_exec_over_an_unbacked_pnpm_shim (test_update_agent_assets_ua_core.UnderstandAnythingCoreBuildTest.test_prefers_mise_exec_over_an_unbacked_pnpm_shim) ... ok
test_rebuilds_a_release_dist_older_than_its_sources (test_update_agent_assets_ua_core.UnderstandAnythingCoreBuildTest.test_rebuilds_a_release_dist_older_than_its_sources) ... ok
test_skips_the_build_when_the_release_artifact_already_has_dist (test_update_agent_assets_ua_core.UnderstandAnythingCoreBuildTest.test_skips_the_build_when_the_release_artifact_already_has_dist) ... ok
test_uses_mise_exec_when_pnpm_is_not_on_path (test_update_agent_assets_ua_core.UnderstandAnythingCoreBuildTest.test_uses_mise_exec_when_pnpm_is_not_on_path) ... ok
test_uses_path_pnpm_only_when_mise_is_absent (test_update_agent_assets_ua_core.UnderstandAnythingCoreBuildTest.test_uses_path_pnpm_only_when_mise_is_absent) ... ok
test_warns_and_continues_when_no_pnpm_is_resolvable (test_update_agent_assets_ua_core.UnderstandAnythingCoreBuildTest.test_warns_and_continues_when_no_pnpm_is_resolvable) ... ok
test_warns_and_continues_when_the_build_fails (test_update_agent_assets_ua_core.UnderstandAnythingCoreBuildTest.test_warns_and_continues_when_the_build_fails) ... ok
test_candidate_is_no_when_another_claude_family_is_larger (test_usage_review.UsageReviewTests.test_candidate_is_no_when_another_claude_family_is_larger) ... ok
test_malformed_latest_snapshot_warns_and_never_raises (test_usage_review.UsageReviewTests.test_malformed_latest_snapshot_warns_and_never_raises) ... ok
test_report_computes_share_ratio_and_baseline_deltas (test_usage_review.UsageReviewTests.test_report_computes_share_ratio_and_baseline_deltas) ... ok
test_report_emits_due_windows_and_matching_notes_suppress_them (test_usage_review.UsageReviewTests.test_report_emits_due_windows_and_matching_notes_suppress_them) ... ok
test_snapshot_does_not_rewrite_existing_daily_file (test_usage_review.UsageReviewTests.test_snapshot_does_not_rewrite_existing_daily_file) ... ok
test_a_masked_key_collision_fails_and_leaves_the_file_unchanged (test_validate_agent_assets.MaskSecretsModeTest.test_a_masked_key_collision_fails_and_leaves_the_file_unchanged) ... ok
test_leaves_allowed_placeholders_the_scan_accepts (test_validate_agent_assets.MaskSecretsModeTest.test_leaves_allowed_placeholders_the_scan_accepts) ... ok
test_masks_an_earlier_duplicate_member_so_the_scan_passes (test_validate_agent_assets.MaskSecretsModeTest.test_masks_an_earlier_duplicate_member_so_the_scan_passes) ... ok
test_masks_every_match_in_place_and_reports_counts (test_validate_agent_assets.MaskSecretsModeTest.test_masks_every_match_in_place_and_reports_counts) ... ok
test_masks_json_string_values_and_keeps_the_document_parseable (test_validate_agent_assets.MaskSecretsModeTest.test_masks_json_string_values_and_keeps_the_document_parseable) ... ok
test_missing_file_exits_2_without_touching_others (test_validate_agent_assets.MaskSecretsModeTest.test_missing_file_exits_2_without_touching_others) ... ok
test_a_key_after_json_escaped_whitespace_is_flagged (test_validate_agent_assets.SecretPatternBoundaryTest.test_a_key_after_json_escaped_whitespace_is_flagged) ... ok
test_a_key_prefix_inside_a_hyphenated_word_is_clean (test_validate_agent_assets.SecretPatternBoundaryTest.test_a_key_prefix_inside_a_hyphenated_word_is_clean) ... ok
test_a_long_hyphenated_run_scans_in_linear_time (test_validate_agent_assets.SecretPatternBoundaryTest.test_a_long_hyphenated_run_scans_in_linear_time) ... ok
test_a_real_key_prefix_is_still_flagged (test_validate_agent_assets.SecretPatternBoundaryTest.test_a_real_key_prefix_is_still_flagged) ... ok
test_an_sk_key_body_needs_a_hyphen_free_run (test_validate_agent_assets.SecretPatternBoundaryTest.test_an_sk_key_body_needs_a_hyphen_free_run) ... <frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8f032d40>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8f0332e0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8ed05a80>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8ed058a0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8ed04f40>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8ed06890>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8ed073d0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8ed05120>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8ed06c50>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8ed05030>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8ed04a90>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8f0335b0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8ed05300>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8ef65c60>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8ed072e0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8ed04c70>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8ed05210>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8ed04b80>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8e9ed120>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8e9ed3f0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8e9ed030>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8e9ece50>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8e9ecd60>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8e9ec040>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8e9ecc70>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8e9ecb80>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8e9ec130>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8e9ec310>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8e9ec8b0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8e9ec400>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8e9ec220>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8e9eca90>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8e9ed5d0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8e9ed6c0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8e9ed990>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8e9edc60>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8e9edd50>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8e9ede40>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8e9edf30>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8e9ee020>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8e9ee110>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8e9ee200>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8e9ee2f0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xffba8e9ee3e0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
ok
test_masking_keeps_the_escape_before_the_key (test_validate_agent_assets.SecretPatternBoundaryTest.test_masking_keeps_the_escape_before_the_key) ... ok
test_agent_manifest_accepts_a_worker_worktree_under_claude_worktrees (test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_accepts_a_worker_worktree_under_claude_worktrees) ... ok
test_agent_manifest_accepts_exact_security_profile_set (test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_accepts_exact_security_profile_set) ... ok
test_agent_manifest_pins_the_audit_codex_profile (test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_pins_the_audit_codex_profile) ... ok
test_agent_manifest_rejects_a_worker_worktree_outside_claude_worktrees (test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_a_worker_worktree_outside_claude_worktrees) ... ok
test_agent_manifest_rejects_invalid_or_missing_worker_kind (test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_invalid_or_missing_worker_kind) ... ok
test_agent_manifest_rejects_missing_audit_profile (test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_missing_audit_profile) ... ok
test_agent_manifest_rejects_missing_security_profile (test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_missing_security_profile) ... ok
test_agent_manifest_rejects_unknown_worker_profile (test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_unknown_worker_profile) ... ok
test_agent_manifest_rejects_wrong_security_codex_model (test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_wrong_security_codex_model) ... ok
test_agent_manifest_requires_fable_advisor_on_the_worker_profile (test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_fable_advisor_on_the_worker_profile) ... ok
test_agent_manifest_requires_readme_to_document_restart_worker (test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_readme_to_document_restart_worker) ... ok
test_agent_manifest_requires_readme_to_state_the_worker_kind (test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_readme_to_state_the_worker_kind) ... ok
test_agmsg_installer_requires_a_release_pin_and_its_tag (test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_installer_requires_a_release_pin_and_its_tag) ... ok
test_agmsg_installer_requires_the_full_tag_commit (test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_installer_requires_the_full_tag_commit) ... ok
test_agmsg_installer_requires_the_npm_bootstrap_integrity (test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_installer_requires_the_npm_bootstrap_integrity) ... ok
test_agmsg_ownership_accepts_the_installer_layout (test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_accepts_the_installer_layout) ... ok
test_agmsg_ownership_rejects_a_managed_claude_command (test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_rejects_a_managed_claude_command) ... ok
test_agmsg_ownership_rejects_a_vendored_skill_copy (test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_rejects_a_vendored_skill_copy) ... ok
test_agmsg_ownership_rejects_removing_installer_owned_paths (test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_rejects_removing_installer_owned_paths) ... ok
test_agmsg_ownership_requires_retiring_the_symlink_farm (test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_requires_retiring_the_symlink_farm) ... ok
test_assets_accept_complete_declarations_and_rendered_versions (test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_accept_complete_declarations_and_rendered_versions) ... ok
test_assets_reject_a_malformed_render_entry (test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_a_malformed_render_entry) ... ok
test_assets_reject_each_incomplete_declaration (test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_each_incomplete_declaration) ... ok
test_assets_reject_one_assignment_rendered_from_two_fields (test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_one_assignment_rendered_from_two_fields) ... ok
test_assets_reject_one_assignment_rendered_through_a_symlink_alias (test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_one_assignment_rendered_through_a_symlink_alias) ... ok
test_assets_reject_unrendered_literal_versions_anywhere_in_install_or_scripts (test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_unrendered_literal_versions_anywhere_in_install_or_scripts) ... ok
test_assets_report_an_unrendered_declare_r_version (test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_report_an_unrendered_declare_r_version) ... ok
test_assets_scan_setup_sh_for_unrendered_versions (test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_scan_setup_sh_for_unrendered_versions) ... ok
test_claude_mcp_config_accepts_an_empty_map_and_rejects_a_non_mapping (test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_mcp_config_accepts_an_empty_map_and_rejects_a_non_mapping) ... ok
test_claude_permissions_allow_must_list_non_empty_rules (test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_permissions_allow_must_list_non_empty_rules) ... ok
test_claude_sandbox_accepts_manifest_symmetric_settings (test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_accepts_manifest_symmetric_settings) ... ok
test_claude_sandbox_extra_allow_write_must_be_absolute_or_home_paths_without_globs (test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_extra_allow_write_must_be_absolute_or_home_paths_without_globs) ... ok
test_claude_sandbox_rejects_each_broken_rule (test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_rejects_each_broken_rule) ... ok
test_claude_sandbox_requires_extra_codex_writable_roots (test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_requires_extra_codex_writable_roots) ... ok
test_claude_sandbox_unix_sockets_must_be_absolute_or_home_paths_without_globs (test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_unix_sockets_must_be_absolute_or_home_paths_without_globs) ... ok
test_codex_modify_script_requires_executable_source (test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_modify_script_requires_executable_source) ... ok
test_codex_projects_accept_working_tree_placeholder (test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_projects_accept_working_tree_placeholder) ... ok
test_codex_projects_reject_hard_coded_macos_home (test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_projects_reject_hard_coded_macos_home) ... ok
test_codex_projects_reject_missing_working_tree_placeholder (test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_projects_reject_missing_working_tree_placeholder) ... ok
test_codex_sandbox_workspace_write_accepts_matching_manifest (test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_sandbox_workspace_write_accepts_matching_manifest) ... ok
test_codex_sandbox_workspace_write_must_match_manifest (test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_sandbox_workspace_write_must_match_manifest) ... ok
test_codex_sandbox_workspace_write_requires_all_agmsg_roots (test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_sandbox_workspace_write_requires_all_agmsg_roots) ... ok
test_hook_composition_accepts_managed_source_fixture (test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_accepts_managed_source_fixture) ... ok
test_hook_composition_pins_sessionstart_order (test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_pins_sessionstart_order) ... ok
test_hook_composition_rejects_duplicate_command (test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_rejects_duplicate_command) ... ok
test_hook_composition_rejects_sync_timeout_over_budget (test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_rejects_sync_timeout_over_budget) ... ok
test_hook_composition_requires_permgate_first (test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_requires_permgate_first) ... ok
test_manifest_home_paths_allow_chezmoi_home_dir (test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_allow_chezmoi_home_dir) ... ok
test_manifest_home_paths_allow_flow_style_projects (test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_allow_flow_style_projects) ... ok
test_manifest_home_paths_exempt_runtime_owned_projects (test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_exempt_runtime_owned_projects) ... ok
test_manifest_home_paths_only_exempt_the_projects_subtree (test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_only_exempt_the_projects_subtree) ... ok
test_manifest_home_paths_reject_hard_coded_home (test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_reject_hard_coded_home) ... ok
test_manifest_home_paths_reject_hard_coded_linux_home (test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_reject_hard_coded_linux_home) ... ok
test_manifest_home_paths_reject_non_codex_projects_mapping (test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_reject_non_codex_projects_mapping) ... ok
test_permgate_policy_requires_a_schema_3_object (test_validate_agent_assets.ValidateAgentAssetsTest.test_permgate_policy_requires_a_schema_3_object) ... ok
test_recursive_scans_skip_nested_git_trees_only (test_validate_agent_assets.ValidateAgentAssetsTest.test_recursive_scans_skip_nested_git_trees_only) ... ok
test_repo_claude_settings_accept_portable_interpreter (test_validate_agent_assets.ValidateAgentAssetsTest.test_repo_claude_settings_accept_portable_interpreter) ... ok
test_repo_claude_settings_reject_machine_specific_interpreter (test_validate_agent_assets.ValidateAgentAssetsTest.test_repo_claude_settings_reject_machine_specific_interpreter) ... ERROR: /tmp/validate-agent-assets-test-e5dl_e9s/.claude/settings.json hook SessionEnd must not hard-code a machine-specific home path: /Users/mryfmo/.local/share/mise/installs/python/3.14.7/bin/python3.14
ok
test_secret_scan_allows_exact_placeholder_tokens (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_allows_exact_placeholder_tokens) ... ok
test_secret_scan_checks_docs_paths (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_docs_paths) ... ok
test_secret_scan_checks_extensionless_executables (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_extensionless_executables) ... ok
test_secret_scan_checks_utf16_bom_text (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_utf16_bom_text) ... ok
test_secret_scan_fails_a_nul_in_orchestration_text_and_skips_other_binaries (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_fails_a_nul_in_orchestration_text_and_skips_other_binaries) ... ok
test_secret_scan_reads_json_per_key_and_string_value (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_reads_json_per_key_and_string_value) ... ok
test_secret_scan_rejects_placeholder_with_suffix (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_rejects_placeholder_with_suffix) ... ok
test_secret_scan_rejects_utf16_orchestration_text_with_the_nul_offset (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_rejects_utf16_orchestration_text_with_the_nul_offset) ... ok
test_checkout_does_not_persist_credentials_without_explicit_exemption (test_workflow_security.WorkflowSecurityTest.test_checkout_does_not_persist_credentials_without_explicit_exemption) ... ok
test_checkout_rejects_duplicate_or_non_false_credential_settings (test_workflow_security.WorkflowSecurityTest.test_checkout_rejects_duplicate_or_non_false_credential_settings) ... ok
test_checkout_setting_does_not_leak_from_the_next_step (test_workflow_security.WorkflowSecurityTest.test_checkout_setting_does_not_leak_from_the_next_step) ... ok
test_external_actions_use_full_commit_shas (test_workflow_security.WorkflowSecurityTest.test_external_actions_use_full_commit_shas) ... ok
test_quoted_unnamed_checkout_is_detected (test_workflow_security.WorkflowSecurityTest.test_quoted_unnamed_checkout_is_detected) ... ok
test_unnamed_checkout_setting_does_not_leak_from_the_next_step (test_workflow_security.WorkflowSecurityTest.test_unnamed_checkout_setting_does_not_leak_from_the_next_step) ... ok
test_workflows_have_exact_top_level_permissions (test_workflow_security.WorkflowSecurityTest.test_workflows_have_exact_top_level_permissions) ... ok
test_workflows_have_no_job_level_permission_overrides (test_workflow_security.WorkflowSecurityTest.test_workflows_have_no_job_level_permission_overrides) ... ok

----------------------------------------------------------------------
Ran 778 tests in 194.973s

OK
```

## make render-check on final head; exit0

```text
uv run --with pyyaml scripts/generate-agent-configs.py --check
generated agent configs are up to date
```

## make validate-agent-assets on final head; exit0

```text
uv run --with pyyaml scripts/validate-agent-assets.py
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/autoskill/runs/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/learning/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/reports/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/sandboxes/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/validation/dotfiles-T90-github-identity-separation-a01-worker-crit.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/validation/dotfiles-T90-github-identity-separation-a01-worker-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/validation/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: additional worker workspace still open: dotfiles worker worker-d (herdr-agents --remove-worker)
WARN: regime-boundary: additional worker tab still open in dotfiles: dotfiles:codex-security-dot-a007 (herdr-agents --remove-worker)
agent asset validation ok
```

## shfmt diff on launcher and doctor; exit0

```text
```

## shellcheck launcher and doctor; exit0

```text
```

## Prettier check README, SKILL and integration rule; exit0

```text
Checking formatting...
All matched files use Prettier code style!
```

## Ruff format --config ruff.toml --check six Python files; exit0

```text
6 files already formatted
```

## gh pr checks 262 on final head; exit0

```text
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37220833846/job/111490653543	
private-bootstrap (macos-14, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37220833865/job/111490653843	
private-bootstrap (ubuntu-24.04, client)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37220833865/job/111490653856	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37220833865/job/111490653887	
public-bootstrap (macos-14, client)	pass	8m2s	https://github.com/mryfmo/dotfiles/actions/runs/37220833865/job/111490653855	
public-bootstrap (ubuntu-24.04, client)	pass	7m4s	https://github.com/mryfmo/dotfiles/actions/runs/37220833865/job/111490653923	
public-bootstrap (ubuntu-24.04, server)	pass	7m25s	https://github.com/mryfmo/dotfiles/actions/runs/37220833865/job/111490653701	
test (macos-14, client)	pass	6m32s	https://github.com/mryfmo/dotfiles/actions/runs/37220833846/job/111490680120	
test (ubuntu-24.04, client)	pass	7m26s	https://github.com/mryfmo/dotfiles/actions/runs/37220833846/job/111490680171	
test (ubuntu-24.04, server)	pass	4m19s	https://github.com/mryfmo/dotfiles/actions/runs/37220833846/job/111490680067	
test (ubuntu-26.04, client)	pass	8m9s	https://github.com/mryfmo/dotfiles/actions/runs/37220833846/job/111490680081	
validate	pass	27s	https://github.com/mryfmo/dotfiles/actions/runs/37220833834/job/111490653521	

```

## gh api pull metadata; exit0

```text
{"base":"8cd66881021c4bffe28d5a3d2ba75aba76e76665","head":"507e9c159d6ce73998ca70e79ac3951c04f81ff6","mergeable_state":"blocked"}

```

## Final diff stat against origin/main; exit0

```text
 README.md                                          |  76 ++++++++++++++-
 home/dot_agents/agent-config.yaml                  |   2 +
 home/dot_agents/model-profiles.env                 |   1 +
 .../dot_agents/skills/agmsg-orchestration/SKILL.md |   2 +-
 home/dot_config/claude/rules/pr-integration.md     |   2 +
 home/dot_local/bin/common/executable_herdr-agents  |  60 +++++++++++-
 scripts/check-tools.sh                             |  65 +++++++++++++
 scripts/generate-agent-configs.py                  |   6 +-
 scripts/require-crit-review.py                     |  80 ++++++++++++++++
 tests/unit/test_generate_agent_configs.py          |  19 ++++
 tests/unit/test_herdr_agents.py                    | 103 ++++++++++++++++++---
 tests/unit/test_require_crit_review.py             |  70 ++++++++++++++
 tests/unit/test_runtime_health.py                  |  61 +++++++++++-
 13 files changed, 527 insertions(+), 20 deletions(-)

```

## Final local review gate; exit0

```text
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.

```

## Late paginated Bot inline comments (prior head); exit0

```text
[[{"url":"https://api.github.com/repos/mryfmo/dotfiles/pulls/comments/4178600965","pull_request_review_id":5407325540,"id":4178600965,"node_id":"PRRC_kwDOSMyAV875EGQF","diff_hunk":"@@ -1008,6 +1008,74 @@ gh api -X POST repos/mryfmo/dotfiles/rulesets --input - <<'JSON'\n JSON\n ```\n \n+GitHub roles are configured separately. Workers (Claude and Codex, in the\n+pair, restarted pair workers, and `--add-worker` seats) use the manifest's\n+`worker_gh_config_dir`, default `~/.config/gh-worker`; the generated\n+`WORKER_GH_CONFIG_DIR` selects that directory at launch. The orchestrator\n+keeps the default gh configuration (`~/.config/gh`, or `$XDG_CONFIG_HOME/gh`).\n+Worker launches clear `GH_TOKEN`, `GITHUB_TOKEN` and their enterprise variants,\n+which otherwise take precedence over stored credentials. Codex workers also\n+receive a worker-only `shell_environment_policy.set.GH_CONFIG_DIR` override so\n+their shell tools retain the selection with `inherit=core`.\n+\n+Operator phase (once per machine, outside the sandbox): authenticate the\n+orchestrator with the merging account in its default gh config, then log into\n+the worker config as a different account with repository write access. Do not\n+give the worker a ruleset bypass. Use the manifest path if customized:\n+\n+```bash\n+unset GH_CONFIG_DIR GH_TOKEN GITHUB_TOKEN GH_ENTERPRISE_TOKEN GITHUB_ENTERPRISE_TOKEN\n+gh auth login --hostname github.com\n+gh api user --jq .login\n+umask 077\n+mkdir -p \"$HOME/.config/gh-worker\"\n+GH_CONFIG_DIR=\"$HOME/.config/gh-worker\" gh auth login --hostname github.com --git-protocol https --insecure-storage\n+chmod 600 \"$HOME/.config/gh-worker/hosts.yml\"\n+GH_CONFIG_DIR=\"$HOME/.config/gh-worker\" gh auth setup-git --hostname github.com\n+GH_CONFIG_DIR=\"$HOME/.config/gh-worker\" gh auth status --active --hostname github.com\n+make doctor\n+```\n+\n+`--insecure-storage` deliberately uses gh's token file: the Claude Linux\n+sandbox cannot reach the host keyring. Keep `hosts.yml` user-owned, mode 0600,\n+and outside the repository. The default path is readable under the managed\n+Claude and Codex sandbox policies; a custom path must also be readable.","path":"README.md","commit_id":"507e9c159d6ce73998ca70e79ac3951c04f81ff6","original_commit_id":"01ce1acc44b15620879b148a714e67dceaebedfd","user":{"login":"chatgpt-codex-connector[bot]","id":199175422,"node_id":"BOT_kgDOC98s_g","avatar_url":"https://avatars.githubusercontent.com/in/1144995?v=4","gravatar_id":"","url":"https://api.github.com/users/chatgpt-codex-connector%5Bbot%5D","html_url":"https://github.com/apps/chatgpt-codex-connector","followers_url":"https://api.github.com/users/chatgpt-codex-connector%5Bbot%5D/followers","following_url":"https://api.github.com/users/chatgpt-codex-connector%5Bbot%5D/following{/other_user}","gists_url":"https://api.github.com/users/chatgpt-codex-connector%5Bbot%5D/gists{/gist_id}","starred_url":"https://api.github.com/users/chatgpt-codex-connector%5Bbot%5D/starred{/owner}{/repo}","subscriptions_url":"https://api.github.com/users/chatgpt-codex-connector%5Bbot%5D/subscriptions","organizations_url":"https://api.github.com/users/chatgpt-codex-connector%5Bbot%5D/orgs","repos_url":"https://api.github.com/users/chatgpt-codex-connector%5Bbot%5D/repos","events_url":"https://api.github.com/users/chatgpt-codex-connector%5Bbot%5D/events{/privacy}","received_events_url":"https://api.github.com/users/chatgpt-codex-connector%5Bbot%5D/received_events","type":"Bot","user_view_type":"public","site_admin":false},"body":"**<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Update worker playbooks for isolated credentials**\n\nAfter the `hosts.yml` provisioning documented here, `home/dot_agents/skills/agmsg-orchestration/SKILL.md:169` and the mirrored `home/dot_config/claude/rules/agmsg-orchestration.md:16` still tell Claude workers to bypass the sandbox for authenticated `gh`, `git fetch`, and `git push` “until dotfiles-T90” provides this credential. Thus, on a provisioned machine, workers continue using the permission-gated out-of-sandbox path instead of the new in-sandbox file-backed identity; retire that exception (or make it apply only when provisioning is absent or broken) in both playbooks.\n\nAGENTS.md reference: [AGENTS.md:L71-L72](https://github.com/mryfmo/dotfiles/blob/01ce1acc44b15620879b148a714e67dceaebedfd/AGENTS.md#L71-L72)\n\nUseful? React with 👍 / 👎.","created_at":"2026-10-04T17:23:54Z","updated_at":"2026-10-04T17:23:54Z","html_url":"https://github.com/mryfmo/dotfiles/pull/262#discussion_r4178600965","pull_request_url":"https://api.github.com/repos/mryfmo/dotfiles/pulls/262","_links":{"self":{"href":"https://api.github.com/repos/mryfmo/dotfiles/pulls/comments/4178600965"},"html":{"href":"https://github.com/mryfmo/dotfiles/pull/262#discussion_r4178600965"},"pull_request":{"href":"https://api.github.com/repos/mryfmo/dotfiles/pulls/262"}},"reactions":{"url":"https://api.github.com/repos/mryfmo/dotfiles/pulls/comments/4178600965/reactions","total_count":0,"+1":0,"-1":0,"laugh":0,"hooray":0,"confused":0,"heart":0,"rocket":0,"eyes":0},"start_line":1039,"original_start_line":1039,"start_side":"RIGHT","line":1042,"original_line":1042,"side":"RIGHT","author_association":"NONE","original_position":57,"position":57,"subject_type":"line"}]]
```

## GraphQL thread resolution state; exit0

```text
{"data":{"repository":{"pullRequest":{"reviewThreads":{"nodes":[{"id":"PRRT_kwDOSMyAV86o0xpQ","isResolved":false,"isOutdated":false,"comments":{"nodes":[{"databaseId":4178600965,"url":"https://github.com/mryfmo/dotfiles/pull/262#discussion_r4178600965"}]}}]}}}}}
```

`herdr tab create --help` confirms installed CLI supports `--env <KEY=VALUE>` for launched-process environment; full upstream driver fixture validation is recorded above.

## Final-head Bot wait

```text
Diff head: 507e9c159d6ce73998ca70e79ac3951c04f81ff6
Wait started: 2026-10-04T17:31:42.830523+00:00
bot: none (15-minute bounded wait)
Wait finished: 2026-10-04T17:46:43.318366+00:00
```

The late review described above belongs to prior head01ce1acc; no Bot review of507e9c15 arrived by the final-head deadline.

## Final readiness snapshot

`gh pr checks 262` (exit0):

```text
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37220833846/job/111490653543	
private-bootstrap (macos-14, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37220833865/job/111490653843	
private-bootstrap (ubuntu-24.04, client)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37220833865/job/111490653856	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37220833865/job/111490653887	
public-bootstrap (macos-14, client)	pass	8m2s	https://github.com/mryfmo/dotfiles/actions/runs/37220833865/job/111490653855	
public-bootstrap (ubuntu-24.04, client)	pass	7m4s	https://github.com/mryfmo/dotfiles/actions/runs/37220833865/job/111490653923	
public-bootstrap (ubuntu-24.04, server)	pass	7m25s	https://github.com/mryfmo/dotfiles/actions/runs/37220833865/job/111490653701	
test (macos-14, client)	pass	6m32s	https://github.com/mryfmo/dotfiles/actions/runs/37220833846/job/111490680120	
test (ubuntu-24.04, client)	pass	7m26s	https://github.com/mryfmo/dotfiles/actions/runs/37220833846/job/111490680171	
test (ubuntu-24.04, server)	pass	4m19s	https://github.com/mryfmo/dotfiles/actions/runs/37220833846/job/111490680067	
test (ubuntu-26.04, client)	pass	8m9s	https://github.com/mryfmo/dotfiles/actions/runs/37220833846/job/111490680081	
validate	pass	27s	https://github.com/mryfmo/dotfiles/actions/runs/37220833834/job/111490653521	
```

`gh api repos/mryfmo/dotfiles/pulls/262 --jq <head/base/mergeable_state>` (exit0):

```json
{"base":"8cd66881021c4bffe28d5a3d2ba75aba76e76665","head":"507e9c159d6ce73998ca70e79ac3951c04f81ff6","mergeable_state":"blocked"}
```

`gh api repos/mryfmo/dotfiles/git/ref/heads/main --jq .object.sha` (exit0):

```text
8cd66881021c4bffe28d5a3d2ba75aba76e76665
```

The blocked mergeability is the unresolved late Bot thread; conflict-free mergeability and passing checks are separate facts. Worker does not resolve threads or merge.

## Completion make validate-agent-assets; exit0

```text
uv run --with pyyaml scripts/validate-agent-assets.py
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/autoskill/runs/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/learning/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/reports/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/sandboxes/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/validation/dotfiles-T90-github-identity-separation-a01-worker-crit.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/validation/dotfiles-T90-github-identity-separation-a01-worker-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/validation/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: additional worker workspace still open: dotfiles worker worker-d (herdr-agents --remove-worker)
WARN: regime-boundary: additional worker tab still open in dotfiles: dotfiles:codex-security-dot-a007 (herdr-agents --remove-worker)
agent asset validation ok
```

## Completion review gate with all resolved local findings; exit0

```text
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.
```

## Revise round 1

Only README changed in the revision commit; code and tests remain identical to the 778-test implementation run at 507e9c15. Independent reviewer /root/t97_evidence_review returned no actionable findings and Verdict: correct for README and report completion item 4. No CompactionDB command was run; orchestrator records it at acceptance.

### /tmp/t90-revise-prettier.log

```text
Checking formatting...
[warn] README.md
[warn] Code style issues found in the above file. Run Prettier with --write to fix.
```

### /tmp/t90-revise-format.log

```text
README.md 128ms
Checking formatting...
All matched files use Prettier code style!
```

### /tmp/t90-revise-crit-status.log

```text
{
  "branch": "feat/github-identity-separation",
  "daemon": {
    "running": false
  },
  "review_file": "/home/moriya/.crit/reviews/7fd1f01ac41b/review.json",
  "review_file_exists": false,
  "sessions": [],
  "vcs": "git"
}
```

### /tmp/t90-revise-gate.log

```text
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.
```

### /tmp/t90-revise-commit.log

```text
[feat/github-identity-separation e2d5c9a3] docs: defer GitHub merge restrictions to T90b
 1 file changed, 46 insertions(+), 38 deletions(-)
e2d5c9a3fdae30f6137c5e5fb5cae785691a66fd
```

### /tmp/t90-revise-push.log

```text
To github.com:mryfmo/dotfiles.git
   507e9c15..e2d5c9a3  feat/github-identity-separation -> feat/github-identity-separation
```

### /tmp/t90-revise-pr-edit.log

```text
https://github.com/mryfmo/dotfiles/pull/262
```

### /tmp/t90-revise-assets.log

```text
uv run --with pyyaml scripts/validate-agent-assets.py
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/acceptance/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/autoskill/runs/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/learning/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/reports/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/sandboxes/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/tasks/dotfiles-T90b-ruleset-sole-merger-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T90-github-identity-separation-a01-audit-507e9c1.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T90-github-identity-separation-a01-audit-507e9c1.md.last.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T90-github-identity-separation-a01-crit.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T90-github-identity-separation-a01-pr-feedback.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T90-github-identity-separation-a01-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T90-github-identity-separation-a01-worker-crit.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T90-github-identity-separation-a01-worker-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/autoskill/runs/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/learning/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/reports/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/sandboxes/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/validation/dotfiles-T90-github-identity-separation-a01-worker-crit.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/validation/dotfiles-T90-github-identity-separation-a01-worker-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/validation/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: additional worker workspace still open: dotfiles worker worker-d (herdr-agents --remove-worker)
WARN: regime-boundary: additional worker tab still open in dotfiles: dotfiles:codex-security-dot-a007 (herdr-agents --remove-worker)
agent asset validation ok
```

### /tmp/t90-revise-mergeable.log

```text
{"base":"8cd66881021c4bffe28d5a3d2ba75aba76e76665","head":"e2d5c9a3fdae30f6137c5e5fb5cae785691a66fd","mergeable":true,"mergeable_state":"blocked","number":262}
```

### /tmp/t90-revise-scope.log

```text
README.md
02ce714034a48ce384b6d8c10a628fbf19f6730e55ef192b2e9e6e04f93e644f  /home/moriya/Workspace/dotfiles/.orchestration/tasks/dotfiles-T90-github-identity-separation-a01.md
 README.md                                          | 130 ++++++++++++++++-----
 home/dot_agents/agent-config.yaml                  |   2 +
 home/dot_agents/model-profiles.env                 |   1 +
 .../dot_agents/skills/agmsg-orchestration/SKILL.md |   2 +-
 home/dot_config/claude/rules/pr-integration.md     |   2 +
 home/dot_local/bin/common/executable_herdr-agents  |  60 +++++++++-
 scripts/check-tools.sh                             |  65 +++++++++++
 scripts/generate-agent-configs.py                  |   6 +-
 scripts/require-crit-review.py                     |  80 +++++++++++++
 tests/unit/test_generate_agent_configs.py          |  19 +++
 tests/unit/test_herdr_agents.py                    | 103 ++++++++++++++--
 tests/unit/test_require_crit_review.py             |  70 +++++++++++
 tests/unit/test_runtime_health.py                  |  61 +++++++++-
 13 files changed, 558 insertions(+), 43 deletions(-)
```

### /tmp/t90-revise-ci-final.log

```text
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
public-bootstrap (macos-14, client)	pass	9m11s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
public-bootstrap (ubuntu-24.04, client)	pass	8m43s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
public-bootstrap (ubuntu-24.04, server)	pass	7m24s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
test (macos-14, client)	pass	5m49s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
test (ubuntu-24.04, client)	pass	7m42s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
test (ubuntu-24.04, server)	pass	4m20s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
test (ubuntu-26.04, client)	pass	7m49s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
```

### /tmp/t90-revise-mergeable-final.log

```text
{"base":"8cd66881021c4bffe28d5a3d2ba75aba76e76665","head":"e2d5c9a3fdae30f6137c5e5fb5cae785691a66fd","mergeable":true,"mergeable_state":"clean","number":262}
```

### Current review-thread state (worker did not resolve)

```json
{"data":{"repository":{"pullRequest":{"reviewThreads":{"nodes":[{"id":"PRRT_kwDOSMyAV86o0xpQ","isResolved":true,"comments":{"nodes":[{"databaseId":4178600965,"url":"https://github.com/mryfmo/dotfiles/pull/262#discussion_r4178600965","body":"**<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Update worker playbooks for isolated credentials**\n\nAfter the `hosts.yml` provisioning documented here, `home/dot_agents/skills/agmsg-orchestration/SKILL.md:169` and the mirrored `home/dot_config/claude/rules/agmsg-orchestration.md:16` still tell Claude workers to bypass the sandbox for authenticated `gh`, `git fetch`, and `git push` “until dotfiles-T90” provides this credential. Thus, on a provisioned machine, workers continue using the permission-gated out-of-sandbox path instead of the new in-sandbox file-backed identity; retire that exception (or make it apply only when provisioning is absent or broken) in both playbooks.\n\nAGENTS.md reference: [AGENTS.md:L71-L72](https://github.com/mryfmo/dotfiles/blob/01ce1acc44b15620879b148a714e67dceaebedfd/AGENTS.md#L71-L72)\n\nUseful? React with 👍 / 👎."}]}}]}}}}}
```

### /tmp/t90-revise-ci.log

```text
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
validate	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
test (ubuntu-24.04, server)	pass	4m20s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
test (ubuntu-24.04, server)	pass	4m20s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
test (ubuntu-24.04, server)	pass	4m20s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
test (ubuntu-24.04, server)	pass	4m20s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
test (ubuntu-24.04, server)	pass	4m20s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
test (ubuntu-24.04, server)	pass	4m20s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
test (ubuntu-24.04, server)	pass	4m20s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
test (ubuntu-24.04, server)	pass	4m20s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
test (ubuntu-24.04, server)	pass	4m20s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
test (macos-14, client)	pass	5m49s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
test (ubuntu-24.04, server)	pass	4m20s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
test (macos-14, client)	pass	5m49s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
test (ubuntu-24.04, server)	pass	4m20s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
test (macos-14, client)	pass	5m49s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
test (ubuntu-24.04, server)	pass	4m20s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
test (macos-14, client)	pass	5m49s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
test (ubuntu-24.04, server)	pass	4m20s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
test (macos-14, client)	pass	5m49s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
test (ubuntu-24.04, server)	pass	4m20s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
test (macos-14, client)	pass	5m49s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
test (ubuntu-24.04, server)	pass	4m20s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
test (macos-14, client)	pass	5m49s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
test (ubuntu-24.04, server)	pass	4m20s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
public-bootstrap (ubuntu-24.04, server)	pass	7m24s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
test (macos-14, client)	pass	5m49s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
test (ubuntu-24.04, server)	pass	4m20s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
public-bootstrap (ubuntu-24.04, server)	pass	7m24s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
test (macos-14, client)	pass	5m49s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
test (ubuntu-24.04, server)	pass	4m20s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
public-bootstrap (ubuntu-24.04, server)	pass	7m24s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
test (macos-14, client)	pass	5m49s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
test (ubuntu-24.04, server)	pass	4m20s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
test (macos-14, client)	pass	5m49s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
test (ubuntu-24.04, server)	pass	4m20s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
public-bootstrap (ubuntu-24.04, server)	pass	7m24s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
test (ubuntu-24.04, client)	pass	7m42s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
test (macos-14, client)	pass	5m49s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
public-bootstrap (ubuntu-24.04, server)	pass	7m24s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
test (ubuntu-24.04, client)	pass	7m42s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
test (ubuntu-24.04, server)	pass	4m20s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
test (ubuntu-26.04, client)	pass	7m49s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
test (macos-14, client)	pass	5m49s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
public-bootstrap (ubuntu-24.04, server)	pass	7m24s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
test (ubuntu-24.04, client)	pass	7m42s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
test (ubuntu-24.04, server)	pass	4m20s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
test (ubuntu-26.04, client)	pass	7m49s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
test (macos-14, client)	pass	5m49s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
public-bootstrap (ubuntu-24.04, server)	pass	7m24s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
test (ubuntu-24.04, client)	pass	7m42s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
test (ubuntu-24.04, server)	pass	4m20s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
test (ubuntu-26.04, client)	pass	7m49s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
test (macos-14, client)	pass	5m49s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
public-bootstrap (ubuntu-24.04, server)	pass	7m24s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
test (ubuntu-24.04, client)	pass	7m42s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
test (ubuntu-24.04, server)	pass	4m20s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
test (ubuntu-26.04, client)	pass	7m49s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
public-bootstrap (ubuntu-24.04, client)	pass	8m43s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
public-bootstrap (ubuntu-24.04, server)	pass	7m24s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
test (macos-14, client)	pass	5m49s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
test (ubuntu-24.04, client)	pass	7m42s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
test (ubuntu-24.04, server)	pass	4m20s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
test (ubuntu-26.04, client)	pass	7m49s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
public-bootstrap (ubuntu-24.04, client)	pass	8m43s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
public-bootstrap (ubuntu-24.04, server)	pass	7m24s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
test (macos-14, client)	pass	5m49s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
test (ubuntu-24.04, client)	pass	7m42s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
test (ubuntu-24.04, server)	pass	4m20s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
test (ubuntu-26.04, client)	pass	7m49s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
public-bootstrap (ubuntu-24.04, client)	pass	8m43s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
public-bootstrap (ubuntu-24.04, server)	pass	7m24s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
test (macos-14, client)	pass	5m49s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
test (ubuntu-24.04, client)	pass	7m42s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
test (ubuntu-24.04, server)	pass	4m20s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
test (ubuntu-26.04, client)	pass	7m49s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
public-bootstrap (macos-14, client)	pass	9m11s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
public-bootstrap (ubuntu-24.04, client)	pass	8m43s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
public-bootstrap (ubuntu-24.04, server)	pass	7m24s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
test (macos-14, client)	pass	5m49s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
test (ubuntu-24.04, client)	pass	7m42s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
test (ubuntu-24.04, server)	pass	4m20s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
test (ubuntu-26.04, client)	pass	7m49s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495832006	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832313	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832422	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832457	
public-bootstrap (macos-14, client)	pass	9m11s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832468	
public-bootstrap (ubuntu-24.04, client)	pass	8m43s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832562	
public-bootstrap (ubuntu-24.04, server)	pass	7m24s	https://github.com/mryfmo/dotfiles/actions/runs/37222611614/job/111495832355	
test (macos-14, client)	pass	5m49s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864227	
test (ubuntu-24.04, client)	pass	7m42s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864336	
test (ubuntu-24.04, server)	pass	4m20s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864222	
test (ubuntu-26.04, client)	pass	7m49s	https://github.com/mryfmo/dotfiles/actions/runs/37222611507/job/111495864203	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37222611489/job/111495831855	
```

### /tmp/t90-revise-final-gate.log

```text
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.
```

### /tmp/t90-revise-final-status.log

```text
?? .orchestration/autoskill/runs/dotfiles-T90-github-identity-separation-a01.md
?? .orchestration/learning/dotfiles-T90-github-identity-separation-a01.md
?? .orchestration/reports/dotfiles-T90-github-identity-separation-a01.md
?? .orchestration/sandboxes/dotfiles-T90-github-identity-separation-a01.md
?? .orchestration/validation/dotfiles-T90-github-identity-separation-a01-worker-crit.json
?? .orchestration/validation/dotfiles-T90-github-identity-separation-a01-worker-review-receipt.md
?? .orchestration/validation/dotfiles-T90-github-identity-separation-a01.md
```

### /tmp/t90-revise-bot.log

```text
Diff head: e2d5c9a3fdae30f6137c5e5fb5cae785691a66fd
Wait started: 2026-10-04T18:00:07.187583+00:00
bot: none (15-minute bounded wait)
Wait finished: 2026-10-04T18:15:08.191862+00:00
```
